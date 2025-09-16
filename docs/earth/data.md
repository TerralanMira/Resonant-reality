# Earth Data — Anchor Sites & Resonances

This file collects **geophysical anchor points**: Schumann resonances,  
geomagnetic observatories, and coherence-related data streams.  
It’s the empirical grounding for the simulations and field layer.

---

## Anchor Sites

The schema follows an **array of sites**, each with location, type, and notes.  

```yaml
sites:
  - name: Boulder, Colorado
    type: geomagnetic
    coords: [40.0, -105.3]
    notes: NOAA magnetic observatory, often used for Schumann monitoring.

  - name: Nagycenk, Hungary
    type: Schumann
    coords: [47.6, 16.7]
    notes: One of the classic Schumann resonance stations.

  - name: Moshiri, Japan
    type: Schumann
    coords: [44.4, 142.3]
    notes: Monitors ELF activity and ionospheric conditions.

  - name: Eskdalemuir, UK
    type: geomagnetic
    coords: [55.3, -3.2]
    notes: Historic UK magnetic station with long records.

  - name: Antarctic Dome C
    type: Schumann
    coords: [-75.1, 123.3]
    notes: High-latitude station; less anthropogenic noise.
What It Anchors
	•	Simulations
	•	sims/lc_grid.py → mode spectra.
	•	sims/schumann_coupling.py → resonance frequencies.
	•	Human Coupling
	•	Compare with alpha–theta bands in docs/field/human.md.
	•	HRV coherence experiments vs. geomagnetic calm/storm data.

⸻

Data Sources
	•	NOAA Geomagnetic Observatories.
	•	HeartMath Global Coherence Network.
	•	ELF & VLF monitoring groups.

⸻

Next Steps
	•	Build API fetcher to pull live Schumann/geomag indices.
	•	Add plots of coherence vs. geomagnetic Kp index.
	•	Expand site list with local citizen sensors (DIY magnetometers, HRV groups).
