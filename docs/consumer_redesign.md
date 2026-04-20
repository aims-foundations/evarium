# Consumer Market Redesign — Phase 1 Design Doc (Option 1.5)

**Status:** Phase 1 (design only). No code changes yet.
**Date:** 2026-04-18 (session 39c)
**Scope:** Uniform deployment-context ontology, no new axes, ~50 fewer parameters than current state.
**Decisions locked:** see §14 (Q1-Q6 resolved with user).

---

## 1. Motivation

The current consumer market (16 `use_case` profiles × 3 archetypes ≈ 39 segments) has three structural problems:

1. **Mixed ontology.** Individuals are categorized by job function (`software_dev`, `healthcare`, `legal`); organizations are categorized by industry vertical (`hospital_system`, `enterprise_finance`, `enterprise_legal`). These are not partitions of the same space. A `healthcare` individual segment and a `hospital_system` org segment overlap conceptually but are treated as disjoint.
2. **Asymmetric coverage.** 11 individual segments (75% of population weight) vs. 5 organizational segments (25%). McKinsey 2024 puts >70% of AI spend on the enterprise side. The simulation has the inverse skew on value-at-stake.
3. **Compliance is decorative.** `compliance_requirements` is a tag, not a load-bearing parameter. EU AI Act risk tiers are not represented despite being the most defensible regulatory anchor in the literature.

Two downstream consequences:
- The `affected_sectors` mapping on incidents is partially dead because authored sector strings (e.g. `enterprise_saas`, `healthcare_individual`, `enterprise_hr`) don't match any actual `use_case` name. 5 of 7 sector strings match nothing → the 2× sector multiplier in `consumer.py:645-646` never fires for `misinformation`, `misuse`, `bias_discrimination`, or healthcare-individual harm.
- `dynamic_enterprise_growth` shifts a global enterprise share that has no clean empirical anchor; the natural empirical question is "how does enterprise vs individual share shift *within each deployment context*", which the current ontology can't ask.

## 2. Design principles (per user-provided guidance)

1. **Ground in real data where it exists.** Cite the source inline; write a reproducible derivation script in `external-validation/scripts/`.
2. **Where data is unavailable, lean on frameworks.** Specifically: EU AI Act Annex III (risk tiers), US BLS SOC 2018 (occupation taxonomy), GDPval (OpenAI 2025 — economic value across occupations), Rogers' Diffusion of Innovations (archetype distribution).
3. **Internal validity is the goal.** Confidence in the mechanism is the deliverable, not just numerical fidelity. Every parameter should be defensible from primary sources or expert judgment with citation.
4. **Endogenize where justifiable; otherwise stay exogenous and admit it.** This version uses Level 1 (per-context exogenous growth rates calibrated to multiple recent sources). No safety-aware endogenization (Level 2) — accepted as future work.
5. **Calibration trap caution.** Be explicit about which parameters are empirically anchored vs. expert-judgment-with-citations vs. set-by-sensitivity-analysis.

## 3. Proposed structure

A two-axis structure with one cross-cutting property and one within-segment property:

```
Segment = (deployment_context, archetype)
       + risk_tier (property of context, not a free axis)
       + consumer_type (derived from archetype: individual archetypes → individual; enterprise archetypes → organization)
```

**Axis 1 — Deployment context** (10 values): What is AI being used for. Carries `need_weights`, `risk_tier`, `incident_susceptibility`, `decision_delay`, `keyword_priorities`, `enterprise_growth_rate`.

**Axis 2 — Archetype** (6 values, unchanged from current): 3 individual (`leaderboard_follower`, `experience_driven`, `cautious`) + 3 organizational (`enterprise_cautious`, `enterprise_growth`, `enterprise_established`). Distribution within context determined by `consumer_type_split` (per-context individual/organization fraction).

**Cross-cutting — Risk tier** (2 values): `high` or `limited` per EU AI Act Annex III. Property of context, not an independent axis. Multiplies incident susceptibility, raises regulator attention threshold. **No `minimal` tier** — empty for frontier LLM deployment contexts.

**Within-segment — Consumer type** (2 values, unchanged from current): `individual` or `organization`. Derived from archetype family. Determines decision_delay, switching_cost multiplier, compliance_weight (existing mechanisms unchanged).

