"""
Orbital Resonance Maps (toy)
Visualizes simple harmonic ratios between two synthetic orbital cycles,
and a spiral map of their phase relationship.

Outputs:
  sims/figures/orbital_ratio_time.png
  sims/figures/orbital_spiral_map.png

Run:
  python sims/orbital_resonance.py
"""
import os, argparse
import numpy as np
import matplotlib.pyplot as plt

def make_orbits(T=20000, dt=1.0, P1=365.25, P2=4332.59, phase2=0.0):
    t = np.arange(T)*dt
    th1 = 2*np.pi*t/P1
    th2 = 2*np.pi*t/P2 + phase2
    return t, th1%(2*np.pi), th2%(2*np.pi)

def ratio_signal(th1, th2):
    # instantaneous frequency ratio proxy via phase increments
    d1 = np.diff(np.unwrap(th1)); d2 = np.diff(np.unwrap(th2))
    r = np.where(d2!=0, d1/d2, np.nan)
    r_sm = np.convolve(r, np.ones(200)/200, mode="same")  # smooth
    return r_sm

def plot_ratio_time(t, r, out="sims/figures/orbital_ratio_time.png"):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    plt.figure(figsize=(9,4))
    plt.plot(t[1:], r)
    plt.xlabel("time"); plt.ylabel("ω1/ω2 (smoothed)")
    plt.title("Instantaneous orbital ratio (toy)")
    plt.tight_layout(); plt.savefig(out, dpi=150)

def spiral_phase_map(th1, th2, turns=6, out="sims/figures/orbital_spiral_map.png"):
    # map relative phase onto a logarithmic spiral
    n = min(len(th1), len(th2))
    dphi = (th1[:n]-th2[:n]+np.pi)%(2*np.pi)-np.pi
    t = np.linspace(0, 2*np.pi*turns, n)
    r = 0.2*np.exp(0.15*t) * (0.9 + 0.1*np.cos(dphi))  # modulate radius by phase lock
    x = r*np.cos(t); y = r*np.sin(t)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    plt.figure(figsize=(6,6))
    plt.scatter(x, y, s=0.5)
    plt.axis('equal'); plt.title("Orbital resonance spiral (toy)")
    plt.tight_layout(); plt.savefig(out, dpi=150)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--T", type=int, default=20000)
    ap.add_argument("--dt", type=float, default=1.0)
    ap.add_argument("--P1", type=float, default=365.25, help="inner orbital period")
    ap.add_argument("--P2", type=float, default=4332.59, help="outer orbital period")
    ap.add_argument("--phase2", type=float, default=0.0)
    args = ap.parse_args()

    t, th1, th2 = make_orbits(args.T, args.dt, args.P1, args.P2, args.phase2)
    r = ratio_signal(th1, th2)
    plot_ratio_time(t, r)
    spiral_phase_map(th1, th2)
    print("Saved sims/figures/orbital_ratio_time.png")
    print("Saved sims/figures/orbital_spiral_map.png")

if __name__ == "__main__":
    main()
