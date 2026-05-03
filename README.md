# AI Evaluation Ecosystem Simulation

A multi-agent simulation of the AI evaluation ecosystem: model providers, evaluators, consumers, regulators, funders, and media. Provider strategy emerges from portfolio allocation (R&D / safety / product) and per-benchmark focus weights. Goodhart-style score--satisfaction divergence arises when benchmark-need weights misalign with consumer-need weights, not from any explicit gaming lever.

The simulation supports two execution modes:
- **Heuristic mode** — deterministic rules at every actor; no-LLM baseline.
- **LLM mode** — LLM-driven planning at provider, regulator, funder, and (optionally) evaluator actors.

Inspired by the [Generative Agents](https://github.com/joonspk-research/generative_agents) approach to agent-based simulation.

## Installation

```bash
pip install -r requirements.txt
```

For LLM mode, configure a provider in `.env`:
- `LLM_PROVIDER=anthropic` + `ANTHROPIC_API_KEY=...`
- `LLM_PROVIDER=openai` + `OPENAI_API_KEY=...`
- `LLM_PROVIDER=gemini` + `GOOGLE_API_KEY=...`

## Running an experiment

```bash
# heuristic baseline, 40-round single seed
python scripts/run_experiment.py --condition baseline --mode heuristic --seed 42

# LLM mode (Sonnet 4.6 default)
python scripts/run_experiment.py --condition baseline --mode llm --seed 42

# privacy-ladder ablation
python scripts/run_experiment.py --condition private_only --mode llm --seed 42
```

Output lands at `hf_data_staging/<bucket>/.../seed_N/` in the canonical 7-file slim shape (`config.json`, `metadata.json`, `rounds.jsonl`, `summary.json`, `ground_truth.json`, `game_log.md`, `dashboard.png`).

Run `python scripts/run_experiment.py --help` for the full condition list.

## Reproducing paper results

The dataset of paper-supporting runs is withheld during double-blind review; the permanent location will be released at camera-ready.

To regenerate plots or re-run a saved config:

```bash
# Re-run a saved experiment from its config.json
python scripts/rerun_experiment.py path/to/seed_dir/config.json

# Regenerate plots for an existing seed dir
python scripts/replot_experiment.py path/to/seed_dir
```

Conditions reported in the paper:
- **Privacy ladder** — 5 conditions (`public_only`, `baseline`, `private_dominant`, `private_only`, `iid_holdout`) × 10 Sonnet seeds with paired Opus / GPT-5.5 cross-model coverage
- **Sequence robustness** — 9 ecosystem-composition counterfactuals (s0–s8) × 5 privacy rungs
- **Structural ablations** — `no_incidents`, `no_funders`, `no_regulator`, `no_media`, `no_opensource`, `homogeneous_consumers`, `initial_uniform_capability`, plus interaction conditions
- **Evaluator capture** — case study at `evaluation_lag=0`
- **Exogenous shock** — `ev1_deepseek_shock` capability-release validation

## Project structure

```
src/                  Core simulation library (actors, scoring, visibility, incidents, LLM integration)
scripts/              CLI entry points + analysis tools
  run_experiment.py       main experiment runner
  rerun_experiment.py     re-run a saved config
  build_hf_metadata.py    regenerate dataset registry + manifest
  plots/                  paper-figure generators
  dashboard/              single-run 9-panel dashboard generator
  aggregate/              cross-run aggregation helpers
docs/
  stakeholders.md         canonical architecture reference
  case_studies/           policy-adjacent case study designs
external-validation/  Real-world data + validation scripts
```

## Documentation

- **`docs/stakeholders.md`** — full architecture reference (actors, state, scoring formula, parameters, design rationale)
- **`docs/case_studies/`** — designed and worked case studies: privacy ladder, evaluator capture, media shadow, benchmark sponsorship, audit & verification, transparency mandates, EU vs US regulation

## Citation

Citation details are withheld during double-blind review.
