"""
Count LLM fallback events per run by scanning actor_traces in rounds.jsonl.

A "fallback" is any actor_trace reasoning string containing the word "fallback".
This catches all fallback returns — not just the ones that print `[LLM FALLBACK]` to stdout —
so it's more complete than grepping logs.

Usage:
    python scripts/count_fallbacks.py                                    # scan sandbox/experiments/llm/
    python scripts/count_fallbacks.py --root hf_data/llm_core            # scan a different root
    python scripts/count_fallbacks.py --per-round                        # include per-round breakdown
    python scripts/count_fallbacks.py --threshold 50                     # flag runs with >=50 fallbacks

Output columns:
    total        — all actor_traces entries containing "fallback"
    provider     — provider actors (Orion/Apex/Genesis/Mirage/OpenCore/Spark)
    funder       — funder actors (VC/corp/gov/foundation names)
    evaluator    — Evaluator actor (captured since session 29)
    regulator    — Regulator actor
    fb_rate      — total / approx_llm_calls, assuming ~500 calls/run for 40-round sim
"""
import argparse
import glob
import json
import os
import sys
from collections import defaultdict

PROVIDER_NAMES = {"Orion Labs", "Apex AI", "Genesis Systems", "Mirage AI", "OpenCore", "Spark AI"}
APPROX_CALLS_PER_RUN = 500  # rough estimate: ~10-15 calls/round * 40 rounds


def classify(actor: str) -> str:
    if actor in PROVIDER_NAMES:
        return "provider"
    low = actor.lower()
    if "evaluator" in low:
        return "evaluator"
    if "regulator" in low:
        return "regulator"
    if any(k in low for k in ("fund", "capital", "venture", "foundation", "corp", "research")):
        return "funder"
    return "other"


def scan_run(rjl_path: str):
    """Return (total, by_category_dict, by_round_dict)."""
    total = 0
    by_cat = defaultdict(int)
    by_round = defaultdict(int)
    with open(rjl_path) as f:
        for line in f:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            round_num = r.get("round", -1)
            at = r.get("actor_traces", {}) or {}
            for actor, trace in at.items():
                if not isinstance(trace, str):
                    continue
                if "fallback" not in trace.lower():
                    continue
                total += 1
                by_cat[classify(actor)] += 1
                by_round[round_num] += 1
    return total, dict(by_cat), dict(by_round)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default="sandbox/experiments/llm",
                        help="Root directory to scan (default: sandbox/experiments/llm)")
    parser.add_argument("--per-round", action="store_true",
                        help="Print per-round fallback counts for runs above threshold")
    parser.add_argument("--threshold", type=int, default=0,
                        help="Only print runs with total fallbacks >= this (default: 0, all)")
    parser.add_argument("--sort-by", choices=["name", "total"], default="name")
    args = parser.parse_args()

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    root = args.root if os.path.isabs(args.root) else os.path.join(project_root, args.root)
    if not os.path.isdir(root):
        print(f"ERROR: {root} not found", file=sys.stderr)
        sys.exit(1)

    runs = sorted(glob.glob(os.path.join(root, "**/rounds.jsonl"), recursive=True))
    if not runs:
        print(f"No rounds.jsonl files found under {root}", file=sys.stderr)
        sys.exit(1)

    results = []
    for rjl in runs:
        rel = os.path.relpath(os.path.dirname(rjl), root).replace(os.sep, "/")
        total, by_cat, by_round = scan_run(rjl)
        results.append((rel, total, by_cat, by_round))

    if args.sort_by == "total":
        results.sort(key=lambda x: -x[1])

    header = f'{"run":<60} {"total":>6} {"prov":>5} {"fund":>5} {"eval":>5} {"reg":>4} {"fb%":>5}'
    print(header)
    print("-" * len(header))
    for rel, total, by_cat, _ in results:
        if total < args.threshold:
            continue
        fb_rate = 100.0 * total / APPROX_CALLS_PER_RUN
        print(f'{rel:<60} {total:>6} {by_cat.get("provider",0):>5} {by_cat.get("funder",0):>5} '
              f'{by_cat.get("evaluator",0):>5} {by_cat.get("regulator",0):>4} {fb_rate:>4.1f}%')

    if args.per_round:
        print()
        print("Per-round breakdown (runs >= threshold):")
        for rel, total, _, by_round in results:
            if total < args.threshold:
                continue
            rounds_sorted = sorted(by_round.items())
            compact = " ".join(f"r{r}={c}" for r, c in rounds_sorted if c > 0)
            print(f"  {rel}: {compact}")


if __name__ == "__main__":
    main()
