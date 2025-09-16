# Reciprocity Network — Economy as Coherence

This minimal model treats an economy as a network seeking balance between **giving** and **receiving**.
If imbalance persists, the network fragments; if it decreases, coherence emerges.

## What it shows
- How simple feedback (coupling **K**) reduces average imbalance.
- Why reciprocity networks (mutual aid, gift cycles) stabilize civic coherence.

## How to run
```bash
python sims/reciprocity_network.py
# or explore parameters:
python sims/reciprocity_network.py --N 120 --T 600 --K 0.08 --seed 7 --save-csv
Figures will be saved in sims/figures/:
	•	reciprocity_network.png (imbalance over time)
	•	reciprocity_history.csv (optional)

Pass / Falsifier
	•	Pass: average imbalance trends ↓ toward ~0 for reasonable K.
	•	Falsifier: imbalance stuck high or exploding → model/assumption needs revision.

Next
	•	Add heterogenous K per agent (trust differences).
	•	Introduce shocks (resource scarcity) and test resilience.
	•	Couple this to Kuramoto Sync to study attention + reciprocity co-dynamics.
