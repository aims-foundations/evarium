# TODO

## Open threads to raise with collaborators

- [ ] **Interview integration in §5.3 Validation** — how should practitioner interviews enter the paper? Abstract + §3 mention them as input to framework construction; §5.3 alludes to them as a design-grounding source but defers specifics. Options: (a) separate appendix stub listing practitioner roles + which design choices each informed; (b) paragraph in §3 intro about interview methodology; (c) defer to follow-on paper. Needs collaborator input before writing.

## Paper (NeurIPS)

- [ ] **Document model snapshot IDs for reproducibility** — three-way model set: Sonnet 4.6 (`claude-sonnet-4-6`, released 2026-02-17), Opus 4.6 (`claude-opus-4-6`, released 2026-02-05), GPT-5.5 (pinned snapshot `gpt-5.5-2026-04-23`).
  - [x] **Backfill (retroactive):** `scripts/backfill_metadata_models.py` written and applied — 80 `metadata.json` files in `sandbox/experiments/**/llm/*_sonnet|*_opus|*_gpt55/seeds/seed_*/` now carry `llm_model` + `llm_provider`. 52 no-suffix legacy dirs (all under `_preserved/` and `_llm_apr23_v1/`) correctly skipped per design.
  - [x] **Prevention (forward):** `ExperimentMetadata` dataclass at `src/experiment_logger.py` got two new defaulted fields (`llm_model: str = ""`, `llm_provider: str = ""`); `DirectoryLogger.save_metadata()` accepts matching kwargs; `scripts/run_experiment.py:1191` passes resolved `LLM_MODEL` env var + `LLM["provider"]` (only when `llm_mode=True`; heuristic runs get empty strings). Backward-compatible: legacy callers and `ExperimentLogger.create_experiment` get empty defaults. In-process smoke verified the schema for LLM, heuristic, and old-signature callers — output matches the backfill exactly (same key ordering, same types).
  - [ ] **Paper + checklist:** add a Models table to the paper appendix (provider × API ID × release date × which run series) and populate the NeurIPS reproducibility checklist row. **Caveat to flag in appendix:** Anthropic does NOT publish dated snapshot IDs for the 4.6/4.7 generation (unlike Haiku 4.5 / Sonnet 4.5 which use `-YYYYMMDD` suffix). Per Anthropic docs the alias `claude-sonnet-4-6` IS the canonical ID; identical snapshots are guaranteed to share the ID. Reproducibility anchor for our runs is therefore (alias × release date × `metadata.json:created_at`), since runs predate any future re-point.
