"""
aggregate_llm.py -- Extraction pipeline for LLM ecosystem runs.

Mirrors the structure of aggregate_heuristic.py but adapted to LLM specifics:
- N=1 per cell (no SE/CI/t-tests)
- Reasoning traces present in actor_traces (heuristic runs have none)
- Outputs include pivotal events, incident-response profiles, and cross-cutting
  joins against the existing heuristic baseline.

Outputs (all under output/llm_analysis/):
  - llm_summary.csv             (one row per run, endpoint metrics)
  - llm_outcome_typology.csv    (one row per run, market winner/structure/pathway)
  - llm_trajectory_data/*.csv   (per-round time series for 6 core metrics)
  - llm_pivotal_events.csv      (flat pivotal events across all runs)
  - llm_pivotal_events.jsonl    (same events + reasoning trace excerpts)
  - llm_incident_response.csv   (incident-response validation table)
  - llm_vs_heuristic_outcomes.csv (cross-comparison join)
  - evaluator_case_study.csv    (full_ecosystem vs dynamic_evaluator paired)
  - <seed_dir>/reasoning_analysis.md (per-run human-readable narrative)

Usage:
  python scripts/aggregate_llm.py
  python scripts/aggregate_llm.py --condition full_ecosystem
  python scripts/aggregate_llm.py --condition full_ecosystem --policy balanced --seed 221
  python scripts/aggregate_llm.py --skip-reasoning-md  (skip per-run MD report generation)
"""

import argparse
import csv
import json
import os
import sys
from collections import Counter, defaultdict

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(_PROJECT_ROOT, "src"))
sys.path.insert(0, os.path.join(_PROJECT_ROOT, "scripts"))

# Reuse from existing pipelines
from aggregate.heuristic import (
    parse_condition_policy,
    discover_heuristic_runs,
    load_history_jsonl,
    compute_condition_metrics,
    classify_outcome,
    CORE_METRIC_FNS,
)
from reasoning_pipeline import (
    detect_pivotal_rounds,
    extract_reasoning_windows,
    extract_strategic_arcs,
    extract_funder_arcs,
    generate_report,
)

LLM_BASE = os.path.join(_PROJECT_ROOT, "sandbox", "experiments", "llm")
HEURISTIC_OUTCOMES_CSV = os.path.join(
    _PROJECT_ROOT, "output", "heuristic_analysis", "outcome_typology.csv"
)
OUTPUT_BASE = os.path.join(_PROJECT_ROOT, "output", "llm_analysis")

# Filter threshold for incident-response table: minimum incident_penalty
# magnitude to count as "major" enough to record. From stakeholders.md the
# severity weights are minor=0.01, moderate=0.05, major=0.10, critical=0.20.
# A 0.05 floor catches moderate and above.
INCIDENT_PENALTY_FLOOR = 0.05


# ============================================================================
# CLI
# ============================================================================

def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--condition", type=str, default=None,
                   help="Filter to specific condition")
    p.add_argument("--policy", type=str, default=None,
                   help="Filter to specific policy (balanced/us/eu)")
    p.add_argument("--seed", type=int, default=None,
                   help="Filter to specific seed")
    p.add_argument("--last-n", type=int, default=5,
                   help="Number of final rounds for endpoint metrics")
    p.add_argument("--skip-reasoning-md", action="store_true",
                   help="Skip per-run reasoning_analysis.md generation")
    p.add_argument("-o", "--output", type=str, default=None,
                   help="Output directory override")
    return p.parse_args()


# ============================================================================
# Per-run extraction
# ============================================================================

def _seed_from_dir(seed_dir: str) -> int:
    """Extract seed integer from path '.../seeds/seed_<N>'."""
    base = os.path.basename(seed_dir.rstrip(os.sep))
    if base.startswith("seed_"):
        try:
            return int(base.split("_", 1)[1])
        except (ValueError, IndexError):
            return -1
    return -1


def compute_trajectory_single(history: list) -> dict:
    """Per-round series for the 6 core metrics for a single run.

    Returns {metric_name: [val_per_round]} (NaN where metric is None).
    """
    result = {}
    for name, fn in CORE_METRIC_FNS.items():
        vals = []
        for rd in history:
            v = fn(rd)
            vals.append(float(v) if v is not None else float("nan"))
        result[name] = vals
    return result


