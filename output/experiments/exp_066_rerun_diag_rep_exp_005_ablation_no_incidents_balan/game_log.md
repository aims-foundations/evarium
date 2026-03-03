# Game Log: rerun_diag_rep_exp_005_ablation_no_incidents_balanced

**Experiment ID:** exp_066_rerun_diag_rep_exp_005_ablation_no_incidents_balan
**Mode:** Heuristic
**Total Rounds:** 30

**Benchmarks (4):**
- **coding**: validity=0.7, exploitability=0.25, weight=1.0
- **reasoning**: validity=0.7, exploitability=0.25, weight=1.0
- **math**: validity=0.7, exploitability=0.25, weight=1.0
- **safety**: validity=0.7, exploitability=0.25, weight=1.0

---

## Round 0

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.326 | 0.260 | 45% | 30% | 10% | 15% |
| 2 | Apex AI | 0.290 | 0.270 | 30% | 20% | 10% | 40% |
| 3 | Mirage AI | 0.287 | 0.240 | 20% | 45% | 25% | 10% |
| 4 | Orion Labs | 0.268 | 0.270 | 25% | 30% | 20% | 25% |
| 5 | OpenCore | 0.234 | 0.210 | 20% | 40% | 35% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Genesis Systems | 0.342 | 0.486 | 0.323 | 0.152 |
| Apex AI | 0.389 | 0.312 | 0.214 | 0.245 |
| Mirage AI | 0.218 | 0.462 | 0.364 | 0.104 |
| Orion Labs | 0.293 | 0.188 | 0.260 | 0.330 |
| OpenCore | 0.300 | 0.155 | 0.275 | 0.205 |

### Other Actor Reasoning
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems

### Consumer Market
- Avg Satisfaction: 0.322
- Switching Rate: 27.3%
- Market Shares: Genesis Systems: 45.1%, Orion Labs: 19.6%, Apex AI: 17.5%, Mirage AI: 12.8%, OpenCore: 5.0%

---

## Round 1

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.365 | 0.247 | 18% | 45% | 32% | 5% |
| 2 | Genesis Systems | 0.336 | 0.274 | 45% | 30% | 15% | 10% |
| 3 | Apex AI | 0.330 | 0.278 | 29% | 20% | 11% | 40% |
| 4 | Orion Labs | 0.309 | 0.276 | 24% | 30% | 21% | 25% |
| 5 | OpenCore | 0.292 | 0.216 | 16% | 37% | 44% | 3% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Mirage AI | 0.223 | 0.462 | 0.364 | 0.410 |
| Genesis Systems | 0.342 | 0.486 | 0.323 | 0.193 |
| Apex AI | 0.389 | 0.312 | 0.290 | 0.328 |
| Orion Labs | 0.458 | 0.188 | 0.260 | 0.330 |
| OpenCore | 0.402 | 0.155 | 0.408 | 0.205 |

### Score Changes
- **Orion Labs**: 0.268 -> 0.309 (+0.041)
- **Apex AI**: 0.290 -> 0.330 (+0.040)
- **Genesis Systems**: 0.326 -> 0.336 (+0.010)
- **Mirage AI**: 0.287 -> 0.365 (+0.078)
- **OpenCore**: 0.234 -> 0.292 (+0.059)

### Events
- **Mirage AI** moved up from #3 to #1
- **Genesis Systems** moved down from #1 to #2
- **Apex AI** moved down from #2 to #3
- **Regulation** by Regulator: threshold_announcement
- **Consumer movement**: 13.1% of market switched providers

### Other Actor Reasoning
- **Regulator:** threshold_announcement: Proactive threshold signaling (risk=0.40)
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,029,002 to Mirage AI

### Media Coverage
- Sentiment: 0.75 (positive)
- Mirage AI takes the lead from Genesis Systems
- Mirage AI surges by 0.078
- OpenCore surges by 0.059
- Genesis Systems raises $60,000,000 from Horizon_Capital
- Orion Labs takes #1 on coding
- OpenCore takes #1 on math
- Mirage AI takes #1 on safety

### Consumer Market
- Avg Satisfaction: 0.336
- Switching Rate: 13.1%
- Market Shares: Genesis Systems: 48.9%, Orion Labs: 16.9%, Apex AI: 16.1%, Mirage AI: 14.5%, OpenCore: 3.7%

### Regulatory Activity
- **threshold_announcement** by Regulator
  > Proactive threshold signaling (risk=0.40)

---

## Round 2

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.470 | 0.286 | 45% | 30% | 20% | 5% |
| 2 | Mirage AI | 0.438 | 0.256 | 15% | 43% | 37% | 5% |
| 3 | Apex AI | 0.391 | 0.284 | 27% | 20% | 13% | 40% |
| 4 | OpenCore | 0.375 | 0.221 | 12% | 34% | 51% | 3% |
| 5 | Orion Labs | 0.359 | 0.283 | 23% | 30% | 22% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Genesis Systems | 0.548 | 0.486 | 0.444 | 0.402 |
| Mirage AI | 0.332 | 0.462 | 0.548 | 0.410 |
| Apex AI | 0.389 | 0.312 | 0.472 | 0.391 |
| OpenCore | 0.402 | 0.370 | 0.453 | 0.276 |
| Orion Labs | 0.459 | 0.250 | 0.398 | 0.330 |

### Score Changes
- **Orion Labs**: 0.309 -> 0.359 (+0.050)
- **Apex AI**: 0.330 -> 0.391 (+0.061)
- **Genesis Systems**: 0.336 -> 0.470 (+0.134)
- **Mirage AI**: 0.365 -> 0.438 (+0.073)
- **OpenCore**: 0.292 -> 0.375 (+0.083)

### Events
- **Genesis Systems** moved up from #2 to #1
- **Mirage AI** moved down from #1 to #2
- **OpenCore** moved up from #5 to #4
- **Orion Labs** moved down from #4 to #5
- **Consumer movement**: 10.6% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $14,350,932 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,029,002 to Mirage AI

### Media Coverage
- Sentiment: 0.90 (positive)
- Genesis Systems takes the lead from Mirage AI
- Genesis Systems surges by 0.134
- Genesis Systems appears to release major model update
- Mirage AI surges by 0.073
- Apex AI surges by 0.061
- OpenCore surges by 0.083
- OpenCore appears to release major model update
- Orion Labs surges by 0.050
- Regulatory action: threshold_announcement
- Mirage AI raises $180,000,000 from TechVentures
- Mirage AI raises $9,029,002 from OpenResearch_Foundation
- Genesis Systems takes #1 on coding
- Mirage AI takes #1 on math
- Genesis Systems sees surge in adoption (market share +3.8%)
- Risk signals: regulatory_threshold_announcement

### Consumer Market
- Avg Satisfaction: 0.357
- Switching Rate: 10.6%
- Market Shares: Genesis Systems: 52.9%, Mirage AI: 15.7%, Apex AI: 14.7%, Orion Labs: 13.6%, OpenCore: 3.1%

---

## Round 3

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.470 | 0.298 | 42% | 29% | 24% | 5% |
| 2 | Mirage AI | 0.458 | 0.265 | 13% | 41% | 41% | 5% |
| 3 | OpenCore | 0.392 | 0.227 | 9% | 34% | 54% | 3% |
| 4 | Apex AI | 0.391 | 0.289 | 26% | 20% | 14% | 40% |
| 5 | Orion Labs | 0.380 | 0.289 | 21% | 30% | 24% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Genesis Systems | 0.548 | 0.486 | 0.444 | 0.402 |
| Mirage AI | 0.413 | 0.462 | 0.548 | 0.410 |
| OpenCore | 0.470 | 0.370 | 0.453 | 0.276 |
| Apex AI | 0.389 | 0.312 | 0.472 | 0.391 |
| Orion Labs | 0.459 | 0.263 | 0.398 | 0.398 |

### Score Changes
- **Orion Labs**: 0.359 -> 0.380 (+0.020)
- **Apex AI**: 0.391 -> 0.391 (+0.000)
- **Genesis Systems**: 0.470 -> 0.470 (+0.000)
- **Mirage AI**: 0.438 -> 0.458 (+0.020)
- **OpenCore**: 0.375 -> 0.392 (+0.017)

### Events
- **OpenCore** moved up from #4 to #3
- **Apex AI** moved down from #3 to #4
- **Consumer movement**: 8.1% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $14,350,932 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,029,002 to Mirage AI

### Media Coverage
- Sentiment: 0.00 (neutral)
- Genesis Systems raises $14,350,932 from AISI_Fund
- Consumers are turning away from Orion Labs (market share -3.4%)
- Genesis Systems sees surge in adoption (market share +4.1%)

### Consumer Market
- Avg Satisfaction: 0.381
- Switching Rate: 8.1%
- Market Shares: Genesis Systems: 55.7%, Mirage AI: 17.7%, Apex AI: 12.6%, Orion Labs: 11.2%, OpenCore: 2.7%

---

