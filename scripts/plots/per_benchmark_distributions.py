"""Distributional per-benchmark gap plots for many-LLM-run case.

Three sketches (one panel each, saved as separate PNGs):

    (1) Reliability scatter — score (x) vs matched satisfaction (y), one dot per
        (provider, benchmark, seed, condition, batch). 45° diagonal = perfect
        calibration; below = overpromise, above = underpromise. The most
        opinionated framing: Goodhart IS distance from the diagonal.

    (2) Side-by-side boxes — x=benchmark (ordered by overall median gap),
        y=clean gap, one box per condition dodged within each benchmark group.
        Replaces the forest plot when N per cell > ~15.

    (3) Strip + median — same axes as (2) but every (seed, provider) is a dot
        with a median bar per (benchmark, condition) cell. Honest version for
        small N (5–30) where boxes lie about shape.

CLI:
    python -m scripts.plots.per_benchmark_distributions \\
        [--conditions baseline private_only ...] \\
        [--batches llm_apr19_diag session39_llm_probe ...] \\
        [--out-subject per_benchmark_distributions]

Outputs three PNGs under output/analysis/<subject>/:
    reliability_scatter.png
    boxes_by_benchmark.png
    strip_by_benchmark.png
"""
from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from . import paths as _paths
import glob

from .per_benchmark import (
    _discover_llm_runs,
    per_benchmark_from_jsonl,
    EXCLUDE_BM,
)


def _discover_heuristic_runs():
    """Mirror of `_discover_llm_runs()` for heuristic-mode runs.
    Walks both sandbox layouts:
        sandbox/experiments/<batch>/heuristic/<cond>/seeds/seed_<N>/rounds.jsonl
        sandbox/experiments/heuristic/<cond>/seeds/seed_<N>/rounds.jsonl   (batch="heuristic")
    """
    root = os.path.join(_paths.PROJECT_ROOT, "sandbox", "experiments")
    patterns = [
        os.path.join(root, "*", "heuristic", "*", "seeds", "seed_*", "rounds.jsonl"),
        os.path.join(root, "heuristic", "*", "seeds", "seed_*", "rounds.jsonl"),
    ]
    seen, out = set(), []
    for pat in patterns:
        for p in glob.glob(pat):
            norm = os.path.normpath(p)
            if norm in seen:
                continue
            seen.add(norm)
            parts = norm.replace("\\", "/").split("/")
            try:
                i = len(parts) - 1 - parts[::-1].index("heuristic")
            except ValueError:
                continue
            if i > 0 and parts[i - 1] != "experiments":
                batch = parts[i - 1]
            else:
                batch = "heuristic"
            cond = parts[i + 1]
            seed_label = parts[-2]
            out.append((norm, batch, cond, seed_label))
    return sorted(out)

plt.rcParams.update({
    "figure.dpi": 110, "savefig.dpi": 150,
    "font.size": 10, "axes.titlesize": 12, "axes.labelsize": 10,
    "xtick.labelsize": 9, "ytick.labelsize": 10, "legend.fontsize": 9,
    "axes.spines.top": False, "axes.spines.right": False,
    "font.family": "DejaVu Sans",
})

# Colorblind-friendly 8-way palette (Okabe-Ito extended).
_PALETTE = [
    "#1976D2", "#C62828", "#2E7D32", "#6A1B9A",
    "#EF6C00", "#00838F", "#5D4037", "#AD1457",
]


def _load_benchmark_types(run_dir):
    """Return {benchmark_name: benchmark_type} from config.json next to rounds.jsonl.
    Returns {} if the config is missing or predates session-38 (no benchmark_type field)."""
    import json
    cfg_path = os.path.join(run_dir, "config.json")
    if not os.path.exists(cfg_path):
        return {}
    with open(cfg_path) as f:
        cfg = json.load(f)
    bms = list(cfg.get("benchmarks", [])) + list(cfg.get("benchmark_sequence", []))
    out = {}
    for b in bms:
        name = b.get("name")
        btype = b.get("benchmark_type")
        if name and btype:
            out[name] = btype
    return out


# Fallback type inference for conditions where every benchmark is the same
# type but the config.json predates the `benchmark_type` field (e.g. the
# session-42 `fixed_public` diagnostic).
_HOMOGENEOUS_TYPE_BY_CONDITION = {
    "fixed_public": "public",
    "public_only": "public",
    "private_only": "private",
    "private_dominant": "partial",
    "iid_holdout": "iid_holdout",
}


