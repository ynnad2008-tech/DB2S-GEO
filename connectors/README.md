# Connector Framework — DB2S-GEO

Arquitectura de conectores independientes.

**Fase 1:** conectores MVP operativos con metadatos curados (read-only).  
**No** hay descarga de datos ni ejecución de código externo.

## Principio

Cada fuente = un conector independiente, sin modificar el núcleo.

## Contrato

Métodos: `identify` · `discover` · `describe` · `access_info` · `cite`

Ver `base.py`, `models.py` y `docs/07_connectors_framework.md`.

## Conectores MVP (operativos)

| Carpeta | Fuente | Estado |
|---------|--------|--------|
| ideam | IDEAM | MVP |
| invemar | INVEMAR | MVP (Fase 2) |
| gbif | GBIF | MVP |
| fao | FAOSTAT | MVP |
| worldpop | WorldPop | MVP |
| gee | Google Earth Engine | MVP |
| sgc | SGC | MVP (enriquecimiento) |
| dynamicworld | Dynamic World | MVP (enriquecimiento) |
| nasa | NASA | MVP (enriquecimiento) |
| mapbiomas | MapBiomas | MVP (enriquecimiento) |
| unosat | UNOSAT | MVP (enriquecimiento) |
| igac | IGAC | MVP (enriquecimiento) |
| upra | UPRA | MVP (enriquecimiento) |
| dane | DANE | MVP (enriquecimiento) |
| dnp | DNP | MVP (enriquecimiento) |
| contraloria | Contraloría | MVP (enriquecimiento) |
| superservicios | Superservicios | MVP (enriquecimiento) |
| mintransporte | MinTransporte | MVP (enriquecimiento) |
| upit | UPIT | MVP (enriquecimiento) |
| invias | INVIAS | MVP (enriquecimiento) |
| ansv | ANSV | MVP (enriquecimiento) |
| ani | ANI | MVP (enriquecimiento) |
| supertransporte | Supertransporte | MVP (enriquecimiento) |

Registro: `connectors/registry.py` → `build_mvp_connectors()`.

## Otros conectores

Permanecen en skeleton (`NotImplementedConnector`) hasta fases posteriores.

## Estructura

```text
connectors/<fuente>/
├── README.md
├── __init__.py
├── connector.py
└── manifest.yaml
```
