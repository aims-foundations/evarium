"""
Simulation Diagnostics Module

Pure-function analytics for the six diagnostic categories described in
Section 4.3 of the paper:

1. Independent replications and statistical inference
2. CRN paired comparisons
3. (Trajectory inspection — handled by diagnostic_plots.py)
4. Sensitivity analysis
5. Behavioral coherence of LLM actors
6. Pattern-oriented validation

Operates solely on JSON data from experiment directories.
No simulation imports needed.
"""

import json
import os
from pathlib import Path
from typing import Callable, Optional

import numpy as np


# ============================================================================
# Data Loading
# ============================================================================


def load_batch_manifest(batch_path: str) -> dict:
    """Load a batch manifest JSON file."""
    with open(batch_path) as f:
        return json.load(f)


def load_experiment_history(experiments_dir: str, exp_id: str) -> list:
    """Load history.json from an experiment directory."""
    path = os.path.join(experiments_dir, exp_id, "history.json")
    with open(path) as f:
        return json.load(f)


def load_batch_histories(
    batch_path: str, experiments_dir: str
) -> list[list[dict]]:
    """Load all histories for a batch.

    Returns list of N histories, each a list of round_data dicts.
    """
    manifest = load_batch_manifest(batch_path)
    return [
        load_experiment_history(experiments_dir, eid)
        for eid in manifest["experiments"]
    ]


# ============================================================================
# Metric Extraction
# ============================================================================


def extract_metric_series(
    histories: list[list[dict]],
    metric_fn: Callable[[dict], Optional[float]],
) -> np.ndarray:
    """Extract a scalar metric from each round of each replication.

    Returns np.ndarray of shape (N, T). Shorter histories are NaN-padded.
    """
    n_reps = len(histories)
    max_rounds = max(len(h) for h in histories)
    result = np.full((n_reps, max_rounds), np.nan)
    for i, history in enumerate(histories):
        for t, rd in enumerate(history):
            val = metric_fn(rd)
            if val is not None:
                result[i, t] = val
    return result


# --- Predefined metric functions ---


def metric_mean_true_capability(rd: dict) -> Optional[float]:
    caps = list(rd.get("true_capabilities", {}).values())
    return sum(caps) / len(caps) if caps else None


def metric_mean_eval_engineering(rd: dict) -> Optional[float]:
    strats = rd.get("strategies", {})
    vals = [s.get("evaluation_engineering", 0) for s in strats.values()]
    return sum(vals) / len(vals) if vals else None


def metric_mean_safety_alignment(rd: dict) -> Optional[float]:
    strats = rd.get("strategies", {})
    vals = [s.get("safety_alignment", 0) for s in strats.values()]
    return sum(vals) / len(vals) if vals else None


def metric_mean_score(rd: dict) -> Optional[float]:
    scores = list(rd.get("scores", {}).values())
    return sum(scores) / len(scores) if scores else None


def metric_mean_gaming_gap(rd: dict) -> Optional[float]:
    """Mean (score - true_capability) across providers."""
    gaps = []
    for name, score in rd.get("scores", {}).items():
        true_cap = rd.get("true_capabilities", {}).get(name)
        if true_cap is not None:
            gaps.append(score - true_cap)
    return sum(gaps) / len(gaps) if gaps else None


def metric_hhi(rd: dict) -> Optional[float]:
    """Herfindahl-Hirschman Index from market shares."""
    cd = rd.get("consumer_data", {})
    shares = cd.get("market_shares", {})
    if not shares:
        return None
    vals = list(shares.values())
    return sum(s**2 for s in vals)


def metric_consumer_satisfaction(rd: dict) -> Optional[float]:
    cd = rd.get("consumer_data", {})
    return cd.get("avg_satisfaction")


def metric_mean_benchmark_validity(rd: dict) -> Optional[float]:
    bm = rd.get("benchmark_params", {})
    if not bm:
        return None
    validities = [params["validity"] for params in bm.values()]
    return sum(validities) / len(validities) if validities else None


