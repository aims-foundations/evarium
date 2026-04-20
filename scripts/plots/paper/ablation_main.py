"""
Ablation main figure -- session-38 privacy ablation.

Single-panel trajectory plot of the score-satisfaction gap across the 5
privacy conditions (public_only / baseline / private_dominant / private_only /
iid_holdout). Color encodes privacy-strength progression; iid_holdout is
dashed to signal its ablation role (cosine=1.0 isolates Channels 2+3 from
Channel 1 weight distance).

Works for both heuristic (N>=2 seeds, renders p10-p90 band) and LLM (N=1 case
study, renders single trajectory only) via --base-path.

Usage:
  python -m scripts.plots.paper.ablation_main
  python -m scripts.plots.paper.ablation_main --base-path sandbox/experiments/llm_evaluator/llm
  python -m scripts.plots.paper.ablation_main --show
"""
import argparse
import os
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .. import paths as _paths
from .._ablation_utils import load_runs, compute_series, plot_trajectory_panel

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

# Session-38 privacy ablation set. Five conditions along the privacy-strength axis:
# public_only (no privacy)  →  baseline (realistic mix)  →  private_dominant (all mild private)
#                           →  private_only (all adversarial private)
# iid_holdout = ablation isolating the reporting-lag + sample-noise channels from
# the weight-distance channel (holdout weights identical to public).
CORE_CONDITIONS = [
    "public_only",
    "baseline",
    "private_dominant",
    "private_only",
    "iid_holdout",
]

CONDITION_LABELS = {
    "public_only":       "Public-only",
    "baseline":          "Baseline (realistic mix)",
    "private_dominant":  "Private-dominant ($\\cos=0.95$)",
    "private_only":      "Private-only ($\\cos=0.85$)",
    "iid_holdout":       "IID holdout (ablation, $\\cos=1.0$)",
}

CONDITION_COLORS = {
    "public_only":       "#808080",
    "baseline":          "#4472C4",
    "private_dominant":  "#ED7D31",
    "private_only":      "#C00000",
    "iid_holdout":       "#7030A0",
}

CONDITION_LINESTYLES = {
    "public_only":       "-",
    "baseline":          "-",
    "private_dominant":  "-",
    "private_only":      "-",
    "iid_holdout":       "--",
}


def _gap_at_round(r: dict) -> float:
    """Market-share-weighted mean score-satisfaction gap for one round."""
    scores = r.get("scores", {})
    sat = r.get("consumer_data", {}).get("provider_satisfaction", {})
    ms = r.get("consumer_data", {}).get("market_shares", {})
    providers = [p for p in scores if p in sat and p in ms]
    if not providers:
        return float("nan")
    total_ms = sum(ms[p] for p in providers)
    if total_ms == 0:
        return float("nan")
    return sum(ms[p] / total_ms * (scores[p] - sat[p]) for p in providers)


def main(base_path: Path, out_path: str, show: bool):
    is_single_seed = "llm" in str(base_path).lower()
    suffix = " (LLM, N=1)" if is_single_seed else ""

    print(f"Loading runs from: {base_path}")
    all_runs = {}
    for cond in CORE_CONDITIONS:
        all_runs[cond] = load_runs(base_path, cond)
        print(f"  {cond}: {len(all_runs[cond])} seed(s)")

    print("Computing gap series...")
    gap_series = {cond: compute_series(all_runs[cond], _gap_at_round) for cond in all_runs}

    fig, ax = plt.subplots(1, 1, figsize=(4.5, 2.6))

    handles = plot_trajectory_panel(
        ax,
        series_dict={c: gap_series.get(c, {}) for c in CORE_CONDITIONS},
        colors=CONDITION_COLORS,
        labels=CONDITION_LABELS,
        linestyles=CONDITION_LINESTYLES,
        ylabel="Score $-$ satisfaction gap",
        title=f"Privacy ablation: gaming dynamics{suffix}",
    )

    fig.legend(
        handles=handles,
        loc="lower center",
        ncol=3,
        fontsize=6.5,
        frameon=False,
        bbox_to_anchor=(0.5, -0.04),
        handlelength=1.6,
        columnspacing=1.0,
        handletextpad=0.4,
    )

    fig.tight_layout(rect=[0, 0.16, 1, 1], pad=0.8)

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
    ap.add_argument("--base-path", default="sandbox/experiments/session38_heuristic/heuristic",
                    help="Root containing condition subdirs with seeds/*/rounds.jsonl")
    ap.add_argument("--out", default=os.path.join(_paths.paper_dir(), "ablation_main.pdf"))
    ap.add_argument("--show", action="store_true")
    args = ap.parse_args()
    base = Path(args.base_path)
    if not base.is_absolute():
        base = REPO_ROOT / base
    main(base, args.out, args.show)


if __name__ == "__main__":
    cli()
