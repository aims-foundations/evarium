# Analysis Methodology for LLM-Agent Simulation Runs

How to analyze runs from the evaluation ecosystem simulation. Covers quantitative aggregation, reasoning trace analysis, and the relationship between the two.

## The Aggregation Problem

Standard ABM aggregation (mean ± SE across seeds) assumes cross-seed variance is noise to be averaged out. In this simulation, that assumption fails for LLM runs due to path-dependent reasoning divergence: small early differences in LLM decisions cascade through competitor reactions, media, funders, and consumers. By round 10, two seeds with identical initial conditions can be in fundamentally different competitive landscapes. The mean across these trajectories is a statistical fiction — a trajectory nobody experienced.

This creates a tension: path dependence is the most interesting property of the LLM simulation, but it resists the aggregation methods that provide statistical power.

### Resolution: Three Uses of Multiple Seeds

Each use has different N requirements and supports different claims.

**Use 1: Structural validation.** Binary questions: does score inflation emerge? Does the market concentrate? Does safety investment respond to incidents? These are yes/no per seed. Report pass rates across seeds. N=10 gives ±15% precision; N=30 gives ±9%. The existing `check_patterns()` framework in diagnostics.py does exactly this.

Best served by heuristic runs (N=30, fully seed-controlled, cheap to run). LLM runs confirm robustness across reasoning engines but are not independent replications.

**Use 2: Outcome enumeration.** Classify runs into outcome types (who won, market structure) and report the space of possible outcomes. At N=3, you can say "the simulation produces at least 3 distinct market structures." At N=30, you can estimate outcome frequencies. The qualitative version (outcome space) is valid at small N and is often more informative than a mean — "Orion wins 70% of the time" is less useful than "three distinct pathways exist and here's what determines which one you get."

**Use 3: Divergence analysis.** For seeds that produce different outcome types, identify where trajectories diverge. This is inherently a case study — N=1 per comparison, depth over breadth. More seeds give more pairs to compare but each comparison is qualitative.

**Cross-model runs** (Claude, Qwen, Llama) are robustness checks. They share the same stochastic events (same seeds) but use different reasoning engines. They cannot be pooled for statistical power — different LLMs are not independent samples from a well-defined population. The honest framing: seeds vary the environment, models vary the reasoning. Both are sensitivity checks, neither is replication in the statistical sense.

---

## Quantitative Analysis

### Trajectory Visualization

For each metric across N seeds of the same condition:

- **N ≥ 10:** Quantile bands (median line + 10th/90th percentile shading). This shows distributional properties.
- **N = 3-9:** Spaghetti plot (all individual seed trajectories overlaid, semi-transparent). Quantile bands from <10 seeds are visually misleading — the 10th percentile of 3 values is just the minimum.
- **N = 30 (heuristic):** Quantile bands with tight confidence. This is the statistical backbone.

When comparing heuristic (N=30) vs LLM (N=3-5) trajectories, do not overlay bands — the visual contrast between tight and wide bands misleads readers into thinking LLM mode is "less stable" when really you ran fewer seeds. Instead, show them in adjacent panels with matched axes.

### Core Metrics (6 panels per condition comparison)

| Metric | Source | What it shows |
|--------|--------|---------------|
| Score-satisfaction gap | `scores[p]` - `consumer_data.provider_satisfaction[p]`, mean across providers | Goodhart signal: are benchmarks diverging from consumer experience? |
| HHI | `sum(share^2)` from `consumer_data.market_shares` | Market concentration trajectory |
| Mean safety investment | `effective_strategies[p].safety`, mean across providers | Does safety respond to incidents and regulation? |
| Consumer satisfaction | `consumer_data.avg_satisfaction` | Are consumers better off over time? |
| Cumulative incidents | Running sum from `media_data.risk_signals` (items containing "incident") | Is the ecosystem getting safer or more dangerous? |
| Score reliability | Spearman rank correlation: `scores` vs `consumer_data.provider_satisfaction` | Do benchmark rankings track actual consumer value? |

### Endpoint Aggregation

For summary tables (cross-condition comparison), compute metrics over the last 5 rounds and report:
- For heuristic (N=30): mean ± 95% CI using t-distribution
- For LLM (N=3-10): individual values or mean with explicit caveat about small N

