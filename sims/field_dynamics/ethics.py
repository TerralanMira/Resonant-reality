# ethics.py
# Ethical gate (E-gate): consent, non-coercion, sovereignty weighting.

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any, Callable
import functools

@dataclass
class EGParams:
    consent: bool = True
    non_coercion: bool = True
    sovereignty: float = 1.0  # 0..1 emphasis on user control (>=0.9 preferred)

def egate_allows(params: EGParams) -> bool:
    if not params.consent:
        return False
    if not params.non_coercion:
        return False
    if params.sovereignty < 0.9:
        return False
    return True

def require_egate(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to enforce E-gate checks when sending/acting."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        eg = kwargs.get("eg_params") or kwargs.get("ethics") or EGParams()
        if isinstance(eg, dict):
            eg = EGParams(**eg)
        if not egate_allows(eg):
            raise PermissionError("E-gate blocked this action (consent/non-coercion/sovereignty).")
        return fn(*args, **kwargs)
    return wrapper
