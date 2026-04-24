# TODO

## Open threads to raise with collaborators

- [ ] **Interview integration in §5.3 Validation** — how should practitioner interviews enter the paper? Abstract + §3 mention them as input to framework construction; §5.3 Validation alludes to them as a design-grounding source but defers specifics. Options: (a) separate appendix stub listing practitioner roles + which design choices each informed; (b) paragraph in §3 intro about interview methodology; (c) defer to follow-on paper. Open thread; needs collaborator input before writing.

## Paper (NeurIPS)

- [ ] **Sync `docs/references.md` with `overleaf/references.bib`** — references.md has accumulated citations across sessions (market growth, consumer, regulator, funder, benchmark-privacy / Singh 2024 / Dominguez-Olmedo 2024 / Xu 2024 / Deng 2024 / Epoch AI data / Kaggle LLM leaderboard). Sync pass to bib; verify `\cite{}` calls in Appendix C resolve.
- [ ] **K-calibration appendix** — add `app:k-calibration` subsection (referenced from `overleaf/appendix/C_design_rationale.tex` "Cadence calibration" and "Holdout weight distance calibration" paragraphs). Contents: (a) K-cadence methodology (24 Epoch benchmarks × 8 labs matrix, per-provider variance, tier-1 robustness); (b) cosine-distance methodology (same-family / within-dim / cross-dim Pearson correlations from `analyze_cosine_distance.py`); (c) reference to literature triangulation (Singh et al., Dominguez-Olmedo et al.). Source data in `external-validation/data/processed/k_cadence_*.csv` and `cosine_pairs.csv`; reproducible via the two analysis scripts.
- [ ] **Private-benchmark mechanism implementation** — session-38 design landed in code (2026-04-18):
    1. [x] Holdout-only scoring formula (no blend); compute_holdout_scores removed
    2. [x] h controls holdout sample-size noise scaling (σ / √(samples × h))
    3. [x] σ_prior-based initialization of inferred_weights (noisy-public-weights prior; new SimulationConfig.sigma_prior default 0.05)
    4. [x] Configurable cosine per benchmark type via `_scale_cdw` helper in `run_experiment.py`: scale=0 (iid), scale=1 (partial, hand-crafted ≈ 0.95), scale=2 (private, amplified ≈ 0.85)
    5. [x] Five-condition presets (`public_only`/`baseline`/`private_dominant`/`private_only`/`iid_holdout`); old `fixed_partial`/`fixed_private`/`expanding_partial`/`expanding_private`/`periodic_partial`/`periodic_private` deleted
    6. [x] LLM provider prompt exposes benchmark type as `[private benchmark: X% of items held out; scored on holdout only]`
    7. [x] K-lag gating verified end-to-end (smoke test: all 5 conditions, 5-round heuristic runs, per-benchmark score trajectories show correct freeze-and-publish behavior)
    8. [ ] σ_prior calibration — current default 0.05 is preliminary; run longer heuristic sweeps to verify reasonable convergence time for inferred_weights on private benchmarks
