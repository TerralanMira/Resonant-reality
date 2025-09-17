"""
Plaza Synchrony (toy ABM)
Agents wander inside a circular plaza. Each agent carries a phase theta_i.
They couple (a) to nearby agents and (b) to a soft center source field.
Shows how designed space can amplify coherence.

Outputs:
  sims/figures/plaza_sync.png
  sims/figures/plaza_field.png

Run:
  python sims/plaza.py
  # or tweak:
  python sims/plaza.py --N 250 --T 2000 --radius 12 --k_local 0.055 --k_center 0.03 --seed 3
"""
import os, argparse
import numpy as np
import matplotlib.pyplot as plt

def simulate(
    N=200,               # number of agents
    T=1500,              # timesteps
    dt=1.0,              # step size
    radius=10.0,         # plaza radius
    speed=0.08,          # random walk step
    view=2.0,            # interaction radius
    k_local=0.06,        # local (agent↔agent) coupling
    k_center=0.02,       # source (plaza center) coupling
    center_freq=2*np.pi/40.0,  # "ritual beat" at the heart of the plaza
    seed=0
):
    rng = np.random.default_rng(seed)

    # positions (x,y) in a disk; phases uniformly random
    def sample_in_disk(n, R):
        u = rng.random(n)
        r = R*np.sqrt(u)
        ang = rng.uniform(0, 2*np.pi, n)
        return r*np.cos(ang), r*np.sin(ang)

    x, y = sample_in_disk(N, radius)
    theta = rng.uniform(0, 2*np.pi, N)

    order_hist = []
    field_hist = []

    for t in range(T):
        # --- movement: small random walk, reflect off circular boundary
        x += speed*rng.normal(0, 1, N)
        y += speed*rng.normal(0, 1, N)
        r = np.sqrt(x*x + y*y)
        mask = r > radius
        if np.any(mask):
            # reflect toward interior
            x[mask] *= (radius / (r[mask] + 1e-9))
            y[mask] *= (radius / (r[mask] + 1e-9))

        # --- phases: local Kuramoto-like + center source
        # local coupling via neighbor mean phase (within "view")
        # (naive O(N^2) for clarity; fine for small N)
        dtheta_local = np.zeros(N)
        for i in range(N):
            dx = x - x[i]
            dy = y - y[i]
            d2 = dx*dx + dy*dy
            nbr = (d2 <= view*view) & (d2 > 0)
            if np.any(nbr):
                mean_phasor = np.exp(1j*theta[nbr]).mean()
                mean_phase = np.angle(mean_phasor)
                dtheta_local[i] = k_local*np.sin(mean_phase - theta[i])

        # center source: a slowly rotating reference at origin
        phi_c = (center_freq*t*dt) % (2*np.pi)
        ang_to_center = np.arctan2(-y, -x)  # direction of origin from agent
        # phase of source as if "heard" from center (simple model)
        source_phase = phi_c
        dtheta_center = k_center*np.sin(source_phase - theta)

        # update phases
        theta = (theta + (dtheta_local + dtheta_center)*dt) % (2*np.pi)

        # metrics: global order parameter; center coupling field strength
        R = np.abs(np.exp(1j*theta).mean())
        order_hist.append(R)

        # optional field metric: average |source coupling| experienced
        field_strength = np.mean(np.abs(np.sin(source_phase - theta)))
        field_hist.append(field_strength)

    return {
        "x": x, "y": y, "theta": theta,
        "order": np.array(order_hist),
        "field": np.array(field_hist)
    }

def plot_sync(res, out1="sims/figures/plaza_sync.png", out2="sims/figures/plaza_field.png"):
    os.makedirs(os.path.dirname(out1), exist_ok=True)

    # time series
    plt.figure(figsize=(8,3))
    plt.plot(res["order"])
    plt.ylim(0, 1.05)
    plt.xlabel("time")
    plt.ylabel("coherence R")
    plt.title("Plaza Synchrony — Global Coherence")
    plt.tight_layout(); plt.savefig(out1, dpi=150)

    # static scatter colored by final phase
    plt.figure(figsize=(4.5,4.5))
    plt.scatter(res["x"], res["y"], c=np.angle(np.exp(1j*res["theta"])), s=8)
    plt.gca().add_artist(plt.Circle((0,0), radius=10.0, fill=False))
    plt.axis('equal'); plt.axis('off')
    plt.title("Final phase pattern (hue = phase)")
    plt.tight_layout(); plt.savefig(out2, dpi=150)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, default=200)
    ap.add_argument("--T", type=int, default=1500)
    ap.add_argument("--radius", type=float, default=10.0)
    ap.add_argument("--speed", type=float, default=0.08)
    ap.add_argument("--view", type=float, default=2.0)
    ap.add_argument("--k_local", type=float, default=0.06)
    ap.add_argument("--k_center", type=float, default=0.02)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    res = simulate(
        N=args.N, T=args.T,
        radius=args.radius, speed=args.speed, view=args.view,
        k_local=args.k_local, k_center=args.k_center,
        seed=args.seed
    )
    plot_sync(res)
    print("Saved sims/figures/plaza_sync.png and sims/figures/plaza_field.png")

if __name__ == "__main__":
    main()
