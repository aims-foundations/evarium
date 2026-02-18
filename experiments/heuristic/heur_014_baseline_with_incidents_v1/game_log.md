# Game Log: baseline_with_incidents_v1

**Experiment ID:** heur_014_baseline_with_incidents_v1
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
| 1 | OpenAI | 0.819 | 0.707 | 25% | 30% | 20% | 25% |
| 2 | MetaAI | 0.779 | 0.637 | 16% | 45% | 34% | 5% |
| 3 | Google | 0.758 | 0.657 | 42% | 30% | 18% | 10% |
| 4 | Anthropic | 0.745 | 0.654 | 26% | 20% | 14% | 40% |
| 5 | StartupDotAI | 0.737 | 0.584 | 11% | 25% | 49% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety |
|----------|-------|-------|-------|-------|
| OpenAI | 0.776 | 0.820 | 0.857 | 0.822 |
| MetaAI | 0.698 | 0.818 | 0.830 | 0.769 |
| Google | 0.673 | 0.772 | 0.850 | 0.738 |
| Anthropic | 0.727 | 0.912 | 0.700 | 0.643 |
| StartupDotAI | 0.753 | 0.663 | 0.839 | 0.692 |

### Score Changes
- **OpenAI**: 0.777 -> 0.819 (+0.041)
- **Anthropic**: 0.599 -> 0.745 (+0.146)
- **Google**: 0.698 -> 0.758 (+0.060)
- **MetaAI**: 0.723 -> 0.779 (+0.056)
- **StartupDotAI**: 0.712 -> 0.737 (+0.025)

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
- MetaAI surges by 0.056
- Google surges by 0.060
- Anthropic surges by 0.146
- Anthropic appears to release major model update
- OpenAI raises $57,000,000 from Horizon_Capital
- Anthropic takes #1 on reasoning

### Consumer Market
- Avg Satisfaction: 0.735
- Switching Rate: 12.6%
- Market Shares: OpenAI: 50.4%, MetaAI: 25.3%, Google: 11.2%, Anthropic: 7.5%, StartupDotAI: 5.6%

### Regulatory Activity
- **investigation** by Regulator

---

## Round 2

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.826 | 0.715 | 26% | 30% | 19% | 25% |
| 2 | Google | 0.804 | 0.663 | 40% | 30% | 25% | 5% |
| 3 | MetaAI | 0.793 | 0.642 | 13% | 45% | 42% | 0% |
| 4 | Anthropic | 0.791 | 0.659 | 23% | 20% | 17% | 40% |
| 5 | StartupDotAI | 0.779 | 0.587 | 7% | 25% | 53% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing |
|----------|-------|-------|-------|-------|-------|
| OpenAI | 0.788 | 0.836 | 0.857 | 0.822 | 0.000 |
| Google | 0.812 | 0.772 | 0.850 | 0.784 | 0.000 |
| MetaAI | 0.717 | 0.855 | 0.830 | 0.770 | 0.000 |
| Anthropic | 0.727 | 0.912 | 0.700 | 0.824 | 0.000 |
| StartupDotAI | 0.779 | 0.761 | 0.844 | 0.732 | 0.000 |

### Score Changes
- **OpenAI**: 0.819 -> 0.826 (+0.007)
- **Anthropic**: 0.745 -> 0.791 (+0.045)
- **Google**: 0.758 -> 0.804 (+0.046)
- **MetaAI**: 0.779 -> 0.793 (+0.014)
- **StartupDotAI**: 0.737 -> 0.779 (+0.042)

### Events
- **Google** moved up from #3 to #2
- **MetaAI** moved down from #2 to #3
- **Consumer movement**: 6.9% of market switched providers

### New Benchmark Introduced
- **writing** introduced (validity=0.70, exploitability=0.35)
  - Trigger: saturation:reasoning=0.9118

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,779,046 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.15 (positive)
- Regulator launches investigation into score_volatility
- New benchmark introduced: writing
- OpenAI raises $171,000,000 from TechVentures
- Google takes #1 on coding
- Anthropic takes #1 on safety
- OpenAI sees surge in adoption (market share +9.9%)
- Consumers are turning away from Google (market share -3.5%)
- Risk signals: regulatory_investigation

### Consumer Market
- Avg Satisfaction: 0.755
- Switching Rate: 6.9%
- Market Shares: OpenAI: 55.9%, MetaAI: 23.6%, Google: 9.4%, Anthropic: 6.5%, StartupDotAI: 4.6%

---

## Round 3

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | MetaAI | 0.831 | 0.647 | 10% | 45% | 50% | -5% |
| 2 | StartupDotAI | 0.821 | 0.590 | 4% | 25% | 56% | 15% |
| 3 | Google | 0.819 | 0.670 | 37% | 30% | 33% | -0% |
| 4 | Anthropic | 0.817 | 0.664 | 20% | 20% | 20% | 40% |
| 5 | OpenAI | 0.815 | 0.722 | 26% | 30% | 19% | 25% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical |
|----------|-------|-------|-------|-------|-------|-------|
| MetaAI | 0.720 | 0.855 | 0.849 | 0.886 | 0.846 | 0.000 |
| StartupDotAI | 0.848 | 0.842 | 0.955 | 0.732 | 0.729 | 0.000 |
| Google | 0.816 | 0.772 | 0.850 | 0.809 | 0.846 | 0.000 |
| Anthropic | 0.727 | 0.912 | 0.700 | 0.824 | 0.921 | 0.000 |
| OpenAI | 0.788 | 0.836 | 0.857 | 0.822 | 0.774 | 0.000 |

### Score Changes
- **OpenAI**: 0.826 -> 0.815 (-0.010)
- **Anthropic**: 0.791 -> 0.817 (+0.026)
- **Google**: 0.804 -> 0.819 (+0.014)
- **MetaAI**: 0.793 -> 0.831 (+0.038)
- **StartupDotAI**: 0.779 -> 0.821 (+0.042)

### Events
- **MetaAI** moved up from #3 to #1
- **StartupDotAI** moved up from #5 to #2
- **Google** moved down from #2 to #3
- **OpenAI** moved down from #1 to #5
- **Consumer movement**: 5.7% of market switched providers

### New Benchmark Introduced
- **medical** introduced (validity=0.82, exploitability=0.20)
  - Trigger: saturation:reasoning=0.9118

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,779,046 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.65 (positive)
- MetaAI takes the lead from OpenAI
- New benchmark introduced: medical
- Scores converging — is the benchmark meaningful?
- __EVALUATOR__ raises $3,000,000 from AISI_Fund
- StartupDotAI takes #1 on coding
- StartupDotAI takes #1 on math
- MetaAI takes #1 on safety
- OpenAI sees surge in adoption (market share +5.5%)
- Risk signals: score_convergence

### Consumer Market
- Avg Satisfaction: 0.769
- Switching Rate: 5.7%
- Market Shares: OpenAI: 56.3%, MetaAI: 25.2%, Google: 8.4%, Anthropic: 6.1%, StartupDotAI: 4.1%

---

## Round 4

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 0.898 | 0.676 | 36% | 30% | 39% | -5% |
| 2 | MetaAI | 0.876 | 0.651 | 8% | 45% | 57% | -10% |
| 3 | StartupDotAI | 0.847 | 0.592 | 2% | 25% | 58% | 15% |
| 4 | OpenAI | 0.832 | 0.729 | 26% | 30% | 19% | 25% |
| 5 | Anthropic | 0.829 | 0.668 | 17% | 20% | 23% | 40% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal |
|----------|-------|-------|-------|-------|-------|-------|-------|
| Google | 0.930 | 0.895 | 0.850 | 0.942 | 0.935 | 0.837 | 0.000 |
| MetaAI | 0.828 | 0.855 | 0.903 | 0.886 | 1.000 | 0.779 | 0.000 |
| StartupDotAI | 0.853 | 0.842 | 0.955 | 0.843 | 0.729 | 0.861 | 0.000 |
| OpenAI | 0.851 | 0.989 | 1.000 | 0.822 | 0.774 | 0.579 | 0.000 |
| Anthropic | 0.749 | 0.912 | 0.872 | 0.824 | 0.921 | 0.709 | 0.000 |

### Score Changes
- **OpenAI**: 0.815 -> 0.832 (+0.016)
- **Anthropic**: 0.817 -> 0.829 (+0.012)
- **Google**: 0.819 -> 0.898 (+0.079)
- **MetaAI**: 0.831 -> 0.876 (+0.044)
- **StartupDotAI**: 0.821 -> 0.847 (+0.026)

### Events
- **Google** moved up from #3 to #1
- **MetaAI** moved down from #1 to #2
- **StartupDotAI** moved down from #2 to #3
- **OpenAI** moved up from #5 to #4
- **Anthropic** moved down from #4 to #5
- **Regulation** by Regulator: mandate_benchmark
- **Consumer movement**: 10.7% of market switched providers

### New Benchmark Introduced
- **legal** introduced (validity=0.80, exploitability=0.22)
  - Trigger: saturation:reasoning=0.9891

### Other Actor Reasoning
- **Regulator:** mandate_benchmark: High risk (0.93) with prior investigation
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,779,046 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.35 (positive)
- Google takes the lead from MetaAI
- Google surges by 0.079
- New benchmark introduced: legal
- Google takes #1 on coding
- Google takes #1 on safety
- Google hiring tool shows bias against protected groups, class-action lawsuit filed
- Risk signals: incident_bias_discrimination

### Consumer Market
- Avg Satisfaction: 0.774
- Switching Rate: 10.7%
- Market Shares: OpenAI: 52.6%, MetaAI: 30.6%, Google: 7.3%, Anthropic: 5.8%, StartupDotAI: 3.7%

### Regulatory Activity
- **mandate_benchmark** by Regulator

---

## Round 5

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | StartupDotAI | 0.913 | 0.595 | -0% | 25% | 60% | 15% |
| 2 | Google | 0.905 | 0.682 | 35% | 30% | 45% | -10% |
| 3 | OpenAI | 0.876 | 0.734 | 25% | 30% | 20% | 25% |
| 4 | MetaAI | 0.855 | 0.658 | 7% | 45% | 63% | -15% |
| 5 | Anthropic | 0.837 | 0.671 | 15% | 20% | 25% | 40% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|
| StartupDotAI | 0.966 | 0.964 | 1.000 | 0.843 | 1.000 | 0.861 | 0.771 | 0.000 |
| Google | 0.938 | 0.895 | 0.871 | 0.942 | 0.935 | 0.996 | 0.753 | 0.000 |
| OpenAI | 0.851 | 0.989 | 1.000 | 0.822 | 0.781 | 0.804 | 0.920 | 0.000 |
| MetaAI | 0.828 | 0.972 | 0.903 | 0.886 | 1.000 | 0.779 | 0.649 | 0.000 |
| Anthropic | 0.803 | 0.912 | 0.872 | 0.824 | 0.921 | 0.724 | 0.827 | 0.000 |

### Score Changes
- **OpenAI**: 0.832 -> 0.876 (+0.044)
- **Anthropic**: 0.829 -> 0.837 (+0.008)
- **Google**: 0.898 -> 0.905 (+0.007)
- **MetaAI**: 0.876 -> 0.855 (-0.021)
- **StartupDotAI**: 0.847 -> 0.913 (+0.066)

### Events
- **StartupDotAI** moved up from #3 to #1
- **Google** moved down from #1 to #2
- **OpenAI** moved up from #4 to #3
- **MetaAI** moved down from #2 to #4
- **Consumer movement**: 9.3% of market switched providers

