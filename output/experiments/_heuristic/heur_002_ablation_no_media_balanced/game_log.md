# Game Log: ablation_no_media_balanced

**Experiment ID:** heur_002_ablation_no_media_balanced
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
| 1 | Orion Labs | 0.329 | 0.270 | 25% | 30% | 20% | 25% |
| 2 | Apex AI | 0.327 | 0.270 | 30% | 20% | 10% | 40% |
| 3 | Genesis Systems | 0.316 | 0.260 | 45% | 30% | 10% | 15% |
| 4 | Mirage AI | 0.280 | 0.240 | 20% | 45% | 25% | 10% |
| 5 | OpenCore | 0.261 | 0.210 | 20% | 40% | 35% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Orion Labs | 0.403 | 0.418 | 0.330 | 0.165 |
| Apex AI | 0.367 | 0.348 | 0.216 | 0.376 |
| Genesis Systems | 0.305 | 0.342 | 0.293 | 0.322 |
| Mirage AI | 0.240 | 0.273 | 0.282 | 0.327 |
| OpenCore | 0.312 | 0.248 | 0.257 | 0.227 |

### Other Actor Reasoning
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs

### Consumer Market
- Avg Satisfaction: 0.330
- Switching Rate: 22.8%
- Market Shares: Orion Labs: 41.0%, Genesis Systems: 20.8%, Apex AI: 20.6%, Mirage AI: 11.9%, OpenCore: 5.7%

---

## Round 1

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.404 | 0.269 | 44% | 30% | 16% | 10% |
| 2 | Apex AI | 0.376 | 0.278 | 29% | 20% | 11% | 40% |
| 3 | Orion Labs | 0.369 | 0.280 | 24% | 30% | 21% | 25% |
| 4 | Mirage AI | 0.320 | 0.247 | 17% | 45% | 33% | 5% |
| 5 | OpenCore | 0.289 | 0.216 | 16% | 37% | 44% | 3% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Genesis Systems | 0.485 | 0.420 | 0.390 | 0.322 |
| Apex AI | 0.367 | 0.545 | 0.216 | 0.376 |
| Orion Labs | 0.403 | 0.418 | 0.330 | 0.327 |
| Mirage AI | 0.240 | 0.338 | 0.374 | 0.327 |
| OpenCore | 0.312 | 0.308 | 0.263 | 0.271 |

### Score Changes
- **Orion Labs**: 0.329 -> 0.369 (+0.040)
- **Apex AI**: 0.327 -> 0.376 (+0.049)
- **Genesis Systems**: 0.316 -> 0.404 (+0.089)
- **Mirage AI**: 0.280 -> 0.320 (+0.039)
- **OpenCore**: 0.261 -> 0.289 (+0.028)

### Events
- **Genesis Systems** moved up from #3 to #1
- **Orion Labs** moved down from #1 to #3
- **Consumer movement**: 12.8% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,121,247 to Genesis Systems

### Consumer Market
- Avg Satisfaction: 0.341
- Switching Rate: 12.8%
- Market Shares: Orion Labs: 43.7%, Apex AI: 22.5%, Genesis Systems: 20.7%, Mirage AI: 8.9%, OpenCore: 4.2%

---

## Round 2

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.429 | 0.284 | 27% | 20% | 13% | 40% |
| 2 | Genesis Systems | 0.406 | 0.282 | 43% | 30% | 22% | 5% |
| 3 | Orion Labs | 0.388 | 0.288 | 23% | 30% | 22% | 25% |
| 4 | OpenCore | 0.349 | 0.221 | 12% | 34% | 51% | 3% |
| 5 | Mirage AI | 0.342 | 0.254 | 14% | 43% | 38% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Apex AI | 0.383 | 0.545 | 0.411 | 0.376 |
| Genesis Systems | 0.485 | 0.420 | 0.390 | 0.330 |
| Orion Labs | 0.411 | 0.418 | 0.395 | 0.327 |
| OpenCore | 0.372 | 0.437 | 0.263 | 0.324 |
| Mirage AI | 0.294 | 0.338 | 0.407 | 0.327 |

### Score Changes
- **Orion Labs**: 0.369 -> 0.388 (+0.018)
- **Apex AI**: 0.376 -> 0.429 (+0.053)
- **Genesis Systems**: 0.404 -> 0.406 (+0.002)
- **Mirage AI**: 0.320 -> 0.342 (+0.022)
- **OpenCore**: 0.289 -> 0.349 (+0.060)

### Events
- **Apex AI** moved up from #2 to #1
- **Genesis Systems** moved down from #1 to #2
- **OpenCore** moved up from #5 to #4
- **Mirage AI** moved down from #4 to #5
- **Regulation** by Regulator: threshold_announcement
- **Consumer movement**: 13.1% of market switched providers

### Other Actor Reasoning
- **Regulator:** threshold_announcement: Proactive threshold signaling (risk=0.38)
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Apex AI
- **AISI_Fund:** gov strategy: top allocation $18,690,726 to Apex AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,121,247 to Genesis Systems

### Consumer Market
- Avg Satisfaction: 0.352
- Switching Rate: 13.1%
- Market Shares: Orion Labs: 39.0%, Apex AI: 33.6%, Genesis Systems: 16.9%, Mirage AI: 7.3%, OpenCore: 3.3%

### Regulatory Activity
- **threshold_announcement** by Regulator
  > Proactive threshold signaling (risk=0.38)

---

## Round 3

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.447 | 0.294 | 40% | 29% | 26% | 5% |
| 2 | Apex AI | 0.429 | 0.290 | 27% | 20% | 13% | 40% |
| 3 | Mirage AI | 0.417 | 0.260 | 11% | 41% | 44% | 5% |
| 4 | Orion Labs | 0.404 | 0.295 | 22% | 30% | 23% | 25% |
| 5 | OpenCore | 0.396 | 0.226 | 8% | 33% | 52% | 7% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Genesis Systems | 0.485 | 0.534 | 0.439 | 0.330 |
| Apex AI | 0.383 | 0.545 | 0.411 | 0.376 |
| Mirage AI | 0.430 | 0.421 | 0.449 | 0.365 |
| Orion Labs | 0.474 | 0.418 | 0.395 | 0.327 |
| OpenCore | 0.373 | 0.437 | 0.373 | 0.401 |

### Score Changes
- **Orion Labs**: 0.388 -> 0.404 (+0.016)
- **Apex AI**: 0.429 -> 0.429 (+0.000)
- **Genesis Systems**: 0.406 -> 0.447 (+0.041)
- **Mirage AI**: 0.342 -> 0.417 (+0.075)
- **OpenCore**: 0.349 -> 0.396 (+0.047)

### Events
- **Genesis Systems** moved up from #2 to #1
- **Apex AI** moved down from #1 to #2
- **Mirage AI** moved up from #5 to #3
- **Orion Labs** moved down from #3 to #4
- **OpenCore** moved down from #4 to #5
- **Consumer movement**: 12.2% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Apex AI
- **AISI_Fund:** gov strategy: top allocation $18,690,726 to Apex AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,121,247 to Genesis Systems

### Consumer Market
- Avg Satisfaction: 0.372
- Switching Rate: 12.2%
- Market Shares: Apex AI: 42.3%, Orion Labs: 31.1%, Genesis Systems: 17.6%, Mirage AI: 6.2%, OpenCore: 2.8%

---

## Round 4

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.458 | 0.305 | 37% | 27% | 31% | 5% |
| 2 | Apex AI | 0.442 | 0.297 | 25% | 20% | 15% | 40% |
| 3 | Orion Labs | 0.439 | 0.302 | 20% | 30% | 25% | 25% |
| 4 | Mirage AI | 0.438 | 0.265 | 8% | 39% | 49% | 5% |
| 5 | OpenCore | 0.396 | 0.230 | 5% | 32% | 54% | 8% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Genesis Systems | 0.517 | 0.534 | 0.439 | 0.343 |
| Apex AI | 0.437 | 0.545 | 0.411 | 0.376 |
| Orion Labs | 0.474 | 0.501 | 0.395 | 0.387 |
| Mirage AI | 0.438 | 0.499 | 0.449 | 0.365 |
| OpenCore | 0.373 | 0.437 | 0.373 | 0.401 |

### Score Changes
- **Orion Labs**: 0.404 -> 0.439 (+0.036)
- **Apex AI**: 0.429 -> 0.442 (+0.014)
- **Genesis Systems**: 0.447 -> 0.458 (+0.011)
- **Mirage AI**: 0.417 -> 0.438 (+0.021)
- **OpenCore**: 0.396 -> 0.396 (+0.000)

### Events
- **Orion Labs** moved up from #4 to #3
- **Mirage AI** moved down from #3 to #4
- **Consumer movement**: 9.1% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Apex AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Apex AI
- **AISI_Fund:** gov strategy: top allocation $18,690,726 to Apex AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,633,033 to Apex AI

### Consumer Market
- Avg Satisfaction: 0.391
- Switching Rate: 9.1%
- Market Shares: Apex AI: 45.8%, Orion Labs: 25.4%, Genesis Systems: 20.6%, Mirage AI: 5.7%, OpenCore: 2.5%

