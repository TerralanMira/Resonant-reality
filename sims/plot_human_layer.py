import json, matplotlib.pyplot as plt
from sims.human_layer_sim import HumanResonanceEngine, HumanState

def run_and_plot(steps=240, dt=0.5):
    eng = HumanResonanceEngine(HumanState())
    k_hist, g_hist, c_hist = [], [], []
    t = 0.0
    for _ in range(steps):
        eng.step(t, dt)
        t += dt
        k_hist.append(eng.state.kappa)
        g_hist.append(eng.state.gamma)
        c_hist.append(eng.state.chi)
    plt.figure(); plt.plot(k_hist); plt.title("κ coherence")
    plt.figure(); plt.plot(g_hist); plt.title("γ binding")
    plt.figure(); plt.plot(c_hist); plt.title("χ fascia/water charge")
    plt.show()

if __name__ == "__main__":
    run_and_plot()
