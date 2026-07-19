# 09 — Recommendation Engine

## Propósito

Definir el motor de recomendación de fuentes y datasets según problemas territoriales.

## Alcance

Responsabilidades y flujo conceptual. Sin algoritmos implementados.

## Objetivos

1. Traducir preguntas geográficas en recomendaciones.
2. Combinar Country Profiles, Scoring y Knowledge Graph.
3. Explicar por qué se recomienda una fuente.

## Entradas conceptuales

- Pregunta / caso de uso territorial
- País / región
- Dominio temático
- Restricciones (resolución, temporalidad, licencia) — futuro

## Salidas conceptuales

- Lista ordenada de fuentes / datasets
- Explicación de la selección
- Enlaces a citación y métodos de acceso (fases posteriores)

## Flujo conceptual

```text
Pregunta geográfica
        │
        ▼
┌───────────────────┐
│ Normalización     │  dominio · país · variables
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ Candidatos (KG +  │
│ Country Profiles) │
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ Scoring           │  Scientific · Trust · GIS · AI · Sustainability
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ Ranking + Explain │
└───────────────────┘
```

## Ejemplo

```text
Entrada: "Modelar hábitat de aves en Colombia"
Salida conceptual:
  GBIF · eBird · SiB Colombia · WorldCover · Sentinel-2 · CHELSA
```

## Ubicación en código (skeleton)

```text
backend/recommendation/
```

## Secciones reservadas (futuro)

- [ ] Estrategias de ranking
- [ ] Explicaciones estructuradas
- [ ] Personalización por perfil de usuario
- [ ] Evaluación offline de recomendaciones

---

*Sin lógica de negocio operativa.*