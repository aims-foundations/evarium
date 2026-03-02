"""
Run diagnostics on existing experiment data.

Performs trajectory inspection, strategy drift detection, role adherence
checks, pattern validation, and ablation comparison on all available
experiments.
"""

import json
import os
import sys
import warnings

import matplotlib as mpl
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# ---------------------------------------------------------------------------
# Tueplots NeurIPS styling with LaTeX fonts
# ---------------------------------------------------------------------------
try:
    from tueplots import bundles as _tueplots_bundles

    _NEURIPS_RC = _tueplots_bundles.neurips2024()
    _NEURIPS_RC.pop("figure.figsize", None)
    # Enable LaTeX rendering for publication-quality fonts.
    # Set MPLLATEX=0 in the environment to disable if LaTeX is not available.
    if os.environ.get("MPLLATEX", "1") != "0":
        _NEURIPS_RC["text.usetex"] = True
    mpl.rcParams.update(_NEURIPS_RC)
except ImportError:
    warnings.warn(
        "tueplots not installed — using default matplotlib style. "
        "Run: pip install tueplots",
        stacklevel=1,
    )

import matplotlib.pyplot as plt  # noqa: E402 — must come after rcParams update

from diagnostics import (
    aggregate_replications,
    analyze_prompt_sensitivity,
    check_patterns,
    check_role_adherence,
    detect_strategy_drift_all_providers,
    extract_metric_series,
    metric_bte_composite,
    metric_consumer_satisfaction,
    metric_hhi,
    metric_incident_count,
    metric_mean_benchmark_validity,
    metric_mean_eval_engineering,
    metric_mean_gaming_gap,
    metric_mean_safety_alignment,
    metric_mean_score,
    metric_mean_true_capability,
)
from diagnostic_plots import (
    plot_crn_paired_difference,
    plot_pattern_validation_checklist,
    plot_strategy_drift_heatmap,
    plot_trace_overlay,
    plot_trace_overlay_multi,
)

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "output", "experiments")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output", "diagnostics")

METRICS = {
    "Mean True Capability": (metric_mean_true_capability, "Capability"),
    "Mean Benchmark Score": (metric_mean_score, "Score"),
    "Mean Gaming Gap": (metric_mean_gaming_gap, "Gap (score - capability)"),
    "Mean Eval Engineering": (metric_mean_eval_engineering, "Investment fraction"),
    "Mean Safety Alignment": (metric_mean_safety_alignment, "Investment fraction"),
    "HHI (Market Concentration)": (metric_hhi, "HHI"),
    "Consumer Satisfaction": (metric_consumer_satisfaction, "Satisfaction"),
    "Mean Benchmark Validity": (metric_mean_benchmark_validity, "Validity"),
    "Incident Count": (metric_incident_count, "Count"),
    "Barrier to Entry": (metric_bte_composite, "BTE composite"),
}

# Experiment groups
CANONICAL_50 = [
    "exp_013_full_ecosystem_balanced",
    "exp_014_full_ecosystem_us",
    "exp_015_full_ecosystem_eu",
]

BASELINE_30 = "exp_011_full_ecosystem_balanced"

ABLATIONS_30 = {
    "no_media": "exp_004_ablation_no_media_balanced",
    "no_incidents": "exp_005_ablation_no_incidents_balanced",
    "no_startups": "exp_006_ablation_no_startups_balanced",
    "no_opencore": "exp_007_ablation_no_opencore_balanced",
    "single_benchmark": "exp_008_ablation_single_benchmark_balanced",
    "no_funders": "exp_009_ablation_no_funders_balanced",
    "no_bench_evolution": "exp_010_ablation_no_benchmark_evolution_balanced",
    "eval_as_company": "exp_012_ablation_eval_as_company_balanced",
}


def load_history(exp_id):
    path = os.path.join(BASE_DIR, exp_id, "history.json")
    with open(path) as f:
        return json.load(f)


