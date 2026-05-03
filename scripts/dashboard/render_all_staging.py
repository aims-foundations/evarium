"""Batch-render the 9-panel dashboard for every LLM run in hf_data_staging.

Walks `hf_data_staging/<tier>/llm/<model>/<condition>/seed_NN/rounds.jsonl`
and writes `dashboard.png` next to each. Pass --pdf to also write
`dashboard.pdf` (off by default since the slim release shape excludes PDFs).

Usage:
  python scripts/dashboard/render_all_staging.py
  python scripts/dashboard/render_all_staging.py --skip-existing
  python scripts/dashboard/render_all_staging.py --pdf
"""
from __future__ import annotations

import argparse
import sys
import time
import traceback
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
from dashboard import render  # noqa: E402

STAGING = REPO / "hf_data_staging"


def find_runs() -> list[Path]:
    runs = []
    for jsonl in STAGING.rglob("rounds.jsonl"):
        if "/llm/" not in jsonl.as_posix():
            continue
        runs.append(jsonl.parent)
    return sorted(runs)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--skip-existing", action="store_true",
                    help="Skip runs that already have dashboard.png")
    ap.add_argument("--pdf", action="store_true",
                    help="Also save dashboard.pdf alongside .png (off by default).")
    args = ap.parse_args()

    runs = find_runs()
    print(f"Found {len(runs)} LLM runs in {STAGING.relative_to(REPO)}")
    failures = []
    skipped = 0
    t0 = time.time()
    for i, run_dir in enumerate(runs, 1):
        out = run_dir / "dashboard.png"
        rel = run_dir.relative_to(STAGING).as_posix()
        if args.skip_existing and out.is_file():
            print(f"  [{i:>2}/{len(runs)}] skip (exists): {rel}")
            skipped += 1
            continue
        try:
            t = time.time()
            render(run_dir, out, save_pdf=args.pdf)
            print(f"  [{i:>2}/{len(runs)}] OK ({time.time()-t:.1f}s): {rel}")
        except Exception as e:
            print(f"  [{i:>2}/{len(runs)}] FAIL: {rel}: {e}")
            traceback.print_exc()
            failures.append((rel, str(e)))

    elapsed = time.time() - t0
    print(f"\nDone in {elapsed/60:.1f} min. {len(runs)-len(failures)-skipped} ok, "
          f"{skipped} skipped, {len(failures)} failed.")
    if failures:
        print("Failures:")
        for rel, msg in failures:
            print(f"  - {rel}: {msg}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
