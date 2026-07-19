"""
Conector DANE — enriquecimiento operativo DB2S-GEO.

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

SOURCE_ID = "dane"
INSTITUTION = "Departamento Administrativo Nacional de Estadística (DANE)"
HOMEPAGE = "https://www.dane.gov.co"
LICENSE = "Según términos DANE / microdatos / datos abiertos"

_RESOURCES: dict[str, dict[str, Any]] = {
    "dane:encuesta-agropecuaria": {
        "resource_id": "dane:encuesta-agropecuaria",
        "title": "Encuesta Nacional Agropecuaria (ENA) — DANE",
        "type": "dataset",
        "domains": ["agricultura", "poblacion"],
        "primary_domain": "agricultura",
        "keywords": [
            "encuesta",
            "nacional",
            "agropecuaria",
            "ena",
            "produccion",
            "rendimiento",
            "cultivos",
            "inventario",
            "pecuario",
            "seguridad",
            "alimentaria",
            "estadisticas",
            "rurales",
            "dane"
        ],
        "description": (
            "Operación estadística del DANE que estima uso del suelo, área, "
            "producción y rendimiento de cultivos, inventario pecuario y "
            "producción de leche en Colombia. Boletines, anexos y microdatos "
            "oficiales. DB2S-GEO solo documenta el acceso; no descarga "
            "microdatos ni tablas."
        ),
        "spatial_coverage": "Colombia (32 departamentos según operación)",
        "temporal_coverage": "Según año de operación ENA publicado",
        "formats": ["boletines", "anexos", "microdatos", "portal"],
        "homepage": HOMEPAGE,
        "portal_url": (
            "https://www.dane.gov.co/index.php/estadisticas-por-tema/"
            "agropecuario/encuesta-nacional-agropecuaria-ena/"
        ),
        "documentation_url": (
            "https://www.dane.gov.co/index.php/estadisticas-por-tema/"
            "agropecuario/encuesta-nacional-agropecuaria-ena/"
        ),
        "endpoints": [
            {
                "method": "portal",
                "url": (
                    "https://www.dane.gov.co/index.php/estadisticas-por-tema/"
                    "agropecuario/encuesta-nacional-agropecuaria-ena/"
                ),
                "label": "ENA — página oficial DANE",
            },
            {
                "method": "portal",
                "url": "https://microdatos.dane.gov.co/",
                "label": "Archivo de microdatos DANE",
            },
            {
                "method": "portal",
                "url": HOMEPAGE,
                "label": "Portal institucional DANE",
            },
        ],
        "access_methods": ["portal"],
        "citation_reference": (
            "Departamento Administrativo Nacional de Estadística (DANE). "
            "Encuesta Nacional Agropecuaria (ENA). "
            "https://www.dane.gov.co/index.php/estadisticas-por-tema/"
            "agropecuario/encuesta-nacional-agropecuaria-ena/"
        ),
        "doi": "",
    },
    "dane:eva-agricola": {
        "resource_id": "dane:eva-agricola",
        "title": "Evaluaciones Agropecuarias Municipales (EVA)",
        "type": "dataset",
        "domains": ["agricultura"],
        "primary_domain": "agricultura",
        "keywords": [
            "eva",
            "evaluaciones",
            "agropecuarias",
            "municipales",
            "agricultura",
            "produccion",
            "rendimiento",
            "cultivos",
            "area",
            "cosechada",
            "estadisticas",
            "oficiales",
            "upra",
            "dane"
        ],
        "description": (
            "Evaluaciones Agropecuarias Municipales (EVA): estadísticas de "
            "área, producción y rendimiento de cultivos a escala municipal "
            "(operación a cargo de UPRA / MADR; difusión también vía "
            "Agronet y datos.gov.co). Complementa la ENA del DANE para "
            "análisis de producción agrícola. DB2S-GEO solo documenta el "
            "acceso; no descarga bases."
        ),
        "spatial_coverage": "Colombia (municipios con reporte EVA)",
        "temporal_coverage": "Según serie publicada (p. ej. 2019–2024)",
        "formats": ["CSV/tablas", "portal", "SIPRA", "datos abiertos"],
        "homepage": "https://upra.gov.co/es-co/eva",
        "portal_url": "https://upra.gov.co/es-co/eva",
        "documentation_url": (
            "https://www.datos.gov.co/Agricultura-y-Desarrollo-Rural/"
            "Evaluaciones-Agropecuarias-Municipales-EVA/2pnw-mmge"
        ),
        "endpoints": [
            {
                "method": "portal",
                "url": "https://upra.gov.co/es-co/eva",
                "label": "EVA — portal UPRA",
            },
            {
                "method": "portal",
                "url": (
                    "https://www.datos.gov.co/Agricultura-y-Desarrollo-Rural/"
                    "Evaluaciones-Agropecuarias-Municipales-EVA/2pnw-mmge"
                ),
                "label": "EVA — Datos Abiertos Colombia",
            },
            {
                "method": "portal",
                "url": (
                    "https://agronet.gov.co/plataformas/"
                    "evaluaciones-agropecuarias-municipales-eva"
                ),
                "label": "EVA — Agronet",
            },
        ],
        "access_methods": ["portal"],
        "citation_reference": (
            "Unidad de Planificación Rural Agropecuaria (UPRA) / MADR. "
            "Evaluaciones Agropecuarias Municipales (EVA). "
            "https://upra.gov.co/es-co/eva"
        ),
        "doi": "",
    },
}


class DaneConnector(BaseConnector):
    connector_id = SOURCE_ID
    source_name = "DANE"
    version = "1.1.0"

    def identify(self) -> dict[str, Any]:
        return normalize_source(
            source_id=SOURCE_ID,
            source="DANE",
            institution=INSTITUTION,
            country_or_scope="Colombia",
            domains=["agricultura", "poblacion"],
            access_methods=["portal"],
            description=(
                "Autoridad estadística nacional de Colombia. Documenta "
                "operaciones agropecuarias (ENA) y el acceso a EVA "
                "(producción municipal, UPRA/MADR) para seguridad "
                "alimentaria y economía rural. DB2S-GEO solo documenta acceso."
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
                "DB2S-GEO no descarga microdatos ni anexos DANE. "
                "Consulte el portal oficial y cite la operación estadística."
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
            f"DANE. ({accessed[:4]}). {item['title']}. "
            f"{INSTITUTION}. {url}"
        )
        return {
            "source": "DANE",
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
