# Stakeholder Architecture: No Explicit Gaming

> **Status: Pre-implementation plan. Last updated: 2026-03-23.**
> Gaming emerges from provider data sourcing decisions and benchmark weight mismatch — not from an explicit investment lever. The prior architecture (with explicit `evaluation_engineering`) is preserved in `rough/stakeholders_old_eval_eng.md`.

---

## Provider Name Mapping

Provider names are anonymized to prevent LLM reasoning from being biased by real-world company reputations.

| Simulation Name | Modeled After |
|-----------------|---------------|
| Orion Labs | OpenAI |
| Apex AI | Anthropic |
| Genesis Systems | Google DeepMind |
| Mirage AI | Meta AI |
| Spark AI | (generic benchmark-focused startup) |
| OpenCore | DeepSeek (open-source, `open_source: True`) |

**Simulation window:** 30 rounds ≈ 2.5 years (2023 Q1 → mid-2025). 1 round = 1 month.

---

## File Reference

| File | Purpose |
|------|---------|
| `docs/stakeholders.md` | This file — canonical architecture reference |
| `rough/design_diff.md` | Old (eval_eng) vs new design — all changed primitives |
| `rough/logging_spec.md` | verbose=False / verbose=True logging spec |
| `rough/validation_plan.md` | Validation plan — Sargent, PIMMUR, Windrum, Axtell, Park et al. |
| `src/simulation.py` | Core sim loop, `SimulationConfig`, `EvalEcosystemSimulation`, regulatory presets |
| `src/capability_dimensions.py` | `DIMENSIONS` constant, `dot()`, `normalize()`, `deficit_weights()` utilities |
| `src/visibility.py` | State classes: PublicState, PrivateState, GroundTruth, AIIncident |
| `src/actors/model_provider.py` | ModelProvider: plan/observe/reflect/execute cycle |
| `src/actors/evaluator.py` | Evaluator, Benchmark, benchmark pool, introduction/retirement |
| `src/actors/consumer.py` | ConsumerMarket with archetype × use-case segments |
| `src/actors/regulator.py` | Regulator with graduated interventions, calibrated EU/US presets |
| `src/actors/funder.py` | Funder (VC, gov, foundation types), media-aware |
| `src/actors/media.py` | Media actor (TechPress) — coverage influences downstream actors |
| `src/incidents.py` | `IncidentGenerator` — probabilistic AI safety incident generation |
| `src/llm.py` | Multi-provider LLM integration (OpenAI, Anthropic, Ollama, Gemini) |
| `src/plotting.py` | Per-experiment visualization dashboards |
| `src/experiment_logger.py` | `ExperimentLogger` + `DirectoryLogger` |
| `src/game_log.py` | Natural language game log generator |
| `scripts/run_experiment.py` | Editable experiment config — edit and run |
| `scripts/rerun_experiment.py` | Re-runs a past experiment from saved config |
| `scripts/compare_experiments.py` | Side-by-side experiment comparisons |
| `scripts/final_plots.py` | Canonical multi-experiment analysis |

---

## Actors Overview

| Actor | File | LLM mode | Role |
|-------|------|----------|------|
| Model Provider | `actors/model_provider.py` | Yes | Develops models, allocates R&D portfolio |
| Evaluator | `actors/evaluator.py` | Yes — `dynamic_evaluator=True` only | Operates benchmarks; introduces new benchmarks as ecosystem evolves |
| Consumer Market | `actors/consumer.py` | No — formula-based only | Segments (archetype × use-case); proportional switching |
| Regulator | `actors/regulator.py` | Yes | Graduated interventions; EU/US/balanced presets |
| Funder | `actors/funder.py` | Yes | VC, gov, foundation types; media-aware capital allocation |
| Media | `actors/media.py` | Yes | TechPress outlet; coverage influences all downstream actors |
| Incident System | `incidents.py` | No — probabilistic only | Probabilistic AI safety incidents; ecosystem propagation |

---

## Visibility System

Three-tier information access enforced structurally:

| Level | Who Can Access | Examples |
|-------|----------------|---------|
| **Public** | All actors | Published scores, leaderboard, regulatory interventions, market shares |
| **Private** | Self only | Beliefs, strategies, investment allocations, satisfaction signals |
| **Ground Truth** | Simulation only | Capability vectors, true satisfaction, benchmark dimension weights |

Ground truth is held externally by the simulation. No actor (including LLM prompts) can access hidden information.

`score_reliability` (Pearson-r of scores vs. consumer satisfaction) is computed by the simulation each round as a **researcher-only diagnostic** — logged to `rounds.jsonl` but never passed to any actor. Actors detect Goodhart dynamics only through their respective observable proxies (incidents, market share trends, media coverage).

---

## Design Philosophy

### Gaming as an Emergent Phenomenon

In the prior architecture, gaming was an explicit investment category (`evaluation_engineering`) with a named payoff term:

```
score ~ Normal(true_capability + eval_engineering × exploitability, σ²)
```

This made gaming's incentive axiomatic: it was always rewarded when `exploitability > 0`.

In this architecture, gaming is not pre-specified. Providers allocate a training budget across four levers and choose, per capability dimension, how narrowly or broadly to source training data. Goodhart dynamics arise when benchmark dimension weights diverge from consumer need weights and providers discover — through score signals — that specializing toward benchmark-measured dimensions raises scores faster than it raises satisfaction. The score-satisfaction gap is discovered by the simulation, not imposed by it.

### Removed Primitives

- `exploitability` — scalar property of the evaluator
- `gaming_penalty` — term in the consumer satisfaction formula
- `evaluation_engineering` — investment lever and portfolio key
- `gaming_pressure` — tracked metric in simulation state
- `eval_engineering_risk` — field in ProviderPrivateState
- `validity_decay` / `decay_rate` — manually tuned parameter
- `revise_benchmark` — evaluators introduce new benchmarks instead of revising existing ones

---

## Core Primitives

### Capability Dimensions

```python
DIMENSIONS = ["reasoning", "coding", "knowledge", "safety", "communication", "agentic"]
```

| Dimension | What it represents | Primary benchmark anchor | Primary investment pathway |
|---|---|---|---|
| `reasoning` | General problem solving, logic, multi-step inference | MMLU, GPQA, BIG-Bench | Reasoning-specific post-training, chain-of-thought RLHF |
| `coding` | Software engineering, code generation, debugging | HumanEval, MBPP | Code-specific training data, correctness-based RL |
| `knowledge` | Factual recall, domain expertise | MMLU subsets, domain evals | Domain corpus investment, retrieval fine-tuning |
| `safety` | Harmlessness, refusal quality, adversarial robustness | TruthfulQA, safety benchmarks | RLHF for harmlessness, red-teaming (via Safety lever) |
| `communication` | Instruction following, fluency, long-context coherence | MT-Bench, IFEval | Instruction-following RLHF, long-context training |
| `agentic` | Tool use, multi-step task execution, error recovery | SWE-bench, WebArena, BFCL | Multi-step trajectory RL, tool-use fine-tuning |

Dimensions are investment targets, not statistically orthogonal factors. The correlation between dimensions observed empirically reflects the dominance of Research (g-like) investment. `math` is absorbed into `reasoning`; `language` is replaced by `communication`; `domain` is replaced by `knowledge`; `agentic` is added as the current frontier of separable investment.

### ProviderGroundTruth

```python
@dataclass
class ProviderGroundTruth:
    capability_vector: dict[str, float]   # per-dimension score, 0–1
    safety_incidents_caused: int
    market_share: float
```

