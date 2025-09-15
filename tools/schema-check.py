#!/usr/bin/env python3
import json
import sys
from pathlib import Path

try:
    # jsonschema is usually present in CI; if not, add it to requirements
    from jsonschema import Draft202012Validator
except ImportError as e:
    print("ERROR: jsonschema is not installed. Add `jsonschema` to requirements or CI env.", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]  # repo root
SCHEMA_PATH = ROOT / "earth" / "specs" / "site.schema.json"
DATA_PATH   = ROOT / "earth" / "data"  / "sites.json"

def load_json(p: Path):
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

def main():
    if not SCHEMA_PATH.exists():
        print(f"ERROR: schema not found: {SCHEMA_PATH}", file=sys.stderr)
        sys.exit(2)
    if not DATA_PATH.exists():
        print(f"ERROR: data not found: {DATA_PATH}", file=sys.stderr)
        sys.exit(2)

    schema = load_json(SCHEMA_PATH)
    data   = load_json(DATA_PATH)

    # Validate the entire array of sites
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)

    if not errors:
        print("OK: earth/data/sites.json validates against earth/specs/site.schema.json")
        # Small summary
        count = len(data) if isinstance(data, list) else 1
        print(f"Sites validated: {count}")
        sys.exit(0)
    else:
        print("VALIDATION ERRORS:")
        for err in errors:
            # Show the array index if present
            loc = list(err.path)
            path_str = "/" + "/".join(str(x) for x in loc) if loc else "(root)"
            print(f"- at {path_str}: {err.message}")
        sys.exit(1)

if __name__ == "__main__":
    main()
