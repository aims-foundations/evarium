"""Prototype alternatives for Figure 4 (heuristic_vs_llm) that show all 5 privacy conditions.

Current Figure 4 shows only public_only vs private_only. This script produces several distinct
layout options so the user can pick one. Most variants panel heuristic vs LLM.

Run from project root:
    python -m scripts.plots.paper.figure4_prototypes [--only B,B_overlay,B_pooled,B_2x2,B_all,A,C,D,E]

Default: B + B_all + B_overlay + B_pooled + B_2x2 (all session-62 main-body candidates).

Outputs to output/paper/fig4_proto_*.png
"""
from __future__ import annotations

import argparse
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


def _two_line_labels(labels):
    """Split each label on its first whitespace into two lines for compact y-tick rendering."""
    return [l.replace(" ", "\n", 1) for l in labels]


# ─────────────────────── Data loading (canonical staging) ───────────────────────

def _load_llm_one(model_short: str):
    """Load + aggregate one LLM model from canonical hf_data_staging via patched discover_runs."""
    df_llm = build_long_df("_core_privacy", model_short)
    sub_l = df_llm[df_llm.condition.isin(PRIV_ORDER)]
    sub_l = sub_l[~sub_l["benchmark"].isin(EXCLUDE_BM)]
    return _agg_per_condition(sub_l)


def _load_heuristic_and_order():
    """Load heuristic data and return (heur, bm_sorted)."""
    hdf = pd.read_csv(HEUR_CSV)
    sub_h = hdf[(hdf.structural == "none") & (hdf.condition.isin(PRIV_ORDER))]
    sub_h = sub_h[~sub_h["benchmark"].isin(EXCLUDE_BM)]
    g_h = sub_h.groupby(["condition", "seed", "benchmark"])["clean_gap"].mean().reset_index()
    heur = g_h.groupby(["benchmark", "condition"])["clean_gap"].agg(
        mean="mean", sd="std", n="count"
    ).reset_index()
    heur["ci"] = np.where(heur["n"] > 1, 1.96 * heur["sd"] / np.sqrt(heur["n"]), 0.0)

    order_map = heur[heur.condition == "public_only"].set_index("benchmark")["mean"]
    keep = [b for b in BM_ORDER if b not in EXCLUDE_BM]
    bm_sorted = (order_map.reindex([b for b in keep if b in order_map.index])
                          .dropna().sort_values(ascending=False).index.tolist())
    return heur, bm_sorted


def load_data():
    """Return (heur_agg, sonnet_llm_agg, bm_sorted) — Sonnet-only LLM, canonical staging path."""
    heur, bm_sorted = _load_heuristic_and_order()
    sonnet = _load_llm_one("sonnet")
    return heur, sonnet, bm_sorted


def load_data_all_llms():
    """Return (heur_agg, {model_short: agg_df}, bm_sorted) — all 3 LLM models from canonical staging."""
    heur, bm_sorted = _load_heuristic_and_order()
    llms = {m: _load_llm_one(m) for m in ("sonnet", "opus", "gpt55")}
    return heur, llms, bm_sorted


# ─────────────────────── Shared forest draw helpers ───────────────────────

def _forest_draw(ax, agg, bm_sorted):
    """Single-panel forest: 5 dots + CI per benchmark row, Δg label at right."""
    n_cond = len(PRIV_ORDER)
    dodge = np.linspace(-0.28, 0.28, n_cond)
    y_pos = np.arange(len(bm_sorted))
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
    xmin, xmax = ax.get_xlim()
    ax.set_xlim(xmin, max(xmax, label_x + 0.022))


def _attach_legend(fig):
    """Bottom-centered legend: privacy conditions only."""
    handles = [Line2D([0], [0], marker="o", color="w",
                      markerfacecolor=PRIV_COLORS[c], markeredgecolor="black",
                      markersize=7, label=PRIV_LABELS[c])
               for c in PRIV_ORDER]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.02),
               ncol=5, fontsize=9, frameon=False,
               columnspacing=1.8, handletextpad=0.6)


# ─────────────────────── Proto A: 5-bar grouped horizontal bars ───────────────────────

