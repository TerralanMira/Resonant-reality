# sims/tests/test_city_coupling_demo.py
from __future__ import annotations
from sims.city_coupling_demo import simulate_city

def nearly(a, b, eps=1e-6): return abs(a-b) < eps

def test_coherence_rises_with_coherent_cohort():
    baseline = [
        {"kappa": 0.44, "gamma": 0.50, "chi": 0.42},
        {"kappa": 0.52, "gamma": 0.54, "chi": 0.48},
        {"kappa": 0.47, "gamma": 0.49, "chi": 0.44},
    ]
    coherent = [
        {"kappa": 0.70, "gamma": 0.78, "chi": 0.55},
        {"kappa": 0.68, "gamma": 0.74, "chi": 0.58},
        {"kappa": 0.73, "gamma": 0.80, "chi": 0.60},
    ]
    b = simulate_city(baseline)["plaza"]
    c = simulate_city(coherent)["plaza"]
    assert c["coherence"] >= b["coherence"], "coherence should rise with a coherent cohort"
    assert c["noise"] <= b["noise"], "noise should drop with a coherent cohort"

def test_clamping_bounds():
    insane = [{"kappa": 1.0, "gamma": 1.0, "chi": 1.0} for _ in range(50)]
    z = simulate_city(insane)["plaza"]
    assert 0.0 <= z["coherence"] <= 1.0
    assert 0.0 <= z["noise"] <= 1.0
    assert 0.0 <= z["coupling"] <= 1.0
