# Stakeholder Architecture: No Explicit Gaming

> **Architecture reference.** Sections below describe the simulation's actors, state representations, and mechanics as implemented.
> Gaming emerges from provider investment decisions and benchmark-need weight mismatch — not from an explicit gaming lever.

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
| `src/simulation.py` | Core sim loop, `SimulationConfig`, `EvalEcosystemSimulation`, regulatory presets |
| `src/capability_dimensions.py` | `DIMENSIONS` constant, `dot()`, `normalize()`, `deficit_weights()` utilities |
| `src/visibility.py` | State classes: PublicState, PrivateState, GroundTruth, AIIncident |
| `src/actors/model_provider.py` | ModelProvider: plan/observe/reflect/execute cycle |
| `src/actors/evaluator.py` | Evaluator, Benchmark, benchmark pool, saturation detection, dynamic introduction |
| `src/actors/consumer.py` | ConsumerMarket with archetype × use-case segments |
| `src/actors/regulator.py` | Regulator with graduated interventions, calibrated EU/US presets |
| `src/actors/funder.py` | Funder (VC, gov, foundation types), media-aware |
| `src/actors/media.py` | Media actor (TechPress) — coverage influences downstream actors |
| `src/incidents.py` | `IncidentGenerator` — probabilistic AI safety incident generation |
| `src/llm.py` | Multi-provider LLM integration (OpenAI, Anthropic, Ollama, Gemini) |
| `src/plotting.py` | Per-experiment visualization; presentation plots (pres_slide1/2) are default end-of-run output |
| `scripts/plot_single_run.py` | Presentation-style single-run plots (incident+intervention with escalation colors) |
| `scripts/plot_batch.py` | Batch presentation plots (fig1-fig5 across presets) |
| `docs/aggregation_pipeline.md` | Reasoning-grounded trajectory analysis design doc |
| `src/experiment_logger.py` | `ExperimentLogger` + `DirectoryLogger` |
| `src/game_log.py` | Natural language game log generator |
| `scripts/run_experiment.py` | Editable experiment config — edit and run |
| `scripts/rerun_experiment.py` | Re-runs a past experiment from saved config |
| `scripts/plot_experiment.py` | Single-run comparison + aggregate cross-condition plots |

---

## Actors Overview

| Actor | File | LLM mode | Role |
|-------|------|----------|------|
| Model Provider | `actors/model_provider.py` | Yes | Develops models, allocates R&D portfolio |
| Evaluator | `actors/evaluator.py` | Yes — `dynamic` mode only | Operates benchmarks; creates/retires benchmarks; 3 modes (fixed_sequence / randomized_pool / dynamic). Dynamic mode is **time-triggered** every `benchmark_introduction_interval` rounds (default 4); no signal-based saturation/validity triggers. Heuristic: gap-based pool selection. LLM: judgment from pool. |
| Consumer Market | `actors/consumer.py` | No — formula-based only | Segments (archetype × use-case); proportional switching |
| Regulator | `actors/regulator.py` | Yes | Graduated interventions; EU/US/balanced presets |
| Funder | `actors/funder.py` | Yes | VC, gov, foundation types; media-aware capital allocation |
| Media | `actors/media.py` | No — fully algorithmic | TechPress outlet; template headlines + rule-based sentiment / attention / narrative-state; coverage influences all downstream actors |
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

Gaming is not pre-specified. Providers allocate a training budget across three levers (R&D, Safety, Product) and choose which benchmarks to prioritize in their R&D pipeline. Goodhart dynamics arise when benchmark dimension weights diverge from consumer need weights and providers discover — through score signals — that specializing toward benchmark-measured dimensions raises scores faster than it raises satisfaction. The score-satisfaction gap is discovered by the simulation, not imposed by it.

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

Dimensions are investment targets, not statistically orthogonal factors. The correlation between dimensions observed empirically reflects the dominance of Research (g-like) investment. Dimensions cover the current frontier of separable investment: `reasoning` (subsumes math), `communication` (subsumes language), `knowledge` (subsumes domain), and `agentic`.

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
    holdout_fraction: float = 0.0          # fraction of score from holdout set (0=public, 1=fully opaque)
    holdout_category_dimension_weights: Optional[dict] = None  # holdout weights (same domain, less extreme)
```

`holdout_fraction > 0` activates the private benchmark blending formula (see Score Formula below). Holdout weights are domain-consistent — same capability space as public weights, dominant dimension reduced ~13-15pp to model a harder/different slice of the same test distribution. 10 of 22 pool benchmarks carry holdout weights.

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

**Private benchmark scoring (holdout-only, h > 0):**
```
published_score = Normal(dot(capability_vector, holdout_weights), (noise_sigma / sqrt(samples * h))²)
```

Published every K rounds (K = `evaluation_lag` = 3). Between publications, providers see stale scores. The market receives only the holdout-derived signal for any benchmark with a holdout.

**h controls observation noise, not blending.** `h` is the fraction of benchmark items in the private holdout; the holdout-only score is computed on `samples × h` items, so smaller h produces a noisier statistic. For `partial` (h=0.3) vs `private` (h=1.0): partial has ~1.8× the score noise. Practice-signal mechanisms on the publicly-observable `(1-h)` fraction are NOT modelled; providers have no direct observation of the public portion beyond their prior on `public_weights` (see Provider Belief Model below).

**Three benchmark types + one ablation type:**

| Type | h | cosine(public, holdout) | Real-world analog |
|---|---|---|---|
| `public` | 0 | — | MMLU, HumanEval, GPQA |
| `partial` | 0.3 | 0.95 | SEAL-style, contamination-magnitude asymmetry (Singh et al. 2024 retro-holdout anchor) |
| `private` | 1.0 | 0.85 | FrontierMath-style, adversarially constructed holdout |
| `iid_holdout` | 1.0 | 1.00 | Ablation only: isolates reporting lag from weight asymmetry (holdout weights = public weights) |

Cosine values anchored empirically: 0.85 matches Epoch within-family Pearson correlation (e.g., FrontierMath T1-3 vs T4: 0.85) and MMLU-vs-MMLU-Pro / GSM8K-vs-GSM-Plus literature. 0.95 anchors to Singh et al. (2024) 8–16pp inflation from retro-holdout contamination, which maps to effective cosine ~0.95–0.97 at typical capability magnitudes. Cosine-<1 is a **composite proxy** for contamination, training-on-the-test-task (Dominguez-Olmedo et al. 2024), and distributional adversarialness — the sim's single-knob abstraction of multiple literature mechanisms.

**Evaluation cadence (`evaluation_lag`, K):** K = 3 rounds (global, all providers × all private benchmarks publish simultaneously). Empirical anchor: median-of-medians K_advance = 3.0 months across 24 Epoch AI benchmarks × 8 frontier labs (`external-validation/scripts/analyze_k_cadence.py`, derived tables in `external-validation/data/processed/`). Per-provider asynchronous release variants (Fix-C / Poisson/Bernoulli) are out of scope.

**Six ablation conditions** (pool attribute assignments over the 13-benchmark static set — 4 active at round 0 + 9 introduced at intervals of 4 rounds through round 36):**

| Condition | Pool composition |
|---|---|
| `public_only` | All 13 → `public` |
| `baseline` | 8 `public` + 3 `partial` + 2 `private` (a mix of public, semi-private and fully private evaluation regimes) |
| `baseline_randomized` | 8/3/2 ratio with per-seed randomized assignment (isolates privacy-mechanism coefficient from benchmark-selection confound) |
| `private_dominant` | All 13 → `partial` |
| `private_only` | All 13 → `private` |
| `iid_holdout` | All 13 → `iid_holdout` |

Benchmark names are unchanged across conditions — only structural attributes (h, cosine) vary. LLM providers do not observe benchmark types or real-world analog labels; they infer from score patterns.

**Calibrated `baseline` assignment** (8/3/2 ratio anchored to 2024–2025 history): Safety Evaluation + Scientific Reasoning + Hard Coding as `partial` (SEAL-Safety / GPQA-Diamond / LiveCodeBench contamination-mitigated analogs); Adversarial Robustness (r12, Jan 2024, SEAL-Safety / HarmBench-private era) + Advanced Math (r24, Jan 2025, FrontierMath era) as `private`; remaining 8 as `public`.

**Premium access (orthogonal axis; not activated in primary conditions):**

| Parameter | Scope | Real-world analog |
|---|---|---|
| `premium_pre_access` | Per (provider, benchmark) | FrontierMath-OpenAI pre-launch access: simulates N rounds of public-weight observations at t=0, sharpening the new provider's `inferred_weights[b]` prior beyond the global σ_prior |
| `premium_submissions_per_round` | Per (provider, benchmark) | SEAL-style evaluator-capture: best-of-M scoring each round |

Available as ablation toggles for benchmark-sponsorship + evaluator-capture conditions. Implementation notes: pre-access sharpens initial belief via simulated delta-rule updates before benchmark goes live; submissions-per-round applies standard extremum-of-M score inflation (`sigma/√samples × √(2 ln M)`).

**Channels summary:**

| # | Channel | Controlled by | Mechanism |
|---|---|---|---|
| 1 | Weight distance | `cosine` | Gaming public weights partially misaligned with holdout reward |
| 2 | Reporting lag | `K = 3` | Slower market reactions via K-round publication delay |
| 3 | Observation noise | `h` | Smaller h = noisier holdout score (σ / √(samples × h)) |

Ablation comparisons isolate specific channels: `iid_holdout` vs `public_only` isolates Channels 2+3 (no weight distance); `private_dominant` vs `iid_holdout` isolates the marginal effect of cosine=0.95 weight asymmetry; `private_only` vs `private_dominant` isolates adversarial vs contamination-magnitude cosine (0.85 vs 0.95).

`benchmark_true_weights` are ground truth — held by the simulation, never passed to any actor. Providers observe per-category scores and infer what they reveal about the hidden dimension weights.

---

## Consumer Satisfaction Formula

```
satisfaction = dot(capability_vector, need_weights)
             - incident_penalty × (1 + market_share²)
             + cost_bonus
