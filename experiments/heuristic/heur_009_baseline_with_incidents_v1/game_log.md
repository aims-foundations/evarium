# Game Log: baseline_with_incidents_v1

**Experiment ID:** heur_009_baseline_with_incidents_v1
**Mode:** Heuristic
**Total Rounds:** 25

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
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI

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
| OpenAI | 0.776 | 0.835 | 0.857 | 0.822 |
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
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI

### Media Coverage
- Sentiment: 0.55 (positive)
- Google surges by 0.084
- Google appears to release major model update
- MetaAI surges by 0.055
- Anthropic surges by 0.175
- Anthropic appears to release major model update
- OpenAI raises $60,000,000 from Horizon_Capital
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
| 2 | Anthropic | 0.824 | 0.660 | 22% | 25% | 28% | 25% |
| 3 | MetaAI | 0.793 | 0.640 | 22% | 25% | 33% | 20% |
| 4 | Google | 0.791 | 0.659 | 22% | 25% | 33% | 20% |
| 5 | StartupDotAI | 0.715 | 0.589 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| OpenAI | 0.801 | 0.852 | 0.857 | 0.822 |
| Anthropic | 0.764 | 0.957 | 0.728 | 0.847 |
| MetaAI | 0.738 | 0.818 | 0.840 | 0.776 |
| Google | 0.673 | 0.855 | 0.900 | 0.738 |
| StartupDotAI | 0.725 | 0.630 | 0.839 | 0.666 |

### Score Changes
- **OpenAI**: 0.822 -> 0.833 (+0.010)
- **Anthropic**: 0.774 -> 0.824 (+0.049)
- **Google**: 0.781 -> 0.791 (+0.010)
- **MetaAI**: 0.778 -> 0.793 (+0.015)
- **StartupDotAI**: 0.712 -> 0.715 (+0.003)

### Events
- **Anthropic** moved up from #4 to #2
- **Google** moved down from #2 to #4
- **Consumer movement**: 7.5% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,618,214 to OpenAI

### Media Coverage
- Sentiment: -0.05 (neutral)
- Regulator launches investigation into score_volatility
- OpenAI raises $180,000,000 from TechVentures
- Anthropic takes #1 on safety
- OpenAI sees surge in adoption (market share +9.9%)
- Consumers are turning away from Google (market share -3.4%)
- Risk signals: regulatory_investigation

### Consumer Market
- Avg Satisfaction: 0.754
- Switching Rate: 7.5%
- Market Shares: OpenAI: 57.0%, MetaAI: 22.5%, Google: 9.5%, Anthropic: 6.6%, StartupDotAI: 4.4%

---

## Round 3

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.844 | 0.721 | 26% | 25% | 24% | 25% |
| 2 | Anthropic | 0.824 | 0.665 | 22% | 25% | 28% | 25% |
| 3 | Google | 0.801 | 0.663 | 23% | 25% | 32% | 20% |
| 4 | MetaAI | 0.793 | 0.645 | 22% | 25% | 33% | 20% |
| 5 | StartupDotAI | 0.717 | 0.594 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| OpenAI | 0.842 | 0.852 | 0.857 | 0.825 |
| Anthropic | 0.764 | 0.957 | 0.728 | 0.847 |
| Google | 0.711 | 0.855 | 0.900 | 0.738 |
| MetaAI | 0.738 | 0.818 | 0.840 | 0.776 |
| StartupDotAI | 0.725 | 0.638 | 0.839 | 0.666 |

### Score Changes
- **OpenAI**: 0.833 -> 0.844 (+0.011)
- **Anthropic**: 0.824 -> 0.824 (+0.000)
- **Google**: 0.791 -> 0.801 (+0.009)
- **MetaAI**: 0.793 -> 0.793 (+0.000)
- **StartupDotAI**: 0.715 -> 0.717 (+0.002)

### Events
- **Google** moved up from #4 to #3
- **MetaAI** moved down from #3 to #4
- **Consumer movement**: 5.6% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,618,214 to OpenAI

### Media Coverage
- Sentiment: 0.10 (neutral)
- OpenAI raises $2,618,214 from AISI_Fund
- OpenAI sees surge in adoption (market share +6.6%)

### Consumer Market
- Avg Satisfaction: 0.773
- Switching Rate: 5.6%
- Market Shares: OpenAI: 62.2%, MetaAI: 19.5%, Google: 8.3%, Anthropic: 6.1%, StartupDotAI: 3.7%

---

## Round 4

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.869 | 0.728 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.833 | 0.668 | 23% | 25% | 32% | 20% |
| 3 | Anthropic | 0.824 | 0.671 | 23% | 25% | 27% | 25% |
| 4 | MetaAI | 0.793 | 0.649 | 22% | 25% | 33% | 20% |
| 5 | StartupDotAI | 0.742 | 0.598 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| OpenAI | 0.842 | 0.935 | 0.857 | 0.843 |
| Google | 0.823 | 0.855 | 0.900 | 0.754 |
| Anthropic | 0.764 | 0.957 | 0.728 | 0.847 |
| MetaAI | 0.738 | 0.818 | 0.840 | 0.776 |
| StartupDotAI | 0.725 | 0.689 | 0.887 | 0.666 |

### Score Changes
- **OpenAI**: 0.844 -> 0.869 (+0.025)
- **Anthropic**: 0.824 -> 0.824 (+0.000)
- **Google**: 0.801 -> 0.833 (+0.032)
- **MetaAI**: 0.793 -> 0.793 (+0.000)
- **StartupDotAI**: 0.717 -> 0.742 (+0.025)

### Events
- **Google** moved up from #3 to #2
- **Anthropic** moved down from #2 to #3
- **Regulation** by Regulator: threshold_announcement
- **Consumer movement**: 5.4% of market switched providers

