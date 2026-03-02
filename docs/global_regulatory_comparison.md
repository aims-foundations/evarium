# Global AI Regulatory Comparison Guide

Covers five regulatory philosophies modeled in the simulation: US Light-Touch, EU Precautionary, Balanced, China State-Directed, and Singapore Trust-Infrastructure. For implementation of EU and US presets, see `simulation.py` (`POLICYMAKER_PRESETS`). China and Singapore are documented here as candidate presets for future implementation.

---

## Quick-Reference Comparison Table

| | **US Light-Touch** | **EU Precautionary** | **Balanced** | **China State-Directed** | **Singapore Trust-Infrastructure** |
|---|---|---|---|---|---|
| **Primary lever** | Market | Enforcement | Mix | State control | Evaluation infrastructure |
| `intervention_threshold` | 0.75 | 0.35 | 0.50 | ~0.15 (political compliance trigger) | ~0.70 |
| `risk_tolerance` | 0.70 | 0.20 | 0.50 | ~0.10 (political); high for capability | ~0.65 |
| `intervention_cooldown` | 5 rds | 2 rds | 3 rds | 1 rd (immediate compliance) | 5 rds |
| `sanction_fine_multiplier` | 0.10 | 0.35 | 0.22 | ~0.60+ (existential sanctions possible) | ~0.05 |
| `sanction_duration` | 2 rds | 4 rds | 3 rds | Indefinite / market withdrawal | 1 rd |
| `sanction_min_severity` | critical | major | major | Any (political) | critical |
| `startup_entry_probability` | 0.15 | 0.04 | — | ~0.02 (security review gate) | ~0.12 |
| `startup_entry_cap` | 4 | 1 | — | 1 (state-approved only) | 3 |
| **Benchmark validity outcome** | Low | Medium | Medium | Very low (parallel regime) | Highest |
| **Market concentration** | High (market leader dominates) | Volatile (mandate shocks) | Medium | Designated champion | High (international dominant) |
| **Safety investment driver** | Market competition | Regulatory mandate | Mix | Compliance theater | Reputation / procurement access |
| **Most notable dynamics** | Market-driven safety exceeds regulatory safety | Mandate timing reshuffles market | — | Gaming bifurcates: capability + political compliance | Evaluator governance slows Goodhart decay |

**Fine at 60% market share:** EU 16.8% R&D reduction · US 1.8% · China: market withdrawal possible · Singapore: effectively 0%

---

## US Light-Touch (Implemented)

### Philosophy
Ex-post, market-driven. Regulators react to demonstrated harm rather than anticipating it. Consumer satisfaction and competitive pressure are the primary safety drivers.

### Parameters
| Parameter | Value |
|---|---|
| `intervention_threshold` | 0.75 |
| `risk_tolerance` | 0.70 |
| `intervention_cooldown` | 5 rounds |
| `sanction_fine_multiplier` | 0.10 |
| `sanction_duration` | 2 rounds |
| `sanction_min_severity` | critical |
| `mandate_risk_threshold` | 0.75 |
| `sanction_incident_threshold` | 4 |

### Expected Dynamics
- More incidents before intervention; skewed toward higher severity
- Higher innovation speed; less regulatory friction
- Market-driven safety — providers invest in safety as a product differentiator, not to comply
- Benchmark mandate issued late; limited market disruption
- Sustained regulator trust (high threshold means it is rarely crossed)

---

## EU Precautionary (Implemented)

### Philosophy
Ex-ante, enforcement-driven. Regulators intervene before widespread harm materializes. Based on the EU AI Act's tiered risk classification and pre-market conformity assessment architecture.

### Parameters
| Parameter | Value |
|---|---|
| `intervention_threshold` | 0.35 |
| `risk_tolerance` | 0.20 |
| `intervention_cooldown` | 2 rounds |
| `sanction_fine_multiplier` | 0.35 |
| `sanction_duration` | 4 rounds |
| `sanction_min_severity` | major |
| `mandate_risk_threshold` | 0.50 |
| `sanction_incident_threshold` | 2 |

### Expected Dynamics
- Fewer high-severity incidents; more moderate/minor ones as escalation is dampened early
- Benchmark mandate issued earlier; can reshuffle market significantly (see empirical results)
- Providers may invest in compliance-theater rather than genuine safety under frequent early mandates
- Regulator trust erodes as incidents accumulate against a low-risk-tolerance baseline
- Open-source providers exempt from sanctions and market concentration reviews (EU AI Act open-source exemption)

---

## Balanced (Implemented)

Middle ground between US and EU. Not anchored to a specific real-world jurisdiction — used as a neutral baseline for ablation experiments.

