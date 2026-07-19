"""Tests unitarios — Discovery Engine MVP (Fase 1)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.citation.engine import CitationEngine
from backend.discovery.engine import DiscoveryEngine
from connectors.registry import MVP_CONNECTOR_IDS, build_mvp_connectors


@pytest.fixture
def discovery() -> DiscoveryEngine:
    return DiscoveryEngine()


@pytest.fixture
def citation(discovery: DiscoveryEngine) -> CitationEngine:
    return CitationEngine(discovery)


def test_mvp_connectors_registered(discovery: DiscoveryEngine) -> None:
    info = discovery.info()
    assert info["status"] == "mvp"
    assert info["connectors_registered"] == 6
    assert set(info["connector_ids"]) == set(MVP_CONNECTOR_IDS)


def test_list_sources_normalized(discovery: DiscoveryEngine) -> None:
    sources = discovery.list_sources()
    assert len(sources) == 6
    for item in sources:
        assert "source" in item
        assert "institution" in item
        assert "domains" in item
        assert "access_methods" in item
        assert item["curation"] == "human"


def test_ideam_identity_shape(discovery: DiscoveryEngine) -> None:
    ideam = discovery.get_source("ideam")
    assert ideam is not None
    assert ideam["source"] == "IDEAM"
    assert ideam["institution"] == (
        "Instituto de Hidrología, Meteorología y Estudios Ambientales"
    )
    assert "clima" in ideam["domains"]
    assert "hidrologia" in ideam["domains"]
    assert set(ideam["access_methods"]) >= {"api", "portal", "arcgis"}
    assert len(ideam["resources"]) >= 1


def test_search_by_domain(discovery: DiscoveryEngine) -> None:
    results = discovery.search(domain="biodiversidad")
    ids = {r["source_id"] for r in results}
    assert ids == {"gbif", "invemar"}


def test_search_by_query(discovery: DiscoveryEngine) -> None:
    results = discovery.search(query="worldpop")
    assert len(results) == 1
    assert results[0]["source"] == "WorldPop"


def test_access_info_read_only(discovery: DiscoveryEngine) -> None:
    access = discovery.access_info("gbif", resource_id="gbif:occurrence")
    assert access is not None
    assert access["read_only"] is True
    assert access["downloads_supported"] is False
    assert access["access_methods"]


def test_citation_fields(citation: CitationEngine) -> None:
    cite = citation.cite_source("gbif", resource_id="gbif:occurrence")
    assert cite is not None
    for key in ("source", "institution", "reference", "url", "accessed"):
        assert key in cite
        assert cite[key]
    assert "apa" in cite
    assert cite.get("doi")


def test_citation_faostat(citation: CitationEngine) -> None:
    cite = citation.cite_source("faostat")
    assert cite is not None
    assert cite["source"] == "FAOSTAT"
    assert "FAO" in cite["institution"]


def test_unknown_source(discovery: DiscoveryEngine) -> None:
    assert discovery.get_source("nasa") is None


def test_connector_contract_methods() -> None:
    for connector in build_mvp_connectors().values():
        identity = connector.identify()
        assert identity["source_id"]
        resources = connector.discover()
        assert isinstance(resources, list)
        assert resources
        rid = resources[0]["resource_id"]
        assert "title" in connector.describe(rid)
        assert connector.access_info(rid)["read_only"] is True
        cite = connector.cite(rid)
        assert cite["accessed"]
        assert cite["reference"]
