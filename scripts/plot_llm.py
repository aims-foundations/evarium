"""
plot_llm.py -- Visualization for LLM aggregation outputs.

Reads from output/llm_analysis/*.csv and writes PDFs to
output/llm_analysis/plots/.

Six plots, designed for readability across 18+ conditions:
  1. endpoint_panels.pdf       6 endpoint metrics, theme-grouped horizontal bars
  2. pathway_flip.pdf          LLM vs heuristic modal pathway, per condition
  3. outcome_grid.pdf          condition x (winner|structure|pathway) tile heatmap
  4. incident_response.pdf     fraction safety-up by condition, with Wilson CI
  5. evaluator_case_study.pdf  3 trajectories: full_eco/221, full_eco/427, dyn_eval/221
  6. divergence_full_eco.pdf   full_ecosystem balanced 221 vs 427 divergence

Usage:
  python scripts/plot_llm.py
  python scripts/plot_llm.py --skip outcome_grid
  python scripts/plot_llm.py --only evaluator_case_study
"""

import argparse
import csv
import json
import math
import os
import sys
import warnings
from collections import Counter, defaultdict

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LLM_OUT = os.path.join(_PROJECT_ROOT, "output", "llm_analysis")
PLOTS_DIR = os.path.join(LLM_OUT, "plots")
HEURISTIC_ABLATION_CSV = os.path.join(
    _PROJECT_ROOT, "output", "heuristic_analysis", "ablation_effects.csv"
)


# ============================================================================
# Theme grouping for the 18+ conditions
# ============================================================================

THEMES = [
    ("Baseline / initial structure",
     ["full_ecosystem", "initial_duopoly", "initial_leader", "initial_uniform"]),
    ("Ecosystem removals",
     ["no_funders", "no_incidents", "no_media", "no_opensource",
      "no_product_channels", "no_regulator"]),
    ("Evaluation mechanics",
     ["aligned_benchmarks", "bm_orientation_adjustable", "bm_orientation_max",
      "dynamic_evaluator", "eval_as_company", "eval_full_autonomy",
      "eval_randomized_pool"]),
    ("Consumer / market",
     ["fixed_market_size", "homogeneous_consumers", "static_consumer_market"]),
]

# Default policy: only the balanced primary cells appear in most plots
PRIMARY_POLICY = "balanced"
PRIMARY_SEED = 221


def ordered_conditions(present_conditions: set) -> list:
    """Return conditions ordered by theme grouping; conditions not in any theme
    fall through alphabetically at the end."""
    out = []
    seen = set()
    for _, conds in THEMES:
        for c in conds:
            if c in present_conditions:
                out.append(c)
                seen.add(c)
    leftover = sorted(present_conditions - seen)
    return out + leftover


def theme_of(condition: str) -> str:
    for label, conds in THEMES:
        if condition in conds:
            return label
    return "Other"


def theme_separator_indices(conditions: list) -> list:
    """Return y-axis indices where horizontal separators should be drawn
    (between adjacent rows belonging to different themes)."""
    seps = []
    for i in range(1, len(conditions)):
        if theme_of(conditions[i]) != theme_of(conditions[i - 1]):
            seps.append(i - 0.5)
    return seps


# ============================================================================
# Plotting setup
# ============================================================================

def setup_plt():
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    try:
        from tueplots import bundles as _tb
        rc = _tb.neurips2024()
        rc.pop("figure.figsize", None)
        if os.environ.get("MPLLATEX", "1") != "0":
            rc["text.usetex"] = True
        mpl.rcParams.update(rc)
    except Exception as e:
        warnings.warn(f"tueplots not available -- using defaults ({e})")
    return plt


