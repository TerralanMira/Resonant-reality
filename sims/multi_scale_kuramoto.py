#!/usr/bin/env python3
"""
Multi-scale Kuramoto
- Create C clusters of size S. Strong intra-cluster coupling, weaker inter-cluster coupling.
- Visualize R for each cluster and global R.
- Saves: sims/figures/multi_scale_kuramoto.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "figures"
OUTDIR.mkdir(parents=True, exist_ok=True)
OUTPNG = OUTDIR / "multi_scale_kuramoto.png"

def simulate(C=5, S=80, K_intra=1.0, K_inter=0.05, T=200.0, dt=0.05, seed=10):
    rng = np.random.default_rng(seed)
    N = C*S
    # cluster labels
    labels = np.repeat(np.arange(C), S)
    omega = rng.normal(1.0, 0.3, size=N)  # rad/s like earlier
    theta = rng.uniform(0, 2*np.pi, size=N)
    steps = int(T/dt)

    R_hist = np.empty((steps, C))
    R_global = np.empty(steps)

    for t in range(steps):
        # per-cluster order parameter
        z_c = []
        for c in range(C):
            idx = labels==c
            z = np.mean(np.exp(1j*theta[idx]))
            z_c.append(z)
            R_hist[t, c] = np.abs(z)
        R_global[t] = np.abs(np.mean(np.exp(1j*theta)))

        # coupling: each oscillator feels intra coupling strongly and weaker pull from other clusters
        coupling = np.zeros_like(theta)
        for i in range(N):
            same = labels==labels[i]
            other = ~same
            # intra
            phase_diff_intra = theta[i] - theta[same]
            coupling[i] += (K_intra / same.sum()) * np.sum(-np.sin(phase_diff_intra))
            # inter (mean-field across other clusters)
            coupling[i] += (K_inter / other.sum()) * np.sum(-np.sin(theta[i] - theta[other]))

        theta = theta + (omega + coupling) * dt

    return R_hist, R_global

def run_and_plot():
    R_hist, Rg = simulate()
    t = np.arange(Rg.size)

    plt.figure(figsize=(10,5))
    for c in range(R_hist.shape[1]):
        plt.plot(t, R_hist[:,c], alpha=0.8, label=f"cluster {c+1}")
    plt.plot(t, Rg, color="k", linewidth=2, label="global R")
    plt.xlabel("time steps")
    plt.ylabel("coherence R")
    plt.title("Multi-scale Kuramoto — cluster vs global coherence")
    plt.legend(loc="upper right", fontsize="small")
    plt.tight_layout()
    plt.savefig(OUTPNG, dpi=150)
    print(f"Saved: {OUTPNG}")

if __name__ == "__main__":
    run_and_plot()
  What to expect
	•	With strong K_intra but weak K_inter, clusters lock internally (high cluster R) while global R remains low.
	•	Increase K_inter and observe global lock. This demonstrates how local coherence can exist without global coherence until coupling across scales increases.
  
