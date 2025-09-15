#!/usr/bin/env python3
"""
Generate a quick-look map of Earth sites from earth/data/sites.json.
Output PNG: docs/assets/figs/earth_sites.png

Notes:
- Uses matplotlib only (no seaborn).
- Single chart, default colors.
"""

from pathlib import Path
import json
import os
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]  # repo root
DATA = ROOT / "earth" / "data" / "sites.json"
OUTDIR = ROOT / "docs" / "assets" / "figs"
OUTDIR.mkdir(parents=True, exist_ok=True)
OUTPNG = OUTDIR / "earth_sites.png"

def main():
    if not DATA.exists():
        print(f"Data not found: {DATA}")
        return

    with DATA.open("r", encoding="utf-8") as f:
        sites = json.load(f)

    # Extract lon/lat safely
    lats, lons, names = [], [], []
    for s in sites if isinstance(sites, list) else []:
        if "lat" in s and "lon" in s:
            lats.append(s["lat"])
            lons.append(s["lon"])
            names.append(s.get("name", ""))

    # Plot
    plt.figure(figsize=(10, 5))
    plt.scatter(lons, lats, s=20)  # default style, single chart
    plt.title("Resonant Earth Sites (scatter)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.xlim(-180, 180)
    plt.ylim(-90, 90)
    plt.grid(True, linewidth=0.3)

    # Light annotation for first few to avoid clutter
    for lon, lat, name in list(zip(lons, lats, names))[:8]:
        plt.text(lon, lat, f" {name}", fontsize=8)

    plt.tight_layout()
    plt.savefig(OUTPNG, dpi=150)
    print(f"Saved: {OUTPNG}")

if __name__ == "__main__":
    main()
