"""
Persistencia JSON anónima — Observatory MVP.

Estructura:
  <data_dir>/queries.json
"""

from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Any


class ObservatoryStore:
    """Almacenamiento local de eventos de consulta (sin PII)."""

    def __init__(self, data_dir: Path | str) -> None:
        self.data_dir = Path(data_dir)
        self.path = self.data_dir / "queries.json"
        self._lock = threading.Lock()
        self.data_dir.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write([])

    def append(self, event: dict[str, Any]) -> None:
        with self._lock:
            items = self._read()
            items.append(event)
            # Cap suave para MVP local
            if len(items) > 5000:
                items = items[-5000:]
            self._write(items)

    def list_events(self, *, limit: int | None = None) -> list[dict[str, Any]]:
        with self._lock:
            items = self._read()
        items = sorted(items, key=lambda e: e.get("timestamp", ""), reverse=True)
        if limit is not None:
            items = items[:limit]
        return items

    def clear(self) -> None:
        with self._lock:
            self._write([])

    def count(self) -> int:
        return len(self.list_events())

    def stats(self) -> dict[str, Any]:
        items = self.list_events()
        return {
            "events": len(items),
            "data_dir": str(self.data_dir),
            "stores_pii": False,
            "stores_ip": False,
        }

    def _read(self) -> list[dict[str, Any]]:
        with self.path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, list) else []

    def _write(self, items: list[dict[str, Any]]) -> None:
        with self.path.open("w", encoding="utf-8") as fh:
            json.dump(items, fh, ensure_ascii=False, indent=2)
