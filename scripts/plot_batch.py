#!/usr/bin/env python3
"""
Generate presentation-quality summary plots from a batch of heuristic runs.

Usage:
    python scripts/plot_batch.py <batch_dir>
    python scripts/plot_batch.py sandbox/experiments/batch_heuristic_20260402_162434

Reads all rounds.jsonl + config.json from subdirectories of <batch_dir>.
Outputs figures to <batch_dir>/plots/.

Figures:
    1. Score-Satisfaction Gap — US / EU / balanced full_ecosystem (1x3)
    2. Ablation Effect Sizes — grouped bar chart, all conditions (1 figure)
    3. Orientation Mechanism Deep-Dive — adjustable / fixed / max (1x3)
    4. Regulatory Regime Deep-Dive — US / EU / balanced incidents + interventions (1x3)
    5. Incident System Validation — safety investment vs incident rate (1x3)
"""
import argparse
import json
import math
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------

PROVIDER_COLORS = {
    "Orion Labs":      "#E63946",
    "Apex AI":         "#457B9D",
    "Genesis Systems": "#2A9D8F",
    "Mirage AI":       "#E9C46A",
    "OpenCore":        "#F4A261",
    "Spark AI":        "#264653",
}

PRESET_COLORS = {"us": "#E63946", "eu": "#457B9D", "balanced": "#2A9D8F"}

