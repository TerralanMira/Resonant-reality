import numpy as np
from sims.kuramoto_basic import simulate

def test_coherence_increases_with_coupling():
    R_low = simulate(K=0.2)
    R_high = simulate(K=1.2)
    # Compare mean of last 20% of steps
    n = len(R_low)
    tail = slice(int(0.8*n), n)
    assert R_high[tail].mean() > R_low[tail].mean()
