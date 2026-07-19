# DB2S-GEO
## Registro de Diseño y Evolución Conceptual

### Estado
Pre-arquitectura

### Autor
Dany Arbey Benavides

---

# 1. Origen de la idea

La idea comenzó como un catálogo de fuentes geoespaciales para apoyar proyectos SIG, gestión territorial, investigación ambiental y análisis de cuencas.

Inicialmente el objetivo era identificar:

- APIs geoespaciales.
- Servicios OGC.
- Servicios ArcGIS.
- Datos abiertos.
- Fuentes nacionales e internacionales.

Posteriormente el alcance evolucionó.

---

# 2. Cambio de paradigma

Se concluyó que un catálogo no era suficiente.

Un catálogo responde:

¿Qué datos existen?

DB2S-GEO debe responder:

- ¿Qué información necesito?
- ¿Cuál fuente es mejor?
- ¿Por qué es mejor?
- ¿Cómo acceder?
- ¿Cómo citar?
- ¿Cómo utilizar?

---

# 3. Cambio de nombre

GEONIDO evolucionó hacia DB2S-GEO para mantener coherencia con el ecosistema DB2S.

---

# 4. Definición conceptual final

DB2S-GEO es una plataforma inteligente para el descubrimiento, evaluación, recomendación e integración de información geoespacial.

---

# 5. Enfoque geográfico

La plataforma debe pensar como un geógrafo y responder preguntas territoriales.

Ejemplo:

Necesito modelar hábitat de aves.

Fuentes sugeridas:

- GBIF
- eBird
- SiB Colombia
- WorldCover
- Sentinel-2
- CHELSA

---

# 6. Dominios temáticos

- Geografía Base
- Clima
- Hidrología
- Biodiversidad
- Cobertura del suelo
- Suelos
- Agricultura y Ganadería
- Riesgo
- Población
- Conservación
- Observación de la Tierra

---

# 7. Fuentes estratégicas identificadas

## Colombia

- SIAC
- IDEAM
- IGAC
- DANE
- SGC
- ANLA
- INVEMAR
- DIMAR
- SINCHI
- IIAP
- IAvH

## Observación de la Tierra

### NASA

- EarthData
- LP DAAC
- GES DISC
- ORNL
- Giovanni
- AppEEARS
- FIRMS

### ESA

- Sentinel-1
- Sentinel-2
- Sentinel-3
- Sentinel-5P
- Sentinel-6

### Otros

- ASF
- Planetary Computer
- Earth Search
- Google Earth Engine

## Biodiversidad

- GBIF
- eBird
- BirdCast
- Macaulay Library
- iNaturalist
- SiB Colombia
- OBIS
- BIEN

## Cobertura

- MapBiomas
- WorldCover
- Dynamic World
- Global Forest Watch

## Clima

- CHIRPS
- ERA5
- WorldClim
- CHELSA
- IRI
- GPM

## Suelos

- SoilGrids
- OpenLandMap

## Socioeconómico

- FAOSTAT
- Banco Mundial
- WorldPop
- HDX
- ONU

## Riesgo

- UNOSAT
- EM-DAT
- DesInventar
- INFORM
- USGS Hazards

---

# 8. Incorporación de la dimensión socioeconómica

Integración de población, pobreza, producción, infraestructura y estadística oficial.

Fuentes:

- DANE
- FAO
- Banco Mundial
- WorldPop
- HDX

---

# 9. Incorporación de biodiversidad

Fuentes prioritarias:

- GBIF
- eBird
- SiB Colombia

---

# 10. Perfiles nacionales

## Colombia

- IGAC
- IDEAM
- DANE
- SGC

## Honduras

- ICF
- SINIT
- CENAOS
- INE
- MiAmbiente
- CATIE
- ESNACIFOR

## Costa Rica

- IGN
- SNIT
- SINAC
- IMN
- INEC
- MINAE
- CATIE
- OTS

---

# 11. Regla de priorización

1. Fuente oficial nacional
2. Fuente regional especializada
3. Fuente global
4. Alternativas complementarias

---

# 12. Sistema de recomendación

Indicadores:

- Scientific Score
- GIS Score
- Trust Score
- AI Score

---

# 13. Sistema de citación

- APA
- BibTeX
- RIS
- DOI
- Artículo original
- Documentación oficial

---

# 14. Knowledge Graph

Institución → Fuente → Dataset → Variable → Servicio → API → Referencia → Caso de uso

---

# 15. Watcher Engine

Detecta:

- Nuevos datasets
- Nuevas APIs
- Nuevos STAC
- Nuevos ArcGIS Hub
- Nuevos geoportales
- Nuevas versiones

---

# 16. Conectores

Ejemplos:

- Connector_IDEAM
- Connector_GBIF
- Connector_FAO
- Connector_WorldBank
- Connector_GEE
- Connector_MapBiomas

---

# 17. Agentes IA

- DB2S-GEO Discover
- DB2S-GEO Compare
- DB2S-GEO Cite
- DB2S-GEO Code
- DB2S-GEO Advisor
- DB2S-GEO Watcher

---

# 18. Tecnología objetivo

- Cursor
- GitHub
- Hugging Face
- FastAPI
- PostgreSQL
- PostGIS
- OpenSearch
- Elasticsearch

