# City Coupling — Humans as Resonant Nodes

**Claim:** human coherence (κ), binding (γ), and fascia/water charge (χ) can be treated as node weights that nudge a public zone (e.g., a plaza) toward higher coherence and lower noise.

## How it works
- `node_influence_from_human(kappa, gamma, chi)` converts personal metrics to deltas:
  - `zone_coherence_delta` (↑)
  - `noise_reduction_delta` (↓)
  - `coupling_gain_delta` (↑)
- Deltas are small and cumulative; many coherent humans → measurable shift.

## Try it (no files needed)
```bash
python -m sims.city_coupling_demo
Output: A JSON report with three cohorts (baseline, coherent, mixed) and the plaza’s metrics after aggregation.

Why this matters
	•	It shows a safe, observable pathway from Human Layer → City without personal data exposure.
	•	It is compatible with resonance_lock.json & ethics gates (consent-first principle).

See also
	•	adapters/human_to_city.py
	•	sims/human_layer_sim.py
	•	conductor/pulses/{resonance_lock.json, collective_lock.json}
