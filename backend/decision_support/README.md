# backend/decision_support

**Decision Support Engine — Fase 8 MVP**

Consulta orientada a problemas → **rutas de acción** (qué hacer, dónde, fuente, recursos, por qué).

## Principios

- Sin IA / embeddings / LLMs
- Construye sobre Recommendation + Discovery + KG
- Solo fuentes MVP (no inventa CHIRPS u otras)
- Toda ruta incluye justificación (`why`)
- El sistema orienta; la curaduría humana decide

## Flujo

```text
Consulta
  → Intención (descargar | analizar | …)
  → Conceptos normalizados (agua→hidrología, lluvia→precipitación, …)
  → Necesidad
  → Rutas de acción (perfiles curados o ranking)
  → Fuente + recursos + dónde + por qué
```

## Uso

```python
from backend.discovery import DiscoveryEngine
from backend.metadata import MetadataEngine
from backend.knowledge_graph import KnowledgeGraphEngine
from backend.recommendation import RecommendationEngine
from backend.decision_support import DecisionSupportEngine

d = DiscoveryEngine()
m = MetadataEngine(d)
kg = KnowledgeGraphEngine(d, m)
rec = RecommendationEngine(kg, d, m)
dss = DecisionSupportEngine(rec, d, m, kg)

dss.advise("Necesito analizar inundaciones en una microcuenca")
dss.advise("Quiero datos de precipitación")
```

## API

```http
GET /decision-support/info
GET /decision-support?q=Necesito+analizar+inundaciones
```
