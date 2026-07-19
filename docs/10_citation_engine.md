# 10 — Citation Engine

## Propósito

Definir el motor de citación reproducible de fuentes y datasets.

## Alcance

Formatos y responsabilidades. Sin generadores implementados.

## Objetivos

1. Garantizar trazabilidad científica.
2. Estandarizar salidas de citación.
3. Integrarse con conectores y agentes Cite / Code.

## Formatos previstos

| Formato | Uso típico |
|---------|------------|
| APA | Publicaciones y reportes |
| BibTeX | LaTeX / gestores |
| RIS | Gestores bibliográficos |
| DOI | Identificador persistente |
| Referencia oficial | Citación de la institución productora |
| Documentación oficial | Enlace a docs de la fuente |
| Artículo original | Cuando aplique |

## Flujo conceptual

```text
Dataset / Fuente
      │
      ▼
Metadatos de citación (Metadata Engine + Connector)
      │
      ▼
Citation Engine
      │
      ├── APA
      ├── BibTeX
      ├── RIS
      ├── DOI
      └── Referencia oficial
```

## Ubicación en código (skeleton)

```text
backend/citation/
agents/cite/
```

## Secciones reservadas (futuro)

- [ ] Plantillas por formato
- [ ] Normalización de autores / años / URLs
- [ ] Validación de DOI
- [ ] Empaquetado con código reproducible

---

*Solo diseño conceptual.*