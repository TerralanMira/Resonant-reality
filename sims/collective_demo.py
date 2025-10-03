# sims/collective_demo.py
"""
Collective Multi-Zone Simulation
- Aggregates human resonance (κ, γ, χ) into multiple city zones over time.
- Uses adapters.human_to_city to map person->zone deltas.
- Optional read of conductor/pulses/collective_lock.json to set decay/grace.
- Logs per-step metrics to CSV/JSON for easy comparison.

Run:
  python -m sims.collective_demo --scenario coherent --steps 240 --export csv,json --outdir out/collective
"""
from __future__ import annotations
import argparse, json, math, os, random
from adapters.human_to_city import node_influence_from_human
from sims.analysis_utils import to_csv, to_json, summarize_time_series, ensure_dir

# --------- Cohorts (examples) ----------
BASELINE = [
    {"kappa": 0.44, "gamma": 0.50, "chi": 0.42},
    {"kappa": 0.52, "gamma": 0.54, "chi": 0.48},
    {"kappa": 0.47, "gamma": 0.49, "chi": 0.44},
]
COHERENT = [
    {"kappa": 0.70, "gamma": 0.78, "chi": 0.55},
    {"kappa": 0.68, "gamma": 0.74, "chi": 0.58},
    {"kappa": 0.73, "gamma": 0.80, "chi": 0.60},
]
MIXED = [
    {"kappa": 0.30, "gamma": 0.40, "chi": 0.35},
    {"kappa": 0.71, "gamma": 0.77, "chi": 0.55},
    {"kappa": 0.62, "gamma": 0.58, "chi": 0.60},
    {"kappa": 0.49, "gamma": 0.52, "chi": 0.46},
]

# --------- Zones (toy grid) ----------
def default_zones():
    # hearth is stable anchor, plaza is social hub, wild is high entropy edge
    return {
        "hearth": {"coherence": 0.60, "noise": 0.30, "coupling": 0.55},
        "plaza":  {"coherence": 0.50, "noise": 0.40, "coupling": 0.60},
        "wild":   {"coherence": 0.40, "noise": 0.50, "coupling": 0.50},
    }

def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return lo if x < lo else hi if x > hi else x

def load_collective_lock(path: str = "conductor/pulses/collective_lock.json") -> dict:
    if not os.path.exists(path):
        # sensible defaults if lock is absent
        return {
            "stability": {"entropy_threshold": 0.14, "coherence_window": 0.75, "grace_factor": 0.20},
            "calibration": {"baseline_frequency_hz": 7.83}
        }
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def zone_decay_and_noise(zone: dict, grace: float, step: int, baseline_f: float) -> dict:
    # mild natural decay toward midline; little noise proportional to "wildness" (=noise)
    decay = 0.0025 * (1.0 - grace)  # more grace -> less decay
    # periodic background modulation (like day-night / Schumann beat)
    mod = 0.01 * math.sin(2 * math.pi * baseline_f * (step / 240.0))
    zone["coherence"] = clamp(zone["coherence"] - decay + mod)
    zone["noise"]     = clamp(zone["noise"] + decay/2 - mod/2)
    zone["coupling"]  = clamp(zone["coupling"] - decay/3 + mod/3)
    # small stochastic perturbation scaled by current noise
    jitter = 0.01 * zone["noise"]
    zone["coherence"] = clamp(zone["coherence"] + random.uniform(-jitter, jitter))
    zone["noise"]     = clamp(zone["noise"]     + random.uniform(-jitter, jitter))
    zone["coupling"]  = clamp(zone["coupling"]  + random.uniform(-jitter, jitter))
    return zone

def apply_cohort_to_zone(zone: dict, cohort: list[dict]) -> dict:
    # sum small influences from all humans
    c_delta = n_delta = g_delta = 0.0
    for h in cohort:
        d = node_influence_from_human(h["kappa"], h["gamma"], h["chi"])
        c_delta += d["zone_coherence_delta"]
        n_delta += d["noise_reduction_delta"]
        g_delta += d["coupling_gain_delta"]
    zone["coherence"] = clamp(zone["coherence"] + c_delta)
    zone["noise"]     = clamp(zone["noise"] - n_delta)
    zone["coupling"]  = clamp(zone["coupling"] + g_delta)
    return zone

