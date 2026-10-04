"""
fetch_pwc.py — Collect real-world LLM benchmark data from two sources:

1. KNOWN_SCORES (hardcoded) — flagship model scores from published technical
   reports and papers.  These are the most important datapoints for comparing
   against the sim's major providers and are not subject to API availability.

2. Open LLM Leaderboard v2 — HF dataset 'open-llm-leaderboard/contents'.
   Covers thousands of open-source models with submission dates.  Good proxy
   for the competitive landscape below the frontier.

Papers with Code was shut down by Meta in July 2025; its archive is hosted on
Hugging Face but the datasets server is unreliable for it.

Writes:  validation/data/raw/paperwithcode/<benchmark>.json
         Each file: list of {method, provider_raw, score, date, benchmark} dicts

Usage:
    python validation/scripts/fetch_pwc.py [--skip-leaderboard]
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import requests

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw" / "paperwithcode"

# ---------------------------------------------------------------------------
# 1. Hardcoded flagship benchmark scores
#    Sources: GPT-4 TR (2023-03), Claude-3 TR (2024-03), Gemini TR (2023-12),
#             LLaMA-3 blog (2024-04), DeepSeek-V2 TR (2024-05),
#             GPT-4o blog (2024-05), Claude-3.5-S blog (2024-06),
#             Gemini-1.5-Pro TR (2024-02), o1 blog (2024-09)
# ---------------------------------------------------------------------------
KNOWN_SCORES: list[dict] = [
    # --- MMLU (5-shot accuracy) ---
    {"benchmark": "MMLU", "method": "GPT-4",            "provider_raw": "openai",    "score": 0.864, "date": "2023-03-14"},
    {"benchmark": "MMLU", "method": "GPT-3.5-turbo",    "provider_raw": "openai",    "score": 0.700, "date": "2022-11-30"},
    {"benchmark": "MMLU", "method": "Claude-2",         "provider_raw": "anthropic", "score": 0.787, "date": "2023-07-11"},
    {"benchmark": "MMLU", "method": "Claude-3-Haiku",   "provider_raw": "anthropic", "score": 0.752, "date": "2024-03-13"},
    {"benchmark": "MMLU", "method": "Claude-3-Sonnet",  "provider_raw": "anthropic", "score": 0.790, "date": "2024-03-13"},
    {"benchmark": "MMLU", "method": "Claude-3-Opus",    "provider_raw": "anthropic", "score": 0.868, "date": "2024-03-13"},
    {"benchmark": "MMLU", "method": "Claude-3.5-Sonnet","provider_raw": "anthropic", "score": 0.889, "date": "2024-06-20"},
    {"benchmark": "MMLU", "method": "Gemini-1.0-Pro",   "provider_raw": "google",    "score": 0.714, "date": "2023-12-06"},
    {"benchmark": "MMLU", "method": "Gemini-1.0-Ultra", "provider_raw": "google",    "score": 0.900, "date": "2023-12-06"},
    {"benchmark": "MMLU", "method": "Gemini-1.5-Pro",   "provider_raw": "google",    "score": 0.818, "date": "2024-02-15"},
    {"benchmark": "MMLU", "method": "PaLM-2-L",         "provider_raw": "google",    "score": 0.780, "date": "2023-05-10"},
    {"benchmark": "MMLU", "method": "LLaMA-2-70B",      "provider_raw": "meta",      "score": 0.690, "date": "2023-07-18"},
    {"benchmark": "MMLU", "method": "LLaMA-3-8B",       "provider_raw": "meta",      "score": 0.666, "date": "2024-04-18"},
    {"benchmark": "MMLU", "method": "LLaMA-3-70B",      "provider_raw": "meta",      "score": 0.820, "date": "2024-04-18"},
    {"benchmark": "MMLU", "method": "Mixtral-8x7B",     "provider_raw": "mistral",   "score": 0.706, "date": "2023-12-11"},
    {"benchmark": "MMLU", "method": "Mistral-7B",       "provider_raw": "mistral",   "score": 0.641, "date": "2023-09-27"},
    {"benchmark": "MMLU", "method": "DeepSeek-V2",      "provider_raw": "deepseek",  "score": 0.783, "date": "2024-05-07"},
    {"benchmark": "MMLU", "method": "GPT-4o",           "provider_raw": "openai",    "score": 0.887, "date": "2024-05-13"},
    {"benchmark": "MMLU", "method": "o1-preview",       "provider_raw": "openai",    "score": 0.904, "date": "2024-09-12"},

    # --- HumanEval (pass@1) ---
    {"benchmark": "HumanEval", "method": "GPT-4",           "provider_raw": "openai",    "score": 0.670, "date": "2023-03-14"},
    {"benchmark": "HumanEval", "method": "GPT-3.5-turbo",   "provider_raw": "openai",    "score": 0.480, "date": "2022-11-30"},
    {"benchmark": "HumanEval", "method": "Claude-3-Opus",   "provider_raw": "anthropic", "score": 0.840, "date": "2024-03-13"},
    {"benchmark": "HumanEval", "method": "Claude-3.5-Sonnet","provider_raw":"anthropic", "score": 0.920, "date": "2024-06-20"},
    {"benchmark": "HumanEval", "method": "Gemini-1.0-Ultra","provider_raw": "google",    "score": 0.745, "date": "2023-12-06"},
    {"benchmark": "HumanEval", "method": "Gemini-1.5-Pro",  "provider_raw": "google",    "score": 0.845, "date": "2024-02-15"},
    {"benchmark": "HumanEval", "method": "LLaMA-3-70B",     "provider_raw": "meta",      "score": 0.816, "date": "2024-04-18"},
    {"benchmark": "HumanEval", "method": "Mixtral-8x7B",    "provider_raw": "mistral",   "score": 0.409, "date": "2023-12-11"},
    {"benchmark": "HumanEval", "method": "DeepSeek-Coder-V2","provider_raw":"deepseek",  "score": 0.900, "date": "2024-06-17"},
    {"benchmark": "HumanEval", "method": "GPT-4o",          "provider_raw": "openai",    "score": 0.903, "date": "2024-05-13"},
    {"benchmark": "HumanEval", "method": "code-davinci-002","provider_raw": "openai",    "score": 0.470, "date": "2022-03-01"},

    # --- MATH (accuracy) ---
    {"benchmark": "MATH", "method": "GPT-4",            "provider_raw": "openai",    "score": 0.426, "date": "2023-03-14"},
    {"benchmark": "MATH", "method": "GPT-3.5-turbo",    "provider_raw": "openai",    "score": 0.342, "date": "2022-11-30"},
    {"benchmark": "MATH", "method": "Claude-3-Opus",    "provider_raw": "anthropic", "score": 0.605, "date": "2024-03-13"},
    {"benchmark": "MATH", "method": "Claude-3.5-Sonnet","provider_raw": "anthropic", "score": 0.715, "date": "2024-06-20"},
    {"benchmark": "MATH", "method": "Gemini-1.0-Ultra", "provider_raw": "google",    "score": 0.536, "date": "2023-12-06"},
    {"benchmark": "MATH", "method": "Gemini-1.5-Pro",   "provider_raw": "google",    "score": 0.677, "date": "2024-02-15"},
    {"benchmark": "MATH", "method": "LLaMA-3-70B",      "provider_raw": "meta",      "score": 0.504, "date": "2024-04-18"},
    {"benchmark": "MATH", "method": "Mixtral-8x7B",     "provider_raw": "mistral",   "score": 0.287, "date": "2023-12-11"},
    {"benchmark": "MATH", "method": "DeepSeek-V2",      "provider_raw": "deepseek",  "score": 0.534, "date": "2024-05-07"},
    {"benchmark": "MATH", "method": "GPT-4o",           "provider_raw": "openai",    "score": 0.764, "date": "2024-05-13"},
    {"benchmark": "MATH", "method": "o1-preview",       "provider_raw": "openai",    "score": 0.850, "date": "2024-09-12"},

    # --- GPQA (accuracy, diamond set) ---
    {"benchmark": "GPQA", "method": "GPT-4",            "provider_raw": "openai",    "score": 0.363, "date": "2023-11-01"},
    {"benchmark": "GPQA", "method": "Claude-3-Opus",    "provider_raw": "anthropic", "score": 0.503, "date": "2024-03-13"},
    {"benchmark": "GPQA", "method": "Claude-3.5-Sonnet","provider_raw": "anthropic", "score": 0.593, "date": "2024-06-20"},
    {"benchmark": "GPQA", "method": "Gemini-1.5-Pro",   "provider_raw": "google",    "score": 0.463, "date": "2024-02-15"},
    {"benchmark": "GPQA", "method": "GPT-4o",           "provider_raw": "openai",    "score": 0.534, "date": "2024-05-13"},
    {"benchmark": "GPQA", "method": "o1-preview",       "provider_raw": "openai",    "score": 0.739, "date": "2024-09-12"},
    {"benchmark": "GPQA", "method": "LLaMA-3-70B",      "provider_raw": "meta",      "score": 0.397, "date": "2024-04-18"},
    {"benchmark": "GPQA", "method": "DeepSeek-V2",      "provider_raw": "deepseek",  "score": 0.435, "date": "2024-05-07"},

    # --- HellaSwag (accuracy, 10-shot) ---
    {"benchmark": "HellaSwag", "method": "GPT-4",           "provider_raw": "openai",    "score": 0.952, "date": "2023-03-14"},
    {"benchmark": "HellaSwag", "method": "GPT-3.5-turbo",   "provider_raw": "openai",    "score": 0.850, "date": "2022-11-30"},
    {"benchmark": "HellaSwag", "method": "Claude-3-Opus",   "provider_raw": "anthropic", "score": 0.953, "date": "2024-03-13"},
    {"benchmark": "HellaSwag", "method": "Gemini-1.0-Ultra","provider_raw": "google",    "score": 0.874, "date": "2023-12-06"},
    {"benchmark": "HellaSwag", "method": "PaLM-2-L",        "provider_raw": "google",    "score": 0.868, "date": "2023-05-10"},
    {"benchmark": "HellaSwag", "method": "LLaMA-2-70B",     "provider_raw": "meta",      "score": 0.875, "date": "2023-07-18"},
    {"benchmark": "HellaSwag", "method": "LLaMA-3-70B",     "provider_raw": "meta",      "score": 0.928, "date": "2024-04-18"},
    {"benchmark": "HellaSwag", "method": "Mistral-7B",      "provider_raw": "mistral",   "score": 0.813, "date": "2023-09-27"},
    {"benchmark": "HellaSwag", "method": "Mixtral-8x7B",    "provider_raw": "mistral",   "score": 0.864, "date": "2023-12-11"},
]

# Add source field to all hardcoded rows
for _r in KNOWN_SCORES:
    _r["source"] = "paperswithcode"

# ---------------------------------------------------------------------------
# 2. Open LLM Leaderboard v2
#    Maps open-source model names → sim providers; extracts available scores
# ---------------------------------------------------------------------------
HF_ROWS_URL = "https://datasets-server.huggingface.co/rows"
LB_DATASET = "open-llm-leaderboard/contents"
LB_PAGE_SIZE = 100

# Benchmark columns in the leaderboard → our benchmark labels
LB_COLUMNS = {
    "MMLU-PRO":     "MMLU",
    "MATH Lvl 5":   "MATH",
    "GPQA":         "GPQA",
    "BBH":          "MMLU",     # Big-Bench Hard ≈ reasoning, map to MMLU as proxy
    "IFEval":       None,       # skip — no sim analog
    "MUSR":         None,       # skip
}

# Provider keyword → provider_raw
LB_PROVIDER_MAP = [
    ("llama",     "meta"),
    ("meta-",     "meta"),
    ("mistral",   "mistral"),
    ("mixtral",   "mistral"),
    ("deepseek",  "deepseek"),
    ("qwen",      "other"),
    ("falcon",    "other"),
    ("phi",       "other"),
    ("yi-",       "other"),
]


def lb_provider(fullname: str) -> str:
    fl = fullname.lower()
    for kw, prov in LB_PROVIDER_MAP:
        if kw in fl:
            return prov
    return "other"


def fetch_leaderboard() -> list[dict]:
    """Page through the Open LLM Leaderboard dataset and extract benchmark rows."""
    rows = []
    offset = 0
    total = None

    while True:
        url = (
            f"{HF_ROWS_URL}?dataset={LB_DATASET}"
            f"&config=default&split=train&offset={offset}&length={LB_PAGE_SIZE}"
        )
        try:
            resp = requests.get(url, timeout=90)
            resp.raise_for_status()
        except (requests.HTTPError, requests.exceptions.Timeout) as exc:
            print(f"  [WARN] Leaderboard fetch failed at offset {offset}: {exc}")
            break

        data = resp.json()
        if total is None:
            total = data.get("num_rows_total", 0)

        batch = data.get("rows", [])
        if not batch:
            break

        for item in batch:
            r = item["row"]
            fullname = r.get("fullname", "")
            date_str = r.get("Submission Date") or r.get("Upload To Hub Date") or ""
            provider = lb_provider(fullname)

            for col, bench in LB_COLUMNS.items():
                if bench is None:
                    continue
                score_raw = r.get(col)
                if score_raw is None:
                    score_raw = r.get(f"{col} Raw")
                if score_raw is None:
                    continue
                try:
                    score = float(score_raw)
                    # Leaderboard scores are 0-100; normalise to 0-1
                    if score > 1.5:
                        score = score / 100.0
                except (TypeError, ValueError):
                    continue

                rows.append({
                    "benchmark": bench,
                    "method": fullname,
                    "provider_raw": provider,
                    "score": round(score, 4),
                    "date": date_str[:10] if date_str else "",
                    "source": "paperswithcode",
                })

        offset += len(batch)
        print(f"  Fetched {offset}/{total} leaderboard rows ...", end="\r")

        if total and offset >= total:
            break
        time.sleep(0.3)

    print()
    return rows


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main(skip_leaderboard: bool) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    # --- Hardcoded known scores ---
    print("Loading hardcoded flagship benchmark scores ...")
    all_rows = list(KNOWN_SCORES)
    print(f"  {len(all_rows)} hardcoded rows loaded.")

    # --- Open LLM Leaderboard ---
    if not skip_leaderboard:
        print("Fetching Open LLM Leaderboard v2 ...")
        lb_rows = fetch_leaderboard()
        print(f"  {len(lb_rows)} leaderboard rows fetched.")
        all_rows.extend(lb_rows)
    else:
        print("Skipping Open LLM Leaderboard.")

    # --- Split by benchmark and write ---
    benchmarks: dict[str, list[dict]] = {}
    for r in all_rows:
        benchmarks.setdefault(r["benchmark"], []).append(r)

    for bench, rows in benchmarks.items():
        out_path = RAW_DIR / f"{bench.lower()}.json"
        out_path.write_text(json.dumps(rows, indent=2))
        print(f"  {bench}: {len(rows)} rows -> {out_path.name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skip-leaderboard", action="store_true",
        help="Only use hardcoded scores, skip Open LLM Leaderboard download",
    )
    args = parser.parse_args()
    main(args.skip_leaderboard)
