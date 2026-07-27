"""
Corrección de URLs rotas en el catálogo.
Regla: si la URL específica da 404 o DNS error, usar la URL principal
de la fuente (verificada) o la URL de un recurso padre funcional.
"""

import json, os

CATALOG_DIR = os.path.join(os.path.dirname(__file__), "..", "catalog", "sources")

FIXES = {
    # ── DIMAR / CIOH (404s + DNS) ──
    "cioh.json": {
        "url": "https://www.dimar.mil.co",
        "resources": {
            "cioh:oceanografia-operacional": {"url": "https://www.dimar.mil.co"},
            "cioh:meteorologia-marina": {"url": "https://www.dimar.mil.co", "endpoints": [
                {"method": "portal", "url": "https://www.dimar.mil.co", "label": "DIMAR - Meteorologia Marina"}
            ]},
            "cioh:mareas": {"url": "https://www.dimar.mil.co", "endpoints": [
                {"method": "portal", "url": "https://www.dimar.mil.co", "label": "DIMAR - Pronosticos de Marea"}
            ]},
            "cioh:avisos-navegantes": {"url": "https://www.dimar.mil.co", "endpoints": [
                {"method": "portal", "url": "https://www.dimar.mil.co", "label": "DIMAR - Avisos a Navegantes"}
            ]},
            "cioh:batimetria-caribe": {"url": "https://www.dimar.mil.co"},
        }
    },
    "dimar.json": {
        "resources": {
            "dimar:cartas-nauticas": {"url": "https://www.dimar.mil.co", "endpoints": [
                {"method": "portal", "url": "https://www.dimar.mil.co", "label": "DIMAR - Cartografia Nautica"}
            ]},
            "dimar:batimetria": {"url": "https://www.dimar.mil.co", "endpoints": [
                {"method": "portal", "url": "https://www.dimar.mil.co", "label": "DIMAR - Datos Batimetricos"}
            ]},
            "dimar:senalizacion-maritima": {"url": "https://www.dimar.mil.co", "endpoints": [
                {"method": "portal", "url": "https://www.dimar.mil.co", "label": "DIMAR - Senalizacion Maritima"}
            ]},
            "dimar:cecoldodigital": {"url": "https://www.dimar.mil.co", "endpoints": [
                {"method": "portal", "url": "https://www.dimar.mil.co", "label": "DIMAR - Cecoldo"}
            ]},
        }
    },
    # ── eBird (404s) ──
    "ebird.json": {
        "resources": {
            "ebird:observations": {"url": "https://ebird.org/explore", "endpoints": [
                {"method": "portal", "url": "https://ebird.org/explore", "label": "eBird Explore"},
                {"method": "download", "url": "https://ebird.org/data/download", "label": "eBird Data Download"}
            ]},
            "ebird:hotspots": {"url": "https://ebird.org/hotspots", "endpoints": [
                {"method": "portal", "url": "https://ebird.org/hotspots", "label": "eBird Hotspots"}
            ]},
            "ebird:status-trends": {"url": "https://science.ebird.org/en/status-and-trends", "endpoints": [
                {"method": "portal", "url": "https://science.ebird.org/en/status-and-trends", "label": "eBird Status & Trends"}
            ]},
        }
    },
    # ── ANI ──
    "ani.json": {
        "resources": {
            "ani:fichas-portuarias": {"url": "https://www.ani.gov.co", "endpoints": [
                {"method": "portal", "url": "https://www.ani.gov.co", "label": "ANI - Fichas Portuarias"}
            ]},
        }
    },
    # ── CATIE ──
    "catie.json": {
        "resources": {
            "catie:cuencas": {"url": "https://www.catie.ac.cr", "endpoints": [
                {"method": "portal", "url": "https://www.catie.ac.cr", "label": "CATIE - Cuencas"}
            ]},
            "catie:clima": {"url": "https://www.catie.ac.cr", "endpoints": [
                {"method": "portal", "url": "https://www.catie.ac.cr", "label": "CATIE - Cambio Climatico"}
            ]},
        }
    },
    # ── Copernicus S5P (DNS) ──
    "copernicus.json": {
        "resources": {
            "copernicus:sentinel5p": {"url": "https://www.copernicus.eu", "endpoints": [
                {"method": "portal", "url": "https://www.copernicus.eu", "label": "Copernicus - Sentinel-5P"}
            ]},
        }
    },
    # ── INVEMAR (DNS) ──
    "invemar.json": {
        "resources": {
            "invemar:siam": {"url": "https://www.invemar.org.co", "endpoints": [
                {"method": "portal", "url": "https://www.invemar.org.co", "label": "INVEMAR - SIAM"}
            ]},
        }
    },
    # ── SiB Colombia (DNS) ──
    "sib_colombia.json": {
        "resources": {
            "sib_colombia:api": {"url": "https://sibcolombia.net", "endpoints": [
                {"method": "portal", "url": "https://sibcolombia.net", "label": "SiB Colombia - API"}
            ]},
        }
    },
    # ── World Bank ──
    "world_bank.json": {
        "resources": {
            "world_bank:wdi": {"url": "https://data.worldbank.org", "endpoints": [
                {"method": "portal", "url": "https://data.worldbank.org", "label": "World Bank DataBank"}
            ]},
        }
    },
    # ── GEE (404) ──
    "gee.json": {
        "resources": {
            "gee:chirps-monthly": {"url": "https://developers.google.com/earth-engine/datasets", "endpoints": [
                {"method": "portal", "url": "https://developers.google.com/earth-engine/datasets", "label": "Earth Engine Data Catalog"}
            ]},
        }
    },
    # ── IDEAM (6 URLs rotas) ──
    "ideam.json": {
        "resources": {
            "ideam:tematicas": {"url": "http://www.ideam.gov.co", "endpoints": [
                {"method": "portal", "url": "http://www.ideam.gov.co", "label": "IDEAM - Tematicas"}
            ]},
            "ideam:sivirtual": {"url": "http://www.ideam.gov.co", "endpoints": [
                {"method": "portal", "url": "http://www.ideam.gov.co", "label": "IDEAM - SIVIRTUAL"}
            ]},
            "ideam:siac": {"url": "http://www.siac.gov.co", "endpoints": [
                {"method": "portal", "url": "http://www.siac.gov.co", "label": "SIAC"}
            ]},
            "ideam:redes-hidrologicas": {"url": "http://www.ideam.gov.co", "endpoints": [
                {"method": "portal", "url": "http://www.ideam.gov.co", "label": "IDEAM - Redes Hidrologicas"}
            ]},
            "ideam:servicio-alerta": {"url": "http://www.ideam.gov.co", "endpoints": [
                {"method": "portal", "url": "http://www.ideam.gov.co", "label": "IDEAM - Servicio de Alerta"}
            ]},
            "ideam:consulta-meteorologica": {"url": "http://www.ideam.gov.co", "endpoints": [
                {"method": "portal", "url": "http://www.ideam.gov.co", "label": "IDEAM - Consulta Meteorologica"}
            ]},
        }
    },
    # ── GBIF (403 bloquea bots, OK para humanos) ──
    # No cambiar, solo marcar como verificado
    # ── INVIAS (timeout) ──
    "invias.json": {
        "resources": {
            "invias:vulnerabilidad-faunistica": {"url": "https://www.invias.gov.co", "endpoints": [
                {"method": "portal", "url": "https://www.invias.gov.co", "label": "INVIAS - Vulnerabilidad Faunistica"}
            ]},
        }
    },
}

fixed_sources = 0
fixed_resources = 0

for fname, fix_data in FIXES.items():
    path = os.path.join(CATALOG_DIR, fname)
    if not os.path.exists(path):
        print(f"  ⚠ {fname} no existe, saltando")
        continue

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    sid = data["id"]
    changed = False

    if "url" in fix_data:
        old_url = data.get("url", "")
        new_url = fix_data["url"]
        if old_url != new_url:
            data["url"] = new_url
            print(f"  {sid}: url principal → {new_url}")
            fixed_sources += 1
            changed = True

    for r in data.get("resources", []):
        rid = r["id"]
        rfix = fix_data.get("resources", {}).get(rid, {})
        if not rfix:
            continue
        if "url" in rfix and r.get("url") != rfix["url"]:
            r["url"] = rfix["url"]
            changed = True
        if "endpoints" in rfix:
            r["endpoints"] = rfix["endpoints"]
            changed = True
        if changed:
            print(f"    {rid}: corregido")
            fixed_resources += 1

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

print()
print(f"Corregido: {fixed_sources} fuentes, {fixed_resources} recursos")
print("GBIF: sin cambios (403 = bloquea bots, OK para humanos)")
print("World Bank climate: sin cambios (403 = bloquea HEAD, OK para humanos)")
