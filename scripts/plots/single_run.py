"""Single-run presentation plots.

Per-run tool — writes to `<run_dir>/plots/` by default. Not a paper-canonical
figure; see `scripts.plots.paper.*` for those.

Plots generated:
    1. incidents_interventions.png — incident timeline + regulatory interventions

Usage:
    python -m scripts.plots.single_run <run_dir>
    python -m scripts.plots.single_run <run_dir> --output <output_dir>
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

SEVERITY_MARKERS = {"minor": ".", "moderate": "s", "major": "^", "critical": "X"}
SEVERITY_SIZES   = {"minor": 15, "moderate": 25, "major": 40, "critical": 60}
SEVERITY_COLORS  = {"minor": "#AAAAAA", "moderate": "#E9C46A", "major": "#E76F51", "critical": "#D62828"}

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


def load_rounds(run_dir):
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


def extract_incident_timeseries(rounds):
    events = []
    for rd in rounds:
        inc = rd.get("incidents")
        if inc:
            for i in inc:
                events.append((rd["round"], i["provider"], i["severity"]))
    return events


def extract_intervention_timeseries(rounds):
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


def plot_incidents_interventions(rounds, output_dir):
    fig, ax = plt.subplots(figsize=(5.5, 3.0))
    incidents = extract_incident_timeseries(rounds)
    interventions = extract_intervention_timeseries(rounds)

    providers_in_run = list(rounds[0].get("scores", {}).keys())
    provider_idx = {p: i for i, p in enumerate(providers_in_run)}

    for rnd, provider, severity in incidents:
        y = provider_idx.get(provider, 0)
        color = SEVERITY_COLORS.get(severity, "#999999")
        marker = SEVERITY_MARKERS.get(severity, "o")
        size = SEVERITY_SIZES.get(severity, 20)
        ax.scatter(rnd, y, c=color, marker=marker, s=size, alpha=0.85,
                   edgecolors="black", linewidths=0.3, zorder=5)

    for rnd, action in interventions:
        color = INTERVENTION_COLORS.get(action, "#888888")
        lw = INTERVENTION_LINEWIDTHS.get(action, 1.0)
        ax.axvline(rnd, color=color, linewidth=lw, alpha=0.7,
                   linestyle="--", zorder=3)

    ax.set_yticks(range(len(providers_in_run)))
    ax.set_yticklabels(providers_in_run, fontsize=6)
    _style_ax(ax, title="Incidents & Regulatory Interventions",
              xlabel="Round", ylabel="Provider")

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


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("run_dir", help="Path to a single run directory (contains rounds.jsonl)")
    ap.add_argument("--output", "-o", default=None,
                    help="Output directory (default: <run_dir>/plots/)")
    args = ap.parse_args()

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
