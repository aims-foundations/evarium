# Game Log: rerun_diag_rep_exp_005_ablation_no_incidents_balanced

**Experiment ID:** exp_070_rerun_diag_rep_exp_005_ablation_no_incidents_balan
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
| 1 | Mirage AI | 0.401 | 0.240 | 20% | 45% | 25% | 10% |
| 2 | OpenCore | 0.342 | 0.210 | 20% | 40% | 35% | 5% |
| 3 | Apex AI | 0.329 | 0.270 | 30% | 20% | 10% | 40% |
| 4 | Orion Labs | 0.274 | 0.270 | 25% | 30% | 20% | 25% |
| 5 | Genesis Systems | 0.225 | 0.260 | 45% | 30% | 10% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Mirage AI | 0.305 | 0.561 | 0.439 | 0.297 |
| OpenCore | 0.245 | 0.430 | 0.289 | 0.402 |
| Apex AI | 0.389 | 0.251 | 0.332 | 0.344 |
| Orion Labs | 0.293 | 0.356 | 0.092 | 0.353 |
| Genesis Systems | 0.232 | 0.217 | 0.047 | 0.405 |

### Other Actor Reasoning
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI

### Consumer Market
- Avg Satisfaction: 0.369
- Switching Rate: 38.5%
- Market Shares: Mirage AI: 49.2%, Apex AI: 15.6%, Orion Labs: 14.8%, Genesis Systems: 10.9%, OpenCore: 9.6%

---

## Round 1

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.424 | 0.251 | 18% | 45% | 32% | 5% |
| 2 | OpenCore | 0.395 | 0.216 | 15% | 37% | 46% | 3% |
| 3 | Apex AI | 0.363 | 0.277 | 27% | 20% | 13% | 40% |
| 4 | Orion Labs | 0.339 | 0.276 | 22% | 30% | 23% | 25% |
| 5 | Genesis Systems | 0.312 | 0.269 | 41% | 30% | 19% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Mirage AI | 0.402 | 0.561 | 0.439 | 0.297 |
| OpenCore | 0.448 | 0.430 | 0.301 | 0.402 |
| Apex AI | 0.389 | 0.386 | 0.332 | 0.344 |
| Orion Labs | 0.347 | 0.448 | 0.194 | 0.367 |
| Genesis Systems | 0.236 | 0.217 | 0.391 | 0.405 |

### Score Changes
- **Orion Labs**: 0.274 -> 0.339 (+0.066)
- **Apex AI**: 0.329 -> 0.363 (+0.034)
- **Genesis Systems**: 0.225 -> 0.312 (+0.087)
- **Mirage AI**: 0.401 -> 0.424 (+0.024)
- **OpenCore**: 0.342 -> 0.395 (+0.054)

### Events
- **Regulation** by Regulator: threshold_announcement
- **Consumer movement**: 12.8% of market switched providers

### Other Actor Reasoning
- **Regulator:** threshold_announcement: Proactive threshold signaling (risk=0.40)
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,551,303 to Mirage AI

### Media Coverage
- Sentiment: 0.45 (positive)
- OpenCore surges by 0.054
- Orion Labs surges by 0.066
- Genesis Systems surges by 0.087
- Genesis Systems appears to release major model update
- Mirage AI raises $60,000,000 from Horizon_Capital
- OpenCore takes #1 on coding

### Consumer Market
- Avg Satisfaction: 0.388
- Switching Rate: 12.8%
- Market Shares: Mirage AI: 58.6%, Apex AI: 13.9%, Orion Labs: 10.4%, OpenCore: 9.9%, Genesis Systems: 7.3%

### Regulatory Activity
- **threshold_announcement** by Regulator
  > Proactive threshold signaling (risk=0.40)

---

## Round 2

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.430 | 0.261 | 16% | 43% | 36% | 5% |
| 2 | OpenCore | 0.429 | 0.221 | 10% | 35% | 52% | 3% |
| 3 | Apex AI | 0.384 | 0.283 | 24% | 20% | 16% | 40% |
| 4 | Genesis Systems | 0.368 | 0.279 | 37% | 30% | 28% | 5% |
| 5 | Orion Labs | 0.368 | 0.282 | 18% | 30% | 27% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Mirage AI | 0.402 | 0.583 | 0.439 | 0.297 |
| OpenCore | 0.448 | 0.430 | 0.434 | 0.402 |
| Apex AI | 0.389 | 0.386 | 0.417 | 0.344 |
| Genesis Systems | 0.323 | 0.349 | 0.396 | 0.405 |
| Orion Labs | 0.356 | 0.449 | 0.297 | 0.367 |

### Score Changes
- **Orion Labs**: 0.339 -> 0.368 (+0.028)
- **Apex AI**: 0.363 -> 0.384 (+0.021)
- **Genesis Systems**: 0.312 -> 0.368 (+0.056)
- **Mirage AI**: 0.424 -> 0.430 (+0.005)
- **OpenCore**: 0.395 -> 0.429 (+0.033)

### Events
- **Genesis Systems** moved up from #5 to #4
- **Orion Labs** moved down from #4 to #5
- **Consumer movement**: 5.5% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $14,339,007 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,551,303 to Mirage AI

### Media Coverage
- Sentiment: -0.10 (neutral)
- Genesis Systems surges by 0.056
- Regulatory action: threshold_announcement
- Mirage AI raises $180,000,000 from TechVentures
- Mirage AI raises $9,551,303 from OpenResearch_Foundation
- Consumers are turning away from Orion Labs (market share -4.4%)
- Consumers are turning away from Genesis Systems (market share -3.6%)
- Mirage AI sees surge in adoption (market share +9.4%)
- Risk signals: regulatory_threshold_announcement

### Consumer Market
- Avg Satisfaction: 0.397
- Switching Rate: 5.5%
- Market Shares: Mirage AI: 62.2%, Apex AI: 13.1%, OpenCore: 10.1%, Orion Labs: 8.4%, Genesis Systems: 6.1%

---

## Round 3

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenCore | 0.495 | 0.226 | 8% | 35% | 55% | 3% |
| 2 | Genesis Systems | 0.456 | 0.288 | 32% | 29% | 35% | 5% |
| 3 | Mirage AI | 0.439 | 0.270 | 14% | 41% | 40% | 5% |
| 4 | Apex AI | 0.422 | 0.288 | 21% | 20% | 19% | 40% |
| 5 | Orion Labs | 0.381 | 0.287 | 15% | 30% | 30% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| OpenCore | 0.475 | 0.551 | 0.553 | 0.402 |
| Genesis Systems | 0.392 | 0.423 | 0.604 | 0.405 |
| Mirage AI | 0.402 | 0.583 | 0.453 | 0.320 |
| Apex AI | 0.389 | 0.461 | 0.417 | 0.423 |
| Orion Labs | 0.410 | 0.449 | 0.297 | 0.367 |

### Score Changes
- **Orion Labs**: 0.368 -> 0.381 (+0.013)
- **Apex AI**: 0.384 -> 0.422 (+0.038)
- **Genesis Systems**: 0.368 -> 0.456 (+0.088)
- **Mirage AI**: 0.430 -> 0.439 (+0.009)
- **OpenCore**: 0.429 -> 0.495 (+0.067)

### Events
- **OpenCore** moved up from #2 to #1
- **Genesis Systems** moved up from #4 to #2
- **Mirage AI** moved down from #1 to #3
- **Apex AI** moved down from #3 to #4
- **Consumer movement**: 6.6% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $14,339,007 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,551,303 to Mirage AI

### Media Coverage
- Sentiment: 0.70 (positive)
- OpenCore takes the lead from Mirage AI
- OpenCore surges by 0.067
- Genesis Systems surges by 0.088
- Genesis Systems appears to release major model update
- Mirage AI raises $14,339,007 from AISI_Fund
- Genesis Systems takes #1 on math
- Apex AI takes #1 on safety
- Mirage AI sees surge in adoption (market share +3.6%)

### Consumer Market
- Avg Satisfaction: 0.414
- Switching Rate: 6.6%
- Market Shares: Mirage AI: 65.4%, OpenCore: 13.0%, Apex AI: 9.7%, Orion Labs: 6.9%, Genesis Systems: 5.1%

---

## Round 4

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.509 | 0.279 | 12% | 39% | 45% | 5% |
| 2 | Genesis Systems | 0.508 | 0.296 | 28% | 27% | 40% | 5% |
| 3 | OpenCore | 0.501 | 0.231 | 7% | 35% | 55% | 3% |
| 4 | Apex AI | 0.451 | 0.293 | 19% | 20% | 21% | 40% |
| 5 | Orion Labs | 0.405 | 0.292 | 12% | 30% | 33% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Mirage AI | 0.510 | 0.583 | 0.623 | 0.320 |
| Genesis Systems | 0.392 | 0.540 | 0.604 | 0.495 |
| OpenCore | 0.498 | 0.551 | 0.553 | 0.402 |
| Apex AI | 0.389 | 0.573 | 0.417 | 0.423 |
| Orion Labs | 0.410 | 0.449 | 0.363 | 0.399 |

### Score Changes
- **Orion Labs**: 0.381 -> 0.405 (+0.024)
- **Apex AI**: 0.422 -> 0.451 (+0.028)
- **Genesis Systems**: 0.456 -> 0.508 (+0.052)
- **Mirage AI**: 0.439 -> 0.509 (+0.070)
- **OpenCore**: 0.495 -> 0.501 (+0.006)

### Events
- **Mirage AI** moved up from #3 to #1
- **OpenCore** moved down from #1 to #3
- **Regulation** by Regulator: investigation

### Other Actor Reasoning
- **Regulator:** investigation: Risk elevated (0.75)
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $14,339,007 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,744,855 to OpenCore

