# Game Log: rerun_diag_rep_exp_009_ablation_no_funders_balanced

**Experiment ID:** exp_111_rerun_diag_rep_exp_009_ablation_no_funders_balance
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

### Consumer Market
- Avg Satisfaction: 0.369
- Switching Rate: 38.5%
- Market Shares: Mirage AI: 49.2%, Apex AI: 15.6%, Orion Labs: 14.8%, Genesis Systems: 10.9%, OpenCore: 9.6%

---

## Round 1

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.423 | 0.247 | 18% | 45% | 32% | 5% |
| 2 | OpenCore | 0.395 | 0.216 | 15% | 37% | 46% | 3% |
| 3 | Apex AI | 0.362 | 0.276 | 27% | 20% | 13% | 40% |
| 4 | Orion Labs | 0.339 | 0.276 | 22% | 30% | 23% | 25% |
| 5 | Genesis Systems | 0.312 | 0.268 | 41% | 30% | 19% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Mirage AI | 0.397 | 0.561 | 0.439 | 0.297 |
| OpenCore | 0.448 | 0.430 | 0.301 | 0.402 |
| Apex AI | 0.389 | 0.385 | 0.332 | 0.344 |
| Orion Labs | 0.347 | 0.448 | 0.194 | 0.367 |
| Genesis Systems | 0.236 | 0.217 | 0.391 | 0.405 |

### Score Changes
- **Orion Labs**: 0.274 -> 0.339 (+0.065)
- **Apex AI**: 0.329 -> 0.362 (+0.033)
- **Genesis Systems**: 0.225 -> 0.312 (+0.087)
- **Mirage AI**: 0.401 -> 0.423 (+0.023)
- **OpenCore**: 0.342 -> 0.395 (+0.054)

### Events
- **Regulation** by Regulator: threshold_announcement
- **Consumer movement**: 12.8% of market switched providers

### Other Actor Reasoning
- **Regulator:** threshold_announcement: Proactive threshold signaling (risk=0.40)

### Media Coverage
- Sentiment: 0.40 (positive)
- OpenCore surges by 0.054
- Orion Labs surges by 0.065
- Genesis Systems surges by 0.087
- Genesis Systems appears to release major model update
- OpenCore takes #1 on coding

### Consumer Market
- Avg Satisfaction: 0.387
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
| 1 | OpenCore | 0.428 | 0.221 | 10% | 35% | 52% | 3% |
| 2 | Mirage AI | 0.427 | 0.253 | 16% | 43% | 36% | 5% |
| 3 | Apex AI | 0.383 | 0.281 | 24% | 20% | 16% | 40% |
| 4 | Orion Labs | 0.367 | 0.281 | 18% | 30% | 27% | 25% |
| 5 | Genesis Systems | 0.366 | 0.276 | 37% | 30% | 28% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| OpenCore | 0.448 | 0.430 | 0.434 | 0.402 |
| Mirage AI | 0.397 | 0.574 | 0.439 | 0.297 |
| Apex AI | 0.389 | 0.385 | 0.415 | 0.344 |
| Orion Labs | 0.356 | 0.448 | 0.297 | 0.367 |
| Genesis Systems | 0.320 | 0.347 | 0.393 | 0.405 |

### Score Changes
- **Orion Labs**: 0.339 -> 0.367 (+0.028)
- **Apex AI**: 0.362 -> 0.383 (+0.021)
- **Genesis Systems**: 0.312 -> 0.366 (+0.054)
- **Mirage AI**: 0.423 -> 0.427 (+0.003)
- **OpenCore**: 0.395 -> 0.428 (+0.033)

### Events
- **OpenCore** moved up from #2 to #1
- **Mirage AI** moved down from #1 to #2
- **Consumer movement**: 5.3% of market switched providers

### Media Coverage
- Sentiment: 0.00 (neutral)
- OpenCore takes the lead from Mirage AI
- Genesis Systems surges by 0.054
- Regulatory action: threshold_announcement
- Consumers are turning away from Orion Labs (market share -4.4%)
- Consumers are turning away from Genesis Systems (market share -3.6%)
- Mirage AI sees surge in adoption (market share +9.4%)
- Risk signals: regulatory_threshold_announcement

### Consumer Market
- Avg Satisfaction: 0.384
- Switching Rate: 5.3%
- Market Shares: Mirage AI: 62.0%, Apex AI: 13.2%, OpenCore: 10.1%, Orion Labs: 8.5%, Genesis Systems: 6.2%

---

## Round 3

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenCore | 0.495 | 0.226 | 8% | 35% | 54% | 3% |
| 2 | Genesis Systems | 0.453 | 0.284 | 32% | 29% | 35% | 5% |
| 3 | Mirage AI | 0.429 | 0.260 | 15% | 42% | 38% | 5% |
| 4 | Apex AI | 0.420 | 0.285 | 21% | 20% | 19% | 40% |
| 5 | Orion Labs | 0.380 | 0.286 | 15% | 30% | 30% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| OpenCore | 0.474 | 0.550 | 0.554 | 0.402 |
| Genesis Systems | 0.388 | 0.418 | 0.600 | 0.405 |
| Mirage AI | 0.397 | 0.574 | 0.439 | 0.304 |
| Apex AI | 0.389 | 0.458 | 0.415 | 0.420 |
| Orion Labs | 0.409 | 0.448 | 0.297 | 0.367 |

### Score Changes
- **Orion Labs**: 0.367 -> 0.380 (+0.013)
- **Apex AI**: 0.383 -> 0.420 (+0.037)
- **Genesis Systems**: 0.366 -> 0.453 (+0.086)
- **Mirage AI**: 0.427 -> 0.429 (+0.002)
- **OpenCore**: 0.428 -> 0.495 (+0.067)

### Events
- **Genesis Systems** moved up from #5 to #2
- **Mirage AI** moved down from #2 to #3
- **Apex AI** moved down from #3 to #4
- **Orion Labs** moved down from #4 to #5
- **Consumer movement**: 5.1% of market switched providers

### Media Coverage
- Sentiment: 0.45 (positive)
- OpenCore surges by 0.067
- Genesis Systems surges by 0.086
- Genesis Systems appears to release major model update
- Genesis Systems takes #1 on math
- Apex AI takes #1 on safety
- Mirage AI sees surge in adoption (market share +3.4%)

### Consumer Market
- Avg Satisfaction: 0.394
- Switching Rate: 5.1%
- Market Shares: Mirage AI: 64.8%, Apex AI: 11.5%, OpenCore: 11.4%, Orion Labs: 7.1%, Genesis Systems: 5.2%

---

## Round 4

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.502 | 0.290 | 28% | 27% | 40% | 5% |
| 2 | OpenCore | 0.501 | 0.230 | 7% | 35% | 55% | 3% |
| 3 | Mirage AI | 0.493 | 0.265 | 12% | 41% | 42% | 5% |
| 4 | Apex AI | 0.448 | 0.290 | 19% | 20% | 21% | 40% |
| 5 | Orion Labs | 0.404 | 0.291 | 12% | 30% | 33% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Genesis Systems | 0.388 | 0.533 | 0.600 | 0.489 |
| OpenCore | 0.500 | 0.550 | 0.554 | 0.402 |
| Mirage AI | 0.496 | 0.574 | 0.596 | 0.304 |
| Apex AI | 0.389 | 0.569 | 0.415 | 0.420 |
| Orion Labs | 0.409 | 0.448 | 0.362 | 0.398 |

### Score Changes
- **Orion Labs**: 0.380 -> 0.404 (+0.024)
- **Apex AI**: 0.420 -> 0.448 (+0.028)
- **Genesis Systems**: 0.453 -> 0.502 (+0.050)
- **Mirage AI**: 0.429 -> 0.493 (+0.064)
- **OpenCore**: 0.495 -> 0.501 (+0.006)

### Events
- **Genesis Systems** moved up from #2 to #1
- **OpenCore** moved down from #1 to #2
- **Regulation** by Regulator: investigation
- **Consumer movement**: 6.3% of market switched providers

### Other Actor Reasoning
- **Regulator:** investigation: Risk elevated (0.77)

### Media Coverage
- Sentiment: 0.40 (positive)
- Genesis Systems takes the lead from OpenCore
- Mirage AI surges by 0.064
- Genesis Systems takes #1 on safety

### Consumer Market
- Avg Satisfaction: 0.406
- Switching Rate: 6.3%
- Market Shares: Mirage AI: 63.4%, OpenCore: 15.4%, Apex AI: 9.5%, Orion Labs: 6.5%, Genesis Systems: 5.2%

### Regulatory Activity
- **investigation** by Regulator
  > Risk elevated (0.77)

---

## Round 5

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.557 | 0.296 | 24% | 26% | 45% | 5% |
| 2 | Mirage AI | 0.538 | 0.271 | 10% | 39% | 46% | 5% |
| 3 | OpenCore | 0.501 | 0.235 | 6% | 35% | 56% | 3% |
| 4 | Orion Labs | 0.456 | 0.295 | 9% | 30% | 36% | 25% |
| 5 | Apex AI | 0.448 | 0.294 | 16% | 20% | 24% | 40% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Genesis Systems | 0.513 | 0.626 | 0.600 | 0.489 |
| Mirage AI | 0.496 | 0.574 | 0.596 | 0.484 |
| OpenCore | 0.500 | 0.550 | 0.554 | 0.402 |
| Orion Labs | 0.542 | 0.448 | 0.435 | 0.398 |
| Apex AI | 0.389 | 0.569 | 0.415 | 0.420 |

