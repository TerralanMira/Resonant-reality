"""
Solar → Schumann Coupling (toy)
Models how an 11-year solar cycle could modulate the Schumann window (~7.83 Hz).
Outputs:
  sims/figures/solar_schumann_series.png
  sims/figures/solar_schumann_spectrum.png

Run:
  python sims/solar_schumann.py
"""
import os, argparse
import numpy as np
import matplotlib.pyplot as plt

def solar_index(T=4000, dt=1.0, period=11*365, noise=0.2, seed=0):
    rng = np.random.default_rng(seed)
    t = np.arange(T) * dt
    base = 0.5 * (1 + np.sin(2*np.pi*t/period))
    return np.clip(base + rng.normal(0, noise, T)*0.05, 0, 1), t

def schumann_center(solar, f0=7.83, depth=0.12):
    # Center frequency shifts slightly with solar activity
    # scale ~ ±depth Hz around f0
    return f0 + depth*(solar - solar.mean())

def schumann_coherence(solar, base=0.7, amp=0.2):
    # Hypothesis: higher solar activity → less stable Schumann window
    return np.clip(base - amp*(solar - solar.mean()), 0.0, 1.0)

def spectrum_signal(f_center, coh, fs=1.0):
    # Build a toy amplitude-modulated sinusoid at the shifting center freq
    t = np.arange(len(f_center))/fs
    phase = 2*np.pi*np.cumsum(f_center)/fs
    sig = np.sin(phase) * (0.5 + 0.5*coh)
    return sig, t

def save_series(t, solar, f_c, coh, out="sims/figures/solar_schumann_series.png"):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    plt.figure(figsize=(10,6))
    ax1 = plt.subplot(3,1,1)
    ax1.plot(t, solar); ax1.set_ylabel("solar idx"); ax1.set_title("Solar Index (toy)")
    ax2 = plt.subplot(3,1,2)
    ax2.plot(t, f_c); ax2.set_ylabel("f_center (Hz)"); ax2.set_title("Schumann center shift")
    ax3 = plt.subplot(3,1,3)
    ax3.plot(t, coh); ax3.set_ylabel("coherence"); ax3.set_xlabel("time (days)")
    ax3.set_title("Schumann coherence (toy)")
    plt.tight_layout(); plt.savefig(out, dpi=150)

def save_spectrum(sig, fs=1.0, out="sims/figures/solar_schumann_spectrum.png"):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    # simple magnitude spectrum
    S = np.abs(np.fft.rfft(sig))
    f = np.fft.rfftfreq(len(sig), d=1/fs)
    plt.figure(figsize=(7,4))
    plt.plot(f, S)
    plt.xlim(0, 20)  # focus near Schumann band
    plt.xlabel("Hz"); plt.ylabel("|FFT|")
    plt.title("Toy spectrum around Schumann band")
    plt.tight_layout(); plt.savefig(out, dpi=150)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--T", type=int, default=4000)
    ap.add_argument("--dt", type=float, default=1.0)  # days
    ap.add_argument("--period", type=float, default=11*365)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    solar, t = solar_index(T=args.T, dt=args.dt, period=args.period, seed=args.seed)
    f_c = schumann_center(solar)
    coh = schumann_coherence(solar)
    sig, _ = spectrum_signal(f_c, coh, fs=1.0/args.dt)

    save_series(t, solar, f_c, coh)
    save_spectrum(sig, fs=1.0/args.dt)
    print("Saved sims/figures/solar_schumann_series.png")
    print("Saved sims/figures/solar_schumann_spectrum.png")

if __name__ == "__main__":
    main()
