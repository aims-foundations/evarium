# CS6: Audit & Verification

**Status:** Brainstorm. Collects the five distinct senses of "audit" that have accumulated across the project and sketches the declare-then-verify game-theoretic extension. Most content deferred post-deadline.

## 1. Policy anchor

AVERI's landscape piece ("Frontier AI Auditing-Related Legislation in the US: Landscape, Challenges, and a Path Forward") organizes 22 US audit proposals along roughly six axes: who audits, cadence, scope, information access, publication rules, teeth. No consolidated framework exists; the space is pre-Sarbanes-Oxley in structure.

Real-world anchors for the five sim-relevant senses:

1. **Regulator audit lever** — EU AI Office "Ecosystem Investigations"; FTC Section 6(b) orders; state AG powers. Graduated action between disclosure and sanction.
2. **Third-party capability evaluation** — Epoch, SEAL, LMArena, METR, Apollo. Already the subject of CS1 / CS4.
3. **Self-attested disclosure** — SB 53 Framework publication; SB 53 quarterly CA OES summary. Already the subject of CS2.
4. **Third-party compliance audit** — NY RAISE annual SSP audit (effective 2026); UK AISI pre-deployment evals; AVERI's majority of proposals sit here.
5. **Verification of declared commitments** — Anthropic RSP, OpenAI Preparedness Framework, DeepMind Frontier Safety Framework are *declared* policies; no mechanism currently verifies compliance. AISI and external auditors could fill this role.

## 2. Sim mechanism

### 2.1 The five senses in our primitives

| Sense | Already in sim? | Primitive | Gap |
|---|---|---|---|
| 1. Regulator audit lever | Yes — step 4 of `commitment → advisory → disclosure → audit → sanction` | `Regulator.plan()` action space | Abstract; doesn't model what auditors see or publish |
| 2. Third-party capability eval | Yes — `Evaluator` + benchmark pool | `BenchmarkGroundTruth`, `evaluate_all` | None for this sense |
| 3. Self-attested disclosure | Designed (CS2) | `disclosed_safety_allocation` | CS2 only — no verification layer |
| 4. Third-party compliance audit | **No** | — | Would require new actor or event |
| 5. Declare-then-verify | **No** | — | Would require `declared_safety_commitment` primitive |

### 2.2 Sense 5 — verification audit mechanism

Structure:

1. **Round `t`:** provider declares `d_p ∈ [0, 1]` (committed safety-allocation target). Published.
2. **Rounds `t..t+K`:** provider executes actual `a_p[t..t+K]`. May drift.
3. **Round `t+K`:** verifier observes actual (with noise `σ_v`); penalty applied if `|d_p − mean(a_p[t..t+K])| > τ`.
4. Market share / funder capital respond to **declared** `d_p` (visible immediately); verification creates the consequence.

Game-theoretic payoffs:

- **Asymmetric penalty (only over-promise punished):** pushes everyone toward `d ≈ a + ε` (undershoot); greenwashing dominated, but honest claims diluted by conservatism.
- **Symmetric penalty:** truth-telling equilibrium; `d = a`.
- **Noisy verification (σ_v > 0):** truth-telling equilibrium shrinks; some overpromise rational.
- **Heterogeneous types:** separating equilibrium where high-safety providers declare truthfully (signals type), low-safety pool at moderate overpromise. Spence / Kartik territory.

### 2.3 LOC estimate (Tier 2, heuristic-only)

- `src/actors/model_provider.py` — add `declared_safety_commitment[t]` to private state; heuristic planning logic sets it from rolling actual plus a configurable optimism bias.
- `src/simulation.py` — add `verification_audit_cadence`, `verification_noise_sigma`, `verification_penalty_scale` to `SimulationConfig`; run verification check at cadence; apply penalty to funder allocation + consumer trust.
- `src/actors/funder.py`, `consumer.py` — consume declared commitment when visible.
- `scripts/run_experiment.py` — `verification_off` vs `verification_on` conditions.

~80 LOC. The modeling is tractable; the calibration is not.

## 3. Slotting — three tiers

**Tier 1 — scope note in current paper (~1 paragraph).** Appendix or §5.5 hypothesis table: "CS2 models disclosure of realized allocation, not verification of declared commitments. The latter introduces declaration game-theoretic dynamics (cheap talk + costly verification) orthogonal to the scope-heterogeneity effect tested here." Acknowledge the gap; do not fill it.

