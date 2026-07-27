"""
Conector ASF — Alaska Satellite Facility (NASA DAAC).

Metadatos curados humanamente. Read-only. Sin descarga ni ejecución remota.
ASF distribuye datos SAR globales. Esencial para InSAR y monitoreo en
zonas de alta nubosidad como el Pacífico colombiano y Amazonia.
"""

from __future__ import annotations

from typing import Any

from connectors._curated import (
    filter_resources, find_resource, resource_not_found, today_iso,
)
from connectors.base import BaseConnector
from connectors.models import normalize_source

SOURCE_ID = "asf"
INSTITUTION = "NASA / Alaska Satellite Facility (ASF DAAC)"
HOMEPAGE = "https://asf.alaska.edu"
LICENSE = "NASA open data / acceso abierto con registro gratuito Earthdata"

_RESOURCES: dict[str, dict[str, Any]] = {
    "asf:vertex": {
        "resource_id": "asf:vertex",
        "title": "ASF Vertex — Búsqueda y descarga de datos SAR",
        "type": "portal",
        "domains": ["observacion_tierra", "riesgo"],
        "primary_domain": "observacion_tierra",
        "keywords": ["sar", "radar", "sentinel-1", "alos", "palsar", "uavsar",
                     "insar", "deformacion", "interferometria", "geotiff", "nasa"],
        "description": (
            "Plataforma de búsqueda y descarga de datos SAR de la NASA. "
            "Archivo completo Sentinel-1 (A/B), ALOS PALSAR, UAVSAR. "
            "Ideal para zonas nubosas. Búsqueda por área, fecha y sensor."
        ),
        "access": {"method": "portal", "url": "https://search.asf.alaska.edu"},
        "attribution": "Alaska Satellite Facility (ASF). NASA. https://asf.alaska.edu",
        "status": "active", "curated_at": today_iso(),
    },
    "asf:hyp3": {
        "resource_id": "asf:hyp3",
        "title": "HyP3 — Procesamiento SAR on-demand (InSAR/RTC)",
        "type": "api",
        "domains": ["observacion_tierra", "riesgo"],
        "primary_domain": "observacion_tierra",
        "keywords": ["hyp3", "insar", "rtc", "procesamiento", "on_demand",
                     "deformacion", "terremoto", "volcan", "subsidencia",
                     "sentinel-1", "gama", "desplazamiento"],
        "description": (
            "Procesamiento SAR on-demand en la nube: interferogramas InSAR "
            "y productos RTC de Sentinel-1. Monitoreo de deformación, "
            "subsidencia y actividad volcánica. API y SDK Python."
        ),
        "access": {"method": "api", "url": "https://hyp3-docs.asf.alaska.edu"},
        "attribution": "ASF HyP3. NASA. https://hyp3-docs.asf.alaska.edu",
        "status": "active", "curated_at": today_iso(),
    },
    "asf:opentopography": {
        "resource_id": "asf:opentopography",
        "title": "OpenTopography — DEM de alta resolución",
        "type": "dataset",
        "domains": ["observacion_tierra", "riesgo", "suelos"],
        "primary_domain": "observacion_tierra",
        "keywords": ["topografia", "dem", "lidar", "srtm", "alos", "worlddem",
                     "elevacion", "pendiente", "geomorfologia", "nasa"],
        "description": (
            "Portal de datos topográficos globales: SRTM, ALOS World 3D, "
            "Copernicus DEM y LiDAR. API y descarga. Copatrocinado ASF/NASA."
        ),
        "access": {"method": "portal", "url": "https://opentopography.org"},
        "attribution": "OpenTopography / ASF / NASA. https://opentopography.org",
        "status": "active", "curated_at": today_iso(),
    },
}


class AsfConnector(BaseConnector):
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
        return normalize_source(source_id=self.connector_id,
                                institution=self.institution, homepage=self.homepage,
                                license=self.license, resources=_RESOURCES)

    def describe(self, source_id: str | None = None) -> dict[str, Any]:
        return normalize_source(source_id=self.connector_id,
                                institution=self.institution, homepage=self.homepage,
                                license=self.license, resources=_RESOURCES)

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
                    "citation": "Alaska Satellite Facility (ASF). NASA. https://asf.alaska.edu"}
        resource = find_resource(_RESOURCES, resource_id, self.connector_id)
        if resource is None:
            return resource_not_found(self.connector_id, resource_id)
        return {"source_id": self.connector_id, "resource_id": resource_id,
                "citation": resource.get("attribution", "")}

    def list_resources(self, domain: str | None = None) -> list[dict[str, Any]]:
        return filter_resources(_RESOURCES, domain)

    def get_resource(self, resource_id: str) -> dict[str, Any] | None:
        return find_resource(_RESOURCES, resource_id, self.connector_id)
