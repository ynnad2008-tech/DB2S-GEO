"""
Corrección de keywords: revierte el enriquecimiento excesivo y
aplica la estrategia correcta:

  GENERIC_KEYWORDS → filtra ruido del scoring (no puntúan)
  CURATED_ALIASES → expande la CONSULTA del usuario (no los recursos)
  Resource keywords → SOLO términos ESPECÍFICOS y diferenciadores

Principio: keywords genéricos en recursos DEGRADAN el MVP.
"""

from __future__ import annotations

import json
import os

CATALOG_DIR = os.path.join(os.path.dirname(__file__), "..", "catalog", "sources")
BACKUP_DIR = os.path.join(os.path.dirname(__file__), "..", "catalog", "reports")

# ── Keywords DEMASIADO genéricos para estar en recursos ──
# Estos términos los expande CURATED_ALIASES a nivel de consulta,
# o los filtra GENERIC_KEYWORDS. NO deben estar en los recursos.
GENERIC_NOISE = {
    # Verbos y conceptos demasiado amplios
    "cambio", "transicion", "evolucion", "dinamica", "tendencia",
    "transformacion", "modificacion", "variacion", "trayectoria",
    # Monitoreo genérico
    "monitoreo", "monitorizacion", "seguimiento", "observacion",
    "vigilancia", "control", "verificacion", "actualizacion",
    # Términos geográficos demasiado amplios
    "colombia", "colombiano", "colombiana", "nacional", "global",
    "regional", "local", "municipal", "departamental",
    # Adjetivos genéricos
    "historico", "integrado", "consolidado", "unificado",
    "oficial", "institucional", "publico", "abierto",
    # Palabras vacías en este contexto
    "datos", "dato", "informacion", "sistema", "plataforma",
    "portal", "servicio", "servicios", "mapa", "mapas",
    "acceso", "consulta", "visualizacion", "descarga",
    "metadatos", "catalogo", "repositorio", "documento",
}

# ── Keywords específicos a CONSERVAR (diferencian recursos) ──
KEEP_SPECIFIC = {
    # Nombres de fuentes/productos propietarios
    "landsat", "sentinel-1", "sentinel-2", "modis", "smap",
    "hansen", "glad", "radd", "dynamicworld", "worldcover",
    "mapbiomas", "soilgrids", "chirps", "era5", "worldclim",
    "chelsa", "srtm", "aster", "gpm", "firms",
    # Instituciones / sistemas propietarios
    "ideam", "igac", "invemar", "dimar", "cioh", "dane", "sgc",
    "upra", "gbif", "ebird", "sib", "faostat", "worldpop",
    "gee", "nasa", "copernicus", "unosat", "arcgis", "qgis",
    # Geografía específica (no genérica)
    "buenaventura", "tumaco", "cartagena", "santa_marta",
    "barranquilla", "leticia", "quibdo", "pasto", "popayan",
    "pacifico", "pacifico_colombiano", "caribe", "caribe_colombiano",
    "amazonia", "orinoquia", "andes", "choco_biogeografico",
    "sierra_nevada", "macizo_colombiano", "catatumbo",
    "rio_magdalena", "rio_cauca", "golfo_uraba", "cienaga_grande",
    # Términos técnicos específicos
    "batimetria", "multihaz", "monohaz", "csar", "s57", "iho",
    "enc", "cartas_nauticas", "mareografos", "tsm",
    "carbono_organico", "densidad_aparente", "cec", "ksat",
    "ndvi", "evi", "nbr", "sar", "lidar", "multiespectral",
    "termal", "radar", "insar", "polinsar",
    "landcover", "lulc", "treecover", "lossyear",
    # Estándares y protocolos
    "wms", "wfs", "wcs", "wmts", "ogc", "stac", "rest",
    "geotiff", "netcdf", "grib", "hdf", "darwin_core",
    # Métodos científicos
    "machine_learning", "random_forest", "clasificacion",
    "segmentacion", "deteccion_cambio", "serie_tiempo",
    "multitemporal", "analisis_espacial", "geoprocesamiento",
}

os.makedirs(BACKUP_DIR, exist_ok=True)

total_removed = 0
total_kept = 0
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
        old_kw = r.get("keywords", [])
        before = len(old_kw)

        # Conservar SOLO keywords específicos, eliminar ruido genérico
        cleaned = [kw for kw in old_kw if kw not in GENERIC_NOISE]
        after = len(cleaned)

        removed = before - after
        if removed > 0:
            r["keywords"] = cleaned
            changed = True
            total_removed += removed
            total_kept += after

    if changed:
        # Backup
        backup_path = os.path.join(BACKUP_DIR, f"kw2_{fname}")
        with open(backup_path, "w", encoding="utf-8") as bf:
            json.dump(data, bf, ensure_ascii=False, indent=2)
        modified += 1

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Corrección de keywords completada:")
print(f"  Fuentes modificadas: {modified}")
print(f"  Keywords genéricos eliminados: {total_removed}")
print(f"  Keywords específicos conservados: {total_kept}")
print(f"  Backups en: {BACKUP_DIR}/kw2_*.json")
print()
print(f"  Estrategia correcta:")
print(f"    ✓ Keywords de recursos = SOLO específicos y diferenciadores")
print(f"    ✓ Sinónimos y expansiones → CURATED_ALIASES (nivel consulta)")
print(f"    ✓ Términos genéricos → GENERIC_KEYWORDS (filtrados del scoring)")
