"""Prototype: Panel 5 -- pop-weighted score vs satisfaction over time, with
score-satisfaction reliability (Pearson r across providers) on a secondary axis.

Usage:
  python scripts/dashboard/panel5_score_sat_reliability.py \\
    --run-dir sandbox/experiments/_core_privacy/llm/baseline_s42_sonnet/seeds/seed_42
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr


def compute_series(rounds, smooth_window=3):
    rnds = []
    score_w = []   # market-weighted average score
    sat_w = []     # population-weighted average satisfaction
    rel = []       # Pearson r between score and satisfaction across providers

    for h in rounds:
        rnds.append(h["round"])
        scores = h.get("scores", {}) or {}
        cd = h.get("consumer_data", {}) or {}
        ms = cd.get("market_shares", {}) or {}
        psat = cd.get("provider_satisfaction", {}) or {}

        provs = sorted(scores.keys())
        if not provs:
            score_w.append(np.nan); sat_w.append(np.nan); rel.append(np.nan)
            continue

        sv = np.array([float(scores.get(p, 0.0)) for p in provs])
        mv = np.array([float(ms.get(p, 0.0)) for p in provs])
        psv = np.array([float(psat.get(p, 0.0)) for p in provs])

        if mv.sum() > 0:
            score_w.append(float((sv * mv).sum() / mv.sum()))
        else:
            score_w.append(float(sv.mean()))

        avg_sat = cd.get("avg_satisfaction")
        if avg_sat is None:
            sat_w.append(float((psv * mv).sum() / mv.sum()) if mv.sum() > 0 else float(psv.mean()))
        else:
            sat_w.append(float(avg_sat))

        if sv.std() > 1e-6 and psv.std() > 1e-6:
            r, _ = pearsonr(sv, psv)
            rel.append(float(r))
        else:
            rel.append(np.nan)

    rnds = np.array(rnds)
    score_w = np.array(score_w)
    sat_w = np.array(sat_w)
    rel = np.array(rel)

    if smooth_window > 1:
        rel_smooth = np.full_like(rel, np.nan, dtype=float)
        for i in range(len(rel)):
            lo = max(0, i - smooth_window + 1)
            window = rel[lo:i + 1]
            window = window[~np.isnan(window)]
            if window.size:
                rel_smooth[i] = window.mean()
        rel = rel_smooth

    return rnds, score_w, sat_w, rel


def draw_panel(ax, rounds, smooth_window: int = 3):
    """Draw P5 onto a provided axis. Returns the secondary axis."""
    rnds, score_w, sat_w, rel = compute_series(rounds, smooth_window)
    _draw_lines_and_overlay(ax, rnds, score_w, sat_w, rel, smooth_window)


def _draw_lines_and_overlay(ax, rnds, score_w, sat_w, rel, smooth_window):

    has_score_above = bool(np.any(score_w >= sat_w))
    has_sat_above = bool(np.any(sat_w > score_w))

    if has_score_above:
        ax.fill_between(rnds, sat_w, score_w,
                        where=(score_w >= sat_w), color="#E76F51", alpha=0.18,
                        interpolate=True, label="gap (score > sat)")
    if has_sat_above:
        ax.fill_between(rnds, sat_w, score_w,
                        where=(score_w < sat_w), color="#1565C0", alpha=0.18,
                        interpolate=True, label="gap (sat > score)")

    ax.plot(rnds, score_w, color="#222", linewidth=2.2, label="Score (market-weighted)")
    ax.plot(rnds, sat_w, color="#2A9D8F", linewidth=2.2, label="Satisfaction (population-weighted)")

    ax.set_xlim(rnds[0], rnds[-1])
    ax.set_ylim(0, 1)
    ax.set_xlabel("Round", fontsize=11)
    ax.set_ylabel("Score / satisfaction", fontsize=11)
    ax.set_title("(e) Score vs satisfaction (with reliability)",
                 fontsize=13, loc="left", fontweight="bold")
    ax.tick_params(labelsize=10)
    ax.spines["top"].set_visible(False)
    ax.grid(True, alpha=0.25, linewidth=0.4)

    ax_r = ax.twinx()
    rel_min = np.nanmin(rel) if np.any(~np.isnan(rel)) else 0.0
    r_lo = -0.5 if rel_min > -0.5 else max(-1.0, rel_min - 0.1)
    ax_r.plot(rnds, rel, color="#9B5DE5", linewidth=1.6, linestyle="--",
              label=f"Reliability (Pearson r, rolling-{smooth_window})")
    ax_r.set_ylim(r_lo, 1.0)
    ax_r.set_ylabel("Score-sat reliability (Pearson r)", color="#9B5DE5", fontsize=11)
    ax_r.tick_params(axis="y", labelsize=10, colors="#9B5DE5")
    ax_r.spines["top"].set_visible(False)
    ax_r.spines["right"].set_color("#9B5DE5")

    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax_r.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="lower left", fontsize=7,
              frameon=True, framealpha=0.9, ncol=3,
              handlelength=1.4, columnspacing=0.8,
              labelspacing=0.25, borderpad=0.3)

    final_gap = float(score_w[-1] - sat_w[-1])
    final_rel = float(rel[-1]) if not np.isnan(rel[-1]) else float("nan")
    ax.text(0.99, 0.97,
            f"Final gap (g): {final_gap:+.3f}\nFinal reliability: {final_rel:+.2f}",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=9, color="#444",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#bbb"))


def render(run_dir: Path, out_path: Path, smooth_window: int):
    rounds = [json.loads(l) for l in (run_dir / "rounds.jsonl").read_text().splitlines() if l.strip()]
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    draw_panel(ax, rounds, smooth_window)
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
                    default=Path("output/dashboard/panel5_score_sat_reliability.png"))
    ap.add_argument("--smooth-window", type=int, default=3)
    args = ap.parse_args()
    render(args.run_dir, args.out, args.smooth_window)
