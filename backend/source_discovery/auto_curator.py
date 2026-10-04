"""
Crecimiento autogestionado del catálogo — Auto Curator (Gemini + verificación).

Gobernanza elegida por el autor (2026-10-03): auto total.
- Fuentes nuevas: Gemini las propone desde los vacíos del Observatorio;
  la COMPUERTA DETERMINISTA (verificación HTTP real) es obligatoria —
  una URL muerta descarta el candidato (Gemini no verifica URLs).
- Fichas existentes: solo se AGREGAN keywords propuestas por Gemini desde
  las interacciones recientes (nunca se borran ni se reescriben recursos).
- Toda acción queda en el log JSONL (data/auto_curation/log.jsonl) con
  provenance: "llm-verified".

Variables de entorno:
  AUTO_CURATION=on  — habilita el ciclo (endpoint /source-discovery/auto-curate)
  GEMINI_API_KEY    — requerida (cadena de modelos de llm_interpreter)
"""

from __future__ import annotations

import json
import os
import re
import ssl
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from backend.decision_support.llm_interpreter import MODEL_CHAIN, _call_gemini
from backend.metadata.domains import INITIAL_DOMAINS
from backend.recommendation.scoring import is_generic_keyword, normalize_token

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCES_DIR = ROOT / "catalog" / "sources"
DEFAULT_LOG_DIR = ROOT / "data" / "auto_curation"

ID_RE = re.compile(r"^[a-z][a-z0-9_-]{1,63}$")
MAX_NEW_SOURCES = 6
MAX_ENRICH_SOURCES = 5
MAX_KEYWORDS_PER_SOURCE = 5
MAX_GAP_QUERIES = 8

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
UA = {"User-Agent": "Mozilla/5.0 (DB2S-GEO auto-curator; verificacion)"}

PROPOSE_PROMPT = (
    "Eres el curador automático de DB2S-GEO, un catálogo de fuentes de datos "
    "geoespaciales y ambientales. Estas consultas de usuarios no encontraron "
    "buenas fuentes:\n{queries}\n"
    "PRIORIZA fuentes con GEOSERVICIOS accesibles (ArcGIS REST, WMS, WFS, "
    "WMTS): esa es la misión principal de la plataforma. Propón hasta {n} "
    "fuentes de datos públicas y REALES que las atiendan.\n"
    "Responde SOLO JSON, una lista de objetos con estos campos:\n"
    '- "id": slug corto en minusculas (solo letras, numeros, - y _)\n'
    '- "name": nombre de la fuente\n'
    '- "institution": institucion responsable\n'
    '- "url": URL canonica REAL del portal (https)\n'
    '- "geoservice_url": URL REAL del geoservicio (directorio ArcGIS REST o '
    "endpoint WMS/WFS); omitir si no la conoces\n"
    '- "geoservice_type": "ArcGIS_REST", "WMS", "WFS" o "WMTS" (solo si hay geoservice_url)\n'
    '- "coverage": cobertura espacial (p. ej. "Global", "Colombia", "Honduras")\n'
    '- "domains": lista de 1-3 de estos: ' + ", ".join(sorted(INITIAL_DOMAINS)) + '\n'
    '- "keywords": lista de 3-8 palabras clave en minusculas sin tildes\n'
    '- "description": descripcion de 1-2 frases\n'
    "NO inventes URLs: si no conoces la URL real, omite ese campo o esa "
    "fuente. Solo fuentes que existen de verdad.\n"
)

ENRICH_PROMPT = (
    "Fuente del catálogo DB2S-GEO: {name} ({institution}).\n"
    "Estos términos aparecieron en consultas recientes de usuarios que "
    "mencionan esta fuente: {terms}\n"
    "Elige hasta {n} términos REALMENTE relevantes para esta fuente como "
    "keywords de búsqueda. Responde SOLO JSON: lista de strings en "
    "minúsculas, sin tildes, separadas con _ si son compuestas.\n"
)


def enabled() -> bool:
    return os.environ.get("AUTO_CURATION", "").strip().lower() == "on"


