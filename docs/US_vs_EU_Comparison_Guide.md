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
