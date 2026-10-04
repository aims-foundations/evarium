"""
LLM-vs-heuristic score-satisfaction gap overlay.

3-panel NeurIPS figure: one per condition. Heuristic mean + p10-p90 band (grey)
overlaid with an LLM single-seed trajectory (colored).

Usage:
  python -m scripts.plots.paper.llm_vs_heuristic_gap
"""
import argparse
import json
import os
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .. import paths as _paths

REPO_ROOT = Path(_paths.PROJECT_ROOT)

try:
    from tueplots import bundles as _tb
    _RC = _tb.neurips2024()
    _RC.pop("figure.figsize", None)
    if os.environ.get("MPLLATEX", "1") != "0":
        _RC["text.usetex"] = True
    plt.rcParams.update(_RC)
except ImportError:
    warnings.warn("tueplots not installed -- using default style")

HEURISTIC_BASE = REPO_ROOT / "sandbox/experiments/heuristic"
LLM_BASE = REPO_ROOT / "sandbox/experiments/llm_evaluator/llm"

CONDITIONS = [
    ("full_ecosystem", "seed_125", "Full ecosystem (h=0)"),
    ("expanding_private", "seed_125", "Expanding / private (h=0.50)"),
    ("fixed_private", "seed_127", "Fixed / private (h=0.50)"),
]

PANEL_COLORS = {
    "full_ecosystem":    "#4472C4",
    "expanding_private": "#4472C4",
    "fixed_private":     "#d62728",
}


def _last_run(all_rounds: list) -> list:
    last_zero = 0
    for i, r in enumerate(all_rounds):
        if r.get("round", -1) == 0:
            last_zero = i
    return all_rounds[last_zero:]


def load_heuristic_runs(condition: str):
    cdir = HEURISTIC_BASE / condition / "seeds"
    if not cdir.exists():
        return []
    runs = []
    for seed_dir in sorted(cdir.iterdir()):
        jsonl = seed_dir / "rounds.jsonl"
        if not jsonl.exists():
            continue
        all_rounds = []
        with open(jsonl) as f:
            for line in f:
                line = line.strip()
                if line:
                    all_rounds.append(json.loads(line))
        if all_rounds:
            runs.append(_last_run(all_rounds))
    return runs


def load_llm_run(condition: str, seed: str):
    jsonl = LLM_BASE / condition / "seeds" / seed / "rounds.jsonl"
    if not jsonl.exists():
        return []
    with open(jsonl) as f:
        return [json.loads(l) for l in f if l.strip()]


def gap_at_round(r: dict) -> float:
    scores = r.get("scores", {})
    sat = r.get("consumer_data", {}).get("provider_satisfaction", {})
    ms = r.get("consumer_data", {}).get("market_shares", {})
    providers = [p for p in scores if p in sat and p in ms]
    if not providers:
        return float("nan")
    total = sum(ms[p] for p in providers)
    if total == 0:
        return float("nan")
    return sum(ms[p] / total * (scores[p] - sat[p]) for p in providers)


def heuristic_series(runs):
    if not runs:
        return {}
    max_rounds = max(len(run) for run in runs)
    by_round = {i: [] for i in range(max_rounds)}
    for run in runs:
        for i, r in enumerate(run):
            v = gap_at_round(r)
            if not np.isnan(v):
                by_round[i].append(v)
    result = {}
    for i, vals in by_round.items():
        if vals:
            result[i] = {"mean": float(np.mean(vals)),
                         "p10":  float(np.percentile(vals, 10)),
                         "p90":  float(np.percentile(vals, 90)),
                         "n":    len(vals)}
    return result


def llm_series(rounds_list):
    return {r["round"]: gap_at_round(r) for r in rounds_list if not np.isnan(gap_at_round(r))}


def main(out_path: str, show: bool):
    print("Loading runs...")
    heur = {c: heuristic_series(load_heuristic_runs(c)) for c, _, _ in CONDITIONS}
    llm = {c: llm_series(load_llm_run(c, s)) for c, s, _ in CONDITIONS}
    for c, _, _ in CONDITIONS:
        print(f"  {c}: heuristic rounds={len(heur[c])}, LLM rounds={len(llm[c])}")

    fig, axes = plt.subplots(1, 3, figsize=(6.75, 2.4), sharey=True)
    for i, (cond, seed, label) in enumerate(CONDITIONS):
        ax = axes[i]
        h = heur[cond]; l = llm[cond]
        color = PANEL_COLORS[cond]
        if h:
            xs = sorted(h.keys())
            m = [h[x]["mean"] for x in xs]
            p10 = [h[x]["p10"] for x in xs]
            p90 = [h[x]["p90"] for x in xs]
            ax.fill_between(xs, p10, p90, color="#888888", alpha=0.22, zorder=2, label="heuristic p10--p90")
            ax.plot(xs, m, color="#444444", lw=1.1, zorder=3, label="heuristic mean")
        if l:
            xs_l = sorted(l.keys())
            ys_l = [l[x] for x in xs_l]
            ax.plot(xs_l, ys_l, color=color, lw=1.6, zorder=5, label=f"LLM ({seed})")
        ax.axhline(0, color="#888888", lw=0.5, ls="--", zorder=1)
        ax.set_title(label, fontsize=8, fontweight="bold")
        ax.set_xlabel("Round", fontsize=7)
        if i == 0:
            ax.set_ylabel("Score $-$ satisfaction gap", fontsize=7)
        ax.tick_params(labelsize=6.5)
        ax.grid(axis="y", lw=0.3, alpha=0.35, ls="--")
        if i == 2:
            ax.legend(loc="lower right", fontsize=6, frameon=False)

    fig.tight_layout(pad=0.6)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    png_path = out_path.replace(".pdf", ".png")
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    fig.savefig(png_path, dpi=150, bbox_inches="tight")
    print(f"Saved: {out_path}")
    print(f"Saved: {png_path}")
    if show:
        plt.show()


def cli():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(_paths.paper_dir(), "llm_vs_heuristic_gap.pdf"))
    ap.add_argument("--show", action="store_true")
    args = ap.parse_args()
    main(args.out, args.show)


if __name__ == "__main__":
    cli()
