# Experiment Plan: Ablation Design & Validation

## Overview

This document tracks the full experimental plan for the simulation. The design
tests whether benchmark gaming dynamics emerge structurally from the evaluation
ecosystem, and which mechanisms drive or suppress them.

Five phases:

1. **Phase 1** — Structural ablations: 15 conditions x 3 regulatory presets = 45 canonical runs (single seed)
2. **Phase 2** — Independent replications for statistical inference (30 seeds/condition)
3. **Phase 3** — Sensitivity analysis (continuous parameter sweeps)
4. **Phase 4** — Cross-model robustness (multiple LLMs)
5. **Phase 5** — Heuristic baseline (rule-based actors, fully seed-controlled)

**Primary model:** Qwen3-235B-A22B (vLLM, local)
**Round count:** 30 rounds across all conditions and phases.

---

## Ablation Conditions

### Category 1: Structural Ablations

Remove a component entirely. Tests whether the component is load-bearing.

| # | Condition | Config override | What it tests |
|---|-----------|-----------------|---------------|
| 1 | Full Ecosystem | (baseline) | Reference run with all mechanisms active |
| 2 | No Media | `enable_media=False` | Does media amplify/dampen gaming via attention and sentiment? |
| 3 | No Funders | `enable_funders=False` | Does the capital allocation feedback loop matter? |
| 4 | No Regulator | `enable_regulators=False` | Does regulatory intervention change provider behavior? |
| 5 | No OpenSource | Remove OpenCore from provider configs | Does an open-weight competitor reshape dynamics? |
| 6 | No Incidents | `enable_incidents=False` | Is the penalty channel load-bearing for the gap? |
| 7 | Single Benchmark | `single_benchmark=True` | Does benchmark diversity affect dynamics? |

### Category 2: Mechanism Ablations

A component is present but a specific mechanism is toggled or varied.

| # | Condition | Config override | What it tests |
|---|-----------|-----------------|---------------|
| 8 | BM Orientation = 1.0 | `benchmark_orientation_mode="max"` | Does max benchmark-chasing intensify dimensional mismatch? |
| 9 | BM Orientation adjustable | `benchmark_orientation_mode="adjustable"` | Can providers learn to de-emphasize benchmarks? |
| 10 | Dynamic Evaluator | `dynamic_evaluator=True` | Does signal-responsive benchmark introduction improve validity? |
| 11 | OS without externalities | `os_belief_broadcast=False, os_safety_erosion=False` | Are OS information/safety externalities driving Goodhart acceleration? |
| 12 | Eval-as-a-company | `evaluator_as_company=True` | Do evaluation conflicts of interest worsen outcomes? |
| 13 | Aligned Benchmarks | `aligned_benchmarks=True` | Is benchmark-need misalignment the root cause of gaming? |

### Category 3: Internal Validity Checks

Test whether results are artifacts of simulation design choices.

| # | Condition | Config override | What it tests |
|---|-----------|-----------------|---------------|
| 14 | Homogeneous Consumers | `homogeneous_consumers=True` | Is consumer heterogeneity load-bearing for the dynamics? |
| 15 | Homogeneous Providers | `homogeneous_providers=True` | Is differentiation emergent or baked into initial conditions? |

### Condition x Preset Matrix

Each condition is run under all 3 regulatory presets: **Balanced**, **US light-touch**, **EU precautionary**.

Total Phase 1 runs: **15 x 3 = 45**.

---

## Metrics

All metrics are computed from `rounds.jsonl`. Source fields are from the new
architecture logging (see TODO.md "Plotting Redo" for field descriptions).

### Primary Outcomes

| Metric | Computation | Aggregation |
|--------|-------------|-------------|
| Gap decomposition: score noise | `score - dot(cap, bm_agg)` per provider | per-round + last-5r mean |
| Gap decomposition: dim mismatch | `dot(cap, bm_agg) - dot(cap, need)` per provider | per-round + last-5r mean |
| Gap decomposition: penalty load | `dot(cap, need) - satisfaction` per provider | per-round + last-5r mean |
| Total score-satisfaction gap | `score - satisfaction` per provider | per-round + last-5r mean |
| Score reliability | `Pearson_r(score_rank, satisfaction_rank)` | per-round |
| HHI market concentration | `sum(market_share^2)` | per-round + last-5r mean |
| Mean consumer satisfaction | `consumer_data.avg_satisfaction` | per-round + last-5r mean |

### Secondary Outcomes

| Metric | Computation | Aggregation |
|--------|-------------|-------------|
| Mean capability growth | `mean(cap_T) - mean(cap_0)` across providers | scalar per run |
| Safety investment (mean) | `mean(strategies[p].safety)` across providers | per-round |
| Growth direction alignment | `cos(cap_T - cap_0, need_weights)` per provider | scalar per run |
| Benchmark orientation | `benchmark_orientations[p]` | per-round (meaningful only in adjustable mode) |
| Funder concentration | correlation of funder allocations across providers | per-round |
| Incident count by severity | from `incidents` | cumulative per run |
| Intervention count by type | from `regulator_data.interventions` | cumulative per run |
| Consumer switching rate | `consumer_data.switching_rate` | per-round |
| Per-benchmark score spread | `std(scores)` across providers per benchmark | per-round per-benchmark |

### Pattern Validation (binary per run -> pass-rate across seeds)

| Pattern | Criterion |
|---------|-----------|
| Dimensional mismatch emerges | `abs(dot(cap, bm_agg) - dot(cap, need)) > 0.02` for market leader by round 15 |
| Penalty channel dominates | `penalty_load > abs(dim_mismatch)` for market leader at final round |
| Score reliability declines | `score_reliability` drops below 0.7 by round 20 |
| Safety underinvestment | mean safety allocation declines from initial by round 20 |
| Market concentration | HHI exceeds 0.25 by final round |
| Benchmark turnover | at least one new benchmark introduced after round 0 |
| Regulatory escalation | at least one intervention beyond `request_voluntary_commitment` |

