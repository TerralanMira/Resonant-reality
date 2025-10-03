# sims/city_coupling_demo.py
from adapters.human_to_city import node_influence_from_human

def clamp(x, lo=0.0, hi=1.0):
    return lo if x < lo else hi if x > hi else x

def simulate_city(humans):
    """
    Toy demo: aggregates human resonance into a single 'plaza' zone.
    Metrics:
      - coherence: ↑ with human κ/γ/χ
      - noise: ↓ with human κ/γ/χ
      - coupling: ↑ with human κ/γ/χ
    """
    zones = {"plaza": {"coherence": 0.50, "noise": 0.40, "coupling": 0.60}}

    for h in humans:
        deltas = node_influence_from_human(h["kappa"], h["gamma"], h["chi"])
        # Map deltas explicitly
        zones["plaza"]["coherence"] = clamp(
            zones["plaza"]["coherence"] + deltas["zone_coherence_delta"]
        )
        zones["plaza"]["noise"] = clamp(
            zones["plaza"]["noise"] - deltas["noise_reduction_delta"]
        )
        zones["plaza"]["coupling"] = clamp(
            zones["plaza"]["coupling"] + deltas["coupling_gain_delta"]
        )

    return zones

if __name__ == "__main__":
    # Example cohort (κ, γ, χ)
    humans = [
        {"kappa": 0.44, "gamma": 0.50, "chi": 0.42},
        {"kappa": 0.70, "gamma": 0.78, "chi": 0.55},
        {"kappa": 0.62, "gamma": 0.58, "chi": 0.60},
    ]
    result = simulate_city(humans)
    print("Plaza resonance:", result)
