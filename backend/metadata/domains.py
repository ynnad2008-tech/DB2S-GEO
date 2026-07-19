"""
Dominios temáticos iniciales — Metadata Engine (Fase 2).

Taxonomía curada y ampliable. No inventar dominios fuera de este registro
sin curaduría humana.
"""

from __future__ import annotations

from typing import Any

# Dominios iniciales (FASE 2) — ampliables en fases posteriores.
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
    "biodiversidad": {
        "domain_id": "biodiversidad",
        "label": "Biodiversidad",
        "description": "Especies, ocurrencias, taxonomía y hábitats.",
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
    "agricultura": {
        "domain_id": "agricultura",
        "label": "Agricultura",
        "description": "Producción agropecuaria, uso de la tierra y seguridad alimentaria.",
    },
    "poblacion": {
        "domain_id": "poblacion",
        "label": "Población",
        "description": "Demografía espacial, densidad y estructuras poblacionales.",
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
