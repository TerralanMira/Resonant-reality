#!/usr/bin/env python3
"""
Earth Grid Coherence — stub

Generates a conceptual "standing-wave" field over lon/lat using simple
sin/cos patterns (a separable proxy for planetary modes) and saves a heatmap.

- Single chart (no subplots), default matplotlib colors/styles.
- No seaborn. Output saved to sims/figures/lc_grid.png
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# Paths
ROOT = Path(__file__).resolve().parents[1]   # .../sims
OUTDIR = ROOT / "figures"
OUTDIR.mkdir(parents=True, exist_ok=True)
OUTPNG = OUTDIR / "lc_grid.png"

def field(lon_deg, lat_deg, k_lon=6, k_lat=3):
    """
    Conceptual standing-wave pattern over degrees.
    Not true spherical harmonics; illustrative only.
    """
    lon = np.radians(lon_deg)
    lat = np.radians(lat_deg)
    return np.sin(k_lat * lat) * np.cos(k_lon * lon)

def main():
    # Build a lon/lat grid
    lon = np.linspace(-180, 180, 361)   # 1-degree steps
    lat = np.linspace(-90, 90, 181)     # 1-degree steps
    LON, LAT = np.meshgrid(lon, lat)

    # Compute intensity field
    Z = field(LON, LAT, k_lon=6, k_lat=3)

    # Render heatmap
    plt.figure(figsize=(10,5))
    plt.imshow(
        Z,
        extent=[-180, 180, -90, 90],
        origin="lower",
        aspect="auto",
    )
    plt.title("Earth Grid Coherence — conceptual standing-wave pattern")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.colorbar(label="Intensity")
    plt.tight_layout()
    plt.savefig(OUTPNG, dpi=150)
    print(f"Saved: {OUTPNG}")

if __name__ == "__main__":
    main()