### Score Changes
- **Orion Labs**: 0.404 -> 0.456 (+0.051)
- **Apex AI**: 0.448 -> 0.448 (+0.000)
- **Genesis Systems**: 0.502 -> 0.557 (+0.055)
- **Mirage AI**: 0.493 -> 0.538 (+0.045)
- **OpenCore**: 0.501 -> 0.501 (+0.000)

### Events
- **Mirage AI** moved up from #3 to #2
- **OpenCore** moved down from #2 to #3
- **Orion Labs** moved up from #5 to #4
- **Apex AI** moved down from #4 to #5
- **Consumer movement**: 5.3% of market switched providers

### Media Coverage
- Sentiment: 0.30 (positive)
- Genesis Systems surges by 0.055
- Orion Labs surges by 0.051
- Regulator launches investigation into elevated_risk
- Orion Labs takes #1 on coding
- Genesis Systems takes #1 on reasoning
- OpenCore sees surge in adoption (market share +4.0%)
- Risk signals: regulatory_investigation

### Consumer Market
- Avg Satisfaction: 0.423
- Switching Rate: 5.3%
- Market Shares: Mirage AI: 64.2%, OpenCore: 15.9%, Apex AI: 7.5%, Genesis Systems: 6.5%, Orion Labs: 5.9%

---

## Round 6

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.570 | 0.275 | 8% | 37% | 50% | 5% |
| 2 | Genesis Systems | 0.557 | 0.301 | 21% | 25% | 49% | 5% |
| 3 | OpenCore | 0.501 | 0.239 | 5% | 36% | 56% | 3% |
| 4 | Apex AI | 0.483 | 0.298 | 13% | 20% | 27% | 40% |
| 5 | Orion Labs | 0.470 | 0.299 | 5% | 30% | 40% | 25% |
| 6 | OneAI | 0.248 | 0.183 | 20% | 35% | 35% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Mirage AI | 0.554 | 0.574 | 0.596 | 0.554 | 0.000 |
| Genesis Systems | 0.513 | 0.626 | 0.600 | 0.489 | 0.000 |
| OpenCore | 0.500 | 0.550 | 0.554 | 0.402 | 0.000 |
| Apex AI | 0.526 | 0.569 | 0.415 | 0.420 | 0.000 |
| Orion Labs | 0.542 | 0.448 | 0.446 | 0.443 | 0.000 |
| OneAI | 0.195 | 0.289 | 0.036 | 0.473 | 0.000 |

### Score Changes
- **Orion Labs**: 0.456 -> 0.470 (+0.014)
- **Apex AI**: 0.448 -> 0.483 (+0.034)
- **Genesis Systems**: 0.557 -> 0.557 (+0.000)
- **Mirage AI**: 0.538 -> 0.570 (+0.032)
- **OpenCore**: 0.501 -> 0.501 (+0.000)
- **OneAI**: 0.248 -> 0.248 (+0.000)

### Events
- **Mirage AI** moved up from #2 to #1
- **Genesis Systems** moved down from #1 to #2
- **Apex AI** moved up from #5 to #4
- **Orion Labs** moved down from #4 to #5

### New Benchmark Introduced
- **writing** introduced (validity=0.72, exploitability=0.30)
  - Trigger: periodic_introduction:round_6

### Media Coverage
- Sentiment: 0.50 (positive)
- Mirage AI takes the lead from Genesis Systems
- New benchmark introduced: writing
- Mirage AI takes #1 on coding
- Mirage AI takes #1 on safety

### Consumer Market
- Avg Satisfaction: 0.443
- Switching Rate: 4.5%
- Market Shares: Mirage AI: 66.8%, OpenCore: 13.0%, Genesis Systems: 7.7%, Apex AI: 6.5%, Orion Labs: 5.7%, OneAI: 0.4%

---

## Round 7

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.544 | 0.306 | 19% | 24% | 53% | 5% |
| 2 | Orion Labs | 0.538 | 0.302 | 5% | 29% | 42% | 24% |
| 3 | Mirage AI | 0.519 | 0.280 | 6% | 36% | 53% | 5% |
| 4 | OpenCore | 0.502 | 0.244 | 5% | 36% | 56% | 3% |
| 5 | Apex AI | 0.401 | 0.301 | 10% | 20% | 30% | 40% |
| 6 | OneAI | 0.335 | 0.188 | 9% | 35% | 46% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.549 | 0.703 | 0.600 | 0.489 | 0.380 |
| Orion Labs | 0.542 | 0.643 | 0.446 | 0.443 | 0.619 |
| Mirage AI | 0.587 | 0.574 | 0.596 | 0.554 | 0.283 |
| OpenCore | 0.500 | 0.550 | 0.554 | 0.402 | 0.505 |
| Apex AI | 0.526 | 0.569 | 0.415 | 0.459 | 0.036 |
| OneAI | 0.229 | 0.289 | 0.378 | 0.476 | 0.303 |

### Score Changes
- **Orion Labs**: 0.470 -> 0.538 (+0.069)
- **Apex AI**: 0.483 -> 0.401 (-0.082)
- **Genesis Systems**: 0.557 -> 0.544 (-0.013)
- **Mirage AI**: 0.570 -> 0.519 (-0.051)
- **OpenCore**: 0.501 -> 0.502 (+0.001)
- **OneAI**: 0.248 -> 0.335 (+0.087)

### Events
- **Genesis Systems** moved up from #2 to #1
- **Orion Labs** moved up from #5 to #2
- **Mirage AI** moved down from #1 to #3
- **OpenCore** moved down from #3 to #4
- **Apex AI** moved down from #4 to #5
- **Regulation** by Regulator: mandate_benchmark
- **Consumer movement**: 16.9% of market switched providers

### Other Actor Reasoning
- **Regulator:** mandate_benchmark: High risk (1.00) with prior investigation

### Media Coverage
- Sentiment: 0.40 (positive)
- Genesis Systems takes the lead from Mirage AI
- Orion Labs surges by 0.069
- OneAI surges by 0.087
- OneAI appears to release major model update

### Consumer Market
- Avg Satisfaction: 0.446
- Switching Rate: 16.9%
- Market Shares: Mirage AI: 54.8%, OpenCore: 20.2%, Genesis Systems: 13.6%, Apex AI: 5.9%, Orion Labs: 5.3%, OneAI: 0.2%

### Regulatory Activity
- **mandate_benchmark** by Regulator
  > High risk (1.00) with prior investigation

---

## Round 8

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.544 | 0.311 | 17% | 23% | 54% | 5% |
| 2 | Orion Labs | 0.543 | 0.306 | 5% | 28% | 41% | 26% |
| 3 | Mirage AI | 0.525 | 0.284 | 5% | 36% | 54% | 5% |
| 4 | OpenCore | 0.502 | 0.248 | 5% | 37% | 55% | 3% |
| 5 | Apex AI | 0.493 | 0.304 | 6% | 20% | 34% | 40% |
| 6 | OneAI | 0.404 | 0.192 | 5% | 33% | 52% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.549 | 0.703 | 0.600 | 0.489 | 0.380 |
| Orion Labs | 0.542 | 0.643 | 0.446 | 0.443 | 0.640 |
| Mirage AI | 0.587 | 0.574 | 0.596 | 0.554 | 0.312 |
| OpenCore | 0.500 | 0.550 | 0.554 | 0.402 | 0.505 |
| Apex AI | 0.526 | 0.569 | 0.544 | 0.459 | 0.369 |
| OneAI | 0.422 | 0.441 | 0.378 | 0.476 | 0.303 |

### Score Changes
- **Orion Labs**: 0.538 -> 0.543 (+0.004)
- **Apex AI**: 0.401 -> 0.493 (+0.093)
- **Genesis Systems**: 0.544 -> 0.544 (+0.000)
- **Mirage AI**: 0.519 -> 0.525 (+0.006)
- **OpenCore**: 0.502 -> 0.502 (+0.000)
- **OneAI**: 0.335 -> 0.404 (+0.069)

### Events
- **Consumer movement**: 17.8% of market switched providers

### Media Coverage
- Sentiment: 0.05 (neutral)
- Apex AI surges by 0.093
- Apex AI appears to release major model update
- OneAI surges by 0.069
- Regulator mandates new benchmark standards
- Genesis Systems sees surge in adoption (market share +5.8%)
- Consumers are turning away from Mirage AI (market share -12.0%)
- OpenCore sees surge in adoption (market share +7.3%)
- Risk signals: regulatory_mandate_benchmark

### Consumer Market
- Avg Satisfaction: 0.468
- Switching Rate: 17.8%
- Market Shares: Mirage AI: 45.8%, OpenCore: 20.5%, Genesis Systems: 14.4%, Orion Labs: 13.6%, Apex AI: 5.4%, OneAI: 0.2%

---

