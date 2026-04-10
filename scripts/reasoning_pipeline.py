"""
Reasoning-Grounded Trajectory Analysis (Steps 1-2 + Strategic Arc Extraction)

Implements the pipeline from docs/aggregation_pipeline.md:
  Step 1: Detect pivotal rounds from behavioral data
  Step 2: Extract reasoning windows around pivots

Plus: Strategic arc extraction — per-provider narrative summaries that capture
the "conventional wisdom" about what each provider did and why they ended up
where they did (analogous to "Anthropic won enterprise because of safety focus").

Usage:
    python scripts/reasoning_pipeline.py <run_dir>
    python scripts/reasoning_pipeline.py <run_dir> --output report.md

Example:
    python scripts/reasoning_pipeline.py sandbox/experiments/apr9_sonnet46_market_structure/full_ecosystem_balanced_llm_s11_20260409_031446
"""

import argparse
import json
import os
import sys
from collections import namedtuple

# ============================================================
#  Step 1: Detect Pivotal Rounds
# ============================================================

PivotalEvent = namedtuple("PivotalEvent", ["round", "provider", "event_type", "details"])

# Thresholds (from aggregation_pipeline.md)
ALLOC_SHIFT_THRESHOLD = 0.05    # portfolio lever change
MARKET_DISRUPTION_THRESHOLD = 0.03  # market share change in one round
INCIDENT_SEVERITY_THRESHOLD = "major"  # major or critical


def detect_pivotal_rounds(rounds: list) -> list:
    """Detect pivotal rounds purely from behavioral data.

    Returns list of PivotalEvent namedtuples sorted by round.
    """
    events = []
    providers = list(rounds[0]["scores"].keys())

    for i, r in enumerate(rounds):
        rnd = r["round"]
        if i == 0:
            continue

        prev = rounds[i - 1]

        # --- Allocation shifts ---
        for p in providers:
            curr_strat = r.get("effective_strategies", {}).get(p, {})
            prev_strat = prev.get("effective_strategies", {}).get(p, {})
            for lever in ("rd", "safety", "product"):
                curr_val = curr_strat.get(lever, 0)
                prev_val = prev_strat.get(lever, 0)
                delta = curr_val - prev_val
                if abs(delta) >= ALLOC_SHIFT_THRESHOLD:
                    events.append(PivotalEvent(
                        round=rnd, provider=p, event_type="allocation_shift",
                        details={"lever": lever, "delta": round(delta, 3),
                                 "from": round(prev_val, 3), "to": round(curr_val, 3)}
                    ))

        # --- Market disruptions ---
        curr_shares = r.get("consumer_data", {}).get("market_shares", {})
        prev_shares = prev.get("consumer_data", {}).get("market_shares", {})
        for p in providers:
            curr_ms = curr_shares.get(p, 0)
            prev_ms = prev_shares.get(p, 0)
            delta = curr_ms - prev_ms
            if abs(delta) >= MARKET_DISRUPTION_THRESHOLD:
                events.append(PivotalEvent(
                    round=rnd, provider=p, event_type="market_disruption",
                    details={"delta": round(delta, 3),
                             "from": round(prev_ms, 3), "to": round(curr_ms, 3)}
                ))

        # --- Gap crossings (score - satisfaction crosses zero) ---
        for p in providers:
            curr_score = r.get("scores", {}).get(p, 0)
            prev_score = prev.get("scores", {}).get(p, 0)
            curr_sat = r.get("consumer_data", {}).get("provider_satisfaction", {}).get(p, 0)
            prev_sat = prev.get("consumer_data", {}).get("provider_satisfaction", {}).get(p, 0)
            curr_gap = curr_score - curr_sat
            prev_gap = prev_score - prev_sat
            if prev_gap * curr_gap < 0:  # sign change
                events.append(PivotalEvent(
                    round=rnd, provider=p, event_type="gap_crossing",
                    details={"prev_gap": round(prev_gap, 4), "curr_gap": round(curr_gap, 4)}
                ))

        # --- Incident shocks ---
        risk_signals = r.get("media_data", {}).get("risk_signals", [])
        if isinstance(risk_signals, list):
            incidents = [x for x in risk_signals if isinstance(x, str) and "incident" in x]
        elif isinstance(risk_signals, dict):
            incidents = [k for k, v in risk_signals.items() if v and "incident" in k]
        else:
            incidents = []
        for inc in incidents:
            # Check penalty breakdown to find which provider was hit
            penalties = r.get("consumer_data", {}).get("penalty_breakdown", {})
            hit_provider = None
            max_penalty = 0
            for p, pb in penalties.items():
                pen = pb.get("incident_penalty", 0)
                if pen > max_penalty:
                    max_penalty = pen
                    hit_provider = p
            events.append(PivotalEvent(
                round=rnd, provider=hit_provider or "unknown",
                event_type="incident_shock",
                details={"incident_type": inc, "max_penalty": round(max_penalty, 3)}
            ))

        # --- Regulatory escalation ---
        interventions = r.get("regulator_data", {}).get("interventions", [])
        for intv in interventions:
            itype = intv.get("type", intv.get("action", "unknown"))
            if itype in ("impose_sanction", "emergency_investigation"):
                target = intv.get("target", intv.get("provider", "all"))
                events.append(PivotalEvent(
                    round=rnd, provider=target, event_type="regulatory_escalation",
                    details={"action": itype}
                ))

    return sorted(events, key=lambda e: (e.round, e.provider))


