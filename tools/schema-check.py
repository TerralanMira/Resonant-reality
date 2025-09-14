import os, json, sys
from jsonschema import Draft202012Validator, exceptions as JSE

ROOT = os.path.dirname(os.path.abspath(__file__)) + "/.."
SCHEMA = os.path.join(ROOT, "city/specs/citymap.schema.json")
DATA   = os.path.join(ROOT, "city/configs/citymap.json")

def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    if not os.path.exists(SCHEMA):
        print("[schema-check] Missing schema:", SCHEMA); sys.exit(0)
    if not os.path.exists(DATA):
        print("[schema-check] Missing data:", DATA); sys.exit(0)

    schema = load(SCHEMA)
    data   = load(DATA)

    try:
        Draft202012Validator(schema).validate(data)
        print("[schema-check] OK:", os.path.relpath(DATA, ROOT))
        sys.exit(0)
    except JSE.ValidationError as e:
        path = " → ".join(map(str, list(e.path))) or "(root)"
        print("[schema-check] FAIL:", os.path.relpath(DATA, ROOT))
        print("  at:", path)
        print("  msg:", e.message)
        # Show the failing instance (trim long)
        snippet = e.instance
        try:
            s = json.dumps(snippet, ensure_ascii=False)
            print("  instance:", (s[:300] + "…") if len(s) > 300 else s)
        except Exception:
            pass
        sys.exit(1)

if __name__ == "__main__":
    main()
# Validate citymap schema
with open("city/citymap.schema.json") as f:
    city_schema = json.load(f)

with open("city/citymap.json") as f:
    city_data = json.load(f)

jsonschema.validate(city_data, city_schema)
print("Citymap schema is valid!")

# Validate pulses seed
with open("conductor/pulses/seed.json") as f:
    seed_data = json.load(f)

# (Optional) Add a schema if you want strict validation, or just ensure it’s valid JSON
print("Seed JSON is valid!")
