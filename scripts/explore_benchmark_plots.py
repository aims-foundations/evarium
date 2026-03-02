"""
explore_benchmark_plots.py — Benchmark-level score inflation visualisations

Three experimental plots for comparing per-benchmark gaming dynamics across
experiments. Intentionally separate from create_final_plots.py — edit freely.

Usage:
    python explore_benchmark_plots.py                  # use EXPERIMENTS list
    python explore_benchmark_plots.py 3 9 11           # resolve by number
    python explore_benchmark_plots.py 3 9 11 my_run    # named output folder
"""

import os
import sys
import json
import warnings
from math import ceil

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib as mpl
import numpy as np

# Add src/ to path
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_PROJECT_ROOT, "src"))

# ---------------------------------------------------------------------------
# Tueplots styling
# ---------------------------------------------------------------------------
try:
    from tueplots import bundles as _tb
    _rc = _tb.neurips2024()
    _rc.pop("figure.figsize", None)
    # Enable LaTeX rendering for publication-quality fonts.
    # Set MPLLATEX=0 in the environment to disable if LaTeX is not available.
    if os.environ.get("MPLLATEX", "1") != "0":
        _rc["text.usetex"] = True
    mpl.rcParams.update(_rc)
except ImportError:
    warnings.warn("tueplots not installed — using default style", stacklevel=1)

from plotting import get_providers, get_provider_colors, get_investment_colors

# ===========================================================================
# CONFIGURATION
# ===========================================================================
EXPERIMENTS = [
    {"id": "exp_003_full_ecosystem_us", "label": "US Baseline"},
    {"id": "exp_002_full_ecosystem_eu", "label": "EU Baseline"},
    {"id": "exp_004_ablation_no_media_balanced", "label": "No Media"},
]

OUTPUT_DIR   = os.path.join(_PROJECT_ROOT, "output", "explore-benchmark-plots")
EXPERIMENTS_DIR = os.path.join(_PROJECT_ROOT, "output", "experiments")

# ===========================================================================
# Data helpers
# ===========================================================================

def load_history(exp_id):
    path = os.path.join(EXPERIMENTS_DIR, exp_id, "history.json")
    if not os.path.exists(path):
        warnings.warn(f"Missing: {path}")
        return []
    with open(path) as f:
        return json.load(f)


def all_benchmarks(history):
    """Ordered list of benchmarks by first appearance round."""
    seen = {}
    for h in history:
        for b in h.get("per_benchmark_scores", {}):
            if b not in seen:
                seen[b] = h["round"]
    return sorted(seen, key=seen.get)


def intro_round(history, benchmark):
    """Round a benchmark first appears; None if never."""
    for h in history:
        if benchmark in h.get("per_benchmark_scores", {}):
            return h["round"]
    return None


def score_inflation_series(history, benchmark):
    """
    Returns (rounds, mean_inflation) where inflation = mean over providers of
    (per_benchmark_score - true_capability) for rounds the benchmark is active.
    """
    rounds, inflations = [], []
    for h in history:
        pbs = h.get("per_benchmark_scores", {})
        caps = h.get("true_capabilities", {})
        if benchmark not in pbs:
            continue
        vals = []
        for p, score in pbs[benchmark].items():
            if p in caps:
                vals.append(score - caps[p])
        if vals:
            rounds.append(h["round"])
            inflations.append(np.mean(vals))
    return rounds, inflations


def provider_mean_inflation(history, benchmark):
    """
    Returns {provider: mean inflation} for a benchmark across all rounds it
    is active.
    """
    acc = {}
    counts = {}
    for h in history:
        pbs = h.get("per_benchmark_scores", {})
        caps = h.get("true_capabilities", {})
        if benchmark not in pbs:
            continue
        for p, score in pbs[benchmark].items():
            if p in caps:
                acc[p]    = acc.get(p, 0.0) + (score - caps[p])
                counts[p] = counts.get(p, 0) + 1
    return {p: acc[p] / counts[p] for p in acc}


def rolling_bench_correlation(history, benchmark, window=5):
    """Rolling Pearson r between per_benchmark_score and true_capability."""
    rounds_out, corrs = [], []
    active = [(h["round"],
               h["per_benchmark_scores"][benchmark],
               h["true_capabilities"])
              for h in history
              if benchmark in h.get("per_benchmark_scores", {})]
    if len(active) < window:
        return [], []
    for i in range(window, len(active) + 1):
        win = active[i - window:i]
        scores, caps = [], []
        for _, pbs, tcaps in win:
            for p, s in pbs.items():
                if p in tcaps:
                    scores.append(s)
                    caps.append(tcaps[p])
        if len(scores) >= 2:
            r = np.corrcoef(scores, caps)[0, 1]
            if not np.isnan(r):
                rounds_out.append(active[i - 1][0])
                corrs.append(r)
    return rounds_out, corrs


# ===========================================================================
# Shared colour map for experiments
# ===========================================================================

def exp_colors(n):
    return plt.cm.tab10(np.linspace(0, 0.9, n))


# ===========================================================================
# Plot A — Score Inflation Trajectories (small multiples by benchmark)
# ===========================================================================
# One panel per benchmark. Each panel: x=round, y=mean(score-capability),
# one line per experiment. Vertical dashed line at benchmark introduction.
# Reveals: does gaming accumulate? Does new-benchmark introduction reset it?

