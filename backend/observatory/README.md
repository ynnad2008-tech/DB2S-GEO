# backend/observatory

**Knowledge Usage Observatory — Fase 8.1 MVP**

Registro **anónimo** de consultas para mejorar el catálogo y detectar vacíos.

## Principios

- Anonimización y minimización
- Sin nombres, correos, credenciales ni IP persistente
- Transparencia (aviso visible en Workbench)
- Uso técnico / científico

## Qué se registra

| Campo | Descripción |
|-------|-------------|
| consulta | Texto sanitizado |
| timestamp | Fecha/hora UTC |
| result_count / has_results | Resultados obtenidos |
| domains | Dominios activados |
| recommendations | `source_id` + score (mínimo) |

## API

```http
GET  /observatory/info
GET  /observatory/notice
GET  /observatory/dashboard
GET  /observatory/top-queries
GET  /observatory/empty-queries
GET  /observatory/domains
GET  /observatory/emerging
GET  /observatory/timeline
GET  /observatory/wordcloud
```

Las consultas a `/recommend` y `/decision-support` se registran automáticamente de forma anónima.
