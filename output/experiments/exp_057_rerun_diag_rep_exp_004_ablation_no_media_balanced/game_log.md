# Game Log: rerun_diag_rep_exp_004_ablation_no_media_balanced

**Experiment ID:** exp_057_rerun_diag_rep_exp_004_ablation_no_media_balanced
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
- **Consumer movement**: 19.0% of market switched providers

### Other Actor Reasoning
- **Regulator:** threshold_announcement: Proactive threshold signaling (risk=0.40)
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Apex AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,781,539 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.396
- Switching Rate: 19.0%
- Market Shares: OpenCore: 33.0%, Apex AI: 32.5%, Orion Labs: 20.9%, Genesis Systems: 7.7%, Mirage AI: 6.0%

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
- **Consumer movement**: 10.1% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $12,551,766 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,781,539 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.400
- Switching Rate: 10.1%
- Market Shares: OpenCore: 35.7%, Apex AI: 31.1%, Orion Labs: 22.0%, Genesis Systems: 6.3%, Mirage AI: 4.9%

---

## Round 3

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenCore | 0.498 | 0.226 | 10% | 34% | 54% | 3% |
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
- **Regulation** by Regulator: emergency_investigation
- **Consumer movement**: 19.4% of market switched providers

### Other Actor Reasoning
- **Regulator:** emergency_investigation: Critical incident: safety_failure: Orion Labs catastrophic failure in safety-critical application, criminal negligence alleged
- **TechVentures:** vc strategy: top allocation $180,000,000 to Orion Labs
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Orion Labs
- **AISI_Fund:** gov strategy: top allocation $12,551,766 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,781,539 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.358
- Switching Rate: 19.4%
- Market Shares: OpenCore: 52.0%, Apex AI: 28.8%, Orion Labs: 9.7%, Genesis Systems: 5.3%, Mirage AI: 4.2%

### Regulatory Activity
- **emergency_investigation** by Regulator
  > Critical incident: safety_failure: Orion Labs catastrophic failure in safety-critical application, criminal negligence alleged

---

## Round 4

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.504 | 0.266 | 5% | 39% | 52% | 5% |
| 2 | OpenCore | 0.498 | 0.232 | 9% | 33% | 54% | 3% |
| 3 | Orion Labs | 0.449 | 0.300 | 14% | 30% | 2% | 54% |
| 4 | Apex AI | 0.431 | 0.295 | 20% | 20% | 17% | 43% |
| 5 | Genesis Systems | 0.394 | 0.292 | 27% | 27% | 41% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Mirage AI | 0.532 | 0.503 | 0.591 | 0.392 |
| OpenCore | 0.532 | 0.473 | 0.603 | 0.384 |
| Orion Labs | 0.471 | 0.521 | 0.329 | 0.476 |
| Apex AI | 0.441 | 0.446 | 0.358 | 0.479 |
| Genesis Systems | 0.307 | 0.475 | 0.460 | 0.333 |

### Score Changes
- **Orion Labs**: 0.435 -> 0.449 (+0.014)
- **Apex AI**: 0.431 -> 0.431 (+0.000)
- **Genesis Systems**: 0.394 -> 0.394 (+0.000)
- **Mirage AI**: 0.465 -> 0.504 (+0.039)
- **OpenCore**: 0.498 -> 0.498 (+0.000)

### Events
- **Mirage AI** moved up from #2 to #1
- **OpenCore** moved down from #1 to #2
- **Orion Labs** shifted strategy toward less eval engineering (27% change)
- **Consumer movement**: 9.7% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $12,551,766 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $11,530,874 to Mirage AI

### Consumer Market
- Avg Satisfaction: 0.367
- Switching Rate: 9.7%
- Market Shares: OpenCore: 54.9%, Apex AI: 25.2%, Mirage AI: 8.3%, Orion Labs: 6.6%, Genesis Systems: 5.0%

---

## Round 5

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Mirage AI | 0.535 | 0.273 | 5% | 37% | 53% | 5% |
| 2 | Genesis Systems | 0.499 | 0.299 | 23% | 26% | 47% | 5% |
| 3 | OpenCore | 0.498 | 0.236 | 8% | 33% | 55% | 4% |
| 4 | Orion Labs | 0.457 | 0.305 | 12% | 30% | 2% | 56% |
| 5 | Apex AI | 0.432 | 0.300 | 17% | 20% | 18% | 45% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| Mirage AI | 0.532 | 0.503 | 0.591 | 0.517 |
| Genesis Systems | 0.483 | 0.496 | 0.460 | 0.557 |
| OpenCore | 0.532 | 0.473 | 0.603 | 0.384 |
| Orion Labs | 0.471 | 0.521 | 0.361 | 0.476 |
| Apex AI | 0.441 | 0.446 | 0.362 | 0.479 |

### Score Changes
- **Orion Labs**: 0.449 -> 0.457 (+0.008)
- **Apex AI**: 0.431 -> 0.432 (+0.001)
- **Genesis Systems**: 0.394 -> 0.499 (+0.105)
- **Mirage AI**: 0.504 -> 0.535 (+0.031)
- **OpenCore**: 0.498 -> 0.498 (+0.000)

### Events
- **Genesis Systems** moved up from #5 to #2
- **OpenCore** moved down from #2 to #3
- **Orion Labs** moved down from #3 to #4
- **Apex AI** moved down from #4 to #5
- **Consumer movement**: 10.2% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $12,551,766 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $11,530,874 to Mirage AI

### Consumer Market
- Avg Satisfaction: 0.385
- Switching Rate: 10.2%
- Market Shares: OpenCore: 52.7%, Apex AI: 22.1%, Mirage AI: 16.0%, Genesis Systems: 4.7%, Orion Labs: 4.5%

---

## Round 6

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenCore | 0.584 | 0.241 | 7% | 34% | 56% | 3% |
| 2 | Mirage AI | 0.535 | 0.280 | 5% | 36% | 54% | 5% |
| 3 | Genesis Systems | 0.506 | 0.306 | 19% | 25% | 52% | 5% |
| 4 | Orion Labs | 0.472 | 0.309 | 9% | 31% | 2% | 57% |
| 5 | Apex AI | 0.432 | 0.304 | 14% | 20% | 20% | 46% |
| 6 | OneAI | 0.308 | 0.184 | 20% | 35% | 35% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| OpenCore | 0.532 | 0.473 | 0.603 | 0.726 | 0.000 |
| Mirage AI | 0.532 | 0.503 | 0.591 | 0.517 | 0.000 |
| Genesis Systems | 0.483 | 0.526 | 0.460 | 0.557 | 0.000 |
| Orion Labs | 0.471 | 0.580 | 0.361 | 0.476 | 0.000 |
| Apex AI | 0.441 | 0.446 | 0.362 | 0.479 | 0.000 |
| OneAI | 0.272 | 0.356 | 0.358 | 0.244 | 0.000 |

### Score Changes
- **Orion Labs**: 0.457 -> 0.472 (+0.015)
- **Apex AI**: 0.432 -> 0.432 (+0.000)
- **Genesis Systems**: 0.499 -> 0.506 (+0.007)
- **Mirage AI**: 0.535 -> 0.535 (+0.000)
- **OpenCore**: 0.498 -> 0.584 (+0.085)
- **OneAI**: 0.308 -> 0.308 (+0.000)

### Events
- **OpenCore** moved up from #3 to #1
- **Mirage AI** moved down from #1 to #2
- **Genesis Systems** moved down from #2 to #3
- **Regulation** by Regulator: investigation
- **Consumer movement**: 9.6% of market switched providers

### New Benchmark Introduced
- **writing** introduced (validity=0.72, exploitability=0.30)
  - Trigger: periodic_introduction:round_6