### BenchmarkGroundTruth

Hidden from all actors. Defines how the evaluator converts capability vectors into scores:

```python
@dataclass
class BenchmarkGroundTruth:
    category_dimension_weights: dict[str, dict[str, float]]  # hidden per-category loadings
    noise_sigma: float
    samples: int
```

### ConsumerSegment

```python
@dataclass
class ConsumerSegment:
    name: str
    size: float
    need_weights: dict[str, float]    # normalized, sums to 1; ground truth utility function
    # archetype parameters: leaderboard_trust, switching_cost, switching_threshold, cost_sensitivity
```

---

## Score Formula

Each benchmark has public task categories and hidden dimension loadings per category. Published score is the dot product of the provider's capability vector with the benchmark's hidden aggregate dimension weights, plus Gaussian noise. Published scores are monotonically non-decreasing per provider (providers do not disclose a regression):

```
raw_score       = dot(capability_vector, benchmark_true_weights)
published_score = max(prev_published_score,
                      Normal(raw_score, (noise_sigma / sqrt(samples))²))
```

`benchmark_true_weights` are ground truth — held by the simulation, never passed to any actor. Providers observe per-category scores and infer what they reveal about the hidden dimension weights.

---

## Consumer Satisfaction Formula

```
satisfaction = dot(capability_vector, need_weights)
             - incident_penalty × (1 + market_share²)
             - media_penalty × leaderboard_trust
             + cost_bonus
```

There is no `gaming_penalty` term. The score-satisfaction gap is a measurement artifact: it arises when a provider's capability vector is tilted toward benchmark-weighted dimensions that the consuming segment does not need.

- **Incident penalty:** Severity-weighted (minor: 0.02, moderate: 0.08, major: 0.15, critical: 0.30); 2× if category matches segment sector. Scaled by `(1 + market_share²)` — the HHI contribution of a single firm, reflecting that dominant providers face greater scrutiny and reputational exposure per incident (grounded in scale-contingent regulatory obligations: EO 14110, SB 1047).
- **Media penalty:** `provider_attention × negative_sentiment × leaderboard_trust` — archetype-modulated; high-trust segments are more responsive to media signals, experience-driven segments are less so. Zero new parameters.
- **Cost bonus:** `cost_sensitivity × cost_advantage × 0.15`

### Expected Quality (Selection Stage)

Consumers select providers based on observed signals, not true capability. Expected quality is:

```
expected_quality[provider] = leaderboard_trust × dot(published_scores, effective_relevance)
                            + (1 - leaderboard_trust) × running_perceived_quality[provider]
```

`running_perceived_quality` is updated each round via EMA on realized satisfaction. This is the SERVQUAL Gap 5 framing: the gap between `expected_quality` and realized `satisfaction` drives switching dissatisfaction. AI services are credence goods — consumers cannot directly evaluate quality on their own tasks, so they rationally over-rely on benchmark signals (high `leaderboard_trust` segments) even when those signals are distorted.

Switching is triggered when `expected_quality - satisfaction > switching_threshold`.

---

## Provider Investment Model

### Portfolio Keys

Providers allocate 100% of their training budget across three levers each round:

| Lever | Competitive axis | Mechanical effect |
|---|---|---|
| `rd` | Capability (broad + targeted) | Directed toward benchmark-focused dimensions when `focus_level[b]` is set; approximately uniform when no deliberate focus; breakthrough-eligible |
| `safety` | Safety capability | Improves `capability_vector["safety"]` at fixed efficiency; always builds true safety capability |
| `product` | Market adoption | Accumulates `market_presence`; maps to `cost_advantage` → flows through to `cost_bonus` in satisfaction formula. Possible extensions: switching cost stickiness, enterprise segment adoption rate — both deferred. |

**Gaming mechanism:** When `focus_level[b]` is high for benchmark b, R&D gain concentrates on dimensions the provider believes b emphasizes (via `inferred_benchmark_weights[b]`). If those beliefs are accurate and benchmark weights diverge from consumer need weights, scores rise faster than consumer satisfaction. The score-satisfaction gap emerges without any explicit gaming term.

### Capability Update Rule

Each round, per-dimension:

```
focus_weights[b]    = normalize(focus_level[b] for b in active_benchmarks)
benchmark_driven[dim] = sum(focus_weights[b] × inferred_benchmark_weights[b][dim]
                            for b in active_benchmarks)
                        # when all focus_level[b] at baseline: benchmark_driven[dim] ≈ uniform

target[dim]         = benchmark_orientation × benchmark_driven[dim] + (1 - benchmark_orientation) × satisfaction_signal[dim]

gain[dim] = (
    rd     × target[dim]
  + safety × (1 if dim == "safety" else 0)
)

capability_vector[dim] = min(1.0, capability_vector[dim] + gain[dim])
```

Where:
- Absolute gain scaling for both `rd` and `safety` are calibration parameters (Thread 9)

`S_efficiency` dropped — the structural distinction between genuine safety investment and benchmark-driven safety gains already exists via the two additive pathways. Relative efficiency between them is a calibration choice, not a structural one.

### Provider Belief Model

Providers hold beliefs about the benchmark's hidden dimension weights, updated each round from score prediction errors.

**ProviderPrivateState additions:**

```python
inferred_benchmark_weights: dict[str, dict[str, float]]  # per-benchmark × per-dim; heuristic-updated; initially uniform per benchmark
focus_level: dict[str, float]                            # per active benchmark, running scalar; provider-calibrated baseline
benchmark_orientation: float                             # [0.05, 0.95]; per-provider initial value; ordinal LLM-updated
satisfaction_signal: dict[str, float]                    # 6-dim vector; noise ∝ 1/sqrt(market_share)
```

**New benchmark initialization:** When a benchmark b is introduced mid-simulation, `focus_level[b]` is initialized at `mean(focus_level[other active benchmarks])` for that provider. `inferred_benchmark_weights[b]` initializes uniform. All providers are scored on all active benchmarks each round regardless of focus_level — scores feed the belief update from the benchmark's introduction round onward. `focus_level` affects capability gains, not scoring participation.

**Belief update (both modes — heuristic):**

Updated each round per active benchmark from score prediction errors. Beliefs are epistemic state, not strategic choice — the LLM does not output belief updates.

```
for each active benchmark b:
    predicted_score[b]            = dot(capability_vector, inferred_benchmark_weights[b])
    error[b]                      = observed_score[b] - predicted_score[b]
    for dim in DIMENSIONS:
        inferred_benchmark_weights[b][dim] += learning_rate × error[b] × capability_vector[dim]
    inferred_benchmark_weights[b]  = normalize(clip_non_negative(inferred_benchmark_weights[b]))
```

`learning_rate` (default 0.15) is a config parameter.

**LLM call (single call per provider per round):**

Prompt inputs: per-category scores this round (own + competitor ranks), score delta vs. last round, current `portfolio`, current `focus_level` per benchmark, current `inferred_benchmark_weights` per benchmark, `satisfaction_signal` vector with confidence interval, last `reasoning_memory_depth` entries from `recent_insights`. No apparatus vocabulary (`gaming`, `exploitability`, `benchmark_weight_confidence`) appears in any prompt. Providers are addressed as "the strategy team at {name}."