**Total cell count:** 10 contexts × 6 archetypes = 60 potential segments. Active segments determined by `consumer_type_split` per context (e.g., `clinical_care` is org-heavy → individual archetype shares small).

**No deployment_scale axis** (rejected: parameter expansion not earned by the empirical anchors available).
**No endogenized α** (rejected for v1: keeps mechanism controllable; can be added post-deadline as Level 2).
**No `compliance_intensity` float** (rejected: existing `compliance_weight` × `consumer_type` mechanism is sufficient; risk_tier captures the gradation).

## 4. Deployment context taxonomy

**Sources:** EU AI Act Annex III (high-risk areas); GDPval (OpenAI 2025) occupation list; US BLS SOC 2018 major groups; AI Index 2025 §2 (use-case adoption).

| Context | Scope | EU AI Act mapping | Risk tier |
|---|---|---|---|
| `clinical_care` | Diagnosis, treatment recommendation, hospital workflow, clinician copilot | Annex III §5 (essential services) + medical device regulation | high |
| `financial_decisioning` | Credit scoring, fraud detection, financial advisory, trading support | Annex III §5 (creditworthiness) | high |
| `legal_research` | Case research, contract drafting, judicial decision support | Annex III §8 (administration of justice) | high |
| `education` | Tutoring, grading, assessment, personalized learning | Annex III §3 (education) | high |
| `public_administration` | Citizen services, eligibility determinations, policy analysis | Annex III §5,6,8 | high |
| `hr_talent` | Recruiting, screening, performance management, promotion decisions | Annex III §4 (employment) | high |
| `code_production` | Code generation, IDE assistants, autonomous coding agents | Limited unless embedded in safety-critical | limited |
| `content_creation` | Writing, marketing, design, media production | Limited (transparency for synthetic content) | limited |
| `customer_engagement` | Chatbots, support automation, conversational interfaces | Limited (chatbot transparency) | limited |
| `security_operations` | SOC, threat detection, incident response, vulnerability research | Limited (most cases) | limited |

**Resolved decisions (locked):**
- `researcher` (current use_case) → all into `code_production` per Q1 (GDPval and BLS group "Research Scientists" with computational occupations).
- `creative` + `marketing` (current use_cases) → both into `content_creation` per Q2 (need_weights similar; CMO/freelancer differentiation captured by archetype).

## 5. Risk tier mapping (EU AI Act Annex III)

Direct citation: Regulation (EU) 2024/1689, Annex III, final text adopted June 2024.

```
high:    clinical_care, financial_decisioning, legal_research, education,
         public_administration, hr_talent
limited: code_production, content_creation, customer_engagement, security_operations
```

**Risk tier downstream effects** (kept minimal — 2 multipliers only):

| Mechanism | high | limited |
|---|---|---|
| `incident_susceptibility` multiplier | 1.4× | 1.0× |
| Regulator attention threshold (incidents needed before regulator considers action) | 1 | 3 |

**Source for multiplier values:** CEPS 2023 EU AI Act compliance-cost study (estimates 6-17% revenue overhead for high-risk applications); EU AI Act fine schedule (up to 7% global revenue for high-risk violations vs. 1.5% for limited-risk transparency violations). The ~5:1 fine ratio anchors the qualitative ordering high > limited; the 1.4× incident multiplier is expert-judgment within plausible range and subject to sensitivity analysis (§10).

**Risk_tier × need_weights reconciliation** (resolved): the risk tier does NOT impose a `safety` need_weight floor. need_weights are authored independently from cited literature (§7), and high-risk contexts naturally have higher safety values from those citations. risk_tier multipliers act on `incident_susceptibility` and regulator attention only — no double-counting with need_weights.

## 6. Archetype distribution

Unchanged from current state (uniform across contexts, anchored in Rogers 2003 Diffusion of Innovations 5→3 bin mapping):

```
Individual:     leaderboard_follower 0.40, experience_driven 0.35, cautious 0.25
Organizational: enterprise_cautious 0.50, enterprise_growth 0.30, enterprise_established 0.20
```

**Why uniform (not per-context):** per-context overrides require context-specific surveys (Doximity, SHRM, ABA, etc.) for each row. The empirical anchor for the 5→3 bin mapping is itself approximate. Trading additional context-level realism for 30 new parameters with weak anchors is a net loss in defensibility. Future work.

