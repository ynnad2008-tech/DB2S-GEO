"""Limpiar keywords geograficos de fuentes NACIONALES que no deberian tenerlos."""
import json, os

CAT = "catalog/sources"
GEO_KW = {"buenaventura", "cartagena", "santa_marta", "tumaco",
          "pacifico", "pacifico_colombiano", "choco_biogeografico",
          "caribe", "caribe_colombiano", "barranquilla", "amazonia",
          "amazonas", "leticia", "caqueta", "putumayo", "guaviare",
          "orinoquia", "oriente", "meta", "casanare", "vichada", "arauca"}

# Fuentes NACIONALES (no regionales) cuyos recursos NO deberian tener
# keywords geograficos especificos
NACIONALES = {"ani", "fao", "world_bank", "dnp", "contraloria",
              "ansv", "mintransporte", "superservicios", "supertransporte",
              "dane", "upit", "unosat", "gbif", "worldpop"}

cleaned = 0
for fname in os.listdir(CAT):
    if not fname.endswith(".json"):
        continue
    sid = fname.replace(".json", "")
    if sid not in NACIONALES:
        continue
    path = os.path.join(CAT, fname)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    for r in data.get("resources", []):
        old_kw = set(r.get("keywords", []))
        geo_found = old_kw & GEO_KW
        if geo_found:
            new_kw = sorted(old_kw - GEO_KW)
            r["keywords"] = new_kw
            cleaned += len(geo_found)
            print(f"  {sid}:{r['id']} -{geo_found}")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nKeywords geograficos eliminados: {cleaned} en fuentes nacionales")
print("Estas fuentes son de cobertura NACIONAL, no deben tener keywords regionales.")
