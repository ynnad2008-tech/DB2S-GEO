"""
Conector SiB Colombia — Sistema de Información sobre Biodiversidad de Colombia.

Metadatos curados humanamente. Read-only. Sin descarga ni ejecución remota.
SiB Colombia es el nodo nacional de GBIF. Publica datos de biodiversidad
de cientos de instituciones colombianas: colecciones biológicas, museos,
herbarios, observaciones de ciencia ciudadana y monitoreo institucional.
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

SOURCE_ID = "sib_colombia"
INSTITUTION = "Sistema de Información sobre Biodiversidad de Colombia (SiB Colombia)"
HOMEPAGE = "https://sibcolombia.net"
LICENSE = "Variables según publicador / datos abiertos con atribución"

_RESOURCES: dict[str, dict[str, Any]] = {
    "sib_colombia:explorador": {
        "resource_id": "sib_colombia:explorador",
        "title": "Explorador de Datos — SiB Colombia",
        "type": "portal",
        "domains": ["biodiversidad"],
        "primary_domain": "biodiversidad",
        "keywords": [
            "biodiversidad", "especies", "ocurrencias", "registros",
            "biologicos", "colecciones", "museos", "herbarios",
            "colombia", "gbif", "nodo", "nacional", "datos", "abiertos",
        ],
        "description": (
            "Portal principal de consulta de datos de biodiversidad de Colombia. "
            "Agrega cientos de conjuntos de datos de instituciones colombianas: "
            "colecciones biológicas, museos de historia natural, herbarios, "
            "observaciones de ciencia ciudadana (iNaturalist, eBird Colombia), "
            "y monitoreo institucional. Nodo oficial de GBIF en Colombia."
        ),
        "access": {
            "method": "portal",
            "url": "https://sibcolombia.net",
        },
        "attribution": (
            "Sistema de Información sobre Biodiversidad de Colombia (SiB Colombia). "
            "Explorador de Datos. "
            "Consultado [fecha]. Disponible en: https://sibcolombia.net"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
    "sib_colombia:catalogo": {
        "resource_id": "sib_colombia:catalogo",
        "title": "Catálogo de Metadatos — SiB Colombia",
        "type": "catalog",
        "domains": ["biodiversidad"],
        "primary_domain": "biodiversidad",
        "keywords": [
            "metadatos", "catalogo", "biodiversidad", "conjuntos",
            "datos", "publicadores", "instituciones", "colecciones",
            "colombia", "curados", "estandar", "darwin", "core",
        ],
        "description": (
            "Catálogo nacional de metadatos de biodiversidad. Inventario de todos "
            "los conjuntos de datos publicados por instituciones colombianas a través "
            "del SiB. Incluye información sobre publicadores, licencias, cobertura "
            "taxonómica y geográfica. Metadatos estandarizados bajo Darwin Core."
        ),
        "access": {
            "method": "portal",
            "url": "https://sibcolombia.net/datos/",
        },
        "attribution": (
            "Sistema de Información sobre Biodiversidad de Colombia (SiB Colombia). "
            "Catálogo de Metadatos. "
            "Consultado [fecha]. Disponible en: https://sibcolombia.net"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
    "sib_colombia:api": {
        "resource_id": "sib_colombia:api",
        "title": "API REST — SiB Colombia (GBIF API nacional)",
        "type": "api",
        "domains": ["biodiversidad"],
        "primary_domain": "biodiversidad",
        "keywords": [
            "api", "rest", "gbif", "json", "ocurrencias", "especies",
            "taxonomia", "registros", "biologicos", "programatica",
            "web", "services", "colombia",
        ],
        "description": (
            "API REST compatible con GBIF para consulta programática de registros "
            "biológicos de Colombia. Soporta filtros por taxonomía, geografía, "
            "fecha, publicador y licencia. Formatos: JSON, Darwin Core Archive, CSV. "
            "Documentación en https://sibcolombia.net/api/"
        ),
        "access": {
            "method": "rest",
            "url": "https://api.sibcolombia.net",
        },
        "attribution": (
            "Sistema de Información sobre Biodiversidad de Colombia (SiB Colombia). "
            "API REST. Nodo GBIF Colombia. "
            "Consultado [fecha]. Disponible en: https://sibcolombia.net"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
    "sib_colombia:colecciones": {
        "resource_id": "sib_colombia:colecciones",
        "title": "Registro Nacional de Colecciones Biológicas — SiB Colombia",
        "type": "registry",
        "domains": ["biodiversidad"],
        "primary_domain": "biodiversidad",
        "keywords": [
            "colecciones", "biologicas", "museos", "herbarios",
            "zoologicos", "botanicos", "registro", "nacional",
            "curaduria", "especimenes", "colombia",
        ],
        "description": (
            "Registro Nacional de Colecciones Biológicas de Colombia. "
            "Directorio autorizado de todas las colecciones biológicas del país: "
            "herbarios, museos zoológicos, colecciones entomológicas, bancos de "
            "tejidos y colecciones microbiológicas. Incluye metadatos de contacto, "
            "tamaño de colección y cobertura taxonómica."
        ),
        "access": {
            "method": "portal",
            "url": "https://sibcolombia.net/colecciones/",
        },
        "attribution": (
            "Sistema de Información sobre Biodiversidad de Colombia (SiB Colombia). "
            "Registro Nacional de Colecciones Biológicas. "
            "Consultado [fecha]. Disponible en: https://sibcolombia.net"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
}


class SibColombiaConnector(BaseConnector):
    connector_id = SOURCE_ID
    institution = INSTITUTION
    homepage = HOMEPAGE
    license = LICENSE
    version = "1.0.0"

    def identify(self) -> dict[str, Any]:
        return {
            "connector_id": self.connector_id,
            "institution": self.institution,
            "homepage": self.homepage,
            "license": self.license,
            "version": self.version,
            "phase": "mvp",
            "curation": "human",
            "resources": len(_RESOURCES),
        }

    def discover(self) -> dict[str, Any]:
        return normalize_source(
            source_id=self.connector_id,
            institution=self.institution,
            homepage=self.homepage,
            license=self.license,
            resources=_RESOURCES,
        )

    def describe(self, source_id: str | None = None) -> dict[str, Any]:
        return normalize_source(
            source_id=self.connector_id,
            institution=self.institution,
            homepage=self.homepage,
            license=self.license,
            resources=_RESOURCES,
        )

    def access_info(self, resource_id: str | None = None) -> dict[str, Any]:
        if resource_id is None:
            return {"source_id": self.connector_id, "access": "portal"}
        resource = find_resource(_RESOURCES, resource_id, self.connector_id)
        if resource is None:
            return resource_not_found(self.connector_id, resource_id)
        return {
            "source_id": self.connector_id,
            "resource_id": resource_id,
            "access": resource.get("access", {}),
        }

    def cite(self, resource_id: str | None = None) -> dict[str, Any]:
        if resource_id is None:
            return {
                "source_id": self.connector_id,
                "citation": (
                    "Sistema de Información sobre Biodiversidad de Colombia (SiB Colombia). "
                    "Consultado [fecha]. Disponible en: https://sibcolombia.net"
                ),
            }
        resource = find_resource(_RESOURCES, resource_id, self.connector_id)
        if resource is None:
            return resource_not_found(self.connector_id, resource_id)
        return {
            "source_id": self.connector_id,
            "resource_id": resource_id,
            "citation": resource.get("attribution", ""),
        }

    def list_resources(self, domain: str | None = None) -> list[dict[str, Any]]:
        return filter_resources(_RESOURCES, domain)

    def get_resource(self, resource_id: str) -> dict[str, Any] | None:
        return find_resource(_RESOURCES, resource_id, self.connector_id)
