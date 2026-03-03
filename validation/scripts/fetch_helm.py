"""
fetch_helm.py — Download and parse HELM run results from the Stanford CRFM CDN.

HELM releases data as JSON files at:
  https://storage.googleapis.com/crfm-helm-public/benchmark_output/runs/<version>/

We target specific scenarios (mmlu, math, humaneval) and extract
per-model accuracy / pass@1 scores.

Writes:  validation/data/raw/helm/<scenario>.json
         Each file: list of {model, provider_raw, scenario, score, run_date} dicts

Usage:
    python validation/scripts/fetch_helm.py [--version v0.4.0] [--scenarios mmlu math humaneval]
"""

import argparse
import json
import re
import time
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# HELM CDN configuration
# ---------------------------------------------------------------------------
HELM_CDN = "https://storage.googleapis.com/crfm-helm-public/benchmark_output/runs"

# Stable release that has broad coverage; override with --version
DEFAULT_VERSION = "v0.4.0"

# Scenario → expected metric key in HELM JSON
SCENARIO_METRICS = {
    "mmlu": "quasi_exact_match",
    "math": "quasi_exact_match",
    "humaneval": "pass@1",
}

# Approximate run dates per HELM release (used when individual run_date missing)
RELEASE_DATES = {
    "v0.2.0": "2022-11-01",
    "v0.2.4": "2023-02-01",
    "v0.3.0": "2023-06-01",
    "v0.4.0": "2023-11-01",
}

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw" / "helm"


def fetch_index(version: str) -> dict:
    """Fetch the top-level groups.json (or runs.json) index from HELM CDN."""
    url = f"{HELM_CDN}/{version}/groups.json"
    resp = requests.get(url, timeout=60)
    if resp.status_code == 404:
        # Older format
        url = f"{HELM_CDN}/{version}/summary.json"
        resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    return resp.json()


def extract_runs_for_scenario(index: dict, scenario: str, version: str) -> list[dict]:
    """
    Parse HELM groups index to find run entries for a given scenario prefix,
    then pull per-model scores.
    """
    rows = []
    run_date = RELEASE_DATES.get(version, "")
    metric_key = SCENARIO_METRICS.get(scenario, "quasi_exact_match")

    # groups.json schema: list of group objects with 'name' and 'stats'
    groups = index if isinstance(index, list) else index.get("groups", [])

    for group in groups:
        group_name = group.get("name", "")
        if not group_name.lower().startswith(scenario.lower()):
            continue

        for stat in group.get("stats", []):
            # stat example: {"model": "openai/gpt-4", "mean": 0.864, ...}
            model = stat.get("model", stat.get("name", ""))
            mean = stat.get("mean")
            if model and mean is not None:
                try:
                    score = float(mean)
                except (TypeError, ValueError):
                    continue
                rows.append({
                    "scenario": scenario,
                    "model": model,
                    "provider_raw": model.split("/")[0] if "/" in model else model,
                    "score": score,
                    "metric": metric_key,
                    "run_date": run_date,
                    "helm_version": version,
                    "source": "helm",
                })

    return rows


def fetch_scenario_direct(scenario: str, version: str) -> list[dict]:
    """
    Attempt to fetch a per-scenario summary JSON directly from the CDN,
    as a fallback when the groups index doesn't contain the scenario.
    """
    rows = []
    run_date = RELEASE_DATES.get(version, "")
    metric_key = SCENARIO_METRICS.get(scenario, "quasi_exact_match")

    url = f"{HELM_CDN}/{version}/scenarios/{scenario}.json"
    resp = requests.get(url, timeout=60)
    if resp.status_code != 200:
        return rows

    data = resp.json()
    # schema varies; try common patterns
    for entry in data if isinstance(data, list) else data.get("results", []):
        model = entry.get("model", entry.get("name", ""))
        score = entry.get(metric_key, entry.get("score", entry.get("mean")))
        if model and score is not None:
            try:
                rows.append({
                    "scenario": scenario,
                    "model": model,
                    "provider_raw": model.split("/")[0] if "/" in model else model,
                    "score": float(score),
                    "metric": metric_key,
                    "run_date": run_date,
                    "helm_version": version,
                    "source": "helm",
                })
            except (TypeError, ValueError):
                pass

    return rows


def main(version: str, scenarios: list[str]) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Fetching HELM index for version {version} ...")
    try:
        index = fetch_index(version)
    except requests.HTTPError as exc:
        print(f"[ERROR] Could not fetch HELM index: {exc}")
        index = {}

    for scenario in scenarios:
        print(f"  Processing scenario: {scenario}")
        rows = extract_runs_for_scenario(index, scenario, version)

        if not rows:
            print(f"    Not found in index, trying direct fetch ...")
            rows = fetch_scenario_direct(scenario, version)
            time.sleep(0.5)

        out_path = RAW_DIR / f"{scenario}.json"
        out_path.write_text(json.dumps(rows, indent=2))
        print(f"    -> {len(rows)} rows written to {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default=DEFAULT_VERSION)
    parser.add_argument(
        "--scenarios",
        nargs="+",
        default=list(SCENARIO_METRICS.keys()),
    )
    args = parser.parse_args()
    main(args.version, args.scenarios)