```

Satisfaction is purely experience-based. There is no `gaming_penalty` or `media_penalty` term. The score-satisfaction gap is a measurement artifact: it arises when a provider's capability vector is tilted toward benchmark-weighted dimensions that the consuming segment does not need. Media influence is routed through exploration behavior, not satisfaction (see Exploration Churn below; grounded in Hardy et al. 2024: benchmarks/media drive attention and exploration, not direct quality perception).

- **Incident penalty:** Severity-weighted (minor: 0.01, moderate: 0.05, major: 0.10, critical: 0.20) with exponential decay over time (`weight × 0.70^age`, ~2.3-round half-life, max 10-round window); 2x if category matches segment sector. Scaled by `(1 + market_share^2)` -- the HHI contribution of a single firm, reflecting that dominant providers face greater scrutiny and reputational exposure per incident (grounded in scale-contingent regulatory obligations: EO 14110, SB 1047). Weights are sized to prevent single-incident satisfaction wipeout while preserving meaningful differentiation.
- **Cost bonus:** `cost_sensitivity × cost_advantage × 0.15`

### Expected Quality (Selection Stage)

Consumers select providers based on observed signals, not true capability. Expected quality is:

```
expected_quality[provider] = leaderboard_trust × dot(published_scores, effective_relevance)
                            + (1 - leaderboard_trust) × running_perceived_quality[provider]
```

`running_perceived_quality` is updated each round via EMA (alpha=0.3) on realized satisfaction. This is the SERVQUAL Gap 5 framing: the gap between `expected_quality` and realized `satisfaction` drives switching dissatisfaction. AI services are credence goods — consumers cannot directly evaluate quality on their own tasks, so they rationally over-rely on benchmark signals (high `leaderboard_trust` segments) even when those signals are distorted.

Switching is triggered when `expected_quality - satisfaction > switching_threshold`.

**Exploration churn (media-driven):** Each round, a per-provider fraction of share enters an exploration pool. The base rate is 5%. Negative media coverage increases the rate for the covered provider's users: `provider_rate = 0.05 + provider_attention × abs(sentiment) × leaderboard_trust`. A critical incident (attention=1.0, sentiment=-0.40) on a high-trust segment (0.85) pushes exploration to ~39%; a quiet round stays at 5%. This is the primary pathway for media influence on consumers -- media drives attention and exploration, not direct satisfaction (Hardy et al. 2024).

Redistribution is blended: baseline explorers redistribute proportional to satisfaction (experience-based), while media-driven explorers redistribute proportional to `believed_quality` weighted by positive media buzz (`1 + sentiment × attention × trust`). This preserves credence good dynamics -- consumers who can't evaluate safety themselves follow public signals when exploring, including safety coverage. The media-driven fraction is estimated from the overshoot above base_rate.

**Positive exploration (media-driven):** When a provider receives positive media attention (`sentiment > 0`), users of other providers with low attention (`< 0.3`) churn toward the buzzy provider at rate `0.5 × max_attn × sentiment × leaderboard_trust`. Redistribution during positive-exploration rounds is additionally biased toward positively-covered providers via `bq_scores` boost. This models hype-driven switching (new model releases, breakthrough announcements) symmetrically with the negative-coverage exodus.

**New-user entry (market expansion):** When `market_growth_rate > 0`, new users enter each segment each round (sized by the growth rate as a fraction of existing market). New users are distributed proportional to `believed_quality` rather than inheriting incumbent shares, modeling that new adopters choose based on current public signals. No effect when `market_growth_rate = 0`.

**Implementation:** `believed_quality` in `MarketSegment` stores the blended `expected_quality`. Both `observe()` and `observe_per_benchmark()` compute the blend; `compute_satisfaction()` updates `running_perceived_quality` via EMA after each round.

---

## Provider Investment Model

### Portfolio Keys

Providers allocate 100% of their training budget across three levers each round:

| Lever | Competitive axis | Mechanical effect |
|---|---|---|
| `rd` | Capability (broad + targeted) | Directed toward benchmark-focused dimensions when `focus_level[b]` is set; approximately uniform when no deliberate focus; breakthrough-eligible |
| `safety` | Safety capability | Improves `capability_vector["safety"]` with diminishing returns `(1 - current_safety)`, stochastic efficiency `uniform(0.3, 0.9)` (mean 0.6). Execution inertia via rolling-averaged portfolio. |
| `product` | Analytics + retention | Two channels: (1) **Consumer signal fidelity** — quality-gates the consumer need signal used in R&D targeting (`compute_capability_gains`). Higher product budget means R&D grows capabilities users actually need. Sigmoid: `quality = 1/(1+exp(-3*(budget-0.5)))`, OS ceiling 0.40. (2) **Switching cost retention** — increases effective switching cost via `bonus = 0.50*(1-exp(-2*budget))`, OS cap 0.15. Both use absolute product budget (effective portfolio fraction x total budget). |

**Gaming mechanism:** When `focus_level[b]` is high for benchmark b, R&D gain concentrates on dimensions the provider believes b emphasizes (via `inferred_benchmark_weights[b]`). If those beliefs are accurate and benchmark weights diverge from consumer need weights, scores rise faster than consumer satisfaction. The score-satisfaction gap emerges without any explicit gaming term.

### Capability Update Rule

Each round, the simulation computes an effective budget with two layers of diminishing returns, then applies per-dimension gains:

```
-- Budget scaling (simulation-level, in simulation.py) --
rd_budget_raw     = base_revenue + funder_allocations
budget_scale      = sqrt(rd_budget_raw)                        # sqrt compression on funding
headroom          = max(0, capability_ceiling - mean(capability_vector))
effective_budget  = budget_scale × rnd_efficiency × sanction_multiplier × regulatory_multiplier × headroom

-- Per-dimension gains (provider-level, in model_provider.py) --
focus_weights[b]    = normalize(focus_level[b] for b in active_benchmarks)
benchmark_driven[dim] = sum(focus_weights[b] × inferred_benchmark_weights[b][dim]
                            for b in active_benchmarks)
                        # when all focus_level[b] at baseline: benchmark_driven[dim] ≈ uniform

-- Consumer signal quality-gated by product investment --
quality             = consumer_signal_fidelity(product_budget, is_open_source)
effective_signal[dim] = quality × true_consumer_signal[dim] + (1 - quality) × uniform[dim]

