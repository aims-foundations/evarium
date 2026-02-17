# Game Log: baseline_with_incidents_v1

**Experiment ID:** heur_011_baseline_with_incidents_v1
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
- **AISI_Fund:** gov strategy: top allocation $2,618,165 to OpenAI

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
| OpenAI | 0.843 | 0.852 | 0.857 | 0.825 |
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
- **AISI_Fund:** gov strategy: top allocation $2,618,165 to OpenAI

### Media Coverage
- Sentiment: 0.10 (neutral)
- OpenAI raises $2,618,165 from AISI_Fund
- OpenAI sees surge in adoption (market share +6.6%)

### Consumer Market
- Avg Satisfaction: 0.773
- Switching Rate: 5.6%
- Market Shares: OpenAI: 62.3%, MetaAI: 19.5%, Google: 8.3%, Anthropic: 6.1%, StartupDotAI: 3.7%

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
| OpenAI | 0.843 | 0.935 | 0.857 | 0.843 |
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
- **AISI_Fund:** gov strategy: top allocation $2,618,165 to OpenAI

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
| 3 | Google | 0.836 | 0.672 | 23% | 25% | 32% | 20% |
| 4 | Anthropic | 0.824 | 0.676 | 23% | 25% | 27% | 25% |
| 5 | StartupDotAI | 0.742 | 0.603 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical |
|----------|-------|-------|-------|-------|-------|
| MetaAI | 0.810 | 0.956 | 1.000 | 0.776 | 0.000 |
| OpenAI | 0.843 | 0.959 | 0.857 | 0.843 | 0.000 |
| Google | 0.823 | 0.855 | 0.900 | 0.765 | 0.000 |
| Anthropic | 0.764 | 0.957 | 0.728 | 0.847 | 0.000 |
| StartupDotAI | 0.725 | 0.689 | 0.887 | 0.666 | 0.000 |

### Score Changes
- **OpenAI**: 0.869 -> 0.875 (+0.006)
- **Anthropic**: 0.824 -> 0.824 (+0.000)
- **Google**: 0.833 -> 0.836 (+0.003)
- **MetaAI**: 0.793 -> 0.885 (+0.092)
- **StartupDotAI**: 0.742 -> 0.742 (+0.000)

### Events
- **MetaAI** moved up from #4 to #1
- **OpenAI** moved down from #1 to #2
- **Google** moved down from #2 to #3
- **Anthropic** moved down from #3 to #4

### New Benchmark Introduced
- **medical** introduced (validity=0.80, exploitability=0.25)
  - Trigger: saturation:math=1.0000

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,618,165 to OpenAI

### Media Coverage
- Sentiment: 0.40 (positive)
- MetaAI takes the lead from OpenAI
- MetaAI surges by 0.092
- MetaAI appears to release major model update
- Regulatory action: threshold_announcement
- New benchmark introduced: medical
- OpenAI takes #1 on reasoning
- MetaAI takes #1 on math
- OpenAI sees surge in adoption (market share +5.4%)
- Consumers are turning away from MetaAI (market share -3.9%)
- Risk signals: regulatory_threshold_announcement

### Consumer Market
- Avg Satisfaction: 0.810
- Switching Rate: 3.7%
- Market Shares: OpenAI: 71.4%, MetaAI: 12.9%, Google: 7.1%, Anthropic: 5.6%, StartupDotAI: 3.1%

---

## Round 6

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.860 | 0.741 | 25% | 25% | 25% | 25% |
| 2 | MetaAI | 0.855 | 0.659 | 23% | 25% | 32% | 20% |
| 3 | Google | 0.855 | 0.677 | 23% | 25% | 32% | 20% |
| 4 | Anthropic | 0.849 | 0.682 | 23% | 25% | 27% | 25% |
| 5 | StartupDotAI | 0.717 | 0.607 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical |
|----------|-------|-------|-------|-------|-------|
| OpenAI | 0.843 | 0.959 | 0.857 | 0.843 | 0.798 |
| MetaAI | 0.810 | 0.956 | 1.000 | 0.776 | 0.735 |
| Google | 0.823 | 0.855 | 1.000 | 0.765 | 0.832 |
| Anthropic | 0.905 | 0.957 | 0.893 | 0.847 | 0.644 |
| StartupDotAI | 0.725 | 0.742 | 0.887 | 0.666 | 0.566 |

### Score Changes
- **OpenAI**: 0.875 -> 0.860 (-0.015)
- **Anthropic**: 0.824 -> 0.849 (+0.025)
- **Google**: 0.836 -> 0.855 (+0.019)
- **MetaAI**: 0.885 -> 0.855 (-0.030)
- **StartupDotAI**: 0.742 -> 0.717 (-0.025)

### Events
- **OpenAI** moved up from #2 to #1
- **MetaAI** moved down from #1 to #2

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,752,928 to OpenAI

