# backend/recommendation

**Recommendation Engine — Fase 4 MVP**

Recomendaciones **explicables** a partir del Knowledge Graph.

## Principios

- Sin IA / embeddings / LLMs
- Toda recomendación incluye `score`, `reason` y `relations_used`
- Solo fuentes MVP registradas (no inventa CHIRPS u otras)

## Uso

```python
from backend.discovery import DiscoveryEngine
from backend.metadata import MetadataEngine
from backend.knowledge_graph import KnowledgeGraphEngine
from backend.recommendation import RecommendationEngine

d = DiscoveryEngine()
m = MetadataEngine(d)
kg = KnowledgeGraphEngine(d, m)
rec = RecommendationEngine(kg, d, m)

rec.recommend("precipitacion")
rec.recommend_by_domain("clima")
rec.recommend_by_source("ideam")
rec.recommend_by_resource("ideam:precipitacion")
```

## API

```http
GET /recommend?q=precipitacion
GET /recommend/domain/clima
GET /recommend/source/ideam
GET /recommend/resource/ideam:precipitacion
```