target[dim]         = benchmark_orientation × benchmark_driven[dim] + (1 - benchmark_orientation) × effective_signal[dim]

gain[dim] = rd × target[dim]

-- Safety lever: separate pathway with diminishing returns and noise --
safety_raw       = safety_fraction × effective_budget
safety_diminish  = safety_raw × (1 - current_safety)          # A: diminishing returns
safety_noisy     = safety_diminish × uniform(0.3, 0.9)        # B: stochastic efficiency (mean 0.6)

gain["safety"] += safety_noisy
-- Execution inertia handled by rolling-averaged portfolio (all levers) --

capability_vector[dim] = min(1.0, capability_vector[dim] + gain[dim])
```

**Budget scaling rationale:** Two mechanisms control runaway dynamics. The first option, `headroom ^ (1/diminishing_returns_rate)`, which penalized capability-level proximity to the ceiling. Two simpler mechanisms are used: (1) **sqrt budget compression** prevents runaway funding concentration from translating linearly to capability — 10x more funding does not yield 10x more capability due to coordination overhead, talent bottlenecks, and diminishing marginal returns on compute (Besiroglu et al. 2024, Epoch AI scaling); (2) **linear headroom** provides a gentle ceiling approach without a steep cliff. Together these prevent dominant-provider runaway without artificially capping leaders.

**Safety lever rationale:** Safety R&D has structurally different dynamics than capability R&D:
- **Diminishing returns** — easy wins (RLHF, basic red-teaming) come first; frontier safety research has uncertain and diminishing payoff
- **Stochastic efficiency** — red-teaming is discovery-based (some campaigns find critical issues, some find nothing); unlike compute-scaling where more FLOPS reliably improves loss curves
- **Execution inertia** — all portfolio allocations (rd, safety, product) use a 3-round rolling average, so shifts in safety investment take multiple rounds to fully materialize. The rolling average provides uniform inertia across all levers.

### Provider Belief Model

Providers hold beliefs about the benchmark's hidden dimension weights, updated each round from score prediction errors.

**ProviderPrivateState additions:**

```python
inferred_benchmark_weights: dict[str, dict[str, float]]  # per-benchmark × per-dim; heuristic-updated; initialized at noisy-public-weights prior (see "New benchmark initialization")
focus_level: dict[str, float]                            # per active benchmark, running scalar; provider-calibrated baseline
benchmark_orientation: float                             # fixed at 0.80 for all providers; not LLM-adjustable (mode="fixed")
consumer_signal: dict[str, float]                    # 6-dim vector; noise ∝ 1/sqrt(market_share)
```

**New benchmark initialization:** When a benchmark b is introduced mid-simulation, `focus_level[b]` is initialized at `mean(focus_level[other active benchmarks])` for that provider. `inferred_benchmark_weights[b]` initializes at a **noisy-public-weights prior**: `normalize(public_weights[b] + Normal(0, σ_prior))`, where σ_prior is a global config parameter representing framing uncertainty (provider knows what category the benchmark is in but not its exact dimension-profile). σ_prior is independent of h. For private/partial benchmarks, this prior differs from the holdout target by the cosine gap, which providers must learn via K-lagged published signals. Providers with `premium_pre_access[b]` additionally pre-run N simulated delta-rule observations of `public_weights[b]` at t=0, arriving with a sharper prior (models sponsor / early-access advantage; see Premium access section above). All providers are scored on all active benchmarks each round regardless of focus_level — scores feed the belief update from the benchmark's introduction round onward. `focus_level` affects capability gains, not scoring participation.

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

Prompt inputs: per-category scores this round (own + competitor ranks), score delta vs. last round, current `portfolio`, current `focus_level` per benchmark, current `inferred_benchmark_weights` per benchmark, `consumer_signal` vector with confidence interval, last `reasoning_memory_depth` entries from `recent_insights`. No apparatus vocabulary (`gaming`, `exploitability`, `benchmark_weight_confidence`) appears in any prompt. Providers are addressed as "the strategy team at {name}."

LLM output JSON:
```json
{
  "portfolio":       {"rd": "more", "safety": "same", "product": "less"},
  "benchmark_focus": {"General Capability": "same", "Coding Evaluation": "more",
                      "Safety Evaluation": "less", "Instruction Following": "same"},
  "reasoning": "Free-text summary — appended to recent_insights"
}
```

Outputs are ordinal signals (`"more"` / `"less"` / `"same"`). The sim applies δ to running `portfolio` and `focus_level` state and renormalizes. `reasoning` is appended to `recent_insights`. (`benchmark_orientation` is fixed at 0.80 and not LLM-adjustable in default mode; adjustable mode exists as an ablation via `--condition bm_orientation_adjustable`.)

**Prompt framing note:** `benchmark_focus` decisions must be framed as relative priorities — the prompt explicitly states that R&D capacity is finite, prioritizing one benchmark means less attention on others, and the provider should focus on benchmarks most important to their goals. Saying "more" on all benchmarks simultaneously is a no-op after normalization. `portfolio` framing is naturally relative since it is zero-sum.

**`consumer_signal`:** Providers receive a 6-dim vector representing what their current user base values, derived from market-share-weighted consumer need weights. Modeled on private usage data and telemetry (e.g. CursorBench-style signals):

```
profile_share[p]         = sum over archetypes a of segment_share[a, p]
segment_weights[p]       = profile_share[p] / market_share[provider]   # sums to 1
true_signal[dim]         = sum over profiles p of (segment_weights[p] × need_weights[p][dim])
consumer_signal[dim] = clip(true_signal[dim] + Normal(0, σ_base / sqrt(market_share[provider])), min=0)
consumer_signal      = normalize(consumer_signal)
```

`true_signal` sums to 1 by construction (weighted average of distributions). Noise uses relative market share — larger providers get a more precise signal. Per-dimension noise drawn independently; clipped and renormalized. Tracks the provider's current user base composition: as market share shifts across segments, the signal shifts accordingly.

`benchmark_orientation` (fixed at 0.80 for all providers) controls how much benchmark focus dominates over consumer signal in the capability update. In default mode (`benchmark_orientation_mode="fixed"`), the value is not LLM-adjustable — it acts as a structural constraint reflecting that real labs organize most R&D around benchmark targets. The value is surfaced in the LLM prompt as context (e.g. "80% toward benchmark performance, 20% toward user feedback") but the LLM cannot change it. Adjustable mode is available as an ablation (`--condition bm_orientation_adjustable`) but universally decays to the floor — see `docs/run_diagnostic_20260402_us_llm.md`.

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

**Initial capability vectors (calibrated for Q1 2023 landscape, 40-round growth trajectory):**

| Provider | reasoning | coding | knowledge | safety | communication | agentic | Notes |
|---|---|---|---|---|---|---|---|
| Orion Labs | 0.54 | 0.51 | 0.53 | 0.51 | 0.54 | 0.47 | GPT-3.5 frontier; early mover in consumer AI and developer APIs |
| Apex AI | 0.52 | 0.49 | 0.51 | 0.55 | 0.53 | 0.43 | Claude 1 launching; safety lead via Constitutional AI |
| Genesis Systems | 0.53 | 0.48 | 0.54 | 0.49 | 0.51 | 0.45 | Largest compute infrastructure; strong knowledge |
| Mirage AI | 0.51 | 0.49 | 0.49 | 0.45 | 0.49 | 0.41 | Large-platform lab; broad adoption focus |
| Spark AI | 0.49 | 0.51 | 0.46 | 0.43 | 0.47 | 0.46 | VC-funded startup; developer tools specialization |
| OpenCore | 0.47 | 0.49 | 0.46 | 0.42 | 0.45 | 0.40 | Open-weight lab; community-driven adoption |

Vectors use a tight spread (mean ~0.47–0.52) with elevated agentic baselines (0.40–0.47), reflecting that the simulation's 40-round growth trajectory requires room for differentiation without starting from near-zero in any dimension. Sqrt budget compression and linear headroom handle convergence dynamics rather than wide initial gaps.

### Cognitive Loop

1. **Observe** — per-category scores (own + competitor ranks), market share, incidents this round, media coverage, regulator interventions, `consumer_signal` vector
2. **Belief update** — heuristic: per-benchmark `inferred_benchmark_weights[b]` updated from score prediction errors (both modes)
3. **LLM call** — outputs ordinal {much_more/more/same/less/much_less} for `portfolio` levers and per-benchmark `focus_level`; sim applies deltas and renormalizes; `strategy_memo` + `reasoning` appended to `recent_insights`; `public_comms` sampled from lever allocations
4. **Execute** — capability updates computed from focus-weighted `inferred_benchmark_weights`

**Heuristic incident pressure:** Safety incidents accumulate `_incident_safety_pressure` (minor: 0.01, moderate: 0.04, major: 0.08, critical: 0.12, cap: 0.25), shifting `portfolio["safety"]` upward. Decays 60%/round (~2-round half-life).

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
| `open_source` | `False` | Enables OS-specific mechanics |
| `openness_level` | `0.0` | Fixed at init: 0=closed, 0.5=open-weight, 1.0=fully-open (weights + training data) |
| `cost_advantage` | `0.0` | Relative pricing competitiveness (0=most expensive, 1=free). OS providers default to 0.35 (blended average: large at scale, negligible for individual users) |
| `rd_budget_floor` | `0.0` | No hardcoded floor; OS funding comes through gov/foundation funder logic |
| `os_belief_broadcast` | `False` | Ablation flag (default off): whether OS weights accelerate other providers' benchmark belief convergence |
| `broadcast_rate` | `0.30` (hardcoded constant) | Scales belief broadcast nudge strength per round (only active when `os_belief_broadcast=True`) |
| `os_safety_erosion` | `False` | Ablation flag (default off): whether deployed safety is discounted below nominal |
| `erosion_sensitivity` | `0.50` (hardcoded constant) | Controls how rapidly safety erosion grows with deployment breadth (only active when `os_safety_erosion=True`) |

### OS-Specific Mechanics (Structural)

These are the structurally defensible differences between open-source and closed-source providers — kept because they reflect real asymmetries rather than injecting theory about outcomes.

**No VC funding:** VC-type funders skip OS providers entirely (no equity model). Gov and foundation funders can still allocate through normal funder scoring logic.

**Moderate cost advantage:** `cost_bonus = cost_sensitivity × cost_advantage × 0.15`. OS default `cost_advantage=0.35` reflects a blended population average: enterprises self-hosting at scale save significantly, but individual/SMB users see little cost difference (closed providers offer free tiers and cheap consumer plans). Existing segment-level `cost_sensitivity` ensures the bonus matters more for cost-sensitive segments.

**Slightly lower safety floor:** OS providers use `max(0.15, capability_vector["safety"])` vs. `max(0.25, ...)` for closed providers in the ground truth capability update (portfolio allocation floors are 0.10 vs 0.15). Gap is narrow — fine-tuning can partially strip guardrails, but base models ship with alignment. Actual safety outcomes emerge primarily from investment allocation, not the floor.

**No regulatory exemptions:** OS providers can be sanctioned and are subject to audit deployment gates, same as closed providers. The regulator decides how to treat open-source based on observable signals. A separate deployer liability guidance track exists: when an OS provider accumulates 2+ incidents, regulators may issue guidance shifting liability to commercial deployers — but this is a regulator *decision*, not an automatic exemption.

### PIMMUR Design Note

The OpenCore implementation is constrained to documented structural differences between open-weight and closed-source providers. The PIMMUR Minimal-Control audit verifies that no hardcoded advantage (safety-floor exemption, sanction exemption, audit-gate exemption, asymmetric switching friction, R&D-budget floor, belief broadcast, safety erosion) is wired in by default; only the asymmetries below remain on:
- **Calibrated asymmetries:** safety_floor gap (0.15 OS vs 0.25 closed), cost_advantage 0.35
- **Defaulted off:** belief broadcast, safety erosion (available as ablation flags)

5-seed heuristic test (seeds 7/12/42/88/103, 40 rounds): OpenCore averages ~28% market share (range 14-45%) with four different providers winning across seeds. Outcomes vary meaningfully by seed.

### Ablation: Belief Broadcast

When enabled (`os_belief_broadcast=True`), OS provider's published weights allow competitors to infer benchmark dimension emphasis. Each round, all providers receive a nudge to `inferred_benchmark_weights` toward true weights:

```
belief_broadcast = openness_level × deployment_breadth × broadcast_rate
```

Accelerates Goodhart dynamics (providers learn benchmark weights faster). **Default off** — theory-laden mechanism with no empirical calibration anchor.

### Ablation: Safety Erosion

When enabled (`os_safety_erosion=True`), deployed safety is discounted below nominal:

```
safety_erosion_factor = openness_level × market_share × erosion_sensitivity
deployed_safety       = capability_vector["safety"] × (1 - safety_erosion_factor)
```

**Default off** — directionally plausible but bakes in a strong assumption about downstream fine-tuning behavior.

---

## Evaluator / Benchmark Model

### Benchmark Structure

```python
@dataclass
class Benchmark:
    name: str
    tags: str                                                  # public keyword string for consumer relevance matching
    noise_level: float                                         # base noise sigma
