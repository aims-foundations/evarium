"""
create_final_plots.py — Multi-Experiment Comparison Plots

Loads history.json from a hardcoded list of experiment folders and produces
comparison plots + CSV tables in final-plots/.

Edit EXPERIMENTS below to configure which experiments to include.

Plots generated:
  1. market_share_comparison        — stacked-area market share per experiment
  2. score_vs_capability            — score vs ground-truth capability scatter
  3. incident_validity_combined     — incident timeline + validity/interventions
  4. investment_allocation          — provider R&D portfolio over rounds
  5. strategy_divergence            — mean pairwise L1 distance between strategies
  6. C_rolling_validity             — per-benchmark rolling Pearson r (window=5)
  7. F_slope_intercept              — gaming decomposition: slope vs intercept
  8. H_validity_vs_inflation        — late-period validity vs inflation tradeoff

CSV tables:
  safety_investment.csv
  consumer_satisfaction.csv
  incident_counts.csv
"""

import os
import sys
import json
import csv
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
    # Enable LaTeX rendering for publication-quality fonts.
    # Set MPLLATEX=0 in the environment to disable if LaTeX is not available.
    if os.environ.get("MPLLATEX", "1") != "0":
        _NEURIPS_RC["text.usetex"] = True
    mpl.rcParams.update(_NEURIPS_RC)
except ImportError:
    warnings.warn(
        "tueplots not installed — using default matplotlib style. "
        "Run: pip install tueplots",
        stacklevel=1,
    )

# ---------------------------------------------------------------------------
# Imports from plotting.py
# ---------------------------------------------------------------------------
from plotting import (
    get_providers,
    get_provider_colors,
    get_investment_colors,
    compute_rolling_correlation,
    PROVIDER_COLOR_MAP,
)

# ===========================================================================
# CONFIGURATION — edit this list to add/remove experiments
# ===========================================================================
EXPERIMENTS = [
    {"id": "exp_003_full_ecosystem_us",          "label": "US Baseline"},
    {"id": "exp_002_full_ecosystem_eu",          "label": "EU Baseline"},
    # {"id": "exp_004_ablation_no_media_balanced", "label": "No Media"},
    # {"id": "exp_005_ablation_no_incidents_balanced", "label": "No Incidents"},
    # {"id": "exp_006_ablation_no_startups_balanced",  "label": "No Startups"},
    # {"id": "exp_007_ablation_no_opencore_balanced",  "label": "No OpenCore"},
]

OUTPUT_DIR = os.path.join(_PROJECT_ROOT, "output", "final-plots")
EXPERIMENTS_DIR = os.path.join(_PROJECT_ROOT, "output", "experiments")

MAX_COLS = 4  # max columns before wrapping rows

# Fixed provider display order
CORE_PROVIDERS = [
    "Orion Labs",
    "Apex AI",
    "Genesis Systems",
    "Mirage AI",
    "OpenCore",
]

# Marker cycle for benchmark scatter plots
_BENCH_MARKERS = ["o", "s", "^", "D", "v", "P", "*", "X", "h", "p"]

# ---------------------------------------------------------------------------
# General helpers
# ---------------------------------------------------------------------------

def _figsize(rows: int, cols: int, base_w: float = 2.25, base_h: float = 1.7):
    return (base_w * cols, base_h * rows)


def _save(fig, filename: str):
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved: {path}")


def load_history(exp_id: str) -> list:
    path = os.path.join(EXPERIMENTS_DIR, exp_id, "history.json")
    if not os.path.exists(path):
        warnings.warn(f"history.json not found for {exp_id} — skipping")
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def collect_incidents(history: list) -> list:
    """Flat list of {round, provider, severity, category} from history."""
    result = []
    for h in history:
        incs = h.get("incidents") or []
        for inc in incs:
            result.append({
                "round":    h["round"],
                "provider": inc.get("provider", "Unknown"),
                "severity": inc.get("severity", "minor"),
                "category": inc.get("category", ""),
            })
    return result


def load_all_histories() -> list:
    """Returns list of {label, history} dicts (skips missing experiments)."""
    result = []
    for exp in EXPERIMENTS:
        hist = load_history(exp["id"])
        result.append({"label": exp["label"], "history": hist if hist else []})
    return result


def _grid(N: int):
    n_cols = min(N, MAX_COLS)
    n_rows = ceil(N / n_cols)
    return n_rows, n_cols


def exp_colors(n: int):
    """Distinct tab10 colors for up to n experiments."""
    return plt.cm.tab10(np.linspace(0, 0.9, n))


# ---------------------------------------------------------------------------
# Benchmark-level helpers (used by plots C and F)
# ---------------------------------------------------------------------------

