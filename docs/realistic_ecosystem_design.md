# Toward a Fully Emergent Evaluation Ecosystem: Design Vision

*Speculative north-star document. Describes a more realistic simulation architecture that builds on the current implementation without changing it. Intended as a design reference for future development.*

---

## Motivation

The current simulation treats providers as portfolio-allocating agents that respond to public signals each round. This captures the Goodhart dynamic well but conflates decisions that happen at very different timescales and abstracts away the mechanisms that make gaming rational in practice. This document describes what a more realistic ecosystem would look like — one where gaming, safety investment, and capability development are *emergent consequences* of provider incentives rather than explicit portfolio choices.

The key shift: providers should want **revenue and market position**, not benchmark scores. Benchmark scores enter their objective function only because the market over-weights them as a capability signal. When that over-weighting disappears (e.g., after a major incident exposes the gap, or a new evaluation paradigm gains traction), gaming should naturally decline — without any rule change in the simulation.

---

## What It Means to "Focus on a Benchmark"

In the current simulation, `benchmark_focus` is a weight vector that routes `evaluation_engineering` budget toward specific domains. This captures the output of benchmark specialization but not the mechanism.

In reality, "focusing on a benchmark" means something more specific and more varied:

### 1. Post-training Data Curation
The most common form. A lab curates its RLHF, instruction-tuning, or fine-tuning dataset to emphasize tasks that resemble the target benchmark's format, rubric, and difficulty level. This is not deliberate cheating — the lab genuinely believes it is building a more useful model by training on coding tasks if it wants to improve HumanEval. The problem is that the proxy (benchmark) degrades under optimization pressure faster than the underlying skill improves.

Concretely: a lab targeting MATH will include more step-by-step math problems in its post-training distribution, favor chain-of-thought formats that match MATH's grading rubric, and downweight unrelated tasks. The capability gain is real but narrower than the score improvement suggests.

### 2. Benchmark-Adjacent Data Collection
Labs actively seek out or generate data that is "in the neighborhood" of benchmark test sets — same domain, same format, plausibly drawn from the same distribution. This can happen without access to test labels (so it is not classic contamination) but still inflates scores by reducing the distribution shift between training and evaluation.

### 3. Selective Disclosure and Cherry-Picking
The most common real-world form of gaming and entirely absent from the current model. A lab runs 20--50 evaluation seeds or checkpoint submissions and reports the best-performing run. They evaluate on benchmarks where they expect to perform well and omit others. They time releases to follow competitor announcements. None of this improves underlying capability, but it systematically inflates published scores. It is legal, common, and structurally identical to gaming in its effect on market signals.

### 4. Benchmark-Specific Prompting and Evaluation Engineering
Labs tune their inference pipeline — prompt templates, few-shot examples, output parsing, sampling parameters — specifically for benchmark conditions. A model can score substantially higher on GSM8K with a chain-of-thought prompt template optimized for that rubric than with the same model in a neutral prompt condition. This is the current model's `evaluation_engineering` lever, but in reality it is continuous and gradient-guided rather than a simple portfolio weight.

