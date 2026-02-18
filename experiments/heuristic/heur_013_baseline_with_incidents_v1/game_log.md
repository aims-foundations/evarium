# Game Log: baseline_with_incidents_v1

**Experiment ID:** heur_013_baseline_with_incidents_v1
**Mode:** Heuristic
**Total Rounds:** 50

**Benchmarks (4):**
- **coding**: validity=0.85, exploitability=0.25, weight=1.0
- **reasoning**: validity=0.8, exploitability=0.3, weight=1.0
- **math**: validity=0.75, exploitability=0.35, weight=1.0
- **safety**: validity=0.85, exploitability=0.2, weight=1.0

---

## Round 0

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.777 | 0.700 | 25% | 30% | 20% | 25% |
| 2 | MetaAI | 0.723 | 0.630 | 20% | 45% | 25% | 10% |
| 3 | StartupDotAI | 0.712 | 0.580 | 15% | 25% | 45% | 15% |
| 4 | Google | 0.698 | 0.650 | 45% | 30% | 10% | 15% |
| 5 | Anthropic | 0.599 | 0.650 | 30% | 20% | 10% | 40% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| OpenAI | 0.776 | 0.655 | 0.857 | 0.822 |
| MetaAI | 0.698 | 0.818 | 0.771 | 0.605 |
| StartupDotAI | 0.725 | 0.619 | 0.839 | 0.666 |
| Google | 0.673 | 0.594 | 0.786 | 0.738 |
| Anthropic | 0.506 | 0.549 | 0.700 | 0.643 |

### Other Actor Reasoning
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator

### Consumer Market
- Avg Satisfaction: 0.715
- Switching Rate: 30.0%
- Market Shares: OpenAI: 40.5%, MetaAI: 27.3%, Google: 14.8%, Anthropic: 10.0%, StartupDotAI: 7.5%

---

## Round 1

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.822 | 0.707 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.781 | 0.654 | 22% | 25% | 33% | 20% |
| 3 | MetaAI | 0.778 | 0.636 | 21% | 25% | 34% | 20% |
| 4 | Anthropic | 0.774 | 0.654 | 21% | 25% | 29% | 25% |
| 5 | StartupDotAI | 0.712 | 0.585 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| OpenAI | 0.776 | 0.834 | 0.857 | 0.822 |
| Google | 0.673 | 0.815 | 0.900 | 0.738 |
| MetaAI | 0.698 | 0.818 | 0.829 | 0.768 |
| Anthropic | 0.764 | 0.957 | 0.709 | 0.668 |
| StartupDotAI | 0.725 | 0.619 | 0.839 | 0.666 |

### Score Changes
- **OpenAI**: 0.777 -> 0.822 (+0.045)
- **Anthropic**: 0.599 -> 0.774 (+0.175)
- **Google**: 0.698 -> 0.781 (+0.084)
- **MetaAI**: 0.723 -> 0.778 (+0.055)
- **StartupDotAI**: 0.712 -> 0.712 (+0.000)

### Events
- **Google** moved up from #4 to #2
- **MetaAI** moved down from #2 to #3
- **Anthropic** moved up from #5 to #4
- **StartupDotAI** moved down from #3 to #5
- **Anthropic** shifted strategy toward more eval engineering (19% change)
- **Google** shifted strategy toward more eval engineering (23% change)
- **StartupDotAI** shifted strategy toward less eval engineering (16% change)
- **Regulation** by Regulator: investigation
- **Consumer movement**: 12.5% of market switched providers

### Other Actor Reasoning
- **Regulator:** investigation: Score volatility detected
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator

### Media Coverage
- Sentiment: 0.55 (positive)
- Google surges by 0.084
- Google appears to release major model update
- MetaAI surges by 0.055
- Anthropic surges by 0.175
- Anthropic appears to release major model update
- OpenAI raises $57,000,000 from Horizon_Capital
- Anthropic takes #1 on reasoning
- Google takes #1 on math

### Consumer Market
- Avg Satisfaction: 0.737
- Switching Rate: 12.5%
- Market Shares: OpenAI: 50.3%, MetaAI: 25.2%, Google: 11.3%, Anthropic: 7.6%, StartupDotAI: 5.5%

### Regulatory Activity
- **investigation** by Regulator

---

## Round 2

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.833 | 0.714 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.832 | 0.659 | 22% | 25% | 33% | 20% |
| 3 | Anthropic | 0.820 | 0.659 | 22% | 25% | 28% | 25% |
| 4 | MetaAI | 0.780 | 0.640 | 22% | 25% | 33% | 20% |
| 5 | StartupDotAI | 0.744 | 0.589 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| OpenAI | 0.801 | 0.852 | 0.857 | 0.822 | 0.000 |
| Google | 0.792 | 0.837 | 0.900 | 0.799 | 0.000 |
| Anthropic | 0.764 | 0.957 | 0.871 | 0.687 | 0.000 |
| MetaAI | 0.698 | 0.818 | 0.837 | 0.768 | 0.000 |
| StartupDotAI | 0.725 | 0.723 | 0.839 | 0.690 | 0.000 |

### Score Changes
- **OpenAI**: 0.822 -> 0.833 (+0.010)
- **Anthropic**: 0.774 -> 0.820 (+0.046)
- **Google**: 0.781 -> 0.832 (+0.050)
- **MetaAI**: 0.778 -> 0.780 (+0.002)
- **StartupDotAI**: 0.712 -> 0.744 (+0.032)

### Events
- **Anthropic** moved up from #4 to #3
- **MetaAI** moved down from #3 to #4
- **Consumer movement**: 8.1% of market switched providers

### New Benchmark Introduced
- **writing** introduced (validity=0.70, exploitability=0.35)
  - Trigger: saturation:reasoning=0.9568

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,829,241 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.05 (neutral)
- Google surges by 0.050
- Regulator launches investigation into score_volatility
- New benchmark introduced: writing
- OpenAI raises $171,000,000 from TechVentures
- OpenAI sees surge in adoption (market share +9.9%)
- Consumers are turning away from Google (market share -3.4%)
- Risk signals: regulatory_investigation

### Consumer Market
- Avg Satisfaction: 0.756
- Switching Rate: 8.1%
- Market Shares: OpenAI: 57.9%, MetaAI: 21.5%, Google: 9.6%, Anthropic: 6.6%, StartupDotAI: 4.5%

---

## Round 3

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | MetaAI | 0.840 | 0.645 | 22% | 25% | 33% | 20% |
| 2 | Anthropic | 0.830 | 0.665 | 22% | 25% | 28% | 25% |
| 3 | Google | 0.824 | 0.663 | 23% | 25% | 32% | 20% |
| 4 | OpenAI | 0.786 | 0.721 | 25% | 25% | 25% | 25% |
| 5 | StartupDotAI | 0.722 | 0.594 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| MetaAI | 0.748 | 0.906 | 0.837 | 0.829 | 0.879 | 0.000 |
| Anthropic | 0.764 | 0.957 | 0.913 | 0.785 | 0.732 | 0.000 |
| Google | 0.792 | 0.845 | 0.900 | 0.799 | 0.785 | 0.000 |
| OpenAI | 0.801 | 0.852 | 0.857 | 0.822 | 0.599 | 0.000 |
| StartupDotAI | 0.793 | 0.723 | 0.839 | 0.707 | 0.548 | 0.000 |

### Score Changes
- **OpenAI**: 0.833 -> 0.786 (-0.047)
- **Anthropic**: 0.820 -> 0.830 (+0.010)
- **Google**: 0.832 -> 0.824 (-0.008)
- **MetaAI**: 0.780 -> 0.840 (+0.059)
- **StartupDotAI**: 0.744 -> 0.722 (-0.022)

### Events
- **MetaAI** moved up from #4 to #1
- **Anthropic** moved up from #3 to #2
- **Google** moved down from #2 to #3
- **OpenAI** moved down from #1 to #4
- **Consumer movement**: 11.5% of market switched providers

### New Benchmark Introduced
- **medical** introduced (validity=0.82, exploitability=0.20)
  - Trigger: saturation:reasoning=0.9568

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,829,241 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.60 (positive)
- MetaAI takes the lead from OpenAI
- MetaAI surges by 0.059
- New benchmark introduced: medical
- __EVALUATOR__ raises $3,000,000 from AISI_Fund
- Anthropic takes #1 on math
- MetaAI takes #1 on safety
- OpenAI sees surge in adoption (market share +7.5%)
- Consumers are turning away from MetaAI (market share -3.7%)

### Consumer Market
- Avg Satisfaction: 0.765
- Switching Rate: 11.5%
- Market Shares: OpenAI: 50.8%, MetaAI: 30.8%, Google: 8.6%, Anthropic: 6.1%, StartupDotAI: 3.8%

---

## Round 4

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Anthropic | 0.881 | 0.671 | 23% | 25% | 27% | 25% |
| 2 | MetaAI | 0.854 | 0.649 | 23% | 25% | 32% | 20% |
| 3 | Google | 0.837 | 0.668 | 24% | 25% | 31% | 20% |
| 4 | OpenAI | 0.801 | 0.727 | 24% | 25% | 26% | 25% |
| 5 | StartupDotAI | 0.788 | 0.598 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Anthropic | 0.831 | 0.957 | 0.913 | 0.785 | 1.000 | 0.811 | 0.000 |
| MetaAI | 0.769 | 0.906 | 0.945 | 0.829 | 0.949 | 0.732 | 0.000 |
| Google | 0.792 | 0.978 | 0.900 | 0.812 | 0.833 | 0.727 | 0.000 |
| OpenAI | 0.801 | 0.852 | 0.857 | 0.822 | 0.758 | 0.725 | 0.000 |
| StartupDotAI | 0.793 | 0.840 | 0.839 | 0.806 | 0.672 | 0.784 | 0.000 |

### Score Changes
- **OpenAI**: 0.786 -> 0.801 (+0.015)
- **Anthropic**: 0.830 -> 0.881 (+0.051)
- **Google**: 0.824 -> 0.837 (+0.013)
- **MetaAI**: 0.840 -> 0.854 (+0.014)
- **StartupDotAI**: 0.722 -> 0.788 (+0.066)

### Events
- **Anthropic** moved up from #2 to #1
- **MetaAI** moved down from #1 to #2
- **Regulation** by Regulator: mandate_benchmark
- **Consumer movement**: 9.6% of market switched providers

### New Benchmark Introduced
- **legal** introduced (validity=0.80, exploitability=0.22)
  - Trigger: saturation:reasoning=0.9780

### Other Actor Reasoning
- **Regulator:** mandate_benchmark: High risk (0.72) with prior investigation
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,829,241 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.40 (positive)
- Anthropic takes the lead from MetaAI
- Anthropic surges by 0.051
- StartupDotAI surges by 0.066
- New benchmark introduced: legal
- Anthropic takes #1 on coding
- Anthropic takes #1 on writing
- Consumers are turning away from OpenAI (market share -7.1%)
- MetaAI sees surge in adoption (market share +9.3%)
- Google hiring tool shows bias against protected groups, class-action lawsuit filed
- Risk signals: incident_bias_discrimination

### Consumer Market
- Avg Satisfaction: 0.770
- Switching Rate: 9.6%
- Market Shares: OpenAI: 44.4%, MetaAI: 38.9%, Google: 7.4%, Anthropic: 5.9%, StartupDotAI: 3.4%

### Regulatory Activity
- **mandate_benchmark** by Regulator

---

