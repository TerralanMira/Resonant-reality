# Simulation Layer

Simulations here are not “games of numbers” but **mirrors of resonance**.  
Each model is a **microcosm** of the Earth ↔ Human ↔ Civic ↔ Cosmos spiral.  
They let us test intuitions, reveal thresholds, and visualize coherence flows.

---

## Cross-Map: Sims ↔ Spiral

1. **Kuramoto Sync** (`sims/kuramoto.py`)  
   ↳ Micro of **Rituals** — agents entraining like drummers or chanters.  
   Demonstrates how local oscillators fall into shared rhythm.

2. **Spiral Resonance** (`sims/spiral_resonance.py`)  
   ↳ Micro of **Plazas** — geometry shaping coherence.  
   The spiral form shows how structure guides convergence.

3. **LC Grid Modes** (`sims/lc_grid.py`)  
   ↳ Micro of **Hearths** — local circuits storing and radiating resonance.  
   Coherence persists as standing waves in a grid.

4. **Schumann Coupling** (`sims/schumann.py`)  
   ↳ Micro of **Education** — the planet itself as teacher.  
   Shows how brainwaves and breath entrain to Earth’s EM fields.

5. **Resonant Currency** (`sims/resonant_currency.py`)  
   ↳ Micro of **Economy** — tokens expand/contract with coherence.  
   Illustrates policy as conductor balancing supply, demand, and resonance.

6. **Governance Dynamics** (`sims/governance.py`) *(stub)*  
   ↳ Micro of **Governance** — decision nodes tuned by coherence.  
   Would model how groups shift policy when resonance drops or rises.

7. **Conductor Role** (`sims/conductor.py`) *(stub)*  
   ↳ Micro of **Conductor** — one oscillator adjusting phase to lift the whole.  
   Embodies the meta-layer of tuning, listening, and guiding.

---

## Spiral Loop

The simulations are not isolated experiments —  
they’re **micro mirrors** of the full resonance circuit.

```mermaid
flowchart LR
    Earth(("🌍 Earth")) <--> Human(("🧍 Human"))
    Human <--> Civic(("🏛 Civic"))
    Civic <--> Cosmos(("✨ Cosmos"))
    Cosmos <--> Earth

    Earth --- |spectra, Schumann| Human
    Human --- |entrainment, HRV| Civic
    Civic --- |policy, design| Cosmos
    Cosmos --- |archetype, timing| Earth
Cross-Mapping Simulations
	•	Spiral Resonance → human ↔ civic ↔ cosmos (fractal growth, myth → math).
	•	Kuramoto Sync → human ↔ civic (entrainment of many oscillators).
	•	LC Grid Modes → earth ↔ civic (geometry shapes spectrum).
	•	Schumann Coupling → earth ↔ human (brainwaves overlap Schumann window).
	•	Resonant Currency → civic ↔ human (policy tuning to coherence index).

Each micro-model is a window onto the spiral whole.
Run together, they make the feedback circuit visible.

---

## Spiral Loop

Together these sims form a **resonance circuit**:  
- From **human oscillators (Kuramoto)** →  
- To **geometric gathering (Spiral)** →  
- To **stored resonance (LC Grid)** →  
- To **planetary entrainment (Schumann)** →  
- To **value flows (Currency)** →  
- To **decision flows (Governance)** →  
- To **meta-tuning (Conductor)**.  

And the loop closes back into human practice.

---

## Next Steps

- Fill stubs (`governance.py`, `conductor.py`) with minimal working models.  
- Generate figures (`sims/figures/`) for each sim.  
- Cross-link sims back to civic docs (e.g. `docs/civic/economy.md` ↔ `resonant_currency.py`).