# Color palettes -- DISJOINT across the three categorical columns so the same
# color never means two different things on the same plot.
# Winners use tab10 primary hues; structure uses grayscale; pathway uses
# tab10 alternates (cyan/olive/pink) which don't collide with the primaries.
PATHWAY_COLORS = {
    "rd_led": "#17becf",     # cyan (distinct from Orion blue)
    "safety_led": "#bcbd22", # olive (distinct from Genesis green)
    "product_led": "#e377c2",# pink  (distinct from Mirage red)
    "": "#cccccc",
}
STRUCTURE_COLORS = {
    "competitive": "#f0f0f0",  # near-white
    "moderate":    "#969696",  # mid grey
    "concentrated":"#252525",  # near-black
    "": "#cccccc",
}
WINNER_COLORS = {
    "Orion Labs": "#1f77b4",
    "Apex AI": "#ff7f0e",
    "Genesis Systems": "#2ca02c",
    "Mirage AI": "#d62728",
    "OpenCore": "#9467bd",
    "Spark AI": "#8c564b",
    "": "#cccccc",
    "unknown": "#cccccc",
}


# ============================================================================
# Data loading
# ============================================================================

def _read_csv(name: str) -> list:
    path = os.path.join(LLM_OUT, name)
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _fnum(s, default=None):
    try:
        return float(s)
    except (TypeError, ValueError):
        return default


def load_data():
    return {
        "summary": _read_csv("llm_summary.csv"),
        "vs_heuristic": _read_csv("llm_vs_heuristic_outcomes.csv"),
        "incidents": _read_csv("llm_incident_response.csv"),
    }


def load_trajectory(condition: str, policy: str, seed: int) -> dict:
    """Load one trajectory CSV. Returns dict {metric: [values]}."""
    name = f"{condition}_{policy}_seed{seed}.csv"
    path = os.path.join(LLM_OUT, "llm_trajectory_data", name)
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames or []
        result = {c: [] for c in cols}
        for row in reader:
            for c in cols:
                result[c].append(_fnum(row[c], float("nan")))
    return result


def load_eval_case_study() -> dict:
    """Load evaluator_case_study.csv grouped by (condition, seed)."""
    path = os.path.join(LLM_OUT, "evaluator_case_study.csv")
    if not os.path.exists(path):
        return {}
    grouped = defaultdict(list)
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = (row["condition"], int(row["seed"]))
            grouped[key].append(row)
    for key in grouped:
        grouped[key].sort(key=lambda r: int(r["round"]))
    return dict(grouped)


# ============================================================================
# Wilson CI for incident-response binomial proportion
# ============================================================================

def wilson_ci(k: int, n: int, z: float = 1.96):
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (p, max(center - half, 0.0), min(center + half, 1.0))


# ============================================================================
# Plot 1: Endpoint metric panels
# ============================================================================

ENDPOINT_METRICS = [
    ("total_gap",          "score-satisfaction gap",   None),
    ("score_reliability",  "score reliability",        (0.0, 1.05)),
    ("hhi",                "HHI",                      (0.0, 1.05)),
    ("mean_safety",        "mean safety alloc",        (0.0, 0.5)),
    ("mean_satisfaction",  "mean satisfaction",        (0.0, 1.0)),
    ("incidents_per_round","incidents / round",        None),
]


