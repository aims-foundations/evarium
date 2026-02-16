# Case Study: US vs EU AI Policy Approaches
## Modeling Regulatory Philosophy in the Evaluation Ecosystem Simulation

**Last Updated:** 2026-02-16
**Status:** Planning Document
**Related Tasks:** Goal 1 - Policymaker Intervention Control

---

## Executive Summary

This document analyzes the fundamental differences between US and EU approaches to AI regulation and proposes how to model these distinct philosophies in the evaluation ecosystem simulation. The goal is to create configurable parameters that allow researchers to explore how different regulatory styles affect gaming dynamics, consumer welfare, and ecosystem health.

---

## Part 1: Real-World Policy Approaches

### EU Approach: Precautionary Regulation

**Core Philosophy:** Rights-protection and risk prevention
**Regulatory Model:** Ex-ante (before deployment) comprehensive framework

#### Key Characteristics

1. **Risk-Based Framework**
   - Four-tier risk classification: unacceptable, high, limited, minimal
   - Risk defined as: probability of harm × severity of harm
   - Graduated obligations based on risk level

2. **Mandatory Compliance Requirements (High-Risk Systems)**
   - Risk management systems throughout AI lifecycle
   - High-quality datasets with bias testing
   - Detailed technical documentation
   - Human oversight and transparency
   - Post-market monitoring
   - Incident reporting systems

3. **Enforcement & Penalties**
   - Severe fines: up to €35M or 7% of global annual turnover
   - Prohibition of certain AI practices (unacceptable risk)
   - Clear enforcement mechanisms with regulatory bodies

4. **Implementation Timeline**
   - EU AI Act entered force: August 1, 2024
   - Phased rollout: Aug 2024 - Feb 2027
   - Prohibited practices: Feb 2, 2025
   - Full applicability: Aug 2, 2026

5. **Precautionary Principle**
   - Regulate potential harms before they occur
   - Err on side of caution
   - Protect fundamental rights proactively

