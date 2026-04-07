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

## Part 8: Evaluator Landscape Survey (2026-04-05)

Comprehensive survey of real-world organizations functioning as AI evaluators, organized by archetype. Each case study maps organizational structure, funding model, and capture risk to inform the simulation's evaluator-as-organization model.

---

### 8.1 Taxonomy Overview

| Archetype | Examples | Funding Model | Capture Risk | Independence |
|-----------|----------|---------------|-------------|-------------|
| **Benchmark/Leaderboard** | LMArena, HELM, Hugging Face | VC + provider fees + compute donations | High | Low-Medium |
| **Red-Team / Adversarial** | Gray Swan, Haize Labs, Trail of Bits | VC + consulting fees from labs | Medium | Medium |
| **Compliance / Audit** | Credo AI, Holistic AI, Big Four | Fee-for-service (auditee pays) | Very High | Low |
| **Government / Nonprofit** | UK AISI, METR, Apollo Research | Government budget / grants | Low | High |
| **Internal Lab Teams** | OpenAI Preparedness, Anthropic RSP | Parent company budget | Structural (self-eval) | None (by design) |

---

### 8.2 Case Study: Gray Swan AI (Red-Team / Adversarial)

**Profile:** AI security startup commercializing adversarial research from Carnegie Mellon University.

| Attribute | Detail |
|-----------|--------|
| Founded | 2024, Pittsburgh PA |
| Founders | Matt Fredrikson (CEO, CMU faculty), Andy Zou (CTO, first author of universal adversarial attacks paper arXiv:2307.15043), Zico Kolter (CMU faculty) |
| Funding | ~$5.7M (Juniper Ventures, Lionheart Ventures, Aperiam Ventures, LiveRamp Ventures) |
| Customers | Frontier labs (OpenAI, Anthropic, Meta), UK AI Safety Institute |
| Team | Small (~15-25 estimated), plus 15,000+ crowdsourced red teamers in the Arena |

**Products:**
- **Shade** — Automated red-teaming and continuous vulnerability assessment
- **Cygnal** — Real-time I/O filtering (99.98% attack block rate, <100ms latency)
- **Cygnet** — Safety-tuned LLM for text moderation (based on Llama-3)
- **Arena** — Crowdsourced jailbreaking platform. UK AISI/Gray Swan challenge: 1.8M attacks across 22 models — every model broke.

**Business model:** Multi-layered: SaaS products (usage-based), enterprise on-prem/VPC, red-teaming consulting, Arena as data flywheel (prize-incentivized red teamers generate adversarial data that improves products).

**Capture dynamics:** Gray Swan's position is unusual — their value proposition is explicitly adversarial, which structurally resists capture (an evaluator that finds nothing has no value). However: (a) frontier labs are both customers and subjects, creating dual-role tension; (b) the Arena depends on model access from labs; (c) the team explicitly distanced from compliance/policy (SB-1047 statement). Their academic pedigree and open research model (the founding paper is public) provide some independence, but revenue dependency on labs is a structural risk as the company scales.

**Simulation relevance:** Represents the "adversarial evaluator" archetype — high capability, lab-funded, inherent tension between finding vulnerabilities (value prop) and maintaining access (revenue dependency).

---

### 8.3 Case Study: Haize Labs (Red-Team / Adversarial)

| Attribute | Detail |
|-----------|--------|
| Founded | 2023, New York |
| Founders | Leonard Tang (CEO, turned down Stanford PhD), Steve Li (Berkeley AI Research) |
| Funding | $12.5M seed (General Catalyst), $100M valuation |
| Team | ~14 employees |
| Investors | Angels include Amjad Masad (Replit), Scott Wu (Cognition), Demi Guo (Pika), Neil Shen (Sequoia China) |

**What they do:** "Haizing" — rigorous stress-testing and red-teaming of AI systems to discover failure modes. Tagline: "Deploy 99.9% Reliable AI." Pure-play adversarial testing, closer to research end than compliance.

**Capture risk:** Medium. VC-backed with strong investor bench but small team. Independence depends on whether they can diversify beyond lab-funded engagements.

---

### 8.4 Case Study: The Acquisition Wave (Red-Team Firms Absorbed by Platform Players)

Three major AI security startups were acquired in 2024-2025, totaling ~$1.1B. This consolidation pattern mirrors cloud security circa 2018-2022.