def metric_incident_count(rd: dict) -> float:
    return float(len(rd.get("incidents", [])))


def metric_bte_composite(rd: dict) -> Optional[float]:
    bte = rd.get("barrier_to_entry", {})
    return bte.get("composite")


# ============================================================================
# Diagnostic 1: Aggregate Replications
# ============================================================================


def aggregate_replications(
    histories: list[list[dict]],
    metric_fn: Callable[[dict], Optional[float]],
    confidence: float = 0.95,
) -> dict:
    """Compute per-round mean, SD, and CI across replications.

    Uses t-distribution for small N.

    Returns dict with keys: rounds, mean, std, ci_lower, ci_upper, n_valid.
    """
    from scipy import stats

    data = extract_metric_series(histories, metric_fn)
    _n_reps, n_rounds = data.shape

    means = np.nanmean(data, axis=0)
    stds = np.nanstd(data, axis=0, ddof=1)
    n_valid = np.sum(~np.isnan(data), axis=0)

    alpha = 1 - confidence
    ci_half = np.zeros(n_rounds)
    for t in range(n_rounds):
        n = int(n_valid[t])
        if n >= 2:
            ci_half[t] = stats.t.ppf(1 - alpha / 2, df=n - 1) * stds[t] / np.sqrt(n)

    return {
        "rounds": list(range(n_rounds)),
        "mean": means,
        "std": stds,
        "ci_lower": means - ci_half,
        "ci_upper": means + ci_half,
        "n_valid": n_valid.astype(int),
    }


# ============================================================================
# Diagnostic 2: CRN Paired Comparisons
# ============================================================================


def crn_paired_difference(
    histories_a: list[list[dict]],
    histories_b: list[list[dict]],
    metric_fn: Callable[[dict], Optional[float]],
    confidence: float = 0.95,
) -> dict:
    """Compute paired differences (A - B) across CRN-matched replications.

    Returns per-round and overall statistics.
    """
    from scipy import stats

    data_a = extract_metric_series(histories_a, metric_fn)
    data_b = extract_metric_series(histories_b, metric_fn)

    min_rounds = min(data_a.shape[1], data_b.shape[1])
    data_a = data_a[:, :min_rounds]
    data_b = data_b[:, :min_rounds]

    diffs = data_a - data_b
    mean_diff = np.nanmean(diffs, axis=0)
    std_diff = np.nanstd(diffs, axis=0, ddof=1)
    n_valid = np.sum(~np.isnan(diffs), axis=0)

    alpha = 1 - confidence
    ci_half = np.zeros(min_rounds)
    t_stats = np.zeros(min_rounds)
    p_values = np.ones(min_rounds)
    for t in range(min_rounds):
        n = int(n_valid[t])
        if n >= 2:
            se = std_diff[t] / np.sqrt(n)
            t_stats[t] = mean_diff[t] / se if se > 0 else 0
            p_values[t] = 2 * stats.t.sf(abs(t_stats[t]), df=n - 1)
            ci_half[t] = stats.t.ppf(1 - alpha / 2, df=n - 1) * se

    # Overall summary
    overall_diffs = np.nanmean(diffs, axis=1)
    n_overall = int(np.sum(~np.isnan(overall_diffs)))
    if n_overall >= 2:
        overall_mean = float(np.nanmean(overall_diffs))
        overall_se = float(np.nanstd(overall_diffs, ddof=1) / np.sqrt(n_overall))
        overall_t = overall_mean / overall_se if overall_se > 0 else 0
        overall_p = float(2 * stats.t.sf(abs(overall_t), df=n_overall - 1))
    else:
        overall_mean = overall_t = overall_p = None

    return {
        "rounds": list(range(min_rounds)),
        "mean_diff": mean_diff,
        "std_diff": std_diff,
        "ci_lower": mean_diff - ci_half,
        "ci_upper": mean_diff + ci_half,
        "t_stat": t_stats,
        "p_value": p_values,
        "overall": {
            "mean_diff": overall_mean,
            "t_stat": overall_t,
            "p_value": overall_p,
        },
    }


