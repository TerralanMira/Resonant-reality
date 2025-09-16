"""
Sunspot Cycle — solar rhythm & Schumann proxy (toy)
Creates a synthetic ~11-year solar cycle and a simple 'Schumann coherence' proxy.

Outputs:
  sims/figures/sunspot_cycle.png
  sims/figures/sunspot_schumann_proxy.png

Run:
  python sims/sunspot_cycle.py
"""
import os, argparse
import numpy as np
import matplotlib.pyplot as plt

def sunspot_series(years=60, dt_days=5.0, period_years=11.0, seed=0):
    rng = np.random.default_rng(seed)
    T = int((years*365)/dt_days)
    t_days = np.arange(T)*dt_days
    t_years = t_days/365.0
    base = 0.5*(1 + np.sin(2*np.pi*t_years/period_years))
    env  = 0.3 + 0.7*np.sin(2*np.pi*t_years/(2*period_years))**2
    noise = 0.12*rng.standard_normal(T)
    s = np.clip(env*base + noise, 0, None)
    return t_years, s

def schumann_coherence_proxy(solar_idx, base=0.7, amp=0.25):
    # Toy idea: higher solar activity → lower Schumann coherence stability
    s_norm = (solar_idx - solar_idx.mean())/(solar_idx.std()+1e-9)
    coh = np.clip(base - amp*(s_norm/3.0), 0.0, 1.0)
    return coh

def save_cycle(t, solar, out="sims/figures/sunspot_cycle.png"):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    plt.figure(figsize=(9,3))
    plt.plot(t, solar)
    plt.xlabel("years"); plt.ylabel("solar index (toy)")
    plt.title("Synthetic sunspot cycle (~11y)")
    plt.tight_layout(); plt.savefig(out, dpi=150)

def save_proxy(t, solar, coh, out="sims/figures/sunspot_schumann_proxy.png"):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    plt.figure(figsize=(9,4))
    plt.plot(t, solar, label="solar index")
    plt.plot(t, coh, label="Schumann coherence (proxy)")
    plt.xlabel("years"); plt.legend()
    plt.title("Solar activity vs Schumann coherence (toy proxy)")
    plt.tight_layout(); plt.savefig(out, dpi=150)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", type=float, default=60)
    ap.add_argument("--dt_days", type=float, default=5.0)
    ap.add_argument("--period_years", type=float, default=11.0)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    t, solar = sunspot_series(args.years, args.dt_days, args.period_years, args.seed)
    coh = schumann_coherence_proxy(solar)
    save_cycle(t, solar)
    save_proxy(t, solar, coh)
    print("Saved sims/figures/sunspot_cycle.png")
    print("Saved sims/figures/sunspot_schumann_proxy.png")

if __name__ == "__main__":
    main()
