# 17 — MVP Conceptual

## Propósito

Acotar el Producto Mínimo Viable de DB2S-GEO.

## Alcance

Definición conceptual del MVP. La implementación mínima del Discovery Engine
está en Fase 1 (`backend/discovery`, `connectors/{ideam,gbif,fao,worldpop,gee}`,
`GET /sources*`).

## Objetivos

1. Priorizar valor temprano.
2. Limitar el alcance a cinco fuentes.
3. Validar descubrimiento + explicación + citación.

## Conectores prioritarios

1. **IDEAM**
2. **GBIF**
3. **FAOSTAT**
4. **WorldPop**
5. **Google Earth Engine**

## Capacidades mínimas del MVP

| Capacidad | Descripción |
|-----------|-------------|
| Descubrir fuentes | Identificar y localizar las fuentes MVP |
| Clasificarlas | Dominio, país/ámbito, tipo |
| Explicarlas | Por qué son relevantes al caso |
| Información básica | Metadatos esenciales de acceso |
| Generar citas | Referencias en formatos previstos |

## Fuera de alcance del MVP

- Watcher Engine completo
- API pública estabilizada
- Todos los country profiles poblados
- Agentes IA en producción
- Descarga masiva / ETL complejo
- Scoring calibrado en producción

## Criterio de éxito conceptual

Un usuario puede formular una pregunta territorial simple y obtener: fuentes candidatas MVP, explicación breve y cita básica.

## Relación con roadmap

MVP se materializa principalmente en **Fase 5**, apoyado en Fases 1–4.

## Secciones reservadas (futuro)

- [ ] Historias de usuario detalladas
- [ ] Criterios de aceptación verificables
- [ ] Dataset de evaluación del MVP

---

*MVP conceptual únicamente.*