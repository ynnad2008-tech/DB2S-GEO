"""
Utilidades compartidas para conectores MVP (metadatos curados, read-only).
"""

from __future__ import annotations

from datetime import date
from typing import Any


def today_iso() -> str:
    return date.today().isoformat()


def filter_resources(
    resources: list[dict[str, Any]],
    query: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    """Filtra recursos curados por dominio o texto libre (q)."""
    if not query:
        return [dict(r) for r in resources]

    q = str(query.get("q") or query.get("query") or "").strip().lower()
    domain = str(query.get("domain") or "").strip().lower()

    results: list[dict[str, Any]] = []
    for item in resources:
        domains = [d.lower() for d in item.get("domains", [])]
        if domain and domain not in domains:
            continue
        if q:
            haystack = " ".join(
                [
                    str(item.get("resource_id", "")),
                    str(item.get("title", "")),
                    str(item.get("description", "")),
                    " ".join(domains),
                ]
            ).lower()
            if q not in haystack:
                continue
        results.append(dict(item))
    return results


def find_resource(
    catalog: dict[str, dict[str, Any]],
    resource_id: str,
) -> dict[str, Any] | None:
    key = resource_id.strip()
    if key in catalog:
        return dict(catalog[key])
    # Permitir alias sin prefijo de fuente
    for rid, payload in catalog.items():
        if rid.endswith(f":{key}") or rid.split(":")[-1] == key:
            return dict(payload)
    return None


def resource_not_found(resource_id: str, source_id: str) -> dict[str, Any]:
    return {
        "resource_id": resource_id,
        "source_id": source_id,
        "status": "not_found",
        "error": f"Recurso no encontrado en catálogo curado: {resource_id}",
    }
