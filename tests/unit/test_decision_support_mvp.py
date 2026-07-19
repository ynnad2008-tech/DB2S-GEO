"""Tests — Decision Support Engine MVP (Fase 8)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.api.main import app
from backend.decision_support.concepts import expand_concepts
from backend.decision_support.engine import DecisionSupportEngine
from backend.decision_support.intents import detect_intents
from backend.discovery.engine import DiscoveryEngine
from backend.knowledge_graph.engine import KnowledgeGraphEngine
from backend.metadata.engine import MetadataEngine
from backend.recommendation.engine import RecommendationEngine

MVP = {"ideam", "invemar", "gbif", "fao", "worldpop", "gee"}


@pytest.fixture
def dss() -> DecisionSupportEngine:
    discovery = DiscoveryEngine()
    metadata = MetadataEngine(discovery)
    kg = KnowledgeGraphEngine(discovery, metadata)
    rec = RecommendationEngine(kg, discovery, metadata)
    return DecisionSupportEngine(rec, discovery, metadata, kg)


def test_concept_aliases() -> None:
    assert "hidrologia" in expand_concepts("agua")
    assert "precipitacion" in expand_concepts("lluvia")
    concepts = expand_concepts("inundaciones en microcuenca")
    assert "hidrologia" in concepts
    assert "precipitacion" in concepts
    assert "suelos" in expand_concepts("erosion")


def test_detect_intents() -> None:
    assert "analizar" in detect_intents("Necesito analizar inundaciones")
    assert "descargar" in detect_intents("Quiero descargar datos de precipitación")
    assert "monitorear" in detect_intents("monitorear manglares")


def test_advise_inundaciones(dss: DecisionSupportEngine) -> None:
    payload = dss.advise("Necesito analizar inundaciones en una microcuenca")
    assert payload["ai"] is False
    assert payload["count"] >= 3
    assert payload["need"]
    source_ids = {r["source_id"] for r in payload["routes"]}
    assert "ideam" in source_ids
    assert "gee" in source_ids
    assert "worldpop" in source_ids

    for route in payload["routes"]:
        assert route["what_to_do"]
        assert route["where"]
        assert route["source_id"] in MVP
        assert route["why"]
        assert "category" in route
        assert "resources" in route


def test_advise_precipitacion_routes(dss: DecisionSupportEngine) -> None:
    payload = dss.advise("Quiero datos de precipitación")
    assert payload["count"] >= 1
    sources = {r["source_id"] for r in payload["routes"]}
    assert "ideam" in sources
    # Debe orientar a descarga/consulta institucional
    cats = {r["category"] for r in payload["routes"]}
    assert "descargar_datos" in cats or "consultar_informacion_institucional" in cats


def test_only_mvp_sources(dss: DecisionSupportEngine) -> None:
    payload = dss.advise("biodiversidad y especies")
    for route in payload["routes"]:
        assert route["source_id"] in MVP
        assert route["source"] != "CHIRPS"


def test_empty_query(dss: DecisionSupportEngine) -> None:
    payload = dss.advise("")
    assert payload["count"] == 0
    assert payload["routes"] == []


def test_api_decision_support() -> None:
    with TestClient(app) as client:
        info = client.get("/decision-support/info")
        assert info.status_code == 200
        assert info.json()["engine"] == "DecisionSupportEngine"
        assert info.json()["ai"] is False

        res = client.get(
            "/decision-support",
            params={"q": "Necesito analizar inundaciones en una microcuenca"},
        )
        assert res.status_code == 200
        body = res.json()
        assert body["count"] >= 3
        assert any(r["source_id"] == "ideam" for r in body["routes"])

        missing = client.get("/decision-support")
        assert missing.status_code == 422

        root = client.get("/")
        assert "GET /decision-support?q=" in root.json()["endpoints"]
        assert root.json()["version"].startswith("0.9")

        health = client.get("/health")
        assert "decision_support" in health.json()
