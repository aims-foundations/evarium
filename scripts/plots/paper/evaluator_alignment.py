"""
Plot: Leader Capability Alignment with Benchmarks, by Evaluator Condition

1x3 panel layout -- one panel per evaluator condition. Raw seed points + mean.
X: time window (Rounds 0-9, 10-19, 20-29, 30-39).
Y: dot(market_leader_capability, benchmark_dimension_weights[b]).
Color + marker: benchmark family. Hollow: newly introduced in this window.

Usage:
  python -m scripts.plots.paper.evaluator_alignment
"""
import argparse
import json
import os
import warnings
from pathlib import Path

import matplotlib.lines as mlines
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


DIMS = ["reasoning", "coding", "knowledge", "safety", "communication", "agentic"]

CONDITIONS = {
    "Randomized Pool":    REPO_ROOT / "sandbox/experiments/llm/eval_randomized_pool_balanced",
    "Dynamic Evaluator":  REPO_ROOT / "sandbox/experiments/llm/dynamic_evaluator_balanced",
    "Eval as Company":    REPO_ROOT / "sandbox/experiments/llm/eval_as_company_balanced",
}

BENCHMARK_FAMILIES = {
    "Reasoning / Knowledge": [
        "General Capability", "Scientific Reasoning", "Advanced Math",
        "Domain Expert", "Legal Reasoning", "Financial Analysis",
        "Hard Knowledge", "Clinical Reasoning",
    ],
    "Coding / Agentic": [
        "Coding Evaluation", "Hard Coding", "Agentic Tasks",
        "Function Calling", "Web Navigation", "Issue Resolution",
    ],
    "Safety": [
        "Safety Evaluation", "Agentic Safety", "Adversarial Robustness",
    ],
    "Communication": [
        "Instruction Following", "Long Context", "Human Preference",
        "Multilingual Understanding", "Creative Writing",
    ],
}

FAMILY_MARKERS = {
    "Reasoning / Knowledge": "o",
    "Coding / Agentic":      "s",
    "Safety":                "^",
    "Communication":         "D",
}

FAMILY_COLORS = {
    "Reasoning / Knowledge": "#4472C4",
    "Coding / Agentic":      "#ED7D31",
    "Safety":                "#C00000",
    "Communication":         "#70AD47",
}

WINDOWS     = [(0, 9), (10, 19), (20, 29), (30, 39)]
WINDOW_LABELS = ["0-9", "10-19", "20-29", "30-39"]
JITTER_SEED  = 42
JITTER_SCALE = 0.08


def _benchmark_family(name: str) -> str:
    for fam, members in BENCHMARK_FAMILIES.items():
        if name in members:
            return fam
    return "Reasoning / Knowledge"


def _dot(cap_vec: dict, bm_weights: dict) -> float:
    return sum(cap_vec.get(d, 0.0) * bm_weights.get(d, 0.0) for d in DIMS)


def load_runs(condition_dir: Path):
    seeds_dir = condition_dir / "seeds"
    if not seeds_dir.exists():
        return []
    runs = []
    for seed_dir in sorted(seeds_dir.iterdir()):
        if "degraded" in seed_dir.name:
            continue
        jsonl = seed_dir / "rounds.jsonl"
        if not jsonl.exists():
            continue
        rounds = []
        with open(jsonl) as f:
            for line in f:
                line = line.strip()
                if line:
                    rounds.append(json.loads(line))
        if rounds:
            runs.append(rounds)
    return runs


def _get_leader(rounds, idx: int) -> str:
    idx = min(idx, len(rounds) - 1)
    ms = rounds[idx].get("consumer_data", {}).get("market_shares", {})
    return max(ms, key=ms.get) if ms else ""


def _active_benchmarks_at(rounds, idx: int) -> set:
    idx = max(0, min(idx, len(rounds) - 1))
    return set(rounds[idx].get("benchmark_dimension_weights", {}).keys())


def compute_window_data(runs, w_start: int, w_end: int):
    points = []
    for seed_idx, run in enumerate(runs):
        end_idx = min(w_end, len(run) - 1)
        leader = _get_leader(run, end_idx)
        if not leader:
            continue
        cap_vec = run[end_idx].get("capability_vectors", {}).get(leader, {})
        bm_weights_map = run[end_idx].get("benchmark_dimension_weights", {})
        prev_active = _active_benchmarks_at(run, w_start - 1) if w_start > 0 else _active_benchmarks_at(run, 0)
        for bm, weights in bm_weights_map.items():
            is_new = (w_start > 0) and (bm not in prev_active)
            points.append({
                "value": _dot(cap_vec, weights),
                "family": _benchmark_family(bm),
                "is_new": is_new,
                "seed_idx": seed_idx,
                "benchmark": bm,
            })
    return points


