"""
Scoring determinista y explicable — Recommendation Engine MVP (Fase 4).

Sin IA, embeddings ni ML. Pesos fijos y trazables.
"""

from __future__ import annotations

from typing import Any

# Pesos máximos (suman > 100; el score se capea a 100).
WEIGHT_KEYWORD_EXACT = 25
WEIGHT_DOMAIN_MATCH = 45
WEIGHT_RESOURCE_MATCH = 20
WEIGHT_SOURCE_MATCH = 20
WEIGHT_RELATED_DOMAIN = 10
WEIGHT_RELATED_KEYWORD = 5
WEIGHT_OFFICIAL_NATIONAL = 15

# Fuentes oficiales nacionales Colombia (curaduría humana / country profile).
OFFICIAL_NATIONAL_SOURCES = frozenset({"ideam", "invemar"})

# Términos institucionales / genéricos: no puntúan ni se indexan en KG.
# Evitan falsos positivos (p. ej. query "transporte" + keyword "colombia").
GENERIC_KEYWORDS = frozenset(
    {
        # Nacionales / geográficos genéricos
        "colombia", "colombiano", "colombiana", "colombianos", "colombianas",
        "nacional", "nacionales", "territorio", "territorial",
        "global", "regional", "local", "municipal", "departamental",
        # Información / sistemas
        "sistema", "informacion", "informacion_geografica",
        "datos", "dato", "geografico", "geograficos",
        "portal", "mapa", "mapas", "servicio", "servicios",
        "oficial", "institucional", "publico", "abierto",
        "plataforma", "acceso", "consulta", "visualizacion",
        "descarga", "metadatos", "catalogo", "repositorio",
        "documento", "documentacion",
        # Verbos / conceptos demasiado amplios
        "cambio", "transicion", "evolucion", "dinamica", "tendencia",
        "transformacion", "modificacion", "variacion", "trayectoria",
        "monitoreo", "monitorizacion", "seguimiento", "observacion",
        "vigilancia", "control", "verificacion", "actualizacion",
        "historico", "integrado", "consolidado", "unificado",
        "serie_tiempo", "multitemporal", "tiempo_real",
        # Descriptores vacíos
        "estudio", "analisis", "investigacion", "proyecto",
        "desarrollo", "gestion", "planificacion", "evaluacion",
        # Preposiciones y conectores españoles: hacen match por subcadena
        # en etiquetas ("Gobernación del X") y dispersan el ranking.
        "a", "al", "ante", "bajo", "con", "contra", "de", "del",
        "desde", "durante", "e", "el", "en", "entre", "hacia", "hasta",
        "la", "las", "lo", "los", "mediante", "ni", "o", "para", "pero",
        "por", "que", "segun", "si", "sin", "sobre", "su", "sus", "tras",
        "u", "un", "una", "unas", "unos", "y",
        "cada", "como", "cual", "cuales", "cuando", "cuyo", "cuyos",
        "donde", "eso", "esta", "estas", "este", "estos", "mas", "muy",
        "no", "tambien", "ya",
    }
)