```

`BenchmarkGroundTruth` (held by simulation, not the `Benchmark` dataclass) contains hidden `category_dimension_weights`, `noise_sigma`, and `samples`. The `Benchmark` dataclass is lean: there is no `validity` field. Published per round: overall score + per-category scores.

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

**Pool:** 22 benchmarks defined in `BENCHMARK_POOL` (`actors/evaluator.py`). Dimension weights are **peaked**: specialized benchmarks load 0.75-0.85 on their primary dimension so that focused investment can drive scores toward genuine saturation (0.90+). Broad benchmarks (General Capability, Hard Knowledge) stay flat (primary ~0.35-0.40). Full pool with weights in `BENCHMARK_POOL` constant.

Consumer population average need_weights (anchor for alignment assessment):
```
{reasoning: 0.20, coding: 0.12, knowledge: 0.25, safety: 0.18, communication: 0.20, agentic: 0.05}
```

Starting gap: ecosystem over-indexed on reasoning/coding, under-indexed on safety. Goodhart pressure concentrated there from round 0.

**Initial benchmarks (round 0):**

| Benchmark | Primary dim | Weight | Type | Real analog |
|---|---|---|---|---|
| General Capability | reasoning 0.35 + knowledge 0.30 | broad | MMLU |
| Coding Evaluation | coding 0.78 | peaked | HumanEval/MBPP |
| Safety Evaluation | safety 0.80 | peaked | TruthfulQA/BBQ |
| Instruction Following | communication 0.80 | peaked | MT-Bench/IFEval |

**Sequence benchmarks (introduced by cooldown schedule):**

| Benchmark | Primary dim | Weight | Type | Real analog |
|---|---|---|---|---|
| Scientific Reasoning | reasoning 0.78 | peaked | GPQA |
| Agentic Tasks | agentic 0.75 | peaked | SWE-bench |
| Hard Coding | coding 0.80 | peaked | LiveCodeBench |
| Long Context | communication 0.62 | moderate | RULER/HELMET |
| Domain Expert | knowledge 0.65 | moderate | MedQA/LegalBench |
| Agentic Safety | safety 0.50 + agentic 0.25 | dual-peaked | -- |

**Additional pool benchmarks (12):** Advanced Math (reasoning 0.85), Human Preference (communication 0.58), Hard Knowledge (broad), Clinical Reasoning (knowledge 0.65), Legal Reasoning (knowledge 0.60), Financial Analysis (knowledge 0.55), Multilingual Understanding (communication 0.55), Function Calling (agentic 0.40 + coding 0.30, anchored to BFCL), Adversarial Robustness (safety 0.85), Web Navigation (agentic 0.72), Issue Resolution (coding 0.42 + agentic 0.38), Creative Writing (communication 0.82).

**Toggleable misalignment extension (`benchmark_misalignment_enabled: bool = False`):** When enabled, benchmark weights are initialized via interpolation toward a misaligned vector concentrating on automatable/measurable dimensions (reasoning-heavy, safety-light). Default off; natural benchmark structures create sufficient Goodhart pressure.

### Saturation Detection (Delta-Based)

A benchmark is saturated when the max-score delta is below `saturation_delta_threshold` (0.005) for `saturation_window` (3) consecutive rounds. Perfect scores (>= 1.0) trigger immediate saturation. Per-benchmark `max_score_history` tracks the series (trimmed to window size). After saturation, a `cooldown_remaining` counter (default 2 rounds) is decremented each round before the saturation trigger can fire.

**Retirement:** When the evaluator introduces a new benchmark and the active count is at `max_benchmarks`, the most saturated benchmark is auto-retired (earliest `saturation_round`, then highest `max_score`). Retirement cleans up all tracking state. If no replacement config is available (sequence exhausted, pool empty), no retirement occurs. Retired benchmarks are tracked in `_retired_benchmarks`.

Media skips saturated benchmarks for headlines (`is_benchmark_saturated` check).

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
| **Create new benchmark** | `fixed_sequence`/`randomized_pool`: saturation (bypasses cooldown) or periodic schedule. `dynamic`: time-triggered every `benchmark_introduction_interval` rounds — heuristic picks the pool benchmark that best fills the need-vs-coverage gap; LLM picks from pool or chooses `none`. |
| **Retire benchmark** | Auto-retirement when `max_benchmarks` is reached and a new benchmark is introduced (most-saturated active benchmark is removed). In `dynamic` LLM mode, the LLM can also explicitly retire by judgment. |
| **none** | Default in `dynamic` LLM mode when no suitable candidate is found. |

### Evaluator Modes

```python
evaluator_mode: str = "fixed_sequence"     # "fixed_sequence" | "randomized_pool" | "dynamic"
benchmark_pool: list = BENCHMARK_POOL      # 22-benchmark expanded pool
benchmark_introduction_cooldown: int = 4   # rounds between periodic introductions (fixed_sequence / randomized_pool)
benchmark_introduction_interval: int = 4   # rounds between dynamic-mode introduction decisions
```

**Three modes (ladder, each step = single-primitive change from previous):**

| Mode | Trigger | Selection | Actor |
|------|---------|-----------|-------|
| `fixed_sequence` | Cooldown-periodic + saturation | Preset sequence | — |
| `randomized_pool` | Cooldown-periodic + saturation | Random draw from pool | — |
| `dynamic` | Time-triggered every `benchmark_introduction_interval` rounds | Gap-based pool selection (heuristic) OR LLM pool pick / `none` (LLM) | — (heuristic) OR `llm_plan_dynamic_evaluator` |

**Trigger logic for fixed_sequence / randomized_pool** (`_evaluate_introduction_trigger`):

| Trigger | Cooldown |
|---------|----------|
| Saturation (delta-based) | Min gap 1 round + per-benchmark `_saturation_cooldown` |
| Periodic (every `benchmark_introduction_cooldown` rounds) | Standard cooldown |

**Dynamic mode** (both heuristic and LLM variants):

- **Trigger:** time-based only — fires when `round_num % benchmark_introduction_interval == 0` (skips round 0). No dev pipeline; introductions are immediate.
- **Heuristic selection** (`_select_pool_benchmark_by_gap` in `simulation.py`): computes current dimension coverage across active benchmarks and market-fraction-weighted consumer need weights; picks the pool candidate whose dimension profile best fills `max(0, need - coverage)`.
- **LLM selection** (`llm_plan_dynamic_evaluator` in `llm.py`): picks from pool or chooses `none`/`retire` given observables (active benchmarks, score deltas, spread, saturation states, media headlines, `internal_validity`). If the LLM names a benchmark not in the current pool, the action is downgraded to `none`.
- Three-tier visibility preserved: dimension weights and ground-truth need weights are never shown to the LLM.

Known asymmetry: heuristic selection is gap-driven (reactive to the consumer-need/coverage mismatch); LLM selection reasons from public-visible signals only and can be proactive in ways the heuristic cannot. This asymmetry is intentional: the heuristic's by-design opacity establishes a Goodhart-pressure baseline, and divergence from the LLM-mode trajectory is itself the finding.

**LLM dynamic mode** uses `DYNAMIC_EVALUATOR_SYSTEM_PROMPT` (stewardship framing; inaction as default). No staff-capacity / pipeline block is surfaced — The time-trigger provides all pacing; there is no separate pipeline cap.

**Internal validity:** `Pearson_r(score_rank, market_share_rank)` — updated each round when `evaluator_mode == "dynamic"`. Evaluator-internal only, never published; passed to the LLM as an observable signal but not used as a trigger.

**Condition preset:** `--condition dynamic_evaluator` (works in both `--mode llm` and `--mode heuristic`).

**No apparatus vocabulary** in LLM prompts — saturation, validity, and Goodhart framing are never surfaced. The evaluator is addressed as "the team responsible for maintaining the AI evaluation leaderboard."

**Consumer market LLM mode** is optional and gated behind `consumer_llm_mode`. Default is heuristic-only. When enabled for organizations (`consumer_llm_organizations=True`), org segments use a PIMMUR-compliant vendor review brief (see Organizational Consumer LLM Mode section). Individual consumers remain heuristic-only by default — their decisions are routine and habitual rather than strategic.

### Evaluator-as-Company (`evaluator_as_company=True`)

Models evaluator conflict of interest (Leaderboard Illusion paper; cross-sector capture dynamics from credit rating agencies, financial auditing). Gated behind `evaluator_as_company: bool = False`.

**Three mechanics activate when enabled:**

**1. Best-of-N trial submissions.** Each provider chooses how many model variants to submit per round (1 to `max_eval_submissions`, default 10). Each extra submission costs `fee_per_submission` (default 0.03 sim units), deducted from R&D budget. Evaluator runs N independent scoring trials per benchmark; best score published. Selection bias from best-of-N with Gaussian noise: `E[max(X_1,...,X_N)] ~ mu + sigma * sqrt(2 ln N)`.

- **Heuristic mode:** `N = min(max_n, 1 + int((base_revenue + discretionary_budget) * 0.15 / fee))`. Affordability-gated by 15% of total resources.
- **LLM mode:** Provider outputs `"n_submissions": int` in planning JSON. Prompt frames it as a strategic cost/benefit tradeoff.
- **K-lag fee gating:** On rounds where no benchmark produces a fresh score (fully-frozen K-lag rounds under `private_only` / `iid_holdout`), fee is waived and `premium_revenue` is zero. Best-of-N only runs on publish rounds, so the fee only fires when the service is rendered. Checked via `EvalEcosystemSimulation._any_benchmark_publishes_fresh(round_num)`.

**2. Early access.** Premium subscribers start closer to the actual holdout-scoring target at benchmark introduction. The blend uses the noisy-public-weights prior (`normalize(public_weights + Normal(0, σ_prior))`) as the base and pulls it toward the benchmark's `holdout_category_dimension_weights`:

```
premium_init = (1 - factor) × noisy_public_prior + factor × holdout_weights
```

`factor=0` matches non-subscribers (no advantage); `factor=1` gives exact holdout knowledge at introduction. On public-type benchmarks where `holdout_category_dimension_weights is None`, the blend falls back to public weights and collapses to a weak sharpening of the noisy prior — i.e. evaluator-capture sells private-benchmark access advantage specifically, consistent with the SEAL business model. Justification: paying subscribers have implicit bias-variance knowledge (better sense of where their models overfit), so start with a holdout-target-informed prior without extra effort. Default `early_access_factor=0.5`.

**3. Discretionary budget.** Per-provider `discretionary_budget` field represents parent company resources available for evaluator access (does NOT affect R&D capability gains). Only affects submission affordability calculation. Models that Google/Meta subsidiaries can trivially afford maximum submissions while standalone startups are constrained.

| Provider | discretionary_budget | Rationale |
|---|---|---|
| Genesis Systems | 2.0 | Alphabet subsidiary |
| Mirage AI | 2.0 | Meta subsidiary |
| Orion Labs | 0.5 | Microsoft partnership |
| Apex AI | 0.3 | VC-funded standalone |
| Spark AI | 0.0 | Resource-constrained startup |
| OpenCore | 0.0 | Open-source, limited discretionary |

**Config parameters:**

| Parameter | Default | Description |
|---|---|---|
| `evaluator_as_company` | `False` | Feature gate |
| `evaluator_base_budget` | `0.0` | Evaluator starting budget (display dollars) |
| `fee_per_submission` | `0.03` | R&D cost per extra submission (sim units) |
| `max_eval_submissions` | `10` | Hard cap on submissions per provider per round |
| `early_access_factor` | `0.5` | Belief blend: 0=noisy-public prior (no advantage), 1=exact holdout weights |

**Logging:** `evaluator_business_metrics` in `rounds.jsonl` includes `submission_counts` (per-provider N), `premium_revenue`, `n_premium_subscribers`. Provider execution memory includes `n_submissions`.

---

## Consumer Market

### Segments

Each segment = use-case profile × behavioral archetype. Archetypes modify observation behavior and switching friction only — not `need_weights`. Actual needs are the same regardless of archetype; the gap between how a segment selects providers (leaderboard-based) and what it actually needs (`need_weights`) is itself a dynamic of interest.

**Archetypes:**

| Archetype | `leaderboard_trust` | `switching_cost` | `switching_threshold` | `cost_sensitivity` |
|-----------|---------------------|------------------|-----------------------|--------------------|
| `leaderboard_follower` | 0.85 | 0.05 | 0.10 | 0.15 |
| `experience_driven` | 0.35 | 0.08 | 0.06 | 0.30 |
| `cautious` | 0.50 | 0.20 | 0.18 | 0.20 |
| `enterprise_cautious` | 0.25 | 0.35 | 0.20 | 0.10 |
| `enterprise_growth` | 0.45 | 0.25 | 0.15 | 0.15 |
| `enterprise_established` | 0.35 | 0.40 | 0.18 | 0.08 |

### Need Weights Per Profile

| Profile | reasoning | coding | knowledge | safety | communication | agentic | Pop weight |
|---|---|---|---|---|---|---|---|
| **Individual** | | | | | | | |
| software_dev | 0.22 | **0.55** | 0.03 | 0.02 | 0.03 | 0.15 | 0.14 |
| content_writer | 0.10 | 0.02 | 0.20 | 0.03 | **0.63** | 0.02 | 0.08 |
| legal | 0.30 | 0.01 | **0.35** | 0.22 | 0.10 | 0.02 | 0.04 |
| healthcare | 0.12 | 0.02 | 0.28 | **0.48** | 0.08 | 0.02 | 0.05 |
| finance | **0.35** | 0.08 | 0.22 | 0.25 | 0.05 | 0.05 | 0.05 |
| educator | 0.15 | 0.02 | 0.28 | 0.08 | **0.45** | 0.02 | 0.07 |
| customer_service | 0.05 | 0.01 | 0.12 | 0.15 | **0.50** | 0.17 | 0.08 |
| researcher | 0.30 | 0.22 | 0.28 | 0.03 | 0.07 | 0.10 | 0.06 |
| creative | 0.12 | 0.02 | 0.10 | 0.03 | **0.65** | 0.08 | 0.06 |
| marketing | 0.12 | 0.02 | 0.18 | 0.03 | **0.55** | 0.10 | 0.07 |
| service_worker | 0.08 | 0.01 | 0.15 | 0.18 | **0.55** | 0.03 | 0.05 |
| **Organizational** | | | | | | | |
| hospital_system | 0.12 | 0.02 | 0.25 | **0.48** | 0.10 | 0.03 | 0.05 |
| enterprise_finance | 0.32 | 0.08 | 0.18 | 0.30 | 0.05 | 0.07 | 0.05 |
| tech_startup | 0.18 | **0.38** | 0.05 | 0.04 | 0.05 | **0.30** | 0.06 |
| enterprise_legal | 0.28 | 0.02 | **0.35** | 0.22 | 0.11 | 0.02 | 0.04 |
| government_agency | 0.12 | 0.02 | 0.22 | **0.48** | 0.12 | 0.04 | 0.05 |
| enterprise_hr | 0.20 | 0.02 | 0.20 | **0.35** | 0.18 | 0.05 | 0.04 |

Population weights are adoption-weighted market shares, grounded in NBER Bick/Blandin/Deming 2024 occupation-level AI adoption data, Stanford AI Index 2025, and McKinsey State of AI 2025. `enterprise_hr` is anchored in EEOC 2024 algorithmic-discrimination guidance + NYC Local Law 144 + EU AI Act Annex III §4. Full citations are in the paper's bibliography. Raw pop weights sum to 1.04; `create_default_segments` normalizes to 1.0.

Population-weighted average ≈ `{reasoning: 0.18, coding: 0.12, knowledge: 0.18, safety: 0.17, communication: 0.27, agentic: 0.09}` (`enterprise_hr` ticks safety up ~0.007 via its safety-0.35 weight). `agentic` is intentionally low at simulation start (2023).

### Benchmark Relevance (Derived)

Each benchmark carries a `tags` string (e.g., `"coding software engineering programming"`). Benchmark relevance is derived at runtime by matching segment `benchmark_prefs` category keywords against each benchmark's tags:

```python
for category, pref_weight in segment.benchmark_prefs.items():
    if category in benchmark.tags:
        weights[benchmark] = max(weights[benchmark], pref_weight)
