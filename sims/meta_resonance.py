#!/usr/bin/env python3
"""
Meta-Resonance — Human ↔ Schumann ↔ Civic Pulses (coupled model)

What it does
- N = C*S oscillators (humans) in C clusters (hearths/neighborhoods).
- Strong intra-cluster coupling K_intra, weaker inter-cluster K_inter.
- External Schumann-like driver at f_driver (default 7.83 Hz) with strength G.
- Simple feedback: global coherence R boosts driver amplitude (alpha_feedback).
- Civic pulses (festivals/rituals) periodically boost inter-coupling and driver.

Saves two figures:
- sims/figures/meta_resonance_R.png        (global R and driver amplitude vs time)
- sims/figures/meta_resonance_layers.png   (cluster R's and global R)

Adjust parameters at bottom to explore behavior.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "figures"
OUTDIR.mkdir(parents=True, exist_ok=True)
OUT_R = OUTDIR / "meta_resonance_R.png"
OUT_L = OUTDIR / "meta_resonance_layers.png"

def simulate(C=4, S=120,                       # clusters × size
             K_intra=1.0, K_inter=0.05,        # couplings
             f_driver=7.83, G=0.5,             # Schumann-like driver
             alpha_feedback=0.25,              # driver ← global R feedback
             event_period=30.0, event_duration=6.0,
             boost_inter=0.25, boost_driver=0.35,
             T=200.0, dt=0.01, seed=7):
    rng = np.random.default_rng(seed)
    N = C * S

    # Natural frequencies (Hz) for humans — low-frequency band (breath/step/chant range)
    omega_hz = rng.normal(0.7, 0.25, size=N).clip(0.05, 2.5)
    omega = 2*np.pi*omega_hz  # rad/s

    # Initial phases
    theta = rng.uniform(0, 2*np.pi, size=N)

    # Cluster labels
    labels = np.repeat(np.arange(C), S)

    # Driver state
    phi_d = 0.0
    w_d = 2*np.pi*f_driver

    steps = int(T/dt)
    R_global = np.empty(steps)
    R_clusters = np.empty((steps, C))
    amp_hist = np.empty(steps)

    for t in range(steps):
        # Order parameters
        z = np.mean(np.exp(1j*theta))
        R = np.abs(z)
        R_global[t] = R

        for c in range(C):
            idx = (labels == c)
            R_clusters[t, c] = np.abs(np.mean(np.exp(1j*theta[idx])))

        # Civic pulse window?
        time = t * dt
        in_pulse = (event_period > 0) and ((time % event_period) < event_duration)

        # Effective couplings during civic pulse
        Kint = K_inter * (1.0 + boost_inter if in_pulse else 1.0)

        # Driver amplitude with feedback (and pulse boost)
        amp = G * (1.0 + alpha_feedback * R) * (1.0 + (boost_driver if in_pulse else 0.0))
        amp_hist[t] = amp

        # External driver force
        driver_force = amp * np.sin(phi_d - theta)

        # Intra + inter coupling (pairwise, but vectorized)
        # For efficiency: mean-field approximation per cluster + global
        coupling = np.zeros(N)
        for c in range(C):
            idx_c = (labels == c)
            the_c = theta[idx_c]
            z_c = np.mean(np.exp(1j*the_c))
            psi_c = np.angle(z_c)
            # intra pull toward cluster mean
            coupling[idx_c] += K_intra * np.sin(psi_c - the_c)

        # inter pull toward global mean (excluding own cluster implicitly)
        psi_g = np.angle(z)
        coupling += Kint * np.sin(psi_g - theta)

        # Integrate phases
        theta = theta + (omega + coupling + driver_force) * dt

        # Advance driver phase
        phi_d = (phi_d + w_d * dt + np.pi) % (2*np.pi) - np.pi

    return R_global, R_clusters, amp_hist

def run_and_plot():
    Rg, Rc, A = simulate()

    t = np.arange(Rg.size)

    # Figure 1: global coherence vs driver amplitude
    plt.figure(figsize=(10,4))
    A_norm = A / (A.max() if A.max()>0 else 1.0)
    plt.plot(t, Rg, label="Global coherence R")
    plt.plot(t, A_norm, label="Driver amplitude (normalized)")
    plt.xlabel("time steps")
    plt.ylabel("R / relative amplitude")
    plt.title("Meta-Resonance — Global Coherence vs Driver Amplitude")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT_R, dpi=150)
    print(f"Saved: {OUT_R}")

    # Figure 2: cluster R's + global R
    plt.figure(figsize=(10,5))
    for c in range(Rc.shape[1]):
        plt.plot(t, Rc[:,c], alpha=0.85, label=f"cluster {c+1}")
    plt.plot(t, Rg, linewidth=2.0, label="global R")
    plt.xlabel("time steps")
    plt.ylabel("coherence R")
    plt.title("Meta-Resonance — Cluster vs Global Coherence")
    plt.legend(loc="upper right", fontsize="small")
    plt.tight_layout()
    plt.savefig(OUT_L, dpi=150)
    print(f"Saved: {OUT_L}")

if __name__ == "__main__":
    run_and_plot()
