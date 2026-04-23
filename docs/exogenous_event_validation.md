# Exogenous Event Validation

**Last updated:** 2026-04-22

Face-validity check via real-world event replay. Inject a concrete shock corresponding to a known event in the 2023–25 AI industry history, let the sim run forward, and evaluate whether actor responses pattern-match the observed real-world response.

## 1. Purpose

Distinct from other validation activities in the project:

| Activity | Question | Location |
|---|---|---|
| **Mechanism testing** (case studies) | Does the sim produce expected directional effects when mechanism X is toggled? | `docs/case_studies/` |
| **Empirical calibration** | Do sim parameters match real-world values? | `external-validation/` |
| **Face validity (this doc)** | Do actors respond to known real events in qualitatively plausible ways? | Here |
| **PIMMUR / architectural** | Are the primitives themselves structurally valid? | `rough/validation_plan.md`, `docs/pimmur_principles.md` |

The framing corresponds to **Sargent's operational validity** and **Windrum's empirical descriptive accuracy**. It is not mechanism validation; it tests the sim's holistic response to an exogenous shock against the observed real-world response.

## 2. Conventions

### 2.1 Shock operationalization principles

- **Dual-injection path.** Every shock has two parallel components: **(a) state perturbation** (capability vector, media sentiment, funding) so the sim's existing mechanisms see a changed world, and **(b) narrative event description** — a short natural-language field (`recent_exogenous_events`) injected into LLM planners' planning prompt. Component (b) is the load-bearing channel for face validity; (a) exists so state propagates consistently and heuristic actors don't freeze. Without (b), LLMs are back-deriving the scenario from state variables alone, which is both harder and unrealistic (real actors read the news, they don't reverse-engineer market data).
- **One-round exogenous injection only.** Both components applied at a single round. Everything after propagates through existing mechanisms.
- **No mid-run parameter changes.** Regulator presets, consumer weights, benchmark pool, narrative decay rates — all held constant. No retrofitting of primitives to make the rubric pass. If the sim can't respond plausibly, that's a finding, not a bug to patch.
- **No new actor levers for the event.** Actors respond using the levers they already have (portfolio rebalance, allocation shift, ladder escalation, media narrative transition). If an actor's available levers can't express a plausible response, that's a scope-limitation to report, not a reason to add levers.
- **Target the analog provider where one exists.** Provider-specific shocks apply to the provider whose real-world analog matches (see `docs/stakeholders.md` name mapping).
- **Document what the shock does NOT model.** Out-of-sim effects (stock markets, foreign policy, etc.) are explicitly scoped out per event.

### 2.2 Two-tier run plan

| Tier | N | Purpose | Evaluation mode |
|---|---|---|---|
| **Heuristic** | 60 matched pre/post (30 seeds × 2 conditions) | **Structural sanity** — does the sim not crash under the shock? Does state propagate? Does baseline drift not dominate? | Diagnostic only — heuristics respond to state variables they were pre-coded to watch; they cannot face-validly respond to novel events. Not a face-validity verdict. |
| **LLM** | 4 paired (2 shock + 2 no-shock, seeds matched, claude-sonnet-4-6) | **Face validity** — do LLM actors reason plausibly about the novel scenario using their planning prompts (with injected event description) and the levers they already have? | Trace inspection — do reasoning traces cite the right things? Are actions consistent with rationales? Reported as existence claims, not prevalence claims (N=2 doesn't support the latter). |

**LLM carries the face-validity verdict.** Heuristics cannot: they only respond to state variables, and the meaning of a novel event lives in its context (competitive frame, market narrative), not in a new state variable. LLMs can reason about context if it's in their planning prompt. Heuristic runs serve to confirm the sim doesn't break under the shock, nothing more.

### 2.3 Rubric conventions

Each event has **4–5 trace-evaluation questions**, one per relevant actor pathway. Questions frame as:

> "Does [actor]'s reasoning trace demonstrate [the expected articulation of the new situation]?"

Evaluation protocol per question:

- **Pass** — at least one of the matched actor's shock-condition traces articulates the expected reasoning, AND the matched no-shock traces do not. (The matched-control check confirms the reasoning is event-triggered, not endogenous to the actor's planning style.)
- **Fail** — shock traces do not articulate the expected reasoning, OR shock and no-shock traces articulate it equally (not event-triggered).
- **Partial** — some but not all matched actors articulate it. Document verbatim.

