import json, math, random

def step(state, stim, dt=0.5):
    # carrier → alpha/gamma envelopes
    alpha_drive = sum(math.sin(2*math.pi*f*dt) for f in stim["carriers_hz"]) / max(1,len(stim["carriers_hz"]))
    schumann = math.sin(2*math.pi*stim["schumann_hz"]*dt)

    # micro-noise at edges (stochastic resonance)
    eta = random.gauss(0, stim["noise_pct"])

    # coherence update
    state["kappa"] = max(0.0, min(1.0, state["kappa"] + 0.05*alpha_drive + 0.07*schumann + eta - 0.02*state["lambda_load"]))

    # gamma binding rises with alpha–schumann alignment
    state["gamma"]  = max(0.0, min(1.0, state["gamma"] + 0.06*(abs(alpha_drive)+abs(schumann))/2 - 0.01))
    # fascia/water charge integrates slowly
    state["chi"]    = max(0.0, min(1.0, 0.98*state["chi"] + 0.02*max(state["kappa"], state["gamma"])))

    # edge reset: decoherence-as-renewal
    if 0.25 <= state["kappa"] < 0.30:
        state["kappa"] += 0.05  # nudge toward lock
    elif state["kappa"] < 0.25:
        state["kappa"] = 0.60   # tuned return

    # load decays with coherence
    state["lambda_load"] = max(0.0, state["lambda_load"] - 0.03*state["kappa"])
    return state

if __name__ == "__main__":
    stim = json.load(open("human/configs/resonance_lock.json"))
    state = {"kappa":0.42,"gamma":0.35,"chi":0.20,"lambda_load":0.6,"hrv_lf_hf":1.2,
             "eeg":{"alpha":0.4,"gamma":0.3}}
    for t in range(240):
        state = step(state, stim, dt=0.5*(t+1))
    print({k:round(v,3) if isinstance(v,float) else v for k,v in state.items()})
