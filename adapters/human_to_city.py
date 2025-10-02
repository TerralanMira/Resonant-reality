def node_influence_from_human(kappa: float, gamma: float, chi: float) -> dict:
    """
    Converts human coherence metrics into city node weights.
    Returns deltas to apply to a zone's resonance.
    """
    base = (0.6*kappa + 0.3*gamma + 0.1*chi)
    return {
        "zone_coherence_delta": round(0.25*base, 4),
        "noise_reduction_delta": round(0.15*base, 4),
        "coupling_gain_delta":   round(0.10*base, 4)
    }
