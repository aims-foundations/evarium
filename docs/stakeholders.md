# Stakeholder Architecture: No Explicit Gaming

> **Living architecture reference. Last updated: 2026-04-23 (session 49d end: (i) all 6 provider identities rewrote grounded in real-world public positioning — removed moral-licensing hooks in Apex, caricature language in Orion, "minimal safety/no guardrails" prescriptions in OpenCore; (ii) A1 benchmark-type mechanism context added to provider prompts (K=3 reporting lag, holdout weight framing — factual, not coaching); (iii) dumbbell + allocations_over_time plots autogenerate; (iv) media headline budget 4→6 + two new leaderboard headline triggers (milestone crossings, rival-closes-gap); (v) incident exposure-multiplier floor 0.5→0.3 to reduce disproportionate per-share incident over-tax on small providers. Post-identity 40r validation confirms: Apex moral-licensing resolved during incidents (partial late-run regression), OpenCore emerges as safety leader (no-guardrails coaching removal), VC herding strongly resolved (r=0.20 mean), Orion rebuilds despite regulator targeting. Session 49c (prior): regulator-intervention-target plumbing fix (`simulation.py` aggregation was dropping the provider field); LLM dynamic evaluator prompt audit landed (memory channel via `_dynamic_llm_decisions`, F-soft trigger reframe, enriched retirement/introduction metadata, active_regulations); TechVentures VC identity softened "winners"→"allocation" to reduce VC herding; 40-round baseline_40r + 10-round dynamic_10r + 10-round vcfix_10r LLM smokes landed. Session-49 prior (2026-04-22): funder recalibration from empirical AI-funding research (`docs/ai_corporate_funder_research.md`). Changes: (1) Cooldowns recalibrated (VC 2–3→4, corporate 3→7, gov 4→10, foundation 3→6) anchored to per-provider event rates divided by sim-to-real aggregation factors. (2) Corporate per-provider rotation rule deleted (contradicted data; zero strategic exits 2020–2026). (3) Second corporate funder `IndustryPartners_AI` added — minimum needed for aggregation math. (4) Availability-curve mechanism added: `total_capital` re-anchored to $198B ecosystem integral with empirical-first splits; geometric release `availability(r) = (1+g)^r / Σ` normalized to sum to 1.0 over sim, `g=capital_growth_rate=0.07` (7%/mo, 2.3× YoY). Per-decision deployment = `max_round_deployment × availability(r) × total_capital`. `FUNDER_BUDGET_SCALE` kept at 1e-9. (5) LLM funder renormalization bug fixed (`src/llm.py:1671–1678`): prior code scaled-up under-deployments, violating "hold in reserve" prompt intent; now caps at total_capital, never scales up. Full calibration provenance in `docs/funder_calibration.md`. Session 48 (prior): LLM planning prompt overhaul for Model Provider and Regulator — identity moved to system prompt, competitor/industry-news signals added, per-provider incident aggregation. See Session Changelog for full session-48 detail.)**
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
| `rough/logging_spec.md` | verbose=False / verbose=True logging spec |
| `rough/validation_plan.md` | Validation plan — Sargent, PIMMUR, Windrum, Axtell, Park et al. |
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

Published every K rounds (K = `evaluation_lag` = 3). Between publications, providers see stale scores. There is no blended formula; the market receives only the holdout-derived signal for any benchmark with a holdout.

**h controls observation noise, not blending.** `h` is the fraction of benchmark items in the private holdout; the holdout-only score is computed on `samples × h` items, so smaller h produces a noisier statistic. For `partial` (h=0.3) vs `private` (h=1.0): partial has ~1.8× the score noise. Practice-signal mechanisms on the publicly-observable `(1-h)` fraction are NOT modelled; providers have no direct observation of the public portion beyond their prior on `public_weights` (see Provider Belief Model below).

**Three benchmark types + one ablation type:**

| Type | h | cosine(public, holdout) | Real-world analog |
|---|---|---|---|
| `public` | 0 | — | MMLU, HumanEval, GPQA |
| `partial` | 0.3 | 0.95 | SEAL-style, contamination-magnitude asymmetry (Singh et al. 2024 retro-holdout anchor) |
| `private` | 1.0 | 0.85 | FrontierMath-style, adversarially constructed holdout |
| `iid_holdout` | 1.0 | 1.00 | Ablation only: isolates reporting lag from weight asymmetry (holdout weights = public weights) |

Cosine values anchored empirically: 0.85 matches Epoch within-family Pearson correlation (e.g., FrontierMath T1-3 vs T4: 0.85) and MMLU-vs-MMLU-Pro / GSM8K-vs-GSM-Plus literature. 0.95 anchors to Singh et al. (2024) 8–16pp inflation from retro-holdout contamination, which maps to effective cosine ~0.95–0.97 at typical capability magnitudes. Cosine-<1 is a **composite proxy** for contamination, training-on-the-test-task (Dominguez-Olmedo et al. 2024), and distributional adversarialness — the sim's single-knob abstraction of multiple literature mechanisms.

**Evaluation cadence (`evaluation_lag`, K):** K = 3 rounds (global, all providers × all private benchmarks publish simultaneously). Empirical anchor: median-of-medians K_advance = 3.0 months across 24 Epoch AI benchmarks × 8 frontier labs (`external-validation/scripts/analyze_k_cadence.py`, derived tables in `external-validation/data/processed/`). Code default stays at K = 0 until full wiring lands; condition configs set K=3 explicitly. Per-provider asynchronous release variants (Fix-C / Poisson/Bernoulli) are deferred as sensitivity ablations — see `TODO.md`.

**Six ablation conditions (session 43; pool attribute assignments over the 13-benchmark static set — 4 active at round 0 + 9 introduced at intervals of 4 rounds through round 36):**

| Condition | Pool composition |
|---|---|
| `public_only` | All 13 → `public` |
| `baseline` | 8 `public` + 3 `partial` + 2 `private` (matches 2024–2025 empirical 62/23/15% split) |
| `baseline_randomized` | 8/3/2 ratio with per-seed randomized assignment (session 43; isolates privacy-mechanism coefficient from benchmark-selection confound — see `rough/randomized_baseline_design.md`) |
| `private_dominant` | All 13 → `partial` |
| `private_only` | All 13 → `private` |
| `iid_holdout` | All 13 → `iid_holdout` |

Benchmark names are unchanged across conditions — only structural attributes (h, cosine) vary. LLM providers do not observe benchmark types or real-world analog labels; they infer from score patterns.

**Calibrated `baseline` assignment (session 43, 8/3/2 ratio anchored to 2024–2025 history):** Safety Evaluation + Scientific Reasoning + Hard Coding as `partial` (SEAL-Safety / GPQA-Diamond / LiveCodeBench contamination-mitigated analogs); Adversarial Robustness (r12, Jan 2024, SEAL-Safety / HarmBench-private era) + Advanced Math (r24, Jan 2025, FrontierMath era) as `private`; remaining 8 as `public`. See `rough/randomized_baseline_design.md` for the full timeline anchor.

**Premium access (orthogonal axis; not activated in primary conditions):**

| Parameter | Scope | Real-world analog |
|---|---|---|
| `premium_pre_access` | Per (provider, benchmark) | FrontierMath-OpenAI pre-launch access: simulates N rounds of public-weight observations at t=0, sharpening the new provider's `inferred_weights[b]` prior beyond the global σ_prior |
| `premium_submissions_per_round` | Per (provider, benchmark) | SEAL-style eval-as-company: best-of-M scoring each round |

Reserved for future benchmark-sponsorship + eval-as-company ablations. Implementation notes: pre-access sharpens initial belief via simulated delta-rule updates before benchmark goes live; submissions-per-round applies standard extremum-of-M score inflation (`sigma/√samples × √(2 ln M)`).

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

- **Incident penalty:** Severity-weighted (minor: 0.01, moderate: 0.05, major: 0.10, critical: 0.20) with exponential decay over time (`weight × 0.70^age`, ~2.3-round half-life, max 10-round window); 2x if category matches segment sector. Scaled by `(1 + market_share^2)` -- the HHI contribution of a single firm, reflecting that dominant providers face greater scrutiny and reputational exposure per incident (grounded in scale-contingent regulatory obligations: EO 14110, SB 1047). Weights reduced ~33% in session 21 recalibration to prevent single-incident satisfaction wipeout while preserving meaningful differentiation.
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

