"""Tests — Knowledge Usage Observatory MVP (Fase 8.1)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.api.main import app
from backend.observatory.engine import ObservatoryEngine
from backend.observatory.privacy import TRANSPARENCY_NOTICE, sanitize_query


@pytest.fixture
def obs(tmp_path: Path) -> ObservatoryEngine:
    return ObservatoryEngine(data_dir=tmp_path / "observatory")


def test_sanitize_strips_email() -> None:
    clean = sanitize_query("precipitacion user@example.com token")
    assert "user@example.com" not in clean
    assert "redacted-email" in clean


def test_log_and_analytics(obs: ObservatoryEngine) -> None:
    obs.log_query(
        "inundaciones microcuenca",
        channel="recommend",
        result_count=3,
        domains=["hidrologia", "clima"],
        recommendations=[{"source_id": "ideam", "score": 80}],
        terms=["inundaciones", "hidrologia"],
    )
    obs.log_query(
        "chirps inventado",
        channel="recommend",
        result_count=0,
        domains=[],
        recommendations=[],
        terms=["chirps"],
    )
    obs.log_query(
        "precipitacion",
        channel="decision_support",
        result_count=2,
        domains=["clima"],
        recommendations=[{"source_id": "ideam", "score": 70}],
        terms=["precipitacion"],
    )

    top = obs.top_queries()["items"]
    assert any(r["query"] == "precipitacion" or "inundaciones" in r["query"] for r in top)

    empty = obs.empty_queries()["items"]
    assert any("chirps" in r["query"] for r in empty)

    domains = obs.domains()["items"]
    assert any(d["domain"] == "clima" for d in domains)

    cloud = obs.wordcloud()["items"]
    assert cloud
    assert "weight" in cloud[0]

    timeline = obs.timeline(days=7)["items"]
    assert len(timeline) == 7
    assert sum(d["count"] for d in timeline) >= 3

    emerging = obs.emerging()["items"]
    assert any(e["term"] == "chirps" for e in emerging)

    dash = obs.dashboard()
    assert dash["anonymous"] is True
    assert TRANSPARENCY_NOTICE in dash["notice"]
    assert "ip" not in str(dash).lower() or "stores_ip" in str(obs.info())


def test_wordcloud_includes_domain_and_weight(obs: ObservatoryEngine) -> None:
    obs.log_query(
        "precipitacion",
        channel="recommend",
        result_count=2,
        domains=["clima"],
        terms=["precipitacion", "lluvia"],
    )
    rows = obs.wordcloud()["items"]
    assert rows
    top = next((r for r in rows if r["term"] == "precipitacion"), rows[0])
    assert "weight" in top
    assert top["count"] >= 1
    assert top.get("domain") == "clima"


def test_never_logs_empty_or_pii_only(obs: ObservatoryEngine) -> None:
    assert obs.log_query("", channel="recommend", result_count=0) is None
    assert obs.log_query("user@x.com", channel="recommend", result_count=0) is None


def test_api_observatory_and_autolog(tmp_path: Path) -> None:
    with TestClient(app) as client:
        # Aislar store de tests
        client.app.state.observatory = ObservatoryEngine(
            data_dir=tmp_path / "obs_api",
            metadata=client.app.state.metadata,
        )

        notice = client.get("/observatory/notice")
        assert notice.status_code == 200
        assert "anónima" in notice.json()["notice"] or "anonima" in notice.json()["notice"].lower()

        rec = client.get("/recommend", params={"q": "precipitacion"})
        assert rec.status_code == 200

        dss = client.get(
            "/decision-support",
            params={"q": "Necesito analizar inundaciones"},
        )
        assert dss.status_code == 200

        # Consulta sin resultados esperables
        client.get("/recommend", params={"q": "xyzzy_unknown_term_xyz"})

        dash = client.get("/observatory/dashboard")
        assert dash.status_code == 200
        body = dash.json()
        assert body["summary"]["total_queries"] >= 2
        assert body["wordcloud"] is not None

        info = client.get("/observatory/info")
        assert info.json()["stores_pii"] is False
        assert info.json()["stores_ip"] is False

        root = client.get("/")
        assert root.json()["version"].startswith("0.2")
        assert "Preview" in root.json().get("release", "")
        assert root.json().get("author") == "Dany Arbey Benavides"
        assert "GET /observatory/dashboard" in root.json()["endpoints"]
        assert "GET /telemetry/recent" in root.json()["endpoints"]
        assert "POST /telemetry/click" in root.json()["endpoints"]
        assert "GET /healthz" in root.json()["endpoints"]
        assert "GET /version" in root.json()["endpoints"]

        html = client.get("/workbench/")
        assert "Observatorio" in html.text
        assert "anónima" in html.text or "anonima" in html.text.lower()
        assert "obs-cloud" in html.text