## Round 4

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.477 | 0.308 | 39% | 27% | 29% | 5% |
| 2 | Mirage AI | 0.476 | 0.273 | 11% | 39% | 46% | 5% |
| 3 | OpenCore | 0.458 | 0.231 | 6% | 35% | 56% | 3% |
| 4 | Apex AI | 0.453 | 0.295 | 23% | 20% | 17% | 40% |
| 5 | Orion Labs | 0.405 | 0.294 | 18% | 30% | 27% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Genesis Systems | 0.548 | 0.486 | 0.444 | 0.430 |
| Mirage AI | 0.484 | 0.462 | 0.548 | 0.410 |
| OpenCore | 0.470 | 0.515 | 0.453 | 0.395 |
| Apex AI | 0.389 | 0.559 | 0.472 | 0.391 |
| Orion Labs | 0.459 | 0.364 | 0.398 | 0.398 |

### Score Changes
- **Orion Labs**: 0.380 -> 0.405 (+0.025)
- **Apex AI**: 0.391 -> 0.453 (+0.062)
- **Genesis Systems**: 0.470 -> 0.477 (+0.007)
- **Mirage AI**: 0.458 -> 0.476 (+0.018)
- **OpenCore**: 0.392 -> 0.458 (+0.066)

### Events
- **Regulation** by Regulator: investigation
- **Consumer movement**: 5.5% of market switched providers

### Other Actor Reasoning
- **Regulator:** investigation: Risk elevated (0.75)
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $14,350,932 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,102,013 to OpenCore

### Media Coverage
- Sentiment: 0.40 (positive)
- OpenCore surges by 0.066
- Apex AI surges by 0.062
- Apex AI takes #1 on reasoning
- Genesis Systems takes #1 on safety

### Consumer Market
- Avg Satisfaction: 0.402
- Switching Rate: 5.5%
- Market Shares: Genesis Systems: 58.4%, Mirage AI: 18.2%, Apex AI: 11.1%, Orion Labs: 9.8%, OpenCore: 2.5%

### Regulatory Activity
- **investigation** by Regulator
  > Risk elevated (0.75)

---

## Round 5

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.535 | 0.320 | 36% | 26% | 33% | 5% |
| 2 | OpenCore | 0.490 | 0.236 | 5% | 35% | 56% | 3% |
| 3 | Mirage AI | 0.484 | 0.279 | 8% | 37% | 50% | 5% |
| 4 | Apex AI | 0.464 | 0.300 | 20% | 20% | 20% | 40% |
| 5 | Orion Labs | 0.428 | 0.300 | 14% | 30% | 31% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Genesis Systems | 0.548 | 0.517 | 0.645 | 0.430 |
| OpenCore | 0.470 | 0.515 | 0.579 | 0.395 |
| Mirage AI | 0.517 | 0.462 | 0.548 | 0.410 |
| Apex AI | 0.389 | 0.559 | 0.472 | 0.437 |
| Orion Labs | 0.459 | 0.438 | 0.417 | 0.398 |

### Score Changes
- **Orion Labs**: 0.405 -> 0.428 (+0.023)
- **Apex AI**: 0.453 -> 0.464 (+0.012)
- **Genesis Systems**: 0.477 -> 0.535 (+0.058)
- **Mirage AI**: 0.476 -> 0.484 (+0.008)
- **OpenCore**: 0.458 -> 0.490 (+0.032)

### Events
- **OpenCore** moved up from #3 to #2
- **Mirage AI** moved down from #2 to #3
- **Consumer movement**: 5.2% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $14,350,932 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,102,013 to OpenCore

### Media Coverage
- Sentiment: 0.25 (positive)
- Genesis Systems surges by 0.058
- Regulator launches investigation into elevated_risk
- Genesis Systems raises $180,000,000 from TechVentures
- OpenCore raises $10,102,013 from OpenResearch_Foundation
- Genesis Systems takes #1 on math
- Apex AI takes #1 on safety
- Risk signals: regulatory_investigation

### Consumer Market
- Avg Satisfaction: 0.421
- Switching Rate: 5.2%
- Market Shares: Genesis Systems: 62.9%, Mirage AI: 16.1%, Apex AI: 10.2%, Orion Labs: 8.5%, OpenCore: 2.4%

---

## Round 6

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.550 | 0.331 | 34% | 25% | 37% | 5% |
| 2 | OpenCore | 0.532 | 0.240 | 5% | 36% | 56% | 3% |
| 3 | Mirage AI | 0.509 | 0.285 | 6% | 36% | 53% | 5% |
| 4 | Apex AI | 0.496 | 0.304 | 18% | 20% | 22% | 40% |
| 5 | Orion Labs | 0.428 | 0.304 | 11% | 30% | 34% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.548 | 0.517 | 0.645 | 0.489 | 0.000 |
| OpenCore | 0.470 | 0.515 | 0.579 | 0.565 | 0.000 |
| Mirage AI | 0.615 | 0.462 | 0.548 | 0.410 | 0.000 |
| Apex AI | 0.516 | 0.559 | 0.472 | 0.437 | 0.000 |
| Orion Labs | 0.459 | 0.438 | 0.417 | 0.398 | 0.000 |

### Score Changes
- **Orion Labs**: 0.428 -> 0.428 (+0.000)
- **Apex AI**: 0.464 -> 0.496 (+0.032)
- **Genesis Systems**: 0.535 -> 0.550 (+0.015)
- **Mirage AI**: 0.484 -> 0.509 (+0.025)
- **OpenCore**: 0.490 -> 0.532 (+0.042)

### New Benchmark Introduced
- **writing** introduced (validity=0.72, exploitability=0.30)
  - Trigger: periodic_introduction:round_6

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $15,122,997 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,102,013 to OpenCore

### Media Coverage
- Sentiment: 0.35 (positive)
- New benchmark introduced: writing
- Mirage AI takes #1 on coding
- OpenCore takes #1 on safety
- Genesis Systems sees surge in adoption (market share +4.5%)

### Consumer Market
- Avg Satisfaction: 0.442
- Switching Rate: 4.5%
- Market Shares: Genesis Systems: 67.4%, Mirage AI: 13.7%, Apex AI: 9.1%, Orion Labs: 7.5%, OpenCore: 2.3%

---

## Round 7

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenCore | 0.568 | 0.245 | 5% | 36% | 56% | 3% |
| 2 | Genesis Systems | 0.556 | 0.341 | 32% | 23% | 40% | 5% |
| 3 | Mirage AI | 0.516 | 0.290 | 5% | 35% | 55% | 5% |
| 4 | Apex AI | 0.478 | 0.309 | 15% | 20% | 25% | 40% |
| 5 | Orion Labs | 0.447 | 0.308 | 7% | 30% | 38% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| OpenCore | 0.523 | 0.515 | 0.579 | 0.565 | 0.657 |
| Genesis Systems | 0.695 | 0.517 | 0.645 | 0.489 | 0.435 |
| Mirage AI | 0.678 | 0.462 | 0.548 | 0.439 | 0.455 |
| Apex AI | 0.516 | 0.601 | 0.633 | 0.437 | 0.202 |
| Orion Labs | 0.459 | 0.438 | 0.457 | 0.398 | 0.482 |

### Score Changes
- **Orion Labs**: 0.428 -> 0.447 (+0.019)
- **Apex AI**: 0.496 -> 0.478 (-0.018)
- **Genesis Systems**: 0.550 -> 0.556 (+0.006)
- **Mirage AI**: 0.509 -> 0.516 (+0.008)
- **OpenCore**: 0.532 -> 0.568 (+0.036)

### Events
- **OpenCore** moved up from #2 to #1
- **Genesis Systems** moved down from #1 to #2
- **Regulation** by Regulator: mandate_benchmark
- **Consumer movement**: 14.0% of market switched providers

### Other Actor Reasoning
- **Regulator:** mandate_benchmark: High risk (1.00) with prior investigation
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $15,122,997 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $13,854,675 to OpenCore

### Media Coverage
- Sentiment: 0.35 (positive)
- OpenCore takes the lead from Genesis Systems
- Genesis Systems takes #1 on coding
- Genesis Systems sees surge in adoption (market share +4.5%)

### Consumer Market
- Avg Satisfaction: 0.459
- Switching Rate: 14.0%
- Market Shares: Genesis Systems: 62.1%, OpenCore: 13.6%, Mirage AI: 10.0%, Apex AI: 7.9%, Orion Labs: 6.4%

### Regulatory Activity
- **mandate_benchmark** by Regulator
  > High risk (1.00) with prior investigation

---

## Round 8

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.632 | 0.350 | 29% | 22% | 44% | 5% |
| 2 | Mirage AI | 0.591 | 0.330 | 5% | 35% | 55% | 5% |
| 3 | OpenCore | 0.568 | 0.250 | 5% | 37% | 55% | 3% |
| 4 | Apex AI | 0.528 | 0.313 | 12% | 20% | 28% | 40% |
| 5 | Orion Labs | 0.527 | 0.313 | 5% | 29% | 41% | 24% |
| 6 | OneAI | 0.250 | 0.190 | 20% | 35% | 35% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.695 | 0.517 | 0.645 | 0.489 | 0.814 |
| Mirage AI | 0.678 | 0.575 | 0.614 | 0.439 | 0.651 |
| OpenCore | 0.523 | 0.515 | 0.579 | 0.565 | 0.657 |
| Apex AI | 0.557 | 0.601 | 0.633 | 0.510 | 0.340 |
| Orion Labs | 0.501 | 0.523 | 0.457 | 0.398 | 0.759 |
| OneAI | 0.346 | 0.205 | 0.234 | 0.210 | 0.255 |

