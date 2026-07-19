# RELEASE CHECKLIST — DB2S-GEO 0.1.0-preview

Versión congelada: **`0.1.0-preview`**  
Fecha: 2026-07-19

---

## Bloqueantes

- [x] Congelar catálogo (23 fuentes / 71 recursos / 0 pendientes)
- [x] Documentar release (`RELEASE_NOTES_PREVIEW_0_1.md`)
- [x] Auditoría deploy (`DEPLOY_AUDIT.md`)
- [x] `GET /health` y `GET /version` operativos
- [x] `GET /healthz` para sonda Cloud Run
- [x] Dockerfile raíz listo (PORT 8080)
- [x] Telemetría query + timestamp + result_count
- [x] Telemetría clics de recurso
- [x] UX home como asistente (Decision Support, sin LLM)
- [x] Texto de primera pantalla: problema territorial / ambiental / geoespacial
- [x] Tests unitarios verdes (98)
- [ ] Deploy Cloud Run con IAM (ops — no automatizado en repo)
- [ ] Invitar colegas (`roles/run.invoker`)

---

## Necesarios

- [x] Schema Supabase mínimo (`supabase/supabase_schema.sql`)
- [x] Guía Cloud Run (`deployment/cloudrun/README.md`)
- [x] `.env.example` preview
- [x] Checklist y notes de congelamiento
- [ ] Aplicar SQL en proyecto Supabase (ops)
- [ ] Comunicar limitaciones de ranking («colombia») a colegas

---

## Deseables

- [ ] Cablear API → Supabase (hoy SQLite local)
- [ ] Volumen persistente / export telemetría
- [ ] Fix ranking keyword genérica
- [ ] Ampliar taxonomía de dominios
- [ ] GitHub Actions → Cloud Run
- [ ] Banner visible «Private Preview» en topbar
- [ ] Rate limiting Cloud Armor

---

## Decisión

**PUBLICAR PREVIEW PRIVADA** tras completar casillas ops de IAM.
