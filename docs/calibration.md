# Calibration — Choosing the Right Lock

**Goal:** make comparisons **visible and repeatable** by running identical scenarios with different calibration profiles.

## Locks

- `calibration/res_lock.v1.low_noise.json`  
  Conservative; emphasizes stability (higher grace, lower amplitude range).
- `calibration/res_lock.v1.medium.json`  
  Balanced; default for public demos.
- `calibration/res_lock.v1.high_harmonic.json`  
  Exploratory; higher harmonics with tighter windows.

All inherit from `conductor/pulses/resonance_lock.json` and can be used by sims.

## Quick Bench

```bash
python scripts/bench_collective.py --steps 240 --outdir out/bench --seed 42
Outputs
	•	out/bench/bench_results.csv — table of zone means/min/max across locks × scenarios
	•	out/bench/bench_results.json — same data as JSON

Read the Results
	•	Higher plaza_coherence_mean + lower plaza_noise_mean indicates better public-space alignment.
	•	Compare wild responses to check stability and jitter under the same lock.
	•	Use low_noise when you need robust behavior; use high_harmonic for learning-edge experiments.

Tip: Pair with docs/results.md to generate plots for a chosen run and visually confirm trends.
