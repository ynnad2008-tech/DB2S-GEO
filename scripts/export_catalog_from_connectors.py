"""
Exporta conectores Python MVP actuales a catalog/sources/*.json (one-shot / mantenimiento).

Uso (desde raíz del repo):
  python scripts/export_catalog_from_connectors.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.metadata.domains import INITIAL_DOMAINS
from connectors.registry import MVP_CONNECTOR_IDS, build_python_mvp_connectors

OUT = ROOT / "catalog" / "sources"
KNOWN_DOMAINS = frozenset(INITIAL_DOMAINS.keys())


def _canon_domains(domains: list) -> list[str]:
    return [str(d) for d in domains if str(d) in KNOWN_DOMAINS]


def _category(identity: dict) -> str:
    inst = (identity.get("institution") or "").lower()
    sid = identity.get("source_id") or ""
    if sid in {"gbif", "fao", "nasa", "unosat"}:
        return "internacional"
    if sid in {"gee", "gee-copernicus-sentinel2"}:
        return "plataforma"
    if sid in {"worldpop", "mapbiomas"}:
        return "academia" if sid == "worldpop" else "iniciativa"
    if "superintendencia" in inst or "ministerio" in inst or "departamento" in inst:
        return "gobierno"
    return "instituto"


def export_one(conn) -> dict:
    identity = conn.identify()
    sid = identity["source_id"]
    resources_out = []
    for summary in conn.discover():
        rid = summary["resource_id"]
        desc = conn.describe(rid)
        access = conn.access_info(rid)
        if desc.get("status") == "not_found":
            continue
        resources_out.append(
            {
                "id": rid,
                "name": desc.get("title") or summary.get("title") or rid,
                "description": desc.get("description") or summary.get("description") or "",
                "url": access.get("portal_url")
                or desc.get("homepage")
                or identity.get("homepage")
                or "",
                "category": desc.get("type") or summary.get("type") or "dataset",
                "coverage": {
                    "spatial": desc.get("spatial_coverage") or identity.get("country_or_scope") or "Colombia",
                    "temporal": desc.get("temporal_coverage") or "Según publicación de la fuente",
                },
                "domains": _canon_domains(
                    list(desc.get("domains") or summary.get("domains") or [])
                ),
                "keywords": list(desc.get("keywords") or summary.get("keywords") or []),
                "access_methods": list(
                    access.get("access_methods") or desc.get("access_methods") or []
                ),
                "endpoints": list(access.get("endpoints") or []),
                "formats": list(desc.get("formats") or []),
                "documentation_url": access.get("documentation_url") or "",
                "doi": desc.get("doi") or "",
                "citation_reference": "",
            }
        )
        cite = conn.cite(rid)
        if cite and cite.get("status") != "not_found":
            resources_out[-1]["citation_reference"] = cite.get("reference") or ""
            if cite.get("doi"):
                resources_out[-1]["doi"] = cite.get("doi") or ""
            if not resources_out[-1]["doi"]:
                resources_out[-1]["doi"] = cite.get("doi") or ""
    return {
        "id": sid,
        "name": identity.get("source") or sid,
        "description": identity.get("description") or "",
        "url": identity.get("homepage") or "",
        "category": _category(identity),
        "coverage": {
            "spatial": identity.get("country_or_scope") or "Colombia",
            "temporal": "Según publicación de la fuente",
        },
        "status": "active",
        "institution": identity.get("institution") or "",
        "domains": _canon_domains(list(identity.get("domains") or [])),
        "license": identity.get("license") or "",
        "version": identity.get("version") or conn.version,
        "resources": resources_out,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    connectors = build_python_mvp_connectors()
    for sid in MVP_CONNECTOR_IDS:
        conn = connectors[sid]
        payload = export_one(conn)
        path = OUT / f"{sid}.json"
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"wrote {path.name} resources={len(payload['resources'])}")
    print(f"done -> {OUT} ({len(MVP_CONNECTOR_IDS)} sources)")


if __name__ == "__main__":
    main()
