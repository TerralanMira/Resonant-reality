"""
Galactic Pulse — toy burst field
Generates a slow baseline with occasional pulses (as if from a distant source),
then shows time series and spectrum.

Outputs:
  sims/figures/galactic_pulse.png

Run:
  python sims/galactic_pulse.py
"""
import os, argparse
import numpy as np
import matplotlib.pyplot as plt

def galactic_signal(T=50000, dt=1.0, burst_every=7000, burst_width=400, seed=0):
    rng = np.random.default_rng(seed)
    t = np.arange(T)*dt
    base = 0.05*np.sin(2*np.pi*t/(20000))  # very slow drift
    noise = 0.02*rng.standard_normal(T)
    sig = base + noise
    # add pulses
    for k in range(burst_every, T, burst_every):
        k0 = max(0, k - burst_width//2)
        k1 = min(T, k + burst_width//2)
        bump = np.hanning(k1-k0) * 0.6
        sig[k0:k1] += bump
    return t, sig

def save_plot(t, sig, out="sims/figures/galactic_pulse.png"):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig = plt.figure(figsize=(9,5))
    ax1 = fig.add_subplot(2,1,1)
    ax1.plot(t, sig); ax1.set_xlabel("time"); ax1.set_ylabel("amplitude")
    ax1.set_title("Galactic pulse (toy)")
    # spectrum
    S = np.abs(np.fft.rfft(sig))
    f = np.fft.rfftfreq(len(sig), d=(t[1]-t[0]))
    ax2 = fig.add_subplot(2,1,2)
    ax2.plot(f, S); ax2.set_xlabel("freq"); ax2.set_ylabel("|FFT|")
    fig.tight_layout(); fig.savefig(out, dpi=150)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--T", type=int, default=50000)
    ap.add_argument("--dt", type=float, default=1.0)
    ap.add_argument("--burst_every", type=int, default=7000)
    ap.add_argument("--burst_width", type=int, default=400)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    t, sig = galactic_signal(args.T, args.dt, args.burst_every, args.burst_width, args.seed)
    save_plot(t, sig)
    print("Saved sims/figures/galactic_pulse.png")

if __name__ == "__main__":
    main()
