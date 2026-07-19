"""
Conector UPIT — enriquecimiento operativo DB2S-GEO.

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

SOURCE_ID = "upit"
INSTITUTION = (
    "Unidad de Planeación de Infraestructura de Transporte (UPIT) — "
    "Ministerio de Transporte"
)
HOMEPAGE = "https://upit.gov.co"
LICENSE = "Según términos UPIT / Hub de Mapas"

_RESOURCES: dict[str, dict[str, Any]] = {
    "upit:hub-transporte": {
        "resource_id": "upit:hub-transporte",
        "title": "Hub de Mapas UPIT — infraestructura y transporte",
        "type": "catalog",
        "domains": ["observacion_tierra"],
        "primary_domain": "observacion_tierra",
        "keywords": [
            "hub",
            "mapas",
            "transporte",
            "planeacion",
            "infraestructura",
            "webmaps",
            "movilidad",
            "analisis",
            "territorial",
            "tableros",
            "geovisores",
            "upit",
            "colombia",
        ],
        "description": (
            "Hub institucional de mapas de la UPIT: datos, indicadores, "
            "tableros y geovisores sobre infraestructura de transporte "
            "(carretero, férreo, fluvial, aéreo) y planeación sectorial. "
            "Incluye servicios REST GIS UPIT. DB2S-GEO solo documenta el "
            "acceso; no descarga capas."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Según capas y tableros publicados en el Hub",
        "formats": ["Hub ArcGIS", "geovisores", "FeatureServer", "tableros"],
        "homepage": HOMEPAGE,
        "portal_url": "https://upithub-upit.hub.arcgis.com/",
        "documentation_url": "https://upit.gov.co/",
        "endpoints": [
            {
                "method": "portal",
                "url": "https://upithub-upit.hub.arcgis.com/",
                "label": "Hub de Mapas UPIT",
            },
            {
                "method": "arcgis",
                "url": "https://gis.upit.gov.co/wa_server/rest/services",
                "label": "Directorio REST GIS UPIT",
            },
            {
                "method": "portal",
                "url": HOMEPAGE,
                "label": "Portal institucional UPIT",
            },
        ],
        "access_methods": ["portal", "arcgis"],
        "citation_reference": (
            "Unidad de Planeación de Infraestructura de Transporte (UPIT). "
            "Hub de Mapas — infraestructura de transporte. "
            "https://upithub-upit.hub.arcgis.com/"
        ),
        "doi": "",
    },
}


class UpitConnector(BaseConnector):
    connector_id = SOURCE_ID
    source_name = "UPIT"
    version = "1.0.0"

    def identify(self) -> dict[str, Any]:
        return normalize_source(
            source_id=SOURCE_ID,
            source="UPIT",
            institution=INSTITUTION,
            country_or_scope="Colombia",
            domains=["observacion_tierra"],
            access_methods=["portal", "arcgis"],
            description=(
                "Unidad de Planeación de Infraestructura de Transporte: "
                "Hub de Mapas y servicios GIS para planeación multimodal. "
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
                "DB2S-GEO no descarga productos del Hub UPIT. "
                "Consulte el Hub/GIS oficiales y cite la fuente."
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
            f"UPIT. ({accessed[:4]}). {item['title']}. "
            f"{INSTITUTION}. {url}"
        )
        return {
            "source": "UPIT",
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
