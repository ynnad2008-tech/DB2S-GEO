# backend/source_discovery

**Source Discovery Assistant — Fase 6 MVP**

Analiza URLs desconocidas y genera **propuestas** de incorporación.

## Principio

> El sistema propone. Los curadores deciden.

- NO crea conectores automáticamente
- NO modifica el catálogo oficial
- NO aprueba fuentes

## API

```http
POST /source-discovery/analyze
GET  /source-discovery/candidates
GET  /source-discovery/candidates/{id}
GET  /source-discovery/info
```

## Persistencia

`data/source_discovery/candidates.json`
