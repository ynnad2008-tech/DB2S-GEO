"""Tests API — Recommendation endpoints (Fase 4)."""

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


def test_recommend_q_precipitacion(client: TestClient) -> None:
    response = client.get("/recommend", params={"q": "precipitacion"})
    assert response.status_code == 200
    body = response.json()
    assert body["count"] >= 1
    top = body["recommendations"][0]
    assert top["source"] in {"IDEAM", "Google Earth Engine", "NASA"}
    assert top["score"] >= 50
    assert top["reason"]
    assert top["relations_used"]
    ideam = next(r for r in body["recommendations"] if r["source"] == "IDEAM")
    assert ideam["score"] >= 50
    assert ideam["reason"]
    assert ideam["relations_used"]


def test_recommend_domain(client: TestClient) -> None:
    response = client.get("/recommend/domain/clima")
    assert response.status_code == 200
    assert any(r["source"] == "IDEAM" for r in response.json()["recommendations"])


def test_recommend_source(client: TestClient) -> None:
    response = client.get("/recommend/source/ideam")
    assert response.status_code == 200
    assert response.json()["count"] >= 1


def test_recommend_resource(client: TestClient) -> None:
    response = client.get("/recommend/resource/ideam:precipitacion")
    assert response.status_code == 200
    body = response.json()
    assert body["count"] >= 1
    assert any(r["source_id"] == "ideam" for r in body["recommendations"])


def test_recommend_unknown_domain(client: TestClient) -> None:
    response = client.get("/recommend/domain/astrofisica")
    assert response.status_code == 404


def test_recommend_requires_q(client: TestClient) -> None:
    response = client.get("/recommend")
    assert response.status_code == 422
