# 06 — Catálogo de Fuentes de Datos

## Propósito

Preparar la estructura documental para registrar fuentes geoespaciales y afines.

## Alcance

Inventario estructurado y extensible. Sin conectores ni acceso en vivo.

## Objetivos

1. Organizar fuentes por categoría.
2. Facilitar crecimiento futuro del catálogo.
3. Alinear con Country Profiles y Connector Framework.

## Estructura del registro (plantilla)

```text
Fuente:
  id:            # identificador estable (futuro)
  nombre:
  categoría:
  país_o_ámbito:
  institución:
  tipo:          # API | OGC | STAC | Portal | Dataset | Hub | Catálogo bibliográfico
  dominios:      []
  estado:        # identificado | documentado | conector_pendiente
  notas:
```

## Colombia — instituciones y sistemas base

| Fuente | Estado skeleton |
|--------|-----------------|
| SIAC | Identificada |
| IDEAM | Identificada (MVP) |
| IGAC | Identificada |
| DANE | Identificada |
| SGC | Identificada |
| ANLA | Identificada |
| INVEMAR | Identificada |
| DIMAR | Identificada |
| SINCHI | Identificada |
| IIAP | Identificada |
| IAvH | Identificada |



### CIOH

Centro de Investigaciones Oceanográficas e Hidrográficas.

Dominios principales:

- Oceanografía física
- Oceanografía costera
- Hidrografía
- Monitoreo marino

Estado:
Identificada



### DIMAR

Dominios principales:

- Oceanografía
- Hidrografía marítima
- Cartografía náutica
- Información marítima

Estado:
Identificada


### IDEAM

Métodos de acceso identificados:

- Portal institucional
- API Socrata
- Servicios geoespaciales
- CapasGeo IDEAM
- Documentación técnica

Repositorio de descargas:

https://bart.ideam.gov.co/cneideam/Capasgeo/

Tipo:
Repositorio oficial de capas geográficas descargables.


## Colombia — conservación y áreas protegidas

| Fuente | Estado skeleton | Notas conceptuales |
|--------|-----------------|--------------------|
| RUNAP | Identificada | Registro Único Nacional de Áreas Protegidas |
| Parques Nacionales | Identificada | Parques Nacionales Naturales de Colombia |

## Colombia — tierras, ruralidad y planificación agropecuaria

| Fuente | Estado skeleton | Notas conceptuales |
|--------|-----------------|--------------------|
| UPRA | Identificada | Unidad de Planificación Rural Agropecuaria |
| SIPRA | Identificada | Sistema de Información para la Planificación Rural Agropecuaria |
| ANT | Identificada | Agencia Nacional de Tierras |
| URT | Identificada | Unidad de Restitución de Tierras |

## Colombia — población, víctimas, paz y focalización social

| Fuente | Estado skeleton | Notas conceptuales |
|--------|-----------------|--------------------|
| SNARIV | Identificada | Sistema Nacional de Atención y Reparación Integral a las Víctimas |
| UARIV | Identificada | Unidad para la Atención y Reparación Integral a las Víctimas |
| SISBÉN | Identificada | Sistema de Identificación de Potenciales Beneficiarios de Programas Sociales |
| UBPD | Identificada | Unidad de Búsqueda de Personas dadas por Desaparecidas |

## Colombia — datos abiertos

| Fuente | Estado skeleton | Notas conceptuales |
|--------|-----------------|--------------------|
| datos.gov.co | Identificada | Portal nacional de datos abiertos |

## Observación de la Tierra

| Fuente | Estado skeleton |
|--------|-----------------|
| NASA (EarthData, LP DAAC, GES DISC, ORNL, Giovanni, AppEEARS, FIRMS, …) | Identificada |
| Copernicus / Sentinel (1, 2, 3, 5P, 6) | Identificada |
| Landsat | Identificada |
| ASF | Identificada |
| GEE | Identificada (MVP) |
| Planetary Computer | Identificada |

## Biodiversidad

GBIF (MVP) · eBird · BirdCast · SiB Colombia · iNaturalist · OBIS · BIEN · Macaulay Library · Protected Planet

## Coberturas y bosques

| Fuente | Estado skeleton |
|--------|-----------------|
| MapBiomas | Identificada |
| ESA WorldCover | Identificada |
| Dynamic World | Identificada |
| Global Forest Watch | Identificada |
| Global Mangrove Watch | Identificada |
| CORINE | Identificada |

## Clima

| Fuente | Estado skeleton |
|--------|-----------------|
| CHIRPS | Identificada |
| ERA5 | Identificada |
| WorldClim | Identificada |
| CHELSA | Identificada |
| IRI | Identificada |
| GPM | Identificada |
| GLDAS | Identificada |
| MERRA-2 | Identificada |
| CGIAR Aridity Index | Identificada |

## Hidrología (relacionadas)

HydroSHEDS · MERIT Hydro · IDEAM

## Suelos

| Fuente | Estado skeleton |
|--------|-----------------|
| SoilGrids (ISRIC) | Identificada |
| OpenLandMap | Identificada |

## Socioeconómico

FAOSTAT (MVP) · WaPOR · Banco Mundial · WorldPop (MVP) · HDX · ONU · ODS · OECD

## Riesgo

UNOSAT · EM-DAT · DesInventar · INFORM · USGS Hazards · Copernicus Emergency · Global Flood Database · FIRMS

## Literatura científica (descubrimiento y citación)

| Fuente | Estado skeleton | Rol conceptual en DB2S-GEO |
|--------|-----------------|----------------------------|
| Google Scholar | Identificada | Descubrimiento bibliográfico / apoyo a Citation Engine |
| Scopus | Identificada | Indexación científica / citación |
| Web of Science | Identificada | Indexación científica / citación |

## Plataformas / hubs adicionales

ArcGIS Living Atlas · ArcGIS Hub · Earth Search

## Resumen de incorporación documental (2026)

Nuevas fuentes registradas en esta actualización:

```text
Colombia:
  RUNAP · Parques Nacionales · UPRA · SIPRA · ANT · URT
  SNARIV · UARIV · SISBÉN · UBPD · datos.gov.co

Globales / especializadas:
  Global Forest Watch · SoilGrids · OpenLandMap · CGIAR Aridity Index

Literatura científica:
  Google Scholar · Scopus · Web of Science
```

## Ubicación en repositorio

```text
datasets/catalog/     # registros futuros del catálogo
connectors/           # un conector por fuente prioritaria
docs/06_...           # este documento
country_profiles/     # priorización nacional
```

## Secciones reservadas (futuro)

- [ ] Fichas completas por fuente
- [ ] URLs y licencias verificadas
- [ ] Cobertura espacial/temporal
- [ ] Estado de conector asociado
- [ ] Clasificación de sensibilidad (p. ej. víctimas, datos personales)

---

*Catálogo preparado para crecimiento. Sin implementaciones.*


