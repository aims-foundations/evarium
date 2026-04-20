"""
aggregate_heuristic.py -- Comprehensive aggregation of heuristic baseline runs.

Produces:
  - heuristic_summary.csv     (endpoint metrics per condition x policy)
  - outcome_typology.csv      (per-run outcome classification)
  - pattern_matrix.csv        (structural pattern pass rates)
  - trajectory_data/*.csv     (per-round quantile bands for 6 core metrics)
  - ablation_effects.csv      (delta vs baseline with statistical tests)
  - plots/                    (quantile trajectories, heatmaps, forest plots)

Usage:
  python scripts/aggregate_heuristic.py
  python scripts/aggregate_heuristic.py --condition full_ecosystem
  python scripts/aggregate_heuristic.py --policy balanced
  python scripts/aggregate_heuristic.py --no-plots
"""

import argparse
import csv
import json
import os
import sys
import warnings
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(_PROJECT_ROOT, "src"))

HEURISTIC_BASE = os.path.join(
    _PROJECT_ROOT, "sandbox", "experiments", "heuristic"
)
OUTPUT_BASE = os.path.join(_PROJECT_ROOT, "output", "heuristic_analysis")
POLICIES = ("balanced", "us", "eu")
BASELINE_CONDITION = "full_ecosystem"

HHI_COMPETITIVE = 0.15
HHI_CONCENTRATED = 0.25

# ---------------------------------------------------------------------------
# Imports from existing modules
# ---------------------------------------------------------------------------
from plotting import (
    _DIMS, _to_vec, _cos_sim, _get_need_weights, _get_bm_agg_weights,
    _gap_decomposition, get_providers,
)
from diagnostics import (
    extract_metric_series,
    check_patterns,
    metric_hhi,
    metric_mean_safety,
    metric_consumer_satisfaction,
    metric_incident_count,
    metric_mean_score,
)


# ============================================================================
# CLI
# ============================================================================

def parse_args():
    p = argparse.ArgumentParser(
        description="Aggregate Phase 5 heuristic baseline results."
    )
    p.add_argument("--condition", type=str, default=None,
                   help="Filter to specific condition")
    p.add_argument("--policy", type=str, default=None,
                   help="Filter to specific policy (balanced/us/eu)")
    p.add_argument("--no-plots", action="store_true",
                   help="Skip plot generation (CSV output only)")
    p.add_argument("--last-n", type=int, default=5,
                   help="Number of final rounds for endpoint metrics")
    p.add_argument("-o", "--output", type=str, default=None,
                   help="Output directory override")
    return p.parse_args()


# ============================================================================
# Discovery
# ============================================================================

def parse_condition_policy(dirname: str):
    """Split 'no_media_balanced' -> ('no_media', 'balanced')."""
    for pol in POLICIES:
        suffix = f"_{pol}"
        if dirname.endswith(suffix):
            return dirname[: -len(suffix)], pol
    return dirname, "unknown"


def discover_heuristic_runs(base_dir, condition_filter=None,
                            policy_filter=None):
    """Walk nested dir structure, return grouped seed dirs.

    Returns:
        {label: {"condition": str, "policy": str,
                 "seed_dirs": [abs_paths]}}
    """
    results = {}
    if not os.path.isdir(base_dir):
        print(f"WARNING: base dir not found: {base_dir}")
        return results

    for entry in sorted(os.listdir(base_dir)):
        entry_path = os.path.join(base_dir, entry)
        if not os.path.isdir(entry_path):
            continue
        condition, policy = parse_condition_policy(entry)

        if condition_filter and condition != condition_filter:
            continue
        if policy_filter and policy != policy_filter:
            continue

        seeds_dir = os.path.join(entry_path, "seeds")
        if not os.path.isdir(seeds_dir):
            continue

        seed_dirs = []
        for seed_entry in sorted(os.listdir(seeds_dir)):
            seed_path = os.path.join(seeds_dir, seed_entry)
            if os.path.isdir(seed_path) and os.path.exists(
                os.path.join(seed_path, "rounds.jsonl")
            ):
                seed_dirs.append(seed_path)

        if seed_dirs:
            results[entry] = {
                "condition": condition,
                "policy": policy,
                "seed_dirs": seed_dirs,
            }

    return results


# ============================================================================
# Data loading
# ============================================================================

def load_history_jsonl(exp_dir: str) -> list:
    """Load rounds.jsonl from an experiment directory."""
    path = os.path.join(exp_dir, "rounds.jsonl")
    if not os.path.exists(path):
        return []
    rounds = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rounds.append(json.loads(line))
    return rounds


# ============================================================================
# Per-run metrics (reused from plot_experiment.py logic)
# ============================================================================

