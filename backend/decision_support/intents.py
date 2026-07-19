"""
Detección heurística de intención — Decision Support MVP.

Sin NLP/ML: coincidencia de palabras clave en texto normalizado.
"""

from __future__ import annotations

from backend.recommendation.scoring import normalize_token

# Intención → disparadores (español / inglés básico)
INTENT_TRIGGERS: dict[str, tuple[str, ...]] = {
    "descargar": ("descargar", "download", "bajar", "obtener_datos", "bajarme"),
    "analizar": ("analizar", "analisis", "análisis", "analysis", "procesar"),
    "monitorear": ("monitorear", "monitoreo", "seguimiento", "vigilancia", "monitor"),
    "comparar": ("comparar", "comparacion", "comparación", "contrastar"),
    "evaluar": ("evaluar", "evaluacion", "evaluación", "valorar"),
    "estudiar": ("estudiar", "estudio", "investigar", "investigacion"),
    "identificar": ("identificar", "detectar", "localizar", "ubicar", "mapear"),
}

INTENT_LABELS: dict[str, str] = {
    "descargar": "Descargar datos",
    "analizar": "Analizar",
    "monitorear": "Monitorear",
    "comparar": "Comparar",
    "evaluar": "Evaluar",
    "estudiar": "Estudiar",
    "identificar": "Identificar",
}


def detect_intents(query: str) -> list[str]:
    """Devuelve intenciones detectadas (orden estable). Si ninguna, ['estudiar']."""
    norm = normalize_token(query)
    # Espacios ya son _; también buscamos substrings
    found: list[str] = []
    for intent, triggers in INTENT_TRIGGERS.items():
        for t in triggers:
            token = normalize_token(t)
            if token in norm or token.replace("_", "") in norm.replace("_", ""):
                if intent not in found:
                    found.append(intent)
                break
    if not found:
        # "necesito" / "quiero" → estudiar por defecto
        if any(x in norm for x in ("necesito", "quiero", "requiero", "busco")):
            found.append("estudiar")
        else:
            found.append("estudiar")
    return found
