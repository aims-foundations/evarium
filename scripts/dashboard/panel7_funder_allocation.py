"""Prototype: Panel 7 -- cumulative funder allocation per provider over time.

Stacked area, one band per provider, per round = total capital deployed by ALL
funders to that provider in that round, cumulated across rounds. Slope = funding
velocity; band thickness at endpoint = total accumulated capital.

Usage:
  python scripts/dashboard/panel7_funder_allocation.py \\
    --run-dir sandbox/experiments/_core_privacy/llm/baseline_s42_sonnet/seeds/seed_42
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
from plotting import get_provider_colors  # noqa: E402


def draw_panel(ax, rounds):
    providers = sorted(rounds[-1]["scores"].keys())
    rnds = [h["round"] for h in rounds]

    per_round = {p: [] for p in providers}
    for h in rounds:
        deployed_this_round = {p: 0.0 for p in providers}
        allocs = (h.get("funder_data", {}) or {}).get("allocations", {}) or {}
        for funder_allocs in allocs.values():
            for p, amt in (funder_allocs or {}).items():
                if p in deployed_this_round:
                    deployed_this_round[p] += float(amt)
        for p in providers:
            per_round[p].append(deployed_this_round[p])

    cumulative = {p: np.cumsum(per_round[p]) for p in providers}

    order = sorted(providers, key=lambda p: -cumulative[p][-1])
    p_colors = get_provider_colors(providers)

    bottom = np.zeros(len(rnds))
    legend_handles = []
    for p in order:
        cum = cumulative[p]
        ax.fill_between(rnds, bottom, bottom + cum,
                        color=p_colors[p], alpha=0.85, linewidth=0.4,
                        edgecolor="white")
        legend_handles.append((p, cum[-1]))
        bottom += cum

    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: rf"\${x/1e6:.0f}M"))
    ax.set_xlim(rnds[0], rnds[-1])
    ax.set_ylim(0, bottom.max() * 1.02 if bottom.max() > 0 else 1)
    ax.set_xlabel("Round", fontsize=11)
    ax.set_ylabel(r"Cumulative funder deployment (\$M)", fontsize=11)
    ax.set_title("(g) Funder allocation (cumulative)",
                 fontsize=13, loc="left", fontweight="bold")
    ax.tick_params(axis="x", labelsize=10)
    ax.tick_params(axis="y", labelsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    from matplotlib.patches import Patch
    handles = [Patch(facecolor=p_colors[p], alpha=0.85,
                     label=rf"{p}  (\${tot/1e6:.0f}M)") for p, tot in legend_handles]
    ax.legend(handles=handles, loc="upper left", fontsize=7,
              frameon=True, framealpha=0.92, ncol=3,
              handlelength=1.4, columnspacing=0.8,
              labelspacing=0.25, borderpad=0.3)

    total = bottom[-1]
    n_funders = len({f for h in rounds
                     for f in ((h.get("funder_data", {}) or {}).get("allocations") or {}).keys()})
    ax.text(0.99, 0.97,
            rf"Total deployed: \${total/1e9:.1f}B across {n_funders} funders",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=9, color="#444",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#bbb"))


def render(run_dir: Path, out_path: Path):
    rounds = [json.loads(l) for l in (run_dir / "rounds.jsonl").read_text().splitlines() if l.strip()]
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    draw_panel(ax, rounds)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    fig.savefig(out_path.with_suffix(".pdf"), bbox_inches="tight")
    print(f"Saved: {out_path}")
    print(f"Saved: {out_path.with_suffix('.pdf')}")
    plt.close(fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--run-dir", type=Path, required=True)
    ap.add_argument("--out", type=Path,
                    default=Path("output/dashboard/panel7_funder_allocation.png"))
    args = ap.parse_args()
    render(args.run_dir, args.out)
