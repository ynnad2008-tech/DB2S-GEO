# 22 — Esquema de funcionamiento (v0.8.0)

Documento de referencia del estado congelado de la plataforma.
Si algo no está aquí, no es parte del núcleo.

---

## 1. Componentes

```
┌──────────────────────────────────────────────────────────────┐
│ WORKBENCH (HTML/JS) — 6 paneles funcionales                   │
│  Inicio (asistente + chat) · Explorar · Recomendaciones       │
│  Monitoreo · Observatorio · Administración (Auto Curator)     │
└──────────────────────────┬───────────────────────────────────┘
                           │ REST (FastAPI, 52 endpoints)
┌──────────────────────────▼───────────────────────────────────┐
│ API (backend/api/main.py)                                     │
│  /sources · /recommend · /decision-support · /chat            │
│  /graph · /watcher · /observatory · /source-discovery         │
└────┬───────────┬──────────────┬──────────────┬────────────┬───┘
     │           │              │              │            │
 CATÁLOGO     MOTORES         GEMINI      OBSERVATORIO  TELEMETRÍA
 (JSON, 122)  deterministas   (opcional)   (anónimo)     (anónima)
```

### Catálogo (la base de datos)
- `catalog/sources/*.json` — 122 fichas activas (Colombia, regional, globales).
- Solo `status=active` entra en runtime. Carga al arranque (reiniciar tras cambios).
- Cada recurso documenta: portal Y geoservicio cuando está verificado
  (política: solo URLs con respuesta HTTP real; nunca conjeturas).

### Motores deterministas (la lógica — sin IA, explicable)
1. **Discovery**: lista/busca fuentes (filtros `q`, `domain`, `coverage`).
2. **Knowledge Graph**: nodos Institución→Fuente→Recurso→Dominio/Keyword
   (~1200 nodos). Solo relaciones de 1 salto, sin recursión.
3. **Recommendation**: scoring fijo y trazable — keyword 25/15/10/5
   (decreciente), dominio 45, fuente 20, recurso 20, bonus oficial
   nacional 15. Empates se deshacen por evidencia (recursos→keywords→
   dominios→orden estable).
4. **Decision Support**: interpretación → perfiles curados (inundación
   marítima/fluvial, precipitación, biodiversidad, erosión) o recomendación
   → rutas (qué / dónde / fuente / recursos / por qué) → narración.
5. **Coverage**: coberturas curadas (Colombia 32 dptos + ciudades +
   regiones; Honduras, Costa Rica, México, Perú). Detección automática
   desde la consulta ("en el Tolima"). Los globales cubren todo
   (`include_global`).
6. **Watcher / Source Discovery / Auto Curator**: monitoreo de cambios;
   candidatos; crecimiento asistido (Gemini propone → verificación HTTP
   obligatoria → activa con `curation: llm-verified`).

### Gemini (opcional, 3 roles, siempre con fallback determinista)
- **Intérprete**: consulta → intents/conceptos/need.
- **Narrador**: resumen en lenguaje natural + preguntas de seguimiento.
- **Curador**: propuestas de fuentes/keywords (Auto Curator).
- Circuit breaker: tras 429/503 entra en cooldown (60 s) y todo sigue
  determinista. En producción la key es opcional (variable del servicio).

---

## 2. Flujo de una consulta

```
consulta
  → (si hay historial) /chat: hereda cobertura del hilo + resuelve anáforas
  → interpretación (Gemini → fallback determinista)
  → cobertura detectada
  → perfil de necesidad (disparo directo o ≥2 conceptos; algunos requieren
    disparo directo) — si no, recomendación
  → rutas filtradas por cobertura (y completadas con recomendación si
    quedan cortas)
  → narración (Gemini → plantilla)
  → respuesta: need · rutas con why (aristas reales del grafo) ·
    coverage · narrative · interpretation
```

---

## 3. Flujo de curaduría (alta de fuentes)

```
candidato (CSV / JSON validado por el curador / propuesta Gemini)
  → verificación HTTP (portal + geoservicio con su protocolo)
  → ficha draft → scripts/validate_catalog.py → scripts/activate_sources.py
  → suite 146 tests → commit → push
```

---

## 4. Despliegue continuo

```
push a main
  → GitHub Actions: validate-catalog → unit-tests (146)
  → deploy: autentica con GCP_SA_KEY → Cloud Build (imagen) →
    Cloud Run (servicio db2s-geo, us-central1, min 0 / max 1)
  → smoke tests (health, version, sources dinámico, workbench)
  → URL: https://db2s-geo-546367148987.us-central1.run.app
```

- Variables de consola (p. ej. `GEMINI_API_KEY`) se conservan
  (`--update-env-vars`).
- En producción: determinista por defecto; Auto Curator apagado
  (filesystem efímero → crecimiento vía git).

---

## 5. Principios congelados

1. **Acceso directo**: cada recurso lleva al dato o al servicio, no a la
   portada. Es la misión.
2. **Explicabilidad**: toda recomendación dice por qué (aristas del grafo).
3. **Sin invención**: el LLM propone e interpreta; la máquina verifica;
   nada entra al catálogo sin respuesta HTTP real.
4. **Simplificación**: la expansión conceptual vive en los aliases
   (un solo lugar); las fichas conservan keywords específicas, no bloques
   genéricos que inflan puntuaciones.
5. **Integralidad temática**: el catálogo crece por temáticas completas,
   con el mismo criterio de verificación.

---

## 6. Alcance congelado

| Capa | Estado |
|---|---|
| Motores, API, pipeline, workbench | **Núcleo estable** — solo corrección de bugs |
| Catálogo + acceso directo por temáticas | **Activo** — crece por curaduría |
| Agente, auto-alias, más UI | **Pausado** hasta completar acceso directo |