| Parameter | Value |
|---|---|
| `intervention_threshold` | 0.50 |
| `risk_tolerance` | 0.50 |
| `intervention_cooldown` | 3 rounds |
| `sanction_fine_multiplier` | 0.22 |
| `sanction_duration` | 3 rounds |
| `sanction_min_severity` | major |
| `sanction_incident_threshold` | 3 |

---

## China State-Directed (Candidate Preset)

### Policy Basis
China's AI governance is structured through layered regulations: the Algorithm Recommendation Rules (2022), Deep Synthesis Provisions (2022), Generative AI Interim Measures (August 2023), AI Safety Governance Framework (September 2024), and AI Content Labeling Measures (effective September 2025). These are jointly enforced by the Cyberspace Administration of China (CAC), Ministry of Industry and Information Technology (MIIT), Ministry of Public Security, and the Standardization Administration. A comprehensive AI Basic Law is in preparation.

The core distinction from US and EU: the Chinese state is not an external regulator — it is an active market participant with preferred market outcomes, operating through both mandatory compliance requirements and directed capital flows.

### Key Structural Differences

**1. Pre-launch security review as entry gate**
Providers with "public opinion attributes or capacity for social mobilization" must pass a CAC security assessment and complete regulatory filing *before* deployment. This is not a post-harm intervention — it is a mandatory market-entry filter. In simulation terms: a startup cannot enter the market without clearing a compliance gate, regardless of benchmark performance or incident history. Maps to: very low `startup_entry_probability`, plus an additional pre-launch compliance cost not currently in the model.

**2. Parallel benchmark regime**
China's national standard TC260-003 specifies security requirements including "corpus safety" — meaning a provider's content on politically sensitive topics is assessed by state regulators, not by open evaluations. Providers optimize for two parallel benchmark regimes: the capability benchmarks legible to international funders and consumers, and the political compliance benchmarks legible to domestic regulators. The `benchmark_focus` mechanism could capture this by adding state-mandated benchmarks with a separate validity/exploitability structure.

**3. State-directed funding**
State-linked sovereign funds, policy banks, and government procurement directives steer capital toward nationally strategic providers regardless of market performance. In the funder model: a dominant state funder whose allocation is politically determined, not signal-responsive. VC funders still operate but subject to national security review (CFIUS-equivalent for outbound investment).

**4. Existential sanctions**
Sanctions in China can include service suspension and market withdrawal — not just R&D efficiency penalties. The `sanction_fine_multiplier` concept understates the severity; the correct model would include a non-zero probability of full market exit per sanction event.

**5. Open-source and national champion dynamics**
DeepSeek's emergence reflects a China-specific structure: state-linked but technically sophisticated open-source providers that can undercut pricing and accelerate benchmark contamination globally while remaining exempt from international enforcement. OpenCore in the current simulation partially models this, but without the state-capital backing.

### Candidate Parameters
| Parameter | Value | Rationale |
|---|---|---|
| `intervention_threshold` | 0.15 | CAC acts on content compliance breaches immediately |
| `risk_tolerance` | 0.10 | Near-zero tolerance for political content violations |
| `intervention_cooldown` | 1 round | Immediate enforcement; no cooldown for political breaches |
| `sanction_fine_multiplier` | 0.60 | Severe, up to market withdrawal |
| `sanction_duration` | 6+ rounds | Indefinite pending compliance demonstration |
| `sanction_min_severity` | any | Political compliance incidents trigger sanctions regardless of severity |
| `startup_entry_probability` | 0.02 | Security review gate severely limits entry |
| `startup_entry_cap` | 1 | Only state-approved entrants |
| Funder type | State-dominant | Politically directed allocation ignoring gaming signals |

### Expected Dynamics
- A designated national champion emerges faster than under any other regime, driven by state capital rather than market performance
- Benchmark validity collapses sooner because the gaming target shifts to state-defined compliance benchmarks (opaque to the rest of the ecosystem)
- Startups are rare and state-approved; the barrier-to-entry composite is structurally higher even at low incumbent market concentration
- Consumer satisfaction is decoupled from market signals — consumers in state-critical sectors have limited switching options

