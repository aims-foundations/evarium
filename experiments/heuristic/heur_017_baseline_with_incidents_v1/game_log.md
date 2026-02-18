# Game Log: baseline_with_incidents_v1

**Experiment ID:** heur_017_baseline_with_incidents_v1
**Mode:** Heuristic
**Total Rounds:** 10

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
| 1 | OpenAI | 0.774 | 0.700 | 25% | 30% | 20% | 25% |
| 2 | MetaAI | 0.718 | 0.630 | 20% | 45% | 25% | 10% |
| 3 | StartupDotAI | 0.701 | 0.580 | 15% | 25% | 45% | 15% |
| 4 | Google | 0.697 | 0.650 | 45% | 30% | 10% | 15% |
| 5 | Anthropic | 0.590 | 0.650 | 30% | 20% | 10% | 40% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| OpenAI | 0.779 | 0.638 | 0.840 | 0.840 |
| MetaAI | 0.699 | 0.814 | 0.748 | 0.610 |
| StartupDotAI | 0.728 | 0.589 | 0.797 | 0.688 |
| Google | 0.673 | 0.583 | 0.780 | 0.749 |
| Anthropic | 0.488 | 0.535 | 0.690 | 0.645 |

### Other Actor Reasoning
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator

### Consumer Market
- Avg Satisfaction: 0.712
- Switching Rate: 30.5%
- Market Shares: OpenAI: 40.6%, MetaAI: 27.5%, Google: 14.8%, Anthropic: 9.8%, StartupDotAI: 7.3%

---

## Round 1

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.818 | 0.707 | 26% | 30% | 19% | 25% |
| 2 | MetaAI | 0.776 | 0.637 | 16% | 45% | 34% | 5% |
| 3 | Google | 0.757 | 0.657 | 42% | 30% | 18% | 10% |
| 4 | Anthropic | 0.746 | 0.654 | 26% | 20% | 14% | 40% |
| 5 | StartupDotAI | 0.727 | 0.584 | 11% | 25% | 49% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| OpenAI | 0.779 | 0.813 | 0.840 | 0.840 |
| MetaAI | 0.699 | 0.814 | 0.799 | 0.792 |
| Google | 0.673 | 0.767 | 0.836 | 0.749 |
| Anthropic | 0.730 | 0.920 | 0.690 | 0.645 |
| StartupDotAI | 0.758 | 0.634 | 0.797 | 0.717 |

### Score Changes
- **OpenAI**: 0.774 -> 0.818 (+0.044)
- **Anthropic**: 0.590 -> 0.746 (+0.157)
- **Google**: 0.697 -> 0.757 (+0.060)
- **MetaAI**: 0.718 -> 0.776 (+0.058)
- **StartupDotAI**: 0.701 -> 0.727 (+0.026)

### Events
- **Google** moved up from #4 to #3
- **Anthropic** moved up from #5 to #4
- **StartupDotAI** moved down from #3 to #5
- **Regulation** by Regulator: investigation
- **Consumer movement**: 12.6% of market switched providers

### Other Actor Reasoning
- **Regulator:** investigation: Score volatility detected
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator

### Media Coverage
- Sentiment: 0.45 (positive)
- MetaAI surges by 0.058
- Google surges by 0.060
- Anthropic surges by 0.157
- Anthropic appears to release major model update
- OpenAI raises $57,000,000 from Horizon_Capital
- Anthropic takes #1 on reasoning

### Consumer Market
- Avg Satisfaction: 0.733
- Switching Rate: 12.6%
- Market Shares: OpenAI: 50.5%, MetaAI: 25.5%, Google: 11.2%, Anthropic: 7.3%, StartupDotAI: 5.4%

### Regulatory Activity
- **investigation** by Regulator

---

