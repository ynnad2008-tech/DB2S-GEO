# backend/citation

**Citation Engine — Fase 1 MVP**

Integrado con Discovery Engine. Retorna atribución según
`docs/21_attribution_and_citation_policy.md`:

- fuente
- institución
- referencia
- URL
- fecha de consulta (`accessed`)
- APA (cuando exista)
- DOI (cuando exista)

```python
from backend.discovery import DiscoveryEngine
from backend.citation import CitationEngine

discovery = DiscoveryEngine()
citation = CitationEngine(discovery)
citation.cite_source("gbif", resource_id="gbif:occurrence")
```
