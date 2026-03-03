"""
create_final_plots.py — Multi-Experiment Comparison Plots

Loads history.json from a hardcoded list of experiment folders and produces
comparison plots + CSV tables in final-plots/.

Edit EXPERIMENTS below to configure which experiments to include.
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
# Tueplots NeurIPS styling (same block as plotting.py)
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

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _figsize(rows: int, cols: int, base_w: float = 2.25, base_h: float = 1.7):
    return (base_w * cols, base_h * rows)


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
        if hist:
            result.append({"label": exp["label"], "history": hist})
        else:
            result.append({"label": exp["label"], "history": []})
    return result


def _grid(N: int):
    n_cols = min(N, MAX_COLS)
    n_rows = ceil(N / n_cols)
    return n_rows, n_cols


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

        # Check consumer data
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

    # Hide unused axes
    total_slots = n_rows * n_cols
    for idx in range(N, total_slots):
        row, col = divmod(idx, n_cols)
        axes[row][col].set_visible(False)

    # Shared legend (from last valid plot)
    handles = [mpatches.Patch(color=PROVIDER_COLOR_MAP.get(p, "#666666"), label=p)
               for p in PROVIDER_COLOR_MAP]
    fig.legend(handles=handles, loc="lower center", ncol=min(5, len(handles)),
               bbox_to_anchor=(0.5, -0.02), frameon=True)

    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "market_share_comparison.png")
    fig.savefig(out_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved: {out_path}")


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

        # y=x line
        if all_caps_flat:
            mn, mx = min(all_caps_flat), max(all_caps_flat)
            ax.plot([mn, mx], [mn, mx], "k--", alpha=0.3)

        # Pearson r
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

    # Hide unused axes
    total_slots = n_rows * n_cols
    for idx in range(N, total_slots):
        row, col = divmod(idx, n_cols)
        axes[row][col].set_visible(False)

    # Shared provider legend
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
    out_path = os.path.join(OUTPUT_DIR, "score_vs_capability.png")
    fig.savefig(out_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved: {out_path}")


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

        # Left axis — incident scatter (y = provider index)
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

        # Right axis — validity correlation + interventions
        ax_right = ax_left.twinx()
        validity_rounds, validity_values = compute_rolling_correlation(history)
        if validity_values:
            ax_right.plot(validity_rounds, validity_values, "o-", color="#457B9D",
                          markersize=3, linewidth=1.5, label="Validity Corr.", zorder=2)

        # Intervention vlines
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

    # Figure-level legend — severity markers + provider colors, two rows, centered
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

    # Combine: severity first, then a spacer title patch, then providers
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
    out_path = os.path.join(OUTPUT_DIR, "incident_validity_combined.png")
    fig.savefig(out_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved: {out_path}")


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
        # Market leader = provider with highest mean score
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



INVESTMENT_TYPES = [
    "fundamental_research",
    "training_optimization",
    "evaluation_engineering",
    "safety_alignment",
]

# Fixed provider order: core 5 first, startups appended after
CORE_PROVIDERS = [
    "Orion Labs",
    "Apex AI",
    "Genesis Systems",
    "Mirage AI",
    "OpenCore",
]


def _provider_order(all_data: list) -> list:
    """Return provider display order for the allocation plot.

    Visual layout (top -> bottom on the chart):
      Orion Labs, Apex AI, Genesis Systems, Mirage AI, OpenCore, OneAI

    Core 5 are fixed at the top (highest y-slots).  Only the first startup
    (OneAI) is appended; subsequent startups are ignored.

    Since matplotlib y=0 is at the bottom, the returned list is ordered
    bottom-to-top: [OneAI, OpenCore, Mirage AI, Genesis Systems, Apex AI,
    Orion Labs].
    """
    # Find only the first startup by earliest appearance round
    startup_seen = {}
    for d in all_data:
        for h in d["history"]:
            for p in h.get("strategies", {}):
                if p not in CORE_PROVIDERS and p not in startup_seen:
                    startup_seen[p] = h["round"]
    first_startup = sorted(startup_seen, key=startup_seen.get)[:1]
    # Bottom-to-top: startup(s) first, then core reversed so Orion is at top
    return first_startup + list(reversed(CORE_PROVIDERS))


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
# Main
# ===========================================================================

def _output_dir_for_experiments() -> str:
    """Build a folder name from the numeric prefixes of the active experiment IDs.

    E.g. ["exp_004_...", "exp_005_...", "exp_006_..."] -> "final-plots/004_005_006"
    Falls back to "final-plots/custom" if no numbers can be extracted.
    """
    import re
    numbers = []
    for exp in EXPERIMENTS:
        m = re.match(r"exp_(\d+)", exp["id"])
        if m:
            numbers.append(m.group(1))
    suffix = "_".join(numbers) if numbers else "custom"
    return os.path.join(_PROJECT_ROOT, "output", "final-plots", suffix)


def _folder_to_label(folder_name: str) -> str:
    """Derive a readable label from an experiment folder name.

    e.g. "exp_004_ablation_no_media_balanced" -> "No Media"
         "exp_003_full_ecosystem_us"           -> "Full Ecosystem US"
    """
    import re
    # Strip leading exp_NNN_
    name = re.sub(r"^exp_\d+_", "", folder_name)
    # Strip common noise tokens
    for token in ("ablation_", "_balanced", "_ablation"):
        name = name.replace(token, "")
    name = name.strip("_")
    # Replace underscores and title-case, then fix known acronyms
    label = name.replace("_", " ").title()
    for acronym in ("Us", "Eu", "Llm", "Ai"):
        label = label.replace(acronym, acronym.upper())
    return label


def _resolve_experiment_id(num: int) -> dict:
    """Find the experiment folder matching a zero-padded number prefix.

    Scans EXPERIMENTS_DIR for folders named exp_NNN_* and returns
    {"id": folder_name, "label": <derived from folder name>}.
    Raises if not found.
    """
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
    """Parse CLI arguments.

    Usage:
      python create_final_plots.py                      # use EXPERIMENTS list
      python create_final_plots.py 1 3 5               # resolve by number, auto folder
      python create_final_plots.py 1 3 5 my_run        # resolve by number, named folder
    """
    import sys
    args = sys.argv[1:]
    if not args:
        return None, None   # fall back to EXPERIMENTS config

    numbers = []
    folder_name = None
    for token in args:
        if token.lstrip("-").isdigit():
            numbers.append(int(token))
        else:
            folder_name = token  # last non-numeric token used as folder name

    if not numbers:
        return None, None

    experiments = [_resolve_experiment_id(n) for n in numbers]
    return experiments, folder_name


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

    print("\nGenerating plots...")
    plot_market_share(all_data)
    plot_score_vs_capability(all_data)
    plot_incident_validity_combined(all_data)
    plot_investment_allocation(all_data)
    plot_strategy_divergence(all_data)

    print("\nGenerating CSV tables...")
    write_csv_safety_investment(all_data)
    write_csv_consumer_satisfaction(all_data)
    write_csv_incident_counts(all_data)

    print(f"\nDone. Output written to: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
