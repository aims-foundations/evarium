# Case Study: US vs EU AI Policy Approaches
## Modeling Regulatory Philosophy in the Evaluation Ecosystem Simulation

**Last Updated:** 2026-02-18
**Status:** Active — parameters implemented and calibrated
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

## Part 1.5: Empirical Enforcement Record — LLM/GenAI Focus (2024–2026)

This section grounds model parameters in observed regulatory behavior specifically targeting LLMs and generative AI products. Non-AI enforcement (general GDPR, antitrust) is excluded except where it directly informs LLM enforcement patterns.

---

### EU Enforcement on LLMs: Early but Accelerating

**The first GenAI fine in the EU — Italy Garante vs. OpenAI/ChatGPT (December 2024):**
- Italy's data protection authority (Garante) opened a probe in March 2023 after a ChatGPT data breach, temporarily banning the service before OpenAI restored it with compliance changes.
- After ~21 months of investigation, Garante issued a **€15 million fine** against OpenAI (December 20, 2024) — the first GDPR fine specifically targeting a generative AI product.
- Violations: no lawful basis for training data, insufficient transparency to users, no age verification to protect minors, failure to notify the Garante of the March 2023 breach.
- Ancillary remedy: OpenAI must run a 6-month public information campaign in Italian media.
- OpenAI is appealing, calling the fine "disproportionate" and noting it is nearly 20x its Italian revenue during the period.
- **Timeline:** March 2023 breach → December 2024 fine = ~21 months. Fast by EU standards.

**EU AI Act: zero AI Act fines as of February 2026.**
- Prohibited practices (e.g., social scoring, manipulative AI) enforceable since **February 2, 2025**.
- GPAI/LLM obligations (transparency, systemic risk assessments) enforceable since **August 2, 2025**.
- The EU AI Office can fine up to **€35M or 7% of global turnover** for systemic-risk GPAI non-compliance.
- As of February 2026, no national authority has issued an AI Act fine. Pattern mirrors GDPR: first GDPR fine appeared ~8 months post-entry-into-force; large fines took 3–5 years.

**EU AI Office — formal investigations (ongoing, 2026):**
- **X / Grok deepfakes (January–February 2026):** EU Commission opened formal DSA proceedings against X after Grok generated >3 million sexualized images in under two weeks, including ~23,000 depicting minors. Maximum potential fine: ~$174M (DSA: 6% global revenue). No fine issued yet; investigation ongoing. X was already fined **€120M** (December 2025) under DSA for advertising transparency violations — a separate action not specific to Grok.
- **Meta GPAI (January 2026):** EU AI Office launched a formal GPAI investigation into Meta's WhatsApp Business APIs. Meta refused to sign the voluntary AI Code of Practice, leaving it exposed to "Ecosystem Investigations" with up to 7% global turnover fines.
- **Systemic-risk designations:** Any model trained with ≥10²⁵ FLOPs (covers GPT-4-class models, Gemini, Grok) is presumed systemic-risk; providers must submit safety evaluations, incident reports, and technical documentation to the AI Office.
- **Cooperative posture of others:** Amazon, Anthropic, Google, IBM, Microsoft, OpenAI all signed the GPAI Code of Practice by December 2025, reducing (but not eliminating) investigation risk.

**EU enforcement timelines for LLM-specific cases:**
- Italy Garante vs. OpenAI: **~21 months** (breach → fine)
- EU AI Act fines: **not yet issued** (framework operational August 2025; early cases expected 2026–2027)
- EU DSA (centralized): ~13 months based on prior DMA actions; Grok investigation opened January 2026

**Summary of EU LLM-specific enforcement:**
| Action | Date | Fine / Outcome |
|---|---|---|
| Italy Garante — ChatGPT temporary ban | March 2023 | Operational ban (lifted after compliance changes) |
| Italy Garante — ChatGPT GDPR fine | December 2024 | €15M + public campaign |
| X DSA — blue checkmark / user data | December 2025 | €120M |
| EU AI Office — X/Grok deepfakes | January 2026 | Investigation ongoing (potential ~$174M) |
| EU AI Office — Meta GPAI | January 2026 | Investigation ongoing |
| EU AI Act fines (any provider) | — | None issued as of Feb 2026 |

---

### US Enforcement on LLMs: Targeted but Structurally Limited

**FTC Operation AI Comply (September 2024):** Five simultaneous enforcement actions against AI companies making deceptive claims:
- **DoNotPay** ("world's first robot lawyer"): $193K fine + advertising restrictions. No real AI legal capability.
- **Rytr**: Charged with enabling fake review generation. Consent order issued 2024. Notably, the Trump administration FTC **set aside the Rytr consent order** in December 2025, citing the AI Action Plan's innovation-first directive — a direct signal of US regulatory retreat on AI.
- **IntelliVision** (facial recognition): Final order January 2025 — barred from making unsubstantiated accuracy claims.
- **Evolv Technologies** (security scanning): Settled December 2024 — banned from unsubstantiated claims; K-12 customers given contract exit option.
- Fine sizes: $193K–$15M. None targeted major LLM providers (OpenAI, Google, Anthropic, Meta).

**FTC AI chatbot inquiry (September 2025):**
- FTC issued Section 6(b) orders to **Alphabet, CharacterAI, Instagram, Meta, OpenAI, Snapchat, and xAI** — information-gathering on chatbot safety for children/teens.
- This is a data collection/inquiry, not an enforcement action. No fines issued. Outcome TBD.