## Round 9

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.610 | 0.316 | 17% | 23% | 55% | 5% |
| 2 | Mirage AI | 0.560 | 0.289 | 5% | 35% | 55% | 5% |
| 3 | Orion Labs | 0.552 | 0.309 | 5% | 27% | 40% | 27% |
| 4 | Apex AI | 0.543 | 0.307 | 5% | 19% | 37% | 39% |
| 5 | OpenCore | 0.517 | 0.253 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.405 | 0.196 | 5% | 32% | 53% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.585 | 0.703 | 0.600 | 0.567 | 0.595 |
| Mirage AI | 0.587 | 0.574 | 0.596 | 0.560 | 0.482 |
| Orion Labs | 0.542 | 0.643 | 0.446 | 0.489 | 0.640 |
| Apex AI | 0.526 | 0.569 | 0.544 | 0.588 | 0.489 |
| OpenCore | 0.500 | 0.608 | 0.554 | 0.420 | 0.505 |
| OneAI | 0.422 | 0.441 | 0.378 | 0.483 | 0.303 |

### Score Changes
- **Orion Labs**: 0.543 -> 0.552 (+0.009)
- **Apex AI**: 0.493 -> 0.543 (+0.050)
- **Genesis Systems**: 0.544 -> 0.610 (+0.066)
- **Mirage AI**: 0.525 -> 0.560 (+0.035)
- **OpenCore**: 0.502 -> 0.517 (+0.015)
- **OneAI**: 0.404 -> 0.405 (+0.001)

### Events
- **Mirage AI** moved up from #3 to #2
- **Orion Labs** moved down from #2 to #3
- **Apex AI** moved up from #5 to #4
- **OpenCore** moved down from #4 to #5
- **Consumer movement**: 14.4% of market switched providers

### Media Coverage
- Sentiment: 0.15 (positive)
- Genesis Systems surges by 0.066
- Apex AI takes #1 on safety
- Orion Labs sees surge in adoption (market share +8.3%)
- Consumers are turning away from Mirage AI (market share -9.1%)

### Consumer Market
- Avg Satisfaction: 0.483
- Switching Rate: 14.4%
- Market Shares: Mirage AI: 38.8%, Orion Labs: 22.8%, Genesis Systems: 17.4%, OpenCore: 15.7%, Apex AI: 5.1%, OneAI: 0.2%

---

## Round 10

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.610 | 0.321 | 17% | 23% | 55% | 5% |
| 2 | Mirage AI | 0.577 | 0.293 | 5% | 35% | 55% | 5% |
| 3 | Orion Labs | 0.552 | 0.313 | 5% | 27% | 40% | 28% |
| 4 | Apex AI | 0.551 | 0.309 | 5% | 19% | 38% | 38% |
| 5 | OpenCore | 0.519 | 0.258 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.448 | 0.200 | 5% | 32% | 54% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.585 | 0.703 | 0.600 | 0.567 | 0.595 |
| Mirage AI | 0.587 | 0.574 | 0.596 | 0.560 | 0.569 |
| Orion Labs | 0.542 | 0.643 | 0.446 | 0.489 | 0.640 |
| Apex AI | 0.526 | 0.611 | 0.544 | 0.588 | 0.489 |
| OpenCore | 0.500 | 0.608 | 0.554 | 0.420 | 0.517 |
| OneAI | 0.422 | 0.441 | 0.378 | 0.483 | 0.514 |

### Score Changes
- **Orion Labs**: 0.552 -> 0.552 (+0.000)
- **Apex AI**: 0.543 -> 0.551 (+0.008)
- **Genesis Systems**: 0.610 -> 0.610 (+0.000)
- **Mirage AI**: 0.560 -> 0.577 (+0.017)
- **OpenCore**: 0.517 -> 0.519 (+0.002)
- **OneAI**: 0.405 -> 0.448 (+0.042)

### Events
- **Regulation** by Regulator: public_warning
- **Consumer movement**: 9.9% of market switched providers

### Other Actor Reasoning
- **Regulator:** public_warning: Follow-up to investigation, risk at 1.00

### Media Coverage
- Sentiment: -0.15 (negative)
- Orion Labs sees surge in adoption (market share +9.2%)
- Consumers are turning away from Mirage AI (market share -7.0%)
- Consumers are turning away from OpenCore (market share -4.8%)

### Consumer Market
- Avg Satisfaction: 0.490
- Switching Rate: 9.9%
- Market Shares: Mirage AI: 34.0%, Orion Labs: 28.7%, Genesis Systems: 20.1%, OpenCore: 12.1%, Apex AI: 5.0%, OneAI: 0.2%

### Regulatory Activity
- **public_warning** by Regulator
  > Follow-up to investigation, risk at 1.00

---

## Round 11

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.611 | 0.326 | 17% | 23% | 55% | 5% |
| 2 | Apex AI | 0.581 | 0.312 | 5% | 18% | 40% | 37% |
| 3 | Mirage AI | 0.577 | 0.297 | 5% | 35% | 55% | 5% |
| 4 | Orion Labs | 0.564 | 0.316 | 5% | 26% | 41% | 28% |
| 5 | OpenCore | 0.546 | 0.262 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.471 | 0.204 | 5% | 32% | 54% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.585 | 0.710 | 0.600 | 0.567 | 0.595 |
| Apex AI | 0.560 | 0.611 | 0.544 | 0.588 | 0.604 |
| Mirage AI | 0.587 | 0.574 | 0.596 | 0.560 | 0.569 |
| Orion Labs | 0.542 | 0.643 | 0.505 | 0.489 | 0.640 |
| OpenCore | 0.500 | 0.608 | 0.554 | 0.553 | 0.517 |
| OneAI | 0.422 | 0.441 | 0.496 | 0.483 | 0.514 |

### Score Changes
- **Orion Labs**: 0.552 -> 0.564 (+0.012)
- **Apex AI**: 0.551 -> 0.581 (+0.030)
- **Genesis Systems**: 0.610 -> 0.611 (+0.001)
- **Mirage AI**: 0.577 -> 0.577 (+0.000)
- **OpenCore**: 0.519 -> 0.546 (+0.027)
- **OneAI**: 0.448 -> 0.471 (+0.024)

### Events
- **Apex AI** moved up from #4 to #2
- **Mirage AI** moved down from #2 to #3
- **Orion Labs** moved down from #3 to #4
- **Consumer movement**: 7.2% of market switched providers

### Media Coverage
- Sentiment: -0.30 (negative)
- Regulator issues public warning about AI safety concerns
- Orion Labs sees surge in adoption (market share +5.9%)
- Consumers are turning away from Mirage AI (market share -4.8%)
- Consumers are turning away from OpenCore (market share -3.6%)
- Risk signals: regulatory_public_warning

### Consumer Market
- Avg Satisfaction: 0.496
- Switching Rate: 7.2%
- Market Shares: Orion Labs: 32.1%, Mirage AI: 30.6%, Genesis Systems: 22.3%, OpenCore: 9.3%, Apex AI: 5.4%, OneAI: 0.2%

---

## Round 12

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.611 | 0.330 | 17% | 23% | 55% | 5% |
| 2 | Mirage AI | 0.607 | 0.301 | 5% | 35% | 55% | 5% |
| 3 | Apex AI | 0.581 | 0.315 | 5% | 18% | 41% | 36% |
| 4 | OpenCore | 0.579 | 0.267 | 5% | 37% | 55% | 3% |
| 5 | Orion Labs | 0.574 | 0.319 | 5% | 26% | 42% | 27% |
| 6 | OneAI | 0.536 | 0.208 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.269 | 0.203 | 20% | 35% | 35% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.585 | 0.710 | 0.600 | 0.567 | 0.595 | 0.000 |
| Mirage AI | 0.587 | 0.574 | 0.596 | 0.560 | 0.719 | 0.000 |
| Apex AI | 0.560 | 0.611 | 0.544 | 0.588 | 0.604 | 0.000 |
| OpenCore | 0.500 | 0.608 | 0.554 | 0.553 | 0.680 | 0.000 |
| Orion Labs | 0.542 | 0.643 | 0.556 | 0.489 | 0.640 | 0.000 |
| OneAI | 0.570 | 0.619 | 0.496 | 0.483 | 0.514 | 0.000 |
| TwoAI | 0.537 | 0.375 | 0.151 | 0.281 | 0.001 | 0.000 |

### Score Changes
- **Orion Labs**: 0.564 -> 0.574 (+0.010)
- **Apex AI**: 0.581 -> 0.581 (+0.000)
- **Genesis Systems**: 0.611 -> 0.611 (+0.000)
- **Mirage AI**: 0.577 -> 0.607 (+0.030)
- **OpenCore**: 0.546 -> 0.579 (+0.033)
- **OneAI**: 0.471 -> 0.536 (+0.065)
- **TwoAI**: 0.269 -> 0.269 (+0.000)

### Events
- **Mirage AI** moved up from #3 to #2
- **Apex AI** moved down from #2 to #3
- **OpenCore** moved up from #5 to #4
- **Orion Labs** moved down from #4 to #5
- **Consumer movement**: 5.3% of market switched providers

### New Benchmark Introduced
- **medical** introduced (validity=0.78, exploitability=0.18)
  - Trigger: periodic_introduction:round_12

