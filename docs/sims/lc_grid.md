# LC Grid Modes — Geometry Shapes Resonance

This simulation explores how arrays of inductors (L) and capacitors (C) form  
standing-wave modes depending on geometry and boundary conditions.  

It’s a minimal toy model showing how **spatial layout tunes spectral response** —  
like how the Earth–ionosphere cavity supports Schumann resonances.

---

## Concept

- An **LC grid** behaves like a discrete resonant medium.  
- Changing the grid’s **size** or **boundary conditions** shifts the mode spectrum.  
- Useful analogy: cities, hearts, and ecosystems all show similar “resonant lattices.”  

---

## What It Shows

- Eigenmodes of the LC grid (frequencies + mode shapes).  
- How geometry determines which resonances dominate.  
- Why scaling up/down produces predictable frequency shifts.  

---

## Run It

```bash
python sims/lc_grid.py
This generates mode plots and saves them to:
	•	sims/figures/lc_grid.png

⸻

Outputs
	•	A visual map of the lowest eigenmodes of the LC lattice.
	•	Frequencies vs. mode index (spectrum).

Example (after running):
	•	Mode 1: uniform in-phase oscillation
	•	Mode 2+: alternating phase bands across the grid

⸻

Implications
	•	Physics: Earth’s Schumann cavity acts like an LC shell; geometry → frequencies.
	•	Biology: Cardiac + neural networks rely on lattice-like coupling.
	•	Civic: Cities with grid/plaza geometries may “tune” collective resonance.

⸻

Next Steps
	•	Compare LC grid modes with Schumann frequencies.
	•	Cross-link to docs/sims/schumann.md.
	•	Explore larger grid sizes (e.g. 10x10 vs 20x20) to show scaling laws.
	•	Add figures from sims/figures/lc_grid.png to the gallery in docs/sims/index.md.