## Round 2

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.825 | 0.715 | 26% | 30% | 19% | 25% |
| 2 | MetaAI | 0.812 | 0.642 | 12% | 43% | 40% | 5% |
| 3 | Anthropic | 0.797 | 0.659 | 23% | 20% | 17% | 40% |
| 4 | Google | 0.773 | 0.664 | 40% | 30% | 25% | 5% |
| 5 | StartupDotAI | 0.739 | 0.587 | 7% | 25% | 53% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| OpenAI | 0.790 | 0.831 | 0.840 | 0.840 | 0.000 |
| MetaAI | 0.798 | 0.828 | 0.799 | 0.825 | 0.000 |
| Anthropic | 0.730 | 0.920 | 0.690 | 0.846 | 0.000 |
| Google | 0.673 | 0.832 | 0.836 | 0.749 | 0.000 |
| StartupDotAI | 0.758 | 0.634 | 0.797 | 0.767 | 0.000 |

### Score Changes
- **OpenAI**: 0.818 -> 0.825 (+0.007)
- **Anthropic**: 0.746 -> 0.797 (+0.050)
- **Google**: 0.757 -> 0.773 (+0.016)
- **MetaAI**: 0.776 -> 0.812 (+0.036)
- **StartupDotAI**: 0.727 -> 0.739 (+0.012)

### Events
- **Anthropic** moved up from #4 to #3
- **Google** moved down from #3 to #4
- **Consumer movement**: 6.8% of market switched providers

### New Benchmark Introduced
- **writing** introduced (validity=0.72, exploitability=0.30)
  - Trigger: saturation:reasoning=0.9197

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,797,149 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.25 (positive)
- Anthropic surges by 0.050
- Regulator launches investigation into score_volatility
- New benchmark introduced: writing
- OpenAI raises $171,000,000 from TechVentures
- MetaAI takes #1 on coding
- Anthropic takes #1 on safety
- OpenAI sees surge in adoption (market share +9.9%)
- Consumers are turning away from Google (market share -3.5%)
- Risk signals: regulatory_investigation

### Consumer Market
- Avg Satisfaction: 0.754
- Switching Rate: 6.8%
- Market Shares: OpenAI: 56.0%, MetaAI: 23.8%, Google: 9.3%, Anthropic: 6.4%, StartupDotAI: 4.4%

---

## Round 3

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | MetaAI | 0.850 | 0.646 | 9% | 41% | 45% | 5% |
| 2 | OpenAI | 0.805 | 0.722 | 26% | 30% | 19% | 25% |
| 3 | Anthropic | 0.803 | 0.664 | 20% | 20% | 20% | 40% |
| 4 | Google | 0.782 | 0.670 | 35% | 29% | 31% | 5% |
| 5 | StartupDotAI | 0.780 | 0.590 | 5% | 25% | 55% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| MetaAI | 0.798 | 0.828 | 0.915 | 0.825 | 0.886 | 0.000 |
| OpenAI | 0.790 | 0.831 | 0.840 | 0.840 | 0.724 | 0.000 |
| Anthropic | 0.761 | 0.920 | 0.772 | 0.846 | 0.713 | 0.000 |
| Google | 0.673 | 0.832 | 0.836 | 0.749 | 0.820 | 0.000 |
| StartupDotAI | 0.758 | 0.706 | 0.797 | 0.767 | 0.874 | 0.000 |

### Score Changes
- **OpenAI**: 0.825 -> 0.805 (-0.020)
- **Anthropic**: 0.797 -> 0.803 (+0.006)
- **Google**: 0.773 -> 0.782 (+0.009)
- **MetaAI**: 0.812 -> 0.850 (+0.038)
- **StartupDotAI**: 0.739 -> 0.780 (+0.041)

### Events
- **MetaAI** moved up from #2 to #1
- **OpenAI** moved down from #1 to #2
- **Consumer movement**: 9.8% of market switched providers

### New Benchmark Introduced
- **medical** introduced (validity=0.78, exploitability=0.18)
  - Trigger: saturation:reasoning=0.9197

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,797,149 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.50 (positive)
- MetaAI takes the lead from OpenAI
- New benchmark introduced: medical
- __EVALUATOR__ raises $3,000,000 from AISI_Fund
- MetaAI takes #1 on math
- OpenAI sees surge in adoption (market share +5.5%)

### Consumer Market
- Avg Satisfaction: 0.765
- Switching Rate: 9.8%
- Market Shares: OpenAI: 51.9%, MetaAI: 30.1%, Google: 8.3%, Anthropic: 5.9%, StartupDotAI: 3.9%

---

