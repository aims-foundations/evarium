# EU vs US Regulatory Philosophy

## 1. Policy anchor

Two divergent regulatory philosophies shape the frontier-AI policy landscape.

### 1.1 EU: Precautionary regulation

**Core philosophy:** rights protection and risk prevention.
**Model:** ex-ante (before deployment) comprehensive framework.

Key elements:

- Four-tier risk classification (unacceptable / high / limited / minimal); risk = probability × severity.
- Mandatory compliance for high-risk: risk management, dataset quality, documentation, human oversight, post-market monitoring, incident reporting.
- Fines up to **€35M or 7% of global annual turnover**.
- EU AI Act entered force 1 Aug 2024; prohibited practices effective 2 Feb 2025; GPAI obligations effective 2 Aug 2025; full applicability 2 Aug 2026.
- Precautionary principle: regulate potential harms before they occur.

### 1.2 US: Light-touch innovation focus

**Core philosophy:** technological dominance and competitiveness.
**Model:** ex-post (after problems emerge) minimal oversight.

Key elements:

- January 2025 Executive Order reversed previous AI safety policies; explicit "win the AI race" framing.
- Voluntary codes; public-private collaboration; minimal federal mandates.
- Federal preemption strategy actively overrides state regulations.
- Limited enforcement (export controls + biosecurity only).
- Ex-post problem solving; market correction primary mechanism.

Notable state-level contrast: California (SB 53), Colorado, and New York (RAISE) have enacted AI-specific regulation that mirrors the EU's risk-based approach. Creates tension with federal preemption strategy.

## 2. Empirical enforcement record (LLM-specific, 2024–2026)

### 2.1 EU: early but accelerating

| Action | Date | Outcome |
|---|---|---|
| Italy Garante — ChatGPT temporary ban | March 2023 | Operational ban (lifted after compliance changes) |
| Italy Garante — ChatGPT GDPR fine | December 2024 | **€15M + 6-month public campaign** |
| X DSA — advertising transparency | December 2025 | €120M |
| EU AI Office — X/Grok deepfakes | January 2026 | Investigation ongoing (potential ~$174M under DSA 6% global revenue) |
| EU AI Office — Meta GPAI | January 2026 | Investigation ongoing (up to 7% global turnover) |
| EU AI Act fines | — | **None issued as of Feb 2026** |

The Italy Garante fine (Dec 2024) was the first GDPR fine specifically targeting generative AI. Violations: no lawful basis for training data, insufficient transparency, no age verification, failure to notify of March 2023 breach. Timeline: ~21 months breach to fine (fast by EU standards). OpenAI appealing; fine ≈ 20× OpenAI's Italian revenue during the period.

EU AI Act enforcement mirrors the GDPR ramp pattern: first GDPR fine appeared ~8 months post-entry; large fines took 3–5 years.

Amazon, Anthropic, Google, IBM, Microsoft, OpenAI signed the GPAI Code of Practice by Dec 2025, reducing (but not eliminating) investigation risk. Meta refused to sign.

### 2.2 US: targeted but structurally limited

**FTC Operation AI Comply (Sept 2024):** five simultaneous actions against AI deceptive-claims companies:

| Target | Outcome |
|---|---|
| DoNotPay | $193K fine + advertising restrictions |
| Rytr | Consent order issued 2024; **set aside by Trump-era FTC Dec 2025** (signal of retreat) |
| IntelliVision (facial recognition) | Final order Jan 2025 — barred from unsubstantiated claims |
| Evolv Technologies | Settled Dec 2024 — banned from unsubstantiated claims |

Fine sizes: $193K–$15M. **None targeted major LLM providers.**

**FTC chatbot inquiry (Sept 2025):** Section 6(b) orders to Alphabet, CharacterAI, Instagram, Meta, OpenAI, Snapchat, xAI on chatbot safety for children/teens. Data collection, not enforcement. Outcome TBD.

**What has NOT happened (as of Feb 2026):**

- No federal fine to OpenAI, Anthropic, Google, or Meta specifically for AI harms.
- No LLM product banned or restricted by US federal action.
- Trump Jan 2025 EO reversed Biden-era safety policies; preempted state AI laws.
- State AG enforcement against LLMs specifically has been minimal.

