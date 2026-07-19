# Knowledge Graph MVP — ejemplos documentados

Grafo construido desde Discovery + Metadata (curaduría humana).
Solo relaciones; metadatos completos viven en los engines previos.

## Fuentes MVP

| Source | Institution (nodo) | Dominios típicos |
|--------|--------------------|------------------|
| IDEAM | Instituto de Hidrología… | clima, hidrologia |
| INVEMAR | Instituto de Investigaciones Marinas… | oceanos_costas, biodiversidad |
| GBIF | Global Biodiversity Information Facility | biodiversidad |
| FAOSTAT | FAO | agricultura |
| WorldPop | WorldPop / University of Southampton | poblacion |
| GEE | Google Earth Engine | observacion_tierra |

## Cadenas de ejemplo

### IDEAM → Precipitación → Clima

```text
Institution(IDEAM)
  -publishes-> Source(ideam)
                 -contains-> Resource(ideam:precipitacion)
                               -belongs_to-> Domain(clima)
                               -associated_with-> Keyword(precipitacion)
```

### GBIF → Occurrence → Biodiversidad

```text
Institution(GBIF)
  -publishes-> Source(gbif)
                 -contains-> Resource(gbif:occurrence)
                               -belongs_to-> Domain(biodiversidad)
```

### INVEMAR → Ecosistemas costeros → Océanos y costas

```text
Institution(INVEMAR)
  -publishes-> Source(invemar)
                 -contains-> Resource(invemar:ecosistemas-costeros)
                               -belongs_to-> Domain(oceanos_costas)
```

### FAOSTAT → Production → Agricultura

```text
Source(fao) -contains-> Resource(fao:faostat-production)
                          -belongs_to-> Domain(agricultura)
```

### WorldPop → Population Density → Población

```text
Source(worldpop) -contains-> Resource(worldpop:population-density)
                             -belongs_to-> Domain(poblacion)
```

### GEE → Catalog → Observación de la Tierra

```text
Source(gee) -contains-> Resource(gee:catalog)
                          -belongs_to-> Domain(observacion_tierra)
```

## Consultas API

```http
GET /graph/stats
GET /graph/nodes
GET /graph/relations
GET /graph/domain/clima
GET /graph/source/ideam
GET /graph/institution/ideam
```

`GET /graph/domain/clima` responde con fuentes y resource_ids relacionados
(sin reenviar metadatos completos del Metadata Engine).
