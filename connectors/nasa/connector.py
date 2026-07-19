"""
Conector NASA — enriquecimiento operativo DB2S-GEO.

Metadatos curados humanamente. Read-only. Sin descarga ni ejecución remota.
No autentica Earthdata ni ejecuta GEE.
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

SOURCE_ID = "nasa"
INSTITUTION = "National Aeronautics and Space Administration (NASA)"
HOMEPAGE = "https://www.nasa.gov"
LICENSE = (
    "Datos NASA Earth Science / GPM según términos Earthdata y productor; "
    "verificar DOI y licencia del producto"
)

_RESOURCES: dict[str, dict[str, Any]] = {
    "nasa:imerg-colombia": {
        "resource_id": "nasa:imerg-colombia",
        "title": "GPM IMERG precipitación para Colombia (NASA)",
        "type": "collection",
        "domains": ["clima", "hidrologia"],
        "primary_domain": "clima",
        "keywords": [
            "precipitacion",
            "satelital",
            "meteorologia",
            "clima",
            "lluvia",
            "monitoreo",
            "multitemporal",
            "imerg",
            "gpm",
            "nasa",
            "colombia",
        ],
        "description": (
            "Producto GPM IMERG (Integrated Multi-satellitE Retrievals for "
            "GPM) de NASA para precipitación satelital, documentado para uso "
            "en Colombia vía Earth Engine (NASA/GPM_L3/IMERG_V07) y portales "
            "GPM/Giovanni. Apoya meteorología, clima y monitoreo "
            "multitemporal. DB2S-GEO no descarga ni autentica Earthdata."
        ),
        "spatial_coverage": "Colombia (vía filtro espacial / región en portales)",
        "temporal_coverage": "2000–presente (según producto IMERG)",
        "formats": ["Earth Engine ImageCollection", "NetCDF (GES DISC)"],
        "homepage": "https://gpm.nasa.gov/data",
        "portal_url": (
            "https://developers.google.com/earth-engine/datasets/catalog/"
            "NASA_GPM_L3_IMERG_V07"
        ),
        "documentation_url": "https://gpm.nasa.gov/data",
        "endpoints": [
            {
                "method": "portal",
                "url": (
                    "https://developers.google.com/earth-engine/datasets/"
                    "catalog/NASA_GPM_L3_IMERG_V07"
                ),
                "label": "NASA/GPM_L3/IMERG_V07 (GEE Catalog)",
            },
            {
                "method": "portal",
                "url": "https://giovanni.gsfc.nasa.gov/",
                "label": "NASA Giovanni (análisis / región)",
            },
            {
                "method": "portal",
                "url": "https://gpm.nasa.gov/data",
                "label": "GPM Data (NASA)",
            },
        ],
        "access_methods": ["portal", "platform", "api"],
        "citation_reference": (
            "Huffman, G. J., et al. GPM IMERG Final Precipitation L3. "
            "NASA GES DISC. DOI: 10.5067/GPM/IMERG/3B-HH/07. "
            "Accessed via Google Earth Engine: NASA/GPM_L3/IMERG_V07."
        ),
        "doi": "10.5067/GPM/IMERG/3B-HH/07",
    },
    "nasa:grace-groundwater-colombia": {
        "resource_id": "nasa:grace-groundwater-colombia",
        "title": "GRACE — almacenamiento de agua subterránea (Colombia)",
        "type": "collection",
        "domains": ["hidrologia", "observacion_tierra"],
        "primary_domain": "hidrologia",
        "keywords": [
            "agua",
            "subterranea",
            "almacenamiento",
            "hidrico",
            "grace",
            "acuiferos",
            "hidrologia",
            "satelital",
            "nasa",
            "colombia",
        ],
        "description": (
            "Monitoreo de cambios de almacenamiento de agua subterránea "
            "con datos GRACE/GRACE-FO (NASA), orientado a Colombia vía "
            "subsetting regional (GGST) y productos GRACE. Apoya hidrología "
            "satelital y análisis de acuíferos. DB2S-GEO no autentica ni "
            "descarga productos."
        ),
        "spatial_coverage": "Colombia (vía región / shapefile en GGST u AOI)",
        "temporal_coverage": "2002–presente (GRACE / GRACE-FO, según producto)",
        "formats": ["series temporales", "NetCDF", "mapas"],
        "homepage": "https://grace.jpl.nasa.gov/",
        "portal_url": "https://ggst.readthedocs.io/",
        "documentation_url": "https://ggst.readthedocs.io/en/latest/overview/",
        "endpoints": [
            {
                "method": "portal",
                "url": "https://ggst.readthedocs.io/",
                "label": "GRACE Groundwater Subsetting Tool (docs)",
            },
            {
                "method": "portal",
                "url": "https://grace.jpl.nasa.gov/",
                "label": "NASA JPL GRACE",
            },
            {
                "method": "portal",
                "url": (
                    "https://developers.google.com/earth-engine/datasets/"
                    "catalog/NASA_GRACE_MASS_GRIDS_MASCON_CRI"
                ),
                "label": "GRACE Mascons (GEE Catalog)",
            },
        ],
        "access_methods": ["portal", "platform", "api"],
        "citation_reference": (
            "NASA Jet Propulsion Laboratory. GRACE / GRACE-FO mission data. "
            "Groundwater analysis vía GRACE Groundwater Subsetting Tool (GGST). "
            "https://grace.jpl.nasa.gov/"
        ),
        "doi": "",
    },
}


class NasaConnector(BaseConnector):
    connector_id = SOURCE_ID
    source_name = "NASA"
    version = "1.1.0"

    def identify(self) -> dict[str, Any]:
        return normalize_source(
            source_id=SOURCE_ID,
            source="NASA",
            institution=INSTITUTION,
            country_or_scope="Global",
            domains=["clima", "observacion_tierra", "hidrologia"],
            access_methods=["portal", "platform", "api"],
            description=(
                "Agencia espacial de EE. UU. Productos de observación de la "
                "Tierra, precipitación (GPM/IMERG) y almacenamiento hídrico "
                "(GRACE). DB2S-GEO solo documenta acceso; no autentica ni descarga."
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
                "DB2S-GEO no descarga productos NASA ni autentica Earthdata. "
                "Use GEE, Giovanni o GES DISC oficiales y cite el DOI."
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
            f"NASA. ({accessed[:4]}). {item['title']}. "
            f"{INSTITUTION}. {url}"
        )
        return {
            "source": "NASA",
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