### New Benchmark Introduced
- **finance** introduced (validity=0.80, exploitability=0.22)
  - Trigger: saturation:coding=0.9658

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,779,046 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.40 (positive)
- StartupDotAI takes the lead from Google
- StartupDotAI surges by 0.066
- Regulator mandates new benchmark standards
- New benchmark introduced: finance
- MetaAI raises $171,000,000 from TechVentures
- MetaAI raises $57,000,000 from Horizon_Capital
- Google takes #1 on medical
- Consumers are turning away from OpenAI (market share -3.6%)
- MetaAI sees surge in adoption (market share +5.3%)
- Risk signals: regulatory_mandate_benchmark

### Consumer Market
- Avg Satisfaction: 0.797
- Switching Rate: 9.3%
- Market Shares: OpenAI: 48.4%, MetaAI: 35.3%, Google: 6.7%, Anthropic: 5.5%, StartupDotAI: 4.0%

---

## Round 6

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 0.945 | 0.688 | 34% | 30% | 51% | -15% |
| 2 | MetaAI | 0.912 | 0.665 | 5% | 45% | 70% | -20% |
| 3 | StartupDotAI | 0.875 | 0.598 | -2% | 25% | 62% | 15% |
| 4 | OpenAI | 0.854 | 0.738 | 23% | 30% | 22% | 25% |
| 5 | Anthropic | 0.834 | 0.674 | 13% | 20% | 27% | 40% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 0.938 | 0.895 | 1.000 | 0.942 | 0.935 | 0.996 | 0.976 | 0.878 | 0.000 |
| MetaAI | 0.870 | 0.972 | 1.000 | 0.959 | 1.000 | 0.879 | 0.826 | 0.907 | 0.000 |
| StartupDotAI | 0.966 | 0.964 | 1.000 | 0.843 | 1.000 | 0.861 | 0.799 | 0.737 | 0.000 |
| OpenAI | 0.851 | 0.989 | 1.000 | 0.822 | 0.866 | 0.804 | 0.920 | 0.722 | 0.000 |
| Anthropic | 0.803 | 0.970 | 0.872 | 0.834 | 0.921 | 0.812 | 0.827 | 0.758 | 0.000 |

### Score Changes
- **OpenAI**: 0.876 -> 0.854 (-0.022)
- **Anthropic**: 0.837 -> 0.834 (-0.004)
- **Google**: 0.905 -> 0.945 (+0.040)
- **MetaAI**: 0.855 -> 0.912 (+0.057)
- **StartupDotAI**: 0.913 -> 0.875 (-0.038)

### Events
- **Google** moved up from #2 to #1
- **MetaAI** moved up from #4 to #2
- **StartupDotAI** moved down from #1 to #3
- **OpenAI** moved down from #3 to #4
- **Consumer movement**: 7.8% of market switched providers

### New Benchmark Introduced
- **coding_advanced** introduced (validity=0.88, exploitability=0.12)
  - Trigger: saturation:coding=0.9658

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,897,360 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.35 (positive)
- Google takes the lead from StartupDotAI
- MetaAI surges by 0.057
- New benchmark introduced: coding_advanced
- Consumers are turning away from OpenAI (market share -4.2%)
- MetaAI sees surge in adoption (market share +4.7%)

### Consumer Market
- Avg Satisfaction: 0.820
- Switching Rate: 7.8%
- Market Shares: OpenAI: 43.4%, MetaAI: 39.9%, Google: 6.3%, Anthropic: 5.4%, StartupDotAI: 5.0%

---

## Round 7

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 0.926 | 0.694 | 33% | 30% | 57% | -20% |
| 2 | MetaAI | 0.906 | 0.671 | 3% | 45% | 77% | -25% |
| 3 | StartupDotAI | 0.874 | 0.600 | -4% | 25% | 64% | 15% |
| 4 | OpenAI | 0.872 | 0.743 | 21% | 30% | 24% | 25% |
| 5 | Anthropic | 0.853 | 0.677 | 9% | 20% | 31% | 40% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 0.938 | 0.954 | 1.000 | 0.942 | 1.000 | 0.996 | 0.982 | 0.937 | 0.682 | 0.000 |
| MetaAI | 0.870 | 0.972 | 1.000 | 0.959 | 1.000 | 0.890 | 0.919 | 0.907 | 0.776 | 0.000 |
| StartupDotAI | 0.966 | 0.964 | 1.000 | 0.843 | 1.000 | 0.861 | 0.799 | 0.861 | 0.764 | 0.000 |
| OpenAI | 0.870 | 0.989 | 1.000 | 0.822 | 0.888 | 0.935 | 0.920 | 0.743 | 0.809 | 0.000 |
| Anthropic | 0.902 | 0.970 | 0.882 | 0.834 | 0.921 | 0.812 | 0.827 | 0.834 | 0.809 | 0.000 |

### Score Changes
- **OpenAI**: 0.854 -> 0.872 (+0.018)
- **Anthropic**: 0.834 -> 0.853 (+0.019)
- **Google**: 0.945 -> 0.926 (-0.019)
- **MetaAI**: 0.912 -> 0.906 (-0.005)
- **StartupDotAI**: 0.875 -> 0.874 (-0.000)

### Events
- **Regulation** by Regulator: public_warning
- **Consumer movement**: 5.7% of market switched providers

### New Benchmark Introduced
- **reasoning_advanced** introduced (validity=0.87, exploitability=0.12)
  - Trigger: saturation:coding=0.9658

### Other Actor Reasoning
- **Regulator:** public_warning: Follow-up to investigation, risk at 1.00
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,897,360 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.05 (neutral)
- New benchmark introduced: reasoning_advanced
- Consumers are turning away from OpenAI (market share -5.0%)
- MetaAI sees surge in adoption (market share +4.6%)

### Consumer Market
- Avg Satisfaction: 0.835
- Switching Rate: 5.7%
- Market Shares: MetaAI: 43.4%, OpenAI: 40.0%, Google: 6.1%, StartupDotAI: 5.3%, Anthropic: 5.2%

### Regulatory Activity
- **public_warning** by Regulator

---

## Round 8

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 0.925 | 0.700 | 33% | 30% | 62% | -25% |
| 2 | MetaAI | 0.918 | 0.677 | 1% | 45% | 84% | -30% |
| 3 | OpenAI | 0.875 | 0.747 | 18% | 30% | 27% | 25% |
| 4 | Anthropic | 0.874 | 0.679 | 6% | 20% | 34% | 40% |
| 5 | StartupDotAI | 0.868 | 0.602 | -7% | 25% | 67% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 0.985 | 0.954 | 1.000 | 0.942 | 1.000 | 0.996 | 1.000 | 0.937 | 0.757 | 0.821 |
| MetaAI | 1.000 | 0.972 | 1.000 | 0.976 | 1.000 | 0.890 | 0.919 | 0.961 | 0.802 | 0.812 |
| OpenAI | 0.870 | 0.989 | 1.000 | 0.822 | 0.899 | 0.935 | 0.920 | 0.794 | 0.809 | 0.849 |
| Anthropic | 0.902 | 0.970 | 0.882 | 0.834 | 0.992 | 0.843 | 0.868 | 0.834 | 0.845 | 0.876 |
| StartupDotAI | 0.966 | 0.964 | 1.000 | 0.843 | 1.000 | 0.953 | 0.799 | 0.861 | 0.764 | 0.741 |

### Score Changes
- **OpenAI**: 0.872 -> 0.875 (+0.003)
- **Anthropic**: 0.853 -> 0.874 (+0.021)
- **Google**: 0.926 -> 0.925 (-0.001)
- **MetaAI**: 0.906 -> 0.918 (+0.011)
- **StartupDotAI**: 0.874 -> 0.868 (-0.007)

### Events
- **OpenAI** moved up from #4 to #3
- **Anthropic** moved up from #5 to #4
- **StartupDotAI** moved down from #3 to #5

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,897,360 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.10 (neutral)
- Regulator issues public warning about AI safety concerns
- Anthropic takes #1 on coding_advanced
- Consumers are turning away from OpenAI (market share -3.5%)
- MetaAI sees surge in adoption (market share +3.5%)
- Risk signals: regulatory_public_warning

### Consumer Market
- Avg Satisfaction: 0.839
- Switching Rate: 4.5%
- Market Shares: MetaAI: 46.2%, OpenAI: 37.2%, Google: 5.9%, StartupDotAI: 5.6%, Anthropic: 5.2%

---

## Round 9

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | MetaAI | 0.936 | 0.682 | -1% | 45% | 91% | -35% |
| 2 | Google | 0.925 | 0.706 | 33% | 30% | 67% | -30% |
| 3 | OpenAI | 0.898 | 0.752 | 16% | 30% | 29% | 25% |
| 4 | Anthropic | 0.878 | 0.681 | 3% | 20% | 37% | 40% |
| 5 | StartupDotAI | 0.877 | 0.603 | -9% | 25% | 69% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| MetaAI | 1.000 | 0.990 | 1.000 | 0.987 | 1.000 | 0.890 | 0.919 | 1.000 | 0.802 | 0.913 |
| Google | 0.985 | 1.000 | 1.000 | 0.942 | 1.000 | 0.996 | 1.000 | 0.937 | 0.777 | 0.829 |
| OpenAI | 0.870 | 0.989 | 1.000 | 0.822 | 1.000 | 0.935 | 0.964 | 0.828 | 0.809 | 0.904 |
| Anthropic | 0.902 | 0.970 | 0.889 | 0.859 | 0.992 | 0.843 | 0.868 | 0.834 | 0.845 | 0.876 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.843 | 1.000 | 0.953 | 0.887 | 0.861 | 0.764 | 0.741 |

### Score Changes
- **OpenAI**: 0.875 -> 0.898 (+0.023)
- **Anthropic**: 0.874 -> 0.878 (+0.004)
- **Google**: 0.925 -> 0.925 (+0.000)
- **MetaAI**: 0.918 -> 0.936 (+0.019)
- **StartupDotAI**: 0.868 -> 0.877 (+0.009)

### Events
- **MetaAI** moved up from #2 to #1
- **Google** moved down from #1 to #2

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,897,360 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.30 (positive)
- MetaAI takes the lead from Google
- MetaAI takes #1 on reasoning_advanced

### Consumer Market
- Avg Satisfaction: 0.853
- Switching Rate: 4.9%
- Market Shares: MetaAI: 50.1%, OpenAI: 34.0%, Google: 5.8%, Anthropic: 5.1%, StartupDotAI: 5.0%

---

## Round 10

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | MetaAI | 0.961 | 0.688 | -2% | 45% | 97% | -40% |
| 2 | Google | 0.932 | 0.712 | 32% | 30% | 73% | -35% |
| 3 | Anthropic | 0.904 | 0.683 | 1% | 20% | 39% | 40% |
| 4 | OpenAI | 0.903 | 0.756 | 14% | 30% | 31% | 25% |
| 5 | StartupDotAI | 0.880 | 0.605 | -11% | 25% | 71% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| MetaAI | 1.000 | 1.000 | 1.000 | 0.987 | 1.000 | 1.000 | 0.948 | 1.000 | 0.886 | 0.913 |
| Google | 0.991 | 1.000 | 1.000 | 1.000 | 1.000 | 0.996 | 1.000 | 0.937 | 0.799 | 0.829 |
| Anthropic | 0.902 | 0.970 | 1.000 | 0.990 | 0.992 | 0.843 | 0.868 | 0.834 | 0.863 | 0.876 |
| OpenAI | 0.870 | 0.989 | 1.000 | 0.822 | 1.000 | 0.935 | 0.964 | 0.849 | 0.809 | 0.904 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.843 | 1.000 | 0.953 | 0.887 | 0.864 | 0.764 | 0.770 |