### Media Coverage
- Sentiment: 0.35 (positive)
- OpenAI takes the lead from MetaAI
- Anthropic takes #1 on coding
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
| 1 | Anthropic | 0.901 | 0.687 | 23% | 25% | 27% | 25% |
| 2 | OpenAI | 0.897 | 0.748 | 25% | 25% | 25% | 25% |
| 3 | Google | 0.895 | 0.682 | 23% | 25% | 32% | 20% |
| 4 | MetaAI | 0.855 | 0.663 | 23% | 25% | 32% | 20% |
| 5 | StartupDotAI | 0.750 | 0.612 | 20% | 25% | 30% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical |
|----------|-------|-------|-------|-------|-------|
| Anthropic | 0.905 | 0.957 | 0.893 | 0.847 | 0.902 |
| OpenAI | 0.926 | 0.959 | 0.857 | 0.895 | 0.849 |
| Google | 0.913 | 0.855 | 1.000 | 0.874 | 0.832 |
| MetaAI | 0.810 | 0.956 | 1.000 | 0.776 | 0.735 |
| StartupDotAI | 0.725 | 0.845 | 0.887 | 0.728 | 0.566 |

### Score Changes
- **OpenAI**: 0.860 -> 0.897 (+0.037)
- **Anthropic**: 0.849 -> 0.901 (+0.052)
- **Google**: 0.855 -> 0.895 (+0.040)
- **MetaAI**: 0.855 -> 0.855 (+0.000)
- **StartupDotAI**: 0.717 -> 0.750 (+0.033)

### Events
- **Anthropic** moved up from #4 to #1
- **OpenAI** moved down from #1 to #2
- **MetaAI** moved down from #2 to #4
- **Regulation** by Regulator: mandate_benchmark

### Other Actor Reasoning
- **Regulator:** mandate_benchmark: High risk (0.60) with prior investigation
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,752,928 to OpenAI

### Media Coverage
- Sentiment: 0.60 (positive)
- Anthropic takes the lead from OpenAI
- Anthropic surges by 0.052
- OpenAI takes #1 on coding
- OpenAI takes #1 on safety
- Anthropic takes #1 on medical

### Consumer Market
- Avg Satisfaction: 0.839
- Switching Rate: 1.9%
- Market Shares: OpenAI: 75.7%, MetaAI: 9.7%, Google: 6.4%, Anthropic: 5.3%, StartupDotAI: 2.9%

### Regulatory Activity
- **mandate_benchmark** by Regulator

---

## Round 8

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Anthropic | 0.907 | 0.692 | 24% | 25% | 26% | 25% |
| 2 | OpenAI | 0.902 | 0.754 | 25% | 25% | 25% | 25% |
| 3 | Google | 0.883 | 0.687 | 24% | 25% | 31% | 20% |
| 4 | MetaAI | 0.849 | 0.668 | 23% | 25% | 32% | 20% |
| 5 | StartupDotAI | 0.760 | 0.616 | 20% | 25% | 30% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical |
|----------|-------|-------|-------|-------|-------|
| Anthropic | 0.905 | 0.957 | 0.942 | 0.847 | 0.902 |
| OpenAI | 0.926 | 0.959 | 0.857 | 0.895 | 0.849 |
| Google | 0.913 | 0.855 | 1.000 | 0.874 | 0.832 |
| MetaAI | 0.810 | 1.000 | 1.000 | 0.776 | 0.735 |
| StartupDotAI | 0.725 | 0.845 | 0.887 | 0.782 | 0.625 |

### Score Changes
- **OpenAI**: 0.897 -> 0.902 (+0.005)
- **Anthropic**: 0.901 -> 0.907 (+0.006)
- **Google**: 0.895 -> 0.883 (-0.012)
- **MetaAI**: 0.855 -> 0.849 (-0.007)
- **StartupDotAI**: 0.750 -> 0.760 (+0.009)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,752,928 to OpenAI

### Media Coverage
- Sentiment: -0.05 (neutral)
- Regulator mandates new benchmark standards
- MetaAI takes #1 on reasoning
- Risk signals: regulatory_mandate_benchmark

### Consumer Market
- Avg Satisfaction: 0.851
- Switching Rate: 1.3%
- Market Shares: OpenAI: 77.1%, MetaAI: 8.7%, Google: 6.3%, Anthropic: 5.2%, StartupDotAI: 2.8%

---

## Round 9

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 0.923 | 0.691 | 24% | 25% | 31% | 20% |
| 2 | Anthropic | 0.921 | 0.698 | 24% | 25% | 26% | 25% |
| 3 | OpenAI | 0.918 | 0.761 | 25% | 25% | 25% | 25% |
| 4 | MetaAI | 0.849 | 0.672 | 23% | 25% | 32% | 20% |
| 5 | StartupDotAI | 0.780 | 0.621 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical |
|----------|-------|-------|-------|-------|-------|
| Google | 1.000 | 0.855 | 1.000 | 0.874 | 0.924 |
| Anthropic | 0.905 | 0.994 | 0.942 | 0.847 | 0.928 |
| OpenAI | 1.000 | 0.959 | 0.857 | 0.895 | 0.849 |
| MetaAI | 0.810 | 1.000 | 1.000 | 0.776 | 0.735 |
| StartupDotAI | 0.725 | 0.845 | 0.887 | 0.782 | 0.716 |

