"""
API Gateway — DB2S-GEO (Discovery → … → Decision Support + Workbench).

Endpoints: Discovery · Metadata · KG · Recommend · Watcher ·
Source Discovery · Decision Support · Workbench.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from backend.citation.engine import CitationEngine
from backend.decision_support.engine import DecisionSupportEngine
from backend.discovery.engine import DiscoveryEngine
from backend.knowledge_graph.engine import KnowledgeGraphEngine
from backend.metadata.engine import MetadataEngine
from backend.observatory.engine import ObservatoryEngine
from backend.recommendation.engine import RecommendationEngine
from backend.source_discovery.engine import SourceDiscoveryAssistant
from backend.telemetry import get_telemetry_store
from backend.watcher.engine import WatcherEngine

APP_NAME = "DB2S-GEO"
APP_PHASE = "preview"
APP_VERSION = "0.2.0-preview"
APP_RELEASE_LABEL = "DB2S-GEO v0.2.0 Preview"
APP_AUTHOR = "Dany Arbey Benavides"

ROOT_DIR = Path(__file__).resolve().parents[2]
WORKBENCH_DIR = ROOT_DIR / "frontend" / "workbench"


class AnalyzeRequest(BaseModel):
    url: str = Field(..., description="URL de la fuente desconocida")
    persist: bool = Field(default=True, description="Guardar como candidato")


class TelemetryClickRequest(BaseModel):
    resource_id: str = Field(..., min_length=1, max_length=200)
    source_id: str | None = Field(default=None, max_length=120)


def create_engines() -> tuple[
    DiscoveryEngine,
    CitationEngine,
    MetadataEngine,
    KnowledgeGraphEngine,
    RecommendationEngine,
    WatcherEngine,
    SourceDiscoveryAssistant,
    DecisionSupportEngine,
    ObservatoryEngine,
]:
    discovery = DiscoveryEngine()
    citation = CitationEngine(discovery)
    metadata = MetadataEngine(discovery)
    knowledge_graph = KnowledgeGraphEngine(discovery, metadata)
    recommendation = RecommendationEngine(knowledge_graph, discovery, metadata)
    watcher = WatcherEngine(discovery, metadata)
    source_discovery = SourceDiscoveryAssistant(
        discovery, metadata, knowledge_graph, recommendation
    )
    decision_support = DecisionSupportEngine(
        recommendation, discovery, metadata, knowledge_graph
    )
    observatory = ObservatoryEngine(metadata=metadata)
    return (
        discovery,
        citation,
        metadata,
        knowledge_graph,
        recommendation,
        watcher,
        source_discovery,
        decision_support,
        observatory,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not getattr(app.state, "discovery", None):
        engines = create_engines()
        (
            app.state.discovery,
            app.state.citation,
            app.state.metadata,
            app.state.knowledge_graph,
            app.state.recommendation,
            app.state.watcher,
            app.state.source_discovery,
            app.state.decision_support,
            app.state.observatory,
        ) = engines
    yield


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=(
        "DB2S-GEO — Discovery, Metadata, KG, Recommend, Watcher, "
        "Source Discovery, Decision Support, Observatory y Workbench."
    ),
    lifespan=lifespan,
)

# Consola de curaduría (HTML/CSS/JS vanilla)
if (WORKBENCH_DIR / "static").is_dir():
    app.mount(
        "/workbench/static",
        StaticFiles(directory=str(WORKBENCH_DIR / "static")),
        name="workbench_static",
    )

(
    _default_discovery,
    _default_citation,
    _default_metadata,
    _default_kg,
    _default_rec,
    _default_watcher,
    _default_source_discovery,
    _default_decision_support,
    _default_observatory,
) = create_engines()
app.state.discovery = _default_discovery
app.state.citation = _default_citation
app.state.metadata = _default_metadata
app.state.knowledge_graph = _default_kg
app.state.recommendation = _default_rec
app.state.watcher = _default_watcher
app.state.source_discovery = _default_source_discovery
app.state.decision_support = _default_decision_support
app.state.observatory = _default_observatory


def _ensure_engines(request: Request) -> None:
    if getattr(request.app.state, "discovery", None) is None:
        engines = create_engines()
        (
            request.app.state.discovery,
            request.app.state.citation,
            request.app.state.metadata,
            request.app.state.knowledge_graph,
            request.app.state.recommendation,
            request.app.state.watcher,
            request.app.state.source_discovery,
            request.app.state.decision_support,
            request.app.state.observatory,
        ) = engines
    else:
        if getattr(request.app.state, "decision_support", None) is None:
            request.app.state.decision_support = DecisionSupportEngine(
                request.app.state.recommendation,
                request.app.state.discovery,
                request.app.state.metadata,
                request.app.state.knowledge_graph,
            )
        if getattr(request.app.state, "observatory", None) is None:
            request.app.state.observatory = ObservatoryEngine(
                metadata=request.app.state.metadata
            )


def _discovery(request: Request) -> DiscoveryEngine:
    _ensure_engines(request)
    return request.app.state.discovery


def _citation(request: Request) -> CitationEngine:
    _ensure_engines(request)
    return request.app.state.citation


def _metadata(request: Request) -> MetadataEngine:
    _ensure_engines(request)
    return request.app.state.metadata


def _kg(request: Request) -> KnowledgeGraphEngine:
    _ensure_engines(request)
    return request.app.state.knowledge_graph


def _recommend(request: Request) -> RecommendationEngine:
    _ensure_engines(request)
    return request.app.state.recommendation


def _watcher(request: Request) -> WatcherEngine:
    _ensure_engines(request)
    return request.app.state.watcher


def _source_discovery(request: Request) -> SourceDiscoveryAssistant:
    _ensure_engines(request)
    return request.app.state.source_discovery


def _decision_support(request: Request) -> DecisionSupportEngine:
    _ensure_engines(request)
    return request.app.state.decision_support


def _observatory(request: Request) -> ObservatoryEngine:
    _ensure_engines(request)
    return request.app.state.observatory


@app.get("/")
def root() -> dict[str, Any]:
    return get_app_info()


@app.get("/version")
def version() -> dict[str, str]:
    """Endpoint liviano de versión (sondas / Cloud Run)."""
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "phase": APP_PHASE,
        "release": APP_RELEASE_LABEL,
    }


@app.get("/healthz")
def healthz() -> dict[str, str]:
    """Health check liviano para Cloud Run / load balancers."""
    return {"status": "ok"}


@app.get("/workbench")
@app.get("/workbench/")
def workbench_home() -> FileResponse:
    """Curator Workbench — interfaz operativa ligera."""
    index = WORKBENCH_DIR / "index.html"
    if not index.is_file():
        raise HTTPException(status_code=404, detail="Workbench no encontrado")
    return FileResponse(index)


@app.get("/health")
def health(request: Request) -> dict[str, Any]:
    return {
        "status": "ok",
        "phase": APP_PHASE,
        "version": APP_VERSION,
        "discovery": _discovery(request).info(),
        "metadata": _metadata(request).info(),
        "citation": _citation(request).info(),
        "knowledge_graph": _kg(request).info(),
        "recommendation": _recommend(request).info(),
        "watcher": _watcher(request).info(),
        "source_discovery": _source_discovery(request).info(),
        "decision_support": _decision_support(request).info(),
        "observatory": _observatory(request).info(),
        "telemetry": get_telemetry_store().info(),
    }


@app.get("/sources")
def list_sources(
    request: Request,
    q: str | None = Query(default=None, description="Búsqueda por texto"),
    domain: str | None = Query(default=None, description="Filtro por dominio"),
) -> dict[str, Any]:
    discovery = _discovery(request)
    if q or domain:
        items = discovery.search(query=q, domain=domain)
    else:
        items = discovery.list_sources()
    payload = {
        "count": len(items),
        "sources": items,
        "curation": "human",
        "security": "read_only",
    }
    if q:
        try:
            _observatory(request).log_from_search(q, payload)
        except Exception:
            pass
    return payload


@app.get("/sources/{source_id}")
def get_source(source_id: str, request: Request) -> dict[str, Any]:
    payload = _discovery(request).get_source(source_id)
    if payload is None:
        raise HTTPException(status_code=404, detail=f"Fuente no encontrada: {source_id}")
    return payload


@app.get("/sources/{source_id}/citation")
def get_citation(
    source_id: str,
    request: Request,
    resource_id: str | None = Query(default=None),
) -> dict[str, Any]:
    payload = _citation(request).cite_source(source_id, resource_id=resource_id)
    if payload is None:
        raise HTTPException(status_code=404, detail=f"Fuente no encontrada: {source_id}")
    if payload.get("status") == "not_found":
        raise HTTPException(status_code=404, detail=payload.get("error", "Recurso no encontrado"))
    return payload


@app.get("/sources/{source_id}/access")
def get_access(
    source_id: str,
    request: Request,
    resource_id: str | None = Query(default=None),
) -> dict[str, Any]:
    payload = _discovery(request).access_info(source_id, resource_id=resource_id)
    if payload is None:
        raise HTTPException(status_code=404, detail=f"Fuente no encontrada: {source_id}")
    if payload.get("status") == "not_found":
        raise HTTPException(status_code=404, detail=payload.get("error", "Recurso no encontrado"))
    return payload


@app.get("/sources/{source_id}/resources")
def list_source_resources(
    source_id: str,
    request: Request,
    domain: str | None = Query(default=None, description="Filtro por dominio"),
    full: bool = Query(default=False, description="Si true, metadatos normalizados completos"),
) -> dict[str, Any]:
    metadata = _metadata(request)
    items = metadata.list_resources(source_id, domain=domain, summary=not full)
    if items is None:
        raise HTTPException(status_code=404, detail=f"Fuente no encontrada: {source_id}")
    return {
        "source_id": source_id.lower(),
        "count": len(items),
        "resources": items,
        "curation": "human",
        "normalization": "metadata_engine_v1",
    }


@app.get("/sources/{source_id}/resources/{resource_id:path}")
def get_source_resource(
    source_id: str,
    resource_id: str,
    request: Request,
) -> dict[str, Any]:
    metadata = _metadata(request)
    payload = metadata.get_resource(source_id, resource_id)
    if payload is None:
        raise HTTPException(status_code=404, detail=f"Fuente no encontrada: {source_id}")
    if payload.get("status") == "not_found":
        raise HTTPException(
            status_code=404,
            detail=payload.get("error", f"Recurso no encontrado: {resource_id}"),
        )
    return payload


@app.get("/domains")
def list_domains_endpoint(request: Request) -> dict[str, Any]:
    items = _metadata(request).list_domains()
    return {
        "count": len(items),
        "domains": items,
        "curation": "human",
        "extensible": True,
    }


@app.get("/domains/{domain}")
def get_domain_endpoint(domain: str, request: Request) -> dict[str, Any]:
    payload = _metadata(request).get_domain(domain)
    if payload is None:
        raise HTTPException(status_code=404, detail=f"Dominio no encontrado: {domain}")
    return payload


# --- Fase 3: Knowledge Graph ---


@app.get("/graph/stats")
def graph_stats(request: Request) -> dict[str, Any]:
    return _kg(request).stats()


@app.get("/graph/nodes")
def graph_nodes(
    request: Request,
    type: str | None = Query(
        default=None,
        description="Institution | Source | Resource | Domain | Keyword",
    ),
) -> dict[str, Any]:
    items = _kg(request).list_nodes(node_type=type)
    return {"count": len(items), "nodes": items}


@app.get("/graph/relations")
def graph_relations(
    request: Request,
    type: str | None = Query(
        default=None,
        description="publishes | contains | belongs_to | associated_with",
    ),
) -> dict[str, Any]:
    items = _kg(request).list_relations(rel_type=type)
    return {"count": len(items), "relations": items}


@app.get("/graph/domain/{domain_id}")
def graph_domain(domain_id: str, request: Request) -> dict[str, Any]:
    payload = _kg(request).resources_by_domain(domain_id)
    if payload is None:
        raise HTTPException(status_code=404, detail=f"Dominio no encontrado en el grafo: {domain_id}")
    return payload


@app.get("/graph/source/{source_id}")
def graph_source(source_id: str, request: Request) -> dict[str, Any]:
    payload = _kg(request).resources_by_source(source_id)
    if payload is None:
        raise HTTPException(status_code=404, detail=f"Fuente no encontrada en el grafo: {source_id}")
    return payload


@app.get("/graph/institution/{institution_id}")
def graph_institution(institution_id: str, request: Request) -> dict[str, Any]:
    payload = _kg(request).get_institution(institution_id)
    if payload is None:
        raise HTTPException(
            status_code=404,
            detail=f"Institución no encontrada en el grafo: {institution_id}",
        )
    return payload


# --- Fase 4: Recommendation ---


@app.get("/recommend/info")
def recommend_info(request: Request) -> dict[str, Any]:
    """Metadatos del Recommendation Engine (sin ejecutar ranking)."""
    return _recommend(request).info()


@app.get("/recommend")
def recommend_query(
    request: Request,
    q: str = Query(..., description="Keyword, dominio, fuente o recurso"),
    limit: int = Query(default=10, ge=1, le=50),
) -> dict[str, Any]:
    payload = _recommend(request).recommend(q, limit=limit)
    try:
        _observatory(request).log_from_recommend(q, payload)
    except Exception:
        pass
    try:
        get_telemetry_store().log(q, int(payload.get("count") or 0))
    except Exception:
        pass
    return payload


@app.get("/recommend/domain/{domain_id}")
def recommend_domain(
    domain_id: str,
    request: Request,
    limit: int = Query(default=10, ge=1, le=50),
) -> dict[str, Any]:
    payload = _recommend(request).recommend_by_domain(domain_id, limit=limit)
    if payload.get("error"):
        raise HTTPException(status_code=404, detail=payload["error"])
    return payload


@app.get("/recommend/source/{source_id}")
def recommend_source(
    source_id: str,
    request: Request,
    limit: int = Query(default=10, ge=1, le=50),
) -> dict[str, Any]:
    payload = _recommend(request).recommend_by_source(source_id, limit=limit)
    if payload.get("error"):
        raise HTTPException(status_code=404, detail=payload["error"])
    return payload


@app.get("/recommend/resource/{resource_id:path}")
def recommend_resource(
    resource_id: str,
    request: Request,
    limit: int = Query(default=10, ge=1, le=50),
) -> dict[str, Any]:
    payload = _recommend(request).recommend_by_resource(resource_id, limit=limit)
    if payload.get("error"):
        raise HTTPException(status_code=404, detail=payload["error"])
    return payload


# --- Fase 5: Watcher ---


@app.get("/watcher/info")
def watcher_info(request: Request) -> dict[str, Any]:
    return _watcher(request).info()


@app.get("/watcher/events")
def watcher_events(
    request: Request,
    limit: int | None = Query(default=50, ge=1, le=500),
) -> dict[str, Any]:
    events = _watcher(request).list_events(limit=limit)
    return {
        "count": len(events),
        "events": events,
        "auto_applied": False,
        "curation": "human_required",
    }


@app.get("/watcher/events/type/{event_type}")
def watcher_events_by_type(
    event_type: str,
    request: Request,
    limit: int | None = Query(default=50, ge=1, le=500),
) -> dict[str, Any]:
    events = _watcher(request).list_events(event_type=event_type, limit=limit)
    return {
        "event_type": event_type.upper(),
        "count": len(events),
        "events": events,
        "auto_applied": False,
        "curation": "human_required",
    }


@app.get("/watcher/events/{source_id}")
def watcher_events_by_source(
    source_id: str,
    request: Request,
    limit: int | None = Query(default=50, ge=1, le=500),
) -> dict[str, Any]:
    events = _watcher(request).list_events(source_id=source_id, limit=limit)
    return {
        "source": source_id.lower(),
        "count": len(events),
        "events": events,
        "auto_applied": False,
        "curation": "human_required",
    }


@app.post("/watcher/run")
def watcher_run(
    request: Request,
    source_id: str | None = Query(
        default=None,
        description="Opcional: ejecutar solo sobre una fuente MVP",
    ),
) -> dict[str, Any]:
    """
    Ejecuta un ciclo de observación.
    Detecta y registra eventos. NO modifica el catálogo.
    """
    watcher = _watcher(request)
    targets = [source_id] if source_id else None
    return watcher.run(source_ids=targets)


# --- Fase 6: Source Discovery Assistant ---


@app.get("/source-discovery/info")
def source_discovery_info(request: Request) -> dict[str, Any]:
    return _source_discovery(request).info()


@app.post("/source-discovery/analyze")
def source_discovery_analyze(
    body: AnalyzeRequest,
    request: Request,
) -> dict[str, Any]:
    """
    Analiza una URL desconocida y genera una propuesta candidata.
    NO incorpora al catálogo ni crea conectores.
    """
    result = _source_discovery(request).analyze(body.url, persist=body.persist)
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("error", "Análisis fallido"))
    return result


@app.get("/source-discovery/candidates")
def source_discovery_candidates(
    request: Request,
    limit: int = Query(default=50, ge=1, le=200),
) -> dict[str, Any]:
    items = _source_discovery(request).list_candidates(limit=limit)
    return {
        "count": len(items),
        "candidates": items,
        "curation": "human_required",
        "catalog_modified": False,
    }


@app.get("/source-discovery/candidates/{candidate_id}")
def source_discovery_candidate(
    candidate_id: str,
    request: Request,
) -> dict[str, Any]:
    item = _source_discovery(request).get_candidate(candidate_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Candidato no encontrado: {candidate_id}")
    return item


# --- Fase 8: Decision Support ---


@app.get("/decision-support/info")
def decision_support_info(request: Request) -> dict[str, Any]:
    """Metadatos del Decision Support Engine."""
    return _decision_support(request).info()


@app.get("/decision-support")
def decision_support_advise(
    request: Request,
    q: str = Query(..., description="Consulta orientada a un problema o necesidad"),
    limit: int = Query(default=6, ge=1, le=20),
) -> dict[str, Any]:
    """
    Devuelve rutas de acción: qué hacer, dónde, fuente, recursos y por qué.
    No modifica el catálogo.
    """
    payload = _decision_support(request).advise(q, limit=limit)
    try:
        _observatory(request).log_from_decision_support(q, payload)
    except Exception:
        pass
    try:
        get_telemetry_store().log(q, int(payload.get("count") or 0))
    except Exception:
        pass
    return payload


# --- Fase 8.1: Knowledge Usage Observatory ---


@app.get("/observatory/info")
def observatory_info(request: Request) -> dict[str, Any]:
    return _observatory(request).info()


@app.get("/observatory/notice")
def observatory_notice(request: Request) -> dict[str, Any]:
    return _observatory(request).notice()


@app.get("/observatory/dashboard")
def observatory_dashboard(request: Request) -> dict[str, Any]:
    """Payload agregado para el Workbench (nube, rankings, timeline)."""
    return _observatory(request).dashboard()


@app.get("/observatory/top-queries")
def observatory_top_queries(
    request: Request,
    limit: int = Query(default=20, ge=1, le=100),
) -> dict[str, Any]:
    return _observatory(request).top_queries(limit=limit)


@app.get("/observatory/empty-queries")
def observatory_empty_queries(
    request: Request,
    limit: int = Query(default=20, ge=1, le=100),
) -> dict[str, Any]:
    return _observatory(request).empty_queries(limit=limit)


@app.get("/observatory/domains")
def observatory_domains(
    request: Request,
    limit: int = Query(default=20, ge=1, le=100),
) -> dict[str, Any]:
    return _observatory(request).domains(limit=limit)


@app.get("/observatory/emerging")
def observatory_emerging(
    request: Request,
    limit: int = Query(default=20, ge=1, le=100),
) -> dict[str, Any]:
    return _observatory(request).emerging(limit=limit)


@app.get("/observatory/timeline")
def observatory_timeline(
    request: Request,
    days: int = Query(default=30, ge=1, le=90),
) -> dict[str, Any]:
    return _observatory(request).timeline(days=days)


@app.get("/observatory/wordcloud")
def observatory_wordcloud(
    request: Request,
    limit: int = Query(default=40, ge=1, le=100),
) -> dict[str, Any]:
    return _observatory(request).wordcloud(limit=limit)


# --- Telemetría mínima (preview) ---


@app.get("/telemetry/info")
def telemetry_info() -> dict[str, Any]:
    return get_telemetry_store().info()


@app.get("/telemetry/recent")
def telemetry_recent(
    limit: int = Query(default=50, ge=1, le=200),
) -> dict[str, Any]:
    """Últimos eventos: query · timestamp · result_count."""
    items = get_telemetry_store().recent(limit=limit)
    return {"count": len(items), "items": items}


@app.get("/telemetry/clicks")
def telemetry_clicks(
    limit: int = Query(default=50, ge=1, le=200),
) -> dict[str, Any]:
    """Últimos clics de recurso."""
    items = get_telemetry_store().recent_clicks(limit=limit)
    return {"count": len(items), "items": items}


@app.post("/telemetry/click")
def telemetry_click(body: TelemetryClickRequest) -> dict[str, Any]:
    """Registra clic anónimo sobre un resource_id."""
    event = get_telemetry_store().log_click(body.resource_id, body.source_id)
    if event is None:
        raise HTTPException(status_code=400, detail="resource_id inválido")
    return {"ok": True, "event": event}


def get_app_info() -> dict[str, Any]:
    return {
        "name": APP_NAME,
        "phase": APP_PHASE,
        "version": APP_VERSION,
        "release": APP_RELEASE_LABEL,
        "author": APP_AUTHOR,
        "status": "preview",
        "endpoints": [
            "GET /version",
            "GET /healthz",
            "GET /health",
            "GET /sources",
            "GET /sources/{source_id}",
            "GET /sources/{source_id}/citation",
            "GET /sources/{source_id}/access",
            "GET /sources/{source_id}/resources",
            "GET /sources/{source_id}/resources/{resource_id}",
            "GET /domains",
            "GET /domains/{domain}",
            "GET /graph/stats",
            "GET /graph/nodes",
            "GET /graph/relations",
            "GET /graph/domain/{domain_id}",
            "GET /graph/source/{source_id}",
            "GET /graph/institution/{institution_id}",
            "GET /recommend/info",
            "GET /recommend?q=",
            "GET /recommend/domain/{domain_id}",
            "GET /recommend/source/{source_id}",
            "GET /recommend/resource/{resource_id}",
            "GET /watcher/info",
            "GET /watcher/events",
            "GET /watcher/events/{source_id}",
            "GET /watcher/events/type/{event_type}",
            "POST /watcher/run",
            "GET /source-discovery/info",
            "POST /source-discovery/analyze",
            "GET /source-discovery/candidates",
            "GET /source-discovery/candidates/{id}",
            "GET /decision-support/info",
            "GET /decision-support?q=",
            "GET /observatory/info",
            "GET /observatory/notice",
            "GET /observatory/dashboard",
            "GET /observatory/top-queries",
            "GET /observatory/empty-queries",
            "GET /observatory/domains",
            "GET /observatory/emerging",
            "GET /observatory/timeline",
            "GET /observatory/wordcloud",
            "GET /telemetry/info",
            "GET /telemetry/recent",
            "GET /telemetry/clicks",
            "POST /telemetry/click",
            "GET /workbench/",
        ],
        "workbench": "/workbench/",
    }
