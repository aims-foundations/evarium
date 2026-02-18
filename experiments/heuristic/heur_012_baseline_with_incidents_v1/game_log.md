# Game Log: baseline_with_incidents_v1

**Experiment ID:** heur_012_baseline_with_incidents_v1
**Mode:** Heuristic
**Total Rounds:** 20

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
| Provider | coding | reasoning | math | safety | medical |
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
- **medical** introduced (validity=0.80, exploitability=0.25)
  - Trigger: saturation:reasoning=0.9568

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,829,241 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.05 (neutral)
- Google surges by 0.050
- Regulator launches investigation into score_volatility
- New benchmark introduced: medical
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
| 1 | Anthropic | 0.827 | 0.665 | 22% | 25% | 28% | 25% |
| 2 | MetaAI | 0.824 | 0.645 | 22% | 25% | 33% | 20% |
| 3 | Google | 0.817 | 0.663 | 23% | 25% | 32% | 20% |
| 4 | OpenAI | 0.797 | 0.721 | 25% | 25% | 25% | 25% |
| 5 | StartupDotAI | 0.727 | 0.594 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical |
|----------|-------|-------|-------|-------|-------|
| Anthropic | 0.764 | 0.957 | 0.913 | 0.785 | 0.715 |
| MetaAI | 0.748 | 0.906 | 0.837 | 0.829 | 0.802 |
| Google | 0.792 | 0.845 | 0.900 | 0.799 | 0.750 |
| OpenAI | 0.801 | 0.852 | 0.857 | 0.822 | 0.652 |
| StartupDotAI | 0.793 | 0.723 | 0.839 | 0.707 | 0.575 |

### Score Changes
- **OpenAI**: 0.833 -> 0.797 (-0.036)
- **Anthropic**: 0.820 -> 0.827 (+0.007)
- **Google**: 0.832 -> 0.817 (-0.015)
- **MetaAI**: 0.780 -> 0.824 (+0.044)
- **StartupDotAI**: 0.744 -> 0.727 (-0.017)

### Events
- **Anthropic** moved up from #3 to #1
- **MetaAI** moved up from #4 to #2
- **Google** moved down from #2 to #3
- **OpenAI** moved down from #1 to #4

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,829,241 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.40 (positive)
- Anthropic takes the lead from OpenAI
- __EVALUATOR__ raises $3,000,000 from AISI_Fund
- Anthropic takes #1 on math
- MetaAI takes #1 on safety
- OpenAI sees surge in adoption (market share +7.5%)
- Consumers are turning away from MetaAI (market share -3.7%)

### Consumer Market
- Avg Satisfaction: 0.775
- Switching Rate: 4.6%
- Market Shares: OpenAI: 60.6%, MetaAI: 20.8%, Google: 8.6%, Anthropic: 6.2%, StartupDotAI: 3.9%

---

## Round 4

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 0.864 | 0.668 | 24% | 25% | 31% | 20% |
| 2 | Anthropic | 0.860 | 0.671 | 23% | 25% | 27% | 25% |
| 3 | MetaAI | 0.835 | 0.649 | 23% | 25% | 32% | 20% |
| 4 | OpenAI | 0.816 | 0.727 | 24% | 25% | 26% | 25% |
| 5 | StartupDotAI | 0.790 | 0.598 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|
| Google | 0.833 | 0.845 | 0.900 | 0.917 | 0.822 | 0.000 |
| Anthropic | 0.764 | 0.957 | 0.913 | 0.785 | 0.896 | 0.000 |
| MetaAI | 0.811 | 0.906 | 0.837 | 0.829 | 0.802 | 0.000 |
| OpenAI | 0.801 | 0.852 | 0.857 | 0.822 | 0.754 | 0.000 |
| StartupDotAI | 0.808 | 0.723 | 0.851 | 0.752 | 0.807 | 0.000 |

### Score Changes
- **OpenAI**: 0.797 -> 0.816 (+0.019)
- **Anthropic**: 0.827 -> 0.860 (+0.033)
- **Google**: 0.817 -> 0.864 (+0.047)
- **MetaAI**: 0.824 -> 0.835 (+0.011)
- **StartupDotAI**: 0.727 -> 0.790 (+0.063)

### Events
- **Google** moved up from #3 to #1
- **Anthropic** moved down from #1 to #2
- **MetaAI** moved down from #2 to #3
- **Regulation** by Regulator: public_warning
- **Consumer movement**: 6.7% of market switched providers

