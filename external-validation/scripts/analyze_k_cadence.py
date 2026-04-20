"""
Compute per-(provider, benchmark) K_advance from Epoch AI benchmark CSVs.

K_advance = months between consecutive releases where a provider's running-max
score on that benchmark advances. Anchor for private-benchmark reporting cadence
(Appendix C Q2 — how often does a private benchmark get "re-evaluated" for a
given provider in real-world leaderboard dynamics).

Inputs:
    external-validation/data/benchmarks/*.csv (one file per benchmark)

Outputs:
    external-validation/data/processed/k_cadence_long.csv
    external-validation/data/processed/k_cadence_matrix_mean.csv   (provider x benchmark)
    external-validation/data/processed/k_cadence_matrix_median.csv
    external-validation/data/processed/k_cadence_n_advances.csv
"""
from pathlib import Path
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
BENCH_DIR = REPO_ROOT / "external-validation" / "data" / "benchmarks"
OUT_DIR = REPO_ROOT / "external-validation" / "data" / "processed"

# (filename, display_name, score_column)
# Score column verified by inspecting each CSV. Files with multi-row-per-model
# schemas (terminalbench_external, posttrainbench_external, gso_external) are
# excluded — they have a `Scaffold`/`Agent` axis that breaks running-max semantics.
BENCHMARKS = [
    ("mmlu_external.csv",               "MMLU",               "EM"),
    ("gpqa_diamond.csv",                "GPQA-Diamond",       "mean_score"),
    ("math_level_5.csv",                "MATH-L5",            "mean_score"),
    ("frontiermath.csv",                "FrontierMath-T1-3",  "mean_score"),
    ("frontiermath_tier_4.csv",         "FrontierMath-T4",    "mean_score"),
    ("swe_bench_verified.csv",          "SWE-Bench-Verified", "mean_score"),
    ("swe_bench_bash.csv",              "SWE-Bench-Bash",     "% Resolved"),
    ("aider_polyglot_external.csv",     "Aider-Polyglot",     "Percent correct"),
    ("arc_agi_external.csv",            "ARC-AGI-1",          "Score"),
    ("arc_agi_2_external.csv",          "ARC-AGI-2",          "Score"),
    ("hle_external.csv",                "HLE",                "Accuracy"),
    ("os_world_external.csv",           "OS-World",           "Score"),
    ("the_agent_company_external.csv",  "AgentCo",            "% Score"),
    ("apex_agents_external.csv",        "APEX-Agents",        "Pass@1 score"),
    ("cybench_external.csv",            "Cybench",            "Unguided % Solved"),
    ("simpleqa_verified.csv",           "SimpleQA-V",         "mean_score"),
    ("chess_puzzles.csv",               "Chess-Puzzles",      "mean_score"),
    ("live_bench_external.csv",         "LiveBench",          "Global average"),
    ("bbh_external.csv",                "BBH",                "Average"),
    ("gsm8k_external.csv",              "GSM8K",              "EM"),
    ("balrog_external.csv",             "BALROG",             "Average progress"),
    ("otis_mock_aime_2024_2025.csv",    "OTIS-AIME",          "mean_score"),
    ("webdev_arena_external.csv",       "WebDev-Arena",       "Arena Score"),
    ("epoch_capabilities_index.csv",    "ECI",                "ECI Score"),
]

# Canonicalize provider names — merge Google/DeepMind and Meta/Meta AI so we
# get a single row per provider in the output matrix.
ORG_CANONICAL = {
    "Google DeepMind": "Google",
    "Google":          "Google",
    "Meta AI":         "Meta",
    "Meta":            "Meta",
    "Facebook AI Research": "Meta",
    "Alibaba Cloud":   "Alibaba",
    "Alibaba":         "Alibaba",
}

FRONTIER_LABS = {
    "OpenAI", "Anthropic", "Google", "Meta",
    "DeepSeek", "xAI", "Mistral AI", "Alibaba",
}