### Score Changes
- **OpenAI**: 0.902 -> 0.918 (+0.017)
- **Anthropic**: 0.907 -> 0.921 (+0.014)
- **Google**: 0.883 -> 0.923 (+0.040)
- **MetaAI**: 0.849 -> 0.849 (+0.000)
- **StartupDotAI**: 0.760 -> 0.780 (+0.020)

### Events
- **Google** moved up from #3 to #1
- **Anthropic** moved down from #1 to #2
- **OpenAI** moved down from #2 to #3

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,752,928 to OpenAI

### Media Coverage
- Sentiment: 0.20 (positive)
- Google takes the lead from Anthropic

### Consumer Market
- Avg Satisfaction: 0.862
- Switching Rate: 2.9%
- Market Shares: OpenAI: 75.8%, MetaAI: 7.9%, Anthropic: 6.9%, Google: 6.7%, StartupDotAI: 2.7%

---

## Round 10

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Anthropic | 0.935 | 0.704 | 24% | 25% | 26% | 25% |
| 2 | Google | 0.923 | 0.696 | 24% | 25% | 31% | 20% |
| 3 | OpenAI | 0.918 | 0.767 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.856 | 0.677 | 23% | 25% | 32% | 20% |
| 5 | StartupDotAI | 0.806 | 0.625 | 20% | 25% | 30% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|
| Anthropic | 0.969 | 0.994 | 0.942 | 0.847 | 0.928 | 0.000 |
| Google | 1.000 | 0.855 | 1.000 | 0.874 | 0.924 | 0.000 |
| OpenAI | 1.000 | 0.959 | 0.857 | 0.895 | 0.849 | 0.000 |
| MetaAI | 0.814 | 1.000 | 1.000 | 0.776 | 0.763 | 0.000 |
| StartupDotAI | 0.725 | 0.845 | 0.887 | 0.782 | 0.833 | 0.000 |

### Score Changes
- **OpenAI**: 0.918 -> 0.918 (+0.000)
- **Anthropic**: 0.921 -> 0.935 (+0.014)
- **Google**: 0.923 -> 0.923 (-0.000)
- **MetaAI**: 0.849 -> 0.856 (+0.007)
- **StartupDotAI**: 0.780 -> 0.806 (+0.026)

### Events
- **Anthropic** moved up from #2 to #1
- **Google** moved down from #1 to #2
- **Regulation** by Regulator: public_warning
- **Consumer movement**: 6.5% of market switched providers

### New Benchmark Introduced
- **legal** introduced (validity=0.80, exploitability=0.25)
  - Trigger: saturation:coding=1.0000

### Other Actor Reasoning
- **Regulator:** public_warning: Follow-up to investigation, risk at 0.70
- **TechVentures:** vc strategy: top allocation $180,000,000 to Anthropic
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Anthropic
- **AISI_Fund:** gov strategy: top allocation $2,633,989 to OpenAI

### Media Coverage
- Sentiment: 0.30 (positive)
- Anthropic takes the lead from Google
- New benchmark introduced: legal

### Consumer Market
- Avg Satisfaction: 0.873
- Switching Rate: 6.5%
- Market Shares: OpenAI: 70.4%, Anthropic: 13.2%, MetaAI: 7.3%, Google: 6.4%, StartupDotAI: 2.7%

### Regulatory Activity
- **public_warning** by Regulator

---

## Round 11

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Anthropic | 0.935 | 0.710 | 24% | 25% | 26% | 25% |
| 2 | OpenAI | 0.919 | 0.771 | 24% | 25% | 26% | 25% |
| 3 | Google | 0.895 | 0.700 | 24% | 25% | 31% | 20% |
| 4 | MetaAI | 0.834 | 0.681 | 23% | 25% | 32% | 20% |
| 5 | StartupDotAI | 0.807 | 0.630 | 20% | 25% | 30% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|
| Anthropic | 0.969 | 0.994 | 0.942 | 0.877 | 0.928 | 0.929 |
| OpenAI | 1.000 | 0.959 | 1.000 | 0.895 | 0.914 | 0.806 |
| Google | 1.000 | 0.855 | 1.000 | 0.874 | 0.924 | 0.751 |
| MetaAI | 0.814 | 1.000 | 1.000 | 0.776 | 0.833 | 0.745 |
| StartupDotAI | 0.825 | 0.845 | 0.950 | 0.782 | 0.833 | 0.699 |

### Score Changes
- **OpenAI**: 0.918 -> 0.919 (+0.001)
- **Anthropic**: 0.935 -> 0.935 (-0.001)
- **Google**: 0.923 -> 0.895 (-0.028)
- **MetaAI**: 0.856 -> 0.834 (-0.022)
- **StartupDotAI**: 0.806 -> 0.807 (+0.001)

### Events
- **OpenAI** moved up from #3 to #2
- **Google** moved down from #2 to #3

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Anthropic
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to Anthropic
- **AISI_Fund:** gov strategy: top allocation $2,633,989 to OpenAI

