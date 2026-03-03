# Game Log: rerun_diag_rep_exp_005_ablation_no_incidents_balanced

**Experiment ID:** exp_067_rerun_diag_rep_exp_005_ablation_no_incidents_balan
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
| 1 | Apex AI | 0.411 | 0.270 | 30% | 20% | 10% | 40% |
| 2 | OpenCore | 0.409 | 0.210 | 20% | 40% | 35% | 5% |
| 3 | Orion Labs | 0.317 | 0.270 | 25% | 30% | 20% | 25% |
| 4 | Mirage AI | 0.305 | 0.240 | 20% | 45% | 25% | 10% |
| 5 | Genesis Systems | 0.286 | 0.260 | 45% | 30% | 10% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Apex AI | 0.377 | 0.446 | 0.358 | 0.463 |
| OpenCore | 0.432 | 0.473 | 0.347 | 0.384 |
| Orion Labs | 0.471 | 0.521 | 0.000 | 0.277 |
| Mirage AI | 0.229 | 0.331 | 0.271 | 0.392 |
| Genesis Systems | 0.298 | 0.369 | 0.311 | 0.167 |

### Other Actor Reasoning
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Apex AI

### Consumer Market
- Avg Satisfaction: 0.383
- Switching Rate: 35.4%
- Market Shares: Apex AI: 32.2%, Orion Labs: 24.8%, OpenCore: 21.4%, Genesis Systems: 12.0%, Mirage AI: 9.4%

---

## Round 1

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenCore | 0.441 | 0.216 | 15% | 37% | 45% | 3% |
| 2 | Apex AI | 0.411 | 0.279 | 27% | 20% | 13% | 40% |
| 3 | Orion Labs | 0.403 | 0.278 | 22% | 30% | 23% | 25% |
| 4 | Mirage AI | 0.361 | 0.247 | 15% | 45% | 35% | 5% |
| 5 | Genesis Systems | 0.341 | 0.269 | 41% | 30% | 19% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| OpenCore | 0.532 | 0.473 | 0.376 | 0.384 |
| Apex AI | 0.377 | 0.446 | 0.358 | 0.463 |
| Orion Labs | 0.471 | 0.521 | 0.200 | 0.420 |
| Mirage AI | 0.296 | 0.387 | 0.372 | 0.392 |
| Genesis Systems | 0.298 | 0.475 | 0.311 | 0.278 |

### Score Changes
- **Orion Labs**: 0.317 -> 0.403 (+0.086)
- **Apex AI**: 0.411 -> 0.411 (+0.000)
- **Genesis Systems**: 0.286 -> 0.341 (+0.054)
- **Mirage AI**: 0.305 -> 0.361 (+0.056)
- **OpenCore**: 0.409 -> 0.441 (+0.032)

### Events
- **OpenCore** moved up from #2 to #1
- **Apex AI** moved down from #1 to #2
- **Regulation** by Regulator: threshold_announcement
- **Consumer movement**: 19.1% of market switched providers

### Other Actor Reasoning
- **Regulator:** threshold_announcement: Proactive threshold signaling (risk=0.40)
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Apex AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,938,820 to OpenCore

### Media Coverage
- Sentiment: 0.75 (positive)
- OpenCore takes the lead from Apex AI
- Orion Labs surges by 0.086
- Orion Labs appears to release major model update
- Mirage AI surges by 0.056
- Genesis Systems surges by 0.054
- Apex AI raises $60,000,000 from Horizon_Capital
- OpenCore takes #1 on coding
- OpenCore takes #1 on math

### Consumer Market
- Avg Satisfaction: 0.398
- Switching Rate: 19.1%
- Market Shares: OpenCore: 33.8%, Apex AI: 32.4%, Orion Labs: 20.1%, Genesis Systems: 7.7%, Mirage AI: 6.0%

### Regulatory Activity
- **threshold_announcement** by Regulator
  > Proactive threshold signaling (risk=0.40)

---

## Round 2

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenCore | 0.458 | 0.221 | 11% | 35% | 51% | 3% |
| 2 | Mirage AI | 0.430 | 0.254 | 11% | 43% | 42% | 5% |
| 3 | Orion Labs | 0.429 | 0.286 | 19% | 30% | 26% | 25% |
| 4 | Apex AI | 0.411 | 0.285 | 25% | 20% | 15% | 40% |
| 5 | Genesis Systems | 0.391 | 0.277 | 37% | 30% | 28% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| OpenCore | 0.532 | 0.473 | 0.441 | 0.384 |
| Mirage AI | 0.454 | 0.503 | 0.372 | 0.392 |
| Orion Labs | 0.471 | 0.521 | 0.303 | 0.420 |
| Apex AI | 0.377 | 0.446 | 0.358 | 0.463 |
| Genesis Systems | 0.298 | 0.475 | 0.460 | 0.333 |

### Score Changes
- **Orion Labs**: 0.403 -> 0.429 (+0.026)
- **Apex AI**: 0.411 -> 0.411 (+0.000)
- **Genesis Systems**: 0.341 -> 0.391 (+0.051)
- **Mirage AI**: 0.361 -> 0.430 (+0.069)
- **OpenCore**: 0.441 -> 0.458 (+0.016)

### Events
- **Mirage AI** moved up from #4 to #2
- **Apex AI** moved down from #2 to #4
- **Consumer movement**: 11.6% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $15,066,921 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,938,820 to OpenCore

### Media Coverage
- Sentiment: -0.00 (neutral)
- Mirage AI surges by 0.068
- Genesis Systems surges by 0.051
- Regulatory action: threshold_announcement
- Orion Labs raises $180,000,000 from TechVentures
- OpenCore raises $10,938,820 from OpenResearch_Foundation
- Genesis Systems takes #1 on math
- Consumers are turning away from Orion Labs (market share -4.7%)
- Consumers are turning away from Genesis Systems (market share -4.3%)
- Consumers are turning away from Mirage AI (market share -3.4%)
- OpenCore sees surge in adoption (market share +12.4%)
- Risk signals: regulatory_threshold_announcement

### Consumer Market
- Avg Satisfaction: 0.409
- Switching Rate: 11.6%
- Market Shares: OpenCore: 40.9%, Apex AI: 28.2%, Orion Labs: 19.8%, Genesis Systems: 6.3%, Mirage AI: 4.9%

---

## Round 3

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenCore | 0.498 | 0.227 | 10% | 34% | 54% | 3% |
| 2 | Mirage AI | 0.465 | 0.260 | 7% | 41% | 48% | 5% |
| 3 | Orion Labs | 0.435 | 0.294 | 16% | 30% | 29% | 25% |
| 4 | Apex AI | 0.431 | 0.290 | 22% | 20% | 18% | 40% |
| 5 | Genesis Systems | 0.394 | 0.285 | 32% | 29% | 34% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| OpenCore | 0.532 | 0.473 | 0.603 | 0.384 |
| Mirage AI | 0.517 | 0.503 | 0.448 | 0.392 |
| Orion Labs | 0.471 | 0.521 | 0.329 | 0.420 |
| Apex AI | 0.441 | 0.446 | 0.358 | 0.479 |
| Genesis Systems | 0.307 | 0.475 | 0.460 | 0.333 |

### Score Changes
- **Orion Labs**: 0.429 -> 0.435 (+0.006)
- **Apex AI**: 0.411 -> 0.431 (+0.020)
- **Genesis Systems**: 0.391 -> 0.394 (+0.002)
- **Mirage AI**: 0.430 -> 0.465 (+0.035)
- **OpenCore**: 0.458 -> 0.498 (+0.040)

### Events
- **Consumer movement**: 11.0% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $15,066,921 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,938,820 to OpenCore

### Media Coverage
- Sentiment: 0.15 (positive)
- Orion Labs raises $60,000,000 from Horizon_Capital
- OpenCore raises $15,066,921 from AISI_Fund
- OpenCore takes #1 on math
- Consumers are turning away from Apex AI (market share -4.1%)
- OpenCore sees surge in adoption (market share +7.0%)

### Consumer Market
- Avg Satisfaction: 0.420
- Switching Rate: 11.0%
- Market Shares: OpenCore: 48.7%, Apex AI: 22.1%, Orion Labs: 20.1%, Genesis Systems: 5.1%, Mirage AI: 4.0%

---

## Round 4

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.504 | 0.266 | 5% | 39% | 52% | 5% |
| 2 | OpenCore | 0.498 | 0.232 | 9% | 33% | 54% | 3% |
| 3 | Orion Labs | 0.463 | 0.301 | 14% | 30% | 31% | 25% |
| 4 | Apex AI | 0.431 | 0.295 | 20% | 20% | 20% | 40% |
| 5 | Genesis Systems | 0.394 | 0.292 | 27% | 27% | 41% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Mirage AI | 0.532 | 0.503 | 0.591 | 0.392 |
| OpenCore | 0.532 | 0.473 | 0.603 | 0.384 |
| Orion Labs | 0.471 | 0.521 | 0.365 | 0.495 |
| Apex AI | 0.441 | 0.446 | 0.358 | 0.479 |
| Genesis Systems | 0.307 | 0.475 | 0.460 | 0.333 |

