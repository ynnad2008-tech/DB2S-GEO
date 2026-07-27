"""
Enriquecimiento sistemático de keywords en todo el catálogo.
Estrategia: sinónimos, variantes geográficas, conceptos relacionados.
NO modifica dominios. Mantiene los existentes.
"""
from __future__ import annotations

import json
import os
from collections import Counter

CATALOG_DIR = os.path.join(os.path.dirname(__file__), "..", "catalog", "sources")
BACKUP_DIR = os.path.join(os.path.dirname(__file__), "..", "catalog", "reports")

# ── Mapa de sinónimos y conceptos relacionados ──
# Cada tupla es (keyword_canonica, [sinónimos_y_relacionados])
SYNONYMS = {
    # cambio / dinámica temporal
    "cambio": ["cambio", "transicion", "evolucion", "dinamica", "tendencia",
               "multitemporal", "serie_tiempo", "deteccion_cambio", "variacion",
               "transformacion", "modificacion", "historico", "trayectoria"],
    # coberturas / uso del suelo
    "coberturas": ["coberturas", "cobertura", "uso_suelo", "uso_del_suelo",
                   "landcover", "land_cover", "lulc", "tipo_cobertura",
                   "clasificacion", "mapa_cobertura"],
    # monitoreo / observación
    "monitoreo": ["monitoreo", "monitorizacion", "seguimiento", "observacion",
                  "vigilancia", "control", "verificacion", "actualizacion"],
    # bosques / deforestación
    "bosques": ["bosques", "bosque", "forestal", "deforestacion", "reforestacion",
                "cobertura_forestal", "arborea", "arbol", "dosel", "silvicultura"],
    # agua / hidrología
    "agua": ["agua", "aguas", "hidrico", "hidrica", "hidrologico", "hidrologica",
             "cuenca", "rio", "quebrada", "humedal", "cienaga", "estuario"],
    # mar / costa
    "costa": ["costa", "costero", "costera", "litoral", "bahia", "ensenada",
              "golfo", "estuario", "playa", "manglar", "marino", "marina",
              "oceano", "oceanico", "oceanica", "mar", "maritimo", "maritima"],
    # biodiversidad
    "biodiversidad": ["biodiversidad", "diversidad", "especie", "especies",
                      "fauna", "flora", "habitat", "ecosistema", "ecosistemas",
                      "bioma", "conservacion", "area_protegida", "protegida"],
    # región Pacífico colombiano
    "pacifico": ["pacifico", "pacifico_colombiano", "buenaventura", "tumaco",
                 "choco", "choco_biogeografico", "llanura_pacifica", "tropico_humedo"],
    # región Caribe
    "caribe": ["caribe", "caribe_colombiano", "cartagena", "santa_marta",
               "barranquilla", "san_andres", "providencia", "guajira"],
    # Amazonía
    "amazonia": ["amazonia", "amazonas", "amazonico", "amazonica",
                 "leticia", "caqueta", "putumayo", "guaviare", "vaupes"],
    # Orinoquía
    "orinoquia": ["orinoquia", "llanos", "oriente", "meta", "casanare",
                  "vichada", "arauca", "sabana", "morichal"],
    # Andes
    "andes": ["andes", "andina", "andino", "cordillera", "montaña", "paramo",
              "altiplano", "cundiboyacense", "cafetero", "santander"],
    # clima
    "clima": ["clima", "climatico", "climatica", "meteorologia", "meteorologico",
              "precipitacion", "temperatura", "humedad", "viento", "evapotranspiracion",
              "lluvia", "sequia", "fenomeno_nino", "fenomeno_nina"],
    # suelo
    "suelo": ["suelo", "suelos", "edafico", "edafica", "edafologia",
              "propiedades_suelo", "textura", "ph", "carbono_organico",
              "erosion", "degradacion", "fertilidad"],
    # geología
    "geologia": ["geologia", "geologico", "geologica", "geomorfologia", "litologia",
                 "falla", "sismo", "sismico", "sismica", "volcan", "volcanico"],
    # población
    "poblacion": ["poblacion", "poblacional", "demografia", "demografico", "censo",
                  "habitantes", "densidad", "asentamiento", "urbano", "rural"],
    # infraestructura
    "infraestructura": ["infraestructura", "via", "vial", "carretera", "puerto",
                        "aeropuerto", "transporte", "conexion", "red", "acueducto"],
    # riesgo
    "riesgo": ["riesgo", "amenaza", "vulnerabilidad", "desastre", "inundacion",
               "deslizamiento", "incendio", "emergencia", "peligro", "resiliencia"],
}

