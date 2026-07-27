"""Simulación: morfometría de la cuenca del río Dagua con DEM."""
from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)
Q = "morfometria cuenca rio Dagua DEM"

print("=" * 70)
print('SIMULACIÓN: "Quiero saber cómo es la morfometría de la')
print('           cuenca del río Dagua con un DEM"')
print("=" * 70)
print()

# 1. Recommend
r = client.get("/recommend", params={"q": Q, "limit": 8})
d = r.json()
print(f"RECOMMEND ENGINE — {d.get('count')} resultados")
print(f"  Tokens: {d.get('tokens', [])[:12]}...")
print()
for i, rec in enumerate(d.get("recommendations", [])):
    src = rec["source"]
    score = rec["score"]
    reason = rec.get("reason", [])[:2]
    resources = rec.get("resources", [])[:3]
    print(f"  {i+1}. {src} (score: {score})")
    print(f"     {', '.join(reason)}")
    print(f"     Recursos: {', '.join(resources)}")
    print()

# 2. Decision Support
r2 = client.get("/decision-support", params={"q": Q, "limit": 6})
ds = r2.json()
print("-" * 70)
print("DECISION SUPPORT:")
print(f"  Intención: {ds.get('intent', '?')}")
print(f"  Necesidad: {ds.get('need', '?')}")
print()
for i, action in enumerate(ds.get("actions", [])[:6]):
    print(f"  {i+1}. {action.get('verb', '?').upper()}: {action.get('what', '?')}")
    print(f"     Fuente: {action.get('source', '?')} | Complejidad: {action.get('complexity', '?')}")
    print()

# 3. Key sources for DEM/morphometry
print("-" * 70)
print("FUENTES CLAVE PARA DEM Y MORFOMETRÍA:")
for sid in ["asf", "igac", "nasa", "gee", "copernicus", "sgc"]:
    r = client.get(f"/sources/{sid}")
    if r.status_code == 200:
        src = r.json()
        print(f"  {sid.upper()}: {src.get('domains', [])} ({len(src.get('resources', []))} recursos)")

print()
print("=" * 70)
print("FIN SIMULACIÓN")
