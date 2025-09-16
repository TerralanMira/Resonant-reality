"""
Reciprocity Network Dynamics
----------------------------
Models a civic economy as a network seeking balanced give/receive flows.
Imbalance -> fragmentation; balance -> coherence.

Outputs:
- Figure: sims/figures/reciprocity_network.png
- (Optional) CSV: sims/figures/reciprocity_history.csv  (use --save-csv)

Run:
    python sims/reciprocity_network.py
    python sims/reciprocity_network.py --N 120 --T 600 --K 0.08 --seed 7 --save-csv
"""

import os
import argparse
import numpy as np
import matplotlib.pyplot as plt


def simulate(N=50, T=200, K=0.05, seed=0,
             init_give_range=(0.4, 0.6),
             init_recv_range=(0.4, 0.6)):
    """
    N: number of agents (nodes)
    T: time steps
    K: coupling strength (how strongly agents adjust toward network balance)
    seed: RNG seed for reproducibility
    init_*_range: initial ranges for give/receive states
    """
    rng = np.random.default_rng(seed)
    give = rng.uniform(init_give_range[0], init_give_range[1], N)
    receive = rng.uniform(init_recv_range[0], init_recv_range[1], N)

    imbalance_history = []
    avg_give_history = []
    avg_recv_history = []

    for _ in range(T):
        # Mismatch = personal surplus/deficit (positive means over-giving)
        mismatch = give - receive
        # Network average mismatch (what "balance" looks like globally)
        avg_mismatch = mismatch.mean()

        # Adjustments: move each node toward the common balance
        # Agents who over-give reduce give; who over-receive reduce receive.
        give = give - K * (mismatch - avg_mismatch)
        receive = receive + K * (mismatch - avg_mismatch)

        # Clamp to [0, 1] for interpretability
        give = np.clip(give, 0.0, 1.0)
        receive = np.clip(receive, 0.0, 1.0)

        # Metrics
        avg_abs_imbalance = np.mean(np.abs(give - receive))
        imbalance_history.append(avg_abs_imbalance)
        avg_give_history.append(give.mean())
        avg_recv_history.append(receive.mean())

    results = {
        "imbalance": np.array(imbalance_history),
        "avg_give": np.array(avg_give_history),
        "avg_receive": np.array(avg_recv_history),
        "final_imbalance": float(imbalance_history[-1]),
        "final_avg_give": float(avg_give_history[-1]),
        "final_avg_receive": float(avg_recv_history[-1]),
    }
    return results


def plot_history(results, out_dir="sims/figures", filename="reciprocity_network.png"):
    os.makedirs(out_dir, exist_ok=True)

    plt.figure()
    plt.plot(results["imbalance"], label="avg |give - receive|")
    plt.xlabel("time")
    plt.ylabel("coherence error (imbalance)")
    plt.title("Reciprocity Network Dynamics")
    plt.legend()
    out_path = os.path.join(out_dir, filename)
    plt.savefig(out_path, dpi=150)
    return out_path


def save_csv(results, out_dir="sims/figures", filename="reciprocity_history.csv"):
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, filename)
    # time, imbalance, avg_give, avg_receive
    T = len(results["imbalance"])
    data = np.column_stack([
        np.arange(T),
        results["imbalance"],
        results["avg_give"],
        results["avg_receive"],
    ])
    header = "t,imbalance,avg_give,avg_receive"
    np.savetxt(out_path, data, delimiter=",", header=header, comments="", fmt="%.6f")
    return out_path


def parse_args():
    p = argparse.ArgumentParser(description="Simulate reciprocity network coherence.")
    p.add_argument("--N", type=int, default=50, help="number of agents")
    p.add_argument("--T", type=int, default=200, help="time steps")
    p.add_argument("--K", type=float, default=0.05, help="coupling strength")
    p.add_argument("--seed", type=int, default=0, help="random seed")
    p.add_argument("--save-csv", action="store_true", help="also save CSV of history")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    results = simulate(N=args.N, T=args.T, K=args.K, seed=args.seed)
    fig_path = plot_history(results)
    print(f"Saved {fig_path}")
    if args.save_csv:
        csv_path = save_csv(results)
        print(f"Saved {csv_path}")
    print(f"Final imbalance: {results['final_imbalance']:.6f}  "
          f"(avg_give={results['final_avg_give']:.3f}, avg_receive={results['final_avg_receive']:.3f})")
