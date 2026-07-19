# Roadmap — DB2S-GEO

## Propósito

Definir las fases de evolución del proyecto desde la arquitectura hasta la API pública.

## Estado actual

**Alpha Release — DB2S-GEO v0.9** (preparación para publicación)

Fases 0–8.1 entregadas. Prioridad: presentación, documentación, despliegue.

---

## Vista general

```text
Fase 0    Arquitectura                         ✓
Fase 0.5  Consolidación conceptual             ✓
Fase 1    Discovery Engine MVP                 ✓
Fase 2    Metadata Engine MVP                  ✓
Fase 3    Knowledge Graph MVP                  ✓
Fase 4    Recommendation Engine MVP            ✓
Fase 5    Watcher Engine MVP                   ✓
Fase 6    Source Discovery Assistant MVP       ✓
Fase 7    Curator Workbench MVP (+ 7.1 UX)     ✓
Fase 8    Decision Support Engine MVP          ✓
Fase 8.1  Knowledge Usage Observatory MVP      ✓
Fase α    Alpha Release (publicación)          ✓
Fase 9    API pública / Agentes IA (reservado)
```

---

## Fase 0 — Arquitectura

**Objetivo:** Base estructural, documental y contractual.

**Entregables:**
- Estructura de repositorio
- Documentación fundacional (`docs/`)
- Charter y roadmap
- Plantillas de country profiles
- Interfaces y contratos del Connector Framework
- Modelos conceptuales del Knowledge Graph
- Esqueletos de backend / frontend / agents
- Catálogo documental ampliado de fuentes identificadas (sin conectores)

**Criterio de cierre:** Skeleton completo sin lógica de negocio. ✓

### Fuentes identificadas (backlog documental — sin implementación)

```text
Colombia:
  RUNAP · Parques Nacionales · UPRA · SIPRA · ANT · URT
  SNARIV · UARIV · SISBÉN · UBPD · datos.gov.co

Globales / especializadas:
  Global Forest Watch · SoilGrids · OpenLandMap · CGIAR Aridity Index

Literatura científica (apoyo Citation / Discovery):
  Google Scholar · Scopus · Web of Science
```

---

## Fase 1 — Discovery Engine

**Objetivo:** Capacidad de descubrir fuentes, describirlas, mostrar metadatos/atribución y citar.

**MVP entregado:**
- Discovery Engine operativo (`backend/discovery/`)
- Citation Engine básico integrado (`backend/citation/`)
- 5 conectores MVP: IDEAM · GBIF · FAOSTAT · WorldPop · GEE
- API mínima: `GET /sources`, `/sources/{id}`, `/citation`, `/access`
- Respuestas normalizadas + curaduría humana + read-only

**Fuera de alcance (aún reservado):**
- OpenSearch / indexación distribuida
- Autenticación, IA, Recommendation, Watcher, descargas, procesamiento geoespacial

---

## Fase 2 — Metadata Engine / Knowledge Graph

**Metadata Engine MVP (entregado en Fase 2):**
- Normalización de recursos (`backend/metadata/`)
- Dominios temáticos iniciales
- Endpoints: `/sources/{id}/resources`, `/domains`
- Conector INVEMAR añadido al MVP
- Puente listo para Knowledge Graph

**Knowledge Graph MVP (entregado en Fase 3):**
- Grafo en memoria Python puro (`backend/knowledge_graph/`)
- Nodos: Institution · Source · Resource · Domain · Keyword
- Relaciones: publishes · contains · belongs_to · associated_with
- Construido SOBRE Discovery + Metadata (sin duplicar metadatos)
- Endpoints: `/graph/stats`, `/graph/nodes`, `/graph/relations`,
  `/graph/domain/{id}`, `/graph/source/{id}`, `/graph/institution/{id}`
- Sin Neo4j / RDF / SPARQL / GraphDB

**Reservado (post-MVP grafo):** persistencia e inferencia avanzada.

**Entidades documentales futuras:**
Institución → Fuente → Dataset → Variable → Servicio → API → Método de acceso → Referencia → Caso de uso → País → Tema

---

## Fase 3 — Recommendation Engine

> *Nota:* Knowledge Graph MVP = Fase 3 implementada; Recommendation = **Fase 4**.

**Recommendation Engine MVP (entregado en Fase 4):**
- Scoring determinista sobre Knowledge Graph (`backend/recommendation/`)
- Explicabilidad obligatoria: `score` · `reason` · `relations_used`
- Sin IA / embeddings / LLMs
- Endpoints: `/recommend?q=` · `/recommend/domain/{id}` ·
  `/recommend/source/{id}` · `/recommend/resource/{id}`

**Scores conceptuales futuros (docs/08):** Scientific · Trust · GIS · AI · Sustainability

**Reservado:** pesos calibrados por país/caso de uso.

**Objetivo:** Recomendar fuentes según problema territorial.

**Scores previstos:**
- Scientific Score
- Trust Score
- GIS Score
- AI Score
- Sustainability Score

**Reservado:** Algoritmos y pesos.

---

## Fase 4 — Citation Engine

**Objetivo:** Generar referencias reproducibles.

**Formatos previstos:** APA, BibTeX, RIS, DOI, referencia oficial.

**Estado parcial (Fase 1):** referencia oficial · APA · DOI cuando existe · fecha de consulta.

