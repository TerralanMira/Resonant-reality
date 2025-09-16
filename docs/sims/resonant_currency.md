# Simulation — Resonant Currency

A toy model of **policy-as-conductor**, where a local token supply  
adjusts dynamically in response to a *coherence index* (C) and price drift.  
This lets us explore how money itself can become a **resonance amplifier**  
instead of a blind extraction mechanism.

---

## What It Models

- **Agents** contribute more when collective coherence is high.  
- **Demand** rises with coherence, falls if price rises too far above 1.0.  
- **Supply** expands when coherence is strong, contracts when price drifts.  
- **Price** is the ratio of demand to supply — tuned around 1.0.  

The system behaves like a **feedback instrument**:  
growth in coherence → abundance; turbulence → contraction and stability.

---

## Code Reference

See [`sims/resonant_currency.py`](../../sims/resonant_currency.py).

**Outputs (figures):**

- `sims/figures/resonant_currency_price.png`  
- `sims/figures/resonant_currency_supply.png`  

---

## How to Run

```bash
python sims/resonant_currency.py
python sims/resonant_currency.py --T 600 --agents 400 --alpha 0.08 --beta 0.06 --seed 7
•	--T: number of timesteps
	•	--agents: number of contributing agents
	•	--alpha: policy sensitivity to coherence
	•	--beta: policy sensitivity to price error

⸻

What to Look For
	•	Price trace (resonant_currency_price.png)
	•	Should hover around 1.0
	•	Expansions during high coherence
	•	Corrections when price drifts
	•	Supply trace (resonant_currency_supply.png)
	•	Expands when coherence and contributions rise
	•	Contracts when noise or turbulence dominates

⸻

Interpretations
	•	Abundance emerges when collective rhythm is strong.
	•	Stability arises when contraction reins in drift.
	•	Participation is rewarded — coherence isn’t abstract, it’s felt and earned.
	•	A resonant economy behaves less like a market machine and more like a musical ensemble.

⸻

Next Steps
	•	Cross-link with docs/civic/economy.md.
	•	Add experiments: varying coherence patterns, shocks, or policy rules.
	•	Compare to real-world analogues: local currencies, time banks, crypto DAOs.
	•	Explore: Could global resonant tokens stabilize planetary-scale coherence?