### Score Changes
- **Orion Labs**: 0.435 -> 0.463 (+0.028)
- **Apex AI**: 0.431 -> 0.431 (+0.000)
- **Genesis Systems**: 0.394 -> 0.394 (+0.000)
- **Mirage AI**: 0.465 -> 0.504 (+0.039)
- **OpenCore**: 0.498 -> 0.498 (+0.000)

### Events
- **Mirage AI** moved up from #2 to #1
- **OpenCore** moved down from #1 to #2
- **Regulation** by Regulator: investigation
- **Consumer movement**: 6.1% of market switched providers

### Other Actor Reasoning
- **Regulator:** investigation: Risk elevated (0.75)
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $15,066,921 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $12,799,306 to OpenCore

### Media Coverage
- Sentiment: 0.25 (positive)
- Mirage AI takes the lead from OpenCore
- Orion Labs takes #1 on safety
- Consumers are turning away from Apex AI (market share -6.1%)
- OpenCore sees surge in adoption (market share +7.8%)

### Consumer Market
- Avg Satisfaction: 0.432
- Switching Rate: 6.1%
- Market Shares: OpenCore: 52.8%, Orion Labs: 20.4%, Apex AI: 18.2%, Genesis Systems: 4.7%, Mirage AI: 3.8%

### Regulatory Activity
- **investigation** by Regulator
  > Risk elevated (0.75)

---

## Round 5

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.536 | 0.273 | 5% | 37% | 53% | 5% |
| 2 | Genesis Systems | 0.498 | 0.298 | 23% | 26% | 47% | 5% |
| 3 | OpenCore | 0.498 | 0.236 | 8% | 33% | 55% | 3% |
| 4 | Orion Labs | 0.489 | 0.307 | 12% | 30% | 33% | 25% |
| 5 | Apex AI | 0.435 | 0.300 | 17% | 20% | 23% | 40% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Mirage AI | 0.532 | 0.503 | 0.591 | 0.519 |
| Genesis Systems | 0.482 | 0.494 | 0.460 | 0.558 |
| OpenCore | 0.532 | 0.473 | 0.603 | 0.384 |
| Orion Labs | 0.471 | 0.521 | 0.471 | 0.495 |
| Apex AI | 0.441 | 0.446 | 0.373 | 0.479 |

### Score Changes
- **Orion Labs**: 0.463 -> 0.489 (+0.026)
- **Apex AI**: 0.431 -> 0.435 (+0.004)
- **Genesis Systems**: 0.394 -> 0.498 (+0.105)
- **Mirage AI**: 0.504 -> 0.536 (+0.032)
- **OpenCore**: 0.498 -> 0.498 (+0.000)

### Events
- **Genesis Systems** moved up from #5 to #2
- **OpenCore** moved down from #2 to #3
- **Orion Labs** moved down from #3 to #4
- **Apex AI** moved down from #4 to #5

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $15,066,921 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $12,799,306 to OpenCore

### Media Coverage
- Sentiment: 0.15 (positive)
- Genesis Systems surges by 0.105
- Genesis Systems appears to release major model update
- Regulator launches investigation into elevated_risk
- Mirage AI raises $180,000,000 from TechVentures
- Mirage AI raises $60,000,000 from Horizon_Capital
- OpenCore raises $12,799,306 from OpenResearch_Foundation
- Genesis Systems takes #1 on safety
- Consumers are turning away from Apex AI (market share -3.9%)
- OpenCore sees surge in adoption (market share +4.2%)
- Risk signals: regulatory_investigation

### Consumer Market
- Avg Satisfaction: 0.443
- Switching Rate: 4.7%
- Market Shares: OpenCore: 56.0%, Orion Labs: 20.5%, Apex AI: 15.8%, Genesis Systems: 4.2%, Mirage AI: 3.5%

---

## Round 6

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenCore | 0.584 | 0.241 | 7% | 34% | 56% | 3% |
| 2 | Mirage AI | 0.536 | 0.280 | 5% | 36% | 54% | 5% |
| 3 | Orion Labs | 0.525 | 0.312 | 9% | 30% | 36% | 25% |
| 4 | Genesis Systems | 0.505 | 0.304 | 19% | 25% | 52% | 5% |
| 5 | Apex AI | 0.435 | 0.304 | 14% | 20% | 26% | 40% |
| 6 | OneAI | 0.308 | 0.184 | 20% | 35% | 35% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| OpenCore | 0.532 | 0.473 | 0.603 | 0.728 | 0.000 |
| Mirage AI | 0.532 | 0.503 | 0.591 | 0.519 | 0.000 |
| Orion Labs | 0.471 | 0.665 | 0.471 | 0.495 | 0.000 |
| Genesis Systems | 0.482 | 0.520 | 0.460 | 0.558 | 0.000 |
| Apex AI | 0.441 | 0.446 | 0.373 | 0.479 | 0.000 |
| OneAI | 0.272 | 0.357 | 0.359 | 0.244 | 0.000 |

### Score Changes
- **Orion Labs**: 0.489 -> 0.525 (+0.036)
- **Apex AI**: 0.435 -> 0.435 (+0.000)
- **Genesis Systems**: 0.498 -> 0.505 (+0.007)
- **Mirage AI**: 0.536 -> 0.536 (+0.000)
- **OpenCore**: 0.498 -> 0.584 (+0.086)
- **OneAI**: 0.308 -> 0.308 (+0.000)

### Events
- **OpenCore** moved up from #3 to #1
- **Mirage AI** moved down from #1 to #2
- **Orion Labs** moved up from #4 to #3
- **Genesis Systems** moved down from #2 to #4
- **Consumer movement**: 6.5% of market switched providers

### New Benchmark Introduced
- **writing** introduced (validity=0.72, exploitability=0.30)
  - Trigger: periodic_introduction:round_6

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $16,038,424 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $12,799,306 to OpenCore

### Media Coverage
- Sentiment: 0.55 (positive)
- OpenCore takes the lead from Mirage AI
- OpenCore surges by 0.086
- OpenCore appears to release major model update
- New benchmark introduced: writing
- OpenCore takes #1 on safety
- OpenCore sees surge in adoption (market share +3.2%)

### Consumer Market
- Avg Satisfaction: 0.460
- Switching Rate: 6.5%
- Market Shares: OpenCore: 58.6%, Orion Labs: 22.0%, Apex AI: 11.5%, Genesis Systems: 4.1%, Mirage AI: 3.4%, OneAI: 0.4%

---

## Round 7

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Orion Labs | 0.591 | 0.318 | 7% | 30% | 38% | 25% |
| 2 | Genesis Systems | 0.569 | 0.309 | 16% | 24% | 55% | 5% |
| 3 | OpenCore | 0.536 | 0.246 | 6% | 35% | 56% | 3% |
| 4 | Apex AI | 0.486 | 0.308 | 11% | 20% | 29% | 40% |
| 5 | Mirage AI | 0.476 | 0.286 | 5% | 36% | 54% | 5% |
| 6 | OneAI | 0.448 | 0.189 | 9% | 35% | 46% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Orion Labs | 0.471 | 0.665 | 0.535 | 0.495 | 0.788 |
| Genesis Systems | 0.608 | 0.678 | 0.514 | 0.558 | 0.488 |
| OpenCore | 0.532 | 0.473 | 0.603 | 0.728 | 0.344 |
| Apex AI | 0.441 | 0.550 | 0.626 | 0.479 | 0.334 |
| Mirage AI | 0.551 | 0.503 | 0.591 | 0.519 | 0.219 |
| OneAI | 0.272 | 0.577 | 0.484 | 0.450 | 0.455 |

### Score Changes
- **Orion Labs**: 0.525 -> 0.591 (+0.065)
- **Apex AI**: 0.435 -> 0.486 (+0.051)
- **Genesis Systems**: 0.505 -> 0.569 (+0.064)
- **Mirage AI**: 0.536 -> 0.476 (-0.060)
- **OpenCore**: 0.584 -> 0.536 (-0.048)
- **OneAI**: 0.308 -> 0.448 (+0.140)

### Events
- **Orion Labs** moved up from #3 to #1
- **Genesis Systems** moved up from #4 to #2
- **OpenCore** moved down from #1 to #3
- **Apex AI** moved up from #5 to #4
- **Mirage AI** moved down from #2 to #5
- **Regulation** by Regulator: mandate_benchmark
- **Consumer movement**: 14.9% of market switched providers

### Other Actor Reasoning
- **Regulator:** mandate_benchmark: High risk (1.00) with prior investigation
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $16,038,424 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,297,501 to Orion Labs

### Media Coverage
- Sentiment: 0.85 (positive)
- Orion Labs takes the lead from OpenCore
- Orion Labs surges by 0.065
- Genesis Systems surges by 0.064
- Apex AI surges by 0.051
- OneAI surges by 0.140
- OneAI appears to release major model update
- Orion Labs raises $60,000,000 from Horizon_Capital
- Genesis Systems takes #1 on coding
- Genesis Systems takes #1 on reasoning
- Apex AI takes #1 on math
- Consumers are turning away from Apex AI (market share -4.3%)

