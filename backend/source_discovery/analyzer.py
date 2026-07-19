"""
Análisis heurístico de URLs — Source Discovery Assistant MVP.

Sin IA / embeddings / LLMs. Solo patrones curados y señales deterministas.
"""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlparse, unquote

# Host → institución probable (curaduría humana).
KNOWN_HOSTS: dict[str, dict[str, str]] = {
    "sgc.gov.co": {
        "institution": "Servicio Geológico Colombiano",
        "institution_short": "SGC",
        "name": "Servicio Geológico Colombiano",
    },
    "ideam.gov.co": {
        "institution": "Instituto de Hidrología, Meteorología y Estudios Ambientales",
        "institution_short": "IDEAM",
        "name": "IDEAM",
    },
    "igac.gov.co": {
        "institution": "Instituto Geográfico Agustín Codazzi",
        "institution_short": "IGAC",
        "name": "IGAC",
    },
    "invemar.org.co": {
        "institution": "Instituto de Investigaciones Marinas y Costeras",
        "institution_short": "INVEMAR",
        "name": "INVEMAR",
    },
    "dane.gov.co": {
        "institution": "Departamento Administrativo Nacional de Estadística",
        "institution_short": "DANE",
        "name": "DANE",
    },
    "gbif.org": {
        "institution": "Global Biodiversity Information Facility",
        "institution_short": "GBIF",
        "name": "GBIF",
    },
    "fao.org": {
        "institution": "Food and Agriculture Organization of the United Nations",
        "institution_short": "FAO",
        "name": "FAOSTAT / FAO",
    },
    "worldpop.org": {
        "institution": "WorldPop",
        "institution_short": "WorldPop",
        "name": "WorldPop",
    },
    "earthengine.google.com": {
        "institution": "Google Earth Engine",
        "institution_short": "GEE",
        "name": "Google Earth Engine",
    },
    "datos.gov.co": {
        "institution": "Gobierno de Colombia — Datos Abiertos",
        "institution_short": "datos.gov.co",
        "name": "Portal de Datos Abiertos de Colombia",
    },
}

# Palabras en path/host → dominios temáticos (taxonomía Metadata + ampliaciones).
DOMAIN_HINTS: dict[str, list[str]] = {
    "clima": ["clima"],
    "climate": ["clima"],
    "meteo": ["clima"],
    "precipit": ["clima", "hidrologia"],
    "hidro": ["hidrologia"],
    "hydro": ["hidrologia"],
    "cuenca": ["hidrologia"],
    "biodivers": ["biodiversidad"],
    "species": ["biodiversidad"],
    "occurrence": ["biodiversidad"],
    "marino": ["oceanos_costas"],
    "ocean": ["oceanos_costas"],
    "costa": ["oceanos_costas"],
    "manglar": ["oceanos_costas"],
    "suelo": ["suelos"],
    "soil": ["suelos"],
    "agric": ["agricultura"],
    "agro": ["agricultura"],
    "poblacion": ["poblacion"],
    "population": ["poblacion"],
    "demograf": ["poblacion"],
    "satelit": ["observacion_tierra"],
    "sentinel": ["observacion_tierra"],
    "landsat": ["observacion_tierra"],
    "raster": ["observacion_tierra"],
    "geolog": ["geologia"],
    "riesgo": ["riesgo"],
    "amenaza": ["riesgo"],
    "sismo": ["geologia", "riesgo"],
    "volcan": ["geologia", "riesgo"],
    "fallas": ["geologia"],
    "simma": ["geologia", "riesgo"],
    "amenazasismica": ["geologia", "riesgo"],
    "capastematicas": ["geologia"],
    "capasgeo": ["clima", "hidrologia", "observacion_tierra"],
    "cneideam": ["clima", "hidrologia"],
    "geovisor": ["observacion_tierra"],
}

SOURCE_TYPE_PATTERNS: list[tuple[str, str, list[str]]] = [
    # (regex, source_type, access_methods)
    (r"featureserver", "ArcGIS REST FeatureServer", ["arcgis", "api"]),
    (r"mapserver", "ArcGIS REST MapServer", ["arcgis", "api"]),
    (r"imageserver", "ArcGIS REST ImageServer", ["arcgis", "api"]),
    (r"/rest/services", "ArcGIS REST", ["arcgis", "api"]),
    (r"/arcgis/", "ArcGIS REST", ["arcgis", "api"]),
    (r"/stac", "STAC", ["stac", "api"]),
    (r"stac\.|stac-", "STAC", ["stac", "api"]),
    (r"[?&]service=wms|\bwms\b|/wms", "WMS", ["ogc", "wms"]),
    (r"[?&]service=wfs|\bwfs\b|/wfs", "WFS", ["ogc", "wfs"]),
    (r"[?&]service=wcs|\bwcs\b|/wcs", "WCS", ["ogc", "wcs"]),
    (r"/api/|/v1/|/v2/|\.json(\?|$)", "API JSON", ["api"]),
    (r"geonetwork|ckan|socrata|opendata", "Portal / Catálogo", ["portal", "api"]),
    (r"capasgeo|capas_geo|/capas/|geovisor|geoportal", "Portal de capas geoespaciales", ["portal", "arcgis"]),
    (r"download|/datos|/data/", "Repositorio de descargas", ["portal", "download"]),
]