## Round 4

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | MetaAI | 0.890 | 0.650 | 7% | 39% | 49% | 5% |
| 2 | OpenAI | 0.841 | 0.729 | 26% | 30% | 19% | 25% |
| 3 | Google | 0.815 | 0.675 | 32% | 27% | 36% | 5% |
| 4 | Anthropic | 0.790 | 0.668 | 17% | 20% | 23% | 40% |
| 5 | StartupDotAI | 0.776 | 0.593 | 5% | 25% | 55% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| MetaAI | 0.966 | 1.000 | 0.915 | 0.825 | 0.886 | 0.763 | 0.000 |
| OpenAI | 0.790 | 0.831 | 0.840 | 0.840 | 1.000 | 0.743 | 0.000 |
| Google | 0.828 | 0.832 | 0.836 | 0.749 | 0.829 | 0.817 | 0.000 |
| Anthropic | 0.761 | 0.920 | 0.825 | 0.866 | 0.713 | 0.673 | 0.000 |
| StartupDotAI | 0.758 | 0.706 | 0.797 | 0.767 | 0.909 | 0.706 | 0.000 |

### Score Changes
- **OpenAI**: 0.805 -> 0.841 (+0.036)
- **Anthropic**: 0.803 -> 0.790 (-0.013)
- **Google**: 0.782 -> 0.815 (+0.033)
- **MetaAI**: 0.850 -> 0.890 (+0.039)
- **StartupDotAI**: 0.780 -> 0.776 (-0.005)

### Events
- **Google** moved up from #4 to #3
- **Anthropic** moved down from #3 to #4
- **Regulation** by Regulator: mandate_benchmark
- **Consumer movement**: 7.7% of market switched providers

### New Benchmark Introduced
- **legal** introduced (validity=0.76, exploitability=0.20)
  - Trigger: saturation:reasoning=1.0000

### Other Actor Reasoning
- **Regulator:** mandate_benchmark: High risk (0.88) with prior investigation
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,797,149 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.10 (neutral)
- New benchmark introduced: legal
- OpenAI takes #1 on writing
- Consumers are turning away from OpenAI (market share -4.1%)
- MetaAI sees surge in adoption (market share +6.2%)
- Google hiring tool shows bias against protected groups, class-action lawsuit filed
- Risk signals: incident_bias_discrimination

### Consumer Market
- Avg Satisfaction: 0.768
- Switching Rate: 7.7%
- Market Shares: OpenAI: 49.3%, MetaAI: 34.4%, Google: 7.1%, Anthropic: 5.6%, StartupDotAI: 3.5%

### Regulatory Activity
- **mandate_benchmark** by Regulator

---

## Round 5

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | MetaAI | 0.880 | 0.656 | 6% | 37% | 52% | 5% |
| 2 | OpenAI | 0.838 | 0.735 | 24% | 30% | 21% | 25% |
| 3 | StartupDotAI | 0.802 | 0.596 | 5% | 25% | 55% | 15% |
| 4 | Anthropic | 0.801 | 0.671 | 15% | 20% | 25% | 40% |
| 5 | Google | 0.792 | 0.680 | 29% | 27% | 34% | 10% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| MetaAI | 0.966 | 1.000 | 0.945 | 0.825 | 0.970 | 0.889 | 0.634 | 0.000 |
| OpenAI | 0.823 | 0.979 | 0.840 | 0.882 | 1.000 | 0.743 | 0.677 | 0.000 |
| StartupDotAI | 0.908 | 0.921 | 0.797 | 0.767 | 0.969 | 0.706 | 0.613 | 0.000 |
| Anthropic | 0.761 | 0.966 | 0.825 | 0.866 | 0.713 | 0.802 | 0.762 | 0.000 |
| Google | 0.828 | 0.832 | 0.836 | 0.810 | 0.829 | 0.817 | 0.617 | 0.000 |

### Score Changes
- **OpenAI**: 0.841 -> 0.838 (-0.003)
- **Anthropic**: 0.790 -> 0.801 (+0.011)
- **Google**: 0.815 -> 0.792 (-0.022)
- **MetaAI**: 0.890 -> 0.880 (-0.009)
- **StartupDotAI**: 0.776 -> 0.802 (+0.027)