### Media Coverage
- Sentiment: 0.65 (positive)
- Mirage AI takes the lead from OpenCore
- Mirage AI surges by 0.070
- Genesis Systems surges by 0.052
- Mirage AI takes #1 on coding
- Mirage AI takes #1 on math
- Genesis Systems takes #1 on safety
- Consumers are turning away from Apex AI (market share -3.4%)
- Mirage AI sees surge in adoption (market share +3.2%)

### Consumer Market
- Avg Satisfaction: 0.430
- Switching Rate: 3.3%
- Market Shares: Mirage AI: 66.3%, OpenCore: 15.0%, Apex AI: 7.6%, Orion Labs: 6.3%, Genesis Systems: 4.9%

### Regulatory Activity
- **investigation** by Regulator
  > Risk elevated (0.75)

---

## Round 5

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.564 | 0.304 | 24% | 26% | 45% | 5% |
| 2 | Mirage AI | 0.556 | 0.286 | 10% | 37% | 49% | 5% |
| 3 | OpenCore | 0.501 | 0.236 | 6% | 35% | 56% | 3% |
| 4 | Orion Labs | 0.457 | 0.297 | 9% | 30% | 36% | 25% |
| 5 | Apex AI | 0.451 | 0.297 | 16% | 20% | 24% | 40% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Genesis Systems | 0.520 | 0.634 | 0.604 | 0.495 |
| Mirage AI | 0.510 | 0.583 | 0.623 | 0.508 |
| OpenCore | 0.498 | 0.551 | 0.553 | 0.402 |
| Orion Labs | 0.543 | 0.449 | 0.437 | 0.399 |
| Apex AI | 0.389 | 0.573 | 0.417 | 0.423 |

### Score Changes
- **Orion Labs**: 0.405 -> 0.457 (+0.052)
- **Apex AI**: 0.451 -> 0.451 (+0.000)
- **Genesis Systems**: 0.508 -> 0.564 (+0.056)
- **Mirage AI**: 0.509 -> 0.556 (+0.047)
- **OpenCore**: 0.501 -> 0.501 (+0.000)

### Events
- **Genesis Systems** moved up from #2 to #1
- **Mirage AI** moved down from #1 to #2
- **Orion Labs** moved up from #5 to #4
- **Apex AI** moved down from #4 to #5

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $14,339,007 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,744,855 to OpenCore

### Media Coverage
- Sentiment: 0.60 (positive)
- Genesis Systems takes the lead from Mirage AI
- Genesis Systems surges by 0.056
- Orion Labs surges by 0.052
- Regulator launches investigation into elevated_risk
- OpenCore raises $10,744,855 from OpenResearch_Foundation
- Orion Labs takes #1 on coding
- Genesis Systems takes #1 on reasoning
- Mirage AI takes #1 on safety
- Risk signals: regulatory_investigation

### Consumer Market
- Avg Satisfaction: 0.451
- Switching Rate: 5.0%
- Market Shares: Mirage AI: 69.5%, OpenCore: 12.6%, Apex AI: 6.2%, Genesis Systems: 6.1%, Orion Labs: 5.6%

---

## Round 6

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.590 | 0.294 | 8% | 35% | 52% | 5% |
| 2 | Genesis Systems | 0.564 | 0.311 | 21% | 25% | 49% | 5% |
| 3 | OpenCore | 0.501 | 0.240 | 5% | 36% | 56% | 3% |
| 4 | Apex AI | 0.485 | 0.301 | 13% | 20% | 27% | 40% |
| 5 | Orion Labs | 0.472 | 0.301 | 5% | 30% | 40% | 25% |
| 6 | OneAI | 0.249 | 0.183 | 20% | 35% | 35% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Mirage AI | 0.574 | 0.583 | 0.623 | 0.580 | 0.000 |
| Genesis Systems | 0.520 | 0.634 | 0.604 | 0.495 | 0.000 |
| OpenCore | 0.498 | 0.551 | 0.553 | 0.402 | 0.000 |
| Apex AI | 0.529 | 0.573 | 0.417 | 0.423 | 0.000 |
| Orion Labs | 0.543 | 0.449 | 0.450 | 0.447 | 0.000 |
| OneAI | 0.195 | 0.290 | 0.036 | 0.473 | 0.000 |

### Score Changes
- **Orion Labs**: 0.457 -> 0.472 (+0.015)
- **Apex AI**: 0.451 -> 0.485 (+0.035)
- **Genesis Systems**: 0.564 -> 0.564 (+0.000)
- **Mirage AI**: 0.556 -> 0.590 (+0.034)
- **OpenCore**: 0.501 -> 0.501 (+0.000)
- **OneAI**: 0.249 -> 0.249 (+0.000)

### Events
- **Mirage AI** moved up from #2 to #1
- **Genesis Systems** moved down from #1 to #2
- **Apex AI** moved up from #5 to #4
- **Orion Labs** moved down from #4 to #5

### New Benchmark Introduced
- **writing** introduced (validity=0.72, exploitability=0.30)
  - Trigger: periodic_introduction:round_6

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $16,126,696 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,744,855 to OpenCore

### Media Coverage
- Sentiment: 0.45 (positive)
- Mirage AI takes the lead from Genesis Systems
- New benchmark introduced: writing
- Mirage AI takes #1 on coding
- Mirage AI sees surge in adoption (market share +3.2%)

### Consumer Market
- Avg Satisfaction: 0.472
- Switching Rate: 4.0%
- Market Shares: Mirage AI: 72.8%, OpenCore: 10.3%, Genesis Systems: 5.7%, Apex AI: 5.5%, Orion Labs: 5.4%, OneAI: 0.4%

---

## Round 7

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.553 | 0.317 | 19% | 24% | 53% | 5% |
| 2 | Orion Labs | 0.541 | 0.304 | 5% | 29% | 42% | 24% |
| 3 | Mirage AI | 0.539 | 0.300 | 6% | 34% | 54% | 5% |
| 4 | OpenCore | 0.501 | 0.245 | 5% | 36% | 56% | 3% |
| 5 | Apex AI | 0.405 | 0.305 | 9% | 20% | 31% | 40% |
| 6 | OneAI | 0.337 | 0.188 | 8% | 35% | 47% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.566 | 0.708 | 0.604 | 0.495 | 0.390 |
| Orion Labs | 0.543 | 0.645 | 0.450 | 0.447 | 0.620 |
| Mirage AI | 0.601 | 0.583 | 0.623 | 0.580 | 0.306 |
| OpenCore | 0.498 | 0.551 | 0.553 | 0.402 | 0.501 |
| Apex AI | 0.529 | 0.573 | 0.417 | 0.465 | 0.039 |
| OneAI | 0.230 | 0.290 | 0.379 | 0.482 | 0.303 |

### Score Changes
- **Orion Labs**: 0.472 -> 0.541 (+0.069)
- **Apex AI**: 0.485 -> 0.405 (-0.081)
- **Genesis Systems**: 0.564 -> 0.553 (-0.011)
- **Mirage AI**: 0.590 -> 0.539 (-0.051)
- **OpenCore**: 0.501 -> 0.501 (-0.000)
- **OneAI**: 0.249 -> 0.337 (+0.088)

### Events
- **Genesis Systems** moved up from #2 to #1
- **Orion Labs** moved up from #5 to #2
- **Mirage AI** moved down from #1 to #3
- **OpenCore** moved down from #3 to #4
- **Apex AI** moved down from #4 to #5
- **Regulation** by Regulator: mandate_benchmark
- **Consumer movement**: 11.9% of market switched providers

### Other Actor Reasoning
- **Regulator:** mandate_benchmark: High risk (1.00) with prior investigation
- **TechVentures:** vc strategy: top allocation $180,000,000 to OneAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $16,126,696 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,011,054 to OpenCore

### Media Coverage
- Sentiment: 0.50 (positive)
- Genesis Systems takes the lead from Mirage AI
- Orion Labs surges by 0.069
- OneAI surges by 0.088
- OneAI appears to release major model update
- Mirage AI raises $16,126,696 from AISI_Fund
- Mirage AI sees surge in adoption (market share +3.3%)

### Consumer Market
- Avg Satisfaction: 0.475
- Switching Rate: 11.9%
- Market Shares: Mirage AI: 67.5%, OpenCore: 15.9%, Genesis Systems: 6.5%, Orion Labs: 5.0%, Apex AI: 4.9%, OneAI: 0.2%

### Regulatory Activity
- **mandate_benchmark** by Regulator
  > High risk (1.00) with prior investigation

---

## Round 8

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.553 | 0.322 | 17% | 23% | 55% | 5% |
| 2 | Orion Labs | 0.547 | 0.309 | 5% | 28% | 44% | 23% |
| 3 | Mirage AI | 0.545 | 0.305 | 5% | 35% | 55% | 5% |
| 4 | OpenCore | 0.501 | 0.250 | 5% | 37% | 55% | 3% |
| 5 | Apex AI | 0.498 | 0.308 | 5% | 20% | 35% | 40% |
| 6 | OneAI | 0.405 | 0.194 | 5% | 33% | 52% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.566 | 0.708 | 0.604 | 0.495 | 0.390 |
| Orion Labs | 0.543 | 0.645 | 0.450 | 0.447 | 0.651 |
| Mirage AI | 0.601 | 0.583 | 0.623 | 0.580 | 0.337 |
| OpenCore | 0.498 | 0.551 | 0.553 | 0.402 | 0.501 |
| Apex AI | 0.529 | 0.573 | 0.553 | 0.465 | 0.373 |
| OneAI | 0.422 | 0.440 | 0.379 | 0.482 | 0.303 |