def analyze_url(url: str) -> dict[str, Any]:
    """Analiza una URL y produce señales estructuradas (sin red)."""
    raw = (url or "").strip()
    if not raw:
        return {"ok": False, "error": "URL vacía"}

    if not re.match(r"^https?://", raw, re.I):
        raw = "https://" + raw

    parsed = urlparse(raw)
    host = (parsed.hostname or "").lower()
    path = unquote(parsed.path or "")
    query = unquote(parsed.query or "")
    full = f"{host}{path}?{query}".lower()

    source_type, access_methods = _detect_source_type(full)
    host_info = _match_host(host)
    domains = _infer_domains(full)
    name = host_info.get("name") or _guess_name_from_path(host, path)
    institution = host_info.get("institution") or _guess_institution(host)
    institution_short = host_info.get("institution_short") or institution

    potential_resources = _guess_resources(path, source_type)
    signals = {
        "host_known": bool(host_info),
        "source_type_detected": source_type != "Desconocido",
        "domains_inferred": bool(domains),
        "https": parsed.scheme == "https",
        "path_informative": len(path) > 1,
    }
    confidence = _confidence(signals)

    return {
        "ok": True,
        "url": raw,
        "host": host,
        "path": path,
        "status": "candidate_source",
        "name": name,
        "source_type": source_type,
        "institution": institution_short if len(institution_short) <= 40 else institution,
        "institution_full": institution,
        "domains": domains,
        "access_methods": access_methods,
        "potential_resources": potential_resources,
        "confidence": confidence,
        "signals": signals,
        "curation": "human_required",
        "auto_applied": False,
        "catalog_modified": False,
        "connector_created": False,
    }


def _detect_source_type(full: str) -> tuple[str, list[str]]:
    for pattern, source_type, methods in SOURCE_TYPE_PATTERNS:
        if re.search(pattern, full, re.I):
            return source_type, list(methods)
    if full.endswith("/") or "/" not in full.split("?", 1)[0].rstrip("/"):
        return "Portal institucional", ["portal"]
    return "Desconocido", ["portal"]


def _match_host(host: str) -> dict[str, str]:
    for known, info in KNOWN_HOSTS.items():
        if host == known or host.endswith("." + known):
            return dict(info)
    return {}


def _infer_domains(full: str) -> list[str]:
    found: list[str] = []
    for hint, domains in DOMAIN_HINTS.items():
        if hint in full:
            for d in domains:
                if d not in found:
                    found.append(d)
    return found


def _guess_name_from_path(host: str, path: str) -> str:
    parts = [p for p in path.split("/") if p and p.lower() not in {"rest", "services", "api", "v1", "v2"}]
    if parts:
        # Preferir último segmento significativo (p. ej. nombre del servicio)
        label = parts[-1].replace("_", " ").replace("-", " ")
        if label.lower() in {"featureserver", "mapserver", "imageserver"}:
            label = parts[-2].replace("_", " ").replace("-", " ") if len(parts) > 1 else host
        return label.title()
    return host


def _guess_institution(host: str) -> str:
    # quitar www. y TLD comunes
    h = host[4:] if host.startswith("www.") else host
    base = h.split(".")[0]
    return base.upper() if len(base) <= 6 else base.replace("-", " ").title()


def _guess_resources(path: str, source_type: str) -> list[dict[str, str]]:
    parts = [p for p in path.split("/") if p]
    resources: list[dict[str, str]] = []
    if "FeatureServer" in path or "MapServer" in path or "ImageServer" in path:
        # .../services/Folder/ServiceName/FeatureServer
        for i, part in enumerate(parts):
            if part.lower() in {"featureserver", "mapserver", "imageserver"} and i > 0:
                resources.append(
                    {
                        "candidate_id": parts[i - 1],
                        "title": parts[i - 1].replace("_", " "),
                        "type": source_type,
                    }
                )
                break
    if not resources and parts:
        resources.append(
            {
                "candidate_id": parts[-1],
                "title": parts[-1].replace("_", " "),
                "type": source_type,
            }
        )
    return resources


def _confidence(signals: dict[str, bool]) -> float:
    weights = {
        "host_known": 0.35,
        "source_type_detected": 0.30,
        "domains_inferred": 0.15,
        "https": 0.05,
        "path_informative": 0.15,
    }
    score = sum(weights[k] for k, v in signals.items() if v and k in weights)
    # Desconocido tipado baja confianza
    if not signals.get("source_type_detected"):
        score = min(score, 0.45)
    return round(min(0.99, max(0.05, score)), 2)
