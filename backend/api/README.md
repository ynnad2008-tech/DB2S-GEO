# backend/api

**API Gateway — Fase 8 Decision Support + Workbench**

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/sources` | Listar / buscar fuentes MVP |
| GET | `/sources/{source_id}` | Detalle + recursos descubiertos |
| GET | `/sources/{source_id}/citation` | Citación / atribución |
| GET | `/sources/{source_id}/access` | Información de acceso |
| GET | `/sources/{source_id}/resources` | Recursos normalizados (Metadata) |
| GET | `/sources/{source_id}/resources/{resource_id}` | Metadatos de un recurso |
| GET | `/domains` | Dominios temáticos iniciales |
| GET | `/domains/{domain}` | Dominio + fuentes/recursos asociados |
| GET | `/graph/stats` | Estadísticas del grafo |
| GET | `/graph/nodes` | Nodos (filtro `?type=`) |
| GET | `/graph/relations` | Relaciones (filtro `?type=`) |
| GET | `/graph/domain/{domain_id}` | Recursos/fuentes por dominio |
| GET | `/graph/source/{source_id}` | Recursos/dominios por fuente |
| GET | `/graph/institution/{institution_id}` | Fuentes/dominios por institución |
| GET | `/recommend?q=` | Recomendación por texto |
| GET | `/recommend/domain/{domain_id}` | Por dominio |
| GET | `/recommend/source/{source_id}` | Fuentes relacionadas |
| GET | `/recommend/resource/{resource_id}` | Recursos relacionados |
| GET | `/watcher/info` | Estado del Watcher |
| GET | `/watcher/events` | Eventos recientes |
| GET | `/watcher/events/{source_id}` | Eventos por fuente |
| GET | `/watcher/events/type/{event_type}` | Eventos por tipo |
| POST | `/watcher/run` | Ejecutar ciclo de observación |
| GET | `/source-discovery/info` | Estado del asistente |
| POST | `/source-discovery/analyze` | Analizar URL desconocida |
| GET | `/source-discovery/candidates` | Listar candidatos |
| GET | `/source-discovery/candidates/{id}` | Detalle de candidato |
| GET | `/decision-support/info` | Estado del Decision Support |
| GET | `/decision-support?q=` | Rutas de acción (qué / dónde / fuente / recursos / por qué) |
| GET | `/observatory/dashboard` | Panel agregado (nube, rankings, timeline) |
| GET | `/observatory/notice` | Aviso de transparencia |
| GET | `/observatory/top-queries` | Consultas frecuentes |
| GET | `/observatory/empty-queries` | Consultas sin resultado |
| GET | `/observatory/domains` | Dominios más usados |
| GET | `/observatory/emerging` | Términos emergentes |
| GET | `/observatory/timeline` | Frecuencia temporal |
| GET | `/observatory/wordcloud` | Nube de palabras |
| GET | `/workbench/` | Curator Workbench (UI) |

## Arranque

```bash
pip install -r backend/requirements.txt
uvicorn backend.api.main:app --reload --app-dir .
```