- [ ] **Sync `docs/references.md` with `evaluation_ecosystem_overleaf/references.bib`** — references.md has accumulated citations across sessions (market growth, consumer, regulator, funder, benchmark-privacy / Singh 2024 / Dominguez-Olmedo 2024 / Xu 2024 / Deng 2024 / Epoch AI data / Kaggle LLM leaderboard). Sync pass to bib; verify `\cite{}` calls in Appendix C resolve.
- [ ] **K-calibration appendix** — add `app:k-calibration` subsection (referenced from `evaluation_ecosystem_overleaf/appendix/C_design_rationale.tex` "Cadence calibration" + "Holdout weight distance calibration" paragraphs). Contents: (a) K-cadence methodology (24 Epoch benchmarks × 8 labs); (b) cosine-distance methodology (`analyze_cosine_distance.py` Pearson correlations); (c) literature triangulation (Singh et al., Dominguez-Olmedo et al.). Source data in `external-validation/data/processed/`.
- [ ] **σ_prior calibration** — current default 0.05 is preliminary; run longer heuristic sweeps to verify reasonable convergence time for `inferred_weights` on private benchmarks.
- [ ] **Premium-access axis** — implement `premium_pre_access` (N rounds of public-weight observations at t=0, sharpening initial `inferred_weights[b]`) and `premium_submissions_per_round` (best-of-M scoring). Orthogonal to the 5-condition primary set.
- [ ] **Private-benchmark asynchrony sensitivity (deferred)** — primary ablations use global K=3 (synchronized). Optional sensitivity ablation with per-provider asynchronous release cadence (Fix-C deterministic + jitter, or F3 Bernoulli per round with p=1/K_p) to verify findings don't depend on synchronized releases.
- [ ] **Revise abstract** — rework to reflect current paper framing (ecosystem lens, §5 reorganization around privacy + evaluator_capture, softened seed-sensitive claims).
- [ ] **Redo Appendix H** — restructure plan: H.1 heuristic methodology; H.2 privacy ladder extended; H.3 evaluator-capture cross-mode; H.4 Tier 2 ablation sweep; H.5 face-validity cross-mode; H.6 methodological caveats. Trigger when Tier 1–3 LLM runs land.
- [ ] **Heuristic batch 1: evaluator-capture N=30** — single condition + matched baseline, 40 rounds, ~2 hr. Enables §5.3 cross-mode panel. Populates App H.3.
- [ ] **Heuristic batch 2: Tier 2 ablations N=30** — 14 conditions × 30 seeds × 40 rounds (~1 day). Populates App H.4. Defer until Tier 1 LLM lands so we know which ablations are worth including.
- [ ] **Heuristic batch 3: EV2 EU AI Act N=30** — 1 condition × 30 seeds × 40 rounds. Face-validity companion to LLM EV1/EV2. Populates App H.5 cross-mode.
- [ ] **Pre-submission seed audit** — verify all `N{=}X` and seed-range references in paper match what actually ran. Known inconsistencies: `sections/5exp.tex:4` says N=5; `5exp.tex:63,105` say N=3; App H + `docs/experiment_plan.md` now say N=6 (seeds 42-47). Resolve once runs land.
- [ ] **Limitations pass (main body vs appendix)** — rethink what belongs in main body §6/§5 scope paragraph vs Appendix G. Substantive changes expected.
- [ ] **Main-body trim** — currently ~14.5 pp; target NeurIPS 10 pp. Heaviest remaining: Related Work (3.3pp), Simulation (4.0pp).
- [ ] **Dangling references** — `\ref` labels may be broken after restructuring; full pass needed.
- [ ] **Missing bib entries** — Add: singh2025leaderboard, zhou2026pimmur, bick2024rapid, bachmann2023firms, rhee2006liability, hardy2024benchmarks, dulleck2006credence.
- [ ] **Expert interviews** — mentioned in contributions; not conducted. Ties to validation workstream.
- [ ] **Commit pending sim + evaluation_ecosystem_overleaf changes** — flagged across multiple sessions.
- [x] **Appendix G refresh (Cross-Model Robustness)** — extended to 3-way (Sonnet 4.6 / Opus 4.6 / GPT-5.5) via session 54 + 55 work. New playbook at `docs/model_robustness_appendix_playbook.md`. Appendix file renamed `G_sonnet_opus.tex` → `G_model_robustness.tex`; labels renamed to `app:model-robust*`; figures renamed to `model_robustness_*.pdf`; Opus 4.7 → 4.6 corrected throughout. Cross-references updated in E_validation, F_llm_results, 5exp, I_limitations.
- [ ] **Regenerate appendix G figures + prose after overnight ladder fills (2026-04-25 night) complete.** New runs land canonically at `hf_data_staging/core_privacy/llm/{claude-opus-4-6,claude-sonnet-4-6,gpt-5.5-2026-04-23}/<cond>/seed_{43,47}/`. `discover_paired_runs` was patched (this session) to walk both sandbox and canonical layouts, so the regen is now a one-shot: (1) `python -m scripts.tag_reasoning_frames` then (2) `python -m scripts.plots.paper.model_robustness` then (3) `python -m scripts.plots.paper.model_robustness_path_dependence`; (4) `cp output/paper/model_robustness_*.pdf ../evaluation_ecosystem_overleaf/figures/`. Prose updates: (a) drop the "two missing cells" caveat in G.3 path-dependence — Opus s44 + GPT-5.5 s44 still missing but the highlighted-seed selection can shift to {42, 43, 47} for full Sonnet coverage with Opus/GPT-5.5 at {42, 43}; (b) Table G.1 grows from 18 to ~30 rows with new s43 fills — consider pivoting to a (cond, seed) × model-column table for compactness; (c) frame share denominators grow ~30%; refresh the percentages in G.4 / E_validation / F_llm_results / I_limitations. Wall-clock and runtime numbers in G.5 remain valid (paired ratios won't shift meaningfully).

## Sim — open design items

- [ ] **Compliance burden R&D tax** — provider under active regulation (compliance_audit+) faces 0.05–0.15× `rnd_efficiency` reduction. EU preset only; US never. Empirical anchor: GDPR 1–3% revenue (IAPP/EY 2017); EU AI Act conformity assessment €30K–€400K per system.
- [ ] **Endogenous startup entry triggers** — currently exogenous fixed probability. Make market-driven: spike when top provider >0.5 share, or when funder has excess undeployed capital.
- [ ] **Brand barrier for new entrants** — high-trust-sensitivity consumers don't distinguish new entrants from incumbents. Add `new_entrant_trust_penalty` decaying over N rounds.
- [ ] **Gov funder exclusion for startups** — restrict gov/foundation funders from new entrants in early rounds.
- [ ] **`cost_advantage` ↔ `cost_satisfaction_bonus` interaction** — flagged for review; cost_bonus formula may double-count.
- [ ] **Funder `open_source_sponsor` archetype** — funds based on `ecosystem_influence` rather than market-share ROI. Low priority.
- [ ] **VCs investing in non-AI** — allow option (no need to model deeply).
- [ ] **Tier 2 / Tier 3 policymaker implementations**.
- [ ] **Same-round simultaneous saturation** — when two benchmarks saturate on the same round, the second replacement is delayed by min-gap. Allow returning a list. Low priority.

## Single-run dashboard (session 55, 2026-04-25)

- [ ] **Dashboard cosmetic polish** — `scripts/dashboard/dashboard.py` v1 renders 9 panels but: panel-letter labels collide ((c) used by both row 1 col 3 and row 2 col 1; P5/P7/P9 missing prefix). Renumber consistently to (a)–(i) by overriding `ax.set_title(...)` after each panel call. Tighten P3/P5/P7 legends (crowd adjacent panels at composed scale). Reduce P7 y-tick font size for cell density. Add `(g)` prefix to P7 funder-allocation title.
- [x] **Wire dashboard into `scripts/run_experiment.py` post-run hook** — added at end of `run()` (after `logger.finalize()`); LLM-mode only, non-fatal on failure (run still saves), respects `--lightweight`. Import smoke passes. Dashboards now auto-generated alongside `dashboard.png` + `dashboard.pdf` in the run's seed dir for every LLM run going forward. Backfill of existing 14 missing staging dashboards done via `render_all_staging.py --skip-existing` (51 had them, 14 added, 0 failed, 3.4 min wall).
- [x] **Rename `dashboard_prototypes/` → `dashboard/`** (session 68). Original target was `scripts/plots/dashboard/`; settled on simpler `scripts/dashboard/` since the panel modules are import-shaped and live alongside their runner.

## Watch items (calibration concerns)

- [ ] **Goodhart dynamics imposed vs emergent** — `benchmark_orientation` fixed at 0.80 in most runs. If prompt fixes don't resolve, consider orientation floor (~0.30), noisier consumer signal, or structural justification.
- [ ] **EU consolidation artifact** — binding audit deployment gate hits non-OS providers equally regardless of size; uniform fixed cost disproportionately burdens small players. Real-world pattern (EU AI Act) but mechanism simplified.
- [ ] **LLM backbone homogeneity** — all providers reasoned by the same Claude model in most runs. Convergent strategies may reflect shared cognitive biases. Cross-LLM extension tracked in `docs/validation_brainstorm.md` IV.33.
- [ ] **Open-source advantage stack** — OpenCore ends at 50–60% share with minimal incidents despite 10% safety. Review: incident probability uses portfolio `safety` not `safety_capability`; sanction exemption (simulation.py:843); safety floor 0.03 vs 0.35; `cost_advantage` 0.9; no deployer liability model. Each defensible; stack may be too favorable in aggregate.

## Aggregation plot readability

- [ ] **`scripts/aggregate_heuristic.py` quantile trajectory facets too tall** — 5x4 grid hard to read. Options: (a) split into 2 figures by ablation category, (b) single overlay with median lines only, (c) sparklines.
- [ ] **`scripts/aggregate_heuristic.py` forest plots stack 51 ablations vertically** — split into 3 forest plots per policy, or facet horizontally, or only show significant effects.

## Parameter concision (Occam's razor pass)

- [ ] **Full-sim parameter audit** — for every heuristic parameter: (1) does it connect to any other actor's decision, or is it isolated? Cut if isolated. (2) Does it duplicate another parameter? Merge. (3) Can LLM mode subsume it? Scope: model_provider.py, regulator.py, funder.py, media.py, incidents.py. Goal: fewer knobs, cleaner causal attribution.

## Validation — incident path-dependence (open)

5-seed heuristic runs (seeds 7/12/42/88/103, 40 rounds) showed market outcomes highly sensitive to *which* provider receives a major/critical incident and *when*. A single critical incident can swing 30+ pp of share; four different providers win across 5 seeds. Either a feature (matches real-world Samsung Note 7 / 737 MAX dynamics) or calibration issue.

- [ ] Run 30+ seeds and characterize the distribution
- [ ] Ablation: `enable_incidents=False` to isolate variance contribution
- [ ] Compare share-loss magnitudes against empirical cases
- [ ] Check whether heuristic safety-pressure ratchet response is too aggressive/passive
