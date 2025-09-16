# Meta-Resonance — Coupling Humans, Earth, and Civic Pulses

This simulation shows **nested coherence**:
- Human clusters (hearths/neighborhoods)
- Planetary driver (Schumann-like band)
- Civic pulses (festivals/rituals) that temporarily boost coupling

It’s the *bridge* from myth → math → visible coherence.

## Run
```bash
python sims/meta_resonance.py
Figures saved to:
	•	sims/figures/meta_resonance_R.png
	•	sims/figures/meta_resonance_layers.png

What to look for
	•	Local-first locking: cluster R rises before global R.
	•	Pulse windows: during civic pulses, global R jumps.
	•	Feedback loop: as global R rises, driver amplitude nudges higher (simple model).

Pass / Falsifier
	•	Pass: global R exhibits plateaus or step-ups during pulses; cluster R stays > global R when inter-coupling is low.
	•	Falsifier: no change in R across parameter sweeps (e.g., raising K_inter, G, or alpha_feedback does nothing) → revisit values or dt.

Next
	•	Drive with real data (Schumann/geomagnetic time series).
	•	Place clusters at Earth nodes; couple to LC grid modes.
	•	Let ritual calendars (equinox/solstice) set pulse timing.
