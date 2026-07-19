# DB2S-GEO

**Plataforma de conocimiento geoespacial**

**Estado:** v0.9 Alpha · **Autor:** Dany Arbey Benavides

> ✅ **¡Validada por humanos!** — Supervisado, recomendaciones explicables, sin auto-aplicación al catálogo.

Repositorio oficial: [github.com/ynnad2008-tech/DB2S-GEO](https://github.com/ynnad2008-tech/DB2S-GEO)

---

## ¿Qué es DB2S-GEO?

DB2S-GEO es una plataforma operativa que ayuda a descubrir, evaluar, recomendar y monitorear fuentes de datos geoespaciales, ambientales y científicas.

No es solo un catálogo: orienta hacia **acciones concretas** (qué hacer, dónde, con qué fuente y por qué), con trazabilidad y validación humana.

---

## ¿Qué problemas resuelve?

- Encontrar fuentes confiables para un problema territorial.
- Entender relaciones entre instituciones, recursos y dominios.
- Recibir recomendaciones **explicables** (no caja negra).
- Detectar cambios en fuentes sin alterar el catálogo automáticamente.
- Observar tendencias de uso de forma **anónima**.
- Preparar incorporación de nuevas fuentes con curaduría humana.

---

## Capacidades principales

| Capacidad | Descripción |
|-----------|-------------|
| Discovery Engine | Catálogo MVP curado (IDEAM, INVEMAR, GBIF, FAO, WorldPop, GEE) |
| Metadata Engine | Metadatos normalizados y evaluables |
| Knowledge Graph | Institution → Source → Resource → Domain → Keyword |
| Recommendation Engine | Score, razones y relaciones explicables |
| Decision Support Engine | Rutas de acción (qué / dónde / fuente / recursos / por qué) |
| Watcher Engine | Monitoreo de cambios sin auto-aplicación |
| Source Discovery Assistant | Candidatos para curaduría humana |
| Knowledge Usage Observatory | Consultas anónimas, tendencias y vacíos |
| Curator Workbench | Consola HTML/CSS/JS responsive (móvil incluido) |

---

## Inicio rápido

```bash
pip install -r backend/requirements.txt
uvicorn backend.api.main:app --host 127.0.0.1 --port 8000 --app-dir .
```

- Workbench: http://127.0.0.1:8000/workbench/
- API docs: http://127.0.0.1:8000/docs

Guía de despliegue Alpha: [ALPHA_DEPLOYMENT.md](ALPHA_DEPLOYMENT.md)  
Historial de versiones: [CHANGELOG.md](CHANGELOG.md)

---

## Autor

**Dany Arbey Benavides**  
Proyecto concebido y desarrollado por el autor.  
Herramientas de IA (Copilot, Cursor, DeepSeek) usadas como asistentes técnicos; las decisiones de diseño, arquitectura y curaduría corresponden al autor.

---

## Cómo citar esta plataforma

```text
Benavides, D. A. (2026). DB2S-GEO: Plataforma de conocimiento geoespacial (versión 0.9 Alpha) [plataforma de software]. Consultado el [fecha].
```

También disponible en el Workbench: **Cómo citar esta plataforma**.

---

## Estado Alpha

La arquitectura principal se considera **funcional** para demostraciones, pruebas en internet y validación móvil.

**Prioridad actual:** presentación, documentación, identidad, trazabilidad y despliegue.  
**Fuera de alcance Alpha:** nuevos motores, taxonomías ampliadas, autenticación de usuarios o capas de IA generativa.

© DB2S-GEO · 2026 · Dany Arbey Benavides
