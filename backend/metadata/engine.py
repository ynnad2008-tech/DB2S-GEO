"""
Metadata Engine — Fase 2 MVP.

Normaliza metadatos de recursos descubiertos por Discovery Engine.
No reemplaza Discovery. No inventa campos: si no existen, se marcan
explícitamente en `unavailable_fields`.

Puente conceptual hacia el futuro Knowledge Graph.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from backend.metadata.domains import get_domain, is_known_domain, list_domains

if TYPE_CHECKING:
    from backend.discovery.engine import DiscoveryEngine

# Campos del contrato de metadatos normalizados (FASE 2).
NORMALIZED_FIELDS: tuple[str, ...] = (
    "resource_id",
    "title",
    "description",
    "institution",
    "source",
    "domain",
    "keywords",
    "access_methods",
    "spatial_scope",
    "temporal_scope",
    "license",
    "citation_available",
)

# Valor explícito cuando el campo no está disponible en el catálogo curado.
UNAVAILABLE = None


class MetadataEngine:
    """Capa de metadatos desacoplada; consume Discovery Engine."""

    status = "mvp"

    def __init__(self, discovery: DiscoveryEngine | None = None) -> None:
        self._discovery = discovery

    def bind_discovery(self, discovery: DiscoveryEngine) -> None:
        self._discovery = discovery

    def list_resources(
        self,
        source_id: str,
        *,
        domain: str | None = None,
        summary: bool = True,
    ) -> list[dict[str, Any]] | None:
        """Lista recursos normalizados de una fuente."""
        if self._discovery is None:
            return None
        if self._discovery.get_connector(source_id) is None:
            return None

        discovered = self._discovery.discover_resources(source_id) or []
        items: list[dict[str, Any]] = []
        for summary_item in discovered:
            rid = summary_item.get("resource_id")
            if not rid:
                continue
            normalized = self.get_resource(source_id, rid)
            if normalized is None or normalized.get("status") == "not_found":
                continue
            if domain:
                d = domain.strip().lower()
                resource_domain = (normalized.get("domain") or "").lower()
                extra = [x.lower() for x in normalized.get("domains") or []]
                if resource_domain != d and d not in extra:
                    continue
            items.append(self._as_summary(normalized) if summary else normalized)
        return items

    def get_resource(
        self,
        source_id: str,
        resource_id: str,
    ) -> dict[str, Any] | None:
        """Describe y normaliza un recurso (estructura común)."""
        if self._discovery is None:
            return None
        connector = self._discovery.get_connector(source_id)
        if connector is None:
            return None

        identity = connector.identify()
        raw = connector.describe(resource_id)
        if raw.get("status") == "not_found":
            return raw

        access = connector.access_info(resource_id)
        cite = connector.cite(resource_id)
        citation_available = cite.get("status") != "not_found"

        return self.normalize_resource(
            raw=raw,
            identity=identity,
            access=access if access.get("status") != "not_found" else {},
            citation_available=citation_available,
        )

    def normalize_resource(
        self,
        *,
        raw: dict[str, Any],
        identity: dict[str, Any],
        access: dict[str, Any] | None = None,
        citation_available: bool = False,
    ) -> dict[str, Any]:
        """
        Produce la estructura común de metadatos.

        No inventa valores: campos ausentes → null + lista unavailable_fields.
        """
        access = access or {}
        domains = list(raw.get("domains") or identity.get("domains") or [])
        primary = raw.get("primary_domain")
        if not primary and domains:
            # Solo usa el primer dominio curado del recurso (no inventa otros).
            primary = domains[0]
        if primary and not is_known_domain(str(primary)):
            # Dominio no registrado en taxonomía inicial → no forzar etiqueta.
            pass

        keywords = raw.get("keywords")
        if keywords is not None and not isinstance(keywords, list):
            keywords = None

        access_methods = (
            access.get("access_methods")
            or raw.get("access_methods")
            or identity.get("access_methods")
        )

        candidates: dict[str, Any] = {
            "resource_id": raw.get("resource_id"),
            "title": raw.get("title"),
            "description": raw.get("description"),
            "institution": raw.get("institution") or identity.get("institution"),
            "source": identity.get("source"),
            "domain": primary,
            "keywords": keywords if keywords else UNAVAILABLE,
            "access_methods": access_methods if access_methods else UNAVAILABLE,
            "spatial_scope": raw.get("spatial_coverage") or raw.get("spatial_scope"),
            "temporal_scope": raw.get("temporal_coverage") or raw.get("temporal_scope"),
            "license": raw.get("license") or identity.get("license"),
            "citation_available": citation_available,
        }

        normalized: dict[str, Any] = {}
        unavailable: list[str] = []
        for field in NORMALIZED_FIELDS:
            value = candidates.get(field, UNAVAILABLE)
            if self._is_unavailable(value):
                normalized[field] = UNAVAILABLE
                unavailable.append(field)
            else:
                normalized[field] = value

        # Campos auxiliares (no inventados) para puente a Knowledge Graph.
        normalized["domains"] = domains if domains else UNAVAILABLE
        if not domains:
            unavailable.append("domains")
        normalized["source_id"] = (
            raw.get("source_id") or identity.get("source_id") or UNAVAILABLE
        )
        normalized["type"] = raw.get("type") or UNAVAILABLE
        normalized["unavailable_fields"] = unavailable
        normalized["curation"] = "human"
        normalized["normalization"] = "metadata_engine_v1"
        return normalized

    def list_domains(self) -> list[dict[str, Any]]:
        """Lista dominios temáticos iniciales."""
        return list_domains()

    def get_domain(self, domain_id: str) -> dict[str, Any] | None:
        """
        Detalle de un dominio + fuentes/recursos MVP asociados
        (solo con metadatos curados disponibles).
        """
        base = get_domain(domain_id)
        if base is None:
            return None
        if self._discovery is None:
            return {**base, "sources": [], "resources": [], "count_resources": 0}

        sources_hit: list[dict[str, Any]] = []
        resources_hit: list[dict[str, Any]] = []
        d = domain_id.strip().lower()

        for source in self._discovery.list_sources():
            sid = source["source_id"]
            source_domains = [x.lower() for x in source.get("domains", [])]
            source_match = d in source_domains
            resources = self.list_resources(sid, domain=d, summary=True) or []
            if source_match or resources:
                sources_hit.append(
                    {
                        "source_id": sid,
                        "source": source.get("source"),
                        "institution": source.get("institution"),
                        "domains": source.get("domains", []),
                    }
                )
            for item in resources:
                resources_hit.append(
                    {
                        "source_id": sid,
                        "resource_id": item.get("resource_id"),
                        "title": item.get("title"),
                        "domain": item.get("domain"),
                        "keywords": item.get("keywords"),
                    }
                )

        return {
            **base,
            "sources": sources_hit,
            "resources": resources_hit,
            "count_resources": len(resources_hit),
            "curation": "human",
        }

    def info(self) -> dict[str, Any]:
        return {
            "engine": "MetadataEngine",
            "status": self.status,
            "normalized_fields": list(NORMALIZED_FIELDS),
            "domains_registered": len(list_domains()),
            "discovery_bound": self._discovery is not None,
            "invents_fields": False,
            "curation": "human",
            "security": "read_only",
            "knowledge_graph_ready": True,
        }

    @staticmethod
    def _is_unavailable(value: Any) -> bool:
        if value is UNAVAILABLE:
            return True
        if value == "":
            return True
        if isinstance(value, (list, dict)) and len(value) == 0:
            return True
        return False

    @staticmethod
    def _as_summary(normalized: dict[str, Any]) -> dict[str, Any]:
        """Resumen para listados (contrato de ejemplo Fase 2)."""
        return {
            "resource_id": normalized.get("resource_id"),
            "title": normalized.get("title"),
            "domain": normalized.get("domain"),
            "keywords": normalized.get("keywords"),
            "description": normalized.get("description"),
            "source": normalized.get("source"),
            "citation_available": normalized.get("citation_available"),
            "unavailable_fields": [
                f
                for f in ("resource_id", "title", "domain", "keywords")
                if f in (normalized.get("unavailable_fields") or [])
            ],
        }
