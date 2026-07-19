"""
Persistencia ligera JSON — Watcher Engine MVP.

Estructura:
  <data_dir>/
    snapshots/<source_id>.json
    events.json
"""

from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Any


class WatcherStore:
    """Almacenamiento local JSON (sin BD). Thread-safe básico."""

    def __init__(self, data_dir: Path | str) -> None:
        self.data_dir = Path(data_dir)
        self.snapshots_dir = self.data_dir / "snapshots"
        self.events_path = self.data_dir / "events.json"
        self._lock = threading.Lock()
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)
        if not self.events_path.exists():
            self._write_json(self.events_path, [])

    def load_snapshot(self, source_id: str) -> dict[str, Any] | None:
        path = self.snapshots_dir / f"{source_id}.json"
        if not path.exists():
            return None
        return self._read_json(path)

    def save_snapshot(self, source_id: str, snapshot: dict[str, Any]) -> None:
        path = self.snapshots_dir / f"{source_id}.json"
        with self._lock:
            self._write_json(path, snapshot)

    def list_snapshots(self) -> list[str]:
        return sorted(p.stem for p in self.snapshots_dir.glob("*.json"))

    def append_events(self, events: list[dict[str, Any]]) -> None:
        if not events:
            return
        with self._lock:
            current = self._read_json(self.events_path)
            if not isinstance(current, list):
                current = []
            current.extend(events)
            self._write_json(self.events_path, current)

    def list_events(
        self,
        *,
        source_id: str | None = None,
        event_type: str | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        with self._lock:
            events = self._read_json(self.events_path)
        if not isinstance(events, list):
            events = []
        if source_id:
            key = source_id.strip().lower()
            events = [e for e in events if str(e.get("source", "")).lower() == key]
        if event_type:
            et = event_type.strip().upper()
            events = [e for e in events if str(e.get("event_type", "")).upper() == et]
        # más recientes primero
        events = sorted(events, key=lambda e: e.get("timestamp", ""), reverse=True)
        if limit is not None:
            events = events[:limit]
        return events

    def clear_events(self) -> None:
        with self._lock:
            self._write_json(self.events_path, [])

    def stats(self) -> dict[str, Any]:
        events = self.list_events()
        by_type: dict[str, int] = {}
        by_source: dict[str, int] = {}
        for event in events:
            et = str(event.get("event_type", "UNKNOWN"))
            src = str(event.get("source", "unknown"))
            by_type[et] = by_type.get(et, 0) + 1
            by_source[src] = by_source.get(src, 0) + 1
        return {
            "snapshots": len(self.list_snapshots()),
            "events": len(events),
            "events_by_type": by_type,
            "events_by_source": by_source,
            "data_dir": str(self.data_dir),
        }

    @staticmethod
    def _read_json(path: Path) -> Any:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)

    @staticmethod
    def _write_json(path: Path, payload: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
