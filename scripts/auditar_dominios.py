"""Auditoría integral de dominios por fuente — DB2S-GEO."""
from __future__ import annotations

from collections import defaultdict
from backend.discovery.engine import DiscoveryEngine

discovery = DiscoveryEngine()
sources = discovery.list_sources()

# ── Dominios definidos en el sistema ──
from backend.metadata.domains import INITIAL_DOMAINS
ALL_DOMAINS = set(INITIAL_DOMAINS.keys())

print("=" * 70)
print("AUDITORÍA DE DOMINIOS POR FUENTE — DB2S-GEO")
print(f"Fuentes activas: {len(sources)}")
print(f"Dominios definidos: {len(ALL_DOMAINS)}")
print("=" * 70)
print()

usage = defaultdict(int)
domain_sources = defaultdict(list)

for s in sorted(sources, key=lambda x: x["source_id"]):
    sid = s["source_id"]
    doms = s.get("domains", [])
    resources = s.get("resources", [])

    for d in doms:
        usage[d] += 1
        domain_sources[d].append(sid)

    print(f"◆ {sid}  ({len(resources)} recursos)")
    if doms:
        print(f"  Dominios: {', '.join(doms)}")
    else:
        print(f"  ⚠ Dominios: NINGUNO")

    # Recursos agrupados por dominio
    by_domain = defaultdict(list)
    for r in resources:
        pd = r.get("primary_domain") or r.get("domain") or "sin_dominio"
        by_domain[pd].append(r.get("resource_id", "?"))

    for d, rids in sorted(by_domain.items()):
        print(f"    └ {d}: {len(rids)} recursos")
    if not resources:
        print(f"    └ sin recursos listados")
    print()

# ── Resumen: dominios sin cobertura ──
print("=" * 70)
print("RESUMEN DE COBERTURA")
print("=" * 70)
print()
print(f"{'Dominio':<24s} {'Fuentes':>7s}  {'Cobertura'}")
print("-" * 50)
for d_id in sorted(ALL_DOMAINS):
    d_info = INITIAL_DOMAINS[d_id]
    count = usage.get(d_id, 0)
    bar = "█" * count if count else "·"
    print(f"{d_id:<24s} {count:>7d}  {bar}")

print("-" * 50)
print(f"{'TOTAL':<24s} {sum(usage.values()):>7d} asignaciones")
print()

# ── Fuentes sin dominios ──
no_domains = [s["source_id"] for s in sources if not s.get("domains")]
if no_domains:
    print(f"⚠ Fuentes sin ningún dominio: {', '.join(no_domains)}")
else:
    print("✓ Todas las fuentes tienen al menos un dominio asignado")

# ── Dominios del sistema sin uso ──
unused = ALL_DOMAINS - set(usage.keys())
if unused:
    print(f"⚠ Dominios definidos pero sin uso: {', '.join(sorted(unused))}")
else:
    print("✓ Todos los dominios definidos tienen al menos una fuente")

# ── Propuestas de mejora ──
print()
print("=" * 70)
print("HALLAZGOS")
print("=" * 70)
print()

# SGC sin geologia
if "sgc" in [s["source_id"] for s in sources]:
    sgc = discovery.get_source("sgc")
    if sgc and "geologia" not in sgc.get("domains", []):
        print("🔴 SGC no tiene dominio 'geologia' — DEBERÍA tenerlo")
        print(f"   Actual: {sgc.get('domains')}")

# DIMAR/CIOH sin oceanos_costas
for sid in ["dimar", "cioh"]:
    src = discovery.get_source(sid)
    if src and "oceanos_costas" not in src.get("domains", []):
        print(f"🔴 {sid.upper()} no tiene dominio 'oceanos_costas' — DEBERÍA tenerlo")

# IDEAM
ideam = discovery.get_source("ideam")
if ideam:
    missing = {"clima", "hidrologia", "biodiversidad", "suelos"} - set(ideam.get("domains", []))
    if missing:
        print(f"🟡 IDEAM: podrían faltar dominios — {missing}")

# MAPBIOMAS
mb = discovery.get_source("mapbiomas")
if mb:
    expected = {"observacion_tierra", "biodiversidad", "agricultura", "suelos", "hidrologia"}
    missing = expected - set(mb.get("domains", []))
    if missing:
        print(f"🟡 MapBiomas: podrían faltar dominios — {missing}")

# NASA
nasa = discovery.get_source("nasa")
if nasa:
    expected = {"observacion_tierra", "clima", "suelos", "hidrologia", "biodiversidad"}
    missing = expected - set(nasa.get("domains", []))
    if missing:
        print(f"🟡 NASA: podrían faltar dominios — {missing}")

print()
print("✓ Auditoría completada. Revisar hallazgos arriba.")