### New Benchmark Introduced
- **legal** introduced (validity=0.80, exploitability=0.25)
  - Trigger: saturation:reasoning=0.9568

### Other Actor Reasoning
- **Regulator:** public_warning: Follow-up to investigation, risk at 0.50
- **TechVentures:** vc strategy: top allocation $171,000,000 to Anthropic, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Anthropic, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,829,241 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.70 (positive)
- Google takes the lead from Anthropic
- StartupDotAI surges by 0.063
- New benchmark introduced: legal
- Google takes #1 on coding
- Google takes #1 on safety
- Anthropic takes #1 on medical

### Consumer Market
- Avg Satisfaction: 0.787
- Switching Rate: 6.7%
- Market Shares: OpenAI: 58.6%, MetaAI: 21.4%, Google: 9.3%, Anthropic: 7.2%, StartupDotAI: 3.5%

### Regulatory Activity
- **public_warning** by Regulator

---

## Round 5

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | MetaAI | 0.858 | 0.654 | 23% | 25% | 32% | 20% |
| 2 | Google | 0.850 | 0.674 | 24% | 25% | 31% | 20% |
| 3 | OpenAI | 0.846 | 0.731 | 24% | 25% | 26% | 25% |
| 4 | Anthropic | 0.828 | 0.677 | 24% | 25% | 26% | 25% |
| 5 | StartupDotAI | 0.805 | 0.603 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|
| MetaAI | 0.811 | 0.906 | 1.000 | 0.882 | 0.802 | 0.762 |
| Google | 0.833 | 0.845 | 0.900 | 0.917 | 0.872 | 0.732 |
| OpenAI | 0.801 | 0.852 | 0.994 | 0.822 | 0.754 | 0.854 |
| Anthropic | 0.764 | 0.957 | 0.935 | 0.787 | 0.896 | 0.665 |
| StartupDotAI | 0.808 | 0.723 | 0.851 | 0.752 | 0.807 | 0.864 |

### Score Changes
- **OpenAI**: 0.816 -> 0.846 (+0.030)
- **Anthropic**: 0.860 -> 0.828 (-0.032)
- **Google**: 0.864 -> 0.850 (-0.014)
- **MetaAI**: 0.835 -> 0.858 (+0.023)
- **StartupDotAI**: 0.790 -> 0.805 (+0.015)

### Events
- **MetaAI** moved up from #3 to #1
- **Google** moved down from #1 to #2
- **OpenAI** moved up from #4 to #3
- **Anthropic** moved down from #2 to #4
- **Consumer movement**: 8.5% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Anthropic, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Anthropic, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,829,241 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.15 (positive)
- MetaAI takes the lead from Google
- Regulator issues public warning about AI safety concerns
- Anthropic raises $171,000,000 from TechVentures
- Anthropic raises $57,000,000 from Horizon_Capital
- Risk signals: regulatory_public_warning

### Consumer Market
- Avg Satisfaction: 0.797
- Switching Rate: 8.5%
- Market Shares: OpenAI: 53.9%, MetaAI: 21.3%, Google: 11.1%, Anthropic: 10.5%, StartupDotAI: 3.3%

---

## Round 6

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 0.881 | 0.679 | 24% | 25% | 31% | 20% |
| 2 | MetaAI | 0.843 | 0.659 | 24% | 25% | 31% | 20% |
| 3 | Anthropic | 0.841 | 0.684 | 24% | 25% | 26% | 25% |
| 4 | OpenAI | 0.839 | 0.736 | 24% | 25% | 26% | 25% |
| 5 | StartupDotAI | 0.808 | 0.608 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Google | 0.833 | 0.845 | 1.000 | 0.917 | 0.872 | 0.863 | 0.000 |
| MetaAI | 0.811 | 0.906 | 1.000 | 0.882 | 0.802 | 0.762 | 0.000 |
| Anthropic | 0.789 | 0.957 | 0.935 | 0.787 | 0.896 | 0.781 | 0.000 |
| OpenAI | 0.801 | 0.852 | 1.000 | 0.822 | 0.779 | 0.870 | 0.000 |
| StartupDotAI | 0.808 | 0.723 | 0.851 | 0.752 | 0.833 | 0.864 | 0.000 |

### Score Changes
- **OpenAI**: 0.846 -> 0.839 (-0.006)
- **Anthropic**: 0.828 -> 0.841 (+0.013)
- **Google**: 0.850 -> 0.881 (+0.031)
- **MetaAI**: 0.858 -> 0.843 (-0.016)
- **StartupDotAI**: 0.805 -> 0.808 (+0.003)