def plot_a_inflation_trajectories(all_data):
    # Union of benchmarks across all experiments, ordered by first appearance
    bench_union = []
    seen = set()
    for d in all_data:
        for b in all_benchmarks(d["history"]):
            if b not in seen:
                bench_union.append(b)
                seen.add(b)

    N = len(bench_union)
    if N == 0:
        return

    n_cols = min(N, 4)
    n_rows = ceil(N / n_cols)
    colors = exp_colors(len(all_data))

    fig, axes = plt.subplots(n_rows, n_cols,
                             figsize=(2.25 * n_cols, 1.75 * n_rows),
                             squeeze=False)
    fig.suptitle("Score Inflation Trajectories per Benchmark\n"
                 r"(mean score $-$ true capability across providers)",
                 fontweight="bold", fontsize=13)

    for bi, bench in enumerate(bench_union):
        row, col = divmod(bi, n_cols)
        ax = axes[row][col]
        ax.axhline(0, color="black", linewidth=0.8, linestyle="-", alpha=0.4)

        for di, (d, color) in enumerate(zip(all_data, colors)):
            history = d["history"]
            rounds, inflation = score_inflation_series(history, bench)
            if not rounds:
                continue
            ax.plot(rounds, inflation, marker="o", markersize=2.5,
                    linewidth=1.5, color=color, label=d["label"])

            # Vertical line at introduction round
            ir = intro_round(history, bench)
            if ir is not None and ir > min(rounds):
                ax.axvline(ir, color=color, linewidth=0.8,
                           linestyle="--", alpha=0.5)

        ax.set_title(bench.replace("_", " ").title(),
                     fontweight="bold", fontsize=10)
        ax.set_xlabel("Round", fontsize=9)
        ax.set_ylabel("Score Inflation", fontsize=9)
        ax.tick_params(labelsize=8)
        ax.grid(False)

    # Hide unused
    for bi in range(N, n_rows * n_cols):
        row, col = divmod(bi, n_cols)
        axes[row][col].set_visible(False)

    # Legend once
    handles = [mlines.Line2D([], [], color=c, linewidth=1.5, label=d["label"])
               for d, c in zip(all_data, colors)]
    fig.legend(handles=handles, loc="lower center",
               bbox_to_anchor=(0.5, -0.02), ncol=len(all_data),
               fontsize=9, frameon=True)

    fig.tight_layout(rect=[0, 0.05, 1, 0.95])
    _save(fig, "A_inflation_trajectories.png")


# ===========================================================================
# Plot B — Provider Gaming Fingerprint Heatmap
# ===========================================================================
# Rows = providers (fixed order), columns = benchmarks.
# Color = mean score inflation (score - capability) averaged over all active rounds.
# One heatmap per experiment, stacked vertically.
# Reveals: which providers game which benchmarks, and does this change across conditions?

CORE_PROVIDERS = ["Orion Labs", "Apex AI", "Genesis Systems", "Mirage AI", "OpenCore"]


def _provider_order_for_heatmap(all_data):
    startup_seen = {}
    for d in all_data:
        for h in d["history"]:
            for p in h.get("per_benchmark_scores", {}).get(
                    list(h.get("per_benchmark_scores", {}).keys() or [""])[0], {}):
                if p not in CORE_PROVIDERS and p not in startup_seen:
                    startup_seen[p] = h["round"]
    first = sorted(startup_seen, key=startup_seen.get)[:1]
    return CORE_PROVIDERS + first


def plot_b_gaming_fingerprint(all_data):
    bench_union = []
    seen = set()
    for d in all_data:
        for b in all_benchmarks(d["history"]):
            if b not in seen:
                bench_union.append(b)
                seen.add(b)

    providers = _provider_order_for_heatmap(all_data)
    N_exp = len(all_data)
    if not bench_union:
        return

    fig, axes = plt.subplots(N_exp, 1,
                             figsize=(min(6.75, max(3.25, len(bench_union) * 0.45)),
                                      1.2 * N_exp + 0.5),
                             squeeze=False)
    fig.suptitle("Provider Gaming Fingerprint\n"
                 r"(mean score $-$ true capability per provider per benchmark)",
                 fontweight="bold", fontsize=13)

    # Compute global color scale for consistent comparison across experiments
    all_vals = []
    for d in all_data:
        for b in bench_union:
            inf = provider_mean_inflation(d["history"], b)
            all_vals.extend(inf.values())
    vmax = max(abs(v) for v in all_vals) if all_vals else 0.2
    vmin = -vmax

    for ei, d in enumerate(all_data):
        ax = axes[ei][0]
        mat = np.full((len(providers), len(bench_union)), np.nan)
        for pi, p in enumerate(providers):
            for bi, b in enumerate(bench_union):
                inf = provider_mean_inflation(d["history"], b)
                if p in inf:
                    mat[pi, bi] = inf[p]

        im = ax.imshow(mat, aspect="auto", cmap="RdBu_r",
                       vmin=vmin, vmax=vmax, interpolation="nearest")

        ax.set_yticks(range(len(providers)))
        ax.set_yticklabels(providers, fontsize=8)
        ax.set_xticks(range(len(bench_union)))
        ax.set_xticklabels([b.replace("_", "\n") for b in bench_union],
                           fontsize=7, ha="center")
        ax.set_title(d["label"], fontweight="bold", fontsize=10, loc="left")
        ax.tick_params(length=0)

        # Annotate cells with value
        for pi in range(len(providers)):
            for bi in range(len(bench_union)):
                v = mat[pi, bi]
                if not np.isnan(v):
                    ax.text(bi, pi, f"{v:+.2f}", ha="center", va="center",
                            fontsize=6.5,
                            color="white" if abs(v) > vmax * 0.6 else "black")

    # Shared colorbar
    cb = fig.colorbar(im, ax=axes[:, 0], fraction=0.02, pad=0.02)
    cb.set_label("Score Inflation", fontsize=9)
    cb.ax.tick_params(labelsize=8)

    fig.subplots_adjust(top=0.90, bottom=0.05, left=0.12, right=0.91, hspace=0.4)
    _save(fig, "B_gaming_fingerprint.png")