### Sources
- [White & Case: AI Watch Global Regulatory Tracker — China](https://www.whitecase.com/insight-our-thinking/ai-watch-global-regulatory-tracker-china)
- [MIT Technology Review: Four things to know about China's new AI rules in 2024](https://www.technologyreview.com/2024/01/17/1086704/china-ai-regulation-changes-2024/)
- [DLA Piper: China releases AI Safety Governance Framework](https://www.dlapiper.com/en/insights/publications/2024/09/china-releases-ai-safety-governance-framework)
- [Carnegie Endowment: China's AI Policy in the DeepSeek Era](https://carnegieendowment.org/research/2025/07/chinas-ai-policy-in-the-deepseek-era?lang=en)
- [Chambers and Partners: Artificial Intelligence 2025 — China](https://practiceguides.chambers.com/practice-guides/artificial-intelligence-2025/china)
- [Reed Smith: Navigating the Complexities of AI Regulation in China](https://www.reedsmith.com/articles/navigating-the-complexities-of-ai-regulation-in-china/)
- [Columbia Law: The Promise and Perils of China's Regulation of Artificial Intelligence](https://www.law.columbia.edu/sites/default/files/2024-04/The%20Promise%20and%20Perils%20of%20Chinese%20AI%20Regulation.pdf)

---

## Singapore Trust-Infrastructure (Candidate Preset)

### Policy Basis
Singapore governs AI through a voluntary, risk-based, sector-specific framework. The Model AI Governance Framework (2019, updated 2020 and 2024 for GenAI) is non-binding guidance; compliance signals governance quality to enterprise buyers and earns access to government procurement. Hard law applies only to narrow high-stakes domains (elections, online safety, workplace fairness). The AI Verify toolkit (2022) and Global AI Assurance Pilot (2025) position Singapore as a **governance infrastructure provider** rather than an enforcement state. The 2025 draft addendum on Agentic AI extends this framework proactively to autonomous systems before widespread deployment.

Singapore has no domestic frontier AI providers. Its policy goal is to attract international providers by offering a trusted, low-friction deployment environment — using governance credibility as a competitive advantage for the city-state.

### Key Structural Differences

**1. Voluntary frameworks with reputational incentives**
Providers adopt the Model AI Governance Framework not because they must, but because doing so grants access to government procurement, earns enterprise consumer trust, and improves relationships with international partners. In simulation terms: the `intervention_threshold` is very high (regulators almost never mandate), but a voluntary compliance signal is available that reduces a provider's `exploitability` because their scores are subject to third-party audit.

**2. AI Verify and third-party testing as public infrastructure**
AI Verify is a government-developed open-source testing toolkit that lets providers demonstrate governance properties independently. This is a **meta-evaluation layer** — a provider who participates earns a higher-signal benchmark of governance quality. In simulation terms: this functions like an evaluator with structurally higher validity that is not susceptible to Goodhart decay from individual provider gaming, because it is maintained as a public good rather than a commercial product.

**3. Evaluator as public good**
Singapore's Global AI Assurance Pilot (2025) and alignment with OECD/GPAI assurance criteria create an international governance interoperability layer. In `Eval As Company` terms, this is the opposite: the evaluator has no revenue motive and is explicitly designed to maintain benchmark validity. This maps to: lower Goodhart decay rate, higher initial benchmark validity, lower `exploitability` growth per round.

**4. Sector-specific hard law at the boundary**
Hard mandatory requirements apply only where AI outcomes could undermine democratic integrity or cause clear harm (elections, online safety, workplace fairness). This is a precision instrument: very high threshold for most providers, but with targeted low-threshold rules for specific incident categories. In the incident model: political/election category incidents trigger immediate intervention; capability or safety incidents follow the high-threshold voluntary pathway.

**5. No state champion dynamics**
Singapore has no domestic providers to protect. Funders are fully market-driven; state funding flows toward governance infrastructure (AI Verify, research grants) rather than toward specific providers. The competitive dynamic is among international providers operating in a neutral, low-friction market.

### Candidate Parameters
| Parameter | Value | Rationale |
|---|---|---|
| `intervention_threshold` | 0.70 | Very few mandatory interventions |
| `risk_tolerance` | 0.65 | High tolerance for capability-related risk |
| `intervention_cooldown` | 5 rounds | Deliberate, slow-moving |
| `sanction_fine_multiplier` | 0.05 | Effectively no enforcement penalties |
| `sanction_duration` | 1 round | Token compliance period |
| `sanction_min_severity` | critical | Only catastrophic events trigger mandatory action |
| `mandate_risk_threshold` | 0.85 | Almost never mandates |
| Initial benchmark `validity` | 0.85+ | Evaluator-as-public-good starts with high credibility |
| Goodhart decay rate | Reduced by ~30% | Third-party audit resists gaming pressure |
| `evaluator_as_company` | False | Explicitly not revenue-seeking |
| Funder type | Market-driven only | No state champion allocation |

### Expected Dynamics
- Benchmark validity remains highest across all presets — not from enforcement but from evaluator governance quality
- Goodhart decay is slower; gaming inflation stabilizes at a lower plateau (analogous to the upper-left of the validity-inflation tradeoff)
- Market concentration emerges from pure market dynamics — a dominant international provider captures most of the market (consistent with real-world Singapore deployment patterns)
- Consumer satisfaction is high for enterprise segments because trust signals are credible and auditable
- Startups enter relatively freely; BTE composite is lower than US because there is no regulatory burden, though network effects and consumer lock-in still apply

### Sources
- [IMDA: Model AI Governance Framework for Generative AI (2024)](https://www.imda.gov.sg/resources/press-releases-factsheets-and-speeches/press-releases/2024/public-consult-model-ai-governance-framework-genai)
- [IAPP: Global AI Governance Law and Policy — Singapore](https://iapp.org/resources/article/global-ai-governance-singapore)
- [Hogan Lovells: Singapore releases draft Agentic AI governance frameworks (2025)](https://www.hoganlovells.com/en/publications/singapore-releases-draft-quantum-and-agentic-ai-governance-frameworks)
- [Cambridge Core: Governing intelligence — Singapore's evolving AI governance framework](https://www.cambridge.org/core/journals/cambridge-forum-on-ai-law-and-governance/article/governing-intelligence-singapores-evolving-ai-governance-framework/5E54A373E193E2D51354ADC1F509B9B4)
- [GovInsider: Singapore solved the AI governance paralysis](https://govinsider.asia/intl-en/article/singapore-solved-the-ai-governance-paralysis-heres-how)
- [Chambers and Partners: Artificial Intelligence 2025 — Singapore](https://practiceguides.chambers.com/practice-guides/artificial-intelligence-2025/singapore/trends-and-developments)
- [Nemko Digital: Singapore AI Regulation — Model & GenAI Frameworks](https://digital.nemko.com/regulations/singapore-ai-regulation)

---

## Empirical Results: EU vs US (Experiments 032 and 033)

Paired 30-round simulation run under identical market conditions. Five providers (anonymized), heuristic mode, seed 42.

- **exp032**: EU Precautionary (`intervention_threshold=0.35`, `risk_tolerance=0.2`)
- **exp033**: US Light-Touch (`intervention_threshold=0.75`, `risk_tolerance=0.7`)

### Key Outcomes

| Metric | EU (exp032) | US (exp033) |
|---|---|---|
| Industry trust (R0 → R29) | 0.501 → 0.399 | 1.0 → 1.0 |
| Total interventions | 6 | 6 |
| Total incidents | 12 | 12 |
| Major incidents | 2 | 4 |
| Avg safety\_alignment (R29) | ~19% | ~23% |
| Final avg consumer satisfaction | 0.777 | 0.739 |
| True capabilities | Nearly identical | Nearly identical |

**Market shares (R29):**

| Provider | EU | US |
|---|---|---|
| Anthropic | 61.8% | 64.6% |
| OpenAI | 9.6% | 23.8% |
| Google | 13.4% | 5.4% |
| MetaAI | 12.6% | 3.8% |
| StartupDotAI | 2.5% | 2.5% |

### Hypothesis Verification

| Hypothesis | Predicted | Actual |
|---|---|---|
| EU reduces incident count by 30–50% | Fewer EU incidents | **WRONG** — both 12; EU skewed lower-severity |
| US achieves higher capability by R25 | Higher US capabilities | **WRONG** — nearly identical |
| US leads to higher market concentration | More concentrated US | **WRONG** — both Anthropic-dominated |
| EU forces higher safety\_alignment | Higher EU investment | **WRONG** — US averaged higher (23% vs 19%) |
| EU maintains higher long-term satisfaction | Higher EU satisfaction | **CORRECT** — 0.777 vs 0.739 |

### Key Finding
Formal regulatory pressure did not increase safety investment — market competition did. Under the EU regime, providers adapted to frequent early interventions by optimizing for compliance benchmarks rather than genuine safety. Under the US regime, providers used safety alignment as a product differentiator to capture consumer trust. The benchmark mandate's timing was the single largest differentiating event: EU's earlier mandate (R24 at `fairness_risk=0.75`) reshuffled the market significantly (Google surged from ~8% to 46% briefly); the US mandate at R24 (`fairness_risk=0.90`) produced only minor adjustments.

---

## Running Comparison Experiments

```bash
# EU preset
python run_experiment.py --policy eu

# US preset
python run_experiment.py --policy us

# Compare results
python compare_experiments.py exp_XXX exp_YYY
```

See `docs/experiment_comparison_protocol.md` for the full comparison workflow. Key metrics: incident counts by severity, intervention types and timing, market share trajectories, safety alignment investment, consumer satisfaction, true capability growth.