def step_system(zones: dict, cohorts: dict[str, list[dict]], step: int, lock: dict) -> dict:
    grace = float(lock.get("stability", {}).get("grace_factor", 0.20))
    baseline_f = float(lock.get("calibration", {}).get("baseline_frequency_hz", 7.83))
    # natural dynamics first
    for z in zones:
        zones[z] = zone_decay_and_noise(zones[z], grace, step, baseline_f)
    # apply human influences
    if "hearth" in zones and "hearth" in cohorts:
        zones["hearth"] = apply_cohort_to_zone(zones["hearth"], cohorts["hearth"])
    if "plaza" in zones and "plaza" in cohorts:
        zones["plaza"]  = apply_cohort_to_zone(zones["plaza"], cohorts["plaza"])
    if "wild" in zones and "wild" in cohorts:
        zones["wild"]   = apply_cohort_to_zone(zones["wild"], cohorts["wild"])
    return zones

def choose_cohort(name: str) -> list[dict]:
    return {"baseline": BASELINE, "coherent": COHERENT, "mixed": MIXED}.get(name, BASELINE)

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", type=str, default="coherent", choices=["baseline","coherent","mixed","custom"],
                    help="Which cohort to apply to plaza; hearth defaults to baseline, wild to mixed")
    ap.add_argument("--steps", type=int, default=240)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--export", type=str, default="json,csv", help="Comma list: json,csv")
    ap.add_argument("--outdir", type=str, default="out/collective")
    ap.add_argument("--lock", type=str, default="conductor/pulses/collective_lock.json")
    ap.add_argument("--custom_path", type=str, default="", help="Path to custom cohort JSON (list of {kappa,gamma,chi})")
    return ap.parse_args()

def main():
    args = parse_args()
    random.seed(args.seed)
    lock = load_collective_lock(args.lock)

    # Build zones and cohorts
    zones = default_zones()
    hearth_cohort = choose_cohort("baseline")
    wild_cohort   = choose_cohort("mixed")

    if args.scenario == "custom" and args.custom_path and os.path.exists(args.custom_path):
        with open(args.custom_path, "r", encoding="utf-8") as f:
            plaza_cohort = json.load(f)
    else:
        plaza_cohort = choose_cohort(args.scenario)

    cohorts = {"hearth": hearth_cohort, "plaza": plaza_cohort, "wild": wild_cohort}

    # Sim loop
    series = []
    for step in range(args.steps):
        zones = step_system(zones, cohorts, step, lock)
        series.append({
            "step": step,
            "hearth_coherence": zones["hearth"]["coherence"],
            "hearth_noise": zones["hearth"]["noise"],
            "hearth_coupling": zones["hearth"]["coupling"],
            "plaza_coherence": zones["plaza"]["coherence"],
            "plaza_noise": zones["plaza"]["noise"],
            "plaza_coupling": zones["plaza"]["coupling"],
            "wild_coherence": zones["wild"]["coherence"],
            "wild_noise": zones["wild"]["noise"],
            "wild_coupling": zones["wild"]["coupling"],
        })

    # Summaries
    summaries = {
        "hearth": summarize_time_series(series, ["hearth_coherence","hearth_noise","hearth_coupling"]),
        "plaza":  summarize_time_series(series, ["plaza_coherence","plaza_noise","plaza_coupling"]),
        "wild":   summarize_time_series(series, ["wild_coherence","wild_noise","wild_coupling"]),
        "lock_used": lock
    }

    # Exports
    ensure_dir(args.outdir)
    exts = {e.strip().lower() for e in args.export.split(",") if e.strip()}
    if "json" in exts:
        to_json({"series": series, "summaries": summaries}, os.path.join(args.outdir, "collective_results.json"))
    if "csv" in exts:
        to_csv(series, os.path.join(args.outdir, "collective_series.csv"))

    # Console print (concise)
    print(json.dumps({"summaries": summaries}, indent=2))

if __name__ == "__main__":
    main()