# ============================================================================
# Utilities
# ============================================================================


def compute_hhi(market_shares: dict) -> float:
    """Compute Herfindahl-Hirschman Index. 1/N = equal, 1 = monopoly."""
    vals = list(market_shares.values())
    if not vals:
        return 0.0
    return sum(s**2 for s in vals)


# ============================================================================
# Diagnostic 4: Sensitivity Analysis
# ============================================================================


def sensitivity_analysis(
    batch_manifest: dict,
    experiments_dir: str,
    metric_fn: Callable[[dict], Optional[float]],
    summary_fn: Callable[[np.ndarray], float] = None,
) -> dict:
    """Compute effect sizes for a one-at-a-time sensitivity sweep.

    Returns param_name, baseline info, and per-perturbation metrics/effects.
    """
    if summary_fn is None:
        summary_fn = np.nanmean

    params_varied = batch_manifest["parameters_varied"]
    param_name = list(params_varied.keys())[0]
    param_sweep = params_varied[param_name]

    base_config_path = os.path.join(
        experiments_dir, batch_manifest["base_config"], "config.json"
    )
    with open(base_config_path) as f:
        base_config = json.load(f)
    baseline_value = base_config.get(param_name)

    results = {
        "param_name": param_name,
        "baseline_value": baseline_value,
        "perturbations": [],
    }

    for value_str, exp_ids in param_sweep.items():
        value = float(value_str)
        histories = [
            load_experiment_history(experiments_dir, eid) for eid in exp_ids
        ]
        series = extract_metric_series(histories, metric_fn)
        rep_summaries = np.array(
            [summary_fn(series[i]) for i in range(series.shape[0])]
        )
        results["perturbations"].append(
            {
                "value": value,
                "metric_mean": float(np.nanmean(rep_summaries)),
                "metric_std": float(np.nanstd(rep_summaries, ddof=1))
                if len(rep_summaries) > 1
                else 0.0,
            }
        )

    baseline_pert = [
        p
        for p in results["perturbations"]
        if baseline_value is not None and abs(p["value"] - baseline_value) < 1e-10
    ]
    results["baseline_metric"] = (
        baseline_pert[0]["metric_mean"] if baseline_pert else None
    )

    if results["baseline_metric"] is not None:
        for p in results["perturbations"]:
            p["effect"] = p["metric_mean"] - results["baseline_metric"]

    return results


# ============================================================================
# Diagnostic 5: Behavioral Coherence of LLM Actors
# ============================================================================


def detect_strategy_drift(
    history: list[dict],
    provider_name: str,
    window: int = 5,
) -> list[float]:
    """Detect strategy drift via cosine distance from rolling-window mean.

    Returns list of drift scores (one per round, NaN for early rounds).
    """
    allocations = []
    for rd in history:
        strat = rd.get("strategies", {}).get(provider_name, {})
        if strat:
            vec = np.array(
                [
                    strat.get("fundamental_research", 0),
                    strat.get("training_optimization", 0),
                    strat.get("evaluation_engineering", 0),
                    strat.get("safety_alignment", 0),
                ]
            )
            allocations.append(vec)
        else:
            allocations.append(np.full(4, np.nan))

    drift_scores = []
    for t in range(len(allocations)):
        if t < window:
            drift_scores.append(float("nan"))
            continue
        window_vecs = np.array(allocations[t - window : t])
        if np.any(np.isnan(window_vecs)):
            drift_scores.append(float("nan"))
            continue
        mean_vec = np.mean(window_vecs, axis=0)
        current = allocations[t]
        dot = np.dot(current, mean_vec)
        norm_a = np.linalg.norm(current)
        norm_b = np.linalg.norm(mean_vec)
        if norm_a > 0 and norm_b > 0:
            cos_sim = dot / (norm_a * norm_b)
            drift_scores.append(1.0 - cos_sim)
        else:
            drift_scores.append(float("nan"))

    return drift_scores


