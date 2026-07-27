"""Verificar que los scores ahora tienen spread (no todos 100)."""
from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)

queries = [
    ("clima del pacifico colombiano", "Pacifico"),
    ("cambio coberturas bahia buenaventura", "Buenaventura"),
    ("morfometria cuenca rio Dagua DEM", "Dagua"),
    ("biodiversidad amazonia", "Amazonia"),
]

for q, label in queries:
    r = client.get("/recommend", params={"q": q, "limit": 6})
    d = r.json()
    scores = [rec["score"] for rec in d.get("recommendations", [])]
    unique = len(set(scores))
    print(f"{label}: {len(scores)} resultados, {unique} scores distintos")
    for i, rec in enumerate(d.get("recommendations", [])[:6]):
        print(f"  {i+1}. {rec['source']:<20s} score={rec['score']:<4d}")
    print()

# Verificar que hay spread
all_same = all(len(set([r["score"] for r in d.get("recommendations", [])])) == 1
               for q, _ in queries
               for d in [client.get("/recommend", params={"q": q, "limit": 6}).json()])
if all_same:
    print("WARNING: All queries still return uniform scores")
else:
    print("OK: Scores now have differentiation")
