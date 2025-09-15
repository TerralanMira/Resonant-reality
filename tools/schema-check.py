#!/usr/bin/env python3
"""
Schema Check — Resonant Reality
Validates JSON/JSON-like data files against JSON Schemas.

- Uses Draft 2020-12
- Prints a clean PASS/FAIL report per pair
- Skips gracefully if a file is missing (does not fail CI)
- Exits 0 only if all checked pairs either PASS or SKIP
- Exits 1 if any pair FAILS validation

Extend the CHECKS list below as new schemas/data are added.
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
# Declare the schema→data pairs you want to validate.
# If a path doesn't exist, it's reported as SKIP (not a failure).
# --------------------------------------------------------------------
CHECKS = [
    # EARTH (array-of-sites schema you just adopted)
    {
        "name": "earth sites",
        "schema": ROOT / "earth" / "specs" / "site.schema.json",
        "data":   ROOT / "earth" / "data"  / "sites.json",
    },

    # CITY (add or adjust these as your repo evolves)
    # Example: citymap config against its schema (rename if your filenames differ)
    {
        "name": "city map",
        "schema": ROOT / "city" / "specs" / "citymap.schema.json",
        "data":   ROOT / "city" / "configs" / "citymap.json",
    },

    # Example: a garden lesson file against a lesson schema
    {
        "name": "garden lesson (candle intro)",
        "schema": ROOT / "city" / "specs" / "garden_lesson.schema.json",
        "data":   ROOT / "city" / "garden_lessons" / "candle_intro.json",
    },

    # Add more pairs here as you introduce schemas:
    # {
    #     "name": "conductor preset",
    #     "schema": ROOT / "conductor" / "specs" / "preset.schema.json",
    #     "data":   ROOT / "conductor" / "presets" / "garden_day.json",
    # },
]

# --------------------------------------------------------------------
def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def validate_pair(name: str, schema_path: Path, data_path: Path) -> str:
    """
    Returns one of: 'PASS', 'FAIL', 'SKIP'
    Prints a concise report line and any errors.
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
        # Helpful tiny summary for arrays/objects
        summary = ""
        if isinstance(data, list):
            summary = f" (items: {len(data)})"
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

    # Fail CI only if any FAIL occurred.
    return 1 if failed > 0 else 0

if __name__ == "__main__":
    sys.exit(main())