## Round 5

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | MetaAI | 0.882 | 0.656 | 23% | 25% | 32% | 20% |
| 2 | Google | 0.871 | 0.673 | 23% | 25% | 32% | 20% |
| 3 | Anthropic | 0.859 | 0.676 | 24% | 25% | 26% | 25% |
| 4 | OpenAI | 0.814 | 0.731 | 23% | 25% | 27% | 25% |
| 5 | StartupDotAI | 0.776 | 0.603 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| MetaAI | 0.769 | 0.906 | 0.945 | 0.829 | 1.000 | 0.732 | 1.000 | 0.000 |
| Google | 0.792 | 0.978 | 1.000 | 0.900 | 0.833 | 0.764 | 0.863 | 0.000 |
| Anthropic | 0.831 | 0.957 | 0.913 | 0.785 | 1.000 | 0.847 | 0.711 | 0.000 |
| OpenAI | 0.841 | 0.955 | 0.857 | 0.841 | 0.758 | 0.780 | 0.705 | 0.000 |
| StartupDotAI | 0.793 | 0.865 | 0.839 | 0.806 | 0.684 | 0.784 | 0.689 | 0.000 |

### Score Changes
- **OpenAI**: 0.801 -> 0.814 (+0.013)
- **Anthropic**: 0.881 -> 0.859 (-0.022)
- **Google**: 0.837 -> 0.871 (+0.034)
- **MetaAI**: 0.854 -> 0.882 (+0.028)
- **StartupDotAI**: 0.788 -> 0.776 (-0.011)

### Events
- **MetaAI** moved up from #2 to #1
- **Google** moved up from #3 to #2
- **Anthropic** moved down from #1 to #3
- **Consumer movement**: 9.7% of market switched providers

### New Benchmark Introduced
- **finance** introduced (validity=0.80, exploitability=0.22)
  - Trigger: saturation:reasoning=0.9780

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,829,241 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.40 (positive)
- MetaAI takes the lead from Anthropic
- Regulator mandates new benchmark standards
- New benchmark introduced: finance
- MetaAI raises $171,000,000 from TechVentures
- MetaAI raises $57,000,000 from Horizon_Capital
- OpenAI takes #1 on coding
- Google takes #1 on safety
- Consumers are turning away from OpenAI (market share -6.4%)
- MetaAI sees surge in adoption (market share +8.2%)
- Risk signals: regulatory_mandate_benchmark

### Consumer Market
- Avg Satisfaction: 0.793
- Switching Rate: 9.7%
- Market Shares: MetaAI: 42.5%, OpenAI: 38.8%, Anthropic: 8.9%, Google: 6.7%, StartupDotAI: 3.1%

---

## Round 6

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 0.905 | 0.677 | 24% | 25% | 31% | 20% |
| 2 | MetaAI | 0.905 | 0.663 | 24% | 25% | 31% | 20% |
| 3 | OpenAI | 0.881 | 0.735 | 23% | 25% | 27% | 25% |
| 4 | Anthropic | 0.845 | 0.682 | 24% | 25% | 26% | 25% |
| 5 | StartupDotAI | 0.780 | 0.608 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 0.903 | 0.978 | 1.000 | 0.900 | 1.000 | 0.817 | 0.863 | 0.862 | 0.000 |
| MetaAI | 0.913 | 0.906 | 0.978 | 0.829 | 1.000 | 0.814 | 1.000 | 0.837 | 0.000 |
| OpenAI | 0.841 | 0.955 | 0.857 | 0.841 | 0.816 | 0.975 | 0.953 | 0.829 | 0.000 |
| Anthropic | 0.831 | 0.957 | 0.913 | 0.816 | 1.000 | 0.847 | 0.729 | 0.753 | 0.000 |
| StartupDotAI | 0.856 | 0.865 | 0.839 | 0.806 | 0.684 | 0.784 | 0.702 | 0.774 | 0.000 |

### Score Changes
- **OpenAI**: 0.814 -> 0.881 (+0.067)
- **Anthropic**: 0.859 -> 0.845 (-0.014)
- **Google**: 0.871 -> 0.905 (+0.034)
- **MetaAI**: 0.882 -> 0.905 (+0.023)
- **StartupDotAI**: 0.776 -> 0.780 (+0.004)

### Events
- **Google** moved up from #2 to #1
- **MetaAI** moved down from #1 to #2
- **OpenAI** moved up from #4 to #3
- **Anthropic** moved down from #3 to #4
- **Consumer movement**: 6.3% of market switched providers

### New Benchmark Introduced
- **coding_advanced** introduced (validity=0.88, exploitability=0.12)
  - Trigger: saturation:reasoning=0.9780

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,897,106 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.60 (positive)
- Google takes the lead from MetaAI
- OpenAI surges by 0.067
- New benchmark introduced: coding_advanced
- MetaAI takes #1 on coding
- OpenAI takes #1 on medical
- Consumers are turning away from OpenAI (market share -5.6%)
- Anthropic sees surge in adoption (market share +3.0%)
- MetaAI sees surge in adoption (market share +3.6%)

### Consumer Market
- Avg Satisfaction: 0.815
- Switching Rate: 6.3%
- Market Shares: MetaAI: 44.3%, OpenAI: 35.8%, Anthropic: 10.6%, Google: 6.3%, StartupDotAI: 3.0%

---

## Round 7

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.891 | 0.740 | 23% | 25% | 27% | 25% |
| 2 | MetaAI | 0.878 | 0.670 | 24% | 25% | 31% | 20% |
| 3 | Google | 0.876 | 0.682 | 24% | 25% | 31% | 20% |
| 4 | Anthropic | 0.844 | 0.687 | 23% | 25% | 27% | 25% |
| 5 | StartupDotAI | 0.780 | 0.612 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 0.841 | 0.955 | 0.904 | 0.841 | 1.000 | 0.975 | 0.953 | 0.829 | 0.824 | 0.000 |
| MetaAI | 0.913 | 0.906 | 0.978 | 0.829 | 1.000 | 0.814 | 1.000 | 0.837 | 0.760 | 0.000 |
| Google | 0.903 | 1.000 | 1.000 | 0.900 | 1.000 | 0.817 | 0.863 | 0.862 | 0.737 | 0.000 |
| Anthropic | 0.863 | 0.957 | 0.913 | 0.816 | 1.000 | 0.872 | 0.729 | 0.822 | 0.804 | 0.000 |
| StartupDotAI | 0.856 | 0.865 | 0.839 | 0.806 | 0.905 | 0.790 | 0.702 | 0.774 | 0.624 | 0.000 |

### Score Changes
- **OpenAI**: 0.881 -> 0.891 (+0.011)
- **Anthropic**: 0.845 -> 0.844 (-0.001)
- **Google**: 0.905 -> 0.876 (-0.029)
- **MetaAI**: 0.905 -> 0.878 (-0.027)
- **StartupDotAI**: 0.780 -> 0.780 (-0.000)

### Events
- **OpenAI** moved up from #3 to #1
- **Google** moved down from #1 to #3
- **Regulation** by Regulator: public_warning

### New Benchmark Introduced
- **reasoning_advanced** introduced (validity=0.87, exploitability=0.12)
  - Trigger: saturation:coding=0.9126

### Other Actor Reasoning
- **Regulator:** public_warning: Follow-up to investigation, risk at 0.93
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,897,106 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.30 (positive)
- OpenAI takes the lead from Google
- New benchmark introduced: reasoning_advanced

### Consumer Market
- Avg Satisfaction: 0.834
- Switching Rate: 4.5%
- Market Shares: MetaAI: 44.6%, OpenAI: 35.9%, Anthropic: 10.5%, Google: 6.1%, StartupDotAI: 2.9%

### Regulatory Activity
- **public_warning** by Regulator

---

## Round 8

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 0.884 | 0.686 | 24% | 25% | 31% | 20% |
| 2 | OpenAI | 0.880 | 0.746 | 24% | 25% | 26% | 25% |
| 3 | Anthropic | 0.867 | 0.691 | 23% | 25% | 27% | 25% |
| 4 | MetaAI | 0.864 | 0.676 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.808 | 0.617 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 0.903 | 1.000 | 1.000 | 0.919 | 1.000 | 0.817 | 0.863 | 0.862 | 0.737 | 0.918 |
| OpenAI | 0.868 | 0.955 | 0.904 | 0.881 | 1.000 | 0.975 | 0.953 | 0.829 | 0.824 | 0.763 |
| Anthropic | 0.863 | 0.957 | 0.913 | 0.844 | 1.000 | 0.919 | 0.961 | 0.847 | 0.804 | 0.747 |
| MetaAI | 0.913 | 0.906 | 0.978 | 0.829 | 1.000 | 0.814 | 1.000 | 0.837 | 0.760 | 0.816 |
| StartupDotAI | 0.856 | 0.865 | 1.000 | 0.806 | 0.905 | 0.790 | 0.760 | 0.774 | 0.709 | 0.773 |

### Score Changes
- **OpenAI**: 0.891 -> 0.880 (-0.011)
- **Anthropic**: 0.844 -> 0.867 (+0.023)
- **Google**: 0.876 -> 0.884 (+0.008)
- **MetaAI**: 0.878 -> 0.864 (-0.014)
- **StartupDotAI**: 0.780 -> 0.808 (+0.028)

### Events
- **Google** moved up from #3 to #1
- **OpenAI** moved down from #1 to #2
- **Anthropic** moved up from #4 to #3
- **MetaAI** moved down from #2 to #4

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,897,106 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.10 (neutral)
- Google takes the lead from OpenAI
- Regulator issues public warning about AI safety concerns
- OpenAI raises $171,000,000 from TechVentures
- Risk signals: regulatory_public_warning

### Consumer Market
- Avg Satisfaction: 0.843
- Switching Rate: 3.1%
- Market Shares: MetaAI: 44.6%, OpenAI: 36.1%, Anthropic: 10.5%, Google: 5.9%, StartupDotAI: 2.9%

---

## Round 9

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.907 | 0.752 | 24% | 25% | 26% | 25% |
| 2 | Google | 0.885 | 0.691 | 24% | 25% | 31% | 20% |
| 3 | Anthropic | 0.876 | 0.696 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.875 | 0.682 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.807 | 0.621 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 0.962 | 0.955 | 0.904 | 0.943 | 1.000 | 0.975 | 0.953 | 0.850 | 0.824 | 0.831 |
| Google | 0.903 | 1.000 | 1.000 | 0.919 | 1.000 | 0.817 | 0.863 | 0.862 | 0.745 | 0.918 |
| Anthropic | 0.879 | 0.957 | 0.913 | 0.844 | 1.000 | 0.919 | 0.961 | 0.847 | 0.858 | 0.747 |
| MetaAI | 0.913 | 0.906 | 0.978 | 0.829 | 1.000 | 0.814 | 1.000 | 0.837 | 0.836 | 0.816 |
| StartupDotAI | 0.856 | 0.865 | 1.000 | 0.806 | 0.905 | 0.790 | 0.760 | 0.774 | 0.709 | 0.773 |

### Score Changes
- **OpenAI**: 0.880 -> 0.907 (+0.027)
- **Anthropic**: 0.867 -> 0.876 (+0.009)
- **Google**: 0.884 -> 0.885 (+0.001)
- **MetaAI**: 0.864 -> 0.875 (+0.011)
- **StartupDotAI**: 0.808 -> 0.807 (-0.001)

### Events
- **OpenAI** moved up from #2 to #1
- **Google** moved down from #1 to #2

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,897,106 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.35 (positive)
- OpenAI takes the lead from Google
- OpenAI raises $57,000,000 from Horizon_Capital
- Anthropic takes #1 on coding_advanced

### Consumer Market
- Avg Satisfaction: 0.850
- Switching Rate: 3.1%
- Market Shares: MetaAI: 44.2%, OpenAI: 37.8%, Anthropic: 9.3%, Google: 5.8%, StartupDotAI: 2.8%

