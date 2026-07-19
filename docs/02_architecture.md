# 02 — Arquitectura

## Propósito

Definir la arquitectura conceptual de DB2S-GEO sin comprometer implementaciones.

## Alcance

Componentes, límites, flujos de alto nivel y tecnologías objetivo.

## Objetivos

1. Describir el mapa de componentes.
2. Separar núcleo de conectores y agentes.
3. Preparar despliegue futuro (Docker, FastAPI, PostGIS, etc.).

## Arquitectura conceptual

```text
                         ┌─────────────────────┐
                         │     API Gateway     │
                         │      (FastAPI)      │
                         └──────────┬──────────┘
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         │                          │                          │
         ▼                          ▼                          ▼
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│ Discovery Engine│      │Recommendation   │      │ Citation Engine │
└────────┬────────┘      │ Engine          │      └────────┬────────┘
         │               └────────┬────────┘               │
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  ▼
                    ┌─────────────────────────┐
                    │     Knowledge Graph     │
                    │   + Metadata Engine     │
                    └────────────┬────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│ Country Profiles│   │Connector        │   │ Watcher Engine  │
│                 │   │ Framework       │   │                 │
└─────────────────┘   └────────┬────────┘   └─────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Fuentes externas   │
                    │ (nacionales/global) │
                    └─────────────────────┘

                    ┌─────────────────────┐
                    │     AI Agents       │
                    │ Discover·Compare·   │
                    │ Cite·Code·Advisor·  │
                    │ Watcher             │
                    └─────────────────────┘
```

## Componentes

| Componente | Responsabilidad |
|------------|-----------------|
| Discovery Engine | Descubrir datasets, servicios, APIs, fuentes |
| Knowledge Graph | Relacionar entidades de conocimiento |
| Recommendation Engine | Ranking y recomendación contextual |
| Citation Engine | Referencias bibliográficas |
| Metadata Engine | Normalización y calidad de metadatos |
| Watcher Engine | Monitoreo de novedades |
| Country Profiles | Priorización por país |
| Connector Framework | Integración estandarizada de fuentes |
| AI Agents | Asistencia especializada |
| API Gateway | Exposición de capacidades |

## Tecnologías objetivo (sin implementar)

FastAPI · PostgreSQL · PostGIS · OpenSearch · Elasticsearch · Hugging Face · MCP · ArcGIS · QGIS · Earth Engine · Python · Docker

## Estructura de repositorio

```text
DB2S_GEO/
├── backend/
├── frontend/
├── datasets/
├── country_profiles/
├── connectors/
├── agents/
├── knowledge_graph/
├── docs/
├── tests/
├── deployment/
└── scripts/
```

## Secciones reservadas (futuro)

- [ ] Diagramas C4 (Context, Container, Component)
- [ ] Decisiones ADR
- [ ] Contratos OpenAPI versionados
- [ ] Topología de red y secretos

---

*No constituye diseño de implementación detallada.*