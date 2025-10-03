# sims/gravity_partner.py
"""
Gravity as Partner (conceptual hook)
Treat gravity as a coupling slightly modulated by coherence (κ) and a carrier (f).
Bounded so it stays sensible; compare on/off resonance by varying κ and f.
"""
from __future__ import annotations
import math

def resonance_gravity_force(mass_kg: float, base_g: float = 9.81,
                            freq_hz: float = 7.83, kappa: float = 0.6, t: float = 0.0) -> float:
    coupling = 0.05 * kappa * math.sin(2 * math.pi * freq_hz * t)  # ± ~5% * κ window
    g_eff = base_g * (1.0 + coupling)
    return mass_kg * g_eff

def demo():
    rows = []
    for k in (0.2, 0.6, 0.85):
        for f in (0.0, 7.83, 528.0):
            force_t0 = resonance_gravity_force(70, freq_hz=f, kappa=k, t=0.0)
            force_tq = resonance_gravity_force(70, freq_hz=f, kappa=k, t=0.25)
            rows.append({"κ": k, "f": f, "F(t=0)": round(force_t0, 3), "F(t=0.25)": round(force_tq, 3)})
    return rows

if __name__ == "__main__":
    import json
    print(json.dumps(demo(), indent=2))