LLM output JSON:
```json
{
  "portfolio":       {"rd": "more", "safety": "same", "product": "less"},
  "benchmark_focus": {"General Capability": "same", "Coding Evaluation": "more",
                      "Safety Evaluation": "less", "Instruction Following": "same"},
  "reasoning": "Free-text summary — appended to recent_insights"
}
```

Outputs are ordinal signals (`"more"` / `"less"` / `"same"`). The sim applies δ to running `portfolio`, `focus_level`, and `benchmark_orientation` state and renormalizes. `reasoning` is appended to `recent_insights`.

**Prompt framing note:** `benchmark_focus` decisions must be framed as relative priorities — "which benchmarks do you want to prioritise more than others this round?" — since saying "more" on all benchmarks simultaneously is a no-op after normalization. `portfolio` framing is naturally relative since it is zero-sum.

**`satisfaction_signal`:** Providers receive a 6-dim vector representing what their current user base values, derived from market-share-weighted consumer need weights. Modeled on private usage data and telemetry (e.g. CursorBench-style signals):

```
profile_share[p]         = sum over archetypes a of segment_share[a, p]
segment_weights[p]       = profile_share[p] / market_share[provider]   # sums to 1
true_signal[dim]         = sum over profiles p of (segment_weights[p] × need_weights[p][dim])
satisfaction_signal[dim] = clip(true_signal[dim] + Normal(0, σ_base / sqrt(market_share[provider])), min=0)
satisfaction_signal      = normalize(satisfaction_signal)
```

`true_signal` sums to 1 by construction (weighted average of distributions). Noise uses relative market share — larger providers get a more precise signal. Per-dimension noise drawn independently; clipped and renormalized. Tracks the provider's current user base composition: as market share shifts across segments, the signal shifts accordingly.

`benchmark_orientation` (default ~0.8) controls how much benchmark focus dominates over consumer signal in the capability update. Thread 9 calibration parameter. In LLM mode, surfaced in prompt as "how oriented is your R&D strategy toward benchmark performance vs. consumer feedback"; provider adjusts via ordinal output. In heuristic mode, feeds into the capability update mechanically but does not otherwise wire into portfolio or focus decisions.

### Default Provider Profiles

**Lever allocations (2023 Q1 baseline — Research + Development consolidated into R&D):**

| Provider | R&D | Safety | Product |
|---|---|---|---|
| Apex AI | 60% | 30% | 10% |
| Orion Labs | 55% | 15% | 30% |
| Genesis Systems | 70% | 15% | 15% |
| Mirage AI | 80% | 10% | 10% |
| Spark AI | 65% | 10% | 25% |
| OpenCore | 75% | 10% | 15% |

**Initial `focus_level[b]` (2023 baseline):**

Per-provider, per-benchmark baselines anchored to the 2023 empirical landscape. 6 providers × 4 starting benchmarks = 24 values; grows as new benchmarks are introduced per the pool schedule. See Thread 9 for calibration protocol. Qualitative anchors:
- Spark AI: highest focus on Coding Evaluation (explicit HumanEval orientation in 2023)
- Apex AI: elevated focus on Safety Evaluation relative to peers
- OpenCore: elevated focus on Coding Evaluation; lower on Safety
- All providers: low baseline focus on Instruction Following relative to General Capability and Coding

**Initial capability vectors (values in [0.40, 0.55] — calibrated for 30-round growth trajectory):**

| Provider | reasoning | coding | knowledge | safety | communication | agentic |
|---|---|---|---|---|---|---|
| Apex AI | 0.52 | 0.49 | 0.51 | 0.55 | 0.53 | 0.43 |
| Orion Labs | 0.54 | 0.51 | 0.53 | 0.51 | 0.54 | 0.47 |
| Genesis Systems | 0.53 | 0.48 | 0.54 | 0.49 | 0.51 | 0.45 |
| Mirage AI | 0.51 | 0.49 | 0.49 | 0.45 | 0.49 | 0.41 |
| Spark AI | 0.49 | 0.51 | 0.46 | 0.43 | 0.47 | 0.46 |
| OpenCore | 0.47 | 0.49 | 0.46 | 0.42 | 0.45 | 0.40 |

Score spread is intentionally compressed (~0.07) — early-round competition is tight, differentiation emerges from investment decisions over time. Formal empirical calibration against `external-validation/` data is pending.

### Cognitive Loop

1. **Observe** — per-category scores (own + competitor ranks), market share, incidents this round, media coverage, regulator interventions, `satisfaction_signal` vector
2. **Belief update** — heuristic: per-benchmark `inferred_benchmark_weights[b]` updated from score prediction errors (both modes)
3. **LLM call** — outputs ordinal {more/less/same} for `portfolio` levers and per-benchmark `focus_level`; sim applies deltas and renormalizes; `reasoning` appended to `recent_insights`; `public_comms` sampled from lever allocations
4. **Execute** — capability updates computed from focus-weighted `inferred_benchmark_weights`

**Heuristic incident pressure:** Safety incidents accumulate `_incident_safety_pressure` (minor: 0.03, moderate: 0.10, major: 0.20, critical: 0.30, cap: 0.40), shifting `portfolio["safety"]` upward. Decays 40%/round (~4-round effect).

### Cross-Round Memory (PIMMUR)

`ProviderPrivateState` holds `recent_insights` persisting LLM reasoning across rounds:

```python
recent_insights: list   # [{"round": int, "type": str, "reasoning": str}, ...]
```

Entry types: `"reflection"` and `"planning"`. The full list is kept in state; only the last `reasoning_memory_depth` entries are passed to LLM prompts (each truncated to 120 characters). `reasoning_memory_depth: int` is a config parameter (default 2). Setting it to 0 ablates memory injection.

No apparatus vocabulary appears in any prompt. Internal labels are translated to natural language before injection.

---

## Open Source Provider

### Design: Multiple Providers, One Initial Implementation

The architecture supports multiple concurrent OS providers with different configs. OS-specific properties are all per-provider config fields — nothing is hardcoded at the simulation level. Adding a second OS provider requires only a new config entry.

For the initial implementation, one OS provider (OpenCore) is active with `openness_level=1.0` (fully open — weights + training data public). OpenCore represents the aggregate of the open source ecosystem at any given time — whichever model is currently dominant. Its capability vector updates via continuous R&D and episodic step-change jumps (see Calibration Notes).

### Config Fields

| Field | Default | Description |
|---|---|---|
| `open_source` | `False` | Enables all OS-specific mechanics |
| `openness_level` | `0.0` | Fixed at init: 0=closed, 0.5=open-weight, 1.0=fully-open (weights + training data) |
| `cost_advantage` | `0.0` | Relative pricing competitiveness (0=most expensive, 1=free). OS providers default to 0.9 |
| `rd_budget_floor` | `1.0` | Exogenous minimum R&D budget regardless of funder allocations |
| `os_belief_broadcast` | `True` | Toggleable ablation: whether OS weights accelerate other providers' benchmark belief convergence |
| `broadcast_rate` | `0.30` (hardcoded constant) | Scales belief broadcast nudge strength per round |
| `os_safety_erosion` | `True` | Toggleable ablation: whether deployed safety is discounted below nominal |
| `erosion_sensitivity` | `0.50` (hardcoded constant) | Controls how rapidly safety erosion grows with deployment breadth |

### OS-Specific Mechanics

**No VC funding:** VC-type funders skip OS providers entirely (no equity model). Gov and foundation funders can still allocate. `rd_budget_floor` ensures OS providers are not starved by market dynamics regardless of funder behavior.

