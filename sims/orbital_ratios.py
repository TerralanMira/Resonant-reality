"""
Orbital Ratios — 'music of the spheres' (toy)
Generates simple visuals of planetary orbital period ratios and a spiral map.

Outputs:
  sims/figures/orbital_ratios.png
  sims/figures/orbital_ratios_spiral.png

Run:
  python sims/orbital_ratios.py
"""
import os, argparse
import numpy as np
import matplotlib.pyplot as plt

# Approx orbital periods in days (inner → outer, editable)
PLANETS = {
    "Mercury": 87.969,
    "Venus":   224.701,
    "Earth":   365.256,
    "Mars":    686.980,
    "Jupiter": 4332.59,
    "Saturn":  10759.22,
    "Uranus":  30688.5,
    "Neptune": 60182.0,
}

def ratios(ref="Earth"):
    pref = PLANETS[ref]
    names, vals = [], []
    for k, P in PLANETS.items():
        names.append(k)
        vals.append(P / pref)  # period ratio to reference
    return names, np.array(vals)

def save_bar(names, vals, out="sims/figures/orbital_ratios.png"):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    x = np.arange(len(names))
    plt.figure(figsize=(9,4))
    plt.bar(x, vals)
    plt.xticks(x, names, rotation=0)
    plt.ylabel("Period ratio to reference")
    plt.title("Orbital period ratios (toy)")
    plt.tight_layout(); plt.savefig(out, dpi=150)

def save_spiral(names, vals, turns=6, out="sims/figures/orbital_ratios_spiral.png"):
    # map ratios to radii, place along a logarithmic spiral
    n = len(vals)
    t = np.linspace(0, 2*np.pi*turns, n)
    r = 0.25*np.exp(0.25*t) * (0.7 + 0.3*(vals/vals.max()))
    x = r*np.cos(t); y = r*np.sin(t)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    plt.figure(figsize=(6,6))
    plt.scatter(x, y, s=40)
    for i, name in enumerate(names):
        plt.text(x[i], y[i], name, fontsize=8)
    plt.axis('equal'); plt.title("Orbital ratios spiral (toy)")
    plt.tight_layout(); plt.savefig(out, dpi=150)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", type=str, default="Earth", help="reference planet")
    args = ap.parse_args()
    names, vals = ratios(args.ref)
    save_bar(names, vals)
    save_spiral(names, vals)
    print("Saved sims/figures/orbital_ratios.png")
    print("Saved sims/figures/orbital_ratios_spiral.png")

if __name__ == "__main__":
    main()
