# AI Evaluation Ecosystem Simulation

A multi-agent simulation studying Goodhart's Law in AI benchmarking: when model providers optimize for benchmark scores, the scores cease to be good measures of capability.

Simulates an AI evaluation ecosystem with model providers, evaluators, consumers, policymakers, funders, and media. Providers allocate resources between genuine capability-building (research, training) and benchmark-specific optimization (gaming). The simulation explores emergent dynamics: score inflation, consumer dissatisfaction, regulatory intervention, and capital allocation patterns.

Inspired by the [Generative Agents](https://github.com/joonspk-research/generative_agents) paper's approach to agent-based simulation.

## Installation

```bash
pip install -r requirements.txt
```

For LLM mode, install the relevant provider:
- **OpenAI/Anthropic/Gemini:** `pip install openai` (or `anthropic`, `google-genai`) and add API keys to `.env`
- **Ollama:** Install [Ollama](https://ollama.ai), pull a model (e.g., `ollama pull llama2`), and set `LLM_PROVIDER=ollama` in `.env`

## Running Experiments

**Quick start:**
1. Edit parameters in `scripts/run_experiment.py` (providers, benchmarks, rounds, etc.)
2. Toggle `llm_mode=True` for LLM-driven agents or `llm_mode=False` for heuristic mode
3. Run: `python scripts/run_experiment.py`

Additional configuration options are available in `src/simulation.py` (`SimulationConfig` class).

For quick CLI tests: `python scripts/run_llm_now.py --rounds 5 --provider openai`

## Project Structure

```
src/          # Core simulation library
scripts/      # CLI entry points
output/       # Generated artifacts (experiments, plots, comparisons)
docs/         # Documentation
tests/        # Tests
```

## Reproducing Paper Results

All 15 experiments from the paper can be reproduced from their saved configurations:

```bash
./reproduce.sh                        # run all 15 experiments (2 concurrent)
./reproduce.sh --jobs 4               # run 4 at a time
./reproduce.sh --experiments 1 2 3    # run specific experiments only
./reproduce.sh --dry-run              # preview without executing
```

Requires a `.env` file with `ANTHROPIC_API_KEY` (all experiments use LLM mode). Logs are written to `output/reproduce_logs/`.

## Documentation

See `docs/stakeholders.md` for detailed documentation on the simulation model, stakeholders, and experiment infrastructure.
