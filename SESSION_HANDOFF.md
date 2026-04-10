# Session Handoff -- 2026-04-09 (session 27)

## Completed (session 27)
- **Heuristic baseline rerun:** 1,620 runs (18 conditions x 3 policies x 30 seeds) on current code. All runs in `sandbox/experiments/heuristic/<cond_policy>/seeds/seed_<N>/`. Seeds saved to `SEEDS.txt`.
- **`dynamic_consumer_market` now default `True`.** New `static_consumer_market` ablation is the inverse. Replaces old `dynamic_market` condition.
- **Refactored dev output paths** in `run_experiment.py` to nested structure: `sandbox/experiments/<batch>/<mode>/<cond_policy>/seeds/seed_<N>/`. Mirrors canonical hf_data layout.
- **`scripts/aggregate_heuristic.py`** (new, ~1100 lines): produces `heuristic_summary.csv`, `outcome_typology.csv` (1,620 rows), `pattern_matrix.csv`, 54 trajectory CSVs, `ablation_effects.csv` (459 effects, 152 significant). Plus 31 plots: quantile trajectories, outcome heatmaps, pattern heatmap, ablation forest plots. Outputs to `output/heuristic_analysis/`.

## In Progress
- Sessions 16-27 code changes still uncommitted
- Aggregation plots are functional but readability needs work (see TODO.md)

## Open findings worth investigating
- **Negative `total_gap` (~-0.017)** across all conditions: scores *underestimate* satisfaction. Either calibration shifted post-session-26 weight changes, or it's a real signal worth interpreting.
- **`safety_incident_response` pattern fails ~97%** of seeds: heuristic providers don't react to incidents in expected ways
- **`aligned_benchmarks` shows largest positive gap delta** in forest plots — counterintuitive
- **`score_inflation` and `gaming_persistence` patterns fail across all 54 conditions** — consistent with the negative gap finding

## Next Steps (priority order)
1. **Interpret heuristic baseline results** — investigate negative gap, failing patterns. Are these calibration issues or genuine findings?
2. **Fix aggregation plot readability** — facet trajectories, split forest plots (logged in TODO.md)
3. **Calibrate saturation threshold** — carryover from session 26
4. **Paper updates** — experiments section now has real numbers to use
5. **Commit sessions 16-27 changes**
