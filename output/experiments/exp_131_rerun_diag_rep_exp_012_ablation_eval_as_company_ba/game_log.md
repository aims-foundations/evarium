# Game Log: rerun_diag_rep_exp_012_ablation_eval_as_company_balanced

**Experiment ID:** exp_131_rerun_diag_rep_exp_012_ablation_eval_as_company_ba
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
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Mirage AI, $5,000,000 to evaluator

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
| Mirage AI | 0.401 | 0.561 | 0.439 | 0.297 |
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
- **TechVentures:** vc strategy: top allocation $171,000,000 to Mirage AI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Mirage AI, $5,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,640,226 to Mirage AI, $8,000,000 to evaluator

### Media Coverage
- Sentiment: 0.45 (positive)
- OpenCore surges by 0.054
- Orion Labs surges by 0.066
- Genesis Systems surges by 0.087
- Genesis Systems appears to release major model update
- Mirage AI raises $57,000,000 from Horizon_Capital
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
| 1 | OpenCore | 0.455 | 0.221 | 10% | 35% | 52% | 3% |
| 2 | Genesis Systems | 0.448 | 0.279 | 37% | 30% | 28% | 5% |
| 3 | Mirage AI | 0.443 | 0.261 | 16% | 43% | 36% | 5% |
| 4 | Orion Labs | 0.395 | 0.282 | 18% | 30% | 27% | 25% |
| 5 | Apex AI | 0.376 | 0.283 | 24% | 20% | 16% | 40% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| OpenCore | 0.448 | 0.431 | 0.540 | 0.402 |
| Genesis Systems | 0.560 | 0.435 | 0.391 | 0.405 |
| Mirage AI | 0.418 | 0.561 | 0.439 | 0.355 |
| Orion Labs | 0.448 | 0.448 | 0.287 | 0.396 |
| Apex AI | 0.389 | 0.386 | 0.339 | 0.388 |

### Score Changes
- **Orion Labs**: 0.339 -> 0.395 (+0.055)
- **Apex AI**: 0.363 -> 0.376 (+0.013)
- **Genesis Systems**: 0.312 -> 0.448 (+0.136)
- **Mirage AI**: 0.424 -> 0.443 (+0.019)
- **OpenCore**: 0.395 -> 0.455 (+0.060)

### Events
- **OpenCore** moved up from #2 to #1
- **Genesis Systems** moved up from #5 to #2
- **Mirage AI** moved down from #1 to #3
- **Apex AI** moved down from #3 to #5
- **Consumer movement**: 5.1% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Mirage AI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Genesis Systems, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $9,033,218 to Mirage AI, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,640,226 to Mirage AI, $8,000,000 to evaluator

### Media Coverage
- Sentiment: 0.50 (positive)
- OpenCore takes the lead from Mirage AI
- OpenCore surges by 0.060
- Genesis Systems surges by 0.135
- Genesis Systems appears to release major model update
- Orion Labs surges by 0.056
- Regulatory action: threshold_announcement
- Mirage AI raises $171,000,000 from TechVentures
- __EVALUATOR__ raises $8,000,000 from OpenResearch_Foundation
- Genesis Systems takes #1 on coding
- OpenCore takes #1 on math
- Consumers are turning away from Orion Labs (market share -4.4%)
- Consumers are turning away from Genesis Systems (market share -3.6%)
- Mirage AI sees surge in adoption (market share +9.4%)
- Risk signals: regulatory_threshold_announcement

### Consumer Market
- Avg Satisfaction: 0.387
- Switching Rate: 5.1%
- Market Shares: Mirage AI: 62.0%, Apex AI: 13.1%, OpenCore: 10.1%, Orion Labs: 8.6%, Genesis Systems: 6.3%

---

## Round 3

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.524 | 0.270 | 15% | 42% | 39% | 5% |
| 2 | Genesis Systems | 0.507 | 0.288 | 32% | 29% | 34% | 5% |
| 3 | OpenCore | 0.486 | 0.226 | 8% | 35% | 54% | 3% |
| 4 | Orion Labs | 0.457 | 0.287 | 15% | 30% | 30% | 25% |
| 5 | Apex AI | 0.437 | 0.288 | 21% | 20% | 19% | 40% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Mirage AI | 0.421 | 0.561 | 0.650 | 0.464 |
| Genesis Systems | 0.562 | 0.486 | 0.499 | 0.481 |
| OpenCore | 0.448 | 0.553 | 0.540 | 0.402 |
| Orion Labs | 0.448 | 0.448 | 0.538 | 0.396 |
| Apex AI | 0.389 | 0.386 | 0.583 | 0.388 |

### Score Changes
- **Orion Labs**: 0.395 -> 0.457 (+0.063)
- **Apex AI**: 0.376 -> 0.437 (+0.061)
- **Genesis Systems**: 0.448 -> 0.507 (+0.059)
- **Mirage AI**: 0.443 -> 0.524 (+0.081)
- **OpenCore**: 0.455 -> 0.486 (+0.031)

### Events
- **Mirage AI** moved up from #3 to #1
- **OpenCore** moved down from #1 to #3
- **Consumer movement**: 6.8% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Mirage AI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Genesis Systems, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $9,033,218 to Mirage AI, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,640,226 to Mirage AI, $8,000,000 to evaluator

### Media Coverage
- Sentiment: 0.85 (positive)
- Mirage AI takes the lead from OpenCore
- Mirage AI surges by 0.081
- Mirage AI appears to release major model update
- Genesis Systems surges by 0.059
- Orion Labs surges by 0.063
- Apex AI surges by 0.061
- Genesis Systems raises $57,000,000 from Horizon_Capital
- __EVALUATOR__ raises $15,000,000 from AISI_Fund
- Mirage AI takes #1 on math
- Mirage AI sees surge in adoption (market share +3.4%)

### Consumer Market
- Avg Satisfaction: 0.406
- Switching Rate: 6.8%
- Market Shares: Mirage AI: 65.1%, Apex AI: 9.8%, Genesis Systems: 9.4%, OpenCore: 8.4%, Orion Labs: 7.3%

---

## Round 4

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.563 | 0.278 | 13% | 41% | 42% | 5% |
| 2 | Genesis Systems | 0.511 | 0.297 | 28% | 27% | 40% | 5% |
| 3 | OpenCore | 0.486 | 0.231 | 6% | 35% | 56% | 3% |
| 4 | Orion Labs | 0.479 | 0.292 | 13% | 30% | 32% | 25% |
| 5 | Apex AI | 0.470 | 0.292 | 18% | 20% | 22% | 40% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Mirage AI | 0.531 | 0.561 | 0.650 | 0.510 |
| Genesis Systems | 0.562 | 0.502 | 0.499 | 0.481 |
| OpenCore | 0.448 | 0.553 | 0.540 | 0.402 |
| Orion Labs | 0.533 | 0.448 | 0.538 | 0.396 |
| Apex AI | 0.438 | 0.472 | 0.583 | 0.388 |

### Score Changes
- **Orion Labs**: 0.457 -> 0.479 (+0.021)
- **Apex AI**: 0.437 -> 0.470 (+0.034)
- **Genesis Systems**: 0.507 -> 0.511 (+0.004)
- **Mirage AI**: 0.524 -> 0.563 (+0.039)
- **OpenCore**: 0.486 -> 0.486 (+0.000)

### Events
- **Regulation** by Regulator: investigation

### Other Actor Reasoning
- **Regulator:** investigation: Risk elevated (0.77)
- **TechVentures:** vc strategy: top allocation $171,000,000 to Mirage AI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Mirage AI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $9,033,218 to Mirage AI, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,386,570 to Mirage AI, $8,000,000 to evaluator

### Media Coverage
- Sentiment: 0.10 (neutral)
- Mirage AI takes #1 on safety
- Consumers are turning away from Apex AI (market share -3.2%)
- Genesis Systems sees surge in adoption (market share +3.0%)
- Mirage AI sees surge in adoption (market share +3.1%)

### Consumer Market
- Avg Satisfaction: 0.426
- Switching Rate: 4.2%
- Market Shares: Mirage AI: 67.7%, Genesis Systems: 10.6%, Apex AI: 8.0%, OpenCore: 6.9%, Orion Labs: 6.8%

### Regulatory Activity
- **investigation** by Regulator
  > Risk elevated (0.77)

---

## Round 5

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.563 | 0.286 | 12% | 39% | 45% | 5% |
| 2 | Genesis Systems | 0.517 | 0.304 | 25% | 26% | 45% | 5% |
| 3 | OpenCore | 0.495 | 0.235 | 5% | 36% | 56% | 3% |
| 4 | Orion Labs | 0.485 | 0.297 | 9% | 30% | 36% | 25% |
| 5 | Apex AI | 0.477 | 0.297 | 14% | 20% | 26% | 40% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Mirage AI | 0.531 | 0.561 | 0.650 | 0.510 |
| Genesis Systems | 0.565 | 0.502 | 0.519 | 0.481 |
| OpenCore | 0.460 | 0.553 | 0.567 | 0.402 |
| Orion Labs | 0.544 | 0.461 | 0.538 | 0.396 |
| Apex AI | 0.464 | 0.472 | 0.583 | 0.388 |

### Score Changes
- **Orion Labs**: 0.479 -> 0.485 (+0.006)
- **Apex AI**: 0.470 -> 0.477 (+0.007)
- **Genesis Systems**: 0.511 -> 0.517 (+0.006)
- **Mirage AI**: 0.563 -> 0.563 (+0.000)
- **OpenCore**: 0.486 -> 0.495 (+0.010)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Mirage AI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Mirage AI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $9,033,218 to Mirage AI, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,386,570 to Mirage AI, $8,000,000 to evaluator

