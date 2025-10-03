# Examples — One-liners

## Human Layer (baseline)
```bash
python -m sims.human_layer_sim --config human/configs/baseline_rest.json
Human Layer (lock-tuned)
python -m sims.human_layer_sim --config human/configs/resonance_lock.json
Human Layer (edge reset)
python -m sims.human_layer_sim --config human/configs/edge_reset.json
City Coupling
python -m sims.city_coupling_demo
Gravity as Partner (concept)
python -m sims.gravity_partner