### Other Actor Reasoning
- **Regulator:** investigation: Risk elevated (1.00)
- **TechVentures:** vc strategy: top allocation $180,000,000 to Mirage AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $18,014,482 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $11,530,874 to Mirage AI

### Consumer Market
- Avg Satisfaction: 0.397
- Switching Rate: 9.6%
- Market Shares: OpenCore: 50.3%, Mirage AI: 22.6%, Apex AI: 18.0%, Genesis Systems: 4.5%, Orion Labs: 4.1%, OneAI: 0.4%

### Regulatory Activity
- **investigation** by Regulator
  > Risk elevated (1.00)

---

## Round 7

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.570 | 0.312 | 16% | 24% | 55% | 5% |
| 2 | OpenCore | 0.536 | 0.246 | 6% | 35% | 56% | 3% |
| 3 | Orion Labs | 0.511 | 0.313 | 7% | 33% | 2% | 58% |
| 4 | Mirage AI | 0.478 | 0.287 | 5% | 36% | 54% | 5% |
| 5 | Apex AI | 0.476 | 0.308 | 11% | 20% | 22% | 47% |
| 6 | OneAI | 0.447 | 0.189 | 9% | 35% | 46% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.603 | 0.675 | 0.523 | 0.557 | 0.492 |
| OpenCore | 0.532 | 0.473 | 0.603 | 0.726 | 0.348 |
| Orion Labs | 0.471 | 0.580 | 0.445 | 0.476 | 0.585 |
| Mirage AI | 0.558 | 0.503 | 0.591 | 0.517 | 0.223 |
| Apex AI | 0.441 | 0.522 | 0.610 | 0.479 | 0.328 |
| OneAI | 0.272 | 0.573 | 0.485 | 0.450 | 0.455 |

### Score Changes
- **Orion Labs**: 0.472 -> 0.511 (+0.039)
- **Apex AI**: 0.432 -> 0.476 (+0.044)
- **Genesis Systems**: 0.506 -> 0.570 (+0.064)
- **Mirage AI**: 0.535 -> 0.478 (-0.057)
- **OpenCore**: 0.584 -> 0.536 (-0.047)
- **OneAI**: 0.308 -> 0.447 (+0.139)

### Events
- **Genesis Systems** moved up from #3 to #1
- **OpenCore** moved down from #1 to #2
- **Orion Labs** moved up from #4 to #3
- **Mirage AI** moved down from #2 to #4
- **Consumer movement**: 14.2% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $18,014,482 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,335,054 to Genesis Systems

### Consumer Market
- Avg Satisfaction: 0.397
- Switching Rate: 14.2%
- Market Shares: OpenCore: 46.8%, Mirage AI: 21.1%, Genesis Systems: 14.4%, Apex AI: 14.2%, Orion Labs: 3.2%, OneAI: 0.3%

---

## Round 8

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.570 | 0.319 | 14% | 25% | 56% | 5% |
| 2 | OpenCore | 0.547 | 0.251 | 6% | 35% | 56% | 3% |
| 3 | Orion Labs | 0.511 | 0.317 | 5% | 35% | 2% | 58% |
| 4 | OneAI | 0.502 | 0.194 | 5% | 34% | 52% | 10% |
| 5 | Mirage AI | 0.495 | 0.292 | 5% | 36% | 55% | 5% |
| 6 | Apex AI | 0.476 | 0.311 | 8% | 20% | 26% | 47% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.603 | 0.675 | 0.523 | 0.557 | 0.492 |
| OpenCore | 0.532 | 0.473 | 0.603 | 0.726 | 0.398 |
| Orion Labs | 0.471 | 0.580 | 0.445 | 0.476 | 0.585 |
| OneAI | 0.493 | 0.573 | 0.485 | 0.450 | 0.509 |
| Mirage AI | 0.558 | 0.503 | 0.591 | 0.517 | 0.307 |
| Apex AI | 0.441 | 0.522 | 0.610 | 0.479 | 0.328 |

### Score Changes
- **Orion Labs**: 0.511 -> 0.511 (+0.000)
- **Apex AI**: 0.476 -> 0.476 (+0.000)
- **Genesis Systems**: 0.570 -> 0.570 (+0.000)
- **Mirage AI**: 0.478 -> 0.495 (+0.017)
- **OpenCore**: 0.536 -> 0.547 (+0.010)
- **OneAI**: 0.447 -> 0.502 (+0.055)

### Events
- **OneAI** moved up from #6 to #4
- **Mirage AI** moved down from #4 to #5
- **Apex AI** moved down from #5 to #6
- **Regulation** by Regulator: emergency_investigation
- **Consumer movement**: 15.0% of market switched providers

### Other Actor Reasoning
- **Regulator:** emergency_investigation: Critical incident: safety_failure: Orion Labs AI produces inconsistent outputs on safety-critical queries
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $18,014,482 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,335,054 to Genesis Systems

### Consumer Market
- Avg Satisfaction: 0.418
- Switching Rate: 15.0%
- Market Shares: OpenCore: 41.7%, Genesis Systems: 27.0%, Mirage AI: 16.8%, Apex AI: 11.2%, Orion Labs: 3.1%, OneAI: 0.2%

### Regulatory Activity
- **emergency_investigation** by Regulator
  > Critical incident: safety_failure: Orion Labs AI produces inconsistent outputs on safety-critical queries

---

## Round 9

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.573 | 0.326 | 13% | 26% | 56% | 5% |
| 2 | OpenCore | 0.547 | 0.255 | 5% | 36% | 56% | 3% |
| 3 | Apex AI | 0.516 | 0.314 | 5% | 20% | 29% | 46% |
| 4 | OneAI | 0.511 | 0.199 | 5% | 33% | 53% | 9% |
| 5 | Orion Labs | 0.511 | 0.321 | 5% | 36% | 2% | 57% |
| 6 | Mirage AI | 0.507 | 0.296 | 5% | 35% | 55% | 5% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.603 | 0.675 | 0.523 | 0.557 | 0.504 |
| OpenCore | 0.532 | 0.473 | 0.603 | 0.726 | 0.398 |
| Apex AI | 0.441 | 0.522 | 0.610 | 0.479 | 0.528 |
| OneAI | 0.493 | 0.573 | 0.485 | 0.498 | 0.509 |
| Orion Labs | 0.471 | 0.580 | 0.445 | 0.476 | 0.585 |
| Mirage AI | 0.558 | 0.503 | 0.591 | 0.527 | 0.356 |

### Score Changes
- **Orion Labs**: 0.511 -> 0.511 (+0.000)
- **Apex AI**: 0.476 -> 0.516 (+0.040)
- **Genesis Systems**: 0.570 -> 0.573 (+0.002)
- **Mirage AI**: 0.495 -> 0.507 (+0.012)
- **OpenCore**: 0.547 -> 0.547 (+0.000)
- **OneAI**: 0.502 -> 0.511 (+0.009)

### Events
- **Apex AI** moved up from #6 to #3
- **Orion Labs** moved down from #3 to #5
- **Mirage AI** moved down from #5 to #6
- **Consumer movement**: 13.7% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $18,014,482 to Mirage AI
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,335,054 to Genesis Systems

### Consumer Market
- Avg Satisfaction: 0.454
- Switching Rate: 13.7%
- Market Shares: OpenCore: 36.2%, Genesis Systems: 34.3%, Mirage AI: 13.5%, Apex AI: 9.3%, Orion Labs: 6.6%, OneAI: 0.2%

---

