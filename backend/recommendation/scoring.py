"""
Scoring determinista y explicable — Recommendation Engine MVP (Fase 4).

Sin IA, embeddings ni ML. Pesos fijos y trazables.
"""

from __future__ import annotations

from typing import Any

# Pesos máximos (suman > 100; el score se capea a 100).
WEIGHT_KEYWORD_EXACT = 40
WEIGHT_DOMAIN_MATCH = 30
WEIGHT_RESOURCE_MATCH = 25
WEIGHT_SOURCE_MATCH = 35
WEIGHT_RELATED_DOMAIN = 15
WEIGHT_RELATED_KEYWORD = 10
WEIGHT_OFFICIAL_NATIONAL = 10

# Fuentes oficiales nacionales Colombia (curaduría humana / country profile).
OFFICIAL_NATIONAL_SOURCES = frozenset({"ideam", "invemar"})

# Términos institucionales / genéricos: no puntúan ni se indexan en KG.
# Evitan falsos positivos (p. ej. query "transporte" + keyword "colombia").
GENERIC_KEYWORDS = frozenset(
    {
        "colombia",
        "colombiano",
        "colombiana",
        "colombianos",
        "colombianas",
        "nacional",
        "nacionales",
        "territorio",
        "territorial",
        "sistema",
        "informacion",
        "informacion_geografica",
        "datos",
        "dato",
        "geografico",
        "geograficos",
        "portal",
        "mapa",
        "mapas",
        "servicio",
        "servicios",
        "oficial",
        "institucional",
    }
)

# Alias curados (no embeddings): expanden la consulta a términos del grafo.
CURATED_ALIASES: dict[str, list[str]] = {
    "lluvia": ["precipitacion"],
    "precipitacion": ["precipitacion", "lluvia", "meteorologia"],
    "oceanos": ["oceanos", "oceanos_costas", "marino", "costas"],
    "manglares": ["manglar", "ecosistemas", "costas"],
    "manglar": ["manglar", "ecosistemas"],
    "cuencas": ["hidrologia", "caudales", "cuencas"],
    "biodiversidad": ["biodiversidad", "especies", "occurrence"],
    "poblacion": ["poblacion", "densidad"],
    "satelite": ["observacion_tierra", "sentinel", "landsat"],
}


def normalize_token(text: str) -> str:
    value = text.strip().lower()
    for old, new in (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("ñ", "n"),
        ("ü", "u"),
    ):
        value = value.replace(old, new)
    return value.replace(" ", "_").replace("-", "_")


def is_generic_keyword(token: str) -> bool:
    return normalize_token(token) in GENERIC_KEYWORDS


def expand_query_tokens(query: str) -> list[str]:
    """Tokens de búsqueda incluyendo alias curados (sin genéricos)."""
    base = normalize_token(query)
    raw: set[str] = {base}
    if "_" in base:
        raw.update(p for p in base.split("_") if p)
    for alias_key, alias_vals in CURATED_ALIASES.items():
        if base == alias_key or base in alias_vals or any(
            normalize_token(v) in raw for v in alias_vals
        ):
            raw.add(alias_key)
            raw.update(normalize_token(v) for v in alias_vals)
    # Quitar stopwords genéricas; si la query era solo genérica, dejar vacío
    # (el motor aún puede matchear por source_id / dominio explícito).
    tokens = {t for t in raw if t and not is_generic_keyword(t)}
    return sorted(tokens)


def cap_score(raw: int) -> int:
    return max(0, min(100, raw))


def official_national_bonus(source_id: str) -> tuple[int, str | None]:
    if source_id in OFFICIAL_NATIONAL_SOURCES:
        return WEIGHT_OFFICIAL_NATIONAL, "fuente oficial nacional"
    return 0, None


def empty_accumulator(source_id: str, source_label: str) -> dict[str, Any]:
    return {
        "source_id": source_id,
        "source": source_label,
        "score_raw": 0,
        "reason": [],
        "relations_used": [],
        "matched_resources": [],
        "matched_domains": [],
        "matched_keywords": [],
    }


def add_reason(acc: dict[str, Any], reason: str) -> None:
    if reason and reason not in acc["reason"]:
        acc["reason"].append(reason)


def add_relation(
    acc: dict[str, Any],
    rel_type: str,
    from_id: str,
    to_id: str,
) -> None:
    item = {"type": rel_type, "from_id": from_id, "to_id": to_id}
    if item not in acc["relations_used"]:
        acc["relations_used"].append(item)


def finalize(acc: dict[str, Any]) -> dict[str, Any] | None:
    """Descarta candidatos sin justificación."""
    if not acc["reason"] or not acc["relations_used"]:
        return None
    return {
        "source": acc["source"],
        "source_id": acc["source_id"],
        "score": cap_score(acc["score_raw"]),
        "reason": list(acc["reason"]),
        "relations_used": list(acc["relations_used"]),
        "resources": list(acc["matched_resources"]),
        "domains": list(acc["matched_domains"]),
        "keywords": list(acc["matched_keywords"]),
    }
