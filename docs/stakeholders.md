# Stakeholder Architecture: No Explicit Gaming

> **Status: Pre-implementation plan. Last updated: 2026-03-17.**
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

| Actor | File | Role |
|-------|------|------|
| Model Provider | `actors/model_provider.py` | Develops models, allocates R&D portfolio |
| Evaluator | `actors/evaluator.py` | Operates benchmarks; introduces new benchmarks as ecosystem evolves |
| Consumer Market | `actors/consumer.py` | Segments (archetype × use-case); proportional switching |
| Regulator | `actors/regulator.py` | Graduated interventions; EU/US/balanced presets |
| Funder | `actors/funder.py` | VC, gov, foundation types; media-aware capital allocation |
| Media | `actors/media.py` | TechPress outlet; coverage influences all downstream actors |
| Incident System | `incidents.py` | Probabilistic AI safety incidents; ecosystem propagation |

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

Providers allocate 100% of their training budget across four levers each round:

| Lever | Competitive axis | Mechanical effect | Benchmark-specializable? |
|---|---|---|---|
| `research` | Capability (broad) | Uniform gain across all dimensions; high variance; breakthrough-eligible | No — broad by definition |
| `development` | Capability (targeted) | Gain toward dimensions chosen by provider; rate modulated by `benchmark_adjacency[dim]` | Yes — via `benchmark_adjacency[dim]` |
| `safety` | Safety capability | Improves `capability_vector["safety"]` at fixed efficiency | No — always builds true safety capability |
| `product` | Market adoption | Accumulates `product_stock`; maps to `cost_advantage` → flows through to `cost_bonus` in satisfaction formula | N/A — does not affect capability vectors. Possible extensions: switching cost stickiness (per-provider modifier on `switching_cost`); enterprise segment adoption rate — both deferred. |

**Gaming mechanism:** When `benchmark_adjacency[dim]` is high, development gain concentrates on dimensions the provider believes the benchmark emphasizes. If believed weights are accurate and benchmark weights diverge from consumer need weights, scores rise faster than consumer satisfaction. The score-satisfaction gap emerges without any explicit gaming term.

### Development Sub-Structure

The Development lever has two internal vectors in `ProviderPrivateState`:

```
dimension_allocation[dim]  — how Development budget is split across dimensions (sums to 1)
benchmark_adjacency[dim]        — per-dimension data strategy (0 = diverse, 1 = benchmark-adjacent)
```

These are orthogonal choices. A provider can invest heavily in coding (`dimension_allocation["coding"]` high) with diverse data (`benchmark_adjacency["coding"]` low), or lightly invest but use narrow benchmark-adjacent data. `dimension_allocation` is updated first (where to compete), `benchmark_adjacency` second (how to source data).

### Capability Update Rule

Each round, per-dimension:

```python
gain[dim] = (
    research    × R_efficiency / n_dims
  + development × dimension_allocation[dim]
               × ((1 - benchmark_adjacency[dim]) × deficit_weight[dim]
                 + benchmark_adjacency[dim]      × believed_benchmark_weight[dim])
  + safety      × S_efficiency × (1 if dim == "safety" else 0)
) × provider_efficiency_multiplier

capability_vector[dim] = min(1.0, capability_vector[dim] + gain[dim])
```

Where:
- `deficit_weight[dim] = (1 - capability_vector[dim]) / sum(1 - capability_vector[d] for d in DIMENSIONS)`
- `R_efficiency ≈ 1.5 / n_dims`
- `S_efficiency ≈ 2.0`

### Provider Belief Model

Providers hold beliefs about the benchmark's hidden dimension weights, updated each round from score prediction errors.

**ProviderPrivateState additions:**

```python
believed_benchmark_weights: dict[str, float]      # initially uniform across DIMENSIONS
dimension_allocation: dict[str, float]             # Development budget split (sums to 1)
benchmark_adjacency: dict[str, float]                   # per-dimension data strategy (0–1)
satisfaction_signal: float                   # noisy private estimate from usage data
```

