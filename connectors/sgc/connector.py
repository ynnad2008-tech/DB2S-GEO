"""
Conector SGC — enriquecimiento operativo DB2S-GEO.

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

SOURCE_ID = "sgc"
INSTITUTION = "Servicio Geológico Colombiano"
HOMEPAGE = "https://www2.sgc.gov.co"
GEOPORTAL = "https://geoportal.sgc.gov.co"
LICENSE = "Términos institucionales SGC / datos abiertos cuando apliquen"

_RESOURCES: dict[str, dict[str, Any]] = {
    "sgc:amenaza-sismica": {
        "resource_id": "sgc:amenaza-sismica",
        "title": "Amenaza sísmica nacional (SGC)",
        "type": "geoservice",
        "domains": ["observacion_tierra"],
        "primary_domain": "observacion_tierra",
        "keywords": [
            "amenaza",
            "sismica",
            "sismo",
            "riesgo",
            "geologico",
            "geologia",
            "ordenamiento",
            "territorial",
            "gestion",
            "arcgis",
            "mapserver",
            "sgc",
            "colombia",
        ],
        "description": (
            "Servicio geoespacial oficial del SGC con el mapa nacional de "
            "amenaza sísmica (PGA y productos asociados). Apoya gestión del "
            "riesgo, ordenamiento territorial y análisis de amenaza sísmica "
            "en Colombia. DB2S-GEO solo documenta el endpoint; "
            "no ejecuta consultas remotas."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Según publicación institucional del SGC",
        "formats": ["ArcGIS REST", "JSON", "imagen de mapa"],
        "homepage": GEOPORTAL,
        "portal_url": GEOPORTAL,
        "documentation_url": (
            "https://geoportal.sgc.gov.co/arcgis/rest/services/"
            "Amenaza_Sismica/Mapa_Amenaza_Sismica_Nacional_PGA2475/MapServer"
        ),
        "endpoints": [
            {
                "method": "arcgis",
                "url": (
                    "https://geoportal.sgc.gov.co/arcgis/rest/services/"
                    "Amenaza_Sismica/Mapa_Amenaza_Sismica_Nacional_PGA2475/"
                    "MapServer"
                ),
                "label": "Mapa Amenaza Sísmica Nacional PGA2475 MapServer",
            },
            {
                "method": "portal",
                "url": GEOPORTAL,
                "label": "Geoportal SGC",
            },
        ],
        "access_methods": ["arcgis", "portal"],
        "citation_reference": (
            "Servicio Geológico Colombiano. Amenaza sísmica nacional "
            "(Mapa Amenaza Sísmica Nacional PGA2475). "
            "Servicio ArcGIS REST MapServer. "
            "https://geoportal.sgc.gov.co/arcgis/rest/services/"
            "Amenaza_Sismica/Mapa_Amenaza_Sismica_Nacional_PGA2475/MapServer"
        ),
        "doi": "",
    },
    "sgc:simma-geologia": {
        "resource_id": "sgc:simma-geologia",
        "title": "SIMMA — Capas temáticas geológicas (SGC)",
        "type": "geoservice",
                "domains": ["geologia", "riesgo"],
        "primary_domain": "geologia",
        "keywords": [
            "geologia",
            "geologia_nacional",
            "cartografia",
            "tematica",
            "servicios",
            "geologicos",
            "geociencias",
            "simma",
            "arcgis",
            "mapserver",
            "sgc",
            "colombia",
        ],
        "description": (
            "Servicio ArcGIS REST MapServer SIMMA/CapasTematicasXEscalas "
            "del SGC: cartografía temática geológica y capas asociadas "
            "por escalas. Apoya geociencias, geología nacional y "
            "servicios geológicos. DB2S-GEO solo documenta el endpoint; "
            "no ejecuta consultas remotas."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Según publicación institucional del SGC / SIMMA",
        "formats": ["ArcGIS REST", "JSON", "imagen de mapa"],
        "homepage": GEOPORTAL,
        "portal_url": GEOPORTAL,
        "documentation_url": (
            "https://geoportal.sgc.gov.co/arcgis/rest/services/"
            "SIMMA/CapasTematicasXEscalas/MapServer"
        ),
        "endpoints": [
            {
                "method": "arcgis",
                "url": (
                    "https://geoportal.sgc.gov.co/arcgis/rest/services/"
                    "SIMMA/CapasTematicasXEscalas/MapServer"
                ),
                "label": "SIMMA CapasTematicasXEscalas MapServer",
            },
            {
                "method": "portal",
                "url": GEOPORTAL,
                "label": "Geoportal SGC",
            },
        ],
        "access_methods": ["arcgis", "portal"],
        "citation_reference": (
            "Servicio Geológico Colombiano. SIMMA — Capas temáticas "
            "por escalas (CapasTematicasXEscalas). "
            "Servicio ArcGIS REST MapServer. "
            "https://geoportal.sgc.gov.co/arcgis/rest/services/"
            "SIMMA/CapasTematicasXEscalas/MapServer"
        ),
        "doi": "",
    },
    "sgc:agua-subterranea": {
        "resource_id": "sgc:agua-subterranea",
        "title": "Inventario de puntos de agua subterránea (SGC)",
        "type": "portal",
        "domains": ["hidrologia", "observacion_tierra"],
        "primary_domain": "hidrologia",
        "keywords": [
            "hidrogeologia",
            "pozos",
            "manantiales",
            "acuiferos",
            "aguas",
            "termales",
            "subterranea",
            "inventario",
            "sgc",
            "colombia",
        ],
        "description": (
            "Inventario nacional de puntos de agua del SGC (pozos, "
            "manantiales y puntos asociados a aguas subterráneas y "
            "geotermia). Apoya hidrogeología y gestión de acuíferos. "
            "DB2S-GEO solo documenta el acceso; no descarga datos."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Según actualización institucional del inventario",
        "formats": ["portal web", "tablero interactivo", "servicios GIS"],
        "homepage": (
            "https://www2.sgc.gov.co/sgc/mapas/Paginas/"
            "inventario-de-puntos-de-agua-en-Colombia.aspx"
        ),
        "portal_url": (
            "https://www2.sgc.gov.co/sgc/mapas/Paginas/"
            "inventario-de-puntos-de-agua-en-Colombia.aspx"
        ),
        "documentation_url": GEOPORTAL,
        "endpoints": [
            {
                "method": "portal",
                "url": (
                    "https://www2.sgc.gov.co/sgc/mapas/Paginas/"
                    "inventario-de-puntos-de-agua-en-Colombia.aspx"
                ),
                "label": "Mapa inventario de puntos de agua (SGC)",
            },
            {
                "method": "portal",
                "url": GEOPORTAL,
                "label": "Geoportal SGC (hidrogeología)",
            },
        ],
        "access_methods": ["portal", "arcgis"],
        "citation_reference": (
            "Servicio Geológico Colombiano. Inventario de puntos de agua "
            "en Colombia. "
            "https://www2.sgc.gov.co/sgc/mapas/Paginas/"
            "inventario-de-puntos-de-agua-en-Colombia.aspx"
        ),
        "doi": "",
    },
}


class SgcConnector(BaseConnector):
    connector_id = SOURCE_ID
    source_name = "SGC"
    version = "1.2.0"

    def identify(self) -> dict[str, Any]:
        return normalize_source(
            source_id=SOURCE_ID,
            source="SGC",
            institution=INSTITUTION,
            country_or_scope="Colombia",
            domains=["riesgo", "geologia", "hidrologia"],
            access_methods=["portal", "arcgis"],
            description=(
                "Autoridad nacional en geociencias de Colombia. "
                "Fuente oficial de amenaza sísmica, geología, "
                "hidrogeología y cartografía temática geocientífica."
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
                "DB2S-GEO expone solo metadatos de acceso. "
                "Consulte el geoportal oficial SGC para datos y productos."
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
            f"Servicio Geológico Colombiano. ({accessed[:4]}). "
            f"{item['title']}. {INSTITUTION}. {url}"
        )
        return {
            "source": "SGC",
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