def extract_incident_response(
    history: list, condition: str, policy: str, seed: int
) -> list:
    """Extract incident-response profiles per trace_analysis_plan.md Section 1.

    For each round whose risk_signals contain an incident_* token AND whose
    max incident_penalty exceeds INCIDENT_PENALTY_FLOOR, build one record per
    affected provider.
    """
    rows = []
    n = len(history)

    def _safety(rd_idx, prov):
        if rd_idx < 0 or rd_idx >= n:
            return None
        s = history[rd_idx].get("effective_strategies", {}).get(prov, {})
        return s.get("safety")

    def _share(rd_idx, prov):
        if rd_idx < 0 or rd_idx >= n:
            return None
        s = history[rd_idx].get("consumer_data", {}).get("market_shares", {})
        return s.get(prov)

    def _funding(rd_idx, prov):
        if rd_idx < 0 or rd_idx >= n:
            return None
        f = history[rd_idx].get("funder_data", {}).get("provider_funding_totals", {})
        return f.get(prov)

    for i, rd in enumerate(history):
        round_num = rd.get("round", i)
        media = rd.get("media_data", {}) or {}
        risk_signals = media.get("risk_signals", []) or []

        incidents = []
        if isinstance(risk_signals, list):
            incidents = [x for x in risk_signals
                         if isinstance(x, str) and "incident" in x]
        elif isinstance(risk_signals, dict):
            incidents = [k for k, v in risk_signals.items()
                         if v and "incident" in k]
        if not incidents:
            continue

        # Find hit provider via penalty_breakdown
        penalties = rd.get("consumer_data", {}).get("penalty_breakdown", {}) or {}
        hit_provider = None
        max_penalty = 0.0
        for p, pb in penalties.items():
            pen = (pb or {}).get("incident_penalty", 0) or 0
            if pen > max_penalty:
                max_penalty = pen
                hit_provider = p

        if hit_provider is None or max_penalty < INCIDENT_PENALTY_FLOOR:
            continue

        incident_type = ",".join(sorted(set(incidents)))

        # Safety alloc delta N -> N+1
        safety_at = _safety(i, hit_provider)
        safety_next = _safety(i + 1, hit_provider)
        safety_change = (
            float(safety_next - safety_at)
            if (safety_at is not None and safety_next is not None)
            else None
        )

        # Share delta N-1 -> N
        share_prev = _share(i - 1, hit_provider)
        share_at = _share(i, hit_provider)
        share_change = (
            float(share_at - share_prev)
            if (share_prev is not None and share_at is not None)
            else None
        )

        # Recovery rounds: forward search until share returns to share_prev - 0.5*loss
        recovery_rounds = None
        if share_prev is not None and share_at is not None and share_change is not None and share_change < 0:
            target = share_prev + 0.5 * share_change  # share_change is negative
            for j in range(i + 1, n):
                s = _share(j, hit_provider)
                if s is not None and s >= target:
                    recovery_rounds = j - i
                    break

        # Regulator interventions issued at round N (collect types)
        interventions = rd.get("regulator_data", {}).get("interventions", []) or []
        intv_types = []
        for it in interventions:
            t = it.get("type") or it.get("action") or "unknown"
            intv_types.append(t)
        regulator_action = ",".join(intv_types) if intv_types else ""

        # Funder funding delta N-1 -> N+2
        fund_prev = _funding(i - 1, hit_provider)
        fund_post = _funding(i + 2, hit_provider)
        fund_change = (
            float(fund_post - fund_prev)
            if (fund_prev is not None and fund_post is not None)
            else None
        )

        # Provider reasoning excerpt at round N+1
        next_round = history[i + 1] if i + 1 < n else {}
        traces_next = next_round.get("actor_traces", {}) or {}
        reasoning = (traces_next.get(hit_provider) or "")[:500]

        rows.append({
            "condition": condition,
            "policy": policy,
            "seed": seed,
            "round": round_num,
            "hit_provider": hit_provider,
            "incident_type": incident_type,
            "incident_penalty": round(max_penalty, 4),
            "safety_change_pp": (round(safety_change, 4)
                                 if safety_change is not None else ""),
            "share_change_pp": (round(share_change, 4)
                                if share_change is not None else ""),
            "recovery_rounds": (recovery_rounds
                                if recovery_rounds is not None else ""),
            "regulator_action_at_round": regulator_action,
            "funder_change": (round(fund_change, 2)
                              if fund_change is not None else ""),
            "provider_reasoning_excerpt": reasoning.replace("\n", " ").replace("\r", " "),
        })

    return rows