- [ ] **Premium-access axis (future benchmark-sponsorship + eval-as-company ablations)** — implement `premium_pre_access` (simulates N rounds of public-weight observations at t=0, sharpening initial `inferred_weights[b]`) and `premium_submissions_per_round` (best-of-M scoring). Orthogonal to the 5-condition primary set.
- [ ] **Private-benchmark asynchrony sensitivity (deferred)** — primary ablations use global K=3 (F1: all providers × benchmarks synchronized). Optional sensitivity ablation with per-provider asynchronous release cadence (Fix-C deterministic + gap-level jitter, or F3 Bernoulli per round with p=1/K_p) to verify qualitative findings don't depend on synchronized releases. See session-38 memo.
- [ ] **Revise abstract** — rework to reflect current paper framing (ecosystem lens, session-49 §5 reorganization around privacy + eval_as_company, softened seed-sensitive claims).
- [ ] **Redo Appendix H** — comprehensive LLM + heuristic results section needs full rewrite once Tier 1–3 runs land. Current content is session-44-era (21 LLM runs, 18-condition heuristic matrix, volcano/forest/pathway-scatter plots) and no longer matches the paper's results story after the §5 privacy+eval_as_company pivot. Restructure plan: H.1 heuristic methodology (no runs needed); H.2 privacy ladder extended (existing data); H.3 eval-as-company cross-mode (batch 1); H.4 Tier 2 ablation sweep (batch 2); H.5 face-validity cross-mode (batch 3 + Tier 1 EV1/EV2); H.6 methodological caveats (salvage from current).
- [ ] **Heuristic batch 1: eval-as-company N=30** — single condition + matched baseline, 40 rounds, ~2 hr. Enables §5.3 cross-mode panel. Expect p=0.20 directional effect (per session 49b); publishable finding is "business-model effect is LLM-reasoning-dependent." Populates App H.3.
- [ ] **Heuristic batch 2: Tier 2 ablations N=30** — 14 conditions × 30 seeds × 40 rounds (~1 day). Converts Tier 2 from directional LLM × 2 seeds into distributional table. Populates App H.4. Defer until Tier 1 LLM lands so we know which ablations are worth including (may cut half).
- [ ] **Heuristic batch 3: EV2 EU AI Act N=30** — 1 condition × 30 seeds × 40 rounds. Face-validity companion to LLM EV1/EV2 runs. Populates App H.5 cross-mode.
- [ ] **Pre-submission seed audit** — verify all `N{=}X` and seed-range references in paper match what actually ran. Current known inconsistencies: `sections/5exp.tex:4` says N=5; `5exp.tex:63,105` say N=3; Appendix H and `docs/experiment_plan.md` now say N=6 (seeds 42-47). Don't resolve until runs land — pick whichever matches ground truth.
- [ ] **Limitations pass (main body vs appendix)** — rethink what belongs in main body §6/§5 scope paragraph vs Appendix G (scope). Substantive changes expected (not just relocation). Current split is ad-hoc across §5.4 scope paragraph, G_scope limitations, and the orphan 6scope.tex.
- [ ] **Main-body trim** — currently ~14.5 pp; target NeurIPS 10 pp. Heaviest remaining: Related Work (3.3pp), Simulation (4.0pp).
- [ ] **Dangling references** — `\ref` labels may be broken after restructuring; full pass needed.
- [ ] **Missing bib entries** — Add: singh2025leaderboard, zhou2026pimmur, bick2024rapid, bachmann2023firms, rhee2006liability, hardy2024benchmarks, dulleck2006credence.
- [ ] **Expert interviews** — mentioned in contributions; not conducted. Ties to validation workstream.
- [ ] **Commit pending sim + overleaf changes** — flagged across multiple sessions.
- [ ] **Appendix K refresh (Sonnet vs Opus) when Tier 1 Opus ladder completes** — re-run full playbook in `docs/sonnet_vs_opus_appendix_playbook.md` once batch 3a/3b lands. Current draft (2026-04-24) covers 4 matched pairs: `baseline@s42`, `baseline@s43`, `private_dominant@s42`, `private_only@s42`. Refresh adds `public_only@s42` + `iid_holdout@s42` Opus (→ full seed-42 ladder). Re-run: `python -m scripts.plots.paper.sonnet_vs_opus` then `python -m scripts.tag_reasoning_frames` then re-run plots, copy PDFs to `overleaf/figures/`, update Table K.1, K.3 percentages, K.4 wall-clock numbers in `overleaf/appendix/K_sonnet_opus.tex`.

## Aggregation Plot Readability (session 26)

- [ ] **`scripts/aggregate_heuristic.py` — quantile trajectory facets too tall.** With 18 conditions per policy, the 5x4 grid is hard to read at one glance. Options: (a) split into 2 figures of 9 conditions each grouped by ablation category (structural / mechanism / validity), (b) use a single overlay plot with color-coded conditions and median lines only, (c) drop quantile bands and use small-multiples sparklines.
- [ ] **`scripts/aggregate_heuristic.py` — forest plots stack 51 ablations vertically.** Currently one row per condition x policy. Options: (a) split into 3 forest plots (one per policy, ~17 rows each), (b) facet horizontally by policy with shared y-axis labels, (c) only show significant effects.

