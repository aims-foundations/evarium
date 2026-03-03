"""
normalize.py — Align raw benchmark and market data to a common format.

Outputs:
  validation/data/processed/benchmarks.csv
    columns: provider, benchmark, score_norm, score_raw, date, sim_round, source

  validation/data/processed/market_share.csv
    columns: provider, date, sim_round, share_estimate, source

Normalization steps:
  1. Map real provider names → sim provider names
  2. Map real benchmark names → sim benchmark analogs
  3. Convert date → sim_round  (anchor: GPT-4 launch 2023-03-14 ≈ round 0,
                                  each round ≈ 1 quarter = 3 months)
  4. Min-max normalize scores per benchmark → [0, 1]
  5. Normalize market share to sum-to-1 fractions per (date, source)

Usage:
    python validation/scripts/normalize.py
"""

import csv
import json
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
VAL_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = VAL_DIR / "data" / "raw"
PROC_DIR = VAL_DIR / "data" / "processed"

# ---------------------------------------------------------------------------
# Provider mapping  (substring match, case-insensitive; order matters)
# ---------------------------------------------------------------------------
PROVIDER_MAP = [
    # (substring_in_raw_name,  sim_provider)
    ("openai", "Orion Labs"),
    ("gpt", "Orion Labs"),
    ("o1", "Orion Labs"),
    ("o3", "Orion Labs"),
    ("anthropic", "Apex AI"),
    ("claude", "Apex AI"),
    ("google", "Genesis Systems"),
    ("deepmind", "Genesis Systems"),
    ("gemini", "Genesis Systems"),
    ("bard", "Genesis Systems"),
    ("palm", "Genesis Systems"),
    ("meta", "Mirage AI"),
    ("llama", "Mirage AI"),
    ("deepseek", "OpenCore"),
    ("mistral", "Spark AI"),
    ("mixtral", "Spark AI"),
    ("cohere", "Spark AI"),
]


def map_provider(raw: str) -> str:
    raw_lower = raw.lower()
    for keyword, sim_name in PROVIDER_MAP:
        if keyword in raw_lower:
            return sim_name
    return "Other"


# ---------------------------------------------------------------------------
# Benchmark mapping
# ---------------------------------------------------------------------------
BENCHMARK_MAP = {
    "MMLU": "writing",          # general knowledge, long history
    "HumanEval": "coding_advanced",
    "humaneval": "coding_advanced",
    "MATH": "math_advanced",
    "math": "math_advanced",
    "GPQA": "reasoning_advanced",
    "HellaSwag": "writing",
    "mmlu": "writing",
    "code-generation": "coding_advanced",
    "math-word-problem-solving": "math_advanced",
    "question-answering": "reasoning_advanced",
    "sentence-completion": "writing",
}


def map_benchmark(raw: str) -> str:
    return BENCHMARK_MAP.get(raw, raw.lower().replace(" ", "_"))


# ---------------------------------------------------------------------------
# Date → sim round
# Anchor: 2023-03-14 (GPT-4 launch) = round 0.  1 round = 1 quarter.
# ---------------------------------------------------------------------------
ANCHOR = datetime(2023, 3, 14)
DAYS_PER_ROUND = 91  # ~3 months


def date_to_sim_round(date_str: str) -> int | None:
    """Return integer sim round (can be negative for pre-GPT-4 data)."""
    if not date_str:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
        try:
            dt = datetime.strptime(date_str[:len(fmt.replace("%Y", "0000").replace("%m", "00").replace("%d", "00"))], fmt)
            delta_days = (dt - ANCHOR).days
            return round(delta_days / DAYS_PER_ROUND)
        except ValueError:
            pass
    # Try ISO with fractional seconds
    try:
        dt = datetime.fromisoformat(date_str[:10])
        delta_days = (dt - ANCHOR).days
        return round(delta_days / DAYS_PER_ROUND)
    except ValueError:
        return None


def _parse_date(date_str: str) -> datetime | None:
    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
        try:
            return datetime.strptime(date_str[:10], fmt)
        except ValueError:
            pass
    return None


# ---------------------------------------------------------------------------
# Load raw benchmark data
# ---------------------------------------------------------------------------
def load_pwc_rows() -> list[dict]:
    rows = []
    pwc_dir = RAW_DIR / "paperwithcode"
    for json_file in pwc_dir.glob("*.json"):
        try:
            data = json.loads(json_file.read_text())
        except json.JSONDecodeError:
            print(f"[WARN] Could not parse {json_file}")
            continue
        bench_name = json_file.stem.upper()
        for r in data:
            rows.append({
                "benchmark_raw": r.get("benchmark", bench_name),
                "provider_raw": r.get("provider_raw", r.get("method", "")),
                "score_raw": r.get("score"),
                "date": r.get("date", ""),
                "source": "paperswithcode",
            })
    return rows


def load_helm_rows() -> list[dict]:
    rows = []
    helm_dir = RAW_DIR / "helm"
    for json_file in helm_dir.glob("*.json"):
        try:
            data = json.loads(json_file.read_text())
        except json.JSONDecodeError:
            print(f"[WARN] Could not parse {json_file}")
            continue
        for r in data:
            rows.append({
                "benchmark_raw": r.get("scenario", json_file.stem),
                "provider_raw": r.get("provider_raw", r.get("model", "")),
                "score_raw": r.get("score"),
                "date": r.get("run_date", ""),
                "source": "helm",
            })
    return rows


