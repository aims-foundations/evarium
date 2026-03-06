"""
process_mindshare.py — Mind Share Stacked Area Plots

Reads actor_mentions.json and documents_mentions.json from data/processed/,
normalises counts to percentage mind share at each time point, and produces
two stacked area charts (documents + actor pairs) styled to match the
final_plots.py NeurIPS figure aesthetic.

Output:
  plots/mindshare_documents.png
  plots/mindshare_actor_pairs.png
  plots/mindshare_combined.png

Usage:
  python scripts/process_mindshare.py
"""

import os
import json
import warnings

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib as mpl
import numpy as np

# ---------------------------------------------------------------------------
# Tueplots NeurIPS styling (mirrors final_plots.py)
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

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_SCRIPT_DIR)

DATA_DIR   = os.path.join(_PROJECT_ROOT, "data", "processed")
OUTPUT_DIR = os.path.join(_PROJECT_ROOT, "plots")
os.makedirs(OUTPUT_DIR, exist_ok=True)

DOCUMENTS_JSON = os.path.join(DATA_DIR, "documents_mentions.json")
ACTORS_JSON    = os.path.join(DATA_DIR, "actors_mentions.json")

# ---------------------------------------------------------------------------
# Providers & colours (match original chart exactly)
# ---------------------------------------------------------------------------
COMPANIES = ["OpenAI", "Anthropic", "Google", "Meta", "Deepseek"]

# Colors mapped to sim provider analogs so both plots share the same palette:
#   OpenAI -> Orion Labs (#1f77b4), Anthropic -> Apex AI (#ff7f0e),
#   Google -> Genesis Systems (#2ca02c), Meta -> Mirage AI (#d62728),
#   Deepseek -> OpenCore (#9467bd)
COLORS = {
    "OpenAI":    "#1f77b4",
    "Anthropic": "#ff7f0e",
    "Google":    "#2ca02c",
    "Meta":      "#d62728",
    "Deepseek":  "#9467bd",
}

# Stack order: bottom → top (mirrors SIM_STACK_ORDER analog order)
STACK_ORDER = ["Deepseek", "Meta", "Google", "Anthropic", "OpenAI"]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_json(path: str) -> dict:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize(raw: dict, dates: list) -> dict:
    """
    Given raw[company][i] counts aligned to `dates`, return a dict of
    normalised percentages that sum to 100 at each time point.

    raw   : {company: [count, ...]}  — must include all COMPANIES
    dates : [str, ...]               — date labels, same length as value lists
    """
    n = len(dates)
    normed = {c: np.zeros(n) for c in COMPANIES}
    for i in range(n):
        total = sum(raw.get(c, [0] * n)[i] for c in COMPANIES)
        if total > 0:
            for c in COMPANIES:
                normed[c][i] = raw.get(c, [0] * n)[i] / total * 100.0
    return normed


def extract_dates_and_series(data: dict):
    """
    Accepts either:
      { "dates": [...], "series": { company: [...] } }   — explicit schema
      { company: [...] }                                  — flat schema where
                                                            keys include "dates"
    Returns (dates: list[str], raw: dict[str, list[float]])
    """
    if "dates" in data and "series" in data:
        return data["dates"], data["series"]
    elif "dates" in data:
        dates = data["dates"]
        raw   = {k: v for k, v in data.items() if k != "dates"}
        return dates, raw
    else:
        # Assume all keys are companies; derive dates from first series length
        first = next(iter(data.values()))
        dates = [str(i) for i in range(len(first))]
        return dates, data


def _save(fig, filename: str):
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved: {path}")


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def plot_mindshare(ax, dates: list, normed: dict, title: str):
    """Draw a stacked area chart of mind share onto `ax`."""
    x      = np.arange(len(dates))
    bottom = np.zeros(len(dates))

    for company in STACK_ORDER:
        vals = normed.get(company, np.zeros(len(dates)))
        ax.fill_between(
            x, bottom, bottom + vals,
            color=COLORS[company],
            alpha=0.82,
            linewidth=0,
            label=company,
        )
        # Thin border between layers for legibility
        ax.plot(x, bottom + vals, color="white", linewidth=0.3, alpha=0.5)
        bottom += vals

    # Axes formatting
    ax.set_xlim(0, len(dates) - 1)
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"])
    ax.set_ylabel("Mind Share")
    ax.set_title(title, fontweight="bold")

    # X ticks: show every 6th label to avoid clutter
    tick_indices = [i for i in range(len(dates)) if i % 6 == 0]
    ax.set_xticks(tick_indices)
    ax.set_xticklabels([dates[i] for i in tick_indices], rotation=45, ha="right", fontsize=8)

    ax.grid(axis="y", linestyle="--", linewidth=0.5, color="#cccccc", alpha=0.7)
    ax.grid(axis="x", visible=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def build_legend_handles():
    return [
        mpatches.Patch(color=COLORS[c], alpha=0.82, label=c)
        for c in reversed(STACK_ORDER)   # top-of-stack first in legend
    ]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    doc_data   = load_json(DOCUMENTS_JSON)
    actor_data = load_json(ACTORS_JSON)

    doc_dates,   doc_raw   = extract_dates_and_series(doc_data)
    actor_dates, actor_raw = extract_dates_and_series(actor_data)

    doc_normed   = normalize(doc_raw,   doc_dates)
    actor_normed = normalize(actor_raw, actor_dates)

    # ------------------------------------------------------------------
    # Combined figure (two panels, matches final_plots.py layout style)
    # ------------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
    fig.suptitle(
        "Provider Mind Share Over Time",
        fontweight="bold",
        fontsize=13,
    )

    plot_mindshare(axes[0], doc_dates,   doc_normed,   "(a) Documents (With Fuzzing)")
    plot_mindshare(axes[1], actor_dates, actor_normed, "(b) Actor Pairs (With Fuzzing)")

    handles = build_legend_handles()
    fig.legend(
        handles=handles,
        loc="lower center",
        ncol=len(COMPANIES),
        bbox_to_anchor=(0.5, -0.08),
        frameon=True,
        fontsize=9,
    )
    fig.tight_layout()
    _save(fig, "mindshare_combined.png")

    # ------------------------------------------------------------------
    # Individual figures
    # ------------------------------------------------------------------
    for dates, normed, title, fname in [
        (doc_dates,   doc_normed,   "Documents (With Fuzzing) — Mind Share",   "mindshare_documents.png"),
        (actor_dates, actor_normed, "Actor Pairs (With Fuzzing) — Mind Share", "mindshare_actor_pairs.png"),
    ]:
        fig, ax = plt.subplots(figsize=(6, 3.2))
        plot_mindshare(ax, dates, normed, title)
        handles = build_legend_handles()
        fig.legend(
            handles=handles,
            loc="lower center",
            ncol=len(COMPANIES),
            bbox_to_anchor=(0.5, -0.12),
            frameon=True,
            fontsize=9,
        )
        fig.tight_layout()
        _save(fig, fname)


if __name__ == "__main__":
    main()