**Lower safety floor:** OS providers use `max(0.03, capability_vector["safety"])` vs. `max(0.05, ...)` for closed providers. Lower incentive without regulatory liability.

**Lower consumer switching friction:** Opportunity threshold halved when the alternative is an OS provider (free to try = lower barrier).

**Regulatory exemption:** OS providers are exempt from sanctions. Liability for downstream harms shifts to commercial deployers.

**Cost floor pressure:** `cost_bonus = cost_sensitivity × cost_advantage × 0.15` applies to all providers with non-zero `cost_advantage`. OS providers drive the reference price floor for the market.

### Belief Broadcast

When an OS provider publishes weights (`openness_level > 0`), other providers can analyze them to infer which capability dimensions the benchmark actually emphasizes. Each round, all providers receive a small nudge to their `inferred_benchmark_weights` toward the true `benchmark_true_weights`, proportional to the OS provider's openness level and deployment breadth:

```
belief_broadcast = openness_level × deployment_breadth × broadcast_rate
```

`deployment_breadth` = OS provider market share. This is a simplification — OS models are also widely used by researchers and academics outside the consumer market — but the belief broadcast toggle (`os_belief_broadcast`) already captures the outcome of that community activity without needing to model the mechanism explicitly.

The broadcast reveals what the benchmark measures — not what consumers need. Consumer need weights remain unobservable to all providers. The downstream effect is to accelerate Goodhart dynamics: providers learn benchmark weights faster → invest more efficiently in benchmark-adjacent dimensions → scores diverge from satisfaction more quickly. When `os_belief_broadcast=False`, this nudge is zero (ablation).

### Safety Erosion

OS providers release weights with some nominal `capability_vector["safety"]`. Once weights are public, downstream users can strip safety alignment. Consumer satisfaction and incident probability use `deployed_safety` rather than nominal safety:

```
safety_erosion_factor = openness_level × market_share × erosion_sensitivity
deployed_safety       = capability_vector["safety"] × (1 - safety_erosion_factor)
```

Naturally bounded: `openness_level ≤ 1`, `market_share ≤ 1`, so `safety_erosion_factor ≤ erosion_sensitivity`. No separate ceiling needed. Linear in market share — the most defensible form given no empirical data on the functional shape.

The provider cannot observe `safety_erosion_factor` directly — they observe higher-than-expected incident rates as a noisy signal. The provider controls nominal safety through investment in the safety lever; deployed safety is outside their control.

This mechanic stacks with the lower safety floor: OS providers invest less in safety to begin with, and whatever they invest is partially eroded in deployment. When `os_safety_erosion=False`, the safety dimension is used as-is (ablation).

---

## Evaluator / Benchmark Model

### Benchmark Structure

```python
@dataclass
class Benchmark:
    name: str
    categories: list[str]                                      # public
    category_dimension_weights: dict[str, dict[str, float]]   # hidden ground truth
    noise_sigma: float
    samples: int
    introduced_round: int
    retired_round: int | None
    parent_benchmark: str | None
```

Published per round: overall score + per-category scores. Hidden: how each category loads on the 6 capability dimensions.

Example (General Capability benchmark):
```
categories: ["general_reasoning", "factual_knowledge",
             "quantitative_reasoning", "natural_language_understanding"]

category_dimension_weights:
  general_reasoning:              {reasoning: 0.70, knowledge: 0.15, communication: 0.10, ...}
  factual_knowledge:              {knowledge: 0.65, reasoning: 0.20, communication: 0.10, ...}
  quantitative_reasoning:         {reasoning: 0.55, coding: 0.20, knowledge: 0.20, ...}
  natural_language_understanding: {communication: 0.60, reasoning: 0.25, knowledge: 0.10, ...}
```

### Benchmark Pool and Introduction Schedule

Consumer population average need_weights (anchor for alignment assessment):
```
{reasoning: 0.20, coding: 0.12, knowledge: 0.25, safety: 0.18, communication: 0.20, agentic: 0.05}
```

Starting gap: ecosystem over-indexed on reasoning/coding, under-indexed on safety. Goodhart pressure concentrated there from round 0.

| Round | Benchmark | reasoning | coding | knowledge | safety | communication | agentic | Real analog |
|---|---|---|---|---|---|---|---|---|
| 0 | General Capability | 0.39 | 0.06 | 0.30 | 0.02 | 0.22 | 0.01 | MMLU |
| 0 | Coding Evaluation | 0.30 | 0.53 | 0.05 | 0.00 | 0.04 | 0.08 | HumanEval/MBPP |
| 0 | Safety Evaluation | 0.06 | 0.00 | 0.10 | 0.58 | 0.26 | 0.00 | TruthfulQA/BBQ |
| 0 | Instruction Following | 0.20 | 0.03 | 0.08 | 0.03 | 0.65 | 0.01 | MT-Bench/IFEval |
| 6 | Scientific Reasoning | 0.57 | 0.02 | 0.32 | 0.00 | 0.08 | 0.01 | GPQA |
| 12 | Agentic Tasks | 0.25 | 0.19 | 0.01 | 0.00 | 0.07 | 0.48 | SWE-bench/BFCL |
| 18 | Hard Coding | 0.31 | 0.52 | 0.05 | 0.00 | 0.01 | 0.11 | LiveCodeBench |
| 18 | Long Context | 0.19 | 0.01 | 0.28 | 0.00 | 0.47 | 0.05 | RULER/HELMET |
| 24 | Domain Expert | 0.33 | 0.01 | 0.53 | 0.05 | 0.07 | 0.01 | MedQA/LegalBench |
| 28 | Agentic Safety | 0.11 | 0.00 | 0.01 | 0.63 | 0.13 | 0.12 | — |

**Toggleable misalignment extension (`benchmark_misalignment_enabled: bool = False`):** When enabled, benchmark weights are initialized via interpolation toward a misaligned vector concentrating on automatable/measurable dimensions (reasoning-heavy, safety-light). Default off — natural benchmark structures already create sufficient Goodhart pressure.

### Saturation (Implicit)

Saturation is not tracked as an explicit state. When providers cluster near the top of a benchmark and score deltas approach zero, the benchmark stops influencing actor decisions organically: providers gain little competitive signal, funders and regulators discount it, evaluators respond by introducing harder benchmarks. No mechanical retirement trigger is enforced.

### Evaluator Observation Model

The evaluator observes:
- Score deltas per benchmark per provider (derived from score history)
- Score spread per benchmark (derived from current round)
- Provider participation rates
- Media coverage of benchmark relevance or criticism
- **Internal validity estimate:** `Pearson_r(score_rank, market_share_rank)` — evaluator-internal only, never published to PublicState

Does NOT observe: capability vectors, consumer satisfaction, provider investment allocations.

### Evaluator Actions

| Action | When |
|---|---|
| **Introduce harder successor** | Deltas near zero on B for `saturation_window` rounds; same categories, harder items, more dimension-pure; parent may be retired |
| **Introduce fresh benchmark** | Coverage gap: dimension underweighted across active benchmarks; OR internal validity below threshold |
| **Retire benchmark** | Saturated; stop publishing scores |

### Dynamic Evaluator Toggle

```python
dynamic_evaluator: bool = False    # config parameter
saturation_window: int = 3
saturation_delta_threshold: float = 0.005
```

- `False` (default): fixed proactive schedule — benchmarks introduced at specified rounds regardless of simulation state. Reproducible and empirically anchored. No LLM reasoning used.
- `True`: signal-based introduction — evaluator draws from pool when saturation signals fire; fallback rounds ensure key benchmarks are introduced even if signals are weak. LLM reasoning active.

