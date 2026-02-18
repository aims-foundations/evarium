# US vs EU Regulatory Style Comparison Guide

## Overview

The simulation includes three policymaker regulatory philosophies that model different approaches to AI governance:

- **us_light_touch**: Ex-post response (US-style)
- **eu_precautionary**: Ex-ante prevention (EU-style)
- **balanced**: Middle ground

## Regulatory Philosophy Differences

| Parameter | US Light-Touch | EU Precautionary | Balanced |
|-----------|---------------|------------------|----------|
| **Intervention Threshold** | 0.75 (high) | 0.35 (low) | 0.50 (medium) |
| **Risk Tolerance** | 0.7 (high) | 0.2 (low) | 0.5 (medium) |
| **Response Speed** | Slow | Fast | Medium |
| **Approach** | Ex-post (react to harm) | Ex-ante (prevent before harm) | Mixed |

## How to Run Comparison Experiments

### Step 1: Run EU Baseline

```bash
# Edit run_experiment.py
# Set: POLICYMAKERS["configs"][0]["philosophy"] = "eu_precautionary"
python run_experiment.py
# Note output: e.g., heur_008_baseline_with_incidents_v1
```

### Step 2: Run US Comparison

```bash
# Edit run_experiment.py:
# 1. Change: POLICYMAKERS["configs"][0]["philosophy"] = "us_light_touch"
# 2. Change: EXPERIMENT["name"] = "baseline_us_style_v1"
python run_experiment.py
# Note output: e.g., heur_009_baseline_us_style_v1
```

### Step 3: Compare Results

Check `experiments/heuristic/` directory for both experiment folders.

**Key Metrics to Compare:**

1. **Incident Counts**
   - Total incidents across 25 rounds
   - Incidents by severity (minor, moderate, major, critical)
   - Incidents by provider

2. **Regulatory Interventions**
   - Total interventions
   - Intervention types
   - Round numbers when interventions occurred
   - Providers targeted

3. **Market Dynamics**
   - Provider market shares over time
   - Consumer satisfaction trends
   - Switching behavior

4. **Safety Adaptation**
   - How providers adjust safety_alignment over time
   - Difference between high-safety and low-safety providers

## Expected Differences

### US Light-Touch (Ex-Post)
- **More incidents**: Higher threshold allows more incidents before intervention
- **Slower response**: Longer cooldowns between interventions
- **Higher innovation**: Providers face less regulatory burden
- **Market-driven safety**: Consumer satisfaction drives safety investment

### EU Precautionary (Ex-Ante)
- **Fewer incidents**: Lower threshold triggers preventive action
- **Faster response**: Shorter cooldowns, more frequent interventions
- **Lower innovation**: Regulatory compliance slows capability growth
- **Regulation-driven safety**: Mandatory requirements force safety investment

### Balanced
- **Middle ground**: Moderate incident rate, moderate intervention frequency
- **Mixed drivers**: Both market and regulatory pressures

## Analysis Commands

### Count Incidents

```bash
cd experiments/heuristic/[experiment_id]
python -c "
import json
total = sum(1 for line in open('rounds.jsonl')
           for data in [json.loads(line)]
           if data.get('incidents'))
print(f'Rounds with incidents: {total}')
"
```

### Count Interventions

```bash
python -c "
import json
interventions = []
for line in open('rounds.jsonl'):
    data = json.loads(line)
    if data.get('policymaker_data', {}).get('interventions'):
        interventions.extend(data['policymaker_data']['interventions'])
print(f'Total interventions: {len(interventions)}')
for i in interventions[:10]:
    print(f\"  Round {i.get('details', {}).get('round', '?')}: {i['type']}\")
"
```

## Testable Hypotheses

1. **Incident Rate**: EU style reduces total incident count by 30-50%
2. **Innovation Speed**: US style achieves higher average capability by round 25
3. **Market Concentration**: US style leads to higher market concentration
4. **Safety Investment**: EU style forces higher safety_alignment across all providers
5. **Consumer Satisfaction**: EU style maintains higher long-term satisfaction

## Visualization

After running both experiments, use plotting tools to compare:

```bash
# Generate comparison plots
python -c "
from plotting import plot_provider_dashboard
# Load both experiment histories
# Generate side-by-side comparison
"
```

## Example Comparison

