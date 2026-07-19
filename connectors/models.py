"""
Modelos normalizados del Connector Framework (Fase 1 — Discovery MVP).

Estructuras de respuesta compartidas. Sin acceso a red ni descarga de datos.
"""

from __future__ import annotations

from typing import Any, TypedDict


class SourceIdentity(TypedDict, total=False):
    """Respuesta normalizada de identify() / Discovery Engine."""

    source_id: str
    source: str
    institution: str
    country_or_scope: str
    domains: list[str]
    access_methods: list[str]
    description: str
    homepage: str
    license: str
    curation: str
    status: str
    connector_id: str
    version: str


class ResourceSummary(TypedDict, total=False):
    """Recurso descubierto por un conector (metadatos curados)."""

    resource_id: str
    title: str
    type: str
    domains: list[str]
    description: str
    source_id: str


class ResourceDescription(TypedDict, total=False):
    """Descripción de un recurso (describe)."""

    resource_id: str
    title: str
    type: str
    description: str
    domains: list[str]
    spatial_coverage: str
    temporal_coverage: str
    formats: list[str]
    source_id: str
    institution: str
    license: str
    homepage: str


class AccessInfo(TypedDict, total=False):
    """Información de acceso — cómo llegar al recurso, sin ejecutarlo."""

    resource_id: str
    source_id: str
    access_methods: list[str]
    endpoints: list[dict[str, str]]
    portal_url: str
    documentation_url: str
    notes: str
    read_only: bool
    downloads_supported: bool


class CitationInfo(TypedDict, total=False):
    """Metadatos de citación y atribución."""

    source: str
    institution: str
    reference: str
    url: str
    accessed: str
    apa: str
    doi: str
    license: str
    resource_id: str
    source_id: str


def normalize_source(
    *,
    source_id: str,
    source: str,
    institution: str,
    domains: list[str],
    access_methods: list[str],
    country_or_scope: str = "",
    description: str = "",
    homepage: str = "",
    license: str = "",
    connector_id: str = "",
    version: str = "1.0.0",
    status: str = "mvp",
) -> SourceIdentity:
    """Construye la estructura normalizada exigida por el Discovery Engine."""
    return {
        "source_id": source_id,
        "source": source,
        "institution": institution,
        "country_or_scope": country_or_scope,
        "domains": list(domains),
        "access_methods": list(access_methods),
        "description": description,
        "homepage": homepage,
        "license": license,
        "curation": "human",
        "status": status,
        "connector_id": connector_id or source_id,
        "version": version,
    }


def as_dict(payload: dict[str, Any]) -> dict[str, Any]:
    """Copia superficial tipada → dict mutable para respuestas API."""
    return dict(payload)
