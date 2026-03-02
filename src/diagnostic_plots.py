"""
Diagnostic Plots for Simulation Diagnostics

Publication-quality plots for:
- Trace overlay with mean/CI envelope (Diagnostic 3)
- Sensitivity tornado chart (Diagnostic 4)
- Strategy drift heatmap (Diagnostic 5)
- Pattern validation checklist (Diagnostic 6)
- CRN paired difference (Diagnostic 2)
"""

import os
import warnings
from typing import Callable, Optional

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# Apply tueplots NeurIPS bundle for publication-quality styling.
# Falls back gracefully if tueplots is not installed or LaTeX is unavailable.
try:
    from tueplots import bundles as _tueplots_bundles

    _NEURIPS_RC = _tueplots_bundles.neurips2024()
    # Diagnostic plots need flexible sizing — drop figsize override.
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

from diagnostics import aggregate_replications, extract_metric_series


# ============================================================================
# Diagnostic 3: Trace Overlay
# ============================================================================


def plot_trace_overlay(
    histories: list[list[dict]],
    metric_fn: Callable,
    metric_name: str,
    ylabel: str,
    save_path: str = None,
    show: bool = False,
    figsize: tuple = (3, 3),
) -> plt.Figure:
    """Plot N trace overlays + mean + 95% CI envelope."""
    data = extract_metric_series(histories, metric_fn)
    agg = aggregate_replications(histories, metric_fn)

    fig, ax = plt.subplots(figsize=figsize)
    rounds = agg["rounds"]

    for i in range(data.shape[0]):
        ax.plot(rounds, data[i], color="steelblue", alpha=0.15, linewidth=0.8)

    ax.plot(rounds, agg["mean"], color="steelblue", linewidth=2.5, label="Mean")
    ax.fill_between(
        rounds,
        agg["ci_lower"],
        agg["ci_upper"],
        color="steelblue",
        alpha=0.25,
        label=r"95\% CI",
    )

    ax.set_title(f"{metric_name} ({data.shape[0]} replications)", fontweight="bold")
    ax.set_xlabel("Round")
    ax.set_ylabel(ylabel)
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    if not show:
        plt.close(fig)
    return fig


def plot_trace_overlay_multi(
    histories: list[list[dict]],
    metrics: dict,
    save_path: str = None,
    show: bool = False,
) -> plt.Figure:
    """Plot multiple metrics in a grid of trace overlay panels.

    Args:
        metrics: {display_name: (metric_fn, ylabel)}.
    """
    n_metrics = len(metrics)
    cols = min(3, n_metrics)
    rows = (n_metrics + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(3 * cols, 3 * rows))
    if n_metrics == 1:
        axes = np.array([axes])
    axes = np.atleast_1d(axes).flatten()

    n_reps = len(histories)
    for idx, (name, (metric_fn, ylabel)) in enumerate(metrics.items()):
        ax = axes[idx]
        data = extract_metric_series(histories, metric_fn)
        agg = aggregate_replications(histories, metric_fn)
        rounds = agg["rounds"]

        for i in range(data.shape[0]):
            ax.plot(rounds, data[i], color="steelblue", alpha=0.15, linewidth=0.8)
        ax.plot(rounds, agg["mean"], color="steelblue", linewidth=2.0)
        ax.fill_between(
            rounds, agg["ci_lower"], agg["ci_upper"], color="steelblue", alpha=0.25
        )
        ax.set_title(name, fontweight="bold")
        ax.set_xlabel("Round")
        ax.set_ylabel(ylabel)
        ax.grid(True, alpha=0.3)

    for idx in range(n_metrics, len(axes)):
        axes[idx].set_visible(False)

    fig.suptitle(
        f"Trajectory Inspection ({n_reps} replications)", fontweight="bold", y=1.02
    )
    fig.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    if not show:
        plt.close(fig)
    return fig


# ============================================================================
# Diagnostic 4: Sensitivity Tornado
# ============================================================================


def plot_sensitivity_tornado(
    sensitivity_results: list[dict],
    metric_label: str = "Outcome",
    save_path: str = None,
    show: bool = False,
    figsize: tuple = (3, 3),
) -> plt.Figure:
    """Tornado diagram showing sensitivity of outcome to each parameter."""
    fig, ax = plt.subplots(figsize=figsize)

    param_names = []
    low_effects = []
    high_effects = []

    for sr in sensitivity_results:
        param_names.append(sr["param_name"])
        effects = [p.get("effect", 0) for p in sr["perturbations"]]
        if effects:
            low_effects.append(min(effects))
            high_effects.append(max(effects))
        else:
            low_effects.append(0)
            high_effects.append(0)

    ranges = [abs(h - l) for l, h in zip(low_effects, high_effects)]
    order = np.argsort(ranges)[::-1]

    y_pos = np.arange(len(param_names))

    for i, idx in enumerate(order):
        color_low = "#E63946" if low_effects[idx] < 0 else "#2A9D8F"
        color_high = "#2A9D8F" if high_effects[idx] > 0 else "#E63946"
        ax.barh(i, low_effects[idx], color=color_low, alpha=0.7, height=0.6)
        ax.barh(i, high_effects[idx], color=color_high, alpha=0.7, height=0.6)

    ax.set_yticks(y_pos)
    ax.set_yticklabels([param_names[idx] for idx in order])
    ax.axvline(x=0, color="black", linewidth=0.8)
    ax.set_title(f"Sensitivity Tornado: {metric_label}", fontweight="bold")
    ax.set_xlabel("Effect on outcome")
    ax.grid(True, alpha=0.3, axis="x")

    fig.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    if not show:
        plt.close(fig)
    return fig


