"""
plot_validation.py — 4-panel comparison plots: real vs sim benchmark and market data.

Panels per benchmark (or benchmark group):
  A — Real benchmark scores over time (by provider)
  B — Real market share over time (by provider)
  C — Sim benchmark scores over time
  D — Sim market share over time

Additional plots:
  - Score-share rank correlation (real vs sim, with lag sweep)
  - Saturation detection: rolling improvement rate per benchmark

Usage:
    python validation/scripts/plot_validation.py [--benchmarks coding_advanced math_advanced ...]
                                                  [--exp-id exp_001]
                                                  [--out-dir validation/plots]
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
VAL_DIR = Path(__file__).resolve().parents[1]
PROC_DIR = VAL_DIR / "data" / "processed"
DEFAULT_OUT = VAL_DIR / "plots"

PROVIDER_COLORS = {
    "Orion Labs":      "#1f77b4",
    "Apex AI":         "#ff7f0e",
    "Genesis Systems": "#2ca02c",
    "Mirage AI":       "#d62728",
    "OpenCore":        "#9467bd",
    "Spark AI":        "#8c564b",
    "Other":           "#7f7f7f",
}

# Map sim benchmark name → readable label
BENCH_LABELS = {
    "coding_advanced":   "Coding (HumanEval analog)",
    "math_advanced":     "Math (MATH analog)",
    "reasoning_advanced":"Reasoning (GPQA analog)",
    "writing":           "Writing / General (MMLU / HellaSwag analog)",
    "_composite":        "Composite Score",
}


# ---------------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------------
def load_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def group_by(rows: list[dict], *keys: str) -> dict:
    result = defaultdict(list)
    for r in rows:
        k = tuple(r[key] for key in keys)
        result[k].append(r)
    return dict(result)


def safe_float(v) -> float | None:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Plotting helpers
# ---------------------------------------------------------------------------
def _provider_color(provider: str) -> str:
    return PROVIDER_COLORS.get(provider, "#333333")


def plot_benchmark_panel(ax: plt.Axes, rows: list[dict], x_col: str, title: str,
                         benchmark: str, xlabel: str = "Round") -> None:
    """Plot benchmark score trajectories grouped by provider."""
    by_provider = defaultdict(list)
    for r in rows:
        if r.get("benchmark") != benchmark:
            continue
        x = safe_float(r.get(x_col))
        y = safe_float(r.get("score_norm") or r.get("score"))
        if x is not None and y is not None:
            by_provider[r["provider"]].append((x, y))

    for provider, pts in sorted(by_provider.items()):
        pts.sort()
        xs, ys = zip(*pts)
        ax.plot(xs, ys, marker="o", markersize=3, label=provider,
                color=_provider_color(provider))

    ax.set_title(title, fontsize=9)
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_ylabel("Score (norm)", fontsize=8)
    ax.set_ylim(0, 1.05)
    ax.tick_params(labelsize=7)
    ax.legend(fontsize=6, loc="lower right")


def plot_market_panel(ax: plt.Axes, rows: list[dict], x_col: str, title: str,
                      xlabel: str = "Round") -> None:
    """Plot market share trajectories grouped by provider."""
    by_provider = defaultdict(list)
    for r in rows:
        x = safe_float(r.get(x_col))
        y = safe_float(r.get("share_estimate") or r.get("market_share"))
        if x is not None and y is not None:
            by_provider[r["provider"]].append((x, y))

    for provider, pts in sorted(by_provider.items()):
        pts.sort()
        xs, ys = zip(*pts)
        ax.plot(xs, ys, marker="s", markersize=3, label=provider,
                color=_provider_color(provider))

    ax.set_title(title, fontsize=9)
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_ylabel("Market share", fontsize=8)
    ax.set_ylim(0, 1.05)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0))
    ax.tick_params(labelsize=7)
    ax.legend(fontsize=6, loc="upper right")


def add_event_vlines(ax: plt.Axes, events: list[dict], x_col: str,
                     event_types: list[str]) -> None:
    """Draw vertical dashed lines for sim or real events."""
    for ev in events:
        if ev.get("event_type") in event_types:
            x = safe_float(ev.get(x_col))
            if x is not None:
                ax.axvline(x, color="gray", linestyle="--", linewidth=0.6, alpha=0.7)


# ---------------------------------------------------------------------------
# 4-panel plot per benchmark
# ---------------------------------------------------------------------------
def make_4panel(
    benchmark: str,
    real_bench: list[dict],
    real_market: list[dict],
    sim_bench: list[dict],
    sim_market: list[dict],
    sim_events: list[dict],
    out_dir: Path,
) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(
        f"Real vs Sim — {BENCH_LABELS.get(benchmark, benchmark)}",
        fontsize=11, fontweight="bold"
    )

    # Panel A — Real benchmark scores
    ax = axes[0, 0]
    plot_benchmark_panel(ax, real_bench, x_col="sim_round",
                         title="A — Real Benchmark Scores (by quarter from GPT-4 launch)",
                         benchmark=benchmark, xlabel="Sim-equivalent round")

    # Panel B — Real market share
    ax = axes[0, 1]
    plot_market_panel(ax, real_market, x_col="sim_round",
                      title="B — Real Market Share (web traffic / survey)",
                      xlabel="Sim-equivalent round")

    # Panel C — Sim benchmark scores
    ax = axes[1, 0]
    plot_benchmark_panel(ax, sim_bench, x_col="round",
                         title="C — Sim Benchmark Scores",
                         benchmark=benchmark, xlabel="Sim round")
    add_event_vlines(ax, sim_events, "round",
                     ["benchmark_introduced", "benchmark_leader_change"])

    # Panel D — Sim market share
    ax = axes[1, 1]
    plot_market_panel(ax, sim_market, x_col="round",
                      title="D — Sim Market Share",
                      xlabel="Sim round")
    add_event_vlines(ax, sim_events, "round", ["market_leader_change"])

    plt.tight_layout()
    out_path = out_dir / f"4panel_{benchmark}.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"  Saved: {out_path}")


# ---------------------------------------------------------------------------
# Score-share rank correlation
# ---------------------------------------------------------------------------
def plot_rank_correlation(
    real_bench: list[dict],
    real_market: list[dict],
    sim_bench: list[dict],
    sim_market: list[dict],
    out_dir: Path,
    max_lag: int = 4,
) -> None:
    """
    For each lag (0..max_lag rounds), compute Spearman rank correlation between
    benchmark rank and market share rank.  Plot real vs sim correlation curves.
    """
    def spearman_corr(x: list[float], y: list[float]) -> float:
        n = len(x)
        if n < 2:
            return float("nan")
        rx = np.argsort(np.argsort(x)).astype(float)
        ry = np.argsort(np.argsort(y)).astype(float)
        d2 = np.sum((rx - ry) ** 2)
        return 1 - 6 * d2 / (n * (n ** 2 - 1))

    def compute_lag_corrs(
        bench_rows: list[dict], market_rows: list[dict],
        bench_x: str, market_x: str, score_col: str, share_col: str
    ) -> list[float]:
        # Build: round → {provider: score}
        bench_by_round: dict[int, dict[str, float]] = defaultdict(dict)
        for r in bench_rows:
            x = safe_float(r.get(bench_x))
            s = safe_float(r.get(score_col))
            if x is not None and s is not None and r.get("benchmark") == "_composite":
                bench_by_round[int(x)][r["provider"]] = s

        market_by_round: dict[int, dict[str, float]] = defaultdict(dict)
        for r in market_rows:
            x = safe_float(r.get(market_x))
            sh = safe_float(r.get(share_col))
            if x is not None and sh is not None:
                market_by_round[int(x)][r["provider"]] = sh

        corrs = []
        for lag in range(max_lag + 1):
            all_bench, all_market = [], []
            for rnd, bench_scores in bench_by_round.items():
                mkt = market_by_round.get(rnd + lag, {})
                common = set(bench_scores) & set(mkt)
                if len(common) < 3:
                    continue
                all_bench.extend(bench_scores[p] for p in sorted(common))
                all_market.extend(mkt[p] for p in sorted(common))
            corrs.append(spearman_corr(all_bench, all_market) if all_bench else float("nan"))
        return corrs

    real_corrs = compute_lag_corrs(
        real_bench, real_market, "sim_round", "sim_round", "score_norm", "share_estimate"
    )
    sim_corrs = compute_lag_corrs(
        sim_bench, sim_market, "round", "round", "score", "market_share"
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    lags = list(range(max_lag + 1))
    ax.plot(lags, real_corrs, marker="o", label="Real data")
    ax.plot(lags, sim_corrs, marker="s", label="Sim data")
    ax.axhline(0, color="gray", linewidth=0.5)
    ax.set_xlabel("Lag (rounds)", fontsize=9)
    ax.set_ylabel("Spearman rank correlation\n(benchmark rank → market share rank)", fontsize=8)
    ax.set_title("Score-Share Rank Correlation vs Lag", fontsize=10)
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
    window: int = 3,
    threshold: float = 0.02,
) -> None:
    """
    Rolling improvement rate per benchmark.  Mark when rate drops below threshold.
    """
    def compute_improvement_rate(rows: list[dict], x_col: str, score_col: str,
                                 bench: str) -> tuple[list[float], list[float]]:
        """Return (rounds, rolling_improvement_rate) averaged across all providers."""
        by_round: dict[int, list[float]] = defaultdict(list)
        for r in rows:
            if r.get("benchmark") != bench:
                continue
            x = safe_float(r.get(x_col))
            s = safe_float(r.get(score_col))
            if x is not None and s is not None:
                by_round[int(x)].append(s)

        rounds = sorted(by_round)
        avg_scores = [np.mean(by_round[rnd]) for rnd in rounds]

        if len(avg_scores) < window + 1:
            return [], []

        improvement = []
        imp_rounds = []
        for i in range(window, len(rounds)):
            delta = avg_scores[i] - avg_scores[i - window]
            improvement.append(delta / window)
            imp_rounds.append(rounds[i])

        return imp_rounds, improvement

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    fig.suptitle(
        f"Saturation Detection — {BENCH_LABELS.get(benchmark, benchmark)}",
        fontsize=10
    )

    for ax, rows, x_col, score_col, label in [
        (axes[0], real_bench, "sim_round", "score_norm", "Real"),
        (axes[1], sim_bench,  "round",     "score",      "Sim"),
    ]:
        rnd_list, imp = compute_improvement_rate(rows, x_col, score_col, benchmark)
        if rnd_list:
            ax.plot(rnd_list, imp, label="Avg improvement/round")
            ax.axhline(threshold, color="red", linestyle="--", linewidth=0.8,
                       label=f"Saturation threshold ({threshold})")
            # Mark saturation point
            sat_rounds = [r for r, v in zip(rnd_list, imp) if v < threshold]
            if sat_rounds:
                ax.axvline(sat_rounds[0], color="orange", linestyle=":", linewidth=1,
                           label=f"Saturation round ~{sat_rounds[0]}")
        ax.set_title(f"{label} Data", fontsize=9)
        ax.set_xlabel("Round" if label == "Sim" else "Sim-equivalent round", fontsize=8)
        ax.set_ylabel("Rolling avg score improvement", fontsize=8)
        ax.legend(fontsize=7)
        ax.axhline(0, color="gray", linewidth=0.4)

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

    # Filter sim data by exp_id if provided
    if exp_id:
        sim_bench  = [r for r in sim_bench  if r.get("exp_id", "").startswith(exp_id)]
        sim_market = [r for r in sim_market if r.get("exp_id", "").startswith(exp_id)]
        sim_events = [r for r in sim_events if r.get("exp_id", "").startswith(exp_id)]

    if not benchmarks:
        # Derive from sim data
        benchmarks = sorted({r["benchmark"] for r in sim_bench if r.get("benchmark")})

    print(f"Plotting benchmarks: {benchmarks}")

    for bench in benchmarks:
        print(f"\n  4-panel: {bench}")
        make_4panel(bench, real_bench, real_market, sim_bench, sim_market, sim_events, out_dir)
        plot_saturation(real_bench, sim_bench, bench, out_dir)

    print("\n  Rank correlation plot ...")
    plot_rank_correlation(real_bench, real_market, sim_bench, sim_market, out_dir)

    print(f"\nAll plots saved to {out_dir}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmarks", nargs="*", default=[], help="Sim benchmark names")
    parser.add_argument("--exp-id", default=None, help="Filter sim data to this experiment prefix")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    main(args.benchmarks, args.exp_id, args.out_dir)
