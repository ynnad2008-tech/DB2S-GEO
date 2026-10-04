"""Tests — filtro coverage (cobertura geográfica curada)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.api.main import app
from backend.decision_support.engine import DecisionSupportEngine
from backend.discovery.engine import DiscoveryEngine
from backend.knowledge_graph.engine import KnowledgeGraphEngine
from backend.metadata.coverage import detect_coverage, matches_coverage, normalize_coverage
from backend.metadata.engine import MetadataEngine
from backend.recommendation.engine import RecommendationEngine


# --- unidad: matches_coverage ---

def test_cobertura_subnacional_exacta() -> None:
    assert matches_coverage("Tolima", "tolima")
    assert not matches_coverage("Cali", "tolima")


def test_cobertura_nacional_cubre_subnacional() -> None:
    assert matches_coverage("Colombia", "tolima")
    assert matches_coverage("Colombia (32 departamentos según operación)", "tolima")


def test_departamento_cubre_sus_ciudades() -> None:
    assert matches_coverage("Valle del Cauca", "cali")
    assert not matches_coverage("Antioquia", "cali")


def test_global_segun_include_global() -> None:
    assert matches_coverage("Global", "tolima", include_global=True)
    assert not matches_coverage("Global", "tolima", include_global=False)
    assert matches_coverage("Global", "colombia", include_global=True)


def test_cobertura_colombia_incluye_subnacionales() -> None:
    assert matches_coverage("Tolima", "colombia")
    assert matches_coverage("Valle del Cauca", "colombia")
    assert matches_coverage("Amazonía", "colombia")
    assert not matches_coverage("Honduras", "colombia")


def test_cobertura_paises_regionales() -> None:
    # Nacional cubre sus subnacionales
    assert matches_coverage("Honduras", "honduras")
    assert matches_coverage("Honduras", "tegucigalpa")
    assert matches_coverage("Costa Rica", "san_jose")
    assert matches_coverage("Perú", "cusco")
    assert matches_coverage("México", "guadalajara")
    # Países no se cruzan
    assert not matches_coverage("Honduras", "colombia")
    assert not matches_coverage("Costa Rica", "honduras")
    assert not matches_coverage("Perú", "mexico")
    # Global opcional
    assert matches_coverage("Global", "honduras", include_global=True)
    assert not matches_coverage("Global", "honduras", include_global=False)


def test_detecta_paises_regionales() -> None:
    assert detect_coverage("datos de precipitacion en tegucigalpa") == "tegucigalpa"
    assert detect_coverage("ordenamiento territorial en san jose") == "san_jose"
    assert detect_coverage("inundaciones en honduras") == "honduras"
    assert detect_coverage("cuencas en costa rica") == "costa_rica"


def test_normalize_coverage_limpia_parentesis() -> None:
    assert normalize_coverage("Colombia (32 departamentos según operación)") == "colombia"
    assert normalize_coverage("Valle del Cauca") == "valle_del_cauca"


# --- unidad: detect_coverage ---

def test_detecta_cobertura_desde_consulta() -> None:
    assert detect_coverage("necesito datos de precipitacion en el tolima") == "tolima"
    assert detect_coverage("ordenamiento territorial en cali") == "cali"
    assert detect_coverage("cuenca del magdalena") == "cuenca_del_magdalena"
    assert detect_coverage("valle del cauca") == "valle_del_cauca"


def test_no_detecta_falsos_positivos() -> None:
    assert detect_coverage("metadatos del catálogo") is None  # no "meta"
    assert detect_coverage("calidad del agua") is None  # no "cali"
    assert detect_coverage("precipitacion") is None


# --- regresión: expansión de tokens sin encadenamiento transitivo ---

def test_expansion_tokens_un_solo_salto() -> None:
    from backend.recommendation.scoring import expand_query_tokens

    tokens = expand_query_tokens(
        "susceptibilidad al cambio de temperaturas en ecosistemas marinos"
    )
    # relevantes presentes
    assert "temperatura" in tokens
    assert "tsm" in tokens
    assert "ecosistemas" in tokens
    assert "marino" in tokens
    assert "oceanos_costas" in tokens
    # ruido transitivo ausente (antes: bahia → caribe → morfometria…)
    assert "bahia" not in tokens
    assert "barranquilla" not in tokens
    assert "alos_palsar" not in tokens
    assert "dem" not in tokens
    assert "deslizamiento" not in tokens


# --- API: /sources?coverage= ---

@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


def test_sources_coverage_tolima(client: TestClient) -> None:
    r = client.get("/sources", params={"coverage": "tolima"})
    assert r.status_code == 200
    ids = {s["source_id"] for s in r.json()["sources"]}
    assert "gob-tolima" in ids
    assert "ideam" in ids  # nacional cubre tolima
    assert "cartagena" not in ids  # otra ciudad queda fuera
    assert "gbif" in ids  # global incluido por defecto


def test_sources_coverage_cali_sin_globales(client: TestClient) -> None:
    r = client.get("/sources", params={"coverage": "cali", "include_global": False})
    ids = {s["source_id"] for s in r.json()["sources"]}
    assert "cali" in ids
    assert "gbif" not in ids
    assert "gee" not in ids
    assert "gob-valle" in ids  # departamento cubre sus ciudades


# --- API: /recommend?coverage= ---

def test_recommend_coverage_cali_excluye_otras_ciudades(client: TestClient) -> None:
    r = client.get("/recommend", params={"q": "ordenamiento territorial", "coverage": "cali"})
    body = r.json()
    ids = {x["source_id"] for x in body["recommendations"]}
    assert "cali" in ids
    assert "barranquilla" not in ids
    assert "cartagena" not in ids


# --- Decision Support: auto-detección ---

@pytest.fixture
def dss() -> DecisionSupportEngine:
    discovery = DiscoveryEngine()
    metadata = MetadataEngine(discovery)
    kg = KnowledgeGraphEngine(discovery, metadata)
    rec = RecommendationEngine(kg, discovery, metadata)
    return DecisionSupportEngine(rec, discovery, metadata, kg)


def test_advise_cali_no_recomienda_otras_ciudades(dss: DecisionSupportEngine) -> None:
    payload = dss.advise("que fuentes hay para ordenamiento territorial en cali")
    assert payload["coverage"]["requested"] == "cali"
    assert payload["coverage"]["detected_auto"] is True
    ids = {r["source_id"] for r in payload["routes"]}
    assert "cali" in ids
    assert "barranquilla" not in ids
    assert "cartagena" not in ids
    assert "gob-antioquia" not in ids


def test_advise_sin_cobertura_no_filtra(dss: DecisionSupportEngine) -> None:
    payload = dss.advise("precipitacion")
    assert payload["coverage"]["requested"] is None
    assert payload["coverage"]["detected_auto"] is False