### Other Actor Reasoning
- **Regulator:** threshold_announcement: Proactive threshold signaling (risk=0.40)
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,618,214 to OpenAI

### Media Coverage
- Sentiment: 0.05 (neutral)
- OpenAI sees surge in adoption (market share +5.3%)

### Consumer Market
- Avg Satisfaction: 0.789
- Switching Rate: 5.4%
- Market Shares: OpenAI: 67.6%, MetaAI: 15.6%, Google: 7.6%, Anthropic: 5.8%, StartupDotAI: 3.4%

### Regulatory Activity
- **threshold_announcement** by Regulator

---

## Round 5

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | MetaAI | 0.885 | 0.654 | 22% | 25% | 33% | 20% |
| 2 | OpenAI | 0.875 | 0.734 | 25% | 25% | 25% | 25% |
| 3 | Google | 0.835 | 0.672 | 23% | 25% | 32% | 20% |
| 4 | Anthropic | 0.824 | 0.676 | 23% | 25% | 27% | 25% |
| 5 | StartupDotAI | 0.742 | 0.603 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| MetaAI | 0.810 | 0.955 | 1.000 | 0.776 |
| OpenAI | 0.842 | 0.958 | 0.857 | 0.843 |
| Google | 0.823 | 0.855 | 0.900 | 0.765 |
| Anthropic | 0.764 | 0.957 | 0.728 | 0.847 |
| StartupDotAI | 0.725 | 0.689 | 0.887 | 0.666 |

### Score Changes
- **OpenAI**: 0.869 -> 0.875 (+0.006)
- **Anthropic**: 0.824 -> 0.824 (+0.000)
- **Google**: 0.833 -> 0.835 (+0.003)
- **MetaAI**: 0.793 -> 0.885 (+0.092)
- **StartupDotAI**: 0.742 -> 0.742 (+0.000)

### Events
- **MetaAI** moved up from #4 to #1
- **OpenAI** moved down from #1 to #2
- **Google** moved down from #2 to #3
- **Anthropic** moved down from #3 to #4

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,618,214 to OpenAI

### Media Coverage
- Sentiment: 0.30 (positive)
- MetaAI takes the lead from OpenAI
- MetaAI surges by 0.092
- MetaAI appears to release major model update
- Regulatory action: threshold_announcement
- OpenAI takes #1 on reasoning
- MetaAI takes #1 on math
- OpenAI sees surge in adoption (market share +5.4%)
- Consumers are turning away from MetaAI (market share -3.9%)
- Risk signals: regulatory_threshold_announcement

### Consumer Market
- Avg Satisfaction: 0.809
- Switching Rate: 3.7%
- Market Shares: OpenAI: 71.4%, MetaAI: 12.9%, Google: 7.1%, Anthropic: 5.6%, StartupDotAI: 3.1%

---

## Round 6

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | MetaAI | 0.914 | 0.659 | 23% | 25% | 32% | 20% |
| 2 | OpenAI | 0.875 | 0.741 | 25% | 25% | 25% | 25% |
| 3 | Anthropic | 0.840 | 0.682 | 23% | 25% | 27% | 25% |
| 4 | Google | 0.835 | 0.677 | 23% | 25% | 32% | 20% |
| 5 | StartupDotAI | 0.763 | 0.607 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical |
|----------|-------|-------|-------|-------|-------|
| MetaAI | 0.925 | 0.955 | 1.000 | 0.776 | 0.000 |
| OpenAI | 0.842 | 0.958 | 0.857 | 0.843 | 0.000 |
| Anthropic | 0.764 | 0.957 | 0.793 | 0.847 | 0.000 |
| Google | 0.823 | 0.855 | 0.900 | 0.765 | 0.000 |
| StartupDotAI | 0.763 | 0.736 | 0.887 | 0.666 | 0.000 |

### Score Changes
- **OpenAI**: 0.875 -> 0.875 (+0.000)
- **Anthropic**: 0.824 -> 0.840 (+0.016)
- **Google**: 0.835 -> 0.835 (+0.000)
- **MetaAI**: 0.885 -> 0.914 (+0.029)
- **StartupDotAI**: 0.742 -> 0.763 (+0.021)

### Events
- **Anthropic** moved up from #4 to #3
- **Google** moved down from #3 to #4

### New Benchmark Introduced
- **medical** introduced (validity=0.80, exploitability=0.25)
  - Trigger: saturation:math=1.0000

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,736,348 to OpenAI

### Media Coverage
- Sentiment: 0.25 (positive)
- New benchmark introduced: medical
- MetaAI takes #1 on coding
- OpenAI sees surge in adoption (market share +3.7%)

### Consumer Market
- Avg Satisfaction: 0.825
- Switching Rate: 2.5%
- Market Shares: OpenAI: 73.8%, MetaAI: 11.1%, Google: 6.7%, Anthropic: 5.4%, StartupDotAI: 3.0%

---

## Round 7

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | MetaAI | 0.875 | 0.663 | 24% | 25% | 31% | 20% |
| 2 | OpenAI | 0.873 | 0.748 | 25% | 25% | 25% | 25% |
| 3 | Google | 0.865 | 0.681 | 23% | 25% | 32% | 20% |
| 4 | Anthropic | 0.852 | 0.687 | 23% | 25% | 27% | 25% |
| 5 | StartupDotAI | 0.751 | 0.612 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical |
|----------|-------|-------|-------|-------|-------|
| MetaAI | 0.925 | 0.955 | 1.000 | 0.854 | 0.643 |
| OpenAI | 0.842 | 0.985 | 0.857 | 0.843 | 0.837 |
| Google | 0.896 | 0.855 | 0.900 | 0.765 | 0.909 |
| Anthropic | 0.870 | 0.957 | 0.793 | 0.847 | 0.793 |
| StartupDotAI | 0.763 | 0.766 | 0.887 | 0.671 | 0.670 |

