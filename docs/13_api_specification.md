# 13 — Especificación de API (conceptual)

## Propósito

Reservar el espacio de especificación del API Gateway de DB2S-GEO.

## Alcance

Superficie conceptual de endpoints. Sin OpenAPI implementado ni handlers.

## Objetivos

1. Anticipar recursos principales.
2. Alinear frontend, agentes y clientes externos.
3. Preparar Fase 8 — API pública.

## Tecnología objetivo

FastAPI (sin implementar en Fase 0).

## Recursos conceptuales

```text
/api/v1/
├── discovery/          # búsqueda y descubrimiento
├── sources/            # fuentes registradas
├── datasets/           # datasets
├── recommendations/    # recomendaciones
├── citations/          # citas
├── countries/          # country profiles
├── domains/            # dominios temáticos
├── knowledge/          # consultas al grafo (futuro)
├── watchers/           # señales del watcher (futuro)
└── agents/             # invocación de agentes (futuro)
```

## Principios

- Versionado (`/v1`)
- Respuestas explicables (especialmente recommendations)
- Separación discovery vs. acceso a datos crudos
- Sin exponer secretos de conectores

## Ejemplo ilustrativo (no normativo)

```http
GET /api/v1/discovery?q=precipitacion&country=CO&domain=clima
```

*Contrato exacto: reservado.*

## Secciones reservadas (futuro)

- [ ] OpenAPI / JSON Schema
- [ ] Autenticación y autorización
- [ ] Rate limiting y cuotas
- [ ] Códigos de error estandarizados
- [ ] SDKs cliente

---

*Especificación conceptual. No implementada.*