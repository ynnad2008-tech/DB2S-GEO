# backend/discovery

**Discovery Engine — Fase 1 MVP**

Responsabilidades:
- Registrar conectores MVP (curaduría humana explícita)
- Listar fuentes disponibles
- Buscar fuentes por texto / dominio
- Obtener información normalizada de una fuente
- Exponer `access_info` (read-only, sin descargas)

Sin OpenSearch ni indexación distribuida.

```python
from backend.discovery import DiscoveryEngine

engine = DiscoveryEngine()
engine.list_sources()
engine.search(query="clima")
engine.get_source("ideam")
```