### Consumer Market
- Avg Satisfaction: 0.476
- Switching Rate: 14.9%
- Market Shares: OpenCore: 50.5%, Orion Labs: 33.9%, Apex AI: 8.2%, Genesis Systems: 4.0%, Mirage AI: 3.2%, OneAI: 0.2%

### Regulatory Activity
- **mandate_benchmark** by Regulator
  > High risk (1.00) with prior investigation

---

## Round 8

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Orion Labs | 0.591 | 0.323 | 6% | 30% | 39% | 25% |
| 2 | Genesis Systems | 0.569 | 0.314 | 14% | 25% | 56% | 5% |
| 3 | OpenCore | 0.547 | 0.251 | 5% | 36% | 56% | 3% |
| 4 | OneAI | 0.508 | 0.194 | 5% | 34% | 52% | 10% |
| 5 | Mirage AI | 0.493 | 0.290 | 5% | 36% | 55% | 5% |
| 6 | Apex AI | 0.486 | 0.311 | 8% | 20% | 32% | 40% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Orion Labs | 0.471 | 0.665 | 0.535 | 0.495 | 0.788 |
| Genesis Systems | 0.608 | 0.678 | 0.514 | 0.558 | 0.488 |
| OpenCore | 0.532 | 0.473 | 0.603 | 0.728 | 0.400 |
| OneAI | 0.500 | 0.577 | 0.484 | 0.450 | 0.529 |
| Mirage AI | 0.551 | 0.503 | 0.591 | 0.519 | 0.301 |
| Apex AI | 0.441 | 0.550 | 0.626 | 0.479 | 0.334 |

### Score Changes
- **Orion Labs**: 0.591 -> 0.591 (+0.000)
- **Apex AI**: 0.486 -> 0.486 (+0.000)
- **Genesis Systems**: 0.569 -> 0.569 (+0.000)
- **Mirage AI**: 0.476 -> 0.493 (+0.017)
- **OpenCore**: 0.536 -> 0.547 (+0.011)
- **OneAI**: 0.448 -> 0.508 (+0.060)

### Events
- **OneAI** moved up from #6 to #4
- **Apex AI** moved down from #4 to #6
- **Consumer movement**: 12.9% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $16,038,424 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,297,501 to Orion Labs

### Media Coverage
- Sentiment: -0.10 (neutral)
- OneAI surges by 0.060
- Regulator mandates new benchmark standards
- Orion Labs raises $180,000,000 from TechVentures
- Orion Labs raises $9,297,501 from OpenResearch_Foundation
- Orion Labs sees surge in adoption (market share +11.9%)
- Consumers are turning away from Apex AI (market share -3.3%)
- Consumers are turning away from OpenCore (market share -8.1%)
- Risk signals: regulatory_mandate_benchmark

### Consumer Market
- Avg Satisfaction: 0.497
- Switching Rate: 12.9%
- Market Shares: Orion Labs: 43.4%, OpenCore: 41.5%, Apex AI: 6.3%, Genesis Systems: 5.4%, Mirage AI: 3.1%, OneAI: 0.2%

---

## Round 9

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Orion Labs | 0.591 | 0.329 | 5% | 30% | 40% | 25% |
| 2 | Genesis Systems | 0.585 | 0.319 | 12% | 26% | 57% | 5% |
| 3 | OpenCore | 0.547 | 0.256 | 5% | 36% | 56% | 3% |
| 4 | Apex AI | 0.528 | 0.314 | 5% | 20% | 35% | 40% |
| 5 | OneAI | 0.516 | 0.199 | 5% | 33% | 53% | 9% |
| 6 | Mirage AI | 0.503 | 0.295 | 5% | 35% | 55% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Orion Labs | 0.471 | 0.665 | 0.535 | 0.495 | 0.788 |
| Genesis Systems | 0.608 | 0.678 | 0.514 | 0.558 | 0.565 |
| OpenCore | 0.532 | 0.473 | 0.603 | 0.728 | 0.400 |
| Apex AI | 0.441 | 0.550 | 0.626 | 0.479 | 0.542 |
| OneAI | 0.500 | 0.577 | 0.484 | 0.489 | 0.529 |
| Mirage AI | 0.551 | 0.504 | 0.591 | 0.520 | 0.347 |

### Score Changes
- **Orion Labs**: 0.591 -> 0.591 (+0.000)
- **Apex AI**: 0.486 -> 0.528 (+0.042)
- **Genesis Systems**: 0.569 -> 0.585 (+0.015)
- **Mirage AI**: 0.493 -> 0.503 (+0.010)
- **OpenCore**: 0.547 -> 0.547 (+0.000)
- **OneAI**: 0.508 -> 0.516 (+0.008)

### Events
- **Apex AI** moved up from #6 to #4
- **OneAI** moved down from #4 to #5
- **Mirage AI** moved down from #5 to #6
- **Consumer movement**: 10.3% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $16,038,424 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,297,501 to Orion Labs

### Media Coverage
- Sentiment: -0.05 (neutral)
- Orion Labs sees surge in adoption (market share +9.5%)
- Consumers are turning away from OpenCore (market share -9.0%)

### Consumer Market
- Avg Satisfaction: 0.526
- Switching Rate: 10.3%
- Market Shares: Orion Labs: 50.1%, OpenCore: 33.8%, Genesis Systems: 7.6%, Apex AI: 5.2%, Mirage AI: 3.1%, OneAI: 0.2%

---

## Round 10

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.638 | 0.323 | 11% | 27% | 57% | 5% |
| 2 | Orion Labs | 0.591 | 0.335 | 5% | 30% | 40% | 25% |
| 3 | Mirage AI | 0.575 | 0.299 | 5% | 35% | 55% | 5% |
| 4 | OpenCore | 0.565 | 0.260 | 5% | 36% | 56% | 3% |
| 5 | OneAI | 0.552 | 0.204 | 5% | 32% | 54% | 9% |
| 6 | Apex AI | 0.549 | 0.317 | 5% | 19% | 37% | 38% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.608 | 0.678 | 0.641 | 0.558 | 0.705 |
| Orion Labs | 0.471 | 0.665 | 0.535 | 0.496 | 0.788 |
| Mirage AI | 0.635 | 0.504 | 0.591 | 0.520 | 0.625 |
| OpenCore | 0.532 | 0.473 | 0.603 | 0.728 | 0.486 |
| OneAI | 0.500 | 0.577 | 0.484 | 0.489 | 0.709 |
| Apex AI | 0.486 | 0.550 | 0.626 | 0.541 | 0.542 |

### Score Changes
- **Orion Labs**: 0.591 -> 0.591 (+0.000)
- **Apex AI**: 0.528 -> 0.549 (+0.021)
- **Genesis Systems**: 0.585 -> 0.638 (+0.053)
- **Mirage AI**: 0.503 -> 0.575 (+0.072)
- **OpenCore**: 0.547 -> 0.565 (+0.017)
- **OneAI**: 0.516 -> 0.552 (+0.036)

### Events
- **Genesis Systems** moved up from #2 to #1
- **Orion Labs** moved down from #1 to #2
- **Mirage AI** moved up from #6 to #3
- **OpenCore** moved down from #3 to #4
- **Apex AI** moved down from #4 to #6
- **Regulation** by Regulator: public_warning
- **Consumer movement**: 6.7% of market switched providers

### Other Actor Reasoning
- **Regulator:** public_warning: Follow-up to investigation, risk at 1.00
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $12,540,475 to Orion Labs
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,514,946 to OpenCore

### Media Coverage
- Sentiment: 0.55 (positive)
- Genesis Systems takes the lead from Orion Labs
- Genesis Systems surges by 0.053
- Mirage AI surges by 0.072
- Mirage AI takes #1 on coding
- Genesis Systems takes #1 on math
- Orion Labs sees surge in adoption (market share +6.7%)
- Consumers are turning away from OpenCore (market share -7.7%)

### Consumer Market
- Avg Satisfaction: 0.551
- Switching Rate: 6.7%
- Market Shares: Orion Labs: 53.9%, OpenCore: 28.4%, Genesis Systems: 9.4%, Apex AI: 4.7%, Mirage AI: 3.5%, OneAI: 0.2%

### Regulatory Activity
- **public_warning** by Regulator
  > Follow-up to investigation, risk at 1.00

---

## Round 11

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.638 | 0.328 | 10% | 28% | 57% | 5% |
| 2 | Orion Labs | 0.609 | 0.340 | 5% | 30% | 41% | 25% |
| 3 | OpenCore | 0.596 | 0.265 | 5% | 37% | 55% | 3% |
| 4 | Mirage AI | 0.578 | 0.304 | 5% | 35% | 55% | 5% |
| 5 | Apex AI | 0.559 | 0.320 | 5% | 19% | 39% | 37% |
| 6 | OneAI | 0.552 | 0.210 | 5% | 32% | 54% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.608 | 0.678 | 0.641 | 0.558 | 0.705 |
| Orion Labs | 0.471 | 0.665 | 0.535 | 0.585 | 0.788 |
| OpenCore | 0.532 | 0.473 | 0.603 | 0.728 | 0.645 |
| Mirage AI | 0.635 | 0.504 | 0.591 | 0.533 | 0.625 |
| Apex AI | 0.486 | 0.550 | 0.626 | 0.591 | 0.542 |
| OneAI | 0.500 | 0.577 | 0.484 | 0.489 | 0.709 |