**Tier 2 — heuristic-only Appendix H sensitivity.** Implement declare-then-verify, run 30-seed heuristic across `verification_off` / `verification_on` / `verification_high_noise`. Risk: penalty calibration is hand-wavy — what's the absolute magnitude, how noisy is verification, what's the prior over types — and failing to defend these would weaken the current paper's transparency-mandate claim in §5.3.

**Tier 3 — centerpiece of a follow-on paper.** "When AI safety commitments are declared but not verified, what equilibrium do we get?" Ties to RSP/Preparedness anchors; AVERI's 22 proposals give empirical texture; Kartik 2009 / Crawford-Sobel give theoretical backbone. This is the mechanism-rich use of the sim that a policy-focused paper can carry.

**Current recommendation:** Tier 1 in this paper; Tier 3 as its own workstream.

## 4. Open questions (for Tier 3)

- **Penalty magnitude** — calibrate against what? Real-world penalties for RSP/Preparedness non-compliance don't exist yet (none enforced).
- **Verification noise `σ_v`** — what does imperfect audit quality look like? Ties to AVERI's "information access" axis.
- **Asymmetric vs symmetric** — default is asymmetric (over-promise punished). Plausible; symmetric is a robustness check.
- **Declaration cadence** — annual (RAISE), quarterly (SB 53), or per-release? Interacts with K-lag from CS1.
- **Type heterogeneity** — providers differ in genuine safety preference; does the sim's existing `strategy_profile` anchor this enough, or do we need a new `safety_type` primitive?
- **Expose-vs-verify** — does the verifier publicly expose mismatches, or just apply the penalty quietly? Changes reputation feedback loop.

## 5. Tensions with the regulator audit lever (sense 1)

The existing regulator `audit` step in the 5-lever ladder is abstract: it raises scrutiny and applies a small penalty, but doesn't model who audits, what they see, or what they publish. Tier 3 work would need to either:

- **Retrofit sense 1** to become concrete (the regulator's audit step triggers a verification event with information access and publication rules), or
- **Add a separate auditor actor** distinct from the regulator (AISI-style), with its own cadence and scope.

Retrofit is cheaper and preserves the current ladder. Separate actor is richer but adds a fifth LLM-mode actor.

## 6. References

- AVERI — "Frontier AI Auditing-Related Legislation in the US" (https://www.averi.org/ourwork/frontier-ai-auditing-related-legislation-in-the-us-landscape-challenges-and-a-path-forward)
- AISI — "Early lessons from evaluating frontier AI systems"; "Making safeguard evaluations actionable"
- METR — Common Elements of Frontier AI Safety Policies (Nov 2024)
- Anthropic — Responsible Scaling Policy v3.0
- OpenAI — Preparedness Framework v2 (Apr 2025)
- Google DeepMind — Frontier Safety Framework v3 (Sep 2025)
- Anthropic × OpenAI — Alignment Evaluation Exercise (2025)
- NY S6953 RAISE Act — third-party audit clause

Academic:

- Crawford & Sobel (1982). Strategic information transmission.
- Kartik (2009). Strategic communication with lying costs.
- Benabou & Tirole (2006). Incentives and prosocial behavior.
- Dewatripont & Tirole (1999). Advocates. (Adversarial auditing analog.)
- Bolton, Freixas, Shapiro (2012). The Credit Ratings Game. (Cross-sector capture precedent.)
- Spence (1973). Job Market Signaling.
- Casper et al. (2024). Black-Box Access is Insufficient for Rigorous AI Audits.
- Longpre et al. (2024). A Safe Harbor for Independent AI Evaluation.

## 7. Internal pointers

- `src/actors/regulator.py` — current audit lever (sense 1)
- `docs/stakeholders.md` §Regulator — 5-lever ladder reference
- `case_studies/transparency_mandate.md` (CS2) — self-attested disclosure, which this extends
- `case_studies/eval_as_company.md` (CS4) — overlapping capture dynamics
- Session discussions: session 33 (benchmark sponsorship + n_submissions), session 47 (AVERI agent deep-dive, inline in conversation only)
