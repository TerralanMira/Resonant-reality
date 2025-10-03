# Collective Simulation — Multi-Zone Resonance

**What it is:** A time-based simulation where human cohorts (κ, γ, χ) nudge multiple zones (hearth, plaza, wild). It demonstrates how coherent humans shift a public space’s coherence/noise/coupling under a shared lock.

## Run
```bash
python -m sims.collective_demo --scenario coherent --steps 240 --export json,csv --outdir out/collective
	•	--scenario: baseline | coherent | mixed | custom
	•	--custom_path: JSON list of {kappa, gamma, chi} for custom cohorts
	•	--lock: optional path to conductor/pulses/collective_lock.json

Output
	•	out/collective/collective_series.csv — per-step zone metrics
	•	out/collective/collective_results.json — time-series + summaries
