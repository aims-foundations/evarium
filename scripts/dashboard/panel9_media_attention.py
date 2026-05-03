"""Prototype: Panel 9 -- per-provider media attention share over time.

media_data.provider_attention values overlap (multiple providers can be in the
news at once), so we normalize per round to a share-of-attention (sums to 1).
Stacked area, one band per provider; band thickness = relative narrative footprint.

Usage:
  python scripts/dashboard/panel9_media_attention.py \\
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

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
from plotting import get_provider_colors  # noqa: E402


def draw_panel(ax, rounds):
    providers = sorted(rounds[-1]["scores"].keys())
    rnds = [h["round"] for h in rounds]

    # Per-round per-provider attention, normalized to share-of-attention
    share = {p: [] for p in providers}
    sentiment = []
    for h in rounds:
        md = h.get("media_data", {}) or {}
        attn = md.get("provider_attention", {}) or {}
        sentiment.append(float(md.get("sentiment", 0.0)))
        raw = np.array([float(attn.get(p, 0.0)) for p in providers])
        total = raw.sum()
        if total > 0:
            normed = raw / total
        else:
            normed = np.full_like(raw, 1.0 / len(providers))
        for i, p in enumerate(providers):
            share[p].append(float(normed[i]))

    # Order by final attention share (largest at bottom for visual stacking)
    final_share = {p: share[p][-1] for p in providers}
    order = sorted(providers, key=lambda p: -final_share[p])
    p_colors = get_provider_colors(providers)

    bottom = np.zeros(len(rnds))
    for p in order:
        s = np.array(share[p])
        ax.fill_between(rnds, bottom, bottom + s,
                        color=p_colors[p], alpha=0.85, linewidth=0.4,
                        edgecolor="white")
        bottom += s

    ax.set_xlim(rnds[0], rnds[-1])
    ax.set_ylim(0, 1)
    ax.set_xlabel("Round", fontsize=11)
    ax.set_ylabel("Share of media attention (normalized)", fontsize=11)
    ax.set_title("(i) Media attention share",
                 fontsize=13, loc="left", fontweight="bold")
    ax.tick_params(labelsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    from matplotlib.patches import Patch
    handles = [Patch(facecolor=p_colors[p], alpha=0.85,
                     label=f"{p}  ({final_share[p]*100:.0f}\\%)") for p in order]
    ax.legend(handles=handles, loc="upper left", fontsize=7,
              frameon=True, framealpha=0.92, ncol=3,
              handlelength=1.4, columnspacing=0.8,
              labelspacing=0.25, borderpad=0.3)

    avg_sent = float(np.mean(sentiment))
    final_sent = sentiment[-1]
    ax.text(0.99, 0.97,
            (f"Avg sentiment: {avg_sent:+.2f}, final: {final_sent:+.2f}\n"
             "(sentiment is global, not per-provider)"),
            transform=ax.transAxes, ha="right", va="top",
            fontsize=8, color="#444",
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
                    default=Path("output/dashboard/panel9_media_attention.png"))
    args = ap.parse_args()
    render(args.run_dir, args.out)
