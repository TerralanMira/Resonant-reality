# Planetary Orbital Resonance — metronomes of the sky

This toy visualizer shows pairwise orbital period ratios for selected planets,
highlighting near-integer bands where resonances commonly appear (e.g., 2:1, 3:1).

---

## What it shows
- Period ratios (larger/smaller) for planet pairs.
- Integer bands marked as candidate resonance windows.

## Run it
```bash
python sims/planetary_orbital_resonance.py
Output
	•	sims/figures/planetary_orbital_ratios.png

Notes
	•	Use as a visualization primer. Extend by importing real ephemeris time series,
computing moving-window commensurabilities, or animating conjunction cycles.
