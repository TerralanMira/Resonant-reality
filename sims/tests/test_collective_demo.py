# sims/tests/test_collective_demo.py
"""
Sanity checks for collective demo behavior:
- Coherent scenario should not increase noise relative to baseline in the plaza summary mean.
- Coherent scenario should not reduce coherence relative to baseline in the plaza summary mean.
"""
from __future__ import annotations
import json, tempfile, os, subprocess, sys

def run_cmd(args: list[str]) -> dict:
    proc = subprocess.run([sys.executable, "-m"] + args, capture_output=True, text=True, check=True)
    return json.loads(proc.stdout)

def run_collective(scenario: str) -> dict:
    # Write to temp dir to avoid clobbering user output
    with tempfile.TemporaryDirectory() as td:
        args = ["sims.collective_demo", "--scenario", scenario, "--steps", "180", "--export", "json", "--outdir", td]
        res = run_cmd(args)
        return res["summaries"]["plaza"]

def test_plaza_coherent_vs_baseline():
    b = run_collective("baseline")
    c = run_collective("coherent")
    # Coherent should yield >= mean coherence and <= mean noise vs baseline
    assert c["plaza_coherence"]["mean"] >= b["plaza_coherence"]["mean"] - 1e-9
    assert c["plaza_noise"]["mean"] <= b["plaza_noise"]["mean"] + 1e-9
