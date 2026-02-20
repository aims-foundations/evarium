# Experiment Comparison

| | A | B |
| --- | --- | --- |
| Experiment | exp_043_eu_precautionary_sanctions_v2 | exp_044_us_lighttouch_sanctions_v2 |
| Rounds | 50 | 50 |

## Regulatory Configuration

| Parameter | A | B |
| --- | --- | --- |
| intervention_threshold | 0.350 | 0.750 |
| risk_tolerance | 0.200 | 0.700 |
| intervention_cooldown | 2.0 | 5.0 |
| sanction_fine_multiplier | 0.350 | 0.100 |
| sanction_incident_threshold | 2.0 | 4.0 |
| sanction_duration | 4.0 | 2.0 |
| mandate_risk_threshold | 0.500 | 0.750 |
| sanction_min_severity | major | critical |

## Interventions

| Type | A | B |
| --- | --- | --- |
| **total** | **16** | **10** |
| compliance_audit | 8 | 3 |
| emergency_investigation | 2 | 2 |
| investigation | 1 | 1 |
| mandate_benchmark | 1 | 1 |
| public_warning | 1 | 1 |
| sanctions_and_fines | 2 | 1 |
| threshold_announcement | 1 | 1 |

**A timeline:** R1: investigation  
R3: threshold_announcement  
R5: public_warning  
R10: emergency_investigation  
R25: sanctions_and_fines ->  (fine=3.9%)  
R27: mandate_benchmark  
R31: compliance_audit  
R33: compliance_audit  
R35: compliance_audit  
R37: compliance_audit  
R39: compliance_audit  
R41: compliance_audit  
R43: compliance_audit  
R45: compliance_audit  
R47: emergency_investigation  
R49: sanctions_and_fines ->  (fine=3.1%)

**B timeline:** R1: investigation  
R6: public_warning  
R10: emergency_investigation  
R15: threshold_announcement  
R25: sanctions_and_fines ->  (fine=0.5%)  
R30: mandate_benchmark  
R35: compliance_audit  
R36: emergency_investigation  
R41: compliance_audit  
R46: compliance_audit

## Active Sanctions Log

| Exp | Round | Provider | Fine | Expires | Reason |
| --- | --- | --- | --- | --- | --- |
| A | R25 | OpenAI | 3.9% | R29 | Critical incident after public warning |
| A | R26 | OpenAI | 3.9% | R29 | Critical incident after public warning |
| A | R27 | OpenAI | 3.9% | R29 | Critical incident after public warning |
| A | R28 | OpenAI | 3.9% | R29 | Critical incident after public warning |
| A | R49 | Google | 3.1% | R53 | Repeated major+ incidents |
| B | R25 | OpenAI | 0.5% | R27 | Critical incident after public warning |
| B | R26 | OpenAI | 0.5% | R27 | Critical incident after public warning |

## Incidents

|  | A | B |
| --- | --- | --- |
| **total** | **23** | **23** |
| critical | 1 | 1 |
| major | 3 | 3 |
| moderate | 6 | 6 |
| minor | 13 | 13 |

| Provider | A incidents | B incidents |
| --- | --- | --- |
| Anthropic | 4 | 5 |
| Google | 4 | 7 |
| MetaAI | 4 | 3 |
| OpenAI | 7 | 5 |
| StartupDotAI | 4 | 3 |

## Final Market Shares

| Provider | A | B |
| --- | --- | --- |
| Anthropic | 72.5% | 71.5% |
| Google | 11.2% | 10.4% |
| MetaAI | 3.9% | 4.0% |
| OpenAI | 9.9% | 11.5% |
| StartupDotAI | 2.5% | 2.5% |

## Final True Capabilities

| Provider | A | B |
| --- | --- | --- |
| Anthropic | 0.921 | 0.920 |
| Google | 0.888 | 0.877 |
| MetaAI | 0.830 | 0.827 |
| OpenAI | 0.882 | 0.889 |
| StartupDotAI | 0.773 | 0.775 |
| **avg** | **0.859** | **0.858** |

## Provider Strategy (Round Means)

| Provider | A safety | B safety | A eval_eng | B eval_eng |
| --- | --- | --- | --- | --- |
| Anthropic | 0.224 | 0.215 | n/a | n/a |
| Google | 0.151 | 0.159 | n/a | n/a |
| MetaAI | 0.170 | 0.183 | n/a | n/a |
| OpenAI | 0.196 | 0.215 | n/a | n/a |
| StartupDotAI | 0.166 | 0.153 | n/a | n/a |

## Consumer Outcomes

| Metric | A | B |
| --- | --- | --- |
| mean satisfaction | 0.772 | 0.767 |
| final satisfaction | 0.923 | 0.918 |
| avg switching rate | 0.069 | 0.069 |

