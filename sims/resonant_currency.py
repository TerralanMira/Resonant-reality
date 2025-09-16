"""
Resonant Currency — Policy-as-Conductor
---------------------------------------
A minimal macro-micro toy model for a local token whose policy targets
a "coherence index" C_t in [0,1]. The token supply adjusts to keep
real price ~ 1.0 while rewarding contribution under high coherence.

Outputs:
- sims/figures/resonant_currency_price.png
- sims/figures/resonant_currency_supply.png

Run:
    python sims/resonant_currency.py
    python sims/resonant_currency.py --T 600 --agents 400 --alpha 0.08 --beta 0.06 --seed 7
"""

import os
import argparse
import numpy as np
import matplotlib.pyplot as plt


def coherence_series(T=400, seed=0, base=0.6, amp=0.25, noise=0.08, period=120):
    """
    Generate a synthetic 'coherence index' C_t in [0,1].
    Think: group HRV / geomagnetic calm / participation rate.
    """
    rng = np.random.default_rng(seed)
    t = np.arange(T)
    wave = amp * np.sin(2 * np.pi * t / period)
    noise_term = rng.normal(0, noise, T)
    C = np.clip(base + wave + noise_term, 0.0, 1.0)
    return C


def simulate(
    T=400,
    N_agents=300,
    alpha=0.05,     # policy sensitivity: supply expands with coherence
    beta=0.05,      # policy sensitivity: supply contracts with price error
    k_demand=0.6,   # demand responsiveness to coherence
    price_elastic=0.8, # demand sensitivity to price
    seed=0
):
    """
    Coupled dynamics:
      - Coherence C_t drives (a) baseline demand and (b) policy target
      - Supply adjusts via policy rule: dS = alpha*C - beta*(P - 1)
      - Price P determined by demand/supply with elastic response
      - Agents contribute more (earn tokens) when coherence is high

    Intuition:
      - If C high: policy loosens (more issuance for contribution), but if price drifts >1,
        contraction term brings it back.
      - If C low: issuance slows; policy prioritizes stability over growth.
    """
    rng = np.random.default_rng(seed)
    C = coherence_series(T=T, seed=seed)

    # State
    S = np.zeros(T)           # circulating supply
    P = np.zeros(T)           # token price (target ~ 1.0)
    D = np.zeros(T)           # demand (flow)
    contrib = np.zeros(T)     # aggregate contribution/earning rate

    # init
    S[0] = 1000.0
    P[0] = 1.0

    for t in range(1, T):
        # Agents' contribution rises with coherence (plus small noise)
        contrib[t] = np.maximum(0.0, N_agents * (0.2 * C[t] + 0.02 * rng.random()))

        # Baseline nominal demand rises with coherence, but falls with price above 1
        D[t] = np.maximum(
            1e-6,
            k_demand * (1.0 + 0.8 * (C[t] - 0.5)) * (1.0 - price_elastic * (P[t-1] - 1.0))
        )

        # Simple price formation: demand per unit supply (plus small jitter)
        # (Think: if supply is scarce relative to demand, price > 1)
        P[t] = np.maximum(0.05, (D[t] / (S[t-1] / 1000.0)) + 0.02 * rng.normal())

        # Policy rule (controller): adjust supply using coherence & price error
        price_error = (P[t] - 1.0)         # positive if too expensive
        dS_policy = alpha * C[t] * contrib[t] - beta * price_error * 1000.0

        # Mint/burn cannot be negative beyond current supply
        S[t] = max(50.0, S[t-1] + dS_policy)

    out = {
        "C": C, "S": S, "P": P, "D": D, "contrib": contrib,
        "final_price": float(P[-1]), "final_supply": float(S[-1])
    }
    return out


def plot_price(P, C, out_dir="sims/figures", fname="resonant_currency_price.png"):
    os.makedirs(out_dir, exist_ok=True)
    plt.figure()
    plt.plot(P, label="price")
    plt.plot(C, label="coherence (scaled)", alpha=0.8)
    plt.axhline(1.0, linestyle="--", label="target price")
    plt.xlabel("time")
    plt.ylabel("price / index")
    plt.title("Resonant Currency — Price vs Coherence")
    plt.legend()
    path = os.path.join(out_dir, fname)
    plt.savefig(path, dpi=150)
    return path


def plot_supply(S, out_dir="sims/figures", fname="resonant_currency_supply.png"):
    os.makedirs(out_dir, exist_ok=True)
    plt.figure()
    plt.plot(S, label="supply")
    plt.xlabel("time")
    plt.ylabel("tokens")
    plt.title("Resonant Currency — Circulating Supply")
    plt.legend()
    path = os.path.join(out_dir, fname)
    plt.savefig(path, dpi=150)
    return path


def parse_args():
    ap = argparse.ArgumentParser(description="Resonant currency toy model.")
    ap.add_argument("--T", type=int, default=400, help="timesteps")
    ap.add_argument("--agents", type=int, default=300, help="number of agents (contribution scale)")
    ap.add_argument("--alpha", type=float, default=0.05, help="policy sensitivity to coherence")
    ap.add_argument("--beta", type=float, default=0.05, help="policy sensitivity to price error")
    ap.add_argument("--seed", type=int, default=0, help="random seed")
    return ap.parse_args()


if __name__ == "__main__":
    args = parse_args()
    res = simulate(
        T=args.T, N_agents=args.agents,
        alpha=args.alpha, beta=args.beta,
        seed=args.seed
    )
    p1 = plot_price(res["P"], res["C"])
    p2 = plot_supply(res["S"])
    print(f"Saved {p1}")
    print(f"Saved {p2}")
    print(f"Final price: {res['final_price']:.3f} | Final supply: {res['final_supply']:.1f}")
