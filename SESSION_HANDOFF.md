# Session Handoff — 2026-03-30

## Completed
- **Thread 9 calibration** — all core parameters set:
  - `rnd_efficiency=0.05`, `revenue_per_share=5.0` in SIMULATION config + wired into SimulationConfig
  - `focus_level_init` per provider (5 providers × 4 benchmarks) in PROVIDERS
  - Safety capability floor: 0.35 (closed), 0.03 (OS) — in `_update_ground_truth()`
  - `init_benchmark()` fix: no longer overwrites existing focus_level values
- **Variable name / dead code audit** — removed `exploitability` everywhere:
  - `evaluator.py`: removed `exploitability` field from `Benchmark`
  - `policymaker.py`: removed `compliance_audit` exploitability mutation block
  - `simulation.py`: fixed `benchmark_params` to media; removed dead compliance_audit block
  - `game_log.py`: fixed KeyError on `new_bm['validity']`/`new_bm['exploitability']`
  - `run_experiment.py`, `rerun_experiment.py`, `run_llm_now.py`: removed all `benchmark_exploitability` refs
- **LLM pass-through (major)** — `src/llm.py` fully rewritten for new arch:
  - Removed all old-arch dead code (`llm_plan_portfolio`, `llm_reflect`, `get_client`, etc.)
  - Added `call_llm()` wrapper (for `consumer.py`)
  - Wrote `PROVIDER_PLANNING_SYSTEM_PROMPT`, `_build_provider_planning_prompt`, `llm_plan_provider` (ordinal 3-lever output)
  - Fixed `llm_plan_funding` / `create_funder_planning_prompt`: replaced `believed_provider_gaming` + `consumer_satisfaction` with `market_shares` (PIMMUR compliance)
  - Smoke test: all imports + heuristic run PASS

## Deferred (in TODO.md)
1. Heuristic scoring formulas (funder `_plan_vc/gov/foundation`) diverge from stakeholders.md spec
2. LLM prompt review (PIMMUR: goal-injection, reflection coaching, "simulating" framing)
3. `run_llm_now.py` out of sync with `run_experiment.py` (new config params not wired)

## Next Steps
1. Run full 30-round experiment (all 5 providers + all actors) via `run_experiment.py --dev`
2. Inspect trajectories: Goodhart gap, market shares, incidents, funder allocations, interventions
3. LLM end-to-end smoke test: `run_llm_now.py -r 3 -p anthropic` (tests `llm_plan_provider`)
4. Thread 9 end: align heuristic funder scoring formulas with stakeholders.md spec
