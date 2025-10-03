# sims/city_coupling_demo.py
"""
City Coupling Demo
Aggregates human resonance (κ, γ, χ) into a city 'plaza' node.
- coherence ↑ with human κ/γ/χ
- noise ↓ with human κ/γ/χ
- coupling ↑ with human κ/γ/χ
Safe: no external files required.
"""
from __future__ import annotations
import json
from adapters.human_to_city import node_influence_from_human

def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return lo if x < lo else hi if x > hi else x

def apply_influence(zone: dict, deltas: dict) -> dict:
    zone["coherence"] = clamp(zone["coherence"] + deltas["zone_coherence_delta"])
    zone["noise"]     = clamp(zone["noise"] - deltas["noise_reduction_delta"])
    zone["coupling"]  = clamp(zone["coupling"] + deltas["coupling_gain_delta"])
    return zone

def simulate_city(humans: list[dict]) -> dict:
    zones = {"plaza": {"coherence": 0.50, "noise": 0.40, "coupling": 0.60}}
    for h in humans:
        deltas = node_influence_from_human(h["kappa"], h["gamma"], h["chi"])
        zones["plaza"] = apply_influence(zones["plaza"], deltas)
    return zones

def scenario(name: str, cohort: list[dict]) -> dict:
    out = simulate_city(cohort)
    return {"scenario": name, "humans": cohort, "plaza_after": out["plaza"]}

def main():
    # Three illustrative cohorts
    baseline = [
        {"kappa": 0.44, "gamma": 0.50, "chi": 0.42},
        {"kappa": 0.52, "gamma": 0.54, "chi": 0.48},
        {"kappa": 0.47, "gamma": 0.49, "chi": 0.44},
    ]
    coherent = [
        {"kappa": 0.70, "gamma": 0.78, "chi": 0.55},
        {"kappa": 0.68, "gamma": 0.74, "chi": 0.58},
        {"kappa": 0.73, "gamma": 0.80, "chi": 0.60},
    ]
    mixed = [
        {"kappa": 0.30, "gamma": 0.40, "chi": 0.35},
        {"kappa": 0.71, "gamma": 0.77, "chi": 0.55},
        {"kappa": 0.62, "gamma": 0.58, "chi": 0.60},
        {"kappa": 0.49, "gamma": 0.52, "chi": 0.46},
    ]

    report = {
        "baseline": scenario("baseline", baseline),
        "coherent": scenario("coherent", coherent),
        "mixed":    scenario("mixed", mixed),
    }
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
