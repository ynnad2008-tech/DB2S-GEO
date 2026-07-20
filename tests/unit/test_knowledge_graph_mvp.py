"""Tests — Knowledge Graph MVP (Fase 3)."""


from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.discovery.engine import DiscoveryEngine
from backend.knowledge_graph.engine import KnowledgeGraphEngine
from backend.metadata.engine import MetadataEngine


@pytest.fixture
def kg() -> KnowledgeGraphEngine:
    discovery = DiscoveryEngine()
    metadata = MetadataEngine(discovery)
    return KnowledgeGraphEngine(discovery, metadata)


def test_stats_counts(kg: KnowledgeGraphEngine) -> None:
    stats = kg.stats()
    assert stats["sources"] == 23
    assert stats["institutions"] >= 1
    assert stats["resources"] >= 6
    assert stats["domains"] == 15
    assert stats["keywords"] >= 1
    assert stats["relations"] > 0
    assert stats["stores_full_metadata"] is False
    assert stats["backend"] == "python_memory"


def test_resources_by_domain_clima(kg: KnowledgeGraphEngine) -> None:
    payload = kg.resources_by_domain("clima")
    assert payload is not None
    assert "IDEAM" in payload["sources"]
    assert "ideam:consulta-meteorologica" in payload["resources"]


def test_resources_by_source_ideam(kg: KnowledgeGraphEngine) -> None:
    payload = kg.resources_by_source("ideam")
    assert payload is not None
    assert payload["source"] == "IDEAM"
    assert "ideam:consulta-meteorologica" in payload["resources"]
    assert "clima" in payload["domains"] or "hidrologia" in payload["domains"]


def test_domains_of_gbif(kg: KnowledgeGraphEngine) -> None:
    payload = kg.domains_of_source("gbif")
    assert payload is not None
    assert "biodiversidad" in payload["domains"]


def test_institutions_by_domain_biodiversidad(kg: KnowledgeGraphEngine) -> None:
    payload = kg.institutions_by_domain("biodiversidad")
    assert payload is not None
    assert payload["count"] >= 1
    joined = " ".join(payload["institutions"]).lower()
    assert "biodiversity" in joined or "invemar" in joined or "marino" in joined


def test_invemar_ocean_chain(kg: KnowledgeGraphEngine) -> None:
    payload = kg.resources_by_domain("oceanos_costas")
    assert payload is not None
    assert "INVEMAR" in payload["sources"]
    assert any("ecosistemas" in r for r in payload["resources"])


def test_nodes_and_relations(kg: KnowledgeGraphEngine) -> None:
    nodes = kg.list_nodes()
    rels = kg.list_relations()
    assert any(n["type"] == "Source" for n in nodes)
    assert any(r["type"] == "publishes" for r in rels)
    assert any(r["type"] == "contains" for r in rels)
    assert any(r["type"] == "belongs_to" for r in rels)
    assert any(r["type"] == "associated_with" for r in rels)


def test_graph_does_not_store_full_metadata(kg: KnowledgeGraphEngine) -> None:
    """Nodos solo tienen id/type/label — sin description/license/etc."""
    for node in kg.list_nodes("Resource"):
        assert set(node.keys()) <= {"id", "type", "label"}
