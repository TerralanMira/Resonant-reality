```python
import os, numpy as np, matplotlib.pyplot as plt

# Discrete Laplacian eigenmodes on a grid as a proxy for LC mode shapes
def grid_laplacian(n, m):
    N = n*m
    L = np.zeros((N, N))
    def idx(i,j): return i*m + j
    for i in range(n):
        for j in range(m):
            k = idx(i,j)
            L[k,k] = 0
            for di,dj in [(1,0),(-1,0),(0,1),(0,-1)]:
                ii, jj = i+di, j+dj
                if 0 <= ii < n and 0 <= jj < m:
                    kk = idx(ii,jj)
                    L[k,k] += 1
                    L[k,kk] -= 1
    return L

def main(n=12, m=18, modes=6):
    L = grid_laplacian(n,m)
    vals, vecs = np.linalg.eigh(L)
    order = np.argsort(vals)
    vals, vecs = vals[order], vecs[:,order]

    os.makedirs("sims/figures", exist_ok=True)
    plt.figure(figsize=(10,6))
    for k in range(1, modes+1):
        mode = vecs[:,k].reshape(n,m)
        plt.subplot(2, (modes+1)//2, k)
        plt.imshow(mode, aspect='auto')
        plt.title(f"mode {k} (λ={vals[k]:.2f})"); plt.axis('off')
    plt.tight_layout()
    out = "sims/figures/civic_grid_modes.png"
    plt.savefig(out, dpi=150); print(f"Saved {out}")

if __name__ == "__main__":
    main()
