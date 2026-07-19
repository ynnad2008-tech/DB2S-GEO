"""Tests API — Metadata Engine endpoints (Fase 2)."""

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


def test_list_resources_ideam(client: TestClient) -> None:
    response = client.get("/sources/ideam/resources")
    assert response.status_code == 200
    body = response.json()
    assert body["count"] >= 1
    precip = next(r for r in body["resources"] if r["resource_id"] == "ideam:precipitacion")
    assert precip["domain"] == "clima"
    assert "precipitacion" in precip["keywords"]


def test_get_resource_normalized(client: TestClient) -> None:
    response = client.get("/sources/ideam/resources/ideam:precipitacion")
    assert response.status_code == 200
    body = response.json()
    assert body["resource_id"] == "ideam:precipitacion"
    assert body["source"] == "IDEAM"
    assert body["institution"]
    assert body["citation_available"] is True
    assert "unavailable_fields" in body


def test_list_domains(client: TestClient) -> None:
    response = client.get("/domains")
    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 8
    ids = {d["domain_id"] for d in body["domains"]}
    assert "oceanos_costas" in ids


def test_get_domain_biodiversidad(client: TestClient) -> None:
    response = client.get("/domains/biodiversidad")
    assert response.status_code == 200
    body = response.json()
    assert body["domain_id"] == "biodiversidad"
    assert body["count_resources"] >= 1


def test_invemar_now_available(client: TestClient) -> None:
    response = client.get("/sources/invemar")
    assert response.status_code == 200
    assert response.json()["source"] == "INVEMAR"


def test_unknown_domain(client: TestClient) -> None:
    response = client.get("/domains/astrofisica")
    assert response.status_code == 404


def test_sources_count_is_six(client: TestClient) -> None:
    response = client.get("/sources")
    assert response.status_code == 200
    assert response.json()["count"] == 6