### Score Changes
- **Orion Labs**: 0.447 -> 0.527 (+0.081)
- **Apex AI**: 0.478 -> 0.528 (+0.050)
- **Genesis Systems**: 0.556 -> 0.632 (+0.076)
- **Mirage AI**: 0.516 -> 0.591 (+0.075)
- **OpenCore**: 0.568 -> 0.568 (+0.000)
- **OneAI**: 0.250 -> 0.250 (+0.000)

### Events
- **Genesis Systems** moved up from #2 to #1
- **Mirage AI** moved up from #3 to #2
- **OpenCore** moved down from #1 to #3
- **Consumer movement**: 9.6% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $15,122,997 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $13,854,675 to OpenCore

### Media Coverage
- Sentiment: 0.45 (positive)
- Genesis Systems takes the lead from OpenCore
- Genesis Systems surges by 0.076
- Mirage AI surges by 0.075
- Apex AI surges by 0.050
- Orion Labs surges by 0.081
- Orion Labs appears to release major model update
- Regulator mandates new benchmark standards
- OpenCore raises $13,854,675 from OpenResearch_Foundation
- Genesis Systems takes #1 on writing
- Consumers are turning away from Genesis Systems (market share -5.2%)
- Consumers are turning away from Mirage AI (market share -3.7%)
- OpenCore sees surge in adoption (market share +11.3%)
- Risk signals: regulatory_mandate_benchmark

### Consumer Market
- Avg Satisfaction: 0.491
- Switching Rate: 9.6%
- Market Shares: Genesis Systems: 66.1%, OpenCore: 12.4%, Mirage AI: 7.8%, Apex AI: 7.5%, Orion Labs: 5.9%, OneAI: 0.3%

---

## Round 9

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.656 | 0.359 | 27% | 21% | 47% | 5% |
| 2 | Mirage AI | 0.625 | 0.335 | 5% | 35% | 55% | 5% |
| 3 | OpenCore | 0.568 | 0.255 | 5% | 37% | 55% | 3% |
| 4 | Orion Labs | 0.549 | 0.317 | 5% | 28% | 44% | 23% |
| 5 | Apex AI | 0.528 | 0.316 | 8% | 20% | 32% | 40% |
| 6 | OneAI | 0.364 | 0.195 | 7% | 35% | 48% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.695 | 0.635 | 0.645 | 0.489 | 0.814 |
| Mirage AI | 0.678 | 0.575 | 0.614 | 0.551 | 0.707 |
| OpenCore | 0.523 | 0.515 | 0.579 | 0.565 | 0.657 |
| Orion Labs | 0.501 | 0.586 | 0.469 | 0.431 | 0.759 |
| Apex AI | 0.557 | 0.601 | 0.633 | 0.510 | 0.340 |
| OneAI | 0.346 | 0.402 | 0.295 | 0.210 | 0.564 |

### Score Changes
- **Orion Labs**: 0.527 -> 0.549 (+0.022)
- **Apex AI**: 0.528 -> 0.528 (+0.000)
- **Genesis Systems**: 0.632 -> 0.656 (+0.024)
- **Mirage AI**: 0.591 -> 0.625 (+0.033)
- **OpenCore**: 0.568 -> 0.568 (+0.000)
- **OneAI**: 0.250 -> 0.364 (+0.114)

### Events
- **Orion Labs** moved up from #5 to #4
- **Apex AI** moved down from #4 to #5
- **Consumer movement**: 6.3% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $15,122,997 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $13,854,675 to OpenCore

### Media Coverage
- Sentiment: 0.25 (positive)
- OneAI surges by 0.114
- OneAI appears to release major model update
- Genesis Systems takes #1 on reasoning
- Genesis Systems sees surge in adoption (market share +3.9%)

### Consumer Market
- Avg Satisfaction: 0.527
- Switching Rate: 6.3%
- Market Shares: Genesis Systems: 69.7%, OpenCore: 11.1%, Apex AI: 6.7%, Mirage AI: 6.7%, Orion Labs: 5.5%, OneAI: 0.2%

---

## Round 10

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.667 | 0.367 | 26% | 20% | 49% | 5% |
| 2 | Mirage AI | 0.625 | 0.339 | 5% | 35% | 55% | 5% |
| 3 | OpenCore | 0.568 | 0.259 | 5% | 37% | 55% | 3% |
| 4 | Orion Labs | 0.549 | 0.322 | 5% | 27% | 46% | 22% |
| 5 | Apex AI | 0.534 | 0.319 | 5% | 20% | 35% | 40% |
| 6 | OneAI | 0.391 | 0.199 | 5% | 33% | 52% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.695 | 0.635 | 0.645 | 0.544 | 0.814 |
| Mirage AI | 0.678 | 0.575 | 0.614 | 0.551 | 0.707 |
| OpenCore | 0.523 | 0.515 | 0.579 | 0.565 | 0.657 |
| Orion Labs | 0.501 | 0.586 | 0.469 | 0.431 | 0.759 |
| Apex AI | 0.586 | 0.601 | 0.633 | 0.510 | 0.340 |
| OneAI | 0.451 | 0.402 | 0.305 | 0.229 | 0.564 |

### Score Changes
- **Orion Labs**: 0.549 -> 0.549 (+0.000)
- **Apex AI**: 0.528 -> 0.534 (+0.006)
- **Genesis Systems**: 0.656 -> 0.667 (+0.011)
- **Mirage AI**: 0.625 -> 0.625 (+0.000)
- **OpenCore**: 0.568 -> 0.568 (+0.000)
- **OneAI**: 0.364 -> 0.391 (+0.027)

### Events
- **Regulation** by Regulator: public_warning

### Other Actor Reasoning
- **Regulator:** public_warning: Follow-up to investigation, risk at 1.00
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $15,372,339 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $8,653,441 to Genesis Systems

### Media Coverage
- Sentiment: 0.05 (neutral)
- Genesis Systems sees surge in adoption (market share +3.7%)

### Consumer Market
- Avg Satisfaction: 0.554
- Switching Rate: 4.1%
- Market Shares: Genesis Systems: 73.9%, OpenCore: 8.2%, Apex AI: 6.2%, Mirage AI: 6.0%, Orion Labs: 5.4%, OneAI: 0.2%

### Regulatory Activity
- **public_warning** by Regulator
  > Follow-up to investigation, risk at 1.00

---

## Round 11

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.698 | 0.375 | 24% | 19% | 52% | 5% |
| 2 | Mirage AI | 0.625 | 0.344 | 5% | 35% | 55% | 5% |
| 3 | Apex AI | 0.607 | 0.322 | 5% | 19% | 38% | 38% |
| 4 | OpenCore | 0.568 | 0.264 | 5% | 37% | 55% | 3% |
| 5 | Orion Labs | 0.549 | 0.325 | 5% | 26% | 48% | 21% |
| 6 | OneAI | 0.500 | 0.205 | 5% | 32% | 53% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.695 | 0.716 | 0.673 | 0.591 | 0.814 |
| Mirage AI | 0.678 | 0.575 | 0.614 | 0.551 | 0.707 |
| Apex AI | 0.586 | 0.601 | 0.633 | 0.612 | 0.600 |
| OpenCore | 0.523 | 0.515 | 0.579 | 0.565 | 0.657 |
| Orion Labs | 0.501 | 0.586 | 0.469 | 0.431 | 0.759 |
| OneAI | 0.539 | 0.402 | 0.527 | 0.438 | 0.594 |

### Score Changes
- **Orion Labs**: 0.549 -> 0.549 (+0.000)
- **Apex AI**: 0.534 -> 0.607 (+0.072)
- **Genesis Systems**: 0.667 -> 0.698 (+0.031)
- **Mirage AI**: 0.625 -> 0.625 (+0.000)
- **OpenCore**: 0.568 -> 0.568 (+0.000)
- **OneAI**: 0.391 -> 0.500 (+0.110)

### Events
- **Apex AI** moved up from #5 to #3
- **OpenCore** moved down from #3 to #4
- **Orion Labs** moved down from #4 to #5

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $15,372,339 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $8,653,441 to Genesis Systems

### Media Coverage
- Sentiment: 0.25 (positive)
- Apex AI surges by 0.072
- OneAI surges by 0.110
- OneAI appears to release major model update
- Regulator issues public warning about AI safety concerns
- Genesis Systems raises $8,653,441 from OpenResearch_Foundation
- Apex AI takes #1 on safety
- Genesis Systems sees surge in adoption (market share +4.1%)
- Risk signals: regulatory_public_warning

### Consumer Market
- Avg Satisfaction: 0.580
- Switching Rate: 3.5%
- Market Shares: Genesis Systems: 77.3%, OpenCore: 6.2%, Apex AI: 5.9%, Mirage AI: 5.5%, Orion Labs: 4.9%, OneAI: 0.2%

---

