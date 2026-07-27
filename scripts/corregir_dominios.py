"""
Corrección integral de dominios en el catálogo JSON (25 fuentes).
Regla: source.domains = union de todos los resource.domains.
Excepciones documentadas con justificación.
"""
from __future__ import annotations

import json
import os
import sys

CATALOG_DIR = os.path.join(os.path.dirname(__file__), "..", "catalog", "sources")
BACKUP_DIR = os.path.join(os.path.dirname(__file__), "..", "catalog", "reports")

# ── Correcciones manuales con justificación ──
# Fuentes donde la regla union() no es suficiente porque
# hay recursos que DEBERÍAN tener un dominio pero no lo tienen,
# o dominios fundamentales de la misión institucional.

MANUAL_OVERRIDES = {
    "sgc": {
        "add_to_source": ["geologia"],  # Misión institucional fundamental
        "add_to_resources": {
            "sgc:mapa-geologico": ["geologia"],
            "sgc:amenaza-sismica": ["geologia", "riesgo"],
            "sgc:geoportal": ["geologia"],
        },
        "justification": "SGC es el Servicio Geológico Colombiano. geologia es su dominio misional principal."
    },
    "igac": {
        "add_to_source": ["cartografia_base"],  # Misión institucional — IGAC ES cartografía base
        "justification": "IGAC es la autoridad cartográfica nacional. cartografia_base es su misión fundacional."
    },
    "upra": {
        "add_to_source": ["ordenamiento"],  # UPRA define ordenamiento productivo rural
        "justification": "UPRA planifica el ordenamiento productivo rural. ordenamiento es parte de su misión."
    },
}

os.makedirs(BACKUP_DIR, exist_ok=True)

print("=" * 70)
print("CORRECCIÓN INTEGRAL DE DOMINIOS — DB2S-GEO")
print("=" * 70)
print()

total_fixes = 0

for fname in sorted(os.listdir(CATALOG_DIR)):
    if not fname.endswith(".json"):
        continue

    path = os.path.join(CATALOG_DIR, fname)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    sid = data.get("id", fname.replace(".json", ""))
    resources = data.get("resources", [])
    old_domains = set(data.get("domains", []))

    # ── Calcular dominios correctos: union de resource.domains ──
    resource_domains = set()
    for r in resources:
        rd = r.get("domains", [])
        if isinstance(rd, str):
            rd = [rd]
        resource_domains.update(rd)

    # Aplicar overrides manuales
    override = MANUAL_OVERRIDES.get(sid, {})
    add_src = set(override.get("add_to_source", []))
    add_res = override.get("add_to_resources", {})

    new_domains = resource_domains | add_src

    # ── Aplicar correcciones a recursos ──
    for r in resources:
        rid = r.get("id", "")
        if rid in add_res:
            rd = set(r.get("domains", []))
            rd.update(add_res[rid])
            r["domains"] = sorted(rd)

    # ── Ordenar y guardar ──
    new_domains_list = sorted(new_domains)

    fixes = []
    added = new_domains - old_domains
    removed = old_domains - new_domains

    if added:
        fixes.append("+" + ", ".join(sorted(added)))
    if removed:
        fixes.append("-" + ", ".join(sorted(removed)))
    if override.get("add_to_resources"):
        n_res = sum(len(v) for v in add_res.values())
        fixes.append(f"↳ {n_res} dominios agregados a recursos")

    if not fixes and not override.get("add_to_resources"):
        print(f"  ✓ {sid}: sin cambios ({len(new_domains_list)} dominios)")
        continue

    # ── Backup ──
    backup_path = os.path.join(BACKUP_DIR, fname)
    with open(backup_path, "w", encoding="utf-8") as bf:
        json.dump(data, bf, ensure_ascii=False, indent=2)

    # ── Guardar corregido ──
    data["domains"] = new_domains_list
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"  ◆ {sid}: {old_domains}")
    print(f"     → {new_domains_list}")
    if override.get("justification"):
        print(f"     ⓘ {override['justification']}")
    total_fixes += 1

print()
print(f"Correcciones aplicadas: {total_fixes} fuentes")
print(f"Backups en: {BACKUP_DIR}")
print()
print("✓ Catálogo corregido. Ejecutar tests para verificar.")
