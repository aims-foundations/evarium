# Experiment Plan: Factorial Design & Ablation

## Overview

This document tracks the full experimental plan for the simulation, including
completed experiments, planned replications, sensitivity sweeps, and cross-model
comparisons. The design is organized into five phases:

1. **Phase 1** — Structural ablations: 27 canonical conditions (9 structural × 3 regulatory presets), single seed, 30 rounds
2. **Phase 2** — Independent replications for statistical inference (10 seeds/condition)
3. **Phase 3** — Sensitivity analysis (continuous parameter sweeps)
4. **Phase 4** — Cross-model robustness (multiple LLMs)
5. **Phase 5** — Heuristic baseline (rule-based actors, fully seed-controlled)

**Primary model:** Qwen3-235B-A22B (vLLM, local)
**Round count:** Standardized to **30 rounds** across all conditions and phases.

---

## Output Directory Structure

Experiments are organized by purpose. The `core/` directory holds the 27 canonical
single-seed reference runs. The `validation/` directory holds all robustness evidence.

```
output/
  core/                              # Phase 1: 27 canonical single-seed runs
    full_ecosystem_balanced/         # Full artifacts (game_log, rounds, history, plots)
    full_ecosystem_us/
    full_ecosystem_eu/
    ablation_no_media_balanced/
    ablation_no_media_us/
    ablation_no_media_eu/
    ablation_no_incidents_balanced/
    ablation_no_incidents_us/
    ablation_no_incidents_eu/
    ablation_no_startups_balanced/
    ablation_no_startups_us/
    ablation_no_startups_eu/
    ablation_no_opencore_balanced/
    ablation_no_opencore_us/
    ablation_no_opencore_eu/
    ablation_single_benchmark_balanced/
    ablation_single_benchmark_us/
    ablation_single_benchmark_eu/
    ablation_no_funders_balanced/
    ablation_no_funders_us/
    ablation_no_funders_eu/
    ablation_no_bench_evolution_balanced/
    ablation_no_bench_evolution_us/
    ablation_no_bench_evolution_eu/
    ablation_eval_as_company_balanced/
    ablation_eval_as_company_us/
    ablation_eval_as_company_eu/

  validation/
    heuristic_baseline/              # Phase 5: 27 conditions x 10 seeds, no LLM
      full_ecosystem_balanced/
        aggregate.json               # Primary artifact: per-round mean/CI, pattern pass rates
        seeds/
          seed_1/
            rounds.jsonl
            summary.json
            config.json
          seed_2/
            ...
      ...

    replications_llm/                # Phase 2: LLM replications
      qwen/
        full_ecosystem_balanced/
          aggregate.json
          seeds/
            seed_1/
              rounds.jsonl
              summary.json
              config.json
            ...
        ...

    sensitivity/                     # Phase 3: parameter sweeps
      rnd_efficiency/
        aggregate.json
      benchmark_validity_decay/
      benchmark_exploitability_growth/
      startup_entry_probability/
      capability_ceiling/
      initial_capability/

    cross_model/                     # Phase 4: organized by condition then model
      full_ecosystem_balanced/
        deepseek/
          aggregate.json
          seeds/seed_1/ ...
        gemini_flash/
        gemini_pro/
        gpt_5/
        claude_sonnet_4/

  runs.jsonl                         # Post-hoc registry (see Runs Registry section)
  reproduce_logs/                    # Raw shell logs from run_phase.sh
```

### Storage Policy

- **`core/`**: Store everything — `game_log.md`, `rounds.jsonl`, `history.json`,
  `summary.json`, `config.json`, `metadata.json`, `plots/`, `providers/`,
  `funders/`, `policymakers/`. These are the reference runs cited in the paper.

- **`validation/` per-seed**: Store `rounds.jsonl` + `summary.json` + `config.json`
  + `metadata.json`. Skip `game_log.md`, `history.json`, `plots/`, `providers/`,
  `funders/`, `policymakers/`.
  - `rounds.jsonl` is kept because it is the raw data source: all metrics can be
    re-extracted from it and plots can be regenerated if needed.
  - `summary.json` is the pre-extracted fast-query artifact used to build the
    central CSV and runs registry without loading raw data.