### Evaluator LLM Mode (`dynamic_evaluator=True` only)

In fixed schedule mode there are no decisions to make — LLM reasoning is irrelevant. In dynamic mode the evaluator makes genuine strategic decisions and LLM reasoning is enabled.

**Observation inputs to LLM prompt:** score deltas per benchmark per provider (last `saturation_window` rounds), score spread per benchmark, provider participation rates, media coverage of benchmark relevance/criticism, internal validity estimate (Pearson-r of score rank vs market share rank), which capability dimensions are currently underweighted across active benchmarks.

**LLM output JSON:**
```json
{
  "action": "introduce_successor | introduce_fresh | retire | none",
  "target_benchmark": "<benchmark_name if retire or successor>",
  "new_benchmark_focus": ["<dimension>", ...],
  "reasoning": "..."
}
```

**No apparatus vocabulary** in prompts — saturation, validity, and Goodhart framing are never surfaced. The evaluator is addressed as "the team responsible for maintaining the AI evaluation leaderboard."

**Consumer market uses no LLM mode.** The archetype system (`leaderboard_trust`, `switching_threshold`, `switching_cost`, `cost_sensitivity`) combined with the formula-based satisfaction model and `running_perceived_quality` EMA captures sufficient behavioral heterogeneity. Consumer decisions are routine and habitual rather than strategic, making LLM reasoning an unnecessary source of variance.

---

## Consumer Market

### Segments

Each segment = use-case profile × behavioral archetype. Archetypes modify observation behavior and switching friction only — not `need_weights`. Actual needs are the same regardless of archetype; the gap between how a segment selects providers (leaderboard-based) and what it actually needs (`need_weights`) is itself a dynamic of interest.

**Archetypes:**

| Archetype | `leaderboard_trust` | `switching_cost` | `switching_threshold` | `cost_sensitivity` |
|-----------|---------------------|------------------|-----------------------|--------------------|
| `leaderboard_follower` | 0.85 | 0.05 | 0.15 | 0.15 |
| `experience_driven` | 0.35 | 0.08 | 0.08 | 0.30 |
| `cautious` | 0.50 | 0.20 | 0.25 | 0.20 |
| `enterprise_cautious` | 0.25 | 0.35 | 0.50 | 0.10 |
| `enterprise_growth` | 0.45 | 0.25 | 0.30 | 0.15 |
| `enterprise_established` | 0.35 | 0.40 | 0.40 | 0.08 |

### Need Weights Per Profile

| Profile | reasoning | coding | knowledge | safety | communication | agentic |
|---|---|---|---|---|---|---|
| **Individual** | | | | | | |
| software_dev | 0.20 | 0.45 | 0.08 | 0.02 | 0.05 | 0.20 |
| content_writer | 0.15 | 0.03 | 0.25 | 0.05 | 0.50 | 0.02 |
| legal | 0.35 | 0.03 | 0.30 | 0.10 | 0.20 | 0.02 |
| healthcare | 0.20 | 0.03 | 0.25 | 0.40 | 0.10 | 0.02 |
| finance | 0.30 | 0.15 | 0.25 | 0.20 | 0.07 | 0.03 |
| educator | 0.25 | 0.03 | 0.25 | 0.10 | 0.35 | 0.02 |
| customer_service | 0.07 | 0.02 | 0.15 | 0.20 | 0.55 | 0.01 |
| researcher | 0.30 | 0.25 | 0.25 | 0.03 | 0.07 | 0.10 |
| creative | 0.15 | 0.03 | 0.20 | 0.05 | 0.55 | 0.02 |
| marketing | 0.20 | 0.03 | 0.25 | 0.05 | 0.45 | 0.02 |
| service_worker | 0.12 | 0.02 | 0.20 | 0.20 | 0.45 | 0.01 |
| **Organizational** | | | | | | |
| hospital_system | 0.18 | 0.03 | 0.25 | 0.40 | 0.12 | 0.02 |
| enterprise_finance | 0.28 | 0.12 | 0.22 | 0.25 | 0.10 | 0.03 |
| tech_startup | 0.20 | 0.30 | 0.12 | 0.05 | 0.08 | 0.25 |
| enterprise_legal | 0.32 | 0.04 | 0.28 | 0.12 | 0.22 | 0.02 |
| government_agency | 0.20 | 0.03 | 0.25 | 0.35 | 0.15 | 0.02 |

Population-weighted average ≈ `{reasoning: 0.22, coding: 0.09, knowledge: 0.23, safety: 0.17, communication: 0.26, agentic: 0.05}`. `agentic` intentionally low at simulation start (2023).

### Benchmark Relevance (Derived)

`benchmark_prefs` as a separate stored field is removed. Benchmark relevance is derived at runtime from the segment's own need weights dotted with each benchmark's publicly stated category loadings:

```
base_relevance[b]      = dot(need_weights, benchmark_public_category_weights[b])
effective_relevance[b] = base_relevance[b] × archetype_modifier[archetype][b]
effective_relevance    = normalize(effective_relevance)
```

`benchmark_public_category_weights[b]` is a public summary of what each benchmark claims to measure (stated category loadings — not the hidden true dimension weights).

Archetype modifiers:
- `leaderboard_follower`: upweights high-publicity benchmarks (General Capability, Coding Evaluation)
- `cautious`: upweights safety-focused benchmarks
- `early_adopter`: upweights newer benchmarks (Agentic Tasks, Long Context)

### Switching

Proportional sigmoid-based switching within each segment. Two triggers: dissatisfaction (expected > experienced quality) and opportunity (better alternative exists). Tenure bonus adds inertia. Opportunity threshold halved when the alternative is an OS provider.

---

## Incident System

Structurally preserved from prior architecture, with field updates for the capability vector model.

**Base rate:** 10% per provider per round. Multiplied by factors:

| Factor | Formula | Direction |
|--------|---------|-----------|
| Safety investment | `1 - (capability_vector["safety"] × 0.8)` | Higher safety → lower prob |
| Market share (exposure) | `0.5 + (market_share × 1.5)` | Larger market → higher prob |
| Capability level | `0.8 + (mean(capability_vector) × 0.4)` | Higher capability → higher stakes |
| Incident history escalation | `+0.04 per prior major/critical, cap +0.20` | Past harm → elevated future risk |
| Active sanction | `0.75×` while sanctioned | Regulatory oversight → reduced prob |

Capped at 0.40 per round.

**OS providers:** Use `deployed_safety` (after erosion) rather than `capability_vector["safety"]` when `os_safety_erosion=True`.

**Mandatory safety floor under compliance:** Providers under `commission_audit` or `impose_sanction` have `capability_vector["safety"]` clamped to a minimum floor (value to be recalibrated from old 0.15 to new capability scale).

**Severity distribution:**

| Severity | Probability |
|----------|-------------|
| Minor | 50% |
| Moderate | 31% |
| Major | 12% |
| Critical | 7% |

**Categories:** `healthcare_harm` (20%), `security_breach` (25%), `bias_discrimination` (20%), `safety_failure` (20%), `misinformation` (10%), `misuse` (5%).

**Ecosystem propagation:**
- **Media:** Headlines for moderate+; provider attention and sentiment penalties; risk signals
- **Consumers:** Incident penalty in satisfaction; `leaderboard_trust` erosion for follower segments
- **Regulator:** Risk belief updates; critical incidents may skip escalation levels
- **Funders:** Incident penalty in provider scoring

