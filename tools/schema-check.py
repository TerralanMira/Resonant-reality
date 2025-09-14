import os, json, sys
from jsonschema import Draft202012Validator, exceptions as JSE

ROOT = os.path.dirname(os.path.abspath(__file__)) + "/.."

def validate_pair(schema_rel, data_rel):
    sp = os.path.join(ROOT, schema_rel)
    dp = os.path.join(ROOT, data_rel)
    if not (os.path.exists(sp) and os.path.exists(dp)):
        print(f"[schema-check] Skipping (missing): {schema_rel} / {data_rel}")
        return True
    try:
        with open(sp) as f: schema = json.load(f)
        with open(dp) as f: data = json.load(f)
        Draft202012Validator(schema).validate(data)
        print(f"[schema-check] OK: {data_rel}")
        return True
    except JSE.ValidationError as e:
        print(f"[schema-check] FAIL: {data_rel}")
        # Pinpoint path & message
        loc = " → ".join([str(p) for p in list(e.path)])
        print(f"  at: {loc or '(root)'}")
        print(f"  msg: {e.message}")
        # show a tiny snippet of the instance that failed
        try:
            import json as _j
            print("  instance:", _j.dumps(e.instance, ensure_ascii=False)[:300])
        except Exception:
            pass
        return False

checks = [
    ("city/specs/citymap.schema.json", "city/configs/citymap.json"),
]

ok = all(validate_pair(*c) for c in checks)
sys.exit(0 if ok else 1)