---

# 19. Conclusión actual

DB2S-GEO debe evolucionar hacia un sistema de conocimiento geográfico capaz de integrar información ambiental, territorial, socioeconómica y científica para apoyar decisiones y responder preguntas geográficas complejas.

---

# Estado de madurez conceptual

- Visión: Completa
- Arquitectura conceptual: Completa
- Dominios: Completo
- Fuentes estratégicas: Muy avanzado
- Perfiles país: Iniciado
- Knowledge Graph: Definido
- Sistema de puntajes: Definido
- Agentes IA: Definidos
- Arquitectura técnica: Preliminar
- MVP: Definido
- Implementación: No iniciada


# 20. Evolución Conceptual Posterior a la Generación del Skeleton

## Contexto

Una vez completada la Fase 0 y generado el skeleton profesional de DB2S-GEO, se continuó el proceso de reflexión conceptual para identificar vacíos temáticos, nuevas fuentes estratégicas y mejoras al modelo de conocimiento territorial.

El objetivo de esta etapa no fue desarrollar código, sino ampliar y consolidar el marco conceptual del proyecto.

---

## 20.1 Validación de la Arquitectura Base

La generación del skeleton confirmó varias decisiones consideradas críticas:

- Arquitectura modular.
- Framework de conectores desacoplado.
- Country Profiles independientes.
- Knowledge Graph como núcleo conceptual.
- Agentes IA separados del backend principal.
- Roadmap por fases.
- MVP claramente delimitado.

Se concluyó que la arquitectura base es suficientemente flexible para crecer sin modificar el núcleo del sistema.

---

## 20.2 Evolución de la Visión del Proyecto

La visión evolucionó progresivamente.

### Versión inicial

Catalogar datasets geoespaciales.

### Segunda versión

Descubrir y recomendar fuentes de datos.

### Tercera versión

Plataforma de conocimiento geográfico.

### Versión actual

Infraestructura de inteligencia territorial capaz de integrar:

- información ambiental;
- información socioeconómica;
- conocimiento científico;
- sistemas institucionales;
- observatorios;
- plataformas de datos.

---

## 20.3 Principio de Escala Territorial

Se identificó que la calidad de una fuente depende de la escala territorial adecuada.

La jerarquía conceptual quedó definida como:

Global
↓
Regional Internacional
↓
Nacional
↓
Regional Subnacional
↓
Local

La plataforma no debe asumir que una fuente global es siempre la mejor opción.

---

## 20.4 Nueva Jerarquía de Fuentes

Se concluyó que las fuentes no deben clasificarse únicamente por institución.

La clasificación propuesta es:

### Datos

Datasets individuales.

### Sistemas de Información

Ejemplos:

- SIPRA
- RUNAP
- SISBÉN
- SiB Colombia

### Infraestructuras de Datos

Ejemplos:

- SIAC
- datos.gov.co
- SNIT
- SINIT

### Observatorios

Ejemplos:

- UBPD
- observatorios regionales
- observatorios temáticos

### Plataformas Científicas

Ejemplos:

- Scopus
- Web of Science
- OpenAlex
- Google Scholar

---

## 20.5 Nuevas Fuentes Prioritarias Identificadas

### Datos Abiertos

- datos.gov.co

### Conservación

- RUNAP
- Parques Nacionales Naturales
- Global Forest Watch
- Protected Planet

### Tierra y Tenencia

- ANT
- URT

### Planificación Rural

- UPRA
- SIPRA

### Vulnerabilidad Social

- SISBÉN

### Reparación y Conflicto

- SNARIV
- UARIV
- UBPD

---

## 20.6 Importancia Estratégica de UPRA

Durante la discusión se concluyó que la UPRA es una fuente estratégica de primer nivel para Colombia.

Razones:

- vocación productiva;
- aptitud agropecuaria;
- frontera agrícola;
- conflictos de uso;
- ordenamiento productivo.

Para estudios de:

- ganadería;
- planificación rural;
- cuencas hidrográficas;
- resiliencia;

la UPRA puede resultar tan importante como IDEAM o DANE.

---

## 20.7 Incorporación Formal de Tierra y Tenencia

Inicialmente el proyecto estaba enfocado en ambiente y geografía.

Posteriormente se reconoció la necesidad de incluir:

- tenencia;
- acceso a tierras;
- restitución;
- reforma agraria;
- conflicto territorial.

Fuentes principales:

- ANT
- URT
- UPRA
- SIPRA

---

## 20.8 Incorporación de Vulnerabilidad y Reparación

Se identificó la necesidad de modelar variables sociales y territoriales asociadas a:

- pobreza;
- vulnerabilidad;
- reparación;
- conflicto;
- memoria.

Fuentes:

- SISBÉN
- SNARIV
- UARIV
- UBPD

---

## 20.9 Nuevas Fuentes de Conservación

Se concluyó que las siguientes fuentes deben tener prioridad alta:

### Nacional

- RUNAP
- Parques Nacionales Naturales

### Internacional

- Global Forest Watch
- Protected Planet

Estas fuentes complementan directamente:

- GBIF
- eBird
- WorldCover
- MapBiomas

---