# ---------------------------------------------------------------------------
# Normalize benchmarks
# ---------------------------------------------------------------------------
def normalize_benchmarks() -> None:
    all_rows = load_pwc_rows() + load_helm_rows()

    if not all_rows:
        print("[WARN] No raw benchmark data found. Run fetch_pwc.py and fetch_helm.py first.")
        PROC_DIR.mkdir(parents=True, exist_ok=True)
        (PROC_DIR / "benchmarks.csv").write_text(
            "provider,benchmark,score_norm,score_raw,date,sim_round,source\n"
        )
        return

    # Map provider and benchmark
    for r in all_rows:
        r["provider"] = map_provider(r["provider_raw"])
        r["benchmark"] = map_benchmark(r["benchmark_raw"])
        r["sim_round"] = date_to_sim_round(r["date"])

    # Min-max per benchmark
    from collections import defaultdict
    bench_scores: dict[str, list[float]] = defaultdict(list)
    for r in all_rows:
        if r["score_raw"] is not None:
            try:
                bench_scores[r["benchmark"]].append(float(r["score_raw"]))
            except (TypeError, ValueError):
                pass

    bench_min = {b: min(v) for b, v in bench_scores.items()}
    bench_max = {b: max(v) for b, v in bench_scores.items()}

    PROC_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PROC_DIR / "benchmarks.csv"
    fieldnames = ["provider", "benchmark", "score_norm", "score_raw", "date", "sim_round", "source"]

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in all_rows:
            if r["score_raw"] is None:
                continue
            b = r["benchmark"]
            lo, hi = bench_min.get(b, 0), bench_max.get(b, 1)
            try:
                raw = float(r["score_raw"])
            except (TypeError, ValueError):
                continue
            score_norm = (raw - lo) / (hi - lo) if hi > lo else 0.5
            writer.writerow({
                "provider": r["provider"],
                "benchmark": b,
                "score_norm": round(score_norm, 4),
                "score_raw": round(raw, 4),
                "date": r["date"],
                "sim_round": r["sim_round"],
                "source": r["source"],
            })

    print(f"benchmarks.csv: {len(all_rows)} rows -> {out_path}")


# ---------------------------------------------------------------------------
# Load and normalize market share
# ---------------------------------------------------------------------------
def load_market_rows() -> list[dict]:
    rows = []
    market_dir = RAW_DIR / "market"

    # web_traffic.csv
    wt = market_dir / "web_traffic.csv"
    if wt.exists():
        with wt.open(encoding="utf-8") as f:
            for line in f:
                if line.startswith("#"):
                    continue
            f.seek(0)
            try:
                reader = csv.DictReader(f)
                for r in reader:
                    visits = r.get("monthly_visits", "")
                    try:
                        v = float(visits) if visits else None
                    except ValueError:
                        v = None
                    rows.append({
                        "provider_raw": r.get("domain", ""),
                        "sim_provider": r.get("sim_provider", ""),
                        "date": r.get("date", ""),
                        "raw_value": v,
                        "source": "similarweb",
                    })
            except Exception as exc:
                print(f"[WARN] web_traffic.csv parse error: {exc}")

    # so_survey.csv
    so = market_dir / "so_survey.csv"
    if so.exists():
        with so.open(encoding="utf-8") as f:
            for line in f:
                if line.startswith("#"):
                    continue
            f.seek(0)
            try:
                reader = csv.DictReader(f)
                for r in reader:
                    try:
                        frac = float(r.get("usage_fraction", 0))
                    except ValueError:
                        frac = None
                    rows.append({
                        "provider_raw": r.get("sim_provider", ""),
                        "sim_provider": r.get("sim_provider", ""),
                        "date": r.get("date", ""),
                        "raw_value": frac,
                        "source": r.get("source", "so_survey"),
                    })
            except Exception as exc:
                print(f"[WARN] so_survey.csv parse error: {exc}")

    return rows


def normalize_market() -> None:
    rows = load_market_rows()

    PROC_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PROC_DIR / "market_share.csv"

    if not rows:
        print("[WARN] No market data found. Run fetch_market.py first.")
        out_path.write_text("provider,date,sim_round,share_estimate,source\n")
        return

    # Group by (date, source) → normalize to sum=1
    from collections import defaultdict
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for r in rows:
        key = (r["date"], r["source"])
        groups[key].append(r)

    fieldnames = ["provider", "date", "sim_round", "share_estimate", "source"]
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for (date, source), group in groups.items():
            total = sum(r["raw_value"] or 0 for r in group)
            sim_round = date_to_sim_round(date)
            for r in group:
                val = r["raw_value"]
                share = (val / total) if (val and total > 0) else None
                writer.writerow({
                    "provider": r["sim_provider"] or map_provider(r["provider_raw"]),
                    "date": date,
                    "sim_round": sim_round,
                    "share_estimate": round(share, 4) if share is not None else "",
                    "source": source,
                })

    print(f"market_share.csv: {len(rows)} rows -> {out_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    normalize_benchmarks()
    normalize_market()
    print("Normalization complete.")


if __name__ == "__main__":
    main()