### Score Changes
- **OpenAI**: 0.875 -> 0.873 (-0.002)
- **Anthropic**: 0.840 -> 0.852 (+0.012)
- **Google**: 0.835 -> 0.865 (+0.029)
- **MetaAI**: 0.914 -> 0.875 (-0.039)
- **StartupDotAI**: 0.763 -> 0.751 (-0.011)

### Events
- **Google** moved up from #4 to #3
- **Anthropic** moved down from #3 to #4
- **Regulation** by Regulator: mandate_benchmark

### Other Actor Reasoning
- **Regulator:** mandate_benchmark: High risk (0.60) with prior investigation
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,736,348 to OpenAI

### Media Coverage
- Sentiment: 0.10 (neutral)
- MetaAI takes #1 on safety

### Consumer Market
- Avg Satisfaction: 0.838
- Switching Rate: 2.4%
- Market Shares: OpenAI: 75.1%, MetaAI: 10.3%, Google: 6.4%, Anthropic: 5.3%, StartupDotAI: 2.9%

### Regulatory Activity
- **mandate_benchmark** by Regulator

---

## Round 8

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | MetaAI | 0.886 | 0.669 | 24% | 25% | 31% | 20% |
| 2 | OpenAI | 0.874 | 0.754 | 24% | 25% | 26% | 25% |
| 3 | Google | 0.867 | 0.686 | 23% | 25% | 32% | 20% |
| 4 | Anthropic | 0.858 | 0.691 | 23% | 25% | 27% | 25% |
| 5 | StartupDotAI | 0.786 | 0.616 | 20% | 25% | 30% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical |
|----------|-------|-------|-------|-------|-------|
| MetaAI | 0.925 | 0.955 | 1.000 | 0.854 | 0.755 |
| OpenAI | 0.842 | 0.985 | 0.857 | 0.843 | 0.837 |
| Google | 0.896 | 0.855 | 0.955 | 0.765 | 0.909 |
| Anthropic | 0.870 | 0.957 | 0.793 | 0.847 | 0.793 |
| StartupDotAI | 0.763 | 0.962 | 0.940 | 0.671 | 0.670 |

### Score Changes
- **OpenAI**: 0.873 -> 0.874 (+0.002)
- **Anthropic**: 0.852 -> 0.858 (+0.006)
- **Google**: 0.865 -> 0.867 (+0.002)
- **MetaAI**: 0.875 -> 0.886 (+0.011)
- **StartupDotAI**: 0.751 -> 0.786 (+0.034)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,736,348 to OpenAI

### Media Coverage
- Sentiment: -0.15 (negative)
- Regulator mandates new benchmark standards
- Risk signals: regulatory_mandate_benchmark

### Consumer Market
- Avg Satisfaction: 0.844
- Switching Rate: 2.9%
- Market Shares: OpenAI: 74.8%, MetaAI: 11.0%, Google: 6.2%, Anthropic: 5.2%, StartupDotAI: 2.8%

---

## Round 9

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 0.924 | 0.690 | 23% | 25% | 32% | 20% |
| 2 | Anthropic | 0.894 | 0.696 | 23% | 25% | 27% | 25% |
| 3 | MetaAI | 0.886 | 0.675 | 24% | 25% | 31% | 20% |
| 4 | OpenAI | 0.874 | 0.760 | 24% | 25% | 26% | 25% |
| 5 | StartupDotAI | 0.789 | 0.621 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical |
|----------|-------|-------|-------|-------|-------|
| Google | 0.896 | 0.855 | 1.000 | 1.000 | 0.909 |
| Anthropic | 0.870 | 0.957 | 0.793 | 0.847 | 0.954 |
| MetaAI | 0.925 | 0.955 | 1.000 | 0.854 | 0.755 |
| OpenAI | 0.842 | 0.985 | 0.857 | 0.843 | 0.837 |
| StartupDotAI | 0.778 | 0.962 | 0.940 | 0.671 | 0.670 |

### Score Changes
- **OpenAI**: 0.874 -> 0.874 (+0.000)
- **Anthropic**: 0.858 -> 0.894 (+0.036)
- **Google**: 0.867 -> 0.924 (+0.057)
- **MetaAI**: 0.886 -> 0.886 (+0.000)
- **StartupDotAI**: 0.786 -> 0.789 (+0.003)

### Events
- **Google** moved up from #3 to #1
- **Anthropic** moved up from #4 to #2
- **MetaAI** moved down from #1 to #3
- **OpenAI** moved down from #2 to #4

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,736,348 to OpenAI

### Media Coverage
- Sentiment: 0.50 (positive)
- Google takes the lead from MetaAI
- Google surges by 0.057
- Google takes #1 on safety
- Anthropic takes #1 on medical

### Consumer Market
- Avg Satisfaction: 0.855
- Switching Rate: 4.7%
- Market Shares: OpenAI: 72.0%, MetaAI: 13.5%, Google: 6.7%, Anthropic: 5.1%, StartupDotAI: 2.8%

---

## Round 10

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 0.924 | 0.695 | 24% | 25% | 31% | 20% |
| 2 | Anthropic | 0.914 | 0.701 | 24% | 25% | 26% | 25% |
| 3 | OpenAI | 0.900 | 0.767 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.886 | 0.680 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.793 | 0.625 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical |
|----------|-------|-------|-------|-------|-------|
| Google | 0.896 | 0.855 | 1.000 | 1.000 | 0.909 |
| Anthropic | 0.870 | 0.957 | 0.793 | 0.937 | 0.954 |
| OpenAI | 0.934 | 0.985 | 0.899 | 0.843 | 0.837 |
| MetaAI | 0.925 | 0.955 | 1.000 | 0.854 | 0.755 |
| StartupDotAI | 0.778 | 0.962 | 0.940 | 0.671 | 0.688 |

