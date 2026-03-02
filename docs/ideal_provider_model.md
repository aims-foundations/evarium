# Ideal Model Provider: Action Space and Architecture
*North star document — describes the conceptually grounded model we are working toward. Not a description of current implementation.*

---

## Core Claim

A model provider is not a benchmark-score maximizer. It is an organization trying to sustain a business by building products that win in competitive markets, subject to capital constraints, regulatory requirements, and talent dynamics. Benchmark scores are instruments, not goals. A simulation that treats providers as score-maximizers will model gaming as a portfolio choice rather than as a rational response to market conditions — which is the circular reasoning problem.

---

## What Providers Actually Want (Objective Function)

In rough priority order:

1. **Revenue and market position** — sustaining the business, justifying valuations to funders, winning enterprise contracts and consumer adoption
2. **Capability leadership** — staying at or near the frontier, which feeds revenue but also drives organizational mission, talent attraction, and the ability to attract future compute
3. **Regulatory standing** — not being shut down, maintaining access to key markets (EU deployment, government contracts), managing liability exposure
4. **Talent and compute access** — the binding constraints on capability development; everything else is downstream of these

Benchmark scores enter the objective indirectly: they are a credible (to consumers and funders) signal of capability leadership. A lab cares about MMLU because funders and customers look at MMLU, not because MMLU is intrinsically valuable. This distinction determines *when* gaming is rational: gaming is attractive when benchmark signal is over-weighted by the market relative to other signals, and when the gap between benchmark performance and product performance is hard for market actors to observe.

---

## Decision Timescales (Why a Single Portfolio is Wrong)

Real provider decisions happen at very different timescales and are made by different parts of the organization:

| Decision | Timescale | Who decides | What constrains it |
|---|---|---|---|
| Pre-training compute allocation | Months to years ahead | Leadership + finance | Available capital, committed fundraising, hardware delivery |
| Model architecture choices | Per training run | Research team | State of the art, internal research agenda |
| Post-training target distribution | Per training run / continuously | ML team + product | Product roadmap, benchmark portfolio, user feedback |
| Which results to publish / when | Per release | Leadership + comms | Competitive positioning, regulatory disclosure rules |
| Pricing and deployment strategy | Quarterly | Product + business | Market conditions, cost structure, competitor pricing |
| Safety commitments | Varies | Leadership + policy | Regulatory pressure, public commitments, incidents |

The current simulation's round-by-round portfolio allocation collapses all of these into a single tactical decision. The most critical ones to separate are:

- **Compute allocation** — largely driven by funding; not a free tactical choice each round
- **Post-training target distribution** — the real locus of the benchmark alignment decision
- **Disclosure/release strategy** — absent from current model; major gaming mechanism

---

## The Ideal Action Space

### Decision 1: Compute Commitment (slow-moving, capital-constrained)

Not a round-by-round choice. Determined primarily by available funding. Affects the *ceiling* on capability gains. Would be modeled as a function of `funding_multiplier` rather than an explicit allocation.

### Decision 2: Training Target Distribution (the core strategic choice)

Each training run, a provider implicitly chooses what task distribution to optimize for. The key axis:

- **Real-task alignment**: diverse user deployment tasks — coding, reasoning, instruction following, factual QA across diverse contexts. Builds `general_capability`. Gains are slower but transfer across domains.
- **Benchmark alignment**: tasks that resemble the current benchmark portfolio — specific formats, known rubrics, datasets adjacent to test sets. Builds `benchmark_capability`. Gains are faster but narrow.

This is not deliberate cheating. A lab genuinely believes it is building a better model by optimizing for coding benchmarks. The problem is that benchmark tasks are a proxy for real tasks, and the proxy degrades under optimization pressure (Goodhart). Gaming emerges structurally from the incentive to optimize a measurable proxy rather than the underlying construct.

Grounded in: RLHF target distribution choices; known cases of benchmark score inflation without clear capability gains (MMLU saturation, HumanEval); Chollet's task distribution argument; recent work on benchmark contamination and score-capability gaps.

### Decision 3: Disclosure Strategy (absent from current model)

Providers choose:
- Whether to publish evaluation results at all (selective disclosure)
- Which model version to submit (cherry-picking checkpoints)
- When to release (timing relative to competitor releases)
- How to frame capability claims (marketing vs. technical accuracy)

This is arguably the most direct gaming mechanism, and entirely absent. A lab can run 50 eval seeds and publish the best-performing run. They can delay release until after a benchmark refresh. They can choose which benchmarks to report on (selecting favorable ones). This is legal, common, and creates systematic score inflation with no corresponding capability gain.

