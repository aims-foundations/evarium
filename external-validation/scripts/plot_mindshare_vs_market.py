"""
plot_mindshare_vs_market.py — 4-row x 3-col stacked area comparison panel.

Layout:
  Row 0 — Claude  (full_ecosystem_balanced / us / eu)   sim market share
  Row 1 — Qwen    (full_ecosystem_balanced / us / eu)   sim market share
  Row 2 — Llama   (full_ecosystem_balanced / us / eu)   sim market share
  Row 3 — [actor mentions stacked area] [document mentions stacked area] [blank]

Columns:
  Col 0 — Balanced regulatory preset
  Col 1 — US regulatory preset
  Col 2 — EU regulatory preset

All panels use the same stacked-area style as process_mindshare.py.
Sim market share uses one seed (seed_1) per model x preset combination.

Usage:
  python external-validation/scripts/plot_mindshare_vs_market.py [--out-dir external-validation/plots]
"""

from __future__ import annotations

import json
import os
import warnings
from pathlib import Path

import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------------------
# Tueplots NeurIPS styling (mirrors process_mindshare.py)
# ---------------------------------------------------------------------------
try:
    from tueplots import bundles as _tb
    _RC = _tb.neurips2024()
    _RC.pop("figure.figsize", None)
    if os.environ.get("MPLLATEX", "1") != "0":
        _RC["text.usetex"] = True
    mpl.rcParams.update(_RC)
except ImportError:
    warnings.warn("tueplots not installed — using default matplotlib style.", stacklevel=1)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_SCRIPT_DIR   = Path(__file__).resolve().parent
_VAL_DIR      = _SCRIPT_DIR.parent
_HF_DATA      = _VAL_DIR.parent / "hf_data"
_PROC_DIR     = _VAL_DIR / "data" / "processed"
DEFAULT_OUT   = _VAL_DIR / "plots"

# ---------------------------------------------------------------------------
# Provider colours — sim providers (match PROVIDER_COLORS in plot_validation.py)
# ---------------------------------------------------------------------------
SIM_PROVIDERS = ["Orion Labs", "Apex AI", "Genesis Systems", "Mirage AI", "OpenCore"]
SIM_COLORS = {
    "Orion Labs":      "#1f77b4",
    "Apex AI":         "#ff7f0e",
    "Genesis Systems": "#2ca02c",
    "Mirage AI":       "#d62728",
    "OpenCore":        "#9467bd",
}
SIM_STACK_ORDER = ["OpenCore", "Mirage AI", "Genesis Systems", "Apex AI", "Orion Labs"]

# Sim → real name mapping for legend labels
_SIM_TO_REAL = {
    "Orion Labs":      "OpenAI",
    "Apex AI":         "Anthropic",
    "Genesis Systems": "Google",
    "Mirage AI":       "Meta",
    "OpenCore":        "DeepSeek",
}

# Mindshare (real) providers — mapped to sim colors via provider analogs:
#   OpenAI -> Orion Labs, Anthropic -> Apex AI, Google -> Genesis Systems,
#   Meta -> Mirage AI, Deepseek -> OpenCore
MS_COMPANIES  = ["OpenAI", "Anthropic", "Google", "Meta", "Deepseek"]
MS_COLORS = {
    "OpenAI":    SIM_COLORS["Orion Labs"],
    "Anthropic": SIM_COLORS["Apex AI"],
    "Google":    SIM_COLORS["Genesis Systems"],
    "Meta":      SIM_COLORS["Mirage AI"],
    "Deepseek":  SIM_COLORS["OpenCore"],
}
MS_STACK_ORDER = ["Deepseek", "Meta", "Google", "Anthropic", "OpenAI"]

# ---------------------------------------------------------------------------
# LLM models x regulatory presets
# ---------------------------------------------------------------------------
MODELS = [
    ("Claude",  "claude_archive",  None),          # uses exp_011_full_ecosystem_balanced etc.
    ("Qwen",    "llm_core/qwen-235b",  None),
    ("Llama",   "llm_core/llama-70b",  None),
]

PRESETS = ["balanced", "us", "eu"]
PRESET_LABELS = {"balanced": "Balanced", "us": "US", "eu": "EU"}