def compute_condition_metrics(history, last_n=5):
    """Compute aggregate metrics for one experiment run."""
    if not history:
        return {}

    from scipy.stats import rankdata

    providers = get_providers(history)
    need = _get_need_weights(history)
    n_rounds = len(history)
    last_rounds = history[-last_n:] if n_rounds >= last_n else history

    sn, dm, pl, tg = [], [], [], []
    for h in last_rounds:
        for p in providers:
            g = _gap_decomposition(h, p, need)
            sn.append(g["score_noise"])
            dm.append(g["dim_mismatch"])
            pl.append(g["penalty_load"])
            tg.append(g["total_gap"])

    reliability_vals = []
    for h in last_rounds:
        cd = h.get("consumer_data", {})
        ps = cd.get("provider_satisfaction", {})
        scores_list, sats_list = [], []
        for p in providers:
            if p in h.get("scores", {}) and p in ps:
                scores_list.append(h["scores"][p])
                sats_list.append(ps[p])
        if len(scores_list) >= 2:
            sr = rankdata(scores_list)
            satr = rankdata(sats_list)
            corr = np.corrcoef(sr, satr)[0, 1]
            if not np.isnan(corr):
                reliability_vals.append(corr)

    hhi_vals = []
    for h in last_rounds:
        ms = h.get("consumer_data", {}).get("market_shares", {})
        if ms:
            hhi_vals.append(sum(v ** 2 for v in ms.values()))

    safety_vals = []
    for h in last_rounds:
        for p in providers:
            s = h.get("strategies", {}).get(p, {}).get("safety", 0)
            safety_vals.append(s)

    total_incidents = sum(len(h.get("incidents", [])) for h in history)
    incidents_per_round = total_incidents / max(n_rounds, 1)

    sat_vals = []
    for h in last_rounds:
        sat = h.get("consumer_data", {}).get("avg_satisfaction")
        if sat is not None:
            sat_vals.append(sat)

    diff_vals = []
    for h in last_rounds:
        cap_means = []
        for p in providers:
            cv = h.get("capability_vectors", {}).get(p, {})
            if cv:
                cap_means.append(sum(cv.values()) / len(cv))
        if len(cap_means) >= 2:
            diff_vals.append(float(np.std(cap_means)))

    growth_cos_vals = []
    if len(history) >= 2:
        r0, rf = history[0], history[-1]
        for p in providers:
            cv0 = r0.get("capability_vectors", {}).get(p, {})
            cvf = rf.get("capability_vectors", {}).get(p, {})
            if cv0 and cvf:
                cap0, capf = _to_vec(cv0), _to_vec(cvf)
                growth = capf - cap0
                if np.linalg.norm(growth) > 1e-8:
                    growth_cos_vals.append(_cos_sim(growth, need))

    def _m(vals):
        return float(np.mean(vals)) if vals else 0.0

    def _se(vals):
        return (float(np.std(vals, ddof=1) / np.sqrt(len(vals)))
                if len(vals) >= 2 else 0.0)

    return {
        "score_noise": _m(sn), "score_noise_se": _se(sn),
        "dim_mismatch": _m(dm), "dim_mismatch_se": _se(dm),
        "penalty_load": _m(pl), "penalty_load_se": _se(pl),
        "total_gap": _m(tg), "total_gap_se": _se(tg),
        "score_reliability": _m(reliability_vals),
        "score_reliability_se": _se(reliability_vals),
        "hhi": _m(hhi_vals), "hhi_se": _se(hhi_vals),
        "mean_safety": _m(safety_vals),
        "incidents_per_round": incidents_per_round,
        "mean_satisfaction": _m(sat_vals),
        "mean_satisfaction_se": _se(sat_vals),
        "provider_differentiation": _m(diff_vals),
        "growth_need_alignment": _m(growth_cos_vals),
        "n_rounds": n_rounds,
    }


def aggregate_across_seeds(seed_metrics):
    """Aggregate metrics from multiple seeds into mean +/- SE."""
    if len(seed_metrics) == 1:
        result = dict(seed_metrics[0])
        result["n_seeds"] = 1
        return result

    se_fields = [
        "score_noise", "dim_mismatch", "penalty_load", "total_gap",
        "score_reliability", "hhi", "mean_satisfaction",
    ]
    scalar_fields = [
        "mean_safety", "incidents_per_round", "provider_differentiation",
        "growth_need_alignment",
    ]

    result = {}
    n = len(seed_metrics)

    for field in se_fields:
        vals = [m[field] for m in seed_metrics if field in m]
        result[field] = float(np.mean(vals)) if vals else 0.0
        result[f"{field}_se"] = (
            float(np.std(vals, ddof=1) / np.sqrt(len(vals)))
            if len(vals) >= 2 else 0.0
        )

    for field in scalar_fields:
        vals = [m[field] for m in seed_metrics if field in m]
        result[field] = float(np.mean(vals)) if vals else 0.0
        # Add SE for scalar fields too (useful for ablation effects)
        result[f"{field}_se"] = (
            float(np.std(vals, ddof=1) / np.sqrt(len(vals)))
            if len(vals) >= 2 else 0.0
        )

    result["n_rounds"] = max(m["n_rounds"] for m in seed_metrics)
    result["n_seeds"] = n

    return result


