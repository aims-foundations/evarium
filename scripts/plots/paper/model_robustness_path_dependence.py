"""Cross-model path-dependence: Orion market-share trajectory under
``baseline`` across (seed, model) cells, with all other LLM runs in grey.

Mirrors the design of ``incident_path_dependence.py`` but for the cross-model
robustness appendix:
    - Background (grey, thin):  every full 40-round LLM run in _core_privacy/
                                that is NOT one of the highlighted cells.
    - Highlighted (color+style): baseline @ seeds {42, 43, 44} × models
                                {sonnet, opus, gpt55}, where data exists.
                                Color = model, linestyle = seed.
                                s44 has only Sonnet (Opus and GPT-5.5 don't
                                cover seed 44); the missing two cells are
                                simply not drawn.

Critical incidents are marked on every line; major incidents on highlighted
lines only (so the background stays readable).

Usage:
    python -m scripts.plots.paper.model_robustness_path_dependence
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
from .model_robustness import (MODEL_ORDER, MODEL_COLORS, MODEL_LABELS,
                                discover_paired_runs)

PROVIDER = "Orion Labs"
HIGHLIGHT_COND = "baseline"
HIGHLIGHT_SEEDS = [42, 43, 44]
SEED_LINESTYLES = {42: "-", 43: "--", 44: ":"}

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


def main(batch: str, out_dir: str, min_rounds: int = 40, poster: bool = False):
    runs = []
    for cond, seed, model, seed_dir, jsonl in discover_paired_runs(batch, min_rounds):
        xs, ys, inc, n = load_trajectory(jsonl)
        is_highlight = (cond == HIGHLIGHT_COND and seed in HIGHLIGHT_SEEDS)
        runs.append({
            "cond": cond, "seed": seed, "model": model,
            "xs": xs, "ys": ys, "inc": inc,
            "name": f"{cond}_s{seed}_{model}",
            "final": ys[-1], "highlight": is_highlight,
        })
    if not runs:
        raise FileNotFoundError(
            f"No {min_rounds}-round runs found under sandbox/{batch} "
            f"or hf_data_staging/{batch.lstrip('_')}"
        )

    n_total = len(runs)
    highlights = [r for r in runs if r["highlight"]]
    background = [r for r in runs if not r["highlight"]]

    fig, ax = plt.subplots(figsize=(7.0, 6.0) if poster else (10, 5.5))

    # Background: every non-highlighted (cond, seed, model) trajectory in grey.
    for r in background:
        ax.plot(r["xs"], r["ys"], color="#808080", lw=0.8, alpha=0.35, zorder=2)
        for rnd, sev in r["inc"]:
            if sev != "critical":
                continue
            mk, c, sz = SEV_MARK[sev]
            y = r["ys"][rnd] if rnd < len(r["ys"]) else 0
            ax.scatter(rnd, y, marker=mk, s=sz * 0.5, color=c,
                       edgecolors="black", linewidths=0.25, alpha=0.4, zorder=3)

    # Highlights: baseline @ {42,43,44} × {sonnet,opus,gpt55}, where data exists.
    # Sort so legend prints in (seed, model) reading order.
    highlights.sort(key=lambda r: (HIGHLIGHT_SEEDS.index(r["seed"]),
                                    MODEL_ORDER.index(r["model"])))
    for r in highlights:
        ls = SEED_LINESTYLES[r["seed"]]
        color = MODEL_COLORS[r["model"]]
        ax.plot(r["xs"], r["ys"], color=color, lw=2.0, alpha=0.95,
                linestyle=ls, zorder=5)
        for rnd, sev in r["inc"]:
            mk, c, sz = SEV_MARK[sev]
            y = r["ys"][rnd] if rnd < len(r["ys"]) else 0
            ax.scatter(rnd, y, marker=mk, s=sz * 1.2, color=c,
                       edgecolors="black", linewidths=0.6, zorder=6)

    ax.set_xlabel("Round", fontsize=10)
    ax.set_ylabel(f"Market share — {PROVIDER}", fontsize=10)
    ax.set_ylim(0, 1.0)
    ax.set_xlim(0, max(r["xs"][-1] for r in runs))
    ax.grid(True, alpha=0.25, linewidth=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Factored legend: model = color, seed = linestyle; then incidents + background.
    model_handles = [
        Line2D([0], [0], color=MODEL_COLORS[m], lw=2.5, linestyle="-",
               label=MODEL_LABELS[m])
        for m in MODEL_ORDER
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
    ax.legend(handles=model_handles + seed_handles + marker_handles,
              loc="lower right", fontsize=8, frameon=True, framealpha=0.9,
              ncol=1)

    n_highlighted = len(highlights)
    n_expected = len(HIGHLIGHT_SEEDS) * len(MODEL_ORDER)
    n_missing = n_expected - n_highlighted
    coverage = (
        f"{n_highlighted}/{n_expected} cells"
        if n_missing == 0
        else f"{n_highlighted} of {n_expected} cells; {n_missing} missing"
    )
    title = (
        f"Cross-model path dependence: {PROVIDER} market share under {HIGHLIGHT_COND}\n"
        f"Highlighted: seeds {HIGHLIGHT_SEEDS} × {len(MODEL_ORDER)} models "
        f"({coverage}). N={n_total} total LLM runs."
    )
    ax.set_title(title, loc="left", fontsize=10.5)

    os.makedirs(out_dir, exist_ok=True)
    suffix = "_poster" if poster else ""
    pdf = os.path.join(out_dir, f"model_robustness_path_dependence{suffix}.pdf")
    png = os.path.join(out_dir, f"model_robustness_path_dependence{suffix}.png")
    fig.tight_layout()
    fig.savefig(pdf, dpi=300, bbox_inches="tight")
    fig.savefig(png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {pdf}")
    print(f"Saved {png}")
    print(f"Highlighted {n_highlighted}/{len(HIGHLIGHT_SEEDS) * len(MODEL_ORDER)} "
          f"(seed × model) cells; {n_missing} missing.")


def cli():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", default="_core_privacy")
    ap.add_argument("--out-dir", default=None)
    ap.add_argument(
        "--poster", action="store_true",
        help="Render closer-to-square (~7x6) variant for poster use; "
             "writes model_robustness_path_dependence_poster.{pdf,png}",
    )
    args = ap.parse_args()
    out_dir = args.out_dir or _paths.paper_dir()
    main(args.batch, out_dir, poster=args.poster)


if __name__ == "__main__":
    cli()
