# DB2S-GEO — contenedor Alpha (local / Hugging Face Spaces)

FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=8000

COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

COPY . /app

EXPOSE 8000

# HF Spaces inyecta PORT (p. ej. 7860). Local usa 8000 por defecto.
CMD ["sh", "-c", "uvicorn backend.api.main:app --host 0.0.0.0 --port ${PORT:-8000} --app-dir ."]