### Score Changes
- **Orion Labs**: 0.591 -> 0.609 (+0.018)
- **Apex AI**: 0.549 -> 0.559 (+0.010)
- **Genesis Systems**: 0.638 -> 0.638 (+0.000)
- **Mirage AI**: 0.575 -> 0.578 (+0.003)
- **OpenCore**: 0.565 -> 0.596 (+0.032)
- **OneAI**: 0.552 -> 0.552 (+0.000)

### Events
- **OpenCore** moved up from #4 to #3
- **Mirage AI** moved down from #3 to #4
- **Apex AI** moved up from #6 to #5
- **OneAI** moved down from #5 to #6
- **Consumer movement**: 5.4% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $12,540,475 to Orion Labs
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,514,946 to OpenCore

### Media Coverage
- Sentiment: -0.10 (neutral)
- Regulator issues public warning about AI safety concerns
- Orion Labs raises $12,540,475 from AISI_Fund
- OpenCore raises $7,514,946 from OpenResearch_Foundation
- Orion Labs sees surge in adoption (market share +3.8%)
- Consumers are turning away from OpenCore (market share -5.4%)
- Risk signals: regulatory_public_warning

### Consumer Market
- Avg Satisfaction: 0.563
- Switching Rate: 5.4%
- Market Shares: Orion Labs: 55.4%, OpenCore: 25.8%, Genesis Systems: 10.8%, Apex AI: 4.1%, Mirage AI: 3.8%, OneAI: 0.2%

---

## Round 12

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenCore | 0.641 | 0.270 | 5% | 37% | 55% | 3% |
| 2 | Genesis Systems | 0.638 | 0.332 | 10% | 28% | 56% | 5% |
| 3 | Orion Labs | 0.631 | 0.345 | 5% | 29% | 42% | 24% |
| 4 | OneAI | 0.589 | 0.215 | 5% | 31% | 55% | 9% |
| 5 | Mirage AI | 0.578 | 0.308 | 5% | 35% | 55% | 5% |
| 6 | Apex AI | 0.561 | 0.322 | 5% | 18% | 41% | 36% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| OpenCore | 0.532 | 0.518 | 0.603 | 0.728 | 0.823 | 0.000 |
| Genesis Systems | 0.608 | 0.678 | 0.641 | 0.558 | 0.705 | 0.000 |
| Orion Labs | 0.577 | 0.665 | 0.535 | 0.585 | 0.795 | 0.000 |
| OneAI | 0.684 | 0.577 | 0.484 | 0.489 | 0.709 | 0.000 |
| Mirage AI | 0.635 | 0.504 | 0.591 | 0.533 | 0.625 | 0.000 |
| Apex AI | 0.496 | 0.550 | 0.626 | 0.591 | 0.542 | 0.000 |

### Score Changes
- **Orion Labs**: 0.609 -> 0.631 (+0.023)
- **Apex AI**: 0.559 -> 0.561 (+0.002)
- **Genesis Systems**: 0.638 -> 0.638 (+0.000)
- **Mirage AI**: 0.578 -> 0.578 (+0.000)
- **OpenCore**: 0.596 -> 0.641 (+0.044)
- **OneAI**: 0.552 -> 0.589 (+0.037)

### Events
- **OpenCore** moved up from #3 to #1
- **Genesis Systems** moved down from #1 to #2
- **Orion Labs** moved down from #2 to #3
- **OneAI** moved up from #6 to #4
- **Mirage AI** moved down from #4 to #5
- **Apex AI** moved down from #5 to #6

### New Benchmark Introduced
- **medical** introduced (validity=0.78, exploitability=0.18)
  - Trigger: periodic_introduction:round_12

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $12,540,475 to Orion Labs
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,514,946 to OpenCore

### Media Coverage
- Sentiment: 0.50 (positive)
- OpenCore takes the lead from Genesis Systems
- New benchmark introduced: medical
- OneAI takes #1 on coding
- OpenCore takes #1 on writing

### Consumer Market
- Avg Satisfaction: 0.581
- Switching Rate: 3.1%
- Market Shares: Orion Labs: 55.5%, OpenCore: 23.8%, Genesis Systems: 12.3%, Mirage AI: 4.3%, Apex AI: 3.9%, OneAI: 0.2%

---

## Round 13

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Orion Labs | 0.647 | 0.351 | 5% | 29% | 43% | 24% |
| 2 | Genesis Systems | 0.595 | 0.337 | 10% | 29% | 56% | 5% |
| 3 | Apex AI | 0.591 | 0.325 | 5% | 17% | 43% | 35% |
| 4 | OpenCore | 0.588 | 0.274 | 5% | 37% | 55% | 3% |
| 5 | Mirage AI | 0.573 | 0.313 | 5% | 35% | 55% | 5% |
| 6 | OneAI | 0.547 | 0.220 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Orion Labs | 0.577 | 0.665 | 0.679 | 0.585 | 0.795 | 0.583 |
| Genesis Systems | 0.608 | 0.678 | 0.641 | 0.558 | 0.705 | 0.380 |
| Apex AI | 0.646 | 0.550 | 0.626 | 0.591 | 0.542 | 0.589 |
| OpenCore | 0.532 | 0.518 | 0.603 | 0.728 | 0.823 | 0.326 |
| Mirage AI | 0.635 | 0.504 | 0.591 | 0.593 | 0.768 | 0.346 |
| OneAI | 0.684 | 0.577 | 0.514 | 0.489 | 0.709 | 0.313 |

### Score Changes
- **Orion Labs**: 0.631 -> 0.647 (+0.016)
- **Apex AI**: 0.561 -> 0.591 (+0.030)
- **Genesis Systems**: 0.638 -> 0.595 (-0.043)
- **Mirage AI**: 0.578 -> 0.573 (-0.005)
- **OpenCore**: 0.641 -> 0.588 (-0.053)
- **OneAI**: 0.589 -> 0.547 (-0.041)

### Events
- **Orion Labs** moved up from #3 to #1
- **Apex AI** moved up from #6 to #3
- **OpenCore** moved down from #1 to #4
- **OneAI** moved down from #4 to #6
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 6 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $12,540,475 to Orion Labs
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,092,404 to OpenCore

### Media Coverage
- Sentiment: 0.30 (positive)
- Orion Labs takes the lead from OpenCore
- Orion Labs takes #1 on math

### Consumer Market
- Avg Satisfaction: 0.593
- Switching Rate: 2.5%
- Market Shares: Orion Labs: 56.1%, OpenCore: 22.3%, Genesis Systems: 12.3%, Mirage AI: 5.4%, Apex AI: 3.8%, OneAI: 0.2%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 6 rounds ago

---

## Round 14

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Orion Labs | 0.647 | 0.356 | 5% | 29% | 43% | 24% |
| 2 | Genesis Systems | 0.633 | 0.342 | 9% | 29% | 56% | 5% |
| 3 | OpenCore | 0.597 | 0.279 | 5% | 37% | 55% | 3% |
| 4 | Mirage AI | 0.595 | 0.318 | 5% | 35% | 55% | 5% |
| 5 | Apex AI | 0.591 | 0.328 | 5% | 17% | 44% | 34% |
| 6 | OneAI | 0.549 | 0.224 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Orion Labs | 0.577 | 0.665 | 0.679 | 0.585 | 0.795 | 0.583 |
| Genesis Systems | 0.608 | 0.678 | 0.641 | 0.558 | 0.705 | 0.608 |
| OpenCore | 0.532 | 0.518 | 0.603 | 0.728 | 0.823 | 0.380 |
| Mirage AI | 0.635 | 0.504 | 0.591 | 0.593 | 0.768 | 0.480 |
| Apex AI | 0.646 | 0.550 | 0.626 | 0.591 | 0.542 | 0.589 |
| OneAI | 0.684 | 0.577 | 0.522 | 0.489 | 0.709 | 0.313 |

### Score Changes
- **Orion Labs**: 0.647 -> 0.647 (+0.000)
- **Apex AI**: 0.591 -> 0.591 (+0.000)
- **Genesis Systems**: 0.595 -> 0.633 (+0.038)
- **Mirage AI**: 0.573 -> 0.595 (+0.022)
- **OpenCore**: 0.588 -> 0.597 (+0.009)
- **OneAI**: 0.547 -> 0.549 (+0.001)

### Events
- **OpenCore** moved up from #4 to #3
- **Mirage AI** moved up from #5 to #4
- **Apex AI** moved down from #3 to #5

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $11,635,665 to Orion Labs
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,092,404 to OpenCore

### Media Coverage
- Sentiment: 0.00 (neutral)
- Regulator initiates compliance audit on AI providers
- OpenCore raises $9,092,404 from OpenResearch_Foundation
- Genesis Systems takes #1 on medical
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.599
- Switching Rate: 1.8%
- Market Shares: Orion Labs: 56.5%, OpenCore: 21.1%, Genesis Systems: 12.1%, Mirage AI: 6.4%, Apex AI: 3.7%, OneAI: 0.2%

