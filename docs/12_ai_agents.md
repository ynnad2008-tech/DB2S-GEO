# 12 — Agentes IA

## Propósito

Documentar responsabilidades de los agentes IA de DB2S-GEO.

## Alcance

Definición de roles. Sin prompts, modelos ni orquestación ejecutables.

## Objetivos

1. Delimitar el perímetro de cada agente.
2. Evitar solapamientos de responsabilidad.
3. Preparar integración futura con MCP / Hugging Face.

## Agentes

| Agente | Responsabilidad |
|--------|-----------------|
| **DB2S-GEO Discover** | Descubrir fuentes, datasets, servicios y APIs |
| **DB2S-GEO Compare** | Comparar datasets / fuentes según criterios |
| **DB2S-GEO Cite** | Generar referencias bibliográficas |
| **DB2S-GEO Code** | Generar código reproducible (Python, ArcPy, PyQGIS, GeoPandas, PostGIS, Earth Engine) |
| **DB2S-GEO Advisor** | Recomendar datasets según el problema territorial |
| **DB2S-GEO Watcher** | Detectar nuevas fuentes y cambios |

## Mapa de colaboración

```text
Usuario / Sistema
       │
       ▼
  Orquestación (futuro · MCP)
       │
       ├── Discover ──► Discovery Engine
       ├── Compare  ──► Knowledge Graph + Metadata
       ├── Cite     ──► Citation Engine
       ├── Code     ──► Conectores + plantillas de acceso
       ├── Advisor  ──► Recommendation Engine
       └── Watcher  ──► Watcher Engine
```

## Estructura en repositorio

```text
agents/
├── README.md
├── discover/
├── compare/
├── cite/
├── code/
├── advisor/
└── watcher/
```

## Tecnologías objetivo (futuro)

Hugging Face · MCP · FastAPI (como gateway)

## Secciones reservadas (futuro)

- [ ] Contratos de entrada/salida por agente
- [ ] Políticas de seguridad y grounding
- [ ] Evaluación de calidad de respuestas
- [ ] Memoria / contexto compartido

---

*Solo documentación de responsabilidades.*