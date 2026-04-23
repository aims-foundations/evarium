# Case Studies — Policy-Adjacent Questions for the Evaluation Ecosystem Sim

**Last updated:** 2026-04-22

A bank of case studies showing how the evaluation ecosystem simulation can be used to answer policy-adjacent questions. Each study pairs a real-world policy or market phenomenon with a sim mechanism sketch. Use these as (a) references in the main paper, (b) appendix sketches, (c) seeds for follow-on work.

## Inventory

| # | Case study | Policy anchor | Sim mechanism | Status | Paper location |
|---|---|---|---|---|---|
| CS1 | [Privacy ladder](privacy_ladder.md) | Epoch private holdouts, FrontierMath-T4, SEAL-Safety | `holdout_fraction` + K=3 lag + cosine distance | **Live** | §5.2 |
| CS2 | [Transparency mandate](transparency_mandate.md) | SB 53 (CA), NY RAISE, EU Art 55 | Rolling-mean disclosure of `safety_allocation` → consumer / funder / media | **Designed** | §5.3 |
| CS3 | [Media-as-shadow-evaluator](media_shadow.md) | Sora/Devin virality, AI Twitter influence, `hardy2024benchmarks` | `media_trust` term in `expected_quality`; top-3 viral tweets in planner prompt | **Designed** | §5.4 |
| CS4 | [Eval-as-company](eval_as_company.md) | LMArena, Leaderboard Illusion, Scale/SEAL | `evaluator_as_company` flag; best-of-N + early access | **Demoted** | App. H |
| CS5 | [Benchmark sponsorship](benchmark_sponsorship.md) | FrontierMath / OpenAI, ARC Prize, Epoch | Per-benchmark sponsor attribution; sponsor pre-access; scoring asymmetry | **Brainstorm** | — |
| CS6 | [Audit & verification](audit_verification.md) | AISI, RAISE third-party audit, Anthropic RSP, AVERI landscape | 5 senses of "audit"; declare-then-verify game | **Brainstorm** | — |
| CS7 | [EU vs US regulatory philosophy](eu_us_regulation.md) | EU AI Act, CA SB 53, US EO reversal, Italy Garante €15M | `intervention_threshold` + graduated-sanction presets | **Archival** | App. archival |

## Status legend

- **Live** — mechanism implemented, runs exist, referenced in current paper.
- **Designed** — mechanism specced at ~LOC level, not yet implemented.
- **Brainstorm** — framing established, mechanism not yet specced; belongs to a post-deadline workstream.
- **Demoted** — originally load-bearing, moved to appendix after recalibration revealed weaker effect than assumed.
- **Archival** — implemented early, no longer load-bearing, preserved for reference.

## How to use this bank

- **Citing in main paper:** each case study has a "paper claim" subsection formatted for lifting into section text.
- **Appendix sketches:** `Policy anchor` + `Sim mechanism` subsections give reviewers a ~1-page summary without requiring mechanism depth.
- **Reviewer responses:** matrix above answers "why didn't you simulate X policy" — point at status and scope.
- **Follow-on workstreams:** `Brainstorm` studies (CS5, CS6) are candidates for post-deadline development; CS4 is a candidate for recalibration work.

## Adding a new case study

Create `case_studies/<snake_case_name>.md` with these sections:

1. **Policy anchor** — the real-world proposal or market phenomenon, with ≥3 references.
2. **Sim mechanism** — primitives, parameters, LOC estimate, ablation conditions.
3. **Status** — live / designed / deferred / brainstorm, and what's blocking.
4. **Paper claim** (if live/designed) — ≤100 words, written as it would appear in §5.
5. **Open questions** — what would need to be resolved before running.
6. **References** — real-world anchors + academic frames.
7. **Internal pointers** — relevant `src/`, `scripts/`, and session memory files.

Then add a row to the inventory table above.

## Related docs

- `docs/stakeholders.md` — canonical architecture reference for all primitives used in these mechanisms.
- `docs/references.md` — master reference list; case studies cite into it.
- `docs/validation_brainstorm.md` — empirical validation approaches (orthogonal to policy framing).
