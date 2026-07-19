# Alpha Deployment — DB2S-GEO v0.9

Guía para publicar y validar DB2S-GEO en entorno Alpha: demostraciones, pruebas en internet, validación móvil y despliegue (local, Docker, Hugging Face Spaces).

**Versión:** `0.9.0-alpha` · **Etiqueta:** `DB2S-GEO v0.9 Alpha`  
**Autor:** Dany Arbey Benavides

---

## 1. Requisitos

| Requisito | Notas |
|-----------|--------|
| Python 3.11+ (recomendado 3.12 / 3.13) | Probado en desarrollo local |
| pip | Instalación de dependencias |
| Puerto libre | Local `8000`; Hugging Face Spaces suele usar `7860` |
| Navegador moderno | Workbench HTML/CSS/JS vanilla (sin frameworks) |
| Docker (opcional) | Despliegue contenedorizado / Spaces Docker |

**No requiere:** base de datos externa, GPU, claves de LLM, Redis, autenticación de usuarios.

---

## 2. Dependencias

```bash
pip install -r backend/requirements.txt
```

Paquetes principales: FastAPI, Uvicorn, httpx, pytest.

Código incluido en el repositorio: motores Discovery, Metadata, Knowledge Graph, Recommendation, Watcher, Source Discovery, Decision Support, Observatorio y Curator Workbench.

---

## 3. Variables de entorno

| Variable | Default | Uso |
|----------|---------|-----|
| `HOST` | `0.0.0.0` | Bind (Docker / Spaces). Local puede usar `127.0.0.1` |
| `PORT` | `8000` | Puerto HTTP. HF inyecta `PORT` (p. ej. `7860`) |
| `ENVIRONMENT` | `alpha` | Etiqueta de entorno (opcional) |

No hay secretos obligatorios en Alpha.  
El Observatorio **no** almacena IP ni PII.

Datos locales opcionales (gitignore):

- `data/watcher/`
- `data/source_discovery/`
- `data/observatory/queries.json`

En Spaces/Docker sin volumen, esos datos son **efímeros**.

---

## 4. Rutas clave

| Ruta | Descripción |
|------|-------------|
| `/workbench/` | Interfaz pública (Workbench) |
| `/docs` | OpenAPI |
| `/` | Info de versión y endpoints |
| `/health` | Salud de motores |

---

## 5. Despliegue local

Desde la **raíz del repositorio**:

```bash
pip install -r backend/requirements.txt
uvicorn backend.api.main:app --host 127.0.0.1 --port 8000 --app-dir .
```

Verificación:

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/health
# Abrir http://127.0.0.1:8000/workbench/
```

Tests:

```bash
python -m pytest tests/unit -q
```

En la misma red (prueba desde celular en LAN):

```bash
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --app-dir .
# Abrir http://<IP-local>:8000/workbench/
```

---

## 6. Despliegue con Docker

```bash
docker build -t db2s-geo:0.9-alpha .
docker run --rm -p 8000:8000 db2s-geo:0.9-alpha
```

Workbench: http://localhost:8000/workbench/

Puerto personalizado (p. ej. compatible con Spaces):

```bash
docker run --rm -e PORT=7860 -p 7860:7860 db2s-geo:0.9-alpha
```

El `Dockerfile` en la raíz escucha en `0.0.0.0:${PORT:-8000}`.

---

## 7. Despliegue en Hugging Face Spaces

1. Crear un Space tipo **Docker**.
2. Conectar este repositorio (o subir el código con el `Dockerfile` en la raíz).
3. El contenedor debe escuchar en `0.0.0.0:$PORT` (HF inyecta `PORT`, suele ser `7860`).
4. Tras el build, abrir: `https://<usuario>-<space>.hf.space/workbench/`.

Notas:

- Persistencia de Observatorio/Watcher es efímera salvo volumen/bucket.
- Catálogo Alpha es de lectura; no hay autenticación de usuarios.
- Ver también `deployment/huggingface/README.md`.

---

## 8. Validación responsive (Alpha)

Probar el Workbench en anchos:

| Ancho | Dispositivo tipico |
|-------|--------------------|
| 320 px | Teléfonos muy estrechos |
| 360 px | Android compacto |
| 390 px | iPhone estándar |
| 412 px | Android amplio |
| 768 px | Tablet |

Revisar en cada ancho:

- [ ] Menú principal (hamburguesa ≤768 px; cierra al navegar / Escape)
- [ ] Hero: **DB2S-GEO**, subtítulo, **¡Validada por humanos!**
- [ ] Buscador y botones (sin salir de pantalla)
- [ ] Nube de tendencias (sin scroll horizontal)
- [ ] Recomendaciones, Observatorio, Administración
- [ ] Tablas: scroll interno, no romper layout
- [ ] Footer institucional (3 bloques)

Corregir si aparecen: desbordamientos, scroll horizontal, textos cortados, botones fuera de vista, tablas ilegibles.

---

## 9. Checklist previo a publicación

### Identidad

- [ ] Título / marca: **DB2S-GEO**
- [ ] Subtítulo: **Plataforma de conocimiento geoespacial**
- [ ] Sello solo en Inicio: **¡Validada por humanos!**

### Navegación

- [ ] Inicio · Explorar · Recomendaciones · Monitoreo · Observatorio · Administración
- [ ] Contador: **Administración (N)** cuando hay candidatos
- [ ] Menú responsive en móvil

### Footer institucional

- [ ] Izquierda: `© DB2S-GEO · 2026` · Proyecto concebido y desarrollado por · **Dany Arbey Benavides**
- [ ] Centro: Cómo citar esta plataforma · Apoya el desarrollo de DB2S-GEO
- [ ] Derecha: **API** → `/docs`
- [ ] Línea de versión: `DB2S-GEO v0.9 Alpha`

### Funcionalidad

- [ ] `GET /` → `version` `0.9.0-alpha` / release Alpha
- [ ] Observatorio funcional + aviso de anonimato
- [ ] Nube dinámica de tendencias (Inicio + Observatorio)
- [ ] Recomendación / Decision Support responden
- [ ] `/docs` accesible
- [ ] README + este archivo en el repositorio

### Prueba real

- [ ] Abrir URL pública o LAN desde celular
- [ ] Navegar todos los paneles principales
- [ ] Confirmar ausencia de scroll horizontal

---

## 10. Fuera de alcance Alpha

- Nuevas fases / motores / dominios / módulos de IA
- Autenticación de usuarios
- LLM / embeddings
- Rate limiting avanzado (reservado)
- Dominio propio (migración futura)

---

© DB2S-GEO · 2026 · Dany Arbey Benavides
