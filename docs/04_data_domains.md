# 04 — Dominios de Datos

## Propósito

Catalogar los dominios temáticos que organiza DB2S-GEO.

## Alcance

Taxonomía temática. No incluye datasets concretos ni esquemas físicos.

## Objetivos

1. Homogeneizar la clasificación de fuentes.
2. Orientar country profiles y recommendation.
3. Facilitar navegación por problema geográfico.

## Dominios temáticos

### Geografía Base
Cartografía · Límites administrativos · Geodesia · Catastro · Tierras

Fuentes de referencia (ejemplos): IGAC · ANT · URT · datos.gov.co

### Clima
Precipitación · Temperatura · Humedad · Evapotranspiración · Aridez

Fuentes de referencia (ejemplos): IDEAM · CHIRPS · ERA5 · WorldClim · CHELSA · CGIAR Aridity Index

### Hidrología
Cuencas · Hidrografía · Caudales · Inundaciones

### Biodiversidad
Especies · Ocurrencias · Hábitats · Conectividad

### Cobertura del Suelo
Bosques · Agricultura · Pasturas · Urbanización · Monitoreo forestal

Fuentes de referencia (ejemplos): MapBiomas · ESA WorldCover · Dynamic World · Global Forest Watch

### Suelos
Carbono · Textura · Fertilidad · pH · Propiedades edáficas globales

Fuentes de referencia (ejemplos): SoilGrids · OpenLandMap

### Agricultura
Producción · Sistemas productivos · Seguridad alimentaria · Planificación rural agropecuaria

Fuentes de referencia (ejemplos): UPRA · SIPRA · FAOSTAT

### Ganadería
Sistemas pecuarios · Pasturas · Producción animal

### Riesgo
Sequías · Inundaciones · Incendios · Movimientos en masa · Sismos

### Desastres
Eventos · Impactos · Respuesta · Emergencias

### Población
Demografía · Vulnerabilidad · Pobreza · Servicios · Focalización social

Fuentes de referencia (ejemplos): DANE · SISBÉN · WorldPop

### Infraestructura
Vías · Energía · Agua · Equipamientos

### Conservación
Áreas protegidas · Corredores biológicos · Restauración · Parques nacionales

Fuentes de referencia (ejemplos): RUNAP · Parques Nacionales · Protected Planet

### Océanos
Batimetría · Manglares · Arrecifes · Corrientes

### Observación de la Tierra
Satélites · Imágenes · Radar · Sensores remotos

### Socioecología
Interacciones sociedad–ecosistema · Indicadores socioecológicos

### Tierras y ordenamiento rural
Tenencia · Restitución · Formalización · Planificación del uso agropecuario

Fuentes de referencia (ejemplos): ANT · URT · UPRA · SIPRA

### Víctimas, paz y reparación
Atención a víctimas · Reparación · Búsqueda de personas · Sistemas de información asociados

Fuentes de referencia (ejemplos): SNARIV · UARIV · UBPD

## Geomorfología

Estado: Activo

Descripción:

Disciplina orientada al estudio de las formas del relieve y los procesos que modelan la superficie terrestre.

Justificación:

La geomorfología constituye un área de conocimiento transversal para el análisis territorial, ambiental e hidrológico.

Aplicaciones:

- análisis de cuencas;
- procesos erosivos;
- modelación hidrológica;
- riesgos naturales;
- movimientos en masa;
- ordenamiento territorial;
- geomorfometría.

Conceptos asociados:

- geomorfología
- relieve
- pendientes
- geoformas
- geomorfometría
- erosión
- movimientos en masa
- disección del terreno
- estabilidad de laderas

Fuentes asociadas:

- SGC
- IDEAM
- IGAC
- Copernicus DEM
- SRTM
- ALOS
- HydroSHEDS

Dominios relacionados:

- Hidrología
- Geología
- Paisaje
- Suelos

## Paisaje

Estado: Activo

Descripción:

Dominio orientado al análisis de la estructura, función y dinámica espacial de los paisajes naturales y productivos.

Conceptos asociados:

- ecología del paisaje
- conectividad
- fragmentación
- mosaicos territoriales
- heterogeneidad
- multifuncionalidad
- resiliencia
- corredores ecológicos
- paisajes sostenibles

Dominios relacionados:

- Biodiversidad
- Coberturas
- Servicios Ecosistémicos
- Ordenamiento Territorial
- Restauración Ecológica


### Literatura científica
Descubrimiento bibliográfico · Indexación · Apoyo a citación reproducible

Fuentes de referencia (ejemplos): Google Scholar · Scopus · Web of Science

## Mapa conceptual

```text
                    ┌─ Geografía Base / Tierras y ordenamiento rural
                    ├─ Clima / Hidrología
                    ├─ Biodiversidad / Conservación
DB2S-GEO Dominios ──┼─ Cobertura / Suelos / Agricultura / Ganadería
                    ├─ Riesgo / Desastres
                    ├─ Población / Infraestructura / Socioecología
                    ├─ Víctimas, paz y reparación
                    ├─ Océanos / Observación de la Tierra
                    └─ Literatura científica
```

### Dominios metodológicos

## SIG

Estado: Activo

Conceptos asociados:

- QGIS
- ArcGIS
- PostGIS
- geoprocesamiento
- análisis espacial
- geoestadística
- álgebra de mapas


## Sensores Remotos

Estado: Activo

Conceptos asociados:

- Sentinel
- Landsat
- MODIS
- SAR
- LiDAR
- NDVI
- clasificación supervisada
- teledetección


## Relación dominio ↔ fuentes nuevas (2026)

| Dominio | Fuentes incorporadas al catálogo |
|---------|----------------------------------|
| Conservación | RUNAP · Parques Nacionales |
| Cobertura del Suelo | Global Forest Watch |
| Agricultura / Tierras | UPRA · SIPRA · ANT · URT |
| Población | SISBÉN |
| Víctimas, paz y reparación | SNARIV · UARIV · UBPD |
| Geografía Base / datos abiertos | datos.gov.co |
| Suelos | SoilGrids · OpenLandMap |
| Clima | CGIAR Aridity Index |
| Literatura científica | Google Scholar · Scopus · Web of Science |

## Secciones reservadas (futuro)

- [ ] Vocabularios controlados por dominio
- [ ] Mapeo dominio ↔ variables del Knowledge Graph
- [ ] Priorización por país y dominio
- [ ] Políticas de sensibilidad por dominio (víctimas, datos personales)

---

*Taxonomía fundacional.*