**Budget scaling rationale:** The old design used `headroom ^ (1/diminishing_returns_rate)` which penalized capability-level proximity to the ceiling. This was replaced with two simpler mechanisms: (1) **sqrt budget compression** prevents runaway funding concentration from translating linearly to capability — 10x more funding does not yield 10x more capability due to coordination overhead, talent bottlenecks, and diminishing marginal returns on compute (Besiroglu et al. 2024, Epoch AI scaling); (2) **linear headroom** provides a gentle ceiling approach without the steep cliff of the old exponential formula. Together these prevent dominant-provider runaway without artificially capping leaders.

**Safety lever rationale:** Safety R&D has structurally different dynamics than capability R&D:
- **Diminishing returns** — easy wins (RLHF, basic red-teaming) come first; frontier safety research has uncertain and diminishing payoff
- **Stochastic efficiency** — red-teaming is discovery-based (some campaigns find critical issues, some find nothing); unlike compute-scaling where more FLOPS reliably improves loss curves
- **Execution inertia** — all portfolio allocations (rd, safety, product) use a 3-round rolling average, so shifts in safety investment take multiple rounds to fully materialize. This replaced a previous 2-round delivery lag to provide uniform inertia across all levers.

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

Vectors were recalibrated to a tighter spread (mean ~0.47–0.52) with higher agentic baselines (0.40–0.47) reflecting that the simulation's 40-round growth trajectory requires room for differentiation without starting from near-zero in any dimension. The old vectors (session 9) had wider spread and near-zero agentic; sqrt budget compression and linear headroom now handle convergence dynamics instead of relying on wide initial gaps.

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

Session 14 (2026-04-05) identified that the original OS design had a stack of ~10 compounding hardcoded advantages (safety_floor 0.03 vs 0.35, sanction exemption, audit gate exemption, switching friction ×0.5, rd_budget_floor=1.0, belief broadcast, safety erosion) that predetermined OpenCore's market dominance rather than allowing it to emerge. These were audited against PIMMUR's Minimal Control principle and restructured:
- **Removed:** sanction exemption, audit gate exemption, switching friction discount, rd_budget_floor guarantee
- **Narrowed:** safety_floor gap (0.15 vs 0.25, was 0.03 vs 0.35), cost_advantage (0.35, was 0.90)
- **Defaulted off:** belief broadcast, safety erosion (available as ablation flags)

5-seed heuristic test (seeds 7/12/42/88/103, 40 rounds): OpenCore averages ~28% market share (range 14-45%) with four different providers winning across seeds. Outcomes now vary meaningfully by seed.

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

`BenchmarkGroundTruth` (held by simulation, not the `Benchmark` dataclass) contains hidden `category_dimension_weights`, `noise_sigma`, and `samples`. The `Benchmark` dataclass is lean — `validity` field removed (was only used by now-removed weight-decay machinery). Published per round: overall score + per-category scores.

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

**Expanded pool:** 22 benchmarks defined in `BENCHMARK_POOL` (`actors/evaluator.py`). Dimension weights are **peaked**: specialized benchmarks load 0.75-0.85 on their primary dimension so that focused investment can drive scores toward genuine saturation (0.90+). Broad benchmarks (General Capability, Hard Knowledge) stay flat (primary ~0.35-0.40). Full pool with weights in `BENCHMARK_POOL` constant.

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

**Additional pool benchmarks (12):** Advanced Math (reasoning 0.85), Human Preference (communication 0.58), Hard Knowledge (broad), Clinical Reasoning (knowledge 0.65), Legal Reasoning (knowledge 0.60), Financial Analysis (knowledge 0.55), Multilingual Understanding (communication 0.55), Function Calling (agentic 0.40 + coding 0.30 — session-45 BFCL recalibration), Adversarial Robustness (safety 0.85), Web Navigation (agentic 0.72), Issue Resolution (coding 0.42 + agentic 0.38), Creative Writing (communication 0.82).

**Toggleable misalignment extension (`benchmark_misalignment_enabled: bool = False`):** When enabled, benchmark weights are initialized via interpolation toward a misaligned vector concentrating on automatable/measurable dimensions (reasoning-heavy, safety-light). Default off — natural benchmark structures already create sufficient Goodhart pressure.

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

Known asymmetry: heuristic selection is gap-driven (reactive to the consumer-need/coverage mismatch); LLM selection reasons from public-visible signals only and can be proactive in ways the heuristic cannot. This difference is the research finding, not a bug.

**LLM dynamic mode** uses `DYNAMIC_EVALUATOR_SYSTEM_PROMPT` (stewardship framing; inaction as default). No staff-capacity / pipeline block is surfaced — the N=2 pipeline cap described in earlier design docs was never implemented; the time-trigger provides all pacing.

**Internal validity:** `Pearson_r(score_rank, market_share_rank)` — updated each round when `evaluator_mode == "dynamic"`. Evaluator-internal only, never published; passed to the LLM as an observable signal but not used as a trigger.

**Condition preset:** `--condition dynamic_evaluator` (works in both `--mode llm` and `--mode heuristic`). The legacy `evaluator_mode="full_autonomy"` string and `dynamic_evaluator: bool` field were retired in session 31 (saved configs in `sandbox/experiments/llm/` were migrated in-place; the `__post_init__` shim is gone). Replays of any pre-session-31 config that still carries those legacy values will now fail loudly rather than auto-migrate.

**No apparatus vocabulary** in LLM prompts — saturation, validity, and Goodhart framing are never surfaced. The evaluator is addressed as "the team responsible for maintaining the AI evaluation leaderboard."

**Consumer market LLM mode** is optional and gated behind `consumer_llm_mode`. Default is heuristic-only. When enabled for organizations (`consumer_llm_organizations=True`), org segments use a PIMMUR-compliant vendor review brief (see Organizational Consumer LLM Mode section). Individual consumers remain heuristic-only by default — their decisions are routine and habitual rather than strategic.

### Evaluator-as-Company (`evaluator_as_company=True`)

Models evaluator conflict of interest (Leaderboard Illusion paper; cross-sector capture dynamics from credit rating agencies, financial auditing). Gated behind `evaluator_as_company: bool = False`.

**Three mechanics activate when enabled:**

**1. Best-of-N trial submissions.** Each provider chooses how many model variants to submit per round (1 to `max_eval_submissions`, default 10). Each extra submission costs `fee_per_submission` (default 0.03 sim units), deducted from R&D budget. Evaluator runs N independent scoring trials per benchmark; best score published. Selection bias from best-of-N with Gaussian noise: `E[max(X_1,...,X_N)] ~ mu + sigma * sqrt(2 ln N)`.

- **Heuristic mode:** `N = min(max_n, 1 + int((base_revenue + discretionary_budget) * 0.15 / fee))`. Affordability-gated by 15% of total resources.
- **LLM mode:** Provider outputs `"n_submissions": int` in planning JSON. Prompt frames it as a strategic cost/benefit tradeoff.
- **K-lag fee gating (session 41):** On rounds where no benchmark produces a fresh score (fully-frozen K-lag rounds under `private_only` / `iid_holdout`), fee is waived and `premium_revenue` is zero. Best-of-N only runs on publish rounds, so the fee only fires when the service is rendered. Checked via `EvalEcosystemSimulation._any_benchmark_publishes_fresh(round_num)`.

**2. Early access.** Premium subscribers start closer to the actual holdout-scoring target at benchmark introduction. The blend uses the noisy-public-weights prior (session 38 default, `normalize(public_weights + Normal(0, σ_prior))`) as the base and pulls it toward the benchmark's `holdout_category_dimension_weights`:

```
premium_init = (1 - factor) × noisy_public_prior + factor × holdout_weights
```

`factor=0` matches non-subscribers (no advantage); `factor=1` gives exact holdout knowledge at introduction. On public-type benchmarks where `holdout_category_dimension_weights is None`, the blend falls back to public weights and collapses to a weak sharpening of the noisy prior — i.e. eval-as-company sells private-benchmark access advantage specifically, consistent with the SEAL business model. Justification: paying subscribers have implicit bias-variance knowledge (better sense of where their models overfit), so start with a holdout-target-informed prior without extra effort. Default `early_access_factor=0.5` — aggressive under new semantics; revisit before activation.

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