# ===========================================================================
# Plot C — Per-Benchmark Rolling Validity
# ===========================================================================
# One panel per benchmark. X = round, Y = rolling Pearson r(score, capability).
# One line per experiment. Shows when each benchmark's validity degrades, and
# whether policy conditions slow or accelerate that process.

def plot_c_rolling_validity(all_data):
    bench_union = []
    seen = set()
    for d in all_data:
        for b in all_benchmarks(d["history"]):
            if b not in seen:
                bench_union.append(b)
                seen.add(b)

    N = len(bench_union)
    if N == 0:
        return

    n_cols = min(N, 4)
    n_rows = ceil(N / n_cols)
    colors = exp_colors(len(all_data))

    fig, axes = plt.subplots(n_rows, n_cols,
                             figsize=(2.25 * n_cols, 1.75 * n_rows),
                             squeeze=False)
    fig.suptitle("Per-Benchmark Rolling Validity\n"
                 r"(Pearson $r$: benchmark score vs true capability, window=5)",
                 fontweight="bold", fontsize=13)

    for bi, bench in enumerate(bench_union):
        row, col = divmod(bi, n_cols)
        ax = axes[row][col]

        for d, color in zip(all_data, colors):
            rounds, corrs = rolling_bench_correlation(d["history"], bench)
            if not rounds:
                continue
            ax.plot(rounds, corrs, marker="o", markersize=2.5,
                    linewidth=1.5, color=color, label=d["label"])

        # Reference lines
        ax.axhline(0.7, color="green",  linewidth=0.7, linestyle=":", alpha=0.6)
        ax.axhline(0.5, color="orange", linewidth=0.7, linestyle=":", alpha=0.6)
        ax.axhline(0.3, color="red",    linewidth=0.7, linestyle=":", alpha=0.6)

        ax.set_ylim(-0.1, 1.05)
        ax.set_title(bench.replace("_", " ").title(),
                     fontweight="bold", fontsize=10)
        ax.set_xlabel("Round", fontsize=9)
        ax.set_ylabel("Validity (r)", fontsize=9)
        ax.tick_params(labelsize=8)
        ax.grid(False)

    for bi in range(N, n_rows * n_cols):
        row, col = divmod(bi, n_cols)
        axes[row][col].set_visible(False)

    handles = [mlines.Line2D([], [], color=c, linewidth=1.5, label=d["label"])
               for d, c in zip(all_data, colors)]
    # Reference line legend entries
    handles += [
        mlines.Line2D([], [], color="green",  linestyle=":", label="r=0.7 (good)"),
        mlines.Line2D([], [], color="orange", linestyle=":", label="r=0.5 (moderate)"),
        mlines.Line2D([], [], color="red",    linestyle=":", label="r=0.3 (poor)"),
    ]
    fig.legend(handles=handles, loc="lower center",
               bbox_to_anchor=(0.5, -0.02),
               ncol=min(6, len(handles)), fontsize=9, frameon=True)

    fig.tight_layout(rect=[0, 0.05, 1, 0.95])
    _save(fig, "C_rolling_validity.png")


# ===========================================================================
# Plot D — Per-Provider Regression Lines (rows=benchmarks, cols=experiments)
# ===========================================================================
# Each cell: scatter of (true_capability, per_benchmark_score) across all
# rounds, one color per provider, with a fitted OLS line per provider.
# Intercept encodes systematic score inflation; slope encodes whether scores
# track capability changes. y=x dashed reference. Axis limits shared within
# each benchmark row for direct cross-experiment comparison.