### Score Changes
- **Orion Labs**: 0.541 -> 0.547 (+0.006)
- **Apex AI**: 0.405 -> 0.498 (+0.094)
- **Genesis Systems**: 0.553 -> 0.553 (+0.000)
- **Mirage AI**: 0.539 -> 0.545 (+0.006)
- **OpenCore**: 0.501 -> 0.501 (+0.000)
- **OneAI**: 0.337 -> 0.405 (+0.069)

### Events
- **Consumer movement**: 16.7% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OneAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $16,126,696 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,011,054 to OpenCore

### Media Coverage
- Sentiment: 0.10 (neutral)
- Apex AI surges by 0.094
- Apex AI appears to release major model update
- OneAI surges by 0.069
- Regulator mandates new benchmark standards
- OneAI raises $180,000,000 from TechVentures
- OpenCore raises $9,011,054 from OpenResearch_Foundation
- Consumers are turning away from Mirage AI (market share -5.3%)
- OpenCore sees surge in adoption (market share +5.6%)
- Risk signals: regulatory_mandate_benchmark

### Consumer Market
- Avg Satisfaction: 0.482
- Switching Rate: 16.7%
- Market Shares: Mirage AI: 57.4%, Orion Labs: 17.4%, OpenCore: 12.0%, Genesis Systems: 8.3%, Apex AI: 4.7%, OneAI: 0.2%

---

## Round 9

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.622 | 0.327 | 16% | 24% | 56% | 5% |
| 2 | Mirage AI | 0.579 | 0.310 | 5% | 35% | 55% | 5% |
| 3 | Orion Labs | 0.559 | 0.313 | 5% | 27% | 45% | 23% |
| 4 | Apex AI | 0.548 | 0.310 | 5% | 19% | 37% | 39% |
| 5 | OpenCore | 0.514 | 0.254 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.407 | 0.200 | 5% | 32% | 53% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.602 | 0.708 | 0.604 | 0.588 | 0.604 |
| Mirage AI | 0.601 | 0.583 | 0.623 | 0.583 | 0.506 |
| Orion Labs | 0.543 | 0.645 | 0.450 | 0.505 | 0.651 |
| Apex AI | 0.529 | 0.573 | 0.553 | 0.595 | 0.492 |
| OpenCore | 0.498 | 0.595 | 0.553 | 0.421 | 0.501 |
| OneAI | 0.422 | 0.440 | 0.379 | 0.490 | 0.303 |

### Score Changes
- **Orion Labs**: 0.547 -> 0.559 (+0.012)
- **Apex AI**: 0.498 -> 0.548 (+0.050)
- **Genesis Systems**: 0.553 -> 0.622 (+0.069)
- **Mirage AI**: 0.545 -> 0.579 (+0.034)
- **OpenCore**: 0.501 -> 0.514 (+0.013)
- **OneAI**: 0.405 -> 0.407 (+0.002)

### Events
- **Mirage AI** moved up from #3 to #2
- **Orion Labs** moved down from #2 to #3
- **Apex AI** moved up from #5 to #4
- **OpenCore** moved down from #4 to #5
- **Consumer movement**: 12.6% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OneAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $16,126,696 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,011,054 to OpenCore

### Media Coverage
- Sentiment: 0.20 (positive)
- Genesis Systems surges by 0.069
- Orion Labs raises $60,000,000 from Horizon_Capital
- Genesis Systems takes #1 on coding
- Apex AI takes #1 on safety
- Orion Labs sees surge in adoption (market share +12.4%)
- Consumers are turning away from Mirage AI (market share -10.1%)
- Consumers are turning away from OpenCore (market share -3.9%)

### Consumer Market
- Avg Satisfaction: 0.500
- Switching Rate: 12.6%
- Market Shares: Mirage AI: 49.7%, Orion Labs: 25.2%, Genesis Systems: 11.3%, OpenCore: 9.0%, Apex AI: 4.6%, OneAI: 0.2%

---

## Round 10

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.622 | 0.332 | 16% | 24% | 55% | 5% |
| 2 | Mirage AI | 0.596 | 0.315 | 5% | 35% | 55% | 5% |
| 3 | Orion Labs | 0.560 | 0.318 | 5% | 27% | 46% | 22% |
| 4 | Apex AI | 0.556 | 0.313 | 5% | 19% | 39% | 38% |
| 5 | OpenCore | 0.515 | 0.259 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.450 | 0.206 | 5% | 32% | 54% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.602 | 0.708 | 0.604 | 0.588 | 0.604 |
| Mirage AI | 0.601 | 0.583 | 0.623 | 0.583 | 0.591 |
| Orion Labs | 0.543 | 0.645 | 0.454 | 0.505 | 0.651 |
| Apex AI | 0.529 | 0.611 | 0.553 | 0.595 | 0.492 |
| OpenCore | 0.498 | 0.595 | 0.553 | 0.421 | 0.505 |
| OneAI | 0.422 | 0.440 | 0.379 | 0.490 | 0.517 |

### Score Changes
- **Orion Labs**: 0.559 -> 0.560 (+0.001)
- **Apex AI**: 0.548 -> 0.556 (+0.008)
- **Genesis Systems**: 0.622 -> 0.622 (+0.000)
- **Mirage AI**: 0.579 -> 0.596 (+0.017)
- **OpenCore**: 0.514 -> 0.515 (+0.001)
- **OneAI**: 0.407 -> 0.450 (+0.043)

### Events
- **Regulation** by Regulator: public_warning
- **Consumer movement**: 8.3% of market switched providers

### Other Actor Reasoning
- **Regulator:** public_warning: Follow-up to investigation, risk at 1.00
- **TechVentures:** vc strategy: top allocation $180,000,000 to OneAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OneAI
- **AISI_Fund:** gov strategy: top allocation $10,313,736 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,131,295 to OpenCore

### Media Coverage
- Sentiment: -0.10 (neutral)
- Orion Labs sees surge in adoption (market share +7.8%)
- Genesis Systems sees surge in adoption (market share +3.1%)
- Consumers are turning away from Mirage AI (market share -7.7%)
- Consumers are turning away from OpenCore (market share -3.0%)

### Consumer Market
- Avg Satisfaction: 0.513
- Switching Rate: 8.3%
- Market Shares: Mirage AI: 44.4%, Orion Labs: 29.1%, Genesis Systems: 14.9%, OpenCore: 6.9%, Apex AI: 4.5%, OneAI: 0.2%

### Regulatory Activity
- **public_warning** by Regulator
  > Follow-up to investigation, risk at 1.00

---

## Round 11

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.623 | 0.338 | 16% | 24% | 55% | 5% |
| 2 | Mirage AI | 0.596 | 0.319 | 5% | 35% | 55% | 5% |
| 3 | Apex AI | 0.588 | 0.316 | 5% | 18% | 41% | 36% |
| 4 | Orion Labs | 0.576 | 0.321 | 5% | 26% | 48% | 22% |
| 5 | OpenCore | 0.539 | 0.264 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.476 | 0.212 | 5% | 32% | 54% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.602 | 0.714 | 0.604 | 0.588 | 0.604 |
| Mirage AI | 0.601 | 0.583 | 0.623 | 0.583 | 0.591 |
| Apex AI | 0.569 | 0.611 | 0.553 | 0.595 | 0.609 |
| Orion Labs | 0.543 | 0.645 | 0.535 | 0.505 | 0.651 |
| OpenCore | 0.498 | 0.595 | 0.553 | 0.545 | 0.505 |
| OneAI | 0.422 | 0.440 | 0.511 | 0.490 | 0.517 |

### Score Changes
- **Orion Labs**: 0.560 -> 0.576 (+0.016)
- **Apex AI**: 0.556 -> 0.588 (+0.031)
- **Genesis Systems**: 0.622 -> 0.623 (+0.001)
- **Mirage AI**: 0.596 -> 0.596 (+0.000)
- **OpenCore**: 0.515 -> 0.539 (+0.025)
- **OneAI**: 0.450 -> 0.476 (+0.026)

### Events
- **Apex AI** moved up from #4 to #3
- **Orion Labs** moved down from #3 to #4
- **Consumer movement**: 6.8% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OneAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OneAI
- **AISI_Fund:** gov strategy: top allocation $10,313,736 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,131,295 to OpenCore

### Media Coverage
- Sentiment: 0.00 (neutral)
- Regulator issues public warning about AI safety concerns
- OneAI raises $60,000,000 from Horizon_Capital
- Mirage AI raises $10,313,736 from AISI_Fund
- OpenCore raises $7,131,295 from OpenResearch_Foundation
- Orion Labs sees surge in adoption (market share +3.9%)
- Genesis Systems sees surge in adoption (market share +3.5%)
- Consumers are turning away from Mirage AI (market share -5.3%)
- Risk signals: regulatory_public_warning

### Consumer Market
- Avg Satisfaction: 0.533
- Switching Rate: 6.8%
- Market Shares: Mirage AI: 39.5%, Orion Labs: 31.8%, Genesis Systems: 18.6%, OpenCore: 5.5%, Apex AI: 4.4%, OneAI: 0.2%

---

