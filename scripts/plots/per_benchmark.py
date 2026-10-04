"""Per-benchmark gap analysis — the session-42 narrative figures.

Produces three plots for the per-benchmark × matched-consumer-experience gap:

    1. Single-run dumbbell     "Which benchmarks overpromise?"
    2. Aggregate forest plot   Privacy × per-benchmark gap across heuristic runs.
    3. Heuristic + LLM paired  Side-by-side mode comparison (baseline vs private_only).

Matched satisfaction for benchmark b
    matched_sat_b = Σ_s (align(cdw_b, nw_s) · size_s · cap · nw_s)
                    / Σ_s (align(cdw_b, nw_s) · size_s)
where align = dot product of normalized benchmark-cdw and segment need-weights.
gap_b = score_b − matched_sat_b.

Agentic Tasks is excluded as a calibration outlier (cdw weights agentic 0.75 but
capability is systematically low because no heuristic rule invests there).

CLI:
    python -m scripts.plots.per_benchmark \\
        --heuristic-batch heuristic_apr19_postF1 \\
        --llm-batch llm_apr19_diag \\
        --llm-seed 2026

Inputs:
    - Heuristic long-form gap CSV at
        sandbox/experiments/<heuristic-batch>/per_benchmark_long.csv
      (produced by `extract_per_benchmark` below or its sandbox copy).
    - LLM run dirs at sandbox/experiments/<llm-batch>/llm/<cond>/seeds/seed_<N>/rounds.jsonl
Outputs:
    - output/analysis/per_benchmark_gap/plot1_single_run_dumbbell.png
    - output/analysis/per_benchmark_gap/plot2_aggregate_heuristic_forest.png
    - output/analysis/per_benchmark_gap/plot3_heuristic_plus_llm.png
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import os
import sys
from collections import defaultdict

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Make src importable for USE_CASE_PROFILES
from . import paths as _paths
sys.path.insert(0, os.path.join(_paths.PROJECT_ROOT, "src", "actors"))
from consumer import USE_CASE_PROFILES  # type: ignore  # noqa: E402

DIMS = ["reasoning", "coding", "knowledge", "safety", "communication", "agentic"]
BM_ORDER = [
    "General Capability", "Coding Evaluation", "Safety Evaluation", "Instruction Following",
    "Scientific Reasoning", "Clinical Reasoning", "Adversarial Robustness", "Hard Coding",
    "Agentic Tasks", "Advanced Math", "Function Calling", "Long Context", "Legal Reasoning",
]
EXCLUDE_BM = ["Agentic Tasks", "Function Calling"]
BM_KEEP = [b for b in BM_ORDER if b not in EXCLUDE_BM]

PRIV_ORDER = ["public_only", "baseline", "private_dominant", "private_only", "iid_holdout"]
PRIV_COLORS = {
    # Sequential blue scale: lighter = more public, darker = more private.
    "public_only":      "#c6dbef",
    "baseline":         "#6baed6",
    "private_dominant": "#2171b5",
    "private_only":     "#08306b",
    # iid_holdout sits off the privacy axis (ablation); distinct contrast color.
    "iid_holdout":      "#d94801",
}

plt.rcParams.update({
    "figure.dpi": 110, "savefig.dpi": 150,
    "font.size": 10, "axes.titlesize": 12, "axes.labelsize": 10,
    "xtick.labelsize": 9, "ytick.labelsize": 10, "legend.fontsize": 9,
    "axes.spines.top": False, "axes.spines.right": False,
    "font.family": "DejaVu Sans",
})


# ───────── utilities ─────────

def _vec(d):
    return np.array([d.get(k, 0.0) for k in DIMS], dtype=float)


def _normalize(x):
    s = x.sum()
    return x / s if s > 0 else x


def _parse_cond_struct(dirname):
    if "__" in dirname:
        cond, struct = dirname.split("__", 1)
    else:
        cond, struct = dirname, "none"
    return cond, struct


def per_benchmark_from_rows(rows: list) -> pd.DataFrame:
    """Compute per-benchmark × per-provider gap from a pre-loaded rounds list."""
    last = rows[-1]
    providers = list(last["scores"].keys())
    cdw = {b: _normalize(_vec(last["benchmark_dimension_weights"][b]))
           for b in last["per_benchmark_scores"].keys()}
    cap = {p: _vec(last["capability_vectors"][p]) for p in providers}

    segdata = last["consumer_data"]["segment_data"]
    names = list(segdata.keys())
    nw_mat = np.zeros((len(names), len(DIMS)))
    sizes = np.zeros(len(names))
    for i, n in enumerate(names):
        sd = segdata[n]
        uc = sd.get("use_case")
        nw = USE_CASE_PROFILES.get(uc, {}).get("need_weights")
        nw_mat[i] = _normalize(_vec(nw)) if nw else np.ones(len(DIMS)) / len(DIMS)
        sizes[i] = float(sd.get("market_fraction", 0.0))

    out = []
    for b, cdw_b in cdw.items():
        alignment = nw_mat @ cdw_b
        weights = alignment * sizes
        denom = weights.sum()
        if denom <= 0:
            continue
        for p in providers:
            if p not in cap:
                continue
            base = nw_mat @ cap[p]
            matched = float(np.sum(base * weights) / denom)
            score = float(last["per_benchmark_scores"][b].get(p, 0.0))
            out.append({"benchmark": b, "provider": p, "score": score,
                        "clean_matched": matched, "clean_gap": score - matched})
    return pd.DataFrame(out)


def per_benchmark_from_jsonl(path: str) -> pd.DataFrame:
    """Compute per-benchmark × per-provider gap from a rounds.jsonl file."""
    with open(path) as f:
        rows = [json.loads(l) for l in f]
    return per_benchmark_from_rows(rows)


def extract_per_benchmark(batch: str, out_csv: str | None = None) -> str:
    """Walk sandbox/experiments/<batch>/heuristic/*/seeds/seed_*/ and write a
    long-form CSV of per-benchmark gaps. Reusable across any heuristic batch.
    """
    root = _paths.sandbox_run_dir(batch, "heuristic")
    dirs = sorted(glob.glob(os.path.join(root, "*", "seeds", "seed_*")))
    if not dirs:
        raise FileNotFoundError(f"No run dirs under {root}")
    out_csv = out_csv or _paths.sandbox_run_dir(batch, "per_benchmark_long.csv")
    rows_out = []

    for run_dir in dirs:
        parts = run_dir.replace("\\", "/").split("/")
        seed = int(parts[-1].replace("seed_", ""))
        cond, struct = _parse_cond_struct(parts[-3])
        jsonl = os.path.join(run_dir, "rounds.jsonl")
        if not os.path.exists(jsonl):
            continue
        try:
            df = per_benchmark_from_jsonl(jsonl)
        except Exception as e:
            print(f"ERROR {run_dir}: {e}")
            continue
        for _, r in df.iterrows():
            rows_out.append({
                "condition": cond, "structural": struct, "seed": seed,
                "benchmark": r["benchmark"], "provider": r["provider"],
                "score": r["score"], "clean_matched": r["clean_matched"],
                "clean_gap": r["clean_gap"],
            })

    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
        w.writeheader()
        w.writerows(rows_out)
    print(f"Wrote {out_csv}: {len(rows_out)} rows from {len(dirs)} runs")
    return out_csv


def _ci95(x):
    x = np.asarray(x)
    return 1.96 * x.std(ddof=1) / np.sqrt(len(x)) if len(x) > 1 else 0.0


# ───────── Plot 1: single-run dumbbell ─────────

def plot_single_run_dumbbell(jsonl_path: str, out_path: str, title_suffix: str = ""):
    """File-path variant. See `dumbbell_from_df` if you already have the DataFrame."""
    df = per_benchmark_from_jsonl(jsonl_path)
    dumbbell_from_df(df, out_path, title_suffix=title_suffix)


def dumbbell_from_df(df: pd.DataFrame, out_path: str, title_suffix: str = "",
                     ax: "plt.Axes | None" = None):
    """Render dumbbell on a given Axes (or new figure if ax=None) from a pre-computed
    per-benchmark × per-provider gap DataFrame (columns: benchmark, score, clean_matched, clean_gap).
    """
    df = df[~df["benchmark"].isin(EXCLUDE_BM)]
    g = df.groupby("benchmark").agg(
        score=("score", "mean"),
        matched=("clean_matched", "mean"),
        gap=("clean_gap", "mean"),
    ).reset_index().sort_values("gap", ascending=False).reset_index(drop=True)

    created_fig = ax is None
    if created_fig:
        fig, ax = plt.subplots(figsize=(10, 5.5))
    y_pos = np.arange(len(g))
    for i, row in g.iterrows():
        color = "#C62828" if row.gap > 0 else "#1565C0"
        ax.plot([row.matched, row.score], [i, i], color=color, lw=3, zorder=1, alpha=0.65)
        ax.scatter(row.matched, i, color="#6a6a6a", s=85, zorder=3,
                   label="matched satisfaction" if i == 0 else None,
                   edgecolor="black", linewidth=0.8)
        ax.scatter(row.score, i, color=color, s=110, zorder=3,
                   label="benchmark score" if i == 0 else None,
                   edgecolor="black", linewidth=0.8)
        mid_x = (row.score + row.matched) / 2
        ax.text(mid_x, i - 0.28, f"{row.gap:+.3f}", ha="center", va="top",
                fontsize=8, color=color, weight="bold")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(g["benchmark"])
    ax.invert_yaxis()
    ax.set_xlabel("Value (score or matched satisfaction)")
    ax.axvline(g["matched"].mean(), color="gray", ls="--", lw=0.7, alpha=0.4)
    ax.legend(loc="lower right", frameon=False)

    n_pos = int((g.gap > 0).sum())
    ax.set_title(
        f"Which benchmarks overpromise what consumers experience?\n"
        f"{title_suffix or 'single run'} — "
        f"{n_pos}/{len(g)} benchmarks score > matched satisfaction (red)",
        loc="left")
    ax.text(0.01, -0.19,
            "matched satisfaction = capability · consumer-need-weights, weighted by segment alignment to the benchmark's dimension weights\n"
            f"excluded: {', '.join(EXCLUDE_BM)} (calibration outlier — benchmark weights one dimension where capability is systematically low)",
            transform=ax.transAxes, fontsize=7.5, color="#444", style="italic")

    if created_fig:
        fig = ax.figure
        fig.tight_layout()
        if out_path:
            fig.savefig(out_path)
            plt.close(fig)
            print(f"Saved {out_path}")


# ───────── Plot 2: aggregate heuristic forest ─────────

def plot_aggregate_heuristic_forest(long_csv: str, out_path: str, title_suffix: str = ""):
    df = pd.read_csv(long_csv)
    sub = df[df.structural == "none"]
    g_run = sub.groupby(["condition", "seed", "benchmark"])["clean_gap"].mean().reset_index()
    agg = g_run.groupby(["benchmark", "condition"])["clean_gap"].agg(
        mean="mean", sd="std", n="count"
    ).reset_index()
    agg["ci"] = 1.96 * agg["sd"] / np.sqrt(agg["n"])
    # Pooled gap of excluded benchmarks (across all 5 privacy conditions) for caption.
    excluded_stats = {
        bm: float(g_run[g_run.benchmark == bm]["clean_gap"].mean())
        for bm in EXCLUDE_BM
        if bm in set(g_run.benchmark)
    }
    agg = agg[~agg["benchmark"].isin(EXCLUDE_BM)]

    order_df = agg[agg.condition == "public_only"].set_index("benchmark")["mean"].reindex(BM_KEEP)
    bm_sorted = order_df.sort_values(ascending=False).index.tolist()

    fig, ax = plt.subplots(figsize=(11, 6))
    y_pos = np.arange(len(bm_sorted))
    dodge = np.linspace(-0.28, 0.28, len(PRIV_ORDER))

    for i, cond in enumerate(PRIV_ORDER):
        ys, xs, cis = [], [], []
        for bm in bm_sorted:
            row = agg[(agg.benchmark == bm) & (agg.condition == cond)]
            if len(row):
                xs.append(float(row["mean"].iloc[0]))
                cis.append(float(row["ci"].iloc[0]))
                ys.append(y_pos[bm_sorted.index(bm)] + dodge[i])
            else:
                xs.append(np.nan); cis.append(0); ys.append(np.nan)
        ax.errorbar(xs, ys, xerr=cis, fmt="o", markersize=6,
                    color=PRIV_COLORS[cond], label=cond,
                    capsize=3, lw=1.2, elinewidth=1.0,
                    markeredgecolor="black", markeredgewidth=0.4)

    ax.axvline(0, color="black", lw=1, alpha=0.6)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(bm_sorted)
    ax.invert_yaxis()
    ax.set_xlabel("Per-benchmark clean gap  (score − matched satisfaction)")
    ax.legend(title="privacy condition", loc="lower right", frameon=True, framealpha=0.9)
    ax.text(0.02, 0.96, "← benchmark underpromises",
            transform=ax.transAxes, fontsize=9, color="#1565C0", alpha=0.8)
    ax.text(0.98, 0.96, "benchmark overpromises →",
            transform=ax.transAxes, fontsize=9, color="#C62828", alpha=0.8, ha="right")
    excl_str = ", ".join(f"{bm} (pooled g={excluded_stats[bm]:+.3f})"
                         for bm in EXCLUDE_BM if bm in excluded_stats)
    ax.set_title(
        "Privacy conditions compress per-benchmark gap toward zero\n"
        f"{title_suffix or 'aggregate heuristic'} (struct=none, 5 privacy × seeds × providers)"
        f"\nexcluded as agentic-calibration outliers: {excl_str}",
        loc="left")
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)
    print(f"Saved {out_path}")


# ───────── Plot 3: heuristic + LLM paired ─────────

def plot_heuristic_plus_llm(long_csv: str, llm_batch: str, llm_seed: int,
                            out_path: str, title_suffix: str = ""):
    df = pd.read_csv(long_csv)
    sub = df[(df.structural == "none") & (df.condition.isin(["baseline", "private_only"]))]
    sub = sub[~sub["benchmark"].isin(EXCLUDE_BM)]
    g_run = sub.groupby(["condition", "seed", "benchmark"])["clean_gap"].mean().reset_index()
    heur = g_run.groupby(["benchmark", "condition"])["clean_gap"].agg(
        mean="mean", sd="std", n="count"
    ).reset_index()
    heur["ci"] = 1.96 * heur["sd"] / np.sqrt(heur["n"])

    def _llm_gap(cond_dir):
        path = _paths.sandbox_run_dir(
            llm_batch, "llm", cond_dir, "seeds", f"seed_{llm_seed}", "rounds.jsonl"
        )
        if not os.path.exists(path):
            return None
        return per_benchmark_from_jsonl(path).groupby("benchmark")["clean_gap"].mean()

    llm_bl = _llm_gap("baseline")
    llm_pr = _llm_gap("private_only")
    if llm_bl is None or llm_pr is None:
        raise FileNotFoundError(f"LLM baseline or private_only run missing under batch={llm_batch}")

    fp_path = _paths.sandbox_run_dir(
        llm_batch, "llm", "fixed_public", "seeds", f"seed_{llm_seed}", "rounds.jsonl"
    )
    include_fp = False
    llm_fp = None
    if os.path.exists(fp_path):
        with open(fp_path) as f:
            if sum(1 for _ in f) >= 30:
                llm_fp = per_benchmark_from_jsonl(fp_path).groupby("benchmark")["clean_gap"].mean()
                include_fp = True

    order_map = heur[heur.condition == "baseline"].set_index("benchmark")["mean"]
    bm_sorted = order_map.reindex(BM_KEEP).sort_values(ascending=False).index.tolist()

    fig, axes = plt.subplots(1, 2, figsize=(13, 6.5), sharey=True,
                             gridspec_kw={"wspace": 0.08})
    y_pos = np.arange(len(bm_sorted))
    width = 0.36
    BL_COLOR, PR_COLOR = "#455A64", "#2E7D32"

    # Panel A: heuristic
    ax = axes[0]
    for i, bm in enumerate(bm_sorted):
        b = heur[(heur.benchmark == bm) & (heur.condition == "baseline")]
        p = heur[(heur.benchmark == bm) & (heur.condition == "private_only")]
        if not len(b) or not len(p):
            continue
        bm_mean, bm_ci = float(b["mean"].iloc[0]), float(b["ci"].iloc[0])
        pm_mean, pm_ci = float(p["mean"].iloc[0]), float(p["ci"].iloc[0])
        ax.barh(i - width/2, bm_mean, width, xerr=bm_ci, color=BL_COLOR,
                edgecolor="black", linewidth=0.4, capsize=2, zorder=3)
        ax.barh(i + width/2, pm_mean, width, xerr=pm_ci, color=PR_COLOR,
                edgecolor="black", linewidth=0.4, capsize=2, zorder=3)
        delta = abs(bm_mean) - abs(pm_mean)
        ax.text(max(bm_mean, pm_mean) + max(bm_ci, pm_ci) + 0.004, i,
                f"Δ|g|={delta:+.3f}",
                fontsize=7.5, va="center", color="#555")
    ax.axvline(0, color="black", lw=1.2, alpha=0.7)
    ax.set_yticks(y_pos); ax.set_yticklabels(bm_sorted); ax.invert_yaxis()
    ax.set_xlabel("Per-benchmark clean gap")
    ax.set_title("Heuristic (aggregate)\n30 seeds × providers per bar; error bars = 95% CI",
                 loc="left", fontsize=11)

    # Panel B: LLM
    ax = axes[1]
    for i, bm in enumerate(bm_sorted):
        if bm not in llm_bl.index or bm not in llm_pr.index:
            continue
        bm_v, pm_v = float(llm_bl[bm]), float(llm_pr[bm])
        ax.barh(i - width/2, bm_v, width, color=BL_COLOR, edgecolor="black",
                linewidth=0.4, zorder=3)
        ax.barh(i + width/2, pm_v, width, color=PR_COLOR, edgecolor="black",
                linewidth=0.4, zorder=3)
        delta = abs(bm_v) - abs(pm_v)
        ax.text(max(bm_v, pm_v) + 0.004, i, f"Δ|g|={delta:+.3f}",
                fontsize=7.5, va="center", color="#555")
        if include_fp and llm_fp is not None and bm in llm_fp.index:
            fv = float(llm_fp[bm])
            ax.scatter(fv, i + width/2 + 0.05, marker="v", s=45,
                       color="#FF6F00", edgecolor="black", linewidth=0.5, zorder=5)

    ax.axvline(0, color="black", lw=1.2, alpha=0.7)
    fp_note = " | ▼ = fixed_public (static pool)" if include_fp else ""
    ax.set_title(f"LLM (seed {llm_seed}){fp_note}", loc="left", fontsize=11)
    ax.set_xlabel("Per-benchmark clean gap")

    legend_elems = [
        plt.Rectangle((0, 0), 1, 1, facecolor=BL_COLOR, edgecolor="black", label="baseline"),
        plt.Rectangle((0, 0), 1, 1, facecolor=PR_COLOR, edgecolor="black", label="private_only"),
    ]
    if include_fp:
        legend_elems.append(Line2D([0], [0], marker="v", color="w",
                                   markerfacecolor="#FF6F00", markeredgecolor="black",
                                   markersize=9, label="fixed_public (LLM)"))
    axes[1].legend(handles=legend_elems, loc="lower right", frameon=True, fontsize=9)

    fig.suptitle(
        "Privacy compresses per-benchmark gap — heuristic and LLM agree on direction\n"
        f"Δ|g| = |baseline gap| − |private_only gap| (positive = privacy helped). "
        f"Excluded: {', '.join(EXCLUDE_BM)}.{' — ' + title_suffix if title_suffix else ''}",
        fontsize=12, y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(out_path)
    plt.close(fig)
    print(f"Saved {out_path}")


# ───────── walk-all-runs: Plot 1 per LLM run in sandbox/experiments ─────────

def _discover_llm_runs():
    """Return (jsonl_path, batch, condition, seed_label) tuples for every LLM run
    under sandbox/experiments. Handles both layouts:
        sandbox/experiments/<batch>/llm/<cond>/seeds/seed_<N>/rounds.jsonl
        sandbox/experiments/llm/<cond>/seeds/seed_<N>/rounds.jsonl   (batch literally "llm")
    """
    root = os.path.join(_paths.PROJECT_ROOT, "sandbox", "experiments")
    patterns = [
        os.path.join(root, "*", "llm", "*", "seeds", "seed_*", "rounds.jsonl"),
        os.path.join(root, "llm", "*", "seeds", "seed_*", "rounds.jsonl"),
    ]
    seen = set()
    out = []
    for pat in patterns:
        for p in glob.glob(pat):
            norm = os.path.normpath(p)
            if norm in seen:
                continue
            seen.add(norm)
            parts = norm.replace("\\", "/").split("/")
            try:
                i = len(parts) - 1 - parts[::-1].index("llm")
            except ValueError:
                continue
            if i == 0 or parts[i - 1] != "experiments":
                batch = parts[i - 1]
            else:
                batch = "llm"
            cond = parts[i + 1]
            seed_label = parts[-2]
            out.append((norm, batch, cond, seed_label))
    return sorted(out)


def plot_all_llm_runs(out_dir: str):
    """Emit one Plot 1 (single-run dumbbell) per LLM run found in sandbox/experiments."""
    runs = _discover_llm_runs()
    if not runs:
        print("No LLM runs found under sandbox/experiments/**/llm/*/seeds/seed_*/")
        return
    os.makedirs(out_dir, exist_ok=True)
    ok = 0
    for jsonl, batch, cond, seed_label in runs:
        fname = f"{batch}__{cond}__{seed_label}.png"
        out_path = os.path.join(out_dir, fname)
        try:
            plot_single_run_dumbbell(
                jsonl, out_path,
                title_suffix=f"{batch} / {cond} / {seed_label}",
            )
            ok += 1
        except Exception as e:
            print(f"ERROR {jsonl}: {e}")
    print(f"Plot 1 per-run: wrote {ok}/{len(runs)} plots to {out_dir}")


# ───────── CLI ─────────

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--heuristic-batch", default="heuristic_apr19_postF1",
                    help="sandbox/experiments/<batch>/ directory holding heuristic runs")
    ap.add_argument("--llm-batch", default="llm_apr19_diag",
                    help="sandbox/experiments/<batch>/ directory holding LLM runs")
    ap.add_argument("--llm-seed", type=int, default=2026,
                    help="LLM seed to use for Plot 1 and Plot 3")
    ap.add_argument("--llm-condition", default="baseline",
                    help="condition name under <llm-batch>/llm/ for the Plot 1 single-run dumbbell")
    ap.add_argument("--rebuild-csv", action="store_true",
                    help="rebuild per_benchmark_long.csv from the heuristic batch")
    ap.add_argument("--out-subject", default="per_benchmark_gap",
                    help="subject name under output/analysis/")
    ap.add_argument("--all-llm-runs", action="store_true",
                    help="Emit Plot 1 per LLM run under sandbox/experiments/ and exit "
                         "(skips heuristic Plots 2/3).")
    args = ap.parse_args()

    if args.all_llm_runs:
        out_dir = os.path.join(_paths.analysis_dir(args.out_subject), "per_run")
        plot_all_llm_runs(out_dir)
        return

    out_dir = _paths.analysis_dir(args.out_subject)

    csv_path = _paths.sandbox_run_dir(args.heuristic_batch, "per_benchmark_long.csv")
    if args.rebuild_csv or not os.path.exists(csv_path):
        csv_path = extract_per_benchmark(args.heuristic_batch, csv_path)

    # Plot 1: single LLM run (condition-agnostic via --llm-condition)
    bl_jsonl = _paths.sandbox_run_dir(
        args.llm_batch, "llm", args.llm_condition, "seeds", f"seed_{args.llm_seed}", "rounds.jsonl"
    )
    if os.path.exists(bl_jsonl):
        plot_single_run_dumbbell(
            bl_jsonl,
            os.path.join(out_dir, "plot1_single_run_dumbbell.png"),
            title_suffix=f"LLM {args.llm_condition}, seed {args.llm_seed}",
        )
    else:
        print(f"SKIP Plot 1 — missing {bl_jsonl}")

    # Plot 2: aggregate heuristic forest
    plot_aggregate_heuristic_forest(
        csv_path,
        os.path.join(out_dir, "plot2_aggregate_heuristic_forest.png"),
        title_suffix=args.heuristic_batch,
    )

    # Plot 3: heuristic + LLM paired
    try:
        plot_heuristic_plus_llm(
            csv_path, args.llm_batch, args.llm_seed,
            os.path.join(out_dir, "plot3_heuristic_plus_llm.png"),
            title_suffix=f"{args.heuristic_batch} | LLM {args.llm_batch}/seed_{args.llm_seed}",
        )
    except FileNotFoundError as e:
        print(f"SKIP Plot 3 — {e}")


if __name__ == "__main__":
    main()
