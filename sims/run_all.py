"""
Run-All: executes a curated set of simulations and writes figures to sims/figures.
Usage:
    python sims/run_all.py
"""
import subprocess, sys, os

ROOT = os.path.dirname(os.path.abspath(__file__))

SIMS = [
    "spiral_resonance.py",
    "kuramoto_basic.py",
    "lc_grid.py",
    "schumann_coupling.py",
    "resonant_currency.py",
    "reciprocity_network.py",
    "governance_sync.py",
    "civic_coherence_grid.py",
    "meta_resonance.py",
    "planetary_orbital_resonance.py",
    "solar_hrv_correlation.py",
    "galactic_spiral_toy.py",
]

def run(cmd):
    print(">>", " ".join(cmd))
    subprocess.run(cmd, check=False)

if __name__ == "__main__":
    print("Running simulations… figures will be written to sims/figures/")
    py = sys.executable
    for sim in SIMS:
        path = os.path.join(ROOT, sim)
        if not os.path.exists(path):
            print(f"– Skipping (not found): {sim}")
            continue
        run([py, path])
    print("\nAll done.")