# ── Reglas por fuente: keywords adicionales específicos ──
PER_SOURCE_ADDITIONS = {
    "dimar": {
        "dimar:batimetria": ["cambio", "costero", "sedimentacion", "dragado",
                             "buenaventura", "tumaco", "pacifico", "caribe"],
        "dimar:sigdimar": ["monitoreo", "integrado", "costero", "multitematico",
                           "buenaventura", "cartagena", "santa_marta"],
        "dimar:senalizacion-maritima": ["buenaventura", "cartagena", "puerto"],
        "dimar:ide-maritima": ["interoperabilidad", "estandar", "costero", "fluvial"],
    },
    "invemar": {
        "invemar:siamexplorer": ["cambio", "costero", "monitoreo", "buenaventura",
                                 "tumaco", "pacifico", "caribe", "multitemporal"],
        "invemar:geovisor": ["costero", "marino", "monitoreo", "cartografia",
                             "buenaventura", "tumaco", "pacifico"],
        "invemar:data-hub": ["cambio", "costero", "historico", "serie_tiempo",
                             "monitoreo", "pacifico", "caribe"],
    },
    "ideam": {
        "ideam:coberturas-tierra": ["cambio", "multitemporal", "deforestacion",
                                    "uso_suelo", "landcover", "lulc", "clasificacion",
                                    "transformacion", "dinamica", "colombia"],
        "ideam:ecosistemas": ["cambio", "transformacion", "biodiversidad",
                              "conservacion", "habitat", "cobertura", "monitoreo"],
        "ideam:deforestacion": ["cambio", "coberturas", "bosques", "perdida",
                                "monitoreo", "alerta", "anual", "colombia"],
        "ideam:consulta-meteorologica": ["cambio", "historico", "tendencia",
                                         "variacion", "serie_tiempo", "monitoreo"],
    },
    "mapbiomas": {
        "mapbiomas:cobertura-colombia": ["cambio", "multitemporal", "dinamica",
                                         "transicion", "uso_suelo", "landcover",
                                         "lulc", "colombia", "anual", "serie_tiempo",
                                         "buenaventura", "pacifico", "caribe"],
        "mapbiomas:transiciones-cobertura": ["cambio", "transicion", "multitemporal",
                                             "dinamica", "uso_suelo", "flujo"],
        "mapbiomas:agua-superficial": ["cambio", "dinamica", "multitemporal",
                                       "inundacion", "estacional", "superficie"],
    },
    "gee": {
        "gee:dynamicworld": ["cambio", "coberturas", "multitemporal", "sentinel-2",
                             "clasificacion", "landcover", "lulc", "dinamica"],
        "gee:era5": ["cambio", "historico", "tendencia", "variacion", "serie_tiempo"],
    },
    "gee-copernicus-sentinel2": {
        "gee-copernicus-sentinel2:dynamicworld": ["cambio", "coberturas", "multitemporal",
                                                   "clasificacion", "landcover", "lulc",
                                                   "sentinel-2", "dinamica", "monitoreo",
                                                   "buenaventura", "pacifico", "colombia"],
    },
    "nasa": {
        "nasa:lpdaac": ["cambio", "coberturas", "multitemporal", "landsat",
                        "modis", "monitoreo", "serie_tiempo"],
    },
    "igac": {
        "igac:ortofotos": ["cambio", "multitemporal", "comparacion", "historico"],
        "igac:cartografia-base": ["coberturas", "uso_suelo", "colombia"],
    },
    "global-forest-watch": {
        "gfw:tree-cover-loss": ["cambio", "coberturas", "multitemporal", "colombia",
                                "buenaventura", "pacifico", "caribe", "monitoreo"],
        "gfw:glad-alerts": ["cambio", "monitoreo", "tiempo_real", "colombia",
                            "buenaventura", "pacifico", "amazonia"],
        "gfw:radd-alerts": ["cambio", "monitoreo", "tiempo_real", "colombia",
                            "buenaventura", "pacifico", "nubes", "tropico_humedo"],
        "gfw:integrated-alerts": ["cambio", "monitoreo", "diario", "colombia",
                                  "buenaventura", "pacifico", "consolidado"],
    },
}

os.makedirs(BACKUP_DIR, exist_ok=True)

total_added = 0
modified = 0

for fname in sorted(os.listdir(CATALOG_DIR)):
    if not fname.endswith(".json"):
        continue

    path = os.path.join(CATALOG_DIR, fname)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    sid = data.get("id", "")
    resources = data.get("resources", [])
    changed = False

    for r in resources:
        rid = r.get("id", "")
        existing = set(r.get("keywords", []))

        # Enriquecer con adiciones específicas por fuente
        specific = PER_SOURCE_ADDITIONS.get(sid, {}).get(rid, [])
        # Enriquecer con sinónimos para keywords ya existentes
        synonym_additions = set()
        for kw in existing:
            for canonical, synonyms in SYNONYMS.items():
                if kw in synonyms:
                    synonym_additions.update(synonyms)

        new_kw = sorted(existing | set(specific) | synonym_additions)
        added = len(new_kw) - len(existing)

        if added > 0:
            r["keywords"] = new_kw
            changed = True
            total_added += added

    if changed:
        # Backup
        backup_path = os.path.join(BACKUP_DIR, f"kw_{fname}")
        with open(backup_path, "w", encoding="utf-8") as bf:
            json.dump(data, bf, ensure_ascii=False, indent=2)
        modified += 1

    # Guardar
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Enriquecimiento completado:")
print(f"  Fuentes modificadas: {modified}")
print(f"  Keywords agregados: {total_added}")
print(f"  Backups en: {BACKUP_DIR}/kw_*.json")
print()
print("Estrategia aplicada:")
print("  ✓ Sinónimos y conceptos relacionados para cada keyword existente")
print("  ✓ Adiciones específicas por fuente y recurso")
print("  ✓ Variantes geográficas (buenaventura, pacifico, caribe, amazonia...)")
print("  ✗ Dominios NO modificados")