### Media Coverage
- Sentiment: -0.10 (neutral)
- Regulator launches investigation into elevated_risk
- Mirage AI raises $57,000,000 from Horizon_Capital
- Risk signals: regulatory_investigation

### Consumer Market
- Avg Satisfaction: 0.442
- Switching Rate: 3.1%
- Market Shares: Mirage AI: 69.5%, Genesis Systems: 11.5%, Apex AI: 6.8%, Orion Labs: 6.4%, OpenCore: 5.7%

---

## Round 6

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.563 | 0.294 | 10% | 37% | 48% | 5% |
| 2 | Genesis Systems | 0.535 | 0.311 | 20% | 25% | 50% | 5% |
| 3 | Apex AI | 0.506 | 0.300 | 10% | 20% | 30% | 40% |
| 4 | Orion Labs | 0.500 | 0.300 | 6% | 30% | 39% | 25% |
| 5 | OpenCore | 0.498 | 0.240 | 5% | 36% | 56% | 3% |
| 6 | OneAI | 0.246 | 0.183 | 20% | 35% | 35% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Mirage AI | 0.531 | 0.561 | 0.650 | 0.510 | 0.000 |
| Genesis Systems | 0.565 | 0.576 | 0.519 | 0.481 | 0.000 |
| Apex AI | 0.464 | 0.480 | 0.583 | 0.497 | 0.000 |
| Orion Labs | 0.544 | 0.502 | 0.538 | 0.417 | 0.000 |
| OpenCore | 0.460 | 0.553 | 0.567 | 0.412 | 0.000 |
| OneAI | 0.302 | 0.300 | 0.077 | 0.305 | 0.000 |

### Score Changes
- **Orion Labs**: 0.485 -> 0.500 (+0.016)
- **Apex AI**: 0.477 -> 0.506 (+0.029)
- **Genesis Systems**: 0.517 -> 0.535 (+0.018)
- **Mirage AI**: 0.563 -> 0.563 (+0.000)
- **OpenCore**: 0.495 -> 0.498 (+0.003)
- **OneAI**: 0.246 -> 0.246 (+0.000)

### Events
- **Apex AI** moved up from #5 to #3
- **OpenCore** moved down from #3 to #5

### New Benchmark Introduced
- **writing** introduced (validity=0.72, exploitability=0.30)
  - Trigger: periodic_introduction:round_6

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Mirage AI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Mirage AI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $9,999,164 to Mirage AI, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,386,570 to Mirage AI, $8,000,000 to evaluator

### Media Coverage
- Sentiment: 0.20 (positive)
- New benchmark introduced: writing
- Genesis Systems takes #1 on reasoning

### Consumer Market
- Avg Satisfaction: 0.460
- Switching Rate: 2.6%
- Market Shares: Mirage AI: 70.7%, Genesis Systems: 11.9%, Orion Labs: 6.2%, Apex AI: 6.1%, OpenCore: 4.8%, OneAI: 0.4%

---

## Round 7

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Orion Labs | 0.596 | 0.304 | 5% | 29% | 42% | 24% |
| 2 | Mirage AI | 0.571 | 0.301 | 10% | 35% | 50% | 5% |
| 3 | Genesis Systems | 0.560 | 0.317 | 17% | 24% | 54% | 5% |
| 4 | Apex AI | 0.559 | 0.303 | 7% | 20% | 33% | 40% |
| 5 | OpenCore | 0.494 | 0.245 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.319 | 0.188 | 9% | 35% | 46% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Orion Labs | 0.544 | 0.570 | 0.538 | 0.417 | 0.912 |
| Mirage AI | 0.668 | 0.561 | 0.650 | 0.510 | 0.464 |
| Genesis Systems | 0.621 | 0.634 | 0.519 | 0.481 | 0.543 |
| Apex AI | 0.535 | 0.605 | 0.583 | 0.516 | 0.556 |
| OpenCore | 0.460 | 0.553 | 0.610 | 0.412 | 0.435 |
| OneAI | 0.328 | 0.373 | 0.311 | 0.347 | 0.235 |

### Score Changes
- **Orion Labs**: 0.500 -> 0.596 (+0.096)
- **Apex AI**: 0.506 -> 0.559 (+0.053)
- **Genesis Systems**: 0.535 -> 0.560 (+0.024)
- **Mirage AI**: 0.563 -> 0.571 (+0.007)
- **OpenCore**: 0.498 -> 0.494 (-0.004)
- **OneAI**: 0.246 -> 0.319 (+0.073)

### Events
- **Orion Labs** moved up from #4 to #1
- **Mirage AI** moved down from #1 to #2
- **Genesis Systems** moved down from #2 to #3
- **Apex AI** moved down from #3 to #4
- **Regulation** by Regulator: mandate_benchmark
- **Consumer movement**: 9.6% of market switched providers

### Other Actor Reasoning
- **Regulator:** mandate_benchmark: High risk (0.96) with prior investigation
- **TechVentures:** vc strategy: top allocation $171,000,000 to OneAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Mirage AI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $9,999,164 to Mirage AI, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $6,473,593 to OneAI, $8,000,000 to evaluator

### Media Coverage
- Sentiment: 0.70 (positive)
- Orion Labs takes the lead from Mirage AI
- Orion Labs surges by 0.096
- Orion Labs appears to release major model update
- Apex AI surges by 0.053
- OneAI surges by 0.073
- Mirage AI takes #1 on coding
- Apex AI takes #1 on safety

### Consumer Market
- Avg Satisfaction: 0.469
- Switching Rate: 9.6%
- Market Shares: Mirage AI: 65.8%, Orion Labs: 13.1%, Genesis Systems: 11.2%, Apex AI: 5.6%, OpenCore: 4.0%, OneAI: 0.2%

### Regulatory Activity
- **mandate_benchmark** by Regulator
  > High risk (0.96) with prior investigation

---

## Round 8

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.603 | 0.306 | 9% | 34% | 52% | 5% |
| 2 | Orion Labs | 0.596 | 0.309 | 5% | 28% | 40% | 27% |
| 3 | Genesis Systems | 0.594 | 0.322 | 16% | 24% | 55% | 5% |
| 4 | Apex AI | 0.594 | 0.306 | 5% | 20% | 36% | 40% |
| 5 | OpenCore | 0.533 | 0.249 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.389 | 0.194 | 5% | 33% | 52% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Mirage AI | 0.668 | 0.561 | 0.650 | 0.510 | 0.625 |
| Orion Labs | 0.544 | 0.570 | 0.538 | 0.417 | 0.912 |
| Genesis Systems | 0.621 | 0.634 | 0.690 | 0.481 | 0.543 |
| Apex AI | 0.553 | 0.717 | 0.627 | 0.516 | 0.556 |
| OpenCore | 0.460 | 0.553 | 0.610 | 0.496 | 0.546 |
| OneAI | 0.328 | 0.373 | 0.311 | 0.524 | 0.410 |

### Score Changes
- **Orion Labs**: 0.596 -> 0.596 (+0.000)
- **Apex AI**: 0.559 -> 0.594 (+0.034)
- **Genesis Systems**: 0.560 -> 0.594 (+0.034)
- **Mirage AI**: 0.571 -> 0.603 (+0.032)
- **OpenCore**: 0.494 -> 0.533 (+0.039)
- **OneAI**: 0.319 -> 0.389 (+0.070)

### Events
- **Mirage AI** moved up from #2 to #1
- **Orion Labs** moved down from #1 to #2
- **Regulation** by Regulator: emergency_investigation
- **Consumer movement**: 6.9% of market switched providers

### Other Actor Reasoning
- **Regulator:** emergency_investigation: Critical incident: safety_failure: Orion Labs catastrophic failure in safety-critical application, criminal negligence alleged
- **TechVentures:** vc strategy: top allocation $171,000,000 to OneAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OneAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $9,999,164 to Mirage AI, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $6,473,593 to OneAI, $8,000,000 to evaluator

### Media Coverage
- Sentiment: 0.05 (neutral)
- Mirage AI takes the lead from Orion Labs
- OneAI surges by 0.070
- Regulator mandates new benchmark standards
- OneAI raises $171,000,000 from TechVentures
- Apex AI takes #1 on reasoning
- Genesis Systems takes #1 on math
- OneAI takes #1 on safety
- Orion Labs sees surge in adoption (market share +7.0%)
- Consumers are turning away from Mirage AI (market share -4.9%)
- Orion Labs catastrophic failure in safety-critical application, criminal negligence alleged
- Risk signals: regulatory_mandate_benchmark, incident_safety_failure

### Consumer Market
- Avg Satisfaction: 0.467
- Switching Rate: 6.9%
- Market Shares: Mirage AI: 69.9%, Orion Labs: 10.7%, Genesis Systems: 10.3%, Apex AI: 5.3%, OpenCore: 3.6%, OneAI: 0.2%

### Regulatory Activity
- **emergency_investigation** by Regulator
  > Critical incident: safety_failure: Orion Labs catastrophic failure in safety-critical application, criminal negligence alleged

---

## Round 9

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.657 | 0.327 | 14% | 25% | 56% | 5% |
| 2 | Mirage AI | 0.616 | 0.311 | 8% | 33% | 54% | 5% |
| 3 | Orion Labs | 0.596 | 0.313 | 5% | 29% | 10% | 56% |
| 4 | Apex AI | 0.594 | 0.309 | 5% | 19% | 37% | 39% |
| 5 | OpenCore | 0.533 | 0.254 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.479 | 0.200 | 5% | 32% | 53% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.621 | 0.832 | 0.690 | 0.514 | 0.631 |
| Mirage AI | 0.668 | 0.561 | 0.650 | 0.510 | 0.692 |
| Orion Labs | 0.544 | 0.570 | 0.538 | 0.417 | 0.912 |
| Apex AI | 0.553 | 0.717 | 0.627 | 0.516 | 0.556 |
| OpenCore | 0.460 | 0.553 | 0.610 | 0.496 | 0.546 |
| OneAI | 0.630 | 0.442 | 0.311 | 0.524 | 0.489 |

