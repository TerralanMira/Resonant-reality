#!/usr/bin/env python3
"""
Media Coupler — broadcast driver as external field.

- Oscillators receive a global periodic signal with strength G.
- Trust/noise reduces or enhances coupling to the driver.
- Output: coherence R(t) across different G and trust levels.
- Figure: sims/figures/media_coupler.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "figures"
OUTDIR.mkdir(parents=True, exist_ok=True)
OUTPNG = OUTDIR / "media_coupler.png"

def simulate(N=300, K=0.3, G=0.5, trust=0.7, driver_freq=1.0, T=400, dt=0.05, seed=4):
    rng = np.random.default_rng(seed)
    omega = rng.normal(0.0, 1.0, N)
    theta = rng.uniform(0, 2*np.pi, N)
    steps = int(T/dt)
    R_hist = np.empty(steps, dtype=float)

    # some agents distrust the driver → effective coupling scaled down
    agent_gain = rng.uniform(trust*0.5, trust*1.5, size=N).clip(0.0, 1.0)

    phase_driver = 0.0
    w_driver = 2*np.pi*driver_freq

    for t in range(steps):
        phase_driver += w_driver*dt
        # Kuramoto mean-field
        phase_diff = theta[:, None] - theta[None, :]
        coupling = (K / N) * np.sum(np.sin(-phase_diff), axis=1)
        # external broadcast driver
        driver_force = G * agent_gain * np.sin(phase_driver - theta)

        theta = theta + (omega + coupling + driver_force) * dt
        R_hist[t] = np.abs(np.mean(np.exp(1j*theta)))
    return R_hist

def run_and_plot():
    plt.figure(figsize=(9,5))
    configs = [
        ("weak G, low trust", 0.2, 0.3),
        ("weak G, high trust", 0.2, 0.9),
        ("strong G, low trust", 0.8, 0.3),
        ("strong G, high trust", 0.8, 0.9),
    ]
    for label, G, trust in configs:
        R = simulate(G=G, trust=trust)
        plt.plot(R, label=label)
    plt.xlabel("time steps")
    plt.ylabel("coherence R")
    plt.title("Media as Global Coupler — entrainment vs fragmentation")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPNG, dpi=150)
    print(f"Saved: {OUTPNG}")

if __name__ == "__main__":
    run_and_plot()
