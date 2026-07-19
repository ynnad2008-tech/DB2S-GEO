# Relaciones conceptuales

## Cadena canónica

```text
Institution → Source → Dataset → Variable → Service → API → AccessMethod → Reference → UseCase
```

## Relaciones adicionales

```text
Country ——owns/hosts——► Institution
Theme ——classifies——► Dataset
UseCase ——recommends——► Dataset
Source ——exposes——► Service
Dataset ——cited_by——► Reference
Reference ——indexed_in——► BibliographicIndex
OpenDataPortal ——harvests——► Source / Dataset
```

## Ejemplos de nodos por tema (Colombia / globales)

```text
Conservación:     Parques Nacionales · RUNAP
Tierras/Rural:    UPRA · SIPRA · ANT · URT
Víctimas/Paz:     SNARIV · UARIV · UBPD · SISBÉN
Datos abiertos:   datos.gov.co
Cobertura:        Global Forest Watch
Suelos:           SoilGrids · OpenLandMap
Clima:            CGIAR Aridity Index
Literatura:       Google Scholar · Scopus · Web of Science
```