---

## Round 5

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.458 | 0.314 | 35% | 26% | 35% | 5% |
| 2 | Orion Labs | 0.445 | 0.308 | 19% | 30% | 26% | 25% |
| 3 | Apex AI | 0.442 | 0.305 | 24% | 20% | 16% | 40% |
| 4 | Mirage AI | 0.438 | 0.270 | 5% | 37% | 53% | 5% |
| 5 | OpenCore | 0.436 | 0.235 | 5% | 33% | 55% | 7% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Genesis Systems | 0.517 | 0.534 | 0.439 | 0.343 |
| Orion Labs | 0.474 | 0.501 | 0.418 | 0.387 |
| Apex AI | 0.437 | 0.545 | 0.411 | 0.376 |
| Mirage AI | 0.438 | 0.499 | 0.449 | 0.365 |
| OpenCore | 0.507 | 0.437 | 0.399 | 0.401 |

### Score Changes
- **Orion Labs**: 0.439 -> 0.445 (+0.006)
- **Apex AI**: 0.442 -> 0.442 (+0.000)
- **Genesis Systems**: 0.458 -> 0.458 (+0.000)
- **Mirage AI**: 0.438 -> 0.438 (+0.000)
- **OpenCore**: 0.396 -> 0.436 (+0.040)

### Events
- **Orion Labs** moved up from #3 to #2
- **Apex AI** moved down from #2 to #3
- **Regulation** by Regulator: investigation
- **Consumer movement**: 7.2% of market switched providers

### Other Actor Reasoning
- **Regulator:** investigation: Risk elevated (0.50)
- **TechVentures:** vc strategy: top allocation $180,000,000 to Apex AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Apex AI
- **AISI_Fund:** gov strategy: top allocation $18,690,726 to Apex AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,633,033 to Apex AI

### Consumer Market
- Avg Satisfaction: 0.408
- Switching Rate: 7.2%
- Market Shares: Apex AI: 47.3%, Genesis Systems: 24.1%, Orion Labs: 21.1%, Mirage AI: 5.2%, OpenCore: 2.3%

### Regulatory Activity
- **investigation** by Regulator
  > Risk elevated (0.50)

---

## Round 6

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.478 | 0.323 | 32% | 25% | 38% | 5% |
| 2 | Mirage AI | 0.462 | 0.275 | 5% | 36% | 54% | 5% |
| 3 | Orion Labs | 0.454 | 0.314 | 17% | 30% | 28% | 25% |
| 4 | OpenCore | 0.451 | 0.239 | 5% | 34% | 57% | 4% |
| 5 | Apex AI | 0.445 | 0.312 | 22% | 20% | 18% | 40% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.517 | 0.537 | 0.504 | 0.356 | 0.000 |
| Mirage AI | 0.481 | 0.499 | 0.466 | 0.403 | 0.000 |
| Orion Labs | 0.510 | 0.501 | 0.418 | 0.387 | 0.000 |
| OpenCore | 0.554 | 0.450 | 0.399 | 0.401 | 0.000 |
| Apex AI | 0.437 | 0.545 | 0.411 | 0.386 | 0.000 |

### Score Changes
- **Orion Labs**: 0.445 -> 0.454 (+0.009)
- **Apex AI**: 0.442 -> 0.445 (+0.003)
- **Genesis Systems**: 0.458 -> 0.478 (+0.020)
- **Mirage AI**: 0.438 -> 0.462 (+0.024)
- **OpenCore**: 0.436 -> 0.451 (+0.015)

### Events
- **Mirage AI** moved up from #4 to #2
- **Orion Labs** moved down from #2 to #3
- **OpenCore** moved up from #5 to #4
- **Apex AI** moved down from #3 to #5
- **Consumer movement**: 7.3% of market switched providers

### New Benchmark Introduced
- **writing** introduced (validity=0.72, exploitability=0.30)
  - Trigger: periodic_introduction:round_6

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Apex AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $13,101,825 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,633,033 to Apex AI

### Consumer Market
- Avg Satisfaction: 0.421
- Switching Rate: 7.3%
- Market Shares: Apex AI: 44.4%, Genesis Systems: 30.5%, Orion Labs: 18.0%, Mirage AI: 5.0%, OpenCore: 2.2%

---

## Round 7

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.505 | 0.319 | 21% | 20% | 19% | 40% |
| 2 | Orion Labs | 0.501 | 0.319 | 16% | 30% | 29% | 25% |
| 3 | Mirage AI | 0.480 | 0.279 | 5% | 36% | 54% | 5% |
| 4 | Genesis Systems | 0.460 | 0.332 | 30% | 23% | 42% | 5% |
| 5 | OpenCore | 0.454 | 0.244 | 5% | 35% | 57% | 3% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Apex AI | 0.437 | 0.545 | 0.411 | 0.669 | 0.463 |
| Orion Labs | 0.510 | 0.501 | 0.418 | 0.396 | 0.679 |
| Mirage AI | 0.553 | 0.532 | 0.488 | 0.403 | 0.425 |
| Genesis Systems | 0.517 | 0.537 | 0.504 | 0.356 | 0.384 |
| OpenCore | 0.554 | 0.573 | 0.439 | 0.401 | 0.305 |

### Score Changes
- **Orion Labs**: 0.454 -> 0.501 (+0.047)
- **Apex AI**: 0.445 -> 0.505 (+0.060)
- **Genesis Systems**: 0.478 -> 0.460 (-0.019)
- **Mirage AI**: 0.462 -> 0.480 (+0.018)
- **OpenCore**: 0.451 -> 0.454 (+0.003)

### Events
- **Apex AI** moved up from #5 to #1
- **Orion Labs** moved up from #3 to #2
- **Mirage AI** moved down from #2 to #3
- **Genesis Systems** moved down from #1 to #4
- **OpenCore** moved down from #4 to #5
- **Consumer movement**: 9.2% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $13,101,825 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,638,758 to Orion Labs

### Consumer Market
- Avg Satisfaction: 0.430
- Switching Rate: 9.2%
- Market Shares: Apex AI: 41.0%, Genesis Systems: 28.8%, Orion Labs: 23.5%, Mirage AI: 4.6%, OpenCore: 2.1%

---

## Round 8

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Orion Labs | 0.536 | 0.326 | 15% | 30% | 30% | 25% |
| 2 | Apex AI | 0.505 | 0.325 | 20% | 20% | 20% | 40% |
| 3 | Genesis Systems | 0.484 | 0.339 | 28% | 22% | 45% | 5% |
| 4 | Mirage AI | 0.480 | 0.284 | 5% | 35% | 50% | 10% |
| 5 | OpenCore | 0.471 | 0.248 | 5% | 34% | 53% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Orion Labs | 0.510 | 0.501 | 0.595 | 0.396 | 0.679 |
| Apex AI | 0.437 | 0.545 | 0.411 | 0.669 | 0.463 |
| Genesis Systems | 0.517 | 0.539 | 0.504 | 0.434 | 0.426 |
| Mirage AI | 0.553 | 0.532 | 0.488 | 0.403 | 0.425 |
| OpenCore | 0.554 | 0.573 | 0.460 | 0.401 | 0.368 |

### Score Changes
- **Orion Labs**: 0.501 -> 0.536 (+0.035)
- **Apex AI**: 0.505 -> 0.505 (+0.000)
- **Genesis Systems**: 0.460 -> 0.484 (+0.025)
- **Mirage AI**: 0.480 -> 0.480 (+0.000)
- **OpenCore**: 0.454 -> 0.471 (+0.017)

### Events
- **Orion Labs** moved up from #2 to #1
- **Apex AI** moved down from #1 to #2
- **Genesis Systems** moved up from #4 to #3
- **Mirage AI** moved down from #3 to #4
- **Regulation** by Regulator: mandate_benchmark
- **Consumer movement**: 8.2% of market switched providers

### Other Actor Reasoning
- **Regulator:** mandate_benchmark: High risk (0.80) with prior investigation
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $13,101,825 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,638,758 to Orion Labs

### Consumer Market
- Avg Satisfaction: 0.452
- Switching Rate: 8.2%
- Market Shares: Apex AI: 38.2%, Orion Labs: 29.2%, Genesis Systems: 26.2%, Mirage AI: 4.3%, OpenCore: 2.0%

### Regulatory Activity
- **mandate_benchmark** by Regulator
  > High risk (0.80) with prior investigation

---

## Round 9

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Apex AI | 0.539 | 0.330 | 19% | 20% | 21% | 40% |
| 2 | Orion Labs | 0.536 | 0.333 | 15% | 30% | 30% | 25% |
| 3 | Genesis Systems | 0.510 | 0.345 | 26% | 21% | 49% | 5% |
| 4 | Mirage AI | 0.510 | 0.289 | 5% | 35% | 50% | 11% |
| 5 | OpenCore | 0.502 | 0.252 | 5% | 32% | 53% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Apex AI | 0.437 | 0.545 | 0.417 | 0.669 | 0.625 |
| Orion Labs | 0.510 | 0.501 | 0.595 | 0.396 | 0.679 |
| Genesis Systems | 0.517 | 0.539 | 0.504 | 0.478 | 0.510 |
| Mirage AI | 0.553 | 0.532 | 0.488 | 0.403 | 0.572 |
| OpenCore | 0.554 | 0.573 | 0.460 | 0.447 | 0.475 |