def _log(log_dir: Path, action: str, detail: dict[str, Any]) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        **detail,
    }
    with (log_dir / "log.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def probe_url(url: str) -> bool:
    """Compuerta determinista: la URL debe responder de verdad."""
    if not url or not url.startswith(("http://", "https://")):
        return False
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers=UA)
            with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
                return resp.status in (200, 301, 302, 303, 307, 308)
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (403, 405, 501):
                continue
            return e.code == 403  # WAF anti-bot: URL probablemente OK
        except Exception:
            return False
    return False


def probe_geoservice(url: str, tipo: str) -> bool:
    """Compuerta para geoservicios: el endpoint debe responder su protocolo."""
    if not url or not url.startswith(("http://", "https://")):
        return False
    sep = "&" if "?" in url else "?"
    if tipo == "ArcGIS_REST":
        url += f"{sep}f=json"
    elif tipo in ("WMS", "WFS", "WMTS"):
        service = "WMS" if tipo != "WFS" else "WFS"
        url += f"{sep}service={service}&request=GetCapabilities"
    try:
        req = urllib.request.Request(url, method="GET", headers=UA)
        with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
            body = resp.read(2000).decode("utf-8", errors="ignore").lstrip()
            if tipo == "ArcGIS_REST":
                return body.startswith("{")
            return body.startswith("<")
    except Exception:
        return False


def _gemini(prompt: str) -> dict[str, Any]:
    """Llama a Gemini con la cadena de modelos; lanza la última excepción."""
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("GEMINI_API_KEY no configurada")
    timeout = 30.0
    last: Exception | None = None
    for model in MODEL_CHAIN:
        try:
            text = _call_gemini(prompt, model=model, key=key, timeout=timeout)
            text = text.strip()
            if text.startswith("```"):
                text = text.strip("`")
                if text.startswith("json"):
                    text = text[4:]
            return json.loads(text)
        except Exception as exc:
            last = exc
            continue
    raise last if last else RuntimeError("sin modelos disponibles")


def _gaps(observatory: Any) -> list[dict[str, Any]]:
    """Consultas sin resultados (o con score débil) del observatorio."""
    events = observatory._store.list_events()  # interfaz interna del repo
    gaps: list[dict[str, Any]] = []
    seen: set[str] = set()
    for e in events:
        q = str(e.get("query") or "").strip()
        if not q or q in seen:
            continue
        has = bool(e.get("has_results")) and int(e.get("result_count") or 0) >= 3
        if not has:
            seen.add(q)
            gaps.append({"query": q, "terms": list(e.get("terms") or [])[:12]})
        if len(gaps) >= MAX_GAP_QUERIES:
            break
    return gaps


def _sanitize_candidate(c: dict[str, Any]) -> dict[str, Any] | None:
    sid = str(c.get("id") or "").strip().lower()
    name = str(c.get("name") or "").strip()
    url = str(c.get("url") or "").strip()
    if not ID_RE.match(sid) or len(name) < 2 or not url.startswith("https://"):
        return None
    domains = [d for d in (c.get("domains") or []) if str(d) in INITIAL_DOMAINS][:3]
    keywords: list[str] = []
    for kw in c.get("keywords") or []:
        token = normalize_token(str(kw))
        if len(token) < 3 or is_generic_keyword(token) or token in keywords:
            continue
        keywords.append(token)
    if not keywords:
        return None
    geo_url = str(c.get("geoservice_url") or "").strip()
    geo_tipo = str(c.get("geoservice_type") or "").strip()
    if geo_url and not geo_url.startswith("https://"):
        geo_url = ""
    if geo_tipo not in ("ArcGIS_REST", "WMS", "WFS", "WMTS"):
        geo_tipo = ""
    return {
        "id": sid,
        "name": name[:120],
        "institution": str(c.get("institution") or name).strip()[:200],
        "url": url,
        "coverage": str(c.get("coverage") or "Global").strip()[:80],
        "domains": domains,
        "keywords": keywords,
        "description": str(c.get("description") or "").strip()[:400],
        "geoservice_url": geo_url if geo_tipo else "",
        "geoservice_type": geo_tipo,
    }


