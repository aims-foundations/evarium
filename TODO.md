# TODO

## NeurIPS Paper (target: draft by Thu Apr 10, deadline ~4 weeks)

- [ ] **Run new experiments** — 17 conditions x 3 presets with updated sim design (sessions 16-18 changes). Blocks experiments section.
- [ ] **Experiments section** — Replace placeholder content (currently presentation-era results) with new figures and findings.
- [ ] **Discussion + Conclusion** — Write after experiments finalize.
- [ ] **Related work** — Untouched from old draft; trim to ~1.5 pages, move LLM-sim validation discussion to Appendix F.
- [ ] **Dangling references** — `\ref` labels may be broken after restructuring; do a full pass.
- [ ] **Missing bib entries** — Add: singh2025leaderboard, zhou2026pimmur, bick2024rapid, bachmann2023firms, rhee2006liability, hardy2024benchmarks, dulleck2006credence.
- [ ] **Compile + page count check** — Verify main body fits NeurIPS 10-page limit.
- [ ] **Commit sessions 16-18 sim changes** — Still uncommitted.
- [ ] **Commit session 20 overleaf changes** — Still uncommitted.
- [ ] **Expert interviews** — Conduct a few before submission; mentioned in contributions but not budgeted in draft.

## Parameter Concision / Occam's Razor Pass

- [ ] **Full-sim parameter audit** — Inspired by session 23 discovery that switching_cost, switching_threshold, tenure_bonus, integration_friction, and decision_delay were all interacting in unauditable ways. For every heuristic parameter in the sim, ask: (1) does it connect to any other actor's decision, or is it isolated? If isolated, consider cutting. (2) Is it doing the same thing as another parameter? If so, merge. (3) Can the LLM mode subsume it? Scope: consumer.py (done for switching), model_provider.py, regulator.py, funder.py, media.py, incidents.py. Goal: fewer knobs, cleaner causal attribution, more auditable heuristic mode.

## Session 22 Open Threads

