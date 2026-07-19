"""
Conector GBIF — Fase 1 Discovery MVP.

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

SOURCE_ID = "gbif"
INSTITUTION = "Global Biodiversity Information Facility"
HOMEPAGE = "https://www.gbif.org"
API_BASE = "https://api.gbif.org/v1"
LICENSE = "Según dataset (frecuente CC0 / CC BY); ver licencia del recurso en GBIF"

_RESOURCES: dict[str, dict[str, Any]] = {
    "gbif:occurrence": {
        "resource_id": "gbif:occurrence",
        "title": "GBIF Occurrence API",
        "type": "api",
        "domains": ["biodiversidad"],
        "primary_domain": "biodiversidad",
        "keywords": [
            "ocurrencias",
            "biodiversidad",
            "especimenes",
            "observaciones",
            "gbif",
        ],
        "description": (
            "API de ocurrencias de biodiversidad (especímenes y observaciones) "
            "publicadas a través de la red GBIF."
        ),
        "spatial_coverage": "Global",
        "temporal_coverage": "Histórico a presente",
        "formats": ["JSON", "DwC-A"],
        "homepage": HOMEPAGE,
        "portal_url": "https://www.gbif.org",
        "documentation_url": "https://www.gbif.org/developer/summary",
        "endpoints": [
            {
                "method": "api",
                "url": f"{API_BASE}/occurrence/search",
                "label": "Occurrence search",
            },
            {
                "method": "portal",
                "url": HOMEPAGE,
                "label": "Portal GBIF",
            },
        ],
        "access_methods": ["api", "portal"],
        "citation_reference": (
            "GBIF.org. GBIF Occurrence data. "
            "Global Biodiversity Information Facility."
        ),
        "doi": "10.15468/dl.gbif",
    },
    "gbif:species": {
        "resource_id": "gbif:species",
        "title": "GBIF Species / Backbone Taxonomy",
        "type": "api",
        "domains": ["biodiversidad"],
        "primary_domain": "biodiversidad",
        "keywords": [
            "especies",
            "taxonomia",
            "backbone",
            "gbif",
        ],
        "description": (
            "Servicios de taxonomía y especies (Backbone Taxonomy) de GBIF."
        ),
        "spatial_coverage": "Global",
        "temporal_coverage": "Actualizaciones continuas",
        "formats": ["JSON"],
        "homepage": HOMEPAGE,
        "portal_url": HOMEPAGE,
        "documentation_url": "https://www.gbif.org/developer/species",
        "endpoints": [
            {
                "method": "api",
                "url": f"{API_BASE}/species",
                "label": "Species API",
            }
        ],
        "access_methods": ["api", "portal"],
        "citation_reference": (
            "GBIF Secretariat. GBIF Backbone Taxonomy. "
            "Global Biodiversity Information Facility."
        ),
        "doi": "10.15468/39omei",
    },
    "gbif:datasets": {
        "resource_id": "gbif:datasets",
        "title": "GBIF Dataset Registry",
        "type": "catalog",
        "domains": ["biodiversidad"],
        "primary_domain": "biodiversidad",
        "keywords": [
            "datasets",
            "registro",
            "metadatos",
            "doi",
            "gbif",
        ],
        "description": (
            "Registro de datasets publicados en GBIF, con metadatos y DOI "
            "por conjunto de datos."
        ),
        "spatial_coverage": "Global",
        "temporal_coverage": "Actualizaciones continuas",
        "formats": ["JSON"],
        "homepage": HOMEPAGE,
        "portal_url": "https://www.gbif.org/dataset/search",
        "documentation_url": "https://www.gbif.org/developer/registry",
        "endpoints": [
            {
                "method": "api",
                "url": f"{API_BASE}/dataset",
                "label": "Dataset registry API",
            }
        ],
        "access_methods": ["api", "portal"],
        "citation_reference": (
            "GBIF.org. Dataset registry. "
            "Global Biodiversity Information Facility."
        ),
        "doi": "",
    },
    "gbif:occurrence-colombia": {
        "resource_id": "gbif:occurrence-colombia",
        "title": "Ocurrencias de biodiversidad en Colombia (GBIF)",
        "type": "api",
        "domains": ["biodiversidad"],
        "primary_domain": "biodiversidad",
        "keywords": [
            "biodiversidad",
            "especies",
            "ocurrencias",
            "registros",
            "biologicos",
            "conservacion",
            "colombia",
            "gbif",
        ],
        "description": (
            "Acceso a ocurrencias y registros biológicos de biodiversidad "
            "en Colombia publicados en GBIF (filtro country=CO). "
            "Apoya conservación, inventarios de especies y análisis de "
            "distribución. DB2S-GEO solo documenta el endpoint; "
            "no descarga ocurrencias."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Histórico a presente (según datasets publicados)",
        "formats": ["JSON", "DwC-A"],
        "homepage": "https://www.gbif.org/occurrence/search?country=CO",
        "portal_url": "https://www.gbif.org/occurrence/search?country=CO",
        "documentation_url": "https://techdocs.gbif.org/en/openapi/v1/occurrence",
        "endpoints": [
            {
                "method": "api",
                "url": f"{API_BASE}/occurrence/search?country=CO",
                "label": "Occurrence search (Colombia)",
            },
            {
                "method": "portal",
                "url": "https://www.gbif.org/occurrence/search?country=CO",
                "label": "Portal GBIF ocurrencias Colombia",
            },
        ],
        "access_methods": ["api", "portal"],
        "citation_reference": (
            "GBIF.org. Occurrence search — Colombia (country=CO). "
            "Global Biodiversity Information Facility. "
            "https://api.gbif.org/v1/occurrence/search?country=CO"
        ),
        "doi": "10.15468/dl.gbif",
    },
    "gbif:species-colombia": {
        "resource_id": "gbif:species-colombia",
        "title": "Especies y taxonomía en Colombia (GBIF)",
        "type": "api",
        "domains": ["biodiversidad"],
        "primary_domain": "biodiversidad",
        "keywords": [
            "biodiversidad",
            "taxonomia",
            "especies",
            "conservacion",
            "observaciones",
            "biologicas",
            "colombia",
            "gbif",
        ],
        "description": (
            "Acceso a información de especies y taxonomía asociada a "
            "biodiversidad en Colombia a través de GBIF (portal país CO "
            "y Species API). Apoya conservación, inventarios y "
            "observaciones biológicas. DB2S-GEO solo documenta el endpoint; "
            "no descarga datos."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Actualizaciones continuas (según publicación GBIF)",
        "formats": ["JSON"],
        "homepage": "https://www.gbif.org/country/CO/search",
        "portal_url": "https://www.gbif.org/country/CO/search",
        "documentation_url": "https://www.gbif.org/developer/species",
        "endpoints": [
            {
                "method": "api",
                "url": f"{API_BASE}/species/search",
                "label": "Species search API",
            },
            {
                "method": "portal",
                "url": "https://www.gbif.org/country/CO/search",
                "label": "Portal GBIF especies Colombia",
            },
        ],
        "access_methods": ["api", "portal"],
        "citation_reference": (
            "GBIF.org. Species / taxonomy — Colombia. "
            "Global Biodiversity Information Facility. "
            "https://www.gbif.org/country/CO/search"
        ),
        "doi": "10.15468/39omei",
    },
}


class GbifConnector(BaseConnector):
    connector_id = SOURCE_ID
    source_name = "GBIF"
    version = "1.2.0"

    def identify(self) -> dict[str, Any]:
        return normalize_source(
            source_id=SOURCE_ID,
            source="GBIF",
            institution=INSTITUTION,
            country_or_scope="Global",
            domains=["biodiversidad"],
            access_methods=["api", "portal"],
            description=(
                "Infraestructura global de datos de biodiversidad. "
                "Agrega ocurrencias, taxonomía y datasets con DOI."
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
                "DB2S-GEO no descarga ocurrencias. Use la API o portal GBIF "
                "oficial y cite el DOI del dataset cuando exista."
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
            f"GBIF.org. ({accessed[:4]}). {item['title']}. "
            f"{INSTITUTION}. {url}"
        )
        return {
            "source": "GBIF",
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
