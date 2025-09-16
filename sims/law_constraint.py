#!/usr/bin/env python3
"""
Law Constraint — coherence vs rigidity.

- Oscillators evolve freely (Kuramoto-like) but 'law' snaps phases
  toward allowed bands (phase bins) with strength L.
- Shows tradeoff: too little law → disorder; too much → brittle uniformity.
- Figure: sims/figures/law_constraint.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "figures"
OUTDIR.mkdir(parents=True, exist_ok=True)
OUTPNG = OUTDIR / "law_constraint.png"

def simulate(N=200, K=0.5, L=0.3, bins=8, T=400, dt=0.05, seed=3):
    rng = np.random.default_rng(seed)
    omega = rng.normal(0.0, 1.0, N)
    theta = rng.uniform(0, 2*np.pi, N)
    steps = int(T/dt)
    R_hist = np.empty(steps, dtype=float)

    # precompute bin centers
    centers = np.linspace(0, 2*np.pi, bins, endpoint=False)

    for t in range(steps):
        # Kuramoto coupling
        phase_diff = theta[:, None] - theta[None, :]
        coupling = (K / N) * np.sum(np.sin(-phase_diff), axis=1)

        # law pull toward nearest allowed phase center
        # for each theta_i, find nearest center
        idx = np.argmin(np.abs((theta[:,None]-centers[None,:]+np.pi)%(2*np.pi)-np.pi), axis=1)
        target = centers[idx]
        law_force = L * np.sin(target - theta)  # small-angle pull toward target

        theta = theta + (omega + coupling + law_force) * dt
        R_hist[t] = np.abs(np.mean(np.exp(1j*theta)))
    return R_hist

def run_and_plot():
    plt.figure(figsize=(9,5))
    for L in (0.0, 0.2, 0.5, 1.0):
        R = simulate(L=L)
        plt.plot(R, label=f"L={L}")
    plt.xlabel("time steps")
    plt.ylabel("coherence R")
    plt.title("Law as Phase Constraint — order vs rigidity")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPNG, dpi=150)
    print(f"Saved: {OUTPNG}")

if __name__ == "__main__":
    run_and_plot()