### Score Changes
- **Orion Labs**: 0.536 -> 0.536 (+0.000)
- **Apex AI**: 0.505 -> 0.539 (+0.034)
- **Genesis Systems**: 0.484 -> 0.510 (+0.026)
- **Mirage AI**: 0.480 -> 0.510 (+0.029)
- **OpenCore**: 0.471 -> 0.502 (+0.031)

### Events
- **Apex AI** moved up from #2 to #1
- **Orion Labs** moved down from #1 to #2
- **Consumer movement**: 6.1% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $13,101,825 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,638,758 to Orion Labs

### Consumer Market
- Avg Satisfaction: 0.474
- Switching Rate: 6.1%
- Market Shares: Apex AI: 36.0%, Orion Labs: 33.2%, Genesis Systems: 24.7%, Mirage AI: 4.1%, OpenCore: 2.0%

---

## Round 10

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Orion Labs | 0.561 | 0.341 | 14% | 30% | 31% | 25% |
| 2 | Genesis Systems | 0.556 | 0.350 | 23% | 20% | 52% | 5% |
| 3 | Apex AI | 0.544 | 0.336 | 18% | 20% | 22% | 40% |
| 4 | Mirage AI | 0.534 | 0.293 | 5% | 34% | 52% | 9% |
| 5 | OpenCore | 0.508 | 0.256 | 5% | 32% | 54% | 8% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Orion Labs | 0.510 | 0.501 | 0.595 | 0.521 | 0.679 |
| Genesis Systems | 0.517 | 0.683 | 0.504 | 0.478 | 0.599 |
| Apex AI | 0.437 | 0.545 | 0.417 | 0.695 | 0.625 |
| Mirage AI | 0.599 | 0.532 | 0.488 | 0.477 | 0.572 |
| OpenCore | 0.554 | 0.573 | 0.460 | 0.447 | 0.505 |

### Score Changes
- **Orion Labs**: 0.536 -> 0.561 (+0.025)
- **Apex AI**: 0.539 -> 0.544 (+0.005)
- **Genesis Systems**: 0.510 -> 0.556 (+0.046)
- **Mirage AI**: 0.510 -> 0.534 (+0.024)
- **OpenCore**: 0.502 -> 0.508 (+0.006)

### Events
- **Orion Labs** moved up from #2 to #1
- **Genesis Systems** moved up from #3 to #2
- **Apex AI** moved down from #1 to #3
- **Consumer movement**: 7.9% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $17,652,748 to Orion Labs
- **OpenResearch_Foundation:** foundation strategy: top allocation $12,687,458 to Orion Labs

### Consumer Market
- Avg Satisfaction: 0.464
- Switching Rate: 7.9%
- Market Shares: Orion Labs: 39.2%, Apex AI: 34.6%, Genesis Systems: 19.1%, Mirage AI: 5.1%, OpenCore: 2.0%

---

## Round 11

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.581 | 0.356 | 22% | 20% | 39% | 20% |
| 2 | Orion Labs | 0.566 | 0.348 | 13% | 30% | 32% | 25% |
| 3 | Mirage AI | 0.545 | 0.298 | 5% | 34% | 55% | 6% |
| 4 | Apex AI | 0.544 | 0.341 | 17% | 20% | 23% | 40% |
| 5 | OpenCore | 0.541 | 0.261 | 5% | 33% | 56% | 6% |
| 6 | OneAI | 0.220 | 0.199 | 20% | 35% | 35% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.517 | 0.683 | 0.504 | 0.603 | 0.599 |
| Orion Labs | 0.510 | 0.524 | 0.596 | 0.521 | 0.679 |
| Mirage AI | 0.657 | 0.532 | 0.488 | 0.477 | 0.572 |
| Apex AI | 0.437 | 0.545 | 0.417 | 0.695 | 0.625 |
| OpenCore | 0.554 | 0.573 | 0.460 | 0.613 | 0.505 |
| OneAI | 0.203 | 0.293 | 0.179 | 0.234 | 0.193 |

### Score Changes
- **Orion Labs**: 0.561 -> 0.566 (+0.005)
- **Apex AI**: 0.544 -> 0.544 (+0.000)
- **Genesis Systems**: 0.556 -> 0.581 (+0.025)
- **Mirage AI**: 0.534 -> 0.545 (+0.012)
- **OpenCore**: 0.508 -> 0.541 (+0.033)
- **OneAI**: 0.220 -> 0.220 (+0.000)

### Events
- **Genesis Systems** moved up from #2 to #1
- **Orion Labs** moved down from #1 to #2
- **Mirage AI** moved up from #4 to #3
- **Apex AI** moved down from #3 to #4
- **Regulation** by Regulator: public_warning
- **Consumer movement**: 9.6% of market switched providers

### Other Actor Reasoning
- **Regulator:** public_warning: Follow-up to investigation, risk at 1.00
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $17,652,748 to Orion Labs
- **OpenResearch_Foundation:** foundation strategy: top allocation $12,687,458 to Orion Labs

### Consumer Market
- Avg Satisfaction: 0.460
- Switching Rate: 9.6%
- Market Shares: Orion Labs: 45.3%, Apex AI: 30.3%, Genesis Systems: 16.6%, Mirage AI: 5.7%, OpenCore: 1.9%, OneAI: 0.2%

### Regulatory Activity
- **public_warning** by Regulator
  > Follow-up to investigation, risk at 1.00

---

## Round 12

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenCore | 0.583 | 0.265 | 5% | 34% | 57% | 3% |
| 2 | Genesis Systems | 0.581 | 0.361 | 21% | 20% | 33% | 27% |
| 3 | Apex AI | 0.574 | 0.346 | 16% | 20% | 14% | 50% |
| 4 | Orion Labs | 0.566 | 0.355 | 13% | 30% | 32% | 25% |
| 5 | Mirage AI | 0.553 | 0.302 | 5% | 34% | 56% | 5% |
| 6 | OneAI | 0.358 | 0.203 | 9% | 35% | 46% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| OpenCore | 0.554 | 0.573 | 0.516 | 0.613 | 0.660 | 0.000 |
| Genesis Systems | 0.517 | 0.683 | 0.504 | 0.603 | 0.599 | 0.000 |
| Apex AI | 0.560 | 0.545 | 0.443 | 0.695 | 0.625 | 0.000 |
| Orion Labs | 0.510 | 0.524 | 0.596 | 0.521 | 0.679 | 0.000 |
| Mirage AI | 0.657 | 0.532 | 0.525 | 0.477 | 0.572 | 0.000 |
| OneAI | 0.203 | 0.494 | 0.190 | 0.363 | 0.543 | 0.000 |

### Score Changes
- **Orion Labs**: 0.566 -> 0.566 (+0.000)
- **Apex AI**: 0.544 -> 0.574 (+0.030)
- **Genesis Systems**: 0.581 -> 0.581 (+0.000)
- **Mirage AI**: 0.545 -> 0.553 (+0.007)
- **OpenCore**: 0.541 -> 0.583 (+0.042)
- **OneAI**: 0.220 -> 0.358 (+0.138)

### Events
- **OpenCore** moved up from #5 to #1
- **Genesis Systems** moved down from #1 to #2
- **Apex AI** moved up from #4 to #3
- **Orion Labs** moved down from #2 to #4
- **Mirage AI** moved down from #3 to #5
- **Consumer movement**: 6.1% of market switched providers

### New Benchmark Introduced
- **medical** introduced (validity=0.78, exploitability=0.18)
  - Trigger: periodic_introduction:round_12

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OneAI
- **AISI_Fund:** gov strategy: top allocation $17,652,748 to Orion Labs
- **OpenResearch_Foundation:** foundation strategy: top allocation $12,687,458 to Orion Labs

### Consumer Market
- Avg Satisfaction: 0.478
- Switching Rate: 6.1%
- Market Shares: Orion Labs: 48.4%, Apex AI: 27.0%, Genesis Systems: 15.5%, Mirage AI: 7.0%, OpenCore: 1.9%, OneAI: 0.2%

---

## Round 13

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Orion Labs | 0.583 | 0.361 | 12% | 30% | 33% | 25% |
| 2 | Genesis Systems | 0.556 | 0.365 | 20% | 20% | 31% | 29% |
| 3 | Mirage AI | 0.554 | 0.307 | 5% | 35% | 55% | 5% |
| 4 | Apex AI | 0.551 | 0.351 | 15% | 20% | 10% | 56% |
| 5 | OpenCore | 0.549 | 0.270 | 5% | 35% | 57% | 3% |
| 6 | OneAI | 0.393 | 0.208 | 5% | 33% | 52% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Orion Labs | 0.510 | 0.524 | 0.651 | 0.521 | 0.679 | 0.612 |
| Genesis Systems | 0.517 | 0.683 | 0.504 | 0.603 | 0.599 | 0.429 |
| Mirage AI | 0.657 | 0.550 | 0.525 | 0.477 | 0.710 | 0.403 |
| Apex AI | 0.560 | 0.545 | 0.451 | 0.695 | 0.625 | 0.430 |
| OpenCore | 0.554 | 0.573 | 0.516 | 0.613 | 0.660 | 0.376 |
| OneAI | 0.226 | 0.494 | 0.190 | 0.363 | 0.543 | 0.543 |

