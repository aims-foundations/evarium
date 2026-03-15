# AI Evaluation Ecosystem Simulation — Architecture Reference

This document describes how actors are modeled in the simulation. For planned work, see `TODO.md`. For experiment setup, see `run_experiment.py`.

**Last updated:** 2026-03-15 (PIMMUR: cross-round reasoning persistence added to ModelProvider, Policymaker, and Funder; new hf_data output directory structure; `--dev` flag on run_experiment.py)

---

## Provider Name Mapping

Provider names are anonymized to prevent LLM reasoning from being biased by real-world company reputations. The mapping is:

| Simulation Name | Modeled After |
|-----------------|---------------|
| Orion Labs | OpenAI |
| Apex AI | Anthropic |
| Genesis Systems | Google DeepMind |
| Mirage AI | Meta AI |
| Spark AI | (generic benchmark-focused startup) |
| OpenCore | DeepSeek (open-source, `open_source: True`) |

---

## File Reference

| File | Purpose |
|------|---------|
| `src/simulation.py` | Core sim loop, `SimulationConfig`, `EvalEcosystemSimulation`, `POLICYMAKER_PRESETS` |
| `scripts/run_experiment.py` | **Editable experiment config** — edit and run with `python scripts/run_experiment.py` |
| `scripts/rerun_experiment.py` | Re-runs a past experiment from saved config; supports `--modify key=value` overrides; `--list` to show all experiments |
| `scripts/compare_experiments.py` | Comparison tool: `python scripts/compare_experiments.py exp_039 exp_040` |
| `scripts/final_plots.py` | **Canonical multi-experiment analysis** — 8 plots + 3 CSV tables; `python scripts/final_plots.py <exp_num1> <exp_num2> [label]` |
| `scripts/create_final_plots.py` | Older combined plots script (prefer final_plots.py) |
| `src/actors/model_provider.py` | ModelProvider with plan/observe/reflect/execute cycle |
| `src/actors/evaluator.py` | Evaluator, Benchmark, benchmark evolution and introduction |
| `src/actors/consumer.py` | ConsumerMarket with archetype × use-case market segments |
| `src/actors/policymaker.py` | Policymaker with graduated interventions, calibrated EU/US presets |
| `src/actors/funder.py` | Funder (VC, gov, foundation types), media-aware |
| `src/actors/media.py` | Media actor (TechPress) — publishes coverage influencing downstream actors |
| `src/incidents.py` | `IncidentGenerator` — probabilistic AI safety incident generation |
| `src/visibility.py` | State classes: PublicState, PrivateState, GroundTruth, AIIncident |
| `src/llm.py` | Multi-provider LLM integration (OpenAI, Anthropic, Ollama, Gemini) |
| `src/plotting.py` | Per-experiment visualization dashboards (run via ExperimentLogger or replot.py) |
| `src/experiment_logger.py` | `ExperimentLogger` (numbered `exp_NNN_*` dirs) + `DirectoryLogger` (fixed-path, used for canonical hf_data runs) |
| `src/game_log.py` | Natural language markdown game log generator |

---

## Actors Overview

| Actor | File | Status | Role |
|-------|------|--------|------|
| Model Provider | `actors/model_provider.py` | Implemented | Develops models, allocates R&D portfolio |
| Evaluator | `actors/evaluator.py` | Implemented | Operates benchmarks; evolves under gaming pressure |
| Consumer Market | `actors/consumer.py` | Implemented | 39 segments (archetype × use-case); proportional switching |
| Policymaker | `actors/policymaker.py` | Implemented | Graduated interventions; EU/US/balanced presets |
| Funder | `actors/funder.py` | Implemented | VC, gov, foundation types; media-aware capital allocation |
| Media | `actors/media.py` | Implemented | TechPress outlet; coverage influences all downstream actors |
| Incident System | `incidents.py` | Implemented | Probabilistic AI safety incidents; ecosystem propagation |

---

## Visibility System

Three-tier information access enforced structurally:

| Level | Who Can Access | Examples |
|-------|----------------|---------|
| **Public** | All actors | Published scores, leaderboard, regulatory interventions |
| **Private** | Self only | Beliefs, strategies, satisfaction history |
| **Ground Truth** | Simulation only | True capability, true satisfaction |