### Decision 4: Safety and Deployment Commitments

Providers make public safety commitments (voluntary commitments, third-party audits, red-teaming policies) that are partially strategic (regulatory positioning) and partially genuine. These affect:
- Incident probability (via actual safety investment)
- Consumer trust in regulated sectors (via visible commitment signals)
- Regulatory standing (via compliance credibility)

Currently `safety_alignment` as a portfolio weight partially captures this but misses the distinction between *actual* safety investment and *signaled* safety commitment — a provider can make strong public safety commitments without investing heavily in actual alignment work.

---

## The 2D Capability Decomposition (Option D)

The most structurally important change. Replace scalar `true_capability` with:

### `general_capability`
- What the model can actually do on novel, diverse real-world tasks
- Grows from fundamental research and training optimization
- Hard to grow quickly — subject to compute and algorithmic constraints
- What consumer satisfaction should depend on (with noise/variance)
- Analogous to "g" in psychometrics — the general factor that transfers

### `benchmark_capability`
- How well the model performs on the current benchmark portfolio
- Grows from general_capability (benchmarks do measure something real) + benchmark alignment investment
- Can diverge significantly from general_capability under optimization pressure
- What published scores reflect (alongside benchmark validity/exploitability)
- Analogous to "g-loaded" vs "g-independent" test performance

**Score generation model:**
```
score ~ Normal(benchmark_capability + eval_eng_bonus × exploitability, noise)
```
where `benchmark_capability = general_capability + alignment_gain` and `alignment_gain` grows from benchmark-focused post-training.

**Key property:** `benchmark_capability` cannot exceed `general_capability + max_alignment_gap`. The ceiling on how much you can inflate benchmark capability above general capability is bounded — it degrades as benchmark validity decays (the evaluator gets harder to game), and it resets when a new benchmark is introduced (specialization doesn't transfer to new benchmarks).

**Consumer satisfaction model:**
```
satisfaction = f(general_capability) + other_factors
```
where the gap between `benchmark_capability` and `general_capability` is what creates consumer disappointment — not a computed penalty, but a structural consequence of the two-track capability model.

---

## What Consumer Satisfaction Should Depend On

Beyond general_capability, candidate factors (see separate design discussion):

1. **Reliability / output variance** — a model that sometimes does great and sometimes fails badly creates lower satisfaction than a consistent model at the same average capability level. Risk-averse segments (enterprise, healthcare) weight this heavily.
2. **Task-domain fit** — how well the provider's capability profile matches the segment's use-case requirements. A high-general-capability model that is weak in a specific domain (say, code generation) may satisfy a coding-focused segment less than a lower-capability model with strong benchmark_capability in coding.
3. **Price / access cost** — already in the model via cost_advantage; well-grounded.
4. **Safety and reliability of service** — incident history, uptime, compliance signals. Already partially in the model.
5. **Switching friction** — already modeled.
6. **Trust signals and transparency** — how much does the consumer know about what they're getting? Opaque models create uncertainty; providers who publish evals, audits, or commit to transparency earn trust credit.

---

## Key Missing Interactions

### Disclosure / signaling between providers
Labs watch each other and respond to benchmark releases, paper publications, and product releases. No richer signaling than score observation exists in the current model.

### Compute as an explicit scarce resource
The most fundamental driver of capability gains — absent. Capital goes to funding_multiplier but there is no explicit compute market, no scaling-law-driven returns, no hardware bottleneck.

### Product-benchmark gap belief
Providers should form beliefs about how well their benchmark performance predicts real user outcomes, updated by consumer satisfaction signals. Providers who believe the gap is large would rationally invest more in general capability. This creates heterogeneity without hand-coding it.

### Selective disclosure as a gaming mechanism
The most common real-world form of gaming is absent. Providers should be able to choose what to submit and when.

---

## What to Preserve from Current Model

- The plan/observe/reflect/execute cognitive loop — sound architecture
- `funding_multiplier` modulating capability growth — directionally right
- Safety investment reducing incident probability — well-grounded
- The four-actor downstream ecosystem (consumers, policymakers, funders, media) — this is the simulation's main contribution and should be preserved
- Heuristic vs LLM mode — flexibility is valuable
- Benchmark evolution (Goodhart decay, saturation, replacement) — mechanistically sound, just needs to operate on `benchmark_capability` not `true_capability`
