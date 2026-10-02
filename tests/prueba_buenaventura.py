"""Prueba de calidad: cambio de coberturas en Bahía de Buenaventura."""
from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)
Q = "cambio coberturas bahia buenaventura"

print("=" * 70)
print('PRUEBA DE CALIDAD')
print('Consulta: "Quiero evaluar el cambio de coberturas en la región')
print('          de la bahía de Buenaventura"')
print("=" * 70)
print()

# ── 1. RECOMMEND ENGINE ──
r = client.get("/recommend", params={"q": Q, "limit": 8})
data = r.json()
print("RECOMMEND ENGINE — Top 8 resultados:")
print(f"  Total: {data.get('count', 0)} resultados")
print()
for i, item in enumerate(data.get("recommendations", [])[:8]):
    source = item.get("source_id", item.get("source", "?"))
    score = item.get("score", 0)
    why = item.get("reason", [])
    if isinstance(why, str):
        why = [why]
    why_str = "; ".join(why[:2]) if why else "sin justificación"
    print(f"  {i+1}. [{source}] Score: {score}")
    print(f"     {why_str}")
    print()

# ── 2. DECISION SUPPORT ──
r2 = client.get("/decision-support", params={"q": Q, "limit": 6})
ds = r2.json()
print("-" * 70)
print("DECISION SUPPORT:")
print(f"  Intención detectada: {ds.get('intents', '?')}")
print(f"  Necesidad: {ds.get('need', '?')}")
print(f"  Rutas recomendadas ({ds.get('count', 0)}):")
print()
for i, action in enumerate(ds.get("routes", [])[:6]):
    title = action.get("title", "?")
    what = action.get("what_to_do", "?")
    source = action.get("source_id", action.get("source", "?"))
    why = action.get("why", [])
    why = "; ".join(why[:2]) if isinstance(why, list) else why
    print(f"  {i+1}. {title}")
    print(f"     Fuente: {source} | {what[:80]}")
    print(f"     {why}")
    print()

# ── 3. BÚSQUEDA POR DOMINIO ──
print("-" * 70)
print("COBERTURA DE DOMINIOS RELEVANTES:")
for domain in ["oceanos_costas", "observacion_tierra", "biodiversidad", "hidrologia"]:
    r = client.get("/sources", params={"domain": domain})
    d = r.json()
    ids = [s["source_id"] for s in d.get("sources", [])]
    print(f"  {domain}: {d.get('count', 0)} fuentes → {', '.join(ids)}")

# ── 4. FUENTES CLAVE PARA ESTE CASO ──
print("-" * 70)
print("FUENTES CLAVE PARA BAHÍA DE BUENAVENTURA:")
for sid in ["ideam", "invemar", "dimar", "cioh", "mapbiomas", "gee", "nasa"]:
    r = client.get(f"/sources/{sid}")
    if r.status_code == 200:
        src = r.json()
        doms = src.get("domains", [])
        n_res = len(src.get("resources", []))
        print(f"  {sid.upper()}: {doms} ({n_res} recursos)")
    else:
        print(f"  {sid.upper()}: NO ENCONTRADO")

# ── 5. KNOWLEDGE GRAPH ──
print("-" * 70)
r = client.get("/graph/domain/observacion_tierra")
kg = r.json()
resources = kg.get("resources", [])
print(f"  Knowledge Graph — observacion_tierra: {len(resources)} recursos "
      f"→ {', '.join(resources[:15])}{'…' if len(resources) > 15 else ''}")

print()
print("=" * 70)
print("FIN DE LA PRUEBA")
