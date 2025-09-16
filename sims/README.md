# Simulations Hub — myth → math → visible coherence

This folder contains runnable Python models that make resonance **visible**.

## Core sims (start here)
- `spiral_resonance.py` — spiral → coherence (animated/gif)
- `kuramoto_basic.py` — many oscillators syncing as coupling rises
- `lc_grid.py` — geometry shapes resonance spectra (LC modes)
- `schumann_coupling.py` — Earth–brain entrainment window near 7.83 Hz
- `resonant_currency.py` — policy as conductor for coherence-stable value
- `reciprocity_network.py` — economy as balanced give/receive flows

## How to run
```bash
pip install -r sims/requirements.txt
python sims/run_all.py
Figures land in sims/figures/.

Tips
	•	Keep sims minimal and interpretable.
	•	Every sim should:
	1.	Plot or save a figure in sims/figures/
	2.	Print a brief “what happened” line
	3.	Have a matching doc page in docs/sims/
