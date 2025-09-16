# Resonant Currency — Policy as Conductor

A minimal model where a local token’s supply policy follows a **coherence index** (C ∈ [0,1])  
and stabilizes around **price ≈ 1** while rewarding contribution during high coherence.

## What it shows
- **Controller logic:** dS = α·C − β·(P−1)·K keeps price near target while allowing growth.
- **Coherence coupling:** higher C boosts contribution and issuance; low C tightens policy.
- **Stability tradeoff:** α (growth) vs β (stability) tunes resilience.

## How to run
```bash
python sims/resonant_currency.py
# explore:
python sims/resonant_currency.py --T 600 --agents 400 --alpha 0.08 --beta 0.06 --seed 7
Figures saved to sims/figures/:
	•	resonant_currency_price.png — price vs coherence (target = 1.0)
	•	resonant_currency_supply.png — circulating supply over time

Pass / Falsifier
	•	Pass: price hovers near 1 with reasonable α, β; supply adapts smoothly.
	•	Falsifier: runaway price or wild oscillations across broad α, β → controller needs redesign.

Next
	•	Couple to Reciprocity Network (attention + contribution co-dynamics).
	•	Make C(t) an input from real data (HRV/geomagnetic indices).
	•	Introduce shocks (resource scarcity, demand spike) and test policy robustness.
