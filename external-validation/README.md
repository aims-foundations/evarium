# External Validation Pipeline

Compares qualitative behavior of the simulation against real-world AI benchmark
and market share data.  The goal is **shape matching** — rate of improvement,
saturation timing, leader-change dynamics — not absolute value reproduction.

---

## Folder Structure

```
validation/
├── data/
│   ├── raw/
│   │   ├── paperwithcode/   ← fetch_pwc.py output
│   │   ├── helm/            ← fetch_helm.py output
│   │   └── market/          ← fetch_market.py output + manual SO survey CSVs
│   └── processed/
│       ├── benchmarks.csv       real data, normalized
│       ├── market_share.csv     real data, normalized
│       ├── sim_benchmarks.csv   sim data (from sim_export.py)
│       ├── sim_market.csv
│       └── sim_events.csv
├── plots/                   ← plot_validation.py output
├── scripts/
│   ├── fetch_pwc.py
│   ├── fetch_helm.py
│   ├── fetch_market.py
│   ├── normalize.py
│   └── plot_validation.py
├── sim_export.py
└── README.md  ← you are here
```

---

## Quick Start

Run all steps from the repo root:

```bash
# 1. Fetch real benchmark data
python validation/scripts/fetch_pwc.py
python validation/scripts/fetch_helm.py

# 2. Fetch market proxy data  (SimilarWeb scrape + optional SO survey)
python validation/scripts/fetch_market.py

# 3. (Optional) Download Stack Overflow survey CSVs manually:
#    https://insights.stackoverflow.com/survey
#    Save as: validation/data/raw/market/so_survey_<year>.csv
#    Then re-run:
#    python validation/scripts/fetch_market.py

# 4. Normalize everything to common schema
python validation/scripts/normalize.py

# 5. Export sim experiment data
python validation/sim_export.py exp_001
# Or multiple experiments:
# python validation/sim_export.py exp_001 exp_003

# 6. Generate plots
python validation/scripts/plot_validation.py --exp-id exp_001
# Specific benchmarks only:
# python validation/scripts/plot_validation.py --benchmarks coding_advanced math_advanced --exp-id exp_001
# Custom output dir:
# python validation/scripts/plot_validation.py --out-dir my_plots/
```

---

## Provider Mapping

| Real Company | Sim Name |
|---|---|
| OpenAI / GPT | Orion Labs |
| Anthropic / Claude | Apex AI |
| Google / DeepMind / Gemini | Genesis Systems |
| Meta / LLaMA | Mirage AI |
| DeepSeek | OpenCore |
| Mistral / Cohere / smaller | Spark AI |

---

## Benchmark Mapping

| Real Benchmark | Sim Analog | Notes |
|---|---|---|
| MMLU, HellaSwag | `writing` | General knowledge |
| HumanEval, MBPP | `coding_advanced` | Code generation |
| MATH | `math_advanced` | Math reasoning |
| GPQA, BIG-Bench Hard | `reasoning_advanced` | Hard reasoning |
| HELM runs | All | Controlled evaluator |

---

## Date → Sim Round Conversion

- Anchor: GPT-4 launch **2023-03-14 = round 0**
- 1 sim round ≈ 1 calendar quarter (91 days)
- Pre-GPT-4 data gets negative round numbers
- Formula: `round = (date − 2023-03-14) / 91 days`

---

## Outputs

### `data/processed/benchmarks.csv`
| Column | Description |
|---|---|
| `provider` | Sim provider name |
| `benchmark` | Sim benchmark analog |
| `score_norm` | Min-max normalized score [0, 1] |
| `score_raw` | Original score from source |
| `date` | ISO date string |
| `sim_round` | Estimated sim round |
| `source` | `paperswithcode` or `helm` |

### `data/processed/market_share.csv`
| Column | Description |
|---|---|
| `provider` | Sim provider name |
| `date` | ISO date string |
| `sim_round` | Estimated sim round |
| `share_estimate` | Fraction [0, 1] summing to 1 per (date, source) |
| `source` | `similarweb` or `so_survey_<year>` |

### `data/processed/sim_benchmarks.csv` / `sim_market.csv` / `sim_events.csv`
Extracted from `rounds.jsonl` by `sim_export.py`.  See that script for schema.

---

## Plots

All written to `validation/plots/` (or `--out-dir`):

| File | Description |
|---|---|
| `4panel_<benchmark>.png` | 4-panel: real bench / real market / sim bench / sim market |
| `saturation_<benchmark>.png` | Rolling improvement rate, saturation point marker |
| `rank_correlation.png` | Spearman rank corr (bench rank vs market rank) across lags |

---

## Notes & Caveats

- **SimilarWeb** scraping is fragile and may return empty values if the page
  structure changes.  Check `data/raw/market/web_traffic.csv` for `N/A` entries.
- **HELM** JSON structure varies by version.  The default version `v0.4.0` is
  used; override with `--version`.
- Provider attribution in PwC SOTA rows is imperfect — many rows are paper
  submissions without a clear company affiliation.  The provider mapping is a
  best-effort keyword match.
- The simulation uses quarterly rounds; real benchmark dates are continuous.
  The round mapping rounds to the nearest quarter, which can introduce ±1 round
  jitter in comparisons.
