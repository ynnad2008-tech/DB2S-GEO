"""
Decision Support Engine — Fase 8 MVP.

Transforma una consulta orientada a problemas en rutas de acción concretas.
Construye sobre Recommendation Engine + Discovery (acceso). Sin IA.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from backend.decision_support.actions import (
    ACTION_CATEGORIES,
    category_for_intent,
    match_need_profile,
    where_for_source,
)
from backend.decision_support.concepts import expand_concepts, primary_need_label
from backend.decision_support.intents import INTENT_LABELS, detect_intents
from backend.recommendation.scoring import normalize_token

if TYPE_CHECKING:
    from backend.discovery.engine import DiscoveryEngine
    from backend.knowledge_graph.engine import KnowledgeGraphEngine
    from backend.metadata.engine import MetadataEngine
    from backend.recommendation.engine import RecommendationEngine

MVP_SOURCES = frozenset({"ideam", "invemar", "gbif", "fao", "worldpop", "gee"})


class DecisionSupportEngine:
    """Motor de apoyo a la decisión: necesidad → rutas de acción justificadas."""

    status = "mvp"

    def __init__(
        self,
        recommendation: RecommendationEngine | None = None,
        discovery: DiscoveryEngine | None = None,
        metadata: MetadataEngine | None = None,
        knowledge_graph: KnowledgeGraphEngine | None = None,
    ) -> None:
        self._recommendation = recommendation
        self._discovery = discovery
        self._metadata = metadata
        self._kg = knowledge_graph

    def bind(
        self,
        recommendation: RecommendationEngine,
        discovery: DiscoveryEngine | None = None,
        metadata: MetadataEngine | None = None,
        knowledge_graph: KnowledgeGraphEngine | None = None,
    ) -> None:
        self._recommendation = recommendation
        if discovery is not None:
            self._discovery = discovery
        if metadata is not None:
            self._metadata = metadata
        if knowledge_graph is not None:
            self._kg = knowledge_graph

    def info(self) -> dict[str, Any]:
        return {
            "engine": "DecisionSupportEngine",
            "status": self.status,
            "ai": False,
            "embeddings": False,
            "llm": False,
            "principle": "Consulta → necesidad → ruta → fuente → recursos → justificación",
            "built_from": ["recommendation", "discovery", "knowledge_graph", "metadata"],
            "intents": list(INTENT_LABELS.keys()),
            "action_categories": dict(ACTION_CATEGORIES),
            "explainability": "required",
            "curation": "human",
            "read_only": True,
            "invents_sources": False,
        }

    def advise(self, query: str, *, limit: int = 6) -> dict[str, Any]:
        """
        Responde una consulta orientada a problemas con rutas de acción.

        Cada ruta incluye: qué hacer, dónde, fuente, recursos y por qué.
        """
        q = (query or "").strip()
        if not q:
            return self._empty(query="")

        intents = detect_intents(q)
        concepts = expand_concepts(q)
        need = primary_need_label(concepts, q)
        query_norm = normalize_token(q)

        profile = match_need_profile(concepts, query_norm)
        if profile is not None:
            routes = self._routes_from_profile(profile, intents, limit=limit)
            need = profile.get("need") or need
        else:
            routes = self._routes_from_recommendations(q, concepts, intents, limit=limit)

        return {
            "query": q,
            "need": need,
            "intents": intents,
            "intent_labels": [INTENT_LABELS.get(i, i) for i in intents],
            "concepts": concepts,
            "count": len(routes),
            "routes": routes,
            "explainability": "required",
            "method": "decision_support_action_routes",
            "ai": False,
            "principle": "El sistema orienta; la curaduría humana decide.",
        }

    # --- construcción de rutas ---

    def _routes_from_profile(
        self,
        profile: dict[str, Any],
        intents: list[str],
        *,
        limit: int,
    ) -> list[dict[str, Any]]:
        routes: list[dict[str, Any]] = []
        primary_intent = intents[0] if intents else "estudiar"

        for idx, template in enumerate(profile.get("routes") or [], start=1):
            if len(routes) >= limit:
                break
            source_id = template["source_id"]
            if source_id not in MVP_SOURCES:
                continue

            source_meta = self._source_meta(source_id)
            if source_meta is None:
                continue

            # Preferir categoría del perfil; ajustar si la intención es descargar
            category = template.get("category") or category_for_intent(primary_intent, source_id)
            if primary_intent == "descargar" and source_id != "gee":
                category = "descargar_datos"

            resource_ids = list(template.get("resource_ids") or [])
            resources = self._enrich_resources(source_id, resource_ids, concepts_hint=None)

            # Enriquecer justificación con Recommendation Engine si hay match
            rec_reasons, relations, score = self._justify_source(
                source_id, " ".join(resource_ids) or source_id
            )
            why = list(rec_reasons) if rec_reasons else []
            if template.get("why_default") and template["why_default"] not in why:
                why.insert(0, template["why_default"])
            if not why:
                why = ["Coincide con la necesidad detectada en el catálogo MVP."]

            routes.append(
                self._route_item(
                    rank=idx,
                    title=template.get("title") or ACTION_CATEGORIES.get(category, category),
                    category=category,
                    what_to_do=template.get("what_to_do") or INTENT_LABELS.get(primary_intent, ""),
                    where=where_for_source(source_id, category),
                    source_id=source_id,
                    source=source_meta.get("source") or source_id,
                    institution=source_meta.get("institution"),
                    resources=resources,
                    why=why,
                    score=score,
                    relations_used=relations,
                    intents=intents,
                )
            )
        return routes

    def _routes_from_recommendations(
        self,
        query: str,
        concepts: list[str],
        intents: list[str],
        *,
        limit: int,
    ) -> list[dict[str, Any]]:
        if self._recommendation is None:
            return []

        # Consulta enriquecida con conceptos para mejor recall
        search_q = query
        if concepts:
            # Usar los conceptos más informativos (no stopwords cortas)
            extra = [c for c in concepts if len(c) > 3][:6]
            if extra:
                search_q = f"{query} {' '.join(extra)}"

        payload = self._recommendation.recommend(search_q, limit=max(limit, 8))
        recommendations = payload.get("recommendations") or []

        # Si la consulta enriquecida falla, reintentar con query original
        if not recommendations:
            payload = self._recommendation.recommend(query, limit=max(limit, 8))
            recommendations = payload.get("recommendations") or []

        # Segunda pasada por conceptos individuales si aún vacío
        if not recommendations and concepts:
            for concept in concepts:
                payload = self._recommendation.recommend(concept, limit=5)
                recommendations.extend(payload.get("recommendations") or [])
                if len(recommendations) >= limit:
                    break
            # Deduplicar por source_id conservando mejor score
            best: dict[str, dict[str, Any]] = {}
            for item in recommendations:
                sid = item["source_id"]
                if sid not in best or item["score"] > best[sid]["score"]:
                    best[sid] = item
            recommendations = sorted(best.values(), key=lambda x: -x["score"])

        primary_intent = intents[0] if intents else "estudiar"
        routes: list[dict[str, Any]] = []
        seen: set[str] = set()

        for item in recommendations:
            sid = item["source_id"]
            if sid in seen or sid not in MVP_SOURCES:
                continue
            seen.add(sid)
            if len(routes) >= limit:
                break

            category = category_for_intent(primary_intent, sid)
            # Si hay varias intenciones y una es descargar + analizar, abrir rutas paralelas
            titles = {
                "descargar_datos": "Descargar datos",
                "consultar_informacion_institucional": "Consultar información institucional",
                "consumir_apis": "Consumir APIs",
                "utilizar_plataformas_de_analisis": "Utilizar plataformas de análisis",
                "realizar_analisis_geoespacial_avanzado": "Análisis geoespacial avanzado",
                "obtener_informacion_complementaria": "Información complementaria",
            }

            resource_ids = list(item.get("resources") or [])
            resources = self._enrich_resources(sid, resource_ids, concepts_hint=concepts)

            what = self._what_to_do(primary_intent, sid, category, resources)
            why = list(item.get("reason") or [])
            if not why:
                why = ["Relaciones del Knowledge Graph alineadas con la consulta."]

            routes.append(
                self._route_item(
                    rank=len(routes) + 1,
                    title=titles.get(category, item.get("source") or sid),
                    category=category,
                    what_to_do=what,
                    where=where_for_source(sid, category),
                    source_id=sid,
                    source=item.get("source") or sid,
                    institution=self._source_meta(sid) or {},
                    resources=resources,
                    why=why,
                    score=item.get("score"),
                    relations_used=list(item.get("relations_used") or []),
                    intents=intents,
                )
            )

        # Si intención incluye descargar y analizar, duplicar ruta GEE vs institucional cuando aplique
        if "descargar" in intents and "analizar" in intents:
            routes = self._ensure_download_and_analysis_split(routes, intents, limit=limit)

        return routes[:limit]

    def _ensure_download_and_analysis_split(
        self,
        routes: list[dict[str, Any]],
        intents: list[str],
        *,
        limit: int,
    ) -> list[dict[str, Any]]:
        """Garantiza rutas paralelas descarga vs análisis cuando ambas intenciones existen."""
        has_download = any(r["category"] == "descargar_datos" for r in routes)
        has_analysis = any(
            r["category"]
            in (
                "realizar_analisis_geoespacial_avanzado",
                "utilizar_plataformas_de_analisis",
            )
            for r in routes
        )
        if has_download and has_analysis:
            return routes

        out = list(routes)
        if not has_analysis:
            meta = self._source_meta("gee")
            if meta and len(out) < limit:
                resources = self._enrich_resources(
                    "gee", ["gee:sentinel2", "gee:landsat"], concepts_hint=None
                )
                out.append(
                    self._route_item(
                        rank=len(out) + 1,
                        title="Análisis geoespacial avanzado",
                        category="realizar_analisis_geoespacial_avanzado",
                        what_to_do=(
                            "Realizar análisis espacial y series temporales "
                            "en Google Earth Engine."
                        ),
                        where=where_for_source("gee", "realizar_analisis_geoespacial_avanzado"),
                        source_id="gee",
                        source=meta.get("source") or "Google Earth Engine",
                        institution=meta.get("institution"),
                        resources=resources,
                        why=["Plataforma de análisis geoespacial avanzado del catálogo MVP."],
                        score=None,
                        relations_used=[],
                        intents=intents,
                    )
                )
        if not has_download:
            meta = self._source_meta("ideam")
            if meta and len(out) < limit:
                resources = self._enrich_resources(
                    "ideam", ["ideam:precipitacion"], concepts_hint=None
                )
                out.append(
                    self._route_item(
                        rank=len(out) + 1,
                        title="Descargar datos",
                        category="descargar_datos",
                        what_to_do="Descargar o consultar datos desde portal/API institucional.",
                        where=where_for_source("ideam", "descargar_datos"),
                        source_id="ideam",
                        source=meta.get("source") or "IDEAM",
                        institution=meta.get("institution"),
                        resources=resources,
                        why=["Fuente oficial nacional con acceso portal y API."],
                        score=None,
                        relations_used=[],
                        intents=intents,
                    )
                )
        # Re-numerar
        for i, r in enumerate(out, start=1):
            r["rank"] = i
        return out

    # --- helpers ---

    def _justify_source(
        self, source_id: str, hint: str
    ) -> tuple[list[str], list[dict[str, Any]], int | None]:
        if self._recommendation is None:
            return [], [], None
        payload = self._recommendation.recommend_by_source(source_id, limit=1)
        items = payload.get("recommendations") or []
        if not items:
            payload = self._recommendation.recommend(hint, limit=5)
            items = [r for r in (payload.get("recommendations") or []) if r["source_id"] == source_id]
        if not items:
            return [], [], None
        top = items[0]
        return list(top.get("reason") or []), list(top.get("relations_used") or []), top.get("score")

    def _source_meta(self, source_id: str) -> dict[str, Any] | None:
        if self._discovery is None:
            return {"source_id": source_id, "source": source_id}
        return self._discovery.get_source(source_id)

    def _enrich_resources(
        self,
        source_id: str,
        resource_ids: list[str],
        concepts_hint: list[str] | None,
    ) -> list[dict[str, Any]]:
        """Lista de recursos con id + título legible cuando exista en Discovery."""
        out: list[dict[str, Any]] = []
        ids = list(resource_ids)

        discovered: list[dict[str, Any]] = []
        if self._discovery is not None:
            discovered = self._discovery.discover_resources(source_id) or []

        if not ids and discovered and concepts_hint:
            for res in discovered:
                rid = str(res.get("resource_id") or "")
                blob = normalize_token(
                    " ".join(
                        [
                            rid,
                            str(res.get("title") or ""),
                            " ".join(res.get("domains") or []),
                            " ".join(res.get("keywords") or []),
                        ]
                    )
                )
                if any(c in blob for c in concepts_hint):
                    ids.append(rid)
        if not ids and discovered:
            ids = [str(r.get("resource_id")) for r in discovered[:3] if r.get("resource_id")]

        title_by_id = {
            str(r.get("resource_id")): str(r.get("title") or r.get("name") or "")
            for r in discovered
            if r.get("resource_id")
        }

        for rid in ids:
            title = title_by_id.get(rid) or rid.split(":")[-1].replace("-", " ").replace("_", " ")
            if self._metadata is not None:
                try:
                    meta = self._metadata.get_resource(source_id, rid)
                    if meta and isinstance(meta, dict) and meta.get("status") != "not_found":
                        title = meta.get("title") or meta.get("name") or title
                except Exception:
                    pass
            item = {"resource_id": rid, "title": title}
            if item not in out:
                out.append(item)
        return out

    def _what_to_do(
        self,
        intent: str,
        source_id: str,
        category: str,
        resources: list[dict[str, Any]],
    ) -> str:
        cat_label = ACTION_CATEGORIES.get(category, category)
        res_hint = ""
        if resources:
            names = ", ".join(r.get("title") or r["resource_id"] for r in resources[:3])
            res_hint = f" Recursos sugeridos: {names}."
        intent_label = INTENT_LABELS.get(intent, intent)
        return (
            f"{intent_label}: {cat_label.lower()} mediante {source_id.upper()}.{res_hint}"
        ).strip()

    def _route_item(
        self,
        *,
        rank: int,
        title: str,
        category: str,
        what_to_do: str,
        where: list[str],
        source_id: str,
        source: str,
        institution: Any,
        resources: list[dict[str, Any]],
        why: list[str],
        score: int | None,
        relations_used: list[dict[str, Any]],
        intents: list[str],
    ) -> dict[str, Any]:
        inst = institution
        if isinstance(institution, dict):
            inst = institution.get("institution")
        return {
            "rank": rank,
            "title": title,
            "category": category,
            "category_label": ACTION_CATEGORIES.get(category, category),
            "what_to_do": what_to_do,
            "where": where,
            "source_id": source_id,
            "source": source,
            "institution": inst,
            "resources": resources,
            "why": why,
            "score": score,
            "relations_used": relations_used,
            "intents": list(intents),
        }

    def _empty(self, *, query: str) -> dict[str, Any]:
        return {
            "query": query,
            "need": None,
            "intents": [],
            "intent_labels": [],
            "concepts": [],
            "count": 0,
            "routes": [],
            "explainability": "required",
            "method": "decision_support_action_routes",
            "ai": False,
            "principle": "El sistema orienta; la curaduría humana decide.",
        }
