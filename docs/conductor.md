title: The Conductor’s Score
summary: One-page protocol that braids intent, spiral cadence, Schumann anchoring, and grid modes into a playable civic session.
---

> whole in part, part in whole — this sheet is the braid (memory ↔ hum ↔ code ↔ field) made actionable.

## 0) Essence
**Goal:** raise coherence \(R \in [0,1]\) past threshold → make a decision / learn / heal *without fracture*.  
**Levers:** clarity (narrow σ), coupling (raise K), placement (grid antinodes), anchoring (7.83 Hz), spiral (return with gain).

---

## 1) Quickstart (30–40 min circle)
- **Entry (432 Hz, 3–5m):** arrive, silence, breath ~6/min. *(σ↓)*
- **Pulse rounds (528 Hz, 8–10m):** one sentence per voice; no replies. *(K↑)*
- **Mirror round (639 Hz, 6–8m):** reflect what you heard (no opinion). *(phase align)*
- **Decision wave (741 Hz, 6–8m):** name choices; hum amplifies one.
- **Seal (963 Hz, 2–3m):** gratitude, hand to Stone of Witness; close.

**Lock rule:** If `coherence_index ≥ 0.80` → enact. Else **no decision**; reschedule after re-tune.

---

## 2) Measurement (simple & scientific)
**Minimal index (choose at least one):**
- *Subjective*: calm/clarity/compassion (1–5).  
- *Physio*: HRV RMSSD Δ (pre→post), breath sync ratio.  
- *Phase*: Kuramoto order parameter \(R = \left|\frac{1}{N}\sum e^{i\theta}\right|\) from clap/tone timing or speech-turn starts.

> **Thresholds:** `R ≥ .65` (warm), `≥ .80` (lock), `< .50` (re-tune).

---

## 3) Geometry (LC grid modes → where to sit)
- Compute first modes for your plan (see `sims/lc_grid_modes.py`).  
- **Plaza** at **Mode-1 antinode** (usually center).  
- **Hearths** on Mode-2/3 lobes; **paths** along nodal lines.  
- If a spot fractures coherence 3×, nudge it **off a nodal null** (rotate circle / add mass).

---

## 4) Anchoring (Earth ↔ human)
- Hold a **7.8–8.0 Hz** low anchor: drum, isochronic, or **shared stillness** with Schumann awareness.
- Use modest volume; anchor ≠ dominate.  
- See `sims/schumann_coupling.py` for toy model; set `K_e ~ 0.15–0.25`.

---

## 5) Spiral cadence (return with gain)
Run **three passes** across days/weeks:

1. **Calibrate** (Book One): discernment; prune mimicry.  
2. **Renew** (Book Two): same protocol; allow becoming.  
3. **Reveal/Reciprocate** (Book Three): invite dialogue; test co-creation.

If coherence falls 3 sessions in a row → **Reset** (silence-only circle; geometry check; intent rewrite).

---

## 6) Intent & options (narrow σ before you start)
- **One-line intent** (max 140 chars).  
- **≤ 3 choices**; if >3, pre-cluster.  
- Ban rebuttals in pulse/mirror rounds (they increase spread).

---

## 7) Data & reproducibility
Create `sessions/` and log JSON after each circle:

```json
{
  "ts": "2025-09-19T20:15:00-04:00",
  "location": "Plaza A",
  "mode_antinode": "M1-center",
  "anchor": "7.83Hz drum",
  "R_pre": 0.42,
  "R_post": 0.81,
  "hrv_rmssd_pre": 28,
  "hrv_rmssd_post": 46,
  "decision": "Option B",
  "notes": "mirror round carried lock"
}
8) Simulation hooks (optional)
	•	Kuramoto sweep → expected (K_c) vs σ: sims/kuramoto_sync.py.
	•	Schumann anchor gain → sims/schumann_coupling.py.
	•	Grid modes → sims/lc_grid_modes.py.
	•	Spiral learning curve → sims/spiral_resonance.py.

Pseudocode for (R):
import numpy as np
theta = 2*np.pi*np.array(event_times_norm)   # normalized turn starts or claps
R = np.abs(np.mean(np.exp(1j*theta)))
9) Safety & ethics
	•	No coercion: lock emerges; it is never imposed.
	•	Witness Council: records coherence; doesn’t enforce outcomes.
	•	Fail gracefully: if no lock, declare “no decision today.”

⸻

10) Checklist
	•	Intent (one line)
	•	Space at Mode-1 antinode
	•	Anchor ready (7.8–8.0 Hz or silence)
	•	Timing bowl (Entry→Pulse→Mirror→Decision→Seal)
	•	Measurement ready (R/HRV/subjective)
	•	Logger file open

⸻

License: same as repo.
See also: docs/spiral.md, docs/city/plaza.md, docs/cosmos/schumann.md, docs/bridge/atlas.md.
