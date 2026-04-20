# Archived scripts

Scripts retired from active use. Kept for reference only — not linked from
`scripts/plots/README.md` and not expected to work against current data schema.

## Contents

| Script | Retired | Reason |
|--------|---------|--------|
| `prototype_headline_figures.py` | 2026-04-20 (session 42) | Dev prototype for NeurIPS headline figures; superseded by `scripts/plot_ablation_main.py` + `plot_ablation_ecosystem.py` and the session-42 per-benchmark gap story plots (`sandbox/.../plot_gap_story.py`). |
| `prototype_grid_cell.py` | 2026-04-20 (session 42) | Dev prototype for market-structure grid figures; never promoted. Reference for the grid-cell pattern if ever needed. |
| `aggregate_example.py` | 2026-04-20 (session 42) | Worked-example aggregation walkthrough; superseded by `scripts/aggregate_heuristic.py` and `scripts/aggregate_llm.py`. Keep only if the pedagogical narrative is useful for onboarding. |

## Restore policy

If you need to revive one of these, copy to `scripts/` and register in
`scripts/plots/README.md`. Do not reach into `scripts/archive/` directly from
other scripts.
