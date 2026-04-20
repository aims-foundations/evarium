"""
plot_inflation_trajectories.py

Loads rounds.jsonl for each run in the registry and plots per-round
gaming gap (mean published score - true capability) with 95% CI bands
across seeds.

Produces two figures saved to overleaf/figures/validation/:
  - inflation_traj_presets.pdf   : full_ecosystem x 3 presets, llama + qwen
  - inflation_traj_ablations.pdf : all 9 ablations, balanced preset, llama + qwen

Usage:
    python scripts/plot_inflation_trajectories.py
"""

import json
import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from .. import paths as _paths

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT    = Path(_paths.PROJECT_ROOT)
HF_DATA = ROOT / "hf_data"
RUNS    = HF_DATA / "runs.jsonl"
FIG_DIR = ROOT.parent / "overleaf" / "figures" / "validation"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Style constants (consistent with plot_validation_figures.py)
# ---------------------------------------------------------------------------

MODEL_COLORS = {
    "llama-70b":  "#6ACC65",
    "qwen-235b":  "#D65F5F",
    "heuristic":  "#888888",
}
MODEL_LABELS = {
    "llama-70b": "Llama-70b",
    "qwen-235b": "Qwen-235b",
    "heuristic": "Heuristic",
}

PRESET_DASH = {
    "balanced": "-",
    "us":       "--",
    "eu":       ":",
}
PRESET_LABELS = {
    "balanced": "Balanced",
    "us":       "US Light-Touch",
    "eu":       "EU Precautionary",
}

CONDITION_LABELS = {
    "full_ecosystem":       "Full Ecosystem",
    "ablation_no_media":    "No Media",
    "ablation_no_incidents":"No Incidents",
    "ablation_no_startups": "No Startups",
    "ablation_no_opencore": "No OpenCore",
    "ablation_single_benchmark": "Single Benchmark",
    "ablation_no_funders":  "No Funders",
    "ablation_no_bench_evol": "No Bench. Evol.",
    "ablation_eval_as_company": "Eval As Company",
}

ABLATION_ORDER = [
    "full_ecosystem",
    "ablation_no_media",
    "ablation_no_incidents",
    "ablation_no_startups",
    "ablation_no_opencore",
    "ablation_single_benchmark",
    "ablation_no_funders",
    "ablation_no_bench_evol",
    "ablation_eval_as_company",
]

# Distinct colors for 9 conditions
CONDITION_COLORS = [
    "#4878CF", "#6ACC65", "#D65F5F", "#B47CC7",
    "#C4AD66", "#77BEDB", "#E87E4D", "#92C462", "#AB4E52",
]

# ---------------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------------