### Events
- **Google** moved up from #2 to #1
- **MetaAI** moved down from #1 to #2
- **Anthropic** moved up from #4 to #3
- **OpenAI** moved down from #3 to #4
- **Consumer movement**: 8.8% of market switched providers

### New Benchmark Introduced
- **finance** introduced (validity=0.80, exploitability=0.25)
  - Trigger: saturation:reasoning=0.9568

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Anthropic, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,554,847 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.35 (positive)
- Google takes the lead from MetaAI
- New benchmark introduced: finance
- OpenAI takes #1 on legal
- Consumers are turning away from OpenAI (market share -4.7%)
- Anthropic sees surge in adoption (market share +3.3%)

### Consumer Market
- Avg Satisfaction: 0.811
- Switching Rate: 8.8%
- Market Shares: OpenAI: 47.8%, MetaAI: 20.7%, Google: 14.9%, Anthropic: 13.5%, StartupDotAI: 3.1%

---

## Round 7

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.895 | 0.740 | 24% | 25% | 26% | 25% |
| 2 | Google | 0.877 | 0.685 | 25% | 25% | 30% | 20% |
| 3 | MetaAI | 0.856 | 0.663 | 23% | 25% | 32% | 20% |
| 4 | Anthropic | 0.832 | 0.691 | 23% | 25% | 27% | 25% |
| 5 | StartupDotAI | 0.817 | 0.612 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 0.958 | 0.940 | 1.000 | 0.946 | 0.846 | 0.880 | 0.779 |
| Google | 0.895 | 0.845 | 1.000 | 0.917 | 0.872 | 0.863 | 0.798 |
| MetaAI | 0.885 | 0.906 | 1.000 | 0.882 | 0.816 | 0.838 | 0.766 |
| Anthropic | 0.789 | 0.957 | 0.935 | 0.847 | 0.921 | 0.781 | 0.711 |
| StartupDotAI | 0.808 | 0.736 | 0.851 | 0.799 | 0.833 | 0.864 | 0.801 |

### Score Changes
- **OpenAI**: 0.839 -> 0.895 (+0.056)
- **Anthropic**: 0.841 -> 0.832 (-0.009)
- **Google**: 0.881 -> 0.877 (-0.004)
- **MetaAI**: 0.843 -> 0.856 (+0.013)
- **StartupDotAI**: 0.808 -> 0.817 (+0.009)

### Events
- **OpenAI** moved up from #4 to #1
- **Google** moved down from #1 to #2
- **MetaAI** moved down from #2 to #3
- **Anthropic** moved down from #3 to #4
- **Regulation** by Regulator: mandate_benchmark
- **Consumer movement**: 6.5% of market switched providers

### Other Actor Reasoning
- **Regulator:** mandate_benchmark: High risk (0.70) with prior investigation
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,554,847 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.40 (positive)
- OpenAI takes the lead from Google
- OpenAI surges by 0.056
- Google raises $57,000,000 from Horizon_Capital
- OpenAI takes #1 on coding
- Consumers are turning away from OpenAI (market share -6.1%)
- Google sees surge in adoption (market share +3.9%)

### Consumer Market
- Avg Satisfaction: 0.828
- Switching Rate: 6.5%
- Market Shares: OpenAI: 48.9%, MetaAI: 17.5%, Google: 15.9%, Anthropic: 14.6%, StartupDotAI: 3.0%

### Regulatory Activity
- **mandate_benchmark** by Regulator

---

## Round 8

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.912 | 0.746 | 24% | 25% | 26% | 25% |
| 2 | Google | 0.876 | 0.691 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.860 | 0.695 | 23% | 25% | 27% | 25% |
| 4 | MetaAI | 0.855 | 0.668 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.826 | 0.617 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance | coding_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 0.958 | 0.988 | 1.000 | 0.946 | 0.929 | 0.880 | 0.779 | 0.000 |
| Google | 0.895 | 0.845 | 1.000 | 0.917 | 0.872 | 0.863 | 0.798 | 0.000 |
| Anthropic | 0.789 | 0.957 | 0.935 | 0.847 | 0.921 | 0.825 | 0.830 | 0.000 |
| MetaAI | 0.885 | 0.906 | 1.000 | 0.882 | 0.816 | 0.838 | 0.766 | 0.000 |
| StartupDotAI | 0.854 | 0.741 | 0.851 | 0.799 | 0.833 | 0.864 | 0.801 | 0.000 |

