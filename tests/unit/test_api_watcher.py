"""Tests API — Watcher endpoints (Fase 5)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.api.main import app
from backend.watcher.engine import WatcherEngine
from backend.watcher.store import WatcherStore


@pytest.fixture
def client(tmp_path: Path) -> TestClient:
    """API con store temporal para no contaminar data/watcher del repo."""
    with TestClient(app) as test_client:
        discovery = test_client.app.state.discovery
        metadata = test_client.app.state.metadata
        test_client.app.state.watcher = WatcherEngine(
            discovery,
            metadata,
            store=WatcherStore(tmp_path / "watcher"),
        )
        yield test_client


def test_watcher_info(client: TestClient) -> None:
    response = client.get("/watcher/info")
    assert response.status_code == 200
    body = response.json()
    assert body["engine"] == "WatcherEngine"
    assert body["auto_updates_catalog"] is False


def test_watcher_run_and_events(client: TestClient) -> None:
    run = client.post("/watcher/run", params={"source_id": "ideam"})
    assert run.status_code == 200
    body = run.json()
    assert body["auto_applied"] is False
    assert body["events_detected"] >= 1

    events = client.get("/watcher/events")
    assert events.status_code == 200
    assert events.json()["count"] >= 1
    assert events.json()["curation"] == "human_required"

    by_source = client.get("/watcher/events/ideam")
    assert by_source.status_code == 200
    assert all(e["source"] == "ideam" for e in by_source.json()["events"])

    by_type = client.get("/watcher/events/type/BASELINE_CREATED")
    assert by_type.status_code == 200
    assert by_type.json()["count"] >= 1
