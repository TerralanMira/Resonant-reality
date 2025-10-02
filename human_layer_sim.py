# sims/human_layer_sim.py
"""
Human Layer Simulation — Embodied Resonance Engine
--------------------------------------------------
Models the body as a resonant transceiver that houses consciousness:
- Inputs: field carriers (e.g., 7.83, 432, 528, 639, 741, 852, 963 Hz)
- State: kappa (κ: coherence), gamma (γ: binding), chi (χ: fascia/water charge),
         lambda_load (λ: stress), hrv_lf_hf (HRV ratio)
- Mechanisms:
  * Stochastic resonance (micro-noise) near learning edges
  * Decoherence-as-renewal: tuned return when κ dips below stability
  * Prosody proxy (cadence/pause) and a simple coherence grade
- Lock integration: reads /conductor/pulses/resonance_lock.json for gates/limits

CLI:
    python -m sims.human_layer_sim --config human/configs/resonance_lock.json
(or pass another JSON with keys: carriers_hz, schumann_hz, am_depth, noise_pct)

Outputs: prints final state + simple metrics. Intended as a reference engine.
"""
from __future__ import annotations
import os, json, math, random, argparse
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

# ---------- Defaults ----------
DEFAULT_STIM = {
    "carriers_hz": [528.0, 639.0, 852.0, 963.0],
    "schumann_hz": 7.83,
    "am_depth": 0.35,      # amplitude modulation depth [0..1]
    "noise_pct": 0.05      # stochastic resonance strength [0..0.2]
}

LOCK_PATH = os.path.join("conductor", "pulses", "resonance_lock.json")

# ---------- Data Structures ----------
@dataclass
class EEG:
    delta: float = 0.2
    theta: float = 0.3
    alpha: float = 0.4
    beta:  float = 0.35
    gamma: float = 0.30

@dataclass
class HumanState:
    kappa: float = 0.42        # coherence [0..1]
    gamma: float = 0.35        # binding [0..1]
    chi: float   = 0.20        # fascia/water charge [0..1]
    lambda_load: float = 0.60  # stress/load [0..∞)
    hrv_lf_hf: float = 1.20    # HRV ratio
    eeg: EEG = EEG()
    cadence_var: float = 0.35  # prosody proxy
    pause_entropy: float = 0.40

# ---------- Utilities ----------
def safe_clip(x: float, lo: float, hi: float) -> float:
    return lo if x < lo else hi if x > hi else x

def coherence_grade(kappa: float, gamma: float) -> str:
    if kappa >= 0.80 and gamma >= 0.45: return "resonant"
    if kappa >= 0.65: return "stable"
    if kappa >= 0.50: return "recovering"
    return "fragmenting"

def prosody_stability(cadence_variance: float, pause_entropy: float) -> float:
    # lower variance/entropy → steadier expression [0..1]
    score = 1.0 - (0.6*cadence_variance + 0.4*pause_entropy)
    return safe_clip(score, 0.0, 1.0)

def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_lock(path: str = LOCK_PATH) -> Dict[str, Any]:
    if os.path.exists(path):
        return load_json(path)
    # minimal fallback if lock is missing
    return {
        "gates": {"E": True, "consent": True, "sovereignty": True, "Pi_u": 0.72, "GL_min": 0.33},
        "limits": {"sigma_cap_early": 0.25, "sigma_cap_peak": 0.85,
                   "ignition_cap": 1.0, "temperature_bounds": [0.1, 1.0]},
        "pacing": {"Tr_base_ms": 500, "Tr_resonant_ms": 432, "Tr_harmonic_ms": 528}
    }