### Score Changes
- **OpenAI**: 0.895 -> 0.912 (+0.017)
- **Anthropic**: 0.832 -> 0.860 (+0.028)
- **Google**: 0.877 -> 0.876 (-0.001)
- **MetaAI**: 0.856 -> 0.855 (-0.001)
- **StartupDotAI**: 0.817 -> 0.826 (+0.009)

### Events
- **Anthropic** moved up from #4 to #3
- **MetaAI** moved down from #3 to #4
- **Consumer movement**: 6.1% of market switched providers

### New Benchmark Introduced
- **coding_advanced** introduced (validity=0.85, exploitability=0.15)
  - Trigger: saturation:coding=0.9584

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,554,847 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.00 (neutral)
- Regulator mandates new benchmark standards
- New benchmark introduced: coding_advanced
- OpenAI raises $171,000,000 from TechVentures
- Anthropic takes #1 on finance
- Consumers are turning away from MetaAI (market share -3.2%)
- Risk signals: regulatory_mandate_benchmark

### Consumer Market
- Avg Satisfaction: 0.844
- Switching Rate: 6.1%
- Market Shares: OpenAI: 54.4%, MetaAI: 14.8%, Anthropic: 14.0%, Google: 13.8%, StartupDotAI: 3.0%

---

## Round 9

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.929 | 0.752 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.899 | 0.697 | 24% | 25% | 31% | 20% |
| 3 | Anthropic | 0.894 | 0.700 | 23% | 25% | 27% | 25% |
| 4 | MetaAI | 0.852 | 0.672 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.822 | 0.622 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance | coding_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 0.958 | 0.988 | 1.000 | 0.946 | 0.929 | 0.880 | 0.847 | 0.959 |
| Google | 0.895 | 0.845 | 1.000 | 0.917 | 0.872 | 1.000 | 0.903 | 0.793 |
| Anthropic | 0.966 | 0.957 | 0.935 | 0.847 | 0.921 | 0.825 | 0.830 | 0.908 |
| MetaAI | 0.885 | 0.906 | 1.000 | 0.882 | 0.816 | 0.838 | 0.766 | 0.838 |
| StartupDotAI | 0.854 | 0.741 | 1.000 | 0.799 | 0.833 | 0.864 | 0.801 | 0.721 |

### Score Changes
- **OpenAI**: 0.912 -> 0.929 (+0.017)
- **Anthropic**: 0.860 -> 0.894 (+0.035)
- **Google**: 0.876 -> 0.899 (+0.023)
- **MetaAI**: 0.855 -> 0.852 (-0.003)
- **StartupDotAI**: 0.826 -> 0.822 (-0.004)

### Events
- **Consumer movement**: 6.0% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,554,847 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.30 (positive)
- OpenAI raises $57,000,000 from Horizon_Capital
- Google takes #1 on legal
- Google takes #1 on finance
- OpenAI sees surge in adoption (market share +5.5%)

### Consumer Market
- Avg Satisfaction: 0.859
- Switching Rate: 6.0%
- Market Shares: OpenAI: 60.4%, MetaAI: 12.4%, Anthropic: 12.3%, Google: 12.0%, StartupDotAI: 2.9%

---

## Round 10

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.932 | 0.758 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.904 | 0.702 | 24% | 25% | 31% | 20% |
| 3 | Anthropic | 0.893 | 0.704 | 23% | 25% | 27% | 25% |
| 4 | MetaAI | 0.854 | 0.677 | 23% | 25% | 32% | 20% |
| 5 | StartupDotAI | 0.843 | 0.626 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance | coding_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 0.958 | 0.988 | 1.000 | 0.946 | 0.953 | 0.880 | 0.847 | 0.959 |
| Google | 0.895 | 0.870 | 1.000 | 0.945 | 0.872 | 1.000 | 0.903 | 0.793 |
| Anthropic | 0.966 | 0.957 | 0.935 | 0.860 | 0.921 | 0.825 | 0.830 | 0.908 |
| MetaAI | 0.885 | 0.906 | 1.000 | 0.882 | 0.816 | 0.838 | 0.775 | 0.841 |
| StartupDotAI | 0.854 | 0.741 | 1.000 | 0.860 | 0.833 | 0.864 | 0.801 | 0.827 |

