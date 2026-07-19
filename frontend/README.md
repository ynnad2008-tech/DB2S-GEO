# Frontend — DB2S-GEO

## Curator Workbench (Fase 7 + 7.1 UX)

Consola operativa ligera para curadores:

```text
frontend/workbench/
├── index.html
├── README.md
└── static/
    ├── workbench.css
    └── workbench.js
```

Navegación: **Inicio · Explorar · Recomendaciones · Monitoreo · Observatorio · Administración**

Inicio incluye nube dinámica de conceptos (`GET /observatory/wordcloud`) debajo del buscador.
Administración muestra contador secundario: `Administración (N)`.

Inicio incluye nube dinámica de conceptos (`GET /observatory/wordcloud`) alrededor del buscador.

Abrir tras arrancar la API:

[http://127.0.0.1:8000/workbench/](http://127.0.0.1:8000/workbench/)

Stack: HTML · CSS · JavaScript vanilla (sin React/Vue/Angular).

Private Preview: el buscador de Inicio llama a `GET /decision-support` y muestra
rutas de orientación (qué hacer / fuente / por qué). No hay app React en este repo.

## Público / producto (futuro)

Reservado: interfaz pública de descubrimiento y recomendaciones.
