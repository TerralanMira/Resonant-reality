# Governance Sync — Councils as Kuramoto

Deliberation can be modeled as **oscillators seeking phase-lock** around shared attractors (values, proposals).

## What it shows
- With **low coupling** → factions drift (low coherence).
- With **high coupling** → brittle lockstep.
- A **middle band** sustains phase-locked diversity.

## How to run
```bash
python sims/governance_sync.py
Output: sims/figures/governance_sync_R.png (order parameter R over time)

Pass / Falsifier
	•	Pass: R rises smoothly in a mid-coupling band.
	•	Falsifier: Only chaos or only lockstep across all couplings.

Next
	•	Heterogeneous trust (agent-specific coupling).
	•	Media shocks (time-varying coupling).
	•	Link to: docs/civic/governance.md
