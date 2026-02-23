"""
replot.py — Regenerate all plots for a finished experiment.

Usage:
    python replot.py 3
    python replot.py 003
    python replot.py exp_003_full_ecosystem_us

The script resolves the experiment folder from experiments/index.json using
the experiment number, then calls every dashboard function on the saved
history.json and overwrites the plots/ directory.
"""
import argparse
import json
import os
import sys


def resolve_exp_dir(exp_input: str) -> str:
    """
    Resolve an experiment directory from a number or full folder name.

    Accepts:
        "3", "03", "003"           -> matched by zero-padded prefix exp_003_*
        "exp_003_full_ecosystem_us" -> used directly
    """
    exp_root = os.path.join(os.path.dirname(__file__), "experiments")

    # If it looks like a full folder name, use directly
    if exp_input.startswith("exp_"):
        candidate = os.path.join(exp_root, exp_input)
        if os.path.isdir(candidate):
            return candidate
        sys.exit(f"Error: directory not found: {candidate}")

    # Otherwise treat as a number
    try:
        num = int(exp_input)
    except ValueError:
        sys.exit(f"Error: cannot parse experiment input '{exp_input}'")

    prefix = f"exp_{num:03d}_"
    matches = [
        d for d in os.listdir(exp_root)
        if d.startswith(prefix) and os.path.isdir(os.path.join(exp_root, d))
    ]
    if not matches:
        sys.exit(f"Error: no experiment folder matching '{prefix}*' found in {exp_root}")
    if len(matches) > 1:
        sys.exit(f"Error: multiple matches for '{prefix}*': {matches}. Use the full folder name.")
    return os.path.join(exp_root, matches[0])


def main():
    parser = argparse.ArgumentParser(
        description="Regenerate all dashboard plots for a finished experiment."
    )
    parser.add_argument(
        "experiment",
        help="Experiment number (e.g. 3, 03, 003) or full folder name (e.g. exp_003_full_ecosystem_us)",
    )
    args = parser.parse_args()

    exp_dir = resolve_exp_dir(args.experiment)
    history_path = os.path.join(exp_dir, "history.json")
    plots_dir = os.path.join(exp_dir, "plots")

    if not os.path.isfile(history_path):
        sys.exit(f"Error: history.json not found in {exp_dir}")

    os.makedirs(plots_dir, exist_ok=True)

    print(f"Experiment : {os.path.basename(exp_dir)}")
    print(f"History    : {history_path}")
    print(f"Output dir : {plots_dir}")
    print()

    with open(history_path, encoding="utf-8") as f:
        history = json.load(f)

    print(f"Loaded {len(history)} rounds of history.")

    # Import here so tueplots rcParams are applied before any figure is created
    from plotting import (
        plot_provider_dashboard,
        plot_consumer_dashboard,
        plot_evaluator_dashboard,
        plot_policymaker_dashboard,
        plot_funder_dashboard,
        plot_media_dashboard,
        plot_summary_dashboard,
        plot_incident_dashboard,
    )

    dashboards = [
        ("summary",     plot_summary_dashboard),
        ("provider",    plot_provider_dashboard),
        ("consumer",    plot_consumer_dashboard),
        ("evaluator",   plot_evaluator_dashboard),
        ("policymaker", plot_policymaker_dashboard),
        ("funder",      plot_funder_dashboard),
        ("media",       plot_media_dashboard),
        ("incident",    plot_incident_dashboard),
    ]

    for name, fn in dashboards:
        save_path = os.path.join(plots_dir, f"{name}_dashboard.png")
        print(f"  Plotting {name}...", end=" ", flush=True)
        try:
            result = fn(history, save_path=save_path, show=False)
            if result is None:
                print("skipped (no data)")
            else:
                print(f"saved -> {save_path}")
        except Exception as exc:
            print(f"FAILED: {exc}")

    print("\nDone.")


if __name__ == "__main__":
    main()
