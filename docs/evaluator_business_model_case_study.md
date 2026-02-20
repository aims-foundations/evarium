# Case Study: Evaluator Business Models and The Leaderboard Illusion
## Modeling Evaluator-Provider-Funder Dependencies in the Ecosystem Simulation

**Last Updated:** 2026-02-16
**Status:** Design Document
**Related Tasks:** Goal 3 - Funder-Evaluator Relationship

---

## Executive Summary

This document analyzes how real-world AI evaluation platforms (like LMSYS Chatbot Arena / LMArena) depend on both funders and model providers, and how these dual dependencies create conflicts of interest that bias leaderboard rankings. Drawing from the "Leaderboard Illusion" paper and LMArena's business model, we propose modeling evaluators as companies with resource constraints and revenue incentives that affect their benchmark design choices and access policies.

**Key insight:** Evaluators are not neutral arbiters. They are businesses that depend on funding, and providers who pay for premium access gain systematic advantages through multiple submissions and early benchmark access.

---

## Part 1: Real-World Evidence

### The Leaderboard Illusion (arXiv:2504.20879)

**Authors:** Shivalika Singh, Yiyang Nan, Alex Wang (2025)
**Venue:** NeurIPS 2025 Datasets and Benchmarks Track

#### Core Findings

1. **Multiple Private Submissions Create Selection Bias**
   - Meta tested **27 private Llama-4 variants** before public release
   - Providers choose best-performing variant to publish
   - Testing just 10 variants yields ~**100-point Elo boost**
   - This is systematic leaderboard gaming through selective disclosure

2. **Data Access Inequality**
   - Google: 19.2% of all Chatbot Arena evaluation data
   - OpenAI: 20.4% of all evaluation data
   - 83 open-weight models combined: Only 29.7%
   - More data access → **112% relative performance gains**

3. **Private Testing as Premium Service**
   - Undisclosed private testing practices benefit handful of providers
   - Creates "distorted playing field"
   - Providers who pay get advantages not available to others

**Implication:** Chatbot Arena is not a level playing field. Well-resourced labs systematically outperform due to structural advantages, not just model quality.

