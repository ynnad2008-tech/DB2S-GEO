"""
Observatory Engine — Fase 8.1 MVP.

Registra consultas anónimas y expone analítica de uso / vacíos.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

from backend.observatory import analytics as an
from backend.observatory.privacy import (
    TRANSPARENCY_NOTICE,
    extract_domains_from_payload,
    is_safe_to_log,
    minimize_recommendations,
    sanitize_query,
)
from backend.observatory.store import ObservatoryStore
from backend.recommendation.scoring import normalize_token

if TYPE_CHECKING:
    from backend.metadata.engine import MetadataEngine

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = ROOT / "data" / "observatory"


class ObservatoryEngine:
    """Observatorio de uso y tendencias (anónimo)."""

    status = "mvp"

    def __init__(
        self,
        data_dir: Path | str | None = None,
        metadata: MetadataEngine | None = None,
    ) -> None:
        self._store = ObservatoryStore(data_dir or DEFAULT_DATA_DIR)
        self._metadata = metadata

    def bind(self, metadata: MetadataEngine | None = None) -> None:
        if metadata is not None:
            self._metadata = metadata

    def info(self) -> dict[str, Any]:
        return {
            "engine": "ObservatoryEngine",
            "status": self.status,
            "anonymous": True,
            "stores_pii": False,
            "stores_ip": False,
            "transparency_notice": TRANSPARENCY_NOTICE,
            "purpose": [
                "mejorar recomendaciones",
                "identificar vacíos de conocimiento",
                "detectar nuevas temáticas",
                "enriquecer taxonomías",
                "priorizar expansión del catálogo",
            ],
            "records": [
                "consulta",
                "fecha_hora",
                "resultados",
                "dominios",
                "recomendaciones",
            ],
            "never_records": [
                "nombres",
                "correos",
                "credenciales",
                "ip_persistente",
                "pii",
            ],
            **self._store.stats(),
        }

    def notice(self) -> dict[str, str]:
        return {"notice": TRANSPARENCY_NOTICE, "anonymous": True}

    def log_query(
        self,
        query: str,
        *,
        channel: str,
        result_count: int = 0,
        domains: list[str] | None = None,
        recommendations: list[dict[str, Any]] | None = None,
        terms: list[str] | None = None,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """
        Registra un evento anónimo. Devuelve el evento o None si no es seguro/vacío.
        Nunca acepta ni almacena IP u otros identificadores.
        """
        if not is_safe_to_log(query):
            return None

        clean = sanitize_query(query)
        domains_out = list(domains or [])
        if payload:
            for d in extract_domains_from_payload(payload):
                if d not in domains_out:
                    domains_out.append(d)
            if not recommendations and payload.get("recommendations"):
                recommendations = payload["recommendations"]
            if not recommendations and payload.get("routes"):
                recommendations = [
                    {"source_id": r.get("source_id"), "score": r.get("score")}
                    for r in payload["routes"]
                ]
            if result_count == 0 and "count" in payload:
                result_count = int(payload.get("count") or 0)
            if not terms and payload.get("concepts"):
                terms = [str(c) for c in payload["concepts"]]
            if not terms and payload.get("tokens"):
                terms = [str(t) for t in payload["tokens"]]

        # Dominios conocidos del catálogo que aparecen en la consulta
        known = self._known_domains()
        qn = normalize_token(clean)
        for d in known:
            if d in qn and d not in domains_out:
                domains_out.append(d)

        terms_out = [normalize_token(t) for t in (terms or []) if t]
        # tokens de la consulta
        for part in qn.split("_"):
            if len(part) >= 3 and part not in terms_out:
                terms_out.append(part)

        event = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "channel": channel,
            "query": clean,
            "query_norm": qn,
            "result_count": int(result_count),
            "has_results": int(result_count) > 0,
            "domains": domains_out[:20],
            "recommendations": minimize_recommendations(recommendations),
            "terms": terms_out[:30],
        }
        self._store.append(event)
        return event

    def log_from_recommend(self, query: str, payload: dict[str, Any]) -> dict[str, Any] | None:
        domains: list[str] = []
        for item in payload.get("recommendations") or []:
            for d in item.get("domains") or []:
                d = str(d).lower()
                if d not in domains:
                    domains.append(d)
        return self.log_query(
            query,
            channel="recommend",
            result_count=int(payload.get("count") or 0),
            domains=domains,
            recommendations=payload.get("recommendations"),
            terms=payload.get("tokens"),
            payload=payload,
        )

    def log_from_decision_support(
        self, query: str, payload: dict[str, Any]
    ) -> dict[str, Any] | None:
        return self.log_query(
            query,
            channel="decision_support",
            result_count=int(payload.get("count") or 0),
            domains=[],
            recommendations=[
                {"source_id": r.get("source_id"), "score": r.get("score")}
                for r in (payload.get("routes") or [])
            ],
            terms=payload.get("concepts"),
            payload=payload,
        )

    def log_from_search(self, query: str, payload: dict[str, Any]) -> dict[str, Any] | None:
        domains: list[str] = []
        for s in payload.get("sources") or []:
            for d in (s.get("domains") or "").split() if isinstance(s.get("domains"), str) else (s.get("domains") or []):
                d = str(d).lower()
                if d and d not in domains:
                    domains.append(d)
        return self.log_query(
            query,
            channel="explore",
            result_count=int(payload.get("count") or 0),
            domains=domains,
            payload=payload,
        )

    # --- vistas ---

    def summary(self) -> dict[str, Any]:
        events = self._store.list_events()
        return {
            **an.summary(events),
            "notice": TRANSPARENCY_NOTICE,
            "anonymous": True,
        }

    def top_queries(self, *, limit: int = 20) -> dict[str, Any]:
        events = self._store.list_events()
        rows = an.top_queries(events, limit=limit)
        return {"count": len(rows), "items": rows}

    def empty_queries(self, *, limit: int = 20) -> dict[str, Any]:
        events = self._store.list_events()
        rows = an.empty_queries(events, limit=limit)
        return {"count": len(rows), "items": rows, "insight": "Posibles vacíos de catálogo"}

    def domains(self, *, limit: int = 20) -> dict[str, Any]:
        events = self._store.list_events()
        rows = an.domain_ranking(events, limit=limit)
        return {"count": len(rows), "items": rows}

    def emerging(self, *, limit: int = 20) -> dict[str, Any]:
        events = self._store.list_events()
        rows = an.emerging_terms(
            events, limit=limit, known_domains=self._known_domains()
        )
        return {"count": len(rows), "items": rows, "insight": "Candidatos a taxonomía / conectores"}

    def timeline(self, *, days: int = 30) -> dict[str, Any]:
        events = self._store.list_events()
        rows = an.timeline(events, days=days)
        return {"days": days, "items": rows}

    def wordcloud(self, *, limit: int = 40) -> dict[str, Any]:
        events = self._store.list_events()
        rows = an.wordcloud(
            events,
            limit=limit,
            known_domains=self._known_domains(),
        )
        return {"count": len(rows), "items": rows}

    def dashboard(self) -> dict[str, Any]:
        """Payload único para el Workbench."""
        return {
            "notice": TRANSPARENCY_NOTICE,
            "summary": self.summary(),
            "wordcloud": self.wordcloud(limit=36)["items"],
            "top_queries": self.top_queries(limit=12)["items"],
            "empty_queries": self.empty_queries(limit=12)["items"],
            "domains": self.domains(limit=12)["items"],
            "emerging": self.emerging(limit=12)["items"],
            "timeline": self.timeline(days=14)["items"],
            "anonymous": True,
            "ai": False,
        }

    def _known_domains(self) -> set[str]:
        if self._metadata is None:
            return {
                "clima",
                "hidrologia",
                "biodiversidad",
                "oceanos_costas",
                "suelos",
                "agricultura",
                "poblacion",
                "observacion_tierra",
            }
        try:
            items = self._metadata.list_domains() or []
            return {str(d.get("domain_id") or "").lower() for d in items if d.get("domain_id")}
        except Exception:
            return set()