See `experiments/comparisons/` for example US vs EU comparison results (if available).

## Advanced: Parameter Sweeps

To test sensitivity to regulatory parameters:

1. Run multiple experiments varying intervention_threshold: [0.3, 0.5, 0.7, 0.9]
2. Run multiple experiments varying risk_tolerance: [0.2, 0.4, 0.6, 0.8]
3. Analyze incident rate vs innovation speed tradeoffs

## Notes

- Keep all other parameters constant between US and EU runs for valid comparison
- Use same random seed (42) for reproducibility
- Run at least 3 replicates with different seeds for statistical confidence
- US vs EU differences become more pronounced after round 15-20

---

## Empirical Results: Experiments 032 (EU) and 033 (US)

This section documents actual outcomes from a paired simulation run using identical market conditions but different regulatory philosophies. Both experiments used the `baseline_with_incidents_v2` scenario: 5 providers (OpenAI, Anthropic, Google, MetaAI, StartupDotAI), 30 rounds, heuristic-mode actors, same random seed.

- **exp032**: EU Precautionary (`intervention_threshold=0.35`, `risk_tolerance=0.2`)
- **exp033**: US Light-Touch (`intervention_threshold=0.75`, `risk_tolerance=0.7`)

### Regulatory Parameters and Industry Trust

| Metric | EU (exp032) | US (exp033) |
|--------|-------------|-------------|
| Intervention threshold | 0.35 | 0.75 |
| Risk tolerance | 0.2 | 0.7 |
| Industry trust (R0) | 0.501 | 1.0 |
| Industry trust (R29) | 0.399 | 1.0 |

The EU regulator's industry trust eroded steadily over time as incidents accumulated against its low-risk-tolerance baseline. The US regulator's trust remained pegged at 1.0 throughout — consistent with a high-threshold philosophy that treats incidents as acceptable market signals rather than systemic failures.

### Interventions: Same Count, Different Triggers

Both regulators issued exactly **6 interventions** over 30 rounds, of the same types (transparency_requirement, public_disclosure, performance_audit, emergency_investigation, benchmark_mandate). The difference was in trigger timing and targets:

| Round | EU Intervention | US Intervention |
|-------|-----------------|-----------------|
| R1 | transparency_requirement | transparency_requirement |
| R4 | public_disclosure | public_disclosure |
| R7 | performance_audit | performance_audit |
| R9 | emergency_investigation (StartupDotAI, critical safety_failure) | — |
| R10 | — | emergency_investigation (Anthropic, critical safety_failure) |
| R24 | benchmark_mandate (triggered at fairness_risk=0.75) | benchmark_mandate (triggered at fairness_risk=0.90) |
| R28 | (final intervention) | (final intervention) |

The emergency investigations targeted different providers: the EU flagged **StartupDotAI** at R9 (a marginal provider, earlier trigger), while the US flagged **Anthropic** at R10 (the market leader, one round later and at a higher risk threshold). This reflects the precautionary regulator acting earlier and being willing to challenge any provider, while the light-touch regulator waited longer and only acted when the dominant firm crossed a higher bar.

### Incident Outcomes

Both experiments produced **12 total incidents**, contradicting the hypothesis that EU regulation reduces incident counts:

| Severity | EU (exp032) | US (exp033) |
|----------|-------------|-------------|
| Critical | 1 | 1 |
| Major | 2 | 4 |
| Moderate | 3 | 2 |
| Minor | 6 | 5 |
| **Total** | **12** | **12** |

The EU profile skewed toward lower-severity incidents (more minor/moderate, fewer major), while the US profile had more major incidents. This suggests the EU's early interventions may have dampened escalation — but they could not reduce the baseline incident rate driven by provider capability growth and the underlying incident probability model.

### The Benchmark Mandate: A Market-Reshuffling Event

The most consequential policy divergence occurred at **Round 24**, when both regulators issued a benchmark_mandate. The EU triggered it at `fairness_risk=0.75`; the US held out until `fairness_risk=0.90`.

**EU outcome (exp032):** Google surged from roughly 8% market share to **38-46%** in the rounds immediately following the mandate. This reshuffling reflects Google meeting newly imposed benchmark standards better than competitors at that moment. The market only partially re-stabilized by R29, with Google retaining 13.4% — permanently above its pre-mandate level.