# ============================================================
#  Step 2: Extract Reasoning Windows
# ============================================================

def extract_reasoning_windows(rounds: list, events: list, context_window: int = 2) -> list:
    """For each pivotal event, extract reasoning traces + public context.

    Returns list of dicts with event, reasoning_before, reasoning_at, public_context.
    """
    rounds_by_num = {r["round"]: r for r in rounds}
    windows = []

    for event in events:
        rnd = event.round
        r = rounds_by_num.get(rnd, {})

        # Get reasoning at pivot round
        traces = r.get("actor_traces", {})
        reasoning_at = traces.get(event.provider, "")

        # Get reasoning before (context_window prior rounds)
        reasoning_before = []
        for offset in range(context_window, 0, -1):
            prev_rnd = rnd - offset
            prev_r = rounds_by_num.get(prev_rnd, {})
            prev_traces = prev_r.get("actor_traces", {})
            reasoning_before.append(prev_traces.get(event.provider, ""))

        # Public context at pivot round
        leaderboard = {p: r.get("scores", {}).get(p, 0)
                       for p in r.get("scores", {}).keys()}
        market_shares = r.get("consumer_data", {}).get("market_shares", {})
        media_sentiment = r.get("media_data", {}).get("sentiment", 0)
        media_headlines = r.get("media_data", {}).get("headlines", [])
        risk_signals = r.get("media_data", {}).get("risk_signals", [])
        interventions = r.get("regulator_data", {}).get("interventions", [])

        windows.append({
            "event": event._asdict(),
            "reasoning_before": reasoning_before,
            "reasoning_at": reasoning_at,
            "public_context": {
                "leaderboard": leaderboard,
                "market_shares": market_shares,
                "media_sentiment": media_sentiment,
                "media_headlines": media_headlines[:3],  # cap for readability
                "risk_signals": risk_signals,
                "interventions": interventions,
            }
        })

    return windows


# ============================================================
#  Strategic Arc Extraction
# ============================================================