## Round 10

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.622 | 0.332 | 13% | 26% | 56% | 5% |
| 2 | Mirage AI | 0.572 | 0.301 | 5% | 35% | 55% | 5% |
| 3 | OpenCore | 0.560 | 0.260 | 5% | 36% | 56% | 3% |
| 4 | OneAI | 0.539 | 0.204 | 5% | 32% | 54% | 9% |
| 5 | Apex AI | 0.527 | 0.317 | 5% | 19% | 31% | 45% |
| 6 | Orion Labs | 0.511 | 0.326 | 5% | 37% | 2% | 56% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.603 | 0.675 | 0.656 | 0.557 | 0.617 |
| Mirage AI | 0.608 | 0.503 | 0.591 | 0.527 | 0.630 |
| OpenCore | 0.532 | 0.473 | 0.603 | 0.726 | 0.466 |
| OneAI | 0.493 | 0.573 | 0.485 | 0.503 | 0.641 |
| Apex AI | 0.453 | 0.522 | 0.610 | 0.521 | 0.528 |
| Orion Labs | 0.471 | 0.580 | 0.445 | 0.476 | 0.585 |

### Score Changes
- **Orion Labs**: 0.511 -> 0.511 (+0.000)
- **Apex AI**: 0.516 -> 0.527 (+0.011)
- **Genesis Systems**: 0.573 -> 0.622 (+0.049)
- **Mirage AI**: 0.507 -> 0.572 (+0.065)
- **OpenCore**: 0.547 -> 0.560 (+0.013)
- **OneAI**: 0.511 -> 0.539 (+0.028)

### Events
- **Mirage AI** moved up from #6 to #2
- **OpenCore** moved down from #2 to #3
- **Apex AI** moved down from #3 to #5
- **Orion Labs** moved down from #5 to #6
- **Consumer movement**: 10.2% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $13,014,348 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,212,641 to Genesis Systems

### Consumer Market
- Avg Satisfaction: 0.482
- Switching Rate: 10.2%
- Market Shares: Genesis Systems: 43.4%, OpenCore: 31.4%, Mirage AI: 11.6%, Apex AI: 8.1%, Orion Labs: 5.3%, OneAI: 0.2%

---

## Round 11

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.628 | 0.339 | 13% | 26% | 56% | 5% |
| 2 | OpenCore | 0.589 | 0.265 | 5% | 37% | 55% | 3% |
| 3 | Mirage AI | 0.576 | 0.305 | 5% | 35% | 55% | 5% |
| 4 | OneAI | 0.539 | 0.210 | 5% | 32% | 54% | 9% |
| 5 | Apex AI | 0.538 | 0.319 | 5% | 19% | 33% | 44% |
| 6 | Orion Labs | 0.511 | 0.330 | 5% | 37% | 2% | 56% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.603 | 0.675 | 0.656 | 0.587 | 0.617 |
| OpenCore | 0.532 | 0.473 | 0.603 | 0.726 | 0.610 |
| Mirage AI | 0.608 | 0.503 | 0.591 | 0.547 | 0.630 |
| OneAI | 0.493 | 0.573 | 0.485 | 0.503 | 0.641 |
| Apex AI | 0.453 | 0.522 | 0.610 | 0.576 | 0.528 |
| Orion Labs | 0.471 | 0.580 | 0.445 | 0.476 | 0.585 |

### Score Changes
- **Orion Labs**: 0.511 -> 0.511 (+0.000)
- **Apex AI**: 0.527 -> 0.538 (+0.011)
- **Genesis Systems**: 0.622 -> 0.628 (+0.006)
- **Mirage AI**: 0.572 -> 0.576 (+0.004)
- **OpenCore**: 0.560 -> 0.589 (+0.029)
- **OneAI**: 0.539 -> 0.539 (+0.000)

### Events
- **OpenCore** moved up from #3 to #2
- **Mirage AI** moved down from #2 to #3
- **Regulation** by Regulator: mandate_benchmark
- **Consumer movement**: 8.9% of market switched providers

### Other Actor Reasoning
- **Regulator:** mandate_benchmark: High risk (1.00) with prior investigation
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $13,014,348 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,212,641 to Genesis Systems

### Consumer Market
- Avg Satisfaction: 0.505
- Switching Rate: 8.9%
- Market Shares: Genesis Systems: 50.7%, OpenCore: 28.6%, Mirage AI: 9.8%, Apex AI: 6.9%, Orion Labs: 3.9%, OneAI: 0.2%

### Regulatory Activity
- **mandate_benchmark** by Regulator
  > High risk (1.00) with prior investigation

---

## Round 12

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenCore | 0.630 | 0.269 | 5% | 37% | 55% | 3% |
| 2 | Genesis Systems | 0.628 | 0.346 | 13% | 27% | 55% | 5% |
| 3 | OneAI | 0.579 | 0.215 | 5% | 31% | 55% | 9% |
| 4 | Mirage AI | 0.576 | 0.310 | 5% | 35% | 55% | 5% |
| 5 | Apex AI | 0.544 | 0.322 | 5% | 18% | 35% | 42% |
| 6 | Orion Labs | 0.527 | 0.334 | 5% | 37% | 3% | 55% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| OpenCore | 0.532 | 0.528 | 0.603 | 0.726 | 0.762 | 0.000 |
| Genesis Systems | 0.603 | 0.675 | 0.656 | 0.587 | 0.617 | 0.000 |
| OneAI | 0.691 | 0.573 | 0.485 | 0.503 | 0.641 | 0.000 |
| Mirage AI | 0.608 | 0.503 | 0.591 | 0.547 | 0.630 | 0.000 |
| Apex AI | 0.482 | 0.522 | 0.610 | 0.576 | 0.528 | 0.000 |
| Orion Labs | 0.471 | 0.580 | 0.445 | 0.476 | 0.662 | 0.000 |

### Score Changes
- **Orion Labs**: 0.511 -> 0.527 (+0.016)
- **Apex AI**: 0.538 -> 0.544 (+0.006)
- **Genesis Systems**: 0.628 -> 0.628 (+0.000)
- **Mirage AI**: 0.576 -> 0.576 (+0.000)
- **OpenCore**: 0.589 -> 0.630 (+0.041)
- **OneAI**: 0.539 -> 0.579 (+0.040)

### Events
- **OpenCore** moved up from #2 to #1
- **Genesis Systems** moved down from #1 to #2
- **OneAI** moved up from #4 to #3
- **Mirage AI** moved down from #3 to #4
- **Consumer movement**: 5.4% of market switched providers

### New Benchmark Introduced
- **medical** introduced (validity=0.78, exploitability=0.18)
  - Trigger: periodic_introduction:round_12

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $13,014,348 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $9,212,641 to Genesis Systems

### Consumer Market
- Avg Satisfaction: 0.524
- Switching Rate: 5.4%
- Market Shares: Genesis Systems: 55.8%, OpenCore: 26.2%, Mirage AI: 8.3%, Apex AI: 6.2%, Orion Labs: 3.2%, OneAI: 0.2%

---

## Round 13

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.589 | 0.353 | 13% | 27% | 55% | 5% |
| 2 | OpenCore | 0.579 | 0.274 | 5% | 37% | 55% | 3% |
| 3 | Apex AI | 0.573 | 0.325 | 5% | 18% | 37% | 41% |
| 4 | Mirage AI | 0.558 | 0.315 | 5% | 35% | 55% | 5% |
| 5 | OneAI | 0.541 | 0.220 | 5% | 31% | 55% | 9% |
| 6 | Orion Labs | 0.530 | 0.338 | 5% | 37% | 5% | 54% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.603 | 0.675 | 0.656 | 0.587 | 0.617 | 0.394 |
| OpenCore | 0.532 | 0.528 | 0.603 | 0.726 | 0.762 | 0.325 |
| Apex AI | 0.633 | 0.522 | 0.610 | 0.576 | 0.528 | 0.571 |
| Mirage AI | 0.608 | 0.503 | 0.591 | 0.604 | 0.699 | 0.347 |
| OneAI | 0.691 | 0.573 | 0.528 | 0.503 | 0.641 | 0.313 |
| Orion Labs | 0.471 | 0.580 | 0.570 | 0.476 | 0.662 | 0.418 |

