"""
Single-run ecosystem-loop figure (paper §5.1).

1x4 panel figure concretising the ecosystem loop on one LLM run:
  (a) market-share trajectories (stacked area)
  (b) incident + regulator-intervention timeline
  (c) portfolio allocations over time (rd solid, safety dotted; weighted mean bold)
  (d) per-benchmark dumbbell (endpoint score vs matched satisfaction)

Usage:
  python -m scripts.plots.paper.single_run_loop \\
    --run-dir sandbox/experiments/_llm_apr23_v1/llm/baseline_seed2_postid/seeds/seed_2
  python -m scripts.plots.paper.single_run_loop --run-dir <path> --out <pdf_path>
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np

from .. import paths as _paths
sys.path.insert(0, os.path.join(_paths.PROJECT_ROOT, "src"))
from plotting import get_provider_colors  # type: ignore  # noqa: E402

from ..portfolio import extract_portfolio_data, _weighted_mean_alloc  # noqa: E402
from ..per_benchmark import per_benchmark_from_rows, dumbbell_from_df  # noqa: E402


SEVERITY_MARKERS = {"minor": ".", "moderate": "s", "major": "^", "critical": "X"}
SEVERITY_SIZES = {"minor": 28, "moderate": 52, "major": 88, "critical": 130}
SEVERITY_COLORS = {"minor": "#AAAAAA", "moderate": "#E9C46A",
                   "major": "#E76F51", "critical": "#D62828"}

ESCALATION_ORDER = [
    "request_voluntary_commitment", "publish_advisory",
    "mandate_safety_disclosure", "commission_audit",
    "impose_sanction", "emergency_investigation",
]
INTERVENTION_COLORS = {
    "request_voluntary_commitment": "#90BE6D",
    "publish_advisory":             "#F9C74F",
    "mandate_safety_disclosure":    "#F8961E",
    "commission_audit":             "#F3722C",
    "impose_sanction":              "#D62828",
    "emergency_investigation":      "#9B2226",
}
INTERVENTION_LW = {
    a: 1.2 + 1.8 * (i / (len(ESCALATION_ORDER) - 1))
    for i, a in enumerate(ESCALATION_ORDER)
}
INTERVENTION_LABELS = {
    "request_voluntary_commitment": "Voluntary",
    "publish_advisory":             "Advisory",
    "mandate_safety_disclosure":    "Disclosure",
    "commission_audit":             "Audit",
    "impose_sanction":              "Sanction",
    "emergency_investigation":      "Emergency",
}


def _load_rounds(run_dir: Path) -> list:
    path = run_dir / "rounds.jsonl"
    if not path.is_file():
        raise FileNotFoundError(f"{path} not found")
    with path.open() as f:
        return [json.loads(line) for line in f if line.strip()]


# ---------- panel (a): market share ----------
def _panel_market_share(ax, rounds, providers, p_colors):
    rnds = [h["round"] for h in rounds]
    share = {p: [] for p in providers}
    for h in rounds:
        ms = h.get("consumer_data", {}).get("market_shares", {}) or {}
        for p in providers:
            share[p].append(float(ms.get(p, 0.0) or 0.0))
    bottom = np.zeros(len(rnds))
    for p in providers:
        vals = np.array(share[p])
        ax.fill_between(rnds, bottom, bottom + vals,
                        color=p_colors[p], alpha=0.85, linewidth=0)
        bottom += vals
    ax.set_xlim(rnds[0], rnds[-1])
    ax.set_ylim(0, max(1.0, bottom.max() * 1.02))
    ax.set_title("(a) Market share", fontsize=13, loc="left", fontweight="bold")
    ax.set_xlabel("Round", fontsize=12)
    ax.set_ylabel("Share", fontsize=12)
    ax.tick_params(labelsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


# ---------- panel (b): incidents + interventions ----------
def _panel_incidents(ax, rounds, providers):
    prov_idx = {p: i for i, p in enumerate(providers)}
    sev_counts = {k: 0 for k in SEVERITY_MARKERS}
    for h in rounds:
        for inc in h.get("incidents", []) or []:
            p = inc.get("provider", "")
            if p not in prov_idx:
                continue
            sev = inc.get("severity", "minor")
            sev_counts[sev] = sev_counts.get(sev, 0) + 1
            ax.scatter(h["round"], prov_idx[p],
                       marker=SEVERITY_MARKERS.get(sev, "o"),
                       s=SEVERITY_SIZES.get(sev, 18),
                       color=SEVERITY_COLORS.get(sev, "#999"),
                       alpha=0.9, edgecolors="black",
                       linewidths=0.3, zorder=5)

    for h in rounds:
        rd = h.get("regulator_data", {}) or {}
        for iv in rd.get("interventions", []) or []:
            action = iv.get("type") or iv.get("action", "unknown") if isinstance(iv, dict) else iv
            color = INTERVENTION_COLORS.get(action, "#888")
            lw = INTERVENTION_LW.get(action, 0.9)
            ax.axvline(h["round"], color=color, linewidth=lw,
                       alpha=0.7, linestyle="--", zorder=3)

    rnds = [h["round"] for h in rounds]
    ax.set_xlim(rnds[0], rnds[-1])
    ax.set_yticks(range(len(providers)))
    ax.set_yticklabels([p.split()[0] for p in providers], fontsize=11)
    ax.set_title("(b) Incidents \\& interventions",
                 fontsize=13, loc="left", fontweight="bold")
    ax.set_xlabel("Round", fontsize=12)
    ax.tick_params(axis="x", labelsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    return sev_counts


# ---------- panel (c): allocations over time ----------
def _panel_allocations(ax, rounds, providers, portfolios, p_colors):
    T = len(rounds)
    xs = np.arange(T)
    for p in providers:
        c = p_colors[p]
        ax.plot(xs, portfolios[p]["rd"], color=c, linestyle="-",
                linewidth=0.8, alpha=0.75)
        ax.plot(xs, portfolios[p]["safety"], color=c, linestyle=":",
                linewidth=0.8, alpha=0.75)
    wm_rd = _weighted_mean_alloc(rounds, providers, portfolios, "rd")
    wm_sf = _weighted_mean_alloc(rounds, providers, portfolios, "safety")
    ax.plot(xs, wm_rd, color="black", linestyle="-", linewidth=2.0,
            label="mean R\\&D")
    ax.plot(xs, wm_sf, color="black", linestyle=":", linewidth=2.0,
            label="mean safety")
    ax.set_xlim(0, T - 1)
    ax.set_ylim(0, 1)
    ax.set_title("(c) Portfolio allocations",
                 fontsize=13, loc="left", fontweight="bold")
    ax.set_xlabel("Round", fontsize=12)
    ax.set_ylabel("Allocation fraction", fontsize=12)
    ax.tick_params(labelsize=10)
    ax.grid(True, alpha=0.25, linewidth=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


# ---------- panel (d): per-benchmark dumbbell ----------
def _panel_dumbbell(ax, rounds):
    df = per_benchmark_from_rows(rounds)
    g = df.groupby("benchmark").agg(
        score=("score", "mean"),
        matched=("clean_matched", "mean"),
        gap=("clean_gap", "mean"),
    ).reset_index().sort_values("gap", ascending=False).reset_index(drop=True)

    y_pos = np.arange(len(g))
    for i, row in g.iterrows():
        color = "#C62828" if row.gap > 0 else "#1565C0"
        ax.plot([row.matched, row.score], [i, i],
                color=color, lw=2.2, zorder=1, alpha=0.6)
        ax.scatter(row.matched, i, color="#6a6a6a", s=32, zorder=3,
                   edgecolor="black", linewidth=0.5,
                   label="matched sat." if i == 0 else None)
        ax.scatter(row.score, i, color=color, s=42, zorder=3,
                   edgecolor="black", linewidth=0.5,
                   label="score" if i == 0 else None)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(g["benchmark"], fontsize=10)
    ax.invert_yaxis()
    ax.set_title("(d) Per-benchmark gap",
                 fontsize=13, loc="left", fontweight="bold")
    ax.set_xlabel("Value", fontsize=12)
    ax.tick_params(axis="x", labelsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def main(run_dir: Path, out_path: Path, show: bool = False,
         orientation: str = "horizontal"):
    rounds = _load_rounds(run_dir)
    providers, T, portfolios, final_shares = extract_portfolio_data(rounds)
    # Order providers by final share (largest first) for consistent legend
    providers = sorted(providers, key=lambda p: -final_shares.get(p, 0.0))
    p_colors = get_provider_colors(providers)

    plt.rcParams["figure.constrained_layout.use"] = False
    plt.rcParams["figure.autolayout"] = False

    if orientation == "vertical":
        fig, axes = plt.subplots(4, 1, figsize=(6.5, 16.0),
                                 gridspec_kw={"hspace": 0.50,
                                              "height_ratios": [1.0, 1.0, 1.0, 1.25]})
        ax_a, ax_b, ax_c, ax_d = axes
    elif orientation == "grid":
        fig, axes = plt.subplots(2, 2, figsize=(11.0, 9.5),
                                 gridspec_kw={"hspace": 0.42, "wspace": 0.32,
                                              "width_ratios": [1.0, 1.15]})
        ax_a, ax_b = axes[0]
        ax_c, ax_d = axes[1]
    else:  # horizontal
        fig, axes = plt.subplots(1, 4, figsize=(14.0, 4.4),
                                 gridspec_kw={"wspace": 0.55,
                                              "width_ratios": [1.0, 1.0, 1.0, 1.25]})
        ax_a, ax_b, ax_c, ax_d = axes

    _panel_market_share(ax_a, rounds, providers, p_colors)
    sev_counts = _panel_incidents(ax_b, rounds, providers)
    _panel_allocations(ax_c, rounds, providers, portfolios, p_colors)
    _panel_dumbbell(ax_d, rounds)

    # Shared figure-level legend at bottom: providers | severity | interventions
    prov_handles = [
        mlines.Line2D([0], [0], color=p_colors[p], linewidth=3, label=p)
        for p in providers
    ]
    _leg_marker = {"minor": 7, "moderate": 10, "major": 12, "critical": 14}
    sev_handles = [
        mlines.Line2D([0], [0], marker=SEVERITY_MARKERS[s], color="w",
                      markerfacecolor=SEVERITY_COLORS[s], markeredgecolor="black",
                      markeredgewidth=0.5,
                      markersize=_leg_marker[s],
                      linestyle="None",
                      label=f"{s} ({sev_counts.get(s, 0)})")
        for s in ("minor", "moderate", "major", "critical")
    ]
    intv_handles = [
        mlines.Line2D([0], [0], color=INTERVENTION_COLORS[a],
                      linewidth=INTERVENTION_LW[a] + 0.8, alpha=0.85,
                      linestyle="--", label=INTERVENTION_LABELS[a])
        for a in ESCALATION_ORDER
    ]

    if orientation == "vertical":
        fig.subplots_adjust(left=0.13, right=0.97, top=0.975, bottom=0.18,
                            hspace=0.55)
        # Three legend rows stacked at the bottom (narrow column).
        leg1 = fig.legend(handles=prov_handles, loc="upper center",
                          bbox_to_anchor=(0.5, 0.135), ncol=3,
                          fontsize=10, frameon=False, handlelength=1.8,
                          columnspacing=1.6, title="Providers",
                          title_fontsize=11)
        leg2 = fig.legend(handles=sev_handles, loc="upper center",
                          bbox_to_anchor=(0.5, 0.080), ncol=4,
                          fontsize=10, frameon=False, handlelength=1.2,
                          columnspacing=1.2, title="Incident severity",
                          title_fontsize=11)
        leg3 = fig.legend(handles=intv_handles, loc="upper center",
                          bbox_to_anchor=(0.5, 0.038), ncol=3,
                          fontsize=10, frameon=False, handlelength=1.6,
                          columnspacing=1.2, title="Regulator action ladder",
                          title_fontsize=11)
    elif orientation == "grid":
        fig.subplots_adjust(left=0.07, right=0.985, top=0.965, bottom=0.16,
                            hspace=0.42, wspace=0.32)
        # Providers row 1; severity + interventions row 2 (square aspect → fits).
        leg1 = fig.legend(handles=prov_handles, loc="upper center",
                          bbox_to_anchor=(0.5, 0.115), ncol=len(providers),
                          fontsize=10, frameon=False, handlelength=1.8,
                          columnspacing=1.6, title="Providers",
                          title_fontsize=11)
        leg2 = fig.legend(handles=sev_handles, loc="upper left",
                          bbox_to_anchor=(0.07, 0.055), ncol=len(sev_handles),
                          fontsize=10, frameon=False, handlelength=1.2,
                          columnspacing=1.2, title="Incident severity",
                          title_fontsize=11)
        leg3 = fig.legend(handles=intv_handles, loc="upper left",
                          bbox_to_anchor=(0.47, 0.055), ncol=len(intv_handles),
                          fontsize=10, frameon=False, handlelength=1.4,
                          columnspacing=1.2, title="Regulator action ladder",
                          title_fontsize=11)
    else:  # horizontal
        fig.subplots_adjust(left=0.055, right=0.995, top=0.94, bottom=0.28,
                            wspace=0.55)
        # Row 1 (top): providers.  Row 2 (bottom): severity + intervention ladder.
        leg1 = fig.legend(handles=prov_handles, loc="upper center",
                          bbox_to_anchor=(0.5, 0.22), ncol=len(providers),
                          fontsize=11, frameon=False, handlelength=1.8,
                          columnspacing=1.8, title="Providers",
                          title_fontsize=12)
        leg2 = fig.legend(handles=sev_handles, loc="upper left",
                          bbox_to_anchor=(0.06, 0.10), ncol=len(sev_handles),
                          fontsize=11, frameon=False, handlelength=1.2,
                          columnspacing=1.2, title="Incident severity",
                          title_fontsize=12)
        leg3 = fig.legend(handles=intv_handles, loc="upper left",
                          bbox_to_anchor=(0.38, 0.10), ncol=len(intv_handles),
                          fontsize=11, frameon=False, handlelength=1.6,
                          columnspacing=1.2, title="Regulator action ladder",
                          title_fontsize=12)
    fig.add_artist(leg1)
    fig.add_artist(leg2)
    fig.add_artist(leg3)

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    png_path = out_path.with_suffix(".png")
    fig.savefig(png_path, dpi=150, bbox_inches="tight")
    print(f"Saved: {out_path}")
    print(f"Saved: {png_path}")
    if show:
        plt.show()
    plt.close(fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument(
        "--run-dir", type=Path, required=True,
        help="Path to a single-run directory containing rounds.jsonl",
    )
    ap.add_argument(
        "--out", type=Path,
        default=Path(_paths.paper_dir()) / "single_run_loop.pdf",
        help="Output PDF path (png written alongside)",
    )
    ap.add_argument("--show", action="store_true")
    ap.add_argument(
        "--orientation", choices=["horizontal", "vertical", "grid"],
        default="horizontal",
        help="Layout: horizontal (1x4 paper default), vertical (4x1 poster), grid (2x2)",
    )
    args = ap.parse_args()
    out = args.out
    default_out = Path(_paths.paper_dir()) / "single_run_loop.pdf"
    if args.orientation != "horizontal" and out == default_out:
        out = Path(_paths.paper_dir()) / f"single_run_loop_{args.orientation}.pdf"
    main(args.run_dir, out, args.show, args.orientation)