**Sources:**
- [EU AI Act Official](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
- [High-level AI Act Summary](https://artificialintelligenceact.eu/high-level-summary/)
- [Risk-Based Approach Primer (RAND)](https://www.rand.org/pubs/research_reports/RRA3243-3.html)

---

### US Approach: Light-Touch Innovation Focus

**Core Philosophy:** Technological dominance and competitiveness
**Regulatory Model:** Ex-post (after problems emerge) minimal oversight

#### Key Characteristics

1. **Innovation-First Policy**
   - Explicit goal: "US must win the AI race"
   - Remove barriers to American AI leadership
   - January 2025 Executive Order reversed previous AI safety policies
   - Focus on accelerating innovation, building infrastructure, international leadership

2. **Industry Self-Regulation**
   - Voluntary codes of conduct encouraged
   - Public-private collaboration emphasized
   - Minimal federal mandates
   - Companies "free to innovate without cumbersome regulation"

3. **Federal Preemption Strategy**
   - Active effort to override state-level AI regulations
   - Concern about "patchwork of 50 different regulatory regimes"
   - Centralized light-touch approach preferred over diverse state rules

4. **Limited Enforcement**
   - Enforcement mentioned only for export controls and biosecurity
   - No comprehensive penalty framework
   - Market-driven accountability

5. **Ex-Post Problem Solving**
   - Address issues after they emerge
   - Reactive rather than proactive
   - Market correction as primary mechanism

**Notable Contrast:**
Some US states (California, Colorado, New York) have enacted AI-specific regulations that mirror EU's risk-based approach, creating tension with federal preemption strategy.

**Sources:**
- [White House AI Policy Framework](https://www.whitehouse.gov/presidential-actions/2025/12/eliminating-state-law-obstruction-of-national-artificial-intelligence-policy/)
- [Trump AI Executive Order Analysis (Squire Patton Boggs)](https://www.squirepattonboggs.com/insights/publications/key-insights-on-president-trumps-new-ai-executive-order-and-policy-regulatory-implications/)
- [Federal AI Regulation Overview (Pillsbury)](https://www.pillsburylaw.com/en/news-and-insights/new-executive-order-national-policy-framework-artificial-intelligence.html)

---

## Part 2: Fundamental Differences Summary

| Dimension | US Light-Touch | EU Precautionary |
|-----------|----------------|------------------|
| **Timing** | Ex-post (after incidents) | Ex-ante (before deployment) |
| **Philosophy** | Innovation & competitiveness | Rights protection & safety |
| **Mechanism** | Voluntary self-regulation | Mandatory compliance |
| **Enforcement** | Minimal federal oversight | Severe penalties (€35M / 7% revenue) |
| **Speed** | Reactive, slow interventions | Proactive, rapid enforcement |
| **Scope** | Targeted, minimal | Comprehensive, risk-based |
| **Burden** | Light documentation | Extensive testing & documentation |
| **Market Intervention** | Rare, market-driven | Permitted (operating restrictions, bans) |
| **Risk Tolerance** | High (move fast, fix later) | Low (prevent harm upfront) |

---

## Part 3: Mapping to Simulation Parameters

### Proposed Parameter Set

The following parameters would control policymaker intervention style:

| Parameter | Type | US Value | Balanced | EU Value | Description |
|-----------|------|----------|----------|----------|-------------|
| `intervention_philosophy` | enum | "light_touch" | "balanced" | "precautionary" | Preset that configures others |
| `intervention_threshold` | float (0-1) | 0.75 | 0.50 | 0.35 | Evidence/risk level needed to trigger action |
| `intervention_cooldown` | int (rounds) | 6 | 3 | 2 | Minimum rounds between interventions |
| `enforcement_stringency` | float (0-1) | 0.25 | 0.50 | 0.85 | Penalty severity multiplier |
| `compliance_burden` | float (0-1) | 0.15 | 0.40 | 0.75 | Documentation/testing opportunity cost |
| `ex_ante_requirements` | bool | False | False | True | Require pre-deployment compliance vs post-incident |
| `mandatory_safety_threshold` | float (0-1) | 0.80 | 0.60 | 0.40 | Risk level triggering mandatory safety evals |
| `independent_audit_threshold` | float (0-1) | 0.90 | 0.70 | 0.50 | Risk level triggering independent audits |
| `sanction_escalation_rate` | float (0-1) | 0.30 | 0.50 | 0.75 | How quickly to climb sanctions ladder |
| `market_intervention_enabled` | bool | False | False | True | Allow operating restrictions/market bans |

### Parameter Interpretation

#### intervention_threshold (0-1)
- **US (0.75):** Only intervene when risk beliefs are very high; give industry benefit of doubt
- **EU (0.35):** Intervene at moderate risk levels; precautionary stance
- **Effect:** Controls when first intervention triggers

#### intervention_cooldown (rounds)
- **US (6 rounds):** Slower regulatory cycle; give companies time to respond
- **EU (2 rounds):** Rapid follow-up; aggressive enforcement
- **Effect:** Controls regulatory tempo and pressure

#### enforcement_stringency (0-1)
- **US (0.25):** Light fines, warnings, mostly reputational damage
- **EU (0.85):** Heavy economic penalties, real consequences
- **Effect:** Multiplier on fine amounts and compliance costs

#### compliance_burden (0-1)
- **US (0.15):** Minimal documentation requirements; low opportunity cost
- **EU (0.75):** Extensive testing, audits, documentation; high opportunity cost
- **Effect:** Reduces provider R&D efficiency when under compliance requirements

#### ex_ante_requirements (bool)
- **US (False):** Providers can deploy first, regulate later if problems emerge
- **EU (True):** Must meet requirements before deployment (pre-approval gate)
- **Effect:** Slows model releases, requires safety benchmarks upfront

#### mandatory_safety_threshold (0-1)
- **US (0.80):** Only mandate safety evals at extreme risk
- **EU (0.40):** Mandate safety evals at moderate risk
- **Effect:** Triggers requirement for safety benchmark compliance

#### independent_audit_threshold (0-1)
- **US (0.90):** Almost never commission independent audits (prohibitively high bar)
- **EU (0.50):** Commission audits when moderate-high risk detected
- **Effect:** Triggers third-party evaluation (exposes gaming directly)

#### sanction_escalation_rate (0-1)
- **US (0.30):** Slow escalation; many chances before serious consequences
- **EU (0.75):** Rapid escalation; quickly move from warning to fines to restrictions
- **Effect:** Controls speed through graduated sanctions ladder

#### market_intervention_enabled (bool)
- **US (False):** No market bans or operating restrictions (antitrust is separate)
- **EU (True):** Can impose funding caps, market share caps, or prohibit deployment
- **Effect:** Enables most severe regulatory consequences

---

## Part 4: Implementation Requirements

### Tier 1 (Already Implemented)
- ✅ Market concentration monitoring & review
- ✅ Information requests (pre-investigation)
- ✅ Threshold signaling (public announcements)
- ✅ Basic intervention cooldown

### Tier 2 (New - Medium Complexity)

#### 2A. Sanctions and Fines System
**Requirements:**
- Provider revenue/capital tracking (new)
- Fine calculation: `base_fine × enforcement_stringency × (market_share OR revenue)`
- Option to redirect fines to fund independent evaluations
- Compliance failure detection (ignored information requests, gaming after mandates)

**Economic Impact:**
- Fines reduce provider capital
- Capital constraints limit R&D investment
- Creates real deterrent beyond reputation damage

#### 2B. Mandatory Safety Evaluations
**Requirements:**
- Safety benchmark dimension (separate from capability)
- Trigger: `gaming_risk > mandatory_safety_threshold`
- Mandate providers run safety benchmarks (adversarial robustness, jailbreak resistance, fairness)
- Non-compliance results in fines + escalation

**Implementation Options:**
1. Add safety benchmarks to existing benchmark suite
2. Create separate "safety_score" dimension
3. Safety investment affects safety scores (existing `safety_alignment` portfolio allocation)

### Tier 3 (New - High Complexity)

#### 3A. Third-Party Independent Evaluations
**Requirements:**
- Policymaker budget system (capital for audits)
- Independent evaluation mechanism (simulation-run, not provider-submitted)
- Trigger: `gaming_risk > independent_audit_threshold AND (high_score + low_satisfaction)`
- Results publicly disclosed → high credibility signal to consumers

**Design:**
- Audit reveals true capability vs published score gap
- Publicly exposes gaming (not just suspected)
- Expensive for policymaker (budget constraint)

#### 3B. Graduated Sanctions Ladder
**Escalation Path:**
1. **Information Request** → 5% opportunity cost, 2-round deadline
2. **Investigation** → 10% opportunity cost, reputation hit
3. **Public Warning** → Reduces consumer leaderboard_trust
4. **Mandate + Fine** → Benchmark requirements + 10% revenue fine
5. **Operating Restrictions** → Funding cap (50% reduction) OR market share cap
6. **Market Ban** → Provider cannot deploy new models (game over)

**Requirements:**
- Track escalation state per provider
- `sanction_escalation_rate` controls trigger thresholds for each step
- `market_intervention_enabled` gates steps 5-6
- Economic model (revenue, capital constraints)

---

## Part 5: Experimental Hypotheses

### Research Questions

**RQ1:** Does EU-style precautionary regulation reduce gaming more effectively than US light-touch?
- **Prediction:** EU reduces eval engineering investment but may slow capability growth

**RQ2:** How do intervention philosophies affect consumer welfare?
- **Prediction:** EU improves satisfaction (less gaming) but slower innovation; US higher capability ceiling but more disappointment

**RQ3:** Do sanctions/fines change provider strategy mix?
- **Prediction:** Economic penalties create stronger deterrent than reputational damage alone

**RQ4:** What is the optimal balance between innovation velocity and consumer protection?
- **Prediction:** Balanced approach with moderate thresholds outperforms both extremes

**RQ5:** Do ex-ante requirements prevent gaming or just slow deployment?
- **Prediction:** Ex-ante creates safety compliance overhead but catches problems earlier

**RQ6:** How does regulatory philosophy interact with funder behavior?
- **Prediction:** VCs avoid heavily regulated providers; government funders favor compliant providers

---

## Part 6: Next Steps

### Planning Phase
- [ ] Finalize parameter mappings
- [ ] Design provider economic model (revenue, capital, fines)
- [ ] Design safety benchmark system (separate dimension)
- [ ] Design policymaker budget constraints
- [ ] Define graduated sanctions ladder mechanics

### Implementation Phase
- [ ] Add intervention philosophy parameters to Policymaker.__init__
- [ ] Implement US/EU/balanced presets
- [ ] Implement sanctions and fines (Tier 2A)
- [ ] Implement mandatory safety evaluations (Tier 2B)
- [ ] Implement third-party audits (Tier 3A)
- [ ] Implement graduated sanctions ladder (Tier 3B)
- [ ] Add economic constraints to providers

### Testing Phase
- [ ] Run US vs EU comparison experiments
- [ ] Validate parameter ranges produce realistic behavior
- [ ] Test escalation ladder progression
- [ ] Measure impact on gaming, satisfaction, capability growth

### Documentation Phase
- [ ] Update stakeholders.md with new policymaker tiers
- [ ] Document parameter presets in simulation.py
- [ ] Create experiment templates for policy comparison studies
- [ ] Add US vs EU case study to experiment gallery

---

## Appendix: Related Reading

### EU AI Act
- [Official EU AI Act Text](https://artificialintelligenceact.eu/)
- [Risk Classification Guide](https://gdprlocal.com/ai-risk-classification/)
- [Compliance Requirements Summary](https://www.modelop.com/ai-governance/ai-regulations-standards/eu-ai-act)

### US AI Policy
- [America's AI Action Plan](https://www.whitehouse.gov/presidential-actions/2025/12/eliminating-state-law-obstruction-of-national-artificial-intelligence-policy/)
- [Federal Preemption Strategy](https://www.bipc.com/new-executive-order-signals-federal-preemption-strategy-for-state-laws-on-artificial-intelligence)
- [State-Level AI Regulation](https://carta.com/blog/ai-regulation/)

### Academic Analysis
- [RAND: Risk-Based AI Regulation](https://www.rand.org/pubs/research_reports/RRA3243-3.html)
- [Chicago Law Review: Comparing EU & US](https://businesslawreview.uchicago.edu/online-archive/comparing-eu-ai-act-proposed-ai-related-legislation-us)

---

## Document History

- **2026-02-16:** Initial research and parameter mapping
- **Future:** Implementation notes, experimental results, calibration