# Tier-1 = labs that have held the capability frontier (top of ECI) at some
# point in 2023-2026. DeepSeek, Mistral, and Alibaba release frontier-adjacent
# models but have rarely (or never) set the global max; their K dynamics are
# closer to fast-follower cadence than frontier cadence. Use this set to
# confirm conclusions don't hinge on trailing-tier providers.
FRONTIER_TIER_1 = {
    "OpenAI", "Anthropic", "Google", "xAI", "Meta",
}

# Benchmarks dropped entirely: they track a different cadence than flagship releases.
# >3 rows/month means checkpoint variants / community re-runs, not model events.
EXCLUDE_FROM_PRIMARY = {
    "Aider-Polyglot":   "community benchmark updates on checkpoint variants (~3.7 rows/mo)",
    "ARC-AGI-1":        "community-run rapid submissions (~6.6 rows/mo)",
    "ARC-AGI-2":        "community-run rapid submissions (~5.9 rows/mo)",
    "LiveBench":        "live-updating composite by design; measures continuous drift, not release events",
}

# Benchmarks kept but truncated at their saturation date — defined as the last
# date where the *global frontier* running-max advanced. Submissions after this
# contribute only ceiling-bound observations and would inflate K_advance
# artificially. The window before saturation still carries a valid release-cadence
# signal that we want to retain.
TRUNCATE_AT_SATURATION = {
    "MMLU":  "saturated for frontier labs; truncate to pre-saturation window",
    "GSM8K": "saturated early 2024; truncate to pre-saturation window",
    "BBH":   "no submissions after 2024-12; truncate to last-advance date",
}

# Sim-dimension groupings (from docs/stakeholders.md capability DIMENSIONS).
# Math benchmarks split out from Reasoning for two reasons: (1) they form a
# coherent cluster in the sim's Scientific Reasoning pool entry; (2) they
# saturate at different rates than general reasoning. LiveBench held aside as
# a mixed-composite; ECI reported separately as overall-capability reference.
DIMENSION_GROUPS = {
    "Knowledge":  ["MMLU", "SimpleQA-V"],
    "Reasoning":  ["GPQA-Diamond", "BBH", "ARC-AGI-1", "ARC-AGI-2", "HLE", "Chess-Puzzles"],
    "Math":       ["MATH-L5", "FrontierMath-T1-3", "FrontierMath-T4", "GSM8K", "OTIS-AIME"],
    "Coding":     ["Aider-Polyglot", "SWE-Bench-Bash", "SWE-Bench-Verified", "WebDev-Arena"],
    "Agentic":    ["OS-World", "AgentCo", "APEX-Agents", "BALROG"],
    "Safety":     ["Cybench"],
    "Composite":  ["LiveBench", "ECI"],
}


def _global_saturation_date(df: pd.DataFrame) -> pd.Timestamp:
    """Date of the last global frontier advance (running-max across all providers).
    After this date, no new submission can advance the frontier by definition —
    those submissions are ceiling-bound and inflate K if retained."""
    g = df.sort_values("date").reset_index(drop=True)
    running_max = -np.inf
    last_advance_date = g["date"].iloc[0]
    for _, row in g.iterrows():
        if row["score"] > running_max:
            running_max = row["score"]
            last_advance_date = row["date"]
    return last_advance_date


def load_benchmark(csv_name: str, display: str, score_col: str,
                   lab_filter: set[str]) -> pd.DataFrame | None:
    path = BENCH_DIR / csv_name
    if not path.exists():
        print(f"[skip] {csv_name}: file not found")
        return None
    df = pd.read_csv(path)
    if score_col not in df.columns:
        print(f"[skip] {csv_name}: score column '{score_col}' missing")
        return None
    df = df.rename(columns={score_col: "score"})
    df["date"] = pd.to_datetime(df["Release date"], errors="coerce")
    df["score"] = pd.to_numeric(df["score"], errors="coerce")
    df = df.dropna(subset=["date", "score", "Organization"])
    df["org"] = df["Organization"].map(lambda o: ORG_CANONICAL.get(o, o))
    df = df[df["org"].isin(lab_filter)].copy()
    df["benchmark"] = display

    if display in TRUNCATE_AT_SATURATION and len(df) > 0:
        cutoff = _global_saturation_date(df)
        n_before = len(df)
        df = df[df["date"] <= cutoff].copy()
        print(f"[truncate] {display}: cutoff={cutoff.date()}, kept {len(df)}/{n_before} frontier rows")
    return df[["org", "benchmark", "date", "score"]]


