# Catálogo JSON-first — DB2S-GEO 0.2

```text
catalog/
├── schema/source.schema.json
├── sources/*.json          # una ficha por fuente
└── reports/latest_validation.json
```

## Estados

| status | Runtime Discovery/Rec/KG/Workbench |
|--------|-------------------------------------|
| draft | No |
| validated | No |
| active | Sí |

## Comandos

```bash
python scripts/validate_catalog.py
python scripts/activate_sources.py --id <source_id>
python scripts/activate_sources.py --all-validated
python scripts/activate_sources.py --demote <source_id> --to draft
python scripts/export_catalog_from_connectors.py   # mantenimiento / re-export
```

Runtime: `connectors.registry.build_mvp_connectors()` carga solo JSON `active`
vía `connectors.catalog_loader`.