- **`aggregate.json`** (per condition in validation): Per-round mean/CI for all
  metrics, pattern pass/fail rates across seeds. Primary artifact for paper tables.

- **Central CSV**: Built post-hoc from `aggregate.json` files across all conditions
  and phases (see Metrics section for schema).

---

## Phase 1: Structural Ablations

### Design

Full factorial over structural conditions × regulatory presets.
All runs: 30 rounds, single seed (seed=1), Qwen3-235B-A22B.

- **9 structural conditions**: Full Ecosystem + 8 one-at-a-time ablations
- **3 regulatory presets**: Balanced, US light-touch, EU precautionary
- **Total: 27 experiments**

### Condition Table

| Condition | Balanced | US | EU |
|-----------|----------|----|----|
| Full Ecosystem | Pending | Pending | Pending |
| No Media | Pending | Pending | Pending |
| No Incidents | Pending | Pending | Pending |
| No Startups | Pending | Pending | Pending |
| No OpenCore | Pending | Pending | Pending |
| Single Benchmark | Pending | Pending | Pending |
| No Funders | Pending | Pending | Pending |
| No Benchmark Evolution | Pending | Pending | Pending |
| Eval As Company | Pending | Pending | Pending |

### Condition Matrix

```
                       Balanced                    US Light-Touch              EU Precautionary
Full Ecosystem         full_ecosystem_balanced     full_ecosystem_us           full_ecosystem_eu
No Media               ablation_no_media_balanced  ablation_no_media_us        ablation_no_media_eu
No Incidents           ablation_no_incidents_*     ablation_no_incidents_*     ablation_no_incidents_*
No Startups            ablation_no_startups_*      ablation_no_startups_*      ablation_no_startups_*
No OpenCore            ablation_no_opencore_*      ablation_no_opencore_*      ablation_no_opencore_*
Single Benchmark       ablation_single_bench_*     ablation_single_bench_*     ablation_single_bench_*
No Funders             ablation_no_funders_*       ablation_no_funders_*       ablation_no_funders_*
No Bench Evolution     ablation_no_bench_evol_*    ablation_no_bench_evol_*    ablation_no_bench_evol_*
Eval As Company        ablation_eval_as_company_*  ablation_eval_as_company_*  ablation_eval_as_company_*
```

### TODO (Phase 1)

- [ ] Await completion of all 27 Qwen runs
- [ ] Reorganize completed output into `core/` structure

### Historical Reference (Claude 3.5 Sonnet)

exp_001–exp_015 used Claude 3.5 Sonnet and are preserved in `output/experiments/`
as permanent reference runs. They cover the balanced ablations (exp_004–exp_012),
primary baseline (exp_011), eval-as-company (exp_012), full ecosystem US/EU at 30r
(exp_001–exp_002), and 50-round variants (exp_013–exp_015). exp_003 is a duplicate
of exp_001 but is retained. These runs are superseded by the Qwen Phase 1 runs for
analysis purposes but must not be deleted.
Diagnostic results from those runs are documented in the Findings section below.

---

## Phase 2: Independent Replications

### Purpose

Report inter-run means, standard deviations, and 95% confidence intervals.
Each condition needs N ≥ 10 replications to produce meaningful CIs via
t-distribution. Stored under `validation/replications_llm/<model>/`.

### Design

- **Seeds**: 30 distinct seeds per condition (seeds 1–30)
- **Rounds**: 30 per run
- **CRN caveat**: Seed controls simulation RNG (incident sampling, market
  dynamics, benchmark noise) but not LLM server-side stochasticity. CRN
  provides partial variance reduction. For full seed control, use Phase 5
  (heuristic).
- **Storage**: `rounds.jsonl` + `summary.json` + `config.json` + `metadata.json`
  per seed; `aggregate.json` per condition.

### Replication Plan

All 27 conditions, 30 seeds each = **810 runs** total.