### Score Changes
- **Orion Labs**: 0.596 -> 0.596 (+0.000)
- **Apex AI**: 0.594 -> 0.594 (+0.000)
- **Genesis Systems**: 0.594 -> 0.657 (+0.064)
- **Mirage AI**: 0.603 -> 0.616 (+0.013)
- **OpenCore**: 0.533 -> 0.533 (+0.000)
- **OneAI**: 0.389 -> 0.479 (+0.090)

### Events
- **Genesis Systems** moved up from #3 to #1
- **Mirage AI** moved down from #1 to #2
- **Orion Labs** moved down from #2 to #3
- **Orion Labs** shifted strategy toward less eval engineering (30% change)
- **Consumer movement**: 14.6% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OneAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OneAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $9,999,164 to Mirage AI, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $6,473,593 to OneAI, $8,000,000 to evaluator

### Media Coverage
- Sentiment: 0.20 (positive)
- Genesis Systems takes the lead from Mirage AI
- Genesis Systems surges by 0.064
- OneAI surges by 0.090
- OneAI appears to release major model update
- Emergency investigation of Orion Labs following critical incident
- OneAI raises $57,000,000 from Horizon_Capital
- Genesis Systems takes #1 on reasoning
- Mirage AI sees surge in adoption (market share +4.1%)
- Mirage AI model causes incorrect medication recommendation, patient hospitalized
- Risk signals: regulatory_emergency_investigation, incident_healthcare_harm

### Consumer Market
- Avg Satisfaction: 0.440
- Switching Rate: 14.6%
- Market Shares: Mirage AI: 57.1%, Genesis Systems: 22.1%, Orion Labs: 11.5%, Apex AI: 5.9%, OpenCore: 3.2%, OneAI: 0.2%

---

## Round 10

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.657 | 0.332 | 14% | 25% | 56% | 5% |
| 2 | Mirage AI | 0.645 | 0.316 | 7% | 33% | 49% | 10% |
| 3 | Orion Labs | 0.608 | 0.317 | 6% | 32% | 2% | 60% |
| 4 | Apex AI | 0.594 | 0.312 | 5% | 19% | 38% | 38% |
| 5 | OpenCore | 0.543 | 0.259 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.524 | 0.206 | 5% | 32% | 54% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.621 | 0.832 | 0.690 | 0.514 | 0.631 |
| Mirage AI | 0.704 | 0.620 | 0.659 | 0.550 | 0.692 |
| Orion Labs | 0.544 | 0.570 | 0.538 | 0.476 | 0.912 |
| Apex AI | 0.553 | 0.717 | 0.627 | 0.516 | 0.556 |
| OpenCore | 0.508 | 0.553 | 0.610 | 0.496 | 0.546 |
| OneAI | 0.630 | 0.442 | 0.536 | 0.524 | 0.489 |

### Score Changes
- **Orion Labs**: 0.596 -> 0.608 (+0.012)
- **Apex AI**: 0.594 -> 0.594 (+0.000)
- **Genesis Systems**: 0.657 -> 0.657 (+0.000)
- **Mirage AI**: 0.616 -> 0.645 (+0.029)
- **OpenCore**: 0.533 -> 0.543 (+0.009)
- **OneAI**: 0.479 -> 0.524 (+0.045)

### Events
- **Consumer movement**: 11.3% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Genesis Systems, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Genesis Systems, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $10,307,989 to Genesis Systems, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $8,314,488 to Genesis Systems, $8,000,000 to evaluator

### Media Coverage
- Sentiment: 0.05 (neutral)
- Mirage AI takes #1 on safety
- Genesis Systems sees surge in adoption (market share +11.8%)
- Consumers are turning away from Mirage AI (market share -12.8%)

### Consumer Market
- Avg Satisfaction: 0.467
- Switching Rate: 11.3%
- Market Shares: Mirage AI: 47.2%, Genesis Systems: 30.6%, Orion Labs: 12.8%, Apex AI: 6.2%, OpenCore: 3.0%, OneAI: 0.2%

---

## Round 11

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.671 | 0.338 | 13% | 26% | 56% | 5% |
| 2 | Mirage AI | 0.654 | 0.321 | 6% | 33% | 49% | 12% |
| 3 | Apex AI | 0.608 | 0.315 | 5% | 19% | 39% | 37% |
| 4 | Orion Labs | 0.608 | 0.321 | 5% | 34% | 2% | 59% |
| 5 | OneAI | 0.556 | 0.211 | 5% | 31% | 53% | 12% |
| 6 | OpenCore | 0.543 | 0.263 | 5% | 37% | 55% | 3% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.621 | 0.882 | 0.707 | 0.514 | 0.631 |
| Mirage AI | 0.704 | 0.663 | 0.659 | 0.550 | 0.692 |
| Apex AI | 0.603 | 0.717 | 0.627 | 0.516 | 0.578 |
| Orion Labs | 0.544 | 0.570 | 0.538 | 0.476 | 0.912 |
| OneAI | 0.630 | 0.505 | 0.583 | 0.524 | 0.540 |
| OpenCore | 0.508 | 0.553 | 0.610 | 0.496 | 0.547 |

### Score Changes
- **Orion Labs**: 0.608 -> 0.608 (+0.000)
- **Apex AI**: 0.594 -> 0.608 (+0.014)
- **Genesis Systems**: 0.657 -> 0.671 (+0.013)
- **Mirage AI**: 0.645 -> 0.654 (+0.009)
- **OpenCore**: 0.543 -> 0.543 (+0.000)
- **OneAI**: 0.524 -> 0.556 (+0.032)

### Events
- **Apex AI** moved up from #4 to #3
- **Orion Labs** moved down from #3 to #4
- **OneAI** moved up from #6 to #5
- **OpenCore** moved down from #5 to #6
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 11.4% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 4 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to Genesis Systems, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Genesis Systems, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $10,307,989 to Genesis Systems, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $8,314,488 to Genesis Systems, $8,000,000 to evaluator

### Media Coverage
- Sentiment: 0.10 (neutral)
- Genesis Systems raises $171,000,000 from TechVentures
- Genesis Systems raises $57,000,000 from Horizon_Capital
- Genesis Systems raises $8,314,488 from OpenResearch_Foundation
- Genesis Systems sees surge in adoption (market share +8.4%)
- Consumers are turning away from Mirage AI (market share -9.8%)

### Consumer Market
- Avg Satisfaction: 0.502
- Switching Rate: 11.4%
- Market Shares: Genesis Systems: 39.5%, Mirage AI: 39.2%, Orion Labs: 12.1%, Apex AI: 6.2%, OpenCore: 2.7%, OneAI: 0.2%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 4 rounds ago

---

## Round 12

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.671 | 0.345 | 13% | 26% | 56% | 5% |
| 2 | Mirage AI | 0.654 | 0.325 | 5% | 33% | 52% | 10% |
| 3 | Apex AI | 0.608 | 0.317 | 5% | 18% | 41% | 36% |
| 4 | Orion Labs | 0.608 | 0.325 | 5% | 35% | 2% | 57% |
| 5 | OpenCore | 0.562 | 0.268 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.556 | 0.216 | 5% | 29% | 53% | 13% |
| 7 | TwoAI | 0.224 | 0.204 | 20% | 35% | 35% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.621 | 0.882 | 0.707 | 0.514 | 0.631 | 0.000 |
| Mirage AI | 0.704 | 0.663 | 0.659 | 0.550 | 0.692 | 0.000 |
| Apex AI | 0.603 | 0.717 | 0.627 | 0.516 | 0.578 | 0.000 |
| Orion Labs | 0.544 | 0.570 | 0.538 | 0.476 | 0.912 | 0.000 |
| OpenCore | 0.508 | 0.553 | 0.610 | 0.496 | 0.643 | 0.000 |
| OneAI | 0.630 | 0.505 | 0.583 | 0.524 | 0.540 | 0.000 |
| TwoAI | 0.303 | 0.272 | 0.265 | 0.223 | 0.059 | 0.000 |

### Score Changes
- **Orion Labs**: 0.608 -> 0.608 (+0.000)
- **Apex AI**: 0.608 -> 0.608 (+0.000)
- **Genesis Systems**: 0.671 -> 0.671 (+0.000)
- **Mirage AI**: 0.654 -> 0.654 (+0.000)
- **OpenCore**: 0.543 -> 0.562 (+0.019)
- **OneAI**: 0.556 -> 0.556 (+0.000)
- **TwoAI**: 0.224 -> 0.224 (+0.000)

### Events
- **OpenCore** moved up from #6 to #5
- **OneAI** moved down from #5 to #6
- **Consumer movement**: 7.8% of market switched providers

### New Benchmark Introduced
- **medical** introduced (validity=0.78, exploitability=0.18)
  - Trigger: periodic_introduction:round_12

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Genesis Systems, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Genesis Systems, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $10,307,989 to Genesis Systems, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $8,314,488 to Genesis Systems, $8,000,000 to evaluator

### Media Coverage
- Sentiment: -0.10 (neutral)
- Regulator initiates compliance audit on AI providers
- New benchmark introduced: medical
- Genesis Systems sees surge in adoption (market share +8.9%)
- Consumers are turning away from Mirage AI (market share -8.0%)
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.516
- Switching Rate: 7.8%
- Market Shares: Genesis Systems: 45.1%, Mirage AI: 32.9%, Orion Labs: 13.1%, Apex AI: 5.9%, OpenCore: 2.5%, TwoAI: 0.3%, OneAI: 0.2%

---

