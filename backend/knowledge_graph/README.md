# backend/knowledge_graph

**Knowledge Graph — Fase 3 MVP**

Grafo en memoria (Python puro) construido **sobre** Discovery Engine y
Metadata Engine. Almacena relaciones, no metadatos completos.

## Nodos

Institution · Source · Resource · Domain · Keyword

## Relaciones

```text
Institution -publishes-> Source
Source -contains-> Resource
Resource -belongs_to-> Domain
Resource -associated_with-> Keyword
```

## Uso

```python
from backend.discovery import DiscoveryEngine
from backend.metadata import MetadataEngine
from backend.knowledge_graph import KnowledgeGraphEngine

discovery = DiscoveryEngine()
metadata = MetadataEngine(discovery)
kg = KnowledgeGraphEngine(discovery, metadata)

kg.stats()
kg.resources_by_domain("clima")
kg.resources_by_source("ideam")
kg.domains_of_source("gbif")
kg.institutions_by_domain("biodiversidad")
```

## No incluye

Neo4j · RDF · OWL · SPARQL · GraphQL · Recommendation · IA

## Ejemplos documentados

Ver `examples.md`.
