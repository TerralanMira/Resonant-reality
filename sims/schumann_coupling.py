import numpy as np
import matplotlib.pyplot as plt

# Damped driven oscillator: x'' + 2ζω0 x' + ω0^2 x = A cos(ω_d t)
f0 = 7.83    # Hz
zeta = 0.05  # damping ratio
A = 1.0
dt = 0.001
T = 10.0
t = np.arange(0, T, dt)
w0 = 2*np.pi*f0

def response(fd):
    wd = 2*np.pi*fd
    x, v = 0.0, 0.0
    xs = []
    for ti in t:
        a = A*np.cos(wd*ti) - 2*zeta*w0*v - (w0**2)*x
        v += a*dt
        x += v*dt
        xs.append(x)
    xs = np.array(xs)
    # measure entrainment by correlation between drive and response
    drive = np.cos(wd*t)
    corr = np.corrcoef(xs, drive)[0,1]
    return corr

fds = np.linspace(5.0, 12.0, 60)
corrs = [response(fd) for fd in fds]

plt.figure()
plt.plot(fds, corrs)
plt.xlabel("drive frequency (Hz)")
plt.ylabel("entrainment (corr with drive)")
plt.title("Entrainment window around Schumann 7.83 Hz")
import os
os.makedirs("sims/figures", exist_ok=True)
plt.savefig("sims/figures/schumann_entrainment.png", dpi=150)
print("Saved sims/figures/schumann_entrainment.png")
