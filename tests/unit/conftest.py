"""Fixtures compartidas — catálogo curado como fuente de verdad de integración.

Los tests de conteo/registro comparan motores y API contra los IDs activos
de catalog/sources/*.json (curaduría humana), no contra números fijos, para
que la suite siga al catálogo cuando se incorporan fuentes verificadas.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

SOURCES_DIR = Path(__file__).resolve().parents[2] / "catalog" / "sources"


def _active_catalog_ids() -> set[str]:
    ids: set[str] = set()
    for path in sorted(SOURCES_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if str(data.get("status") or "").strip().lower() == "active":
            sid = str(data.get("id") or "").strip().lower()
            if sid:
                ids.add(sid)
    return ids


@pytest.fixture(scope="session")
def active_catalog_ids() -> set[str]:
    return _active_catalog_ids()


@pytest.fixture(scope="session")
def active_catalog_count() -> int:
    return len(_active_catalog_ids())