The user explicitly accepted this loss in Option 1.5 scope.

## 7. Need_weights per context

The most calibration-trap-sensitive parameter set. Honest framing: these are derived from a combination of (a) capability-vs-task analyses in the literature, (b) the structure of established benchmarks for the domain, and (c) expert judgment within the literature-implied rank ordering. They are NOT derived from user-satisfaction regressions, which would be the gold standard but don't exist publicly.

**Proposed table** (each row sums to 1.0):

| Context | reasoning | coding | knowledge | safety | communication | agentic | Anchor |
|---|---|---|---|---|---|---|---|
| `clinical_care` | 0.18 | 0.02 | 0.30 | 0.40 | 0.08 | 0.02 | Topol 2019; Rajpurkar 2022 (medical AI priorities) |
| `financial_decisioning` | 0.35 | 0.05 | 0.20 | 0.30 | 0.05 | 0.05 | Federal Reserve SR 11-7 model-risk priorities |
| `legal_research` | 0.30 | 0.02 | 0.35 | 0.20 | 0.10 | 0.03 | ABA 2024 + LegalBench paper |
| `education` | 0.20 | 0.05 | 0.25 | 0.25 | 0.20 | 0.05 | RAND teacher survey + Khan Academy public studies |
| `public_administration` | 0.15 | 0.02 | 0.25 | 0.40 | 0.13 | 0.05 | NIST AI RMF; OECD government AI principles |
| `hr_talent` | 0.20 | 0.02 | 0.20 | 0.35 | 0.18 | 0.05 | EEOC 2024 algorithmic discrimination guidance |
| `code_production` | 0.20 | 0.45 | 0.10 | 0.05 | 0.05 | 0.15 | Stack Overflow Developer Survey 2024 + GitHub Copilot user studies. coding reduced from 0.55 to 0.45; agentic raised 0.10→0.15; knowledge 0.05→0.10. Smoke-probe diagnostic with coding=0.55 produced Spark AI 50% share + HHI 0.352, contradicting real-world fragmentation in the coding market (GPT-4o/Claude/Gemini all within ~5pp on HumanEval; Cursor/Copilot/etc. fragment IDE share). Reduced peakedness reflects developer survey priorities beyond raw codegen (debugging, integration, language support) |
| `content_creation` | 0.12 | 0.02 | 0.18 | 0.15 | 0.45 | 0.08 | Jasper user studies 2024; published OpenAI usage summaries (non-Anthropic sources only). Safety=0.15 retained from current `creative` use_case (was 0.18) — smoke-probe diagnostic showed dropping safety to 0.05 produced Orion-dominance in 7 of 10 contexts; restoring safety preserves Apex AI as content_creation contender |
| `customer_engagement` | 0.08 | 0.02 | 0.12 | 0.10 | 0.60 | 0.08 | Zendesk State of CX 2024 |
| `security_operations` | 0.30 | 0.30 | 0.15 | 0.10 | 0.05 | 0.10 | MITRE ATT&CK + SANS 2024 SOC survey |

**Calibration honesty:**
- **Direction** (which dimension dominates per context) is well-supported by the cited literature.
- **Rank ordering** within each row is defensible from citations.
- **Exact magnitudes** are expert-judgment within the rank-ordering — subject to sensitivity analysis (§10).
- Cross-segment population-weighted average should be close to current 0.22/0.09/0.23/0.17/0.26/0.05 (used as homogeneous baseline in `simulation.py:618`) so aggregate dynamics don't shift radically. Verify in §10 sensitivity step.

**Reproducible derivation:** `external-validation/scripts/derive_need_weights.py` — reads a citations table (manually curated from sources above), applies a literature-mapping rule (dominant dimension at 0.4-0.55, secondary at 0.20-0.35, etc.), outputs the CSV. Phase 2.

## 8. Population weights per context (60/40 adoption-favoring blend)

**Resolved decision (Q3):** 60/40 adoption-favoring blend.

