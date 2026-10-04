"""
Cobertura geográfica curada — filtro coverage (DB2S-GEO 0.6).

Permite filtrar fuentes por cobertura espacial (country_or_scope) contra
una lista curada de coberturas colombianas (nacional, departamental,
municipal y regional). Además detecta cobertura mencionada en la consulta
("precipitación en el Tolima" → coverage=tolima).

Semántica de matches_coverage(scope, coverage, include_global):
- coverage="colombia" → scope nacional o subnacional colombiano (+global si include_global)
- coverage=<subnacional> → scope exacto, o nacional (cubre todo el país)
  (+global si include_global)
- coverage="global" → solo scope global

Sin IA: listas curadas y normalización textual.
"""

from __future__ import annotations

# NOTA: no se importa recommendation.scoring a nivel de módulo — creaba un
# ciclo (discovery.engine → coverage → scoring → recommendation.__init__ →
# recommendation.engine → coverage). normalize_token se importa lazy.

# Departamentos de Colombia (normalizados, sin tildes)
DEPARTAMENTOS = frozenset(
    {
        "amazonas", "antioquia", "arauca", "atlantico", "bolivar", "boyaca",
        "caldas", "caqueta", "casanare", "cauca", "cesar", "choco", "cordoba",
        "cundinamarca", "guainia", "guaviare", "huila", "la_guajira",
        "magdalena", "meta", "narino", "norte_de_santander", "putumayo",
        "quindio", "risaralda", "san_andres", "santander", "sucre", "tolima",
        "valle_del_cauca", "vaupes", "vichada",
    }
)

# Ciudades / municipios clave (normalizados)
CIUDADES = frozenset(
    {
        "bogota", "medellin", "cali", "barranquilla", "cartagena", "manizales",
        "pereira", "bucaramanga", "cucuta", "ibague", "pasto", "villavicencio",
        "monteria", "sincelejo", "valledupar", "riohacha", "quibdo", "popayan",
        "neiva", "armenia", "florencia", "mocoa", "leticia", "tumaco",
        "buenaventura", "santa_marta", "san_jose_del_guaviare",
        "puerto_inirida", "mitu", "yopal",
    }
)

# Regiones naturales / cuencas (normalizados)
REGIONES = frozenset(
    {
        "amazonia", "orinoquia", "caribe", "pacifico", "andina",
        "caribe_colombiano", "pacifico_colombiano", "cuenca_del_magdalena",
    }
)

# ── Otros países de la expansión regional (2026-10-03) ──
# Lugares clave por país (normalizados); el nombre del país es cobertura
# nacional y cubre sus subnacionales.
PAISES_LUGARES: dict[str, frozenset[str]] = {
    "honduras": frozenset(
        {
            "tegucigalpa", "san_pedro_sula", "catacamas", "olancho",
            "la_ceiba", "comayagua", "choluteca", "siguatepeque",
        }
    ),
    "costa_rica": frozenset(
        {
            "san_jose", "heredia", "cartago", "alajuela", "limon",
            "puntarenas", "guanacaste",
        }
    ),
    "mexico": frozenset(
        {
            "cdmx", "ciudad_de_mexico", "guadalajara", "monterrey",
            "yucatan", "chiapas", "oaxaca", "veracruz", "sonora",
        }
    ),
    "peru": frozenset(
        {
            "lima", "cusco", "arequipa", "loreto", "piura", "trujillo",
            "puno", "ica", "ancash", "junin",
        }
    ),
}

# País → lugares (incluida la cobertura nacional)
COUNTRY_SCOPES: dict[str, frozenset[str]] = {
    "colombia": DEPARTAMENTOS | CIUDADES | REGIONES | frozenset({"colombia"}),
    "honduras": PAISES_LUGARES["honduras"] | frozenset({"honduras"}),
    "costa_rica": PAISES_LUGARES["costa_rica"] | frozenset({"costa_rica"}),
    "mexico": PAISES_LUGARES["mexico"] | frozenset({"mexico"}),
    "peru": PAISES_LUGARES["peru"] | frozenset({"peru"}),
}

NATIONAL_KEYS = frozenset(COUNTRY_SCOPES.keys())

# Frases multi-palabra de los nuevos países (detección)
PHRASES_PAISES: tuple[str, ...] = (
    "san_jose", "san_pedro_sula", "ciudad_de_mexico", "costa_rica",
)

# Alias de detección → cobertura canónica
DETECTION_ALIASES: dict[str, str] = {
    "co": "colombia",
    "colombiano": "colombia",
    "colombiana": "colombia",
    "amazonas": "amazonia",  # en consultas suele referirse a la región
    "amazonica": "amazonia",
    "caribe_colombiano": "caribe",
    "pacifico_colombiano": "pacifico",
}