def process_run(seed_dir: str, condition: str, policy: str,
                last_n: int, skip_reasoning_md: bool) -> dict:
    """Run all per-run extractions for one seed directory.

    Returns a dict bundling all results for cross-run aggregation.
    """
    seed = _seed_from_dir(seed_dir)
    history = load_history_jsonl(seed_dir)
    if not history:
        return {
            "seed": seed, "condition": condition, "policy": policy,
            "history": [], "metrics": {}, "outcome": {},
            "trajectory": {}, "events": [], "windows": [],
            "incident_rows": [],
        }

    metrics = compute_condition_metrics(history, last_n=last_n)
    outcome = classify_outcome(history, last_n=last_n)
    trajectory = compute_trajectory_single(history)
    events = detect_pivotal_rounds(history)
    windows = extract_reasoning_windows(history, events, context_window=2)
    incident_rows = extract_incident_response(history, condition, policy, seed)

    if not skip_reasoning_md:
        try:
            arcs = extract_strategic_arcs(history)
            funder_arcs = extract_funder_arcs(history)
            report = generate_report(history, events, windows, arcs, funder_arcs)
            md_path = os.path.join(seed_dir, "reasoning_analysis.md")
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(report)
        except Exception as e:
            print(f"  WARNING: failed to write reasoning_analysis.md "
                  f"for {seed_dir}: {e}")

    return {
        "seed": seed,
        "condition": condition,
        "policy": policy,
        "history": history,
        "metrics": metrics,
        "outcome": outcome,
        "trajectory": trajectory,
        "events": events,
        "windows": windows,
        "incident_rows": incident_rows,
    }


# ============================================================================
# CSV writers
# ============================================================================

SUMMARY_FIELDS = [
    "condition", "policy", "seed", "n_rounds",
    "total_gap", "score_noise", "dim_mismatch", "penalty_load",
    "score_reliability", "hhi", "mean_safety",
    "incidents_per_round", "mean_satisfaction",
    "provider_differentiation", "growth_need_alignment",
    "market_winner", "winner_share", "market_structure", "leader_pathway",
]