def proto_A_grouped_bars(heur, llm, bm_sorted, out_path):
    fig, axes = plt.subplots(1, 2, figsize=(13.0, 6.5), sharey=True,
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
    axes[0].set_yticklabels(_two_line_labels(bm_sorted))
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
    """2-panel forest: heuristic (left) | Sonnet 4.6 (right)."""
    fig, axes = plt.subplots(1, 2, figsize=(13.0, 6.6), sharey=True,
                             gridspec_kw={"wspace": 0.08})
    _forest_draw(axes[0], heur, bm_sorted)
    axes[0].set_title("Heuristic (N=30)", loc="left", fontsize=11, fontweight="bold")
    axes[0].set_yticks(np.arange(len(bm_sorted)))
    axes[0].set_yticklabels(_two_line_labels(bm_sorted))
    axes[0].invert_yaxis()

    _forest_draw(axes[1], llm, bm_sorted)
    axes[1].set_title("LLM — Claude Sonnet 4.6 (N=10)", loc="left", fontsize=11, fontweight="bold")

    _attach_legend(fig)
    fig.tight_layout(rect=[0, 0.06, 1, 1])
    fig.savefig(out_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved {out_path}")


# Cross-model titles + markers (for all_llms / overlay / pooled / 2x2 variants).
_LLM_PANEL_TITLES = {
    "sonnet": "Claude Sonnet 4.6",
    "opus":   "Claude Opus 4.6",
    "gpt55":  "GPT-5.5 (2026-04-23)",
}
_LLM_MODEL_MARKERS = {"sonnet": "o", "opus": "s", "gpt55": "^"}
_LLM_MODEL_SHORT = {"sonnet": "Sonnet", "opus": "Opus", "gpt55": "GPT-5.5"}


def proto_B_forest_all_llms(heur, llm_dict, bm_sorted, out_path,
                             order=("sonnet", "opus", "gpt55")):
    """4-panel single-row forest: heuristic | Sonnet | Opus | GPT-5.5."""
    n_panels = 1 + len(order)
    fig, axes = plt.subplots(1, n_panels, figsize=(5.5 * n_panels, 6.6), sharey=True,
                             gridspec_kw={"wspace": 0.08})
    _forest_draw(axes[0], heur, bm_sorted)
    axes[0].set_title("Heuristic (N=30)", loc="left", fontsize=11, fontweight="bold")
    axes[0].set_yticks(np.arange(len(bm_sorted)))
    axes[0].set_yticklabels(_two_line_labels(bm_sorted))
    axes[0].invert_yaxis()

    for i, model in enumerate(order):
        agg = llm_dict[model]
        _forest_draw(axes[i + 1], agg, bm_sorted)
        n_seeds = int(agg["n"].max()) if len(agg) else 0
        axes[i + 1].set_title(f"LLM — {_LLM_PANEL_TITLES.get(model, model)} (N={n_seeds})",
                              loc="left", fontsize=11, fontweight="bold")

    _attach_legend(fig)
    fig.tight_layout(rect=[0, 0.06, 1, 1])
    fig.savefig(out_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved {out_path}")


def _forest_draw_overlay(ax, llm_dict, bm_sorted, model_order=("sonnet", "opus", "gpt55")):
    """Forest where each (benchmark, condition) cell gets one marker per model.
    Color = condition; marker shape = model. Tight per-condition x-jitter to avoid stacking."""
    n_cond = len(PRIV_ORDER)
    n_models = len(model_order)
    cond_dodge = np.linspace(-0.30, 0.30, n_cond)
    model_jitter = np.linspace(-0.06, 0.06, n_models) if n_models > 1 else [0.0]
    y_pos = np.arange(len(bm_sorted))
    panel_max_x = -np.inf

    for j, cond in enumerate(PRIV_ORDER):
        for k, model in enumerate(model_order):
            agg = llm_dict[model]
            for i, bm in enumerate(bm_sorted):
                row = agg[(agg.benchmark == bm) & (agg.condition == cond)]
                if not len(row):
                    continue
                x = float(row["mean"].iloc[0])
                ci = float(row["ci"].iloc[0])
                y = y_pos[i] + cond_dodge[j] + model_jitter[k]
                ax.errorbar([x], [y], xerr=[ci], fmt=_LLM_MODEL_MARKERS[model],
                            markersize=4.5, color=PRIV_COLORS[cond], capsize=1.5,
                            lw=0.8, elinewidth=0.7,
                            markeredgecolor="black", markeredgewidth=0.3, zorder=3)
                panel_max_x = max(panel_max_x, x + ci)

    label_x = panel_max_x + 0.004
    for i, bm in enumerate(bm_sorted):
        dg_vals = []
        for model in model_order:
            agg = llm_dict[model]
            pub = agg[(agg.benchmark == bm) & (agg.condition == "public_only")]
            priv = agg[(agg.benchmark == bm) & (agg.condition == "private_only")]
            if len(pub) and len(priv):
                dg_vals.append(float(priv["mean"].iloc[0]) - float(pub["mean"].iloc[0]))
        if dg_vals:
            ax.text(label_x, y_pos[i], f"Δg̅={np.mean(dg_vals):+.3f}",
                    fontsize=8, va="center", color="#444")
    ax.axvline(0, color="black", lw=1.0, alpha=0.7)
    ax.set_xlabel("Gap (g): score − matched satisfaction")
    xmin, xmax = ax.get_xlim()
    ax.set_xlim(xmin, max(xmax, label_x + 0.024))


def _attach_overlay_legend(fig):
    """Two-row legend: privacy conditions (color) on top, LLM models (marker) below."""
    cond_handles = [Line2D([0], [0], marker="o", color="w",
                           markerfacecolor=PRIV_COLORS[c], markeredgecolor="black",
                           markersize=7, label=PRIV_LABELS[c])
                    for c in PRIV_ORDER]
    model_handles = [Line2D([0], [0], marker=_LLM_MODEL_MARKERS[m], color="w",
                            markerfacecolor="#888", markeredgecolor="black",
                            markersize=7, label=_LLM_MODEL_SHORT[m])
                     for m in ("sonnet", "opus", "gpt55")]
    fig.legend(handles=cond_handles, loc="lower center", bbox_to_anchor=(0.5, -0.02),
               ncol=5, fontsize=9, frameon=False, columnspacing=1.6, handletextpad=0.4)
    fig.legend(handles=model_handles, loc="lower center", bbox_to_anchor=(0.5, -0.07),
               ncol=3, fontsize=9, frameon=False,
               columnspacing=2.0, handletextpad=0.4, title="LLM model (marker)",
               title_fontsize=8)


def proto_B_forest_llm_overlay(heur, llm_dict, bm_sorted, out_path):
    """2-panel forest: heuristic | LLM (3 models overlaid via marker shape, color=condition)."""
    fig, axes = plt.subplots(1, 2, figsize=(13.0, 6.6), sharey=True,
                             gridspec_kw={"wspace": 0.08})
    _forest_draw(axes[0], heur, bm_sorted)
    axes[0].set_title("Heuristic (N=30)", loc="left", fontsize=11, fontweight="bold")
    axes[0].set_yticks(np.arange(len(bm_sorted)))
    axes[0].set_yticklabels(_two_line_labels(bm_sorted))
    axes[0].invert_yaxis()

    _forest_draw_overlay(axes[1], llm_dict, bm_sorted)
    n_total = sum(int(llm_dict[m]["n"].max()) for m in ("sonnet", "opus", "gpt55") if len(llm_dict[m]))
    axes[1].set_title(f"LLM — Sonnet 4.6 + Opus 4.6 + GPT-5.5 overlaid (Σ N={n_total})",
                      loc="left", fontsize=11, fontweight="bold")

    _attach_overlay_legend(fig)
    fig.tight_layout(rect=[0, 0.10, 1, 1])
    fig.savefig(out_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved {out_path}")


def _aggregate_llm_pooled(llm_dict, model_order=("sonnet", "opus", "gpt55")):
    """Pool seeds across all LLM models per (benchmark, condition). Produces a single
    agg-style DataFrame so _forest_draw can render it as one set of dots.
    Pooled mean: weighted by n_i. Pooled var: includes between-model mean shift."""
    rows = []
    keys = set()
    for m in model_order:
        for _, r in llm_dict[m].iterrows():
            keys.add((r["benchmark"], r["condition"]))
    for (bm, cond) in sorted(keys):
        means, sds, ns = [], [], []
        for m in model_order:
            sub = llm_dict[m]
            row = sub[(sub.benchmark == bm) & (sub.condition == cond)]
            if not len(row):
                continue
            means.append(float(row["mean"].iloc[0]))
            sds.append(float(row["sd"].iloc[0]) if not pd.isna(row["sd"].iloc[0]) else 0.0)
            ns.append(int(row["n"].iloc[0]))
        if not ns:
            continue
        N = sum(ns)
        pooled_mean = sum(n * m_ for n, m_ in zip(ns, means)) / N
        pooled_var = sum(n * (sd ** 2 + (m_ - pooled_mean) ** 2)
                         for n, m_, sd in zip(ns, means, sds)) / N
        pooled_sd = float(np.sqrt(pooled_var))
        pooled_ci = 1.96 * pooled_sd / np.sqrt(N) if N > 1 else 0.0
        rows.append({"benchmark": bm, "condition": cond,
                     "mean": pooled_mean, "sd": pooled_sd, "n": N, "ci": pooled_ci})
    return pd.DataFrame(rows)


def proto_B_forest_llm_aggregate(heur, llm_dict, bm_sorted, out_path):
    """2-panel forest: heuristic | all-LLMs-pooled (Sonnet+Opus+GPT-5.5 treated as one)."""
    fig, axes = plt.subplots(1, 2, figsize=(13.0, 6.6), sharey=True,
                             gridspec_kw={"wspace": 0.08})
    _forest_draw(axes[0], heur, bm_sorted)
    axes[0].set_title("Heuristic (N=30)", loc="left", fontsize=11, fontweight="bold")
    axes[0].set_yticks(np.arange(len(bm_sorted)))
    axes[0].set_yticklabels(_two_line_labels(bm_sorted))
    axes[0].invert_yaxis()

    pooled = _aggregate_llm_pooled(llm_dict)
    _forest_draw(axes[1], pooled, bm_sorted)
    N = int(pooled["n"].max()) if len(pooled) else 0
    axes[1].set_title(f"LLM — pooled (Sonnet + Opus + GPT-5.5, ΣN={N})",
                      loc="left", fontsize=11, fontweight="bold")

    _attach_legend(fig)
    fig.tight_layout(rect=[0, 0.06, 1, 1])
    fig.savefig(out_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved {out_path}")


def proto_B_forest_2x2(heur, llm_dict, bm_sorted, out_path,
                        order=("sonnet", "opus", "gpt55")):
    """4-panel 2x2 grid: heur top-left, then 3 LLMs in remaining cells. Square aspect for
    appendix use; preserves all info but more compact than 1x4 layout."""
    fig, axes = plt.subplots(2, 2, figsize=(13.0, 13.0), sharey=False,
                             gridspec_kw={"wspace": 0.08, "hspace": 0.20})
    panels = [(axes[0, 0], "Heuristic (N=30)", heur)]
    for i, model in enumerate(order):
        row, col = divmod(i + 1, 2)
        agg = llm_dict[model]
        n_seeds = int(agg["n"].max()) if len(agg) else 0
        title = f"LLM — {_LLM_PANEL_TITLES.get(model, model)} (N={n_seeds})"
        panels.append((axes[row, col], title, agg))

    for ax, title, agg in panels:
        _forest_draw(ax, agg, bm_sorted)
        ax.set_title(title, loc="left", fontsize=11, fontweight="bold")
        ax.set_yticks(np.arange(len(bm_sorted)))
        ax.set_yticklabels(_two_line_labels(bm_sorted))
        ax.invert_yaxis()

    _attach_legend(fig)
    fig.tight_layout(rect=[0, 0.04, 1, 1])
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
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 6.2), sharey=True,
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
    axes[0].set_yticklabels(_two_line_labels(bm_sorted))

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
    fig, axes = plt.subplots(1, 2, figsize=(13.0, 6.0), sharey=True,
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
    axes[0].set_yticklabels(_two_line_labels(bm_sorted))
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
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None,
                    help="Comma-separated subset to render: B, B_all, B_overlay, B_pooled, B_2x2, A, C, D, E. "
                         "Default: B + B_all + B_overlay + B_pooled + B_2x2.")
    args = ap.parse_args()
    only = (set(args.only.split(",")) if args.only
            else {"B", "B_all", "B_overlay", "B_pooled", "B_2x2"})

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    sonnet_needed = bool(only & {"A", "B", "C", "D", "E"})
    if sonnet_needed:
        heur, sonnet, bm_sorted = load_data()
        if "A" in only:
            proto_A_grouped_bars(heur, sonnet, bm_sorted, OUT_DIR / "fig4_proto_A_grouped_bars.png")
        if "B" in only:
            proto_B_forest(heur, sonnet, bm_sorted, OUT_DIR / "fig4_proto_B_forest_sonnet.png")
        if "C" in only:
            proto_C_ladder_lines(heur, sonnet, bm_sorted, OUT_DIR / "fig4_proto_C_ladder.png")
        if "D" in only:
            proto_D_heatmap(heur, sonnet, bm_sorted, OUT_DIR / "fig4_proto_D_heatmap.png")
        if "E" in only:
            proto_E_delta_bars(heur, sonnet, bm_sorted, OUT_DIR / "fig4_proto_E_delta_bars.png")

    all_llms_needed = bool(only & {"B_all", "B_overlay", "B_pooled", "B_2x2"})
    if all_llms_needed:
        heur, llms, bm_sorted = load_data_all_llms()
        if "B_all" in only:
            proto_B_forest_all_llms(heur, llms, bm_sorted, OUT_DIR / "fig4_proto_B_forest_all_llms.png")
        if "B_overlay" in only:
            proto_B_forest_llm_overlay(heur, llms, bm_sorted,
                                        OUT_DIR / "fig4_proto_B_forest_llm_overlay.png")
        if "B_pooled" in only:
            proto_B_forest_llm_aggregate(heur, llms, bm_sorted,
                                          OUT_DIR / "fig4_proto_B_forest_llm_pooled.png")
        if "B_2x2" in only:
            proto_B_forest_2x2(heur, llms, bm_sorted, OUT_DIR / "fig4_proto_B_forest_2x2.png")


if __name__ == "__main__":
    main()
