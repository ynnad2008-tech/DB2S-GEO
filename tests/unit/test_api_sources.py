"""Tests de API — Discovery Engine MVP (Fase 1)."""

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


def test_list_sources(client: TestClient) -> None:
    response = client.get("/sources")
    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 23
    assert len(body["sources"]) == 23


def test_get_source_ideam(client: TestClient) -> None:
    response = client.get("/sources/ideam")
    assert response.status_code == 200
    body = response.json()
    assert body["source"] == "IDEAM"
    assert "resources" in body


def test_get_citation(client: TestClient) -> None:
    response = client.get("/sources/gbif/citation", params={"resource_id": "gbif:occurrence"})
    assert response.status_code == 200
    body = response.json()
    assert body["source"] == "GBIF"
    assert body["accessed"]
    assert body["apa"]


def test_get_access(client: TestClient) -> None:
    response = client.get("/sources/worldpop/access")
    assert response.status_code == 200
    body = response.json()
    assert body["read_only"] is True
    assert body["downloads_supported"] is False


def test_source_not_found(client: TestClient) -> None:
    response = client.get("/sources/unknown")
    assert response.status_code == 404


def test_search_query(client: TestClient) -> None:
    response = client.get("/sources", params={"q": "earth"})
    assert response.status_code == 200
    body = response.json()
    assert body["count"] >= 1
    assert any(s["source_id"] == "gee" for s in body["sources"])
