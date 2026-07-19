# 14 — Modelo de Base de Datos (conceptual)

## Propósito

Bosquejar el modelo de datos persistente previsto para DB2S-GEO.

## Alcance

Entidades lógicas y tecnologías objetivo. Sin migraciones ni DDL operativo.

## Objetivos

1. Alinear persistencia con Knowledge Graph y catálogo.
2. Preparar PostgreSQL + PostGIS.
3. Reservar índices de búsqueda (OpenSearch / Elasticsearch).

## Tecnologías objetivo

| Uso | Tecnología |
|-----|------------|
| Relacional / espacial | PostgreSQL + PostGIS |
| Búsqueda / facetas | OpenSearch / Elasticsearch |
| Grafo (opción futura) | Por decidir (ver docs/03) |

## Entidades lógicas previstas

```text
Institution
Source
Dataset
Variable
Service
API
Reference
UseCase
Country
Theme / Domain
ConnectorRegistry
ScoreSnapshot          # futuro
WatcherSignal          # futuro
CitationRecord         # futuro
```

## Relaciones (alto nivel)

```text
Country 1──* Institution
Institution 1──* Source
Source 1──* Dataset
Dataset *──* Variable
Dataset *──* Theme
Source 1──* Service
Service 1──* API
Dataset *──* Reference
UseCase *──* Dataset
```

## Consideraciones espaciales

- Extensiones / footprints vía PostGIS (futuro)
- CRS y resolución como metadatos, no como geometría obligatoria

## Secciones reservadas (futuro)

- [ ] Diagrama ER detallado
- [ ] Migraciones
- [ ] Índices espaciales y de texto
- [ ] Estrategia de sincronización KG ↔ DB
- [ ] Retención y auditoría

---

*Modelo conceptual. Sin implementación.*