"""Privacy-gap two-panel figure for paper §5 (Figure 4) --- main-body version.

(a) Per-benchmark gap g (= published score − matched consumer satisfaction)
    across the 5 privacy conditions, for 5 representative benchmarks --- one per
    primary capability dimension covered by the benchmark suite. The forest is
    populated from the 11-benchmark non-outlier set (Agentic Tasks and Function
    Calling are excluded as agentic-calibration outliers).
(b) Δg = gap@private_only − gap@public_only versus provider over-investment on
    each benchmark's primary dimension (capability on the highest-weighted
    dimension minus the cross-dimension mean, computed from public_only seeds).
    Same 11-benchmark exclusion convention.

LLM Sonnet 4.6 (filled markers) overlaid with heuristic-mode endpoints (open
markers, larger N). Shared plotting helpers in this file are also imported by
``privacy_gap_full.py`` (the 13-benchmark appendix variant).

Outputs (PDF + PNG):
    output/paper/privacy_gap_main.pdf  — 5 representative benchmarks (paper §5)

Usage:
    python -m scripts.plots.paper.privacy_gap_main
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.plots import paths as _paths
from scripts.plots.per_benchmark import (
    per_benchmark_from_jsonl, BM_ORDER, EXCLUDE_BM as _EXCL_DEF, DIMS,
)
from scripts.plots.per_benchmark_core_privacy import build_long_df, _agg_per_condition

EXCLUDE_BM = list(_EXCL_DEF)

PRIV_ORDER = ["public_only", "baseline", "private_dominant", "private_only", "iid_holdout"]
PRIV_LABELS = {
    "public_only":      "public (13/0/0)",
    "baseline":         "baseline (8/3/2 mix)",
    "private_dominant": "private-dominant (cos=0.95)",
    "private_only":     "private (cos=0.85)",
    "iid_holdout":      "iid-holdout null (cos=1.0)",
}
PRIV_COLORS = {
    "public_only":      "#2c7fb8",  # blue
    "baseline":         "#fec44f",  # yellow
    "private_dominant": "#fd8d3c",  # orange
    "private_only":     "#b10026",  # dark red
    "iid_holdout":      "#7f7f7f",  # neutral gray
}
DIM_COLORS = {
    "reasoning":     "#1f77b4",
    "coding":        "#2ca02c",
    "knowledge":     "#9467bd",
    "safety":        "#d62728",
    "communication": "#ff7f0e",
    "agentic":       "#8c564b",
}

# 5 reps for main-paper panel (a). One benchmark per primary capability dimension
# present in the active suite (agentic is dropped because the only agentic-primary
# benchmarks are the EXCLUDE_BM calibration outliers).
REP_BENCHMARKS = [
    "Advanced Math",          # reasoning
    "Safety Evaluation",      # safety
    "Clinical Reasoning",     # knowledge
    "Coding Evaluation",      # coding
    "Instruction Following",  # communication
]

# Marker sizes / fonts tuned bigger than the prior figure4_combined.
MS_LLM = 12.0      # filled (LLM)
MS_HEUR = 13.0     # open (heuristic) — slightly larger so the ring is legible behind the LLM dot
MS_PANEL_B = 14.0  # scatter (panel b)
ELW = 1.6          # error-bar linewidth

plt.rcParams.update({
    "font.size":         13,
    "axes.titlesize":    14,
    "axes.labelsize":    13,
    "xtick.labelsize":   12,
    "ytick.labelsize":   12,
    "legend.fontsize":   12,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "font.family":       "DejaVu Sans",
    "savefig.dpi":       180,
})


def _vec(d):
    return np.array([d.get(k, 0.0) for k in DIMS], dtype=float)


# ───────────────────── Heuristic loader (canonical staging) ─────────────────────

def discover_heuristic_runs(min_rounds: int = 40):
    """Yield (cond, seed, jsonl_path) for heuristic runs at
    hf_data_staging/core_privacy/heuristic/<cond>/seed_*/rounds.jsonl."""
    root = os.path.join(_paths.PROJECT_ROOT, "hf_data_staging", "core_privacy", "heuristic")
    if not os.path.isdir(root):
        return
    for cond_dir in sorted(glob.glob(os.path.join(root, "*"))):
        cond = os.path.basename(cond_dir)
        if cond not in PRIV_ORDER:
            continue
        for seed_dir in sorted(glob.glob(os.path.join(cond_dir, "seed_*"))):
            seed = int(os.path.basename(seed_dir).split("_", 1)[1])
            jsonl = os.path.join(seed_dir, "rounds.jsonl")
            if not os.path.exists(jsonl):
                continue
            with open(jsonl) as f:
                n = sum(1 for _ in f)
            if n < min_rounds:
                continue
            yield cond, seed, jsonl


def build_long_df_heuristic(restrict_conds=None) -> pd.DataFrame:
    rows = []
    for cond, seed, jsonl in discover_heuristic_runs():
        if restrict_conds and cond not in restrict_conds:
            continue
        try:
            df = per_benchmark_from_jsonl(jsonl)
        except Exception as e:
            print(f"  ERR {jsonl}: {e}")
            continue
        for _, r in df.iterrows():
            rows.append({"condition": cond, "seed": seed,
                         "benchmark": r["benchmark"], "provider": r["provider"],
                         "clean_gap": r["clean_gap"], "score": r["score"],
                         "clean_matched": r["clean_matched"]})
    return pd.DataFrame(rows)


# ───────────────────── Primary-dimension + capability surplus ─────────────────────

def _last_round(jsonl_path: str):
    with open(jsonl_path) as f:
        rounds = [json.loads(l) for l in f if l.strip()]
    return rounds[-1] if rounds else None


def benchmark_primary_dims(jsonl_path: str) -> dict[str, str]:
    """{bm_name: primary_dim} from the final-round CDW."""
    last = _last_round(jsonl_path)
    if last is None:
        return {}
    out = {}
    for bm, w in last.get("benchmark_dimension_weights", {}).items():
        v = _vec(w)
        if v.sum() <= 0:
            continue
        out[bm] = DIMS[int(np.argmax(v))]
    return out


def population_capability_surplus(public_jsonls: list[str], primary: dict[str, str],
                                   exclude_bm: list[str] | None = None) -> pd.DataFrame:
    """Per-benchmark surplus = pop_capability[primary_dim(bm)] − pop_capability.mean()
    where pop_capability is averaged across providers, rounds, and seeds in public_only runs.

    exclude_bm: benchmarks to drop. None → use the module default EXCLUDE_BM.
                Pass an empty list to keep every benchmark.
    """
    if exclude_bm is None:
        exclude_bm = EXCLUDE_BM
    per_run_caps = []
    for j in public_jsonls:
        with open(j) as f:
            rounds = [json.loads(l) for l in f if l.strip()]
        if not rounds:
            continue
        accum = defaultdict(lambda: np.zeros(len(DIMS)))
        cnt = defaultdict(int)
        for r in rounds:
            for p, cap in r.get("capability_vectors", {}).items():
                accum[p] += _vec(cap)
                cnt[p] += 1
        per_run_caps.append({p: accum[p] / cnt[p] for p, c in cnt.items() if c})
    if not per_run_caps:
        return pd.DataFrame()
    provs = set().union(*(d.keys() for d in per_run_caps))
    prov_mean = {p: np.mean([d[p] for d in per_run_caps if p in d], axis=0) for p in provs}
    pop = np.mean(list(prov_mean.values()), axis=0)
    pop_avg = float(pop.mean())
    rows = []
    for bm, dim in primary.items():
        if bm in exclude_bm:
            continue
        rows.append({"benchmark": bm, "primary_dim": dim,
                     "surplus": float(pop[DIMS.index(dim)] - pop_avg)})
    return pd.DataFrame(rows)


def _delta_gap(agg: pd.DataFrame) -> dict[str, float]:
    """Return {bm: gap@private_only − gap@public_only}."""
    out = {}
    for bm in agg.benchmark.unique():
        pub = agg[(agg.benchmark == bm) & (agg.condition == "public_only")]
        priv = agg[(agg.benchmark == bm) & (agg.condition == "private_only")]
        if len(pub) and len(priv):
            out[bm] = float(priv["mean"].iloc[0]) - float(pub["mean"].iloc[0])
    return out


# ───────────────────── Panel (a): forest, LLM filled + heuristic open ─────────────────────

def _draw_forest(ax, agg_llm, agg_heur, bm_list, label_dg=True):
    n_cond = len(PRIV_ORDER)
    dodge = np.linspace(-0.32, 0.32, n_cond)
    y_pos = np.arange(len(bm_list))
    panel_max_x = -np.inf

    for j, cond in enumerate(PRIV_ORDER):
        for i, bm in enumerate(bm_list):
            # Heuristic open (background)
            rh = agg_heur[(agg_heur.benchmark == bm) & (agg_heur.condition == cond)]
            if len(rh):
                xh = float(rh["mean"].iloc[0])
                ch = float(rh["ci"].iloc[0])
                ax.errorbar([xh], [y_pos[i] + dodge[j]], xerr=[ch],
                            fmt="o", markersize=MS_HEUR, mfc="white",
                            mec=PRIV_COLORS[cond], mew=1.6,
                            ecolor=PRIV_COLORS[cond], elinewidth=ELW * 0.7,
                            capsize=2.5, alpha=0.95, zorder=2)
                panel_max_x = max(panel_max_x, xh + ch)
            # LLM filled (foreground)
            rl = agg_llm[(agg_llm.benchmark == bm) & (agg_llm.condition == cond)]
            if len(rl):
                xl = float(rl["mean"].iloc[0])
                cl = float(rl["ci"].iloc[0])
                ax.errorbar([xl], [y_pos[i] + dodge[j]], xerr=[cl],
                            fmt="o", markersize=MS_LLM, color=PRIV_COLORS[cond],
                            mec="black", mew=0.6,
                            elinewidth=ELW, capsize=2.5, zorder=4)
                panel_max_x = max(panel_max_x, xl + cl)

    label_x = panel_max_x + 0.004
    if label_dg:
        dg_llm = _delta_gap(agg_llm)
        for i, bm in enumerate(bm_list):
            if bm in dg_llm:
                ax.text(label_x, y_pos[i], rf"$\Delta g$={dg_llm[bm]:+.3f}",
                        fontsize=12, va="center", color="#333")

    ax.axvline(0, color="black", lw=1.0, alpha=0.7)
    ax.set_xlabel(r"Gap (g) = score $-$ matched satisfaction")
    xmin, xmax = ax.get_xlim()
    ax.set_xlim(xmin, max(xmax, label_x + 0.028))


# ───────────────────── Panel (b): Δg vs surplus scatter ─────────────────────

def _draw_scatter(ax, llm_pts: pd.DataFrame, heur_pts: pd.DataFrame):
    """llm_pts and heur_pts both have columns: benchmark, primary_dim, surplus, dgap."""
    # Heuristic (open rings) drawn first; then LLM (filled) on top.
    for df, fill_kind, ms, alpha, zorder in [
        (heur_pts, "open", MS_PANEL_B + 1, 0.85, 2),
        (llm_pts,  "fill", MS_PANEL_B,     0.95, 4),
    ]:
        for _, r in df.iterrows():
            c = DIM_COLORS.get(r["primary_dim"], "#444")
            if fill_kind == "fill":
                ax.plot(r["surplus"], r["dgap"], "o", markersize=ms,
                        color=c, mec="black", mew=0.6, alpha=alpha, zorder=zorder)
            else:
                ax.plot(r["surplus"], r["dgap"], "o", markersize=ms,
                        mfc="white", mec=c, mew=1.7, alpha=alpha, zorder=zorder)

    # Benchmark labels (LLM positions, slightly offset)
    for _, r in llm_pts.iterrows():
        ax.annotate(r["benchmark"],
                    xy=(r["surplus"], r["dgap"]),
                    xytext=(6, 4), textcoords="offset points",
                    fontsize=10.5, color="#333", alpha=0.95)

    # Regression lines: solid LLM, dashed heuristic.
    xlim_lo = min(llm_pts.surplus.min(), heur_pts.surplus.min()) - 0.005
    xlim_hi = max(llm_pts.surplus.max(), heur_pts.surplus.max()) + 0.025
    xs = np.linspace(xlim_lo, xlim_hi, 50)
    stats_lines = []
    for label, df, ls, lw in [("LLM Sonnet", llm_pts, "-", 1.7),
                               ("Heuristic ", heur_pts, "--", 1.4)]:
        if len(df) >= 2:
            slope, intercept = np.polyfit(df.surplus, df.dgap, 1)
            ax.plot(xs, slope * xs + intercept, ls=ls, lw=lw, color="#444",
                    alpha=0.85, zorder=1)
            r = float(np.corrcoef(df.surplus, df.dgap)[0, 1])
            # two-sided p from t-stat
            n = len(df)
            t_stat = r * np.sqrt(max(n - 2, 1) / max(1 - r * r, 1e-12))
            from scipy.stats import t as student_t
            p = float(2 * (1 - student_t.cdf(abs(t_stat), df=max(n - 2, 1))))
            stats_lines.append(f"{label}: r = {r:.3f}, p = {p:.2g}")

    ax.axvline(0, color="gray", lw=0.6, alpha=0.5)
    ax.axhline(0, color="gray", lw=0.6, alpha=0.5)
    ax.set_xlim(xlim_lo, xlim_hi)
    ax.set_xlabel("Provider over-investment on benchmark's primary skill")
    ax.set_ylabel(r"$\Delta$gap shift under privacy"
                  "\n"
                  r"(gap @ private$\_$only $-$ gap @ public$\_$only)")
    if stats_lines:
        ax.text(0.03, 0.05, "\n".join(stats_lines + [f"N = {len(llm_pts)} benchmarks"]),
                transform=ax.transAxes, ha="left", va="bottom", fontsize=11.5,
                bbox=dict(boxstyle="round,pad=0.45", fc="white", ec="#888", alpha=0.95))


# ───────────────────── Combined figure ─────────────────────

def _bm_ordering_for_panel_a(agg_llm: pd.DataFrame, restrict_to: list[str]) -> list[str]:
    """Return the benchmarks in `restrict_to` ordered by LLM public_only mean (descending)."""
    pub = agg_llm[agg_llm.condition == "public_only"].set_index("benchmark")["mean"]
    keep = [b for b in restrict_to if b in pub.index]
    return list(pub.reindex(keep).sort_values(ascending=False).index)


def _attach_panel_a_legend(ax, anchor_y: float = -0.10):
    """Privacy-conditions legend, two rows, anchored just below the x-axis label."""
    handles = [Line2D([0], [0], marker="o", color="w",
                      markerfacecolor=PRIV_COLORS[c], markeredgecolor="black",
                      markersize=11, label=PRIV_LABELS[c])
               for c in PRIV_ORDER]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, anchor_y),
              ncol=3, fontsize=12, frameon=False,
              columnspacing=1.4, handletextpad=0.4)


def _attach_panel_b_legend(ax, anchor_y: float = -0.10):
    """Primary-dimension color legend, two rows, anchored just below the x-axis label."""
    handles = [Line2D([0], [0], marker="o", color="w",
                      markerfacecolor=DIM_COLORS[d], markeredgecolor="black",
                      markersize=11, label=d)
               for d in DIMS]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, anchor_y),
              ncol=3, fontsize=12, frameon=False,
              columnspacing=1.4, handletextpad=0.4)


def render(agg_llm: pd.DataFrame, agg_heur: pd.DataFrame,
           llm_pts: pd.DataFrame, heur_pts: pd.DataFrame,
           bm_list_panel_a: list[str], n_llm_pub: int, n_heur_pub: int,
           out_path_no_ext: str, panel_a_title: str,
           figsize: tuple[float, float] = (17.5, 7.4),
           legend_anchor_y: float = -0.10):
    """Render the two-panel figure. ``figsize`` and ``legend_anchor_y`` allow
    callers (e.g. the 11-bm vs 13-bm scripts) to tune the aspect ratio and
    legend whitespace independently."""
    fig = plt.figure(figsize=figsize)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.05, 1.0], wspace=0.22)
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])

    _draw_forest(ax_a, agg_llm, agg_heur, bm_list_panel_a, label_dg=True)
    ax_a.set_yticks(np.arange(len(bm_list_panel_a)))
    ax_a.set_yticklabels([b.replace(" ", "\n", 1) for b in bm_list_panel_a])
    ax_a.invert_yaxis()
    ax_a.set_title(panel_a_title, loc="left", fontsize=14, fontweight="bold")
    _attach_panel_a_legend(ax_a, anchor_y=legend_anchor_y)

    _draw_scatter(ax_b, llm_pts, heur_pts)
    ax_b.set_title("(b) Gap shift tracks capability surplus on dominant dimension",
                   loc="left", fontsize=14, fontweight="bold")
    _attach_panel_b_legend(ax_b, anchor_y=legend_anchor_y)

    fig.tight_layout(rect=[0, 0.08, 1, 1])
    for ext in ("pdf", "png"):
        out = f"{out_path_no_ext}.{ext}"
        fig.savefig(out, bbox_inches="tight")
        print(f"  wrote {out}")
    plt.close(fig)


# ───────────────────────────── main ─────────────────────────────

def _build_panel_b_points(df_long: pd.DataFrame, public_jsonls: list[str],
                          primary: dict[str, str],
                          exclude_bm: list[str] | None = None) -> pd.DataFrame:
    """One row per benchmark (after exclude_bm): (benchmark, primary_dim, surplus, dgap).
    df_long: long-form (condition, seed, benchmark, provider, clean_gap).
    exclude_bm: defaults to module EXCLUDE_BM. Pass [] to retain all benchmarks."""
    if exclude_bm is None:
        exclude_bm = EXCLUDE_BM
    surplus = population_capability_surplus(public_jsonls, primary, exclude_bm=exclude_bm)
    if surplus.empty:
        return pd.DataFrame()
    sub = df_long[df_long.condition.isin(["public_only", "private_only"])]
    sub = sub[~sub.benchmark.isin(exclude_bm)]
    g_run = sub.groupby(["condition", "seed", "benchmark"])["clean_gap"].mean().reset_index()
    g_bm = g_run.groupby(["benchmark", "condition"])["clean_gap"].mean().reset_index()
    pub = g_bm[g_bm.condition == "public_only"].set_index("benchmark")["clean_gap"]
    priv = g_bm[g_bm.condition == "private_only"].set_index("benchmark")["clean_gap"]
    rows = []
    for _, r in surplus.iterrows():
        bm = r["benchmark"]
        if bm in pub.index and bm in priv.index:
            rows.append({"benchmark": bm,
                         "primary_dim": r["primary_dim"],
                         "surplus":     r["surplus"],
                         "dgap":        float(priv[bm] - pub[bm])})
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out-dir", default=None,
                    help="Output directory (default: output/paper/)")
    args = ap.parse_args()

    out_dir = args.out_dir or _paths.paper_dir()
    os.makedirs(out_dir, exist_ok=True)

    # ── Load LLM (canonical staging, sonnet only) ──
    print("Loading LLM Sonnet 4.6 (hf_data_staging/core_privacy/llm/claude-sonnet-4-6)...")
    df_llm = build_long_df("_core_privacy", "sonnet")
    df_llm = df_llm[df_llm.condition.isin(PRIV_ORDER)]
    df_llm = df_llm[~df_llm.benchmark.isin(EXCLUDE_BM)]
    print(f"  rows={len(df_llm)}, seeds={df_llm.seed.nunique()}, conds={sorted(df_llm.condition.unique())}")

    # ── Load heuristic (canonical staging) ──
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
    # Mirror _agg_per_condition for heuristic (already free of excluded bms).
    g_run = df_heur.groupby(["condition", "seed", "benchmark"])["clean_gap"].mean().reset_index()
    agg_heur = g_run.groupby(["benchmark", "condition"])["clean_gap"].agg(
        mean="mean", sd="std", n="count").reset_index()
    agg_heur["ci"] = np.where(agg_heur["n"] > 1,
                               1.96 * agg_heur["sd"] / np.sqrt(agg_heur["n"]),
                               0.0)

    # ── Primary dimensions + capability surplus ──
    print("Resolving primary dimensions + population capability surplus...")
    sample_pub_dirs = sorted(glob.glob(os.path.join(
        _paths.PROJECT_ROOT, "hf_data_staging", "core_privacy",
        "llm", "claude-sonnet-4-6", "public_only", "seed_*")))
    sample_pub_jsonls_llm = [os.path.join(d, "rounds.jsonl") for d in sample_pub_dirs
                              if os.path.exists(os.path.join(d, "rounds.jsonl"))]
    sample_pub_jsonls_heur = [j for cond, _seed, j in discover_heuristic_runs()
                               if cond == "public_only"]
    primary = benchmark_primary_dims(sample_pub_jsonls_llm[0])
    print("  primary dims (sample):",
          {k: primary.get(k) for k in REP_BENCHMARKS})

    # Paper §5: exclude agentic-calibration outliers (11-bm view) from panel (b).
    llm_pts  = _build_panel_b_points(df_llm,  sample_pub_jsonls_llm,  primary)
    heur_pts = _build_panel_b_points(df_heur, sample_pub_jsonls_heur, primary)
    print(f"  panel-b points (11-bm): LLM N={len(llm_pts)}, heur N={len(heur_pts)}")

    n_llm_pub  = int(df_llm[df_llm.condition == "public_only"]["seed"].nunique())
    n_heur_pub = int(df_heur[df_heur.condition == "public_only"]["seed"].nunique())

    # ── Render: 5-rep main figure (panel-a 5 reps; panel-b 11-bm) ──
    # Wider aspect + tighter legend whitespace for the main-paper figure.
    print("\nRendering 5-rep main figure -> privacy_gap_main.{pdf,png}")
    bm_panel_a = _bm_ordering_for_panel_a(agg_llm, REP_BENCHMARKS)
    render(agg_llm, agg_heur, llm_pts, heur_pts,
           bm_list_panel_a=bm_panel_a,
           n_llm_pub=n_llm_pub, n_heur_pub=n_heur_pub,
           out_path_no_ext=os.path.join(out_dir, "privacy_gap_main"),
           panel_a_title="(a) Per-benchmark gap across privacy ladder",
           figsize=(20.0, 6.6), legend_anchor_y=-0.08)


if __name__ == "__main__":
    main()