Ground truth is held externally by the simulation, making it structurally impossible for any actor (including LLM prompts) to access hidden information.

---

## Model Provider

### Investment Portfolio

Providers allocate 100% of effort across four areas each round:

| Investment | Capability Effect | Score Effect | Notes |
|------------|------------------|--------------|-------|
| `fundamental_research` | High (1.5× efficiency) | Indirect | Breakthrough-eligible |
| `training_optimization` | Moderate (1.0×) | Indirect | Reliable, low variance |
| `evaluation_engineering` | Minimal (0.1×) | Direct inflation via exploitability | The gaming lever |
| `safety_alignment` | None directly | None directly | Reduces incident probability; affects consumer satisfaction |

### Benchmark Specialization (benchmark_focus)

Each provider has a `benchmark_focus: dict[str, float]` weight vector (stored in `ProviderPrivateState`) that routes their `evaluation_engineering` budget across benchmarks:

```
effective_eval_eng_on_B = provider.evaluation_engineering * focus_weight[B] * n_benchmarks
```

Multiplying by `n_benchmarks` preserves total eval_eng budget for uniform-focus providers while allowing specialists to concentrate effort. A provider with `focus_benchmarks: ["safety"]` scores materially higher on safety vs. a provider with equal eval_eng but no safety focus.

**Initialization:** Provider configs specify `focus_benchmarks: list[str]` (priority-ordered, may include benchmarks introduced later in the sequence). Weight assignment (focused bms get priority weights; remainder split uniformly among unfocused):
- 1 focus: 70% / (30% shared)
- 2 focus: 50% / 30% / (20% shared)
- 3 focus: 40% / 28% / 20% / (12% shared)
- 4 focus: 35% / 25% / 18% / 12% / (10% shared)
- 5 focus: 30% / 22% / 16% / 12% / 8% / (12% shared)
- 6+ focus: 25% / 18% / 14% / 10% / 8% / 6% / (19% shared, top-6 only)
- No focus list: uniform 1/n

**Evolution per round** (called at end of `plan()`):
1. **New benchmark expansion**: When a benchmark is added mid-sim, initial weight uses trait-affinity keywords (0.6 if traits match, else 0.2) plus noise, then re-normalized.
2. **Competitive pull**: If gap > 0.05 vs leader on a benchmark, shift weight up (max 0.08/round).
3. **Stochastic perturbation**: Normal(0, 0.03) noise each round.
4. **Clip + normalize**: Each weight clipped to [0.05, 0.80], re-normalized to sum 1.0.

**Trait-affinity keywords:** `coding`: coding/software/engineering/developer/api; `safety`: safety/alignment/risk/guardrails; `math`: math/reasoning/science/research; `reasoning`: reasoning/logic/general/analytical.

### Default Provider Profiles (5-provider config + optional OS provider)

| Provider | Research | Training | Eval Eng | Safety | Benchmark Focus |
|----------|----------|----------|----------|--------|-----------------|
| Orion Labs | 25% | 30% | 20% | 25% | coding, reasoning |
| Apex AI | 30% | 20% | 10% | 40% | safety, reasoning |
| Genesis Systems | 45% | 30% | 10% | 15% | reasoning, math |
| Mirage AI | 20% | 45% | 25% | 10% | math, coding |
| Spark AI | 15% | 25% | 45% | 15% | coding |
| OpenCore | 20% | 35% | 35% | 10% | math, coding (no safety focus) |

Initial capabilities (v3, recalibrated to mean=0.25): Orion Labs 0.27, Apex AI 0.27, Genesis Systems 0.26, OpenCore 0.25, Mirage AI 0.24, Spark AI 0.21. Believed capabilities follow the same relative biases (Orion +0.02 overconfident, Genesis +0.02, Spark +0.02, Apex/OpenCore slight underestimates).

### Open-Source Provider Config Fields

Providers with `"open_source": True` in their config behave structurally differently:

| Field | Default | Description |
|-------|---------|-------------|
| `open_source` | `False` | Enables all OS-specific mechanics |
| `cost_advantage` | `0.0` | Relative pricing competitiveness applicable to **all** providers (0=most expensive/frontier, 1=free/open-weights). Calibrated to real-world token pricing: Apex AI≈0.05 (~$3/1M), Orion Labs≈0.08 (~$2.50/1M), Genesis Systems≈0.18 (~$1.25/1M), Spark AI≈0.35 (~$0.50/1M), Mirage AI≈0.42 (~$0.30/1M), OpenCore≈0.50 (~$0.07/1M). OS providers default to 0.9 if not explicitly set. |
| `contamination_multiplier` | `1.8` | Multiplier on Goodhart gaming pressure (published weights accelerate contamination). OS only. |
| `commoditization_threshold` | `0.33` | True capability level triggering one-time market shock. OS only. Recalibrated proportionally for 0.25-mean capability scale. |

**OS mechanics:**
- **Safety floor:** OS providers use `max(0.03, safety_alignment)` vs `max(0.05, ...)` for closed. Lower incentive without regulatory liability.
- **Eval-eng bias:** Heuristic planning adds +0.05 to `evaluation_engineering` (community benchmark optimization).
- **No VC funding:** VC-type funders skip OS providers entirely (no equity model). Gov and foundation funders can still allocate.
- **No premium evaluator access:** OS providers cannot purchase evaluator best-of-N or early benchmark access.
- **Lower consumer switching friction:** Opportunity threshold halved when the alternative is an OS provider (free to try = lower barrier).
- **Regulatory exemptions:** OS providers exempt from market concentration reviews and from both sanction conditions (EU AI Act open-source exemption).
- **Benchmark contamination:** Each round the OS provider contributes `contamination_multiplier × (ecosystem_influence/100)` additional gaming pressure to `update_benchmark()`.
- **Ecosystem influence:** Logistic growth each round: `ecosystem_influence += cost_advantage × true_capability × 5 × (1 - ecosystem_influence/100)`. Capped at 100. Logged in `rounds.jsonl` under `open_source_data`. Not fed back into actor decisions (analysis only).
- **Commoditization shock (one-time):** When `true_capability >= commoditization_threshold`, compresses the top closed provider's share by `min(8%, ecosystem_influence/200)`.
- **Persistent commoditization pressure:** After shock fires, `cost_advantage += 0.02/round` (capped at 0.95).
- **Consumer cost bonus:** `satisfaction += cost_sensitivity × cost_advantage × 0.15` per segment (price-sensitive segments benefit from lower-cost providers).

### Cognitive Loop