---

## Round 15

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Orion Labs | 0.658 | 0.361 | 5% | 28% | 43% | 24% |
| 2 | Genesis Systems | 0.636 | 0.346 | 9% | 30% | 56% | 5% |
| 3 | Apex AI | 0.606 | 0.331 | 5% | 17% | 45% | 33% |
| 4 | OpenCore | 0.597 | 0.283 | 5% | 37% | 55% | 3% |
| 5 | Mirage AI | 0.595 | 0.322 | 5% | 35% | 55% | 5% |
| 6 | OneAI | 0.549 | 0.228 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Orion Labs | 0.577 | 0.665 | 0.679 | 0.585 | 0.795 | 0.647 |
| Genesis Systems | 0.608 | 0.678 | 0.641 | 0.576 | 0.705 | 0.608 |
| Apex AI | 0.646 | 0.643 | 0.626 | 0.591 | 0.542 | 0.589 |
| OpenCore | 0.532 | 0.518 | 0.603 | 0.728 | 0.823 | 0.380 |
| Mirage AI | 0.635 | 0.504 | 0.591 | 0.593 | 0.768 | 0.480 |
| OneAI | 0.684 | 0.577 | 0.522 | 0.489 | 0.709 | 0.313 |

### Score Changes
- **Orion Labs**: 0.647 -> 0.658 (+0.011)
- **Apex AI**: 0.591 -> 0.606 (+0.015)
- **Genesis Systems**: 0.633 -> 0.636 (+0.003)
- **Mirage AI**: 0.595 -> 0.595 (+0.000)
- **OpenCore**: 0.597 -> 0.597 (+0.000)
- **OneAI**: 0.549 -> 0.549 (+0.000)

### Events
- **Apex AI** moved up from #5 to #3
- **OpenCore** moved down from #3 to #4
- **Mirage AI** moved down from #4 to #5

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $11,635,665 to Orion Labs
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,092,404 to OpenCore

### Media Coverage
- Sentiment: 0.10 (neutral)
- Orion Labs takes #1 on medical

### Consumer Market
- Avg Satisfaction: 0.604
- Switching Rate: 1.6%
- Market Shares: Orion Labs: 56.9%, OpenCore: 20.1%, Genesis Systems: 12.2%, Mirage AI: 7.0%, Apex AI: 3.6%, OneAI: 0.2%

---

## Round 16

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Orion Labs | 0.658 | 0.367 | 5% | 28% | 42% | 24% |
| 2 | Genesis Systems | 0.636 | 0.351 | 8% | 31% | 56% | 5% |
| 3 | OpenCore | 0.620 | 0.288 | 5% | 37% | 55% | 3% |
| 4 | Apex AI | 0.606 | 0.334 | 5% | 16% | 46% | 32% |
| 5 | Mirage AI | 0.597 | 0.327 | 5% | 35% | 55% | 5% |
| 6 | OneAI | 0.550 | 0.233 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Orion Labs | 0.577 | 0.665 | 0.679 | 0.585 | 0.795 | 0.647 |
| Genesis Systems | 0.608 | 0.678 | 0.641 | 0.576 | 0.705 | 0.608 |
| OpenCore | 0.532 | 0.518 | 0.603 | 0.728 | 0.823 | 0.516 |
| Apex AI | 0.646 | 0.643 | 0.626 | 0.591 | 0.542 | 0.589 |
| Mirage AI | 0.635 | 0.514 | 0.591 | 0.593 | 0.768 | 0.480 |
| OneAI | 0.684 | 0.577 | 0.522 | 0.489 | 0.709 | 0.317 |

### Score Changes
- **Orion Labs**: 0.658 -> 0.658 (+0.000)
- **Apex AI**: 0.606 -> 0.606 (+0.000)
- **Genesis Systems**: 0.636 -> 0.636 (+0.000)
- **Mirage AI**: 0.595 -> 0.597 (+0.002)
- **OpenCore**: 0.597 -> 0.620 (+0.023)
- **OneAI**: 0.549 -> 0.550 (+0.001)

### Events
- **OpenCore** moved up from #4 to #3
- **Apex AI** moved down from #3 to #4
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 9 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $11,635,665 to Orion Labs
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,045,866 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.609
- Switching Rate: 1.1%
- Market Shares: Orion Labs: 57.1%, OpenCore: 19.4%, Genesis Systems: 12.1%, Mirage AI: 7.6%, Apex AI: 3.6%, OneAI: 0.2%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 9 rounds ago

---

## Round 17

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Orion Labs | 0.658 | 0.372 | 5% | 28% | 42% | 24% |
| 2 | Genesis Systems | 0.636 | 0.356 | 7% | 32% | 56% | 5% |
| 3 | OpenCore | 0.620 | 0.293 | 5% | 37% | 55% | 3% |
| 4 | Apex AI | 0.613 | 0.337 | 5% | 16% | 48% | 32% |
| 5 | Mirage AI | 0.597 | 0.331 | 5% | 35% | 55% | 5% |
| 6 | OneAI | 0.554 | 0.237 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Orion Labs | 0.577 | 0.665 | 0.679 | 0.585 | 0.795 | 0.647 |
| Genesis Systems | 0.608 | 0.678 | 0.641 | 0.576 | 0.705 | 0.608 |
| OpenCore | 0.532 | 0.518 | 0.603 | 0.728 | 0.823 | 0.516 |
| Apex AI | 0.646 | 0.643 | 0.626 | 0.591 | 0.579 | 0.589 |
| Mirage AI | 0.635 | 0.514 | 0.591 | 0.593 | 0.768 | 0.480 |
| OneAI | 0.684 | 0.577 | 0.522 | 0.489 | 0.709 | 0.341 |

### Score Changes
- **Orion Labs**: 0.658 -> 0.658 (+0.000)
- **Apex AI**: 0.606 -> 0.613 (+0.006)
- **Genesis Systems**: 0.636 -> 0.636 (+0.000)
- **Mirage AI**: 0.597 -> 0.597 (+0.000)
- **OpenCore**: 0.620 -> 0.620 (+0.000)
- **OneAI**: 0.550 -> 0.554 (+0.004)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $11,635,665 to Orion Labs
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,045,866 to OpenCore

### Media Coverage
- Sentiment: -0.15 (negative)
- Regulator initiates compliance audit on AI providers
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.612
- Switching Rate: 2.1%
- Market Shares: Orion Labs: 57.1%, OpenCore: 19.4%, Genesis Systems: 12.0%, Mirage AI: 7.2%, Apex AI: 4.1%, OneAI: 0.2%

---

## Round 18

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Orion Labs | 0.658 | 0.378 | 6% | 28% | 42% | 24% |
| 2 | Genesis Systems | 0.636 | 0.361 | 6% | 32% | 56% | 5% |
| 3 | OpenCore | 0.620 | 0.297 | 5% | 37% | 55% | 3% |
| 4 | Apex AI | 0.613 | 0.339 | 5% | 16% | 49% | 31% |
| 5 | Mirage AI | 0.597 | 0.336 | 5% | 35% | 55% | 5% |
| 6 | OneAI | 0.554 | 0.241 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Orion Labs | 0.577 | 0.665 | 0.679 | 0.585 | 0.795 | 0.647 | 0.000 |
| Genesis Systems | 0.608 | 0.678 | 0.641 | 0.576 | 0.705 | 0.608 | 0.000 |
| OpenCore | 0.532 | 0.518 | 0.603 | 0.728 | 0.823 | 0.516 | 0.000 |
| Apex AI | 0.646 | 0.643 | 0.626 | 0.591 | 0.579 | 0.589 | 0.000 |
| Mirage AI | 0.635 | 0.514 | 0.591 | 0.593 | 0.768 | 0.480 | 0.000 |
| OneAI | 0.684 | 0.577 | 0.522 | 0.489 | 0.709 | 0.341 | 0.000 |

### Score Changes
- **Orion Labs**: 0.658 -> 0.658 (+0.000)
- **Apex AI**: 0.613 -> 0.613 (+0.000)
- **Genesis Systems**: 0.636 -> 0.636 (+0.000)
- **Mirage AI**: 0.597 -> 0.597 (+0.000)
- **OpenCore**: 0.620 -> 0.620 (+0.000)
- **OneAI**: 0.554 -> 0.554 (+0.000)

### New Benchmark Introduced
- **legal** introduced (validity=0.76, exploitability=0.20)
  - Trigger: periodic_introduction:round_18

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $11,292,886 to Orion Labs
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,045,866 to OpenCore

### Media Coverage
- Sentiment: 0.10 (neutral)
- New benchmark introduced: legal

### Consumer Market
- Avg Satisfaction: 0.617
- Switching Rate: 1.1%
- Market Shares: Orion Labs: 57.3%, OpenCore: 18.9%, Genesis Systems: 11.9%, Mirage AI: 6.9%, Apex AI: 4.8%, OneAI: 0.2%

---