# ============================================================================
# Outcome classification
# ============================================================================

def classify_outcome(history, last_n=5):
    """Classify a single run's outcome type."""
    if not history:
        return {}

    providers = get_providers(history)
    need = _get_need_weights(history)
    last_rounds = history[-last_n:] if len(history) >= last_n else history
    final = history[-1]

    # Market winner
    ms = final.get("consumer_data", {}).get("market_shares", {})
    if ms:
        winner = max(ms, key=ms.get)
        winner_share = ms[winner]
    else:
        winner, winner_share = "unknown", 0.0

    # HHI and market structure
    hhi = sum(v ** 2 for v in ms.values()) if ms else 0.0
    if hhi < HHI_COMPETITIVE:
        structure = "competitive"
    elif hhi < HHI_CONCENTRATED:
        structure = "moderate"
    else:
        structure = "concentrated"

    # Leader pathway (winner's mean allocation over last_n)
    rd_vals, safety_vals, product_vals = [], [], []
    for h in last_rounds:
        strat = h.get("effective_strategies", h.get("strategies", {}))
        s = strat.get(winner, {})
        rd_vals.append(s.get("rd", 0))
        safety_vals.append(s.get("safety", 0))
        product_vals.append(s.get("product", 0))

    leader_rd = float(np.mean(rd_vals)) if rd_vals else 0.0
    leader_safety = float(np.mean(safety_vals)) if safety_vals else 0.0
    leader_product = float(np.mean(product_vals)) if product_vals else 0.0

    allocs = {"rd_led": leader_rd, "safety_led": leader_safety,
              "product_led": leader_product}
    pathway = max(allocs, key=allocs.get)

    # Final gap
    gap_vals = []
    for h in last_rounds:
        for p in providers:
            g = _gap_decomposition(h, p, need)
            gap_vals.append(g["total_gap"])
    final_gap = float(np.mean(gap_vals)) if gap_vals else 0.0

    return {
        "market_winner": winner,
        "winner_share": round(winner_share, 4),
        "market_structure": structure,
        "hhi": round(hhi, 4),
        "leader_pathway": pathway,
        "leader_rd": round(leader_rd, 4),
        "leader_safety": round(leader_safety, 4),
        "leader_product": round(leader_product, 4),
        "final_gap": round(final_gap, 4),
    }


# ============================================================================
# Compatibility wrapper for check_patterns
# ============================================================================

def _inject_true_capabilities(history):
    """Add true_capabilities from capability_vectors for check_patterns compat."""
    for rd in history:
        if "true_capabilities" not in rd and "capability_vectors" in rd:
            rd["true_capabilities"] = {
                name: sum(vec.values()) / len(vec) if vec else 0.0
                for name, vec in rd["capability_vectors"].items()
            }
    return history


# ============================================================================
# New metric functions for trajectories
# ============================================================================

def metric_mean_gap(rd):
    """Mean (score - provider_satisfaction) across providers."""
    scores = rd.get("scores", {})
    cd = rd.get("consumer_data", {})
    ps = cd.get("provider_satisfaction", {})
    gaps = []
    for name, score in scores.items():
        sat = ps.get(name)
        if sat is not None:
            gaps.append(score - sat)
    return float(np.mean(gaps)) if gaps else None


def metric_reliability(rd):
    """Per-round Spearman rank correlation (scores vs satisfaction)."""
    from scipy.stats import rankdata
    scores = rd.get("scores", {})
    cd = rd.get("consumer_data", {})
    ps = cd.get("provider_satisfaction", {})
    s_list, sat_list = [], []
    for name, score in scores.items():
        sat = ps.get(name)
        if sat is not None:
            s_list.append(score)
            sat_list.append(sat)
    if len(s_list) < 2:
        return None
    sr = rankdata(s_list)
    satr = rankdata(sat_list)
    corr = np.corrcoef(sr, satr)[0, 1]
    return float(corr) if not np.isnan(corr) else None


CORE_METRIC_FNS = {
    "gap": metric_mean_gap,
    "hhi": metric_hhi,
    "safety": metric_mean_safety,
    "satisfaction": metric_consumer_satisfaction,
    "incidents": metric_incident_count,
    "reliability": metric_reliability,
}


# ============================================================================
# Trajectory quantiles
# ============================================================================