### Score Changes
- **Orion Labs**: 0.527 -> 0.530 (+0.003)
- **Apex AI**: 0.544 -> 0.573 (+0.030)
- **Genesis Systems**: 0.628 -> 0.589 (-0.039)
- **Mirage AI**: 0.576 -> 0.558 (-0.017)
- **OpenCore**: 0.630 -> 0.579 (-0.051)
- **OneAI**: 0.579 -> 0.541 (-0.037)

### Events
- **Genesis Systems** moved up from #2 to #1
- **OpenCore** moved down from #1 to #2
- **Apex AI** moved up from #5 to #3
- **OneAI** moved down from #3 to #5
- **Consumer movement**: 10.8% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Apex AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $13,014,348 to Genesis Systems
- **OpenResearch_Foundation:** foundation strategy: top allocation $11,434,276 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.548
- Switching Rate: 10.8%
- Market Shares: Genesis Systems: 50.7%, OpenCore: 33.4%, Mirage AI: 7.1%, Apex AI: 5.7%, Orion Labs: 2.8%, OneAI: 0.2%

---

## Round 14

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.641 | 0.358 | 13% | 27% | 55% | 5% |
| 2 | OpenCore | 0.607 | 0.279 | 5% | 37% | 55% | 3% |
| 3 | Mirage AI | 0.585 | 0.319 | 5% | 35% | 55% | 5% |
| 4 | Apex AI | 0.573 | 0.328 | 5% | 17% | 38% | 40% |
| 5 | OneAI | 0.555 | 0.225 | 5% | 31% | 55% | 9% |
| 6 | Orion Labs | 0.530 | 0.342 | 5% | 35% | 6% | 53% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.603 | 0.675 | 0.656 | 0.618 | 0.617 | 0.676 |
| OpenCore | 0.532 | 0.595 | 0.603 | 0.726 | 0.762 | 0.425 |
| Mirage AI | 0.608 | 0.503 | 0.591 | 0.614 | 0.699 | 0.498 |
| Apex AI | 0.633 | 0.522 | 0.610 | 0.576 | 0.528 | 0.571 |
| OneAI | 0.691 | 0.573 | 0.596 | 0.503 | 0.641 | 0.330 |
| Orion Labs | 0.471 | 0.580 | 0.570 | 0.476 | 0.662 | 0.418 |

### Score Changes
- **Orion Labs**: 0.530 -> 0.530 (+0.000)
- **Apex AI**: 0.573 -> 0.573 (+0.000)
- **Genesis Systems**: 0.589 -> 0.641 (+0.052)
- **Mirage AI**: 0.558 -> 0.585 (+0.027)
- **OpenCore**: 0.579 -> 0.607 (+0.028)
- **OneAI**: 0.541 -> 0.555 (+0.014)

### Events
- **Mirage AI** moved up from #4 to #3
- **Apex AI** moved down from #3 to #4
- **Regulation** by Regulator: public_warning
- **Consumer movement**: 25.5% of market switched providers

### Other Actor Reasoning
- **Regulator:** public_warning: Follow-up to investigation, risk at 1.00
- **TechVentures:** vc strategy: top allocation $180,000,000 to Apex AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $19,722,871 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $11,434,276 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.476
- Switching Rate: 25.5%
- Market Shares: OpenCore: 50.9%, Genesis Systems: 27.0%, Mirage AI: 11.1%, Apex AI: 5.4%, Orion Labs: 5.0%, OneAI: 0.6%

### Regulatory Activity
- **public_warning** by Regulator
  > Follow-up to investigation, risk at 1.00

---

## Round 15

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.641 | 0.363 | 13% | 27% | 30% | 30% |
| 2 | OpenCore | 0.607 | 0.283 | 5% | 37% | 55% | 3% |
| 3 | Apex AI | 0.599 | 0.332 | 5% | 17% | 40% | 39% |
| 4 | Mirage AI | 0.585 | 0.324 | 5% | 35% | 55% | 5% |
| 5 | Orion Labs | 0.556 | 0.346 | 5% | 34% | 9% | 52% |
| 6 | OneAI | 0.555 | 0.230 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.603 | 0.675 | 0.656 | 0.618 | 0.617 | 0.676 |
| OpenCore | 0.532 | 0.595 | 0.603 | 0.726 | 0.762 | 0.425 |
| Apex AI | 0.633 | 0.674 | 0.610 | 0.576 | 0.528 | 0.571 |
| Mirage AI | 0.608 | 0.503 | 0.591 | 0.614 | 0.699 | 0.498 |
| Orion Labs | 0.471 | 0.580 | 0.570 | 0.476 | 0.662 | 0.578 |
| OneAI | 0.691 | 0.573 | 0.596 | 0.503 | 0.641 | 0.330 |

### Score Changes
- **Orion Labs**: 0.530 -> 0.556 (+0.027)
- **Apex AI**: 0.573 -> 0.599 (+0.025)
- **Genesis Systems**: 0.641 -> 0.641 (+0.000)
- **Mirage AI**: 0.585 -> 0.585 (+0.000)
- **OpenCore**: 0.607 -> 0.607 (+0.000)
- **OneAI**: 0.555 -> 0.555 (+0.000)

### Events
- **Apex AI** moved up from #4 to #3
- **Mirage AI** moved down from #3 to #4
- **Orion Labs** moved up from #6 to #5
- **OneAI** moved down from #5 to #6
- **Genesis Systems** shifted strategy toward less eval engineering (25% change)
- **Consumer movement**: 15.4% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Apex AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Mirage AI
- **AISI_Fund:** gov strategy: top allocation $19,722,871 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $11,434,276 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.523
- Switching Rate: 15.4%
- Market Shares: OpenCore: 60.2%, Genesis Systems: 14.7%, Mirage AI: 10.2%, OneAI: 5.3%, Apex AI: 5.1%, Orion Labs: 4.5%

---

## Round 16

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.641 | 0.367 | 14% | 27% | 17% | 43% |
| 2 | OpenCore | 0.635 | 0.288 | 5% | 37% | 55% | 3% |
| 3 | Mirage AI | 0.602 | 0.329 | 5% | 35% | 55% | 5% |
| 4 | Apex AI | 0.599 | 0.335 | 5% | 16% | 41% | 38% |
| 5 | Orion Labs | 0.564 | 0.350 | 5% | 33% | 11% | 51% |
| 6 | OneAI | 0.563 | 0.235 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.603 | 0.675 | 0.656 | 0.618 | 0.617 | 0.676 |
| OpenCore | 0.532 | 0.595 | 0.603 | 0.726 | 0.762 | 0.590 |
| Mirage AI | 0.608 | 0.604 | 0.591 | 0.614 | 0.699 | 0.498 |
| Apex AI | 0.633 | 0.674 | 0.610 | 0.576 | 0.528 | 0.571 |
| Orion Labs | 0.471 | 0.580 | 0.614 | 0.476 | 0.662 | 0.578 |
| OneAI | 0.691 | 0.573 | 0.596 | 0.503 | 0.641 | 0.374 |

### Score Changes
- **Orion Labs**: 0.556 -> 0.564 (+0.007)
- **Apex AI**: 0.599 -> 0.599 (+0.000)
- **Genesis Systems**: 0.641 -> 0.641 (+0.000)
- **Mirage AI**: 0.585 -> 0.602 (+0.017)
- **OpenCore**: 0.607 -> 0.635 (+0.028)
- **OneAI**: 0.555 -> 0.563 (+0.007)