**Belief update (heuristic mode):**

Aggregated across all active benchmarks, weighted by score spread (tighter clustering = less signal):

```
for each active benchmark b:
    predicted_score[b] = dot(capability_vector, believed_benchmark_weights[b])
    error[b]           = observed_score[b] - predicted_score[b]
    weight[b]          = score_spread[b] / sum(score_spread values)

for dim in DIMENSIONS:
    believed_benchmark_weights[dim] += learning_rate × weighted_sum(error[b] × capability_vector[dim])

believed_benchmark_weights = normalize(clip_non_negative(believed_benchmark_weights))
```

`learning_rate` (default 0.15) is a config parameter. `benchmark_weight_confidence` is dropped — `learning_rate` already provides damping at the belief update level; confidence was double-damping a signal that's already slow-moving. In LLM mode, providers reason about uncertainty themselves from context.

**Belief update (LLM mode):**

Belief update is part of the reflection step. The LLM reasons sequentially: (1) what did my investments produce? (2) what does that reveal about what the benchmark measures? (3) how should I adjust data sourcing and dimension focus? All three are one coherent thought.

Prompt inputs: per-category scores this round, score delta vs. last round, competitor rank per benchmark (rank only — not raw scores), prior `dimension_allocation`, prior `benchmark_adjacency`, current `believed_benchmark_weights`, last round's `recent_reasoning`. No apparatus vocabulary (`gaming`, `exploitability`, `benchmark_weight_confidence`) appears in any prompt. Providers are addressed as "the strategy team at {name}."

LLM output JSON:
```json
{
  "benchmark_beliefs": {
    "<benchmark_name>": {
      "weights": {"reasoning": 0.35, "knowledge": 0.25, "communication": 0.20,
                  "coding": 0.10, "safety": 0.05, "agentic": 0.05},
      "reasoning": "..."
    }
  },
  "dimension_allocation": {"reasoning": 0.28, "coding": 0.22, ...},
  "benchmark_adjacency": {"reasoning": 0.3, "coding": 0.6, ...},
  "reasoning": "Free-text summary — injected as recent_reasoning next round"
}
```


**`satisfaction_signal`:** Providers have a noisy private signal of their own consumer satisfaction, derived from usage data, ratings, and feedback. In LLM mode, it is surfaced as raw data in the observation/reflection prompt — no prescribed inference is given. A provider may respond to a rising score / falling satisfaction gap in multiple ways (reduce benchmark_adjacency, double down on scores, attribute the gap to incidents or pricing, etc.). That heterogeneity is intentional and consistent with PIMMUR. In heuristic mode, `satisfaction_signal` is available but does not directly wire into portfolio allocation.

### Dimension Allocation Evolution

**Heuristic evolution rule:**

```
for dim in DIMENSIONS:
    gap[dim]              = max(0, leader_category_score_on[dim] - own_category_score_on[dim])
    benchmark_signal[dim] = believed_benchmark_weights[dim]
    dr_discount[dim]      = 1 - capability_vector[dim]

    signal[dim] = α × gap[dim] + β × benchmark_signal[dim] + γ × dr_discount[dim]

target_allocation = normalize(signal)
dimension_allocation[dim] = (1 - λ) × dimension_allocation[dim] + λ × target_allocation[dim]
dimension_allocation = clip_normalize(dimension_allocation, min=0.05, max=0.60)
```

| Param | Role | Value | Rationale |
|---|---|---|---|
| α | Competitive gap weight | 0.4 | Catching up to leader is primary driver |
| β | Benchmark signal weight | 0.4 | Benchmark-directed investment is real |
| γ | Diminishing returns weight | 0.2 | Prevents over-concentration |
| λ | Learning rate | 0.15 | ~15% move toward target per round |

The gap on a dimension is approximated by comparing category scores on benchmarks that load heavily on that dimension, using `believed_benchmark_weights` — keeping inference uncertain and making benchmark belief accuracy competitively valuable.