SEED = "seed_1"

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_rounds(model_dir_key: str, preset: str) -> list[dict]:
    """
    Load rounds.jsonl for a given model directory key and regulatory preset.
    Returns list of round dicts (empty list if not found).
    """
    exp_name = f"full_ecosystem_{preset}"

    # Claude archive uses dated experiment folders
    if model_dir_key == "claude_archive":
        base = _HF_DATA / "claude_archive"
        # Find a matching folder (prefer _balanced/_us/_eu suffix, pick first)
        candidates = sorted(base.glob(f"*_{exp_name}"))
        if not candidates:
            return []
        rounds_path = candidates[0] / "rounds.jsonl"
    else:
        base = _HF_DATA / model_dir_key
        rounds_path = base / exp_name / "seeds" / SEED / "rounds.jsonl"

    if not rounds_path.exists():
        return []

    rounds = []
    with rounds_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rounds.append(json.loads(line))
    return rounds


def extract_market_shares(rounds: list[dict]) -> dict[str, list[float]]:
    """Return {provider: [share_per_round]} from rounds list."""
    series: dict[str, list[float]] = {p: [] for p in SIM_PROVIDERS}
    for r in rounds:
        ms = r.get("consumer_data", {}).get("market_shares", {})
        total = sum(ms.get(p, 0.0) for p in SIM_PROVIDERS)
        for p in SIM_PROVIDERS:
            val = ms.get(p, 0.0)
            series[p].append(val / total * 100.0 if total > 0 else 0.0)
    return series


def load_mindshare_json(path: Path):
    """Return (dates, series_dict) from a mindshare JSON file."""
    if not path.exists():
        return [], {}
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if "dates" in data and "series" in data:
        return data["dates"], data["series"]
    elif "dates" in data:
        dates = data["dates"]
        return dates, {k: v for k, v in data.items() if k not in ("dates", "title")}
    first = next(iter(data.values()))
    return [str(i) for i in range(len(first))], data


# ---------------------------------------------------------------------------
# Shared stacked-area drawing helper
# ---------------------------------------------------------------------------