| Company | Acquirer | Price | What They Did |
|---------|----------|-------|---------------|
| Robust Intelligence | Cisco | ~$400M (Oct 2024) | "AI Firewall," algorithmic red-teaming. Team became Cisco's Foundation AI unit. |
| CalypsoAI | F5 | $180M (2025) | Enterprise AI guardrails (Moderator product). Had raised $40M+ from Paladin Capital, Lockheed Martin Ventures. |
| Protect AI | Palo Alto Networks | ~$500-700M (Jul 2025) | MLSecOps: model scanning, posture management, red-teaming, runtime protection. Had raised $108.5M. |
| Lakera | Check Point | $190M (2025) | AI application firewall for prompt injection (Lakera Guard). Built "Gandalf" (interactive prompt injection game / data flywheel). |

**Capture implication:** When independent red-team firms get acquired by large security/infra vendors, the adversarial independence may weaken. The acquirer's enterprise sales relationships with AI labs create new conflicts. A Cisco salesperson selling networking gear to OpenAI has different incentives than an independent Robust Intelligence researcher finding OpenAI vulnerabilities.

**Market size:** AI red-teaming services: ~$1.75B (2025), projected $6.17B by 2030 (28-30% CAGR). Total AI security startup funding: $8.5B across 175 companies over 24 months.

---

### 8.5 Case Study: Scale AI / SEAL Leaderboard (Benchmark Provider)

