"""
fetch_pwc.py — Scrape Papers with Code SOTA leaderboards for target benchmarks.

Writes:  validation/data/raw/paperwithcode/<benchmark>.json
         Each file: list of {method, provider_raw, score, date} dicts

Usage:
    python validation/scripts/fetch_pwc.py [--benchmarks MMLU HumanEval ...]
"""

import argparse
import json
import time
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# PwC task slugs for each benchmark we care about
# ---------------------------------------------------------------------------
BENCHMARK_TASKS = {
    "MMLU": "multi-task-language-understanding",
    "HumanEval": "code-generation",
    "MATH": "math-word-problem-solving",
    "GPQA": "question-answering",
    "HellaSwag": "sentence-completion",
}

# Metric names vary per task; we keep the first numeric metric found if not listed
PREFERRED_METRIC = {
    "MMLU": "Accuracy",
    "HumanEval": "pass@1",
    "MATH": "Accuracy",
    "GPQA": "Accuracy",
    "HellaSwag": "Accuracy",
}

# Known LLM provider keywords for lightweight filtering
PROVIDER_KEYWORDS = [
    "gpt", "openai", "claude", "anthropic", "gemini", "google", "deepmind",
    "llama", "meta", "mistral", "deepseek", "grok", "cohere", "palm",
]

BASE_URL = "https://paperswithcode.com/api/v1"
RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw" / "paperwithcode"


def fetch_sota(task_slug: str, benchmark_name: str) -> list[dict]:
    """Fetch SOTA rows for a given PwC task slug."""
    url = f"{BASE_URL}/sota/?task={task_slug}&format=json"
    rows = []
    page = 1

    while url:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        for sota_row in data.get("results", []):
            benchmark = sota_row.get("benchmark", {})
            for result in sota_row.get("sota_rows", []):
                metric_name = PREFERRED_METRIC.get(benchmark_name, "")
                # Find the right metric value
                score = None
                metrics = result.get("metrics", {})
                if metric_name and metric_name in metrics:
                    score = metrics[metric_name]
                elif metrics:
                    # fallback: first numeric value
                    for v in metrics.values():
                        try:
                            score = float(v)
                            break
                        except (TypeError, ValueError):
                            pass

                if score is None:
                    continue

                rows.append({
                    "benchmark": benchmark_name,
                    "method": result.get("method_name", ""),
                    "provider_raw": result.get("method_name", ""),
                    "score": float(score),
                    "date": result.get("paper_date") or result.get("date", ""),
                    "paper_title": result.get("paper_title", ""),
                    "source": "paperswithcode",
                })

        url = data.get("next")  # pagination
        page += 1
        if page > 10:  # safety cap
            break
        time.sleep(0.5)  # be polite

    return rows


def main(benchmarks: list[str]) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    for bench in benchmarks:
        task_slug = BENCHMARK_TASKS.get(bench)
        if not task_slug:
            print(f"[WARN] No task slug defined for {bench}, skipping.")
            continue

        print(f"Fetching {bench} ({task_slug}) ...")
        try:
            rows = fetch_sota(task_slug, bench)
        except requests.HTTPError as exc:
            print(f"  [ERROR] HTTP {exc.response.status_code}: {exc}")
            rows = []

        out_path = RAW_DIR / f"{bench.lower()}.json"
        out_path.write_text(json.dumps(rows, indent=2))
        print(f"  -> {len(rows)} rows written to {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--benchmarks",
        nargs="+",
        default=list(BENCHMARK_TASKS.keys()),
        help="Benchmarks to fetch (default: all)",
    )
    args = parser.parse_args()
    main(args.benchmarks)