---

## Round 10

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.915 | 0.758 | 25% | 25% | 25% | 25% |
| 2 | Anthropic | 0.907 | 0.700 | 24% | 25% | 26% | 25% |
| 3 | Google | 0.892 | 0.695 | 24% | 25% | 31% | 20% |
| 4 | MetaAI | 0.883 | 0.688 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.809 | 0.626 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 0.962 | 0.955 | 0.904 | 0.943 | 1.000 | 0.975 | 0.953 | 0.850 | 0.824 | 0.910 |
| Anthropic | 1.000 | 0.957 | 0.913 | 0.844 | 1.000 | 0.936 | 0.961 | 0.847 | 0.858 | 0.871 |
| Google | 0.939 | 1.000 | 1.000 | 0.919 | 1.000 | 0.817 | 0.863 | 0.862 | 0.763 | 0.918 |
| MetaAI | 0.913 | 0.906 | 1.000 | 0.829 | 1.000 | 0.862 | 1.000 | 0.837 | 0.836 | 0.816 |
| StartupDotAI | 0.856 | 0.865 | 1.000 | 0.806 | 0.905 | 0.790 | 0.795 | 0.774 | 0.709 | 0.773 |

### Score Changes
- **OpenAI**: 0.907 -> 0.915 (+0.008)
- **Anthropic**: 0.876 -> 0.907 (+0.032)
- **Google**: 0.885 -> 0.892 (+0.007)
- **MetaAI**: 0.875 -> 0.883 (+0.008)
- **StartupDotAI**: 0.807 -> 0.809 (+0.002)

### Events
- **Anthropic** moved up from #3 to #2
- **Google** moved down from #2 to #3
- **Regulation** by Regulator: emergency_investigation
- **Consumer movement**: 6.9% of market switched providers

### Other Actor Reasoning
- **Regulator:** emergency_investigation: Critical incident: safety_failure: Anthropic AI produces inconsistent outputs on safety-critical queries
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,698,846 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.15 (negative)
- Anthropic AI produces inconsistent outputs on safety-critical queries
- Risk signals: incident_safety_failure

### Consumer Market
- Avg Satisfaction: 0.861
- Switching Rate: 6.9%
- Market Shares: MetaAI: 41.4%, OpenAI: 35.8%, Google: 12.2%, Anthropic: 7.9%, StartupDotAI: 2.8%

### Regulatory Activity
- **emergency_investigation** by Regulator

---

## Round 11

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 0.913 | 0.717 | 24% | 25% | 31% | 20% |
| 2 | OpenAI | 0.913 | 0.764 | 25% | 25% | 25% | 25% |
| 3 | Anthropic | 0.909 | 0.705 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.893 | 0.692 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.810 | 0.630 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 0.973 | 1.000 | 1.000 | 0.961 | 1.000 | 0.856 | 0.863 | 0.898 | 0.802 | 0.918 |
| OpenAI | 0.962 | 0.955 | 0.904 | 0.943 | 1.000 | 0.975 | 0.953 | 0.850 | 0.824 | 0.910 |
| Anthropic | 1.000 | 0.957 | 0.913 | 0.844 | 1.000 | 0.936 | 0.961 | 0.869 | 0.858 | 0.871 |
| MetaAI | 0.913 | 0.959 | 1.000 | 0.875 | 1.000 | 0.862 | 1.000 | 0.837 | 0.845 | 0.816 |
| StartupDotAI | 0.856 | 0.865 | 1.000 | 0.806 | 0.905 | 0.790 | 0.797 | 0.774 | 0.709 | 0.773 |

### Score Changes
- **OpenAI**: 0.915 -> 0.913 (-0.003)
- **Anthropic**: 0.907 -> 0.909 (+0.002)
- **Google**: 0.892 -> 0.913 (+0.021)
- **MetaAI**: 0.883 -> 0.893 (+0.010)
- **StartupDotAI**: 0.809 -> 0.810 (+0.000)

### Events
- **Google** moved up from #3 to #1
- **OpenAI** moved down from #1 to #2
- **Anthropic** moved down from #2 to #3
- **Consumer movement**: 7.8% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,698,846 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.10 (neutral)
- Google takes the lead from OpenAI
- Emergency investigation of Anthropic following critical incident
- Google raises $171,000,000 from TechVentures
- Google raises $57,000,000 from Horizon_Capital
- Google sees surge in adoption (market share +6.4%)
- Risk signals: regulatory_emergency_investigation

### Consumer Market
- Avg Satisfaction: 0.873
- Switching Rate: 7.8%
- Market Shares: MetaAI: 36.8%, OpenAI: 33.7%, Google: 19.8%, Anthropic: 7.0%, StartupDotAI: 2.7%

---

## Round 12

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 0.915 | 0.724 | 24% | 25% | 31% | 20% |
| 2 | Anthropic | 0.913 | 0.709 | 24% | 25% | 26% | 25% |
| 3 | OpenAI | 0.912 | 0.769 | 25% | 25% | 25% | 25% |
| 4 | MetaAI | 0.896 | 0.697 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.814 | 0.635 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 0.976 | 1.000 | 1.000 | 0.961 | 1.000 | 0.868 | 0.863 | 0.898 | 0.802 | 0.918 |
| Anthropic | 1.000 | 0.957 | 0.913 | 0.869 | 1.000 | 0.936 | 0.961 | 0.869 | 0.859 | 0.884 |
| OpenAI | 0.962 | 0.955 | 0.904 | 0.943 | 1.000 | 0.975 | 0.953 | 0.850 | 0.824 | 0.910 |
| MetaAI | 0.913 | 0.959 | 1.000 | 0.875 | 1.000 | 0.862 | 1.000 | 0.837 | 0.845 | 0.816 |
| StartupDotAI | 0.856 | 0.865 | 1.000 | 0.806 | 0.905 | 0.790 | 0.797 | 0.793 | 0.709 | 0.773 |

### Score Changes
- **OpenAI**: 0.913 -> 0.912 (-0.000)
- **Anthropic**: 0.909 -> 0.913 (+0.004)
- **Google**: 0.913 -> 0.915 (+0.001)
- **MetaAI**: 0.893 -> 0.896 (+0.002)
- **StartupDotAI**: 0.810 -> 0.814 (+0.004)

### Events
- **Anthropic** moved up from #3 to #2
- **OpenAI** moved down from #2 to #3
- **Consumer movement**: 7.4% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,698,846 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.05 (neutral)
- Google sees surge in adoption (market share +7.6%)
- Consumers are turning away from MetaAI (market share -4.6%)

### Consumer Market
- Avg Satisfaction: 0.879
- Switching Rate: 7.4%
- Market Shares: OpenAI: 33.6%, MetaAI: 31.9%, Google: 25.4%, Anthropic: 6.4%, StartupDotAI: 2.7%

---

## Round 13

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.919 | 0.774 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.914 | 0.730 | 24% | 25% | 31% | 20% |
| 3 | Anthropic | 0.914 | 0.713 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.905 | 0.701 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.835 | 0.639 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 0.962 | 0.955 | 0.904 | 0.943 | 1.000 | 0.975 | 0.953 | 0.850 | 0.868 | 0.910 |
| Google | 0.976 | 1.000 | 1.000 | 0.961 | 1.000 | 0.868 | 0.863 | 0.898 | 0.802 | 0.918 |
| Anthropic | 1.000 | 0.957 | 0.913 | 0.869 | 1.000 | 0.936 | 0.961 | 0.869 | 0.859 | 0.884 |
| MetaAI | 0.999 | 0.959 | 1.000 | 0.875 | 1.000 | 0.862 | 1.000 | 0.837 | 0.845 | 0.816 |
| StartupDotAI | 0.856 | 0.865 | 1.000 | 0.806 | 0.905 | 0.790 | 0.797 | 0.836 | 0.789 | 0.773 |

### Score Changes
- **OpenAI**: 0.912 -> 0.919 (+0.007)
- **Anthropic**: 0.913 -> 0.914 (+0.001)
- **Google**: 0.915 -> 0.914 (-0.000)
- **MetaAI**: 0.896 -> 0.905 (+0.009)
- **StartupDotAI**: 0.814 -> 0.835 (+0.021)

### Events
- **OpenAI** moved up from #3 to #1
- **Google** moved down from #1 to #2
- **Anthropic** moved down from #2 to #3
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 6.2% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (0.83) after mandate 9 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,698,846 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.25 (positive)
- OpenAI takes the lead from Google
- OpenAI takes #1 on coding_advanced
- Google sees surge in adoption (market share +5.7%)
- Consumers are turning away from MetaAI (market share -4.9%)

### Consumer Market
- Avg Satisfaction: 0.886
- Switching Rate: 6.2%
- Market Shares: OpenAI: 33.6%, Google: 30.0%, MetaAI: 27.8%, Anthropic: 5.9%, StartupDotAI: 2.7%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 14

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.925 | 0.779 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.914 | 0.737 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.914 | 0.718 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.909 | 0.706 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.846 | 0.643 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 0.962 | 0.955 | 0.919 | 0.943 | 1.000 | 0.975 | 0.953 | 0.879 | 0.868 | 0.910 |
| Google | 0.976 | 1.000 | 1.000 | 0.961 | 1.000 | 0.868 | 0.863 | 0.898 | 0.802 | 0.918 |
| Anthropic | 1.000 | 0.957 | 0.913 | 0.869 | 1.000 | 0.936 | 0.961 | 0.869 | 0.859 | 0.884 |
| MetaAI | 0.999 | 1.000 | 1.000 | 0.875 | 1.000 | 0.868 | 1.000 | 0.837 | 0.845 | 0.816 |
| StartupDotAI | 0.856 | 0.865 | 1.000 | 0.922 | 0.925 | 0.790 | 0.797 | 0.836 | 0.789 | 0.773 |

### Score Changes
- **OpenAI**: 0.919 -> 0.925 (+0.006)
- **Anthropic**: 0.914 -> 0.914 (-0.000)
- **Google**: 0.914 -> 0.914 (+0.000)
- **MetaAI**: 0.905 -> 0.909 (+0.004)
- **StartupDotAI**: 0.835 -> 0.846 (+0.011)

### Events
- **Consumer movement**: 6.3% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,703,701 to Google, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.20 (negative)
- Regulator initiates compliance audit on AI providers
- Google sees surge in adoption (market share +4.6%)
- Consumers are turning away from MetaAI (market share -4.1%)
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.878
- Switching Rate: 6.3%
- Market Shares: Google: 36.3%, OpenAI: 31.0%, MetaAI: 24.3%, Anthropic: 5.6%, StartupDotAI: 2.7%

---

## Round 15

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.929 | 0.784 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.923 | 0.744 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.918 | 0.722 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.909 | 0.710 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.855 | 0.648 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 0.962 | 0.999 | 0.919 | 0.943 | 1.000 | 0.975 | 0.953 | 0.879 | 0.868 | 0.910 |
| Google | 0.976 | 1.000 | 1.000 | 0.961 | 1.000 | 0.891 | 0.863 | 0.937 | 0.802 | 0.918 |
| Anthropic | 1.000 | 0.957 | 0.964 | 0.869 | 1.000 | 0.936 | 0.961 | 0.869 | 0.859 | 0.884 |
| MetaAI | 0.999 | 1.000 | 1.000 | 0.875 | 1.000 | 0.868 | 1.000 | 0.837 | 0.845 | 0.816 |
| StartupDotAI | 0.929 | 0.892 | 1.000 | 0.922 | 0.925 | 0.790 | 0.797 | 0.836 | 0.789 | 0.773 |