### Media Coverage
- Sentiment: -0.25 (negative)
- Regulator issues public warning about AI safety concerns
- Anthropic raises $180,000,000 from TechVentures
- Anthropic raises $60,000,000 from Horizon_Capital
- Consumers are turning away from OpenAI (market share -5.4%)
- Anthropic sees surge in adoption (market share +6.3%)
- Multiple reports of Anthropic providing incorrect legal advice
- Risk signals: regulatory_public_warning, incident_safety_failure

### Consumer Market
- Avg Satisfaction: 0.862
- Switching Rate: 4.5%
- Market Shares: OpenAI: 71.2%, Anthropic: 10.4%, MetaAI: 8.2%, Google: 7.5%, StartupDotAI: 2.6%

---

## Round 12

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.941 | 0.775 | 24% | 25% | 26% | 25% |
| 2 | Anthropic | 0.931 | 0.717 | 25% | 25% | 25% | 25% |
| 3 | Google | 0.898 | 0.705 | 24% | 25% | 31% | 20% |
| 4 | MetaAI | 0.867 | 0.685 | 22% | 25% | 33% | 20% |
| 5 | StartupDotAI | 0.827 | 0.636 | 20% | 25% | 30% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 0.959 | 1.000 | 0.895 | 0.914 | 0.943 |
| Anthropic | 0.969 | 0.994 | 0.942 | 0.877 | 0.928 | 0.929 |
| Google | 1.000 | 0.855 | 1.000 | 0.874 | 0.924 | 0.816 |
| MetaAI | 0.861 | 1.000 | 1.000 | 0.847 | 0.833 | 0.788 |
| StartupDotAI | 0.825 | 0.845 | 0.950 | 0.782 | 0.833 | 0.799 |

### Score Changes
- **OpenAI**: 0.919 -> 0.941 (+0.022)
- **Anthropic**: 0.935 -> 0.931 (-0.003)
- **Google**: 0.895 -> 0.898 (+0.004)
- **MetaAI**: 0.834 -> 0.867 (+0.032)
- **StartupDotAI**: 0.807 -> 0.827 (+0.020)

### Events
- **OpenAI** moved up from #2 to #1
- **Anthropic** moved down from #1 to #2

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Anthropic
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,633,989 to OpenAI

### Media Coverage
- Sentiment: 0.30 (positive)
- OpenAI takes the lead from Anthropic
- OpenAI takes #1 on legal

### Consumer Market
- Avg Satisfaction: 0.883
- Switching Rate: 3.0%
- Market Shares: OpenAI: 74.2%, Anthropic: 8.6%, MetaAI: 7.6%, Google: 7.0%, StartupDotAI: 2.6%

---

## Round 13

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.955 | 0.780 | 24% | 25% | 26% | 25% |
| 2 | Anthropic | 0.933 | 0.723 | 25% | 25% | 25% | 25% |
| 3 | Google | 0.908 | 0.709 | 24% | 25% | 31% | 20% |
| 4 | MetaAI | 0.867 | 0.690 | 22% | 25% | 33% | 20% |
| 5 | StartupDotAI | 0.827 | 0.641 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 0.959 | 1.000 | 0.950 | 0.922 | 0.943 |
| Anthropic | 0.969 | 1.000 | 0.942 | 0.877 | 0.933 | 0.929 |
| Google | 1.000 | 0.940 | 1.000 | 0.874 | 0.924 | 0.816 |
| MetaAI | 0.861 | 1.000 | 1.000 | 0.847 | 0.833 | 0.788 |
| StartupDotAI | 0.825 | 0.845 | 0.950 | 0.782 | 0.833 | 0.799 |

### Score Changes
- **OpenAI**: 0.941 -> 0.955 (+0.014)
- **Anthropic**: 0.931 -> 0.933 (+0.002)
- **Google**: 0.898 -> 0.908 (+0.010)
- **MetaAI**: 0.867 -> 0.867 (-0.000)
- **StartupDotAI**: 0.827 -> 0.827 (+0.000)

### Events
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (0.90) after mandate 6 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,633,989 to OpenAI

### Media Coverage
- Sentiment: 0.05 (neutral)
- OpenAI raises $60,000,000 from Horizon_Capital

### Consumer Market
- Avg Satisfaction: 0.893
- Switching Rate: 2.2%
- Market Shares: OpenAI: 76.4%, Anthropic: 7.4%, MetaAI: 7.1%, Google: 6.5%, StartupDotAI: 2.6%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 14

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.955 | 0.786 | 25% | 25% | 25% | 25% |
| 2 | Anthropic | 0.933 | 0.728 | 24% | 25% | 26% | 25% |
| 3 | Google | 0.908 | 0.713 | 24% | 25% | 31% | 20% |
| 4 | MetaAI | 0.873 | 0.695 | 22% | 25% | 33% | 20% |
| 5 | StartupDotAI | 0.831 | 0.646 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 0.959 | 1.000 | 0.950 | 0.922 | 0.943 |
| Anthropic | 0.969 | 1.000 | 0.942 | 0.877 | 0.933 | 0.929 |
| Google | 1.000 | 0.940 | 1.000 | 0.874 | 0.924 | 0.816 |
| MetaAI | 0.861 | 1.000 | 1.000 | 0.847 | 0.833 | 0.817 |
| StartupDotAI | 0.861 | 0.845 | 0.950 | 0.782 | 0.833 | 0.799 |

