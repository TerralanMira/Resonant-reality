
```python
"""
Galactic Spiral Toy — draws logarithmic spirals and computes radial intensity.

Run:
    python sims/galactic_spiral_toy.py
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
    plt.scatter(x, y, s=0.5, c=np.linspace(0,1,len(x)), cmap='magma')
    plt.axis('equal')
    plt.title("Logarithmic Spiral (toy galactic arm)")
    out = os.path.join(out_dir, "galactic_spiral.png")
    plt.savefig(out, dpi=150)
    print("Saved", out)

def radial_profile(x, y, bins=200, out_dir="sims/figures"):
    r = np.sqrt(x**2 + y**2)
    hist, edges = np.histogram(r, bins=bins)
    centers = 0.5*(edges[:-1] + edges[1:])
    os.makedirs(out_dir, exist_ok=True)
    plt.figure(figsize=(8,3))
    plt.plot(centers, hist)
    plt.xlabel("radius")
    plt.ylabel("intensity (counts)")
    plt.title("Radial intensity profile of spiral (toy)")
    out = os.path.join(out_dir, "galactic_radial_profile.png")
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    print("Saved", out)

def main():
    x,y = make_spiral()
    plot_spiral(x,y)
    radial_profile(x,y)

if __name__ == "__main__":
    main()
# Galactic Spiral Toy — fractal above, fractal below

A simple generator of logarithmic spirals (a proxy for galactic arm geometry).
Generates:
- `sims/figures/galactic_spiral.png`
- `sims/figures/galactic_radial_profile.png`

---

## Run it
```bash
python sims/galactic_spiral_toy.py
What it shows
	•	Spiral geometry (visual) and radial intensity (spectrum-like).
	•	Useful as a visual metaphor and a starting point for spectral experiments.

Next steps
	•	Animate multiple arms (phase-offset).
	•	Compute 2D FFT to examine spatial frequency content.
	•	Connect to sims/spiral_resonance.py and docs/cosmos/galactic.md.
