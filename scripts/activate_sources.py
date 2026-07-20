"""
Activa / degrada fuentes del catálogo JSON (solo campo status).

No modifica Python ni registry.py.

Uso:
  python scripts/activate_sources.py --id nueva-fuente
  python scripts/activate_sources.py --all-validated
  python scripts/activate_sources.py --demote ideam --to draft
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES_DIR = ROOT / "catalog" / "sources"
VALIDATE = ROOT / "scripts" / "validate_catalog.py"

ALLOWED = frozenset({"draft", "validated", "active"})
TRANSITIONS = {
    ("draft", "validated"),
    ("validated", "active"),
    ("draft", "active"),  # permitido solo si validación limpia
}


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _save(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _find(source_id: str) -> Path | None:
    direct = SOURCES_DIR / f"{source_id}.json"
    if direct.is_file():
        return direct
    for path in SOURCES_DIR.glob("*.json"):
        data = _load(path)
        if str(data.get("id") or "").lower() == source_id.lower():
            return path
    return None


def _run_validate() -> int:
    return subprocess.call([sys.executable, str(VALIDATE)], cwd=str(ROOT))


def _set_status(path: Path, new_status: str, *, force: bool = False) -> None:
    payload = _load(path)
    old = str(payload.get("status") or "draft").lower()
    new_status = new_status.lower()
    if new_status not in ALLOWED:
        raise SystemExit(f"status inválido: {new_status}")
    if old == new_status:
        print(f"{payload.get('id')}: ya está en {new_status}")
        return
    if new_status == "draft" and old == "active" and not force:
        # demote explícito usa --demote que pasa force
        pass
    if (old, new_status) not in TRANSITIONS and not (
        old == "active" and new_status == "draft" and force
    ):
        raise SystemExit(f"transición no permitida: {old} → {new_status}")
    payload["status"] = new_status
    payload["status_updated_at"] = datetime.now(timezone.utc).isoformat()
    _save(path, payload)
    print(f"{payload.get('id')}: {old} → {new_status}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Activación de fuentes del catálogo JSON")
    parser.add_argument("--id", help="Activar una fuente validated → active")
    parser.add_argument(
        "--all-validated",
        action="store_true",
        help="Activar todas las fuentes en status=validated",
    )
    parser.add_argument("--demote", help="Fuente a degradar a draft (acción humana explícita)")
    parser.add_argument("--to", default="draft", help="Estado destino con --demote (default draft)")
    parser.add_argument(
        "--skip-validate",
        action="store_true",
        help="No re-ejecutar validate_catalog al final",
    )
    args = parser.parse_args()

    if not SOURCES_DIR.is_dir():
        print(f"FATAL: no existe {SOURCES_DIR}", file=sys.stderr)
        return 2

    if args.demote:
        path = _find(args.demote)
        if path is None:
            print(f"FATAL: fuente no encontrada: {args.demote}", file=sys.stderr)
            return 2
        _set_status(path, args.to, force=True)
    elif args.all_validated:
        for path in sorted(SOURCES_DIR.glob("*.json")):
            data = _load(path)
            if str(data.get("status") or "").lower() == "validated":
                # draft→active vía validated; aquí validated→active
                _set_status(path, "active", force=False)
    elif args.id:
        path = _find(args.id)
        if path is None:
            print(f"FATAL: fuente no encontrada: {args.id}", file=sys.stderr)
            return 2
        data = _load(path)
        current = str(data.get("status") or "draft").lower()
        if current == "draft":
            _set_status(path, "validated", force=False)
            # re-validate then active
            code = _run_validate()
            if code != 0:
                print("Activación abortada: catálogo inválido tras validated", file=sys.stderr)
                return code
            _set_status(path, "active", force=False)
        elif current == "validated":
            _set_status(path, "active", force=False)
        else:
            print(f"{args.id}: status actual={current}; nada que activar")
    else:
        parser.print_help()
        return 2

    if not args.skip_validate:
        return _run_validate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