def plot_endpoint_panels(data, plt):
    rows = [r for r in data["summary"]
            if r["policy"] == PRIMARY_POLICY and int(r["seed"]) == PRIMARY_SEED]
    if not rows:
        print("  endpoint_panels: no rows")
        return

    conditions = ordered_conditions({r["condition"] for r in rows})
    by_cond = {r["condition"]: r for r in rows}
    seps = theme_separator_indices(conditions)

    n_metrics = len(ENDPOINT_METRICS)
    fig, axes = plt.subplots(
        1, n_metrics, figsize=(2.0 * n_metrics, 0.32 * len(conditions) + 1.2),
        sharey=True,
    )
    if n_metrics == 1:
        axes = [axes]

    y_pos = list(range(len(conditions)))
    for ax, (metric, label, ylim) in zip(axes, ENDPOINT_METRICS):
        vals = [_fnum(by_cond[c][metric], 0.0) for c in conditions]
        bars = ax.barh(y_pos, vals, color="#4c72b0", edgecolor="black",
                       linewidth=0.4, height=0.7)

        # Highlight negative gap
        if metric == "total_gap":
            for b, v in zip(bars, vals):
                if v < 0:
                    b.set_color("#dd8452")
            ax.axvline(0, color="black", linewidth=0.5)

        ax.set_title(label, fontsize=9)
        if ylim:
            ax.set_xlim(*ylim)
        for s in seps:
            ax.axhline(s, color="gray", linewidth=0.4, linestyle=":")
        ax.tick_params(axis="x", labelsize=7)
        ax.tick_params(axis="y", labelsize=7)

    axes[0].set_yticks(y_pos)
    axes[0].set_yticklabels(conditions)
    axes[0].invert_yaxis()  # first theme on top

    # Add theme labels on the far left
    fig.canvas.draw()
    fig.suptitle(f"LLM endpoint metrics (last 5 rounds, balanced/seed{PRIMARY_SEED})",
                 fontsize=10, y=0.995)
    fig.tight_layout(rect=(0, 0, 1, 0.97))

    out = os.path.join(PLOTS_DIR, "endpoint_panels.pdf")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"  Wrote {out}")


# ============================================================================
# Plot 2: Pathway flip — LLM vs heuristic modal
# ============================================================================

def plot_pathway_flip(data, plt):
    rows = [r for r in data["vs_heuristic"]
            if r["policy"] == PRIMARY_POLICY]
    if not rows:
        print("  pathway_flip: no rows")
        return

    # Collapse to one row per (condition, policy) — when N_llm > 1 we use first
    by_cond = {}
    for r in rows:
        if r["condition"] not in by_cond:
            by_cond[r["condition"]] = r

    conditions = ordered_conditions(set(by_cond.keys()))
    seps = theme_separator_indices(conditions)

    fig, ax = plt.subplots(figsize=(5.0, 0.32 * len(conditions) + 1.2))
    y_pos = list(range(len(conditions)))

    pathway_x = {"rd_led": 0, "safety_led": 1, "product_led": 2}
    for i, c in enumerate(conditions):
        row = by_cond[c]
        llm = row["llm_pathway"]
        heur = row["heuristic_modal_pathway"]
        if llm in pathway_x:
            ax.scatter(pathway_x[llm], i,
                       s=110, c=PATHWAY_COLORS[llm],
                       marker="o", edgecolor="black", linewidth=0.6, zorder=3)
        if heur in pathway_x:
            ax.scatter(pathway_x[heur] + 0.18, i,
                       s=80, facecolor="white",
                       edgecolor=PATHWAY_COLORS[heur], linewidth=1.4,
                       marker="o", zorder=3)
        # Connecting line if they differ
        if llm != heur and llm in pathway_x and heur in pathway_x:
            ax.plot([pathway_x[llm], pathway_x[heur] + 0.18], [i, i],
                    color="gray", linewidth=0.6, linestyle=":", zorder=1)

    for s in seps:
        ax.axhline(s, color="gray", linewidth=0.4, linestyle=":")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(conditions, fontsize=8)
    ax.invert_yaxis()
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(["rd_led", "safety_led", "product_led"], fontsize=8)
    ax.set_xlim(-0.5, 2.7)
    ax.set_title("Leader pathway: LLM (filled) vs heuristic modal (open)",
                 fontsize=10)

    # Legend
    from matplotlib.lines import Line2D
    handles = [
        Line2D([0], [0], marker="o", color="w",
               markerfacecolor="#666", markeredgecolor="black",
               markersize=10, label="LLM (1 seed)"),
        Line2D([0], [0], marker="o", color="w",
               markerfacecolor="white", markeredgecolor="#666",
               markersize=10, markeredgewidth=1.4,
               label="heuristic (modal of 30 seeds)"),
    ]
    ax.legend(handles=handles, loc="upper right", fontsize=7,
              frameon=True, framealpha=0.9)

    fig.tight_layout()
    out = os.path.join(PLOTS_DIR, "pathway_flip.pdf")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"  Wrote {out}")


