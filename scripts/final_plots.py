"""
final_plots.py — Combined comparison + benchmark plots

Combines create_final_plots.py and selected plots from explore_benchmark_plots.py.

Plots generated:
  1. market_share_comparison     — stacked-area market share per experiment
  2. score_vs_capability         — score vs ground-truth capability scatter
  3. incident_validity_combined  — incident timeline + validity/interventions
  4. investment_allocation       — provider R&D portfolio over rounds
  5. strategy_divergence         — mean pairwise L1 distance between strategies
  C. C_rolling_validity          — per-benchmark rolling Pearson r (window=5)
  F. F_slope_intercept           — gaming decomposition: slope vs intercept
  H. H_validity_vs_inflation     — late-period validity vs inflation tradeoff

CSV tables:
  safety_investment.csv
  consumer_satisfaction.csv
  incident_counts.csv

Usage:
  python final_plots.py                  # use EXPERIMENTS list below
  python final_plots.py 3 2             # resolve by experiment number, auto folder
  python final_plots.py 3 2 my_run      # resolve by number, named output folder
"""

import os
import sys
import json
import csv
import re
import warnings
from math import ceil

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib as mpl
import numpy as np

# Add src/ to path
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_PROJECT_ROOT, "src"))

# ---------------------------------------------------------------------------
# Tueplots NeurIPS styling
# ---------------------------------------------------------------------------
try:
    from tueplots import bundles as _tueplots_bundles
    _NEURIPS_RC = _tueplots_bundles.neurips2024()
    _NEURIPS_RC.pop("figure.figsize", None)
    if os.environ.get("MPLLATEX", "1") != "0":
        _NEURIPS_RC["text.usetex"] = True
    mpl.rcParams.update(_NEURIPS_RC)
except ImportError:
    warnings.warn("tueplots not installed — using default matplotlib style.", stacklevel=1)

from plotting import (
    get_providers,
    get_provider_colors,
    get_investment_colors,
    compute_rolling_correlation,
    PROVIDER_COLOR_MAP,
)

# ===========================================================================
# CONFIGURATION
# ===========================================================================
EXPERIMENTS = [
    {"id": "exp_003_full_ecosystem_us", "label": "US Baseline"},
    {"id": "exp_002_full_ecosystem_eu", "label": "EU Baseline"},
    # {"id": "exp_004_ablation_no_media_balanced",      "label": "No Media"},
    # {"id": "exp_005_ablation_no_incidents_balanced",  "label": "No Incidents"},
    # {"id": "exp_006_ablation_no_startups_balanced",   "label": "No Startups"},
    # {"id": "exp_007_ablation_no_opencore_balanced",   "label": "No OpenCore"},
]

OUTPUT_DIR      = os.path.join(_PROJECT_ROOT, "output", "final-plots")
EXPERIMENTS_DIR = os.path.join(_PROJECT_ROOT, "output", "experiments")

MAX_COLS = 4

INVESTMENT_TYPES = [
    "fundamental_research",
    "training_optimization",
    "evaluation_engineering",
    "safety_alignment",
]

CORE_PROVIDERS = [
    "Orion Labs",
    "Apex AI",
    "Genesis Systems",
    "Mirage AI",
    "OpenCore",
]

_BENCH_MARKERS = ["o", "s", "^", "D", "v", "P", "*", "X", "h", "p"]

SEVERITY_MARKERS = {"minor": "o", "moderate": "s", "major": "^", "critical": "X"}
SEVERITY_SIZES   = {"minor": 30,  "moderate": 60,  "major": 100, "critical": 150}

# ===========================================================================
# Helpers
# ===========================================================================

def _figsize(rows, cols, base_w=2.25, base_h=1.7):
    return (base_w * cols, base_h * rows)


