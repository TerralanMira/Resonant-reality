#!/usr/bin/env python3
"""
Solar Kuramoto — stub

Treats major solar-system bodies as phase oscillators with natural
frequencies derived from orbital periods (simplified). Demonstrates
emergent coherence under coupling K.

- One figure (no subplots), default matplotlib style/colors.
- Saves to: sims/figures/solar.png
- Dependencies: numpy, matplotlib

This is illustrative (not ephemeris-accurate). It shows how a small,
heterogeneous set can exhibit partial phase-locking as K increases.
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# Paths
ROOT = Path(__file__).resolve().parents[1]   # .../sims
OUTDIR = ROOT / "figures"
OUTDIR.mkdir(parents=True, exist_ok=True)
OUTPNG = OUTDIR / "solar.png"

# --- Orbital periods (days) — rough canonical values
# You can adjust or expand this list as desired.
BODIES = {
    "Mercury":   87.97,
    "Venus":    224.70,
    "Earth":    365.25,
    "Mars":     686.98,
    "Jupiter": 4332.59,
    "Saturn":  10759.22,
    "Uranus":  30688.5,
    "Neptune": 60182.0,
}

def natural_frequencies(periods_days, scale="cycles_per_1000d"):
    """
    Convert orbital periods into natural frequencies for the Kuramoto model.
    We normalize to avoid extremely small numbers.

    scale options:
      - "cycles_per_day"
      - "cycles_per_1000d"  (default; keeps numbers ~0..4)
    """
    periods = np.array(periods_days, dtype=float)
    if scale == "cycles_per_day":
        freq = 1.0 / periods
    else:  # "cycles_per_1000d"
        freq = 1000.0 / periods
    # Convert to angular frequencies (rad / time-step "t")
    # time-step "t" here is abstract; we use dt below to scale integration.
    return 2.0 * np.pi * freq

def simulate(omega, K=0.6, T=4000, dt=0.05, seed=0):
    """
    Basic Euler integration of the Kuramoto model:
        dtheta_i/dt = omega_i + (K/N) * sum_j sin(theta_j - theta_i)

    Returns:
      - R_hist: order parameter over time
    """
    rng = np.random.default_rng(seed)
    N = len(omega)
    steps = int(T / dt)
    theta = rng.uniform(0, 2*np.pi, size=N)

    R_hist = np.empty(steps, dtype=float)
    for t in range(steps):
        # Order parameter R = |mean(exp(i*theta))|
        R = np.abs(np.mean(np.exp(1j * theta)))
        R_hist[t] = R

        # Mean-field coupling term
        # Using vectorized mean of sin(theta_j - theta_i)
        phase_diff = theta[:, None] - theta[None, :]
        coupling = (K / N) * np.sum(np.sin(-phase_diff), axis=1)  # sin(theta_j - theta_i)

        # Euler step
        theta = theta + (omega + coupling) * dt

    return R_hist

def run_and_plot(K_values=(0.2, 0.6, 1.2)):
    periods = list(BODIES.values())
    omega = natural_frequencies(periods, scale="cycles_per_1000d")

    plt.figure(figsize=(9, 5))
    for K in K_values:
        R_hist = simulate(omega, K=K, T=4000, dt=0.05, seed=0)
        plt.plot(R_hist, label=f"K={K}")

    plt.xlabel("time steps")
    plt.ylabel("coherence R")
    plt.title("Solar Kuramoto — coherence vs coupling (illustrative)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPNG, dpi=150)
    print(f"Saved: {OUTPNG}")

if __name__ == "__main__":
    run_and_plot()
  How to run (terminal):
python sims/solar_kuramoto.py
This will create:
sims/figures/solar.png

