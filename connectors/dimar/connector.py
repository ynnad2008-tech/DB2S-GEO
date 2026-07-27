"""
Conector DIMAR — Dirección General Marítima de Colombia.

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

SOURCE_ID = "dimar"
INSTITUTION = "Dirección General Marítima de Colombia"
HOMEPAGE = "https://www.dimar.mil.co"
LICENSE = "Términos institucionales DIMAR / datos abiertos según Resolución 1751 de 2021"

_RESOURCES: dict[str, dict[str, Any]] = {
    "dimar:sigdimar": {
        "resource_id": "dimar:sigdimar",
        "title": "SIGDIMAR — Sistema de Información Geográfica de DIMAR",
        "type": "platform",
        "domains": ["oceanos_costas", "hidrologia", "observacion_tierra"],
        "primary_domain": "oceanos_costas",
        "keywords": [
            "sigdimar", "mares", "costas", "cartografia", "nautica",
            "batimetria", "senalizacion", "maritima", "litorales",
            "gis", "arcgis", "geoservicios", "wms", "wfs",
        ],
        "description": (
            "Sistema de Información Geográfica de la Autoridad Marítima Colombiana. "
            "Integra bases de datos geoespaciales con esquemas ASEM (señalización), "
            "ARHD (hidrografía), AMIZC (manejo costero), AROPE (oceanografía operacional), "
            "LITORALES, SEAFLOWER y ANTARTICA. 70+ aplicaciones geográficas desarrolladas."
        ),
        "access": {
            "method": "portal",
            "url": "https://litorales-dimar.hub.arcgis.com",
        },
        "attribution": (
            "Dirección General Marítima de Colombia (DIMAR). "
            "SIGDIMAR — Sistema de Información Geográfica. "
            "Consultado [fecha]. Disponible en: https://www.dimar.mil.co"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
    "dimar:cartas-nauticas": {
        "resource_id": "dimar:cartas-nauticas",
        "title": "Cartas Náuticas Electrónicas (ENC) — DIMAR",
        "type": "dataset",
        "domains": ["oceanos_costas"],
        "primary_domain": "oceanos_costas",
        "keywords": [
            "cartas", "nauticas", "enc", "navegacion", "profundidad",
            "batimetria", "puertos", "derrotas", "s57", "iho",
            "cartografia", "maritima", "seguridad", "navegacion",
        ],
        "description": (
            "63 Cartas Náuticas Electrónicas (ENC) con cobertura del 100% en cartas de paso "
            "y puerto, y 76% en cartas costeras. Producidas por el Servicio Hidrográfico "
            "Nacional (SHN) bajo estándar IHO S-57. Siglo XIX al presente."
        ),
        "access": {
            "method": "portal",
            "url": "https://www.dimar.mil.co/cartografia-nautica",
        },
        "attribution": (
            "Dirección General Marítima de Colombia (DIMAR). "
            "Servicio Hidrográfico Nacional. Cartas Náuticas Electrónicas. "
            "Consultado [fecha]. Disponible en: https://www.dimar.mil.co"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
    "dimar:batimetria": {
        "resource_id": "dimar:batimetria",
        "title": "Superficies Batimétricas — DIMAR",
        "type": "dataset",
        "domains": ["oceanos_costas"],
        "primary_domain": "oceanos_costas",
        "keywords": [
            "batimetria", "superficies", "profundidad", "fondo", "marino",
            "relevo", "submarino", "csar", "hidrografia", "oceanografia",
            "caribe", "pacifico", "colombiano",
        ],
        "description": (
            "494 superficies batimétricas en formato .csar generadas a partir de levantamientos "
            "hidrográficos del SHN. Cubren áreas del Caribe y Pacífico colombiano. "
            "Utilizadas para cartografía náutica, modelación oceanográfica y gestión costera."
        ),
        "access": {
            "method": "wcs",
            "url": "https://www.dimar.mil.co/datos-batimetricos",
        },
        "attribution": (
            "Dirección General Marítima de Colombia (DIMAR). "
            "Superficies batimétricas. Servicio Hidrográfico Nacional. "
            "Consultado [fecha]. Disponible en: https://www.dimar.mil.co"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
    "dimar:senalizacion-maritima": {
        "resource_id": "dimar:senalizacion-maritima",
        "title": "Señalización Marítima y Fluvial — DIMAR",
        "type": "dataset",
        "domains": ["oceanos_costas"],
        "primary_domain": "oceanos_costas",
        "keywords": [
            "faros", "boyas", "balizas", "ayudas", "navegacion",
            "senalizacion", "maritima", "fluvial", "puertos",
            "canales", "acceso", "seguridad", "maritima",
        ],
        "description": (
            "Catálogo geoespacial de ayudas a la navegación marítima y fluvial en Colombia: "
            "faros, boyas, balizas, enfilaciones y otras señales. "
            "Aplicativo web con visualización geográfica de todas las ayudas activas. "
            "Esquema ASEM de SIGDIMAR."
        ),
        "access": {
            "method": "portal",
            "url": "https://www.dimar.mil.co/senalizacion-maritima",
        },
        "attribution": (
            "Dirección General Marítima de Colombia (DIMAR). "
            "Señalización Marítima y Fluvial. "
            "Consultado [fecha]. Disponible en: https://www.dimar.mil.co"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
    "dimar:cecoldodigital": {
        "resource_id": "dimar:cecoldodigital",
        "title": "Cecoldo — Repositorio Digital de DIMAR",
        "type": "repository",
        "domains": ["oceanos_costas", "biodiversidad", "clima"],
        "primary_domain": "oceanos_costas",
        "keywords": [
            "repositorio", "digital", "datos", "oceanograficos",
            "meteorologicos", "mareas", "oleaje", "clima", "maritimo",
            "investigacion", "cientifica", "documentos", "historicos",
        ],
        "description": (
            "Centro Colombiano de Datos Oceanográficos (Cecoldo). "
            "Repositorio institucional con datos primarios de investigación marina, "
            "atlas oceanográficos, climatología marina, series históricas de boyas, "
            "mareógrafos y estaciones meteorológicas costeras. "
            "Acceso abierto bajo política de datos DIMAR (Res. 1751/2021)."
        ),
        "access": {
            "method": "download",
            "url": "https://cecoldodigital.dimar.mil.co",
        },
        "attribution": (
            "Dirección General Marítima de Colombia (DIMAR). "
            "Cecoldo — Centro Colombiano de Datos Oceanográficos. "
            "Consultado [fecha]. Disponible en: https://cecoldodigital.dimar.mil.co"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
    "dimar:ide-maritima": {
        "resource_id": "dimar:ide-maritima",
        "title": "IDE Marítima, Fluvial y Costera de Colombia",
        "type": "platform",
        "domains": ["oceanos_costas", "hidrologia"],
        "primary_domain": "oceanos_costas",
        "keywords": [
            "ide", "infraestructura", "datos", "espaciales", "maritima",
            "fluvial", "costera", "wms", "wfs", "wcs", "wmts",
            "geoservicios", "interoperabilidad", "ogc", "metadatos",
        ],
        "description": (
            "Infraestructura de Datos Espaciales Marítima, Fluvial y Costera de Colombia "
            "liderada por DIMAR. Ofrece servicios WMS, WFS, WCS y WMTS con datos de "
            "cartografía náutica, batimetría, litorales, oceanografía y señalización marítima. "
            "Implementada con Spatial Fusion Enterprise sobre ArcGIS."
        ),
        "access": {
            "method": "ogc",
            "url": "https://litorales-dimar.hub.arcgis.com",
        },
        "attribution": (
            "Dirección General Marítima de Colombia (DIMAR). "
            "IDE Marítima, Fluvial y Costera. "
            "Consultado [fecha]. Disponible en: https://litorales-dimar.hub.arcgis.com"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
}


class DimarConnector(BaseConnector):
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
                    "Dirección General Marítima de Colombia (DIMAR). "
                    "Consultado [fecha]. Disponible en: https://www.dimar.mil.co"
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
