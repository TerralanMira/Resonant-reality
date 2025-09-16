"""
Planetary Orbital Resonance — toy visualizer

Produces:
 - a plot of orbital period ratios (pairwise)
 - highlights near-integer ratio bands (resonance candidates)

Run:
    python sims/planetary_orbital_resonance.py
"""
import os
import numpy as np
import matplotlib.pyplot as plt

# Example orbital periods (days) for inner planets & some neighbors
PLANETS = {
    "Mercury": 87.97,
    "Venus": 224.70,
    "Earth": 365.26,
    "Mars": 686.98,
    "Jupiter": 4332.59,
    "Saturn": 10759.22
}

def pairwise_ratios(periods):
    names = list(periods.keys())
    n = len(names)
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            p1 = periods[names[i]]
            p2 = periods[names[j]]
            ratio = p2 / p1
            pairs.append((names[i], names[j], ratio))
    return pairs

def plot_ratios(pairs, out_dir="sims/figures"):
    os.makedirs(out_dir, exist_ok=True)
    labels = [f"{a}/{b}" for a,b,_ in pairs]
    ratios = np.array([r for _,_,r in pairs])
    plt.figure(figsize=(10,4))
    plt.bar(labels, ratios, color='tab:blue', alpha=0.8)
    plt.axhline(1.0, color='k', linestyle='--')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Period ratio")
    plt.title("Planetary orbital period ratios (larger / smaller)")
    # mark near-integer resonances
    for k in range(2,7):
        plt.axhline(k, color='orange', linestyle=':', alpha=0.6)
        plt.text(len(labels)-1, k+0.05, f"{k}:1", color='orange', va='bottom', ha='right')
    out = os.path.join(out_dir, "planetary_orbital_ratios.png")
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    print("Saved", out)

def main():
    pairs = pairwise_ratios(PLANETS)
    plot_ratios(pairs)

if __name__ == "__main__":
    main()