| Priority | Condition | Preset | Seeds | Model |
|----------|-----------|--------|-------|-------|
| P0 | Full Ecosystem | Balanced | 1–30 | Qwen3-235B |
| P0 | Full Ecosystem | US | 1–30 | Qwen3-235B |
| P0 | Full Ecosystem | EU | 1–30 | Qwen3-235B |
| P1 | No OpenCore | Balanced | 1–30 | Qwen3-235B |
| P1 | No OpenCore | US | 1–30 | Qwen3-235B |
| P1 | No OpenCore | EU | 1–30 | Qwen3-235B |
| P1 | No Startups | Balanced | 1–30 | Qwen3-235B |
| P1 | No Startups | US | 1–30 | Qwen3-235B |
| P1 | No Startups | EU | 1–30 | Qwen3-235B |
| P1 | Single Benchmark | Balanced | 1–30 | Qwen3-235B |
| P1 | Single Benchmark | US | 1–30 | Qwen3-235B |
| P1 | Single Benchmark | EU | 1–30 | Qwen3-235B |
| P2 | No Media | Balanced | 1–30 | Qwen3-235B |
| P2 | No Media | US | 1–30 | Qwen3-235B |
| P2 | No Media | EU | 1–30 | Qwen3-235B |
| P2 | No Incidents | Balanced | 1–30 | Qwen3-235B |
| P2 | No Incidents | US | 1–30 | Qwen3-235B |
| P2 | No Incidents | EU | 1–30 | Qwen3-235B |
| P2 | No Funders | Balanced | 1–30 | Qwen3-235B |
| P2 | No Funders | US | 1–30 | Qwen3-235B |
| P2 | No Funders | EU | 1–30 | Qwen3-235B |
| P2 | No Bench Evolution | Balanced | 1–30 | Qwen3-235B |
| P2 | No Bench Evolution | US | 1–30 | Qwen3-235B |
| P2 | No Bench Evolution | EU | 1–30 | Qwen3-235B |
| P2 | Eval As Company | Balanced | 1–30 | Qwen3-235B |
| P2 | Eval As Company | US | 1–30 | Qwen3-235B |
| P2 | Eval As Company | EU | 1–30 | Qwen3-235B |

### Commands

```bash
# P0: Full ecosystem replications
./run_phase.sh --phase 2p0 --model qwen

# P1/P2: Ablation replications
./run_phase.sh --phase 2p1 --model qwen
./run_phase.sh --phase 2p2 --model qwen

# Analyze
python scripts/run_diagnostics.py analyze <batch_name>
```

---

## Phase 3: Sensitivity Analysis

### Purpose

Address reviewer concern that findings may be artifacts of specific parameter
choices. One-at-a-time perturbation sweeps over key hyperparameters, 3 seeds per
perturbation point. Results stored under `validation/sensitivity/<param>/`.

### Parameters to Sweep

| Parameter | Baseline | Sweep Values | Rationale |
|-----------|----------|-------------|-----------|
| `rnd_efficiency` | 0.01 | 0.005, 0.008, 0.01, 0.012, 0.015 | R&D effectiveness; controls capability growth rate |
| `benchmark_validity_decay_rate` | 0.02 | 0.01, 0.015, 0.02, 0.03, 0.04 | How fast benchmarks degrade under gaming |
| `benchmark_exploitability_growth_rate` | 0.015 | 0.005, 0.01, 0.015, 0.02, 0.03 | Returns to eval engineering |
| `startup_entry_probability` | 0.09 | 0, 0.05, 0.09, 0.15, 0.25 | Market contestability |
| `capability_ceiling` | 1.0 | 0.7, 0.85, 1.0, 1.2 | Upper bound on capability |
| Initial true capability (mean) | 0.25 | 0.15, 0.20, 0.25, 0.30, 0.35 | ±40% perturbation |
| `capability_shift` | 0.0 | -0.10, 0.0, 0.10, 0.20, 0.30 | Shift applied to provider initial values and policymaker absolute thresholds |

### Design

- 7 parameters × 5 levels × 3 seeds = **105 runs**
- Base condition: `full_ecosystem_balanced`, 30 rounds, Qwen3-235B
- Storage: `rounds.jsonl` + `summary.json` per seed; `aggregate.json` per parameter.

### Key Questions

For each parameter, does the qualitative finding persist?
- "Gaming gap > 0.10 at end" (score inflation is persistent)
- "HHI increases over time" (market concentrates)
- "Benchmark validity declines" (Goodhart decay occurs)

### Commands