## Parameter Concision / Occam's Razor Pass

- [ ] **Full-sim parameter audit** — Inspired by session 23 discovery that switching_cost, switching_threshold, tenure_bonus, integration_friction, and decision_delay were all interacting in unauditable ways. For every heuristic parameter in the sim, ask: (1) does it connect to any other actor's decision, or is it isolated? If isolated, consider cutting. (2) Is it doing the same thing as another parameter? If so, merge. (3) Can the LLM mode subsume it? Scope: consumer.py (done for switching), model_provider.py, regulator.py, funder.py, media.py, incidents.py. Goal: fewer knobs, cleaner causal attribution, more auditable heuristic mode.

## Session 22 Open Threads

- [ ] **Reasoning pipeline worked example** — Implement Steps 1-2 of `docs/aggregation_pipeline.md` on one run. Hand-code clusters. Produce reasoning timeline figure.
- [ ] **Higher dimensions / latent needs** — Explore adding unmeasured consumer need dimensions (reliability, UX, deployment ease) that benchmarks can't capture. Would increase dim_mismatch structurally.

## Calibration — verify if still relevant

Most items were addressed through sessions 9–26 (wider capability spread, rnd_efficiency retuning, dynamic consumer market, switching formula overhaul). Before final runs, spot-check:

- [ ] Provider–need cosine similarities — still flat >0.90?
- [ ] `rnd_efficiency` growth — providers reaching 0.7–0.85 by round 40?
- [ ] Funder allocations — 10–30% of leader's base revenue?
- [ ] Score–satisfaction gap visible by round 15–20?

## Watch items (from session 11 flags)