## 20.10 Nuevas Fuentes de Suelos

Se identificaron como estratégicas:

### SoilGrids

Variables:

- carbono;
- pH;
- textura;
- densidad aparente;
- propiedades físicas del suelo.

### OpenLandMap

Variables:

- suelos;
- hidrología;
- vegetación;
- clima.

### Grupos Hidrológicos de Suelo

Aplicaciones:

- infiltración;
- escorrentía;
- Curve Number;
- modelación hidrológica.

---

## 20.11 Índice Global de Aridez

Se identificó la necesidad de incorporar:

### Global Aridity Index

Variables:

- índice de aridez;
- evapotranspiración potencial.

Aplicaciones:

- balance hídrico;
- cambio climático;
- restauración ecológica;
- resiliencia.

---

## 20.12 Inteligencia Científica

Surge un nuevo dominio estratégico.

### Motores de Descubrimiento Científico

- Google Scholar
- OpenAlex
- Semantic Scholar

### Bibliometría

- Scopus
- Web of Science

### Identidad Académica

- ORCID

### Metadatos

- Crossref

### Propiedad Intelectual y Ciencia

- Lens

---

## 20.13 Nuevo Dominio: Inteligencia Científica

Objetivos:

- descubrir literatura;
- identificar metodologías;
- encontrar artículos relevantes;
- identificar investigadores;
- soportar el Scientific Score.

Se reconoció que DB2S-GEO debe descubrir tanto datos como conocimiento científico asociado a esos datos.

---

## 20.14 Nuevos Dominios Temáticos

La estructura temática se amplía para incluir:

01 Geografía Base

02 Clima

03 Hidrología

04 Suelos

05 Biodiversidad

06 Coberturas

07 Conservación

08 Agricultura

09 Ganadería

10 Planificación Rural

11 Tierra y Tenencia

12 Reforma Agraria

13 Conflicto y Reparación

14 Riesgo

15 Desastres

16 Población

17 Vulnerabilidad Social

18 Infraestructura

19 Observación de la Tierra

20 Inteligencia Científica

21 Datos Abiertos

22 Gobernanza Territorial

23 Socioecología

---

## 20.15 Lección Arquitectónica Principal

La conclusión más importante alcanzada durante esta fase fue:

DB2S-GEO no debe evolucionar como un catálogo de datasets.

Debe evolucionar como una infraestructura de inteligencia territorial capaz de conectar:

- datos;
- instituciones;
- sistemas de información;
- observatorios;
- literatura científica;
- casos de uso;
- conocimiento geográfico.

La calidad de las respuestas dependerá de la capacidad de relacionar todas estas dimensiones dentro del Knowledge Graph.

---

## 20.16 Estado al Final de la Fase 0

Completado:

- visión;
- arquitectura conceptual;
- framework de conectores;
- skeleton;
- roadmap;
- MVP;
- knowledge graph conceptual;
- perfiles de país iniciales.

Pendiente:

- consolidación documental;
- actualización de catálogos;
- expansión del Knowledge Graph;
- Discovery Engine.

Se propone formalmente una Fase 0.5 destinada exclusivamente a consolidación conceptual antes de iniciar desarrollos funcionales.

A partir de la disertación se adoptó formalmente el **Principio de Curaduría Humana** como decisión arquitectónica del proyecto.

Justificación:

Se concluyó que DB2S-GEO podrá descubrir automáticamente nuevas fuentes, APIs, servicios y modificaciones externas mediante mecanismos de monitoreo.

Sin embargo, ninguna modificación del catálogo oficial será incorporada automáticamente.

Toda actualización deberá ser validada por una persona responsable de la curaduría del conocimiento para garantizar calidad, trazabilidad, estabilidad y seguridad.

### Principio de Atribución y Trazabilidad

Se adopta como principio fundacional de DB2S-GEO que toda información presentada por la plataforma deberá conservar la referencia explícita de su fuente original.

El sistema deberá facilitar la citación académica e institucional mediante formatos estandarizados como APA, BibTeX, RIS y DOI cuando estén disponibles.

DB2S-GEO actuará como integrador y facilitador de información, reconociendo permanentemente la autoría de las instituciones, repositorios, investigadores y organizaciones responsables de la producción de los datos.


### Principio de Atribución y Trazabilidad

Se adopta formalmente que todo resultado generado por DB2S-GEO deberá conservar la referencia de su fuente original.

La plataforma facilitará la citación mediante formatos como APA, BibTeX, RIS y DOI cuando estén disponibles.

DB2S-GEO actuará como integrador y facilitador del conocimiento, reconociendo explícitamente la autoría de instituciones, investigadores y organizaciones responsables de la producción de los datos.

## Declaración de Cierre de Fase 0.5

Tras la consolidación documental, la incorporación de nuevas fuentes estratégicas, la definición de los principios de Curaduría Humana y Atribución y Trazabilidad, así como la formalización del modelo de colaboración y gobernanza, se considera completada la Fase 0.5 del proyecto DB2S-GEO.

La arquitectura conceptual se considera suficientemente madura para iniciar la Fase 1 (Discovery Engine MVP).