def write_llm_summary(runs: list, output_dir: str):
    path = os.path.join(output_dir, "llm_summary.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=SUMMARY_FIELDS)
        w.writeheader()
        for run in sorted(runs, key=lambda r: (r["condition"], r["policy"], r["seed"])):
            m = run["metrics"]
            o = run["outcome"]
            row = {
                "condition": run["condition"],
                "policy": run["policy"],
                "seed": run["seed"],
                "n_rounds": m.get("n_rounds", len(run["history"])),
                "total_gap": round(m.get("total_gap", 0.0), 6),
                "score_noise": round(m.get("score_noise", 0.0), 6),
                "dim_mismatch": round(m.get("dim_mismatch", 0.0), 6),
                "penalty_load": round(m.get("penalty_load", 0.0), 6),
                "score_reliability": round(m.get("score_reliability", 0.0), 6),
                "hhi": round(m.get("hhi", 0.0), 6),
                "mean_safety": round(m.get("mean_safety", 0.0), 6),
                "incidents_per_round": round(m.get("incidents_per_round", 0.0), 6),
                "mean_satisfaction": round(m.get("mean_satisfaction", 0.0), 6),
                "provider_differentiation": round(
                    m.get("provider_differentiation", 0.0), 6),
                "growth_need_alignment": round(
                    m.get("growth_need_alignment", 0.0), 6),
                "market_winner": o.get("market_winner", ""),
                "winner_share": o.get("winner_share", 0.0),
                "market_structure": o.get("market_structure", ""),
                "leader_pathway": o.get("leader_pathway", ""),
            }
            w.writerow(row)
    print(f"  Wrote {path} ({len(runs)} runs)")


OUTCOME_FIELDS = [
    "condition", "policy", "seed", "market_winner", "winner_share",
    "market_structure", "hhi", "leader_pathway",
    "leader_rd", "leader_safety", "leader_product", "final_gap",
]


def write_llm_outcomes(runs: list, output_dir: str):
    path = os.path.join(output_dir, "llm_outcome_typology.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=OUTCOME_FIELDS)
        w.writeheader()
        for run in sorted(runs, key=lambda r: (r["condition"], r["policy"], r["seed"])):
            o = run["outcome"]
            row = {
                "condition": run["condition"],
                "policy": run["policy"],
                "seed": run["seed"],
                "market_winner": o.get("market_winner", ""),
                "winner_share": o.get("winner_share", 0.0),
                "market_structure": o.get("market_structure", ""),
                "hhi": o.get("hhi", 0.0),
                "leader_pathway": o.get("leader_pathway", ""),
                "leader_rd": o.get("leader_rd", 0.0),
                "leader_safety": o.get("leader_safety", 0.0),
                "leader_product": o.get("leader_product", 0.0),
                "final_gap": o.get("final_gap", 0.0),
            }
            w.writerow(row)
    print(f"  Wrote {path}")


def write_llm_trajectories(runs: list, output_dir: str):
    traj_dir = os.path.join(output_dir, "llm_trajectory_data")
    os.makedirs(traj_dir, exist_ok=True)
    metric_names = list(CORE_METRIC_FNS.keys())
    fields = ["round"] + metric_names

    for run in runs:
        if not run["trajectory"]:
            continue
        label = f"{run['condition']}_{run['policy']}_seed{run['seed']}"
        path = os.path.join(traj_dir, f"{label}.csv")
        n_rounds = len(next(iter(run["trajectory"].values())))
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            for t in range(n_rounds):
                row = {"round": t}
                for mname in metric_names:
                    vals = run["trajectory"].get(mname, [])
                    v = vals[t] if t < len(vals) else float("nan")
                    row[mname] = "" if (v != v) else round(v, 6)  # NaN check
                w.writerow(row)

    print(f"  Wrote {len(runs)} trajectory CSVs to {traj_dir}")


PIVOTAL_CSV_FIELDS = [
    "condition", "policy", "seed", "round", "provider",
    "event_type", "details_json",
]


def write_pivotal_events(runs: list, output_dir: str):
    csv_path = os.path.join(output_dir, "llm_pivotal_events.csv")
    jsonl_path = os.path.join(output_dir, "llm_pivotal_events.jsonl")

    n_events = 0
    with open(csv_path, "w", newline="", encoding="utf-8") as cf, \
         open(jsonl_path, "w", encoding="utf-8") as jf:
        w = csv.DictWriter(cf, fieldnames=PIVOTAL_CSV_FIELDS)
        w.writeheader()

        for run in runs:
            events = run["events"]
            windows = run["windows"]
            # events and windows are 1:1 ordered
            for ev, win in zip(events, windows):
                row = {
                    "condition": run["condition"],
                    "policy": run["policy"],
                    "seed": run["seed"],
                    "round": ev.round,
                    "provider": ev.provider,
                    "event_type": ev.event_type,
                    "details_json": json.dumps(ev.details, sort_keys=True),
                }
                w.writerow(row)

                rec = {
                    "condition": run["condition"],
                    "policy": run["policy"],
                    "seed": run["seed"],
                    "round": ev.round,
                    "provider": ev.provider,
                    "event_type": ev.event_type,
                    "details": ev.details,
                    "reasoning_at": win.get("reasoning_at", ""),
                    "reasoning_before": win.get("reasoning_before", []),
                    "public_context": win.get("public_context", {}),
                }
                jf.write(json.dumps(rec, ensure_ascii=False) + "\n")
                n_events += 1

    print(f"  Wrote {csv_path} and {jsonl_path} ({n_events} events)")


INCIDENT_FIELDS = [
    "condition", "policy", "seed", "round",
    "hit_provider", "incident_type", "incident_penalty",
    "safety_change_pp", "share_change_pp", "recovery_rounds",
    "regulator_action_at_round", "funder_change",
    "provider_reasoning_excerpt",
]


def write_incident_response(runs: list, output_dir: str):
    path = os.path.join(output_dir, "llm_incident_response.csv")
    rows = []
    for run in runs:
        rows.extend(run["incident_rows"])
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=INCIDENT_FIELDS)
        w.writeheader()
        for row in sorted(rows, key=lambda r: (r["condition"], r["policy"],
                                               r["seed"], r["round"])):
            w.writerow(row)
    print(f"  Wrote {path} ({len(rows)} incidents)")


# ============================================================================
# Cross-cut: LLM vs heuristic outcome comparison
# ============================================================================

VS_HEURISTIC_FIELDS = [
    "condition", "policy", "n_heuristic", "n_llm",
    "llm_winner", "llm_structure", "llm_pathway", "llm_hhi",
    "heuristic_modal_winner", "heuristic_modal_winner_freq",
    "heuristic_competitive_n", "heuristic_moderate_n",
    "heuristic_concentrated_n",
    "heuristic_modal_pathway", "heuristic_modal_pathway_freq",
]


def load_heuristic_outcomes(csv_path: str) -> list:
    if not os.path.exists(csv_path):
        return []
    with open(csv_path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_vs_heuristic(runs: list, output_dir: str):
    """Join per-(condition, policy) LLM runs against heuristic distribution."""
    heuristic_rows = load_heuristic_outcomes(HEURISTIC_OUTCOMES_CSV)
    if not heuristic_rows:
        print(f"  WARNING: heuristic outcome CSV not found at "
              f"{HEURISTIC_OUTCOMES_CSV} -- skipping vs-heuristic comparison")
        return

    # Group heuristic by (condition, policy)
    heur_by_cell = defaultdict(list)
    for r in heuristic_rows:
        heur_by_cell[(r["condition"], r["policy"])].append(r)

    # Group LLM by (condition, policy)
    llm_by_cell = defaultdict(list)
    for run in runs:
        llm_by_cell[(run["condition"], run["policy"])].append(run)

    path = os.path.join(output_dir, "llm_vs_heuristic_outcomes.csv")
    n_written = 0
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=VS_HEURISTIC_FIELDS)
        w.writeheader()

        for (cond, pol), llm_runs in sorted(llm_by_cell.items()):
            heur = heur_by_cell.get((cond, pol), [])
            if not heur:
                continue

            structure_counts = Counter(r["market_structure"] for r in heur)
            winner_counts = Counter(r["market_winner"] for r in heur)
            pathway_counts = Counter(r["leader_pathway"] for r in heur)
            modal_winner, modal_winner_n = winner_counts.most_common(1)[0]
            modal_pathway, modal_pathway_n = pathway_counts.most_common(1)[0]

            # Aggregate LLM side: with N=1 mostly, just emit per-seed rows
            for run in llm_runs:
                o = run["outcome"]
                row = {
                    "condition": cond,
                    "policy": pol,
                    "n_heuristic": len(heur),
                    "n_llm": len(llm_runs),
                    "llm_winner": o.get("market_winner", ""),
                    "llm_structure": o.get("market_structure", ""),
                    "llm_pathway": o.get("leader_pathway", ""),
                    "llm_hhi": o.get("hhi", 0.0),
                    "heuristic_modal_winner": modal_winner,
                    "heuristic_modal_winner_freq": round(
                        modal_winner_n / len(heur), 3),
                    "heuristic_competitive_n": structure_counts.get("competitive", 0),
                    "heuristic_moderate_n": structure_counts.get("moderate", 0),
                    "heuristic_concentrated_n": structure_counts.get("concentrated", 0),
                    "heuristic_modal_pathway": modal_pathway,
                    "heuristic_modal_pathway_freq": round(
                        modal_pathway_n / len(heur), 3),
                }
                w.writerow(row)
                n_written += 1

    print(f"  Wrote {path} ({n_written} LLM-vs-heuristic rows)")


# ============================================================================
# Cross-cut: Evaluator case study
# ============================================================================

EVAL_CASE_FIELDS = [
    "round", "condition", "policy", "seed",
    "score_reliability", "mean_gap", "hhi", "mean_satisfaction",
    "n_active_benchmarks",
]


def write_evaluator_case_study(runs: list, output_dir: str):
    """Long-format paired CSV for full_ecosystem vs dynamic_evaluator."""
    target_conds = ("full_ecosystem", "dynamic_evaluator")
    selected = [
        r for r in runs
        if r["condition"] in target_conds and r["policy"] == "balanced"
    ]
    if not selected:
        print("  Skipping evaluator case study (no eligible runs)")
        return

    path = os.path.join(output_dir, "evaluator_case_study.csv")
    n_rows = 0
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=EVAL_CASE_FIELDS)
        w.writeheader()

        for run in sorted(selected, key=lambda r: (r["condition"], r["seed"])):
            history = run["history"]
            traj = run["trajectory"]
            for t, rd in enumerate(history):
                bm_params = rd.get("benchmark_params", {}) or {}
                row = {
                    "round": rd.get("round", t),
                    "condition": run["condition"],
                    "policy": run["policy"],
                    "seed": run["seed"],
                    "score_reliability": (
                        round(traj["reliability"][t], 6)
                        if traj.get("reliability") and t < len(traj["reliability"])
                        and traj["reliability"][t] == traj["reliability"][t]
                        else ""
                    ),
                    "mean_gap": (
                        round(traj["gap"][t], 6)
                        if traj.get("gap") and t < len(traj["gap"])
                        and traj["gap"][t] == traj["gap"][t]
                        else ""
                    ),
                    "hhi": (
                        round(traj["hhi"][t], 6)
                        if traj.get("hhi") and t < len(traj["hhi"])
                        and traj["hhi"][t] == traj["hhi"][t]
                        else ""
                    ),
                    "mean_satisfaction": (
                        round(traj["satisfaction"][t], 6)
                        if traj.get("satisfaction") and t < len(traj["satisfaction"])
                        and traj["satisfaction"][t] == traj["satisfaction"][t]
                        else ""
                    ),
                    "n_active_benchmarks": len(bm_params),
                }
                w.writerow(row)
                n_rows += 1

    print(f"  Wrote {path} ({n_rows} rows)")


