"""Tests — Recommendation Engine MVP (Fase 4)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.discovery.engine import DiscoveryEngine
from backend.knowledge_graph.engine import KnowledgeGraphEngine
from backend.metadata.engine import MetadataEngine
from backend.recommendation.engine import RecommendationEngine
from connectors.registry import MVP_CONNECTOR_IDS


@pytest.fixture
def rec() -> RecommendationEngine:
    discovery = DiscoveryEngine()
    metadata = MetadataEngine(discovery)
    kg = KnowledgeGraphEngine(discovery, metadata)
    return RecommendationEngine(kg, discovery, metadata)


def test_recommend_precipitacion(rec: RecommendationEngine) -> None:
    payload = rec.recommend("precipitacion")
    assert payload["count"] >= 1
    assert payload["ai"] is False
    top = payload["recommendations"][0]
    assert top["source"] in {"IDEAM", "Google Earth Engine", "NASA"}
    assert top["score"] >= 50
    assert "reason" in top and top["reason"]
    assert "relations_used" in top and top["relations_used"]
    ideam = next(r for r in payload["recommendations"] if r["source"] == "IDEAM")
    assert ideam["score"] >= 50
    assert any("precipitacion" in r or "keyword" in r for r in ideam["reason"])


def test_no_recommendation_without_justification(rec: RecommendationEngine) -> None:
    payload = rec.recommend("precipitacion")
    for item in payload["recommendations"]:
        assert item["reason"]
        assert item["relations_used"]
        assert 0 <= item["score"] <= 100


def test_recommend_by_domain_clima(rec: RecommendationEngine) -> None:
    payload = rec.recommend_by_domain("clima")
    assert payload["count"] >= 1
    sources = {r["source"] for r in payload["recommendations"]}
    assert "IDEAM" in sources


def test_recommend_by_source_ideam(rec: RecommendationEngine) -> None:
    payload = rec.recommend_by_source("ideam")
    assert payload["count"] >= 1
    assert any(r["source_id"] == "ideam" for r in payload["recommendations"])


def test_recommend_by_resource(rec: RecommendationEngine) -> None:
    payload = rec.recommend_by_resource("ideam:consulta-meteorologica")
    assert payload["count"] >= 1
    assert any(r["source_id"] == "ideam" for r in payload["recommendations"])


def test_only_mvp_sources(rec: RecommendationEngine) -> None:
    payload = rec.recommend("biodiversidad")
    allowed = set(MVP_CONNECTOR_IDS)
    for item in payload["recommendations"]:
        assert item["source_id"] in allowed
        assert item["source"] != "CHIRPS"


def test_manglares_alias(rec: RecommendationEngine) -> None:
    payload = rec.recommend("manglares")
    assert payload["count"] >= 1
    assert any(r["source_id"] == "invemar" for r in payload["recommendations"])