# Frases multi-palabra (se buscan antes que los tokens sueltos)
PHRASES: tuple[str, ...] = (
    "valle_del_cauca",
    "norte_de_santander",
    "la_guajira",
    "san_andres",
    "santa_marta",
    "san_jose_del_guaviare",
    "puerto_inirida",
    "cuenca_del_magdalena",
    "caribe_colombiano",
    "pacifico_colombiano",
)


def normalize_coverage(text: str) -> str:
    """Normaliza una cobertura/scope: minúsculas, sin tildes, _ por espacio.

    Los paréntesis explicativos de las fichas ("Colombia (32 departamentos…)"
    → "colombia") se eliminan.
    """
    from backend.recommendation.scoring import normalize_token  # lazy: evita ciclo

    value = normalize_token(text or "")
    if "_(" in value:
        value = value.split("_(")[0]
    return value


def is_national_colombia(scope_norm: str) -> bool:
    """scope nacional de Colombia (incluye variantes con paréntesis ya limpiadas)."""
    return scope_norm == "colombia"


# Jerarquía ciudad → departamento (un dataset departamental cubre sus ciudades)
CITY_TO_DEPT: dict[str, str] = {
    "bogota": "colombia",
    "medellin": "antioquia",
    "cali": "valle_del_cauca",
    "buenaventura": "valle_del_cauca",
    "barranquilla": "atlantico",
    "cartagena": "bolivar",
    "santa_marta": "magdalena",
    "valledupar": "cesar",
    "riohacha": "la_guajira",
    "sincelejo": "sucre",
    "monteria": "cordoba",
    "manizales": "caldas",
    "pereira": "risaralda",
    "armenia": "quindio",
    "ibague": "tolima",
    "neiva": "huila",
    "popayan": "cauca",
    "pasto": "narino",
    "cucuta": "norte_de_santander",
    "bucaramanga": "santander",
    "villavicencio": "meta",
    "quibdo": "choco",
    "yopal": "casanare",
    "florencia": "caqueta",
    "mocoa": "putumayo",
    "leticia": "amazonas",
    "mitu": "vaupes",
    "puerto_inirida": "guainia",
    "san_jose_del_guaviare": "guaviare",
    "tumaco": "narino",
}


def matches_coverage(
    country_or_scope: str,
    coverage: str,
    *,
    include_global: bool = True,
) -> bool:
    """Indica si un scope cubre la cobertura pedida.

    Semántica: cobertura nacional → sus subnacionales; cobertura subnacional
    → el propio lugar, su contenedor (departamento → ciudad) y su país;
    los globales cubren todo (opcional con include_global).
    """
    scope = normalize_coverage(country_or_scope)
    cov = normalize_coverage(coverage)
    if not cov:
        return True
    if cov in NATIONAL_KEYS:
        if scope == "global":
            return include_global
        return scope in COUNTRY_SCOPES[cov]
    if cov == "global":
        return scope == "global"
    if scope == cov:
        return True
    if cov in CIUDADES and scope == CITY_TO_DEPT.get(cov):
        return True
    # El país cubre sus subnacionales (p. ej. scope Honduras, cov tegucigalpa)
    for country, lugares in COUNTRY_SCOPES.items():
        if scope == country and cov in lugares:
            return True
    if scope == "global":
        return include_global
    if cov in REGIONES and scope == cov:
        return True
    return False


def detect_coverage(query: str) -> str | None:
    """Detecta cobertura mencionada en la consulta (o None).

    Reconoce Colombia (nacional, departamentos, ciudades y regiones) y los
    países de la expansión regional (honduras, costa_rica, mexico, peru)
    con sus ciudades clave.
    """
    from backend.recommendation.scoring import normalize_token  # lazy: evita ciclo

    norm = normalize_token(query or "")
    if not norm:
        return None
    # Frases multi-palabra primero
    for phrase in PHRASES + PHRASES_PAISES:
        if phrase in norm:
            return DETECTION_ALIASES.get(phrase, phrase)
    # Tokens individuales (match exacto de token, no subcadena:
    # "metadatos" no dispara "meta", "calidad" no dispara "cali").
    for token in norm.split("_"):
        canon = DETECTION_ALIASES.get(token, token)
        if canon == "colombia":
            return "colombia"
        if canon in NATIONAL_KEYS:
            return canon
        if canon in DEPARTAMENTOS or canon in CIUDADES or canon in REGIONES:
            return canon
        for country, lugares in PAISES_LUGARES.items():
            if canon in lugares:
                return canon
    return None
