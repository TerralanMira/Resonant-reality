import json, os

def load_json(path):
    with open(path, "r", encoding="utf-8") as f: return json.load(f)

def check_consent(policy_path="ethics/consent_policy.json"):
    if not os.path.exists(policy_path):
        raise RuntimeError("Consent policy missing at ethics/consent_policy.json")
    pol = load_json(policy_path)["requirements"]
    if not (pol.get("explicit_consent") and pol.get("non_coercion") and pol.get("human_sovereignty")):
        raise PermissionError("Consent/sovereignty gates not satisfied.")
    return True

def load_lock(lock_path="conductor/pulses/resonance_lock.json"):
    if not os.path.exists(lock_path):
        raise FileNotFoundError("Resonance lock not found at conductor/pulses/resonance_lock.json")
    return load_json(lock_path)
