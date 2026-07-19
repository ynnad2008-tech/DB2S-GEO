"""
Conector DNP — enriquecimiento operativo DB2S-GEO.

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

SOURCE_ID = "dnp"
INSTITUTION = "Departamento Nacional de Planeación (DNP)"
HOMEPAGE = "https://www.dnp.gov.co"
LICENSE = "Según términos DNP / plataformas oficiales"

_RESOURCES: dict[str, dict[str, Any]] = {
    "dnp:catastro-multiproposito": {
        "resource_id": "dnp:catastro-multiproposito",
        "title": "Política de Catastro Multipropósito y SAT (DNP)",
        "type": "catalog",
        "domains": ["observacion_tierra"],
        "primary_domain": "observacion_tierra",
        "keywords": [
            "catastro",
            "multiproposito",
            "sat",
            "administracion",
            "territorio",
            "seguimiento",
            "politica",
            "avance",
            "cooperacion",
            "territorial",
            "planificacion",
            "nacional",
            "conpes",
            "dnp",
            "colombia",
        ],
        "description": (
            "Rol del DNP como articulador de la política de Catastro "
            "Multipropósito y del Sistema de Administración del Territorio "
            "(SAT): seguimiento de avance, planificación nacional y "
            "cooperación territorial. Complementa la operación catastral "
            "del IGAC. DB2S-GEO solo documenta el acceso; no descarga datos."
        ),
        "spatial_coverage": "Colombia",
        "temporal_coverage": "Según documentos de política y avance publicados",
        "formats": ["portal", "documentación", "noticias / indicadores"],
        "homepage": HOMEPAGE,
        "portal_url": "https://www.catastromultiproposito.gov.co/",
        "documentation_url": (
            "https://dnp.gov.co/publicaciones/Planeacion/Paginas/"
            "politica-catastro-multiproposito-colombia-transitando-"
            "catastro-tradicional-multiproposito-parte1.aspx"
        ),
        "endpoints": [
            {
                "method": "portal",
                "url": "https://www.catastromultiproposito.gov.co/",
                "label": "Portal Catastro Multipropósito",
            },
            {
                "method": "portal",
                "url": (
                    "https://dnp.gov.co/publicaciones/Planeacion/Paginas/"
                    "politica-catastro-multiproposito-colombia-transitando-"
                    "catastro-tradicional-multiproposito-parte1.aspx"
                ),
                "label": "Política Catastro Multipropósito — DNP",
            },
            {
                "method": "portal",
                "url": "https://www.icde.gov.co/marcos/catastro-multiproposito",
                "label": "ICDE — marco Catastro Multipropósito",
            },
        ],
        "access_methods": ["portal"],
        "citation_reference": (
            "Departamento Nacional de Planeación (DNP). Política de "
            "Catastro Multipropósito y Sistema de Administración del "
            "Territorio (SAT). "
            "https://www.catastromultiproposito.gov.co/"
        ),
        "doi": "",
    },
    "dnp:mapa-inversiones": {
        "resource_id": "dnp:mapa-inversiones",
        "title": "MapaInversiones — inversión pública georreferenciada (DNP)",
        "type": "catalog",
        "domains": ["observacion_tierra", "poblacion"],
        "primary_domain": "observacion_tierra",
        "keywords": [
            "mapa",
            "inversiones",
            "inversion",
            "publica",
            "proyectos",
            "presupuesto",
            "seguimiento",
            "planificacion",
            "territorial",
            "piip",
            "transparencia",
            "geovisor",
            "dnp",
            "colombia",
        ],
        "description": (
            "Plataforma MapaInversiones del DNP: georreferencia proyectos "
            "de inversión pública, recursos presupuestados/ejecutados y "
            "seguimiento físico-financiero a escala nacional y territorial. "
            "Incluye tableros, reportes y datos abiertos. DB2S-GEO solo "
            "documenta el acceso; no descarga bases ni reportes."
        ),
        "spatial_coverage": "Colombia (nacional y territorial)",
        "temporal_coverage": "Según proyectos y periodos publicados en PIIP",
        "formats": ["geovisor", "tableros", "reportes", "datos abiertos"],
        "homepage": HOMEPAGE,
        "portal_url": "https://mapainversiones.dnp.gov.co/",
        "documentation_url": (
            "https://mapainversiones.dnp.gov.co/Home/AcercaDeMapaInversiones"
        ),
        "endpoints": [
            {
                "method": "portal",
                "url": "https://mapainversiones.dnp.gov.co/",
                "label": "MapaInversiones — plataforma DNP",
            },
            {
                "method": "portal",
                "url": (
                    "https://mapainversiones.dnp.gov.co/Home/"
                    "AcercaDeMapaInversiones"
                ),
                "label": "Acerca de MapaInversiones",
            },
            {
                "method": "portal",
                "url": (
                    "https://www.dnp.gov.co/LaEntidad_/subdireccion-general-"
                    "inversiones-seguimiento-evaluacion/direccion-proyectos-"
                    "informacion-para-inversion-publica/Paginas/"
                    "mapa-de-inversion.aspx"
                ),
                "label": "Mapa Inversiones — página institucional DNP",
            },
        ],
        "access_methods": ["portal"],
        "citation_reference": (
            "Departamento Nacional de Planeación (DNP). MapaInversiones — "
            "plataforma de inversión pública georreferenciada. "
            "https://mapainversiones.dnp.gov.co/"
        ),
        "doi": "",
    },
}


class DnpConnector(BaseConnector):
    connector_id = SOURCE_ID
    source_name = "DNP"
    version = "1.0.0"

    def identify(self) -> dict[str, Any]:
        return normalize_source(
            source_id=SOURCE_ID,
            source="DNP",
            institution=INSTITUTION,
            country_or_scope="Colombia",
            domains=["observacion_tierra", "poblacion"],
            access_methods=["portal"],
            description=(
                "Departamento Nacional de Planeación: política de Catastro "
                "Multipropósito / SAT y plataforma MapaInversiones de "
                "inversión pública georreferenciada. "
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
                "DB2S-GEO no descarga productos DNP. "
                "Consulte los portales oficiales y cite la fuente."
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
            f"DNP. ({accessed[:4]}). {item['title']}. "
            f"{INSTITUTION}. {url}"
        )
        return {
            "source": "DNP",
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