def compute_k_advance(group: pd.DataFrame) -> dict:
    """Return stats for one (provider, benchmark) group."""
    g = group.sort_values("date").reset_index(drop=True)
    advance_dates: list[pd.Timestamp] = []
    running_max = -np.inf
    for _, row in g.iterrows():
        if row["score"] > running_max:
            advance_dates.append(row["date"])
            running_max = row["score"]
    n_releases = len(g)
    n_advances = len(advance_dates)
    if n_advances < 2:
        return {
            "n_releases": n_releases,
            "n_advances": n_advances,
            "span_months": (g["date"].max() - g["date"].min()).days / 30.0 if n_releases > 1 else np.nan,
            "mean_K": np.nan,
            "median_K": np.nan,
        }
    gaps_days = np.diff([d.to_pydatetime() for d in advance_dates])
    gaps_months = np.array([g.days / 30.0 for g in gaps_days])
    return {
        "n_releases": n_releases,
        "n_advances": n_advances,
        "span_months": (advance_dates[-1] - advance_dates[0]).days / 30.0,
        "mean_K": float(gaps_months.mean()),
        "median_K": float(np.median(gaps_months)),
    }


def compute_benchmark_diagnostics(all_df: pd.DataFrame) -> pd.DataFrame:
    """Per-benchmark density + saturation diagnostics to support exclusion decisions."""
    rows = []
    cutoff_saturation = pd.Timestamp("2025-07-01")  # end of sim window; advances after this = still moving
    for bench, g in all_df.groupby("benchmark"):
        n_rows = len(g)
        span = (g["date"].max() - g["date"].min()).days / 30.0
        density = n_rows / span if span > 0 else np.nan
        # Check saturation: what fraction of providers with n>=3 had their running max advance after cutoff?
        providers = g["org"].unique()
        still_advancing = 0
        evaluable = 0
        for p in providers:
            sub = g[g["org"] == p].sort_values("date")
            if len(sub) < 3:
                continue
            evaluable += 1
            # Latest advance date for this provider
            run_max = -np.inf
            last_advance = None
            for _, row in sub.iterrows():
                if row["score"] > run_max:
                    run_max = row["score"]
                    last_advance = row["date"]
            if last_advance is not None and last_advance >= cutoff_saturation:
                still_advancing += 1
        sat_frac = 1.0 - (still_advancing / evaluable) if evaluable > 0 else np.nan
        if bench in EXCLUDE_FROM_PRIMARY:
            handling = "drop"; reason = EXCLUDE_FROM_PRIMARY[bench]
        elif bench in TRUNCATE_AT_SATURATION:
            handling = "truncate"; reason = TRUNCATE_AT_SATURATION[bench]
        else:
            handling = "keep"; reason = ""
        rows.append({
            "benchmark": bench,
            "n_rows": n_rows,
            "span_months": round(span, 1),
            "rows_per_month": round(density, 2),
            "pct_providers_saturated": round(sat_frac * 100, 0) if not np.isnan(sat_frac) else np.nan,
            "handling": handling,
            "reason": reason,
        })
    return pd.DataFrame(rows).sort_values("rows_per_month", ascending=False).reset_index(drop=True)


