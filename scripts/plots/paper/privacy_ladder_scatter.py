"""
Privacy-ladder reliability scatter.

For the 5 privacy conditions (public_only / baseline / private_dominant /
private_only / iid_holdout), plot every (benchmark, seed, round) row of the
market-leader provider (provider with highest final-round market share in that
run) as a point in (benchmark score, matched satisfaction) space. Diagonal =
perfect calibration; below diagonal = benchmark overpromises vs. consumer
experience.

Three outputs:
  s5_privacy_ladder_heuristic.png              single panel, by benchmark privacy type
  s5_privacy_ladder_heuristic_by_provider.png  single panel, by provider (leader across seeds)
  s5_privacy_ladder_heuristic_bm_cond.png      2-panel: (left) by benchmark, (right) by privacy ablation

Market-leader filtering reduces overplotting. Legend reports % of total rows and
% of rows that overpromise (score > matched).

Usage:
  python -m scripts.plots.paper.privacy_ladder_scatter \
      --base-path sandbox/experiments/heuristic_session44/heuristic
"""
from __future__ import annotations

import argparse
import json
import os
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .. import paths as _paths
from ..per_benchmark import per_benchmark_from_rows

try:
    from tueplots import bundles as _tb
    _RC = _tb.neurips2024()
    _RC.pop("figure.figsize", None)
    if os.environ.get("MPLLATEX", "1") != "0":
        _RC["text.usetex"] = True
    plt.rcParams.update(_RC)
except ImportError:
    warnings.warn("tueplots not installed -- using default style")

CORE_CONDITIONS = [
    "public_only",
    "baseline",
    "private_dominant",
    "private_only",
    "iid_holdout",
]

CONDITION_COLORS = {
    # Sequential blue scale: lighter = more public, darker = more private.
    "public_only":      "#c6dbef",  # very light blue
    "baseline":         "#6baed6",  # light-medium blue
    "private_dominant": "#2171b5",  # medium-dark blue
    "private_only":     "#08306b",  # darkest blue
    # iid_holdout sits off the privacy axis (ablation); distinct contrast color.
    "iid_holdout":      "#d94801",  # dark orange
}
CONDITION_LABELS = {
    "public_only":      "public_only",
    "baseline":         "baseline",
    "private_dominant": "private_dominant",
    "private_only":     "private_only",
    "iid_holdout":      "iid_holdout",
}

PRIVACY_COLORS = {
    # 4-level benchmark privacy scale: lighter = more public.
    "public":      "#9ecae1",  # light blue
    "partial":     "#4292c6",  # medium blue
    "private":     "#08519c",  # dark blue
    # iid_holdout is an ablation type (cos=1.0); distinct contrast color.
    "iid_holdout": "#d94801",  # dark orange
}
PRIVACY_ORDER = ["public", "partial", "private", "iid_holdout"]

PROVIDER_COLORS = {
    "Orion Labs":      "#1f77b4",
    "Apex AI":         "#ff7f0e",
    "Genesis Systems": "#2ca02c",
    "Mirage AI":       "#d62728",
    "OpenCore":        "#9467bd",
    "Spark AI":        "#8c564b",
}

BM_ORDER_13 = [
    "General Capability", "Coding Evaluation", "Safety Evaluation", "Instruction Following",
    "Scientific Reasoning", "Clinical Reasoning", "Adversarial Robustness", "Hard Coding",
    "Agentic Tasks", "Advanced Math", "Function Calling", "Long Context", "Legal Reasoning",
]
# 13-color palette: tab20 first 13
_TAB20 = plt.get_cmap("tab20").colors
BM_COLORS = {bm: _TAB20[i % len(_TAB20)] for i, bm in enumerate(BM_ORDER_13)}