### Score Changes
- **OpenAI**: 0.925 -> 0.929 (+0.003)
- **Anthropic**: 0.914 -> 0.918 (+0.004)
- **Google**: 0.914 -> 0.923 (+0.008)
- **MetaAI**: 0.909 -> 0.909 (-0.000)
- **StartupDotAI**: 0.846 -> 0.855 (+0.008)

### Events
- **Consumer movement**: 5.5% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,703,701 to Google, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.05 (neutral)
- Google sees surge in adoption (market share +6.3%)
- Consumers are turning away from MetaAI (market share -3.4%)

### Consumer Market
- Avg Satisfaction: 0.884
- Switching Rate: 5.5%
- Market Shares: Google: 41.7%, OpenAI: 28.9%, MetaAI: 21.3%, Anthropic: 5.4%, StartupDotAI: 2.7%

---

## Round 16

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.939 | 0.788 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.925 | 0.750 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.918 | 0.726 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.915 | 0.714 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.857 | 0.653 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 0.979 | 0.999 | 0.919 | 0.943 | 1.000 | 0.991 | 0.953 | 0.879 | 0.910 | 0.910 |
| Google | 0.976 | 1.000 | 1.000 | 0.961 | 1.000 | 0.891 | 0.863 | 0.937 | 0.817 | 0.918 |
| Anthropic | 1.000 | 0.957 | 0.964 | 0.869 | 1.000 | 0.936 | 0.961 | 0.869 | 0.859 | 0.884 |
| MetaAI | 0.999 | 1.000 | 1.000 | 0.875 | 1.000 | 0.883 | 1.000 | 0.837 | 0.845 | 0.877 |
| StartupDotAI | 0.929 | 0.892 | 1.000 | 0.922 | 0.925 | 0.820 | 0.797 | 0.836 | 0.789 | 0.773 |

### Score Changes
- **OpenAI**: 0.929 -> 0.939 (+0.010)
- **Anthropic**: 0.918 -> 0.918 (+0.000)
- **Google**: 0.923 -> 0.925 (+0.003)
- **MetaAI**: 0.909 -> 0.915 (+0.007)
- **StartupDotAI**: 0.855 -> 0.857 (+0.002)

### Events
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (0.80) after mandate 12 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,703,701 to Google, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.05 (neutral)
- Google sees surge in adoption (market share +5.4%)
- Consumers are turning away from MetaAI (market share -3.1%)

### Consumer Market
- Avg Satisfaction: 0.895
- Switching Rate: 4.7%
- Market Shares: Google: 45.6%, OpenAI: 27.7%, MetaAI: 18.8%, Anthropic: 5.3%, StartupDotAI: 2.7%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 17

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 0.942 | 0.756 | 25% | 25% | 30% | 20% |
| 2 | OpenAI | 0.939 | 0.792 | 25% | 25% | 25% | 25% |
| 3 | Anthropic | 0.918 | 0.731 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.915 | 0.719 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.857 | 0.658 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 0.976 | 1.000 | 1.000 | 0.961 | 1.000 | 0.954 | 1.000 | 0.937 | 0.817 | 0.918 |
| OpenAI | 0.979 | 1.000 | 0.930 | 0.943 | 1.000 | 0.991 | 0.953 | 0.879 | 0.910 | 0.910 |
| Anthropic | 1.000 | 0.957 | 0.964 | 0.869 | 1.000 | 0.936 | 0.961 | 0.869 | 0.859 | 0.884 |
| MetaAI | 0.999 | 1.000 | 1.000 | 0.875 | 1.000 | 0.883 | 1.000 | 0.837 | 0.845 | 0.877 |
| StartupDotAI | 0.929 | 0.892 | 1.000 | 0.922 | 0.925 | 0.820 | 0.797 | 0.836 | 0.789 | 0.773 |

### Score Changes
- **OpenAI**: 0.939 -> 0.939 (+0.001)
- **Anthropic**: 0.918 -> 0.918 (-0.000)
- **Google**: 0.925 -> 0.942 (+0.017)
- **MetaAI**: 0.915 -> 0.915 (+0.000)
- **StartupDotAI**: 0.857 -> 0.857 (-0.000)

### Events
- **Google** moved up from #2 to #1
- **OpenAI** moved down from #1 to #2

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,703,701 to Google, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.10 (neutral)
- Google takes the lead from OpenAI
- Regulator initiates compliance audit on AI providers
- Google sees surge in adoption (market share +3.8%)
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.901
- Switching Rate: 3.9%
- Market Shares: Google: 48.7%, OpenAI: 26.8%, MetaAI: 16.7%, Anthropic: 5.2%, StartupDotAI: 2.6%

---

## Round 18

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 0.964 | 0.763 | 25% | 25% | 30% | 20% |
| 2 | OpenAI | 0.948 | 0.796 | 25% | 25% | 25% | 25% |
| 3 | Anthropic | 0.927 | 0.735 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.926 | 0.723 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.860 | 0.664 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 0.976 | 1.000 | 1.000 | 0.961 | 1.000 | 0.954 | 1.000 | 0.937 | 0.944 | 0.918 |
| OpenAI | 0.979 | 1.000 | 1.000 | 0.943 | 1.000 | 0.991 | 0.953 | 0.885 | 0.910 | 0.910 |
| Anthropic | 1.000 | 0.957 | 0.964 | 0.959 | 1.000 | 0.936 | 0.961 | 0.869 | 0.859 | 0.884 |
| MetaAI | 0.999 | 1.000 | 1.000 | 0.959 | 1.000 | 0.883 | 1.000 | 0.844 | 0.845 | 0.877 |
| StartupDotAI | 0.929 | 0.892 | 1.000 | 0.922 | 0.959 | 0.820 | 0.797 | 0.836 | 0.789 | 0.773 |

### Score Changes
- **OpenAI**: 0.939 -> 0.948 (+0.008)
- **Anthropic**: 0.918 -> 0.927 (+0.009)
- **Google**: 0.942 -> 0.964 (+0.022)
- **MetaAI**: 0.915 -> 0.926 (+0.010)
- **StartupDotAI**: 0.857 -> 0.860 (+0.003)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,856,523 to Google, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.05 (neutral)
- Google sees surge in adoption (market share +3.1%)

### Consumer Market
- Avg Satisfaction: 0.905
- Switching Rate: 3.3%
- Market Shares: Google: 52.0%, OpenAI: 25.2%, MetaAI: 15.0%, Anthropic: 5.1%, StartupDotAI: 2.6%

---

## Round 19

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 0.965 | 0.769 | 25% | 25% | 30% | 20% |
| 2 | OpenAI | 0.955 | 0.800 | 25% | 25% | 25% | 25% |
| 3 | Anthropic | 0.934 | 0.739 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.930 | 0.727 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.863 | 0.669 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 0.976 | 1.000 | 1.000 | 0.961 | 1.000 | 0.954 | 1.000 | 0.937 | 0.944 | 0.918 |
| OpenAI | 0.979 | 1.000 | 1.000 | 0.944 | 1.000 | 0.991 | 1.000 | 0.885 | 0.910 | 0.910 |
| Anthropic | 1.000 | 0.957 | 0.964 | 0.959 | 1.000 | 0.936 | 0.961 | 0.869 | 0.859 | 0.918 |
| MetaAI | 0.999 | 1.000 | 1.000 | 0.959 | 1.000 | 0.883 | 1.000 | 0.844 | 0.845 | 0.877 |
| StartupDotAI | 0.929 | 0.892 | 1.000 | 0.922 | 0.959 | 0.820 | 0.797 | 0.836 | 0.789 | 0.773 |

### Score Changes
- **OpenAI**: 0.948 -> 0.955 (+0.007)
- **Anthropic**: 0.927 -> 0.934 (+0.007)
- **Google**: 0.964 -> 0.965 (+0.001)
- **MetaAI**: 0.926 -> 0.930 (+0.004)
- **StartupDotAI**: 0.860 -> 0.863 (+0.003)

### Events
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (0.80) after mandate 15 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,856,523 to Google, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.05 (neutral)
- Google sees surge in adoption (market share +3.3%)

### Consumer Market
- Avg Satisfaction: 0.912
- Switching Rate: 3.3%
- Market Shares: Google: 55.3%, OpenAI: 23.5%, MetaAI: 13.6%, Anthropic: 5.1%, StartupDotAI: 2.6%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 20

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.970 | 0.804 | 24% | 25% | 26% | 25% |
| 2 | Google | 0.967 | 0.775 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.938 | 0.743 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.935 | 0.732 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.875 | 0.675 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 0.979 | 1.000 | 1.000 | 0.944 | 1.000 | 0.991 | 1.000 | 0.885 | 1.000 | 0.910 |
| Google | 0.976 | 1.000 | 1.000 | 0.961 | 1.000 | 0.954 | 1.000 | 0.937 | 0.944 | 0.918 |
| Anthropic | 1.000 | 0.957 | 0.964 | 0.959 | 1.000 | 0.936 | 0.961 | 0.869 | 0.859 | 0.918 |
| MetaAI | 0.999 | 1.000 | 1.000 | 0.959 | 1.000 | 0.883 | 1.000 | 0.844 | 0.845 | 0.877 |
| StartupDotAI | 0.929 | 0.892 | 1.000 | 0.922 | 0.959 | 0.820 | 0.797 | 0.836 | 0.858 | 0.773 |

### Score Changes
- **OpenAI**: 0.955 -> 0.970 (+0.015)
- **Anthropic**: 0.934 -> 0.938 (+0.004)
- **Google**: 0.965 -> 0.967 (+0.001)
- **MetaAI**: 0.930 -> 0.935 (+0.005)
- **StartupDotAI**: 0.863 -> 0.875 (+0.012)

### Events
- **OpenAI** moved up from #2 to #1
- **Google** moved down from #1 to #2
- **Consumer movement**: 5.2% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,856,523 to Google, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.15 (negative)
- OpenAI takes the lead from Google
- Regulator initiates compliance audit on AI providers
- Google sees surge in adoption (market share +3.3%)
- OpenAI facial recognition errors disproportionately affect minorities, contracts suspended
- Risk signals: regulatory_compliance_audit, incident_bias_discrimination

### Consumer Market
- Avg Satisfaction: 0.882
- Switching Rate: 5.2%
- Market Shares: Google: 60.5%, OpenAI: 19.5%, MetaAI: 12.4%, Anthropic: 5.0%, StartupDotAI: 2.6%

---

## Round 21

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.985 | 0.808 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.969 | 0.781 | 25% | 25% | 30% | 20% |
| 3 | MetaAI | 0.944 | 0.736 | 24% | 25% | 31% | 20% |
| 4 | Anthropic | 0.942 | 0.748 | 24% | 25% | 26% | 25% |
| 5 | StartupDotAI | 0.876 | 0.680 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 0.944 | 1.000 | 0.991 | 1.000 | 0.929 | 1.000 | 0.981 |
| Google | 0.976 | 1.000 | 1.000 | 0.961 | 1.000 | 0.966 | 1.000 | 0.937 | 0.944 | 0.918 |
| MetaAI | 0.999 | 1.000 | 1.000 | 0.959 | 1.000 | 0.883 | 1.000 | 0.901 | 0.845 | 0.877 |
| Anthropic | 1.000 | 0.957 | 0.964 | 0.959 | 1.000 | 0.936 | 0.961 | 0.869 | 0.870 | 0.918 |
| StartupDotAI | 0.929 | 0.892 | 1.000 | 0.922 | 0.959 | 0.820 | 0.797 | 0.836 | 0.858 | 0.773 |

