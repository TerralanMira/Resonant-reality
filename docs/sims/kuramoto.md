# Kuramoto Synchronization — phase locking → coherence

**What it shows:** As coupling **K** increases, many oscillators shift from scattered phases to a coherent state.  
**Metric:** order parameter **R(t) ∈ [0,1]** (0 = scattered, 1 = locked).

## Run
```bash
python sims/kuramoto_basic.py
Output: sims/figures/kuramoto_R.png

Read the plot
	•	Low K: R stays low and noisy.
	•	High K: R rises and stabilizes → coherence.

Why it matters

Micro alignment → macro order. This underpins Conductor cycles and civic coherence.

Falsifier hook

If increasing K does not raise mean R in the final 20% of steps → claim fails here.
---

### 3) LC Grid doc
**Path:** `docs/sims/lc_grid.md`
```markdown
# LC Grid Modes — geometry shapes resonance

**What it shows:** A simple LC chain’s eigenfrequencies depend on **layout and coupling**. Geometry → spectrum.  
**Why it matters:** Domes, circles, spirals bias mode families (design ↔ physics).

## Run
```bash
python sims/lc_grid.py
Output: sims/figures/lc_modes.png

Read the plot
	•	Frequencies vs mode index. Tuning alpha (coupling) shifts the spectrum.

Falsifier hook

If geometry/coupling changes do not shift mode frequencies as predicted → claim fails here.
---

### 4) Schumann doc
**Path:** `docs/sims/schumann.md`
```markdown
# Schumann Coupling — entrainment near 7.83 Hz

**What it shows:** A damped oscillator driven near **7.83 Hz** exhibits an **entrainment window** (high correlation with the drive).  
**Why it matters:** Local systems can lock to planetary baseline (Earth Layer).

## Run
```bash
python sims/schumann_coupling.py
Output: sims/figures/schumann_entrainment.png

Read the plot
	•	Peak correlation near ~7.8 Hz → entrainment zone (bandwidth set by damping).

Falsifier hook

If no peak forms near baseline (within damping-appropriate band) → claim fails here.
---

### 5) MkDocs nav (adds Sims section)
Add this block to `mkdocs.yml` (where you want it in the sidebar):
```yaml
- Simulations:
    - Overview: sims/index.md
    - Quickstart: sims/quickstart.md
    - Spiral Resonance: sims/spiral_resonance.md
    - Kuramoto Sync: sims/kuramoto.md
    - LC Grid Modes: sims/lc_grid.md
    - Schumann Coupling: sims/schumann.md
