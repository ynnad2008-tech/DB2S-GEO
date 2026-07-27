"""
Conector Global Forest Watch (GFW) — World Resources Institute.

Metadatos curados humanamente. Read-only. Sin descarga ni ejecución remota.
Principio de Curaduría Humana + Attribution & Citation Policy.

GFW es la plataforma líder mundial de monitoreo de bosques.
Para Colombia ofrece: cobertura forestal, pérdida anual, alertas GLAD-S2,
alertas RADD, capa integrada de deforestación y análisis de concesiones.
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

SOURCE_ID = "global-forest-watch"
INSTITUTION = "World Resources Institute (WRI) / Global Forest Watch"
HOMEPAGE = "https://www.globalforestwatch.org"
LICENSE = "CC BY 4.0 / Datos abiertos con atribución"

_RESOURCES: dict[str, dict[str, Any]] = {
    "global-forest-watch:tree-cover-loss": {
        "resource_id": "global-forest-watch:tree-cover-loss",
        "title": "Pérdida de Cobertura Arbórea Anual (Hansen/UMD)",
        "type": "dataset",
        "domains": ["biodiversidad", "observacion_tierra"],
        "primary_domain": "observacion_tierra",
        "keywords": [
            "bosques", "deforestacion", "cobertura", "arborea", "perdida",
            "hansen", "landsat", "30m", "global", "anual", "2001",
            "treecover", "lossyear", "colombia",
        ],
        "description": (
            "Mapa global de pérdida de cobertura arbórea anual (2001-presente) "
            "derivado de Landsat a 30m de resolución. Variables: treecover2000, "
            "lossyear, gain, datamask. GFW reporta ~84 Mha de bosques en Colombia. "
            "Actualización anual. Datos de Hansen/UMD/Google/USGS/NASA."
        ),
        "access": {
            "method": "download",
            "url": "https://data.globalforestwatch.org",
        },
        "attribution": (
            "Hansen, M.C. et al. (2013). High-Resolution Global Maps of "
            "21st-Century Forest Cover Change. Science, 342, 850-853. "
            "Datos accedidos via Global Forest Watch. www.globalforestwatch.org"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
    "global-forest-watch:glad-alerts": {
        "resource_id": "global-forest-watch:glad-alerts",
        "title": "Alertas GLAD-S2 — Deforestación en tiempo casi real (Sentinel-2, 10m)",
        "type": "alert",
        "domains": ["biodiversidad", "observacion_tierra", "riesgo"],
        "primary_domain": "biodiversidad",
        "keywords": [
            "alertas", "deforestacion", "glad", "sentinel-2", "10m",
            "tiempo", "real", "deteccion", "temprana", "semanal",
            "amazonia", "colombia", "bosques", "perdida",
        ],
        "description": (
            "Sistema de alertas tempranas de deforestación basado en imágenes "
            "Sentinel-2 a 10m de resolución. Actualización cada 5 días para la "
            "cuenca amazónica. Detecta cambios en cobertura forestal en tiempo "
            "casi real. Complementa las alertas GLAD-L (Landsat 30m) y RADD (radar)."
        ),
        "access": {
            "method": "download",
            "url": "https://www.globalforestwatch.org/map",
        },
        "attribution": (
            "Global Land Analysis & Discovery (GLAD). University of Maryland. "
            "Alertas GLAD-S2. Datos accedidos via Global Forest Watch. "
            "www.globalforestwatch.org"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
    "global-forest-watch:radd-alerts": {
        "resource_id": "global-forest-watch:radd-alerts",
        "title": "Alertas RADD — Deforestación por radar (Sentinel-1, 10m)",
        "type": "alert",
        "domains": ["biodiversidad", "observacion_tierra", "riesgo"],
        "primary_domain": "biodiversidad",
        "keywords": [
            "radd", "radar", "sentinel-1", "10m", "deforestacion",
            "alertas", "nubes", "tropico", "humedo", "colombia",
            "semanal", "monitoreo", "bosques",
        ],
        "description": (
            "Sistema de alertas de deforestación basado en radar Sentinel-1 a 10m. "
            "Penetra nubes — ideal para zonas tropicales húmedas con alta nubosidad "
            "como el Pacífico colombiano y Amazonia. Actualización semanal. "
            "Desarrollado por Wageningen University."
        ),
        "access": {
            "method": "download",
            "url": "https://www.globalforestwatch.org/map",
        },
        "attribution": (
            "Reiche, J. et al. Wageningen University. "
            "RADD Alert System. Datos accedidos via Global Forest Watch. "
            "www.globalforestwatch.org"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
    "global-forest-watch:integrated-alerts": {
        "resource_id": "global-forest-watch:integrated-alerts",
        "title": "Capa Integrada de Alertas de Deforestación (GLAD + RADD)",
        "type": "alert",
        "domains": ["biodiversidad", "observacion_tierra"],
        "primary_domain": "biodiversidad",
        "keywords": [
            "integrada", "combinada", "glad", "radd", "alertas",
            "deforestacion", "consolidada", "rapida", "confiable",
            "colombia", "monitoreo", "diaria",
        ],
        "description": (
            "Capa que combina las alertas GLAD-S2, GLAD-L y RADD en un solo "
            "producto integrado para mayor rapidez y confianza en la detección. "
            "Actualización diaria. Para Colombia detectó ~728.000 ha de pérdida "
            "de cobertura arbórea en 2021-2023."
        ),
        "access": {
            "method": "portal",
            "url": "https://www.globalforestwatch.org/map",
        },
        "attribution": (
            "Global Forest Watch (GFW). World Resources Institute. "
            "Integrated Deforestation Alerts. "
            "Consultado [fecha]. Disponible en: www.globalforestwatch.org"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
    "global-forest-watch:climate": {
        "resource_id": "global-forest-watch:climate",
        "title": "GFW Climate — Carbono Forestal y Emisiones",
        "type": "dataset",
        "domains": ["biodiversidad", "clima", "observacion_tierra"],
        "primary_domain": "clima",
        "keywords": [
            "carbono", "forestal", "emisiones", "co2", "biomasa",
            "redd", "stock", "flujos", "clima", "mitigacion",
            "colombia", "sumideros", "dosel", "altura",
        ],
        "description": (
            "Datos de carbono forestal: densidad de carbono en biomasa aérea (Mg/ha), "
            "flujos de emisiones de CO2 por deforestación, altura de dosel. "
            "Insumo crítico para REDD+, contabilidad de carbono y NDC de Colombia. "
            "Resolución 30m, cobertura global con detalle para el trópico."
        ),
        "access": {
            "method": "download",
            "url": "https://climate.globalforestwatch.org",
        },
        "attribution": (
            "Global Forest Watch Climate. World Resources Institute. "
            "Forest Carbon Fluxes and Stocks. "
            "Consultado [fecha]. Disponible en: climate.globalforestwatch.org"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
}


class GlobalForestWatchConnector(BaseConnector):
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
                    "Global Forest Watch. World Resources Institute. "
                    "Consultado [fecha]. Disponible en: www.globalforestwatch.org"
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