def detect_strategy_drift_all_providers(
    history: list[dict], window: int = 5
) -> dict[str, list[float]]:
    """Compute strategy drift for all providers in a history."""
    providers = set()
    for rd in history:
        providers.update(rd.get("strategies", {}).keys())
    return {
        name: detect_strategy_drift(history, name, window)
        for name in sorted(providers)
    }


def check_role_adherence(
    history: list[dict],
    forbidden_terms: list[str] = None,
) -> list[dict]:
    """Scan actor_traces for ground-truth information leakage.

    Returns list of violation dicts with round, actor, term, and excerpt.
    """
    if forbidden_terms is None:
        forbidden_terms = [
            "true capability",
            "true_capability",
            "ground truth",
            "ground_truth",
            "actual capability",
            "hidden state",
            "real capability",
        ]

    violations = []
    for rd in history:
        traces = rd.get("actor_traces", {})
        for actor_name, trace_text in traces.items():
            if not isinstance(trace_text, str):
                continue
            trace_lower = trace_text.lower()
            for term in forbidden_terms:
                if term.lower() in trace_lower:
                    idx = trace_lower.index(term.lower())
                    start = max(0, idx - 50)
                    end = min(len(trace_text), idx + len(term) + 150)
                    violations.append(
                        {
                            "round": rd.get("round"),
                            "actor": actor_name,
                            "term_found": term,
                            "trace_excerpt": trace_text[start:end],
                        }
                    )
    return violations


def analyze_prompt_sensitivity(
    histories: list[list[dict]],
    provider_name: str,
) -> dict:
    """Measure cross-replication variance in investment decisions.

    Returns per-round SD for each investment category + summary.
    """
    categories = [
        "fundamental_research",
        "training_optimization",
        "evaluation_engineering",
        "safety_alignment",
    ]

    result = {cat: [] for cat in categories}
    max_rounds = max(len(h) for h in histories)

    for t in range(max_rounds):
        for cat in categories:
            vals = []
            for history in histories:
                if t < len(history):
                    strat = (
                        history[t].get("strategies", {}).get(provider_name, {})
                    )
                    if cat in strat:
                        vals.append(strat[cat])
            if len(vals) >= 2:
                result[cat].append(float(np.std(vals, ddof=1)))
            else:
                result[cat].append(float("nan"))

    summary = {}
    for cat in categories:
        vals = [v for v in result[cat] if not np.isnan(v)]
        summary[cat] = float(np.mean(vals)) if vals else None

    result["summary"] = summary
    return result


# ============================================================================
# Diagnostic 6: Pattern-Oriented Validation
# ============================================================================


def check_patterns(histories: list[list[dict]]) -> dict:
    """Run pattern-oriented validation checks across replications.

    Returns {pattern_name: {passed: bool, fraction: float, details: str}}.
    A pattern passes if it holds in >= 50% of replications.
    """
    n = len(histories)
    checks = {
        "benchmark_turnover": _check_benchmark_turnover,
        "score_inflation": _check_score_inflation,
        "safety_incident_response": _check_safety_responds_to_incidents,
        "gaming_persistence": _check_gaming_persistence,
        "commoditization_shock": _check_commoditization_shock,
        "regulatory_escalation": _check_regulatory_escalation,
        "funding_follows_scores": _check_funding_follows_scores,
    }

    results = {}
    for name, fn in checks.items():
        count = sum(1 for h in histories if fn(h))
        results[name] = {
            "passed": count / n >= 0.5,
            "fraction": count / n,
            "details": f"{count}/{n} replications",
        }

    return results


def _check_benchmark_turnover(history: list[dict]) -> bool:
    for rd in history:
        if "new_benchmark" in rd:
            return True
    return False


def _check_score_inflation(history: list[dict]) -> bool:
    gaps = [metric_mean_gaming_gap(rd) for rd in history]
    gaps = [g for g in gaps if g is not None]
    if len(gaps) < 10:
        return False
    mid = len(gaps) // 2
    return np.mean(gaps[mid:]) > np.mean(gaps[:mid])