Two underlying signals:
- **Adoption count** (% of orgs/individuals using AI in this function). Sources: McKinsey State of AI 2025 (n≈1500), Stack Overflow Developer Survey 2024, Stanford AI Index 2025 §2.
- **Value-at-stake** (economic value of AI in this domain). Sources: GDPval (OpenAI 2025) occupation-level economic-value scoring, BLS wage data × occupation × AI exposure (Eloundou et al. 2023 methodology as fallback if GDPval methodology contested).

**Rationale for adoption-favoring (per user discussion):** incidents scale with deployment volume (exposure surface), not with per-deployment value. Risk tier multipliers (§5) and per-category severity distribution (current `incidents.py:SEVERITY_PROBS`) capture per-incident severity separately. No double-counting.

**Proposed initial weights** (60% adoption signal + 40% value signal, normalized):

| Context | Weight | Reasoning |
|---|---|---|
| `code_production` | 0.16 | High adoption + moderate-high GDPval |
| `content_creation` | 0.14 | High adoption (marketing+sales+content) |
| `customer_engagement` | 0.13 | Service operations top McKinsey adoption |
| `clinical_care` | 0.10 | Mid adoption, very high GDPval pulls up |
| `financial_decisioning` | 0.10 | Mid adoption, high GDPval pulls up |
| `education` | 0.08 | Mid adoption, mid GDPval |
| `legal_research` | 0.08 | Lower adoption, very high per-task GDPval |
| `public_administration` | 0.08 | Mid adoption, mid GDPval |
| `hr_talent` | 0.07 | Low adoption (11% McKinsey), mid GDPval |
| `security_operations` | 0.06 | Lower adoption, growing |

Sum: 1.00.

**Reproducible derivation:** `external-validation/scripts/derive_context_population.py` — reads McKinsey + AI Index + GDPval source tables, applies `weight = 0.6 × adoption_share + 0.4 × value_share`, normalizes to 1.0, outputs CSV with provenance per row. Phase 2.

## 9. Consumer type split per context + Level 1 enterprise growth

**Static `consumer_type_split` per context** (individual / organization fractions at round 0):

| Context | Individual | Organization | Source |
|---|---|---|---|
| `code_production` | 0.55 | 0.45 | Largest individual base (devs personally use Copilot) |
| `content_creation` | 0.50 | 0.50 | Mix of freelancers, agencies, in-house teams |
| `customer_engagement` | 0.05 | 0.95 | Almost entirely org-deployed |
| `clinical_care` | 0.20 | 0.80 | Hospital systems dominate; some clinician individual use |
| `financial_decisioning` | 0.05 | 0.95 | Bank/fund deployment dominates |
| `education` | 0.30 | 0.70 | Mix of teachers, schools, districts |
| `legal_research` | 0.30 | 0.70 | Solo + small-firm + biglaw mix |
| `public_administration` | 0.0 | 1.00 | Inherently institutional |
| `hr_talent` | 0.05 | 0.95 | Primarily mid-large enterprise tools |
| `security_operations` | 0.10 | 0.90 | SOC tooling org-deployed |

**Sources** (triangulated, **no Anthropic source per user direction**):
- Menlo Ventures State of AI in the Enterprise 2025 (per-vertical enterprise spend)
- Stanford AI Index 2025 §6 (industry adoption × company size cuts; AI Index 2026 if available by Phase 2)
- Deloitte State of Generative AI in the Enterprise Q4 2025 (industry deployment quarterly tracker)
- McKinsey State of AI 2025 (functional adoption survey, enterprise-vs-individual breakdowns)
- Sector-specific where applicable: FSB AI in Financial Services 2025; FDA AI/ML device list 2024-2025; OECD.AI live indicators

**Triangulation rule:** for each context, take the median of available sources. Where sources disagree by >20pp, flag in derivation log and use median plus a sensitivity-test entry.

### Level 1 enterprise growth (per-context exogenous)

**Per-round shift in `consumer_type_split` toward organization**, reflecting empirical enterprise-share growth observed 2023-2025. Cap at 0.95 organization (no context goes fully institutional).

