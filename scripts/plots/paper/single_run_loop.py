"""
Single-run ecosystem-loop figure (paper §5.1).

2x2 panel figure concretising the ecosystem loop on one LLM run:
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
SEVERITY_SIZES = {"minor": 10, "moderate": 18, "major": 30, "critical": 45}
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
    a: 0.5 + 1.0 * (i / (len(ESCALATION_ORDER) - 1))
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
    ax.set_title("(a) Market share", fontsize=9, loc="left", fontweight="bold")
    ax.set_xlabel("Round", fontsize=7)
    ax.set_ylabel("Share", fontsize=7)
    ax.tick_params(labelsize=6)
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
    ax.set_yticklabels([p.split()[0] for p in providers], fontsize=6)
    ax.set_title("(b) Incidents \\& regulator interventions",
                 fontsize=9, loc="left", fontweight="bold")
    ax.set_xlabel("Round", fontsize=7)
    ax.tick_params(axis="x", labelsize=6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    sev_handles = [
        mlines.Line2D([0], [0], marker=SEVERITY_MARKERS[s], color="w",
                      markerfacecolor=SEVERITY_COLORS[s], markeredgecolor="black",
                      markeredgewidth=0.3, markersize=SEVERITY_SIZES[s] ** 0.5,
                      linestyle="None",
                      label=f"{s} ({sev_counts.get(s, 0)})")
        for s in ("minor", "moderate", "major", "critical")
    ]
    intv_handles = [
        mlines.Line2D([0], [0], color=INTERVENTION_COLORS[a],
                      linewidth=INTERVENTION_LW[a] + 0.2, alpha=0.8,
                      linestyle="--", label=INTERVENTION_LABELS[a])
        for a in ESCALATION_ORDER
    ]
    ax.legend(handles=sev_handles + intv_handles,
              loc="upper left", bbox_to_anchor=(1.01, 1.02),
              fontsize=5, frameon=False, handlelength=1.6,
              handletextpad=0.4, borderaxespad=0.0, labelspacing=0.3)


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
    ax.set_title("(c) Portfolio allocations (market-share-weighted mean in bold)",
                 fontsize=9, loc="left", fontweight="bold")
    ax.set_xlabel("Round", fontsize=7)
    ax.set_ylabel("Allocation fraction", fontsize=7)
    ax.tick_params(labelsize=6)
    ax.grid(True, alpha=0.25, linewidth=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.02),
              fontsize=6, frameon=False, handlelength=2.0)


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
    ax.set_yticklabels(g["benchmark"], fontsize=6)
    ax.invert_yaxis()
    ax.set_title(f"(d) Per-benchmark gap at round {rounds[-1]['round']}",
                 fontsize=9, loc="left", fontweight="bold")
    ax.set_xlabel("Value", fontsize=7)
    ax.tick_params(axis="x", labelsize=6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(loc="lower right", fontsize=5, frameon=False,
              handletextpad=0.4, borderaxespad=0.3)


def main(run_dir: Path, out_path: Path, show: bool = False):
    rounds = _load_rounds(run_dir)
    providers, T, portfolios, final_shares = extract_portfolio_data(rounds)
    # Order providers by final share (largest first) for consistent legend
    providers = sorted(providers, key=lambda p: -final_shares.get(p, 0.0))
    p_colors = get_provider_colors(providers)

    fig, axes = plt.subplots(2, 2, figsize=(7.5, 5.0))
    (ax_a, ax_b), (ax_c, ax_d) = axes

    _panel_market_share(ax_a, rounds, providers, p_colors)
    _panel_incidents(ax_b, rounds, providers)
    _panel_allocations(ax_c, rounds, providers, portfolios, p_colors)
    _panel_dumbbell(ax_d, rounds)

    # Shared provider legend at figure bottom
    prov_handles = [
        mlines.Line2D([0], [0], color=p_colors[p], linewidth=3,
                      label=p)
        for p in providers
    ]
    fig.legend(handles=prov_handles, loc="lower center",
               bbox_to_anchor=(0.5, -0.02), ncol=len(providers),
               fontsize=7, frameon=False, handlelength=1.8,
               columnspacing=1.2)

    fig.tight_layout(rect=[0, 0.035, 1, 1.0])

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
    args = ap.parse_args()
    main(args.run_dir, args.out, args.show)
