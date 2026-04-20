# Session Handoff — 2026-04-20 (session 42: F1 heuristic rewrite + cadence reconciliation + per-benchmark gap reframing)

## Completed
- **F1 — `_plan_heuristic` rewrite** (`src/actors/model_provider.py:508-579`, `src/simulation.py:808-830`): removed recurring profile-string modifiers (the `+=0.05 safety/round` ratchet); added 3 universal rules (share trend, CRISIS narrative, own-intervention). Added 3 ctx signals (`own_share_history`, `narrative_state`, `own_recent_interventions`). Safety cap 0.55→0.70. Uncommitted.
- **1,500-run post-F1 re-baseline** (`sandbox/experiments/heuristic_apr19_postF1/`, seeds 1000-1029). Apex/Orion `safety_last` std 0.000 → 0.13-0.15. **Regime shift**: leader flipped Mirage 47% → 0.9%, Orion 18% → 64%. HHI 0.27 → 0.56. Prior Mirage-dominance confirmed as policy artifact of profile ratchets.
- **6 LLM diagnostic runs** (anthropic API, seed 2026, 30 rounds): baseline, private_only, initial_uniform_allocation, no_regulator, no_incidents, fixed_public. Regulator bites in LLM (Apex 0.62→0.16 share w/o it); `bo_mean` pinned at 0.80 in both modes; `fixed_public` N=1 shows +61% |gap| on shared benchmarks (validates aging hypothesis).
- **Per-benchmark gap reframing + 3 story plots** (`heuristic_apr19_postF1/plots_story/`): dumbbell, forest, side-by-side heuristic+LLM. 8/10 benchmarks show positive gap; Agentic Tasks excluded as calibration outlier (cdw 0.75-agentic vs cap 0.26-agentic).
- **Cadence reconciliation to canonical 4**: fixed 10 locations across `simulation.py`, `evaluator.py`, `run_experiment.py`, `stakeholders.md`, `A_architecture.tex`. `fee_per_submission` default 0.03 → 0.05.
- **2 new structural ablations**: `cadence_static`, `cadence_every_8`. Smoke-tested; not yet run at scale.
- **Paper Appendix A** updated with cadence=4 schedule table + "Schedule calibration" paragraph mapping each sim benchmark to real release date.

## In Progress
Nothing running. No commits.

## Next Steps (priority)
1. **Commit** session-42 edits. Split: (a) F1 heuristic rewrite, (b) cadence reconciliation + 2 new ablations, (c) `fee_per_submission` default.
2. **Cadence ablation runs** — 2 new struct × 5 privacy × 30 seeds = 300 heuristic runs (~30 min); +1-2 LLM seeds at each for mode consistency.
3. **LLM validation at N≥3** per privacy condition — confirm privacy + aging findings beyond seed 2026.
4. **F2/F3/F4 re-scoped** — regulator/funder/media bite is a heuristic-specific gap (LLM handles it); turn into heuristic Rule strengthening, not sim redesign.
5. **Paper figures** — integrate Plot 1/2/3 into section 5 / Appendix H (per-benchmark gap story).
6. **Caveat or re-baseline** — existing postF1 batch used cadence=5 (pre-reconciliation); new canonical is 4. Flag as caveat or re-run at 4.
7. **Post-deadline**: eval-as-company + benchmark-sponsorship redesign with per-benchmark metrics (Task #23).

## Breaking
- Post-F1 heuristic results incompatible with pre-F1 (regime shift: Mirage-dominance → Orion-dominance). All existing heuristic figures need re-caption or re-baseline.
- Cadence default changed 5 → 4; any existing config.json claiming cooldown=5 won't match new defaults.
