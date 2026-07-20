"""
Carga del catálogo JSON-first (solo status=active en runtime).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from connectors.base import BaseConnector
from connectors.json_catalog import JsonCatalogConnector

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCES_DIR = ROOT / "catalog" / "sources"

ALLOWED_STATUS = frozenset({"draft", "validated", "active"})


def catalog_sources_dir() -> Path:
    return DEFAULT_SOURCES_DIR


def catalog_available(sources_dir: Path | None = None) -> bool:
    d = sources_dir or DEFAULT_SOURCES_DIR
    return d.is_dir() and any(d.glob("*.json"))


def load_source_payloads(sources_dir: Path | None = None) -> list[dict[str, Any]]:
    d = sources_dir or DEFAULT_SOURCES_DIR
    if not d.is_dir():
        return []
    payloads: list[dict[str, Any]] = []
    for path in sorted(d.glob("*.json")):
        with path.open(encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, dict):
            data["_catalog_path"] = str(path)
            payloads.append(data)
    return payloads


def build_connectors_from_catalog(
    sources_dir: Path | None = None,
    *,
    statuses: frozenset[str] | None = None,
) -> dict[str, BaseConnector]:
    """
    Instancia conectores JSON.

    Por defecto solo status=active (Discovery / KG / Recommendation / Workbench).
    """
    allowed = statuses or frozenset({"active"})
    out: dict[str, BaseConnector] = {}
    for payload in load_source_payloads(sources_dir):
        status = str(payload.get("status") or "draft").strip().lower()
        if status not in allowed:
            continue
        if status not in ALLOWED_STATUS:
            continue
        sid = str(payload.get("id") or "").strip().lower()
        if not sid:
            continue
        out[sid] = JsonCatalogConnector(payload)
    return out
