# 21 — Curaduría: fuentes de Colombia y ampliación del Decision Support

**Fecha:** 2026-10-02 · **Autor de la curaduría:** Dany A. Benavides (con asistencia técnica de IA)
**Estado:** aplicado, verificado y respaldado.

---

## 1. Alcance

Incorporación de 38 fuentes oficiales de Colombia pendientes en
`csv/fuentes_pendientes.csv`, con verificación previa de cada fuente y
activación en el catálogo JSON-first. Ampliación del motor de apoyo a la
decisión para que las nuevas fuentes participen en rutas de acción, junto con
dos mejoras de calidad del ranking y un perfil nuevo de inundación
marítima/costera.

## 2. Metodología de verificación (capacidad 9: evaluación de fuentes)

1. **Identificación**: cruce de `fuentes_pendientes.csv` y los perfiles de país
   contra los conectores activos del catálogo → 39 candidatas de Colombia.
2. **Verificación HTTP** por cada candidata (geoservicio y portal): HEAD con
   respaldo GET, reintentos (3) para fallos de DNS, y `curl` con User-Agent de
   navegador como segunda opinión para 403/500/timeout.
3. **Criterio de evidencia**: todas las 38 cargadas son organismos oficiales
   colombianos o instituciones académicas → **nivel de evidencia alto**
   (organismos oficiales y documentación institucional).
4. **Regla de no invención**: en cada ficha solo se documentan URLs verificados.
   Los geoservicios `geoportal.X.gov.co` del CSV resultaron en su mayoría
   dominios inexistentes (fallo DNS consistente); solo se incluyó el geoportal
   de MinEducación, único con respuesta real (HTTP 200).

## 3. Fuentes cargadas (38)

| Grupo | Fuentes |
|---|---|
| Ministerios | minsalud, mineducacion (portal + geoportal ArcGIS), minagricultura, mincomercio, mintic |
| Corporaciones y agencias | anh, cvc, cormagdalena |
| Institutos de investigación | humboldt (IAvH), sinchi, ipse |
| Gobernaciones (20) | antioquia, cundinamarca, tolima, valle, santander, boyaca, narino, caldas, risaralda, quindio, cauca, huila, nortedesantander, cesar, magdalena, cordoba, sucre, bolivar, atlantico, choco |
| Alcaldías (5) | cali, barranquilla, cartagena, pereira, manizales |
| Universidades | unal, uniandes |

**Excluida:** `gob-meta` (Gobernación del Meta) — portal sin respuesta desde la
red de curaduría (timeout en 4 intentos). Pendiente de reverificación.

**Observación de verificación:** 4 portales responden con WAF anti-bot
(HTTP 403 para clientes automáticos; dominio y TLS activos): boyaca, magdalena,
barranquilla, cartagena. Se cargaron según el estándar del propio repositorio
(`scripts/verificar_urls.py`: 403 = "URL probablemente OK"), con la advertencia
registrada en este documento.

## 4. Cambios de motor

| Archivo | Cambio |
|---|---|
| `backend/decision_support/engine.py` | `MVP_SOURCES` 6 → 46 (44 + dimar/cioh); ventana de recall 8 → 15 |
| `backend/decision_support/actions.py` | `SOURCE_WHERE` curado para las 38 nuevas + dimar/cioh; nuevo perfil `inundaciones_maritimas` (invemar, dimar, cioh) con prioridad sobre el perfil fluvial |
| `backend/recommendation/scoring.py` | `GENERIC_KEYWORDS` ampliado con preposiciones y conectores españoles (ruido de ranking por subcadena) |
| `tests/unit/conftest.py` | Fixtures `active_catalog_ids` / `active_catalog_count`: los tests de conteo siguen al catálogo curado, no a números fijos |
| `tests/prueba_buenaventura.py` | Escenario e2e actualizado al contrato API vigente |

## 5. Estado del sistema (verificado en vivo)

| Métrica | Antes | Después |
|---|---|---|
| Fuentes activas | 33 | **71** |
| Recursos | 130 | **169** |
| Nodos del Knowledge Graph | 960 | **1190** |
| Aristas | 2739 | **3075** |
| Tests | 93 passed / 11 failed (stale) | **105 passed** |
| Integridad de grafo | — | 24/24 chequeos OK |

Verificación de integridad: toda arista referencia nodos existentes; toda
fuente activa tiene nodo Source y relación `publishes` desde su Institution;
todo recurso tiene nodo Resource y relación `contains`; stats de la API
consistentes con los datos servidos.

Efecto e2e confirmado: `prueba_buenaventura.py`, `simulacion_morfometria.py`,
`simulacion_pacifico.py` y `simulacion_dagua.py` completan; las rutas de
decision-support arrastran `relations_used` con aristas reales del grafo
(ej. invemar 7, dimar 19, cioh 13).

## 6. Caso de uso corregido: "inundacion maritima"

Antes, la consulta caía en el perfil de inundaciones fluviales (ideam, gee,
worldpop). Ahora dispara el perfil `inundaciones_maritimas`:
invemar (ecosistemas costeros y manglares), dimar (IDE marítima y pronósticos
meteomarinos) y cioh (mareas y oceanografía operacional). El perfil fluvial
queda intacto para consultas de microcuenca.

## 7. Limitaciones conocidas (orden de prioridad sugerido)

1. **Geografía de la consulta no se aplica**: "en Cali" o "Valle del Cauca" no
   filtran ni reordenan resultados (`country_or_scope` no entra en el haystack
   de búsqueda; no existe filtro `coverage`). Propuesta: filtro `coverage` en
   `/sources` y `/recommend` con lista curada de coberturas colombianas.
2. **Preemption de perfiles por expansión de conceptos**: consultas como
   "cobertura educativa" pueden activar el perfil de erosión vía el concepto
   "suelos". Requiere disparadores más estrictos.
3. **Scores saturados en 100**: empates frecuentes en el tope del ranking;
   se propone desempate por cobertura o profundidad de metadatos.
4. **Fuentes globales pendientes**: ~20 candidatas realmente nuevas en
   `csv/deepseek_fuentes_globales.csv` (CHIRPS, ERA5, WorldClim, CHELSA, GPM,
   HydroSHEDS, GSW, OBIS, NOAA, USGS Hazards, etc.), más 26 fuentes de otros
   países (Honduras, Costa Rica, México, Perú) en `fuentes_pendientes.csv`.

## 8. Respaldo

Restore point: `backup/restore-points/catalog-expansion-colombia-20261002-005203/`
(catálogo completo, motor, tests y reporte de validación + README de inventario).
