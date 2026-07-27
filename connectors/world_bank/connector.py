"""
Conector World Bank — Banco Mundial (DataBank / API).

Metadatos curados humanamente. Read-only. Indicadores de desarrollo global:
PIB, pobreza, población, educación, salud, cambio climático económico.
"""

from __future__ import annotations
from typing import Any
from connectors._curated import (
    filter_resources, find_resource, resource_not_found, today_iso,
)
from connectors.base import BaseConnector
from connectors.models import normalize_source

SOURCE_ID = "world_bank"
INSTITUTION = "World Bank Group / DataBank"
HOMEPAGE = "https://data.worldbank.org"
LICENSE = "CC BY 4.0 / Datos abiertos"

_RESOURCES: dict[str, dict[str, Any]] = {
    "world_bank:wdi": {
        "resource_id": "world_bank:wdi",
        "title": "World Development Indicators (WDI) — Banco Mundial",
        "type": "dataset",
        "domains": ["economia", "poblacion"],
        "primary_domain": "economia",
        "keywords": ["wdi", "pib", "pobreza", "desigualdad", "gini",
                     "poblacion", "educacion", "salud", "infraestructura",
                     "comercio", "deuda", "inversion", "indicadores",
                     "desarrollo", "banco_mundial", "colombia", "serie_tiempo"],
        "description": (
            "Base de datos de indicadores de desarrollo más completa del mundo. "
            "1,600+ indicadores para 200+ países desde 1960. PIB, pobreza, "
            "desigualdad (Gini), esperanza de vida, alfabetización, acceso a "
            "servicios básicos. API REST (JSON/XML) y descarga CSV/Excel."
        ),
        "access": {"method": "rest", "url": "https://api.worldbank.org/v2/"},
        "attribution": "World Bank. World Development Indicators. https://data.worldbank.org",
        "status": "active", "curated_at": today_iso(),
    },
    "world_bank:climate": {
        "resource_id": "world_bank:climate",
        "title": "Climate Change Knowledge Portal (CCKP) — Banco Mundial",
        "type": "dataset",
        "domains": ["clima", "riesgo", "economia"],
        "primary_domain": "clima",
        "keywords": ["clima", "cambio_climatico", "proyecciones", "cmip6",
                     "temperatura", "precipitacion", "adaptacion", "vulnerabilidad",
                     "impactos", "agricolas", "hidricos", "salud", "colombia"],
        "description": (
            "Portal de conocimiento de cambio climático con proyecciones CMIP6, "
            "datos históricos, escenarios de emisiones y evaluaciones de "
            "vulnerabilidad por país. Incluye impactos proyectados en agricultura, "
            "recursos hídricos y salud para Colombia y América Latina."
        ),
        "access": {"method": "portal", "url": "https://climateknowledgeportal.worldbank.org"},
        "attribution": "World Bank. Climate Change Knowledge Portal. https://climateknowledgeportal.worldbank.org",
        "status": "active", "curated_at": today_iso(),
    },
    "world_bank:gender": {
        "resource_id": "world_bank:gender",
        "title": "Gender Data Portal — Banco Mundial",
        "type": "dataset",
        "domains": ["poblacion", "economia"],
        "primary_domain": "poblacion",
        "keywords": ["genero", "mujeres", "brecha", "salarial", "participacion",
                     "laboral", "educacion", "salud_materna", "violencia",
                     "empoderamiento", "inclusion", "colombia", "latinoamerica"],
        "description": (
            "Portal de datos de género con indicadores desagregados por sexo: "
            "participación laboral, brecha salarial, educación, salud materna, "
            "representación política. Datos por país con series 1960-presente."
        ),
        "access": {"method": "rest", "url": "https://genderdata.worldbank.org"},
        "attribution": "World Bank. Gender Data Portal. https://genderdata.worldbank.org",
        "status": "active", "curated_at": today_iso(),
    },
}


class WorldBankConnector(BaseConnector):
    connector_id = SOURCE_ID
    institution = INSTITUTION
    homepage = HOMEPAGE
    license = LICENSE
    version = "1.0.0"

    def identify(self) -> dict[str, Any]:
        return {"connector_id": self.connector_id, "institution": self.institution,
                "homepage": self.homepage, "license": self.license,
                "version": self.version, "phase": "mvp", "curation": "human",
                "resources": len(_RESOURCES)}

    def discover(self) -> dict[str, Any]:
        return normalize_source(source_id=self.connector_id, institution=self.institution,
                                homepage=self.homepage, license=self.license, resources=_RESOURCES)

    def describe(self, source_id: str | None = None) -> dict[str, Any]:
        return normalize_source(source_id=self.connector_id, institution=self.institution,
                                homepage=self.homepage, license=self.license, resources=_RESOURCES)

    def access_info(self, resource_id: str | None = None) -> dict[str, Any]:
        if resource_id is None:
            return {"source_id": self.connector_id, "access": "portal"}
        resource = find_resource(_RESOURCES, resource_id, self.connector_id)
        if resource is None:
            return resource_not_found(self.connector_id, resource_id)
        return {"source_id": self.connector_id, "resource_id": resource_id,
                "access": resource.get("access", {})}

    def cite(self, resource_id: str | None = None) -> dict[str, Any]:
        if resource_id is None:
            return {"source_id": self.connector_id,
                    "citation": "World Bank. DataBank. https://data.worldbank.org"}
        resource = find_resource(_RESOURCES, resource_id, self.connector_id)
        if resource is None:
            return resource_not_found(self.connector_id, resource_id)
        return {"source_id": self.connector_id, "resource_id": resource_id,
                "citation": resource.get("attribution", "")}

    def list_resources(self, domain: str | None = None) -> list[dict[str, Any]]:
        return filter_resources(_RESOURCES, domain)

    def get_resource(self, resource_id: str) -> dict[str, Any] | None:
        return find_resource(_RESOURCES, resource_id, self.connector_id)
