"""
Worked Example: Aggregation Pipeline
=====================================
Demonstrates how to go from raw run outputs (rounds.jsonl) to aggregated
cross-condition summary metrics.

Usage:
    python scripts/aggregate_example.py <batch_dir>

Example:
    python scripts/aggregate_example.py sandbox/experiments/_preserved/llm_full_ecosystem_progression

This script:
  1. Discovers all runs in the batch directory
  2. Groups them by condition (using the same logic as plot_experiment.py)
  3. Loads rounds.jsonl for each run
  4. Computes per-run metrics (gap decomposition, HHI, safety, satisfaction, etc.)
  5. Aggregates across seeds (mean +/- SE)
  6. Prints a summary table and writes T1_condition_summary.csv
"""

import argparse
import csv
import json
import os
import re
import sys
from collections import defaultdict

import numpy as np

# ============================================================
#  Step 1: Discover runs and group by condition
# ============================================================

def extract_condition_label(dirname: str) -> str:
    """Extract condition label from directory name.

    Handles format: condition_preset_mode_s{seed}_YYYYMMDD_HHMMSS
    Returns: condition_preset_mode (without seed or timestamp)
    """
    parts = dirname.rsplit("_", 2)
    if len(parts) < 3:
        return dirname
    stem = parts[0]
    if re.match(r'.*_s\d+$', stem):
        stem = stem.rsplit("_", 1)[0]
    return stem


def discover_runs(batch_dir: str) -> dict:
    """Discover all runs in a batch directory, grouped by condition.

    Returns: {condition_label: [list of run directory paths]}
    """
    by_condition = defaultdict(list)
    for name in sorted(os.listdir(batch_dir)):
        full = os.path.join(batch_dir, name)
        if not os.path.isdir(full):
            continue
        if not os.path.exists(os.path.join(full, "rounds.jsonl")):
            continue
        label = extract_condition_label(name)
        by_condition[label].append(full)
    return dict(by_condition)


# ============================================================
#  Step 2: Load round data from a single run
# ============================================================

def load_rounds(run_dir: str) -> list:
    """Load rounds.jsonl -> list of round dicts."""
    path = os.path.join(run_dir, "rounds.jsonl")
    rounds = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rounds.append(json.loads(line))
    return rounds


# ============================================================
#  Step 3: Compute per-run metrics
# ============================================================

def _get_providers(history: list) -> list:
    return list(history[0]["scores"].keys())


def _get_need_weights(history: list) -> np.ndarray:
    """Infer consumer need weights from consumer_signals (last round with data)."""
    dims = ["reasoning", "coding", "knowledge", "safety", "communication", "agentic"]
    for h in reversed(history):
        cs = h.get("consumer_signals", {})
        if cs:
            first_prov = next(iter(cs.values()), {})
            nw = first_prov.get("need_weights", {})
            if nw:
                return np.array([nw.get(d, 0.0) for d in dims])
    return np.ones(len(dims)) / len(dims)


def _to_vec(cv: dict) -> np.ndarray:
    dims = ["reasoning", "coding", "knowledge", "safety", "communication", "agentic"]
    return np.array([cv.get(d, 0.0) for d in dims])


def _get_bm_agg_weights(h: dict) -> np.ndarray:
    """Compute benchmark-aggregate dimension weights from benchmark_dimension_weights."""
    dims = ["reasoning", "coding", "knowledge", "safety", "communication", "agentic"]
    bdw = h.get("benchmark_dimension_weights", {})
    if not bdw:
        return np.ones(len(dims)) / len(dims)
    agg = np.zeros(len(dims))
    for bm, weights in bdw.items():
        overall = weights.get("overall", weights)
        for i, d in enumerate(dims):
            agg[i] += overall.get(d, 0.0)
    total = agg.sum()
    if total > 0:
        agg /= total
    return agg


def _gap_decomposition(h: dict, provider: str, need: np.ndarray) -> dict:
    """Decompose score-satisfaction gap for one provider in one round."""
    dims = ["reasoning", "coding", "knowledge", "safety", "communication", "agentic"]
    cv = h.get("capability_vectors", {}).get(provider, {})
    if not cv:
        return {"score_noise": 0, "dim_mismatch": 0, "penalty_load": 0, "total_gap": 0}

    cap = _to_vec(cv)
    bm_agg = _get_bm_agg_weights(h)
    score = h.get("scores", {}).get(provider, 0)
    sat = h.get("consumer_data", {}).get("provider_satisfaction", {}).get(provider, 0)

    bm_proj = float(np.dot(cap, bm_agg))
    need_proj = float(np.dot(cap, need))

    return {
        "score_noise": score - bm_proj,
        "dim_mismatch": bm_proj - need_proj,
        "penalty_load": need_proj - sat,
        "total_gap": score - sat,
    }