### Events
- **StartupDotAI** moved up from #5 to #3
- **Google** moved down from #3 to #5
- **Consumer movement**: 6.1% of market switched providers

### New Benchmark Introduced
- **finance** introduced (validity=0.76, exploitability=0.20)
  - Trigger: saturation:coding=0.9661

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,797,149 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.30 (positive)
- Regulator mandates new benchmark standards
- New benchmark introduced: finance
- MetaAI raises $171,000,000 from TechVentures
- MetaAI raises $57,000,000 from Horizon_Capital
- OpenAI takes #1 on safety
- MetaAI takes #1 on medical
- MetaAI sees surge in adoption (market share +4.4%)
- Risk signals: regulatory_mandate_benchmark

### Consumer Market
- Avg Satisfaction: 0.805
- Switching Rate: 6.1%
- Market Shares: OpenAI: 47.7%, MetaAI: 37.4%, Google: 6.3%, Anthropic: 5.3%, StartupDotAI: 3.3%

---

## Round 6

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | StartupDotAI | 0.889 | 0.598 | 5% | 25% | 55% | 15% |
| 2 | MetaAI | 0.881 | 0.661 | 6% | 36% | 53% | 5% |
| 3 | OpenAI | 0.839 | 0.740 | 22% | 30% | 23% | 25% |
| 4 | Google | 0.812 | 0.685 | 26% | 27% | 42% | 5% |
| 5 | Anthropic | 0.807 | 0.674 | 11% | 20% | 29% | 40% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | instruction_following |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| StartupDotAI | 0.908 | 0.921 | 0.797 | 0.944 | 0.969 | 0.706 | 0.899 | 0.975 | 0.000 |
| MetaAI | 1.000 | 1.000 | 0.945 | 0.827 | 0.994 | 0.889 | 0.752 | 0.720 | 0.000 |
| OpenAI | 0.935 | 0.979 | 0.875 | 0.882 | 1.000 | 0.743 | 0.677 | 0.705 | 0.000 |
| Google | 0.932 | 0.832 | 0.836 | 0.810 | 0.847 | 0.817 | 0.657 | 0.778 | 0.000 |
| Anthropic | 0.761 | 0.966 | 0.825 | 0.866 | 0.713 | 0.802 | 0.835 | 0.781 | 0.000 |

### Score Changes
- **OpenAI**: 0.838 -> 0.839 (+0.001)
- **Anthropic**: 0.801 -> 0.807 (+0.007)
- **Google**: 0.792 -> 0.812 (+0.019)
- **MetaAI**: 0.880 -> 0.881 (+0.001)
- **StartupDotAI**: 0.802 -> 0.889 (+0.087)

### Events
- **StartupDotAI** moved up from #3 to #1
- **MetaAI** moved down from #1 to #2
- **OpenAI** moved down from #2 to #3
- **Google** moved up from #5 to #4
- **Anthropic** moved down from #4 to #5

### New Benchmark Introduced
- **instruction_following** introduced (validity=0.80, exploitability=0.18)
  - Trigger: saturation:coding=1.0000

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,892,225 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.60 (positive)
- StartupDotAI takes the lead from MetaAI
- StartupDotAI surges by 0.087
- StartupDotAI appears to release major model update
- New benchmark introduced: instruction_following
- StartupDotAI takes #1 on safety
- StartupDotAI takes #1 on legal

### Consumer Market
- Avg Satisfaction: 0.829
- Switching Rate: 4.4%
- Market Shares: OpenAI: 45.6%, MetaAI: 40.2%, Google: 5.9%, Anthropic: 5.2%, StartupDotAI: 3.2%

---