Population weights are adoption-weighted market shares, grounded in NBER Bick/Blandin/Deming 2024 occupation-level AI adoption data, Stanford AI Index 2025, and McKinsey State of AI 2025. `enterprise_hr` (session 40b) is anchored in EEOC 2024 algorithmic-discrimination guidance + NYC Local Law 144 + EU AI Act Annex III §4. See `docs/references.md` for full citations. Raw pop weights sum to 1.04; `create_default_segments` normalizes to 1.0.

Population-weighted average ≈ `{reasoning: 0.18, coding: 0.12, knowledge: 0.18, safety: 0.17, communication: 0.27, agentic: 0.09}` post-40b (safety ticks up ~0.007 from `enterprise_hr`'s safety-0.35 weight). `agentic` intentionally low at simulation start (2023).

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

This replaces the earlier dot-product spec (`dot(need_weights, benchmark_public_category_weights)`) — no `benchmark_public_category_weights` data structure exists. Tag-matching achieves the same directional effect with simpler, more auditable parameters.

### Switching

Proportional sigmoid-based switching within each segment. Two independent triggers:

1. **Dissatisfaction:** `gap = believed_quality - satisfaction`. Fires when gap > 0; probability = `sigmoid(10 * (gap - threshold))` where `threshold = switching_threshold + switch_cooldown`.
2. **Opportunity:** `improvement = blended_score[alt] - blended_score[current]`. `opportunity_threshold = switching_threshold * 0.5 + switch_cooldown`.

**Switching cost** acts as a damper on the fraction that follows through: `cost_damper = 1.0 - min(0.9, switching_cost * (1 + retention_bonus))`. Product investment retention bonus (`retention_bonus`) connects provider product lever to consumer stickiness.

**Post-switch cooldown** replaces the old `tenure_bonus` and `decision_delay` parameters. After a switch, `_switch_cooldown` spikes to 0.20 and decays 0.5x per round (~2-round half-life). This naturally models institutional inertia without a binary gate or separate parameter.

**Removed (session 23):** `integration_friction` (redundant with switching_cost), `tenure_bonus` (subsumed by cooldown + EMA smoothing), `decision_delay` (subsumed by cooldown).

### Dynamic Consumer Market

When `dynamic_consumer_market=True` (the **default** since session 27, and the dataclass default since session 31), enterprise segment `market_fraction` grows from ~25% to ~55% over the simulation via a logistic curve, modeling the real-world shift from consumer-dominated (Q1 2023) to enterprise-dominated (mid-2025) AI market. Individual segments shrink proportionally. Within each class, relative proportions are preserved. The inverse ablation is `--condition static_enterprise_size`, which sets it back to `False`.

```
enterprise_share(t) = start + (end - start) / (1 + exp(-0.25 * (t - midpoint)))
```

Default: `enterprise_share_start=0.25`, `enterprise_share_end=0.55`, `enterprise_growth_midpoint=18`. Grounded in McKinsey State of AI (2024-2025), Menlo Ventures (2024-2025), Stanford HAI (2024-2025). See `docs/references.md`.

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

**Base rate:** 20% per provider per round (session 39b recalibration — raised from 10% to make safety lever observable against market-share confound). Multiplied by factors:

| Factor | Formula | Direction |
|--------|---------|-----------|
| Safety investment | `1 - (portfolio["safety"] × 1.5)`, clipped ≥ 0 | Higher safety allocation → lower prob |
| Market share (exposure) | `(0.3 + market_share × 1.5) × sqrt(total_market_size)` | Larger market → higher prob |
| Incident history escalation | `+0.02 per prior major/critical in last 15 rounds, cap +0.10` | Past harm → elevated future risk (ages out) |
| Active sanction | `0.75×` while sanctioned | Regulatory oversight → reduced prob |

Floor at 2% (session 39b, from 5%). Capped at 50% per round (session 39b, from 40%). See Session Changelog for the validation that led to these values.

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

**Sector propagation (session 40b correction):** Each category has an `affected_sectors` list. Segments whose `use_case` or `consumer_type` is in that list get a 2× satisfaction-penalty multiplier. Prior to session 40b, 5 of 7 sector strings did not match any `USE_CASE_PROFILES` key — `misinformation` and `misuse` propagation were effectively dead. Corrected mapping:

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

**Empirical calibration (see `docs/incident_path_dependence.md`):** Cross-sector survey validates that critical incidents can cause 30+pp market share swings: Boeing 737 MAX (39pp delivery share drop), Avandia (34pp within-class), Cruise robotaxi (50+pp to permanent exit). Session 21 recalibration reduced severity weights ~33% and halved history escalation (+0.02/prior, cap 0.10, 15-round aging) to prevent death spirals while preserving meaningful differentiation. 5-seed validation showed 3 different winners across seeds (vs 4 previously), with strategic advantage now surviving moderate incidents but critical incidents still reshaping markets. Key calibration nuances from the evidence:
- **Incident type matters:** Physical harm + regulatory shutdown produces permanent exits; pure reputational/trust incidents produce ~0pp shifts in AI markets (trust-behavior gap). Media headline competition (critical=guaranteed, major/moderate=pooled with weighted sampling) partially captures this: critical incidents always dominate news, while moderate incidents may be crowded out by other stories.
- **Recovery is slow and fragile:** Boeing partially recovered in 3 years but was reset by a second incident. Decay half-life (~2.3 rounds) remains unchanged; the reduced severity weights lower the peak penalty rather than extending the tail.
- **"Liability of good reputation":** Market leaders are MORE vulnerable to incident shocks (Rhee & Haunschild, 2006). The `(1 + market_share^2)` scaling captures this.
- **Contagion vs. competition:** Some incidents damage the entire sector (COX-2 class destruction after Vioxx), not just the affected firm. Not currently modeled (deferred).

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

Threshold values are config parameters — flagged for sensitivity analysis.

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

Media independently covers leaderboard changes and score leaders — no score-delta boost needed in `public_comms` weights. Score-driven visibility flows from media to consumers via the exploration pathway: big score jumps generate media coverage (provider_attention + sentiment), which increases per-provider exploration rates for high-trust segments and biases redistribution toward positively-covered providers. This subsumes the "score-delta buzz effect" without a separate mechanism.

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
- **Funder herding mechanic** — explicit modeled herd behavior dropped; herding emerges naturally from funders observing each other's allocations and updating `believed_provider_quality` accordingly

---

## Calibration Notes

### Open Source Capability Jump Calibration

The OS provider has two update modes: slow continuous R&D gain (every round) and episodic step-change capability jumps (stochastic, representing a new frontier OS release entering the market). Jump magnitude and frequency should be calibrated empirically: examine OS model performance trends on tracked benchmarks (e.g., Epoch AI's Notable AI Models dataset / capabilities index, Hugging Face Open LLM Leaderboard history, HELM benchmark trajectories). Look for seemingly sudden score jumps — corresponding to major releases like LLaMA 2 → 3.1 → DeepSeek R1 — and study: (a) how large the capability jump was relative to the prior trend, (b) how frequently jumps occur, (c) whether jump magnitude correlates with inter-release interval. These empirical distributions then parameterize `jump_magnitude` and `jump_probability`.

### Ecosystem-Level Metrics (Deferred)

Metrics like `score_reliability` (Pearson-r of scores vs. satisfaction) are detectable only through triangulation across multiple actors' partial views — no single actor has the full picture. How these are computed, what is logged vs. published, and how actors respond to their respective fragments requires a dedicated design discussion. Deferred for now.

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

## Calibration (Pending)

Items requiring simulation output before values can be finalized:

- **Mandatory safety floor**: working estimate 0.35; confirm against safety trajectories in early runs
- **Empirical calibration**: initial capability vectors against `external-validation/` data
- **`focus_level[b]` baselines**: 24 values at round 0 (6 providers x 4 benchmarks); grows to 60 by round 28. Qualitative anchors in Default Provider Profiles above; numeric values require calibration
- **R&D gain scaling**: absolute magnitude of `rd x target[dim]` per round; confirm against capability growth trajectories
- **`sigma_base`**: noise scale for `consumer_signal`; calibrate so signal is informative but not precise at realistic market shares
- **`benchmark_orientation`**: fixed at 0.80 for all providers (uniform); adjustable mode available as ablation
- **Media parameters**: narrative transition thresholds, sentiment weights per trigger type, `saturation_threshold`
- **Funder parameters**: `funder_pool` size per type, `revenue_per_share` scalar, scoring formula weights
- **Regulator parameters**: exact threshold values per preset (EU/Balanced/US)
- **Consumer state**: `running_perceived_quality` initialization value per segment per provider
- **Incident severity/recovery calibration**: Current critical penalty (0.30) and decay (~2.3-round half-life) produce 30+pp swings, consistent with Boeing/Avandia/Cruise evidence. Consider: (a) slower decay for critical incidents (half-life 4-5 rounds), (b) incident-type gating (physical harm vs. reputational), (c) contagion mechanic where sector-wide incidents hit all providers. See `docs/incident_path_dependence.md`.

---

## Experiment Seeds

30 unique 3-digit seeds used for all heuristic baseline runs. Generated once and fixed for reproducibility. Stored in `SEEDS.txt`.

```python
import random
random.seed(42)
seeds = sorted(random.sample(range(100, 1000), 30))
```

Seeds: 125 127 130 132 189 195 204 214 242 303 323 328 338 350 381 529 532 617 658 674 704 716 754 765 792 818 833 854 858 859

---

## Session Changelog

Entries preserve the *why* behind recent structural changes. Current state is reflected in the architecture sections above; this changelog is for auditing how we got there. Older sessions are summarized in single bullets; see `SESSION_HANDOFF.md` and project memory for full detail.

### 2026-04-23 — Session 49d: provider identity redesign (all 6) + benchmark-type context + seed=2 flag-ledger revision

**All six provider identities rewrote** (`scripts/run_experiment.py`) grounded in real-world public positioning documents (OpenAI Charter + "Planning for AGI and Beyond"; Anthropic Core Views on AI Safety; DeepMind About; Meta AI homepage; DeepSeek public positioning via Wikipedia/SCMP/CNBC; generic VC-funded AI startup profile). **Why:** previous identity text contained multiple behavior prescriptions (e.g., Apex "safety-conscious, principled" → moral-licensing rationalization vector producing rank-last safety allocation across seeds; Orion "aggressive, product-focused" caricature; OpenCore "minimal safety investment / no guardrails / benchmark-optimizing" → coaching the very behavior the sim studies). New identities are mission/thesis/structural only — describe role constraints without prescribing allocation choices. PIMMUR-clean across all 6 (re-audited): no decision-rule language, no pre-labeled outcomes, no coupling to competitor behavior. Symmetric "capital-intensive" / PBC structural conditions acknowledged. Behavior-prescription-free identity prompts let emergent LLM reasoning produce market dynamics. Heuristic mode unaffected.

**Benchmark-type context added to provider planning prompt** (`src/llm.py` — user-prompt legend at `# Evaluation Results` header + one-sentence mechanism description in all 3 `PROVIDER_PLANNING_SYSTEM_PROMPT*` variants). Factual description of `public`/`partial`/`private` mechanism (K=3-round reporting lag, holdout-vs-blended weights) without prescribing strategic response. Rationale: pre-fix only 2% of provider traces cited privacy mechanism in private_only condition; LLM providers were benchmark-type-blind. Adding mechanism legend enables measurement of emergent privacy-strategic reasoning without coaching the response.

**D1/D2 plot autogen** (`src/plotting.py`): per-benchmark dumbbell (invoking `scripts/plots/per_benchmark.dumbbell_from_df`) + new `allocations_over_time.png` (invoking `scripts/plots/portfolio.plot_allocations_mean` — solid R&D, dotted safety, bold market-share-weighted-mean overlay). Both now fire automatically alongside the 5 pres_slide plots at end of every sim run. `plot_allocations_mean` added as a new function in `scripts/plots/portfolio.py`.

**Design-flag ledger revised via seed=2 evidence** (partial 31-32 round runs at `_llm_apr23_v1/llm/{baseline_seed2,eval_as_company_seed2,initial_uniform_cap_seed2}/`): **Orion overshoot is seed-fragile** (78% at seed=1 → 32% at seed=2, collapsing further not rebuilding — B2 Orion-dampener concern killed). **Genesis chronic undershoot is partially seed-fragile** (5-7% at seed=1 → 17% at seed=2, within real-world range — distribution-advantage limitation softened). **Apex archetype drift is seed-robust** (20% safety / rank 5-6 of 6 across seeds and starting conditions — motivated the identity rewrite). **`initial_uniform_cap` produces OpenCore dominance** (48.7% market share when capabilities start uniform) — capability-vector asymmetry is the load-bearing lever for market structure, more than LLM strategy or prompt differences. **Contra Agent-C1 earlier finding**: eval_as_company Apex-win at seed=1 was NOT stochastic incident-draw — replicates stronger at seed=2 (60.4% vs 31.1%), so session-49b retune claim IS defensible.

**Breaking changes:**
- LLM provider planning prompts changed shape (all 6 identity blocks + benchmark-type context). Prior LLM runs reason from materially different identity prompts; session-28/29/32/49c LLM traces not directly comparable on reasoning content.
- Heuristic mode unaffected.

**Post-identity 40r validation run** (`_llm_apr23_v1/llm/baseline_seed2_postid/seeds/seed_2/`, seed=2): 5-agent analysis found zero regressions (0 fallbacks, clean reasoning, regulator plumbing still 13/14 targeted) and multiple positive effects: **VC-VC correlation dropped further to mean r=0.20** (session-49c softening was TechVentures-only; full identity rewrite across all 6 providers dropped herding further), **OpenCore unexpectedly emerged as safety leader** at R39 (44.2% safety allocation — highest in ecosystem) confirming the "no guardrails / minimum safety" coaching removal worked. **Apex identity fix is partial/time-limited**: works during incident-response phase (R10-R25 sustains 27% safety), degrades under sustained share-pressure late-run (R39 back to 14.6%). **Orion-overshoot concern revived**: despite 9 regulator interventions targeting Orion correctly, Orion rebuilt from 33% (R30) to 60.6% (R39) — validating a narrower version of the session-49c B2 "post-fix regulator can target but doesn't persistently suppress recovery" concern. **Identity propagates via public_comms into funder reasoning** (OpenCore's new "research-oriented" framing cited by OpenResearch_Foundation; Orion's "AGI-ready" language appears in TechVentures reasoning). **A1 benchmark-type context lands weakly** — only R1-R4 citations, no ongoing strategic anchor; emergent finding that LLMs don't reason about privacy mechanism as strategy even when surfaced.

**Media + incidents calibration tweaks (session 49d end):**
- *Media headline budget raised* `_media_sample_size` 4 → 6 in `src/actors/media.py`. Rationale: leaderboard-related events were ~10% of media flow in baseline, crowded out by provider public_comms + funder deals. Higher cap lets more newsworthy events survive weighted-sampling.
- *Two new leaderboard headline triggers* in `src/actors/media.py`: **benchmark-milestone crossings** (first provider to cross 70/80/90% on any benchmark — fires weight=2.0 headline), and **rival-closes-gap** (when #1→#2 gap narrows by >0.008 in one round — attention boost goes to #2, the gaining provider, not the incident-hit leader). Grounded in interview finding that benchmarks function as marketing vessels + that competitor panic becomes PR for the rival. Dry-replay on baseline seed=1 would add ~22-26 headlines/40r.
- *Incident exposure-multiplier floor* `incidents.py:251` lowered from 0.5 → 0.3. The original floor over-taxed small providers (OpenCore at 5% share received 2.7× Orion-per-round incident rate ratio vs a more realistic 4-6× share scaling). Rationale: 0.3 retains a baseline "even a niche provider faces some scrutiny" floor without dominating; 0.02 final floor at `incidents.py:285` still protects tiniest providers from zero-incident pathology. Small provider incidents drop ~35% per round; mid-share (20-40%) drop 10-20%; dominant (60-70%) drop ~15%. All prior LLM runs (including session-49 evidence base) used 0.5 floor — new Tier 1 runs will show slightly different incident distributions.

### 2026-04-23 — Session 49c: evaluator prompt audit + plumbing bugfix + LLM smoke

**Regulator intervention target plumbing fix** (`src/simulation.py:1925`, `src/actors/funder.py observe()`). Pre-fix: aggregated `regulator_data["interventions"]` dropped the `provider` field from the regulator's intervention object; every intervention rendered as `details={}` with no target across all downstream consumers. Downstream, the session-49 funder `_recent_interventions` tracker read `"target_provider"` (never populated) and reported system-wide for every intervention. **Impact in baseline_40r smoke:** all 14 regulator interventions over 40 rounds aggregated as `system-wide` even when regulator reasoning cited Orion by name. Fix: aggregation now includes `"provider": intervention.get("provider")`; funder observe falls through `provider → target_provider → details.target_provider`.

**LLM dynamic evaluator prompt audit landed** (session-48 playbook). Files: `src/actors/evaluator.py`, `src/llm.py`, `src/simulation.py`. Changes: **(a)** new `_dynamic_llm_decisions` list + `_retirement_reasons` dict on Evaluator (persisted via save/load); **(b)** `retire_benchmark(reason=...)` signature — auto-refines to `"saturation"` when auto-selecting a saturated benchmark, otherwise `"auto-retire at cap"`, LLM path passes `"llm: <tail>"`; **(c)** `get_llm_observation` dynamic-mode branch now returns `prior_decisions` (last 3), `introduction_metadata` (round + reasoning per active benchmark), `retired_benchmarks_enriched` (name, round, reason), `active_regulations`; **(d)** `DYNAMIC_EVALUATOR_SYSTEM_PROMPT` rewrite — "Triggers that justify action" block replaced with descriptive "Signals to watch for" (F-soft reframe, session-48 coaching pattern); "Correct when" phrasing dropped from `none` option; "A good evaluation suite..." value-judgment sentence deleted; **(e)** user prompt: new `Your Prior Quarterly Decisions` section (memory channel — previously absent; biggest structural gap fixed), enriched `Previously Retired` + `Active Benchmarks` with introduction/retirement metadata, new `Active Regulations` section, `[SATURATED]` label dropped (saturation now readable from Score Movement numerics only), media keyword filter dropped (raw headlines last-4); **(f)** `simulation._dynamic_evaluator_decision` writes reasoning to `introduction_history[-1]` + logs decision to `_dynamic_llm_decisions`. 10-round anthropic smoke (dynamic_10r): 0 fallbacks; R8 evaluator reasoning explicitly references "Agentic Tasks (introduced Month 4)" — memory channel validated end-to-end.

**TechVentures VC identity language softened** (`src/llm.py FUNDER_IDENTITY_BLOCKS["vc"]`): `"Concentrated bets on high-conviction winners are common"` → `"Selective, high-conviction allocation is common"`. Observed in baseline_40r: all four VC/corp funders piled into Orion+Genesis, with zero mentions of Apex in any LLM VC reasoning. Pre-session-49 reference run: same seed, 3/3 VCs explicitly named Apex with asymmetric-upside rationale. vcfix_10r paired-seed run at seed=1 confirms: Apex jumps from 4.7% → 31.7% of round-2 VC funding share; both VCs now cite Apex as "#2 pick" with Azure-partnership rationale. **Word change only; no coaching added.**

**Smoke runs landed:** `sandbox/experiments/session49_smoke/llm/{baseline_40r,dynamic_10r,vcfix_10r}/`. Baseline_40r hit Orion 50.5% / Apex 21.3% at R40 — tracks real-world closely, but via a single catastrophic R36 incident that reversed an Orion 79.6% peak. 5-agent comprehensive post-run analysis found design flags beyond plumbing: Apex safety archetype drifted to 14% (lowest of 6, from starting 30%), Genesis chronic undershoot (5-7% vs real-world 10-15%), VC-VC co-investment r=0.923, regulator plumbing bug (fixed this session).

**Breaking changes:**
- Pre-fix LLM regulator interventions recorded with `provider=None`; any analysis of `regulator_data["interventions"]` targeting specific providers is unreliable pre-fix.
- LLM evaluator dynamic-mode prompt shape changed. Prior session-28/29/32 LLM evaluator runs reasoned from materially different prompts; reasoning-trace content not directly comparable.

### 2026-04-22 — Session 49: funder recalibration (cooldowns, roster, availability curve, bug fix)

**Source:** `docs/ai_corporate_funder_research.md` (timeline of corporate AI funding 2020–Apr 2026). Full calibration provenance in `docs/funder_calibration.md`.

**Cooldowns recalibrated** (`scripts/run_experiment.py`): VC 2–3→4, corporate 3→7, gov 4→10, foundation 3→6. Anchored to per-provider event rates (Anthropic ~4mo, OpenAI ~3–4mo for corporate events; frontier Series rounds ~8mo for VC) adjusted by sim roster-to-real aggregation factors (corporate 4:1, VC ~2:1 on leads, gov 5:1, foundation 3:1).

**Per-provider corporate rotation rule deleted** (`src/actors/funder.py:_plan_corporate`). Previous logic skipped a provider for 3 rounds after allocating to it. Contradicted research data (zero strategic corporate exits 2020–2026). Corporate funders now re-evaluate top 2–4 partners each decision without artificial exclusion.

**Second corporate funder added** (`IndustryPartners_AI`, `scripts/run_experiment.py`). Previously 1 corporate (StratCorp_AI); now 2. Minimum needed for the aggregation math in the cooldown calibration to work cleanly. Name deliberately generic — no pre-assignment of provider partnerships.

**Availability curve on capital deployment** (`src/actors/funder.py`, new `_availability()` method, new params `capital_growth_rate=0.07` and `sim_total_rounds`). `total_capital` is now the sim-window integral, released geometrically at 7%/month compound (empirical anchor: 2.3× YoY corporate equity 2023–2026). Per-decision deployment = `max_round_deployment × availability(r) × total_capital`. Availability sums to 1.0 over sim length. Ramps ~14× from round 0 to round 39.

**`total_capital` re-anchored to empirical $198B ecosystem integral** (`scripts/run_experiment.py`). Previous pool size ~$5.5B; new ~$193B split by sim-funder share of 2023–2026 disclosed frontier funding. Corporate dominates (66%) matching real distribution. Replaces the prior stakeholders.md claim of "relatively inelastic" pool.

**FUNDER_BUDGET_SCALE unchanged at 1e-9** (`src/simulation.py:33`). Mean-preserving by construction: `total_capital × mean(availability) = total_capital / N`, which equals previous per-round pool for corporate at midpoint. Early sim deploys ~0.2× previous per-round capital; late sim ~2.8× (~3.7× range in sqrt-damped capability gains). VC/gov/foundation see modest below-previous mid-sim contribution (0.15–0.5× previous) — reflects empirical fact that corporate dwarfs other types by 2025.

**LLM funder renormalization bug fix** (`src/llm.py:1671–1677`). Previously silently scaled *up* when LLM under-deployed (violating explicit "hold in reserve" prompt instruction). Now caps at total_capital; never scales up. Affects LLM-mode funder deployments materially — prior LLM baselines no longer directly comparable on provider-capability-growth figures.

**LLM funder prompt audit (parallel thread, session-48-playbook):**
- Identity moved from per-round user prompt into system prompt via new `FUNDER_IDENTITY_BLOCKS` (one per funder type) + per-funder `mission_statement` appended. Ends per-round identity re-injection pattern.
- Static "Funder types:" 4-item menu dropped from system prompt (~430 chars/call × every month × every funder).
- New prompt sections: `Regulatory Context` (active regulations + `_recent_interventions` tail), `Other Funders This Month` (peer allocations, top-3 per provider by amount), `Your Funding Portfolio` (cumulative per-provider + last-round — replaces flat 3-row history list).
- Leaderboard rows now show 2-round score delta alongside last-round when history is deep enough.
- Media `Overall media tone` label dropped — raw headlines only (same coaching-removal pattern as session-48 regulator).
- Cross-round reasoning truncation raised 120→250 chars (prior cap mangled trajectory).
- Softer reserve-directive phrasing ("You may fund any subset... hold in reserve"), drops "1-3 providers" concentration anchor.
- New `_recent_interventions: [(round, type, target), ...]` tracker in `Funder.observe()`.
- **Proportional pruning window** `max(3, funding_cooldown)` for both `_recent_incident_counts` and `_recent_interventions` — long-cadence funders (gov=10, foundation=6) now retain enough history to see signals accumulated between their decisions. Prior 3-round fixed window left gov funders blind to 70% of their decision gap.
- `simulation.py:_setup_funders` hard-fails on empty `mission_statement` when `llm_mode=True` (guarantees identity differentiation across same-type funders).

Files: `src/llm.py` (`FUNDER_PLANNING_SYSTEM_PROMPT` rewrite + `FUNDER_IDENTITY_BLOCKS` + `create_funder_planning_prompt` + `llm_plan_funding` signature), `src/actors/funder.py` (`observe()` interventions tracker + proportional pruning, `_plan_llm` ctx assembly), `src/simulation.py` (mission guard).

Composition after: user prompt 2.6k chars (vs 1.7k before — +0.9k from 2 new info sections); system prompt 0.85k chars (vs 1.05k — menu removed). No section exceeds 22% of user prompt. All changes are either role-definition, information-additive, or coaching-removal; no new scaffolds, epistemic assertions, or decision rules introduced. Role-definition vs coaching distinction explicitly audited — behavior-prescriptive language in identity blocks retained as definitional archetype (not studied as emergent outcome).

**Eval-as-company conservative retune** (`scripts/run_experiment.py:632-645`). Session-49 funder recalibration attenuated the eval_as_company HHI-delta vs baseline by ~65% (+0.073 → +0.026 at N=30 heuristic). Two parameters adjusted to restore detectability without breaking empirical plausibility: `max_eval_submissions` 10 → 12 (still well below Meta's 27-variants anchor) and `early_access_factor` 0.5 → 0.7 (the prior default was flagged as "aggressive under new semantics; revisit before activation" in the Evaluator-as-Company section). Post-retune HHI delta is +0.041 (p=0.20 at N=30, directional only); gap / score_noise / dim_mismatch channels preserved significance. Paper App H claim narrows to information-quality degradation; market-concentration channel remains directional. Rerun at `sandbox/experiments/heuristic_session49/heuristic/eval_as_company/` (30 seeds).

**Breaking changes:**
- Pre-session-49 heuristic baselines use 5.5B total pool + static release; new regime has 193B with time-varying release. Mid-window mean preserved for corporate, reduced for VC/gov/foundation.
- Pre-session-49 LLM funder runs affected by renormalization bug (forced full deployment). Not comparable to post-fix LLM runs on provider funding magnitude.
- LLM funder planning prompt shape has changed (parallel-thread audit). Prior LLM funder reasoning traces reason from materially different prompts; session-41/28/29 LLM funder baselines not directly comparable on reasoning content or allocation distribution.
- Corporate per-provider rotation rule removed — any analysis relying on that behavior invalidated.
- eval_as_company default parameters shifted (`max_eval_submissions` 10 → 12, `early_access_factor` 0.5 → 0.7). Pre-retune eval_as_company heuristic and LLM runs not directly comparable on concentration magnitudes.

### 2026-04-20 — Session 42: heuristic policy rewrite (F1) + cadence reconciliation + per-benchmark gap reframing

**F1 — `_plan_heuristic` rewrite (`src/actors/model_provider.py:508-579`, `src/simulation.py:808-830`):**
Removed unconditional profile-string-based modifiers (the `if "safety" in profile_lower: safety += 0.05` ratchets) that were firing every round and saturating providers at deterministic end-states. `safety_last` std across 1,500 runs was 0.000 for Apex and Orion — blocking all safety counterfactual analysis. New policy preserves incident-pressure mechanism and adds 3 universal observation-driven rules: **Rule A** (share trend: 3-round Δshare < −0.02 → product +=0.03, rd −=0.03; Δshare > +0.02 → rd +=0.02, product −=0.02); **Rule C** (CRISIS narrative → safety +=0.04, rd −=0.04); **Rule D** (own-targeted recent interventions → safety += min(0.06, 0.02·count)). Provider identity now comes from initial portfolio + innate cap vector only; no per-policy profile bias. Safety cap raised 0.55→0.70 since ratchet is gone. Added 3 ctx signals in `_get_provider_ecosystem_context`: `own_share_history` (last 5 rounds), `narrative_state`, `own_recent_interventions`. LLM mode untouched.

**Validation (1,500-run re-baseline, same seeds 1000-1029):**
- Apex `safety_last` std 0.0000 → 0.187; Orion 0.0000 → 0.149. Variance unlocked across all providers.
- **Regime shift**: leader-by-share flipped Mirage 47% → 0.9%; Orion 18% → 64%. Prior Mirage-dominance confirmed as policy artifact of profile ratchets.
- Gap more negative (−0.057 → −0.145) and HHI up (0.27 → 0.56) across all 5 privacy conditions. Satisfaction 0.62 → 0.75.

**Cadence reconciliation to canonical 4** (was spread across 3/4/5/6/7/8 in 10 locations): `src/simulation.py` (cooldown default 5→4; interval already 4), `src/actors/evaluator.py` (init default 7→4, deserialization default 8→4), `scripts/run_experiment.py` (SIMULATION value 5→4; fallbacks 6/4→4), `docs/stakeholders.md` (cooldown doc 3→4), `overleaf/appendix/A_architecture.tex` (schedule rounds 0/5/10/15/20/25/30 → 0/4/8/12/16/20/24).

**2 new structural ablations** (`run_experiment.py:_STRUCTURAL_CHOICES` + `_apply_structural_overrides`): `cadence_static` (sets `benchmark_sequence=[]` — only 4 initial benchmarks, "fixed benchmark era" counterfactual); `cadence_every_8` (cooldown=8 — pre-2023-era slower release rate). Default cadence=4 stays as `none`. Smoke-tested; 450 heuristic runs queued but unexecuted. Matrix becomes 5 privacy × 12 structural × 30 seeds = 1,800 if fully re-baselined.

**`fee_per_submission` default 0.03 → 0.05** (`src/simulation.py:193`) — aligns `SimulationConfig` default with calibrated session-18 value that `run_experiment.py` was overriding. Structurally eval-as-company was already correct.

**Per-benchmark gap reframing** (analysis-only; not a sim change). Replaced scalar `score − satisfaction` with per-benchmark × per-provider `score_b − matched_sat_b_aligned` where matched = weighted avg of (cap · need_weights_s) across segments × alignment(cdw_b, nw_s) × size. Decomposed into clean (pure capability × weight mismatch) and full (incl. cost_bonus + incident_penalty). Finding: 8/10 benchmarks have positive gap (overpromise); Agentic Tasks is −0.21 outlier because cdw heavily weights agentic (0.75) but capability stays low (0.26) — no heuristic rule invests there. Privacy mechanism IS visible at per-benchmark level (gaps compress toward zero under `private_only`) — aggregate scalar averaged it out. Validates session-38 claim. Paper figures 1-3 drafted at `sandbox/experiments/heuristic_apr19_postF1/plots_story/`.

**6 LLM diagnostic runs** (anthropic API, seed 2026, 30 rounds): `baseline`, `private_only`, `baseline × initial_uniform_allocation`, `baseline × no_regulator`, `baseline × no_incidents`, `fixed_public`. Key findings: (a) regulator IS load-bearing in LLM (removing it: Apex share 0.62→0.16, Orion 0.07→0.65) — the heuristic no-op is a heuristic-specific weakness, not a sim-design failure; F2/F3/F4 scope reduces to "port LLM-mode responsiveness into heuristic Rules"; (b) `fixed_public` at N=1 validates aging/overfitting hypothesis — mean |gap| on 4 shared benchmarks +61% vs baseline (0.015 → 0.024); (c) `bo_mean_last` pinned at 0.800 in LLM mode too (mode="fixed" is the default across sessions 38, 39, 42) — session-38 gap collapse mechanism operated via `inferred_benchmark_weights` delta-rule drift, not bo adjustment; (d) `initial_uniform_allocation` LLM run: providers DO drift to differentiated portfolios within 30 rounds (Apex safety 0.31, Orion 0.15) but Orion still wins via capability moat — confirms R4 (capability recalibration) as prerequisite for any "equal start" story.

**Paper — Appendix A updated**: schedule table rounds shifted to cadence=4 (0/4/8/12/16/20/24); new "Schedule calibration" paragraph maps each sim benchmark to its real-world analog release date (MMLU Sep 2020 through LiveCodeBench Mar 2024 / RULER Apr 2024) and notes the implicit ~1 round ≈ 2 months conversion.

**Agentic Tasks cdw recalibrated** (`scripts/run_experiment.py:200` SIMULATION.benchmark_sequence + `src/actors/evaluator.py:107-123` BENCHMARK_POOL): public agentic weight 0.75 → 0.48 with the rest of the profile aligned to paper Appendix A (reasoning 0.25, coding 0.19, communication 0.07). Holdout agentic 0.60 → 0.38 with proportional redistribution, preserving cos(public, holdout) ≈ 0.98. Reason: 0.75 agentic was too narrow for SWE-bench/BFCL-style analog (those benchmarks measure agentic + coding + reasoning, not pure agentic) and created a spurious −0.21 per-benchmark gap outlier driven by the mismatch between cdw and what even agentic-aligned consumer segments weight. **Breaking:** pre-session-42 per-benchmark gap figures for Agentic Tasks not comparable to post-42 runs. `heuristic_apr19_postF1` batch was generated with old weights; re-baseline needed if Agentic Tasks is to be included (currently excluded as outlier). 8 of 10 other benchmarks also drift between code and paper (Coding Eval, Hard Coding, Long Context); reconciling deferred to follow-up session.

**Plotting consolidation** (Phase 1 + 2): `scripts/plots/` package created with TOC README; 18 legacy `scripts/plot_*.py` + `scripts/aggregate_*.py` + 4 sandbox scripts migrated into `scripts/plots/`, `scripts/plots/paper/`, `scripts/aggregate/`. 3 prototypes archived to `scripts/archive/`. Output conventions: `output/paper/`, `output/analysis/<subject>/`, `output/diagnostic/`. Invocation pattern: `python -m scripts.plots.<module>`. Documentation at `scripts/plots/README.md`. `fee_per_submission` default 0.03 → 0.05 (aligns SimulationConfig with session-18 calibrated value).

### 2026-04-20 — Session 41: eval_as_company minimal honesty fix + re-baseline validation

**Problem.** Three latent inconsistencies in `evaluator_as_company` code paths vs the session-38 holdout typology:
1. `_on_new_benchmark` early-access blend used `(1-factor) × uniform + factor × aggregate_true_weights` — overwriting the new noisy-public-weights prior (session 38) with a different blend, and blurring the public/holdout split that the new mechanic was specifically designed to preserve.
2. `fee_per_submission` was deducted every round regardless of whether any benchmark actually produced a fresh score. On K-lag private/partial rounds, providers paid for best-of-N that didn't run.
3. Same issue for `premium_revenue` accounting on the evaluator side.

**Fix (Option A — minimal honesty pass; `src/simulation.py`):**
- New staticmethod `_aggregate_holdout_weights(bm_gt)` — mirror of `_aggregate_bm_weights` that reads `holdout_category_dimension_weights` instead of `category_dimension_weights`. Returns `{}` on public benchmarks.
- New method `_any_benchmark_publishes_fresh(round_num)` — mirrors the K-lag gate in `evaluator.evaluate_all`. Used to gate eval_as_company submission fees.
- Early-access blend (`_on_new_benchmark`) rewritten: target is `holdout_category_dimension_weights` (falls back to public on public benchmarks); base is the existing `inferred_benchmark_weights[b]` set by `init_benchmark` (noisy-public prior). `factor=0` now means no advantage; `factor=1` means exact holdout knowledge at introduction. Consistent with the SEAL business model (sells private-benchmark access advantage).
- Fee accounting gated on `_any_publish = self._any_benchmark_publishes_fresh(round_num)`: `sub_cost` and `premium_revenue` collapse to 0.0 on fully-frozen K-lag rounds.

**Justification for Option A semantics.** Paying subscribers have implicit bias-variance knowledge (better sense of where their models overfit) → they arrive with a holdout-target-informed prior without extra effort. Avoids tuning an N-rounds-of-pre-access parameter.

**Not done.**
- Full benchmark-sponsorship mechanic (FrontierMath-style per-(provider, benchmark) pre-launch holdout access) — still spec-only in stakeholders.md §"Premium access"; not in code.
- `early_access_factor=0.5` default is aggressive under new semantics (50% of the way to exact holdout). Should revisit before any paper condition activates `evaluator_as_company`.

**Validation runs (session 41 re-baseline under session-39c incident formula + session-40b sector fix + session-41 eval_as_company fixes):**
- 50 heuristic runs (5 conditions × 10 seeds, baseline condition): gap stable at −0.05 ± 0.006 across all 5 privacy conditions, 13 incidents/run, `r(safety, incidents)` ≈ −0.45. No regressions vs pre-session-41 expectations.
- 3 LLM runs (anthropic baseline, seeds 125/127/130, 30 rounds, 0 fallbacks each): **gap flipped sign vs session-39c (+0.023 → −0.065 ± 0.012 across all 3 seeds; not seed noise).** LLM + heuristic now agree on gap sign and magnitude. Session-28/29 "LLM gaming cleaner" narrative (memory: `finding_llm_consumer_feedback_loop`) needs revisiting. Most likely driver: session-39c incident formula (incident count up ~65% in LLM runs). Session-40b sector fix secondary.
- 20 initial-condition-probe runs (`--structural initial_uniform_capability` / `initial_uniform_allocation`, 10 seeds each): **Apex's safety lead is ~100% capability-vector-driven.** Under `initial_uniform_capability`: Apex safety drops 0.82 → 0.66; leader distribution flips to Mirage:6 / OpenCore:3 / Spark:1. Under `initial_uniform_allocation`: Orion dominance strengthens (8/10 vs 6/10 baseline). Gap magnitude drops ~40% under uniform capability (emergent component of gap ≈ −0.03, vs baseline −0.05).

**External-validation pipeline executed** (first time end-to-end) on session-41 LLM baseline. Paper-quality signal: **reasoning rank-correlation Spearman ρ ≈ 0.90 (paired sim vs PWC real-world) across all 3 seeds (p ≤ 0.05 each).** Coding ρ ≈ 0.73 (marginal). Writing ρ ≈ 0.27 (does not validate — likely a PWC "writing" dimension mismatch; MMLU/HellaSwag-derived rather than communication-focused). Math n=0 (Advanced Math didn't enter active pool in any seed).

**Profile-anchoring finding (LLM actor_traces).** Profile-token reference rate varies 6× across providers: OpenCore 2.95 hits/round (100% of rounds); Spark 1.60 (92%); Mirage 0.93 (58%); big-4 closed-source 0.47-0.54 (33-38%). Driven by profile-string length disparity (8-38 words). OpenCore and Spark outcomes are doubly profile-determined (mechanical + narrative); big-4 outcomes are mostly mechanical. Redesign options catalogued as post-deadline memory (`future_work_provider_profile_redesign.md`): minimal structural facts / historical behavior / single-axis-asymmetry-fixed-length / null profiles + memory-only. Swap-ablation proposal included.

**Breaking:** none. All session-41 code changes live behind `evaluator_as_company=False` default.

**Deferred:**
- Commit pending — session-39 Tier-1 PIMMUR edits + session-40b Fix-B + session-41 eval_as_company fixes all uncommitted.
- Paper narrative update reflecting the LLM-gap-sign-flip (session 28/29 finding needs revisiting in Section 5 + Appendix H).
- Math validation (force Advanced Math into active pool).
- Provider profile redesign (post-deadline memory saved).
- Benchmark introduction cadence kept at 4-month default; unjustified empirically vs raw adoption (1.2 mo/event) but defensible under "research-guiding only" narrow filter (3.5-5 mo/wave). Documented as informal calibration in memory.

### 2026-04-19 — Session 40b: `enterprise_hr` use_case + incident sector-string correction

**Problem.** In `incidents.py` `CATEGORIES`, 5 of 7 `affected_sectors` strings did not match any `USE_CASE_PROFILES` key or `consumer_type` value. The 2× propagation multiplier at `consumer.py:645` never fired for `misinformation` or `misuse`, and was partially dead for `safety_failure` and `bias_discrimination`.

**Fix-A (sector-string corrections in `incidents.py`):**
- `healthcare_individual` → `healthcare`
- `government` → `government_agency`
- `consumer` → `individual`
- `enterprise_saas` → dropped (no SaaS-specific use_case; finance/legal/govt already over-represented)

**Fix-B (new `enterprise_hr` use_case in `consumer.py`):** closes EU AI Act Annex III §4 (employment) coverage gap. Properties: `consumer_type="organization"`, need_weights safety-dominant (0.35; rest: reasoning 0.20, knowledge 0.20, communication 0.18, agentic 0.05, coding 0.02), `compliance_requirements=[EEOC, non_discrimination, GDPR_art22]`, decision_delay 5, pop weight 0.04. Added to `ORG_FIELD_PRIORITIES`, `USE_CASE_POP_WEIGHTS`, `scripts/run_experiment.py` `use_case_profiles` list, and `plotting.py` `_USE_CASE_GROUPS["Operations"]`. Anchored in EEOC 2024 algorithmic-discrimination guidance, NYC Local Law 144 (bias-audit mandate), and EU AI Act Annex III §4.

**Validation (5 seeds × 30 rounds, baseline heuristic, paired prior vs post):**
- mean Δgap = −0.0015 (SD 0.0017); mean Δgap_h2 = −0.0011 (SD 0.0011); all 5 seeds preserve sign
- mean ΔHHI = +0.008 (SD 0.010)
- incident counts near-identical (−0.20 mean; one `misinformation` incident shifted across 5 seeds)
- provider share shifts: Apex AI (safety leader) +0.8pp, Mirage AI −1.1pp, others within ±0.1pp
- Decision rule (`consumer_redesign.md` §13): |Δgap| > 0.022 AND CI-crosses-zero → halt. Passes with margin.

**Breaking:** pre-40b heuristic runs have mostly-dead sector multipliers. Any cross-condition incident figure that depends on per-category propagation requires re-baseline under the new sector strings. Session-39c's incident formula re-baseline (see below) already required a fresh run, so 40b piggybacks at zero marginal cost.

**Deferred:** Full consumer-ontology redesign (Option 1.5 in `docs/consumer_redesign.md`, 10 uniform deployment contexts) — 40b is the minimal incident-correctness subset, not the full ontology rework. `security_operations` coverage gap still open.

### 2026-04-19 — Session 39b: incident formula recalibration

`incidents.py:_compute_incident_probability` retuned to make the safety-investment lever observable against the market-share exposure confound.

| Parameter | Before | After |
|---|---|---|
| base_incident_rate | 0.10 | 0.20 |
| safety_multiplier coef | 0.8 | 1.5 (clipped ≥ 0) |
| floor | 0.05 | 0.02 |
| cap | 0.40 | 0.50 |

**Validation (15-seed paired heuristic baseline):**
- Pearson r(safety, incidents) flipped +0.138 → −0.066 (correct direction at last)
- safety-leader Apex incident count 2.33 → 1.87 (−20%)
- incident rate/round 0.46 → 0.53; regulator-action SD 2.8 → 1.6 (less noise)
- gap + max market share unchanged within noise

An intermediate coef=1.0 variant was rejected (Pearson flipped positive again at +0.088 — market-share exposure re-dominated).

**Breaking:** all pre-39b heuristic incident counts use the prior formula and are not directly comparable.

### 2026-04-18 — Session 39: PIMMUR Tier-1 heuristic realism upgrades

Five edits landed and validated against a 5-seed paired prior/post baseline:

1. **Per-provider incident logging** — `incident_summary` in `rounds.jsonl` now carries `by_provider_severity` and `by_provider_category` (`simulation.py:1464–1496`); closes `future_work_incident_logging.md`. Old `by_provider` retained for backwards-compat.
2. **Media narrative inertia** — `Media._cumulative_incidents` is now `float` (was `int`); decays 10%/round when no new incidents (`media.py:92, 503`); SKEPTICISM→OPTIMISM and CRISIS→SKEPTICISM recoveries now require BOTH the existing time-since-incident gate AND `cumulative < threshold/2` (`media.py:529–536`). Removes the prior instant-reset on recovery.
3. **Evaluator stewardship prompt** — hard-coded `0.75` validity-correlation threshold dropped from `DYNAMIC_EVALUATOR_SYSTEM_PROMPT` (`llm.py:1462`); replaced with neutral framing. Min-Control upgrade.
4. **Profile-derived heuristic learning rate** — new `ModelProvider._profile_learning_rate()` (`model_provider.py:359–376`) returns 0.20 for aggressive/competitive profiles, 0.10 for safety/responsible/risk-averse, default 0.15. `update_benchmark_beliefs` default `learning_rate` is now `Optional[float] = None`; resolves via `_profile_learning_rate()` when None (`model_provider.py:378–402`). Sim call site no longer passes the hard-coded 0.15 (`simulation.py:1141–1148`).
5. Verified positive-sentiment exploration churn already present at `consumer.py:844–850` (no edit).

**Validation (5 seeds × 30 rounds, paired):** provider economics drift in 4th decimal (Δsat=+0.000±0.001, ΔHHI=+0.002±0.003, Δgap≈0); incident counts identical; media narrative-state distribution per-seed-variable (Δ%OPTIMISM=−6±25pp, max single-seed swing ±43pp). Existing 30-seed heuristic baseline safe for sat/HHI/gap/incident figures; **30-seed re-baseline recommended for any narrative-state figure** before publication.

### 2026-04-18 — Session 38: private-benchmark mechanism redesign

Q1 (reporting) + Q3 (cosine) Appendix C questions resolved. Code and presets landed same session.

1. **Holdout-only reporting** replaces the blended formula: `published_score = dot(cap, holdout_weights) + noise`.
2. **Three benchmark types with public/partial/private typology:**
   - `public` (h=0)
   - `partial` (h=0.3, cosine=0.95, noise ×√(1/0.3) ≈ 1.8×)
   - `private` (h=1.0, cosine=0.85, baseline noise)
   - plus ablation-only `iid_holdout` (h=1.0, cosine=1.0)
3. **Five ablation conditions** (uniform pool-type assignment): `public_only`, `baseline` (matches reality), `private_dominant`, `private_only`, `iid_holdout`. K=3 locked (session 37 empirical calibration retained).
4. **h role redefined as sample-size noise scaling**, not blending fraction; practice-signal mechanism dropped.
5. **`inferred_benchmark_weights` initialization** changed to noisy-public-weights prior (`σ_prior` independent of h; default 0.05).
6. **Premium access as orthogonal axis** (`premium_pre_access`, `premium_submissions_per_round`) for future benchmark-sponsorship / eval-as-company ablations.

**Also this session:** Evaluator Modes section rewritten to match actual code — dynamic mode is time-triggered every `benchmark_introduction_interval` rounds (heuristic: gap-based pool selection; LLM: pool pick or `none`/`retire`), immediate introduction, auto-retire on `max_benchmarks`. Removed fictitious spec for 4-round dev pipeline, N=2 concurrency cap, `replaces`-graph paired retirement (never implemented). Internal validity corrected to Pearson (was Spearman). Actors Overview Media row corrected to "No — fully algorithmic"; `media.py` contains zero LLM calls.

### Prior sessions (compressed)

- **Session 37 (2026-04-17):** `evaluation_lag = 3` empirically calibrated via `external-validation/scripts/analyze_k_cadence.py` (24 Epoch benchmarks × 8 labs, median-of-medians K_advance 2.5–3.3 months).
- **Session 35 (2026-04-16):** `evaluation_lag: int = 0` field added to `SimulationConfig`.
- **Session 34 (2026-04-16):** Per-benchmark `holdout_fraction` + `holdout_category_dimension_weights` introduced (superseded by session-38 typology).
- **Sessions ≤ 33:** see `SESSION_HANDOFF.md` git history + project memory index.