| Attribute | Detail |
|-----------|--------|
| Founded | 2016 (Scale AI); SEAL launched ~2024 |
| Founder | Alexandr Wang (CEO, departed to Meta in 2025 after Meta's $14.3B investment) |
| Valuation | $29B (with Meta investment) |
| Revenue | $1.8B (2025 estimated) |
| Employees | 500+ |

**What they do:** Scale AI is primarily a data labeling company that expanded into AI evaluation via SEAL (Safety, Evaluations, and Alignment Lab). SEAL produces expert-curated benchmarks and leaderboards, positioning as a more rigorous alternative to LMArena's crowd-sourced approach.

**Capture risk:** Very high. Scale AI's core data labeling business depends on contracts with the same labs it evaluates. Meta's $14.3B investment makes Scale financially entangled with a frontier lab. The evaluator cannot credibly rate its investor/client unfavorably.

---

### 8.6 Case Study: Stanford HELM (Academic Benchmark)

| Attribute | Detail |
|-----------|--------|
| Founded | 2022, Stanford Center for Research on Foundation Models (CRFM) |
| Lead | Percy Liang (Stanford CS) |
| Funding | Stanford + industry compute donations |
| Model | Open-source, academic |

**What they do:** Holistic Evaluation of Language Models — multi-metric evaluation across accuracy, calibration, robustness, fairness, bias, toxicity, and efficiency. Open methodology, publicly available results.

**Capture risk:** Moderate. Academic independence provides structural protection, but: (a) industry funds Stanford broadly; (b) CRFM receives compute donations from labs; (c) academic career incentives reward lab cooperation (access to models, co-authorship). Percy Liang has maintained HELM's methodological independence, but the next generation of academic evaluators may face stronger pull.

---

### 8.7 Case Study: Credo AI (Compliance / Governance Platform)

| Attribute | Detail |
|-----------|--------|
| Founded | 2020 |
| CEO | Navrina Singh (former VP at Qualcomm) |
| Notable | Andrew Ng is co-founder/board member |
| Funding | $41.3M total, $101M valuation |
| Recognition | Gartner 2025 Market Guide for AI Governance Platforms; Fast Company Most Innovative 2026 |

**What they do:** Enterprise AI governance platform — risk assessment, policy management, compliance tracking. Positioned for EU AI Act readiness. Helps enterprises document, monitor, and demonstrate responsible AI use.

**Capture risk:** High. Classic "auditee pays" — enterprises being governed are the customers. Revenue depends on making governance painless enough that enterprises adopt it, which incentivizes lenient defaults. Andrew Ng's involvement provides credibility but also signals industry alignment.

**Market context:** Enterprise AI governance market: $2.2B (2025), projected $11.05B by 2036 at 15.8% CAGR. EU AI Act compliance market estimated at EUR 17B by 2030.

---

### 8.8 Case Study: Big Four AI Audit Practices

All four firms are building AI governance/audit capabilities, leveraging existing enterprise relationships.

| Firm | AI Investment | Approach |
|------|-------------|----------|
| KPMG | $2B committed to AI | Launched Workbench (Jun 2025) — multi-agent audit collaboration |
| PwC | Undisclosed | Launched Agent OS — compliance-focused, governance-driven platform |
| Deloitte | Undisclosed | Launched Zora AI (Mar 2025) — AI-powered procurement/audit |
| EY | 30% revenue increase in AI services | Enterprise AI transformation + governance frameworks |

**Capture risk:** Very high — identical to financial auditing. The "auditee pays" model, client retention incentives, non-audit service revenue from the same clients, and revolving door dynamics all apply. The Big Four will dominate compliance auditing by default due to existing enterprise relationships, but their independence is structurally compromised.

**Key difference from financial auditing:** No PCAOB equivalent exists for AI. No mandatory rotation. No restrictions on non-audit services. The AI audit market currently resembles pre-Sarbanes-Oxley financial auditing — voluntary, unregulated, structurally prone to capture.

---

### 8.9 Case Study: UK AI Safety Institute (Government Evaluator)

| Attribute | Detail |
|-----------|--------|
| Founded | November 2023 (Bletchley Park AI Safety Summit) |
| Budget | ~GBP 100M/year |
| Head | Formerly Ian Hogarth; restructured under Labour government |
| Staff | 100+ researchers |

**What they do:** Pre-deployment safety testing of frontier models. Tested 30+ models. Built the open-source **Inspect** framework for AI evaluation. Partnered with Gray Swan Arena for adversarial challenges.

**Capture risk:** Low (structurally). Government-funded, no revenue dependency on labs. But: (a) labs cooperate voluntarily (no legal mandate) — if AISI is too aggressive, labs can withdraw access; (b) political pressure can redirect priorities (the Trump-era gutting of the US AISI demonstrates this risk); (c) cultural capture via close working relationships with lab safety teams.

**US counterpart (NIST/CAISI):** The US AI Safety Institute was effectively gutted under the Trump administration (renamed, director departed, staff cuts). Demonstrates that government evaluators face political capture risk even if they're structurally independent from industry.

---

### 8.10 Case Study: METR (Government-Adjacent Nonprofit)

| Attribute | Detail |
|-----------|--------|
| Founded | 2023 (originally ARC Evals, spun out of ARC) |
| Focus | Dangerous capability evaluations (autonomous replication, resource acquisition) |
| Funding | Grants (Open Philanthropy, others) |
| Key people | Beth Barnes (founder) |

**What they do:** Evaluate whether frontier models can autonomously acquire resources, replicate, or cause catastrophic harm. Pre-deployment evaluations for frontier labs.

**Capture resistance:** METR explicitly **refuses payment from AI labs** to maintain independence. Funded by philanthropic grants. This is the strongest independence model in the ecosystem but depends on continued grant funding.

**Limitation:** Labs cooperate voluntarily — METR has no legal right to access or test models. If a lab refuses to engage, METR cannot compel evaluation.

---

### 8.11 Case Study: Apollo Research (Nonprofit Safety Evaluator)

| Attribute | Detail |
|-----------|--------|
| Founded | 2023, London |
| Focus | AI deception and scheming behavior |
| Founder | Marius Hobbhahn (Time 100 AI 2025) |
| Funding | Grants |

**What they do:** Specialize in detecting whether AI models engage in deceptive behavior — scheming, sandbagging (performing poorly on safety evals to avoid restrictions), and strategic deception. Published influential research on frontier model deception capabilities.

**Capture risk:** Low. Grant-funded nonprofit with narrow adversarial focus. But faces the same access-dependency problem as METR.

---

### 8.12 Case Study: Internal Lab Evaluation Teams

| Lab | Team | Lead | Framework |
|-----|------|------|-----------|
| OpenAI | Preparedness | Aleksander Madry | Preparedness Framework v2 (scorecard system) |
| Anthropic | Frontier Red Team | Jared Kaplan (RSO) | Responsible Scaling Policy v3.0 |
| Google DeepMind | Frontier Safety | (multiple) | Frontier Safety Framework v3 (Sep 2025) |
| Meta | Purple Llama | (multiple) | CyberSecEval (open-source), CrowdStrike collab |

**Capture:** Structural by design — these teams report to the same organization they evaluate. Their purpose is internal risk management, not independent oversight. Key tensions: (a) safety teams compete for resources with product teams; (b) safety findings that delay launches create organizational pressure to soften conclusions; (c) the Timnit Gebru case at Google demonstrates what happens when internal evaluation conflicts with commercial priorities.

**Relationship to external evaluators:** Internal teams often coordinate with external evaluators (METR, AISI) for pre-deployment testing, but the lab controls access, scope, and publication timing. External evaluators supplement but do not replace internal evaluation.

---

## Part 9: Capture Dynamics — Cross-Sector Framework

### 9.1 Five Structural Enablers of Evaluator Capture

Drawing from financial auditing (Arthur Andersen/SOX), credit rating agencies (2008 crisis/Dodd-Frank), cybersecurity compliance (SOC 2/PCI-DSS), and AI evaluation:

**1. "Evaluated Entity Pays" Funding Model**

| Sector | Who Pays | Capture Severity |
|--------|----------|-----------------|
| Financial auditing | Auditee pays auditor | High (pre-SOX), moderate (post-SOX) |
| Credit ratings | Issuer pays rater | Very high (pre-2008), high (post-Dodd-Frank) |
| Cybersecurity audits | Auditee pays auditor | High (no reforms) |
| AI evaluation (benchmark) | Labs pay for premium access + compute | High |
| AI evaluation (compliance) | Enterprise/lab pays auditor | Very high |
| AI evaluation (govt/nonprofit) | Government/grants | Low |

Every sector where the evaluated entity pays the evaluator develops capture over time. The severity is modulated by oversight bodies and result transparency.

**2. Revolving Door**

The AI talent pipeline is especially severe: AI labs pay 3-10x academic salaries. Evaluators who plan to join labs (or whose students want lab jobs) have career incentives to maintain good relationships. Specific documented dynamics:
- HELM contributors → AI lab positions
- Academic benchmark designers → industry research scientist roles
- Government safety institute staff → lab safety teams

Creates both anticipatory bias (soften assessments to preserve employment options) and knowledge transfer (former evaluators help labs game future evaluations).

**3. Information Asymmetry / Access Dependency**

This is the **most severe** capture vector in AI, and unique among analogous sectors:
- Financial auditing: auditors have **legal rights** to access all financial records (securities law). Obstruction is criminal.
- Credit ratings: issuers must provide material information to maintain investment-grade ratings.
- Cybersecurity: pen-testers negotiate scope but have contracted access once engaged.
- **AI evaluation: evaluators have NO legal right to access model internals, training data, or deployment logs.** Access is entirely at the lab's discretion. Labs can provide black-box API access while withholding weights, training data, RLHF reward models, and internal safety evaluations.

This gives labs effective veto power over evaluation scope and timing.

**4. Evaluator Concentration**

| Sector | Major Evaluators | Dynamic |
|--------|-----------------|---------|
| Financial auditing | 4 (Big Four) | "Too big to sanction" |
| Credit ratings | 3 (Moody's, S&P, Fitch) | ~95% market share |
| Cybersecurity | Fragmented | Race to bottom on quality |
| AI evaluation | ~5-10 credible orgs, consolidating fast | Early-stage; acquisitions reducing count |

Paradox: high concentration creates too-big-to-sanction; low concentration enables audit shopping and quality race-to-bottom. Optimal: moderate concentration + strong accreditation (CREST model in cybersecurity, PCAOB in financial auditing).

**5. Transparency of Results**

- Financial auditing: audit opinions are **public** (SEC filings)
- Credit ratings: ratings are **public**
- Cybersecurity: SOC 2 reports are **restricted** (shared only with customers)
- AI evaluation: benchmark results typically **public**, but evaluation methodology, scope limitations, and failed tests often **under NDA**. Safety evaluation results frequently restricted.

### 9.2 Historical Capture Case: Arthur Andersen / Enron

The most relevant historical analogy for AI evaluator capture.

**How capture worked:**
- Andersen earned $25M/year from Enron for auditing and $27M/year for consulting — consulting revenue exceeded audit revenue
- Andersen designed the accounting systems it then audited (equivalent to: an AI evaluator that also consults on model development)
- Enron's CFO and Chief Accounting Officer were former Andersen employees (revolving door)
- Andersen partners embedded at Enron adopted Enron's culture (cultural capture)
- When SEC investigation began, Andersen destroyed audit documents

**Sarbanes-Oxley reforms (2002):** Created PCAOB, prohibited most non-audit services to audit clients, required lead partner rotation every 5 years. Academic evidence: improved audit quality initially but gains plateaued. Core "auditee pays" model was NOT changed.

### 9.3 Historical Capture Case: Credit Rating Agencies / 2008

**How the "issuer pays" model created capture:**
- By mid-2000s, structured finance ratings = ~50% of Moody's revenue
- Rating shopping: issuers approached multiple agencies, chose the most favorable
- Agencies published models; banks reverse-engineered them to barely meet thresholds ("ratings arbitrage")
- Internal emails: "Let's hope we are all wealthy and retired by the time this house of cards falters" (S&P analyst, FCIC report)

**Bolton, Freixas & Shapiro (2012):** Showed counter-intuitively that **more competition among rating agencies makes inflation worse** because issuers can more easily shop for favorable ratings.

**Dodd-Frank reforms:** Created SEC Office of Credit Ratings, but **did NOT change the issuer-pays model**. An assignment system (centralized body assigns raters to deals) was proposed but killed by industry lobbying.

### 9.4 Cybersecurity Compliance as Analogy

SOC 2, ISO 27001, and PCI-DSS audits share the "auditee pays" model with AI evaluation. Key parallels:
- **Audit shopping:** Companies switch auditors after unfavorable results (documented in North Carolina State study, 2019)
- **Compliance theater:** Target (2013), Home Depot (2014), and Heartland (2008) were all PCI-DSS compliant when breached
- **No public reporting:** SOC 2 reports are restricted; opacity enables weak audits
- **No PCAOB equivalent:** Cybersecurity auditing is voluntary and unregulated (except PCI-DSS for payment processors)

The AI evaluation space currently resembles pre-SOX financial auditing or current cybersecurity auditing: voluntary, unregulated, structurally prone to capture.

### 9.5 Capture Resistance Mechanisms (Cross-Sector Lessons)

| Mechanism | Source Sector | AI Applicability |
|-----------|--------------|-----------------|
| Independent oversight board (PCAOB) | Financial auditing | High — "AI PCAOB" frequently proposed |
| Mandatory evaluator rotation | Financial auditing (EU) | Moderate — could work for frontier model evals |
| Legal access rights for evaluators | Financial auditing (securities law) | Critical need — requires legislation |
| Public disclosure of evaluation results | Financial auditing (SEC filings) | High — transparency is partial remedy |
| Separation of evaluation and consulting | SOX Section 201 | High — evaluators should not also advise labs |
| Assignment system (break shopping) | Proposed but rejected for CRAs | Novel — centralized body assigns evaluators |
| Accreditation of evaluators | CREST (cybersecurity) | High — establishes quality floor |
| Evaluator-funded-by-third-party | METR model / pre-1970s CRAs | Ideal but economically challenging at scale |

### 9.6 Implications for Simulation

**Mapping to the evaluator-as-organization model (Parts 2-6 above):**

The current simulation models evaluator capture through a single axis: premium access (provider pays evaluator → gets extra trials + early access). The real-world evidence suggests capture operates through at least **five distinct channels**, and the simulation could benefit from encoding more of them:

1. **Funding dependency** (already modeled via premium subscriber revenue) — the ratio of provider-fee revenue to total revenue is the key capture metric. The credit rating agency evidence suggests this alone is a strong predictor.

2. **Access dependency** (not modeled) — evaluators depend on labs for model access. A lab that withdraws cooperation can effectively shut down evaluation. This is unique to AI and is the most severe capture vector.

3. **Scope negotiation** (partially modeled via benchmark design) — labs negotiate what gets evaluated. An evaluator that insists on broad scope loses clients. In the simulation, this could manifest as evaluators avoiding safety-focused benchmarks to retain premium subscribers.

4. **Revolving door** (not modeled) — evaluator staff moving to labs creates anticipatory bias. Could be modeled as a parameter that softens evaluator assessment rigor over time when evaluator depends on lab-funded revenue.

5. **Cultural capture** (not modeled) — evaluators who spend time with labs adopt shared assumptions. This is the subtlest form and hardest to model explicitly.

**The key structural insight from cross-sector evidence:** The "auditee pays" model is the single most reliable predictor of eventual capture, and **no sector has successfully reformed it**. SOX didn't change it for financial auditing. Dodd-Frank didn't change it for credit ratings. The only working alternative is third-party funding (METR model, government evaluation), but this doesn't scale to cover all evaluation needs.

For the simulation: the most impactful parameter is the evaluator's funding source mix. Government/foundation funding → more independence. Provider fees → more capture. The interaction between funding source and benchmark design choices (which dimensions get measured) is where the most interesting dynamics should emerge.

---

## Document History

- **2026-02-16:** Initial design based on Leaderboard Illusion paper and LMArena business model
- **2026-02-18:** Updated to reflect actual implementation — corrected `compute_n_trials` formula (binary not gradient funding_bonus), updated config params to match `SimulationConfig`, corrected funding model signatures; implemented Phase 3 item 2 (`_get_effective_benchmark()` with 1.5x exploitability multiplier for early access window); corrected Phase 5 checklist (both logging and dashboard were already implemented)
- **2026-04-05:** Added Parts 8-9: Evaluator landscape survey (12 case studies across 5 archetypes) and cross-sector capture dynamics framework (financial auditing, credit ratings, cybersecurity). 35+ organizations mapped. Five structural enablers of capture identified. Simulation implications documented.
