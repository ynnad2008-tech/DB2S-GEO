"""Valida que existan carpetas clave del skeleton DB2S-GEO."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "backend",
    "frontend",
    "datasets",
    "country_profiles",
    "connectors",
    "agents",
    "knowledge_graph",
    "docs",
    "tests",
    "deployment",
    "scripts",
    "README.md",
    "PROJECT_CHARTER.md",
    "ROADMAP.md",
]


def main() -> int:
    missing = [p for p in REQUIRED if not (ROOT / p).exists()]
    if missing:
        print("MISSING:")
        for m in missing:
            print(f"  - {m}")
        return 1
    print("OK — estructura base presente.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())