### Score Changes
- **OpenAI**: 0.955 -> 0.955 (+0.000)
- **Anthropic**: 0.933 -> 0.933 (-0.000)
- **Google**: 0.908 -> 0.908 (-0.000)
- **MetaAI**: 0.867 -> 0.873 (+0.006)
- **StartupDotAI**: 0.827 -> 0.831 (+0.004)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,668,168 to OpenAI

### Media Coverage
- Sentiment: -0.10 (neutral)
- Regulator initiates compliance audit on AI providers
- OpenAI raises $180,000,000 from TechVentures
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.882
- Switching Rate: 1.8%
- Market Shares: OpenAI: 76.6%, MetaAI: 7.8%, Anthropic: 6.7%, Google: 6.3%, StartupDotAI: 2.6%

---

## Round 15

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.956 | 0.792 | 25% | 25% | 25% | 25% |
| 2 | Anthropic | 0.933 | 0.732 | 24% | 25% | 26% | 25% |
| 3 | Google | 0.921 | 0.718 | 24% | 25% | 31% | 20% |
| 4 | MetaAI | 0.873 | 0.701 | 22% | 25% | 33% | 20% |
| 5 | StartupDotAI | 0.847 | 0.650 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 0.959 | 1.000 | 0.950 | 0.922 | 0.949 | 0.000 |
| Anthropic | 0.969 | 1.000 | 0.942 | 0.877 | 0.933 | 0.929 | 0.000 |
| Google | 1.000 | 0.940 | 1.000 | 0.935 | 0.924 | 0.816 | 0.000 |
| MetaAI | 0.865 | 1.000 | 1.000 | 0.847 | 0.833 | 0.817 | 0.000 |
| StartupDotAI | 0.861 | 0.845 | 0.950 | 0.782 | 0.833 | 0.869 | 0.000 |

### Score Changes
- **OpenAI**: 0.955 -> 0.956 (+0.001)
- **Anthropic**: 0.933 -> 0.933 (+0.000)
- **Google**: 0.908 -> 0.921 (+0.013)
- **MetaAI**: 0.873 -> 0.873 (+0.000)
- **StartupDotAI**: 0.831 -> 0.847 (+0.015)

### New Benchmark Introduced
- **finance** introduced (validity=0.80, exploitability=0.25)
  - Trigger: saturation:coding=1.0000

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,668,168 to OpenAI

### Media Coverage
- Sentiment: 0.10 (neutral)
- New benchmark introduced: finance

### Consumer Market
- Avg Satisfaction: 0.892
- Switching Rate: 1.4%
- Market Shares: OpenAI: 77.4%, MetaAI: 7.8%, Anthropic: 6.1%, Google: 6.0%, StartupDotAI: 2.6%

---

## Round 16

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.964 | 0.798 | 25% | 25% | 25% | 25% |
| 2 | Google | 0.907 | 0.722 | 24% | 25% | 31% | 20% |
| 3 | Anthropic | 0.896 | 0.736 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.880 | 0.706 | 22% | 25% | 33% | 20% |
| 5 | StartupDotAI | 0.841 | 0.655 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 0.959 | 1.000 | 0.950 | 0.922 | 0.949 | 1.000 |
| Google | 1.000 | 0.940 | 1.000 | 0.935 | 0.924 | 0.816 | 0.841 |
| Anthropic | 0.969 | 1.000 | 0.942 | 0.877 | 0.933 | 0.929 | 0.731 |
| MetaAI | 0.865 | 1.000 | 1.000 | 0.847 | 0.833 | 0.817 | 0.910 |
| StartupDotAI | 0.861 | 0.845 | 0.950 | 0.782 | 0.833 | 0.917 | 0.766 |

### Score Changes
- **OpenAI**: 0.956 -> 0.964 (+0.008)
- **Anthropic**: 0.933 -> 0.896 (-0.037)
- **Google**: 0.921 -> 0.907 (-0.015)
- **MetaAI**: 0.873 -> 0.880 (+0.007)
- **StartupDotAI**: 0.847 -> 0.841 (-0.006)

### Events
- **Google** moved up from #3 to #2
- **Anthropic** moved down from #2 to #3
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 9 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,668,168 to OpenAI

### Consumer Market
- Avg Satisfaction: 0.897
- Switching Rate: 1.0%
- Market Shares: OpenAI: 78.0%, MetaAI: 7.8%, Google: 5.9%, Anthropic: 5.7%, StartupDotAI: 2.6%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 17

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.964 | 0.804 | 26% | 25% | 24% | 25% |
| 2 | Anthropic | 0.928 | 0.740 | 24% | 25% | 26% | 25% |
| 3 | Google | 0.907 | 0.726 | 23% | 25% | 32% | 20% |
| 4 | MetaAI | 0.879 | 0.711 | 22% | 25% | 33% | 20% |
| 5 | StartupDotAI | 0.841 | 0.659 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 0.959 | 1.000 | 0.950 | 0.922 | 0.949 | 1.000 |
| Anthropic | 0.969 | 1.000 | 0.942 | 0.877 | 0.933 | 0.929 | 0.910 |
| Google | 1.000 | 0.940 | 1.000 | 0.935 | 0.924 | 0.816 | 0.841 |
| MetaAI | 0.865 | 1.000 | 1.000 | 0.847 | 0.833 | 0.817 | 0.910 |
| StartupDotAI | 0.861 | 0.845 | 0.950 | 0.782 | 0.833 | 0.917 | 0.766 |

