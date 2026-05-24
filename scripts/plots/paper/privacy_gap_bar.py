"""Privacy-gap two-panel figure — bar-plot variant.

(a) Grouped bar plot: per-benchmark gap g (= published score − matched consumer
    satisfaction) for public_only vs private_only only, across all 11 non-outlier
    benchmarks (Agentic Tasks and Function Calling excluded as calibration outliers).
    Solid bars = LLM Sonnet 4.6; hatched bars = heuristic-mode (larger N).

(b) Unchanged from privacy_gap_main: Δg = gap@private_only − gap@public_only vs
    provider over-investment on each benchmark's primary dimension.

Outputs (PDF + PNG):
    output/paper/privacy_gap_bar.pdf

Usage:
    python -m scripts.plots.paper.privacy_gap_bar
"""
from __future__ import annotations

import argparse
import glob
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.plots import paths as _paths
from scripts.plots.per_benchmark import (
    per_benchmark_from_jsonl, BM_ORDER, EXCLUDE_BM as _EXCL_DEF, DIMS,
)
from scripts.plots.per_benchmark_core_privacy import build_long_df, _agg_per_condition

# Reuse helpers from the main figure without circular import.
from scripts.plots.paper.privacy_gap_main import (
    PRIV_ORDER, PRIV_LABELS, PRIV_COLORS, DIM_COLORS,
    MS_PANEL_B, ELW,
    discover_heuristic_runs,
    build_long_df_heuristic,
    benchmark_primary_dims,
    population_capability_surplus,
    _delta_gap,
    _build_panel_b_points,
    _draw_scatter,
    _attach_panel_b_legend,
)

EXCLUDE_BM = list(_EXCL_DEF)
BM_KEEP = [b for b in BM_ORDER if b not in EXCLUDE_BM]

BAR_CONDITIONS = ["public_only", "private_only"]

plt.rcParams.update({
    "font.size":         13,
    "axes.titlesize":    14,
    "axes.labelsize":    13,
    "xtick.labelsize":   11,
    "ytick.labelsize":   12,
    "legend.fontsize":   12,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "font.family":       "DejaVu Sans",
    "savefig.dpi":       180,
})

BAR_W = 0.33         # width of each bar
BAR_GAP = 0.08       # gap between the two condition bars within a group


def _bm_ordering_bar(agg_llm: pd.DataFrame, bm_list: list[str]) -> list[str]:
    """Order benchmarks by LLM public_only mean descending."""
    pub = agg_llm[agg_llm.condition == "public_only"].set_index("benchmark")["mean"]
    keep = [b for b in bm_list if b in pub.index]
    return list(pub.reindex(keep).sort_values(ascending=False).index)


