"""
Conector INVIAS — enriquecimiento operativo DB2S-GEO.

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

SOURCE_ID = "invias"
INSTITUTION = "Instituto Nacional de Vías (INVIAS)"
HOMEPAGE = "https://www.invias.gov.co"
LICENSE = "Según términos INVIAS / HERMES"

_RESOURCES: dict[str, dict[str, Any]] = {
    "invias:hermes": {
        "resource_id": "invias:hermes",
        "title": "HERMES — Sistema de Información Vial (INVIAS)",
        "type": "catalog",
        "domains": ["observacion_tierra"],
        "primary_domain": "observacion_tierra",
        "keywords": [
            "hermes",
            "siv",
            "red",
            "vial",
            "nacional",
            "carreteras",
            "puentes",
            "peajes",
            "viaje",
            "seguro",
            "conectividad",
            "territorial",
            "invias",
            "colombia",
        ],
        "description": (
            "Sistema de Información Vial HERMES (SIV) del INVIAS: consulta "
            "de red vial nacional (concesionada y no concesionada), puentes, "
            "peajes y planificación de rutas. Incluye visor HERMES2 y "
            "servicios ArcGIS REST (mapa de carreteras / SIV). "
            "DB2S-GEO solo documenta el acceso; no descarga geometrías."
        ),
        "spatial_coverage": "Colombia (red vial a cargo / publicada)",
        "temporal_coverage": "Según actualizaciones HERMES / capas publicadas",
        "formats": ["visor web", "MapServer", "portal"],
        "homepage": HOMEPAGE,
        "portal_url": "https://hermes2.invias.gov.co/SIV/",
        "documentation_url": "https://hermes2.invias.gov.co/",
        "endpoints": [
            {
                "method": "portal",
                "url": "https://hermes2.invias.gov.co/SIV/",
                "label": "HERMES2 — Sistema de Información Vial",
            },
            {
                "method": "arcgis",
                "url": (
                    "https://hermes.invias.gov.co/arcgis/rest/services/"
                    "Mapa_Carreteras/Mapa_de_Carreteras/MapServer"
                ),
                "label": "MapServer Mapa de Carreteras INVIAS",
            },
            {
                "method": "arcgis",
                "url": (
                    "https://hermes.invias.gov.co/arcgis/rest/services/"
                    "Sistema_informacion_vial/SIV_V20/MapServer"
                ),
                "label": "MapServer SIV V20 HERMES",
            },
        ],
        "access_methods": ["portal", "arcgis"],
        "citation_reference": (
            "Instituto Nacional de Vías (INVIAS). HERMES — Sistema de "
            "Información Vial. "
            "https://hermes2.invias.gov.co/SIV/"
        ),
        "doi": "",
    },
    "invias:vulnerabilidad-faunistica": {
        "resource_id": "invias:vulnerabilidad-faunistica",
        "title": "Mapa de vulnerabilidad faunística al atropellamiento (INVIAS)",
        "type": "dataset",
        "domains": ["biodiversidad", "observacion_tierra"],
        "primary_domain": "biodiversidad",
        "keywords": [
            "vulnerabilidad",
            "faunistica",
            "atropellamiento",
            "fauna",
            "corredores",
            "ecologicos",
            "conectividad",
            "ecologica",
            "infraestructura",
            "vial",
            "biodiversidad",
            "sukubun",
            "invias",
            "colombia",
        ],
        "description": (
            "Mapa nacional de vulnerabilidad faunística y riesgo de "
            "atropellamiento de fauna silvestre en vías primarias a cargo "
            "del INVIAS (ITM / Política de Sostenibilidad). Apoya pasos de "
            "fauna y mitigación en proyectos viales. Visor en HERMES. "
            "DB2S-GEO solo documenta el acceso; no descarga capas."
        ),
        "spatial_coverage": "Colombia (red vial primaria INVIAS)",
        "temporal_coverage": "Según versión del mapa publicada por INVIAS",
        "formats": ["visor web", "mapa", "portal"],
        "homepage": HOMEPAGE,
        "portal_url": "https://hermes.invias.gov.co/VulnerabilidadFaunistica/",
        "documentation_url": (
            "https://mintransporte.gov.co/publicaciones/10864/"
            "gobierno-nacional-lanza-mapa-para-identificar-puntos-de-mayor-"
            "vulnerabilidad-faunistica-al-atropellamiento-en-proyectos-viales/"
        ),
        "endpoints": [
            {
                "method": "portal",
                "url": "https://hermes.invias.gov.co/VulnerabilidadFaunistica/",
                "label": "Visor vulnerabilidad faunística INVIAS",
            },
            {
                "method": "portal",
                "url": (
                    "https://mintransporte.gov.co/publicaciones/10864/"
                    "gobierno-nacional-lanza-mapa-para-identificar-puntos-de-"
                    "mayor-vulnerabilidad-faunistica-al-atropellamiento-en-"
                    "proyectos-viales/"
                ),
                "label": "Lanzamiento oficial — MinTransporte / INVIAS",
            },
            {
                "method": "portal",
                "url": HOMEPAGE,
                "label": "Portal institucional INVIAS",
            },
        ],
        "access_methods": ["portal"],
        "citation_reference": (
            "Instituto Nacional de Vías (INVIAS) / ITM. Mapa de "
            "vulnerabilidad faunística al atropellamiento en vías. "
            "https://hermes.invias.gov.co/VulnerabilidadFaunistica/"
        ),
        "doi": "",
    },
    "invias:datos-abiertos-viales": {
        "resource_id": "invias:datos-abiertos-viales",
        "title": "Datos abiertos de infraestructura vial (INVIAS)",
        "type": "dataset",
        "domains": ["observacion_tierra"],
        "primary_domain": "observacion_tierra",
        "keywords": [
            "datos",
            "abiertos",
            "vias",
            "peajes",
            "puentes",
            "postes",
            "referencia",
            "infraestructura",
            "vial",
            "opendata",
            "red",
            "vial",
            "invias",
            "colombia",
        ],
        "description": (
            "Conjuntos de datos abiertos oficiales del INVIAS sobre "
            "infraestructura vial: red vial, puentes, pontones, peajes y "
            "postes de referencia. Disponibles vía Open Data ArcGIS INVIAS, "
            "FeatureServer OpenData/HERMES y datos.gov.co. "
            "DB2S-GEO solo documenta el acceso; no descarga tablas."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Según publicación de cada conjunto abierto",
        "formats": ["FeatureServer", "CSV/tablas", "portal Open Data"],
        "homepage": HOMEPAGE,
        "portal_url": "https://inviasopendata-invias.opendata.arcgis.com/",
        "documentation_url": (
            "https://www.invias.gov.co/publicaciones/6264/"
            "sistema-de-informacion-vial/"
        ),
        "endpoints": [
            {
                "method": "portal",
                "url": "https://inviasopendata-invias.opendata.arcgis.com/",
                "label": "Portal Open Data ArcGIS INVIAS",
            },
            {
                "method": "arcgis",
                "url": (
                    "https://hermes.invias.gov.co/arcgis/rest/services/"
                    "OpenData/ServiciosOpenData/FeatureServer"
                ),
                "label": "FeatureServer OpenData — red, peajes, puentes",
            },
            {
                "method": "portal",
                "url": (
                    "https://www.datos.gov.co/Transporte/"
                    "Tr-fico-Peajes-Invias/tcfu-jngt"
                ),
                "label": "Datos.gov.co — Tráfico Peajes INVIAS",
            },
        ],
        "access_methods": ["portal", "arcgis"],
        "citation_reference": (
            "Instituto Nacional de Vías (INVIAS). Datos abiertos de "
            "infraestructura vial. "
            "https://inviasopendata-invias.opendata.arcgis.com/"
        ),
        "doi": "",
    },
}


class InviasConnector(BaseConnector):
    connector_id = SOURCE_ID
    source_name = "INVIAS"
    version = "1.1.0"

    def identify(self) -> dict[str, Any]:
        return normalize_source(
            source_id=SOURCE_ID,
            source="INVIAS",
            institution=INSTITUTION,
            country_or_scope="Colombia",
            domains=["observacion_tierra", "biodiversidad"],
            access_methods=["portal", "arcgis"],
            description=(
                "Instituto Nacional de Vías: HERMES (SIV), datos abiertos "
                "viales y mapa de vulnerabilidad faunística. "
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
                "DB2S-GEO no descarga productos HERMES/INVIAS. "
                "Consulte el visor oficial / MapServer y cite la fuente."
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
            f"INVIAS. ({accessed[:4]}). {item['title']}. "
            f"{INSTITUTION}. {url}"
        )
        return {
            "source": "INVIAS",
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