def _load_seed(seed_dir: Path):
    rounds = []
    with open(seed_dir / "rounds.jsonl") as f:
        for line in f:
            if line.strip():
                rounds.append(json.loads(line))
    with open(seed_dir / "config.json") as f:
        cfg = json.load(f)
    bm_type = {}
    for bm in list(cfg.get("benchmarks") or []) + list(cfg.get("benchmark_sequence") or []):
        bm_type[bm["name"]] = bm.get("benchmark_type", "public")
    return rounds, bm_type


def _market_leader(rounds):
    """Return provider name with highest final-round market share."""
    last = rounds[-1]
    ms = last.get("consumer_data", {}).get("market_shares", {})
    if not ms:
        return None
    return max(ms, key=ms.get)


def collect_rows(base_path: Path, conditions, stride: int = 1, leader_only: bool = True):
    """Walk base_path/<cond>/seeds/seed_*/ and collect per-round per-benchmark rows.

    If leader_only, keep only rows for the provider with max final-round market share
    in that seed×condition run. This removes provider-level overplotting.
    """
    rows_out = []
    for cond in conditions:
        # Sandbox layout: <base>/<cond>/seeds/seed_*/ ; canonical staging: <base>/<cond>/seed_*/
        seeds_subdir = base_path / cond / "seeds"
        cond_dir = seeds_subdir if seeds_subdir.exists() else base_path / cond
        if not cond_dir.exists():
            print(f"  [missing] {cond}")
            continue
        n_seeds = 0
        for seed_dir in sorted(cond_dir.iterdir()):
            if not seed_dir.is_dir() or not seed_dir.name.startswith("seed_"):
                continue
            if not (seed_dir / "rounds.jsonl").exists():
                continue
            rounds, bm_type = _load_seed(seed_dir)
            leader = _market_leader(rounds) if leader_only else None
            for k in range(0, len(rounds), stride):
                df = per_benchmark_from_rows([rounds[k]])
                if df.empty:
                    continue
                if leader is not None:
                    df = df[df.provider == leader]
                for _, r in df.iterrows():
                    rows_out.append({
                        "score":     float(r["score"]),
                        "matched":   float(r["clean_matched"]),
                        "benchmark": r["benchmark"],
                        "provider":  r["provider"],
                        "bm_type":   bm_type.get(r["benchmark"], "public"),
                        "condition": cond,
                    })
            n_seeds += 1
        print(f"  {cond}: {n_seeds} seeds")
    return rows_out


def _panel(ax, rows, group_key, color_map, group_order, legend_title,
           s=4.0, alpha=0.28):
    groups = {}
    for r in rows:
        groups.setdefault(r[group_key], []).append(r)
    plot_order = [g for g in group_order if g in groups] + [
        g for g in groups if g not in group_order
    ]
    total = len(rows)
    for g in plot_order:
        pts = groups[g]
        xs = np.array([p["score"] for p in pts])
        ys = np.array([p["matched"] for p in pts])
        n = len(pts)
        over = int((xs > ys).sum())
        color = color_map.get(g, "#888888")
        pct_all = 100 * n / total if total else 0
        pct_over = 100 * over / n if n else 0
        label = f"{g} ({pct_all:.1f}\\%, {pct_over:.0f}\\% overpromise)"
        ax.scatter(xs, ys, s=s, c=[color], alpha=alpha, edgecolors="none",
                   rasterized=True, label=label)

    lo = max(0.25, min(min(r["score"] for r in rows), min(r["matched"] for r in rows)) - 0.02)
    hi = min(1.00, max(max(r["score"] for r in rows), max(r["matched"] for r in rows)) + 0.02)
    ax.plot([lo, hi], [lo, hi], color="black", lw=0.7, ls="--",
            label="perfect calibration")
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("Benchmark score")
    ax.set_ylabel("Matched satisfaction")
    ax.tick_params(labelsize=7)
    leg = ax.legend(
        title=legend_title, fontsize=6, title_fontsize=6.5,
        loc="lower right", frameon=True, framealpha=0.92,
        markerscale=3.0, handletextpad=0.3, labelspacing=0.3,
    )
    leg.get_frame().set_linewidth(0.4)


