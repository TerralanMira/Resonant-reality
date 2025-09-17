# Plaza Simulation — Space-as-Conductor (toy)

**What it shows**  
A circular **plaza** with a soft center “beat” can **amplify synchrony** among wandering agents.  
Agents entrain (a) to nearby neighbors and (b) to a gentle **center source**.  
This models how **architecture + ritual** can raise collective coherence.

---

## How it works (intuition)

- Each agent carries a phase `θ_i` (think: breath/HRV/attention rhythm).  
- Local coupling: agents nudge toward the **mean phase** of nearby neighbors.  
- Center coupling: a slow **source phase** at the heart of the plaza (ritual drum, chant, bell).  
- The **global order parameter** `R = |⟨e^{iθ}⟩|` rises when synchrony emerges.

---

## Run

```bash
python sims/plaza.py
# tweak:
python sims/plaza.py --N 250 --T 2000 --radius 12 --k_local 0.055 --k_center 0.03 --seed 3
Outputs
	•	sims/figures/plaza_sync.png — time series of global coherence R
	•	sims/figures/plaza_field.png — final phase pattern (agents colored by phase)

⸻

Parameters to explore
	•	k_local — neighbor coupling (social sensitivity)
	•	k_center — pull to plaza’s center beat (ritual strength)
	•	view — interaction radius (how far agents “hear” neighbors)
	•	radius — size of plaza (geometry effect)

Expect thresholds: below certain coupling values, synchrony won’t hold.

⸻

Cross-map (micro ↔ macro)
	•	Civic: relates to docs/civic/plaza.md (design patterns for coherence).
	•	Human: mirrors Kuramoto synchronization in neural/HRV rhythms.
	•	Earth: plaza acts like an LC cavity, shaping local spectral modes.
	•	Cosmos: log-spiral plazas and calendrical rituals echo cosmic timing.

⸻

Pass / falsifier
	•	Pass: with plausible parameters, R(t) rises above ~0.6 and stays elevated.
	•	Falsifier: no stable increase in R even at high k_local/k_center, or incoherent patterns dominate.

A plaza is a conductor’s instrument: when design (geometry) and ritual (timing) align,
coherence becomes visible — and livable.
