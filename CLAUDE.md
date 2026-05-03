# Project: AI Evaluation Ecosystem Simulation (eval_sim)

## Environment

- **OS:** Windows (native, NOT WSL)
- **Shell:** PowerShell / cmd — do NOT use bash-isms (e.g. `uname`, `make`, `zip`)
- **Python:** 3.12
- **Paths:** Use forward slashes or raw strings. Never assume Unix paths.
- **Package manager:** pip
- **Background processes:** Shell backgrounding (`&`, `nohup`) does NOT survive parent exit on Windows/Git Bash. For long-running experiments, use separate `run_in_background: true` Bash tool calls — one per process.

## Project Paths

- **Project root:** `C:\Users\yashd\Desktop\evaluation-ecosytem-project\evaluation-ecosystem-simulation\`
- Always search from the project root, not from `/` or `~`
- Key entry points:
  - `scripts/run_experiment.py` — editable experiment config file (edit & run)
  - `src/simulation.py` — core sim loop, SimulationConfig, provider config presets

## Working Style

- Do not solve extra problems or add unrequested features
- When editing JSON files (especially `experiments/index.json`), validate syntax after editing — trailing commas have caused failures multiple times
- Before long-running experiments, do a preflight check: validate JSON configs, test LLM provider connectivity, verify output directory exists
- Do not use unknown unicode alphabet (for example, tick marks or crosses to indicate success or failure). They cause errors and cannot be parsed always.

## Planning & Implementation

- When asked to implement, scope your work to what was explicitly requested. Implement phase by phase if the plan has multiple phases, unless told otherwise.
- If a task touches more than 2-3 files, stop and confirm the approach before proceeding.

## Jupyter Notebooks

- Do NOT use NotebookEdit to create or edit notebooks — it fails frequently
- Instead, provide code as copy-paste snippets in chat
- When working on homework problems, only address the specific problem requested

## Simulation Architecture

- Three-tier visibility: PublicState, PrivateState, GroundTruth (held by sim)
- Actors: ModelProvider, Evaluator, Consumer, Regulator, Funder
- Provider investment portfolio: rd, safety, product (sum to 1.0)
- Providers use either heuristic or LLM mode for planning
- LLM providers: openai, anthropic, ollama, gemini (set via `LLM_PROVIDER` env var)
- Experiment results logged to `hf_data/` via DirectoryLogger (canonical) or `sandbox/experiments/` for local runs
- Incremental round logging: `rounds.jsonl` (one JSON line per round, written live)
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
│       ├── regulator.py          # Regulator: graduated interventions (media-aware)
│       ├── funder.py             # Funder: VC/gov/foundation types (media-aware)
│       └── media.py              # Media/TechPress actor
│
├── scripts/                      # Entry points and analysis tools
│   ├── run_experiment.py         # Edit & run experiments (main entry point)
│   ├── rerun_experiment.py       # Rerun a past experiment from config.json
│   ├── run_all.py                # Batch experiment runner
│   ├── run_diagnostics.py        # Run diagnostics on an experiment
│   ├── plot_experiment.py         # Single-run comparison + aggregate cross-condition plots
│   ├── plot_batch.py             # Presentation figures from a batch directory
│   ├── plot_inflation_trajectories.py  # Score inflation trajectory plots (paper figures)
│   ├── plot_validation_figures.py# Exploratory analysis of runs (paper figures)
│   ├── replot_experiment.py      # Regenerate dashboard plots for existing experiments
│   ├── registry_build.py         # Build a registry index of completed runs
│   ├── registry_analyze.py       # Analyze the run registry (hf_data/runs.jsonl)
│   ├── generate_preset_configs.py# Generate preset experiment configs
│   ├── sync_hf_data.py           # Sync hf_data/ to/from Hugging Face
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

**Note on paper (`evaluation_ecosystem_overleaf/`):** The LaTeX paper lives at `../evaluation_ecosystem_overleaf/` (one level up, in `evaluation-ecosytem-project/evaluation_ecosystem_overleaf/`). This is intentional — the paper is not nested inside the simulation repository. (Renamed from `overleaf/` on 2026-04-24.)

### Key bugs fixed (for reference)
- `src/simulation.py` line ~775: `if round_num > 0 and self.config.enable_incidents:` — was missing `enable_incidents` check; caused ablations to still generate incidents
- `scripts/rerun_experiment.py`: `policymaker_configs` was not extracted/passed to `sim.setup()`; `sim.consumers` (deprecated empty list) replaced with `sim.consumer_market`

### Plotting
- `plot_experiment.py` is the canonical plotting script (single-run comparison + aggregate cross-condition)
- Single mode: `python scripts/plot_experiment.py <exp_num1> <exp_num2> [run_label]`
- Aggregate mode: `python scripts/plot_experiment.py --aggregate --from-sandbox [--preset eu]`
- Outputs to `output/final-plots/` (single) or `output/aggregate_plots/` (aggregate)
- Uses tueplots NeurIPS styling + matplotlib; requires LaTeX (TinyTeX on Windows)
- TinyTeX packages needed: `type1cm`, `cm-super`, `underscore`, `dvipng`
- tlmgr path: `C:/Users/yashd/AppData/Roaming/TinyTeX/bin/windows/tlmgr.bat`

### Documentation
- `docs/stakeholders.md` — Living architecture reference (see Working With Claude > Session Start/End rules)
- Always update `TODO.md` when implementing from it or identifying new work

---

## Working With Claude

### Interruptions & Stopping
When the user interrupts tool use or says "stop", immediately halt the current approach and ask what they want instead. Do not continue executing commands after an interruption.

### Codebase Exploration
Do NOT explore the codebase unless explicitly asked. If you need to find a file or understand something, ask first — the user likely knows where it is. When the user provides file paths, use only those files.

### Plan vs. Implement
Do NOT implement anything until explicitly asked. Default to planning and discussion first. When the user says "plan" or "design", stay in that mode — produce a plan document only, no code changes.

### Minimal Targeted Changes
When editing files, make minimal targeted changes. Do not refactor, reorganize, rename, or "fix" things the user did not ask about.

### Session Start: Load Architecture Context
At the start of any session involving simulation code or architecture, read `docs/stakeholders.md` before taking action. This is the living reference for how actors are modeled and how simulation mechanics work.

### Session End: Update Docs & Write Handoff
1. If any structural changes were made to the simulation during the session (new actors, changed mechanics, updated state representations, etc.), update `docs/stakeholders.md` to reflect them before the session ends. Ask if unsure whether a change is structural.
2. Before ending any non-trivial session, write or update `SESSION_HANDOFF.md` in the project root with three sections:
   - **Completed:** what was finished this session
   - **In Progress:** anything partially done, with current state
   - **Next Steps:** what to do next session
   Keep it under 30 lines.

### Task Scoping (Phase-Based Work)
Break large multi-step tasks into explicit phases. Default structure: Phase 1 = plan only, Phase 2+ = implement. Do not proceed to the next phase without user approval. This allows clean exit between phases without losing progress.

### Front-Loading Context
When the user provides explicit file paths in a request, use only those files. Do not search for additional files unless asked. If file paths are not provided and they are needed, ask before exploring.
