"""
Conector genérico respaldado por ficha JSON del catálogo (DB2S-GEO 0.2).

Read-only. Sin red. Solo fuentes con status=active llegan aquí vía CatalogLoader.
"""

from __future__ import annotations

from typing import Any

from connectors._curated import (
    filter_resources,
    find_resource,
    resource_not_found,
    today_iso,
)
from connectors.base import BaseConnector


class JsonCatalogConnector(BaseConnector):
    """Adapta una ficha catalog/sources/*.json al contrato BaseConnector."""

    def __init__(self, payload: dict[str, Any]) -> None:
        self._raw = payload
        self.connector_id = str(payload["id"]).strip().lower()
        self.source_name = str(payload.get("name") or self.connector_id)
        self.version = str(payload.get("version") or "1.0.0")
        self._resources = self._index_resources(payload.get("resources") or [])

    @staticmethod
    def _index_resources(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
        out: dict[str, dict[str, Any]] = {}
        for item in items:
            rid = str(item.get("id") or item.get("resource_id") or "").strip()
            if not rid:
                continue
            title = item.get("name") or item.get("title") or rid
            endpoints = item.get("endpoints") or []
            if not endpoints and item.get("url"):
                endpoints = [
                    {
                        "method": "portal",
                        "url": item["url"],
                        "label": title,
                    }
                ]
            out[rid] = {
                "resource_id": rid,
                "title": title,
                "type": item.get("category") or item.get("type") or "dataset",
                "domains": list(item.get("domains") or []),
                "primary_domain": (item.get("domains") or [None])[0],
                "keywords": list(item.get("keywords") or []),
                "description": item.get("description") or "",
                "spatial_coverage": (item.get("coverage") or {}).get("spatial")
                or item.get("spatial_coverage")
                or "",
                "temporal_coverage": (item.get("coverage") or {}).get("temporal")
                or item.get("temporal_coverage")
                or "",
                "formats": list(item.get("formats") or []),
                "homepage": item.get("url") or item.get("homepage") or "",
                "portal_url": item.get("url") or item.get("portal_url") or "",
                "documentation_url": item.get("documentation_url")
                or item.get("url")
                or "",
                "endpoints": endpoints,
                "access_methods": list(
                    item.get("access_methods")
                    or sorted({e.get("method") for e in endpoints if e.get("method")})
                ),
                "doi": item.get("doi") or "",
                "citation_reference": item.get("citation_reference") or "",
            }
        return out

    def identify(self) -> dict[str, Any]:
        cov = self._raw.get("coverage") or {}
        methods: set[str] = set()
        for r in self._resources.values():
            methods.update(r.get("access_methods") or [])
        domains: list[str] = list(self._raw.get("domains") or [])
        for r in self._resources.values():
            for d in r.get("domains") or []:
                if d not in domains:
                    domains.append(d)
        return {
            "source_id": self.connector_id,
            "source": self.source_name,
            "institution": self._raw.get("institution") or self.source_name,
            "country_or_scope": cov.get("spatial") or "Colombia",
            "domains": domains,
            "access_methods": sorted(methods) or ["portal"],
            "description": self._raw.get("description") or "",
            "homepage": self._raw.get("url") or "",
            "license": self._raw.get("license") or "Según términos de la fuente",
            "curation": "human",
            "status": self._raw.get("status") or "active",
            "category": self._raw.get("category") or "",
            "connector_id": self.connector_id,
            "version": self.version,
            "catalog": "json",
        }

    def discover(self, query: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        summaries = [
            {
                "resource_id": r["resource_id"],
                "title": r["title"],
                "type": r["type"],
                "domains": r["domains"],
                "primary_domain": r.get("primary_domain"),
                "keywords": r.get("keywords") or [],
                "description": r.get("description") or "",
                "source_id": self.connector_id,
            }
            for r in self._resources.values()
        ]
        return filter_resources(summaries, query)

    def describe(self, resource_id: str) -> dict[str, Any]:
        item = find_resource(self._resources, resource_id)
        if item is None:
            return resource_not_found(resource_id, self.connector_id)
        identity = self.identify()
        return {
            "resource_id": item["resource_id"],
            "title": item["title"],
            "type": item["type"],
            "description": item["description"],
            "domains": item["domains"],
            "primary_domain": item.get("primary_domain"),
            "keywords": item.get("keywords") or [],
            "spatial_coverage": item.get("spatial_coverage") or "",
            "temporal_coverage": item.get("temporal_coverage") or "",
            "formats": item.get("formats") or [],
            "source_id": self.connector_id,
            "institution": identity["institution"],
            "license": identity["license"],
            "homepage": item.get("homepage") or identity["homepage"],
            "access_methods": item.get("access_methods") or identity["access_methods"],
        }

    def access_info(self, resource_id: str) -> dict[str, Any]:
        item = find_resource(self._resources, resource_id)
        if item is None:
            return resource_not_found(resource_id, self.connector_id)
        return {
            "resource_id": item["resource_id"],
            "source_id": self.connector_id,
            "access_methods": item.get("access_methods") or ["portal"],
            "endpoints": item.get("endpoints") or [],
            "portal_url": item.get("portal_url") or item.get("homepage") or "",
            "documentation_url": item.get("documentation_url") or "",
            "notes": (
                "DB2S-GEO expone solo información de acceso. "
                "La consulta o descarga debe realizarse en los portales oficiales."
            ),
            "read_only": True,
            "downloads_supported": False,
        }

    def cite(self, resource_id: str) -> dict[str, Any]:
        item = find_resource(self._resources, resource_id)
        if item is None:
            return resource_not_found(resource_id, self.connector_id)
        identity = self.identify()
        accessed = today_iso()
        url = item.get("homepage") or identity.get("homepage") or ""
        reference = (
            item.get("citation_reference")
            or f"{identity['source']}. {item['title']}. {url}".strip()
        )
        apa = (
            f"{identity['institution']}. ({accessed[:4]}). {item['title']}. "
            f"{identity['source']}. {url}"
        )
        return {
            "source": identity["source"],
            "institution": identity["institution"],
            "reference": reference,
            "url": url,
            "accessed": accessed,
            "apa": apa,
            "doi": item.get("doi") or "",
            "license": identity["license"],
            "resource_id": item["resource_id"],
            "source_id": self.connector_id,
        }