def _save(fig, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved: {path}")


def load_history(exp_id):
    path = os.path.join(EXPERIMENTS_DIR, exp_id, "history.json")
    if not os.path.exists(path):
        warnings.warn(f"history.json not found for {exp_id} — skipping")
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_all_histories():
    result = []
    for exp in EXPERIMENTS:
        hist = load_history(exp["id"])
        result.append({"label": exp["label"], "history": hist if hist else []})
    return result


def collect_incidents(history):
    result = []
    for h in history:
        for inc in (h.get("incidents") or []):
            result.append({
                "round":    h["round"],
                "provider": inc.get("provider", "Unknown"),
                "severity": inc.get("severity", "minor"),
                "category": inc.get("category", ""),
            })
    return result


def exp_colors(n):
    return plt.cm.tab10(np.linspace(0, 0.9, n))


# ---------------------------------------------------------------------------
# Benchmark helpers (used by plots C and F)
# ---------------------------------------------------------------------------

def all_benchmarks(history):
    """Benchmarks ordered by first appearance round."""
    seen = {}
    for h in history:
        for b in h.get("per_benchmark_scores", {}):
            if b not in seen:
                seen[b] = h["round"]
    return sorted(seen, key=seen.get)


def rolling_bench_correlation(history, benchmark, window=5):
    """Rolling Pearson r between per_benchmark_score and true_capability."""
    active = [
        (h["round"], h["per_benchmark_scores"][benchmark], h["true_capabilities"])
        for h in history
        if benchmark in h.get("per_benchmark_scores", {})
    ]
    if len(active) < window:
        return [], []
    rounds_out, corrs = [], []
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


# ---------------------------------------------------------------------------
# Provider order helper (used by plot 4)
# ---------------------------------------------------------------------------

def _provider_order(all_data):
    startup_seen = {}
    for d in all_data:
        for h in d["history"]:
            for p in h.get("strategies", {}):
                if p not in CORE_PROVIDERS and p not in startup_seen:
                    startup_seen[p] = h["round"]
    first_startup = sorted(startup_seen, key=startup_seen.get)[:1]
    return first_startup + list(reversed(CORE_PROVIDERS))


# ===========================================================================
# Plot 1 — Market Share
# ===========================================================================

def plot_market_share(all_data):
    N = len(all_data)
    if N == 0:
        return
    n_cols = min(N, 3)
    n_rows = ceil(N / n_cols)
    fig, axes = plt.subplots(n_rows, n_cols, figsize=_figsize(n_rows, n_cols), squeeze=False)
    fig.suptitle("Provider Market Share Dynamics Across Experimental Conditions",
                 fontweight="bold", fontsize=13)

    for idx, entry in enumerate(all_data):
        row, col = divmod(idx, n_cols)
        ax = axes[row][col]
        label, history = entry["label"], entry["history"]

        if not history:
            ax.set_title(label, fontweight="bold")
            ax.text(0.5, 0.5, "No data", transform=ax.transAxes, ha="center", va="center", color="gray")
            continue

        if not any(h.get("consumer_data", {}).get("market_shares") for h in history):
            ax.set_title(label, fontweight="bold")
            ax.text(0.5, 0.5, "No consumer data", transform=ax.transAxes, ha="center", va="center", color="gray")
            continue

        providers = get_providers(history)
        colors    = get_provider_colors(providers)
        rounds    = [h["round"] for h in history]

        shares = {p: [] for p in providers}
        for h in history:
            ms    = h.get("consumer_data", {}).get("market_shares", {})
            total = sum(ms.values()) if ms else 0
            for p in providers:
                shares[p].append(ms.get(p, 0) / total if total > 0 else 0)

        bottoms = np.zeros(len(rounds))
        for p in providers:
            vals = np.array(shares[p])
            ax.fill_between(rounds, bottoms, bottoms + vals, color=colors[p], alpha=0.8, label=p)
            bottoms += vals

        ax.set_ylim(0, 1)
        ax.set_title(label, fontweight="bold", fontsize=11)
        ax.set_xlabel("Simulation Round", fontsize=10)
        ax.set_ylabel("Market Share", fontsize=10)
        ax.tick_params(labelsize=9)
        ax.grid(False)

    for idx in range(N, n_rows * n_cols):
        row, col = divmod(idx, n_cols)
        axes[row][col].set_visible(False)

    handles = [mpatches.Patch(color=PROVIDER_COLOR_MAP.get(p, "#666666"), label=p)
               for p in PROVIDER_COLOR_MAP]
    fig.legend(handles=handles, loc="lower center", ncol=min(5, len(handles)),
               bbox_to_anchor=(0.5, -0.02), frameon=True)
    fig.tight_layout()
    _save(fig, "market_share_comparison.png")


# ===========================================================================
# Plot 2 — Score vs True Capability
# ===========================================================================

def plot_score_vs_capability(all_data):
    N = len(all_data)
    if N == 0:
        return
    n_cols = min(N, 3)
    n_rows = ceil(N / n_cols)
    fig, axes = plt.subplots(n_rows, n_cols, figsize=_figsize(n_rows, n_cols), squeeze=False)
    fig.suptitle("Benchmark Score vs. Ground-Truth Capability Across Experimental Conditions",
                 fontweight="bold", fontsize=13)

    for idx, entry in enumerate(all_data):
        row, col = divmod(idx, n_cols)
        ax = axes[row][col]
        label, history = entry["label"], entry["history"]

        if not history:
            ax.set_title(label, fontweight="bold")
            ax.text(0.5, 0.5, "No data", transform=ax.transAxes, ha="center", va="center", color="gray")
            continue

        providers = get_providers(history)
        colors    = get_provider_colors(providers)
        all_s, all_c = [], []

        for p in providers:
            s = [h["scores"][p] for h in history if p in h.get("scores", {})]
            c = [h["true_capabilities"][p] for h in history if p in h.get("true_capabilities", {})]
            n = min(len(s), len(c))
            if n == 0:
                continue
            ax.scatter(c[:n], s[:n], color=colors[p], alpha=0.5, s=15, label=p)
            all_s.extend(s[:n]); all_c.extend(c[:n])

        if all_c:
            mn, mx = min(all_c), max(all_c)
            ax.plot([mn, mx], [mn, mx], "k--", alpha=0.3)

        corr_str = f"  (r = {np.corrcoef(all_s, all_c)[0,1]:.2f})" if len(all_s) >= 2 else ""
        ax.set_title(label + corr_str, fontweight="bold", fontsize=11)
        ax.set_xlabel("Ground-Truth Capability", fontsize=10)
        ax.set_ylabel("Benchmark Score", fontsize=10)
        ax.tick_params(labelsize=9)
        ax.grid(False)

    for idx in range(N, n_rows * n_cols):
        row, col = divmod(idx, n_cols)
        axes[row][col].set_visible(False)

    all_providers, seen = [], set()
    for entry in all_data:
        for p in get_providers(entry["history"]):
            if p not in seen:
                all_providers.append(p); seen.add(p)
    colors_all = get_provider_colors(all_providers)
    handles = [mpatches.Patch(color=colors_all[p], label=p) for p in all_providers]
    if handles:
        fig.legend(handles=handles, loc="lower center", ncol=min(5, len(handles)),
                   bbox_to_anchor=(0.5, -0.06), frameon=True)
    fig.tight_layout()
    _save(fig, "score_vs_capability.png")


# ===========================================================================
# Plot 3 — Incident Timeline + Validity (dual y-axis)
# ===========================================================================

def plot_incident_validity_combined(all_data):
    N = len(all_data)
    if N == 0:
        return

    fig, axes = plt.subplots(N, 1, figsize=(6.75, 1.7 * N), squeeze=False)
    fig.suptitle("Safety Incident Timeline and Benchmark Validity Across Experimental Conditions",
                 fontweight="bold", fontsize=13)

    for idx, entry in enumerate(all_data):
        ax_l = axes[idx][0]
        label, history = entry["label"], entry["history"]
        ax_l.set_title(label, fontweight="bold", fontsize=11)

        if not history:
            ax_l.text(0.5, 0.5, "No data", transform=ax_l.transAxes, ha="center", va="center", color="gray")
            ax_l.set_yticks([])
            continue

        providers       = get_providers(history)
        provider_colors = get_provider_colors(providers)
        rounds          = [h["round"] for h in history]
        incidents       = collect_incidents(history)

        if incidents and providers:
            for inc in incidents:
                if inc["provider"] not in providers:
                    continue
                ax_l.scatter(
                    inc["round"], providers.index(inc["provider"]),
                    marker=SEVERITY_MARKERS.get(inc["severity"], "o"),
                    s=SEVERITY_SIZES.get(inc["severity"], 30),
                    color=provider_colors.get(inc["provider"], "#666666"),
                    alpha=0.7, edgecolors="black", linewidth=0.5, zorder=3,
                )

        if providers:
            ax_l.set_yticks(range(len(providers)))
            ax_l.set_yticklabels(providers, fontsize=9)
        else:
            ax_l.set_yticks([])

        if rounds:
            ax_l.set_xlim(min(rounds) - 1, max(rounds) + 1)
        ax_l.set_xlabel("Simulation Round", fontsize=10)
        ax_l.set_ylabel("Provider", fontsize=10)
        ax_l.tick_params(axis="x", labelsize=9)
        ax_l.grid(False)

        ax_r = ax_l.twinx()
        vr, vv = compute_rolling_correlation(history)
        if vv:
            ax_r.plot(vr, vv, "o-", color="#457B9D", markersize=3, linewidth=1.5, zorder=2)
        for h in history:
            if h.get("policymaker_data", {}).get("interventions"):
                ax_r.axvline(x=h["round"], color="#E63946", linestyle="--", alpha=0.5, linewidth=0.8)
        ax_r.set_ylim(-0.1, 1.1)
        ax_r.set_ylabel("Validity Correlation", fontsize=10)
        ax_r.tick_params(axis="y", labelsize=9)

    sev_handles = [
        mlines.Line2D([0], [0], marker=m, color="w", markerfacecolor="gray",
                      markeredgecolor="black", markersize=ms, label=sev.capitalize())
        for sev, (m, ms) in {"minor": ("o", 7), "moderate": ("s", 9),
                              "major": ("^", 11), "critical": ("X", 13)}.items()
    ]
    all_providers, seen = [], set()
    for entry in all_data:
        for p in get_providers(entry["history"]):
            if p not in seen:
                all_providers.append(p); seen.add(p)
    pc = get_provider_colors(all_providers)
    prov_handles = [mpatches.Patch(color=pc[p], label=p) for p in all_providers]
    all_handles = ([mpatches.Patch(color="none", label="Severity:")] + sev_handles +
                   [mpatches.Patch(color="none", label="Providers:")] + prov_handles)
    fig.legend(handles=all_handles, loc="lower center", bbox_to_anchor=(0.5, -0.06),
               ncol=ceil(len(all_handles) / 2), frameon=True, fontsize=9,
               handlelength=1.5, columnspacing=1.2)
    fig.tight_layout()
    _save(fig, "incident_validity_combined.png")


# ===========================================================================
# Plot 4 — Investment Allocation
# ===========================================================================

def _draw_allocation_panel(ax, rounds, strats, providers, inv_colors, show_ylabel):
    n_providers = len(providers)
    xs = list(range(len(rounds)))

    for p_idx, provider in enumerate(providers):
        slot_bottom = p_idx
        if not any(provider in strats[r] for r in rounds):
            ax.fill_between([-0.5, len(rounds) - 0.5],
                            [slot_bottom, slot_bottom], [slot_bottom+1, slot_bottom+1],
                            color="#E8E8E8", linewidth=0, zorder=0)
            continue
        cum = np.zeros(len(rounds))
        for inv in INVESTMENT_TYPES:
            vals = np.array([strats[r].get(provider, {}).get(inv, 0.0) for r in rounds])
            ax.fill_between(xs, slot_bottom + cum, slot_bottom + cum + vals,
                            color=inv_colors[inv], linewidth=0, alpha=0.9, zorder=1)
            cum += vals

    for i in range(1, n_providers):
        ax.axhline(i, color="black", linewidth=0.6, linestyle=":", zorder=3)

    xtick_pos = [i for i, r in enumerate(rounds) if r % 10 == 0 or r == rounds[0]]
    ax.set_xticks(xtick_pos)
    ax.set_xticklabels([str(rounds[i]) for i in xtick_pos], fontsize=8)
    ax.set_xlabel("Simulation Round", fontsize=9)
    ax.set_xlim(-0.5, len(rounds) - 0.5)
    ax.set_ylim(0, n_providers)
    ax.tick_params(axis="y", length=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    if show_ylabel:
        ax.set_yticks([i + 0.5 for i in range(n_providers)])
        ax.set_yticklabels(providers, fontsize=9)
    else:
        ax.set_yticks([])


def plot_investment_allocation(all_data):
    valid = [d for d in all_data if d["history"]]
    if not valid:
        return

    inv_colors  = get_investment_colors()
    providers   = _provider_order(all_data)
    N           = len(valid)
    n_cols      = min(N, 3)
    n_rows      = ceil(N / n_cols)
    panel_w     = max(2.0, 6.75 / n_cols)
    panel_h     = max(1.7, len(providers) * 0.35 + 0.6)

    fig, axes = plt.subplots(n_rows, n_cols,
                             figsize=(panel_w * n_cols, panel_h * n_rows),
                             squeeze=False)
    fig.suptitle("Provider Investment Allocation Over Simulation Rounds",
                 fontweight="bold", fontsize=13)

    for idx, d in enumerate(valid):
        row, col = divmod(idx, n_cols)
        ax       = axes[row][col]
        history  = d["history"]
        rounds   = [h["round"] for h in history]
        strats   = {h["round"]: h.get("strategies", {}) for h in history}
        _draw_allocation_panel(ax, rounds, strats, providers, inv_colors, col == 0)
        ax.set_title(d["label"], fontweight="bold", fontsize=11)

    for idx in range(N, n_rows * n_cols):
        row, col = divmod(idx, n_cols)
        axes[row][col].set_visible(False)

    fig.legend(
        handles=[mpatches.Patch(color=inv_colors[inv], label=inv.replace("_", " ").title())
                 for inv in INVESTMENT_TYPES],
        loc="lower center", bbox_to_anchor=(0.5, -0.02), ncol=4, fontsize=9, frameon=True,
    )
    fig.tight_layout(rect=[0, 0.06, 1, 0.96])
    _save(fig, "investment_allocation.png")


# ===========================================================================
# Plot 5 — Strategy Divergence
# ===========================================================================

def _mean_pairwise_l1(vectors):
    if len(vectors) < 2:
        return 0.0
    total, count = 0.0, 0
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            total += np.sum(np.abs(vectors[i] - vectors[j]))
            count += 1
    return total / count


def plot_strategy_divergence(all_data):
    valid = [(d["label"], d["history"]) for d in all_data if d["history"]]
    if not valid:
        return

    fig, ax = plt.subplots(figsize=(3.25, 1.86))
    fig.suptitle("Strategic Divergence Among Providers Over Time",
                 fontweight="bold", fontsize=13)

    colors = exp_colors(len(valid))
    for (label, history), color in zip(valid, colors):
        providers = get_providers(history)
        rounds, divs = [], []
        for h in history:
            strats = h.get("strategies", {})
            vecs = [np.array([strats[p].get(inv, 0.0) for inv in INVESTMENT_TYPES])
                    for p in providers if p in strats]
            if len(vecs) >= 2:
                rounds.append(h["round"])
                divs.append(_mean_pairwise_l1(vecs))
        if rounds:
            ax.plot(rounds, divs, marker="o", markersize=3, linewidth=1.8, label=label, color=color)

    ax.set_xlabel("Simulation Round", fontsize=10)
    ax.set_ylabel("Mean Pairwise L1 Distance", fontsize=10)
    ax.tick_params(labelsize=9)
    ax.grid(False)
    ax.legend(fontsize=9, frameon=True)
    ax.text(0.01, 0.97, "Higher = more differentiated strategies",
            transform=ax.transAxes, fontsize=8, va="top", color="gray", style="italic")
    fig.tight_layout()
    _save(fig, "strategy_divergence.png")


# ===========================================================================
# Plot C — Per-Benchmark Rolling Validity
# ===========================================================================

def plot_c_rolling_validity(all_data):
    bench_union, seen = [], set()
    for d in all_data:
        for b in all_benchmarks(d["history"]):
            if b not in seen:
                bench_union.append(b); seen.add(b)
    if not bench_union:
        return

    N      = len(bench_union)
    n_cols = min(N, 4)
    n_rows = ceil(N / n_cols)
    colors = exp_colors(len(all_data))

    fig, axes = plt.subplots(n_rows, n_cols,
                             figsize=(4.5 * n_cols, 3.5 * n_rows),
                             squeeze=False)
    fig.suptitle("Per-Benchmark Rolling Validity\n"
                 r"(Pearson $r$: benchmark score vs true capability, window=5)",
                 fontweight="bold", fontsize=13)

    for bi, bench in enumerate(bench_union):
        row, col = divmod(bi, n_cols)
        ax = axes[row][col]
        for d, color in zip(all_data, colors):
            rounds, corrs = rolling_bench_correlation(d["history"], bench)
            if rounds:
                ax.plot(rounds, corrs, marker="o", markersize=2.5,
                        linewidth=1.5, color=color, label=d["label"])
        ax.axhline(0.7, color="green",  linewidth=0.7, linestyle=":", alpha=0.6)
        ax.axhline(0.5, color="orange", linewidth=0.7, linestyle=":", alpha=0.6)
        ax.axhline(0.3, color="red",    linewidth=0.7, linestyle=":", alpha=0.6)
        ax.set_ylim(-0.1, 1.05)
        ax.set_title(bench.replace("_", " ").title(), fontweight="bold", fontsize=10)
        ax.set_xlabel("Round", fontsize=9)
        ax.set_ylabel("Validity (r)", fontsize=9)
        ax.tick_params(labelsize=8)
        ax.grid(True, alpha=0.25)

    for bi in range(N, n_rows * n_cols):
        row, col = divmod(bi, n_cols)
        axes[row][col].set_visible(False)

    handles = [mlines.Line2D([], [], color=c, linewidth=1.5, label=d["label"])
               for d, c in zip(all_data, colors)]
    handles += [
        mlines.Line2D([], [], color="green",  linestyle=":", label="r=0.7 (good)"),
        mlines.Line2D([], [], color="orange", linestyle=":", label="r=0.5 (moderate)"),
        mlines.Line2D([], [], color="red",    linestyle=":", label="r=0.3 (poor)"),
    ]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.02),
               ncol=min(6, len(handles)), fontsize=9, frameon=True)
    fig.tight_layout(rect=[0, 0.05, 1, 0.95])
    _save(fig, "C_rolling_validity.png")