def plot_evaluator_alignment(save_path: str = None, show: bool = False):
    rng = np.random.default_rng(JITTER_SEED)
    all_runs = {}
    for cname, cdir in CONDITIONS.items():
        all_runs[cname] = load_runs(cdir)
        print(f"  {cname}: {len(all_runs[cname])} seed(s)")

    cond_names = list(CONDITIONS.keys())
    fig, axes = plt.subplots(1, len(cond_names), figsize=(6.75, 2.8),
                             sharey=True, sharex=False)

    all_vals = []
    panel_data = []
    for w_start, w_end in WINDOWS:
        row = {c: compute_window_data(all_runs[c], w_start, w_end) for c in cond_names}
        panel_data.append(row)
        for pts in row.values():
            all_vals.extend(pt["value"] for pt in pts)

    y_min = max(0.0, min(all_vals) - 0.03) if all_vals else 0.0
    y_max = min(1.0, max(all_vals) + 0.03) if all_vals else 1.0
    x_pos = {label: i for i, label in enumerate(WINDOW_LABELS)}

    for col, cname in enumerate(cond_names):
        ax = axes[col] if len(cond_names) > 1 else axes
        n_seeds = len(all_runs[cname])

        for win_idx, ((w_start, w_end), w_label) in enumerate(zip(WINDOWS, WINDOW_LABELS)):
            pts = panel_data[win_idx][cname]
            x_base = x_pos[w_label]

            by_bm, by_bm_meta = {}, {}
            for pt in pts:
                bm = pt["benchmark"]
                by_bm.setdefault(bm, []).append(pt["value"])
                by_bm_meta[bm] = {"family": pt["family"], "is_new": pt["is_new"]}

            for bm, vals in by_bm.items():
                meta = by_bm_meta[bm]
                color = FAMILY_COLORS[meta["family"]]
                marker = FAMILY_MARKERS[meta["family"]]
                fill = "none" if meta["is_new"] else "full"
                mew = 0.6

                for v in vals:
                    jitter = rng.uniform(-JITTER_SCALE, JITTER_SCALE)
                    ax.plot(x_base + jitter, v, marker=marker, color=color,
                            alpha=0.45, ms=3, fillstyle=fill, markeredgewidth=mew,
                            lw=0, zorder=3)
                if n_seeds > 1:
                    ax.plot(x_base, float(np.mean(vals)), marker=marker, color=color,
                            alpha=0.9, ms=5, fillstyle=fill, markeredgewidth=0.8,
                            lw=0, zorder=5)

        ax.set_title(cname, fontsize=8, fontweight="bold")
        ax.set_xticks(list(x_pos.values()))
        ax.set_xticklabels(WINDOW_LABELS, fontsize=6.5)
        ax.set_xlabel("Rounds", fontsize=7)
        ax.set_xlim(-0.5, len(WINDOWS) - 0.5)
        ax.set_ylim(y_min, y_max)
        ax.grid(axis="y", lw=0.4, alpha=0.35, ls="--")
        ax.tick_params(axis="y", labelsize=7)
        if col == 0:
            ax.set_ylabel("Leader cap $\\cdot$ benchmark weights", fontsize=7)

    family_handles = [
        mlines.Line2D([], [], marker=FAMILY_MARKERS[f], color=FAMILY_COLORS[f],
                      ls="None", ms=5, label=f, markeredgewidth=0.7)
        for f in BENCHMARK_FAMILIES
    ]
    new_handle = mlines.Line2D([], [], marker="o", color="#555555", ls="None", ms=5,
                                fillstyle="none", markeredgewidth=0.7, label="New (hollow)")
    fig.legend(handles=family_handles + [new_handle],
               loc="lower center", ncol=5, fontsize=6.5, frameon=False,
               bbox_to_anchor=(0.5, -0.05),
               handlelength=1.0, columnspacing=0.8)

    fig.tight_layout(rect=[0, 0.10, 1, 1.0])

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Saved: {save_path}")
    if show:
        plt.show()
    return fig


def cli():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(_paths.paper_dir(), "evaluator_alignment.pdf"))
    ap.add_argument("--show", action="store_true")
    args = ap.parse_args()
    print("Loading runs...")
    plot_evaluator_alignment(save_path=args.out, show=args.show)


if __name__ == "__main__":
    cli()