**What has NOT happened in the US (as of February 2026):**
- No major LLM provider (OpenAI, Anthropic, Google, Meta) has received a US federal fine specifically for AI harms.
- No LLM product has been banned or had a US-mandated product restriction.
- The Trump January 2025 Executive Order reversed Biden-era AI safety policies and preempted state AI laws — further reducing enforcement pressure on LLM providers at the federal level.
- States (California, Colorado, Texas) have proposed AI bills; enforcement from state AGs has been minimal for LLMs specifically.

**Fine size as % revenue — LLM-specific cases:**
| Fine | As % Revenue |
|---|---|
| Italy: OpenAI €15M GDPR | ~20x Italian revenue (OpenAI's own estimate) |
| US: DoNotPay $193K FTC | Negligible — small company |
| US: Major LLM provider fine | None issued |

**Key structural difference (EU vs US):**
- EU enforced against the dominant LLM product (ChatGPT) within 21 months of a triggering incident, resulting in a real monetary fine.
- US FTC has only fined small AI companies making deceptive claims; enforcement against frontier LLM providers remains absent.
- US has *structurally* retreated from AI enforcement since January 2025 (EO reversal, Rytr consent order set aside).
- EU is actively building case law for LLMs while enforcement machinery (AI Act) ramps up through 2026.

---

### Calibration Implications for the Model

| Parameter | EU Empirical Basis | US Empirical Basis |
|---|---|---|
| `intervention_cooldown` | 2 rounds — Italy acted within 21 months; EU AI Office opened Grok investigation within weeks of deepfake reports | 5 rounds — FTC chatbot inquiry issued Sept 2025, no outcome yet; no major LLM fines at all |
| `sanction_fine_multiplier` | 0.35 — €15M was ~20x OpenAI's Italian revenue; AI Act ceiling is 7% global turnover | 0.10 — largest AI-specific US fine was $193K; no fine for frontier LLM providers |
| `sanction_incident_threshold` | 2 — Italy acted on a single breach + pattern of transparency failures | 4 — US has not sanctioned any LLM provider even after multiple documented harm incidents |
| `sanction_duration` | 4 rounds — OpenAI's Italy remedy includes ongoing 6-month campaign; compliance cycles are lengthy | 2 rounds — US consent decrees shorter, and even those are being reversed (Rytr) |
| `mandate_risk_threshold` | 0.50 — EU AI Office mandates systemic-risk assessments at moderate compute thresholds | 0.75 — US has no mandate framework for LLMs; prefers voluntary codes |
| `sanction_min_severity` | "major" — Italy acted on a data breach that was not catastrophic (no mass harm, internal bug) | "critical" — US only likely to act after documented critical harm at scale |

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

### Implemented Parameter Set (as of 2026-02-18)

The following parameters control policymaker intervention style. All are implemented in `Policymaker.__init__()` and used in `_plan_heuristic()`. Presets are defined in `simulation.POLICYMAKER_PRESETS`.

| Parameter | Type | US Value | Balanced | EU Value | Empirical Basis |
|-----------|------|----------|----------|----------|-----------------|
| `intervention_threshold` | float (0-1) | 0.75 | 0.50 | 0.35 | EU acts at moderate risk; US waits for high risk |
| `risk_tolerance` | float (0-1) | 0.70 | 0.50 | 0.20 | EU: low; US: high (innovation-first) |
| `intervention_cooldown` | int (rounds) | **5** | 3 | **2** | EU: 6-12 mo cycles; US: 18-36 mo FTC cycle |
| `sanction_fine_multiplier` | float | **0.10** | 0.22 | **0.35** | EU: larger bite (7% turnover); US: consent-order-only |
| `sanction_incident_threshold` | int | **4** | 3 | **2** | EU: 2+ incidents trigger; US: needs clear pattern |
| `sanction_duration` | int (rounds) | **2** | 3 | **4** | EU: lengthy compliance cycles; US: short consent decrees |
| `mandate_risk_threshold` | float (0-1) | **0.75** | 0.62 | **0.50** | EU: ex-ante mandates; US: almost never mandates |
| `sanction_min_severity` | str | **"critical"** | "major" | **"major"** | US only acts on critical incidents; EU acts on major+ |

**Parameters planned but not yet implemented** (from original proposal):
- `compliance_burden` — documentation/testing opportunity cost
- `ex_ante_requirements` — pre-deployment gate (EU AI Act model)
- `independent_audit_threshold` — third-party audit trigger
- `market_intervention_enabled` — operating restrictions / market bans

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
- ✅ Configurable intervention cooldown (per-preset: EU=2, US=5)

### Tier 2 (Implemented)

#### 2A. Sanctions and Fines System ✅
**Implemented:** `sanctions_and_fines` action in `actors/policymaker.py`
- Fine formula: `min(0.4, sanction_fine_multiplier × market_share × (1 - risk_tolerance))`
- Condition 1: critical incident after public warning
- Condition 2: accumulated incidents (>= sanction_incident_threshold, severity >= sanction_min_severity) after investigation
- Applied in `simulation.py`: reduces `funding_multiplier` for sanctioned provider in next round
- Duration configurable per preset (EU=4 rounds, US=2 rounds)

**Calibrated presets** drive EU/US divergence without special-casing:
- EU fine (60% share): ~16.8% R&D efficiency reduction
- US fine (60% share): ~1.8% R&D efficiency reduction (and rarely triggered due to higher thresholds)

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
- **2026-02-18:** Part 1.5 added — empirical enforcement record (general tech/GDPR)
- **2026-02-18:** Part 1.5 revised — narrowed to LLM/GenAI-specific enforcement (2024–2026 only)