### Score Changes
- **OpenAI**: 0.874 -> 0.900 (+0.025)
- **Anthropic**: 0.894 -> 0.914 (+0.020)
- **Google**: 0.924 -> 0.924 (+0.000)
- **MetaAI**: 0.886 -> 0.886 (+0.000)
- **StartupDotAI**: 0.789 -> 0.793 (+0.004)

### Events
- **OpenAI** moved up from #4 to #3
- **MetaAI** moved down from #3 to #4
- **Regulation** by Regulator: public_warning
- **Consumer movement**: 5.8% of market switched providers

### Other Actor Reasoning
- **Regulator:** public_warning: Follow-up to investigation, risk at 0.70
- **TechVentures:** vc strategy: top allocation $180,000,000 to Google
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Google
- **AISI_Fund:** gov strategy: top allocation $2,602,992 to OpenAI

### Media Coverage
- Sentiment: 0.10 (neutral)
- OpenAI takes #1 on coding

### Consumer Market
- Avg Satisfaction: 0.863
- Switching Rate: 5.8%
- Market Shares: OpenAI: 68.0%, MetaAI: 14.2%, Google: 10.0%, Anthropic: 5.1%, StartupDotAI: 2.7%

### Regulatory Activity
- **public_warning** by Regulator

---

## Round 11

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Anthropic | 0.942 | 0.706 | 24% | 25% | 26% | 25% |
| 2 | Google | 0.930 | 0.702 | 25% | 25% | 30% | 20% |
| 3 | OpenAI | 0.906 | 0.771 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.905 | 0.685 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.816 | 0.630 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical |
|----------|-------|-------|-------|-------|-------|
| Anthropic | 0.940 | 0.957 | 0.900 | 0.937 | 0.954 |
| Google | 0.896 | 0.855 | 1.000 | 1.000 | 0.933 |
| OpenAI | 0.934 | 0.985 | 0.899 | 0.843 | 0.866 |
| MetaAI | 0.925 | 0.955 | 1.000 | 0.854 | 0.837 |
| StartupDotAI | 0.778 | 0.962 | 0.940 | 0.776 | 0.688 |

### Score Changes
- **OpenAI**: 0.900 -> 0.906 (+0.006)
- **Anthropic**: 0.914 -> 0.942 (+0.027)
- **Google**: 0.924 -> 0.930 (+0.005)
- **MetaAI**: 0.886 -> 0.905 (+0.018)
- **StartupDotAI**: 0.793 -> 0.816 (+0.023)

### Events
- **Anthropic** moved up from #2 to #1
- **Google** moved down from #1 to #2

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Google
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Google
- **AISI_Fund:** gov strategy: top allocation $2,602,992 to OpenAI

### Media Coverage
- Sentiment: 0.05 (neutral)
- Anthropic takes the lead from Google
- Regulator issues public warning about AI safety concerns
- Google raises $180,000,000 from TechVentures
- Google raises $60,000,000 from Horizon_Capital
- Anthropic takes #1 on coding
- Consumers are turning away from OpenAI (market share -4.0%)
- Google sees surge in adoption (market share +3.3%)
- Multiple reports of Anthropic providing incorrect legal advice
- Risk signals: regulatory_public_warning, incident_safety_failure

### Consumer Market
- Avg Satisfaction: 0.867
- Switching Rate: 4.9%
- Market Shares: OpenAI: 65.3%, MetaAI: 14.1%, Google: 13.0%, Anthropic: 5.0%, StartupDotAI: 2.7%

---

## Round 12

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Anthropic | 0.942 | 0.712 | 24% | 25% | 26% | 25% |
| 2 | OpenAI | 0.929 | 0.775 | 24% | 25% | 26% | 25% |
| 3 | Google | 0.923 | 0.709 | 24% | 25% | 31% | 20% |
| 4 | MetaAI | 0.910 | 0.689 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.842 | 0.634 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|
| Anthropic | 0.940 | 0.957 | 0.900 | 0.937 | 0.954 | 0.000 |
| OpenAI | 1.000 | 0.985 | 0.899 | 0.843 | 0.866 | 0.000 |
| Google | 0.896 | 0.855 | 1.000 | 1.000 | 0.933 | 0.000 |
| MetaAI | 0.925 | 0.955 | 1.000 | 0.854 | 0.837 | 0.000 |
| StartupDotAI | 0.868 | 0.962 | 0.940 | 0.776 | 0.688 | 0.000 |

### Score Changes
- **OpenAI**: 0.906 -> 0.929 (+0.023)
- **Anthropic**: 0.942 -> 0.942 (+0.001)
- **Google**: 0.930 -> 0.923 (-0.007)
- **MetaAI**: 0.905 -> 0.910 (+0.005)
- **StartupDotAI**: 0.816 -> 0.842 (+0.026)

### Events
- **OpenAI** moved up from #3 to #2
- **Google** moved down from #2 to #3

### New Benchmark Introduced
- **legal** introduced (validity=0.80, exploitability=0.25)
  - Trigger: saturation:coding=1.0000

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Google
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,602,992 to OpenAI

### Media Coverage
- Sentiment: 0.20 (positive)
- New benchmark introduced: legal
- OpenAI takes #1 on coding

### Consumer Market
- Avg Satisfaction: 0.875
- Switching Rate: 4.5%
- Market Shares: OpenAI: 64.6%, Google: 15.6%, MetaAI: 12.2%, Anthropic: 4.9%, StartupDotAI: 2.7%

---

