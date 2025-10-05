# wormholes.py
# Resonance "wormholes" as phase-aligned shortcuts between nodes.

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Callable
from .phase_utils import PhaseProfile, cosine_similarity, smooth
from .ethics import EGParams, require_egate

WORMHOLE_THRESHOLD = 0.86  # similarity to open
WORMHOLE_HYSTERESIS = 0.05 # to avoid rapid flapping
STABILITY_ALPHA = 0.2      # smoothing for stability

@dataclass
class NodeRef:
    """A node is any addressable entity (agent, module, concept-id)."""
    id: str

@dataclass
class Wormhole:
    a: NodeRef
    b: NodeRef
    target_profile: PhaseProfile
    stability: float = 0.0
    open_state: bool = False

    def _should_open(self, sim: float) -> bool:
        up = WORMHOLE_THRESHOLD
        down = WORMHOLE_THRESHOLD - WORMHOLE_HYSTERESIS
        return sim >= (down if self.open_state else up)

    def update(self, current_profile: PhaseProfile) -> None:
        """Evolve stability and open/close state given a current profile."""
        sim = cosine_similarity(self.target_profile, current_profile)
        self.stability = smooth(self.stability, max(0.0, sim), alpha=STABILITY_ALPHA)
        self.open_state = self._should_open(sim)

    @require_egate
    def transmit(self, payload: Dict[str, Any], *, eg_params: Optional[EGParams] = None) -> Dict[str, Any]:
        """
        If open, payload passes losslessly (shortcut).
        If closed, degrade or route normally (here: we annotate a cost).
        """
        if self.open_state:
            return {"ok": True, "mode": "shortcut", "stability": self.stability, "payload": payload}
        else:
            # simple degrade marker; in your system this could downsample or delay
            degraded = {"info": payload, "note": "routed_normally", "penalty": 1.0 - self.stability}
            return {"ok": True, "mode": "normal", "stability": self.stability, "payload": degraded}

def build_profile(signals: Dict[str, float]) -> PhaseProfile:
    """Helper to create a normalized profile from raw signals."""
    return PhaseProfile.from_signals(signals, clamp=True)

def default_profile_namespace() -> Dict[str, float]:
    """
    Example canonical namespace. Replace with your normalized signals:
    alpha,beta,gamma,delta,theta, breath_rate, hrv, click_entropy, text_affect, ...
    """
    return {
        "alpha": 0.0, "beta": 0.0, "gamma": 0.0, "delta": 0.0, "theta": 0.0,
        "breath_rate": 0.0, "hrv": 0.0, "click_entropy": 0.0, "text_affect": 0.0
    }