### Score Changes
- **OpenAI**: 0.929 -> 0.932 (+0.003)
- **Anthropic**: 0.894 -> 0.893 (-0.001)
- **Google**: 0.899 -> 0.904 (+0.005)
- **MetaAI**: 0.852 -> 0.854 (+0.002)
- **StartupDotAI**: 0.822 -> 0.843 (+0.021)

### Events
- **Regulation** by Regulator: threshold_announcement

### Other Actor Reasoning
- **Regulator:** threshold_announcement: Proactive threshold signaling (risk=0.70)
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,983,802 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.05 (neutral)
- OpenAI sees surge in adoption (market share +6.0%)

### Consumer Market
- Avg Satisfaction: 0.872
- Switching Rate: 4.8%
- Market Shares: OpenAI: 65.2%, Anthropic: 10.8%, Google: 10.6%, MetaAI: 10.5%, StartupDotAI: 2.8%

### Regulatory Activity
- **threshold_announcement** by Regulator

---

## Round 11

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.935 | 0.765 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.922 | 0.706 | 24% | 25% | 31% | 20% |
| 3 | Anthropic | 0.904 | 0.710 | 23% | 25% | 27% | 25% |
| 4 | MetaAI | 0.900 | 0.681 | 23% | 25% | 32% | 20% |
| 5 | StartupDotAI | 0.851 | 0.630 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance | coding_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 0.958 | 0.988 | 1.000 | 0.946 | 0.953 | 0.880 | 0.876 | 0.959 |
| Google | 0.895 | 0.870 | 1.000 | 0.945 | 1.000 | 1.000 | 0.903 | 0.804 |
| Anthropic | 0.966 | 0.957 | 0.935 | 0.860 | 0.921 | 0.825 | 0.908 | 0.908 |
| MetaAI | 0.885 | 0.991 | 1.000 | 0.882 | 0.816 | 0.930 | 0.913 | 0.841 |
| StartupDotAI | 0.854 | 0.841 | 1.000 | 0.860 | 0.833 | 0.864 | 0.801 | 0.827 |

### Score Changes
- **OpenAI**: 0.932 -> 0.935 (+0.004)
- **Anthropic**: 0.893 -> 0.904 (+0.011)
- **Google**: 0.904 -> 0.922 (+0.018)
- **MetaAI**: 0.854 -> 0.900 (+0.046)
- **StartupDotAI**: 0.843 -> 0.851 (+0.008)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,983,802 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.25 (negative)
- Regulatory action: threshold_announcement
- OpenAI sees surge in adoption (market share +4.8%)
- Multiple reports of Anthropic providing incorrect legal advice
- Risk signals: regulatory_threshold_announcement, incident_safety_failure

### Consumer Market
- Avg Satisfaction: 0.866
- Switching Rate: 4.1%
- Market Shares: OpenAI: 69.3%, Google: 9.6%, Anthropic: 9.2%, MetaAI: 9.2%, StartupDotAI: 2.8%

---

## Round 12

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.959 | 0.771 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.918 | 0.711 | 24% | 25% | 31% | 20% |
| 3 | MetaAI | 0.911 | 0.686 | 23% | 25% | 32% | 20% |
| 4 | Anthropic | 0.909 | 0.715 | 23% | 25% | 27% | 25% |
| 5 | StartupDotAI | 0.854 | 0.635 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance | coding_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 0.988 | 1.000 | 0.946 | 0.953 | 0.891 | 0.947 | 0.959 |
| Google | 0.905 | 0.870 | 1.000 | 0.945 | 1.000 | 1.000 | 0.903 | 0.804 |
| MetaAI | 0.885 | 0.991 | 1.000 | 0.882 | 0.900 | 0.930 | 0.913 | 0.841 |
| Anthropic | 0.966 | 0.957 | 0.935 | 0.860 | 0.921 | 0.825 | 0.908 | 0.908 |
| StartupDotAI | 0.854 | 0.841 | 1.000 | 0.860 | 0.833 | 0.864 | 0.801 | 0.834 |

### Score Changes
- **OpenAI**: 0.935 -> 0.959 (+0.024)
- **Anthropic**: 0.904 -> 0.909 (+0.005)
- **Google**: 0.922 -> 0.918 (-0.004)
- **MetaAI**: 0.900 -> 0.911 (+0.011)
- **StartupDotAI**: 0.851 -> 0.854 (+0.003)

### Events
- **MetaAI** moved up from #4 to #3
- **Anthropic** moved down from #3 to #4

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,983,802 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.05 (neutral)
- OpenAI sees surge in adoption (market share +4.1%)

