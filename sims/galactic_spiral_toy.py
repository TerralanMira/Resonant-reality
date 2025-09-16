"""
Galactic Spiral Toy — draws a logarithmic spiral and its radial intensity profile.

Run:
    python sims/galactic_spiral_toy.py

Outputs:
    sims/figures/galactic_spiral.png
    sims/figures/galactic_radial_profile.png
"""
import os
import numpy as np
import matplotlib.pyplot as plt

def make_spiral(a=0.2, b=0.25, turns=4, points=4000):
    t = np.linspace(0, 2*np.pi*turns, points)
    r = a * np.exp(b * t)
    x = r * np.cos(t)
    y = r * np.sin(t)
    return x, y

def plot_spiral(x, y, out_dir="sims/figures"):
    os.makedirs(out_dir, exist_ok=True)
    plt.figure(figsize=(6,6))
    plt.scatter(x, y, s=0.5)
    plt.axis('equal')
    plt.title("Logarithmic Spiral (toy galactic arm)")
    path = os.path.join(out_dir, "galactic_spiral.png")
    plt.savefig(path, dpi=150)
    print("Saved", path)

def radial_profile(x, y, bins=200, out_dir="sims/figures"):
    r = np.sqrt(x**2 + y**2)
    hist, edges = np.histogram(r, bins=bins)
    centers = 0.5*(edges[:-1] + edges[1:])
    os.makedirs(out_dir, exist_ok=True)
    plt.figure(figsize=(8,3))
    plt.plot(centers, hist)
    plt.xlabel("radius")
    plt.ylabel("intensity (counts)")
    plt.title("Radial intensity profile (toy)")
    path = os.path.join(out_dir, "galactic_radial_profile.png")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    print("Saved", path)

if __name__ == "__main__":
    x, y = make_spiral()
    plot_spiral(x, y)
    radial_profile(x, y)
