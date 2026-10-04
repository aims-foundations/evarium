"""Privacy-gap two-panel figure --- full 13-benchmark appendix variant.

Same construction as ``privacy_gap_main.py`` but renders the appendix figure
covering all 13 benchmarks in the active suite (i.e. the 11-benchmark non-
outlier set plus Agentic Tasks and Function Calling, the two agentic-
calibration outliers normally excluded). Both panels are 13-bm:

(a) Per-benchmark gap forest --- 13 benchmarks in one column, ordered by LLM
    public_only mean descending.
(b) Δg vs capability surplus on each benchmark's primary dimension. Regression
    is fit on all 13 points; the 2 outliers (Function Calling, Agentic Tasks)
    sit at the strongly-negative-surplus / strongly-positive-Δg corner and
    extend the regression's leverage.

Shared plotting helpers are imported from ``privacy_gap_main`` --- this script
only adds the 13-bm data-loading and orchestration. Run independently of the
main figure.

Outputs (PDF + PNG):
    output/paper/privacy_gap_full.pdf  — all 13 benchmarks (Appendix F)

Usage:
    python -m scripts.plots.paper.privacy_gap_full
"""
from __future__ import annotations

import argparse
import glob
import os
import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.plots import paths as _paths
from scripts.plots.per_benchmark import BM_ORDER
from scripts.plots.per_benchmark_core_privacy import build_long_df, _agg_per_condition

# Reuse all helpers + constants from the main-figure script.
from scripts.plots.paper.privacy_gap_main import (
    PRIV_ORDER,
    benchmark_primary_dims, build_long_df_heuristic, discover_heuristic_runs,
    _build_panel_b_points, _bm_ordering_for_panel_a, render,
)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out-dir", default=None,
                    help="Output directory (default: output/paper/)")
    args = ap.parse_args()

    out_dir = args.out_dir or _paths.paper_dir()
    os.makedirs(out_dir, exist_ok=True)

    # ── Load LLM (canonical staging, sonnet only). NO EXCLUDE_BM filter. ──
    print("Loading LLM Sonnet 4.6 (hf_data_staging/core_privacy/llm/claude-sonnet-4-6)...")
    df_llm = build_long_df("_core_privacy", "sonnet")
    df_llm = df_llm[df_llm.condition.isin(PRIV_ORDER)]
    print(f"  rows={len(df_llm)}, seeds={df_llm.seed.nunique()}, "
          f"benchmarks={df_llm.benchmark.nunique()}")

    print("Loading heuristic (hf_data_staging/core_privacy/heuristic)...")
    df_heur = build_long_df_heuristic(restrict_conds=PRIV_ORDER)
    print(f"  rows={len(df_heur)}, seeds={df_heur.seed.nunique()}, "
          f"benchmarks={df_heur.benchmark.nunique()}")

    if df_llm.empty:
        sys.exit("No LLM runs discovered.")
    if df_heur.empty:
        sys.exit("No heuristic runs discovered.")

    # ── Aggregate per (benchmark, condition) for the forest panel ──
    agg_llm = _agg_per_condition(df_llm)
    g_run = df_heur.groupby(["condition", "seed", "benchmark"])["clean_gap"].mean().reset_index()
    agg_heur = g_run.groupby(["benchmark", "condition"])["clean_gap"].agg(
        mean="mean", sd="std", n="count").reset_index()
    agg_heur["ci"] = np.where(agg_heur["n"] > 1,
                               1.96 * agg_heur["sd"] / np.sqrt(agg_heur["n"]),
                               0.0)

    # ── Primary dimensions + capability surplus (no exclusion) ──
    print("Resolving primary dimensions + population capability surplus...")
    sample_pub_dirs = sorted(glob.glob(os.path.join(
        _paths.PROJECT_ROOT, "hf_data_staging", "core_privacy",
        "llm", "claude-sonnet-4-6", "public_only", "seed_*")))
    sample_pub_jsonls_llm = [os.path.join(d, "rounds.jsonl") for d in sample_pub_dirs
                              if os.path.exists(os.path.join(d, "rounds.jsonl"))]
    sample_pub_jsonls_heur = [j for cond, _seed, j in discover_heuristic_runs()
                               if cond == "public_only"]
    primary = benchmark_primary_dims(sample_pub_jsonls_llm[0])

    llm_pts  = _build_panel_b_points(df_llm,  sample_pub_jsonls_llm,  primary,
                                     exclude_bm=[])
    heur_pts = _build_panel_b_points(df_heur, sample_pub_jsonls_heur, primary,
                                     exclude_bm=[])
    print(f"  panel-b points (13-bm): LLM N={len(llm_pts)}, heur N={len(heur_pts)}")

    n_llm_pub  = int(df_llm[df_llm.condition == "public_only"]["seed"].nunique())
    n_heur_pub = int(df_heur[df_heur.condition == "public_only"]["seed"].nunique())

    # ── Render: 13-bm appendix figure ──
    print("\nRendering full 13-bm figure -> privacy_gap_full.{pdf,png}")
    bm_full = _bm_ordering_for_panel_a(agg_llm, list(BM_ORDER))
    render(agg_llm, agg_heur, llm_pts, heur_pts,
           bm_list_panel_a=bm_full,
           n_llm_pub=n_llm_pub, n_heur_pub=n_heur_pub,
           out_path_no_ext=os.path.join(out_dir, "privacy_gap_full"),
           panel_a_title="(a) Per-benchmark gap across privacy ladder (all 13 benchmarks)")


if __name__ == "__main__":
    main()
