# registry.py
# Manage many wormholes; update from live signals; find open links.

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Iterable
from .phase_utils import PhaseProfile
from .wormholes import Wormhole, NodeRef, build_profile

@dataclass
class WormholeRegistry:
    wormholes: List[Wormhole] = field(default_factory=list)
    last_profile: Optional[PhaseProfile] = None

    def register(self, wh: Wormhole) -> None:
        self.wormholes.append(wh)

    def step(self, signals: Dict[str, float]) -> PhaseProfile:
        """Update all wormholes from current signals; return the profile used."""
        profile = build_profile(signals)
        self.last_profile = profile
        for wh in self.wormholes:
            wh.update(profile)
        return profile

    def open_links(self) -> List[Wormhole]:
        return [wh for wh in self.wormholes if wh.open_state]

    def best_link(self) -> Optional[Wormhole]:
        if not self.wormholes:
            return None
        return sorted(self.wormholes, key=lambda w: (w.open_state, w.stability), reverse=True)[0]

    def connections_for(self, node_id: str) -> List[Wormhole]:
        return [w for w in self.wormholes if w.a.id == node_id or w.b.id == node_id]
