"""
Conector eBird — Cornell Lab of Ornithology.

Metadatos curados humanamente. Read-only. Sin descarga ni ejecución remota.
eBird es la plataforma de ciencia ciudadana de aves más grande del mundo.
Para Colombia ofrece millones de registros de observación, hotspots,
listados regionales y datos de abundancia relativa.
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

SOURCE_ID = "ebird"
INSTITUTION = "Cornell Lab of Ornithology / eBird"
HOMEPAGE = "https://ebird.org/colombia"
LICENSE = "CC BY 4.0 / Datos abiertos con atribución (términos de uso eBird)"

_RESOURCES: dict[str, dict[str, Any]] = {
    "ebird:observations": {
        "resource_id": "ebird:observations",
        "title": "Registros de Observación — eBird Colombia",
        "type": "dataset",
        "domains": ["biodiversidad"],
        "primary_domain": "biodiversidad",
        "keywords": [
            "aves", "pajaros", "observaciones", "checklists", "ebird",
            "ciencia", "ciudadana", "cornell", "ornitologia", "registros",
            "visuales", "auditivos", "colombia", "especies", "listados",
        ],
        "description": (
            "Base de datos global de observaciones de aves con millones de registros "
            "para Colombia (el país con mayor diversidad de aves del mundo: ~1,966 spp). "
            "Cada registro incluye: especie, ubicación, fecha, observador, esfuerzo "
            "de muestreo y evidencias (fotos/audio). Ciencia ciudadana validada por "
            "revisores regionales expertos. API pública y descargas por especie/región."
        ),
        "access": {
            "method": "rest",
            "url": "https://api.ebird.org/v2/data/obs",
        },
        "attribution": (
            "eBird. Cornell Lab of Ornithology. "
            "eBird Basic Dataset. Version: EBD_relColombia. "
            "Consultado [fecha]. Disponible en: https://ebird.org/colombia"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
    "ebird:hotspots": {
        "resource_id": "ebird:hotspots",
        "title": "Hotspots de Observación de Aves — eBird Colombia",
        "type": "dataset",
        "domains": ["biodiversidad"],
        "primary_domain": "biodiversidad",
        "keywords": [
            "hotspots", "sitios", "observacion", "aves", "localidades",
            "ebird", "avistamiento", "turismo", "ornitologia",
            "colombia", "region", "listados", "especies",
        ],
        "description": (
            "Directorio geoespacial de sitios de observación de aves (hotspots) "
            "en Colombia. Cada hotspot incluye: ubicación GPS, lista de especies "
            "registradas, número de listados, fotos y rankings regionales. "
            "Cientos de hotspots desde La Guajira hasta Amazonas."
        ),
        "access": {
            "method": "rest",
            "url": "https://api.ebird.org/v2/ref/hotspot",
        },
        "attribution": (
            "eBird. Cornell Lab of Ornithology. "
            "eBird Hotspots. "
            "Consultado [fecha]. Disponible en: https://ebird.org/colombia"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
    "ebird:status-trends": {
        "resource_id": "ebird:status-trends",
        "title": "eBird Status & Trends — Abundancia Relativa y Distribución",
        "type": "dataset",
        "domains": ["biodiversidad", "observacion_tierra"],
        "primary_domain": "biodiversidad",
        "keywords": [
            "abundancia", "relativa", "distribucion", "modelacion",
            "estacional", "migracion", "habitat", "poblacion",
            "tendencias", "aves", "conservacion", "mapas", "raster",
        ],
        "description": (
            "Modelos de abundancia relativa y distribución de especies de aves "
            "basados en datos de eBird. Mapas semanales de abundancia a 3 km de "
            "resolución. Incluye trayectorias de migración, tendencias poblacionales "
            "y predicciones de hábitat para cientos de especies. "
            "Herramienta crítica para planificación de conservación en Colombia."
        ),
        "access": {
            "method": "download",
            "url": "https://science.ebird.org/en/status-and-trends",
        },
        "attribution": (
            "Fink, D. et al. eBird Status & Trends. Cornell Lab of Ornithology. "
            "Consultado [fecha]. Disponible en: https://science.ebird.org"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
    "ebird:macauley": {
        "resource_id": "ebird:macauley",
        "title": "Macaulay Library — Archivo Multimedia de Aves",
        "type": "repository",
        "domains": ["biodiversidad"],
        "primary_domain": "biodiversidad",
        "keywords": [
            "macaulay", "biblioteca", "multimedia", "fotos", "audio",
            "video", "cantos", "aves", "especimenes", "archivo",
            "historico", "documentacion", "colombia",
        ],
        "description": (
            "Archivo multimedia de sonidos, fotos y videos de aves más grande "
            "del mundo. Extensa colección de grabaciones de cantos y llamados "
            "de aves colombianas, fotografías de especímenes y videos documentales. "
            "Esencial para identificación acústica, estudios de bioacústica y "
            "documentación de biodiversidad colombiana."
        ),
        "access": {
            "method": "portal",
            "url": "https://macaulaylibrary.org",
        },
        "attribution": (
            "Macaulay Library. Cornell Lab of Ornithology. "
            "Consultado [fecha]. Disponible en: https://macaulaylibrary.org"
        ),
        "status": "active",
        "curated_at": today_iso(),
    },
}


class EbirdConnector(BaseConnector):
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
                    "eBird. Cornell Lab of Ornithology. "
                    "Consultado [fecha]. Disponible en: https://ebird.org/colombia"
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