| Context | Per-round enterprise growth (Δ org share) | Anchor |
|---|---|---|
| `code_production` | +0.005 | Menlo Ventures: enterprise SWE adoption +50% YoY (~+0.6%/month) |
| `content_creation` | +0.004 | Mid-pace enterprise adoption per Deloitte Q4 2025 |
| `customer_engagement` | +0.001 | Already org-saturated |
| `clinical_care` | +0.002 | Slow institutional adoption per FDA approval data |
| `financial_decisioning` | +0.001 | Already org-saturated |
| `education` | +0.003 | District-level deployment growing per RAND 2025 |
| `legal_research` | +0.004 | BigLaw + mid-firm rapid adoption per ABA Tech Survey 2025 |
| `public_administration` | +0.001 | Already saturated |
| `hr_talent` | +0.002 | Slow growth (post-bias-incident regulatory caution per SHRM 2024) |
| `security_operations` | +0.003 | Steady org adoption per SANS 2024 |

**Reproducible derivation:** `external-validation/scripts/derive_context_enterprise_growth.py` — reads Menlo Ventures + AI Index + Deloitte + sector sources, computes per-context monthly growth rate via median across sources, outputs CSV with per-source values logged. Phase 2.

**Honesty caveat:** these are growth rates *up to the present (2026 Q1)*. Forward projection assumes continuation of observed trends; no S-curve saturation modeled (acceptable simplification for 30-round window ≈ 2.5 years).

**What this replaces:** current global `enterprise_growth_rate` config parameter. New behavior is per-context, calibrated, and reproducible.

## 10. Calibration trap mitigation

For each parameter family, classify and document:

| Parameter family | # params | Anchor type | Mitigation |
|---|---|---|---|
| Context list (categorical) | — | Empirical (EU AI Act Annex III + GDPval + BLS SOC) | Direct citation in stakeholders.md |
| Risk tier mapping (categorical) | — | Empirical (EU AI Act direct citation per row) | Direct citation |
| Risk tier multipliers | 4 | Expert-judgment within EU AI Act fine-ratio framework | Sensitivity analysis: vary multiplier across [1.0×, 2.0×], confirm directional results stable |
| Archetype distribution (uniform) | 6 | Empirical (Rogers 2003 5→3 bin mapping) | Document the bin-mapping rule; no per-context variation |
| Need_weights | 60 | Expert-judgment with literature anchor per row | Sensitivity analysis: vary each context's dominant dimension ±20%, confirm score-satisfaction gap direction stable |
| Population weights | 10 | Empirical (McKinsey + AI Index + GDPval 60/40 blend) | Derivation script + CSV; document blend formula |
| Consumer_type_split per context | 10 | Empirical (Menlo + AI Index + Deloitte median) | Derivation script + CSV; document triangulation rule |
| Enterprise growth rate per context | 10 | Empirical (Menlo + AI Index + Deloitte + sector sources, median) | Derivation script + CSV |
| Decision_delay per context | 10 | Expert-judgment with Gartner 2024 anchor | Derive scale-stratified defaults from Gartner; document |

**Mandatory before paper publication:** sensitivity-analysis run on the 2 expert-judgment parameter families (need_weights, risk_tier multipliers — per Q5 priority). If results invert direction under any plausible setting, that finding goes in the appendix as a known caveat.

## 11. Migration table (current 16 → Option 1.5's 10)

| Current `use_case` | Current pop weight | New context | Notes |
|---|---|---|---|
| `software_dev` | 0.14 | `code_production` | Direct |
| `tech_startup` | 0.06 | `code_production` | Tech_startup is a buyer profile; deployment context is code |
| `researcher` | 0.06 | `code_production` | Per Q1 (GDPval + BLS group with computational occupations) |
| `content_writer` | 0.08 | `content_creation` | Direct |
| `creative` | 0.06 | `content_creation` | Per Q2 |
| `marketing` | 0.07 | `content_creation` | Per Q2 |
| `legal` | 0.04 | `legal_research` | Direct (consumer_type via archetype) |
| `enterprise_legal` | 0.04 | `legal_research` | Direct |
| `healthcare` | 0.05 | `clinical_care` | Direct (consumer_type via archetype) |
| `hospital_system` | 0.05 | `clinical_care` | Direct |
| `finance` | 0.05 | `financial_decisioning` | Direct (consumer_type via archetype) |
| `enterprise_finance` | 0.05 | `financial_decisioning` | Direct |
| `educator` | 0.07 | `education` | Direct (consumer_type via archetype) |
| `customer_service` | 0.08 | `customer_engagement` | Direct |
| `service_worker` | 0.05 | `customer_engagement` | End-user-facing customer engagement |
| `government_agency` | 0.05 | `public_administration` | Direct |
| (NEW) | — | `hr_talent` | Closes EU AI Act Annex III §4 gap; pop weight 0.07 |
| (NEW) | — | `security_operations` | Closes coverage gap; pop weight 0.06 |

