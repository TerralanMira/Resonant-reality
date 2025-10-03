# sims/plot_collective.py
"""
Reads out/collective/collective_series.csv and renders three line charts:
- coherence per zone
- noise per zone
- coupling per zone

Usage:
  python -m sims.plot_collective --csv out/collective/collective_series.csv --outdir out/collective/plots
"""
from __future__ import annotations
import argparse, os, csv
import matplotlib.pyplot as plt

def ensure_dir(p: str) -> None:
    os.makedirs(p, exist_ok=True)

def read_series(csv_path: str) -> list[dict]:
    rows = []
    with open(csv_path, "r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append(row)
    return rows

def cast_float(rows: list[dict], keys: list[str]) -> None:
    for row in rows:
        for k in keys:
            row[k] = float(row[k])

def lineplot(ax, xs, ys, label: str) -> None:
    ax.plot(xs, ys, label=label)

def make_plot(rows: list[dict], metrics: list[str], title: str, outfile: str) -> None:
    xs = [int(r["step"]) for r in rows]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for m in metrics:
        ys = [r[m] for r in rows]
        lineplot(ax, xs, ys, m)
    ax.set_title(title)
    ax.set_xlabel("step")
    ax.set_ylabel("value (0..1)")
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(outfile)
    plt.close(fig)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", type=str, default="out/collective/collective_series.csv")
    ap.add_argument("--outdir", type=str, default="out/collective/plots")
    args = ap.parse_args()

    ensure_dir(args.outdir)
    rows = read_series(args.csv)

    float_keys = [
        "hearth_coherence","hearth_noise","hearth_coupling",
        "plaza_coherence","plaza_noise","plaza_coupling",
        "wild_coherence","wild_noise","wild_coupling"
    ]
    cast_float(rows, float_keys)

    # Coherence per zone
    make_plot(
        rows,
        ["hearth_coherence","plaza_coherence","wild_coherence"],
        "Coherence per Zone",
        os.path.join(args.outdir, "coherence_per_zone.png"),
    )
    # Noise per zone
    make_plot(
        rows,
        ["hearth_noise","plaza_noise","wild_noise"],
        "Noise per Zone",
        os.path.join(args.outdir, "noise_per_zone.png"),
    )
    # Coupling per zone
    make_plot(
        rows,
        ["hearth_coupling","plaza_coupling","wild_coupling"],
        "Coupling per Zone",
        os.path.join(args.outdir, "coupling_per_zone.png"),
    )
    print(f"Saved plots to {args.outdir}")

if __name__ == "__main__":
    main()
