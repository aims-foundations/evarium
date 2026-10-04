"""
fetch_helm.py — Download and parse HELM run results from the Stanford CRFM CDN.

Actual URL structure (verified):
  https://storage.googleapis.com/crfm-helm-public/benchmark_output/releases/<version>/groups/<scenario>.json

Each groups/<scenario>.json is a list of table objects.  Each table has:
  - header: list of {value, description, ...}  (column names)
  - rows:   list of rows, each row is a list of {value, ...} cells
The first column is "Model/adapter", the second is the primary metric (e.g. "EM").

Writes:  validation/data/raw/helm/<scenario>.json
         Each file: list of {model, provider_raw, scenario, score, metric, run_date, helm_version} dicts

Usage:
    python validation/scripts/fetch_helm.py [--version v0.4.0] [--scenarios mmlu math]
"""

import argparse
import json
import time
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# HELM CDN configuration
# ---------------------------------------------------------------------------
HELM_BASE = "https://storage.googleapis.com/crfm-helm-public/benchmark_output/releases"

# Verified working version
DEFAULT_VERSION = "v0.4.0"

# Map our scenario names → HELM group file names (without .json)
# Verified from releases/v0.4.0/groups.json index hrefs
SCENARIO_GROUPS = {
    "mmlu":      "mmlu",
    "math":      "math_regular",   # "MATH" benchmark group
    "gsm":       "gsm",            # GSM8K grade-school math (easier, more models)
    "humaneval": "code_humaneval", # HumanEval coding benchmark
    "reasoning": "reasoning",      # General reasoning
}

# Primary metric column name per scenario (matches HELM table headers)
SCENARIO_METRIC = {
    "mmlu":      "EM",
    "math":      "EM",
    "gsm":       "EM",
    "humaneval": "pass@1",
    "reasoning": "EM",
}

# Approximate release dates (used as run_date since HELM doesn't tag individual rows)
RELEASE_DATES = {
    "v0.2.0": "2022-11-01",
    "v0.2.4": "2023-02-01",
    "v0.3.0": "2023-06-01",
    "v0.4.0": "2023-11-01",
}

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw" / "helm"


def fetch_group(version: str, group_name: str) -> list[dict]:
    """Fetch the groups/<group_name>.json file from the HELM CDN."""
    url = f"{HELM_BASE}/{version}/groups/{group_name}.json"
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    return resp.json()


def extract_scores(tables: list[dict], scenario: str, version: str) -> list[dict]:
    """
    Parse HELM group JSON (list of table objects) and extract per-model scores.

    Table schema:
      {
        "title": "...",
        "header": [{"value": "Model/adapter"}, {"value": "EM"}, ...],
        "rows":   [[{"value": "GPT-4"}, {"value": 0.864}, ...], ...]
      }
    """
    rows = []
    run_date = RELEASE_DATES.get(version, "")
    target_metric = SCENARIO_METRIC.get(scenario, "EM")

    for table in tables:
        header = table.get("header", [])
        if not header:
            continue

        # Find column indices
        col_names = [h.get("value", "") for h in header]
        model_col = 0  # always "Model/adapter"

        # Find the target metric column; fall back to the second column
        metric_col = 1
        for i, name in enumerate(col_names):
            if name == target_metric:
                metric_col = i
                break

        actual_metric = col_names[metric_col] if metric_col < len(col_names) else target_metric

        for data_row in table.get("rows", []):
            if len(data_row) <= metric_col:
                continue

            model_cell = data_row[model_col]
            score_cell = data_row[metric_col]

            model = model_cell.get("value", "")
            score_raw = score_cell.get("value")

            if not model or score_raw is None:
                continue
            try:
                score = float(score_raw)
            except (TypeError, ValueError):
                continue

            # Derive provider from model name
            # HELM model names look like "openai/gpt-4" or "anthropic/claude-2"
            if "/" in str(model):
                provider_raw = str(model).split("/")[0]
            else:
                provider_raw = str(model)

            rows.append({
                "scenario": scenario,
                "model": str(model),
                "provider_raw": provider_raw,
                "score": round(score, 6),
                "metric": actual_metric,
                "run_date": run_date,
                "helm_version": version,
                "source": "helm",
            })

    return rows


def main(version: str, scenarios: list[str]) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    for scenario in scenarios:
        group_name = SCENARIO_GROUPS.get(scenario, scenario)
        url_display = f"{HELM_BASE}/{version}/groups/{group_name}.json"
        print(f"Fetching HELM {scenario} (group: {group_name}) ...")
        print(f"  URL: {url_display}")

        try:
            tables = fetch_group(version, group_name)
        except requests.HTTPError as exc:
            print(f"  [ERROR] HTTP {exc.response.status_code}: {exc}")
            tables = []
        except Exception as exc:
            print(f"  [ERROR] {exc}")
            tables = []

        rows = extract_scores(tables, scenario, version) if tables else []

        out_path = RAW_DIR / f"{scenario}.json"
        out_path.write_text(json.dumps(rows, indent=2))
        print(f"  -> {len(rows)} rows written to {out_path}")
        time.sleep(0.3)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default=DEFAULT_VERSION)
    parser.add_argument(
        "--scenarios",
        nargs="+",
        default=list(SCENARIO_GROUPS.keys()),
    )
    args = parser.parse_args()
    main(args.version, args.scenarios)