def draw_stacked_area(
    ax: plt.Axes,
    x: np.ndarray,
    series: dict[str, list | np.ndarray],
    stack_order: list[str],
    colors: dict[str, str],
    xtick_labels: list[str] | None = None,
    xtick_step: int = 6,
    ylabel: str = "Share (%)",
) -> None:
    bottom = np.zeros(len(x))
    for company in stack_order:
        vals = np.array(series.get(company, np.zeros(len(x))), dtype=float)
        ax.fill_between(x, bottom, bottom + vals,
                        color=colors[company], alpha=0.82, linewidth=0)
        ax.plot(x, bottom + vals, color="white", linewidth=0.3, alpha=0.5)
        bottom += vals

    ax.set_xlim(0, len(x) - 1)
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=6)
    ax.set_ylabel(ylabel, fontsize=7)

    if xtick_labels is not None:
        tick_idx = [i for i in range(len(xtick_labels)) if i % xtick_step == 0]
        ax.set_xticks(tick_idx)
        ax.set_xticklabels([xtick_labels[i] for i in tick_idx],
                           rotation=45, ha="right", fontsize=6)
    else:
        tick_idx = [i for i in range(len(x)) if i % xtick_step == 0]
        ax.set_xticks(tick_idx)
        ax.set_xticklabels([str(x[i]) for i in tick_idx], fontsize=6)

    ax.grid(axis="y", linestyle="--", linewidth=0.4, color="#cccccc", alpha=0.7)
    ax.grid(axis="x", visible=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


# ---------------------------------------------------------------------------
# Main figure
# ---------------------------------------------------------------------------

def make_figure(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    # Load mindshare data
    actor_dates, actor_series = load_mindshare_json(_PROC_DIR / "actors_mentions.json")
    doc_dates,   doc_series   = load_mindshare_json(_PROC_DIR / "documents_mentions.json")

    # Normalise mindshare series to percent
    def norm_series(series, dates, companies):
        n = len(dates)
        normed = {}
        for c in companies:
            normed[c] = np.zeros(n)
        for i in range(n):
            total = sum(series.get(c, [0]*n)[i] for c in companies)
            if total > 0:
                for c in companies:
                    normed[c][i] = series.get(c, [0]*n)[i] / total * 100.0
        return normed

    actor_normed = norm_series(actor_series, actor_dates, MS_COMPANIES)
    doc_normed   = norm_series(doc_series,   doc_dates,   MS_COMPANIES)

    fig, axes = plt.subplots(4, 3, figsize=(13, 14))
    fig.suptitle(
        "Provider Mind Share (Real) vs Simulated Market Share by Model and Regulatory Preset",
        fontweight="bold", fontsize=11,
    )

    # -----------------------------------------------------------------------
    # Rows 0-2: sim market share per model x preset
    # -----------------------------------------------------------------------
    for row_idx, (model_label, model_dir_key, _) in enumerate(MODELS):
        for col_idx, preset in enumerate(PRESETS):
            ax = axes[row_idx, col_idx]
            rounds = load_rounds(model_dir_key, preset)

            if rounds:
                ms = extract_market_shares(rounds)
                x  = np.arange(len(rounds))
                draw_stacked_area(
                    ax, x, ms, SIM_STACK_ORDER, SIM_COLORS,
                    xtick_labels=[str(r["round"]) for r in rounds],
                    xtick_step=5,
                    ylabel="Market Share (%)",
                )
                ax.set_xlabel("Sim Round", fontsize=7)
            else:
                ax.text(0.5, 0.5, "No data", transform=ax.transAxes,
                        ha="center", va="center", fontsize=9, color="gray")

            title = f"{model_label} — {PRESET_LABELS[preset]}"
            ax.set_title(title, fontsize=8, fontweight="bold")

    # -----------------------------------------------------------------------
    # Row 3: actor mentions | document mentions | blank
    # -----------------------------------------------------------------------
    # Col 0 — Actor mentions
    ax_actor = axes[3, 0]
    if actor_dates:
        x = np.arange(len(actor_dates))
        draw_stacked_area(ax_actor, x, actor_normed, MS_STACK_ORDER, MS_COLORS,
                          xtick_labels=actor_dates, xtick_step=6,
                          ylabel="Mind Share (%)")
        ax_actor.set_xlabel("Date", fontsize=7)
    else:
        ax_actor.text(0.5, 0.5, "No data", transform=ax_actor.transAxes,
                      ha="center", va="center", fontsize=9, color="gray")
    ax_actor.set_title("Actor Mentions — Mind Share (Real)", fontsize=8, fontweight="bold")

    # Col 1 — Document mentions
    ax_doc = axes[3, 1]
    if doc_dates:
        x = np.arange(len(doc_dates))
        draw_stacked_area(ax_doc, x, doc_normed, MS_STACK_ORDER, MS_COLORS,
                          xtick_labels=doc_dates, xtick_step=6,
                          ylabel="Mind Share (%)")
        ax_doc.set_xlabel("Date", fontsize=7)
    else:
        ax_doc.text(0.5, 0.5, "No data", transform=ax_doc.transAxes,
                    ha="center", va="center", fontsize=9, color="gray")
    ax_doc.set_title("Document Mentions — Mind Share (Real)", fontsize=8, fontweight="bold")

    # Col 2 — Legend panel (keep axes visible but empty of data)
    ax_leg = axes[3, 2]
    ax_leg.set_axis_off()

    sim_handles = [
        mpatches.Patch(color=SIM_COLORS[p], alpha=0.82,
                       label=f"{p}  ({_SIM_TO_REAL[p]})")
        for p in reversed(SIM_STACK_ORDER)
    ]
    ax_leg.legend(
        handles=sim_handles,
        title="Providers  (sim name — real analog)",
        loc="center",
        frameon=True,
        fontsize=10,
        title_fontsize=10,
        handlelength=2,
        handleheight=1.4,
        borderpad=1.0,
        labelspacing=0.8,
    )

    fig.tight_layout()

    out_path = out_dir / "mindshare_vs_market_4x3.png"
    fig.savefig(out_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved: {out_path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    make_figure(args.out_dir)
