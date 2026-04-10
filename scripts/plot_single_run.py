#!/usr/bin/env python3
"""
plot_single_run.py — Presentation-quality single-run plots.

Based on the batch presentation style (plot_batch.py) but for individual runs.

Usage:
    python scripts/plot_single_run.py <run_dir>
    python scripts/plot_single_run.py <run_dir> --output <output_dir>
    python scripts/plot_single_run.py sandbox/experiments/apr8_.../full_ecosystem_balanced_llm_...

Plots generated:
    1. incidents_interventions  — incident timeline + regulatory interventions

Outputs to <run_dir>/plots/ by default, or --output <dir>.
"""
import argparse
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

# ---------------------------------------------------------------------------
# Styling — matches plot_batch.py presentation palette
# ---------------------------------------------------------------------------

PROVIDER_COLORS = {
    "Orion Labs":      "#E63946",
    "Apex AI":         "#457B9D",
    "Genesis Systems": "#2A9D8F",
    "Mirage AI":       "#E9C46A",
    "OpenCore":        "#F4A261",
    "Spark AI":        "#264653",
}

SEVERITY_MARKERS = {"minor": ".", "moderate": "s", "major": "^", "critical": "X"}
SEVERITY_SIZES   = {"minor": 15, "moderate": 25, "major": 40, "critical": 60}
SEVERITY_COLORS  = {"minor": "#AAAAAA", "moderate": "#E9C46A", "major": "#E76F51", "critical": "#D62828"}

# Escalation ladder — ordered from lightest to heaviest
ESCALATION_ORDER = [
    "request_voluntary_commitment",
    "publish_advisory",
    "mandate_safety_disclosure",
    "commission_audit",
    "impose_sanction",
    "emergency_investigation",
]

INTERVENTION_COLORS = {
    "request_voluntary_commitment": "#90BE6D",
    "publish_advisory":            "#F9C74F",
    "mandate_safety_disclosure":   "#F8961E",
    "commission_audit":            "#F3722C",
    "impose_sanction":             "#D62828",
    "emergency_investigation":     "#9B2226",
}

# Linewidth scales continuously with escalation level (0.6 → 1.8)
INTERVENTION_LINEWIDTHS = {
    action: 0.6 + 1.2 * (i / (len(ESCALATION_ORDER) - 1))
    for i, action in enumerate(ESCALATION_ORDER)
}

INTERVENTION_LABELS = {
    "request_voluntary_commitment": "Voluntary commitment",
    "publish_advisory":            "Advisory",
    "mandate_safety_disclosure":   "Disclosure mandate",
    "commission_audit":            "Audit",
    "impose_sanction":             "Sanction",
    "emergency_investigation":     "Emergency investigation",
}


def _style_ax(ax, title="", xlabel="", ylabel=""):
    ax.set_title(title, fontsize=9, fontweight="bold")
    ax.set_xlabel(xlabel, fontsize=7)
    ax.set_ylabel(ylabel, fontsize=7)
    ax.tick_params(labelsize=6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_rounds(run_dir):
    """Load rounds.jsonl from a single run directory."""
    path = os.path.join(run_dir, "rounds.jsonl")
    if not os.path.isfile(path):
        print(f"ERROR: {path} not found")
        sys.exit(1)
    rounds = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                rounds.append(json.loads(line))
    return rounds


# ---------------------------------------------------------------------------
# Metric extraction (from plot_batch.py)
# ---------------------------------------------------------------------------

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
                action = iv.get("type") or iv.get("action", "unknown")
                events.append((rd["round"], action))
            elif isinstance(iv, str):
                events.append((rd["round"], iv))
    return events


# ---------------------------------------------------------------------------
# Plot 1: Incidents & Interventions
# ---------------------------------------------------------------------------

def plot_incidents_interventions(rounds, output_dir):
    """Incident timeline + regulatory interventions (single run)."""
    fig, ax = plt.subplots(figsize=(5.5, 3.0))

    incidents = extract_incident_timeseries(rounds)
    interventions = extract_intervention_timeseries(rounds)

    # Provider y-axis mapping
    providers_in_run = list(rounds[0].get("scores", {}).keys())
    provider_idx = {p: i for i, p in enumerate(providers_in_run)}

    # Plot incidents as scatter (colored by severity)
    for rnd, provider, severity in incidents:
        y = provider_idx.get(provider, 0)
        color = SEVERITY_COLORS.get(severity, "#999999")
        marker = SEVERITY_MARKERS.get(severity, "o")
        size = SEVERITY_SIZES.get(severity, 20)
        ax.scatter(rnd, y, c=color, marker=marker, s=size, alpha=0.85,
                   edgecolors="black", linewidths=0.3, zorder=5)

    # Plot interventions as colored vertical lines with escalation-scaled linewidth
    for rnd, action in interventions:
        color = INTERVENTION_COLORS.get(action, "#888888")
        lw = INTERVENTION_LINEWIDTHS.get(action, 1.0)
        ax.axvline(rnd, color=color, linewidth=lw, alpha=0.7,
                   linestyle="--", zorder=3)

    ax.set_yticks(range(len(providers_in_run)))
    ax.set_yticklabels(providers_in_run, fontsize=6)
    _style_ax(ax, title="Incidents & Regulatory Interventions",
              xlabel="Round", ylabel="Provider")

    # Combined legend: severity markers + intervention lines
    legend_elements = []
    for sev in ("minor", "moderate", "major", "critical"):
        legend_elements.append(Line2D(
            [0], [0], marker=SEVERITY_MARKERS[sev], color="w",
            markerfacecolor=SEVERITY_COLORS[sev], markeredgecolor="black",
            markeredgewidth=0.3, markersize=SEVERITY_SIZES[sev] ** 0.5,
            label=sev.capitalize(), linestyle="None"))
    for action in ESCALATION_ORDER:
        label = INTERVENTION_LABELS.get(action, action)
        legend_elements.append(Line2D(
            [0], [0], color=INTERVENTION_COLORS[action],
            linewidth=INTERVENTION_LINEWIDTHS[action], alpha=0.7,
            linestyle="--", label=label))

    ax.legend(handles=legend_elements, loc="upper left",
              bbox_to_anchor=(1.02, 1.0), fontsize=5, frameon=True,
              borderpad=0.5, handlelength=2.0)

    fig.tight_layout()
    path = os.path.join(output_dir, "incidents_interventions.png")
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate presentation-quality plots for a single run.")
    parser.add_argument("run_dir", help="Path to a single run directory (contains rounds.jsonl)")
    parser.add_argument("--output", "-o", default=None,
                        help="Output directory (default: <run_dir>/plots/)")
    args = parser.parse_args()

    run_dir = args.run_dir
    if not os.path.isdir(run_dir):
        print(f"ERROR: {run_dir} is not a directory")
        sys.exit(1)

    output_dir = args.output or os.path.join(run_dir, "plots")
    os.makedirs(output_dir, exist_ok=True)

    print(f"Loading {run_dir} ...")
    rounds = load_rounds(run_dir)
    print(f"  {len(rounds)} rounds loaded")

    print(f"Generating plots to {output_dir} ...")
    plot_incidents_interventions(rounds, output_dir)

    print("Done.")


if __name__ == "__main__":
    main()
