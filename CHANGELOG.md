# Changelog

Todos los cambios relevantes de DB2S-GEO se documentan en este archivo.

El formato se inspira en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

---

## [v0.7.2] — 2026-10-03

Workbench simplificado (solo paneles funcionales) · narrador Gemini · uso del suelo en consultas agro.

### Cambiado — Frontend

- Fuera las secciones informativas (Acerca de, Cómo citar, Autoría, Apoyo)
  y las vistas técnicas avanzadas: solo los 6 paneles funcionales.
- El panel manual de candidatos fue reemplazado por el panel
  **Auto Curator** (ejecutar ciclo + log de trazabilidad).
- Textos de gobernanza actualizados: "Curaduría asistida por IA · fuentes
  verificadas automáticamente" y aviso "La IA puede cometer errores" en
  hero, administración, principios y footer.

### Añadido — Narrador Gemini (inmersivo)

- `llm_narrator.py`: resumen en lenguaje natural de cada orientación y
  preguntas de seguimiento, con fallback determinista garantizado
  (campo `narrative` en /decision-support).

### Añadido — Uso del suelo en consultas agro

- Aliases `ganaderia` y `zonificacion` → uso_suelo/coberturas/aptitud:
  consultas de ganadería ahora alcanzan MapBiomas, IGAC, UPRA y GEE.
- DynamicWorld enriquecido con keywords agro/uso del suelo (subió de
  "sin match" a top-13 con razones pertinentes).
- `GET /source-discovery/auto-curate/log` para el panel del workbench.
- Suite 144/144.

---

## [v0.7.1] — 2026-10-03

Crecimiento autogestionado del catálogo (Auto Curator) con prioridad de geoservicios.

### Añadido

- `backend/source_discovery/auto_curator.py`: ciclo automático — Gemini
  propone fuentes desde los vacíos del Observatorio; compuerta HTTP
  determinista obligatoria (portal y geoservicio con su protocolo);
  fichas nuevas activadas con `curation: llm-verified`.
- **Geoservicios primero (mandatorio)**: el prompt prioriza fuentes con
  ArcGIS REST/WMS/WFS; el geoservicio verificado es el recurso primario
  de la ficha; los portales solo rellenan si faltan para el tope.
- Enriquecimiento de fichas existentes: solo AGREGA keywords propuestas
  por Gemini desde las interacciones (nunca borra; tope 5/fuente).
- Log JSONL completo en `data/auto_curation/log.jsonl` (propuestas,
  rechazos, altas y errores).
- Endpoint `POST /source-discovery/auto-curate` con guarda
  `AUTO_CURATION=on` (403 si está apagada).
- Servicios ecosistémicos como alias (`provision`, `habitat`, …) y
  DynamicWorld vinculado a hábitat.
- Suite 141/141.

---

## [v0.7.0] — 2026-10-03

Expansión total: catálogo 116 fuentes · cobertura regional · perfiles refinados.

### Añadido — Fuentes verificadas (+35)

- **Costa Rica (5)**: CNE, IMN, MINAE, SINAC, SNIT.
- **Perú (8)**: IGN, MINAM, SENAMHI, SERFOR, SERNANP, MIDAGRI (antes
  MINAGRI), INDECI, UNMSM-IGGT.
- **México (2)**: CONAGUA, SIAP (vía gob.mx).
- **Honduras (1)**: CENAOS-COPECO.
- **Colombia (1)**: datos.gov.co (portal nacional de datos abiertos).
- **Globales (18)**: CHIRPS, GPM, Global Surface Water, Global Mangrove
  Watch, OpenLandMap, OBIS, NOAA, USGS Hazards, DesInventar, EM-DAT,
  INFORM, HDX, iNaturalist, BirdCast, Earth Search, Planetary Computer,
  OpenAlex, Semantic Scholar.
- 12 pendientes con evidencia: INEGI/CONABIO/INEC (TLS o timeout desde la
  red de curaduría), SINIT/CNA/ESNACIFOR/MiAmbiente/SET (Honduras, DNS),
  ARESEP/IGN-CR, ERA5 (CDS timeout) y gob-meta (sigue caído).

### Añadido — Cobertura regional

- `coverage.py` generalizado: honduras, costa_rica, mexico y peru con sus
  ciudades clave; el país cubre sus subnacionales; detección automática en
  consultas ("en Tegucigalpa" → tegucigalpa).

### Corregido

- Perfil de inundaciones sin "microcuenca" como disparador (mencionar una
  microcuenca no implica inundación).
- Perfiles con cobertura geográfica se completan con recomendaciones
  regionales cuando las plantillas quedan cortas (p. ej. precipitación
  fuera de Colombia → CHIRPS/GPM/WorldClim).
- Ciclo de imports en frío (discovery → coverage → scoring → recommendation)
  resuelto con import lazy de normalize_token en coverage.py.
- Categorías y "dónde" por defecto para fuentes sin entrada en SOURCE_WHERE.
- Suite 133/133.

---

## [v0.6.1] — 2026-10-03

Precisión semántica de consultas: fin del encadenamiento transitivo de aliases.

### Corregido

- `expand_query_tokens` / `expand_concepts`: expansión de aliases de **un
  solo salto** sobre los tokens del usuario (con formas singular/plural).
  Antes la cadena transitiva (ecosistemas → manglares → costas → bahía →
  caribe → morfometría) contaminaba consultas marinas con ASF/SGC/GFW.
- Aliases geográficos sin ciudades: la geografía se maneja con el filtro
  `coverage`, no con keywords ("cartagena"/"barranquilla" ya no aparecen
  como razón en consultas de Buenaventura).
