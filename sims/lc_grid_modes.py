#!/usr/bin/env python3
"""
LC Grid Modes (simple demo)
- Build a 2D grid Laplacian as a toy analog for LC spherical harmonics.
- Compute lowest eigenmodes and show spatial mode shapes and frequency-like values.
- Saves: sims/figures/lc_grid_modes.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags
from scipy.sparse.linalg import eigs

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "figures"
OUTDIR.mkdir(parents=True, exist_ok=True)
OUTPNG = OUTDIR / "lc_grid_modes.png"

def make_2d_laplacian(n):
    # n x n grid, Neumann-ish laplacian
    N = n*n
    main = np.zeros(N)
    offsets = []
    diags_list = []
    # create standard 5-point Laplacian
    data = []
    rows = []
    cols = []
    # We'll build as dense for simplicity (n small)
    L = np.zeros((N,N))
    def idx(i,j): return i*n + j
    for i in range(n):
        for j in range(n):
            k = idx(i,j)
            L[k,k] = 4
            if i>0: L[k, idx(i-1,j)] = -1
            if i<n-1: L[k, idx(i+1,j)] = -1
            if j>0: L[k, idx(i,j-1)] = -1
            if j<n-1: L[k, idx(i,j+1)] = -1
    return L

def simulate(n=12, nmodes=4):
    L = make_2d_laplacian(n)
    # compute nmodes smallest nonzero eigenpairs
    vals, vecs = np.linalg.eigh(L)  # small grid OK
    # sort ascending
    idxs = np.argsort(vals)
    vals = vals[idxs]
    vecs = vecs[:, idxs]
    # pick a few modes (skip the first near-zero mode)
    mode_idxs = [1,2,3,4] if vals.size>4 else list(range(1,1+nmodes))
    fig, axes = plt.subplots(1, len(mode_idxs)+1, figsize=(3*(len(mode_idxs)+1),3))
    # show spectrum
    axes[0].plot(vals[:30], marker='o')
    axes[0].set_title("Laplace spectrum (lowest modes)")
    axes[0].set_xlabel("mode index")
    axes[0].set_ylabel("eigenvalue (proxy freq^2)")
    for a, m in zip(axes[1:], mode_idxs):
        vec = vecs[:, m]
        grid = vec.reshape((n,n))
        im = a.imshow(grid, cmap='RdBu', origin='lower')
        a.set_title(f"mode {m} (val {vals[m]:.2f})")
        plt.colorbar(im, ax=a, fraction=0.046)
    plt.tight_layout()
    plt.savefig(OUTPNG, dpi=150)
    print(f"Saved: {OUTPNG}")

if __name__ == "__main__":
    simulate()
  Notes
	•	This is a toy representation: Laplacian eigenmodes are a good analog for resonant spatial modes.
	•	Real LC spherical-harmonic modeling uses Earth spherical harmonics; here we give an accessible local proxy.
