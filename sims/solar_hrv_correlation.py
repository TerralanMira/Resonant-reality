---

```python
"""
Solar ↔ HRV Correlation Toy

Generates a synthetic solar activity index and a synthetic HRV/coherence series,
computes cross-correlation, and plots both time series + correlation.

Run:
    python sims/solar_hrv_correlation.py
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate

def synthetic_solar(T=2000, seed=1):
    rng = np.random.default_rng(seed)
    t = np.arange(T)
    # slow cycle + faster modulation + noise
    slow = 0.5 * np.sin(2*np.pi*t/400.0)
    mid = 0.2 * np.sin(2*np.pi*t/60.0)
    noise = 0.12 * rng.standard_normal(T)
    return (slow + mid + noise + 1.0)  # positive index

def synthetic_hrv(solar, seed=2):
    rng = np.random.default_rng(seed)
    T = len(solar)
    t = np.arange(T)
    # HRV slightly anticorrelated with solar slow peaks in this toy
    base = 0.6 + 0.15 * np.sin(2*np.pi*t/300.0)
    influence = -0.12 * (solar - np.mean(solar))
    noise = 0.08 * rng.standard_normal(T)
    return np.clip(base + influence + noise, 0.0, None)

def plot_time_series(solar, hrv, out_dir="sims/figures"):
    os.makedirs(out_dir, exist_ok=True)
    t = np.arange(len(solar))
    plt.figure(figsize=(10,4))
    plt.plot(t, solar, label="Solar index (synthetic)")
    plt.plot(t, hrv, label="HRV coherence (synthetic)", alpha=0.9)
    plt.legend()
    plt.xlabel("time")
    plt.ylabel("index")
    plt.title("Synthetic Solar Index vs HRV Coherence")
    out = os.path.join(out_dir, "solar_hrv_timeseries.png")
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    print("Saved", out)

def plot_xcorr(solar, hrv, out_dir="sims/figures"):
    os.makedirs(out_dir, exist_ok=True)
    solar_z = (solar - np.mean(solar)) / np.std(solar)
    hrv_z = (hrv - np.mean(hrv)) / np.std(hrv)
    corr = correlate(hrv_z, solar_z, mode='full')
    lags = np.arange(-len(solar_z)+1, len(solar_z))
    mid = len(corr)//2
    plt.figure(figsize=(8,3))
    plt.plot(lags, corr / np.max(np.abs(corr)))
    plt.axvline(0, color='k', linestyle='--')
    plt.xlabel("lag")
    plt.ylabel("normalized cross-correlation")
    plt.title("Cross-correlation (HRV vs Solar)")
    out = os.path.join(out_dir, "solar_hrv_xcorr.png")
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    print("Saved", out)

def main():
    solar = synthetic_solar()
    hrv = synthetic_hrv(solar)
    plot_time_series(solar, hrv)
    plot_xcorr(solar, hrv)

if __name__ == "__main__":
    main()
    Note: this script uses scipy.signal.correlate. If scipy isn’t in sims/requirements.txt, add scipy or change to numpy cross-correlation.