def _style_ax(ax, title="", xlabel="", ylabel=""):
    ax.set_title(title, fontsize=9, fontweight="bold")
    ax.set_xlabel(xlabel, fontsize=7)
    ax.set_ylabel(ylabel, fontsize=7)
    ax.tick_params(labelsize=6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def _pres_figsize(n_cols):
    return (3.6 * n_cols, 2.8)


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_batch(batch_dir):
    """Load all runs from a batch directory.

    Returns dict: {(condition, preset): {"rounds": [...], "config": {...}}}
    """
    runs = {}
    for entry in sorted(os.listdir(batch_dir)):
        run_dir = os.path.join(batch_dir, entry)
        rounds_path = os.path.join(run_dir, "rounds.jsonl")
        config_path = os.path.join(run_dir, "config.json")
        if not os.path.isfile(rounds_path):
            continue

        # Parse condition and preset from directory name
        # Format: {condition}_{preset}_heuristic_{timestamp}
        # e.g. full_ecosystem_us_heuristic_20260402_162435
        parts = entry.split("_heuristic_")[0] if "_heuristic_" in entry else entry.split("_llm_")[0]
        # Last token is the preset
        tokens = parts.split("_")
        preset = tokens[-1]
        condition = "_".join(tokens[:-1])

        if preset not in ("us", "eu", "balanced"):
            continue

        rounds = []
        with open(rounds_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    rounds.append(json.loads(line))

        config = {}
        if os.path.isfile(config_path):
            with open(config_path) as f:
                config = json.load(f)

        runs[(condition, preset)] = {"rounds": rounds, "config": config}

    return runs


# ---------------------------------------------------------------------------
# Metric extraction
# ---------------------------------------------------------------------------

def _dot(a, b):
    return sum(a.get(k, 0) * b.get(k, 0) for k in set(a) | set(b))


def _norm(v):
    s = math.sqrt(sum(x * x for x in v.values()))
    return {k: x / s for k, x in v.items()} if s > 0 else v


def extract_gap_timeseries(rounds):
    """Per-provider score - satisfaction gap over time."""
    result = {}  # {provider: [gap_per_round]}
    for rd in rounds:
        scores = rd.get("scores", {})
        cd = rd.get("consumer_data", {})
        sats = cd.get("provider_satisfaction", {})
        for p in scores:
            if p not in result:
                result[p] = []
            result[p].append(scores[p] - sats.get(p, scores[p]))
    round_nums = [rd["round"] for rd in rounds]
    return round_nums, result


def extract_mean_gap(rounds):
    """Mean score-satisfaction gap across providers, final 5 rounds."""
    if len(rounds) < 5:
        return 0.0
    tail = rounds[-5:]
    gaps = []
    for rd in tail:
        scores = rd.get("scores", {})
        sats = rd.get("consumer_data", {}).get("provider_satisfaction", {})
        for p in scores:
            gaps.append(scores[p] - sats.get(p, scores[p]))
    return np.mean(gaps) if gaps else 0.0


def extract_mean_hhi(rounds):
    """Mean HHI across final 5 rounds."""
    if len(rounds) < 5:
        return 0.0
    hhis = []
    for rd in rounds[-5:]:
        shares = rd.get("consumer_data", {}).get("market_shares", {})
        if shares:
            hhis.append(sum(s ** 2 for s in shares.values()))
    return np.mean(hhis) if hhis else 0.0


def extract_mean_satisfaction(rounds):
    """Mean consumer satisfaction, final 5 rounds."""
    if len(rounds) < 5:
        return 0.0
    return np.mean([
        rd.get("consumer_data", {}).get("avg_satisfaction", 0.0)
        for rd in rounds[-5:]
    ])


def extract_incident_count(rounds):
    """Total incident count across all rounds."""
    total = 0
    for rd in rounds:
        inc = rd.get("incidents")
        if inc:
            total += len(inc)
    return total


def extract_incident_timeseries(rounds):
    """Per-round incident data: [(round, provider, severity), ...]"""
    events = []
    for rd in rounds:
        inc = rd.get("incidents")
        if inc:
            for i in inc:
                events.append((rd["round"], i["provider"], i["severity"]))
    return events


def extract_intervention_timeseries(rounds):
    """Per-round regulator interventions: [(round, action), ...]"""
    events = []
    for rd in rounds:
        reg = rd.get("regulator_data", {})
        interventions = reg.get("interventions", [])
        for iv in interventions:
            if isinstance(iv, dict):
                events.append((rd["round"], iv.get("action", "unknown")))
            elif isinstance(iv, str):
                events.append((rd["round"], iv))
    return events


def extract_safety_vs_incidents(rounds):
    """Per-round: mean safety allocation, cumulative incident rate."""
    cum_incidents = 0
    n_providers = 0
    result = []  # [(round, mean_safety_alloc, cum_incident_rate)]
    for rd in rounds:
        strats = rd.get("strategies", {})
        if strats:
            n_providers = len(strats)
            mean_safety = np.mean([s.get("safety", 0) for s in strats.values()])
        else:
            mean_safety = 0.0
        inc = rd.get("incidents")
        if inc:
            cum_incidents += len(inc)
        rate = cum_incidents / max(1, (rd["round"] + 1) * max(1, n_providers))
        result.append((rd["round"], mean_safety, rate))
    return result


# ---------------------------------------------------------------------------
# Figure 1: Score-Satisfaction Gap — 3 presets
# ---------------------------------------------------------------------------

def fig1_gap_presets(runs, output_dir):
    """Score-satisfaction gap for full_ecosystem across 3 presets."""
    fig, axes = plt.subplots(1, 3, figsize=_pres_figsize(3), sharey=True)

    for idx, preset in enumerate(("us", "eu", "balanced")):
        ax = axes[idx]
        key = ("full_ecosystem", preset)
        if key not in runs:
            _style_ax(ax, title=f"{preset.upper()} (missing)")
            continue

        round_nums, gaps = extract_gap_timeseries(runs[key]["rounds"])
        for provider, gap_series in gaps.items():
            color = PROVIDER_COLORS.get(provider, "#999999")
            ax.plot(round_nums[:len(gap_series)], gap_series,
                    color=color, linewidth=1.0, label=provider, alpha=0.8)

        ax.axhline(0, color="grey", linewidth=0.5, linestyle="--")
        _style_ax(ax, title=f"{preset.upper()}", xlabel="Round",
                  ylabel="Score - Satisfaction" if idx == 0 else "")

    # Legend outside
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, fontsize=6,
               bbox_to_anchor=(0.5, -0.08))
    fig.suptitle("Score-Satisfaction Gap by Regulatory Regime", fontsize=10,
                 fontweight="bold", y=1.02)
    fig.tight_layout()
    path = os.path.join(output_dir, "fig1_gap_presets.png")
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {path}")


# ---------------------------------------------------------------------------
# Figure 2: Ablation effect sizes — grouped bar chart
# ---------------------------------------------------------------------------

def fig2_ablation_bars(runs, output_dir):
    """Grouped bar chart: final-round mean gap per condition x preset."""
    # Collect all conditions
    conditions = sorted(set(c for c, p in runs.keys()))
    presets = ["us", "eu", "balanced"]

    # Compute baseline gap (full_ecosystem per preset)
    baseline = {}
    for preset in presets:
        key = ("full_ecosystem", preset)
        if key in runs:
            baseline[preset] = extract_mean_gap(runs[key]["rounds"])
        else:
            baseline[preset] = 0.0

    # Build data matrix
    data = {}  # {condition: {preset: gap}}
    for condition in conditions:
        data[condition] = {}
        for preset in presets:
            key = (condition, preset)
            if key in runs:
                data[condition][preset] = extract_mean_gap(runs[key]["rounds"])
            else:
                data[condition][preset] = np.nan

    n_conditions = len(conditions)
    n_presets = len(presets)
    x = np.arange(n_conditions)
    bar_width = 0.25

    fig_w = max(8, n_conditions * 0.9)
    fig, ax = plt.subplots(figsize=(fig_w, 3.5))

    for i, preset in enumerate(presets):
        values = [data[c].get(preset, np.nan) for c in conditions]
        bars = ax.bar(x + i * bar_width, values, bar_width,
                      label=preset.upper(), color=PRESET_COLORS[preset],
                      alpha=0.85, edgecolor="white", linewidth=0.5)

    ax.set_xticks(x + bar_width)
    ax.set_xticklabels([c.replace("_", "\n") for c in conditions],
                       fontsize=6, ha="center")
    ax.axhline(0, color="grey", linewidth=0.5, linestyle="--")
    ax.legend(fontsize=7, loc="upper right")
    _style_ax(ax, title="Score-Satisfaction Gap by Condition (final 5 rounds)",
              ylabel="Mean Gap (score - satisfaction)")

    fig.tight_layout()
    path = os.path.join(output_dir, "fig2_ablation_bars.png")
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {path}")


# ---------------------------------------------------------------------------
# Figure 3: Orientation mechanism deep-dive (1x3)
# ---------------------------------------------------------------------------

def fig3_orientation_deepdive(runs, output_dir):
    """Gap trajectory for adjustable / fixed / max orientation."""
    orientation_conditions = [
        ("bm_orientation_adjustable", "Adjustable"),
        ("full_ecosystem", "Fixed (0.80)"),
        ("bm_orientation_max", "Max (1.0)"),
    ]
    # Use balanced preset for clean comparison
    preset = "balanced"

    fig, axes = plt.subplots(1, 3, figsize=_pres_figsize(3), sharey=True)

    for idx, (condition, label) in enumerate(orientation_conditions):
        ax = axes[idx]
        key = (condition, preset)
        if key not in runs:
            _style_ax(ax, title=f"{label} (missing)")
            continue

        round_nums, gaps = extract_gap_timeseries(runs[key]["rounds"])
        for provider, gap_series in gaps.items():
            color = PROVIDER_COLORS.get(provider, "#999999")
            ax.plot(round_nums[:len(gap_series)], gap_series,
                    color=color, linewidth=1.0, label=provider, alpha=0.8)

        ax.axhline(0, color="grey", linewidth=0.5, linestyle="--")
        _style_ax(ax, title=label, xlabel="Round",
                  ylabel="Score - Satisfaction" if idx == 0 else "")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, fontsize=6,
               bbox_to_anchor=(0.5, -0.08))
    fig.suptitle("Orientation Mechanism: Impact on Score-Satisfaction Gap",
                 fontsize=10, fontweight="bold", y=1.02)
    fig.tight_layout()
    path = os.path.join(output_dir, "fig3_orientation_deepdive.png")
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {path}")