def all_benchmarks(history: list) -> list:
    """Ordered list of benchmarks by first appearance round."""
    seen = {}
    for h in history:
        for b in h.get("per_benchmark_scores", {}):
            if b not in seen:
                seen[b] = h["round"]
    return sorted(seen, key=seen.get)


def rolling_bench_correlation(history: list, benchmark: str, window: int = 5):
    """Rolling Pearson r between per_benchmark_score and true_capability."""
    rounds_out, corrs = [], []
    active = [
        (h["round"], h["per_benchmark_scores"][benchmark], h["true_capabilities"])
        for h in history
        if benchmark in h.get("per_benchmark_scores", {})
    ]
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
# Plot 1 — Market Share Across Runs
# ===========================================================================

def plot_market_share(all_data: list):
    N = len(all_data)
    if N == 0:
        return
    n_cols = min(N, 3)
    n_rows = ceil(N / n_cols)
    fig, axes = plt.subplots(n_rows, n_cols,
                             figsize=_figsize(n_rows, n_cols),
                             squeeze=False)
    fig.suptitle("Provider Market Share Dynamics Across Experimental Conditions",
                 fontweight="bold", fontsize=13)

    for idx, entry in enumerate(all_data):
        row, col = divmod(idx, n_cols)
        ax = axes[row][col]
        label = entry["label"]
        history = entry["history"]

        if not history:
            ax.set_title(label, fontweight="bold")
            ax.text(0.5, 0.5, "No data", transform=ax.transAxes,
                    ha="center", va="center", color="gray")
            ax.set_visible(True)
            continue

        has_consumer = any(h.get("consumer_data", {}).get("market_shares") for h in history)
        if not has_consumer:
            ax.set_title(label, fontweight="bold")
            ax.text(0.5, 0.5, "No consumer data", transform=ax.transAxes,
                    ha="center", va="center", color="gray")
            continue

        providers = get_providers(history)
        colors = get_provider_colors(providers)
        rounds = [h["round"] for h in history]

        shares_by_provider = {p: [] for p in providers}
        for h in history:
            ms = h.get("consumer_data", {}).get("market_shares", {})
            total = sum(ms.values()) if ms else 0
            for p in providers:
                shares_by_provider[p].append(ms.get(p, 0) / total if total > 0 else 0)

        bottoms = np.zeros(len(rounds))
        for p in providers:
            vals = np.array(shares_by_provider[p])
            ax.fill_between(rounds, bottoms, bottoms + vals,
                            color=colors[p], alpha=0.8, label=p)
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
# Plot 2 — Score vs True Capability Scatter
# ===========================================================================

def plot_score_vs_capability(all_data: list):
    N = len(all_data)
    if N == 0:
        return
    n_cols = min(N, 3)
    n_rows = ceil(N / n_cols)
    fig, axes = plt.subplots(n_rows, n_cols,
                             figsize=_figsize(n_rows, n_cols),
                             squeeze=False)
    fig.suptitle("Benchmark Score vs. Ground-Truth Capability Across Experimental Conditions",
                 fontweight="bold", fontsize=13)

    for idx, entry in enumerate(all_data):
        row, col = divmod(idx, n_cols)
        ax = axes[row][col]
        label = entry["label"]
        history = entry["history"]

        if not history:
            ax.set_title(label, fontweight="bold")
            ax.text(0.5, 0.5, "No data", transform=ax.transAxes,
                    ha="center", va="center", color="gray")
            continue

        providers = get_providers(history)
        colors = get_provider_colors(providers)

        all_scores_flat, all_caps_flat = [], []
        for p in providers:
            scores = [h["scores"][p] for h in history if p in h.get("scores", {})]
            caps = [h["true_capabilities"][p] for h in history if p in h.get("true_capabilities", {})]
            n = min(len(scores), len(caps))
            if n == 0:
                continue
            ax.scatter(caps[:n], scores[:n], color=colors[p], alpha=0.5,
                       s=15, label=p)
            all_scores_flat.extend(scores[:n])
            all_caps_flat.extend(caps[:n])

        if all_caps_flat:
            mn, mx = min(all_caps_flat), max(all_caps_flat)
            ax.plot([mn, mx], [mn, mx], "k--", alpha=0.3)

        if len(all_scores_flat) >= 2:
            corr = np.corrcoef(all_scores_flat, all_caps_flat)[0, 1]
            title = f"{label}  (r = {corr:.2f})"
        else:
            title = label

        ax.set_title(title, fontweight="bold", fontsize=11)
        ax.set_xlabel("Ground-Truth Capability", fontsize=10)
        ax.set_ylabel("Benchmark Score", fontsize=10)
        ax.tick_params(labelsize=9)
        ax.grid(False)

    for idx in range(N, n_rows * n_cols):
        row, col = divmod(idx, n_cols)
        axes[row][col].set_visible(False)

    all_providers = []
    seen = set()
    for entry in all_data:
        for p in get_providers(entry["history"]):
            if p not in seen:
                all_providers.append(p)
                seen.add(p)
    colors_all = get_provider_colors(all_providers)
    handles = [mpatches.Patch(color=colors_all[p], label=p) for p in all_providers]
    if handles:
        fig.legend(handles=handles, loc="lower center", ncol=min(5, len(handles)),
                   bbox_to_anchor=(0.5, -0.06), frameon=True)

    fig.tight_layout()
    _save(fig, "score_vs_capability.png")


