"""
Conector UNOSAT — enriquecimiento operativo DB2S-GEO.

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

SOURCE_ID = "unosat"
INSTITUTION = "United Nations Satellite Centre (UNOSAT / UNITAR)"
HOMEPAGE = "https://www.unosat.org"
LICENSE = "Según términos UNOSAT / UNITAR de cada producto"

_RESOURCES: dict[str, dict[str, Any]] = {
    "unosat:disaster-mapping": {
        "resource_id": "unosat:disaster-mapping",
        "title": "UNOSAT — cartografía satelital de desastres",
        "type": "catalog",
                "domains": ["riesgo", "observacion_tierra"],
        "primary_domain": "riesgo",
        "keywords": [
            "desastre",
            "emergencia",
            "inundaciones",
            "movimientos",
            "masa",
            "monitoreo",
            "eventos",
            "extremos",
            "cartografia",
            "satelital",
            "unosat",
            "colombia",
        ],
        "description": (
            "Productos UNOSAT de mapeo satelital operacional para evaluación "
            "post-desastre, inundaciones, movimientos en masa y eventos "
            "extremos. Catálogo de activaciones y mapas en vivo. "
            "DB2S-GEO solo documenta el acceso; no descarga productos."
        ),
        "spatial_coverage": "Global (incluye activaciones sobre Colombia cuando existan)",
        "temporal_coverage": "Según activaciones operacionales UNOSAT",
        "formats": ["mapas PDF", "GIS data", "live web maps"],
        "homepage": HOMEPAGE,
        "portal_url": "https://www.unosat.org/products/",
        "documentation_url": "https://unosat.org/about-us/",
        "endpoints": [
            {
                "method": "portal",
                "url": "https://www.unosat.org/products/",
                "label": "Catálogo de productos UNOSAT",
            },
            {
                "method": "portal",
                "url": HOMEPAGE,
                "label": "Portal UNOSAT",
            },
        ],
        "access_methods": ["portal"],
        "citation_reference": (
            "UNITAR-UNOSAT. Operational satellite mapping products. "
            "United Nations Satellite Centre. "
            "https://www.unosat.org/products/"
        ),
        "doi": "",
    },
}


class UnosatConnector(BaseConnector):
    connector_id = SOURCE_ID
    source_name = "UNOSAT"
    version = "1.0.0"

    def identify(self) -> dict[str, Any]:
        return normalize_source(
            source_id=SOURCE_ID,
            source="UNOSAT",
            institution=INSTITUTION,
            country_or_scope="Global",
            domains=["riesgo", "observacion_tierra"],
            access_methods=["portal"],
            description=(
                "Centro satelital de las Naciones Unidas (UNITAR): análisis "
                "de imágenes para respuesta humanitaria y gestión del riesgo. "
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
                "DB2S-GEO no descarga productos UNOSAT. "
                "Consulte el catálogo oficial y cite el product ID."
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
            f"UNOSAT. ({accessed[:4]}). {item['title']}. "
            f"{INSTITUTION}. {url}"
        )
        return {
            "source": "UNOSAT",
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