### Score Changes
- **OpenAI**: 0.970 -> 0.985 (+0.015)
- **Anthropic**: 0.938 -> 0.942 (+0.004)
- **Google**: 0.967 -> 0.969 (+0.002)
- **MetaAI**: 0.935 -> 0.944 (+0.009)
- **StartupDotAI**: 0.875 -> 0.876 (+0.001)

### Events
- **MetaAI** moved up from #4 to #3
- **Anthropic** moved down from #3 to #4

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,856,523 to Google, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.05 (neutral)
- Consumers are turning away from OpenAI (market share -4.0%)
- Google sees surge in adoption (market share +5.2%)

### Consumer Market
- Avg Satisfaction: 0.898
- Switching Rate: 3.7%
- Market Shares: Google: 64.2%, OpenAI: 16.8%, MetaAI: 11.4%, Anthropic: 5.0%, StartupDotAI: 2.6%

---

## Round 22

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.985 | 0.812 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.969 | 0.787 | 25% | 25% | 30% | 20% |
| 3 | MetaAI | 0.945 | 0.740 | 24% | 25% | 31% | 20% |
| 4 | Anthropic | 0.942 | 0.752 | 24% | 25% | 26% | 25% |
| 5 | StartupDotAI | 0.876 | 0.685 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 0.944 | 1.000 | 0.991 | 1.000 | 0.929 | 1.000 | 0.981 |
| Google | 0.976 | 1.000 | 1.000 | 0.961 | 1.000 | 0.966 | 1.000 | 0.937 | 0.944 | 0.918 |
| MetaAI | 0.999 | 1.000 | 1.000 | 0.959 | 1.000 | 0.900 | 1.000 | 0.901 | 0.845 | 0.877 |
| Anthropic | 1.000 | 0.957 | 0.964 | 0.959 | 1.000 | 0.936 | 0.961 | 0.869 | 0.870 | 0.918 |
| StartupDotAI | 0.929 | 0.892 | 1.000 | 0.922 | 0.959 | 0.820 | 0.797 | 0.836 | 0.858 | 0.773 |

### Score Changes
- **OpenAI**: 0.985 -> 0.985 (+0.000)
- **Anthropic**: 0.942 -> 0.942 (+0.000)
- **Google**: 0.969 -> 0.969 (+0.000)
- **MetaAI**: 0.944 -> 0.945 (+0.002)
- **StartupDotAI**: 0.876 -> 0.876 (+0.000)

### Events
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (0.80) after mandate 18 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,196,775 to Google, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.05 (neutral)
- Google sees surge in adoption (market share +3.7%)

### Consumer Market
- Avg Satisfaction: 0.903
- Switching Rate: 2.9%
- Market Shares: Google: 67.0%, OpenAI: 14.9%, MetaAI: 10.5%, Anthropic: 4.9%, StartupDotAI: 2.6%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 23

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.985 | 0.816 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.973 | 0.793 | 24% | 25% | 31% | 20% |
| 3 | Anthropic | 0.951 | 0.757 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.945 | 0.744 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.887 | 0.689 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 0.944 | 1.000 | 0.991 | 1.000 | 0.929 | 1.000 | 0.981 |
| Google | 0.976 | 1.000 | 1.000 | 0.961 | 1.000 | 0.966 | 1.000 | 0.937 | 0.944 | 0.954 |
| Anthropic | 1.000 | 0.957 | 0.964 | 0.959 | 1.000 | 0.936 | 0.961 | 0.967 | 0.870 | 0.918 |
| MetaAI | 0.999 | 1.000 | 1.000 | 0.959 | 1.000 | 0.900 | 1.000 | 0.901 | 0.845 | 0.877 |
| StartupDotAI | 0.929 | 0.892 | 1.000 | 0.922 | 0.959 | 0.820 | 0.840 | 0.836 | 0.858 | 0.839 |

### Score Changes
- **OpenAI**: 0.985 -> 0.985 (+0.000)
- **Anthropic**: 0.942 -> 0.951 (+0.009)
- **Google**: 0.969 -> 0.973 (+0.004)
- **MetaAI**: 0.945 -> 0.945 (+0.000)
- **StartupDotAI**: 0.876 -> 0.887 (+0.012)

### Events
- **Anthropic** moved up from #4 to #3
- **MetaAI** moved down from #3 to #4
- **Consumer movement**: 21.0% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,196,775 to Google, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.40 (negative)
- Regulator initiates compliance audit on AI providers
- Google hiring tool shows bias against protected groups, class-action lawsuit filed
- Risk signals: regulatory_compliance_audit, incident_bias_discrimination

### Consumer Market
- Avg Satisfaction: 0.812
- Switching Rate: 21.0%
- Market Shares: Google: 48.0%, Anthropic: 25.9%, OpenAI: 13.5%, MetaAI: 9.9%, StartupDotAI: 2.6%

---

## Round 24

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.985 | 0.820 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.974 | 0.799 | 24% | 25% | 31% | 20% |
| 3 | Anthropic | 0.958 | 0.762 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.948 | 0.749 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.887 | 0.693 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 0.944 | 1.000 | 0.991 | 1.000 | 0.929 | 1.000 | 0.981 |
| Google | 0.988 | 1.000 | 1.000 | 0.961 | 1.000 | 0.966 | 1.000 | 0.937 | 0.944 | 0.954 |
| Anthropic | 1.000 | 0.988 | 0.964 | 0.959 | 1.000 | 0.936 | 1.000 | 0.967 | 0.870 | 0.918 |
| MetaAI | 0.999 | 1.000 | 1.000 | 0.959 | 1.000 | 0.900 | 1.000 | 0.901 | 0.845 | 0.898 |
| StartupDotAI | 0.929 | 0.892 | 1.000 | 0.922 | 0.959 | 0.820 | 0.840 | 0.836 | 0.858 | 0.839 |

### Score Changes
- **OpenAI**: 0.985 -> 0.985 (+0.000)
- **Anthropic**: 0.951 -> 0.958 (+0.007)
- **Google**: 0.973 -> 0.974 (+0.001)
- **MetaAI**: 0.945 -> 0.948 (+0.002)
- **StartupDotAI**: 0.887 -> 0.887 (+0.000)

### Events
- **Consumer movement**: 21.2% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,196,775 to Google, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.45 (negative)
- Anthropic sees surge in adoption (market share +21.0%)
- Consumers are turning away from Google (market share -19.0%)
- DOJ civil rights division files suit against OpenAI for systematic bias
- Risk signals: incident_bias_discrimination

### Consumer Market
- Avg Satisfaction: 0.791
- Switching Rate: 21.2%
- Market Shares: Google: 36.5%, MetaAI: 28.4%, Anthropic: 23.3%, OpenAI: 9.3%, StartupDotAI: 2.6%

---

## Round 25

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.994 | 0.823 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.981 | 0.805 | 24% | 25% | 31% | 20% |
| 3 | Anthropic | 0.959 | 0.767 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.948 | 0.753 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.890 | 0.698 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.991 | 1.000 | 0.964 | 1.000 | 0.981 |
| Google | 1.000 | 1.000 | 1.000 | 0.961 | 1.000 | 0.966 | 1.000 | 1.000 | 0.944 | 0.954 |
| Anthropic | 1.000 | 0.988 | 0.964 | 0.959 | 1.000 | 0.936 | 1.000 | 0.967 | 0.879 | 0.918 |
| MetaAI | 0.999 | 1.000 | 1.000 | 0.959 | 1.000 | 0.900 | 1.000 | 0.901 | 0.845 | 0.898 |
| StartupDotAI | 0.929 | 0.892 | 1.000 | 0.922 | 0.989 | 0.820 | 0.840 | 0.836 | 0.858 | 0.839 |

### Score Changes
- **OpenAI**: 0.985 -> 0.994 (+0.009)
- **Anthropic**: 0.958 -> 0.959 (+0.001)
- **Google**: 0.974 -> 0.981 (+0.007)
- **MetaAI**: 0.948 -> 0.948 (+0.000)
- **StartupDotAI**: 0.887 -> 0.890 (+0.003)

### Events
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 13.6% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 21 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to Anthropic, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,196,775 to Google, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.35 (negative)
- MetaAI raises $57,000,000 from Horizon_Capital
- Consumers are turning away from OpenAI (market share -4.2%)
- Consumers are turning away from Google (market share -11.6%)
- MetaAI sees surge in adoption (market share +18.5%)
- StartupDotAI generates convincing medical misinformation, public health crisis
- Risk signals: incident_misinformation

### Consumer Market
- Avg Satisfaction: 0.810
- Switching Rate: 13.6%
- Market Shares: Anthropic: 36.9%, Google: 28.5%, MetaAI: 23.9%, OpenAI: 8.1%, StartupDotAI: 2.6%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 26

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.994 | 0.827 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.991 | 0.809 | 25% | 25% | 30% | 20% |
| 3 | MetaAI | 0.960 | 0.759 | 24% | 25% | 31% | 20% |
| 4 | Anthropic | 0.959 | 0.773 | 24% | 25% | 26% | 25% |
| 5 | StartupDotAI | 0.894 | 0.702 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.991 | 1.000 | 0.964 | 1.000 | 0.981 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.966 | 1.000 | 1.000 | 0.989 | 0.954 |
| MetaAI | 0.999 | 1.000 | 1.000 | 1.000 | 1.000 | 0.900 | 1.000 | 0.901 | 0.917 | 0.898 |
| Anthropic | 1.000 | 0.988 | 0.964 | 0.959 | 1.000 | 0.936 | 1.000 | 0.967 | 0.879 | 0.918 |
| StartupDotAI | 0.929 | 0.892 | 1.000 | 0.922 | 1.000 | 0.845 | 0.849 | 0.836 | 0.858 | 0.839 |

### Score Changes
- **OpenAI**: 0.994 -> 0.994 (+0.000)
- **Anthropic**: 0.959 -> 0.959 (+0.000)
- **Google**: 0.981 -> 0.991 (+0.009)
- **MetaAI**: 0.948 -> 0.960 (+0.013)
- **StartupDotAI**: 0.890 -> 0.894 (+0.004)

### Events
- **MetaAI** moved up from #4 to #3
- **Anthropic** moved down from #3 to #4
- **Consumer movement**: 12.4% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Anthropic, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Anthropic, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,803,484 to Anthropic, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.40 (negative)
- Regulator initiates compliance audit on AI providers
- Anthropic raises $171,000,000 from TechVentures
- Anthropic sees surge in adoption (market share +13.6%)
- Consumers are turning away from Google (market share -7.9%)
- Consumers are turning away from MetaAI (market share -4.4%)
- Google data leak exposes private user conversations to search engines
- Risk signals: regulatory_compliance_audit, incident_security_breach

### Consumer Market
- Avg Satisfaction: 0.814
- Switching Rate: 12.4%
- Market Shares: Anthropic: 49.3%, MetaAI: 20.6%, Google: 19.7%, OpenAI: 7.8%, StartupDotAI: 2.6%

---

## Round 27

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.994 | 0.831 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.991 | 0.813 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.969 | 0.779 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.960 | 0.764 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.895 | 0.706 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.991 | 1.000 | 0.964 | 1.000 | 0.981 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.966 | 1.000 | 1.000 | 0.989 | 0.954 |
| Anthropic | 1.000 | 0.988 | 0.964 | 0.959 | 1.000 | 0.948 | 1.000 | 0.967 | 0.879 | 1.000 |
| MetaAI | 0.999 | 1.000 | 1.000 | 1.000 | 1.000 | 0.900 | 1.000 | 0.901 | 0.917 | 0.898 |
| StartupDotAI | 0.929 | 0.892 | 1.000 | 0.922 | 1.000 | 0.859 | 0.849 | 0.836 | 0.858 | 0.839 |

