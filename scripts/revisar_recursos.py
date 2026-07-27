"""Revisar dominios a nivel de recurso para cada fuente del catálogo."""
from __future__ import annotations

import json
import os
from collections import defaultdict

CATALOG_DIR = os.path.join(os.path.dirname(__file__), "..", "catalog", "sources")

for fname in sorted(os.listdir(CATALOG_DIR)):
    if not fname.endswith(".json"):
        continue
    path = os.path.join(CATALOG_DIR, fname)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    sid = data.get("id", "?")
    doms = data.get("domains", [])
    resources = data.get("resources", [])

    # Recolectar dominios de todos los recursos
    resource_domains = defaultdict(list)
    for r in resources:
        rid = r.get("id", "?")
        rd = r.get("domains", r.get("primary_domain", []))
        if isinstance(rd, str):
            rd = [rd]
        for d in rd:
            resource_domains[d].append(rid)

    print(f"=== {sid.upper()} ({len(resources)} recursos) ===")
    print(f"  Fuente: {doms}")

    # Dominios en recursos que NO estan en la fuente
    all_res_domains = set(resource_domains.keys())
    extra = all_res_domains - set(doms)
    if extra:
        print(f"  ⚠ Recursos tienen dominios no declarados en fuente: {extra}")

    # Dominios de fuente que NO tienen recursos
    missing = set(doms) - all_res_domains
    if missing:
        print(f"  ⚡ Fuente declara dominios sin recursos: {missing}")

    # Dominios por recurso
    for d, rids in sorted(resource_domains.items()):
        in_source = "✓" if d in doms else "✗"
        print(f"    {in_source} {d}: {len(rids)} recursos")

    if not resources:
        print("    (sin recursos listados)")

    print()