# ===========================================================================
# Plot F — Slope vs Intercept (gaming decomposition)
# ===========================================================================

def plot_f_slope_intercept(all_data):
    bench_union, seen = [], set()
    for d in all_data:
        for b in all_benchmarks(d["history"]):
            if b not in seen:
                bench_union.append(b); seen.add(b)
    if not bench_union:
        return

    colors     = exp_colors(len(all_data))
    marker_map = {b: _BENCH_MARKERS[i % len(_BENCH_MARKERS)] for i, b in enumerate(bench_union)}

    fig, ax = plt.subplots(figsize=(7, 6))
    fig.suptitle("Gaming Decomposition: Slope vs. Intercept\n"
                 "(intercept = floor bias; slope = capability amplification)",
                 fontweight="bold", fontsize=12)

    for d, color in zip(all_data, colors):
        for bench in bench_union:
            caps_list, scores_list = [], []
            for h in d["history"]:
                pbs  = h.get("per_benchmark_scores", {}).get(bench, {})
                caps = h.get("true_capabilities", {})
                for p, score in pbs.items():
                    if p in caps:
                        caps_list.append(caps[p])
                        scores_list.append(score)
            if len(np.unique(caps_list)) < 2:
                continue
            slope, intercept = np.polyfit(caps_list, scores_list, 1)
            ax.scatter(intercept, slope, color=color, marker=marker_map[bench],
                       s=70, alpha=0.85, linewidths=0.5, edgecolors="black", zorder=3)

    ax.axhline(1.0, color="gray", linewidth=0.9, linestyle="--", alpha=0.6, zorder=1)
    ax.axvline(0.0, color="gray", linewidth=0.9, linestyle="--", alpha=0.6, zorder=1)
    ax.set_xlim(left=min(-0.05, ax.get_xlim()[0] - 0.02))

    quad_kw = dict(fontsize=7.5, color="#555555", ha="center", va="center", style="italic")
    def _qtext(xf, yf, text):
        xl, xr = ax.get_xlim(); yb, yt = ax.get_ylim()
        ax.text(xl + xf*(xr-xl), yb + yf*(yt-yb), text, **quad_kw)
    _qtext(0.25, 0.92, "floor bias\nlow amplification")
    _qtext(0.75, 0.92, "floor bias\n+ amplification")
    _qtext(0.25, 0.08, "well-calibrated\n(low gaming)")
    _qtext(0.75, 0.08, "amplification\nno floor bias")

    ax.set_xlabel("Intercept (floor bias)", fontsize=10)
    ax.set_ylabel("Slope (amplification)", fontsize=10)
    ax.tick_params(labelsize=8)
    ax.grid(True, alpha=0.2)

    fig.legend(
        handles=[mpatches.Patch(color=c, label=d["label"]) for d, c in zip(all_data, colors)],
        loc="upper center", bbox_to_anchor=(0.5, 1.0),
        ncol=min(4, len(all_data)), fontsize=8, frameon=True,
        title="Experiment", title_fontsize=8,
    )
    fig.legend(
        handles=[mlines.Line2D([], [], color="gray", marker=marker_map[b], markersize=6,
                               linewidth=0, label=b.replace("_", " ").title())
                 for b in bench_union],
        loc="lower center", bbox_to_anchor=(0.5, 0.0),
        ncol=min(4, len(bench_union)), fontsize=8, frameon=True,
        title="Benchmark", title_fontsize=8,
    )
    fig.tight_layout(rect=[0, 0.10, 1, 0.88])
    _save(fig, "F_slope_intercept.png")


