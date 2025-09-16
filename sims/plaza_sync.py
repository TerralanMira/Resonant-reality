#!/usr/bin/env python3
"""
Plaza Synchrony — Kuramoto crowd in a resonant square.

- N agents with random natural frequencies.
- Coupling K mimics acoustic/proximity gains of a plaza.
- Output: order parameter R(t) vs time for several K.
- Figure: sims/figures/plaza_sync.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]   # .../sims
OUTDIR = ROOT / "figures"
OUTDIR.mkdir(parents=True, exist_ok=True)
OUTPNG = OUTDIR / "plaza_sync.png"

def simulate(N=300, K=0.6, T=300, dt=0.05, seed=1):
    rng = np.random.default_rng(seed)
    omega = rng.normal(0.0, 1.0, N)  # natural frequencies
    theta = rng.uniform(0, 2*np.pi, N)
    steps = int(T/dt)
    R_hist = np.empty(steps, dtype=float)

    for t in range(steps):
        R = np.abs(np.mean(np.exp(1j*theta)))
        R_hist[t] = R
        phase_diff = theta[:, None] - theta[None, :]
        coupling = (K / N) * np.sum(np.sin(-phase_diff), axis=1)
        theta = theta + (omega + coupling) * dt
    return R_hist

def run_and_plot(K_values=(0.2, 0.6, 1.0, 1.4)):
    plt.figure(figsize=(9,5))
    for K in K_values:
        R = simulate(K=K)
        plt.plot(R, label=f"K={K}")
    plt.xlabel("time steps")
    plt.ylabel("coherence R")
    plt.title("Plaza Synchrony — crowd lock-in vs coupling")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPNG, dpi=150)
    print(f"Saved: {OUTPNG}")

if __name__ == "__main__":
    run_and_plot()
