#!/usr/bin/env python3
"""
Orchestrator for running experiment conditions across presets, seeds, and models.

Edit the configuration section below to control what runs. Comment out
conditions you don't need. Change SEEDS, MODE, PROVIDER as needed for
different phases.

Usage:
    # Phase 1: core runs (single seed, all conditions)
    python scripts/run_all.py

    # Phase 5: heuristic baseline (edit MODE="heuristic", SEEDS=range(1,31))
    python scripts/run_all.py

    # Dry run (print commands without executing):
    python scripts/run_all.py --dry-run

    # Resume after failure (skips runs whose output dir already exists):
    python scripts/run_all.py --skip-existing

    # Custom batch label:
    python scripts/run_all.py --batch my_experiment
"""
import argparse
import os
import subprocess
import sys
import time

# ============================================================
#  CONFIGURATION — edit this section
# ============================================================

# Explicit list of (condition, preset) pairs to run.
# These don't form a clean cross-product, so we list them directly.
JOBS_SPEC = [
    ("full_ecosystem", "balanced"),
    # ("full_ecosystem", "us"),
    # ("full_ecosystem", "eu"),
    # ("bm_orientation_adjustable", "balanced"),
    # ("market_expansion", "balanced"),
    # ("misaligned_benchmarks", "balanced"),
]

# Phase 1: single seed. Phase 2: range(1, 31). Phase 5: range(1, 31)
SEEDS = [1]

# "llm" for LLM-driven runs, "heuristic" for Phase 5
MODE = "llm"

# LLM provider: "anthropic", "openai", "ollama", "gemini"
# For Qwen via vLLM: set PROVIDER="openai" and configure env vars
# (OPENAI_BASE_URL=http://localhost:8000/v1, OPENAI_API_KEY=dummy)
PROVIDER = "anthropic"

ROUNDS = 40

# Set True for local dev/test runs (output -> sandbox/experiments/)
DEV = True

# ============================================================
#  END CONFIGURATION
# ============================================================

def build_jobs(jobs_spec, seeds):
    """Build flat list of (condition, preset, seed) tuples from explicit spec."""
    jobs = []
    for condition, preset in jobs_spec:
        for seed in seeds:
            jobs.append((condition, preset, seed))
    return jobs


def build_command(condition, preset, seed, mode, provider, rounds, dev,
                  batch=None):
    """Build the run_experiment.py command for a single job."""
    cmd = [
        sys.executable, "scripts/run_experiment.py",
        "--condition", condition,
        "--policy", preset,
        "--mode", mode,
        "--seed", str(seed),
        "--rounds", str(rounds),
    ]
    if mode == "llm":
        cmd += ["--provider", provider]
    if dev:
        cmd.append("--dev")
    if batch:
        cmd += ["--batch", batch]
    return cmd


