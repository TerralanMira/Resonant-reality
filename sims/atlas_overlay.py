#!/usr/bin/env python3
"""
Atlas Overlay — stub

Conceptual overlay:
- Draws a simple spiral (memory of the whole).
- Plots Earth sites (from earth/data/sites.json) on a lon/lat scatter.
- Shows how mythic spiral and planetary nodes can be seen in one view.

Outputs: sims/figures/atlas_overlay.png
"""

from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
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
    for s in data if isinstance(data, list) else []:
        if "lat" in s and "lon" in s:
            pts.append((float(s["lon"]), float(s["lat"]), s.get("name","")))
    return pts

def spiral_points(turns=3, steps=600, scale_x=180, scale_y=90):
    # Parametric spiral in abstract space, scaled to lon/lat ranges
    t = np.linspace(0, 2*np.pi*turns, steps)
    r = np.linspace(0.1, 1.0, steps)  # outward growth
    x = scale_x * r * np.cos(t)       # map to -180..180 ish
    y = scale_y * r * np.sin(t)       # map to  -90..90 ish
    return x, y

def main():
    sites = load_sites(DATA)
    # Spiral
    sx, sy = spiral_points()

    plt.figure(figsize=(10,5))
    # Spiral line
    plt.plot(sx, sy, linewidth=1.5)
    # Sites
    if sites:
        xs = [p[0] for p in sites]
        ys = [p[1] for p in sites]
        plt.scatter(xs, ys, s=25)
        # label a few to avoid clutter
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
