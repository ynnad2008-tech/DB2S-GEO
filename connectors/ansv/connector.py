"""
Conector ANSV — enriquecimiento operativo DB2S-GEO.

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

SOURCE_ID = "ansv"
INSTITUTION = "Agencia Nacional de Seguridad Vial (ANSV)"
HOMEPAGE = "https://ansv.gov.co"
LICENSE = "Según términos ANSV / Observatorio Nacional de Seguridad Vial"

_RESOURCES: dict[str, dict[str, Any]] = {
    "ansv:siniestralidad-vial": {
        "resource_id": "ansv:siniestralidad-vial",
        "title": "Geoportal de siniestralidad vial (ANSV / Observatorio)",
        "type": "catalog",
        "domains": ["observacion_tierra", "poblacion"],
        "primary_domain": "observacion_tierra",
        "keywords": [
            "siniestralidad",
            "vial",
            "seguridad",
            "siniestros",
            "transito",
            "accidentalidad",
            "transporte",
            "movilidad",
            "observatorio",
            "geoportal",
            "ansv"
        ],
        "description": (
            "Geoportal del Observatorio Nacional de Seguridad Vial (ANSV): "
            "mapas interactivos de distribución geográfica de siniestros, "
            "muertes y lesionados, cámaras salva-vidas y variables de "
            "seguridad vial. Incluye Hub ArcGIS y servicios REST. "
            "DB2S-GEO solo documenta el acceso; no descarga datos."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Según series del Observatorio / anuarios",
        "formats": ["geovisor", "Hub ArcGIS", "MapServer", "estadísticas"],
        "homepage": HOMEPAGE,
        "portal_url": "https://geoportal-ansv-ansv.hub.arcgis.com/",
        "documentation_url": "https://ansv.gov.co/observatorio/estad%C3%ADsticas",
        "endpoints": [
            {
                "method": "portal",
                "url": "https://geoportal-ansv-ansv.hub.arcgis.com/",
                "label": "Hub Geoportal ANSV",
            },
            {
                "method": "portal",
                "url": "https://ansv.gov.co/observatorio/estad%C3%ADsticas",
                "label": "Observatorio ANSV — estadísticas / geoportal",
            },
            {
                "method": "arcgis",
                "url": "https://srvansvargweb.ansv.gov.co/server/rest/services",
                "label": "Directorio REST servicios ANSV",
            },
        ],
        "access_methods": ["portal", "arcgis"],
        "citation_reference": (
            "Agencia Nacional de Seguridad Vial (ANSV). Geoportal / "
            "Observatorio Nacional de Seguridad Vial — siniestralidad. "
            "https://geoportal-ansv-ansv.hub.arcgis.com/"
        ),
        "doi": "",
    },
}


class AnsvConnector(BaseConnector):
    connector_id = SOURCE_ID
    source_name = "ANSV"
    version = "1.0.0"

    def identify(self) -> dict[str, Any]:
        return normalize_source(
            source_id=SOURCE_ID,
            source="ANSV",
            institution=INSTITUTION,
            country_or_scope="Colombia",
            domains=["observacion_tierra", "poblacion"],
            access_methods=["portal", "arcgis"],
            description=(
                "Agencia Nacional de Seguridad Vial: Observatorio y "
                "geoportal de siniestralidad vial. "
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
                "DB2S-GEO no descarga datos del Geoportal ANSV. "
                "Consulte el Observatorio oficial y cite la fuente."
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
            f"ANSV. ({accessed[:4]}). {item['title']}. "
            f"{INSTITUTION}. {url}"
        )
        return {
            "source": "ANSV",
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
