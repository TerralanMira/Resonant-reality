# Schumann Resonance Coupling

This sim explores the **entrainment window** near Earth’s natural resonance (~7.83 Hz).  
It shows how local oscillators can lock into the planetary hum.

---

## What it shows
- A driven oscillator with a frequency sweep near 7–8 Hz.
- Locking occurs when drive frequency ≈ Schumann band.
- Visual: phase slip → phase lock.

---

## How to run
```bash
python sims/schumann_coupling.py
Output

Saved to: sims/figures/schumann.png
Read the plot
	•	X-axis: time steps.
	•	Y-axis: phase difference between oscillator and driver.
	•	Locking visible as phase difference stabilizes.

⸻

Pass / Falsifier
	•	✅ Pass: phase lock occurs near ~7.83 Hz.
	•	❌ Falsifier: no visible lock around Schumann band.
