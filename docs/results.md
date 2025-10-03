# Collective Results — Proof & Plots

This page shows the **visible shift** when a coherent cohort nudges a multi-zone city model under a shared lock.

## How to Reproduce

1. **Run the collective simulation**
```bash
python -m sims.collective_demo --scenario coherent --steps 240 --export json,csv --outdir out/collective
	2.	Render plots
python -m sims.plot_collective --csv out/collective/collective_series.csv --outdir out/collective/plots
	3.	Inspect outputs

	•	out/collective/plots/coherence_per_zone.png
	•	out/collective/plots/noise_per_zone.png
	•	out/collective/plots/coupling_per_zone.png

What to Look For
	•	Coherence per Zone
Plaza coherence should trend higher under a coherent cohort relative to baseline. Hearth remains steady; Wild is more sensitive to noise.
	•	Noise per Zone
With coherent input, plaza noise stabilizes or declines; wild stabilizes more slowly due to background entropy and jitter.
	•	Coupling per Zone
Gradual increase indicates improved energy transfer and alignment between agents and space.

Key Takeaways
	•	Small, bounded influences accumulate into measurable macro-patterns.
	•	Lock settings (entropy threshold, grace factor) govern how quickly zones stabilize.
	•	This pipeline is deterministic, auditable, and reproducible: CSVs + plots from the exact run.
---

### `Makefile`
```make
# Makefile — quick commands for Proof & Plots

PY=python

run-collective:
	$(PY) -m sims.collective_demo --scenario coherent --steps 240 --export json,csv --outdir out/collective

plot-collective:
	$(PY) -m sims.plot_collective --csv out/collective/collective_series.csv --outdir out/collective/plots

proof:
	$(MAKE) run-collective
	$(MAKE) plot-collective
	@echo "Proof generated: out/collective/plots/*"

clean-proof:
	rm -rf out/collective
	@echo "Cleaned proof artifacts."
