# sims/gravity_partner.py
"""
Gravity as Partner (concept stub)
Treat gravity as a coupling that modulates with coherence (κ) and carrier frequency (f).
This is a simple exploratory hook for comparing resonance-on vs. resonance-off scenarios.
"""
import math

def resonance_gravity_force(mass_kg: float, base_g=9.81, freq_hz=7.83, kappa=0.6, t=0.0):
    # Coupling term bounded in a small band to avoid absurd values
    coupling = 0.05 * kappa * math.sin(2 * math.pi * freq_hz * t)
    g_eff = base_g * (1.0 + coupling)
    return mass_kg * g_eff

if __name__ == "__main__":
    for t in [0, 0.25, 0.5, 0.75, 1.0]:
        print(t, round(resonance_gravity_force(70, freq_hz=7.83, kappa=0.6, t=t), 4))
