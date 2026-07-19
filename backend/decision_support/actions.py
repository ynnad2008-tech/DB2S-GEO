"""
Rutas de acción curadas — Decision Support MVP.

Plantillas que convierten una necesidad en varias rutas complementarias
(qué hacer / dónde / fuente / recursos / por qué).
"""

from __future__ import annotations

from typing import Any

# Categorías de acción (API id → etiqueta UI)
ACTION_CATEGORIES: dict[str, str] = {
    "descargar_datos": "Descargar datos",
    "consultar_informacion_institucional": "Consultar información institucional",
    "consumir_apis": "Consumir APIs",
    "utilizar_plataformas_de_analisis": "Utilizar plataformas de análisis",
    "realizar_analisis_geoespacial_avanzado": "Realizar análisis geoespacial avanzado",
    "obtener_informacion_complementaria": "Obtener información complementaria",
}

# Preferencias de acceso por fuente MVP
SOURCE_WHERE: dict[str, dict[str, Any]] = {
    "ideam": {
        "where": ["Portal institucional IDEAM", "API / datos abiertos", "Servicios ArcGIS Capasgeo"],
        "access_methods": ["portal", "api", "arcgis"],
        "default_categories": [
            "consultar_informacion_institucional",
            "consumir_apis",
            "descargar_datos",
        ],
    },
    "invemar": {
        "where": ["Portal institucional INVEMAR", "Geoportal / servicios"],
        "access_methods": ["portal", "api"],
        "default_categories": [
            "consultar_informacion_institucional",
            "descargar_datos",
        ],
    },
    "gbif": {
        "where": ["Portal GBIF", "API GBIF"],
        "access_methods": ["portal", "api"],
        "default_categories": ["consumir_apis", "descargar_datos"],
    },
    "fao": {
        "where": ["FAOSTAT / portal FAO"],
        "access_methods": ["portal", "api"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "worldpop": {
        "where": ["Portal WorldPop", "Descargas de capas poblacionales"],
        "access_methods": ["portal", "download"],
        "default_categories": ["obtener_informacion_complementaria", "descargar_datos"],
    },
    "gee": {
        "where": ["Google Earth Engine Code Editor / API"],
        "access_methods": ["platform", "api"],
        "default_categories": [
            "utilizar_plataformas_de_analisis",
            "realizar_analisis_geoespacial_avanzado",
        ],
    },
}

# Perfiles de necesidad: varias rutas complementarias (ej. inundaciones)
NEED_PROFILES: dict[str, dict[str, Any]] = {
    "inundaciones": {
        "need": "análisis de inundaciones en microcuenca",
        "match_any": ("inundaciones", "inundacion", "microcuenca"),
        "routes": [
            {
                "title": "Datos hidrológicos",
                "category": "consultar_informacion_institucional",
                "what_to_do": (
                    "Consultar series hidrológicas, precipitación y estaciones "
                    "oficiales para caracterizar la microcuenca."
                ),
                "source_id": "ideam",
                "resource_ids": [
                    "ideam:hidrologia",
                    "ideam:precipitacion",
                    "ideam:estaciones-meteorologicas",
                ],
                "why_default": "Fuente oficial nacional de hidrología y clima.",
            },
            {
                "title": "Análisis geoespacial",
                "category": "realizar_analisis_geoespacial_avanzado",
                "what_to_do": (
                    "Usar imágenes satelitales y series temporales para "
                    "análisis espacial de cobertura e inundabilidad."
                ),
                "source_id": "gee",
                "resource_ids": ["gee:sentinel2", "gee:landsat"],
                "why_default": "Procesamiento espacial y series temporales en plataforma de análisis.",
            },
            {
                "title": "Exposición poblacional",
                "category": "obtener_informacion_complementaria",
                "what_to_do": (
                    "Incorporar capas de población para estimar exposición "
                    "potencial en el área de estudio."
                ),
                "source_id": "worldpop",
                "resource_ids": [
                    "worldpop:population-density",
                    "worldpop:population-counts",
                ],
                "why_default": "Población potencialmente expuesta.",
            },
        ],
    },
    "precipitacion": {
        "need": "datos de precipitación",
        "match_any": ("precipitacion", "lluvia"),
        "routes": [
            {
                "title": "Descargar / consultar datos oficiales",
                "category": "descargar_datos",
                "what_to_do": (
                    "Obtener precipitaciones desde el portal o API institucional."
                ),
                "source_id": "ideam",
                "resource_ids": [
                    "ideam:precipitacion",
                    "ideam:estaciones-meteorologicas",
                ],
                "why_default": "Fuente oficial nacional; acceso portal y API.",
            },
            {
                "title": "Análisis avanzado con teledetección",
                "category": "realizar_analisis_geoespacial_avanzado",
                "what_to_do": (
                    "Complementar con catálogo Earth Engine (observación de la Tierra) "
                    "para análisis espacial y temporal."
                ),
                "source_id": "gee",
                "resource_ids": ["gee:sentinel2", "gee:landsat", "gee:catalog"],
                "why_default": "Plataforma de análisis geoespacial avanzado (MVP; sin inventar productos no curados).",
            },
        ],
    },
    "biodiversidad": {
        "need": "biodiversidad / especies",
        "match_any": ("biodiversidad", "especies", "occurrence"),
        "routes": [
            {
                "title": "Registros de biodiversidad",
                "category": "consumir_apis",
                "what_to_do": "Consultar ocurrencias y metadatos vía GBIF.",
                "source_id": "gbif",
                "resource_ids": [],
                "why_default": "Red global de datos de biodiversidad con API.",
            },
            {
                "title": "Ecosistemas costeros (Colombia)",
                "category": "consultar_informacion_institucional",
                "what_to_do": "Revisar productos marino-costeros institucionales.",
                "source_id": "invemar",
                "resource_ids": [],
                "why_default": "Fuente oficial nacional para océanos y costas.",
            },
        ],
    },
    "erosion": {
        "need": "análisis de erosión / suelos",
        "match_any": ("erosion", "erosiones", "suelos"),
        "routes": [
            {
                "title": "Observación de la Tierra",
                "category": "realizar_analisis_geoespacial_avanzado",
                "what_to_do": "Analizar cobertura y cambios con imágenes satelitales.",
                "source_id": "gee",
                "resource_ids": ["gee:sentinel2", "gee:landsat"],
                "why_default": "Series temporales y procesamiento espacial.",
            },
            {
                "title": "Datos agropecuarios complementarios",
                "category": "obtener_informacion_complementaria",
                "what_to_do": "Consultar indicadores FAO relacionados con suelo/agricultura.",
                "source_id": "fao",
                "resource_ids": [],
                "why_default": "Contexto estadístico agrícola internacional.",
            },
        ],
    },
}


def match_need_profile(concepts: list[str], query_norm: str) -> dict[str, Any] | None:
    """Selecciona el perfil de necesidad más específico que coincida."""
    concept_set = set(concepts)
    # Preferir perfiles en orden de especificidad
    order = ("inundaciones", "precipitacion", "biodiversidad", "erosion")
    for key in order:
        profile = NEED_PROFILES[key]
        triggers = profile["match_any"]
        if any(t in concept_set or t in query_norm for t in triggers):
            return {"profile_id": key, **profile}
    return None


def category_for_intent(intent: str, source_id: str) -> str:
    """Elige categoría de acción según intención + fuente."""
    meta = SOURCE_WHERE.get(source_id, {})
    defaults = list(meta.get("default_categories") or ["obtener_informacion_complementaria"])

    if intent == "descargar":
        if "descargar_datos" in defaults or source_id != "gee":
            return "descargar_datos" if source_id != "gee" else defaults[0]
        return defaults[0]
    if intent in ("analizar", "evaluar", "identificar", "comparar"):
        if source_id == "gee":
            return "realizar_analisis_geoespacial_avanzado"
        if "consumir_apis" in defaults:
            return "consumir_apis"
        return defaults[0]
    if intent == "monitorear":
        if source_id == "gee":
            return "utilizar_plataformas_de_analisis"
        return "consultar_informacion_institucional"
    return defaults[0]


def where_for_source(source_id: str, category: str) -> list[str]:
    meta = SOURCE_WHERE.get(source_id, {})
    where = list(meta.get("where") or ["Consultar metadatos de la fuente en el catálogo"])
    if category == "consumir_apis":
        return [w for w in where if "API" in w.upper() or "api" in w.lower()] or where
    if category == "descargar_datos":
        return where
    if category in (
        "realizar_analisis_geoespacial_avanzado",
        "utilizar_plataformas_de_analisis",
    ):
        return [w for w in where if "Earth Engine" in w or "plataforma" in w.lower()] or where
    return where