```bash
./run_phase.sh --phase 3 --model qwen

# Or directly:
python scripts/run_diagnostics.py sensitivity full_ecosystem_balanced \
  --param rnd_efficiency --values 0.005,0.008,0.01,0.012,0.015 --n-seeds 3
```

---

## Phase 4: Cross-Model Robustness

### Purpose

Demonstrate that qualitative findings are not artifacts of a single LLM's
behavioral biases. If the same emergent patterns arise under different LLM
backbones, the dynamics are driven by simulation structure, not LLM idiosyncrasies.
Results stored under `validation/cross_model/<condition>/<model>/`.

### Models to Compare

| Model | Provider | Supported |
|-------|----------|-----------|
| Qwen3-235B-A22B | Local (vLLM) | Yes — primary |
| DeepSeek-R1 | Local (vLLM) | Yes |
| Gemini 2.5 Flash | Google | Yes |
| Gemini 2.5 Pro | Google | Yes |
| GPT-5 | OpenAI | Yes |
| Claude Sonnet 4 | Anthropic | Yes |

### Design

- Run `full_ecosystem_balanced` (30 rounds) with each non-Qwen model
- 5 seeds per model
- Compare: gaming gap trajectory, pattern validation pass/fail rates, strategy drift
- Storage: `rounds.jsonl` + `summary.json` per seed; `aggregate.json` per model.

### Priority Order

1. **DeepSeek-R1** — local, strong explicit CoT contrast with Qwen
2. **Gemini 2.5 Flash** — cheapest; validates findings hold at budget scale
3. **GPT-5** — different provider and reasoning style
4. **Gemini 2.5 Pro** — stronger Gemini for quality comparison
5. **Claude Sonnet 4** — Anthropic cross-check

### Commands

```bash
./run_phase.sh --phase 4
```

---

## Phase 5: Heuristic Baseline

### Purpose

Compare LLM-driven actors against heuristic (rule-based) actors to quantify
what the LLM contributes. Fully seed-controlled (no API stochasticity), so
CRN guarantees hold exactly. Results stored under
`validation/heuristic_baseline/<condition>/`.

### Design

- All 27 conditions, 30 seeds each, 30 rounds = **810 runs**
- No API calls — free and fast
- Compare pattern validation pass rates: LLM vs heuristic
- Storage: `rounds.jsonl` + `summary.json` per seed; `aggregate.json` per condition.

### Commands

```bash
./run_phase.sh --phase 5
```

---

## Runs Registry

### Design

A flat `output/runs.jsonl` (one line per run) generated **post-hoc** by walking
the filesystem. Never written to during execution — safe for parallel cluster runs
with no locking or stagger hacks needed. Replaces the current `index.json`
race-condition workaround (the 3-second stagger in `rerun_experiment.py`).

```bash
python scripts/build_registry.py   # walks output/, writes output/runs.jsonl
```

Each row contains discriminating attributes and key inline metrics so aggregation
queries don't require loading individual `summary.json` files:

```jsonl
{"condition": "full_ecosystem_balanced", "phase": "replications_llm", "model": "qwen", "seed": 3, "rounds": 30, "git_commit": "abc123", "path": "validation/replications_llm/qwen/full_ecosystem_balanced/seeds/seed_3", ...metrics...}
```

### Parallel Safety

- Each run writes only to its own directory — no shared state during execution
- `aggregate.json` is generated post-hoc (after all seeds done), never written concurrently
- Maps cleanly to SLURM job arrays: one job = one seed, fully independent
- Registry regeneration runs as a final step after all array jobs complete:
  `--dependency=afterok:$ARRAY_JOB_ID`

### Aggregation Patterns

| Query | Filter | Group by |
|-------|--------|----------|
| Within-condition variance | `condition == X, phase == replications_llm` | seed |
| Cross-model comparison | `condition == X, phase == cross_model` | model |
| Ablation comparison | `phase == core` or `phase == replications_llm` | condition |
| Preset comparison | `condition_base == full_ecosystem` | preset |
| LLM vs heuristic | `condition == X` | phase |
| Sensitivity sweep | `phase == sensitivity, param == Y` | param_value |

---

## Budget Summary

