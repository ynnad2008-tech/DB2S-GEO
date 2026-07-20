"""
Valida catalog/sources/*.json y escribe catalog/reports/latest_validation.json.

Exit codes:
  0 OK
  1 Invalid
  2 Fatal error
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.metadata.domains import INITIAL_DOMAINS

SOURCES_DIR = ROOT / "catalog" / "sources"
REPORT_PATH = ROOT / "catalog" / "reports" / "latest_validation.json"
SCHEMA_PATH = ROOT / "catalog" / "schema" / "source.schema.json"

ID_RE = re.compile(r"^[a-z][a-z0-9_-]{1,63}$")
ALLOWED_STATUS = frozenset({"draft", "validated", "active"})
KNOWN_DOMAINS = frozenset(INITIAL_DOMAINS.keys())


def _is_http_url(value: str) -> bool:
    try:
        p = urlparse(value)
        return p.scheme in {"http", "https"} and bool(p.netloc)
    except Exception:
        return False


def validate_source(payload: dict[str, Any], *, filename: str) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    sid = str(payload.get("id") or "").strip().lower()

    for field in ("id", "name", "description", "url", "category", "coverage", "resources", "status"):
        if field not in payload or payload[field] in (None, "", []):
            errors.append(f"campo obligatorio ausente o vacío: {field}")

    if sid and not ID_RE.match(sid):
        errors.append(f"id inválido: {sid}")

    status = str(payload.get("status") or "").strip().lower()
    if status and status not in ALLOWED_STATUS:
        errors.append(f"status inválido: {status}")

    url = str(payload.get("url") or "")
    if url and not _is_http_url(url):
        errors.append(f"url inválida: {url}")

    desc = str(payload.get("description") or "")
    if desc and len(desc) < 80:
        warnings.append("description corta (<80 chars)")

    coverage = payload.get("coverage")
    if isinstance(coverage, dict):
        if not coverage.get("spatial"):
            errors.append("coverage.spatial obligatorio")
        if not coverage.get("temporal"):
            warnings.append("coverage.temporal ausente")
    elif "coverage" in payload:
        errors.append("coverage debe ser objeto")

    domains = payload.get("domains") or []
    if isinstance(domains, list):
        for d in domains:
            if str(d) not in KNOWN_DOMAINS:
                msg = f"dominio desconocido en fuente: {d}"
                if status == "active":
                    errors.append(msg)
                else:
                    warnings.append(msg)

    resources = payload.get("resources")
    if not isinstance(resources, list):
        errors.append("resources debe ser lista")
        resources = []
    elif status in {"validated", "active"} and len(resources) == 0:
        errors.append("resources vacío no permitido para validated/active")

    seen_res: set[str] = set()
    for i, res in enumerate(resources):
        if not isinstance(res, dict):
            errors.append(f"resources[{i}] no es objeto")
            continue
        rid = str(res.get("id") or "").strip()
        prefix = f"resources[{i}]"
        for field in ("id", "name", "description", "url", "category", "coverage"):
            if field not in res or res[field] in (None, ""):
                errors.append(f"{prefix}.{field} obligatorio")
        if rid:
            if rid in seen_res:
                errors.append(f"resource id duplicado: {rid}")
            seen_res.add(rid)
            if sid and not rid.startswith(f"{sid}:"):
                errors.append(f"{prefix}.id debe iniciar con '{sid}:'")
        rurl = str(res.get("url") or "")
        if rurl and not _is_http_url(rurl):
            errors.append(f"{prefix}.url inválida")
        rdesc = str(res.get("description") or "")
        if rdesc and len(rdesc) < 40:
            warnings.append(f"{prefix}.description corta")
        if not (res.get("keywords") or []):
            warnings.append(f"{prefix}.keywords vacías")
        if not (res.get("endpoints") or []):
            warnings.append(f"{prefix}.endpoints vacíos")
        for d in res.get("domains") or []:
            if str(d) not in KNOWN_DOMAINS:
                msg = f"{prefix}.dominio desconocido: {d}"
                if status == "active":
                    errors.append(msg)
                else:
                    warnings.append(msg)

    bucket = "invalid" if errors else status if status in ALLOWED_STATUS else "invalid"
    incomplete = bool(warnings) and not errors
    return {
        "id": sid or filename,
        "file": filename,
        "status": status or "missing",
        "bucket": bucket,
        "incomplete": incomplete,
        "resources": len(resources),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    try:
        if not SOURCES_DIR.is_dir():
            print(f"FATAL: no existe {SOURCES_DIR}", file=sys.stderr)
            return 2

        results: list[dict[str, Any]] = []
        ids: dict[str, str] = {}
        for path in sorted(SOURCES_DIR.glob("*.json")):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except Exception as exc:  # noqa: BLE001
                results.append(
                    {
                        "id": path.stem,
                        "file": path.name,
                        "status": "invalid",
                        "bucket": "invalid",
                        "incomplete": False,
                        "resources": 0,
                        "errors": [f"JSON inválido: {exc}"],
                        "warnings": [],
                    }
                )
                continue
            if not isinstance(payload, dict):
                results.append(
                    {
                        "id": path.stem,
                        "file": path.name,
                        "status": "invalid",
                        "bucket": "invalid",
                        "incomplete": False,
                        "resources": 0,
                        "errors": ["raíz JSON debe ser objeto"],
                        "warnings": [],
                    }
                )
                continue
            row = validate_source(payload, filename=path.name)
            sid = row["id"]
            if sid in ids:
                row["errors"].append(f"id duplicado con archivo {ids[sid]}")
                row["bucket"] = "invalid"
            else:
                ids[sid] = path.name
            results.append(row)

        active = [r for r in results if r["bucket"] == "active"]
        validated = [r for r in results if r["bucket"] == "validated"]
        draft = [r for r in results if r["bucket"] == "draft"]
        invalid = [r for r in results if r["bucket"] == "invalid"]
        incomplete = [r for r in results if r.get("incomplete")]

        report = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "schema": str(SCHEMA_PATH.relative_to(ROOT)) if SCHEMA_PATH.exists() else None,
            "summary": {
                "total": len(results),
                "active": len(active),
                "validated": len(validated),
                "draft": len(draft),
                "invalid": len(invalid),
                "incomplete": len(incomplete),
            },
            "active": [{"id": r["id"], "resources": r["resources"]} for r in active],
            "validated": [{"id": r["id"], "resources": r["resources"]} for r in validated],
            "draft": [{"id": r["id"], "resources": r["resources"]} for r in draft],
            "invalid": [
                {"id": r["id"], "errors": r["errors"]} for r in invalid
            ],
            "incomplete": [
                {"id": r["id"], "warnings": r["warnings"]} for r in incomplete
            ],
            "details": results,
        }

        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        print("=== DB2S-GEO catalog validation ===")
        print(
            f"total={report['summary']['total']} "
            f"active={report['summary']['active']} "
            f"validated={report['summary']['validated']} "
            f"draft={report['summary']['draft']} "
            f"invalid={report['summary']['invalid']} "
            f"incomplete={report['summary']['incomplete']}"
        )
        print(f"report -> {REPORT_PATH}")

        if invalid:
            for row in invalid:
                print(f"INVALID {row['id']}: {'; '.join(row['errors'])}")
            return 1
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
