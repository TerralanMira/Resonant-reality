import math

def resonance_gravity(mass, freq, coherence):
    """Treats gravity not as force but as coupling partner with resonance."""
    g = 9.81  # baseline
    modifier = 1 + (coherence * math.sin(freq))
    return mass * g * modifier

if __name__ == "__main__":
    print(resonance_gravity(70, 7.83, 0.6))
