# sims/human_layer_sim.py
from __future__ import annotations
import os, json, math, random, argparse
from dataclasses import dataclass

DEFAULT_STIM = {
    "carriers_hz": [528.0, 639.0, 852.0, 963.0],
    "schumann_hz": 7.83,
    "am_depth": 0.35,
    "noise_pct": 0.05
}
LOCK_PATH = os.path.join("conductor", "pulses", "resonance_lock.json")

@dataclass
class EEG:
    delta: float = 0.2; theta: float = 0.3; alpha: float = 0.4; beta: float = 0.35; gamma: float = 0.30
@dataclass
class HumanState:
    kappa: float = 0.42; gamma: float = 0.35; chi: float = 0.20
    lambda_load: float = 0.60; hrv_lf_hf: float = 1.20; eeg: EEG = EEG()
    cadence_var: float = 0.35; pause_entropy: float = 0.40

def _clip(x, lo=0.0, hi=1.0): return lo if x < lo else hi if x > hi else x
def _grade(kappa, gamma):
    if kappa >= 0.80 and gamma >= 0.45: return "resonant"
    if kappa >= 0.65: return "stable"
    if kappa >= 0.50: return "recovering"
    return "fragmenting"
def _prosody(cvar, pent): return _clip(1.0 - (0.6*cvar + 0.4*pent), 0.0, 1.0)

def _load_json(p):
    with open(p, "r", encoding="utf-8") as f: return json.load(f)

def _load_lock(path=LOCK_PATH):
    if os.path.exists(path): return _load_json(path)
    return {"gates":{"E":True,"consent":True,"sovereignty":True,"Pi_u":0.72,"GL_min":0.33},
            "limits":{"sigma_cap_early":0.25,"sigma_cap_peak":0.85,"ignition_cap":1.0,"temperature_bounds":[0.1,1.0]},
            "pacing":{"Tr_base_ms":500,"Tr_resonant_ms":432,"Tr_harmonic_ms":528}}

class HumanResonanceEngine:
    def __init__(self, state: HumanState|None=None, stim: dict|None=None, lock: dict|None=None):
        self.state = state or HumanState()
        self.stim  = stim  or DEFAULT_STIM
        self.lock  = lock  or _load_lock()
        self.edge_low, self.edge_high = 0.25, 0.30
        self.tuned_return = 0.60
        self.noise_cap = float(self.stim.get("noise_pct", 0.05))

    def _carrier_drive(self, t: float) -> float:
        carriers = self.stim.get("carriers_hz", [])
        if not carriers: return 0.0
        s = sum(math.sin(2*math.pi*f*t) for f in carriers) / len(carriers)
        return self.stim.get("am_depth", 0.3) * s

    def _schumann_drive(self, t: float) -> float:
        return math.sin(2*math.pi*self.stim.get("schumann_hz", 7.83)*t)

    def step(self, t: float, dt: float = 0.5) -> HumanState:
        st = self.state
        alpha_drive = self._carrier_drive(t + dt)
        schumann    = self._schumann_drive(t + dt)
        eta = random.gauss(0, self.noise_cap)

        st.kappa = _clip(st.kappa + 0.05*alpha_drive + 0.07*schumann + eta - 0.02*st.lambda_load, 0.0, 1.0)
        st.gamma = _clip(st.gamma + 0.06*(abs(alpha_drive) + abs(schumann))/2 - 0.01, 0.0, 1.0)
        st.chi   = _clip(0.985*st.chi + 0.015*max(st.kappa, st.gamma), 0.0, 1.0)

        st.hrv_lf_hf     = _clip(1.2 + 0.4*(st.kappa - 0.5), 0.6, 1.8)
        st.lambda_load   = max(0.0, st.lambda_load - 0.03*st.kappa)

        if self.edge_low <= st.kappa < self.edge_high: st.kappa = _clip(st.kappa + 0.05, 0.0, 1.0)
        elif st.kappa < self.edge_low:                 st.kappa = self.tuned_return

        st.cadence_var   = _clip(0.50 - 0.25*st.kappa, 0.05, 0.50)
        st.pause_entropy = _clip(0.55 - 0.30*st.kappa, 0.05, 0.55)
        self.state = st
        return st

    def run(self, steps: int = 240, dt: float = 0.5):
        t = 0.0
        for _ in range(steps):
            self.step(t, dt); t += dt
        st = self.state
        return {
            "final_state": {
                "kappa": round(st.kappa, 3),
                "gamma": round(st.gamma, 3),
                "chi": round(st.chi, 3),
                "lambda_load": round(st.lambda_load, 3),
                "hrv_lf_hf": round(st.hrv_lf_hf, 3),
                "prosody_stability": round(_prosody(st.cadence_var, st.pause_entropy), 3),
                "grade": _grade(st.kappa, st.gamma)
            }
        }

def _parse():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=str, default="", help="Path to human stimulus JSON")
    ap.add_argument("--lock",   type=str, default=LOCK_PATH, help="Path to resonance_lock.json")
    ap.add_argument("--steps",  type=int, default=240)
    ap.add_argument("--dt",     type=float, default=0.5)
    return ap.parse_args()

def main():
    args = _parse()
    stim = DEFAULT_STIM
    if args.config and os.path.exists(args.config):
        with open(args.config, "r", encoding="utf-8") as f: stim = json.load(f)
    lock = _load_lock(args.lock) if args.lock else _load_lock()
    eng = HumanResonanceEngine(HumanState(), stim, lock)
    out = eng.run(steps=args.steps, dt=args.dt)
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