# Alias curados (no embeddings): expanden la consulta a términos del grafo.
CURATED_ALIASES: dict[str, list[str]] = {
    # Clima y meteorología
    "lluvia": ["precipitacion", "meteorologia", "clima"],
    "precipitacion": ["precipitacion", "lluvia", "meteorologia", "clima", "chirps", "gpm"],
    "temperatura": ["temperatura", "clima", "tsm", "era5", "worldclim"],
    "clima": ["clima", "meteorologia", "precipitacion", "temperatura", "evapotranspiracion"],
    # Océanos y costas
    "oceanos": ["oceanos_costas", "marino", "costas", "dimar", "invemar", "cioh"],
    # Sin "inundacion": asociación débil que secuestraba la etiqueta de
    # necesidad en consultas de ecosistemas (p. ej. marinos + temperatura).
    "manglares": ["manglar", "manglares", "costas", "humedal", "ecosistemas"],
    "costas": ["costas", "costero", "costera", "litoral", "bahia", "playa", "erosion_costera"],
    # Sin ciudades (buenaventura/cartagena): la geografía se maneja con el
    # filtro coverage; mezclar ciudades en aliases conceptuales generaba
    # razones ajenas ("keyword cartagena" en consultas de Buenaventura).
    "bahia": ["bahia", "golfo", "ensenada", "estuario"],
    # Hidrología
    "cuencas": ["hidrologia", "cuencas", "caudales", "rios", "cuenca",
                "microcuenca", "microcuencas"],
    "inundaciones": ["inundacion", "inundaciones", "riesgo", "hidrologia", "desbordamiento"],
    # Coberturas y uso del suelo (clave para el caso Buenaventura)
    "coberturas": ["coberturas", "cobertura", "uso_suelo", "landcover", "lulc", "mapbiomas", "habitat"],
    "deforestacion": ["deforestacion", "bosques", "perdida_bosque", "gfw", "alertas", "cobertura_forestal"],
    "uso_suelo": ["uso_suelo", "coberturas", "landcover", "lulc", "mapbiomas", "clasificacion"],
    # Biodiversidad
    "biodiversidad": ["biodiversidad", "especies", "fauna", "flora", "habitat", "conservacion"],
    "aves": ["aves", "pajaros", "ebird", "ornitologia", "biodiversidad"],
    "ecosistemas": ["ecosistemas", "ecosistema", "ecosistemica", "ecosistemico",
                    "ecosistemicos", "bioma", "habitat", "biodiversidad", "conservacion"],
    # Servicios ecosistémicos (provisión, hábitat, regulación…)
    "servicios_ecosistemicos": ["servicios_ecosistemicos", "provision", "habitat",
                                "regulacion", "soporte", "ecosistemas"],
    # Suelos
    "suelos": ["suelos", "suelo", "edafologia", "soilgrids", "carbono_organico", "ph", "textura"],
    # Geología
    "geologia": ["geologia", "geologico", "geomorfologia", "sismico", "volcan", "sgc", "fallas"],
    "sismos": ["sismos", "sismo", "sismicidad", "terremoto", "amenaza_sismica", "sgc"],
    # Población
    "poblacion": ["poblacion", "densidad", "demografia", "censo", "worldpop", "dane"],
    # Observación de la Tierra
    "satelite": ["observacion_tierra", "sentinel", "landsat", "modis", "nasa", "gee"],
    "imagenes": ["imagenes", "satelitales", "ortofotos", "observacion_tierra", "sentinel", "landsat"],
    # Morfometría / relieve / DEM
    "morfometria": ["morfometria", "morfologia", "relieve", "dem", "elevacion", "pendiente",
                    "alos_palsar", "srtm", "topografia", "cuenca", "hidrologia"],
    # Riesgo
    "riesgo": ["riesgo", "amenaza", "vulnerabilidad", "desastre", "inundacion", "deslizamiento"],
    # Regiones geográficas: solo regiones, sin ciudades (la cobertura
    # específica la maneja el filtro coverage).
    "buenaventura": ["buenaventura", "pacifico", "pacifico_colombiano"],
    "pacifico": ["pacifico", "pacifico_colombiano", "choco_biogeografico"],
    "caribe": ["caribe", "caribe_colombiano"],
    "amazonia": ["amazonia", "amazonas", "leticia", "caqueta", "putumayo", "guaviare"],
    # Infraestructura (sin expandir a ciudades específicas)
    "transporte": ["transporte", "infraestructura", "vias", "carreteras", "aeropuertos"],
    "puertos": ["puertos", "portuario", "portuaria"],
    # Uso del suelo / agro (ganadería y zonificación implican coberturas)
    "ganaderia": ["ganaderia", "ganadera", "pastos", "agricultura",
                  "uso_suelo", "coberturas"],
    "zonificacion": ["zonificacion", "ordenamiento", "uso_suelo", "aptitud",
                     "coberturas"],
    # Ecosistemas estratégicos colombianos
    "paramos": ["paramos", "paramo", "humedales", "alta_montana",
                "ecosistemas", "biodiversidad"],
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


def _word_forms(token: str) -> set[str]:
    """Formas simple/plural de un token para matching de alias."""
    forms = {token}
    if len(token) > 4 and token.endswith("s"):
        forms.add(token[:-1])
    return forms


def expand_query_tokens(query: str) -> list[str]:
    """Tokens de búsqueda incluyendo alias curados (sin genéricos).

    Expansión de UN solo salto sobre los tokens originales del usuario
    (con formas singular/plural). Antes la expansión se encadenaba
    transitivamente (ecosistemas → manglares → costas → bahía → caribe…)
    y contaminaba consultas con temas ajenos (morfometría, deslizamientos)
    en consultas marinas.
    """
    base = normalize_token(query)
    raw: set[str] = {base}
    if "_" in base:
        raw.update(p for p in base.split("_") if p)
    # Snapshot de los tokens del usuario: solo contra estos se compara;
    # los tokens agregados por un alias no disparan otros alias.
    snapshot: set[str] = set(raw)
    for token in list(raw):
        snapshot.update(_word_forms(token))
    for alias_key, alias_vals in CURATED_ALIASES.items():
        key_forms = _word_forms(alias_key)
        value_forms = {normalize_token(v) for v in alias_vals}
        if (
            base == alias_key
            or snapshot & key_forms
            or snapshot & value_forms
        ):
            raw.add(alias_key)
            raw.update(normalize_token(v) for v in alias_vals)
    # Quitar stopwords genéricas; si la query era solo genérica, dejar vacío
    # (el motor aún puede matchear por source_id / dominio explícito).
    tokens = {t for t in raw if t and not is_generic_keyword(t)}
    return sorted(tokens)


def cap_score(raw: int) -> int:
    """Escala logarítmica para diferenciar scores. Máximo teórico ~200."""
    if raw <= 0:
        return 0
    # Escala: 0-50 lineal, 50-150 se comprime, >150 asintótico a 100
    if raw <= 50:
        return raw
    if raw <= 150:
        return 50 + int((raw - 50) * 0.5)
    return min(100, 100)


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
