"""Tests — Source Discovery Assistant MVP (Fase 6)."""

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
from backend.source_discovery.analyzer import analyze_url
from backend.source_discovery.engine import SourceDiscoveryAssistant
from backend.source_discovery.store import CandidateStore


@pytest.fixture
def assistant(tmp_path: Path) -> SourceDiscoveryAssistant:
    discovery = DiscoveryEngine()
    metadata = MetadataEngine(discovery)
    kg = KnowledgeGraphEngine(discovery, metadata)
    rec = RecommendationEngine(kg, discovery, metadata)
    store = CandidateStore(tmp_path / "source_discovery")
    return SourceDiscoveryAssistant(discovery, metadata, kg, rec, store=store)


def test_analyze_sgc_featureserver(assistant: SourceDiscoveryAssistant) -> None:
    url = (
        "https://srvags.sgc.gov.co/arcgis/rest/services/"
        "Geologia/AmenazaSismica/FeatureServer"
    )
    result = assistant.analyze(url)
    assert result["status"] == "candidate_source"
    assert result["source_type"] == "ArcGIS REST FeatureServer"
    assert result["institution"] in {"SGC", "Servicio Geológico Colombiano"}
    assert "geologia" in result["domains"] or "riesgo" in result["domains"]
    assert result["confidence"] >= 0.7
    assert result["curation"] == "human_required"
    assert result["auto_applied"] is False
    assert result["catalog_modified"] is False
    assert result["connector_created"] is False
    assert result["ai"] is False


def test_analyze_stac(assistant: SourceDiscoveryAssistant) -> None:
    result = assistant.analyze("https://example.org/stac/collections/sentinel")
    assert result["source_type"] == "STAC"
    assert "stac" in result["access_methods"]
    assert "observacion_tierra" in result["domains"]


def test_analyze_wms(assistant: SourceDiscoveryAssistant) -> None:
    result = assistant.analyze(
        "https://geo.example.gov.co/ows?service=WMS&request=GetCapabilities"
    )
    assert result["source_type"] == "WMS"
    assert "wms" in result["access_methods"]


def test_candidates_persisted(assistant: SourceDiscoveryAssistant) -> None:
    created = assistant.analyze("https://datos.gov.co/dataset/clima-nacional")
    listed = assistant.list_candidates()
    assert any(c["id"] == created["id"] for c in listed)
    fetched = assistant.get_candidate(created["id"])
    assert fetched is not None
    assert fetched["status"] == "candidate_source"


def test_does_not_modify_catalog(assistant: SourceDiscoveryAssistant) -> None:
    discovery = assistant._discovery
    assert discovery is not None
    before = discovery.list_sources()
    assistant.analyze("https://nuevo.ejemplo.gov.co/arcgis/rest/services/X/MapServer")
    after = discovery.list_sources()
    assert before == after


def test_empty_url() -> None:
    result = analyze_url("")
    assert result["ok"] is False