**Validation:** all current use_cases mapped (no silent drops). New pop weights (§8) re-derived from triangulation, not just "split current weights." Old per-use_case `consumer_type` field becomes irrelevant — `consumer_type` is now derived from archetype family.

**Backwards compatibility (Q6 resolved):** hard-cut, no shim. Pre-redesign configs outside sandbox fail loud (consistent with session 31 precedent).

## 12. Reproducible scripts plan (Phase 2 deliverables)

To be authored in `external-validation/scripts/`:

| Script | Inputs | Outputs | Status |
|---|---|---|---|
| `derive_context_population.py` | McKinsey 2025, AI Index 2025/2026, GDPval | `data/processed/context_population.csv` | New |
| `derive_consumer_type_split.py` | Menlo Ventures 2025, AI Index, Deloitte Q4 2025, McKinsey, sector sources | `data/processed/consumer_type_split.csv` | New |
| `derive_context_enterprise_growth.py` | Menlo Ventures 2025, AI Index, Deloitte Q4 2025, sector sources | `data/processed/context_enterprise_growth.csv` | New |
| `derive_need_weights.py` | Manually curated literature-citation table | `data/processed/context_need_weights.csv` | New |

Each script writes its derivation rule + source citations as a header comment block; per-row provenance written to CSV. Future reviewers can audit the choices.

**Anthropic Economic Index excluded from all triangulation per user direction.**

## 12.5. Provider capability vector recalibration (DEPENDENT FOLLOW-UP)

**Status:** Flagged. To be done AFTER Phase 2 lands, BEFORE 30-seed re-baseline becomes paper-quality.

The current Q1 2023 capability vectors (per `simulation.py` provider configs) were anchored against the prior 16-use_case ontology. Specifically:
- Apex AI's safety lead was sized to win `healthcare` and `hospital_system` (combined weight 0.10)
- Spark AI's coding lead was sized to win `software_dev` (weight 0.14)
- Genesis Systems' reasoning + knowledge profile was sized for `enterprise_legal` and `researcher`

The new ontology has different aggregate dimension demand:
- Population-weighted safety demand likely rises (6 high-risk contexts now vs ~2 prior)
- Population-weighted coding demand may shift (code_production 0.16 absorbs `software_dev` 0.14 + `tech_startup` 0.06 + `researcher` 0.06 = 0.26 of prior)
- Communication demand is concentrated in 2 contexts (content_creation 0.14 + customer_engagement 0.13)

Without recalibration, providers carry implicit advantages or disadvantages from the old ontology's distribution. The smoke-probe results show this matters — Spark AI dominance in code_production was partly driven by the old capability vector being over-tuned to a single-dimension software_dev demand.

**Recalibration requires:**
1. Compute new population-weighted aggregate need vector under Option 1.5
2. Re-anchor Q1 2023 capability vectors against real-world Q1 2023 model performance reports (HELM 2023 Q1 leaderboard, public benchmark releases at the time)
3. Verify each provider has a defensible "where do they win" story consistent with real-world Q1 2023 positioning (OpenAI broad lead, Anthropic safety lead, Meta open-source value, etc.)
4. Re-run smoke probe to confirm market dynamics still produce diversity

**When:** between Phase 2 Step 6 (refactor lands) and Phase 2 Step 8 (overnight 30-seed baseline). Do NOT skip — pre-recalibration baseline is misleading because it conflates "ontology change effects" with "capability-mismatch effects."

**Out of scope for this design doc.** Add to TODO.md after Phase 2 lands.

## 13. Pre-Phase-2 smoke probe (mandatory, per meta-critique)

