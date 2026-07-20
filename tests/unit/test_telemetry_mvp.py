"""Tests — telemetría mínima preview (query · timestamp · result_count · clicks)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.api.main import app
from backend.telemetry.store import TelemetryStore


def test_telemetry_store_three_fields(tmp_path: Path) -> None:
    store = TelemetryStore(db_path=tmp_path / "q.db")
    assert store.log("inundacion", 3) is not None
    assert store.log("", 0) is None
    rows = store.recent(limit=10)
    assert len(rows) == 1
    assert set(rows[0].keys()) == {"query", "timestamp", "result_count"}
    assert rows[0]["query"] == "inundacion"
    assert rows[0]["result_count"] == 3


def test_telemetry_store_clicks(tmp_path: Path) -> None:
    store = TelemetryStore(db_path=tmp_path / "c.db")
    ev = store.log_click("ideam:amenaza-inundacion", "ideam")
    assert ev is not None
    assert ev["event_type"] == "resource_click"
    clicks = store.recent_clicks(limit=5)
    assert len(clicks) == 1
    assert clicks[0]["resource_id"] == "ideam:amenaza-inundacion"


def test_telemetry_api_and_autolog(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    db = tmp_path / "preview.db"
    monkeypatch.setenv("TELEMETRY_DB_PATH", str(db))
    import backend.telemetry.store as ts

    ts._store = None

    with TestClient(app) as client:
        info = client.get("/telemetry/info")
        assert info.status_code == 200
        assert info.json()["fields"] == ["query", "timestamp", "result_count"]

        hz = client.get("/healthz")
        assert hz.status_code == 200
        assert hz.json()["status"] == "ok"

        ver = client.get("/version")
        assert ver.status_code == 200
        assert ver.json()["version"] == "0.2.0-preview"

        health = client.get("/health")
        assert health.status_code == 200
        assert health.json()["status"] == "ok"

        client.get("/recommend", params={"q": "precipitacion", "limit": 5})
        recent = client.get("/telemetry/recent")
        assert recent.status_code == 200
        body = recent.json()
        assert body["count"] >= 1
        assert body["items"][0]["query"] == "precipitacion"
        assert "result_count" in body["items"][0]
        assert "timestamp" in body["items"][0]

        click = client.post(
            "/telemetry/click",
            json={"resource_id": "ideam:precipitacion", "source_id": "ideam"},
        )
        assert click.status_code == 200
        assert click.json()["ok"] is True
        clicks = client.get("/telemetry/clicks")
        assert clicks.json()["count"] >= 1
