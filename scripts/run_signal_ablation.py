"""
Consumer Signal Ablation Runner
================================
Runs 3 conditions to test how prompt framing affects provider orientation behavior:

1. control:    Original prompt + full consumer signal (baseline — replicates old ratchet)
2. reframed:   Reframed orientation language + full consumer signal (tests: does reframing alone help?)
3. no_signal:  Reframed orientation language + no consumer signal (tests: does removing signal add differentiation?)

All conditions: 10 rounds, seed 1, LLM mode, adjustable orientation, balanced policy, dev output.
Output goes to sandbox/experiments/ with batch label "signal_ablation".

Usage:
    python scripts/run_signal_ablation.py                    # run all 3
    python scripts/run_signal_ablation.py --condition control  # run one
    python scripts/run_signal_ablation.py --rounds 5          # quick smoke test
"""
import subprocess
import sys
import os
import argparse

CONDITIONS = ["signal_ablation_control", "signal_ablation_reframed", "signal_ablation_no_signal"]

parser = argparse.ArgumentParser(description="Run consumer signal ablation experiments")
parser.add_argument("--condition", choices=CONDITIONS, default=None,
                    help="Run a single condition (default: run all 3)")
parser.add_argument("--rounds", type=int, default=10,
                    help="Number of rounds per condition (default: 10)")
parser.add_argument("--seed", type=int, default=1,
                    help="Random seed (default: 1)")
parser.add_argument("--provider", default="anthropic",
                    help="LLM provider (default: anthropic)")
args = parser.parse_args()

conditions = [args.condition] if args.condition else CONDITIONS

scripts_dir = os.path.dirname(os.path.abspath(__file__))

for i, condition in enumerate(conditions):
    print(f"\n{'='*60}")
    print(f"  Ablation {i+1}/{len(conditions)}: {condition}")
    print(f"  Rounds: {args.rounds}, Seed: {args.seed}, Provider: {args.provider}")
    print(f"{'='*60}\n")

    cmd = [
        sys.executable, os.path.join(scripts_dir, "run_experiment.py"),
        "--condition", condition,
        "--mode", "llm",
        "--provider", args.provider,
        "--rounds", str(args.rounds),
        "--seed", str(args.seed),
        "--batch", "signal_ablation",
    ]

    result = subprocess.run(cmd, cwd=os.path.dirname(scripts_dir))

    if result.returncode != 0:
        print(f"\nERROR: {condition} failed with return code {result.returncode}")
        print("Stopping ablation run.")
        sys.exit(1)

    print(f"\nCompleted: {condition}")

print(f"\n{'='*60}")
print(f"  All {len(conditions)} ablation conditions complete.")
print(f"  Output: sandbox/experiments/signal_ablation/")
print(f"{'='*60}")