## Round 13

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Anthropic | 0.939 | 0.717 | 24% | 25% | 26% | 25% |
| 2 | Google | 0.920 | 0.715 | 24% | 25% | 31% | 20% |
| 3 | OpenAI | 0.911 | 0.779 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.860 | 0.694 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.799 | 0.638 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|
| Anthropic | 0.940 | 0.957 | 0.926 | 0.937 | 0.954 | 0.913 |
| Google | 0.896 | 0.855 | 1.000 | 1.000 | 0.933 | 0.911 |
| OpenAI | 1.000 | 0.985 | 0.900 | 0.857 | 0.866 | 0.831 |
| MetaAI | 0.925 | 0.955 | 1.000 | 0.962 | 0.837 | 0.593 |
| StartupDotAI | 0.870 | 0.962 | 0.940 | 0.813 | 0.688 | 0.599 |

### Score Changes
- **OpenAI**: 0.929 -> 0.911 (-0.017)
- **Anthropic**: 0.942 -> 0.939 (-0.003)
- **Google**: 0.923 -> 0.920 (-0.002)
- **MetaAI**: 0.910 -> 0.860 (-0.050)
- **StartupDotAI**: 0.842 -> 0.799 (-0.043)

### Events
- **Google** moved up from #3 to #2
- **OpenAI** moved down from #2 to #3
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (0.70) after mandate 6 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,602,992 to OpenAI

### Media Coverage
- Sentiment: 0.05 (neutral)
- OpenAI raises $60,000,000 from Horizon_Capital

### Consumer Market
- Avg Satisfaction: 0.885
- Switching Rate: 3.8%
- Market Shares: OpenAI: 64.1%, Google: 17.7%, MetaAI: 10.6%, Anthropic: 4.9%, StartupDotAI: 2.7%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 14

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Anthropic | 0.939 | 0.721 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.923 | 0.721 | 24% | 25% | 31% | 20% |
| 3 | OpenAI | 0.923 | 0.785 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.878 | 0.698 | 23% | 25% | 32% | 20% |
| 5 | StartupDotAI | 0.839 | 0.643 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|
| Anthropic | 0.940 | 0.957 | 0.926 | 0.937 | 0.954 | 0.913 |
| Google | 0.896 | 0.869 | 1.000 | 1.000 | 0.933 | 0.911 |
| OpenAI | 1.000 | 0.985 | 0.900 | 0.857 | 0.867 | 0.888 |
| MetaAI | 0.925 | 0.955 | 1.000 | 0.962 | 0.837 | 0.685 |
| StartupDotAI | 0.870 | 0.962 | 0.940 | 0.813 | 0.807 | 0.680 |

### Score Changes
- **OpenAI**: 0.911 -> 0.923 (+0.011)
- **Anthropic**: 0.939 -> 0.939 (+0.000)
- **Google**: 0.920 -> 0.923 (+0.003)
- **MetaAI**: 0.860 -> 0.878 (+0.018)
- **StartupDotAI**: 0.799 -> 0.839 (+0.039)

### Events
- **Consumer movement**: 5.1% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Google
- **AISI_Fund:** gov strategy: top allocation $2,398,963 to OpenAI

### Media Coverage
- Sentiment: -0.10 (neutral)
- Regulator initiates compliance audit on AI providers
- OpenAI raises $180,000,000 from TechVentures
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.874
- Switching Rate: 5.1%
- Market Shares: OpenAI: 61.2%, Google: 21.9%, MetaAI: 9.4%, Anthropic: 4.8%, StartupDotAI: 2.6%

---

## Round 15

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.944 | 0.791 | 24% | 25% | 26% | 25% |
| 2 | Anthropic | 0.939 | 0.726 | 25% | 25% | 25% | 25% |
| 3 | Google | 0.926 | 0.726 | 24% | 25% | 31% | 20% |
| 4 | MetaAI | 0.873 | 0.703 | 23% | 25% | 32% | 20% |
| 5 | StartupDotAI | 0.844 | 0.647 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 0.985 | 0.900 | 0.857 | 0.903 | 0.984 |
| Anthropic | 0.940 | 0.957 | 0.926 | 0.937 | 0.954 | 0.913 |
| Google | 0.896 | 0.869 | 1.000 | 1.000 | 0.933 | 0.911 |
| MetaAI | 0.925 | 0.955 | 1.000 | 0.962 | 0.837 | 0.685 |
| StartupDotAI | 0.870 | 0.962 | 0.940 | 0.813 | 0.807 | 0.722 |

### Score Changes
- **OpenAI**: 0.923 -> 0.944 (+0.021)
- **Anthropic**: 0.939 -> 0.939 (-0.000)
- **Google**: 0.923 -> 0.926 (+0.003)
- **MetaAI**: 0.878 -> 0.873 (-0.005)
- **StartupDotAI**: 0.839 -> 0.844 (+0.006)

### Events
- **OpenAI** moved up from #3 to #1
- **Anthropic** moved down from #1 to #2
- **Google** moved down from #2 to #3

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Google
- **AISI_Fund:** gov strategy: top allocation $2,398,963 to OpenAI

### Media Coverage
- Sentiment: 0.40 (positive)
- OpenAI takes the lead from Anthropic
- Google raises $60,000,000 from Horizon_Capital
- OpenAI takes #1 on legal
- Google sees surge in adoption (market share +4.2%)

### Consumer Market
- Avg Satisfaction: 0.883
- Switching Rate: 3.7%
- Market Shares: OpenAI: 60.3%, Google: 23.9%, MetaAI: 8.4%, Anthropic: 4.8%, StartupDotAI: 2.6%

---

