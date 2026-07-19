# Backend — DB2S-GEO

Backend modular (FastAPI) — **Fase 1: Discovery Engine MVP**.

## Módulos activos (MVP)

| Módulo | Estado | Rol |
|--------|--------|-----|
| discovery | MVP | Registro, listado, búsqueda y metadatos de fuentes |
| metadata | MVP | Normalización de recursos y dominios |
| knowledge_graph | MVP | Relaciones Institution/Source/Resource/Domain/Keyword |
| recommendation | MVP | Ranking explicable sobre el Knowledge Graph |
| watcher | MVP | Snapshots, comparación y eventos (sin auto-update) |
| source_discovery | MVP | Análisis de URLs y candidatos (curaduría humana) |
| decision_support | MVP | Rutas de acción (qué / dónde / fuente / recursos / por qué) |
| observatory | MVP | Uso anónimo, vacíos y tendencias de consultas |
| citation | MVP | Atribución y citas (APA / DOI cuando existan) |
| api | MVP | API + Curator Workbench en `/workbench/` |
| connectors | MVP (6) | IDEAM · INVEMAR · GBIF · FAOSTAT · WorldPop · GEE |

## Arranque

```bash
# desde la raíz del repo
pip install -r backend/requirements.txt
uvicorn backend.api.main:app --reload --app-dir .
```

- API docs: http://127.0.0.1:8000/docs
- Workbench: http://127.0.0.1:8000/workbench/
## Principios MVP

- Curaduría humana (solo conectores registrados explícitamente)
- Atribución y trazabilidad
- Seguridad read-only
- Sin descarga masiva ni ejecución de código externo
