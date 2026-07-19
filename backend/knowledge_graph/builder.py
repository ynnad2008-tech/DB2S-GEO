"""
Constructor del Knowledge Graph — Fase 3 MVP.

Construye relaciones SOBRE Discovery Engine y Metadata Engine.
No vuelve a almacenar metadatos completos: solo ids, labels y aristas.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from backend.knowledge_graph.graph import KnowledgeGraph
from backend.knowledge_graph.models import slug_institution
from backend.metadata.domains import INITIAL_DOMAINS

if TYPE_CHECKING:
    from backend.discovery.engine import DiscoveryEngine
    from backend.metadata.engine import MetadataEngine


def build_knowledge_graph(
    discovery: DiscoveryEngine,
    metadata: MetadataEngine,
) -> KnowledgeGraph:
    """
    Materializa el grafo MVP a partir de fuentes/recursos ya curados.

    Relaciones:
      Institution -publishes-> Source
      Source -contains-> Resource
      Resource -belongs_to-> Domain
      Resource -associated_with-> Keyword
    """
    graph = KnowledgeGraph()

    # Dominios conocidos (taxonomía Metadata) — nodos Domain.
    for domain_id, info in INITIAL_DOMAINS.items():
        graph.add_node("Domain", domain_id, info.get("label") or domain_id)

    for source in discovery.list_sources():
        source_id = source["source_id"]
        source_label = source.get("source") or source_id
        institution_name = source.get("institution") or ""
        inst_key = slug_institution(institution_name) if institution_name else f"org_{source_id}"
        inst_label = institution_name or f"Institution of {source_label}"

        inst_node = graph.add_node("Institution", inst_key, inst_label)
        source_node = graph.add_node("Source", source_id, source_label)
        graph.add_relation("publishes", inst_node, source_node)

        # Recursos vía Metadata (estructura normalizada, sin copiar todo al grafo)
        resources = metadata.list_resources(source_id, summary=False) or []
        for resource in resources:
            rid = resource.get("resource_id")
            if not rid:
                continue
            title = resource.get("title") or rid
            resource_node = graph.add_node("Resource", rid, title)
            graph.add_relation("contains", source_node, resource_node)

            # belongs_to Domain — primary + domains secundarios curados
            domain_keys: list[str] = []
            primary = resource.get("domain")
            if primary:
                domain_keys.append(str(primary))
            for d in resource.get("domains") or []:
                if d and d not in domain_keys:
                    domain_keys.append(str(d))

            for dkey in domain_keys:
                # Solo relacionar dominios de la taxonomía inicial (curaduría).
                if dkey not in INITIAL_DOMAINS:
                    continue
                domain_node = graph.add_node(
                    "Domain",
                    dkey,
                    INITIAL_DOMAINS[dkey].get("label") or dkey,
                )
                graph.add_relation("belongs_to", resource_node, domain_node)

            # associated_with Keyword — solo keywords curadas existentes
            keywords = resource.get("keywords") or []
            if isinstance(keywords, list):
                for kw in keywords:
                    if not kw or not str(kw).strip():
                        continue
                    kw_key = str(kw).strip().lower().replace(" ", "_")
                    kw_label = str(kw).strip()
                    kw_node = graph.add_node("Keyword", kw_key, kw_label)
                    graph.add_relation("associated_with", resource_node, kw_node)

    return graph