---

## Regulator

Renamed from Policymaker. Lever set redesigned; political capital dropped; threshold+cooldown+exogenous events model replaces old intervention logic.

### Observation Model

Regulator observes:
- Incident rate and severity (public)
- Market share distribution (public)
- Media pressure index (`narrative_state` from Media actor)
- Provider compliance status (prior commitments/mandates met?)
- Own lever cooldown status (private)

Does NOT observe: consumer satisfaction, `score_reliability`, capability vectors, benchmark validity.

### Intervention Levers

Graduated escalation: voluntary commitment → advisory → disclosure → audit → sanction. Major/critical incidents can skip levels. OS providers exempt from `impose_sanction`.

| Lever | Real-world analog | Cooldown | Mechanical effect |
|---|---|---|---|
| `request_voluntary_commitment` | White House/Seoul safety pledges | 3 rounds | Public safety pledge; media sentiment boost; no direct capability effect |
| `publish_advisory` | AISI evaluation summaries | 4 rounds | Media penalty to named providers; consumer trust effect |
| `mandate_safety_disclosure` | System card requirements | 6 rounds | Provider must publish capability claims; affects media and consumer observation |
| `commission_audit` | AISI pre-deployment evaluation | 8 rounds | Partial, noisy capability signal revealed to regulator; reputational effect; safety floor enforced |
| `impose_sanction` | EU AI Act fines, FTC action | 10 rounds | Market share/revenue penalty via `funding_multiplier`; requires prior non-compliance evidence |

**`audit_is_binding: bool`** (part of regulatory preset):
- `False` (US default): advisory only — no deployment gate
- `True` (EU default): can conditionally delay provider deployment if audit findings are severe

### Trigger Conditions

| Lever | Trigger |
|---|---|
| `request_voluntary_commitment` | incident_rate > low_threshold OR media_pressure > low_threshold |
| `publish_advisory` | incident_rate > low_threshold AND prior voluntary commitment unmet |
| `mandate_safety_disclosure` | incident_rate > medium_threshold OR major incident occurred |
| `commission_audit` | incident_rate > medium_threshold AND prior advisory issued |
| `impose_sanction` | incident_rate > high_threshold AND prior audit finding severe |

### Exogenous Events

| Preset | Round | Event | Effect |
|---|---|---|---|
| US | 24 | Administration change (Jan 2025) | Cancel active interventions; raise all thresholds; `audit_is_binding=False` enforced |
| EU | 14 | AI Act passed (Mar 2024) | Lower thresholds; enable binding audit enforcement |

### EU / US / Balanced Presets

| Parameter | EU | Balanced | US |
|---|---|---|---|
| Incident threshold (low) | 0.10 | 0.15 | 0.20 |
| Incident threshold (medium) | 0.25 | 0.35 | 0.45 |
| Incident threshold (high) | 0.45 | 0.55 | 0.65 |
| `audit_is_binding` | True (after round 14) | False | False |
| Posture | Proactive, precautionary | Moderate | Reactive, incident-driven |

Threshold values are config parameters — flagged for sensitivity analysis.

### Cross-Round Memory (PIMMUR)

`RegulatorPrivateState` holds `recent_reasoning` (last 3 entries stored; last 2 passed to prompts, each truncated to 120 characters). Allows maintaining consistent policy stances across rounds.

---

## Funder

### Types and Investment Logic

| Type | Pattern | Cooldown | Can allocate to OS? |
|------|---------|----------|---------------------|
| `vc` | Concentrated; skips OS providers (no equity model) | Per-funder: 3 rounds after any allocation | No |
| `corporate` | Multi-relationship; anchored to market position | Per-provider: 3 rounds after allocating to a specific provider | Yes |
| `gov` | Spread proportionally; safety/mission-oriented | None — continuous | Yes |
| `foundation` | Ecosystem health focus; safety/mission-oriented | None — continuous | Yes |

**Provider budget model:**

```
provider_rd_budget = base_revenue_income + sum(active_funder_allocations)

base_revenue_income = market_share × revenue_per_share × (1 - cost_advantage)
```

`revenue_per_share` is a fixed global scalar (calibration-time). `cost_advantage` discounts revenue for low-cost providers — OS providers with `cost_advantage = 0.9` generate almost no base revenue and depend on `rd_budget_floor`. `funding_multiplier` is replaced by this additive model.

**Funder allocation pool:** Each funder type has a fixed capital pool per round (set at sim initialization). Funders allocate from this pool across providers each round based on their scoring formula. Pool size is fixed — total AI investment is relatively inelastic; what changes is allocation pattern across providers.

**Scoring formulas (used to normalize allocation across providers):**

```
vc:          (market_share_growth × media_sentiment × (1 - incident_risk))
corporate:   (market_share × media_sentiment × (1 - incident_risk))
gov:         ((1 - incident_rate) × market_share_growth)
foundation:  ((1 - incident_rate) × market_share_growth)
```

`public_comms` (last 3 rounds per provider) are read directly and inform LLM-mode funder reasoning — no hardcoded weighting by announcement type. LLM funders reason freely from content and pattern of announcements alongside the scoring signals above.

**Performativity mechanism:** By treating benchmark scores and capability announcements as signals of provider quality, funders direct capital toward providers with strong public-facing performance. This makes benchmarks and `public_comms` partially constitutive of the market — capital flows to high-scorers and high-announcers, increasing their R&D capacity. The mechanism is amplifying, not corrective: empirically, major AI funders deepen commitments over time rather than withdrawing when performance signals weaken. The corrective dynamic in the ecosystem flows through consumers (market share erosion from satisfaction gaps) and revenue, not through funder withdrawal.

**`rd_budget_floor`:** OS providers receive an exogenous minimum budget regardless of funder allocations, representing state or large-tech-subsidized backing (e.g. Meta's corporate R&D, DeepSeek's hedge fund patron) that does not depend on market performance.

### Observation Model

Funder observes:
- Benchmark scores at face value (as capability claims — not validity-adjusted)
- Market share trends and score deltas
- Incident history per provider
- Media sentiment per provider
- `public_comms` last 3 rounds per provider (direct — not filtered through media)
- Other funders' investment behavior (herding signal)

Does NOT observe: consumer satisfaction, `score_reliability`, benchmark validity, provider investment allocations.

### Cross-Round Memory (PIMMUR)

`FunderPrivateState` holds `recent_reasoning` (last 3 entries stored; last 2 passed to prompts, each truncated to 120 characters). Allows maintaining investment theses across rounds.

---

## Media

Single outlet (TechPress). Publishes after evaluator scoring, before consumer/regulator/funder rounds.

### Observation Model

Media observes:
- Leaderboard (scores and ranks — public)
- Market share distribution
- Incidents (severity and named provider — public)
- Regulator interventions
- Provider press releases
- Org-archetype consumer switches
- Funder round announcements

Does NOT observe: capability vectors, consumer satisfaction, `score_reliability`, dimension weights, provider investment allocations.

### Coverage Triggers

| Trigger | Condition |
|---|---|
| Incident | Severity ≥ moderate — always fires; negative for named provider |
| SOTA announcement | Provider issues `rd` public_comms — fires with newsworthiness gate |
| Leaderboard change | Score leader changes this round — always fires; positive for new leader |
| Gaming scandal | Score leader diverges from market share leader for N rounds AND incident occurred |
| Saturation narrative | Median score across active benchmarks > saturation_threshold |
| Safety concern narrative | Cumulative incident rate > low_threshold for M consecutive rounds |
| Major partnership | Org-archetype consumer switches OR funder leads significant round (probabilistic) |

