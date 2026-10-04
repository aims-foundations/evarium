"""Provider portfolio (rd / safety / product) evolution plots.

Per-run tool — writes into `<run_dir>/plots/` by default (use --output to override).
Not a paper-canonical figure; see `scripts.plots.paper.*` for those.

Three options:
  Option 1: Top-2 stacked area (by final market share)
  Option 3: Ternary trajectory (all 6 providers)
  Allocations-mean: Per-provider rd (solid) + safety (dotted) trajectories with
                    market-share-weighted mean overlaid in bold.

Usage:
    python -m scripts.plots.portfolio <run_dir>
"""
import argparse
import json
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from . import paths as _paths
sys.path.insert(0, os.path.join(_paths.PROJECT_ROOT, "src"))
from plotting import get_provider_colors, get_investment_colors  # type: ignore  # noqa: E402


def extract_portfolio_data(rounds: list):
    """Extract (providers, T, portfolios, final_shares) from a pre-loaded rounds list.

    Uses `effective_strategies` when present (actual execution), falling back to
    `strategies` (planned target) for older history.json formats.
    """
    providers = list(rounds[0]["strategies"].keys())
    T = len(rounds)
    def _alloc(r, p, k):
        es = r.get("effective_strategies", {}).get(p)
        if es is not None and k in es:
            return es[k]
        return r.get("strategies", {}).get(p, {}).get(k, 0.0)
    portfolios = {
        p: {k: np.array([_alloc(r, p, k) for r in rounds]) for k in ("rd", "safety", "product")}
        for p in providers
    }
    final_shares = rounds[-1].get("consumer_data", {}).get("market_shares", {})
    return providers, T, portfolios, final_shares


def _load(run_dir: Path):
    rounds = [json.loads(l) for l in (run_dir / "rounds.jsonl").open()]
    providers, T, portfolios, final_shares = extract_portfolio_data(rounds)
    return rounds, providers, T, portfolios, final_shares


def plot_top2_stacked(ax_list, providers, T, portfolios, final_shares, inv_colors):
    top2 = sorted(providers, key=lambda p: -final_shares.get(p, 0.0))[:2]
    xs = np.arange(T)
    for ax, p in zip(ax_list, top2):
        rd = portfolios[p]["rd"]
        sf = portfolios[p]["safety"]
        pd = portfolios[p]["product"]
        ax.stackplot(xs, rd, sf, pd,
                     colors=[inv_colors["rd"], inv_colors["safety"], inv_colors["product"]],
                     labels=["R\\&D", "Safety", "Product"] if mpl_uses_tex() else ["R&D", "Safety", "Product"],
                     alpha=0.85, edgecolor="white", linewidth=0.3)
        ax.set_xlim(0, T - 1); ax.set_ylim(0, 1)
        ax.set_title(f"{p} (share={final_shares.get(p, 0):.0%})", fontsize=9)
        ax.set_xlabel("Round"); ax.set_ylabel("Allocation fraction")
        ax.grid(True, alpha=0.3, linewidth=0.5)
    ax_list[1].legend(loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False, fontsize=7)


def mpl_uses_tex():
    return plt.rcParams.get("text.usetex", False)


def _ternary_to_xy(rd, sf, pd):
    x = sf + 0.5 * pd
    y = (np.sqrt(3) / 2) * pd
    return x, y


def plot_ternary(ax, providers, T, portfolios, final_shares, p_colors):
    h = np.sqrt(3) / 2
    ax.plot([0, 1, 0.5, 0], [0, 0, h, 0], color="black", linewidth=1.0)
    for g in (0.25, 0.5, 0.75):
        xs_rd = [g, g / 2]; ys_rd = [0, g * h]
        xs_sf = [1 - g, 1 - g + g / 2]; ys_sf = [0, g * h]
        xs_pd = [(1 - g) / 2, 1 - (1 - g) / 2]; ys_pd = [(1 - g) * h, (1 - g) * h]
        for xs, ys in [(xs_rd, ys_rd), (xs_sf, ys_sf), (xs_pd, ys_pd)]:
            ax.plot(xs, ys, color="gray", alpha=0.2, linewidth=0.5)
    ax.text(-0.04, -0.04, r"R\&D" if mpl_uses_tex() else "R&D", ha="right", va="top", fontsize=9)
    ax.text(1.04, -0.04, "Safety", ha="left", va="top", fontsize=9)
    ax.text(0.5, h + 0.04, "Product", ha="center", va="bottom", fontsize=9)

    for p in providers:
        rd = portfolios[p]["rd"]; sf = portfolios[p]["safety"]; pd = portfolios[p]["product"]
        x, y = _ternary_to_xy(rd, sf, pd)
        color = p_colors[p]
        for i in range(T - 1):
            alpha = 0.15 + 0.75 * (i / max(T - 2, 1))
            ax.plot(x[i:i + 2], y[i:i + 2], color=color, alpha=alpha, linewidth=1.3)
        ax.plot(x[0], y[0], "o", color=color, markerfacecolor="white", markersize=4, markeredgewidth=1.0)
        share = final_shares.get(p, 0.0)
        ax.plot(x[-1], y[-1], "o", color=color, markersize=6)
        ax.annotate(f"{p.split()[0]} ({share:.0%})", xy=(x[-1], y[-1]),
                    xytext=(6, 4), textcoords="offset points", fontsize=7, color=color)
    ax.set_xlim(-0.15, 1.15); ax.set_ylim(-0.1, h + 0.12)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Portfolio trajectory (rounds 0 $\\rightarrow$ final)" if mpl_uses_tex()
                 else "Portfolio trajectory (rounds 0 -> final)", fontsize=9)


