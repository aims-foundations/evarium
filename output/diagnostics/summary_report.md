# Simulation Diagnostics Report

Experiments analyzed: 15

## Pattern-Oriented Validation

| Pattern | full_ecosystem_us | full_ecosystem_eu | full_ecosystem_us | ablation_no_media_ | ablation_no_incide | ablation_no_startu | ablation_no_openco | ablation_single_be | ablation_no_funder | ablation_no_benchm | full_ecosystem_bal | ablation_eval_as_c | full_ecosystem_bal | full_ecosystem_us | full_ecosystem_eu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Benchmark Turnover | PASS | PASS | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | FAIL | PASS | PASS | PASS | PASS | PASS |
| Score Inflation | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Safety Incident Response | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS |
| Gaming Persistence | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | FAIL | FAIL | FAIL |
| Commoditization Shock | PASS | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Regulatory Escalation | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Funding Follows Scores | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | PASS | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL |

## Role Adherence

- **exp_001_full_ecosystem_us**: 82 violations
- **exp_002_full_ecosystem_eu**: 87 violations
- **exp_003_full_ecosystem_us**: 92 violations
- **exp_004_ablation_no_media_balanced**: 74 violations
- **exp_005_ablation_no_incidents_balanced**: 83 violations
- **exp_006_ablation_no_startups_balanced**: 83 violations
- **exp_007_ablation_no_opencore_balanced**: 52 violations
- **exp_008_ablation_single_benchmark_balanced**: 98 violations
- **exp_009_ablation_no_funders_balanced**: 70 violations
- **exp_010_ablation_no_benchmark_evolution_balanced**: 67 violations
- **exp_011_full_ecosystem_balanced**: 107 violations
- **exp_012_ablation_eval_as_company_balanced**: 74 violations
- **exp_013_full_ecosystem_balanced**: 206 violations
- **exp_014_full_ecosystem_us**: 225 violations
- **exp_015_full_ecosystem_eu**: 182 violations

## Strategy Drift (mean cosine distance)

| Provider | full_ecosystem_us | full_ecosystem_eu | full_ecosystem_us | ablation_no_media_ | ablation_no_incide | ablation_no_startu | ablation_no_openco | ablation_single_be | ablation_no_funder | ablation_no_benchm | full_ecosystem_bal | ablation_eval_as_c | full_ecosystem_bal | full_ecosystem_us | full_ecosystem_eu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Apex AI | 0.0081 | 0.0105 | 0.0067 | 0.0107 | 0.0075 | 0.0107 | 0.0188 | 0.0104 | 0.0073 | 0.0070 | 0.0065 | 0.0116 | 0.0076 | 0.0076 | 0.0089 |
| FourAI | 0.0006 | N/A | 0.0006 | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | 0.0123 | N/A |
| Genesis Systems | 0.0115 | 0.0095 | 0.0142 | 0.0063 | 0.0096 | 0.0073 | 0.0174 | 0.0116 | 0.0081 | 0.0077 | 0.0077 | 0.0083 | 0.0061 | 0.0087 | 0.0068 |
| Mirage AI | 0.0074 | 0.0103 | 0.0116 | 0.0071 | 0.0105 | 0.0092 | 0.0197 | 0.0182 | 0.0093 | 0.0097 | 0.0096 | 0.0114 | 0.0088 | 0.0080 | 0.0088 |
| OneAI | 0.0013 | 0.0002 | 0.0018 | 0.0056 | 0.0006 | N/A | 0.0005 | 0.0007 | 0.0060 | 0.0008 | 0.0006 | 0.0055 | 0.0075 | 0.0078 | 0.0106 |
| OpenCore | 0.0091 | 0.0102 | 0.0116 | 0.0127 | 0.0088 | 0.0183 | N/A | 0.0219 | 0.0098 | 0.0096 | 0.0126 | 0.0101 | 0.0095 | 0.0096 | 0.0088 |
| Orion Labs | 0.0043 | 0.0067 | 0.0091 | 0.0061 | 0.0089 | 0.0107 | 0.0182 | 0.0092 | 0.0081 | 0.0072 | 0.0070 | 0.0094 | 0.0072 | 0.0094 | 0.0083 |
| ThreeAI | 0.0010 | N/A | 0.0004 | 0.0006 | 0.0006 | N/A | 0.0004 | 0.0006 | 0.0007 | 0.0006 | 0.0006 | 0.0006 | 0.0099 | 0.0133 | N/A |
| TwoAI | 0.0002 | 0.0011 | 0.0002 | 0.0022 | 0.0023 | N/A | 0.0006 | 0.0015 | 0.0027 | 0.0021 | 0.0022 | 0.0021 | 0.0084 | 0.0087 | 0.0131 |