# ============================================================================
# Diagnostic 5: Strategy Drift Heatmap
# ============================================================================


def plot_strategy_drift_heatmap(
    drift_data: dict,
    save_path: str = None,
    show: bool = False,
    figsize: tuple = (3, 3),
) -> plt.Figure:
    """Heatmap of strategy drift scores (provider x round)."""
    providers = sorted(drift_data.keys())
    max_rounds = max(len(v) for v in drift_data.values())

    matrix = np.full((len(providers), max_rounds), np.nan)
    for i, name in enumerate(providers):
        scores = drift_data[name]
        matrix[i, : len(scores)] = scores

    fig, ax = plt.subplots(figsize=figsize, layout="constrained")
    im = ax.imshow(
        matrix, aspect="auto", cmap="YlOrRd", interpolation="nearest", vmin=0, vmax=0.3
    )

    ax.set_yticks(range(len(providers)))
    ax.set_yticklabels(providers)
    ax.set_xlabel("Round")
    ax.set_title(
        "Strategy Drift (cosine distance from rolling mean)", fontweight="bold"
    )

    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("Drift score")

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    if not show:
        plt.close(fig)
    return fig


# ============================================================================
# Diagnostic 6: Pattern Validation Checklist
# ============================================================================


def plot_pattern_validation_checklist(
    pattern_results: dict,
    save_path: str = None,
    show: bool = False,
    figsize: tuple = (3, 3),
) -> plt.Figure:
    """Visual checklist of pattern-oriented validation results."""
    names = list(pattern_results.keys())
    fractions = [pattern_results[n]["fraction"] for n in names]
    passed = [pattern_results[n]["passed"] for n in names]

    fig, ax = plt.subplots(figsize=figsize)

    colors = ["#2A9D8F" if p else "#E63946" for p in passed]
    y_pos = np.arange(len(names))
    ax.barh(y_pos, fractions, color=colors, alpha=0.8, height=0.6)
    ax.axvline(x=0.5, color="black", linewidth=0.8, linestyle="--", alpha=0.5)

    ax.set_yticks(y_pos)
    ax.set_yticklabels([n.replace("_", " ").title() for n in names])
    ax.set_xlim(0, 1)
    ax.set_xlabel("Fraction of replications")
    ax.set_title("Pattern-Oriented Validation", fontweight="bold")

    for i, (frac, p) in enumerate(zip(fractions, passed)):
        status = "PASS" if p else "FAIL"
        pct = f"{frac*100:.0f}"
        ax.text(frac + 0.02, i, rf"{pct}\% [{status}]", va="center")

    fig.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    if not show:
        plt.close(fig)
    return fig


# ============================================================================
# Diagnostic 2: CRN Paired Difference
# ============================================================================


def plot_crn_paired_difference(
    paired_result: dict,
    metric_name: str,
    condition_a_label: str = "A",
    condition_b_label: str = "B",
    save_path: str = None,
    show: bool = False,
    figsize: tuple = (3, 3),
) -> plt.Figure:
    """Plot CRN paired difference (A - B) with CI envelope."""
    fig, ax = plt.subplots(figsize=figsize)

    rounds = paired_result["rounds"]
    mean_diff = paired_result["mean_diff"]
    ci_lower = paired_result["ci_lower"]
    ci_upper = paired_result["ci_upper"]

    ax.plot(rounds, mean_diff, color="steelblue", linewidth=2, label="Mean diff")
    ax.fill_between(
        rounds, ci_lower, ci_upper, color="steelblue", alpha=0.25, label="95% CI"
    )
    ax.axhline(y=0, color="black", linewidth=0.8, linestyle="--")

    for t in range(len(rounds)):
        if ci_lower[t] > 0 or ci_upper[t] < 0:
            ax.axvspan(rounds[t] - 0.4, rounds[t] + 0.4, color="gold", alpha=0.2)

    overall = paired_result.get("overall", {})
    p_val = overall.get("p_value")
    title = f"CRN Paired Difference: {condition_a_label} - {condition_b_label}"
    if p_val is not None:
        title += f"\n{metric_name} (overall p={p_val:.4f})"
    else:
        title += f"\n{metric_name}"

    ax.set_title(title, fontweight="bold")
    ax.set_xlabel("Round")
    ax.set_ylabel(f"Difference ({condition_a_label} - {condition_b_label})")
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    if not show:
        plt.close(fig)
    return fig
