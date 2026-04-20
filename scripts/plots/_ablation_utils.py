"""
Shared utilities for ablation plot scripts.

Used by:
  - scripts/plot_ablation_main.py
  - scripts/plot_ablation_ecosystem.py

Supports both multi-seed paths (heuristic, N>=2, renders mean+p10-p90 band) and
single-seed paths (LLM case studies, N=1, renders single trajectory only).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def _last_run(all_rounds: list) -> list:
    """Extract the last complete run from a possibly-concatenated rounds list."""
    last_zero = 0
    for i, r in enumerate(all_rounds):
        if r.get("round", -1) == 0:
            last_zero = i
    return all_rounds[last_zero:]


def load_runs(base_path: Path, condition: str) -> list[list]:
    """Load rounds.jsonl for every seed under `base_path/{condition}/seeds/`.

    Works for both `sandbox/experiments/heuristic/` (N~30 seeds per condition)
    and `sandbox/experiments/llm_evaluator/llm/` (N=1 case studies).
    """
    cdir = Path(base_path) / condition / "seeds"
    if not cdir.exists():
        print(f"  [missing] {condition} ({cdir})")
        return []
    runs = []
    for seed_dir in sorted(cdir.iterdir()):
        jsonl = seed_dir / "rounds.jsonl"
        if not jsonl.exists():
            continue
        all_rounds = []
        with open(jsonl) as f:
            for line in f:
                line = line.strip()
                if line:
                    all_rounds.append(json.loads(line))
        if all_rounds:
            runs.append(_last_run(all_rounds))
    return runs


def _rolling_mean(vals: list, window: int) -> list:
    out = []
    for i in range(len(vals)):
        w = vals[max(0, i - window + 1): i + 1]
        w = [v for v in w if not np.isnan(v)]
        out.append(float(np.mean(w)) if w else float("nan"))
    return out


def compute_series(runs: list, metric_fn, rolling: int = 0) -> dict:
    """Per-round statistics across seeds.

    Returns {round_idx: {mean, p10, p90, n}}.
    For N=1 (single seed), mean==p10==p90 and plotting helpers suppress the band.
    """
    if not runs:
        return {}
    max_rounds = max(len(run) for run in runs)
    by_round: dict[int, list] = {i: [] for i in range(max_rounds)}
    for run in runs:
        raw = [metric_fn(r) for r in run]
        if rolling > 1:
            raw = _rolling_mean(raw, rolling)
        for i, v in enumerate(raw):
            if not np.isnan(v):
                by_round[i].append(v)
    result = {}
    for i, vals in by_round.items():
        if vals:
            result[i] = {
                "mean": float(np.mean(vals)),
                "p10":  float(np.percentile(vals, 10)),
                "p90":  float(np.percentile(vals, 90)),
                "n":    len(vals),
            }
    return result


def plot_trajectory_panel(
    ax,
    series_dict: dict,
    colors: dict,
    labels: dict,
    linestyles: dict | None = None,
    ylabel: str = "",
    title: str = "",
    show_legend: bool = False,
    lw: float = 1.3,
    band_alpha: float = 0.12,
) -> list:
    """Plot one panel. Suppresses the p10-p90 band when N==1 per round.

    Returns line handles (for custom legend composition upstream).
    """
    handles = []
    for cond, series in series_dict.items():
        if not series:
            continue
        xs = sorted(series.keys())
        means = [series[x]["mean"] for x in xs]
        p10   = [series[x]["p10"]  for x in xs]
        p90   = [series[x]["p90"]  for x in xs]
        ns    = [series[x]["n"]    for x in xs]
        color = colors.get(cond, "#888888")
        ls    = (linestyles or {}).get(cond, "-")
        label = labels.get(cond, cond)
        line, = ax.plot(xs, means, color=color, lw=lw, ls=ls, label=label, zorder=4)
        if any(n >= 2 for n in ns):
            ax.fill_between(xs, p10, p90, color=color, alpha=band_alpha, zorder=2)
        handles.append(line)
    ax.axhline(0, color="#888888", lw=0.5, ls="--", zorder=1)
    ax.set_xlabel("Round", fontsize=7)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=7)
    if title:
        ax.set_title(title, fontsize=8, fontweight="bold")
    ax.tick_params(labelsize=6.5)
    ax.grid(axis="y", lw=0.4, alpha=0.35, ls="--")
    if show_legend:
        ax.legend(fontsize=6, frameon=False, handlelength=1.2)
    return handles
