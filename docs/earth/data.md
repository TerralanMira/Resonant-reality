# Earth Data

The Earth layer grounds resonance in place.  
Here we collect **sites, frequencies, and measurements** in a simple, expandable format.

---

## Schema
- `site`: name of the place
- `coords`: [lat, lon]
- `freqs`: known or hypothesized resonance bands (Hz)
- `notes`: contextual information (archaeology, myth, physics, or observed hum)

---

## Example Data

```yaml
sites:
  - site: Giza Plateau
    coords: [29.9792, 31.1342]
    freqs: [7.83, 16, 32]
    notes: "Schumann fundamental plus harmonics; alignment with Orion."
  - site: Stonehenge
    coords: [51.1789, -1.8262]
    freqs: [7.83, 14.3]
    notes: "Acoustic resonance chamber effect; seasonal rituals."
  - site: Uluru
    coords: [-25.3444, 131.0369]
    freqs: [9.0]
    notes: "Dreamtime myth; geomagnetic anomaly."
  - site: Machu Picchu
    coords: [-13.1631, -72.5450]
    freqs: [8.5, 17]
    notes: "High-altitude coupling, Incan cosmology."
  - site: Teotihuacan
    coords: [19.6925, -98.8430]
    freqs: [7.83, 20]
    notes: "Pyramid of the Sun; echo chambers tuned to resonance."
Next Steps
	•	Expand the sites list with new data points.
	•	Visualize maps from these coordinates → link to sims/earth_map.py.
	•	Explore connections between mythic narratives and physical resonance.
