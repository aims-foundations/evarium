# Case Studies — Policy-Adjacent Questions for the Evaluation Ecosystem Simulation

A bank of case studies showing how the evaluation ecosystem simulation can be used to investigate policy-adjacent questions. Each study pairs a real-world policy or market phenomenon with a mechanism sketch in the simulation.

## Inventory

| # | Case study | Policy or market anchor | Simulation mechanism |
|---|---|---|---|
| 1 | [Privacy ladder](privacy_ladder.md) | Epoch private holdouts, FrontierMath-T4, SEAL-Safety | `holdout_fraction` + reporting lag K + cosine distance |
| 2 | [Transparency mandate](transparency_mandate.md) | SB 53 (CA), NY RAISE, EU AI Act Article 55 | Rolling-mean disclosure of `safety_allocation` to consumer / funder / media channels |
| 3 | [Media as shadow evaluator](media_shadow.md) | Sora/Devin virality, AI Twitter influence (Hardy et al. 2024) | `media_trust` term in `expected_quality`; viral-tweet observations in planner prompt |
| 4 | [Evaluator capture](evaluator_capture.md) | LMArena, Leaderboard Illusion, Scale/SEAL | `evaluator_as_company` flag; best-of-N + early access |
| 5 | [Benchmark sponsorship](benchmark_sponsorship.md) | FrontierMath / OpenAI, ARC Prize, MLPerf | Per-benchmark sponsor attribution; sponsor pre-access; scoring asymmetry |
| 6 | [Audit and verification](audit_verification.md) | UK AISI, RAISE third-party audit, Anthropic RSP, AVERI landscape | Five senses of "audit"; declare-then-verify game |
| 7 | [EU vs US regulatory philosophy](eu_us_regulation.md) | EU AI Act, CA SB 53, US EO reversal, Italy Garante €15M | `intervention_threshold` + graduated-sanction presets |

## How to use this bank

- **Policy anchor and simulation mechanism** are kept in separate sections so a reader can read the real-world framing without committing to the mechanism details, or jump straight to the implementation if they already know the policy.
- **References** at the end of each study point to the primary policy texts and academic frames that anchor the mechanism.
- **Open questions** flag what would need to be resolved to extend or recalibrate each mechanism.

## Adding a new case study

Create `case_studies/<snake_case_name>.md` with these sections:

1. **Policy anchor** — the real-world proposal or market phenomenon, with at least three references.
2. **Simulation mechanism** — primitives, parameters, and ablation conditions.
3. **Findings** (if implemented) or **Hypothesis** (if not) — what the simulation shows or is expected to show.
4. **Open questions** — what would need to be resolved before running or extending.
5. **References** — real-world anchors and academic frames.

Then add a row to the inventory table above.

## Related docs

- `docs/stakeholders.md` — canonical architecture reference for all primitives used in these mechanisms.
- `docs/references.md` — master reference list; case studies cite into it.
