from __future__ import annotations

from typing import Any

INITIAL_DOMAINS: dict[str, dict[str, Any]] = {
    "clima": {
        "domain_id": "clima",
        "label": "Clima",
        "description": "Precipitación, temperatura, humedad y productos climáticos.",
    },
    "hidrologia": {
        "domain_id": "hidrologia",
        "label": "Hidrología",
        "description": "Cuencas, caudales, niveles e información hidrológica.",
    },
    "oceanos_costas": {
        "domain_id": "oceanos_costas",
        "label": "Océanos y costas",
        "description": "Ambientes marinos, costeros y ecosistemas asociados.",
    },
    "suelos": {
        "domain_id": "suelos",
        "label": "Suelos",
        "description": "Propiedades edáficas y cartografía de suelos.",
    },
    "geologia": {
        "domain_id": "geologia",
        "label": "Geología",
        "description": "Geología, geomorfología, geodesia, vulcanología y riesgos geológicos.",
    },
    "biodiversidad": {
        "domain_id": "biodiversidad",
        "label": "Biodiversidad",
        "description": "Especies, ocurrencias, taxonomía, hábitats y conservación.",
    },
    "agricultura": {
        "domain_id": "agricultura",
        "label": "Agricultura",
        "description": "Producción agropecuaria, uso de la tierra y seguridad alimentaria.",
    },
    "riesgo": {
        "domain_id": "riesgo",
        "label": "Riesgo",
        "description": "Gestión del riesgo, amenazas, desastres y vulnerabilidad social.",
    },
    "cartografia_base": {
        "domain_id": "cartografia_base",
        "label": "Cartografía base",
        "description": "Cartografía base, referencias geodésicas y marcos de referencia.",
    },
    "catastro": {
        "domain_id": "catastro",
        "label": "Catastro",
        "description": "Catastro multipropósito, predios y avalúos catastrales.",
    },
    "ordenamiento": {
        "domain_id": "ordenamiento",
        "label": "Ordenamiento territorial",
        "description": "Ordenamiento territorial, planes de ordenamiento y zonificación ambiental.",
    },
    "infraestructura": {
        "domain_id": "infraestructura",
        "label": "Infraestructura",
        "description": "Infraestructura de transporte, energía, minería, hidrocarburos, servicios públicos y licenciamiento ambiental.",
    },
    "poblacion": {
        "domain_id": "poblacion",
        "label": "Población",
        "description": "Demografía espacial, densidad y estructuras poblacionales.",
    },
    "economia": {
        "domain_id": "economia",
        "label": "Economía",
        "description": "Indicadores económicos, finanzas, presupuestos y desarrollo regional.",
    },
    "observacion_tierra": {
        "domain_id": "observacion_tierra",
        "label": "Observación de la Tierra",
        "description": "Imágenes satelitales, sensores remotos y catálogos EO.",
    },
}


def list_domains() -> list[dict[str, Any]]:
    return [dict(v) for v in INITIAL_DOMAINS.values()]


def get_domain(domain_id: str) -> dict[str, Any] | None:
    key = domain_id.strip().lower()
    payload = INITIAL_DOMAINS.get(key)
    return dict(payload) if payload else None


def is_known_domain(domain_id: str) -> bool:
    return domain_id.strip().lower() in INITIAL_DOMAINS
