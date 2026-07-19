"""
Tipos de nodos y relaciones del Knowledge Graph MVP (Fase 3).

Solo identificadores y etiquetas mínimas. Los metadatos completos
permanecen en Discovery / Metadata Engine.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

NodeType = Literal["Institution", "Source", "Resource", "Domain", "Keyword"]

RelationType = Literal[
    "publishes",
    "contains",
    "belongs_to",
    "associated_with",
]


class GraphNode(TypedDict, total=False):
    """Nodo ligero: id + tipo + etiqueta. Sin metadatos completos."""

    id: str
    type: NodeType
    label: str


class GraphRelation(TypedDict):
    """Arista dirigida tipada."""

    id: str
    type: RelationType
    from_id: str
    to_id: str


def node_id(node_type: NodeType, key: str) -> str:
    """Identificador estable: Type:key."""
    return f"{node_type}:{key}"


def relation_id(rel_type: RelationType, from_id: str, to_id: str) -> str:
    return f"{rel_type}|{from_id}|{to_id}"


def slug_institution(name: str) -> str:
    """Slug determinista para instituciones (curaduría / trazabilidad)."""
    text = name.strip().lower()
    for old, new in (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("ñ", "n"),
        ("ü", "u"),
    ):
        text = text.replace(old, new)
    out: list[str] = []
    for ch in text:
        if ch.isalnum():
            out.append(ch)
        elif ch in (" ", "-", "/", "(", ")", ",", "."):
            out.append("_")
    slug = "".join(out)
    while "__" in slug:
        slug = slug.replace("__", "_")
    return slug.strip("_")[:80] or "unknown"


def as_dict(payload: dict[str, Any]) -> dict[str, Any]:
    return dict(payload)
