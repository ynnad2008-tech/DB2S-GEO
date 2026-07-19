"""
Conector UPRA — enriquecimiento operativo DB2S-GEO.

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

SOURCE_ID = "upra"
INSTITUTION = (
    "Unidad de Planificación Rural Agropecuaria (UPRA) — "
    "Ministerio de Agricultura y Desarrollo Rural"
)
HOMEPAGE = "https://upra.gov.co"
LICENSE = "Uso libre según términos UPRA / SIPRA"

_RESOURCES: dict[str, dict[str, Any]] = {
    "upra:aptitud-agropecuaria": {
        "resource_id": "upra:aptitud-agropecuaria",
        "title": "Aptitud agropecuaria y evaluación de tierras (UPRA / SIPRA)",
        "type": "dataset",
        "domains": ["agricultura", "suelos"],
        "primary_domain": "agricultura",
        "keywords": [
            "aptitud",
            "agropecuaria",
            "evaluacion",
            "tierras",
            "zonificacion",
            "cadenas",
            "productivas",
            "planificacion",
            "rural",
            "sipra",
            "upra",
            "colombia",
        ],
        "description": (
            "Mapas y consultas de aptitud de la tierra por cadena productiva "
            "y evaluación de tierras de la UPRA, expuestos en el Sistema de "
            "Información para la Planificación Rural Agropecuaria (SIPRA). "
            "Soporta planificación rural, sistemas productivos y uso eficiente "
            "del suelo. DB2S-GEO solo documenta el acceso; no descarga capas."
        ),
        "spatial_coverage": "Colombia (nacional y departamental según capa)",
        "temporal_coverage": "Según publicación de capas SIPRA / UPRA",
        "formats": ["mapas", "servicios web", "portal", "consulta espacial"],
        "homepage": HOMEPAGE,
        "portal_url": "https://sipra.upra.gov.co/",
        "documentation_url": (
            "https://upra.gov.co/es-co/planificacion-del-ordenamiento-agropecuario/"
            "sistemas-de-informacion"
        ),
        "endpoints": [
            {
                "method": "portal",
                "url": "https://sipra.upra.gov.co/",
                "label": "SIPRA — Sistema de Información UPRA",
            },
            {
                "method": "portal",
                "url": "https://sipra.upra.gov.co/nacional",
                "label": "SIPRA nacional (aptitud y temáticas)",
            },
            {
                "method": "portal",
                "url": HOMEPAGE,
                "label": "Portal institucional UPRA",
            },
        ],
        "access_methods": ["portal", "arcgis"],
        "citation_reference": (
            "Unidad de Planificación Rural Agropecuaria (UPRA). Aptitud "
            "agropecuaria y evaluación de tierras — SIPRA. "
            "https://sipra.upra.gov.co/"
        ),
        "doi": "",
    },
    "upra:frontera-agricola": {
        "resource_id": "upra:frontera-agricola",
        "title": "Frontera agrícola nacional (UPRA)",
        "type": "dataset",
        "domains": ["agricultura", "suelos"],
        "primary_domain": "agricultura",
        "keywords": [
            "frontera",
            "agricola",
            "expansion",
            "productiva",
            "uso",
            "suelo",
            "sostenibilidad",
            "planificacion",
            "territorial",
            "ordenamiento",
            "sipra",
            "upra",
            "colombia",
        ],
        "description": (
            "Delimitación oficial de la frontera agrícola nacional de "
            "Colombia (UPRA), disponible en SIPRA y como servicio ArcGIS "
            "REST de ordenamiento productivo. Apoya análisis de expansión "
            "productiva, uso del suelo y planificación territorial sostenible. "
            "DB2S-GEO solo documenta el acceso; no descarga geometrías."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Según versión oficial publicada por UPRA",
        "formats": ["MapServer", "mapas", "portal"],
        "homepage": HOMEPAGE,
        "portal_url": "https://sipra.upra.gov.co/",
        "documentation_url": (
            "https://geoservicios.upra.gov.co/arcgis/rest/services/"
            "ordenamiento_productivo/frontera_agricola/MapServer"
        ),
        "endpoints": [
            {
                "method": "arcgis",
                "url": (
                    "https://geoservicios.upra.gov.co/arcgis/rest/services/"
                    "ordenamiento_productivo/frontera_agricola/MapServer"
                ),
                "label": "MapServer frontera agrícola UPRA",
            },
            {
                "method": "portal",
                "url": "https://sipra.upra.gov.co/",
                "label": "SIPRA — consulta frontera agrícola",
            },
            {
                "method": "portal",
                "url": HOMEPAGE,
                "label": "Portal institucional UPRA",
            },
        ],
        "access_methods": ["arcgis", "portal"],
        "citation_reference": (
            "Unidad de Planificación Rural Agropecuaria (UPRA). Frontera "
            "agrícola nacional. "
            "https://geoservicios.upra.gov.co/arcgis/rest/services/"
            "ordenamiento_productivo/frontera_agricola/MapServer"
        ),
        "doi": "",
    },
    "upra:zonificacion-productiva": {
        "resource_id": "upra:zonificacion-productiva",
        "title": "Zonificación productiva y cadenas agropecuarias (UPRA / SIPRA)",
        "type": "dataset",
        "domains": ["agricultura", "suelos"],
        "primary_domain": "agricultura",
        "keywords": [
            "zonificacion",
            "productiva",
            "cadenas",
            "productivas",
            "cultivos",
            "planificacion",
            "agropecuaria",
            "modelos",
            "productivos",
            "ordenamiento",
            "rural",
            "sipra",
            "upra",
            "colombia",
        ],
        "description": (
            "Capas de zonificación de aptitud y evaluación de tierras por "
            "cadena productiva de la UPRA, consultables en SIPRA "
            "(nacional y departamental). Apoya planificación agropecuaria, "
            "modelos productivos y ordenamiento rural. "
            "DB2S-GEO solo documenta el acceso; no descarga capas."
        ),
        "spatial_coverage": "Colombia (nacional y departamental según capa)",
        "temporal_coverage": "Según publicación de capas SIPRA / UPRA",
        "formats": ["mapas", "servicios web", "portal", "consulta espacial"],
        "homepage": HOMEPAGE,
        "portal_url": "https://sipra.upra.gov.co/",
        "documentation_url": (
            "https://upra.gov.co/es-co/planificacion-del-ordenamiento-agropecuario/"
            "sistemas-de-informacion"
        ),
        "endpoints": [
            {
                "method": "portal",
                "url": "https://sipra.upra.gov.co/nacional",
                "label": "SIPRA nacional — zonificación y aptitud",
            },
            {
                "method": "portal",
                "url": "https://sipra.upra.gov.co/",
                "label": "SIPRA — Sistema de Información UPRA",
            },
            {
                "method": "arcgis",
                "url": (
                    "https://geoservicios.upra.gov.co/arcgis/rest/services/"
                    "ordenamiento_productivo"
                ),
                "label": "Geoservicios ordenamiento productivo UPRA",
            },
        ],
        "access_methods": ["portal", "arcgis"],
        "citation_reference": (
            "Unidad de Planificación Rural Agropecuaria (UPRA). Zonificación "
            "productiva y evaluación de tierras por cadena — SIPRA. "
            "https://sipra.upra.gov.co/"
        ),
        "doi": "",
    },
}


class UpraConnector(BaseConnector):
    connector_id = SOURCE_ID
    source_name = "UPRA"
    version = "1.1.0"

    def identify(self) -> dict[str, Any]:
        return normalize_source(
            source_id=SOURCE_ID,
            source="UPRA",
            institution=INSTITUTION,
            country_or_scope="Colombia",
            domains=["agricultura", "suelos"],
            access_methods=["portal", "arcgis"],
            description=(
                "Unidad de Planificación Rural Agropecuaria: aptitud de "
                "tierras, frontera agrícola, zonificación productiva y "
                "planificación rural vía SIPRA y geoservicios. "
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
                "DB2S-GEO no descarga productos UPRA/SIPRA. "
                "Consulte SIPRA o los geoservicios oficiales y cite la fuente."
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
            f"UPRA. ({accessed[:4]}). {item['title']}. "
            f"{INSTITUTION}. {url}"
        )
        return {
            "source": "UPRA",
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