**LLM mode:** Provider sees current capability per benchmark category, competitor category scores, `believed_benchmark_weights`, and market share. Outputs updated `dimension_allocation` as JSON.

### Default Provider Profiles

**Lever allocations (2023 Q1 baseline):**

| Provider | Research | Development | Safety | Product |
|---|---|---|---|---|
| Apex AI | 35% | 25% | 30% | 10% |
| Orion Labs | 25% | 30% | 15% | 30% |
| Genesis Systems | 45% | 25% | 15% | 15% |
| Mirage AI | 35% | 45% | 10% | 10% |
| Spark AI | 10% | 55% | 10% | 25% |
| OpenCore | 25% | 50% | 10% | 15% |

**Initial `dimension_allocation` (2023 baseline — working estimates pending empirical calibration):**

| Provider | reasoning | coding | knowledge | safety | communication | agentic |
|---|---|---|---|---|---|---|
| Apex AI | 0.25 | 0.15 | 0.10 | 0.25 | 0.20 | 0.05 |
| Orion Labs | 0.30 | 0.25 | 0.10 | 0.10 | 0.20 | 0.05 |
| Genesis Systems | 0.25 | 0.15 | 0.30 | 0.10 | 0.15 | 0.05 |
| Mirage AI | 0.25 | 0.35 | 0.15 | 0.05 | 0.15 | 0.05 |
| Spark AI | 0.15 | 0.40 | 0.05 | 0.05 | 0.15 | 0.20 |
| OpenCore | 0.20 | 0.45 | 0.15 | 0.05 | 0.10 | 0.05 |

`agentic` intentionally low (0.05) for all frontier labs in 2023. Spark AI higher (0.20) — benchmark-focused startups were building agent scaffolding. OpenCore heavily coding-focused in 2023; reasoning-first identity came later with R1 (2025).

**Initial `benchmark_adjacency[dim]` (2023 baseline):**

| Provider | reasoning | coding | knowledge | safety | communication | agentic |
|---|---|---|---|---|---|---|
| Apex AI | 0.20 | 0.20 | 0.15 | 0.10 | 0.20 | 0.05 |
| Orion Labs | 0.30 | 0.35 | 0.20 | 0.10 | 0.20 | 0.15 |
| Genesis Systems | 0.25 | 0.20 | 0.25 | 0.10 | 0.20 | 0.10 |
| Mirage AI | 0.35 | 0.45 | 0.25 | 0.05 | 0.20 | 0.20 |
| Spark AI | 0.30 | 0.55 | 0.20 | 0.05 | 0.15 | 0.35 |
| OpenCore | 0.20 | 0.40 | 0.20 | 0.05 | 0.10 | 0.15 |

Values are per-dimension [0,1] scalars — not a budget (do not sum to 1). 0 = diverse data, 1 = benchmark-adjacent data. These are starting points; `benchmark_adjacency[dim]` evolves each round via the Plan step. All providers have meaningful benchmark orientation in 2023 — the differentiation is in degree and which dimensions. Safety benchmark_adjacency is low across the board (0.05–0.10) — no provider was explicitly targeting safety benchmarks over genuine safety investment in 2023. Spark AI's coding benchmark_adjacency (0.55) is the highest — startups in 2023 were explicitly HumanEval-focused.

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

1. **Observe** — per-category scores (own + competitor ranks), market share, incidents this round, media coverage, regulator interventions, `satisfaction_signal` signal
2. **Reflect** — update `believed_benchmark_weights` and `benchmark_weight_confidence`; append reasoning to `recent_insights`
3. **Plan** — update `dimension_allocation` and `benchmark_adjacency`; allocate four levers; check press release threshold
4. **Execute** — capability updates via R&D investments

**Heuristic incident pressure:** Safety incidents accumulate `_incident_safety_pressure` (minor: 0.03, moderate: 0.10, major: 0.20, critical: 0.30, cap: 0.40), shifting resources from `development` toward `safety`. Decays 40%/round (~4-round effect).

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