# ---------------------------------------------------------------------------
# Figure 4: Regulatory regime deep-dive — incidents + interventions (1x3)
# ---------------------------------------------------------------------------

SEVERITY_MARKERS = {"minor": ".", "moderate": "s", "major": "^", "critical": "X"}
SEVERITY_SIZES = {"minor": 15, "moderate": 25, "major": 40, "critical": 60}
SEVERITY_COLORS = {"minor": "#AAAAAA", "moderate": "#E9C46A", "major": "#E76F51", "critical": "#D62828"}

INTERVENTION_COLORS = {
    "request_voluntary_commitment": "#90BE6D",
    "publish_advisory":            "#F9C74F",
    "mandate_safety_disclosure":   "#F8961E",
    "commission_audit":            "#F3722C",
    "impose_sanction":             "#D62828",
    "emergency_investigation":     "#9B2226",
}
INTERVENTION_LABELS = {
    "request_voluntary_commitment": "Voluntary commitment",
    "publish_advisory":            "Advisory",
    "mandate_safety_disclosure":   "Disclosure mandate",
    "commission_audit":            "Audit",
    "impose_sanction":             "Sanction",
    "emergency_investigation":     "Emergency investigation",
}

def fig4_regulatory_deepdive(runs, output_dir):
    """Incident timeline + regulator interventions for 3 presets."""
    fig, axes = plt.subplots(1, 3, figsize=_pres_figsize(3))

    for idx, preset in enumerate(("us", "eu", "balanced")):
        ax = axes[idx]
        key = ("full_ecosystem", preset)
        if key not in runs:
            _style_ax(ax, title=f"{preset.upper()} (missing)")
            continue

        rounds_data = runs[key]["rounds"]
        incidents = extract_incident_timeseries(rounds_data)
        interventions = extract_intervention_timeseries(rounds_data)

        # Plot incidents as scatter (colored by severity)
        providers_in_run = list(runs[key]["rounds"][0].get("scores", {}).keys())
        provider_idx = {p: i for i, p in enumerate(providers_in_run)}

        for rnd, provider, severity in incidents:
            y = provider_idx.get(provider, 0)
            color = SEVERITY_COLORS.get(severity, "#999999")
            marker = SEVERITY_MARKERS.get(severity, "o")
            size = SEVERITY_SIZES.get(severity, 20)
            ax.scatter(rnd, y, c=color, marker=marker, s=size, alpha=0.85,
                       edgecolors="black", linewidths=0.3, zorder=5)

        # Plot interventions as colored vertical lines
        for rnd, action in interventions:
            color = INTERVENTION_COLORS.get(action, "#888888")
            ax.axvline(rnd, color=color, linewidth=1.2, alpha=0.7,
                       linestyle="-", zorder=3)

        ax.set_yticks(range(len(providers_in_run)))
        ax.set_yticklabels(providers_in_run, fontsize=5)
        _style_ax(ax, title=f"{preset.upper()}", xlabel="Round",
                  ylabel="Provider" if idx == 0 else "")

    # Build combined legend: severity markers + intervention lines
    from matplotlib.lines import Line2D
    legend_elements = []
    # Severity markers
    for sev in ("minor", "moderate", "major", "critical"):
        legend_elements.append(Line2D(
            [0], [0], marker=SEVERITY_MARKERS[sev], color="w",
            markerfacecolor=SEVERITY_COLORS[sev], markeredgecolor="black",
            markeredgewidth=0.3, markersize=SEVERITY_SIZES[sev] ** 0.5,
            label=sev.capitalize(), linestyle="None"))
    # Intervention lines
    for action, label in INTERVENTION_LABELS.items():
        legend_elements.append(Line2D(
            [0], [0], color=INTERVENTION_COLORS[action],
            linewidth=1.2, alpha=0.7, label=label))

    fig.legend(handles=legend_elements, loc="lower center",
               ncol=5, fontsize=5, bbox_to_anchor=(0.5, -0.12))
    fig.suptitle("Incidents & Regulatory Interventions by Regime",
                 fontsize=10, fontweight="bold", y=1.02)
    fig.tight_layout()
    path = os.path.join(output_dir, "fig4_regulatory_deepdive.png")
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {path}")


