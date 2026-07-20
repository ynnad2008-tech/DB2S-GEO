# DB2S-GEO — ENRICHMENT INDEX

## Objetivo

Mantener una hoja de ruta única para el enriquecimiento incremental
de la base de conocimiento DB2S-GEO.

Todos los recursos incorporados deben seguir el flujo:

```text
Conector
→ Discovery
→ Metadata
→ Knowledge Graph
→ Recommendation
→ Tests
```

## Reglas Operativas

1. Máximo 2 recursos por iteración.
2. No modificar motores durante el enriquecimiento.
3. Validar siempre:
   - Discovery
   - Access
   - Knowledge Graph
   - Recommendation
   - Tests
4. No hacer commit automático.
5. No hacer push automático.
6. Actualizar este índice al finalizar cada iteración.

---

# FASE 1 — IDEAM

## COMPLETADO

- [x] ideam:capas-ideam-rest
- [x] ideam:amenaza-inundacion

---

# FASE 2 — INVEMAR

## COMPLETADO

- [x] invemar:manglares-colombia
- [x] invemar:ecorregiones-marinas

---

# FASE 3 — GBIF

## COMPLETADO

- [x] gbif:occurrence-colombia
- [x] gbif:species-colombia

---

# FASE 4 — SGC

## COMPLETADO

- [x] sgc:amenaza-sismica
- [x] sgc:simma-geologia

---

# FASE 5 — DEMOGRAFÍA

## COMPLETADO

- [x] worldpop:colombia

---

# FASE 6 — CLIMA

## COMPLETADO

- [x] gee:chirps
- [x] gee-copernicus-sentinel2:dynamicworld

---

# FASE 7 — ECOSISTEMAS

## COMPLETADO

- [x] ideam:estado-ecosistemas

---

# FASE 8 — OBSERVATORIOS

## COMPLETADO

- [x] invemar:siam

---

# MÉTRICAS DEL PROGRAMA

Estado actual:

- Recursos en KG (Resource nodes): 71
- Fuentes MVP: 23 (incluye Supertransporte)
- Motores modificados: 0
- Regresiones: 0
- Iteraciones de enriquecimiento completadas: 29
- Proceso validado: Sí
- PENDIENTES del índice: **0** (índice agotado)

Última iteración:

- supertransporte:visor-maritimo-fluvial
- supertransporte:observatorio-vigilancia

Próximos 2 PENDIENTE (sugeridos):

1. — (ninguno; índice FASE 1–17 cerrado)
2. — (definir FASE 18 si se amplía el inventario)

---

# FASE 9 — HIDROLOGÍA Y AGUA

Esta fase se deriva del inventario Geodata Agua compilado por Rodolfo Franco
y prioriza recursos ampliamente utilizados en Colombia para monitoreo,
hidrología, precipitación y aguas subterráneas.

## COMPLETADO

- [x] ideam:fews-colombia
- [x] gee:chirps-colombia
- [x] nasa:imerg-colombia
- [x] mapbiomas:agua-colombia
- [x] sgc:agua-subterranea
- [x] nasa:grace-groundwater-colombia

---

# FASE 10 — GESTIÓN DEL RIESGO DE DESASTRES

Objetivo:

Fortalecer la cobertura nacional de amenazas naturales,
gestión del riesgo, monitoreo de desastres y análisis de exposición.

## COMPLETADO

- [x] sgc:amenaza-sismica
- [x] sgc:simma-geologia
- [x] worldpop:colombia
- [x] ideam:fews-colombia
- [x] gee:chirps-colombia
- [x] nasa:imerg-colombia
- [x] unosat:disaster-mapping
- [x] igac:modelo-terreno-colombia

---

# FASE 11 — AGROPECUARIO Y TIERRAS

Objetivo:

Fortalecer la cobertura temática de agricultura, uso del suelo,
aptitud productiva, sistemas agropecuarios y planificación rural
en Colombia.

## COMPLETADO

- [x] igac:estudio-general-suelos
- [x] igac:agrologia-colombia
- [x] upra:aptitud-agropecuaria
- [x] upra:frontera-agricola
- [x] upra:zonificacion-productiva

---

# FASE 12 — COBERTURA Y USO DEL SUELO

Objetivo:

Complementar los recursos ambientales y agropecuarios mediante
capas de cobertura, transformación del paisaje y monitoreo del
territorio.

## COMPLETADO

- [x] mapbiomas:cobertura-colombia
- [x] mapbiomas:transiciones-cobertura

---

# FASE 13 — CATASTRO Y TERRITORIO

Objetivo:

Incorporar información geográfica oficial para apoyar análisis
territoriales, catastrales y de planificación.

## COMPLETADO

- [x] igac:geoportal-nacional
- [x] igac:servicios-geograficos

---

# FASE 14 — SEGURIDAD ALIMENTARIA Y PRODUCCIÓN

Objetivo:

Fortalecer la cobertura sobre producción agropecuaria,
seguridad alimentaria y análisis productivo.

## COMPLETADO

- [x] dane:encuesta-agropecuaria
- [x] dane:eva-agricola

---

# FASE 15 — CATASTRO MULTIPROPÓSITO

Objetivo:

Incorporar los principales recursos nacionales asociados al
Catastro Multipropósito, consulta predial, jurisdicciones
catastrales y administración del territorio.

## COMPLETADO

- [x] igac:catastro-multiproposito
- [x] igac:datos-abiertos-catastro
- [x] igac:colombia-en-mapas-catastro
- [x] igac:consulta-catastral
- [x] igac:gestores-catastrales
- [x] dnp:catastro-multiproposito

---

# FASE 16 — INVERSIÓN PÚBLICA Y SERVICIOS

Objetivo:

Incorporar fuentes oficiales para el análisis territorial de
inversión pública, infraestructura, control fiscal y cobertura
de servicios públicos en Colombia.

## COMPLETADO

- [x] dnp:mapa-inversiones
- [x] contraloria:obras-infraestructura
- [x] superservicios:cobertura-servicios-publicos
- [x] superservicios:captacion-servicios-publicos

---

# FASE 17 — VÍAS, TRANSPORTE Y LOGÍSTICA

Objetivo:

Incorporar fuentes oficiales relacionadas con infraestructura vial,
movilidad, transporte multimodal, seguridad vial, concesiones e
infraestructura logística de Colombia.

## COMPLETADO

- [x] mintransporte:sinc
- [x] upit:hub-transporte
- [x] invias:hermes
- [x] invias:vulnerabilidad-faunistica
- [x] invias:datos-abiertos-viales
- [x] ansv:siniestralidad-vial
- [x] ani:aniscopio
- [x] ani:atlas-concesiones
- [x] ani:fichas-portuarias
- [x] supertransporte:visor-maritimo-fluvial
- [x] supertransporte:observatorio-vigilancia

---

## Notas (iteración 29)

- Conector nuevo: `supertransporte` v1.0.0 (2 recursos).
- Visor: infraestructura marítima/fluvial no concesionada + apps digitales.
- Observatorio: vigilancia, inspección, control (VIGIA) e indicadores sectoriales.

---

# PROMPT OPERATIVO ESTÁNDAR

```text
EJECUTAR SEGÚN ENRICHMENT_INDEX

Tomar los siguientes 2 recursos marcados como PENDIENTE.

Aplicar el patrón validado de enriquecimiento.

Validar:

- Discovery
- Access
- Knowledge Graph
- Recommendation
- Tests

Actualizar ENRICHMENT_INDEX.

Generar informe técnico.

No hacer commit.
No hacer push.
```