def expected_output_dir(condition, preset, seed, mode, provider, dev):
    """Predict the output directory for a job (for --skip-existing)."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    condition_name = f"{condition}_{preset}"
    seed_label = f"seed_{seed}"

    if dev:
        # Dev mode uses timestamped dirs — can't predict, so never skip
        return None

    if mode == "heuristic":
        return os.path.join(project_root, "hf_data", "heuristic_baseline",
                            condition_name, "seeds", seed_label)
    else:
        model_slug = {
            "anthropic": "claude-sonnet-4-6",
            "openai": "qwen-235b",
            "gemini": "gemini-flash",
            "ollama": "ollama",
        }.get(provider, provider)
        return os.path.join(project_root, "hf_data", "llm_core",
                            model_slug, condition_name, "seeds", seed_label)


def run_jobs(jobs, mode, provider, rounds, dev, dry_run=False,
             skip_existing=False, batch=None):
    """Execute all jobs sequentially."""
    total = len(jobs)
    completed = 0
    skipped = 0
    failed = []

    print("=" * 70)
    print(f"  Run All: {total} jobs")
    print(f"  Mode: {mode} | Provider: {provider} | Rounds: {rounds}")
    print(f"  Jobs: {len(JOBS_SPEC)} specs x {len(SEEDS)} seeds")
    if dev:
        print("  [DEV MODE]")
    print("=" * 70)
    print()

    start_time = time.time()

    for i, (condition, preset, seed) in enumerate(jobs):
        label = f"[{i+1}/{total}] {condition} / {preset} / seed_{seed}"

        # Skip existing
        if skip_existing and not dev:
            out_dir = expected_output_dir(condition, preset, seed, mode, provider, dev)
            if out_dir and os.path.exists(os.path.join(out_dir, "rounds.jsonl")):
                print(f"  SKIP {label} (already exists)")
                skipped += 1
                continue

        cmd = build_command(condition, preset, seed, mode, provider, rounds, dev, batch=batch)

        if dry_run:
            print(f"  {label}")
            print(f"    {' '.join(cmd)}")
            print()
            continue

        print(f"  START {label} ({time.strftime('%H:%M:%S')})")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5400)
            if result.returncode == 0:
                completed += 1
                print(f"  DONE  {label}")
            else:
                failed.append((condition, preset, seed, result.stderr[-500:]))
                print(f"  FAIL  {label}")
                # Print last few lines of stderr for diagnosis
                for line in result.stderr.strip().split("\n")[-5:]:
                    print(f"    {line}")
        except subprocess.TimeoutExpired:
            failed.append((condition, preset, seed, "TIMEOUT"))
            print(f"  TIMEOUT {label}")
        except KeyboardInterrupt:
            print(f"\n  Interrupted at {label}")
            break
        print()

    elapsed = time.time() - start_time

    if not dry_run:
        print()
        print("=" * 70)
        print(f"  FINISHED in {elapsed/60:.1f} min")
        print(f"  Completed: {completed} | Skipped: {skipped} | Failed: {len(failed)}")
        if failed:
            print()
            print("  Failed jobs:")
            for cond, preset, seed, err in failed:
                print(f"    {cond} / {preset} / seed_{seed}: {err[:100]}")
        print("=" * 70)



def main():
    parser = argparse.ArgumentParser(description="Run all experiment conditions.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print commands without executing")
    parser.add_argument("--skip-existing", action="store_true",
                        help="Skip jobs whose output directory already has rounds.jsonl")
    parser.add_argument("--batch", type=str, default=None,
                        help="Batch label for grouping dev output (default: auto-generated timestamp)")
    args = parser.parse_args()

    jobs = build_jobs(JOBS_SPEC, SEEDS)

    # Auto-generate batch label if not provided (dev mode only)
    batch = args.batch
    if DEV and not batch:
        from datetime import datetime
        batch = f"batch_{MODE}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    run_jobs(jobs, MODE, PROVIDER, ROUNDS, DEV,
             dry_run=args.dry_run, skip_existing=args.skip_existing, batch=batch)

    # Generate aggregate plots if batch dir exists and not dry-run
    if not args.dry_run and batch and DEV:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        batch_dir = os.path.join(project_root, "sandbox", "experiments", batch)
        if os.path.isdir(batch_dir):
            print()
            print("Generating aggregate plots...")
            try:
                sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
                from plot_batch import load_batch, fig1_gap_presets, fig2_ablation_bars
                from plot_batch import fig3_orientation_deepdive, fig4_regulatory_deepdive
                from plot_batch import fig5_incident_validation
                runs = load_batch(batch_dir)
                plot_dir = os.path.join(batch_dir, "_plots")
                os.makedirs(plot_dir, exist_ok=True)
                fig1_gap_presets(runs, plot_dir)
                fig2_ablation_bars(runs, plot_dir)
                fig3_orientation_deepdive(runs, plot_dir)
                fig4_regulatory_deepdive(runs, plot_dir)
                fig5_incident_validation(runs, plot_dir)
            except Exception as e:
                print(f"  Plot generation failed: {e}")


if __name__ == "__main__":
    main()