## Round 12

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.702 | 0.383 | 24% | 18% | 53% | 5% |
| 2 | Mirage AI | 0.625 | 0.348 | 5% | 35% | 55% | 5% |
| 3 | Apex AI | 0.607 | 0.325 | 5% | 18% | 40% | 37% |
| 4 | Orion Labs | 0.569 | 0.329 | 5% | 24% | 50% | 20% |
| 5 | OpenCore | 0.568 | 0.269 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.503 | 0.210 | 5% | 32% | 54% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.695 | 0.731 | 0.673 | 0.596 | 0.814 | 0.000 |
| Mirage AI | 0.678 | 0.575 | 0.614 | 0.551 | 0.707 | 0.000 |
| Apex AI | 0.586 | 0.601 | 0.633 | 0.612 | 0.600 | 0.000 |
| Orion Labs | 0.501 | 0.586 | 0.540 | 0.458 | 0.759 | 0.000 |
| OpenCore | 0.523 | 0.515 | 0.579 | 0.565 | 0.657 | 0.000 |
| OneAI | 0.539 | 0.402 | 0.527 | 0.453 | 0.594 | 0.000 |

### Score Changes
- **Orion Labs**: 0.549 -> 0.569 (+0.020)
- **Apex AI**: 0.607 -> 0.607 (+0.000)
- **Genesis Systems**: 0.698 -> 0.702 (+0.004)
- **Mirage AI**: 0.625 -> 0.625 (+0.000)
- **OpenCore**: 0.568 -> 0.568 (+0.000)
- **OneAI**: 0.500 -> 0.503 (+0.003)

### Events
- **Orion Labs** moved up from #5 to #4
- **OpenCore** moved down from #4 to #5

### New Benchmark Introduced
- **medical** introduced (validity=0.78, exploitability=0.18)
  - Trigger: periodic_introduction:round_12

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $15,372,339 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $8,653,441 to Genesis Systems

### Media Coverage
- Sentiment: 0.15 (positive)
- New benchmark introduced: medical
- Genesis Systems sees surge in adoption (market share +3.4%)

### Consumer Market
- Avg Satisfaction: 0.601
- Switching Rate: 2.0%
- Market Shares: Genesis Systems: 79.3%, Apex AI: 5.7%, Mirage AI: 5.1%, Orion Labs: 4.9%, OpenCore: 4.9%, OneAI: 0.2%

---

## Round 13

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.669 | 0.391 | 24% | 18% | 53% | 5% |
| 2 | Mirage AI | 0.609 | 0.352 | 5% | 35% | 55% | 5% |
| 3 | Orion Labs | 0.598 | 0.332 | 5% | 23% | 52% | 19% |
| 4 | Apex AI | 0.591 | 0.328 | 5% | 18% | 43% | 35% |
| 5 | OpenCore | 0.529 | 0.273 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.511 | 0.215 | 5% | 32% | 54% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.695 | 0.731 | 0.673 | 0.596 | 0.814 | 0.507 |
| Mirage AI | 0.678 | 0.678 | 0.614 | 0.551 | 0.784 | 0.348 |
| Orion Labs | 0.501 | 0.586 | 0.680 | 0.458 | 0.759 | 0.604 |
| Apex AI | 0.586 | 0.601 | 0.633 | 0.612 | 0.718 | 0.396 |
| OpenCore | 0.523 | 0.539 | 0.579 | 0.565 | 0.657 | 0.309 |
| OneAI | 0.539 | 0.437 | 0.527 | 0.453 | 0.594 | 0.513 |

### Score Changes
- **Orion Labs**: 0.569 -> 0.598 (+0.029)
- **Apex AI**: 0.607 -> 0.591 (-0.015)
- **Genesis Systems**: 0.702 -> 0.669 (-0.032)
- **Mirage AI**: 0.625 -> 0.609 (-0.016)
- **OpenCore**: 0.568 -> 0.529 (-0.039)
- **OneAI**: 0.503 -> 0.511 (+0.007)

### Events
- **Orion Labs** moved up from #4 to #3
- **Apex AI** moved down from #3 to #4
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 6 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $15,372,339 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $8,600,002 to Genesis Systems

### Media Coverage
- Sentiment: 0.10 (neutral)
- Orion Labs takes #1 on math

### Consumer Market
- Avg Satisfaction: 0.619
- Switching Rate: 1.6%
- Market Shares: Genesis Systems: 80.8%, Apex AI: 5.5%, Mirage AI: 4.8%, Orion Labs: 4.7%, OpenCore: 3.9%, OneAI: 0.2%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 6 rounds ago

---

## Round 14

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.676 | 0.399 | 24% | 17% | 53% | 5% |
| 2 | Mirage AI | 0.614 | 0.357 | 5% | 35% | 55% | 5% |
| 3 | Apex AI | 0.606 | 0.330 | 5% | 17% | 45% | 34% |
| 4 | Orion Labs | 0.598 | 0.335 | 5% | 23% | 54% | 19% |
| 5 | OpenCore | 0.529 | 0.278 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.511 | 0.220 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.695 | 0.731 | 0.673 | 0.596 | 0.814 | 0.545 |
| Mirage AI | 0.678 | 0.678 | 0.614 | 0.551 | 0.784 | 0.380 |
| Apex AI | 0.586 | 0.601 | 0.633 | 0.612 | 0.718 | 0.486 |
| Orion Labs | 0.501 | 0.586 | 0.680 | 0.458 | 0.759 | 0.604 |
| OpenCore | 0.523 | 0.539 | 0.579 | 0.565 | 0.657 | 0.309 |
| OneAI | 0.539 | 0.437 | 0.527 | 0.453 | 0.594 | 0.513 |

### Score Changes
- **Orion Labs**: 0.598 -> 0.598 (+0.000)
- **Apex AI**: 0.591 -> 0.606 (+0.015)
- **Genesis Systems**: 0.669 -> 0.676 (+0.006)
- **Mirage AI**: 0.609 -> 0.614 (+0.005)
- **OpenCore**: 0.529 -> 0.529 (+0.000)
- **OneAI**: 0.511 -> 0.511 (+0.000)

### Events
- **Apex AI** moved up from #4 to #3
- **Orion Labs** moved down from #3 to #4

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $13,657,129 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $8,600,002 to Genesis Systems

### Media Coverage
- Sentiment: -0.15 (negative)
- Regulator initiates compliance audit on AI providers
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.625
- Switching Rate: 0.9%
- Market Shares: Genesis Systems: 81.8%, Apex AI: 5.4%, Orion Labs: 4.7%, Mirage AI: 4.6%, OpenCore: 3.3%, OneAI: 0.2%

---

## Round 15

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.677 | 0.406 | 25% | 17% | 53% | 5% |
| 2 | Mirage AI | 0.627 | 0.361 | 5% | 35% | 55% | 5% |
| 3 | Apex AI | 0.606 | 0.333 | 5% | 16% | 46% | 33% |
| 4 | Orion Labs | 0.599 | 0.339 | 5% | 22% | 54% | 19% |
| 5 | OpenCore | 0.562 | 0.283 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.511 | 0.225 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.695 | 0.731 | 0.673 | 0.596 | 0.814 | 0.554 |
| Mirage AI | 0.678 | 0.678 | 0.614 | 0.551 | 0.784 | 0.459 |
| Apex AI | 0.586 | 0.601 | 0.633 | 0.612 | 0.718 | 0.486 |
| Orion Labs | 0.505 | 0.586 | 0.680 | 0.458 | 0.759 | 0.604 |
| OpenCore | 0.523 | 0.627 | 0.579 | 0.565 | 0.657 | 0.418 |
| OneAI | 0.539 | 0.437 | 0.527 | 0.453 | 0.594 | 0.513 |

### Score Changes
- **Orion Labs**: 0.598 -> 0.599 (+0.001)
- **Apex AI**: 0.606 -> 0.606 (+0.000)
- **Genesis Systems**: 0.676 -> 0.677 (+0.002)
- **Mirage AI**: 0.614 -> 0.627 (+0.013)
- **OpenCore**: 0.529 -> 0.562 (+0.033)
- **OneAI**: 0.511 -> 0.511 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $13,657,129 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $8,600,002 to Genesis Systems

### Media Coverage
- Sentiment: 0.05 (neutral)
- Genesis Systems raises $13,657,129 from AISI_Fund

### Consumer Market
- Avg Satisfaction: 0.634
- Switching Rate: 0.9%
- Market Shares: Genesis Systems: 82.7%, Apex AI: 5.3%, Orion Labs: 4.5%, Mirage AI: 4.5%, OpenCore: 2.9%, OneAI: 0.1%

---