### 5. Emergent Specialization vs. Strategic Focus
A key distinction absent from the current model: some benchmark specialization is **strategic** (the lab explicitly decides to target a benchmark to signal quality to funders/consumers) while some is **emergent** (the lab's genuine R&D agenda happens to align with benchmark domains because those domains are where commercial applications are). A lab that builds products for software developers will naturally score well on coding benchmarks even without strategic gaming. The simulation currently cannot distinguish these, which means it cannot model the conditions under which gaming is rational versus when it is a byproduct of legitimate optimization.

---

## Toward Fully Emergent Dynamics

The current simulation's main deviation from full emergence is that providers have explicit portfolio levers (`evaluation_engineering`, `fundamental_research`, etc.) that mechanically map to outcomes. This works but means that gaming is always a choice rather than a consequence. A more emergent architecture would remove the explicit levers and let behavior emerge from a smaller set of primitive decisions.

### The 2D Capability Architecture (from `ideal_provider_model.md`)

Replace scalar `true_capability` with:

- **`general_capability`**: What the model can do on novel, diverse real-world tasks. Grows from fundamental research and compute investment. Hard to grow quickly. What consumer satisfaction *should* depend on.
- **`benchmark_capability`**: How well the model performs on the current benchmark portfolio. Grows from `general_capability` (benchmarks do measure something real) plus benchmark-alignment investment (post-training data curation, fine-tuning). Can diverge significantly from `general_capability` under optimization pressure.

The score generation becomes:
```
score ~ Normal(benchmark_capability + selective_disclosure_bonus × exploitability, noise / validity)
```
where `benchmark_capability = general_capability + alignment_gain` and `alignment_gain` is capped by a `max_alignment_gap` that shrinks as benchmark validity decays.

**Why this produces emergent gaming**: providers maximize revenue, which depends on market share, which depends on consumer satisfaction. Consumer satisfaction depends on `general_capability` (actual product performance), but consumers *choose* based on published scores, which reflect `benchmark_capability`. The gap between what consumers choose on and what they experience is structurally the Goodhart dynamic — no explicit gaming lever required.

### Compute as an Explicit Scarce Resource

Currently capital is represented abstractly as `funding_multiplier` on capability growth. A more realistic architecture would include:

- **Compute market**: H100/B200 cluster contracts, lead times (6--18 months), and prices. Capital converts to compute capacity on a timeline, not instantly.
- **Scaling laws**: capability gains from training follow approximately log-linear scaling with compute (Chinchilla laws). This bounds how fast any provider can grow true capability and means that well-funded providers have a structural advantage that cannot be closed by smart portfolio allocation.
- **Inference cost structure**: larger, more capable models cost more to serve, creating a pricing floor. This makes the cost_advantage / pricing dynamics endogenous — a provider's pricing is constrained by their model size and hardware costs, not a free parameter.

In this architecture, gaming becomes attractive precisely when compute is scarce and competitors are catching up — a provider with limited compute can close a benchmark gap cheaply through benchmark alignment when it cannot close a capability gap through training. This is the real-world logic of benchmark gaming, and it emerges from the economics rather than being imposed.

### Decision Timescale Separation

Real provider decisions happen at very different timescales. The current single-round portfolio allocation collapses these. A more realistic architecture separates:

| Decision | Timescale in simulation | Driver |
|---|---|---|
| Compute commitment | Slow (5--10 rounds) | Funding received, hardware lead times |
| Training run target distribution | Medium (2--4 rounds) | Post-training roadmap, benchmark portfolio |
| Selective disclosure | Fast (1 round) | Competitive positioning, release timing |
| Pricing update | Fast (1 round) | Market conditions, cost structure |
| Safety commitment signals | Medium (varies) | Regulatory pressure, incidents |

Separating these means that a provider cannot instantly respond to a competitor's benchmark release by gaming the same benchmark — they need to commit to a post-training run first. This introduces realistic inertia and makes the competitive dynamics richer.

### Selective Disclosure as a First-Class Mechanism

Currently providers must publish all scores. In reality, selective disclosure is the primary gaming mechanism:

- **Which benchmarks to report**: Providers choose which benchmarks to evaluate on and which to publish. A provider who scores poorly on safety benchmarks simply does not report them.
- **Which run to submit**: From multiple training runs or checkpoints, providers pick the best-performing. The published score is the maximum of a distribution, not the expected value.
- **Release timing**: Providers time releases to maximize competitive impact — releasing before a competitor's benchmark refresh, or after their own new benchmark that they expect to perform well on.

In a fully emergent model, selective disclosure would be an action in the provider's strategy space, with the evaluator able to mandate reporting standards as an intervention (which is precisely what real-world evaluation governance debates are about).

### Modeling the Product-Benchmark Gap Belief

Providers should form beliefs about how well their benchmark performance predicts real user outcomes, updated by consumer satisfaction signals. This belief heterogeneity creates emergent variation in gaming behavior:

- A provider who receives strong consumer satisfaction signals despite modest benchmark scores will learn that `general_capability > benchmark_capability` is commercially viable, and will invest less in benchmark alignment.
- A provider who relies heavily on funders who weight benchmark scores will rationally invest more in benchmark alignment even if they suspect the scores do not predict product quality.

This means gaming is not a fixed strategic choice but a dynamic response to the information environment — and reducing gaming requires changing the information environment (e.g., publishing consumer satisfaction data, requiring third-party capability audits) not just imposing regulatory fines.

---

## Pricing and Cost Dynamics

The current `cost_advantage` parameter is static (set at initialization, with a slow drift for open-source providers). A realistic pricing model would be more dynamic:

### Endogenous Pricing
A provider's price per token is determined by:
- **Training amortization cost**: the total compute cost of the training run amortized over expected tokens served
- **Inference cost**: hardware cost per token at a given model size and utilization rate
- **Competitive margin**: markup over cost, bounded by willingness-to-switch

This means that larger models have higher pricing floors even if they have higher capability. It also means that providers who achieve a given capability level at lower compute cost (through algorithmic efficiency) can sustainably undercut competitors — which is the DeepSeek dynamic.

### Price as a Signal
Beyond affecting consumer satisfaction directly, pricing is a signal about the provider's strategy. A provider who prices aggressively low signals either: (a) cost efficiency, (b) willingness to sacrifice margin for market share, or (c) open-source deployment model. Funders interpret price differently depending on whether revenue is growing (loss-leader strategy) or flat (efficiency advantage). This signaling dimension is entirely absent from the current model.

---

## What Changes in Consumer Dynamics

In the more emergent model, consumer satisfaction would structurally depend on the gap between `benchmark_capability` (what consumers used when choosing) and `general_capability` (what they experience in deployment). This removes the explicit `gaming_penalty` parameter and replaces it with a structural consequence of the two-track capability architecture.

Additional dimensions worth modeling:

- **Output variance / reliability**: Enterprise consumers in healthcare and legal care not just about average capability but about worst-case performance. A model that is excellent on average but occasionally fails badly is less acceptable in high-stakes settings than a consistently good model at lower average capability. This segment-specific risk aversion is absent.
- **Task-domain fit**: A provider with high general capability but specialization misaligned with a segment's use case (e.g., a math-focused model for a legal enterprise buyer) may satisfy that segment less than a lower-capability model with better domain fit.
- **Trust and transparency signals**: Providers who publish audits, commit to third-party evaluations, or participate in standardized benchmarking earn a trust premium among cautious and enterprise segments. This creates a virtuous cycle where evaluation transparency is commercially incentivized rather than purely compliance-driven.

---

## What to Preserve

The following aspects of the current model are well-grounded and should be carried forward:

- **The plan/observe/reflect/execute cognitive loop** — sound architecture for strategic actors
- **Benchmark Goodhart decay** ($\alpha \downarrow$, $\beta \uparrow$ proportional to mean eval\_eng) — mechanistically sound, just needs to operate on `benchmark_capability` rather than `true_capability`
- **The four-actor downstream ecosystem** (consumers, policymakers, funders, media) — the simulation's main contribution; richer than anything in the benchmark gaming literature
- **Graduated policymaker escalation** — realistic and well-calibrated
- **Open-source provider exemptions and contamination dynamics** — captures a real structural asymmetry
- **Barrier-to-entry index** — a useful composite metric for market contestability
- **Heuristic vs. LLM planning modes** — flexibility is valuable for sensitivity analysis

---

## Summary: From Parameterized to Emergent

| Current | Emergent alternative |
|---|---|
| `evaluation_engineering` portfolio weight | Benchmark-alignment post-training investment + selective disclosure action |
| Scalar `true_capability` | 2D: `general_capability` + `benchmark_capability` |
| `cost_advantage` as static parameter | Endogenous pricing from compute cost structure |
| Gaming penalty computed externally | Consumer disappointment as structural gap between `benchmark_capability` and `general_capability` |
| Round-by-round portfolio reallocation | Timescale-separated decisions (compute commitments, training runs, disclosure) |
| Funding → capability multiplier | Funding → compute capacity → training throughput → capability ceiling |
| Safety as portfolio weight | Signaled commitments vs. actual investment (two separate levers) |

The goal is a simulation where benchmark gaming, safety underinvestment, and market concentration emerge from a minimal set of primitive incentives (revenue, compute, regulatory standing) rather than from explicit portfolio levers — making the model's predictions less sensitive to parameterization choices and more structurally robust.
