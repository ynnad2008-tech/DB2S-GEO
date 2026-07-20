"""
Conector IDEAM — Fase 1 Discovery MVP.

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

SOURCE_ID = "ideam"
INSTITUTION = (
    "Instituto de Hidrología, Meteorología y Estudios Ambientales"
)
HOMEPAGE = "https://www.ideam.gov.co"
LICENSE = "Datos abiertos institucionales / términos IDEAM y datos.gov.co"

# Catálogo curado (Human Curation) — recursos representativos, no índice vivo.
_RESOURCES: dict[str, dict[str, Any]] = {
    "ideam:estaciones-meteorologicas": {
        "resource_id": "ideam:estaciones-meteorologicas",
        "title": "Red de estaciones meteorológicas",
        "type": "dataset",
        "domains": ["clima"],
        "primary_domain": "clima",
        "keywords": [
            "estaciones",
            "meteorologia",
            "clima",
            "temperatura",
            "ideam",
        ],
        "description": (
            "Información de estaciones meteorológicas y variables climáticas "
            "administradas por el IDEAM."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Histórico / actualizaciones institucionales",
        "formats": ["CSV", "GeoJSON", "servicios web"],
        "homepage": HOMEPAGE,
        "portal_url": "https://www.ideam.gov.co",
        "documentation_url": "https://www.ideam.gov.co",
        "endpoints": [
            {
                "method": "portal",
                "url": "https://www.ideam.gov.co",
                "label": "Portal institucional IDEAM",
            },
            {
                "method": "portal",
                "url": "https://www.datos.gov.co",
                "label": "Datos abiertos Colombia (conjuntos IDEAM)",
            },
        ],
        "access_methods": ["portal", "api", "arcgis"],
        "citation_reference": (
            "IDEAM. Red de estaciones meteorológicas. "
            "Instituto de Hidrología, Meteorología y Estudios Ambientales."
        ),
        "doi": "",
    },
    "ideam:precipitacion": {
        "resource_id": "ideam:precipitacion",
        "title": "Precipitación",
        "type": "dataset",
        "domains": ["clima", "hidrologia"],
        "primary_domain": "clima",
        "keywords": [
            "precipitacion",
            "lluvia",
            "meteorologia",
        ],
        "description": (
            "Productos e información de precipitación para análisis "
            "hidrológicos y climáticos en Colombia."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Series históricas institucionales",
        "formats": ["CSV", "raster", "tablas"],
        "homepage": HOMEPAGE,
        "portal_url": "https://www.ideam.gov.co",
        "documentation_url": "https://www.ideam.gov.co",
        "endpoints": [
            {
                "method": "portal",
                "url": "https://www.ideam.gov.co",
                "label": "Portal institucional IDEAM",
            }
        ],
        "access_methods": ["portal", "api"],
        "citation_reference": (
            "IDEAM. Información de precipitación. "
            "Instituto de Hidrología, Meteorología y Estudios Ambientales."
        ),
        "doi": "",
    },
    "ideam:hidrologia": {
        "resource_id": "ideam:hidrologia",
        "title": "Información hidrológica",
        "type": "dataset",
        "domains": ["hidrologia"],
        "primary_domain": "hidrologia",
        "keywords": [
            "hidrologia",
            "caudales",
            "niveles",
            "cuencas",
            "ideam",
        ],
        "description": (
            "Datos e información hidrológica (caudales, niveles y productos "
            "relacionados) bajo responsabilidad del IDEAM."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Series institucionales",
        "formats": ["CSV", "tablas", "servicios"],
        "homepage": HOMEPAGE,
        "portal_url": "https://www.ideam.gov.co",
        "documentation_url": "https://www.ideam.gov.co",
        "endpoints": [
            {
                "method": "portal",
                "url": "https://www.ideam.gov.co",
                "label": "Portal institucional IDEAM",
            }
        ],
        "access_methods": ["portal", "api", "arcgis"],
        "citation_reference": (
            "IDEAM. Información hidrológica. "
            "Instituto de Hidrología, Meteorología y Estudios Ambientales."
        ),
        "doi": "",
    },
    "ideam:capas-ideam-rest": {
        "resource_id": "ideam:capas-ideam-rest",
        "title": "Capas IDEAM (ArcGIS REST FeatureServer)",
        "type": "geoservice",
        "domains": ["clima", "hidrologia"],
        "primary_domain": "clima",
        "keywords": [
            "arcgis",
            "rest",
            "featureserver",
            "capas",
            "geoservicio",
            "ideam"
        ],
        "description": (
            "Servicio ArcGIS REST FeatureServer Capas_Ideam del visualizador "
            "IDEAM: acceso programático a capas geoespaciales institucionales. "
            "DB2S-GEO solo documenta el endpoint; no ejecuta consultas remotas."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Según publicación institucional del servicio",
        "formats": ["ArcGIS REST", "JSON", "GeoJSON (vía query del servicio)"],
        "homepage": "https://visualizador.ideam.gov.co/gisserver/rest/services",
        "portal_url": "https://visualizador.ideam.gov.co/gisserver/rest/services",
        "documentation_url": (
            "https://visualizador.ideam.gov.co/gisserver/rest/services/"
            "Capas_Ideam/FeatureServer"
        ),
        "endpoints": [
            {
                "method": "arcgis",
                "url": (
                    "https://visualizador.ideam.gov.co/gisserver/rest/services/"
                    "Capas_Ideam/FeatureServer"
                ),
                "label": "Capas_Ideam FeatureServer",
            },
            {
                "method": "arcgis",
                "url": "https://visualizador.ideam.gov.co/gisserver/rest/services",
                "label": "Directorio ArcGIS REST IDEAM",
            },
        ],
        "access_methods": ["arcgis", "portal"],
        "citation_reference": (
            "IDEAM. Capas_Ideam (ArcGIS REST FeatureServer). "
            "Instituto de Hidrología, Meteorología y Estudios Ambientales. "
            "https://visualizador.ideam.gov.co/gisserver/rest/services/"
            "Capas_Ideam/FeatureServer"
        ),
        "doi": "",
    },
    "ideam:amenaza-inundacion": {
        "resource_id": "ideam:amenaza-inundacion",
        "title": "Amenaza por inundación (ArcGIS REST MapServer)",
        "type": "geoservice",
        "domains": ["hidrologia", "clima"],
        "primary_domain": "hidrologia",
        "keywords": [
            "inundacion",
            "amenaza",
            "riesgo",
            "hidrologia",
            "arcgis",
            "mapserver",
            "ideam"
        ],
        "description": (
            "Servicio ArcGIS REST MapServer Amenaza_Ambiental del visualizador "
            "IDEAM, con capas de amenaza e inundación para centros poblados y "
            "productos relacionados. DB2S-GEO solo documenta el endpoint; "
            "no ejecuta consultas remotas."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Según publicación institucional del servicio",
        "formats": ["ArcGIS REST", "JSON", "GeoJSON (vía query del servicio)"],
        "homepage": "https://visualizador.ideam.gov.co/gisserver/rest/services",
        "portal_url": "https://visualizador.ideam.gov.co/gisserver/rest/services",
        "documentation_url": (
            "https://visualizador.ideam.gov.co/gisserver/rest/services/"
            "Amenaza_Ambiental/MapServer"
        ),
        "endpoints": [
            {
                "method": "arcgis",
                "url": (
                    "https://visualizador.ideam.gov.co/gisserver/rest/services/"
                    "Amenaza_Ambiental/MapServer"
                ),
                "label": "Amenaza_Ambiental MapServer",
            },
            {
                "method": "arcgis",
                "url": (
                    "https://visualizador.ideam.gov.co/gisserver/rest/services/"
                    "Amenaza_Ambiental/MapServer/layers"
                ),
                "label": "Capas Amenaza_Ambiental (listado)",
            },
        ],
        "access_methods": ["arcgis", "portal"],
        "citation_reference": (
            "IDEAM. Amenaza_Ambiental (ArcGIS REST MapServer). "
            "Instituto de Hidrología, Meteorología y Estudios Ambientales. "
            "https://visualizador.ideam.gov.co/gisserver/rest/services/"
            "Amenaza_Ambiental/MapServer"
        ),
        "doi": "",
    },
    "ideam:estado-ecosistemas": {
        "resource_id": "ideam:estado-ecosistemas",
        "title": "Estado de los ecosistemas (IDEAM)",
        "type": "geoservice",
        "domains": ["biodiversidad", "oceanos_costas"],
        "primary_domain": "biodiversidad",
        "keywords": [
            "ecosistemas",
            "conservacion",
            "restauracion",
            "monitoreo",
            "ambiental",
            "estado",
            "cobertura",
            "arcgis",
            "mapserver",
            "ideam",
        ],
        "description": (
            "Servicio ArcGIS REST Estado_Ecosistemas del IDEAM: capas de "
            "ecosistemas continentales, marinos y costeros. Apoya "
            "conservación, restauración y monitoreo ambiental. "
            "DB2S-GEO solo documenta el endpoint; no ejecuta consultas remotas."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Según publicación institucional (p. ej. 100K 2024)",
        "formats": ["ArcGIS REST", "JSON", "GeoJSON (vía query del servicio)"],
        "homepage": "https://visualizador.ideam.gov.co/gisserver/rest/services",
        "portal_url": "https://ideam.gov.co/geoportal-ambiental-institucional",
        "documentation_url": (
            "https://visualizador.ideam.gov.co/gisserver/rest/services/"
            "Estado_Ecosistemas/MapServer"
        ),
        "endpoints": [
            {
                "method": "arcgis",
                "url": (
                    "https://visualizador.ideam.gov.co/gisserver/rest/services/"
                    "Estado_Ecosistemas/MapServer"
                ),
                "label": "Estado_Ecosistemas MapServer",
            },
            {
                "method": "arcgis",
                "url": (
                    "https://visualizador.ideam.gov.co/gisserver/rest/services/"
                    "Estado_Ecosistemas/FeatureServer"
                ),
                "label": "Estado_Ecosistemas FeatureServer",
            },
        ],
        "access_methods": ["arcgis", "portal"],
        "citation_reference": (
            "IDEAM. Estado de los ecosistemas (Estado_Ecosistemas MapServer). "
            "Instituto de Hidrología, Meteorología y Estudios Ambientales. "
            "https://visualizador.ideam.gov.co/gisserver/rest/services/"
            "Estado_Ecosistemas/MapServer"
        ),
        "doi": "",
    },
    "ideam:fews-colombia": {
        "resource_id": "ideam:fews-colombia",
        "title": "FEWS Colombia — alertas y pronóstico hidrológico (IDEAM)",
        "type": "portal",
        "domains": ["hidrologia", "clima"],
        "primary_domain": "hidrologia",
        "keywords": [
            "alertas",
            "tempranas",
            "pronostico",
            "hidrologico",
            "niveles",
            "rio",
            "inundaciones",
            "monitoreo",
            "fews",
            "ideam"
        ],
        "description": (
            "Plataforma FEWS-Colombia del IDEAM (sistema operacional de "
            "pronóstico hidrológico): monitoreo de estaciones, niveles y "
            "alertas tempranas por inundación. Apoya gestión del riesgo "
            "hidrológico. DB2S-GEO solo documenta el acceso; no opera FEWS."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Operativo / actualizaciones institucionales",
        "formats": ["portal web", "series de tiempo (visor)"],
        "homepage": "https://www.ideam.gov.co/web/agua/fews",
        "portal_url": "https://fews.ideam.gov.co/colombia/MapaEstacionesColombiaEstado.html",
        "documentation_url": "https://www.ideam.gov.co/web/agua/fews",
        "endpoints": [
            {
                "method": "portal",
                "url": (
                    "https://fews.ideam.gov.co/colombia/"
                    "MapaEstacionesColombiaEstado.html"
                ),
                "label": "Visor FEWS-Colombia (estaciones)",
            },
            {
                "method": "portal",
                "url": "https://www.ideam.gov.co/web/agua/fews",
                "label": "Información institucional FEWS IDEAM",
            },
        ],
        "access_methods": ["portal"],
        "citation_reference": (
            "IDEAM. FEWS-Colombia — Sistema operacional de pronóstico "
            "hidrológico. Instituto de Hidrología, Meteorología y Estudios "
            "Ambientales. "
            "https://fews.ideam.gov.co/colombia/MapaEstacionesColombiaEstado.html"
        ),
        "doi": "",
    },
}


class IdeamConnector(BaseConnector):
    connector_id = SOURCE_ID
    source_name = "IDEAM"
    version = "1.4.0"

    def identify(self) -> dict[str, Any]:
        return normalize_source(
            source_id=SOURCE_ID,
            source="IDEAM",
            institution=INSTITUTION,
            country_or_scope="Colombia",
            domains=["clima", "hidrologia", "biodiversidad", "oceanos_costas"],
            access_methods=["api", "portal", "arcgis"],
            description=(
                "Autoridad nacional colombiana en hidrología, meteorología "
                "y estudios ambientales. Fuente oficial de clima e hidrología."
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
                "DB2S-GEO expone solo información de acceso. "
                "La consulta o descarga debe realizarse en los portales oficiales."
            ),
            "read_only": True,
            "downloads_supported": False,
        }

    def cite(self, resource_id: str) -> dict[str, Any]:
        item = find_resource(_RESOURCES, resource_id)
        if not item:
            return resource_not_found(resource_id, SOURCE_ID)
        accessed = today_iso()
        reference = item["citation_reference"]
        url = item["homepage"]
        apa = (
            f"IDEAM. ({accessed[:4]}). {item['title']}. "
            f"{INSTITUTION}. {url}"
        )
        return {
            "source": "IDEAM",
            "institution": INSTITUTION,
            "reference": reference,
            "url": url,
            "accessed": accessed,
            "apa": apa,
            "doi": item.get("doi") or "",
            "license": LICENSE,
            "resource_id": item["resource_id"],
            "source_id": SOURCE_ID,
        }
