# DEPLOY AUDIT — DB2S-GEO 0.1.0-preview

Auditoría sobre el repositorio real (2026-07-19). Sin rutas inventadas.

---

## Hallazgo estructural (CRÍTICO — documentación)

| Supuesto externo | Realidad en repo |
|------------------|------------------|
| Frontend React | **No hay** `package.json`, ni `src/` React, ni Vite/Next. UI = `frontend/workbench/` (HTML/CSS/JS vanilla) servida por FastAPI |
| GitHub Actions | **No hay** `.github/workflows/` |
| Supabase conectado | **No** hay cliente Supabase en código; schema preparado en `supabase/supabase_schema.sql` |
| BD producto activa | Observatory = JSON (`data/observatory/`); telemetría preview = SQLite local; `backend/database/base.py` = placeholder |

---

## Inventario verificado

| Componente | Ruta real | Estado |
|------------|-----------|--------|
| API | `backend/api/main.py` | Operativo |
| Requirements | `backend/requirements.txt` | fastapi, uvicorn, httpx, pytest |
| Workbench | `frontend/workbench/index.html` | Operativo |
| Docker | `Dockerfile` (raíz) | Operativo Cloud Run |
| Compose | `deployment/compose/docker-compose.yml` | Vacío (`services: {}`) |
| Env example | `deployment/env/.env.example` | Existe |
| Cloud Run guide | `deployment/cloudrun/README.md` | Existe |
| Health | `GET /health`, `GET /healthz` | Existen |
| Version | `GET /version` | Existe |
| Startup | `uvicorn backend.api.main:app --app-dir .` | Documentado en README |

---

## Clasificación

### CRÍTICO

| ID | Hallazgo | Acción |
|----|----------|--------|
| C1 | No existe frontend React / build step | Desplegar **solo** el contenedor FastAPI+Workbench; no usar Vercel para UI |
| C2 | Preview sin IAM → URL pública indexable | Cloud Run con `--no-allow-unauthenticated` + `roles/run.invoker` |
| C3 | Telemetría en `/tmp` en Cloud Run es efímera | Aceptable preview corta; migrar a Supabase cuando haya proyecto |

### ALTO

| ID | Hallazgo | Acción |
|----|----------|--------|
| A1 | Ranking keyword `colombia` | Comunicar a colegas; no bloquea preview privada |
| A2 | Taxonomía 8 dominios (catastro/transporte/geología → `observacion_tierra`) | Post-preview |
| A3 | Sin GitHub Actions | Deploy manual `gcloud` esta semana |

### MEDIO

| ID | Hallazgo | Acción |
|----|----------|--------|
| M1 | `/health` carga todos los motores (pesado) | Usar `/healthz` como sonda Cloud Run |
| M2 | Compose placeholder | Ignorar; usar Dockerfile raíz |
| M3 | Supabase schema listo pero no cableado | Aplicar SQL en dashboard Supabase; cablear en iteración post-deploy |

### BAJO

| ID | Hallazgo | Acción |
|----|----------|--------|
| B1 | `deployment/docker/README.md` era placeholder | Actualizado a apuntar Dockerfile raíz |
| B2 | Versioning histórico `0.9.x` → `0.1.0-preview` | Congelamiento explícito en release notes |

---

## Variables de entorno (preview)

| Variable | Uso | Obligatorio |
|----------|-----|-------------|
| `PORT` | Cloud Run inyecta | Sí (plataforma) |
| `ENVIRONMENT` | `preview` / `private-preview` | No |
| `TELEMETRY_DB_PATH` | SQLite local | No (default `data/telemetry/queries.db`) |
| `SUPABASE_URL` | Futuro | No en 0.1.0-preview runtime |
| `SUPABASE_SERVICE_KEY` | Futuro | No en 0.1.0-preview runtime |

---

## Opción de despliegue elegida

Ver sección TAREA 7 en respuesta / `RELEASE_CHECKLIST.md`: **C. Cloud Run completo**.