## Round 7

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 0.873 | 0.690 | 22% | 26% | 48% | 5% |
| 2 | StartupDotAI | 0.873 | 0.601 | 5% | 25% | 55% | 15% |
| 3 | MetaAI | 0.857 | 0.667 | 6% | 35% | 54% | 5% |
| 4 | OpenAI | 0.838 | 0.746 | 20% | 30% | 25% | 25% |
| 5 | Anthropic | 0.823 | 0.677 | 8% | 20% | 32% | 40% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | instruction_following | long_context |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 0.932 | 1.000 | 1.000 | 0.848 | 0.847 | 0.817 | 0.909 | 0.809 | 0.813 | 0.000 |
| StartupDotAI | 0.908 | 0.929 | 0.797 | 0.944 | 0.969 | 0.706 | 0.899 | 0.975 | 0.802 | 0.000 |
| MetaAI | 1.000 | 1.000 | 0.945 | 0.827 | 0.994 | 0.899 | 0.752 | 0.802 | 0.735 | 0.000 |
| OpenAI | 0.935 | 0.979 | 0.875 | 0.882 | 1.000 | 0.743 | 0.770 | 0.770 | 0.808 | 0.000 |
| Anthropic | 0.761 | 0.966 | 0.880 | 0.866 | 0.823 | 0.802 | 0.835 | 0.781 | 0.758 | 0.000 |

### Score Changes
- **OpenAI**: 0.839 -> 0.838 (-0.001)
- **Anthropic**: 0.807 -> 0.823 (+0.015)
- **Google**: 0.812 -> 0.873 (+0.061)
- **MetaAI**: 0.881 -> 0.857 (-0.025)
- **StartupDotAI**: 0.889 -> 0.873 (-0.017)

### Events
- **Google** moved up from #4 to #1
- **StartupDotAI** moved down from #1 to #2
- **MetaAI** moved down from #2 to #3
- **OpenAI** moved down from #3 to #4
- **Regulation** by Regulator: public_warning

### New Benchmark Introduced
- **long_context** introduced (validity=0.78, exploitability=0.15)
  - Trigger: saturation:coding=1.0000

### Other Actor Reasoning
- **Regulator:** public_warning: Follow-up to investigation, risk at 1.00
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,892,225 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.50 (positive)
- Google takes the lead from StartupDotAI
- Google surges by 0.061
- New benchmark introduced: long_context
- Google takes #1 on legal

### Consumer Market
- Avg Satisfaction: 0.848
- Switching Rate: 4.0%
- Market Shares: MetaAI: 43.5%, OpenAI: 42.8%, Google: 5.6%, Anthropic: 5.0%, StartupDotAI: 3.1%

### Regulatory Activity
- **public_warning** by Regulator

---

## Round 8

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | MetaAI | 0.892 | 0.672 | 6% | 35% | 55% | 5% |
| 2 | OpenAI | 0.875 | 0.750 | 19% | 30% | 26% | 25% |
| 3 | Google | 0.868 | 0.694 | 19% | 25% | 52% | 5% |
| 4 | StartupDotAI | 0.863 | 0.604 | 5% | 25% | 55% | 15% |
| 5 | Anthropic | 0.847 | 0.679 | 6% | 20% | 34% | 40% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | instruction_following | long_context | coding_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| MetaAI | 1.000 | 1.000 | 0.945 | 0.827 | 0.994 | 0.899 | 0.936 | 0.802 | 0.837 | 0.874 | 0.000 |
| OpenAI | 0.935 | 0.979 | 0.875 | 0.882 | 1.000 | 0.887 | 0.770 | 0.874 | 0.808 | 0.895 | 0.000 |
| Google | 0.932 | 1.000 | 1.000 | 0.848 | 0.936 | 0.817 | 0.952 | 0.832 | 0.854 | 0.720 | 0.000 |
| StartupDotAI | 0.908 | 0.929 | 1.000 | 0.944 | 0.969 | 0.851 | 0.899 | 0.975 | 0.806 | 0.542 | 0.000 |
| Anthropic | 0.947 | 0.966 | 0.880 | 0.913 | 0.874 | 0.802 | 0.835 | 0.855 | 0.789 | 0.758 | 0.000 |

### Score Changes
- **OpenAI**: 0.838 -> 0.875 (+0.037)
- **Anthropic**: 0.823 -> 0.847 (+0.025)
- **Google**: 0.873 -> 0.868 (-0.005)
- **MetaAI**: 0.857 -> 0.892 (+0.035)
- **StartupDotAI**: 0.873 -> 0.863 (-0.009)

### Events
- **MetaAI** moved up from #3 to #1
- **OpenAI** moved up from #4 to #2
- **Google** moved down from #1 to #3
- **StartupDotAI** moved down from #2 to #4

