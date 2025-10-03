# sims/analysis_utils.py
from __future__ import annotations
import csv, json, os
from statistics import mean

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def to_csv(rows: list[dict], out_path: str) -> None:
    ensure_dir(os.path.dirname(out_path) or ".")
    if not rows: return
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

def to_json(obj, out_path: str, indent: int = 2) -> None:
    ensure_dir(os.path.dirname(out_path) or ".")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=indent)

def summarize_time_series(rows: list[dict], keys: list[str]) -> dict:
    if not rows: return {}
    out = {}
    for k in keys:
        vals = [float(r[k]) for r in rows if k in r]
        out[k] = {"mean": round(mean(vals), 6), "min": round(min(vals), 6), "max": round(max(vals), 6)}
    return out