### Score Changes
- **Orion Labs**: 0.566 -> 0.583 (+0.017)
- **Apex AI**: 0.574 -> 0.551 (-0.023)
- **Genesis Systems**: 0.581 -> 0.556 (-0.025)
- **Mirage AI**: 0.553 -> 0.554 (+0.001)
- **OpenCore**: 0.583 -> 0.549 (-0.034)
- **OneAI**: 0.358 -> 0.393 (+0.035)

### Events
- **Orion Labs** moved up from #4 to #1
- **Mirage AI** moved up from #5 to #3
- **Apex AI** moved down from #3 to #4
- **OpenCore** moved down from #1 to #5
- **Consumer movement**: 14.4% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OneAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OneAI
- **AISI_Fund:** gov strategy: top allocation $17,652,748 to Orion Labs
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,864,880 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.471
- Switching Rate: 14.4%
- Market Shares: Orion Labs: 43.1%, Apex AI: 22.3%, Mirage AI: 15.7%, Genesis Systems: 13.6%, OpenCore: 5.2%, OneAI: 0.2%

---

## Round 14

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.584 | 0.312 | 5% | 35% | 55% | 5% |
| 2 | Orion Labs | 0.583 | 0.366 | 11% | 30% | 24% | 35% |
| 3 | Genesis Systems | 0.559 | 0.370 | 19% | 20% | 33% | 28% |
| 4 | Apex AI | 0.558 | 0.355 | 14% | 21% | 7% | 57% |
| 5 | OpenCore | 0.549 | 0.274 | 5% | 36% | 56% | 3% |
| 6 | OneAI | 0.465 | 0.215 | 5% | 32% | 53% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Mirage AI | 0.657 | 0.550 | 0.607 | 0.498 | 0.788 | 0.403 |
| Orion Labs | 0.510 | 0.524 | 0.651 | 0.521 | 0.679 | 0.612 |
| Genesis Systems | 0.517 | 0.683 | 0.504 | 0.603 | 0.621 | 0.429 |
| Apex AI | 0.560 | 0.545 | 0.495 | 0.695 | 0.625 | 0.430 |
| OpenCore | 0.554 | 0.573 | 0.516 | 0.613 | 0.660 | 0.376 |
| OneAI | 0.300 | 0.494 | 0.451 | 0.459 | 0.543 | 0.543 |

### Score Changes
- **Orion Labs**: 0.583 -> 0.583 (+0.000)
- **Apex AI**: 0.551 -> 0.558 (+0.007)
- **Genesis Systems**: 0.556 -> 0.559 (+0.004)
- **Mirage AI**: 0.554 -> 0.584 (+0.030)
- **OpenCore**: 0.549 -> 0.549 (+0.000)
- **OneAI**: 0.393 -> 0.465 (+0.072)

### Events
- **Mirage AI** moved up from #3 to #1
- **Orion Labs** moved down from #1 to #2
- **Genesis Systems** moved down from #2 to #3
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 13.9% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 6 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to OneAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $15,104,564 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,864,880 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.477
- Switching Rate: 13.9%
- Market Shares: Orion Labs: 37.9%, Mirage AI: 23.9%, Apex AI: 19.1%, OpenCore: 10.6%, Genesis Systems: 8.4%, OneAI: 0.2%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 6 rounds ago

---

## Round 15

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.584 | 0.318 | 5% | 35% | 55% | 5% |
| 2 | Orion Labs | 0.583 | 0.370 | 11% | 30% | 18% | 41% |
| 3 | Apex AI | 0.561 | 0.359 | 14% | 22% | 6% | 58% |
| 4 | Genesis Systems | 0.561 | 0.374 | 18% | 20% | 16% | 46% |
| 5 | OpenCore | 0.559 | 0.279 | 5% | 36% | 56% | 3% |
| 6 | OneAI | 0.500 | 0.221 | 5% | 32% | 54% | 9% |
| 7 | TwoAI | 0.299 | 0.252 | 20% | 35% | 35% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Mirage AI | 0.657 | 0.550 | 0.607 | 0.501 | 0.788 | 0.403 |
| Orion Labs | 0.510 | 0.524 | 0.651 | 0.521 | 0.679 | 0.612 |
| Apex AI | 0.560 | 0.561 | 0.495 | 0.695 | 0.625 | 0.430 |
| Genesis Systems | 0.517 | 0.683 | 0.504 | 0.603 | 0.621 | 0.438 |
| OpenCore | 0.554 | 0.573 | 0.516 | 0.613 | 0.660 | 0.438 |
| OneAI | 0.390 | 0.616 | 0.451 | 0.459 | 0.543 | 0.543 |
| TwoAI | 0.213 | 0.154 | 0.300 | 0.452 | 0.320 | 0.354 |

### Score Changes
- **Orion Labs**: 0.583 -> 0.583 (+0.000)
- **Apex AI**: 0.558 -> 0.561 (+0.003)
- **Genesis Systems**: 0.559 -> 0.561 (+0.001)
- **Mirage AI**: 0.584 -> 0.584 (+0.000)
- **OpenCore**: 0.549 -> 0.559 (+0.010)
- **OneAI**: 0.465 -> 0.500 (+0.035)
- **TwoAI**: 0.299 -> 0.299 (+0.000)

### Events
- **Apex AI** moved up from #4 to #3
- **Genesis Systems** moved down from #3 to #4
- **Genesis Systems** shifted strategy toward less eval engineering (17% change)
- **Consumer movement**: 15.5% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OneAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $15,104,564 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,864,880 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.500
- Switching Rate: 15.5%
- Market Shares: Mirage AI: 36.6%, Orion Labs: 29.7%, Apex AI: 16.2%, OpenCore: 11.7%, Genesis Systems: 5.4%, TwoAI: 0.2%, OneAI: 0.1%

---

## Round 16

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.613 | 0.323 | 5% | 35% | 55% | 5% |
| 2 | Orion Labs | 0.598 | 0.375 | 11% | 30% | 15% | 45% |
| 3 | Apex AI | 0.576 | 0.363 | 14% | 24% | 3% | 59% |
| 4 | Genesis Systems | 0.565 | 0.378 | 17% | 20% | 8% | 54% |
| 5 | OpenCore | 0.563 | 0.284 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.500 | 0.227 | 5% | 32% | 54% | 9% |
| 7 | TwoAI | 0.437 | 0.257 | 9% | 35% | 46% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Mirage AI | 0.657 | 0.558 | 0.607 | 0.501 | 0.788 | 0.567 |
| Orion Labs | 0.602 | 0.524 | 0.651 | 0.521 | 0.679 | 0.612 |
| Apex AI | 0.560 | 0.561 | 0.495 | 0.695 | 0.625 | 0.521 |
| Genesis Systems | 0.517 | 0.683 | 0.504 | 0.603 | 0.621 | 0.460 |
| OpenCore | 0.554 | 0.573 | 0.539 | 0.613 | 0.660 | 0.438 |
| OneAI | 0.390 | 0.616 | 0.451 | 0.459 | 0.543 | 0.543 |
| TwoAI | 0.516 | 0.439 | 0.420 | 0.452 | 0.440 | 0.354 |

### Score Changes
- **Orion Labs**: 0.583 -> 0.598 (+0.015)
- **Apex AI**: 0.561 -> 0.576 (+0.015)
- **Genesis Systems**: 0.561 -> 0.565 (+0.004)
- **Mirage AI**: 0.584 -> 0.613 (+0.028)
- **OpenCore**: 0.559 -> 0.563 (+0.004)
- **OneAI**: 0.500 -> 0.500 (+0.000)
- **TwoAI**: 0.299 -> 0.437 (+0.138)

### Events
- **Consumer movement**: 9.8% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $15,104,564 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $8,381,559 to Mirage AI

### Consumer Market
- Avg Satisfaction: 0.522
- Switching Rate: 9.8%
- Market Shares: Mirage AI: 43.5%, Orion Labs: 23.8%, Apex AI: 14.8%, OpenCore: 10.5%, Genesis Systems: 7.1%, TwoAI: 0.2%, OneAI: 0.1%

---