# Organizational field-specific upweighting (1.5x) from ORG_FIELD_PRIORITIES
# Normalize to sum to 1.0
```

Unmatched benchmarks get a default weight of 0.1. Multiple keyword matches take the max preference weight. Tags are set in benchmark configs and propagated through the sequence. When new benchmarks are introduced mid-simulation, `resolve_benchmark_weights()` is re-called with the updated tag map.

Tag-matching is the implemented mechanism (no `benchmark_public_category_weights` data structure exists); it gives a directional effect with auditable parameters.

### Switching

Proportional sigmoid-based switching within each segment. Two independent triggers:

1. **Dissatisfaction:** `gap = believed_quality - satisfaction`. Fires when gap > 0; probability = `sigmoid(10 * (gap - threshold))` where `threshold = switching_threshold + switch_cooldown`.
2. **Opportunity:** `improvement = blended_score[alt] - blended_score[current]`. `opportunity_threshold = switching_threshold * 0.5 + switch_cooldown`.

**Switching cost** acts as a damper on the fraction that follows through: `cost_damper = 1.0 - min(0.9, switching_cost * (1 + retention_bonus))`. Product investment retention bonus (`retention_bonus`) connects provider product lever to consumer stickiness.

**Post-switch cooldown.** After a switch, `_switch_cooldown` spikes to 0.20 and decays 0.5x per round (~2-round half-life). This naturally models institutional inertia without a binary gate or separate parameter.

### Dynamic Consumer Market

When `dynamic_consumer_market=True` (the **default**), enterprise segment `market_fraction` grows from ~25% to ~55% over the simulation via a logistic curve, modeling the real-world shift from consumer-dominated (Q1 2023) to enterprise-dominated (mid-2025) AI market. Individual segments shrink proportionally. Within each class, relative proportions are preserved. The inverse ablation is `--condition static_enterprise_size`, which sets it back to `False`.

```
enterprise_share(t) = start + (end - start) / (1 + exp(-0.25 * (t - midpoint)))
```

Default: `enterprise_share_start=0.25`, `enterprise_share_end=0.55`, `enterprise_growth_midpoint=18`. Informed by the McKinsey State of AI and Stanford AI Index adoption surveys. The enterprise-share curve itself is a modeling choice.

### Organizational Consumer LLM Mode

When `consumer_llm_mode=True` and `consumer_llm_organizations=True`, organizational segments use a single LLM call per segment per round (not per-provider). The prompt is a PIMMUR-compliant vendor review brief containing:
- Cross-round memory (last 2 decisions with reasoning)
- Current vendor experience (qualitative: Excellent/Good/Mixed/Poor)
- Benchmark comparison table (rank labels, no raw scores)
- Alternative vendors (qualitative performance, cost tier, incident count)
- Compliance requirements, media intelligence, regulatory context
- No simulation parameters, no private state, no apparatus vocabulary

Output format: `{action: renew|switch|pilot, target_provider, share_to_move, reasoning}`. "Pilot" moves 10-25% of deployments; "switch" moves 30-100%. Cooldown spikes after switch (0.25) or pilot (0.15).

---

## Incident System

Probabilistic AI safety incidents with ecosystem-wide propagation effects. Empirical grounding in `docs/incident_path_dependence.md` (cross-sector survey of 12+ real-world cases).

**Base rate:** 20% per provider per round (calibrated so the safety lever is observable against the market-share confound). Multiplied by factors:

| Factor | Formula | Direction |
|--------|---------|-----------|
| Safety investment | `1 - (portfolio["safety"] × 1.5)`, clipped ≥ 0 | Higher safety allocation → lower prob |
| Market share (exposure) | `(0.3 + market_share × 1.5) × sqrt(total_market_size)` | Larger market → higher prob |
| Incident history escalation | `+0.02 per prior major/critical in last 15 rounds, cap +0.10` | Past harm → elevated future risk (ages out) |
| Active sanction | `0.75×` while sanctioned | Regulatory oversight → reduced prob |

Floor at 2%. Capped at 50% per round.

**OS providers:** Use `deployed_safety` (after erosion) rather than `capability_vector["safety"]` when `os_safety_erosion=True`.

**Mandatory safety floor under compliance:** Providers under `commission_audit` or `impose_sanction` have `capability_vector["safety"]` clamped to a minimum floor.

**Severity distribution:**

| Severity | Probability |
|----------|-------------|
| Minor | 50% |
| Moderate | 31% |
| Major | 12% |
| Critical | 7% |

**Categories:** `healthcare_harm` (20%), `security_breach` (25%), `bias_discrimination` (20%), `safety_failure` (20%), `misinformation` (10%), `misuse` (5%).

**Sector propagation:** Each category has an `affected_sectors` list. Segments whose `use_case` or `consumer_type` is in that list get a 2× satisfaction-penalty multiplier. Mapping:

| Category | Sectors |
|---|---|
| healthcare_harm | `hospital_system`, `healthcare` |
| security_breach | `enterprise_finance`, `hospital_system` |
| bias_discrimination | `enterprise_hr`, `enterprise_finance`, `government_agency` |
| safety_failure | `enterprise_finance`, `government_agency` |
| misinformation | `individual`, `government_agency` |
| misuse | `individual` |

Matching logic at `consumer.py:645`: `if seg.use_case in affected_sectors or seg.consumer_type in affected_sectors: weight *= 2.0`.

**Ecosystem propagation:**
- **Media:** Critical incidents get guaranteed headline slots; major/moderate incidents compete for coverage in the pooled event system via weighted sampling (major: 3x weight, moderate: 2x, routine news: 1x). This models the attention economy — not all incidents make the news, but severe ones are more likely to. Provider attention and sentiment penalties apply regardless of coverage.
- **Consumers:** Incident penalty in satisfaction; `leaderboard_trust` erosion across all archetypes (scaled by current trust -- high-trust segments erode more); media-driven exploration boost
- **Regulator:** Risk belief updates; critical incidents may skip escalation levels
- **Funders:** Incident penalty in provider scoring

**Empirical calibration:** Cross-sector survey validates that critical incidents can cause 30+pp market share swings: Boeing 737 MAX (737 share of 737 + A320-family deliveries 48% in 2018 to 9% in 2020, 31% in 2024), Avandia (rosiglitazone share of TZD Medicaid prescriptions 56% to 19% / 49% to 23%, Hsu et al. 2015), Cruise robotaxi (permit suspension Oct 2023, GM ended robotaxi funding Dec 2024). Severity weights and history escalation (+0.02/prior, cap 0.10, 15-round aging) are sized to prevent death spirals while preserving meaningful differentiation. Across a 5-seed validation, 3 different winners emerge; strategic advantage survives moderate incidents while critical incidents still reshape markets. Key calibration nuances from the evidence:
- **Incident type matters:** Physical harm + regulatory shutdown produces permanent exits; pure reputational/trust incidents produce ~0pp shifts in AI markets (trust-behavior gap). Media headline competition (critical=guaranteed, major/moderate=pooled with weighted sampling) partially captures this: critical incidents always dominate news, while moderate incidents may be crowded out by other stories.
- **Recovery is slow and fragile:** Boeing partially recovered in 3 years but was reset by a second incident. Decay half-life (~2.3 rounds) remains unchanged; the reduced severity weights lower the peak penalty rather than extending the tail.
- **"Liability of good reputation":** Market leaders are MORE vulnerable to incident shocks (Rhee & Haunschild, 2006). The `(1 + market_share^2)` scaling captures this.
- **Contagion vs. competition:** Some incidents damage the entire sector (COX-2 class destruction after Vioxx), not just the affected firm. Not modeled.

---

## Regulator

Graduated intervention model with threshold-based triggers, cooldowns, and exogenous policy events.

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

| Lever | Real-world analog | Cooldown | Mechanical effect (heuristic mode) |
|---|---|---|---|
| `request_voluntary_commitment` | White House/Seoul safety pledges (SB 53) | 3 rounds | Providers boost safety `public_comms` weight (+0.15, decaying). Cheap talk — no direct capability effect. |
| `publish_advisory` | AISI evaluation summaries, NIST AI RMF | 4 rounds | Enterprise archetypes reduce `leaderboard_trust` (x0.90, floor 0.15). Market-side effect — changes demand, not supply. |
| `mandate_safety_disclosure` | EU AI Act Art. 13, system card mandates | 6 rounds | Providers boost safety `public_comms` weight (+0.20, decaying). Compliance overhead: `rnd_efficiency` x0.95 for cooldown duration. |
| `commission_audit` | AISI pre-deployment evaluation, EU conformity assessment | 8 rounds | Compliance overhead: `rnd_efficiency` x0.85 for 3 rounds. If `audit_is_binding`: all capability gains zeroed for 1 round (deployment gate). |
| `impose_sanction` | EU AI Act fines (7% turnover), FTC enforcement | 10 rounds | Existing `rnd_efficiency` penalty + funder allocation x0.90 for sanction duration. |

**`audit_is_binding: bool`** (part of regulatory preset):
- `False` (US default): compliance overhead only — no deployment gate
- `True` (EU default): capability gains zeroed for 1 round (deployment gate)

**Design principle:** No lever forces providers to invest more in safety. Levers operate through cost (efficiency penalty), information (disclosure), market signals (enterprise trust), and funding (capital flight). Provider response to these pressures is their own strategic choice. In LLM mode, richer effects emerge from actors reasoning about communicated interventions.

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
| Incident threshold (low) | 0.03 | 0.05 | 0.08 |
| Incident threshold (medium) | 0.10 | 0.15 | 0.20 |
| Incident threshold (high) | 0.20 | 0.25 | 0.35 |
| `audit_is_binding` | True (after round 14) | False | False |
| Posture | Proactive, precautionary | Moderate | Reactive, incident-driven |

Thresholds calibrated against realistic incident rates (~5-7% per-provider per-round, severity-weighted 3-round window typically 0.03-0.10). Flagged for sensitivity analysis.

Threshold values are config parameters.

### Cross-Round Memory (PIMMUR)

`RegulatorPrivateState` holds `recent_reasoning` (last 3 entries stored; last 2 passed to prompts, each truncated to 120 characters). Allows maintaining consistent policy stances across rounds.

---

## Funder

### Types and Investment Logic

| Type | Pattern | `funding_cooldown` | Can allocate to OS? |
|------|---------|----------|---------------------|
| `vc` | Concentrated; skips OS providers (no equity model) | 4 rounds between decisions | No |
| `corporate` | Multi-relationship; anchored to market position; 2–4 strategic partners | 7 rounds between decisions | Yes |
| `gov` | Spread proportionally; safety/mission-oriented | 10 rounds between decisions | Yes |
| `foundation` | Ecosystem health focus; safety/mission-oriented | 6 rounds between decisions | Yes |

Cooldowns calibrated against per-provider funding event rates, adjusted for the sim's roster-vs-real-ecosystem aggregation factor. See `docs/funder_calibration.md`.

**Provider budget model:**

```
provider_rd_budget = base_revenue_income + sum(active_funder_allocations)

