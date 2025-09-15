#!/usr/bin/env python3
"""
Schema Check — Resonant Reality
Validates JSON/JSON-like data files against JSON Schemas.

- Draft 2020-12
- Clear PASS/FAIL/SKIP per pair
- SKIP when a path doesn't exist (doesn't fail CI)
- Exit 1 only if any pair FAILS

Extend CHECKS as new schema/data pairs are added.
"""

from __future__ import annotations
import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print("ERROR: jsonschema is not installed. Add `jsonschema` to requirements or CI env.", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]  # repo root

# --------------------------------------------------------------------
# Declare schema→data pairs here. Edit paths to match your repo.
# --------------------------------------------------------------------
CHECKS = [
    # EARTH — array of sites
    {
        "name": "earth sites",
        "schema": ROOT / "earth" / "specs" / "site.schema.json",
        "data":   ROOT / "earth" / "data"  / "sites.json",
    },

    # CITY — city map config
    {
        "name": "city map",
        "schema": ROOT / "city" / "specs" / "citymap.schema.json",
        "data":   ROOT / "city" / "configs" / "citymap.json",
    },

    # CITY — example lesson (note: lives under city/configs/garden_lessons/)
    {
        "name": "garden lesson (candle intro)",
        "schema": ROOT / "city" / "specs" / "garden_lesson.schema.json",
        "data":   ROOT / "city" / "configs" / "garden_lessons" / "candle_intro.json",
    },

    # Add more pairs as you introduce schemas, e.g.:
    # {
    #     "name": "conductor preset",
    #     "schema": ROOT / "conductor" / "specs" / "preset.schema.json",
    #     "data":   ROOT / "conductor" / "presets" / "garden_day.json",
    # },
]

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def validate_pair(name: str, schema_path: Path, data_path: Path) -> str:
    """
    Returns: 'PASS' | 'FAIL' | 'SKIP'
    Prints a concise report and any errors.
    """
    missing = []
    if not schema_path.exists():
        missing.append(f"schema not found: {schema_path}")
    if not data_path.exists():
        missing.append(f"data not found:   {data_path}")

    if missing:
        print(f"[SKIP] {name}")
        for m in missing:
            print(f"       - {m}")
        return "SKIP"

    try:
        schema = load_json(schema_path)
    except Exception as e:
        print(f"[FAIL] {name} — could not read schema ({schema_path}): {e}")
        return "FAIL"

    try:
        data = load_json(data_path)
    except Exception as e:
        print(f"[FAIL] {name} — could not read data ({data_path}): {e}")
        return "FAIL"

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: (list(e.path), e.message))

    if not errors:
        summary = f" (items: {len(data)})" if isinstance(data, list) else ""
        print(f"[PASS] {name}{summary}")
        return "PASS"

    print(f"[FAIL] {name} — {len(errors)} error(s)")
    for err in errors:
        loc = "/" + "/".join(str(k) for k in err.path) if err.path else "(root)"
        print(f"       at {loc}: {err.message}")
    return "FAIL"

def main() -> int:
    print("== Schema Check ==")
    results = [validate_pair(c["name"], c["schema"], c["data"]) for c in CHECKS]
    failed = results.count("FAIL")
    skipped = results.count("SKIP")
    passed = results.count("PASS")
    print(f"\nSummary: PASS={passed}  SKIP={skipped}  FAIL={failed}")
    return 1 if failed > 0 else 0

if __name__ == "__main__":
    sys.exit(main())
