#!/usr/bin/env python3
"""
Simulation Diagnostics Runner

Orchestrates diagnostic runs (replications, sensitivity sweeps, CRN paired
comparisons) and invokes the analysis module.

Usage:
    python scripts/run_diagnostics.py replicate <exp_id> --n-seeds 10
    python scripts/run_diagnostics.py sensitivity <exp_id> --param rnd_efficiency --values 0.005,0.01,0.015 --n-seeds 3
    python scripts/run_diagnostics.py crn <exp_id_a> <exp_id_b> --n-seeds 5
    python scripts/run_diagnostics.py analyze <batch_name>
    python scripts/run_diagnostics.py --list-batches

Flags:
    --heuristic     Override llm_mode=False for cheap sweeps
    --api-delay N   Seconds to wait between LLM-mode runs (default: 0)
    --seeds 1,2,3   Explicit seed list (default: 1..n-seeds)
"""

import argparse
import copy
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_SCRIPT_DIR)
_SRC_DIR = os.path.join(_PROJECT_ROOT, "src")
_EXPERIMENTS_DIR = os.path.join(_PROJECT_ROOT, "output", "experiments")
_BATCHES_DIR = os.path.join(_EXPERIMENTS_DIR, "batches")
_DIAGNOSTICS_DIR = os.path.join(_PROJECT_ROOT, "output", "diagnostics")

sys.path.insert(0, _SRC_DIR)
sys.path.insert(0, _SCRIPT_DIR)


def _find_experiment_dir(query: str) -> str:
    """Find experiment directory by ID or prefix."""
    for base in [_EXPERIMENTS_DIR, os.path.join(_EXPERIMENTS_DIR, "_heuristic")]:
        if not os.path.isdir(base):
            continue
        for d in sorted(Path(base).iterdir()):
            if d.is_dir() and d.name.startswith(query):
                return str(d)
    raise FileNotFoundError(f"No experiment found matching: {query}")


def _load_config(exp_dir: str) -> dict:
    """Load config.json from an experiment directory."""
    config_path = os.path.join(exp_dir, "config.json")
    with open(config_path) as f:
        return json.load(f)