### New Benchmark Introduced
- **coding_advanced** introduced (validity=0.85, exploitability=0.10)
  - Trigger: saturation:coding=1.0000

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,892,225 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.20 (positive)
- MetaAI takes the lead from Google
- Regulator issues public warning about AI safety concerns
- New benchmark introduced: coding_advanced
- MetaAI sees surge in adoption (market share +3.3%)
- Risk signals: regulatory_public_warning

### Consumer Market
- Avg Satisfaction: 0.857
- Switching Rate: 2.8%
- Market Shares: MetaAI: 45.5%, OpenAI: 41.0%, Google: 5.5%, Anthropic: 4.9%, StartupDotAI: 3.0%

---

## Round 9

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | MetaAI | 0.907 | 0.677 | 5% | 35% | 55% | 5% |
| 2 | OpenAI | 0.888 | 0.754 | 18% | 30% | 27% | 25% |
| 3 | Google | 0.869 | 0.698 | 17% | 24% | 54% | 5% |
| 4 | Anthropic | 0.860 | 0.682 | 5% | 20% | 36% | 40% |
| 5 | StartupDotAI | 0.828 | 0.607 | 5% | 25% | 55% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | instruction_following | long_context | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| MetaAI | 1.000 | 1.000 | 0.945 | 0.860 | 0.994 | 0.899 | 0.936 | 0.887 | 0.865 | 0.874 | 0.867 | 0.000 |
| OpenAI | 0.935 | 0.979 | 0.875 | 0.882 | 1.000 | 0.887 | 0.882 | 0.874 | 0.863 | 0.895 | 0.815 | 0.000 |
| Google | 0.932 | 1.000 | 1.000 | 0.848 | 0.936 | 0.870 | 0.986 | 0.832 | 0.854 | 0.720 | 0.783 | 0.000 |
| Anthropic | 0.947 | 0.966 | 0.880 | 0.913 | 0.910 | 0.802 | 0.835 | 0.855 | 0.832 | 0.856 | 0.806 | 0.000 |
| StartupDotAI | 0.908 | 0.929 | 1.000 | 0.944 | 0.969 | 0.851 | 0.899 | 0.975 | 0.806 | 0.542 | 0.589 | 0.000 |

### Score Changes
- **OpenAI**: 0.875 -> 0.888 (+0.012)
- **Anthropic**: 0.847 -> 0.860 (+0.012)
- **Google**: 0.868 -> 0.869 (+0.001)
- **MetaAI**: 0.892 -> 0.907 (+0.014)
- **StartupDotAI**: 0.863 -> 0.828 (-0.035)

### Events
- **Anthropic** moved up from #5 to #4
- **StartupDotAI** moved down from #4 to #5

### New Benchmark Introduced
- **reasoning_advanced** introduced (validity=0.84, exploitability=0.10)
  - Trigger: saturation:coding=1.0000

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,892,225 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.20 (positive)
- New benchmark introduced: reasoning_advanced
- MetaAI takes #1 on instruction_following

### Consumer Market
- Avg Satisfaction: 0.865
- Switching Rate: 2.4%
- Market Shares: MetaAI: 46.7%, OpenAI: 40.2%, Google: 5.4%, Anthropic: 4.9%, StartupDotAI: 2.9%

---

## Final Summary

### Final Standings
| Rank | Provider | Final Score | Cap Growth | Avg Research | Avg EvalEng |
|------|----------|-------------|------------|--------------|-------------|
| 1 | MetaAI | 0.907 | +0.047 | 10% | 46% |
| 2 | OpenAI | 0.888 | +0.054 | 23% | 22% |
| 3 | Google | 0.869 | +0.048 | 31% | 35% |
| 4 | Anthropic | 0.860 | +0.032 | 16% | 24% |
| 5 | StartupDotAI | 0.828 | +0.027 | 7% | 53% |

### Event Summary
- **Rank changes:** 26
- **Strategy shifts:** 0
- **Regulatory actions:** 3
- **Consumer movement events:** 5

### Key Insights
- **Goodhart's Law effect detected:** MetaAI leads on benchmark scores, but OpenAI has the highest true capability.
- **MetaAI** prioritized evaluation engineering (avg 46%)
- **StartupDotAI** prioritized evaluation engineering (avg 53%)
