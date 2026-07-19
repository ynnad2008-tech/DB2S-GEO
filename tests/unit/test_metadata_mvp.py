"""Tests — Metadata Engine MVP (Fase 2)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.discovery.engine import DiscoveryEngine
from backend.metadata.engine import MetadataEngine, NORMALIZED_FIELDS
from backend.metadata.domains import INITIAL_DOMAINS


@pytest.fixture
def discovery() -> DiscoveryEngine:
    return DiscoveryEngine()


@pytest.fixture
def metadata(discovery: DiscoveryEngine) -> MetadataEngine:
    return MetadataEngine(discovery)


def test_mvp_sources(discovery: DiscoveryEngine) -> None:
    ids = {s["source_id"] for s in discovery.list_sources()}
    assert ids == {
        "ideam",
        "invemar",
        "gbif",
        "fao",
        "worldpop",
        "gee",
        "sgc",
        "dynamicworld",
        "nasa",
        "mapbiomas",
        "unosat",
        "igac",
        "upra",
        "dane",
        "dnp",
        "contraloria",
        "superservicios",
        "mintransporte",
        "upit",
        "invias",
        "ansv",
        "ani",
        "supertransporte",
    }


def test_list_ideam_resources(metadata: MetadataEngine) -> None:
    items = metadata.list_resources("ideam")
    assert items is not None
    assert len(items) >= 1
    precip = next(i for i in items if i["resource_id"] == "ideam:precipitacion")
    assert precip["title"] == "Precipitación"
    assert precip["domain"] == "clima"
    assert "precipitacion" in precip["keywords"]


def test_normalized_resource_fields(metadata: MetadataEngine) -> None:
    item = metadata.get_resource("ideam", "ideam:precipitacion")
    assert item is not None
    for field in NORMALIZED_FIELDS:
        assert field in item
    assert item["citation_available"] is True
    assert item["curation"] == "human"
    assert "unavailable_fields" in item


def test_invemar_ocean_domain(metadata: MetadataEngine) -> None:
    items = metadata.list_resources("invemar", domain="oceanos_costas")
    assert items is not None
    assert len(items) >= 1
    assert all(i["domain"] == "oceanos_costas" for i in items)


def test_domains_registry(metadata: MetadataEngine) -> None:
    domains = metadata.list_domains()
    assert len(domains) == len(INITIAL_DOMAINS)
    ids = {d["domain_id"] for d in domains}
    assert "clima" in ids
    assert "oceanos_costas" in ids
    assert "observacion_tierra" in ids


def test_get_domain_with_resources(metadata: MetadataEngine) -> None:
    clima = metadata.get_domain("clima")
    assert clima is not None
    assert clima["count_resources"] >= 1
    assert any(s["source_id"] == "ideam" for s in clima["sources"])


def test_unknown_source(metadata: MetadataEngine) -> None:
    assert metadata.list_resources("fuente_inexistente") is None


def test_does_not_invent_empty_keywords(metadata: MetadataEngine) -> None:
    """Si keywords faltaran, deben ser null y listarse en unavailable_fields."""
    # Recursos MVP actuales tienen keywords curados; validamos el contrato.
    item = metadata.get_resource("gbif", "gbif:occurrence")
    assert item is not None
    assert item["keywords"] is not None
    assert "keywords" not in item["unavailable_fields"]