# ===========================================================================
# Plot 3 — Incident Timeline + Validity/Interventions (Combined, dual y-axis)
# ===========================================================================

SEVERITY_MARKERS = {"minor": "o", "moderate": "s", "major": "^", "critical": "X"}
SEVERITY_SIZES   = {"minor": 30,  "moderate": 60,  "major": 100, "critical": 150}


def plot_incident_validity_combined(all_data: list):
    N = len(all_data)
    if N == 0:
        return

    row_h = 1.7
    fig_w = 6.75  # NeurIPS full-width column
    fig, axes = plt.subplots(N, 1, figsize=(fig_w, row_h * N), squeeze=False)
    fig.suptitle(
        "Safety Incident Timeline and Benchmark Validity Across Experimental Conditions",
        fontweight="bold", fontsize=13,
    )

    for idx, entry in enumerate(all_data):
        ax_left = axes[idx][0]
        label = entry["label"]
        history = entry["history"]

        ax_left.set_title(label, fontweight="bold", fontsize=11)

        if not history:
            ax_left.text(0.5, 0.5, "No data", transform=ax_left.transAxes,
                         ha="center", va="center", color="gray")
            ax_left.set_yticks([])
            continue

        providers = get_providers(history)
        provider_colors = get_provider_colors(providers)
        rounds = [h["round"] for h in history]
        incidents = collect_incidents(history)

        if incidents and providers:
            for inc in incidents:
                if inc["provider"] not in providers:
                    continue
                marker = SEVERITY_MARKERS.get(inc["severity"], "o")
                size   = SEVERITY_SIZES.get(inc["severity"], 30)
                color  = provider_colors.get(inc["provider"], "#666666")
                ax_left.scatter(inc["round"], providers.index(inc["provider"]),
                                marker=marker, s=size, color=color,
                                alpha=0.7, edgecolors="black", linewidth=0.5,
                                zorder=3)

        if providers:
            ax_left.set_yticks(range(len(providers)))
            ax_left.set_yticklabels(providers, fontsize=9)
        else:
            ax_left.set_yticks([])

        if rounds:
            ax_left.set_xlim(min(rounds) - 1, max(rounds) + 1)
        ax_left.set_xlabel("Simulation Round", fontsize=10)
        ax_left.set_ylabel("Provider", fontsize=10)
        ax_left.tick_params(axis="x", labelsize=9)
        ax_left.grid(False)

        ax_right = ax_left.twinx()
        validity_rounds, validity_values = compute_rolling_correlation(history)
        if validity_values:
            ax_right.plot(validity_rounds, validity_values, "o-", color="#457B9D",
                          markersize=3, linewidth=1.5, label="Validity Corr.", zorder=2)

        intervention_rounds = set()
        for h in history:
            pm = h.get("policymaker_data", {})
            if pm.get("interventions"):
                intervention_rounds.add(h["round"])
        for ir in intervention_rounds:
            ax_right.axvline(x=ir, color="#E63946", linestyle="--", alpha=0.5, linewidth=0.8)

        ax_right.set_ylim(-0.1, 1.1)
        ax_right.set_ylabel("Validity Correlation", fontsize=10)
        ax_right.tick_params(axis="y", labelsize=9)

    severity_handles = [
        mlines.Line2D([0], [0], marker=m, color="w", markerfacecolor="gray",
                      markeredgecolor="black", markersize=ms,
                      label=sev.capitalize())
        for sev, (m, ms) in {
            "minor": ("o", 7), "moderate": ("s", 9),
            "major": ("^", 11), "critical": ("X", 13),
        }.items()
    ]
    all_providers = []
    seen = set()
    for entry in all_data:
        for p in get_providers(entry["history"]):
            if p not in seen:
                all_providers.append(p)
                seen.add(p)
    pc = get_provider_colors(all_providers)
    provider_handles = [mpatches.Patch(color=pc[p], label=p) for p in all_providers]

    spacer = mpatches.Patch(color="none", label="Providers:")
    severity_label = mpatches.Patch(color="none", label="Severity:")
    all_handles = [severity_label] + severity_handles + [spacer] + provider_handles

    n_per_row = ceil(len(all_handles) / 2)
    fig.legend(
        handles=all_handles,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.06),
        ncol=n_per_row,
        frameon=True,
        fontsize=9,
        handlelength=1.5,
        columnspacing=1.2,
    )

    fig.tight_layout()
    _save(fig, "incident_validity_combined.png")