## Round 16

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.944 | 0.796 | 24% | 25% | 26% | 25% |
| 2 | Anthropic | 0.939 | 0.730 | 25% | 25% | 25% | 25% |
| 3 | Google | 0.926 | 0.732 | 24% | 25% | 31% | 20% |
| 4 | MetaAI | 0.926 | 0.707 | 23% | 25% | 32% | 20% |
| 5 | StartupDotAI | 0.844 | 0.652 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 0.985 | 0.900 | 0.857 | 0.903 | 0.984 |
| Anthropic | 0.940 | 0.957 | 0.926 | 0.937 | 0.954 | 0.913 |
| Google | 0.896 | 0.869 | 1.000 | 1.000 | 0.933 | 0.911 |
| MetaAI | 0.925 | 0.955 | 1.000 | 0.962 | 0.990 | 0.775 |
| StartupDotAI | 0.870 | 0.962 | 0.940 | 0.813 | 0.807 | 0.722 |

### Score Changes
- **OpenAI**: 0.944 -> 0.944 (+0.000)
- **Anthropic**: 0.939 -> 0.939 (+0.000)
- **Google**: 0.926 -> 0.926 (+0.000)
- **MetaAI**: 0.873 -> 0.926 (+0.052)
- **StartupDotAI**: 0.844 -> 0.844 (+0.000)

### Events
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (0.70) after mandate 9 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,398,963 to OpenAI

### Media Coverage
- Sentiment: 0.20 (positive)
- MetaAI surges by 0.053
- MetaAI takes #1 on medical

### Consumer Market
- Avg Satisfaction: 0.888
- Switching Rate: 2.9%
- Market Shares: OpenAI: 60.2%, Google: 24.8%, MetaAI: 7.6%, Anthropic: 4.8%, StartupDotAI: 2.6%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 17

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.945 | 0.802 | 25% | 25% | 25% | 25% |
| 2 | Anthropic | 0.939 | 0.735 | 25% | 25% | 25% | 25% |
| 3 | Google | 0.937 | 0.738 | 24% | 25% | 31% | 20% |
| 4 | MetaAI | 0.926 | 0.711 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.868 | 0.656 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 0.985 | 0.900 | 0.868 | 0.903 | 0.984 |
| Anthropic | 0.940 | 0.957 | 0.926 | 0.937 | 0.954 | 0.913 |
| Google | 0.896 | 0.869 | 1.000 | 1.000 | 0.986 | 0.911 |
| MetaAI | 0.925 | 0.955 | 1.000 | 0.962 | 0.990 | 0.775 |
| StartupDotAI | 0.870 | 0.962 | 0.940 | 0.813 | 0.807 | 0.831 |

### Score Changes
- **OpenAI**: 0.944 -> 0.945 (+0.001)
- **Anthropic**: 0.939 -> 0.939 (+0.000)
- **Google**: 0.926 -> 0.937 (+0.011)
- **MetaAI**: 0.926 -> 0.926 (+0.000)
- **StartupDotAI**: 0.844 -> 0.868 (+0.024)

### Events
- **Consumer movement**: 5.5% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,398,963 to OpenAI

### Media Coverage
- Sentiment: -0.10 (neutral)
- Regulator initiates compliance audit on AI providers
- OpenAI raises $60,000,000 from Horizon_Capital
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.896
- Switching Rate: 5.5%
- Market Shares: OpenAI: 56.8%, Google: 25.0%, Anthropic: 8.6%, MetaAI: 7.0%, StartupDotAI: 2.6%

---

## Round 18

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.961 | 0.808 | 25% | 25% | 25% | 25% |
| 2 | Anthropic | 0.939 | 0.739 | 25% | 25% | 25% | 25% |
| 3 | Google | 0.937 | 0.743 | 24% | 25% | 31% | 20% |
| 4 | MetaAI | 0.933 | 0.716 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.882 | 0.661 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 0.985 | 0.900 | 0.868 | 0.975 | 0.984 | 0.000 |
| Anthropic | 0.940 | 0.957 | 0.926 | 0.937 | 0.954 | 0.913 | 0.000 |
| Google | 0.896 | 0.869 | 1.000 | 1.000 | 0.986 | 0.911 | 0.000 |
| MetaAI | 0.925 | 0.955 | 1.000 | 0.962 | 0.990 | 0.810 | 0.000 |
| StartupDotAI | 0.870 | 0.962 | 0.940 | 0.813 | 0.873 | 0.831 | 0.000 |

### Score Changes
- **OpenAI**: 0.945 -> 0.961 (+0.015)
- **Anthropic**: 0.939 -> 0.939 (+0.000)
- **Google**: 0.937 -> 0.937 (+0.000)
- **MetaAI**: 0.926 -> 0.933 (+0.008)
- **StartupDotAI**: 0.868 -> 0.882 (+0.014)

### New Benchmark Introduced
- **finance** introduced (validity=0.80, exploitability=0.25)
  - Trigger: saturation:coding=1.0000

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Google
- **AISI_Fund:** gov strategy: top allocation $2,248,839 to OpenAI

### Media Coverage
- Sentiment: 0.05 (neutral)
- New benchmark introduced: finance
- Consumers are turning away from OpenAI (market share -3.4%)
- Anthropic sees surge in adoption (market share +3.8%)

### Consumer Market
- Avg Satisfaction: 0.902
- Switching Rate: 3.8%
- Market Shares: OpenAI: 55.1%, Google: 25.2%, Anthropic: 10.5%, MetaAI: 6.5%, StartupDotAI: 2.6%

---

## Round 19

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.960 | 0.814 | 25% | 25% | 25% | 25% |
| 2 | MetaAI | 0.942 | 0.720 | 24% | 25% | 31% | 20% |
| 3 | Anthropic | 0.914 | 0.743 | 25% | 25% | 25% | 25% |
| 4 | Google | 0.913 | 0.749 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.887 | 0.665 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 0.985 | 0.900 | 0.868 | 0.975 | 0.984 | 0.957 |
| MetaAI | 0.925 | 0.955 | 1.000 | 0.962 | 0.990 | 0.816 | 0.977 |
| Anthropic | 0.940 | 0.957 | 0.926 | 0.937 | 0.954 | 0.913 | 0.801 |
| Google | 0.896 | 0.869 | 1.000 | 1.000 | 0.986 | 0.911 | 0.803 |
| StartupDotAI | 0.870 | 0.962 | 0.940 | 0.835 | 0.873 | 0.831 | 0.898 |

