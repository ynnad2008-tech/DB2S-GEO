"""
Conector CIOH — Centro de Investigaciones Oceanográficas e Hidrográficas.

Metadatos curados humanamente. Read-only. Sin descarga ni ejecución remota.
Principio de Curaduría Humana + Attribution & Citation Policy.
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

SOURCE_ID = "cioh"
INSTITUTION = "Centro de Investigaciones Oceanográficas e Hidrográficas del Caribe"
HOMEPAGE = "https://www.dimar.mil.co/cioh"
LICENSE = "Términos institucionales DIMAR/CIOH / datos abiertos según Resolución 1751 de 2021"

_RESOURCES: dict[str, dict[str, Any]] = {
    "cioh:oceanografia-operacional": {
        "resource_id": "cioh:oceanografia-operacional",
        "title": "Oceanografía Operacional — CIOH",
        "type": "platform",
        "domains": ["oceanos_costas", "clima"],
        "primary_domain": "oceanos_costas",
        "keywords": [
            "oceanografia", "operacional", "temperatura", "superficial",
            "mar", "tsm", "salinidad", "corrientes", "marinas",
            "nivel", "mar", "oleaje", "viento", "presion",
            "atmosferica", "modelacion", "pronostico", "caribe",
        ],
        "description": (
            "Sistema de oceanografía operacional del CIOH que provee monitoreo continuo "
            "de variables oceanográficas y meteorológicas en el Caribe colombiano. "
            "Incluye pronósticos de oleaje, corrientes, temperatura superficial del mar "
            "y nivel del mar. Datos de boyas, mareógrafos y sensores remotos."
        ),
        "access": {
            "method": "portal",
            "url": "https://www.dimar.mil.co/cioh",
        },
        "attribution": (
            "Centro de Investigaciones Oceanográficas e Hidrográficas (CIOH). "
            "DIMAR. Oceanografía Operacional. "
            "Consultado [fecha]. Disponible en: https://www.dimar.mil.co/cioh"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
    "cioh:meteorologia-marina": {
        "resource_id": "cioh:meteorologia-marina",
        "title": "Meteorología Marina y Clima Marítimo — CIOH",
        "type": "dataset",
        "domains": ["clima", "oceanos_costas"],
        "primary_domain": "clima",
        "keywords": [
            "meteorologia", "marina", "viento", "oleaje", "presion",
            "temperatura", "aire", "humedad", "precipitacion",
            "clima", "maritimo", "tormentas", "huracanes", "caribe",
            "pacifico", "estaciones", "costeras", "series", "historicas",
        ],
        "description": (
            "Datos meteorológicos marinos de estaciones costeras y boyas en el Caribe "
            "y Pacífico colombiano. Series históricas de viento, presión atmosférica, "
            "temperatura del aire, humedad y precipitación en estaciones costeras. "
            "Boletines meteomarinos diarios y climatología marina."
        ),
        "access": {
            "method": "download",
            "url": "https://cecoldodigital.dimar.mil.co",
        },
        "attribution": (
            "Centro de Investigaciones Oceanográficas e Hidrográficas (CIOH). "
            "DIMAR. Meteorología Marina. "
            "Consultado [fecha]. Disponible en: https://cecoldodigital.dimar.mil.co"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
    "cioh:mareas": {
        "resource_id": "cioh:mareas",
        "title": "Mareas y Nivel del Mar — CIOH",
        "type": "dataset",
        "domains": ["oceanos_costas"],
        "primary_domain": "oceanos_costas",
        "keywords": [
            "mareas", "nivel", "mar", "mareografos", "pronostico",
            "pleamar", "bajamar", "componentes", "armonicas",
            "puertos", "costa", "caribe", "pacifico", "variacion",
        ],
        "description": (
            "Pronósticos de mareas para puertos colombianos en Caribe y Pacífico. "
            "Datos históricos de nivel del mar registrados por la red de mareógrafos. "
            "Componentes armónicas de marea calculadas para estaciones principales. "
            "Utilizado para navegación, ingeniería costera y estudios de cambio climático."
        ),
        "access": {
            "method": "download",
            "url": "https://www.dimar.mil.co/pronosticos-marea",
        },
        "attribution": (
            "Centro de Investigaciones Oceanográficas e Hidrográficas (CIOH). "
            "DIMAR. Pronósticos de mareas. "
            "Consultado [fecha]. Disponible en: https://www.dimar.mil.co"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
    "cioh:batimetria-caribe": {
        "resource_id": "cioh:batimetria-caribe",
        "title": "Batimetría Caribe y Pacífico — CIOH/SHN",
        "type": "dataset",
        "domains": ["oceanos_costas"],
        "primary_domain": "oceanos_costas",
        "keywords": [
            "batimetria", "caribe", "pacifico", "colombiano",
            "levantamientos", "hidrograficos", "multihaz", "monohaz",
            "profundidad", "relieve", "submarino", "cañones",
            "plataforma", "continental", "talud", "cuencas",
        ],
        "description": (
            "Datos batimétricos multihaz y monohaz del Caribe y Pacífico colombiano. "
            "Levantamientos hidrográficos del Servicio Hidrográfico Nacional (SHN) "
            "operados por el CIOH. Cubren áreas de plataforma continental, talud, "
            "cañones submarinos y cuencas oceánicas. Utilizados para cartografía "
            "náutica, modelación de tsunamis y estudios geofísicos marinos."
        ),
        "access": {
            "method": "wcs",
            "url": "https://www.dimar.mil.co/cioh",
        },
        "attribution": (
            "Centro de Investigaciones Oceanográficas e Hidrográficas (CIOH). "
            "DIMAR. Datos batimétricos Caribe y Pacífico. "
            "Consultado [fecha]. Disponible en: https://www.dimar.mil.co"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
    "cioh:avisos-navegantes": {
        "resource_id": "cioh:avisos-navegantes",
        "title": "Avisos a los Navegantes — CIOH",
        "type": "alert",
        "domains": ["oceanos_costas"],
        "primary_domain": "oceanos_costas",
        "keywords": [
            "avisos", "navegantes", "seguridad", "maritima",
            "novedades", "cartas", "nauticas", "peligros",
            "navegacion", "actualizaciones", "boyas", "faros",
            "naufragios", "obstrucciones", "dragados",
        ],
        "description": (
            "Boletines periódicos de seguridad marítima con novedades que afectan "
            "la navegación: cambios en ayudas a la navegación, nuevos peligros, "
            "obras marítimas, dragados, obstrucciones y actualizaciones de cartas "
            "náuticas. Información esencial para capitanes, armadores y navegantes."
        ),
        "access": {
            "method": "download",
            "url": "https://www.dimar.mil.co/avisos-navegantes",
        },
        "attribution": (
            "Centro de Investigaciones Oceanográficas e Hidrográficas (CIOH). "
            "DIMAR. Avisos a los Navegantes. "
            "Consultado [fecha]. Disponible en: https://www.dimar.mil.co"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
}


class CiohConnector(BaseConnector):
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
                    "Centro de Investigaciones Oceanográficas e Hidrográficas (CIOH). "
                    "DIMAR. Consultado [fecha]. Disponible en: https://www.dimar.mil.co/cioh"
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