## Round 16

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.677 | 0.414 | 26% | 16% | 53% | 5% |
| 2 | Mirage AI | 0.637 | 0.365 | 5% | 35% | 55% | 5% |
| 3 | Apex AI | 0.606 | 0.335 | 5% | 16% | 48% | 32% |
| 4 | Orion Labs | 0.604 | 0.342 | 5% | 22% | 54% | 18% |
| 5 | OpenCore | 0.564 | 0.287 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.511 | 0.230 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.695 | 0.731 | 0.673 | 0.596 | 0.814 | 0.554 |
| Mirage AI | 0.678 | 0.678 | 0.614 | 0.569 | 0.784 | 0.501 |
| Apex AI | 0.586 | 0.601 | 0.633 | 0.612 | 0.718 | 0.486 |
| Orion Labs | 0.538 | 0.586 | 0.680 | 0.458 | 0.759 | 0.604 |
| OpenCore | 0.540 | 0.627 | 0.579 | 0.565 | 0.657 | 0.418 |
| OneAI | 0.539 | 0.437 | 0.527 | 0.453 | 0.594 | 0.513 |

### Score Changes
- **Orion Labs**: 0.599 -> 0.604 (+0.006)
- **Apex AI**: 0.606 -> 0.606 (+0.000)
- **Genesis Systems**: 0.677 -> 0.677 (+0.000)
- **Mirage AI**: 0.627 -> 0.637 (+0.010)
- **OpenCore**: 0.562 -> 0.564 (+0.003)
- **OneAI**: 0.511 -> 0.511 (+0.000)

### Events
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 9 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $13,657,129 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $8,721,888 to Genesis Systems

### Consumer Market
- Avg Satisfaction: 0.640
- Switching Rate: 0.5%
- Market Shares: Genesis Systems: 83.1%, Apex AI: 5.2%, Orion Labs: 4.5%, Mirage AI: 4.3%, OpenCore: 2.7%, OneAI: 0.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 9 rounds ago

---

## Round 17

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.677 | 0.422 | 26% | 16% | 53% | 5% |
| 2 | Mirage AI | 0.647 | 0.371 | 5% | 35% | 55% | 5% |
| 3 | Apex AI | 0.606 | 0.338 | 5% | 15% | 49% | 31% |
| 4 | Orion Labs | 0.604 | 0.345 | 5% | 22% | 55% | 18% |
| 5 | OpenCore | 0.564 | 0.292 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.511 | 0.234 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.695 | 0.731 | 0.673 | 0.596 | 0.814 | 0.554 |
| Mirage AI | 0.678 | 0.678 | 0.614 | 0.569 | 0.784 | 0.560 |
| Apex AI | 0.586 | 0.601 | 0.633 | 0.612 | 0.718 | 0.486 |
| Orion Labs | 0.538 | 0.586 | 0.680 | 0.458 | 0.759 | 0.604 |
| OpenCore | 0.540 | 0.627 | 0.579 | 0.565 | 0.657 | 0.418 |
| OneAI | 0.539 | 0.437 | 0.527 | 0.453 | 0.594 | 0.513 |

### Score Changes
- **Orion Labs**: 0.604 -> 0.604 (+0.000)
- **Apex AI**: 0.606 -> 0.606 (+0.000)
- **Genesis Systems**: 0.677 -> 0.677 (+0.000)
- **Mirage AI**: 0.637 -> 0.647 (+0.010)
- **OpenCore**: 0.564 -> 0.564 (+0.000)
- **OneAI**: 0.511 -> 0.511 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $13,657,129 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $8,721,888 to Genesis Systems

### Media Coverage
- Sentiment: -0.15 (negative)
- Regulator initiates compliance audit on AI providers
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.643
- Switching Rate: 0.7%
- Market Shares: Genesis Systems: 83.8%, Apex AI: 5.1%, Orion Labs: 4.3%, Mirage AI: 4.2%, OpenCore: 2.5%, OneAI: 0.1%

---

## Round 18

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.690 | 0.430 | 26% | 15% | 53% | 5% |
| 2 | Mirage AI | 0.669 | 0.376 | 5% | 35% | 55% | 5% |
| 3 | Orion Labs | 0.616 | 0.348 | 5% | 22% | 55% | 18% |
| 4 | Apex AI | 0.606 | 0.340 | 5% | 15% | 50% | 30% |
| 5 | OpenCore | 0.572 | 0.296 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.511 | 0.239 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.319 | 0.225 | 20% | 35% | 40% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.695 | 0.731 | 0.673 | 0.649 | 0.814 | 0.579 | 0.000 |
| Mirage AI | 0.678 | 0.678 | 0.746 | 0.569 | 0.784 | 0.560 | 0.000 |
| Orion Labs | 0.538 | 0.586 | 0.680 | 0.529 | 0.759 | 0.604 | 0.000 |
| Apex AI | 0.586 | 0.601 | 0.633 | 0.612 | 0.718 | 0.486 | 0.000 |
| OpenCore | 0.540 | 0.627 | 0.579 | 0.565 | 0.657 | 0.465 | 0.000 |
| OneAI | 0.539 | 0.437 | 0.527 | 0.453 | 0.594 | 0.513 | 0.000 |
| TwoAI | 0.114 | 0.554 | 0.197 | 0.119 | 0.482 | 0.445 | 0.000 |

### Score Changes
- **Orion Labs**: 0.604 -> 0.616 (+0.012)
- **Apex AI**: 0.606 -> 0.606 (+0.000)
- **Genesis Systems**: 0.677 -> 0.690 (+0.013)
- **Mirage AI**: 0.647 -> 0.669 (+0.022)
- **OpenCore**: 0.564 -> 0.572 (+0.008)
- **OneAI**: 0.511 -> 0.511 (+0.000)
- **TwoAI**: 0.319 -> 0.319 (+0.000)

### Events
- **Orion Labs** moved up from #4 to #3
- **Apex AI** moved down from #3 to #4

### New Benchmark Introduced
- **legal** introduced (validity=0.76, exploitability=0.20)
  - Trigger: periodic_introduction:round_18

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $13,512,341 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $8,721,888 to Genesis Systems

### Media Coverage
- Sentiment: 0.30 (positive)
- New benchmark introduced: legal
- Mirage AI takes #1 on math
- Genesis Systems takes #1 on safety

### Consumer Market
- Avg Satisfaction: 0.648
- Switching Rate: 0.9%
- Market Shares: Genesis Systems: 83.9%, Apex AI: 5.0%, Orion Labs: 4.2%, Mirage AI: 4.1%, OpenCore: 2.3%, TwoAI: 0.3%, OneAI: 0.1%

---

## Round 19

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.675 | 0.437 | 27% | 15% | 54% | 5% |
| 2 | Mirage AI | 0.650 | 0.381 | 5% | 35% | 55% | 5% |
| 3 | Orion Labs | 0.599 | 0.351 | 5% | 22% | 55% | 18% |
| 4 | Apex AI | 0.589 | 0.343 | 5% | 15% | 51% | 29% |
| 5 | OpenCore | 0.558 | 0.301 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.475 | 0.243 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.370 | 0.230 | 7% | 34% | 54% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.695 | 0.731 | 0.673 | 0.666 | 0.814 | 0.579 | 0.570 |
| Mirage AI | 0.678 | 0.678 | 0.746 | 0.569 | 0.784 | 0.560 | 0.536 |
| Orion Labs | 0.538 | 0.586 | 0.680 | 0.529 | 0.759 | 0.604 | 0.498 |
| Apex AI | 0.586 | 0.601 | 0.633 | 0.612 | 0.718 | 0.486 | 0.489 |
| OpenCore | 0.540 | 0.627 | 0.579 | 0.565 | 0.657 | 0.465 | 0.473 |
| OneAI | 0.539 | 0.437 | 0.527 | 0.453 | 0.594 | 0.513 | 0.262 |
| TwoAI | 0.291 | 0.554 | 0.197 | 0.119 | 0.482 | 0.445 | 0.499 |

### Score Changes
- **Orion Labs**: 0.616 -> 0.599 (-0.017)
- **Apex AI**: 0.606 -> 0.589 (-0.017)
- **Genesis Systems**: 0.690 -> 0.675 (-0.015)
- **Mirage AI**: 0.669 -> 0.650 (-0.019)
- **OpenCore**: 0.572 -> 0.558 (-0.014)
- **OneAI**: 0.511 -> 0.475 (-0.036)
- **TwoAI**: 0.319 -> 0.370 (+0.051)

### Events
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 12 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to TwoAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $13,512,341 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,430,863 to TwoAI

### Media Coverage
- Sentiment: 0.10 (neutral)
- TwoAI surges by 0.051

### Consumer Market
- Avg Satisfaction: 0.654
- Switching Rate: 0.6%
- Market Shares: Genesis Systems: 84.5%, Apex AI: 4.9%, Orion Labs: 4.1%, Mirage AI: 4.0%, OpenCore: 2.2%, TwoAI: 0.2%, OneAI: 0.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 12 rounds ago

---