def compute_trajectory_stats(histories, metric_fns):
    """Compute per-round quantile stats across seeds.

    Returns {metric_name: {"round": [...], "mean": [...], "median": [...],
                           "p10": [...], "p90": [...]}}
    """
    result = {}
    for name, fn in metric_fns.items():
        series = extract_metric_series(histories, fn)  # (N, T)
        n_rounds = series.shape[1]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            result[name] = {
                "round": list(range(n_rounds)),
                "mean": [float(x) for x in np.nanmean(series, axis=0)],
                "median": [float(x) for x in np.nanmedian(series, axis=0)],
                "p10": [float(x) for x in np.nanpercentile(series, 10, axis=0)],
                "p90": [float(x) for x in np.nanpercentile(series, 90, axis=0)],
            }
    return result


# ============================================================================
# Ablation effects
# ============================================================================

ABLATION_METRICS = [
    "total_gap", "score_noise", "dim_mismatch", "penalty_load",
    "hhi", "mean_safety", "incidents_per_round",
    "mean_satisfaction", "score_reliability",
]


def compute_ablation_effects(all_seed_metrics):
    """Compute ablation effect sizes vs full_ecosystem baseline per policy.

    Args:
        all_seed_metrics: {label: [list of per-seed metric dicts]}

    Returns:
        list of dicts with delta, CI, Cohen's d, p-value per metric.
    """
    from scipy.stats import ttest_ind, t as t_dist

    # Group by policy
    by_policy = defaultdict(dict)
    for label, metrics_list in all_seed_metrics.items():
        cond, pol = parse_condition_policy(label)
        by_policy[pol][cond] = metrics_list

    results = []
    for pol, cond_metrics in by_policy.items():
        baseline = cond_metrics.get(BASELINE_CONDITION)
        if baseline is None:
            continue

        for cond, abl_metrics in cond_metrics.items():
            if cond == BASELINE_CONDITION:
                continue

            for metric in ABLATION_METRICS:
                base_vals = [m[metric] for m in baseline if metric in m]
                abl_vals = [m[metric] for m in abl_metrics if metric in m]

                if len(base_vals) < 2 or len(abl_vals) < 2:
                    continue

                base_arr = np.array(base_vals)
                abl_arr = np.array(abl_vals)
                n_b, n_a = len(base_arr), len(abl_arr)

                delta = float(np.mean(abl_arr) - np.mean(base_arr))
                s_b = float(np.std(base_arr, ddof=1))
                s_a = float(np.std(abl_arr, ddof=1))

                # Pooled SD
                sp = np.sqrt(
                    ((n_b - 1) * s_b ** 2 + (n_a - 1) * s_a ** 2)
                    / (n_b + n_a - 2)
                ) if (n_b + n_a - 2) > 0 else 1e-10
                cohens_d = delta / sp if sp > 1e-10 else 0.0

                # t-test
                t_stat, p_val = ttest_ind(abl_arr, base_arr)
                p_val = float(p_val) if not np.isnan(p_val) else 1.0

                # 95% CI on delta
                se_diff = sp * np.sqrt(1 / n_a + 1 / n_b)
                df = n_a + n_b - 2
                t_crit = t_dist.ppf(0.975, df)
                ci_lo = delta - t_crit * se_diff
                ci_hi = delta + t_crit * se_diff

                results.append({
                    "condition": cond,
                    "policy": pol,
                    "metric": metric,
                    "baseline_mean": round(float(np.mean(base_arr)), 6),
                    "ablation_mean": round(float(np.mean(abl_arr)), 6),
                    "delta": round(delta, 6),
                    "ci_lo": round(ci_lo, 6),
                    "ci_hi": round(ci_hi, 6),
                    "cohens_d": round(cohens_d, 4),
                    "p_value": round(p_val, 6),
                    "n_baseline": n_b,
                    "n_ablation": n_a,
                    "significant": p_val < 0.05,
                })

    return results


# ============================================================================
# CSV writers
# ============================================================================

