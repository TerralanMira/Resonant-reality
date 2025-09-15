# Simulations — from myth to math

These minimal sims show the TOE’s claims as measurable dynamics.

## A) Kuramoto (phase-locking → coherence)
- File: `sims/kuramoto_basic.py`
- Idea: N oscillators with natural freqs ω_i phase-couple with strength K.
- Metric: **R(t)** in [0,1] (0 = scattered, 1 = locked). Claim: above a threshold K*, R rises.

## B) LC Grid (materials/geometry → resonance)
- File: `sims/lc_grid.py`
- Idea: nodes are LC resonators + nearest-neighbor coupling. Modes depend on layout (circle/line/spiral).

## C) Schumann Coupling (planetary baseline → entrainment)
- File: `sims/schumann_coupling.py`
- Idea: a damped oscillator driven near 7.83 Hz; shows entrainment windows.

### How to run (local)
```bash
pip install -r requirements.txt
python sims/kuramoto_basic.py
python sims/lc_grid.py
python sims/schumann_coupling.py