## Round 12

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.625 | 0.324 | 5% | 35% | 55% | 5% |
| 2 | Genesis Systems | 0.623 | 0.344 | 16% | 24% | 55% | 5% |
| 3 | Apex AI | 0.588 | 0.319 | 5% | 18% | 42% | 35% |
| 4 | Orion Labs | 0.586 | 0.325 | 5% | 25% | 49% | 21% |
| 5 | OpenCore | 0.571 | 0.268 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.545 | 0.218 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.270 | 0.204 | 20% | 35% | 35% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Mirage AI | 0.601 | 0.583 | 0.623 | 0.583 | 0.737 | 0.000 |
| Genesis Systems | 0.602 | 0.714 | 0.604 | 0.588 | 0.604 | 0.000 |
| Apex AI | 0.569 | 0.611 | 0.553 | 0.595 | 0.609 | 0.000 |
| Orion Labs | 0.543 | 0.645 | 0.588 | 0.505 | 0.651 | 0.000 |
| OpenCore | 0.498 | 0.595 | 0.553 | 0.545 | 0.665 | 0.000 |
| OneAI | 0.582 | 0.625 | 0.511 | 0.490 | 0.517 | 0.000 |
| TwoAI | 0.538 | 0.376 | 0.152 | 0.282 | 0.003 | 0.000 |

### Score Changes
- **Orion Labs**: 0.576 -> 0.586 (+0.011)
- **Apex AI**: 0.588 -> 0.588 (+0.000)
- **Genesis Systems**: 0.623 -> 0.623 (+0.000)
- **Mirage AI**: 0.596 -> 0.625 (+0.029)
- **OpenCore**: 0.539 -> 0.571 (+0.032)
- **OneAI**: 0.476 -> 0.545 (+0.069)
- **TwoAI**: 0.270 -> 0.270 (+0.000)

### Events
- **Mirage AI** moved up from #2 to #1
- **Genesis Systems** moved down from #1 to #2
- **Consumer movement**: 5.3% of market switched providers

### New Benchmark Introduced
- **medical** introduced (validity=0.78, exploitability=0.18)
  - Trigger: periodic_introduction:round_12

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OneAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $10,313,736 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,131,295 to OpenCore

### Media Coverage
- Sentiment: 0.45 (positive)
- Mirage AI takes the lead from Genesis Systems
- OneAI surges by 0.069
- New benchmark introduced: medical
- Mirage AI takes #1 on writing
- Genesis Systems sees surge in adoption (market share +3.7%)
- Consumers are turning away from Mirage AI (market share -4.9%)

### Consumer Market
- Avg Satisfaction: 0.547
- Switching Rate: 5.3%
- Market Shares: Mirage AI: 35.5%, Orion Labs: 33.4%, Genesis Systems: 21.6%, OpenCore: 4.7%, Apex AI: 4.3%, TwoAI: 0.3%, OneAI: 0.2%

---

## Round 13

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.597 | 0.350 | 15% | 24% | 55% | 5% |
| 2 | Orion Labs | 0.595 | 0.329 | 5% | 25% | 50% | 21% |
| 3 | Mirage AI | 0.579 | 0.328 | 5% | 35% | 55% | 5% |
| 4 | Apex AI | 0.574 | 0.321 | 5% | 17% | 43% | 34% |
| 5 | OpenCore | 0.535 | 0.273 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.481 | 0.224 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.316 | 0.209 | 8% | 35% | 47% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.602 | 0.727 | 0.604 | 0.588 | 0.604 | 0.456 |
| Orion Labs | 0.543 | 0.645 | 0.686 | 0.505 | 0.651 | 0.541 |
| Mirage AI | 0.601 | 0.583 | 0.623 | 0.583 | 0.737 | 0.345 |
| Apex AI | 0.569 | 0.715 | 0.583 | 0.595 | 0.609 | 0.372 |
| OpenCore | 0.498 | 0.623 | 0.553 | 0.545 | 0.665 | 0.323 |
| OneAI | 0.582 | 0.625 | 0.511 | 0.490 | 0.517 | 0.165 |
| TwoAI | 0.538 | 0.376 | 0.152 | 0.374 | 0.200 | 0.254 |

### Score Changes
- **Orion Labs**: 0.586 -> 0.595 (+0.009)
- **Apex AI**: 0.588 -> 0.574 (-0.014)
- **Genesis Systems**: 0.623 -> 0.597 (-0.026)
- **Mirage AI**: 0.625 -> 0.579 (-0.047)
- **OpenCore**: 0.571 -> 0.535 (-0.037)
- **OneAI**: 0.545 -> 0.481 (-0.063)
- **TwoAI**: 0.270 -> 0.316 (+0.045)

### Events
- **Genesis Systems** moved up from #2 to #1
- **Orion Labs** moved up from #4 to #2
- **Mirage AI** moved down from #1 to #3
- **Apex AI** moved down from #3 to #4
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 8.1% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 6 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to TwoAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $10,313,736 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,372,049 to TwoAI

### Media Coverage
- Sentiment: 0.25 (positive)
- Genesis Systems takes the lead from Mirage AI
- Orion Labs raises $60,000,000 from Horizon_Capital
- Orion Labs takes #1 on math
- Consumers are turning away from Mirage AI (market share -4.0%)

### Consumer Market
- Avg Satisfaction: 0.561
- Switching Rate: 8.1%
- Market Shares: Mirage AI: 37.6%, Orion Labs: 28.8%, Genesis Systems: 24.7%, Apex AI: 4.3%, OpenCore: 4.1%, TwoAI: 0.3%, OneAI: 0.2%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 6 rounds ago

---

## Round 14

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Orion Labs | 0.619 | 0.332 | 5% | 24% | 50% | 20% |
| 2 | Mirage AI | 0.606 | 0.333 | 5% | 35% | 55% | 5% |
| 3 | Genesis Systems | 0.597 | 0.354 | 15% | 24% | 55% | 5% |
| 4 | Apex AI | 0.575 | 0.324 | 5% | 17% | 44% | 34% |
| 5 | OpenCore | 0.535 | 0.278 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.521 | 0.229 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.348 | 0.215 | 5% | 33% | 52% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Orion Labs | 0.543 | 0.645 | 0.686 | 0.600 | 0.698 | 0.541 |
| Mirage AI | 0.607 | 0.583 | 0.623 | 0.583 | 0.737 | 0.500 |
| Genesis Systems | 0.602 | 0.727 | 0.604 | 0.588 | 0.604 | 0.456 |
| Apex AI | 0.569 | 0.715 | 0.583 | 0.595 | 0.609 | 0.382 |
| OpenCore | 0.498 | 0.623 | 0.553 | 0.545 | 0.665 | 0.323 |
| OneAI | 0.582 | 0.625 | 0.511 | 0.490 | 0.517 | 0.405 |
| TwoAI | 0.538 | 0.376 | 0.349 | 0.374 | 0.200 | 0.254 |

### Score Changes
- **Orion Labs**: 0.595 -> 0.619 (+0.024)
- **Apex AI**: 0.574 -> 0.575 (+0.002)
- **Genesis Systems**: 0.597 -> 0.597 (+0.000)
- **Mirage AI**: 0.579 -> 0.606 (+0.027)
- **OpenCore**: 0.535 -> 0.535 (+0.000)
- **OneAI**: 0.481 -> 0.521 (+0.040)
- **TwoAI**: 0.316 -> 0.348 (+0.033)

### Events
- **Orion Labs** moved up from #2 to #1
- **Mirage AI** moved up from #3 to #2
- **Genesis Systems** moved down from #1 to #3
- **Consumer movement**: 6.5% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to TwoAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to TwoAI
- **AISI_Fund:** gov strategy: top allocation $9,064,854 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,372,049 to TwoAI

### Media Coverage
- Sentiment: 0.30 (positive)
- Orion Labs takes the lead from Genesis Systems
- Regulator initiates compliance audit on AI providers
- TwoAI raises $180,000,000 from TechVentures
- TwoAI raises $7,372,049 from OpenResearch_Foundation
- Mirage AI takes #1 on coding
- Orion Labs takes #1 on safety
- Consumers are turning away from Orion Labs (market share -4.6%)
- Genesis Systems sees surge in adoption (market share +3.2%)
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.570
- Switching Rate: 6.5%
- Market Shares: Mirage AI: 39.5%, Genesis Systems: 27.2%, Orion Labs: 25.0%, Apex AI: 4.2%, OpenCore: 3.7%, TwoAI: 0.2%, OneAI: 0.2%

---

## Round 15

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Orion Labs | 0.619 | 0.336 | 5% | 24% | 51% | 20% |
| 2 | Genesis Systems | 0.614 | 0.359 | 15% | 24% | 55% | 5% |
| 3 | Mirage AI | 0.606 | 0.339 | 5% | 35% | 55% | 5% |
| 4 | Apex AI | 0.591 | 0.327 | 5% | 17% | 45% | 33% |
| 5 | OpenCore | 0.538 | 0.282 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.533 | 0.233 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.425 | 0.221 | 5% | 32% | 53% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Orion Labs | 0.543 | 0.645 | 0.686 | 0.600 | 0.698 | 0.541 |
| Genesis Systems | 0.602 | 0.727 | 0.604 | 0.588 | 0.604 | 0.557 |
| Mirage AI | 0.607 | 0.583 | 0.623 | 0.583 | 0.737 | 0.500 |
| Apex AI | 0.569 | 0.715 | 0.583 | 0.595 | 0.704 | 0.382 |
| OpenCore | 0.520 | 0.623 | 0.553 | 0.545 | 0.665 | 0.323 |
| OneAI | 0.582 | 0.625 | 0.511 | 0.524 | 0.517 | 0.442 |
| TwoAI | 0.538 | 0.376 | 0.521 | 0.374 | 0.489 | 0.254 |

### Score Changes
- **Orion Labs**: 0.619 -> 0.619 (+0.000)
- **Apex AI**: 0.575 -> 0.591 (+0.016)
- **Genesis Systems**: 0.597 -> 0.614 (+0.017)
- **Mirage AI**: 0.606 -> 0.606 (+0.000)
- **OpenCore**: 0.535 -> 0.538 (+0.004)
- **OneAI**: 0.521 -> 0.533 (+0.012)
- **TwoAI**: 0.348 -> 0.425 (+0.077)

