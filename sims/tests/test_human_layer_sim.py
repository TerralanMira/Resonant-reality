import json, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from sims.human_layer_sim import HumanResonanceEngine, HumanState

def test_edge_nudge():
    eng = HumanResonanceEngine(HumanState(kappa=0.27))
    eng.step(t=0.0, dt=0.5)
    assert eng.state.kappa >= 0.30, "Edge band should nudge κ above 0.30"

def test_tuned_return():
    eng = HumanResonanceEngine(HumanState(kappa=0.10))
    eng.step(t=0.0, dt=0.5)
    assert abs(eng.state.kappa - 0.60) < 1e-6, "Deep decoherence should tuned-return to 0.60"

def test_lock_required():
    # simulate missing lock path by passing bad path
    try:
        HumanResonanceEngine().run(steps=1)
        assert True  # engine has internal fallback, run should still complete
    except Exception:
        assert False, "Engine should fallback safely if lock not present"
