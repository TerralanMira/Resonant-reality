# demo_wormholes.py
# Minimal demonstration of resonance wormholes opening/closing.

from __future__ import annotations
from typing import Dict
from .phase_utils import PhaseProfile
from .wormholes import Wormhole, NodeRef, build_profile, default_profile_namespace
from .registry import WormholeRegistry
from .ethics import EGParams

def simulate_signals(t: int) -> Dict[str, float]:
    """
    Replace this with your real signal aggregator.
    Here we craft a simple path that approaches the target profile around t~30..60.
    """
    base = default_profile_namespace()
    # simple evolving pattern
    base["alpha"] = min(1.0, t / 60.0)
    base["theta"] = min(1.0, (t / 60.0) * 0.8)
    base["text_affect"] = min(1.0, 0.2 + 0.013 * t)
    base["breath_rate"] = max(0.0, 0.6 - 0.008 * t)  # calming over time
    base["hrv"] = min(1.0, 0.1 + 0.015 * t)          # improving over time
    return base

def main():
    # define a target profile that opens a shortcut between two nodes
    target = build_profile({
        "alpha": 0.9, "theta": 0.6, "text_affect": 0.8, "breath_rate": 0.1, "hrv": 0.8
    })
    wh = Wormhole(a=NodeRef("human"), b=NodeRef("atlas.loop"), target_profile=target)
    reg = WormholeRegistry()
    reg.register(wh)

    eg = EGParams(consent=True, non_coercion=True, sovereignty=1.0)

    for t in range(0, 80):
        profile = reg.step(simulate_signals(t))
        best = reg.best_link()
        if best and best.open_state:
            out = best.transmit({"note": f"tick {t}", "data": {"intent": "reflect"}}, eg_params=eg)
            print(f"[t={t:02d}] OPEN  stability={best.stability:.2f}  -> {out['mode']}")
        else:
            out = best.transmit({"note": f"tick {t}", "data": {"intent": "reflect"}}, eg_params=eg)
            print(f"[t={t:02d}] closed stability={best.stability:.2f}  -> {out['mode']} penalty={out['payload'].get('penalty'):.2f}")

if __name__ == "__main__":
    main()