def plot_d_provider_regression(all_data):
    bench_union = []
    seen = set()
    for d in all_data:
        for b in all_benchmarks(d["history"]):
            if b not in seen:
                bench_union.append(b)
                seen.add(b)

    N_bench = len(bench_union)
    N_exp   = len(all_data)
    if N_bench == 0:
        return

    # Collect all providers across all experiments for a consistent color map
    all_providers = []
    seen_p = set()
    for d in all_data:
        for p in get_providers(d["history"]):
            if p not in seen_p:
                all_providers.append(p)
                seen_p.add(p)
    provider_colors = get_provider_colors(all_providers)

    fig, axes = plt.subplots(
        N_bench, N_exp,
        figsize=(2.25 * N_exp, 1.5 * N_bench),
        squeeze=False,
    )
    fig.suptitle(
        "Score vs. True Capability: Per-Provider Regression by Benchmark\n"
        "(intercept = inflation bias; slope = capability tracking; dashed = perfect calibration)",
        fontweight="bold", fontsize=13,
    )

    # Pre-compute per-row axis limits so all experiments share the same scale
    row_xlims = []
    row_ylims = []
    for bench in bench_union:
        all_caps, all_scores = [], []
        for d in all_data:
            for h in d["history"]:
                pbs  = h.get("per_benchmark_scores", {}).get(bench, {})
                caps = h.get("true_capabilities", {})
                for p, score in pbs.items():
                    if p in caps:
                        all_caps.append(caps[p])
                        all_scores.append(score)
        if all_caps:
            pad = 0.02
            row_xlims.append((min(all_caps)  - pad, max(all_caps)  + pad))
            row_ylims.append((min(all_scores) - pad, max(all_scores) + pad))
        else:
            row_xlims.append((0, 1))
            row_ylims.append((0, 1))

    for bi, bench in enumerate(bench_union):
        xlim = row_xlims[bi]
        ylim = row_ylims[bi]

        for ei, d in enumerate(all_data):
            ax = axes[bi][ei]
            history = d["history"]

            # Collect per-provider (cap, score) pairs
            provider_data = {}
            for h in history:
                pbs  = h.get("per_benchmark_scores", {}).get(bench, {})
                caps = h.get("true_capabilities", {})
                for p, score in pbs.items():
                    if p in caps:
                        provider_data.setdefault(p, ([], []))
                        provider_data[p][0].append(caps[p])
                        provider_data[p][1].append(score)

            if not provider_data:
                ax.text(0.5, 0.5, "No data", transform=ax.transAxes,
                        ha="center", va="center", color="gray", fontsize=9)
            else:
                # y=x reference line
                ref = np.linspace(xlim[0], xlim[1], 50)
                ax.plot(ref, ref, "k--", linewidth=0.8, alpha=0.35, zorder=0)

                for p, (caps_p, scores_p) in provider_data.items():
                    color = provider_colors.get(p, "#888888")
                    caps_arr   = np.array(caps_p)
                    scores_arr = np.array(scores_p)

                    # Scatter (small, semi-transparent)
                    ax.scatter(caps_arr, scores_arr, color=color,
                               s=8, alpha=0.3, zorder=1)

                    # OLS fit (need at least 2 distinct x values)
                    if len(np.unique(caps_arr)) >= 2:
                        m, b = np.polyfit(caps_arr, scores_arr, 1)
                        x_line = np.linspace(caps_arr.min(), caps_arr.max(), 50)
                        ax.plot(x_line, m * x_line + b,
                                color=color, linewidth=1.8, zorder=2)

            ax.set_xlim(xlim)
            ax.set_ylim(ylim)
            ax.tick_params(labelsize=7)
            ax.grid(False)

            # Row label (benchmark) on leftmost column
            if ei == 0:
                ax.set_ylabel(bench.replace("_", " ").title(),
                              fontsize=9, fontweight="bold")
            # Column label (experiment) on top row
            if bi == 0:
                ax.set_title(d["label"], fontweight="bold", fontsize=10)

            if bi == N_bench - 1:
                ax.set_xlabel("True Capability", fontsize=8)

    # Provider legend at bottom
    handles = [mpatches.Patch(color=provider_colors.get(p, "#888888"), label=p)
               for p in all_providers]
    fig.legend(handles=handles, loc="lower center",
               bbox_to_anchor=(0.5, -0.02),
               ncol=min(6, len(handles)), fontsize=9, frameon=True)

    fig.tight_layout(rect=[0, 0.05, 1, 0.95])
    _save(fig, "D_provider_regression.png")


# ===========================================================================
# Slope extraction helper
# ===========================================================================

def extract_slopes(all_data):
    """
    Returns slopes[(exp_label, provider, benchmark)] = OLS slope, or None if
    insufficient data. Also returns bench_exploitability[(exp_label, benchmark)]
    = mean exploitability of that benchmark across rounds it was active.
    """
    bench_union = []
    seen = set()
    for d in all_data:
        for b in all_benchmarks(d["history"]):
            if b not in seen:
                bench_union.append(b)
                seen.add(b)

    all_providers = []
    seen_p = set()
    for d in all_data:
        for p in get_providers(d["history"]):
            if p not in seen_p:
                all_providers.append(p)
                seen_p.add(p)

    slopes = {}
    bench_exploitability = {}

    for d in all_data:
        label   = d["label"]
        history = d["history"]

        # Exploitability: mean over active rounds
        exp_acc, exp_cnt = {}, {}
        for h in history:
            for b, params in h.get("benchmark_params", {}).items():
                exp_acc[b] = exp_acc.get(b, 0.0) + params.get("exploitability", 0.0)
                exp_cnt[b] = exp_cnt.get(b, 0) + 1
        for b in exp_acc:
            bench_exploitability[(label, b)] = exp_acc[b] / exp_cnt[b]

        # OLS slope per (provider, benchmark)
        for bench in bench_union:
            provider_xy = {}
            for h in history:
                pbs  = h.get("per_benchmark_scores", {}).get(bench, {})
                caps = h.get("true_capabilities", {})
                for p, score in pbs.items():
                    if p in caps:
                        provider_xy.setdefault(p, ([], []))
                        provider_xy[p][0].append(caps[p])
                        provider_xy[p][1].append(score)

            for p, (xs, ys) in provider_xy.items():
                xa = np.array(xs)
                ya = np.array(ys)
                if len(np.unique(xa)) >= 2:
                    m, _ = np.polyfit(xa, ya, 1)
                    slopes[(label, p, bench)] = m
                else:
                    slopes[(label, p, bench)] = None

    return slopes, bench_exploitability, bench_union, all_providers