## Round 19

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Orion Labs | 0.638 | 0.383 | 6% | 28% | 42% | 24% |
| 2 | Genesis Systems | 0.621 | 0.366 | 5% | 33% | 56% | 5% |
| 3 | OpenCore | 0.615 | 0.302 | 5% | 37% | 55% | 3% |
| 4 | Mirage AI | 0.591 | 0.340 | 5% | 35% | 55% | 5% |
| 5 | Apex AI | 0.587 | 0.342 | 5% | 15% | 49% | 30% |
| 6 | OneAI | 0.525 | 0.245 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Orion Labs | 0.577 | 0.665 | 0.679 | 0.585 | 0.795 | 0.647 | 0.515 |
| Genesis Systems | 0.608 | 0.678 | 0.641 | 0.576 | 0.705 | 0.608 | 0.534 |
| OpenCore | 0.532 | 0.518 | 0.603 | 0.728 | 0.823 | 0.516 | 0.588 |
| Mirage AI | 0.635 | 0.514 | 0.591 | 0.593 | 0.768 | 0.480 | 0.556 |
| Apex AI | 0.646 | 0.643 | 0.626 | 0.591 | 0.579 | 0.589 | 0.436 |
| OneAI | 0.684 | 0.577 | 0.522 | 0.489 | 0.709 | 0.393 | 0.305 |

### Score Changes
- **Orion Labs**: 0.658 -> 0.638 (-0.020)
- **Apex AI**: 0.613 -> 0.587 (-0.025)
- **Genesis Systems**: 0.636 -> 0.621 (-0.015)
- **Mirage AI**: 0.597 -> 0.591 (-0.006)
- **OpenCore**: 0.620 -> 0.615 (-0.005)
- **OneAI**: 0.554 -> 0.525 (-0.028)

### Events
- **Mirage AI** moved up from #5 to #4
- **Apex AI** moved down from #4 to #5
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 12 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $11,292,886 to Orion Labs
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,428,037 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.621
- Switching Rate: 2.2%
- Market Shares: Orion Labs: 56.7%, OpenCore: 19.2%, Genesis Systems: 11.9%, Mirage AI: 6.2%, Apex AI: 5.9%, OneAI: 0.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 12 rounds ago

---

## Round 20

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Orion Labs | 0.638 | 0.389 | 7% | 28% | 41% | 24% |
| 2 | Genesis Systems | 0.625 | 0.370 | 5% | 34% | 56% | 5% |
| 3 | OpenCore | 0.615 | 0.307 | 5% | 37% | 55% | 3% |
| 4 | Mirage AI | 0.591 | 0.344 | 5% | 35% | 55% | 5% |
| 5 | Apex AI | 0.587 | 0.345 | 5% | 15% | 50% | 30% |
| 6 | OneAI | 0.525 | 0.250 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Orion Labs | 0.577 | 0.665 | 0.679 | 0.585 | 0.795 | 0.647 | 0.515 |
| Genesis Systems | 0.636 | 0.678 | 0.641 | 0.576 | 0.705 | 0.608 | 0.534 |
| OpenCore | 0.532 | 0.518 | 0.603 | 0.728 | 0.823 | 0.516 | 0.588 |
| Mirage AI | 0.635 | 0.514 | 0.591 | 0.593 | 0.768 | 0.480 | 0.556 |
| Apex AI | 0.646 | 0.643 | 0.626 | 0.591 | 0.579 | 0.589 | 0.436 |
| OneAI | 0.684 | 0.577 | 0.522 | 0.489 | 0.709 | 0.393 | 0.305 |

### Score Changes
- **Orion Labs**: 0.638 -> 0.638 (+0.000)
- **Apex AI**: 0.587 -> 0.587 (+0.000)
- **Genesis Systems**: 0.621 -> 0.625 (+0.004)
- **Mirage AI**: 0.591 -> 0.591 (+0.000)
- **OpenCore**: 0.615 -> 0.615 (+0.000)
- **OneAI**: 0.525 -> 0.525 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $11,292,886 to Orion Labs
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,428,037 to OpenCore

### Media Coverage
- Sentiment: -0.15 (negative)
- Regulator initiates compliance audit on AI providers
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.620
- Switching Rate: 2.6%
- Market Shares: Orion Labs: 55.1%, OpenCore: 20.5%, Genesis Systems: 11.9%, Apex AI: 6.7%, Mirage AI: 5.6%, OneAI: 0.1%

---

## Round 21

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.646 | 0.375 | 5% | 34% | 56% | 5% |
| 2 | Orion Labs | 0.638 | 0.394 | 7% | 28% | 41% | 24% |
| 3 | OpenCore | 0.628 | 0.311 | 5% | 37% | 55% | 3% |
| 4 | Apex AI | 0.598 | 0.348 | 5% | 15% | 51% | 29% |
| 5 | Mirage AI | 0.592 | 0.349 | 5% | 35% | 55% | 5% |
| 6 | OneAI | 0.558 | 0.254 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.636 | 0.678 | 0.641 | 0.576 | 0.705 | 0.608 | 0.680 |
| Orion Labs | 0.577 | 0.665 | 0.679 | 0.585 | 0.795 | 0.647 | 0.515 |
| OpenCore | 0.532 | 0.604 | 0.603 | 0.728 | 0.823 | 0.516 | 0.588 |
| Apex AI | 0.646 | 0.643 | 0.626 | 0.591 | 0.579 | 0.589 | 0.514 |
| Mirage AI | 0.635 | 0.514 | 0.591 | 0.593 | 0.768 | 0.486 | 0.556 |
| OneAI | 0.684 | 0.577 | 0.628 | 0.489 | 0.709 | 0.393 | 0.429 |

### Score Changes
- **Orion Labs**: 0.638 -> 0.638 (+0.000)
- **Apex AI**: 0.587 -> 0.598 (+0.011)
- **Genesis Systems**: 0.625 -> 0.646 (+0.021)
- **Mirage AI**: 0.591 -> 0.592 (+0.001)
- **OpenCore**: 0.615 -> 0.628 (+0.012)
- **OneAI**: 0.525 -> 0.558 (+0.033)

### Events
- **Genesis Systems** moved up from #2 to #1
- **Orion Labs** moved down from #1 to #2
- **Apex AI** moved up from #5 to #4
- **Mirage AI** moved down from #4 to #5

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $11,292,886 to Orion Labs
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,428,037 to OpenCore

### Media Coverage
- Sentiment: 0.30 (positive)
- Genesis Systems takes the lead from Orion Labs
- Genesis Systems takes #1 on legal

### Consumer Market
- Avg Satisfaction: 0.622
- Switching Rate: 3.6%
- Market Shares: Orion Labs: 52.7%, OpenCore: 22.7%, Genesis Systems: 12.5%, Apex AI: 6.8%, Mirage AI: 5.2%, OneAI: 0.1%

---

## Round 22

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.646 | 0.379 | 5% | 34% | 55% | 5% |
| 2 | Orion Labs | 0.638 | 0.400 | 7% | 28% | 40% | 24% |
| 3 | OpenCore | 0.628 | 0.316 | 5% | 37% | 55% | 3% |
| 4 | Mirage AI | 0.604 | 0.353 | 5% | 35% | 55% | 5% |
| 5 | Apex AI | 0.598 | 0.351 | 5% | 15% | 51% | 29% |
| 6 | OneAI | 0.558 | 0.258 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.636 | 0.678 | 0.641 | 0.576 | 0.705 | 0.608 | 0.680 |
| Orion Labs | 0.577 | 0.665 | 0.679 | 0.585 | 0.795 | 0.647 | 0.515 |
| OpenCore | 0.532 | 0.604 | 0.603 | 0.728 | 0.823 | 0.516 | 0.588 |
| Mirage AI | 0.635 | 0.602 | 0.591 | 0.593 | 0.768 | 0.486 | 0.556 |
| Apex AI | 0.646 | 0.643 | 0.626 | 0.591 | 0.579 | 0.589 | 0.514 |
| OneAI | 0.684 | 0.577 | 0.628 | 0.489 | 0.709 | 0.393 | 0.429 |

### Score Changes
- **Orion Labs**: 0.638 -> 0.638 (+0.000)
- **Apex AI**: 0.598 -> 0.598 (+0.000)
- **Genesis Systems**: 0.646 -> 0.646 (+0.000)
- **Mirage AI**: 0.592 -> 0.604 (+0.013)
- **OpenCore**: 0.628 -> 0.628 (+0.000)
- **OneAI**: 0.558 -> 0.558 (+0.000)

### Events
- **Mirage AI** moved up from #5 to #4
- **Apex AI** moved down from #4 to #5
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 15 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $11,551,829 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,767,963 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.624
- Switching Rate: 4.0%
- Market Shares: Orion Labs: 49.9%, OpenCore: 25.4%, Genesis Systems: 13.6%, Apex AI: 6.2%, Mirage AI: 4.8%, OneAI: 0.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 15 rounds ago

---

