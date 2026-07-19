"""
Recommendation Engine — Fase 4 MVP.

Recomendaciones explicables basadas en el Knowledge Graph.
Sin IA, embeddings, LLMs ni vector DBs.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from backend.knowledge_graph.models import node_id
from backend.recommendation.scoring import (
    WEIGHT_DOMAIN_MATCH,
    WEIGHT_KEYWORD_EXACT,
    WEIGHT_RELATED_DOMAIN,
    WEIGHT_RELATED_KEYWORD,
    WEIGHT_RESOURCE_MATCH,
    WEIGHT_SOURCE_MATCH,
    add_reason,
    add_relation,
    empty_accumulator,
    expand_query_tokens,
    finalize,
    normalize_token,
    official_national_bonus,
)

if TYPE_CHECKING:
    from backend.discovery.engine import DiscoveryEngine
    from backend.knowledge_graph.engine import KnowledgeGraphEngine
    from backend.metadata.engine import MetadataEngine


class RecommendationEngine:
    """Motor de recomendación determinista y trazable."""

    status = "mvp"

    def __init__(
        self,
        knowledge_graph: KnowledgeGraphEngine | None = None,
        discovery: DiscoveryEngine | None = None,
        metadata: MetadataEngine | None = None,
    ) -> None:
        self._kg = knowledge_graph
        self._discovery = discovery
        self._metadata = metadata

    def bind(
        self,
        knowledge_graph: KnowledgeGraphEngine,
        discovery: DiscoveryEngine | None = None,
        metadata: MetadataEngine | None = None,
    ) -> None:
        self._kg = knowledge_graph
        if discovery is not None:
            self._discovery = discovery
        if metadata is not None:
            self._metadata = metadata

    # --- API pública ---

    def recommend(self, query: str, *, limit: int = 10) -> dict[str, Any]:
        """Recomienda fuentes a partir de texto libre (keyword/dominio/fuente/recurso)."""
        q = (query or "").strip()
        if not q:
            return self._empty_response(query="", mode="query")
        if self._kg is None:
            return self._empty_response(query=q, mode="query")

        tokens = expand_query_tokens(q)
        accumulators = self._new_accumulators()

        self._score_keyword_hits(tokens, accumulators)
        self._score_domain_hits(tokens, accumulators)
        self._score_source_hits(tokens, accumulators)
        self._score_resource_hits(tokens, accumulators)
        self._apply_official_bonus(accumulators)

        recommendations = self._rank(accumulators, limit=limit)
        return {
            "query": q,
            "tokens": tokens,
            "mode": "query",
            "count": len(recommendations),
            "recommendations": recommendations,
            "explainability": "required",
            "method": "knowledge_graph_relations",
            "ai": False,
        }

    def recommend_by_domain(self, domain_id: str, *, limit: int = 10) -> dict[str, Any]:
        domain_id = normalize_token(domain_id)
        if self._kg is None:
            return self._empty_response(query=domain_id, mode="domain")

        payload = self._kg.resources_by_domain(domain_id)
        if payload is None:
            return {
                "query": domain_id,
                "mode": "domain",
                "count": 0,
                "recommendations": [],
                "error": f"Dominio no encontrado en el grafo: {domain_id}",
            }

        accumulators = self._new_accumulators()
        domain_nid = node_id("Domain", domain_id)

        for source_id in payload.get("source_ids", []):
            acc = accumulators.get(source_id)
            if acc is None:
                continue
            acc["score_raw"] += WEIGHT_DOMAIN_MATCH
            add_reason(acc, f"dominio {domain_id}")
            if domain_id not in acc["matched_domains"]:
                acc["matched_domains"].append(domain_id)

        # Asociar recursos y relaciones reales Resource→Domain
        for resource_key in payload.get("resources", []):
            res_nid = node_id("Resource", resource_key)
            res_node = self._kg.graph.get_node(res_nid)
            if res_node is None:
                continue
            sources = self._kg.graph.neighbors(
                res_nid, direction="in", rel_type="contains"
            )
            for src in sources:
                sid = self._source_key(src["id"])
                acc = accumulators.get(sid)
                if acc is None:
                    continue
                acc["score_raw"] += WEIGHT_RELATED_DOMAIN
                add_reason(acc, f"recurso {resource_key} pertenece a {domain_id}")
                add_relation(acc, "belongs_to", res_nid, domain_nid)
                add_relation(acc, "contains", src["id"], res_nid)
                if resource_key not in acc["matched_resources"]:
                    acc["matched_resources"].append(resource_key)

        self._apply_official_bonus(accumulators)
        recommendations = self._rank(accumulators, limit=limit)
        return {
            "query": domain_id,
            "mode": "domain",
            "count": len(recommendations),
            "recommendations": recommendations,
            "explainability": "required",
            "method": "knowledge_graph_relations",
            "ai": False,
        }

    def recommend_by_source(self, source_id: str, *, limit: int = 10) -> dict[str, Any]:
        """Fuentes/recursos relacionados a una fuente (dominios compartidos)."""
        source_id = normalize_token(source_id)
        if self._kg is None:
            return self._empty_response(query=source_id, mode="source")

        source_payload = self._kg.resources_by_source(source_id)
        if source_payload is None:
            return {
                "query": source_id,
                "mode": "source",
                "count": 0,
                "recommendations": [],
                "error": f"Fuente no encontrada en el grafo: {source_id}",
            }

        accumulators = self._new_accumulators()
        self_acc = accumulators.get(source_id)
        if self_acc is not None:
            self_acc["score_raw"] += WEIGHT_SOURCE_MATCH
            add_reason(self_acc, f"fuente consultada {source_payload['source']}")
            source_nid = node_id("Source", source_id)
            insts = self._kg.graph.neighbors(
                source_nid, direction="in", rel_type="publishes"
            )
            for inst in insts:
                add_relation(self_acc, "publishes", inst["id"], source_nid)
            for rid in source_payload.get("resources", []):
                add_relation(self_acc, "contains", source_nid, node_id("Resource", rid))
                if rid not in self_acc["matched_resources"]:
                    self_acc["matched_resources"].append(rid)
            for d in source_payload.get("domains", []):
                if d not in self_acc["matched_domains"]:
                    self_acc["matched_domains"].append(d)

        # Fuentes que comparten dominios
        for domain in source_payload.get("domains", []):
            related = self._kg.resources_by_domain(domain) or {}
            domain_nid = node_id("Domain", domain)
            for other_id in related.get("source_ids", []):
                if other_id == source_id:
                    continue
                acc = accumulators.get(other_id)
                if acc is None:
                    continue
                acc["score_raw"] += WEIGHT_RELATED_DOMAIN
                add_reason(acc, f"comparte dominio {domain} con {source_id}")
                if domain not in acc["matched_domains"]:
                    acc["matched_domains"].append(domain)
                for rid in related.get("resources", []):
                    if rid.startswith(f"{other_id}:") and rid not in acc["matched_resources"]:
                        acc["matched_resources"].append(rid)
                        add_relation(
                            acc,
                            "belongs_to",
                            node_id("Resource", rid),
                            domain_nid,
                        )
                        add_relation(
                            acc,
                            "contains",
                            node_id("Source", other_id),
                            node_id("Resource", rid),
                        )

        self._apply_official_bonus(accumulators)
        recommendations = self._rank(accumulators, limit=limit)
        return {
            "query": source_id,
            "mode": "source",
            "count": len(recommendations),
            "recommendations": recommendations,
            "seed_source": source_payload,
            "explainability": "required",
            "method": "knowledge_graph_relations",
            "ai": False,
        }

    def recommend_by_resource(self, resource_id: str, *, limit: int = 10) -> dict[str, Any]:
        """Recursos/fuentes relacionados por dominio y keywords del recurso semilla."""
        resource_id = resource_id.strip()
        if self._kg is None:
            return self._empty_response(query=resource_id, mode="resource")

        res_nid = node_id("Resource", resource_id)
        res_node = self._kg.graph.get_node(res_nid)
        if res_node is None:
            # permitir resource_id sin prefijo Type
            alt = resource_id
            if not self._kg.graph.get_node(node_id("Resource", alt)):
                return {
                    "query": resource_id,
                    "mode": "resource",
                    "count": 0,
                    "recommendations": [],
                    "error": f"Recurso no encontrado en el grafo: {resource_id}",
                }
            res_nid = node_id("Resource", alt)
            res_node = self._kg.graph.get_node(res_nid)

        assert res_node is not None
        accumulators = self._new_accumulators()

        # Fuente dueña
        owners = self._kg.graph.neighbors(res_nid, direction="in", rel_type="contains")
        for src in owners:
            sid = self._source_key(src["id"])
            acc = accumulators.get(sid)
            if acc is None:
                continue
            acc["score_raw"] += WEIGHT_RESOURCE_MATCH + WEIGHT_SOURCE_MATCH
            add_reason(acc, f"contiene recurso {resource_id}")
            add_relation(acc, "contains", src["id"], res_nid)
            if resource_id not in acc["matched_resources"]:
                acc["matched_resources"].append(resource_id)

        # Dominios del recurso
        owner_ids = {self._source_key(s["id"]) for s in owners}
        domains = self._kg.graph.neighbors(res_nid, direction="out", rel_type="belongs_to")
        for dom in domains:
            dkey = self._node_key(dom["id"])
            domain_payload = self._kg.resources_by_domain(dkey) or {}
            for other_id in domain_payload.get("source_ids", []):
                acc = accumulators.get(other_id)
                if acc is None:
                    continue
                if other_id in owner_ids:
                    acc["score_raw"] += WEIGHT_DOMAIN_MATCH
                else:
                    acc["score_raw"] += WEIGHT_RELATED_DOMAIN
                add_reason(acc, f"dominio compartido {dkey}")
                add_relation(acc, "belongs_to", res_nid, dom["id"])
                if dkey not in acc["matched_domains"]:
                    acc["matched_domains"].append(dkey)
            for rid in domain_payload.get("resources", []):
                if rid == resource_id:
                    continue
                other_res = node_id("Resource", rid)
                other_sources = self._kg.graph.neighbors(
                    other_res, direction="in", rel_type="contains"
                )
                for osrc in other_sources:
                    sid = self._source_key(osrc["id"])
                    acc = accumulators.get(sid)
                    if acc is None:
                        continue
                    if rid not in acc["matched_resources"]:
                        acc["matched_resources"].append(rid)
                    add_relation(acc, "belongs_to", other_res, dom["id"])
                    add_relation(acc, "contains", osrc["id"], other_res)

        # Keywords del recurso
        keywords = self._kg.graph.neighbors(
            res_nid, direction="out", rel_type="associated_with"
        )
        for kw in keywords:
            kw_key = self._node_key(kw["id"])
            related_resources = self._kg.graph.neighbors(
                kw["id"], direction="in", rel_type="associated_with"
            )
            for other in related_resources:
                if other["id"] == res_nid:
                    continue
                other_sources = self._kg.graph.neighbors(
                    other["id"], direction="in", rel_type="contains"
                )
                for osrc in other_sources:
                    sid = self._source_key(osrc["id"])
                    acc = accumulators.get(sid)
                    if acc is None:
                        continue
                    acc["score_raw"] += WEIGHT_RELATED_KEYWORD
                    add_reason(acc, f"keyword compartida {kw_key}")
                    add_relation(acc, "associated_with", other["id"], kw["id"])
                    add_relation(acc, "associated_with", res_nid, kw["id"])
                    rid = self._node_key(other["id"])
                    if rid not in acc["matched_resources"]:
                        acc["matched_resources"].append(rid)
                    if kw_key not in acc["matched_keywords"]:
                        acc["matched_keywords"].append(kw_key)

        self._apply_official_bonus(accumulators)
        recommendations = self._rank(accumulators, limit=limit)
        return {
            "query": resource_id,
            "mode": "resource",
            "count": len(recommendations),
            "recommendations": recommendations,
            "explainability": "required",
            "method": "knowledge_graph_relations",
            "ai": False,
        }

    def info(self) -> dict[str, Any]:
        return {
            "engine": "RecommendationEngine",
            "status": self.status,
            "ai": False,
            "embeddings": False,
            "llm": False,
            "explainability": "required",
            "built_from": ["knowledge_graph"],
            "criteria": [
                "domain_match",
                "keyword_match",
                "kg_relations",
                "related_sources",
                "related_resources",
            ],
            "curation": "human",
            "read_only": True,
        }

    # --- internos ---

    def _new_accumulators(self) -> dict[str, dict[str, Any]]:
        assert self._kg is not None
        accs: dict[str, dict[str, Any]] = {}
        for node in self._kg.list_nodes("Source"):
            sid = self._source_key(node["id"])
            accs[sid] = empty_accumulator(sid, node["label"])
        return accs

    def _score_keyword_hits(
        self,
        tokens: list[str],
        accumulators: dict[str, dict[str, Any]],
    ) -> None:
        assert self._kg is not None
        for token in tokens:
            kw_nid = node_id("Keyword", token)
            kw_node = self._kg.graph.get_node(kw_nid)
            if kw_node is None:
                continue
            resources = self._kg.graph.neighbors(
                kw_nid, direction="in", rel_type="associated_with"
            )
            for res in resources:
                sources = self._kg.graph.neighbors(
                    res["id"], direction="in", rel_type="contains"
                )
                for src in sources:
                    sid = self._source_key(src["id"])
                    acc = accumulators.get(sid)
                    if acc is None:
                        continue
                    acc["score_raw"] += WEIGHT_KEYWORD_EXACT
                    add_reason(acc, f"keyword {token}")
                    add_relation(acc, "associated_with", res["id"], kw_nid)
                    add_relation(acc, "contains", src["id"], res["id"])
                    rid = self._node_key(res["id"])
                    if rid not in acc["matched_resources"]:
                        acc["matched_resources"].append(rid)
                    if token not in acc["matched_keywords"]:
                        acc["matched_keywords"].append(token)

    def _score_domain_hits(
        self,
        tokens: list[str],
        accumulators: dict[str, dict[str, Any]],
    ) -> None:
        assert self._kg is not None
        for token in tokens:
            domain_payload = self._kg.resources_by_domain(token)
            if domain_payload is None:
                continue
            domain_nid = node_id("Domain", token)
            for source_id in domain_payload.get("source_ids", []):
                acc = accumulators.get(source_id)
                if acc is None:
                    continue
                acc["score_raw"] += WEIGHT_DOMAIN_MATCH
                add_reason(acc, f"dominio {token}")
                if token not in acc["matched_domains"]:
                    acc["matched_domains"].append(token)
            for rid in domain_payload.get("resources", []):
                res_nid = node_id("Resource", rid)
                sources = self._kg.graph.neighbors(
                    res_nid, direction="in", rel_type="contains"
                )
                for src in sources:
                    sid = self._source_key(src["id"])
                    acc = accumulators.get(sid)
                    if acc is None:
                        continue
                    add_relation(acc, "belongs_to", res_nid, domain_nid)
                    add_relation(acc, "contains", src["id"], res_nid)
                    if rid not in acc["matched_resources"]:
                        acc["matched_resources"].append(rid)

    def _score_source_hits(
        self,
        tokens: list[str],
        accumulators: dict[str, dict[str, Any]],
    ) -> None:
        assert self._kg is not None
        for token in tokens:
            # match source_id o label
            for node in self._kg.list_nodes("Source"):
                sid = self._source_key(node["id"])
                label = normalize_token(node["label"])
                if token == sid or token == label or token in label:
                    acc = accumulators.get(sid)
                    if acc is None:
                        continue
                    acc["score_raw"] += WEIGHT_SOURCE_MATCH
                    add_reason(acc, f"fuente {node['label']}")
                    # relación publishes desde institución
                    insts = self._kg.graph.neighbors(
                        node["id"], direction="in", rel_type="publishes"
                    )
                    for inst in insts:
                        add_relation(acc, "publishes", inst["id"], node["id"])
                    resources = self._kg.graph.neighbors(
                        node["id"], direction="out", rel_type="contains"
                    )
                    for res in resources:
                        add_relation(acc, "contains", node["id"], res["id"])
                        rid = self._node_key(res["id"])
                        if rid not in acc["matched_resources"]:
                            acc["matched_resources"].append(rid)

    def _score_resource_hits(
        self,
        tokens: list[str],
        accumulators: dict[str, dict[str, Any]],
    ) -> None:
        assert self._kg is not None
        for node in self._kg.list_nodes("Resource"):
            rid = self._node_key(node["id"])
            label = normalize_token(node["label"])
            rid_norm = normalize_token(rid)
            if not any(t in rid_norm or t in label or rid_norm.endswith(t) for t in tokens):
                continue
            sources = self._kg.graph.neighbors(
                node["id"], direction="in", rel_type="contains"
            )
            for src in sources:
                sid = self._source_key(src["id"])
                acc = accumulators.get(sid)
                if acc is None:
                    continue
                acc["score_raw"] += WEIGHT_RESOURCE_MATCH
                add_reason(acc, f"recurso {rid}")
                add_relation(acc, "contains", src["id"], node["id"])
                if rid not in acc["matched_resources"]:
                    acc["matched_resources"].append(rid)
                for dom in self._kg.graph.neighbors(
                    node["id"], direction="out", rel_type="belongs_to"
                ):
                    add_relation(acc, "belongs_to", node["id"], dom["id"])
                    dkey = self._node_key(dom["id"])
                    if dkey not in acc["matched_domains"]:
                        acc["matched_domains"].append(dkey)

    def _apply_official_bonus(self, accumulators: dict[str, dict[str, Any]]) -> None:
        for sid, acc in accumulators.items():
            if not acc["reason"]:
                continue
            bonus, reason = official_national_bonus(sid)
            if bonus and reason:
                acc["score_raw"] += bonus
                add_reason(acc, reason)
                # Trazabilidad: relación publishes de la institución nacional
                assert self._kg is not None
                source_nid = node_id("Source", sid)
                insts = self._kg.graph.neighbors(
                    source_nid, direction="in", rel_type="publishes"
                )
                for inst in insts:
                    add_relation(acc, "publishes", inst["id"], source_nid)

    def _rank(
        self,
        accumulators: dict[str, dict[str, Any]],
        *,
        limit: int,
    ) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for acc in accumulators.values():
            item = finalize(acc)
            if item is not None:
                results.append(item)
        results.sort(key=lambda x: (-x["score"], x["source"]))
        return results[:limit]

    @staticmethod
    def _source_key(nid: str) -> str:
        return nid.split(":", 1)[1] if ":" in nid else nid

    @staticmethod
    def _node_key(nid: str) -> str:
        return nid.split(":", 1)[1] if ":" in nid else nid

    @staticmethod
    def _empty_response(*, query: str, mode: str) -> dict[str, Any]:
        return {
            "query": query,
            "mode": mode,
            "count": 0,
            "recommendations": [],
            "explainability": "required",
            "method": "knowledge_graph_relations",
            "ai": False,
        }
