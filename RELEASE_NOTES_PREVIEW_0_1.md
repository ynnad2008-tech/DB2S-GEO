# RELEASE NOTES — Preview 0.1.0

**Producto:** DB2S-GEO  
**Versión:** `0.1.0-preview`  
**Etiqueta:** DB2S-GEO v0.1.0 Preview  
**Fecha de congelamiento:** 2026-07-19  
**Autor:** Dany Arbey Benavides  
**Estado:** Preview privada (colegas) — **no** beta pública

---

## Congelamiento

| Ítem | Valor congelado |
|------|-----------------|
| Fuentes MVP | **23** |
| Recursos (Resource nodes) | **71** |
| Iteraciones de enriquecimiento | **29** |
| Pendientes en `docs/ENRICHMENT_INDEX.md` | **0** |
| FASE 18 | **No iniciada** (prohibida en este release) |
| Nuevas fuentes / recursos | **Bloqueadas** |
| Tests unitarios | **98 passed** (suite `tests/unit`) |
| Auditoría pre-beta (ajustado) | **76/100** |
| Auditoría pre-beta (bruto) | **91/100** |

Catálogo y conectores MVP quedan **read-only** respecto a enriquecimiento: no se agregan `source_id` ni `resource_id` en esta rama de preview.

---

## Qué incluye 0.1.0-preview

- API FastAPI (Discovery → Metadata → KG → Recommend → Decision Support → Observatory → Watcher → Source Discovery)
- Workbench HTML/CSS/JS en `/workbench/` (no hay app React en el repositorio)
- Telemetría mínima: consultas (`query`, `timestamp`, `result_count`) + clics de recurso
- Schema SQL mínimo para Supabase (`supabase/supabase_schema.sql`)
- Contenedor Docker listo para Cloud Run
- Endpoints `/health`, `/healthz`, `/version`

---

## Qué no incluye

- Beta pública / acceso anónimo abierto sin IAM
- Corrección del ranking por keyword genérica `colombia` (conocido; documentado)
- Ampliación de taxonomía de dominios (conocido; post-preview)
- Frontend React / build Vite/Next
- Auth de aplicación (usuarios/roles propios)

---

## Cómo citar esta preview

```text
Benavides, D. A. (2026). DB2S-GEO: Plataforma de conocimiento geoespacial
(versión 0.1.0-preview) [plataforma de software]. Consultado el [fecha].
```

---

## Decisión de release

**PUBLICAR PREVIEW PRIVADA** con colegas (Cloud Run + IAM).  
No publicar beta pública hasta mitigar ranking y taxonomía.