# ---------------------------------------------------------------------------
# Figure 5: Incident system validation — safety investment vs incidents (1x3)
# ---------------------------------------------------------------------------

def fig5_incident_validation(runs, output_dir):
    """Safety allocation vs cumulative incident rate for 3 presets."""
    fig, axes = plt.subplots(1, 3, figsize=_pres_figsize(3), sharey=True)

    for idx, preset in enumerate(("us", "eu", "balanced")):
        ax = axes[idx]
        key = ("full_ecosystem", preset)
        if key not in runs:
            _style_ax(ax, title=f"{preset.upper()} (missing)")
            continue

        data = extract_safety_vs_incidents(runs[key]["rounds"])
        round_nums = [d[0] for d in data]
        safety_alloc = [d[1] for d in data]
        incident_rate = [d[2] for d in data]

        ax.plot(round_nums, safety_alloc, color="#457B9D", linewidth=1.2,
                label="Mean safety alloc.")
        ax2 = ax.twinx()
        ax2.plot(round_nums, incident_rate, color="#E63946", linewidth=1.2,
                 linestyle="--", label="Cum. incident rate")
        ax2.tick_params(labelsize=6)
        if idx == 2:
            ax2.set_ylabel("Cum. incident rate", fontsize=7, color="#E63946")
        else:
            ax2.set_yticklabels([])
        ax2.spines["top"].set_visible(False)

        _style_ax(ax, title=f"{preset.upper()}", xlabel="Round",
                  ylabel="Mean safety allocation" if idx == 0 else "")

    # Manual legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color="#457B9D", linewidth=1.2, label="Safety alloc."),
        Line2D([0], [0], color="#E63946", linewidth=1.2, linestyle="--",
               label="Cum. incident rate"),
    ]
    fig.legend(handles=legend_elements, loc="lower center", ncol=2, fontsize=6,
               bbox_to_anchor=(0.5, -0.06))
    fig.suptitle("Safety Investment vs Incident Rate by Regime",
                 fontsize=10, fontweight="bold", y=1.02)
    fig.tight_layout()
    path = os.path.join(output_dir, "fig5_incident_validation.png")
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate summary plots from a batch of experiment runs.")
    parser.add_argument("batch_dir", help="Path to batch directory")
    args = parser.parse_args()

    batch_dir = args.batch_dir
    if not os.path.isdir(batch_dir):
        print(f"ERROR: {batch_dir} is not a directory")
        sys.exit(1)

    print(f"Loading runs from {batch_dir} ...")
    runs = load_batch(batch_dir)
    print(f"  Loaded {len(runs)} runs:")
    for (c, p) in sorted(runs.keys()):
        n = len(runs[(c, p)]["rounds"])
        print(f"    {c} / {p}: {n} rounds")

    output_dir = os.path.join(batch_dir, "_plots")
    os.makedirs(output_dir, exist_ok=True)

    print(f"\nGenerating figures to {output_dir} ...")
    fig1_gap_presets(runs, output_dir)
    fig2_ablation_bars(runs, output_dir)
    fig3_orientation_deepdive(runs, output_dir)
    fig4_regulatory_deepdive(runs, output_dir)
    fig5_incident_validation(runs, output_dir)

    print("\nDone.")


if __name__ == "__main__":
    main()
