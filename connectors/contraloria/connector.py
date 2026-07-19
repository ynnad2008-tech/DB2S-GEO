"""
Conector Contraloría — enriquecimiento operativo DB2S-GEO.

Metadatos curados humanamente. Read-only. Sin descarga ni ejecución remota.
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
from connectors.models import normalize_source

SOURCE_ID = "contraloria"
INSTITUTION = "Contraloría General de la República de Colombia"
HOMEPAGE = "https://www.contraloria.gov.co"
LICENSE = "Según términos Contraloría / Geoportal"

_RESOURCES: dict[str, dict[str, Any]] = {
    "contraloria:obras-infraestructura": {
        "resource_id": "contraloria:obras-infraestructura",
        "title": "Geoportal Contraloría — obras de infraestructura pública",
        "type": "catalog",
        "domains": ["observacion_tierra", "poblacion"],
        "primary_domain": "observacion_tierra",
        "keywords": [
            "obras",
            "infraestructura",
            "publica",
            "control",
            "fiscal",
            "contratacion",
            "estatal",
            "secop",
            "seguimiento",
            "territorial",
            "geoportal",
            "transparencia",
            "contraloria"
        ],
        "description": (
            "Geoportal de la Contraloría General (DIARI): consulta "
            "georreferenciada de contratos y obras de infraestructura "
            "pública (SECOP, APPUI, megaobras), con avance físico-financiero "
            "para control fiscal y veeduría ciudadana. DB2S-GEO solo "
            "documenta el acceso; no descarga datos contractuales."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Según contratos y reportes publicados en el Geoportal",
        "formats": ["geovisor", "mapas", "filtros contractuales", "portal"],
        "homepage": HOMEPAGE,
        "portal_url": "https://geoportal.contraloria.gov.co/",
        "documentation_url": HOMEPAGE,
        "endpoints": [
            {
                "method": "portal",
                "url": "https://geoportal.contraloria.gov.co/",
                "label": "Geoportal Contraloría — obras e infraestructura",
            },
            {
                "method": "portal",
                "url": HOMEPAGE,
                "label": "Portal institucional Contraloría General",
            },
        ],
        "access_methods": ["portal"],
        "citation_reference": (
            "Contraloría General de la República. Geoportal — obras de "
            "infraestructura y contratación pública georreferenciada. "
            "https://geoportal.contraloria.gov.co/"
        ),
        "doi": "",
    },
}


class ContraloriaConnector(BaseConnector):
    connector_id = SOURCE_ID
    source_name = "Contraloría"
    version = "1.0.0"

    def identify(self) -> dict[str, Any]:
        return normalize_source(
            source_id=SOURCE_ID,
            source="Contraloría",
            institution=INSTITUTION,
            country_or_scope="Colombia",
            domains=["observacion_tierra", "poblacion"],
            access_methods=["portal"],
            description=(
                "Órgano de control fiscal. Geoportal de obras de "
                "infraestructura y contratación pública georreferenciada. "
                "DB2S-GEO solo documenta acceso."
            ),
            homepage=HOMEPAGE,
            license=LICENSE,
            connector_id=self.connector_id,
            version=self.version,
        )

    def discover(self, query: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        summaries = [
            {
                "resource_id": r["resource_id"],
                "title": r["title"],
                "type": r["type"],
                "domains": list(r["domains"]),
                "primary_domain": r.get("primary_domain"),
                "keywords": list(r.get("keywords", [])),
                "description": r["description"],
                "source_id": SOURCE_ID,
            }
            for r in _RESOURCES.values()
        ]
        return filter_resources(summaries, query)

    def describe(self, resource_id: str) -> dict[str, Any]:
        item = find_resource(_RESOURCES, resource_id)
        if not item:
            return resource_not_found(resource_id, SOURCE_ID)
        return {
            "resource_id": item["resource_id"],
            "title": item["title"],
            "type": item["type"],
            "description": item["description"],
            "domains": list(item["domains"]),
            "primary_domain": item.get("primary_domain"),
            "keywords": list(item.get("keywords", [])),
            "spatial_coverage": item["spatial_coverage"],
            "temporal_coverage": item["temporal_coverage"],
            "formats": list(item["formats"]),
            "source_id": SOURCE_ID,
            "institution": INSTITUTION,
            "license": LICENSE,
            "homepage": item["homepage"],
            "access_methods": list(item["access_methods"]),
        }

    def access_info(self, resource_id: str) -> dict[str, Any]:
        item = find_resource(_RESOURCES, resource_id)
        if not item:
            return resource_not_found(resource_id, SOURCE_ID)
        return {
            "resource_id": item["resource_id"],
            "source_id": SOURCE_ID,
            "access_methods": list(item["access_methods"]),
            "endpoints": list(item["endpoints"]),
            "portal_url": item["portal_url"],
            "documentation_url": item["documentation_url"],
            "notes": (
                "DB2S-GEO no descarga datos del Geoportal Contraloría. "
                "Consulte el portal oficial y cite la fuente."
            ),
            "read_only": True,
            "downloads_supported": False,
        }

    def cite(self, resource_id: str) -> dict[str, Any]:
        item = find_resource(_RESOURCES, resource_id)
        if not item:
            return resource_not_found(resource_id, SOURCE_ID)
        accessed = today_iso()
        url = item["homepage"]
        apa = (
            f"Contraloría General de la República. ({accessed[:4]}). "
            f"{item['title']}. {INSTITUTION}. {url}"
        )
        return {
            "source": "Contraloría",
            "institution": INSTITUTION,
            "reference": item["citation_reference"],
            "url": url,
            "accessed": accessed,
            "apa": apa,
            "doi": item.get("doi") or "",
            "license": LICENSE,
            "resource_id": item["resource_id"],
            "source_id": SOURCE_ID,
        }
