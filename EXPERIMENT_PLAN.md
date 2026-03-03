# Experiment Plan: Factorial Design & Ablation

## Overview

This document tracks the full experimental plan for the simulation, including
completed experiments, planned replications, sensitivity sweeps, and cross-model
comparisons. The design is organized into four phases:

1. **Phase 1** — Structural ablations (8 conditions x 3 regulatory presets) [partially complete]
2. **Phase 2** — Independent replications for statistical inference
3. **Phase 3** — Sensitivity analysis (continuous parameter sweeps)
4. **Phase 4** — Cross-model robustness (multiple LLMs)

---

## Phase 1: Structural Ablations

### Design

One-at-a-time removal of ecosystem components from the full baseline.
All ablations use the **balanced** regulatory preset. The three regulatory
presets are tested on the full (non-ablated) ecosystem.

### Completed Experiments

| ID | Condition | Regulatory | Rounds | LLM | Status |
|----|-----------|-----------|--------|-----|--------|
| exp_001 | Full Ecosystem | US light-touch | 30 | Claude 3.5 Sonnet | Done |
| exp_002 | Full Ecosystem | EU precautionary | 30 | Claude 3.5 Sonnet | Done |
| exp_003 | Full Ecosystem | US light-touch | 30 | Claude 3.5 Sonnet | Done (duplicate of 001) |
| **exp_004** | **No Media** | Balanced | 30 | Claude 3.5 Sonnet | Done |
| **exp_005** | **No Incidents** | Balanced | 30 | Claude 3.5 Sonnet | Done |
| **exp_006** | **No Startups** | Balanced | 30 | Claude 3.5 Sonnet | Done |
| **exp_007** | **No OpenCore** | Balanced | 30 | Claude 3.5 Sonnet | Done |
| **exp_008** | **Single Benchmark** | Balanced | 30 | Claude 3.5 Sonnet | Done |
| **exp_009** | **No Funders** | Balanced | 30 | Claude 3.5 Sonnet | Done |
| **exp_010** | **No Benchmark Evolution** | Balanced | 30 | Claude 3.5 Sonnet | Done |
| exp_011 | Full Ecosystem | Balanced | 30 | Claude 3.5 Sonnet | Done (baseline) |
| **exp_012** | **Eval As Company** | Balanced | 30 | Claude 3.5 Sonnet | Done |
| exp_013 | Full Ecosystem | Balanced | 50 | Claude 3.5 Sonnet | Done |
| exp_014 | Full Ecosystem | US light-touch | 50 | Claude 3.5 Sonnet | Done |
| exp_015 | Full Ecosystem | EU precautionary | 50 | Claude 3.5 Sonnet | Done |

### Condition Matrix

```
                     Balanced    US Light-Touch    EU Precautionary
Full Ecosystem       exp_011(30) exp_001(30)       exp_002(30)
                     exp_013(50) exp_014(50)       exp_015(50)
No Media             exp_004     —                 —
No Incidents         exp_005     —                 —
No Startups          exp_006     —                 —
No OpenCore          exp_007     —                 —
Single Benchmark     exp_008     —                 —
No Funders           exp_009     —                 —
No Bench Evolution   exp_010     —                 —
Eval As Company      exp_012     —                 —
```

### Gaps / TODO (Phase 1)

- [ ] Ablations currently only run under balanced preset. Consider running
      key ablations (No OpenCore, No Funders, Single Benchmark) under US
      and EU presets too, if cross-regime ablation interactions matter.
- [ ] All current runs are single-seed (seed=1). Need replications (Phase 2).

---

## Phase 2: Independent Replications

### Purpose

The paper commits to reporting inter-run means, standard deviations, and 95%
confidence intervals (Section 4.3). Each condition needs N >= 5 replications
(N >= 10 preferred) to produce meaningful CIs via t-distribution.

### Design

- **Seeds**: 10 distinct seeds per condition (seeds 1..10)
- **CRN caveat**: Same seed controls the simulation's internal RNG (incident
  sampling, market dynamics, benchmark noise), but LLM API calls introduce
  server-side stochasticity that seeds cannot control. Even at `temperature=0`,
  GPT is documented to be non-deterministic; Claude is mostly but not perfectly
  reproducible. CRN therefore provides **partial** variance reduction (from
  simulation mechanics) but not the full guarantee of classical CRN. Paired-
  difference tests remain valid — they just have wider CIs than in a fully
  seed-controlled simulation. For full CRN benefits, use `--heuristic` mode
  (Phase 5) where all randomness is seed-controlled.