# ============================================================================
# Main
# ============================================================================

def main():
    args = parse_args()
    output_dir = args.output or OUTPUT_BASE
    os.makedirs(output_dir, exist_ok=True)

    print(f"=== aggregate_llm.py ===")
    print(f"Source: {LLM_BASE}")
    print(f"Output: {output_dir}")
    print()

    # Discovery (reuse heuristic discovery walker rooted at LLM_BASE)
    discovered = discover_heuristic_runs(
        LLM_BASE,
        condition_filter=args.condition,
        policy_filter=args.policy,
    )
    if not discovered:
        print("No LLM runs found.")
        return

    print(f"Discovered {len(discovered)} (condition, policy) cells")

    # Process each run
    runs = []
    for label, info in sorted(discovered.items()):
        cond, pol = info["condition"], info["policy"]
        for seed_dir in info["seed_dirs"]:
            seed = _seed_from_dir(seed_dir)
            if args.seed is not None and seed != args.seed:
                continue
            print(f"  Processing {label}/seed_{seed} ...", end=" ", flush=True)
            try:
                run = process_run(
                    seed_dir, cond, pol,
                    last_n=args.last_n,
                    skip_reasoning_md=args.skip_reasoning_md,
                )
                if not run["history"]:
                    print("(empty history -- skipped)")
                    continue
                runs.append(run)
                print(f"{len(run['history'])} rounds, "
                      f"{len(run['events'])} pivotal events, "
                      f"{len(run['incident_rows'])} incidents")
            except Exception as e:
                print(f"FAILED: {e}")
                import traceback
                traceback.print_exc()

    if not runs:
        print("No runs processed.")
        return

    print(f"\nProcessed {len(runs)} runs. Writing outputs...")
    write_llm_summary(runs, output_dir)
    write_llm_outcomes(runs, output_dir)
    write_llm_trajectories(runs, output_dir)
    write_pivotal_events(runs, output_dir)
    write_incident_response(runs, output_dir)
    write_vs_heuristic(runs, output_dir)
    write_evaluator_case_study(runs, output_dir)

    print("\nDone.")


if __name__ == "__main__":
    main()
