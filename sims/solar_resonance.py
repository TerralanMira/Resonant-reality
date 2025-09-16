#!/usr/bin/env python3
"""
Solar Resonance — stub

Illustrative 11-year solar cycle as a resonant oscillator with slow-frequency drift,
weak stochastic forcing, and a simple "coupling gain" that can amplify coherence.

- One figure (no subplots), default matplotlib styles/colors.
- Saves to: sims/figures/solar_resonance.png
- Deps: numpy, matplotlib

Notes:
- This is NOT a physical solar model; it's a minimal signal that "breathes" like the 11-year cycle.
- Use it to demonstrate resonance windows and coherence amplification (myth → math → visual).
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]  # .../sims
OUTDIR = ROOT / "figures"
OUTDIR.mkdir(parents=True, exist_ok=True)
OUTPNG = OUTDIR / "solar_resonance.png"

def solar_cycle(T_years=60, dt=1/24, base_period=11.0, drift_amp=0.12, coupling=0.25, seed=7):
    """
    Build a synthetic 'sunspot-like' time series.

    Args:
        T_years   : total duration (years)
        dt        : timestep (years) — default = ~half-month (1/24 ≈ 0.5 months)
        base_period : nominal period in years (≈ 11 yrs)
        drift_amp : fractional drift of the period over time (0..~0.2)
        coupling  : gain that boosts coherence of the oscillator (0..1)
        seed      : RNG seed
    Returns:
        t (years), x (normalized amplitude)
    """
    rng = np.random.default_rng(seed)
    n = int(T_years / dt)
    t = np.linspace(0.0, T_years, n, endpoint=False)

    # Period slowly drifts (quasi-periodic)
    # e.g., +/− (drift_amp * base_period)
    slow = np.sin(2*np.pi * t / (5*base_period))  # multi-cycle drift
    period = base_period * (1.0 + drift_amp * slow)
    omega_t = 2*np.pi / period  # instantaneous angular frequency

    # Integrate phase with Euler
    phase = np.zeros(n)
    for i in range(1, n):
        phase[i] = phase[i-1] + omega_t[i] * dt

    # Core oscillation
    core = np.sin(phase)

    # Envelope to mimic asymmetric rise/decay (simple rectified + smoothing)
    env = 0.6 + 0.4 * np.sin(phase - np.pi/3)**2

    # Noise + small broadband component
    noise = 0.2 * rng.normal(size=n)
    broadband = 0.05 * np.sin(2*np.pi * t / (base_period/2.0))

    # Coupling gain: pushes signal toward coherent envelope-carried oscillation
    x = (1 - coupling) * (core + noise + broadband) + coupling * (env * core)

    # Rectify + smooth to resemble "sunspot number" style series
    x = np.abs(x)

    # Normalize to 0..1 for consistent plotting
    x = (x - x.min()) / (x.max() - x.min() + 1e-9)

    return t, x

def run_and_plot():
    # Compare three coupling gains
    params = [
        ("low",   0.05),
        ("mid",   0.25),
        ("high",  0.50),
    ]

    plt.figure(figsize=(10, 5))
    for label, k in params:
        t, x = solar_cycle(coupling=k)
        plt.plot(t, x, label=f"coupling={k:g}")

    plt.title("Solar Resonance — synthetic 11-year cycle with coupling gain")
    plt.xlabel("time (years)")
    plt.ylabel("normalized activity")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPNG, dpi=150)
    print(f"Saved: {OUTPNG}")

if __name__ == "__main__":
    run_and_plot()
  How to run (terminal)
python sims/solar_resonance.py
This will create:
sims/figures/solar_resonance.png
