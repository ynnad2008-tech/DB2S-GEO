"""
Discovery Engine — Fase 1 MVP.

Capacidades:
- registrar conectores
- listar conectores / fuentes disponibles
- buscar fuentes registradas
- obtener información de una fuente
- devolver estructura normalizada

Sin indexación distribuida. Sin OpenSearch.
Curaduría humana: solo conectores MVP registrados explícitamente.
"""

from __future__ import annotations

from typing import Any

from connectors.base import BaseConnector
from connectors.registry import build_mvp_connectors


class DiscoveryEngine:
    """Motor de descubrimiento sobre conectores curados (read-only)."""

    status = "mvp"

    def __init__(self, connectors: dict[str, BaseConnector] | None = None) -> None:
        self._connectors: dict[str, BaseConnector] = {}
        if connectors is None:
            for connector in build_mvp_connectors().values():
                self.register(connector)
        else:
            for connector in connectors.values():
                self.register(connector)

    def register(self, connector: BaseConnector) -> None:
        """Registra un conector por su connector_id (curaduría explícita)."""
        if not isinstance(connector, BaseConnector):
            raise TypeError("Solo se aceptan instancias de BaseConnector")
        self._connectors[connector.connector_id] = connector

    def list_connectors(self) -> list[dict[str, Any]]:
        """Lista conectores disponibles con identidad normalizada."""
        return [self._normalize_identity(c) for c in self._connectors.values()]

    def list_sources(self) -> list[dict[str, Any]]:
        """Alias semántico de list_connectors para la API /sources."""
        return self.list_connectors()

    def get_source(self, source_id: str) -> dict[str, Any] | None:
        """Obtiene información normalizada de una fuente registrada."""
        connector = self._resolve(source_id)
        if connector is None:
            return None
        identity = self._normalize_identity(connector)
        identity["resources"] = connector.discover()
        return identity

    def search(
        self,
        query: str | None = None,
        domain: str | None = None,
    ) -> list[dict[str, Any]]:
        """Busca fuentes registradas por texto y/o dominio."""
        q = (query or "").strip().lower()
        d = (domain or "").strip().lower()
        results: list[dict[str, Any]] = []

        for connector in self._connectors.values():
            identity = self._normalize_identity(connector)
            domains = [x.lower() for x in identity.get("domains", [])]
            if d and d not in domains:
                continue
            if q:
                haystack = " ".join(
                    [
                        str(identity.get("source_id", "")),
                        str(identity.get("source", "")),
                        str(identity.get("institution", "")),
                        str(identity.get("description", "")),
                        " ".join(domains),
                        " ".join(identity.get("access_methods", [])),
                    ]
                ).lower()
                if q not in haystack:
                    continue
            results.append(identity)
        return results

    def discover_resources(
        self,
        source_id: str,
        query: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]] | None:
        connector = self._resolve(source_id)
        if connector is None:
            return None
        return connector.discover(query)

    def describe_resource(
        self,
        source_id: str,
        resource_id: str,
    ) -> dict[str, Any] | None:
        connector = self._resolve(source_id)
        if connector is None:
            return None
        return connector.describe(resource_id)

    def access_info(
        self,
        source_id: str,
        resource_id: str | None = None,
    ) -> dict[str, Any] | None:
        """
        Información de acceso.

        Si no se indica resource_id, se usa el primer recurso curado
        o un resumen a nivel fuente.
        """
        connector = self._resolve(source_id)
        if connector is None:
            return None

        identity = connector.identify()
        if resource_id:
            info = connector.access_info(resource_id)
            info["source"] = identity.get("source")
            info["institution"] = identity.get("institution")
            return info

        resources = connector.discover()
        if resources:
            info = connector.access_info(resources[0]["resource_id"])
            info["source"] = identity.get("source")
            info["institution"] = identity.get("institution")
            info["available_resources"] = [
                r["resource_id"] for r in resources
            ]
            return info

        return {
            "source_id": source_id,
            "source": identity.get("source"),
            "institution": identity.get("institution"),
            "access_methods": identity.get("access_methods", []),
            "portal_url": identity.get("homepage", ""),
            "read_only": True,
            "downloads_supported": False,
            "notes": "Sin recursos curados asociados.",
        }

    def get_connector(self, source_id: str) -> BaseConnector | None:
        return self._resolve(source_id)

    def info(self) -> dict[str, Any]:
        return {
            "engine": "DiscoveryEngine",
            "status": self.status,
            "connectors_registered": len(self._connectors),
            "connector_ids": sorted(self._connectors.keys()),
            "indexing": "none",
            "opensearch": False,
            "curation": "human",
            "security": "read_only",
        }

    def _resolve(self, source_id: str) -> BaseConnector | None:
        key = source_id.strip().lower()
        if key in self._connectors:
            return self._connectors[key]
        # Alias comunes
        aliases = {
            "faostat": "fao",
            "google_earth_engine": "gee",
            "earth_engine": "gee",
            "instituto_invemar": "invemar",
        }
        mapped = aliases.get(key)
        if mapped and mapped in self._connectors:
            return self._connectors[mapped]
        return None

    @staticmethod
    def _normalize_identity(connector: BaseConnector) -> dict[str, Any]:
        raw = connector.identify()
        # Garantiza campos del modelo de respuesta del MVP
        return {
            "source_id": raw.get("source_id") or connector.connector_id,
            "source": raw.get("source") or connector.source_name,
            "institution": raw.get("institution", ""),
            "domains": list(raw.get("domains", [])),
            "access_methods": list(raw.get("access_methods", [])),
            "country_or_scope": raw.get("country_or_scope", ""),
            "description": raw.get("description", ""),
            "homepage": raw.get("homepage", ""),
            "license": raw.get("license", ""),
            "curation": raw.get("curation", "human"),
            "status": raw.get("status", "mvp"),
            "connector_id": raw.get("connector_id") or connector.connector_id,
            "version": raw.get("version") or connector.version,
        }