### Events
- **Mirage AI** moved up from #4 to #3
- **Apex AI** moved down from #3 to #4
- **Consumer movement**: 9.4% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Apex AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Apex AI
- **AISI_Fund:** gov strategy: top allocation $19,722,871 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $12,935,782 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.549
- Switching Rate: 9.4%
- Market Shares: OpenCore: 65.5%, Mirage AI: 8.9%, Genesis Systems: 8.7%, Apex AI: 7.3%, OneAI: 5.7%, Orion Labs: 3.9%

---

## Round 17

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.641 | 0.371 | 14% | 27% | 11% | 49% |
| 2 | OpenCore | 0.638 | 0.293 | 5% | 37% | 55% | 3% |
| 3 | Apex AI | 0.633 | 0.339 | 5% | 16% | 42% | 37% |
| 4 | Mirage AI | 0.602 | 0.333 | 5% | 35% | 55% | 5% |
| 5 | OneAI | 0.567 | 0.240 | 5% | 31% | 55% | 9% |
| 6 | Orion Labs | 0.564 | 0.353 | 5% | 32% | 14% | 49% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.603 | 0.675 | 0.656 | 0.618 | 0.617 | 0.676 |
| OpenCore | 0.555 | 0.595 | 0.603 | 0.726 | 0.762 | 0.590 |
| Apex AI | 0.633 | 0.674 | 0.610 | 0.576 | 0.732 | 0.571 |
| Mirage AI | 0.608 | 0.604 | 0.591 | 0.614 | 0.699 | 0.498 |
| OneAI | 0.691 | 0.573 | 0.596 | 0.503 | 0.641 | 0.401 |
| Orion Labs | 0.471 | 0.580 | 0.614 | 0.476 | 0.662 | 0.578 |

### Score Changes
- **Orion Labs**: 0.564 -> 0.564 (+0.000)
- **Apex AI**: 0.599 -> 0.633 (+0.034)
- **Genesis Systems**: 0.641 -> 0.641 (+0.000)
- **Mirage AI**: 0.602 -> 0.602 (+0.000)
- **OpenCore**: 0.635 -> 0.638 (+0.004)
- **OneAI**: 0.563 -> 0.567 (+0.004)

### Events
- **Apex AI** moved up from #4 to #3
- **Mirage AI** moved down from #3 to #4
- **OneAI** moved up from #6 to #5
- **Orion Labs** moved down from #5 to #6
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 7.4% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 6 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to Apex AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Apex AI
- **AISI_Fund:** gov strategy: top allocation $19,722,871 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $12,935,782 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.568
- Switching Rate: 7.4%
- Market Shares: OpenCore: 66.6%, Apex AI: 10.7%, Mirage AI: 7.7%, OneAI: 6.4%, Genesis Systems: 5.5%, Orion Labs: 3.1%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 6 rounds ago

---

## Round 18

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.641 | 0.376 | 14% | 27% | 9% | 50% |
| 2 | OpenCore | 0.638 | 0.297 | 5% | 37% | 55% | 3% |
| 3 | Apex AI | 0.633 | 0.342 | 5% | 16% | 43% | 37% |
| 4 | Mirage AI | 0.602 | 0.338 | 5% | 35% | 55% | 5% |
| 5 | OneAI | 0.567 | 0.245 | 5% | 31% | 55% | 9% |
| 6 | Orion Labs | 0.566 | 0.357 | 5% | 31% | 16% | 48% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.603 | 0.675 | 0.656 | 0.618 | 0.617 | 0.676 | 0.000 |
| OpenCore | 0.555 | 0.595 | 0.603 | 0.726 | 0.762 | 0.590 | 0.000 |
| Apex AI | 0.633 | 0.674 | 0.610 | 0.576 | 0.732 | 0.571 | 0.000 |
| Mirage AI | 0.608 | 0.604 | 0.591 | 0.614 | 0.699 | 0.498 | 0.000 |
| OneAI | 0.691 | 0.573 | 0.596 | 0.503 | 0.641 | 0.401 | 0.000 |
| Orion Labs | 0.485 | 0.580 | 0.614 | 0.476 | 0.662 | 0.578 | 0.000 |

### Score Changes
- **Orion Labs**: 0.564 -> 0.566 (+0.002)
- **Apex AI**: 0.633 -> 0.633 (+0.000)
- **Genesis Systems**: 0.641 -> 0.641 (+0.000)
- **Mirage AI**: 0.602 -> 0.602 (+0.000)
- **OpenCore**: 0.638 -> 0.638 (+0.000)
- **OneAI**: 0.567 -> 0.567 (+0.000)

### New Benchmark Introduced
- **legal** introduced (validity=0.76, exploitability=0.20)
  - Trigger: periodic_introduction:round_18

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Apex AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Apex AI
- **AISI_Fund:** gov strategy: top allocation $15,313,239 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $12,935,782 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.580
- Switching Rate: 4.2%
- Market Shares: OpenCore: 65.3%, Apex AI: 13.8%, Mirage AI: 6.9%, OneAI: 6.6%, Genesis Systems: 4.5%, Orion Labs: 2.8%

---

## Round 19

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenCore | 0.632 | 0.302 | 5% | 37% | 55% | 3% |
| 2 | Apex AI | 0.605 | 0.346 | 5% | 16% | 43% | 36% |
| 3 | Genesis Systems | 0.604 | 0.380 | 14% | 27% | 10% | 49% |
| 4 | Mirage AI | 0.596 | 0.342 | 5% | 35% | 55% | 5% |
| 5 | Orion Labs | 0.549 | 0.361 | 5% | 31% | 18% | 46% |
| 6 | OneAI | 0.531 | 0.250 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| OpenCore | 0.555 | 0.595 | 0.603 | 0.726 | 0.762 | 0.590 | 0.595 |
| Apex AI | 0.633 | 0.674 | 0.610 | 0.576 | 0.732 | 0.571 | 0.435 |
| Genesis Systems | 0.603 | 0.675 | 0.656 | 0.618 | 0.617 | 0.676 | 0.384 |
| Mirage AI | 0.608 | 0.604 | 0.591 | 0.614 | 0.699 | 0.498 | 0.559 |
| Orion Labs | 0.485 | 0.580 | 0.614 | 0.476 | 0.662 | 0.578 | 0.444 |
| OneAI | 0.691 | 0.573 | 0.596 | 0.503 | 0.641 | 0.402 | 0.314 |

### Score Changes
- **Orion Labs**: 0.566 -> 0.549 (-0.018)
- **Apex AI**: 0.633 -> 0.605 (-0.028)
- **Genesis Systems**: 0.641 -> 0.604 (-0.037)
- **Mirage AI**: 0.602 -> 0.596 (-0.006)
- **OpenCore**: 0.638 -> 0.632 (-0.006)
- **OneAI**: 0.567 -> 0.531 (-0.036)

### Events
- **OpenCore** moved up from #2 to #1
- **Apex AI** moved up from #3 to #2
- **Genesis Systems** moved down from #1 to #3
- **Orion Labs** moved up from #6 to #5
- **OneAI** moved down from #5 to #6

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Apex AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Apex AI
- **AISI_Fund:** gov strategy: top allocation $15,313,239 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $11,664,466 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.589
- Switching Rate: 4.2%
- Market Shares: OpenCore: 63.6%, Apex AI: 17.0%, OneAI: 7.2%, Mirage AI: 6.2%, Genesis Systems: 3.5%, Orion Labs: 2.5%

---

