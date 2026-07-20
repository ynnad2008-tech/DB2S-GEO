"""Tests — catálogo JSON-first + relevancia."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.api.main import app
from backend.recommendation.scoring import expand_query_tokens, is_generic_keyword
from connectors.catalog_loader import build_connectors_from_catalog, catalog_available
from connectors.registry import build_mvp_connectors


def test_catalog_available_and_active_count() -> None:
    assert catalog_available()
    connectors = build_connectors_from_catalog()
    assert len(connectors) == 23
    assert "ideam" in connectors
    assert "supertransporte" in connectors


def test_registry_uses_json_catalog() -> None:
    connectors = build_mvp_connectors()
    assert len(connectors) == 23
    assert connectors["ideam"].identify().get("catalog") == "json"


def test_generic_keywords_filtered() -> None:
    assert is_generic_keyword("colombia")
    assert is_generic_keyword("nacional")
    tokens = expand_query_tokens("transporte colombia")
    assert "transporte" in tokens
    assert "colombia" not in tokens


def test_recommend_transporte_not_dominated_by_colombia_noise() -> None:
    with TestClient(app) as client:
        rr = client.get("/recommend", params={"q": "transporte", "limit": 5}).json()
        assert rr["count"] >= 1
        top_ids = [r["source_id"] for r in rr["recommendations"][:3]]
        transportish = {
            "mintransporte",
            "invias",
            "ani",
            "upit",
            "ansv",
            "supertransporte",
        }
        assert any(s in transportish for s in top_ids)


def test_draft_source_excluded(tmp_path: Path) -> None:
    src = ROOT / "catalog" / "sources" / "ideam.json"
    payload = json.loads(src.read_text(encoding="utf-8"))
    payload["status"] = "draft"
    out = tmp_path / "sources"
    out.mkdir()
    (out / "ideam.json").write_text(json.dumps(payload), encoding="utf-8")
    ani = json.loads((ROOT / "catalog" / "sources" / "ani.json").read_text(encoding="utf-8"))
    (out / "ani.json").write_text(json.dumps(ani), encoding="utf-8")

    active = build_connectors_from_catalog(out)
    assert "ideam" not in active
    assert "ani" in active
