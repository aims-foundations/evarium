# CS2: Transparency Mandate

**Status:** Designed. Implementation is Phase 1 of the §5 redesign workstream (~60 LOC). Primary contrast for paper §5.3.

## 1. Policy anchor

Three real-world frontier-AI transparency laws with overlapping but distinct structure:

### 1.1 California SB 53 — Transparency in Frontier Artificial Intelligence Act

Wiener, signed 29 Sept 2025, effective 1 Jan 2026. Large frontier developers must:

1. Publish a frontier AI safety/security framework; annual review; material changes within 30 days.
2. Transmit a **quarterly** summary of catastrophic-risk assessment to CA Office of Emergency Services.
3. Report critical safety incidents within 15 days (24h if imminent threat).
4. Protect whistleblowers (no financial bounty).

Threshold: compute ≥ 10²⁶ FLOPs **AND** gross revenue ≥ $500M. AG civil penalties up to $1M per violation. Catastrophic-risk scoping: ≥ $1B damage OR ≥ 50 casualties from specific scenarios.

### 1.2 NY RAISE Act (S6953)

Signed Dec 2025, various effective dates in 2026. Large developers (defined by aggregate compute-spend > $100M on any single model) must:

1. Publish a Safety and Security Protocol (SSP), retained 5 years, redacted public version.
2. Pre-deployment testing for "unreasonable risk of critical harm."
3. **Annual third-party audit** of SSP compliance.
4. Safety-incident disclosure within **72 hours**.

Critical harm threshold: > $1B OR ≥ 100 injured/killed. Enforcement: AG penalties up to 5% revenue (first violation), 15% (second).

### 1.3 EU AI Act Article 55

Systemic-risk GPAI (training compute ≥ 10²⁵ FLOPs) obligations: ongoing model evaluation, serious-incident reporting, documentation. No open-source exemption for systemic-risk models. Fine ceiling: €35M or 7% global turnover.

### 1.4 Comparison summary

| Axis | SB 53 (CA) | NY RAISE | EU Art 55 |
|---|---|---|---|
| Trigger | Compute AND revenue | Compute-spend only | Compute only |
| Routine cadence | Quarterly summary to state | Annual SSP update | Ongoing duty, no fixed cadence |
| Incident window | 15 days | **72 hours** | Duty of "serious incident" reporting |
| Third-party audit | Not required | **Annual, required** | Conformity assessment (Art 43) for systemic-risk |
| Public artifact | Full published framework | Redacted SSP | Technical documentation + model card |
| Penalty ceiling | $1M / violation | **5% / 15% revenue** | €35M or 7% global turnover |

The primary axis of interest for §5.3 is **scope heterogeneity**: all three laws apply only to providers above threshold, creating asymmetric information environments across the ecosystem.

## 2. Sim mechanism

### 2.1 Scope heterogeneity across the six-provider roster

| Provider | Real-world analog | Compute ≥ 10²⁶ | Revenue ≥ $500M | SB 53 | RAISE ($100M spend) | EU Art 55 (10²⁵ FLOPs) |
|---|---|---|---|---|---|---|
| Orion Labs | OpenAI | Yes | Yes | **Yes** | Yes | Yes |
| Apex AI | Anthropic | Yes | Yes | **Yes** | Yes | Yes |
| Genesis Systems | Google DeepMind | Yes | Yes (via Google) | **Yes** | Yes | Yes |
| Mirage AI | Meta AI | Yes | Yes (via Meta) | **Yes** | Yes | Yes |
| Spark AI | small startup | No | No | No | No | No |
| OpenCore | DeepSeek | Yes (frontier compute) | No (<$500M) | No | No | **Yes** (OS systemic-risk no exemption) |

Under SB 53: 4/6 covered, 2 exempt (Spark, OpenCore). Under RAISE: same 4/6. Under EU Art 55: 5/6 covered (Spark exempt). **The SB 53 vs EU Art 55 asymmetry — specifically whether OpenCore is in scope — is the load-bearing contrast.**