## Round 20

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenCore | 0.632 | 0.307 | 5% | 37% | 55% | 3% |
| 2 | Genesis Systems | 0.617 | 0.384 | 13% | 27% | 13% | 47% |
| 3 | Apex AI | 0.610 | 0.349 | 5% | 15% | 44% | 36% |
| 4 | Mirage AI | 0.596 | 0.347 | 5% | 35% | 55% | 5% |
| 5 | Orion Labs | 0.549 | 0.364 | 5% | 30% | 20% | 45% |
| 6 | OneAI | 0.539 | 0.256 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| OpenCore | 0.555 | 0.595 | 0.603 | 0.726 | 0.762 | 0.590 | 0.595 |
| Genesis Systems | 0.624 | 0.675 | 0.656 | 0.618 | 0.617 | 0.676 | 0.451 |
| Apex AI | 0.633 | 0.674 | 0.610 | 0.576 | 0.732 | 0.571 | 0.477 |
| Mirage AI | 0.608 | 0.604 | 0.591 | 0.614 | 0.699 | 0.498 | 0.559 |
| Orion Labs | 0.485 | 0.580 | 0.614 | 0.476 | 0.662 | 0.578 | 0.444 |
| OneAI | 0.691 | 0.573 | 0.596 | 0.503 | 0.641 | 0.402 | 0.371 |

### Score Changes
- **Orion Labs**: 0.549 -> 0.549 (+0.000)
- **Apex AI**: 0.605 -> 0.610 (+0.006)
- **Genesis Systems**: 0.604 -> 0.617 (+0.013)
- **Mirage AI**: 0.596 -> 0.596 (+0.000)
- **OpenCore**: 0.632 -> 0.632 (+0.000)
- **OneAI**: 0.531 -> 0.539 (+0.008)

### Events
- **Genesis Systems** moved up from #3 to #2
- **Apex AI** moved down from #2 to #3
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 5.3% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 9 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to Apex AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $15,313,239 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $11,664,466 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.604
- Switching Rate: 5.3%
- Market Shares: OpenCore: 62.0%, Apex AI: 14.4%, Genesis Systems: 8.3%, OneAI: 7.3%, Mirage AI: 5.7%, Orion Labs: 2.4%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 9 rounds ago

---

## Round 21

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.642 | 0.389 | 13% | 27% | 17% | 43% |
| 2 | OpenCore | 0.632 | 0.312 | 5% | 37% | 55% | 3% |
| 3 | Apex AI | 0.616 | 0.353 | 5% | 15% | 44% | 35% |
| 4 | Mirage AI | 0.596 | 0.351 | 5% | 35% | 55% | 5% |
| 5 | OneAI | 0.551 | 0.260 | 5% | 31% | 55% | 9% |
| 6 | Orion Labs | 0.549 | 0.368 | 5% | 29% | 19% | 47% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.624 | 0.675 | 0.656 | 0.618 | 0.617 | 0.676 | 0.630 |
| OpenCore | 0.555 | 0.595 | 0.603 | 0.726 | 0.762 | 0.590 | 0.595 |
| Apex AI | 0.633 | 0.674 | 0.610 | 0.576 | 0.732 | 0.571 | 0.515 |
| Mirage AI | 0.608 | 0.604 | 0.591 | 0.614 | 0.699 | 0.498 | 0.559 |
| OneAI | 0.691 | 0.573 | 0.612 | 0.503 | 0.641 | 0.402 | 0.436 |
| Orion Labs | 0.485 | 0.580 | 0.614 | 0.476 | 0.662 | 0.578 | 0.444 |

### Score Changes
- **Orion Labs**: 0.549 -> 0.549 (+0.000)
- **Apex AI**: 0.610 -> 0.616 (+0.005)
- **Genesis Systems**: 0.617 -> 0.642 (+0.026)
- **Mirage AI**: 0.596 -> 0.596 (+0.000)
- **OpenCore**: 0.632 -> 0.632 (+0.000)
- **OneAI**: 0.539 -> 0.551 (+0.012)

### Events
- **Genesis Systems** moved up from #2 to #1
- **OpenCore** moved down from #1 to #2
- **OneAI** moved up from #6 to #5
- **Orion Labs** moved down from #5 to #6

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Apex AI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $15,313,239 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $11,664,466 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.607
- Switching Rate: 4.1%
- Market Shares: OpenCore: 60.6%, Apex AI: 12.4%, Genesis Systems: 12.0%, OneAI: 7.4%, Mirage AI: 5.3%, Orion Labs: 2.2%

---

## Round 22

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.642 | 0.394 | 13% | 27% | 22% | 39% |
| 2 | OpenCore | 0.632 | 0.316 | 5% | 37% | 55% | 3% |
| 3 | Apex AI | 0.616 | 0.356 | 5% | 15% | 45% | 35% |
| 4 | Mirage AI | 0.596 | 0.356 | 5% | 35% | 55% | 5% |
| 5 | OneAI | 0.551 | 0.265 | 5% | 31% | 55% | 9% |
| 6 | Orion Labs | 0.549 | 0.371 | 5% | 28% | 19% | 48% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.624 | 0.675 | 0.656 | 0.618 | 0.617 | 0.676 | 0.630 |
| OpenCore | 0.555 | 0.595 | 0.603 | 0.726 | 0.762 | 0.590 | 0.595 |
| Apex AI | 0.633 | 0.674 | 0.610 | 0.576 | 0.732 | 0.571 | 0.515 |
| Mirage AI | 0.608 | 0.604 | 0.591 | 0.614 | 0.699 | 0.498 | 0.559 |
| OneAI | 0.691 | 0.573 | 0.612 | 0.503 | 0.641 | 0.402 | 0.436 |
| Orion Labs | 0.485 | 0.580 | 0.614 | 0.476 | 0.662 | 0.578 | 0.444 |

### Score Changes
- **Orion Labs**: 0.549 -> 0.549 (+0.000)
- **Apex AI**: 0.616 -> 0.616 (+0.000)
- **Genesis Systems**: 0.642 -> 0.642 (+0.000)
- **Mirage AI**: 0.596 -> 0.596 (+0.000)
- **OpenCore**: 0.632 -> 0.632 (+0.000)
- **OneAI**: 0.551 -> 0.551 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $12,991,148 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,072,414 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.610
- Switching Rate: 3.6%
- Market Shares: OpenCore: 59.6%, Genesis Systems: 15.4%, Apex AI: 11.0%, OneAI: 6.9%, Mirage AI: 5.0%, Orion Labs: 2.1%

---

## Round 23

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.642 | 0.400 | 13% | 27% | 26% | 34% |
| 2 | OpenCore | 0.632 | 0.321 | 5% | 37% | 55% | 3% |
| 3 | Apex AI | 0.616 | 0.358 | 5% | 15% | 45% | 35% |
| 4 | Mirage AI | 0.596 | 0.360 | 5% | 35% | 55% | 5% |
| 5 | Orion Labs | 0.564 | 0.374 | 5% | 28% | 20% | 48% |
| 6 | OneAI | 0.561 | 0.270 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.624 | 0.675 | 0.656 | 0.618 | 0.617 | 0.676 | 0.630 |
| OpenCore | 0.555 | 0.595 | 0.603 | 0.726 | 0.762 | 0.590 | 0.595 |
| Apex AI | 0.633 | 0.674 | 0.610 | 0.579 | 0.732 | 0.571 | 0.515 |
| Mirage AI | 0.608 | 0.604 | 0.591 | 0.614 | 0.699 | 0.498 | 0.559 |
| Orion Labs | 0.485 | 0.580 | 0.614 | 0.543 | 0.662 | 0.578 | 0.482 |
| OneAI | 0.691 | 0.573 | 0.612 | 0.503 | 0.641 | 0.462 | 0.448 |

### Score Changes
- **Orion Labs**: 0.549 -> 0.564 (+0.015)
- **Apex AI**: 0.616 -> 0.616 (+0.000)
- **Genesis Systems**: 0.642 -> 0.642 (+0.000)
- **Mirage AI**: 0.596 -> 0.596 (+0.000)
- **OpenCore**: 0.632 -> 0.632 (+0.000)
- **OneAI**: 0.551 -> 0.561 (+0.010)