def extract_strategic_arcs(rounds: list) -> dict:
    """Extract per-provider strategic arc: trajectory + key stats + reasoning samples.

    Returns {provider: {trajectory, early_reasoning, mid_reasoning, late_reasoning, stats}}.
    This is the raw material for generating "conventional wisdom" narratives.
    """
    providers = list(rounds[0]["scores"].keys())
    n = len(rounds)
    early = rounds[1] if n > 1 else rounds[0]  # round 1 (first with traces)
    mid = rounds[n // 2]
    late = rounds[-1]

    arcs = {}
    for p in providers:
        # Trajectory stats
        init_score = rounds[0]["scores"].get(p, 0)
        final_score = late["scores"].get(p, 0)
        init_share = rounds[0].get("consumer_data", {}).get("market_shares", {}).get(p, 0)
        final_share = late.get("consumer_data", {}).get("market_shares", {}).get(p, 0)

        init_strat = rounds[0].get("effective_strategies", {}).get(p, {})
        final_strat = late.get("effective_strategies", {}).get(p, {})

        # Peak and trough market share
        shares = [r.get("consumer_data", {}).get("market_shares", {}).get(p, 0) for r in rounds]
        peak_share = max(shares)
        peak_round = shares.index(peak_share)
        trough_share = min(shares)
        trough_round = shares.index(trough_share)

        # Capability growth
        init_cap = rounds[0].get("capability_vectors", {}).get(p, {})
        final_cap = late.get("capability_vectors", {}).get(p, {})
        if init_cap and final_cap:
            init_mean = sum(init_cap.values()) / len(init_cap)
            final_mean = sum(final_cap.values()) / len(final_cap)
            # Strongest growth dimension
            growth = {d: final_cap.get(d, 0) - init_cap.get(d, 0) for d in init_cap}
            top_growth_dim = max(growth, key=growth.get) if growth else "N/A"
        else:
            init_mean, final_mean, top_growth_dim = 0, 0, "N/A"

        # Reasoning samples (early, mid, late)
        early_reasoning = early.get("actor_traces", {}).get(p, "")
        mid_reasoning = mid.get("actor_traces", {}).get(p, "")
        late_reasoning = late.get("actor_traces", {}).get(p, "")

        # Investment trajectory: early vs late portfolio
        arcs[p] = {
            "score_trajectory": f"{init_score:.3f} -> {final_score:.3f} ({final_score - init_score:+.3f})",
            "share_trajectory": f"{init_share:.1%} -> {final_share:.1%}",
            "peak_share": f"{peak_share:.1%} at R{peak_round}",
            "trough_share": f"{trough_share:.1%} at R{trough_round}",
            "portfolio_early": f"rd={init_strat.get('rd', 0):.0%} safety={init_strat.get('safety', 0):.0%} product={init_strat.get('product', 0):.0%}",
            "portfolio_late": f"rd={final_strat.get('rd', 0):.0%} safety={final_strat.get('safety', 0):.0%} product={final_strat.get('product', 0):.0%}",
            "capability_growth": f"{init_mean:.3f} -> {final_mean:.3f}",
            "top_growth_dimension": top_growth_dim,
            "early_reasoning": early_reasoning,
            "mid_reasoning": mid_reasoning,
            "late_reasoning": late_reasoning,
        }

    return arcs


def extract_funder_arcs(rounds: list) -> dict:
    """Extract per-funder arc: who they backed and why."""
    n = len(rounds)
    early = rounds[1] if n > 1 else rounds[0]
    mid = rounds[n // 2]
    late = rounds[-1]

    funders = [k for k in early.get("actor_traces", {}).keys()
               if k not in list(rounds[0]["scores"].keys()) and k != "Regulator"]

    arcs = {}
    for f in funders:
        arcs[f] = {
            "early_reasoning": early.get("actor_traces", {}).get(f, ""),
            "mid_reasoning": mid.get("actor_traces", {}).get(f, ""),
            "late_reasoning": late.get("actor_traces", {}).get(f, ""),
        }
    return arcs


# ============================================================
#  Report Generation
# ============================================================

def generate_report(rounds: list, events: list, windows: list,
                    arcs: dict, funder_arcs: dict) -> str:
    """Generate a markdown report combining pivotal events + strategic arcs."""
    providers = list(rounds[0]["scores"].keys())
    lines = []
    lines.append("# Reasoning-Grounded Analysis Report\n")

    # --- Run summary ---
    n = len(rounds)
    final = rounds[-1]
    final_shares = final.get("consumer_data", {}).get("market_shares", {})
    leader = max(final_shares, key=final_shares.get) if final_shares else "N/A"
    lines.append(f"**Rounds:** {n} | **Leader:** {leader} ({final_shares.get(leader, 0):.1%})")
    lines.append(f"**Pivotal events detected:** {len(events)}\n")

    # --- Event type distribution ---
    type_counts = {}
    for e in events:
        type_counts[e.event_type] = type_counts.get(e.event_type, 0) + 1
    lines.append("## Pivotal Event Summary\n")
    lines.append("| Event Type | Count |")
    lines.append("|------------|-------|")
    for et, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {et} | {count} |")

    # --- Provider event distribution ---
    lines.append("\n| Provider | Total Events | Alloc Shifts | Market Disruptions | Incidents | Regulatory |")
    lines.append("|----------|-------------|-------------|-------------------|-----------|-----------|")
    for p in providers:
        p_events = [e for e in events if e.provider == p]
        alloc = sum(1 for e in p_events if e.event_type == "allocation_shift")
        market = sum(1 for e in p_events if e.event_type == "market_disruption")
        incident = sum(1 for e in p_events if e.event_type == "incident_shock")
        reg = sum(1 for e in p_events if e.event_type == "regulatory_escalation")
        lines.append(f"| {p} | {len(p_events)} | {alloc} | {market} | {incident} | {reg} |")

    # --- Pivotal event timeline ---
    lines.append("\n## Pivotal Event Timeline\n")
    current_round = -1
    for e in events:
        if e.round != current_round:
            lines.append(f"\n**Round {e.round}:**")
            current_round = e.round
        detail_str = ", ".join(f"{k}={v}" for k, v in e.details.items())
        lines.append(f"- [{e.event_type}] {e.provider}: {detail_str}")

    # --- Strategic arcs ---
    lines.append("\n\n## Strategic Arcs (Per-Provider)\n")
    for p in providers:
        arc = arcs[p]
        lines.append(f"### {p}\n")
        lines.append(f"- **Score:** {arc['score_trajectory']}")
        lines.append(f"- **Market share:** {arc['share_trajectory']} (peak {arc['peak_share']}, trough {arc['trough_share']})")
        lines.append(f"- **Portfolio shift:** {arc['portfolio_early']} -> {arc['portfolio_late']}")
        lines.append(f"- **Capability growth:** {arc['capability_growth']} (strongest: {arc['top_growth_dimension']})")

        lines.append(f"\n**Early reasoning (R1):**")
        lines.append(f"> {arc['early_reasoning'][:500]}{'...' if len(arc['early_reasoning']) > 500 else ''}\n")
        lines.append(f"**Mid reasoning (R{n // 2}):**")
        lines.append(f"> {arc['mid_reasoning'][:500]}{'...' if len(arc['mid_reasoning']) > 500 else ''}\n")
        lines.append(f"**Late reasoning (R{n - 1}):**")
        lines.append(f"> {arc['late_reasoning'][:500]}{'...' if len(arc['late_reasoning']) > 500 else ''}\n")

    # --- Funder arcs ---
    lines.append("\n## Funder Arcs\n")
    for f, arc in funder_arcs.items():
        lines.append(f"### {f}\n")
        lines.append(f"**Early (R1):** {arc['early_reasoning'][:300]}{'...' if len(arc['early_reasoning']) > 300 else ''}\n")
        lines.append(f"**Late (R{n - 1}):** {arc['late_reasoning'][:300]}{'...' if len(arc['late_reasoning']) > 300 else ''}\n")

    # --- Reasoning windows for key events (first 10) ---
    lines.append("\n## Key Reasoning Windows (first 10 pivotal events)\n")
    for w in windows[:10]:
        e = w["event"]
        lines.append(f"### R{e['round']}: {e['provider']} — {e['event_type']}")
        detail_str = ", ".join(f"{k}={v}" for k, v in e["details"].items())
        lines.append(f"*{detail_str}*\n")

        ctx = w["public_context"]
        lines.append(f"Media sentiment: {ctx['media_sentiment']:.2f} | Risk signals: {ctx['risk_signals']}")

        if w["reasoning_at"]:
            lines.append(f"\n**Reasoning at pivot:**")
            lines.append(f"> {w['reasoning_at'][:400]}{'...' if len(w['reasoning_at']) > 400 else ''}\n")
        lines.append("---\n")

    return "\n".join(lines)


# ============================================================
#  Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Reasoning-grounded trajectory analysis (Steps 1-2)")
    parser.add_argument("run_dir", help="Path to a single run directory containing rounds.jsonl")
    parser.add_argument("--output", default=None, help="Output markdown path (default: <run_dir>/reasoning_analysis.md)")
    args = parser.parse_args()

    run_dir = args.run_dir
    rounds_path = os.path.join(run_dir, "rounds.jsonl")
    if not os.path.exists(rounds_path):
        print(f"Error: {rounds_path} not found")
        sys.exit(1)

    print(f"Loading {rounds_path}...")
    with open(rounds_path, encoding="utf-8") as f:
        rounds = [json.loads(line) for line in f if line.strip()]
    print(f"Loaded {len(rounds)} rounds")

    # Step 1: Detect pivotal rounds
    print("Step 1: Detecting pivotal rounds...")
    events = detect_pivotal_rounds(rounds)
    print(f"  Found {len(events)} pivotal events")

    # Step 2: Extract reasoning windows
    print("Step 2: Extracting reasoning windows...")
    windows = extract_reasoning_windows(rounds, events)

    # Strategic arcs
    print("Extracting strategic arcs...")
    arcs = extract_strategic_arcs(rounds)
    funder_arcs = extract_funder_arcs(rounds)

    # Generate report
    print("Generating report...")
    report = generate_report(rounds, events, windows, arcs, funder_arcs)

    output_path = args.output or os.path.join(run_dir, "reasoning_analysis.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Report written to {output_path}")

    # Print summary to console
    print(f"\n{'='*60}")
    print(f"PIVOTAL EVENTS: {len(events)}")
    type_counts = {}
    for e in events:
        type_counts[e.event_type] = type_counts.get(e.event_type, 0) + 1
    for et, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {et}: {c}")

    print(f"\nPER-PROVIDER EVENT COUNTS:")
    providers = list(rounds[0]["scores"].keys())
    for p in providers:
        count = sum(1 for e in events if e.provider == p)
        print(f"  {p}: {count}")


if __name__ == "__main__":
    main()