- **Priority**: Start with the 3 full-ecosystem conditions + 2 most impactful ablations

### Replication Plan

| Priority | Condition | Preset | Rounds | Seeds | Est. Cost/run | Total |
|----------|-----------|--------|--------|-------|--------------|-------|
| P0 | Full Ecosystem | Balanced | 50 | 1–10 | ~$2.50 | $25 |
| P0 | Full Ecosystem | US | 50 | 1–10 | ~$2.50 | $25 |
| P0 | Full Ecosystem | EU | 50 | 1–10 | ~$2.50 | $25 |
| P1 | No OpenCore | Balanced | 30 | 1–10 | ~$1.50 | $15 |
| P1 | No Startups | Balanced | 30 | 1–10 | ~$1.50 | $15 |
| P1 | Single Benchmark | Balanced | 30 | 1–10 | ~$1.50 | $15 |
| P2 | No Media | Balanced | 30 | 1–10 | ~$1.50 | $15 |
| P2 | No Incidents | Balanced | 30 | 1–10 | ~$1.50 | $15 |
| P2 | No Funders | Balanced | 30 | 1–10 | ~$1.50 | $15 |
| P2 | No Bench Evolution | Balanced | 30 | 1–10 | ~$1.50 | $15 |
| P2 | Eval As Company | Balanced | 30 | 1–10 | ~$1.50 | $15 |

**Estimated total (Claude 3.5 Sonnet):** ~$195 for all conditions x 10 seeds

### Budget-Conscious Alternative

Use a cheaper model for replications (see Phase 4):

| Model | Cost/run (50 rnd) | 10 seeds x 11 conditions | Savings |
|-------|-------------------|--------------------------|---------|
| Claude 3.5 Sonnet | ~$2.50 | ~$195 | — |
| Gemini 2.5 Flash | ~$0.10 | ~$8 | 96% |
| DeepSeek R1 | ~$0.37 | ~$29 | 85% |
| Claude Haiku 4.5 | ~$0.60 | ~$47 | 76% |

### Commands

```bash
# P0: Full ecosystem replications
python scripts/run_diagnostics.py replicate exp_013 --n-seeds 10
python scripts/run_diagnostics.py replicate exp_014 --n-seeds 10
python scripts/run_diagnostics.py replicate exp_015 --n-seeds 10

# Analyze
python scripts/run_diagnostics.py analyze replication_<batch_name>
```

---

## Phase 3: Sensitivity Analysis

### Purpose