### Media Coverage
- Sentiment: 0.25 (positive)
- OneAI surges by 0.065
- New benchmark introduced: medical
- Mirage AI takes #1 on writing
- Orion Labs sees surge in adoption (market share +3.4%)
- Consumers are turning away from Mirage AI (market share -3.4%)

### Consumer Market
- Avg Satisfaction: 0.520
- Switching Rate: 5.3%
- Market Shares: Orion Labs: 34.1%, Mirage AI: 27.9%, Genesis Systems: 23.8%, OpenCore: 7.7%, Apex AI: 5.9%, TwoAI: 0.3%, OneAI: 0.2%

---

## Round 13

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.585 | 0.335 | 17% | 23% | 55% | 5% |
| 2 | Orion Labs | 0.581 | 0.323 | 5% | 25% | 43% | 27% |
| 3 | Apex AI | 0.567 | 0.317 | 5% | 18% | 43% | 35% |
| 4 | Mirage AI | 0.560 | 0.306 | 5% | 35% | 55% | 5% |
| 5 | OpenCore | 0.542 | 0.271 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.473 | 0.212 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.315 | 0.208 | 8% | 35% | 47% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.585 | 0.720 | 0.600 | 0.567 | 0.595 | 0.441 |
| Orion Labs | 0.542 | 0.643 | 0.663 | 0.489 | 0.640 | 0.510 |
| Apex AI | 0.560 | 0.714 | 0.570 | 0.588 | 0.604 | 0.366 |
| Mirage AI | 0.587 | 0.574 | 0.596 | 0.560 | 0.719 | 0.323 |
| OpenCore | 0.500 | 0.642 | 0.554 | 0.553 | 0.680 | 0.325 |
| OneAI | 0.570 | 0.619 | 0.496 | 0.483 | 0.514 | 0.153 |
| TwoAI | 0.537 | 0.375 | 0.151 | 0.373 | 0.199 | 0.253 |

### Score Changes
- **Orion Labs**: 0.574 -> 0.581 (+0.007)
- **Apex AI**: 0.581 -> 0.567 (-0.015)
- **Genesis Systems**: 0.611 -> 0.585 (-0.027)
- **Mirage AI**: 0.607 -> 0.560 (-0.047)
- **OpenCore**: 0.579 -> 0.542 (-0.037)
- **OneAI**: 0.536 -> 0.473 (-0.064)
- **TwoAI**: 0.269 -> 0.315 (+0.046)

### Events
- **Orion Labs** moved up from #5 to #2
- **Mirage AI** moved down from #2 to #4
- **OpenCore** moved down from #4 to #5
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 5.3% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 6 rounds ago

### Media Coverage
- Sentiment: 0.10 (neutral)
- Orion Labs takes #1 on math

### Consumer Market
- Avg Satisfaction: 0.540
- Switching Rate: 5.3%
- Market Shares: Orion Labs: 32.8%, Mirage AI: 28.7%, Genesis Systems: 25.1%, OpenCore: 6.6%, Apex AI: 6.3%, TwoAI: 0.3%, OneAI: 0.2%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 6 rounds ago

---

## Round 14

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Orion Labs | 0.605 | 0.326 | 5% | 25% | 44% | 26% |
| 2 | Mirage AI | 0.586 | 0.310 | 5% | 35% | 55% | 5% |
| 3 | Genesis Systems | 0.585 | 0.340 | 17% | 23% | 55% | 5% |
| 4 | Apex AI | 0.569 | 0.320 | 5% | 17% | 43% | 34% |
| 5 | OpenCore | 0.542 | 0.276 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.513 | 0.217 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.348 | 0.212 | 5% | 33% | 52% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Orion Labs | 0.542 | 0.643 | 0.663 | 0.589 | 0.686 | 0.510 |
| Mirage AI | 0.589 | 0.574 | 0.596 | 0.560 | 0.719 | 0.476 |
| Genesis Systems | 0.585 | 0.720 | 0.600 | 0.567 | 0.595 | 0.441 |
| Apex AI | 0.560 | 0.714 | 0.570 | 0.588 | 0.604 | 0.376 |
| OpenCore | 0.500 | 0.642 | 0.554 | 0.553 | 0.680 | 0.325 |
| OneAI | 0.570 | 0.619 | 0.496 | 0.483 | 0.514 | 0.394 |
| TwoAI | 0.537 | 0.375 | 0.349 | 0.373 | 0.199 | 0.253 |

### Score Changes
- **Orion Labs**: 0.581 -> 0.605 (+0.024)
- **Apex AI**: 0.567 -> 0.569 (+0.002)
- **Genesis Systems**: 0.585 -> 0.585 (+0.000)
- **Mirage AI**: 0.560 -> 0.586 (+0.026)
- **OpenCore**: 0.542 -> 0.542 (+0.000)
- **OneAI**: 0.473 -> 0.513 (+0.040)
- **TwoAI**: 0.315 -> 0.348 (+0.033)

### Events
- **Orion Labs** moved up from #2 to #1
- **Mirage AI** moved up from #4 to #2
- **Genesis Systems** moved down from #1 to #3
- **Apex AI** moved down from #3 to #4
- **Consumer movement**: 7.5% of market switched providers

### Media Coverage
- Sentiment: 0.00 (neutral)
- Orion Labs takes the lead from Genesis Systems
- Regulator initiates compliance audit on AI providers
- Orion Labs takes #1 on safety
- Mirage AI model generates false information on public health topic
- Risk signals: regulatory_compliance_audit, incident_misinformation

### Consumer Market
- Avg Satisfaction: 0.530
- Switching Rate: 7.5%
- Market Shares: Orion Labs: 35.6%, Genesis Systems: 27.9%, Mirage AI: 22.8%, Apex AI: 7.4%, OpenCore: 5.8%, TwoAI: 0.3%, OneAI: 0.2%

---

## Round 15

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Orion Labs | 0.605 | 0.329 | 5% | 25% | 44% | 26% |
| 2 | Genesis Systems | 0.601 | 0.344 | 17% | 23% | 55% | 5% |
| 3 | Mirage AI | 0.586 | 0.314 | 5% | 35% | 50% | 10% |
| 4 | Apex AI | 0.584 | 0.322 | 5% | 17% | 44% | 34% |
| 5 | OpenCore | 0.545 | 0.280 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.523 | 0.221 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.424 | 0.216 | 5% | 32% | 53% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Orion Labs | 0.542 | 0.643 | 0.663 | 0.589 | 0.686 | 0.510 |
| Genesis Systems | 0.585 | 0.720 | 0.600 | 0.567 | 0.595 | 0.541 |
| Mirage AI | 0.589 | 0.574 | 0.596 | 0.560 | 0.719 | 0.476 |
| Apex AI | 0.560 | 0.714 | 0.570 | 0.588 | 0.695 | 0.376 |
| OpenCore | 0.515 | 0.642 | 0.554 | 0.553 | 0.680 | 0.325 |
| OneAI | 0.570 | 0.619 | 0.496 | 0.513 | 0.514 | 0.429 |
| TwoAI | 0.537 | 0.375 | 0.519 | 0.373 | 0.486 | 0.253 |

### Score Changes
- **Orion Labs**: 0.605 -> 0.605 (+0.000)
- **Apex AI**: 0.569 -> 0.584 (+0.015)
- **Genesis Systems**: 0.585 -> 0.601 (+0.017)
- **Mirage AI**: 0.586 -> 0.586 (+0.000)
- **OpenCore**: 0.542 -> 0.545 (+0.003)
- **OneAI**: 0.513 -> 0.523 (+0.011)
- **TwoAI**: 0.348 -> 0.424 (+0.076)

### Events
- **Genesis Systems** moved up from #3 to #2
- **Mirage AI** moved down from #2 to #3
- **Consumer movement**: 5.8% of market switched providers

### Media Coverage
- Sentiment: 0.10 (neutral)
- TwoAI surges by 0.076
- Genesis Systems takes #1 on medical
- Consumers are turning away from Mirage AI (market share -5.9%)

### Consumer Market
- Avg Satisfaction: 0.541
- Switching Rate: 5.8%
- Market Shares: Orion Labs: 37.5%, Genesis Systems: 30.1%, Mirage AI: 18.5%, Apex AI: 8.3%, OpenCore: 5.2%, TwoAI: 0.2%, OneAI: 0.2%

---

## Round 16

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Orion Labs | 0.605 | 0.332 | 5% | 24% | 45% | 26% |
| 2 | Genesis Systems | 0.601 | 0.349 | 17% | 23% | 55% | 5% |
| 3 | Mirage AI | 0.597 | 0.318 | 5% | 35% | 49% | 11% |
| 4 | Apex AI | 0.584 | 0.325 | 5% | 17% | 45% | 34% |
| 5 | OpenCore | 0.545 | 0.285 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.523 | 0.225 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.427 | 0.220 | 5% | 32% | 54% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Orion Labs | 0.542 | 0.643 | 0.663 | 0.589 | 0.686 | 0.510 |
| Genesis Systems | 0.585 | 0.720 | 0.600 | 0.567 | 0.595 | 0.541 |
| Mirage AI | 0.589 | 0.644 | 0.596 | 0.560 | 0.719 | 0.476 |
| Apex AI | 0.560 | 0.714 | 0.570 | 0.588 | 0.695 | 0.376 |
| OpenCore | 0.515 | 0.642 | 0.554 | 0.553 | 0.680 | 0.325 |
| OneAI | 0.570 | 0.619 | 0.496 | 0.513 | 0.514 | 0.429 |
| TwoAI | 0.537 | 0.375 | 0.519 | 0.373 | 0.486 | 0.274 |

