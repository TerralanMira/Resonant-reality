import numpy as np
import matplotlib.pyplot as plt

# Simple 1D LC chain with nearest-neighbor coupling
# Each node: L, C; coupling via mutual inductance M (dimensionless alpha)
N = 20
L = 1.0
C = 1.0
alpha = 0.1  # coupling strength

# Linearized small-signal eigenmodes (toy model)
# Effective capacitance matrix (tridiagonal with coupling)
K = np.zeros((N,N))
for i in range(N):
    K[i,i] = 1.0 + (2*alpha if 0 < i < N-1 else alpha)
    if i+1 < N:
        K[i,i+1] = -alpha
        K[i+1,i] = -alpha

# Eigenvalues correspond to omega^2 ~ K/(L*C)
evals, evecs = np.linalg.eigh(K)
omega2 = evals/(L*C)
omega = np.sqrt(np.maximum(omega2, 0))

plt.figure()
plt.plot(range(N), omega, marker="o")
plt.xlabel("mode index")
plt.ylabel("frequency (arb units)")
plt.title("LC chain mode spectrum vs coupling")
import os
os.makedirs("sims/figures", exist_ok=True)
plt.savefig("sims/figures/lc_modes.png", dpi=150)
print("Saved sims/figures/lc_modes.png")
