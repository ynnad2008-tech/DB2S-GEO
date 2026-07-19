"""Tests — Workbench Alpha (identidad y navegación)."""

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


def test_workbench_html(client: TestClient) -> None:
    response = client.get("/workbench/")
    assert response.status_code == 200
    text = response.text
    assert "DB2S-GEO" in text
    assert "Inicio" in text
    assert "Explorar" in text
    assert "Recomendaciones" in text
    assert "Monitoreo" in text
    assert "Observatorio" in text
    assert "Administración" in text
    assert "nav-admin" in text
    assert "nav-toggle" in text
    assert "admin-candidates-count" in text
    assert "status-badge" not in text
    assert "brand-tag" not in text
    assert "Desarrolladores" in text
    assert "¡Validada por humanos!" in text
    assert text.count("¡Validada por humanos!") == 1
    assert "trust-badge" in text
    assert "Asistente geoespacial" in text
    assert "Describe el problema territorial, ambiental o geoespacial que deseas resolver." in text
    assert "Orientar" in text
    assert "home-advice" in text
    assert "Plataforma de conocimiento geoespacial (versión 0.1.0-preview)" in text
    assert "footer-grid" in text
    assert "Cómo citar esta plataforma" in text
    assert "Apoya el desarrollo de DB2S-GEO" in text
    assert "© DB2S-GEO · 2026" in text
    assert "Proyecto concebido y desarrollado por" in text
    assert "Dany Arbey Benavides" in text
    assert "0.1.0-preview" in text or "v0.1.0 Preview" in text
    assert "github.com" not in text.lower()
    assert "obs-cloud" in text
    assert "home-cloud" in text
    assert "panel-admin" in text


def test_workbench_static_css(client: TestClient) -> None:
    response = client.get("/workbench/static/workbench.css")
    assert response.status_code == 200
    assert "Fraunces" in response.text or "--brand" in response.text
    assert "home-cloud" in response.text or "hc-drift" in response.text
    assert "trust-badge" in response.text
    assert "nav-toggle" in response.text
    assert "max-width: 768px" in response.text


def test_workbench_static_js(client: TestClient) -> None:
    response = client.get("/workbench/static/workbench.js")
    assert response.status_code == 200
    assert "/sources" in response.text
    assert "/watcher/events" in response.text
    assert "loadHome" in response.text
    assert "updateCandidatesCount" in response.text
    assert "/observatory/wordcloud" in response.text
    assert "/graph/stats" in response.text
    assert "setNavOpen" in response.text
    assert "closeNav" in response.text
    assert "runHomeAdvice" in response.text
    assert "/decision-support" in response.text
    assert "/telemetry/click" in response.text
    assert "humanReason" in response.text
    assert "candidateStatusBadges" in response.text
    assert "rec-cards" in response.text or "renderRecommendCards" in response.text
    assert "showCandidateJson" in response.text
    assert "navigateToResource" in response.text
    assert "focusGraphView" in response.text
    assert "cand-detail-link" in response.text
    assert "stat-link" in response.text


def test_workbench_html_ux_sprint1(client: TestClient) -> None:
    response = client.get("/workbench/")
    assert response.status_code == 200
    text = response.text
    assert 'id="rec-cards"' in text
    assert 'id="cand-detail-wrap"' in text
    assert "JSON técnico" in text


def test_workbench_css_ux_sprint1(client: TestClient) -> None:
    response = client.get("/workbench/static/workbench.css")
    assert response.status_code == 200
    assert "rec-cards" in response.text
    assert "badge-pending" in response.text
    assert "max-width: 1366px" in response.text
    assert "stat-link" in response.text
    assert "res-link" in response.text


def test_root_lists_workbench(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body.get("workbench") == "/workbench/"
    assert "GET /workbench/" in body["endpoints"]
    assert body.get("version", "").startswith("0.1")