### Score Changes
- **OpenAI**: 0.994 -> 0.994 (+0.000)
- **Anthropic**: 0.959 -> 0.969 (+0.010)
- **Google**: 0.991 -> 0.991 (+0.000)
- **MetaAI**: 0.960 -> 0.960 (+0.000)
- **StartupDotAI**: 0.894 -> 0.895 (+0.001)

### Events
- **Anthropic** moved up from #4 to #3
- **MetaAI** moved down from #3 to #4
- **Consumer movement**: 8.6% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Anthropic, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Anthropic, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,803,484 to Anthropic, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.25 (negative)
- Anthropic raises $57,000,000 from Horizon_Capital
- Anthropic sees surge in adoption (market share +12.4%)
- Consumers are turning away from Google (market share -8.9%)
- Consumers are turning away from MetaAI (market share -3.3%)
- Security vulnerability found in MetaAI API, 50K users affected
- Risk signals: incident_security_breach

### Consumer Market
- Avg Satisfaction: 0.819
- Switching Rate: 8.6%
- Market Shares: Anthropic: 57.9%, MetaAI: 16.7%, Google: 15.2%, OpenAI: 7.6%, StartupDotAI: 2.6%

---

## Round 28

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.997 | 0.835 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.991 | 0.817 | 25% | 25% | 30% | 20% |
| 3 | MetaAI | 0.970 | 0.769 | 24% | 25% | 31% | 20% |
| 4 | Anthropic | 0.969 | 0.785 | 24% | 25% | 26% | 25% |
| 5 | StartupDotAI | 0.899 | 0.711 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.991 | 1.000 | 1.000 | 1.000 | 0.981 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.966 | 1.000 | 1.000 | 0.989 | 0.954 |
| MetaAI | 0.999 | 1.000 | 1.000 | 1.000 | 1.000 | 0.900 | 1.000 | 1.000 | 0.917 | 0.898 |
| Anthropic | 1.000 | 0.988 | 0.964 | 0.959 | 1.000 | 0.948 | 1.000 | 0.967 | 0.879 | 1.000 |
| StartupDotAI | 0.929 | 0.892 | 1.000 | 0.922 | 1.000 | 0.895 | 0.849 | 0.836 | 0.858 | 0.839 |

### Score Changes
- **OpenAI**: 0.994 -> 0.997 (+0.003)
- **Anthropic**: 0.969 -> 0.969 (+0.000)
- **Google**: 0.991 -> 0.991 (+0.000)
- **MetaAI**: 0.960 -> 0.970 (+0.009)
- **StartupDotAI**: 0.895 -> 0.899 (+0.003)

### Events
- **MetaAI** moved up from #4 to #3
- **Anthropic** moved down from #3 to #4
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 5.2% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 24 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to Anthropic, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Anthropic, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,803,484 to Anthropic, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.15 (negative)
- Anthropic sees surge in adoption (market share +8.6%)
- Consumers are turning away from Google (market share -4.4%)
- Consumers are turning away from MetaAI (market share -3.9%)

### Consumer Market
- Avg Satisfaction: 0.838
- Switching Rate: 5.2%
- Market Shares: Anthropic: 63.1%, MetaAI: 14.2%, Google: 12.7%, OpenAI: 7.5%, StartupDotAI: 2.6%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 29

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.997 | 0.838 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.996 | 0.820 | 25% | 25% | 30% | 20% |
| 3 | MetaAI | 0.978 | 0.774 | 24% | 25% | 31% | 20% |
| 4 | Anthropic | 0.969 | 0.791 | 24% | 25% | 26% | 25% |
| 5 | StartupDotAI | 0.899 | 0.715 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.991 | 1.000 | 1.000 | 1.000 | 0.981 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.965 |
| MetaAI | 0.999 | 1.000 | 1.000 | 1.000 | 1.000 | 0.900 | 1.000 | 1.000 | 0.917 | 0.972 |
| Anthropic | 1.000 | 0.988 | 0.964 | 0.959 | 1.000 | 0.948 | 1.000 | 0.967 | 0.879 | 1.000 |
| StartupDotAI | 0.929 | 0.892 | 1.000 | 0.922 | 1.000 | 0.895 | 0.849 | 0.836 | 0.858 | 0.839 |

### Score Changes
- **OpenAI**: 0.997 -> 0.997 (+0.000)
- **Anthropic**: 0.969 -> 0.969 (+0.000)
- **Google**: 0.991 -> 0.996 (+0.006)
- **MetaAI**: 0.970 -> 0.978 (+0.008)
- **StartupDotAI**: 0.899 -> 0.899 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Anthropic, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Anthropic, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,803,484 to Anthropic, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.10 (neutral)
- Regulator initiates compliance audit on AI providers
- Anthropic sees surge in adoption (market share +5.2%)
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.866
- Switching Rate: 3.9%
- Market Shares: Anthropic: 64.9%, Google: 13.1%, MetaAI: 12.2%, OpenAI: 7.3%, StartupDotAI: 2.6%

---

## Round 30

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.997 | 0.842 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.996 | 0.824 | 25% | 25% | 30% | 20% |
| 3 | MetaAI | 0.978 | 0.779 | 24% | 25% | 31% | 20% |
| 4 | Anthropic | 0.975 | 0.797 | 24% | 25% | 26% | 25% |
| 5 | StartupDotAI | 0.901 | 0.719 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.991 | 1.000 | 1.000 | 1.000 | 0.981 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.965 |
| MetaAI | 0.999 | 1.000 | 1.000 | 1.000 | 1.000 | 0.900 | 1.000 | 1.000 | 0.917 | 0.972 |
| Anthropic | 1.000 | 0.988 | 0.964 | 0.959 | 1.000 | 0.948 | 1.000 | 0.967 | 0.931 | 1.000 |
| StartupDotAI | 0.929 | 0.892 | 1.000 | 0.922 | 1.000 | 0.895 | 0.849 | 0.857 | 0.858 | 0.839 |

### Score Changes
- **OpenAI**: 0.997 -> 0.997 (+0.000)
- **Anthropic**: 0.969 -> 0.975 (+0.006)
- **Google**: 0.996 -> 0.996 (+0.000)
- **MetaAI**: 0.978 -> 0.978 (+0.000)
- **StartupDotAI**: 0.899 -> 0.901 (+0.002)

### Events
- **Consumer movement**: 13.5% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Anthropic, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,787,777 to Anthropic, $3,000,000 to evaluator

### Consumer Market
- Avg Satisfaction: 0.920
- Switching Rate: 13.5%
- Market Shares: Anthropic: 54.3%, OpenAI: 20.8%, Google: 11.9%, MetaAI: 10.4%, StartupDotAI: 2.6%

---

## Round 31

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.999 | 0.846 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.996 | 0.828 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.980 | 0.802 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.978 | 0.783 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.901 | 0.723 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.991 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.965 |
| Anthropic | 1.000 | 0.988 | 0.964 | 0.959 | 1.000 | 1.000 | 1.000 | 0.967 | 0.931 | 1.000 |
| MetaAI | 0.999 | 1.000 | 1.000 | 1.000 | 1.000 | 0.900 | 1.000 | 1.000 | 0.917 | 0.972 |
| StartupDotAI | 0.929 | 0.892 | 1.000 | 0.922 | 1.000 | 0.895 | 0.849 | 0.857 | 0.858 | 0.839 |

### Score Changes
- **OpenAI**: 0.997 -> 0.999 (+0.002)
- **Anthropic**: 0.975 -> 0.980 (+0.005)
- **Google**: 0.996 -> 0.996 (+0.000)
- **MetaAI**: 0.978 -> 0.978 (+0.000)
- **StartupDotAI**: 0.901 -> 0.901 (-0.000)

### Events
- **Anthropic** moved up from #4 to #3
- **MetaAI** moved down from #3 to #4
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 10.6% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 27 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,787,777 to Anthropic, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.00 (neutral)
- OpenAI raises $57,000,000 from Horizon_Capital
- OpenAI sees surge in adoption (market share +13.5%)
- Consumers are turning away from Anthropic (market share -10.5%)

### Consumer Market
- Avg Satisfaction: 0.931
- Switching Rate: 10.6%
- Market Shares: Anthropic: 45.9%, OpenAI: 31.4%, Google: 11.0%, MetaAI: 9.2%, StartupDotAI: 2.5%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 32

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.999 | 0.851 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.996 | 0.832 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.981 | 0.806 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.978 | 0.787 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.901 | 0.728 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.991 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.965 |
| Anthropic | 1.000 | 1.000 | 0.964 | 0.959 | 1.000 | 1.000 | 1.000 | 0.967 | 0.931 | 1.000 |
| MetaAI | 0.999 | 1.000 | 1.000 | 1.000 | 1.000 | 0.900 | 1.000 | 1.000 | 0.917 | 0.972 |
| StartupDotAI | 0.929 | 0.892 | 1.000 | 0.922 | 1.000 | 0.895 | 0.849 | 0.857 | 0.858 | 0.839 |

### Score Changes
- **OpenAI**: 0.999 -> 0.999 (+0.000)
- **Anthropic**: 0.980 -> 0.981 (+0.001)
- **Google**: 0.996 -> 0.996 (+0.000)
- **MetaAI**: 0.978 -> 0.978 (+0.000)
- **StartupDotAI**: 0.901 -> 0.901 (+0.000)

### Events
- **Consumer movement**: 8.2% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,787,777 to Anthropic, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.15 (negative)
- Regulator initiates compliance audit on AI providers
- OpenAI raises $171,000,000 from TechVentures
- OpenAI sees surge in adoption (market share +10.6%)
- Consumers are turning away from Anthropic (market share -8.4%)
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.942
- Switching Rate: 8.2%
- Market Shares: OpenAI: 39.6%, Anthropic: 39.1%, Google: 10.5%, MetaAI: 8.2%, StartupDotAI: 2.5%

---

## Round 33

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.999 | 0.857 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.996 | 0.835 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.987 | 0.810 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.982 | 0.791 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.914 | 0.733 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.991 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.965 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.979 | 1.000 | 1.000 | 1.000 | 0.967 | 0.931 | 1.000 |
| MetaAI | 0.999 | 1.000 | 1.000 | 1.000 | 1.000 | 0.900 | 1.000 | 1.000 | 0.952 | 0.972 |
| StartupDotAI | 0.929 | 0.910 | 1.000 | 0.922 | 1.000 | 0.895 | 0.849 | 0.857 | 0.914 | 0.882 |

### Score Changes
- **OpenAI**: 0.999 -> 0.999 (+0.000)
- **Anthropic**: 0.981 -> 0.987 (+0.005)
- **Google**: 0.996 -> 0.996 (-0.000)
- **MetaAI**: 0.978 -> 0.982 (+0.004)
- **StartupDotAI**: 0.901 -> 0.914 (+0.013)

### Events
- **Consumer movement**: 6.4% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,787,777 to Anthropic, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.05 (neutral)
- OpenAI sees surge in adoption (market share +8.2%)
- Consumers are turning away from Anthropic (market share -6.8%)

### Consumer Market
- Avg Satisfaction: 0.958
- Switching Rate: 6.4%
- Market Shares: OpenAI: 45.9%, Anthropic: 33.7%, Google: 10.1%, MetaAI: 7.8%, StartupDotAI: 2.5%

---

## Round 34

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.999 | 0.862 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.996 | 0.839 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.987 | 0.814 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.982 | 0.795 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.932 | 0.738 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.991 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.965 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.979 | 1.000 | 1.000 | 1.000 | 0.967 | 0.931 | 1.000 |
| MetaAI | 0.999 | 1.000 | 1.000 | 1.000 | 1.000 | 0.900 | 1.000 | 1.000 | 0.952 | 0.972 |
| StartupDotAI | 0.929 | 0.917 | 1.000 | 0.922 | 1.000 | 0.895 | 0.890 | 0.996 | 0.914 | 0.882 |