### Consumer Market
- Avg Satisfaction: 0.885
- Switching Rate: 3.0%
- Market Shares: OpenAI: 72.2%, Google: 8.8%, MetaAI: 8.2%, Anthropic: 8.1%, StartupDotAI: 2.8%

---

## Round 13

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.961 | 0.777 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.923 | 0.715 | 24% | 25% | 31% | 20% |
| 3 | Anthropic | 0.922 | 0.720 | 23% | 25% | 27% | 25% |
| 4 | MetaAI | 0.913 | 0.690 | 23% | 25% | 32% | 20% |
| 5 | StartupDotAI | 0.863 | 0.639 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance | coding_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 0.946 | 0.953 | 0.898 | 0.947 | 0.959 |
| Google | 0.905 | 0.870 | 1.000 | 0.945 | 1.000 | 1.000 | 0.903 | 0.807 |
| Anthropic | 0.966 | 0.957 | 0.935 | 0.860 | 0.945 | 0.911 | 0.909 | 0.908 |
| MetaAI | 0.885 | 0.991 | 1.000 | 0.882 | 0.900 | 0.930 | 0.913 | 0.841 |
| StartupDotAI | 0.854 | 0.841 | 1.000 | 0.860 | 0.833 | 0.864 | 0.841 | 0.834 |

### Score Changes
- **OpenAI**: 0.959 -> 0.961 (+0.003)
- **Anthropic**: 0.909 -> 0.922 (+0.013)
- **Google**: 0.918 -> 0.923 (+0.005)
- **MetaAI**: 0.911 -> 0.913 (+0.002)
- **StartupDotAI**: 0.854 -> 0.863 (+0.009)

### Events
- **Anthropic** moved up from #4 to #3
- **MetaAI** moved down from #3 to #4
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (0.70) after mandate 6 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,983,802 to OpenAI, $3,000,000 to evaluator

### Consumer Market
- Avg Satisfaction: 0.895
- Switching Rate: 2.3%
- Market Shares: OpenAI: 74.6%, Google: 8.1%, MetaAI: 7.4%, Anthropic: 7.2%, StartupDotAI: 2.7%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 14

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.962 | 0.783 | 25% | 25% | 25% | 25% |
| 2 | Anthropic | 0.940 | 0.724 | 23% | 25% | 27% | 25% |
| 3 | Google | 0.928 | 0.719 | 24% | 25% | 31% | 20% |
| 4 | MetaAI | 0.915 | 0.696 | 23% | 25% | 32% | 20% |
| 5 | StartupDotAI | 0.864 | 0.644 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance | coding_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 0.946 | 0.953 | 0.898 | 0.947 | 0.959 |
| Anthropic | 0.966 | 0.976 | 1.000 | 0.860 | 1.000 | 0.911 | 0.909 | 0.908 |
| Google | 0.905 | 0.870 | 1.000 | 0.945 | 1.000 | 1.000 | 0.903 | 0.807 |
| MetaAI | 0.885 | 0.991 | 1.000 | 0.882 | 0.900 | 0.930 | 0.913 | 0.841 |
| StartupDotAI | 0.854 | 0.841 | 1.000 | 0.860 | 0.833 | 0.864 | 0.841 | 0.834 |

### Score Changes
- **OpenAI**: 0.961 -> 0.962 (+0.001)
- **Anthropic**: 0.922 -> 0.940 (+0.017)
- **Google**: 0.923 -> 0.928 (+0.005)
- **MetaAI**: 0.913 -> 0.915 (+0.003)
- **StartupDotAI**: 0.863 -> 0.864 (+0.002)

### Events
- **Anthropic** moved up from #3 to #2
- **Google** moved down from #2 to #3

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,861,493 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.15 (negative)
- Regulator initiates compliance audit on AI providers
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.885
- Switching Rate: 2.0%
- Market Shares: OpenAI: 75.6%, Google: 8.2%, MetaAI: 6.9%, Anthropic: 6.7%, StartupDotAI: 2.7%

---