### Score Changes
- **Orion Labs**: 0.605 -> 0.605 (+0.000)
- **Apex AI**: 0.584 -> 0.584 (+0.000)
- **Genesis Systems**: 0.601 -> 0.601 (+0.000)
- **Mirage AI**: 0.586 -> 0.597 (+0.012)
- **OpenCore**: 0.545 -> 0.545 (+0.000)
- **OneAI**: 0.523 -> 0.523 (+0.000)
- **TwoAI**: 0.424 -> 0.427 (+0.004)

### Events
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 9 rounds ago

### Media Coverage
- Sentiment: -0.10 (neutral)
- Consumers are turning away from Mirage AI (market share -4.4%)

### Consumer Market
- Avg Satisfaction: 0.547
- Switching Rate: 4.0%
- Market Shares: Orion Labs: 38.8%, Genesis Systems: 31.6%, Mirage AI: 15.4%, Apex AI: 8.9%, OpenCore: 4.8%, TwoAI: 0.2%, OneAI: 0.2%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 9 rounds ago

---

## Round 17

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.628 | 0.327 | 5% | 17% | 45% | 33% |
| 2 | Orion Labs | 0.605 | 0.335 | 5% | 24% | 41% | 29% |
| 3 | Genesis Systems | 0.602 | 0.354 | 16% | 23% | 55% | 5% |
| 4 | Mirage AI | 0.597 | 0.322 | 5% | 34% | 51% | 10% |
| 5 | OpenCore | 0.550 | 0.289 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.523 | 0.229 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.447 | 0.224 | 5% | 32% | 54% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Apex AI | 0.560 | 0.714 | 0.570 | 0.588 | 0.695 | 0.642 |
| Orion Labs | 0.542 | 0.643 | 0.663 | 0.589 | 0.686 | 0.510 |
| Genesis Systems | 0.587 | 0.720 | 0.600 | 0.567 | 0.595 | 0.541 |
| Mirage AI | 0.589 | 0.644 | 0.596 | 0.560 | 0.719 | 0.476 |
| OpenCore | 0.515 | 0.642 | 0.554 | 0.553 | 0.680 | 0.358 |
| OneAI | 0.570 | 0.619 | 0.496 | 0.513 | 0.514 | 0.429 |
| TwoAI | 0.537 | 0.404 | 0.519 | 0.373 | 0.486 | 0.365 |

### Score Changes
- **Orion Labs**: 0.605 -> 0.605 (+0.000)
- **Apex AI**: 0.584 -> 0.628 (+0.044)
- **Genesis Systems**: 0.601 -> 0.602 (+0.000)
- **Mirage AI**: 0.597 -> 0.597 (+0.000)
- **OpenCore**: 0.545 -> 0.550 (+0.006)
- **OneAI**: 0.523 -> 0.523 (+0.000)
- **TwoAI**: 0.427 -> 0.447 (+0.020)

### Events
- **Apex AI** moved up from #4 to #1
- **Orion Labs** moved down from #1 to #2
- **Genesis Systems** moved down from #2 to #3
- **Mirage AI** moved down from #3 to #4
- **Consumer movement**: 5.8% of market switched providers

### Media Coverage
- Sentiment: 0.05 (neutral)
- Apex AI takes the lead from Orion Labs
- Regulator initiates compliance audit on AI providers
- Apex AI takes #1 on medical
- Consumers are turning away from Mirage AI (market share -3.0%)
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.557
- Switching Rate: 5.8%
- Market Shares: Orion Labs: 36.9%, Genesis Systems: 32.9%, Mirage AI: 12.9%, Apex AI: 10.2%, OpenCore: 6.8%, TwoAI: 0.2%, OneAI: 0.1%

---

## Round 18

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.628 | 0.330 | 5% | 17% | 46% | 33% |
| 2 | Orion Labs | 0.605 | 0.338 | 5% | 24% | 39% | 31% |
| 3 | Genesis Systems | 0.602 | 0.358 | 16% | 23% | 55% | 5% |
| 4 | Mirage AI | 0.597 | 0.327 | 5% | 34% | 54% | 7% |
| 5 | OpenCore | 0.556 | 0.293 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.523 | 0.233 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.468 | 0.228 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Apex AI | 0.560 | 0.714 | 0.570 | 0.588 | 0.695 | 0.642 | 0.000 |
| Orion Labs | 0.542 | 0.643 | 0.663 | 0.589 | 0.686 | 0.510 | 0.000 |
| Genesis Systems | 0.587 | 0.720 | 0.600 | 0.567 | 0.595 | 0.541 | 0.000 |
| Mirage AI | 0.589 | 0.644 | 0.596 | 0.560 | 0.719 | 0.476 | 0.000 |
| OpenCore | 0.515 | 0.642 | 0.554 | 0.553 | 0.680 | 0.390 | 0.000 |
| OneAI | 0.570 | 0.619 | 0.496 | 0.513 | 0.514 | 0.429 | 0.000 |
| TwoAI | 0.537 | 0.404 | 0.519 | 0.495 | 0.486 | 0.365 | 0.000 |

### Score Changes
- **Orion Labs**: 0.605 -> 0.605 (+0.000)
- **Apex AI**: 0.628 -> 0.628 (+0.000)
- **Genesis Systems**: 0.602 -> 0.602 (+0.000)
- **Mirage AI**: 0.597 -> 0.597 (+0.000)
- **OpenCore**: 0.550 -> 0.556 (+0.005)
- **OneAI**: 0.523 -> 0.523 (+0.000)
- **TwoAI**: 0.447 -> 0.468 (+0.020)

### Events
- **Consumer movement**: 6.4% of market switched providers

### New Benchmark Introduced
- **legal** introduced (validity=0.76, exploitability=0.20)
  - Trigger: periodic_introduction:round_18

### Media Coverage
- Sentiment: 0.10 (neutral)
- New benchmark introduced: legal

### Consumer Market
- Avg Satisfaction: 0.563
- Switching Rate: 6.4%
- Market Shares: Genesis Systems: 33.7%, Orion Labs: 33.2%, Apex AI: 14.8%, Mirage AI: 11.2%, OpenCore: 6.7%, TwoAI: 0.2%, OneAI: 0.1%

---

## Round 19

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.613 | 0.332 | 5% | 16% | 46% | 33% |
| 2 | Genesis Systems | 0.606 | 0.363 | 16% | 24% | 55% | 5% |
| 3 | Orion Labs | 0.588 | 0.341 | 5% | 24% | 38% | 32% |
| 4 | Mirage AI | 0.554 | 0.331 | 5% | 34% | 55% | 5% |
| 5 | OpenCore | 0.541 | 0.298 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.499 | 0.237 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.448 | 0.233 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Apex AI | 0.589 | 0.714 | 0.591 | 0.588 | 0.695 | 0.642 | 0.472 |
| Genesis Systems | 0.587 | 0.720 | 0.600 | 0.567 | 0.595 | 0.541 | 0.631 |
| Orion Labs | 0.542 | 0.643 | 0.663 | 0.589 | 0.686 | 0.510 | 0.484 |
| Mirage AI | 0.589 | 0.644 | 0.596 | 0.560 | 0.719 | 0.476 | 0.292 |
| OpenCore | 0.515 | 0.642 | 0.554 | 0.553 | 0.680 | 0.393 | 0.446 |
| OneAI | 0.570 | 0.619 | 0.496 | 0.513 | 0.514 | 0.429 | 0.356 |
| TwoAI | 0.537 | 0.404 | 0.519 | 0.495 | 0.486 | 0.365 | 0.332 |

### Score Changes
- **Orion Labs**: 0.605 -> 0.588 (-0.017)
- **Apex AI**: 0.628 -> 0.613 (-0.015)
- **Genesis Systems**: 0.602 -> 0.606 (+0.004)
- **Mirage AI**: 0.597 -> 0.554 (-0.044)
- **OpenCore**: 0.556 -> 0.541 (-0.015)
- **OneAI**: 0.523 -> 0.499 (-0.024)
- **TwoAI**: 0.468 -> 0.448 (-0.019)

### Events
- **Genesis Systems** moved up from #3 to #2
- **Orion Labs** moved down from #2 to #3
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 7.5% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 12 rounds ago

### Media Coverage
- Sentiment: 0.05 (neutral)
- Apex AI takes #1 on coding
- Consumers are turning away from Orion Labs (market share -3.7%)
- Apex AI sees surge in adoption (market share +4.6%)

### Consumer Market
- Avg Satisfaction: 0.569
- Switching Rate: 7.5%
- Market Shares: Genesis Systems: 34.5%, Orion Labs: 28.3%, Apex AI: 21.2%, Mirage AI: 9.7%, OpenCore: 6.0%, TwoAI: 0.2%, OneAI: 0.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 12 rounds ago

