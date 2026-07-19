# 03 — Knowledge Graph

## Propósito

Definir el modelo conceptual del grafo de conocimiento geográfico de DB2S-GEO.

## Alcance

Entidades, relaciones y ejemplos conceptuales. Sin persistencia ni inferencia operativa.

## Objetivos

1. Representar el conocimiento territorial de forma estructurada.
2. Habilitar descubrimiento, comparación y recomendación.
3. Servir de base para agentes IA y citation.

## Entidades

| Entidad | Descripción conceptual |
|---------|------------------------|
| Institución | Organización productora o custodial |
| Fuente | Plataforma o sistema de datos |
| Dataset | Conjunto de datos identificable |
| Variable | Medida o atributo temático |
| Servicio | Endpoint o servicio de acceso (OGC, REST, etc.) |
| API | Interfaz programática |
| Caso de Uso | Problema territorial aplicable |
| Referencia | Citación / DOI / documentación |
| País | Ámbito nacional |
| Tema | Dominio temático |
| Índice bibliográfico | Fuente de literatura científica (p. ej. Scopus, WoS, Scholar) |

## Cadena relacional canónica

```text
Institución
    ↓
Fuente
    ↓
Dataset
    ↓
Variable
    ↓
Servicio
    ↓
API
    ↓
Método de acceso
    ↓
Referencia
    ↓
Caso de uso
```

## Relaciones adicionales previstas

```text
País ──────► Institución
Tema ──────► Dataset
Dataset ───► Variable
Fuente ────► Servicio
Caso de Uso ► Dataset (recomendado)
Referencia ◄─ Índice bibliográfico (descubierta / indexada en)
Portal datos abiertos ──► Fuente / Dataset
```

## Ejemplo conceptual — precipitación

```text
Precipitación (Variable / Tema)
    → IDEAM (Institución / Fuente nacional)
    → CHIRPS (Fuente global)
    → GPM (Fuente global)
    → ERA5 (Fuente global)
    → WorldClim (Fuente global)
    → CGIAR Aridity Index (contexto de aridez / clima)
```

## Ejemplo conceptual — conservación en Colombia

```text
Áreas protegidas (Tema: Conservación) · País: Colombia
    → Parques Nacionales (Institución)
    → RUNAP (Fuente / registro nacional)
    → Protected Planet (Fuente global complementaria)
```

## Ejemplo conceptual — tierras y ruralidad

```text
Ordenamiento / tenencia rural (Tema: Tierras) · País: Colombia
    → UPRA / SIPRA (planificación agropecuaria)
    → ANT (tierras)
    → URT (restitución)
    → datos.gov.co (portal de descubrimiento de datasets abiertos)
```

## Ejemplo conceptual — bosques y cobertura

```text
Bosque / cobertura forestal
    → Global Forest Watch (monitoreo global)
    → MapBiomas / WorldCover / Dynamic World (coberturas)
    → SoilGrids / OpenLandMap (contexto edáfico)
```

## Ejemplo conceptual — citación científica

```text
Dataset / Variable
    → Referencia (APA · BibTeX · DOI)
    → Índice bibliográfico
         → Google Scholar
         → Scopus
         → Web of Science
```

## Ejemplo de pregunta geográfica

```text
Necesito modelar hábitat de aves.
Fuentes sugeridas (conceptuales):
  GBIF · eBird · SiB Colombia · WorldCover · Sentinel-2 · CHELSA
```

## Nodos institucionales Colombia (ampliación 2026)

```text
Colombia
  ├── Conservación: Parques Nacionales · RUNAP
  ├── Rural / tierras: UPRA · SIPRA · ANT · URT
  ├── Social / víctimas: SNARIV · UARIV · SISBÉN · UBPD
  └── Datos abiertos: datos.gov.co
```

## Estructura en repositorio

```text
knowledge_graph/
├── models/          # Modelos conceptuales
├── schemas/         # Esquemas / contratos futuros
└── examples/        # Ejemplos ilustrativos
```

## Secciones reservadas (futuro)

- [ ] Ontología formal (OWL / RDF / property graph)
- [ ] Reglas de inferencia
- [ ] Almacenamiento (Neo4j / RDF store / tablas grafo)
- [ ] Pipeline de ingesta al grafo
- [ ] Modelado de sensibilidad ética (víctimas / datos personales)

---

*Modelo conceptual únicamente.*
