"""Simulacion: morfometria de una cuenca."""
from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)
queries = [
    "quiero calcular la morfometria de una cuenca",
    "morfometria de cuenca",
]

for q in queries:
    r = client.get("/recommend", params={"q": q, "limit": 8})
    d = r.json()
    print(f"CONSULTA: {q}")
    print(f"Tokens: {d.get('tokens', [])[:15]}...")
    print(f"Resultados: {d.get('count')}")
    print()
    for i, rec in enumerate(d.get("recommendations", [])[:6]):
        print(f"  {i+1}. {rec['source']:<30s} score={rec['score']}")
        print(f"     {rec.get('reason', [])[:3]}")
        print(f"     Recursos: {rec.get('resources', [])[:3]}")
        print()
    print("-" * 60)

# Decision Support
r2 = client.get("/decision-support", params={"q": q, "limit": 6})
ds = r2.json()
print("DECISION SUPPORT:")
print(f"  Intencion: {ds.get('intent', '?')}")
print(f"  Necesidad: {ds.get('need', '?')}")
for i, a in enumerate(ds.get("actions", [])[:4]):
    print(f"  {i+1}. {a.get('verb', '?')}: {a.get('what', '?')}")
    print(f"     Fuente: {a.get('source', '?')} | {a.get('complexity', '?')}")
