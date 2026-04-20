"""Output-directory conventions for plotting scripts.

Three top-level buckets under `output/`:

  paper/         Canonical paper-bound figures (pdf + png).
                 Replaces legacy `output/final-plots/` and `output/figures_paper_headroom/`.
  analysis/<k>/  Exploratory / multi-condition analysis, bucketed by subject.
                 Replaces legacy `output/heuristic_analysis/`, `output/llm_analysis/`,
                 `output/aggregate_plots/`, `output/presentation_plots/`.
  diagnostic/    Per-run / debugging plots. Replaces legacy `output/diagnostics/`.

Per-run auto-saved plots from `run_experiment.py` stay at `<run_dir>/plots/` — they
belong to the run, not to the global output convention.
"""
from __future__ import annotations

import os

# Resolve project root from this file's location: scripts/plots/paths.py -> ../../
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(_THIS_DIR, "..", ".."))
OUTPUT_ROOT = os.path.join(PROJECT_ROOT, "output")


def paper_dir() -> str:
    """Canonical paper-figure directory. `output/paper/`."""
    d = os.path.join(OUTPUT_ROOT, "paper")
    os.makedirs(d, exist_ok=True)
    return d


def analysis_dir(subject: str) -> str:
    """Exploratory analysis bucket. `output/analysis/<subject>/`.

    Args:
        subject: short kebab-or-snake-case name (e.g. "per_benchmark_gap",
                 "benchmark_aging", "ablation_matrix"). Used as the subdirectory.
    """
    if not subject or "/" in subject or "\\" in subject:
        raise ValueError(f"bad subject {subject!r} — use a short name, no separators")
    d = os.path.join(OUTPUT_ROOT, "analysis", subject)
    os.makedirs(d, exist_ok=True)
    return d


def diagnostic_dir() -> str:
    """Diagnostic / debugging bucket. `output/diagnostic/`."""
    d = os.path.join(OUTPUT_ROOT, "diagnostic")
    os.makedirs(d, exist_ok=True)
    return d


def sandbox_run_dir(batch: str, *subpath: str) -> str:
    """Resolve a path under `sandbox/experiments/<batch>/` for reading inputs
    (CSVs, rounds.jsonl, etc). Writes should go to the output buckets above.
    """
    return os.path.join(PROJECT_ROOT, "sandbox", "experiments", batch, *subpath)


def hf_data_dir(*subpath: str) -> str:
    """Resolve a path under `hf_data/` for canonical run inputs."""
    return os.path.join(PROJECT_ROOT, "hf_data", *subpath)