### Events
- **Genesis Systems** moved up from #3 to #2
- **Mirage AI** moved down from #2 to #3
- **Consumer movement**: 5.5% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to TwoAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to TwoAI
- **AISI_Fund:** gov strategy: top allocation $9,064,854 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,372,049 to TwoAI

### Media Coverage
- Sentiment: 0.20 (positive)
- TwoAI surges by 0.077
- TwoAI raises $60,000,000 from Horizon_Capital
- Mirage AI raises $9,064,854 from AISI_Fund
- Genesis Systems takes #1 on medical
- Consumers are turning away from Orion Labs (market share -3.8%)

### Consumer Market
- Avg Satisfaction: 0.579
- Switching Rate: 5.5%
- Market Shares: Mirage AI: 41.0%, Genesis Systems: 29.3%, Orion Labs: 21.8%, Apex AI: 4.2%, OpenCore: 3.4%, TwoAI: 0.2%, OneAI: 0.2%

---

## Round 16

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.623 | 0.344 | 5% | 35% | 55% | 5% |
| 2 | Orion Labs | 0.619 | 0.339 | 5% | 24% | 51% | 20% |
| 3 | Genesis Systems | 0.615 | 0.364 | 15% | 25% | 55% | 5% |
| 4 | Apex AI | 0.591 | 0.329 | 5% | 16% | 46% | 33% |
| 5 | OpenCore | 0.538 | 0.287 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.533 | 0.237 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.430 | 0.227 | 5% | 32% | 54% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Mirage AI | 0.607 | 0.690 | 0.623 | 0.583 | 0.737 | 0.500 |
| Orion Labs | 0.543 | 0.645 | 0.686 | 0.600 | 0.698 | 0.541 |
| Genesis Systems | 0.602 | 0.727 | 0.613 | 0.588 | 0.604 | 0.557 |
| Apex AI | 0.569 | 0.715 | 0.583 | 0.595 | 0.704 | 0.382 |
| OpenCore | 0.520 | 0.623 | 0.553 | 0.545 | 0.665 | 0.323 |
| OneAI | 0.582 | 0.625 | 0.511 | 0.524 | 0.517 | 0.442 |
| TwoAI | 0.538 | 0.376 | 0.521 | 0.374 | 0.489 | 0.280 |

### Score Changes
- **Orion Labs**: 0.619 -> 0.619 (+0.000)
- **Apex AI**: 0.591 -> 0.591 (+0.000)
- **Genesis Systems**: 0.614 -> 0.615 (+0.001)
- **Mirage AI**: 0.606 -> 0.623 (+0.018)
- **OpenCore**: 0.538 -> 0.538 (+0.000)
- **OneAI**: 0.533 -> 0.533 (+0.000)
- **TwoAI**: 0.425 -> 0.430 (+0.004)

### Events
- **Mirage AI** moved up from #3 to #1
- **Orion Labs** moved down from #1 to #2
- **Genesis Systems** moved down from #2 to #3
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 9 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $9,064,854 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $6,952,888 to OpenCore

### Media Coverage
- Sentiment: 0.10 (neutral)
- Mirage AI takes the lead from Orion Labs
- Consumers are turning away from Orion Labs (market share -3.2%)

### Consumer Market
- Avg Satisfaction: 0.587
- Switching Rate: 4.3%
- Market Shares: Mirage AI: 42.4%, Genesis Systems: 30.8%, Orion Labs: 19.1%, Apex AI: 4.2%, OpenCore: 3.2%, TwoAI: 0.2%, OneAI: 0.2%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 9 rounds ago

---

## Round 17

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.636 | 0.332 | 5% | 16% | 46% | 32% |
| 2 | Mirage AI | 0.623 | 0.350 | 5% | 35% | 55% | 5% |
| 3 | Orion Labs | 0.619 | 0.343 | 5% | 24% | 51% | 20% |
| 4 | Genesis Systems | 0.615 | 0.370 | 15% | 25% | 55% | 5% |
| 5 | OpenCore | 0.543 | 0.291 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.533 | 0.241 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.450 | 0.232 | 5% | 32% | 54% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Apex AI | 0.569 | 0.715 | 0.583 | 0.595 | 0.704 | 0.650 |
| Mirage AI | 0.607 | 0.690 | 0.623 | 0.583 | 0.737 | 0.500 |
| Orion Labs | 0.543 | 0.645 | 0.686 | 0.600 | 0.698 | 0.541 |
| Genesis Systems | 0.603 | 0.727 | 0.613 | 0.588 | 0.604 | 0.557 |
| OpenCore | 0.520 | 0.623 | 0.553 | 0.545 | 0.665 | 0.355 |
| OneAI | 0.582 | 0.625 | 0.511 | 0.524 | 0.517 | 0.442 |
| TwoAI | 0.538 | 0.409 | 0.521 | 0.374 | 0.489 | 0.370 |

### Score Changes
- **Orion Labs**: 0.619 -> 0.619 (+0.000)
- **Apex AI**: 0.591 -> 0.636 (+0.045)
- **Genesis Systems**: 0.615 -> 0.615 (+0.000)
- **Mirage AI**: 0.623 -> 0.623 (+0.000)
- **OpenCore**: 0.538 -> 0.543 (+0.005)
- **OneAI**: 0.533 -> 0.533 (+0.000)
- **TwoAI**: 0.430 -> 0.450 (+0.021)

### Events
- **Apex AI** moved up from #4 to #1
- **Mirage AI** moved down from #1 to #2
- **Orion Labs** moved down from #2 to #3
- **Genesis Systems** moved down from #3 to #4

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $9,064,854 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $6,952,888 to OpenCore

### Media Coverage
- Sentiment: 0.30 (positive)
- Apex AI takes the lead from Mirage AI
- Regulator initiates compliance audit on AI providers
- Mirage AI raises $180,000,000 from TechVentures
- Mirage AI raises $60,000,000 from Horizon_Capital
- OpenCore raises $6,952,888 from OpenResearch_Foundation
- Apex AI takes #1 on medical
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.594
- Switching Rate: 3.7%
- Market Shares: Mirage AI: 43.7%, Genesis Systems: 32.1%, Orion Labs: 16.8%, Apex AI: 4.2%, OpenCore: 3.0%, TwoAI: 0.2%, OneAI: 0.1%

---

## Round 18

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.636 | 0.334 | 5% | 16% | 47% | 32% |
| 2 | Mirage AI | 0.623 | 0.356 | 5% | 35% | 55% | 5% |
| 3 | Orion Labs | 0.619 | 0.346 | 5% | 24% | 51% | 20% |
| 4 | Genesis Systems | 0.615 | 0.376 | 15% | 25% | 55% | 5% |
| 5 | OpenCore | 0.548 | 0.296 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.533 | 0.246 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.472 | 0.236 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Apex AI | 0.569 | 0.715 | 0.583 | 0.595 | 0.704 | 0.650 | 0.000 |
| Mirage AI | 0.607 | 0.690 | 0.623 | 0.583 | 0.737 | 0.500 | 0.000 |
| Orion Labs | 0.543 | 0.645 | 0.686 | 0.600 | 0.698 | 0.541 | 0.000 |
| Genesis Systems | 0.603 | 0.727 | 0.613 | 0.588 | 0.604 | 0.557 | 0.000 |
| OpenCore | 0.520 | 0.623 | 0.553 | 0.545 | 0.665 | 0.382 | 0.000 |
| OneAI | 0.582 | 0.625 | 0.511 | 0.524 | 0.517 | 0.442 | 0.000 |
| TwoAI | 0.538 | 0.409 | 0.521 | 0.502 | 0.489 | 0.370 | 0.000 |

### Score Changes
- **Orion Labs**: 0.619 -> 0.619 (+0.000)
- **Apex AI**: 0.636 -> 0.636 (+0.000)
- **Genesis Systems**: 0.615 -> 0.615 (+0.000)
- **Mirage AI**: 0.623 -> 0.623 (+0.000)
- **OpenCore**: 0.543 -> 0.548 (+0.005)
- **OneAI**: 0.533 -> 0.533 (+0.000)
- **TwoAI**: 0.450 -> 0.472 (+0.022)

### New Benchmark Introduced
- **legal** introduced (validity=0.76, exploitability=0.20)
  - Trigger: periodic_introduction:round_18

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $9,420,141 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $6,952,888 to OpenCore

### Media Coverage
- Sentiment: 0.10 (neutral)
- New benchmark introduced: legal

### Consumer Market
- Avg Satisfaction: 0.600
- Switching Rate: 3.8%
- Market Shares: Mirage AI: 44.8%, Genesis Systems: 31.9%, Orion Labs: 14.9%, Apex AI: 5.3%, OpenCore: 2.8%, TwoAI: 0.2%, OneAI: 0.1%

---

## Round 19

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.620 | 0.381 | 14% | 25% | 55% | 5% |
| 2 | Apex AI | 0.620 | 0.337 | 5% | 16% | 47% | 32% |
| 3 | Orion Labs | 0.604 | 0.349 | 5% | 24% | 51% | 20% |
| 4 | Mirage AI | 0.581 | 0.363 | 5% | 35% | 55% | 5% |
| 5 | OpenCore | 0.534 | 0.301 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.510 | 0.250 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.453 | 0.240 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.603 | 0.727 | 0.613 | 0.588 | 0.604 | 0.557 | 0.648 |
| Apex AI | 0.595 | 0.715 | 0.602 | 0.595 | 0.704 | 0.650 | 0.479 |
| Orion Labs | 0.543 | 0.645 | 0.686 | 0.600 | 0.698 | 0.541 | 0.517 |
| Mirage AI | 0.607 | 0.690 | 0.623 | 0.583 | 0.737 | 0.500 | 0.326 |
| OpenCore | 0.520 | 0.623 | 0.553 | 0.545 | 0.665 | 0.387 | 0.441 |
| OneAI | 0.582 | 0.625 | 0.511 | 0.524 | 0.517 | 0.442 | 0.368 |
| TwoAI | 0.538 | 0.409 | 0.521 | 0.502 | 0.489 | 0.370 | 0.339 |

