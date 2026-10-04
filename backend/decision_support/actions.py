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
    "dimar": {
        "where": ["Portal institucional DIMAR", "IDE Marítima, Fluvial y Costera", "Pronósticos meteomarinos"],
        "access_methods": ["portal", "api"],
        "default_categories": [
            "consultar_informacion_institucional",
            "descargar_datos",
        ],
    },
    "cioh": {
        "where": ["Portal institucional CIOH", "Productos oceanográficos y de mareas"],
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
    # --- Ministerios de Colombia (verificados 2026-10-02) ---
    "minsalud": {
        "where": ["Portal institucional MinSalud"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "mineducacion": {
        "where": ["Portal institucional MinEducación", "Geoportal MinEducación (ArcGIS REST)"],
        "access_methods": ["portal", "arcgis"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "minagricultura": {
        "where": ["Portal institucional MinAgricultura", "Agronet / EVA"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "mincomercio": {
        "where": ["Portal institucional MinComercio"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "mintic": {
        "where": ["Portal institucional MinTIC"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    # --- Corporaciones y agencias ---
    "anh": {
        "where": ["Portal institucional ANH"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "cvc": {
        "where": ["Portal institucional CVC"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "cormagdalena": {
        "where": ["Portal institucional Cormagdalena"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    # --- Institutos de investigación ---
    "humboldt": {
        "where": ["Portal institucional IAvH"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "sinchi": {
        "where": ["Portal institucional SINCHI"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "ipse": {
        "where": ["Portal institucional IPSE"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    # --- Gobernaciones (verificadas 2026-10-02) ---
    "gob-antioquia": {
        "where": ["Portal institucional — Gobernación de Antioquia"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "gob-cundinamarca": {
        "where": ["Portal institucional — Gobernación de Cundinamarca"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "gob-tolima": {
        "where": ["Portal institucional — Gobernación del Tolima"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "gob-valle": {
        "where": ["Portal institucional — Gobernación del Valle del Cauca"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "gob-santander": {
        "where": ["Portal institucional — Gobernación de Santander"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "gob-boyaca": {
        "where": ["Portal institucional — Gobernación de Boyacá"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "gob-narino": {
        "where": ["Portal institucional — Gobernación de Nariño"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "gob-caldas": {
        "where": ["Portal institucional — Gobernación de Caldas"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "gob-risaralda": {
        "where": ["Portal institucional — Gobernación de Risaralda"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "gob-quindio": {
        "where": ["Portal institucional — Gobernación del Quindío"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "gob-cauca": {
        "where": ["Portal institucional — Gobernación del Cauca"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "gob-huila": {
        "where": ["Portal institucional — Gobernación del Huila"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "gob-nortedesantander": {
        "where": ["Portal institucional — Gobernación de Norte de Santander"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "gob-cesar": {
        "where": ["Portal institucional — Gobernación del Cesar"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "gob-magdalena": {
        "where": ["Portal institucional — Gobernación del Magdalena"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "gob-cordoba": {
        "where": ["Portal institucional — Gobernación de Córdoba"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "gob-sucre": {
        "where": ["Portal institucional — Gobernación de Sucre"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "gob-bolivar": {
        "where": ["Portal institucional — Gobernación de Bolívar"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "gob-atlantico": {
        "where": ["Portal institucional — Gobernación del Atlántico"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "gob-choco": {
        "where": ["Portal institucional — Gobernación del Chocó"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    # --- Alcaldías (verificadas 2026-10-02) ---
    "cali": {
        "where": ["Portal institucional — Alcaldía de Cali"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "barranquilla": {
        "where": ["Portal institucional — Alcaldía de Barranquilla"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "cartagena": {
        "where": ["Portal institucional — Alcaldía de Cartagena"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "pereira": {
        "where": ["Portal institucional — Alcaldía de Pereira"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "manizales": {
        "where": ["Portal institucional — Alcaldía de Manizales"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    # --- Universidades ---
    "unal": {
        "where": ["Portal institucional UNAL"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional"],
    },
    "uniandes": {
        "where": ["Portal institucional Uniandes"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional"],
    },
    # --- Fuentes globales validadas por el curador (2026-10-03) ---
    "hydrosheds": {
        "where": ["Portal HydroSHEDS", "Productos hidrográficos (descargas)"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "hydroatlas": {
        "where": ["HydroATLAS — portal de datos (HydroSHEDS)"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "grdc": {
        "where": ["GRDC — portal institucional (BfG)"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "worldclim": {
        "where": ["Portal WorldClim", "Descargas de datos climáticos"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "chelsa": {
        "where": ["Portal CHELSA"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "wdpa": {
        "where": ["Protected Planet — WDPA"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "iucn_red_list": {
        "where": ["IUCN Red List — portal"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "birdlife": {
        "where": ["BirdLife International — portal", "BirdLife Data Zone"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "copernicus_marine": {
        "where": ["Copernicus Marine — portal de productos oceánicos"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
    "emodnet": {
        "where": ["EMODnet — portal", "EMODnet Bathymetry"],
        "access_methods": ["portal"],
        "default_categories": ["consultar_informacion_institucional", "descargar_datos"],
    },
}

# Perfiles de necesidad: varias rutas complementarias (ej. inundaciones)
NEED_PROFILES: dict[str, dict[str, Any]] = {
    "inundaciones_maritimas": {
        "need": "análisis de inundación marítima y costera",
        "match_any": (
            "maritima", "marina", "costera", "costero",
            "marejada", "oleaje", "marea", "litoral",
        ),
        "routes": [
            {
                "title": "Información marino-costera",
                "category": "consultar_informacion_institucional",
                "what_to_do": (
                    "Consultar ecosistemas costeros, manglares y erosión "
                    "costera con la autoridad ambiental marina de Colombia."
                ),
                "source_id": "invemar",
                "resource_ids": [
                    "invemar:ecosistemas-costeros",
                    "invemar:manglares-colombia",
                ],
                "why_default": "Autoridad ambiental marina de Colombia.",
            },
            {
                "title": "Niveles del mar y alertas",
                "category": "consultar_informacion_institucional",
                "what_to_do": (
                    "Consultar la IDE marítima, fluvial y costera y los "
                    "pronósticos meteomarinos de la autoridad marítima nacional."
                ),
                "source_id": "dimar",
                "resource_ids": ["dimar:ide-maritima"],
                "why_default": "Autoridad marítima nacional de Colombia.",
            },
            {
                "title": "Mareas y oceanografía",
                "category": "consultar_informacion_institucional",
                "what_to_do": (
                    "Consultar mareas, nivel del mar y oceanografía "
                    "operacional del Caribe y Pacífico colombiano."
                ),
                "source_id": "cioh",
                "resource_ids": [
                    "cioh:mareas",
                    "cioh:oceanografia-operacional",
                ],
                "why_default": "Investigación oceanográfica e hidrográfica nacional.",
            },
        ],
    },
    "inundaciones": {
        "need": "análisis de inundaciones en microcuenca",
        # "microcuenca" fuera de los disparadores: mencionarla no implica
        # inundación (p. ej. "modelación ecosistémica en la microcuenca").
        "match_any": ("inundaciones", "inundacion"),
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
        # Solo disparo directo: la cadena de conceptos (clima → precipitacion
        # → lluvia) producía ≥2 disparadores falsos en consultas de
        # temperatura/clima y secuestraba la intención del usuario.
        "require_direct": True,
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
        # Solo disparo directo: la cadena ecosistemas → biodiversidad →
        # especies → occurrence producía 3 disparadores falsos y desviaba
        # consultas mixtas (p. ej. temperatura en ecosistemas marinos).
        "require_direct": True,
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
    """Selecciona el perfil de necesidad más específico que coincida.

    Regla estricta de disparo (evita desviar la intención del usuario):
    - disparador directo en la consulta → coincide;
    - si no, se exigen ≥2 disparadores en conceptos expandidos (evidencia
      conceptual fuerte). Un solo concepto no basta: antes "precipitacion"
      (concepto de inundaciones) o "suelos" (de erosión) secuestraban
      consultas no relacionadas.
    """
    concept_set = set(concepts)
    # Preferir perfiles en orden de especificidad
    order = (
        "inundaciones_maritimas",
        "inundaciones",
        "precipitacion",
        "biodiversidad",
        "erosion",
    )
    for key in order:
        profile = NEED_PROFILES[key]
        triggers = profile["match_any"]
        direct = [t for t in triggers if t in query_norm]
        if direct:
            return {"profile_id": key, **profile}
        if profile.get("require_direct"):
            continue
        in_concepts = [t for t in triggers if t in concept_set]
        if len(in_concepts) >= 2:
            return {"profile_id": key, **profile}
    return None


def category_for_intent(intent: str, source_id: str) -> str:
    """Elige categoría de acción según intención + fuente."""
    meta = SOURCE_WHERE.get(source_id, {})
    # Fuentes sin entrada curada: por defecto son portales institucionales.
    defaults = list(meta.get("default_categories") or ["consultar_informacion_institucional"])

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


def where_for_source(
    source_id: str,
    category: str,
    source_label: str | None = None,
) -> list[str]:
    meta = SOURCE_WHERE.get(source_id, {})
    fallback = (
        [f"Portal institucional — {source_label}"] if source_label
        else ["Consultar metadatos de la fuente en el catálogo"]
    )
    where = list(meta.get("where") or fallback)
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