def load_registry():
    runs = []
    with open(RUNS, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                runs.append(json.loads(line))
    return runs


def load_rounds(path_rel):
    p = HF_DATA / path_rel / "rounds.jsonl"
    if not p.exists():
        return []
    rounds = []
    with open(p, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rounds.append(json.loads(line))
    return rounds


def gaming_gap_trajectory(rounds):
    """Return list of (round_num, mean_gap) across all providers."""
    result = []
    for r in rounds:
        scores   = r.get("scores", {})
        true_cap = r.get("true_capabilities", {})
        providers = [p for p in scores if p in true_cap]
        if providers:
            gap = sum(scores[p] - true_cap[p] for p in providers) / len(providers)
            result.append((r.get("round", len(result)), gap))
    return result


def _t_critical(n):
    """95% t critical value for df = n-1."""
    try:
        from scipy.stats import t
        return float(t.ppf(0.975, df=n - 1))
    except ImportError:
        return 2.0  # conservative fallback


def aggregate(run_list):
    """
    Given a list of registry rows, load their rounds.jsonl files and
    return (rounds, means, lower_ci, upper_ci, n_per_round).
    """
    round_gaps = {}  # {round_num: [gap, ...]}
    for row in run_list:
        for rnum, gap in gaming_gap_trajectory(load_rounds(row["path"])):
            round_gaps.setdefault(rnum, []).append(gap)

    sorted_rounds = sorted(round_gaps.keys())
    means, lowers, uppers, ns = [], [], [], []
    for rnum in sorted_rounds:
        vals = round_gaps[rnum]
        n    = len(vals)
        mu   = float(np.mean(vals))
        if n >= 2:
            se = float(np.std(vals, ddof=1)) / math.sqrt(n)
            hw = _t_critical(n) * se
        else:
            hw = 0.0
        means.append(mu)
        lowers.append(mu - hw)
        uppers.append(mu + hw)
        ns.append(n)

    return sorted_rounds, means, lowers, uppers, ns


# ---------------------------------------------------------------------------
# Registry filtering helpers
# ---------------------------------------------------------------------------

def condition_base(row):
    """Strip preset suffix to get base condition name."""
    cond = row.get("condition", "")
    for preset in ("_balanced", "_us", "_eu"):
        if cond.endswith(preset):
            return cond[: -len(preset)]
    return cond


def preset_of(row):
    cond = row.get("condition", "")
    if cond.endswith("_balanced"):
        return "balanced"
    if cond.endswith("_us"):
        return "us"
    if cond.endswith("_eu"):
        return "eu"
    return None


def filter_runs(registry, phase=None, model=None, cond_base=None, preset=None):
    out = registry
    if phase   is not None: out = [r for r in out if r.get("phase")  == phase]
    if model   is not None: out = [r for r in out if r.get("model")  == model]
    if preset  is not None: out = [r for r in out if preset_of(r)    == preset]
    if cond_base is not None:
        out = [r for r in out if condition_base(r) == cond_base]
    return out


def savefig(name):
    path = FIG_DIR / f"{name}.pdf"
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {path.relative_to(ROOT.parent)}")


# ---------------------------------------------------------------------------
# Figure 1 — Full ecosystem x 3 presets, llama vs qwen
# ---------------------------------------------------------------------------

def plot_presets(registry):
    """
    Two-panel figure: left = llama-70b, right = qwen-235b.
    Each panel shows 3 lines (balanced / US / EU) with 95% CI bands,
    full_ecosystem condition only.
    """
    models  = ["llama-70b", "qwen-235b"]
    presets = ["balanced", "us", "eu"]

    fig, axes = plt.subplots(1, 2, figsize=(13, 4), sharey=True)

    for ax, model in zip(axes, models):
        for preset in presets:
            runs = filter_runs(
                registry, phase="llm_core", model=model,
                cond_base="full_ecosystem", preset=preset,
            )
            if not runs:
                continue
            rnds, means, lowers, uppers, ns = aggregate(runs)
            n_rep = ns[0] if ns else 0
            color = MODEL_COLORS[model]
            ls    = PRESET_DASH[preset]
            label = f"{PRESET_LABELS[preset]} (N={n_rep})"
            ax.plot(rnds, means, color=color, linestyle=ls,
                    linewidth=1.8, label=label)
            ax.fill_between(rnds, lowers, uppers,
                            alpha=0.18, color=color)

        ax.set_title(MODEL_LABELS[model], fontsize=11)
        ax.set_xlabel("Round", fontsize=10)
        ax.axhline(0.10, color="black", linestyle="--",
                   linewidth=0.8, alpha=0.5, label="0.10 threshold")
        ax.legend(fontsize=8)
        ax.tick_params(labelsize=9)
        ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())

    axes[0].set_ylabel("Gaming gap (score \u2212 true capability)", fontsize=10)
    fig.suptitle(
        "Score inflation trajectories \u2014 full\_ecosystem, regulatory presets",
        fontsize=12,
    )
    plt.tight_layout()
    savefig("12_inflation_traj_presets")


# ---------------------------------------------------------------------------
# Figure 2 — All ablations x balanced preset, llama vs qwen side by side
# ---------------------------------------------------------------------------

def plot_ablations(registry):
    """
    Two-panel figure: left = llama-70b, right = qwen-235b.
    Each panel shows one line + CI band per ablation condition,
    balanced preset only.
    """
    models = ["llama-70b", "qwen-235b"]
    fig, axes = plt.subplots(1, 2, figsize=(15, 5), sharey=True)

    for ax, model in zip(axes, models):
        for cond_base, color in zip(ABLATION_ORDER, CONDITION_COLORS):
            runs = filter_runs(
                registry, phase="llm_core", model=model,
                cond_base=cond_base, preset="balanced",
            )
            if not runs:
                continue
            rnds, means, lowers, uppers, ns = aggregate(runs)
            n_rep = ns[0] if ns else 0
            label = CONDITION_LABELS.get(cond_base, cond_base)
            if n_rep > 1:
                label += f" (N={n_rep})"
            ax.plot(rnds, means, color=color, linewidth=1.6, label=label)
            ax.fill_between(rnds, lowers, uppers, alpha=0.12, color=color)

        ax.set_title(MODEL_LABELS[model], fontsize=11)
        ax.set_xlabel("Round", fontsize=10)
        ax.axhline(0.10, color="black", linestyle="--",
                   linewidth=0.8, alpha=0.5)
        ax.legend(fontsize=7, ncol=2)
        ax.tick_params(labelsize=9)

    axes[0].set_ylabel("Gaming gap (score \u2212 true capability)", fontsize=10)
    fig.suptitle(
        "Score inflation trajectories \u2014 all ablations, balanced preset",
        fontsize=12,
    )
    plt.tight_layout()
    savefig("13_inflation_traj_ablations")


# ---------------------------------------------------------------------------
# Figure 3 — LLM vs heuristic baseline, full_ecosystem x balanced
# ---------------------------------------------------------------------------

def plot_llm_vs_heuristic(registry):
    """
    Single panel comparing llama-70b, qwen-235b, and heuristic baseline
    under full_ecosystem_balanced. All three have N=30.
    """
    sources = [
        ("llm_core",          "llama-70b"),
        ("llm_core",          "qwen-235b"),
        ("heuristic_baseline","heuristic"),
    ]

    fig, ax = plt.subplots(figsize=(8, 4))

    for phase, model in sources:
        runs = filter_runs(
            registry, phase=phase, model=model,
            cond_base="full_ecosystem", preset="balanced",
        )
        if not runs:
            continue
        rnds, means, lowers, uppers, ns = aggregate(runs)
        n_rep = ns[0] if ns else 0
        color = MODEL_COLORS[model]
        label = f"{MODEL_LABELS[model]} (N={n_rep})"
        ax.plot(rnds, means, color=color, linewidth=2.0, label=label)
        ax.fill_between(rnds, lowers, uppers, alpha=0.18, color=color)

    ax.axhline(0.10, color="black", linestyle="--",
               linewidth=0.8, alpha=0.5, label="0.10 threshold")
    ax.set_xlabel("Round", fontsize=10)
    ax.set_ylabel("Gaming gap (score \u2212 true capability)", fontsize=10)
    ax.set_title(
        "Score inflation trajectories \u2014 LLM vs heuristic baseline\n"
        "full\_ecosystem, balanced preset, N=30 seeds",
        fontsize=11,
    )
    ax.legend(fontsize=9)
    ax.tick_params(labelsize=9)
    plt.tight_layout()
    savefig("14_inflation_traj_llm_vs_heuristic")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"Loading registry from {RUNS} ...")
    registry = load_registry()
    print(f"  {len(registry)} runs loaded.\n")

    print("Plotting Fig 12: presets ...")
    plot_presets(registry)

    print("Plotting Fig 13: ablations ...")
    plot_ablations(registry)

    print("Plotting Fig 14: LLM vs heuristic ...")
    plot_llm_vs_heuristic(registry)

    print("\nDone. All figures saved to overleaf/figures/validation/")