Structural summary: the EU enforced against the dominant LLM product (ChatGPT) within 21 months, resulting in a real fine. The US FTC has only fined small AI firms making deceptive claims; frontier LLM providers remain un-fined. The US retreated from AI enforcement after January 2025.

## 3. Simulation mechanism

### 3.1 Calibrated presets (driven by empirical enforcement record above)

All parameters in `Policymaker.__init__()` and `_plan_heuristic()`. Presets in `simulation.POLICYMAKER_PRESETS`:

| Parameter | Type | US | Balanced | EU | Empirical basis |
|---|---|---|---|---|---|
| `intervention_threshold` | float 0–1 | 0.75 | 0.50 | 0.35 | EU acts at moderate risk; US waits for high |
| `risk_tolerance` | float 0–1 | 0.70 | 0.50 | 0.20 | EU low; US high (innovation-first) |
| `intervention_cooldown` | int rounds | **5** | 3 | **2** | EU: 6–12 mo cycles; US: 18–36 mo FTC cycle |
| `sanction_fine_multiplier` | float | **0.10** | 0.22 | **0.35** | EU: 7% turnover ceiling; US: consent-order-only |
| `sanction_incident_threshold` | int | **4** | 3 | **2** | EU: 2+ triggers; US: needs clear pattern |
| `sanction_duration` | int rounds | **2** | 3 | **4** | EU: lengthy compliance cycles; US: short consent decrees |
| `mandate_risk_threshold` | float 0–1 | **0.75** | 0.62 | **0.50** | EU: ex-ante mandates; US: almost never |
| `sanction_min_severity` | str | **"critical"** | "major" | **"major"** | US acts on critical only; EU on major+ |

### 3.2 Graduated sanctions ladder

Five-lever ladder: `commitment → advisory → disclosure → audit → sanction`. Per-lever cooldowns. LLM regulator uses reasoning memory (PIMMUR Option B). Exogenous events (US R24, EU R14) inject regulatory pressure independent of incident chain.

### 3.3 Sanctions and fines

`sanctions_and_fines` action in `actors/policymaker.py`:

- Fine formula: `min(0.4, sanction_fine_multiplier × market_share × (1 − risk_tolerance))`.
- Condition 1: critical incident after public warning.
- Condition 2: accumulated incidents (≥ `sanction_incident_threshold`, severity ≥ `sanction_min_severity`) after investigation.
- Applied via `funding_multiplier` reduction for sanctioned provider in next round. Duration preset-dependent.

Calibrated effects on a 60%-share provider:

- EU fine: ~16.8% R&D efficiency reduction.
- US fine: ~1.8% reduction (and rarely triggered due to higher thresholds).

### 3.4 Not currently modeled

- `compliance_burden` — documentation/testing opportunity cost.
- `ex_ante_requirements` — pre-deployment gate (EU AI Act model).
- `independent_audit_threshold` — third-party audit trigger. See the audit-and-verification case study.
- `market_intervention_enabled` — operating restrictions / market bans.

## 4. Paired simulation results

A paired simulation contrasting the EU and US presets — five providers, 30 rounds, heuristic mode, same seed, `baseline_with_incidents` scenario, only the regulator preset differs.

### 4.1 Intervention pattern

Both regulators issued **6 interventions** over 30 rounds, same types. Difference: trigger timing and targets.

| Round | EU | US |
|---|---|---|
| 1 | transparency_requirement | transparency_requirement |
| 4 | public_disclosure | public_disclosure |
| 7 | performance_audit | performance_audit |
| 9 | **emergency_investigation (Spark AI, critical)** | — |
| 10 | — | **emergency_investigation (Apex AI, critical)** |
| 24 | benchmark_mandate (fairness_risk=0.75) | benchmark_mandate (fairness_risk=0.90) |
| 28 | final intervention | final intervention |

The EU regulator acted earlier (R9) against a marginal provider; the US regulator waited longer (R10) and acted against the market leader.

### 4.2 Incident outcomes

Both produced 12 total incidents — contradicting the naive "EU reduces incident count" hypothesis.

| Severity | EU | US |
|---|---|---|
| Critical | 1 | 1 |
| Major | 2 | 4 |
| Moderate | 3 | 2 |
| Minor | 6 | 5 |

