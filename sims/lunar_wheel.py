"""
Lunar Wheel — phase calendar (toy)
Draws a simple circular wheel of 29.53-day lunar phases.

Output:
  sims/figures/lunar_wheel.png

Run:
  python sims/lunar_wheel.py
"""
import os
import numpy as np
import matplotlib.pyplot as plt

def draw_wheel(days=29.53, ticks=30, out="sims/figures/lunar_wheel.png"):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    theta = np.linspace(0, 2*np.pi, ticks, endpoint=False)
    r_outer = 1.0
    x = r_outer * np.cos(theta)
    y = r_outer * np.sin(theta)

    plt.figure(figsize=(6,6))
    # circle
    t = np.linspace(0, 2*np.pi, 512)
    plt.plot(np.cos(t), np.sin(t))
    # spokes
    for i, ang in enumerate(theta):
        plt.plot([0, np.cos(ang)], [0, np.sin(ang)], linewidth=0.5)
        if i % 5 == 0:
            label = f"D{i:02d}"
            plt.text(1.08*np.cos(ang), 1.08*np.sin(ang), label, ha="center", va="center", fontsize=8)

    # key markers (approx)
    phases = {
        "New": 0,
        "First Q": int(ticks*0.25),
        "Full": int(ticks*0.5),
        "Last Q": int(ticks*0.75),
    }
    for name, idx in phases.items():
        ang = theta[idx%ticks]
        plt.scatter([np.cos(ang)],[np.sin(ang)], s=60)
        plt.text(1.18*np.cos(ang), 1.18*np.sin(ang), name, ha="center", va="center")

    plt.axis('equal'); plt.axis('off')
    plt.title("Lunar Phase Wheel (toy)")
    plt.tight_layout(); plt.savefig(out, dpi=150)

if __name__ == "__main__":
    draw_wheel()
    print("Saved sims/figures/lunar_wheel.png")