# ===========================================================================
# Plot E1 — Slope Heatmap (provider × benchmark, one per experiment)
# ===========================================================================

def plot_e1_slope_heatmap(all_data):
    slopes, _, bench_union, all_providers = extract_slopes(all_data)
    if not bench_union:
        return

    # Provider display order
    ordered_providers = [p for p in (CORE_PROVIDERS + [
        p for p in all_providers if p not in CORE_PROVIDERS
    ]) if p in all_providers]

    N_exp = len(all_data)
    vmax  = 3.0   # slope range: centre at 1, show 0-4ish
    vmin  = 0.0

    fig, axes = plt.subplots(N_exp, 1,
                             figsize=(min(6.75, max(3.25, len(bench_union) * 0.45)),
                                      1.2 * N_exp + 0.5),
                             squeeze=False)
    fig.suptitle("OLS Slope Heatmap: Score ~ True Capability\n"
                 "(slope=1 tracks capability; <1 compressed/gamed; >1 amplified)",
                 fontweight="bold", fontsize=13)

    for ei, d in enumerate(all_data):
        ax  = axes[ei][0]
        mat = np.full((len(ordered_providers), len(bench_union)), np.nan)
        for pi, p in enumerate(ordered_providers):
            for bi, b in enumerate(bench_union):
                s = slopes.get((d["label"], p, b))
                if s is not None:
                    mat[pi, bi] = s

        im = ax.imshow(mat, aspect="auto", cmap="RdBu",
                       vmin=vmin, vmax=vmax, interpolation="nearest")

        ax.set_yticks(range(len(ordered_providers)))
        ax.set_yticklabels(ordered_providers, fontsize=8)
        ax.set_xticks(range(len(bench_union)))
        ax.set_xticklabels([b.replace("_", "\n") for b in bench_union],
                           fontsize=7, ha="center")
        ax.set_title(d["label"], fontweight="bold", fontsize=10, loc="left")
        ax.tick_params(length=0)

        for pi in range(len(ordered_providers)):
            for bi in range(len(bench_union)):
                v = mat[pi, bi]
                if not np.isnan(v):
                    ax.text(bi, pi, f"{v:.2f}", ha="center", va="center",
                            fontsize=6.5,
                            color="white" if (v < 0.5 or v > 2.5) else "black")

    cb = fig.colorbar(im, ax=axes[:, 0], fraction=0.02, pad=0.02)
    cb.set_label("Slope", fontsize=9)
    cb.ax.axhline(1.0, color="black", linewidth=1.0)  # mark slope=1
    cb.ax.tick_params(labelsize=8)

    fig.subplots_adjust(top=0.88, bottom=0.05, left=0.14, right=0.91, hspace=0.45)
    _save(fig, "E1_slope_heatmap.png")


# ===========================================================================
# Plot E2 — Slope vs Exploitability Scatter
# ===========================================================================

def plot_e2_slope_vs_exploitability(all_data):
    slopes, bench_exploit, bench_union, all_providers = extract_slopes(all_data)
    provider_colors = get_provider_colors(all_providers)

    N_exp = len(all_data)
    n_cols = min(N_exp, 3)
    n_rows = ceil(N_exp / n_cols)

    fig, axes = plt.subplots(n_rows, n_cols,
                             figsize=(2.25 * n_cols, 2.0 * n_rows),
                             squeeze=False)
    fig.suptitle("OLS Slope vs. Benchmark Exploitability\n"
                 "(tests whether high-exploitability benchmarks decouple scores from capability)",
                 fontweight="bold", fontsize=13)

    for ei, d in enumerate(all_data):
        row, col = divmod(ei, n_cols)
        ax = axes[row][col]
        label = d["label"]

        xs_all, ys_all = [], []
        for p in all_providers:
            for b in bench_union:
                s    = slopes.get((label, p, b))
                expl = bench_exploit.get((label, b))
                if s is None or expl is None:
                    continue
                color = provider_colors.get(p, "#888888")
                ax.scatter(expl, s, color=color, s=40, alpha=0.8,
                           edgecolors="black", linewidth=0.4, zorder=2)
                xs_all.append(expl)
                ys_all.append(s)

        # Overall trend line
        if len(xs_all) >= 2:
            m, b_int = np.polyfit(xs_all, ys_all, 1)
            xs_lin = np.linspace(min(xs_all), max(xs_all), 50)
            ax.plot(xs_lin, m * xs_lin + b_int, color="black",
                    linewidth=1.4, linestyle="--", alpha=0.6, zorder=1)

        ax.axhline(1.0, color="gray", linewidth=0.8, linestyle=":", alpha=0.5)
        ax.set_title(label, fontweight="bold", fontsize=10)
        ax.set_xlabel("Benchmark Exploitability", fontsize=9)
        ax.set_ylabel("OLS Slope", fontsize=9)
        ax.tick_params(labelsize=8)
        ax.grid(False)

    for ei in range(N_exp, n_rows * n_cols):
        row, col = divmod(ei, n_cols)
        axes[row][col].set_visible(False)

    handles = [mpatches.Patch(color=provider_colors.get(p, "#888888"), label=p)
               for p in all_providers]
    fig.legend(handles=handles, loc="lower center",
               bbox_to_anchor=(0.5, -0.02),
               ncol=min(6, len(handles)), fontsize=9, frameon=True)

    fig.tight_layout(rect=[0, 0.06, 1, 0.93])
    _save(fig, "E2_slope_vs_exploitability.png")