def run_single_experiment_diagnostics(exp_id, out_dir):
    """Run all single-run diagnostics for one experiment."""
    print(f"\n{'='*60}")
    print(f"  Diagnosing: {exp_id}")
    print(f"{'='*60}")

    history = load_history(exp_id)
    n_rounds = len(history)
    print(f"  Rounds: {n_rounds}")

    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(os.path.join(out_dir, "plots"), exist_ok=True)

    results = {"experiment": exp_id, "n_rounds": n_rounds}

    # --- Trajectory metrics ---
    print("  Computing trajectory metrics...")
    trajectories = {}
    for name, (fn, _ylabel) in METRICS.items():
        series = extract_metric_series([history], fn)
        vals = series[0].tolist()
        trajectories[name] = {
            "values": vals,
            "final": vals[-1] if vals else None,
            "mean": float(np.nanmean(vals)),
        }
    results["trajectories"] = trajectories

    # --- Strategy drift ---
    print("  Detecting strategy drift...")
    drift_data = detect_strategy_drift_all_providers(history)
    drift_summary = {}
    for provider, scores in drift_data.items():
        valid = [s for s in scores if not np.isnan(s)]
        drift_summary[provider] = {
            "mean_drift": float(np.mean(valid)) if valid else None,
            "max_drift": float(max(valid)) if valid else None,
            "n_high_drift": sum(1 for s in valid if s > 0.05),
        }
    results["strategy_drift"] = drift_summary

    # Plot strategy drift heatmap
    plot_strategy_drift_heatmap(
        drift_data,
        save_path=os.path.join(out_dir, "plots", "strategy_drift_heatmap.png"),
    )

    # --- Role adherence ---
    print("  Checking role adherence...")
    violations = check_role_adherence(history)
    results["role_adherence"] = {
        "n_violations": len(violations),
        "violations": violations[:20],  # cap at 20 for readability
    }
    if violations:
        print(f"    WARNING: {len(violations)} role adherence violations found!")
        for v in violations[:5]:
            print(f"      Round {v['round']}, {v['actor']}: '{v['term_found']}'")
    else:
        print("    No violations detected.")

    # --- Pattern validation (single run = fraction is 0 or 1) ---
    print("  Running pattern validation...")
    patterns = check_patterns([history])
    results["patterns"] = patterns
    for name, info in patterns.items():
        status = "PASS" if info["passed"] else "FAIL"
        print(f"    {name}: {status}")

    # Plot pattern checklist
    plot_pattern_validation_checklist(
        patterns,
        save_path=os.path.join(out_dir, "plots", "pattern_checklist.png"),
    )

    # --- Trace overlay (single run = just the trajectory line) ---
    plot_trace_overlay_multi(
        [history],
        METRICS,
        save_path=os.path.join(out_dir, "plots", "trajectory_overview.png"),
    )

    # Save results
    with open(os.path.join(out_dir, "diagnostic_results.json"), "w") as f:
        json.dump(results, f, indent=2, default=str)

    return results


