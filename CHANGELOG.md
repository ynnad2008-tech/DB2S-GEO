# Changelog

Todos los cambios relevantes de DB2S-GEO se documentan en este archivo.

El formato se inspira en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

---

## [v0.3.0] — 2026-07-27

Catálogo completo: 33 fuentes, 130 recursos, 15/15 dominios. Hardening de infraestructura.

### Añadido — Conectores (+10)

- **DIMAR** — cartografía náutica, batimetría, señalización marítima, IDE marítima (6 recursos)
- **CIOH** — oceanografía operacional, meteorología marina, mareas, avisos a navegantes (5 recursos)
- **Global Forest Watch** — cobertura forestal, alertas GLAD-S2, alertas RADD, carbono forestal (5 recursos)
- **SiB Colombia** — explorador de biodiversidad, catálogo, API REST, colecciones biológicas (4 recursos)
- **eBird** — registros de aves, hotspots, Status & Trends, Macaulay Library (4 recursos)
- **SoilGrids** — propiedades del suelo 250m, WCS, API REST, parámetros hidrológicos (5 recursos)
- **ASF** — Vertex SAR, HyP3 InSAR, OpenTopography DEM (3 recursos)
- **CATIE** — café, cacao, cuencas, cambio climático tropical (4 recursos)
- **Copernicus** — ERA5, CAMS calidad del aire, Sentinel-5P TROPOMI (3 recursos)
- **World Bank** — WDI, Climate Knowledge Portal, Gender Data (3 recursos)

### Añadido — Infraestructura

- `pyproject.toml` a raíz con `pip install -e .`
- Entorno virtual Python 3.12
- Health check real verificando estado de engines
- Middleware de errores global + logging estructurado
- `.env` para desarrollo local
- CORS middleware
- Favicon inline SVG en Workbench

### Corregido — Calidad del catálogo

- Auditoría integral de dominios: 15/15 con cobertura, 0 vacíos
- Corrección de keywords: filtro de términos genéricos (`GENERIC_KEYWORDS`) + sinónimos a nivel consulta (`CURATED_ALIASES`)
- Endpoints completos en los 130 recursos del catálogo
- Prefijos de recursos normalizados (`global-forest-watch:`, `sib_colombia:`)
- Validación: 33 activos, 0 inválidos, 0 incompletos, 0 duplicados

### Corregido — CI/CD

- Dockerfile migrado a `pyproject.toml` + `pip install -e .`
- GitHub Actions: `pip install -r backend/requirements.txt` → `pip install -e .`
- Smoke tests post-deploy: verifica conteo de fuentes, DIMAR, GFW, ASF, SoilGrids
- Script de deploy actualizado (`deploy_0_2_preview.sh`)

### Notas técnicas

- Catálogo: 33 fuentes JSON-first + 33 conectores Python fallback
- Tests: 104 unitarios pasando
- Dominios: agricultura, biodiversidad, cartografia_base, catastro, clima, economia, geologia, hidrologia, infraestructura, observacion_tierra, oceanos_costas, ordenamiento, poblacion, riesgo, suelos
- Stubs pendientes: 0 (todos los conectores implementados)

---

## [v0.2.0-preview] — 2026-07-19

JSON catalog, relevance filters, Workbench URL links.

## [v0.1.0-preview] — 2026-07-19

23 fuentes, 71 recursos, Cloud Run readiness.

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
