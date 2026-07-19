"""
Conector FAO / FAOSTAT — Fase 1 Discovery MVP.

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

SOURCE_ID = "fao"
INSTITUTION = "Food and Agriculture Organization of the United Nations (FAO)"
HOMEPAGE = "https://www.fao.org/faostat"
LICENSE = "Términos de uso FAO / FAOSTAT (datos estadísticos abiertos con atribución)"

_RESOURCES: dict[str, dict[str, Any]] = {
    "fao:faostat-production": {
        "resource_id": "fao:faostat-production",
        "title": "FAOSTAT — Production",
        "type": "dataset",
        "domains": ["agricultura", "socioeconomico"],
        "primary_domain": "agricultura",
        "keywords": [
            "produccion",
            "agricultura",
            "pecuaria",
            "faostat",
        ],
        "description": (
            "Estadísticas de producción agrícola y pecuaria a nivel de país "
            "en FAOSTAT."
        ),
        "spatial_coverage": "Global (países)",
        "temporal_coverage": "Series anuales históricas",
        "formats": ["CSV", "API JSON"],
        "homepage": HOMEPAGE,
        "portal_url": "https://www.fao.org/faostat/en/#data",
        "documentation_url": "https://www.fao.org/faostat/en/#data",
        "endpoints": [
            {
                "method": "portal",
                "url": "https://www.fao.org/faostat/en/#data",
                "label": "FAOSTAT data portal",
            },
            {
                "method": "api",
                "url": "https://fenixservices.fao.org/faostat/api/",
                "label": "FAOSTAT API (documentación oficial)",
            },
        ],
        "access_methods": ["api", "portal"],
        "citation_reference": (
            "FAO. FAOSTAT — Production. "
            "Food and Agriculture Organization of the United Nations."
        ),
        "doi": "",
    },
    "fao:faostat-land": {
        "resource_id": "fao:faostat-land",
        "title": "FAOSTAT — Land Use / Land Cover indicators",
        "type": "dataset",
        "domains": ["agricultura", "cobertura"],
        "primary_domain": "agricultura",
        "keywords": [
            "uso de la tierra",
            "cobertura",
            "land use",
            "agricultura",
            "faostat",
        ],
        "description": (
            "Indicadores de uso de la tierra y coberturas relacionados "
            "con agricultura en FAOSTAT."
        ),
        "spatial_coverage": "Global (países)",
        "temporal_coverage": "Series anuales",
        "formats": ["CSV", "API JSON"],
        "homepage": HOMEPAGE,
        "portal_url": "https://www.fao.org/faostat/en/#data",
        "documentation_url": "https://www.fao.org/faostat/en/#data",
        "endpoints": [
            {
                "method": "portal",
                "url": "https://www.fao.org/faostat/en/#data",
                "label": "FAOSTAT data portal",
            }
        ],
        "access_methods": ["api", "portal"],
        "citation_reference": (
            "FAO. FAOSTAT — Land. "
            "Food and Agriculture Organization of the United Nations."
        ),
        "doi": "",
    },
    "fao:faostat-emissions": {
        "resource_id": "fao:faostat-emissions",
        "title": "FAOSTAT — Emissions / Climate related agriculture",
        "type": "dataset",
        "domains": ["agricultura", "clima"],
        "primary_domain": "agricultura",
        "keywords": [
            "emisiones",
            "clima",
            "agricultura",
            "agropecuario",
            "faostat",
        ],
        "description": (
            "Estadísticas de emisiones y variables climáticas asociadas "
            "al sector agropecuario en FAOSTAT."
        ),
        "spatial_coverage": "Global (países)",
        "temporal_coverage": "Series anuales",
        "formats": ["CSV", "API JSON"],
        "homepage": HOMEPAGE,
        "portal_url": "https://www.fao.org/faostat/en/#data",
        "documentation_url": "https://www.fao.org/faostat/en/#data",
        "endpoints": [
            {
                "method": "portal",
                "url": "https://www.fao.org/faostat/en/#data",
                "label": "FAOSTAT data portal",
            }
        ],
        "access_methods": ["api", "portal"],
        "citation_reference": (
            "FAO. FAOSTAT — Emissions. "
            "Food and Agriculture Organization of the United Nations."
        ),
        "doi": "",
    },
}


class FaoConnector(BaseConnector):
    connector_id = SOURCE_ID
    source_name = "FAOSTAT"
    version = "1.0.0"

    def identify(self) -> dict[str, Any]:
        return normalize_source(
            source_id=SOURCE_ID,
            source="FAOSTAT",
            institution=INSTITUTION,
            country_or_scope="Global",
            domains=["agricultura", "socioeconomico"],
            access_methods=["api", "portal"],
            description=(
                "Base estadística de la FAO sobre agricultura, alimentación, "
                "uso de la tierra y variables socioeconómicas relacionadas."
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
                "DB2S-GEO describe rutas de acceso a FAOSTAT. "
                "No realiza descargas masivas ni consultas bulk."
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
            f"FAO. ({accessed[:4]}). {item['title']}. "
            f"FAOSTAT. {url}"
        )
        return {
            "source": "FAOSTAT",
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
