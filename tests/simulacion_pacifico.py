"""Simulación: clima del Pacífico colombiano."""
from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)
Q = "clima del pacifico colombiano"

r = client.get("/recommend", params={"q": Q, "limit": 10})
d = r.json()

print("CONSULTA:", Q)
print("Tokens:", d.get("tokens", []))
print("Total resultados:", d.get("count"))
print()

for i, rec in enumerate(d.get("recommendations", [])):
    src = rec["source"]
    score = rec["score"]
    reason = rec.get("reason", [])[:3]
    keywords = rec.get("keywords", [])[:5]
    resources = rec.get("resources", [])[:3]
    print(f"  {i+1}. {src} (score: {score})")
    print(f"     Razones: {reason}")
    print(f"     Keywords match: {keywords}")
    print(f"     Recursos: {resources}")
    print()

# Ver fuentes clave que DEBERÍAN aparecer
print("-" * 60)
print("Fuentes que deberían aparecer para 'clima + Pacífico':")
expected = ["ideam", "cioh", "dimar", "copernicus", "nasa", "gee"]
for sid in expected:
    r2 = client.get(f"/sources/{sid}")
    if r2.status_code == 200:
        src = r2.json()
        doms = src.get("domains", [])
        n = len(src.get("resources", []))
        print(f"  {sid.upper()}: dominios={doms} ({n} recursos)")
    else:
        print(f"  {sid.upper()}: NO ENCONTRADO")