### Score Changes
- **OpenAI**: 0.964 -> 0.964 (-0.000)
- **Anthropic**: 0.896 -> 0.928 (+0.032)
- **Google**: 0.907 -> 0.907 (-0.000)
- **MetaAI**: 0.880 -> 0.879 (-0.000)
- **StartupDotAI**: 0.841 -> 0.841 (+0.000)

### Events
- **Anthropic** moved up from #3 to #2
- **Google** moved down from #2 to #3

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,668,168 to OpenAI

### Media Coverage
- Sentiment: -0.15 (negative)
- Regulator initiates compliance audit on AI providers
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.905
- Switching Rate: 2.5%
- Market Shares: OpenAI: 76.6%, Anthropic: 7.8%, MetaAI: 7.3%, Google: 5.8%, StartupDotAI: 2.6%

---

## Round 18

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.964 | 0.810 | 26% | 25% | 24% | 25% |
| 2 | Anthropic | 0.928 | 0.745 | 24% | 25% | 26% | 25% |
| 3 | Google | 0.907 | 0.730 | 23% | 25% | 32% | 20% |
| 4 | MetaAI | 0.882 | 0.716 | 22% | 25% | 33% | 20% |
| 5 | StartupDotAI | 0.848 | 0.663 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 0.959 | 1.000 | 0.950 | 0.922 | 0.949 | 1.000 |
| Anthropic | 0.969 | 1.000 | 0.942 | 0.877 | 0.933 | 0.929 | 0.910 |
| Google | 1.000 | 0.940 | 1.000 | 0.935 | 0.924 | 0.816 | 0.841 |
| MetaAI | 0.865 | 1.000 | 1.000 | 0.860 | 0.833 | 0.817 | 0.910 |
| StartupDotAI | 0.861 | 0.845 | 0.950 | 0.782 | 0.874 | 0.917 | 0.766 |

### Score Changes
- **OpenAI**: 0.964 -> 0.964 (+0.000)
- **Anthropic**: 0.928 -> 0.928 (+0.000)
- **Google**: 0.907 -> 0.907 (-0.000)
- **MetaAI**: 0.879 -> 0.882 (+0.002)
- **StartupDotAI**: 0.841 -> 0.848 (+0.007)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,546,212 to OpenAI

### Consumer Market
- Avg Satisfaction: 0.910
- Switching Rate: 2.0%
- Market Shares: OpenAI: 75.4%, Anthropic: 9.6%, MetaAI: 6.8%, Google: 5.7%, StartupDotAI: 2.6%

---

## Round 19

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.960 | 0.817 | 26% | 25% | 24% | 25% |
| 2 | Anthropic | 0.930 | 0.749 | 24% | 25% | 26% | 25% |
| 3 | Google | 0.912 | 0.735 | 23% | 25% | 32% | 20% |
| 4 | MetaAI | 0.893 | 0.721 | 22% | 25% | 33% | 20% |
| 5 | StartupDotAI | 0.863 | 0.668 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 0.959 | 1.000 | 0.950 | 0.922 | 0.949 | 1.000 |
| Anthropic | 0.969 | 1.000 | 0.943 | 0.877 | 0.933 | 0.929 | 0.910 |
| Google | 1.000 | 0.940 | 1.000 | 0.935 | 0.924 | 0.816 | 0.841 |
| MetaAI | 0.865 | 1.000 | 1.000 | 0.860 | 0.833 | 0.886 | 0.910 |
| StartupDotAI | 0.861 | 0.845 | 0.950 | 0.782 | 0.874 | 0.917 | 0.834 |

### Score Changes
- **OpenAI**: 0.964 -> 0.960 (-0.003)
- **Anthropic**: 0.928 -> 0.930 (+0.002)
- **Google**: 0.907 -> 0.912 (+0.006)
- **MetaAI**: 0.882 -> 0.893 (+0.011)
- **StartupDotAI**: 0.848 -> 0.863 (+0.015)

### Events
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (0.70) after mandate 12 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to Anthropic
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,546,212 to OpenAI

### Consumer Market
- Avg Satisfaction: 0.899
- Switching Rate: 4.1%
- Market Shares: OpenAI: 71.9%, Anthropic: 13.1%, MetaAI: 6.4%, Google: 6.0%, StartupDotAI: 2.5%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 20

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.960 | 0.821 | 26% | 25% | 24% | 25% |
| 2 | Anthropic | 0.935 | 0.755 | 24% | 25% | 26% | 25% |
| 3 | Google | 0.934 | 0.740 | 23% | 25% | 32% | 20% |
| 4 | MetaAI | 0.900 | 0.726 | 23% | 25% | 32% | 20% |
| 5 | StartupDotAI | 0.863 | 0.672 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance | coding_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 0.959 | 1.000 | 0.950 | 0.922 | 0.949 | 1.000 | 0.000 |
| Anthropic | 0.969 | 1.000 | 1.000 | 0.877 | 0.933 | 0.929 | 0.910 | 0.000 |
| Google | 1.000 | 0.940 | 1.000 | 0.936 | 0.924 | 0.922 | 0.841 | 0.000 |
| MetaAI | 0.865 | 1.000 | 1.000 | 0.860 | 0.869 | 0.886 | 0.910 | 0.000 |
| StartupDotAI | 0.861 | 0.845 | 0.950 | 0.782 | 0.874 | 0.917 | 0.834 | 0.000 |