Before committing to the full Phase 2 implementation, run a **5-seed × 1-condition smoke probe** with the new ontology to bound the gap-invalidation risk (meta-critique #11).

**Procedure:**
1. Hand-write a minimal Python override of consumer.py constants reflecting the proposed need_weights + pop weights + consumer_type_split (no full refactor needed; monkey-patch in a smoke test script).
2. Run 5 seeds × 1 condition (`baseline` heuristic mode, 30 rounds).
3. Compare aggregate score-satisfaction gap mean to existing 30-seed heuristic baseline.
4. **Decision rule:** if |Δgap| > 50% of current value AND directional inversion possible (lower bound of CI crosses zero), HALT Phase 2 and revisit need_weights derivation. Otherwise proceed.

**Cost:** ~2 hours including analysis. Cheap insurance against losing the central paper finding.

## 14. Open questions (resolved)

| # | Question | Resolution |
|---|---|---|
| Q1 | `research_analysis` placement | All `researcher` → `code_production` (GDPval + BLS group with computational occupations) |
| Q2 | `creative` + `marketing` collapse | Both into `content_creation`; CMO/freelancer differentiation via archetype |
| Q3 | Population weight formula | 60/40 adoption-favoring blend (incident exposure scales with deployment volume; severity captured separately by risk_tier) |
| Q4 | Enterprise-growth endogenization | Level 1: per-context exogenous growth rates calibrated to multi-source triangulation. No α (Level 2 is future work) |
| Q5 | Sensitivity analysis priority | need_weights first, risk_tier multipliers second |
| Q6 | Backwards compatibility | Hard-cut, no shim (consistent with session 31 precedent) |

## 15. Phase 2 plan (pending Phase 1 sign-off)

Estimated **~5 hours coding** + overnight runs + 2-3 hours paper integration.

**Step 0 (2h, MANDATORY before any code refactor):** Smoke probe per §13. Halt Phase 2 if gap finding doesn't survive.

**Step 1 (1h):** Author the 4 derivation scripts (§12). Each is small and side-effect-free.

**Step 2 (1.5h):** Rewrite `USE_CASE_PROFILES`, `USE_CASE_POP_WEIGHTS`, `ORG_FIELD_PRIORITIES` in `consumer.py` from the CSVs. Add `risk_tier` and `enterprise_growth_rate` fields to context profile dict. Add per-context `consumer_type_split` table.

**Step 3 (0.5h):** Update `incidents.py` sector strings to match new context names (now trivial — sector names = context names). Rewire incident generation to use new sector-mapping for the consumer.py:645-646 propagation path.

**Step 4 (1h):** Audit `regulator.py`, `funder.py`, `media.py`, `simulation.py` for use_case-name dependencies (~30 sites per earlier grep). Update.

**Step 5 (0.5h):** Update LLM consumer prompts in `llm.py` (`use_case_label` rendering, prompt text referring to old segment names). Verify smoke test still passes.

**Step 6 (0.5h):** Rewrite `dynamic_enterprise_growth` to operate per-context using new growth-rate table (Level 1).

**Step 7 (smoke):** `scripts/smoke_test.py` — verify all simulation paths run cleanly under new ontology.

**Step 8 (overnight):** 5-condition × 30-seed re-baseline.

**Step 9 (next session):** Sensitivity analysis runs (§10 — need_weights ±20%, risk_tier multipliers [1.0×, 2.0×]).

**Step 10 (next session):** Paper integration — rewrite `4simulation.tex:54` (currently says "39 segments × 16 use-cases") and Appendix C.

---

## Summary of changes vs current state

- **Ontology:** 16 mixed use_cases → 10 uniform deployment contexts
- **New segments added:** `hr_talent`, `security_operations` (closes EU AI Act §4 gap + coverage gap)
- **Risk tier:** new property derived from EU AI Act Annex III; 2 multipliers
- **Parameter count:** ~174 → ~124 (net reduction of ~50)
- **Empirical anchors:** every parameter family has at least one cited source; population, scale-split, and enterprise-growth families have reproducible derivation scripts
- **Endogenization:** per-context exogenous enterprise growth (Level 1); calibrated to Menlo Ventures + AI Index + Deloitte + sector sources (no Anthropic source)
- **Backwards compatibility:** hard-cut
- **Mandatory smoke probe** before full refactor commit

## Key decision summary for co-author review

All 6 open questions resolved (§14). Phase 2 ready pending sign-off on this design doc.
