# DB2S-GEO — contenedor 0.2.0-preview (Cloud Run / local)

FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=8080 \
    ENVIRONMENT=preview \
    TELEMETRY_DB_PATH=/app/data/telemetry/queries.db

# Instalar dependencias via pyproject.toml (modo editable)
COPY pyproject.toml /app/
COPY backend/ /app/backend/
COPY connectors/ /app/connectors/
RUN pip install --no-cache-dir -e .

# Copiar resto de la app
COPY . /app

RUN mkdir -p /app/data/telemetry /app/data/observatory /app/data/watcher /app/data/source_discovery \
    && chmod -R 777 /app/data

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:'+__import__('os').environ.get('PORT','8080')+'/healthz')" || exit 1

CMD ["sh", "-c", "uvicorn backend.api.main:app --host 0.0.0.0 --port ${PORT:-8080} --app-dir ."]
