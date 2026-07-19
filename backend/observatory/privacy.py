"""
Privacidad y minimización — Knowledge Usage Observatory MVP.

Principios: anonimización, transparencia, sin PII.
"""

from __future__ import annotations

import re
from typing import Any

TRANSPARENCY_NOTICE = (
    "Las consultas realizadas en DB2S-GEO pueden registrarse de forma anónima "
    "para mejorar recomendaciones, identificar vacíos de conocimiento y fortalecer "
    "la plataforma. No se recopila información personal identificable."
)

# Patrones a redactar (nunca persistir)
_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_URL_CREDS_RE = re.compile(r"(https?://)([^/\s:@]+):([^/\s@]+)@")
_LONG_DIGITS_RE = re.compile(r"\b\d{8,}\b")
_PASSWORDISH_RE = re.compile(
    r"(?i)\b(password|passwd|contraseña|secret|token|api[_-]?key)\s*[:=]\s*\S+"
)


def sanitize_query(text: str, *, max_len: int = 240) -> str:
    """Elimina indicios de PII / secretos y trunca."""
    value = (text or "").strip()
    if not value:
        return ""
    value = _EMAIL_RE.sub("[redacted-email]", value)
    value = _URL_CREDS_RE.sub(r"\1[redacted]@", value)
    value = _PASSWORDISH_RE.sub(r"\1=[redacted]", value)
    value = _LONG_DIGITS_RE.sub("[redacted-id]", value)
    # Colapsar espacios
    value = re.sub(r"\s+", " ", value).strip()
    if len(value) > max_len:
        value = value[: max_len - 1].rstrip() + "…"
    return value


def is_safe_to_log(text: str) -> bool:
    """False si tras sanitizar queda vacío o solo redacciones."""
    clean = sanitize_query(text)
    if not clean:
        return False
    stripped = re.sub(r"\[redacted[^\]]*\]", "", clean, flags=re.I).strip()
    return len(stripped) >= 2


def minimize_recommendations(items: list[dict[str, Any]] | None, *, limit: int = 8) -> list[dict[str, Any]]:
    """Solo source_id + score (sin metadatos personales)."""
    out: list[dict[str, Any]] = []
    for item in items or []:
        sid = item.get("source_id") or item.get("source")
        if not sid:
            continue
        entry: dict[str, Any] = {"source_id": str(sid)}
        if "score" in item and item["score"] is not None:
            entry["score"] = item["score"]
        out.append(entry)
        if len(out) >= limit:
            break
    return out


def extract_domains_from_payload(payload: dict[str, Any]) -> list[str]:
    """Recoge dominios de recomendaciones / rutas sin PII."""
    found: list[str] = []
    for key in ("recommendations", "routes"):
        for item in payload.get(key) or []:
            for d in item.get("domains") or []:
                d = str(d).strip().lower()
                if d and d not in found:
                    found.append(d)
            # rutas DSS pueden no traer domains; mirar resources titles no
    for d in payload.get("domains") or []:
        d = str(d).strip().lower()
        if d and d not in found:
            found.append(d)
    for c in payload.get("concepts") or []:
        # conceptos que coinciden con dominios conocidos se añaden en el engine
        pass
    return found
