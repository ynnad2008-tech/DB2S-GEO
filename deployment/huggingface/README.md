# Hugging Face Spaces — DB2S-GEO Alpha

SDK: **Docker** · App file: `Dockerfile` (raíz del repositorio)

## Pasos

1. Crear un Space → **Docker**.
2. Conectar el repositorio o subir el código.
3. HF inyecta `PORT` (típicamente `7860`); el `Dockerfile` ya usa `${PORT:-8000}`.
4. Tras el build: `https://<usuario>-<space>.hf.space/workbench/`

## Comprobaciones rápidas

- `/` → versión `0.9.0-alpha`
- `/health` → motores OK
- `/workbench/` → interfaz
- `/docs` → API

Ver guía completa: [`ALPHA_DEPLOYMENT.md`](../../ALPHA_DEPLOYMENT.md).
