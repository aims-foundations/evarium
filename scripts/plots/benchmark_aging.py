"""Benchmark-aging / overfitting analysis across a batch of LLM runs.

Tests the hypothesis: benchmarks in the sim the longest should show faster
per-round score growth (overfitting signal), while late-introduced benchmarks
grow slower. Also plots per-benchmark final score vs aggregate satisfaction.

CLI:
    python -m scripts.plots.benchmark_aging --llm-batch llm_apr19_diag --llm-seed 2026

Outputs (under output/analysis/benchmark_aging/):
    bm_aging_trajectories.png   — per-run, per-benchmark score trajectories
    bm_aging_growth_rate.png    — lifetime vs growth/round scatter + trend
    bm_final_vs_sat.png         — per-benchmark final score − avg_sat, per run
"""
from __future__ import annotations

import argparse
import glob
import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import cm

from . import paths as _paths

# Default run suffixes to scan inside the LLM batch. Any condition/structural
# directory under <batch>/llm/ that contains seeds/seed_<N>/rounds.jsonl works.
DEFAULT_RUNS = [
    ("baseline", "baseline (dynamic pool)"),
    ("private_only", "private_only"),
    ("baseline__initial_uniform_allocation", "init_uniform_allocation"),
    ("baseline__no_regulator", "no_regulator"),
    ("baseline__no_incidents", "no_incidents"),
    ("fixed_public", "fixed_public (static pool)"),
]


def _load_run(dir_path: str):
    jsonl = os.path.join(dir_path, "rounds.jsonl")
    with open(jsonl) as f:
        return [json.loads(l) for l in f]


def _per_bm_trajectories(rows):
    bm_traj = {}
    for r in rows:
        pbs = r.get("per_benchmark_scores", {})
        for bm, scores in pbs.items():
            bm_traj.setdefault(bm, []).append((r["round"], float(np.mean(list(scores.values())))))
    return bm_traj


def _resolve_runs(llm_batch: str, seed: int):
    resolved = []
    for subdir, label in DEFAULT_RUNS:
        p = _paths.sandbox_run_dir(llm_batch, "llm", subdir, "seeds", f"seed_{seed}")
        if os.path.exists(os.path.join(p, "rounds.jsonl")):
            resolved.append((subdir, label, p))
    if not resolved:
        raise FileNotFoundError(
            f"No valid LLM runs under {_paths.sandbox_run_dir(llm_batch, 'llm')} "
            f"for seed {seed}"
        )
    return resolved