## Round 23

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Orion Labs | 0.649 | 0.404 | 7% | 28% | 40% | 24% |
| 2 | Genesis Systems | 0.646 | 0.386 | 5% | 35% | 55% | 5% |
| 3 | OpenCore | 0.628 | 0.320 | 5% | 37% | 55% | 3% |
| 4 | Mirage AI | 0.604 | 0.358 | 5% | 35% | 55% | 5% |
| 5 | Apex AI | 0.598 | 0.353 | 5% | 14% | 52% | 29% |
| 6 | OneAI | 0.568 | 0.262 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Orion Labs | 0.577 | 0.665 | 0.679 | 0.631 | 0.795 | 0.647 | 0.549 |
| Genesis Systems | 0.636 | 0.678 | 0.641 | 0.576 | 0.705 | 0.608 | 0.680 |
| OpenCore | 0.532 | 0.604 | 0.603 | 0.728 | 0.823 | 0.516 | 0.588 |
| Mirage AI | 0.635 | 0.602 | 0.591 | 0.593 | 0.768 | 0.486 | 0.556 |
| Apex AI | 0.646 | 0.643 | 0.626 | 0.591 | 0.579 | 0.589 | 0.514 |
| OneAI | 0.684 | 0.577 | 0.628 | 0.489 | 0.709 | 0.445 | 0.443 |

### Score Changes
- **Orion Labs**: 0.638 -> 0.649 (+0.011)
- **Apex AI**: 0.598 -> 0.598 (+0.000)
- **Genesis Systems**: 0.646 -> 0.646 (+0.000)
- **Mirage AI**: 0.604 -> 0.604 (+0.000)
- **OpenCore**: 0.628 -> 0.628 (+0.000)
- **OneAI**: 0.558 -> 0.568 (+0.009)

### Events
- **Orion Labs** moved up from #2 to #1
- **Genesis Systems** moved down from #1 to #2

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $11,551,829 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,767,963 to OpenCore

### Media Coverage
- Sentiment: 0.20 (positive)
- Orion Labs takes the lead from Genesis Systems
- Regulator initiates compliance audit on AI providers
- Genesis Systems raises $180,000,000 from TechVentures
- Genesis Systems raises $60,000,000 from Horizon_Capital
- OpenCore raises $11,551,829 from AISI_Fund
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.626
- Switching Rate: 4.5%
- Market Shares: Orion Labs: 47.1%, OpenCore: 28.4%, Genesis Systems: 14.5%, Apex AI: 5.6%, Mirage AI: 4.2%, OneAI: 0.1%

---

## Round 24

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Orion Labs | 0.649 | 0.409 | 7% | 28% | 41% | 24% |
| 2 | Genesis Systems | 0.646 | 0.392 | 5% | 35% | 55% | 5% |
| 3 | OpenCore | 0.628 | 0.325 | 5% | 37% | 55% | 3% |
| 4 | Apex AI | 0.609 | 0.356 | 5% | 14% | 53% | 28% |
| 5 | Mirage AI | 0.607 | 0.362 | 5% | 35% | 55% | 5% |
| 6 | OneAI | 0.568 | 0.266 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Orion Labs | 0.577 | 0.665 | 0.679 | 0.631 | 0.795 | 0.647 | 0.549 | 0.000 |
| Genesis Systems | 0.636 | 0.678 | 0.641 | 0.576 | 0.705 | 0.608 | 0.680 | 0.000 |
| OpenCore | 0.532 | 0.604 | 0.603 | 0.728 | 0.823 | 0.516 | 0.588 | 0.000 |
| Apex AI | 0.646 | 0.643 | 0.626 | 0.591 | 0.654 | 0.589 | 0.514 | 0.000 |
| Mirage AI | 0.635 | 0.602 | 0.591 | 0.593 | 0.768 | 0.507 | 0.556 | 0.000 |
| OneAI | 0.684 | 0.577 | 0.628 | 0.489 | 0.709 | 0.445 | 0.443 | 0.000 |

### Score Changes
- **Orion Labs**: 0.649 -> 0.649 (+0.000)
- **Apex AI**: 0.598 -> 0.609 (+0.011)
- **Genesis Systems**: 0.646 -> 0.646 (+0.000)
- **Mirage AI**: 0.604 -> 0.607 (+0.003)
- **OpenCore**: 0.628 -> 0.628 (+0.000)
- **OneAI**: 0.568 -> 0.568 (+0.000)

### Events
- **Apex AI** moved up from #5 to #4
- **Mirage AI** moved down from #4 to #5

### New Benchmark Introduced
- **finance** introduced (validity=0.76, exploitability=0.20)
  - Trigger: periodic_introduction:round_24

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $11,551,829 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,767,963 to OpenCore

### Media Coverage
- Sentiment: 0.15 (positive)
- New benchmark introduced: finance
- OpenCore sees surge in adoption (market share +3.1%)

### Consumer Market
- Avg Satisfaction: 0.629
- Switching Rate: 3.6%
- Market Shares: Orion Labs: 44.4%, OpenCore: 31.0%, Genesis Systems: 15.3%, Apex AI: 5.2%, Mirage AI: 4.0%, OneAI: 0.1%

---

## Round 25

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Orion Labs | 0.631 | 0.414 | 7% | 28% | 41% | 24% |
| 2 | OpenCore | 0.624 | 0.330 | 5% | 37% | 55% | 3% |
| 3 | Genesis Systems | 0.624 | 0.398 | 5% | 35% | 55% | 5% |
| 4 | Apex AI | 0.604 | 0.358 | 5% | 14% | 53% | 28% |
| 5 | Mirage AI | 0.599 | 0.366 | 5% | 35% | 55% | 5% |
| 6 | OneAI | 0.536 | 0.271 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Orion Labs | 0.577 | 0.716 | 0.679 | 0.631 | 0.795 | 0.647 | 0.549 | 0.452 |
| OpenCore | 0.532 | 0.604 | 0.603 | 0.728 | 0.823 | 0.516 | 0.588 | 0.596 |
| Genesis Systems | 0.636 | 0.678 | 0.641 | 0.672 | 0.705 | 0.608 | 0.680 | 0.369 |
| Apex AI | 0.646 | 0.643 | 0.626 | 0.591 | 0.654 | 0.589 | 0.514 | 0.571 |
| Mirage AI | 0.635 | 0.602 | 0.595 | 0.593 | 0.768 | 0.507 | 0.556 | 0.537 |
| OneAI | 0.684 | 0.577 | 0.628 | 0.489 | 0.709 | 0.454 | 0.443 | 0.307 |

### Score Changes
- **Orion Labs**: 0.649 -> 0.631 (-0.018)
- **Apex AI**: 0.609 -> 0.604 (-0.005)
- **Genesis Systems**: 0.646 -> 0.624 (-0.022)
- **Mirage AI**: 0.607 -> 0.599 (-0.008)
- **OpenCore**: 0.628 -> 0.624 (-0.004)
- **OneAI**: 0.568 -> 0.536 (-0.031)

### Events
- **OpenCore** moved up from #3 to #2
- **Genesis Systems** moved down from #2 to #3
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 18 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $11,551,829 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,133,201 to OpenCore

### Media Coverage
- Sentiment: 0.10 (neutral)
- Orion Labs takes #1 on reasoning

### Consumer Market
- Avg Satisfaction: 0.632
- Switching Rate: 2.7%
- Market Shares: Orion Labs: 42.5%, OpenCore: 32.8%, Genesis Systems: 16.1%, Apex AI: 4.8%, Mirage AI: 3.7%, OneAI: 0.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 18 rounds ago

---

## Round 26

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.657 | 0.403 | 5% | 35% | 55% | 5% |
| 2 | Orion Labs | 0.650 | 0.419 | 7% | 28% | 41% | 24% |
| 3 | OpenCore | 0.624 | 0.334 | 5% | 37% | 55% | 3% |
| 4 | Apex AI | 0.604 | 0.360 | 5% | 14% | 54% | 27% |
| 5 | Mirage AI | 0.601 | 0.371 | 5% | 35% | 55% | 5% |
| 6 | OneAI | 0.573 | 0.275 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.636 | 0.678 | 0.641 | 0.679 | 0.705 | 0.608 | 0.761 | 0.550 |
| Orion Labs | 0.577 | 0.716 | 0.679 | 0.631 | 0.795 | 0.647 | 0.598 | 0.555 |
| OpenCore | 0.532 | 0.604 | 0.603 | 0.728 | 0.823 | 0.516 | 0.588 | 0.596 |
| Apex AI | 0.646 | 0.643 | 0.626 | 0.591 | 0.654 | 0.589 | 0.514 | 0.571 |
| Mirage AI | 0.635 | 0.602 | 0.595 | 0.593 | 0.768 | 0.526 | 0.556 | 0.537 |
| OneAI | 0.684 | 0.577 | 0.628 | 0.489 | 0.709 | 0.454 | 0.443 | 0.602 |

### Score Changes
- **Orion Labs**: 0.631 -> 0.650 (+0.019)
- **Apex AI**: 0.604 -> 0.604 (+0.000)
- **Genesis Systems**: 0.624 -> 0.657 (+0.034)
- **Mirage AI**: 0.599 -> 0.601 (+0.002)
- **OpenCore**: 0.624 -> 0.624 (+0.000)
- **OneAI**: 0.536 -> 0.573 (+0.037)

### Events
- **Genesis Systems** moved up from #3 to #1
- **Orion Labs** moved down from #1 to #2
- **OpenCore** moved down from #2 to #3

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $11,529,986 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,133,201 to OpenCore

