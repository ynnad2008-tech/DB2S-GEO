"""
Conector WorldPop — Fase 1 Discovery MVP.

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

SOURCE_ID = "worldpop"
INSTITUTION = "WorldPop (University of Southampton / WorldPop Project)"
HOMEPAGE = "https://www.worldpop.org"
LICENSE = "CC BY 4.0 (verificar producto específico en WorldPop)"

_RESOURCES: dict[str, dict[str, Any]] = {
    "worldpop:population-density": {
        "resource_id": "worldpop:population-density",
        "title": "WorldPop Population Density",
        "type": "dataset",
        "domains": ["poblacion"],
        "primary_domain": "poblacion",
        "keywords": [
            "densidad poblacional",
            "poblacion",
            "raster",
            "worldpop",
        ],
        "description": (
            "Rasters de densidad poblacional a alta resolución espacial "
            "producidos por WorldPop."
        ),
        "spatial_coverage": "Global / por país",
        "temporal_coverage": "Años de referencia según producto",
        "formats": ["GeoTIFF", "metadata"],
        "homepage": HOMEPAGE,
        "portal_url": "https://hub.worldpop.org",
        "documentation_url": "https://www.worldpop.org/methods/",
        "endpoints": [
            {
                "method": "portal",
                "url": "https://hub.worldpop.org",
                "label": "WorldPop Data Hub",
            },
            {
                "method": "api",
                "url": "https://www.worldpop.org/rest/data",
                "label": "WorldPop REST (metadatos / listados)",
            },
        ],
        "access_methods": ["api", "portal"],
        "citation_reference": (
            "WorldPop. Open Spatial Demographic Data and Research. "
            "University of Southampton."
        ),
        "doi": "10.5258/SOTON/WP00647",
    },
    "worldpop:population-counts": {
        "resource_id": "worldpop:population-counts",
        "title": "WorldPop Population Counts",
        "type": "dataset",
        "domains": ["poblacion"],
        "primary_domain": "poblacion",
        "keywords": [
            "conteo poblacional",
            "poblacion",
            "grilla",
            "worldpop",
        ],
        "description": (
            "Estimaciones de conteo poblacional en grilla, desagregadas "
            "espacialmente."
        ),
        "spatial_coverage": "Global / por país",
        "temporal_coverage": "Años de referencia según producto",
        "formats": ["GeoTIFF"],
        "homepage": HOMEPAGE,
        "portal_url": "https://hub.worldpop.org",
        "documentation_url": "https://www.worldpop.org/methods/",
        "endpoints": [
            {
                "method": "portal",
                "url": "https://hub.worldpop.org",
                "label": "WorldPop Data Hub",
            }
        ],
        "access_methods": ["api", "portal"],
        "citation_reference": (
            "WorldPop. Population counts datasets. "
            "University of Southampton."
        ),
        "doi": "",
    },
    "worldpop:age-sex": {
        "resource_id": "worldpop:age-sex",
        "title": "WorldPop Age and Sex Structures",
        "type": "dataset",
        "domains": ["poblacion", "socioeconomico"],
        "primary_domain": "poblacion",
        "keywords": [
            "edad",
            "sexo",
            "estructura poblacional",
            "poblacion",
            "worldpop",
        ],
        "description": (
            "Estructuras de edad y sexo desagregadas espacialmente "
            "(productos WorldPop)."
        ),
        "spatial_coverage": "Global / por país",
        "temporal_coverage": "Años de referencia según producto",
        "formats": ["GeoTIFF"],
        "homepage": HOMEPAGE,
        "portal_url": "https://hub.worldpop.org",
        "documentation_url": "https://www.worldpop.org/methods/",
        "endpoints": [
            {
                "method": "portal",
                "url": "https://hub.worldpop.org",
                "label": "WorldPop Data Hub",
            }
        ],
        "access_methods": ["api", "portal"],
        "citation_reference": (
            "WorldPop. Age and sex structures. "
            "University of Southampton."
        ),
        "doi": "",
    },
    "worldpop:colombia": {
        "resource_id": "worldpop:colombia",
        "title": "Población de Colombia (WorldPop)",
        "type": "dataset",
        "domains": ["poblacion"],
        "primary_domain": "poblacion",
        "keywords": [
            "poblacion",
            "colombia",
            "exposicion",
            "riesgo",
            "planeacion",
            "territorial",
            "densidad",
            "worldpop",
        ],
        "description": (
            "Productos demográficos espaciales de WorldPop filtrados a "
            "Colombia (ISO3=COL): densidad y conteos poblacionales de "
            "alta resolución. Apoya exposición, riesgo y planeación "
            "territorial. DB2S-GEO solo documenta el endpoint; "
            "no descarga rasters."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Años de referencia según producto WorldPop",
        "formats": ["GeoTIFF", "JSON (metadatos REST)"],
        "homepage": "https://hub.worldpop.org",
        "portal_url": "https://hub.worldpop.org",
        "documentation_url": "https://www.worldpop.org/methods/",
        "endpoints": [
            {
                "method": "api",
                "url": "https://www.worldpop.org/rest/data/pop/wpgp?iso3=COL",
                "label": "WorldPop REST población Colombia (iso3=COL)",
            },
            {
                "method": "portal",
                "url": "https://hub.worldpop.org",
                "label": "WorldPop Data Hub",
            },
        ],
        "access_methods": ["api", "portal"],
        "citation_reference": (
            "WorldPop. Population datasets — Colombia (ISO3=COL). "
            "University of Southampton. "
            "https://www.worldpop.org/rest/data/pop/wpgp?iso3=COL"
        ),
        "doi": "10.5258/SOTON/WP00647",
    },
}


class WorldpopConnector(BaseConnector):
    connector_id = SOURCE_ID
    source_name = "WorldPop"
    version = "1.1.0"

    def identify(self) -> dict[str, Any]:
        return normalize_source(
            source_id=SOURCE_ID,
            source="WorldPop",
            institution=INSTITUTION,
            country_or_scope="Global",
            domains=["poblacion", "socioeconomico"],
            access_methods=["api", "portal"],
            description=(
                "Proyecto de demografía espacial de alta resolución: "
                "densidad, conteos y estructuras poblacionales."
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
                "DB2S-GEO no descarga rasters WorldPop. "
                "Use el Data Hub oficial y cite DOI/licencia del producto."
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
            f"WorldPop. ({accessed[:4]}). {item['title']}. "
            f"University of Southampton. {url}"
        )
        return {
            "source": "WorldPop",
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
