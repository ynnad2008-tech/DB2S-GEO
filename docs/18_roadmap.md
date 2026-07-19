# 18 — Roadmap (detalle documental)

## Propósito

Ampliar el roadmap del repositorio (`ROADMAP.md`) con notas de gobernanza de fases.

## Alcance

Fases 0–8. Sin estimaciones de calendario rígidas.

## Fases

| Fase | Nombre | Enfoque |
|------|--------|---------|
| 0 | Arquitectura | Skeleton, docs, contratos, catálogo ampliado |
| 1 | Discovery Engine | Descubrimiento de recursos |
| 2 | Knowledge Graph | Relaciones de conocimiento + nodos nuevos |
| 3 | Recommendation Engine | Ranking y explicación |
| 4 | Citation Engine | Referencias + índices bibliográficos (documental) |
| 5 | Conectores prioritarios | IDEAM, GBIF, FAOSTAT, WorldPop, GEE |
| 6 | Agentes IA | Discover·Compare·Cite·Code·Advisor·Watcher |
| 7 | Watcher Engine | Monitoreo de novedades |
| 8 | API pública | Gateway estable |

## Incorporación de fuentes (2026) — impacto por fase

| Fase | Impacto documental |
|------|--------------------|
| 0 | Registro en catálogo, country profile Colombia, dominios, KG conceptual |
| 1 | Candidatas a discovery (datos.gov.co, portales institucionales) |
| 2 | Nodos y relaciones (conservación, tierras, víctimas, suelos, aridez, literatura) |
| 4 | Google Scholar · Scopus · Web of Science como apoyo a citación |
| 5+ | Backlog post-MVP de conectores (sin alterar el MVP de 5 fuentes) |

## Fuentes en backlog (sin implementación)

```text
RUNAP · Parques Nacionales · Global Forest Watch
UPRA · SIPRA · ANT · URT
SNARIV · UARIV · SISBÉN · UBPD · datos.gov.co
SoilGrids · OpenLandMap · CGIAR Aridity Index
Google Scholar · Scopus · Web of Science
```

## Regla de avance

No se inicia implementación de una fase sin:

1. Cierre documental mínimo de la fase previa.
2. Contratos/interfaces estables cuando aplique.
3. Alineación con el Project Charter.
4. Evaluación ética cuando la fuente involucre víctimas, paz o datos personales.

## Diagrama

```text
0 Arquitectura  ← catálogo y perfiles actualizados
└─1 Discovery
  └─2 Knowledge Graph  ← nodos Colombia + globales + literatura
    ├─3 Recommendation
    ├─4 Citation  ← Scholar / Scopus / WoS (documental)
    └─5 Conectores MVP
      │   └─ backlog post-MVP (conectores candidatos)
      └─6 Agentes IA
        └─7 Watcher
          └─8 API pública
```

## Secciones reservadas (futuro)

- [ ] Fechas y milestones
- [ ] Responsables por fase
- [ ] Dependencias externas (credenciales, cuotas API)
- [ ] Priorización formal del backlog post-MVP

---

*Ver también `ROADMAP.md` en la raíz.*
