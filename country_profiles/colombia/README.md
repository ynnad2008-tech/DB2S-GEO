# Country Profile — Colombia

> Plantilla estandarizada DB2S-GEO · Solo documentación · Sin conectores operativos

| Campo | Valor |
|-------|-------|
| País | Colombia |
| Código carpeta | colombia |
| Estado | plantilla ampliada (fuentes identificadas) |
| Última actualización | 2026-07 |

---

## 1. Instituciones geográficas

| Institución | Sigla | Rol | URL | Notas |
|-------------|-------|-----|-----|-------|
| Instituto Geográfico Agustín Codazzi | IGAC | Cartografía, catastro, geodesia | | Identificada |
| Servicio Geológico Colombiano | SGC | Geología, amenazas geológicas | | Identificada |
| Agencia Nacional de Tierras | ANT | Tierras, formalización | | Identificada |
| Unidad de Restitución de Tierras | URT | Restitución de tierras | | Identificada |

---

## 2. Instituciones ambientales

| Institución | Sigla | Rol | URL | Notas |
|-------------|-------|-----|-----|-------|
| Sistema de Información Ambiental de Colombia | SIAC | Información ambiental | | Identificada |
| Autoridad Nacional de Licencias Ambientales | ANLA | Licenciamiento ambiental | | Identificada |
| Instituto de Investigación de Recursos Biológicos Alexander von Humboldt | IAvH | Biodiversidad | | Identificada |
| Instituto Amazónico de Investigaciones Científicas | SINCHI | Amazonía | | Identificada |
| Instituto de Investigaciones Ambientales del Pacífico | IIAP | Pacífico | | Identificada |
| Instituto de Investigaciones Marinas y Costeras | INVEMAR | Marino-costero | | Identificada |
| Dirección General Marítima | DIMAR | Ámbito marítimo | | Identificada |
| Parques Nacionales Naturales de Colombia | PNN / Parques Nacionales | Áreas protegidas nacionales | | Identificada |
| Registro Único Nacional de Áreas Protegidas | RUNAP | Registro de áreas protegidas | | Identificada (sistema) |

---

## 3. Instituciones meteorológicas / climáticas

| Institución | Sigla | Rol | URL | Notas |
|-------------|-------|-----|-----|-------|
| Instituto de Hidrología, Meteorología y Estudios Ambientales | IDEAM | Clima, hidrología, ambiente | | Identificada (MVP) |

---

## 4. Instituciones estadísticas y focalización social

| Institución | Sigla | Rol | URL | Notas |
|-------------|-------|-----|-----|-------|
| Departamento Administrativo Nacional de Estadística | DANE | Estadística oficial | | Identificada |
| Sistema de Identificación de Potenciales Beneficiarios de Programas Sociales | SISBÉN | Focalización social | | Identificada |

---

## 5. Instituciones de tierras, ruralidad y planificación agropecuaria

| Institución / sistema | Sigla | Rol | Notas |
|----------------------|-------|-----|-------|
| Unidad de Planificación Rural Agropecuaria | UPRA | Planificación rural agropecuaria | Identificada |
| Sistema de Información para la Planificación Rural Agropecuaria | SIPRA | Información para planificación agropecuaria | Identificada |
| Agencia Nacional de Tierras | ANT | Tierras | Identificada |
| Unidad de Restitución de Tierras | URT | Restitución | Identificada |

---

## 6. Instituciones y sistemas de víctimas, paz y reparación

| Institución / sistema | Sigla | Rol | Notas |
|----------------------|-------|-----|-------|
| Sistema Nacional de Atención y Reparación Integral a las Víctimas | SNARIV | Sistema nacional | Identificada |
| Unidad para la Atención y Reparación Integral a las Víctimas | UARIV | Atención y reparación | Identificada |
| Unidad de Búsqueda de Personas dadas por Desaparecidas | UBPD | Búsqueda de personas | Identificada |

---

## 7. Geoportales y portales de datos

| Nombre | Tipo | URL | Protocolos | Notas |
|--------|------|-----|------------|-------|
| datos.gov.co | Portal de datos abiertos | | | Identificado — hub nacional |
| RUNAP | Registro / geoportal temático | | | Áreas protegidas |
| SIPRA | Sistema de información | | | Planificación agropecuaria |
| SIAC | Sistema ambiental | | | Identificado |

---

## 8. APIs y servicios

| Nombre | Proveedor | Tipo | URL / endpoint | Estado |
|--------|-----------|------|----------------|--------|
| *Por documentar* | IDEAM | | | Identificada (MVP futuro) |
| *Por documentar* | datos.gov.co | Portal / API | | Identificada |
| *Por documentar* | RUNAP / PNN | | | Identificada |

---

## 9. Fuentes prioritarias (borrador)

Según política: Oficial nacional → Regional → Global → Complementaria.

| Prioridad | Fuente | Dominios | Notas |
|-----------|--------|----------|-------|
| 1 | IDEAM · IGAC · DANE · RUNAP · Parques Nacionales · UPRA · SIPRA · ANT · URT · datos.gov.co | Clima, geografía, población, conservación, tierras | Oficiales nacionales |
| 1 | SNARIV · UARIV · SISBÉN · UBPD | Población / víctimas / paz | Oficiales; sensibilidad ética alta |
| 2 | CATIE (regional, cuando aplique) | Socioecología / rural | Regional especializada |
| 3 | Global Forest Watch · SoilGrids · OpenLandMap · CGIAR Aridity Index | Cobertura, suelos, clima | Globales |
| 4 | Google Scholar · Scopus · Web of Science | Literatura científica | Complementarias a citación |

---

## 10. Observaciones

- Las fuentes de víctimas, paz y focalización social requieren políticas de sensibilidad y uso ético (ver `docs/15_security_model.md`).
- `datos.gov.co` actúa como hub de descubrimiento; no sustituye a las instituciones productoras.
- RUNAP y Parques Nacionales se relacionan en el Knowledge Graph bajo el tema Conservación.
- UPRA/SIPRA y ANT/URT se relacionan bajo Agricultura / Tierras y ordenamiento rural.

---

## 11. Relación con conectores

| Fuente | Conector (`connectors/`) | Estado |
|--------|--------------------------|--------|
| IDEAM | `connectors/ideam/` | skeleton (MVP) |
| IGAC | `connectors/igac/` | skeleton |
| DANE | `connectors/dane/` | skeleton |
| RUNAP | — | identificado — conector pendiente |
| Parques Nacionales | — | identificado — conector pendiente |
| UPRA | — | identificado — conector pendiente |
| SIPRA | — | identificado — conector pendiente |
| ANT | — | identificado — conector pendiente |
| URT | — | identificado — conector pendiente |
| SNARIV | — | identificado — conector pendiente |
| UARIV | — | identificado — conector pendiente |
| SISBÉN | — | identificado — conector pendiente |
| UBPD | — | identificado — conector pendiente |
| datos.gov.co | — | identificado — conector pendiente |

---

*Ver docs/05_country_profiles.md y docs/06_data_sources_catalog.md*

## Fuentes Colombia — inventario consolidado

**Base previa:** IGAC · IDEAM · DANE · SGC · SIAC · ANLA · INVEMAR · DIMAR · IAvH · SINCHI · IIAP

**Incorporadas 2026:** RUNAP · Parques Nacionales · UPRA · SIPRA · ANT · URT · SNARIV · UARIV · SISBÉN · UBPD · datos.gov.co
