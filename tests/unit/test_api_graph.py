"""Tests API — Knowledge Graph endpoints (Fase 3)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.api.main import app


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


def test_graph_stats(client: TestClient) -> None:
    response = client.get("/graph/stats")
    assert response.status_code == 200
    body = response.json()
    assert body["sources"] == 23
    assert body["relations"] > 0
    assert body["stores_full_metadata"] is False


def test_graph_nodes(client: TestClient) -> None:
    response = client.get("/graph/nodes", params={"type": "Source"})
    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 23


def test_graph_relations(client: TestClient) -> None:
    response = client.get("/graph/relations", params={"type": "contains"})
    assert response.status_code == 200
    assert response.json()["count"] >= 23


def test_graph_domain_clima(client: TestClient) -> None:
    response = client.get("/graph/domain/clima")
    assert response.status_code == 200
    body = response.json()
    assert body["domain"] == "clima"
    assert "IDEAM" in body["sources"]
    assert "ideam:consulta-meteorologica" in body["resources"]


def test_graph_source_ideam(client: TestClient) -> None:
    response = client.get("/graph/source/ideam")
    assert response.status_code == 200
    body = response.json()
    assert body["source"] == "IDEAM"
    assert len(body["resources"]) >= 1


def test_graph_institution(client: TestClient) -> None:
    response = client.get("/graph/institution/invemar")
    assert response.status_code == 200
    body = response.json()
    assert "INVEMAR" in body["sources"] or any(
        "invemar" in s.lower() for s in body["source_ids"]
    )


def test_graph_unknown_domain(client: TestClient) -> None:
    response = client.get("/graph/domain/astrofisica")
    assert response.status_code == 404