def _save_batch_manifest(batch_name: str, manifest: dict):
    """Save a batch manifest to the batches directory."""
    os.makedirs(_BATCHES_DIR, exist_ok=True)
    path = os.path.join(_BATCHES_DIR, f"{batch_name}.json")
    with open(path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Batch manifest saved: {path}")
    return path


def _run_single(config: dict, source_label: str, api_delay: float = 0) -> str:
    """Run a single simulation from a config dict.

    Returns the experiment ID.
    """
    from rerun_experiment import run_from_config

    config_copy = copy.deepcopy(config)
    _sim, exp_id = run_from_config(config_copy, source_label)

    if api_delay > 0:
        print(f"  Waiting {api_delay}s before next run...")
        time.sleep(api_delay)

    return exp_id


# ============================================================================
# Subcommands
# ============================================================================


def cmd_replicate(args):
    """Run N replications of a base experiment with different seeds."""
    exp_dir = _find_experiment_dir(args.exp_id)
    base_config = _load_config(exp_dir)
    base_exp_id = Path(exp_dir).name

    if args.heuristic:
        base_config["llm_mode"] = False

    seeds = (
        [int(s) for s in args.seeds.split(",")]
        if args.seeds
        else list(range(1, args.n_seeds + 1))
    )

    batch_name = f"replication_{base_exp_id}_N{len(seeds)}"
    print(f"\n=== Replication batch: {batch_name} ===")
    print(f"Base experiment: {base_exp_id}")
    print(f"Seeds: {seeds}")
    print(f"LLM mode: {base_config.get('llm_mode', False)}")
    print()

    experiment_ids = []
    for i, seed in enumerate(seeds):
        print(f"--- Replication {i + 1}/{len(seeds)} (seed={seed}) ---")
        config = copy.deepcopy(base_config)
        config["seed"] = seed
        exp_id = _run_single(config, f"diag_rep_{base_exp_id}", args.api_delay)
        experiment_ids.append(exp_id)
        print(f"  -> {exp_id}\n")

    manifest = {
        "batch_name": batch_name,
        "batch_type": "replication",
        "created_at": datetime.now().isoformat(),
        "base_config": base_exp_id,
        "experiments": experiment_ids,
        "seeds": seeds,
        "parameters_varied": {},
    }
    batch_path = _save_batch_manifest(batch_name, manifest)

    print(f"\n=== Replication batch complete: {len(experiment_ids)} runs ===")
    print(f"Analyze with: python scripts/run_diagnostics.py analyze {batch_name}")
    return batch_path


def cmd_sensitivity(args):
    """Run one-at-a-time sensitivity sweep."""
    exp_dir = _find_experiment_dir(args.exp_id)
    base_config = _load_config(exp_dir)
    base_exp_id = Path(exp_dir).name

    if args.heuristic:
        base_config["llm_mode"] = False

    param_name = args.param
    values = [float(v) for v in args.values.split(",")]
    seeds = (
        [int(s) for s in args.seeds.split(",")]
        if args.seeds
        else list(range(1, args.n_seeds + 1))
    )

    batch_name = f"sensitivity_{param_name}_{base_exp_id}"
    print(f"\n=== Sensitivity sweep: {batch_name} ===")
    print(f"Parameter: {param_name}")
    print(f"Values: {values}")
    print(f"Seeds per value: {seeds}")
    print()

    all_experiment_ids = []
    param_sweep = {}

    for value in values:
        value_str = str(value)
        param_sweep[value_str] = []
        for seed in seeds:
            print(f"--- {param_name}={value}, seed={seed} ---")
            config = copy.deepcopy(base_config)
            config["seed"] = seed
            config[param_name] = value
            exp_id = _run_single(
                config, f"diag_sens_{param_name}_{base_exp_id}", args.api_delay
            )
            param_sweep[value_str].append(exp_id)
            all_experiment_ids.append(exp_id)
            print(f"  -> {exp_id}\n")

    manifest = {
        "batch_name": batch_name,
        "batch_type": "sensitivity",
        "created_at": datetime.now().isoformat(),
        "base_config": base_exp_id,
        "experiments": all_experiment_ids,
        "seeds": seeds,
        "parameters_varied": {param_name: param_sweep},
    }
    batch_path = _save_batch_manifest(batch_name, manifest)

    print(f"\n=== Sensitivity sweep complete: {len(all_experiment_ids)} runs ===")
    print(f"Analyze with: python scripts/run_diagnostics.py analyze {batch_name}")
    return batch_path


def cmd_crn(args):
    """Run CRN-paired replications of two conditions."""
    exp_dir_a = _find_experiment_dir(args.exp_id_a)
    exp_dir_b = _find_experiment_dir(args.exp_id_b)
    config_a = _load_config(exp_dir_a)
    config_b = _load_config(exp_dir_b)
    base_a = Path(exp_dir_a).name
    base_b = Path(exp_dir_b).name

    if args.heuristic:
        config_a["llm_mode"] = False
        config_b["llm_mode"] = False

    seeds = (
        [int(s) for s in args.seeds.split(",")]
        if args.seeds
        else list(range(1, args.n_seeds + 1))
    )

    batch_name = f"crn_{base_a}_vs_{base_b}_N{len(seeds)}"
    print(f"\n=== CRN paired comparison: {batch_name} ===")
    print(f"Condition A: {base_a}")
    print(f"Condition B: {base_b}")
    print(f"Seeds: {seeds}")
    print()

    ids_a, ids_b = [], []
    seed_pairs = []

    for i, seed in enumerate(seeds):
        print(f"--- Pair {i + 1}/{len(seeds)} (seed={seed}) ---")

        ca = copy.deepcopy(config_a)
        ca["seed"] = seed
        eid_a = _run_single(ca, f"diag_crn_a_{base_a}", args.api_delay)
        ids_a.append(eid_a)
        print(f"  A -> {eid_a}")

        cb = copy.deepcopy(config_b)
        cb["seed"] = seed
        eid_b = _run_single(cb, f"diag_crn_b_{base_b}", args.api_delay)
        ids_b.append(eid_b)
        print(f"  B -> {eid_b}\n")

        seed_pairs.append([seed, eid_a, eid_b])

    manifest = {
        "batch_name": batch_name,
        "batch_type": "crn_paired",
        "created_at": datetime.now().isoformat(),
        "condition_a": {"base": base_a, "experiments": ids_a},
        "condition_b": {"base": base_b, "experiments": ids_b},
        "experiments": ids_a + ids_b,
        "seeds": seeds,
        "seed_pairs": seed_pairs,
        "parameters_varied": {},
    }
    batch_path = _save_batch_manifest(batch_name, manifest)

    print(f"\n=== CRN batch complete: {len(seed_pairs)} pairs ===")
    print(f"Analyze with: python scripts/run_diagnostics.py analyze {batch_name}")
    return batch_path


def cmd_analyze(args):
    """Run diagnostic analysis on a completed batch."""
    import matplotlib
    matplotlib.use("Agg")

    from diagnostics import (
        analyze_batch,
        load_batch_histories,
        load_batch_manifest,
        aggregate_replications,
        crn_paired_difference,
        detect_strategy_drift_all_providers,
        metric_mean_true_capability,
        metric_mean_eval_engineering,
        metric_mean_safety_alignment,
        metric_mean_score,
        metric_mean_gaming_gap,
        metric_hhi,
        metric_consumer_satisfaction,
        metric_mean_benchmark_validity,
    )
    from diagnostic_plots import (
        plot_trace_overlay_multi,
        plot_strategy_drift_heatmap,
        plot_pattern_validation_checklist,
        plot_crn_paired_difference,
    )

    batch_path = os.path.join(_BATCHES_DIR, f"{args.batch_name}.json")
    if not os.path.exists(batch_path):
        print(f"Batch manifest not found: {batch_path}")
        sys.exit(1)

    output_dir = os.path.join(_DIAGNOSTICS_DIR, args.batch_name)
    print(f"\n=== Analyzing batch: {args.batch_name} ===")
    print(f"Output: {output_dir}\n")

    # Run core analysis
    results = analyze_batch(batch_path, _EXPERIMENTS_DIR, output_dir)

    print(f"Replications: {results['n_replications']}")
    print()

    # Print pattern results
    print("Pattern Validation:")
    for name, info in results.get("patterns", {}).items():
        status = "PASS" if info["passed"] else "FAIL"
        print(f"  {name}: {status} ({info['fraction']:.0%})")
    print()

    # Print coherence summary
    violations = results.get("coherence", {}).get("role_adherence_violations", [])
    print(f"Role adherence violations: {len(violations)}")
    print()

    # Generate plots
    manifest = load_batch_manifest(batch_path)
    histories = load_batch_histories(batch_path, _EXPERIMENTS_DIR)
    plots_dir = os.path.join(output_dir, "plots")

    # Trace overlay multi-panel
    metrics = {
        "Mean True Capability": (metric_mean_true_capability, "Capability"),
        "Mean Eval Engineering": (metric_mean_eval_engineering, "Fraction"),
        "Mean Score": (metric_mean_score, "Score"),
        "Mean Gaming Gap": (metric_mean_gaming_gap, "Gap"),
        "HHI (Market Concentration)": (metric_hhi, "HHI"),
        "Mean Benchmark Validity": (metric_mean_benchmark_validity, "Validity"),
    }
    plot_trace_overlay_multi(
        histories, metrics, save_path=os.path.join(plots_dir, "trace_overlay_multi.png")
    )
    print(f"Saved: trace_overlay_multi.png")

    # Strategy drift heatmap (from first replication)
    if histories:
        drift = detect_strategy_drift_all_providers(histories[0])
        plot_strategy_drift_heatmap(
            drift, save_path=os.path.join(plots_dir, "strategy_drift_heatmap.png")
        )
        print(f"Saved: strategy_drift_heatmap.png")

    # Pattern checklist
    plot_pattern_validation_checklist(
        results["patterns"],
        save_path=os.path.join(plots_dir, "pattern_checklist.png"),
    )
    print(f"Saved: pattern_checklist.png")

    # CRN paired difference (if applicable)
    if manifest.get("batch_type") == "crn_paired":
        ids_a = manifest["condition_a"]["experiments"]
        ids_b = manifest["condition_b"]["experiments"]
        from diagnostics import load_experiment_history

        hist_a = [load_experiment_history(_EXPERIMENTS_DIR, eid) for eid in ids_a]
        hist_b = [load_experiment_history(_EXPERIMENTS_DIR, eid) for eid in ids_b]

        for metric_name, metric_fn in [
            ("Mean Gaming Gap", metric_mean_gaming_gap),
            ("Mean True Capability", metric_mean_true_capability),
            ("HHI", metric_hhi),
        ]:
            paired = crn_paired_difference(hist_a, hist_b, metric_fn)
            fname = f"crn_{metric_name.lower().replace(' ', '_')}.png"
            plot_crn_paired_difference(
                paired,
                metric_name,
                manifest["condition_a"]["base"],
                manifest["condition_b"]["base"],
                save_path=os.path.join(plots_dir, fname),
            )
            print(f"Saved: {fname}")

    print(f"\nDiagnostic report: {os.path.join(output_dir, 'diagnostic_report.md')}")
    print(f"All outputs in: {output_dir}")


def cmd_list_batches(args):
    """List all batch manifests."""
    if not os.path.isdir(_BATCHES_DIR):
        print("No batches directory found.")
        return

    batches = sorted(Path(_BATCHES_DIR).glob("*.json"))
    if not batches:
        print("No batch manifests found.")
        return

    print(f"\n{'Batch Name':<50} {'Type':<15} {'Runs':<6} {'Created'}")
    print("-" * 90)
    for bp in batches:
        with open(bp) as f:
            m = json.load(f)
        print(
            f"{m.get('batch_name', bp.stem):<50} "
            f"{m.get('batch_type', '?'):<15} "
            f"{len(m.get('experiments', [])):<6} "
            f"{m.get('created_at', '?')[:19]}"
        )


# ============================================================================
# CLI
# ============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Simulation Diagnostics Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="command")

    # replicate
    p_rep = sub.add_parser("replicate", help="Run N replications with different seeds")
    p_rep.add_argument("exp_id", help="Base experiment ID or prefix")
    p_rep.add_argument("--n-seeds", type=int, default=5)
    p_rep.add_argument("--seeds", help="Comma-separated seed list")
    p_rep.add_argument("--heuristic", action="store_true")
    p_rep.add_argument("--api-delay", type=float, default=0)

    # sensitivity
    p_sens = sub.add_parser("sensitivity", help="One-at-a-time sensitivity sweep")
    p_sens.add_argument("exp_id", help="Base experiment ID or prefix")
    p_sens.add_argument("--param", required=True, help="Parameter name to sweep")
    p_sens.add_argument("--values", required=True, help="Comma-separated values")
    p_sens.add_argument("--n-seeds", type=int, default=3)
    p_sens.add_argument("--seeds", help="Comma-separated seed list")
    p_sens.add_argument("--heuristic", action="store_true")
    p_sens.add_argument("--api-delay", type=float, default=0)

    # crn
    p_crn = sub.add_parser("crn", help="CRN-paired comparison of two conditions")
    p_crn.add_argument("exp_id_a", help="Condition A experiment ID")
    p_crn.add_argument("exp_id_b", help="Condition B experiment ID")
    p_crn.add_argument("--n-seeds", type=int, default=5)
    p_crn.add_argument("--seeds", help="Comma-separated seed list")
    p_crn.add_argument("--heuristic", action="store_true")
    p_crn.add_argument("--api-delay", type=float, default=0)

    # analyze
    p_ana = sub.add_parser("analyze", help="Analyze a completed batch")
    p_ana.add_argument("batch_name", help="Batch name (without .json)")

    # list-batches
    sub.add_parser("list-batches", help="List all batch manifests")

    args = parser.parse_args()

    if args.command == "replicate":
        cmd_replicate(args)
    elif args.command == "sensitivity":
        cmd_sensitivity(args)
    elif args.command == "crn":
        cmd_crn(args)
    elif args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "list-batches":
        cmd_list_batches(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