def _check_safety_responds_to_incidents(history: list[dict]) -> bool:
    responded = 0
    total_events = 0
    for t, rd in enumerate(history):
        incidents = rd.get("incidents", [])
        severe = [
            inc
            for inc in incidents
            if inc.get("severity") in ("major", "critical")
        ]
        for inc in severe:
            provider = inc.get("provider")
            if not provider:
                continue
            total_events += 1
            before = (
                rd.get("strategies", {})
                .get(provider, {})
                .get("safety_alignment", 0)
            )
            for dt in range(1, 3):
                if t + dt < len(history):
                    after = (
                        history[t + dt]
                        .get("strategies", {})
                        .get(provider, {})
                        .get("safety_alignment", 0)
                    )
                    if after > before + 0.01:
                        responded += 1
                        break
    if total_events == 0:
        return True  # vacuously true
    return responded / total_events >= 0.3


def _check_gaming_persistence(history: list[dict]) -> bool:
    vals = [metric_mean_eval_engineering(rd) for rd in history]
    vals = [v for v in vals if v is not None]
    return np.mean(vals) >= 0.10 if vals else False


def _check_commoditization_shock(history: list[dict]) -> bool:
    for rd in history:
        os_data = rd.get("open_source_data")
        if isinstance(os_data, dict):
            for _name, data in os_data.items():
                if isinstance(data, dict) and data.get(
                    "commoditization_shock_fired"
                ):
                    return True
    return False


def _check_regulatory_escalation(history: list[dict]) -> bool:
    ORDERING = {
        "investigation": 0,
        "public_warning": 1,
        "benchmark_mandate": 2,
        "compliance_audit": 3,
        "sanctions_and_fines": 4,
        "emergency_investigation": 5,
    }
    interventions = []
    for rd in history:
        pm_data = rd.get("policymaker_data", {})
        for iv in pm_data.get("interventions", []):
            interventions.append(iv.get("type", ""))
    ordered = [ORDERING[iv] for iv in interventions if iv in ORDERING]
    if len(ordered) < 2:
        return True
    return ordered[0] < max(ordered)


def _check_funding_follows_scores(history: list[dict]) -> bool:
    score_vals, cap_vals, funding_vals = [], [], []
    for rd in history:
        fd = rd.get("funder_data", {})
        mults = fd.get("funding_multipliers", {})
        if not mults:
            continue
        for name in mults:
            if name in rd.get("scores", {}) and name in rd.get(
                "true_capabilities", {}
            ):
                score_vals.append(rd["scores"][name])
                cap_vals.append(rd["true_capabilities"][name])
                funding_vals.append(mults[name])
    if len(score_vals) < 10:
        return True  # not enough data
    corr_score = np.corrcoef(score_vals, funding_vals)[0, 1]
    corr_cap = np.corrcoef(cap_vals, funding_vals)[0, 1]
    return corr_score > corr_cap


# ============================================================================
# Top-Level Orchestrator
# ============================================================================