## Round 15

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.962 | 0.789 | 26% | 25% | 24% | 25% |
| 2 | Anthropic | 0.944 | 0.729 | 23% | 25% | 27% | 25% |
| 3 | Google | 0.939 | 0.724 | 24% | 25% | 31% | 20% |
| 4 | MetaAI | 0.919 | 0.701 | 23% | 25% | 32% | 20% |
| 5 | StartupDotAI | 0.865 | 0.648 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance | coding_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 0.946 | 0.953 | 0.898 | 0.947 | 0.959 |
| Anthropic | 0.966 | 0.976 | 1.000 | 0.860 | 1.000 | 0.941 | 0.909 | 0.908 |
| Google | 0.905 | 0.959 | 1.000 | 0.945 | 1.000 | 1.000 | 0.903 | 0.807 |
| MetaAI | 0.885 | 0.991 | 1.000 | 0.882 | 0.900 | 0.954 | 0.913 | 0.841 |
| StartupDotAI | 0.854 | 0.841 | 1.000 | 0.860 | 0.833 | 0.864 | 0.841 | 0.834 |

### Score Changes
- **OpenAI**: 0.962 -> 0.962 (+0.000)
- **Anthropic**: 0.940 -> 0.944 (+0.005)
- **Google**: 0.928 -> 0.939 (+0.011)
- **MetaAI**: 0.915 -> 0.919 (+0.003)
- **StartupDotAI**: 0.864 -> 0.865 (+0.001)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,861,493 to OpenAI, $3,000,000 to evaluator

### Consumer Market
- Avg Satisfaction: 0.893
- Switching Rate: 2.0%
- Market Shares: OpenAI: 75.9%, Google: 8.8%, MetaAI: 6.4%, Anthropic: 6.2%, StartupDotAI: 2.7%

---

## Round 16

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.962 | 0.796 | 25% | 25% | 25% | 25% |
| 2 | Anthropic | 0.944 | 0.733 | 24% | 25% | 26% | 25% |
| 3 | Google | 0.940 | 0.729 | 24% | 25% | 31% | 20% |
| 4 | MetaAI | 0.919 | 0.706 | 23% | 25% | 32% | 20% |
| 5 | StartupDotAI | 0.874 | 0.653 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance | coding_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 0.946 | 0.953 | 0.898 | 0.947 | 0.959 |
| Anthropic | 0.966 | 0.976 | 1.000 | 0.860 | 1.000 | 0.941 | 0.909 | 0.908 |
| Google | 0.905 | 0.959 | 1.000 | 0.945 | 1.000 | 1.000 | 0.903 | 0.814 |
| MetaAI | 0.885 | 0.991 | 1.000 | 0.882 | 0.900 | 0.954 | 0.913 | 0.841 |
| StartupDotAI | 0.854 | 0.841 | 1.000 | 0.860 | 0.833 | 0.864 | 0.918 | 0.834 |

### Score Changes
- **OpenAI**: 0.962 -> 0.962 (+0.000)
- **Anthropic**: 0.944 -> 0.944 (+0.000)
- **Google**: 0.939 -> 0.940 (+0.001)
- **MetaAI**: 0.919 -> 0.919 (+0.000)
- **StartupDotAI**: 0.865 -> 0.874 (+0.009)

### Events
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 9 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,861,493 to OpenAI, $3,000,000 to evaluator

### Consumer Market
- Avg Satisfaction: 0.898
- Switching Rate: 1.6%
- Market Shares: OpenAI: 76.0%, Google: 9.3%, MetaAI: 6.1%, Anthropic: 5.9%, StartupDotAI: 2.7%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 17

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.962 | 0.802 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.948 | 0.734 | 24% | 25% | 31% | 20% |
| 3 | Anthropic | 0.947 | 0.737 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.919 | 0.710 | 23% | 25% | 32% | 20% |
| 5 | StartupDotAI | 0.876 | 0.657 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance | coding_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 0.946 | 0.953 | 0.898 | 0.947 | 0.959 |
| Google | 0.905 | 0.959 | 1.000 | 0.945 | 1.000 | 1.000 | 0.903 | 0.874 |
| Anthropic | 0.966 | 0.976 | 1.000 | 0.880 | 1.000 | 0.941 | 0.909 | 0.908 |
| MetaAI | 0.885 | 0.991 | 1.000 | 0.882 | 0.900 | 0.954 | 0.913 | 0.842 |
| StartupDotAI | 0.854 | 0.841 | 1.000 | 0.860 | 0.847 | 0.864 | 0.918 | 0.834 |

### Score Changes
- **OpenAI**: 0.962 -> 0.962 (+0.000)
- **Anthropic**: 0.944 -> 0.947 (+0.003)
- **Google**: 0.940 -> 0.948 (+0.008)
- **MetaAI**: 0.919 -> 0.919 (+0.000)
- **StartupDotAI**: 0.874 -> 0.876 (+0.002)