# ============================================================================
# Plot 3: Outcome grid (heatmap of categorical outcomes)
# ============================================================================

def plot_outcome_grid(data, plt):
    rows = [r for r in data["vs_heuristic"]
            if r["policy"] == PRIMARY_POLICY]
    if not rows:
        print("  outcome_grid: no rows")
        return

    by_cond = {}
    for r in rows:
        if r["condition"] not in by_cond:
            by_cond[r["condition"]] = r

    conditions = ordered_conditions(set(by_cond.keys()))
    seps = theme_separator_indices(conditions)

    fig, ax = plt.subplots(figsize=(5.0, 0.32 * len(conditions) + 1.2))

    # Six tile columns: LLM_winner | H_winner | LLM_struct | H_struct | LLM_path | H_path
    col_groups = [
        ("market_winner", WINNER_COLORS, "winner"),
        ("market_structure", STRUCTURE_COLORS, "structure"),
        ("leader_pathway", PATHWAY_COLORS, "pathway"),
    ]

    import matplotlib.patches as mp
    n_cols = 6
    cell_w = 0.9
    gap_between_groups = 0.4

    x_centers = []
    x = 0.0
    for gi, _ in enumerate(col_groups):
        x_centers.append(x); x += cell_w
        x_centers.append(x); x += cell_w + gap_between_groups

    for i, c in enumerate(conditions):
        row = by_cond[c]
        for gi, (key, palette, label) in enumerate(col_groups):
            llm_key_name = "llm_" + ("structure" if key == "market_structure"
                                     else ("winner" if key == "market_winner"
                                           else "pathway"))
            heur_key_name = ("heuristic_modal_" +
                             ("winner" if key == "market_winner"
                              else ("pathway" if key == "leader_pathway"
                                    else "structure")))
            llm_val = row.get(llm_key_name, "")
            # heuristic structure: use majority of c/m/cc counts as a stand-in
            if key == "market_structure":
                cn = int(row.get("heuristic_competitive_n", 0) or 0)
                mn = int(row.get("heuristic_moderate_n", 0) or 0)
                ccn = int(row.get("heuristic_concentrated_n", 0) or 0)
                heur_counts = {"competitive": cn, "moderate": mn,
                               "concentrated": ccn}
                heur_val = max(heur_counts, key=heur_counts.get)
            else:
                heur_val = row.get(heur_key_name, "")

            llm_color = palette.get(llm_val, "#cccccc")
            heur_color = palette.get(heur_val, "#cccccc")

            xL = x_centers[gi * 2]
            xH = x_centers[gi * 2 + 1]
            ax.add_patch(mp.Rectangle((xL - cell_w / 2, i - 0.4),
                                       cell_w, 0.8, facecolor=llm_color,
                                       edgecolor="black", linewidth=0.4))
            ax.add_patch(mp.Rectangle((xH - cell_w / 2, i - 0.4),
                                       cell_w, 0.8, facecolor=heur_color,
                                       edgecolor="black", linewidth=0.4))

    for s in seps:
        ax.axhline(s, color="black", linewidth=0.6, alpha=0.6)

    # X-axis: group labels
    ax.set_xticks(x_centers)
    xlabels = []
    for _, _, name in col_groups:
        xlabels += [f"L\\,{name}", f"H\\,{name}"]
    ax.set_xticklabels(xlabels, fontsize=7, rotation=30, ha="right")

    ax.set_yticks(list(range(len(conditions))))
    ax.set_yticklabels(conditions, fontsize=7)
    ax.invert_yaxis()
    ax.set_xlim(-0.7, x_centers[-1] + 0.7)
    ax.set_ylim(len(conditions) - 0.5, -0.7)
    ax.set_title("Outcome grid: LLM (L) vs heuristic modal (H)", fontsize=10)
    ax.set_aspect("auto")

    # Build a compact legend with each entry prefixed by category code so
    # the same color in two columns can never be ambiguous.
    from matplotlib.patches import Patch
    legend_handles = []
    blank = Patch(facecolor="white", edgecolor="white", label=" ")
    for prefix, palette in [("W", WINNER_COLORS),
                             ("S", STRUCTURE_COLORS),
                             ("P", PATHWAY_COLORS)]:
        for k, c in palette.items():
            if k in ("", "unknown"):
                continue
            legend_handles.append(
                Patch(facecolor=c, edgecolor="black",
                      label=f"[{prefix}] {k}"))
        legend_handles.append(blank)
    # Drop trailing blank
    if legend_handles and legend_handles[-1] is blank:
        legend_handles.pop()
    ax.legend(handles=legend_handles, loc="center left",
              bbox_to_anchor=(1.02, 0.5), fontsize=6, frameon=False,
              ncol=1, handlelength=1.2, handletextpad=0.4,
              labelspacing=0.25)

    fig.tight_layout()
    out = os.path.join(PLOTS_DIR, "outcome_grid.pdf")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"  Wrote {out}")


