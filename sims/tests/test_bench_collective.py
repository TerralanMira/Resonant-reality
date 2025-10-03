# sims/tests/test_bench_collective.py
from __future__ import annotations
import json, tempfile, os, subprocess, sys

def run_bench(steps=60):
    with tempfile.TemporaryDirectory() as td:
        proc = subprocess.run(
            [sys.executable, "scripts/bench_collective.py", "--steps", str(steps), "--outdir", td, "--seed", "3"],
            capture_output=True, text=True, check=True
        )
        with open(os.path.join(td, "bench_results.json"), "r", encoding="utf-8") as f:
            return json.load(f)["rows"]

def test_rows_exist_and_have_plaza_metrics():
    rows = run_bench(steps=60)
    assert len(rows) > 0
    sample = rows[0]
    # Expect plaza metrics to be present
    keys = [k for k in sample.keys() if k.startswith("plaza_")]
    assert any("coherence_mean" in k for k in keys)
    assert any("noise_mean" in k for k in keys)
  Why this matters
	•	Repeatable proof: same scenarios across locks → comparable, auditable outputs.
	•	CI artifacts: every PR can ship CSV/JSON results; debates defer to data.
	•	Bridging octave: this ties harmonics → public zones → governance choices with visible deltas.
