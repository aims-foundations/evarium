"""
sim_export.py — Extract sim experiment data from rounds.jsonl → comparable CSVs.

Outputs (in validation/data/processed/):
  sim_benchmarks.csv   columns: round, provider, benchmark, score, true_capability
  sim_market.csv       columns: round, provider, market_share
  sim_events.csv       columns: round, event_type, detail

Usage:
    python validation/sim_export.py <exp_id>
    python validation/sim_export.py exp_001
    python validation/sim_export.py exp_001 exp_003    # exports both, appends exp_id column
"""

import csv
import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[1]
EXP_ROOT = REPO_ROOT / "output" / "experiments"
OUT_DIR = Path(__file__).resolve().parent / "data" / "processed"


def find_exp_dir(exp_id: str) -> Path:
    """Locate experiment directory by prefix match (e.g. 'exp_001')."""
    matches = [d for d in EXP_ROOT.iterdir() if d.is_dir() and d.name.startswith(exp_id)]
    if not matches:
        raise FileNotFoundError(
            f"No experiment directory matching '{exp_id}' in {EXP_ROOT}"
        )
    if len(matches) > 1:
        print(f"[WARN] Multiple matches for '{exp_id}': {[d.name for d in matches]}. Using first.")
    return matches[0]


# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------
def extract_rounds(rounds_path: Path, exp_id: str) -> tuple[list[dict], list[dict], list[dict]]:
    """
    Parse rounds.jsonl and return three lists:
      bench_rows    — one row per (round, provider, benchmark)
      market_rows   — one row per (round, provider)
      event_rows    — one row per notable event
    """
    bench_rows: list[dict] = []
    market_rows: list[dict] = []
    event_rows: list[dict] = []

    prev_leader: dict[str, str] = {}   # benchmark → leading provider
    prev_market_leader: str | None = None

    with rounds_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue

            rnd = d.get("round", 0)

            # ----------------------------------------------------------------
            # Benchmark scores
            # ----------------------------------------------------------------
            per_bench = d.get("per_benchmark_scores", {})
            true_caps = d.get("true_capabilities", {})
            # aggregate score (composite) from d["scores"]
            agg_scores = d.get("scores", {})

            for bench, provider_scores in per_bench.items():
                for provider, score in provider_scores.items():
                    # true_capability: same provider from true_capabilities dict
                    true_cap = true_caps.get(provider)
                    bench_rows.append({
                        "exp_id": exp_id,
                        "round": rnd,
                        "provider": provider,
                        "benchmark": bench,
                        "score": round(float(score), 4),
                        "true_capability": round(float(true_cap), 4) if true_cap is not None else "",
                    })

            # Also emit composite (aggregated) score
            for provider, score in agg_scores.items():
                true_cap = true_caps.get(provider)
                bench_rows.append({
                    "exp_id": exp_id,
                    "round": rnd,
                    "provider": provider,
                    "benchmark": "_composite",
                    "score": round(float(score), 4),
                    "true_capability": round(float(true_cap), 4) if true_cap is not None else "",
                })

            # Leader change events (per benchmark)
            for bench, provider_scores in per_bench.items():
                if not provider_scores:
                    continue
                leader = max(provider_scores, key=lambda p: provider_scores[p])
                if prev_leader.get(bench) and prev_leader[bench] != leader:
                    event_rows.append({
                        "exp_id": exp_id,
                        "round": rnd,
                        "event_type": "benchmark_leader_change",
                        "detail": f"{bench}: {prev_leader[bench]} → {leader}",
                    })
                prev_leader[bench] = leader

            # ----------------------------------------------------------------
            # Market share
            # ----------------------------------------------------------------
            consumer_data = d.get("consumer_data", {})
            market_shares = consumer_data.get("market_shares", {})

            for provider, share in market_shares.items():
                market_rows.append({
                    "exp_id": exp_id,
                    "round": rnd,
                    "provider": provider,
                    "market_share": round(float(share), 4),
                })

            # Market leader change event
            if market_shares:
                market_leader = max(market_shares, key=lambda p: market_shares[p])
                if prev_market_leader and prev_market_leader != market_leader:
                    event_rows.append({
                        "exp_id": exp_id,
                        "round": rnd,
                        "event_type": "market_leader_change",
                        "detail": f"{prev_market_leader} → {market_leader}",
                    })
                prev_market_leader = market_leader

            # New entrant event
            if d.get("new_entrant"):
                event_rows.append({
                    "exp_id": exp_id,
                    "round": rnd,
                    "event_type": "new_entrant",
                    "detail": str(d["new_entrant"]),
                })

            # Benchmark introduction: if a benchmark appears for first time
            for bench in per_bench:
                if bench not in prev_leader:
                    event_rows.append({
                        "exp_id": exp_id,
                        "round": rnd,
                        "event_type": "benchmark_introduced",
                        "detail": bench,
                    })
                    prev_leader[bench] = ""  # mark as seen

    return bench_rows, market_rows, event_rows


def write_csv(rows: list[dict], path: Path, append: bool = False) -> None:
    if not rows:
        return
    mode = "a" if append and path.exists() else "w"
    fieldnames = list(rows[0].keys())
    with path.open(mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if mode == "w":
            writer.writeheader()
        writer.writerows(rows)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main(exp_ids: list[str]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    bench_out = OUT_DIR / "sim_benchmarks.csv"
    market_out = OUT_DIR / "sim_market.csv"
    events_out = OUT_DIR / "sim_events.csv"

    # Clear existing files for fresh export
    for p in [bench_out, market_out, events_out]:
        if p.exists():
            p.unlink()

    for exp_id in exp_ids:
        try:
            exp_dir = find_exp_dir(exp_id)
        except FileNotFoundError as e:
            print(f"[ERROR] {e}")
            continue

        rounds_path = exp_dir / "rounds.jsonl"
        if not rounds_path.exists():
            print(f"[ERROR] {rounds_path} not found")
            continue

        print(f"Exporting {exp_dir.name} ...")
        bench_rows, market_rows, event_rows = extract_rounds(rounds_path, exp_id)

        append = bench_out.exists()
        write_csv(bench_rows, bench_out, append=append)
        write_csv(market_rows, market_out, append=append)
        write_csv(event_rows, events_out, append=append)

        print(f"  bench rows:  {len(bench_rows)}")
        print(f"  market rows: {len(market_rows)}")
        print(f"  events:      {len(event_rows)}")

    print(f"\nOutputs written to {OUT_DIR}/")
    print(f"  {bench_out.name}")
    print(f"  {market_out.name}")
    print(f"  {events_out.name}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1:])
