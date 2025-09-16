#!/usr/bin/env python3
"""
Atlas Overlay — stub

Concept:
- Plot a simple spiral (the 'memory of the whole').
- Overlay Earth sites from earth/data/sites.json on a lon/lat scatter.
- One figure, default matplotlib settings (no seaborn), saved to sims/figures/atlas_overlay.png
"""

from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt

# Paths
ROOT = Path(__file__).resolve().parents[1]   # .../sims
DATA = ROOT.parent / "earth" / "data" / "sites.json"
OUTDIR = ROOT / "figures"
OUTDIR.mkdir(parents=True, exist_ok=True)
OUTPNG = OUTDIR / "atlas_overlay.png"

def load_sites(path: Path):
    if not path.exists():
        print(f"Data not found: {path}")
        return []
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    pts = []
    if isinstance(data, list):
        for s in data:
            if "lat" in s and "lon" in s:
                pts.append((float(s["lon"]), float(s["lat"]), s.get("name","")))
    return pts

def spiral_points(turns=3, steps=600, scale_x=180.0, scale_y=90.0):
    """
    Parametric spiral in abstract space, scaled into lon/lat bounds.
    This is illustrative (not a geodesic); it’s a myth→math overlay.
    """
    t = np.linspace(0.0, 2.0*np.pi*turns, steps)
    r = np.linspace(0.1, 1.0, steps)   # outward growth from center
    x = scale_x * r * np.cos(t)        # ~ -180..180
    y = scale_y * r * np.sin(t)        # ~  -90..90
    return x, y

def main():
    sites = load_sites(DATA)
    sx, sy = spiral_points(turns=3, steps=800)

    plt.figure(figsize=(10,5))
    # Spiral path
    plt.plot(sx, sy, linewidth=1.5)
    # Sites overlay
    if sites:
        xs = [p[0] for p in sites]
        ys = [p[1] for p in sites]
        plt.scatter(xs, ys, s=25)
        # Light labeling for first few to avoid clutter
        for (x, y, name) in sites[:8]:
            plt.text(x, y, f" {name}", fontsize=8)

    plt.title("Atlas Overlay — spiral memory over planetary nodes (conceptual)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.xlim(-180, 180)
    plt.ylim(-90, 90)
    plt.grid(True, linewidth=0.3)
    plt.tight_layout()
    plt.savefig(OUTPNG, dpi=150)
    print(f"Saved: {OUTPNG}")

if __name__ == "__main__":
    main()
