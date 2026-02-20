# AI Evaluation Ecosystem Simulation — Architecture Reference

This document describes how actors are modeled in the simulation. For planned work, see `TODO.md`. For experiment setup, see `run_experiment.py`.

**Last updated:** 2026-02-19

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

---

## File Reference

| File | Purpose |
|------|---------|
| `simulation.py` | Core sim loop, `SimulationConfig`, `EvalEcosystemSimulation`, `POLICYMAKER_PRESETS` |
| `run_experiment.py` | **Editable experiment config** — edit and run with `python run_experiment.py` |
| `rerun_experiment.py` | Re-runs a past experiment from saved config; supports `--modify key=value` overrides |
| `compare_experiments.py` | Comparison tool: `python compare_experiments.py exp_039 exp_040` → `comparisons/exp_039_vs_exp_040.md` |
| `actors/model_provider.py` | ModelProvider with plan/observe/reflect/execute cycle |
| `actors/evaluator.py` | Evaluator, Benchmark, benchmark evolution and introduction |
| `actors/consumer.py` | ConsumerMarket with archetype × use-case market segments |
| `actors/policymaker.py` | Policymaker with graduated interventions, calibrated EU/US presets |
| `actors/funder.py` | Funder (VC, gov, foundation types), media-aware |
| `actors/media.py` | Media actor (TechPress) — publishes coverage influencing downstream actors |
| `incidents.py` | `IncidentGenerator` — probabilistic AI safety incident generation |
| `visibility.py` | State classes: PublicState, PrivateState, GroundTruth, AIIncident |
| `llm.py` | Multi-provider LLM integration (OpenAI, Anthropic, Ollama, Gemini) |
| `plotting.py` | Visualization dashboards |
| `experiment_logger.py` | Logs experiments to `experiments/` |
| `game_log.py` | Natural language markdown game log generator |

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

### Default Provider Profiles (5-provider config)

| Provider | Research | Training | Eval Eng | Safety | Philosophy |
|----------|----------|----------|----------|--------|------------|
| Orion Labs | 25% | 30% | 20% | 25% | Product-focused, benchmark-aware |
| Apex AI | 30% | 20% | 10% | 40% | Safety-first, alignment research |
| Genesis Systems | 45% | 30% | 10% | 15% | Research-first, scientifically rigorous |
| Mirage AI | 20% | 45% | 25% | 10% | Open-source moat, pragmatic scaler |
| Spark AI | 15% | 25% | 45% | 15% | Capital-constrained, benchmark-obsessed |

Initial capabilities: Orion Labs 0.49, Apex AI 0.50, Genesis Systems 0.47, Mirage AI 0.43, Spark AI 0.38.

### Cognitive Loop

1. **Observe** — published scores (own + competitors')
2. **Reflect** — update beliefs about own capability and benchmark exploitability
3. **Plan** — allocate portfolio (LLM or heuristic), informed by own satisfaction, market share, and regulatory pressure
4. **Execute** — capability updates via R&D investments

**Incident pressure (heuristic mode):** Safety incidents accumulate `_incident_safety_pressure` (minor=0.03, moderate=0.10, major=0.20, critical=0.30, cap=0.40), shifting resources from `evaluation_engineering` toward `safety_alignment`. Decays 40%/round (~4-round effect).

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

| Archetype | `leaderboard_trust` | `switching_cost` | `switching_threshold` |
|-----------|---------------------|------------------|-----------------------|
| `leaderboard_follower` | 0.85 | 0.05 | 0.15 |
| `experience_driven` | 0.35 | 0.08 | 0.08 |
| `cautious` | 0.50 | 0.20 | 0.25 |

### Satisfaction Model

```
satisfaction = believed_quality - gaming_penalty + safety_bonus - media_penalty - incident_penalty
```

- **Gaming penalty:** Score inflation above true capability → disappointment (-20% per unit gap)
- **Safety bonus:** Provider safety investment × segment safety preference (+0 to +0.12)
- **Incident penalty:** Severity-weighted (minor: 0.02, moderate: 0.08, major: 0.15, critical: 0.30); 2× if category matches segment sector

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
| `sanctions_and_fines` | Critical incident after warning, or accumulated incidents | Reduces provider `funding_multiplier` for sanction duration |
| `market_concentration_review` | Market share > 75% | Funding multiplier reduction for dominant provider |

### Sanctions and Fines

Fine formula: `min(0.4, sanction_fine_multiplier × market_share × (1 - risk_tolerance))`

Two triggers:
1. Critical incident after a prior public warning
2. Accumulated incidents ≥ `sanction_incident_threshold` of severity ≥ `sanction_min_severity` (requires prior investigation)

Active sanctions are stored in `_active_sanctions` and applied to `funding_multiplier` in the following round's capability update.

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

---

## Media

Single outlet (TechPress). Publishes after evaluator scoring, before consumer/policymaker/funder rounds.

**Newsworthy triggers:** leader change, large score jump (>0.05), regulatory action, new benchmark, low validity (<0.5), score convergence, funding decisions, market share shifts (>3%).

**Output:** `headlines`, `sentiment` (-1 to +1), `provider_attention` (0–1 per provider), `risk_signals`.

**Downstream influence:** Sentiment modulates consumer belief update rate; risk signals bump policymaker gaming_risk; attention + risk signals increase funder `believed_gaming`.

---

## Simulation Round Order

```
1. Providers plan portfolios → capability updates (with funding + sanction multipliers)
2. Evaluator scores all providers → benchmark evolution → saturation detection → new benchmark
3. Providers observe scores and reflect
4. Incidents generated (with safety floor, sanction reduction, investigation discount)
5. Media observes and publishes
6. Consumers observe leaderboard + media → compute satisfaction → switching
7. Policymakers observe → update risk beliefs → intervene if triggered
8. Funders observe → update beliefs → allocate capital
```

---

## Experiment Infrastructure

### Directory Structure

```
experiments/exp_XXX_name/
├── metadata.json        # Description, tags, timestamp, seed
├── config.json          # Full configuration
├── rounds.jsonl         # Incremental per-round data (one JSON line per round)
├── summary.json         # Final aggregated metrics
├── game_log.md          # Human-readable simulation narrative
├── plots/               # Generated dashboards
├── providers/
├── policymakers/
│   └── Regulator/
│       ├── params.json  # Policymaker configuration
│       └── memory.json  # Intervention history and reasoning
└── funders/
```

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

### Running Experiments

```
python run_experiment.py              # Edit config at top, then run
python compare_experiments.py exp_039 exp_040   # Compare two experiments
```

See `docs/experiment_comparison_protocol.md` for the full comparison workflow.
