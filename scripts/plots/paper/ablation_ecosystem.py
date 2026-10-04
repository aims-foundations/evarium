"""
Ablation ecosystem outcomes figure -- 3-panel NeurIPS layout.

All metrics are market-share-weighted to reflect the average user's experience.

Panel A: Market-share-weighted incident exposure per round (rolling mean).
Panel B: Market-share-weighted safety portfolio allocation.
Panel C: Market-share-weighted safety capability dimension.

Works for both heuristic (N>=2 seeds, p10-p90 band) and LLM (N=1) via --base-path.

Usage:
  python -m scripts.plots.paper.ablation_ecosystem
  python -m scripts.plots.paper.ablation_ecosystem --base-path sandbox/experiments/llm_evaluator/llm
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

SPINE_CONDITIONS = ["full_ecosystem", "expanding_private", "fixed_private"]
CONDITION_LABELS = {
    "full_ecosystem":    "Expanding / Public",
    "expanding_private": "Expanding / Private",
    "fixed_private":     "Fixed / Private",
}
SPINE_COLORS = {
    "full_ecosystem":    "#4472C4",
    "expanding_private": "#C00000",
    "fixed_private":     "#ED7D31",
}
SEVERITY_WEIGHTS = {"minor": 1, "moderate": 3, "major": 6, "critical": 12}
ROLLING_WINDOW = 3


def _market_shares(r: dict) -> dict:
    return r.get("consumer_data", {}).get("market_shares", {})


def _weighted_incidents(r: dict) -> float:
    ms = _market_shares(r)
    total_ms = sum(ms.values())
    if total_ms == 0:
        return float("nan")
    incidents = r.get("incidents", [])
    provider_severity = {}
    for inc in incidents:
        p = inc.get("provider", "")
        w = SEVERITY_WEIGHTS.get(inc.get("severity", "minor"), 1)
        provider_severity[p] = provider_severity.get(p, 0) + w
    if not provider_severity:
        return 0.0
    return sum(
        (ms.get(p, 0) / total_ms) * provider_severity.get(p, 0)
        for p in set(list(ms.keys()) + list(provider_severity.keys()))
    )


def _weighted_safety_allocation(r: dict) -> float:
    ms = _market_shares(r)
    strategies = r.get("strategies", {})
    providers = [p for p in ms if p in strategies]
    total_ms = sum(ms[p] for p in providers)
    if total_ms == 0:
        return float("nan")
    return sum(ms[p] / total_ms * strategies[p].get("safety", 0.0) for p in providers)


def _weighted_safety_capability(r: dict) -> float:
    ms = _market_shares(r)
    caps = r.get("capability_vectors", {})
    providers = [p for p in ms if p in caps]
    total_ms = sum(ms[p] for p in providers)
    if total_ms == 0:
        return float("nan")
    return sum(ms[p] / total_ms * caps[p].get("safety", 0.0) for p in providers)


def main(base_path: Path, out_path: str, show: bool):
    is_single_seed = "llm" in str(base_path).lower()
    suffix = " (LLM, N=1)" if is_single_seed else ""

    print(f"Loading runs from: {base_path}")
    all_runs = {c: load_runs(base_path, c) for c in SPINE_CONDITIONS}
    for c, runs in all_runs.items():
        print(f"  {c}: {len(runs)} seed(s)")

    print("Computing series...")
    incident_series  = {c: compute_series(all_runs[c], _weighted_incidents, rolling=ROLLING_WINDOW)
                        for c in SPINE_CONDITIONS}
    safety_alloc     = {c: compute_series(all_runs[c], _weighted_safety_allocation)
                        for c in SPINE_CONDITIONS}
    safety_cap       = {c: compute_series(all_runs[c], _weighted_safety_capability)
                        for c in SPINE_CONDITIONS}

    fig, axes = plt.subplots(1, 3, figsize=(6.75, 2.6), sharey=False)

    plot_trajectory_panel(axes[0], series_dict=incident_series, colors=SPINE_COLORS,
                          labels=CONDITION_LABELS,
                          ylabel="Weighted incident exposure",
                          title=f"(a) Incident exposure ({ROLLING_WINDOW}-round rolling mean){suffix}",
                          show_legend=True)
    plot_trajectory_panel(axes[1], series_dict=safety_alloc, colors=SPINE_COLORS,
                          labels=CONDITION_LABELS,
                          ylabel="Safety allocation (market-share weighted)",
                          title=f"(b) Safety investment{suffix}")
    plot_trajectory_panel(axes[2], series_dict=safety_cap, colors=SPINE_COLORS,
                          labels=CONDITION_LABELS,
                          ylabel="Safety capability (market-share weighted)",
                          title=f"(c) Safety capability{suffix}")

    fig.tight_layout(pad=0.8)

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
    ap.add_argument("--base-path", default="sandbox/experiments/heuristic",
                    help="Root containing condition subdirs with seeds/*/rounds.jsonl")
    ap.add_argument("--out", default=os.path.join(_paths.paper_dir(), "ablation_ecosystem.pdf"))
    ap.add_argument("--show", action="store_true")
    args = ap.parse_args()
    base = Path(args.base_path)
    if not base.is_absolute():
        base = REPO_ROOT / base
    main(base, args.out, args.show)


if __name__ == "__main__":
    cli()
