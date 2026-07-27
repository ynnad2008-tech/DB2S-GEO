"""
Conector Copernicus — Programa Europeo de Observación de la Tierra.

Metadatos curados humanamente. Read-only. Climate Data Store (CDS/ERA5),
Atmosphere Monitoring (CAMS) y Sentinel-5P para calidad del aire.
"""

from __future__ import annotations
from typing import Any
from connectors._curated import (
    filter_resources, find_resource, resource_not_found, today_iso,
)
from connectors.base import BaseConnector
from connectors.models import normalize_source

SOURCE_ID = "copernicus"
INSTITUTION = "European Union / Copernicus Programme (ECMWF / ESA / EEA)"
HOMEPAGE = "https://www.copernicus.eu"
LICENSE = "Copernicus open data / acceso gratuito con registro CDS"

_RESOURCES: dict[str, dict[str, Any]] = {
    "copernicus:era5": {
        "resource_id": "copernicus:era5",
        "title": "ERA5 — Reanálisis climático global (CDS)",
        "type": "dataset",
        "domains": ["clima", "hidrologia", "observacion_tierra"],
        "primary_domain": "clima",
        "keywords": ["era5", "reanalisis", "climatico", "ecmwf", "cds",
                     "temperatura", "precipitacion", "viento", "presion",
                     "humedad", "radiacion", "evapotranspiracion", "historico",
                     "horario", "0.25", "global", "netcdf", "grib"],
        "description": (
            "Reanálisis climático global ERA5 del ECMWF. Datos horarios desde 1940 "
            "a 0.25° (~31km). Variables atmosféricas, oceánicas y terrestres. "
            "Acceso vía Climate Data Store (CDS) con API Python (cdsapi). "
            "Estándar de referencia para modelación climática e hidrológica."
        ),
        "access": {"method": "api", "url": "https://cds.climate.copernicus.eu"},
        "attribution": "Hersbach, H. et al. ERA5. ECMWF / Copernicus CDS. https://cds.climate.copernicus.eu",
        "status": "active", "curated_at": today_iso(),
    },
    "copernicus:cams": {
        "resource_id": "copernicus:cams",
        "title": "CAMS — Monitoreo de calidad del aire (Copernicus Atmosphere)",
        "type": "dataset",
        "domains": ["clima", "riesgo"],
        "primary_domain": "clima",
        "keywords": ["cams", "calidad", "aire", "atmosfera", "pm2.5", "pm10",
                     "ozono", "no2", "so2", "co", "aerosoles", "emisiones",
                     "incendios", "polen", "salud", "copernicus", "ecmwf"],
        "description": (
            "Copernicus Atmosphere Monitoring Service. Datos globales y regionales "
            "de calidad del aire: PM2.5, PM10, O3, NO2, SO2, CO, aerosoles. "
            "Pronósticos a 5 días y reanálisis. Monitoreo de incendios forestales "
            "y transporte de humo. Crítico para salud pública y gestión ambiental."
        ),
        "access": {"method": "api", "url": "https://atmosphere.copernicus.eu"},
        "attribution": "CAMS. ECMWF / Copernicus. https://atmosphere.copernicus.eu",
        "status": "active", "curated_at": today_iso(),
    },
    "copernicus:sentinel5p": {
        "resource_id": "copernicus:sentinel5p",
        "title": "Sentinel-5P — Composición atmosférica (TROPOMI)",
        "type": "dataset",
        "domains": ["clima", "observacion_tierra", "riesgo"],
        "primary_domain": "clima",
        "keywords": ["sentinel-5p", "tropomi", "no2", "so2", "co", "ch4",
                     "metano", "ozono", "aerosoles", "columna", "atmosferica",
                     "contaminacion", "satelite", "copernicus", "esa"],
        "description": (
            "Sensor TROPOMI a bordo de Sentinel-5P. Mapeo global diario de "
            "gases traza atmosféricos: NO2, SO2, CO, CH4 (metano), O3, "
            "aerosoles y formaldehído (HCHO). Resolución 7×3.5 km. "
            "Esencial para monitoreo de contaminación urbana e industrial."
        ),
        "access": {"method": "download", "url": "https://s5phub.copernicus.eu"},
        "attribution": "ESA / Copernicus. Sentinel-5P TROPOMI. https://s5phub.copernicus.eu",
        "status": "active", "curated_at": today_iso(),
    },
}


class CopernicusConnector(BaseConnector):
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
                    "citation": "Copernicus Programme. EU/ECMWF/ESA. https://www.copernicus.eu"}
        resource = find_resource(_RESOURCES, resource_id, self.connector_id)
        if resource is None:
            return resource_not_found(self.connector_id, resource_id)
        return {"source_id": self.connector_id, "resource_id": resource_id,
                "citation": resource.get("attribution", "")}

    def list_resources(self, domain: str | None = None) -> list[dict[str, Any]]:
        return filter_resources(_RESOURCES, domain)

    def get_resource(self, resource_id: str) -> dict[str, Any] | None:
        return find_resource(_RESOURCES, resource_id, self.connector_id)
