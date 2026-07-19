"""
Conector IGAC — enriquecimiento operativo DB2S-GEO.

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

SOURCE_ID = "igac"
INSTITUTION = "Instituto Geográfico Agustín Codazzi"
HOMEPAGE = "https://www.igac.gov.co"
LICENSE = "Datos abiertos / términos IGAC según producto"

_RESOURCES: dict[str, dict[str, Any]] = {
    "igac:modelo-terreno-colombia": {
        "resource_id": "igac:modelo-terreno-colombia",
        "title": "Modelo digital de terreno de Colombia (IGAC)",
        "type": "dataset",
        "domains": ["observacion_tierra", "suelos"],
        "primary_domain": "observacion_tierra",
        "keywords": [
            "topografia",
            "relieve",
            "cuencas",
            "modelo",
            "terreno",
            "mdt",
            "dem",
            "amenazas",
            "geomorfologia",
            "igac",
            "colombia",
        ],
        "description": (
            "Modelos digitales de terreno (MDT) y productos altimétricos "
            "oficiales del IGAC, disponibles vía Colombia en Mapas y datos "
            "abiertos geoespaciales. Apoya topografía, análisis de cuencas, "
            "modelación de amenazas y geomorfología. DB2S-GEO solo documenta "
            "el acceso; no descarga rasters."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Según escala y proyecto cartográfico publicado",
        "formats": ["GeoTIFF", "servicios web", "portal"],
        "homepage": HOMEPAGE,
        "portal_url": "https://www.colombiaenmapas.gov.co/",
        "documentation_url": (
            "https://www.igac.gov.co/datos-abiertos/datos-abiertos-geoespaciales"
        ),
        "endpoints": [
            {
                "method": "portal",
                "url": "https://www.colombiaenmapas.gov.co/",
                "label": "Colombia en Mapas (IGAC)",
            },
            {
                "method": "portal",
                "url": (
                    "https://www.igac.gov.co/datos-abiertos/"
                    "datos-abiertos-geoespaciales"
                ),
                "label": "Datos abiertos geoespaciales IGAC",
            },
        ],
        "access_methods": ["portal", "arcgis"],
        "citation_reference": (
            "Instituto Geográfico Agustín Codazzi (IGAC). Modelos digitales "
            "de terreno / cartografía básica oficial. "
            "https://www.colombiaenmapas.gov.co/"
        ),
        "doi": "",
    },
    "igac:estudio-general-suelos": {
        "resource_id": "igac:estudio-general-suelos",
        "title": "Estudios generales de suelos y capacidad de uso (IGAC)",
        "type": "dataset",
        "domains": ["suelos", "agricultura"],
        "primary_domain": "suelos",
        "keywords": [
            "suelos",
            "estudio",
            "general",
            "capacidad",
            "uso",
            "aptitud",
            "edafologia",
            "agrologia",
            "igac",
            "colombia",
        ],
        "description": (
            "Estudios Generales de Suelos y Capacidad de Uso del IGAC "
            "(escala 1:100.000): caracterización y clasificación de suelos "
            "a nivel departamental, aptitud y limitaciones de uso. "
            "DB2S-GEO solo documenta el acceso; no descarga productos."
        ),
        "spatial_coverage": "Colombia (cobertura departamental según estudio)",
        "temporal_coverage": "Según publicación del estudio por departamento",
        "formats": ["mapas", "reportes", "servicios web", "portal"],
        "homepage": (
            "https://www.igac.gov.co/datos-abiertos/datos-abiertos-geoespaciales"
        ),
        "portal_url": "https://www.colombiaenmapas.gov.co/",
        "documentation_url": (
            "https://www.igac.gov.co/datos-abiertos/datos-abiertos-geoespaciales"
        ),
        "endpoints": [
            {
                "method": "portal",
                "url": (
                    "https://www.igac.gov.co/datos-abiertos/"
                    "datos-abiertos-geoespaciales"
                ),
                "label": "Datos abiertos geoespaciales — Agrología IGAC",
            },
            {
                "method": "portal",
                "url": "https://www.colombiaenmapas.gov.co/",
                "label": "Colombia en Mapas",
            },
        ],
        "access_methods": ["portal", "arcgis"],
        "citation_reference": (
            "Instituto Geográfico Agustín Codazzi (IGAC). Estudios Generales "
            "de Suelos y Capacidad de Uso (escala 1:100.000). "
            "https://www.igac.gov.co/datos-abiertos/datos-abiertos-geoespaciales"
        ),
        "doi": "",
    },
    "igac:agrologia-colombia": {
        "resource_id": "igac:agrologia-colombia",
        "title": "Agrología y clases agrológicas de Colombia (IGAC)",
        "type": "dataset",
        "domains": ["suelos", "agricultura"],
        "primary_domain": "suelos",
        "keywords": [
            "agrologia",
            "capacidad",
            "agrologica",
            "uso",
            "potencial",
            "ordenamiento",
            "productivo",
            "desarrollo",
            "rural",
            "igac",
            "colombia",
        ],
        "description": (
            "Información agrológica oficial del IGAC (Subdirección de "
            "Agrología): clases agrológicas, capacidad de uso y productos "
            "asociados para ordenamiento productivo y desarrollo rural. "
            "Consulta vía Colombia en Mapas. DB2S-GEO solo documenta el "
            "acceso; no descarga productos."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Según productos agrológicos publicados",
        "formats": ["portal web", "mapas", "servicios web"],
        "homepage": "https://www.igac.gov.co/node/24279",
        "portal_url": "https://www.colombiaenmapas.gov.co/",
        "documentation_url": "https://www.igac.gov.co/node/24279",
        "endpoints": [
            {
                "method": "portal",
                "url": "https://www.igac.gov.co/node/24279",
                "label": "Subdirección de Agrología IGAC",
            },
            {
                "method": "portal",
                "url": "https://www.colombiaenmapas.gov.co/",
                "label": "Colombia en Mapas (consulta clases agrológicas)",
            },
        ],
        "access_methods": ["portal", "arcgis"],
        "citation_reference": (
            "Instituto Geográfico Agustín Codazzi (IGAC). Subdirección de "
            "Agrología — información agrológica de Colombia. "
            "https://www.igac.gov.co/node/24279"
        ),
        "doi": "",
    },
    "igac:geoportal-nacional": {
        "resource_id": "igac:geoportal-nacional",
        "title": "Colombia en Mapas — geoportal nacional (IGAC / ICDE)",
        "type": "catalog",
        "domains": ["observacion_tierra", "suelos"],
        "primary_domain": "observacion_tierra",
        "keywords": [
            "geoportal",
            "cartografia",
            "base",
            "geografia",
            "oficial",
            "referencia",
            "espacial",
            "territorio",
            "catastro",
            "colombia",
            "en",
            "mapas",
            "icde",
            "igac",
        ],
        "description": (
            "Portal nacional de información geoespacial Colombia en Mapas, "
            "liderado por el IGAC y articulado con la ICDE. Centraliza "
            "cartografía base, geografía oficial, referencia espacial y "
            "datos territoriales/catastrales de entidades nacionales. "
            "DB2S-GEO solo documenta el acceso; no descarga capas."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Según capas y versiones publicadas en el portal",
        "formats": ["visor web", "servicios web", "descargas según capa"],
        "homepage": HOMEPAGE,
        "portal_url": "https://www.colombiaenmapas.gov.co/",
        "documentation_url": "https://www.colombiaenmapas.gov.co/inicio",
        "endpoints": [
            {
                "method": "portal",
                "url": "https://www.colombiaenmapas.gov.co/",
                "label": "Colombia en Mapas — geoportal nacional",
            },
            {
                "method": "portal",
                "url": "https://www.colombiaenmapas.gov.co/inicio",
                "label": "Inicio / guía Colombia en Mapas",
            },
            {
                "method": "portal",
                "url": (
                    "https://www.igac.gov.co/datos-abiertos/"
                    "datos-abiertos-geoespaciales"
                ),
                "label": "Datos abiertos geoespaciales IGAC",
            },
        ],
        "access_methods": ["portal", "arcgis"],
        "citation_reference": (
            "Instituto Geográfico Agustín Codazzi (IGAC) / ICDE. "
            "Colombia en Mapas — Portal Nacional de Información Geoespacial. "
            "https://www.colombiaenmapas.gov.co/"
        ),
        "doi": "",
    },
    "igac:servicios-geograficos": {
        "resource_id": "igac:servicios-geograficos",
        "title": "Servicios geográficos IGAC (ArcGIS REST / interoperabilidad)",
        "type": "catalog",
        "domains": ["observacion_tierra"],
        "primary_domain": "observacion_tierra",
        "keywords": [
            "servicios",
            "ogc",
            "wms",
            "wfs",
            "arcgis",
            "rest",
            "cartografia",
            "oficial",
            "interoperabilidad",
            "infraestructura",
            "datos",
            "espaciales",
            "geoservicios",
            "icde",
            "igac",
            "colombia",
        ],
        "description": (
            "Catálogo de geoservicios del IGAC (ArcGIS REST Server) y "
            "acceso interoperable vía Colombia en Mapas / ICDE (OGC y "
            "REST). Incluye cartografía oficial, catastro, relieve, límites "
            "y otros temas. DB2S-GEO solo documenta el acceso; no consume "
            "ni descarga servicios."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Según servicio y versión publicada",
        "formats": ["MapServer", "FeatureServer", "WMS/WFS vía ICDE", "REST"],
        "homepage": HOMEPAGE,
        "portal_url": "https://mapas.igac.gov.co/server/rest/services",
        "documentation_url": (
            "https://colombia-en-mapas.gitbook.io/colombia-en-mapas/"
            "funcionalidades/como-se-consumen-geoservicios/consumo-servicios-rest"
        ),
        "endpoints": [
            {
                "method": "arcgis",
                "url": "https://mapas.igac.gov.co/server/rest/services",
                "label": "Directorio ArcGIS REST Services IGAC",
            },
            {
                "method": "portal",
                "url": "https://www.icde.gov.co/geoservicio",
                "label": "Catálogo de geoservicios ICDE",
            },
            {
                "method": "portal",
                "url": "https://www.colombiaenmapas.gov.co/",
                "label": "Colombia en Mapas (consumo de geoservicios)",
            },
        ],
        "access_methods": ["arcgis", "portal", "ogc"],
        "citation_reference": (
            "Instituto Geográfico Agustín Codazzi (IGAC). Servicios "
            "geográficos ArcGIS REST / geoservicios ICDE. "
            "https://mapas.igac.gov.co/server/rest/services"
        ),
        "doi": "",
    },
    "igac:catastro-multiproposito": {
        "resource_id": "igac:catastro-multiproposito",
        "title": "Catastro Multipropósito y modelo LADM_COL (IGAC)",
        "type": "catalog",
        "domains": ["observacion_tierra"],
        "primary_domain": "observacion_tierra",
        "keywords": [
            "catastro",
            "multiproposito",
            "ladm",
            "ladm_col",
            "predial",
            "administracion",
            "territorio",
            "modernizacion",
            "catastral",
            "registro",
            "sinic",
            "igac",
            "colombia",
        ],
        "description": (
            "Marco nacional de Catastro Multipropósito del IGAC: modelo "
            "extendido Catastro-Registro LADM_COL, administración del "
            "territorio e información predial interoperable. Incluye "
            "documentación normativa y acceso a datos/catálogos oficiales. "
            "DB2S-GEO solo documenta el acceso; no descarga bases prediales."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Según versión del modelo y avance catastral",
        "formats": ["documentación", "modelo LADM_COL", "portal", "datos abiertos"],
        "homepage": HOMEPAGE,
        "portal_url": "https://www.igac.gov.co/catastro-multiproposito/ladmcol",
        "documentation_url": (
            "https://www.igac.gov.co/catastro-multiproposito/ladmcol"
        ),
        "endpoints": [
            {
                "method": "portal",
                "url": "https://www.igac.gov.co/catastro-multiproposito/ladmcol",
                "label": "LADM_COL — Catastro Multipropósito IGAC",
            },
            {
                "method": "portal",
                "url": "https://www.igac.gov.co/index.php/node/31261",
                "label": "Dirección de Gestión Catastral IGAC",
            },
            {
                "method": "portal",
                "url": (
                    "https://www.igac.gov.co/datos-abiertos/"
                    "datos-abiertos-geoespaciales"
                ),
                "label": "Datos abiertos geoespaciales / catastro IGAC",
            },
        ],
        "access_methods": ["portal"],
        "citation_reference": (
            "Instituto Geográfico Agustín Codazzi (IGAC). Catastro "
            "Multipropósito — Modelo Extendido Catastro-Registro LADM_COL. "
            "https://www.igac.gov.co/catastro-multiproposito/ladmcol"
        ),
        "doi": "",
    },
    "igac:datos-abiertos-catastro": {
        "resource_id": "igac:datos-abiertos-catastro",
        "title": "Datos abiertos catastrales IGAC (Dirección de Gestión Catastral)",
        "type": "dataset",
        "domains": ["observacion_tierra"],
        "primary_domain": "observacion_tierra",
        "keywords": [
            "datos",
            "abiertos",
            "bases",
            "catastrales",
            "predial",
            "gestion",
            "catastral",
            "alfanumerico",
            "geografico",
            "codigo",
            "predial",
            "nacional",
            "csv",
            "igac",
            "colombia",
        ],
        "description": (
            "Conjuntos de datos abiertos de la Dirección de Gestión "
            "Catastral del IGAC: bases geográficas y alfanuméricas "
            "prediales, catálogo de objetos, estructura del código predial "
            "y diccionarios de registros secuenciales. Apoya gestión "
            "catastral y reutilización pública. DB2S-GEO solo documenta "
            "el acceso; no descarga bases."
        ),
        "spatial_coverage": "Colombia (según cobertura publicada por el IGAC)",
        "temporal_coverage": "Actualización periódica según publicación DGC",
        "formats": ["CSV", "GeoJSON/SHP según conjunto", "PDF documentación", "portal"],
        "homepage": HOMEPAGE,
        "portal_url": "https://www.igac.gov.co/datos-abiertos/",
        "documentation_url": "https://www.igac.gov.co/index.php/node/31261",
        "endpoints": [
            {
                "method": "portal",
                "url": "https://www.igac.gov.co/datos-abiertos/",
                "label": "Portal de datos abiertos IGAC",
            },
            {
                "method": "portal",
                "url": "https://www.igac.gov.co/index.php/node/31261",
                "label": "Dirección de Gestión Catastral — datos abiertos",
            },
            {
                "method": "portal",
                "url": (
                    "https://www.igac.gov.co/datos-abiertos/"
                    "datos-abiertos-geoespaciales"
                ),
                "label": "Datos abiertos geoespaciales IGAC",
            },
        ],
        "access_methods": ["portal"],
        "citation_reference": (
            "Instituto Geográfico Agustín Codazzi (IGAC). Datos abiertos "
            "catastrales — Dirección de Gestión Catastral. "
            "https://www.igac.gov.co/datos-abiertos/"
        ),
        "doi": "",
    },
    "igac:colombia-en-mapas-catastro": {
        "resource_id": "igac:colombia-en-mapas-catastro",
        "title": "Colombia en Mapas — categoría Catastro",
        "type": "catalog",
        "domains": ["observacion_tierra"],
        "primary_domain": "observacion_tierra",
        "keywords": [
            "colombia",
            "en",
            "mapas",
            "categoria",
            "catastro",
            "cartografia",
            "catastral",
            "consulta",
            "territorial",
            "visualizacion",
            "base",
            "catastral",
            "nacional",
            "servicios",
            "geograficos",
            "igac",
        ],
        "description": (
            "Capas y productos de la categoría Catastro en Colombia en "
            "Mapas (IGAC/ICDE): cartografía catastral, base catastral "
            "nacional, visualización y descarga de servicios asociados. "
            "Complementa el geoportal general con enfoque predial. "
            "DB2S-GEO solo documenta el acceso; no descarga capas."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Según capas publicadas en Colombia en Mapas",
        "formats": ["visor web", "servicios web", "descargas según capa"],
        "homepage": HOMEPAGE,
        "portal_url": "https://www.colombiaenmapas.gov.co/",
        "documentation_url": "https://www.colombiaenmapas.gov.co/inicio/",
        "endpoints": [
            {
                "method": "portal",
                "url": "https://www.colombiaenmapas.gov.co/",
                "label": "Colombia en Mapas — categoría Catastro",
            },
            {
                "method": "portal",
                "url": "https://www.colombiaenmapas.gov.co/inicio/",
                "label": "Inicio Colombia en Mapas (temáticas Catastro)",
            },
            {
                "method": "arcgis",
                "url": "https://mapas.igac.gov.co/server/rest/services/catastro",
                "label": "Carpeta REST servicios Catastro IGAC",
            },
        ],
        "access_methods": ["portal", "arcgis"],
        "citation_reference": (
            "Instituto Geográfico Agustín Codazzi (IGAC) / ICDE. "
            "Colombia en Mapas — categoría Catastro. "
            "https://www.colombiaenmapas.gov.co/"
        ),
        "doi": "",
    },
    "igac:consulta-catastral": {
        "resource_id": "igac:consulta-catastral",
        "title": "Consulta Catastral (Colombia en Mapas / IGAC)",
        "type": "service",
        "domains": ["observacion_tierra"],
        "primary_domain": "observacion_tierra",
        "keywords": [
            "consulta",
            "catastral",
            "predial",
            "busqueda",
            "direccion",
            "numero",
            "predial",
            "coordenadas",
            "localizacion",
            "predios",
            "urbano",
            "rural",
            "igac",
            "colombia",
        ],
        "description": (
            "Herramienta de consulta catastral de Colombia en Mapas: "
            "búsqueda de predios urbanos y rurales por número predial, "
            "dirección o coordenadas, con información básica del terreno "
            "y construcciones. DB2S-GEO solo documenta el acceso; no "
            "ejecuta consultas remotas."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Según actualización de la base catastral publicada",
        "formats": ["visor web", "consulta interactiva", "JSON según descarga"],
        "homepage": HOMEPAGE,
        "portal_url": "https://www.colombiaenmapas.gov.co/",
        "documentation_url": (
            "https://colombia-en-mapas.gitbook.io/colombia-en-mapas/"
            "funcionalidades/consultas-avanzadas/como-hacer-una-consulta-catastral"
        ),
        "endpoints": [
            {
                "method": "portal",
                "url": "https://www.colombiaenmapas.gov.co/",
                "label": "Colombia en Mapas — Consulta Catastral",
            },
            {
                "method": "portal",
                "url": "https://www.colombiaenmapas.gov.co/inicio/",
                "label": "Inicio — acceso ConsultaCatastral",
            },
            {
                "method": "portal",
                "url": (
                    "https://colombia-en-mapas.gitbook.io/colombia-en-mapas/"
                    "funcionalidades/consultas-avanzadas/"
                    "como-hacer-una-consulta-catastral"
                ),
                "label": "Guía: cómo hacer una consulta catastral",
            },
        ],
        "access_methods": ["portal"],
        "citation_reference": (
            "Instituto Geográfico Agustín Codazzi (IGAC). Consulta "
            "Catastral — Colombia en Mapas. "
            "https://www.colombiaenmapas.gov.co/"
        ),
        "doi": "",
    },
    "igac:gestores-catastrales": {
        "resource_id": "igac:gestores-catastrales",
        "title": "Jurisdicción de gestores catastrales (IGAC)",
        "type": "dataset",
        "domains": ["observacion_tierra"],
        "primary_domain": "observacion_tierra",
        "keywords": [
            "gestores",
            "catastrales",
            "jurisdiccion",
            "habilitacion",
            "administracion",
            "territorial",
            "cobertura",
            "institucional",
            "descentralizado",
            "municipios",
            "mapa",
            "igac",
            "colombia",
        ],
        "description": (
            "Información sobre gestores catastrales habilitados por el "
            "IGAC y su jurisdicción municipal: cobertura institucional "
            "del servicio público catastral (IGAC y gestores "
            "territoriales). Disponible en Colombia en Mapas y páginas "
            "de regulación/habilitación. DB2S-GEO solo documenta el "
            "acceso; no descarga geometrías."
        ),
        "spatial_coverage": "Colombia (jurisdicciones municipales)",
        "temporal_coverage": "Según habilitación y mapa vigente IGAC",
        "formats": ["mapa", "visor web", "portal"],
        "homepage": HOMEPAGE,
        "portal_url": (
            "https://www.igac.gov.co/el-igac/areas-estrategicas/"
            "direccion-de-regulacion-y-habilitacion"
        ),
        "documentation_url": (
            "https://www.igac.gov.co/catastro-multiproposito/"
            "catastro-multiproposito"
        ),
        "endpoints": [
            {
                "method": "portal",
                "url": (
                    "https://www.igac.gov.co/el-igac/areas-estrategicas/"
                    "direccion-de-regulacion-y-habilitacion"
                ),
                "label": "Dirección de Regulación y Habilitación — gestores",
            },
            {
                "method": "portal",
                "url": (
                    "https://www.igac.gov.co/catastro-multiproposito/"
                    "catastro-multiproposito"
                ),
                "label": "Catastro Multipropósito — mapa de gestores",
            },
            {
                "method": "portal",
                "url": "https://www.colombiaenmapas.gov.co/",
                "label": "Colombia en Mapas — Gestores Catastrales",
            },
        ],
        "access_methods": ["portal"],
        "citation_reference": (
            "Instituto Geográfico Agustín Codazzi (IGAC). Jurisdicción "
            "de gestores catastrales habilitados. "
            "https://www.igac.gov.co/el-igac/areas-estrategicas/"
            "direccion-de-regulacion-y-habilitacion"
        ),
        "doi": "",
    },
}


class IgacConnector(BaseConnector):
    connector_id = SOURCE_ID
    source_name = "IGAC"
    version = "1.6.0"

    def identify(self) -> dict[str, Any]:
        return normalize_source(
            source_id=SOURCE_ID,
            source="IGAC",
            institution=INSTITUTION,
            country_or_scope="Colombia",
            domains=["observacion_tierra", "suelos", "agricultura"],
            access_methods=["portal", "arcgis", "ogc"],
            description=(
                "Autoridad cartográfica y catastral nacional de Colombia. "
                "Produce cartografía básica, MDT, suelos, geoportal, "
                "geoservicios y Catastro Multipropósito (LADM_COL). "
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
                "DB2S-GEO no descarga cartografía, MDT ni estudios de suelos "
                "IGAC. Use Colombia en Mapas / datos abiertos oficiales."
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
            f"IGAC. ({accessed[:4]}). {item['title']}. "
            f"{INSTITUTION}. {url}"
        )
        return {
            "source": "IGAC",
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
