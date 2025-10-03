#!/usr/bin/env python3
"""
Benchmarks collective scenarios across calibration locks.
Runs sims.collective_demo, captures JSON summaries from stdout,
and writes a CSV + JSON leaderboard.

Usage:
  python scripts/bench_collective.py --steps 240 --outdir out/bench --seed 42
"""
from __future__ import annotations
import argparse, csv, json, os, subprocess, sys
from typing import List, Dict

LOCKS = [
    "conductor/pulses/collective_lock.json",
    "conductor/pulses/calibration/res_lock.v1.low_noise.json",
    "conductor/pulses/calibration/res_lock.v1.medium.json",
    "conductor/pulses/calibration/res_lock.v1.high_harmonic.json",
]
SCENARIOS = ["baseline", "coherent", "mixed"]

def run_collective(lock: str, scenario: str, steps: int, seed: int) -> Dict:
    args = [
        "-m", "sims.collective_demo",
        "--scenario", scenario,
        "--steps", str(steps),
        "--export", "json",
        "--outdir", "-",               # discard file exports
        "--lock", lock,
        "--seed", str(seed),
    ]
    proc = subprocess.run([sys.executable] + args, capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout)
    return data.get("summaries", {})

def flatten(prefix: str, d: Dict) -> Dict[str, float]:
    out = {}
    for k, v in d.items():
        if isinstance(v, dict) and all(m in v for m in ("mean","min","max")):
            out[f"{prefix}_{k}_mean"] = v["mean"]
            out[f"{prefix}_{k}_min"] = v["min"]
            out[f"{prefix}_{k}_max"] = v["max"]
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=240)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--outdir", type=str, default="out/bench")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    rows: List[Dict] = []

    for lock in LOCKS:
        for scenario in SCENARIOS:
            summaries = run_collective(lock, scenario, args.steps, args.seed)
            row = {
                "lock": os.path.basename(lock),
                "scenario": scenario,
            }
            row.update(flatten("plaza", summaries.get("plaza", {})))
            row.update(flatten("hearth", summaries.get("hearth", {})))
            row.update(flatten("wild", summaries.get("wild", {})))
            rows.append(row)
            print(f"[bench] {row['lock']} | {scenario} -> plaza_coherence_mean={row.get('plaza_plaza_coherence_mean', row.get('plaza_coherence_mean','?'))}")

    # Write CSV
    csv_path = os.path.join(args.outdir, "bench_results.csv")
    if rows:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)

    # Write JSON
    json_path = os.path.join(args.outdir, "bench_results.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"rows": rows}, f, indent=2)

    print(f"[bench] Wrote {csv_path} and {json_path}")

if __name__ == "__main__":
    main()