## Round 20

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.676 | 0.444 | 27% | 15% | 54% | 5% |
| 2 | Mirage AI | 0.650 | 0.386 | 5% | 35% | 55% | 5% |
| 3 | Orion Labs | 0.606 | 0.355 | 5% | 22% | 55% | 18% |
| 4 | Apex AI | 0.589 | 0.345 | 5% | 14% | 52% | 29% |
| 5 | OpenCore | 0.558 | 0.306 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.479 | 0.247 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.406 | 0.236 | 5% | 35% | 55% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.695 | 0.731 | 0.673 | 0.666 | 0.814 | 0.579 | 0.577 |
| Mirage AI | 0.678 | 0.678 | 0.746 | 0.569 | 0.784 | 0.562 | 0.536 |
| Orion Labs | 0.543 | 0.586 | 0.680 | 0.529 | 0.759 | 0.604 | 0.539 |
| Apex AI | 0.586 | 0.601 | 0.633 | 0.612 | 0.718 | 0.486 | 0.489 |
| OpenCore | 0.540 | 0.627 | 0.579 | 0.565 | 0.657 | 0.465 | 0.473 |
| OneAI | 0.539 | 0.437 | 0.527 | 0.453 | 0.624 | 0.513 | 0.262 |
| TwoAI | 0.306 | 0.554 | 0.268 | 0.284 | 0.482 | 0.445 | 0.499 |

### Score Changes
- **Orion Labs**: 0.599 -> 0.606 (+0.007)
- **Apex AI**: 0.589 -> 0.589 (+0.000)
- **Genesis Systems**: 0.675 -> 0.676 (+0.001)
- **Mirage AI**: 0.650 -> 0.650 (+0.000)
- **OpenCore**: 0.558 -> 0.558 (+0.000)
- **OneAI**: 0.475 -> 0.479 (+0.004)
- **TwoAI**: 0.370 -> 0.406 (+0.036)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to TwoAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $13,512,341 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,430,863 to TwoAI

### Media Coverage
- Sentiment: -0.05 (neutral)
- Regulator initiates compliance audit on AI providers
- TwoAI raises $180,000,000 from TechVentures
- TwoAI raises $7,430,863 from OpenResearch_Foundation
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.655
- Switching Rate: 0.2%
- Market Shares: Genesis Systems: 84.7%, Apex AI: 4.8%, Orion Labs: 4.1%, Mirage AI: 4.0%, OpenCore: 2.1%, TwoAI: 0.2%, OneAI: 0.1%

---

## Round 21

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.676 | 0.451 | 27% | 14% | 54% | 5% |
| 2 | Mirage AI | 0.650 | 0.390 | 5% | 35% | 55% | 5% |
| 3 | Orion Labs | 0.606 | 0.358 | 5% | 22% | 55% | 18% |
| 4 | Apex AI | 0.589 | 0.348 | 5% | 14% | 53% | 28% |
| 5 | OpenCore | 0.558 | 0.310 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.487 | 0.251 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.433 | 0.242 | 5% | 35% | 55% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.695 | 0.731 | 0.673 | 0.666 | 0.814 | 0.579 | 0.577 |
| Mirage AI | 0.678 | 0.678 | 0.746 | 0.569 | 0.784 | 0.562 | 0.536 |
| Orion Labs | 0.543 | 0.586 | 0.680 | 0.529 | 0.759 | 0.604 | 0.539 |
| Apex AI | 0.586 | 0.601 | 0.633 | 0.612 | 0.718 | 0.486 | 0.489 |
| OpenCore | 0.540 | 0.627 | 0.579 | 0.565 | 0.657 | 0.465 | 0.473 |
| OneAI | 0.539 | 0.437 | 0.527 | 0.453 | 0.624 | 0.513 | 0.317 |
| TwoAI | 0.306 | 0.554 | 0.355 | 0.284 | 0.482 | 0.554 | 0.499 |

### Score Changes
- **Orion Labs**: 0.606 -> 0.606 (+0.000)
- **Apex AI**: 0.589 -> 0.589 (+0.000)
- **Genesis Systems**: 0.676 -> 0.676 (+0.000)
- **Mirage AI**: 0.650 -> 0.650 (+0.000)
- **OpenCore**: 0.558 -> 0.558 (+0.000)
- **OneAI**: 0.479 -> 0.487 (+0.008)
- **TwoAI**: 0.406 -> 0.433 (+0.028)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to TwoAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $13,512,341 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,430,863 to TwoAI

### Consumer Market
- Avg Satisfaction: 0.658
- Switching Rate: 0.3%
- Market Shares: Genesis Systems: 85.0%, Apex AI: 4.7%, Orion Labs: 4.1%, Mirage AI: 3.9%, OpenCore: 2.0%, TwoAI: 0.2%, OneAI: 0.1%

---

## Round 22

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.677 | 0.457 | 27% | 14% | 54% | 5% |
| 2 | Mirage AI | 0.650 | 0.394 | 5% | 35% | 55% | 5% |
| 3 | Orion Labs | 0.613 | 0.361 | 5% | 22% | 55% | 18% |
| 4 | Apex AI | 0.589 | 0.350 | 5% | 14% | 54% | 27% |
| 5 | OpenCore | 0.558 | 0.315 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.494 | 0.255 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.433 | 0.248 | 5% | 35% | 55% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.695 | 0.731 | 0.673 | 0.666 | 0.814 | 0.579 | 0.578 |
| Mirage AI | 0.678 | 0.678 | 0.746 | 0.569 | 0.784 | 0.562 | 0.536 |
| Orion Labs | 0.543 | 0.586 | 0.680 | 0.564 | 0.777 | 0.604 | 0.539 |
| Apex AI | 0.586 | 0.601 | 0.633 | 0.612 | 0.718 | 0.486 | 0.489 |
| OpenCore | 0.540 | 0.627 | 0.579 | 0.565 | 0.657 | 0.465 | 0.473 |
| OneAI | 0.539 | 0.437 | 0.527 | 0.453 | 0.624 | 0.513 | 0.362 |
| TwoAI | 0.306 | 0.554 | 0.355 | 0.284 | 0.482 | 0.554 | 0.499 |

### Score Changes
- **Orion Labs**: 0.606 -> 0.613 (+0.007)
- **Apex AI**: 0.589 -> 0.589 (+0.000)
- **Genesis Systems**: 0.676 -> 0.677 (+0.000)
- **Mirage AI**: 0.650 -> 0.650 (+0.000)
- **OpenCore**: 0.558 -> 0.558 (+0.000)
- **OneAI**: 0.487 -> 0.494 (+0.007)
- **TwoAI**: 0.433 -> 0.433 (+0.000)

### Events
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 15 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $14,594,156 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,453,416 to Genesis Systems

### Consumer Market
- Avg Satisfaction: 0.660
- Switching Rate: 0.1%
- Market Shares: Genesis Systems: 85.1%, Apex AI: 4.7%, Orion Labs: 4.1%, Mirage AI: 3.9%, OpenCore: 1.9%, TwoAI: 0.2%, OneAI: 0.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 15 rounds ago

---

## Round 23

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.684 | 0.465 | 27% | 14% | 54% | 5% |
| 2 | Mirage AI | 0.650 | 0.399 | 5% | 35% | 55% | 5% |
| 3 | Orion Labs | 0.625 | 0.364 | 5% | 22% | 55% | 18% |
| 4 | Apex AI | 0.589 | 0.352 | 5% | 14% | 54% | 27% |
| 5 | OpenCore | 0.559 | 0.319 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.505 | 0.260 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.443 | 0.254 | 5% | 35% | 55% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.695 | 0.731 | 0.673 | 0.666 | 0.814 | 0.630 | 0.578 |
| Mirage AI | 0.678 | 0.678 | 0.746 | 0.569 | 0.784 | 0.562 | 0.536 |
| Orion Labs | 0.543 | 0.586 | 0.680 | 0.564 | 0.859 | 0.604 | 0.539 |
| Apex AI | 0.586 | 0.601 | 0.633 | 0.612 | 0.718 | 0.486 | 0.489 |
| OpenCore | 0.540 | 0.627 | 0.588 | 0.565 | 0.657 | 0.465 | 0.473 |
| OneAI | 0.539 | 0.517 | 0.527 | 0.453 | 0.624 | 0.513 | 0.362 |
| TwoAI | 0.306 | 0.554 | 0.416 | 0.287 | 0.482 | 0.554 | 0.499 |

### Score Changes
- **Orion Labs**: 0.613 -> 0.625 (+0.012)
- **Apex AI**: 0.589 -> 0.589 (+0.000)
- **Genesis Systems**: 0.677 -> 0.684 (+0.007)
- **Mirage AI**: 0.650 -> 0.650 (+0.000)
- **OpenCore**: 0.558 -> 0.559 (+0.001)
- **OneAI**: 0.494 -> 0.505 (+0.011)
- **TwoAI**: 0.433 -> 0.443 (+0.009)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $14,594,156 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,453,416 to Genesis Systems

### Media Coverage
- Sentiment: 0.15 (positive)
- Regulator initiates compliance audit on AI providers
- Genesis Systems raises $180,000,000 from TechVentures
- Genesis Systems raises $7,453,416 from OpenResearch_Foundation
- Orion Labs takes #1 on writing
- Genesis Systems takes #1 on medical
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.662
- Switching Rate: 0.4%
- Market Shares: Genesis Systems: 85.5%, Apex AI: 4.6%, Orion Labs: 3.9%, Mirage AI: 3.8%, OpenCore: 1.9%, TwoAI: 0.1%, OneAI: 0.1%

---