def _weighted_mean_alloc(rounds: list, providers: list, portfolios: dict, key: str) -> np.ndarray:
    """Per-round market-share-weighted mean of `portfolios[p][key]`.

    Uses `consumer_data.market_shares` from each round. Providers missing
    from market_shares at a given round get weight 0. If total weight is 0
    for a round (e.g. pre-consumer initialization), fall back to NaN so the
    line breaks rather than mis-reporting.
    """
    T = len(rounds)
    out = np.full(T, np.nan, dtype=float)
    for t, r in enumerate(rounds):
        shares = r.get("consumer_data", {}).get("market_shares", {}) or {}
        num = 0.0
        den = 0.0
        for p in providers:
            s = float(shares.get(p, 0.0) or 0.0)
            v = float(portfolios[p][key][t])
            num += s * v
            den += s
        if den > 0:
            out[t] = num / den
    return out


def plot_allocations_mean(ax, rounds, providers, T, portfolios, p_colors):
    """Per-provider rd (solid) + safety (dotted) over time; bold weighted-mean overlay.

    Returns nothing; mutates `ax`. Legend is placed outside to the right.
    """
    xs = np.arange(T)

    # Per-provider thin lines
    for p in providers:
        color = p_colors[p]
        ax.plot(xs, portfolios[p]["rd"], color=color, linestyle="-", linewidth=1.0,
                alpha=0.85, label=p)
        ax.plot(xs, portfolios[p]["safety"], color=color, linestyle=":", linewidth=1.0,
                alpha=0.85)

    # Weighted-mean bold overlays
    wm_rd = _weighted_mean_alloc(rounds, providers, portfolios, "rd")
    wm_sf = _weighted_mean_alloc(rounds, providers, portfolios, "safety")
    ax.plot(xs, wm_rd, color="black", linestyle="-", linewidth=2.5,
            label="weighted mean (R\\&D)" if mpl_uses_tex() else "weighted mean (R&D)")
    ax.plot(xs, wm_sf, color="black", linestyle=":", linewidth=2.5,
            label="weighted mean (safety)")

    ax.set_xlim(0, T - 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Round")
    ax.set_ylabel("Allocation fraction")
    ax.grid(True, alpha=0.3, linewidth=0.5)
    ax.set_title("Investment allocations over time "
                 "(market-share-weighted mean in bold)", fontsize=10)
    ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5),
              frameon=False, fontsize=7)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("run_dir", type=Path)
    ap.add_argument("--output", type=Path, default=None,
                    help="Output dir (default: <run_dir>/plots/)")
    args = ap.parse_args()

    run_dir = args.run_dir.resolve()
    out_dir = args.output.resolve() if args.output else run_dir / "plots"
    out_dir.mkdir(parents=True, exist_ok=True)

    rounds, providers, T, portfolios, final_shares = _load(run_dir)
    p_colors = get_provider_colors(providers)
    inv_colors = get_investment_colors()

    fig1, axes1 = plt.subplots(1, 2, figsize=(6.5, 2.3), sharey=True)
    plot_top2_stacked(axes1, providers, T, portfolios, final_shares, inv_colors)
    fig1.suptitle("Option 1: Top-2 providers — portfolio over time (stacked area)", fontsize=10)
    fig1.tight_layout(rect=[0, 0, 0.88, 0.95])
    out1_png = out_dir / "portfolio_option1_top2_stacked.png"
    out1_pdf = out_dir / "portfolio_option1_top2_stacked.pdf"
    fig1.savefig(out1_png, dpi=200, bbox_inches="tight")
    fig1.savefig(out1_pdf, bbox_inches="tight")
    plt.close(fig1)

    fig3, ax3 = plt.subplots(1, 1, figsize=(4.0, 3.6))
    plot_ternary(ax3, providers, T, portfolios, final_shares, p_colors)
    fig3.suptitle("Option 3: Portfolio trajectories on rd / safety / product simplex", fontsize=10)
    fig3.tight_layout()
    out3_png = out_dir / "portfolio_option3_ternary.png"
    out3_pdf = out_dir / "portfolio_option3_ternary.pdf"
    fig3.savefig(out3_png, dpi=200, bbox_inches="tight")
    fig3.savefig(out3_pdf, bbox_inches="tight")
    plt.close(fig3)

    fig4, ax4 = plt.subplots(1, 1, figsize=(6.5, 3.4))
    plot_allocations_mean(ax4, rounds, providers, T, portfolios, p_colors)
    fig4.tight_layout(rect=[0, 0, 0.82, 1.0])
    out4_png = out_dir / "allocations_over_time.png"
    out4_pdf = out_dir / "allocations_over_time.pdf"
    fig4.savefig(out4_png, dpi=200, bbox_inches="tight")
    fig4.savefig(out4_pdf, bbox_inches="tight")
    plt.close(fig4)

    print(f"Wrote:\n  {out1_png}\n  {out1_pdf}\n  {out3_png}\n  {out3_pdf}\n  {out4_png}\n  {out4_pdf}")


if __name__ == "__main__":
    main()
