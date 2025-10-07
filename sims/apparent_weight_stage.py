# sims/apparent_weight_stage.py
"""
Apparent weight on a vibrating stage (physically interpretable)

We keep gravity g constant. The normal force measured by a scale is:
    F_n(t) = m * [ g + a_stage(t) ]

The stage acceleration is a sinusoid at f_drive, shaped by a damped
single-DOF resonance (natural freq f0, quality factor Q). This is the
standard base-excitation transmissibility picture.

This file replaces the old "gravity partner" toy.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple
import math

@dataclass(frozen=True)
class Params:
    mass_kg: float = 70.0       # mass on the stage
    g: float = 9.81             # gravitational acceleration (constant)
    f_drive: float = 7.83       # drive frequency (Hz)
    a_in: float = 0.2           # input base acceleration amplitude (m/s^2)
    f0: float = 7.83            # stage natural frequency (Hz)
    Q: float = 30.0             # quality factor (Q = 1/(2ζ))
    phase: float = 0.0          # phase offset (rad)

    def validate(self) -> None:
        if self.mass_kg <= 0: raise ValueError("mass_kg must be > 0")
        if not (0 < self.g < 100): raise ValueError("g out of range")
        if self.f0 <= 0 or self.f_drive <= 0: raise ValueError("frequencies must be > 0")
        if self.Q <= 0: raise ValueError("Q must be > 0")
        if self.a_in < 0: raise ValueError("a_in must be ≥ 0")


def transmissibility(f_drive: float, f0: float, Q: float) -> float:
    """
    Acceleration transmissibility for a SDOF base-excited system (simple form).
    r = ω/ω0, ζ = 1/(2Q)
    T_accel(r) ≈ sqrt( (1 + (2ζr)**2) / ((1 - r**2)**2 + (2ζr)**2) )
    """
    ω = 2*math.pi*f_drive
    ω0 = 2*math.pi*f0
    r = ω/ω0
    ζ = 1.0/(2.0*Q)
    num = 1.0 + (2*ζ*r)**2
    den = (1.0 - r**2)**2 + (2*ζ*r)**2
    return math.sqrt(num/den)


def a_stage(t: float, p: Params) -> float:
    """Stage acceleration shaped by resonance."""
    T = transmissibility(p.f_drive, p.f0, p.Q)
    a_amp = p.a_in * T
    return a_amp * math.sin(2*math.pi*p.f_drive*t + p.phase)


def apparent_weight(t: float, p: Params) -> float:
    """Normal force measured by a scale on the vibrating stage."""
    return p.mass_kg * (p.g + a_stage(t, p))


def simulate(p: Params, duration: float = 1.0, dt: float = 0.0005) -> Dict[str, float]:
    """Return summary stats for F_n and a_stage."""
    p.validate()
    n = max(1, int(duration/dt))
    F_vals, a_vals = [], []
    for i in range(n):
        t = i*dt
        a = a_stage(t, p)
        F = p.mass_kg * (p.g + a)
        a_vals.append(a)
        F_vals.append(F)

    def stats(xs: List[float]) -> Tuple[float, float, float, float]:
        m = sum(xs)/len(xs)
        v = sum((x-m)**2 for x in xs)/max(1, len(xs)-1)
        s = math.sqrt(v)
        return m, s, min(xs), max(xs)

    Fm, Fs, Fmin, Fmax = stats(F_vals)
    am, asd, amin, amax = stats(a_vals)
    return {
        "mass_kg": p.mass_kg,
        "g": p.g,
        "f_drive": p.f_drive,
        "f0": p.f0,
        "Q": p.Q,
        "a_in": p.a_in,
        "T_accel": round(transmissibility(p.f_drive, p.f0, p.Q), 6),
        "a_stage_mean": round(am, 9),
        "a_stage_std": round(asd, 9),
        "a_stage_min": round(amin, 9),
        "a_stage_max": round(amax, 9),
        "F_mean": round(Fm, 6),
        "F_std": round(Fs, 6),
        "F_min": round(Fmin, 6),
        "F_max": round(Fmax, 6),
    }


def demo() -> List[Dict[str, float]]:
    base = Params()
    return [
        simulate(base),
        simulate(Params(**{**base.__dict__, "f_drive": base.f0*0.5})),  # off resonance (low)
        simulate(Params(**{**base.__dict__, "f_drive": base.f0*2.0})),  # off resonance (high)
        simulate(Params(**{**base.__dict__, "Q": 10.0})),               # lower Q (broader peak)
        simulate(Params(**{**base.__dict__, "a_in": 0.5})),             # stronger drive
    ]


if __name__ == "__main__":
    import json
    print(json.dumps(demo(), indent=2))