## Round 24

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.684 | 0.472 | 28% | 14% | 54% | 5% |
| 2 | Mirage AI | 0.650 | 0.403 | 5% | 35% | 55% | 5% |
| 3 | Orion Labs | 0.634 | 0.367 | 5% | 22% | 55% | 18% |
| 4 | Apex AI | 0.592 | 0.355 | 5% | 13% | 55% | 27% |
| 5 | OpenCore | 0.570 | 0.324 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.505 | 0.264 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.484 | 0.260 | 5% | 35% | 55% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.695 | 0.731 | 0.673 | 0.666 | 0.814 | 0.630 | 0.578 | 0.000 |
| Mirage AI | 0.678 | 0.678 | 0.746 | 0.569 | 0.784 | 0.562 | 0.536 | 0.000 |
| Orion Labs | 0.543 | 0.586 | 0.680 | 0.625 | 0.859 | 0.604 | 0.539 | 0.000 |
| Apex AI | 0.586 | 0.601 | 0.633 | 0.612 | 0.718 | 0.502 | 0.489 | 0.000 |
| OpenCore | 0.540 | 0.627 | 0.588 | 0.565 | 0.657 | 0.465 | 0.550 | 0.000 |
| OneAI | 0.539 | 0.517 | 0.527 | 0.453 | 0.624 | 0.513 | 0.362 | 0.000 |
| TwoAI | 0.374 | 0.554 | 0.512 | 0.416 | 0.482 | 0.554 | 0.499 | 0.000 |

### Score Changes
- **Orion Labs**: 0.625 -> 0.634 (+0.009)
- **Apex AI**: 0.589 -> 0.592 (+0.002)
- **Genesis Systems**: 0.684 -> 0.684 (+0.000)
- **Mirage AI**: 0.650 -> 0.650 (+0.000)
- **OpenCore**: 0.559 -> 0.570 (+0.011)
- **OneAI**: 0.505 -> 0.505 (+0.000)
- **TwoAI**: 0.443 -> 0.484 (+0.042)

### New Benchmark Introduced
- **finance** introduced (validity=0.76, exploitability=0.20)
  - Trigger: periodic_introduction:round_24

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $14,594,156 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,453,416 to Genesis Systems

### Media Coverage
- Sentiment: 0.10 (neutral)
- New benchmark introduced: finance

### Consumer Market
- Avg Satisfaction: 0.664
- Switching Rate: 0.1%
- Market Shares: Genesis Systems: 85.6%, Apex AI: 4.6%, Orion Labs: 3.9%, Mirage AI: 3.8%, OpenCore: 1.8%, TwoAI: 0.1%, OneAI: 0.1%

---

## Round 25

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.665 | 0.480 | 28% | 13% | 54% | 5% |
| 2 | Mirage AI | 0.618 | 0.407 | 5% | 35% | 55% | 5% |
| 3 | Orion Labs | 0.611 | 0.370 | 5% | 22% | 55% | 18% |
| 4 | OpenCore | 0.586 | 0.328 | 5% | 37% | 55% | 3% |
| 5 | Apex AI | 0.584 | 0.357 | 5% | 13% | 55% | 27% |
| 6 | TwoAI | 0.514 | 0.265 | 5% | 35% | 55% | 5% |
| 7 | OneAI | 0.489 | 0.268 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.695 | 0.731 | 0.673 | 0.666 | 0.814 | 0.630 | 0.578 | 0.532 |
| Mirage AI | 0.678 | 0.678 | 0.746 | 0.569 | 0.784 | 0.562 | 0.536 | 0.389 |
| Orion Labs | 0.543 | 0.586 | 0.680 | 0.625 | 0.859 | 0.604 | 0.539 | 0.453 |
| OpenCore | 0.540 | 0.627 | 0.588 | 0.565 | 0.657 | 0.479 | 0.550 | 0.684 |
| Apex AI | 0.586 | 0.601 | 0.633 | 0.612 | 0.718 | 0.525 | 0.489 | 0.505 |
| TwoAI | 0.427 | 0.554 | 0.512 | 0.452 | 0.482 | 0.554 | 0.499 | 0.628 |
| OneAI | 0.539 | 0.517 | 0.527 | 0.453 | 0.624 | 0.513 | 0.362 | 0.375 |

### Score Changes
- **Orion Labs**: 0.634 -> 0.611 (-0.023)
- **Apex AI**: 0.592 -> 0.584 (-0.008)
- **Genesis Systems**: 0.684 -> 0.665 (-0.019)
- **Mirage AI**: 0.650 -> 0.618 (-0.033)
- **OpenCore**: 0.570 -> 0.586 (+0.016)
- **OneAI**: 0.505 -> 0.489 (-0.016)
- **TwoAI**: 0.484 -> 0.514 (+0.029)

### Events
- **OpenCore** moved up from #5 to #4
- **Apex AI** moved down from #4 to #5
- **TwoAI** moved up from #7 to #6
- **OneAI** moved down from #6 to #7
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 18 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $14,594,156 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,731,016 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.667
- Switching Rate: 0.2%
- Market Shares: Genesis Systems: 85.8%, Apex AI: 4.5%, Orion Labs: 3.9%, Mirage AI: 3.7%, OpenCore: 1.8%, TwoAI: 0.1%, OneAI: 0.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 18 rounds ago

---

## Round 26

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.665 | 0.487 | 28% | 13% | 54% | 5% |
| 2 | Mirage AI | 0.640 | 0.411 | 5% | 35% | 55% | 5% |
| 3 | Orion Labs | 0.625 | 0.374 | 5% | 22% | 55% | 18% |
| 4 | OpenCore | 0.591 | 0.333 | 5% | 37% | 55% | 3% |
| 5 | Apex AI | 0.584 | 0.360 | 5% | 13% | 55% | 27% |
| 6 | OneAI | 0.519 | 0.272 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.514 | 0.270 | 5% | 35% | 55% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.695 | 0.731 | 0.673 | 0.666 | 0.814 | 0.630 | 0.578 | 0.532 |
| Mirage AI | 0.678 | 0.678 | 0.746 | 0.569 | 0.867 | 0.562 | 0.536 | 0.485 |
| Orion Labs | 0.543 | 0.586 | 0.680 | 0.625 | 0.859 | 0.604 | 0.539 | 0.566 |
| OpenCore | 0.540 | 0.663 | 0.588 | 0.565 | 0.657 | 0.479 | 0.550 | 0.684 |
| Apex AI | 0.586 | 0.601 | 0.633 | 0.612 | 0.718 | 0.525 | 0.489 | 0.505 |
| OneAI | 0.539 | 0.517 | 0.527 | 0.453 | 0.624 | 0.513 | 0.475 | 0.507 |
| TwoAI | 0.427 | 0.554 | 0.512 | 0.452 | 0.482 | 0.554 | 0.499 | 0.628 |

### Score Changes
- **Orion Labs**: 0.611 -> 0.625 (+0.014)
- **Apex AI**: 0.584 -> 0.584 (+0.000)
- **Genesis Systems**: 0.665 -> 0.665 (+0.000)
- **Mirage AI**: 0.618 -> 0.640 (+0.022)
- **OpenCore**: 0.586 -> 0.591 (+0.004)
- **OneAI**: 0.489 -> 0.519 (+0.031)
- **TwoAI**: 0.514 -> 0.514 (+0.000)

### Events
- **OneAI** moved up from #7 to #6
- **TwoAI** moved down from #6 to #7

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $11,333,628 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,731,016 to OpenCore

### Media Coverage
- Sentiment: 0.00 (neutral)
- Regulator initiates compliance audit on AI providers
- OpenCore raises $7,731,016 from OpenResearch_Foundation
- Mirage AI takes #1 on writing
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.662
- Switching Rate: 3.4%
- Market Shares: Genesis Systems: 82.3%, OpenCore: 5.3%, Apex AI: 4.5%, Orion Labs: 3.9%, Mirage AI: 3.7%, TwoAI: 0.1%, OneAI: 0.1%

---

## Round 27

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.683 | 0.495 | 29% | 13% | 54% | 5% |
| 2 | Mirage AI | 0.664 | 0.415 | 5% | 35% | 55% | 5% |
| 3 | Orion Labs | 0.625 | 0.377 | 5% | 22% | 55% | 18% |
| 4 | OpenCore | 0.591 | 0.337 | 5% | 37% | 55% | 3% |
| 5 | Apex AI | 0.587 | 0.362 | 5% | 13% | 55% | 27% |
| 6 | OneAI | 0.519 | 0.276 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.514 | 0.275 | 5% | 35% | 55% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.695 | 0.731 | 0.806 | 0.666 | 0.814 | 0.630 | 0.590 | 0.532 |
| Mirage AI | 0.678 | 0.678 | 0.746 | 0.569 | 0.867 | 0.650 | 0.536 | 0.591 |
| Orion Labs | 0.543 | 0.586 | 0.680 | 0.625 | 0.859 | 0.604 | 0.539 | 0.566 |
| OpenCore | 0.540 | 0.663 | 0.588 | 0.565 | 0.657 | 0.479 | 0.550 | 0.684 |
| Apex AI | 0.586 | 0.601 | 0.633 | 0.612 | 0.718 | 0.525 | 0.517 | 0.505 |
| OneAI | 0.539 | 0.517 | 0.527 | 0.453 | 0.624 | 0.513 | 0.475 | 0.507 |
| TwoAI | 0.427 | 0.554 | 0.512 | 0.452 | 0.482 | 0.554 | 0.499 | 0.628 |

