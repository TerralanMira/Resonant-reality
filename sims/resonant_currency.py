"""
Resonant Currency Simulation
----------------------------
Toy agent-based model of wealth flow:
- Agents trade using two different rules.
- Compare hoarding vs reciprocity dynamics.
"""

import numpy as np
import matplotlib.pyplot as plt

N = 100  # agents
T = 200  # timesteps
wealth = np.ones(N)  # everyone starts with 1 unit

def step(agents, mode="hoard"):
    i, j = np.random.choice(len(agents), 2, replace=False)
    if mode == "hoard":
        # winner-takes-all: one agent grabs from the other
        transfer = 0.1 * agents[j]
        agents[i] += transfer
        agents[j] -= transfer
    elif mode == "reciprocity":
        # exchange: both share 10% of their wealth
        share_i = 0.1 * agents[i]
        share_j = 0.1 * agents[j]
        agents[i] = agents[i] - share_i + share_j
        agents[j] = agents[j] - share_j + share_i
    return agents

def simulate(mode="hoard"):
    agents = wealth.copy()
    hist = []
    for _ in range(T):
        agents = step(agents, mode=mode)
        hist.append(np.std(agents))  # inequality measure
    return hist

if __name__ == "__main__":
    hoard_hist = simulate("hoard")
    reciprocity_hist = simulate("reciprocity")

    plt.plot(hoard_hist, label="Hoarding")
    plt.plot(reciprocity_hist, label="Reciprocity")
    plt.xlabel("time")
    plt.ylabel("inequality (std dev)")
    plt.legend()
    plt.title("Resonant Currency Dynamics")
    plt.savefig("sims/figures/resonant_currency.png", dpi=150)
    print("Saved sims/figures/resonant_currency.png")