def run_analysis(lab_filter: set[str], tag: str) -> dict:
    """Compute K_advance tables for a given lab-filter set; write outputs with `tag` suffix."""
    print(f"\n{'#' * 110}")
    print(f"# ANALYSIS: {tag.upper()}  (labs: {sorted(lab_filter)})")
    print(f"{'#' * 110}")

    frames = [load_benchmark(*row, lab_filter=lab_filter) for row in BENCHMARKS]
    frames = [f for f in frames if f is not None and len(f) > 0]
    all_df = pd.concat(frames, ignore_index=True)
    print(f"\nLoaded {len(frames)} benchmarks; {len(all_df):,} rows after filter")

    diag = compute_benchmark_diagnostics(all_df)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    diag.to_csv(OUT_DIR / f"benchmark_diagnostics_{tag}.csv", index=False)

    rows = []
    for (org, bench), g in all_df.groupby(["org", "benchmark"]):
        rows.append({"provider": org, "benchmark": bench, **compute_k_advance(g)})
    result = pd.DataFrame(rows)
    result.to_csv(OUT_DIR / f"k_cadence_long_{tag}.csv", index=False)

    bench_order = [b for _, b, _ in BENCHMARKS if b in result["benchmark"].unique()]
    provider_order = [p for p in ["OpenAI", "Anthropic", "Google", "Meta",
                                  "DeepSeek", "xAI", "Mistral AI", "Alibaba"]
                      if p in result["provider"].unique()]

    mean_pivot = (result.pivot(index="provider", columns="benchmark", values="mean_K")
                        .reindex(index=provider_order, columns=bench_order))
    median_pivot = (result.pivot(index="provider", columns="benchmark", values="median_K")
                          .reindex(index=provider_order, columns=bench_order))
    n_pivot = (result.pivot(index="provider", columns="benchmark", values="n_advances")
                     .reindex(index=provider_order, columns=bench_order))

    mean_pivot.to_csv(OUT_DIR / f"k_cadence_matrix_mean_{tag}.csv")
    median_pivot.to_csv(OUT_DIR / f"k_cadence_matrix_median_{tag}.csv")
    n_pivot.to_csv(OUT_DIR / f"k_cadence_n_advances_{tag}.csv")

    print("\nK_advance MEAN (provider x benchmark, months):")
    print(mean_pivot.round(1).to_string(na_rep="—"))

    # --- Per-provider aggregate (across their benchmarks, post-exclusion) ---
    prov_src = result[(result["n_advances"] >= 2) & (~result["benchmark"].isin(EXCLUDE_FROM_PRIMARY))]
    prov_agg = (prov_src.groupby("provider")
                          .agg(n_benchmarks=("benchmark", "nunique"),
                               n_total_advances=("n_advances", "sum"),
                               mean_K=("mean_K", "mean"),
                               median_K=("mean_K", "median"),
                               std_K=("mean_K", "std"),
                               min_K=("mean_K", "min"),
                               max_K=("mean_K", "max"))
                          .round(2)
                          .reindex(provider_order)
                          .dropna(subset=["n_benchmarks"]))
    prov_agg.to_csv(OUT_DIR / f"k_cadence_provider_aggregate_{tag}.csv")

    print(f"\n{'=' * 110}")
    print("PER-PROVIDER AGGREGATE (across benchmarks, after excluding checkpoint-cadence + live)")
    print("=" * 110)
    print(prov_agg.to_string(na_rep="—"))

    pm = prov_agg["mean_K"]
    print(f"\nAcross-provider stats of mean_K:  median={pm.median():.2f}  std={pm.std():.2f}  "
          f"range=[{pm.min():.2f}, {pm.max():.2f}]  CV={pm.std()/pm.mean():.0%}")

    # --- Dimension-level aggregation ---
    bench_to_dim = {b: d for d, bs in DIMENSION_GROUPS.items() for b in bs}
    result_valid = result[result["n_advances"] >= 2].copy()
    result_valid["dimension"] = result_valid["benchmark"].map(bench_to_dim)
    result_valid = result_valid.dropna(subset=["dimension"])
    result_valid = result_valid[~result_valid["benchmark"].isin(EXCLUDE_FROM_PRIMARY)]

    dim_simple = (result_valid.groupby(["provider", "dimension"])
                              .agg(n_benchmarks=("benchmark", "nunique"),
                                   mean_K=("mean_K", "mean"))
                              .reset_index())

    def _weighted_mean(sub: pd.DataFrame) -> float:
        w = sub["n_advances"].astype(float)
        return float((sub["mean_K"] * w).sum() / w.sum()) if w.sum() > 0 else np.nan
    dim_weighted = (result_valid.groupby(["provider", "dimension"])
                                .apply(_weighted_mean, include_groups=False)
                                .reset_index(name="mean_K_weighted"))

    dim_order = list(DIMENSION_GROUPS.keys())
    dim_simple_pivot = (dim_simple.pivot(index="provider", columns="dimension", values="mean_K")
                                  .reindex(index=provider_order, columns=dim_order))
    dim_weighted_pivot = (dim_weighted.pivot(index="provider", columns="dimension", values="mean_K_weighted")
                                      .reindex(index=provider_order, columns=dim_order))
    dim_simple_pivot.to_csv(OUT_DIR / f"k_cadence_dimension_mean_{tag}.csv")
    dim_weighted_pivot.to_csv(OUT_DIR / f"k_cadence_dimension_weighted_{tag}.csv")

    print(f"\n{'=' * 110}")
    print("K_advance by SIM DIMENSION — n_advances-weighted mean (months)")
    print("=" * 110)
    print(dim_weighted_pivot.round(1).to_string(na_rep="—"))

    pooled = (result_valid.groupby("dimension")
                          .apply(lambda s: pd.Series({
                              "n_providers": s["provider"].nunique(),
                              "n_benchmarks": s["benchmark"].nunique(),
                              "n_cells": len(s),
                              "simple_mean_K": float(s["mean_K"].mean()),
                              "weighted_mean_K": float((s["mean_K"] * s["n_advances"]).sum() / s["n_advances"].sum()),
                              "median_of_medians_K": float(s["median_K"].median()),
                          }), include_groups=False)
                          .reindex(dim_order)
                          .round(2))
    pooled.to_csv(OUT_DIR / f"k_cadence_dimension_pooled_{tag}.csv")
    print(f"\n{'=' * 110}")
    print("DIMENSION AGGREGATE — pooled across (provider, benchmark) cells")
    print("=" * 110)
    print(pooled.to_string(na_rep="—"))

    return {"pooled": pooled, "provider_agg": prov_agg, "dim_weighted": dim_weighted_pivot}