# ===========================================================================
# Plot 4 — Investment Allocation Across Experiments and Rounds
# ===========================================================================

INVESTMENT_TYPES = [
    "fundamental_research",
    "training_optimization",
    "evaluation_engineering",
    "safety_alignment",
]

ALLOC_MAX_COLS = 3


def _provider_order(all_data: list) -> list:
    startup_seen = {}
    for d in all_data:
        for h in d["history"]:
            for p in h.get("strategies", {}):
                if p not in CORE_PROVIDERS and p not in startup_seen:
                    startup_seen[p] = h["round"]
    first_startup = sorted(startup_seen, key=startup_seen.get)[:1]
    return first_startup + list(reversed(CORE_PROVIDERS))


def _draw_allocation_panel(ax, rounds, strats, providers, inv_colors, show_ylabel):
    n_providers = len(providers)
    xs = list(range(len(rounds)))

    for p_idx, provider in enumerate(providers):
        slot_bottom = p_idx
        present = any(provider in strats[r] for r in rounds)

        if not present:
            ax.fill_between(
                [-0.5, len(rounds) - 0.5],
                [slot_bottom, slot_bottom],
                [slot_bottom + 1, slot_bottom + 1],
                color="#E8E8E8", linewidth=0, zorder=0,
            )
            continue

        cum = np.zeros(len(rounds))
        for inv in INVESTMENT_TYPES:
            vals = np.array([strats[r].get(provider, {}).get(inv, 0.0) for r in rounds])
            ax.fill_between(
                xs,
                slot_bottom + cum,
                slot_bottom + cum + vals,
                color=inv_colors[inv], linewidth=0, alpha=0.9, zorder=1,
            )
            cum += vals

    for i in range(1, n_providers):
        ax.axhline(i, color="black", linewidth=0.6, linestyle=":", zorder=3)

    xtick_pos = [i for i, r in enumerate(rounds) if r % 10 == 0 or r == rounds[0]]
    xtick_lab = [str(rounds[i]) for i in xtick_pos]
    ax.set_xticks(xtick_pos)
    ax.set_xticklabels(xtick_lab, fontsize=8)
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


def plot_investment_allocation(all_data: list):
    valid = [d for d in all_data if d["history"]]
    if not valid:
        return

    inv_colors = get_investment_colors()
    providers   = _provider_order(all_data)
    n_providers = len(providers)
    N = len(valid)

    n_cols = min(N, ALLOC_MAX_COLS)
    n_rows = ceil(N / n_cols)

    panel_w = max(2.5, 10.0 / n_cols)
    panel_h = max(3.5, n_providers * 0.7 + 1.0)
    fig, axes = plt.subplots(
        n_rows, n_cols,
        figsize=(panel_w * n_cols, panel_h * n_rows),
        squeeze=False,
    )

    fig.suptitle(
        "Provider Investment Allocation Over Simulation Rounds",
        fontweight="bold", fontsize=13,
    )

    for idx, d in enumerate(valid):
        row, col = divmod(idx, n_cols)
        ax = axes[row][col]
        history = d["history"]
        rounds  = [h["round"] for h in history]
        strats  = {h["round"]: h.get("strategies", {}) for h in history}

        show_ylabel = (col == 0)
        _draw_allocation_panel(ax, rounds, strats, providers, inv_colors, show_ylabel)
        ax.set_title(d["label"], fontweight="bold", fontsize=11)

    for idx in range(N, n_rows * n_cols):
        row, col = divmod(idx, n_cols)
        axes[row][col].set_visible(False)

    legend_handles = [
        mpatches.Patch(color=inv_colors[inv], label=inv.replace("_", " ").title())
        for inv in INVESTMENT_TYPES
    ]
    fig.legend(handles=legend_handles, loc="lower center",
               bbox_to_anchor=(0.5, -0.02), ncol=4, fontsize=9, frameon=True)

    fig.tight_layout(rect=[0, 0.06, 1, 0.96])
    _save(fig, "investment_allocation.png")