# ============================================================================
# Plot 4: Incident response forest plot
# ============================================================================

def plot_incident_response(data, plt):
    incs = data["incidents"]
    if not incs:
        print("  incident_response: no incidents")
        return

    by_cond = defaultdict(list)
    for r in incs:
        if r["policy"] != PRIMARY_POLICY or int(r["seed"]) != PRIMARY_SEED:
            continue
        by_cond[r["condition"]].append(r)

    rows = []
    for cond, lst in by_cond.items():
        n = len(lst)
        k = sum(1 for r in lst
                if (_fnum(r["safety_change_pp"], 0.0) or 0.0) > 0)
        p, lo, hi = wilson_ci(k, n)
        rows.append((cond, p, lo, hi, k, n))

    conditions = ordered_conditions({r[0] for r in rows})
    by = {r[0]: r for r in rows}
    seps = theme_separator_indices(conditions)

    fig, ax = plt.subplots(figsize=(4.8, 0.32 * len(conditions) + 1.2))
    y_pos = list(range(len(conditions)))

    for i, c in enumerate(conditions):
        _, p, lo, hi, k, n = by[c]
        ax.errorbar([p], [i], xerr=[[p - lo], [hi - p]], fmt="o",
                    markersize=5, color="#1f77b4", capsize=2.5,
                    elinewidth=0.8)
        ax.text(1.04, i, f"{k}/{n}", va="center", fontsize=6,
                color="#444")

    ax.axvline(0.5, color="gray", linewidth=0.6, linestyle="--")
    for s in seps:
        ax.axhline(s, color="gray", linewidth=0.4, linestyle=":")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(conditions, fontsize=7)
    ax.invert_yaxis()
    ax.set_xlim(0, 1.15)
    ax.set_xlabel("fraction of incidents with safety up at N+1 (95\\% Wilson)",
                  fontsize=8)
    ax.set_title("Incident response: provider safety reaction",
                 fontsize=10)

    fig.tight_layout()
    out = os.path.join(PLOTS_DIR, "incident_response.pdf")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"  Wrote {out}")


# ============================================================================
# Plot 5: Evaluator case study trajectories
# ============================================================================

def _series(rows, key):
    return [_fnum(r[key], float("nan")) for r in rows]


