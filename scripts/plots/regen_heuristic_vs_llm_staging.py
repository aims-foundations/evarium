"""Regenerate the heuristic-vs-LLM bar plot from the new hf_data_staging layout.

Reads:
  hf_data_staging/core_privacy/heuristic/<cond>/seed_<N>/rounds.jsonl
  hf_data_staging/core_privacy/llm/<model>/<cond>/seed_<N>/rounds.jsonl

Reuses the existing `plot_heuristic_vs_llm` renderer from
`scripts.plots.per_benchmark_core_privacy` by materialising a temporary
heuristic per_benchmark_long.csv (structural=none) on disk.

CLI:
  python -m scripts.plots.regen_heuristic_vs_llm_staging
  python -m scripts.plots.regen_heuristic_vs_llm_staging --model claude-opus-4-6
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
import tempfile
from pathlib import Path

import pandas as pd

from . import paths as _paths
from .per_benchmark import per_benchmark_from_jsonl
from .per_benchmark_core_privacy import plot_heuristic_vs_llm, plot_llm_bars

STAGING_ROOT = Path(_paths.PROJECT_ROOT) / "hf_data_staging" / "core_privacy"


def discover_heuristic_runs(staging_root: Path, min_rounds: int = 40):
    """Yield (cond, seed, jsonl) under <staging_root>/heuristic/<cond>/seed_<N>/rounds.jsonl."""
    root = staging_root / "heuristic"
    if not root.exists():
        return
    for cond_dir in sorted(root.iterdir()):
        if not cond_dir.is_dir():
            continue
        cond = cond_dir.name
        for seed_dir in sorted(cond_dir.iterdir()):
            if not seed_dir.is_dir() or not seed_dir.name.startswith("seed_"):
                continue
            try:
                seed = int(seed_dir.name.split("_", 1)[1])
            except ValueError:
                continue
            jsonl = seed_dir / "rounds.jsonl"
            if not jsonl.exists():
                continue
            with open(jsonl) as f:
                n_rounds = sum(1 for _ in f)
            if n_rounds < min_rounds:
                print(f"SKIP heuristic (partial {n_rounds}/{min_rounds}): {cond}/seed_{seed}")
                continue
            yield cond, seed, str(jsonl)


def discover_llm_runs(staging_root: Path, model: str, min_rounds: int = 40):
    """Yield (cond, seed, jsonl) under <staging_root>/llm/<model>/<cond>/seed_<N>/rounds.jsonl."""
    root = staging_root / "llm" / model
    if not root.exists():
        print(f"WARN llm/{model} not under staging — available: "
              f"{[d.name for d in (staging_root / 'llm').iterdir()] if (staging_root / 'llm').exists() else []}")
        return
    for cond_dir in sorted(root.iterdir()):
        if not cond_dir.is_dir():
            continue
        cond = cond_dir.name
        for seed_dir in sorted(cond_dir.iterdir()):
            if not seed_dir.is_dir() or not seed_dir.name.startswith("seed_"):
                continue
            try:
                seed = int(seed_dir.name.split("_", 1)[1])
            except ValueError:
                continue
            jsonl = seed_dir / "rounds.jsonl"
            if not jsonl.exists():
                continue
            with open(jsonl) as f:
                n_rounds = sum(1 for _ in f)
            if n_rounds < min_rounds:
                print(f"SKIP llm (partial {n_rounds}/{min_rounds}): {model}/{cond}/seed_{seed}")
                continue
            yield cond, seed, str(jsonl)


def write_heuristic_csv(staging_root: Path, csv_path: str) -> int:
    """Build a CSV matching extract_per_benchmark's schema (structural='none')
    so it can be fed straight into plot_heuristic_vs_llm. Returns row count."""
    rows = []
    seed_counts = {}
    for cond, seed, jsonl in discover_heuristic_runs(staging_root):
        try:
            df = per_benchmark_from_jsonl(jsonl)
        except Exception as e:
            print(f"ERROR {jsonl}: {e}")
            continue
        for _, r in df.iterrows():
            rows.append({
                "condition": cond, "structural": "none", "seed": seed,
                "benchmark": r["benchmark"], "provider": r["provider"],
                "score": r["score"], "clean_matched": r["clean_matched"],
                "clean_gap": r["clean_gap"],
            })
        seed_counts[cond] = seed_counts.get(cond, set()) | {seed}
    if not rows:
        return 0
    fieldnames = list(rows[0].keys())
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote heuristic CSV {csv_path}: {len(rows)} rows")
    for cond, seeds in sorted(seed_counts.items()):
        print(f"  heuristic {cond}: {len(seeds)} seeds")
    return len(rows)


def build_llm_long_df(staging_root: Path, model: str) -> pd.DataFrame:
    rows = []
    seed_counts = {}
    for cond, seed, jsonl in discover_llm_runs(staging_root, model):
        try:
            df = per_benchmark_from_jsonl(jsonl)
        except Exception as e:
            print(f"ERROR {jsonl}: {e}")
            continue
        for _, r in df.iterrows():
            rows.append({
                "condition": cond, "seed": seed, "model": model,
                "benchmark": r["benchmark"], "provider": r["provider"],
                "clean_gap": r["clean_gap"], "score": r["score"],
                "clean_matched": r["clean_matched"],
            })
        seed_counts[cond] = seed_counts.get(cond, set()) | {seed}
    df_long = pd.DataFrame(rows)
    for cond, seeds in sorted(seed_counts.items()):
        print(f"  llm/{model} {cond}: {len(seeds)} seeds")
    return df_long


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--staging-root", default=str(STAGING_ROOT),
                    help="Path to <hf_data_staging>/core_privacy (default: project hf_data_staging/core_privacy)")
    ap.add_argument("--model", default="claude-sonnet-4-6",
                    help="LLM model directory under staging/llm/ (default: claude-sonnet-4-6)")
    ap.add_argument("--out", default=os.path.join(_paths.paper_dir(), "heuristic_vs_llm.png"),
                    help="Output path for paired panel (default: output/paper/heuristic_vs_llm.png)")
    ap.add_argument("--out-llm-only", default=os.path.join(_paths.paper_dir(), "bars_public_vs_private.png"),
                    help="Output path for LLM-only panel (default: output/paper/bars_public_vs_private.png)")
    args = ap.parse_args()

    staging_root = Path(args.staging_root)
    if not staging_root.exists():
        print(f"ERROR: staging root not found: {staging_root}")
        sys.exit(1)

    print(f"Staging root: {staging_root}")
    print(f"LLM model:    {args.model}")
    print(f"Output:       {args.out}")
    print()

    df_long_llm = build_llm_long_df(staging_root, args.model)
    if df_long_llm.empty:
        print(f"ERROR: no LLM runs found under {staging_root}/llm/{args.model}")
        sys.exit(1)

    with tempfile.NamedTemporaryFile(
        prefix="heuristic_per_benchmark_long_",
        suffix=".csv",
        delete=False,
        mode="w",
    ) as tmp:
        tmp_csv = tmp.name
    try:
        n_heur = write_heuristic_csv(staging_root, tmp_csv)
        if n_heur == 0:
            print(f"ERROR: no heuristic runs found under {staging_root}/heuristic/")
            sys.exit(1)

        n_pub_h = sum(1 for c, _, _ in discover_heuristic_runs(staging_root) if c == "public_only")
        n_pri_h = sum(1 for c, _, _ in discover_heuristic_runs(staging_root) if c == "private_only")
        n_pub_l = int(df_long_llm[df_long_llm.condition == "public_only"]["seed"].nunique())
        n_pri_l = int(df_long_llm[df_long_llm.condition == "private_only"]["seed"].nunique())
        title_suffix = (
            f"hf_data_staging | heuristic N={n_pub_h}/{n_pri_h} (pub/priv) | "
            f"LLM {args.model} N={n_pub_l}/{n_pri_l}"
        )

        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        plot_heuristic_vs_llm(df_long_llm, tmp_csv, args.out, title_suffix=title_suffix)

        Path(args.out_llm_only).parent.mkdir(parents=True, exist_ok=True)
        llm_title_suffix = f"hf_data_staging | LLM {args.model} N={n_pub_l}/{n_pri_l}"
        plot_llm_bars(df_long_llm, args.out_llm_only,
                      title_suffix=llm_title_suffix, delta_mode="signed")
    finally:
        try:
            os.unlink(tmp_csv)
        except OSError:
            pass


if __name__ == "__main__":
    main()
