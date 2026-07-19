"""
Citation Engine — Fase 1 MVP.

Se integra con Discovery Engine / conectores para devolver atribución:
fuente, institución, referencia, URL, fecha de consulta, APA y DOI (si existe).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from backend.discovery.engine import DiscoveryEngine
    from connectors.base import BaseConnector


class CitationEngine:
    """Genera citas a partir de conectores curados (Attribution Policy)."""

    status = "mvp"

    def __init__(self, discovery: DiscoveryEngine | None = None) -> None:
        self._discovery = discovery

    def bind_discovery(self, discovery: DiscoveryEngine) -> None:
        self._discovery = discovery

    def cite_source(
        self,
        source_id: str,
        resource_id: str | None = None,
    ) -> dict[str, Any] | None:
        """
        Cita a nivel fuente o recurso.

        Campos mínimos (docs/21): fuente, institución, referencia,
        URL, fecha de consulta; APA y DOI cuando existan.
        """
        connector = self._get_connector(source_id)
        if connector is None:
            return None

        identity = connector.identify()
        if resource_id:
            citation = connector.cite(resource_id)
        else:
            resources = connector.discover()
            if not resources:
                return self._source_level_citation(identity)
            citation = connector.cite(resources[0]["resource_id"])
            citation["available_resources"] = [
                r["resource_id"] for r in resources
            ]

        if citation.get("status") == "not_found":
            return citation

        return self._normalize_citation(citation, identity)

    def cite_resource(
        self,
        source_id: str,
        resource_id: str,
    ) -> dict[str, Any] | None:
        return self.cite_source(source_id, resource_id=resource_id)

    def info(self) -> dict[str, Any]:
        return {
            "engine": "CitationEngine",
            "status": self.status,
            "formats": ["reference", "apa", "doi"],
            "policy": "docs/21_attribution_and_citation_policy.md",
            "discovery_bound": self._discovery is not None,
        }

    def _get_connector(self, source_id: str) -> BaseConnector | None:
        if self._discovery is None:
            return None
        return self._discovery.get_connector(source_id)

    @staticmethod
    def _normalize_citation(
        citation: dict[str, Any],
        identity: dict[str, Any],
    ) -> dict[str, Any]:
        doi = citation.get("doi") or ""
        payload = {
            "source": citation.get("source") or identity.get("source"),
            "institution": citation.get("institution")
            or identity.get("institution"),
            "reference": citation.get("reference", ""),
            "url": citation.get("url") or identity.get("homepage", ""),
            "accessed": citation.get("accessed", ""),
            "license": citation.get("license") or identity.get("license", ""),
            "resource_id": citation.get("resource_id", ""),
            "source_id": citation.get("source_id")
            or identity.get("source_id"),
        }
        # Incluir APA / DOI cuando existan (requisito MVP)
        apa = citation.get("apa") or ""
        if apa:
            payload["apa"] = apa
        if doi:
            payload["doi"] = doi
        if "available_resources" in citation:
            payload["available_resources"] = citation["available_resources"]
        return payload

    @staticmethod
    def _source_level_citation(identity: dict[str, Any]) -> dict[str, Any]:
        from connectors._curated import today_iso

        accessed = today_iso()
        source = identity.get("source", "")
        institution = identity.get("institution", "")
        url = identity.get("homepage", "")
        reference = f"{source}. {institution}."
        apa = f"{source}. ({accessed[:4]}). {institution}. {url}".strip()
        return {
            "source": source,
            "institution": institution,
            "reference": reference,
            "url": url,
            "accessed": accessed,
            "apa": apa,
            "license": identity.get("license", ""),
            "source_id": identity.get("source_id", ""),
            "resource_id": "",
        }