# ===========================================================================
# Plot E3 — Slope Bump Chart Across Experiments
# ===========================================================================
# X = experiments (discrete), Y = slope. One line per (provider, benchmark)
# pair. Reveals which pairs shift most between conditions.
# Faceted by benchmark (one panel per benchmark) to avoid overplotting.

def plot_e3_slope_bump(all_data):
    slopes, _, bench_union, all_providers = extract_slopes(all_data)
    provider_colors = get_provider_colors(all_providers)

    N_bench = len(bench_union)
    if N_bench == 0:
        return

    n_cols = min(N_bench, 4)
    n_rows = ceil(N_bench / n_cols)
    exp_labels = [d["label"] for d in all_data]
    x_pos = list(range(len(all_data)))

    fig, axes = plt.subplots(n_rows, n_cols,
                             figsize=(2.25 * n_cols, 1.75 * n_rows),
                             squeeze=False)
    fig.suptitle("Slope Bump Chart Across Experimental Conditions\n"
                 "(each line = one provider; tracks whether slope shifts between conditions)",
                 fontweight="bold", fontsize=13)

    for bi, bench in enumerate(bench_union):
        row, col = divmod(bi, n_cols)
        ax = axes[row][col]

        ax.axhline(1.0, color="gray", linewidth=0.8, linestyle=":", alpha=0.5)

        for p in all_providers:
            ys = [slopes.get((d["label"], p, bench)) for d in all_data]
            # Only draw if provider has slopes in at least 2 experiments
            valid_pairs = [(x, y) for x, y in zip(x_pos, ys) if y is not None]
            if len(valid_pairs) < 2:
                continue
            vx, vy = zip(*valid_pairs)
            color = provider_colors.get(p, "#888888")
            ax.plot(vx, vy, marker="o", markersize=5, linewidth=1.6,
                    color=color, label=p, alpha=0.85)

        ax.set_xticks(x_pos)
        ax.set_xticklabels(exp_labels, fontsize=7, rotation=15, ha="right")
        ax.set_title(bench.replace("_", " ").title(),
                     fontweight="bold", fontsize=10)
        ax.set_ylabel("OLS Slope", fontsize=9)
        ax.tick_params(labelsize=8)
        ax.grid(False)

    for bi in range(N_bench, n_rows * n_cols):
        row, col = divmod(bi, n_cols)
        axes[row][col].set_visible(False)

    handles = [mpatches.Patch(color=provider_colors.get(p, "#888888"), label=p)
               for p in all_providers]
    fig.legend(handles=handles, loc="lower center",
               bbox_to_anchor=(0.5, -0.02),
               ncol=min(6, len(handles)), fontsize=9, frameon=True)

    fig.tight_layout(rect=[0, 0.06, 1, 0.93])
    _save(fig, "E3_slope_bump.png")


# ===========================================================================
# Plot F — Slope vs Intercept Scatter (2D gaming decomposition)
# ===========================================================================
# x = OLS intercept (floor bias: unconditional score inflation)
# y = OLS slope     (amplification: proportional distortion of capability signal)
# One point per (benchmark × experiment). Color = experiment, marker = benchmark.
# Quadrant annotations clarify gaming flavour.
# Reference lines: slope=1 (perfect tracking), intercept=0 (no bias).

_BENCH_MARKERS = ["o", "s", "^", "D", "v", "P", "*", "X", "h", "p"]