- Perfiles `precipitacion` y `biodiversidad` con `require_direct`: la
  cadena conceptual clima→precipitación→lluvia ya no secuestra consultas
  de temperatura; la etiqueta de necesidad prioriza temperatura/clima.
- `_routes_from_recommendations`: consulta original primero; el
  enriquecimiento con conceptos solo como respaldo de recall (evita el
  segundo salto de expansión).
- Copernicus Marine enriquecido con keywords SST (temperatura superficial
  del mar) — ahora aparece en consultas de temperatura marina.
- 2 tests de regresión nuevos; suite 129/129.

---

## [v0.6.0] — 2026-10-03

Filtro geográfico `coverage` en Discovery, Recomendación y Decision Support.

### Añadido

- `backend/metadata/coverage.py`: coberturas colombianas curadas (nacional,
  32 departamentos, ciudades clave, regiones y cuencas) con jerarquía
  ciudad→departamento y semántica de cobertura (el país cubre lo
  subnacional; el departamento cubre sus ciudades; los globales cubren
  todo, opcional con `include_global`).
- `/sources?coverage=` y `/recommend?coverage=` — filtro explícito con
  `include_global` (default true).
- `/decision-support`: **detección automática** de cobertura desde la
  consulta ("… en Cali" → cali) con filtro en ambas vías (perfiles y
  recomendaciones). La respuesta expone `coverage` (requested,
  detected_auto, include_global).
- Corrige el caso U2 de la evaluación de usuario final: consultas con
  ciudad ya no recomiendan fuentes de otras ciudades.

### Añadido — Desempate de scores (v0.5.x)

- Ranking por profundidad de evidencia ante empates de score: recursos →
  keywords → dominios coincidentes → orden estable. Expuesto en
  `/recommend/info`.

---

## [v0.5.0] — 2026-10-03

Catálogo 81 fuentes · Geoservicios verificados · Intérprete NL Gemini.

### Añadido — Geoservicios verificados

- 50 endpoints ArcGIS REST verificados y cargados como recursos `geoservice`
  en 8 fuentes: ANI, ANSV, IDEAM, IGAC, INVEMAR, INVIAS, SGC y UPIT.
- Acceso a nivel de usuario vía `/sources/{id}/access?resource_id=...`
  (endpoints, método, read_only). Solo URLs con respuesta real; los dominios
  inexistentes o rutas 404 del CSV se descartaron.

### Añadido — Fuentes globales validadas por el curador (+10)

- HydroSHEDS, HydroATLAS, GRDC, WorldClim, CHELSA, WDPA (Protected Planet),
  IUCN Red List, BirdLife, Copernicus Marine y EMODnet — verificadas y
  activas; integradas a Decision Support (`MVP_SOURCES`, `SOURCE_WHERE`).

### Añadido — Intérprete NL opcional (Gemini)

- `backend/decision_support/llm_interpreter.py`: interpreta consultas en
  lenguaje natural (intents/need/concepts) con Gemini vía API key de AI
  Studio (`GEMINI_API_KEY`, `GEMINI_MODEL`, `GEMINI_TIMEOUT`).
- Cadena de modelos con reintento: GEMINI_MODEL → gemini-3.7-flash →
  gemini-3.1-pro-preview. Fallback determinista garantizado (sin key, sin
  red, cuota o JSON inválido) y trazabilidad en `interpretation` de la
  respuesta. Los motores de decisión siguen siendo deterministas
  (`ai: false`, sin inventar fuentes).

### Corregido — Disparadores de perfiles

- `concepts.py`: eliminada la expansión inversa de alias — "precipitación"
  ya no dispara el perfil de inundaciones; "cobertura" ya no dispara erosión.
- `match_need_profile`: disparo directo en consulta o ≥2 conceptos.
- 2 tests de regresión; suite 113/113.

---

## [v0.4.0] — 2026-10-02

Catálogo 71 fuentes · Decision Support ampliado · Perfil de inundación marítima.

### Añadido — Fuentes de Colombia verificadas (+38)

- 5 ministerios (MinSalud, MinEducación con geoportal ArcGIS, MinAgricultura,
  MinComercio, MinTIC), 3 corporaciones/agencias (ANH, CVC, Cormagdalena),
  3 institutos de investigación (IAvH, SINCHI, IPSE), 20 gobernaciones,
  5 alcaldías y 2 universidades (UNAL, Uniandes).
- Verificación HTTP previa de cada fuente (portal y geoservicio); solo URLs
  verificados documentados en las fichas.
- Gobernación del Meta excluida: portal sin respuesta desde la red de curaduría.

### Añadido — Decision Support

- `MVP_SOURCES` 6 → 46 fuentes (44 + DIMAR/CIOH para el perfil marítimo).
- Perfil `inundaciones_maritimas` (INVEMAR, DIMAR, CIOH) con prioridad sobre
  el perfil de inundaciones fluviales.
- `SOURCE_WHERE` curado para las 38 nuevas fuentes y DIMAR/CIOH.
- Ventana de recall de recomendaciones 8 → 15.

### Corregido

- `GENERIC_KEYWORDS` filtra preposiciones y conectores españoles ("de", "en",
  "del"…) que dispersaban el ranking por coincidencia de subcadena.
- Tests de conteo alineados al catálogo dinámico (fixtures en `conftest.py`):
  suite 105/105.
- `tests/prueba_buenaventura.py` actualizado al contrato API vigente.

### Documentación

- `docs/21_curaduria_fuentes_colombia_2026.md` — metodología de verificación,
  inventario y limitaciones.
- Restore point: `backup/restore-points/catalog-expansion-colombia-20261002-005203/`.

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