| Phase | Runs | Model | Est. Cost |
|-------|------|-------|-----------|
| Phase 1 | 27 | Qwen3-235B (local) | ~$0 |
| Phase 2 | 810 | Qwen3-235B (local) | ~$0 |
| Phase 3 | 90 | Qwen3-235B (local) | ~$0 |
| Phase 4 | 25 | Mixed (cloud) | ~$53 |
| Phase 5 | 810 | None (heuristic) | $0 |
| **Total** | **1762** | | **~$53 cloud** |

---

## Implementation Note

> Before executing any phase, `run_phase.sh` and all other `.sh` scripts must be
> updated to match this spec: 27 conditions, 30 seeds, Qwen3-235B as primary model,
> `core/` + `validation/` output directory structure, and `build_registry.py`
> integration. The current scripts reflect the older 11-condition / Claude design.

---

## Execution Order

1. [x] **Claude Phase 1 reference** — exp_001–exp_015 (Claude 3.5 Sonnet, preserved permanently)
2. [ ] **Phase 1** — 27 Qwen core runs (in progress)
3. [ ] **Reorganize** — Migrate completed runs into `core/` structure; run `build_registry.py`
4. [ ] **Phase 5** — Heuristic baseline (free, fast, validates infrastructure)
5. [ ] **Phase 2 P0** — Full-ecosystem × 3 preset replications (most important for paper)
6. [ ] **Phase 4** — Cross-model comparison (DeepSeek first)
7. [ ] **Phase 2 P1** — High-signal ablations × 3 presets
8. [ ] **Phase 3** — Sensitivity sweeps
9. [ ] **Phase 2 P2** — Remaining ablation replications

---

## Diagnostics Output

After each validation phase, run:

```bash
python scripts/run_diagnostics.py analyze <batch_name>
```

Key outputs per batch (`aggregate.json`):
- Per-round mean/CI for all metrics
- Pattern pass/fail rates across seeds (7 checks)
- Strategy drift and role adherence summary

Plots (generated at batch level only, not per-seed):
- Trajectory overlays with confidence bands
- Tornado charts (sensitivity phase)
- Cross-model comparison grids

---

## Metrics to Track Per Run

One `summary.json` per run and one row in the central CSV. Per-round trajectories
stored as JSON arrays. Source for all metrics is `rounds.jsonl`.

### Primary Outcomes

| Metric | Source in `rounds.jsonl` | Aggregation |
|--------|--------------------------|-------------|
| Mean score inflation | `mean(scores[p] - true_capabilities[p])` | per-round + last-5r mean |
| Score inflation per provider | `scores[p] - true_capabilities[p]` | per-round |
| Mean true capability | `mean(true_capabilities.values())` | per-round + last-5r mean |
| True capability per provider | `true_capabilities[p]` | per-round |
| Mean eval engineering | `mean(strategies[p].evaluation_engineering)` | per-round + last-5r mean |
| Eval eng per provider | `strategies[p].evaluation_engineering` | per-round |
| HHI | `sum(s^2 for s in consumer_data.market_shares.values())` | per-round + last-5r mean |
| Mean consumer satisfaction | `consumer_data.avg_satisfaction` | per-round + last-5r mean |
| Benchmark validity (alpha) | `benchmark_params[b].validity` | per-round per-benchmark |
| Benchmark exploitability (beta) | `benchmark_params[b].exploitability` | per-round per-benchmark |
| Validity correlation (rolling r) | Pearson r(scores, true_caps), window=5 | per-round per-benchmark |

### Secondary Outcomes

