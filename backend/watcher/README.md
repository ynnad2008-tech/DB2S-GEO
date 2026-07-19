# backend/watcher

**Watcher Engine — Fase 5 MVP**

Observa fuentes MVP, compara snapshots y registra eventos.

## Principio

> El sistema se automonitorea. El sistema no se autogobierna.

- **NO** actualiza el catálogo automáticamente
- **NO** modifica conectores
- Solo observa, compara, detecta, registra y alerta

## Persistencia

JSON local en `data/watcher/`:
- `snapshots/<source_id>.json`
- `events.json`

## API

```http
GET  /watcher/info
GET  /watcher/events
GET  /watcher/events/{source_id}
GET  /watcher/events/type/{event_type}
POST /watcher/run
```

## Eventos

`NEW_RESOURCE` · `REMOVED_RESOURCE` · `RESOURCE_CHANGED` ·
`NEW_ACCESS_METHOD` · `ACCESS_METHOD_REMOVED` · `METADATA_CHANGED` ·
`SOURCE_UNAVAILABLE` · `BASELINE_CREATED`
