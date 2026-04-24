"""LLM-only per-benchmark gap plots for the _core_privacy batch.

Produces two figures:
    forest_llm_core_privacy.png   5-privacy forest (LLM, pooled seeds)
    bars_baseline_vs_private.png  baseline vs private_only paired bars (LLM)

Reuses per_benchmark_from_jsonl() from scripts.plots.per_benchmark.
CLI:
    python -m scripts.plots.per_benchmark_core_privacy \
        --batch _core_privacy --model sonnet
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
from collections import defaultdict

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from . import paths as _paths
from .per_benchmark import (
    per_benchmark_from_jsonl, BM_ORDER, EXCLUDE_BM as _DEFAULT_EXCLUDE_BM, PRIV_ORDER,
)

# Mutable module-level: CLI can override to include Agentic Tasks / Function Calling.
EXCLUDE_BM = list(_DEFAULT_EXCLUDE_BM)


def _bm_keep():
    """Recompute the keep-list from the current (potentially-overridden) EXCLUDE_BM."""
    return [b for b in BM_ORDER if b not in EXCLUDE_BM]

# Palette F: ColorBrewer YlOrRd ramp for the privacy axis + blue for public_only.
# Reads as "cooler = public / hotter = private"; iid_holdout is neutral gray (off-axis).
PRIV_COLORS = {
    "public_only":      "#2c7fb8",  # blue (cool anchor, off the warm ramp)
    "baseline":         "#fec44f",  # warmer yellow-orange (one step darker on YlOrRd)
    "private_dominant": "#fd8d3c",  # orange
    "private_only":     "#b10026",  # dark red
    "iid_holdout":      "#7f7f7f",  # neutral gray (off-axis ablation)
}

# Bars plot (public_only vs private_only): the clean 100% endpoints.
# Avoids baseline's 8/3/2 public-partial-private mix confound.
PUB_BAR_COLOR = PRIV_COLORS["public_only"]
PR_BAR_COLOR = PRIV_COLORS["private_only"]

plt.rcParams.update({
    "figure.dpi": 110, "savefig.dpi": 150,
    "font.size": 10, "axes.titlesize": 12, "axes.labelsize": 10,
    "xtick.labelsize": 9, "ytick.labelsize": 10, "legend.fontsize": 9,
    "axes.spines.top": False, "axes.spines.right": False,
    "font.family": "DejaVu Sans",
})


# Pattern: <condition>_s<seed>_<model>
_NAME_RE = re.compile(r"^(?P<cond>.+?)_s(?P<seed>\d+)_(?P<model>sonnet|opus)$")


def discover_runs(batch: str, model_filter: str | None = None, min_rounds: int = 40):
    """Yield (condition, seed, model, jsonl_path) for runs under sandbox/experiments/<batch>/llm/*.

    Skips runs with fewer than min_rounds rounds in rounds.jsonl (default: full 40-round runs only).
    """
    root = os.path.join(_paths.PROJECT_ROOT, "sandbox", "experiments", batch, "llm")
    dirs = sorted(glob.glob(os.path.join(root, "*")))
    for d in dirs:
        name = os.path.basename(d)
        m = _NAME_RE.match(name)
        if not m:
            continue
        cond = m.group("cond")
        seed = int(m.group("seed"))
        model = m.group("model")
        if model_filter and model != model_filter:
            continue
        jsonl = os.path.join(d, "seeds", f"seed_{seed}", "rounds.jsonl")
        if not os.path.exists(jsonl):
            continue
        with open(jsonl) as f:
            n_rounds = sum(1 for _ in f)
        if n_rounds < min_rounds:
            print(f"SKIP (partial {n_rounds}/{min_rounds}): {name}")
            continue
        yield cond, seed, model, jsonl


def build_long_df(batch: str, model_filter: str | None = None) -> pd.DataFrame:
    """Per-benchmark × per-provider long-form DataFrame across all discovered runs."""
    rows = []
    for cond, seed, model, jsonl in discover_runs(batch, model_filter):
        try:
            df = per_benchmark_from_jsonl(jsonl)
        except Exception as e:
            print(f"ERROR {jsonl}: {e}")
            continue
        for _, r in df.iterrows():
            rows.append({
                "condition": cond, "seed": seed, "model": model,
                "benchmark": r["benchmark"], "provider": r["provider"],
                "clean_gap": r["clean_gap"], "score": r["score"],
                "clean_matched": r["clean_matched"],
            })
    return pd.DataFrame(rows)


def _agg_per_condition(df_long: pd.DataFrame) -> pd.DataFrame:
    """Aggregate to (benchmark, condition): mean/sd/n using per-run (seed) means first."""
    g_run = df_long.groupby(["condition", "seed", "benchmark"])["clean_gap"].mean().reset_index()
    agg = g_run.groupby(["benchmark", "condition"])["clean_gap"].agg(
        mean="mean", sd="std", n="count"
    ).reset_index()
    # 95% CI from seed-level std; 0 when n<2.
    agg["ci"] = np.where(agg["n"] > 1, 1.96 * agg["sd"] / np.sqrt(agg["n"]), 0.0)
    return agg


# ─────────────────────── Plot 1: LLM forest (5 privacy) ───────────────────────

def plot_llm_forest(df_long: pd.DataFrame, out_path: str, title_suffix: str = ""):
    agg_full = _agg_per_condition(df_long)
    agg = agg_full[~agg_full["benchmark"].isin(EXCLUDE_BM)]
    excluded_agg = agg_full[agg_full["benchmark"].isin(EXCLUDE_BM)]

    order_src = agg[agg.condition == "public_only"].set_index("benchmark")["mean"]
    bm_sorted = (order_src.reindex([b for b in _bm_keep() if b in agg.benchmark.values])
                         .dropna().sort_values(ascending=False).index.tolist())

    # Ghost-row benchmarks (excluded outliers, dashed separator above them)
    excl_sorted = [b for b in EXCLUDE_BM if b in excluded_agg.benchmark.values]
    all_bm = bm_sorted + excl_sorted
    separator_idx = len(bm_sorted) - 0.5  # between main and excluded

    fig, ax = plt.subplots(figsize=(11, 6.5))
    y_pos = np.arange(len(all_bm))
    dodge = np.linspace(-0.28, 0.28, len(PRIV_ORDER))

    for i, cond in enumerate(PRIV_ORDER):
        xs, ys, cis = [], [], []
        for bm in all_bm:
            src = excluded_agg if bm in EXCLUDE_BM else agg
            row = src[(src.benchmark == bm) & (src.condition == cond)]
            if len(row):
                xs.append(float(row["mean"].iloc[0]))
                cis.append(float(row["ci"].iloc[0]))
                ys.append(y_pos[all_bm.index(bm)] + dodge[i])
            else:
                xs.append(np.nan); cis.append(0); ys.append(np.nan)
        # Lower alpha on excluded-benchmark dots
        alphas_list = [0.4 if bm in EXCLUDE_BM else 1.0 for bm in all_bm]
        # errorbar takes a single alpha; split into two calls for main vs excluded
        main_idx = [j for j, bm in enumerate(all_bm) if bm not in EXCLUDE_BM]
        excl_idx = [j for j, bm in enumerate(all_bm) if bm in EXCLUDE_BM]
        for idx_set, alpha_val in [(main_idx, 1.0), (excl_idx, 0.55)]:
            if not idx_set:
                continue
            ax.errorbar([xs[j] for j in idx_set],
                        [ys[j] for j in idx_set],
                        xerr=[cis[j] for j in idx_set],
                        fmt="o", markersize=6,
                        color=PRIV_COLORS[cond],
                        label=cond if (i >= 0 and alpha_val == 1.0) else None,
                        capsize=3, lw=1.2, elinewidth=1.0, alpha=alpha_val,
                        markeredgecolor="black", markeredgewidth=0.4)

    # Dashed separator + label for the excluded section
    if excl_sorted:
        ax.axhline(separator_idx, color="#555", lw=0.8, ls="--", alpha=0.7, zorder=1)
        ax.text(ax.get_xlim()[1], separator_idx - 0.1,
                "  excluded (benchmark cdw weights agentic=0.75, capability lags)",
                fontsize=7.5, style="italic", color="#555",
                va="bottom", ha="right")

    ax.axvline(0, color="black", lw=1, alpha=0.6)
    ax.set_yticks(y_pos); ax.set_yticklabels(all_bm)
    # Gray-out the excluded row labels
    for tick, bm in zip(ax.get_yticklabels(), all_bm):
        if bm in EXCLUDE_BM:
            tick.set_color("#555"); tick.set_style("italic")
    ax.invert_yaxis()
    ax.set_xlabel("Per-benchmark clean gap  (score − matched satisfaction)")
    ax.legend(title="privacy condition", loc="lower right", frameon=True, framealpha=0.9)
    ax.text(0.02, 0.97, "← benchmark underpromises",
            transform=ax.transAxes, fontsize=9, color="#1565C0", alpha=0.8)
    ax.text(0.98, 0.97, "benchmark overpromises →",
            transform=ax.transAxes, fontsize=9, color="#C62828", alpha=0.8, ha="right")
    seed_counts = df_long.groupby("condition")["seed"].nunique().to_dict()
    seed_str = ", ".join(f"{c}:{seed_counts.get(c, 0)}" for c in PRIV_ORDER)
    ax.set_title(
        "Privacy conditions compress per-benchmark gap toward zero — LLM runs\n"
        f"{title_suffix} — error bars = 95% CI where n≥2",
        loc="left")
    ax.text(0.0, -0.13,
            f"seeds per condition: {seed_str}",
            transform=ax.transAxes, fontsize=8, color="#555", style="italic")
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out_path}")


# ─────────────── Plot 2: baseline vs private_only paired bars (LLM) ───────────────

def _excluded_deltas(df_long: pd.DataFrame, cond_a: str, cond_b: str) -> list[tuple[str, float, float, float]]:
    """For each excluded benchmark, return (bm, gap_a, gap_b, Δ|g| = |a|−|b|)."""
    out = []
    for bm in EXCLUDE_BM:
        sub = df_long[df_long.benchmark == bm]
        if sub.empty:
            continue
        g_run = sub.groupby(["condition", "seed"])["clean_gap"].mean().reset_index()
        means = g_run.groupby("condition")["clean_gap"].mean().to_dict()
        if cond_a in means and cond_b in means:
            out.append((bm, means[cond_a], means[cond_b], abs(means[cond_a]) - abs(means[cond_b])))
    return out


def plot_llm_bars(df_long: pd.DataFrame, out_path: str, title_suffix: str = "",
                  delta_mode: str = "signed"):
    """delta_mode: 'signed' (default) → Δg = private − public (direction of shift);
                   'abs' → Δ|g| = |public|−|private| (compression of misalignment magnitude)."""
    sub = df_long[df_long.condition.isin(["public_only", "private_only"])]
    sub = sub[~sub["benchmark"].isin(EXCLUDE_BM)]
    agg = _agg_per_condition(sub)

    order_map = agg[agg.condition == "public_only"].set_index("benchmark")["mean"]
    bm_sorted = (order_map.reindex([b for b in _bm_keep() if b in agg.benchmark.values])
                          .dropna().sort_values(ascending=False).index.tolist())

    fig, ax = plt.subplots(figsize=(10, 6.5))
    y_pos = np.arange(len(bm_sorted))
    width = 0.36

    for i, bm in enumerate(bm_sorted):
        b = agg[(agg.benchmark == bm) & (agg.condition == "public_only")]
        p = agg[(agg.benchmark == bm) & (agg.condition == "private_only")]
        if not len(b) or not len(p):
            continue
        bm_mean, bm_ci = float(b["mean"].iloc[0]), float(b["ci"].iloc[0])
        pm_mean, pm_ci = float(p["mean"].iloc[0]), float(p["ci"].iloc[0])
        ax.barh(i - width/2, bm_mean, width, xerr=bm_ci,
                color=PUB_BAR_COLOR, edgecolor="black", linewidth=0.4, capsize=2, zorder=3)
        ax.barh(i + width/2, pm_mean, width, xerr=pm_ci,
                color=PR_BAR_COLOR, edgecolor="black", linewidth=0.4, capsize=2, zorder=3)
        if delta_mode == "signed":
            delta = pm_mean - bm_mean
            label = f"Δg={delta:+.3f}"
        else:
            delta = abs(bm_mean) - abs(pm_mean)
            label = f"Δ|g|={delta:+.3f}"
        ax.text(max(bm_mean, pm_mean) + max(bm_ci, pm_ci) + 0.003, i,
                label, fontsize=7.5, va="center", color="#555")

    ax.axvline(0, color="black", lw=1.2, alpha=0.7)
    ax.set_yticks(y_pos); ax.set_yticklabels(bm_sorted)
    ax.invert_yaxis()
    ax.set_xlabel("Per-benchmark clean gap  (score − matched satisfaction)")

    n_pub = sub[sub.condition == "public_only"]["seed"].nunique()
    n_pr = sub[sub.condition == "private_only"]["seed"].nunique()
    legend_elems = [
        plt.Rectangle((0, 0), 1, 1, facecolor=PUB_BAR_COLOR, edgecolor="black",
                      label=f"public_only (n={n_pub})"),
        plt.Rectangle((0, 0), 1, 1, facecolor=PR_BAR_COLOR, edgecolor="black",
                      label=f"private_only (n={n_pr})"),
    ]
    ax.legend(handles=legend_elems, loc="lower right", bbox_to_anchor=(1.0, 0.08),
              frameon=True, fontsize=9)

    if delta_mode == "signed":
        subtitle = "Δg = private_only gap − public_only gap   (Δg < 0 = privacy compresses gap)"
    else:
        subtitle = "Δ|g| = |public_only gap| − |private_only gap|   (Δ|g| > 0 = privacy compresses gap)"
    ax.set_title(
        f"Private benchmarks (generally) reduce satisfaction gaps — LLM runs\n{subtitle}",
        loc="left", fontsize=11)

    # Excluded-benchmarks callout: placed above legend (inside axes, lower-right area).
    # Split each benchmark across two lines to keep the block narrow; aim for 5 lines total.
    excl = _excluded_deltas(df_long, "public_only", "private_only")
    if excl:
        delta_label = "Δg" if delta_mode == "signed" else "Δ|g|"
        lines = ["Excluded (underpromise side):"]
        for bm, g_pub, g_priv, d_abs in excl:
            d = (g_priv - g_pub) if delta_mode == "signed" else d_abs
            lines.append(f"  {bm}")
            lines.append(f"    pub g={g_pub:+.3f}  priv g={g_priv:+.3f}  {delta_label}={d:+.3f}")
        # Anchor just above the legend (legend is loc='lower right'). Right-aligned, bottom-
        # anchored so the block grows upward from the anchor point.
        ax.text(0.985, 0.22, "\n".join(lines),
                transform=ax.transAxes, fontsize=7.5, color="#555", style="italic",
                family="monospace", va="bottom", ha="right", zorder=5,
                bbox=dict(facecolor="white", edgecolor="#ccc", linewidth=0.5, alpha=0.95, pad=3))
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out_path}")


# ─────────── Plot B: per-condition gap decomposition (alignment / population / externality) ───────────

def _decompose_run(jsonl_path: str, exclude_bm: list[str]) -> dict | None:
    """Compute per-provider (score, matched_sat_mean, base_sat, provider_sat) + market share
    at end-of-run. Returns None if required data missing.

    matched_sat_mean is averaged across non-excluded benchmarks (per-benchmark matched_sat
    from per_benchmark_from_jsonl, averaged across benchmarks for each provider).
    """
    with open(jsonl_path) as f:
        rounds = [json.loads(l) for l in f if l.strip()]
    if not rounds:
        return None
    last = rounds[-1]
    # Per-benchmark matched_sat + score per provider
    per_bm = per_benchmark_from_jsonl(jsonl_path)
    per_bm = per_bm[~per_bm["benchmark"].isin(exclude_bm)]
    agg_p = per_bm.groupby("provider").agg(
        score_mean=("score", "mean"),
        matched_mean=("clean_matched", "mean"),
    ).reset_index()

    pb = last["consumer_data"]["penalty_breakdown"]
    ps = last["consumer_data"]["provider_satisfaction"]
    ms = last["consumer_data"]["market_shares"]

    rows = []
    for _, row in agg_p.iterrows():
        p = row["provider"]
        if p not in pb or p not in ps or p not in ms:
            continue
        rows.append({
            "provider": p,
            "score": row["score_mean"],
            "matched_sat": row["matched_mean"],
            "base_sat": pb[p]["base_satisfaction"],
            "provider_sat": ps[p],
            "incident_penalty": pb[p]["incident_penalty"],
            "cost_bonus": pb[p]["cost_bonus"],
            "market_share": ms[p],
        })
    return pd.DataFrame(rows)


def build_decomposition_df(batch: str, model_filter: str | None) -> pd.DataFrame:
    """For each (condition, seed) run: market-share-weighted A/B/C gap components."""
    rows = []
    for cond, seed, model, jsonl in discover_runs(batch, model_filter):
        df = _decompose_run(jsonl, EXCLUDE_BM)
        if df is None or df.empty:
            continue
        w = df["market_share"].values
        if w.sum() == 0:
            continue
        def wmean(v):
            return float(np.average(df[v].values, weights=w))
        rows.append({
            "condition": cond, "seed": seed, "model": model,
            "score":         wmean("score"),
            "matched_sat":   wmean("matched_sat"),
            "base_sat":      wmean("base_sat"),
            "provider_sat":  wmean("provider_sat"),
            "A_alignment":   wmean("score") - wmean("matched_sat"),
            "B_population":  wmean("matched_sat") - wmean("base_sat"),
            "C_externality": wmean("base_sat") - wmean("provider_sat"),
        })
    return pd.DataFrame(rows)


def plot_gap_decomposition(batch: str, model_filter: str | None,
                           out_path: str, title_suffix: str = ""):
    """Stacked horizontal bars: one per privacy condition, showing A/B/C contributions
    to total score-satisfaction divergence."""
    dec = build_decomposition_df(batch, model_filter)
    if dec.empty:
        print(f"SKIP decomposition — no runs found for batch={batch}, model={model_filter}")
        return

    # Aggregate across seeds per condition
    agg = dec.groupby("condition").agg(
        A_mean=("A_alignment", "mean"),   A_sd=("A_alignment", "std"),
        B_mean=("B_population", "mean"),  B_sd=("B_population", "std"),
        C_mean=("C_externality", "mean"), C_sd=("C_externality", "std"),
        total_mean=("A_alignment", lambda s: (dec.loc[s.index, "A_alignment"] +
                                              dec.loc[s.index, "B_population"] +
                                              dec.loc[s.index, "C_externality"]).mean()),
        n=("seed", "nunique"),
    ).reindex(PRIV_ORDER)

    fig, ax = plt.subplots(figsize=(10.5, 4.5))

    y_pos = np.arange(len(PRIV_ORDER))
    comp_colors = {
        "A_alignment":    "#d62728",  # alignment loss — red (publishing side)
        "B_population":   "#9467bd",  # population mix — purple
        "C_externality":  "#2ca02c",  # externality — green (incidents/cost)
    }
    comp_labels = {
        "A_alignment":    "A. Alignment (score − matched_sat): benchmark cdw vs ideal-match need vector",
        "B_population":   "B. Population (matched_sat − base_sat): ideal-match vs actual consumer mix",
        "C_externality": "C. Externality (base_sat − provider_sat): incident penalty − cost bonus",
    }

    # Two stacked passes: positive segments right of 0, negative segments left of 0
    running_pos = np.zeros(len(PRIV_ORDER))
    running_neg = np.zeros(len(PRIV_ORDER))
    for comp in ["A_alignment", "B_population", "C_externality"]:
        means = agg[f"{comp.replace('_mean','_')}mean" if False else f"{comp[0]}_mean"].values
        # cleaner: explicit mapping
        key_map = {"A_alignment": "A_mean", "B_population": "B_mean", "C_externality": "C_mean"}
        means = agg[key_map[comp]].values

        pos = np.where(means > 0, means, 0.0)
        neg = np.where(means < 0, means, 0.0)
        ax.barh(y_pos, pos, left=running_pos, color=comp_colors[comp],
                edgecolor="black", linewidth=0.4, label=comp_labels[comp], zorder=3)
        ax.barh(y_pos, neg, left=running_neg, color=comp_colors[comp],
                edgecolor="black", linewidth=0.4, zorder=3)
        running_pos += pos
        running_neg += neg

    # Total marker + numeric label
    totals = agg["total_mean"].values
    ax.scatter(totals, y_pos, marker="D", s=40, color="black", zorder=5,
               label="Total = score − provider_sat")
    for i, (t, n) in enumerate(zip(totals, agg["n"].values)):
        ax.text(max(running_pos[i], t) + 0.003, i, f"total={t:+.3f} (n={int(n)})",
                fontsize=8, va="center", color="#333")

    ax.axvline(0, color="black", lw=1.0, alpha=0.7)
    ax.set_yticks(y_pos)
    ax.set_yticklabels([PRIV_ORDER[i] for i in range(len(PRIV_ORDER))])
    ax.invert_yaxis()
    ax.set_xlabel("Gap contribution  (share-weighted across providers, mean across seeds)")
    ax.legend(loc="lower right", fontsize=8, frameon=True, framealpha=0.9)
    ax.set_title(
        f"Score–satisfaction divergence decomposed — LLM runs  ({title_suffix})\n"
        f"Total = A + B + C. Excluded from A: {', '.join(EXCLUDE_BM)}",
        loc="left", fontsize=11)
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out_path}")


# ─────────── Plot 3: Heuristic vs LLM baseline vs private_only side-by-side ───────────

def plot_heuristic_vs_llm(df_long_llm: pd.DataFrame, heuristic_csv: str,
                          out_path: str, title_suffix: str = ""):
    """Two-panel paired bars: heuristic aggregate (left) vs LLM aggregate (right).

    Uses public_only vs private_only (clean 100% endpoints) to avoid baseline's
    8/3/2 public-partial-private mix confounding the privacy comparison.
    """
    hdf = pd.read_csv(heuristic_csv)
    sub_h = hdf[(hdf.structural == "none") & (hdf.condition.isin(["public_only", "private_only"]))]
    sub_h = sub_h[~sub_h["benchmark"].isin(EXCLUDE_BM)]
    g_h = sub_h.groupby(["condition", "seed", "benchmark"])["clean_gap"].mean().reset_index()
    heur = g_h.groupby(["benchmark", "condition"])["clean_gap"].agg(
        mean="mean", sd="std", n="count"
    ).reset_index()
    heur["ci"] = np.where(heur["n"] > 1, 1.96 * heur["sd"] / np.sqrt(heur["n"]), 0.0)

    sub_l = df_long_llm[df_long_llm.condition.isin(["public_only", "private_only"])]
    sub_l = sub_l[~sub_l["benchmark"].isin(EXCLUDE_BM)]
    llm = _agg_per_condition(sub_l)

    # Shared benchmark ordering (by heuristic public_only descending)
    order_map = heur[heur.condition == "public_only"].set_index("benchmark")["mean"]
    bm_sorted = (order_map.reindex([b for b in _bm_keep() if b in order_map.index])
                          .dropna().sort_values(ascending=False).index.tolist())

    fig, axes = plt.subplots(1, 2, figsize=(13.0, 4.8), sharey=True,
                             gridspec_kw={"wspace": 0.08})
    y_pos = np.arange(len(bm_sorted))
    width = 0.36

    def _draw(ax, agg, show_err=True):
        for i, bm in enumerate(bm_sorted):
            b = agg[(agg.benchmark == bm) & (agg.condition == "public_only")]
            p = agg[(agg.benchmark == bm) & (agg.condition == "private_only")]
            if not len(b) or not len(p):
                continue
            bm_v = float(b["mean"].iloc[0])
            pm_v = float(p["mean"].iloc[0])
            bm_ci = float(b["ci"].iloc[0]) if show_err else 0.0
            pm_ci = float(p["ci"].iloc[0]) if show_err else 0.0
            ax.barh(i - width/2, bm_v, width, xerr=bm_ci if bm_ci > 0 else None,
                    color=PUB_BAR_COLOR, edgecolor="black", linewidth=0.4,
                    capsize=2, zorder=3)
            ax.barh(i + width/2, pm_v, width, xerr=pm_ci if pm_ci > 0 else None,
                    color=PR_BAR_COLOR, edgecolor="black", linewidth=0.4,
                    capsize=2, zorder=3)
            delta = pm_v - bm_v
            pad = max(bm_ci, pm_ci) + 0.003
            ax.text(max(bm_v, pm_v) + pad, i, f"Δg={delta:+.3f}",
                    fontsize=7.5, va="center", color="#555")
        ax.axvline(0, color="black", lw=1.2, alpha=0.7)
        ax.set_xlabel("Per-benchmark clean gap")
        xmin, xmax = ax.get_xlim()
        ax.set_xlim(xmin, xmax + 0.25 * (xmax - xmin))  # room for Δ|g| labels

    _draw(axes[0], heur, show_err=True)
    n_h = g_h.groupby("condition")["seed"].nunique().to_dict()
    axes[0].set_title(
        f"Heuristic (N={n_h.get('public_only', 0)})",
        loc="left", fontsize=11, fontweight="bold")
    axes[0].set_yticks(y_pos); axes[0].set_yticklabels(bm_sorted); axes[0].invert_yaxis()

    _draw(axes[1], llm, show_err=True)
    n_lb = int(sub_l[sub_l.condition == "public_only"]["seed"].nunique())
    n_lp = int(sub_l[sub_l.condition == "private_only"]["seed"].nunique())
    axes[1].set_title(
        f"LLM (public N={n_lb}, private N={n_lp})",
        loc="left", fontsize=11, fontweight="bold")

    legend_elems = [
        plt.Rectangle((0, 0), 1, 1, facecolor=PUB_BAR_COLOR, edgecolor="black",
                      label="public_only"),
        plt.Rectangle((0, 0), 1, 1, facecolor=PR_BAR_COLOR, edgecolor="black",
                      label="private_only"),
    ]
    axes[1].legend(handles=legend_elems, loc="lower right", frameon=True, fontsize=9)

    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out_path}")


# ─────────────────────────── CLI ───────────────────────────

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--batch", default="_core_privacy",
                    help="sandbox/experiments/<batch>/ directory holding LLM runs")
    ap.add_argument("--model", default="sonnet", choices=["sonnet", "opus", "all"],
                    help="Filter runs by model suffix (default: sonnet)")
    ap.add_argument("--heuristic-csv", default=None,
                    help="Path to heuristic per_benchmark_long.csv "
                         "(default: sandbox/experiments/heuristic_session49/per_benchmark_long.csv)")
    ap.add_argument("--out-dir", default=None,
                    help="Output directory (default: output/paper/ via _paths.paper_dir())")
    ap.add_argument("--include-excluded", action="store_true",
                    help="Include Agentic Tasks + Function Calling (normally excluded as "
                         "agentic-calibration outliers). Output filenames gain a _withagentic suffix.")
    args = ap.parse_args()

    out_dir = args.out_dir or _paths.paper_dir()
    os.makedirs(out_dir, exist_ok=True)

    global EXCLUDE_BM
    suffix = ""
    if args.include_excluded:
        EXCLUDE_BM = []
        suffix = "_withagentic"

    model_filter = None if args.model == "all" else args.model
    df_long = build_long_df(args.batch, model_filter)
    if df_long.empty:
        print(f"No runs found under sandbox/experiments/{args.batch}/llm/")
        sys.exit(1)

    seed_counts = df_long.groupby("condition")["seed"].nunique().to_dict()
    print(f"Loaded {df_long.shape[0]} rows from {df_long['seed'].nunique()} seeds across "
          f"{df_long['condition'].nunique()} conditions: {seed_counts}")

    tag = f"{args.batch}/{args.model}"
    plot_llm_forest(df_long,
                    os.path.join(out_dir, f"forest_llm_core_privacy{suffix}.png"),
                    title_suffix=tag)
    plot_llm_bars(df_long,
                  os.path.join(out_dir, f"bars_public_vs_private{suffix}.png"),
                  title_suffix=tag, delta_mode="signed")

    heur_csv = args.heuristic_csv or os.path.join(
        _paths.PROJECT_ROOT, "sandbox", "experiments",
        "heuristic_session49", "per_benchmark_long.csv")
    if os.path.exists(heur_csv):
        plot_heuristic_vs_llm(df_long, heur_csv,
                              os.path.join(out_dir, f"heuristic_vs_llm{suffix}.png"),
                              title_suffix=f"heuristic_session49 | LLM {tag}")
    else:
        print(f"SKIP heuristic_vs_llm — missing {heur_csv}")

    # Plot B: per-condition gap decomposition (A/B/C)
    plot_gap_decomposition(args.batch, model_filter,
                           os.path.join(out_dir, f"gap_decomposition{suffix}.png"),
                           title_suffix=tag)


if __name__ == "__main__":
    main()
