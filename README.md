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
1. Edit parameters in `run_experiment.py` (providers, benchmarks, rounds, etc.)
2. Toggle `llm_mode=True` for LLM-driven agents or `llm_mode=False` for heuristic mode
3. Run: `python run_experiment.py`

Additional configuration options are available in `simulation.py` (`SimulationConfig` class).

For quick CLI tests: `python run_llm_now.py --rounds 5 --provider openai`

## Documentation

See `stakeholders.md` for detailed documentation on the simulation model, stakeholders, and experiment infrastructure.

