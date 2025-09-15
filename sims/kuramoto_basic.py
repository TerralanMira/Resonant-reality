---

## 2) Kuramoto simulation
**Path:** `sims/kuramoto_basic.py`
```python
import numpy as np
import matplotlib.pyplot as plt

# N oscillators with natural frequencies drawn from normal(0,1)
N = 100
np.random.seed(0)
omega = np.random.normal(0.0, 1.0, N)

def simulate(K=1.0, T=20.0, dt=0.01):
    steps = int(T/dt)
    theta = np.random.uniform(0, 2*np.pi, N)
    R_hist = []
    for _ in range(steps):
        # order parameter
        R = np.abs(np.mean(np.exp(1j*theta)))
        R_hist.append(R)
        # Kuramoto update
        coupling = K * np.imag(np.exp(1j*(theta[:,None]-theta[None,:]))).mean(axis=1)
        theta = theta + (omega + coupling) * dt
    return np.array(R_hist)

def run_and_plot(K_values=(0.2, 0.6, 1.2)):
    plt.figure()
    for K in K_values:
        R_hist = simulate(K=K)
        plt.plot(R_hist, label=f"K={K}")
    plt.xlabel("time steps")
    plt.ylabel("coherence R")
    plt.legend()
    import os
    os.makedirs("sims/figures", exist_ok=True)
    plt.savefig("sims/figures/kuramoto_R.png", dpi=150)
    print("Saved sims/figures/kuramoto_R.png")

if __name__ == "__main__":
    run_and_plot()
