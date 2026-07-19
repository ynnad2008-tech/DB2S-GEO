"""
Normalización de conceptos y equivalencias curadas — Decision Support MVP.

Expande lenguaje natural a dominios / keywords del catálogo MVP.
Sin embeddings.
"""

from __future__ import annotations

from backend.recommendation.scoring import CURATED_ALIASES, normalize_token

# Equivalencias adicionales orientadas a necesidades (Fase 8).
CONCEPT_ALIASES: dict[str, list[str]] = {
    "agua": ["hidrologia", "precipitacion", "caudales"],
    "lluvia": ["precipitacion", "lluvia", "meteorologia"],
    "precipitacion": ["precipitacion", "lluvia", "meteorologia", "clima"],
    "inundaciones": ["hidrologia", "precipitacion", "caudales", "cuencas"],
    "inundacion": ["hidrologia", "precipitacion", "caudales", "cuencas"],
    "microcuenca": ["hidrologia", "cuencas", "caudales"],
    "cuenca": ["hidrologia", "cuencas", "caudales"],
    "erosion": ["suelos", "observacion_tierra", "cobertura"],
    "erosiones": ["suelos", "observacion_tierra"],
    "suelos": ["suelos", "agricultura"],
    "poblacion": ["poblacion", "densidad"],
    "expuesta": ["poblacion", "densidad"],
    "exposicion": ["poblacion", "densidad"],
    "satelite": ["observacion_tierra", "sentinel", "landsat"],
    "cobertura": ["observacion_tierra", "cobertura", "sentinel"],
    "biodiversidad": ["biodiversidad", "especies", "occurrence"],
    "manglares": ["manglar", "ecosistemas", "costas"],
    "clima": ["clima", "precipitacion", "temperatura"],
    "hidrologia": ["hidrologia", "caudales", "cuencas"],
}

_STOPWORDS = frozenset(
    {
        "el",
        "la",
        "los",
        "las",
        "un",
        "una",
        "unos",
        "unas",
        "de",
        "del",
        "en",
        "con",
        "para",
        "por",
        "y",
        "o",
        "que",
        "se",
        "su",
        "sus",
        "al",
        "lo",
        "mi",
        "me",
        "necesito",
        "quiero",
        "requiero",
        "busco",
        "datos",
        "informacion",
        "hacer",
        "sobre",
        "como",
        "desde",
        "hacia",
        "entre",
        "analizar",
        "descargar",
        "estudiar",
        "evaluar",
        "comparar",
        "monitorear",
        "identificar",
    }
)


def expand_concepts(query: str) -> list[str]:
    """Tokens conceptuales (alias Fase 4 + Fase 8)."""
    base = normalize_token(query)
    tokens: set[str] = set()

    for part in base.replace(",", " ").split("_"):
        part = part.strip()
        if len(part) >= 3 and part not in _STOPWORDS:
            tokens.add(part)

    for alias_key, alias_vals in CURATED_ALIASES.items():
        if alias_key in tokens or any(
            normalize_token(v) in tokens for v in alias_vals
        ):
            tokens.add(alias_key)
            tokens.update(normalize_token(v) for v in alias_vals)

    for alias_key, alias_vals in CONCEPT_ALIASES.items():
        if alias_key in tokens or alias_key in base:
            tokens.add(alias_key)
            tokens.update(normalize_token(v) for v in alias_vals)
        elif any(normalize_token(v) in tokens for v in alias_vals):
            tokens.add(alias_key)
            tokens.update(normalize_token(v) for v in alias_vals)

    for alias_key, alias_vals in CONCEPT_ALIASES.items():
        if alias_key in base:
            tokens.add(alias_key)
            tokens.update(normalize_token(v) for v in alias_vals)

    tokens -= _STOPWORDS
    return sorted(tokens)


def primary_need_label(concepts: list[str], query: str) -> str:
    """Etiqueta legible de la necesidad detectada."""
    priority = (
        "inundaciones",
        "inundacion",
        "precipitacion",
        "hidrologia",
        "erosion",
        "biodiversidad",
        "poblacion",
        "manglares",
        "clima",
        "suelos",
        "agua",
    )
    for key in priority:
        if key in concepts:
            labels = {
                "inundaciones": "análisis de inundaciones / hidrología",
                "inundacion": "análisis de inundaciones / hidrología",
                "precipitacion": "datos de precipitación",
                "hidrologia": "datos hidrológicos",
                "erosion": "análisis de erosión / suelos",
                "biodiversidad": "biodiversidad y especies",
                "poblacion": "información poblacional",
                "manglares": "ecosistemas de manglar",
                "clima": "información climática",
                "suelos": "suelos y cobertura",
                "agua": "recursos hídricos",
            }
            return labels.get(key, key)
    q = (query or "").strip()
    return q[:120] if q else "consulta general"
