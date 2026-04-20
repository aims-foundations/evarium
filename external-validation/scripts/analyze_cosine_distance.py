"""
Empirical calibration of holdout-vs-public weight cosine distance (Appendix C Q3).

Under the sim's linear scoring abstraction  score = dot(capability, weights) + noise,
the Pearson correlation of two benchmarks' scores across a shared set of models
approximates  cosine(weights_A, weights_B). Score correlations between related
benchmarks are therefore our best empirical handle on how adversarial a "holdout"
benchmark actually is relative to a "public" one.

We compute correlations at three tiers:
    same_family      — two variants of the same benchmark (upper bound)
    within_dimension — two different benchmarks in the same sim capability dimension
    cross_dimension  — benchmarks in structurally different dimensions (lower bound)

CAVEAT: Pearson r between benchmarks is inflated by the dominant "general capability"
factor (good models are good on everything). Treat absolute values as an upper bound
on the true weight-space cosine; the relative ordering across tiers is the primary
signal.

Outputs:
    external-validation/data/processed/cosine_pairs.csv
    (printed: tier-level aggregates + per-pair breakdown)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
from analyze_k_cadence import BENCHMARKS, BENCH_DIR, OUT_DIR, ORG_CANONICAL  # noqa: E402

# Pairs grouped by structural relationship. Each tuple is (benchmark_display_A, benchmark_display_B).
# Chosen to span the sim's capability dimensions and capture both same-skill and cross-skill pairs.
PAIRS: dict[str, list[tuple[str, str]]] = {
    "same_family": [
        ("SWE-Bench-Verified", "SWE-Bench-Bash"),
        ("FrontierMath-T1-3", "FrontierMath-T4"),
        ("ARC-AGI-1",         "ARC-AGI-2"),
    ],
    "within_dimension": [
        ("MMLU",              "GPQA-Diamond"),     # Knowledge + Reasoning
        ("GPQA-Diamond",      "HLE"),              # Reasoning (hard)
        ("MATH-L5",           "FrontierMath-T1-3"),# Math
        ("MATH-L5",           "OTIS-AIME"),        # Math (aime-style)
        ("SWE-Bench-Verified","Aider-Polyglot"),   # Coding
        ("OS-World",          "APEX-Agents"),      # Agentic
        ("ARC-AGI-2",         "HLE"),              # Reasoning
    ],
    "cross_dimension": [
        ("MMLU",              "SWE-Bench-Verified"),# Knowledge vs Coding
        ("MMLU",              "MATH-L5"),           # Knowledge vs Math
        ("GPQA-Diamond",      "OS-World"),          # Reasoning vs Agentic
        ("MATH-L5",           "SWE-Bench-Verified"),# Math vs Coding
        ("HLE",               "OS-World"),          # Hard reasoning vs Agentic
        ("SimpleQA-V",        "MATH-L5"),           # Factual vs Math
    ],
}

# Suffixes and patterns to strip from Model version to build a canonical join key.
_SUFFIX_RE = re.compile(
    r"(_xhigh|_xlow|_high|_medium|_low|_unknown|_32k|_64k|_128k|_8k|_16k"
    r"|-customtools|-preview|-thinking|_thinking|_reasoning|_pro|_fast)",
    flags=re.IGNORECASE,
)
_DATE_RE  = re.compile(r"[-_](\d{4}-\d{2}-\d{2}|\d{8})")
_VENDOR_RE = re.compile(r"^(amazon\.|anthropic/|google/|meta/|openai/)")


def normalize_model_name(raw: str) -> str:
    if not isinstance(raw, str):
        return ""
    s = raw.strip().lower()
    s = _VENDOR_RE.sub("", s)
    s = _SUFFIX_RE.sub("", s)
    s = _DATE_RE.sub("", s)
    s = re.sub(r":0$", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"--+", "-", s).strip("-")
    return s


def load_scores(csv_name: str, display: str, score_col: str) -> pd.DataFrame | None:
    path = BENCH_DIR / csv_name
    if not path.exists():
        return None
    df = pd.read_csv(path)
    if score_col not in df.columns or "Model version" not in df.columns:
        return None
    df = df.rename(columns={score_col: "score"})
    df["score"] = pd.to_numeric(df["score"], errors="coerce")
    df = df.dropna(subset=["score", "Model version"])
    df["model_key"] = df["Model version"].apply(normalize_model_name)
    df = df[df["model_key"] != ""]
    df["org"] = df["Organization"].map(lambda o: ORG_CANONICAL.get(o, o) if isinstance(o, str) else o)
    # Keep max score per model_key (some benchmarks have multiple submissions per model)
    agg = (df.groupby("model_key", as_index=False)
             .agg(score=("score", "max"), org=("org", "first")))
    agg = agg.rename(columns={"score": display})
    return agg[["model_key", "org", display]]


def compare_pair(a: str, b: str, benchmark_lookup: dict) -> dict | None:
    if a not in benchmark_lookup or b not in benchmark_lookup:
        return None
    df_a = benchmark_lookup[a]
    df_b = benchmark_lookup[b]
    merged = pd.merge(df_a, df_b, on="model_key", suffixes=("_A", "_B"))
    # Drop rows where org disagreement suggests the name-normalization collided
    if "org_A" in merged and "org_B" in merged:
        merged = merged[(merged["org_A"].isna()) | (merged["org_B"].isna()) |
                        (merged["org_A"] == merged["org_B"])]
    n = len(merged)
    if n < 4:
        return {"pair": f"{a} vs {b}", "n": n, "pearson_r": np.nan, "spearman_r": np.nan, "p_pearson": np.nan}
    x = merged[a].to_numpy()
    y = merged[b].to_numpy()
    r, p = pearsonr(x, y)
    rho, _ = spearmanr(x, y)
    return {"pair": f"{a} vs {b}", "n": n,
            "pearson_r": round(float(r), 3),
            "spearman_r": round(float(rho), 3),
            "p_pearson": round(float(p), 4)}


def main() -> None:
    # Load all referenced benchmarks once
    needed = {b for tier in PAIRS.values() for pair in tier for b in pair}
    benchmark_lookup: dict[str, pd.DataFrame] = {}
    for csv_name, display, score_col in BENCHMARKS:
        if display not in needed:
            continue
        loaded = load_scores(csv_name, display, score_col)
        if loaded is not None:
            benchmark_lookup[display] = loaded
            print(f"[load] {display}: {len(loaded)} unique models")
        else:
            print(f"[skip] {display}: could not load")

    rows = []
    for tier, pair_list in PAIRS.items():
        for a, b in pair_list:
            result = compare_pair(a, b, benchmark_lookup)
            if result is None:
                print(f"[skip] {a} vs {b}: benchmark missing")
                continue
            result["tier"] = tier
            rows.append(result)
    df = pd.DataFrame(rows)
    if df.empty:
        print("No pairs produced.")
        return

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_DIR / "cosine_pairs.csv", index=False)

    # Tier aggregate
    valid = df.dropna(subset=["pearson_r"])
    agg = (valid.groupby("tier")
                 .agg(n_pairs=("pair", "count"),
                      median_pearson=("pearson_r", "median"),
                      mean_pearson=("pearson_r", "mean"),
                      median_spearman=("spearman_r", "median"))
                 .reindex(["same_family", "within_dimension", "cross_dimension"])
                 .round(3))

    print("\n" + "=" * 100)
    print("COSINE DISTANCE CALIBRATION — Pearson r as proxy for cosine(weights_A, weights_B)")
    print("=" * 100)
    for tier in ["same_family", "within_dimension", "cross_dimension"]:
        sub = df[df["tier"] == tier].drop(columns=["tier"])
        if len(sub) == 0:
            continue
        print(f"\n{tier.upper()}")
        print(sub.to_string(index=False, na_rep="—"))

    print("\n" + "=" * 100)
    print("TIER AGGREGATE (median and mean Pearson r; Spearman as robust sanity check)")
    print("=" * 100)
    print(agg.to_string(na_rep="—"))

    print("\nInterpretation note: Pearson r is inflated by the 'general capability' factor "
          "(frontier models tend to be good across all benchmarks). Treat values as an upper "
          "bound on the true weight-space cosine; the RELATIVE ordering across tiers is the "
          "primary anchor for Q3.")


if __name__ == "__main__":
    main()
