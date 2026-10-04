"""
Narrador de orientaciones — Gemini (modo inmersivo).

Escribe un resumen en lenguaje natural de la orientación generada y
sugiere preguntas de seguimiento. Nunca inventa fuentes: solo narra las
rutas ya calculadas por los motores deterministas.

Fallback determinista garantizado: sin API key, cooldown (429/503 previo),
sin red o respuesta inválida → resumen plantilla + sin followups.
"""

from __future__ import annotations

import json
import os
from typing import Any

from backend.decision_support.llm_interpreter import (
    MODEL_CHAIN,
    _call_gemini,
    _clear_cooldown,
    _gemini_on_cooldown,
    _set_cooldown,
)

_PROMPT = (
    "Eres el asistente geoespacial de DB2S-GEO. Un usuario consultó: "
    '"{query}".\n'
    'La necesidad detectada es: "{need}".\n'
    "Las rutas de orientación calculadas por los motores (fuente, título y "
    "por qué) son:\n{routes}\n"
    "Escribe un resumen de 2-3 frases, claro y útil, que oriente al usuario "
    "sobre qué hacer y con qué fuentes (no inventes fuentes: usa solo las "
    "listadas). Además propone 2-3 preguntas de seguimiento breves para "
    "profundizar.\n"
    'Responde SOLO JSON: {{"summary": "texto", "followups": ["pregunta1", '
    '"pregunta2"]}}.\n'
)


def _fallback(need: str, routes: list[dict[str, Any]]) -> dict[str, Any]:
    if not routes:
        summary = (
            f"Para «{need}» el catálogo aún no tiene fuentes curadas con "
            "buena cobertura. El Auto Curator registrará este vacío para "
            "proponer fuentes."
        )
    else:
        top = ", ".join(str(r.get("source") or r.get("source_id")) for r in routes[:3])
        summary = (
            f"Para «{need}» la plataforma orienta hacia: {top}. "
            "Cada ruta incluye qué hacer, con qué fuente oficial y por qué."
        )
    return {"source": "deterministic", "summary": summary, "followups": []}


_CHAT_PROMPT = (
    "Eres el asistente geoespacial conversacional de DB2S-GEO. Esta es la "
    "conversación hasta ahora:\n{history}\n"
    'La última pregunta del usuario es: "{query}".\n'
    'La necesidad detectada es: "{need}".\n'
    "Las rutas de orientación calculadas por los motores para esta pregunta "
    "son:\n{routes}\n"
    "Responde en 2-4 frases conversacionales, refiriéndote al contexto de la "
    "conversación si aplica (no inventes fuentes: usa solo las listadas). "
    "Propón 2-3 preguntas de seguimiento breves.\n"
    'Responde SOLO JSON: {{"summary": "texto", "followups": ["p1", "p2"]}}.\n'
)


def narrate_chat(
    query: str,
    need: str,
    routes: list[dict[str, Any]],
    history: list[dict[str, str]],
) -> dict[str, Any]:
    """Narración conversacional con contexto del hilo. Fallback determinista."""
    fallback = _fallback(need, routes)
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key or _gemini_on_cooldown() or not routes:
        return fallback

    history_txt = "\n".join(
        f"{str(h.get('role') or 'user')}: {str(h.get('text') or '')[:160]}"
        for h in (history or [])[-8:]
    ) or "(sin historial previo)"
    routes_txt = "\n".join(
        f"- {r.get('source') or r.get('source_id')}: {r.get('title', '')} "
        f"(porque: {'; '.join(map(str, (r.get('why') or [])[:2]))})"
        for r in routes[:6]
    )
    prompt = _CHAT_PROMPT.format(
        history=history_txt[:1000],
        query=query[:200],
        need=need[:120],
        routes=routes_txt[:1200],
    )
    last_error: Exception | None = None
    for model in MODEL_CHAIN:
        try:
            raw = _call_gemini(prompt, model=model, key=key, timeout=20.0)
            text = raw.strip()
            if text.startswith("```"):
                text = text.strip("`")
                if text.startswith("json"):
                    text = text[4:]
            data = json.loads(text)
            summary = str(data.get("summary") or "").strip()[:800]
            if not summary:
                raise ValueError("summary vacío")
            followups = [
                str(f).strip()[:140]
                for f in (data.get("followups") or [])
                if str(f).strip()
            ][:3]
            _clear_cooldown()
            return {"source": "gemini", "model": model,
                    "summary": summary, "followups": followups}
        except Exception as exc:
            last_error = exc
            if getattr(exc, "code", None) in (429, 503):
                _set_cooldown()
                break
            continue
    result = dict(fallback)
    if last_error is not None:
        result["error"] = f"{type(last_error).__name__}: {last_error}"[:140]
    return result


def narrate_orientation(
    query: str,
    need: str,
    routes: list[dict[str, Any]],
) -> dict[str, Any]:
    """Narra la orientación. Fallback determinista garantizado."""
    fallback = _fallback(need, routes)
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key or _gemini_on_cooldown() or not routes:
        return fallback

    routes_txt = "\n".join(
        f"- {r.get('source') or r.get('source_id')}: {r.get('title', '')} "
        f"(porque: {'; '.join(map(str, (r.get('why') or [])[:2]))})"
        for r in routes[:6]
    )
    prompt = _PROMPT.format(query=query[:200], need=need[:120], routes=routes_txt[:1200])
    last_error: Exception | None = None
    for model in MODEL_CHAIN:
        try:
            raw = _call_gemini(prompt, model=model, key=key, timeout=20.0)
            text = raw.strip()
            if text.startswith("```"):
                text = text.strip("`")
                if text.startswith("json"):
                    text = text[4:]
            data = json.loads(text)
            summary = str(data.get("summary") or "").strip()[:600]
            if not summary:
                raise ValueError("summary vacío")
            followups = [
                str(f).strip()[:140]
                for f in (data.get("followups") or [])
                if str(f).strip()
            ][:3]
            _clear_cooldown()
            return {"source": "gemini", "model": model,
                    "summary": summary, "followups": followups}
        except Exception as exc:
            last_error = exc
            if getattr(exc, "code", None) in (429, 503):
                _set_cooldown()
                break
            continue
    result = dict(fallback)
    if last_error is not None:
        result["error"] = f"{type(last_error).__name__}: {last_error}"[:140]
    return result
