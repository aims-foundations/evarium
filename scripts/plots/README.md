# Plotting scripts — TOC + purpose + outputs

**Last audit:** 2026-04-20 (session 42, Phase 2 complete)

This file is the canonical index of every plotting script in the repo. When
adding a new plot, register it here.

## Migration status — **Phase 2 complete**

All legacy `scripts/plot_*.py` and `scripts/aggregate_*.py` scripts migrated into
the `scripts/plots/` and `scripts/aggregate/` packages. Invoke with
`python -m scripts.plots.<module>` or `python -m scripts.aggregate.<module>`.

**Phase 1** (done): archived 3 stale prototypes (`scripts/archive/`), added this
TOC, documented output conventions.

**Phase 2** (done): 18 scripts migrated from legacy `scripts/*.py` into the
package. Originals deleted. Sandbox-originals also deleted when superseded.

## Output directory conventions

- `output/paper/` — canonical paper figures (from `scripts.plots.paper.*`)
- `output/analysis/<subject>/` — exploratory/analysis, bucketed by subject
- `output/diagnostic/` — per-run debugging
- `<run_dir>/plots/` — per-run auto-saved (from `scripts/run_experiment.py` and per-run tools)
- `overleaf/figures/validation/` — direct-to-paper-source for a few validation figures (legacy convention, preserved)
- `output/heuristic_analysis/`, `output/llm_analysis/` — aggregation CSVs + plots (legacy, preserved; may migrate later)

Use `scripts.plots.paths` helpers: `paper_dir()`, `analysis_dir("<subj>")`, `diagnostic_dir()`, `sandbox_run_dir(batch, ...)`, `hf_data_dir(...)`.

## `scripts/plots/` package

### Top-level modules

| Module | CLI | Purpose |
|--------|-----|---------|
| `paths` | library | Output path helpers |
| `_ablation_utils` | library | Shared helpers for ablation paper modules |
| `per_benchmark` | `python -m scripts.plots.per_benchmark` | Per-benchmark gap: dumbbell + forest + paired heuristic×LLM plots |
| `per_benchmark_heatmap` | `python -m scripts.plots.per_benchmark_heatmap` | Per-benchmark × per-provider 3-panel heatmap (clean / full / drag) |
| `benchmark_aging` | `python -m scripts.plots.benchmark_aging` | Trajectory + growth-vs-age + per-benchmark-vs-sat bars |
| `single_run` | `python -m scripts.plots.single_run <run_dir>` | Incident timeline + regulatory interventions |
| `portfolio` | `python -m scripts.plots.portfolio <run_dir>` | Top-2 stacked-area + ternary simplex trajectories |
| `batch` | `python -m scripts.plots.batch <batch_dir>` | Presentation-quality summary plots from a batch of runs |
| `experiment` | `python -m scripts.plots.experiment [ids...]` | Canonical single-run comparison + `--aggregate` cross-condition dashboard. Also invokes top-2 allocations + per-benchmark dumbbell |
| `llm` | `python -m scripts.plots.llm` | 6 plots from `output/llm_analysis/` CSVs (endpoint panels, pathway flip, outcome grid, incident response, evaluator case study, divergence) |

### `scripts/plots/paper/` (canonical paper figures)

| Module | Default output | Purpose |
|--------|----------------|---------|
| `ablation_main` | `output/paper/ablation_main.pdf` | Session-38 privacy 5-condition gap trajectory panel |
| `ablation_ecosystem` | `output/paper/ablation_ecosystem.pdf` | 3-panel ecosystem ablation (incidents / safety alloc / safety cap) |
| `evaluator_alignment` | `output/paper/evaluator_alignment.pdf` | Leader-capability × benchmark alignment scatter |
| `llm_vs_heuristic_gap` | `output/paper/llm_vs_heuristic_gap.pdf` | 3-panel heuristic-vs-LLM gap trajectory overlay |
| `inflation_trajectories` | `overleaf/figures/validation/inflation_traj_*.pdf` | Score inflation trajectory (presets + ablations) |
| `validation_figures` | `overleaf/figures/validation/*.pdf` | Exploratory runs.jsonl analysis (NOTE: executes at module load, must be run directly) |

## `scripts/aggregate/` package

| Module | CLI | Purpose |
|--------|-----|---------|
| `heuristic` | `python -m scripts.aggregate.heuristic` | Data extraction for heuristic batches → `output/heuristic_analysis/*.csv` + in-line plots |
| `llm` | `python -m scripts.aggregate.llm` | Data extraction for LLM batches → `output/llm_analysis/*.csv` + in-line plots |

## Library plotting (called by the sim, not invoked directly)

| File | Purpose |
|------|---------|
| `src/plotting.py` | 5-slide per-run presentation plots (`pres_slide1..5`); called from `scripts/run_experiment.py` |
| `src/diagnostic_plots.py` | Diagnostic visualization; called by `scripts/run_diagnostics.py` |

## How to add a new plot

1. **Per-run analysis:** `scripts/plots/<name>.py`, writes to `<run_dir>/plots/` or `_paths.analysis_dir("<subj>")`.
2. **Paper-canonical figure:** `scripts/plots/paper/<name>.py`, writes to `_paths.paper_dir()` by default.
3. **Data extraction only:** `scripts/aggregate/<name>.py`.
4. Register in the relevant table above.
5. Use `from .. import paths as _paths` (inside paper/) or `from . import paths as _paths` (inside plots/) for the output helpers.

## Archived scripts

See `scripts/archive/README.md` for the 3 retired prototypes.

## Known issues / TODO

- `scripts/plots/paper/validation_figures.py` runs its analysis at module load
  (not under `if __name__ == "__main__":`). Must be invoked as a script, not
  imported. Pre-existing issue; fix when convenient.
- `scripts/plots/paper/inflation_trajectories.py` has SyntaxWarnings from
  `\_` in string literals. Cosmetic; should be `r"\_"` or `\\_`.
- Some scripts still write to legacy `output/heuristic_analysis/` and
  `output/llm_analysis/` instead of `output/analysis/<subject>/`. Convention
  migration is orthogonal to the code migration.