- [ ] **Goodhart dynamics imposed vs emergent** — `benchmark_orientation` fixed at 0.80 in most runs. If prompt fixes and adjustable-mode ablations don't resolve, consider orientation floor (~0.30), noisier consumer signal, or structural justification (funder/procurement dependence on benchmark rank).
- [ ] **Orion dominance** — if churn + threshold fixes don't break >75% share in all runs, consider segment-specific incumbency, diminishing returns to market_presence, or rebalancing initial brand_recognition/product allocations.
- [ ] **EU consolidation artifact** — binding audit deployment gate hits non-OS providers equally regardless of size. Compliance as uniform fixed cost disproportionately burdens small players. Real-world pattern (EU AI Act) but mechanism simplified.
- [ ] **LLM backbone homogeneity** — all providers reasoned by the same Claude model in most runs. Convergent strategies may reflect shared cognitive biases. Cross-LLM extension tracked in `docs/validation_brainstorm.md` IV.33.
- [ ] **Open-source advantage stack** — OpenCore ends at 50–60% share with minimal incidents despite 10% safety. Review: (1) incident probability uses portfolio `safety` not `safety_capability` (safety erosion from openness doesn't raise incidents), (2) sanction exemption (simulation.py:843), (3) safety floor 0.03 vs 0.35, (4) `cost_advantage` 0.9, (5) no deployer liability model. Each defensible individually; stack may be too favorable in aggregate. Consider: use post-erosion `safety_capability` in incident prob, or model downstream deployer incidents traced back to OS provider.

## Sim improvements — open design items

### Policymaker → Incident Probability

- [ ] **Compliance burden R&D tax** — While under active regulation (compliance_audit or higher), provider faces small `rnd_efficiency` reduction (0.05–0.15x) modelling legal/documentation overhead. Separate from sanction fine. EU preset applies at compliance_audit+; US never. Empirical basis: GDPR compliance costs 1–3% revenue (IAPP/EY 2017); EU AI Act conformity assessment €30K–€400K per system.

### Simulation Behavior

- [ ] VCs should be able to invest in non-AI companies (no need to model deeply — just allow the option).
- [ ] Tier 2 and Tier 3 implementation of policymakers.
- [ ] Rethink market share approach to fines — research whether fine rates in the US are actually higher in practice.

### Open-Source Provider Modeling

Session 14 PIMMUR audit removed most hardcoded OS advantages. Remaining structural differences: `cost_advantage=0.35`, safety_floor 0.15 vs 0.25, VC exclusion, deployer liability guidance track. See `stakeholders.md` OS section for full details.

- [ ] **Funder `open_source_sponsor` archetype** — new funder type funding based on `ecosystem_influence` rather than market-share ROI. Low priority; current funder behavior acceptable for most experiments.
- [ ] **Market share vs. ecosystem influence for funder traction** — for OS providers, `ecosystem_influence` (logged per round in `open_source_data`) should replace market share as the traction signal in funder allocations.
- [ ] **`cost_advantage` ↔ `cost_satisfaction_bonus` interaction** — flagged for review. The cost_bonus formula (`cost_sensitivity × cost_advantage × 0.15`) may double-count the cost effect alongside the revenue discount. Investigate whether both are needed.

### Barriers to Entry / Startup Entry

Core mechanic implemented. Remaining follow-on work:

- [ ] **Endogenous entry triggers** — currently exogenous fixed probability. Make market-driven: spike when top provider >0.5 share, or when a funder has excess undeployed capital.
- [ ] **Brand barrier for consumers** — consumers with high trust sensitivity don't distinguish new entrants from incumbents. Add `new_entrant_trust_penalty` decaying over N rounds post-entry.
- [ ] **Gov funder exclusion** — government funders can currently allocate to new entrants after delay. Add flag to restrict gov/foundation funders from startups in early rounds.

## PIMMUR Prompt Review (remaining)

Provider and funder prompts fully audited and fixed in sessions 16–17. Consumer prompts audited in session 17.

- [ ] **Regulator / Media / Evaluator prompts** — same PIMMUR pass as funder. Review for "simulating" framing, experimental vocabulary, and pre-computed hints. Lower priority since these actors make fewer decisions per round.

## Validation — Incident Path-Dependence

Pointer: cross-referenced in `docs/validation_brainstorm.md` (II.A.15 AIID match, I.2 ablations).

5-seed heuristic runs (seeds 7/12/42/88/103, 40 rounds) showed market outcomes highly sensitive to which provider receives a major/critical incident and when. A single critical incident can swing 30+ percentage points of market share. Four different providers win across 5 seeds. Either a feature (matching real-world dynamics where a single safety failure reshapes competitive standing) or a calibration issue. Needs empirical grounding against real cases (Samsung Note 7, Boeing 737 MAX, specific AI incidents).

Steps:
- Run 30+ seeds and characterize the distribution (not just point estimates)
- Ablation: `enable_incidents=False` to isolate how much variance incidents explain
- Compare share-loss magnitudes against empirical cases
- Check whether heuristic portfolio response to incidents (safety pressure ratchet) is too aggressive or too passive

## Known Edge Cases

- **Same-round simultaneous saturation:** When two benchmarks saturate on the same round, the second replacement is delayed by the min-gap cooldown. Fix: allow introducing two benchmarks in one round (return a list instead of a single Benchmark). Low priority.

## Plotting (nice-to-haves)

- Enhanced summary dashboard: incident summary tile (by severity, most incident-prone provider) and evaluator business tile (budget, premium providers, revenue mix).
- Interactive plots (Plotly/Bokeh), animated visualizations, comparative side-by-side dashboards.

## Documentation / Paper (non-implementation)

- **Update actor one-pager** — stakeholders.md changes from the no-explicit-gaming rewrite need to propagate to the one-page actor summary used in presentations/paper appendix.
- **Update paper diagrams** — architecture diagrams (capability update rule, scoring formula, gaming emergence mechanism) need to reflect the new design (3-lever portfolio, dot-product score, no eval_eng).