# ===========================================================================
# Plot H — Late-Period Validity vs Inflation
# ===========================================================================

def plot_h_validity_vs_inflation(all_data):
    colors = exp_colors(len(all_data))

    fig, ax = plt.subplots(figsize=(7, 5.5))
    fig.suptitle("Late-Period Validity vs. Inflation Tradeoff\n"
                 "(each point = one experiment; last 10 rounds; ideal = upper-left)",
                 fontweight="bold", fontsize=12)

    xs, ys, labels_pts, cols = [], [], [], []
    for d, color in zip(all_data, colors):
        late = d["history"][-10:] if len(d["history"]) >= 10 else d["history"]
        inf_vals, caps_all, scores_all = [], [], []
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
        r = np.corrcoef(caps_all, scores_all)[0, 1] if len(caps_all) > 1 else float("nan")
        if not (np.isnan(mean_inf) or np.isnan(r)):
            xs.append(mean_inf); ys.append(r)
            labels_pts.append(d["label"]); cols.append(color)

    for x, y, label, color in zip(xs, ys, labels_pts, cols):
        ax.scatter(x, y, color=color, s=90, zorder=3, edgecolors="black", linewidths=0.5)
        ax.annotate(label, (x, y), textcoords="offset points", xytext=(6, 4),
                    fontsize=7.5, color=color)

    if xs and ys:
        xm, ym = np.median(xs), np.median(ys)
        xl, xr = ax.get_xlim(); yb, yt = ax.get_ylim()
        pad_y = (yt - yb) * 0.05
        ax.axhline(ym, color="gray", linewidth=0.6, linestyle=":", alpha=0.5)
        ax.axvline(xm, color="gray", linewidth=0.6, linestyle=":", alpha=0.5)
        qkw = dict(fontsize=7, color="#777777", style="italic", ha="center")
        ax.text(xl + (xm-xl)/2, yt - pad_y, "low inflation\nhigh validity\n(ideal)", va="top", **qkw)
        ax.text(xr - (xr-xm)/2, yt - pad_y, "high inflation\nhigh validity",          va="top", **qkw)
        ax.text(xl + (xm-xl)/2, yb + pad_y, "low inflation\nlow validity",             va="bottom", **qkw)
        ax.text(xr - (xr-xm)/2, yb + pad_y, "high inflation\nlow validity\n(worst)",  va="bottom", **qkw)

    ax.set_xlabel("Mean Score Inflation (last 10 rounds)", fontsize=10)
    ax.set_ylabel("Validity: Pearson r(score, capability)", fontsize=10)
    ax.tick_params(labelsize=8)
    ax.grid(True, alpha=0.2)
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    _save(fig, "H_validity_vs_inflation.png")


