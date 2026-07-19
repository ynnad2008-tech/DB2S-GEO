"""
Conector MapBiomas — enriquecimiento operativo DB2S-GEO.

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

SOURCE_ID = "mapbiomas"
INSTITUTION = "MapBiomas Colombia / Red Amazónica de Información Socioambiental"
HOMEPAGE = "https://colombia.mapbiomas.org"
LICENSE = "Según términos MapBiomas Colombia / colección específica"

_RESOURCES: dict[str, dict[str, Any]] = {
    "mapbiomas:agua-colombia": {
        "resource_id": "mapbiomas:agua-colombia",
        "title": "MapBiomas Agua Colombia — agua superficial",
        "type": "dataset",
        "domains": ["hidrologia", "observacion_tierra"],
        "primary_domain": "hidrologia",
        "keywords": [
            "agua",
            "superficial",
            "glaciares",
            "dinamica",
            "hidrica",
            "perdida",
            "ganancia",
            "mapbiomas",
            "colombia",
        ],
        "description": (
            "Colección MapBiomas Agua Colombia: dinámica de agua superficial "
            "(mensual/anual), transiciones y tendencias. Apoya análisis de "
            "pérdida/ganancia hídrica y monitoreo de cuerpos de agua. "
            "DB2S-GEO solo documenta el acceso; no descarga rasters."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "1998–2024 (según colección publicada)",
        "formats": ["GeoTIFF", "plataforma web", "estadísticas"],
        "homepage": HOMEPAGE,
        "portal_url": "https://plataforma.agua.mapbiomas.org/",
        "documentation_url": (
            "https://colombia.mapbiomas.org/metodologia-mapbiomas-agua/"
        ),
        "endpoints": [
            {
                "method": "portal",
                "url": "https://plataforma.agua.mapbiomas.org/",
                "label": "Plataforma MapBiomas Agua",
            },
            {
                "method": "portal",
                "url": (
                    "https://colombia.mapbiomas.org/metodologia-mapbiomas-agua/"
                ),
                "label": "Metodología MapBiomas Agua Colombia",
            },
            {
                "method": "portal",
                "url": HOMEPAGE,
                "label": "MapBiomas Colombia",
            },
        ],
        "access_methods": ["portal", "platform"],
        "citation_reference": (
            "MapBiomas Colombia. Colección MapBiomas Agua Colombia — "
            "dinámica de agua superficial. "
            "https://plataforma.agua.mapbiomas.org/"
        ),
        "doi": "",
    },
    "mapbiomas:cobertura-colombia": {
        "resource_id": "mapbiomas:cobertura-colombia",
        "title": "MapBiomas Colombia — cobertura y uso del suelo",
        "type": "dataset",
        "domains": ["observacion_tierra", "agricultura"],
        "primary_domain": "observacion_tierra",
        "keywords": [
            "cobertura",
            "uso",
            "suelo",
            "lulc",
            "paisaje",
            "monitoreo",
            "territorial",
            "cambio",
            "transicion",
            "clasificacion",
            "mapbiomas",
            "colombia",
        ],
        "description": (
            "Colección anual de mapas de cobertura y uso del suelo de "
            "MapBiomas Colombia (Colección 3.0, serie histórica desde 1985). "
            "Disponible vía portal, descargas GeoTIFF y assets en Google "
            "Earth Engine. Apoya monitoreo territorial, cambio de cobertura "
            "y análisis de paisaje. DB2S-GEO solo documenta el acceso; "
            "no descarga rasters."
        ),
        "spatial_coverage": "Colombia (superficie continental)",
        "temporal_coverage": "1985–2024 (según colección publicada)",
        "formats": ["GeoTIFF", "GEE asset", "plataforma web", "estadísticas"],
        "homepage": HOMEPAGE,
        "portal_url": HOMEPAGE,
        "documentation_url": "https://colombia.mapbiomas.org/herramientas/",
        "endpoints": [
            {
                "method": "portal",
                "url": HOMEPAGE,
                "label": "MapBiomas Colombia",
            },
            {
                "method": "portal",
                "url": (
                    "https://colombia.mapbiomas.org/"
                    "segunda-coleccion-de-mapbiomas-colombia/"
                ),
                "label": "Colecciones — descarga cobertura y uso",
            },
            {
                "method": "portal",
                "url": "https://colombia.mapbiomas.org/herramientas/",
                "label": "Herramientas y assets GEE MapBiomas Colombia",
            },
            {
                "method": "gee",
                "url": (
                    "https://code.earthengine.google.com/"
                    "?asset=projects/mapbiomas-colombia/assets/"
                    "LULC/COLECCION3/INTEGRACION/COLOMBIA-1"
                ),
                "label": (
                    "GEE asset Colección 3.0 — "
                    "projects/mapbiomas-colombia/assets/"
                    "LULC/COLECCION3/INTEGRACION/COLOMBIA-1"
                ),
            },
        ],
        "access_methods": ["portal", "platform", "gee"],
        "citation_reference": (
            "MapBiomas Colombia. Colección de mapas anuales de cobertura y "
            "uso del suelo (Colección 3.0). "
            "https://colombia.mapbiomas.org/"
        ),
        "doi": "",
    },
    "mapbiomas:transiciones-cobertura": {
        "resource_id": "mapbiomas:transiciones-cobertura",
        "title": "MapBiomas Colombia — transiciones de cobertura y uso",
        "type": "dataset",
        "domains": ["observacion_tierra", "agricultura"],
        "primary_domain": "observacion_tierra",
        "keywords": [
            "transiciones",
            "dinamica",
            "territorial",
            "cambio",
            "uso",
            "cobertura",
            "transformacion",
            "paisaje",
            "multitemporal",
            "estadisticas",
            "mapbiomas",
            "colombia",
        ],
        "description": (
            "Mapas de transición entre años seleccionados de la Colección 3.0 "
            "de MapBiomas Colombia: dinámica de cambio de cobertura y uso "
            "del suelo, transformación del paisaje y estadísticas "
            "multitemporales. Acceso vía portal, herramientas y asset GEE. "
            "DB2S-GEO solo documenta el acceso; no descarga rasters."
        ),
        "spatial_coverage": "Colombia (superficie continental)",
        "temporal_coverage": "Pares de años según colección publicada (desde 1985)",
        "formats": ["GeoTIFF", "GEE asset", "plataforma web", "estadísticas"],
        "homepage": HOMEPAGE,
        "portal_url": HOMEPAGE,
        "documentation_url": "https://colombia.mapbiomas.org/herramientas/",
        "endpoints": [
            {
                "method": "portal",
                "url": "https://colombia.mapbiomas.org/herramientas/",
                "label": "Herramientas — transiciones MapBiomas Colombia",
            },
            {
                "method": "portal",
                "url": HOMEPAGE,
                "label": "MapBiomas Colombia",
            },
            {
                "method": "gee",
                "url": (
                    "https://code.earthengine.google.com/"
                    "?asset=projects/mapbiomas-colombia/assets/"
                    "LULC/COLECCION3/INTEGRACION/"
                    "mapbiomas_colombia_collection3_transitions_v1"
                ),
                "label": (
                    "GEE asset transiciones Col. 3.0 — "
                    "projects/mapbiomas-colombia/assets/"
                    "LULC/COLECCION3/INTEGRACION/"
                    "mapbiomas_colombia_collection3_transitions_v1"
                ),
            },
        ],
        "access_methods": ["portal", "platform", "gee"],
        "citation_reference": (
            "MapBiomas Colombia. Mapas de transición de cobertura y uso del "
            "suelo (Colección 3.0). "
            "https://colombia.mapbiomas.org/herramientas/"
        ),
        "doi": "",
    },
}


class MapbiomasConnector(BaseConnector):
    connector_id = SOURCE_ID
    source_name = "MapBiomas"
    version = "1.2.0"

    def identify(self) -> dict[str, Any]:
        return normalize_source(
            source_id=SOURCE_ID,
            source="MapBiomas",
            institution=INSTITUTION,
            country_or_scope="Colombia / Panamazonía",
            domains=["observacion_tierra", "hidrologia", "agricultura"],
            access_methods=["portal", "platform", "gee"],
            description=(
                "Iniciativa de mapeo de cobertura, uso del suelo y dinámica "
                "de agua superficial (MapBiomas Colombia). "
                "DB2S-GEO solo documenta acceso; no descarga productos."
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
                "DB2S-GEO no descarga colecciones MapBiomas. "
                "Use la plataforma oficial y cite la colección correspondiente."
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
            f"MapBiomas. ({accessed[:4]}). {item['title']}. "
            f"{INSTITUTION}. {url}"
        )
        return {
            "source": "MapBiomas",
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
