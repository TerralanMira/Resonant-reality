"""
Cosmic ↔ Civic Calendar Dynamics (toy ABM)
Agents align on ritual timing; shared calendar boosts coherence.

Outputs:
  sims/figures/civic_calendar_coherence.png
  sims/figures/civic_calendar_alignment.png

Run:
  python sims/civic_calendar.py
"""
import os, argparse
import numpy as np
import matplotlib.pyplot as plt

def simulate(N=200, T=2000, period=30.0, coupling=0.06, cosmic_lock=0.02, seed=0):
    """
    Agents with phases theta_i try to align to each other (coupling)
    and to an external cosmic rhythm (period).
    """
    rng = np.random.default_rng(seed)
    theta = rng.uniform(0, 2*np.pi, N)
    dt = 1.0
    omega_cosmic = 2*np.pi/period
    coherence, align_err = [], []

    for _ in range(T):
        # Kuramoto-like coupling to neighbors (global mean field)
        mean_phasor = np.exp(1j*theta).mean()
        mean_phase = np.angle(mean_phasor)

        # Step dynamics
        dtheta = coupling*np.sin(mean_phase - theta) + cosmic_lock*np.sin(omega_cosmic*_ - theta)
        theta = (theta + dtheta*dt)%(2*np.pi)

        # Metrics
        R = abs(mean_phasor)  # order parameter
        coherence.append(R)

        # alignment error to cosmic phase (mod 2pi)
        cosmic_phase = (omega_cosmic*_)%(2*np.pi)
        err = np.mean(np.abs(np.angle(np.exp(1j*(theta - cosmic_phase)))))
        align_err.append(err)

    return np.array(coherence), np.array(align_err)

def plot_results(coh, err, out1="sims/figures/civic_calendar_coherence.png",
                 out2="sims/figures/civic_calendar_alignment.png"):
    os.makedirs(os.path.dirname(out1), exist_ok=True)
    plt.figure(figsize=(8,3))
    plt.plot(coh); plt.ylim(0,1.05)
    plt.xlabel("time"); plt.ylabel("coherence R")
    plt.title("Civic coherence under shared calendar (toy)")
    plt.tight_layout(); plt.savefig(out1, dpi=150)

    plt.figure(figsize=(8,3))
    plt.plot(err)
    plt.xlabel("time"); plt.ylabel("alignment error (rad)")
    plt.title("Alignment to cosmic phase")
    plt.tight_layout(); plt.savefig(out2, dpi=150)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, default=200)
    ap.add_argument("--T", type=int, default=2000)
    ap.add_argument("--period", type=float, default=30.0, help="cosmic cycle length (days)")
    ap.add_argument("--coupling", type=float, default=0.06)
    ap.add_argument("--cosmic_lock", type=float, default=0.02)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    coh, err = simulate(N=args.N, T=args.T, period=args.period,
                        coupling=args.coupling, cosmic_lock=args.cosmic_lock, seed=args.seed)
    plot_results(coh, err)
    print("Saved sims/figures/civic_calendar_coherence.png")
    print("Saved sims/figures/civic_calendar_alignment.png")

if __name__ == "__main__":
    main()
