import os, json, glob, sys
from jsonschema import Draft202012Validator

ROOT = os.path.dirname(os.path.abspath(__file__)) + "/.."

def validate_json(schema_path, data_path):
    with open(schema_path) as f: schema = json.load(f)
    with open(data_path) as f: data = json.load(f)
    Draft202012Validator(schema).validate(data)

# Optional validations; skip silently if files absent
checks = [
  ("city/specs/zone.schema.json", "city/configs/citymap.json"),
]

failed = False
for schema_rel, data_rel in checks:
    sp = os.path.join(ROOT, schema_rel)
    dp = os.path.join(ROOT, data_rel)
    if not (os.path.exists(sp) and os.path.exists(dp)):
        print(f"[schema-check] Skipping (missing): {schema_rel} / {data_rel}")
        continue
    try:
        validate_json(sp, dp)
        print(f"[schema-check] OK: {data_rel}")
    except Exception as e:
        failed = True
        print(f"[schema-check] FAIL {data_rel}: {e}")

sys.exit(1 if failed else 0)
