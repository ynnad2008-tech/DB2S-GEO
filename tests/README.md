# Tests — DB2S-GEO

## Fase 1 — Discovery Engine MVP

```bash
# desde la raíz del repo
pip install -r backend/requirements.txt
pytest tests/unit -q
```

Cobertura prioritaria:
1. Contratos de conectores MVP
2. Discovery Engine (list/search/get/access)
3. Citation Engine (atribución)
4. API `GET /sources*`
