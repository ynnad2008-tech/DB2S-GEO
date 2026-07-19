"""Tests — Watcher Engine MVP (Fase 5)."""

from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.discovery.engine import DiscoveryEngine
from backend.metadata.engine import MetadataEngine
from backend.watcher.compare import build_snapshot, compare_snapshots
from backend.watcher.engine import WatcherEngine
from backend.watcher.store import WatcherStore


@pytest.fixture
def discovery() -> DiscoveryEngine:
    return DiscoveryEngine()


@pytest.fixture
def metadata(discovery: DiscoveryEngine) -> MetadataEngine:
    return MetadataEngine(discovery)


@pytest.fixture
def watcher(tmp_path: Path, discovery: DiscoveryEngine, metadata: MetadataEngine) -> WatcherEngine:
    store = WatcherStore(tmp_path / "watcher")
    return WatcherEngine(discovery, metadata, store=store)


def test_first_run_creates_baseline(watcher: WatcherEngine) -> None:
    result = watcher.run(source_ids=["ideam"])
    assert result["auto_applied"] is False
    assert result["events_detected"] == 1
    assert result["events"][0]["event_type"] == "BASELINE_CREATED"
    assert result["events"][0]["auto_applied"] is False
    assert result["events"][0]["curation"] == "human_required"


def test_second_run_no_change(watcher: WatcherEngine) -> None:
    watcher.run(source_ids=["ideam"])
    result = watcher.run(source_ids=["ideam"])
    assert result["events_detected"] == 0


def test_detects_new_resource(
    watcher: WatcherEngine,
    discovery: DiscoveryEngine,
    metadata: MetadataEngine,
) -> None:
    store = watcher._store
    snap = build_snapshot("ideam", discovery, metadata)
    store.save_snapshot("ideam", snap)

    mutated = copy.deepcopy(snap)
    mutated["resources"]["ideam:coberturas_2026"] = {
        "resource_id": "ideam:coberturas_2026",
        "title": "Coberturas 2026",
        "domain": "cobertura",
        "fingerprint": "abc123",
    }
    events = compare_snapshots(snap, mutated)
    types = {e["event_type"] for e in events}
    assert "NEW_RESOURCE" in types
    new_ev = next(e for e in events if e["event_type"] == "NEW_RESOURCE")
    assert new_ev["resource"] == "ideam:coberturas_2026"
    assert new_ev["severity"] == "info"
    assert new_ev["detected_by"] == "watcher_engine"
    assert new_ev["auto_applied"] is False


def test_detects_removed_and_access_change() -> None:
    previous = {
        "source_id": "ideam",
        "available": True,
        "access_methods": ["api", "portal"],
        "domains": ["clima"],
        "resources": {
            "ideam:old": {"resource_id": "ideam:old", "title": "Old", "fingerprint": "1"},
        },
        "captured_at": "2026-01-01T00:00:00+00:00",
    }
    current = {
        "source_id": "ideam",
        "available": True,
        "access_methods": ["portal", "arcgis"],
        "domains": ["clima"],
        "resources": {},
        "captured_at": "2026-01-02T00:00:00+00:00",
    }
    events = compare_snapshots(previous, current)
    types = {e["event_type"] for e in events}
    assert "REMOVED_RESOURCE" in types
    assert "NEW_ACCESS_METHOD" in types
    assert "ACCESS_METHOD_REMOVED" in types


def test_source_unavailable_critical() -> None:
    previous = {
        "source_id": "ideam",
        "available": True,
        "access_methods": ["api"],
        "domains": [],
        "resources": {},
    }
    current = {
        "source_id": "ideam",
        "available": False,
        "access_methods": [],
        "domains": [],
        "resources": {},
        "captured_at": "2026-01-02T00:00:00+00:00",
    }
    events = compare_snapshots(previous, current)
    assert len(events) == 1
    assert events[0]["event_type"] == "SOURCE_UNAVAILABLE"
    assert events[0]["severity"] == "critical"


def test_list_events_filters(watcher: WatcherEngine) -> None:
    watcher.run(source_ids=["ideam", "gbif"])
    all_events = watcher.list_events()
    assert len(all_events) >= 2
    ideam = watcher.list_events(source_id="ideam")
    assert all(e["source"] == "ideam" for e in ideam)
    baselines = watcher.list_events(event_type="BASELINE_CREATED")
    assert all(e["event_type"] == "BASELINE_CREATED" for e in baselines)


def test_does_not_modify_catalog(watcher: WatcherEngine, discovery: DiscoveryEngine) -> None:
    before = discovery.list_sources()
    watcher.run()
    after = discovery.list_sources()
    assert before == after


def test_info(watcher: WatcherEngine) -> None:
    info = watcher.info()
    assert info["auto_updates_catalog"] is False
    assert info["human_curation"] is True
    assert info["ai"] is False