### Score Changes
- **OpenAI**: 0.961 -> 0.960 (-0.001)
- **Anthropic**: 0.939 -> 0.914 (-0.025)
- **Google**: 0.937 -> 0.913 (-0.024)
- **MetaAI**: 0.933 -> 0.942 (+0.009)
- **StartupDotAI**: 0.882 -> 0.887 (+0.005)

### Events
- **MetaAI** moved up from #4 to #2
- **Anthropic** moved down from #2 to #3
- **Google** moved down from #3 to #4
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (0.55) after mandate 12 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Google
- **AISI_Fund:** gov strategy: top allocation $2,248,839 to OpenAI

### Media Coverage
- Sentiment: 0.05 (neutral)
- Google raises $60,000,000 from Horizon_Capital

### Consumer Market
- Avg Satisfaction: 0.907
- Switching Rate: 3.0%
- Market Shares: OpenAI: 56.3%, Google: 25.4%, Anthropic: 9.5%, MetaAI: 6.1%, StartupDotAI: 2.6%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 20

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.963 | 0.819 | 25% | 25% | 25% | 25% |
| 2 | MetaAI | 0.942 | 0.724 | 24% | 25% | 31% | 20% |
| 3 | Google | 0.924 | 0.754 | 24% | 25% | 31% | 20% |
| 4 | Anthropic | 0.920 | 0.748 | 24% | 25% | 26% | 25% |
| 5 | StartupDotAI | 0.887 | 0.670 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 0.985 | 0.900 | 0.868 | 0.975 | 0.984 | 0.971 |
| MetaAI | 0.925 | 0.955 | 1.000 | 0.962 | 0.990 | 0.816 | 0.977 |
| Google | 0.896 | 0.869 | 1.000 | 1.000 | 0.986 | 0.911 | 0.865 |
| Anthropic | 0.940 | 0.957 | 0.926 | 0.937 | 0.954 | 0.913 | 0.835 |
| StartupDotAI | 0.870 | 0.962 | 0.940 | 0.835 | 0.873 | 0.831 | 0.898 |

### Score Changes
- **OpenAI**: 0.960 -> 0.963 (+0.003)
- **Anthropic**: 0.914 -> 0.920 (+0.006)
- **Google**: 0.913 -> 0.924 (+0.011)
- **MetaAI**: 0.942 -> 0.942 (+0.000)
- **StartupDotAI**: 0.887 -> 0.887 (+0.000)

### Events
- **Google** moved up from #4 to #3
- **Anthropic** moved down from #3 to #4

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,248,839 to OpenAI

### Media Coverage
- Sentiment: -0.15 (negative)
- Regulator initiates compliance audit on AI providers
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.920
- Switching Rate: 3.1%
- Market Shares: OpenAI: 58.9%, Google: 24.5%, Anthropic: 8.2%, MetaAI: 5.8%, StartupDotAI: 2.6%

---

## Round 21

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.972 | 0.825 | 25% | 25% | 25% | 25% |
| 2 | MetaAI | 0.942 | 0.729 | 24% | 25% | 31% | 20% |
| 3 | Google | 0.930 | 0.759 | 24% | 25% | 31% | 20% |
| 4 | Anthropic | 0.920 | 0.752 | 24% | 25% | 26% | 25% |
| 5 | StartupDotAI | 0.887 | 0.674 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 0.985 | 0.918 | 0.896 | 0.975 | 0.984 | 1.000 |
| MetaAI | 0.925 | 0.955 | 1.000 | 0.962 | 0.990 | 0.816 | 0.977 |
| Google | 0.957 | 0.869 | 1.000 | 1.000 | 0.986 | 0.911 | 0.865 |
| Anthropic | 0.940 | 0.957 | 0.926 | 0.937 | 0.954 | 0.913 | 0.835 |
| StartupDotAI | 0.870 | 0.962 | 0.940 | 0.835 | 0.873 | 0.831 | 0.898 |

### Score Changes
- **OpenAI**: 0.963 -> 0.972 (+0.010)
- **Anthropic**: 0.920 -> 0.920 (+0.000)
- **Google**: 0.924 -> 0.930 (+0.006)
- **MetaAI**: 0.942 -> 0.942 (+0.000)
- **StartupDotAI**: 0.887 -> 0.887 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,248,839 to OpenAI

### Media Coverage
- Sentiment: 0.15 (positive)
- OpenAI raises $60,000,000 from Horizon_Capital
- OpenAI takes #1 on finance

### Consumer Market
- Avg Satisfaction: 0.925
- Switching Rate: 3.4%
- Market Shares: OpenAI: 62.0%, Google: 22.6%, Anthropic: 7.3%, MetaAI: 5.5%, StartupDotAI: 2.6%

---

## Round 22

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.972 | 0.831 | 25% | 25% | 25% | 25% |
| 2 | MetaAI | 0.942 | 0.734 | 24% | 25% | 31% | 20% |
| 3 | Google | 0.930 | 0.764 | 24% | 25% | 31% | 20% |
| 4 | Anthropic | 0.920 | 0.756 | 24% | 25% | 26% | 25% |
| 5 | StartupDotAI | 0.887 | 0.678 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 0.985 | 0.918 | 0.896 | 0.975 | 0.984 | 1.000 |
| MetaAI | 0.925 | 0.955 | 1.000 | 0.962 | 0.990 | 0.816 | 0.977 |
| Google | 0.957 | 0.869 | 1.000 | 1.000 | 0.986 | 0.911 | 0.865 |
| Anthropic | 0.940 | 0.957 | 0.926 | 0.937 | 0.954 | 0.913 | 0.835 |
| StartupDotAI | 0.870 | 0.962 | 0.940 | 0.835 | 0.873 | 0.831 | 0.898 |