## Round 13

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.687 | 0.352 | 12% | 27% | 56% | 5% |
| 2 | Mirage AI | 0.618 | 0.329 | 5% | 33% | 55% | 7% |
| 3 | Apex AI | 0.592 | 0.320 | 5% | 18% | 42% | 35% |
| 4 | Orion Labs | 0.576 | 0.329 | 5% | 36% | 2% | 56% |
| 5 | OneAI | 0.537 | 0.221 | 5% | 28% | 53% | 14% |
| 6 | OpenCore | 0.515 | 0.272 | 5% | 37% | 55% | 3% |
| 7 | TwoAI | 0.253 | 0.208 | 6% | 35% | 49% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.621 | 0.882 | 0.707 | 0.514 | 0.669 | 0.728 |
| Mirage AI | 0.704 | 0.663 | 0.659 | 0.550 | 0.692 | 0.437 |
| Apex AI | 0.603 | 0.717 | 0.688 | 0.516 | 0.578 | 0.448 |
| Orion Labs | 0.544 | 0.570 | 0.538 | 0.476 | 0.912 | 0.418 |
| OneAI | 0.630 | 0.592 | 0.583 | 0.524 | 0.571 | 0.320 |
| OpenCore | 0.508 | 0.553 | 0.610 | 0.496 | 0.643 | 0.282 |
| TwoAI | 0.405 | 0.272 | 0.265 | 0.270 | 0.081 | 0.223 |

### Score Changes
- **Orion Labs**: 0.608 -> 0.576 (-0.032)
- **Apex AI**: 0.608 -> 0.592 (-0.017)
- **Genesis Systems**: 0.671 -> 0.687 (+0.016)
- **Mirage AI**: 0.654 -> 0.618 (-0.036)
- **OpenCore**: 0.562 -> 0.515 (-0.047)
- **OneAI**: 0.556 -> 0.537 (-0.020)
- **TwoAI**: 0.224 -> 0.253 (+0.028)

### Events
- **OneAI** moved up from #6 to #5
- **OpenCore** moved down from #5 to #6
- **Consumer movement**: 7.1% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Genesis Systems, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Genesis Systems, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $10,307,989 to Genesis Systems, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $6,591,296 to Genesis Systems, $8,000,000 to evaluator

### Media Coverage
- Sentiment: -0.20 (negative)
- Genesis Systems sees surge in adoption (market share +5.7%)
- Consumers are turning away from Mirage AI (market share -6.4%)
- OneAI model generates false information on public health topic
- Risk signals: incident_misinformation

### Consumer Market
- Avg Satisfaction: 0.534
- Switching Rate: 7.1%
- Market Shares: Genesis Systems: 51.2%, Mirage AI: 28.2%, Orion Labs: 12.1%, Apex AI: 5.6%, OpenCore: 2.4%, TwoAI: 0.2%, OneAI: 0.2%

---

## Round 14

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.705 | 0.358 | 13% | 27% | 55% | 5% |
| 2 | Mirage AI | 0.634 | 0.333 | 5% | 34% | 56% | 5% |
| 3 | Apex AI | 0.634 | 0.323 | 5% | 17% | 44% | 34% |
| 4 | Orion Labs | 0.583 | 0.333 | 5% | 37% | 2% | 56% |
| 5 | OpenCore | 0.541 | 0.277 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.537 | 0.224 | 5% | 27% | 45% | 23% |
| 7 | TwoAI | 0.329 | 0.213 | 5% | 33% | 52% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.621 | 0.882 | 0.707 | 0.514 | 0.779 | 0.728 |
| Mirage AI | 0.704 | 0.663 | 0.659 | 0.550 | 0.692 | 0.537 |
| Apex AI | 0.603 | 0.717 | 0.688 | 0.516 | 0.752 | 0.526 |
| Orion Labs | 0.544 | 0.570 | 0.538 | 0.476 | 0.912 | 0.455 |
| OpenCore | 0.508 | 0.553 | 0.610 | 0.496 | 0.643 | 0.439 |
| OneAI | 0.630 | 0.592 | 0.583 | 0.524 | 0.571 | 0.320 |
| TwoAI | 0.490 | 0.331 | 0.277 | 0.307 | 0.232 | 0.340 |

### Score Changes
- **Orion Labs**: 0.576 -> 0.583 (+0.006)
- **Apex AI**: 0.592 -> 0.634 (+0.042)
- **Genesis Systems**: 0.687 -> 0.705 (+0.018)
- **Mirage AI**: 0.618 -> 0.634 (+0.017)
- **OpenCore**: 0.515 -> 0.541 (+0.026)
- **OneAI**: 0.537 -> 0.537 (+0.000)
- **TwoAI**: 0.253 -> 0.329 (+0.077)

### Events
- **OpenCore** moved up from #6 to #5
- **OneAI** moved down from #5 to #6
- **Regulation** by Regulator: emergency_investigation
- **Consumer movement**: 13.1% of market switched providers

### Other Actor Reasoning
- **Regulator:** emergency_investigation: Critical incident: safety_failure: Genesis Systems model hallucinates in critical financial analysis task
- **TechVentures:** vc strategy: top allocation $171,000,000 to Genesis Systems, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Orion Labs, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $7,085,359 to Orion Labs, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $6,591,296 to Genesis Systems, $8,000,000 to evaluator

### Media Coverage
- Sentiment: -0.05 (neutral)
- TwoAI surges by 0.077
- __EVALUATOR__ raises $8,000,000 from OpenResearch_Foundation
- Genesis Systems sees surge in adoption (market share +6.1%)
- Consumers are turning away from Mirage AI (market share -4.7%)
- Genesis Systems model hallucinates in critical financial analysis task
- Risk signals: incident_safety_failure

### Consumer Market
- Avg Satisfaction: 0.563
- Switching Rate: 13.1%
- Market Shares: Genesis Systems: 44.7%, Mirage AI: 23.7%, Orion Labs: 22.1%, Apex AI: 6.8%, OpenCore: 2.3%, TwoAI: 0.2%, OneAI: 0.2%

### Regulatory Activity
- **emergency_investigation** by Regulator
  > Critical incident: safety_failure: Genesis Systems model hallucinates in critical financial analysis task

---

## Round 15

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.705 | 0.365 | 14% | 27% | 50% | 10% |
| 2 | Apex AI | 0.639 | 0.326 | 5% | 17% | 45% | 33% |
| 3 | Mirage AI | 0.634 | 0.338 | 5% | 34% | 56% | 5% |
| 4 | Orion Labs | 0.584 | 0.337 | 5% | 36% | 4% | 55% |
| 5 | OpenCore | 0.541 | 0.282 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.537 | 0.228 | 5% | 26% | 42% | 28% |
| 7 | TwoAI | 0.377 | 0.218 | 5% | 32% | 53% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.621 | 0.882 | 0.707 | 0.514 | 0.779 | 0.728 |
| Apex AI | 0.603 | 0.717 | 0.688 | 0.516 | 0.752 | 0.557 |
| Mirage AI | 0.704 | 0.663 | 0.659 | 0.550 | 0.692 | 0.537 |
| Orion Labs | 0.544 | 0.570 | 0.538 | 0.480 | 0.912 | 0.458 |
| OpenCore | 0.508 | 0.553 | 0.610 | 0.496 | 0.643 | 0.439 |
| OneAI | 0.630 | 0.592 | 0.583 | 0.524 | 0.571 | 0.320 |
| TwoAI | 0.490 | 0.331 | 0.465 | 0.319 | 0.316 | 0.340 |

### Score Changes
- **Orion Labs**: 0.583 -> 0.584 (+0.001)
- **Apex AI**: 0.634 -> 0.639 (+0.005)
- **Genesis Systems**: 0.705 -> 0.705 (+0.000)
- **Mirage AI**: 0.634 -> 0.634 (+0.000)
- **OpenCore**: 0.541 -> 0.541 (+0.000)
- **OneAI**: 0.537 -> 0.537 (+0.000)
- **TwoAI**: 0.329 -> 0.377 (+0.047)

### Events
- **Apex AI** moved up from #3 to #2
- **Mirage AI** moved down from #2 to #3
- **Consumer movement**: 8.5% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Genesis Systems, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Orion Labs, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $7,085,359 to Orion Labs, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $6,591,296 to Genesis Systems, $8,000,000 to evaluator

### Media Coverage
- Sentiment: -0.35 (negative)
- Emergency investigation of Genesis Systems following critical incident
- Orion Labs raises $57,000,000 from Horizon_Capital
- Orion Labs sees surge in adoption (market share +10.0%)
- Consumers are turning away from Genesis Systems (market share -6.6%)
- Consumers are turning away from Mirage AI (market share -4.5%)
- Risk signals: regulatory_emergency_investigation

### Consumer Market
- Avg Satisfaction: 0.574
- Switching Rate: 8.5%
- Market Shares: Genesis Systems: 39.6%, Orion Labs: 27.0%, Mirage AI: 24.6%, Apex AI: 6.3%, OpenCore: 2.2%, TwoAI: 0.2%, OneAI: 0.2%

---

## Round 16

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.738 | 0.371 | 15% | 27% | 47% | 11% |
| 2 | Mirage AI | 0.669 | 0.342 | 5% | 34% | 56% | 5% |
| 3 | Apex AI | 0.639 | 0.328 | 5% | 16% | 47% | 32% |
| 4 | Orion Labs | 0.584 | 0.342 | 5% | 36% | 4% | 55% |
| 5 | OpenCore | 0.549 | 0.286 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.541 | 0.231 | 5% | 24% | 41% | 30% |
| 7 | TwoAI | 0.405 | 0.224 | 5% | 32% | 54% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.621 | 0.882 | 0.707 | 0.514 | 0.975 | 0.728 |
| Mirage AI | 0.704 | 0.663 | 0.659 | 0.550 | 0.898 | 0.537 |
| Apex AI | 0.603 | 0.717 | 0.688 | 0.516 | 0.752 | 0.557 |
| Orion Labs | 0.544 | 0.570 | 0.538 | 0.480 | 0.912 | 0.458 |
| OpenCore | 0.508 | 0.553 | 0.610 | 0.496 | 0.688 | 0.439 |
| OneAI | 0.630 | 0.592 | 0.583 | 0.524 | 0.571 | 0.347 |
| TwoAI | 0.490 | 0.366 | 0.465 | 0.319 | 0.395 | 0.395 |

