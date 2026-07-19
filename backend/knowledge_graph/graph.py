"""
Grafo en memoria — Python puro (Fase 3).

Almacena nodos ligeros y relaciones. No duplica metadatos de
Discovery / Metadata Engine.
"""

from __future__ import annotations

from typing import Any

from backend.knowledge_graph.models import (
    GraphNode,
    GraphRelation,
    NodeType,
    RelationType,
    node_id,
    relation_id,
)


class KnowledgeGraph:
    """Knowledge Graph MVP: dicts + listas. Sin BD de grafos."""

    def __init__(self) -> None:
        self._nodes: dict[str, GraphNode] = {}
        self._relations: dict[str, GraphRelation] = {}

    # --- mutación (solo en construcción) ---

    def add_node(self, node_type: NodeType, key: str, label: str) -> str:
        nid = node_id(node_type, key)
        if nid not in self._nodes:
            self._nodes[nid] = {
                "id": nid,
                "type": node_type,
                "label": label,
            }
        return nid

    def add_relation(
        self,
        rel_type: RelationType,
        from_id: str,
        to_id: str,
    ) -> str:
        if from_id not in self._nodes or to_id not in self._nodes:
            raise ValueError(
                f"Relación {rel_type} requiere nodos existentes: {from_id} → {to_id}"
            )
        rid = relation_id(rel_type, from_id, to_id)
        if rid not in self._relations:
            self._relations[rid] = {
                "id": rid,
                "type": rel_type,
                "from_id": from_id,
                "to_id": to_id,
            }
        return rid

    # --- lectura ---

    def list_nodes(self, node_type: NodeType | None = None) -> list[dict[str, Any]]:
        nodes = list(self._nodes.values())
        if node_type:
            nodes = [n for n in nodes if n["type"] == node_type]
        return [dict(n) for n in sorted(nodes, key=lambda x: x["id"])]

    def list_relations(
        self,
        rel_type: RelationType | None = None,
    ) -> list[dict[str, Any]]:
        rels = list(self._relations.values())
        if rel_type:
            rels = [r for r in rels if r["type"] == rel_type]
        return [dict(r) for r in sorted(rels, key=lambda x: x["id"])]

    def get_node(self, nid: str) -> dict[str, Any] | None:
        node = self._nodes.get(nid)
        return dict(node) if node else None

    def neighbors(
        self,
        nid: str,
        *,
        direction: str = "out",
        rel_type: RelationType | None = None,
    ) -> list[dict[str, Any]]:
        """Nodos vecinos por dirección (out|in|both)."""
        results: list[dict[str, Any]] = []
        for rel in self._relations.values():
            if rel_type and rel["type"] != rel_type:
                continue
            target: str | None = None
            if direction in ("out", "both") and rel["from_id"] == nid:
                target = rel["to_id"]
            elif direction in ("in", "both") and rel["to_id"] == nid:
                target = rel["from_id"]
            if target and target in self._nodes:
                results.append(dict(self._nodes[target]))
        # únicos por id
        seen: set[str] = set()
        unique: list[dict[str, Any]] = []
        for item in results:
            if item["id"] not in seen:
                seen.add(item["id"])
                unique.append(item)
        return unique

    def stats(self) -> dict[str, Any]:
        by_type: dict[str, int] = {}
        for node in self._nodes.values():
            by_type[node["type"]] = by_type.get(node["type"], 0) + 1
        by_rel: dict[str, int] = {}
        for rel in self._relations.values():
            by_rel[rel["type"]] = by_rel.get(rel["type"], 0) + 1
        return {
            "institutions": by_type.get("Institution", 0),
            "sources": by_type.get("Source", 0),
            "resources": by_type.get("Resource", 0),
            "domains": by_type.get("Domain", 0),
            "keywords": by_type.get("Keyword", 0),
            "relations": len(self._relations),
            "nodes": len(self._nodes),
            "relations_by_type": by_rel,
            "nodes_by_type": by_type,
            "backend": "python_memory",
            "curation": "human",
            "read_only": True,
        }