def plot_f_slope_intercept(all_data):
    bench_union = []
    seen = set()
    for d in all_data:
        for b in all_benchmarks(d["history"]):
            if b not in seen:
                bench_union.append(b)
                seen.add(b)

    if not bench_union:
        return

    colors = exp_colors(len(all_data))
    marker_map = {b: _BENCH_MARKERS[i % len(_BENCH_MARKERS)]
                  for i, b in enumerate(bench_union)}

    fig, ax = plt.subplots(figsize=(3.25, 2.9))
    fig.suptitle(
        "Gaming Decomposition: Slope vs. Intercept\n"
        "(intercept = floor bias; slope = capability amplification)",
        fontweight="bold", fontsize=12,
    )

    for d, color in zip(all_data, colors):
        history = d["history"]
        for bench in bench_union:
            xs, ys = [], []
            caps_list, scores_list = [], []
            for h in history:
                pbs  = h.get("per_benchmark_scores", {}).get(bench, {})
                caps = h.get("true_capabilities", {})
                for p, score in pbs.items():
                    if p in caps:
                        caps_list.append(caps[p])
                        scores_list.append(score)
            if len(np.unique(caps_list)) < 2:
                continue
            slope, intercept = np.polyfit(caps_list, scores_list, 1)
            ax.scatter(intercept, slope,
                       color=color, marker=marker_map[bench],
                       s=70, alpha=0.85, linewidths=0.5,
                       edgecolors="black", zorder=3)

    # Reference lines
    ax.axhline(1.0, color="gray", linewidth=0.9, linestyle="--", alpha=0.6, zorder=1)
    ax.axvline(0.0, color="gray", linewidth=0.9, linestyle="--", alpha=0.6, zorder=1)

    # Quadrant labels (placed at corners)
    quad_kw = dict(fontsize=7.5, color="#555555", ha="center", va="center",
                   style="italic")
    xlims = ax.get_xlim()
    ylims = ax.get_ylim()
    # Use fixed fractions of the visible range — set after data plotted
    ax.set_xlim(left=min(-0.05, ax.get_xlim()[0] - 0.02))

    def _qtext(x_frac, y_frac, text):
        xl, xr = ax.get_xlim()
        yb, yt = ax.get_ylim()
        ax.text(xl + x_frac * (xr - xl), yb + y_frac * (yt - yb),
                text, **quad_kw)

    _qtext(0.25, 0.92, "floor bias\nlow amplification")
    _qtext(0.75, 0.92, "floor bias\n+ amplification")
    _qtext(0.25, 0.08, "well-calibrated\n(low gaming)")
    _qtext(0.75, 0.08, "amplification\nno floor bias")

    ax.set_xlabel("Intercept (floor bias)", fontsize=10)
    ax.set_ylabel("Slope (amplification)", fontsize=10)
    ax.tick_params(labelsize=8)
    ax.grid(False)

    # Legend: experiments (color patches)
    exp_handles = [mpatches.Patch(color=c, label=d["label"])
                   for d, c in zip(all_data, colors)]
    # Legend: benchmarks (marker lines)
    bench_handles = [mlines.Line2D([], [], color="gray",
                                   marker=marker_map[b], markersize=6,
                                   linewidth=0, label=b.replace("_", " ").title())
                     for b in bench_union]
    # Experiments legend: above the plot
    leg1 = fig.legend(handles=exp_handles,
                      loc="upper center", bbox_to_anchor=(0.5, 1.0),
                      ncol=min(4, len(exp_handles)),
                      fontsize=8, frameon=True,
                      title="Experiment", title_fontsize=8)
    # Benchmarks legend: below the plot
    fig.legend(handles=bench_handles,
               loc="lower center", bbox_to_anchor=(0.5, 0.0),
               ncol=min(4, len(bench_handles)),
               fontsize=8, frameon=True,
               title="Benchmark", title_fontsize=8)

    fig.tight_layout(rect=[0, 0.10, 1, 0.88])
    _save(fig, "F_slope_intercept.png")


# ===========================================================================
# Plot G — Aggregate Inflation Accumulation
# ===========================================================================
# x = round, y = mean inflation (score - capability) across all active
# benchmarks and all providers. One line per experiment.
# Shows that gaming is universal, monotone, and the ablation lines fan apart.