def write_heuristic_summary(all_aggregated, all_seed_metrics,
                            all_outcome_rows, output_dir):
    """Write heuristic_summary.csv."""
    from scipy.stats import t as t_dist

    path = os.path.join(output_dir, "heuristic_summary.csv")
    fields = [
        "condition", "policy", "n_seeds",
        "total_gap", "total_gap_se", "total_gap_ci_lo", "total_gap_ci_hi",
        "score_noise", "score_noise_se",
        "dim_mismatch", "dim_mismatch_se",
        "penalty_load", "penalty_load_se",
        "score_reliability", "score_reliability_se",
        "hhi", "hhi_se",
        "mean_safety", "mean_safety_se",
        "incidents_per_round", "incidents_per_round_se",
        "mean_satisfaction", "mean_satisfaction_se",
        "provider_differentiation", "growth_need_alignment",
        "modal_winner", "modal_winner_freq",
    ]

    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()

        for label in sorted(all_aggregated.keys()):
            cond, pol = parse_condition_policy(label)
            agg = all_aggregated[label]
            n = agg.get("n_seeds", 1)

            # 95% CI for total_gap
            se = agg.get("total_gap_se", 0)
            t_crit = t_dist.ppf(0.975, max(n - 1, 1)) if n > 1 else 0
            ci_lo = agg["total_gap"] - t_crit * se
            ci_hi = agg["total_gap"] + t_crit * se

            # Modal winner from outcome rows
            label_outcomes = [
                r for r in all_outcome_rows
                if r["condition"] == cond and r["policy"] == pol
            ]
            if label_outcomes:
                winner_counts = Counter(
                    r["market_winner"] for r in label_outcomes
                )
                modal_winner, modal_count = winner_counts.most_common(1)[0]
                modal_freq = round(modal_count / len(label_outcomes), 3)
            else:
                modal_winner = ""
                modal_freq = 0.0

            row = {
                "condition": cond, "policy": pol,
                "n_seeds": n,
                "total_gap": round(agg["total_gap"], 6),
                "total_gap_se": round(se, 6),
                "total_gap_ci_lo": round(ci_lo, 6),
                "total_gap_ci_hi": round(ci_hi, 6),
                "score_noise": round(agg.get("score_noise", 0), 6),
                "score_noise_se": round(agg.get("score_noise_se", 0), 6),
                "dim_mismatch": round(agg.get("dim_mismatch", 0), 6),
                "dim_mismatch_se": round(agg.get("dim_mismatch_se", 0), 6),
                "penalty_load": round(agg.get("penalty_load", 0), 6),
                "penalty_load_se": round(agg.get("penalty_load_se", 0), 6),
                "score_reliability": round(agg.get("score_reliability", 0), 6),
                "score_reliability_se": round(agg.get("score_reliability_se", 0), 6),
                "hhi": round(agg.get("hhi", 0), 6),
                "hhi_se": round(agg.get("hhi_se", 0), 6),
                "mean_safety": round(agg.get("mean_safety", 0), 6),
                "mean_safety_se": round(agg.get("mean_safety_se", 0), 6),
                "incidents_per_round": round(agg.get("incidents_per_round", 0), 6),
                "incidents_per_round_se": round(agg.get("incidents_per_round_se", 0), 6),
                "mean_satisfaction": round(agg.get("mean_satisfaction", 0), 6),
                "mean_satisfaction_se": round(agg.get("mean_satisfaction_se", 0), 6),
                "provider_differentiation": round(agg.get("provider_differentiation", 0), 6),
                "growth_need_alignment": round(agg.get("growth_need_alignment", 0), 6),
                "modal_winner": modal_winner,
                "modal_winner_freq": modal_freq,
            }
            w.writerow(row)

    print(f"  Wrote {path}")