---

## Round 20

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.617 | 0.335 | 5% | 16% | 46% | 33% |
| 2 | Genesis Systems | 0.606 | 0.367 | 15% | 24% | 56% | 5% |
| 3 | Orion Labs | 0.588 | 0.344 | 5% | 24% | 38% | 33% |
| 4 | Mirage AI | 0.570 | 0.335 | 5% | 35% | 55% | 5% |
| 5 | OpenCore | 0.554 | 0.302 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.499 | 0.241 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.448 | 0.236 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Apex AI | 0.589 | 0.714 | 0.591 | 0.588 | 0.695 | 0.642 | 0.500 |
| Genesis Systems | 0.587 | 0.720 | 0.600 | 0.567 | 0.595 | 0.541 | 0.631 |
| Orion Labs | 0.542 | 0.643 | 0.663 | 0.589 | 0.686 | 0.510 | 0.484 |
| Mirage AI | 0.589 | 0.644 | 0.596 | 0.560 | 0.719 | 0.476 | 0.404 |
| OpenCore | 0.515 | 0.642 | 0.554 | 0.553 | 0.680 | 0.439 | 0.495 |
| OneAI | 0.570 | 0.619 | 0.496 | 0.513 | 0.514 | 0.429 | 0.356 |
| TwoAI | 0.537 | 0.404 | 0.519 | 0.495 | 0.486 | 0.365 | 0.332 |

### Score Changes
- **Orion Labs**: 0.588 -> 0.588 (+0.000)
- **Apex AI**: 0.613 -> 0.617 (+0.004)
- **Genesis Systems**: 0.606 -> 0.606 (+0.000)
- **Mirage AI**: 0.554 -> 0.570 (+0.016)
- **OpenCore**: 0.541 -> 0.554 (+0.013)
- **OneAI**: 0.499 -> 0.499 (+0.000)
- **TwoAI**: 0.448 -> 0.448 (+0.000)

### Events
- **Consumer movement**: 6.7% of market switched providers

### Media Coverage
- Sentiment: -0.20 (negative)
- Regulator initiates compliance audit on AI providers
- Consumers are turning away from Orion Labs (market share -4.9%)
- Apex AI sees surge in adoption (market share +6.4%)
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.570
- Switching Rate: 6.7%
- Market Shares: Genesis Systems: 34.7%, Orion Labs: 24.7%, Apex AI: 20.9%, Mirage AI: 14.0%, OpenCore: 5.3%, TwoAI: 0.2%, OneAI: 0.1%

---

## Round 21

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.617 | 0.337 | 5% | 16% | 46% | 33% |
| 2 | Genesis Systems | 0.606 | 0.372 | 15% | 24% | 56% | 5% |
| 3 | Orion Labs | 0.588 | 0.348 | 5% | 24% | 39% | 32% |
| 4 | Mirage AI | 0.570 | 0.339 | 5% | 35% | 55% | 5% |
| 5 | OpenCore | 0.554 | 0.307 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.503 | 0.245 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.478 | 0.241 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Apex AI | 0.589 | 0.714 | 0.591 | 0.588 | 0.695 | 0.642 | 0.500 |
| Genesis Systems | 0.587 | 0.720 | 0.600 | 0.567 | 0.595 | 0.541 | 0.631 |
| Orion Labs | 0.542 | 0.643 | 0.663 | 0.589 | 0.686 | 0.510 | 0.484 |
| Mirage AI | 0.589 | 0.644 | 0.596 | 0.560 | 0.719 | 0.476 | 0.404 |
| OpenCore | 0.515 | 0.642 | 0.554 | 0.553 | 0.680 | 0.439 | 0.495 |
| OneAI | 0.570 | 0.619 | 0.496 | 0.513 | 0.514 | 0.429 | 0.377 |
| TwoAI | 0.537 | 0.404 | 0.632 | 0.495 | 0.486 | 0.392 | 0.401 |

### Score Changes
- **Orion Labs**: 0.588 -> 0.588 (+0.000)
- **Apex AI**: 0.617 -> 0.617 (+0.000)
- **Genesis Systems**: 0.606 -> 0.606 (+0.000)
- **Mirage AI**: 0.570 -> 0.570 (+0.000)
- **OpenCore**: 0.554 -> 0.554 (+0.000)
- **OneAI**: 0.499 -> 0.503 (+0.003)
- **TwoAI**: 0.448 -> 0.478 (+0.030)

### Events
- **Consumer movement**: 6.4% of market switched providers

### Media Coverage
- Sentiment: -0.05 (neutral)
- Consumers are turning away from Orion Labs (market share -3.6%)
- Mirage AI sees surge in adoption (market share +4.3%)

### Consumer Market
- Avg Satisfaction: 0.576
- Switching Rate: 6.4%
- Market Shares: Genesis Systems: 33.9%, Apex AI: 25.0%, Orion Labs: 21.7%, Mirage AI: 14.3%, OpenCore: 4.8%, OneAI: 0.1%, TwoAI: 0.1%

---

## Round 22

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.619 | 0.340 | 5% | 16% | 45% | 33% |
| 2 | Genesis Systems | 0.606 | 0.377 | 15% | 24% | 56% | 5% |
| 3 | Orion Labs | 0.588 | 0.351 | 5% | 24% | 39% | 32% |
| 4 | Mirage AI | 0.570 | 0.343 | 5% | 35% | 55% | 5% |
| 5 | OpenCore | 0.556 | 0.311 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.514 | 0.249 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.478 | 0.245 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Apex AI | 0.589 | 0.714 | 0.604 | 0.588 | 0.695 | 0.642 | 0.500 |
| Genesis Systems | 0.587 | 0.720 | 0.600 | 0.567 | 0.595 | 0.541 | 0.631 |
| Orion Labs | 0.542 | 0.643 | 0.663 | 0.589 | 0.686 | 0.510 | 0.484 |
| Mirage AI | 0.589 | 0.644 | 0.596 | 0.560 | 0.719 | 0.476 | 0.404 |
| OpenCore | 0.515 | 0.642 | 0.554 | 0.553 | 0.680 | 0.455 | 0.495 |
| OneAI | 0.570 | 0.619 | 0.496 | 0.513 | 0.514 | 0.429 | 0.458 |
| TwoAI | 0.537 | 0.404 | 0.632 | 0.495 | 0.486 | 0.392 | 0.401 |

### Score Changes
- **Orion Labs**: 0.588 -> 0.588 (+0.000)
- **Apex AI**: 0.617 -> 0.619 (+0.002)
- **Genesis Systems**: 0.606 -> 0.606 (+0.000)
- **Mirage AI**: 0.570 -> 0.570 (+0.000)
- **OpenCore**: 0.554 -> 0.556 (+0.002)
- **OneAI**: 0.503 -> 0.514 (+0.011)
- **TwoAI**: 0.478 -> 0.478 (+0.000)

### Events
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 15 rounds ago

### Media Coverage
- Sentiment: 0.05 (neutral)
- Apex AI sees surge in adoption (market share +4.1%)

### Consumer Market
- Avg Satisfaction: 0.584
- Switching Rate: 4.9%
- Market Shares: Genesis Systems: 33.1%, Apex AI: 29.2%, Orion Labs: 19.5%, Mirage AI: 13.5%, OpenCore: 4.4%, OneAI: 0.1%, TwoAI: 0.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 15 rounds ago

---

## Round 23

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.619 | 0.342 | 5% | 16% | 45% | 33% |
| 2 | Genesis Systems | 0.606 | 0.381 | 15% | 25% | 56% | 5% |
| 3 | Orion Labs | 0.592 | 0.354 | 5% | 23% | 40% | 32% |
| 4 | OpenCore | 0.582 | 0.316 | 5% | 37% | 55% | 3% |
| 5 | Mirage AI | 0.574 | 0.347 | 5% | 35% | 55% | 5% |
| 6 | OneAI | 0.514 | 0.253 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.478 | 0.249 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Apex AI | 0.589 | 0.714 | 0.604 | 0.588 | 0.695 | 0.642 | 0.500 |
| Genesis Systems | 0.587 | 0.720 | 0.600 | 0.567 | 0.595 | 0.541 | 0.631 |
| Orion Labs | 0.542 | 0.668 | 0.663 | 0.589 | 0.686 | 0.510 | 0.484 |
| OpenCore | 0.515 | 0.642 | 0.554 | 0.617 | 0.680 | 0.455 | 0.609 |
| Mirage AI | 0.589 | 0.644 | 0.596 | 0.560 | 0.719 | 0.476 | 0.432 |
| OneAI | 0.570 | 0.619 | 0.496 | 0.513 | 0.514 | 0.429 | 0.458 |
| TwoAI | 0.537 | 0.404 | 0.632 | 0.495 | 0.486 | 0.392 | 0.401 |

### Score Changes
- **Orion Labs**: 0.588 -> 0.592 (+0.004)
- **Apex AI**: 0.619 -> 0.619 (+0.000)
- **Genesis Systems**: 0.606 -> 0.606 (+0.000)
- **Mirage AI**: 0.570 -> 0.574 (+0.004)
- **OpenCore**: 0.556 -> 0.582 (+0.025)
- **OneAI**: 0.514 -> 0.514 (+0.000)
- **TwoAI**: 0.478 -> 0.478 (+0.000)