def plot_evaluator_case_study(data, plt):
    grouped = load_eval_case_study()
    if not grouped:
        print("  evaluator_case_study: no data")
        return

    keys = sorted(grouped.keys())
    label_map = {
        ("full_ecosystem", 221): "full_ecosystem (s221)",
        ("full_ecosystem", 427): "full_ecosystem (s427)",
        ("dynamic_evaluator", 221): "dynamic_evaluator (s221)",
        ("eval_full_autonomy", 221): "eval_full_autonomy (s221)",
    }
    color_map = {
        ("full_ecosystem", 221): "#1f77b4",
        ("full_ecosystem", 427): "#aec7e8",
        ("dynamic_evaluator", 221): "#d62728",
        ("eval_full_autonomy", 221): "#2ca02c",
    }

    metrics = [
        ("score_reliability", "score reliability", (0, 1.05)),
        ("mean_gap", "score - satisfaction", None),
        ("hhi", "HHI", (0, 1.0)),
    ]
    fig, axes = plt.subplots(len(metrics), 1, figsize=(5.5, 5.5),
                              sharex=True)
    if len(metrics) == 1:
        axes = [axes]

    for ax, (mkey, mlabel, ylim) in zip(axes, metrics):
        for key in keys:
            rows = grouped[key]
            xs = [int(r["round"]) for r in rows]
            ys = _series(rows, mkey)
            ax.plot(xs, ys, label=label_map.get(key, str(key)),
                    color=color_map.get(key, None), linewidth=1.4)
        if mkey == "mean_gap":
            ax.axhline(0, color="black", linewidth=0.5)
        if ylim:
            ax.set_ylim(*ylim)
        ax.set_ylabel(mlabel, fontsize=8)
        ax.tick_params(axis="both", labelsize=7)
        ax.grid(alpha=0.2)

    axes[-1].set_xlabel("round", fontsize=8)
    axes[0].legend(loc="lower right", fontsize=7, frameon=True,
                   framealpha=0.9)
    fig.suptitle("Evaluator case study: passive vs dynamic vs autonomy",
                 fontsize=10, y=0.995)
    fig.tight_layout(rect=(0, 0, 1, 0.97))

    out = os.path.join(PLOTS_DIR, "evaluator_case_study.pdf")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"  Wrote {out}")


# ============================================================================
# Plot 6: Divergence — full_ecosystem balanced 221 vs 427
# ============================================================================

def plot_divergence_full_eco(data, plt):
    t221 = load_trajectory("full_ecosystem", "balanced", 221)
    t427 = load_trajectory("full_ecosystem", "balanced", 427)
    if not t221 or not t427:
        print("  divergence_full_eco: missing trajectory data")
        return

    metrics = [
        ("hhi", "HHI"),
        ("gap", "score - satisfaction"),
        ("safety", "mean safety alloc"),
    ]
    fig, axes = plt.subplots(len(metrics), 1, figsize=(5.5, 5.5),
                              sharex=True)
    if len(metrics) == 1:
        axes = [axes]

    for ax, (mkey, mlabel) in zip(axes, metrics):
        ax.plot(t221["round"], t221[mkey], label="seed 221", color="#1f77b4",
                linewidth=1.4)
        ax.plot(t427["round"], t427[mkey], label="seed 427", color="#d62728",
                linewidth=1.4)
        if mkey == "gap":
            ax.axhline(0, color="black", linewidth=0.5)
        ax.set_ylabel(mlabel, fontsize=8)
        ax.tick_params(axis="both", labelsize=7)
        ax.grid(alpha=0.2)

    axes[-1].set_xlabel("round", fontsize=8)
    axes[0].legend(loc="best", fontsize=7, frameon=True, framealpha=0.9)
    fig.suptitle("Divergence: full\\_ecosystem balanced, two seeds",
                 fontsize=10, y=0.995)
    fig.tight_layout(rect=(0, 0, 1, 0.97))

    out = os.path.join(PLOTS_DIR, "divergence_full_eco.pdf")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"  Wrote {out}")


# ============================================================================
# Plot 7: Heuristic ablation forest plot (single-policy slice)
# ============================================================================

