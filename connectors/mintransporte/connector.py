"""
Conector MinTransporte — enriquecimiento operativo DB2S-GEO.

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

SOURCE_ID = "mintransporte"
INSTITUTION = "Ministerio de Transporte de Colombia"
HOMEPAGE = "https://www.mintransporte.gov.co"
LICENSE = "Según términos MinTransporte / SINC"

_RESOURCES: dict[str, dict[str, Any]] = {
    "mintransporte:sinc": {
        "resource_id": "mintransporte:sinc",
        "title": "SINC — Sistema Integral Nacional de Información de Carreteras",
        "type": "dataset",
        "domains": ["observacion_tierra"],
        "primary_domain": "observacion_tierra",
        "keywords": [
            "sinc",
            "red",
            "vial",
            "nacional",
            "carreteras",
            "puertos",
            "aeropuertos",
            "vias",
            "ferreas",
            "infraestructura",
            "transporte",
            "puentes",
            "inventario",
            "mintransporte",
            "colombia",
        ],
        "description": (
            "Sistema Integral Nacional de Información de Carreteras (SINC), "
            "administrado por el Ministerio de Transporte: inventario "
            "geográfico de la red vial (nación, departamentos, municipios), "
            "ejes, puentes, túneles, PR y sitios críticos. Disponible vía "
            "Hub ArcGIS MinTransporte y MapServer publicado en HERMES/INVIAS. "
            "DB2S-GEO solo documenta el acceso; no descarga geometrías."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Según actualizaciones reportadas al SINC",
        "formats": ["MapServer", "Hub ArcGIS", "portal"],
        "homepage": HOMEPAGE,
        "portal_url": (
            "https://sitio-sinc-mintransporte-1-1-mintransporte.hub.arcgis.com/"
        ),
        "documentation_url": (
            "https://mintransporte.gov.co/publicaciones/11967/"
            "ministerio-de-transporte-expidio-nuevas-resoluciones-para-el-"
            "reporte-de-informacion-del-sistema-integral-nacional-de-"
            "informacion-de-carreteras-y-la-modificacion-de-aspectos-en-la-"
            "categorizacion-de-vias/"
        ),
        "endpoints": [
            {
                "method": "portal",
                "url": (
                    "https://sitio-sinc-mintransporte-1-1-mintransporte"
                    ".hub.arcgis.com/"
                ),
                "label": "Hub ArcGIS SINC — MinTransporte",
            },
            {
                "method": "arcgis",
                "url": (
                    "https://hermes2.invias.gov.co/server/rest/services/"
                    "MapaCarreteras/SINC_Ministerio_de_transporte/MapServer"
                ),
                "label": "MapServer SINC Ministerio de Transporte",
            },
            {
                "method": "portal",
                "url": HOMEPAGE,
                "label": "Portal institucional MinTransporte",
            },
        ],
        "access_methods": ["portal", "arcgis"],
        "citation_reference": (
            "Ministerio de Transporte. Sistema Integral Nacional de "
            "Información de Carreteras (SINC). "
            "https://sitio-sinc-mintransporte-1-1-mintransporte.hub.arcgis.com/"
        ),
        "doi": "",
    },
}


class MintransporteConnector(BaseConnector):
    connector_id = SOURCE_ID
    source_name = "MinTransporte"
    version = "1.0.0"

    def identify(self) -> dict[str, Any]:
        return normalize_source(
            source_id=SOURCE_ID,
            source="MinTransporte",
            institution=INSTITUTION,
            country_or_scope="Colombia",
            domains=["observacion_tierra"],
            access_methods=["portal", "arcgis"],
            description=(
                "Ministerio de Transporte: administra el SINC (inventario "
                "nacional de carreteras e infraestructura vial asociada). "
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
                "DB2S-GEO no descarga capas del SINC. "
                "Consulte el Hub oficial / MapServer y cite la fuente."
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
            f"MinTransporte. ({accessed[:4]}). {item['title']}. "
            f"{INSTITUTION}. {url}"
        )
        return {
            "source": "MinTransporte",
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
