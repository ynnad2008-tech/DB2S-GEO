"""
Almacén SQLite mínimo para preview 0.1.0.

Consultas: query · timestamp · result_count
Clics: resource_id · timestamp · (source_id opcional)
Sin PII, sin IP, sin user-agent.
"""

from __future__ import annotations

import os
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB = ROOT / "data" / "telemetry" / "queries.db"

_lock = threading.Lock()
_store: TelemetryStore | None = None


class TelemetryStore:
    """SQLite mínimo: búsquedas + clics de recurso."""

    def __init__(self, db_path: Path | str | None = None) -> None:
        env = os.environ.get("TELEMETRY_DB_PATH", "").strip()
        self.path = Path(env) if env else Path(db_path or DEFAULT_DB)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.path), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS query_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    result_count INTEGER NOT NULL DEFAULT 0
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS click_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    resource_id TEXT NOT NULL,
                    source_id TEXT,
                    timestamp TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def log(self, query: str, result_count: int) -> dict[str, Any] | None:
        """Alias: log_query."""
        return self.log_query(query, result_count)

    def log_query(self, query: str, result_count: int) -> dict[str, Any] | None:
        q = (query or "").strip()
        if not q or len(q) > 500:
            return None
        if "@" in q or "password" in q.lower():
            return None
        ts = datetime.now(timezone.utc).isoformat()
        n = max(0, int(result_count))
        with _lock:
            with self._connect() as conn:
                conn.execute(
                    "INSERT INTO query_events (query, timestamp, result_count) VALUES (?, ?, ?)",
                    (q[:500], ts, n),
                )
                conn.commit()
        return {"query": q[:500], "timestamp": ts, "result_count": n}

    def log_click(
        self, resource_id: str, source_id: str | None = None
    ) -> dict[str, Any] | None:
        rid = (resource_id or "").strip()
        if not rid or len(rid) > 200:
            return None
        sid = (source_id or "").strip()[:120] or None
        if not sid and ":" in rid:
            sid = rid.split(":", 1)[0]
        ts = datetime.now(timezone.utc).isoformat()
        with _lock:
            with self._connect() as conn:
                conn.execute(
                    "INSERT INTO click_events (resource_id, source_id, timestamp) VALUES (?, ?, ?)",
                    (rid[:200], sid, ts),
                )
                conn.commit()
        return {
            "event_type": "resource_click",
            "resource_id": rid[:200],
            "source_id": sid,
            "timestamp": ts,
        }

    def recent(self, *, limit: int = 50) -> list[dict[str, Any]]:
        limit = max(1, min(int(limit), 200))
        with _lock:
            with self._connect() as conn:
                rows = conn.execute(
                    """
                    SELECT query, timestamp, result_count
                    FROM query_events
                    ORDER BY id DESC
                    LIMIT ?
                    """,
                    (limit,),
                ).fetchall()
        return [
            {
                "query": r["query"],
                "timestamp": r["timestamp"],
                "result_count": r["result_count"],
            }
            for r in rows
        ]

    def recent_clicks(self, *, limit: int = 50) -> list[dict[str, Any]]:
        limit = max(1, min(int(limit), 200))
        with _lock:
            with self._connect() as conn:
                rows = conn.execute(
                    """
                    SELECT resource_id, source_id, timestamp
                    FROM click_events
                    ORDER BY id DESC
                    LIMIT ?
                    """,
                    (limit,),
                ).fetchall()
        return [
            {
                "resource_id": r["resource_id"],
                "source_id": r["source_id"],
                "timestamp": r["timestamp"],
            }
            for r in rows
        ]

    def count(self) -> int:
        with _lock:
            with self._connect() as conn:
                row = conn.execute("SELECT COUNT(*) AS n FROM query_events").fetchone()
        return int(row["n"] if row else 0)

    def click_count(self) -> int:
        with _lock:
            with self._connect() as conn:
                row = conn.execute("SELECT COUNT(*) AS n FROM click_events").fetchone()
        return int(row["n"] if row else 0)

    def info(self) -> dict[str, Any]:
        return {
            "engine": "TelemetryStore",
            "fields": ["query", "timestamp", "result_count"],
            "click_fields": ["resource_id", "source_id", "timestamp"],
            "backend": "sqlite",
            "path": str(self.path),
            "events": self.count(),
            "clicks": self.click_count(),
            "stores_pii": False,
            "stores_ip": False,
        }


def get_telemetry_store() -> TelemetryStore:
    global _store
    if _store is None:
        _store = TelemetryStore()
    return _store
