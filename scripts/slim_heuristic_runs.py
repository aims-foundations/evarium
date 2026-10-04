"""Slim heuristic runs in hf_data_staging/ to the canonical release file set.

Walks hf_data_staging/<bucket>/heuristic/<condition>/seed_<N>/ and removes
every file/dir not in HEURISTIC_KEEP. LLM buckets are not touched
(use slim_llm_runs.py for that).

Keep policy (option-a): {config.json, rounds.jsonl, metadata.json}.
metadata.json is retained because it carries git_commit + created_at,
which runs.jsonl needs for reproducibility provenance.

Idempotent: safe to re-run; runs already slimmed are no-ops.

Usage:
  python scripts/slim_heuristic_runs.py --dry-run    show what would be removed
  python scripts/slim_heuristic_runs.py              apply
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STAGING = PROJECT_ROOT / "hf_data_staging"

HEURISTIC_KEEP = {
    "config.json",
    "metadata.json",
    "rounds.jsonl",
}


def fmt_bytes(n: float) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}TB"


def find_seed_dirs(staging: Path) -> list[Path]:
    """<bucket>/heuristic/<condition>/seed_<N>/ — return all such dirs."""
    out: list[Path] = []
    for bucket in sorted(p for p in staging.iterdir() if p.is_dir()):
        heuristic_root = bucket / "heuristic"
        if not heuristic_root.is_dir():
            continue
        for seed_dir in sorted(heuristic_root.glob("*/seed_*")):
            if seed_dir.is_dir():
                out.append(seed_dir)
    return out


def collect_removals(seed_dir: Path) -> list[Path]:
    return [p for p in seed_dir.iterdir() if p.name not in HEURISTIC_KEEP]


def remove_path(p: Path) -> int:
    if p.is_dir():
        size = sum(f.stat().st_size for f in p.rglob("*") if f.is_file())
        shutil.rmtree(p)
        return size
    size = p.stat().st_size
    p.unlink()
    return size


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true",
                    help="Print what would be removed; touch nothing.")
    args = ap.parse_args()

    if not STAGING.is_dir():
        print(f"No hf_data_staging/ at {STAGING.relative_to(PROJECT_ROOT)} — nothing to do.")
        return 0

    seed_dirs = find_seed_dirs(STAGING)
    if not seed_dirs:
        print("No heuristic seed dirs found.")
        return 0

    total_paths = 0
    total_bytes = 0
    untouched = 0
    for seed_dir in seed_dirs:
        removals = collect_removals(seed_dir)
        if not removals:
            untouched += 1
            continue
        print(f"\n{seed_dir.relative_to(PROJECT_ROOT)}")
        for p in removals:
            if p.is_dir():
                size = sum(f.stat().st_size for f in p.rglob("*") if f.is_file())
                kind = "dir"
            else:
                size = p.stat().st_size
                kind = "file"
            print(f"  remove {kind}: {p.name}  ({fmt_bytes(size)})")
            total_paths += 1
            total_bytes += size
            if not args.dry_run:
                remove_path(p)

    print()
    print(f"=== {len(seed_dirs)} seed dirs scanned, "
          f"{untouched} already slim, "
          f"{total_paths} paths {'would be' if args.dry_run else ''} removed, "
          f"{fmt_bytes(total_bytes)} freed ===")
    if args.dry_run:
        print("Dry-run: nothing removed. Re-run without --dry-run to apply.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
