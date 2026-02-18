# TODO

## Simulation Behavior

1. Verify each actor uses ecosystem public signals when making decisions, not just their initial character profile.
2. VCs should be able to invest in non-AI companies (no need to model deeply — just allow the option).
3. Benchmark spacing should scale with total rounds (rough target: ~8 benchmarks over 50 rounds).
4. Slow down benchmark saturation; make introduction timing more realistic without overloading the system.

## Known Edge Cases

- **Same-round simultaneous saturation:** When two benchmarks saturate on the same round, the second replacement is delayed by the min-gap cooldown. Fix: allow introducing two benchmarks in one round (return a list instead of a single Benchmark). Low priority.

## Plotting

- Enhanced provider dashboard: "Evaluation Advantage" panel (premium access vs score jumps) and "Investment vs Trials" scatter.
- Enhanced summary dashboard: incident summary tile (by severity, most incident-prone provider) and evaluator business tile (budget, premium providers, revenue mix).
- New dashboard: `plot_ecosystem_dynamics_dashboard()` — incident→media→consumer flow, evaluator financial sustainability, gaming detection ROC, market concentration vs incident rate.
- Nice-to-have: interactive plots (Plotly/Bokeh), animated visualizations, comparative side-by-side dashboards.

## Infrastructure

- **`run_llm_now.py` is likely broken** — new config parameters (`enable_incidents`, `evaluator_as_company`, `enable_media`, `consumer_llm_mode`, policymaker presets, `use_case_profiles`) are not wired up. Needs sync with `run_experiment.py` structure.
- **`compare_experiments.py`** — tool to load two experiments, diff their configs, compute per-metric divergence timelines, and identify the first round of significant divergence. Would replace the current manual summary.json comparison workflow.
