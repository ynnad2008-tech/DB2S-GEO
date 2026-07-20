"""
Conector Google Earth Engine — Fase 1 Discovery MVP.

Metadatos curados humanamente. Read-only. Sin descarga ni ejecución remota.
No ejecuta código Earth Engine ni autentica cuentas.
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

SOURCE_ID = "gee"
INSTITUTION = "Google Earth Engine (Google LLC / partners)"
HOMEPAGE = "https://developers.google.com/earth-engine/datasets"
LICENSE = (
    "Según dataset en el catálogo GEE; términos de Google Earth Engine "
    "y licencia del productor original"
)

_RESOURCES: dict[str, dict[str, Any]] = {
    "gee:catalog": {
        "resource_id": "gee:catalog",
        "title": "Earth Engine Data Catalog",
        "type": "catalog",
        "domains": ["observacion_tierra"],
        "primary_domain": "observacion_tierra",
        "keywords": [
            "catalogo",
            "earth engine",
            "datasets",
            "observacion de la tierra",
            "gee",
        ],
        "description": (
            "Catálogo público de datasets accesibles vía Google Earth Engine "
            "(óptico, radar, clima, demografía, coberturas, etc.)."
        ),
        "spatial_coverage": "Global / según dataset",
        "temporal_coverage": "Según colección",
        "formats": ["Earth Engine Image/ImageCollection", "metadatos"],
        "homepage": "https://developers.google.com/earth-engine/datasets",
        "portal_url": "https://developers.google.com/earth-engine/datasets",
        "documentation_url": "https://developers.google.com/earth-engine",
        "endpoints": [
            {
                "method": "portal",
                "url": "https://developers.google.com/earth-engine/datasets",
                "label": "Earth Engine Data Catalog",
            },
            {
                "method": "platform",
                "url": "https://code.earthengine.google.com",
                "label": "Earth Engine Code Editor",
            },
        ],
        "access_methods": ["platform", "api", "portal"],
        "citation_reference": (
            "Gorelick, N., et al. (2017). Google Earth Engine: Planetary-scale "
            "geospatial analysis for everyone. Remote Sensing of Environment."
        ),
        "doi": "10.1016/j.rse.2017.06.031",
    },
    "gee:sentinel2": {
        "resource_id": "gee:sentinel2",
        "title": "Sentinel-2 (vía Earth Engine)",
        "type": "collection",
        "domains": ["observacion_tierra", "cobertura"],
        "primary_domain": "observacion_tierra",
        "keywords": [
            "sentinel-2",
            "optico",
            "copernicus",
            "earth engine",
            "cobertura",
        ],
        "description": (
            "Colecciones Sentinel-2 disponibles en el catálogo Earth Engine "
            "(acceso sujeto a cuenta GEE y términos ESA/Copernicus)."
        ),
        "spatial_coverage": "Global",
        "temporal_coverage": "2015–presente (según colección)",
        "formats": ["Earth Engine ImageCollection"],
        "homepage": (
            "https://developers.google.com/earth-engine/datasets/catalog/sentinel-2"
        ),
        "portal_url": (
            "https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED"
        ),
        "documentation_url": "https://developers.google.com/earth-engine/datasets",
        "endpoints": [
            {
                "method": "portal",
                "url": (
                    "https://developers.google.com/earth-engine/datasets/"
                    "catalog/COPERNICUS_S2_SR_HARMONIZED"
                ),
                "label": "COPERNICUS/S2_SR_HARMONIZED",
            }
        ],
        "access_methods": ["platform", "api"],
        "citation_reference": (
            "European Union / ESA / Copernicus; accessed via Google Earth Engine. "
            "Sentinel-2 MSI."
        ),
        "doi": "",
    },
    "gee:landsat": {
        "resource_id": "gee:landsat",
        "title": "Landsat (vía Earth Engine)",
        "type": "collection",
        "domains": ["observacion_tierra"],
        "primary_domain": "observacion_tierra",
        "keywords": [
            "landsat",
            "usgs",
            "nasa",
            "earth engine",
            "satelite",
        ],
        "description": (
            "Colecciones Landsat en Earth Engine (USGS/NASA), "
            "accesibles bajo cuenta autorizada."
        ),
        "spatial_coverage": "Global",
        "temporal_coverage": "Histórico Landsat",
        "formats": ["Earth Engine ImageCollection"],
        "homepage": "https://developers.google.com/earth-engine/datasets/catalog/landsat",
        "portal_url": "https://developers.google.com/earth-engine/datasets/catalog/landsat",
        "documentation_url": "https://developers.google.com/earth-engine/datasets",
        "endpoints": [
            {
                "method": "portal",
                "url": "https://developers.google.com/earth-engine/datasets/catalog/landsat",
                "label": "Landsat catalog (GEE)",
            }
        ],
        "access_methods": ["platform", "api"],
        "citation_reference": (
            "U.S. Geological Survey / NASA; accessed via Google Earth Engine. "
            "Landsat collections."
        ),
        "doi": "",
    },
    "gee:chirps": {
        "resource_id": "gee:chirps",
        "title": "CHIRPS precipitación (vía Earth Engine)",
        "type": "collection",
        "domains": ["clima", "hidrologia"],
        "primary_domain": "clima",
        "keywords": [
            "precipitacion",
            "series",
            "temporales",
            "sequia",
            "variabilidad",
            "climatica",
            "chirps",
            "gee",
            "clima",
        ],
        "description": (
            "Colección CHIRPS (Climate Hazards Group InfraRed Precipitation "
            "with Station data) en Google Earth Engine: precipitación "
            "cuasi-global para series temporales, sequía y variabilidad "
            "climática. DB2S-GEO no ejecuta código GEE ni descarga datos."
        ),
        "spatial_coverage": "Cuasi-global (latitudes tropicales / subtropicales)",
        "temporal_coverage": "1981–presente (según colección)",
        "formats": ["Earth Engine ImageCollection"],
        "homepage": (
            "https://developers.google.com/earth-engine/datasets/catalog/"
            "UCSB-CHG_CHIRPS_DAILY"
        ),
        "portal_url": (
            "https://developers.google.com/earth-engine/datasets/catalog/"
            "UCSB-CHG_CHIRPS_DAILY"
        ),
        "documentation_url": "https://www.chc.ucsb.edu/data/chirps",
        "endpoints": [
            {
                "method": "portal",
                "url": (
                    "https://developers.google.com/earth-engine/datasets/"
                    "catalog/UCSB-CHG_CHIRPS_DAILY"
                ),
                "label": "UCSB-CHG/CHIRPS/DAILY (GEE Catalog)",
            },
            {
                "method": "platform",
                "url": "https://code.earthengine.google.com",
                "label": "Earth Engine Code Editor",
            },
        ],
        "access_methods": ["platform", "api", "portal"],
        "citation_reference": (
            "Funk, C., et al. (2015). The climate hazards infrared "
            "precipitation with stations—a new environmental record for "
            "monitoring extremes. Scientific Data. Accessed via Google "
            "Earth Engine: UCSB-CHG/CHIRPS/DAILY."
        ),
        "doi": "10.1038/sdata.2015.66",
    },
    "gee:chirps-colombia": {
        "resource_id": "gee:chirps-colombia",
        "title": "CHIRPS precipitación para Colombia (vía Earth Engine)",
        "type": "collection",
        "domains": ["clima", "hidrologia"],
        "primary_domain": "clima",
        "keywords": [
            "precipitacion",
            "historica",
            "climatologia",
            "cuencas",
            "series",
            "temporales",
            "sequias",
            "chirps",
            "colombia",
            "gee",
        ],
        "description": (
            "Uso de la colección CHIRPS (UCSB-CHG/CHIRPS/DAILY) en Google "
            "Earth Engine acotada a Colombia: precipitación histórica, "
            "climatología, análisis de cuencas, series temporales y sequías. "
            "DB2S-GEO no ejecuta código GEE ni descarga datos; el recorte "
            "espacial a Colombia se realiza en la plataforma GEE."
        ),
        "spatial_coverage": "Colombia (vía filtro espacial en GEE)",
        "temporal_coverage": "1981–presente (según colección CHIRPS)",
        "formats": ["Earth Engine ImageCollection"],
        "homepage": (
            "https://developers.google.com/earth-engine/datasets/catalog/"
            "UCSB-CHG_CHIRPS_DAILY"
        ),
        "portal_url": (
            "https://developers.google.com/earth-engine/datasets/catalog/"
            "UCSB-CHG_CHIRPS_DAILY"
        ),
        "documentation_url": "https://www.chc.ucsb.edu/data/chirps",
        "endpoints": [
            {
                "method": "portal",
                "url": (
                    "https://developers.google.com/earth-engine/datasets/"
                    "catalog/UCSB-CHG_CHIRPS_DAILY"
                ),
                "label": "UCSB-CHG/CHIRPS/DAILY (GEE Catalog)",
            },
            {
                "method": "platform",
                "url": "https://code.earthengine.google.com",
                "label": "Earth Engine Code Editor (filtrar AOI Colombia)",
            },
        ],
        "access_methods": ["platform", "api", "portal"],
        "citation_reference": (
            "Funk, C., et al. (2015). CHIRPS — Climate Hazards Group. "
            "Scientific Data. Uso orientado a Colombia vía Google Earth "
            "Engine: UCSB-CHG/CHIRPS/DAILY."
        ),
                "doi": "10.1038/sdata.2015.66",
    },
    "gee:chirps-pentad": {
        "resource_id": "gee:chirps-pentad",
        "title": "CHIRPS Pentad (vía Earth Engine)",
        "type": "collection",
        "domains": ["clima", "hidrologia"],
        "primary_domain": "clima",
        "keywords": [
            "precipitacion",
            "pentad",
            "5-dias",
            "sequia",
            "ciclos",
            "estacionales",
            "chirps",
            "gee",
            "clima",
        ],
        "description": (
            "Colección CHIRPS Pentad (UCSB-CHG/CHIRPS/PENTAD) en Google "
            "Earth Engine: precipitación cuasi-global con resolución "
            "temporal de 5 días para monitoreo de sequía y ciclos "
            "estacionales. DB2S-GEO no ejecuta código GEE ni descarga datos."
        ),
        "spatial_coverage": "Cuasi-global (50°S–50°N)",
        "temporal_coverage": "1981–presente",
        "formats": ["Earth Engine ImageCollection"],
        "homepage": (
            "https://developers.google.com/earth-engine/datasets/catalog/"
            "UCSB-CHG_CHIRPS_PENTAD"
        ),
        "portal_url": (
            "https://developers.google.com/earth-engine/datasets/catalog/"
            "UCSB-CHG_CHIRPS_PENTAD"
        ),
        "documentation_url": "https://www.chc.ucsb.edu/data/chirps",
        "endpoints": [
            {
                "method": "portal",
                "url": (
                    "https://developers.google.com/earth-engine/datasets/"
                    "catalog/UCSB-CHG_CHIRPS_PENTAD"
                ),
                "label": "UCSB-CHG/CHIRPS/PENTAD (GEE Catalog)",
            },
            {
                "method": "platform",
                "url": "https://code.earthengine.google.com",
                "label": "Earth Engine Code Editor",
            },
        ],
        "access_methods": ["platform", "api", "portal"],
        "citation_reference": (
            "Funk, C., et al. (2015). CHIRPS Pentad. Climate Hazards Group. "
            "Accessed via Google Earth Engine: UCSB-CHG/CHIRPS/PENTAD."
        ),
        "doi": "10.1038/sdata.2015.66",
    },
    "gee:chirps-monthly": {
        "resource_id": "gee:chirps-monthly",
        "title": "CHIRPS Mensual (vía Earth Engine)",
        "type": "collection",
        "domains": ["clima", "hidrologia"],
        "primary_domain": "clima",
        "keywords": [
            "precipitacion",
            "mensual",
            "climatologia",
            "balance",
            "hidrico",
            "sequia",
            "tendencias",
            "chirps",
            "gee",
            "clima",
        ],
        "description": (
            "Colección CHIRPS Mensual (UCSB-CHG/CHIRPS/MONTHLY) en Google "
            "Earth Engine: precipitación mensual cuasi-global para "
            "climatología, balance hídrico, sequías y tendencias de largo "
            "plazo. DB2S-GEO no ejecuta código GEE ni descarga datos."
        ),
        "spatial_coverage": "Cuasi-global (50°S–50°N)",
        "temporal_coverage": "1981–presente",
        "formats": ["Earth Engine ImageCollection"],
        "homepage": (
            "https://developers.google.com/earth-engine/datasets/catalog/"
            "UCSB-CHG_CHIRPS_MONTHLY"
        ),
        "portal_url": (
            "https://developers.google.com/earth-engine/datasets/catalog/"
            "UCSB-CHG_CHIRPS_MONTHLY"
        ),
        "documentation_url": "https://www.chc.ucsb.edu/data/chirps",
        "endpoints": [
            {
                "method": "portal",
                "url": (
                    "https://developers.google.com/earth-engine/datasets/"
                    "catalog/UCSB-CHG_CHIRPS_MONTHLY"
                ),
                "label": "UCSB-CHG/CHIRPS/MONTHLY (GEE Catalog)",
            },
            {
                "method": "platform",
                "url": "https://code.earthengine.google.com",
                "label": "Earth Engine Code Editor",
            },
        ],
        "access_methods": ["platform", "api", "portal"],
        "citation_reference": (
            "Funk, C., et al. (2015). CHIRPS Monthly. Climate Hazards Group. "
            "Accessed via Google Earth Engine: UCSB-CHG/CHIRPS/MONTHLY."
        ),
        "doi": "10.1038/sdata.2015.66",
    },
}


class GeeConnector(BaseConnector):
    connector_id = SOURCE_ID
    source_name = "Google Earth Engine"
    version = "1.2.0"

    def identify(self) -> dict[str, Any]:
        return normalize_source(
            source_id=SOURCE_ID,
            country_or_scope="Global",
            domains=["observacion_tierra", "cobertura"],
            access_methods=["platform", "api", "portal"],
            description=(
                "Plataforma de análisis geoespacial a escala planetaria "
                "con catálogo de datasets satelitales y ambientales. "
                "DB2S-GEO no ejecuta scripts ni autentica cuentas GEE."
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
                "DB2S-GEO no ejecuta código Earth Engine ni descarga colecciones. "
                "El acceso operativo requiere cuenta GEE y cumplimiento de licencias."
            ),
            "read_only": True,
            "downloads_supported": False,
        }

    def cite(self, resource_id: str) -> dict[str, Any]:
        item = find_resource(_RESOURCES, resource_id)
        if not item:
            return resource_not_found(resource_id, SOURCE_ID)
        accessed = today_iso()
        doi = item.get("doi") or ""
        url = f"https://doi.org/{doi}" if doi else item["homepage"]
        apa = (
            f"Google Earth Engine. ({accessed[:4]}). {item['title']}. "
            f"{url}"
        )
        return {
            "source": "Google Earth Engine",
            "institution": INSTITUTION,
            "reference": item["citation_reference"],
            "url": url,
            "accessed": accessed,
            "apa": apa,
            "doi": doi,
            "license": LICENSE,
            "resource_id": item["resource_id"],
            "source_id": SOURCE_ID,
        }