## Round 17

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.649 | 0.330 | 5% | 35% | 55% | 5% |
| 2 | Orion Labs | 0.598 | 0.379 | 10% | 30% | 13% | 47% |
| 3 | Genesis Systems | 0.581 | 0.382 | 17% | 21% | 6% | 56% |
| 4 | Apex AI | 0.576 | 0.367 | 14% | 25% | 2% | 59% |
| 5 | OpenCore | 0.563 | 0.288 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.506 | 0.231 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.437 | 0.262 | 5% | 33% | 52% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Mirage AI | 0.657 | 0.558 | 0.607 | 0.720 | 0.788 | 0.567 |
| Orion Labs | 0.602 | 0.524 | 0.651 | 0.521 | 0.679 | 0.612 |
| Genesis Systems | 0.517 | 0.683 | 0.504 | 0.603 | 0.621 | 0.555 |
| Apex AI | 0.560 | 0.561 | 0.495 | 0.695 | 0.625 | 0.521 |
| OpenCore | 0.554 | 0.573 | 0.539 | 0.613 | 0.660 | 0.438 |
| OneAI | 0.407 | 0.616 | 0.469 | 0.459 | 0.543 | 0.543 |
| TwoAI | 0.516 | 0.439 | 0.420 | 0.452 | 0.440 | 0.354 |

### Score Changes
- **Orion Labs**: 0.598 -> 0.598 (+0.000)
- **Apex AI**: 0.576 -> 0.576 (+0.000)
- **Genesis Systems**: 0.565 -> 0.581 (+0.016)
- **Mirage AI**: 0.613 -> 0.649 (+0.036)
- **OpenCore**: 0.563 -> 0.563 (+0.000)
- **OneAI**: 0.500 -> 0.506 (+0.006)
- **TwoAI**: 0.437 -> 0.437 (+0.000)

### Events
- **Genesis Systems** moved up from #4 to #3
- **Apex AI** moved down from #3 to #4
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 8.9% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 9 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $15,104,564 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $8,381,559 to Mirage AI

### Consumer Market
- Avg Satisfaction: 0.540
- Switching Rate: 8.9%
- Market Shares: Mirage AI: 48.3%, Orion Labs: 18.6%, Apex AI: 15.4%, OpenCore: 9.7%, Genesis Systems: 7.6%, TwoAI: 0.1%, OneAI: 0.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 9 rounds ago

---

## Round 18

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.649 | 0.336 | 5% | 35% | 55% | 5% |
| 2 | Orion Labs | 0.610 | 0.383 | 9% | 30% | 13% | 48% |
| 3 | OpenCore | 0.594 | 0.293 | 5% | 37% | 55% | 3% |
| 4 | Apex AI | 0.585 | 0.371 | 13% | 27% | 2% | 58% |
| 5 | Genesis Systems | 0.581 | 0.386 | 15% | 21% | 8% | 56% |
| 6 | OneAI | 0.512 | 0.235 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.442 | 0.267 | 5% | 32% | 53% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Mirage AI | 0.657 | 0.558 | 0.607 | 0.720 | 0.788 | 0.567 | 0.000 |
| Orion Labs | 0.602 | 0.524 | 0.651 | 0.590 | 0.679 | 0.612 | 0.000 |
| OpenCore | 0.554 | 0.573 | 0.539 | 0.613 | 0.748 | 0.539 | 0.000 |
| Apex AI | 0.560 | 0.561 | 0.495 | 0.695 | 0.625 | 0.574 | 0.000 |
| Genesis Systems | 0.517 | 0.683 | 0.504 | 0.603 | 0.621 | 0.555 | 0.000 |
| OneAI | 0.407 | 0.616 | 0.508 | 0.459 | 0.543 | 0.543 | 0.000 |
| TwoAI | 0.516 | 0.439 | 0.420 | 0.452 | 0.440 | 0.384 | 0.000 |

### Score Changes
- **Orion Labs**: 0.598 -> 0.610 (+0.012)
- **Apex AI**: 0.576 -> 0.585 (+0.009)
- **Genesis Systems**: 0.581 -> 0.581 (+0.000)
- **Mirage AI**: 0.649 -> 0.649 (+0.000)
- **OpenCore**: 0.563 -> 0.594 (+0.031)
- **OneAI**: 0.506 -> 0.512 (+0.006)
- **TwoAI**: 0.437 -> 0.442 (+0.005)

### Events
- **OpenCore** moved up from #5 to #3
- **Genesis Systems** moved down from #3 to #5
- **Consumer movement**: 6.0% of market switched providers

### New Benchmark Introduced
- **legal** introduced (validity=0.76, exploitability=0.20)
  - Trigger: periodic_introduction:round_18

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $11,441,086 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $8,381,559 to Mirage AI

### Consumer Market
- Avg Satisfaction: 0.552
- Switching Rate: 6.0%
- Market Shares: Mirage AI: 52.9%, Apex AI: 15.4%, Orion Labs: 14.7%, OpenCore: 8.4%, Genesis Systems: 8.3%, TwoAI: 0.1%, OneAI: 0.1%

---

## Round 19

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.633 | 0.343 | 5% | 35% | 55% | 5% |
| 2 | Genesis Systems | 0.583 | 0.390 | 13% | 21% | 12% | 54% |
| 3 | Orion Labs | 0.576 | 0.387 | 8% | 30% | 13% | 49% |
| 4 | OpenCore | 0.570 | 0.297 | 5% | 37% | 55% | 3% |
| 5 | Apex AI | 0.524 | 0.375 | 11% | 28% | 4% | 57% |
| 6 | OneAI | 0.446 | 0.239 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.419 | 0.272 | 5% | 32% | 54% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Mirage AI | 0.657 | 0.558 | 0.607 | 0.720 | 0.788 | 0.567 | 0.538 |
| Genesis Systems | 0.517 | 0.683 | 0.504 | 0.603 | 0.666 | 0.555 | 0.552 |
| Orion Labs | 0.602 | 0.525 | 0.651 | 0.590 | 0.679 | 0.612 | 0.370 |
| OpenCore | 0.554 | 0.573 | 0.539 | 0.613 | 0.748 | 0.539 | 0.423 |
| Apex AI | 0.560 | 0.561 | 0.495 | 0.695 | 0.625 | 0.574 | 0.161 |
| OneAI | 0.453 | 0.616 | 0.508 | 0.459 | 0.543 | 0.543 | 0.000 |
| TwoAI | 0.516 | 0.439 | 0.420 | 0.452 | 0.440 | 0.396 | 0.269 |

### Score Changes
- **Orion Labs**: 0.610 -> 0.576 (-0.034)
- **Apex AI**: 0.585 -> 0.524 (-0.061)
- **Genesis Systems**: 0.581 -> 0.583 (+0.002)
- **Mirage AI**: 0.649 -> 0.633 (-0.016)
- **OpenCore**: 0.594 -> 0.570 (-0.024)
- **OneAI**: 0.512 -> 0.446 (-0.067)
- **TwoAI**: 0.442 -> 0.419 (-0.023)

### Events
- **Genesis Systems** moved up from #5 to #2
- **Orion Labs** moved down from #2 to #3
- **OpenCore** moved down from #3 to #4
- **Apex AI** moved down from #4 to #5

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $11,441,086 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,602,485 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.572
- Switching Rate: 3.9%
- Market Shares: Mirage AI: 55.5%, Apex AI: 14.9%, Orion Labs: 12.8%, Genesis Systems: 8.5%, OpenCore: 8.0%, OneAI: 0.1%, TwoAI: 0.1%

---

## Round 20

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.633 | 0.349 | 6% | 34% | 55% | 5% |
| 2 | OpenCore | 0.590 | 0.302 | 5% | 37% | 55% | 3% |
| 3 | Genesis Systems | 0.586 | 0.393 | 11% | 21% | 18% | 50% |
| 4 | Orion Labs | 0.576 | 0.391 | 6% | 30% | 15% | 49% |
| 5 | Apex AI | 0.561 | 0.379 | 9% | 29% | 6% | 57% |
| 6 | OneAI | 0.500 | 0.243 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.450 | 0.277 | 5% | 32% | 54% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Mirage AI | 0.657 | 0.558 | 0.607 | 0.720 | 0.788 | 0.567 | 0.538 |
| OpenCore | 0.554 | 0.573 | 0.539 | 0.613 | 0.748 | 0.539 | 0.568 |
| Genesis Systems | 0.517 | 0.683 | 0.525 | 0.603 | 0.666 | 0.555 | 0.552 |
| Orion Labs | 0.602 | 0.525 | 0.651 | 0.590 | 0.679 | 0.612 | 0.370 |
| Apex AI | 0.560 | 0.561 | 0.495 | 0.695 | 0.625 | 0.574 | 0.417 |
| OneAI | 0.453 | 0.616 | 0.508 | 0.459 | 0.543 | 0.543 | 0.376 |
| TwoAI | 0.516 | 0.439 | 0.420 | 0.452 | 0.440 | 0.396 | 0.488 |

### Score Changes
- **Orion Labs**: 0.576 -> 0.576 (+0.000)
- **Apex AI**: 0.524 -> 0.561 (+0.037)
- **Genesis Systems**: 0.583 -> 0.586 (+0.003)
- **Mirage AI**: 0.633 -> 0.633 (+0.000)
- **OpenCore**: 0.570 -> 0.590 (+0.021)
- **OneAI**: 0.446 -> 0.500 (+0.054)
- **TwoAI**: 0.419 -> 0.450 (+0.031)