The existing `aggregate_example.py` script handles this pipeline. The existing `plot_experiment.py --aggregate` mode handles visualization.

### Outcome Typology

Classify each run into an outcome type based on final state:
- **Market leader identity** — which provider won
- **Market structure** — HHI thresholds from antitrust literature (DOJ scale: <1500 = competitive, 1500-2500 = moderate, >2500 = concentrated; map to 0-1 scale as <0.15, 0.15-0.25, >0.25)
- **Leader pathway** — final-5-round portfolio of the leader (R&D-led vs safety-led vs product-led)

Report: "Under condition X, Y/N seeds produced outcome type A, Z/N produced outcome type B." This is a frequency distribution of outcome types, not a parameter estimate.

---

## Reasoning Trace Analysis

### Step 1: Detect Pivotal Rounds

A round is pivotal if any of the following occur for any provider:

| Event type | Trigger | Rationale |
|---|---|---|
| Allocation shift | Any portfolio lever changes by ≥ 0.05 from previous round | Strategic pivot |
| Market disruption | Any provider's market share changes by ≥ 0.03 in one round | Competitive shock |
| Incident shock | A major or critical incident occurs | Acute safety event |
| Regulatory escalation | Sanction or emergency investigation issued | High-severity intervention |

Gap crossings (score-satisfaction sign change) are excluded unless the gap magnitude exceeds 0.01 on at least one side. Tiny oscillations around zero are noise, not pivots.

Each pivotal round produces a `PivotalEvent(round, provider, event_type, details)`. Implementation: `scripts/reasoning_pipeline.py`.

### Step 2: Extract Reasoning Windows

For each pivotal event, extract:
- **Reasoning at pivot:** The provider's LLM trace from `actor_traces` at the pivotal round
- **Context before:** Traces from 2 prior rounds (what was the agent thinking before the pivot?)
- **Public state:** Leaderboard, market shares, media sentiment, risk signals, interventions

The reasoning traces are in `actor_traces` within `rounds.jsonl`. All actors (providers, funders, regulator) have traces from round 1 onward in LLM mode.

### Step 3: Divergence Analysis

For seeds within the same condition that produce different outcome types:
1. Identify the earliest round where market share trajectories begin separating (> 0.05 difference in leader share)
2. Extract reasoning windows from that round for all providers
3. Compare: what did the divergent seeds' agents reason differently about?

**Caveat on causal attribution:** LLM reasoning traces are verbal reports, not causal explanations. An agent saying "I'm targeting Orion's weakness" doesn't prove that targeting caused the outcome. Traces are evidence about what information the agent attended to, not proof of mechanism. Present as "the agent cited X as its rationale" rather than "X caused the divergence."

**Selection bias in pair comparison:** If multiple seed-pairs diverge, present either all pairs or establish a systematic selection criterion (e.g., always compare most-concentrated vs least-concentrated outcome). Acknowledge the selection explicitly.

### What Traces Cannot Do

- They cannot establish causation (only correlation between stated reasoning and observed behavior)
- They cannot prove emergence (the agent might follow its initialization prompt through a long chain of plausible-sounding reasoning)
- They are not faithful in the ML sense — the LLM's stated reasons may not reflect the actual input features that drove the output
- Funder traces largely reflect initialization (VC chases returns because it was told to). Interesting funder behavior is when a funder *deviates* from type, which should be rare

---

## Visualization

**Figure A — Trajectory plots (quantitative layer):**
Per-metric trajectory across rounds. Spaghetti (LLM, small N) or quantile bands (heuristic, large N). Pivotal events can be overlaid as colored markers.

**Figure B — Reasoning timeline (qualitative layer):**
For a single run, plot pivotal events as colored markers on the trajectory time axis. Color = event type. Shows *when* the interesting decisions happened.

**Figure C — Outcome type frequency table (cross-condition):**
Rows = conditions, columns = outcome types. Cell = count of seeds. Shows at a glance which conditions produce which market structures.

**Figure D — Divergence case study (deep dive):**
Side-by-side trajectories of two divergent seeds, with the branching point marked and reasoning excerpts annotated. The bridge between quantitative and qualitative layers.