# ---------- Core Engine ----------
class HumanResonanceEngine:
    def __init__(self,
                 state: Optional[HumanState] = None,
                 stim: Optional[Dict[str, Any]] = None,
                 lock: Optional[Dict[str, Any]] = None):
        self.state = state or HumanState()
        self.stim = stim or DEFAULT_STIM
        self.lock = lock or load_lock()
        # Edge thresholds (learning band) and tuned return
        self.edge_low, self.edge_high = 0.25, 0.30
        self.tuned_return = 0.60  # κ after deep decoherence
        self.noise_cap = float(self.stim.get("noise_pct", 0.05))

    def _carrier_drive(self, t: float) -> float:
        carriers: List[float] = self.stim.get("carriers_hz", [])
        if not carriers: return 0.0
        # average of sinusoids → envelope
        s = sum(math.sin(2*math.pi*f*t) for f in carriers) / len(carriers)
        return self.stim.get("am_depth", 0.3) * s

    def _schumann_drive(self, t: float) -> float:
        return math.sin(2*math.pi*self.stim.get("schumann_hz", 7.83)*t)

    def step(self, t: float, dt: float = 0.5) -> HumanState:
        st = self.state
        # Drives
        alpha_drive = self._carrier_drive(t + dt)
        schumann    = self._schumann_drive(t + dt)
        # micro-noise (stochastic resonance)
        eta = random.gauss(0, self.noise_cap)

        # κ update (coherence): carriers + schumann – load penalty + noise
        st.kappa = safe_clip(
            st.kappa + 0.05*alpha_drive + 0.07*schumann + eta - 0.02*st.lambda_load,
            0.0, 1.0
        )
        # γ binding rises with alignment, mild decay baseline
        st.gamma = safe_clip(
            st.gamma + 0.06*(abs(alpha_drive) + abs(schumann))/2 - 0.01,
            0.0, 1.0
        )
        # χ (fascia/water) integrates coherence/binding slowly
        st.chi = safe_clip(0.985*st.chi + 0.015*max(st.kappa, st.gamma), 0.0, 1.0)

        # HRV proxy and load decay
        st.hrv_lf_hf = safe_clip(1.2 + 0.4*(st.kappa - 0.5), 0.6, 1.8)
        st.lambda_load = max(0.0, st.lambda_load - 0.03*st.kappa)

        # Decoherence-as-renewal
        if self.edge_low <= st.kappa < self.edge_high:
            # learning band: inject small constructive noise to escape minima
            st.kappa = safe_clip(st.kappa + 0.05, 0.0, 1.0)
        elif st.kappa < self.edge_low:
            # tuned return: restore to a coherent basin, not to max
            st.kappa = self.tuned_return

        # Prosody proxies (stabilize as κ rises)
        st.cadence_var   = safe_clip(0.50 - 0.25*st.kappa, 0.05, 0.50)
        st.pause_entropy = safe_clip(0.55 - 0.30*st.kappa, 0.05, 0.55)

        self.state = st
        return st

    def run(self, steps: int = 240, dt: float = 0.5) -> Dict[str, Any]:
        t = 0.0
        for _ in range(steps):
            self.step(t, dt)
            t += dt
        st = self.state
        return {
            "final_state": {
                "kappa": round(st.kappa, 3),
                "gamma": round(st.gamma, 3),
                "chi": round(st.chi, 3),
                "lambda_load": round(st.lambda_load, 3),
                "hrv_lf_hf": round(st.hrv_lf_hf, 3),
                "prosody_stability": round(prosody_stability(st.cadence_var, st.pause_entropy), 3),
                "grade": coherence_grade(st.kappa, st.gamma)
            }
        }

# ---------- CLI ----------
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run Human Layer Resonance Simulation")
    p.add_argument("--config", type=str, default="", help="Path to human-layer stimulus JSON")
    p.add_argument("--lock",   type=str, default=LOCK_PATH, help="Path to resonance_lock.json")
    p.add_argument("--steps",  type=int, default=240, help="Simulation steps")
    p.add_argument("--dt",     type=float, default=0.5, help="Time step")
    return p.parse_args()

def main():
    args = parse_args()
    stim = DEFAULT_STIM
    if args.config and os.path.exists(args.config):
        stim = load_json(args.config)
    lock = load_lock(args.lock) if args.lock else load_lock()
    engine = HumanResonanceEngine(HumanState(), stim, lock)
    out = engine.run(steps=args.steps, dt=args.dt)
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
Run:
python -m sims.human_layer_sim --config human/configs/resonance_lock.json
