"""
Conector Dynamic World — enriquecimiento operativo DB2S-GEO.

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

SOURCE_ID = "dynamicworld"
INSTITUTION = "Google / World Resources Institute (Dynamic World)"
HOMEPAGE = "https://dynamicworld.app"
LICENSE = (
    "Según términos Dynamic World / Google Earth Engine y licencias "
    "del productor; verificar en catálogo oficial"
)

_RESOURCES: dict[str, dict[str, Any]] = {
    "dynamicworld:landcover": {
        "resource_id": "dynamicworld:landcover",
        "title": "Dynamic World — cobertura del suelo",
        "type": "collection",
        "domains": ["observacion_tierra"],
        "primary_domain": "observacion_tierra",
        "keywords": [
            "cobertura",
            "suelo",
            "landcover",
            "cambio",
            "uso",
            "monitoreo",
            "territorial",
            "clasificacion",
            "dinamica",
            "dynamicworld",
            "gee",
        ],
        "description": (
            "Producto Dynamic World de cobertura del suelo casi en tiempo "
            "real (10 clases), accesible vía Google Earth Engine "
            "(GOOGLE/DYNAMICWORLD/V1). Apoya monitoreo territorial, "
            "cambio de uso y clasificación dinámica. DB2S-GEO no ejecuta "
            "código GEE ni descarga colecciones."
        ),
        "spatial_coverage": "Global (cobertura Sentinel-2)",
        "temporal_coverage": "2015–presente (según disponibilidad)",
        "formats": ["Earth Engine ImageCollection"],
        "homepage": HOMEPAGE,
        "portal_url": (
            "https://developers.google.com/earth-engine/datasets/catalog/"
            "GOOGLE_DYNAMICWORLD_V1"
        ),
        "documentation_url": (
            "https://developers.google.com/earth-engine/datasets/catalog/"
            "GOOGLE_DYNAMICWORLD_V1"
        ),
        "endpoints": [
            {
                "method": "portal",
                "url": (
                    "https://developers.google.com/earth-engine/datasets/"
                    "catalog/GOOGLE_DYNAMICWORLD_V1"
                ),
                "label": "GOOGLE/DYNAMICWORLD/V1 (GEE Catalog)",
            },
            {
                "method": "portal",
                "url": HOMEPAGE,
                "label": "Dynamic World (sitio oficial)",
            },
            {
                "method": "platform",
                "url": "https://code.earthengine.google.com",
                "label": "Earth Engine Code Editor",
            },
        ],
        "access_methods": ["platform", "api", "portal"],
        "citation_reference": (
            "Brown, C. F., et al. (2022). Dynamic World, Near real-time "
            "global 10 m land use land cover mapping. Scientific Data. "
            "Accessed via Google Earth Engine: GOOGLE/DYNAMICWORLD/V1."
        ),
        "doi": "10.1038/s41597-022-01307-4",
    },
}


class DynamicworldConnector(BaseConnector):
    connector_id = SOURCE_ID
    source_name = "Dynamic World"
    version = "1.0.0"

    def identify(self) -> dict[str, Any]:
        return normalize_source(
            source_id=SOURCE_ID,
            source="Dynamic World",
            institution=INSTITUTION,
            country_or_scope="Global",
            domains=["observacion_tierra"],
            access_methods=["platform", "api", "portal"],
            description=(
                "Cobertura del suelo casi en tiempo real a 10 m "
                "(Dynamic World). Acceso operativo típico vía Earth Engine; "
                "DB2S-GEO no ejecuta scripts ni autentica cuentas."
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
                "DB2S-GEO no ejecuta código Earth Engine ni descarga "
                "colecciones Dynamic World. Requiere cuenta GEE y "
                "cumplimiento de licencias."
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
            f"Dynamic World. ({accessed[:4]}). {item['title']}. "
            f"{INSTITUTION}. {url}"
        )
        return {
            "source": "Dynamic World",
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
