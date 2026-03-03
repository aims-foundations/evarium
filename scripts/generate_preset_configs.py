#!/usr/bin/env python3
"""
Generate US and EU ablation configs from existing balanced configs.

Clones each balanced ablation config.json and swaps the regulatory-preset
fields (policymaker_configs, startup params) to produce US and EU variants.

Creates new experiment directories in output/experiments/ so that
run_diagnostics.py can find them by prefix.

Usage:
    python scripts/generate_preset_configs.py            # generate all
    python scripts/generate_preset_configs.py --dry-run   # preview only
"""

import json
import os
import sys
import copy

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPERIMENTS_DIR = os.path.join(PROJECT_ROOT, "output", "experiments")

# Balanced ablation exp_id -> condition name
BALANCED_ABLATIONS = {
    "exp_004_ablation_no_media_balanced": "ablation_no_media",
    "exp_005_ablation_no_incidents_balanced": "ablation_no_incidents",
    "exp_006_ablation_no_startups_balanced": "ablation_no_startups",
    "exp_007_ablation_no_opencore_balanced": "ablation_no_opencore",
    "exp_008_ablation_single_benchmark_balanced": "ablation_single_benchmark",
    "exp_009_ablation_no_funders_balanced": "ablation_no_funders",
    "exp_010_ablation_no_benchmark_evolution_balanced": "ablation_no_bench_evolution",
    "exp_012_ablation_eval_as_company_balanced": "ablation_eval_as_company",
}

# Preset overrides (derived from comparing exp_011 balanced vs exp_001 US vs exp_002 EU)
PRESETS = {
    "us": {
        "policymaker_configs": [
            {
                "name": "Regulator",
                "philosophy": "us_light_touch",
                "policy_objectives": ["safety", "innovation", "free market"],
            }
        ],
        "startup_entry_probability": 0.15,
        "startup_entry_cap": 4,
    },
    "eu": {
        "policymaker_configs": [
            {
                "name": "Regulator",
                "philosophy": "eu_precautionary",
                "policy_objectives": ["safety", "fairness", "consumer_protection"],
            }
        ],
        "startup_entry_probability": 0.04,
        "startup_entry_cap": 2,
    },
}

# Ablations where startup params are part of the ablation itself (keep at 0)
STARTUP_ABLATIONS = {"ablation_no_startups"}


def generate_configs(dry_run=False):
    created = []
    skipped = []

    for balanced_dir, condition_name in BALANCED_ABLATIONS.items():
        balanced_path = os.path.join(EXPERIMENTS_DIR, balanced_dir, "config.json")
        if not os.path.exists(balanced_path):
            print(f"WARNING: Missing {balanced_path}, skipping")
            skipped.append(balanced_dir)
            continue

        with open(balanced_path) as f:
            balanced_config = json.load(f)

        for preset_name, preset_overrides in PRESETS.items():
            new_dir_name = f"gen_{condition_name}_{preset_name}"
            new_dir = os.path.join(EXPERIMENTS_DIR, new_dir_name)
            new_config_path = os.path.join(new_dir, "config.json")

            if os.path.exists(new_config_path):
                print(f"  EXISTS: {new_dir_name} (skipping)")
                skipped.append(new_dir_name)
                continue

            # Clone config
            config = copy.deepcopy(balanced_config)

            # Apply preset overrides
            config["policymaker_configs"] = copy.deepcopy(
                preset_overrides["policymaker_configs"]
            )

            # Apply startup params unless this ablation disables startups
            if condition_name not in STARTUP_ABLATIONS:
                config["startup_entry_probability"] = preset_overrides[
                    "startup_entry_probability"
                ]
                config["startup_entry_cap"] = preset_overrides["startup_entry_cap"]

            if dry_run:
                print(f"  WOULD CREATE: {new_dir_name}")
                print(f"    from: {balanced_dir}")
                print(f"    preset: {preset_name}")
                print(
                    f"    policymaker: {config['policymaker_configs'][0]['philosophy']}"
                )
                print(
                    f"    startup_entry_probability: {config.get('startup_entry_probability')}"
                )
                print()
            else:
                os.makedirs(new_dir, exist_ok=True)
                with open(new_config_path, "w") as f:
                    json.dump(config, f, indent=2)
                print(f"  CREATED: {new_dir_name}")
                created.append(new_dir_name)

    print()
    print(f"Created: {len(created)}")
    print(f"Skipped: {len(skipped)}")
    return created


def main():
    dry_run = "--dry-run" in sys.argv
    if dry_run:
        print("=== DRY RUN ===\n")
    else:
        print("=== Generating US/EU ablation configs ===\n")

    created = generate_configs(dry_run=dry_run)

    if not dry_run and created:
        print()
        print("Generated configs can be used with run_diagnostics.py:")
        print("  python scripts/run_diagnostics.py replicate gen_ablation_no_media_us --n-seeds 30 --heuristic")


if __name__ == "__main__":
    main()
