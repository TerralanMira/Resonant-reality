#!/usr/bin/env python3
"""
Earth Grid Coherence — stub

Creates a simple "standing wave" style field on a lon/lat grid using
sin/cos patterns (conceptual spherical modes), and renders a heatmap.
This is independent of lc_grid.py and serves as a quick Earth-layer visual.

Outputs: sims/figures/lc_grid.png
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "figures"
OUTDIR.mkdir(parents=True, exist_ok=True)
OUTPNG = OUTDIR / "lc_grid.png"

def field(lon_deg, lat_deg, k_lon=6, k_lat=3):
    # Simple separable pattern in degrees (conceptual, not spherical harmonics)
    lon = np.radians(lon_deg)
    lat = np.radians(lat_deg)
    return np.sin(k_lat * lat) * np.cos(k_lon * lon)

def main():
    # Grid
    lon = np.linspace(-180, 180, 361)
    lat = np.linspace(-90, 90, 181)
    LON, LAT = np.meshgrid(lon, lat)

    Z = field(LON, LAT, k_lon=6, k_lat=3)

    plt.figure(figsize=(10,5))
    plt.imshow(Z, extent=[-180,180,-90,90], aspect='auto', origin='lower')
    plt.title("Earth Grid Coherence — conceptual standing-wave pattern")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.colorbar(label="Intensity")
    plt.tight_layout()
    plt.savefig(OUTPNG, dpi=150)
    print(f"Saved: {OUTPNG}")

if __name__ == "__main__":
    main()
