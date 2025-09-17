"""
Orbital Resonance Simulation
----------------------------

A minimal sim of planetary orbital resonance.
We track two planets orbiting a star and highlight
the resonance ratio (e.g., Earth:Venus ~ 8:13).

Outputs:
- sims/figures/orbital_resonance_lissajous.png

Run:
    python sims/orbital_resonance.py
    python sims/orbital_resonance.py --steps 2000 --ratio1 8 --ratio2 13
"""

import os
import argparse
import numpy as np
import matplotlib.pyplot as plt


def simulate_orbits(steps=2000, ratio1=8, ratio2=13):
    """
    Generate orbital positions for two planets.
    Ratio1: number of orbits of planet A
    Ratio2: number of orbits of planet B
    """
    t = np.linspace(0, 2 * np.pi, steps)
    theta1 = ratio1 * t
    theta2 = ratio2 * t
    x = np.cos(theta1)
    y = np.sin(theta1)
    u = np.cos(theta2)
    v = np.sin(theta2)
    return x, y, u, v


def plot_resonance(x, y, u, v, ratio1, ratio2, out_dir="sims/figures"):
    os.makedirs(out_dir, exist_ok=True)
    plt.figure(figsize=(6, 6))
    plt.plot(x, y, alpha=0.5, label=f"Planet A ({ratio1})")
    plt.plot(u, v, alpha=0.5, label=f"Planet B ({ratio2})")
    plt.plot(x - u, y - v, color="black", linewidth=0.8, alpha=0.7, label="Relative path")
    plt.axis("equal")
    plt.title(f"Orbital Resonance: {ratio1}:{ratio2}")
    plt.legend()
    path = os.path.join(out_dir, f"orbital_resonance_{ratio1}_{ratio2}.png")
    plt.savefig(path, dpi=150)
    return path


def parse_args():
    ap = argparse.ArgumentParser(description="Orbital resonance sim.")
    ap.add_argument("--steps", type=int, default=2000, help="time steps")
    ap.add_argument("--ratio1", type=int, default=8, help="orbital ratio for planet A")
    ap.add_argument("--ratio2", type=int, default=13, help="orbital ratio for planet B")
    return ap.parse_args()


if __name__ == "__main__":
    args = parse_args()
    x, y, u, v = simulate_orbits(steps=args.steps, ratio1=args.ratio1, ratio2=args.ratio2)
    path = plot_resonance(x, y, u, v, args.ratio1, args.ratio2)
    print(f"Saved orbital resonance figure: {path}")