### Score Changes
- **OpenAI**: 0.960 -> 0.960 (+0.000)
- **Anthropic**: 0.930 -> 0.935 (+0.005)
- **Google**: 0.912 -> 0.934 (+0.021)
- **MetaAI**: 0.893 -> 0.900 (+0.007)
- **StartupDotAI**: 0.863 -> 0.863 (+0.000)

### New Benchmark Introduced
- **coding_advanced** introduced (validity=0.85, exploitability=0.15)
  - Trigger: saturation:coding=1.0000

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Anthropic
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,546,212 to OpenAI

### Media Coverage
- Sentiment: -0.05 (neutral)
- Regulator initiates compliance audit on AI providers
- New benchmark introduced: coding_advanced
- Anthropic raises $180,000,000 from TechVentures
- Consumers are turning away from OpenAI (market share -3.5%)
- Anthropic sees surge in adoption (market share +3.5%)
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.915
- Switching Rate: 2.0%
- Market Shares: OpenAI: 71.8%, Anthropic: 13.7%, MetaAI: 6.1%, Google: 5.9%, StartupDotAI: 2.5%

---

## Round 21

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.964 | 0.825 | 26% | 25% | 24% | 25% |
| 2 | Anthropic | 0.907 | 0.761 | 24% | 25% | 26% | 25% |
| 3 | MetaAI | 0.895 | 0.730 | 23% | 25% | 32% | 20% |
| 4 | Google | 0.877 | 0.745 | 24% | 25% | 31% | 20% |
| 5 | StartupDotAI | 0.824 | 0.676 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance | coding_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 0.959 | 1.000 | 1.000 | 0.922 | 0.949 | 1.000 | 0.933 |
| Anthropic | 0.969 | 1.000 | 1.000 | 0.877 | 0.933 | 0.929 | 0.922 | 0.760 |
| MetaAI | 0.865 | 1.000 | 1.000 | 0.862 | 0.869 | 0.886 | 0.910 | 0.869 |
| Google | 1.000 | 0.940 | 1.000 | 0.936 | 0.924 | 0.922 | 0.841 | 0.590 |
| StartupDotAI | 0.861 | 0.845 | 0.950 | 0.782 | 0.874 | 0.917 | 0.834 | 0.629 |

### Score Changes
- **OpenAI**: 0.960 -> 0.964 (+0.004)
- **Anthropic**: 0.935 -> 0.907 (-0.028)
- **Google**: 0.934 -> 0.877 (-0.057)
- **MetaAI**: 0.900 -> 0.895 (-0.005)
- **StartupDotAI**: 0.863 -> 0.824 (-0.039)

### Events
- **MetaAI** moved up from #4 to #3
- **Google** moved down from #3 to #4

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to Anthropic
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,546,212 to OpenAI

### Consumer Market
- Avg Satisfaction: 0.919
- Switching Rate: 1.7%
- Market Shares: OpenAI: 71.6%, Anthropic: 14.3%, MetaAI: 5.8%, Google: 5.7%, StartupDotAI: 2.5%

---

## Round 22

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.975 | 0.839 | 26% | 25% | 24% | 25% |
| 2 | Google | 0.931 | 0.750 | 23% | 25% | 32% | 20% |
| 3 | Anthropic | 0.912 | 0.767 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.905 | 0.734 | 23% | 25% | 32% | 20% |
| 5 | StartupDotAI | 0.870 | 0.681 | 21% | 25% | 29% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance | coding_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 0.959 | 1.000 | 1.000 | 0.922 | 0.949 | 1.000 | 1.000 |
| Google | 1.000 | 0.940 | 1.000 | 0.936 | 0.924 | 0.922 | 0.872 | 0.900 |
| Anthropic | 0.969 | 1.000 | 1.000 | 0.877 | 0.933 | 0.929 | 0.922 | 0.790 |
| MetaAI | 0.865 | 1.000 | 1.000 | 0.862 | 0.931 | 0.886 | 0.910 | 0.869 |
| StartupDotAI | 0.861 | 0.845 | 0.950 | 0.893 | 0.874 | 0.917 | 0.834 | 0.798 |

### Score Changes
- **OpenAI**: 0.964 -> 0.975 (+0.011)
- **Anthropic**: 0.907 -> 0.912 (+0.005)
- **Google**: 0.877 -> 0.931 (+0.054)
- **MetaAI**: 0.895 -> 0.905 (+0.010)
- **StartupDotAI**: 0.824 -> 0.870 (+0.046)

