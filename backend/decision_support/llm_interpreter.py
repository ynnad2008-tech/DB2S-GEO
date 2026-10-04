"""
Intérprete NL opcional — Gemini (Google AI Studio).

Convierte la consulta en lenguaje natural en intents / need / concepts con
el vocabulario de la plataforma. Nunca inventa fuentes: solo interpreta.
Si no hay API key, no hay red o la respuesta no valida → interpretación
determinista (detect_intents + expand_concepts). La trazabilidad se expone
en la respuesta de /decision-support ("interpretation").

Variables de entorno (opcionales):
  GEMINI_API_KEY  — clave de AI Studio (ausente → solo determinista)
  GEMINI_MODEL    — id de modelo preferido (si se omite, se usa la cadena)
  GEMINI_TIMEOUT  — segundos máximos por llamada (default: 8)

Cadena de modelos (se prueba en orden ante fallos 4xx/503/429):
  GEMINI_MODEL → gemini-3.7-flash → gemini-3.1-pro-preview
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from typing import Any

from backend.decision_support.concepts import expand_concepts, primary_need_label
from backend.decision_support.intents import INTENT_LABELS, detect_intents
from backend.recommendation.scoring import is_generic_keyword, normalize_token

GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
MODEL_CHAIN = ["gemini-3.7-flash", "gemini-3.1-pro-preview"]
MAX_CONCEPTS = 10

# Circuit breaker: tras 429/503 (cuota/demanda), Gemini entra en cooldown
# para no pagar latencia de reintentos en cada consulta.
_last_unavailable_at: float | None = None
UNAVAILABLE_COOLDOWN = 60.0  # segundos


def _gemini_on_cooldown() -> bool:
    if _last_unavailable_at is None:
        return False
    return time.monotonic() - _last_unavailable_at < UNAVAILABLE_COOLDOWN


def _set_cooldown() -> None:
    global _last_unavailable_at
    _last_unavailable_at = time.monotonic()


def _clear_cooldown() -> None:
    global _last_unavailable_at
    _last_unavailable_at = None

_ALLOWED_INTENTS = list(INTENT_LABELS.keys())

_PROMPT = (
    "Eres el intérprete de consultas de DB2S-GEO, un catálogo curado de "
    "fuentes de datos geoespaciales y ambientales de Colombia. Convierte la "
    "consulta del usuario en un objeto JSON estricto con estos campos:\n"
    '- "intents": lista de 1 a 3 de: ' + ", ".join(_ALLOWED_INTENTS) + '\n'
    '- "need": frase corta en español (máx. 12 palabras) que describa la '
    'necesidad concreta del usuario\n'
    '- "concepts": de 2 a 8 palabras clave normalizadas (minúsculas, sin '
    "tildes, compuestas con _) del vocabulario del catálogo: hidrologia, "
    "precipitacion, inundacion, clima, suelos, erosion, biodiversidad, "
    "oceanos_costas, cartografia, catastro, ordenamiento, agricultura, "
    "poblacion, riesgo, geologia, deforestacion, coberturas, "
    "infraestructura, energia, manglares, morfometria, dem, elevacion\n"
    "Reglas: responde SOLO el JSON, sin texto adicional. No inventes "
    "fuentes ni datos; solo interpreta la consulta.\n"
    "Consulta del usuario: "
)


def _call_gemini(
    prompt: str,
    *,
    model: str,
    key: str,
    timeout: float,
) -> dict[str, Any]:
    """POST a la API de Gemini. Separada para facilitar mocks en tests."""
    url = GEMINI_ENDPOINT.format(model=model) + f"?key={key}"
    body = json.dumps(
        {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "response_mime_type": "application/json",
                "temperature": 0,
            },
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    text = (
        payload["candidates"][0]["content"]["parts"][0]["text"]
    )
    # Gemini a veces envuelve el JSON en cercas markdown
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)


def _sanitize_interpretation(raw: Any, query: str) -> dict[str, Any]:
    """Valida y normaliza la respuesta del modelo. Lanza ValueError si es inútil."""
    if not isinstance(raw, dict):
        raise ValueError("respuesta del modelo no es objeto JSON")
    intents = [str(i).strip().lower() for i in raw.get("intents") or []]
    intents = [i for i in intents if i in _ALLOWED_INTENTS]
    if not intents:
        intents = detect_intents(query)
    need = str(raw.get("need") or "").strip()[:140]
    if not need:
        need = primary_need_label(expand_concepts(query), query)
    concepts: list[str] = []
    for c in raw.get("concepts") or []:
        token = normalize_token(str(c))
        if len(token) < 3 or is_generic_keyword(token) or token in concepts:
            continue
        concepts.append(token)
        if len(concepts) >= MAX_CONCEPTS:
            break
    if not concepts:
        concepts = expand_concepts(query)
    return {"intents": intents, "need": need, "concepts": concepts}


def interpret_query(query: str) -> dict[str, Any]:
    """Interpreta la consulta con Gemini; fallback determinista garantizado.

    Devuelve: {source, model, fallback, error, intents, need, concepts}.
    """
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    try:
        timeout = float(os.environ.get("GEMINI_TIMEOUT", "8"))
    except ValueError:
        timeout = 8.0

    deterministic = {
        "source": "deterministic",
        "model": None,
        "fallback": False,
        "error": None,
        "intents": detect_intents(query),
        "need": primary_need_label(expand_concepts(query), query),
        "concepts": expand_concepts(query),
    }
    if not key:
        return deterministic

    # Circuit breaker: si Gemini viene fallando por cuota/demanda, ir
    # directo al fallback rápido en vez de pagar reintentos por consulta.
    if _gemini_on_cooldown():
        result = dict(deterministic)
        result["fallback"] = True
        result["error"] = "gemini en cooldown (429/503 previo)"
        return result

    models: list[str] = []
    env_model = os.environ.get("GEMINI_MODEL", "").strip()
    if env_model:
        models.append(env_model)
    for m in MODEL_CHAIN:
        if m not in models:
            models.append(m)

    prompt = _PROMPT + query
    last_error: Exception | None = None
    for model in models:
        try:
            raw = _call_gemini(prompt, model=model, key=key, timeout=timeout)
            parsed = _sanitize_interpretation(raw, query)
            _clear_cooldown()
            return {
                "source": "gemini",
                "model": model,
                "fallback": False,
                "error": None,
                **parsed,
            }
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code in (503, 429):
                # alta demanda / cuota: un solo reintento breve, luego cooldown
                time.sleep(1.0)
                try:
                    raw = _call_gemini(prompt, model=model, key=key, timeout=timeout)
                    parsed = _sanitize_interpretation(raw, query)
                    _clear_cooldown()
                    return {
                        "source": "gemini",
                        "model": model,
                        "fallback": False,
                        "error": None,
                        **parsed,
                    }
                except Exception as exc2:
                    last_error = exc2
                    _set_cooldown()
                    break
            continue  # 4xx (modelo retirado, clave sin permiso…) → siguiente modelo
        except Exception as exc:  # sin red, timeout, JSON inválido…
            last_error = exc
            continue

    result = dict(deterministic)
    result["fallback"] = True
    result["error"] = f"{type(last_error).__name__}: {last_error}"[:160]
    return result
