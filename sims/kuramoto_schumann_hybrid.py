#!/usr/bin/env python3
"""
Kuramoto-Schumann Hybrid
- N Kuramoto oscillators (people) with natural frequencies.
- External driver (Schumann-like) at f_driver Hz (default 7.83 Hz).
- Two-way feedback: driver drives oscillators; collective coherence R
  slightly amplifies driver amplitude (very simple feedback).
- Output: R(t), driver amplitude over time, and snapshot phase histogram.
- Saves: sims/figures/kuramoto_schumann_hybrid_R.png and _phase.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "figures"
OUTDIR.mkdir(parents=True, exist_ok=True)

OUTPNG1 = OUTDIR / "kuramoto_schumann_hybrid_R.png"
OUTPNG2 = OUTDIR / "kuramoto_schumann_hybrid_phase.png"

def simulate(N=200, K=0.8, T=200.0, dt=0.01, f_driver=7.83, G=0.6, feedback=0.2, seed=42):
    """
    N: number oscillators
    K: coupling constant between oscillators
    f_driver: external driver frequency in Hz (Schumann ~7.83)
    G: driver base strength
    feedback: how much collective R amplifies the driver (0..1)
    """
    rng = np.random.default_rng(seed)
    # natural frequencies (human-like) in Hz (we keep them small compared to f_driver)
    # use a bimodal-ish distribution centered near low Hz (0.1-1.5 Hz) to show diversity
    omega_hz = rng.normal(0.7, 0.3, size=N).clip(0.05, 2.5)  # Hz
    omega = 2*np.pi*omega_hz  # rad/s

    theta = rng.uniform(0, 2*np.pi, size=N)
    steps = int(T/dt)

    R_hist = np.empty(steps, dtype=float)
    driver_amp_hist = np.empty(steps, dtype=float)

    # driver state: phase and base amplitude
    phase_driver = 0.0
    w_driver = 2*np.pi*f_driver  # rad/s
    base_amp = G

    for i in range(steps):
        # compute mean-field coupling
        z = np.mean(np.exp(1j*theta))
        R = np.abs(z)
        psi = np.angle(z)
        R_hist[i] = R

        # driver amplitude gets slight boost from collective coherence (simple feedback)
        amp = base_amp * (1.0 + feedback * R)
        driver_amp_hist[i] = amp

        # external driver force for each oscillator
        driver_force = amp * np.sin(phase_driver - theta)

        # internal Kuramoto coupling
        phase_diff = theta[:, None] - theta[None, :]
        coupling = (K / N) * np.sum(np.sin(-phase_diff), axis=1)

        # integrate
        theta = theta + (omega + coupling + driver_force) * dt

        # advance driver (driver not affected by oscillators phase in this simple model)
        phase_driver += w_driver * dt
        phase_driver = (phase_driver + np.pi) % (2*np.pi) - np.pi

    return R_hist, driver_amp_hist, theta

def run_and_plot():
    R, amp, theta = simulate()
    t = np.arange(R.size)

    plt.figure(figsize=(10,4))
    plt.plot(t, R, label="R (coherence)")
    plt.plot(t, amp/np.max(amp), label="driver amp (normalized)")
    plt.xlabel("time steps")
    plt.ylabel("coherence / relative amplitude")
    plt.legend()
    plt.title("Kuramoto ↔ Schumann Hybrid — R(t) and driver amplitude")
    plt.tight_layout()
    plt.savefig(OUTPNG1, dpi=150)
    print(f"Saved: {OUTPNG1}")

    # phase histogram snapshot
    plt.figure(figsize=(6,4))
    plt.hist(np.angle(np.exp(1j*theta)), bins=36)
    plt.title("Phase distribution (final snapshot)")
    plt.xlabel("phase (rad)")
    plt.ylabel("count")
    plt.tight_layout()
    plt.savefig(OUTPNG2, dpi=150)
    print(f"Saved: {OUTPNG2}")

if __name__ == "__main__":
    run_and_plot()
  What to expect / pass–falsifier
	•	Expect: R(t) may show low initial coherence; when driver amplitude (or feedback) is strong enough, pockets of entrainment form.
	•	Pass: coherent plateau where R increases and stabilizes for several time units.
	•	Falsifier: R remains ~0.1 constantly regardless of driver amplitude — suggests coupling too weak or parameters inconsistent.