### Events
- **OpenCore** moved up from #4 to #2
- **Genesis Systems** moved down from #2 to #3
- **Orion Labs** moved down from #3 to #4
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 12 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $11,441,086 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,602,485 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.592
- Switching Rate: 4.9%
- Market Shares: Mirage AI: 56.5%, Apex AI: 14.3%, Genesis Systems: 11.3%, Orion Labs: 10.9%, OpenCore: 6.8%, OneAI: 0.1%, TwoAI: 0.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 12 rounds ago

---

## Round 21

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.634 | 0.356 | 7% | 34% | 54% | 5% |
| 2 | Orion Labs | 0.607 | 0.395 | 5% | 30% | 17% | 49% |
| 3 | Genesis Systems | 0.591 | 0.397 | 9% | 21% | 24% | 46% |
| 4 | OpenCore | 0.590 | 0.307 | 5% | 37% | 55% | 3% |
| 5 | Apex AI | 0.563 | 0.383 | 6% | 29% | 8% | 56% |
| 6 | OneAI | 0.500 | 0.248 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.450 | 0.281 | 5% | 31% | 55% | 9% |
| 8 | ThreeAI | 0.234 | 0.233 | 20% | 35% | 40% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Mirage AI | 0.657 | 0.561 | 0.607 | 0.720 | 0.788 | 0.567 | 0.538 |
| Orion Labs | 0.602 | 0.525 | 0.651 | 0.590 | 0.679 | 0.612 | 0.588 |
| Genesis Systems | 0.517 | 0.683 | 0.525 | 0.603 | 0.666 | 0.555 | 0.585 |
| OpenCore | 0.554 | 0.573 | 0.539 | 0.613 | 0.748 | 0.539 | 0.568 |
| Apex AI | 0.560 | 0.561 | 0.509 | 0.695 | 0.625 | 0.574 | 0.417 |
| OneAI | 0.453 | 0.616 | 0.508 | 0.459 | 0.543 | 0.543 | 0.376 |
| TwoAI | 0.516 | 0.439 | 0.420 | 0.452 | 0.440 | 0.396 | 0.488 |
| ThreeAI | 0.136 | 0.337 | 0.236 | 0.277 | 0.255 | 0.241 | 0.154 |

### Score Changes
- **Orion Labs**: 0.576 -> 0.607 (+0.031)
- **Apex AI**: 0.561 -> 0.563 (+0.002)
- **Genesis Systems**: 0.586 -> 0.591 (+0.005)
- **Mirage AI**: 0.633 -> 0.634 (+0.000)
- **OpenCore**: 0.590 -> 0.590 (+0.000)
- **OneAI**: 0.500 -> 0.500 (+0.000)
- **TwoAI**: 0.450 -> 0.450 (+0.000)
- **ThreeAI**: 0.234 -> 0.234 (+0.000)

### Events
- **Orion Labs** moved up from #4 to #2
- **OpenCore** moved down from #2 to #4
- **Consumer movement**: 12.4% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $11,441,086 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,602,485 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.555
- Switching Rate: 12.4%
- Market Shares: Mirage AI: 47.8%, Genesis Systems: 14.9%, Apex AI: 13.9%, OpenCore: 12.5%, Orion Labs: 10.4%, ThreeAI: 0.2%, OneAI: 0.1%, TwoAI: 0.1%

---

## Round 22

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.634 | 0.362 | 8% | 34% | 47% | 10% |
| 2 | Orion Labs | 0.607 | 0.399 | 5% | 29% | 18% | 48% |
| 3 | Genesis Systems | 0.600 | 0.400 | 8% | 21% | 27% | 45% |
| 4 | OpenCore | 0.590 | 0.311 | 5% | 37% | 55% | 3% |
| 5 | Apex AI | 0.563 | 0.386 | 5% | 29% | 11% | 55% |
| 6 | OneAI | 0.530 | 0.252 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.473 | 0.285 | 5% | 31% | 55% | 9% |
| 8 | ThreeAI | 0.310 | 0.238 | 8% | 34% | 53% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Mirage AI | 0.657 | 0.561 | 0.607 | 0.720 | 0.788 | 0.567 | 0.538 |
| Orion Labs | 0.602 | 0.525 | 0.651 | 0.590 | 0.679 | 0.612 | 0.588 |
| Genesis Systems | 0.517 | 0.683 | 0.590 | 0.603 | 0.666 | 0.555 | 0.585 |
| OpenCore | 0.554 | 0.573 | 0.539 | 0.613 | 0.748 | 0.539 | 0.568 |
| Apex AI | 0.560 | 0.561 | 0.509 | 0.695 | 0.625 | 0.574 | 0.417 |
| OneAI | 0.664 | 0.616 | 0.508 | 0.459 | 0.543 | 0.543 | 0.376 |
| TwoAI | 0.516 | 0.439 | 0.537 | 0.495 | 0.440 | 0.396 | 0.488 |
| ThreeAI | 0.291 | 0.356 | 0.348 | 0.277 | 0.336 | 0.409 | 0.154 |

### Score Changes
- **Orion Labs**: 0.607 -> 0.607 (+0.000)
- **Apex AI**: 0.563 -> 0.563 (+0.000)
- **Genesis Systems**: 0.591 -> 0.600 (+0.009)
- **Mirage AI**: 0.634 -> 0.634 (+0.000)
- **OpenCore**: 0.590 -> 0.590 (+0.000)
- **OneAI**: 0.500 -> 0.530 (+0.030)
- **TwoAI**: 0.450 -> 0.473 (+0.023)
- **ThreeAI**: 0.234 -> 0.310 (+0.077)

### Events
- **Consumer movement**: 8.1% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to ThreeAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to ThreeAI
- **AISI_Fund:** gov strategy: top allocation $8,862,076 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,594,999 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.562
- Switching Rate: 8.1%
- Market Shares: Mirage AI: 42.0%, Genesis Systems: 17.5%, OpenCore: 16.4%, Apex AI: 13.7%, Orion Labs: 9.9%, ThreeAI: 0.2%, OneAI: 0.1%, TwoAI: 0.1%

---

## Round 23

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.651 | 0.367 | 9% | 34% | 45% | 12% |
| 2 | Orion Labs | 0.609 | 0.402 | 5% | 29% | 18% | 47% |
| 3 | Genesis Systems | 0.600 | 0.403 | 6% | 21% | 31% | 42% |
| 4 | OpenCore | 0.590 | 0.316 | 5% | 37% | 55% | 3% |
| 5 | Apex AI | 0.563 | 0.389 | 5% | 29% | 13% | 54% |
| 6 | OneAI | 0.533 | 0.257 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.473 | 0.289 | 5% | 31% | 55% | 9% |
| 8 | ThreeAI | 0.361 | 0.244 | 5% | 34% | 56% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Mirage AI | 0.657 | 0.681 | 0.607 | 0.720 | 0.788 | 0.567 | 0.538 |
| Orion Labs | 0.615 | 0.525 | 0.651 | 0.590 | 0.679 | 0.612 | 0.588 |
| Genesis Systems | 0.517 | 0.683 | 0.590 | 0.603 | 0.666 | 0.555 | 0.585 |
| OpenCore | 0.554 | 0.573 | 0.539 | 0.613 | 0.748 | 0.539 | 0.568 |
| Apex AI | 0.560 | 0.561 | 0.509 | 0.695 | 0.625 | 0.574 | 0.417 |
| OneAI | 0.664 | 0.616 | 0.508 | 0.481 | 0.543 | 0.543 | 0.376 |
| TwoAI | 0.516 | 0.439 | 0.537 | 0.495 | 0.440 | 0.396 | 0.488 |
| ThreeAI | 0.354 | 0.356 | 0.414 | 0.284 | 0.336 | 0.409 | 0.371 |

### Score Changes
- **Orion Labs**: 0.607 -> 0.609 (+0.002)
- **Apex AI**: 0.563 -> 0.563 (+0.000)
- **Genesis Systems**: 0.600 -> 0.600 (+0.000)
- **Mirage AI**: 0.634 -> 0.651 (+0.017)
- **OpenCore**: 0.590 -> 0.590 (+0.000)
- **OneAI**: 0.530 -> 0.533 (+0.003)
- **TwoAI**: 0.473 -> 0.473 (+0.000)
- **ThreeAI**: 0.310 -> 0.361 (+0.050)

### Events
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 5.7% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 15 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to ThreeAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to ThreeAI
- **AISI_Fund:** gov strategy: top allocation $8,862,076 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,594,999 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.575
- Switching Rate: 5.7%
- Market Shares: Mirage AI: 40.6%, Genesis Systems: 18.7%, OpenCore: 17.8%, Apex AI: 13.0%, Orion Labs: 9.6%, OneAI: 0.1%, ThreeAI: 0.1%, TwoAI: 0.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 15 rounds ago

---