1. **Observe** — published scores (own + competitors')
2. **Reflect** — update beliefs about own capability and benchmark exploitability; append reflection reasoning to `recent_insights`
3. **Plan** — allocate portfolio (LLM or heuristic), informed by own satisfaction, market share, regulatory pressure, and prior-round insights; append planning reasoning to `recent_insights`
4. **Execute** — capability updates via R&D investments

**Incident pressure (heuristic mode):** Safety incidents accumulate `_incident_safety_pressure` (minor=0.03, moderate=0.10, major=0.20, critical=0.30, cap=0.40), shifting resources from `evaluation_engineering` toward `safety_alignment`. Decays 40%/round (~4-round effect).

### Cross-Round Memory (PIMMUR)

`ProviderPrivateState` holds a `recent_insights` list that persists the provider's own LLM reasoning across rounds:

```python
recent_insights: list   # [{"round": int, "type": str, "reasoning": str}, ...]
```

**Entry types:** `"reflection"` (appended after `reflect()`) and `"planning"` (appended after `plan()`).

**Storage:** Unbounded; the full list is kept in `private_state.recent_insights`. Only the **last 2 entries** are passed to LLM prompts (each reasoning string truncated to 120 characters).

**Prompt injection:** Both the reflection prompt and the planning prompt include a *"Your Strategic Reasoning From Prior Rounds"* section rendered from `recent_insights[-2:]`. This gives the LLM a lightweight working memory so it can track multi-round strategies (e.g., "I said last round I would increase safety; did the scores change?") without re-reading the full history.

**Heuristic mode:** `recent_insights` is populated only in LLM mode. The field exists in `ProviderPrivateState` in all modes but remains empty when heuristic planning is used.

---

## Evaluator

### Benchmark Properties

| Property | Description |
|----------|-------------|
| `validity` (α) | How well the benchmark measures true capability; decays under gaming pressure |
| `exploitability` (β) | How much evaluation engineering inflates scores; grows under gaming pressure |
| `noise_level` (σ) | Score noise standard deviation |

**Validity vs exploitability:** validity is about *signal quality* — low validity means scores are noisy and unreliable regardless of gaming. Exploitability is about *systematic bias* — high exploitability means providers can invest in eval engineering to inflate scores above true capability. In the scoring model, exploitability shifts the mean upward while validity widens the variance. Both degrade together under Goodhart pressure.

### Scoring Model

```
score ~ Normal(true_capability + eval_engineering × exploitability, (σ/√α)²)
```

Published scores are monotonically non-decreasing per provider (providers wouldn't disclose a worse score).

### Benchmark Evolution

- **Goodhart decay:** Each round, validity decreases and exploitability increases proportional to ecosystem-wide average `evaluation_engineering`.
- **Saturation:** Any provider reaching score ≥ 0.90 triggers saturation; benchmark retires after a 2-round cooldown.
- **Introduction:** New benchmarks introduced on validity < 0.4, periodic cooldown, or saturation trigger. Pulls from `benchmark_sequence` if configured (see `run_experiment.py`). Subject to `max_benchmarks` cap.
- **Evaluator-as-company:** Optional mode where providers pay for premium best-of-N submissions. Disabled by default (`evaluator_as_company=False`).

---

## Consumer Market

### Segments

Each segment = use-case profile × behavioral archetype. Default config: 13 use-cases × 3 archetypes = **39 segments**.

**Archetypes:**

| Archetype | `leaderboard_trust` | `switching_cost` | `switching_threshold` | `cost_sensitivity` |
|-----------|---------------------|------------------|-----------------------|--------------------|
| `leaderboard_follower` | 0.85 | 0.05 | 0.15 | 0.15 |
| `experience_driven` | 0.35 | 0.08 | 0.08 | 0.30 |
| `cautious` | 0.50 | 0.20 | 0.25 | 0.20 |
| `enterprise_cautious` | 0.25 | 0.35 | 0.50 | 0.10 |
| `enterprise_growth` | 0.45 | 0.25 | 0.30 | 0.15 |
| `enterprise_established` | 0.35 | 0.40 | 0.40 | 0.08 |

### Satisfaction Model

```
satisfaction = believed_quality - gaming_penalty + safety_bonus - media_penalty - incident_penalty + cost_bonus
```

- **Gaming penalty:** Score inflation above true capability → disappointment (-20% per unit gap)
- **Safety bonus:** Provider safety investment × segment safety preference (+0 to +0.12)
- **Incident penalty:** Severity-weighted (minor: 0.02, moderate: 0.08, major: 0.15, critical: 0.30); 2× if category matches segment sector
- **Cost bonus:** `cost_sensitivity × cost_advantage × 0.15` — all providers with non-zero `cost_advantage` gain satisfaction among price-sensitive segments; higher values (cheaper relative pricing) yield larger bonuses
- **LLM cost reasoning:** When consumers use LLM-mode deliberation, `cost_advantage` is surfaced in the prompt for all providers. Organizational consumers explicitly weigh cost vs capability based on their `cost_sensitivity` tier (HIGH ≥0.20, MODERATE ≥0.10, LOW <0.10); cost is included in the Decision Framework as step 3. Individual consumers surface cost only when `cost_sensitivity ≥ 0.10`.

### Switching

Proportional sigmoid-based switching within each segment. Two triggers: dissatisfaction (expected > experienced quality) and opportunity (better alternative exists). Tenure bonus adds inertia.

Organizational consumers (hospital_system, enterprise_finance, tech_startup) apply 1.5× upweight to domain-relevant benchmarks and can use LLM-mode deliberation.

---

## Incident System

### Probability Model

Base rate: **10% per provider per round**. Multiplied by six factors:

| Factor | Formula | Direction |
|--------|---------|-----------|
| Safety investment | `1 - (safety_alignment × 0.8)` | Higher safety → lower prob |
| Gaming gap | `1 + (published_score - true_capability) × 2` | More gaming → higher prob |
| Market share (exposure) | `0.5 + (market_share × 1.5)` | Larger market → higher prob |
| Capability level | `0.8 + (true_capability × 0.4)` | Higher capability → higher stakes |
| Incident history escalation | `+0.04 per prior major/critical, cap +0.20` | Past harm → elevated future risk |
| Active sanction | `0.75×` while sanctioned | Regulatory oversight → reduced prob |

Additionally, providers under **emergency investigation** have their effective published score discounted 15% for gaming gap calculation, reducing incident probability.

Capped at 0.40 per round.

### Severity Distribution

| Severity | Probability | Description |
|----------|-------------|-------------|
| Minor | 50% | Internal only |
| Moderate | 31% | Multiple users, local coverage |
| Major | 12% | National media, regulatory attention |
| Critical | 7% | Public safety, emergency response |

### Categories

`healthcare_harm` (20%), `security_breach` (25%), `bias_discrimination` (20%), `safety_failure` (20%), `misinformation` (10%), `misuse` (5%).

### Ecosystem Propagation

- **Media:** Headlines for moderate+; provider attention and sentiment penalties; risk signals
- **Consumers:** Incident penalty in satisfaction; leaderboard_trust erosion for follower segments
- **Policymakers:** Risk belief updates by category; critical incidents trigger emergency_investigation
- **Funders:** Increased `believed_gaming`; incident penalty in provider scoring

---

## Policymaker

### Intervention Types (Graduated Escalation)

| Type | Trigger | Effect |
|------|---------|--------|
| `investigation` | Risk beliefs cross threshold | Opens formal inquiry |
| `public_warning` | After investigation | Reduces consumer `leaderboard_trust` |
| `threshold_announcement` | Moderate risk | Signals regulatory thresholds publicly |
| `emergency_investigation` | Critical incident | Overrides cooldown; immediate action |
| `mandate_benchmark` | High risk, after investigation | Forces benchmark validity/exploitability changes |
| `compliance_audit` | Post-mandate | Further reduces exploitability |
| `sanctions_and_fines` | Critical incident after warning, or accumulated incidents | Reduces provider `funding_multiplier` for sanction duration. **OS providers exempt.** |
| `market_concentration_review` | Market share > 75% | Funding multiplier reduction for dominant provider. **OS providers exempt.** |

### Sanctions and Fines

Fine formula: `min(0.4, sanction_fine_multiplier × market_share × (1 - risk_tolerance))`

Two triggers:
1. Critical incident after a prior public warning
2. Accumulated incidents ≥ `sanction_incident_threshold` of severity ≥ `sanction_min_severity` (requires prior investigation)

Active sanctions are stored in `_active_sanctions` and applied to `funding_multiplier` in the following round's capability update.

### Risk Belief Thresholds

| Signal | Threshold | Effect |
|--------|-----------|--------|
| `consumer_satisfaction` | < 0.25 | Increments `consumer_harm_risk` +0.1/round (recalibrated from 0.5 to match 0.25-mean capability scale) |
| `validity_correlation` | < 0.5 | Flags gaming suspicion |
| `eval_engineering` share | > 0.35 | Increments `gaming_risk` |
| `market_share` | > 0.75 | Triggers `market_concentration_review` |
| `max_risk` | > 0.4 | Triggers `investigation` |

### Cross-Round Memory (PIMMUR)

`PolicymakerPrivateState` holds a `recent_reasoning` list that persists the policymaker's LLM decision reasoning across rounds:

```python
recent_reasoning: list   # [{"round": int, "reasoning": str}, ...]
```

**Storage:** Capped at the **last 3 entries**. Only the **last 2** are passed to LLM prompts (each truncated to 120 characters).

**Prompt injection:** Injected at the top of the decision prompt as a *"Your Reasoning From Prior Rounds"* block. This lets the policymaker maintain consistent policy stances across rounds (e.g., tracking whether a previously announced investigation led to provider compliance, or escalating from warning to sanction if the situation has not improved).

**Population:** Appended after each LLM decision call with the `"reasoning"` field extracted from the LLM JSON output.

---

### Regulatory Presets (`POLICYMAKER_PRESETS` in `simulation.py`)

| Parameter | EU Precautionary | Balanced | US Light-Touch | Empirical Basis |
|-----------|-----------------|----------|----------------|-----------------|
| `intervention_threshold` | 0.35 | 0.50 | 0.75 | EU acts at moderate risk; US waits |
| `risk_tolerance` | 0.20 | 0.50 | 0.70 | EU cautious; US innovation-first |
| `intervention_cooldown` | 2 rounds | 3 | 5 | Italy acted on ChatGPT in ~21 months; FTC inquiries take years |
| `sanction_fine_multiplier` | 0.35 | 0.22 | 0.10 | EU AI Act 7% ceiling; US FTC consent-order-only |
| `sanction_incident_threshold` | 2 | 3 | 4 | EU acts on patterns; US needs repeated critical violations |
| `sanction_duration` | 4 rounds | 3 | 2 | EU compliance cycles lengthy; US decrees shorter |
| `mandate_risk_threshold` | 0.50 | 0.62 | 0.75 | EU ex-ante mandates; US almost never mandates |
| `sanction_min_severity` | major | major | critical | EU acts on major+; US critical only |

**Effect sizes at 60% market share:**
- EU fine: `0.35 × 0.6 × 0.8 = 16.8%` R&D efficiency reduction
- US fine: `0.10 × 0.6 × 0.3 = 1.8%` R&D efficiency reduction

### Policymaker → Incident Probability (Implemented Pathways)

| Mechanism | How It Works |
|-----------|-------------|
| **Mandatory safety floor** | Providers under `compliance_audit`, `sanctions_and_fines`, or `emergency_investigation` have `safety_alignment` clamped to minimum 0.15 before incident generation |
| **Sanction → prob reduction** | Active sanction applies 0.75× multiplier to incident probability (compliance audit / operational caution effect) |
| **Investigation → score discount** | Emergency investigation discounts provider's effective published score 15% for gaming gap calculation |
| **Incident history escalation** | Each prior major/critical adds +0.04 to base rate (cap +0.20); policymaker early intervention breaks this feedback loop |

---

## Funder

### Types and Signal Weights

| Type | Quality | Score Momentum | Market Traction | Market Momentum | Diversification | Pattern |
|------|---------|---------------|-----------------|-----------------|-----------------|---------|
| VC | 0.15 | 0.25 | 0.15 | 0.20 | 0.25 | Concentrated; contrarian bias |
| Government | 0.50 | 0.10 | 0.25 | 0.05 | 0.10 | Spread proportionally |
| Foundation | 0.35 | 0.20 | 0.15 | 0.10 | 0.20 | Ecosystem health focus |

Funding affects providers via `funding_multiplier` on capability gains (range 1.0–2.0). Funders observe each other's allocations and diversify portfolios. Per-round deployment capped at `max_round_deployment` of total capital.

**OS provider exclusions:** VC-type funders skip OS providers entirely (no equity model). Gov and foundation funders can still allocate. OS providers also cannot purchase evaluator premium access.

### Cross-Round Memory (PIMMUR)

`FunderPrivateState` holds a `recent_reasoning` list that persists the funder's LLM allocation reasoning across rounds:

```python
recent_reasoning: list   # [{"round": int, "reasoning": str}, ...]
```

**Storage:** Capped at the **last 3 entries**. Only the **last 2** are passed to LLM prompts (each truncated to 120 characters), via the `recent_insights` parameter of `llm_plan_funding()` (note: parameter is named `recent_insights` for API consistency but receives `recent_reasoning` data).

**Prompt injection:** Rendered as a *"Your Reasoning From Prior Rounds"* section in the funder planning prompt, allowing funders to maintain investment theses across rounds (e.g., continuing to back a provider they committed to last round, or following through on a diversification decision).

**Population:** Appended after each LLM funding decision with the `"reasoning"` field from the LLM JSON output.

**Funder eligibility delay:** New startup entrants are invisible to funders for `startup_funder_delay` rounds after entry (default: 1). The leaderboard passed to `funder.observe()` is filtered accordingly.

---

## Startup Entry Dynamics

New `ModelProvider` instances can spawn mid-simulation to model market contestability and EU vs US regulatory differences.

**Config fields (on `SimulationConfig`):**

| Field | Default | Description |
|-------|---------|-------------|
| `startup_entry_probability` | `0.0` | Base per-round entry probability; actual roll uses `base × (1 − bte_composite)` |
| `startup_entry_cap` | `3` | Hard cap on total entrants across the run (policy-specific in `run_experiment.py`) |
| `startup_funder_delay` | `1` | Rounds before funders can allocate to the entrant |
| `startup_llm_mode` | `False` | Whether entrants use LLM planning |

**Entry mechanics:**
- Each round, `_maybe_spawn_startup()` rolls against an **effective probability** that is modulated by last round's BTE composite: `effective_prob = startup_entry_probability × (1 − bte_composite)`. High BTE suppresses entry. Round 0 uses the base probability directly (no BTE history yet).
- Starting capability = `best_open_source_cap * 0.75` (recalibrated for 0.25-mean scale; fallback 0.16 if no OS provider)
- Starting `safety_alignment = 0.10` (startup moving fast)
- Starting `cost_advantage = 0.38` (lean startups undercut incumbents on pricing to gain share)
- Random strategy profile drawn from a startup-flavored pool
- Named `Startup-1`, `Startup-2`, etc.
- Registered with `ConsumerMarket.add_provider()` at ~1% initial share (dilutes incumbents proportionally)
- Logged as `round_data["new_entrant"]`

**EU vs US calibration (current run_experiment.py):**
| Policy | `startup_entry_probability` | `startup_entry_cap` | Expected entrants (avg BTE ~0.5) |
|--------|----------------------------|---------------------|----------------------------------|
| US | 0.15 | 4 | ~2.5 |
| EU | 0.04 | 1 | ~0.6 |

Higher base probability → more competition, lower market concentration, lower safety alignment on average, higher incident rate. BTE feedback means entry naturally slows as incumbents entrench.

---

## Barrier-to-Entry (BTE) Index

Composite per-round metric logged as `round_data["barrier_to_entry"]`. Answers: "How hard would it be for a new AI model provider startup to enter this market right now?" Higher = harder.

**Components (equal-weighted; None if actor not active):**

| Component | Formula | Source |
|-----------|---------|--------|
| `market_concentration` | Normalized HHI of market shares | `consumer_data["market_shares"]` |
| `capability_gap` | `(leader_cap - os_baseline) / (leader_cap - 0.10)` | `true_capabilities`, `is_open_source` |
| `funding_lock_in` | Normalized HHI of funder allocations to non-OS providers | `funder_data["allocations"]` |
| `consumer_lock_in` | Weighted avg friction (switching cost + integration + tenure bonus) / MAX | `consumer_market.segments` |

`composite` = mean of active components. Computed in `_compute_barrier_to_entry()` after all actor phases complete, before round data is persisted to history. The `consumer_lock_in` component normalizes by `MAX_FRICTION = 0.525` (switching_cost 0.20 + integration_friction 0.225 + tenure_bonus 0.10).

---

## Media

Single outlet (TechPress). Publishes after evaluator scoring, before consumer/policymaker/funder rounds.

**Newsworthy triggers:** leader change, large score jump (>0.05), regulatory action, new benchmark, low validity (<0.5), score convergence, funding decisions, market share shifts (>3%).

**Output:** `headlines`, `sentiment` (-1 to +1), `provider_attention` (0–1 per provider), `risk_signals`.

**Downstream influence:** Sentiment modulates consumer belief update rate; risk signals bump policymaker gaming_risk; attention + risk signals increase funder `believed_gaming`.

---

## Simulation Round Order

```
0. Startup entry check: _maybe_spawn_startup() rolls against startup_entry_probability
1. Providers plan portfolios → capability updates (with funding + sanction multipliers)
2. Evaluator scores all providers → benchmark evolution → saturation detection → new benchmark
3. Providers observe scores and reflect
4. Incidents generated (with safety floor, sanction reduction, investigation discount)
5. Media observes and publishes
6. Consumers observe leaderboard + media → compute satisfaction → switching
7. Policymakers observe → update risk beliefs → intervene if triggered
8. Funders observe eligible leaderboard → update beliefs → allocate capital
9. barrier_to_entry index computed and logged
```

---

## Experiment Infrastructure

### Directory Structure

Canonical output lives in `hf_data/` (see `EXPERIMENT_PLAN.md` for the full layout). The two active subtrees:

```
hf_data/
├── claude_archive/              # Legacy Claude 3.5 Sonnet runs exp_001–015 (full artifacts)
├── llm_core/                    # Canonical LLM runs (Phase 1 + Phase 2 replications)
│   ├── claude-sonnet-4-6/       # Written by run_experiment.py (anthropic provider)
│   │   └── <condition>/
│   │       └── seeds/
│   │           └── seed_N/
│   │               ├── config.json
│   │               ├── metadata.json
│   │               ├── rounds.jsonl
│   │               └── summary.json
│   ├── qwen-235b/               # Primary research model
│   └── llama-70b/               # Cross-model comparison
├── heuristic_baseline/          # Phase 5: 27 conditions × 30 seeds (complete)
└── test/                        # Dev/exploratory runs (written when --dev flag is used)
    └── <condition>_<timestamp>/
        └── (full artifacts)
```

`run_experiment.py` uses `DirectoryLogger` (fixed-path, no index.json) for all writes. Per-seed lean storage (llm_core): `rounds.jsonl` + `summary.json` + `config.json` + `metadata.json`. Heavy artifacts (`game_log.md`, `history.json`, `plots/`, `providers/`, `funders/`, `policymakers/`) are written only for dev/test runs (`lightweight=False` when `--dev`).

Legacy `output/experiments/` (numbered `exp_NNN_*` dirs with `index.json`) is no longer used for new runs.

### Known Bugs Fixed
- **`src/simulation.py` ~line 775:** Incidents were generated regardless of `enable_incidents` flag. Fixed: `if round_num > 0 and self.config.enable_incidents:`. Affected: all ablation experiments with `enable_incidents=False` (e.g., exp_005).
- **`scripts/rerun_experiment.py`:** `policymaker_configs` was not extracted from the saved config dict and not passed to `sim.setup()`, causing reruns to use default policymaker settings. Also `sim.consumers` (deprecated empty list) replaced with `sim.consumer_market`.

### Key Metrics

| Metric | What It Reveals |
|--------|----------------|
| `score - true_capability` gap | Benchmark inflation from gaming |
| `validity_correlation` | Overall benchmark trustworthiness (key Goodhart metric) |
| `mean_evaluation_engineering` | Direct gaming effort |
| `active_sanctions` in `policymaker_data` | Which providers are under enforcement and fine sizes |
| `mean_satisfaction` / `final_satisfaction` | Consumer welfare |
| `final_market_shares` | Market outcome; which providers won/lost |
| `funding_multipliers` | Capital advantage per provider |
| `barrier_to_entry["composite"]` | Structural difficulty for a new startup to enter |
| `new_entrant` in round_data | Present when a startup spawned that round |

### Running Experiments

```bash
python scripts/run_experiment.py --policy balanced      # Balanced policy (default)
python scripts/run_experiment.py --policy us            # US light-touch
python scripts/run_experiment.py --policy eu            # EU precautionary
python scripts/run_experiment.py --dev                  # Dev/test: output -> hf_data/test/<condition>_<timestamp>/
python scripts/run_experiment.py --policy balanced --dev  # Combined

python scripts/rerun_experiment.py exp_016              # Rerun a past legacy experiment
python scripts/rerun_experiment.py exp_016 --modify n_rounds=50 --seed 99
python scripts/rerun_experiment.py --list
python scripts/compare_experiments.py exp_039 exp_040
python scripts/final_plots.py 3 2 my_label             # Multi-experiment analysis plots
```

`--dev` routes output to `hf_data/test/` with a timestamp suffix so repeated test runs don't overwrite each other. Use it for exploratory runs, PIMMUR tests, or any experiment you don't want in the canonical `llm_core` record.

See `docs/experiment_comparison_protocol.md` for the full comparison workflow.
