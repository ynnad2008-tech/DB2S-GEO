# 07 — Connector Framework

## Propósito

Definir la arquitectura de conectores independientes para integrar fuentes sin acoplar el núcleo.

## Alcance

Interfaces, contratos, plantillas y documentación. Sin lógica de acceso real.

## Objetivos

1. Estandarizar el ciclo de vida de un conector.
2. Permitir incorporación de fuentes sin modificar el core.
3. Separar contratos de implementaciones futuras.

## Principio

Cada fuente se implementa como conector independiente.

## Arquitectura

```text
Connector Framework
├── interfaces / contratos
├── plantilla (templates/)
├── conectores por fuente
└── registro / descubrimiento de conectores (futuro)
         │
         ▼
    Núcleo DB2S-GEO
    (Discovery · Metadata · KG · Citation)
```

## Contrato conceptual (mínimo)

Todo conector deberá exponer (en fases futuras):

| Método conceptual | Descripción |
|-------------------|-------------|
| `identify` | Metadatos de la fuente |
| `discover` | Listar / buscar recursos |
| `describe` | Describir un recurso |
| `access_info` | Cómo acceder (sin descargar aún en skeleton) |
| `cite` | Información de citación |

*Firmas exactas: reservadas. Ver `connectors/templates/`.*

## Conectores previstos en skeleton

```text
connectors/
├── ideam/          # MVP
├── igac/
├── dane/
├── gbif/           # MVP
├── ebird/
├── sib_colombia/
├── fao/            # FAOSTAT MVP
├── world_bank/
├── worldpop/       # MVP
├── gee/            # MVP
├── nasa/
├── copernicus/
├── asf/
├── mapbiomas/
├── catie/
├── unosat/
└── templates/
```

## Interoperabilidad objetivo

OGC · STAC · ArcGIS REST · Socrata · CKAN · GeoNode · APIs REST

## Secciones reservadas (futuro)

- [ ] SDK de conectores
- [ ] Validación automática de contratos
- [ ] Versionado semántico de conectores
- [ ] Pruebas de conformidad

---

*Solo arquitectura y placeholders.*