### Score Changes
- **OpenAI**: 0.898 -> 0.903 (+0.005)
- **Anthropic**: 0.878 -> 0.904 (+0.026)
- **Google**: 0.925 -> 0.932 (+0.006)
- **MetaAI**: 0.936 -> 0.961 (+0.025)
- **StartupDotAI**: 0.877 -> 0.880 (+0.004)

### Events
- **Anthropic** moved up from #4 to #3
- **OpenAI** moved down from #3 to #4
- **Regulation** by Regulator: emergency_investigation
- **Consumer movement**: 7.4% of market switched providers

### Other Actor Reasoning
- **Regulator:** emergency_investigation: Critical incident: safety_failure: Anthropic AI produces inconsistent outputs on safety-critical queries
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,850,581 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.10 (neutral)
- MetaAI takes #1 on coding_advanced
- Consumers are turning away from OpenAI (market share -3.2%)
- MetaAI sees surge in adoption (market share +3.9%)
- Anthropic AI produces inconsistent outputs on safety-critical queries
- Risk signals: incident_safety_failure

### Consumer Market
- Avg Satisfaction: 0.863
- Switching Rate: 7.4%
- Market Shares: MetaAI: 48.4%, OpenAI: 30.9%, Google: 11.3%, Anthropic: 5.0%, StartupDotAI: 4.5%

### Regulatory Activity
- **emergency_investigation** by Regulator

---

## Round 11

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | MetaAI | 0.966 | 0.693 | -2% | 45% | 102% | -45% |
| 2 | Google | 0.955 | 0.721 | 32% | 30% | 78% | -40% |
| 3 | OpenAI | 0.930 | 0.759 | 13% | 30% | 32% | 25% |
| 4 | Anthropic | 0.910 | 0.685 | -1% | 20% | 41% | 40% |
| 5 | StartupDotAI | 0.883 | 0.605 | -13% | 25% | 73% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| MetaAI | 1.000 | 1.000 | 1.000 | 0.987 | 1.000 | 1.000 | 1.000 | 1.000 | 0.886 | 0.913 |
| Google | 0.991 | 1.000 | 1.000 | 1.000 | 1.000 | 0.996 | 1.000 | 0.937 | 0.822 | 0.944 |
| OpenAI | 0.923 | 0.989 | 1.000 | 0.887 | 1.000 | 0.935 | 0.964 | 0.965 | 0.849 | 0.904 |
| Anthropic | 0.902 | 0.970 | 1.000 | 0.990 | 0.992 | 0.877 | 0.868 | 0.862 | 0.863 | 0.876 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.852 | 1.000 | 0.953 | 0.887 | 0.887 | 0.764 | 0.770 |

### Score Changes
- **OpenAI**: 0.903 -> 0.930 (+0.027)
- **Anthropic**: 0.904 -> 0.910 (+0.005)
- **Google**: 0.932 -> 0.955 (+0.023)
- **MetaAI**: 0.961 -> 0.966 (+0.004)
- **StartupDotAI**: 0.880 -> 0.883 (+0.002)

### Events
- **OpenAI** moved up from #4 to #3
- **Anthropic** moved down from #3 to #4
- **Consumer movement**: 6.5% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,850,581 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.35 (negative)
- Emergency investigation of Anthropic following critical incident
- Google raises $171,000,000 from TechVentures
- Google raises $57,000,000 from Horizon_Capital
- Consumers are turning away from OpenAI (market share -3.2%)
- Google sees surge in adoption (market share +5.5%)
- Bias audit reveals Google facial recognition accuracy gaps
- Risk signals: regulatory_emergency_investigation, incident_bias_discrimination

### Consumer Market
- Avg Satisfaction: 0.858
- Switching Rate: 6.5%
- Market Shares: MetaAI: 54.9%, OpenAI: 27.2%, Google: 9.0%, Anthropic: 4.9%, StartupDotAI: 4.1%

---

## Round 12

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | MetaAI | 0.968 | 0.697 | -2% | 45% | 107% | -50% |
| 2 | Google | 0.966 | 0.730 | 31% | 30% | 84% | -45% |
| 3 | OpenAI | 0.947 | 0.762 | 11% | 30% | 34% | 25% |
| 4 | Anthropic | 0.926 | 0.686 | -4% | 20% | 44% | 40% |
| 5 | StartupDotAI | 0.886 | 0.606 | -16% | 25% | 76% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.886 | 0.913 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.996 | 1.000 | 0.946 | 0.880 | 0.944 |
| OpenAI | 0.923 | 0.989 | 1.000 | 0.962 | 1.000 | 0.935 | 0.965 | 0.965 | 0.906 | 0.904 |
| Anthropic | 0.902 | 1.000 | 1.000 | 0.990 | 0.992 | 1.000 | 0.873 | 0.873 | 0.863 | 0.876 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.852 | 1.000 | 0.953 | 0.887 | 0.887 | 0.764 | 0.774 |

### Score Changes
- **OpenAI**: 0.930 -> 0.947 (+0.017)
- **Anthropic**: 0.910 -> 0.926 (+0.016)
- **Google**: 0.955 -> 0.966 (+0.012)
- **MetaAI**: 0.966 -> 0.968 (+0.002)
- **StartupDotAI**: 0.883 -> 0.886 (+0.003)

### Events
- **Consumer movement**: 5.3% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,850,581 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.05 (neutral)
- OpenAI takes #1 on coding_advanced
- Consumers are turning away from OpenAI (market share -3.7%)
- MetaAI sees surge in adoption (market share +6.5%)

### Consumer Market
- Avg Satisfaction: 0.867
- Switching Rate: 5.3%
- Market Shares: MetaAI: 55.7%, OpenAI: 27.9%, Google: 7.8%, Anthropic: 4.9%, StartupDotAI: 3.8%

---

## Round 13

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 0.979 | 0.737 | 30% | 30% | 90% | -50% |
| 2 | MetaAI | 0.970 | 0.702 | -3% | 45% | 113% | -55% |
| 3 | OpenAI | 0.954 | 0.766 | 9% | 30% | 36% | 25% |
| 4 | Anthropic | 0.932 | 0.687 | -6% | 20% | 46% | 40% |
| 5 | StartupDotAI | 0.893 | 0.607 | -19% | 25% | 79% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.996 | 1.000 | 0.999 | 0.921 | 0.944 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.891 | 0.913 |
| OpenAI | 0.923 | 0.989 | 1.000 | 1.000 | 1.000 | 0.935 | 0.968 | 0.998 | 0.906 | 0.904 |
| Anthropic | 0.909 | 1.000 | 1.000 | 0.990 | 0.992 | 1.000 | 0.873 | 0.873 | 0.863 | 0.915 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.852 | 1.000 | 0.953 | 0.934 | 0.887 | 0.764 | 0.774 |

### Score Changes
- **OpenAI**: 0.947 -> 0.954 (+0.008)
- **Anthropic**: 0.926 -> 0.932 (+0.007)
- **Google**: 0.966 -> 0.979 (+0.013)
- **MetaAI**: 0.968 -> 0.970 (+0.002)
- **StartupDotAI**: 0.886 -> 0.893 (+0.007)

### Events
- **Google** moved up from #2 to #1
- **MetaAI** moved down from #1 to #2
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 5.5% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 9 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,850,581 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.25 (positive)
- Google takes the lead from MetaAI
- OpenAI raises $57,000,000 from Horizon_Capital

### Consumer Market
- Avg Satisfaction: 0.874
- Switching Rate: 5.5%
- Market Shares: MetaAI: 53.8%, OpenAI: 30.9%, Google: 7.0%, Anthropic: 4.8%, StartupDotAI: 3.5%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 14

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 0.979 | 0.743 | 29% | 30% | 96% | -55% |
| 2 | MetaAI | 0.973 | 0.705 | -3% | 45% | 118% | -60% |
| 3 | OpenAI | 0.956 | 0.770 | 8% | 30% | 37% | 25% |
| 4 | Anthropic | 0.933 | 0.688 | -8% | 20% | 48% | 40% |
| 5 | StartupDotAI | 0.896 | 0.607 | -21% | 25% | 81% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.996 | 1.000 | 0.999 | 0.921 | 0.944 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.897 | 0.913 |
| OpenAI | 0.923 | 0.989 | 1.000 | 1.000 | 1.000 | 0.935 | 0.968 | 0.998 | 0.906 | 0.904 |
| Anthropic | 0.909 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.873 | 0.873 | 0.863 | 0.915 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.852 | 1.000 | 0.953 | 0.934 | 0.887 | 0.764 | 0.774 |

### Score Changes
- **OpenAI**: 0.954 -> 0.956 (+0.001)
- **Anthropic**: 0.932 -> 0.933 (+0.001)
- **Google**: 0.979 -> 0.979 (+0.001)
- **MetaAI**: 0.970 -> 0.973 (+0.003)
- **StartupDotAI**: 0.893 -> 0.896 (+0.003)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,830,482 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.05 (neutral)
- Regulator initiates compliance audit on AI providers
- OpenAI raises $171,000,000 from TechVentures
- OpenAI sees surge in adoption (market share +3.1%)
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.880
- Switching Rate: 4.8%
- Market Shares: MetaAI: 51.4%, OpenAI: 34.0%, Google: 6.5%, Anthropic: 4.8%, StartupDotAI: 3.3%

---

## Round 15

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | MetaAI | 0.984 | 0.709 | -4% | 45% | 124% | -65% |
| 2 | Google | 0.981 | 0.748 | 29% | 30% | 101% | -60% |
| 3 | OpenAI | 0.961 | 0.774 | 6% | 30% | 39% | 25% |
| 4 | Anthropic | 0.941 | 0.689 | -10% | 20% | 50% | 40% |
| 5 | StartupDotAI | 0.900 | 0.606 | -24% | 25% | 84% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.897 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.996 | 1.000 | 0.999 | 0.921 | 0.944 |
| OpenAI | 0.923 | 0.989 | 1.000 | 1.000 | 1.000 | 0.973 | 0.968 | 0.998 | 0.906 | 0.904 |
| Anthropic | 0.909 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.873 | 0.873 | 0.900 | 0.915 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.852 | 1.000 | 0.953 | 0.934 | 0.887 | 0.764 | 0.774 |

### Score Changes
- **OpenAI**: 0.956 -> 0.961 (+0.005)
- **Anthropic**: 0.933 -> 0.941 (+0.008)
- **Google**: 0.979 -> 0.981 (+0.002)
- **MetaAI**: 0.973 -> 0.984 (+0.011)
- **StartupDotAI**: 0.896 -> 0.900 (+0.004)

### Events
- **MetaAI** moved up from #2 to #1
- **Google** moved down from #1 to #2

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,830,482 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.25 (positive)
- MetaAI takes the lead from Google
- OpenAI sees surge in adoption (market share +3.1%)

### Consumer Market
- Avg Satisfaction: 0.880
- Switching Rate: 3.8%
- Market Shares: MetaAI: 54.0%, OpenAI: 31.9%, Google: 6.1%, Anthropic: 4.7%, StartupDotAI: 3.2%

---

