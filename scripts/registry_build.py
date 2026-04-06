"""
registry_build.py

Walks hf_data/ and writes hf_data/runs.jsonl (one row per completed run).
A run is "complete" if it has a rounds.jsonl file.

Usage:
    python scripts/registry_build.py [--hf-data PATH] [--out PATH]

Phases encoded in the registry:
    "llm_core"          - hf_data/llm_core/<model>/<condition>/seeds/<seed_N>/
    "heuristic_baseline"- hf_data/heuristic_baseline/<condition>/seeds/<seed_N>/
    "claude_archive"    - hf_data/claude_archive/<exp_NNN_name>/  (flat layout)
"""

import argparse
import json
import math
import re
from pathlib import Path


# ---------------------------------------------------------------------------
# Metric extraction helpers
# ---------------------------------------------------------------------------

def _mean(vals):
    vals = [v for v in vals if v is not None]
    return sum(vals) / len(vals) if vals else None


def _pearsonr(xs, ys):
    n = len(xs)
    if n < 2:
        return None
    mx, my = _mean(xs), _mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if dx == 0 or dy == 0:
        return None
    return num / (dx * dy)


def extract_metrics(rounds_path: Path) -> dict:
    """Load rounds.jsonl and compute all registry metrics."""
    rounds = []
    with open(rounds_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rounds.append(json.loads(line))

    if not rounds:
        return {}

    n = len(rounds)
    last = rounds[-1]

    # --- gaming gap ---
    scores = last.get("scores", {})
    true_caps = last.get("true_capabilities", {})
    providers = [p for p in scores if p in true_caps]
    gaps = [scores[p] - true_caps[p] for p in providers]
    gaming_gap_final = _mean(gaps)

    # last-5 rounds average gaming gap
    last5 = rounds[max(0, n - 5):]
    gaps5 = []
    for r in last5:
        s, tc = r.get("scores", {}), r.get("true_capabilities", {})
        ps = [p for p in s if p in tc]
        if ps:
            gaps5.append(_mean([s[p] - tc[p] for p in ps]))
    gaming_gap_avg_last5 = _mean(gaps5)

    # --- HHI ---
    ms = last.get("consumer_data", {}).get("market_shares", {})
    hhi_final = sum(v ** 2 for v in ms.values()) if ms else None

    # --- capability ---
    mean_capability_final = _mean(list(true_caps.values())) if true_caps else None

    # --- safety investment ---
    strats = last.get("strategies", {})
    safety_vals = [v.get("safety") for v in strats.values() if isinstance(v, dict)]
    mean_safety_final = _mean(safety_vals)

    # --- benchmark validity ---
    bp = last.get("benchmark_params", {})
    if isinstance(bp, dict):
        validities = [v.get("validity") for v in bp.values() if isinstance(v, dict) and "validity" in v]
        benchmark_validity_final = _mean(validities)
    else:
        benchmark_validity_final = None

    # --- role adherence violations ---
    violations = 0
    LEAK_TERMS = ["true capability", "actual capability", "ground truth", "real capability"]
    for r in rounds:
        for trace in r.get("actor_traces", {}).values():
            text = json.dumps(trace).lower()
            violations += sum(1 for t in LEAK_TERMS if t in text)

    # --- pattern flags ---

    # Score Inflation: mean_inflation > 0.10 sustained by round 15
    pattern_score_inflation = False
    rounds_before_15 = [r for r in rounds if r.get("round", 0) >= 15]
    if rounds_before_15:
        inflations = []
        for r in rounds_before_15:
            s, tc = r.get("scores", {}), r.get("true_capabilities", {})
            ps = [p for p in s if p in tc]
            if ps:
                inflations.append(_mean([s[p] - tc[p] for p in ps]))
        pattern_score_inflation = bool(inflations and _mean(inflations) > 0.10)

    # Benchmark Turnover: at least one new benchmark introduced during the run.
    # Note: the simulation only introduces benchmarks (never retires), so the
    # original "retirement + introduction" criterion always returns False.
    # Criterion updated to: benchmark set grows at any point after round 0.
    pattern_benchmark_turnover = False
    initial_benchmarks = set(rounds[0].get("benchmark_params", {}).keys()) if rounds else set()
    for r in rounds[1:]:
        current_bp = r.get("benchmark_params", {})
        if isinstance(current_bp, dict):
            if set(current_bp.keys()) - initial_benchmarks:
                pattern_benchmark_turnover = True
                break

    # Regulatory Escalation: intervention beyond investigation/threshold_announcement
    BASIC_INTERVENTIONS = {"threshold_announcement", "investigation"}
    pattern_regulatory_escalation = False
    for r in rounds:
        for iv in r.get("regulator_data", {}).get("interventions", []):
            iv_type = iv.get("type") if isinstance(iv, dict) else str(iv)
            if iv_type and iv_type not in BASIC_INTERVENTIONS:
                pattern_regulatory_escalation = True
                break
        if pattern_regulatory_escalation:
            break

    # Commoditization Shock
    pattern_commoditization_shock = False
    for r in rounds:
        osd = r.get("open_source_data") or {}
        oc = osd.get("OpenCore") or {}
        if oc.get("commoditization_shock_fired"):
            pattern_commoditization_shock = True
            break

    # Gaming Persistence: mean score-capability gap sustained at round 20+
    pattern_gaming_persistence = False
    if rounds:
        late_rounds = [r for r in rounds if r.get("round", 0) >= 20]
        if late_rounds:
            late_gaps = []
            for r in late_rounds:
                s = r.get("scores", {})
                tc = r.get("true_capabilities", {})
                ps = [p for p in s if p in tc]
                if ps:
                    late_gaps.append(_mean([s[p] - tc[p] for p in ps]))
            pattern_gaming_persistence = bool(late_gaps and _mean(late_gaps) > 0.05)

    # Funding Follows Scores: r(funding, score) > r(funding, true_cap)
    pattern_funding_follows_scores = False
    funding_scores, funding_caps, funding_amts = [], [], []
    for r in rounds:
        ft = r.get("funder_data", {}).get("provider_funding_totals", {})
        s = r.get("scores", {})
        tc = r.get("true_capabilities", {})
        for p in ft:
            if p in s and p in tc:
                funding_amts.append(ft[p])
                funding_scores.append(s[p])
                funding_caps.append(tc[p])
    if len(funding_amts) >= 4:
        r_scores = _pearsonr(funding_amts, funding_scores)
        r_caps = _pearsonr(funding_amts, funding_caps)
        if r_scores is not None and r_caps is not None:
            pattern_funding_follows_scores = r_scores > r_caps

    # Safety Incident Response: funder adjusts allocation following major/critical incident
    # Approximation: check if any round has a major/critical incident in actor_traces
    # and whether funder allocations shift in subsequent rounds
    pattern_safety_incident_response = False
    for i, r in enumerate(rounds):
        traces_text = json.dumps(r.get("actor_traces", {})).lower()
        if ("major" in traces_text or "critical" in traces_text) and "incident" in traces_text:
            if i + 1 < len(rounds):
                fm_before = rounds[i].get("funder_data", {}).get("provider_funding_totals", {})
                fm_after = rounds[i + 1].get("funder_data", {}).get("provider_funding_totals", {})
                if fm_before and fm_after:
                    if any(abs(fm_after.get(p, 0) - fm_before.get(p, 0)) > 0.01 for p in fm_before):
                        pattern_safety_incident_response = True
                        break

    return {
        "n_rounds": n,
        "gaming_gap_final": gaming_gap_final,
        "gaming_gap_avg_last5": gaming_gap_avg_last5,
        "hhi_final": hhi_final,
        "mean_capability_final": mean_capability_final,
        "mean_safety_final": mean_safety_final,
        "benchmark_validity_final": benchmark_validity_final,
        "role_adherence_violations": violations,
        "pattern_score_inflation": pattern_score_inflation,
        "pattern_benchmark_turnover": pattern_benchmark_turnover,
        "pattern_regulatory_escalation": pattern_regulatory_escalation,
        "pattern_commoditization_shock": pattern_commoditization_shock,
        "pattern_safety_incident_response": pattern_safety_incident_response,
        "pattern_gaming_persistence": pattern_gaming_persistence,
        "pattern_funding_follows_scores": pattern_funding_follows_scores,
    }


def load_metadata(seed_dir: Path) -> dict:
    meta_path = seed_dir / "metadata.json"
    if meta_path.exists():
        with open(meta_path, encoding="utf-8") as f:
            return json.load(f)
    return {}


# ---------------------------------------------------------------------------
# Directory walkers
# ---------------------------------------------------------------------------

def walk_llm_core(hf_data: Path):
    """Yield run dicts from hf_data/llm_core/<model>/<condition>/seeds/<seed_N>/"""
    llm_core = hf_data / "llm_core"
    if not llm_core.exists():
        return
    for model_dir in sorted(llm_core.iterdir()):
        if not model_dir.is_dir():
            continue
        model = model_dir.name
        for condition_dir in sorted(model_dir.iterdir()):
            if not condition_dir.is_dir():
                continue
            condition = condition_dir.name
            seeds_dir = condition_dir / "seeds"
            if not seeds_dir.exists():
                continue
            for seed_dir in sorted(seeds_dir.iterdir()):
                if not seed_dir.is_dir():
                    continue
                rounds_path = seed_dir / "rounds.jsonl"
                if not rounds_path.exists():
                    continue
                meta = load_metadata(seed_dir)
                seed_num = meta.get("seed")
                if seed_num is None:
                    m = re.search(r"seed_(\d+)", seed_dir.name)
                    seed_num = int(m.group(1)) if m else None

                rel_path = seed_dir.relative_to(hf_data).as_posix()
                row = {
                    "phase": "llm_core",
                    "model": model,
                    "condition": condition,
                    "seed": seed_num,
                    "path": rel_path,
                    "created_at": meta.get("created_at"),
                    "git_commit": meta.get("git_commit"),
                }
                row.update(extract_metrics(rounds_path))
                yield row


def walk_heuristic_baseline(hf_data: Path):
    """Yield run dicts from hf_data/heuristic_baseline/<condition>/seeds/<seed_N>/"""
    baseline = hf_data / "heuristic_baseline"
    if not baseline.exists():
        return
    for condition_dir in sorted(baseline.iterdir()):
        if not condition_dir.is_dir():
            continue
        condition = condition_dir.name
        seeds_dir = condition_dir / "seeds"
        if not seeds_dir.exists():
            continue
        for seed_dir in sorted(seeds_dir.iterdir()):
            if not seed_dir.is_dir():
                continue
            rounds_path = seed_dir / "rounds.jsonl"
            if not rounds_path.exists():
                continue
            meta = load_metadata(seed_dir)
            seed_num = meta.get("seed")
            if seed_num is None:
                m = re.search(r"seed_(\d+)", seed_dir.name)
                seed_num = int(m.group(1)) if m else None

            rel_path = seed_dir.relative_to(hf_data).as_posix()
            row = {
                "phase": "heuristic_baseline",
                "model": "heuristic",
                "condition": condition,
                "seed": seed_num,
                "path": rel_path,
                "created_at": meta.get("created_at"),
                "git_commit": meta.get("git_commit"),
            }
            row.update(extract_metrics(rounds_path))
            yield row


def walk_claude_archive(hf_data: Path):
    """Yield run dicts from hf_data/claude_archive/<exp_NNN_name>/"""
    archive = hf_data / "claude_archive"
    if not archive.exists():
        return
    for exp_dir in sorted(archive.iterdir()):
        if not exp_dir.is_dir():
            continue
        rounds_path = exp_dir / "rounds.jsonl"
        if not rounds_path.exists():
            continue
        # Parse condition from directory name: exp_NNN_<condition>
        m = re.match(r"exp_(\d+)_(.*)", exp_dir.name)
        exp_num = int(m.group(1)) if m else None
        condition = m.group(2) if m else exp_dir.name

        meta_path = exp_dir / "metadata.json"
        meta = {}
        if meta_path.exists():
            with open(meta_path, encoding="utf-8") as f:
                meta = json.load(f)

        rel_path = exp_dir.relative_to(hf_data).as_posix()
        row = {
            "phase": "claude_archive",
            "model": "claude-3.5-sonnet",
            "condition": condition,
            "exp_num": exp_num,
            "seed": meta.get("seed", 1),
            "path": rel_path,
            "created_at": meta.get("created_at"),
            "git_commit": meta.get("git_commit"),
        }
        row.update(extract_metrics(rounds_path))
        yield row


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Build hf_data/runs.jsonl registry")
    parser.add_argument("--hf-data", default=None,
                        help="Path to hf_data/ directory (default: auto-detect relative to script)")
    parser.add_argument("--out", default=None,
                        help="Output path for runs.jsonl (default: hf_data/runs.jsonl)")
    args = parser.parse_args()

    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    hf_data = Path(args.hf_data) if args.hf_data else project_root / "hf_data"
    out_path = Path(args.out) if args.out else hf_data / "runs.jsonl"

    if not hf_data.exists():
        raise FileNotFoundError(f"hf_data directory not found: {hf_data}")

    print(f"Walking {hf_data} ...")
    rows = []

    for row in walk_heuristic_baseline(hf_data):
        rows.append(row)
        if len(rows) % 50 == 0:
            print(f"  {len(rows)} runs processed...")

    for row in walk_llm_core(hf_data):
        rows.append(row)
        if len(rows) % 50 == 0:
            print(f"  {len(rows)} runs processed...")

    for row in walk_claude_archive(hf_data):
        rows.append(row)
        if len(rows) % 10 == 0:
            print(f"  {len(rows)} runs processed...")

    print(f"Writing {len(rows)} rows to {out_path} ...")
    with open(out_path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")

    # Summary
    phases = {}
    for row in rows:
        phases[row["phase"]] = phases.get(row["phase"], 0) + 1
    print("Done.")
    for phase, count in sorted(phases.items()):
        print(f"  {phase}: {count} runs")


if __name__ == "__main__":
    main()
