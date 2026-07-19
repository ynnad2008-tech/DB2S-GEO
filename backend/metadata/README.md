# backend/metadata

**Metadata Engine — Fase 2 MVP**

Normaliza metadatos de recursos descubiertos por Discovery Engine.

## Capacidades

- Listar recursos por fuente
- Describir recursos con estructura común
- Clasificar dominios temáticos
- Asociar palabras clave curadas
- Marcar campos no disponibles (`unavailable_fields`)
- Preparar puente hacia Knowledge Graph

## Uso

```python
from backend.discovery import DiscoveryEngine
from backend.metadata import MetadataEngine

discovery = DiscoveryEngine()
metadata = MetadataEngine(discovery)
metadata.list_resources("ideam")
metadata.get_resource("ideam", "ideam:precipitacion")
metadata.list_domains()
```

## Principios

- No inventa información
- Consume Discovery sin reemplazarlo
- Curaduría humana · Read-only