base_revenue_income = market_share × revenue_per_share × (1 - cost_advantage)
```

`revenue_per_share` is a fixed global scalar (calibration-time). Budget feeds into capability gains via `sqrt(rd_budget_raw)` — diminishing returns on funding scale, reflecting coordination overhead and talent bottlenecks at scale (Besiroglu et al. 2024, Epoch AI scaling laws). `cost_advantage` discounts revenue for low-cost providers — OS providers with `cost_advantage = 0.9` generate almost no base revenue and depend on `rd_budget_floor`. Sanctions reduce `rnd_efficiency` multiplicatively (not the budget itself). Funder data stores `provider_funding_totals` (raw dollar amounts per provider) rather than normalized multipliers.

**Funder allocation pool:** Each funder holds a `total_capital` pool representing the sum of its intended deployment across the full sim window, and a per-decision deployment fraction (`max_round_deployment`) of whatever is *active* at that round. Capital becomes active via a geometric availability curve (`capital_growth_rate`, default 7%/mo compounded), normalized so availabilities sum to 1.0 across the sim — modeling the empirical ecosystem ramp (~2.3× YoY corporate capital, 2023–2026). Per-decision deployment: `max_round_deployment × availability(round) × total_capital`. See `docs/funder_calibration.md` for anchors and the downstream rd_budget analysis that preserves mean capability-growth calibration without requiring `FUNDER_BUDGET_SCALE` to change.

**Scoring formulas (used to normalize allocation across providers):**

```
vc:          (market_share_growth × media_sentiment × (1 - incident_risk) × (1 - market_share))
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
- Media sentiment (single outlet-level scalar in heuristic mode; headlines naming providers in LLM mode)
- `public_comms` last 3 rounds per provider (direct — not filtered through media)
- Other funders' investment behavior (herding signal)
- Regulator interventions (recent window) and active regulations

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