**US outcome (exp033):** No comparable reshuffling occurred. Anthropic maintained its dominant position throughout, and the mandate produced only minor share adjustments. The later, higher-threshold trigger gave providers more time to comply on their own terms before regulatory pressure crystallized.

### Market Share: Who Won?

Final market shares (Round 29):

| Provider | EU (exp032) | US (exp033) |
|----------|-------------|-------------|
| Anthropic | 61.8% | 64.6% |
| OpenAI | 9.6% | 23.8% |
| Google | 13.4% | 5.4% |
| MetaAI | 12.6% | 3.8% |
| StartupDotAI | 2.5% | 2.5% |

Anthropic dominated in both regimes — but OpenAI's fate diverged sharply. In the EU, OpenAI was marginalized to 9.6% and never recovered after early adverse benchmark performance and the emergency investigation context. In the US, OpenAI declined mid-game but recovered to 23.8%, benefiting from a less disruptive regulatory environment and the absence of the market-reshuffling benchmark shock that hit EU competitors.

Google's result is the inverse: benefiting from the EU mandate surge (13.4% final) while remaining a niche player in the US (5.4%).

### Safety Alignment: The Counterintuitive Result

Average safety_alignment investment across all providers at Round 29:

| | EU (exp032) | US (exp033) |
|-|-------------|-------------|
| Avg safety_alignment | ~19% | ~23% |

**US providers invested more in safety alignment than EU providers.** This inverts the naive prediction that regulatory pressure drives safety investment. A plausible explanation: under the EU's frequent early interventions, providers adapted by investing in evaluation_engineering and compliance-theater (benchmark performance) rather than fundamental safety work. Under the US regime, providers facing a more competitive market used safety alignment as a product differentiator to capture consumer trust — a market-driven safety signal rather than a regulatory one.

### Consumer Satisfaction

| | EU (exp032) | US (exp033) |
|-|-------------|-------------|
| Final avg satisfaction (R29) | 0.777 | 0.739 |

The EU regime produced slightly higher final consumer satisfaction. This aligns with the hypothesis: EU interventions may have restrained destabilizing behavior and maintained more predictable service quality, even as they distorted market structure. The US regime's higher incident severity (more major incidents) likely dragged satisfaction in the second half of the run.

### True Capabilities (Round 29)

| Provider | EU capability | US capability |
|----------|---------------|---------------|
| OpenAI | 0.763 | ~0.76 |
| Anthropic | 0.785 | ~0.78 |
| Google | 0.698 | ~0.70 |
| MetaAI | 0.675 | ~0.67 |
| StartupDotAI | 0.635 | ~0.63 |

True capabilities were nearly identical across both regimes. Regulatory philosophy had negligible effect on capability growth trajectories in this paired run, suggesting that capability accumulation is driven primarily by the investment model and random variation rather than regulatory environment — at least over a 30-round horizon.

### Hypothesis Verification

| Hypothesis | Predicted | Actual |
|------------|-----------|--------|
| EU reduces incident count by 30-50% | Fewer EU incidents | **WRONG** — both had 12; EU skewed lower-severity |
| US achieves higher capability by R25 | Higher US capabilities | **WRONG** — capabilities nearly identical |
| US leads to higher market concentration | More concentrated US | **WRONG** — both Anthropic-dominated; EU slightly more concentrated overall |
| EU forces higher safety_alignment | Higher EU safety investment | **WRONG** — US averaged higher (23% vs 19%) |
| EU maintains higher long-term satisfaction | Higher EU satisfaction | **CORRECT** — 0.777 vs 0.739 |

### Summary

The two regulatory philosophies produced subtly but meaningfully different simulation trajectories over 30 rounds, despite identical starting conditions:

- **EU Precautionary**: More volatile market dynamics (benchmark mandate caused Google surge), OpenAI marginalized, slightly higher consumer satisfaction, eroding regulator trust, lower provider safety investment.
- **US Light-Touch**: Stable Anthropic dominance, OpenAI recovered mid-game, lower consumer satisfaction, sustained regulator trust, higher provider safety investment driven by market competition rather than mandates.

The most surprising finding is that formal regulatory pressure did not increase safety investment — market competition did. The benchmark mandate's market-reshuffling effect was the single largest consequence of regulatory style, creating a natural experiment in how standardization timing shapes competitive outcomes.
