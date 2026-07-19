# DB2S-GEO — contenedor 0.1.0-preview (Cloud Run / local)

FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=8080 \
    ENVIRONMENT=preview \
    TELEMETRY_DB_PATH=/app/data/telemetry/queries.db

COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

COPY . /app

RUN mkdir -p /app/data/telemetry /app/data/observatory /app/data/watcher /app/data/source_discovery \
    && chmod -R 777 /app/data

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:'+__import__('os').environ.get('PORT','8080')+'/healthz')" || exit 1

CMD ["sh", "-c", "uvicorn backend.api.main:app --host 0.0.0.0 --port ${PORT:-8080} --app-dir ."]