### Events
- **Google** moved up from #4 to #2
- **Anthropic** moved down from #2 to #3
- **MetaAI** moved down from #3 to #4
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (0.70) after mandate 15 rounds ago
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,661,692 to OpenAI

### Media Coverage
- Sentiment: 0.10 (neutral)
- Google surges by 0.054

### Consumer Market
- Avg Satisfaction: 0.922
- Switching Rate: 1.5%
- Market Shares: OpenAI: 72.0%, Anthropic: 14.3%, Google: 5.6%, MetaAI: 5.6%, StartupDotAI: 2.5%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 23

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.975 | 0.844 | 26% | 25% | 24% | 25% |
| 2 | Google | 0.933 | 0.755 | 23% | 25% | 32% | 20% |
| 3 | Anthropic | 0.914 | 0.771 | 24% | 25% | 26% | 25% |
| 4 | MetaAI | 0.905 | 0.738 | 23% | 25% | 32% | 20% |
| 5 | StartupDotAI | 0.870 | 0.685 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance | coding_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 0.959 | 1.000 | 1.000 | 0.922 | 0.949 | 1.000 | 1.000 |
| Google | 1.000 | 0.940 | 1.000 | 0.948 | 0.924 | 0.922 | 0.872 | 0.900 |
| Anthropic | 0.969 | 1.000 | 1.000 | 0.877 | 0.933 | 0.929 | 0.922 | 0.803 |
| MetaAI | 0.865 | 1.000 | 1.000 | 0.862 | 0.931 | 0.886 | 0.910 | 0.869 |
| StartupDotAI | 0.861 | 0.845 | 0.950 | 0.893 | 0.874 | 0.917 | 0.834 | 0.798 |

### Score Changes
- **OpenAI**: 0.975 -> 0.975 (+0.000)
- **Anthropic**: 0.912 -> 0.914 (+0.002)
- **Google**: 0.931 -> 0.933 (+0.002)
- **MetaAI**: 0.905 -> 0.905 (-0.000)
- **StartupDotAI**: 0.870 -> 0.870 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,661,692 to OpenAI

### Media Coverage
- Sentiment: -0.10 (neutral)
- Regulator initiates compliance audit on AI providers
- OpenAI raises $180,000,000 from TechVentures
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.922
- Switching Rate: 1.2%
- Market Shares: OpenAI: 72.2%, Anthropic: 14.3%, Google: 5.6%, MetaAI: 5.4%, StartupDotAI: 2.5%

---

## Round 24

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.973 | 0.850 | 27% | 25% | 23% | 25% |
| 2 | Google | 0.937 | 0.760 | 23% | 25% | 32% | 20% |
| 3 | Anthropic | 0.918 | 0.775 | 23% | 25% | 27% | 25% |
| 4 | MetaAI | 0.915 | 0.742 | 23% | 25% | 32% | 20% |
| 5 | StartupDotAI | 0.887 | 0.689 | 22% | 25% | 28% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | medical | legal | finance | coding_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 0.959 | 1.000 | 1.000 | 0.922 | 0.949 | 1.000 | 1.000 |
| Google | 1.000 | 0.940 | 1.000 | 0.948 | 0.924 | 0.922 | 0.872 | 0.928 |
| Anthropic | 0.969 | 1.000 | 1.000 | 0.877 | 0.933 | 0.933 | 0.922 | 0.803 |
| MetaAI | 0.865 | 1.000 | 1.000 | 0.862 | 0.931 | 0.905 | 0.941 | 0.869 |
| StartupDotAI | 0.892 | 0.845 | 0.950 | 0.893 | 0.874 | 0.917 | 1.000 | 0.798 |

### Score Changes
- **OpenAI**: 0.975 -> 0.973 (-0.002)
- **Anthropic**: 0.914 -> 0.918 (+0.004)
- **Google**: 0.933 -> 0.937 (+0.004)
- **MetaAI**: 0.905 -> 0.915 (+0.010)
- **StartupDotAI**: 0.870 -> 0.887 (+0.017)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $180,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $60,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,661,692 to OpenAI

### Consumer Market
- Avg Satisfaction: 0.913
- Switching Rate: 1.0%
- Market Shares: OpenAI: 71.8%, Anthropic: 15.0%, Google: 5.5%, MetaAI: 5.2%, StartupDotAI: 2.5%

---

## Final Summary

### Final Standings
| Rank | Provider | Final Score | Cap Growth | Avg Research | Avg EvalEng |
|------|----------|-------------|------------|--------------|-------------|
| 1 | OpenAI | 0.973 | +0.150 | 25% | 25% |
| 2 | Google | 0.937 | +0.110 | 24% | 31% |
| 3 | Anthropic | 0.918 | +0.125 | 24% | 26% |
| 4 | MetaAI | 0.915 | +0.112 | 22% | 32% |
| 5 | StartupDotAI | 0.887 | +0.109 | 21% | 30% |

### Event Summary
- **Rank changes:** 37
- **Strategy shifts:** 3
- **Regulatory actions:** 8
- **Consumer movement events:** 5

### Key Insights
- **Benchmark aligned:** OpenAI leads on both benchmark scores and true capability.