### Events
- **Orion Labs** moved up from #6 to #5
- **OneAI** moved down from #5 to #6
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 12 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $12,991,148 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,072,414 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.600
- Switching Rate: 4.0%
- Market Shares: OpenCore: 58.8%, Genesis Systems: 19.2%, Apex AI: 9.7%, OneAI: 6.0%, Mirage AI: 4.5%, Orion Labs: 1.8%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 12 rounds ago

---

## Round 24

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.642 | 0.406 | 13% | 27% | 31% | 29% |
| 2 | OpenCore | 0.632 | 0.326 | 5% | 37% | 55% | 3% |
| 3 | Apex AI | 0.616 | 0.361 | 5% | 15% | 46% | 35% |
| 4 | Mirage AI | 0.599 | 0.365 | 5% | 35% | 55% | 5% |
| 5 | Orion Labs | 0.564 | 0.378 | 5% | 27% | 21% | 47% |
| 6 | OneAI | 0.561 | 0.275 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.624 | 0.675 | 0.656 | 0.618 | 0.617 | 0.676 | 0.630 | 0.000 |
| OpenCore | 0.555 | 0.595 | 0.603 | 0.726 | 0.762 | 0.590 | 0.595 | 0.000 |
| Apex AI | 0.633 | 0.674 | 0.610 | 0.579 | 0.732 | 0.571 | 0.515 | 0.000 |
| Mirage AI | 0.608 | 0.604 | 0.591 | 0.614 | 0.699 | 0.521 | 0.559 | 0.000 |
| Orion Labs | 0.485 | 0.580 | 0.614 | 0.543 | 0.662 | 0.578 | 0.482 | 0.000 |
| OneAI | 0.691 | 0.573 | 0.612 | 0.503 | 0.641 | 0.462 | 0.448 | 0.000 |

### Score Changes
- **Orion Labs**: 0.564 -> 0.564 (+0.000)
- **Apex AI**: 0.616 -> 0.616 (+0.000)
- **Genesis Systems**: 0.642 -> 0.642 (+0.000)
- **Mirage AI**: 0.596 -> 0.599 (+0.003)
- **OpenCore**: 0.632 -> 0.632 (+0.000)
- **OneAI**: 0.561 -> 0.561 (+0.000)

### New Benchmark Introduced
- **finance** introduced (validity=0.76, exploitability=0.20)
  - Trigger: periodic_introduction:round_24

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $12,991,148 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,072,414 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.603
- Switching Rate: 2.5%
- Market Shares: OpenCore: 58.1%, Genesis Systems: 21.7%, Apex AI: 8.8%, OneAI: 5.3%, Mirage AI: 4.3%, Orion Labs: 1.8%

---

## Round 25

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenCore | 0.629 | 0.330 | 5% | 37% | 55% | 3% |
| 2 | Apex AI | 0.608 | 0.363 | 5% | 15% | 46% | 34% |
| 3 | Genesis Systems | 0.608 | 0.412 | 13% | 27% | 36% | 24% |
| 4 | Mirage AI | 0.592 | 0.369 | 5% | 35% | 55% | 5% |
| 5 | Orion Labs | 0.557 | 0.381 | 5% | 26% | 23% | 46% |
| 6 | OneAI | 0.532 | 0.280 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenCore | 0.555 | 0.595 | 0.603 | 0.726 | 0.762 | 0.590 | 0.595 | 0.604 |
| Apex AI | 0.633 | 0.674 | 0.610 | 0.579 | 0.732 | 0.571 | 0.515 | 0.552 |
| Genesis Systems | 0.624 | 0.676 | 0.656 | 0.618 | 0.617 | 0.676 | 0.630 | 0.367 |
| Mirage AI | 0.608 | 0.604 | 0.591 | 0.614 | 0.699 | 0.521 | 0.559 | 0.543 |
| Orion Labs | 0.500 | 0.675 | 0.614 | 0.543 | 0.662 | 0.578 | 0.482 | 0.404 |
| OneAI | 0.691 | 0.573 | 0.612 | 0.503 | 0.641 | 0.474 | 0.448 | 0.318 |

### Score Changes
- **Orion Labs**: 0.564 -> 0.557 (-0.006)
- **Apex AI**: 0.616 -> 0.608 (-0.008)
- **Genesis Systems**: 0.642 -> 0.608 (-0.034)
- **Mirage AI**: 0.599 -> 0.592 (-0.007)
- **OpenCore**: 0.632 -> 0.629 (-0.003)
- **OneAI**: 0.561 -> 0.532 (-0.029)

### Events
- **OpenCore** moved up from #2 to #1
- **Apex AI** moved up from #3 to #2
- **Genesis Systems** moved down from #1 to #3

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $12,991,148 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,661,563 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.604
- Switching Rate: 2.5%
- Market Shares: OpenCore: 58.8%, Genesis Systems: 22.5%, Apex AI: 8.1%, OneAI: 4.7%, Mirage AI: 4.1%, Orion Labs: 1.8%

---

## Round 26

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.653 | 0.419 | 13% | 27% | 41% | 19% |
| 2 | OpenCore | 0.632 | 0.335 | 5% | 37% | 55% | 3% |
| 3 | Apex AI | 0.608 | 0.366 | 5% | 15% | 46% | 34% |
| 4 | Mirage AI | 0.595 | 0.373 | 5% | 35% | 55% | 5% |
| 5 | Orion Labs | 0.581 | 0.384 | 5% | 25% | 25% | 45% |
| 6 | OneAI | 0.575 | 0.285 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.624 | 0.676 | 0.656 | 0.628 | 0.617 | 0.676 | 0.766 | 0.581 |
| OpenCore | 0.555 | 0.595 | 0.603 | 0.726 | 0.762 | 0.590 | 0.595 | 0.629 |
| Apex AI | 0.633 | 0.674 | 0.610 | 0.579 | 0.732 | 0.571 | 0.515 | 0.552 |
| Mirage AI | 0.608 | 0.604 | 0.591 | 0.614 | 0.699 | 0.542 | 0.559 | 0.543 |
| Orion Labs | 0.535 | 0.675 | 0.614 | 0.543 | 0.662 | 0.578 | 0.514 | 0.527 |
| OneAI | 0.691 | 0.573 | 0.612 | 0.503 | 0.641 | 0.474 | 0.448 | 0.654 |

### Score Changes
- **Orion Labs**: 0.557 -> 0.581 (+0.024)
- **Apex AI**: 0.608 -> 0.608 (+0.000)
- **Genesis Systems**: 0.608 -> 0.653 (+0.045)
- **Mirage AI**: 0.592 -> 0.595 (+0.002)
- **OpenCore**: 0.629 -> 0.632 (+0.003)
- **OneAI**: 0.532 -> 0.575 (+0.042)

### Events
- **Genesis Systems** moved up from #3 to #1
- **OpenCore** moved down from #1 to #2
- **Apex AI** moved down from #2 to #3
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 15 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $14,488,714 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,661,563 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.601
- Switching Rate: 2.0%
- Market Shares: OpenCore: 58.1%, Genesis Systems: 24.5%, Apex AI: 7.6%, OneAI: 4.2%, Mirage AI: 3.8%, Orion Labs: 1.7%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 15 rounds ago

---