def plot_heuristic_forest_balanced(data, plt):
    """Single-policy forest plot of ablation deltas vs full_ecosystem baseline.

    Reads output/heuristic_analysis/ablation_effects.csv. Plots deltas in
    total_gap with 95% CI. Theme-grouped, balanced policy only.
    """
    if not os.path.exists(HEURISTIC_ABLATION_CSV):
        print("  heuristic_forest_balanced: ablation_effects.csv not found")
        return

    with open(HEURISTIC_ABLATION_CSV, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    rows = [r for r in rows
            if r["policy"] == PRIMARY_POLICY and r["metric"] == "total_gap"]
    if not rows:
        print("  heuristic_forest_balanced: no balanced/total_gap rows")
        return

    by_cond = {r["condition"]: r for r in rows}
    conditions = ordered_conditions(set(by_cond.keys()))
    seps = theme_separator_indices(conditions)

    fig, ax = plt.subplots(figsize=(5.0, 0.32 * len(conditions) + 1.2))
    y_pos = list(range(len(conditions)))

    for i, c in enumerate(conditions):
        r = by_cond[c]
        delta = _fnum(r["delta"], 0.0)
        lo = _fnum(r["ci_lo"], 0.0)
        hi = _fnum(r["ci_hi"], 0.0)
        sig = (r.get("significant", "False") == "True")
        color = "#c0392b" if (sig and delta > 0) else (
            "#2980b9" if (sig and delta < 0) else "#888888")
        ax.errorbar([delta], [i],
                    xerr=[[delta - lo], [hi - delta]],
                    fmt="o", markersize=5, color=color,
                    capsize=2.5, elinewidth=0.8)

    ax.axvline(0, color="black", linewidth=0.6)
    for s in seps:
        ax.axhline(s, color="gray", linewidth=0.4, linestyle=":")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(conditions, fontsize=7)
    ax.invert_yaxis()
    ax.set_xlabel(r"$\Delta$ total\_gap vs full\_ecosystem (balanced, $N{=}30$)",
                  fontsize=8)
    ax.set_title("Heuristic ablation effects on score--satisfaction gap",
                 fontsize=10)

    # Legend
    from matplotlib.lines import Line2D
    handles = [
        Line2D([0], [0], marker="o", color="#c0392b", linestyle="",
               markersize=6, label="significant +"),
        Line2D([0], [0], marker="o", color="#2980b9", linestyle="",
               markersize=6, label="significant --"),
        Line2D([0], [0], marker="o", color="#888888", linestyle="",
               markersize=6, label="n.s."),
    ]
    ax.legend(handles=handles, loc="lower right", fontsize=7,
              frameon=True, framealpha=0.9)

    fig.tight_layout()
    out = os.path.join(PLOTS_DIR, "heuristic_forest_balanced.pdf")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"  Wrote {out}")


# ============================================================================
# Main
# ============================================================================

PLOT_FNS = {
    "endpoint_panels": plot_endpoint_panels,
    "pathway_flip": plot_pathway_flip,
    "outcome_grid": plot_outcome_grid,
    "incident_response": plot_incident_response,
    "evaluator_case_study": plot_evaluator_case_study,
    "divergence_full_eco": plot_divergence_full_eco,
    "heuristic_forest_balanced": plot_heuristic_forest_balanced,
}


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--skip", nargs="*", default=[],
                   help="Plot names to skip")
    p.add_argument("--only", nargs="*", default=None,
                   help="Restrict to these plot names")
    p.add_argument("--no-latex", action="store_true",
                   help="Disable matplotlib LaTeX rendering")
    return p.parse_args()


def main():
    args = parse_args()
    if args.no_latex:
        os.environ["MPLLATEX"] = "0"

    os.makedirs(PLOTS_DIR, exist_ok=True)
    plt = setup_plt()
    data = load_data()

    if not data["summary"]:
        print(f"No llm_summary.csv found at {LLM_OUT} -- did you run "
              f"aggregate_llm.py?")
        return

    todo = list(PLOT_FNS.keys())
    if args.only:
        todo = [k for k in todo if k in args.only]
    todo = [k for k in todo if k not in args.skip]

    print(f"Generating {len(todo)} plots -> {PLOTS_DIR}")
    for name in todo:
        try:
            PLOT_FNS[name](data, plt)
        except Exception as e:
            print(f"  FAILED {name}: {e}")
            import traceback
            traceback.print_exc()

    print("Done.")


if __name__ == "__main__":
    main()
