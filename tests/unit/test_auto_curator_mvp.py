"""Tests — Auto Curator (crecimiento autogestionado con verificación)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.observatory.engine import ObservatoryEngine
from backend.source_discovery import auto_curator


@pytest.fixture(autouse=True)
def env_limpio(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AUTO_CURATION", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)


@pytest.fixture
def observatory(tmp_path: Path) -> ObservatoryEngine:
    obs = ObservatoryEngine(data_dir=tmp_path / "obs")
    obs.log_query("mapa de riesgo de deslizamientos en mi vereda", channel="recommend", result_count=0)
    obs.log_query("datos de calidad del aire por comuna", channel="decision_support", result_count=1)
    return obs


@pytest.fixture
def sources_dir(tmp_path: Path) -> Path:
    d = tmp_path / "catalog"
    d.mkdir()
    return d


def _candidato_valido(url: str) -> dict:
    return {
        "id": "sirena-fake",
        "name": "Sirena Institucional",
        "institution": "Instituto Sirena",
        "url": url,
        "coverage": "Colombia",
        "domains": ["clima", "biodiversidad"],
        "keywords": ["sirena", "alertas", "clima"],
        "description": "Plataforma institucional de alertas climáticas.",
    }


def test_fuente_con_url_muerta_no_se_crea(
    monkeypatch: pytest.MonkeyPatch, observatory, sources_dir: Path
) -> None:
    monkeypatch.setattr(
        auto_curator, "_gemini",
        lambda prompt: [_candidato_valido("https://dominio-inexistente.example/")],
    )
    res = auto_curator.run_cycle(observatory, sources_dir=sources_dir,
                                 log_dir=sources_dir / "log")
    assert res["proposed"] == 1
    assert res["verified"] == 0
    assert res["geoservice_added"] == 0 and res["portal_added"] == 0
    assert not (sources_dir / "sirena-fake.json").exists()


def test_fuente_verificada_se_activa_con_provenance(
    monkeypatch: pytest.MonkeyPatch, observatory, sources_dir: Path
) -> None:
    monkeypatch.setattr(
        auto_curator, "_gemini",
        lambda prompt: [_candidato_valido("https://www.example.com/portal")],
    )
    monkeypatch.setattr(auto_curator, "probe_url", lambda url: True)
    res = auto_curator.run_cycle(observatory, sources_dir=sources_dir,
                                 log_dir=sources_dir / "log")
    assert res["portal_added"] == 1
    ficha = json.loads((sources_dir / "sirena-fake.json").read_text(encoding="utf-8"))
    assert ficha["status"] == "active"
    assert ficha["curation"] == "llm-verified"
    assert ficha["domains"] == ["clima", "biodiversidad"]


def test_geoservicio_verificado_es_recurso_primario(
    monkeypatch: pytest.MonkeyPatch, observatory, sources_dir: Path
) -> None:
    cand = _candidato_valido("https://www.example.com/portal")
    cand["geoservice_url"] = "https://www.example.com/arcgis/rest/services"
    cand["geoservice_type"] = "ArcGIS_REST"
    monkeypatch.setattr(auto_curator, "_gemini", lambda prompt: [cand])
    monkeypatch.setattr(auto_curator, "probe_geoservice", lambda url, tipo: True)
    res = auto_curator.run_cycle(observatory, sources_dir=sources_dir,
                                 log_dir=sources_dir / "log")
    assert res["geoservice_added"] == 1
    ficha = json.loads((sources_dir / "sirena-fake.json").read_text(encoding="utf-8"))
    assert ficha["resources"][0]["category"] == "geoservice"
    assert ficha["resources"][0]["url"] == cand["geoservice_url"]
    assert ficha["url"] == cand["geoservice_url"]


def test_geoservicio_fallido_cae_a_portal(
    monkeypatch: pytest.MonkeyPatch, observatory, sources_dir: Path
) -> None:
    cand = _candidato_valido("https://www.example.com/portal")
    cand["geoservice_url"] = "https://www.example.com/arcgis/rest/services"
    cand["geoservice_type"] = "ArcGIS_REST"
    monkeypatch.setattr(auto_curator, "_gemini", lambda prompt: [cand])
    monkeypatch.setattr(auto_curator, "probe_geoservice", lambda url, tipo: False)
    monkeypatch.setattr(auto_curator, "probe_url", lambda url: True)
    res = auto_curator.run_cycle(observatory, sources_dir=sources_dir,
                                 log_dir=sources_dir / "log")
    assert res["geoservice_added"] == 0
    assert res["portal_added"] == 1  # el portal verificado mantiene la fuente
    ficha = json.loads((sources_dir / "sirena-fake.json").read_text(encoding="utf-8"))
    assert ficha["resources"][0]["category"] == "portal"


def test_candidato_invalido_se_descarta(
    monkeypatch: pytest.MonkeyPatch, observatory, sources_dir: Path
) -> None:
    malo = _candidato_valido("https://www.example.com/portal")
    malo["id"] = "ID INVALIDO!!"
    malo["domains"] = ["astrologia"]  # dominio desconocido
    monkeypatch.setattr(auto_curator, "_gemini", lambda prompt: [malo])
    monkeypatch.setattr(auto_curator, "probe_url", lambda url: True)
    res = auto_curator.run_cycle(observatory, sources_dir=sources_dir,
                                 log_dir=sources_dir / "log")
    assert res["geoservice_added"] == 0 and res["portal_added"] == 0


def test_enriquecimiento_solo_agrega_keywords(
    monkeypatch: pytest.MonkeyPatch, observatory, sources_dir: Path
) -> None:
    # Ficha existente con keywords previas
    ficha = {
        "id": "fuente-x", "name": "Fuente X", "institution": "Inst X",
        "status": "active", "resources": [{"id": "fuente-x:portal",
                                            "name": "Portal", "keywords": ["clima"]}],
    }
    (sources_dir / "fuente-x.json").write_text(
        json.dumps(ficha, ensure_ascii=False), encoding="utf-8"
    )
    # Observatorio: consultas que mencionan fuente-x con términos nuevos
    obs = ObservatoryEngine(data_dir=sources_dir / "obs")
    obs.log_query("anomalias termicas fuente x", channel="recommend",
                  result_count=2, recommendations=[{"source_id": "fuente-x", "score": 80}],
                  terms=["anomalias", "termicas", "satelital"])
    monkeypatch.setattr(auto_curator, "_gemini", lambda prompt: ["anomalias_termicas", "satelital"])
    n = auto_curator.enrich_existing(obs._store.list_events(), sources_dir)
    assert n == 1
    nueva = json.loads((sources_dir / "fuente-x.json").read_text(encoding="utf-8"))
    kws = nueva["resources"][0]["keywords"]
    assert "clima" in kws  # keywords previas intactas
    assert "anomalias_termicas" in kws
    assert nueva["curation"] == "llm-enriched"


def test_sin_gaps_no_llama_a_gemini(
    monkeypatch: pytest.MonkeyPatch, sources_dir: Path
) -> None:
    obs = ObservatoryEngine(data_dir=sources_dir / "obs")
    # solo consultas con buenos resultados
    obs.log_query("inundaciones en microcuenca", channel="recommend",
                  result_count=6, recommendations=[{"source_id": "ideam", "score": 90}])
    llamado = []
    monkeypatch.setattr(auto_curator, "_gemini", lambda p: llamado.append(p) or [])
    res = auto_curator.run_cycle(obs, sources_dir=sources_dir,
                                 log_dir=sources_dir / "log")
    assert llamado == []
    assert "sin vacíos" in res.get("note", "")


def test_endpoint_requiere_auto_curation() -> None:
    from fastapi.testclient import TestClient

    from backend.api.main import app

    with TestClient(app) as client:
        res = client.post("/source-discovery/auto-curate")
        assert res.status_code == 403  # AUTO_CURATION apagada por defecto