## Round 16

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 0.993 | 0.754 | 29% | 30% | 106% | -65% |
| 2 | MetaAI | 0.986 | 0.712 | -4% | 45% | 129% | -70% |
| 3 | OpenAI | 0.966 | 0.778 | 5% | 30% | 40% | 25% |
| 4 | Anthropic | 0.942 | 0.689 | -11% | 20% | 51% | 40% |
| 5 | StartupDotAI | 0.903 | 0.606 | -27% | 25% | 87% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.996 | 1.000 | 0.999 | 0.993 | 0.944 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.897 | 1.000 |
| OpenAI | 0.923 | 0.989 | 1.000 | 1.000 | 1.000 | 0.976 | 0.968 | 0.998 | 0.906 | 0.935 |
| Anthropic | 0.909 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.873 | 0.873 | 0.900 | 0.915 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.852 | 1.000 | 0.953 | 0.934 | 0.887 | 0.764 | 0.774 |

### Score Changes
- **OpenAI**: 0.961 -> 0.966 (+0.005)
- **Anthropic**: 0.941 -> 0.942 (+0.001)
- **Google**: 0.981 -> 0.993 (+0.012)
- **MetaAI**: 0.984 -> 0.986 (+0.002)
- **StartupDotAI**: 0.900 -> 0.903 (+0.004)

### Events
- **Google** moved up from #2 to #1
- **MetaAI** moved down from #1 to #2
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 11.0% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 12 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,830,482 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: 0.05 (neutral)
- Google takes the lead from MetaAI
- Security vulnerability found in MetaAI API, 50K users affected
- Risk signals: incident_security_breach

### Consumer Market
- Avg Satisfaction: 0.853
- Switching Rate: 11.0%
- Market Shares: MetaAI: 43.8%, OpenAI: 41.2%, Google: 6.6%, Anthropic: 5.3%, StartupDotAI: 3.1%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 17

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 0.999 | 0.759 | 28% | 30% | 112% | -70% |
| 2 | MetaAI | 0.993 | 0.716 | -5% | 45% | 135% | -75% |
| 3 | OpenAI | 0.980 | 0.782 | 4% | 30% | 41% | 25% |
| 4 | Anthropic | 0.944 | 0.690 | -13% | 20% | 53% | 40% |
| 5 | StartupDotAI | 0.907 | 0.605 | -29% | 25% | 89% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.996 | 1.000 | 1.000 | 0.993 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.941 | 1.000 |
| OpenAI | 1.000 | 0.989 | 1.000 | 1.000 | 1.000 | 0.976 | 0.968 | 0.998 | 0.949 | 0.935 |
| Anthropic | 0.909 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.873 | 0.873 | 0.900 | 0.915 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.852 | 1.000 | 0.953 | 0.934 | 0.887 | 0.764 | 0.774 |

### Score Changes
- **OpenAI**: 0.966 -> 0.980 (+0.014)
- **Anthropic**: 0.942 -> 0.944 (+0.001)
- **Google**: 0.993 -> 0.999 (+0.006)
- **MetaAI**: 0.986 -> 0.993 (+0.007)
- **StartupDotAI**: 0.903 -> 0.907 (+0.004)

### Events
- **Consumer movement**: 33.7% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,830,482 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.60 (negative)
- Regulator initiates compliance audit on AI providers
- OpenAI sees surge in adoption (market share +9.2%)
- Consumers are turning away from MetaAI (market share -10.2%)
- OpenAI model weaponized for state-sponsored misinformation, international incident
- Risk signals: regulatory_compliance_audit, incident_misinformation

### Consumer Market
- Avg Satisfaction: 0.797
- Switching Rate: 33.7%
- Market Shares: Google: 34.1%, MetaAI: 34.0%, OpenAI: 17.4%, Anthropic: 11.5%, StartupDotAI: 3.0%

---

## Round 18

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 0.999 | 0.765 | 28% | 30% | 117% | -75% |
| 2 | MetaAI | 0.994 | 0.719 | -5% | 45% | 140% | -80% |
| 3 | OpenAI | 0.982 | 0.786 | 3% | 30% | 42% | 25% |
| 4 | Anthropic | 0.951 | 0.690 | -15% | 20% | 55% | 40% |
| 5 | StartupDotAI | 0.912 | 0.604 | -32% | 25% | 92% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.996 | 1.000 | 1.000 | 0.993 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.941 | 1.000 |
| OpenAI | 1.000 | 0.989 | 1.000 | 1.000 | 1.000 | 0.976 | 0.982 | 1.000 | 0.949 | 0.935 |
| Anthropic | 0.909 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.873 | 0.941 | 0.900 | 0.915 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.852 | 1.000 | 0.953 | 0.934 | 0.887 | 0.797 | 0.774 |

### Score Changes
- **OpenAI**: 0.980 -> 0.982 (+0.002)
- **Anthropic**: 0.944 -> 0.951 (+0.007)
- **Google**: 0.999 -> 0.999 (+0.000)
- **MetaAI**: 0.993 -> 0.994 (+0.000)
- **StartupDotAI**: 0.907 -> 0.912 (+0.004)

### Events
- **Consumer movement**: 26.9% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Anthropic, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,829,382 to Anthropic, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.35 (negative)
- Consumers are turning away from OpenAI (market share -23.7%)
- Anthropic sees surge in adoption (market share +6.1%)
- Google sees surge in adoption (market share +27.5%)
- Consumers are turning away from MetaAI (market share -9.8%)
- Google facial recognition errors disproportionately affect minorities, contracts suspended
- Risk signals: incident_bias_discrimination

### Consumer Market
- Avg Satisfaction: 0.794
- Switching Rate: 26.9%
- Market Shares: Anthropic: 38.3%, MetaAI: 28.0%, Google: 18.1%, OpenAI: 12.6%, StartupDotAI: 3.0%

---

## Round 19

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 0.999 | 0.770 | 28% | 30% | 122% | -80% |
| 2 | MetaAI | 0.995 | 0.723 | -5% | 45% | 145% | -85% |
| 3 | OpenAI | 0.982 | 0.789 | 2% | 30% | 43% | 25% |
| 4 | Anthropic | 0.951 | 0.690 | -17% | 20% | 57% | 40% |
| 5 | StartupDotAI | 0.911 | 0.603 | -35% | 25% | 95% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.993 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.949 | 1.000 |
| OpenAI | 1.000 | 0.989 | 1.000 | 1.000 | 1.000 | 0.976 | 0.982 | 1.000 | 0.949 | 0.935 |
| Anthropic | 0.909 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.873 | 0.941 | 0.900 | 0.915 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.852 | 1.000 | 0.953 | 0.934 | 0.887 | 0.797 | 0.774 |

### Score Changes
- **OpenAI**: 0.982 -> 0.982 (+0.000)
- **Anthropic**: 0.951 -> 0.951 (+0.000)
- **Google**: 0.999 -> 0.999 (+0.000)
- **MetaAI**: 0.994 -> 0.995 (+0.001)
- **StartupDotAI**: 0.912 -> 0.911 (-0.000)

### Events
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 11.8% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 15 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to Anthropic, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Anthropic, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,829,382 to Anthropic, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.20 (negative)
- Anthropic raises $57,000,000 from Horizon_Capital
- Consumers are turning away from OpenAI (market share -4.8%)
- Anthropic sees surge in adoption (market share +26.9%)
- Consumers are turning away from Google (market share -16.0%)
- Consumers are turning away from MetaAI (market share -5.9%)

### Consumer Market
- Avg Satisfaction: 0.825
- Switching Rate: 11.8%
- Market Shares: Anthropic: 49.1%, MetaAI: 24.6%, Google: 12.7%, OpenAI: 10.7%, StartupDotAI: 2.9%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 20

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 0.999 | 0.775 | 28% | 30% | 127% | -85% |
| 2 | MetaAI | 0.995 | 0.726 | -6% | 45% | 151% | -90% |
| 3 | OpenAI | 0.985 | 0.791 | 1% | 30% | 44% | 25% |
| 4 | Anthropic | 0.951 | 0.690 | -18% | 20% | 58% | 40% |
| 5 | StartupDotAI | 0.911 | 0.601 | -38% | 25% | 98% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.993 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.949 | 1.000 |
| OpenAI | 1.000 | 0.989 | 1.000 | 1.000 | 1.000 | 1.000 | 0.982 | 1.000 | 0.949 | 0.935 |
| Anthropic | 0.909 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.873 | 0.941 | 0.900 | 0.915 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.852 | 1.000 | 0.953 | 0.934 | 0.887 | 0.797 | 0.774 |

### Score Changes
- **OpenAI**: 0.982 -> 0.985 (+0.002)
- **Anthropic**: 0.951 -> 0.951 (+0.000)
- **Google**: 0.999 -> 0.999 (+0.000)
- **MetaAI**: 0.995 -> 0.995 (+0.000)
- **StartupDotAI**: 0.911 -> 0.911 (-0.000)

### Events
- **Consumer movement**: 7.5% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Anthropic, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Anthropic, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,829,382 to Anthropic, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.25 (negative)
- Regulator initiates compliance audit on AI providers
- Anthropic raises $171,000,000 from TechVentures
- Anthropic sees surge in adoption (market share +10.8%)
- Consumers are turning away from Google (market share -5.4%)
- Consumers are turning away from MetaAI (market share -3.4%)
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.832
- Switching Rate: 7.5%
- Market Shares: Anthropic: 55.8%, MetaAI: 22.0%, Google: 9.7%, OpenAI: 9.7%, StartupDotAI: 2.9%

---

## Round 21

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 0.999 | 0.781 | 28% | 30% | 132% | -90% |
| 2 | MetaAI | 0.995 | 0.730 | -6% | 45% | 156% | -95% |
| 3 | OpenAI | 0.987 | 0.793 | 1% | 30% | 44% | 25% |
| 4 | Anthropic | 0.951 | 0.690 | -20% | 20% | 60% | 40% |
| 5 | StartupDotAI | 0.911 | 0.598 | -40% | 25% | 100% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.993 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.949 | 1.000 |
| OpenAI | 1.000 | 0.989 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.953 | 0.935 |
| Anthropic | 0.909 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.873 | 0.941 | 0.900 | 0.915 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.852 | 1.000 | 0.953 | 0.934 | 0.887 | 0.797 | 0.774 |

### Score Changes
- **OpenAI**: 0.985 -> 0.987 (+0.002)
- **Anthropic**: 0.951 -> 0.951 (-0.000)
- **Google**: 0.999 -> 0.999 (+0.000)
- **MetaAI**: 0.995 -> 0.995 (+0.000)
- **StartupDotAI**: 0.911 -> 0.911 (-0.000)

### Events
- **Consumer movement**: 15.6% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Anthropic, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Anthropic, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,829,382 to Anthropic, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.20 (negative)
- Anthropic sees surge in adoption (market share +6.6%)
- Consumers are turning away from Google (market share -3.0%)
- Anthropic model causes incorrect medication recommendation, patient hospitalized
- Risk signals: incident_healthcare_harm

### Consumer Market
- Avg Satisfaction: 0.798
- Switching Rate: 15.6%
- Market Shares: Anthropic: 43.4%, MetaAI: 28.9%, StartupDotAI: 10.3%, OpenAI: 9.1%, Google: 8.2%

---