**Headline budget:** Critical incidents are guaranteed slots. Major and moderate incidents enter the pooled event system alongside other news (score changes, regulatory actions, funding, product launches) and compete for limited headline slots via weighted sampling (major: 3x, moderate: 2x, routine: 1x). Up to `media_sample_size` (default 4) pooled events are sampled per round. This models the attention economy — a moderate security breach makes the news on a slow day but gets buried when there's a major product launch and a regulatory action in the same round.

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

Media independently covers leaderboard changes and score leaders — no score-delta boost needed in `public_comms` weights. Score-driven visibility flows from media to consumers via the exploration pathway: big score jumps generate media coverage (provider_attention + sentiment), which increases per-provider exploration rates for high-trust segments and biases redistribution toward positively-covered providers.

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

`narrative_state` is the primary input to the regulator's `media_pressure` index. Funder sentiment is modulated by `sentiment` and `provider_attention`. Consumer exploration rate uses `provider_attention` and `sentiment` to drive per-provider churn and redistribution weighting.

All internal trigger labels (`gaming_scandal`, `saturation_narrative`, `CRISIS`, etc.) are simulation-internal only — never passed verbatim to any LLM prompt. Translated to natural language before injection.

**Implementation:** `_update_narrative_state()` in `media.py`. Thresholds: `incident_low=3`, `incident_high=8`, `crisis_recovery=3` rounds, `skepticism_recovery=5` rounds, `scandal_divergence=3` rounds. Gaming scandal fires when score leader diverges from market share leader for 3+ rounds AND an incident occurred. Headline budget: `media_sample_size=4`.

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

