"""Reorganize sandbox/experiments runs into the public hf_data_staging/ layout.

Default mode: dry-run. Prints planned moves + per-bucket counts/sizes; touches nothing.
With --apply: copies (does not move) selected files into hf_data_staging/.

Source → destination mapping (LLM only, this round):
  _core_privacy/llm/<cond>_s<N>_<model>/seeds/seed_<N>/      → core_privacy/llm/<model_full>/<cond>/seed_<N>/
  _tier1_ev1/llm/ev1_deepseek_s<N>_<model>/seeds/seed_<N>/   → exogenous_validation/llm/<model_full>/ev1_deepseek_shock/seed_<N>/
  _tier2_ablations/llm/<cond>_s<N>_<model>/seeds/seed_<N>/   → structural_ablations/llm/<model_full>/<cond>/seed_<N>/
  _core_evaluator_capture/llm/<cond>_s<N>_<model>/seeds/seed_<N>/  → core_evaluator_capture/llm/<model_full>/<cond>/seed_<N>/

Filter: runs with evaluation_lag != 3 are dropped (canonical paper lag).

Skipped sources:
  _preserved/                    legacy/contaminated, not paper-supporting
  _llm_apr23_v1/                 pre-identity-redesign reference runs
  heuristic_session49/           heuristics excluded this round; will be re-run at lag=3 later

Slim policy (LLM):
  Keep {config.json, metadata.json, rounds.jsonl, summary.json, game_log.md, ground_truth.json}
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SANDBOX = PROJECT_ROOT / "sandbox" / "experiments"
STAGING = PROJECT_ROOT / "hf_data_staging"

LLM_KEEP = {"config.json", "metadata.json", "rounds.jsonl",
            "summary.json", "game_log.md", "ground_truth.json"}
HEURISTIC_KEEP = {"config.json", "rounds.jsonl"}

MODEL_MAP = {
    "sonnet": "claude-sonnet-4-6",
    "opus":   "claude-opus-4-6",
    "haiku":  "claude-haiku-4-5",
}

EXPECTED_LAG = 3
EXPECTED_ROUNDS = 40


@dataclass
class RunPlan:
    src: Path
    dst: Path
    files_kept: list[str]
    bucket: str
    is_llm: bool
    rounds: int
    lag: int | None
    fallbacks: int | None
    bytes_total: int
    warnings: list[str] = field(default_factory=list)


def parse_llm_dirname(name: str) -> tuple[str, int, str] | None:
    """`<condition>_s<seed>_<model>` → (condition, seed, model_short)."""
    m = re.match(r"^(.+)_s(\d+)_([a-z]+)$", name)
    if not m:
        return None
    cond, seed, model = m.group(1), int(m.group(2)), m.group(3)
    if model not in MODEL_MAP:
        return None
    return cond, seed, model


def discover_seed_dir(run_root: Path) -> Path | None:
    """Locate the seed_<N> dir under <run_root>/seeds/ — exactly one expected."""
    seeds_dir = run_root / "seeds"
    if not seeds_dir.is_dir():
        return None
    candidates = [p for p in seeds_dir.iterdir() if p.is_dir() and p.name.startswith("seed_")]
    return candidates[0] if len(candidates) == 1 else None


def count_rounds(rounds_jsonl: Path) -> int:
    if not rounds_jsonl.is_file():
        return 0
    with rounds_jsonl.open("rb") as f:
        return sum(1 for _ in f)


def read_lag(config_json: Path) -> int | None:
    try:
        with config_json.open() as f:
            cfg = json.load(f)
        return cfg.get("evaluation_lag")
    except Exception:
        return None


def count_fallbacks(rounds_jsonl: Path) -> int:
    fb = 0
    if not rounds_jsonl.is_file():
        return fb
    with rounds_jsonl.open() as f:
        for line in f:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            llm = r.get("llm_calls")
            if isinstance(llm, dict):
                fb += int(llm.get("fallbacks", 0))
    return fb


def build_run_plan(seed_dir: Path, dst_dir: Path, bucket: str, is_llm: bool) -> RunPlan:
    keep = LLM_KEEP if is_llm else HEURISTIC_KEEP
    files = sorted(p.name for p in seed_dir.iterdir() if p.is_file() and p.name in keep)

    rounds_jsonl = seed_dir / "rounds.jsonl"
    config_json = seed_dir / "config.json"
    n_rounds = count_rounds(rounds_jsonl)
    lag = read_lag(config_json) if config_json.is_file() else None
    fallbacks = count_fallbacks(rounds_jsonl) if is_llm else None

    total_bytes = sum((seed_dir / fn).stat().st_size for fn in files)

    warnings: list[str] = []
    if "rounds.jsonl" not in files:
        warnings.append("MISSING rounds.jsonl")
    if "config.json" not in files:
        warnings.append("MISSING config.json")
    if n_rounds != EXPECTED_ROUNDS:
        warnings.append(f"rounds={n_rounds} (expected {EXPECTED_ROUNDS})")
    if lag is not None and lag != EXPECTED_LAG:
        warnings.append(f"lag={lag} (expected {EXPECTED_LAG})")
    if is_llm and fallbacks:
        warnings.append(f"fallbacks={fallbacks}")

    return RunPlan(
        src=seed_dir, dst=dst_dir, files_kept=files, bucket=bucket,
        is_llm=is_llm, rounds=n_rounds, lag=lag, fallbacks=fallbacks,
        bytes_total=total_bytes, warnings=warnings,
    )


def discover_llm_bucket(src_root: Path, bucket: str, dst_root: Path,
                        cond_normalize=None) -> list[RunPlan]:
    """Walk src_root/llm/<cond>_s<seed>_<model>/seeds/seed_<N>/ and build plans."""
    plans: list[RunPlan] = []
    llm_dir = src_root / "llm"
    if not llm_dir.is_dir():
        return plans
    for run_dir in sorted(llm_dir.iterdir()):
        if not run_dir.is_dir():
            continue
        parsed = parse_llm_dirname(run_dir.name)
        if parsed is None:
            print(f"  [skip] cannot parse: {run_dir.name}", file=sys.stderr)
            continue
        cond, seed, model_short = parsed
        cond_dst = cond_normalize(cond) if cond_normalize else cond
        seed_dir = discover_seed_dir(run_dir)
        if seed_dir is None:
            print(f"  [skip] no seed dir: {run_dir}", file=sys.stderr)
            continue
        dst = dst_root / "llm" / MODEL_MAP[model_short] / cond_dst / f"seed_{seed}"
        plans.append(build_run_plan(seed_dir, dst, bucket=bucket, is_llm=True))
    return plans


def discover_heuristic_bucket(src_root: Path, bucket: str, dst_root: Path) -> list[RunPlan]:
    """Walk src_root/heuristic/<cond>/seeds/seed_<N>/ and build plans."""
    plans: list[RunPlan] = []
    heur_dir = src_root / "heuristic"
    if not heur_dir.is_dir():
        return plans
    for cond_dir in sorted(heur_dir.iterdir()):
        if not cond_dir.is_dir():
            continue
        seeds_dir = cond_dir / "seeds"
        if not seeds_dir.is_dir():
            continue
        for seed_dir in sorted(seeds_dir.iterdir()):
            if not seed_dir.is_dir() or not seed_dir.name.startswith("seed_"):
                continue
            dst = dst_root / cond_dir.name / "seeds" / seed_dir.name
            plans.append(build_run_plan(seed_dir, dst, bucket=bucket, is_llm=False))
    return plans


def discover_all(skip_incomplete: bool = False) -> tuple[list[RunPlan], list[RunPlan], list[RunPlan]]:
    """Return (kept, dropped_lag, dropped_incomplete) plans.

    A plan is dropped if evaluation_lag != EXPECTED_LAG. With skip_incomplete=True,
    plans with rounds < EXPECTED_ROUNDS are also excluded (in-flight runs whose seed
    dirs are being actively written — copying them risks partial/racy data).
    Heuristic + _preserved + _llm_apr23_v1 sources are not discovered this round.
    """
    raw: list[RunPlan] = []
    raw += discover_llm_bucket(SANDBOX / "_core_privacy", "core_privacy",
                               STAGING / "core_privacy")
    raw += discover_llm_bucket(SANDBOX / "_tier1_ev1", "exogenous_validation",
                               STAGING / "exogenous_validation",
                               cond_normalize=lambda _c: "ev1_deepseek_shock")
    raw += discover_llm_bucket(SANDBOX / "_tier2_ablations", "structural_ablations",
                               STAGING / "structural_ablations")
    raw += discover_llm_bucket(SANDBOX / "_core_evaluator_capture", "core_evaluator_capture",
                               STAGING / "core_evaluator_capture")

    kept, dropped_lag, dropped_incomplete = [], [], []
    for p in raw:
        if p.lag != EXPECTED_LAG:
            dropped_lag.append(p)
        elif skip_incomplete and p.rounds < EXPECTED_ROUNDS:
            dropped_incomplete.append(p)
        else:
            kept.append(p)
    return kept, dropped_lag, dropped_incomplete


def fmt_bytes(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}TB"


def render_plan(plans: list[RunPlan], dropped_lag: list[RunPlan],
                dropped_incomplete: list[RunPlan]) -> None:
    by_bucket: dict[str, list[RunPlan]] = {}
    for p in plans:
        by_bucket.setdefault(p.bucket, []).append(p)

    print("\n=== Reorganization plan (dry-run) ===\n")
    grand_bytes = grand_runs = grand_warn = 0
    for bucket, runs in by_bucket.items():
        b_bytes = sum(r.bytes_total for r in runs)
        b_warn = sum(1 for r in runs if r.warnings)
        grand_bytes += b_bytes
        grand_runs += len(runs)
        grand_warn += b_warn
        print(f"--- {bucket}  ({len(runs)} runs, {fmt_bytes(b_bytes)}, {b_warn} with warnings)")
        for r in runs:
            rel_src = r.src.relative_to(PROJECT_ROOT)
            rel_dst = r.dst.relative_to(PROJECT_ROOT)
            warn_str = f"  [WARN: {'; '.join(r.warnings)}]" if r.warnings else ""
            print(f"    {rel_src}")
            print(f" -> {rel_dst}  ({len(r.files_kept)} files, {fmt_bytes(r.bytes_total)}){warn_str}")
        print()

    print(f"=== Grand total (kept): {grand_runs} runs, {fmt_bytes(grand_bytes)}, {grand_warn} with warnings ===")
    print()

    if dropped_lag:
        print(f"--- Dropped (lag != {EXPECTED_LAG}): {len(dropped_lag)} runs ---")
        by_drop_bucket: dict[str, int] = {}
        for d in dropped_lag:
            by_drop_bucket[d.bucket] = by_drop_bucket.get(d.bucket, 0) + 1
        for b, n in sorted(by_drop_bucket.items()):
            print(f"  {b}: {n}")
        print()

    if dropped_incomplete:
        print(f"--- Skipped (incomplete, rounds < {EXPECTED_ROUNDS}): "
              f"{len(dropped_incomplete)} runs ---")
        for d in dropped_incomplete:
            rel_src = d.src.relative_to(PROJECT_ROOT)
            print(f"  {rel_src} (rounds={d.rounds})")
        print()

    print("Sources excluded entirely this round:")
    for d in sorted(SANDBOX.iterdir()):
        if d.is_dir() and d.name in {"_preserved", "_llm_apr23_v1", "heuristic_session49"}:
            print(f"  {d.relative_to(PROJECT_ROOT)}")
    print()
    print("Re-run with --apply to copy files into hf_data_staging/.")


def apply_plan(plans: list[RunPlan]) -> None:
    if STAGING.exists():
        print(f"Removing existing {STAGING.relative_to(PROJECT_ROOT)} ...")
        shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True)

    for r in plans:
        r.dst.mkdir(parents=True, exist_ok=True)
        for fn in r.files_kept:
            src_file = r.src / fn
            dst_file = r.dst / fn
            shutil.copy2(src_file, dst_file)
    print(f"Copied {len(plans)} runs into {STAGING.relative_to(PROJECT_ROOT)}.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true",
                    help="Actually copy files into hf_data_staging/ (default: dry-run)")
    ap.add_argument("--skip-incomplete", action="store_true",
                    help=f"Skip runs with rounds < {EXPECTED_ROUNDS} (in-flight runs being actively written)")
    args = ap.parse_args()

    plans, dropped_lag, dropped_incomplete = discover_all(skip_incomplete=args.skip_incomplete)
    render_plan(plans, dropped_lag, dropped_incomplete)
    if args.apply:
        apply_plan(plans)
    return 0


if __name__ == "__main__":
    sys.exit(main())