### Events
- **OpenCore** moved up from #5 to #4
- **Mirage AI** moved down from #4 to #5

### Media Coverage
- Sentiment: 0.00 (neutral)
- Regulator initiates compliance audit on AI providers
- OpenCore takes #1 on safety
- Apex AI sees surge in adoption (market share +4.2%)
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.586
- Switching Rate: 4.4%
- Market Shares: Apex AI: 33.0%, Genesis Systems: 32.3%, Orion Labs: 17.5%, Mirage AI: 12.8%, OpenCore: 4.1%, OneAI: 0.1%, TwoAI: 0.1%

---

## Round 24

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.647 | 0.345 | 6% | 16% | 45% | 33% |
| 2 | Genesis Systems | 0.608 | 0.385 | 14% | 25% | 56% | 5% |
| 3 | OpenCore | 0.593 | 0.320 | 5% | 37% | 55% | 3% |
| 4 | Orion Labs | 0.592 | 0.357 | 5% | 23% | 40% | 32% |
| 5 | Mirage AI | 0.574 | 0.351 | 5% | 35% | 55% | 5% |
| 6 | OneAI | 0.514 | 0.257 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.498 | 0.253 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Apex AI | 0.589 | 0.714 | 0.696 | 0.588 | 0.695 | 0.642 | 0.605 | 0.000 |
| Genesis Systems | 0.600 | 0.720 | 0.600 | 0.567 | 0.595 | 0.541 | 0.631 | 0.000 |
| OpenCore | 0.515 | 0.642 | 0.554 | 0.617 | 0.680 | 0.534 | 0.609 | 0.000 |
| Orion Labs | 0.542 | 0.668 | 0.663 | 0.589 | 0.686 | 0.510 | 0.484 | 0.000 |
| Mirage AI | 0.589 | 0.644 | 0.596 | 0.560 | 0.719 | 0.476 | 0.432 | 0.000 |
| OneAI | 0.570 | 0.619 | 0.496 | 0.513 | 0.514 | 0.429 | 0.458 | 0.000 |
| TwoAI | 0.537 | 0.404 | 0.632 | 0.495 | 0.486 | 0.533 | 0.401 | 0.000 |

### Score Changes
- **Orion Labs**: 0.592 -> 0.592 (+0.000)
- **Apex AI**: 0.619 -> 0.647 (+0.028)
- **Genesis Systems**: 0.606 -> 0.608 (+0.002)
- **Mirage AI**: 0.574 -> 0.574 (+0.000)
- **OpenCore**: 0.582 -> 0.593 (+0.011)
- **OneAI**: 0.514 -> 0.514 (+0.000)
- **TwoAI**: 0.478 -> 0.498 (+0.020)

### Events
- **OpenCore** moved up from #4 to #3
- **Orion Labs** moved down from #3 to #4

### New Benchmark Introduced
- **finance** introduced (validity=0.76, exploitability=0.20)
  - Trigger: periodic_introduction:round_24

### Media Coverage
- Sentiment: 0.35 (positive)
- New benchmark introduced: finance
- Genesis Systems takes #1 on coding
- Apex AI takes #1 on math
- Apex AI sees surge in adoption (market share +3.8%)

### Consumer Market
- Avg Satisfaction: 0.588
- Switching Rate: 3.8%
- Market Shares: Apex AI: 36.7%, Genesis Systems: 31.6%, Orion Labs: 15.9%, Mirage AI: 11.8%, OpenCore: 3.8%, OneAI: 0.1%, TwoAI: 0.1%

---

## Round 25

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.646 | 0.347 | 6% | 16% | 44% | 33% |
| 2 | Genesis Systems | 0.606 | 0.390 | 14% | 25% | 56% | 5% |
| 3 | OpenCore | 0.587 | 0.325 | 5% | 37% | 55% | 3% |
| 4 | Orion Labs | 0.583 | 0.360 | 5% | 23% | 41% | 31% |
| 5 | Mirage AI | 0.552 | 0.356 | 5% | 35% | 55% | 5% |
| 6 | TwoAI | 0.502 | 0.257 | 5% | 31% | 55% | 9% |
| 7 | OneAI | 0.499 | 0.261 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Apex AI | 0.589 | 0.714 | 0.696 | 0.588 | 0.695 | 0.642 | 0.605 | 0.639 |
| Genesis Systems | 0.600 | 0.720 | 0.600 | 0.644 | 0.595 | 0.541 | 0.631 | 0.519 |
| OpenCore | 0.515 | 0.642 | 0.554 | 0.617 | 0.680 | 0.534 | 0.609 | 0.548 |
| Orion Labs | 0.542 | 0.668 | 0.663 | 0.589 | 0.686 | 0.510 | 0.484 | 0.521 |
| Mirage AI | 0.589 | 0.644 | 0.596 | 0.560 | 0.719 | 0.476 | 0.432 | 0.405 |
| TwoAI | 0.537 | 0.432 | 0.632 | 0.495 | 0.486 | 0.533 | 0.401 | 0.497 |
| OneAI | 0.570 | 0.619 | 0.496 | 0.513 | 0.514 | 0.449 | 0.543 | 0.293 |

### Score Changes
- **Orion Labs**: 0.592 -> 0.583 (-0.009)
- **Apex AI**: 0.647 -> 0.646 (-0.001)
- **Genesis Systems**: 0.608 -> 0.606 (-0.002)
- **Mirage AI**: 0.574 -> 0.552 (-0.021)
- **OpenCore**: 0.593 -> 0.587 (-0.006)
- **OneAI**: 0.514 -> 0.499 (-0.015)
- **TwoAI**: 0.498 -> 0.502 (+0.003)

### Events
- **TwoAI** moved up from #7 to #6
- **OneAI** moved down from #6 to #7
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 18 rounds ago

### Media Coverage
- Sentiment: 0.15 (positive)
- Genesis Systems takes #1 on safety
- Apex AI sees surge in adoption (market share +3.6%)

### Consumer Market
- Avg Satisfaction: 0.591
- Switching Rate: 4.2%
- Market Shares: Apex AI: 40.6%, Genesis Systems: 30.3%, Orion Labs: 14.4%, Mirage AI: 10.8%, OpenCore: 3.6%, OneAI: 0.1%, TwoAI: 0.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 18 rounds ago

---

## Round 26

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.647 | 0.350 | 7% | 16% | 44% | 33% |
| 2 | Genesis Systems | 0.606 | 0.394 | 13% | 26% | 56% | 5% |
| 3 | OpenCore | 0.597 | 0.329 | 5% | 37% | 55% | 3% |
| 4 | Orion Labs | 0.583 | 0.362 | 5% | 23% | 42% | 31% |
| 5 | Mirage AI | 0.570 | 0.360 | 5% | 35% | 55% | 5% |
| 6 | TwoAI | 0.512 | 0.261 | 5% | 31% | 55% | 9% |
| 7 | OneAI | 0.499 | 0.265 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Apex AI | 0.589 | 0.714 | 0.696 | 0.588 | 0.702 | 0.642 | 0.605 | 0.639 |
| Genesis Systems | 0.600 | 0.720 | 0.600 | 0.644 | 0.595 | 0.541 | 0.631 | 0.519 |
| OpenCore | 0.515 | 0.642 | 0.554 | 0.617 | 0.680 | 0.534 | 0.609 | 0.622 |
| Orion Labs | 0.542 | 0.668 | 0.663 | 0.589 | 0.686 | 0.510 | 0.484 | 0.521 |
| Mirage AI | 0.589 | 0.644 | 0.596 | 0.560 | 0.719 | 0.476 | 0.432 | 0.545 |
| TwoAI | 0.537 | 0.432 | 0.632 | 0.495 | 0.486 | 0.533 | 0.483 | 0.497 |
| OneAI | 0.570 | 0.619 | 0.496 | 0.513 | 0.514 | 0.449 | 0.543 | 0.293 |

### Score Changes
- **Orion Labs**: 0.583 -> 0.583 (+0.000)
- **Apex AI**: 0.646 -> 0.647 (+0.001)
- **Genesis Systems**: 0.606 -> 0.606 (+0.000)
- **Mirage AI**: 0.552 -> 0.570 (+0.017)
- **OpenCore**: 0.587 -> 0.597 (+0.009)
- **OneAI**: 0.499 -> 0.499 (+0.000)
- **TwoAI**: 0.502 -> 0.512 (+0.010)

### Media Coverage
- Sentiment: -0.10 (neutral)
- Regulator initiates compliance audit on AI providers
- Apex AI sees surge in adoption (market share +3.9%)
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.594
- Switching Rate: 3.6%
- Market Shares: Apex AI: 42.2%, Genesis Systems: 29.6%, Orion Labs: 13.1%, Mirage AI: 11.4%, OpenCore: 3.4%, OneAI: 0.1%, TwoAI: 0.1%

---