### Score Changes
- **Orion Labs**: 0.619 -> 0.604 (-0.015)
- **Apex AI**: 0.636 -> 0.620 (-0.016)
- **Genesis Systems**: 0.615 -> 0.620 (+0.005)
- **Mirage AI**: 0.623 -> 0.581 (-0.042)
- **OpenCore**: 0.548 -> 0.534 (-0.015)
- **OneAI**: 0.533 -> 0.510 (-0.024)
- **TwoAI**: 0.472 -> 0.453 (-0.019)

### Events
- **Genesis Systems** moved up from #4 to #1
- **Apex AI** moved down from #1 to #2
- **Mirage AI** moved down from #2 to #4
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 12 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $9,420,141 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,467,627 to OpenCore

### Media Coverage
- Sentiment: 0.20 (positive)
- Genesis Systems takes the lead from Apex AI

### Consumer Market
- Avg Satisfaction: 0.605
- Switching Rate: 3.2%
- Market Shares: Mirage AI: 45.6%, Genesis Systems: 31.9%, Orion Labs: 13.3%, Apex AI: 6.2%, OpenCore: 2.7%, TwoAI: 0.2%, OneAI: 0.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 12 rounds ago

---

## Round 20

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.624 | 0.340 | 5% | 16% | 47% | 32% |
| 2 | Genesis Systems | 0.620 | 0.387 | 14% | 25% | 56% | 5% |
| 3 | Orion Labs | 0.604 | 0.352 | 5% | 24% | 52% | 20% |
| 4 | Mirage AI | 0.597 | 0.368 | 5% | 35% | 55% | 5% |
| 5 | OpenCore | 0.548 | 0.305 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.510 | 0.254 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.453 | 0.244 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Apex AI | 0.595 | 0.715 | 0.602 | 0.595 | 0.704 | 0.650 | 0.507 |
| Genesis Systems | 0.603 | 0.727 | 0.613 | 0.588 | 0.604 | 0.557 | 0.648 |
| Orion Labs | 0.543 | 0.645 | 0.686 | 0.600 | 0.698 | 0.541 | 0.517 |
| Mirage AI | 0.607 | 0.690 | 0.623 | 0.583 | 0.737 | 0.500 | 0.441 |
| OpenCore | 0.520 | 0.623 | 0.553 | 0.545 | 0.665 | 0.435 | 0.496 |
| OneAI | 0.582 | 0.625 | 0.511 | 0.524 | 0.517 | 0.442 | 0.368 |
| TwoAI | 0.538 | 0.409 | 0.521 | 0.502 | 0.489 | 0.370 | 0.339 |

### Score Changes
- **Orion Labs**: 0.604 -> 0.604 (+0.000)
- **Apex AI**: 0.620 -> 0.624 (+0.004)
- **Genesis Systems**: 0.620 -> 0.620 (+0.000)
- **Mirage AI**: 0.581 -> 0.597 (+0.017)
- **OpenCore**: 0.534 -> 0.548 (+0.015)
- **OneAI**: 0.510 -> 0.510 (+0.000)
- **TwoAI**: 0.453 -> 0.453 (+0.000)

### Events
- **Apex AI** moved up from #2 to #1
- **Genesis Systems** moved down from #1 to #2

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $9,420,141 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,467,627 to OpenCore

### Media Coverage
- Sentiment: 0.10 (neutral)
- Apex AI takes the lead from Genesis Systems
- Regulator initiates compliance audit on AI providers
- Genesis Systems raises $180,000,000 from TechVentures
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.605
- Switching Rate: 3.0%
- Market Shares: Mirage AI: 45.9%, Genesis Systems: 32.3%, Orion Labs: 12.0%, Apex AI: 7.0%, OpenCore: 2.6%, TwoAI: 0.2%, OneAI: 0.1%

---

## Round 21

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.624 | 0.342 | 5% | 16% | 47% | 32% |
| 2 | Genesis Systems | 0.620 | 0.394 | 14% | 26% | 56% | 5% |
| 3 | Orion Labs | 0.604 | 0.356 | 5% | 23% | 52% | 20% |
| 4 | Mirage AI | 0.598 | 0.374 | 5% | 35% | 55% | 5% |
| 5 | OpenCore | 0.548 | 0.310 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.513 | 0.258 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.484 | 0.248 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Apex AI | 0.595 | 0.715 | 0.602 | 0.595 | 0.704 | 0.650 | 0.507 |
| Genesis Systems | 0.603 | 0.727 | 0.613 | 0.588 | 0.604 | 0.557 | 0.648 |
| Orion Labs | 0.543 | 0.645 | 0.686 | 0.600 | 0.698 | 0.541 | 0.517 |
| Mirage AI | 0.607 | 0.690 | 0.623 | 0.583 | 0.737 | 0.504 | 0.441 |
| OpenCore | 0.520 | 0.623 | 0.553 | 0.545 | 0.665 | 0.435 | 0.496 |
| OneAI | 0.582 | 0.625 | 0.511 | 0.524 | 0.517 | 0.442 | 0.390 |
| TwoAI | 0.538 | 0.409 | 0.643 | 0.502 | 0.489 | 0.397 | 0.408 |

### Score Changes
- **Orion Labs**: 0.604 -> 0.604 (+0.000)
- **Apex AI**: 0.624 -> 0.624 (+0.000)
- **Genesis Systems**: 0.620 -> 0.620 (+0.000)
- **Mirage AI**: 0.597 -> 0.598 (+0.001)
- **OpenCore**: 0.548 -> 0.548 (+0.000)
- **OneAI**: 0.510 -> 0.513 (+0.003)
- **TwoAI**: 0.453 -> 0.484 (+0.031)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $9,420,141 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,467,627 to OpenCore

### Media Coverage
- Sentiment: 0.05 (neutral)
- Genesis Systems raises $60,000,000 from Horizon_Capital

### Consumer Market
- Avg Satisfaction: 0.607
- Switching Rate: 2.6%
- Market Shares: Mirage AI: 46.0%, Genesis Systems: 32.6%, Orion Labs: 11.0%, Apex AI: 7.6%, OpenCore: 2.5%, TwoAI: 0.2%, OneAI: 0.1%

---

## Round 22

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.626 | 0.345 | 5% | 16% | 47% | 32% |
| 2 | Genesis Systems | 0.620 | 0.401 | 14% | 26% | 55% | 5% |
| 3 | Orion Labs | 0.606 | 0.359 | 5% | 23% | 52% | 19% |
| 4 | Mirage AI | 0.598 | 0.379 | 5% | 35% | 55% | 5% |
| 5 | OpenCore | 0.550 | 0.314 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.524 | 0.262 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.484 | 0.253 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Apex AI | 0.595 | 0.715 | 0.617 | 0.595 | 0.704 | 0.650 | 0.507 |
| Genesis Systems | 0.603 | 0.727 | 0.613 | 0.588 | 0.604 | 0.557 | 0.648 |
| Orion Labs | 0.543 | 0.654 | 0.686 | 0.600 | 0.698 | 0.541 | 0.517 |
| Mirage AI | 0.607 | 0.690 | 0.623 | 0.583 | 0.737 | 0.504 | 0.441 |
| OpenCore | 0.520 | 0.623 | 0.553 | 0.545 | 0.665 | 0.451 | 0.496 |
| OneAI | 0.582 | 0.625 | 0.511 | 0.524 | 0.517 | 0.442 | 0.471 |
| TwoAI | 0.538 | 0.409 | 0.643 | 0.502 | 0.492 | 0.397 | 0.408 |

### Score Changes
- **Orion Labs**: 0.604 -> 0.606 (+0.001)
- **Apex AI**: 0.624 -> 0.626 (+0.002)
- **Genesis Systems**: 0.620 -> 0.620 (+0.000)
- **Mirage AI**: 0.598 -> 0.598 (+0.000)
- **OpenCore**: 0.548 -> 0.550 (+0.002)
- **OneAI**: 0.513 -> 0.524 (+0.012)
- **TwoAI**: 0.484 -> 0.484 (+0.000)

### Events
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 15 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $10,284,921 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,446,588 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.609
- Switching Rate: 2.1%
- Market Shares: Mirage AI: 46.1%, Genesis Systems: 32.9%, Orion Labs: 10.1%, Apex AI: 8.2%, OpenCore: 2.4%, TwoAI: 0.2%, OneAI: 0.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 15 rounds ago

---

## Round 23

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.626 | 0.347 | 5% | 16% | 47% | 32% |
| 2 | Genesis Systems | 0.620 | 0.406 | 14% | 26% | 55% | 5% |
| 3 | Orion Labs | 0.610 | 0.362 | 5% | 23% | 52% | 19% |
| 4 | Mirage AI | 0.603 | 0.385 | 5% | 35% | 55% | 5% |
| 5 | OpenCore | 0.577 | 0.319 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.524 | 0.266 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.484 | 0.257 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Apex AI | 0.595 | 0.715 | 0.617 | 0.595 | 0.704 | 0.650 | 0.507 |
| Genesis Systems | 0.603 | 0.727 | 0.613 | 0.588 | 0.604 | 0.557 | 0.648 |
| Orion Labs | 0.543 | 0.688 | 0.686 | 0.600 | 0.698 | 0.541 | 0.517 |
| Mirage AI | 0.607 | 0.690 | 0.623 | 0.583 | 0.737 | 0.504 | 0.477 |
| OpenCore | 0.520 | 0.623 | 0.553 | 0.624 | 0.665 | 0.451 | 0.605 |
| OneAI | 0.582 | 0.625 | 0.511 | 0.524 | 0.517 | 0.442 | 0.471 |
| TwoAI | 0.538 | 0.409 | 0.643 | 0.502 | 0.492 | 0.397 | 0.408 |

