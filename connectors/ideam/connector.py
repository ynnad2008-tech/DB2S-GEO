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
}


class IdeamConnector(BaseConnector):
    connector_id = SOURCE_ID
    source_name = "IDEAM"
    version = "1.0.0"

    def identify(self) -> dict[str, Any]:
        return normalize_source(
            source_id=SOURCE_ID,
            source="IDEAM",
            institution=INSTITUTION,
            country_or_scope="Colombia",
            domains=["clima", "hidrologia"],
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
