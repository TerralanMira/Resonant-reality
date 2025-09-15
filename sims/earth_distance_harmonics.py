#!/usr/bin/env python3
"""
Earth Distance Harmonics — stub

Reads earth/data/sites.json, computes great-circle distances between sites,
and highlights pairs that sit near simple harmonic bands (e.g., multiples of 1000 km).
Outputs a single chart to sims/figures/earth_harmonics.png

Notes:
- Minimal dependencies: numpy, matplotlib, math, json
- One figure (no subplots), default colors
"""

import json, math
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]  # repo root/sims
DATA = ROOT.parent / "earth" / "data" / "sites.json"
OUTDIR = ROOT / "figures"
OUTDIR.mkdir(parents=True, exist_ok=True)
OUTPNG = OUTDIR / "earth_harmonics.png"

EARTH_RADIUS_KM = 6371.0

def haversine_km(lat1, lon1, lat2, lon2):
    # Convert to radians
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi  = math.radians(lat2 - lat1)
    dlamb = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlamb/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    return EARTH_RADIUS_KM * c

def load_sites(path: Path):
    if not path.exists():
        print(f"Data not found: {path}")
        return []
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    sites = []
    for s in data if isinstance(data, list) else []:
        if "lat" in s and "lon" in s:
            sites.append({
                "name": s.get("name", ""),
                "lat": float(s["lat"]),
                "lon": float(s["lon"])
            })
    return sites

def main():
    sites = load_sites(DATA)
    if len(sites) < 2:
        print("Need at least two sites.")
        return

    # Compute pairwise distances
    pairs = []
    for i in range(len(sites)):
        for j in range(i+1, len(sites)):
            a, b = sites[i], sites[j]
            d = haversine_km(a["lat"], a["lon"], b["lat"], b["lon"])
            pairs.append((a["name"], b["name"], d))
    dists = np.array([p[2] for p in pairs])

    # Simple harmonic bands (illustrative): 1000 km multiples
    base = 1000.0
    max_d = max(dists) if len(dists) else 40000.0
    bands = np.arange(base, max_d+base, base)

    # Plot histogram of distances, overlay bands
    plt.figure(figsize=(9,5))
    plt.hist(dists, bins=30, alpha=0.7)
    for b in bands:
        plt.axvline(b, linewidth=0.8)

    plt.title("Great-circle Distances Between Sites (with simple harmonic bands)")
    plt.xlabel("Distance (km)")
    plt.ylabel("Pair count")
    plt.tight_layout()
    plt.savefig(OUTPNG, dpi=150)
    print(f"Saved: {OUTPNG}")

if __name__ == "__main__":
    main()
