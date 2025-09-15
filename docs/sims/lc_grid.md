# LC Grid Modes — geometry shapes resonance

A minimal LC lattice shows how **layout and coupling** determine the resonance spectrum.  
Change the geometry → change the modes. This is the design ↔ physics bridge.

---

## What it shows
- A 1D/2D LC grid with nearest-neighbor coupling.
- Mode frequencies shift as coupling **α** changes.
- Design implication: domes/circles/spirals bias mode families.

---

## How to run
```bash
python sims/lc_grid.py
Output

Saved to:sims/figures/lc_modes.png
Read the plot
	•	X-axis: mode index. Y-axis: frequency (normalized).
	•	Increasing α → modes spread/shift; edge conditions matter.

⸻

Pass / Falsifier
	•	✅ Pass: changing geometry/coupling moves the mode frequencies.
	•	❌ Falsifier: spectrum stays unchanged despite geometry/coupling changes.
