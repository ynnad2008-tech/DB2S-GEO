"""Tests API — Source Discovery endpoints (Fase 6)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.api.main import app
from backend.source_discovery.engine import SourceDiscoveryAssistant
from backend.source_discovery.store import CandidateStore


@pytest.fixture
def client(tmp_path: Path) -> TestClient:
    with TestClient(app) as test_client:
        d = test_client.app.state.discovery
        m = test_client.app.state.metadata
        kg = test_client.app.state.knowledge_graph
        rec = test_client.app.state.recommendation
        test_client.app.state.source_discovery = SourceDiscoveryAssistant(
            d, m, kg, rec, store=CandidateStore(tmp_path / "sd")
        )
        yield test_client


def test_analyze_endpoint(client: TestClient) -> None:
    response = client.post(
        "/source-discovery/analyze",
        json={
            "url": "https://srvags.sgc.gov.co/arcgis/rest/services/Geologia/Riesgo/MapServer"
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "candidate_source"
    assert body["source_type"] == "ArcGIS REST MapServer"
    assert body["curation"] == "human_required"
    assert body["confidence"] > 0


def test_list_and_get_candidates(client: TestClient) -> None:
    created = client.post(
        "/source-discovery/analyze",
        json={"url": "https://api.example.org/v1/biodiversidad.json"},
    ).json()
    listed = client.get("/source-discovery/candidates")
    assert listed.status_code == 200
    assert listed.json()["count"] >= 1
    detail = client.get(f"/source-discovery/candidates/{created['id']}")
    assert detail.status_code == 200
    assert detail.json()["id"] == created["id"]


def test_info(client: TestClient) -> None:
    response = client.get("/source-discovery/info")
    assert response.status_code == 200
    assert response.json()["auto_updates_catalog"] is False
    assert response.json()["ai"] is False
