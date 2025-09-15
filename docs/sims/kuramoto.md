# Kuramoto Synchronization

This sim is the **canonical model of collective resonance**:  
many oscillators with random frequencies, gradually locking as coupling grows.

---

## What it shows
- N oscillators each with a natural frequency (random).
- At low coupling → noise, fragmentation.  
- At high coupling → emergent coherence, shared hum.

---

## How to run

```bash
python sims/kuramoto_basic.py
Output:
	•	Plot of order parameter R(t) across time.
	•	Saved to: sims/figures/kuramoto_R.png

⸻

Pass / Falsifier
	•	✅ Pass: as K increases, R → 1 (strong coherence).
	•	❌ Falsifier: R remains flat, no locking.