def run_ablation_comparison(out_dir):
    """Compare ablation experiments against the baseline."""
    print(f"\n{'='*60}")
    print(f"  Ablation Comparison (baseline: {BASELINE_30})")
    print(f"{'='*60}")

    os.makedirs(out_dir, exist_ok=True)

    baseline_history = load_history(BASELINE_30)

    comparison = {"baseline": BASELINE_30, "ablations": {}}

    key_metrics = {
        "mean_gaming_gap": metric_mean_gaming_gap,
        "mean_true_capability": metric_mean_true_capability,
        "mean_eval_engineering": metric_mean_eval_engineering,
        "mean_safety_alignment": metric_mean_safety_alignment,
        "hhi": metric_hhi,
        "consumer_satisfaction": metric_consumer_satisfaction,
        "mean_benchmark_validity": metric_mean_benchmark_validity,
    }

    # Compute baseline final values
    baseline_finals = {}
    for metric_name, fn in key_metrics.items():
        series = extract_metric_series([baseline_history], fn)
        vals = series[0]
        baseline_finals[metric_name] = float(np.nanmean(vals[-5:]))  # avg last 5 rounds

    print(f"\n  Baseline final values (avg last 5 rounds):")
    for k, v in baseline_finals.items():
        print(f"    {k}: {v:.4f}")

    # Compare each ablation
    print(f"\n  Ablation effects (ablation - baseline):")
    print(f"  {'Ablation':<22} | {'gaming_gap':>11} | {'capability':>11} | {'eval_eng':>11} | {'safety':>11} | {'HHI':>11} | {'satisfaction':>12} | {'validity':>11}")
    print(f"  {'-'*22}-+-{'-'*11}-+-{'-'*11}-+-{'-'*11}-+-{'-'*11}-+-{'-'*11}-+-{'-'*12}-+-{'-'*11}")

    for abl_name, abl_id in ABLATIONS_30.items():
        abl_history = load_history(abl_id)
        abl_finals = {}
        for metric_name, fn in key_metrics.items():
            series = extract_metric_series([abl_history], fn)
            vals = series[0]
            abl_finals[metric_name] = float(np.nanmean(vals[-5:]))

        effects = {k: abl_finals[k] - baseline_finals[k] for k in key_metrics}
        comparison["ablations"][abl_name] = {
            "experiment_id": abl_id,
            "final_values": abl_finals,
            "effects": effects,
        }

        print(
            f"  {abl_name:<22} | {effects['mean_gaming_gap']:>+11.4f} | "
            f"{effects['mean_true_capability']:>+11.4f} | "
            f"{effects['mean_eval_engineering']:>+11.4f} | "
            f"{effects['mean_safety_alignment']:>+11.4f} | "
            f"{effects['hhi']:>+11.4f} | "
            f"{effects['consumer_satisfaction']:>+12.4f} | "
            f"{effects['mean_benchmark_validity']:>+11.4f}"
        )

    with open(os.path.join(out_dir, "ablation_comparison.json"), "w") as f:
        json.dump(comparison, f, indent=2)

    return comparison