- **Startup entry dynamics** — removed; no mid-simulation provider spawning. BTE index is computed as an ecosystem health metric but does not feed into any mechanic.
- **Market concentration review** — antitrust lever dropped from regulator interventions
- **Sandbagging** — providers strategically underperforming on audits when audit context is detected
- **Dynamic need_weights** — `agentic` and related dimensions growing over simulation time as adoption spreads
- **Whistleblower/counter-narrative events** — researcher departure events triggering negative coverage
- **Funder herding mechanic** — no explicit herd behavior; herding emerges naturally from funders observing each other's allocations and updating `believed_provider_quality` accordingly

---

## Calibration Notes

### Open Source Capability Jump Calibration

The OS provider has two update modes: slow continuous R&D gain (every round) and episodic step-change capability jumps representing major frontier OS releases (LLaMA 2 → 3.1 → DeepSeek R1 anchor). `jump_magnitude` and `jump_probability` are anchored to release-cadence and capability-step distributions observed in Epoch AI's Notable AI Models dataset and the HELM / Open-LLM-Leaderboard histories.

### Ecosystem-Level Metrics

Metrics like `score_reliability` (Pearson-r of scores vs. satisfaction) are detectable only through triangulation across multiple actors' partial views — no single actor has the full picture. How these are computed and how actors respond to their respective fragments is out of scope.

### Provider Satisfaction Signal and PIMMUR

`consumer_signal` is surfaced in LLM mode as raw data — no prescribed inference. A provider may respond to a rising score / falling satisfaction gap in multiple ways; that heterogeneity is intentional. In heuristic mode, `consumer_signal` does not directly wire into portfolio allocation. Nuanced satisfaction-responsive reasoning is an LLM-mode capability.

---

## Parameter Defaults

| Parameter | Default | Rationale |
|---|---|---|
| `learning_rate` (belief update) | 0.15 | ~10-round convergence on benchmark weights |
| `broadcast_rate` | 0.30 (hardcoded constant) | Noticeable but not dominant nudge; ablation via toggle |
| `erosion_sensitivity` | 0.50 (hardcoded constant) | ~5–15% erosion at realistic OS market shares; ablation via toggle |
| `silence_weight` (`public_comms`) | 0.30 (hardcoded constant) | Providers don't post every round |
| `ORDINAL_DELTA` / `ORDINAL_DELTA_LARGE` | 0.05 / 0.10 | 5-level ordinal scale: much_more (+0.10), more (+0.05), same (0), less (-0.05), much_less (-0.10). Applied to portfolio, focus_level, and benchmark_orientation; clip and renormalize after applying |
| `benchmark_orientation` | 0.80 (fixed, uniform across providers) | 80% benchmark-driven, 20% satisfaction-signal-driven R&D targeting. Not LLM-adjustable in default mode. |
| `breakthrough_probability` | 0.05 | Per-provider per-round probability of a uniform capability boost (proportional to rd fraction) |
| `breakthrough_magnitude` | 0.20 | Size of breakthrough boost when triggered |

---

## Open Calibrations

Parameters with working-estimate anchors; sensitivity not formally swept. Listed for transparency.

- **Mandatory safety floor**: 0.35.
- **Initial capability vectors**: anchored to `external-validation/` data.
- **`focus_level[b]` baselines**: 24 values at round 0 (6 providers × 4 benchmarks), growing to 60 by round 28. Qualitative anchors in Default Provider Profiles above.
- **R&D gain scaling**: `rd × target[dim]` per round, anchored to observed capability-growth trajectories.
- **`sigma_base`**: noise scale for `consumer_signal`, sized so the signal is informative but not precise at realistic market shares.
- **`benchmark_orientation`**: fixed at 0.80 for all providers (uniform); adjustable mode available as ablation.
- **Media parameters**: narrative transition thresholds, sentiment weights per trigger type, `saturation_threshold`.
- **Funder parameters**: `funder_pool` size per type, `revenue_per_share` scalar, scoring formula weights.
- **Regulator parameters**: threshold values per preset (EU / Balanced / US).
- **Consumer state**: `running_perceived_quality` initialization value per segment per provider.
- **Incident severity/recovery**: critical penalty 0.30 with ~2.3-round half-life produces 30+pp swings, consistent with Boeing / Avandia / Cruise evidence. See `docs/incident_path_dependence.md` for the full empirical framing.

---

## Experiment Seeds

30 unique 3-digit seeds used for all heuristic baseline runs. Generated once and fixed for reproducibility. Stored in `docs/SEEDS.txt`.

```python
import random
random.seed(42)
seeds = sorted(random.sample(range(100, 1000), 30))
```

Seeds: 125 127 130 132 189 195 204 214 242 303 323 328 338 350 381 529 532 617 658 674 704 716 754 765 792 818 833 854 858 859
