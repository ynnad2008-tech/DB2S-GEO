# Changelog

Todos los cambios relevantes de DB2S-GEO se documentan en este archivo.

El formato se inspira en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

---

## [v0.9 Alpha] — 2026-07-19

Primera publicación pública Alpha.

### Añadido

- **Discovery Engine** — catálogo MVP de fuentes geoespaciales curadas
- **Metadata Engine** — metadatos normalizados y evaluables
- **Knowledge Graph** — relaciones Institution → Source → Resource → Domain → Keyword
- **Recommendation Engine** — recomendaciones explicables (score y razones)
- **Watcher Engine** — monitoreo de cambios sin auto-aplicación al catálogo
- **Source Discovery Assistant** — candidatos a revisión humana
- **Decision Support Engine** — rutas de acción (qué / dónde / fuente / recursos / por qué)
- **Knowledge Usage Observatory** — registro anónimo de uso, tendencias y vacíos
- **Curator Workbench** — interfaz HTML/CSS/JS (Inicio, Explorar, Recomendaciones, Monitoreo, Observatorio, Administración)
- **Responsive móvil** — menú hamburguesa y layout adaptado (320–768 px)
- **Footer institucional** — autoría, citación, sostenibilidad y enlace a la API
- **Observatorio y nube dinámica** — tendencias de la comunidad en Inicio y Observatorio
- Identidad Alpha: **¡Validada por humanos!**, páginas Acerca de / Cómo citar / Autoría / Apoya el desarrollo
- Despliegue: `Dockerfile`, `ALPHA_DEPLOYMENT.md` (local, Docker, Hugging Face Spaces)

### Notas

- Sin autenticación de usuarios en Alpha.
- El Observatorio no almacena IP ni PII.
- Artefactos locales (`data/`, `.env`, cachés) quedan fuera del repositorio vía `.gitignore`.

---

[v0.9 Alpha]: https://github.com/ynnad2008-tech/DB2S-GEO