def plot_g_inflation_accumulation(all_data):
    colors = exp_colors(len(all_data))

    fig, ax = plt.subplots(figsize=(3.25, 2.1))
    fig.suptitle(
        "Aggregate Score Inflation Over Time\n"
        r"(mean score $-$ true capability across all benchmarks and providers)",
        fontweight="bold", fontsize=12,
    )

    for d, color in zip(all_data, colors):
        history = d["history"]
        rounds, means = [], []
        for h in history:
            pbs  = h.get("per_benchmark_scores", {})
            caps = h.get("true_capabilities", {})
            vals = []
            for bench_scores in pbs.values():
                for p, score in bench_scores.items():
                    if p in caps:
                        vals.append(score - caps[p])
            if vals:
                rounds.append(h["round"])
                means.append(np.mean(vals))
        if rounds:
            ax.plot(rounds, means, linewidth=1.8, color=color,
                    label=d["label"], alpha=0.9)

    ax.axhline(0, color="black", linewidth=0.7, alpha=0.3)
    ax.set_xlabel("Round", fontsize=10)
    ax.set_ylabel("Mean Score Inflation", fontsize=10)
    ax.tick_params(labelsize=8)
    ax.grid(False)

    ax.legend(loc="upper left", fontsize=8, frameon=True,
              ncol=max(1, len(all_data) // 6))

    fig.tight_layout(rect=[0, 0, 1, 0.92])
    _save(fig, "G_inflation_accumulation.png")


# ===========================================================================
# Plot H — Validity vs Inflation Tradeoff (per-experiment summary)
# ===========================================================================
# x = late-period mean inflation (last 10 rounds)
# y = late-period validity: Pearson r(per_benchmark_score, true_capability)
# One labeled point per experiment.
# Reveals which conditions successfully decouple validity from inflation.

def plot_h_validity_vs_inflation(all_data):
    colors = exp_colors(len(all_data))

    fig, ax = plt.subplots(figsize=(3.25, 2.5))
    fig.suptitle(
        "Late-Period Validity vs. Inflation Tradeoff\n"
        "(each point = one experiment; last 10 rounds; ideal = upper-left)",
        fontweight="bold", fontsize=12,
    )

    xs, ys, labels_pts, cols = [], [], [], []
    for d, color in zip(all_data, colors):
        history = d["history"]
        late = history[-10:] if len(history) >= 10 else history

        # Mean inflation
        inf_vals = []
        caps_all, scores_all = [], []
        for h in late:
            pbs  = h.get("per_benchmark_scores", {})
            caps = h.get("true_capabilities", {})
            for bench_scores in pbs.values():
                for p, score in bench_scores.items():
                    if p in caps:
                        inf_vals.append(score - caps[p])
                        caps_all.append(caps[p])
                        scores_all.append(score)

        mean_inf = np.mean(inf_vals) if inf_vals else float("nan")
        r = (np.corrcoef(caps_all, scores_all)[0, 1]
             if len(caps_all) > 1 else float("nan"))

        if not (np.isnan(mean_inf) or np.isnan(r)):
            xs.append(mean_inf)
            ys.append(r)
            labels_pts.append(d["label"])
            cols.append(color)

    for x, y, label, color in zip(xs, ys, labels_pts, cols):
        ax.scatter(x, y, color=color, s=90, zorder=3,
                   edgecolors="black", linewidths=0.5)
        ax.annotate(label, (x, y),
                    textcoords="offset points", xytext=(6, 4),
                    fontsize=7.5, color=color)

    # Quadrant shading
    if xs and ys:
        xm = np.median(xs)
        ym = np.median(ys)
        xl, xr = ax.get_xlim()
        yb, yt = ax.get_ylim()
        pad_x = (xr - xl) * 0.05
        pad_y = (yt - yb) * 0.05
        ax.axhline(ym, color="gray", linewidth=0.6, linestyle=":", alpha=0.5)
        ax.axvline(xm, color="gray", linewidth=0.6, linestyle=":", alpha=0.5)
        quad_kw = dict(fontsize=7, color="#777777", style="italic", ha="center")
        ax.text(xl + (xm - xl) / 2, yt - pad_y, "low inflation\nhigh validity\n(ideal)",
                va="top", **quad_kw)
        ax.text(xr - (xr - xm) / 2, yt - pad_y, "high inflation\nhigh validity",
                va="top", **quad_kw)
        ax.text(xl + (xm - xl) / 2, yb + pad_y, "low inflation\nlow validity",
                va="bottom", **quad_kw)
        ax.text(xr - (xr - xm) / 2, yb + pad_y, "high inflation\nlow validity\n(worst)",
                va="bottom", **quad_kw)

    ax.set_xlabel("Mean Score Inflation (last 10 rounds)", fontsize=10)
    ax.set_ylabel("Validity: Pearson r(score, capability)", fontsize=10)
    ax.tick_params(labelsize=8)
    ax.grid(False)

    fig.tight_layout(rect=[0, 0, 1, 0.92])
    _save(fig, "H_validity_vs_inflation.png")


# ===========================================================================
# Helpers
# ===========================================================================

def _save(fig, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved: {path}")


def _folder_to_label(folder_name):
    import re
    name = re.sub(r"^exp_\d+_", "", folder_name)
    for token in ("ablation_", "_balanced", "_ablation"):
        name = name.replace(token, "")
    label = name.strip("_").replace("_", " ").title()
    for acronym in ("Us", "Eu", "Llm", "Ai"):
        label = label.replace(acronym, acronym.upper())
    return label


def _resolve_experiment_id(num):
    import re
    target = f"{num:03d}"
    for name in sorted(os.listdir(EXPERIMENTS_DIR)):
        m = re.match(r"exp_(\d+)_", name)
        if m and m.group(1) == target:
            return {"id": name, "label": _folder_to_label(name)}
    raise ValueError(f"No experiment matching exp_{target}_* in {EXPERIMENTS_DIR}/")


def _parse_args():
    args = sys.argv[1:]
    if not args:
        return None, None
    numbers, folder_name = [], None
    for token in args:
        if token.lstrip("-").isdigit():
            numbers.append(int(token))
        else:
            folder_name = token
    if not numbers:
        return None, None
    return [_resolve_experiment_id(n) for n in numbers], folder_name


# ===========================================================================
# Main
# ===========================================================================

def main():
    global OUTPUT_DIR, EXPERIMENTS

    cli_experiments, cli_folder = _parse_args()
    if cli_experiments is not None:
        EXPERIMENTS = cli_experiments

    import re
    if cli_folder:
        OUTPUT_DIR = os.path.join(_PROJECT_ROOT, "output", "explore-benchmark-plots", cli_folder)
    else:
        numbers = [m.group(1) for e in EXPERIMENTS
                   for m in [re.match(r"exp_(\d+)", e["id"])] if m]
        OUTPUT_DIR = os.path.join(_PROJECT_ROOT, "output", "explore-benchmark-plots",
                                  "_".join(numbers) if numbers else "custom")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output directory: {OUTPUT_DIR}")

    all_data = []
    for exp in EXPERIMENTS:
        hist = load_history(exp["id"])
        all_data.append({"label": exp["label"], "history": hist})

    loaded = sum(1 for d in all_data if d["history"])
    print(f"Loaded {loaded}/{len(all_data)} experiments\n")

    valid = [d for d in all_data if d["history"]]

    print("Plot A: Score inflation trajectories...")
    plot_a_inflation_trajectories(valid)

    print("Plot B: Gaming fingerprint heatmap...")
    plot_b_gaming_fingerprint(valid)

    print("Plot C: Per-benchmark rolling validity...")
    plot_c_rolling_validity(valid)

    print("Plot D: Per-provider regression lines...")
    plot_d_provider_regression(valid)

    print("Plot E1: Slope heatmap...")
    plot_e1_slope_heatmap(valid)

    print("Plot E2: Slope vs exploitability...")
    plot_e2_slope_vs_exploitability(valid)

    print("Plot E3: Slope bump chart...")
    plot_e3_slope_bump(valid)

    print("Plot F: Slope vs intercept scatter...")
    plot_f_slope_intercept(valid)

    print("Plot G: Aggregate inflation accumulation...")
    plot_g_inflation_accumulation(valid)

    print("Plot H: Validity vs inflation tradeoff...")
    plot_h_validity_vs_inflation(valid)

    print(f"\nDone. Output: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