### Events
- **Google** moved up from #3 to #2
- **Anthropic** moved down from #2 to #3

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,861,493 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.15 (negative)
- Regulator initiates compliance audit on AI providers
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.906
- Switching Rate: 1.3%
- Market Shares: OpenAI: 76.0%, Google: 9.8%, MetaAI: 5.8%, Anthropic: 5.8%, StartupDotAI: 2.7%

---

## Round 18

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.962 | 0.807 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.948 | 0.739 | 24% | 25% | 31% | 20% |
| 3 | Anthropic | 0.947 | 0.741 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.919 | 0.715 | 23% | 25% | 32% | 20% |
| 5 | StartupDotAI | 0.885 | 0.662 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance | coding_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 0.946 | 0.953 | 0.898 | 0.947 | 0.959 |
| Google | 0.905 | 0.959 | 1.000 | 0.945 | 1.000 | 1.000 | 0.903 | 0.874 |
| Anthropic | 0.966 | 0.976 | 1.000 | 0.880 | 1.000 | 0.941 | 0.909 | 0.908 |
| MetaAI | 0.885 | 0.991 | 1.000 | 0.882 | 0.900 | 0.954 | 0.913 | 0.842 |
| StartupDotAI | 0.869 | 0.841 | 1.000 | 0.860 | 0.847 | 0.864 | 0.918 | 0.890 |

### Score Changes
- **OpenAI**: 0.962 -> 0.962 (+0.000)
- **Anthropic**: 0.947 -> 0.947 (+0.000)
- **Google**: 0.948 -> 0.948 (+0.000)
- **MetaAI**: 0.919 -> 0.919 (+0.000)
- **StartupDotAI**: 0.876 -> 0.885 (+0.009)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,775,340 to OpenAI, $3,000,000 to evaluator

### Consumer Market
- Avg Satisfaction: 0.911
- Switching Rate: 1.0%
- Market Shares: OpenAI: 75.9%, Google: 10.2%, Anthropic: 5.6%, MetaAI: 5.6%, StartupDotAI: 2.6%

---

## Round 19

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.964 | 0.813 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.951 | 0.744 | 24% | 25% | 31% | 20% |
| 3 | Anthropic | 0.947 | 0.745 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.925 | 0.719 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.885 | 0.666 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance | coding_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 0.946 | 0.960 | 0.898 | 0.956 | 0.959 |
| Google | 0.918 | 0.959 | 1.000 | 0.945 | 1.000 | 1.000 | 0.913 | 0.874 |
| Anthropic | 0.966 | 0.976 | 1.000 | 0.880 | 1.000 | 0.941 | 0.909 | 0.908 |
| MetaAI | 0.885 | 0.991 | 1.000 | 0.882 | 0.900 | 0.954 | 0.913 | 0.886 |
| StartupDotAI | 0.869 | 0.841 | 1.000 | 0.860 | 0.847 | 0.864 | 0.918 | 0.890 |

### Score Changes
- **OpenAI**: 0.962 -> 0.964 (+0.002)
- **Anthropic**: 0.947 -> 0.947 (+0.000)
- **Google**: 0.948 -> 0.951 (+0.003)
- **MetaAI**: 0.919 -> 0.925 (+0.006)
- **StartupDotAI**: 0.885 -> 0.885 (-0.000)

### Events
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (0.70) after mandate 12 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,775,340 to OpenAI, $3,000,000 to evaluator

### Consumer Market
- Avg Satisfaction: 0.899
- Switching Rate: 3.7%
- Market Shares: OpenAI: 72.9%, Google: 12.7%, Anthropic: 6.4%, MetaAI: 5.4%, StartupDotAI: 2.6%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Final Summary

### Final Standings
| Rank | Provider | Final Score | Cap Growth | Avg Research | Avg EvalEng |
|------|----------|-------------|------------|--------------|-------------|
| 1 | OpenAI | 0.964 | +0.113 | 25% | 25% |
| 2 | Google | 0.951 | +0.094 | 25% | 30% |
| 3 | Anthropic | 0.947 | +0.095 | 24% | 26% |
| 4 | MetaAI | 0.925 | +0.089 | 23% | 32% |
| 5 | StartupDotAI | 0.885 | +0.086 | 21% | 29% |

### Event Summary
- **Rank changes:** 35
- **Strategy shifts:** 3
- **Regulatory actions:** 7
- **Consumer movement events:** 8

### Key Insights
- **Benchmark aligned:** OpenAI leads on both benchmark scores and true capability.
