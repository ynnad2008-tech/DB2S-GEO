"""
Persistencia de candidatos — Source Discovery Assistant MVP.

JSON local. No modifica el catálogo oficial.
"""

from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Any


class CandidateStore:
    def __init__(self, data_dir: Path | str) -> None:
        self.data_dir = Path(data_dir)
        self.path = self.data_dir / "candidates.json"
        self._lock = threading.Lock()
        self.data_dir.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write([])

    def add(self, candidate: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            items = self._read()
            items.append(candidate)
            self._write(items)
        return candidate

    def list(self, *, limit: int | None = None) -> list[dict[str, Any]]:
        with self._lock:
            items = self._read()
        items = sorted(items, key=lambda x: x.get("created_at", ""), reverse=True)
        if limit is not None:
            items = items[:limit]
        return items

    def get(self, candidate_id: str) -> dict[str, Any] | None:
        with self._lock:
            items = self._read()
        for item in items:
            if item.get("id") == candidate_id:
                return dict(item)
        return None

    def stats(self) -> dict[str, Any]:
        items = self.list()
        return {
            "candidates": len(items),
            "data_dir": str(self.data_dir),
        }

    def _read(self) -> list[dict[str, Any]]:
        with self.path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, list) else []

    def _write(self, items: list[dict[str, Any]]) -> None:
        with self.path.open("w", encoding="utf-8") as fh:
            json.dump(items, fh, ensure_ascii=False, indent=2)