---

## Phase 1: Core Ablations

### Design

- 15 conditions x 3 presets = 45 experiments
- All runs: 30 rounds, single seed (seed=1), Qwen3-235B-A22B
- Output: `hf_data/llm_core/qwen-235b/<condition_preset>/seeds/seed_1/`

### CLI

```bash
# Baseline
python scripts/run_experiment.py --condition full_ecosystem --policy balanced

# Any ablation
python scripts/run_experiment.py --condition no_media --policy us
python scripts/run_experiment.py --condition aligned_benchmarks --policy eu
python scripts/run_experiment.py --condition bm_orientation_max --policy balanced
```

---

## Phase 2: Independent Replications

### Design

- Seeds 1-30 per condition
- 30 rounds per run
- Total: 45 conditions x 30 seeds = **1,350 runs**

### Priority

| Priority | Conditions | Rationale |
|----------|-----------|-----------|
| P0 | Full Ecosystem (x3 presets), Aligned Benchmarks (x3), BM Orientation Max (x3) | Central thesis tests |
| P1 | No Incidents, No OpenSource, Dynamic Evaluator, No Regulator (x3 each) | High-signal structural and mechanism ablations |
| P2 | Remaining conditions (x3 each) | Complete the matrix |

---

## Phase 3: Sensitivity Analysis

### Purpose

Test whether qualitative findings are artifacts of specific parameter choices.
One-at-a-time perturbation sweeps, 3 seeds per point.

### Parameters to Sweep

| Parameter | Baseline | Sweep values | Rationale |
|-----------|----------|-------------|-----------|
| `rnd_efficiency` | 0.05 | 0.02, 0.03, 0.05, 0.08, 0.12 | R&D gain scaling; controls capability growth rate |
| `learning_rate` | 0.15 | 0.0, 0.05, 0.15, 0.30, 0.50 | Belief update speed; higher = faster Goodhart |
| `benchmark_orientation` (all providers) | 0.80 | 0.5, 0.65, 0.80, 0.90, 1.0 | Continuous version of the BM orientation ablation |
| Incident base rate | 0.10 | 0.0, 0.05, 0.10, 0.20, 0.30 | Does doubling incidents change safety investment? |
| Satisfaction signal noise (`sigma_base`) | TBD | 0.5x, 1x, 2x, 4x baseline | How reliable is user feedback? |

### Design

- 5 parameters x 5 levels x 3 seeds = **75 runs**
- Base condition: `full_ecosystem_balanced`, 30 rounds
- Also run `rnd_efficiency` sweep on `no_incidents` condition to check for
  interaction effects (15 additional runs)

### Key Questions

For each parameter, does the qualitative finding persist?
- Penalty channel dominates the gap (or does dim mismatch take over at high orientation?)
- Market concentrates (HHI > 0.25)
- Score reliability declines

---

## Phase 4: Cross-Model Robustness

### Purpose

Demonstrate that qualitative findings are not artifacts of a single LLM's
behavioral biases.

### Models

| Model | Provider | Priority |
|-------|----------|----------|
| Qwen3-235B-A22B | Local (vLLM) | Primary (all phases) |
| DeepSeek-R1 | Local (vLLM) | 1 — strong CoT contrast |
| Gemini 2.5 Flash | Google | 2 — cheapest cloud |
| Claude Sonnet 4.6 | Anthropic | 3 — different provider |

### Design

- `full_ecosystem_balanced` only, 5 seeds per model
- Compare: gap decomposition trajectories, pattern pass/fail, strategy differentiation
- Total: **15 runs** (3 models x 5 seeds)

---

## Phase 5: Heuristic Baseline

### Purpose

Compare LLM-driven actors against heuristic (rule-based) actors. Fully
seed-controlled (no API stochasticity).

### Design

- All 45 conditions, 30 seeds each = **1,350 runs**
- No API calls — free and fast
- Primary comparison: do LLM providers produce qualitatively different dynamics?

---

## Execution Order

1. **Phase 5** — Heuristic baseline (free, validates infrastructure, catches bugs)
2. **Phase 1** — 45 core LLM runs (one seed each)
3. **Phase 2 P0** — Replications for baseline + aligned benchmarks + BM orientation max (9 conditions x 30 seeds)
4. **Phase 4** — Cross-model (15 runs, early robustness check)
5. **Phase 2 P1** — High-signal ablation replications
6. **Phase 3** — Sensitivity sweeps (90 runs)
7. **Phase 2 P2** — Remaining replications

---

## Budget Summary

| Phase | Runs | Model | Est. Cost |
|-------|------|-------|-----------|
| Phase 1 | 45 | Qwen (local) | ~$0 |
| Phase 2 | 1,350 | Qwen (local) | ~$0 |
| Phase 3 | 90 | Qwen (local) | ~$0 |
| Phase 4 | 15 | Mixed (cloud) | ~$30 |
| Phase 5 | 1,350 | None (heuristic) | $0 |
| **Total** | **2,850** | | **~$30 cloud** |

---

## Storage Policy

- **Per seed**: `rounds.jsonl` + `summary.json` + `config.json` + `metadata.json`
- **Per condition** (post-hoc): `aggregate.json` with per-round mean/CI for all metrics
- **Registry**: `hf_data/runs.jsonl` built by `scripts/registry_build.py`
- Phase 1 seed_1 runs also keep `game_log.md` for qualitative inspection