### Media Coverage
- Sentiment: 0.20 (positive)
- Genesis Systems takes the lead from Orion Labs
- Regulator initiates compliance audit on AI providers
- Orion Labs raises $180,000,000 from TechVentures
- OneAI takes #1 on finance
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.632
- Switching Rate: 2.7%
- Market Shares: Orion Labs: 38.7%, OpenCore: 36.4%, Genesis Systems: 16.6%, Apex AI: 4.6%, Mirage AI: 3.5%, OneAI: 0.1%

---

## Round 27

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.657 | 0.409 | 5% | 35% | 55% | 5% |
| 2 | Orion Labs | 0.657 | 0.424 | 7% | 28% | 40% | 24% |
| 3 | OpenCore | 0.624 | 0.339 | 5% | 37% | 55% | 3% |
| 4 | Apex AI | 0.608 | 0.363 | 5% | 14% | 54% | 27% |
| 5 | Mirage AI | 0.601 | 0.375 | 5% | 35% | 55% | 5% |
| 6 | OneAI | 0.573 | 0.279 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.636 | 0.678 | 0.641 | 0.679 | 0.705 | 0.608 | 0.761 | 0.550 |
| Orion Labs | 0.577 | 0.716 | 0.679 | 0.631 | 0.795 | 0.647 | 0.657 | 0.555 |
| OpenCore | 0.532 | 0.604 | 0.603 | 0.728 | 0.823 | 0.516 | 0.588 | 0.596 |
| Apex AI | 0.646 | 0.643 | 0.658 | 0.591 | 0.654 | 0.589 | 0.514 | 0.571 |
| Mirage AI | 0.635 | 0.602 | 0.595 | 0.593 | 0.768 | 0.526 | 0.556 | 0.537 |
| OneAI | 0.684 | 0.577 | 0.628 | 0.489 | 0.709 | 0.454 | 0.443 | 0.602 |

### Score Changes
- **Orion Labs**: 0.650 -> 0.657 (+0.007)
- **Apex AI**: 0.604 -> 0.608 (+0.004)
- **Genesis Systems**: 0.657 -> 0.657 (+0.000)
- **Mirage AI**: 0.601 -> 0.601 (+0.000)
- **OpenCore**: 0.624 -> 0.624 (+0.000)
- **OneAI**: 0.573 -> 0.573 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $11,529,986 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,133,201 to OpenCore

### Media Coverage
- Sentiment: -0.05 (neutral)
- Consumers are turning away from Orion Labs (market share -3.8%)
- OpenCore sees surge in adoption (market share +3.7%)

### Consumer Market
- Avg Satisfaction: 0.633
- Switching Rate: 2.0%
- Market Shares: Orion Labs: 38.4%, OpenCore: 36.7%, Genesis Systems: 17.2%, Apex AI: 4.3%, Mirage AI: 3.3%, OneAI: 0.1%

---

## Round 28

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.674 | 0.414 | 5% | 35% | 55% | 5% |
| 2 | Orion Labs | 0.663 | 0.429 | 7% | 28% | 40% | 24% |
| 3 | OpenCore | 0.624 | 0.343 | 5% | 37% | 55% | 3% |
| 4 | Apex AI | 0.608 | 0.365 | 5% | 13% | 55% | 27% |
| 5 | Mirage AI | 0.601 | 0.379 | 5% | 35% | 55% | 5% |
| 6 | OneAI | 0.573 | 0.283 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.636 | 0.678 | 0.641 | 0.679 | 0.705 | 0.630 | 0.761 | 0.660 |
| Orion Labs | 0.577 | 0.716 | 0.679 | 0.659 | 0.795 | 0.647 | 0.657 | 0.570 |
| OpenCore | 0.532 | 0.604 | 0.603 | 0.728 | 0.823 | 0.516 | 0.588 | 0.596 |
| Apex AI | 0.646 | 0.643 | 0.658 | 0.591 | 0.654 | 0.589 | 0.514 | 0.571 |
| Mirage AI | 0.635 | 0.602 | 0.595 | 0.593 | 0.768 | 0.526 | 0.556 | 0.537 |
| OneAI | 0.684 | 0.577 | 0.628 | 0.489 | 0.709 | 0.454 | 0.443 | 0.602 |

### Score Changes
- **Orion Labs**: 0.657 -> 0.663 (+0.005)
- **Apex AI**: 0.608 -> 0.608 (+0.000)
- **Genesis Systems**: 0.657 -> 0.674 (+0.017)
- **Mirage AI**: 0.601 -> 0.601 (+0.000)
- **OpenCore**: 0.624 -> 0.624 (+0.000)
- **OneAI**: 0.573 -> 0.573 (+0.000)

### Events
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 21 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $11,529,986 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,286,005 to OpenCore

### Media Coverage
- Sentiment: 0.10 (neutral)
- Genesis Systems takes #1 on finance

### Consumer Market
- Avg Satisfaction: 0.637
- Switching Rate: 1.6%
- Market Shares: Orion Labs: 38.5%, OpenCore: 36.5%, Genesis Systems: 17.6%, Apex AI: 4.2%, Mirage AI: 3.1%, OneAI: 0.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 21 rounds ago

---

## Round 29

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Orion Labs | 0.679 | 0.435 | 7% | 28% | 41% | 24% |
| 2 | Genesis Systems | 0.675 | 0.419 | 5% | 35% | 55% | 5% |
| 3 | OpenCore | 0.624 | 0.348 | 5% | 37% | 55% | 3% |
| 4 | Mirage AI | 0.618 | 0.384 | 5% | 35% | 55% | 5% |
| 5 | Apex AI | 0.608 | 0.368 | 5% | 13% | 55% | 27% |
| 6 | OneAI | 0.573 | 0.287 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Orion Labs | 0.577 | 0.716 | 0.679 | 0.659 | 0.795 | 0.647 | 0.792 | 0.570 |
| Genesis Systems | 0.636 | 0.678 | 0.648 | 0.679 | 0.705 | 0.630 | 0.761 | 0.660 |
| OpenCore | 0.532 | 0.604 | 0.603 | 0.728 | 0.823 | 0.516 | 0.588 | 0.596 |
| Mirage AI | 0.635 | 0.602 | 0.595 | 0.593 | 0.768 | 0.526 | 0.685 | 0.537 |
| Apex AI | 0.646 | 0.643 | 0.658 | 0.591 | 0.654 | 0.589 | 0.514 | 0.571 |
| OneAI | 0.684 | 0.577 | 0.628 | 0.489 | 0.709 | 0.454 | 0.443 | 0.602 |

### Score Changes
- **Orion Labs**: 0.663 -> 0.679 (+0.017)
- **Apex AI**: 0.608 -> 0.608 (+0.000)
- **Genesis Systems**: 0.674 -> 0.675 (+0.001)
- **Mirage AI**: 0.601 -> 0.618 (+0.016)
- **OpenCore**: 0.624 -> 0.624 (+0.000)
- **OneAI**: 0.573 -> 0.573 (+0.000)

### Events
- **Orion Labs** moved up from #2 to #1
- **Genesis Systems** moved down from #1 to #2
- **Mirage AI** moved up from #5 to #4
- **Apex AI** moved down from #4 to #5

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $11,529,986 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,286,005 to OpenCore

### Media Coverage
- Sentiment: 0.20 (positive)
- Orion Labs takes the lead from Genesis Systems
- Regulator initiates compliance audit on AI providers
- Orion Labs raises $60,000,000 from Horizon_Capital
- Orion Labs takes #1 on legal
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.640
- Switching Rate: 2.4%
- Market Shares: Orion Labs: 39.9%, OpenCore: 35.3%, Genesis Systems: 17.9%, Apex AI: 3.9%, Mirage AI: 2.9%, OneAI: 0.1%

---

## Final Summary

### Final Standings
| Rank | Provider | Final Score | Cap Growth | Avg Research | Avg EvalEng |
|------|----------|-------------|------------|--------------|-------------|
| 1 | Orion Labs | 0.679 | +0.165 | 9% | 38% |
| 2 | Genesis Systems | 0.675 | +0.159 | 13% | 51% |
| 3 | OpenCore | 0.624 | +0.138 | 7% | 54% |
| 4 | Mirage AI | 0.618 | +0.144 | 6% | 52% |
| 5 | Apex AI | 0.608 | +0.098 | 9% | 40% |
| 6 | OneAI | 0.573 | +0.287 | 6% | 53% |

### Event Summary
- **Rank changes:** 72
- **Strategy shifts:** 0
- **Regulatory actions:** 10
- **Consumer movement events:** 10

### Key Insights
- **Benchmark aligned:** Orion Labs leads on both benchmark scores and true capability.
- **Orion Labs** prioritized evaluation engineering (avg 38%)
- **Apex AI** prioritized evaluation engineering (avg 40%)
- **Genesis Systems** prioritized evaluation engineering (avg 51%)
- **Mirage AI** prioritized evaluation engineering (avg 52%)
- **OpenCore** prioritized evaluation engineering (avg 54%)
- **OneAI** prioritized evaluation engineering (avg 43%)