## Benchmark Quality (Final)

| Metric | A | B |
| --- | --- | --- |
| validity | 0.783 | 0.785 |
| exploitability | 0.100 | 0.100 |
| validity_correlation | 0.967 | 0.968 |

## Plots

### Summary Dashboard

<table><tr>
<td><b>A</b><br>![Summary Dashboard A](../experiments/exp_043_eu_precautionary_sanctions_v2/plots/summary_dashboard.png)</td>
<td><b>B</b><br>![Summary Dashboard B](../experiments/exp_044_us_lighttouch_sanctions_v2/plots/summary_dashboard.png)</td>
</tr></table>

### Provider Dashboard

<table><tr>
<td><b>A</b><br>![Provider Dashboard A](../experiments/exp_043_eu_precautionary_sanctions_v2/plots/provider_dashboard.png)</td>
<td><b>B</b><br>![Provider Dashboard B](../experiments/exp_044_us_lighttouch_sanctions_v2/plots/provider_dashboard.png)</td>
</tr></table>

### Consumer Dashboard

<table><tr>
<td><b>A</b><br>![Consumer Dashboard A](../experiments/exp_043_eu_precautionary_sanctions_v2/plots/consumer_dashboard.png)</td>
<td><b>B</b><br>![Consumer Dashboard B](../experiments/exp_044_us_lighttouch_sanctions_v2/plots/consumer_dashboard.png)</td>
</tr></table>

### Policymaker Dashboard

<table><tr>
<td><b>A</b><br>![Policymaker Dashboard A](../experiments/exp_043_eu_precautionary_sanctions_v2/plots/policymaker_dashboard.png)</td>
<td><b>B</b><br>![Policymaker Dashboard B](../experiments/exp_044_us_lighttouch_sanctions_v2/plots/policymaker_dashboard.png)</td>
</tr></table>

### Incident Dashboard

<table><tr>
<td><b>A</b><br>![Incident Dashboard A](../experiments/exp_043_eu_precautionary_sanctions_v2/plots/incident_dashboard.png)</td>
<td><b>B</b><br>![Incident Dashboard B](../experiments/exp_044_us_lighttouch_sanctions_v2/plots/incident_dashboard.png)</td>
</tr></table>

### Investment Comparison

<table><tr>
<td><b>A</b><br>![Investment Comparison A](../experiments/exp_043_eu_precautionary_sanctions_v2/plots/investment_comparison.png)</td>
<td><b>B</b><br>![Investment Comparison B](../experiments/exp_044_us_lighttouch_sanctions_v2/plots/investment_comparison.png)</td>
</tr></table>

### Funder Dashboard

<table><tr>
<td><b>A</b><br>![Funder Dashboard A](../experiments/exp_043_eu_precautionary_sanctions_v2/plots/funder_dashboard.png)</td>
<td><b>B</b><br>![Funder Dashboard B](../experiments/exp_044_us_lighttouch_sanctions_v2/plots/funder_dashboard.png)</td>
</tr></table>

### Evaluator Dashboard

<table><tr>
<td><b>A</b><br>![Evaluator Dashboard A](../experiments/exp_043_eu_precautionary_sanctions_v2/plots/evaluator_dashboard.png)</td>
<td><b>B</b><br>![Evaluator Dashboard B](../experiments/exp_044_us_lighttouch_sanctions_v2/plots/evaluator_dashboard.png)</td>
</tr></table>

### Media Dashboard

<table><tr>
<td><b>A</b><br>![Media Dashboard A](../experiments/exp_043_eu_precautionary_sanctions_v2/plots/media_dashboard.png)</td>
<td><b>B</b><br>![Media Dashboard B](../experiments/exp_044_us_lighttouch_sanctions_v2/plots/media_dashboard.png)</td>
</tr></table>

### Validity Over Time

<table><tr>
<td><b>A</b><br>![Validity Over Time A](../experiments/exp_043_eu_precautionary_sanctions_v2/plots/validity_over_time.png)</td>
<td><b>B</b><br>![Validity Over Time B](../experiments/exp_044_us_lighttouch_sanctions_v2/plots/validity_over_time.png)</td>
</tr></table>

### Incident Analysis Dashboard

<table><tr>
<td><b>A</b><br>![Incident Analysis Dashboard A](../experiments/exp_043_eu_precautionary_sanctions_v2/plots/incident_analysis_dashboard.png)</td>
<td><b>B</b><br>![Incident Analysis Dashboard B](../experiments/exp_044_us_lighttouch_sanctions_v2/plots/incident_analysis_dashboard.png)</td>
</tr></table>