def write_outcome_typology(all_outcome_rows, output_dir):
    """Write outcome_typology.csv."""
    path = os.path.join(output_dir, "outcome_typology.csv")
    fields = [
        "condition", "policy", "seed", "market_winner", "winner_share",
        "market_structure", "hhi", "leader_pathway",
        "leader_rd", "leader_safety", "leader_product", "final_gap",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in sorted(all_outcome_rows,
                          key=lambda r: (r["condition"], r["policy"],
                                         r["seed"])):
            w.writerow(row)

    print(f"  Wrote {path} ({len(all_outcome_rows)} runs)")


def write_pattern_matrix(all_pattern_results, output_dir):
    """Write pattern_matrix.csv."""
    path = os.path.join(output_dir, "pattern_matrix.csv")
    pattern_names = [
        "benchmark_turnover", "score_inflation", "safety_incident_response",
        "gaming_persistence", "commoditization_shock",
        "regulatory_escalation", "funding_follows_scores",
    ]
    fields = ["condition", "policy", "n_seeds"] + pattern_names

    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for label in sorted(all_pattern_results.keys()):
            cond, pol = parse_condition_policy(label)
            pr = all_pattern_results[label]
            row = {"condition": cond, "policy": pol}
            # n_seeds from pattern details
            for pname in pattern_names:
                info = pr.get(pname, {})
                row[pname] = round(info.get("fraction", 0.0), 3)
            # Get n_seeds from any pattern's details
            for pname in pattern_names:
                info = pr.get(pname, {})
                details = info.get("details", "")
                if "/" in details:
                    try:
                        row["n_seeds"] = int(details.split("/")[-1].split()[0])
                        break
                    except (ValueError, IndexError):
                        pass
            if "n_seeds" not in row:
                row["n_seeds"] = 0
            w.writerow(row)

    print(f"  Wrote {path}")


def write_trajectory_csvs(all_trajectory_data, output_dir):
    """Write per-condition trajectory CSV files."""
    traj_dir = os.path.join(output_dir, "trajectory_data")
    os.makedirs(traj_dir, exist_ok=True)

    for label, metrics_data in sorted(all_trajectory_data.items()):
        path = os.path.join(traj_dir, f"{label}.csv")

        # Build columns
        first_metric = next(iter(metrics_data.values()))
        n_rounds = len(first_metric["round"])

        fields = ["round"]
        for mname in CORE_METRIC_FNS:
            for stat in ("mean", "median", "p10", "p90"):
                fields.append(f"{mname}_{stat}")

        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            for t in range(n_rounds):
                row = {"round": t}
                for mname in CORE_METRIC_FNS:
                    md = metrics_data.get(mname, {})
                    for stat in ("mean", "median", "p10", "p90"):
                        vals = md.get(stat, [])
                        row[f"{mname}_{stat}"] = (
                            round(vals[t], 6) if t < len(vals) else ""
                        )
                w.writerow(row)

    print(f"  Wrote {len(all_trajectory_data)} trajectory CSVs to {traj_dir}")


def write_ablation_effects(effects, output_dir):
    """Write ablation_effects.csv."""
    path = os.path.join(output_dir, "ablation_effects.csv")
    fields = [
        "condition", "policy", "metric",
        "baseline_mean", "ablation_mean", "delta",
        "ci_lo", "ci_hi", "cohens_d", "p_value",
        "n_baseline", "n_ablation", "significant",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in sorted(effects,
                          key=lambda r: (r["policy"], r["condition"],
                                         r["metric"])):
            w.writerow(row)

    n_sig = sum(1 for r in effects if r["significant"])
    print(f"  Wrote {path} ({len(effects)} effects, {n_sig} significant)")


# ============================================================================
# Plots
# ============================================================================

def _setup_plotting():
    """Configure matplotlib with NeurIPS styling."""
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    try:
        from tueplots import bundles as _tb
        rc = _tb.neurips2024()
        rc.pop("figure.figsize", None)
        if os.environ.get("MPLLATEX", "1") != "0":
            rc["text.usetex"] = True
        mpl.rcParams.update(rc)
    except ImportError:
        warnings.warn("tueplots not installed -- using defaults.")
    return plt


def plot_quantile_trajectories(all_trajectory_data, metric_name,
                               ylabel, output_dir, policy_filter=None):
    """Plot quantile band trajectories for one metric, faceted by condition."""
    plt = _setup_plotting()

    # Filter by policy
    labels = sorted(all_trajectory_data.keys())
    if policy_filter:
        labels = [l for l in labels if l.endswith(f"_{policy_filter}")]

    if not labels:
        return

    n = len(labels)
    cols = min(4, n)
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(3.2 * cols, 2.4 * rows),
                             squeeze=False, sharex=True, sharey=True)

    for idx, label in enumerate(labels):
        r, c = divmod(idx, cols)
        ax = axes[r][c]
        md = all_trajectory_data[label].get(metric_name, {})
        rounds = md.get("round", [])
        mean = md.get("mean", [])
        p10 = md.get("p10", [])
        p90 = md.get("p90", [])
        median = md.get("median", [])

        if rounds:
            ax.fill_between(rounds, p10, p90, alpha=0.25, color="#4ECDC4")
            ax.plot(rounds, median, color="#4ECDC4", linewidth=1.2)
            ax.plot(rounds, mean, color="#2C3E50", linewidth=0.8,
                    linestyle="--", alpha=0.7)

        cond, pol = parse_condition_policy(label)
        ax.set_title(cond.replace("_", " "), fontsize=7)
        if c == 0:
            ax.set_ylabel(ylabel, fontsize=7)
        if r == rows - 1:
            ax.set_xlabel("Round", fontsize=7)
        ax.tick_params(labelsize=6)

    # Hide empty subplots
    for idx in range(n, rows * cols):
        r, c = divmod(idx, cols)
        axes[r][c].set_visible(False)

    pol_tag = policy_filter or "all"
    fig.suptitle(f"{metric_name} ({pol_tag})", fontsize=9, y=1.02)
    fig.tight_layout()
    outpath = os.path.join(output_dir, f"traj_{metric_name}_{pol_tag}.png")
    fig.savefig(outpath, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_outcome_heatmap(all_outcome_rows, output_dir):
    """Outcome frequency heatmap: conditions x market winners."""
    plt = _setup_plotting()

    for pol in POLICIES:
        rows = [r for r in all_outcome_rows if r["policy"] == pol]
        if not rows:
            continue

        conditions = sorted(set(r["condition"] for r in rows))
        winners = sorted(set(r["market_winner"] for r in rows))

        matrix = np.zeros((len(conditions), len(winners)))
        for r in rows:
            ci = conditions.index(r["condition"])
            wi = winners.index(r["market_winner"])
            matrix[ci, wi] += 1

        fig, ax = plt.subplots(
            figsize=(max(6, len(winners) * 0.8), max(4, len(conditions) * 0.35))
        )
        im = ax.imshow(matrix, cmap="YlOrRd", aspect="auto")

        ax.set_xticks(range(len(winners)))
        ax.set_xticklabels([w.replace(" ", "\n") for w in winners],
                           fontsize=6, rotation=45, ha="right")
        ax.set_yticks(range(len(conditions)))
        ax.set_yticklabels([c.replace("_", " ") for c in conditions],
                           fontsize=6)

        # Annotate cells
        for i in range(len(conditions)):
            for j in range(len(winners)):
                val = int(matrix[i, j])
                if val > 0:
                    ax.text(j, i, str(val), ha="center", va="center",
                            fontsize=6,
                            color="white" if val > matrix.max() * 0.6
                            else "black")

        ax.set_title(f"Market Winner Frequency ({pol})", fontsize=9)
        fig.colorbar(im, ax=ax, shrink=0.6, label="Count")
        fig.savefig(os.path.join(output_dir, f"outcome_heatmap_{pol}.png"),
                    dpi=200, bbox_inches="tight")
        plt.close(fig)


def plot_pattern_heatmap(all_pattern_results, output_dir):
    """Pattern pass rate heatmap."""
    plt = _setup_plotting()

    pattern_names = [
        "benchmark_turnover", "score_inflation", "safety_incident_response",
        "gaming_persistence", "commoditization_shock",
        "regulatory_escalation", "funding_follows_scores",
    ]
    labels = sorted(all_pattern_results.keys())
    if not labels:
        return

    matrix = np.zeros((len(labels), len(pattern_names)))
    for i, label in enumerate(labels):
        pr = all_pattern_results[label]
        for j, pname in enumerate(pattern_names):
            matrix[i, j] = pr.get(pname, {}).get("fraction", 0.0)

    fig, ax = plt.subplots(
        figsize=(max(6, len(pattern_names) * 0.9),
                 max(4, len(labels) * 0.3))
    )
    im = ax.imshow(matrix, cmap="RdYlGn", aspect="auto", vmin=0, vmax=1)

    ax.set_xticks(range(len(pattern_names)))
    ax.set_xticklabels([p.replace("_", "\n") for p in pattern_names],
                       fontsize=6, rotation=45, ha="right")
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels([l.replace("_", " ") for l in labels], fontsize=5)

    for i in range(len(labels)):
        for j in range(len(pattern_names)):
            val = matrix[i, j]
            ax.text(j, i, f"{val:.0%}", ha="center", va="center",
                    fontsize=5,
                    color="white" if val < 0.3 or val > 0.8 else "black")

    ax.set_title("Pattern Pass Rates", fontsize=9)
    fig.colorbar(im, ax=ax, shrink=0.6, label="Pass fraction")
    fig.savefig(os.path.join(output_dir, "pattern_heatmap.png"),
                dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_ablation_forest(effects, metric, output_dir):
    """Forest plot: ablation effect sizes for one metric."""
    plt = _setup_plotting()

    metric_effects = [e for e in effects if e["metric"] == metric]
    if not metric_effects:
        return

    # Sort by delta magnitude
    metric_effects.sort(key=lambda e: (e["policy"], e["delta"]))

    fig, ax = plt.subplots(
        figsize=(6, max(3, len(metric_effects) * 0.25))
    )

    y_labels = []
    for i, e in enumerate(metric_effects):
        color = "#E74C3C" if e["delta"] > 0 else "#2ECC71"
        alpha = 1.0 if e["significant"] else 0.4
        ax.plot([e["ci_lo"], e["ci_hi"]], [i, i],
                color=color, linewidth=1.5, alpha=alpha)
        ax.plot(e["delta"], i, "o", color=color, markersize=4, alpha=alpha)
        y_labels.append(f"{e['condition']} ({e['policy']})")

    ax.axvline(0, color="black", linewidth=0.5, linestyle="--")
    ax.set_yticks(range(len(metric_effects)))
    ax.set_yticklabels(y_labels, fontsize=6)
    ax.set_xlabel(f"Delta ({metric})", fontsize=8)
    ax.set_title(f"Ablation Effects: {metric}", fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, f"forest_{metric}.png"),
                dpi=200, bbox_inches="tight")
    plt.close(fig)


# ============================================================================
# Main pipeline
# ============================================================================

def main():
    args = parse_args()
    output_dir = args.output or OUTPUT_BASE
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 70)
    print("  Heuristic Baseline Aggregation")
    print("=" * 70)

    # 1. Discovery
    run_groups = discover_heuristic_runs(
        HEURISTIC_BASE, args.condition, args.policy
    )
    total_seeds = sum(len(g["seed_dirs"]) for g in run_groups.values())
    print(f"\n  Found {len(run_groups)} condition-policy combos, "
          f"{total_seeds} total runs\n")

    if not run_groups:
        print("  No runs found. Exiting.")
        return

    # 2. Process per condition-policy
    all_aggregated = {}
    all_seed_metrics = {}
    all_outcome_rows = []
    all_pattern_results = {}
    all_trajectory_data = {}

    for label, info in sorted(run_groups.items()):
        n_seeds = len(info["seed_dirs"])
        print(f"  Processing {label} ({n_seeds} seeds)...", end="", flush=True)

        seed_metrics = []
        outcome_rows = []
        histories = []

        for seed_dir in info["seed_dirs"]:
            history = load_history_jsonl(seed_dir)
            if not history:
                continue

            histories.append(history)

            # Per-run metrics
            metrics = compute_condition_metrics(history, args.last_n)
            if metrics:
                seed_metrics.append(metrics)

            # Outcome classification
            outcome = classify_outcome(history, args.last_n)
            seed_name = os.path.basename(seed_dir)
            try:
                seed_num = int(seed_name.split("_")[1])
            except (IndexError, ValueError):
                seed_num = 0
            outcome["condition"] = info["condition"]
            outcome["policy"] = info["policy"]
            outcome["seed"] = seed_num
            outcome_rows.append(outcome)

        if not seed_metrics:
            print(" SKIP (no valid runs)")
            continue

        # Cross-seed aggregation
        aggregated = aggregate_across_seeds(seed_metrics)
        all_aggregated[label] = aggregated
        all_seed_metrics[label] = seed_metrics
        all_outcome_rows.extend(outcome_rows)

        # Pattern validation
        if len(histories) >= 2:
            injected = [_inject_true_capabilities(h) for h in histories]
            try:
                all_pattern_results[label] = check_patterns(injected)
            except Exception as exc:
                print(f" (pattern check failed: {exc})", end="")

        # Trajectory quantiles
        all_trajectory_data[label] = compute_trajectory_stats(
            histories, CORE_METRIC_FNS
        )

        del histories
        print(f" OK ({len(seed_metrics)} seeds)")

    # 3. Write CSVs
    print(f"\nWriting outputs to {output_dir}/")
    write_heuristic_summary(all_aggregated, all_seed_metrics,
                            all_outcome_rows, output_dir)
    write_outcome_typology(all_outcome_rows, output_dir)
    write_pattern_matrix(all_pattern_results, output_dir)
    write_trajectory_csvs(all_trajectory_data, output_dir)

    effects = compute_ablation_effects(all_seed_metrics)
    write_ablation_effects(effects, output_dir)

    # 4. Plots
    if not args.no_plots:
        plot_dir = os.path.join(output_dir, "plots")
        os.makedirs(plot_dir, exist_ok=True)
        print(f"\nGenerating plots to {plot_dir}/")

        # Quantile trajectory plots (per metric x policy)
        metric_labels = {
            "gap": "Score-Satisfaction Gap",
            "hhi": "HHI (Market Concentration)",
            "safety": "Mean Safety Investment",
            "satisfaction": "Consumer Satisfaction",
            "incidents": "Incidents per Round",
            "reliability": "Score Reliability (rank corr)",
        }
        for mname, ylabel in metric_labels.items():
            for pol in POLICIES:
                plot_quantile_trajectories(
                    all_trajectory_data, mname, ylabel, plot_dir,
                    policy_filter=pol,
                )
        print("  Trajectory plots done")

        # Outcome heatmap
        plot_outcome_heatmap(all_outcome_rows, plot_dir)
        print("  Outcome heatmaps done")

        # Pattern heatmap
        plot_pattern_heatmap(all_pattern_results, plot_dir)
        print("  Pattern heatmap done")

        # Ablation forest plots
        for metric in ABLATION_METRICS:
            plot_ablation_forest(effects, metric, plot_dir)
        print("  Forest plots done")

    # 5. Summary
    print(f"\nDone. {len(all_aggregated)} conditions, "
          f"{total_seeds} runs aggregated.")
    n_sig = sum(1 for e in effects if e["significant"])
    print(f"  {n_sig}/{len(effects)} ablation effects significant (p<0.05)")

    # Quick top-level stats
    for pol in POLICIES:
        baseline_key = f"{BASELINE_CONDITION}_{pol}"
        if baseline_key in all_aggregated:
            agg = all_aggregated[baseline_key]
            print(f"\n  {baseline_key}:")
            print(f"    Gap={agg['total_gap']:.4f} +/- {agg.get('total_gap_se', 0):.4f}")
            print(f"    HHI={agg['hhi']:.4f}, Reliability={agg['score_reliability']:.4f}")
            print(f"    Safety={agg['mean_safety']:.4f}, Satisfaction={agg['mean_satisfaction']:.4f}")


if __name__ == "__main__":
    main()