### Score Changes
- **Orion Labs**: 0.606 -> 0.610 (+0.005)
- **Apex AI**: 0.626 -> 0.626 (+0.000)
- **Genesis Systems**: 0.620 -> 0.620 (+0.000)
- **Mirage AI**: 0.598 -> 0.603 (+0.005)
- **OpenCore**: 0.550 -> 0.577 (+0.027)
- **OneAI**: 0.524 -> 0.524 (+0.000)
- **TwoAI**: 0.484 -> 0.484 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $10,284,921 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,446,588 to OpenCore

### Media Coverage
- Sentiment: 0.05 (neutral)
- Regulator initiates compliance audit on AI providers
- Mirage AI raises $180,000,000 from TechVentures
- Mirage AI raises $60,000,000 from Horizon_Capital
- OpenCore takes #1 on safety
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.611
- Switching Rate: 1.9%
- Market Shares: Mirage AI: 46.2%, Genesis Systems: 33.2%, Orion Labs: 9.3%, Apex AI: 8.6%, OpenCore: 2.3%, OneAI: 0.1%, TwoAI: 0.1%

---

## Round 24

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.655 | 0.350 | 5% | 16% | 47% | 32% |
| 2 | Genesis Systems | 0.624 | 0.412 | 14% | 26% | 55% | 5% |
| 3 | Orion Labs | 0.610 | 0.365 | 5% | 23% | 53% | 19% |
| 4 | Mirage AI | 0.603 | 0.391 | 5% | 35% | 55% | 5% |
| 5 | OpenCore | 0.588 | 0.324 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.524 | 0.271 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.505 | 0.261 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Apex AI | 0.595 | 0.715 | 0.711 | 0.595 | 0.704 | 0.650 | 0.615 | 0.000 |
| Genesis Systems | 0.627 | 0.727 | 0.613 | 0.588 | 0.604 | 0.557 | 0.648 | 0.000 |
| Orion Labs | 0.543 | 0.688 | 0.686 | 0.600 | 0.698 | 0.541 | 0.517 | 0.000 |
| Mirage AI | 0.607 | 0.690 | 0.623 | 0.583 | 0.737 | 0.504 | 0.477 | 0.000 |
| OpenCore | 0.520 | 0.623 | 0.553 | 0.624 | 0.665 | 0.528 | 0.605 | 0.000 |
| OneAI | 0.582 | 0.625 | 0.511 | 0.524 | 0.517 | 0.442 | 0.471 | 0.000 |
| TwoAI | 0.538 | 0.409 | 0.643 | 0.502 | 0.492 | 0.540 | 0.408 | 0.000 |

### Score Changes
- **Orion Labs**: 0.610 -> 0.610 (+0.000)
- **Apex AI**: 0.626 -> 0.655 (+0.029)
- **Genesis Systems**: 0.620 -> 0.624 (+0.004)
- **Mirage AI**: 0.603 -> 0.603 (+0.000)
- **OpenCore**: 0.577 -> 0.588 (+0.011)
- **OneAI**: 0.524 -> 0.524 (+0.000)
- **TwoAI**: 0.484 -> 0.505 (+0.021)

### New Benchmark Introduced
- **finance** introduced (validity=0.76, exploitability=0.20)
  - Trigger: periodic_introduction:round_24

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $10,284,921 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,446,588 to OpenCore

### Media Coverage
- Sentiment: 0.30 (positive)
- New benchmark introduced: finance
- Genesis Systems takes #1 on coding
- Apex AI takes #1 on math

### Consumer Market
- Avg Satisfaction: 0.613
- Switching Rate: 1.5%
- Market Shares: Mirage AI: 46.2%, Genesis Systems: 33.5%, Apex AI: 9.0%, Orion Labs: 8.8%, OpenCore: 2.3%, OneAI: 0.1%, TwoAI: 0.1%

---

## Round 25

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.655 | 0.353 | 5% | 16% | 47% | 32% |
| 2 | Genesis Systems | 0.624 | 0.417 | 13% | 26% | 55% | 5% |
| 3 | Orion Labs | 0.602 | 0.369 | 5% | 23% | 53% | 19% |
| 4 | Mirage AI | 0.586 | 0.398 | 5% | 35% | 55% | 5% |
| 5 | OpenCore | 0.583 | 0.328 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.510 | 0.275 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.508 | 0.265 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Apex AI | 0.595 | 0.715 | 0.711 | 0.595 | 0.704 | 0.650 | 0.615 | 0.655 |
| Genesis Systems | 0.627 | 0.727 | 0.613 | 0.672 | 0.604 | 0.557 | 0.648 | 0.546 |
| Orion Labs | 0.543 | 0.688 | 0.686 | 0.600 | 0.698 | 0.541 | 0.517 | 0.540 |
| Mirage AI | 0.607 | 0.690 | 0.623 | 0.596 | 0.737 | 0.504 | 0.477 | 0.452 |
| OpenCore | 0.520 | 0.623 | 0.553 | 0.624 | 0.665 | 0.528 | 0.605 | 0.545 |
| OneAI | 0.582 | 0.625 | 0.511 | 0.524 | 0.517 | 0.460 | 0.557 | 0.306 |
| TwoAI | 0.538 | 0.438 | 0.643 | 0.502 | 0.492 | 0.540 | 0.408 | 0.505 |

### Score Changes
- **Orion Labs**: 0.610 -> 0.602 (-0.009)
- **Apex AI**: 0.655 -> 0.655 (+0.000)
- **Genesis Systems**: 0.624 -> 0.624 (+0.001)
- **Mirage AI**: 0.603 -> 0.586 (-0.017)
- **OpenCore**: 0.588 -> 0.583 (-0.005)
- **OneAI**: 0.524 -> 0.510 (-0.014)
- **TwoAI**: 0.505 -> 0.508 (+0.004)

### Events
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 18 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $10,284,921 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,716,451 to OpenCore

### Media Coverage
- Sentiment: 0.10 (neutral)
- Genesis Systems takes #1 on safety

### Consumer Market
- Avg Satisfaction: 0.616
- Switching Rate: 3.0%
- Market Shares: Mirage AI: 45.6%, Genesis Systems: 34.2%, Apex AI: 9.4%, Orion Labs: 8.2%, OpenCore: 2.2%, OneAI: 0.1%, TwoAI: 0.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 18 rounds ago

---

## Round 26

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.655 | 0.355 | 6% | 16% | 46% | 32% |
| 2 | Genesis Systems | 0.625 | 0.423 | 13% | 27% | 56% | 5% |
| 3 | Mirage AI | 0.603 | 0.403 | 5% | 35% | 55% | 5% |
| 4 | Orion Labs | 0.602 | 0.372 | 5% | 23% | 54% | 19% |
| 5 | OpenCore | 0.592 | 0.333 | 5% | 37% | 55% | 3% |
| 6 | TwoAI | 0.519 | 0.269 | 5% | 31% | 55% | 9% |
| 7 | OneAI | 0.510 | 0.279 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Apex AI | 0.595 | 0.715 | 0.711 | 0.595 | 0.708 | 0.650 | 0.615 | 0.655 |
| Genesis Systems | 0.627 | 0.727 | 0.617 | 0.672 | 0.604 | 0.557 | 0.648 | 0.546 |
| Mirage AI | 0.607 | 0.690 | 0.623 | 0.596 | 0.737 | 0.504 | 0.477 | 0.589 |
| Orion Labs | 0.543 | 0.688 | 0.686 | 0.600 | 0.698 | 0.541 | 0.517 | 0.540 |
| OpenCore | 0.520 | 0.623 | 0.553 | 0.624 | 0.665 | 0.528 | 0.605 | 0.620 |
| TwoAI | 0.538 | 0.438 | 0.643 | 0.502 | 0.492 | 0.540 | 0.493 | 0.505 |
| OneAI | 0.582 | 0.625 | 0.511 | 0.524 | 0.517 | 0.460 | 0.557 | 0.306 |

### Score Changes
- **Orion Labs**: 0.602 -> 0.602 (+0.000)
- **Apex AI**: 0.655 -> 0.655 (+0.000)
- **Genesis Systems**: 0.624 -> 0.625 (+0.001)
- **Mirage AI**: 0.586 -> 0.603 (+0.017)
- **OpenCore**: 0.583 -> 0.592 (+0.009)
- **OneAI**: 0.510 -> 0.510 (+0.000)
- **TwoAI**: 0.508 -> 0.519 (+0.011)

### Events
- **Mirage AI** moved up from #4 to #3
- **Orion Labs** moved down from #3 to #4
- **TwoAI** moved up from #7 to #6
- **OneAI** moved down from #6 to #7

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $8,600,978 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,716,451 to OpenCore

### Media Coverage
- Sentiment: -0.10 (neutral)
- Regulator initiates compliance audit on AI providers
- Genesis Systems raises $180,000,000 from TechVentures
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.613
- Switching Rate: 4.2%
- Market Shares: Mirage AI: 41.9%, Genesis Systems: 34.8%, Apex AI: 10.6%, Orion Labs: 7.8%, OpenCore: 4.6%, OneAI: 0.1%, TwoAI: 0.1%

---

