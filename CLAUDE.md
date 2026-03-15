# Project: AI Evaluation Ecosystem Simulation (eval_sim)

## Environment

- **OS:** Windows (native, NOT WSL)
- **Shell:** PowerShell / cmd — do NOT use bash-isms (e.g. `uname`, `make`, `zip`)
- **Python:** 3.12
- **Paths:** Use forward slashes or raw strings. Never assume Unix paths.
- **Package manager:** pip

## Project Paths

- **Project root:** `C:\Users\yashd\Desktop\evaluation-ecosytem-project\evaluation-ecosystem-simulation\`
- Always search from the project root, not from `/` or `~`
- Key entry points:
  - `scripts/run_experiment.py` — editable experiment config file (edit & run)
  - `scripts/run_llm_now.py` — CLI-driven quick experiments
  - `src/simulation.py` — core sim loop, SimulationConfig, provider config presets

## Working Style

- When the user asks to investigate or fix something, ask for context if unsure rather than spending many turns exploring the codebase
- Do not solve extra problems or add unrequested features
- When editing JSON files (especially `experiments/index.json`), validate syntax after editing — trailing commas have caused failures multiple times
- Before long-running experiments, do a preflight check: validate JSON configs, test LLM provider connectivity, verify output directory exists
- Do not use unknown unicode alphabet (for example, tick marks or crosses to indicate success or failure). They cause errors and cannot be parsed always.

## Planning & Implementation

- **Before implementing any multi-step feature, present a plan and wait for user approval.** Do not start writing code until the user confirms the approach.
- When asked to plan, produce ONLY a plan document — no code changes at that stage.
- When asked to implement, scope your work to what was explicitly requested. Implement phase by phase if the plan has multiple phases, unless told otherwise.
- If a task touches more than 2-3 files, stop and confirm the approach before proceeding.

## Jupyter Notebooks

- Do NOT use NotebookEdit to create or edit notebooks — it fails frequently
- Instead, provide code as copy-paste snippets in chat
- When working on homework problems, only address the specific problem requested

## Simulation Architecture

- Three-tier visibility: PublicState, PrivateState, GroundTruth (held by sim)
- Actors: ModelProvider, Evaluator, Consumer, Policymaker, Funder
- Provider investment portfolio: fundamental_research, training_optimization, evaluation_engineering, safety_alignment
- Providers use either heuristic or LLM mode for planning
- LLM providers: openai, anthropic, ollama, gemini (set via `LLM_PROVIDER` env var)
- Experiment results logged to `hf_data/` via DirectoryLogger (canonical) or `sandbox/experiments/` for local runs
- Incremental round logging: `rounds.jsonl` (one JSON line per round, written live)
- Always update stakeholders.md when making changes to the simulation so that the documentation is up to date. Confirm if unsure.
- Always update TODO.md when implementing something from it (remove the item) or when identifying new work to track (add it).

## File Structure Quick Reference

```
evaluation-ecosystem-simulation/
├── src/                          # Core simulation source
│   ├── simulation.py             # Main sim loop, SimulationConfig, provider presets
│   ├── visibility.py             # PublicState, PrivateState, GroundTruth
│   ├── llm.py                    # Multi-provider LLM integration
│   ├── experiment_logger.py      # ExperimentLogger (DirectoryLogger for hf_data writes)
│   ├── plotting.py               # Visualization dashboards (per-experiment)
│   ├── game_log.py               # Natural language game log generator
│   ├── incidents.py              # Incident generation/management
│   ├── diagnostics.py            # Simulation diagnostics (aggregates across runs)
│   ├── diagnostic_plots.py       # Diagnostic visualization
│   └── actors/
│       ├── model_provider.py     # ModelProvider: plan/observe/reflect/execute
│       ├── evaluator.py          # Evaluator, Benchmark, Regulation classes
│       ├── consumer.py           # ConsumerMarket with market segments
│       ├── policymaker.py        # Policymaker: graduated interventions (media-aware)
│       ├── funder.py             # Funder: VC/gov/foundation types (media-aware)
│       └── media.py              # Media/TechPress actor
│
├── scripts/                      # Entry points and analysis tools
│   ├── run_experiment.py         # Edit & run experiments (main entry point)
│   ├── run_llm_now.py            # CLI-driven quick experiments
│   ├── rerun_experiment.py       # Rerun a past experiment from config.json
│   ├── final_plots.py            # Combined multi-experiment plots (8 plots + 3 CSV tables)
│   ├── create_final_plots.py     # Older combined plots (partially broken — prefer final_plots.py)
│   ├── explore_benchmark_plots.py# Benchmark-level gaming visualizations (merged into final_plots.py)
│   ├── plot_inflation_trajectories.py  # Score inflation trajectory plots
│   ├── compare_experiments.py    # Side-by-side experiment comparisons
│   ├── replot.py                 # Regenerate plots for existing experiments
│   ├── analyze_existing.py       # Analyze existing experiment data
│   ├── analyze_registry.py       # Analyze the run registry
│   ├── build_run_registry.py     # Build a registry index of completed runs
│   ├── explore_runs.py           # Explore and inspect runs
│   ├── generate_preset_configs.py# Generate preset experiment configs
│   ├── sync_hf_data.py           # Sync hf_data/ to/from Hugging Face
│   ├── run_diagnostics.py        # Run diagnostics on an experiment
│   ├── run_phase1_qwen.sh        # Shell: run Phase 1 with Qwen model
│   └── run_phase5_heuristic.sh   # Shell: run Phase 5 heuristic baseline
│
├── hf_data/                      # Canonical experiment outputs (primary store)
│   │                             # Experiments run on cluster; outputs stored on HuggingFace.
│   │                             # hf_data/ is the local mirror. Use sync_hf_data.py to sync.
│   ├── llm_core/                 # LLM runs (claude-sonnet-4-6/, qwen-235b/, llama-70b/)
│   ├── heuristic_baseline/       # Phase 5: 27 conditions x 30 seeds
│   ├── claude_archive/           # Legacy Claude 3.5 Sonnet runs exp_001-015
│   └── test/                     # Dev/exploratory runs (--dev flag)
│
├── sandbox/
│   └── experiments/              # Local convenience store for small/test runs
│
├── output/
│   └── diagnostics/              # Diagnostic outputs (aggregated across runs, run locally)
│
├── external-validation/          # Real-world data for validating sim against empirical trends
│   ├── data/
│   │   ├── raw/                  # Raw data: helm/, market/, paperwithcode/
│   │   └── processed/            # Processed CSVs + JSONs (benchmarks, market share, sim exports)
│   ├── plots/                    # Validation comparison plots
│   └── scripts/                  # Fetch, normalize, and plot scripts
│
├── docs/
│   ├── stakeholders.md           # Architecture reference (UPDATE when making sim changes)
│   ├── experiment_comparison_protocol.md
│   ├── results_analysis.md
│   ├── US_vs_EU_Comparison_Guide.md
│   ├── evaluator_business_model_case_study.md
│   ├── policy_intervention_case_study.md
│   ├── exp039_vs_exp040_eu_vs_us_sanctions.md
│   ├── mainfig.tex               # TikZ main figure
│   └── draft_paper.pdf           # Working paper draft
│
├── reproduce.sh                  # Top-level reproduction script
├── run_phase.sh                  # Run a specific experiment phase
└── run_qwen_all_phases.sh        # Run all phases with Qwen model
```

**Note on paper (`overleaf/`):** The LaTeX paper lives at `../overleaf/` (one level up, in `evaluation-ecosytem-project/overleaf/`). This is intentional — the paper is not nested inside the simulation repository.

### Key bugs fixed (for reference)
- `src/simulation.py` line ~775: `if round_num > 0 and self.config.enable_incidents:` — was missing `enable_incidents` check; caused ablations to still generate incidents
- `scripts/rerun_experiment.py`: `policymaker_configs` was not extracted/passed to `sim.setup()`; `sim.consumers` (deprecated empty list) replaced with `sim.consumer_market`

### Plotting
- `final_plots.py` is the canonical multi-experiment analysis script
- Run: `python scripts/final_plots.py <exp_num1> <exp_num2> [run_label]`
- Outputs to `output/experiments/plots_<run_label>/`
- Uses tueplots NeurIPS styling + matplotlib; requires LaTeX (TinyTeX on Windows)
- TinyTeX packages needed: `type1cm`, `cm-super`, `underscore`, `dvipng`
- tlmgr path: `C:/Users/yashd/AppData/Roaming/TinyTeX/bin/windows/tlmgr.bat`

### Documentation
- `docs/stakeholders.md` — Comprehensive architecture doc (UPDATE when making sim changes)
- Always update `TODO.md` when implementing from it or identifying new work
