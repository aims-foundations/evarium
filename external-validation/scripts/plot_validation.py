"""
plot_validation.py — 4-panel comparison plots: real vs sim benchmark and market data.

Panels per benchmark:
  A — Real benchmark scores over time (named providers only, cumulative-best per round)
  B — Real market share over time
  C — Sim benchmark scores over time
  D — Sim market share over time

Additional plots:
  - Score-share rank correlation (real vs sim, lag sweep)
  - Saturation detection: rolling improvement of frontier (best provider) per benchmark

Usage:
    python external-validation/scripts/plot_validation.py [--benchmarks math reasoning ...]
                                                           [--exp-id exp_001]
                                                           [--out-dir external-validation/plots]
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
import json

VAL_DIR = Path(__file__).resolve().parents[1]
PROC_DIR = VAL_DIR / "data" / "processed"
DEFAULT_OUT = VAL_DIR / "plots"

NAMED_PROVIDERS = {
    "Orion Labs", "Apex AI", "Genesis Systems", "Mirage AI", "OpenCore", "Spark AI"
}

PROVIDER_COLORS = {
    "Orion Labs":      "#1f77b4",
    "Apex AI":         "#ff7f0e",
    "Genesis Systems": "#2ca02c",
    "Mirage AI":       "#d62728",
    "OpenCore":        "#9467bd",
    "Spark AI":        "#8c564b",
}

BENCH_LABELS = {
    "coding":    "Coding  (HumanEval)",
    "math":      "Math  (MATH / GSM8K)",
    "reasoning": "Reasoning  (GPQA / HELM)",
    "writing":   "Writing / General  (MMLU / HellaSwag)",
    "_composite":"Composite Score",
}

# Real x-axis: round 0 = Q1 2023, each round = 1 quarter
ROUND_YEAR_LABELS = {-4: "Q1'22", -2: "Q3'22", 0: "Q1'23",
                      2: "Q3'23",  4: "Q1'24",  6: "Q3'24",  8: "Q1'25"}


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
def load_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def safe_float(v) -> float | None:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Aggregation helpers
# ---------------------------------------------------------------------------
def best_score_by_provider_round(
    rows: list[dict], benchmark: str, x_col: str, score_col: str,
    named_only: bool = True
) -> dict[str, list[tuple[int, float]]]:
    """
    For each named provider, compute the cumulative-best score up to each round.
    Returns {provider: [(round, cummax_score), ...]} sorted by round.
    """
    # Collect raw: provider → round → best score seen at that exact round
    raw: dict[str, dict[int, float]] = defaultdict(dict)
    for r in rows:
        if r.get("benchmark") != benchmark:
            continue
        provider = r.get("provider", "")
        if named_only and provider not in NAMED_PROVIDERS:
            continue
        x = safe_float(r.get(x_col))
        s = safe_float(r.get(score_col))
        if x is None or s is None:
            continue
        rnd = int(x)
        if rnd not in raw[provider] or s > raw[provider][rnd]:
            raw[provider][rnd] = s

    # Convert to cumulative max trajectory
    result: dict[str, list[tuple[int, float]]] = {}
    for provider, round_scores in raw.items():
        rounds = sorted(round_scores)
        cum_max = float("-inf")
        pts = []
        for rnd in rounds:
            cum_max = max(cum_max, round_scores[rnd])
            pts.append((rnd, cum_max))
        result[provider] = pts
    return result


def best_score_by_round_frontier(
    rows: list[dict], benchmark: str, x_col: str, score_col: str,
    named_only: bool = True
) -> tuple[list[int], list[float]]:
    """
    Frontier = best score across ALL named providers at each round (cumulative).
    Returns (rounds, frontier_scores).
    """
    trajectories = best_score_by_provider_round(rows, benchmark, x_col, score_col, named_only)
    if not trajectories:
        return [], []

    # Merge all (round, score) points
    all_rounds = sorted({rnd for pts in trajectories.values() for rnd, _ in pts})
    # At each round, frontier = max cummax across all providers up to that round
    frontier: dict[int, float] = {}
    for rnd in all_rounds:
        val = max(
            (score for pts in trajectories.values() for r, score in pts if r <= rnd),
            default=float("nan")
        )
        frontier[rnd] = val

    rounds = sorted(frontier)
    return rounds, [frontier[r] for r in rounds]


# ---------------------------------------------------------------------------
# Panel helpers
# ---------------------------------------------------------------------------
def _provider_color(provider: str) -> str:
    return PROVIDER_COLORS.get(provider, "#555555")


def apply_real_xticks(ax: plt.Axes) -> None:
    """Replace numeric round ticks with year labels on the real-data x-axis."""
    ticks = sorted(ROUND_YEAR_LABELS)
    labels = [ROUND_YEAR_LABELS[t] for t in ticks]
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels, fontsize=6, rotation=30, ha="right")


def plot_benchmark_panel(
    ax: plt.Axes, rows: list[dict], x_col: str, title: str,
    benchmark: str, xlabel: str = "Round", real_data: bool = False
) -> None:
    """Plot cumulative-best score trajectories per named provider."""
    trajectories = best_score_by_provider_round(
        rows, benchmark, x_col,
        score_col="score_norm" if real_data else "score",
        named_only=True,
    )

    if not trajectories:
        ax.text(0.5, 0.5, "No data", transform=ax.transAxes,
                ha="center", va="center", fontsize=9, color="gray")
    else:
        for provider, pts in sorted(trajectories.items()):
            xs, ys = zip(*pts)
            ax.plot(xs, ys, marker="o", markersize=4, linewidth=1.5,
                    label=provider, color=_provider_color(provider))

    ax.set_title(title, fontsize=9)
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_ylabel("Score (norm 0–1)", fontsize=8)
    ax.set_ylim(0, 1.05)
    ax.tick_params(labelsize=7)
    if trajectories:
        ax.legend(fontsize=6, loc="lower right")
    if real_data:
        apply_real_xticks(ax)


# Mindshare colors mirror sim provider colors via analog mapping:
#   OpenAI -> Orion Labs, Anthropic -> Apex AI, Google -> Genesis Systems,
#   Meta -> Mirage AI, Deepseek -> OpenCore
MINDSHARE_COLORS = {
    "OpenAI":    PROVIDER_COLORS["Orion Labs"],
    "Anthropic": PROVIDER_COLORS["Apex AI"],
    "Google":    PROVIDER_COLORS["Genesis Systems"],
    "Meta":      PROVIDER_COLORS["Mirage AI"],
    "Deepseek":  PROVIDER_COLORS["OpenCore"],
}


def _load_mindshare_json(path: Path):
    """Return (dates, series_dict) from a mindshare JSON file."""
    if not path.exists():
        return [], {}
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if "dates" in data and "series" in data:
        return data["dates"], data["series"]
    elif "dates" in data:
        dates = data["dates"]
        return dates, {k: v for k, v in data.items() if k != "dates" and k != "title"}
    first = next(iter(data.values()))
    return [str(i) for i in range(len(first))], data


def plot_mindshare_panel(
    ax: plt.Axes,
    dates: list,
    series: dict,
    title: str,
    xlabel: str = "Date",
) -> None:
    """Line plot of normalised mind share (%) per company."""
    import numpy as np
    companies = [c for c in series if c in MINDSHARE_COLORS]
    n = len(dates)
    # Normalise to percent
    totals = np.zeros(n)
    for c in companies:
        totals += np.array(series[c], dtype=float)
    totals = np.where(totals == 0, 1, totals)

    x = np.arange(n)
    for c in companies:
        vals = np.array(series[c], dtype=float) / totals * 100.0
        ax.plot(x, vals, linewidth=1.5, label=c, color=MINDSHARE_COLORS[c])

    # x-ticks: every 6th label
    tick_idx = [i for i in range(n) if i % 6 == 0]
    ax.set_xticks(tick_idx)
    ax.set_xticklabels([dates[i] for i in tick_idx], rotation=30, ha="right", fontsize=6)

    ax.set_title(title, fontsize=9)
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_ylabel("Mind share (%)", fontsize=8)
    ax.set_ylim(0, 100)
    ax.tick_params(labelsize=7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle="--", linewidth=0.4, alpha=0.6)
    ax.legend(fontsize=6, loc="upper left")


def plot_market_panel(
    ax: plt.Axes, rows: list[dict], x_col: str, title: str,
    xlabel: str = "Round", real_data: bool = False
) -> None:
    """Plot market share trajectories per named provider."""
    by_provider: dict[str, list[tuple[float, float]]] = defaultdict(list)
    for r in rows:
        provider = r.get("provider", "")
        if provider not in NAMED_PROVIDERS:
            continue
        x = safe_float(r.get(x_col))
        y = safe_float(r.get("share_estimate") or r.get("market_share"))
        if x is not None and y is not None:
            by_provider[provider].append((x, y))

    if not by_provider:
        ax.text(0.5, 0.5, "No data", transform=ax.transAxes,
                ha="center", va="center", fontsize=9, color="gray")
    else:
        for provider, pts in sorted(by_provider.items()):
            pts.sort()
            xs, ys = zip(*pts)
            ax.plot(xs, ys, marker="s", markersize=4, linewidth=1.5,
                    label=provider, color=_provider_color(provider))

    ax.set_title(title, fontsize=9)
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_ylabel("Market share", fontsize=8)
    ax.set_ylim(0, 1.05)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0))
    ax.tick_params(labelsize=7)
    if by_provider:
        ax.legend(fontsize=6, loc="upper right")
    if real_data:
        apply_real_xticks(ax)


def add_event_vlines(
    ax: plt.Axes, events: list[dict], x_col: str, event_types: list[str]
) -> None:
    seen: set = set()
    for ev in events:
        if ev.get("event_type") in event_types:
            x = safe_float(ev.get(x_col))
            if x is not None and x not in seen:
                ax.axvline(x, color="gray", linestyle="--", linewidth=0.6, alpha=0.5)
                seen.add(x)


# ---------------------------------------------------------------------------
# 4-panel plot
# ---------------------------------------------------------------------------
def make_4panel(
    benchmark: str,
    real_bench: list[dict],
    real_market: list[dict],
    sim_bench: list[dict],
    sim_market: list[dict],
    sim_events: list[dict],
    out_dir: Path,
    mindshare_dates: list | None = None,
    mindshare_series: dict | None = None,
) -> None:
    label = BENCH_LABELS.get(benchmark, benchmark)
    fig, axes = plt.subplots(2, 2, figsize=(13, 8))
    fig.suptitle(f"Real vs Sim — {label}", fontsize=11, fontweight="bold")

    # Panel A — Real benchmark scores (named providers, cumulative-best)
    plot_benchmark_panel(
        axes[0, 0], real_bench, x_col="sim_round",
        title="A — Real Benchmark Scores  (flagship models, cumulative best)",
        benchmark=benchmark, xlabel="Quarter", real_data=True,
    )

    # Panel B — Real mind share (document mentions, line plot)
    if mindshare_dates and mindshare_series:
        plot_mindshare_panel(
            axes[0, 1], mindshare_dates, mindshare_series,
            title="B — Real Provider Mind Share  (document mentions)",
            xlabel="Date",
        )
    else:
        axes[0, 1].text(0.5, 0.5, "No mindshare data", transform=axes[0, 1].transAxes,
                        ha="center", va="center", fontsize=9, color="gray")
        axes[0, 1].set_title("B — Real Provider Mind Share", fontsize=9)

    # Panel C — Sim benchmark scores
    plot_benchmark_panel(
        axes[1, 0], sim_bench, x_col="round",
        title="C — Sim Benchmark Scores",
        benchmark=benchmark, xlabel="Sim round",
    )
    add_event_vlines(axes[1, 0], sim_events, "round",
                     ["benchmark_introduced", "benchmark_leader_change"])

    # Panel D — Sim market share
    plot_market_panel(
        axes[1, 1], sim_market, x_col="round",
        title="D — Sim Market Share",
        xlabel="Sim round",
    )
    add_event_vlines(axes[1, 1], sim_events, "round", ["market_leader_change"])

    plt.tight_layout()
    out_path = out_dir / f"4panel_{benchmark}.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"  Saved: {out_path}")


# ---------------------------------------------------------------------------
# Rank correlation
# ---------------------------------------------------------------------------
def plot_rank_correlation(
    real_bench: list[dict],
    real_market: list[dict],
    sim_bench: list[dict],
    sim_market: list[dict],
    out_dir: Path,
    max_lag: int = 4,
) -> None:
    def spearman(x: list[float], y: list[float]) -> float:
        n = len(x)
        if n < 2:
            return float("nan")
        rx = np.argsort(np.argsort(x)).astype(float)
        ry = np.argsort(np.argsort(y)).astype(float)
        d2 = np.sum((rx - ry) ** 2)
        return float(1 - 6 * d2 / (n * (n ** 2 - 1)))

    def lag_corrs(
        bench_rows: list[dict], market_rows: list[dict],
        bench_x: str, market_x: str, score_col: str, share_col: str,
        bench_name: str = "_composite",
    ) -> list[float]:
        # Use cumulative-best score per provider per round
        bench_by_round: dict[int, dict[str, float]] = defaultdict(dict)
        for r in bench_rows:
            if r.get("benchmark") != bench_name:
                continue
            provider = r.get("provider", "")
            if provider not in NAMED_PROVIDERS:
                continue
            x = safe_float(r.get(bench_x))
            s = safe_float(r.get(score_col))
            if x is None or s is None:
                continue
            rnd = int(x)
            existing = bench_by_round[rnd].get(provider, float("-inf"))
            bench_by_round[rnd][provider] = max(existing, s)

        market_by_round: dict[int, dict[str, float]] = defaultdict(dict)
        for r in market_rows:
            provider = r.get("provider", "")
            if provider not in NAMED_PROVIDERS:
                continue
            x = safe_float(r.get(market_x))
            sh = safe_float(r.get(share_col))
            if x is not None and sh is not None:
                market_by_round[int(x)][provider] = sh

        corrs = []
        for lag in range(max_lag + 1):
            all_b, all_m = [], []
            for rnd, bscores in bench_by_round.items():
                mkt = market_by_round.get(rnd + lag, {})
                common = set(bscores) & set(mkt)
                if len(common) < 3:
                    continue
                all_b.extend(bscores[p] for p in sorted(common))
                all_m.extend(mkt[p] for p in sorted(common))
            corrs.append(spearman(all_b, all_m) if all_b else float("nan"))
        return corrs

    real_corrs = lag_corrs(real_bench, real_market, "sim_round", "sim_round",
                           "score_norm", "share_estimate", bench_name="writing")
    sim_corrs  = lag_corrs(sim_bench,  sim_market,  "round",     "round",
                           "score",     "market_share", bench_name="_composite")

    fig, ax = plt.subplots(figsize=(7, 4))
    lags = list(range(max_lag + 1))

    real_valid = [c for c in real_corrs if not np.isnan(c)]
    if real_valid:
        ax.plot(lags, real_corrs, marker="o", label="Real data")
    else:
        ax.text(0.3, 0.6, "Real market data insufficient\nfor correlation (need time series)",
                transform=ax.transAxes, fontsize=8, color="gray", style="italic")

    ax.plot(lags, sim_corrs, marker="s", label="Sim data")
    ax.axhline(0, color="gray", linewidth=0.5)
    ax.set_xlabel("Lag (rounds)", fontsize=9)
    ax.set_ylabel("Spearman correlation\n(benchmark rank → market share rank)", fontsize=8)
    ax.set_title("Score–Share Rank Correlation vs Lag", fontsize=10)
    ax.legend(fontsize=8)
    ax.set_ylim(-1, 1)
    plt.tight_layout()
    out_path = out_dir / "rank_correlation.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"  Saved: {out_path}")


# ---------------------------------------------------------------------------
# Saturation detection
# ---------------------------------------------------------------------------
def plot_saturation(
    real_bench: list[dict],
    sim_bench: list[dict],
    benchmark: str,
    out_dir: Path,
    window: int = 2,
    threshold: float = 0.02,
) -> None:
    """
    Plot rolling improvement of the frontier (best score across named providers)
    per round.  Uses cumulative-best so the curve is non-decreasing; improvement
    rate drops toward zero as the benchmark saturates.
    """
    def frontier_improvement(
        rows: list[dict], x_col: str, score_col: str, bench: str, named_only: bool
    ) -> tuple[list, list]:
        rnds, scores = best_score_by_round_frontier(rows, bench, x_col, score_col, named_only)
        if len(scores) < window + 1:
            return [], []
        imp_rounds = rnds[window:]
        imp = [(scores[i] - scores[i - window]) / window
               for i in range(window, len(scores))]
        return imp_rounds, imp

    label = BENCH_LABELS.get(benchmark, benchmark)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    fig.suptitle(f"Saturation Detection — {label}", fontsize=10)

    configs = [
        (axes[0], real_bench, "sim_round", "score_norm", "Real  (frontier = best flagship model)", True),
        (axes[1], sim_bench,  "round",     "score",      "Sim  (frontier = best provider)",        True),
    ]

    for ax, rows, x_col, score_col, panel_label, named_only in configs:
        rnd_list, imp = frontier_improvement(rows, x_col, score_col, benchmark, named_only)
        if rnd_list:
            ax.plot(rnd_list, imp, color="#1f77b4", linewidth=1.8,
                    label="Frontier improvement / round")
            ax.axhline(threshold, color="red", linestyle="--", linewidth=0.9,
                       label=f"Saturation threshold ({threshold})")
            sat = [r for r, v in zip(rnd_list, imp) if v < threshold]
            if sat:
                ax.axvline(sat[0], color="orange", linestyle=":", linewidth=1.2,
                           label=f"Saturation ≈ round {sat[0]}")
        else:
            ax.text(0.5, 0.5, "Insufficient data", transform=ax.transAxes,
                    ha="center", va="center", fontsize=9, color="gray")

        ax.set_title(panel_label, fontsize=9)
        ax.set_ylabel("Frontier score improvement / round", fontsize=8)
        ax.axhline(0, color="gray", linewidth=0.4)
        ax.legend(fontsize=7)
        ax.tick_params(labelsize=7)

        if "Real" in panel_label:
            ax.set_xlabel("Quarter", fontsize=8)
            apply_real_xticks(ax)
        else:
            ax.set_xlabel("Sim round", fontsize=8)

    plt.tight_layout()
    out_path = out_dir / f"saturation_{benchmark}.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"  Saved: {out_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main(benchmarks: list[str], exp_id: str | None, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Loading processed data ...")
    real_bench  = load_csv(PROC_DIR / "benchmarks.csv")
    real_market = load_csv(PROC_DIR / "market_share.csv")
    sim_bench   = load_csv(PROC_DIR / "sim_benchmarks.csv")
    sim_market  = load_csv(PROC_DIR / "sim_market.csv")
    sim_events  = load_csv(PROC_DIR / "sim_events.csv")

    # Load mindshare (document mentions) for Panel B
    ms_dates, ms_series = _load_mindshare_json(PROC_DIR / "documents_mentions.json")

    if exp_id:
        sim_bench  = [r for r in sim_bench  if r.get("exp_id", "").startswith(exp_id)]
        sim_market = [r for r in sim_market if r.get("exp_id", "").startswith(exp_id)]
        sim_events = [r for r in sim_events if r.get("exp_id", "").startswith(exp_id)]

    if not benchmarks:
        benchmarks = sorted({r["benchmark"] for r in sim_bench if r.get("benchmark")})

    print(f"Benchmarks: {benchmarks}")

    for bench in benchmarks:
        print(f"\n  4-panel: {bench}")
        make_4panel(bench, real_bench, real_market, sim_bench, sim_market, sim_events, out_dir,
                    mindshare_dates=ms_dates, mindshare_series=ms_series)
        plot_saturation(real_bench, sim_bench, bench, out_dir)

    print("\n  Rank correlation ...")
    plot_rank_correlation(real_bench, real_market, sim_bench, sim_market, out_dir)

    print(f"\nDone. Plots saved to {out_dir}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmarks", nargs="*", default=[])
    parser.add_argument("--exp-id", default=None)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    main(args.benchmarks, args.exp_id, args.out_dir)
