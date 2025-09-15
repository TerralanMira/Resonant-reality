import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

# Parameters
N = 200            # number of oscillators
steps = 400        # time steps
K = 1.2            # coupling strength
dt = 0.05          # time step

# Initial phases (random)
theta = np.random.uniform(0, 2*np.pi, N)

# Natural frequencies
omega = np.random.normal(0.0, 0.5, N)

# History for animation
history = []

def update():
    global theta
    # Kuramoto-like update
    coupling = K * np.imag(np.exp(1j*(theta[:,None]-theta[None,:]))).mean(axis=1)
    theta += (omega + coupling) * dt
    history.append(np.copy(theta))

# Run simulation
for _ in range(steps):
    update()

# Convert history into x,y for spiral visualization
x_hist, y_hist = [], []
for t_idx, thetas in enumerate(history):
    radius = 1 + t_idx/steps * 3.0   # radius grows outward
    x = radius * np.cos(thetas)
    y = radius * np.sin(thetas)
    x_hist.append(x)
    y_hist.append(y)

# Set up animation
fig, ax = plt.subplots(figsize=(6,6))
ax.set_xlim(-5,5)
ax.set_ylim(-5,5)
ax.set_aspect("equal")
scat = ax.scatter([], [], s=10, c="blue", alpha=0.6)

def animate(i):
    scat.set_offsets(np.c_[x_hist[i], y_hist[i]])
    return scat,

ani = animation.FuncAnimation(fig, animate, frames=len(x_hist), interval=50, blit=True)

# Save output
os.makedirs("sims/figures", exist_ok=True)
ani.save("sims/figures/spiral_resonance.gif", writer="pillow", fps=20)
print("Saved spiral resonance animation → sims/figures/spiral_resonance.gif")
