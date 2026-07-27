# Actualización de Fuentes — DB2S-GEO

## Principio de Curaduría Humana

Ninguna modificación del catálogo oficial es automática. Toda fuente nueva, cambio de metadatos o ajuste de dominios requiere revisión y commit humano. El sistema puede detectar cambios (Watcher) y proponer candidatos (Source Discovery), pero **nunca los aplica sin aprobación**.

---

## Ciclo estándar (1 fuente nueva)

### 1. Investigar

Verificar que la fuente existe, su URL es real y tiene datos accesibles:

- ¿Es una fuente oficial, institucional o científica?
- ¿Qué recursos ofrece? (datasets, APIs, portales, geoservicios)
- ¿Qué dominios temáticos cubre?
- ¿Cómo se accede? (descarga, WMS, WFS, REST, portal)
- ¿Cómo se cita? (APA, DOI, institución, año)

### 2. Crear conector Python

```
connectors/<id>/
├── __init__.py
├── connector.py       ← metadatos curados, _RESOURCES dict
└── manifest.yaml      ← connector_id, status, domains, protocols
```

Copiar el patrón de `connectors/invemar/` o `connectors/dimar/`. El conector debe implementar `BaseConnector` (no `NotImplementedConnector`).

**Reglas de keywords:**
- SOLO términos **específicos y diferenciadores** del recurso
- NUNCA genéricos: `cambio`, `monitoreo`, `colombia`, `datos`, `sistema`, `portal`
- Los sinónimos y expansiones van en `backend/recommendation/scoring.py` → `CURATED_ALIASES`
- Los términos a filtrar del scoring van en `GENERIC_KEYWORDS`

### 3. Crear catálogo JSON

```
catalog/sources/<id>.json
```

Mismos metadatos que el conector, más:
- `endpoints[]` — al menos 1 por recurso con `method`, `url`, `label`
- `access_methods[]` — métodos de acceso normalizados
- `formats[]` — formatos de descarga si aplican
- `coverage.spatial`, `coverage.temporal`

**Regla de prefijos:** `resource.id` debe comenzar con `source.id:`  
Ejemplo: fuente `dimar` → recursos `dimar:sigdimar`, `dimar:batimetria`

### 4. Registrar

En `connectors/registry.py`:
- Agregar import del nuevo conector
- Agregar instancia en `build_python_mvp_connectors()`
- Agregar ID en `MVP_CONNECTOR_IDS`

### 5. Asignar dominios

**Regla:** `source.domains = union(todos los resource.domains)`

Excepciones documentadas:
- Dominios misionales (ej: `geologia` para SGC, `cartografia_base` para IGAC)
- Justificar en el commit message

Si el dominio no existe, agregarlo en `backend/metadata/domains.py` → `INITIAL_DOMAINS`.

### 6. Validar

```bash
# Validación estructural
python scripts/validate_catalog.py
# → Debe mostrar: invalid=0, incomplete=0

# Completitud (endpoints, duplicados, URLs)
python scripts/completitud_catalogo.py
# → Debe mostrar: 0 duplicados, 0 URLs inválidas

# Tests
python -m pytest tests/unit/ -q
# → Actualizar conteos en tests si es necesario

# Cobertura de dominios
python scripts/auditar_dominios.py
```

### 7. Commit

```bash
git add -A
git commit -m "nueva fuente: <Nombre> (<dominios>)"
git push origin main
```

Si el CI/CD está activo, GitHub Actions validará y desplegará automático.

---

## Modificar una fuente existente

Mismo flujo, pero cambiando el archivo existente en lugar de crear uno nuevo:

1. Editar `catalog/sources/<id>.json` y/o `connectors/<id>/connector.py`
2. Si se agregan/quitan dominios: verificar unión resource.domains
3. Si se agregan/quitan keywords: verificar regla de especificidad
4. Validar → commit → push

---

## Scripts de apoyo

| Script | Función |
|--------|---------|
| `scripts/validate_catalog.py` | Validar JSON, prefijos, status, recursos vacíos |
| `scripts/completitud_catalogo.py` | Endpoints, duplicados de IDs, URLs inválidas |
| `scripts/auditar_dominios.py` | Cobertura de dominios, fuentes sin dominio, gaps |
| `scripts/corregir_dominios.py` | Auto-corregir source.domains = union(resource.domains) |
| `scripts/corregir_keywords.py` | Limpiar keywords genéricos de recursos |

---

## Lo que NUNCA se debe hacer

- ❌ Modificar el catálogo directamente en Cloud Run o en producción
- ❌ Agregar keywords genéricos (`cambio`, `monitoreo`, `colombia`, `datos`)
- ❌ Crear fuente sin su JSON catalog (el Python connector es solo fallback)
- ❌ Saltarse `validate_catalog.py` antes del commit
- ❌ Modificar dominios de fuente sin verificar la unión con recursos
- ❌ Usar prefijos de recurso que no coincidan con el ID de la fuente
- ❌ Dejar recursos sin `endpoints[]`
- ❌ Committear `data/`, `.env`, `_archived_temp/` o backups

---

## Referencias

- [Principio de Curaduría Humana](archive/DB2S_GEO_Registro_Diseno.md) — §20.15
- [Principio de Atribución y Trazabilidad](archive/DB2S_GEO_Registro_Diseno.md) — §20.16
- [Dominios temáticos](04_data_domains.md)
- [Framework de conectores](07_connectors_framework.md)
- [Sistema de puntuación](08_scoring_system.md)
- [ENRICHMENT_INDEX.md](../docs/ENRICHMENT_INDEX.md)
- [UPDATING_PLAN.md](../docs/UPDATING_PLAN.md)