Las futuras ampliaciones del catálogo no condicionan el inicio del desarrollo funcional, ya que la arquitectura adoptada permite incorporar nuevas fuentes sin modificaciones estructurales del sistema.

## Declaración de Cierre de Fase 1

La Fase 1 (Discovery Engine MVP) se considera completada exitosamente.

Se validó:

- Registro de conectores.
- Descubrimiento de fuentes.
- Obtención de metadatos.
- Integración básica con Citation Engine.
- Generación de referencias.
- Aplicación del Principio de Atribución y Trazabilidad.
- Separación entre catálogo documental y conectores operativos.

Se trabajó exclusivamente con:

- IDEAM
- GBIF
- FAOSTAT
- WorldPop
- Google Earth Engine

La arquitectura demostró ser funcional y extensible.

Se autoriza el inicio de la siguiente etapa.

### Implementación de la Fase 1

Durante la implementación de la Fase 1 se utilizó un subagente de desarrollo para construir el Discovery Engine MVP.

La lógica funcional resultante fue incorporada al backend principal, específicamente en:

- backend/discovery/
- backend/api/
- backend/citation/

Por tanto, el subagente actuó únicamente como mecanismo de desarrollo y no como componente arquitectónico obligatorio del sistema.


### Principio de Sostenibilidad Operativa

DB2S-GEO deberá priorizar arquitecturas, servicios, tecnologías y dependencias que permitan una operación de muy bajo costo o costo cero durante las fases iniciales del proyecto.

Toda decisión tecnológica deberá evaluar explícitamente:

- costo económico;
- costo de mantenimiento;
- dependencia de proveedores;
- facilidad de migración;
- sostenibilidad a largo plazo.


## Declaración de Cierre de Fase 1

La Fase 1 se considera completada exitosamente.

Se validó:

- Registro de conectores.
- Discovery Engine.
- API mínima funcional.
- Citation Engine.
- Curaduría Humana.
- Atribución y Trazabilidad.

Las fuentes MVP implementadas fueron:

- IDEAM
- GBIF
- FAOSTAT
- WorldPop
- Google Earth Engine

Se autoriza el inicio de la Fase 2 (Metadata Engine).


## Expansión MVP Nacional

Tras la validación exitosa de la Fase 1 se acuerda incorporar INVEMAR como primer conector estratégico nacional fuera del conjunto MVP inicial.

La incorporación busca validar la capacidad de DB2S-GEO para representar recursos marino-costeros, biodiversidad marina y sistemas de información ambientales especializados.

Esta ampliación no modifica el alcance original del MVP ni la declaración de cierre de la Fase 1.


## Declaración de Cierre de Fase 2

## Declaración de Cierre de Fase 2

La Fase 2 (Metadata Engine MVP) se considera completada exitosamente.

Se validó:

- Listado de recursos por fuente.
- Descripción normalizada de recursos.
- Clasificación por dominios temáticos.
- Asociación de palabras clave curadas.
- Gestión explícita de campos no disponibles.
- Integración con Discovery Engine.
- Inclusión de INVEMAR como fuente estratégica nacional.
- Preparación de la estructura semántica requerida para el futuro Knowledge Graph.

Se implementó una taxonomía inicial de dominios:

- clima
- hidrologia
- biodiversidad
- oceanos_costas
- suelos
- agricultura
- poblacion
- observacion_tierra

El Metadata Engine opera bajo los principios de:

- Curaduría Humana
- Attribution & Citation Policy
- Read Only
- Security by Design

La arquitectura se considera lista para iniciar la Fase 3 (Knowledge Graph MVP).


## Incorporación de DIMAR y CIOH

Durante la consolidación de fuentes estratégicas para Colombia se identificó la necesidad de fortalecer el componente marino-costero de DB2S-GEO.

### DIMAR

Dirección General Marítima.

Dominios principales:

- océanos;
- costas;
- hidrografía marítima;
- navegación;
- oceanografía;
- información marina.

Información potencial:

- cartografía náutica;
- batimetría;
- oceanografía operacional;
- monitoreo marino;
- mareas;
- servicios marítimos.

### CIOH

Centro de Investigaciones Oceanográficas e Hidrográficas.

Dominios principales:

- oceanografía física;
- oceanografía costera;
- hidrografía;
- monitoreo marino;
- observación oceánica.

Información potencial:

- mareas;
- corrientes;
- condiciones oceanográficas;
- monitoreo del Caribe colombiano;
- monitoreo del Pacífico colombiano.

### Consideración Arquitectónica

DIMAR y CIOH se consideran fuentes estratégicas nacionales para el dominio:

