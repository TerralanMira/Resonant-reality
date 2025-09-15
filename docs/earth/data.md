# Earth Grid Data

This file anchors the resonance models into **real geophysical sites**.  
It connects myth ↔ math by treating sacred / ancient nodes as measurable oscillators.

---

## Structure
Earth data is stored in **JSON** (`earth/sites.json`) with schema validated by `tools/schema-check.py`.

Each site has:
- `name` — site name
- `lat`, `lon` — coordinates
- `hz_band` — dominant resonance band(s) [Hz]
- `notes` — mythic / historic resonance

---

## Example site (JSON)
```json
{
  "name": "Giza Pyramids",
  "lat": 29.9792,
  "lon": 31.1342,
  "hz_band": [7.83, 14.1],
  "notes": "Aligned with Orion; within Schumann band."
}
How to validate
python tools/schema-check.py earth/sites.json
Output:
	•	✅ “valid” if schema matches.
	•	❌ error if missing fields or incorrect types.

⸻

Current map

Sites are progressively added. Early entries:
	•	Giza Pyramids (Egypt)
	•	Chichén Itzá (Mexico)
	•	Stonehenge (UK)
	•	Uluru (Australia)
Next step

Overlay sites with:
	•	Schumann coupling sims
	•	LC grid geometries
	•	Harmonic resonance distances (from CSV)

This creates the Resonant Earth Map → input layer for Cosmic model.