**Pass/fail is existence-level at N=2.** We report "2/2 Apex traces in shock runs named OpenCore as a competitive threat; 0/2 baseline traces did" as a verbatim observation, not a prevalence claim. This is face validity, not a statistical test.

Traces are reported verbatim in the run writeup, alongside the judgment. Failed questions are more informative than passed ones — they bound what the sim can plausibly support.

### 2.4 Sim length

Default: 40 rounds (extended from the canonical 30) to give ≥ 15 rounds of post-shock runway for persistence claims.

## 3. Inventory

| # | Event | Real-world date | Sim round | Pathway tested | Status |
|---|---|---|---|---|---|
| EV1 | [DeepSeek R1 release](#51-deepseek-r1-release-jan-2025) | Jan 2025 | R25 | Surprise shock — reactive reasoning; single analog | **Designed** |
| EV2 | [EU AI Act entry into force](#52-eu-ai-act-entry-into-force-aug-2024) | Aug 2024 | R20 | Scheduled regulation — anticipatory + heterogeneous-scope + collective reasoning | **Designed** |
| EV3 | o1-preview release | Sept 2024 | R21 | Competitive R&D response | Candidate |
| EV4 | Italy Garante ChatGPT fine | Dec 2024 | R24 | Concrete enforcement under EV2 framework | Candidate |
| EV5 | FrontierMath/OpenAI disclosure | Jan 2025 | R25 | Evaluator-capture exposure | Candidate (awaits CS5) |
| EV6 | Sora 2 launch | Sept 2025 | R33 | Media virality pathway | Candidate (awaits CS3) |
| EV7 | Gemini image-gen pullback | Feb 2024 | — | Reputation-crisis event — **sim scope limit** | Demoted |

## 4. How to use this bank

- **Adding a new event:** create a new subsection with the template (§5.1 is the canonical example). Add a row to the inventory above.
- **Running an event:** see the Run Plan subsection for each event. Outputs go to `sandbox/experiments/face_validity_<event_id>/`.
- **Reporting:** failed questions are more informative than passed ones. A rubric with most T-questions passing plus one or two failing is more useful as diagnostic material than a clean sweep — a clean sweep suggests either the LLM layer is articulating everything in its training data (prompt-echoing) or the rubric is too permissive.
- **Relationship to paper:** events that pass broadly at the LLM trace level can be cited as supporting face validity in an Appendix F subsection, with a representative trace pair shown verbatim. Events that fail partially are worth reporting — they bound the claim range the LLM layer can plausibly support, and often point at primitive-fit limitations (e.g., no political-ideological narrative axis for Gemini).

## 5. Events

### 5.1 DeepSeek R1 release (Jan 2025)

**Real-world summary.** Open-source frontier model released Jan 20 2025 by DeepSeek. Claimed frontier-level performance on reasoning/math benchmarks at a training cost reported at ~$5–6M (disputed). Triggered the Jan 27 NVIDIA ~$600B single-day market-cap drawdown, pressure on OpenAI/Anthropic valuations, narrative pivot ("efficiency beats scale," "moats are weaker than assumed"), rapid developer adoption of the free weights, and US export-control debate.

**Sim analog provider.** OpenCore (modeled after DeepSeek; `open_source: True`).

#### Shock operationalization (R25)

**(a) State perturbation.** Minimal; just enough to keep state propagation coherent so heuristics don't freeze and LLMs observe a changed world alongside the narrative.

- OpenCore capability vector bumped to ≈ 90% of leader on reasoning + coding + math-adjacent dimensions.
- OpenCore `cost_advantage` already high by virtue of `open_source: True` — no change.
- OpenCore funding bumped modestly.
- **No media sentiment injection.** Media is algorithmic; its response to the event is part of what's being tested via the existing sentiment/attention/narrative-state machinery, not prescribed.

**(b) Narrative event description** (new `recent_exogenous_events` context field in every LLM actor's planning prompt, for rounds R25 through R27):

```
An open-source model provider (OpenCore) has released a frontier model
this round, claiming performance parity with leading closed models at
roughly 10× lower training cost. Public weights are available. Industry
coverage is dominated by an "efficiency over scale" framing, with
commentary questioning the durability of incumbent cost moats.
```

No numbers prescribed beyond "10× lower training cost" (this is a real public claim, fair for actors to observe). No prescribed response direction. Actors read this as situational awareness and decide what to do.

**Unchanged:** other providers, regulator state, incident schedule, consumer weights, benchmark pool, media decay parameters, graduated ladder thresholds. If the sim can't respond plausibly with these held fixed, that's a finding.

#### Rubric — 5 trace-evaluation questions

| # | Actor | Question |
|---|---|---|
| **T1** | **Incumbent providers (Orion, Apex)** | Does the planning-trace name OpenCore (or the open-source entrant) as a competitive threat? Does the reasoning cite one of: cost-efficiency / open-source release / capability parity / moat erosion? |
| **T2** | **Incumbent providers (Orion, Apex)** | Is the chosen action consistent with the reasoning in T1? A trace that names OpenCore but then makes an allocation move unrelated to the stated concern is a fail. Tests rationale-action coherence. |
| **T3** | **Funders (VC type vs government/foundation)** | Do VC-type funder traces articulate reconsideration of capital-intensity assumptions, moat-durability, or efficiency-vs-scale framing? Do government/foundation traces remain more stable in reasoning content? Tests funder-type differentiation at the reasoning layer. |
| **T4** | **Regulator** | Does the regulator trace acknowledge the event (export-control dynamics, open-source frontier availability, competitive-market framing) but decline to escalate beyond `advisory`? Restraint-in-trace is the signal — regulator should notice, not sanction. |
| **T5** | **OpenCore itself** | Does the OpenCore trace reason about its new competitive position — whether to lean into open-source advantage, shift focus to a specific dimension, hedge against incumbent response? Tests whether the LLM-mode analog provider internalizes its own strategic shift. |

Consumer is formula-based, not LLM — no consumer trace question.

Media is algorithmic — no media trace question. Media *behavior* in response to the event still matters (it's observable in the run output, and incumbent traces will respond to it), but there's no media reasoning to inspect.

#### Run plan

- **Heuristic** (structural sanity): 60 runs. 30 seeds, matched shock vs no-shock pairs. Sim length 40 rounds, shock at R25. Output `sandbox/experiments/face_validity_deepseek_r1/heuristic/{shock,noshock}/seeds/seed_<N>/rounds.jsonl`. Purpose: confirm sim doesn't crash, state propagates, baseline drift doesn't dominate. Not the face-validity verdict.
- **LLM** (face validity): 4 runs. 2 seeds, matched shock vs no-shock pairs. claude-sonnet-4-6. Sim length 40 rounds, shock at R25. `actor_traces/` preserved for every LLM-mode actor. Output `sandbox/experiments/face_validity_deepseek_r1/llm/{shock,noshock}/seeds/seed_<N>/`. Purpose: trace-based reasoning evaluation per T1–T5. One wave, ≤4 concurrent per scheduling policy.
- **Pairing rule:** same seed + same everything except the shock injection. Comparison is within-seed to neutralize seed-driven reasoning variance.

#### Reporting

For each of T1–T5:

- Pass / Fail / Partial judgment per matched trace pair.
- Verbatim excerpts from both shock and no-shock traces side-by-side, so a reader can audit the judgment.
- Aggregated across both seeds, a summary line: "T1: 2/2 shock traces pass; 0/2 no-shock traces articulate."

Paper reporting: if most T-questions pass at the existence-claim level, cite as face-validity support in Appendix F with a selected illustrative trace pair. Failed T-questions are reported as scope limitations of the current LLM layer or sim context.

#### Explicitly NOT tested

- Exact magnitude match to real-world share / valuation / timing.
- Statistical prevalence — N=2 supports existence, not "usually" or "typically" claims.
- US export-control or foreign-policy discourse (no foreign-policy actor in sim; if a regulator trace gestures toward it, that's interesting color but not load-bearing).
- Stock-market or public-equity reactions.
- Heuristic face validity — heuristic providers cannot face-validly respond to novel events; their runs are structural-sanity only.
- Mechanism correctness at the primitive level (that's case-study territory, not here).

#### Open questions

- **R25 timing.** Q1 2023 + 25 months = Feb 2025; DeepSeek R1 was Jan 20 2025. Within ± 1 round — fine.
- **Event description phrasing.** The paragraph above uses "10× lower training cost" and "efficiency over scale" — both real public framings. Is the specificity right? Worth 1–2 drafts before running; wrong phrasing could either under-signal (LLMs miss the event) or over-prescribe (LLMs parrot the description).
- **`recent_exogenous_events` field implementation.** New injection channel; needs a small patch to the LLM planning-prompt builder(s) — likely `src/actors/model_provider.py`, `regulator.py`, `funder.py`. ~10–20 LOC, no mechanism change, just an optional context field. Implementation precedes running.
- **Capability-bump magnitude.** "≈ 90% of leader" is first-pass; may revise per-dimension once we look at R1's actual benchmark-parity profile.
- **How many LLM actors need to be in LLM mode for this to be meaningful?** Currently most actors have both heuristic and LLM modes. Face validity needs the incumbent providers and at least one funder-per-type to be LLM mode. Confirm config before running.

#### References

- Real-world anchors:
  - DeepSeek-R1 paper (arXiv:2501.12948)
  - NVIDIA Jan 27 2025 market-cap drawdown coverage
  - OpenAI o3-mini pricing response announcements
  - Meta Llama 4 acceleration reports
- Sim primitives:
  - `docs/stakeholders.md` — OpenCore provider preset; consumer segment structure
  - `docs/consumer_redesign.md` — segment heterogeneity
  - `src/actors/funder.py` — funder-type allocation logic
  - `src/actors/media.py` — narrative-state transitions

### 5.2 EU AI Act entry into force (Aug 2024)

**Real-world summary.** The EU AI Act entered force on 1 Aug 2024 after a multi-year legislative process. Four-tier risk classification (unacceptable / high / limited / minimal) with corresponding obligations. Phased rollout: prohibited practices effective 2 Feb 2025 (R26 in sim); GPAI obligations effective 2 Aug 2025 (R32); full applicability 2 Aug 2026 (post-sim). Fines to €35M or 7% global turnover. First major comprehensive AI regulation globally. Industry responses during the pre-entry and post-entry windows included the GPAI Code of Practice — signed by Amazon, Anthropic, Google, IBM, Microsoft, OpenAI by Dec 2025; Meta declined.

**Sim analog.** Cross-ecosystem event — affects all providers, not one analog. Scope differentiation:

- **Covered** (systemic-risk, 10²⁵ FLOPs threshold): Orion, Apex, Genesis, Mirage, OpenCore (5/6).
- **Exempt** (below threshold): Spark (1/6).

**Pathway tested.** Three LLM-reasoning operations the surprise-shock frame of EV1 cannot test:

1. **Anticipatory reasoning** — known-in-advance regulation with phased rollout. Does the LLM layer adapt *before* obligations bite, or only react when enforcement arrives?
2. **Heterogeneous-scope reasoning** — does each actor differentiate its reasoning based on whether it's in scope? Spark (exempt) should reason differently from Orion (covered).
3. **Collective reasoning** — second-order: do provider traces surface industry-wide dynamics (voluntary commitments, cooperative signaling, free-riding)?

**Contrast with EV1.**

| | EV1 DeepSeek | EV2 EU AI Act |
|---|---|---|
| Event type | Surprise | Scheduled (phased) |
| Scope | Single analog | Cross-ecosystem, heterogeneous coverage |
| LLM reasoning tested | Reactive | Anticipatory + heterogeneous + collective |
| State perturbation needed | Yes (capability + funding) | Minimal (regulator preset unchanged) |

#### Shock operationalization

**(a) State perturbation.** None. The regulator preset already exists; sim regulatory parameters unchanged. The event is regulatory-informational, not state-perturbative.

**(b) Narrative event description** — injected via `recent_exogenous_events` into LLM planner prompts. **Multi-stage injection** matching the real-world phased rollout: R20 (entry into force), R26 (prohibited practices effective), R32 (GPAI obligations effective). Actors observe the staged arrival of enforcement milestones.

**R20 — entry into force:**

```
A comprehensive AI regulatory framework has entered force in a major
jurisdiction, covering all providers deploying AI systems to its
market. The framework uses a four-tier risk classification with
corresponding obligations. Large frontier providers (above a compute
threshold) face additional duties: ongoing model evaluation, incident
reporting, and documentation. Fines scale to substantial fractions of
global revenue. Phased rollout: prohibited practices effective in
~6 months, general-purpose AI obligations in ~12 months, full
applicability in ~24 months.
```

**R26 — prohibited practices active:**

```
The first enforcement stage of the AI regulatory framework is now
active. Practices classified as unacceptable risk are prohibited;
enforcement actions can be initiated.
```

**R32 — GPAI obligations active:**

```
General-purpose AI obligations are now enforceable. Covered providers
must comply with documentation, evaluation, and incident-reporting
duties or face fines.
```

No specific numbers (no "10²⁵ FLOPs", no "€35M"), no prescribed response direction. Stylized to avoid prompting LLMs to parrot real document language; focus is on structural shift.

**Unchanged:** regulator presets, consumer weights, benchmark pool, incident schedule, media parameters. If providers can't anticipate plausibly with levers they already have, that's a finding.

#### Rubric — 5 trace-evaluation questions

| # | Actor | Question |
|---|---|---|
| **T1** | **Covered providers** (Orion, Apex, Genesis, Mirage, OpenCore) | Does the trace acknowledge the upcoming regulatory regime? Does reasoning *anticipate* future obligations (documentation, evaluation, incident reporting) — treating the regulation as a forward constraint to prepare for rather than a static cost to absorb? |
| **T2** | **Exempt provider** (Spark) | Does Spark's trace differentiate — either noting its below-threshold position, or reasoning about coverage-if-it-grows? This is the distinctive heterogeneous-reasoning signal for this event. If Spark reasons identically to covered providers, the LLM layer isn't using self-knowledge about scope. |
| **T3** | **Funders** (VC vs gov/foundation) | Do VC traces incorporate regulatory-risk premium — tilting toward compliance-ready providers or weighting compliance preparedness? Do government/foundation traces articulate alignment-with-regulation framings (regulatory favorability as an allocation factor)? |
| **T4** | **Regulator** | Primary (EU preset): does the regulator trace reason about exercising expanded authority, coordinating enforcement timing, or prioritizing specific providers? Secondary (US preset, if paired): does it reason about EU frame as influencing its own calibration — regulatory divergence or pressure to respond? |
| **T5** | **Collective-action signal** (second-order) | Across multiple covered-provider traces in the shock condition: do any surface industry-wide dynamics — voluntary commitments, cooperative code-of-practice signaling, free-riding on others' advocacy, pre-emptive positioning? Real-world had the GPAI Code of Practice (most labs signed; Meta refused). If the LLM layer never surfaces collective reasoning, that's a meaningful scope finding about single-actor-only reasoning. |

T2 and T5 are the distinctive tests. T2 checks self-knowledge-of-scope (a first-order operation the sim has never directly stressed); T5 checks second-order reasoning about peer behavior.

#### Run plan

- **Heuristic** (structural sanity): 60 runs. 30 seeds, matched shock vs no-shock pairs. Sim length 40 rounds; narrative injection at R20, R26, R32. Output `sandbox/experiments/face_validity_eu_ai_act/heuristic/{shock,noshock}/seeds/seed_<N>/rounds.jsonl`. Purpose: confirm sim loop holds across the three injection rounds.
- **LLM** (face validity): 4 runs. 2 seeds, matched shock vs no-shock pairs. claude-sonnet-4-6. `actor_traces/` preserved for every LLM-mode actor. Output `sandbox/experiments/face_validity_eu_ai_act/llm/{shock,noshock}/seeds/seed_<N>/`. Purpose: trace-based reasoning evaluation per T1–T5.
- **Regulator preset:** run with **EU preset as primary** (since this is the regulator whose authority the event expands). Optional **US-preset secondary run** for T4's divergence sub-test — adds 2 more LLM runs if desired, or defer as follow-on.
- **Pairing rule:** within-seed comparison.

#### Reporting

For each T1–T5:

- Pass / Fail / Partial judgment per matched trace pair.
- Verbatim excerpts side-by-side.
- **T1 aggregation:** 5 covered providers × 2 seeds × 2 conditions = 20 trace contexts. Report both per-provider breakdowns and aggregate.
- **T2 aggregation:** 1 provider × 2 seeds × 2 conditions = 4 trace contexts. Small N; verbatim reporting is the whole evaluation.
- **T5 reporting:** if any provider in any seed surfaces collective-action reasoning in the shock condition and not in the no-shock, highlight verbatim — second-order reasoning is a distinctive finding.

Paper reporting: T1/T2/T3 passing supports "LLM actors reason anticipatorily about scheduled regulation and differentiate based on scope." T5 passing is a bonus finding worth its own paragraph. T4 divergence result (US preset reasoning about EU frame) is appendix-level color.

#### Explicitly NOT tested

- Legal/technical fidelity — LLMs may misstate Annex III specifics or compute thresholds; we aren't grading legal accuracy, just structural reasoning plausibility.
- Compliance outcomes — whether a given provider's reasoning would pass a real audit is out of scope.
- Multi-jurisdictional providers — sim providers are global; no per-jurisdiction compliance modeling.
- Enforcement-lag calibration — that's CS7 regulator-preset parameter work, not face validity.
- Specific enforcement cases (Italy Garante, X/Grok) — those are candidate EVs (EV4), separate.

#### Open questions

- **R20 timing.** Q1 2023 + 20 months = Sept 2024; EU AI Act entry was Aug 1 2024. Within ± 1 round.
- **Multi-stage re-injection.** Default plan: re-inject at R26 and R32 with updated framing. Alternative: inject only at R20, let actors reason forward. Default preserves faithfulness to real-world phased rollout; alternative cleaner for testing anticipatory reasoning in isolation. Worth trying default first and observing whether traces reference the coming milestones even before re-injection.
- **Regulator preset choice.** Primary EU preset; US as optional divergence test. Scope as primary-only for initial run; add US as follow-on if the primary produces ambiguous T4.
- **`recent_exogenous_events` field implementation.** Same patch as EV1 — one implementation serves both events.
- **Spark LLM mode.** T2 requires Spark to be in LLM planning mode. Confirm config includes Spark as LLM-mode provider; otherwise T2 is untestable.
- **T5 ambiguity.** "Collective-action reasoning" is fuzzier than T1–T4. Pre-agreed markers: provider mentions other providers *by name*, discusses industry-wide response, considers whether to move first vs wait, or references voluntary vs mandatory compliance. Without these markers, T5 is hard to judge.

#### References

- Real-world anchors:
  - EU AI Act — Regulation (EU) 2024/1689; official consolidated text
  - European AI Office — GPAI Code of Practice signatories (Dec 2025)
  - Latham & Watkins — "EU AI Act: GPAI Model Obligations in Force and Final GPAI Code of Practice in Place"
  - FPF — "Conformity Assessments under the EU AI Act: Step-by-Step"
  - Linux Foundation Europe — "What Open Source Developers Need to Know about the EU AI Act"
  - Public compliance statements: Anthropic (2024), Google DeepMind (2024), Microsoft (2024), Meta refusal (Dec 2025)
- Sim primitives:
  - `docs/case_studies/eu_us_regulation.md` (CS7) — existing regulator preset framework
  - `docs/case_studies/transparency_mandate.md` (CS2) — adjacent regulatory-disclosure mechanism
  - `docs/stakeholders.md` — provider compute/revenue attributes used for scope determination

## 6. Future candidates and scope-limit cases

### 6.1 Implementable candidates

- **EV3 — o1-preview release (Sept 2024).** Capability-differentiation shock. Tests whether provider traces reason about follow-the-leader positioning when one competitor breaks out on a differentiated dimension (reasoning). Pure provider-to-provider dynamics. Complements EV1 (general capability entry) with a dimension-specific breakout.
- **EV4 — Italy Garante ChatGPT fine (Dec 2024).** Concrete enforcement action under the EV2 framework. Tests whether regulator and provider traces reason about a specific enforcement event (not just the framework's arrival). Best run *after* EV2 as a follow-up enforcement-specific face-validity check.
- **EV5 — FrontierMath / OpenAI disclosure (Jan 2025).** Evaluator-capture exposure. Awaits CS5 (benchmark sponsorship) implementation.
- **EV6 — Sora 2 launch (Sept 2025).** Media virality pathway. Awaits CS3 (media shadow) implementation.

Candidates depending on unimplemented case studies (EV5, EV6) are parked. Those that exercise existing mechanisms (EV3, EV4) queue after EV1, EV2.

### 6.2 Scope-limit cases (demoted)

- **EV7 — Gemini image-gen pullback (Feb 2024). Demoted.** Real-world was a reputation-crisis event: outputs widely perceived as politically objectionable triggered social-media backlash, product pullback, and a multi-month "Google is behind" narrative. Unlike safety incidents (physical/financial harm), reputation crises depend on (a) a reputation-incident primitive distinct from safety-incident — **not in sim**, and (b) a political-ideological narrative-state axis — **not in sim**. The no-retrofit principle (§2.1) forbids adding primitives to make the rubric pass, so Gemini cannot be face-validly tested under the current architecture.

  Retained as a **documented scope-limit finding** rather than an implementable candidate. The category it represents (reputation crisis without physical harm) is a legitimate class of real-world event the sim currently cannot validate — worth citing in paper scope discussion as an explicit boundary of what ecosystem-level claims this framework can support. Reconsider only if a narrative-axis primitive is later added (would also benefit CS3 media shadow).

## 7. References

### Validation frameworks

- Sargent (2013). Verification and validation of simulation models. *Proc. Winter Simulation Conf.*
- Windrum, Fagiolo, Moneta (2007). Empirical validation of agent-based models: alternatives and prospects. *JASSS*.
- Axtell, Axelrod, Epstein, Cohen (1996). Aligning simulation models: a case study and results. *Computational & Mathematical Organization Theory*.
- Park et al. (2023). Generative agents: interactive simulacra of human behavior. (Docking methodology.)

### Internal

- `rough/validation_plan.md` — Sargent/PIMMUR/Windrum/Axtell/Park validation plan
- `docs/validation_brainstorm.md` — ~40 validation approaches (session 37, prioritized)
- `docs/pimmur_principles.md` — architectural validity checklist
- `docs/case_studies/README.md` — mechanism-testing bank (complementary to this doc)