**Headline budget:** All moderate+ incidents are guaranteed slots. Other fired triggers enter a pool; up to `media_sample_size` (default 4) are sampled randomly per round. This models the attention economy — not all newsworthy events receive coverage.

### Provider Public Communications (`public_comms`)

Each round, each provider may issue at most one public communication. Type is sampled from `{rd, safety, product, none}` proportional to normalized weights:

```python
raw_weights = {
    "rd":      research_allocation + development_allocation,
    "safety":  safety_allocation  if safety_allocation > 0.20 else 0,
    "product": product_allocation if product_allocation > 0.15 else 0,
    "none":    0.30   # silence — always competes; providers don't post every round
}
weights = normalize(raw_weights)   # sum to 1
post_type = sample(weights)
```

Post types and content:

| Type | Real-world analog | Heuristic template |
|---|---|---|
| `rd` | Research publication or technical blog post | `"{name} publishes new research on {best_category}"` |
| `safety` | Safety card, red-teaming report, alignment post | `"{name} releases safety evaluation results"` |
| `product` | Enterprise partnership, integration announcement | `"{name} announces new enterprise deployment"` |
| `none` | No post this round | — |

In LLM mode, a lightweight call after planning generates a one-liner for the sampled type. In heuristic mode, templates are used.

Media independently covers leaderboard changes and score leaders — no score-delta boost needed in `public_comms` weights. Score-driven visibility is handled on the media side.

**Implementation note:** rename `press_releases` → `public_comms` consistently across all files (`media.py`, `funder.py`, `simulation.py`, `rounds.jsonl` schema, `ProviderPublicState`, `MediaCoverage`).

**Newsworthiness gate (for media coverage of `rd` posts only):**
```python
newsworthiness = score_delta / press_release_delta
p_coverage = min(1.0, newsworthiness)
```

### Outputs

```python
@dataclass
class MediaCoverage:
    headlines: list[str]
    sentiment: float                  # -1 to +1
    provider_attention: dict          # {provider: 0–1}
    narrative_state: str              # OPTIMISM / SKEPTICISM / CRISIS
    risk_signals: list[str]
    saturation_signal: bool
    public_comms: list[dict]          # [{provider, type, one_liner, round}]
```

### provider_attention

`provider_attention` is a **heuristic-mode construct**. In LLM mode, actors receive headlines as natural language and reason about provider salience implicitly — `provider_attention` is not injected into LLM prompts and has no effect on LLM-mode decisions.

In heuristic mode, it serves as a salience filter: it gates how much the media's `sentiment` signal bleeds through to a specific provider each round. A provider not in the news gets low attention → low media penalty regardless of overall sentiment.

**Computation (heuristic mode):** Reset each round. Baseline 0.1 for all providers. Bumped by events involving the provider, scaled by severity:

| Event | Attention |
|---|---|
| Critical incident | 1.0 |
| Major incident | 0.8 |
| Moderate incident | 0.6 |
| Sanction imposed | 0.8 |
| Audit commissioned | 0.6 |
| Advisory published | 0.5 |
| Leaderboard leader change (new leader) | 0.8 |
| Leaderboard leader change (displaced) | 0.5 |
| Provider appears in sampled headlines (other) | 0.4 |

Take the max across all applicable events; clip to 1.0. No memory across rounds — attention is purely this round's news.

### Narrative State

```
OPTIMISM  → SKEPTICISM : cumulative incidents > low_threshold OR gaming scandal fires
SKEPTICISM → CRISIS    : cumulative incidents > high_threshold OR multiple scandals
CRISIS    → SKEPTICISM : no incidents for M rounds AND no scandal
SKEPTICISM → OPTIMISM  : no incidents for N rounds
```

`narrative_state` is the primary input to the regulator's `media_pressure` index. Funder sentiment is modulated by `sentiment` and `provider_attention`. Consumer `media_penalty` uses `provider_attention` weighted by `sentiment`.

All internal trigger labels (`gaming_scandal`, `saturation_narrative`, `CRISIS`, etc.) are simulation-internal only — never passed verbatim to any LLM prompt. Translated to natural language before injection.

---

## Simulation Round Order

```
1. Providers plan portfolios → capability updates (rd_budget from base_revenue + active_funder_allocations; sanction multiplier if under sanction)
   → public_comms sampled and issued
2. Evaluator scores all providers on all active benchmarks → saturation detection
   → benchmark introduction/retirement (fixed schedule or signal-based)
3. Providers observe scores and reflect → update benchmark beliefs
4. Incidents generated (with safety floor, sanction multiplier)
5. Media observes and publishes (including public_comms coverage)
6. Consumers observe leaderboard + media → compute satisfaction → switching
7. Regulator observes → update risk beliefs → intervene if triggered
8. Funders observe leaderboard + media + public_comms → update beliefs → allocate capital (respecting cooldowns)
```

---

## Out of Scope (Initial Implementation)

- **Startup entry dynamics** — no `startup_entry_probability`, `startup_entry_cap`, or mid-simulation provider spawning
- **Barrier-to-Entry (BTE) index** — no composite market-contestability metric
- **Market concentration review** — antitrust lever dropped from regulator interventions
- **Sandbagging** — providers strategically underperforming on audits when audit context is detected
- **Dynamic need_weights** — `agentic` and related dimensions growing over simulation time as adoption spreads
- **Whistleblower/counter-narrative events** — researcher departure events triggering negative coverage
- **Funder herding mechanic** — explicit modeled herd behavior dropped; herding emerges naturally from funders observing each other's allocations and updating `believed_provider_quality` accordingly

---

## Calibration Notes

### Open Source Capability Jump Calibration

