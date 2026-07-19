"""
Conector ANI — enriquecimiento operativo DB2S-GEO.

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

SOURCE_ID = "ani"
INSTITUTION = "Agencia Nacional de Infraestructura (ANI)"
HOMEPAGE = "https://www.ani.gov.co"
LICENSE = "Según términos ANI / ANIscopio"

_RESOURCES: dict[str, dict[str, Any]] = {
    "ani:aniscopio": {
        "resource_id": "ani:aniscopio",
        "title": "ANIscopio — concesiones e infraestructura estratégica",
        "type": "catalog",
        "domains": ["observacion_tierra"],
        "primary_domain": "observacion_tierra",
        "keywords": [
            "aniscopio",
            "concesiones",
            "viales",
            "ferreas",
            "aeroportuarias",
            "portuarias",
            "infraestructura",
            "nacional",
            "logistica",
            "ppp",
            "geovisor",
            "ani"
        ],
        "description": (
            "Plataforma ANIscopio de la ANI: visor geográfico de proyectos "
            "de infraestructura concesionada (vial, férrea, aeroportuaria y "
            "portuaria), avances de obra y capas descargables del SIG ANI. "
            "DB2S-GEO solo documenta el acceso; no descarga shapefiles."
        ),
        "spatial_coverage": "Colombia (proyectos concesionados ANI)",
        "temporal_coverage": "Según estado de proyectos publicados",
        "formats": ["geovisor", "shapefile (descarga SIG)", "portal"],
        "homepage": HOMEPAGE,
        "portal_url": "https://aniscopio.ani.gov.co/",
        "documentation_url": (
            "https://www.ani.gov.co/plataforma-aniscopio-un-caso-de-exito-"
            "en-latinoamerica"
        ),
        "endpoints": [
            {
                "method": "portal",
                "url": "https://aniscopio.ani.gov.co/",
                "label": "ANIscopio — visor de concesiones",
            },
            {
                "method": "portal",
                "url": HOMEPAGE,
                "label": "Portal institucional ANI",
            },
            {
                "method": "portal",
                "url": (
                    "https://www.ani.gov.co/plataforma-aniscopio-un-caso-de-"
                    "exito-en-latinoamerica"
                ),
                "label": "Descripción plataforma ANIscopio",
            },
        ],
        "access_methods": ["portal"],
        "citation_reference": (
            "Agencia Nacional de Infraestructura (ANI). ANIscopio — "
            "proyectos de infraestructura concesionada. "
            "https://aniscopio.ani.gov.co/"
        ),
        "doi": "",
    },
    "ani:atlas-concesiones": {
        "resource_id": "ani:atlas-concesiones",
        "title": "Atlas / capas de concesiones y corredores (ANI SIG)",
        "type": "dataset",
        "domains": ["observacion_tierra"],
        "primary_domain": "observacion_tierra",
        "keywords": [
            "atlas",
            "concesiones",
            "corredores",
            "logisticos",
            "peajes",
            "areas",
            "influencia",
            "movilidad",
            "carreteras",
            "modos",
            "sig",
            "ani"
        ],
        "description": (
            "Suite geográfica ANI de concesiones por modos, peajes, "
            "áreas de influencia y corredores logísticos: capas MapServer/"
            "FeatureServer del SIG ANI (Concesiones_Modos, Carreteras, "
            "etc.) complementarias al visor ANIscopio. "
            "DB2S-GEO solo documenta el acceso; no descarga capas."
        ),
        "spatial_coverage": "Colombia (concesiones ANI)",
        "temporal_coverage": "Según actualización SIG ANI",
        "formats": ["MapServer", "FeatureServer", "shapefile", "geovisor"],
        "homepage": HOMEPAGE,
        "portal_url": "https://aniscopio.ani.gov.co/",
        "documentation_url": (
            "https://sig.ani.gov.co/descargas/shpsiganidescargar/"
            "Descripci%C3%B3n%20descargas%20SIG%20ANI.pdf"
        ),
        "endpoints": [
            {
                "method": "arcgis",
                "url": (
                    "https://sig.ani.gov.co/arcgis/rest/services/SigAni/"
                    "Concesiones_Modos/MapServer"
                ),
                "label": "MapServer Concesiones_Modos (atlas multimodal)",
            },
            {
                "method": "arcgis",
                "url": (
                    "https://sig.ani.gov.co/arcgis/rest/services/SigAni/"
                    "ConcesionesCarreteras/MapServer"
                ),
                "label": "MapServer Concesiones Carreteras / peajes",
            },
            {
                "method": "portal",
                "url": "https://aniscopio.ani.gov.co/",
                "label": "ANIscopio — suite de geovisores",
            },
        ],
        "access_methods": ["portal", "arcgis"],
        "citation_reference": (
            "Agencia Nacional de Infraestructura (ANI). Atlas / capas SIG "
            "de concesiones y corredores. "
            "https://sig.ani.gov.co/arcgis/rest/services/SigAni/"
            "Concesiones_Modos/MapServer"
        ),
        "doi": "",
    },
    "ani:fichas-portuarias": {
        "resource_id": "ani:fichas-portuarias",
        "title": "Fichas y concesiones de zonas portuarias (ANI)",
        "type": "dataset",
        "domains": ["oceanos_costas", "observacion_tierra"],
        "primary_domain": "oceanos_costas",
        "keywords": [
            "fichas",
            "portuarias",
            "puertos",
            "zonas",
            "portuarias",
            "concesiones",
            "maritimas",
            "buenaventura",
            "cartagena",
            "santa",
            "marta",
            "logistica",
            "ani"
        ],
        "description": (
            "Fichas cualitativas, cuantitativas y espaciales de las "
            "principales zonas portuarias de Colombia (Buenaventura, "
            "Guajira, Santa Marta/Ciénaga, Urabá, Cartagena, Tumaco, "
            "Golfo de Morrosquillo, San Andrés) y capas de concesiones "
            "portuarias del SIG ANI. DB2S-GEO solo documenta el acceso."
        ),
        "spatial_coverage": "Colombia (zonas portuarias / concesiones marítimas)",
        "temporal_coverage": "Según fichas y capas publicadas por la ANI",
        "formats": ["fichas web", "MapServer", "FeatureServer", "portal"],
        "homepage": HOMEPAGE,
        "portal_url": "https://www.ani.gov.co/zonas-portuarias/",
        "documentation_url": (
            "https://www.ani.gov.co/zonas-portuarias/"
            "zona-portuaria-de-buenaventura"
        ),
        "endpoints": [
            {
                "method": "portal",
                "url": "https://www.ani.gov.co/zonas-portuarias/",
                "label": "Zonas portuarias ANI — fichas",
            },
            {
                "method": "arcgis",
                "url": (
                    "https://sig.ani.gov.co/arcgis/rest/services/SigAni/"
                    "ConcesionesPuertos/MapServer"
                ),
                "label": "MapServer Concesiones Puertos",
            },
            {
                "method": "portal",
                "url": "https://aniscopio.ani.gov.co/",
                "label": "ANIscopio — modo portuario",
            },
        ],
        "access_methods": ["portal", "arcgis"],
        "citation_reference": (
            "Agencia Nacional de Infraestructura (ANI). Fichas y "
            "concesiones de zonas portuarias. "
            "https://www.ani.gov.co/zonas-portuarias/"
        ),
        "doi": "",
    },
}


class AniConnector(BaseConnector):
    connector_id = SOURCE_ID
    source_name = "ANI"
    version = "1.1.0"

    def identify(self) -> dict[str, Any]:
        return normalize_source(
            source_id=SOURCE_ID,
            source="ANI",
            institution=INSTITUTION,
            country_or_scope="Colombia",
            domains=["observacion_tierra", "oceanos_costas"],
            access_methods=["portal", "arcgis"],
            description=(
                "Agencia Nacional de Infraestructura: ANIscopio, atlas/"
                "capas SIG de concesiones y fichas portuarias. "
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
                "DB2S-GEO no descarga capas de ANIscopio. "
                "Consulte el visor oficial y cite la fuente."
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
            f"ANI. ({accessed[:4]}). {item['title']}. "
            f"{INSTITUTION}. {url}"
        )
        return {
            "source": "ANI",
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