# ===========================================================================
# Plot 5 — Strategy Divergence Over Time
# ===========================================================================

def _mean_pairwise_l1(vectors: list) -> float:
    if len(vectors) < 2:
        return 0.0
    total, count = 0.0, 0
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            total += np.sum(np.abs(vectors[i] - vectors[j]))
            count += 1
    return total / count


def plot_strategy_divergence(all_data: list):
    valid = [(d["label"], d["history"]) for d in all_data if d["history"]]
    if not valid:
        return

    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    fig.suptitle(
        "Strategic Divergence Among Providers Over Time",
        fontweight="bold", fontsize=13,
    )

    exp_cols = exp_colors(len(valid))

    for (label, history), color in zip(valid, exp_cols):
        providers = get_providers(history)
        rounds, divergences = [], []

        for h in history:
            strats = h.get("strategies", {})
            vecs = []
            for p in providers:
                if p in strats:
                    v = np.array([
                        strats[p].get(inv, 0.0) for inv in INVESTMENT_TYPES
                    ])
                    vecs.append(v)
            if len(vecs) >= 2:
                rounds.append(h["round"])
                divergences.append(_mean_pairwise_l1(vecs))

        if rounds:
            ax.plot(rounds, divergences, marker="o", markersize=3,
                    linewidth=1.8, label=label, color=color)

    ax.set_xlabel("Simulation Round", fontsize=10)
    ax.set_ylabel("Mean Pairwise L1 Distance", fontsize=10)
    ax.tick_params(labelsize=9)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=9, frameon=True)
    ax.text(0.01, 0.97,
            "Higher = more differentiated strategies",
            transform=ax.transAxes, fontsize=8, va="top", color="gray",
            style="italic")

    fig.tight_layout()
    _save(fig, "strategy_divergence.png")


# ===========================================================================
# Plot C — Per-Benchmark Rolling Validity
# ===========================================================================
# One panel per benchmark. x=round, y=rolling Pearson r(score, capability).
# Reference lines at r=0.7/0.5/0.3.

def plot_c_rolling_validity(all_data: list):
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
            if not rounds:
                continue
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
    fig.legend(handles=handles, loc="lower center",
               bbox_to_anchor=(0.5, -0.02),
               ncol=min(6, len(handles)), fontsize=9, frameon=True)

    fig.tight_layout(rect=[0, 0.05, 1, 0.95])
    _save(fig, "C_rolling_validity.png")


# ===========================================================================
# Plot F — Slope vs Intercept Scatter (2D gaming decomposition)
# ===========================================================================
# x = OLS intercept (floor bias), y = OLS slope (amplification).
# One point per (benchmark × experiment). Color = experiment, marker = benchmark.

def plot_f_slope_intercept(all_data: list):
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

    fig, ax = plt.subplots(figsize=(7, 6))
    fig.suptitle(
        "Gaming Decomposition: Slope vs. Intercept\n"
        "(intercept = floor bias; slope = capability amplification)",
        fontweight="bold", fontsize=12,
    )

    for d, color in zip(all_data, colors):
        history = d["history"]
        for bench in bench_union:
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

    ax.axhline(1.0, color="gray", linewidth=0.9, linestyle="--", alpha=0.6, zorder=1)
    ax.axvline(0.0, color="gray", linewidth=0.9, linestyle="--", alpha=0.6, zorder=1)

    ax.set_xlim(left=min(-0.05, ax.get_xlim()[0] - 0.02))

    quad_kw = dict(fontsize=7.5, color="#555555", ha="center", va="center",
                   style="italic")

    def _qtext(x_frac, y_frac, text):
        xl, xr = ax.get_xlim()
        yb, yt = ax.get_ylim()
        ax.text(xl + x_frac * (xr - xl), yb + y_frac * (yt - yb), text, **quad_kw)

    _qtext(0.25, 0.92, "floor bias\nlow amplification")
    _qtext(0.75, 0.92, "floor bias\n+ amplification")
    _qtext(0.25, 0.08, "well-calibrated\n(low gaming)")
    _qtext(0.75, 0.08, "amplification\nno floor bias")

    ax.set_xlabel("Intercept (floor bias)", fontsize=10)
    ax.set_ylabel("Slope (amplification)", fontsize=10)
    ax.tick_params(labelsize=8)
    ax.grid(True, alpha=0.2)

    exp_handles = [mpatches.Patch(color=c, label=d["label"])
                   for d, c in zip(all_data, colors)]
    bench_handles = [mlines.Line2D([], [], color="gray",
                                   marker=marker_map[b], markersize=6,
                                   linewidth=0, label=b.replace("_", " ").title())
                     for b in bench_union]
    fig.legend(handles=exp_handles,
               loc="upper center", bbox_to_anchor=(0.5, 1.0),
               ncol=min(4, len(exp_handles)),
               fontsize=8, frameon=True,
               title="Experiment", title_fontsize=8)
    fig.legend(handles=bench_handles,
               loc="lower center", bbox_to_anchor=(0.5, 0.0),
               ncol=min(4, len(bench_handles)),
               fontsize=8, frameon=True,
               title="Benchmark", title_fontsize=8)

    fig.tight_layout(rect=[0, 0.10, 1, 0.88])
    _save(fig, "F_slope_intercept.png")