The OS provider has two update modes: slow continuous R&D gain (every round) and episodic step-change capability jumps (stochastic, representing a new frontier OS release entering the market). Jump magnitude and frequency should be calibrated empirically: examine OS model performance trends on tracked benchmarks (e.g., Epoch AI's Notable AI Models dataset / capabilities index, Hugging Face Open LLM Leaderboard history, HELM benchmark trajectories). Look for seemingly sudden score jumps — corresponding to major releases like LLaMA 2 → 3.1 → DeepSeek R1 — and study: (a) how large the capability jump was relative to the prior trend, (b) how frequently jumps occur, (c) whether jump magnitude correlates with inter-release interval. These empirical distributions then parameterize `jump_magnitude` and `jump_probability`.

### Ecosystem-Level Metrics (Deferred)

Metrics like `score_reliability` (Pearson-r of scores vs. satisfaction) are detectable only through triangulation across multiple actors' partial views — no single actor has the full picture. How these are computed, what is logged vs. published, and how actors respond to their respective fragments requires a dedicated design discussion. Deferred for now.

### Provider Satisfaction Signal and PIMMUR

`satisfaction_signal` is surfaced in LLM mode as raw data — no prescribed inference. A provider may respond to a rising score / falling satisfaction gap in multiple ways; that heterogeneity is intentional. In heuristic mode, `satisfaction_signal` does not directly wire into portfolio allocation. Nuanced satisfaction-responsive reasoning is an LLM-mode capability.

---

## Open Threads

1. ~~**`safety_bonus` in satisfaction formula**~~ — **Resolved.** Removed. Safety is fully captured by `need_weights["safety"]` in the dot product. Satisfaction formula updated; expected quality definition added; incident penalty quadratic in market share; media penalty archetype-modulated via `leaderboard_trust`.

2. ~~**Gaming gap factor in incident probability**~~ — **Resolved.** Removed. No clean equivalent exists in the new architecture; remaining factors (safety investment, capability level, market share, incident history) are sufficient. `capability level` already captures low overall capability directly.

3. ~~**`deployment_breadth` for OS mechanics**~~ — **Resolved.** Use OS market share directly. `ecosystem_influence` as a separate quantity dropped — the broadcast toggle captures the outcome without modeling the mechanism.

4. ~~**Safety erosion formula**~~ — **Resolved.** Linear: `safety_erosion_factor = openness_level × market_share × erosion_sensitivity`. Naturally bounded; no ceiling needed. `erosion_sensitivity` hardcoded at 0.50 (see Thread 8).

5. ~~**`product` lever mechanics**~~ — **Resolved.** Accumulates `market_presence` → `cost_advantage` → `cost_bonus`. Switching cost stickiness and enterprise adoption rate effects flagged as possible extensions, deferred.

6. ~~**Initial `benchmark_adjacency[dim]` per provider**~~ — **Superseded.** `benchmark_adjacency[dim]` removed from design. Replaced by `focus_level[b]` (per-benchmark running scalar). Initial `focus_level[b]` baselines are provider-calibrated per the 2023 empirical landscape — see Thread 9 for calibration protocol and Default Provider Profiles for qualitative anchors.

7. ~~**Formal empirical calibration (pre-implementation)**~~ — moved to post-implementation calibration thread below.

8. **Parameter defaults (resolved):**

   | Parameter | Default | Rationale |
   |---|---|---|
   | `learning_rate` (belief update) | 0.15 | ~10-round convergence on benchmark weights |
   | `broadcast_rate` | 0.30 (hardcoded constant) | Noticeable but not dominant nudge; ablation via toggle |
   | `erosion_sensitivity` | 0.50 (hardcoded constant) | ~5–15% erosion at realistic OS market shares; ablation via toggle |
   | `silence_weight` (`public_comms`) | 0.30 (hardcoded constant) | Providers don't post every round |
   | `δ` (ordinal step size) | 0.06–0.09 (Thread 9 calibration) | Additive step applied to portfolio, focus_level, and benchmark_orientation on each "more"/"less" signal; same value for all three; clip and renormalize after applying |
   | `benchmark_orientation` bounds | (0.05, 0.95) (hard bounds) | Prevents providers from fully ignoring either consumer signal or benchmark focus regardless of accumulated ordinal shifts |

   `benchmark_weight_confidence` dropped — redundant with `learning_rate` damping.

9. **Post-implementation calibration** — all items requiring simulation output before values can be set:

   - **Mandatory safety floor**: working estimate 0.35; confirm against safety trajectories in early runs
   - **Empirical calibration**: initial capability vectors against `external-validation/` data
   - **`focus_level[b]` baselines**: 24 values at round 0 (6 providers × 4 benchmarks); anchored to 2023 empirical landscape; grows to 6 × 10 = 60 values by round 28 as new benchmarks enter. Qualitative anchors documented in Default Provider Profiles above; numeric values require calibration against external benchmark focus data
   - **R&D gain scaling**: absolute magnitude of `rd × target[dim]` per round (replaces old `R_efficiency`); confirm against capability growth trajectories in early runs
   - **`σ_base`**: noise scale for `satisfaction_signal`; calibrate so signal is informative but not precise at realistic market shares
   - **`benchmark_orientation`**: per-provider initial value (expected range 0.7–0.9); calibrate against sensitivity of Goodhart dynamics to consumer feedback strength; bounds hard-capped at (0.05, 0.95)
   - **Media parameters**: narrative transition thresholds (N, M rounds), sentiment weights per trigger type, `saturation_threshold`
   - **Funder parameters**: `funder_pool` size per type, `revenue_per_share` scalar, scoring formula weights
   - **Regulator parameters**: exact threshold values per preset (EU/Balanced/US)
   - **Consumer state**: `running_perceived_quality` initialization value per segment per provider

10. ~~**Emergency investigation score discount**~~ — **Resolved.** Removed. Gaming gap no longer exists; reputational and regulatory effects of major incidents are already captured by incident_penalty × (1 + market_share²), media_penalty × leaderboard_trust, and the commission_audit/impose_sanction levers. Score discount was double-counting and has no real-world analog (published benchmark scores don't get discounted during investigations).

11. ~~**Attribute audit — legacy fields**~~ — **Resolved.**
- `funding_multiplier`: replaced by additive budget model (`base_revenue_income + funder_allocations`). `rd_budget_floor` retained for OS providers.
- `ecosystem_influence`: dropped (Thread 3 resolved — use OS market share directly).
- `believed_provider_gaming`: dropped from new design entirely.
- `exploitability`, `benchmark_params.validity`: not present in new design.
- `consumer_satisfaction` direct access in funder: not present in new design (visibility enforced structurally).
- `press_releases`: renamed to `public_comms` throughout; semantics broadened to cover `rd`, `safety`, `product` post types.
- `funding_multiplier` as per-round continuous scalar: replaced by funder type (`vc`, `corporate`, `gov`, `foundation`) with per-funder or per-provider cooldowns and additive pool allocation.
- `research` and `development` levers: consolidated into single `rd` lever. Targeting behavior previously handled by `dimension_allocation` and `benchmark_adjacency` is now handled by `focus_level[b]` and `inferred_benchmark_weights[b]`.
- `dimension_allocation[dim]`: removed. Development budget direction now determined by `focus_level[b]` × `inferred_benchmark_weights[b][dim]`.
- `benchmark_adjacency[dim]`: removed. Replaced by `focus_level[b]` — per-benchmark scalar updated via ordinal LLM output each round.
- `satisfaction_signal` scalar: replaced by 6-dim vector of market-share-weighted consumer need weights, with noise proportional to `1/sqrt(market_share)`.
- `believed_benchmark_weight[dim]` (single aggregated vector): replaced by per-benchmark `inferred_benchmark_weights[b][dim]`, heuristic-updated from score prediction errors per benchmark.
- `provider_efficiency_multiplier`: dropped. Differentiation comes from R&D budget (via market share and funder allocations), initial capability vectors, and strategic choices. Global scaling adds compounding hard-coded advantage that undermines strategic agency.
- `S_efficiency`: dropped. The two-pathway structure (rd toward safety benchmarks + safety lever directly) already provides the intended distinction between benchmark-optimized and genuine safety investment. Relative efficiency between them is absorbed into Thread 9 calibration of absolute gain magnitudes.

---

## What Is Preserved

- Three-tier visibility architecture (PublicState / PrivateState / GroundTruth)
- Incident mechanics (probability model, severity distribution, ecosystem propagation) — with field updates for capability vector
- Consumer switching mechanics (sigmoid, tenure bonus, opportunity threshold)
- PIMMUR cross-round memory (`recent_insights` / `recent_reasoning`) for all actors
- Regulatory presets (EU / Balanced / US) — structure preserved, lever set redesigned
- Experiment infrastructure (DirectoryLogger, `hf_data` layout, `run_experiment.py`)
- Cost advantage mechanic for all providers
- Funder types (`vc`, `corporate`, `gov`, `foundation`) and portfolio diversification logic
