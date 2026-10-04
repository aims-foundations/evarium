"""Export the numbers behind paper Figure 4 (and its 13-benchmark appendix
variant) as one JSON file for the website, so the web figure is drawn from the
same aggregates as the PDF instead of from a screenshot of it.

Runs the exact pipeline of ``privacy_gap_main.py`` / ``privacy_gap_full.py``
(same loaders, same aggregation, same exclusion convention) and writes:

    website/client/data/figures/privacy_gap.json

Contents:
    conditions        ordered privacy conditions, with the paper's legend labels
                      and colors
    dims              capability dimensions with the paper's colors
    panel_a           per (mode, benchmark, condition): mean, ci, n
                      plus the two row orderings (5 representative / all 13)
                      and delta_g per benchmark from the LLM aggregates
    panel_b           per (mode, benchmark): primary_dim, surplus, dgap,
                      and regression stats for the 11-benchmark (paper §5)
                      and 13-benchmark (appendix) sets
    n                 public_only seed counts per mode
    labels            axis labels and panel titles as printed in the paper

Usage:
    python -m scripts.plots.paper.privacy_gap_export
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from pathlib import Path

import numpy as np
from scipy.stats import t as student_t

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.plots import paths as _paths
from scripts.plots.per_benchmark import BM_ORDER, DIMS
from scripts.plots.per_benchmark_core_privacy import build_long_df, _agg_per_condition
from scripts.plots.paper.privacy_gap_main import (
    PRIV_ORDER, PRIV_LABELS, PRIV_COLORS, DIM_COLORS, REP_BENCHMARKS, EXCLUDE_BM,
    benchmark_primary_dims, build_long_df_heuristic, discover_heuristic_runs,
    _build_panel_b_points, _bm_ordering_for_panel_a, _delta_gap,
)


def _regression(pts) -> dict:
    """Same statistics the paper's panel (b) prints: OLS line, Pearson r,
    two-sided p from the t statistic."""
    if len(pts) < 2:
        return {}
    x, y = pts.surplus.to_numpy(float), pts.dgap.to_numpy(float)
    slope, intercept = np.polyfit(x, y, 1)
    r = float(np.corrcoef(x, y)[0, 1])
    n = len(pts)
    t_stat = r * np.sqrt(max(n - 2, 1) / max(1 - r * r, 1e-12))
    p = float(2 * (1 - student_t.cdf(abs(t_stat), df=max(n - 2, 1))))
    return {"slope": float(slope), "intercept": float(intercept), "r": r, "p": p, "n": n}


def _agg_rows(agg, mode):
    return [{"mode": mode, "benchmark": r.benchmark, "condition": r.condition,
             "mean": float(r["mean"]), "ci": float(r["ci"]), "n": int(r["n"])}
            for _, r in agg.iterrows()]


def _pts_rows(pts, mode):
    return [{"mode": mode, "benchmark": r.benchmark, "primary_dim": r.primary_dim,
             "surplus": float(r.surplus), "dgap": float(r.dgap)}
            for _, r in pts.iterrows()]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", default=None,
                    help="Output JSON path (default: website/client/data/figures/privacy_gap.json)")
    args = ap.parse_args()
    out = args.out or os.path.join(_paths.PROJECT_ROOT, "website", "client", "data",
                                   "figures", "privacy_gap.json")

    print("Loading LLM Sonnet 4.6 ...")
    df_llm = build_long_df("_core_privacy", "sonnet")
    df_llm = df_llm[df_llm.condition.isin(PRIV_ORDER)]
    print("Loading heuristic ...")
    df_heur = build_long_df_heuristic(restrict_conds=PRIV_ORDER)
    if df_llm.empty or df_heur.empty:
        sys.exit("No runs discovered.")

    agg_llm = _agg_per_condition(df_llm)
    g_run = df_heur.groupby(["condition", "seed", "benchmark"])["clean_gap"].mean().reset_index()
    agg_heur = g_run.groupby(["benchmark", "condition"])["clean_gap"].agg(
        mean="mean", sd="std", n="count").reset_index()
    agg_heur["ci"] = np.where(agg_heur["n"] > 1,
                               1.96 * agg_heur["sd"] / np.sqrt(agg_heur["n"]), 0.0)

    sample_pub_dirs = sorted(glob.glob(os.path.join(
        _paths.PROJECT_ROOT, "hf_data_staging", "core_privacy",
        "llm", "claude-sonnet-4-6", "public_only", "seed_*")))
    pub_llm = [os.path.join(d, "rounds.jsonl") for d in sample_pub_dirs
               if os.path.exists(os.path.join(d, "rounds.jsonl"))]
    pub_heur = [j for cond, _s, j in discover_heuristic_runs() if cond == "public_only"]
    primary = benchmark_primary_dims(pub_llm[0])

    llm_pts = _build_panel_b_points(df_llm, pub_llm, primary, exclude_bm=[])
    heur_pts = _build_panel_b_points(df_heur, pub_heur, primary, exclude_bm=[])
    keep11 = lambda pts: pts[~pts.benchmark.isin(EXCLUDE_BM)]

    order_rep = _bm_ordering_for_panel_a(agg_llm, REP_BENCHMARKS)
    order_full = _bm_ordering_for_panel_a(agg_llm, list(BM_ORDER))

    data = {
        "source": "scripts/plots/paper/privacy_gap_export.py (same pipeline as privacy_gap_main.py)",
        "conditions": [{"id": c, "label": PRIV_LABELS[c], "color": PRIV_COLORS[c]} for c in PRIV_ORDER],
        "dims": [{"id": d, "color": DIM_COLORS[d]} for d in DIMS],
        "modes": {"llm": "LLM Sonnet", "heur": "Heuristic"},
        "n": {"llm_public_seeds": int(df_llm[df_llm.condition == "public_only"]["seed"].nunique()),
              "heur_public_seeds": int(df_heur[df_heur.condition == "public_only"]["seed"].nunique())},
        "excluded_benchmarks": list(EXCLUDE_BM),
        "panel_a": {
            "order_rep": order_rep,
            "order_full": order_full,
            "delta_g_llm": _delta_gap(agg_llm),
            "rows": _agg_rows(agg_llm, "llm") + _agg_rows(agg_heur, "heur"),
        },
        "panel_b": {
            "primary_dim": {bm: primary.get(bm) for bm in order_full},
            "points": _pts_rows(llm_pts, "llm") + _pts_rows(heur_pts, "heur"),
            "regression": {
                "bm11": {"llm": _regression(keep11(llm_pts)), "heur": _regression(keep11(heur_pts))},
                "bm13": {"llm": _regression(llm_pts), "heur": _regression(heur_pts)},
            },
        },
        "labels": {
            "panel_a_title_rep": "(a) Per-benchmark gap across privacy ladder",
            "panel_a_title_full": "(a) Per-benchmark gap across privacy ladder (all 13 benchmarks)",
            "panel_a_x": "Gap (g) = score − matched satisfaction",
            "panel_b_title": "(b) Gap shift tracks capability surplus on dominant dimension",
            "panel_b_x": "Capability surplus on benchmark's primary dimension",
            "panel_b_y": "Δgap shift under privacy (gap @ private_only − gap @ public_only)",
        },
    }
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=1)
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")

    print("\nrep order:", order_rep)
    print("delta_g (LLM):", {k: round(v, 3) for k, v in data["panel_a"]["delta_g_llm"].items()})
    for key in ("bm11", "bm13"):
        for m in ("llm", "heur"):
            s = data["panel_b"]["regression"][key][m]
            print(f"{key} {m}: r={s['r']:.3f} p={s['p']:.2g} n={s['n']}")
    print("N public seeds:", data["n"])


if __name__ == "__main__":
    main()
