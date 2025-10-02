def prosody_stability(cadence_variance, pause_entropy):
    # lower = steadier; balanced silence lowers entropy
    score = max(0.0, 1.0 - (0.6*cadence_variance + 0.4*pause_entropy))
    return score
