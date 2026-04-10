# Exogenous Events: Design Inventory

Events that actors should react to, organized by category. "Currently implemented" vs "proposed" status noted.

## 1. Safety Incidents (IMPLEMENTED - stochastic)

Generated per-round based on provider safety investment, market share, and incident history. Six categories with severity distribution (minor 50%, moderate 31%, major 12%, critical 7%):

| Category | Weight | Example |
|----------|--------|---------|
| Healthcare harm | 20% | Diagnostic errors, medication mistakes |
| Security breach | 25% | Data leaks, unauthorized access |
| Bias/discrimination | 20% | Hiring bias, facial recognition errors |
| Safety failure | 20% | Hallucinations, incorrect advice |
| Misinformation | 10% | Election disinfo, false health claims |
| Misuse | 5% | Jailbreaks, criminal exploitation |

**Actor reactions:** Consumers penalize (incident_penalty), media shifts sentiment, regulator escalates, funders withdraw.

**Status:** Working well. Severity calibration reviewed against empirical data (Cruise, Boeing 737 MAX, Samsung Note 7, Character.AI).

## 2. Regulatory Shocks (PARTIALLY IMPLEMENTED)

### Currently implemented
- **US Round 24 — Administration change:** Cancels sanctions, doubles incident thresholds, audits become advisory. Simulates deregulatory shift.
- **EU Round 14 — AI Act enters force:** Lowers thresholds 40%, binding audits enabled. Simulates precautionary tightening.

### Proposed additions

| Event | Trigger | Effects | Real-world analog |
|-------|---------|---------|-------------------|
| **Executive order on AI safety** | Round N (configurable) | Lower incident thresholds 20%, mandate safety disclosures for providers above market share threshold | Biden Oct 2023 EO |
| **Regulatory rollback** | Round N | Revoke disclosure mandates, raise thresholds, remove sanctions | Trump Jan 2025 EO revocation |
| **International AI treaty** | Round N | All regulators adopt minimum safety floor, harmonized audit standards | Bletchley Declaration / Seoul Summit |
| **Sector-specific regulation** | Round N | Healthcare/finance providers face binding audits regardless of global policy | FDA AI guidance, SEC AI disclosure rules |
| **Antitrust investigation** | Triggered when HHI > threshold | Market leader faces deployment restrictions or forced API access | FTC/DOJ Big Tech investigations |

## 3. Market/Demand Shocks (PARTIALLY IMPLEMENTED)

### Currently implemented
- **Market growth:** Multiplicative per-round expansion via `market_growth_rate` (default 3%/round)
- **Dynamic consumer composition:** Enterprise share logistic growth (session 23)

### Proposed additions

| Event | Trigger | Effects | Real-world analog |
|-------|---------|---------|-------------------|
| **Enterprise adoption wave** | Round N | Enterprise segment size jumps 15%, enterprise switching threshold drops | 2024 enterprise AI adoption surge |
| **Consumer trust crisis** | After 3+ major incidents in 5 rounds | All segments raise switching thresholds, satisfaction baseline drops | Post-Cambridge Analytica tech trust decline |
| **Agentic AI demand spike** | Round N | Consumer need weights shift toward agentic dimension, new agentic-heavy segments activate | 2025 agentic AI wave |
| **Compute cost shock** | Round N | Cost advantage multipliers shift (cheaper compute benefits smaller providers proportionally more) | GPU price drops, inference cost competition |
| **Market contraction** | Round N | Negative market_growth_rate for 3 rounds, reduced funder budgets | Tech downturn / funding winter |

## 4. Technology Shocks (NOT IMPLEMENTED)

| Event | Trigger | Effects | Real-world analog |
|-------|---------|---------|-------------------|
| **Capability breakthrough (external)** | Round N | New entrant appears with capabilities at 80th percentile of current field | DeepSeek R1 release |
| **Open-source release** | Round N | Strongest closed model's weights leaked/released; OpenCore gains capability boost | Llama release effect on market |
| **Benchmark contamination scandal** | When top provider's orientation > threshold | Gaming scandal: validity drops, media crisis, consumer trust penalty | MMLU contamination concerns |
| **Architecture paradigm shift** | Round N | All providers' R&D efficiency temporarily drops (old approaches devalued), then recovers at higher level | Transformer revolution, reasoning models |

## 5. Evaluation Ecosystem Events (NOT IMPLEMENTED)

| Event | Trigger | Effects | Real-world analog |
|-------|---------|---------|-------------------|
| **Benchmark saturation** | When top-3 providers all score > 0.9 on a benchmark | Benchmark retired, replaced with harder version; scores reset for that benchmark | MMLU saturation, move to MMLU-Pro |
| **Evaluation methodology critique** | Round N or when gaming_gap > threshold | Public critique of evaluation methodology; consumer weight on benchmarks drops, direct experience matters more | "Benchmarks are broken" discourse |
| **New evaluation paradigm** | Round N | Introduction of human-preference-based eval alongside capability benchmarks; different dimension weights | Chatbot Arena emergence |
| **Evaluator conflict of interest** | When eval_as_company revenue exceeds threshold | Media scandal about evaluator incentives; benchmark trust drops | Benchmark provider business model concerns |

## 6. Funding Environment Shocks (NOT IMPLEMENTED)

| Event | Trigger | Effects | Real-world analog |
|-------|---------|---------|-------------------|
| **VC funding winter** | Round N | VC max_round_deployment halved for 5 rounds, risk_tolerance drops | 2023 AI funding tightening |
| **Mega-round** | Round N | One VC gets 3x budget injection, deploys aggressively | SoftBank Vision Fund-style |
| **Government subsidy program** | Round N | Gov funder budget triples, restricted to safety-compliant providers | CHIPS Act / EU AI investment |
| **Corporate strategic acquisition** | When provider market share < 3% for 5 rounds | Weakest provider absorbed by leader (shares consolidated) | Big Tech AI acquisitions |

## Implementation Priority

**Tier 1 — High value, low complexity (implement next):**
- Antitrust investigation (HHI-triggered, uses existing regulator machinery)
- Benchmark contamination scandal (uses existing gaming_gap metric)
- Consumer trust crisis (extends existing incident penalty system)

**Tier 2 — High value, moderate complexity:**
- Executive order / regulatory rollback (extends existing US R24/EU R14 pattern)
- VC funding winter / government subsidy (modifies existing funder configs)
- Capability breakthrough / new entrant

**Tier 3 — Paper-worthy but complex:**
- Architecture paradigm shift
- Evaluation methodology critique
- Benchmark saturation with replacement

## Design Principles

1. **Configurable timing:** All events should have configurable trigger rounds or threshold triggers, not hardcoded.
2. **Announce to all actors:** Events should be visible in the public state so LLM actors can reason about them.
3. **Gradual vs. sudden:** Some events are instant shocks (regulatory order), others unfold over rounds (trust crisis). Both patterns needed.
4. **Reversibility:** Some shocks are permanent (AI Act), others are temporary (funding winter). Duration should be configurable.
5. **Validation-first:** Prioritize events with clear real-world analogs where we can compare simulated vs. actual actor responses (Sargent-style validation).