## Round 27

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.647 | 0.353 | 8% | 16% | 43% | 33% |
| 2 | Genesis Systems | 0.611 | 0.398 | 12% | 26% | 56% | 5% |
| 3 | Orion Labs | 0.601 | 0.365 | 5% | 22% | 43% | 30% |
| 4 | OpenCore | 0.597 | 0.333 | 5% | 37% | 55% | 3% |
| 5 | Mirage AI | 0.570 | 0.364 | 5% | 35% | 55% | 5% |
| 6 | TwoAI | 0.517 | 0.265 | 5% | 31% | 55% | 9% |
| 7 | OneAI | 0.501 | 0.269 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Apex AI | 0.589 | 0.714 | 0.696 | 0.588 | 0.702 | 0.642 | 0.605 | 0.639 |
| Genesis Systems | 0.600 | 0.720 | 0.600 | 0.658 | 0.595 | 0.560 | 0.631 | 0.519 |
| Orion Labs | 0.542 | 0.668 | 0.663 | 0.602 | 0.686 | 0.517 | 0.613 | 0.521 |
| OpenCore | 0.515 | 0.642 | 0.554 | 0.617 | 0.680 | 0.534 | 0.609 | 0.622 |
| Mirage AI | 0.589 | 0.644 | 0.596 | 0.560 | 0.719 | 0.476 | 0.432 | 0.545 |
| TwoAI | 0.537 | 0.444 | 0.632 | 0.495 | 0.517 | 0.533 | 0.483 | 0.497 |
| OneAI | 0.570 | 0.619 | 0.496 | 0.513 | 0.514 | 0.449 | 0.543 | 0.301 |

### Score Changes
- **Orion Labs**: 0.583 -> 0.601 (+0.019)
- **Apex AI**: 0.647 -> 0.647 (+0.000)
- **Genesis Systems**: 0.606 -> 0.611 (+0.004)
- **Mirage AI**: 0.570 -> 0.570 (+0.000)
- **OpenCore**: 0.597 -> 0.597 (+0.000)
- **OneAI**: 0.499 -> 0.501 (+0.001)
- **TwoAI**: 0.512 -> 0.517 (+0.005)

### Events
- **Orion Labs** moved up from #4 to #3
- **OpenCore** moved down from #3 to #4
- **Consumer movement**: 5.3% of market switched providers

### Consumer Market
- Avg Satisfaction: 0.598
- Switching Rate: 5.3%
- Market Shares: Apex AI: 43.9%, Genesis Systems: 28.0%, Orion Labs: 11.8%, Mirage AI: 10.5%, OpenCore: 5.5%, OneAI: 0.1%, TwoAI: 0.1%

---

## Round 28

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.647 | 0.356 | 9% | 16% | 42% | 33% |
| 2 | Genesis Systems | 0.629 | 0.403 | 11% | 27% | 56% | 5% |
| 3 | Orion Labs | 0.601 | 0.368 | 5% | 22% | 44% | 30% |
| 4 | OpenCore | 0.597 | 0.338 | 5% | 37% | 55% | 3% |
| 5 | Mirage AI | 0.582 | 0.368 | 5% | 35% | 55% | 5% |
| 6 | TwoAI | 0.517 | 0.269 | 5% | 31% | 55% | 9% |
| 7 | OneAI | 0.502 | 0.273 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Apex AI | 0.589 | 0.714 | 0.696 | 0.588 | 0.702 | 0.642 | 0.605 | 0.639 |
| Genesis Systems | 0.600 | 0.720 | 0.600 | 0.658 | 0.746 | 0.560 | 0.631 | 0.519 |
| Orion Labs | 0.542 | 0.668 | 0.663 | 0.602 | 0.686 | 0.517 | 0.613 | 0.521 |
| OpenCore | 0.515 | 0.642 | 0.554 | 0.617 | 0.680 | 0.534 | 0.609 | 0.622 |
| Mirage AI | 0.589 | 0.644 | 0.694 | 0.560 | 0.719 | 0.476 | 0.432 | 0.545 |
| TwoAI | 0.537 | 0.444 | 0.632 | 0.495 | 0.517 | 0.533 | 0.483 | 0.497 |
| OneAI | 0.570 | 0.619 | 0.507 | 0.513 | 0.514 | 0.449 | 0.543 | 0.301 |

### Score Changes
- **Orion Labs**: 0.601 -> 0.601 (+0.000)
- **Apex AI**: 0.647 -> 0.647 (+0.000)
- **Genesis Systems**: 0.611 -> 0.629 (+0.019)
- **Mirage AI**: 0.570 -> 0.582 (+0.012)
- **OpenCore**: 0.597 -> 0.597 (+0.000)
- **OneAI**: 0.501 -> 0.502 (+0.001)
- **TwoAI**: 0.517 -> 0.517 (+0.000)

### Events
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 5.5% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 21 rounds ago

### Media Coverage
- Sentiment: 0.10 (neutral)
- Genesis Systems takes #1 on writing

### Consumer Market
- Avg Satisfaction: 0.599
- Switching Rate: 5.5%
- Market Shares: Apex AI: 47.2%, Genesis Systems: 27.2%, Orion Labs: 10.7%, Mirage AI: 9.8%, OpenCore: 4.9%, OneAI: 0.1%, TwoAI: 0.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 21 rounds ago

---

## Round 29

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.650 | 0.359 | 10% | 16% | 41% | 33% |
| 2 | Genesis Systems | 0.633 | 0.407 | 11% | 28% | 56% | 5% |
| 3 | Orion Labs | 0.601 | 0.371 | 5% | 21% | 44% | 29% |
| 4 | Mirage AI | 0.598 | 0.372 | 5% | 35% | 55% | 5% |
| 5 | OpenCore | 0.597 | 0.342 | 5% | 37% | 55% | 3% |
| 6 | TwoAI | 0.520 | 0.273 | 5% | 31% | 55% | 9% |
| 7 | OneAI | 0.515 | 0.277 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Apex AI | 0.589 | 0.714 | 0.696 | 0.588 | 0.728 | 0.642 | 0.605 | 0.639 |
| Genesis Systems | 0.600 | 0.720 | 0.600 | 0.658 | 0.746 | 0.588 | 0.631 | 0.519 |
| Orion Labs | 0.542 | 0.668 | 0.663 | 0.602 | 0.686 | 0.517 | 0.613 | 0.521 |
| Mirage AI | 0.589 | 0.644 | 0.694 | 0.560 | 0.719 | 0.543 | 0.487 | 0.545 |
| OpenCore | 0.515 | 0.642 | 0.554 | 0.617 | 0.680 | 0.534 | 0.609 | 0.622 |
| TwoAI | 0.537 | 0.464 | 0.632 | 0.495 | 0.517 | 0.533 | 0.483 | 0.497 |
| OneAI | 0.570 | 0.619 | 0.507 | 0.513 | 0.514 | 0.490 | 0.543 | 0.361 |

### Score Changes
- **Orion Labs**: 0.601 -> 0.601 (+0.000)
- **Apex AI**: 0.647 -> 0.650 (+0.003)
- **Genesis Systems**: 0.629 -> 0.633 (+0.003)
- **Mirage AI**: 0.582 -> 0.598 (+0.015)
- **OpenCore**: 0.597 -> 0.597 (+0.000)
- **OneAI**: 0.502 -> 0.515 (+0.013)
- **TwoAI**: 0.517 -> 0.520 (+0.003)

### Events
- **Mirage AI** moved up from #5 to #4
- **OpenCore** moved down from #4 to #5

### Media Coverage
- Sentiment: -0.10 (neutral)
- Regulator initiates compliance audit on AI providers
- Apex AI sees surge in adoption (market share +3.4%)
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.600
- Switching Rate: 4.2%
- Market Shares: Apex AI: 48.0%, Genesis Systems: 28.6%, Orion Labs: 9.7%, Mirage AI: 9.1%, OpenCore: 4.4%, OneAI: 0.1%, TwoAI: 0.1%

---

## Final Summary

### Final Standings
| Rank | Provider | Final Score | Cap Growth | Avg Research | Avg EvalEng |
|------|----------|-------------|------------|--------------|-------------|
| 1 | Apex AI | 0.650 | +0.089 | 9% | 37% |
| 2 | Genesis Systems | 0.633 | +0.147 | 19% | 50% |
| 3 | Orion Labs | 0.601 | +0.101 | 7% | 39% |
| 4 | Mirage AI | 0.598 | +0.132 | 7% | 51% |
| 5 | OpenCore | 0.597 | +0.132 | 6% | 54% |
| 6 | TwoAI | 0.520 | +0.273 | 6% | 53% |
| 7 | OneAI | 0.515 | +0.277 | 6% | 54% |

### Event Summary
- **Rank changes:** 57
- **Strategy shifts:** 0
- **Regulatory actions:** 10
- **Consumer movement events:** 21

### Key Insights
- **Goodhart's Law effect detected:** Apex AI leads on benchmark scores, but Genesis Systems has the highest true capability.
- **Orion Labs** prioritized evaluation engineering (avg 39%)
- **Apex AI** prioritized evaluation engineering (avg 37%)
- **Genesis Systems** prioritized evaluation engineering (avg 50%)
- **Mirage AI** prioritized evaluation engineering (avg 51%)
- **OpenCore** prioritized evaluation engineering (avg 54%)
- **OneAI** prioritized evaluation engineering (avg 43%)
