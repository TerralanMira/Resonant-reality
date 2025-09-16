
```python
import os, numpy as np, matplotlib.pyplot as plt

# Two simple order-parameters R1, R2 driven by intrinsic gains and cross-coupling gamma.
def simulate(T=400, gamma=0.5, seed=0):
    rng = np.random.default_rng(seed)
    R1 = 0.2; R2 = 0.3
    h1, h2 = 0.015, 0.012   # intrinsic gains (e.g., practice, education)
    n1, n2 = 0.03, 0.03     # noise scale

    R1_hist, R2_hist = [], []
    for _ in range(T):
        # logistic-like pull toward 1, with cross-coupling
        dR1 = h1*(1-R1)*R1 + gamma*(R2 - R1) + rng.normal(0, n1)
        dR2 = h2*(1-R2)*R2 + gamma*(R1 - R2) + rng.normal(0, n2)
        R1 = np.clip(R1 + dR1, 0, 1)
        R2 = np.clip(R2 + dR2, 0, 1)
        R1_hist.append(R1); R2_hist.append(R2)
    return np.array(R1_hist), np.array(R2_hist)

def sweep():
    gammas = np.linspace(0.0, 1.0, 21)
    finals1, finals2 = [], []
    for g in gammas:
        R1, R2 = simulate(gamma=g)
        finals1.append(R1[-1]); finals2.append(R2[-1])
    return gammas, np.array(finals1), np.array(finals2)

def main():
    os.makedirs("sims/figures", exist_ok=True)
    gammas, f1, f2 = sweep()
    plt.figure()
    plt.plot(gammas, f1, label="R1 final")
    plt.plot(gammas, f2, label="R2 final")
    plt.xlabel("coupling γ"); plt.ylabel("final coherence")
    plt.title("Meta-Resonance: Coherence vs Coupling")
    plt.legend()
    out = "sims/figures/meta_resonance.png"
    plt.savefig(out, dpi=150); print(f"Saved {out}")

if __name__ == "__main__":
    main()