def create_ficha(
    candidate: dict[str, Any],
    sources_dir: Path,
    *,
    geoservice_verified: bool = False,
) -> bool:
    """Crea la ficha (status active, curation llm-verified). False si existe.

    Si el geoservicio fue verificado, es el recurso PRIMARIO (misión de la
    plataforma); el portal queda como recurso secundario.
    """
    path = sources_dir / f"{candidate['id']}.json"
    if path.exists():
        return False
    resources: list[dict[str, Any]] = []
    if geoservice_verified and candidate.get("geoservice_url"):
        method = "arcgis" if candidate["geoservice_type"] == "ArcGIS_REST" else "wms"
        resources.append({
            "id": f"{candidate['id']}:geoservice",
            "name": f"Geoservicio — {candidate['name']}",
            "description": "Geoservicio verificado por la compuerta HTTP del "
                           "curador automático. DB2S-GEO solo documenta el acceso.",
            "url": candidate["geoservice_url"],
            "category": "geoservice",
            "coverage": {"spatial": candidate["coverage"], "temporal": "Según publicación de la fuente"},
            "domains": candidate["domains"],
            "keywords": candidate["keywords"],
            "access_methods": [method],
            "endpoints": [{"method": method, "url": candidate["geoservice_url"],
                           "label": candidate["name"]}],
            "formats": ["servicios REST"] if method == "arcgis" else [candidate["geoservice_type"]],
            "documentation_url": candidate["url"],
            "doi": "",
            "citation_reference": (
                f"{candidate['institution']}. {candidate['name']} (geoservicio). "
                f"{candidate['geoservice_url']}"
            ),
        })
    resources.append({
        "id": f"{candidate['id']}:portal",
        "name": f"Portal — {candidate['name']}",
        "description": "Portal verificado por el curador automático. "
                       "DB2S-GEO solo documenta el acceso.",
        "url": candidate["url"],
        "category": "portal",
        "coverage": {"spatial": candidate["coverage"], "temporal": "Según publicación de la fuente"},
        "domains": candidate["domains"],
        "keywords": candidate["keywords"],
        "access_methods": ["portal"],
        "endpoints": [{"method": "portal", "url": candidate["url"], "label": candidate["name"]}],
        "formats": ["portal"],
        "documentation_url": candidate["url"],
        "doi": "",
        "citation_reference": f"{candidate['institution']}. {candidate['name']}. {candidate['url']}",
    })
    payload = {
        "id": candidate["id"],
        "name": candidate["name"],
        "description": candidate["description"] or (
            f"{candidate['name']}: fuente propuesta por el curador automático "
            "a partir de los vacíos de consulta. DB2S-GEO solo documenta el acceso."
        ),
        "url": candidate["geoservice_url"] if geoservice_verified and candidate.get("geoservice_url")
               else candidate["url"],
        "category": "plataforma",
        "coverage": {"spatial": candidate["coverage"], "temporal": "Según publicación de la fuente"},
        "status": "active",
        "institution": candidate["institution"],
        "domains": candidate["domains"],
        "license": "Según términos de la fuente",
        "version": "1.0.0",
        "curation": "llm-verified",
        "curation_note": "Propuesta por Gemini y verificada por HTTP el "
                         f"{datetime.now(timezone.utc).date().isoformat()}.",
        "resources": resources,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return True


def _source_keywords(payload: dict[str, Any]) -> set[str]:
    kws: set[str] = set()
    for r in payload.get("resources") or []:
        kws.update(normalize_token(str(k)) for k in r.get("keywords") or [])
    return kws


def enrich_existing(events: list[dict[str, Any]], sources_dir: Path) -> int:
    """Agrega keywords LLM a fichas existentes (solo agregar, tope 5/fuente)."""
    # Términos de consultas recientes por fuente mencionada
    terms_by_source: dict[str, set[str]] = {}
    for e in events[:200]:
        for rec in e.get("recommendations") or []:
            sid = str(rec.get("source_id") or "").strip()
            if not sid:
                continue
            for t in e.get("terms") or []:
                token = normalize_token(str(t))
                if len(token) >= 3 and not is_generic_keyword(token):
                    terms_by_source.setdefault(sid, set()).add(token)
    enriched = 0
    for sid, terms in list(terms_by_source.items())[:MAX_ENRICH_SOURCES]:
        path = sources_dir / f"{sid}.json"
        if not path.exists():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        existing = _source_keywords(payload)
        candidates = sorted(terms - existing)
        if not candidates:
            continue
        try:
            raw = _gemini(ENRICH_PROMPT.format(
                name=payload.get("name", sid),
                institution=payload.get("institution", ""),
                terms=", ".join(candidates[:30]),
                n=MAX_KEYWORDS_PER_SOURCE,
            ))
            chosen = [
                normalize_token(str(t)) for t in raw
                if isinstance(raw, list)
                and len(normalize_token(str(t))) >= 3
                and not is_generic_keyword(normalize_token(str(t)))
                and normalize_token(str(t)) not in existing
            ][:MAX_KEYWORDS_PER_SOURCE]
        except Exception as exc:
            _log(DEFAULT_LOG_DIR, "enrich_error", {"source_id": sid, "error": str(exc)[:120]})
            continue
        if not chosen:
            continue
        # Solo agregar: keywords nuevas al primer recurso
        if payload.get("resources"):
            payload["resources"][0]["keywords"] = (
                list(payload["resources"][0].get("keywords") or []) + chosen
            )
            payload["curation"] = "llm-enriched"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        enriched += 1
    return enriched


def run_cycle(
    observatory: Any,
    sources_dir: Path | None = None,
    log_dir: Path | None = None,
) -> dict[str, Any]:
    """Un ciclo completo: vacíos → propuesta Gemini → verificación → fichas."""
    sources_dir = sources_dir or DEFAULT_SOURCES_DIR
    log_dir = log_dir or DEFAULT_LOG_DIR
    summary = {"proposed": 0, "verified": 0, "geoservice_added": 0,
               "portal_added": 0, "enriched": 0, "log": str(log_dir / "log.jsonl")}

    gaps = _gaps(observatory)
    if not gaps:
        summary["note"] = "sin vacíos detectados en el observatorio"
        return summary

    try:
        raw = _gemini(PROPOSE_PROMPT.format(
            queries=json.dumps(gaps, ensure_ascii=False),
            n=MAX_NEW_SOURCES,
        ))
        candidates = [c for c in raw if isinstance(c, dict)] if isinstance(raw, list) else []
    except Exception as exc:
        summary["error"] = f"gemini: {type(exc).__name__}: {exc}"[:160]
        _log(log_dir, "cycle_error", {"error": summary["error"]})
        return summary

    summary["proposed"] = len(candidates)

    # Prioridad mandatoria: fuentes con geoservicio verificable primero.
    geo_ok: list[dict[str, Any]] = []
    portal_ok: list[dict[str, Any]] = []
    for c in candidates:
        candidate = _sanitize_candidate(c)
        if candidate is None:
            continue
        has_geo = bool(candidate.get("geoservice_url"))
        geo_verified = has_geo and probe_geoservice(
            candidate["geoservice_url"], candidate["geoservice_type"]
        )
        if geo_verified:
            summary["verified"] += 1
            geo_ok.append(candidate)
            continue
        # Sin geoservicio verificado: el portal debe responder para entrar
        if not probe_url(candidate["url"]):
            _log(log_dir, "candidate_rejected", {
                "id": candidate["id"], "reason": "url no verificada",
                "url": candidate["url"][:160],
                "geoservice_fallido": has_geo,
            })
            continue
        summary["verified"] += 1
        portal_ok.append(candidate)

    for candidate in geo_ok[:MAX_NEW_SOURCES]:
        if create_ficha(candidate, sources_dir, geoservice_verified=True):
            summary["geoservice_added"] += 1
            _log(log_dir, "source_added", {
                "id": candidate["id"], "kind": "geoservice",
                "geoservice": candidate["geoservice_url"][:160],
                "coverage": candidate["coverage"], "domains": candidate["domains"],
            })
    # Relleno con portales verificados solo si faltan para el tope
    remaining = MAX_NEW_SOURCES - summary["geoservice_added"]
    for candidate in portal_ok[:remaining]:
        if create_ficha(candidate, sources_dir):
            summary["portal_added"] += 1
            _log(log_dir, "source_added", {
                "id": candidate["id"], "kind": "portal",
                "url": candidate["url"][:160],
                "coverage": candidate["coverage"], "domains": candidate["domains"],
            })

    events = observatory._store.list_events()
    summary["enriched"] = enrich_existing(events, sources_dir)
    _log(log_dir, "cycle_summary", summary)
    summary["note"] = "reiniciar el servidor para cargar las fichas nuevas en runtime"
    return summary
