import json, sys, os, glob
from jsonschema import validate, Draft202012Validator

root = os.path.dirname(os.path.abspath(__file__)) + "/.."
schemas = {
  "city/specs/zone.schema.json": "city/configs/citymap.json",
  "field-layer/data/schema.json": "field-layer/data/sacred_sites.csv"  # optional
}

# simple JSON validate
for schema_path, data_path in schemas.items():
    sp = os.path.join(root, schema_path)
    dp = os.path.join(root, data_path)
    if not os.path.exists(dp): continue
    with open(sp) as f: schema = json.load(f)
    with open(dp) as f: data = json.load(f)
    Draft202012Validator(schema).validate(data)
print("Schemas OK")