```text
Océanos y Costas

### Hallazgo: Repositorio CapasGeo IDEAM

Se identificó el repositorio institucional:

https://bart.ideam.gov.co/cneideam/Capasgeo/

Este recurso constituye un mecanismo adicional de acceso a información geoespacial del IDEAM mediante descargas directas.

Se confirma la decisión arquitectónica de modelar múltiples métodos de acceso por fuente.

Caso de IDEAM:

- Portal institucional
- API Socrata
- Servicios geoespaciales
- Repositorio CapasGeo
- Documentación técnica

Lo anterior refuerza el principio:

Fuente ≠ API ≠ Dataset ≠ Servicio.


## Declaración de Cierre de Fase 3

La Fase 3 (Knowledge Graph MVP) se considera completada exitosamente.

Se implementó un Knowledge Graph ligero basado en estructuras Python en memoria.

El modelo incorpora:

- Institution
- Source
- Resource
- Domain
- Keyword

Relaciones:

- publishes
- contains
- belongs_to
- associated_with

Se validó la integración con:

- Discovery Engine
- Metadata Engine

El diseño evita dependencias de tecnologías de grafos externas (Neo4j, RDF, SPARQL), manteniendo la simplicidad, portabilidad y sostenibilidad operacional del proyecto.

La arquitectura se considera lista para iniciar la Fase 4 (Recommendation Engine MVP).



## Declaración de Cierre de Fase 3

La Fase 3 (Knowledge Graph MVP) se considera completada exitosamente.

Se implementó un Knowledge Graph ligero basado en estructuras Python en memoria.

El modelo incorpora:

- Institution
- Source
- Resource
- Domain
- Keyword

Relaciones:

- publishes
- contains
- belongs_to
- associated_with

Se validó la integración con:

- Discovery Engine
- Metadata Engine

El diseño evita dependencias de tecnologías de grafos externas (Neo4j, RDF, SPARQL), manteniendo la simplicidad, portabilidad y sostenibilidad operacional del proyecto.

La arquitectura se considera lista para iniciar la Fase 4 (Recommendation Engine MVP).

### Hallazgos posteriores

Se identifican como fuentes estratégicas para futuras fases:

- DIMAR
- CIOH

Especialmente para fortalecer el dominio:

- Océanos y Costas

Complementando las capacidades de:

- INVEMAR
- IDEAM
- GBIF
- Global Mangrove Watch
- Protected Planet



## Declaración de Cierre de Fase 4

La Fase 4 (Recommendation Engine MVP) se considera completada exitosamente.

Se implementó un sistema de recomendación explicable basado en el Knowledge Graph de DB2S-GEO.

Capacidades validadas:

- Recomendación por palabra clave.
- Recomendación por dominio.
- Recomendación por fuente.
- Recomendación por recurso.
- Generación de score.
- Explicabilidad obligatoria.
- Trazabilidad completa de relaciones utilizadas.

El motor opera sin:

- IA generativa.
- Embeddings.
- Bases vectoriales.
- LLMs.

Las recomendaciones se construyen exclusivamente a partir de relaciones presentes en el Knowledge Graph.

La arquitectura se considera lista para iniciar la Fase 5 (Watcher Engine MVP).

## Declaración de Cierre de Fase 5

La Fase 5 (Watcher Engine MVP) se considera completada exitosamente.

Se implementó un sistema de observación continua de fuentes basado en snapshots, comparación estructurada y generación de eventos.

Capacidades validadas:

- Captura de snapshots por fuente.
- Persistencia local de snapshots.
- Comparación entre estados consecutivos.
- Detección de cambios.
- Generación de eventos estructurados.
- Almacenamiento histórico de eventos.
- Consulta de eventos mediante API.
- Simulación y validación de eventos NEW_RESOURCE.
- Integración con Discovery Engine.
- Integración con Metadata Engine.

Eventos soportados:

- BASELINE_CREATED
- NEW_RESOURCE
- REMOVED_RESOURCE
- RESOURCE_CHANGED
- NEW_ACCESS_METHOD
- ACCESS_METHOD_REMOVED
- METADATA_CHANGED
- SOURCE_UNAVAILABLE

Se validó explícitamente el principio de Curaduría Humana mediante:

- curation = human_required
- auto_applied = false

El Watcher Engine detecta y reporta cambios, pero no modifica automáticamente el catálogo ni los conectores.

La arquitectura se considera lista para iniciar la Fase 6 (Source Discovery Assistant MVP).


## Declaración de Cierre de Fase 6

La Fase 6 (Source Discovery Assistant MVP) se considera completada exitosamente.

Se implementó un sistema de análisis heurístico de fuentes desconocidas capaz de:

- identificar tecnologías de publicación;
- detectar instituciones probables;
- proponer dominios temáticos;
- inferir métodos de acceso;
- generar propuestas de incorporación;
- registrar candidatos para revisión.

Capacidades validadas:

- ArcGIS REST MapServer.
- ArcGIS REST FeatureServer.
- Portales institucionales.
- Repositorios de descargas.
- Clasificación preliminar de dominios.
- Evaluación de confianza.
- Generación de evidencia explicativa.

Se validó explícitamente:

- Curaduría Humana.
- No modificación automática del catálogo.
- No creación automática de conectores.
- No incorporación automática de fuentes.

Todas las propuestas permanecen sujetas a revisión y aprobación humana.

La arquitectura se considera lista para iniciar la siguiente fase de expansión.


## Decisión Arquitectónica — Curator Workbench antes del Frontend Público

Tras la finalización de las fases fundacionales:

- Discovery Engine
- Metadata Engine
- Knowledge Graph
- Recommendation Engine
- Watcher Engine
- Source Discovery Assistant

se decidió posponer la construcción de un frontend público completo.

### Justificación

DB2S-GEO ya dispone de capacidades funcionales suficientes a través de su API y motores internos.

La construcción temprana de un frontend visual complejo podría introducir:

- mayor complejidad;
- más dependencias;
- mayores costos de mantenimiento;
- menor rendimiento;
- desvío de esfuerzos respecto al núcleo de conocimiento.

### Estrategia Adoptada

Antes del frontend público se implementará un Curator Workbench MVP.

El Workbench constituirá una interfaz operativa ligera para:

- revisar candidatos descubiertos;
- revisar eventos del Watcher;
- aprobar o rechazar propuestas;
- inspeccionar recomendaciones;
- consultar el Knowledge Graph;
- auditar la trazabilidad del sistema.

### Principios

- Curaduría Humana.
- Simplicidad.
- Portabilidad.
- Bajo costo operativo.
- Frontend mínimo sobre API existente.

### Alcance del Workbench

No se busca una experiencia visual avanzada.

No incluye:

- visualizadores cartográficos complejos;
- dashboards pesados;
- librerías gráficas extensivas;
- animaciones.

Su objetivo es servir como consola operativa para administradores y curadores.

### Resultado Esperado

DB2S-GEO dispondrá primero de una herramienta de gestión y validación interna antes de exponer capacidades avanzadas al público general.

## Principio de Minimalismo Funcional

DB2S-GEO deberá priorizar interfaces:

- rápidas;
- legibles;
- accesibles;
- visualmente agradables;
- con mínima complejidad técnica.

La simplicidad visual no implica una apariencia rudimentaria.

La experiencia de usuario deberá ser profesional sin comprometer el rendimiento ni la sostenibilidad operativa.


## Decisión de Producto — Footer Institucional y Sostenibilidad

DB2S-GEO incorporará un footer institucional discreto en sus interfaces públicas y operativas.

### Objetivo

Informar a los usuarios sobre la naturaleza independiente del proyecto y ofrecer una vía transparente para apoyar su mantenimiento y evolución.

El mensaje deberá mantener un tono profesional, institucional y no intrusivo.

### Texto aprobado

DB2S-GEO es un proyecto independiente de descubrimiento y gestión de conocimiento territorial.

Si esta plataforma resulta útil para su trabajo, investigación o institución, agradecemos los aportes voluntarios que contribuyen a su mantenimiento y evolución.

Las contribuciones no afectan recomendaciones, resultados ni procesos de curaduría.

© DB2S-GEO

### Principios

- Transparencia.
- Independencia técnica.
- Independencia científica.
- Neutralidad de resultados.
- No existencia de ventajas para contribuyentes.

### Implementación

El footer deberá:

- ubicarse al final de las páginas;
- mantener una tipografía discreta;
- seguir el estilo visual general del sistema;
- evitar ventanas emergentes o mensajes intrusivos;
- poder incluir en el futuro enlaces de apoyo voluntario.

### Consideraciones

Los aportes voluntarios se entienden como un mecanismo de sostenibilidad operativa del proyecto.

Las contribuciones económicas no influyen en:

- recomendaciones;
- rankings;
- procesos de descubrimiento;
- procesos de curaduría;
- decisiones técnicas o científicas.


## Principio de Recomendación Orientada a la Acción

DB2S-GEO no se limitará a recomendar fuentes.

Cuando sea posible, las recomendaciones deberán organizarse en rutas de acción comprensibles para el usuario.

Ejemplos:

- Descargar datos.
- Consultar registros existentes.
- Consumir una API.
- Utilizar plataformas de análisis.
- Realizar procesamiento avanzado.

El objetivo es acercar al usuario a la resolución de su necesidad y no únicamente a los recursos disponibles.

Las explicaciones deberán priorizar:

- qué hacer;
- dónde hacerlo;
- por qué se recomienda;
- nivel de complejidad esperado.

## Decisión de Producto — Atribución y Citación de la Plataforma

DB2S-GEO deberá incorporar mecanismos explícitos de atribución de autoría y citación de la plataforma.

### Objetivo

Facilitar el reconocimiento académico y técnico de la iniciativa y permitir su referencia en:

- tesis;
- artículos científicos;
- informes técnicos;
- proyectos institucionales;
- documentos de planificación.

### Footer Institucional

El sistema podrá mostrar:

© DB2S-GEO · 2026

Proyecto concebido y desarrollado por
Dany Arbey Benavides.

### Citación sugerida

DB2S-GEO deberá incorporar una sección futura denominada:

"Cómo citar"

que permita generar una referencia bibliográfica para la plataforma.

Ejemplo preliminar:

Benavides, D. A. (2026). DB2S-GEO: Plataforma para el descubrimiento, integración y recomendación de fuentes de información territorial y ambiental. Proyecto independiente.

### Principios

- reconocimiento de autoría;
- transparencia;
- trazabilidad académica;
- apoyo a la citación formal;
- coherencia con Attribution & Citation Policy.

## Decisión de Producto — Citación de la Plataforma

DB2S-GEO incorporará una sección permanente denominada:

"Cómo citar esta plataforma"

Objetivos:

- facilitar la referencia académica;
- apoyar tesis, artículos e informes técnicos;
- reconocer la autoría del proyecto;
- promover buenas prácticas de citación.

La sección podrá incluir:

- cita sugerida APA;
- cita sugerida BibTeX;
- versión de la plataforma;
- fecha de consulta;
- autoría del proyecto.


## Decisión de Producto — Sostenibilidad y Apoyos Voluntarios

DB2S-GEO podrá incorporar mecanismos voluntarios de apoyo económico destinados a contribuir a la sostenibilidad operativa del proyecto.

Canales previstos:

### Colombia

- QR interoperable.
- Medios de pago nacionales compatibles.

### Internacional

- Tarjetas internacionales.
- Cuentas de apoyo en USD.
- Cuentas de apoyo en EUR.

### Principios

- Los aportes son voluntarios.
- No existen beneficios funcionales asociados.
- No afectan recomendaciones.
- No afectan procesos de curaduría.
- No afectan resultados del sistema.
- No condicionan decisiones técnicas o científicas.

### Transparencia

Los mecanismos de apoyo deberán distinguir claramente entre:

- uso de la plataforma;
- apoyo voluntario al proyecto.

DB2S-GEO seguirá siendo una herramienta abierta e independiente.

## Decisión de Producto — Observatorio de Uso y Tendencias

DB2S-GEO podrá registrar de forma anónima las consultas realizadas por los usuarios con fines de mejora continua de la plataforma.

### Objetivos

- identificar vacíos de conocimiento;
- enriquecer taxonomías;
- detectar nuevas temáticas emergentes;
- mejorar recomendaciones;
- priorizar procesos de curaduría;
- generar indicadores de uso agregados.

### Información registrada

Podrá registrarse:

- consulta realizada;
- fecha y hora;
- resultados obtenidos;
- dominios activados;
- recomendaciones generadas;
- estadísticas agregadas de uso.

### Información no registrada

No deberán registrarse:

- nombres de usuarios;
- correos electrónicos;
- direcciones IP persistentes;
- credenciales;
- información personal identificable;
- datos sensibles.

### Transparencia

La plataforma deberá informar explícitamente que las consultas podrán ser registradas de forma anonimizada con fines de mejora y análisis de tendencias.

La comunicación deberá ser visible, clara y comprensible para el usuario.

Ejemplo:

"Las consultas realizadas en DB2S-GEO podrán ser registradas de forma anonimizada para mejorar recomendaciones, identificar nuevas temáticas y fortalecer el conocimiento disponible en la plataforma."

### Principios

- anonimización;
- transparencia;
- minimización de datos;
- mejora continua;
- uso exclusivamente técnico y científico.

### Finalidad

La información agregada podrá utilizarse para:

- mejorar el Knowledge Graph;
- ampliar taxonomías;
- incorporar nuevos dominios;
- identificar nuevas fuentes prioritarias;
- analizar tendencias temáticas de interés.

### Consultas sin resultado

Las consultas que no generen recomendaciones deberán recibir atención prioritaria.

Estas consultas constituyen evidencia de vacíos de conocimiento en la plataforma y podrán alimentar futuras tareas de curaduría y expansión temática.

### Comunicación al usuario

DB2S-GEO deberá informar de manera visible que determinadas consultas pueden registrarse de forma anónima para fines de mejora continua.

La notificación deberá:

- estar disponible de forma permanente;
- utilizar lenguaje claro;
- indicar que no se recopilan datos personales;
- enlazar a la política de privacidad y uso de datos cuando exista.

Ejemplo:

"DB2S-GEO registra algunas consultas de forma anónima para mejorar recomendaciones, identificar vacíos de conocimiento y fortalecer la plataforma. No se recopila información personal identificable."

### Visualización de Tendencias

El Observatorio de Uso y Tendencias podrá incorporar mecanismos de visualización agregada de consultas.

Ejemplos:

- nube de palabras;
- tendencias temporales;
- conceptos emergentes;
- dominios más consultados;
- consultas sin resultado.

Objetivos:

- identificar necesidades reales de información;
- orientar procesos de curaduría;
- priorizar incorporación de fuentes;
- enriquecer taxonomías;
- comunicar tendencias de uso de la plataforma.

Las visualizaciones utilizarán exclusivamente datos anonimizados y agregados.

### Nuevos dominios identificados

Se incorporan para futuras versiones de la taxonomía:

- Sensores Remotos
- SIG (Sistemas de Información Geográfica)

Justificación:

Se identifican como áreas de conocimiento transversales con suficiente entidad propia para no depender exclusivamente de otros dominios como Observación de la Tierra, Clima o Coberturas.

Estos dominios servirán para clasificar:

- recursos;
- herramientas;
- plataformas;
- recomendaciones;
- consultas de usuarios.

Ejemplos:

Sensores Remotos:
- Landsat
- Sentinel
- MODIS
- SAR
- LiDAR
- NDVI

SIG:
- QGIS
- ArcGIS
- PostGIS
- Geoprocesamiento
- Álgebra de mapas
- Análisis espacial

## Estrategia de Identidad Digital

DB2S-GEO mantendrá la marca actual durante las fases Alpha y Beta.

Debido a la posible asociación del término "DB2" con tecnologías existentes de terceros, la plataforma reforzará sistemáticamente su identidad mediante:

- nombre completo del proyecto;
- descripción funcional;
- autoría explícita;
- dominio propio futuro;
- página "Cómo citar esta plataforma".

El objetivo será consolidar progresivamente la identidad independiente de DB2S-GEO en buscadores, publicaciones y documentación técnica.

### Valor científico y estratégico del Observatorio

Además de apoyar la mejora continua de DB2S-GEO, el Observatorio de Uso y Tendencias podrá utilizarse como mecanismo de identificación de necesidades emergentes de información ambiental, territorial y científica.

Las consultas agregadas y anonimizadas permitirán:

- detectar temáticas emergentes;
- identificar vacíos de conocimiento;
- orientar procesos de investigación;
- priorizar nuevas líneas de desarrollo;
- apoyar la incorporación de nuevos dominios;
- fortalecer la curaduría del Knowledge Graph.

### Temáticas emergentes

Se consideran de especial interés:

- conceptos con crecimiento sostenido en las consultas;
- nuevos términos con baja representación en el catálogo;
- consultas frecuentes sin resultados;
- temas interdisciplinarios aún no representados en la taxonomía.

### Uso para investigación

Los indicadores agregados podrán emplearse como insumo para:

- artículos científicos;
- tesis;
- informes técnicos;
- análisis de tendencias;
- identificación de oportunidades de investigación;
- priorización de nuevas fuentes de información.

### Principio

DB2S-GEO no solo busca responder preguntas.

También busca identificar qué preguntas aún no tienen respuesta suficiente dentro del ecosistema de información territorial y ambiental.

## Complemento de Búsqueda Externa

DB2S-GEO podrá mostrar resultados externos relevantes como complemento a las recomendaciones internas.

Principios:

- Las recomendaciones de DB2S-GEO tendrán prioridad visual.
- Los resultados externos actuarán como apoyo contextual.
- El objetivo es enriquecer la experiencia del usuario, no sustituir el motor de conocimiento de la plataforma.

Posibles proveedores:

- Google
- IDEAM
- INVEMAR
- datos.gov.co
- GBIF
- SIB Colombia

Las fuentes externas deberán mostrarse claramente diferenciadas de las recomendaciones generadas por DB2S-GEO.

## Idea Futura — Access Accelerator

DB2S-GEO podrá incorporar mecanismos para simplificar el acceso a recursos geoespaciales identificados por la plataforma.

Objetivo:

Reducir la fricción entre el descubrimiento de una fuente y su utilización efectiva.

Capacidades potenciales:

- copiar URLs de servicios;
- generar enlaces directos;
- abrir capas en clientes SIG compatibles;
- generar configuraciones predefinidas;
- facilitar acceso a WMS;
- facilitar acceso a WFS;
- facilitar acceso a ArcGIS REST;
- facilitar acceso a STAC.

Principio:

DB2S-GEO no sustituye a los proveedores de datos.

DB2S-GEO facilita el acceso a recursos publicados por terceros mediante configuraciones y enlaces previamente preparados.

## Principio de Aceleración de Acceso

DB2S-GEO busca reducir la fricción entre el descubrimiento de una fuente y su utilización efectiva.

La plataforma podrá facilitar:

- enlaces directos;
- configuraciones predefinidas;
- acceso simplificado a servicios geoespaciales.

Sin embargo, DB2S-GEO no sustituye el conocimiento técnico necesario para el análisis, interpretación y aplicación de los datos.

El objetivo es facilitar el acceso al conocimiento, no reemplazar la experticia profesional.

### Nube Dinámica de Tendencias

La página de inicio podrá incorporar una visualización dinámica de conceptos y temáticas derivadas del Observatorio de Uso y Tendencias.

Características:

- visualización semitransparente;
- movimiento suave;
- actualización periódica;
- tamaño proporcional a la frecuencia de uso;
- conceptos emergentes destacados;
- impacto visual controlado.

Objetivos:

- comunicar el conocimiento activo de la plataforma;
- destacar tendencias temáticas;
- incentivar la exploración;
- proporcionar identidad visual propia a DB2S-GEO.

Las palabras deberán provenir de datos agregados y anonimizados del Observatorio.

### Nube Dinámica de Interés

La nube de palabras de DB2S-GEO no tendrá una finalidad decorativa.

Representará de forma visual los intereses agregados de la comunidad de usuarios.

Características:

- tamaño proporcional a la frecuencia de consultas;
- actualización periódica;
- alimentación desde el Observatorio de Uso y Tendencias;
- visualización de conceptos emergentes;
- representación de vacíos de conocimiento.

Objetivo:

Convertir la página principal de DB2S-GEO en una representación dinámica de las necesidades actuales de información ambiental, territorial y científica.

### Insignia de confianza

DB2S-GEO utilizará la frase:

"✅ ¡Validado por humanos!"

como mecanismo de comunicación de confianza.

La frase busca destacar que:

- las recomendaciones son explicables;
- existe curaduría humana;
- las fuentes son revisadas;
- las decisiones de conocimiento no dependen exclusivamente de automatización.

La insignia podrá aparecer en la página de inicio y en otros componentes relevantes de la plataforma.

Decisión de Producto

Footer institucional:

Izquierda:
Autoría

Centro:
Cómo citar esta plataforma
Apoya el desarrollo de DB2S-GEO

Derecha:
API