def compute_run_metrics(history: list, last_n: int = 5) -> dict:
    """Compute all aggregate metrics for a single run.

    This is the core function: takes a list of round dicts, returns one dict of metrics.
    """
    from scipy.stats import rankdata

    providers = _get_providers(history)
    need = _get_need_weights(history)
    n_rounds = len(history)
    last_rounds = history[-last_n:] if n_rounds >= last_n else history

    # --- Gap decomposition (last N rounds) ---
    score_noise_vals, dim_mismatch_vals, penalty_load_vals = [], [], []
    for h in last_rounds:
        for p in providers:
            g = _gap_decomposition(h, p, need)
            score_noise_vals.append(g["score_noise"])
            dim_mismatch_vals.append(g["dim_mismatch"])
            penalty_load_vals.append(g["penalty_load"])

    # --- Score reliability (rank correlation: score rank vs satisfaction rank) ---
    reliability_vals = []
    for h in last_rounds:
        ps = h.get("consumer_data", {}).get("provider_satisfaction", {})
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

    # --- Market concentration (HHI) ---
    hhi_vals = []
    for h in last_rounds:
        ms = h.get("consumer_data", {}).get("market_shares", {})
        if ms:
            hhi_vals.append(sum(v ** 2 for v in ms.values()))

    # --- Safety investment ---
    safety_vals = []
    for h in last_rounds:
        for p in providers:
            s = h.get("effective_strategies", h.get("strategies", {})).get(p, {}).get("safety", 0)
            safety_vals.append(s)

    # --- Incidents ---
    total_incidents = 0
    for h in history:
        risk = h.get("media_data", {}).get("risk_signals", [])
        if isinstance(risk, list):
            total_incidents += sum(1 for x in risk if isinstance(x, str) and "incident" in x)
    incidents_per_round = total_incidents / max(n_rounds, 1)

    # --- Satisfaction ---
    sat_vals = []
    for h in last_rounds:
        sat = h.get("consumer_data", {}).get("avg_satisfaction")
        if sat is not None:
            sat_vals.append(sat)

    # --- Provider differentiation (std of mean capabilities) ---
    diff_vals = []
    for h in last_rounds:
        cap_means = []
        for p in providers:
            cv = h.get("capability_vectors", {}).get(p, {})
            if cv:
                cap_means.append(sum(cv.values()) / len(cv))
        if len(cap_means) >= 2:
            diff_vals.append(float(np.std(cap_means)))

    # --- Growth-need alignment (cosine sim between capability growth and consumer needs) ---
    growth_cos_vals = []
    if len(history) >= 2:
        r0, rf = history[0], history[-1]
        for p in providers:
            cv0, cvf = r0.get("capability_vectors", {}).get(p, {}), rf.get("capability_vectors", {}).get(p, {})
            if cv0 and cvf:
                growth = _to_vec(cvf) - _to_vec(cv0)
                norm = np.linalg.norm(growth)
                if norm > 1e-8:
                    growth_cos_vals.append(float(np.dot(growth, need) / (norm * np.linalg.norm(need))))

    # --- Leader info ---
    final_ms = history[-1].get("consumer_data", {}).get("market_shares", {})
    leader = max(final_ms, key=final_ms.get) if final_ms else "N/A"
    leader_share = final_ms.get(leader, 0)

    def _mean(v): return float(np.mean(v)) if v else 0.0
    def _se(v): return float(np.std(v, ddof=1) / np.sqrt(len(v))) if len(v) >= 2 else 0.0

    return {
        "n_rounds": n_rounds,
        "leader": leader,
        "leader_share": leader_share,
        "score_noise": _mean(score_noise_vals),
        "dim_mismatch": _mean(dim_mismatch_vals),
        "penalty_load": _mean(penalty_load_vals),
        "total_gap": _mean(score_noise_vals) + _mean(dim_mismatch_vals) + _mean(penalty_load_vals),
        "score_reliability": _mean(reliability_vals),
        "hhi": _mean(hhi_vals),
        "mean_safety": _mean(safety_vals),
        "incidents_per_round": incidents_per_round,
        "mean_satisfaction": _mean(sat_vals),
        "provider_differentiation": _mean(diff_vals),
        "growth_need_alignment": _mean(growth_cos_vals),
    }


# ============================================================
#  Step 4: Aggregate across seeds
# ============================================================

def aggregate_seeds(seed_metrics: list) -> dict:
    """Aggregate per-run metrics across seeds -> mean +/- SE."""
    if len(seed_metrics) == 1:
        m = seed_metrics[0].copy()
        m["n_seeds"] = 1
        return m

    n = len(seed_metrics)
    numeric_fields = [
        "score_noise", "dim_mismatch", "penalty_load", "total_gap",
        "score_reliability", "hhi", "mean_safety", "incidents_per_round",
        "mean_satisfaction", "provider_differentiation", "growth_need_alignment",
        "leader_share",
    ]
    result = {}
    for field in numeric_fields:
        vals = [m[field] for m in seed_metrics]
        result[field] = float(np.mean(vals))
        result[f"{field}_se"] = float(np.std(vals, ddof=1) / np.sqrt(n))

    result["n_rounds"] = max(m["n_rounds"] for m in seed_metrics)
    result["n_seeds"] = n

    # Most frequent leader
    from collections import Counter
    leaders = Counter(m["leader"] for m in seed_metrics)
    result["leader"] = leaders.most_common(1)[0][0]
    result["leader_consistent"] = len(leaders) == 1

    return result


