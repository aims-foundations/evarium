# Session Handoff — 2026-04-23 (session 49e end: calibration + experiment plan + paper structural revisions)

## Completed

### Sim calibration + experiment plan (parallel stream)

**Dynamic evaluator 40r run** (`_llm_apr23_v1/llm/dynamic_evaluator_40r_s101/`, seed=101, Sonnet). 9 LLM decisions (4 create / 2 retire / 3 none). Evaluator showed coherent curriculum design with explicit self-correction (R20 retired R13-created Agentic Tasks) + leaderboard-adoption correlation as primary signal. Suite evolved 4→6 benchmarks. **Decision: retain as single-seed Appendix artifact; skip multi-seed** — action space narrow enough that proper paper claim would need 3-mode comparison (LLM dynamic vs fixed_sequence vs randomized_pool), not more seeds. E4 downgraded to 0 additional runs.

**Media calibration tweaks (interview-informed)** in `src/actors/media.py`: `_media_sample_size` 4→6; Option A benchmark-milestone crossings (70/80/90% thresholds fire weight=2.0 headline); Option B rival-closes-gap (narrow by >0.008 → headline + attention boost to #2; calibrated down from 0.015). Dry-replay baseline seed=1: +22–26 LB headlines/40r.

**Incident exposure-multiplier floor** 0.5→0.3 (`src/incidents.py:251`). Restores share-proportional scaling; drops OpenCore incidents ~35%, mid-share ~15%, dominant ~15%.

**Experiment plan refreshed** (`docs/experiment_plan.md`): Tier 1 (25 privacy ladder + 11 exogenous = 36 runs); Tier 2 (14 × 2 seeds including `no_opensource`, `homogeneous_consumers`, `initial_uniform_capability`); Tier 3 (CS3/CS2/eval_as_company + 5 Opus paired). Grand total 65 Sonnet + 5 Opus. Seeds 101–105 locked. 4 decision gates. `stakeholders.md` formula table + changelog updated.

### Paper structural revisions + infrastructure (parallel stream)

**Appendix I (LLM prompt templates)** — `overleaf/appendix/I_prompts.tex`, registered in `9appendix.tex`. Reframed provider system prompt + 6 identity blocks, funder + regulator + dynamic-evaluator prompts, user-message schemas, apparatus-vocabulary audit.

**Single-run loop figure** — `scripts/plots/paper/single_run_loop.py` → `overleaf/figures/single_run_loop.pdf`. 2×2: market share / incidents+interventions / allocations over time / per-benchmark dumbbell (all 13 benchmarks incl. Agentic Tasks + Function Calling outliers). §5.1 rewrite sketched; held for results.

**Appendix J (Extended Related Work)** — new file, 4 subsections (supply-chain/value-chain/evaluation-layer positioning + LLM-ABM lit + alternative methodologies + governance analogues). 5 new bib entries: `hopkins2025ai`, `cobbe2023supply`, `widder2023dislocated`, `bommasani2023ecosystem`, `porter1985competitive`.

**Main-body cuts:**
- `2relatedwork.tex`: 120 → 13 lines. Ecosystem-framing opener grounds the "evaluation as distinct layer" argument.
- `1intro.tex`: P2/P3 collapsed → single ecosystem+analogues paragraph pointing to J; contribution bullets tightened (~2× → ~1×); bullet-3 TODO marker preserved.
- `3system.tex`: actor-description intro merged + mechanics-leaking sentences cut from Providers / Evaluation Providers / Regulators / Media.
- `4simulation.tex`: 168 → 126 lines. Hyperparams table moved to `B_parameters.tex`. Sang's methodological-choice comment resolved via round-based/sequential-phasing paragraph; simflow diagram moved to `A_architecture.tex:app:round-protocol` (Algorithm 1 stays in §4).

**Compile-error fixes:** 4 missing bib entries (`singh2024benchmark`, `xu2024contamination`, `dominguezolmedo2024training`, `rhee2006liability`); hyperref math-shift in `C:67` via `\texorpdfstring`; 3 broken fig refs in H rewritten to drop main-body pointers; `D_incidents` overfull (126pt) fixed via `\footnotesize` + `p{5.3cm}`.

**TODO.md** — added "Revise abstract" under Paper (NeurIPS).

## In Progress

Nothing running.

## Next Steps (priority)

1. **Commit** all uncommitted work across both streams (sim calibration + experiment plan + paper infra + structural revisions). BLOCKING Tier 1 launches.
2. **`recent_exogenous_events` plumbing** (~10–20 LOC) — unblocks E2.
3. **Tier 1 launch** — E1 privacy ladder (25 runs, seeds 101–105) + E2-smoke EV1.
4. **Post-Tier-1 analysis** — verify post-49d findings replicate (Apex drift resolution, OpenCore safety-leader, VC herding, Orion rebuild).
5. **Paper post-results pass** — §5.1 rewrite (figure swap + sketch), abstract rewrite, §6 conclusion update, contribution bullet 3 finalise.
6. **Tier 2 ablation sweep** (14 runs); **Tier 3** after decision gate (CS3/CS2/eval_as_company/Opus).
7. **Deferred cluster** (user: flag for later): E_pimmur expand/fold, F_diagnostics populate/cut, orphan 6scope archive/absorb. Not to touch until ready.
8. **Paper submission mechanics** — remaining overfull hboxes, float-only pages in H, author de-anon, checklist.

## Breaking
- Session-49d-end sim changes (media + incident floor) affect Tier 1 runs; pre-change `_llm_apr23_v1` runs remain valid as reference.
- Session 49e paper structural revisions: main-body trim ~⅔ page, hyperparams table moved to appendix, related-work compressed, new Appendix J. Uncommitted.
- Heuristic N=30 session-49b runs unaffected.
