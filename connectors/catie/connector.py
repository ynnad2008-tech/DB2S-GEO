"""
Conector CATIE — Centro Agronómico Tropical de Investigación y Enseñanza.

Metadatos curados humanamente. Read-only. CATIE es el centro de investigación
agroforestal tropical más importante de América Latina. Café, cacao, sistemas
silvopastoriles, cambio climático y cuencas hidrográficas.
"""

from __future__ import annotations
from typing import Any
from connectors._curated import (
    filter_resources, find_resource, resource_not_found, today_iso,
)
from connectors.base import BaseConnector
from connectors.models import normalize_source

SOURCE_ID = "catie"
INSTITUTION = "Centro Agronómico Tropical de Investigación y Enseñanza (CATIE)"
HOMEPAGE = "https://www.catie.ac.cr"
LICENSE = "Acceso abierto con atribución / términos institucionales CATIE"

_RESOURCES: dict[str, dict[str, Any]] = {
    "catie:cafe": {
        "resource_id": "catie:cafe",
        "title": "Investigación en Café — CATIE",
        "type": "dataset",
        "domains": ["agricultura", "clima"],
        "primary_domain": "agricultura",
        "keywords": ["cafe", "cafetales", "agroforesteria", "sombra", "variedades",
                     "roya", "plagas", "cambio_climatico", "adaptacion", "catie"],
        "description": (
            "Investigación en sistemas agroforestales de café: variedades resistentes "
            "a roya, manejo de sombra, adaptación al cambio climático. "
            "Colección internacional de germoplasma de café. Datos de fincas "
            "experimentales en Centroamérica y Colombia."
        ),
        "access": {"method": "portal", "url": "https://www.catie.ac.cr/cafe"},
        "attribution": "CATIE. Programa de Café. https://www.catie.ac.cr",
        "status": "active", "curated_at": today_iso(),
    },
    "catie:cacao": {
        "resource_id": "catie:cacao",
        "title": "Investigación en Cacao — CATIE",
        "type": "dataset",
        "domains": ["agricultura", "biodiversidad"],
        "primary_domain": "agricultura",
        "keywords": ["cacao", "cacaotales", "agroforesteria", "clones", "genetica",
                     "moniliasis", "fitomejoramiento", "centroamerica", "colombia"],
        "description": (
            "Colección internacional de germoplasma de cacao. Investigación en "
            "sistemas agroforestales de cacao, resistencia a moniliasis y "
            "fitomejoramiento genético. Banco de clones élite para el trópico."
        ),
        "access": {"method": "portal", "url": "https://www.catie.ac.cr/cacao"},
        "attribution": "CATIE. Programa de Cacao. https://www.catie.ac.cr",
        "status": "active", "curated_at": today_iso(),
    },
    "catie:cuencas": {
        "resource_id": "catie:cuencas",
        "title": "Manejo de Cuencas Hidrográficas — CATIE",
        "type": "dataset",
        "domains": ["hidrologia", "agricultura", "clima"],
        "primary_domain": "hidrologia",
        "keywords": ["cuencas", "hidrologia", "morfometria", "manejo", "agua",
                     "servicios_ecosistemicos", "pago_servicios_ambientales",
                     "modelacion", "swat", "balance_hidrico", "centroamerica"],
        "description": (
            "Investigación aplicada en manejo integrado de cuencas hidrográficas "
            "tropicales. Modelación hidrológica (SWAT), morfometría de cuencas, "
            "servicios ecosistémicos hídricos y esquemas de PSA. "
            "Experiencia en cuencas cafeteras de Centroamérica y Colombia."
        ),
        "access": {"method": "portal", "url": "https://www.catie.ac.cr/cuencas"},
        "attribution": "CATIE. Programa de Cuencas. https://www.catie.ac.cr",
        "status": "active", "curated_at": today_iso(),
    },
    "catie:clima": {
        "resource_id": "catie:clima",
        "title": "Cambio Climático y Agricultura Tropical — CATIE",
        "type": "dataset",
        "domains": ["clima", "agricultura"],
        "primary_domain": "clima",
        "keywords": ["cambio_climatico", "adaptacion", "mitigacion", "agricultura",
                     "tropical", "modelos", "escenarios", "vulnerabilidad",
                     "ndc", "ganaderia", "silvopastoril", "catie"],
        "description": (
            "Modelación de impactos del cambio climático en agricultura tropical. "
            "Escenarios de adaptación para café, cacao, ganadería. "
            "Sistemas silvopastoriles como estrategia de mitigación. "
            "NDC y políticas climáticas para el sector agrícola."
        ),
        "access": {"method": "download", "url": "https://www.catie.ac.cr/clima"},
        "attribution": "CATIE. Programa de Cambio Climático. https://www.catie.ac.cr",
        "status": "active", "curated_at": today_iso(),
    },
}


class CatieConnector(BaseConnector):
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
                    "citation": "CATIE. https://www.catie.ac.cr"}
        resource = find_resource(_RESOURCES, resource_id, self.connector_id)
        if resource is None:
            return resource_not_found(self.connector_id, resource_id)
        return {"source_id": self.connector_id, "resource_id": resource_id,
                "citation": resource.get("attribution", "")}

    def list_resources(self, domain: str | None = None) -> list[dict[str, Any]]:
        return filter_resources(_RESOURCES, domain)

    def get_resource(self, resource_id: str) -> dict[str, Any] | None:
        return find_resource(_RESOURCES, resource_id, self.connector_id)