### 2.2 Disclosure mechanism (SB 53-literal)

At each audit round `t ∈ {round 3, 6, 9, …, 30}` (quarterly, 3-round cadence):

For each covered provider `p`:
```
disclosed_safety_allocation[p][t] = mean(actual_safety_allocation[p][t-2..t])
```

Rolling-3-round mean matches the statutory "summary of assessment" phrasing (not snapshot); reduces window-gaming.

Exempt providers: no disclosure; `safety_allocation` remains private.

### 2.3 Observation channel

The disclosed value enters three existing formulas without new free parameters:

**Consumer `expected_quality`** (`src/actors/consumer.py`):
```
expected_quality[p] = leaderboard_trust × dot(published_scores[p], effective_relevance)
                    + safety_disclosure_trust × disclosed_safety_allocation[p] × need_weight[safety]
                    + (1 − leaderboard_trust − safety_disclosure_trust) × running_perceived_quality[p]
```

Where `safety_disclosure_trust = leaderboard_trust × need_weight[safety]`, taking share from the leaderboard term rather than the perceived-quality term. This makes disclosure a "better signal" substitute for leaderboard-only evaluation. For exempt providers and pre-disclosure rounds, weight transfers back to `running_perceived_quality` so the blend sums to 1.

**Funder allocation** (`src/actors/funder.py`): each funder type has a safety weight; `disclosed_safety_allocation` enters additively when visible.

**Media narrative** (`src/actors/media.py`): disclosures are a potential narrative trigger — material changes generate coverage (positive if allocation raised, negative if lowered quarter-over-quarter by more than 0.05).

**Zero new free parameters.**

### 2.4 Ablation conditions

Primary contrast (single-point, case-study convention):

| Condition | Mandate active? | Scope | Role |
|---|---|---|---|
| `baseline` | No | — | Reference (also §5.1 illustrative) |
| `transparency_mandate` | Yes | SB 53 (4/6 covered) | Primary for §5.3 |

Appendix sensitivity (heuristic-only):

| Condition | Mandate active? | Scope | Tests |
|---|---|---|---|
| `transparency_eu_scope` | Yes | EU Art 55 (5/6 — adds OpenCore) | OS-inclusion effect |
| `transparency_universal` | Yes | All 6 covered | Counterfactual: no scope threshold |

RAISE is not a separate simulation condition — it yields the same provider coverage as SB 53 for our roster. RAISE differences (audit requirement, 72h window, 15% revenue penalty) are treated as a policy-sensitivity paragraph in §5.5 scope and punted to CS6 (audit & verification).

### 2.5 LOC estimate (~60)

| File | Change |
|---|---|
| `src/simulation.py` | `transparency_mandate_scope: Optional[Literal["sb53", "eu_art55", "universal"]]`; `transparency_disclosure_interval: int = 3` |
| `src/simulation.py` | Per-provider `is_covered_by_mandate` flag, computed at setup from compute + revenue proxies |
| `src/simulation.py` | At `round_num % 3 == 0`, compute rolling 3-round mean, write to `public_state.disclosed_safety_allocations[p]` |
| `src/actors/consumer.py` | Update `expected_quality` weighting to include `safety_disclosure_trust` term |
| `src/actors/funder.py` | Additive safety-weight reading disclosed allocation when available |
| `src/actors/media.py` | `disclosure_changes` trigger for narrative generation |
| `scripts/run_experiment.py` | 3 new conditions |
| `docs/stakeholders.md` | Update §Regulator + §Consumer with new observation channel |

## 3. Paper claim (§5.3)

"Transparency mandates on R&D inputs (SB 53 literal, quarterly cadence) reshape information flow but produce heterogeneous welfare effects. Covered providers face a disclose-and-invest tradeoff; exempt providers retain information asymmetry. In our calibration, safety-conscious segments (enterprise, healthcare) shift market share toward covered providers who invest, while cost-sensitive segments are unaffected. Net ecosystem effect depends on enterprise market-share composition — a finding that is empirically addressable only in an ecosystem frame, not at the benchmark level."