- [x] **Run initial_uniform + initial_duopoly ablations** — Running overnight in apr9 batch (3 seeds each)
- [ ] **Analyze apr9 batch** — 18 runs (6 conditions × 3 seeds) with updated cap/brand vectors. Key question: does initial_uniform break Orion dominance?
- [ ] **Dynamic consumer market** — HIGH PRIORITY. Enterprise share should grow ~25%→55% over 30 rounds to match real 2023→2025 market transition. Enables segment-specific catch-up (Anthropic's real path). See `memory/session22_dynamic_consumer_market.md`.
- [ ] **Rerun stalled apr8 ablations** — no_media (10r), no_funders (14r), no_regulator (33r) need fresh 40-round runs. Delete partials first.
- [ ] **Reasoning pipeline worked example** — Implement Steps 1-2 of `docs/aggregation_pipeline.md` on one run. Hand-code clusters. Produce reasoning timeline figure.
- [ ] **Higher dimensions / latent needs** — Explore adding unmeasured consumer need dimensions (reliability, UX, deployment ease) that benchmarks can't capture. Would increase dim_mismatch structurally.
- [x] **Investigate no_media misalignment** — RESOLVED: run-length artifact. Baseline shows same 0.025 mismatch at R5-9; drops at R10 when new benchmarks introduced. Need full 40r no_media run to confirm.
- [ ] **Commit sessions 16-22 changes** — All still uncommitted.

## Deep Dive Findings (session 22) — for paper framing

Key findings from apr8 batch analysis:
- **Media is the strongest alignment channel** — removing it 3.4x the gap, mostly dim_mismatch
- **Incidents serve as alignment mechanism** — removing them makes gap negative, reduces score reliability
- **Regulator is underpowered** — no_regulator barely changes outcomes; safety floor from incidents + media
- **Gap driven by incidents not gaming** — penalty_load >> dim_mismatch in baseline. Paper framing should be "multiple failure modes" not just Goodhart
- **Seed 1 is unusually stable** — seed 11 produces healthier market dynamics; multi-seed results needed
- **Incident sequences are seed-deterministic** — identical within seed regardless of condition for first ~15 rounds; safety investment doesn't modulate early enough

## Architecture Review Items (2026-03-30) — COMPLETED 2026-03-31

- [x] **Visibility / ground truth audit** — Fixed: `safety_capability` GT leak in consumer LLM context; removed dead `ground_truth` param from `compute_switching` chain; removed dead `provider_strategies` from `regulator.observe()`; added missing `MediaGroundTruth` to `visibility.py`.
- [x] **Startup entry shenanigans** — Decision: not implementing entry yet. `_maybe_spawn_startup()` stubbed to always return `None`; BTE/HHI metrics preserved and still logged every round.
- [x] **Relook at plotting** — Fixed: `safety_alignment` → `safety` in 4 data-access sites; stale axis labels; `get_strategy_key()` dead code; docstring "Eval Engineering" → "R&D Investment".
- [x] **Relook at experiment structure** — Fixed stale keys in `EXTREME_TEST_PROVIDERS` commented block. Active configs already clean.
- [x] **Validity field review** — Fixed: removed `validity` from `game_log.py` narrative, `Benchmark.get_summary()`, `get_benchmark_summary()`, `get_statistics()`. Internal weight-decay uses untouched.
- [ ] **Before cluster runs:** Switch `run_experiment.py` default back to `--no-dev` (currently defaults to dev/sandbox output). Also set `run_all.py` `DEV = False`. Confirm `hf_data/` directory structure exists.

## PIMMUR Prompt Audit (flagged session 16, 2026-04-06) — COMPLETED session 17

- [x] **Full prompt audit for Minimal-Control violations.** Audited all LLM prompts (provider, funder, evaluator, regulator, consumer individual, consumer organizational, public comms) against PIMMUR Minimal-Control and Unawareness principles. Findings:
  - Provider, Funder, Regulator: PASS (clean after session 16 reframe)
  - Evaluator: Fixed — removed "STAGNANT" judgment label (replaced with raw data), removed "time to act" coaching from system prompt, removed "no longer informative" from action description, replaced bucketed validity labels with raw correlation number
  - Consumer (organizational): Fixed — removed 6-point Decision Framework (researcher theory injection), removed reasoning coaching instruction, toned down ALL-CAPS liability labels, removed `switching_threshold` parameter leak from prompt, simplified JSON reasoning placeholder
  - Consumer (individual): PASS (minor coaching questions, acceptable)
  - Cross-cutting Unawareness: structural concern (AI domain vocabulary throughout) — requires domain reframing, not prompt edits
  - Reference: `rough/pimmur_audit.md` (prior audit, 2026-03-09)

## Post-Run Calibration Review (after first 40-round LLM run)

- [ ] **Provider-need alignment**: Initial cosine similarities were 0.93-0.95 (too flat). Widened capability spread + Q1 2023 recalibration (session 9). After 40-round run, check: do profiles diverge enough to create observable misalignment gaps? If cos stays >0.90 for all providers through round 40, the structural alignment between capability profiles and consumer needs may be too high — consider whether consumer need weights need reshaping (e.g. more heterogeneous across segments) or initial capability profiles need sharper spikes.
- [ ] **rnd_efficiency**: Bumped from 0.05 to 0.08. Check growth trajectories — providers should reach 0.7-0.85 by round 40, not ceiling at 1.0 or stagnate at 0.55.
- [ ] **Funder budget scale**: FUNDER_BUDGET_SCALE=1e-9 ($1B = 1.0 internal). Verify funder allocations are 10-30% of market leader's base revenue, not dominant or negligible.
- [ ] **Market concentration**: Round 0 switching created 37% leader in old run. Check if wider capability spread changes this or makes it worse.
- [ ] **Score-satisfaction gap emergence**: Expect visible gaps by round 15-20 from benchmark introduction + provider specialization. If gaps stay near-zero, benchmark-need misalignment may need further sharpening.

## Plotting Redo — DONE (logging) / IN PROGRESS (dashboards)

**Logging fields now populated in rounds.jsonl:**
- `benchmark_dimension_weights` — true {dim: weight} per active benchmark (from evaluator ground truth)
- `focus_levels` — per provider per benchmark scalar
- `inferred_benchmark_weights` — per provider per benchmark {dim: weight}
- `satisfaction_signals` — per provider 6-dim vector
- `capability_gains` — per provider per-dim gains this round
- `consumer_data.penalty_breakdown` — per provider {base_satisfaction, incident_penalty, cost_bonus}
- `consumer_data.need_weights` — population-weighted 6-dim consumer need vector

**Bug fixed:** `evaluator.get_benchmark_dimension_weights()` referenced `self._benchmark_ground_truth` which was never stored. Fixed by caching in `evaluate_all()`.

### Design principles (revised 2026-03-31)

- The score-satisfaction gap has **multiple channels**: dimensional mismatch, score inflation, and penalty load (incidents/media at scale). Visualization must decompose the gap, not assume one mechanism.
- In empirical runs, penalty load (incident_penalty * (1 + market_share^2)) often dominates the gap. Dimensional mismatch may be absent even when the gap is large. Media influence now routes through exploration behavior, not satisfaction.
- Cosine/L1 metrics on capability profiles are secondary evidence — useful when dimensional gaming IS active, but the gap waterfall is the primary diagnostic.
- Organized by question ("did gaming happen?", "who won?", "what were the costs?"), not by actor type.

### Dashboard A: Gap Anatomy (3x2) — `plot_gap_anatomy()`

The headline dashboard. Decomposes the score-satisfaction gap.

| Position | Panel | Data |
|---|---|---|
| A1 top-left | **Gap Waterfall** — per-provider stacked bar: score_noise (score - dot(cap,bm_agg)), dim_mismatch (dot(cap,bm_agg) - dot(cap,need)), penalty_load (dot(cap,need) - satisfaction) | scores, capability_vectors, benchmark_dimension_weights, consumer_data.penalty_breakdown |
| A2 top-right | **Gap Over Time** — stacked area per provider, same 3 components over rounds | same, per round |
| A3 mid-left | **Dimensional Profile** — grouped bars per dimension: benchmark_weight, need_weight, each provider's cap_share | benchmark_dimension_weights, consumer_data.need_weights, capability_vectors |
| A4 mid-right | **Growth Direction** — per-provider grouped bars: cos(growth, need), cos(growth, bm_agg), cos(growth, satisfaction_signal) | capability_vectors round 0 vs final, satisfaction_signals |
| A5 bottom-left | **Per-Benchmark Structural Alignment** — horizontal bars: cos(bm_weights[b], need) per benchmark | benchmark_dimension_weights, consumer_data.need_weights |
| A6 bottom-right | **Score Reliability** — Pearson-r(score_rank, satisfaction_rank) over time | scores, consumer_data.provider_satisfaction |

### Dashboard B: Market and Strategy (3x2) — `plot_market_strategy()`

| Position | Panel | Data |
|---|---|---|
| B1 top-left | **Market Share** — stacked area over time | consumer_data.market_shares |
| B2 top-right | **Investment Portfolio** — small multiples per provider, stacked area rd/safety/product | strategies |
| B3 mid-left | **Funder Allocations** — stacked bar per round, colored by funder | funder_data.allocations |
| B4 mid-right | **Benchmark Orientation** — line per provider over time | benchmark_orientations |
| B5 bottom-left | **Consumer Switching Rate** over time | consumer_data.switching_rate |
| B6 bottom-right | **Per-Benchmark Scores** — small multiples, one per benchmark, lines per provider | per_benchmark_scores |

### Dashboard C: Costs and Interventions (3x2) — `plot_costs_interventions()`

| Position | Panel | Data |
|---|---|---|
| C1 top-left | **Incident Timeline** — bar per round, colored by severity, provider-labeled | incidents |
| C2 top-right | **Safety Investment vs Incident Rate** — connected scatter with time arrows | strategies.safety, incidents |
| C3 mid-left | **Penalty Load Over Time** — line per provider (dot(cap,need) - satisfaction) | capability_vectors, consumer_data |
| C4 mid-right | **Media Sentiment + Provider Attention** — heatmap providers x rounds | media_data |
| C5 bottom-left | **Intervention Timeline** — Gantt: which lever, which provider, which rounds | regulator_data |
| C6 bottom-right | **Cumulative Incidents** — stacked bar by severity per provider | incidents |

---

## Validation Runs -- Target: Thursday March 5

### Status

- 8x A100-80GB on skampere1, all idle
- Python 3.12, vLLM 0.16.0 installed
- 11 of 27 condition configs exist (all balanced + full_ecosystem US/EU)
- `run_phase.sh` is broken (calls `run_diagnostics.py` with `--condition`/`--output-dir` flags that don't exist)
- `build_registry.py` does not exist yet
- `output/core/` and `output/validation/` directories not created yet

### Step 0: Generate missing US/EU ablation configs (16 configs)

We have balanced ablation configs (exp_004-012) but no US/EU variants.
Create them by cloning each balanced config.json and changing `regulatory_preset`.

Conditions to generate (8 ablations x 2 presets = 16):
- no_media: us, eu
- no_incidents: us, eu
- no_startups: us, eu
- no_opencore: us, eu
- single_benchmark: us, eu
- no_funders: us, eu
- no_bench_evolution: us, eu
- eval_as_company: us, eu

Approach: Python script that reads each balanced config.json, swaps
`regulatory_preset`, and writes to a new experiment directory so
`run_diagnostics.py` can find it by exp_id prefix.

### Step 1: Phase 5 -- Heuristic baseline (free, fast)

Run heuristic replications for all 27 conditions (after Step 0), 30 seeds each.
No GPU needed. Uses `run_diagnostics.py replicate <exp_id> --n-seeds 30 --heuristic`.
Output goes to `output/experiments/` (old structure -- reorganize later).

Start with the 11 configs we already have while Step 0 runs:
```
python scripts/run_diagnostics.py replicate exp_011 --n-seeds 30 --heuristic  # full_ecosystem_balanced
python scripts/run_diagnostics.py replicate exp_001 --n-seeds 30 --heuristic  # full_ecosystem_us
python scripts/run_diagnostics.py replicate exp_002 --n-seeds 30 --heuristic  # full_ecosystem_eu
python scripts/run_diagnostics.py replicate exp_004 --n-seeds 30 --heuristic  # no_media_balanced
python scripts/run_diagnostics.py replicate exp_005 --n-seeds 30 --heuristic  # no_incidents_balanced
python scripts/run_diagnostics.py replicate exp_006 --n-seeds 30 --heuristic  # no_startups_balanced
python scripts/run_diagnostics.py replicate exp_007 --n-seeds 30 --heuristic  # no_opencore_balanced
python scripts/run_diagnostics.py replicate exp_008 --n-seeds 30 --heuristic  # single_benchmark_balanced
python scripts/run_diagnostics.py replicate exp_009 --n-seeds 30 --heuristic  # no_funders_balanced
python scripts/run_diagnostics.py replicate exp_010 --n-seeds 30 --heuristic  # no_bench_evolution_balanced
python scripts/run_diagnostics.py replicate exp_012 --n-seeds 30 --heuristic  # eval_as_company_balanced
```

### Step 2: Start vLLM + Phase 1 Qwen core runs (overnight)

Start vLLM server with Qwen3-235B on all 8 GPUs (TP=8 for faster inference):
```
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen3-235B-A22B \
    --tensor-parallel-size 8 \
    --max-model-len 16384 \
    --gpu-memory-utilization 0.95 \
    --trust-remote-code \
    --port 8000 \
    --disable-log-requests
```

Then set env and run the 3 full_ecosystem conditions first (most important):
```
export LLM_PROVIDER=openai LLM_MODEL=Qwen/Qwen3-235B-A22B OPENAI_API_KEY=dummy OPENAI_BASE_URL=http://localhost:8000/v1
python scripts/rerun_experiment.py exp_011   # full_ecosystem_balanced
python scripts/rerun_experiment.py exp_001   # full_ecosystem_us
python scripts/rerun_experiment.py exp_002   # full_ecosystem_eu
```

Then the 8 balanced ablations, then the 16 US/EU ablations from Step 0.

### Step 3: Phase 2 P0 -- Full ecosystem replications (30 seeds, LLM)

After Phase 1 core runs are done, replicate the 3 full_ecosystem conditions:
```
python scripts/run_diagnostics.py --model qwen replicate <full_eco_balanced_exp_id> --n-seeds 30
python scripts/run_diagnostics.py --model qwen replicate <full_eco_us_exp_id> --n-seeds 30
python scripts/run_diagnostics.py --model qwen replicate <full_eco_eu_exp_id> --n-seeds 30
```

### Step 4: Analyze + report

Run `run_diagnostics.py analyze <batch_name>` on completed batches.
Extract metrics, generate plots, build aggregate tables for Serena.

### Deferred (post-Thursday)

- [ ] Fix `run_phase.sh` to match `run_diagnostics.py` interface (or vice versa)
- [ ] Create `output/core/` and `output/validation/` directory structure
- [ ] Implement `build_registry.py` (walks output/, builds `output/runs.jsonl`)
- [ ] Phase 2 P1/P2 replications (remaining ablations, 30 seeds each)
- [ ] Phase 3 sensitivity sweeps
- [ ] Phase 4 cross-model comparison

---

## Experiment Script (Planned)

Important plots (one plot = one experiment):
1. Market share across runs (Full EU, US + Media, Incident, Startup, OpenSource)
3. Score vs capability (with r value)
4. combine incident timeline per provider (top left, incident_analysis_dashboard) with benchmark validity and intervention and incidents (policymaker_dashboard)

Tables (one column = one experiment):
1. Safety investment (Market leader, average)
2. Final consumer satisfaction
3. Total number of incidents (broken down by severity)

### Primary Runs

These are the two canonical full-feature runs to establish baseline results.
Both use LLM mode, 30 rounds, 5 providers + OpenCore, full ecosystem.

| ID | Policy | Command |
|----|--------|---------|
| exp_001 | US light-touch | `python run_experiment.py --policy us` |
| exp_002 | EU precautionary | `python run_experiment.py --policy eu` |

Key things to observe:
- Does EU precautionary policy reduce incident rate and severity vs US?
- Does US light-touch lead to faster capability gains but higher gaming gaps?
- Do startup entrants behave differently under each regime (BTE, funding, survival)?
- How does OpenCore's commoditization shock play out under each regime?
- Do benchmark focus specializations hold up over 30 rounds, or do competitive
  pressures homogenize providers?

---

### Ablations (demonstrating complex systems value)

Each ablation isolates one feedback loop or emergent mechanism to show what the
simulation captures that simpler models miss. Run heuristic mode (fast) unless
noted. All vs the US full-feature baseline.

#### 1. No media (`enable_media=False`)
- **Tests:** Whether media coverage meaningfully amplifies incidents into
  consumer switching and funder reallocation, or if it's cosmetic.
- **Hypothesis:** Without media, incidents cause weaker consumer response and
  slower regulatory escalation — safety underinvestment goes less punished.

#### 2. No incidents (`enable_incidents=False`)
- **Tests:** Whether the incident system creates meaningful safety investment
  pressure, or providers would converge to similar safety allocations anyway.
- **Hypothesis:** Without incidents, safety_alignment collapses for all
  providers — no endogenous force counters the competitive pressure to defund it.

#### 3. No startups (`startup_entry_probability=0`)
- **Tests:** Whether dynamic entry disciplines incumbents, or whether the
  established 5 providers settle into stable oligopoly regardless.
- **Hypothesis:** Without entry threat, incumbents sustain higher gaming gaps
  and less capability investment; market concentration increases monotonically.

#### 4. No benchmark specialization (uniform benchmark_focus)
- **Tests:** The new benchmark_focus feature — does it produce meaningfully
  differentiated leaderboard profiles, or is it noise?
- **Hypothesis:** Without specialization, all providers converge to similar
  per-benchmark profiles; safety benchmark is inflated even for non-safety labs.
  With specialization, Apex AI clearly leads safety; OpenCore leads math.

#### 5. No funders (`enable_funders=False`)
- **Tests:** Whether funder allocation creates meaningful feedback between
  market performance and capability investment, or if providers self-fund evenly.
- **Hypothesis:** Without funders, capability gaps narrow (no Matthew effect);
  startup survival rate drops (no VC runway extension).

#### 6. No open-source provider (remove OpenCore)
- **Tests:** Whether OS disruption dynamics (commoditization shock, cost
  pressure, contamination multiplier) materially reshape the ecosystem, or
  whether the closed-source race dynamics dominate regardless.
- **Hypothesis:** Without OpenCore, consumer cost sensitivity matters less,
  gaming gap is lower (no contamination pressure), market concentration is higher.

#### 7. Single benchmark (remove multi-benchmark setup)
- **Tests:** Whether multiple benchmarks with different validity/exploitability
  produce richer dynamics than a single aggregate score.
- **Hypothesis:** Single-benchmark runs show faster Goodhart degradation and
  less provider differentiation; no benchmark churn or saturation dynamics.

#### 9. Evaluator as company (`evaluator_as_company=True`)
- **Tests:** Whether commercializing the evaluator (premium access, best-of-N
  submissions, early benchmark access) creates conflicts of interest that worsen
  ecosystem outcomes — a structural critique of for-profit evaluation bodies.
- **Hypothesis:** Premium providers gain systematic scoring advantages decoupled
  from true capability; well-funded incumbents widen their lead; gaming gaps
  grow faster; smaller providers and startups are structurally disadvantaged.
  Safety-focused providers (Apex AI) may opt out of premium access on principle,
  worsening their competitive position despite genuine capability.

#### 10. No benchmark evolution (fix validity/exploitability, no new benchmarks)
- **Tests:** The benchmark lifecycle — does validity decay + new benchmark
  introduction actually reset gaming incentives, or do providers adapt instantly?
- **Hypothesis:** Without evolution, gaming gaps widen monotonically; with
  evolution, new benchmarks create periodic resets in the leaderboard order.

#### 11. Initial market structure ablation (capability vector compression)
- **Tests:** Whether initial competitive structure (monopoly vs duopoly vs competition) changes ecosystem outcomes independently of mechanism ablations.
- **Conditions:**
  - *Monopoly:* Orion far ahead (current vectors or wider)
  - *Duopoly:* Orion + Apex nearly tied, rest trailing
  - *Competition:* Top 4 providers compressed to near-parity (mean ~0.38-0.40)
- **Hypothesis:** Monopoly locks in early via revenue feedback loop; competition produces more differentiated strategies and higher Goodhart pressure (more providers chasing scores). Duopoly may show the most interesting dynamics — two leaders can diverge on strategy (one gaming, one not) in ways a monopolist or competitive field cannot.

1. make vcs want to diversify more. not solely based on leaderboard
2. double check that VCs cant fund opensource, opensource cant invest in safety


## Policymaker → Incident Probability (Medium Complexity)

- **Compliance burden R&D tax:** While under active regulation (compliance_audit or
  higher), provider faces a small `rnd_efficiency` reduction (e.g. 0.05–0.15x) modelling
  legal/documentation overhead. Separate from sanction fine. EU preset applies it at
  compliance_audit+; US never. Strong empirical basis: GDPR compliance costs 1–3%
  revenue (IAPP/EY 2017); EU AI Act conformity assessment €30K–€400K per system.

## Simulation Behavior

1. Verify each actor uses ecosystem public signals when making decisions, not just their initial character profile.
2. VCs should be able to invest in non-AI companies (no need to model deeply — just allow the option).
3. Benchmark spacing should scale with total rounds (rough target: ~8 benchmarks over 50 rounds).
4. Slow down benchmark saturation; make introduction timing more realistic without overloading the system.
5. Tier 2 and Tier 3 implementation of policymakers
6. Rethink market share approach to fines. Maybe do research about what happens in practice — are fine rates in the US actually higher?
7. Change provider names to avoid bias

## Open-Source Provider Modeling

Session 14 (2026-04-05): PIMMUR audit removed/narrowed most hardcoded OS advantages. See `stakeholders.md` OS section for full details. Remaining structural differences: cost_advantage=0.35, safety_floor 0.15 vs 0.25, VC exclusion, deployer liability guidance track.

Remaining work:

- **Funder `open_source_sponsor` archetype** — funders currently treat OS providers normally. A new funder type should fund based on ecosystem_influence (adoption) rather than market-share ROI. Low priority since current funder behavior is acceptable for most experiments.
- **Market share vs. ecosystem influence for funder traction** — currently funders use market share for all providers. For OS providers, ecosystem_influence (logged per round in `open_source_data`) should replace market share as the traction signal in funder allocations.
- **cost_advantage <-> cost_satisfaction_bonus interaction** — flagged for review. The cost_bonus formula (`cost_sensitivity x cost_advantage x 0.15`) may double-count the cost effect alongside the revenue discount. Investigate whether both are needed.

## Validation Phase: Incident Path-Dependence

**Flagged 2026-04-05.** 5-seed heuristic runs (seeds 7/12/42/88/103, 40 rounds) show that market outcomes are highly sensitive to which provider receives a major/critical incident and when. A single critical incident can swing 30+ percentage points of market share. Four different providers win across 5 seeds — the winner is essentially whichever high-R&D provider avoids a major incident.

This is either a feature (incidents *should* be high-impact and path-dependent, matching real-world dynamics where a single safety failure can reshape competitive standing) or a calibration issue (incident severity/frequency may be too swingy relative to other forces in the simulation).

**Needs empirical grounding:** Can the magnitude of incident-driven market share shifts be justified by real-world examples (e.g., Samsung Note 7, Boeing 737 MAX, specific AI incidents)? If so, the path-dependence is a valid emergent finding worth reporting. If not, incident effect magnitudes need recalibration.

**Validation steps:**
- Run 30+ seeds and characterize the distribution of outcomes (not just point estimates)
- Ablation: run with `enable_incidents=False` to isolate how much variance incidents explain
- Compare incident-driven share loss magnitudes against empirical cases
- Check whether the heuristic mode's portfolio response to incidents (safety pressure ratchet) is too aggressive or too passive

## Barriers to Entry / Startup Entry

Core mechanic implemented. Remaining follow-on work:

- **Endogenous entry triggers:** Currently exogenous (fixed probability per round). Could make entry probability market-driven — e.g. spike when top provider's market share exceeds 0.5 or when a funder has excess undeployed capital.
- **Brand barrier for consumers:** Consumers with high trust sensitivity currently don't distinguish new entrants from incumbents. Could add a `new_entrant_trust_penalty` that decays over N rounds post-entry.
- **Gov funder exclusion:** Government funders currently can allocate to new entrants after the delay. Could add a flag to restrict gov/foundation funders from funding startups in early rounds.

## Research-Backed Sources for Simulation Components

Collect empirical and theoretical grounding for each major simulation mechanism. Goal: each key parameter or behavioral assumption should be citable.

- **Benchmark gaming / Goodhart's Law:** Goodhart (1975); Anthropic evals literature; Raji et al. "AI and the Everything in the Whole Wide World Benchmark" (NeurIPS 2021); Kiela et al. "Dynabench" (2021); Bowman et al. "Measuring Progress on Scalable Oversight" (2022).
- **Benchmark validity decay:** Document saturation rates empirically — how fast do SOTA models reach ceiling on major benchmarks (MMLU, HumanEval, GSM8K). Papers: Guo et al. on benchmark contamination; "Are We Done with MMLU?" (2024).
- **Safety underinvestment / race dynamics:** Dafoe "AI Governance" (2018); Chan et al. "Harms from Increasingly Agentic AI" (2023); Krakovna et al. on specification gaming; NIST AI RMF for empirical safety investment framing.
- **Funder behavior / VC dynamics:** Funding data from PitchBook/CB Insights AI investment reports; Cihon et al. "Corporate Governance of AI" for non-commercial funder types.
- **Regulatory interventions:** EU AI Act (2024) for precautionary/threshold parameters; NIST AI RMF for US light-touch framing; IAPP/EY GDPR compliance cost study (2017) for compliance burden parameter ($1–3% revenue).
- **Incident rates and severity:** AI Incident Database (AIID) for base rates; Weidinger et al. "Sociotechnical Safety Evaluation" (2023); Anthropic/DeepMind safety papers for severity classification schema.
- **Market share and consumer switching:** Standard discrete-choice / logit switching models; empirical AI adoption surveys (Stanford AI Index annual reports) for segment-level sensitivity parameters.
- **Evaluator independence and conflict of interest:** Raji et al. "Closing the AI Accountability Gap" (2020); Coston et al. on third-party auditing; UK DSIT evaluator landscape reports.

*Action: For each item above, find the canonical citation, extract the specific number or qualitative finding that maps to a simulation parameter, and annotate the relevant code with a comment referencing it.*

## Narrative Development (from exp 004–015 analysis)

The current experiment set supports the following narrative:
> "Benchmark gaming is structurally inevitable. What varies across conditions is whether the ecosystem maintains signal validity."

### Key empirical findings (from 50-round runs)

1. **Gaming is universal and monotone**: all conditions show mean inflation growing from ~0.10 to ~0.16 over 50 rounds. No condition prevents it.
2. **Two distinct gaming modes** (visible in slope vs intercept decomposition):
   - *Floor bias* (high intercept, low slope): providers inflate all scores unconditionally — obscures differentiation. Seen in no-media (004) and no-bench-evolution (010).
   - *Amplification* (slope > 1, low intercept): capability differences are preserved but stretched. Seen in full-ecosystem runs (013/014/015).
3. **Media shifts gaming from floor to amplification**: removing media (004) raises intercepts (0.16–0.24 vs 0.05–0.12) and lowers slopes below 1 on several benchmarks. Media pressure preserves differentiation.
4. **Benchmark evolution is the primary validity maintenance mechanism**: without it (010), validity drops to r=0.569 vs r=0.806 in baseline. New benchmarks reset Goodhart saturation.
5. **Funders act as an accountability signal**: without funders (009), validity drops to r=0.569 despite similar inflation levels. Funder reallocation based on performance maintains meaningful score differentiation.
6. **Market structure (US/EU/Balanced) changes who wins, not gaming intensity**: all three full-ecosystem runs show similar inflation trajectories and slopes. Market concentration differs dramatically (Genesis leads Balanced, Apex AI leads US and EU) but gaming dynamics are indistinguishable.
7. **Open-source (OpenCore) is not the validity anchor** (counter-intuitive): removing it (007) yields the *highest* validity (r=0.876). OpenCore's uniformly lower scores may introduce noise in the score-capability correlation.
8. **Startups reduce inflation growth but also reduce validity**: no-startups (006) has the lowest inflation delta (+0.030) but lowest validity (r=0.525). Competitive pressure from entrants may push gaming.

### Simulation changes needed to sharpen the narrative

- **US vs EU distinction is currently too weak**: both produce near-identical gaming dynamics. To sharpen: make EU policy trigger at lower thresholds (earlier compliance_audit, lower incident tolerance) so that EU shows measurably different slope/intercept profiles.
- **Funder accountability signal is underutilized**: funders should penalize providers with high gaming gaps (score - capability) when they can detect it, not just reward market share. This would make the no-funders ablation more dramatic.
- **Media → evaluator feedback loop is missing**: media coverage of gaming incidents should make evaluators introduce new benchmarks faster (reduce cooldown). Currently media only affects consumers and policymakers.
- **OpenCore floor effect**: OpenCore's fixed low capability drags down validity in all conditions. Consider giving OpenCore a distinct capability trajectory to make its presence informative rather than noisy.

## Known Edge Cases

- **Same-round simultaneous saturation:** When two benchmarks saturate on the same round, the second replacement is delayed by the min-gap cooldown. Fix: allow introducing two benchmarks in one round (return a list instead of a single Benchmark). Low priority.

## Plotting

- Enhanced provider dashboard: "Evaluation Advantage" panel (premium access vs score jumps) and "Investment vs Trials" scatter.
- Enhanced summary dashboard: incident summary tile (by severity, most incident-prone provider) and evaluator business tile (budget, premium providers, revenue mix).
- New dashboard: `plot_ecosystem_dynamics_dashboard()` — incident→media→consumer flow, evaluator financial sustainability, gaming detection ROC, market concentration vs incident rate.
- Nice-to-have: interactive plots (Plotly/Bokeh), animated visualizations, comparative side-by-side dashboards.

## Documentation / Paper (non-implementation)

- **Update actor one-pager** — stakeholders.md changes from the no-explicit-gaming rewrite need to propagate to the one-page actor summary used in presentations/paper appendix.
- **Update paper diagrams** — architecture diagrams (capability update rule, scoring formula, gaming emergence mechanism) need to reflect the new design (3-lever portfolio, dot-product score, no eval_eng).

## Post-implementation: LLM Prompt Review (PIMMUR)

- **Provider prompt** — DONE (2026-03-31): Full rewrite. Removed all apparatus vocabulary (benchmark_orientation, focus_level, dimension weights as numbers). System prompt now describes levers in natural business language. User prompt shows qualitative focus labels, suppresses satisfaction_signal at round 0, adds confidence qualifiers based on market share, hides near-uniform benchmark beliefs. Added `strategy_memo` field for structured cross-round memory.
- **Funder LLM prompt (M + U)** — When writing `llm_plan_funding` in `llm.py`, do NOT inject theory about why scores might diverge from market outcomes (pimmur_audit.md §Minimal-Control item 4: "funder theory injection"). Pass observables only: scores at face value, market shares, score deltas, incident history, media sentiment, `public_comms`. Let the LLM reason freely. No "gap suggests X" or "scores may be inflated" framing.
- **Regulator / Media / Evaluator prompts** — Review for "simulating" framing, experimental vocabulary, and pre-computed hints. Same PIMMUR pass as funder. Lower priority since these actors make fewer decisions per round.

## Implementation Audit (2026-03-31) — stakeholders.md vs code

Comprehensive audit comparing docs/stakeholders.md spec against actual implementation.
Fix priority: critical items first (affect gaming dynamics), then moderate, then minor.

### Critical (affect simulation dynamics)

- [x] **OS Belief Broadcast not implemented** — FIXED (session 9): After all providers update beliefs, OS providers with `os_belief_broadcast=True` nudge all other providers' `inferred_benchmark_weights` toward true benchmark weights. Strength = `openness_level * market_share * 0.30`. Implemented in `simulation.py` step 4a-bis.

- [x] **Funder scoring formulas don't match spec** — FIXED (session 7): Per-type spec formulas implemented. Corporate funder type added. Media sentiment wired into VC/corporate scoring. `_score_providers()` replaced with `_score_providers_vc/corporate/gov/foundation()`.

- [x] **OS Safety erosion not applied to consumer satisfaction** — FIXED (session 9): Consumer satisfaction path now computes `deployed_safety` with same erosion formula as incident path. `safety_capability = safety * (1 - openness_level * market_share * 0.50)` for OS providers with `os_safety_erosion=True`.

### Moderate (spec-implementation mismatch)

- [x] **Regulator lever names differ from spec** — FIXED (session 7): 5 spec levers implemented (`request_voluntary_commitment`, `publish_advisory`, `mandate_safety_disclosure`, `commission_audit`, `impose_sanction`). Per-lever cooldowns. Exogenous events (US round 24, EU round 14). `consumer_satisfaction` removed from regulator observation. LLM prompt PIMMUR-cleaned (risk_beliefs replaced with reasoning memory).

- [x] **Media missing `narrative_state` and headline budget** — FIXED (session 8): OPTIMISM/SKEPTICISM/CRISIS state machine with transition thresholds. Gaming scandal, saturation narrative, safety concern triggers added. Headline budget: incidents guaranteed, pool sampled up to `media_sample_size=4`. `MediaCoverage` outputs `narrative_state` and `saturation_signal`.

- [x] **Provider budget: multiplicative vs additive** — FIXED (session 8): Budget now `base_revenue + sum(funder_allocations)` (additive). `funding_multipliers` replaced with `provider_funding_totals`. Sanctions apply as efficiency multiplier on budget.

- [x] **Consumer `expected_quality` formula differs** — FIXED (session 8): `expected_quality = trust * leaderboard_signal + (1-trust) * running_perceived_quality`. `running_perceived_quality` EMA updated each round from realized satisfaction. Keyword-matching `effective_relevance` retained (no `benchmark_public_category_weights` data structure exists yet).

- [x] **Saturation detection is threshold-based not delta-based** — FIXED (session 8): Delta-based detection: saturated when max-score delta < 0.005 for 3 consecutive rounds. Perfect scores (>=1.0) still trigger immediate saturation. `max_score_history` tracked per benchmark.

### Minor / Already Known

- [x] **`dynamic_evaluator` toggle not wired** — FIXED (session 8): Heuristic dynamic mode implemented. Signal-based triggers: saturation, low internal validity (Spearman-r < 0.5), fallback at 2x cooldown. Internal validity computed from score_rank vs market_share_rank. Fixed mode unchanged. LLM mode deferred.
- [x] **Evaluator internal validity estimate stub** — FIXED (session 8): `update_internal_validity()` computes Spearman-r(score_rank, market_share_rank). Used as trigger in dynamic evaluator mode.

## Session 11 Fixes and Flags (2026-04-03)

Analysis of 5 complete LLM runs (US, EU, bm_orient_adjustable, market_expansion, misaligned_benchmarks).

### Implemented

- [x] **LLM benchmark focus "all more"** — Prompt now says R&D capacity is finite, prioritize benchmarks most important to goals. Both standard and with-orientation prompts updated in `llm.py`.
- [x] **Exploration churn 3% -> 5%** — `consumer.py` ARCHETYPES exploration_rate raised to reduce first-mover lock-in.
- [x] **Switching thresholds ~30% lower** — All 6 archetypes in `consumer.py` ARCHETYPES: leaderboard_follower 0.15->0.10, experience_driven 0.08->0.06, cautious 0.25->0.18, enterprise_cautious 0.50->0.35, enterprise_growth 0.30->0.22, enterprise_established 0.40->0.28.
- [x] **New users choose independently** — In market_expansion runs, new users (from market_growth_rate) now distributed by believed_quality instead of inheriting incumbent shares. `compute_switching` accepts `market_growth_rate`, passes to `_compute_switching_heuristic`. No effect when growth_rate=0.

### Config changes (next runs)

- [ ] **Market expansion growth rate 12% -> 5%** — Not a code change; set `market_growth_rate=0.05` in experiment config. 5% monthly ≈ 80% annual ≈ 7x over 40 months, matching enterprise AI adoption 2023-2025. Old 12% run (45x growth) was unrealistic for sustained rate.
- [ ] **Presentation market_expansion numbers are stale** — Headline findings table in `overleaf/presentation.tex` shows results from the old 12% growth run (51 incidents, +0.070 gap, 13.6% safety). These will change when re-run at 5%. Do not present these as final.
- [ ] **Use mean per-provider gap as canonical metric** — Aggregate gap (mean_score - avg_satisfaction) mixes weighting schemes. Per-provider gap is apples-to-apples and already positive in all 5 runs.

### Watch for (after next runs)

- [ ] **Goodhart dynamics imposed vs emergent** — benchmark_orientation fixed at 0.80 in 4/5 runs. In the one adjustable run, all providers dropped to 0.05 by round 20. If the benchmark_focus prompt fix changes provider specialization behavior, the orientation question may resolve itself. If not, consider: orientation floor (~0.30), noisier consumer signal, or structural reasons to keep orientation high (funder/procurement dependence on benchmark rank).
- [ ] **Orion still dominant?** — Churn + threshold changes should help. If Orion still >75% in all runs, consider: segment-specific incumbency, diminishing returns to market_presence, or rebalancing initial brand_recognition/product allocations.

### Flagged internally (known limitations)

- [ ] **EU consolidation artifact** — Binding audit deployment gate hits all non-OS providers equally regardless of size. Compliance costs as uniform fixed cost disproportionately burdens small players. This is also a real-world pattern (EU AI Act), so finding is defensible but mechanism is simplified.
- [x] **Score-delta buzz effect** — DONE (session 13): Subsumed by media-driven exploration redesign. Removed media_penalty from satisfaction formula; media influence now routes through per-provider exploration rate (negative coverage drives users to explore) and blended redistribution (media-driven explorers follow believed_quality + buzz). Trust erosion extended to all archetypes scaled by leaderboard_trust. Zero net new parameters. Grounded in Hardy et al. (2024).
- [ ] **Single seed per LLM condition** — All findings are N=1 for LLM runs. LLM runs are case studies; heuristic runs (N=30) are the statistical backbone. Caveat in presentation.
- [ ] **LLM backbone homogeneity** — All 6 providers reasoned by same Claude Sonnet model. Convergent strategies may reflect shared cognitive biases rather than emergent equilibrium.
- [x] **Recalibrate benchmark introduction schedule for 40 rounds** — DONE (session 12): max_benchmarks raised to 10, cooldown reduced to 5. All 6 sequence benchmarks introduced by round 30, full pool of 10 active for last 10 rounds.
- [ ] **Open-source provider advantage stack** — OpenCore ends at 50-60% market share in heuristic runs with minimal incidents despite low safety investment (10%). Multiple compounding advantages need review: (1) incident probability uses portfolio `safety` fraction, not `safety_capability` — so safety erosion from openness doesn't increase incident rate; (2) sanctions exempt OS providers entirely (simulation.py:843); (3) safety floor is 0.03 vs 0.35 for closed providers; (4) cost_advantage=0.9 makes switching nearly frictionless; (5) no deployer liability model — downstream deployers bear risk, not the weights publisher. Each individually defensible, but the stack may be too favorable in aggregate. Consider: using deployed `safety_capability` (post-erosion) in incident probability, or modeling downstream deployer incidents that trace back to the OS provider.

## Infrastructure

- **Eval engineering / antitrust audit** — DONE (2026-03-30): all `evaluation_engineering`, `exploitability`, `gaming_penalty`, `market_concentration_review` removed from src/ and scripts/. Portfolio keys now uniformly `{rd, safety, product}` throughout.
- **LLM plumbing** — DONE (2026-03-30): `llm.py` fully rewritten for new arch. `llm_plan_provider`, `call_llm`, `llm_plan_funding` all written. Old-arch dead code removed. PIMMUR fixes applied to funder prompt.
- **LLM end-to-end smoke test** — `llm_plan_provider` is new and untested with a real LLM. Run a short `run_experiment.py` test (3 rounds, LLM mode) to verify before any production run.