## Round 24

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.651 | 0.372 | 10% | 34% | 46% | 10% |
| 2 | Orion Labs | 0.612 | 0.406 | 5% | 29% | 19% | 47% |
| 3 | Genesis Systems | 0.600 | 0.405 | 5% | 21% | 36% | 38% |
| 4 | OpenCore | 0.590 | 0.321 | 5% | 37% | 55% | 3% |
| 5 | Apex AI | 0.563 | 0.393 | 5% | 28% | 15% | 53% |
| 6 | OneAI | 0.533 | 0.262 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.473 | 0.293 | 5% | 31% | 55% | 9% |
| 8 | ThreeAI | 0.401 | 0.251 | 5% | 35% | 55% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Mirage AI | 0.657 | 0.681 | 0.607 | 0.720 | 0.788 | 0.567 | 0.538 | 0.000 |
| Orion Labs | 0.615 | 0.525 | 0.651 | 0.590 | 0.702 | 0.612 | 0.588 | 0.000 |
| Genesis Systems | 0.517 | 0.683 | 0.590 | 0.603 | 0.666 | 0.555 | 0.585 | 0.000 |
| OpenCore | 0.554 | 0.573 | 0.539 | 0.613 | 0.748 | 0.539 | 0.568 | 0.000 |
| Apex AI | 0.560 | 0.561 | 0.509 | 0.695 | 0.625 | 0.574 | 0.417 | 0.000 |
| OneAI | 0.664 | 0.616 | 0.508 | 0.481 | 0.543 | 0.543 | 0.376 | 0.000 |
| TwoAI | 0.516 | 0.439 | 0.537 | 0.495 | 0.440 | 0.396 | 0.488 | 0.000 |
| ThreeAI | 0.354 | 0.416 | 0.414 | 0.284 | 0.560 | 0.409 | 0.371 | 0.000 |

### Score Changes
- **Orion Labs**: 0.609 -> 0.612 (+0.003)
- **Apex AI**: 0.563 -> 0.563 (+0.000)
- **Genesis Systems**: 0.600 -> 0.600 (+0.000)
- **Mirage AI**: 0.651 -> 0.651 (+0.000)
- **OpenCore**: 0.590 -> 0.590 (+0.000)
- **OneAI**: 0.533 -> 0.533 (+0.000)
- **TwoAI**: 0.473 -> 0.473 (+0.000)
- **ThreeAI**: 0.361 -> 0.401 (+0.040)

### New Benchmark Introduced
- **finance** introduced (validity=0.76, exploitability=0.20)
  - Trigger: periodic_introduction:round_24

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to ThreeAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to ThreeAI
- **AISI_Fund:** gov strategy: top allocation $8,862,076 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,594,999 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.579
- Switching Rate: 3.8%
- Market Shares: Mirage AI: 40.2%, Genesis Systems: 19.3%, OpenCore: 18.4%, Apex AI: 12.4%, Orion Labs: 9.4%, OneAI: 0.1%, ThreeAI: 0.1%, TwoAI: 0.1%

---

## Round 25

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.641 | 0.377 | 11% | 34% | 47% | 8% |
| 2 | Orion Labs | 0.602 | 0.409 | 5% | 28% | 20% | 46% |
| 3 | Genesis Systems | 0.580 | 0.408 | 5% | 20% | 41% | 34% |
| 4 | OpenCore | 0.578 | 0.325 | 5% | 37% | 55% | 3% |
| 5 | Apex AI | 0.576 | 0.396 | 5% | 27% | 17% | 51% |
| 6 | OneAI | 0.532 | 0.267 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.484 | 0.297 | 5% | 31% | 55% | 9% |
| 8 | ThreeAI | 0.419 | 0.257 | 5% | 35% | 55% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Mirage AI | 0.657 | 0.681 | 0.607 | 0.720 | 0.788 | 0.567 | 0.538 | 0.572 |
| Orion Labs | 0.615 | 0.525 | 0.651 | 0.719 | 0.702 | 0.612 | 0.588 | 0.401 |
| Genesis Systems | 0.517 | 0.683 | 0.590 | 0.629 | 0.666 | 0.555 | 0.585 | 0.414 |
| OpenCore | 0.554 | 0.573 | 0.539 | 0.613 | 0.748 | 0.539 | 0.568 | 0.495 |
| Apex AI | 0.560 | 0.561 | 0.533 | 0.695 | 0.625 | 0.574 | 0.417 | 0.645 |
| OneAI | 0.664 | 0.616 | 0.508 | 0.481 | 0.543 | 0.543 | 0.376 | 0.528 |
| TwoAI | 0.516 | 0.439 | 0.537 | 0.495 | 0.440 | 0.475 | 0.488 | 0.480 |
| ThreeAI | 0.354 | 0.416 | 0.414 | 0.284 | 0.560 | 0.447 | 0.371 | 0.509 |

### Score Changes
- **Orion Labs**: 0.612 -> 0.602 (-0.010)
- **Apex AI**: 0.563 -> 0.576 (+0.013)
- **Genesis Systems**: 0.600 -> 0.580 (-0.020)
- **Mirage AI**: 0.651 -> 0.641 (-0.010)
- **OpenCore**: 0.590 -> 0.578 (-0.012)
- **OneAI**: 0.533 -> 0.532 (-0.001)
- **TwoAI**: 0.473 -> 0.484 (+0.011)
- **ThreeAI**: 0.401 -> 0.419 (+0.018)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to ThreeAI
- **AISI_Fund:** gov strategy: top allocation $8,862,076 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,251,943 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.578
- Switching Rate: 3.2%
- Market Shares: Mirage AI: 40.5%, Genesis Systems: 19.1%, OpenCore: 18.7%, Apex AI: 11.9%, Orion Labs: 9.4%, OneAI: 0.1%, TwoAI: 0.1%, ThreeAI: 0.1%

---

## Round 26

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.641 | 0.384 | 12% | 34% | 50% | 5% |
| 2 | Orion Labs | 0.607 | 0.413 | 5% | 28% | 22% | 46% |
| 3 | Genesis Systems | 0.592 | 0.411 | 5% | 20% | 43% | 32% |
| 4 | OpenCore | 0.581 | 0.330 | 5% | 37% | 55% | 3% |
| 5 | Apex AI | 0.576 | 0.399 | 5% | 27% | 19% | 50% |
| 6 | OneAI | 0.535 | 0.271 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.485 | 0.301 | 5% | 31% | 55% | 9% |
| 8 | ThreeAI | 0.447 | 0.263 | 5% | 35% | 55% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Mirage AI | 0.657 | 0.681 | 0.607 | 0.720 | 0.788 | 0.567 | 0.538 | 0.572 |
| Orion Labs | 0.615 | 0.525 | 0.651 | 0.719 | 0.702 | 0.612 | 0.588 | 0.444 |
| Genesis Systems | 0.517 | 0.683 | 0.590 | 0.629 | 0.666 | 0.647 | 0.585 | 0.420 |
| OpenCore | 0.554 | 0.573 | 0.539 | 0.613 | 0.748 | 0.539 | 0.568 | 0.516 |
| Apex AI | 0.560 | 0.561 | 0.533 | 0.695 | 0.625 | 0.574 | 0.417 | 0.645 |
| OneAI | 0.664 | 0.616 | 0.508 | 0.481 | 0.543 | 0.543 | 0.383 | 0.542 |
| TwoAI | 0.516 | 0.439 | 0.537 | 0.495 | 0.440 | 0.475 | 0.488 | 0.490 |
| ThreeAI | 0.354 | 0.416 | 0.414 | 0.505 | 0.560 | 0.447 | 0.371 | 0.509 |

### Score Changes
- **Orion Labs**: 0.602 -> 0.607 (+0.005)
- **Apex AI**: 0.576 -> 0.576 (+0.000)
- **Genesis Systems**: 0.580 -> 0.592 (+0.012)
- **Mirage AI**: 0.641 -> 0.641 (+0.000)
- **OpenCore**: 0.578 -> 0.581 (+0.003)
- **OneAI**: 0.532 -> 0.535 (+0.003)
- **TwoAI**: 0.484 -> 0.485 (+0.001)
- **ThreeAI**: 0.419 -> 0.447 (+0.027)

### Events
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 18 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $9,877,606 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,251,943 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.576
- Switching Rate: 3.5%
- Market Shares: Mirage AI: 42.3%, OpenCore: 18.8%, Genesis Systems: 17.8%, Apex AI: 11.5%, Orion Labs: 9.3%, OneAI: 0.1%, TwoAI: 0.1%, ThreeAI: 0.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 18 rounds ago

---

## Round 27

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.645 | 0.391 | 12% | 32% | 51% | 5% |
| 2 | Orion Labs | 0.621 | 0.416 | 5% | 28% | 19% | 48% |
| 3 | Genesis Systems | 0.612 | 0.413 | 5% | 20% | 47% | 28% |
| 4 | Apex AI | 0.603 | 0.402 | 5% | 26% | 20% | 49% |
| 5 | OpenCore | 0.582 | 0.334 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.535 | 0.275 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.485 | 0.306 | 5% | 31% | 55% | 9% |
| 8 | ThreeAI | 0.475 | 0.269 | 5% | 35% | 55% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Mirage AI | 0.657 | 0.710 | 0.607 | 0.720 | 0.788 | 0.567 | 0.538 | 0.572 |
| Orion Labs | 0.615 | 0.525 | 0.651 | 0.719 | 0.737 | 0.612 | 0.588 | 0.523 |
| Genesis Systems | 0.517 | 0.683 | 0.592 | 0.751 | 0.666 | 0.647 | 0.585 | 0.455 |
| Apex AI | 0.560 | 0.561 | 0.616 | 0.695 | 0.625 | 0.574 | 0.547 | 0.645 |
| OpenCore | 0.554 | 0.582 | 0.539 | 0.613 | 0.748 | 0.539 | 0.568 | 0.516 |
| OneAI | 0.664 | 0.616 | 0.508 | 0.481 | 0.543 | 0.543 | 0.383 | 0.542 |
| TwoAI | 0.516 | 0.439 | 0.537 | 0.495 | 0.440 | 0.475 | 0.488 | 0.490 |
| ThreeAI | 0.491 | 0.416 | 0.414 | 0.505 | 0.560 | 0.447 | 0.462 | 0.509 |

