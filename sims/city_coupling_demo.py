from adapters.human_to_city import node_influence_from_human

def simulate_city(humans):
    zones = {"plaza": {"coherence": 0.5, "noise": 0.4, "coupling": 0.6}}
    for h in humans:
        deltas = node_influence_from_human(**h)
        for key in zones["plaza"]:
            zones["plaza"][key] += deltas.get(f"{key}_delta", 0.0)
    return zones

if __name__ == "__main__":
    humans = [
        {"kappa": 0.4, "gamma": 0.6, "chi": 0.7},
        {"kappa": 0.7, "gamma": 0.8, "chi": 0.5},
    ]
    result = simulate_city(humans)
    print("Plaza resonance:", result)