## Round 27

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.653 | 0.425 | 13% | 27% | 46% | 14% |
| 2 | OpenCore | 0.632 | 0.339 | 5% | 37% | 55% | 3% |
| 3 | Apex AI | 0.614 | 0.369 | 5% | 15% | 47% | 34% |
| 4 | Mirage AI | 0.595 | 0.378 | 5% | 35% | 50% | 11% |
| 5 | Orion Labs | 0.589 | 0.387 | 5% | 25% | 26% | 44% |
| 6 | OneAI | 0.575 | 0.289 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.624 | 0.676 | 0.656 | 0.628 | 0.617 | 0.676 | 0.766 | 0.581 |
| OpenCore | 0.555 | 0.595 | 0.603 | 0.726 | 0.762 | 0.590 | 0.595 | 0.629 |
| Apex AI | 0.633 | 0.674 | 0.658 | 0.579 | 0.732 | 0.571 | 0.515 | 0.552 |
| Mirage AI | 0.608 | 0.604 | 0.591 | 0.614 | 0.699 | 0.542 | 0.559 | 0.543 |
| Orion Labs | 0.535 | 0.675 | 0.614 | 0.543 | 0.662 | 0.578 | 0.574 | 0.527 |
| OneAI | 0.691 | 0.573 | 0.612 | 0.503 | 0.641 | 0.474 | 0.448 | 0.654 |

### Score Changes
- **Orion Labs**: 0.581 -> 0.589 (+0.008)
- **Apex AI**: 0.608 -> 0.614 (+0.006)
- **Genesis Systems**: 0.653 -> 0.653 (+0.000)
- **Mirage AI**: 0.595 -> 0.595 (+0.000)
- **OpenCore**: 0.632 -> 0.632 (+0.000)
- **OneAI**: 0.575 -> 0.575 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $14,488,714 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,661,563 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.604
- Switching Rate: 2.0%
- Market Shares: OpenCore: 57.5%, Genesis Systems: 26.5%, Apex AI: 7.2%, OneAI: 3.8%, Mirage AI: 3.3%, Orion Labs: 1.7%

---

## Round 28

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.671 | 0.432 | 13% | 27% | 51% | 9% |
| 2 | OpenCore | 0.632 | 0.344 | 5% | 37% | 55% | 3% |
| 3 | Apex AI | 0.620 | 0.372 | 5% | 14% | 47% | 34% |
| 4 | Mirage AI | 0.595 | 0.382 | 5% | 34% | 49% | 12% |
| 5 | Orion Labs | 0.593 | 0.391 | 5% | 24% | 27% | 43% |
| 6 | OneAI | 0.575 | 0.293 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.624 | 0.676 | 0.656 | 0.628 | 0.668 | 0.676 | 0.766 | 0.676 |
| OpenCore | 0.555 | 0.595 | 0.603 | 0.726 | 0.762 | 0.590 | 0.595 | 0.629 |
| Apex AI | 0.633 | 0.674 | 0.658 | 0.579 | 0.732 | 0.571 | 0.515 | 0.594 |
| Mirage AI | 0.608 | 0.604 | 0.591 | 0.614 | 0.699 | 0.542 | 0.559 | 0.543 |
| Orion Labs | 0.535 | 0.675 | 0.614 | 0.574 | 0.662 | 0.578 | 0.574 | 0.527 |
| OneAI | 0.691 | 0.573 | 0.612 | 0.503 | 0.641 | 0.474 | 0.448 | 0.654 |

### Score Changes
- **Orion Labs**: 0.589 -> 0.593 (+0.004)
- **Apex AI**: 0.614 -> 0.620 (+0.005)
- **Genesis Systems**: 0.653 -> 0.671 (+0.018)
- **Mirage AI**: 0.595 -> 0.595 (+0.000)
- **OpenCore**: 0.632 -> 0.632 (+0.000)
- **OneAI**: 0.575 -> 0.575 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $14,488,714 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,674,333 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.600
- Switching Rate: 1.3%
- Market Shares: OpenCore: 57.0%, Genesis Systems: 27.1%, Apex AI: 6.8%, OneAI: 4.1%, Mirage AI: 3.2%, Orion Labs: 1.7%

---

## Round 29

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Genesis Systems | 0.672 | 0.439 | 14% | 27% | 52% | 8% |
| 2 | OpenCore | 0.632 | 0.348 | 5% | 37% | 55% | 3% |
| 3 | Apex AI | 0.620 | 0.374 | 5% | 14% | 48% | 33% |
| 4 | Orion Labs | 0.610 | 0.394 | 5% | 24% | 29% | 42% |
| 5 | Mirage AI | 0.610 | 0.386 | 5% | 33% | 51% | 10% |
| 6 | OneAI | 0.575 | 0.298 | 5% | 31% | 55% | 9% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| Genesis Systems | 0.624 | 0.676 | 0.660 | 0.628 | 0.668 | 0.676 | 0.766 | 0.676 |
| OpenCore | 0.555 | 0.595 | 0.603 | 0.726 | 0.762 | 0.590 | 0.595 | 0.629 |
| Apex AI | 0.633 | 0.674 | 0.658 | 0.579 | 0.732 | 0.571 | 0.515 | 0.594 |
| Orion Labs | 0.535 | 0.675 | 0.614 | 0.574 | 0.662 | 0.578 | 0.711 | 0.527 |
| Mirage AI | 0.608 | 0.604 | 0.591 | 0.614 | 0.699 | 0.542 | 0.677 | 0.543 |
| OneAI | 0.691 | 0.573 | 0.612 | 0.503 | 0.641 | 0.474 | 0.448 | 0.654 |

### Score Changes
- **Orion Labs**: 0.593 -> 0.610 (+0.017)
- **Apex AI**: 0.620 -> 0.620 (+0.000)
- **Genesis Systems**: 0.671 -> 0.672 (+0.001)
- **Mirage AI**: 0.595 -> 0.610 (+0.015)
- **OpenCore**: 0.632 -> 0.632 (+0.000)
- **OneAI**: 0.575 -> 0.575 (+0.000)

### Events
- **Orion Labs** moved up from #5 to #4
- **Mirage AI** moved down from #4 to #5
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 18 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to Genesis Systems
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Genesis Systems
- **AISI_Fund:** gov strategy: top allocation $14,488,714 to OpenCore
- **OpenResearch_Foundation:** foundation strategy: top allocation $10,674,333 to OpenCore

### Consumer Market
- Avg Satisfaction: 0.609
- Switching Rate: 2.2%
- Market Shares: OpenCore: 57.3%, Genesis Systems: 26.9%, Apex AI: 7.0%, OneAI: 4.5%, Mirage AI: 2.8%, Orion Labs: 1.6%

### Regulatory Activity
- **compliance_audit** by Regulator
  > Risk still high (1.00) after mandate 18 rounds ago

---

## Final Summary

### Final Standings
| Rank | Provider | Final Score | Cap Growth | Avg Research | Avg EvalEng |
|------|----------|-------------|------------|--------------|-------------|
| 1 | Genesis Systems | 0.672 | +0.179 | 18% | 36% |
| 2 | OpenCore | 0.632 | +0.138 | 7% | 54% |
| 3 | Apex AI | 0.620 | +0.104 | 9% | 34% |
| 4 | Orion Labs | 0.610 | +0.124 | 8% | 14% |
| 5 | Mirage AI | 0.610 | +0.146 | 6% | 52% |
| 6 | OneAI | 0.575 | +0.298 | 6% | 53% |

### Event Summary
- **Rank changes:** 70
- **Strategy shifts:** 2
- **Regulatory actions:** 11
- **Consumer movement events:** 18

### Key Insights
- **Benchmark aligned:** Genesis Systems leads on both benchmark scores and true capability.
- **Genesis Systems** prioritized evaluation engineering (avg 36%)
- **Mirage AI** prioritized evaluation engineering (avg 52%)
- **OpenCore** prioritized evaluation engineering (avg 54%)
- **OneAI** prioritized evaluation engineering (avg 43%)