**Fuentes bibliográficas de apoyo (documentadas, no implementadas):**
Google Scholar · Scopus · Web of Science

**Reservado:** BibTeX, RIS, plantillas finales ampliadas.

---

## Fase 5 — Conectores prioritarios (MVP)

**Conectores MVP (operativos en Fases 1–2):**
1. IDEAM
2. INVEMAR
3. GBIF
4. FAOSTAT
5. WorldPop
6. Google Earth Engine

**Capacidades MVP:** descubrir, describir, metadatos normalizados, acceso informativo, citar.

**Reservado post-MVP:** acceso live a APIs, parsers, sincronización de catálogos.

### Post-MVP — candidatos documentales a conector (no priorizados aún)

```text
Colombia: RUNAP · Parques Nacionales · UPRA · SIPRA · ANT · URT
          SNARIV · UARIV · SISBÉN · UBPD · datos.gov.co
Globales: Global Forest Watch · SoilGrids · OpenLandMap · CGIAR Aridity Index
```

*La priorización post-MVP queda sujeta a gobernanza (`docs/19_governance.md`).*

---

## Fase 6 — Agentes IA / Source Discovery

**Source Discovery Assistant MVP (entregado como Fase 6 de implementación 2026):**
- Análisis heurístico de URLs (`backend/source_discovery/`)
- Candidatos persistidos localmente (sin catálogo)
- Endpoints `/source-discovery/*`
- Principio: el sistema propone; los curadores deciden

**Agentes IA (reservado):**
Discover · Compare · Cite · Code · Advisor · Watcher
Prompts, orquestación MCP.

---

## Fase 7 — Curator Workbench / Watcher docs

**Curator Workbench MVP (entregado como Fase 7 de implementación 2026):**
- Consola HTML/CSS/JS en `frontend/workbench/`
- Ruta: `/workbench/`
- Sin React/Vue/Angular · sin mapas · sin auth avanzada

**Fase 7.1 — UX Simplification (entregado):**
- Página **Inicio** con métricas: Fuentes · Recursos · Dominios · Eventos · Candidatos
- Navegación: Inicio · Explorar · Recomendaciones · Monitoreo · Administración
- Knowledge Graph, Watcher técnico y Candidate Sources como **secciones avanzadas**
- Tipografía/espaciado/branding DB2S-GEO; complejidad técnica oculta al inicio

**Watcher Engine MVP:** ver Fase 5 (implementación).


---

## Fase 8 — Decision Support Engine MVP

**Objetivo:** Orientar al usuario hacia **acciones concretas** para resolver una necesidad.

**Entregado:**
- Módulo `backend/decision_support/`
- Flujo: Consulta → necesidad → rutas de acción → fuente → recursos → justificación
- Intenciones: descargar, analizar, monitorear, comparar, evaluar, estudiar, identificar
- Normalización de conceptos (agua→hidrología, lluvia→precipitación, inundaciones→hidrología+precipitación, erosión→suelos+…)
- Categorías de acción (descargar, APIs, portales, análisis geoespacial, complementaria)
- API: `GET /decision-support?q=` · `GET /decision-support/info`
- Sin IA; solo fuentes MVP; explicabilidad obligatoria

---

## Fase 8.1 — Knowledge Usage Observatory MVP

**Objetivo:** Registrar consultas **anónimas** para mejorar recomendaciones, detectar vacíos y priorizar expansión del catálogo.

**Entregado:**
- Módulo `backend/observatory/`
- Persistencia local `data/observatory/queries.json` (sin PII / sin IP)
- Auto-registro en `/recommend`, `/decision-support` y búsqueda `/sources?q=`
- Analítica: top consultas, sin resultado, dominios, emergentes, timeline, wordcloud
- Workbench: sección **Observatorio** + aviso de transparencia
- API: `/observatory/*`

---

## Alpha Release — v0.9

**Objetivo:** Preparar publicación y pruebas con usuarios externos.

**Entregado:**
- Páginas: Acerca de · Cómo citar · Autoría
- Sello «¡Validado por humanos!»
- Footer institucional (© 2026 · autor · versión · citar)
- `ALPHA_DEPLOYMENT.md` · README público · `Dockerfile`
- Versión `0.9.0-alpha` / etiqueta `DB2S-GEO v0.9 Alpha`

---

## Fase 9 — API pública (reservado)

**Objetivo:** Exponer capacidades vía API Gateway endurecida.

**Reservado:** Versionado, autenticación, rate limiting, SLAs.

---

## Dependencias entre fases

```text
Fase 0
  └─► Fase 1 (Discovery)
        └─► Fase 2 (Metadata / KG)
              ├─► Fase 3–4 (Recommendation / Citation)
              ├─► Fase 5 (Watcher)
              ├─► Fase 6 (Source Discovery)
              ├─► Fase 7 (Workbench + 7.1 UX)
              └─► Fase 8 (Decision Support)
                    └─► Fase 9 (API pública)
```

---

## Notas

- Este roadmap es orientativo y sujeto a gobernanza del proyecto.
- El detalle por fase se amplía en `docs/18_roadmap.md` y `docs/17_mvp.md`.
- No se adelanta implementación fuera de la fase activa.

---

*Cortesía: DB2S · Autor: Dany Arbey Benavides Bolaños*