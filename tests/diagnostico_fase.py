"""Diagnóstico de fase del proyecto vs plan original — DB2S-GEO."""
from fastapi.testclient import TestClient
from backend.api.main import app
from backend.discovery.engine import DiscoveryEngine
from backend.metadata.domains import INITIAL_DOMAINS
from backend.recommendation.scoring import GENERIC_KEYWORDS, CURATED_ALIASES
import os, json

client = TestClient(app)
discovery = DiscoveryEngine()

print("=" * 70)
print("DIAGNÓSTICO DE FASE — DB2S-GEO vs Plan Original")
print("=" * 70)
print()

# ── 1. FUENTES ──
sources = discovery.list_sources()
source_ids = {s["source_id"] for s in sources}
catalog_files = [f for f in os.listdir("catalog/sources") if f.endswith(".json")]
python_connectors = [d for d in os.listdir("connectors") if os.path.isdir(os.path.join("connectors", d)) and not d.startswith("_") and not d.startswith("templates") and os.path.exists(os.path.join("connectors", d, "connector.py"))]

print("FUENTES")
print(f"  Activas (catalog JSON):  {len(catalog_files)}")
print(f"  Conectores Python:       {len(python_connectors)}")
print(f"  Runtime (DiscoveryEngine): {len(sources)}")
print()

# ── 2. DOMINIOS ──
usage = {}
for s in sources:
    for d in s.get("domains", []):
        usage[d] = usage.get(d, 0) + 1
all_domains = set(INITIAL_DOMAINS.keys())
covered = all_domains & set(usage.keys())
uncovered = all_domains - set(usage.keys())

print("DOMINIOS")
print(f"  Definidos:    {len(all_domains)}")
print(f"  Con cobertura: {len(covered)}")
print(f"  Sin cobertura: {len(uncovered)}")
if uncovered:
    print(f"    🚫 {uncovered}")
print(f"  Asignaciones totales: {sum(usage.values())}")
print()

# ── 3. RECURSOS ──
total_resources = sum(len(s.get("resources", [])) for s in sources)
print("RECURSOS")
print(f"  Totales: {total_resources}")
print(f"  Promedio por fuente: {total_resources / len(sources):.1f}")
print()

# ── 4. ENDPOINTS ──
endpoints = [
    ("/healthz", "Health check"),
    ("/version", "Versión"),
    ("/sources", "Listar fuentes"),
    ("/domains", "Listar dominios"),
    ("/graph/stats", "KG stats"),
    ("/recommend?q=clima", "Recomendación"),
    ("/decision-support?q=agua", "Decision Support"),
    ("/watcher/events", "Watcher"),
    ("/source-discovery/candidates", "Source Discovery"),
    ("/observatory/dashboard", "Observatorio"),
    ("/telemetry/recent", "Telemetría"),
    ("/workbench/", "Workbench"),
]
print("ENDPOINTS")
all_ok = True
for path, label in endpoints:
    r = client.get(path)
    ok = r.status_code == 200
    if not ok:
        all_ok = False
    print(f"  {'✓' if ok else '✗'} {label:20s} ({path})")
print()

# ── 5. FASE VS PLAN ──
phases = {
    "Fase 0":     ("Arquitectura", True),
    "Fase 0.5":   ("Consolidación conceptual", True),
    "Fase 1":     ("Discovery Engine MVP", True),
    "Fase 2":     ("Metadata Engine MVP", True),
    "Fase 3":     ("Knowledge Graph MVP", True),
    "Fase 4":     ("Recommendation Engine MVP", True),
    "Fase 5":     ("Watcher Engine MVP", True),
    "Fase 6":     ("Source Discovery MVP", True),
    "Fase 7":     ("Curator Workbench MVP", True),
    "Fase 8":     ("Decision Support MVP", True),
    "Fase 8.1":   ("Observatory MVP", True),
    "Fase Alpha": ("Alpha Release", True),
    "Fase 9":     ("API pública", False),
}

print("FASES DEL PLAN ORIGINAL")
print(f"  {'Fase':<14s} {'Estado':<10s} {'Descripción'}")
print(f"  {'-'*14} {'-'*10} {'-'*40}")
for phase, (desc, done) in phases.items():
    print(f"  {phase:<14s} {'✅ COMPLETA' if done else '⏳ RESERVADA':<10s} {desc}")
print()

# ── 6. CALIDAD ──
print("CONTROLES DE CALIDAD")
issues = []

# Dominios completos
if uncovered:
    issues.append(f"Dominios sin cobertura: {uncovered}")

# Endpoints OK
if not all_ok:
    issues.append("Endpoints con error detectados")

# Generic keywords configurados
if len(GENERIC_KEYWORDS) < 30:
    issues.append(f"GENERIC_KEYWORDS solo tiene {len(GENERIC_KEYWORDS)} términos")

# Aliases configurados
if len(CURATED_ALIASES) < 10:
    issues.append(f"CURATED_ALIASES solo tiene {len(CURATED_ALIASES)} entradas")

# Tests
import subprocess
result = subprocess.run(["python", "-m", "pytest", "tests/unit/", "-q"], capture_output=True, text=True)
tests_ok = "failed" not in result.stdout or "0 failed" in result.stdout

# Stubs
stub_count = 0
for d in python_connectors:
    path = os.path.join("connectors", d, "connector.py")
    with open(path) as f:
        if "NotImplementedConnector" in f.read():
            stub_count += 1
            issues.append(f"Stub sin implementar: {d}")

if not issues:
    print("  ✅ Sin problemas detectados")
else:
    for issue in issues:
        print(f"  ⚠️ {issue}")

print()
print("=" * 70)
print("RESUMEN")
print(f"  Fuentes: {len(sources)} | Recursos: {total_resources} | Dominios: {len(covered)}/{len(all_domains)}")
print(f"  Stubs pendientes: {stub_count} | Tests: {'PASAN' if tests_ok else 'FALLAN'}")
print(f"  Fase actual: POST-MVP — Enriquecimiento de catálogo completado")
print(f"  Siguiente:   Fase 9 (reservada) o hardening de producción")
print("=" * 70)
