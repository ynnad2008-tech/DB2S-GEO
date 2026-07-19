# 08 — Sistema de Scoring

## Propósito

Documentar el marco conceptual de puntuación para evaluación y recomendación de fuentes.

## Alcance

Definición de scores. Sin fórmulas, pesos finales ni código.

## Objetivos

1. Nombrar y delimitar cada score.
2. Orientar el Recommendation Engine.
3. Reservar espacio para calibración futura.

## Scores previstos

| Score | Intención conceptual |
|-------|----------------------|
| **Scientific Score** | Rigor, trazabilidad, uso científico |
| **Trust Score** | Confianza institucional / oficialidad |
| **GIS Score** | Utilidad y facilidad de uso en entornos SIG |
| **AI Score** | Aptitud para consumo por sistemas IA / automatización |
| **Sustainability Score** | Continuidad, actualización, sostenibilidad de la fuente |

## Relación con priorización

```text
Priorización cualitativa          Scoring cuantitativo (futuro)
─────────────────────────         ────────────────────────────
1. Oficial nacional        ──►    Trust Score ↑
2. Regional especializada  ──►    Trust + Scientific
3. Global                  ──►    Scientific + GIS + AI
4. Complementaria          ──►    Scores contextuales
```

## Ejemplo conceptual (sin números)

```text
Consulta: Población en Colombia
Candidatos: DANE, WorldPop, Banco Mundial
Orientación: DANE (oficial) precede a globales, scores refinan el ranking.
```

## Secciones reservadas (futuro)

- [ ] Definición operativa de indicadores
- [ ] Pesos por dominio / país / caso de uso
- [ ] Normalización y umbrales
- [ ] Explicabilidad del score

---

*Marco conceptual únicamente.*