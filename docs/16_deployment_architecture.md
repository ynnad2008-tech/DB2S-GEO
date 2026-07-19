# 16 — Arquitectura de Despliegue

## Propósito

Preparar la visión de despliegue contenerizado de DB2S-GEO.

## Alcance

Topología conceptual Docker. Sin orquestación productiva.

## Objetivos

1. Anticipar servicios y dependencias.
2. Organizar `deployment/`.
3. Facilitar entornos locales futuros.

## Topología conceptual

```text
┌──────────────────────────────────────────────┐
│                   Docker Host                │
│                                              │
│  ┌────────────┐   ┌────────────────────┐     │
│  │  Frontend  │   │  API Gateway       │     │
│  │  (futuro)  │──►│  FastAPI (futuro)  │     │
│  └────────────┘   └─────────┬──────────┘     │
│                             │                │
│         ┌───────────────────┼────────────┐   │
│         ▼                   ▼            ▼   │
│  ┌────────────┐   ┌──────────────┐ ┌───────┐ │
│  │ PostgreSQL │   │ OpenSearch / │ │Workers│ │
│  │ + PostGIS  │   │ Elastic      │ │futuro │ │
│  └────────────┘   └──────────────┘ └───────┘ │
└──────────────────────────────────────────────┘
```

## Estructura

```text
deployment/
├── README.md
├── docker/          # Dockerfiles (placeholders)
├── compose/         # compose files (placeholders)
└── env/             # ejemplos de variables (sin secretos)
```

## Secciones reservadas (futuro)

- [ ] Dockerfiles reales
- [ ] Compose multi-servicio
- [ ] CI/CD
- [ ] Observabilidad (logs / métricas / trazas)
- [ ] Escalado horizontal

---

*Solo placeholders de despliegue.*