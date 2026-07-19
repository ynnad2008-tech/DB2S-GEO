"""
Conector Superservicios — enriquecimiento operativo DB2S-GEO.

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

SOURCE_ID = "superservicios"
INSTITUTION = (
    "Superintendencia de Servicios Públicos Domiciliarios (Superservicios)"
)
HOMEPAGE = "https://www.superservicios.gov.co"
LICENSE = "Según términos Superservicios / SUI / geoportal"

_RESOURCES: dict[str, dict[str, Any]] = {
    "superservicios:cobertura-servicios-publicos": {
        "resource_id": "superservicios:cobertura-servicios-publicos",
        "title": "Cobertura de servicios públicos domiciliarios (SUI / Geoportal)",
        "type": "dataset",
        "domains": ["hidrologia", "observacion_tierra"],
        "primary_domain": "hidrologia",
        "keywords": [
            "servicios",
            "publicos",
            "cobertura",
            "territorial",
            "acueducto",
            "alcantarillado",
            "aseo",
            "energia",
            "prestadoras",
            "sui",
            "geoportal",
            "superservicios",
            "colombia",
        ],
        "description": (
            "Información espacial de cobertura de servicios públicos "
            "domiciliarios (acueducto, alcantarillado, aseo y relacionados) "
            "vía Geoportal Superservicios y el Sistema Único de Información "
            "(SUI). Incluye capas FeatureServer de cobertura por año/servicio. "
            "DB2S-GEO solo documenta el acceso; no descarga capas."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Según capas anuales publicadas en el geoportal",
        "formats": ["FeatureServer", "geovisor", "portal SUI"],
        "homepage": HOMEPAGE,
        "portal_url": "https://geoportal.superservicios.gov.co/",
        "documentation_url": "http://sui.superservicios.gov.co/Que-es-el-SUI",
        "endpoints": [
            {
                "method": "portal",
                "url": "https://geoportal.superservicios.gov.co/",
                "label": "Geoportal Superservicios",
            },
            {
                "method": "arcgis",
                "url": (
                    "https://geoportal.superservicios.gov.co/server/rest/"
                    "services/Hosted"
                ),
                "label": "REST Hosted — coberturas SSPD",
            },
            {
                "method": "portal",
                "url": "http://sui.superservicios.gov.co/",
                "label": "Sistema Único de Información (SUI)",
            },
        ],
        "access_methods": ["portal", "arcgis"],
        "citation_reference": (
            "Superintendencia de Servicios Públicos Domiciliarios. "
            "Cobertura de servicios públicos — Geoportal / SUI. "
            "https://geoportal.superservicios.gov.co/"
        ),
        "doi": "",
    },
    "superservicios:captacion-servicios-publicos": {
        "resource_id": "superservicios:captacion-servicios-publicos",
        "title": "Captación e infraestructura hídrica de acueducto (Superservicios)",
        "type": "dataset",
        "domains": ["hidrologia", "observacion_tierra"],
        "primary_domain": "hidrologia",
        "keywords": [
            "captacion",
            "agua",
            "acueducto",
            "infraestructura",
            "hidrica",
            "abastecimiento",
            "prestadores",
            "tratamiento",
            "conduccion",
            "servicios",
            "publicos",
            "sui",
            "superservicios",
            "colombia",
        ],
        "description": (
            "Recursos geográficos del Geoportal Superservicios asociados a "
            "la cadena de acueducto (actividad complementaria de captación, "
            "abastecimiento e infraestructura hídrica de prestadores), "
            "incluyendo capas Hosted de acueducto urbano/rural y SUI. "
            "DB2S-GEO solo documenta el acceso; no descarga capas."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Según capas anuales publicadas en el geoportal",
        "formats": ["FeatureServer", "VectorTile", "geovisor", "portal SUI"],
        "homepage": HOMEPAGE,
        "portal_url": "https://geoportal.superservicios.gov.co/",
        "documentation_url": "http://sui.superservicios.gov.co/Que-es-el-SUI",
        "endpoints": [
            {
                "method": "arcgis",
                "url": (
                    "https://geoportal.superservicios.gov.co/server/rest/"
                    "services/Hosted"
                ),
                "label": "REST Hosted — capas acueducto / captación",
            },
            {
                "method": "arcgis",
                "url": (
                    "https://geoportal.superservicios.gov.co/server/rest/"
                    "services/Hosted/Acueducto_Urbano_2024/FeatureServer"
                ),
                "label": "FeatureServer Acueducto Urbano 2024",
            },
            {
                "method": "portal",
                "url": "http://sui.superservicios.gov.co/",
                "label": "SUI — información de prestadores",
            },
        ],
        "access_methods": ["portal", "arcgis"],
        "citation_reference": (
            "Superintendencia de Servicios Públicos Domiciliarios. "
            "Infraestructura y captación asociadas al servicio de acueducto "
            "— Geoportal / SUI. "
            "https://geoportal.superservicios.gov.co/"
        ),
        "doi": "",
    },
}


class SuperserviciosConnector(BaseConnector):
    connector_id = SOURCE_ID
    source_name = "Superservicios"
    version = "1.1.0"

    def identify(self) -> dict[str, Any]:
        return normalize_source(
            source_id=SOURCE_ID,
            source="Superservicios",
            institution=INSTITUTION,
            country_or_scope="Colombia",
            domains=["hidrologia", "observacion_tierra"],
            access_methods=["portal", "arcgis"],
            description=(
                "Autoridad de vigilancia de servicios públicos domiciliarios. "
                "Geoportal y SUI con coberturas e infraestructura de "
                "acueducto (incl. captación/abastecimiento), alcantarillado "
                "y aseo. DB2S-GEO solo documenta acceso."
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
                "DB2S-GEO no descarga capas del Geoportal Superservicios. "
                "Consulte SUI/geoportal oficiales y cite la fuente."
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
            f"Superservicios. ({accessed[:4]}). {item['title']}. "
            f"{INSTITUTION}. {url}"
        )
        return {
            "source": "Superservicios",
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
