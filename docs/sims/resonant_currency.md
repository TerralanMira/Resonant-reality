# Resonant Currency — Policy-as-Conductor

A minimal macro–micro toy model for a **local token** whose policy targets  
a "coherence index" `C_t` in `[0,1]`.  

- The token supply adjusts dynamically to keep **real price ~ 1.0**  
- Agents earn more tokens when coherence is high  
- The system rewards contribution while dampening instability  

---

## Model Intuition

- **Coherence `C_t`** acts like group HRV, geomagnetic calm, or participation rate.  
- **Demand** rises when coherence is high, but falls if price drifts above 1.  
- **Policy rule** expands supply with coherence, contracts it if price > 1.  
- **Result**: contributions flourish under coherence without runaway inflation.  

---

## Equations (toy form)

- Contribution rate: `contrib_t ∝ agents × C_t`  
- Demand: `D_t ∝ (1 + (C_t - 0.5)) × (1 - elastic × (P_t - 1))`  
- Price: `P_t ≈ D_t / (S_t / 1000)`  
- Policy: `ΔS = α·C_t·contrib_t - β·(P_t - 1)·1000`

---

## Outputs

Running the sim produces two figures:

- `sims/figures/resonant_currency_price.png`  
  → token price vs coherence index  
- `sims/figures/resonant_currency_supply.png`  
  → circulating supply over time  

---

## Run

```bash
python sims/resonant_currency.py
Extended run with parameters:
python sims/resonant_currency.py --T 600 --agents 400 --alpha 0.08 --beta 0.06 --seed 7
Research Directions
	•	Can coherence-based issuance stabilize local economies?
	•	How might collective practices (meditation, festivals, civic rituals) shift C_t?
	•	Could resonant currency smooth volatility better than standard monetary policy?
	•	Link to docs/civic/economy.md for applications.

⸻

Gallery (to be updated)
	•	Price vs Coherence — (placeholder: sims/figures/resonant_currency_price.png)
	•	Circulating Supply — (placeholder: sims/figures/resonant_currency_supply.png)
