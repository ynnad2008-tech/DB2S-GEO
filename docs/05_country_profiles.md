# 05 — Country Profiles

## Propósito

Definir el marco documental de perfiles nacionales para priorizar fuentes oficiales.

## Alcance

Plantillas y estructura por país. Sin evaluación operativa ni conectores.

## Objetivos

1. Estandarizar el registro de instituciones y geoportales por país.
2. Soportar la política de priorización (oficial nacional → regional → global).
3. Preparar expansión geográfica futura.

## Política de priorización

```text
1. Fuente Oficial Nacional
2. Fuente Regional Especializada
3. Fuente Global
4. Alternativas Complementarias
```

### Ejemplo

```text
Población Colombia
1. DANE
2. WorldPop
3. Banco Mundial
```

## Países en skeleton

| Código carpeta | País |
|----------------|------|
| colombia | Colombia |
| honduras | Honduras |
| costa_rica | Costa Rica |
| mexico | México |
| brasil | Brasil |
| peru | Perú |
| ecuador | Ecuador |
| chile | Chile |
| panama | Panamá |
| guatemala | Guatemala |

## Secciones de plantilla (por país)

- Instituciones geográficas
- Instituciones ambientales
- Instituciones meteorológicas
- Instituciones estadísticas
- Geoportales
- APIs
- Observaciones

## Fuentes iniciales documentadas (referencia)

### Colombia
IGAC · IDEAM · DANE · SGC · SIAC · ANLA · INVEMAR · DIMAR · IAvH · SINCHI · IIAP

**Ampliación 2026:** RUNAP · Parques Nacionales · UPRA · SIPRA · ANT · URT · SNARIV · UARIV · SISBÉN · UBPD · datos.gov.co

Complementarias globales relevantes al perfil: Global Forest Watch · SoilGrids · OpenLandMap · CGIAR Aridity Index  
Literatura científica (citación): Google Scholar · Scopus · Web of Science

### Honduras
ICF · SINIT · CENAOS · MiAmbiente · INE · CATIE · ESNACIFOR

### Costa Rica
IGN · SNIT · SINAC · IMN · MINAE · INEC · CATIE · OTS

## Estructura

```text
country_profiles/
├── README.md
├── _template.md
├── colombia/
├── honduras/
├── ...
└── guatemala/
```

## Secciones reservadas (futuro)

- [ ] Completar instituciones por país
- [ ] Enlaces oficiales verificados
- [ ] Mapeo a conectores
- [ ] Scores de cobertura nacional

---

*Solo plantillas documentales.*