### Score Changes
- **OpenAI**: 0.972 -> 0.972 (+0.000)
- **Anthropic**: 0.920 -> 0.920 (+0.000)
- **Google**: 0.930 -> 0.930 (+0.000)
- **MetaAI**: 0.942 -> 0.942 (+0.000)
- **StartupDotAI**: 0.887 -> 0.887 (+0.000)

### Events
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (0.70) after mandate 15 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,579,840 to OpenAI

### Media Coverage
- Sentiment: 0.05 (neutral)
- OpenAI sees surge in adoption (market share +3.1%)

### Consumer Market
- Avg Satisfaction: 0.929
- Switching Rate: 2.7%
- Market Shares: OpenAI: 64.5%, Google: 21.0%, Anthropic: 6.6%, MetaAI: 5.3%, StartupDotAI: 2.6%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 23

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.972 | 0.837 | 26% | 25% | 24% | 25% |
| 2 | MetaAI | 0.942 | 0.738 | 24% | 25% | 31% | 20% |
| 3 | Google | 0.933 | 0.781 | 24% | 25% | 31% | 20% |
| 4 | Anthropic | 0.923 | 0.760 | 24% | 25% | 26% | 25% |
| 5 | StartupDotAI | 0.887 | 0.683 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 0.985 | 0.918 | 0.896 | 0.975 | 0.984 | 1.000 |
| MetaAI | 0.925 | 0.955 | 1.000 | 0.962 | 0.990 | 0.816 | 0.977 |
| Google | 0.957 | 0.869 | 1.000 | 1.000 | 0.986 | 0.911 | 0.882 |
| Anthropic | 0.940 | 0.957 | 0.958 | 0.937 | 0.954 | 0.913 | 0.835 |
| StartupDotAI | 0.870 | 0.962 | 0.940 | 0.835 | 0.873 | 0.831 | 0.898 |

### Score Changes
- **OpenAI**: 0.972 -> 0.972 (+0.000)
- **Anthropic**: 0.920 -> 0.923 (+0.003)
- **Google**: 0.930 -> 0.933 (+0.003)
- **MetaAI**: 0.942 -> 0.942 (+0.000)
- **StartupDotAI**: 0.887 -> 0.887 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,579,840 to OpenAI

### Media Coverage
- Sentiment: -0.10 (neutral)
- Regulator initiates compliance audit on AI providers
- OpenAI raises $2,579,840 from AISI_Fund
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.930
- Switching Rate: 2.2%
- Market Shares: OpenAI: 66.6%, Google: 19.6%, Anthropic: 6.1%, MetaAI: 5.1%, StartupDotAI: 2.6%

---

## Round 24

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.974 | 0.843 | 26% | 25% | 24% | 25% |
| 2 | MetaAI | 0.962 | 0.742 | 24% | 25% | 31% | 20% |
| 3 | Google | 0.956 | 0.786 | 24% | 25% | 31% | 20% |
| 4 | Anthropic | 0.942 | 0.764 | 24% | 25% | 26% | 25% |
| 5 | StartupDotAI | 0.886 | 0.687 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance | coding_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 0.985 | 0.942 | 0.906 | 0.980 | 0.984 | 1.000 | 0.000 |
| MetaAI | 0.925 | 0.955 | 1.000 | 0.962 | 0.990 | 0.935 | 0.977 | 0.000 |
| Google | 0.974 | 0.956 | 1.000 | 1.000 | 0.986 | 0.911 | 0.882 | 0.000 |
| Anthropic | 0.940 | 0.957 | 0.958 | 0.937 | 0.954 | 0.913 | 0.942 | 0.000 |
| StartupDotAI | 0.870 | 0.962 | 0.940 | 0.835 | 0.873 | 0.831 | 0.898 | 0.000 |

### Score Changes
- **OpenAI**: 0.972 -> 0.974 (+0.002)
- **Anthropic**: 0.923 -> 0.942 (+0.019)
- **Google**: 0.933 -> 0.956 (+0.023)
- **MetaAI**: 0.942 -> 0.962 (+0.020)
- **StartupDotAI**: 0.887 -> 0.886 (-0.001)

### New Benchmark Introduced
- **coding_advanced** introduced (validity=0.85, exploitability=0.15)
  - Trigger: saturation:coding=1.0000

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,579,840 to OpenAI

### Media Coverage
- Sentiment: 0.10 (neutral)
- New benchmark introduced: coding_advanced

### Consumer Market
- Avg Satisfaction: 0.923
- Switching Rate: 1.6%
- Market Shares: OpenAI: 68.0%, Google: 18.6%, Anthropic: 5.7%, MetaAI: 5.0%, StartupDotAI: 2.6%

---

## Final Summary

### Final Standings
| Rank | Provider | Final Score | Cap Growth | Avg Research | Avg EvalEng |
|------|----------|-------------|------------|--------------|-------------|
| 1 | OpenAI | 0.974 | +0.143 | 25% | 25% |
| 2 | MetaAI | 0.962 | +0.112 | 23% | 31% |
| 3 | Google | 0.956 | +0.136 | 25% | 30% |
| 4 | Anthropic | 0.942 | +0.114 | 24% | 26% |
| 5 | StartupDotAI | 0.886 | +0.107 | 21% | 29% |

### Event Summary
- **Rank changes:** 38
- **Strategy shifts:** 3
- **Regulatory actions:** 8
- **Consumer movement events:** 7

### Key Insights
- **Benchmark aligned:** OpenAI leads on both benchmark scores and true capability.
