# Spiral Resonance

This sim shows how **local oscillations spiral outward** into coherent global patterns.  
It’s a micro → macro demonstration: the hum of one loop entrains the field, and the field folds back on the loop.

---

## What it shows
- Individual oscillators arranged in a spiral geometry.
- Coupling strength shapes whether coherence emerges.
- The resonance “ripples out” — coherence grows layer by layer.

---

## How to run

```bash
python sims/spiral_resonance.py
Output:
	•	Animated spiral of oscillators.
	•	Coherence metric saved to sims/figures/spiral.png

⸻

Pass / Falsifier
	•	✅ Pass: coherence order parameter rises above 0.6 across the spiral.
	•	❌ Falsifier: coherence stays near 0 → oscillators remain fragmented.
