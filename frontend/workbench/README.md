# Curator Workbench — DB2S-GEO

Consola operativa ligera para curadores (Fase 7 + **7.1 UX simplification**).

## Principios

- HTML + CSS + JavaScript vanilla
- Sin React / Vue / Angular
- Consume la API existente (same-origin)
- No modifica el catálogo automáticamente
- Complejidad técnica oculta hasta Administración → Secciones avanzadas

## Arranque

```bash
pip install -r backend/requirements.txt
uvicorn backend.api.main:app --reload --app-dir .
```

Abrir: [http://127.0.0.1:8000/workbench/](http://127.0.0.1:8000/workbench/)

## Navegación (7.1)

| Sección | Propósito | API |
|---------|-----------|-----|
| **Inicio** | Propósito + métricas (Fuentes, Recursos, Dominios, Eventos, Candidatos) | `/sources`, `/graph/stats`, `/domains`, `/watcher/info`, `/source-discovery/info` |
| **Explorar** | Fuentes y dominios | `GET /sources`, `/domains` |
| **Recomendaciones** | Ranking justificable | `GET /recommend*` |
| **Monitoreo** | Eventos del Watcher (vista operativa) | `GET /watcher/events`, `POST /watcher/run` |
| **Observatorio** | Uso anónimo, nube, vacíos, emergentes | `GET /observatory/dashboard` |
| **Administración** | Candidatos + secciones avanzadas | `POST /source-discovery/analyze`, candidatos |

### Secciones avanzadas (dentro de Administración)

- Knowledge Graph (`/graph/*`)
- Watcher (detalle técnico)
- Candidate Sources (listado + análisis)

### Footer institucional

Texto aprobado en el Registro de Diseño + créditos Alpha:
`© DB2S-GEO · 2026` · autor · `v0.9 Alpha` · Acerca de / Cómo citar / Autoría.


## Estructura

```text
frontend/workbench/
├── index.html
├── README.md
└── static/
    ├── workbench.css
    └── workbench.js
```
