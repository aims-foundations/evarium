# Project: AI Evaluation Ecosystem Simulation (eval_sim)

## Environment

- **OS:** Windows (native, NOT WSL)
- **Shell:** PowerShell / cmd — do NOT use bash-isms (e.g. `uname`, `make`, `zip`)
- **Python:** 3.12
- **Paths:** Use forward slashes or raw strings. Never assume Unix paths.
- **Package manager:** pip


Add under a new ## Jupyter Notebooks section near the top of CLAUDE.md\n\nWhen the user asks for code for Jupyter notebooks, provide it as copy-paste snippets in chat rather than attempting to use NotebookEdit or Write tools to create/edit .ipynb files directly. NotebookEdit is unreliable and frequently times out.
Add under ## Workflow Rules or ## General Instructions section\n\nAlways update documentation (README.md, stakeholders.md, and any relevant .md files) when making code changes. Do not wait to be reminded.
Add under ## Environment section at the top of CLAUDE.md\n\nThis project runs on Windows (not WSL/Linux). Use Windows-compatible commands (e.g., PowerShell, `python` not `python3`, backslash-aware paths). Do not assume bash/WSL unless explicitly told otherwise.
Add under ## Common Pitfalls or ## Editing Rules section\n\nWhen editing JSON files (especially index.json or config files), validate JSON syntax after editing. Trailing commas and malformed JSON have caused experiment failures multiple times.
Add under ## Workflow Rules section\n\nBefore implementing, always present a plan and wait for user approval. Do not start coding multi-step features without confirmation. When asked to plan, produce ONLY a plan document — no code changes.

## Project Paths

- **Project root:** `C:\Users\yashd\Desktop\generative_agents\eval_sim\`
- Always search from the project root, not from `/` or `~`
- Key entry points:
  - `run_experiment.py` — editable experiment config file (edit & run)
  - `run_llm_now.py` — CLI-driven quick experiments
  - `simulation.py` — core sim loop, provider config presets

## Working Style

- When the user asks to investigate or fix something, ask for context if unsure rather than spending many turns exploring the codebase
- Do not solve extra problems or add unrequested features
- When editing JSON files (especially `experiments/index.json`), validate syntax after editing — trailing commas have caused failures multiple times
- Before long-running experiments, do a preflight check: validate JSON configs, test LLM provider connectivity, verify output directory exists
- Do not use unknown unicode alphabet (for example, tick marks or crosses to indicate success or failure). They cause errors and cannot be parsed always.

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
- Experiment results logged to `experiments/` via ExperimentLogger
- Incremental round logging: `rounds.jsonl` (one JSON line per round, written live)
- Always update stakeholders.md when making changes to the simulation so that the documentation is up to date. Confirm if unsure.

## File Structure Quick Reference

### Core Files
- `simulation.py` — Main sim loop, SimulationConfig, provider config presets
- `visibility.py` — State classes: PublicState, PrivateState, GroundTruth
- `llm.py` — Multi-provider LLM integration and prompt templates
- `experiment_logger.py` — ExperimentLogger for systematic logging
- `plotting.py` — Visualization dashboards
- `game_log.py` — Natural language game log generator

### Actor Modules (actors/)
- `model_provider.py` — ModelProvider with plan/observe/reflect/execute cycle
- `evaluator.py` — Evaluator, Benchmark, Regulation classes (evolution + introduction)
- `consumer.py` — ConsumerMarket with market segments (proportional switching)
- `policymaker.py` — Policymaker with graduated interventions (media-aware)
- `funder.py` — Funder (VC, gov, foundation types; media-aware)
- `media.py` — Media actor (TechPress) with coverage influence

### Experiment Results (experiments/)
- `index.json` — Experiment index (VALIDATE JSON after edits!)
- `exp_XXX_name/` — Individual experiment folders with history, plots, logs
- `rounds.jsonl` — Incremental round-by-round data

### Documentation
- `stakeholders.md` — Comprehensive simulation architecture and design doc (UPDATE when making changes)