def build_long_df(runs):
    """runs: iterable of (jsonl_path, batch, condition, seed_label).
    Returns long-form DataFrame with one row per (benchmark, provider).
    Adds `benchmark_type` column from config.json, falling back to a
    condition-name heuristic for homogeneous conditions whose configs
    predate the field."""
    out = []
    for jsonl, batch, cond, seed_label in runs:
        try:
            df = per_benchmark_from_jsonl(jsonl)
        except Exception as e:
            print(f"SKIP {jsonl}: {e}")
            continue
        df = df[~df["benchmark"].isin(EXCLUDE_BM)].copy()
        df["batch"] = batch
        df["condition"] = cond
        df["seed_label"] = seed_label
        type_map = _load_benchmark_types(os.path.dirname(jsonl))
        df["benchmark_type"] = df["benchmark"].map(type_map)
        fallback = _HOMOGENEOUS_TYPE_BY_CONDITION.get(cond)
        if fallback is not None:
            df["benchmark_type"] = df["benchmark_type"].fillna(fallback)
        out.append(df)
    if not out:
        return pd.DataFrame()
    return pd.concat(out, ignore_index=True)


def _filter(df, conditions=None, batches=None):
    if conditions:
        df = df[df["condition"].isin(conditions)]
    if batches:
        df = df[df["batch"].isin(batches)]
    return df


# ───────── Plot 1: reliability scatter ─────────

def plot_reliability_scatter(df, out_path, title_suffix=""):
    """score vs matched, 45° line. Color = benchmark. One dot per
    (benchmark, provider, seed, condition, batch)."""
    bms = sorted(df["benchmark"].unique())
    cmap = {b: _PALETTE[i % len(_PALETTE)] for i, b in enumerate(bms)}

    n_total = len(df)
    s = 22 if n_total < 2000 else 10 if n_total < 20000 else 4
    alpha = 0.55 if n_total < 2000 else 0.30 if n_total < 20000 else 0.15

    fig, ax = plt.subplots(figsize=(7.5, 7.5))
    for b in bms:
        sub = df[df.benchmark == b]
        ax.scatter(sub["score"], sub["clean_matched"],
                   s=s, alpha=alpha, color=cmap[b], edgecolor="none",
                   label=b)

    lo = float(min(df["score"].min(), df["clean_matched"].min()))
    hi = float(max(df["score"].max(), df["clean_matched"].max()))
    pad = 0.02 * (hi - lo)
    ax.plot([lo - pad, hi + pad], [lo - pad, hi + pad],
            color="black", lw=1, ls="--", alpha=0.7, zorder=0, label="perfect calibration")

    ax.set_xlim(lo - pad, hi + pad)
    ax.set_ylim(lo - pad, hi + pad)
    ax.set_aspect("equal")
    ax.set_xlabel("Benchmark score")
    ax.set_ylabel("Matched satisfaction")
    n_over = int((df["clean_gap"] > 0).sum())
    n_tot = len(df)
    ax.set_title(
        f"Reliability scatter — Goodhart = distance below the diagonal\n"
        f"{n_over}/{n_tot} points below (overpromise). {title_suffix}",
        loc="left")
    ax.text(0.02, 0.97,
            "below diagonal → score > satisfaction (overpromise)\n"
            "above diagonal → score < satisfaction (underpromise)",
            transform=ax.transAxes, fontsize=8, color="#444",
            va="top", style="italic")
    ax.legend(loc="lower right", frameon=False, fontsize=8, ncol=2)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)
    print(f"Saved {out_path}")


# ───────── Plot 1b: reliability scatter colored by benchmark type ─────────

_TYPE_COLORS = {
    "public":      "#1976D2",   # blue — freely observable
    "partial":     "#EF6C00",   # orange — partial holdout (h=0.3)
    "private":     "#C62828",   # red   — full holdout (h=1.0)
    "iid_holdout": "#6A1B9A",   # purple — ablation (cosine=1.0)
}
_TYPE_ORDER = ["public", "partial", "private", "iid_holdout"]