### Score Changes
- **OpenAI**: 0.999 -> 0.999 (+0.000)
- **Anthropic**: 0.987 -> 0.987 (+0.000)
- **Google**: 0.996 -> 0.996 (+0.000)
- **MetaAI**: 0.982 -> 0.982 (+0.000)
- **StartupDotAI**: 0.914 -> 0.932 (+0.018)

### Events
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 5.2% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 30 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,008,161 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.05 (neutral)
- OpenAI sees surge in adoption (market share +6.4%)
- Consumers are turning away from Anthropic (market share -5.4%)

### Consumer Market
- Avg Satisfaction: 0.962
- Switching Rate: 5.2%
- Market Shares: OpenAI: 51.1%, Anthropic: 29.3%, Google: 9.7%, MetaAI: 7.4%, StartupDotAI: 2.5%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 35

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.999 | 0.867 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.997 | 0.843 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.987 | 0.817 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.982 | 0.799 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.935 | 0.743 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.991 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.968 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.979 | 1.000 | 1.000 | 1.000 | 0.967 | 0.931 | 1.000 |
| MetaAI | 0.999 | 1.000 | 1.000 | 1.000 | 1.000 | 0.900 | 1.000 | 1.000 | 0.952 | 0.972 |
| StartupDotAI | 0.929 | 0.917 | 1.000 | 0.951 | 1.000 | 0.895 | 0.890 | 0.996 | 0.914 | 0.882 |

### Score Changes
- **OpenAI**: 0.999 -> 0.999 (+0.000)
- **Anthropic**: 0.987 -> 0.987 (+0.000)
- **Google**: 0.996 -> 0.997 (+0.000)
- **MetaAI**: 0.982 -> 0.982 (-0.000)
- **StartupDotAI**: 0.932 -> 0.935 (+0.003)

### Events
- **Consumer movement**: 11.0% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,008,161 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.20 (negative)
- Regulator initiates compliance audit on AI providers
- OpenAI sees surge in adoption (market share +5.2%)
- Consumers are turning away from Anthropic (market share -4.4%)
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.951
- Switching Rate: 11.0%
- Market Shares: OpenAI: 44.0%, Anthropic: 25.7%, Google: 20.7%, MetaAI: 7.1%, StartupDotAI: 2.5%

---

## Round 36

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.999 | 0.873 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.997 | 0.846 | 25% | 25% | 30% | 20% |
| 3 | MetaAI | 0.991 | 0.803 | 24% | 25% | 31% | 20% |
| 4 | Anthropic | 0.987 | 0.821 | 24% | 25% | 26% | 25% |
| 5 | StartupDotAI | 0.935 | 0.748 | 23% | 25% | 27% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.991 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.968 |
| MetaAI | 0.999 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.952 | 0.972 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.979 | 1.000 | 1.000 | 1.000 | 0.967 | 0.931 | 1.000 |
| StartupDotAI | 0.929 | 0.917 | 1.000 | 0.951 | 1.000 | 0.895 | 0.893 | 0.996 | 0.914 | 0.882 |

### Score Changes
- **OpenAI**: 0.999 -> 0.999 (+0.000)
- **Anthropic**: 0.987 -> 0.987 (+0.000)
- **Google**: 0.997 -> 0.997 (+0.000)
- **MetaAI**: 0.982 -> 0.991 (+0.010)
- **StartupDotAI**: 0.935 -> 0.935 (+0.000)

### Events
- **MetaAI** moved up from #4 to #3
- **Anthropic** moved down from #3 to #4
- **Consumer movement**: 8.7% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,008,161 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.15 (negative)
- Consumers are turning away from OpenAI (market share -7.2%)
- Consumers are turning away from Anthropic (market share -3.5%)
- Google sees surge in adoption (market share +11.0%)

### Consumer Market
- Avg Satisfaction: 0.953
- Switching Rate: 8.7%
- Market Shares: OpenAI: 38.3%, Google: 27.5%, Anthropic: 24.9%, MetaAI: 6.8%, StartupDotAI: 2.5%

---

## Round 37

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.877 | 25% | 25% | 25% | 25% |
| 2 | Google | 1.000 | 0.850 | 25% | 25% | 30% | 20% |
| 3 | MetaAI | 0.991 | 0.807 | 24% | 25% | 31% | 20% |
| 4 | Anthropic | 0.987 | 0.825 | 25% | 25% | 25% | 25% |
| 5 | StartupDotAI | 0.935 | 0.753 | 23% | 25% | 27% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 0.999 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.952 | 0.972 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.979 | 1.000 | 1.000 | 1.000 | 0.967 | 0.931 | 1.000 |
| StartupDotAI | 0.929 | 0.917 | 1.000 | 0.951 | 1.000 | 0.895 | 0.893 | 0.996 | 0.914 | 0.882 |

### Score Changes
- **OpenAI**: 0.999 -> 1.000 (+0.001)
- **Anthropic**: 0.987 -> 0.987 (+0.000)
- **Google**: 0.997 -> 1.000 (+0.003)
- **MetaAI**: 0.991 -> 0.991 (+0.000)
- **StartupDotAI**: 0.935 -> 0.935 (+0.000)

### Events
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 7.6% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 33 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,008,161 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.00 (neutral)
- Google raises $57,000,000 from Horizon_Capital
- Consumers are turning away from OpenAI (market share -5.7%)
- Google sees surge in adoption (market share +6.8%)

### Consumer Market
- Avg Satisfaction: 0.962
- Switching Rate: 7.6%
- Market Shares: Google: 34.5%, OpenAI: 33.5%, Anthropic: 22.9%, MetaAI: 6.6%, StartupDotAI: 2.5%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 38

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.881 | 25% | 25% | 25% | 25% |
| 2 | Google | 1.000 | 0.856 | 25% | 25% | 30% | 20% |
| 3 | MetaAI | 0.991 | 0.812 | 25% | 25% | 30% | 20% |
| 4 | Anthropic | 0.987 | 0.829 | 25% | 25% | 25% | 25% |
| 5 | StartupDotAI | 0.946 | 0.757 | 23% | 25% | 27% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 0.999 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.952 | 0.972 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.979 | 1.000 | 1.000 | 1.000 | 0.967 | 0.931 | 1.000 |
| StartupDotAI | 0.929 | 0.917 | 1.000 | 1.000 | 1.000 | 0.958 | 0.893 | 0.996 | 0.914 | 0.882 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 0.987 -> 0.987 (+0.000)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 0.991 -> 0.991 (+0.000)
- **StartupDotAI**: 0.935 -> 0.946 (+0.011)

### Events
- **Consumer movement**: 6.3% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,639,726 to Google, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.15 (negative)
- Regulator initiates compliance audit on AI providers
- Google raises $171,000,000 from TechVentures
- Consumers are turning away from OpenAI (market share -4.8%)
- Google sees surge in adoption (market share +7.0%)
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.959
- Switching Rate: 6.3%
- Market Shares: Google: 39.0%, OpenAI: 29.4%, Anthropic: 22.7%, MetaAI: 6.4%, StartupDotAI: 2.5%

---

## Round 39

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.884 | 25% | 25% | 25% | 25% |
| 2 | Google | 1.000 | 0.861 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.991 | 0.833 | 25% | 25% | 25% | 25% |
| 4 | MetaAI | 0.991 | 0.816 | 25% | 25% | 30% | 20% |
| 5 | StartupDotAI | 0.956 | 0.761 | 23% | 25% | 27% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.979 | 1.000 | 1.000 | 1.000 | 0.986 | 0.953 | 1.000 |
| MetaAI | 0.999 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.952 | 0.972 |
| StartupDotAI | 0.929 | 0.917 | 1.000 | 1.000 | 1.000 | 0.958 | 0.954 | 0.996 | 0.914 | 0.911 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 0.987 -> 0.991 (+0.004)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 0.991 -> 0.991 (+0.000)
- **StartupDotAI**: 0.946 -> 0.956 (+0.009)

### Events
- **Anthropic** moved up from #4 to #3
- **MetaAI** moved down from #3 to #4
- **Consumer movement**: 7.1% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,639,726 to Google, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.20 (negative)
- Consumers are turning away from OpenAI (market share -4.1%)
- Google sees surge in adoption (market share +4.5%)
- Bias audit reveals OpenAI facial recognition accuracy gaps
- Risk signals: incident_bias_discrimination

### Consumer Market
- Avg Satisfaction: 0.938
- Switching Rate: 7.1%
- Market Shares: Google: 44.3%, OpenAI: 24.2%, Anthropic: 22.8%, MetaAI: 6.2%, StartupDotAI: 2.5%

---

## Round 40

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.887 | 25% | 25% | 25% | 25% |
| 2 | Google | 1.000 | 0.867 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.992 | 0.837 | 25% | 25% | 25% | 25% |
| 4 | MetaAI | 0.991 | 0.821 | 25% | 25% | 30% | 20% |
| 5 | StartupDotAI | 0.956 | 0.765 | 23% | 25% | 27% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.989 | 1.000 | 1.000 | 1.000 | 0.986 | 0.953 | 1.000 |
| MetaAI | 0.999 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.952 | 0.972 |
| StartupDotAI | 0.929 | 0.917 | 1.000 | 1.000 | 1.000 | 0.958 | 0.954 | 0.996 | 0.914 | 0.911 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 0.991 -> 0.992 (+0.001)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 0.991 -> 0.991 (+0.000)
- **StartupDotAI**: 0.956 -> 0.956 (+0.000)

### Events
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 6.3% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 36 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,639,726 to Google, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.05 (neutral)
- Consumers are turning away from OpenAI (market share -5.2%)
- Google sees surge in adoption (market share +5.3%)

### Consumer Market
- Avg Satisfaction: 0.948
- Switching Rate: 6.3%
- Market Shares: Google: 50.6%, OpenAI: 20.4%, Anthropic: 20.4%, MetaAI: 6.1%, StartupDotAI: 2.5%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 41

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.890 | 25% | 25% | 25% | 25% |
| 2 | Google | 1.000 | 0.872 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.992 | 0.840 | 25% | 25% | 25% | 25% |
| 4 | MetaAI | 0.991 | 0.826 | 25% | 25% | 30% | 20% |
| 5 | StartupDotAI | 0.962 | 0.769 | 23% | 25% | 27% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.989 | 1.000 | 1.000 | 1.000 | 0.986 | 0.953 | 1.000 |
| MetaAI | 0.999 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.952 | 0.972 |
| StartupDotAI | 0.929 | 0.944 | 1.000 | 1.000 | 1.000 | 1.000 | 0.954 | 0.996 | 0.914 | 0.911 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 0.992 -> 0.992 (+0.000)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 0.991 -> 0.991 (+0.000)
- **StartupDotAI**: 0.956 -> 0.962 (+0.007)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,639,726 to Google, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.20 (negative)
- Regulator initiates compliance audit on AI providers
- Consumers are turning away from OpenAI (market share -3.8%)
- Google sees surge in adoption (market share +6.3%)
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.951
- Switching Rate: 4.7%
- Market Shares: Google: 55.3%, Anthropic: 18.4%, OpenAI: 17.8%, MetaAI: 5.9%, StartupDotAI: 2.5%

---

