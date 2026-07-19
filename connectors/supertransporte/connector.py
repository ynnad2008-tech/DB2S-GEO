"""
Conector Supertransporte — enriquecimiento operativo DB2S-GEO.

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

SOURCE_ID = "supertransporte"
INSTITUTION = "Superintendencia de Transporte"
HOMEPAGE = "https://www.supertransporte.gov.co"
LICENSE = "Según términos Supertransporte / SuperTransporte Digital"

_RESOURCES: dict[str, dict[str, Any]] = {
    "supertransporte:visor-maritimo-fluvial": {
        "resource_id": "supertransporte:visor-maritimo-fluvial",
        "title": "Visor geográfico marítimo y fluvial (Supertransporte)",
        "type": "catalog",
        "domains": ["oceanos_costas", "hidrologia"],
        "primary_domain": "oceanos_costas",
        "keywords": [
            "visor",
            "maritimo",
            "fluvial",
            "infraestructura",
            "portuaria",
            "muelles",
            "embarcaderos",
            "concesiones",
            "logistica",
            "puertos",
            "geovisor",
            "supertransporte",
            "colombia",
        ],
        "description": (
            "Visor geográfico de la Superintendencia de Transporte / "
            "Delegatura de Puertos: infraestructura marítima y fluvial "
            "concesionada y no concesionada (muelles, embarcaderos e "
            "instalaciones portuarias). Complementa ANIscopio con el "
            "enfoque de vigilancia. DB2S-GEO solo documenta el acceso."
        ),
        "spatial_coverage": "Colombia (infraestructura portuaria marítima/fluvial)",
        "temporal_coverage": "Según capas publicadas en el visor",
        "formats": ["geovisor", "ArcGIS", "portal"],
        "homepage": HOMEPAGE,
        "portal_url": (
            "https://www.supertransporte.gov.co/index.php/"
            "superintendencia-delegada-de-puertos/"
            "visor-del-mapa-de-infraestructura-no-concesionada/"
        ),
        "documentation_url": (
            "https://transformaciondigital.supertransporte.gov.co/"
            "index.php/aplicaciones/"
        ),
        "endpoints": [
            {
                "method": "portal",
                "url": (
                    "https://www.supertransporte.gov.co/index.php/"
                    "superintendencia-delegada-de-puertos/"
                    "visor-del-mapa-de-infraestructura-no-concesionada/"
                ),
                "label": "Visor infraestructura no concesionada / marítimo-fluvial",
            },
            {
                "method": "portal",
                "url": (
                    "https://transformaciondigital.supertransporte.gov.co/"
                    "index.php/aplicaciones/"
                ),
                "label": "Aplicaciones SuperTransporte Digital",
            },
            {
                "method": "portal",
                "url": HOMEPAGE,
                "label": "Portal institucional Supertransporte",
            },
        ],
        "access_methods": ["portal"],
        "citation_reference": (
            "Superintendencia de Transporte. Visor geográfico de "
            "infraestructura marítima y fluvial (concesionada y no "
            "concesionada). "
            "https://www.supertransporte.gov.co/index.php/"
            "superintendencia-delegada-de-puertos/"
            "visor-del-mapa-de-infraestructura-no-concesionada/"
        ),
        "doi": "",
    },
    "supertransporte:observatorio-vigilancia": {
        "resource_id": "supertransporte:observatorio-vigilancia",
        "title": "Observatorio de vigilancia, inspección y control",
        "type": "catalog",
        "domains": ["oceanos_costas", "observacion_tierra"],
        "primary_domain": "oceanos_costas",
        "keywords": [
            "observatorio",
            "vigilancia",
            "inspeccion",
            "control",
            "transporte",
            "indicadores",
            "sectoriales",
            "trafico",
            "portuario",
            "boletines",
            "datos",
            "abiertos",
            "supertransporte",
            "colombia",
        ],
        "description": (
            "Observatorio de vigilancia, inspección y control de la "
            "Superintendencia de Transporte: plataforma integral con "
            "visor geográfico, tableros, boletines, tráfico portuario e "
            "indicadores sectoriales, más datos abiertos. "
            "DB2S-GEO solo documenta el acceso; no descarga datasets."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Según publicaciones y tableros del Observatorio",
        "formats": ["geovisor", "tableros", "boletines", "datos abiertos"],
        "homepage": HOMEPAGE,
        "portal_url": (
            "https://transformaciondigital.supertransporte.gov.co/"
            "index.php/observatorio/"
        ),
        "documentation_url": (
            "https://transformaciondigital.supertransporte.gov.co/"
            "index.php/observatorio/"
        ),
        "endpoints": [
            {
                "method": "portal",
                "url": (
                    "https://transformaciondigital.supertransporte.gov.co/"
                    "index.php/observatorio/"
                ),
                "label": "Observatorio SuperTransporte Digital",
            },
            {
                "method": "portal",
                "url": (
                    "https://transformaciondigital.supertransporte.gov.co/"
                    "index.php/aplicaciones/"
                ),
                "label": "Catálogo de aplicaciones digitales",
            },
            {
                "method": "portal",
                "url": "https://www.supertransporte.gov.co/index.php/vigia/",
                "label": "VIGIA — sistema misional de vigilancia",
            },
        ],
        "access_methods": ["portal"],
        "citation_reference": (
            "Superintendencia de Transporte. Observatorio de vigilancia, "
            "inspección y control. "
            "https://transformaciondigital.supertransporte.gov.co/"
            "index.php/observatorio/"
        ),
        "doi": "",
    },
}


class SupertransporteConnector(BaseConnector):
    connector_id = SOURCE_ID
    source_name = "Supertransporte"
    version = "1.0.0"

    def identify(self) -> dict[str, Any]:
        return normalize_source(
            source_id=SOURCE_ID,
            source="Supertransporte",
            institution=INSTITUTION,
            country_or_scope="Colombia",
            domains=["oceanos_costas", "hidrologia", "observacion_tierra"],
            access_methods=["portal"],
            description=(
                "Superintendencia de Transporte: visor marítimo-fluvial y "
                "Observatorio de vigilancia, inspección y control. "
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
                "DB2S-GEO no descarga datos de Supertransporte. "
                "Consulte el Observatorio / visores oficiales y cite la fuente."
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
            f"Supertransporte. ({accessed[:4]}). {item['title']}. "
            f"{INSTITUTION}. {url}"
        )
        return {
            "source": "Supertransporte",
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
