"""
Source Discovery Assistant — Fase 6 MVP.

Analiza URLs desconocidas y genera propuestas de incorporación.
NO modifica catálogo. NO crea conectores. Curaduría humana obligatoria.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from backend.source_discovery.analyzer import analyze_url
from backend.source_discovery.store import CandidateStore

if TYPE_CHECKING:
    from backend.discovery.engine import DiscoveryEngine
    from backend.knowledge_graph.engine import KnowledgeGraphEngine
    from backend.metadata.engine import MetadataEngine
    from backend.recommendation.engine import RecommendationEngine

DEFAULT_DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "source_discovery"


class SourceDiscoveryAssistant:
    """Asistente de descubrimiento de fuentes candidatas."""

    status = "mvp"

    def __init__(
        self,
        discovery: DiscoveryEngine | None = None,
        metadata: MetadataEngine | None = None,
        knowledge_graph: KnowledgeGraphEngine | None = None,
        recommendation: RecommendationEngine | None = None,
        store: CandidateStore | None = None,
        data_dir: Path | str | None = None,
    ) -> None:
        self._discovery = discovery
        self._metadata = metadata
        self._kg = knowledge_graph
        self._recommendation = recommendation
        self._store = store or CandidateStore(data_dir or DEFAULT_DATA_DIR)

    def info(self) -> dict[str, Any]:
        return {
            "engine": "SourceDiscoveryAssistant",
            "status": self.status,
            "auto_creates_connectors": False,
            "auto_updates_catalog": False,
            "auto_approves": False,
            "human_curation": True,
            "principle": "El sistema propone. Los curadores deciden.",
            "ai": False,
            "embeddings": False,
            "llm": False,
            "built_from": [
                "url_heuristics",
                "discovery",
                "metadata",
                "knowledge_graph",
                "recommendation",
            ],
            "supported_hints": [
                "ArcGIS REST",
                "FeatureServer",
                "MapServer",
                "STAC",
                "WMS",
                "WFS",
                "API JSON",
                "Portales",
                "Repositorios",
            ],
            **self._store.stats(),
        }

    def analyze(self, url: str, *, persist: bool = True) -> dict[str, Any]:
        """Analiza URL y opcionalmente persiste el candidato."""
        base = analyze_url(url)
        if not base.get("ok"):
            return {
                "status": "error",
                "error": base.get("error", "Análisis fallido"),
                "curation": "human_required",
                "auto_applied": False,
            }

        enrichment = self._enrich(base)
        candidate = {
            "id": str(uuid4()),
            "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "status": "candidate_source",
            "name": base["name"],
            "source_type": base["source_type"],
            "institution": base["institution"],
            "institution_full": base.get("institution_full"),
            "domains": base.get("domains") or [],
            "access_methods": base.get("access_methods") or [],
            "potential_resources": base.get("potential_resources") or [],
            "confidence": base["confidence"],
            "url": base["url"],
            "host": base.get("host"),
            "signals": base.get("signals"),
            "related_known_sources": enrichment.get("related_known_sources", []),
            "recommended_domains": enrichment.get("recommended_domains", []),
            "domains_in_taxonomy": enrichment.get("domains_in_taxonomy", []),
            "domains_proposed": enrichment.get("domains_proposed", []),
            "already_registered": enrichment.get("already_registered", False),
            "curation": "human_required",
            "auto_applied": False,
            "catalog_modified": False,
            "connector_created": False,
            "analysis_method": "heuristic_url_patterns",
            "ai": False,
        }

        # Ajuste de confianza si ya está registrada o hay solapamiento KG
        if candidate["already_registered"]:
            candidate["confidence"] = min(candidate["confidence"], 0.4)
            candidate["note"] = (
                "La URL parece corresponder a una fuente MVP ya registrada. "
                "No se debe duplicar sin curaduría."
            )
        elif candidate["related_known_sources"]:
            candidate["confidence"] = round(
                min(0.99, candidate["confidence"] + 0.05),
                2,
            )

        if persist:
            self._store.add(candidate)
        return candidate

    def list_candidates(self, *, limit: int | None = 50) -> list[dict[str, Any]]:
        return self._store.list(limit=limit)

    def get_candidate(self, candidate_id: str) -> dict[str, Any] | None:
        return self._store.get(candidate_id)

    def _enrich(self, base: dict[str, Any]) -> dict[str, Any]:
        """Enriquece con Discovery / Metadata / KG / Recommendation (sin IA)."""
        related: list[dict[str, str]] = []
        recommended_domains: list[str] = list(base.get("domains") or [])
        already = False
        host = (base.get("host") or "").lower()
        url = (base.get("url") or "").lower()

        if self._discovery is not None:
            for source in self._discovery.list_sources():
                homepage = (source.get("homepage") or "").lower()
                sid = source.get("source_id", "")
                name = (source.get("source") or "").lower()
                homepage_host = ""
                if homepage:
                    try:
                        from urllib.parse import urlparse

                        homepage_host = (urlparse(homepage).hostname or "").lower()
                        if homepage_host.startswith("www."):
                            homepage_host = homepage_host[4:]
                    except Exception:
                        homepage_host = ""
                host_related = bool(
                    homepage_host
                    and (
                        host == homepage_host
                        or host.endswith("." + homepage_host)
                        or homepage_host in host
                    )
                )
                if homepage and (homepage in url or host in homepage or host_related):
                    already = True
                    related.append(
                        {
                            "source_id": sid,
                            "source": source.get("source", ""),
                            "relation": "host_or_homepage_match",
                        }
                    )
                elif name and name in url:
                    related.append(
                        {
                            "source_id": sid,
                            "source": source.get("source", ""),
                            "relation": "name_in_url",
                        }
                    )

        # Dominios vía Recommendation si hay keywords/dominios inferidos
        if self._recommendation is not None:
            for domain in base.get("domains") or []:
                payload = self._recommendation.recommend_by_domain(domain, limit=3)
                for item in payload.get("recommendations") or []:
                    related.append(
                        {
                            "source_id": item.get("source_id", ""),
                            "source": item.get("source", ""),
                            "relation": f"shared_domain:{domain}",
                        }
                    )
                if domain not in recommended_domains:
                    recommended_domains.append(domain)

        # KG/Metadata: dominios conocidos vs propuestos (ampliación futura)
        if self._metadata is not None:
            known_domains = {
                d["domain_id"] for d in self._metadata.list_domains()
            }
            inferred = list(base.get("domains") or [])
            recommended_domains = inferred
            base["domains_in_taxonomy"] = [
                d for d in inferred if d in known_domains
            ]
            base["domains_proposed"] = [
                d for d in inferred if d not in known_domains
            ]

        # Deduplicar related
        seen: set[str] = set()
        unique_related: list[dict[str, str]] = []
        for item in related:
            key = f"{item.get('source_id')}|{item.get('relation')}"
            if key not in seen and item.get("source_id"):
                seen.add(key)
                unique_related.append(item)

        return {
            "related_known_sources": unique_related[:10],
            "recommended_domains": recommended_domains,
            "already_registered": already,
            "domains_in_taxonomy": base.get("domains_in_taxonomy", []),
            "domains_proposed": base.get("domains_proposed", []),
        }