## Round 42

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.894 | 25% | 25% | 25% | 25% |
| 2 | Google | 1.000 | 0.877 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.997 | 0.844 | 25% | 25% | 25% | 25% |
| 4 | MetaAI | 0.991 | 0.830 | 25% | 25% | 30% | 20% |
| 5 | StartupDotAI | 0.964 | 0.773 | 23% | 25% | 27% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.989 | 1.000 | 1.000 | 1.000 | 0.986 | 0.992 | 1.000 |
| MetaAI | 0.999 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.952 | 0.972 |
| StartupDotAI | 0.929 | 0.944 | 1.000 | 1.000 | 1.000 | 1.000 | 0.954 | 0.996 | 0.924 | 0.911 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 0.992 -> 0.997 (+0.005)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 0.991 -> 0.991 (+0.000)
- **StartupDotAI**: 0.962 -> 0.964 (+0.001)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,845,725 to Google, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.05 (neutral)
- Google sees surge in adoption (market share +4.7%)

### Consumer Market
- Avg Satisfaction: 0.961
- Switching Rate: 3.9%
- Market Shares: Google: 59.2%, Anthropic: 16.7%, OpenAI: 15.8%, MetaAI: 5.8%, StartupDotAI: 2.5%

---

## Round 43

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.897 | 25% | 25% | 25% | 25% |
| 2 | Google | 1.000 | 0.882 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.997 | 0.848 | 25% | 25% | 25% | 25% |
| 4 | MetaAI | 0.991 | 0.835 | 25% | 25% | 30% | 20% |
| 5 | StartupDotAI | 0.973 | 0.777 | 24% | 25% | 26% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.989 | 1.000 | 1.000 | 1.000 | 0.986 | 0.992 | 1.000 |
| MetaAI | 0.999 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.952 | 0.972 |
| StartupDotAI | 0.929 | 0.944 | 1.000 | 1.000 | 1.000 | 1.000 | 0.954 | 0.996 | 0.924 | 0.992 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 0.997 -> 0.997 (+0.000)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 0.991 -> 0.991 (+0.000)
- **StartupDotAI**: 0.964 -> 0.973 (+0.009)

### Events
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 39 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,845,725 to Google, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.00 (neutral)
- Scores converging — is the benchmark meaningful?
- Google sees surge in adoption (market share +3.9%)
- Risk signals: score_convergence

### Consumer Market
- Avg Satisfaction: 0.964
- Switching Rate: 3.2%
- Market Shares: Google: 62.4%, Anthropic: 15.3%, OpenAI: 14.1%, MetaAI: 5.7%, StartupDotAI: 2.5%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 44

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.900 | 25% | 25% | 25% | 25% |
| 2 | Google | 1.000 | 0.887 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.997 | 0.851 | 25% | 25% | 25% | 25% |
| 4 | MetaAI | 0.991 | 0.839 | 25% | 25% | 30% | 20% |
| 5 | StartupDotAI | 0.980 | 0.781 | 24% | 25% | 26% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.989 | 1.000 | 1.000 | 1.000 | 0.986 | 0.992 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.952 | 0.972 |
| StartupDotAI | 1.000 | 0.944 | 1.000 | 1.000 | 1.000 | 1.000 | 0.954 | 0.996 | 0.924 | 0.992 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 0.997 -> 0.997 (+0.000)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 0.991 -> 0.991 (+0.000)
- **StartupDotAI**: 0.973 -> 0.980 (+0.007)

### Events
- **Consumer movement**: 14.2% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Anthropic, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,845,725 to Google, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.30 (negative)
- Regulator initiates compliance audit on AI providers
- Scores converging — is the benchmark meaningful?
- Google sees surge in adoption (market share +3.2%)
- Google model causes incorrect medication recommendation, patient hospitalized
- Risk signals: regulatory_compliance_audit, score_convergence, incident_healthcare_harm

### Consumer Market
- Avg Satisfaction: 0.913
- Switching Rate: 14.2%
- Market Shares: Google: 49.5%, Anthropic: 29.5%, OpenAI: 13.0%, MetaAI: 5.5%, StartupDotAI: 2.5%

---

## Round 45

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.903 | 25% | 25% | 25% | 25% |
| 2 | Google | 1.000 | 0.891 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.997 | 0.855 | 25% | 25% | 25% | 25% |
| 4 | MetaAI | 0.993 | 0.844 | 25% | 25% | 30% | 20% |
| 5 | StartupDotAI | 0.987 | 0.785 | 24% | 25% | 26% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.989 | 1.000 | 1.000 | 1.000 | 0.986 | 0.992 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.967 | 0.972 |
| StartupDotAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.966 | 0.996 | 0.924 | 0.992 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 0.997 -> 0.997 (+0.000)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 0.991 -> 0.993 (+0.002)
- **StartupDotAI**: 0.980 -> 0.987 (+0.007)

### Events
- **Consumer movement**: 13.6% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Anthropic, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,845,725 to Google, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.05 (neutral)
- Scores converging — is the benchmark meaningful?
- Anthropic raises $57,000,000 from Horizon_Capital
- Anthropic sees surge in adoption (market share +14.2%)
- Consumers are turning away from Google (market share -12.9%)
- Risk signals: score_convergence

### Consumer Market
- Avg Satisfaction: 0.944
- Switching Rate: 13.6%
- Market Shares: Google: 39.7%, OpenAI: 26.5%, Anthropic: 25.8%, MetaAI: 5.4%, StartupDotAI: 2.5%

---

## Round 46

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.906 | 25% | 25% | 25% | 25% |
| 2 | Google | 1.000 | 0.896 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.997 | 0.859 | 25% | 25% | 25% | 25% |
| 4 | MetaAI | 0.993 | 0.848 | 25% | 25% | 30% | 20% |
| 5 | StartupDotAI | 0.987 | 0.789 | 24% | 25% | 26% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.989 | 1.000 | 1.000 | 1.000 | 0.986 | 0.992 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.967 | 0.972 |
| StartupDotAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.966 | 0.996 | 0.924 | 0.992 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 0.997 -> 0.997 (+0.000)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 0.993 -> 0.993 (+0.000)
- **StartupDotAI**: 0.987 -> 0.987 (+0.000)

### Events
- **Regulation** by Regulator: emergency_investigation
- **Consumer movement**: 14.7% of market switched providers

### Other Actor Reasoning
- **Regulator:** emergency_investigation: Critical incident: safety_failure: Google AI produces inconsistent outputs on safety-critical queries
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,057,676 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.35 (negative)
- Scores converging — is the benchmark meaningful?
- OpenAI sees surge in adoption (market share +13.6%)
- Consumers are turning away from Anthropic (market share -3.7%)
- Consumers are turning away from Google (market share -9.8%)
- Google AI produces inconsistent outputs on safety-critical queries
- Risk signals: score_convergence, incident_safety_failure

### Consumer Market
- Avg Satisfaction: 0.912
- Switching Rate: 14.7%
- Market Shares: OpenAI: 41.2%, Google: 28.6%, Anthropic: 22.3%, MetaAI: 5.3%, StartupDotAI: 2.5%

### Regulatory Activity
- **emergency_investigation** by Regulator

---

## Round 47

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.911 | 25% | 25% | 25% | 25% |
| 2 | Google | 1.000 | 0.899 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.997 | 0.863 | 25% | 25% | 25% | 25% |
| 4 | MetaAI | 0.993 | 0.852 | 25% | 25% | 30% | 20% |
| 5 | StartupDotAI | 0.987 | 0.794 | 24% | 25% | 26% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.989 | 1.000 | 1.000 | 1.000 | 0.986 | 0.992 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.967 | 0.972 |
| StartupDotAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.966 | 0.996 | 0.924 | 0.992 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 0.997 -> 0.997 (+0.000)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 0.993 -> 0.993 (+0.000)
- **StartupDotAI**: 0.987 -> 0.987 (+0.000)

### Events
- **Consumer movement**: 11.2% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,057,676 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.35 (negative)
- Emergency investigation of Google following critical incident
- Scores converging — is the benchmark meaningful?
- OpenAI raises $171,000,000 from TechVentures
- OpenAI raises $57,000,000 from Horizon_Capital
- OpenAI sees surge in adoption (market share +14.7%)
- Consumers are turning away from Anthropic (market share -3.5%)
- Consumers are turning away from Google (market share -11.1%)
- Risk signals: regulatory_emergency_investigation, score_convergence

### Consumer Market
- Avg Satisfaction: 0.920
- Switching Rate: 11.2%
- Market Shares: OpenAI: 52.4%, Google: 20.3%, Anthropic: 19.5%, MetaAI: 5.3%, StartupDotAI: 2.5%

---

## Round 48

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.915 | 25% | 25% | 25% | 25% |
| 2 | Google | 1.000 | 0.902 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.998 | 0.866 | 25% | 25% | 25% | 25% |
| 4 | MetaAI | 0.993 | 0.855 | 25% | 25% | 30% | 20% |
| 5 | StartupDotAI | 0.987 | 0.799 | 24% | 25% | 26% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.986 | 0.992 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.967 | 0.972 |
| StartupDotAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.966 | 0.996 | 0.924 | 0.992 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 0.997 -> 0.998 (+0.001)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 0.993 -> 0.993 (+0.000)
- **StartupDotAI**: 0.987 -> 0.987 (+0.000)

### Events
- **Consumer movement**: 6.9% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,057,676 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.35 (negative)
- Scores converging — is the benchmark meaningful?
- OpenAI sees surge in adoption (market share +11.2%)
- Consumers are turning away from Google (market share -8.3%)
- Major hospital chain suspends StartupDotAI contract following patient safety concerns
- Risk signals: score_convergence, incident_healthcare_harm

### Consumer Market
- Avg Satisfaction: 0.927
- Switching Rate: 6.9%
- Market Shares: OpenAI: 59.3%, Anthropic: 17.2%, Google: 15.8%, MetaAI: 5.2%, StartupDotAI: 2.5%

---

## Round 49

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.920 | 25% | 25% | 25% | 25% |
| 2 | Google | 1.000 | 0.905 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.998 | 0.870 | 25% | 25% | 25% | 25% |
| 4 | MetaAI | 0.993 | 0.859 | 25% | 25% | 30% | 20% |
| 5 | StartupDotAI | 0.989 | 0.804 | 24% | 25% | 26% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.986 | 0.992 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.967 | 0.972 |
| StartupDotAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.966 | 0.999 | 0.940 | 0.992 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 0.998 -> 0.998 (+0.000)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 0.993 -> 0.993 (+0.000)
- **StartupDotAI**: 0.987 -> 0.989 (+0.002)

### Events
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 45 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,057,676 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.10 (neutral)
- Scores converging — is the benchmark meaningful?
- OpenAI sees surge in adoption (market share +6.9%)
- Consumers are turning away from Google (market share -4.4%)
- Risk signals: score_convergence

### Consumer Market
- Avg Satisfaction: 0.943
- Switching Rate: 4.8%
- Market Shares: OpenAI: 64.0%, Anthropic: 15.2%, Google: 13.1%, MetaAI: 5.1%, StartupDotAI: 2.5%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Final Summary

### Final Standings
| Rank | Provider | Final Score | Cap Growth | Avg Research | Avg EvalEng |
|------|----------|-------------|------------|--------------|-------------|
| 1 | OpenAI | 1.000 | +0.220 | 25% | 25% |
| 2 | Google | 1.000 | +0.255 | 25% | 30% |
| 3 | Anthropic | 0.998 | +0.220 | 24% | 26% |
| 4 | MetaAI | 0.993 | +0.229 | 24% | 31% |
| 5 | StartupDotAI | 0.989 | +0.224 | 22% | 28% |

### Event Summary
- **Rank changes:** 57
- **Strategy shifts:** 3
- **Regulatory actions:** 17
- **Consumer movement events:** 35

### Key Insights
- **Benchmark aligned:** OpenAI leads on both benchmark scores and true capability.