Appendix sensitivity: varying scope (SB 53 / EU Art 55 / universal) isolates the OS-inclusion effect. Including OpenCore in the mandate (EU scope) either improves or degrades welfare depending on whether disclosure incentivizes OpenCore to raise safety allocation or whether it reveals an already-low allocation that consumers/funders then penalize.

## 4. Open questions

1. **LLM prompt integration** — do covered providers see "Your model meets the SB 53 threshold; you must publish a quarterly safety assessment" in their planning prompt? Recommendation: yes (PIMMUR-Memory compliant).
2. **Coverage flag updating** — is `is_covered_by_mandate` frozen at round 0 or updated if provider revenue crosses threshold mid-run? Recommendation: frozen (SB 53 thresholds update annually).
3. **Partial-window rolling mean** — first two disclosures (rounds 3, 6) use whatever rounds are available; from round 9 onward, strict 3-round window.
4. **Verification layer** — CS2 models self-attested disclosure only. For verified disclosure, see CS6 (audit & verification).

## 5. Scope — what CS2 does NOT model

- **Third-party audit** (RAISE annual, EU conformity assessments) — see CS6.
- **Penalty differentiation** — CS2 assumes disclosure compliance; non-compliance penalties are abstracted into the existing regulator lever (CS7).
- **Declaration vs realized gap** — CS2 discloses *actual* allocation; declare-then-verify games are CS6.
- **Redacted vs full disclosure** — CS2 treats disclosure as clean (no noise); RAISE's redacted SSP would introduce `σ_redact`, deferred.

## 6. References

### SB 53 primary

- SB 53 bill text (LegiScan): https://legiscan.com/CA/text/SB53/id/3270002
- CA Legislature: https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202520260SB53
- SB 53 FAQs: https://sb53.info/faq
- FPF — "California's SB 53: The First Frontier AI Law, Explained"
- Wharton AI & Analytics — "SB 53: What California's New AI Safety Law Means for Developers"
- WilmerHale — SB-53 compliance brief
- Anthropic — Compliance framework for SB 53
- Nelson Mullins — SB 53 Expanded Compliance Guide

### NY RAISE primary

- NY S6953 RAISE Act text (NY Senate)
- Jones Walker — "New York's RAISE Act: What Frontier Model Developers Need to Know"

### EU AI Act

- EU AI Act Article 15 — Accuracy, Robustness, Cybersecurity
- EU AI Act Article 43 — Conformity Assessment
- EU AI Act Article 55 — Obligations for Systemic-Risk GPAI
- EU AI Act Annex III — High-Risk AI Systems
- Linux Foundation Europe — Open Source + EU AI Act
- Latham & Watkins — GPAI Model Obligations in Force

### Regulatory-threshold precedent

- EPA NAAQS — percentile-based standards
- FDA 510(k) Premarket Notification / Substantial Equivalence

### Academic

- Anderljung et al. (2023). Frontier AI Regulation: Managing Emerging Risks to Public Safety.
- Shevlane et al. (2023). Model evaluation for extreme risks.
- Cuéllar (2024). Common Law and Emerging Technology. (Stanford L Rev)
- Casper et al. (2024). Black-Box Access is Insufficient for Rigorous AI Audits.
- Longpre et al. (2024). A Safe Harbor for Independent AI Evaluation.
- Raji & Buolamwini lineage — Actionable Auditing.

## 7. Internal pointers

- `src/simulation.py` — `SimulationConfig` (new fields to add)
- `src/actors/consumer.py` — `expected_quality` (to extend)
- `src/actors/funder.py` — safety-weight path (to extend)
- `src/actors/media.py` — narrative triggers (to extend)
- `scripts/run_experiment.py` — condition presets
- `docs/stakeholders.md` — Regulator + Consumer sections (to update on landing)
- `case_studies/audit_verification.md` (CS6) — verification-audit extension
- `case_studies/eu_us_regulation.md` (CS7) — existing regulator-lever framework