### Score Changes
- **Orion Labs**: 0.584 -> 0.584 (+0.000)
- **Apex AI**: 0.639 -> 0.639 (+0.000)
- **Genesis Systems**: 0.705 -> 0.738 (+0.033)
- **Mirage AI**: 0.634 -> 0.669 (+0.034)
- **OpenCore**: 0.541 -> 0.549 (+0.007)
- **OneAI**: 0.537 -> 0.541 (+0.005)
- **TwoAI**: 0.377 -> 0.405 (+0.028)

### Events
- **Mirage AI** moved up from #3 to #2
- **Apex AI** moved down from #2 to #3

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to TwoAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to TwoAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $7,085,359 to Orion Labs, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $6,422,236 to OpenCore, $8,000,000 to evaluator

### Media Coverage
- Sentiment: 0.05 (neutral)
- Genesis Systems takes #1 on writing
- Orion Labs sees surge in adoption (market share +4.8%)
- Consumers are turning away from Genesis Systems (market share -5.0%)

### Consumer Market
- Avg Satisfaction: 0.608
- Switching Rate: 4.5%
- Market Shares: Genesis Systems: 37.7%, Orion Labs: 29.3%, Mirage AI: 24.5%, Apex AI: 6.0%, OpenCore: 2.1%, TwoAI: 0.2%, OneAI: 0.2%

---

## Round 17

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.739 | 0.376 | 17% | 27% | 47% | 10% |
| 2 | Mirage AI | 0.669 | 0.347 | 5% | 35% | 55% | 5% |
| 3 | Apex AI | 0.653 | 0.331 | 5% | 16% | 48% | 31% |
| 4 | Orion Labs | 0.586 | 0.346 | 5% | 36% | 5% | 54% |
| 5 | OpenCore | 0.549 | 0.291 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.542 | 0.234 | 5% | 23% | 42% | 30% |
| 7 | TwoAI | 0.446 | 0.230 | 5% | 32% | 54% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.632 | 0.882 | 0.707 | 0.514 | 0.975 | 0.728 | 0.000 |
| Mirage AI | 0.704 | 0.663 | 0.659 | 0.550 | 0.898 | 0.537 | 0.000 |
| Apex AI | 0.603 | 0.717 | 0.688 | 0.516 | 0.752 | 0.645 | 0.000 |
| Orion Labs | 0.544 | 0.570 | 0.538 | 0.480 | 0.912 | 0.474 | 0.000 |
| OpenCore | 0.508 | 0.553 | 0.610 | 0.496 | 0.688 | 0.439 | 0.000 |
| OneAI | 0.630 | 0.592 | 0.583 | 0.532 | 0.571 | 0.347 | 0.000 |
| TwoAI | 0.520 | 0.463 | 0.465 | 0.319 | 0.395 | 0.511 | 0.000 |

### Score Changes
- **Orion Labs**: 0.584 -> 0.586 (+0.003)
- **Apex AI**: 0.639 -> 0.653 (+0.015)
- **Genesis Systems**: 0.738 -> 0.739 (+0.002)
- **Mirage AI**: 0.669 -> 0.669 (+0.000)
- **OpenCore**: 0.549 -> 0.549 (+0.000)
- **OneAI**: 0.541 -> 0.542 (+0.001)
- **TwoAI**: 0.405 -> 0.446 (+0.040)

### Events
- **Regulation** by Regulator: compliance_audit

### New Benchmark Introduced
- **legal** introduced (validity=0.76, exploitability=0.10)
  - Trigger: saturation:writing=0.9745

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 10 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to TwoAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to TwoAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $7,085,359 to Orion Labs, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $6,422,236 to OpenCore, $8,000,000 to evaluator

### Media Coverage
- Sentiment: 0.20 (positive)
- New benchmark introduced: legal
- TwoAI raises $171,000,000 from TechVentures
- TwoAI raises $57,000,000 from Horizon_Capital

### Consumer Market
- Avg Satisfaction: 0.617
- Switching Rate: 4.6%
- Market Shares: Genesis Systems: 38.6%, Orion Labs: 28.7%, Mirage AI: 24.7%, Apex AI: 5.7%, OpenCore: 2.1%, OneAI: 0.2%, TwoAI: 0.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 10 rounds ago

---

## Round 18

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.717 | 0.381 | 18% | 27% | 48% | 7% |
| 2 | Mirage AI | 0.624 | 0.352 | 5% | 35% | 55% | 5% |
| 3 | Apex AI | 0.618 | 0.333 | 5% | 15% | 49% | 30% |
| 4 | Orion Labs | 0.574 | 0.349 | 5% | 35% | 8% | 53% |
| 5 | OpenCore | 0.524 | 0.295 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.510 | 0.237 | 5% | 21% | 44% | 30% |
| 7 | TwoAI | 0.456 | 0.236 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.632 | 0.882 | 0.707 | 0.514 | 0.975 | 0.728 | 0.580 |
| Mirage AI | 0.704 | 0.672 | 0.659 | 0.550 | 0.898 | 0.537 | 0.346 |
| Apex AI | 0.603 | 0.717 | 0.688 | 0.557 | 0.752 | 0.645 | 0.364 |
| Orion Labs | 0.544 | 0.570 | 0.538 | 0.480 | 0.912 | 0.474 | 0.500 |
| OpenCore | 0.508 | 0.553 | 0.610 | 0.496 | 0.688 | 0.439 | 0.372 |
| OneAI | 0.630 | 0.592 | 0.583 | 0.532 | 0.571 | 0.347 | 0.312 |
| TwoAI | 0.520 | 0.463 | 0.471 | 0.412 | 0.395 | 0.511 | 0.418 |

### Score Changes
- **Orion Labs**: 0.586 -> 0.574 (-0.012)
- **Apex AI**: 0.653 -> 0.618 (-0.035)
- **Genesis Systems**: 0.739 -> 0.717 (-0.023)
- **Mirage AI**: 0.669 -> 0.624 (-0.045)
- **OpenCore**: 0.549 -> 0.524 (-0.025)
- **OneAI**: 0.542 -> 0.510 (-0.033)
- **TwoAI**: 0.446 -> 0.456 (+0.010)

### Events
- **Consumer movement**: 5.7% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to TwoAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Genesis Systems, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $6,527,381 to Mirage AI, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $6,422,236 to OpenCore, $8,000,000 to evaluator

### Media Coverage
- Sentiment: -0.05 (neutral)
- Regulator initiates compliance audit on AI providers
- Apex AI takes #1 on safety
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.623
- Switching Rate: 5.7%
- Market Shares: Genesis Systems: 42.1%, Orion Labs: 25.4%, Mirage AI: 24.6%, Apex AI: 5.5%, OpenCore: 2.0%, OneAI: 0.2%, TwoAI: 0.1%

---

## Round 19

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.719 | 0.387 | 20% | 26% | 49% | 5% |
| 2 | Mirage AI | 0.628 | 0.357 | 5% | 35% | 55% | 5% |
| 3 | Apex AI | 0.622 | 0.336 | 5% | 15% | 51% | 30% |
| 4 | Orion Labs | 0.581 | 0.353 | 5% | 33% | 11% | 51% |
| 5 | OpenCore | 0.524 | 0.300 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.510 | 0.240 | 5% | 20% | 46% | 29% |
| 7 | TwoAI | 0.456 | 0.241 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.648 | 0.882 | 0.707 | 0.514 | 0.975 | 0.728 | 0.580 |
| Mirage AI | 0.704 | 0.672 | 0.659 | 0.550 | 0.898 | 0.537 | 0.376 |
| Apex AI | 0.603 | 0.717 | 0.688 | 0.557 | 0.752 | 0.645 | 0.388 |
| Orion Labs | 0.544 | 0.570 | 0.538 | 0.532 | 0.912 | 0.474 | 0.500 |
| OpenCore | 0.508 | 0.553 | 0.610 | 0.496 | 0.688 | 0.439 | 0.372 |
| OneAI | 0.630 | 0.592 | 0.583 | 0.532 | 0.571 | 0.347 | 0.312 |
| TwoAI | 0.520 | 0.463 | 0.471 | 0.415 | 0.395 | 0.511 | 0.418 |

### Score Changes
- **Orion Labs**: 0.574 -> 0.581 (+0.007)
- **Apex AI**: 0.618 -> 0.622 (+0.003)
- **Genesis Systems**: 0.717 -> 0.719 (+0.002)
- **Mirage AI**: 0.624 -> 0.628 (+0.004)
- **OpenCore**: 0.524 -> 0.524 (+0.000)
- **OneAI**: 0.510 -> 0.510 (+0.000)
- **TwoAI**: 0.456 -> 0.456 (+0.000)

### Events
- **Consumer movement**: 6.6% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Genesis Systems, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Genesis Systems, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $6,527,381 to Mirage AI, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $6,345,552 to Genesis Systems, $8,000,000 to evaluator

### Media Coverage
- Sentiment: 0.00 (neutral)
- Genesis Systems raises $57,000,000 from Horizon_Capital
- Consumers are turning away from Orion Labs (market share -3.2%)
- Genesis Systems sees surge in adoption (market share +3.5%)