def plot_reliability_scatter_by_type(df, out_path, title_suffix=""):
    """Reliability scatter (score vs matched), color = benchmark_type.
    Requires benchmark_type column; rows with None are dropped."""
    d = df.dropna(subset=["benchmark_type"]).copy()
    if d.empty:
        print(f"SKIP reliability-by-type — no rows with benchmark_type (need session-38+ configs)")
        return
    types_present = [t for t in _TYPE_ORDER if t in d["benchmark_type"].unique()]

    n_total = len(d)
    s = 26 if n_total < 2000 else 10 if n_total < 20000 else 4
    alpha = 0.60 if n_total < 2000 else 0.30 if n_total < 20000 else 0.18

    fig, ax = plt.subplots(figsize=(7.5, 7.5))
    for t in types_present:
        sub = d[d.benchmark_type == t]
        n_over = int((sub["clean_gap"] > 0).sum())
        ax.scatter(sub["score"], sub["clean_matched"],
                   s=s, alpha=alpha, color=_TYPE_COLORS[t], edgecolor="none",
                   label=f"{t} (n={len(sub)}, {n_over} overpromise)")

    lo = float(min(d["score"].min(), d["clean_matched"].min()))
    hi = float(max(d["score"].max(), d["clean_matched"].max()))
    pad = 0.02 * (hi - lo)
    ax.plot([lo - pad, hi + pad], [lo - pad, hi + pad],
            color="black", lw=1, ls="--", alpha=0.7, zorder=0, label="perfect calibration")

    ax.set_xlim(lo - pad, hi + pad)
    ax.set_ylim(lo - pad, hi + pad)
    ax.set_aspect("equal")
    ax.set_xlabel("Benchmark score")
    ax.set_ylabel("Matched satisfaction")
    ax.set_title(
        f"Reliability by benchmark type — does privacy pull scores toward the diagonal?\n"
        f"below diagonal = overpromise. {title_suffix}",
        loc="left")
    ax.legend(loc="lower right", frameon=True, framealpha=0.9, fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)
    print(f"Saved {out_path}")


# ───────── Plot 2: side-by-side boxes by benchmark, dodged by condition ─────────

def _order_benchmarks_by_gap(df):
    """Order benchmarks by overall median gap (descending — worst overpromise first)."""
    med = df.groupby("benchmark")["clean_gap"].median().sort_values(ascending=False)
    return med.index.tolist()


def plot_boxes_by_benchmark(df, out_path, title_suffix=""):
    bms = _order_benchmarks_by_gap(df)
    conds = sorted(df["condition"].unique())
    cmap = {c: _PALETTE[i % len(_PALETTE)] for i, c in enumerate(conds)}

    group_width = 0.82
    box_width = group_width / max(len(conds), 1)
    offsets = (np.arange(len(conds)) - (len(conds) - 1) / 2) * box_width

    fig, ax = plt.subplots(figsize=(max(9, 1.0 * len(bms)), 5.2))
    for i, cond in enumerate(conds):
        data, positions = [], []
        for j, bm in enumerate(bms):
            vals = df[(df.benchmark == bm) & (df.condition == cond)]["clean_gap"].values
            if len(vals) == 0:
                continue
            data.append(vals)
            positions.append(j + offsets[i])
        if not data:
            continue
        bp = ax.boxplot(
            data, positions=positions, widths=box_width * 0.85,
            patch_artist=True, showfliers=True,
            medianprops=dict(color="black", lw=1.2),
            flierprops=dict(marker="o", markersize=3, markerfacecolor=cmap[cond],
                            markeredgecolor="none", alpha=0.6),
            boxprops=dict(facecolor=cmap[cond], alpha=0.55, edgecolor="black", lw=0.6),
            whiskerprops=dict(color="black", lw=0.8),
            capprops=dict(color="black", lw=0.8),
        )

    ax.axhline(0, color="black", lw=1, alpha=0.6)
    ax.set_xticks(np.arange(len(bms)))
    ax.set_xticklabels(bms, rotation=25, ha="right")
    ax.set_ylabel("Per-benchmark clean gap (score − matched satisfaction)")
    ax.set_title(
        f"Per-benchmark gap distribution across runs — boxes per condition\n"
        f"benchmarks ordered by overall median gap, N per cell shown below. {title_suffix}",
        loc="left")

    # N annotations beneath each benchmark group
    ymin = df["clean_gap"].min()
    y_ann = ymin - 0.015 * (df["clean_gap"].max() - ymin + 1e-9)
    for j, bm in enumerate(bms):
        n = len(df[df.benchmark == bm])
        ax.text(j, y_ann, f"n={n}", ha="center", va="top", fontsize=7, color="#666")

    legend_handles = [plt.Rectangle((0, 0), 1, 1, facecolor=cmap[c], alpha=0.55,
                                    edgecolor="black", label=c) for c in conds]
    ax.legend(handles=legend_handles, title="condition", loc="upper right",
              frameon=True, framealpha=0.9, fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)
    print(f"Saved {out_path}")


# ───────── Plot 3: strip + median bar ─────────

