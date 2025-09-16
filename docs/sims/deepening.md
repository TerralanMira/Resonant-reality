# Deepening the Simulations — multi-scale, hybrid, and geometry

This folder contains deeper simulation stubs that connect theory → practice.

## Files added
- `sims/kuramoto_schumann_hybrid.py` — human oscillators coupled to a Schumann-like driver; includes simple feedback from collective coherence into driver amplitude.
- `sims/multi_scale_kuramoto.py` — nested clusters showing local locking vs global locking.
- `sims/lc_grid_modes.py` — Laplacian eigenmodes demo as a geometry → spectrum analog.

## How to run
From the repository root (Python 3.9+ recommended):
```bash
pip install -r requirements.txt   # ensure numpy, matplotlib, scipy
python sims/kuramoto_schumann_hybrid.py
python sims/multi_scale_kuramoto.py
python sims/lc_grid_modes.py
Figures saved to sims/figures/.

What each sim shows (pass / falsifier)
	•	Kuramoto-Schumann hybrid
	•	Pass: R increases when driver amplitude/feedback rises; driver_amp responds to R.
	•	Falsifier: no change in R for any parameter sweep → revisit coupling or dt.
	•	Multi-scale Kuramoto
	•	Pass: cluster R high while global R low at low inter-coupling; global R rises as inter-coupling increases.
	•	Falsifier: clusters never show differential behavior → check cluster construction or K_intra.
	•	LC grid modes
	•	Pass: clear spatial eigenmodes and a low-mode spectrum.
	•	Falsifier: flat spectrum / failure to compute eigenvalues → numerical issue (try smaller grid).

Next simulation steps (grow the lab)
	1.	Integrate real Schumann / geomagnetic time series (data ingestion notebook).
	2.	Create Kuramoto clusters whose natural frequencies are drawn from HRV distributions.
	3.	Couple LC grid modes to Kuramoto clusters located at node coordinates (city ↔ Earth model).
	4.	Build a Jupyter notebook that runs parameter sweeps, saves figures, and logs pass/falsifier results.