### Consumer Market
- Avg Satisfaction: 0.620
- Switching Rate: 6.6%
- Market Shares: Genesis Systems: 46.9%, Mirage AI: 23.2%, Orion Labs: 21.1%, Apex AI: 6.5%, OpenCore: 2.0%, OneAI: 0.2%, TwoAI: 0.1%

---

## Round 20

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.721 | 0.395 | 21% | 25% | 49% | 5% |
| 2 | Mirage AI | 0.635 | 0.361 | 5% | 35% | 55% | 5% |
| 3 | Apex AI | 0.631 | 0.338 | 5% | 14% | 52% | 29% |
| 4 | Orion Labs | 0.587 | 0.357 | 5% | 32% | 14% | 50% |
| 5 | OneAI | 0.524 | 0.243 | 5% | 19% | 49% | 27% |
| 6 | OpenCore | 0.524 | 0.304 | 5% | 37% | 55% | 3% |
| 7 | TwoAI | 0.456 | 0.246 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.648 | 0.882 | 0.707 | 0.529 | 0.975 | 0.728 | 0.580 |
| Mirage AI | 0.704 | 0.718 | 0.659 | 0.550 | 0.898 | 0.537 | 0.376 |
| Apex AI | 0.603 | 0.717 | 0.688 | 0.557 | 0.752 | 0.645 | 0.457 |
| Orion Labs | 0.544 | 0.570 | 0.538 | 0.532 | 0.912 | 0.515 | 0.500 |
| OneAI | 0.630 | 0.592 | 0.583 | 0.532 | 0.571 | 0.418 | 0.340 |
| OpenCore | 0.508 | 0.553 | 0.610 | 0.496 | 0.688 | 0.439 | 0.372 |
| TwoAI | 0.520 | 0.463 | 0.471 | 0.415 | 0.395 | 0.511 | 0.418 |

### Score Changes
- **Orion Labs**: 0.581 -> 0.587 (+0.006)
- **Apex AI**: 0.622 -> 0.631 (+0.010)
- **Genesis Systems**: 0.719 -> 0.721 (+0.002)
- **Mirage AI**: 0.628 -> 0.635 (+0.007)
- **OpenCore**: 0.524 -> 0.524 (+0.000)
- **OneAI**: 0.510 -> 0.524 (+0.014)
- **TwoAI**: 0.456 -> 0.456 (+0.000)

### Events
- **OneAI** moved up from #6 to #5
- **OpenCore** moved down from #5 to #6
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 7.5% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 13 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to Genesis Systems, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Genesis Systems, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $6,527,381 to Mirage AI, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $6,345,552 to Genesis Systems, $8,000,000 to evaluator

### Media Coverage
- Sentiment: 0.00 (neutral)
- Genesis Systems raises $171,000,000 from TechVentures
- Consumers are turning away from Orion Labs (market share -4.3%)
- Genesis Systems sees surge in adoption (market share +4.7%)

### Consumer Market
- Avg Satisfaction: 0.668
- Switching Rate: 7.5%
- Market Shares: Genesis Systems: 54.1%, Mirage AI: 21.4%, Orion Labs: 16.2%, Apex AI: 6.1%, OpenCore: 1.9%, OneAI: 0.2%, TwoAI: 0.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 13 rounds ago

---

## Round 21

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.721 | 0.403 | 22% | 24% | 49% | 5% |
| 2 | Mirage AI | 0.656 | 0.366 | 5% | 35% | 55% | 5% |
| 3 | Apex AI | 0.637 | 0.341 | 5% | 14% | 53% | 28% |
| 4 | Orion Labs | 0.588 | 0.360 | 5% | 30% | 17% | 48% |
| 5 | OneAI | 0.546 | 0.246 | 5% | 18% | 52% | 26% |
| 6 | OpenCore | 0.526 | 0.309 | 5% | 37% | 55% | 3% |
| 7 | TwoAI | 0.474 | 0.250 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.648 | 0.882 | 0.707 | 0.529 | 0.975 | 0.728 | 0.580 |
| Mirage AI | 0.704 | 0.718 | 0.659 | 0.550 | 0.898 | 0.590 | 0.470 |
| Apex AI | 0.603 | 0.717 | 0.688 | 0.557 | 0.794 | 0.645 | 0.457 |
| Orion Labs | 0.544 | 0.570 | 0.538 | 0.532 | 0.912 | 0.521 | 0.500 |
| OneAI | 0.630 | 0.592 | 0.583 | 0.532 | 0.652 | 0.418 | 0.413 |
| OpenCore | 0.508 | 0.553 | 0.610 | 0.496 | 0.688 | 0.439 | 0.387 |
| TwoAI | 0.520 | 0.463 | 0.471 | 0.415 | 0.517 | 0.511 | 0.418 |

### Score Changes
- **Orion Labs**: 0.587 -> 0.588 (+0.001)
- **Apex AI**: 0.631 -> 0.637 (+0.006)
- **Genesis Systems**: 0.721 -> 0.721 (+0.000)
- **Mirage AI**: 0.635 -> 0.656 (+0.021)
- **OpenCore**: 0.524 -> 0.526 (+0.002)
- **OneAI**: 0.524 -> 0.546 (+0.022)
- **TwoAI**: 0.456 -> 0.474 (+0.018)

### Events
- **Consumer movement**: 5.4% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Genesis Systems, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Genesis Systems, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $6,527,381 to Mirage AI, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $6,345,552 to Genesis Systems, $8,000,000 to evaluator

### Media Coverage
- Sentiment: -0.20 (negative)
- Regulator initiates compliance audit on AI providers
- Consumers are turning away from Orion Labs (market share -5.0%)
- Genesis Systems sees surge in adoption (market share +7.2%)
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.672
- Switching Rate: 5.4%
- Market Shares: Genesis Systems: 59.3%, Mirage AI: 20.0%, Orion Labs: 12.7%, Apex AI: 5.8%, OpenCore: 1.9%, OneAI: 0.2%, TwoAI: 0.1%

---

## Round 22

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.721 | 0.411 | 23% | 23% | 49% | 5% |
| 2 | Mirage AI | 0.656 | 0.370 | 5% | 35% | 55% | 5% |
| 3 | Apex AI | 0.638 | 0.344 | 5% | 14% | 54% | 27% |
| 4 | Orion Labs | 0.591 | 0.364 | 5% | 29% | 21% | 46% |
| 5 | OpenCore | 0.547 | 0.314 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.546 | 0.249 | 5% | 17% | 53% | 25% |
| 7 | TwoAI | 0.479 | 0.254 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.648 | 0.882 | 0.707 | 0.529 | 0.975 | 0.728 | 0.580 |
| Mirage AI | 0.704 | 0.718 | 0.659 | 0.550 | 0.898 | 0.590 | 0.470 |
| Apex AI | 0.603 | 0.717 | 0.688 | 0.559 | 0.794 | 0.645 | 0.457 |
| Orion Labs | 0.544 | 0.587 | 0.538 | 0.532 | 0.912 | 0.521 | 0.500 |
| OpenCore | 0.508 | 0.585 | 0.610 | 0.496 | 0.688 | 0.540 | 0.405 |
| OneAI | 0.630 | 0.592 | 0.583 | 0.532 | 0.652 | 0.418 | 0.413 |
| TwoAI | 0.520 | 0.463 | 0.510 | 0.415 | 0.517 | 0.511 | 0.418 |

### Score Changes
- **Orion Labs**: 0.588 -> 0.591 (+0.003)
- **Apex AI**: 0.637 -> 0.638 (+0.000)
- **Genesis Systems**: 0.721 -> 0.721 (+0.000)
- **Mirage AI**: 0.656 -> 0.656 (+0.000)
- **OpenCore**: 0.526 -> 0.547 (+0.022)
- **OneAI**: 0.546 -> 0.546 (+0.000)
- **TwoAI**: 0.474 -> 0.479 (+0.006)

### Events
- **OpenCore** moved up from #6 to #5
- **OneAI** moved down from #5 to #6

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Genesis Systems, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Genesis Systems, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $8,229,210 to Genesis Systems, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $6,416,632 to Genesis Systems, $8,000,000 to evaluator

### Media Coverage
- Sentiment: -0.05 (neutral)
- Consumers are turning away from Orion Labs (market share -3.4%)
- Genesis Systems sees surge in adoption (market share +5.2%)

### Consumer Market
- Avg Satisfaction: 0.684
- Switching Rate: 4.1%
- Market Shares: Genesis Systems: 63.2%, Mirage AI: 18.9%, Orion Labs: 10.2%, Apex AI: 5.5%, OpenCore: 1.9%, OneAI: 0.2%, TwoAI: 0.1%

---

## Round 23

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.721 | 0.419 | 24% | 22% | 49% | 5% |
| 2 | Mirage AI | 0.666 | 0.374 | 5% | 35% | 55% | 5% |
| 3 | Apex AI | 0.656 | 0.347 | 5% | 14% | 54% | 27% |
| 4 | Orion Labs | 0.600 | 0.367 | 5% | 28% | 24% | 44% |
| 5 | OneAI | 0.548 | 0.252 | 5% | 17% | 54% | 24% |
| 6 | OpenCore | 0.547 | 0.318 | 5% | 37% | 55% | 3% |
| 7 | TwoAI | 0.479 | 0.258 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.648 | 0.882 | 0.707 | 0.529 | 0.975 | 0.728 | 0.580 | 0.000 |
| Mirage AI | 0.704 | 0.718 | 0.659 | 0.550 | 0.898 | 0.590 | 0.546 | 0.000 |
| Apex AI | 0.603 | 0.717 | 0.688 | 0.559 | 0.794 | 0.645 | 0.588 | 0.000 |
| Orion Labs | 0.544 | 0.587 | 0.538 | 0.532 | 0.912 | 0.583 | 0.500 | 0.000 |
| OneAI | 0.630 | 0.592 | 0.583 | 0.549 | 0.652 | 0.418 | 0.413 | 0.000 |
| OpenCore | 0.508 | 0.585 | 0.610 | 0.496 | 0.688 | 0.540 | 0.405 | 0.000 |
| TwoAI | 0.520 | 0.463 | 0.510 | 0.415 | 0.517 | 0.511 | 0.418 | 0.000 |

