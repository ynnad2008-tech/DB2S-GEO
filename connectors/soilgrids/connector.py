"""
Conector SoilGrids — ISRIC World Soil Information.

Metadatos curados humanamente. Read-only. Sin descarga ni ejecución remota.
SoilGrids es el sistema global de mapeo digital de suelos a 250m de resolución.
Provee propiedades físicas y químicas del suelo para modelación ambiental,
agrícola, hidrológica y de cambio climático.
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

SOURCE_ID = "soilgrids"
INSTITUTION = "ISRIC — World Soil Information / SoilGrids"
HOMEPAGE = "https://soilgrids.org"
LICENSE = "CC BY 4.0 / Datos abiertos con atribución a ISRIC"

_RESOURCES: dict[str, dict[str, Any]] = {
    "soilgrids:properties": {
        "resource_id": "soilgrids:properties",
        "title": "Propiedades del Suelo — SoilGrids 250m v2.0",
        "type": "dataset",
        "domains": ["suelos", "agricultura", "clima"],
        "primary_domain": "suelos",
        "keywords": [
            "suelos", "propiedades", "fisicas", "quimicas", "carbono",
            "organico", "ph", "textura", "arena", "limo", "arcilla",
            "densidad", "aparente", "nitrogeno", "cec", "capacidad",
            "intercambio", "cationico", "isric", "250m", "global",
        ],
        "description": (
            "Mapas digitales de propiedades del suelo a 250m de resolución para "
            "todo el planeta. Variables: carbono orgánico (SOC), pH en agua, "
            "fracciones texturales (arena, limo, arcilla), densidad aparente, "
            "nitrógeno total, capacidad de intercambio catiónico (CEC). "
            "6 profundidades estándar (0-5cm a 100-200cm). "
            "Basado en WoSIS (World Soil Information Service) con >200,000 perfiles. "
            "Esencial para modelación de cultivos, hidrología y carbono del suelo."
        ),
        "access": {
            "method": "ogc",
            "url": "https://maps.isric.org",
        },
        "attribution": (
            "Poggio, L. et al. (2021). SoilGrids 2.0: producing soil information "
            "for the globe with quantified spatial uncertainty. SOIL, 7, 217-240. "
            "ISRIC — World Soil Information. Datos accedidos via https://soilgrids.org"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
    "soilgrids:wcs": {
        "resource_id": "soilgrids:wcs",
        "title": "Servicio WCS — SoilGrids (Web Coverage Service)",
        "type": "api",
        "domains": ["suelos"],
        "primary_domain": "suelos",
        "keywords": [
            "wcs", "geoservicio", "cobertura", "raster", "geotiff",
            "soilgrids", "suelos", "ogc", "web", "coverage",
            "service", "descarga", "programatica",
        ],
        "description": (
            "Servicio WCS (Web Coverage Service) estándar OGC para descarga "
            "programática de capas de suelo SoilGrids. Permite consultar "
            "propiedades del suelo por bounding box, profundidad y variable. "
            "Formatos: GeoTIFF, NetCDF. Cliente recomendado: QGIS, Python (owslib). "
            "Endpoint: https://maps.isric.org/mapserv?map=/map..."
        ),
        "access": {
            "method": "ogc",
            "url": "https://maps.isric.org",
        },
        "attribution": (
            "ISRIC — World Soil Information. SoilGrids WCS. "
            "Consultado [fecha]. Disponible en: https://soilgrids.org"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
    "soilgrids:rest": {
        "resource_id": "soilgrids:rest",
        "title": "API REST — SoilGrids (consultas puntuales y polígonos)",
        "type": "api",
        "domains": ["suelos"],
        "primary_domain": "suelos",
        "keywords": [
            "api", "rest", "json", "consulta", "puntual", "latitud",
            "longitud", "profundidad", "propiedades", "suelo",
            "poligono", "geojson", "soilgrids", "isric",
        ],
        "description": (
            "API REST para consulta de propiedades del suelo por coordenadas "
            "o polígonos. Retorna valores de propiedades físicas y químicas "
            "en formato JSON para cualquier ubicación del planeta. "
            "Soporta consultas puntuales (lat/lon) y extracción por polígonos "
            "o áreas definidas en GeoJSON. Ideal para integración con scripts y modelos."
        ),
        "access": {
            "method": "rest",
            "url": "https://rest.isric.org/soilgrids/v2.0/docs",
        },
        "attribution": (
            "ISRIC — World Information. SoilGrids REST API. "
            "Consultado [fecha]. Disponible en: https://rest.isric.org"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
    "soilgrids:hydrology": {
        "resource_id": "soilgrids:hydrology",
        "title": "Parámetros Hidrológicos del Suelo — SoilGrids",
        "type": "dataset",
        "domains": ["suelos", "hidrologia", "clima"],
        "primary_domain": "hidrologia",
        "keywords": [
            "hidrologia", "suelo", "infiltracion", "conductividad",
            "hidraulica", "saturacion", "curva", "numero", "cn",
            "escorrentia", "agua", "disponible", "capacidad", "campo",
            "marchitez", "grupo", "hidrologico",
        ],
        "description": (
            "Parámetros hidrológicos del suelo derivados de SoilGrids: conductividad "
            "hidráulica saturada (Ksat), capacidad de agua disponible (AWC), "
            "contenido de agua a capacidad de campo y punto de marchitez permanente. "
            "Base para: grupos hidrológicos de suelo (HSG), Curve Number (CN), "
            "modelación precipitación-escorrentía, balance hídrico e irrigación. "
            "6 profundidades estándar, 250m de resolución."
        ),
        "access": {
            "method": "ogc",
            "url": "https://maps.isric.org",
        },
        "attribution": (
            "Turek, M.E. et al. (2023). Global mapping of soil saturated hydraulic "
            "conductivity. ISRIC. Datos accedidos via https://soilgrids.org"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
    "soilgrids:uncertainty": {
        "resource_id": "soilgrids:uncertainty",
        "title": "Mapas de Incertidumbre — SoilGrids",
        "type": "dataset",
        "domains": ["suelos"],
        "primary_domain": "suelos",
        "keywords": [
            "incertidumbre", "error", "cuantiles", "intervalos",
            "confianza", "prediccion", "modelo", "machine", "learning",
            "validacion", "soilgrids", "250m",
        ],
        "description": (
            "Mapas de incertidumbre asociados a cada propiedad del suelo: "
            "intervalos de confianza (5%, 50%, 95%), error estándar y "
            "cuantiles de predicción. Permite evaluar la confiabilidad de "
            "las estimaciones de SoilGrids para cada ubicación. "
            "Importante: la incertidumbre es mayor en regiones tropicales "
            "con pocos perfiles de suelo (Amazonia, Orinoquia colombiana)."
        ),
        "access": {
            "method": "ogc",
            "url": "https://maps.isric.org",
        },
        "attribution": (
            "ISRIC — World Soil Information. SoilGrids Uncertainty Maps. "
            "Consultado [fecha]. Disponible en: https://soilgrids.org"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
}


class SoilgridsConnector(BaseConnector):
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
                    "ISRIC — World Soil Information. SoilGrids 2.0. "
                    "Consultado [fecha]. Disponible en: https://soilgrids.org"
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