def _draw_bar(ax, agg_llm: pd.DataFrame, agg_heur: pd.DataFrame, bm_list: list[str]):
    """Grouped bar chart: public_only vs private_only, LLM solid + heuristic hatched."""
    n = len(bm_list)
    x = np.arange(n)

    offsets = {
        "public_only":  -(BAR_W / 2 + BAR_GAP / 2),
        "private_only":  (BAR_W / 2 + BAR_GAP / 2),
    }

    # Track the top of each benchmark's bar group for annotation placement.
    bar_tops = np.full(n, -np.inf)

    for cond in BAR_CONDITIONS:
        off = offsets[cond]
        color = PRIV_COLORS[cond]
        xs_heur, ys_heur, cis_heur = [], [], []
        xs_llm,  ys_llm,  cis_llm  = [], [], []
        idx_heur, idx_llm = [], []

        for i, bm in enumerate(bm_list):
            rh = agg_heur[(agg_heur.benchmark == bm) & (agg_heur.condition == cond)]
            if len(rh):
                xs_heur.append(x[i] + off)
                ys_heur.append(float(rh["mean"].iloc[0]))
                cis_heur.append(float(rh["ci"].iloc[0]))
                idx_heur.append(i)

            rl = agg_llm[(agg_llm.benchmark == bm) & (agg_llm.condition == cond)]
            if len(rl):
                xs_llm.append(x[i] + off)
                ys_llm.append(float(rl["mean"].iloc[0]))
                cis_llm.append(float(rl["ci"].iloc[0]))
                idx_llm.append(i)

        # Update bar_tops: top = max(mean + ci) across both modes and conditions.
        for k, i in enumerate(idx_heur):
            bar_tops[i] = max(bar_tops[i], ys_heur[k] + cis_heur[k])
        for k, i in enumerate(idx_llm):
            bar_tops[i] = max(bar_tops[i], ys_llm[k] + cis_llm[k])

        # Heuristic: hatched bars (drawn first / behind)
        if xs_heur:
            ax.bar(xs_heur, ys_heur, BAR_W, color="white", edgecolor=color,
                   linewidth=1.3, hatch="////", zorder=2,
                   yerr=cis_heur,
                   error_kw=dict(ecolor=color, elinewidth=ELW * 0.75, capsize=2.5))

        # LLM: solid bars (drawn on top, slightly narrower so hatch shows)
        if xs_llm:
            ax.bar(xs_llm, ys_llm, BAR_W * 0.72, color=color, edgecolor="black",
                   linewidth=0.6, zorder=4, alpha=0.92,
                   yerr=cis_llm,
                   error_kw=dict(ecolor="black", elinewidth=ELW, capsize=2.5))

    # Delta-g annotation just above each benchmark's tallest bar+CI.
    dg = _delta_gap(agg_llm)
    ax.set_xlim(-0.7, n - 0.3)
    ylo, yhi = ax.get_ylim()
    tick = (yhi - ylo) * 0.018   # small gap above the error-bar cap
    headroom = (yhi - ylo) * 0.08
    ax.set_ylim(ylo, yhi + headroom)
    for i, bm in enumerate(bm_list):
        if bm in dg and bar_tops[i] > -np.inf:
            ax.text(x[i], bar_tops[i] + tick, rf"$\Delta g$={dg[bm]:+.3f}",
                    ha="center", va="bottom", fontsize=9.5, color="#444")

    ax.axhline(0, color="black", lw=1.0, alpha=0.7)
    ax.set_ylabel(r"Gap (g) = score $-$ matched satisfaction")
    ax.set_xticks(x)
    ax.set_xticklabels([b.replace(" ", "\n", 1) for b in bm_list],
                       ha="center", fontsize=10)


def _attach_panel_a_bar_legend(ax, n_llm: int, n_heur: int, anchor_y: float = -0.13):
    """Legend: two condition colors (solid = LLM, hatched = heuristic)."""
    handles = []
    for cond in BAR_CONDITIONS:
        c = PRIV_COLORS[cond]
        lbl = PRIV_LABELS[cond].split(" (")[0]
        handles.append(Patch(facecolor=c, edgecolor="black", linewidth=0.6,
                             label=f"LLM (N={n_llm}) — {lbl}"))
        handles.append(Patch(facecolor="white", edgecolor=c, linewidth=1.3,
                             hatch="////", label=f"Heuristic (N={n_heur}) — {lbl}"))
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, anchor_y),
              ncol=2, fontsize=11.5, frameon=False,
              columnspacing=1.4, handletextpad=0.5)