# ===========================================================================
# CSV Tables
# ===========================================================================

def write_csv_safety_investment(all_data):
    rows = []
    for entry in all_data:
        label, history = entry["label"], entry["history"]
        if not history:
            rows.append({"experiment": label, "market_leader_safety_alignment": "", "avg_safety_alignment": ""})
            continue
        providers   = get_providers(history)
        mean_scores = {p: np.mean([h["scores"][p] for h in history if p in h.get("scores", {})] or [0])
                       for p in providers}
        if not mean_scores:
            rows.append({"experiment": label, "market_leader_safety_alignment": "", "avg_safety_alignment": ""})
            continue
        leader = max(mean_scores, key=mean_scores.get)
        def mean_safety(p):
            return np.mean([h["strategies"].get(p, {}).get("safety_alignment", 0) for h in history])
        rows.append({
            "experiment": label,
            "market_leader_safety_alignment": f"{mean_safety(leader):.4f}",
            "avg_safety_alignment": f"{np.mean([mean_safety(p) for p in providers]):.4f}",
        })
    out = os.path.join(OUTPUT_DIR, "safety_investment.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["experiment", "market_leader_safety_alignment", "avg_safety_alignment"])
        w.writeheader(); w.writerows(rows)
    print(f"Saved: {out}")


def write_csv_consumer_satisfaction(all_data):
    rows = []
    for entry in all_data:
        label, history = entry["label"], entry["history"]
        vals = [h.get("consumer_data", {}).get("avg_satisfaction") for h in history]
        vals = [v for v in vals if v is not None]
        rows.append({
            "experiment": label,
            "final_avg_satisfaction": f"{vals[-1]:.4f}" if vals else "",
            "mean_avg_satisfaction":  f"{np.mean(vals):.4f}" if vals else "",
        })
    out = os.path.join(OUTPUT_DIR, "consumer_satisfaction.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["experiment", "final_avg_satisfaction", "mean_avg_satisfaction"])
        w.writeheader(); w.writerows(rows)
    print(f"Saved: {out}")


def write_csv_incident_counts(all_data):
    rows = []
    for entry in all_data:
        incidents = collect_incidents(entry["history"])
        counts = {"minor": 0, "moderate": 0, "major": 0, "critical": 0}
        for inc in incidents:
            if inc["severity"] in counts:
                counts[inc["severity"]] += 1
        rows.append({"experiment": entry["label"], "total": len(incidents), **counts})
    out = os.path.join(OUTPUT_DIR, "incident_counts.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["experiment", "total", "minor", "moderate", "major", "critical"])
        w.writeheader(); w.writerows(rows)
    print(f"Saved: {out}")


# ===========================================================================
# CLI helpers
# ===========================================================================

def _output_dir_for_experiments():
    numbers = [m.group(1) for exp in EXPERIMENTS
               for m in [re.match(r"exp_(\d+)", exp["id"])] if m]
    suffix = "_".join(numbers) if numbers else "custom"
    return os.path.join(_PROJECT_ROOT, "output", "final-plots", suffix)


def _folder_to_label(folder_name):
    name = re.sub(r"^exp_\d+_", "", folder_name)
    for token in ("ablation_", "_balanced", "_ablation"):
        name = name.replace(token, "")
    label = name.strip("_").replace("_", " ").title()
    for acronym in ("Us", "Eu", "Llm", "Ai"):
        label = label.replace(acronym, acronym.upper())
    return label


def _resolve_experiment_id(num):
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
    OUTPUT_DIR = (os.path.join(_PROJECT_ROOT, "output", "final-plots", cli_folder)
                  if cli_folder else _output_dir_for_experiments())

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output directory: {OUTPUT_DIR}")

    print("Loading experiment histories...")
    all_data = load_all_histories()
    loaded   = sum(1 for d in all_data if d["history"])
    print(f"  Loaded {loaded}/{len(all_data)} experiments successfully")

    valid = [d for d in all_data if d["history"]]

    print("\nGenerating plots...")
    plot_market_share(all_data)
    plot_score_vs_capability(all_data)
    plot_incident_validity_combined(all_data)
    plot_investment_allocation(all_data)
    plot_strategy_divergence(all_data)
    plot_c_rolling_validity(valid)
    plot_f_slope_intercept(valid)
    plot_h_validity_vs_inflation(valid)

    print("\nGenerating CSV tables...")
    write_csv_safety_investment(all_data)
    write_csv_consumer_satisfaction(all_data)
    write_csv_incident_counts(all_data)

    print(f"\nDone. Output written to: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