def plot_strip_by_benchmark(df, out_path, title_suffix=""):
    """Every (provider, seed) a dot; short horizontal bar at the median per
    (benchmark, condition) cell. Exposes shape where boxes would smooth."""
    bms = _order_benchmarks_by_gap(df)
    conds = sorted(df["condition"].unique())
    cmap = {c: _PALETTE[i % len(_PALETTE)] for i, c in enumerate(conds)}

    group_width = 0.82
    slot_width = group_width / max(len(conds), 1)
    offsets = (np.arange(len(conds)) - (len(conds) - 1) / 2) * slot_width
    jitter = slot_width * 0.30
    rng = np.random.default_rng(0)

    fig, ax = plt.subplots(figsize=(max(9, 1.0 * len(bms)), 5.2))
    for i, cond in enumerate(conds):
        for j, bm in enumerate(bms):
            vals = df[(df.benchmark == bm) & (df.condition == cond)]["clean_gap"].values
            if len(vals) == 0:
                continue
            x_center = j + offsets[i]
            xs = x_center + rng.uniform(-jitter, jitter, size=len(vals))
            ax.scatter(xs, vals, s=18, alpha=0.55, color=cmap[cond], edgecolor="none")
            med = float(np.median(vals))
            ax.hlines(med, x_center - slot_width * 0.40, x_center + slot_width * 0.40,
                      color="black", lw=1.6, zorder=4)

    ax.axhline(0, color="black", lw=1, alpha=0.6)
    ax.set_xticks(np.arange(len(bms)))
    ax.set_xticklabels(bms, rotation=25, ha="right")
    ax.set_ylabel("Per-benchmark clean gap (score − matched satisfaction)")
    ax.set_title(
        f"Per-benchmark gap — every run a dot, bar = median\n"
        f"honest for small N; bimodality / outlier-driven cells become visible. {title_suffix}",
        loc="left")

    legend_handles = [plt.Line2D([0], [0], marker="o", linestyle="",
                                 markerfacecolor=cmap[c], markeredgecolor="none",
                                 alpha=0.7, markersize=7, label=c)
                      for c in conds]
    legend_handles.append(plt.Line2D([0], [0], color="black", lw=1.6, label="median"))
    ax.legend(handles=legend_handles, title="condition", loc="upper right",
              frameon=True, framealpha=0.9, fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)
    print(f"Saved {out_path}")


# ───────── CLI ─────────

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--conditions", nargs="*", default=None,
                    help="only include these condition names (default: all found)")
    ap.add_argument("--batches", nargs="*", default=None,
                    help="only include these batch names (default: all found)")
    ap.add_argument("--out-subject", default=None,
                    help="subject name under output/analysis/ "
                         "(default: per_benchmark_distributions_<mode>)")
    ap.add_argument("--mode", choices=["llm", "heuristic"], default="llm",
                    help="which mode's runs to plot (discovery path differs)")
    ap.add_argument("--recent-only", action="store_true",
                    help="drop runs whose config.json lacks benchmark_type "
                         "(i.e., keep only session-38+ runs — currently Apr-18+ batches).")
    args = ap.parse_args()

    if args.mode == "heuristic":
        runs = _discover_heuristic_runs()
    else:
        runs = _discover_llm_runs()
    df = build_long_df(runs)
    if df.empty:
        print("No LLM run data found.")
        return
    df = _filter(df, conditions=args.conditions, batches=args.batches)
    if args.recent_only:
        df = df.dropna(subset=["benchmark_type"])
    if df.empty:
        print(f"No runs after filter: conditions={args.conditions} batches={args.batches} "
              f"recent_only={args.recent_only}")
        return

    subject = args.out_subject or f"per_benchmark_distributions_{args.mode}"
    out_dir = _paths.analysis_dir(subject)

    # Summary: runs per (batch, condition)
    summary = df.groupby(["batch", "condition"])["seed_label"].nunique().reset_index()
    summary.columns = ["batch", "condition", "n_seeds"]
    print("Run summary:")
    for _, r in summary.iterrows():
        print(f"  {r.batch:30s}  {r.condition:40s}  n_seeds={r.n_seeds}")
    print(f"Total rows (benchmark×provider×seed×condition): {len(df)}")

    suffix = f"{len(df)} (bm×prov×seed) rows across {df['condition'].nunique()} conditions"
    plot_reliability_scatter(df, os.path.join(out_dir, "reliability_scatter.png"),
                             title_suffix=suffix)
    plot_reliability_scatter_by_type(
        df, os.path.join(out_dir, "reliability_scatter_by_type.png"),
        title_suffix=suffix)
    plot_boxes_by_benchmark(df, os.path.join(out_dir, "boxes_by_benchmark.png"),
                            title_suffix=suffix)
    plot_strip_by_benchmark(df, os.path.join(out_dir, "strip_by_benchmark.png"),
                            title_suffix=suffix)


if __name__ == "__main__":
    main()