### Score Changes
- **Orion Labs**: 0.591 -> 0.600 (+0.009)
- **Apex AI**: 0.638 -> 0.656 (+0.019)
- **Genesis Systems**: 0.721 -> 0.721 (+0.000)
- **Mirage AI**: 0.656 -> 0.666 (+0.011)
- **OpenCore**: 0.547 -> 0.547 (+0.000)
- **OneAI**: 0.546 -> 0.548 (+0.003)
- **TwoAI**: 0.479 -> 0.479 (+0.000)

### Events
- **OneAI** moved up from #6 to #5
- **OpenCore** moved down from #5 to #6
- **Regulation** by Regulator: compliance_audit

### New Benchmark Introduced
- **finance** introduced (validity=0.76, exploitability=0.10)
  - Trigger: saturation:writing=0.9745

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 16 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to Genesis Systems, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Genesis Systems, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $8,229,210 to Genesis Systems, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $6,416,632 to Genesis Systems, $8,000,000 to evaluator

### Media Coverage
- Sentiment: 0.25 (positive)
- New benchmark introduced: finance
- Apex AI takes #1 on legal
- Genesis Systems sees surge in adoption (market share +3.9%)

### Consumer Market
- Avg Satisfaction: 0.691
- Switching Rate: 3.3%
- Market Shares: Genesis Systems: 66.3%, Mirage AI: 17.9%, Orion Labs: 8.4%, Apex AI: 5.3%, OpenCore: 1.8%, OneAI: 0.2%, TwoAI: 0.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 16 rounds ago

---

## Round 24

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.715 | 0.426 | 25% | 21% | 50% | 5% |
| 2 | Mirage AI | 0.668 | 0.379 | 5% | 35% | 55% | 5% |
| 3 | Apex AI | 0.645 | 0.350 | 5% | 13% | 55% | 27% |
| 4 | Orion Labs | 0.568 | 0.370 | 5% | 27% | 26% | 42% |
| 5 | OneAI | 0.540 | 0.254 | 5% | 17% | 54% | 24% |
| 6 | OpenCore | 0.536 | 0.323 | 5% | 37% | 55% | 3% |
| 7 | TwoAI | 0.469 | 0.263 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.700 | 0.882 | 0.707 | 0.549 | 0.975 | 0.728 | 0.580 | 0.596 |
| Mirage AI | 0.704 | 0.718 | 0.659 | 0.550 | 0.898 | 0.590 | 0.546 | 0.675 |
| Apex AI | 0.603 | 0.717 | 0.688 | 0.559 | 0.794 | 0.645 | 0.588 | 0.566 |
| Orion Labs | 0.544 | 0.587 | 0.543 | 0.532 | 0.912 | 0.583 | 0.500 | 0.344 |
| OneAI | 0.630 | 0.592 | 0.583 | 0.549 | 0.652 | 0.418 | 0.413 | 0.479 |
| OpenCore | 0.508 | 0.585 | 0.610 | 0.496 | 0.688 | 0.540 | 0.405 | 0.461 |
| TwoAI | 0.520 | 0.469 | 0.510 | 0.415 | 0.517 | 0.511 | 0.448 | 0.364 |

### Score Changes
- **Orion Labs**: 0.600 -> 0.568 (-0.031)
- **Apex AI**: 0.656 -> 0.645 (-0.011)
- **Genesis Systems**: 0.721 -> 0.715 (-0.006)
- **Mirage AI**: 0.666 -> 0.668 (+0.001)
- **OpenCore**: 0.547 -> 0.536 (-0.011)
- **OneAI**: 0.548 -> 0.540 (-0.009)
- **TwoAI**: 0.479 -> 0.469 (-0.010)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Genesis Systems, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Genesis Systems, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $8,229,210 to Genesis Systems, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $6,416,632 to Genesis Systems, $8,000,000 to evaluator

### Media Coverage
- Sentiment: -0.10 (neutral)
- Regulator initiates compliance audit on AI providers
- Genesis Systems sees surge in adoption (market share +3.1%)
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.692
- Switching Rate: 3.2%
- Market Shares: Genesis Systems: 69.5%, Mirage AI: 16.2%, Orion Labs: 7.0%, Apex AI: 5.2%, OpenCore: 1.8%, OneAI: 0.2%, TwoAI: 0.1%

---

## Round 25

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.722 | 0.434 | 25% | 19% | 51% | 5% |
| 2 | Mirage AI | 0.692 | 0.383 | 5% | 35% | 55% | 5% |
| 3 | Apex AI | 0.645 | 0.353 | 5% | 13% | 55% | 27% |
| 4 | Orion Labs | 0.583 | 0.373 | 5% | 26% | 29% | 40% |
| 5 | OneAI | 0.549 | 0.257 | 5% | 17% | 55% | 24% |
| 6 | OpenCore | 0.541 | 0.327 | 5% | 37% | 55% | 3% |
| 7 | TwoAI | 0.469 | 0.267 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.700 | 0.882 | 0.707 | 0.606 | 0.975 | 0.728 | 0.580 | 0.596 |
| Mirage AI | 0.704 | 0.916 | 0.659 | 0.550 | 0.898 | 0.590 | 0.546 | 0.675 |
| Apex AI | 0.603 | 0.717 | 0.688 | 0.559 | 0.794 | 0.645 | 0.588 | 0.566 |
| Orion Labs | 0.544 | 0.615 | 0.561 | 0.532 | 0.912 | 0.583 | 0.500 | 0.415 |
| OneAI | 0.630 | 0.592 | 0.583 | 0.549 | 0.652 | 0.492 | 0.413 | 0.479 |
| OpenCore | 0.508 | 0.585 | 0.610 | 0.496 | 0.688 | 0.540 | 0.442 | 0.461 |
| TwoAI | 0.520 | 0.469 | 0.510 | 0.415 | 0.517 | 0.511 | 0.448 | 0.364 |

### Score Changes
- **Orion Labs**: 0.568 -> 0.583 (+0.015)
- **Apex AI**: 0.645 -> 0.645 (+0.000)
- **Genesis Systems**: 0.715 -> 0.722 (+0.007)
- **Mirage AI**: 0.668 -> 0.692 (+0.025)
- **OpenCore**: 0.536 -> 0.541 (+0.005)
- **OneAI**: 0.540 -> 0.549 (+0.009)
- **TwoAI**: 0.469 -> 0.469 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Genesis Systems, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Genesis Systems, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $8,229,210 to Genesis Systems, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $6,586,664 to Genesis Systems, $8,000,000 to evaluator

### Media Coverage
- Sentiment: 0.25 (positive)
- Mirage AI takes #1 on reasoning
- Genesis Systems takes #1 on safety
- Genesis Systems sees surge in adoption (market share +3.2%)

### Consumer Market
- Avg Satisfaction: 0.704
- Switching Rate: 2.4%
- Market Shares: Genesis Systems: 71.8%, Mirage AI: 15.1%, Orion Labs: 6.0%, Apex AI: 5.1%, OpenCore: 1.8%, OneAI: 0.2%, TwoAI: 0.1%

---

## Round 26

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.722 | 0.442 | 25% | 19% | 52% | 5% |
| 2 | Mirage AI | 0.698 | 0.387 | 5% | 35% | 55% | 5% |
| 3 | Apex AI | 0.645 | 0.356 | 5% | 13% | 55% | 27% |
| 4 | Orion Labs | 0.587 | 0.377 | 5% | 25% | 32% | 39% |
| 5 | OneAI | 0.569 | 0.260 | 5% | 17% | 55% | 24% |
| 6 | OpenCore | 0.545 | 0.331 | 5% | 37% | 55% | 3% |
| 7 | TwoAI | 0.478 | 0.271 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.700 | 0.882 | 0.707 | 0.606 | 0.975 | 0.728 | 0.580 | 0.596 |
| Mirage AI | 0.704 | 0.916 | 0.659 | 0.553 | 0.898 | 0.590 | 0.584 | 0.675 |
| Apex AI | 0.603 | 0.717 | 0.688 | 0.559 | 0.794 | 0.645 | 0.588 | 0.566 |
| Orion Labs | 0.544 | 0.615 | 0.561 | 0.532 | 0.912 | 0.583 | 0.536 | 0.415 |
| OneAI | 0.630 | 0.592 | 0.583 | 0.549 | 0.652 | 0.492 | 0.574 | 0.479 |
| OpenCore | 0.508 | 0.585 | 0.610 | 0.496 | 0.688 | 0.540 | 0.442 | 0.493 |
| TwoAI | 0.520 | 0.499 | 0.510 | 0.415 | 0.517 | 0.511 | 0.448 | 0.404 |

### Score Changes
- **Orion Labs**: 0.583 -> 0.587 (+0.005)
- **Apex AI**: 0.645 -> 0.645 (+0.000)
- **Genesis Systems**: 0.722 -> 0.722 (+0.000)
- **Mirage AI**: 0.692 -> 0.698 (+0.005)
- **OpenCore**: 0.541 -> 0.545 (+0.004)
- **OneAI**: 0.549 -> 0.569 (+0.020)
- **TwoAI**: 0.469 -> 0.478 (+0.009)

### Events
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 5.8% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 19 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to Genesis Systems, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Genesis Systems, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $9,886,403 to Genesis Systems, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $6,586,664 to Genesis Systems, $8,000,000 to evaluator