# ===========================================================================
# Plot H — Late-Period Validity vs Inflation Tradeoff
# ===========================================================================
# Each point = one experiment. x = mean inflation (last 10 rounds),
# y = Pearson r(score, capability). Quadrant shading. Ideal = upper-left.

def plot_h_validity_vs_inflation(all_data: list):
    colors = exp_colors(len(all_data))

    fig, ax = plt.subplots(figsize=(7, 5.5))
    fig.suptitle(
        "Late-Period Validity vs. Inflation Tradeoff\n"
        "(each point = one experiment; last 10 rounds; ideal = upper-left)",
        fontweight="bold", fontsize=12,
    )

    xs, ys, labels_pts, cols = [], [], [], []
    for d, color in zip(all_data, colors):
        history = d["history"]
        late = history[-10:] if len(history) >= 10 else history

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
    ax.grid(True, alpha=0.2)

    fig.tight_layout(rect=[0, 0, 1, 0.92])
    _save(fig, "H_validity_vs_inflation.png")


# ===========================================================================
# CSV Tables
# ===========================================================================

def write_csv_safety_investment(all_data: list):
    rows = []
    for entry in all_data:
        label = entry["label"]
        history = entry["history"]
        if not history:
            rows.append({"experiment": label,
                         "market_leader_safety_alignment": "",
                         "avg_safety_alignment": ""})
            continue

        providers = get_providers(history)
        mean_scores = {}
        for p in providers:
            vals = [h["scores"][p] for h in history if p in h.get("scores", {})]
            mean_scores[p] = np.mean(vals) if vals else 0.0
        if not mean_scores:
            rows.append({"experiment": label,
                         "market_leader_safety_alignment": "",
                         "avg_safety_alignment": ""})
            continue

        leader = max(mean_scores, key=mean_scores.get)

        def mean_safety(p):
            vals = [h["strategies"].get(p, {}).get("safety_alignment", 0)
                    for h in history]
            return np.mean(vals)

        leader_safety = mean_safety(leader)
        avg_safety = np.mean([mean_safety(p) for p in providers]) if providers else 0.0

        rows.append({
            "experiment": label,
            "market_leader_safety_alignment": f"{leader_safety:.4f}",
            "avg_safety_alignment": f"{avg_safety:.4f}",
        })

    out_path = os.path.join(OUTPUT_DIR, "safety_investment.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["experiment",
                                                "market_leader_safety_alignment",
                                                "avg_safety_alignment"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved: {out_path}")


def write_csv_consumer_satisfaction(all_data: list):
    rows = []
    for entry in all_data:
        label = entry["label"]
        history = entry["history"]
        if not history:
            rows.append({"experiment": label,
                         "final_avg_satisfaction": "",
                         "mean_avg_satisfaction": ""})
            continue

        vals = [h.get("consumer_data", {}).get("avg_satisfaction")
                for h in history]
        vals = [v for v in vals if v is not None]
        if not vals:
            rows.append({"experiment": label,
                         "final_avg_satisfaction": "",
                         "mean_avg_satisfaction": ""})
            continue

        rows.append({
            "experiment": label,
            "final_avg_satisfaction": f"{vals[-1]:.4f}",
            "mean_avg_satisfaction": f"{np.mean(vals):.4f}",
        })

    out_path = os.path.join(OUTPUT_DIR, "consumer_satisfaction.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["experiment",
                                                "final_avg_satisfaction",
                                                "mean_avg_satisfaction"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved: {out_path}")


def write_csv_incident_counts(all_data: list):
    rows = []
    for entry in all_data:
        label = entry["label"]
        incidents = collect_incidents(entry["history"])
        counts = {"minor": 0, "moderate": 0, "major": 0, "critical": 0}
        for inc in incidents:
            sev = inc["severity"]
            if sev in counts:
                counts[sev] += 1
        rows.append({
            "experiment": label,
            "total": len(incidents),
            **counts,
        })

    out_path = os.path.join(OUTPUT_DIR, "incident_counts.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["experiment", "total",
                                                "minor", "moderate",
                                                "major", "critical"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved: {out_path}")


# ===========================================================================
# Plot 4 — Investment Allocation Across Experiments and Rounds
# ===========================================================================

ALLOC_MAX_COLS = 3  # experiments per row before wrapping


def _draw_allocation_panel(ax, rounds, strats, providers, inv_colors, show_ylabel):
    """Draw one experiment's stacked-area allocation into ax."""
    n_providers = len(providers)
    xs = list(range(len(rounds)))

    for p_idx, provider in enumerate(providers):
        slot_bottom = p_idx
        present = any(provider in strats[r] for r in rounds)

        if not present:
            ax.fill_between(
                [-0.5, len(rounds) - 0.5],
                [slot_bottom, slot_bottom],
                [slot_bottom + 1, slot_bottom + 1],
                color="#E8E8E8", linewidth=0, zorder=0,
            )
            continue

        cum = np.zeros(len(rounds))
        for inv in INVESTMENT_TYPES:
            vals = np.array([strats[r].get(provider, {}).get(inv, 0.0) for r in rounds])
            ax.fill_between(
                xs,
                slot_bottom + cum,
                slot_bottom + cum + vals,
                color=inv_colors[inv], linewidth=0, alpha=0.9, zorder=1,
            )
            cum += vals

    # Provider separator lines
    for i in range(1, n_providers):
        ax.axhline(i, color="black", linewidth=0.6, linestyle=":", zorder=3)

    # X-axis ticks: round 1 and every 10th
    xtick_pos = [i for i, r in enumerate(rounds) if r % 10 == 0 or r == rounds[0]]
    xtick_lab = [str(rounds[i]) for i in xtick_pos]
    ax.set_xticks(xtick_pos)
    ax.set_xticklabels(xtick_lab, fontsize=8)
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


def plot_investment_allocation(all_data: list):
    """Stacked-area allocation chart, wrapping to a new row every 3 experiments.

    Each subplot = one experiment.  Y-axis spans [0, N_providers]; each unit
    slice [i, i+1] belongs to one provider with the 4 investment types stacked
    as a continuous area over rounds.  Provider names shown on the leftmost
    column only.  Gray fill for providers absent from an experiment.
    """
    valid = [d for d in all_data if d["history"]]
    if not valid:
        return

    inv_colors = get_investment_colors()
    providers  = _provider_order(all_data)
    n_providers = len(providers)
    N = len(valid)

    n_cols = min(N, ALLOC_MAX_COLS)
    n_rows = ceil(N / n_cols)

    panel_w = max(2.0, 6.75 / n_cols)   # scale width per panel to total figure width
    panel_h = max(1.7, n_providers * 0.35 + 0.6)
    fig, axes = plt.subplots(
        n_rows, n_cols,
        figsize=(panel_w * n_cols, panel_h * n_rows),
        squeeze=False,
    )

    fig.suptitle(
        "Provider Investment Allocation Over Simulation Rounds",
        fontweight="bold", fontsize=13,
    )

    for idx, d in enumerate(valid):
        row, col = divmod(idx, n_cols)
        ax = axes[row][col]
        history = d["history"]
        rounds  = [h["round"] for h in history]
        strats  = {h["round"]: h.get("strategies", {}) for h in history}

        show_ylabel = (col == 0)
        _draw_allocation_panel(ax, rounds, strats, providers, inv_colors, show_ylabel)
        ax.set_title(d["label"], fontweight="bold", fontsize=11)

    # Hide unused axes
    for idx in range(N, n_rows * n_cols):
        row, col = divmod(idx, n_cols)
        axes[row][col].set_visible(False)

    # Shared investment-type legend at the bottom
    legend_handles = [
        mpatches.Patch(color=inv_colors[inv], label=inv.replace("_", " ").title())
        for inv in INVESTMENT_TYPES
    ]
    fig.legend(handles=legend_handles, loc="lower center",
               bbox_to_anchor=(0.5, -0.02), ncol=4, fontsize=9, frameon=True)

    fig.tight_layout(rect=[0, 0.06, 1, 0.96])
    out_path = os.path.join(OUTPUT_DIR, "investment_allocation.png")
    fig.savefig(out_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved: {out_path}")


# ===========================================================================
# Plot 5 — Strategy Divergence Over Time
# ===========================================================================

def _mean_pairwise_l1(vectors: list) -> float:
    """Mean pairwise L1 distance between a list of allocation vectors."""
    if len(vectors) < 2:
        return 0.0
    total, count = 0.0, 0
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            total += np.sum(np.abs(vectors[i] - vectors[j]))
            count += 1
    return total / count


def plot_strategy_divergence(all_data: list):
    """Single panel: mean pairwise L1 distance between provider allocation
    vectors per round, one line per experiment.

    High divergence = providers are pursuing very different strategies.
    Low / falling divergence = strategic convergence.
    """
    valid = [(d["label"], d["history"]) for d in all_data if d["history"]]
    if not valid:
        return

    fig, ax = plt.subplots(figsize=(3.25, 1.86))
    fig.suptitle(
        "Strategic Divergence Among Providers Over Time",
        fontweight="bold", fontsize=13,
    )

    # Color each experiment line distinctly
    exp_colors = plt.cm.tab10(np.linspace(0, 0.9, len(valid)))

    for (label, history), color in zip(valid, exp_colors):
        providers = get_providers(history)
        rounds, divergences = [], []

        for h in history:
            strats = h.get("strategies", {})
            vecs = []
            for p in providers:
                if p in strats:
                    v = np.array([
                        strats[p].get(inv, 0.0) for inv in INVESTMENT_TYPES
                    ])
                    vecs.append(v)
            if len(vecs) >= 2:
                rounds.append(h["round"])
                divergences.append(_mean_pairwise_l1(vecs))

        if rounds:
            ax.plot(rounds, divergences, marker="o", markersize=3,
                    linewidth=1.8, label=label, color=color)

    ax.set_xlabel("Simulation Round", fontsize=10)
    ax.set_ylabel("Mean Pairwise L1 Distance", fontsize=10)
    ax.tick_params(labelsize=9)
    ax.grid(False)
    ax.legend(fontsize=9, frameon=True)

    # Annotate interpretation
    ax.text(0.01, 0.97,
            "Higher = more differentiated strategies",
            transform=ax.transAxes, fontsize=8, va="top", color="gray",
            style="italic")

    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "strategy_divergence.png")
    fig.savefig(out_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved: {out_path}")


# ===========================================================================
# CLI helpers
# ===========================================================================

def _output_dir_for_experiments() -> str:
    import re
    numbers = []
    for exp in EXPERIMENTS:
        m = re.match(r"exp_(\d+)", exp["id"])
        if m:
            numbers.append(m.group(1))
    suffix = "_".join(numbers) if numbers else "custom"
    return os.path.join(_PROJECT_ROOT, "output", "final-plots", suffix)


def _folder_to_label(folder_name: str) -> str:
    import re
    name = re.sub(r"^exp_\d+_", "", folder_name)
    for token in ("ablation_", "_balanced", "_ablation"):
        name = name.replace(token, "")
    name = name.strip("_")
    label = name.replace("_", " ").title()
    for acronym in ("Us", "Eu", "Llm", "Ai"):
        label = label.replace(acronym, acronym.upper())
    return label


def _resolve_experiment_id(num: int) -> dict:
    import re
    target = f"{num:03d}"
    for name in sorted(os.listdir(EXPERIMENTS_DIR)):
        m = re.match(r"exp_(\d+)_", name)
        if m and m.group(1) == target:
            return {"id": name, "label": _folder_to_label(name)}
    raise ValueError(
        f"No experiment folder matching exp_{target}_* found in {EXPERIMENTS_DIR}/"
    )


def _parse_args():
    """
    Usage:
      python create_final_plots.py                      # use EXPERIMENTS list
      python create_final_plots.py 1 3 5               # resolve by number, auto folder
      python create_final_plots.py 1 3 5 my_run        # resolve by number, named folder
    """
    args = sys.argv[1:]
    if not args:
        return None, None

    numbers = []
    folder_name = None
    for token in args:
        if token.lstrip("-").isdigit():
            numbers.append(int(token))
        else:
            folder_name = token

    if not numbers:
        return None, None

    experiments = [_resolve_experiment_id(n) for n in numbers]
    return experiments, folder_name


# ===========================================================================
# Main
# ===========================================================================

def main():
    global OUTPUT_DIR, EXPERIMENTS

    cli_experiments, cli_folder = _parse_args()

    if cli_experiments is not None:
        EXPERIMENTS = cli_experiments

    if cli_folder is not None:
        OUTPUT_DIR = os.path.join(_PROJECT_ROOT, "output", "final-plots", cli_folder)
    else:
        OUTPUT_DIR = _output_dir_for_experiments()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output directory: {OUTPUT_DIR}")

    print("Loading experiment histories...")
    all_data = load_all_histories()
    loaded = sum(1 for d in all_data if d["history"])
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