Address reviewer concern (Sanmi's comments) that findings may be artifacts of
specific parameter choices. One-at-a-time perturbation sweeps over key
hyperparameters, with 3 seeds per perturbation point.

### Parameters to Sweep

| Parameter | Baseline | Sweep Values | Rationale |
|-----------|----------|-------------|-----------|
| `rnd_efficiency` | 0.01 | 0.005, 0.008, 0.01, 0.012, 0.015 | R&D effectiveness; controls capability growth rate |
| `benchmark_validity_decay_rate` | 0.02 | 0.01, 0.015, 0.02, 0.03, 0.04 | How fast benchmarks degrade under gaming |
| `benchmark_exploitability_growth_rate` | 0.015 | 0.005, 0.01, 0.015, 0.02, 0.03 | Returns to eval engineering |
| `startup_entry_probability` | 0.09 | 0, 0.05, 0.09, 0.15, 0.25 | Market contestability |
| `capability_ceiling` | 1.0 | 0.7, 0.85, 1.0, 1.2 | Upper bound on capability |
| Initial true capability (mean) | 0.25 | 0.15, 0.20, 0.25, 0.30, 0.35 | ±40% perturbation |

### Design

- 6 parameters x 5 levels x 3 seeds = **90 runs**
- Use balanced preset, 30 rounds
- Estimated cost: ~$135 (Claude 3.5 Sonnet), ~$5 (Gemini 2.5 Flash)

### Key Question

For each parameter, does the qualitative finding persist?
- "Gaming gap > 0.10 at end" (score inflation is persistent)
- "HHI increases over time" (market concentrates)
- "Benchmark validity declines" (Goodhart decay occurs)

### Commands

```bash
python scripts/run_diagnostics.py sensitivity exp_011 \
  --param rnd_efficiency \
  --values 0.005,0.008,0.01,0.012,0.015 \
  --n-seeds 3
```

---

## Phase 4: Cross-Model Robustness

### Purpose

Demonstrate that qualitative findings are not artifacts of a single LLM's
behavioral biases. This is the strongest form of the behavioral coherence
diagnostic (Section 4.3): if the same emergent patterns arise under different
LLM backbones, the dynamics are driven by simulation structure, not LLM
idiosyncrasies.

### Models to Compare

| Model | Provider | Cost/run | Role | Supported |
|-------|----------|----------|------|-----------|
| Claude 3.5 Sonnet | Anthropic | ~$2.50 | Current baseline | Yes |
| Claude Sonnet 4.6 | Anthropic | ~$4.50 | Frontier upgrade | Yes (update model ID) |
| GPT-5 | OpenAI | ~$2.80 | Cross-provider comparison | Yes (OpenAI provider exists) |
| Gemini 2.5 Pro | Google | ~$2.80 | Cross-provider comparison | Yes (Gemini provider exists) |
| DeepSeek R1 | DeepSeek | ~$0.37 | Budget + explicit CoT | No (needs new provider) |
| Gemini 2.5 Flash | Google | ~$0.10 | Budget replications | Yes (Gemini provider exists) |

### Design

- Run the **full ecosystem balanced** condition (50 rounds) with each model
- 5 seeds per model for cross-model comparison
- Compare: gaming gap trajectory, pattern validation pass/fail, strategy drift

### Priority Order

1. **Claude Sonnet 4.6** — minimal code change (same API, update model string)
2. **GPT-5** — already supported in codebase, different reasoning style
3. **Gemini 2.5 Flash** — cheapest option for mass replications
4. **Gemini 2.5 Pro** — stronger Gemini for quality comparison
5. **DeepSeek R1** — requires adding a new LLM provider class

### Estimated Cost

| Model | Runs | Cost/run | Total |
|-------|------|----------|-------|
| Claude Sonnet 4.6 | 5 | $4.50 | $22.50 |
| GPT-5 | 5 | $2.80 | $14.00 |
| Gemini 2.5 Flash | 5 | $0.10 | $0.50 |
| Gemini 2.5 Pro | 5 | $2.80 | $14.00 |
| **Total** | | | **~$51** |

---

## Phase 5: Heuristic Baseline

### Purpose

Compare LLM-driven actors against heuristic (rule-based) actors to quantify
what the LLM adds. This is already supported via `llm_mode=False`.

### Design

- Run all 11 conditions with `--heuristic` flag
- 10 seeds each (cheap: no API calls)
- Compare pattern validation pass rates: LLM vs heuristic

### Commands

```bash
python scripts/run_diagnostics.py replicate exp_011 --n-seeds 10 --heuristic
```

---

## Summary: Total Experiment Budget

| Phase | Runs | Model | Est. Cost |
|-------|------|-------|-----------|
| Phase 1 (done) | 15 | Claude 3.5 Sonnet | ~$37 (spent) |
| Phase 2 (replications) | 110 | Claude 3.5 Sonnet | ~$195 |
| Phase 3 (sensitivity) | 90 | Gemini 2.5 Flash | ~$5 |
| Phase 4 (cross-model) | 20 | Mixed | ~$51 |
| Phase 5 (heuristic) | 110 | None (heuristic) | $0 |
| **Total** | **345** | | **~$288** |

### Budget-Optimized Plan

If budget is tight, use Gemini 2.5 Flash for Phase 2 replications:

| Phase | Runs | Model | Est. Cost |
|-------|------|-------|-----------|
| Phase 2 (replications) | 110 | Gemini 2.5 Flash | ~$8 |
| Phase 3 (sensitivity) | 90 | Gemini 2.5 Flash | ~$5 |
| Phase 4 (cross-model) | 20 | Mixed | ~$51 |
| Phase 5 (heuristic) | 110 | None | $0 |
| **Total** | **330** | | **~$64** |

---

## Execution Order

1. [ ] **Phase 5** — Heuristic baseline (free, fast, validates infrastructure)
2. [ ] **Phase 2 P0** — Replicate 3 full-ecosystem conditions (most important for paper)
3. [ ] **Phase 4** — Cross-model comparison (Claude 4.6 + GPT-5)
4. [ ] **Phase 3** — Sensitivity sweeps (addresses reviewer concern)
5. [ ] **Phase 2 P1-P2** — Remaining ablation replications

---

## Diagnostics Output

After each phase, run:

```bash
python scripts/analyze_existing.py          # per-experiment diagnostics
python scripts/run_diagnostics.py analyze <batch>  # batch-level aggregation
```

Key outputs per batch:
- `aggregate_stats.json` — per-round mean/CI for all metrics
- `pattern_results.json` — 7 pattern checks with pass/fail fractions
- `coherence_report.json` — strategy drift, role adherence, prompt sensitivity
- `plots/` — trajectory overlays, tornado charts, drift heatmaps

---

## Data Preservation Policy

### Phase 1 experiments (exp_001–exp_015, heuristic runs)
Keep everything as-is. These are the canonical reference runs and their plots, game logs,
and actor traces are used for qualitative interpretation.

### Replication runs (Phase 2–5)
For replication runs the only two things that must be saved are:

1. **`rounds.jsonl`** — the full per-round state. This is the raw ground truth and cannot
   be regenerated without re-running the experiment. Never delete or compress it.
2. **A row in the replication metrics CSV** — one row per run with all extracted scalar
   and summary metrics (see "Metrics to Track" section below). This is what gets aggregated
   for CIs and pattern pass-rates.

Everything else produced by a replication run — `plots/`, `game_log.md`, `summary.json`,
`providers/`, `policymakers/`, `funders/` subdirectories — can be deleted immediately
after the CSV row is written, or simply never generated in the first place. All of those
are either regenerable from `rounds.jsonl` + `config.json`, or not needed for the paper's
statistical claims.

**Practical rule:** after a replication batch completes, run the metrics extraction script
to write the CSV rows, verify `rounds.jsonl` exists and is non-empty for each run, then
delete everything else in those experiment folders.

---

## Metrics to Track Across Replication Runs

These are the metrics to extract per run and aggregate (mean, SD, 95% CI via t-distribution)
across seeds within each condition. Organized by priority.

### Primary Outcomes (paper commits to reporting CIs on these)

| Metric | Source field in `rounds.jsonl` | Aggregation |
|--------|-------------------------------|-------------|
| Mean score inflation | `mean(scores[p]) - mean(true_capabilities[p])` across providers | per-round trajectory + last-5-round mean |
| Score inflation per provider | `scores[p] - true_capabilities[p]` | per-round per-provider |
| Mean true capability | `mean(true_capabilities.values())` | per-round trajectory + last-5-round mean |
| True capability per provider | `true_capabilities[p]` | per-round |
| Mean evaluation engineering | `mean(strategies[p].evaluation_engineering)` | per-round trajectory + last-5-round mean |
| Eval eng per provider | `strategies[p].evaluation_engineering` | per-round |
| HHI (market concentration) | `sum(s^2 for s in consumer_data.market_shares.values())` | per-round trajectory + last-5-round mean |
| Mean consumer satisfaction | `consumer_data.avg_satisfaction` | per-round trajectory + last-5-round mean |
| Benchmark validity (alpha) | `benchmark_params[b].validity` per active benchmark | per-round per-benchmark |
| Benchmark exploitability (beta) | `benchmark_params[b].exploitability` | per-round per-benchmark |
| Validity correlation (rolling r) | Pearson r(scores, true_caps) over window=5 | per-round per-benchmark |

### Secondary Outcomes

| Metric | Source field in `rounds.jsonl` | Aggregation |
|--------|-------------------------------|-------------|
| Fundamental research (mean) | `mean(strategies[p].fundamental_research)` | per-round |
| Training optimization (mean) | `mean(strategies[p].training_optimization)` | per-round |
| Safety alignment (mean) | `mean(strategies[p].safety_alignment)` | per-round |
| Strategy drift (cosine) | cosine distance between consecutive strategy vectors | per-round per-provider; flag if > 0.02 |
| Per-benchmark score inflation | `per_benchmark_scores[b][p] - true_capabilities[p]` | per-round per-benchmark per-provider |
| OLS slope (score ~ true_cap) | regression across providers per benchmark | last-10-round aggregate |
| OLS intercept (floor bias) | same regression | last-10-round aggregate |
| Funding multiplier per provider | `funder_data.funding_multipliers[p]` | per-round |
| Funding HHI | `sum(s^2)` over normalized funder allocations to non-OS providers | per-round |
| Funding-score correlation | Pearson r(funding_multiplier, published_score) | per-round |
| Funding-capability correlation | Pearson r(funding_multiplier, true_capability) | per-round |
| Active sanction count | `len(policymaker_data.active_sanctions)` | per-round |
| Intervention type counts | count by type from `policymaker_data.interventions` | cumulative per run |
| Time to first intervention | first round where `policymaker_data.interventions` is non-empty | per run scalar |
| Gaming risk level | `policymaker_data` risk fields (if logged) | per-round |
| Incident count per severity | count from incident fields by severity | per round and cumulative |
| Incident count per provider | incidents attributed to each provider | cumulative per run |
| Consumer switching rate | `consumer_data.switching_rate` | per-round |
| Satisfaction per archetype | aggregate `consumer_data.segment_data` by archetype | per-round |
| BTE composite | `barrier_to_entry.composite` | per-round |
| BTE components | `barrier_to_entry.market_concentration/capability_gap/funding_lock_in/consumer_lock_in` | per-round |
| Startup entry count | count rounds where `new_entrant` key is present | per run scalar |
| OpenCore ecosystem influence | `open_source_data.OpenCore.ecosystem_influence` | per-round |
| OpenCore commoditization fired | `open_source_data.OpenCore.commoditization_shock_fired` | boolean per run |
| Media sentiment | `media_data.sentiment` | per-round |
| Media headline count | `len(media_data.headlines)` | per-round |
| Media risk signal count | `len(media_data.risk_signals)` | per-round |
| Benchmark turnover count | count benchmark retirements + introductions | per run scalar |
| Breakthrough count | count rounds where capability jump exceeds ~2× normal delta | per run scalar |
| Role adherence violations | count of "true capability" / "actual capability" in `actor_traces` | per round and cumulative |

### Pattern Validation (binary per run, fraction across seeds)

For each seed, record pass (1) or fail (0) for each pattern. Report pass-rate across seeds per condition.

| Pattern | Measurement criterion |
|---------|----------------------|
| Score Inflation | `mean_inflation > 0.10` sustained by round 15 |
| Benchmark Turnover | at least one retirement + introduction during the run |
| Regulatory Escalation | at least one intervention of type beyond `investigation` |
| Commoditization Shock | `open_source_data.OpenCore.commoditization_shock_fired == true` at any round |
| Safety Incident Response | funder adjusts allocation in response to a major/critical incident |
| Gaming Persistence | `mean_eval_eng` remains above initial level through round 20+ |
| Funding Follows Scores | r(funding, published_score) > r(funding, true_capability) |

### Aggregation Protocol (across seeds within a condition)

For every per-round metric, compute:
- `mean_trajectory[t]` — mean across N seeds at each round t
- `std_trajectory[t]` — standard deviation across seeds at round t
- `CI95_lower[t]`, `CI95_upper[t]` — t-distribution 95% CI (df = N-1)

For every per-run scalar (e.g., startup_entry_count, time_to_first_intervention):
- `mean`, `std`, `CI95_lower`, `CI95_upper` across seeds

For pattern pass/fail:
- `pass_rate` = fraction of seeds passing (0.0–1.0)
- `CI95` via Wilson interval or normal approximation

Minimum N for meaningful CIs: **5 seeds** (N=10 preferred per EXPERIMENT_PLAN design).

---

## Findings from Phase 1 Diagnostics

### Pattern Validation (single runs)

| Pattern | Pass Rate (15/15 exps) | Notes |
|---------|----------------------|-------|
| Score Inflation | 15/15 | Persistent across all conditions |
| Benchmark Turnover | 13/15 | Fails only: single_benchmark, no_bench_evolution (expected) |
| Regulatory Escalation | 15/15 | Always present |
| Commoditization Shock | 14/15 | Fails only: no_opencore (expected) |
| Safety Incident Response | 14/15 | Fails only: no_funders |
| Gaming Persistence | 11/15 | Fails in 50-round exps + no_startups (eval eng drops over time) |
| Funding Follows Scores | 2/15 | Funders correlate more with true capability than scores |

### Role Adherence

All 15 experiments show 52–225 violations (terms like "real capability",
"actual capability" in actor traces). This is a known LLM behavior issue —
actors reason about hidden state despite not having it in their prompts.
Needs investigation: are actors hallucinating or genuinely leaking?

### Ablation Effects (vs exp_011 baseline, avg last 5 rounds)

| Ablation | Gaming Gap | Capability | Eval Eng | HHI | Satisfaction |
|----------|-----------|-----------|---------|-----|-------------|
| No Startups | -0.027 | +0.073 | **-0.177** | +0.172 | +0.026 |
| No OpenCore | +0.012 | -0.068 | **+0.142** | +0.114 | +0.052 |
| Single Bench | -0.018 | -0.002 | +0.005 | **+0.292** | +0.085 |
| No Bench Evol | +0.002 | -0.004 | +0.005 | +0.219 | -0.015 |
| No Funders | +0.004 | -0.028 | +0.008 | -0.026 | +0.013 |
| No Media | -0.000 | -0.005 | -0.000 | +0.193 | +0.054 |
| No Incidents | +0.001 | -0.001 | +0.006 | -0.011 | +0.001 |
| Eval As Company | +0.003 | +0.004 | +0.020 | +0.126 | +0.045 |
