"""Privacy-ladder path-dependence: Orion market-share trajectory across the
three focal privacy conditions (public_only / baseline / private_only) for
Claude Sonnet 4.6, with all other LLM runs in grey.

Mirrors model_robustness_path_dependence.py but flips the encoding:
    Color     = privacy condition  (matching privacy_gap_main.py color scheme)
    Linestyle = seed               (42=solid, 43=dashed, 44=dotted)
    Background (grey): every full 40-round LLM run in _core_privacy that is
                       NOT one of the 9 highlighted (cond, seed, sonnet) cells.

Critical incidents are marked on every line; major incidents on highlighted
lines only.

Usage:
    python -m scripts.plots.paper.privacy_ladder_path_dependence
"""
from __future__ import annotations
import argparse
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from .. import paths as _paths
from .model_robustness import discover_paired_runs

PROVIDER = "Orion Labs"
HIGHLIGHT_MODEL = "sonnet"
HIGHLIGHT_CONDS = ["public_only", "baseline", "private_only"]
HIGHLIGHT_SEEDS = [42, 43, 44]
SEED_LINESTYLES = {42: "-", 43: "--", 44: ":"}

COND_COLORS = {
    "public_only":  "#2c7fb8",  # blue   (matches privacy_gap_main)
    "baseline":     "#fec44f",  # yellow
    "private_only": "#b10026",  # dark red
}
COND_LABELS = {
    "public_only":  "public (13/0/0)",
    "baseline":     "baseline (8/3/2 mix)",
    "private_only": "private (cos=0.85)",
}

SEV_MARK = {
    "major":    ("^", "#E76F51", 50),
    "critical": ("X", "#D62828", 90),
}


def load_trajectory(jsonl_path: str):
    rounds = [json.loads(l) for l in open(jsonl_path) if l.strip()]
    xs, ys, incidents = [], [], []
    for r in rounds:
        xs.append(r["round"])
        ys.append(r["consumer_data"]["market_shares"].get(PROVIDER, 0.0))
        for inc in r.get("incidents", []):
            if inc.get("provider") == PROVIDER and inc.get("severity") in SEV_MARK:
                incidents.append((r["round"], inc["severity"]))
    return xs, ys, incidents, len(rounds)


def main(batch: str, out_dir: str, min_rounds: int = 40):
    runs = []
    for cond, seed, model, seed_dir, jsonl in discover_paired_runs(batch, min_rounds):
        xs, ys, inc, n = load_trajectory(jsonl)
        is_highlight = (
            model == HIGHLIGHT_MODEL
            and cond in HIGHLIGHT_CONDS
            and seed in HIGHLIGHT_SEEDS
        )
        runs.append({
            "cond": cond, "seed": seed, "model": model,
            "xs": xs, "ys": ys, "inc": inc,
            "highlight": is_highlight,
        })
    if not runs:
        raise FileNotFoundError(
            f"No {min_rounds}-round runs found under sandbox/{batch} "
            f"or hf_data_staging/{batch.lstrip('_')}"
        )

    n_total = len(runs)
    highlights = [r for r in runs if r["highlight"]]
    background = [r for r in runs if not r["highlight"]]

    fig, ax = plt.subplots(figsize=(10, 5.5))

    # Background: every non-highlighted run in grey
    for r in background:
        ax.plot(r["xs"], r["ys"], color="#808080", lw=0.8, alpha=0.35, zorder=2)
        for rnd, sev in r["inc"]:
            if sev != "critical":
                continue
            mk, c, sz = SEV_MARK[sev]
            y = r["ys"][rnd] if rnd < len(r["ys"]) else 0
            ax.scatter(rnd, y, marker=mk, s=sz * 0.5, color=c,
                       edgecolors="black", linewidths=0.25, alpha=0.4, zorder=3)

    # Highlights: condition x seed, sorted by condition order then seed
    highlights.sort(key=lambda r: (HIGHLIGHT_CONDS.index(r["cond"]),
                                   HIGHLIGHT_SEEDS.index(r["seed"])))
    for r in highlights:
        color = COND_COLORS[r["cond"]]
        ls = SEED_LINESTYLES[r["seed"]]
        ax.plot(r["xs"], r["ys"], color=color, lw=2.0, alpha=0.95,
                linestyle=ls, zorder=5)
        for rnd, sev in r["inc"]:
            mk, c, sz = SEV_MARK[sev]
            y = r["ys"][rnd] if rnd < len(r["ys"]) else 0
            ax.scatter(rnd, y, marker=mk, s=sz * 1.2, color=c,
                       edgecolors="black", linewidths=0.6, zorder=6)

    ax.set_xlabel("Round", fontsize=10)
    ax.set_ylabel(f"Market share - {PROVIDER}", fontsize=10)
    ax.set_ylim(0, 1.0)
    ax.set_xlim(0, max(r["xs"][-1] for r in runs))
    ax.grid(True, alpha=0.25, linewidth=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    cond_handles = [
        Line2D([0], [0], color=COND_COLORS[c], lw=2.5, linestyle="-",
               label=COND_LABELS[c])
        for c in HIGHLIGHT_CONDS
    ]
    seed_handles = [
        Line2D([0], [0], color="black", lw=1.5, linestyle=SEED_LINESTYLES[s],
               label=f"seed {s}")
        for s in HIGHLIGHT_SEEDS
    ]
    marker_handles = [
        Line2D([0], [0], marker="X", color="w", markerfacecolor="#D62828",
               markeredgecolor="black", markersize=10, linestyle="None",
               label="critical incident"),
        Line2D([0], [0], marker="^", color="w", markerfacecolor="#E76F51",
               markeredgecolor="black", markersize=8, linestyle="None",
               label="major incident (highlighted only)"),
        Line2D([0], [0], color="#808080", lw=1, alpha=0.6,
               label=f"other LLM runs (N={len(background)})"),
    ]
    ax.legend(handles=cond_handles + seed_handles + marker_handles,
              loc="upper center", bbox_to_anchor=(0.5, -0.13),
              ncol=5, fontsize=8, frameon=False,
              columnspacing=1.2, handletextpad=0.5)

    n_highlighted = len(highlights)
    n_expected = len(HIGHLIGHT_CONDS) * len(HIGHLIGHT_SEEDS)
    coverage = (
        f"{n_highlighted}/{n_expected} cells"
        if n_highlighted == n_expected
        else f"{n_highlighted} of {n_expected} cells"
    )
    title = (
        f"Privacy ladder path dependence: {PROVIDER} market share (Claude Sonnet 4.6)\n"
        f"Highlighted: seeds {HIGHLIGHT_SEEDS} x 3 conditions "
        f"({coverage}). N={n_total} total LLM runs."
    )
    ax.set_title(title, loc="left", fontsize=10.5)

    os.makedirs(out_dir, exist_ok=True)
    stem = "privacy_ladder_path_dependence"
    pdf = os.path.join(out_dir, f"{stem}.pdf")
    png = os.path.join(out_dir, f"{stem}.png")
    fig.tight_layout(rect=[0, 0.12, 1, 1])
    fig.savefig(pdf, dpi=300, bbox_inches="tight")
    fig.savefig(png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {pdf}")
    print(f"Saved {png}")
    print(f"Highlighted {n_highlighted}/{n_expected} (cond x seed) cells.")


def cli():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", default="_core_privacy")
    ap.add_argument("--out-dir", default=None)
    args = ap.parse_args()
    out_dir = args.out_dir or _paths.paper_dir()
    main(args.batch, out_dir)


if __name__ == "__main__":
    cli()
