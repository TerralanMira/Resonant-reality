def coherence_grade(kappa, gamma):
    if kappa >= 0.80 and gamma >= 0.45: return "resonant"
    if kappa >= 0.65: return "stable"
    return "fragmenting"