def render_bar(agg_llm: pd.DataFrame, agg_heur: pd.DataFrame,
               llm_pts: pd.DataFrame, heur_pts: pd.DataFrame,
               bm_list_panel_a: list[str],
               out_path_no_ext: str,
               n_llm: int = 0, n_heur: int = 0,
               figsize: tuple[float, float] = (22.0, 7.2),
               legend_anchor_y: float = -0.13):
    fig = plt.figure(figsize=figsize)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.25, 1.0], wspace=0.20)
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])

    _draw_bar(ax_a, agg_llm, agg_heur, bm_list_panel_a)
    ax_a.set_title(
        "(a) Per-benchmark gap: public-only vs private-only (all benchmarks)",
        loc="left", fontsize=14, fontweight="bold")
    _attach_panel_a_bar_legend(ax_a, n_llm=n_llm, n_heur=n_heur, anchor_y=legend_anchor_y)

    _draw_scatter(ax_b, llm_pts, heur_pts)
    ax_b.set_title("(b) Gap shift tracks capability surplus on dominant dimension",
                   loc="left", fontsize=14, fontweight="bold")
    _attach_panel_b_legend(ax_b, anchor_y=legend_anchor_y)

    fig.tight_layout(rect=[0, 0.10, 1, 1])
    for ext in ("pdf", "png"):
        out = f"{out_path_no_ext}.{ext}"
        fig.savefig(out, bbox_inches="tight")
        print(f"  wrote {out}")
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out-dir", default=None,
                    help="Output directory (default: output/paper/)")
    args = ap.parse_args()

    out_dir = args.out_dir or _paths.paper_dir()
    os.makedirs(out_dir, exist_ok=True)

    print("Loading LLM Sonnet 4.6 (hf_data_staging/core_privacy/llm/claude-sonnet-4-6)...")
    df_llm = build_long_df("_core_privacy", "sonnet")
    df_llm = df_llm[df_llm.condition.isin(PRIV_ORDER)]
    df_llm = df_llm[~df_llm.benchmark.isin(EXCLUDE_BM)]
    print(f"  rows={len(df_llm)}, seeds={df_llm.seed.nunique()}, conds={sorted(df_llm.condition.unique())}")

    print("Loading heuristic (hf_data_staging/core_privacy/heuristic)...")
    df_heur = build_long_df_heuristic(restrict_conds=PRIV_ORDER)
    df_heur = df_heur[~df_heur.benchmark.isin(EXCLUDE_BM)]
    print(f"  rows={len(df_heur)}, seeds={df_heur.seed.nunique()}, "
          f"conds={sorted(df_heur.condition.unique())}")

    if df_llm.empty:
        sys.exit("No LLM runs discovered.")
    if df_heur.empty:
        sys.exit("No heuristic runs discovered.")

    agg_llm = _agg_per_condition(df_llm)
    g_run = df_heur.groupby(["condition", "seed", "benchmark"])["clean_gap"].mean().reset_index()
    agg_heur = g_run.groupby(["benchmark", "condition"])["clean_gap"].agg(
        mean="mean", sd="std", n="count").reset_index()
    agg_heur["ci"] = np.where(agg_heur["n"] > 1,
                               1.96 * agg_heur["sd"] / np.sqrt(agg_heur["n"]),
                               0.0)

    print("Resolving primary dimensions + population capability surplus...")
    sample_pub_dirs = sorted(glob.glob(os.path.join(
        _paths.PROJECT_ROOT, "hf_data_staging", "core_privacy",
        "llm", "claude-sonnet-4-6", "public_only", "seed_*")))
    sample_pub_jsonls_llm = [os.path.join(d, "rounds.jsonl") for d in sample_pub_dirs
                              if os.path.exists(os.path.join(d, "rounds.jsonl"))]
    sample_pub_jsonls_heur = [j for cond, _seed, j in discover_heuristic_runs()
                               if cond == "public_only"]
    primary = benchmark_primary_dims(sample_pub_jsonls_llm[0])

    llm_pts  = _build_panel_b_points(df_llm,  sample_pub_jsonls_llm,  primary)
    heur_pts = _build_panel_b_points(df_heur, sample_pub_jsonls_heur, primary)
    print(f"  panel-b points (11-bm): LLM N={len(llm_pts)}, heur N={len(heur_pts)}")

    # Order all 11 benchmarks by LLM public_only mean descending (same logic as main figure)
    n_llm  = int(df_llm[df_llm.condition == "public_only"]["seed"].nunique())
    n_heur = int(df_heur[df_heur.condition == "public_only"]["seed"].nunique())

    bm_panel_a = _bm_ordering_bar(agg_llm, BM_KEEP)
    print(f"\nRendering bar figure ({len(bm_panel_a)} benchmarks) -> privacy_gap_bar.{{pdf,png}}")
    render_bar(agg_llm, agg_heur, llm_pts, heur_pts,
               bm_list_panel_a=bm_panel_a,
               n_llm=n_llm, n_heur=n_heur,
               out_path_no_ext=os.path.join(out_dir, "privacy_gap_bar"))


if __name__ == "__main__":
    main()