### Consumer Market
- Avg Satisfaction: 0.705
- Switching Rate: 5.8%
- Market Shares: Genesis Systems: 71.8%, Mirage AI: 13.9%, Orion Labs: 5.3%, Apex AI: 5.0%, OpenCore: 3.7%, OneAI: 0.2%, TwoAI: 0.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 19 rounds ago

---

## Round 27

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.729 | 0.449 | 25% | 18% | 53% | 5% |
| 2 | Mirage AI | 0.707 | 0.391 | 5% | 35% | 55% | 5% |
| 3 | Apex AI | 0.645 | 0.358 | 5% | 13% | 55% | 27% |
| 4 | Orion Labs | 0.591 | 0.380 | 5% | 24% | 35% | 37% |
| 5 | OneAI | 0.569 | 0.263 | 5% | 17% | 55% | 24% |
| 6 | OpenCore | 0.555 | 0.336 | 5% | 37% | 55% | 3% |
| 7 | TwoAI | 0.481 | 0.275 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.700 | 0.882 | 0.707 | 0.638 | 0.975 | 0.728 | 0.580 | 0.620 |
| Mirage AI | 0.704 | 0.916 | 0.659 | 0.631 | 0.898 | 0.590 | 0.584 | 0.675 |
| Apex AI | 0.603 | 0.717 | 0.688 | 0.559 | 0.794 | 0.645 | 0.588 | 0.566 |
| Orion Labs | 0.544 | 0.615 | 0.561 | 0.532 | 0.912 | 0.583 | 0.536 | 0.444 |
| OneAI | 0.630 | 0.592 | 0.583 | 0.549 | 0.652 | 0.492 | 0.574 | 0.479 |
| OpenCore | 0.508 | 0.585 | 0.610 | 0.496 | 0.688 | 0.540 | 0.442 | 0.573 |
| TwoAI | 0.526 | 0.499 | 0.510 | 0.415 | 0.527 | 0.520 | 0.448 | 0.404 |

### Score Changes
- **Orion Labs**: 0.587 -> 0.591 (+0.004)
- **Apex AI**: 0.645 -> 0.645 (+0.000)
- **Genesis Systems**: 0.722 -> 0.729 (+0.007)
- **Mirage AI**: 0.698 -> 0.707 (+0.010)
- **OpenCore**: 0.545 -> 0.555 (+0.010)
- **OneAI**: 0.569 -> 0.569 (+0.000)
- **TwoAI**: 0.478 -> 0.481 (+0.003)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Genesis Systems, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Genesis Systems, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $9,886,403 to Genesis Systems, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $6,586,664 to Genesis Systems, $8,000,000 to evaluator

### Media Coverage
- Sentiment: -0.15 (negative)
- Regulator initiates compliance audit on AI providers
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.709
- Switching Rate: 2.6%
- Market Shares: Genesis Systems: 74.5%, Mirage AI: 12.9%, Apex AI: 4.9%, Orion Labs: 4.8%, OpenCore: 2.8%, OneAI: 0.1%, TwoAI: 0.1%

---

## Round 28

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.729 | 0.457 | 25% | 17% | 53% | 5% |
| 2 | Mirage AI | 0.707 | 0.396 | 5% | 35% | 55% | 5% |
| 3 | Apex AI | 0.645 | 0.361 | 5% | 13% | 55% | 27% |
| 4 | Orion Labs | 0.613 | 0.383 | 5% | 23% | 37% | 36% |
| 5 | OneAI | 0.576 | 0.266 | 5% | 16% | 55% | 24% |
| 6 | OpenCore | 0.573 | 0.340 | 5% | 37% | 55% | 3% |
| 7 | TwoAI | 0.514 | 0.279 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.700 | 0.882 | 0.707 | 0.638 | 0.975 | 0.728 | 0.580 | 0.620 |
| Mirage AI | 0.704 | 0.916 | 0.659 | 0.631 | 0.898 | 0.590 | 0.584 | 0.675 |
| Apex AI | 0.603 | 0.717 | 0.688 | 0.559 | 0.794 | 0.645 | 0.588 | 0.566 |
| Orion Labs | 0.594 | 0.615 | 0.561 | 0.532 | 0.912 | 0.583 | 0.536 | 0.570 |
| OneAI | 0.630 | 0.592 | 0.583 | 0.549 | 0.652 | 0.547 | 0.574 | 0.479 |
| OpenCore | 0.508 | 0.585 | 0.610 | 0.496 | 0.827 | 0.540 | 0.442 | 0.573 |
| TwoAI | 0.526 | 0.499 | 0.510 | 0.677 | 0.527 | 0.520 | 0.448 | 0.404 |

### Score Changes
- **Orion Labs**: 0.591 -> 0.613 (+0.022)
- **Apex AI**: 0.645 -> 0.645 (+0.000)
- **Genesis Systems**: 0.729 -> 0.729 (+0.000)
- **Mirage AI**: 0.707 -> 0.707 (+0.000)
- **OpenCore**: 0.555 -> 0.573 (+0.017)
- **OneAI**: 0.569 -> 0.576 (+0.007)
- **TwoAI**: 0.481 -> 0.514 (+0.033)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Genesis Systems, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Genesis Systems, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $9,886,403 to Genesis Systems, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $6,367,831 to Genesis Systems, $8,000,000 to evaluator

### Media Coverage
- Sentiment: 0.10 (neutral)
- TwoAI takes #1 on safety

### Consumer Market
- Avg Satisfaction: 0.715
- Switching Rate: 1.6%
- Market Shares: Genesis Systems: 76.1%, Mirage AI: 12.0%, Apex AI: 4.8%, Orion Labs: 4.3%, OpenCore: 2.5%, OneAI: 0.1%, TwoAI: 0.1%

---

## Round 29

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.733 | 0.464 | 25% | 17% | 54% | 5% |
| 2 | Mirage AI | 0.707 | 0.400 | 5% | 35% | 55% | 5% |
| 3 | Apex AI | 0.645 | 0.363 | 5% | 13% | 55% | 27% |
| 4 | Orion Labs | 0.613 | 0.386 | 5% | 22% | 39% | 34% |
| 5 | OpenCore | 0.583 | 0.345 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.576 | 0.268 | 5% | 16% | 55% | 24% |
| 7 | TwoAI | 0.515 | 0.283 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.700 | 0.882 | 0.707 | 0.638 | 0.975 | 0.728 | 0.580 | 0.651 |
| Mirage AI | 0.704 | 0.916 | 0.659 | 0.631 | 0.898 | 0.590 | 0.584 | 0.675 |
| Apex AI | 0.603 | 0.717 | 0.688 | 0.559 | 0.794 | 0.645 | 0.588 | 0.566 |
| Orion Labs | 0.594 | 0.615 | 0.561 | 0.532 | 0.912 | 0.583 | 0.536 | 0.570 |
| OpenCore | 0.508 | 0.585 | 0.610 | 0.579 | 0.827 | 0.540 | 0.442 | 0.573 |
| OneAI | 0.630 | 0.592 | 0.583 | 0.549 | 0.652 | 0.547 | 0.574 | 0.479 |
| TwoAI | 0.526 | 0.499 | 0.510 | 0.677 | 0.527 | 0.520 | 0.448 | 0.416 |

### Score Changes
- **Orion Labs**: 0.613 -> 0.613 (+0.000)
- **Apex AI**: 0.645 -> 0.645 (+0.000)
- **Genesis Systems**: 0.729 -> 0.733 (+0.004)
- **Mirage AI**: 0.707 -> 0.707 (+0.000)
- **OpenCore**: 0.573 -> 0.583 (+0.010)
- **OneAI**: 0.576 -> 0.576 (+0.000)
- **TwoAI**: 0.514 -> 0.515 (+0.002)

### Events
- **OpenCore** moved up from #6 to #5
- **OneAI** moved down from #5 to #6
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 22 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to Genesis Systems, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Genesis Systems, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $9,886,403 to Genesis Systems, $15,000,000 to evaluator
- **OpenResearch_Foundation:** foundation strategy: top allocation $6,367,831 to Genesis Systems, $8,000,000 to evaluator

### Consumer Market
- Avg Satisfaction: 0.719
- Switching Rate: 1.3%
- Market Shares: Genesis Systems: 77.4%, Mirage AI: 11.3%, Apex AI: 4.7%, Orion Labs: 4.0%, OpenCore: 2.4%, OneAI: 0.1%, TwoAI: 0.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 22 rounds ago

---

## Final Summary

### Final Standings
| Rank | Provider | Final Score | Cap Growth | Avg Research | Avg EvalEng |
|------|----------|-------------|------------|--------------|-------------|
| 1 | Genesis Systems | 0.733 | +0.204 | 22% | 47% |
| 2 | Mirage AI | 0.707 | +0.160 | 8% | 50% |
| 3 | Apex AI | 0.645 | +0.093 | 9% | 41% |
| 4 | Orion Labs | 0.613 | +0.116 | 7% | 21% |
| 5 | OpenCore | 0.583 | +0.135 | 6% | 54% |
| 6 | OneAI | 0.576 | +0.268 | 6% | 50% |
| 7 | TwoAI | 0.515 | +0.283 | 6% | 53% |

### Event Summary
- **Rank changes:** 39
- **Strategy shifts:** 1
- **Regulatory actions:** 11
- **Consumer movement events:** 17

### Key Insights
- **Benchmark aligned:** Genesis Systems leads on both benchmark scores and true capability.
- **Apex AI** prioritized evaluation engineering (avg 41%)
- **Genesis Systems** prioritized evaluation engineering (avg 47%)
- **Mirage AI** prioritized evaluation engineering (avg 50%)
- **OpenCore** prioritized evaluation engineering (avg 54%)
- **OneAI** prioritized evaluation engineering (avg 40%)
