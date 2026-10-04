# DB2S-GEO

**Plataforma de conocimiento geoespacial**

**Estado:** v0.8.0 · **Autor:** Dany Arbey Benavides

> ✅ **Curaduría asistida por IA** — 116 fuentes verificadas por HTTP,
> recomendaciones explicables y crecimiento autogestionado con trazabilidad.
> La IA puede cometer errores: verifica las fuentes antes de usarlas.

Repositorio oficial: [github.com/ynnad2008-tech/DB2S-GEO](https://github.com/ynnad2008-tech/DB2S-GEO)
https://db2s-geo-546367148987.us-central1.run.app/workbench/

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
| Discovery Engine | Catálogo de 116 fuentes verificadas (Colombia, Centroamérica, Perú, México y globales) |
| Metadata Engine | Metadatos normalizados y evaluables |
| Knowledge Graph | Institution → Source → Resource → Domain → Keyword |
| Recommendation Engine | Score, razones y relaciones explicables (sin caja negra) |
| Decision Support Engine | Rutas de acción (qué / dónde / fuente / recursos / por qué) |
| Asistente conversacional | Chat de seguimiento con contexto del hilo (Gemini interpreta y narra; los motores deciden) |
| Filtro de cobertura | La geografía de la consulta ("en el Tolima") filtra fuentes pertinentes |
| Geoservicios | Acceso de usuario a endpoints ArcGIS REST / WMS verificados |
| Auto Curator | Crecimiento autogestionado: Gemini propone desde los vacíos de consulta; verificación HTTP obligatoria; trazabilidad completa |
| Watcher Engine | Monitoreo de cambios |
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
Cloud Run Private Preview: [deployment/cloudrun/README.md](deployment/cloudrun/README.md)  
Historial de versiones: [CHANGELOG.md](CHANGELOG.md)

---

## Autor

**Dany Arbey Benavides**  
Proyecto concebido y desarrollado por el autor.  
Herramientas de IA (Copilot, Cursor, DeepSeek) usadas como asistentes técnicos; las decisiones de diseño, arquitectura y curaduría corresponden al autor.

---

## Cómo citar esta plataforma

```text
Benavides, D. A. (2026). DB2S-GEO: Plataforma de conocimiento geoespacial (versión 0.8.0) [plataforma de software]. Consultado el [fecha].
```

También disponible en el Workbench: **Cómo citar esta plataforma**.

---

## Estado

La plataforma integra interpretación de lenguaje natural con **Gemini** (intérprete, narrador y curador automático) sobre motores deterministas y explicables: las recomendaciones siempre muestran sus razones y las fuentes solo se incorporan tras verificación HTTP.

**Pendientes operativos:** despliegue público en Cloud Run y validación con usuarios externos.  
**Fuera de alcance actual:** autenticación de usuarios y capas adicionales de IA generativa más allá del intérprete/narrador.

© DB2S-GEO · 2026 · Dany Arbey Benavides
