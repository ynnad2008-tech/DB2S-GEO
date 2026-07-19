# 11 — Watcher Engine

## Propósito

Definir el motor de monitoreo de novedades en el ecosistema de datos geoespaciales.

## Alcance

Responsabilidades y señales a observar. Sin scheduling ni alertas operativas.

## Objetivos

1. Detectar cambios relevantes en fuentes.
2. Alimentar Discovery y Knowledge Graph.
3. Soportar al agente DB2S-GEO Watcher.

## Monitorea (conceptual)

- Nuevos datasets
- Nuevas APIs
- Nuevos servicios
- Nuevas plataformas
- Nuevas versiones
- Nuevos catálogos STAC
- Nuevos ArcGIS Hub / geoportales

## Flujo conceptual

```text
Fuentes / Portales / Hubs
          │
          ▼
   Watcher Engine  ──►  Señales de cambio
          │
          ├──► Discovery Engine
          ├──► Knowledge Graph
          └──► Agente Watcher (notificación / propuesta)
```

## Ubicación en código (skeleton)

```text
backend/watcher/
agents/watcher/
```

## Secciones reservadas (futuro)

- [ ] Frecuencia y políticas de sondeo
- [ ] Deduplicación de señales
- [ ] Cola de revisión humana
- [ ] Integración con Connector Framework

---

*Sin implementación de monitoreo.*