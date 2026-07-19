"""
Analítica agregada — Knowledge Usage Observatory MVP.

Top consultas, vacíos, dominios, emergentes, timeline, wordcloud.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any

from backend.recommendation.scoring import normalize_token

# Términos demasiado genéricos para "emergentes"
_COMMON = frozenset(
    {
        "datos",
        "fuente",
        "fuentes",
        "recurso",
        "recursos",
        "consulta",
        "analisis",
        "informacion",
        "colombia",
        "geo",
        "mapa",
    }
)


def _day_key(ts: str) -> str:
    if not ts:
        return "unknown"
    return ts[:10]


def top_queries(events: list[dict[str, Any]], *, limit: int = 20) -> list[dict[str, Any]]:
    counter: Counter[str] = Counter()
    for e in events:
        q = (e.get("query") or "").strip().lower()
        if q:
            counter[q] += 1
    return [{"query": q, "count": n} for q, n in counter.most_common(limit)]


def empty_queries(events: list[dict[str, Any]], *, limit: int = 20) -> list[dict[str, Any]]:
    counter: Counter[str] = Counter()
    last_seen: dict[str, str] = {}
    for e in events:
        if e.get("has_results"):
            continue
        q = (e.get("query") or "").strip().lower()
        if not q:
            continue
        counter[q] += 1
        ts = str(e.get("timestamp") or "")
        if q not in last_seen or ts > last_seen[q]:
            last_seen[q] = ts
    rows = [
        {"query": q, "count": n, "last_seen": last_seen.get(q)}
        for q, n in counter.most_common(limit)
    ]
    return rows


def domain_ranking(events: list[dict[str, Any]], *, limit: int = 20) -> list[dict[str, Any]]:
    counter: Counter[str] = Counter()
    for e in events:
        for d in e.get("domains") or []:
            d = str(d).strip().lower()
            if d:
                counter[d] += 1
    return [{"domain": d, "count": n} for d, n in counter.most_common(limit)]


def emerging_terms(
    events: list[dict[str, Any]],
    *,
    limit: int = 20,
    known_domains: set[str] | None = None,
) -> list[dict[str, Any]]:
    """
    Términos frecuentes en consultas recientes que no son dominios ya tipificados
    (señal de taxonomía / catálogo a expandir).
    """
    known = known_domains or set()
    # Ventana: últimos N eventos o todos si pocos
    window = events[:200] if len(events) > 200 else events
    counter: Counter[str] = Counter()
    for e in window:
        for t in e.get("terms") or []:
            t = normalize_token(str(t))
            if len(t) < 3 or t in _COMMON or t in known:
                continue
            counter[t] += 1
        # también tokens de query
        q = normalize_token(str(e.get("query") or ""))
        for part in q.split("_"):
            if len(part) < 4 or part in _COMMON or part in known:
                continue
            counter[part] += 1
    return [{"term": t, "count": n} for t, n in counter.most_common(limit)]


def timeline(events: list[dict[str, Any]], *, days: int = 30) -> list[dict[str, Any]]:
    counter: Counter[str] = Counter()
    empty_counter: Counter[str] = Counter()
    for e in events:
        day = _day_key(str(e.get("timestamp") or ""))
        if day == "unknown":
            continue
        counter[day] += 1
        if not e.get("has_results"):
            empty_counter[day] += 1
    # Últimos `days` días calendario presentes + huecos recientes
    today = datetime.now(timezone.utc).date()
    out: list[dict[str, Any]] = []
    for i in range(days - 1, -1, -1):
        from datetime import timedelta

        d = (today - timedelta(days=i)).isoformat()
        out.append(
            {
                "date": d,
                "count": counter.get(d, 0),
                "empty": empty_counter.get(d, 0),
            }
        )
    return out


def wordcloud(
    events: list[dict[str, Any]],
    *,
    limit: int = 40,
    known_domains: set[str] | None = None,
    emerging_limit: int = 12,
) -> list[dict[str, Any]]:
    counter: Counter[str] = Counter()
    domain_hits: dict[str, Counter[str]] = {}
    for e in events:
        event_domains = [normalize_token(str(d)) for d in (e.get("domains") or []) if d]
        for t in e.get("terms") or []:
            t = normalize_token(str(t))
            if len(t) >= 3 and t not in _COMMON:
                counter[t] += 1
                for d in event_domains:
                    domain_hits.setdefault(t, Counter())[d] += 1
        for d in event_domains:
            if d:
                counter[d] += 1
                domain_hits.setdefault(d, Counter())[d] += 1
        q = normalize_token(str(e.get("query") or ""))
        for part in q.split("_"):
            if len(part) >= 4 and part not in _COMMON:
                counter[part] += 1
                for d in event_domains:
                    domain_hits.setdefault(part, Counter())[d] += 1

    items = counter.most_common(limit)
    if not items:
        return []

    known = known_domains or set()
    emerging_rows = emerging_terms(events, limit=emerging_limit, known_domains=known)
    emerging_set = {r["term"] for r in emerging_rows}

    # Alias término → dominio tipificado
    term_domain_alias = {
        "precipitacion": "clima",
        "lluvia": "clima",
        "meteorologia": "clima",
        "temperatura": "clima",
        "caudales": "hidrologia",
        "cuencas": "hidrologia",
        "cuenca": "hidrologia",
        "microcuenca": "hidrologia",
        "inundaciones": "hidrologia",
        "inundacion": "hidrologia",
        "agua": "hidrologia",
        "sentinel": "observacion_tierra",
        "landsat": "observacion_tierra",
        "satelite": "observacion_tierra",
        "satelital": "observacion_tierra",
        "cobertura": "observacion_tierra",
        "manglares": "oceanos_costas",
        "manglar": "oceanos_costas",
        "poblacion": "poblacion",
        "densidad": "poblacion",
        "biodiversidad": "biodiversidad",
        "especies": "biodiversidad",
        "suelos": "suelos",
        "erosion": "suelos",
        "agricultura": "agricultura",
    }

    max_n = items[0][1]
    out: list[dict[str, Any]] = []
    for t, n in items:
        domain = t if t in known else None
        if domain is None and t in term_domain_alias:
            domain = term_domain_alias[t]
        if domain is None and t in domain_hits and domain_hits[t]:
            domain = domain_hits[t].most_common(1)[0][0]
        out.append(
            {
                "term": t,
                "count": n,
                "weight": round(n / max_n, 3) if max_n else 0,
                "domain": domain,
                "emerging": t in emerging_set and t not in known,
            }
        )
    return out


def summary(events: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(events)
    empty = sum(1 for e in events if not e.get("has_results"))
    return {
        "total_queries": total,
        "with_results": total - empty,
        "without_results": empty,
        "unique_queries": len({(e.get("query") or "").lower() for e in events if e.get("query")}),
        "channels": dict(Counter(str(e.get("channel") or "unknown") for e in events)),
    }