| Metric | Source in `rounds.jsonl` | Aggregation |
|--------|--------------------------|-------------|
| Safety alignment (mean) | `mean(strategies[p].safety_alignment)` | per-round |
| Fundamental research (mean) | `mean(strategies[p].fundamental_research)` | per-round |
| Strategy drift (cosine) | cosine dist between consecutive strategy vectors | per-round per-provider |
| OLS slope (score ~ true_cap) | regression across providers per benchmark | last-10r aggregate |
| OLS intercept (floor bias) | same regression | last-10r aggregate |
| Funding multiplier per provider | `funder_data.funding_multipliers[p]` | per-round |
| Funding-score correlation | Pearson r(funding_multiplier, published_score) | per-round |
| Funding-capability correlation | Pearson r(funding_multiplier, true_capability) | per-round |
| Active sanction count | `len(policymaker_data.active_sanctions)` | per-round |
| Intervention counts by type | `policymaker_data.interventions` | cumulative per run |
| Time to first intervention | first round with non-empty interventions | scalar per run |
| Incident count by severity | from incident fields | cumulative per run |
| Consumer switching rate | `consumer_data.switching_rate` | per-round |
| BTE composite + components | `barrier_to_entry.*` | per-round |
| Startup entry count | rounds where `new_entrant` key present | scalar per run |
| OpenCore ecosystem influence | `open_source_data.OpenCore.ecosystem_influence` | per-round |
| OpenCore commoditization fired | `open_source_data.OpenCore.commoditization_shock_fired` | boolean per run |
| Media sentiment | `media_data.sentiment` | per-round |
| Benchmark turnover count | retirements + introductions | scalar per run |
| Role adherence violations | "true capability"/"actual capability" in `actor_traces` | cumulative per run |

### Pattern Validation (binary per run → pass-rate across seeds)

| Pattern | Criterion |
|---------|-----------|
| Score Inflation | `mean_inflation > 0.10` sustained by round 15 |
| Benchmark Turnover | at least one retirement + introduction |
| Regulatory Escalation | at least one intervention beyond `investigation` |
| Commoditization Shock | `open_source_data.OpenCore.commoditization_shock_fired == true` |
| Safety Incident Response | funder adjusts allocation following a major/critical incident |
| Gaming Persistence | `mean_eval_eng` above initial level through round 20+ |
| Funding Follows Scores | r(funding, score) > r(funding, true_capability) |

### Aggregation Protocol

Per-round metrics: `mean_trajectory[t]`, `std_trajectory[t]`, `CI95_lower[t]`, `CI95_upper[t]` (t-dist, df=N-1).

Scalars: `mean`, `std`, `CI95_lower`, `CI95_upper`.

Pattern pass/fail: `pass_rate` + Wilson 95% CI.

Minimum N: **10 seeds** (30 preferred).

### Metrics to Embed in Runs Registry

Per-run scalar metrics for fast querying (inlined into `runs.jsonl`):

**Final-state / last-5r scalars:**
- `gaming_gap_final` — mean(scores - true_caps) at round 30
- `gaming_gap_avg_last5` — average over rounds 26–30
- `hhi_final` — market concentration at round 30
- `mean_capability_final` — average true capability at round 30
- `mean_eval_eng_final` — average eval engineering allocation at round 30
- `benchmark_validity_final` — average benchmark validity at round 30
- `role_adherence_violations` — count of hidden-state leakage terms

**Per-pattern pass/fail flags:**
- `pattern_score_inflation`
- `pattern_benchmark_turnover`
- `pattern_regulatory_escalation`
- `pattern_commoditization_shock`
- `pattern_safety_incident_response`
- `pattern_gaming_persistence`
- `pattern_funding_follows_scores`

**Run-level metadata:**
- `condition`, `preset`, `phase`, `model`, `seed`, `rounds`, `git_commit`,
  `created_at`, `runtime_seconds`, `path`

---

## Findings from Claude 3.5 Sonnet Reference Runs (exp_001–exp_015)

> These findings are from exp_001–exp_015 (Claude 3.5 Sonnet). Retained for
> reference; will be updated once Qwen Phase 1 core runs are complete.

### Pattern Validation

| Pattern | Pass Rate | Notes |
|---------|-----------|-------|
| Score Inflation | 11/11 | Universal |
| Regulatory Escalation | 11/11 | Universal |
| Benchmark Turnover | 9/11 | Fails only: Single Benchmark, No Bench Evolution (expected) |
| Commoditization Shock | 10/11 | Fails only: No OpenCore (expected) |
| Safety Incident Response | 10/11 | Fails only: No Funders |
| Gaming Persistence | 9/11 | Fails in No Startups; 50r runs (not in active design) also showed failure |
| Funding Follows Scores | 2/11 | Funders track true capability, not scores |

### Role Adherence

52–225 violations per experiment (~4/round). Violations scale linearly with run
length, consistent with per-round LLM hallucination rather than information leakage.
Needs investigation: are actors hallucinating or genuinely leaking hidden state?

### Ablation Effects (vs full_ecosystem_balanced, avg rounds 26–30)

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