def plot_single_panel(rows, color_mode, out_path: Path, title_suffix: str = ""):
    fig, ax = plt.subplots(1, 1, figsize=(5.0, 4.8))
    if color_mode == "privacy_type":
        _panel(ax, rows, "bm_type", PRIVACY_COLORS, PRIVACY_ORDER, "benchmark privacy")
        legend_title = "benchmark privacy"
    elif color_mode == "provider":
        _panel(ax, rows, "provider", PROVIDER_COLORS, list(PROVIDER_COLORS.keys()), "provider")
        legend_title = "provider"
    elif color_mode == "condition":
        _panel(ax, rows, "condition", CONDITION_COLORS, CORE_CONDITIONS, "privacy ablation")
        legend_title = "privacy ablation"
    elif color_mode == "benchmark":
        _panel(ax, rows, "benchmark", BM_COLORS, BM_ORDER_13, "benchmark")
        legend_title = "benchmark"
    else:
        raise ValueError(color_mode)
    n_total = len(rows)
    sfx = f" -- {title_suffix}" if title_suffix else ""
    ax.set_title(
        f"Reliability by {legend_title} (market leader only)\n"
        f"{n_total:,} leader-rows across 5 privacy conditions{sfx}",
        fontsize=7.5,
    )
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=220, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out_path}")


def plot_two_panel(rows, out_path: Path, title_suffix: str = ""):
    """2x1 figure: left colored by benchmark, right by privacy ablation condition."""
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.7), sharex=True, sharey=True)
    _panel(axes[0], rows, "benchmark", BM_COLORS, BM_ORDER_13, "benchmark",
           s=4.0, alpha=0.32)
    axes[0].set_title("(a) colored by benchmark", fontsize=8.5, loc="left")
    _panel(axes[1], rows, "condition", CONDITION_COLORS, CORE_CONDITIONS,
           "privacy ablation", s=4.0, alpha=0.32)
    axes[1].set_title("(b) colored by privacy ablation", fontsize=8.5, loc="left")
    axes[1].set_ylabel("")

    n_total = len(rows)
    sfx = f" -- {title_suffix}" if title_suffix else ""
    fig.suptitle(
        f"Reliability of market-leader benchmark scores vs. matched consumer satisfaction\n"
        f"{n_total:,} leader-rows pooled across 5 privacy conditions{sfx}",
        fontsize=8.5, y=1.01,
    )
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=220, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out_path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--base-path",
                    default="sandbox/experiments/heuristic_session44/heuristic")
    ap.add_argument("--out-dir", default=_paths.paper_dir())
    ap.add_argument("--stride", type=int, default=1,
                    help="round stride (1 = every round)")
    ap.add_argument("--no-leader-filter", action="store_true",
                    help="plot every provider, not just the market leader")
    ap.add_argument("--suffix", default="",
                    help="optional title suffix")
    args = ap.parse_args()

    base = Path(args.base_path)
    if not base.is_absolute():
        base = Path(_paths.PROJECT_ROOT) / base

    print(f"Loading from {base}")
    rows = collect_rows(base, CORE_CONDITIONS, stride=args.stride,
                        leader_only=not args.no_leader_filter)
    print(f"Collected {len(rows):,} rows")
    if not rows:
        raise SystemExit("No rows collected -- check --base-path")

    out_dir = Path(args.out_dir)
    plot_single_panel(rows, "privacy_type",
                      out_dir / "s5_privacy_ladder_heuristic.png",
                      title_suffix=args.suffix)
    plot_single_panel(rows, "provider",
                      out_dir / "s5_privacy_ladder_heuristic_by_provider.png",
                      title_suffix=args.suffix)
    plot_two_panel(rows,
                   out_dir / "s5_privacy_ladder_heuristic_bm_cond.png",
                   title_suffix=args.suffix)


if __name__ == "__main__":
    main()