The EU run skewed lower-severity (early interventions dampened escalation); the US run had more major incidents. Both shared the baseline incident rate driven by capability growth.

### 4.3 The benchmark mandate as market-reshuffling event

R24 benchmark mandate: EU triggered at `fairness_risk=0.75`; US at 0.90.

- **EU outcome:** Genesis Systems surged from ~8% to 38–46% in the rounds following the mandate, retained 13.4% at R29 (permanently above pre-mandate).
- **US outcome:** no comparable reshuffling; Apex AI maintained dominance.

### 4.4 Final market shares (R29)

| Provider | EU | US |
|---|---|---|
| Apex AI | 61.8% | 64.6% |
| Orion Labs | 9.6% | **23.8%** |
| Genesis Systems | **13.4%** | 5.4% |
| Mirage AI | 12.6% | 3.8% |
| Spark AI | 2.5% | 2.5% |

Orion Labs was marginalized in the EU run (never recovered from adverse benchmark performance + emergency-investigation context); recovered mid-game in the US run.

### 4.5 Counterintuitive result: safety alignment

| | EU | US |
|---|---|---|
| Avg safety_alignment (R29) | ~19% | **~23%** |

**US providers invested more in safety alignment than EU providers.** Inverts the naive prediction. Mechanism: under frequent EU interventions, providers invested in evaluation engineering and compliance theater rather than fundamental safety. Under the US regime, safety alignment became a market differentiator for consumer trust — market-driven safety rather than regulator-driven.

### 4.6 Hypothesis verification

| Hypothesis | Predicted | Actual |
|---|---|---|
| EU reduces incident count 30–50% | Fewer EU | **Wrong** — both 12; EU skewed lower-severity |
| US higher capability by R25 | Higher US | **Wrong** — identical |
| US higher market concentration | More concentrated US | **Wrong** — EU slightly more |
| EU forces higher safety investment | Higher EU safety | **Wrong** — US 23% vs EU 19% |
| EU maintains higher satisfaction | Higher EU | **Correct** — 0.777 vs 0.739 |

Summary: formal regulatory pressure did not increase safety investment — market competition did. The benchmark mandate's market-reshuffling effect was the single largest consequence of regulatory style.

## 5. Findings

EU and US regulatory philosophies produce subtly but meaningfully different trajectories over 30 rounds despite identical starting conditions. The difference is qualitative (volatility, market-share dynamics, safety-investment driver) rather than quantitative on headline metrics (incident count, capability growth). The case study's primary contribution is parameter grounding for the regulator presets that other case studies use.

## 6. Open questions

- **Cross-jurisdictional provider spread** — current roster assumes all providers operate under the same preset. Real-world: providers face multiple jurisdictions simultaneously. Extending to per-provider jurisdictional coverage would multiply the configuration space.
- **Federal preemption dynamics** — US federal law preempting California or New York state law is a live political dynamic not captured in the preset structure.
- **Enforcement lag** — the 21-month Italy Garante timeline is compressed to 2-round intervention cooldown. Reasonable abstraction at 1 round = 1 month, but should be probed.
- **Interaction with the transparency mandate case study** — uses SB 53 (CA state) scope, which sits under the US preset but adds EU-style disclosure duties for covered providers. Cross-preset composition is unexplored.

## 7. References

### EU

- EU AI Act Official — https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai
- High-level AI Act Summary — https://artificialintelligenceact.eu/high-level-summary/
- RAND — "Risk-Based Approach" (RRA3243-3).
- Italy Garante — ChatGPT GDPR ruling (Dec 2024).
- EU AI Office — Grok DSA proceedings (Jan 2026); Meta GPAI investigation (Jan 2026).

### US

- White House — America's AI Action Plan (Dec 2025).
- Squire Patton Boggs — Trump AI Executive Order analysis.
- Pillsbury — Federal AI Regulation overview.
- FTC — Operation AI Comply (Sept 2024); chatbot 6(b) orders (Sept 2025).
- FTC — Rytr consent order set-aside (Dec 2025).

### Academic

- Chicago Law Review — "Comparing EU & US AI legislation."
- Bar-Gill, Sunstein, Talley (various) — precautionary principle analyses.
