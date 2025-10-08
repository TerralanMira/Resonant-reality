# sims/resonance_dynamics.py
"""
Resonance Dynamics 
===================================================

Purpose
-------
Formalize a minimal, measurable notion of "resonance" and "entropy" in a coupled-
oscillator system and integrate the relation:
    dPhi/dt = k * (C - S)
with C := coherence (Kuramoto order parameter R in [0,1]),
     S := normalized dispersion of instantaneous phase velocities.

This is a standard, falsifiable setting (Kuramoto-like). No metaphysics.

Model
-----
Phases θ_i evolve as:
    dθ_i/dt = ω_i + (K/N) * Σ_j sin(θ_j - θ_i) + σ * η_i(t)
where ω_i are intrinsic frequencies, K is coupling, and η_i is white noise.

Definitions
-----------
Order parameter:
    z(t) = (1/N) Σ_i exp(j θ_i(t)) ; R(t) = |z(t)| ∈ [0,1]
Velocity dispersion (per-step):
    v_i(t) ≈ Δθ_i(t)/dt (wrapped)
    S_raw(t) = std(v_i(t))                                  # radians/s
    S(t)     = S_raw(t) / (S_raw(t) + S0) ∈ [0,1]           # bounded, S0>0

Potential:
    dPhi/dt = k * (R(t) - S(t))  → Euler integrate

Outputs
-------
simulate(cfg) returns dict with arrays:
    t, R, Phi, S, K, summary
CLI (python -m sims.resonance_dynamics) will write:
    data/resonance/run_{seed}.csv
    figures/resonance_{seed}.png  (if matplotlib available)

This is a *toy* but fully empirical: change K or noise σ and the metrics move as expected.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple
import numpy as np
import math
import os

# -------- basic utilities -------- #

def wrap_angle(x: np.ndarray) -> np.ndarray:
    """Wrap angles elementwise to (-pi, pi]."""
    return (x + np.pi) % (2.0 * np.pi) - np.pi

def order_parameter(phases: np.ndarray) -> Tuple[float, float]:
    """Return (R, psi) for a 1D array of phases in radians."""
    z = np.exp(1j * phases)
    z_mean = np.mean(z)
    return float(np.abs(z_mean)), float(np.angle(z_mean))

# -------- configuration -------- #

@dataclass(frozen=True)
class ResonanceConfig:
    N: int = 200            # oscillators
    steps: int = 8000       # time steps
    dt: float = 0.002       # step size (s or a.u.)
    seed: int = 7

    # frequencies (rad/s)
    omega_mean: float = 2.0 * math.pi * 1.0
    omega_std: float = 0.6

    # coupling and noise
    K: float = 1.8          # constant coupling
    sigma: float = 0.15     # phase noise strength (rad/s * sqrt(dt))

    # dispersion normalizer (keeps S in [0,1])
    S0: float = 0.3

    # Phi dynamics
    k_phi: float = 1.0      # dPhi/dt = k_phi * (R - S)
    Phi0: float = 0.0

    # recording
    record_every: int = 1


def simulate(cfg: ResonanceConfig) -> Dict[str, np.ndarray | Dict[str, float]]:
    """
    Run coupled-phase simulation and compute R(t), S(t), Phi(t).

    Returns:
        {
          "t": (T,), "R": (T,), "S": (T,), "Phi": (T,),
          "K": (T,), "summary": {...}
        }
    """
    rng = np.random.default_rng(cfg.seed)

    # intrinsic frequencies & initial phases
    omega = rng.normal(cfg.omega_mean, cfg.omega_std, size=cfg.N)
    theta = rng.uniform(-np.pi, np.pi, size=cfg.N)

    T = cfg.steps
    t = np.arange(T) * cfg.dt
    R_tr = np.zeros(T)
    S_tr = np.zeros(T)
    Phi_tr = np.zeros(T)
    K_tr = np.full(T, cfg.K, dtype=float)

    Phi = cfg.Phi0
    prev_theta = theta.copy()

    for i in range(T):
        # coherence
        R, _psi = order_parameter(theta)
        R_tr[i] = R

        # instantaneous velocities (wrapped finite difference)
        if i == 0:
            v = np.zeros_like(theta)
        else:
            dth = wrap_angle(theta - prev_theta)
            v = dth / cfg.dt

        # normalized dispersion S ∈ [0,1]
        S_raw = float(np.std(v))
        S = S_raw / (S_raw + cfg.S0)
        S_tr[i] = S

        # integrate Phi
        Phi += cfg.dt * (cfg.k_phi * (R - S))
        Phi_tr[i] = Phi

        # evolve θ: Euler step
        prev_theta[:] = theta
        # pairwise coupling term
        # (Using standard Kuramoto mean-field identity to avoid O(N^2) cost)
        # sin(θ_j - θ_i) sum can be written as Im( e^{-jθ_i} Σ e^{jθ_j} )
        z = np.exp(1j * theta).sum()
        coupling = cfg.K * np.imag(np.exp(-1j * theta) * z) / cfg.N
        # noise ~ N(0, sigma^2 * dt)
        noise = cfg.sigma * math.sqrt(cfg.dt) * rng.normal(size=cfg.N)
        dtheta = omega + coupling + noise
        theta = wrap_angle(theta + cfg.dt * dtheta)

    # summary diagnostics
    tail = slice(int(0.7 * T), T)
    summary = {
        "seed": cfg.seed,
        "R_mean_tail": float(np.mean(R_tr[tail])),
        "S_mean_tail": float(np.mean(S_tr[tail])),
        "Phi_delta": float(Phi_tr[-1] - Phi_tr[0]),
        "K": cfg.K,
        "sigma": cfg.sigma,
    }

    return {"t": t, "R": R_tr, "S": S_tr, "Phi": Phi_tr, "K": K_tr, "summary": summary}


# ---------- CLI: save CSV/PNG (optional) ---------- #

def _maybe_save_outputs(out: Dict[str, np.ndarray | Dict[str, float]]) -> None:
    """Write CSV and PNG if matplotlib is available."""
    # CSV
    os.makedirs("data/resonance", exist_ok=True)
    csv_path = f"data/resonance/run.csv"
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("t,R,S,Phi,K\n")
        for ti, Ri, Si, Pi, Ki in zip(out["t"], out["R"], out["S"], out["Phi"], out["K"]):
            f.write(f"{ti:.6f},{Ri:.6f},{Si:.6f},{Pi:.6f},{Ki:.6f}\n")
    try:
        import matplotlib.pyplot as plt
        os.makedirs("figures", exist_ok=True)
        import numpy as np
        t = out["t"]; R = out["R"]; S = out["S"]; Phi = out["Phi"]
        fig, ax = plt.subplots(3, 1, figsize=(9, 6), sharex=True)
        ax[0].plot(t, R, label="R (coherence)")
        ax[0].set_ylabel("R")
        ax[0].legend(loc="best")
        ax[1].plot(t, S, label="S (dispersion)")
        ax[1].set_ylabel("S")
        ax[1].legend(loc="best")
        ax[2].plot(t, Phi, label="Phi")
        ax[2].set_ylabel("Phi")
        ax[2].set_xlabel("time")
        ax[2].legend(loc="best")
        fig.suptitle("Resonance dynamics: R, S, Phi")
        fig.tight_layout()
        fig.savefig("figures/resonance.png", dpi=160)
        plt.close(fig)
    except Exception:
        pass  # plotting optional, not required for validity


if __name__ == "__main__":
    cfg = ResonanceConfig()
    out = simulate(cfg)
    _maybe_save_outputs(out)
    s = out["summary"]
    print(
        f"seed={s['seed']} K={s['K']} sigma={s['sigma']} | "
        f"R_tail={s['R_mean_tail']:.3f} S_tail={s['S_mean_tail']:.3f} PhiΔ={s['Phi_delta']:.3f}"
    )