When an OS provider publishes weights (`openness_level > 0`), other providers can analyze them to infer which capability dimensions the benchmark actually emphasizes. Each round, all providers receive a small nudge to their `believed_benchmark_weights` toward the true `benchmark_true_weights`, proportional to the OS provider's openness level and deployment breadth:

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

- `False` (default): fixed proactive schedule — benchmarks introduced at specified rounds regardless of simulation state. Reproducible and empirically anchored.
- `True`: signal-based introduction — evaluator draws from pool when saturation signals fire; fallback rounds ensure key benchmarks are introduced even if signals are weak.

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

**Actor realism fixes (implementation):** Remove `consumer_satisfaction` direct access from `funder.py` (~line 174); remove `believed_provider_gaming` from `FunderPrivateState` and all dependent logic.

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

5. ~~**`product` lever mechanics**~~ — **Resolved.** Accumulates `product_stock` → `cost_advantage` → `cost_bonus`. Switching cost stickiness and enterprise adoption rate effects flagged as possible extensions, deferred.

6. ~~**Initial `benchmark_adjacency[dim]` per provider**~~ — **Resolved.** Values set for all providers. Range compressed (0.05–0.55); all providers meaningfully benchmark-oriented at 2023 baseline reflecting the real landscape. Evolves endogenously each round.

7. ~~**Formal empirical calibration (pre-implementation)**~~ — moved to post-implementation calibration thread below.

8. **Pre-implementation parameter defaults (resolved):**

   | Parameter | Default | Rationale |
   |---|---|---|
   | `learning_rate` (belief update) | 0.15 | ~10-round convergence on benchmark weights |
   | `broadcast_rate` | 0.30 (hardcoded constant) | Noticeable but not dominant nudge; ablation via toggle |
   | `erosion_sensitivity` | 0.50 (hardcoded constant) | ~5–15% erosion at realistic OS market shares; ablation via toggle |
   | `silence_weight` (`public_comms`) | 0.30 (hardcoded constant) | Providers don't post every round |

   `benchmark_weight_confidence` dropped — redundant with `learning_rate` damping.

9. **Post-implementation calibration** — all items requiring simulation output before values can be set:

   - **Mandatory safety floor**: working estimate 0.35; confirm against safety trajectories in early runs
   - **Empirical calibration**: initial capability vectors and `dimension_allocation` against `external-validation/` data
   - **Media parameters**: narrative transition thresholds (N, M rounds), sentiment weights per trigger type, `saturation_threshold`
   - **Funder parameters**: `funder_pool` size per type, `revenue_per_share` scalar, scoring formula weights
   - **Regulator parameters**: exact threshold values per preset (EU/Balanced/US)
   - **Consumer state**: `running_perceived_quality` initialization value per segment per provider

10. ~~**Emergency investigation score discount**~~ — **Resolved.** Removed. Gaming gap no longer exists; reputational and regulatory effects of major incidents are already captured by incident_penalty × (1 + market_share²), media_penalty × leaderboard_trust, and the commission_audit/impose_sanction levers. Score discount was double-counting and has no real-world analog (published benchmark scores don't get discounted during investigations).

11. ~~**Attribute audit — legacy fields**~~ — **Resolved.**
- `funding_multiplier`: replaced by additive budget model (`base_revenue_income + funder_allocations`). `rd_budget_floor` retained for OS providers.
- `ecosystem_influence`: dropped (Thread 3 resolved — use OS market share directly).
- `believed_provider_gaming`: remove from `FunderPrivateState` and all dependent logic (implementation fix).
- `exploitability`, `benchmark_params.validity`: remove from `media.py` observation model (ground truth leaks — implementation fix).
- `consumer_satisfaction` direct access in `funder.py`: remove (visibility violation — implementation fix).
- `press_releases`: renamed to `public_comms` throughout; semantics broadened to cover `rd`, `safety`, `product` post types.
- `funding_multiplier` as per-round continuous scalar: replaced by funder type (`vc`, `corporate`, `gov`, `foundation`) with per-funder or per-provider cooldowns and additive pool allocation.

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