def analyze_batch(
    batch_path: str,
    experiments_dir: str,
    output_dir: str,
) -> dict:
    """Run full diagnostic analysis on a batch.

    Saves aggregate_stats.json, pattern_results.json, coherence_report.json,
    and diagnostic_report.md to output_dir.
    """
    manifest = load_batch_manifest(batch_path)
    histories = load_batch_histories(batch_path, experiments_dir)

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "plots"), exist_ok=True)

    results = {
        "batch_name": manifest["batch_name"],
        "n_replications": len(histories),
    }

    # --- Aggregate stats ---
    key_metrics = {
        "mean_true_capability": metric_mean_true_capability,
        "mean_eval_engineering": metric_mean_eval_engineering,
        "mean_safety_alignment": metric_mean_safety_alignment,
        "mean_score": metric_mean_score,
        "mean_gaming_gap": metric_mean_gaming_gap,
        "hhi": metric_hhi,
        "consumer_satisfaction": metric_consumer_satisfaction,
        "mean_benchmark_validity": metric_mean_benchmark_validity,
        "incident_count": metric_incident_count,
    }

    aggregate = {}
    for name, fn in key_metrics.items():
        agg = aggregate_replications(histories, fn)
        aggregate[name] = {
            "mean": agg["mean"].tolist(),
            "std": agg["std"].tolist(),
            "ci_lower": agg["ci_lower"].tolist(),
            "ci_upper": agg["ci_upper"].tolist(),
        }
    results["aggregate_stats"] = aggregate

    with open(os.path.join(output_dir, "aggregate_stats.json"), "w") as f:
        json.dump(aggregate, f, indent=2)

    # --- Pattern validation ---
    patterns = check_patterns(histories)
    results["patterns"] = patterns

    with open(os.path.join(output_dir, "pattern_results.json"), "w") as f:
        json.dump(patterns, f, indent=2)

    # --- Behavioral coherence ---
    coherence = {
        "strategy_drift": {},
        "role_adherence_violations": [],
        "prompt_sensitivity": {},
    }

    for i, history in enumerate(histories):
        drift = detect_strategy_drift_all_providers(history)
        for provider, scores in drift.items():
            if provider not in coherence["strategy_drift"]:
                coherence["strategy_drift"][provider] = []
            valid_scores = [s for s in scores if not np.isnan(s)]
            coherence["strategy_drift"][provider].append(
                {
                    "replication": i,
                    "mean_drift": float(np.mean(valid_scores))
                    if valid_scores
                    else None,
                    "max_drift": float(max(valid_scores))
                    if valid_scores
                    else None,
                }
            )

        violations = check_role_adherence(history)
        for v in violations:
            v["replication"] = i
        coherence["role_adherence_violations"].extend(violations)

    providers = set()
    for h in histories:
        for rd in h:
            providers.update(rd.get("strategies", {}).keys())
    for provider_name in sorted(providers):
        ps = analyze_prompt_sensitivity(histories, provider_name)
        coherence["prompt_sensitivity"][provider_name] = ps.get("summary", {})

    results["coherence"] = coherence

    with open(os.path.join(output_dir, "coherence_report.json"), "w") as f:
        json.dump(coherence, f, indent=2, default=str)

    # --- Markdown report ---
    _write_diagnostic_report(results, output_dir)

    return results


def _write_diagnostic_report(results: dict, output_dir: str):
    """Write a human-readable diagnostic report."""
    lines = [
        f"# Diagnostic Report: {results['batch_name']}",
        f"",
        f"Replications: {results['n_replications']}",
        f"",
        f"## Pattern-Oriented Validation",
        f"",
    ]
    for name, info in results.get("patterns", {}).items():
        status = "PASS" if info["passed"] else "FAIL"
        lines.append(
            f"- **{name.replace('_', ' ').title()}**: "
            f"{status} ({info['fraction']:.0%} of replications) -- {info['details']}"
        )

    lines.extend(["", "## Behavioral Coherence", ""])

    violations = results.get("coherence", {}).get(
        "role_adherence_violations", []
    )
    if violations:
        lines.append(f"**Role adherence violations**: {len(violations)}")
        for v in violations[:10]:
            lines.append(
                f"  - Round {v['round']}, {v['actor']}: "
                f"found '{v['term_found']}'"
            )
    else:
        lines.append("**Role adherence**: No violations detected.")

    lines.extend(["", "## Prompt Sensitivity (mean cross-replication SD)", ""])
    ps = results.get("coherence", {}).get("prompt_sensitivity", {})
    for provider, summary in ps.items():
        if isinstance(summary, dict):
            ee = summary.get("evaluation_engineering")
            sa = summary.get("safety_alignment")
            lines.append(
                f"- **{provider}**: eval_eng SD={ee:.3f}, safety SD={sa:.3f}"
                if ee is not None and sa is not None
                else f"- **{provider}**: insufficient data"
            )

    report_path = os.path.join(output_dir, "diagnostic_report.md")
    with open(report_path, "w") as f:
        f.write("\n".join(lines))
