"""
Conector INVEMAR — Fase 2 Metadata Engine MVP.

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

SOURCE_ID = "invemar"
INSTITUTION = "Instituto de Investigaciones Marinas y Costeras José Benito Vives de Andréis"
HOMEPAGE = "https://www.invemar.org.co"
LICENSE = "Términos institucionales INVEMAR / datos abiertos cuando apliquen"

_RESOURCES: dict[str, dict[str, Any]] = {
    "invemar:geovisor": {
        "resource_id": "invemar:geovisor",
        "title": "Geovisor INVEMAR",
        "type": "portal",
        "domains": ["oceanos_costas"],
        "primary_domain": "oceanos_costas",
        "keywords": [
            "oceanos",
            "costas",
            "marino",
            "geovisor",
            "invemar",
        ],
        "description": (
            "Geovisor y acceso cartográfico a información marina y costera "
            "producida o publicada por INVEMAR."
        ),
        "spatial_coverage": "Colombia (marino-costero)",
        "temporal_coverage": "Actualizaciones institucionales",
        "formats": ["servicios web", "mapas"],
        "homepage": HOMEPAGE,
        "portal_url": HOMEPAGE,
        "documentation_url": HOMEPAGE,
        "endpoints": [
            {
                "method": "portal",
                "url": HOMEPAGE,
                "label": "Portal institucional INVEMAR",
            }
        ],
        "access_methods": ["portal", "arcgis"],
        "citation_reference": (
            "INVEMAR. Geovisor e información marina y costera. "
            "Instituto de Investigaciones Marinas y Costeras."
        ),
        "doi": "",
    },
    "invemar:biodiversidad-marina": {
        "resource_id": "invemar:biodiversidad-marina",
        "title": "Biodiversidad marina y costera",
        "type": "dataset",
        "domains": ["oceanos_costas", "biodiversidad"],
        "primary_domain": "oceanos_costas",
        "keywords": [
            "biodiversidad",
            "marino",
            "costero",
            "especies",
            "invemar",
        ],
        "description": (
            "Información y productos sobre biodiversidad marina y costera "
            "bajo responsabilidad de INVEMAR."
        ),
        "spatial_coverage": "Colombia (marino-costero)",
        "temporal_coverage": "Series e inventarios institucionales",
        "formats": ["tablas", "mapas", "reportes"],
        "homepage": HOMEPAGE,
        "portal_url": HOMEPAGE,
        "documentation_url": HOMEPAGE,
        "endpoints": [
            {
                "method": "portal",
                "url": HOMEPAGE,
                "label": "Portal institucional INVEMAR",
            }
        ],
        "access_methods": ["portal"],
        "citation_reference": (
            "INVEMAR. Biodiversidad marina y costera. "
            "Instituto de Investigaciones Marinas y Costeras."
        ),
        "doi": "",
    },
    "invemar:ecosistemas-costeros": {
        "resource_id": "invemar:ecosistemas-costeros",
        "title": "Ecosistemas costeros",
        "type": "dataset",
        "domains": ["oceanos_costas"],
        "primary_domain": "oceanos_costas",
        "keywords": [
            "ecosistemas",
            "manglar",
            "costas",
            "habitat",
            "invemar",
        ],
        "description": (
            "Información sobre ecosistemas costeros (p. ej. manglares y "
            "hábitats asociados) documentada por INVEMAR."
        ),
        "spatial_coverage": "Colombia (zona costera)",
        "temporal_coverage": "Productos institucionales",
        "formats": ["mapas", "reportes"],
        "homepage": HOMEPAGE,
        "portal_url": HOMEPAGE,
        "documentation_url": HOMEPAGE,
        "endpoints": [
            {
                "method": "portal",
                "url": HOMEPAGE,
                "label": "Portal institucional INVEMAR",
            }
        ],
        "access_methods": ["portal"],
        "citation_reference": (
            "INVEMAR. Ecosistemas costeros. "
            "Instituto de Investigaciones Marinas y Costeras."
        ),
        "doi": "",
    },
}


class InvemarConnector(BaseConnector):
    connector_id = SOURCE_ID
    source_name = "INVEMAR"
    version = "1.0.0"

    def identify(self) -> dict[str, Any]:
        return normalize_source(
            source_id=SOURCE_ID,
            source="INVEMAR",
            institution=INSTITUTION,
            country_or_scope="Colombia",
            domains=["oceanos_costas", "biodiversidad"],
            access_methods=["portal", "arcgis"],
            description=(
                "Instituto de investigación marina y costera de Colombia. "
                "Fuente oficial de información oceanográfica, costera y "
                "de biodiversidad marina."
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
                "DB2S-GEO expone solo metadatos de acceso. "
                "Consulte el portal oficial INVEMAR para datos y productos."
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
            f"INVEMAR. ({accessed[:4]}). {item['title']}. "
            f"{INSTITUTION}. {url}"
        )
        return {
            "source": "INVEMAR",
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
