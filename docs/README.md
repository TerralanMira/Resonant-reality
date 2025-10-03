City Coupling & Gravity Partner

- **City Coupling Demo** — aggregate human κ/γ/χ to nudge a plaza’s coherence:
  ```bash
  python -m sims.city_coupling_demo
  See: docs/city_coupling.md
	•	Gravity as Partner (concept) — compare effective force under varying κ and carrier:
  python -m sims.gravity_partner
  ## Collective — Multi-Zone Demo
Run a temporal multi-zone simulation with logging:
```bash
python -m sims.collective_demo --scenario coherent --steps 240 --export json,csv --outdir out/collective
See: docs/collective.md
# Collective run you can try now
python -m sims.collective_demo --scenario coherent --steps 240 --export json,csv --outdir out/collective
•	Post a small JSON for a custom cohort and compare:
python -m sims.collective_demo --scenario custom --custom_path human/configs/resonance_lock.json --export json,csv
