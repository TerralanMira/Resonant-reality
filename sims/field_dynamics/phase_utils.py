# phase_utils.py
# Utilities for constructing and comparing resonance/phase profiles.

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple
import math

@dataclass(frozen=True)
class PhaseProfile:
    """A normalized multidimensional signal vector with stable key order."""
    keys: Tuple[str, ...]
    values: Tuple[float, ...]

    @staticmethod
    def from_signals(signals: Dict[str, float], clamp: bool = True) -> "PhaseProfile":
        # keep deterministic order
        items = sorted((k, float(v)) for k, v in signals.items())
        vals = []
        keys = []
        for k, v in items:
            if clamp:
                v = max(0.0, min(1.0, v))
            keys.append(k)
            vals.append(v)
        # unit-length normalization (avoid zero vector)
        norm = math.sqrt(sum(x * x for x in vals)) or 1.0
        vals = [x / norm for x in vals]
        return PhaseProfile(tuple(keys), tuple(vals))

def cosine_similarity(a: PhaseProfile, b: PhaseProfile) -> float:
    """Cosine similarity for two profiles sharing the same key set."""
    # align by keys; assume both created from same signal namespace
    if a.keys != b.keys:
        # reconcile union of keys, filling missing as 0
        all_keys = sorted(set(a.keys) | set(b.keys))
        av = [a.values[a.keys.index(k)] if k in a.keys else 0.0 for k in all_keys]
        bv = [b.values[b.keys.index(k)] if k in b.keys else 0.0 for k in all_keys]
    else:
        av = list(a.values)
        bv = list(b.values)
    dot = sum(x * y for x, y in zip(av, bv))
    na = math.sqrt(sum(x * x for x in av)) or 1.0
    nb = math.sqrt(sum(y * y for y in bv)) or 1.0
    return max(-1.0, min(1.0, dot / (na * nb)))

def smooth(prev: float, new: float, alpha: float = 0.2) -> float:
    """Exponential moving average for stability evolution."""
    return (1 - alpha) * prev + alpha * new
