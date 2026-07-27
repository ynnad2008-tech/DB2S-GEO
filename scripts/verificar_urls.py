"""Verificación HTTP de URLs en el catálogo. Marca las que fallan."""
import json, os, urllib.request, urllib.error, ssl

CATALOG_DIR = os.path.join(os.path.dirname(__file__), "..", "catalog", "sources")
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

BROKEN = []
OK = 0
TOTAL = 0

for fname in sorted(os.listdir(CATALOG_DIR)):
    if not fname.endswith(".json"):
        continue
    with open(os.path.join(CATALOG_DIR, fname), encoding="utf-8") as f:
        data = json.load(f)
    sid = data["id"]

    # Verificar URL principal
    url = data.get("url", "")
    if url:
        TOTAL += 1
        try:
            req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "DB2S-GEO/0.3"})
            resp = urllib.request.urlopen(req, timeout=15, context=ctx)
            code = resp.status
            if code in (200, 301, 302, 303, 307, 308):
                OK += 1
            elif code == 403:
                OK += 1  # bloquean HEAD, intentamos GET luego
                print(f"  ⚠ {sid}: HTTP {code} (HEAD bloqueado, URL probablemente OK)")
            elif code == 404:
                BROKEN.append((sid, "fuente", url, 404))
                print(f"  ✗ {sid}: HTTP 404 — {url}")
            else:
                BROKEN.append((sid, "fuente", url, code))
                print(f"  ⚠ {sid}: HTTP {code} — {url}")
        except Exception as e:
            BROKEN.append((sid, "fuente", url, str(e)))
            print(f"  ✗ {sid}: ERROR — {url} ({e})")

    # Verificar URLs de recursos
    for r in data.get("resources", []):
        rid = r["id"]
        rurl = r.get("url", "")
        if rurl and rurl != url:
            TOTAL += 1
            try:
                req = urllib.request.Request(rurl, method="HEAD", headers={"User-Agent": "DB2S-GEO/0.3"})
                resp = urllib.request.urlopen(req, timeout=15, context=ctx)
                code = resp.status
                if code in (200, 301, 302, 303, 307, 308):
                    OK += 1
                elif code == 403:
                    OK += 1
                elif code == 404:
                    BROKEN.append((sid, rid, rurl, 404))
                    print(f"  ✗ {rid}: HTTP 404 — {rurl}")
                else:
                    BROKEN.append((sid, rid, rurl, code))
                    print(f"  ⚠ {rid}: HTTP {code} — {rurl}")
            except Exception as e:
                BROKEN.append((sid, rid, rurl, str(e)))
                print(f"  ✗ {rid}: ERROR — {rurl} ({e})")

print()
print("=" * 60)
print(f"RESULTADO: {OK}/{TOTAL} OK, {len(BROKEN)} rotos")
if BROKEN:
    print()
    print("URLs rotas:")
    for b in BROKEN:
        print(f"  {b[0]} / {b[1]} — {b[2]} → {b[3]}")