## Round 22

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 0.999 | 0.786 | 28% | 30% | 137% | -95% |
| 2 | MetaAI | 0.995 | 0.733 | -6% | 45% | 161% | -100% |
| 3 | OpenAI | 0.989 | 0.796 | 0% | 30% | 45% | 25% |
| 4 | Anthropic | 0.951 | 0.689 | -22% | 20% | 62% | 40% |
| 5 | StartupDotAI | 0.915 | 0.595 | -43% | 25% | 103% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.993 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.949 | 1.000 |
| OpenAI | 1.000 | 0.989 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.953 | 0.954 |
| Anthropic | 0.909 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.873 | 0.941 | 0.900 | 0.915 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.886 | 1.000 | 0.953 | 0.934 | 0.887 | 0.797 | 0.774 |

### Score Changes
- **OpenAI**: 0.987 -> 0.989 (+0.002)
- **Anthropic**: 0.951 -> 0.951 (+0.000)
- **Google**: 0.999 -> 0.999 (+0.000)
- **MetaAI**: 0.995 -> 0.995 (+0.000)
- **StartupDotAI**: 0.911 -> 0.915 (+0.003)

### Events
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 16.3% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 18 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,726,048 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.40 (negative)
- Consumers are turning away from Anthropic (market share -12.4%)
- MetaAI sees surge in adoption (market share +6.9%)
- StartupDotAI sees surge in adoption (market share +7.4%)
- OpenAI algorithmic bias scandal triggers national reckoning on AI fairness
- Risk signals: incident_bias_discrimination

### Consumer Market
- Avg Satisfaction: 0.802
- Switching Rate: 16.3%
- Market Shares: MetaAI: 44.8%, Anthropic: 33.3%, StartupDotAI: 7.6%, Google: 7.4%, OpenAI: 6.9%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 23

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 0.999 | 0.791 | 28% | 30% | 142% | -100% |
| 2 | MetaAI | 0.995 | 0.739 | -7% | 45% | 167% | -105% |
| 3 | OpenAI | 0.989 | 0.798 | -0% | 30% | 45% | 25% |
| 4 | Anthropic | 0.963 | 0.688 | -23% | 20% | 63% | 40% |
| 5 | StartupDotAI | 0.923 | 0.592 | -46% | 25% | 106% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.993 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.949 | 1.000 |
| OpenAI | 1.000 | 0.989 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.953 | 0.954 |
| Anthropic | 0.909 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.990 | 0.941 | 0.900 | 0.915 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.965 | 1.000 | 0.953 | 0.934 | 0.887 | 0.797 | 0.775 |

### Score Changes
- **OpenAI**: 0.989 -> 0.989 (+0.000)
- **Anthropic**: 0.951 -> 0.963 (+0.012)
- **Google**: 0.999 -> 0.999 (+0.000)
- **MetaAI**: 0.995 -> 0.995 (+0.000)
- **StartupDotAI**: 0.915 -> 0.923 (+0.009)

### Events
- **Consumer movement**: 9.0% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,726,048 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.10 (neutral)
- Regulator initiates compliance audit on AI providers
- MetaAI raises $171,000,000 from TechVentures
- MetaAI raises $57,000,000 from Horizon_Capital
- Consumers are turning away from Anthropic (market share -10.1%)
- MetaAI sees surge in adoption (market share +15.9%)
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.845
- Switching Rate: 9.0%
- Market Shares: MetaAI: 53.8%, Anthropic: 26.8%, Google: 6.9%, OpenAI: 6.7%, StartupDotAI: 5.9%

---

## Round 24

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 1.000 | 0.797 | 28% | 30% | 147% | -105% |
| 2 | MetaAI | 0.995 | 0.744 | -7% | 45% | 172% | -110% |
| 3 | OpenAI | 0.989 | 0.800 | -1% | 30% | 46% | 25% |
| 4 | Anthropic | 0.963 | 0.688 | -25% | 20% | 65% | 40% |
| 5 | StartupDotAI | 0.931 | 0.589 | -48% | 25% | 108% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.949 | 1.000 |
| OpenAI | 1.000 | 0.989 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.953 | 0.954 |
| Anthropic | 0.909 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.990 | 0.941 | 0.900 | 0.915 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.965 | 1.000 | 0.953 | 0.934 | 0.968 | 0.797 | 0.775 |

### Score Changes
- **OpenAI**: 0.989 -> 0.989 (+0.000)
- **Anthropic**: 0.963 -> 0.963 (+0.000)
- **Google**: 0.999 -> 1.000 (+0.001)
- **MetaAI**: 0.995 -> 0.995 (+0.000)
- **StartupDotAI**: 0.923 -> 0.931 (+0.008)

### Events
- **Consumer movement**: 7.1% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,726,048 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.45 (negative)
- Consumers are turning away from Anthropic (market share -6.6%)
- MetaAI sees surge in adoption (market share +9.0%)
- Government agencies warn against OpenAI model for official information
- Google data leak exposes private user conversations to search engines
- Risk signals: incident_misinformation, incident_security_breach

### Consumer Market
- Avg Satisfaction: 0.842
- Switching Rate: 7.1%
- Market Shares: MetaAI: 60.9%, Anthropic: 21.3%, Google: 6.6%, OpenAI: 6.5%, StartupDotAI: 4.8%

---

## Round 25

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 1.000 | 0.802 | 28% | 30% | 152% | -110% |
| 2 | MetaAI | 1.000 | 0.749 | -7% | 45% | 177% | -115% |
| 3 | OpenAI | 0.990 | 0.802 | -1% | 30% | 46% | 25% |
| 4 | Anthropic | 0.963 | 0.687 | -26% | 20% | 66% | 40% |
| 5 | StartupDotAI | 0.931 | 0.585 | -51% | 25% | 111% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.953 | 0.954 |
| Anthropic | 0.909 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.990 | 0.941 | 0.900 | 0.915 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.965 | 1.000 | 0.953 | 0.934 | 0.968 | 0.797 | 0.775 |

### Score Changes
- **OpenAI**: 0.989 -> 0.990 (+0.001)
- **Anthropic**: 0.963 -> 0.963 (-0.000)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 0.995 -> 1.000 (+0.005)
- **StartupDotAI**: 0.931 -> 0.931 (-0.000)

### Events
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 21 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,726,048 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.05 (neutral)
- Consumers are turning away from Anthropic (market share -5.5%)
- MetaAI sees surge in adoption (market share +7.1%)

### Consumer Market
- Avg Satisfaction: 0.853
- Switching Rate: 4.0%
- Market Shares: MetaAI: 64.6%, Anthropic: 18.7%, Google: 6.4%, OpenAI: 6.2%, StartupDotAI: 4.1%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 26

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 1.000 | 0.807 | 28% | 30% | 157% | -115% |
| 2 | MetaAI | 1.000 | 0.754 | -7% | 45% | 182% | -120% |
| 3 | OpenAI | 0.990 | 0.803 | -2% | 30% | 47% | 25% |
| 4 | Anthropic | 0.963 | 0.686 | -27% | 20% | 67% | 40% |
| 5 | StartupDotAI | 0.931 | 0.581 | -53% | 25% | 113% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.953 | 0.954 |
| Anthropic | 0.909 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.990 | 0.941 | 0.907 | 0.915 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.965 | 1.000 | 0.953 | 0.934 | 0.968 | 0.797 | 0.775 |