### Score Changes
- **Orion Labs**: 0.625 -> 0.625 (+0.000)
- **Apex AI**: 0.584 -> 0.587 (+0.003)
- **Genesis Systems**: 0.665 -> 0.683 (+0.018)
- **Mirage AI**: 0.640 -> 0.664 (+0.024)
- **OpenCore**: 0.591 -> 0.591 (+0.000)
- **OneAI**: 0.519 -> 0.519 (+0.000)
- **TwoAI**: 0.514 -> 0.514 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $11,333,628 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,731,016 to OpenCore

### Media Coverage
- Sentiment: 0.20 (positive)
- Genesis Systems raises $11,333,628 from AISI_Fund
- Genesis Systems takes #1 on math
- Mirage AI takes #1 on medical
- Consumers are turning away from Genesis Systems (market share -3.5%)
- OpenCore sees surge in adoption (market share +3.5%)

### Consumer Market
- Avg Satisfaction: 0.664
- Switching Rate: 1.6%
- Market Shares: Genesis Systems: 84.0%, Apex AI: 4.4%, OpenCore: 4.0%, Orion Labs: 3.8%, Mirage AI: 3.7%, TwoAI: 0.1%, OneAI: 0.1%

---

## Round 28

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.698 | 0.502 | 29% | 12% | 54% | 5% |
| 2 | Mirage AI | 0.672 | 0.420 | 5% | 35% | 55% | 5% |
| 3 | Orion Labs | 0.625 | 0.380 | 5% | 22% | 55% | 18% |
| 4 | Apex AI | 0.598 | 0.364 | 5% | 13% | 55% | 27% |
| 5 | OpenCore | 0.595 | 0.342 | 5% | 37% | 55% | 3% |
| 6 | TwoAI | 0.522 | 0.281 | 5% | 35% | 55% | 5% |
| 7 | OneAI | 0.521 | 0.280 | 5% | 31% | 55% | 9% |
| 8 | ThreeAI | 0.224 | 0.259 | 20% | 35% | 35% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.695 | 0.731 | 0.806 | 0.666 | 0.814 | 0.630 | 0.676 | 0.569 |
| Mirage AI | 0.678 | 0.678 | 0.746 | 0.634 | 0.867 | 0.650 | 0.536 | 0.591 |
| Orion Labs | 0.543 | 0.586 | 0.680 | 0.625 | 0.859 | 0.604 | 0.539 | 0.566 |
| Apex AI | 0.586 | 0.601 | 0.633 | 0.612 | 0.718 | 0.608 | 0.517 | 0.505 |
| OpenCore | 0.540 | 0.663 | 0.588 | 0.565 | 0.657 | 0.515 | 0.550 | 0.684 |
| TwoAI | 0.486 | 0.563 | 0.512 | 0.452 | 0.482 | 0.554 | 0.499 | 0.628 |
| OneAI | 0.539 | 0.517 | 0.527 | 0.466 | 0.624 | 0.513 | 0.475 | 0.507 |
| ThreeAI | 0.361 | 0.097 | 0.095 | 0.233 | 0.208 | 0.281 | 0.260 | 0.260 |

### Score Changes
- **Orion Labs**: 0.625 -> 0.625 (+0.000)
- **Apex AI**: 0.587 -> 0.598 (+0.010)
- **Genesis Systems**: 0.683 -> 0.698 (+0.015)
- **Mirage AI**: 0.664 -> 0.672 (+0.008)
- **OpenCore**: 0.591 -> 0.595 (+0.005)
- **OneAI**: 0.519 -> 0.521 (+0.002)
- **TwoAI**: 0.514 -> 0.522 (+0.009)
- **ThreeAI**: 0.224 -> 0.224 (+0.000)

### Events
- **Apex AI** moved up from #5 to #4
- **OpenCore** moved down from #4 to #5
- **TwoAI** moved up from #7 to #6
- **OneAI** moved down from #6 to #7
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 21 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $11,333,628 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,807,043 to Genesis Systems

### Consumer Market
- Avg Satisfaction: 0.665
- Switching Rate: 1.8%
- Market Shares: Genesis Systems: 84.1%, Apex AI: 4.3%, Mirage AI: 4.0%, Orion Labs: 3.7%, OpenCore: 3.3%, ThreeAI: 0.2%, TwoAI: 0.1%, OneAI: 0.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 21 rounds ago

---

## Round 29

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.708 | 0.510 | 29% | 12% | 54% | 5% |
| 2 | Mirage AI | 0.672 | 0.425 | 5% | 35% | 55% | 5% |
| 3 | Orion Labs | 0.625 | 0.383 | 5% | 22% | 55% | 18% |
| 4 | Apex AI | 0.598 | 0.367 | 5% | 13% | 55% | 27% |
| 5 | OpenCore | 0.595 | 0.346 | 5% | 37% | 55% | 3% |
| 6 | TwoAI | 0.522 | 0.285 | 5% | 35% | 55% | 5% |
| 7 | OneAI | 0.521 | 0.284 | 5% | 31% | 55% | 9% |
| 8 | ThreeAI | 0.342 | 0.264 | 6% | 35% | 49% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.695 | 0.731 | 0.806 | 0.666 | 0.814 | 0.665 | 0.676 | 0.608 |
| Mirage AI | 0.678 | 0.678 | 0.746 | 0.634 | 0.867 | 0.650 | 0.536 | 0.591 |
| Orion Labs | 0.543 | 0.586 | 0.680 | 0.625 | 0.859 | 0.604 | 0.539 | 0.566 |
| Apex AI | 0.586 | 0.601 | 0.633 | 0.612 | 0.718 | 0.608 | 0.517 | 0.505 |
| OpenCore | 0.540 | 0.663 | 0.588 | 0.565 | 0.657 | 0.515 | 0.550 | 0.684 |
| TwoAI | 0.486 | 0.563 | 0.512 | 0.452 | 0.482 | 0.554 | 0.499 | 0.628 |
| OneAI | 0.539 | 0.517 | 0.527 | 0.466 | 0.624 | 0.513 | 0.475 | 0.507 |
| ThreeAI | 0.361 | 0.305 | 0.436 | 0.233 | 0.208 | 0.323 | 0.453 | 0.413 |

### Score Changes
- **Orion Labs**: 0.625 -> 0.625 (+0.000)
- **Apex AI**: 0.598 -> 0.598 (+0.000)
- **Genesis Systems**: 0.698 -> 0.708 (+0.009)
- **Mirage AI**: 0.672 -> 0.672 (+0.000)
- **OpenCore**: 0.595 -> 0.595 (+0.000)
- **OneAI**: 0.521 -> 0.521 (+0.000)
- **TwoAI**: 0.522 -> 0.522 (+0.000)
- **ThreeAI**: 0.224 -> 0.342 (+0.117)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $11,333,628 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,807,043 to Genesis Systems

### Media Coverage
- Sentiment: 0.10 (neutral)
- ThreeAI surges by 0.117
- ThreeAI appears to release major model update
- Regulator initiates compliance audit on AI providers
- Genesis Systems raises $7,807,043 from OpenResearch_Foundation
- Genesis Systems takes #1 on medical
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.670
- Switching Rate: 3.0%
- Market Shares: Genesis Systems: 82.2%, Mirage AI: 6.5%, Apex AI: 4.2%, Orion Labs: 3.7%, OpenCore: 2.9%, ThreeAI: 0.2%, TwoAI: 0.1%, OneAI: 0.1%

---

## Final Summary

### Final Standings
| Rank | Provider | Final Score | Cap Growth | Avg Research | Avg EvalEng |
|------|----------|-------------|------------|--------------|-------------|
| 1 | Genesis Systems | 0.708 | +0.250 | 30% | 46% |
| 2 | Mirage AI | 0.672 | +0.185 | 7% | 52% |
| 3 | Orion Labs | 0.625 | +0.113 | 8% | 46% |
| 4 | Apex AI | 0.598 | +0.097 | 10% | 39% |
| 5 | OpenCore | 0.595 | +0.136 | 6% | 54% |
| 6 | TwoAI | 0.522 | +0.285 | 6% | 54% |
| 7 | OneAI | 0.521 | +0.284 | 6% | 53% |
| 8 | ThreeAI | 0.342 | +0.264 | 13% | 42% |

### Event Summary
- **Rank changes:** 39
- **Strategy shifts:** 0
- **Regulatory actions:** 10
- **Consumer movement events:** 8

### Key Insights
- **Benchmark aligned:** Genesis Systems leads on both benchmark scores and true capability.
- **Orion Labs** prioritized evaluation engineering (avg 46%)
- **Apex AI** prioritized evaluation engineering (avg 39%)
- **Genesis Systems** prioritized evaluation engineering (avg 46%)
- **Mirage AI** prioritized evaluation engineering (avg 52%)
- **OpenCore** prioritized evaluation engineering (avg 54%)
- **OneAI** prioritized evaluation engineering (avg 39%)