def run_regulatory_comparison(out_dir):
    """Compare balanced vs US vs EU regulatory regimes (50-round experiments)."""
    print(f"\n{'='*60}")
    print(f"  Regulatory Regime Comparison (50-round experiments)")
    print(f"{'='*60}")

    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(os.path.join(out_dir, "plots"), exist_ok=True)

    histories = {}
    for eid in CANONICAL_50:
        histories[eid] = load_history(eid)

    key_metrics = {
        "mean_gaming_gap": metric_mean_gaming_gap,
        "mean_true_capability": metric_mean_true_capability,
        "mean_eval_engineering": metric_mean_eval_engineering,
        "mean_safety_alignment": metric_mean_safety_alignment,
        "hhi": metric_hhi,
        "consumer_satisfaction": metric_consumer_satisfaction,
        "incident_count": metric_incident_count,
    }

    # Print comparison table
    print(f"\n  Final values (avg last 5 rounds):")
    header = f"  {'Metric':<25}"
    for eid in CANONICAL_50:
        label = eid.split("_", 2)[-1][:20]
        header += f" | {label:>20}"
    print(header)
    print(f"  {'-'*25}" + ("-+-" + "-" * 20) * len(CANONICAL_50))

    comparison = {}
    for metric_name, fn in key_metrics.items():
        row = f"  {metric_name:<25}"
        comparison[metric_name] = {}
        for eid in CANONICAL_50:
            series = extract_metric_series([histories[eid]], fn)
            val = float(np.nanmean(series[0][-5:]))
            comparison[metric_name][eid] = val
            row += f" | {val:>20.4f}"
        print(row)

    # Plot comparative trajectories
    colors = {"balanced": "#2A9D8F", "us": "#E76F51", "eu": "#264653"}
    labels = {
        "exp_013_full_ecosystem_balanced": "Balanced",
        "exp_014_full_ecosystem_us": "US Light-Touch",
        "exp_015_full_ecosystem_eu": "EU Precautionary",
    }

    n_metrics = len(key_metrics)
    cols = 3
    rows = (n_metrics + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(3 * cols, 3 * rows))
    axes = np.atleast_1d(axes).flatten()

    for idx, (metric_name, fn) in enumerate(key_metrics.items()):
        ax = axes[idx]
        for eid in CANONICAL_50:
            series = extract_metric_series([histories[eid]], fn)
            regime = eid.split("_")[-1]  # balanced/us/eu
            color = colors.get(regime, "gray")
            label = labels.get(eid, eid)
            ax.plot(series[0], color=color, linewidth=1.8, label=label)
        ax.set_title(metric_name.replace("_", " ").title(), fontweight="bold")
        ax.set_xlabel("Round")
        ax.grid(True, alpha=0.3)
        if idx == 0:
            ax.legend()

    for idx in range(n_metrics, len(axes)):
        axes[idx].set_visible(False)

    fig.suptitle("Regulatory Regime Comparison (50 rounds)", fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(
        os.path.join(out_dir, "plots", "regulatory_comparison.png"),
        dpi=300,
        bbox_inches="tight",
    )
    plt.close(fig)

    with open(os.path.join(out_dir, "regulatory_comparison.json"), "w") as f:
        json.dump(comparison, f, indent=2)

    return comparison


def write_summary_report(all_results, out_dir):
    """Write a consolidated markdown report."""
    lines = [
        "# Simulation Diagnostics Report",
        "",
        f"Experiments analyzed: {len(all_results)}",
        "",
    ]

    # Pattern validation summary
    lines.extend(["## Pattern-Oriented Validation", ""])
    lines.append(f"| Pattern | " + " | ".join(
        r["experiment"].split("_", 2)[-1][:18] for r in all_results
    ) + " |")
    lines.append(f"|---|" + "|".join("---" for _ in all_results) + "|")

    pattern_names = list(all_results[0]["patterns"].keys())
    for pname in pattern_names:
        row = f"| {pname.replace('_', ' ').title()} |"
        for r in all_results:
            p = r["patterns"].get(pname, {})
            status = "PASS" if p.get("passed") else "FAIL"
            row += f" {status} |"
        lines.append(row)

    # Role adherence summary
    lines.extend(["", "## Role Adherence", ""])
    for r in all_results:
        n_viol = r["role_adherence"]["n_violations"]
        status = f"{n_viol} violations" if n_viol > 0 else "Clean"
        lines.append(f"- **{r['experiment']}**: {status}")

    # Strategy drift summary
    lines.extend(["", "## Strategy Drift (mean cosine distance)", ""])
    providers_seen = set()
    for r in all_results:
        providers_seen.update(r["strategy_drift"].keys())
    providers_sorted = sorted(providers_seen)

    lines.append(f"| Provider | " + " | ".join(
        r["experiment"].split("_", 2)[-1][:18] for r in all_results
    ) + " |")
    lines.append(f"|---|" + "|".join("---" for _ in all_results) + "|")

    for prov in providers_sorted:
        row = f"| {prov} |"
        for r in all_results:
            drift = r["strategy_drift"].get(prov, {})
            md = drift.get("mean_drift")
            row += f" {md:.4f} |" if md is not None else " N/A |"
        lines.append(row)

    report_path = os.path.join(out_dir, "summary_report.md")
    with open(report_path, "w") as f:
        f.write("\n".join(lines))
    print(f"\nSummary report written to {report_path}")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1. Run diagnostics on each experiment
    all_results = []
    with open(os.path.join(BASE_DIR, "index.json")) as f:
        index = json.load(f)

    for exp in index["experiments"]:
        eid = exp["id"]
        exp_out = os.path.join(OUTPUT_DIR, eid)
        result = run_single_experiment_diagnostics(eid, exp_out)
        all_results.append(result)

    # 2. Ablation comparison
    ablation_out = os.path.join(OUTPUT_DIR, "_ablation_comparison")
    run_ablation_comparison(ablation_out)

    # 3. Regulatory regime comparison
    reg_out = os.path.join(OUTPUT_DIR, "_regulatory_comparison")
    run_regulatory_comparison(reg_out)

    # 4. Summary report
    write_summary_report(all_results, OUTPUT_DIR)

    print(f"\n{'='*60}")
    print(f"  All diagnostics complete!")
    print(f"  Results in: {os.path.abspath(OUTPUT_DIR)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