def plot_trajectories(runs, out_path: str):
    fig, axes = plt.subplots(2, 3, figsize=(16, 9), sharex=True, sharey=True)
    axes = axes.flatten()
    for idx, (_subdir, label, run_dir) in enumerate(runs[:6]):
        ax = axes[idx]
        rows = _load_run(run_dir)
        bm_traj = _per_bm_trajectories(rows)
        births = {bm: pts[0][0] for bm, pts in bm_traj.items()}
        bms_sorted = sorted(bm_traj.keys(), key=lambda b: births[b])
        colors = cm.viridis(np.linspace(0, 1, len(bms_sorted)))
        for bm, color in zip(bms_sorted, colors):
            pts = bm_traj[bm]
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            ax.plot(xs, ys, label=f"{bm} (r{births[bm]})",
                    color=color, lw=1.5, marker="o", markersize=3, alpha=0.85)
        ax.set_title(label)
        ax.set_xlabel("Round")
        ax.set_ylabel("Mean score across providers")
        ax.legend(loc="lower right", fontsize=6, ncol=1)
        ax.grid(True, alpha=0.3)
    for j in range(len(runs), 6):
        axes[j].axis("off")
    fig.suptitle("Per-benchmark score trajectories\n"
                 "color encodes introduction round (viridis: early→late)", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(out_path, dpi=130)
    plt.close(fig)
    print(f"Saved {out_path}")


def plot_growth_vs_age(runs, out_path: str):
    fig, ax = plt.subplots(figsize=(10, 5.5))
    colors = cm.tab10(np.linspace(0, 1, 10))
    all_x, all_y = [], []
    for i, (_sd, label, run_dir) in enumerate(runs):
        rows = _load_run(run_dir)
        bm_traj = _per_bm_trajectories(rows)
        end_round = rows[-1]["round"]
        label_used = False
        for bm, pts in bm_traj.items():
            birth = pts[0][0]
            lifetime = end_round - birth
            if lifetime < 1:
                continue
            growth = pts[-1][1] - pts[0][1]
            rate = growth / lifetime
            ax.scatter(lifetime, rate, s=75, color=colors[i], alpha=0.75,
                       label=label if not label_used else None,
                       edgecolor="black", linewidth=0.4)
            label_used = True
            all_x.append(lifetime); all_y.append(rate)

    xs, ys = np.array(all_x), np.array(all_y)
    if len(xs) >= 2:
        slope, intercept = np.polyfit(xs, ys, 1)
        xx = np.linspace(xs.min(), xs.max(), 20)
        ax.plot(xx, slope * xx + intercept, "r--", lw=2,
                label=f"trend: rate = {slope:+.5f}·lifetime + {intercept:.4f}")
        from scipy.stats import pearsonr
        r, p = pearsonr(xs, ys)
        ax.set_title(f"Benchmark aging: long-lived benchmark → faster growth? "
                     f"(Pearson r={r:+.2f}, p={p:.2g})")
    else:
        ax.set_title("Benchmark aging (insufficient data for trend)")

    ax.set_xlabel("Benchmark lifetime in sim (rounds)")
    ax.set_ylabel("Mean score growth per round")
    ax.legend(loc="best", fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)
    print(f"Saved {out_path}")


def plot_final_vs_sat(runs, out_path: str, bm_order=None):
    if bm_order is None:
        bm_order = ["General Capability", "Coding Evaluation", "Safety Evaluation",
                    "Instruction Following", "Scientific Reasoning", "Agentic Tasks",
                    "Hard Coding", "Long Context", "Domain Expert", "Agentic Safety"]
    fig, ax = plt.subplots(figsize=(14, 5))
    width = 0.8 / max(len(runs), 1)
    for i, (_sd, label, run_dir) in enumerate(runs):
        rows = _load_run(run_dir)
        last = rows[-1]
        avg_sat = last["consumer_data"]["avg_satisfaction"]
        deltas = []
        for bm in bm_order:
            pbs = last.get("per_benchmark_scores", {})
            if bm in pbs:
                deltas.append(float(np.mean(list(pbs[bm].values()))) - avg_sat)
            else:
                deltas.append(np.nan)
        xs = np.arange(len(bm_order))
        ax.bar(xs + i * width - (len(runs) - 1) * width / 2, deltas, width=width,
               label=label, edgecolor="black", linewidth=0.3)
    ax.axhline(0, color="k", lw=0.8, ls="--", alpha=0.5)
    ax.set_xticks(range(len(bm_order)))
    ax.set_xticklabels(bm_order, rotation=25, ha="right", fontsize=8)
    ax.set_ylabel("Final mean score − avg satisfaction")
    ax.set_title("Per-benchmark score vs satisfaction (final round)")
    ax.legend(loc="best", fontsize=8)
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)
    print(f"Saved {out_path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--llm-batch", default="llm_apr19_diag",
                    help="sandbox/experiments/<batch>/llm/ root")
    ap.add_argument("--llm-seed", type=int, default=2026)
    ap.add_argument("--out-subject", default="benchmark_aging")
    args = ap.parse_args()

    out_dir = _paths.analysis_dir(args.out_subject)
    runs = _resolve_runs(args.llm_batch, args.llm_seed)

    plot_trajectories(runs, os.path.join(out_dir, "bm_aging_trajectories.png"))
    plot_growth_vs_age(runs, os.path.join(out_dir, "bm_aging_growth_rate.png"))
    plot_final_vs_sat(runs, os.path.join(out_dir, "bm_final_vs_sat.png"))


if __name__ == "__main__":
    main()