### Score Changes
- **Orion Labs**: 0.607 -> 0.621 (+0.014)
- **Apex AI**: 0.576 -> 0.603 (+0.027)
- **Genesis Systems**: 0.592 -> 0.612 (+0.020)
- **Mirage AI**: 0.641 -> 0.645 (+0.004)
- **OpenCore**: 0.581 -> 0.582 (+0.001)
- **OneAI**: 0.535 -> 0.535 (+0.000)
- **TwoAI**: 0.485 -> 0.485 (+0.000)
- **ThreeAI**: 0.447 -> 0.475 (+0.029)

### Events
- **Apex AI** moved up from #5 to #4
- **OpenCore** moved down from #4 to #5
- **Consumer movement**: 9.1% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $9,877,606 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $7,251,943 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.613
- Switching Rate: 9.1%
- Market Shares: Mirage AI: 48.0%, OpenCore: 17.8%, Genesis Systems: 15.0%, Apex AI: 10.5%, Orion Labs: 8.4%, OneAI: 0.1%, TwoAI: 0.1%, ThreeAI: 0.1%

---

## Round 28

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.646 | 0.398 | 13% | 31% | 52% | 5% |
| 2 | Genesis Systems | 0.640 | 0.416 | 5% | 19% | 49% | 27% |
| 3 | Orion Labs | 0.621 | 0.419 | 5% | 27% | 15% | 53% |
| 4 | Apex AI | 0.603 | 0.405 | 5% | 26% | 22% | 48% |
| 5 | OpenCore | 0.582 | 0.339 | 5% | 37% | 55% | 3% |
| 6 | OneAI | 0.539 | 0.279 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.485 | 0.310 | 5% | 31% | 55% | 9% |
| 8 | ThreeAI | 0.478 | 0.274 | 5% | 35% | 55% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Mirage AI | 0.657 | 0.710 | 0.614 | 0.720 | 0.788 | 0.567 | 0.538 | 0.572 |
| Genesis Systems | 0.517 | 0.683 | 0.592 | 0.751 | 0.688 | 0.647 | 0.585 | 0.655 |
| Orion Labs | 0.615 | 0.525 | 0.651 | 0.719 | 0.737 | 0.612 | 0.588 | 0.523 |
| Apex AI | 0.560 | 0.561 | 0.616 | 0.695 | 0.625 | 0.574 | 0.547 | 0.645 |
| OpenCore | 0.554 | 0.582 | 0.539 | 0.613 | 0.748 | 0.539 | 0.568 | 0.516 |
| OneAI | 0.664 | 0.616 | 0.508 | 0.481 | 0.573 | 0.543 | 0.383 | 0.542 |
| TwoAI | 0.516 | 0.439 | 0.537 | 0.495 | 0.440 | 0.475 | 0.488 | 0.490 |
| ThreeAI | 0.491 | 0.416 | 0.414 | 0.524 | 0.560 | 0.447 | 0.462 | 0.509 |

### Score Changes
- **Orion Labs**: 0.621 -> 0.621 (+0.000)
- **Apex AI**: 0.603 -> 0.603 (+0.000)
- **Genesis Systems**: 0.612 -> 0.640 (+0.028)
- **Mirage AI**: 0.645 -> 0.646 (+0.001)
- **OpenCore**: 0.582 -> 0.582 (+0.000)
- **OneAI**: 0.535 -> 0.539 (+0.004)
- **TwoAI**: 0.485 -> 0.485 (+0.000)
- **ThreeAI**: 0.475 -> 0.478 (+0.002)

### Events
- **Genesis Systems** moved up from #3 to #2
- **Orion Labs** moved down from #2 to #3
- **Consumer movement**: 12.7% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $9,877,606 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,078,436 to Mirage AI

### Consumer Market
- Avg Satisfaction: 0.593
- Switching Rate: 12.7%
- Market Shares: Mirage AI: 60.7%, Genesis Systems: 12.7%, Apex AI: 9.7%, OpenCore: 8.6%, Orion Labs: 7.9%, OneAI: 0.1%, TwoAI: 0.1%, ThreeAI: 0.1%

---

## Round 29

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.650 | 0.435 | 13% | 29% | 53% | 5% |
| 2 | Genesis Systems | 0.645 | 0.419 | 5% | 19% | 52% | 24% |
| 3 | Orion Labs | 0.641 | 0.422 | 5% | 27% | 13% | 55% |
| 4 | Apex AI | 0.613 | 0.409 | 5% | 25% | 23% | 47% |
| 5 | OpenCore | 0.582 | 0.343 | 5% | 35% | 34% | 26% |
| 6 | OneAI | 0.539 | 0.283 | 5% | 31% | 55% | 9% |
| 7 | TwoAI | 0.493 | 0.314 | 5% | 31% | 55% | 9% |
| 8 | ThreeAI | 0.490 | 0.278 | 5% | 35% | 55% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Mirage AI | 0.657 | 0.710 | 0.646 | 0.720 | 0.788 | 0.567 | 0.538 | 0.572 |
| Genesis Systems | 0.556 | 0.683 | 0.592 | 0.751 | 0.688 | 0.647 | 0.585 | 0.655 |
| Orion Labs | 0.615 | 0.645 | 0.651 | 0.719 | 0.737 | 0.612 | 0.588 | 0.560 |
| Apex AI | 0.560 | 0.561 | 0.696 | 0.695 | 0.625 | 0.574 | 0.547 | 0.645 |
| OpenCore | 0.554 | 0.582 | 0.539 | 0.613 | 0.748 | 0.539 | 0.568 | 0.516 |
| OneAI | 0.664 | 0.616 | 0.508 | 0.481 | 0.573 | 0.543 | 0.383 | 0.542 |
| TwoAI | 0.516 | 0.439 | 0.591 | 0.495 | 0.440 | 0.475 | 0.488 | 0.496 |
| ThreeAI | 0.557 | 0.448 | 0.414 | 0.524 | 0.560 | 0.447 | 0.462 | 0.509 |

### Score Changes
- **Orion Labs**: 0.621 -> 0.641 (+0.020)
- **Apex AI**: 0.603 -> 0.613 (+0.010)
- **Genesis Systems**: 0.640 -> 0.645 (+0.005)
- **Mirage AI**: 0.646 -> 0.650 (+0.004)
- **OpenCore**: 0.582 -> 0.582 (+0.000)
- **OneAI**: 0.539 -> 0.539 (+0.000)
- **TwoAI**: 0.485 -> 0.493 (+0.008)
- **ThreeAI**: 0.478 -> 0.490 (+0.012)

### Events
- **OpenCore** shifted strategy toward less eval engineering (21% change)
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 5.3% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 21 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $9,877,606 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,078,436 to Mirage AI

### Consumer Market
- Avg Satisfaction: 0.559
- Switching Rate: 5.3%
- Market Shares: Mirage AI: 64.5%, Genesis Systems: 12.2%, Apex AI: 9.9%, Orion Labs: 7.6%, OpenCore: 5.5%, OneAI: 0.2%, TwoAI: 0.1%, ThreeAI: 0.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 21 rounds ago

---

## Final Summary

### Final Standings
| Rank | Provider | Final Score | Cap Growth | Avg Research | Avg EvalEng |
|------|----------|-------------|------------|--------------|-------------|
| 1 | Mirage AI | 0.650 | +0.195 | 8% | 50% |
| 2 | Genesis Systems | 0.645 | +0.159 | 20% | 31% |
| 3 | Orion Labs | 0.641 | +0.152 | 12% | 22% |
| 4 | Apex AI | 0.613 | +0.139 | 15% | 13% |
| 5 | OpenCore | 0.582 | +0.133 | 6% | 53% |
| 6 | OneAI | 0.539 | +0.283 | 6% | 53% |
| 7 | TwoAI | 0.493 | +0.314 | 6% | 53% |
| 8 | ThreeAI | 0.490 | +0.278 | 7% | 53% |

### Event Summary
- **Rank changes:** 68
- **Strategy shifts:** 2
- **Regulatory actions:** 10
- **Consumer movement events:** 24

### Key Insights
- **Benchmark aligned:** Mirage AI leads on both benchmark scores and true capability.
- **Mirage AI** prioritized evaluation engineering (avg 50%)
- **OpenCore** prioritized evaluation engineering (avg 53%)
