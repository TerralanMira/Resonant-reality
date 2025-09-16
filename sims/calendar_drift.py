#!/usr/bin/env python3
"""
Calendar Drift — communities with periodic festivals drifting and resetting.

- M communities with slightly different periods + noise.
- Optional periodic 'reset' event (equinox/solstice) snaps phases together.
- Output: phase dispersion over time, with/without resets.
- Figure: sims/figures/calendar_drift.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "figures"
OUTDIR.mkdir(parents=True, exist_ok=True)
OUTPNG = OUTDIR / "calendar_drift.png"

def simulate(M=50, T=2000, dt=1.0, reset_period=180.0, reset_strength=0.6, seed=2):
    """Phases advance at slightly different rates + noise; periodic resets reduce dispersion."""
    rng = np.random.default_rng(seed)
    steps = int(T/dt)
    # base period ~ 365d with small variation
    periods = rng.normal(365.0, 5.0, size=M)
    omega = 2*np.pi / periods  # rad/day
    theta = rng.uniform(0, 2*np.pi, size=M)
    dispersion = np.empty(steps, dtype=float)

    for t in range(steps):
        # advance with small jitter
        theta += (omega + rng.normal(0, 1e-3, size=M)) * dt
        theta %= 2*np.pi
        # measure dispersion (1 - R)
        R = np.abs(np.mean(np.exp(1j*theta)))
        dispersion[t] = 1.0 - R

        # periodic reset (e.g., equinox ceremony)
        time = t*dt
        if reset_period and (time % reset_period) < dt:
            mean_angle = np.angle(np.mean(np.exp(1j*theta)))
            # pull phases toward mean
            theta = (1 - reset_strength)*theta + reset_strength*mean_angle
    return dispersion

def run_and_plot():
    plt.figure(figsize=(9,5))
    d_no = simulate(reset_period=None)  # no resets
    d_eq = simulate(reset_period=180.0, reset_strength=0.6)  # semiannual reset
    d_sol = simulate(reset_period=365.0, reset_strength=0.8) # annual strong reset
    plt.plot(d_no, label="no resets")
    plt.plot(d_eq, label="equinox resets")
    plt.plot(d_sol, label="solstice resets")
    plt.xlabel("time steps (days)")
    plt.ylabel("phase dispersion (1 - R)")
    plt.title("Calendar Drift — synchronization via ritual resets")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPNG, dpi=150)
    print(f"Saved: {OUTPNG}")

if __name__ == "__main__":
    run_and_plot()
