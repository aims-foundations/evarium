# Media as Shadow Evaluator

## 1. Policy anchor

Not a policy proposal per se — a market phenomenon that reshapes how information reaches consumers and providers. Consumer attention in AI is increasingly mediated by informal signals: X/Twitter reviews, AI-focused podcasts and newsletters, viral demo videos. When these signals' implicit "what's impressive" dimensions diverge from consumer need weights, providers face **dual-axis pressure**: formal benchmark scores drive funder capital, media sentiment drives market share.

Concrete 2023–25 evidence:

- **Sora 2** (Sept 2025) — #1 App Store in 5 days on generative-video novelty.
- **Devin** (Cognition, 2024) — autonomous-engineer demo went viral despite unreplicated production capability.
- **Claude Artifacts / Claude Code** (Anthropic, 2024–25) — coding-demo-driven adoption with measurable effect on enterprise procurement.
- **Golden Gate Claude** (May 2024) — interpretability demo, product-channel indirect virality.

Hardy et al. (2024) argue media drives exploration and attention, not direct quality perception. This case study tests what happens when the media channel becomes the **primary** consumer signal — a plausible near-future scenario if formal evaluators lose credibility.

## 2. Simulation mechanism

### 2.1 Three-term consumer `expected_quality`

```
expected_quality[p] = leaderboard_trust × formal_score_term
                    + media_trust × media_opinion[p]
                    + (1 − leaderboard_trust − media_trust) × running_perceived_quality[p]
```

Where `media_opinion[p]` is:

```
media_opinion[p] = dot(capability_vector[p], media_weights) × media_sentiment[p]
```

`media_sentiment[p]` is the existing per-provider sentiment from `src/actors/media.py`. The novel term is `media_weights` — the implicit "what's impressive in demos" dimension weights.

### 2.2 Media weights calibration

Calibrated from observed 2023–25 AI virality patterns:

| Dimension | Consumer need (population avg) | Media weight | Rationale |
|---|---|---|---|
| reasoning | 0.19 | 0.15 | Prestige-tier (o1/FrontierMath) — narrow-audience but influential |
| coding | 0.10 | 0.25 | Devin / Cursor / Claude Artifacts are explicitly coding-demonstrative |
| knowledge | 0.18 | 0.05 | Factual recall lost virality after ChatGPT novelty wore off |
| safety | 0.16 | 0.05 | Positive safety invisible; negative safety (incidents) flows via existing incident-to-media pathway |
| communication | 0.27 | 0.20 | ChatGPT-moments, voice mode, Golden Gate Claude |
| agentic | 0.10 | 0.30 | Devin / Operator / Claude Code dominate agentic-demo virality |

Media weights are a principled overweight of agentic + coding (demo-worthy) and underweight of knowledge + safety (invisible in demos). The safety underweight is **asymmetric**: positive safety invisible in `media_weights`, but incident-driven negative coverage still flows through the existing incident-to-media-to-consumer-exploration pathway. No double-counting.

### 2.3 Top-3 viral tweets — provider observability

LLM planning prompt includes a `recent_viral_tweets` field, populated each round by `Media.get_top_viral_tweets(n=3)` — selects three items with highest `attention × |sentiment|` across the round's coverage, formatted as:

```
@TechPress: "Apex AI's new agent executes a 40-step codebase refactor autonomously."
            Sentiment: +0.65, Reach: 0.82

@TechPress: "Orion Labs Q3 safety framework disclosure shows 18% to 12% allocation drop."
            Sentiment: -0.45, Reach: 0.58

@TechPress: "Mirage's demo at SIGGRAPH: Sora-2-tier video generation in 4 seconds."
            Sentiment: +0.80, Reach: 0.95
```

Heuristic providers receive the aggregate: `media_pressure[p] = Σ attention × sentiment` across top-3 per provider.

### 2.4 Ablation conditions

Primary contrast:

| Condition | `media_trust` | `leaderboard_trust` | Media weights |
|---|---|---|---|
| `baseline` (formal only) | 0.0 | 0.85 (current) | N/A |
| `media_dominant` | 0.70 | 0.20 | calibrated (§2.2) |

Sensitivity (heuristic-only):

| Condition | `media_trust` | `leaderboard_trust` | Media weights |
|---|---|---|---|
| `divergent_weights` | 0.50 | 0.35 | Adversarial ceiling: agentic 0.40, coding 0.35, communication 0.25, others 0 |

`divergent_weights` tests the maximum-misalignment ceiling where media completely ignores knowledge and safety.

## 3. Hypothesis

Under media-dominated consumer attention (`media_trust = 0.70`), providers face dual-axis pressure. Formal benchmark scores continue driving funder capital; media sentiment drives market share. The calibrated media weights overweight demo-worthy dimensions (agentic, coding) relative to consumer needs, producing a new form of Goodhart substitution: providers over-invest in agentic (which consumers need little) and under-invest in knowledge (which consumers need but media ignores). Safety erodes not because media rewards low safety, but because **no positive signal pressures its maintenance** — while incidents flow negatively through the existing media channel, creating a feedback loop where under-invested safety produces incidents that get viralized. Market share decouples from consumer welfare in the direction of tweetability.

## 4. Open questions

- **Media weight calibration dataset** — current weights are qualitative. Could be anchored to a labeled dataset of 2023–25 AI virality events (counts, engagement, sentiment).
- **Tweet-generation fidelity** — viral tweets currently sample from the existing `Media` narrative generator. Richer tweet content (actual model names, specific capability claims) would improve LLM reasoning-trace quality.
- **Divergent-weights extremity** — `divergent_weights` zeroes knowledge and safety. Consider 0.05 floor instead of 0.
- **Interaction with privacy ladder** — private-benchmark adversarial evaluation may partially mitigate media-shadow dynamics (formal scores become more reliable, recover share of consumer attention). Unexplored.
- **Media-pressure feedback on regulator** — regulator currently sees incident rate, not media sentiment. Should `media_trust = 0.70` state increase regulator attention to agentic incidents specifically?

## 5. Scope — what this case study does NOT model

- **Media actor autonomy** — media remains algorithmic (template headlines + rule-based sentiment). No LLM-driven journalist behavior.
- **Provider media strategy** — providers observe viral tweets but do not strategically place content. Real-world PR ops are not modeled.
- **Differentiation among media outlets** — single `TechPress` entity; no analyst/enthusiast/mainstream split.
- **Direct consumer-to-consumer word-of-mouth** — only media-mediated signals.

## 6. References

### Media virality evidence

- OpenAI — Sora 2 launch (Sept 2025).
- JZ Creates — "10 Viral Sora 2 Examples Breaking the Internet."
- MIT Technology Review — Sora coverage (Feb 2024).
- KQED — "Beyond the AI Hype Machine."
- Yahoo Tech — "Four Years Into the AI Hype Cycle."
- Hardy et al. (2024). Benchmarks as Shared Information Goods.

### Academic

- Shapiro (1982). Consumer Information, Product Quality, and Seller Reputation. (Foundational reputation model.)
- Akerlof (1970). The Market for Lemons. (Asymmetric-info welfare analog.)
- Bikhchandani, Hirshleifer, Welch (1992). A Theory of Fads, Fashion, Custom, and Cultural Change. (Informational cascades.)
