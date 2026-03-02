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

# Add src/ to path
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_PROJECT_ROOT, "src"))


def resolve_exp_dir(exp_input: str) -> str:
    """
    Resolve an experiment directory from a number or full folder name.

    Accepts:
        "3", "03", "003"           -> matched by zero-padded prefix exp_003_*
        "exp_003_full_ecosystem_us" -> used directly
    """
    exp_root = os.path.join(_PROJECT_ROOT, "output", "experiments")

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
        plot_consumer_satisfaction,
        plot_consumer_switching,
        plot_evaluator_dashboard,
        plot_policymaker_dashboard,
        plot_funder_dashboard,
        plot_media_dashboard,
        plot_summary_dashboard,
        plot_incident_dashboard,
        plot_validity_over_time,
        plot_investment_comparison,
        plot_incident_analysis_dashboard,
        plot_barrier_to_entry_dashboard,
        plot_startup_cohort_dashboard,
    )

    dashboards = [
        ("summary_dashboard",                plot_summary_dashboard),
        ("provider_dashboard",               plot_provider_dashboard),
        ("consumer_satisfaction_dashboard",   plot_consumer_satisfaction),
        ("consumer_switching_dashboard",      plot_consumer_switching),
        ("evaluator_dashboard",              plot_evaluator_dashboard),
        ("policymaker_dashboard",            plot_policymaker_dashboard),
        ("funder_dashboard",                 plot_funder_dashboard),
        ("media_dashboard",                  plot_media_dashboard),
        ("incident_dashboard",               plot_incident_dashboard),
        ("validity_over_time",               plot_validity_over_time),
        ("investment_comparison",             plot_investment_comparison),
        ("incident_analysis_dashboard",      plot_incident_analysis_dashboard),
        ("barrier_to_entry_dashboard",       plot_barrier_to_entry_dashboard),
        ("startup_cohort_dashboard",         plot_startup_cohort_dashboard),
    ]

    for name, fn in dashboards:
        save_path = os.path.join(plots_dir, f"{name}.png")
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
