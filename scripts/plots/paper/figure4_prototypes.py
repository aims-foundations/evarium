"""Prototype alternatives for Figure 4 (heuristic_vs_llm) that show all 5 privacy conditions.

Current Figure 4 shows only public_only vs private_only. This script produces 5 distinct
layout options so the user can pick one. Each prototype panels heuristic (left) vs LLM (right).

Run from project root:
    python -m scripts.plots.paper.figure4_prototypes

Outputs to output/paper/fig4_proto_*.png
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.plots.per_benchmark_core_privacy import (
    build_long_df, _agg_per_condition, EXCLUDE_BM,
    PRIV_COLORS,
)
from scripts.plots.per_benchmark import BM_ORDER

PRIV_ORDER = ["public_only", "baseline", "private_dominant", "private_only", "iid_holdout"]
# For the ladder x-axis, we want iid_holdout (null control) near public_only:
PRIV_LADDER_ORDER = ["public_only", "iid_holdout", "baseline", "private_dominant", "private_only"]

PRIV_LABELS = {
    "public_only":      "public (13/0/0)",
    "baseline":         "baseline (8/3/2 mix)",
    "private_dominant": "private-dominant (0/13/0, cos=0.95)",
    "private_only":     "private (0/0/13, cos=0.85)",
    "iid_holdout":      "iid-holdout null (0/0/13, cos=1.0)",
}

HEUR_CSV = PROJECT_ROOT / "sandbox" / "experiments" / "heuristic_session49" / "per_benchmark_long.csv"
OUT_DIR = PROJECT_ROOT / "output" / "paper"


def load_data():
    """Return (heur_agg, llm_agg, bm_sorted) — all 5 conditions, 11 benchmarks."""
    hdf = pd.read_csv(HEUR_CSV)
    sub_h = hdf[(hdf.structural == "none") & (hdf.condition.isin(PRIV_ORDER))]
    sub_h = sub_h[~sub_h["benchmark"].isin(EXCLUDE_BM)]
    g_h = sub_h.groupby(["condition", "seed", "benchmark"])["clean_gap"].mean().reset_index()
    heur = g_h.groupby(["benchmark", "condition"])["clean_gap"].agg(
        mean="mean", sd="std", n="count"
    ).reset_index()
    heur["ci"] = np.where(heur["n"] > 1, 1.96 * heur["sd"] / np.sqrt(heur["n"]), 0.0)

    df_llm = build_long_df("_core_privacy", "sonnet")
    sub_l = df_llm[df_llm.condition.isin(PRIV_ORDER)]
    sub_l = sub_l[~sub_l["benchmark"].isin(EXCLUDE_BM)]
    llm = _agg_per_condition(sub_l)

    # Order by heuristic public_only descending
    order_map = heur[heur.condition == "public_only"].set_index("benchmark")["mean"]
    keep = [b for b in BM_ORDER if b not in EXCLUDE_BM]
    bm_sorted = (order_map.reindex([b for b in keep if b in order_map.index])
                          .dropna().sort_values(ascending=False).index.tolist())
    return heur, llm, bm_sorted


# ─────────────────────── Proto A: 5-bar grouped horizontal bars ───────────────────────

def proto_A_grouped_bars(heur, llm, bm_sorted, out_path):
    fig, axes = plt.subplots(1, 2, figsize=(13.0, 5.5), sharey=True,
                             gridspec_kw={"wspace": 0.08})
    n_cond = len(PRIV_ORDER)
    bar_h = 0.15
    offsets = np.linspace(-bar_h * (n_cond - 1) / 2, bar_h * (n_cond - 1) / 2, n_cond)

    def _draw(ax, agg):
        for i, bm in enumerate(bm_sorted):
            for j, cond in enumerate(PRIV_ORDER):
                row = agg[(agg.benchmark == bm) & (agg.condition == cond)]
                if not len(row):
                    continue
                v = float(row["mean"].iloc[0])
                ci = float(row["ci"].iloc[0])
                ax.barh(i + offsets[j], v, bar_h,
                        xerr=ci if ci > 0 else None,
                        color=PRIV_COLORS[cond], edgecolor="black", linewidth=0.3,
                        capsize=0, zorder=3)
        ax.axvline(0, color="black", lw=1.0, alpha=0.7)
        ax.set_xlabel("Per-benchmark clean gap")

    _draw(axes[0], heur)
    axes[0].set_title("Heuristic (N=30)", loc="left", fontsize=11, fontweight="bold")
    axes[0].set_yticks(np.arange(len(bm_sorted)))
    axes[0].set_yticklabels(bm_sorted)
    axes[0].invert_yaxis()

    _draw(axes[1], llm)
    axes[1].set_title("LLM — Claude Sonnet 4.6", loc="left", fontsize=11, fontweight="bold")

    handles = [Rectangle((0, 0), 1, 1, facecolor=PRIV_COLORS[c], edgecolor="black",
                         label=PRIV_LABELS[c]) for c in PRIV_ORDER]
    axes[1].legend(handles=handles, loc="lower right", fontsize=9, frameon=True,
                   title="privacy condition", title_fontsize=9)
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved {out_path}")


# ─────────────────────── Proto B: paired forest (dodged points) ───────────────────────

def proto_B_forest(heur, llm, bm_sorted, out_path):
    fig, axes = plt.subplots(1, 2, figsize=(13.0, 5.6), sharey=True,
                             gridspec_kw={"wspace": 0.08})
    n_cond = len(PRIV_ORDER)
    dodge = np.linspace(-0.28, 0.28, n_cond)

    def _draw(ax, agg):
        y_pos = np.arange(len(bm_sorted))
        # Track max extent (point + CI) for placing Δg labels
        panel_max_x = -np.inf
        for j, cond in enumerate(PRIV_ORDER):
            xs, ys, cis = [], [], []
            for i, bm in enumerate(bm_sorted):
                row = agg[(agg.benchmark == bm) & (agg.condition == cond)]
                if len(row):
                    xs.append(float(row["mean"].iloc[0]))
                    cis.append(float(row["ci"].iloc[0]))
                    ys.append(y_pos[i] + dodge[j])
                    panel_max_x = max(panel_max_x, xs[-1] + cis[-1])
                else:
                    xs.append(np.nan); cis.append(0); ys.append(np.nan)
            ax.errorbar(xs, ys, xerr=cis, fmt="o", markersize=5,
                        color=PRIV_COLORS[cond], capsize=2, lw=1.0, elinewidth=0.9,
                        markeredgecolor="black", markeredgewidth=0.3, zorder=3)

        # Signed Δg per benchmark, placed at fixed x just past the rightmost datum
        label_x = panel_max_x + 0.004
        for i, bm in enumerate(bm_sorted):
            pub = agg[(agg.benchmark == bm) & (agg.condition == "public_only")]
            priv = agg[(agg.benchmark == bm) & (agg.condition == "private_only")]
            if len(pub) and len(priv):
                dg = float(priv["mean"].iloc[0]) - float(pub["mean"].iloc[0])
                ax.text(label_x, y_pos[i], f"Δg={dg:+.3f}",
                        fontsize=8, va="center", color="#444")

        ax.axvline(0, color="black", lw=1.0, alpha=0.7)
        ax.set_xlabel("Gap (g): score − matched satisfaction")
        # Extend xlim to fit Δg labels
        xmin, xmax = ax.get_xlim()
        ax.set_xlim(xmin, max(xmax, label_x + 0.022))

    _draw(axes[0], heur)
    axes[0].set_title("Heuristic (N=30)", loc="left", fontsize=11, fontweight="bold")
    axes[0].set_yticks(np.arange(len(bm_sorted)))
    axes[0].set_yticklabels(bm_sorted)
    axes[0].invert_yaxis()

    _draw(axes[1], llm)
    axes[1].set_title("LLM — Claude Sonnet 4.6", loc="left", fontsize=11, fontweight="bold")

    # Shared legend below both panels (freed from bottom-right of LLM panel)
    handles = [Line2D([0], [0], marker="o", color="w",
                      markerfacecolor=PRIV_COLORS[c], markeredgecolor="black",
                      markersize=7, label=PRIV_LABELS[c])
               for c in PRIV_ORDER]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.02),
               ncol=5, fontsize=9, frameon=False,
               columnspacing=1.8, handletextpad=0.6)
    fig.tight_layout(rect=[0, 0.06, 1, 1])
    fig.savefig(out_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved {out_path}")


# ─────────────────────── Proto C: ladder line plot (conditions on x) ───────────────────────

def proto_C_ladder_lines(heur, llm, bm_sorted, out_path):
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.8), sharey=True,
                             gridspec_kw={"wspace": 0.08})

    cmap = plt.cm.get_cmap("tab20", len(bm_sorted) + 2)
    bm_colors = {bm: cmap(i) for i, bm in enumerate(bm_sorted)}

    def _draw(ax, agg):
        for bm in bm_sorted:
            ys = []
            for cond in PRIV_LADDER_ORDER:
                row = agg[(agg.benchmark == bm) & (agg.condition == cond)]
                ys.append(float(row["mean"].iloc[0]) if len(row) else np.nan)
            ax.plot(range(len(PRIV_LADDER_ORDER)), ys,
                    marker="o", markersize=4, linewidth=1.2, alpha=0.85,
                    color=bm_colors[bm], label=bm)
        ax.axhline(0, color="black", lw=1.0, alpha=0.5)
        ax.set_xticks(range(len(PRIV_LADDER_ORDER)))
        ax.set_xticklabels([PRIV_LABELS[c] for c in PRIV_LADDER_ORDER],
                           rotation=25, ha="right", fontsize=9)
        ax.set_ylabel("Per-benchmark clean gap")

    _draw(axes[0], heur)
    axes[0].set_title("Heuristic (N=30)", loc="left", fontsize=11, fontweight="bold")
    _draw(axes[1], llm)
    axes[1].set_title("LLM — Claude Sonnet 4.6", loc="left", fontsize=11, fontweight="bold")

    axes[1].legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=8.5,
                   frameon=False, title="benchmark", title_fontsize=9)
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved {out_path}")


# ─────────────────────── Proto D: heatmap matrix ───────────────────────

def proto_D_heatmap(heur, llm, bm_sorted, out_path):
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 5.2), sharey=True,
                             gridspec_kw={"wspace": 0.08, "width_ratios": [1, 1]})

    def _draw(ax, agg, show_cbar):
        mat = np.full((len(bm_sorted), len(PRIV_ORDER)), np.nan)
        for i, bm in enumerate(bm_sorted):
            for j, cond in enumerate(PRIV_ORDER):
                row = agg[(agg.benchmark == bm) & (agg.condition == cond)]
                if len(row):
                    mat[i, j] = float(row["mean"].iloc[0])
        im = ax.imshow(mat, cmap="RdBu_r", vmin=-0.06, vmax=0.06, aspect="auto")
        for i in range(len(bm_sorted)):
            for j in range(len(PRIV_ORDER)):
                v = mat[i, j]
                if not np.isnan(v):
                    txt_color = "white" if abs(v) > 0.04 else "black"
                    ax.text(j, i, f"{v:+.2f}", ha="center", va="center",
                            fontsize=8, color=txt_color)
        ax.set_xticks(range(len(PRIV_ORDER)))
        ax.set_xticklabels([PRIV_LABELS[c] for c in PRIV_ORDER],
                           rotation=25, ha="right", fontsize=9)
        if show_cbar:
            cbar = plt.colorbar(im, ax=ax, fraction=0.04, pad=0.02)
            cbar.set_label("gap", fontsize=9)
            cbar.ax.tick_params(labelsize=8)
        return im

    _draw(axes[0], heur, show_cbar=False)
    axes[0].set_title("Heuristic (N=30)", loc="left", fontsize=11, fontweight="bold")
    axes[0].set_yticks(np.arange(len(bm_sorted)))
    axes[0].set_yticklabels(bm_sorted)

    _draw(axes[1], llm, show_cbar=True)
    axes[1].set_title("LLM — Claude Sonnet 4.6", loc="left", fontsize=11, fontweight="bold")

    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved {out_path}")


# ─────────────────────── Proto E: delta-vs-public_only bars ───────────────────────

def proto_E_delta_bars(heur, llm, bm_sorted, out_path):
    """4 bars per benchmark: gap(cond) − gap(public_only) for each non-public condition."""
    other_conds = ["baseline", "private_dominant", "private_only", "iid_holdout"]
    fig, axes = plt.subplots(1, 2, figsize=(13.0, 5.0), sharey=True,
                             gridspec_kw={"wspace": 0.08})
    n_cond = len(other_conds)
    bar_h = 0.18
    offsets = np.linspace(-bar_h * (n_cond - 1) / 2, bar_h * (n_cond - 1) / 2, n_cond)

    def _draw(ax, agg):
        for i, bm in enumerate(bm_sorted):
            pub_row = agg[(agg.benchmark == bm) & (agg.condition == "public_only")]
            if not len(pub_row):
                continue
            pub_v = float(pub_row["mean"].iloc[0])
            for j, cond in enumerate(other_conds):
                row = agg[(agg.benchmark == bm) & (agg.condition == cond)]
                if not len(row):
                    continue
                delta = float(row["mean"].iloc[0]) - pub_v
                ax.barh(i + offsets[j], delta, bar_h,
                        color=PRIV_COLORS[cond], edgecolor="black", linewidth=0.3,
                        zorder=3)
        ax.axvline(0, color="black", lw=1.2, alpha=0.7)
        ax.set_xlabel("Δg vs public_only")

    _draw(axes[0], heur)
    axes[0].set_title("Heuristic (N=30)", loc="left", fontsize=11, fontweight="bold")
    axes[0].set_yticks(np.arange(len(bm_sorted)))
    axes[0].set_yticklabels(bm_sorted)
    axes[0].invert_yaxis()

    _draw(axes[1], llm)
    axes[1].set_title("LLM — Claude Sonnet 4.6", loc="left", fontsize=11, fontweight="bold")

    handles = [Rectangle((0, 0), 1, 1, facecolor=PRIV_COLORS[c], edgecolor="black",
                         label=PRIV_LABELS[c]) for c in other_conds]
    axes[1].legend(handles=handles, loc="lower right", fontsize=9, frameon=True,
                   title="Δ vs public_only", title_fontsize=9)
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved {out_path}")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    heur, llm, bm_sorted = load_data()
    proto_A_grouped_bars(heur, llm, bm_sorted, OUT_DIR / "fig4_proto_A_grouped_bars.png")
    proto_B_forest(heur, llm, bm_sorted, OUT_DIR / "fig4_proto_B_forest.png")
    proto_C_ladder_lines(heur, llm, bm_sorted, OUT_DIR / "fig4_proto_C_ladder.png")
    proto_D_heatmap(heur, llm, bm_sorted, OUT_DIR / "fig4_proto_D_heatmap.png")
    proto_E_delta_bars(heur, llm, bm_sorted, OUT_DIR / "fig4_proto_E_delta_bars.png")


if __name__ == "__main__":
    main()