**Sources:**
- [The Leaderboard Illusion (arXiv)](https://arxiv.org/abs/2504.20879)
- [Medium Analysis](https://medium.com/verimsabanci/the-leaderboard-illusion-unmasking-bias-in-ai-benchmarks-4efeb3ae7eb5)
- [The Sequence Newsletter](https://thesequence.substack.com/p/the-sequence-radar-534-the-leaderboard)

---

### LMArena Business Model

**Organizational Evolution:**
- **2023:** Started as LMSYS Org academic project at UC Berkeley
- **2025:** Spun off as LMArena company
- **May 2025:** Raised $100M seed at $600M valuation (a16z, UC Investments, Lightspeed, Felicis, Kleiner Perkins)
- **Jan 2026:** Raised $150M Series A at $1.7B valuation

#### Revenue Model: Freemium with Enterprise Services

**Free Tier (Public Arena):**
- Open community evaluation platform
- Public leaderboard rankings
- Drives traffic and legitimacy

**Premium Tier (Revenue-Generating):**
- **Primary customers:** OpenAI, Google DeepMind, Anthropic, Meta
- **Services offered:**
  - Public benchmarking
  - Competitive positioning
  - **Confidential pre-release testing** (private evaluation before public launch)
  - Custom evaluation infrastructure

**Funding Dependencies:**

1. **Venture Capital:** a16z, Lightspeed, Felicis, UC Investments ($250M total)
2. **Infrastructure Sponsors:** Voltage Park, NVIDIA, Google Cloud, AMD, HuggingFace (compute donations)
3. **Provider Service Fees:** Paid by model labs for private testing and data access
4. **API Credits:** Providers supply credits to serve their models on platform

**Conflict of Interest:**
- Evaluator's revenue depends on serving paying providers
- Providers who pay get private testing → can cherry-pick best variant
- Data access skewed toward paying customers
- Incentive to design benchmarks that paying providers excel at

**Sources:**
- [Contrary Research: LMArena Business Breakdown](https://research.contrary.com/company/lmarena)
- [TechCrunch: LMArena $1.7B Valuation](https://techcrunch.com/2026/01/06/lmarena-lands-1-7b-valuation-four-months-after-launching-its-product/)
- [LMSYS About Page](https://lmsys.org/about/)

---

## Part 2: Simulation Design

### Current Evaluator Model (Baseline)

**Existing behavior (no business model):**
- Evaluators introduce new benchmarks when validity degrades
- Providers submit once per round (no multiple trials)
- No funding dependency
- No premium access tiers
- Neutral arbiters with no resource constraints

**Limitation:** Doesn't capture real-world evaluator incentives and conflicts of interest.

---

### Evaluator-as-Company Model (New)

#### Core Principle: Preferential Access as a Service

Evaluators are **companies** that:
1. Need funding to operate (compute for running benchmarks)
2. Receive revenue from funders (government, foundations, VCs) + provider service fees
3. Offer premium access to paying providers
4. Face tension between neutrality and revenue incentives

#### What Premium Access Provides

| Feature | Free Tier (Non-Paying) | Premium Tier (Paying) |
|---------|------------------------|----------------------|
| **Evaluation Runs** | 1 strategy per round | N trials per round, publish best |
| **Benchmark Access** | See benchmarks when introduced | Early access (2-3 rounds before public) |
| **Data Access** | Standard evaluation data | More frequent evaluations, more data |
| **Cost** | Free | Service fee per round |

**Key mechanisms:**
1. **Best-of-N Selection Bias** (Leaderboard Illusion)
2. **Early Access Advantage** (preparation time for new benchmarks)

---

### Multiple Submission Formula

**Number of trials per provider per round (actual implementation in `actors/evaluator.py`):**

```python
def compute_n_trials(self, provider_name: str, eval_engineering: float) -> int:
    if not self.evaluator_as_company:
        return 1  # Default behavior

    # Binary premium access: provider is either a subscriber or not
    funding_bonus = 1 if provider_name in self.private_state.premium_providers else 0
    eval_eng_bonus = int(eval_engineering * 5)
    # eval_eng=0.2 → +1; eval_eng=0.4 → +2; eval_eng=0.8 → +4

    # Need BOTH premium access AND eval engineering expertise
    n_trials = 1 + min(funding_bonus, eval_eng_bonus)

    return min(5, n_trials)  # Cap at 5
```

**Why minimum of funding_bonus and eval_eng_bonus?**
- **Premium access + low eval_eng:** Subscription paid, but no expertise to generate meaningful variants → limited benefit
- **High eval_eng + no premium access:** Expertise, but no extra trials granted → limited benefit
- **Premium + high eval_eng:** Maximum advantage

Note: `funding_bonus` is binary (0 or 1), not a gradient — providers are either premium subscribers or not. Premium status is determined by whether they appear in `private_state.premium_providers`, which is populated from `provider_premium_payments` passed to `collect_funding()`.

**Selection mechanism (in `evaluate_all`):**
```python
# Premium provider runs N trials, keeps best score per benchmark
trial_scores = [self.evaluate(true_cap, eval_eng, benchmark) for _ in range(n_trials)]
score = max(trial_scores)
```

**Effect:** ~10-20 point score inflation per extra trial (calibrated from Leaderboard Illusion paper).

---

### Early Access Mechanism

**Benchmark introduction timeline:**

| Round | Free Tier | Premium Tier |
|-------|-----------|--------------|
| N-3 | No knowledge | Benchmark spec shared privately |
| N-2 | No knowledge | Can test strategies, optimize |
| N-1 | No knowledge | Refinement round |
| **N** | **Benchmark introduced publicly** | Already optimized (3-round head start) |

**Implementation:**
```python
class Evaluator:
    def __init__(self):
        self.upcoming_benchmarks = []  # Queue of benchmarks to introduce
        self.premium_subscribers = []  # Providers with paid access

    def plan_benchmark_introduction(self, round_num):
        """Introduce benchmark at round N, notify premium subscribers at N-3."""
        new_benchmark = self._design_benchmark()

        # Add to queue with introduction round
        self.upcoming_benchmarks.append({
            "benchmark": new_benchmark,
            "public_introduction_round": round_num + 3,
            "early_access_round": round_num,  # 3 rounds early
        })

        # Notify premium subscribers
        for provider in self.premium_subscribers:
            provider.notify_upcoming_benchmark(new_benchmark, rounds_until_public=3)
```

**Provider response to early access:**
```python
# Premium providers can pre-optimize
if provider.has_early_access and benchmark in provider.upcoming_benchmarks:
    # Adjust eval_engineering allocation toward this benchmark
    provider.benchmark_specific_optimization[benchmark] += 0.2
    # Result: Higher score when benchmark goes public
```

**Effect:** 5-10 point score advantage on new benchmark (preparation time).

---

### Evaluator Funding Model

```python
class Evaluator:
    def __init__(self):
        self.budget = 0.0
        self.base_funding_sources = []  # Government, foundations
        self.premium_subscribers = []  # Providers paying for access
        self.benchmark_introduction_cost = 50000  # Per benchmark
        self.benchmark_operation_cost = 10000  # Per benchmark per round

    def collect_funding(self, funders, round_num):
        """Collect funding from funders and premium providers."""
        # Base funding from funders (government, VCs, foundations)
        base_funding = sum(
            funder.allocation_to_evaluator
            for funder in funders
        )

        # Service fees from premium providers
        # pricing is set by evaluator_premium_pricing in SimulationConfig (default: $15M/round in experiments)
        service_revenue = sum(provider_premium_payments.values())

        self.private_state.budget += base_funding + service_revenue
        self.private_state.premium_providers = set(provider_premium_payments.keys())

    def can_introduce_benchmark(self) -> bool:
        """Check if evaluator has budget to introduce new benchmark."""
        benchmark_cost = 50000.0  # hardcoded in consider_new_benchmark()
        return self.private_state.budget >= benchmark_cost
    # Note: benchmark_operation_cost is not implemented — only introduction cost is gated
```

**Budget constraints affect:**
1. **Benchmark introduction frequency:** Low budget → can't afford new benchmarks → stale evaluation suite
2. **Dependence on provider fees:** Low base funding → more dependent on provider revenue → more conflicts of interest

Note: Benchmark retirement/operation cost is not implemented — only introduction is budget-gated.

---

### Funder Allocation to Evaluators

**New funder decision:** How much to allocate to evaluators vs providers?

```python
class Funder:
    def allocate_capital(self, providers, evaluators, round_num):
        """Split capital between providers (R&D) and evaluators (infrastructure)."""
        # Funder type affects split
        if self.funder_type == "government":
            evaluator_share = 0.30  # Gov values public infrastructure
        elif self.funder_type == "foundation":
            evaluator_share = 0.20  # Balanced
        elif self.funder_type == "vc":
            evaluator_share = 0.05  # VCs fund providers directly

        evaluator_budget = self.round_deployment * evaluator_share
        provider_budget = self.round_deployment * (1 - evaluator_share)

        # Allocate to evaluator
        evaluators[0].budget += evaluator_budget

        # Allocate remaining to providers (existing logic)
        self._allocate_to_providers(providers, provider_budget)
```

**Funder type effects:**
- **Government funders:** High evaluator support → less provider-dependent → more neutral
- **VC funders:** Low evaluator support → evaluator seeks provider fees → conflicts of interest
- **Foundation funders:** Moderate support

---

## Part 3: Emergent Dynamics and Research Questions

### Positive Feedback Loops

**Rich Get Richer:**
1. Well-funded provider pays for premium access
2. Gets N trials + early access → inflated score
3. High score → more consumer adoption → more revenue
4. More revenue → more funding → more premium access (loop)

**Evaluator Capture:**
1. Low base funding from government/foundations
2. Evaluator depends on provider service fees
3. Providers paying for access have implicit leverage
4. Evaluator optimizes for paying customers (introduce benchmarks they excel at, avoid ones they don't)

### Indirect Effects on Incident Rate

**No direct incident logic added.** Effects emerge through existing mechanisms:

```
Premium access
  → N trials + early access
  → Higher published scores (selection bias + preparation)
  → Larger gap: published_score - true_capability
  → Existing incident model: gaming_multiplier = 1.0 + (gap × 2.0)
  → More incidents
```

**Cascade:**
- Provider with high funding → premium access → score inflation → gaming gap → more real-world failures

**Policymaker response:**
- If policymaker detects evaluator is provider-funded → mandate public funding
- EU-style: Require independent evaluators (high base funding, low provider fees)
- US-style: Let market decide (evaluator capture goes unchecked until incidents)

### Research Questions

**RQ1:** Does evaluator dependence on provider revenue increase gaming and incident rates?
- **Hypothesis:** High provider-fee ratio → more gaming → more incidents

**RQ2:** Can government funding break evaluator capture?
- **Hypothesis:** High government allocation to evaluator → less provider dependence → more neutral benchmarks

**RQ3:** Does the "rich get richer" dynamic emerge from premium access?
- **Hypothesis:** Funding advantage compounds over time through leaderboard dominance

**RQ4:** How do different funder types affect evaluator neutrality?
- **Hypothesis:** VC-funded evaluators favor incumbents; gov-funded evaluators more neutral

**RQ5:** Does early access create persistent leaderboard leads?
- **Hypothesis:** Providers with early access dominate new benchmarks, lock in advantage

---

## Part 4: Implementation Parameters

### Configuration Flags

**Actual `SimulationConfig` parameters (in `simulation.py`):**

```python
class SimulationConfig:
    # Evaluator-as-company feature flag
    evaluator_as_company: bool = False      # Default: OFF (backwards compatible)
    evaluator_base_budget: float = 0.0      # Starting budget
    evaluator_premium_pricing: float = 10000.0  # Cost per provider per round
    # (experiments use $15M/round — easily affordable for established providers,
    #  puts StartupDotAI out of reach given their VC funding level)
```

Parameters NOT exposed as config (hardcoded in evaluator):
- `benchmark_introduction_cost = 50000.0`
- `max_trials = 5`
- `early_access_rounds` — queue populated but provider pre-optimization not yet wired

**Backwards compatibility:**
- `evaluator_as_company=False`: 1 trial per provider, no funding or premium access
- `evaluator_as_company=True`: N trials (best-of-N), budget gating, premium subscriber set

### Provider Configuration

```python
class Provider:
    # New attributes (only used if evaluator_as_company=True)
    has_premium_access: bool = False
    n_trials_this_round: int = 1
    early_access_benchmarks: list = []  # Benchmarks provider knows about early
```

### Evaluator Configuration

```python
class Evaluator:
    # New attributes (only used if evaluator_as_company=True)
    budget: float = 0.0
    premium_subscribers: list[str] = []  # Provider names
    upcoming_benchmarks: list = []  # Queue with early access timing

    # Revenue tracking
    base_funding_history: list = []
    service_fee_history: list = []
```

---

## Part 5: Experimental Design

### Experiment 1: Impact of Premium Access on Gaming

**Setup:**
- 5 providers: 2 with premium access (high funding), 3 without
- Evaluator funded 50% by government, 50% by provider fees
- Run 50 rounds

**Metrics:**
- Score inflation: `published_score - true_capability` per provider
- Incident rate by provider (premium vs non-premium)
- Market share evolution (do premium providers dominate?)

**Expected Result:**
- Premium providers have 10-15% higher scores (selection bias)
- Premium providers have more incidents (gaming gap)
- Market share concentrates toward premium providers (rich get richer)

---

### Experiment 2: Government Funding Breaks Evaluator Capture

**Setup:**
- 3 conditions:
  - **High provider-funded:** Evaluator gets 80% from provider fees, 20% from gov
  - **Balanced:** 50% provider fees, 50% gov
  - **High gov-funded:** 20% provider fees, 80% gov
- Same providers across conditions

**Metrics:**
- Evaluator benchmark introduction patterns (do they avoid safety benchmarks?)
- Provider gaming levels (eval_engineering investment)
- Incident rates

**Expected Result:**
- High provider-funded → more gaming, more incidents
- High gov-funded → less gaming, fewer incidents, more safety benchmarks

---

### Experiment 3: US vs EU Evaluator Regulation

**Setup:**
- **US condition:** Light-touch, evaluator can be provider-funded
- **EU condition:** Mandates public evaluator funding (80% government)

**Metrics:**
- Evaluator neutrality (benchmark design)
- Provider gaming levels
- Consumer trust (satisfaction)
- Incident rates

**Expected Result:**
- US: Evaluator capture → more gaming → more incidents → eventual regulatory crisis
- EU: Independent evaluator → less gaming → fewer incidents → slower innovation

---

## Part 6: Implementation Status

### Phase 1: Evaluator Budget System — DONE
- [x] `EvaluatorPrivateState` with `budget`, `base_funding`, `service_revenue`, `funding_history`
- [x] `collect_funding(funder_allocations, provider_premium_payments, round_num)`
- [x] Budget check in `consider_new_benchmark()` (cost = $50K)

### Phase 2: Premium Access (Best-of-N) — DONE
- [x] `compute_n_trials()` implemented (binary funding_bonus + eval_eng_bonus, capped at 5)
- [x] N trials run in `evaluate_all()`, best score published
- [x] Trial results stored in `private_state.trial_results`

### Phase 3: Early Access to Benchmarks — DONE
- [x] `early_access_queue` populated in `private_state` when new benchmark introduced
- [x] `_get_effective_benchmark()` applies 1.5x exploitability multiplier for providers in the
      early-access window (first `early_access_rounds=3` rounds after public introduction)
- [x] Wired into `evaluate_all()` — effective benchmark passed to all N trials

### Phase 4: Funder Allocation to Evaluators — NOT DONE
- [ ] Funders do not currently split capital between providers and evaluator
- [ ] Evaluator receives budget via `evaluator_base_budget` initial value only (set in config)
- [ ] Provider premium payments flow through simulation.py → `collect_funding()`

### Phase 5: Logging and Visualization — DONE
- [x] `private_state` serialized in evaluator `save()` / `load()`
- [x] `trial_counts` per provider logged to `rounds.jsonl` via `evaluator_business_metrics`
- [x] `plot_evaluator_business_dashboard()` implemented in `plotting.py`, wired into `create_all_dashboards()`

### Phase 6: Configuration — DONE
- [x] `evaluator_as_company`, `evaluator_base_budget`, `evaluator_premium_pricing` in `SimulationConfig`
- [x] `evaluator_as_company=False` preserves single-trial behavior (backwards compatible)

---

## Part 7: Open Questions

**Q1: Should evaluator budget affect benchmark validity decay?**
- Low budget → can't maintain benchmarks → faster validity decay?
- Or is validity decay purely from gaming pressure (existing model)?

**Q2: Should providers choose to pay for premium access, or is it automatic based on funding?**
- Automatic: If `funding > threshold`, auto-enroll
- Strategic: Provider decides whether to spend on premium access vs R&D

**Q3: Should early access affect all benchmarks or only new introductions?**
- Current design: Only new benchmarks (introduced after premium access granted)
- Alternative: Premium providers get early access to benchmark updates/revisions

**Q4: Should there be a cap on provider fees as % of evaluator revenue?**
- To prevent total capture: `provider_fees < 0.8 × total_revenue`
- Or let it emerge naturally (policymaker intervenes if too captured)

---

## Document History

- **2026-02-16:** Initial design based on Leaderboard Illusion paper and LMArena business model
- **2026-02-18:** Updated to reflect actual implementation — corrected `compute_n_trials` formula (binary not gradient funding_bonus), updated config params to match `SimulationConfig`, corrected funding model signatures; implemented Phase 3 item 2 (`_get_effective_benchmark()` with 1.5x exploitability multiplier for early access window); corrected Phase 5 checklist (both logging and dashboard were already implemented)
