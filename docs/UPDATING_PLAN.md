# Plan de actualización controlada

Basado en consultas reales del Observatory (`data/observatory/queries.json`).
Cada sesión inicia con un diagnóstico y avanza **1 tema por vez**.

---

## Ciclo por sesión

1. **Diagnóstico** → ejecutar script para identificar vacíos actuales
2. **Elegir 1 tema** del top de "sin resultados"
3. **Investigación** → buscar fuentes colombianas que cubran ese tema
4. **Implementación** → conector + catalog + tests
5. **Validación** → `pytest tests/ -v` (mínimo los tests del conector nuevo)
6. **Commit + Push**
7. **Re-diagnóstico** → verificar que el vacío se redujo

---

## Script de diagnóstico

```bash
python -c "
import json
with open('data/observatory/queries.json') as f:
    data = json.load(f)

nores = [r for r in data if not r.get('has_results')]
print(f'Consultas sin resultados: {len(nores)}/{len(data)}')

from collections import Counter
terms = Counter()
for r in nores:
    for t in r.get('terms', []):
        terms[t] += 1
print('\\nTop 15 terminos sin cobertura:')
for t, c in terms.most_common(15):
    print(f'  {t}: {c}')

from collections import Counter as C2
raw = C2(r['query'].strip().lower() for r in nores)
print('\\nTop 10 consultas sin resultados:')
for q, c in raw.most_common(10):
    print(f'  \"{q}\": {c}')
"
```

---

## Temas frecuentes a cubrir (por confirmar con diagnóstico)

| Tema | Dominio esperado | Posibles fuentes |
|------|-----------------|------------------|
| Ordenamiento territorial | `ordenamiento` | POT, DNP, IGAC |
| Conflictos de uso del suelo | `suelos` | UPRA, IGAC, UAESPNN |
| Cobertura vegetal / bosque | `ecosistemas` | IDEAM, Sinchi, SiB |
| Deforestación | `ecosistemas`, `biodiversidad` | IDEAM, Sinchi |
| Calidad del agua | `hidrologia` | IDEAM, CARs |
| Amenazas naturales | `riesgo` | UNGRD, SGC, IDEAM |
| Infraestructura educativa / salud | `infraestructura` | DNP, MinEducación, MinSalud |
| Cambio climático | `clima` | IDEAM, CIIFEN, NOAA |
| Minerales / minería | `geologia` | SGC, ANM |

---

## Reglas

- **1 tema por commit** (commits atómicos y revisables)
- **Diagnóstico antes y después** para medir impacto
- **No mezclar** correcciones de dominios con nuevos recursos
- Si una fuente ya existe, solo **agregar keywords/endpoints** en lugar de nuevo conector
