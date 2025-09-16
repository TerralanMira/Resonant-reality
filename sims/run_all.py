```python
"""
Run-All: executes a curated set of simulations and writes figures to sims/figures.
Usage:
    python sims/run_all.py
"""
import subprocess, sys, os, textwrap

ROOT = os.path.dirname(os.path.abspath(__file__))
---

```python
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
    print("\n" + "="*72)
    print("RUN:", " ".join(cmd))
    print("="*72)
    proc = subprocess.run(cmd, cwd=ROOT)
    if proc.returncode != 0:
        print(f"!! Failed: {' '.join(cmd)}")
        sys.exit(proc.returncode)

def ensure_fig_dir():
    fig = os.path.join(ROOT, "figures")
    os.makedirs(fig, exist_ok=True)
    return fig

if __name__ == "__main__":
    ensure_fig_dir()
    print(textwrap.dedent("""
    Running core simulations…
    Figures will be written to sims/figures/.
    """).strip())

    # Use the same interpreter to avoid env mismatch
    py = sys.executable

    for sim in SIMS:
        path = os.path.join(ROOT, sim)
        if not os.path.exists(path):
            print(f"– Skipping (not found): {sim}")
            continue
        run([py, sim])

    print("\nAll done. Check sims/figures/ for outputs.")
