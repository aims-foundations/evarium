"""Ablation main figure — LLM variant.

Single-panel trajectory plot of the score-satisfaction gap across the 5 privacy
conditions, rendered from LLM runs in sandbox/experiments/<batch>/llm/.
Mirrors scripts.plots.paper.ablation_main (heuristic version) but reads the
<condition>_s<seed>_<model>/ folder layout used for LLM batches and uses the
palette-F color scheme consistent with the per_benchmark LLM plots.

Usage:
  python -m scripts.plots.paper.ablation_main_llm
  python -m scripts.plots.paper.ablation_main_llm --batch _core_privacy --model sonnet
"""
import argparse
import json
import os
import re
import warnings
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .. import paths as _paths
from .._ablation_utils import compute_series, plot_trajectory_panel, _last_run

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

CORE_CONDITIONS = [
    "public_only", "baseline", "private_dominant", "private_only", "iid_holdout",
]

CONDITION_LABELS = {
    "public_only":       "Public-only",
    "baseline":          "Baseline (realistic mix)",
    "private_dominant":  "Private-dominant ($\\cos=0.95$)",
    "private_only":      "Private-only ($\\cos=0.85$)",
    "iid_holdout":       "IID holdout (ablation, $\\cos=1.0$)",
}

# Palette F: blue (cool anchor) + YlOrRd warm ramp + gray for iid_holdout.
CONDITION_COLORS = {
    "public_only":       "#2c7fb8",
    "baseline":          "#fec44f",
    "private_dominant":  "#fd8d3c",
    "private_only":      "#b10026",
    "iid_holdout":       "#7f7f7f",
}

CONDITION_LINESTYLES = {
    "public_only":       "-",
    "baseline":          "-",
    "private_dominant":  "-",
    "private_only":      "-",
    "iid_holdout":       "--",
}

_NAME_RE = re.compile(r"^(?P<cond>.+?)_s(?P<seed>\d+)_(?P<model>sonnet|opus)$")


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


def load_llm_runs_by_condition(batch_dir: Path, model_filter: str | None,
                               min_rounds: int = 40) -> dict[str, list[list]]:
    """Walk <batch_dir>/llm/<cond>_s<seed>_<model>/seeds/seed_<N>/rounds.jsonl.

    Groups runs by condition. Skips runs with fewer than min_rounds rounds.
    """
    llm_root = batch_dir / "llm"
    by_cond: dict[str, list[list]] = defaultdict(list)
    for run_dir in sorted(llm_root.iterdir()):
        if not run_dir.is_dir():
            continue
        m = _NAME_RE.match(run_dir.name)
        if not m:
            continue
        cond = m.group("cond")
        seed = int(m.group("seed"))
        model = m.group("model")
        if model_filter and model != model_filter:
            continue
        jsonl = run_dir / "seeds" / f"seed_{seed}" / "rounds.jsonl"
        if not jsonl.exists():
            continue
        with open(jsonl) as f:
            rounds = [json.loads(l) for l in f if l.strip()]
        if len(rounds) < min_rounds:
            print(f"  [skip partial {len(rounds)}/{min_rounds}] {run_dir.name}")
            continue
        by_cond[cond].append(_last_run(rounds))
    return dict(by_cond)


def main(batch_dir: Path, model_filter: str | None, out_path: str, show: bool):
    print(f"Loading LLM runs from: {batch_dir}  (model={model_filter or 'all'})")
    by_cond = load_llm_runs_by_condition(batch_dir, model_filter)
    for cond in CORE_CONDITIONS:
        n = len(by_cond.get(cond, []))
        print(f"  {cond}: {n} seed(s)")

    gap_series = {cond: compute_series(by_cond.get(cond, []), _gap_at_round)
                  for cond in CORE_CONDITIONS}

    fig, ax = plt.subplots(1, 1, figsize=(4.5, 2.6))

    handles = plot_trajectory_panel(
        ax,
        series_dict={c: gap_series.get(c, {}) for c in CORE_CONDITIONS},
        colors=CONDITION_COLORS,
        labels=CONDITION_LABELS,
        linestyles=CONDITION_LINESTYLES,
        ylabel="Score $-$ satisfaction gap",
        title=f"Privacy ablation: gaming dynamics (LLM, {model_filter or 'all'})",
    )

    fig.legend(
        handles=handles, loc="lower center", ncol=3, fontsize=6.5, frameon=False,
        bbox_to_anchor=(0.5, -0.04),
        handlelength=1.6, columnspacing=1.0, handletextpad=0.4,
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
    ap.add_argument("--batch", default="_core_privacy",
                    help="sandbox/experiments/<batch>/ directory holding LLM runs")
    ap.add_argument("--model", default="sonnet", choices=["sonnet", "opus", "all"],
                    help="Filter runs by model suffix (default: sonnet)")
    ap.add_argument("--out", default=os.path.join(_paths.paper_dir(), "ablation_main_llm.pdf"))
    ap.add_argument("--show", action="store_true")
    args = ap.parse_args()
    batch_dir = REPO_ROOT / "sandbox" / "experiments" / args.batch
    model_filter = None if args.model == "all" else args.model
    main(batch_dir, model_filter, args.out, args.show)


if __name__ == "__main__":
    cli()