def main() -> None:
    results_frontier = run_analysis(FRONTIER_LABS, tag="frontier")
    results_tier1 = run_analysis(FRONTIER_TIER_1, tag="tier1")

    # --- Side-by-side comparison ---
    print("\n" + "#" * 110)
    print("# COMPARISON: FRONTIER (all 8 labs) vs TIER-1 (OpenAI/Anthropic/Google/Meta/xAI)")
    print("#" * 110)
    cmp = pd.DataFrame({
        "frontier_n_cells":   results_frontier["pooled"]["n_cells"],
        "tier1_n_cells":      results_tier1["pooled"]["n_cells"],
        "frontier_weighted":  results_frontier["pooled"]["weighted_mean_K"],
        "tier1_weighted":     results_tier1["pooled"]["weighted_mean_K"],
        "frontier_medmed":    results_frontier["pooled"]["median_of_medians_K"],
        "tier1_medmed":       results_tier1["pooled"]["median_of_medians_K"],
    })
    cmp["delta_weighted"] = (cmp["tier1_weighted"] - cmp["frontier_weighted"]).round(2)
    cmp["delta_medmed"]   = (cmp["tier1_medmed"]   - cmp["frontier_medmed"]).round(2)
    print("\nDimension-level comparison (months):")
    print(cmp.round(2).to_string(na_rep="—"))

    print("\nHeadline: global n-weighted mean of dimension weighted_mean_K:")
    print(f"  FRONTIER (8 labs): {results_frontier['pooled']['weighted_mean_K'].mean():.2f} mo")
    print(f"  TIER-1 (5 labs):   {results_tier1['pooled']['weighted_mean_K'].mean():.2f} mo")


if __name__ == "__main__":
    main()
