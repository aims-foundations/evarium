# Session Handoff — 2026-04-24 (session 51 end: paper restructure + eval_lag canonicalization + batch launch)

## Completed

### Paper restructure (summary — see `memory/session51_paper_restructure.md` for detail)
- §5 reordered: Privacy → Validation → Limitations → Case studies.
- §5.1 Single-run folded into §4.4 "Example run". Abstract compressed 280→205 words.
- Appendix 12→11 (A–K): PIMMUR merged into F_validation, G_scope removed, B.regulatory-calibration → A. All files renamed A_architecture / B_design_rationale / C_incidents / D_prompts / E_validation / F_llm_results / G_sonnet_opus / H_case_studies_ext / I_limitations_ext / J_parameters / K_extended_related_work.
- 23 new BibTeX entries (in `references.bib`) + 5 quick-win text→bibkey swaps; remaining ~20 swaps in K_parameters queued.
- Deleted unused `sections/5diagnostic.tex` + `sections/6scope.tex`. British→American sweep, showcomments→0. 0 undefined refs.

### Sim code (structural)
- **`src/simulation.py:179`: `evaluation_lag` default changed 0→3.** Aligns the default with the paper's K=3 empirical calibration; privacy-ladder conditional override in `run_experiment.py:715` is now redundant but kept as explicit. `stakeholders.md` top blockquote updated.

### Data hygiene
- `sandbox/experiments/_ev1_smoke/` + `sandbox/experiments/_tier2_ablations/` moved to `_preserved/` (both were at lag=0; orphaned from canonical K=3 evidence base). Retained as reference + future paired-test baseline.

### Experiment plan + launch
- `docs/experiment_plan.md` rewritten with concrete $400 launch plan (5 batches, decision gates, costs).
- **9 runs launched in background (3 shells × 3 runs, ~$108, ~3h wall-clock, all at lag=3 new canonical):**
  - Shell 1 `bncoo5z43` → `_core_privacy`: `public_only_s46`, `private_only_s46`, `iid_holdout_s46`
  - Shell 2 `bdfv2tug0` → `_tier1_ev1` (new batch): `ev1_deepseek_s43/s44/s45`
  - Shell 3 `b7kibz0fa` → fresh `_tier2_ablations`: `no_incidents_s43`, `initial_uniform_capability_s43`, `homogeneous_consumers_s43`

## In Progress
- **3 background shells running** (shell IDs above). Expected wall-clock ~3h; notifications will fire on completion.

## Next Steps (priority)
1. **Await 3 shells; verify completion + round counts.** Flag any fallbacks >2% per run for re-queue.
2. **Post-launch analysis:** refresh `scripts/plots/per_benchmark_core_privacy.py` + `ablation_main_llm.py` against new data. Verify §5.2 HHI claim survives N=5, Mirage-under-initial_uniform_cap at s43 (seed-robustness check).
3. **Launch Batch 2 of re-dos: 4 Tier 2 ablations at s42 lag=3** (`no_funders`, `no_regulator`, `no_media`, `no_opensource`) — paired with `_preserved` s42 lag=0 for lag-effect test. ~4 runs, ~$50.
4. **Commit** — session 48–51 sim + paper changes still uncommitted.
5. **NeurIPS checklist decisions** (6 CONFIRM markers): IRB, code/data release, broader impacts, compute estimate.
6. **Text→bibkey swap pass for K_parameters.tex** — ~20 author-year refs, bibkeys now in `references.bib`.
7. **Optional Batch 3:** 3 hot Tier 2 ablations × s42 lag=3 + all 7 × s43 lag=3 for full coverage (~$120).

## Breaking
- `evaluation_lag` default 0→3: any code path that depends on the old default silently gets K=3 now. `dynamic_evaluator` heuristic (previously ran at lag=0) would now get lag=3 if re-run — verify this is desired if re-running.
- `_tier2_ablations/` contents completely swapped (old lag=0 runs → `_preserved/`; new lag=3 runs landing). Plots that point at the directory need no path change, but results will differ.
- Appendix letter mapping A–L → A–K (from earlier in session) — any external doc citing old letters is stale.
