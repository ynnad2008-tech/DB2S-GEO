# DB2S-GEO 0.1.0-preview — Cloud Run (opción elegida: C completo)

Un solo servicio: FastAPI + Workbench. No hay frontend React → no Vercel.

## PASO 1 — Proyecto GCP

```bash
gcloud auth login
gcloud config set project PROJECT_ID
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com
```

## PASO 2 — Build (raíz del repo)

```bash
export PROJECT_ID=tu-proyecto
export REGION=us-central1
export SERVICE=db2s-geo-preview

gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE:0.1.0-preview
```

## PASO 3 — Deploy privado

```bash
gcloud run deploy $SERVICE \
  --image gcr.io/$PROJECT_ID/$SERVICE:0.1.0-preview \
  --region $REGION \
  --platform managed \
  --no-allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 3 \
  --timeout 60 \
  --port 8080 \
  --set-env-vars "ENVIRONMENT=preview,TELEMETRY_DB_PATH=/tmp/telemetry/queries.db"
```

## PASO 4 — Invitar colega

```bash
gcloud run services add-iam-policy-binding $SERVICE \
  --region $REGION \
  --member="user:colegio@ejemplo.com" \
  --role="roles/run.invoker"
```

## PASO 5 — Verificar

```bash
SERVICE_URL=$(gcloud run services describe $SERVICE --region $REGION --format='value(status.url)')
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" "$SERVICE_URL/healthz"
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" "$SERVICE_URL/version"
# Abrir: $SERVICE_URL/workbench/
```

## PASO 6 — Supabase (opcional misma semana)

1. Crear proyecto Supabase.
2. SQL Editor → pegar `supabase/supabase_schema.sql` → Run.
3. Guardar URL/keys fuera del repo; cablear API en iteración posterior (no bloquea preview).

## PASO 7 — Mensaje a colegas

- URL: `…/workbench/`
- Texto: Preview privada 0.1.0 — no beta pública.
- Limitación conocida: evitar consultas con solo la palabra «Colombia».
