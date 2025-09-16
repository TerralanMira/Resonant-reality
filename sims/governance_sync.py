```python
import os, numpy as np, matplotlib.pyplot as plt

# Simple Kuramoto sweep over coupling K; track mean coherence (R)
def kuramoto(N=60, T=2000, dt=0.01, K=0.6, seed=0):
    rng = np.random.default_rng(seed)
    omega = rng.normal(0.0, 1.0, N)
    theta = rng.uniform(0, 2*np.pi, N)
    Rs = []
    steps = int(T*dt)
    for _ in range(steps):
        R = np.abs(np.mean(np.exp(1j*theta)))
        Rs.append(R)
        coupling = K * np.imag(np.exp(1j*(theta[:,None]-theta[None,:]))).mean(axis=1)
        theta = theta + (omega + coupling) * dt
    return np.array(Rs)

def main():
    os.makedirs("sims/figures", exist_ok=True)
    K_values = [0.2, 0.5, 0.8, 1.2]
    plt.figure()
    for K in K_values:
        R = kuramoto(K=K)
        plt.plot(R, label=f"K={K}")
    plt.xlabel("time steps"); plt.ylabel("coherence R"); plt.legend()
    out = "sims/figures/governance_sync_R.png"
    plt.savefig(out, dpi=150); print(f"Saved {out}")

if __name__ == "__main__":
    main()
  