# ============================================================
#  Step 5: Print results and write CSV
# ============================================================

def print_summary(condition_results: dict):
    """Print a formatted summary table."""
    print()
    print("=" * 110)
    print("AGGREGATED CONDITION SUMMARY")
    print("=" * 110)

    header = (
        f"{'Condition':<35} {'Seeds':>5} {'Leader':<16} {'Share%':>7} "
        f"{'HHI':>7} {'ScoreNoise':>10} {'DimMis':>7} {'PenLoad':>8} "
        f"{'Safety':>7} {'Satisf':>7}"
    )
    print(header)
    print("-" * 110)

    for cond in sorted(condition_results, key=lambda c: (0 if "full_ecosystem" in c else 1, c)):
        r = condition_results[cond]
        consistent = "*" if r.get("leader_consistent", False) else ""
        print(
            f"{cond:<35} {r.get('n_seeds', 1):>5} "
            f"{r['leader'] + consistent:<16} {r['leader_share'] * 100:>6.1f}% "
            f"{r['hhi']:>7.3f} {r['score_noise']:>10.4f} {r['dim_mismatch']:>7.4f} "
            f"{r['penalty_load']:>8.4f} {r['mean_safety']:>7.3f} {r['mean_satisfaction']:>7.3f}"
        )

    print()
    print("* = consistent winner across all seeds")
    print()

    # Print SE for key metrics
    print("Standard Errors (cross-seed):")
    print(f"{'Condition':<35} {'HHI_SE':>8} {'TotalGap_SE':>12} {'Safety_SE':>10} {'Satisf_SE':>10}")
    print("-" * 75)
    for cond in sorted(condition_results, key=lambda c: (0 if "full_ecosystem" in c else 1, c)):
        r = condition_results[cond]
        if r.get("n_seeds", 1) > 1:
            print(
                f"{cond:<35} {r.get('hhi_se', 0):>8.4f} "
                f"{r.get('total_gap_se', 0):>12.4f} "
                f"{r.get('mean_safety_se', 0):>10.4f} "
                f"{r.get('mean_satisfaction_se', 0):>10.4f}"
            )


def write_csv(condition_results: dict, output_path: str):
    """Write T1_condition_summary.csv."""
    fields = [
        "condition", "n_seeds", "n_rounds", "leader", "leader_share",
        "score_noise", "dim_mismatch", "penalty_load", "total_gap",
        "score_reliability", "hhi", "mean_safety", "incidents_per_round",
        "mean_satisfaction", "provider_differentiation", "growth_need_alignment",
    ]
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for cond in sorted(condition_results):
            row = {"condition": cond}
            row.update({k: condition_results[cond].get(k, "") for k in fields if k != "condition"})
            writer.writerow(row)
    print(f"Wrote {output_path}")


# ============================================================
#  Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Aggregation pipeline worked example")
    parser.add_argument("batch_dir", help="Directory containing experiment runs")
    parser.add_argument("--output", default=None, help="Output CSV path (default: <batch_dir>/T1_condition_summary.csv)")
    parser.add_argument("--last-n", type=int, default=5, help="Number of final rounds to average over (default: 5)")
    args = parser.parse_args()

    batch_dir = args.batch_dir
    if not os.path.isdir(batch_dir):
        print(f"Error: {batch_dir} is not a directory")
        sys.exit(1)

    # Step 1: Discover
    print(f"Discovering runs in {batch_dir}...")
    runs_by_condition = discover_runs(batch_dir)
    print(f"Found {sum(len(v) for v in runs_by_condition.values())} runs across {len(runs_by_condition)} conditions:")
    for cond, dirs in sorted(runs_by_condition.items()):
        print(f"  {cond}: {len(dirs)} seeds")

    # Steps 2-4: Load, compute, aggregate
    condition_results = {}
    for cond, dirs in sorted(runs_by_condition.items()):
        seed_metrics = []
        for d in dirs:
            print(f"  Loading {os.path.basename(d)}...")
            history = load_rounds(d)
            if not history:
                print(f"    WARNING: empty rounds.jsonl, skipping")
                continue
            metrics = compute_run_metrics(history, last_n=args.last_n)
            seed_metrics.append(metrics)

        if seed_metrics:
            condition_results[cond] = aggregate_seeds(seed_metrics)

    # Step 5: Output
    print_summary(condition_results)

    output_path = args.output or os.path.join(batch_dir, "T1_condition_summary.csv")
    write_csv(condition_results, output_path)


if __name__ == "__main__":
    main()