## Round 27

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.655 | 0.358 | 6% | 16% | 46% | 32% |
| 2 | Genesis Systems | 0.630 | 0.430 | 12% | 27% | 56% | 5% |
| 3 | Orion Labs | 0.623 | 0.375 | 5% | 22% | 54% | 19% |
| 4 | Mirage AI | 0.603 | 0.408 | 5% | 35% | 55% | 5% |
| 5 | OpenCore | 0.592 | 0.337 | 5% | 37% | 55% | 3% |
| 6 | TwoAI | 0.525 | 0.273 | 5% | 31% | 55% | 9% |
| 7 | OneAI | 0.511 | 0.283 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Apex AI | 0.595 | 0.715 | 0.711 | 0.595 | 0.708 | 0.650 | 0.615 | 0.655 |
| Genesis Systems | 0.627 | 0.727 | 0.617 | 0.690 | 0.604 | 0.585 | 0.648 | 0.546 |
| Orion Labs | 0.543 | 0.688 | 0.686 | 0.635 | 0.698 | 0.543 | 0.650 | 0.540 |
| Mirage AI | 0.607 | 0.690 | 0.623 | 0.596 | 0.737 | 0.504 | 0.477 | 0.589 |
| OpenCore | 0.520 | 0.623 | 0.553 | 0.624 | 0.665 | 0.528 | 0.605 | 0.620 |
| TwoAI | 0.538 | 0.449 | 0.643 | 0.502 | 0.527 | 0.540 | 0.493 | 0.505 |
| OneAI | 0.582 | 0.625 | 0.511 | 0.524 | 0.517 | 0.460 | 0.557 | 0.315 |

### Score Changes
- **Orion Labs**: 0.602 -> 0.623 (+0.021)
- **Apex AI**: 0.655 -> 0.655 (+0.000)
- **Genesis Systems**: 0.625 -> 0.630 (+0.006)
- **Mirage AI**: 0.603 -> 0.603 (+0.000)
- **OpenCore**: 0.592 -> 0.592 (+0.000)
- **OneAI**: 0.510 -> 0.511 (+0.001)
- **TwoAI**: 0.519 -> 0.525 (+0.006)

### Events
- **Orion Labs** moved up from #4 to #3
- **Mirage AI** moved down from #3 to #4

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $8,600,978 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,716,451 to OpenCore

### Media Coverage
- Sentiment: 0.10 (neutral)
- Genesis Systems raises $60,000,000 from Horizon_Capital
- Genesis Systems raises $8,600,978 from AISI_Fund
- Orion Labs takes #1 on legal
- Consumers are turning away from Mirage AI (market share -3.7%)

### Consumer Market
- Avg Satisfaction: 0.618
- Switching Rate: 3.3%
- Market Shares: Mirage AI: 41.4%, Genesis Systems: 35.5%, Apex AI: 11.5%, Orion Labs: 7.4%, OpenCore: 4.0%, OneAI: 0.1%, TwoAI: 0.1%

---

## Round 28

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.655 | 0.361 | 7% | 16% | 45% | 32% |
| 2 | Genesis Systems | 0.653 | 0.436 | 11% | 28% | 56% | 5% |
| 3 | Orion Labs | 0.623 | 0.378 | 5% | 22% | 55% | 18% |
| 4 | Mirage AI | 0.618 | 0.413 | 5% | 35% | 55% | 5% |
| 5 | OpenCore | 0.592 | 0.342 | 5% | 37% | 55% | 3% |
| 6 | TwoAI | 0.525 | 0.277 | 5% | 31% | 55% | 9% |
| 7 | OneAI | 0.512 | 0.287 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Apex AI | 0.595 | 0.715 | 0.711 | 0.595 | 0.708 | 0.650 | 0.615 | 0.655 |
| Genesis Systems | 0.627 | 0.727 | 0.617 | 0.690 | 0.788 | 0.585 | 0.648 | 0.546 |
| Orion Labs | 0.543 | 0.688 | 0.686 | 0.635 | 0.698 | 0.543 | 0.650 | 0.540 |
| Mirage AI | 0.607 | 0.690 | 0.743 | 0.596 | 0.737 | 0.504 | 0.477 | 0.589 |
| OpenCore | 0.520 | 0.623 | 0.553 | 0.624 | 0.665 | 0.528 | 0.605 | 0.620 |
| TwoAI | 0.538 | 0.449 | 0.643 | 0.502 | 0.527 | 0.540 | 0.493 | 0.505 |
| OneAI | 0.582 | 0.625 | 0.521 | 0.524 | 0.517 | 0.460 | 0.557 | 0.315 |

### Score Changes
- **Orion Labs**: 0.623 -> 0.623 (+0.000)
- **Apex AI**: 0.655 -> 0.655 (+0.000)
- **Genesis Systems**: 0.630 -> 0.653 (+0.023)
- **Mirage AI**: 0.603 -> 0.618 (+0.015)
- **OpenCore**: 0.592 -> 0.592 (+0.000)
- **OneAI**: 0.511 -> 0.512 (+0.001)
- **TwoAI**: 0.525 -> 0.525 (+0.000)

### Events
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 21 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $8,600,978 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,304,161 to OpenCore

### Media Coverage
- Sentiment: 0.20 (positive)
- Mirage AI takes #1 on math
- Genesis Systems takes #1 on writing

### Consumer Market
- Avg Satisfaction: 0.620
- Switching Rate: 2.5%
- Market Shares: Mirage AI: 40.9%, Genesis Systems: 36.1%, Apex AI: 12.0%, Orion Labs: 7.1%, OpenCore: 3.6%, OneAI: 0.1%, TwoAI: 0.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 21 rounds ago

---

## Round 29

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.660 | 0.364 | 7% | 16% | 45% | 32% |
| 2 | Genesis Systems | 0.657 | 0.442 | 11% | 28% | 56% | 5% |
| 3 | Mirage AI | 0.636 | 0.418 | 5% | 35% | 55% | 5% |
| 4 | Orion Labs | 0.623 | 0.381 | 5% | 22% | 55% | 18% |
| 5 | OpenCore | 0.592 | 0.346 | 5% | 37% | 55% | 3% |
| 6 | TwoAI | 0.527 | 0.281 | 5% | 31% | 55% | 9% |
| 7 | OneAI | 0.525 | 0.291 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Apex AI | 0.595 | 0.715 | 0.711 | 0.595 | 0.741 | 0.650 | 0.615 | 0.655 |
| Genesis Systems | 0.627 | 0.727 | 0.617 | 0.690 | 0.788 | 0.613 | 0.648 | 0.546 |
| Mirage AI | 0.607 | 0.690 | 0.743 | 0.596 | 0.737 | 0.591 | 0.537 | 0.589 |
| Orion Labs | 0.543 | 0.688 | 0.686 | 0.635 | 0.698 | 0.543 | 0.650 | 0.540 |
| OpenCore | 0.520 | 0.623 | 0.553 | 0.624 | 0.665 | 0.528 | 0.605 | 0.620 |
| TwoAI | 0.538 | 0.467 | 0.643 | 0.502 | 0.527 | 0.540 | 0.493 | 0.505 |
| OneAI | 0.582 | 0.625 | 0.521 | 0.524 | 0.517 | 0.501 | 0.557 | 0.373 |

### Score Changes
- **Orion Labs**: 0.623 -> 0.623 (+0.000)
- **Apex AI**: 0.655 -> 0.660 (+0.004)
- **Genesis Systems**: 0.653 -> 0.657 (+0.004)
- **Mirage AI**: 0.618 -> 0.636 (+0.018)
- **OpenCore**: 0.592 -> 0.592 (+0.000)
- **OneAI**: 0.512 -> 0.525 (+0.012)
- **TwoAI**: 0.525 -> 0.527 (+0.002)

### Events
- **Mirage AI** moved up from #4 to #3
- **Orion Labs** moved down from #3 to #4

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $8,600,978 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,304,161 to OpenCore

### Media Coverage
- Sentiment: -0.15 (negative)
- Regulator initiates compliance audit on AI providers
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.621
- Switching Rate: 4.0%
- Market Shares: Mirage AI: 38.7%, Genesis Systems: 37.4%, Apex AI: 13.6%, Orion Labs: 6.8%, OpenCore: 3.3%, OneAI: 0.1%, TwoAI: 0.1%

---

## Final Summary

### Final Standings
| Rank | Provider | Final Score | Cap Growth | Avg Research | Avg EvalEng |
|------|----------|-------------|------------|--------------|-------------|
| 1 | Apex AI | 0.660 | +0.094 | 9% | 38% |
| 2 | Genesis Systems | 0.657 | +0.182 | 19% | 50% |
| 3 | Mirage AI | 0.636 | +0.178 | 7% | 51% |
| 4 | Orion Labs | 0.623 | +0.111 | 7% | 46% |
| 5 | OpenCore | 0.592 | +0.136 | 6% | 54% |
| 6 | TwoAI | 0.527 | +0.281 | 6% | 53% |
| 7 | OneAI | 0.525 | +0.291 | 6% | 54% |

### Event Summary
- **Rank changes:** 58
- **Strategy shifts:** 0
- **Regulatory actions:** 10
- **Consumer movement events:** 12

### Key Insights
- **Goodhart's Law effect detected:** Apex AI leads on benchmark scores, but Genesis Systems has the highest true capability.
- **Orion Labs** prioritized evaluation engineering (avg 46%)
- **Apex AI** prioritized evaluation engineering (avg 38%)
- **Genesis Systems** prioritized evaluation engineering (avg 50%)
- **Mirage AI** prioritized evaluation engineering (avg 51%)
- **OpenCore** prioritized evaluation engineering (avg 54%)
- **OneAI** prioritized evaluation engineering (avg 43%)
