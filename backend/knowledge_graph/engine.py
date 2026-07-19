"""
Knowledge Graph Engine — Fase 3 MVP.

Consultas simples sobre el grafo en memoria.
Metadatos detallados se resuelven vía Discovery/Metadata cuando se necesiten.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from backend.knowledge_graph.builder import build_knowledge_graph
from backend.knowledge_graph.graph import KnowledgeGraph
from backend.knowledge_graph.models import node_id, slug_institution

if TYPE_CHECKING:
    from backend.discovery.engine import DiscoveryEngine
    from backend.metadata.engine import MetadataEngine


class KnowledgeGraphEngine:
    """API de consulta del Knowledge Graph MVP."""

    status = "mvp"

    def __init__(
        self,
        discovery: DiscoveryEngine | None = None,
        metadata: MetadataEngine | None = None,
        graph: KnowledgeGraph | None = None,
    ) -> None:
        self._discovery = discovery
        self._metadata = metadata
        if graph is not None:
            self._graph = graph
        elif discovery is not None and metadata is not None:
            self._graph = build_knowledge_graph(discovery, metadata)
        else:
            self._graph = KnowledgeGraph()

    def rebuild(self) -> None:
        if self._discovery is None or self._metadata is None:
            raise RuntimeError("Discovery y Metadata son requeridos para rebuild()")
        self._graph = build_knowledge_graph(self._discovery, self._metadata)

    @property
    def graph(self) -> KnowledgeGraph:
        return self._graph

    # --- listados ---

    def list_nodes(self, node_type: str | None = None) -> list[dict[str, Any]]:
        return self._graph.list_nodes(node_type=node_type)  # type: ignore[arg-type]

    def list_relations(self, rel_type: str | None = None) -> list[dict[str, Any]]:
        return self._graph.list_relations(rel_type=rel_type)  # type: ignore[arg-type]

    def stats(self) -> dict[str, Any]:
        base = self._graph.stats()
        base["engine"] = "KnowledgeGraphEngine"
        base["status"] = self.status
        base["stores_full_metadata"] = False
        base["built_from"] = ["discovery", "metadata"]
        return base

    # --- consultas ---

    def resources_by_domain(self, domain_id: str) -> dict[str, Any] | None:
        """Recursos e instituciones/fuentes relacionados a un dominio."""
        did = domain_id.strip().lower()
        domain_node = self._graph.get_node(node_id("Domain", did))
        if domain_node is None:
            return None

        resources = self._graph.neighbors(
            domain_node["id"],
            direction="in",
            rel_type="belongs_to",
        )
        resource_ids = [self._key_from_node(r) for r in resources]
        resource_labels = [r["label"] for r in resources]

        source_labels: list[str] = []
        source_ids: list[str] = []
        seen_sources: set[str] = set()
        for res in resources:
            sources = self._graph.neighbors(
                res["id"],
                direction="in",
                rel_type="contains",
            )
            for src in sources:
                if src["id"] not in seen_sources:
                    seen_sources.add(src["id"])
                    source_ids.append(self._key_from_node(src))
                    source_labels.append(src["label"])

        return {
            "domain": did,
            "label": domain_node["label"],
            "sources": source_labels,
            "source_ids": source_ids,
            "resources": resource_ids,
            "resource_labels": resource_labels,
            "count_resources": len(resource_ids),
            "count_sources": len(source_labels),
        }

    def resources_by_source(self, source_id: str) -> dict[str, Any] | None:
        sid = source_id.strip().lower()
        source_node = self._graph.get_node(node_id("Source", sid))
        if source_node is None:
            return None

        resources = self._graph.neighbors(
            source_node["id"],
            direction="out",
            rel_type="contains",
        )
        domains = self.domains_of_source(sid) or {"domains": []}

        institutions = self._graph.neighbors(
            source_node["id"],
            direction="in",
            rel_type="publishes",
        )

        return {
            "source_id": sid,
            "source": source_node["label"],
            "institutions": [i["label"] for i in institutions],
            "resources": [self._key_from_node(r) for r in resources],
            "resource_labels": [r["label"] for r in resources],
            "domains": domains.get("domains", []),
            "count_resources": len(resources),
        }

    def domains_of_source(self, source_id: str) -> dict[str, Any] | None:
        sid = source_id.strip().lower()
        source_node = self._graph.get_node(node_id("Source", sid))
        if source_node is None:
            return None

        resources = self._graph.neighbors(
            source_node["id"],
            direction="out",
            rel_type="contains",
        )
        domain_map: dict[str, str] = {}
        for res in resources:
            for dom in self._graph.neighbors(
                res["id"],
                direction="out",
                rel_type="belongs_to",
            ):
                domain_map[self._key_from_node(dom)] = dom["label"]

        return {
            "source_id": sid,
            "source": source_node["label"],
            "domains": sorted(domain_map.keys()),
            "domain_labels": [domain_map[k] for k in sorted(domain_map.keys())],
        }

    def institutions_by_domain(self, domain_id: str) -> dict[str, Any] | None:
        did = domain_id.strip().lower()
        domain_node = self._graph.get_node(node_id("Domain", did))
        if domain_node is None:
            return None

        resources = self._graph.neighbors(
            domain_node["id"],
            direction="in",
            rel_type="belongs_to",
        )
        institutions: dict[str, str] = {}
        for res in resources:
            sources = self._graph.neighbors(
                res["id"],
                direction="in",
                rel_type="contains",
            )
            for src in sources:
                insts = self._graph.neighbors(
                    src["id"],
                    direction="in",
                    rel_type="publishes",
                )
                for inst in insts:
                    institutions[inst["id"]] = inst["label"]

        return {
            "domain": did,
            "label": domain_node["label"],
            "institutions": sorted(institutions.values()),
            "institution_ids": sorted(
                self._key_from_node({"id": nid}) for nid in institutions
            ),
            "count": len(institutions),
        }

    def get_source(self, source_id: str) -> dict[str, Any] | None:
        return self.resources_by_source(source_id)

    def get_domain(self, domain_id: str) -> dict[str, Any] | None:
        return self.resources_by_domain(domain_id)

    def get_institution(self, institution_id: str) -> dict[str, Any] | None:
        """
        institution_id: slug, fragmento del nombre, o source_id publicado.
        Retorna fuentes publicadas y dominios alcanzables.
        """
        key = institution_id.strip().lower()
        # Intento directo
        node = self._graph.get_node(node_id("Institution", key))
        if node is None:
            # Búsqueda por coincidencia parcial en id/label
            for candidate in self._graph.list_nodes("Institution"):
                cid = self._key_from_node(candidate).lower()
                label = candidate["label"].lower()
                if key in cid or key in label or key == slug_institution(label):
                    node = candidate
                    break
        if node is None:
            # Resolver vía Source publicada (p. ej. institution_id=invemar)
            source_node = self._graph.get_node(node_id("Source", key))
            if source_node is not None:
                publishers = self._graph.neighbors(
                    source_node["id"],
                    direction="in",
                    rel_type="publishes",
                )
                if publishers:
                    node = publishers[0]
        if node is None:
            return None

        sources = self._graph.neighbors(
            node["id"],
            direction="out",
            rel_type="publishes",
        )
        domains: dict[str, str] = {}
        resources: list[str] = []
        for src in sources:
            for res in self._graph.neighbors(
                src["id"],
                direction="out",
                rel_type="contains",
            ):
                resources.append(self._key_from_node(res))
                for dom in self._graph.neighbors(
                    res["id"],
                    direction="out",
                    rel_type="belongs_to",
                ):
                    domains[self._key_from_node(dom)] = dom["label"]

        return {
            "institution_id": self._key_from_node(node),
            "institution": node["label"],
            "sources": [s["label"] for s in sources],
            "source_ids": [self._key_from_node(s) for s in sources],
            "domains": sorted(domains.keys()),
            "resources": resources,
            "count_sources": len(sources),
            "count_resources": len(resources),
        }

    def info(self) -> dict[str, Any]:
        return {
            "engine": "KnowledgeGraphEngine",
            "status": self.status,
            "backend": "python_memory",
            "neo4j": False,
            "rdf": False,
            "sparql": False,
            "stores_full_metadata": False,
            "built_from": ["discovery", "metadata"],
            "node_types": [
                "Institution",
                "Source",
                "Resource",
                "Domain",
                "Keyword",
            ],
            "relation_types": [
                "publishes",
                "contains",
                "belongs_to",
                "associated_with",
            ],
            "curation": "human",
            "read_only": True,
        }

    @staticmethod
    def _key_from_node(node: dict[str, Any]) -> str:
        """Extrae la clave tras el prefijo Type:."""
        nid = node.get("id", "")
        if ":" in nid:
            return nid.split(":", 1)[1]
        return nid