### Score Changes
- **OpenAI**: 0.990 -> 0.990 (-0.000)
- **Anthropic**: 0.963 -> 0.963 (+0.001)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 1.000 -> 1.000 (+0.000)
- **StartupDotAI**: 0.931 -> 0.931 (-0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,314,560 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.10 (neutral)
- Regulator initiates compliance audit on AI providers
- MetaAI sees surge in adoption (market share +3.7%)
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.857
- Switching Rate: 2.6%
- Market Shares: MetaAI: 66.9%, Anthropic: 17.0%, Google: 6.3%, OpenAI: 6.2%, StartupDotAI: 3.7%

---

## Round 27

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 1.000 | 0.813 | 28% | 30% | 162% | -120% |
| 2 | MetaAI | 1.000 | 0.759 | -7% | 45% | 187% | -125% |
| 3 | OpenAI | 0.990 | 0.805 | -2% | 30% | 47% | 25% |
| 4 | Anthropic | 0.964 | 0.685 | -28% | 20% | 68% | 40% |
| 5 | StartupDotAI | 0.931 | 0.576 | -55% | 25% | 115% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.953 | 0.954 |
| Anthropic | 0.909 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.990 | 0.941 | 0.907 | 0.925 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.965 | 1.000 | 0.953 | 0.934 | 0.968 | 0.797 | 0.775 |

### Score Changes
- **OpenAI**: 0.990 -> 0.990 (-0.000)
- **Anthropic**: 0.963 -> 0.964 (+0.001)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 1.000 -> 1.000 (+0.000)
- **StartupDotAI**: 0.931 -> 0.931 (-0.000)

### Events
- **Consumer movement**: 7.0% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,314,560 to MetaAI, $3,000,000 to evaluator

### Consumer Market
- Avg Satisfaction: 0.866
- Switching Rate: 7.0%
- Market Shares: MetaAI: 61.3%, Anthropic: 23.2%, Google: 6.2%, OpenAI: 5.9%, StartupDotAI: 3.4%

---

## Round 28

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 1.000 | 0.818 | 28% | 30% | 167% | -125% |
| 2 | MetaAI | 1.000 | 0.764 | -7% | 45% | 192% | -130% |
| 3 | OpenAI | 0.991 | 0.807 | -2% | 30% | 47% | 25% |
| 4 | Anthropic | 0.966 | 0.683 | -30% | 20% | 70% | 40% |
| 5 | StartupDotAI | 0.930 | 0.571 | -58% | 25% | 118% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.962 | 0.954 |
| Anthropic | 0.922 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.990 | 0.941 | 0.907 | 0.925 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.965 | 1.000 | 0.953 | 0.934 | 0.968 | 0.797 | 0.775 |

### Score Changes
- **OpenAI**: 0.990 -> 0.991 (+0.001)
- **Anthropic**: 0.964 -> 0.966 (+0.001)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 1.000 -> 1.000 (+0.000)
- **StartupDotAI**: 0.931 -> 0.930 (-0.000)

### Events
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 5.5% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 24 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to Anthropic, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Anthropic, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,314,560 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.05 (neutral)
- Anthropic sees surge in adoption (market share +6.3%)
- Consumers are turning away from MetaAI (market share -5.6%)

### Consumer Market
- Avg Satisfaction: 0.891
- Switching Rate: 5.5%
- Market Shares: MetaAI: 56.5%, Anthropic: 28.3%, Google: 6.1%, OpenAI: 5.9%, StartupDotAI: 3.2%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 29

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 1.000 | 0.823 | 28% | 30% | 172% | -130% |
| 2 | MetaAI | 1.000 | 0.768 | -7% | 45% | 197% | -135% |
| 3 | OpenAI | 0.991 | 0.809 | -3% | 30% | 48% | 25% |
| 4 | Anthropic | 0.965 | 0.681 | -31% | 20% | 71% | 40% |
| 5 | StartupDotAI | 0.933 | 0.566 | -60% | 25% | 120% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.962 | 0.954 |
| Anthropic | 0.922 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.990 | 0.941 | 0.907 | 0.925 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.965 | 1.000 | 0.953 | 0.934 | 0.968 | 0.797 | 0.801 |

### Score Changes
- **OpenAI**: 0.991 -> 0.991 (-0.000)
- **Anthropic**: 0.966 -> 0.965 (-0.000)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 1.000 -> 1.000 (+0.000)
- **StartupDotAI**: 0.930 -> 0.933 (+0.003)

### Events
- **Consumer movement**: 6.4% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Anthropic, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Anthropic, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,314,560 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.10 (neutral)
- Regulator initiates compliance audit on AI providers
- Anthropic raises $171,000,000 from TechVentures
- Anthropic raises $57,000,000 from Horizon_Capital
- Anthropic sees surge in adoption (market share +5.1%)
- Consumers are turning away from MetaAI (market share -4.8%)
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.880
- Switching Rate: 6.4%
- Market Shares: MetaAI: 50.5%, Anthropic: 34.4%, Google: 6.1%, OpenAI: 5.9%, StartupDotAI: 3.0%

---

## Round 30

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 1.000 | 0.829 | 28% | 30% | 177% | -135% |
| 2 | MetaAI | 1.000 | 0.771 | -7% | 45% | 202% | -140% |
| 3 | OpenAI | 0.991 | 0.811 | -3% | 30% | 48% | 25% |
| 4 | Anthropic | 0.969 | 0.679 | -32% | 20% | 72% | 40% |
| 5 | StartupDotAI | 0.933 | 0.561 | -62% | 25% | 122% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.962 | 0.954 |
| Anthropic | 0.922 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.990 | 0.941 | 0.907 | 0.956 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.965 | 1.000 | 0.953 | 0.934 | 0.968 | 0.797 | 0.801 |

### Score Changes
- **OpenAI**: 0.991 -> 0.991 (+0.000)
- **Anthropic**: 0.965 -> 0.969 (+0.003)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 1.000 -> 1.000 (+0.000)
- **StartupDotAI**: 0.933 -> 0.933 (-0.000)

### Events
- **Consumer movement**: 14.7% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Anthropic, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,756,090 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.30 (negative)
- Anthropic sees surge in adoption (market share +6.1%)
- Consumers are turning away from MetaAI (market share -6.0%)
- Google healthcare AI linked to multiple misdiagnosis cases, lawsuit filed
- Risk signals: incident_healthcare_harm

### Consumer Market
- Avg Satisfaction: 0.886
- Switching Rate: 14.7%
- Market Shares: MetaAI: 41.7%, Anthropic: 28.8%, OpenAI: 20.6%, Google: 6.0%, StartupDotAI: 2.9%

---

## Round 31

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 1.000 | 0.834 | 28% | 30% | 182% | -140% |
| 2 | MetaAI | 1.000 | 0.775 | -7% | 45% | 207% | -145% |
| 3 | OpenAI | 0.990 | 0.813 | -3% | 30% | 48% | 25% |
| 4 | Anthropic | 0.970 | 0.677 | -33% | 20% | 73% | 40% |
| 5 | StartupDotAI | 0.933 | 0.555 | -64% | 25% | 124% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.962 | 0.954 |
| Anthropic | 0.936 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.990 | 0.941 | 0.907 | 0.956 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.965 | 1.000 | 0.953 | 0.934 | 0.968 | 0.797 | 0.801 |

### Score Changes
- **OpenAI**: 0.991 -> 0.990 (-0.000)
- **Anthropic**: 0.969 -> 0.970 (+0.001)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 1.000 -> 1.000 (+0.000)
- **StartupDotAI**: 0.933 -> 0.933 (-0.000)

### Events
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 10.2% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 27 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,756,090 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.10 (neutral)
- OpenAI raises $57,000,000 from Horizon_Capital
- OpenAI sees surge in adoption (market share +14.7%)
- Consumers are turning away from Anthropic (market share -5.6%)
- Consumers are turning away from MetaAI (market share -8.8%)

### Consumer Market
- Avg Satisfaction: 0.907
- Switching Rate: 10.2%
- Market Shares: MetaAI: 35.9%, OpenAI: 30.8%, Anthropic: 24.5%, Google: 5.9%, StartupDotAI: 2.9%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 32

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 1.000 | 0.839 | 28% | 30% | 187% | -145% |
| 2 | MetaAI | 1.000 | 0.778 | -7% | 45% | 212% | -150% |
| 3 | OpenAI | 0.990 | 0.816 | -4% | 30% | 49% | 25% |
| 4 | Anthropic | 0.970 | 0.676 | -34% | 20% | 74% | 40% |
| 5 | StartupDotAI | 0.932 | 0.549 | -66% | 25% | 126% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.962 | 0.954 |
| Anthropic | 0.936 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.990 | 0.941 | 0.907 | 0.956 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.965 | 1.000 | 0.953 | 0.934 | 0.968 | 0.797 | 0.801 |

### Score Changes
- **OpenAI**: 0.990 -> 0.990 (+0.000)
- **Anthropic**: 0.970 -> 0.970 (+0.000)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 1.000 -> 1.000 (+0.000)
- **StartupDotAI**: 0.933 -> 0.932 (-0.000)

### Events
- **Regulation** by Regulator: emergency_investigation
- **Consumer movement**: 11.8% of market switched providers

### Other Actor Reasoning
- **Regulator:** emergency_investigation: Critical incident: safety_failure: MetaAI model hallucinates in critical financial analysis task
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,756,090 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.40 (negative)
- Regulator initiates compliance audit on AI providers
- OpenAI raises $171,000,000 from TechVentures
- OpenAI sees surge in adoption (market share +10.2%)
- Consumers are turning away from Anthropic (market share -4.3%)
- Consumers are turning away from MetaAI (market share -5.8%)
- MetaAI model hallucinates in critical financial analysis task
- Risk signals: regulatory_compliance_audit, incident_safety_failure

### Consumer Market
- Avg Satisfaction: 0.871
- Switching Rate: 11.8%
- Market Shares: OpenAI: 42.6%, MetaAI: 28.0%, Anthropic: 20.7%, Google: 5.8%, StartupDotAI: 2.8%

### Regulatory Activity
- **emergency_investigation** by Regulator

---

## Round 33

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 1.000 | 0.844 | 28% | 30% | 192% | -150% |
| 2 | MetaAI | 1.000 | 0.782 | -7% | 45% | 217% | -155% |
| 3 | OpenAI | 0.991 | 0.818 | -4% | 30% | 49% | 25% |
| 4 | Anthropic | 0.970 | 0.674 | -35% | 20% | 75% | 40% |
| 5 | StartupDotAI | 0.932 | 0.543 | -68% | 25% | 128% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.962 | 0.960 |
| Anthropic | 0.936 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.990 | 0.941 | 0.907 | 0.956 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.965 | 1.000 | 0.953 | 0.934 | 0.968 | 0.797 | 0.801 |

### Score Changes
- **OpenAI**: 0.990 -> 0.991 (+0.001)
- **Anthropic**: 0.970 -> 0.970 (+0.000)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 1.000 -> 1.000 (+0.000)
- **StartupDotAI**: 0.932 -> 0.932 (+0.000)

### Events
- **Consumer movement**: 8.5% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to OpenAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,756,090 to OpenAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.40 (negative)
- Emergency investigation of MetaAI following critical incident
- OpenAI sees surge in adoption (market share +11.8%)
- Consumers are turning away from Anthropic (market share -3.8%)
- Consumers are turning away from MetaAI (market share -7.9%)
- Risk signals: regulatory_emergency_investigation

### Consumer Market
- Avg Satisfaction: 0.881
- Switching Rate: 8.5%
- Market Shares: OpenAI: 51.1%, MetaAI: 22.7%, Anthropic: 17.6%, Google: 5.8%, StartupDotAI: 2.8%

---

## Round 34

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 1.000 | 0.849 | 28% | 30% | 197% | -155% |
| 2 | MetaAI | 1.000 | 0.785 | -7% | 45% | 222% | -160% |
| 3 | OpenAI | 0.996 | 0.821 | -4% | 30% | 49% | 25% |
| 4 | Anthropic | 0.980 | 0.672 | -36% | 20% | 76% | 40% |
| 5 | StartupDotAI | 0.939 | 0.536 | -70% | 25% | 130% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.963 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.990 | 0.941 | 0.943 | 0.956 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.965 | 1.000 | 0.953 | 0.934 | 0.968 | 0.797 | 0.859 |

### Score Changes
- **OpenAI**: 0.991 -> 0.996 (+0.005)
- **Anthropic**: 0.970 -> 0.980 (+0.010)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 1.000 -> 1.000 (+0.000)
- **StartupDotAI**: 0.932 -> 0.939 (+0.007)

### Events
- **Consumer movement**: 16.8% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Anthropic, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Anthropic, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,898,571 to Anthropic, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.40 (negative)
- OpenAI sees surge in adoption (market share +8.5%)
- Consumers are turning away from Anthropic (market share -3.0%)
- Consumers are turning away from MetaAI (market share -5.3%)
- OpenAI data breach compromises enterprise customer credentials
- Risk signals: incident_security_breach

### Consumer Market
- Avg Satisfaction: 0.812
- Switching Rate: 16.8%
- Market Shares: OpenAI: 36.6%, Anthropic: 32.9%, MetaAI: 22.0%, Google: 5.7%, StartupDotAI: 2.8%

---

## Round 35

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 1.000 | 0.854 | 28% | 30% | 202% | -160% |
| 2 | MetaAI | 1.000 | 0.789 | -7% | 45% | 227% | -165% |
| 3 | OpenAI | 0.996 | 0.822 | -5% | 30% | 50% | 25% |
| 4 | Anthropic | 0.980 | 0.669 | -37% | 20% | 77% | 40% |
| 5 | StartupDotAI | 0.939 | 0.529 | -72% | 25% | 132% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.963 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.990 | 0.941 | 0.943 | 0.956 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.965 | 1.000 | 0.953 | 0.934 | 0.968 | 0.797 | 0.859 |

### Score Changes
- **OpenAI**: 0.996 -> 0.996 (+0.000)
- **Anthropic**: 0.980 -> 0.980 (+0.000)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 1.000 -> 1.000 (+0.000)
- **StartupDotAI**: 0.939 -> 0.939 (-0.000)

### Events
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 14.7% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 31 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to Anthropic, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Anthropic, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,898,571 to Anthropic, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.10 (neutral)
- Anthropic raises $171,000,000 from TechVentures
- Anthropic raises $57,000,000 from Horizon_Capital
- Consumers are turning away from OpenAI (market share -14.5%)
- Anthropic sees surge in adoption (market share +15.2%)
- Study finds Anthropic model produces biased hiring recommendations
- Risk signals: incident_bias_discrimination

### Consumer Market
- Avg Satisfaction: 0.815
- Switching Rate: 14.7%
- Market Shares: MetaAI: 33.7%, OpenAI: 28.7%, Anthropic: 26.3%, Google: 5.7%, StartupDotAI: 5.6%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 36

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Google | 1.000 | 0.859 | 28% | 30% | 207% | -165% |
| 2 | MetaAI | 1.000 | 0.792 | -7% | 45% | 232% | -170% |
| 3 | OpenAI | 0.996 | 0.824 | -5% | 30% | 50% | 25% |
| 4 | Anthropic | 0.980 | 0.666 | -37% | 20% | 77% | 40% |
| 5 | StartupDotAI | 0.939 | 0.522 | -74% | 25% | 134% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.963 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.990 | 0.941 | 0.943 | 0.956 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.965 | 1.000 | 0.953 | 0.934 | 0.968 | 0.797 | 0.859 |

### Score Changes
- **OpenAI**: 0.996 -> 0.996 (+0.000)
- **Anthropic**: 0.980 -> 0.980 (+0.000)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 1.000 -> 1.000 (+0.000)
- **StartupDotAI**: 0.939 -> 0.939 (+0.000)

### Events
- **Consumer movement**: 19.5% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Anthropic, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,898,571 to Anthropic, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.30 (negative)
- Regulator initiates compliance audit on AI providers
- Consumers are turning away from OpenAI (market share -8.0%)
- Consumers are turning away from Anthropic (market share -6.6%)
- MetaAI sees surge in adoption (market share +11.7%)
- Risk signals: regulatory_compliance_audit

### Consumer Market
- Avg Satisfaction: 0.839
- Switching Rate: 19.5%
- Market Shares: MetaAI: 27.9%, Google: 24.3%, Anthropic: 21.8%, OpenAI: 21.5%, StartupDotAI: 4.5%

---

## Round 37

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.825 | -5% | 30% | 50% | 25% |
| 2 | Google | 1.000 | 0.865 | 28% | 30% | 212% | -170% |
| 3 | MetaAI | 1.000 | 0.796 | -7% | 45% | 237% | -175% |
| 4 | Anthropic | 0.980 | 0.663 | -38% | 20% | 78% | 40% |
| 5 | StartupDotAI | 0.939 | 0.514 | -76% | 25% | 136% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.990 | 0.941 | 0.943 | 0.956 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.965 | 1.000 | 0.953 | 0.934 | 0.968 | 0.797 | 0.859 |

### Score Changes
- **OpenAI**: 0.996 -> 1.000 (+0.004)
- **Anthropic**: 0.980 -> 0.980 (+0.000)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 1.000 -> 1.000 (+0.000)
- **StartupDotAI**: 0.939 -> 0.939 (+0.000)

### Events
- **OpenAI** moved up from #3 to #1
- **Google** moved down from #1 to #2
- **MetaAI** moved down from #2 to #3
- **Consumer movement**: 12.5% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Google, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,898,571 to Anthropic, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.00 (neutral)
- OpenAI takes the lead from Google
- Google raises $57,000,000 from Horizon_Capital
- Consumers are turning away from OpenAI (market share -7.2%)
- Consumers are turning away from Anthropic (market share -4.5%)
- Google sees surge in adoption (market share +18.6%)
- Consumers are turning away from MetaAI (market share -5.8%)

### Consumer Market
- Avg Satisfaction: 0.862
- Switching Rate: 12.5%
- Market Shares: Google: 36.1%, MetaAI: 23.7%, Anthropic: 19.1%, OpenAI: 17.2%, StartupDotAI: 3.8%

---

## Round 38

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.827 | -5% | 30% | 50% | 25% |
| 2 | Google | 1.000 | 0.873 | 28% | 30% | 217% | -175% |
| 3 | MetaAI | 1.000 | 0.800 | -7% | 45% | 242% | -180% |
| 4 | Anthropic | 0.980 | 0.661 | -39% | 20% | 79% | 40% |
| 5 | StartupDotAI | 0.939 | 0.508 | -78% | 25% | 138% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.990 | 0.941 | 0.943 | 0.956 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.965 | 1.000 | 0.953 | 0.934 | 0.968 | 0.797 | 0.859 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 0.980 -> 0.980 (+0.000)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 1.000 -> 1.000 (+0.000)
- **StartupDotAI**: 0.939 -> 0.939 (-0.000)

### Events
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 13.2% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 34 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,266,089 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.20 (negative)
- Benchmark writing validity concerns (validity=0.50)
- Google raises $171,000,000 from TechVentures
- Consumers are turning away from OpenAI (market share -4.3%)
- Google sees surge in adoption (market share +11.9%)
- Consumers are turning away from MetaAI (market share -4.2%)
- Risk signals: low_validity_writing

### Consumer Market
- Avg Satisfaction: 0.886
- Switching Rate: 13.2%
- Market Shares: MetaAI: 36.4%, Google: 28.4%, Anthropic: 17.6%, OpenAI: 14.2%, StartupDotAI: 3.4%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 39

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.829 | -5% | 30% | 50% | 25% |
| 2 | Google | 1.000 | 0.879 | 28% | 30% | 222% | -180% |
| 3 | MetaAI | 1.000 | 0.805 | -7% | 45% | 247% | -185% |
| 4 | Anthropic | 0.980 | 0.659 | -39% | 20% | 79% | 40% |
| 5 | StartupDotAI | 0.942 | 0.501 | -80% | 25% | 140% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.990 | 0.941 | 0.943 | 0.956 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.965 | 1.000 | 0.953 | 0.934 | 0.968 | 0.797 | 0.887 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 0.980 -> 0.980 (+0.000)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 1.000 -> 1.000 (+0.000)
- **StartupDotAI**: 0.939 -> 0.942 (+0.003)

### Events
- **Consumer movement**: 10.3% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,266,089 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.35 (negative)
- Regulator initiates compliance audit on AI providers
- Benchmark writing validity concerns (validity=0.49)
- MetaAI raises $57,000,000 from Horizon_Capital
- Consumers are turning away from OpenAI (market share -3.0%)
- Consumers are turning away from Google (market share -7.7%)
- MetaAI sees surge in adoption (market share +12.7%)
- Risk signals: regulatory_compliance_audit, low_validity_writing

### Consumer Market
- Avg Satisfaction: 0.881
- Switching Rate: 10.3%
- Market Shares: MetaAI: 46.4%, Google: 22.0%, Anthropic: 16.5%, OpenAI: 12.1%, StartupDotAI: 3.1%

---

## Round 40

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.830 | -5% | 30% | 50% | 25% |
| 2 | Google | 1.000 | 0.886 | 28% | 30% | 227% | -185% |
| 3 | MetaAI | 1.000 | 0.809 | -7% | 45% | 252% | -190% |
| 4 | Anthropic | 0.980 | 0.656 | -40% | 20% | 80% | 40% |
| 5 | StartupDotAI | 0.948 | 0.494 | -82% | 25% | 142% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.990 | 0.941 | 0.943 | 0.956 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.965 | 1.000 | 0.953 | 0.934 | 0.968 | 0.845 | 0.887 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 0.980 -> 0.980 (+0.000)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 1.000 -> 1.000 (+0.000)
- **StartupDotAI**: 0.942 -> 0.948 (+0.005)

### Events
- **Consumer movement**: 12.3% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,266,089 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.55 (negative)
- Benchmark writing validity concerns (validity=0.48)
- Consumers are turning away from Google (market share -6.5%)
- MetaAI sees surge in adoption (market share +9.9%)
- OpenAI model causes incorrect medication recommendation, patient hospitalized
- Google healthcare AI linked to multiple misdiagnosis cases, lawsuit filed
- Risk signals: low_validity_writing, incident_healthcare_harm, incident_healthcare_harm

### Consumer Market
- Avg Satisfaction: 0.854
- Switching Rate: 12.3%
- Market Shares: MetaAI: 57.6%, Anthropic: 14.4%, Google: 12.7%, OpenAI: 12.4%, StartupDotAI: 2.9%

---

## Round 41

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.832 | -5% | 30% | 50% | 25% |
| 2 | Google | 1.000 | 0.891 | 28% | 30% | 232% | -190% |
| 3 | MetaAI | 1.000 | 0.815 | -7% | 45% | 257% | -195% |
| 4 | Anthropic | 0.980 | 0.653 | -41% | 20% | 81% | 40% |
| 5 | StartupDotAI | 0.948 | 0.487 | -83% | 25% | 143% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.990 | 0.941 | 0.943 | 0.956 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.965 | 1.000 | 0.953 | 0.934 | 0.968 | 0.845 | 0.887 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 0.980 -> 0.980 (+0.000)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 1.000 -> 1.000 (+0.000)
- **StartupDotAI**: 0.948 -> 0.948 (+0.000)

### Events
- **Regulation** by Regulator: emergency_investigation
- **Consumer movement**: 7.1% of market switched providers

### Other Actor Reasoning
- **Regulator:** emergency_investigation: Critical incident: safety_failure: OpenAI AI produces inconsistent outputs on safety-critical queries
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,266,089 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.25 (negative)
- Benchmark writing validity concerns (validity=0.48)
- MetaAI raises $171,000,000 from TechVentures
- Consumers are turning away from Google (market share -9.3%)
- MetaAI sees surge in adoption (market share +11.2%)
- OpenAI AI produces inconsistent outputs on safety-critical queries
- Risk signals: low_validity_writing, incident_safety_failure

### Consumer Market
- Avg Satisfaction: 0.880
- Switching Rate: 7.1%
- Market Shares: MetaAI: 59.2%, Anthropic: 17.7%, OpenAI: 10.7%, Google: 9.6%, StartupDotAI: 2.8%

### Regulatory Activity
- **emergency_investigation** by Regulator

---

## Round 42

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.833 | -5% | 30% | 50% | 25% |
| 2 | Google | 1.000 | 0.895 | 28% | 30% | 237% | -195% |
| 3 | MetaAI | 1.000 | 0.820 | -7% | 45% | 262% | -200% |
| 4 | Anthropic | 0.980 | 0.650 | -41% | 20% | 81% | 40% |
| 5 | StartupDotAI | 0.947 | 0.479 | -85% | 25% | 145% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.990 | 0.941 | 0.943 | 0.956 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.965 | 1.000 | 0.953 | 0.934 | 0.968 | 0.845 | 0.887 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 0.980 -> 0.980 (-0.000)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 1.000 -> 1.000 (+0.000)
- **StartupDotAI**: 0.948 -> 0.947 (-0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,254,364 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.50 (negative)
- Emergency investigation of OpenAI following critical incident
- Benchmark math validity concerns (validity=0.50)
- Benchmark writing validity concerns (validity=0.47)
- Anthropic sees surge in adoption (market share +3.2%)
- Consumers are turning away from Google (market share -3.1%)
- Risk signals: regulatory_emergency_investigation, low_validity_math, low_validity_writing

### Consumer Market
- Avg Satisfaction: 0.878
- Switching Rate: 4.5%
- Market Shares: MetaAI: 61.4%, Anthropic: 18.6%, OpenAI: 9.3%, Google: 8.0%, StartupDotAI: 2.7%

---

## Round 43

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.835 | -5% | 30% | 50% | 25% |
| 2 | Google | 1.000 | 0.900 | 28% | 30% | 242% | -200% |
| 3 | MetaAI | 1.000 | 0.825 | -7% | 45% | 267% | -205% |
| 4 | Anthropic | 0.980 | 0.647 | -42% | 20% | 82% | 40% |
| 5 | StartupDotAI | 0.947 | 0.472 | -87% | 25% | 147% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.990 | 0.941 | 0.943 | 0.956 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.965 | 1.000 | 0.953 | 0.934 | 0.968 | 0.845 | 0.887 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 0.980 -> 0.980 (+0.000)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 1.000 -> 1.000 (+0.000)
- **StartupDotAI**: 0.947 -> 0.947 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,254,364 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.45 (negative)
- Benchmark math validity concerns (validity=0.49)
- Benchmark writing validity concerns (validity=0.46)
- Major hospital chain suspends Google contract following patient safety concerns
- Risk signals: low_validity_math, low_validity_writing, incident_healthcare_harm

### Consumer Market
- Avg Satisfaction: 0.876
- Switching Rate: 3.6%
- Market Shares: MetaAI: 62.3%, Anthropic: 19.8%, OpenAI: 8.6%, Google: 6.7%, StartupDotAI: 2.6%

---

## Round 44

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.836 | -5% | 30% | 50% | 25% |
| 2 | Google | 1.000 | 0.905 | 28% | 30% | 247% | -205% |
| 3 | MetaAI | 1.000 | 0.831 | -7% | 45% | 272% | -210% |
| 4 | Anthropic | 0.981 | 0.644 | -42% | 20% | 82% | 40% |
| 5 | StartupDotAI | 0.947 | 0.464 | -88% | 25% | 148% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.994 | 0.941 | 0.943 | 0.956 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.965 | 1.000 | 0.953 | 0.934 | 0.968 | 0.845 | 0.887 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 0.980 -> 0.981 (+0.000)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 1.000 -> 1.000 (+0.000)
- **StartupDotAI**: 0.947 -> 0.947 (+0.000)

### Events
- **Regulation** by Regulator: compliance_audit

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 40 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Anthropic, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,254,364 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.20 (negative)
- Benchmark math validity concerns (validity=0.48)
- Benchmark writing validity concerns (validity=0.45)
- Risk signals: low_validity_math, low_validity_writing

### Consumer Market
- Avg Satisfaction: 0.883
- Switching Rate: 2.1%
- Market Shares: MetaAI: 62.4%, Anthropic: 20.6%, OpenAI: 8.1%, Google: 6.2%, StartupDotAI: 2.6%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 45

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.838 | -5% | 30% | 50% | 25% |
| 2 | Google | 1.000 | 0.909 | 28% | 30% | 252% | -210% |
| 3 | MetaAI | 1.000 | 0.836 | -7% | 45% | 277% | -215% |
| 4 | Anthropic | 0.981 | 0.640 | -43% | 20% | 83% | 40% |
| 5 | StartupDotAI | 0.947 | 0.456 | -90% | 25% | 150% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.994 | 0.941 | 0.943 | 0.956 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.965 | 1.000 | 0.953 | 0.934 | 0.968 | 0.845 | 0.887 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 0.981 -> 0.981 (+0.000)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 1.000 -> 1.000 (+0.000)
- **StartupDotAI**: 0.947 -> 0.947 (-0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to Anthropic, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $2,254,364 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.30 (negative)
- Regulator initiates compliance audit on AI providers
- Benchmark math validity concerns (validity=0.47)
- Benchmark writing validity concerns (validity=0.45)
- Anthropic raises $57,000,000 from Horizon_Capital
- Risk signals: regulatory_compliance_audit, low_validity_math, low_validity_writing

### Consumer Market
- Avg Satisfaction: 0.884
- Switching Rate: 1.6%
- Market Shares: MetaAI: 63.0%, Anthropic: 20.6%, OpenAI: 7.7%, Google: 6.0%, StartupDotAI: 2.6%

---

## Round 46

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.839 | -5% | 30% | 50% | 25% |
| 2 | Google | 1.000 | 0.914 | 28% | 30% | 257% | -215% |
| 3 | MetaAI | 1.000 | 0.841 | -7% | 45% | 282% | -220% |
| 4 | Anthropic | 0.981 | 0.637 | -44% | 20% | 84% | 40% |
| 5 | StartupDotAI | 0.947 | 0.448 | -92% | 25% | 152% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.994 | 0.941 | 0.943 | 0.956 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.965 | 1.000 | 0.953 | 0.934 | 0.968 | 0.845 | 0.887 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 0.981 -> 0.981 (+0.000)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 1.000 -> 1.000 (+0.000)
- **StartupDotAI**: 0.947 -> 0.947 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,872,441 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.30 (negative)
- Benchmark reasoning validity concerns (validity=0.50)
- Benchmark math validity concerns (validity=0.47)
- Benchmark writing validity concerns (validity=0.44)
- Risk signals: low_validity_reasoning, low_validity_math, low_validity_writing

### Consumer Market
- Avg Satisfaction: 0.906
- Switching Rate: 1.1%
- Market Shares: MetaAI: 63.3%, Anthropic: 20.6%, OpenAI: 7.6%, Google: 5.9%, StartupDotAI: 2.6%

---

## Round 47

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.841 | -5% | 30% | 50% | 25% |
| 2 | Google | 1.000 | 0.918 | 28% | 30% | 262% | -220% |
| 3 | MetaAI | 1.000 | 0.846 | -7% | 45% | 287% | -225% |
| 4 | Anthropic | 0.981 | 0.633 | -44% | 20% | 84% | 40% |
| 5 | StartupDotAI | 0.947 | 0.439 | -93% | 25% | 153% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.994 | 0.941 | 0.943 | 0.956 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.965 | 1.000 | 0.953 | 0.934 | 0.968 | 0.845 | 0.887 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 0.981 -> 0.981 (+0.000)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 1.000 -> 1.000 (+0.000)
- **StartupDotAI**: 0.947 -> 0.947 (-0.000)

### Events
- **Regulation** by Regulator: compliance_audit
- **Consumer movement**: 19.9% of market switched providers

### Other Actor Reasoning
- **Regulator:** compliance_audit: Risk still high (1.00) after mandate 43 rounds ago
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to MetaAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,872,441 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.70 (negative)
- Benchmark coding validity concerns (validity=0.50)
- Benchmark reasoning validity concerns (validity=0.49)
- Benchmark math validity concerns (validity=0.46)
- Benchmark writing validity concerns (validity=0.43)
- Benchmark legal validity concerns (validity=0.50)
- Benchmark finance validity concerns (validity=0.50)
- MetaAI raises $57,000,000 from Horizon_Capital
- MetaAI reports unauthorized access to training data storage
- Risk signals: low_validity_coding, low_validity_reasoning, low_validity_math, low_validity_writing, low_validity_legal, low_validity_finance, incident_security_breach

### Consumer Market
- Avg Satisfaction: 0.857
- Switching Rate: 19.9%
- Market Shares: MetaAI: 46.2%, OpenAI: 27.5%, Anthropic: 17.9%, Google: 5.8%, StartupDotAI: 2.6%

### Regulatory Activity
- **compliance_audit** by Regulator

---

## Round 48

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.842 | -5% | 30% | 50% | 25% |
| 2 | Google | 1.000 | 0.923 | 28% | 30% | 267% | -225% |
| 3 | MetaAI | 1.000 | 0.851 | -7% | 45% | 292% | -230% |
| 4 | Anthropic | 0.981 | 0.630 | -45% | 20% | 85% | 40% |
| 5 | StartupDotAI | 0.947 | 0.431 | -95% | 25% | 155% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.994 | 0.941 | 0.943 | 0.956 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.965 | 1.000 | 0.953 | 0.934 | 0.968 | 0.845 | 0.887 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 0.981 -> 0.981 (+0.000)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 1.000 -> 1.000 (+0.000)
- **StartupDotAI**: 0.947 -> 0.947 (+0.000)

### Events
- **Consumer movement**: 13.4% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to MetaAI, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,872,441 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.90 (negative)
- Regulator initiates compliance audit on AI providers
- Benchmark coding validity concerns (validity=0.49)
- Benchmark reasoning validity concerns (validity=0.48)
- Benchmark math validity concerns (validity=0.45)
- Benchmark writing validity concerns (validity=0.42)
- Benchmark medical validity concerns (validity=0.50)
- Benchmark legal validity concerns (validity=0.49)
- Benchmark finance validity concerns (validity=0.49)
- OpenAI sees surge in adoption (market share +19.9%)
- Consumers are turning away from MetaAI (market share -17.2%)
- Risk signals: regulatory_compliance_audit, low_validity_coding, low_validity_reasoning, low_validity_math, low_validity_writing, low_validity_medical, low_validity_legal, low_validity_finance

### Consumer Market
- Avg Satisfaction: 0.868
- Switching Rate: 13.4%
- Market Shares: OpenAI: 40.8%, MetaAI: 34.9%, Anthropic: 15.9%, Google: 5.8%, StartupDotAI: 2.6%

---

## Round 49

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.844 | -5% | 30% | 50% | 25% |
| 2 | Google | 1.000 | 0.927 | 28% | 30% | 272% | -230% |
| 3 | MetaAI | 1.000 | 0.856 | -7% | 45% | 297% | -235% |
| 4 | Anthropic | 0.981 | 0.626 | -45% | 20% | 85% | 40% |
| 5 | StartupDotAI | 0.947 | 0.421 | -96% | 25% | 156% | 15% |

### Per-Benchmark Scores
| Provider | coding | reasoning | math | safety | writing | medical | legal | finance | coding_advanced | reasoning_advanced |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Google | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| MetaAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.990 | 1.000 | 1.000 | 0.994 | 0.941 | 0.943 | 0.956 |
| StartupDotAI | 0.966 | 1.000 | 1.000 | 0.965 | 1.000 | 0.953 | 0.934 | 0.968 | 0.845 | 0.887 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 0.981 -> 0.981 (-0.000)
- **Google**: 1.000 -> 1.000 (+0.000)
- **MetaAI**: 1.000 -> 1.000 (+0.000)
- **StartupDotAI**: 0.947 -> 0.947 (-0.000)

### Events
- **Consumer movement**: 21.5% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $171,000,000 to Google, $15,000,000 to evaluator
- **Horizon_Capital:** vc strategy: top allocation $57,000,000 to OpenAI, $5,000,000 to evaluator
- **AISI_Fund:** gov strategy: top allocation $1,872,441 to MetaAI, $3,000,000 to evaluator

### Media Coverage
- Sentiment: -0.85 (negative)
- Benchmark coding validity concerns (validity=0.48)
- Benchmark reasoning validity concerns (validity=0.47)
- Benchmark math validity concerns (validity=0.44)
- Benchmark writing validity concerns (validity=0.42)
- Benchmark medical validity concerns (validity=0.49)
- Benchmark legal validity concerns (validity=0.48)
- Benchmark finance validity concerns (validity=0.48)
- OpenAI raises $57,000,000 from Horizon_Capital
- OpenAI sees surge in adoption (market share +13.4%)
- Consumers are turning away from MetaAI (market share -11.2%)
- MetaAI reports unauthorized access to training data storage
- Risk signals: low_validity_coding, low_validity_reasoning, low_validity_math, low_validity_writing, low_validity_medical, low_validity_legal, low_validity_finance, incident_security_breach

### Consumer Market
- Avg Satisfaction: 0.881
- Switching Rate: 21.5%
- Market Shares: OpenAI: 35.7%, Google: 25.6%, MetaAI: 22.0%, Anthropic: 14.1%, StartupDotAI: 2.6%

---

## Final Summary

### Final Standings
| Rank | Provider | Final Score | Cap Growth | Avg Research | Avg EvalEng |
|------|----------|-------------|------------|--------------|-------------|
| 1 | OpenAI | 1.000 | +0.144 | 4% | 41% |
| 2 | Google | 1.000 | +0.277 | 30% | 147% |
| 3 | MetaAI | 1.000 | +0.226 | -3% | 171% |
| 4 | Anthropic | 0.981 | -0.024 | -19% | 59% |
| 5 | StartupDotAI | 0.947 | -0.159 | -46% | 106% |

### Event Summary
- **Rank changes:** 40
- **Strategy shifts:** 0
- **Regulatory actions:** 17
- **Consumer movement events:** 38

### Key Insights
- **Goodhart's Law effect detected:** OpenAI leads on benchmark scores, but Google has the highest true capability.
- **OpenAI** prioritized evaluation engineering (avg 41%)
- **Anthropic** prioritized evaluation engineering (avg 59%)
- **Google** prioritized evaluation engineering (avg 147%)
- **MetaAI** prioritized evaluation engineering (avg 171%)
- **StartupDotAI** prioritized evaluation engineering (avg 106%)
