"""
Conector INVEMAR — Fase 2 Metadata Engine MVP.

Metadatos curados humanamente. Read-only. Sin descarga ni ejecución remota.
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

SOURCE_ID = "invemar"
INSTITUTION = "Instituto de Investigaciones Marinas y Costeras José Benito Vives de Andréis"
HOMEPAGE = "https://www.invemar.org.co"
LICENSE = "Términos institucionales INVEMAR / datos abiertos cuando apliquen"

_RESOURCES: dict[str, dict[str, Any]] = {
    "invemar:siamexplorer": {
        "resource_id": "invemar:siamexplorer",
        "title": "SiamExplorer — visor oceanográfico (INVEMAR)",
        "type": "portal",
        "domains": ["oceanos_costas"],
        "primary_domain": "oceanos_costas",
        "keywords": [
            "oceanografia",
            "boyas",
            "oleaje",
            "tsm",
            "temperatura",
            "superficial",
            "mar",
            "viento",
            "mareas",
            "nivel",
            "del",
            "mar",
            "corrientes",
            "meteorologia",
            "marina",
            "monitoreo",
            "oceanico",
            "siamexplorer",
            "invemar",
            "colombia",
        ],
        "description": (
            "SiamExplorer: visor operativo de datos oceanográficos y "
            "meteorológicos marinos de INVEMAR. Visualiza boyas, estaciones "
            "meteorológicas marinas, oleaje (altura, dirección, período), "
            "temperatura superficial del mar, viento, nivel del mar, "
            "corrientes y mareas en tiempo real e histórico. "
            "DB2S-GEO solo documenta el acceso; no ejecuta consultas remotas."
        ),
        "spatial_coverage": "Colombia (marino-costero Caribe, Pacífico e insular)",
        "temporal_coverage": "Tiempo real e histórico (según disponibilidad)",
        "formats": ["visor web", "series de tiempo", "descarga CSV"],
        "homepage": "https://www.invemar.org.co",
        "portal_url": "https://siamexplorer.invemar.org.co/",
        "documentation_url": "https://siamexplorer.invemar.org.co/",
        "endpoints": [
            {
                "method": "portal",
                "url": "https://siamexplorer.invemar.org.co/",
                "label": "SiamExplorer — visor oceanográfico INVEMAR",
            },
            {
                "method": "portal",
                "url": "https://www.invemar.org.co/web/invemar/siamexplorer",
                "label": "SiamExplorer (portal institucional)",
            },
        ],
        "access_methods": ["portal"],
        "citation_reference": (
            "INVEMAR. SiamExplorer — visor oceanográfico. "
            "Instituto de Investigaciones Marinas y Costeras "
            "José Benito Vives de Andréis. "
            "https://siamexplorer.invemar.org.co/"
        ),
        "doi": "",
    },
    "invemar:data-hub": {
        "resource_id": "invemar:data-hub",
        "title": "DataHub INVEMAR — catálogo de datos marinos y costeros",
        "type": "portal",
        "domains": ["oceanos_costas", "biodiversidad"],
        "primary_domain": "oceanos_costas",
        "keywords": [
            "datos",
            "hub",
            "catálogo",
            "descarga",
            "oceanografia",
            "marino",
            "costero",
            "biodiversidad",
            "marina",
            "abiertos",
            "invemar",
            "colombia",
        ],
        "description": (
            "DataHub INVEMAR: catálogo centralizado de datos marinos y "
            "costeros de Colombia. Permite búsqueda, visualización y "
            "descarga de conjuntos de datos oceanográficos, pesqueros, "
            "de biodiversidad marina, calidad de agua, ecosistemas "
            "costeros y más. DB2S-GEO solo documenta el acceso; "
            "no descarga conjuntos."
        ),
        "spatial_coverage": "Colombia (marino-costero)",
        "temporal_coverage": "Según conjuntos publicados en el DataHub",
        "formats": ["portal web", "descarga", "API"],
        "homepage": "https://www.invemar.org.co",
        "portal_url": "https://datahub.invemar.org.co/",
        "documentation_url": "https://datahub.invemar.org.co/",
        "endpoints": [
            {
                "method": "portal",
                "url": "https://datahub.invemar.org.co/",
                "label": "DataHub INVEMAR — catálogo de datos",
            },
            {
                "method": "portal",
                "url": "https://www.invemar.org.co/web/invemar/datos",
                "label": "Datos INVEMAR (portal institucional)",
            },
        ],
        "access_methods": ["portal", "api"],
        "citation_reference": (
            "INVEMAR. DataHub — catálogo de datos marinos y costeros. "
            "Instituto de Investigaciones Marinas y Costeras "
            "José Benito Vives de Andréis. "
            "https://datahub.invemar.org.co/"
        ),
        "doi": "",
    },
    "invemar:geovisor": {
        "resource_id": "invemar:geovisor",
        "title": "Geovisor INVEMAR",
        "type": "portal",
        "domains": ["oceanos_costas"],
        "primary_domain": "oceanos_costas",
        "keywords": [
            "oceanos",
            "costas",
            "marino",
            "geovisor",
            "invemar",
        ],
        "description": (
            "Geovisor y acceso cartográfico a información marina y costera "
            "producida o publicada por INVEMAR."
        ),
        "spatial_coverage": "Colombia (marino-costero)",
        "temporal_coverage": "Actualizaciones institucionales",
        "formats": ["servicios web", "mapas"],
        "homepage": HOMEPAGE,
        "portal_url": HOMEPAGE,
        "documentation_url": HOMEPAGE,
        "endpoints": [
            {
                "method": "portal",
                "url": HOMEPAGE,
                "label": "Portal institucional INVEMAR",
            }
        ],
        "access_methods": ["portal", "arcgis"],
        "citation_reference": (
            "INVEMAR. Geovisor e información marina y costera. "
            "Instituto de Investigaciones Marinas y Costeras."
        ),
        "doi": "",
    },
    "invemar:biodiversidad-marina": {
        "resource_id": "invemar:biodiversidad-marina",
        "title": "Biodiversidad marina y costera",
        "type": "dataset",
        "domains": ["oceanos_costas", "biodiversidad"],
        "primary_domain": "oceanos_costas",
        "keywords": [
            "biodiversidad",
            "marino",
            "costero",
            "especies",
            "invemar",
        ],
        "description": (
            "Información y productos sobre biodiversidad marina y costera "
            "bajo responsabilidad de INVEMAR."
        ),
        "spatial_coverage": "Colombia (marino-costero)",
        "temporal_coverage": "Series e inventarios institucionales",
        "formats": ["tablas", "mapas", "reportes"],
        "homepage": HOMEPAGE,
        "portal_url": HOMEPAGE,
        "documentation_url": HOMEPAGE,
        "endpoints": [
            {
                "method": "portal",
                "url": HOMEPAGE,
                "label": "Portal institucional INVEMAR",
            }
        ],
        "access_methods": ["portal"],
        "citation_reference": (
            "INVEMAR. Biodiversidad marina y costera. "
            "Instituto de Investigaciones Marinas y Costeras."
        ),
        "doi": "",
    },
    "invemar:ecosistemas-costeros": {
        "resource_id": "invemar:ecosistemas-costeros",
        "title": "Ecosistemas costeros",
        "type": "dataset",
        "domains": ["oceanos_costas"],
        "primary_domain": "oceanos_costas",
        "keywords": [
            "ecosistemas",
            "manglar",
            "costas",
            "habitat",
            "invemar",
        ],
        "description": (
            "Información sobre ecosistemas costeros (p. ej. manglares y "
            "hábitats asociados) documentada por INVEMAR."
        ),
        "spatial_coverage": "Colombia (zona costera)",
        "temporal_coverage": "Productos institucionales",
        "formats": ["mapas", "reportes"],
        "homepage": HOMEPAGE,
        "portal_url": HOMEPAGE,
        "documentation_url": HOMEPAGE,
        "endpoints": [
            {
                "method": "portal",
                "url": HOMEPAGE,
                "label": "Portal institucional INVEMAR",
            }
        ],
        "access_methods": ["portal"],
        "citation_reference": (
            "INVEMAR. Ecosistemas costeros. "
            "Instituto de Investigaciones Marinas y Costeras."
        ),
        "doi": "",
    },
    "invemar:manglares-colombia": {
        "resource_id": "invemar:manglares-colombia",
        "title": "Manglares de Colombia (INVEMAR)",
        "type": "geoservice",
        "domains": ["oceanos_costas", "biodiversidad"],
        "primary_domain": "oceanos_costas",
        "keywords": [
            "manglar",
            "manglares",
            "carbono",
            "carbono_azul",
            "ecosistema",
            "costero",
            "costas",
            "sigma",
            "arcgis",
            "mapserver",
            "invemar",
            "colombia",
        ],
        "description": (
            "Servicio geoespacial oficial de INVEMAR para la consulta, "
            "visualización y acceso a información sobre los manglares "
            "de Colombia. Apoya procesos de conservación, "
            "planificación costera, biodiversidad, carbono azul "
            "y gestión de ecosistemas marino-costeros."
        ),
        "spatial_coverage": "Colombia (litorales Caribe, Pacífico e insular)",
        "temporal_coverage": "Según publicación institucional del servicio SIGMA",
        "formats": ["ArcGIS REST", "JSON", "GeoJSON (vía query del servicio)"],
        "homepage": "https://sigma.invemar.org.co/geovisor",
        "portal_url": "https://sigma.invemar.org.co/geovisor",
        "documentation_url": (
            "https://gis.invemar.org.co/arcgis/rest/services/"
            "SIGMA/MANGLARES_COLOMBIA/MapServer"
        ),
        "endpoints": [
            {
                "method": "arcgis",
                "url": (
                    "https://gis.invemar.org.co/arcgis/rest/services/"
                    "SIGMA/MANGLARES_COLOMBIA/MapServer"
                ),
                "label": "SIGMA MANGLARES_COLOMBIA MapServer",
            },
            {
                "method": "portal",
                "url": "https://sigma.invemar.org.co/geovisor",
                "label": "Geovisor SIGMA (manglares)",
            },
        ],
        "access_methods": ["arcgis", "portal"],
        "citation_reference": (
            "INVEMAR. Manglares de Colombia. "
            "Instituto de Investigaciones Marinas y Costeras "
            "José Benito Vives de Andréis. "
            "Servicio ArcGIS REST MapServer. "
            "https://gis.invemar.org.co/arcgis/rest/services/"
            "SIGMA/MANGLARES_COLOMBIA/MapServer"
        ),
        "doi": "",
    },
    "invemar:ecorregiones-marinas": {
        "resource_id": "invemar:ecorregiones-marinas",
        "title": "Ecorregiones marinas de Colombia (INVEMAR)",
        "type": "geoservice",
        "domains": ["oceanos_costas", "biodiversidad"],
        "primary_domain": "oceanos_costas",
        "keywords": [
            "ecorregion",
            "ecorregiones",
            "marinas",
            "marino",
            "ecosistemas",
            "marinos",
            "ordenamiento",
            "planificacion",
            "costera",
            "biodiversidad",
            "oceanos",
            "costas",
            "arcgis",
            "featureserver",
            "invemar",
            "colombia",
        ],
        "description": (
            "Servicio geoespacial oficial de INVEMAR para la consulta y "
            "visualización de las ecorregiones marinas de Colombia. "
            "Apoya ordenamiento marino, planificación costera, "
            "gestión de ecosistemas marinos y biodiversidad marina."
        ),
        "spatial_coverage": "Colombia (jurisdicción marina y costera)",
        "temporal_coverage": "Según publicación institucional del servicio",
        "formats": ["ArcGIS REST", "JSON", "GeoJSON (vía query del servicio)"],
        "homepage": "https://geovisorsiam.invemar.org.co/",
        "portal_url": "https://geovisorsiam.invemar.org.co/",
        "documentation_url": (
            "https://gis.invemar.org.co/arcgis/rest/services/"
            "Hosted/Ecorregiones_Marinas_de_Colombia/FeatureServer"
        ),
        "endpoints": [
            {
                "method": "arcgis",
                "url": (
                    "https://gis.invemar.org.co/arcgis/rest/services/"
                    "Hosted/Ecorregiones_Marinas_de_Colombia/FeatureServer"
                ),
                "label": "Ecorregiones_Marinas_de_Colombia FeatureServer",
            },
            {
                "method": "portal",
                "url": "https://geovisorsiam.invemar.org.co/",
                "label": "GeoVisor SIAM INVEMAR",
            },
        ],
        "access_methods": ["arcgis", "portal"],
        "citation_reference": (
            "INVEMAR. Ecorregiones marinas de Colombia. "
            "Instituto de Investigaciones Marinas y Costeras "
            "José Benito Vives de Andréis. "
            "Servicio ArcGIS REST FeatureServer. "
            "https://gis.invemar.org.co/arcgis/rest/services/"
            "Hosted/Ecorregiones_Marinas_de_Colombia/FeatureServer"
        ),
        "doi": "",
    },
    "invemar:siam": {
        "resource_id": "invemar:siam",
        "title": "SIAM — Sistema de Información Ambiental Marina (INVEMAR)",
        "type": "portal",
        "domains": ["oceanos_costas", "biodiversidad"],
        "primary_domain": "oceanos_costas",
        "keywords": [
            "informacion",
            "marina",
            "indicadores",
            "costeros",
            "monitoreo",
            "marino",
            "siam",
            "observatorio",
            "invemar",
            "colombia",
        ],
        "description": (
            "Sistema de Información Ambiental Marina (SIAM) de INVEMAR: "
            "portal e indicadores de información marina y costera, con "
            "acceso al GeoVisor SIAM. Apoya monitoreo marino e indicadores "
            "costeros. DB2S-GEO solo documenta el acceso; no descarga datos."
        ),
        "spatial_coverage": "Colombia (marino-costero)",
        "temporal_coverage": "Actualizaciones institucionales SIAM",
        "formats": ["portal web", "servicios web", "mapas"],
        "homepage": "https://siam.invemar.org.co/",
        "portal_url": "https://siam.invemar.org.co/",
        "documentation_url": "https://siam.invemar.org.co/que-es-siam.html",
        "endpoints": [
            {
                "method": "portal",
                "url": "https://siam.invemar.org.co/",
                "label": "Portal SIAM INVEMAR",
            },
            {
                "method": "portal",
                "url": "https://geovisorsiam.invemar.org.co/",
                "label": "GeoVisor SIAM",
            },
        ],
        "access_methods": ["portal", "arcgis"],
        "citation_reference": (
            "INVEMAR. Sistema de Información Ambiental Marina (SIAM). "
            "Instituto de Investigaciones Marinas y Costeras "
            "José Benito Vives de Andréis. "
            "https://siam.invemar.org.co/"
        ),
        "doi": "",
    },
}


class InvemarConnector(BaseConnector):
    connector_id = SOURCE_ID
    source_name = "INVEMAR"
    version = "1.3.0"

    def identify(self) -> dict[str, Any]:
        return normalize_source(
            source_id=SOURCE_ID,
            source="INVEMAR",
            institution=INSTITUTION,
            country_or_scope="Colombia",
            domains=["oceanos_costas", "biodiversidad"],
            access_methods=["portal", "arcgis"],
            description=(
                "Instituto de investigación marina y costera de Colombia. "
                "Fuente oficial de información oceanográfica, costera y "
                "de biodiversidad marina."
            ),
            homepage=HOMEPAGE,
            license=LICENSE,
            connector_id=self.connector_id,
            version=self.version,
        )

    def discover(self, query: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        summaries = [
            {
                "resource_id": r["resource_id"],
                "title": r["title"],
                "type": r["type"],
                "domains": list(r["domains"]),
                "primary_domain": r.get("primary_domain"),
                "keywords": list(r.get("keywords", [])),
                "description": r["description"],
                "source_id": SOURCE_ID,
            }
            for r in _RESOURCES.values()
        ]
        return filter_resources(summaries, query)

    def describe(self, resource_id: str) -> dict[str, Any]:
        item = find_resource(_RESOURCES, resource_id)
        if not item:
            return resource_not_found(resource_id, SOURCE_ID)
        return {
            "resource_id": item["resource_id"],
            "title": item["title"],
            "type": item["type"],
            "description": item["description"],
            "domains": list(item["domains"]),
            "primary_domain": item.get("primary_domain"),
            "keywords": list(item.get("keywords", [])),
            "spatial_coverage": item["spatial_coverage"],
            "temporal_coverage": item["temporal_coverage"],
            "formats": list(item["formats"]),
            "source_id": SOURCE_ID,
            "institution": INSTITUTION,
            "license": LICENSE,
            "homepage": item["homepage"],
            "access_methods": list(item["access_methods"]),
        }

    def access_info(self, resource_id: str) -> dict[str, Any]:
        item = find_resource(_RESOURCES, resource_id)
        if not item:
            return resource_not_found(resource_id, SOURCE_ID)
        return {
            "resource_id": item["resource_id"],
            "source_id": SOURCE_ID,
            "access_methods": list(item["access_methods"]),
            "endpoints": list(item["endpoints"]),
            "portal_url": item["portal_url"],
            "documentation_url": item["documentation_url"],
            "notes": (
                "DB2S-GEO expone solo metadatos de acceso. "
                "Consulte el portal oficial INVEMAR para datos y productos."
            ),
            "read_only": True,
            "downloads_supported": False,
        }

    def cite(self, resource_id: str) -> dict[str, Any]:
        item = find_resource(_RESOURCES, resource_id)
        if not item:
            return resource_not_found(resource_id, SOURCE_ID)
        accessed = today_iso()
        url = item["homepage"]
        apa = (
            f"INVEMAR. ({accessed[:4]}). {item['title']}. "
            f"{INSTITUTION}. {url}"
        )
        return {
            "source": "INVEMAR",
            "institution": INSTITUTION,
            "reference": item["citation_reference"],
            "url": url,
            "accessed": accessed,
            "apa": apa,
            "doi": item.get("doi") or "",
            "license": LICENSE,
            "resource_id": item["resource_id"],
            "source_id": SOURCE_ID,
        }
