# Experiment Plan

**Last updated:** 2026-04-24 (session 51: concrete launch plan added for remaining $400 budget; current state reflects post-overnight run inventory)

This doc lists the specific runs the paper needs and their current status. It is anchored to the case-studies bank (`docs/case_studies/README.md`) rather than to phase-numbered abstractions. The prior `EXPERIMENT_PLAN.md` (Qwen / 30-round / 15×3 structure) has been retired to `archive/EXPERIMENT_PLAN_phase-structure.md`.

## Current state (post-session 51)

**Spent to date:** ~$300 across 37 runs. **Remaining budget:** ~$400.

Completed overnight runs (`sandbox/experiments/`):

| Batch | Conditions | Seeds present | Runs |
|---|---|---|---|
| `_core_privacy` Sonnet | public_only / baseline / private_dominant / private_only / iid_holdout | s42–s45 (non-baseline); s42–s46 (baseline) | 21 |
| `_core_privacy` Opus | baseline s42–s43; private_dominant/private_only/iid_holdout/public_only s42 | — | 6 |
| `_core_evalcompany` Sonnet | eval_as_company | s42, s43 | 2 |
| `_tier2_ablations` Sonnet | 7 ablations (no_funders/no_regulator/no_incidents/no_media/no_opensource/initial_uniform_capability/homogeneous_consumers) | s42 only | 7 |
| `_ev1_smoke` Sonnet | ev1_deepseek_shock | s42 only | 1 |
| **Total** | | | **37** |

**Still missing to complete the planned Tier 1 privacy ladder at N=6 (Sonnet):** public_only s46+s47, baseline s47, private_dominant s46+s47, private_only s46+s47, iid_holdout s46+s47 = **9 runs**.

## Session 51+ launch plan — $400 budget, five batches

Five targeted batches in priority order. All assume Sonnet 4.6 unless noted. Batches 2+ are **gated on committing session-48-through-51 sim+paper changes first** (see "Blocking dependencies" below).

### Batch 1 — Fill privacy ladder to N=6 (9 runs, $90–135)
Parallelizable with nothing else pending. Upgrades §5.2 headline claim from N=4–5 to N=6 clean.

| Condition | New seeds |
|---|---|
| public_only | s46, s47 |
| baseline | s47 |
| private_dominant | s46, s47 |
| private_only | s46, s47 |
| iid_holdout | s46, s47 |

**Decision gate:** after Batch 1 completes, re-run `scripts/plots/per_benchmark_core_privacy.py` and verify the 9/11 cross-mode sign-agreement claim still holds, monotone HHI compression still holds ($0.46 \rightarrow 0.34$ at N=6), and no single new seed produces an outlier run that flips a sign. If any of those fail, investigate before continuing.

### Batch 2 — E2a EV1 DeepSeek multi-seed (6 runs, $60–90)
One condition, seeds 42–47. Promotes exogenous-shock face validity from smoke-only (currently `_ev1_smoke` at s42) to a multi-seed claim. Paired controls: matched `baseline_s4X_sonnet` already present in `_core_privacy`.

**Decision gate:** verify shock propagates through actor reasoning in ≥ 5/6 seeds (verbatim narrative citation in provider or funder traces, plus R&D rebalance +3–9pp within 3 rounds on matched controls). If ≤ 4/6, defer Batch 3 until the shock plumbing is debugged.

### Batch 3 — E2b EV2 EU AI Act staged (6 runs, $60–90)
One condition (staged regulatory escalation at R20/R26/R32), seeds 42–47. Different shock archetype than EV1 — tests whether provider response to *regulator* shocks differs from provider response to *competitor* shocks. Doubles the face-validity evidence base.

**Decision gate:** confirm staged-shock rounds propagate into regulator reasoning AND provider portfolio reallocation (not just one). If only one layer responds, note as limitation in App E Internal-Subjective.

### Batch 4 — Tier 2 ablation s43 replicates (7 runs, $70–105)
All 7 ablations at seed 43 only (s42 already run). Upgrades App F ablation-sweep from N=1 to N=2 directional; specifically tests whether the Mirage-wins-under-`initial_uniform_capability` finding (seed-42-only, currently flagged as "mode-dependent") replicates or is s42-specific.

**Decision gate:** if `initial_uniform_capability` s43 shows OpenCore winning (matching heuristic-layer prediction) or a third provider, the App H narrative needs a seed-sensitivity caveat. If s43 also produces Mirage, the mode-dependent finding is more defensible.

### Batch 5 — CS2 transparency mandate 1-seed smoke (1 run + dev, $10–15 + ~60 LOC dev)
Only if the transparency-mandate lever is implemented (~60 LOC in `src/actors/regulator.py` per case-study bank). Single-seed smoke (s42) to verify the disclose-vs-window-dress mechanism shows up at all in LLM reasoning. Does **not** let the paper make a CS2 claim — but lets §5.4 case-studies table caption promote CS2 from "future work" to "preliminary implementation, smoke only".

**Decision gate:** if smoke shows provider reasoning explicitly engages the disclosure tradeoff, CS2 becomes a viable post-deadline followup. If providers ignore the lever, defer CS2 indefinitely.

### Batch totals

| Batch | Runs | Cost (midpoint) | Wall-clock @ 4-parallel |
|---|---|---|---|
| 1 Privacy ladder fill | 9 | $110 | ~2h |
| 2 E2a EV1 multi-seed | 6 | $75 | ~1.5h |
| 3 E2b EV2 multi-seed | 6 | $75 | ~1.5h |
| 4 Tier 2 s43 replicates | 7 | $85 | ~2h |
| 5 CS2 smoke (optional) | 1 | $12 | ~30m |
| **Total (all 5)** | **29** | **~$357** | **~7h + dev for B5** |

Fits $400 budget with ~$40 headroom for re-runs if any batch has a failure that requires a retry.

## What we're explicitly NOT buying with this budget

- **More Opus runs.** Existing 6 paired Opus points at s42 + baseline s43 is a defensible robustness story. Cost-per-additional-claim is poor at this margin.
- **E8 eval_as_company scale-up.** Existing N=2 "mode-dependent finding" (ΔHHI = −0.029 LLM vs +0.041 heuristic, Apex share via throughput not safety) is a cleaner paper claim than a noisier N=6.
- **Longer horizons (>40 rounds).** Calibrated cadence choice; extending doesn't strengthen a claim.
- **Homogeneous-consumers × privacy-ladder interaction.** Interesting robustness check but lower marginal value than the 5 batches above.

---

## Context

- Session-49d identity redesign + A1 benchmark-type context landed; all prior LLM runs (sessions 28/29/32/41/49a/c) are pre-49d and not directly comparable on reasoning content or identity behavior.
- Heuristic re-baseline at N=30 × 9 conditions already complete (`sandbox/experiments/heuristic_session49/`).
- Post-49d 2-seed evidence validates identity rewrite + reveals Orion-rebuild-despite-regulation as seed-robust pattern.
- Late session-49d sim tweaks applied: media `_media_sample_size` 4→6 + new milestone-crossing + rival-closes-gap headline triggers; incident exposure-multiplier floor 0.5→0.3 (reduces small-provider over-tax). All Tier 1+ runs will exercise these; pre-change runs in `_llm_apr23_v1` remain valid as reference.
- Dynamic evaluator calibration complete at seed=101; decided as single-seed Appendix artifact (see E4).
- All prompt + identity + media + incident changes uncommitted as of this doc's timestamp.

## Anchoring

Each run serves a paper claim. Paper claims are organized around the case-studies bank:

| Case study | Status | Paper location | Tier |
|---|---|---|---|
| CS1 — Privacy ladder | Live | §5.2 | T1 |
| CS2 — Transparency mandate | Designed (~60 LOC) | §5.3 | T3 |
| CS3 — Media shadow | Designed (~50 LOC) | §5.4 | T3 |
| CS4 — Eval-as-company | Demoted | App H | T3 |
| CS5 — Benchmark sponsorship | Brainstorm | — | post-deadline |
| CS6 — Audit & verification | Brainstorm | — | post-deadline |
| CS7 — EU vs US regulation | Archival | App archival | done |

Exogenous event validation (`docs/exogenous_event_validation.md`) is Tier 1 — external-validity check ahead of internal ablations.

## Tier 1 (MVP core) — 36 LLM runs

### E1 — LLM privacy ladder (5 conditions × 6 seeds each)

**Conditions:** `public_only`, `baseline`, `private_dominant`, `private_only`, `iid_holdout`.
**Seeds:** 42-47.
**Runs:** 30.
**Purpose:** CS1 §5.2 primary claim — adversarial privacy compresses |score − satisfaction gap| monotonically; `iid_holdout` isolates weight-distance channel from noise+lag.
**Cross-reference:** heuristic N=30 × 9 conditions already at `heuristic_session49/`.

### E2 — LLM exogenous event validation

**Prereq:** `recent_exogenous_events` prompt-field plumbing (~10-20 LOC) in `src/actors/{model_provider,regulator,funder}.py`.

- **E2-smoke — 1-seed EV1 DeepSeek R25 shock**. Seed 42. Purpose: verify shock mechanism propagates before committing to 6 seeds. Gate: if EV1 shock is not visible in actor reasoning at N=1, de-scope E2a/E2b until plumbing is fixed.
- **E2a — EV1 DeepSeek R25 (post-smoke)**. Seeds 42-47. Paired controls: E1 `baseline` at matched seeds.
- **E2b — EV2 EU AI Act staged R20/R26/R32**. Seeds 42-47. Paired controls: E1 `baseline` at matched seeds. Gate: only after EV1 harness validates.

**Runs:** 1 + 6 + 6 = 13 (1 smoke counts toward the 13; if smoke fails, stop at 1).

### Tier 1 gate decision

After E1 + E2 complete, verify post-49d findings replicate across seeds 42-47:
- Apex archetype drift resolution (incident-window sustains, late-run partial regression)
- OpenCore-as-safety-leader pattern
- VC-VC r < 0.5
- Orion-rebuild-despite-regulation pattern
- Regulator plumbing ≥ 13/14 targeted
- Privacy-ladder monotonic compression
- Exogenous shocks propagate through actor reasoning

If all directional findings replicate → launch Tier 2. If multiple fail → root-cause before continuing.

## Tier 2 (strengthening) — 14 LLM runs

### E3 — Ablation sweep (7 conditions × 2 seeds each)

Seeds 42-43. Purpose: mechanism decomposition appendix + post-49d surprise investigations.

| Ablation | Addresses |
|---|---|
| `no_funders` | Funder-mechanism contribution |
| `no_regulator` | Regulator-intervention contribution |
| `no_incidents` | Incident-stream contribution |
| `no_media` | Media-channel contribution |
| `initial_uniform_capability` | Post-49d finding: OpenCore dominance under uniform capability |
| `no_opensource` | Post-49d finding: OpenCore-as-archetype ecosystem-diversity role |
| `homogeneous_consumers` | Privacy-ladder robustness + `matched_satisfaction` decomposition concern (see `future_work_per_benchmark_gap_decomposition.md`) |

**Runs:** 14.

### E4 — Dynamic evaluator (decided: single-seed artifact only)

Single-seed calibration run complete (`dynamic_evaluator_40r_s101`, seed=101, 40 rounds). Note: seed=101 predates the seeds 42-47 lock-in; retained as-is for the Appendix artifact since re-running at a seed-range-42-47 value would not change the single-seed claim. Evaluator LLM produced coherent reasoning with memory use + self-correction (R20 retirement of R13-introduced Agentic Tasks) + leaderboard-adoption correlation tracking for decision gating. Suite evolved 4→6 benchmarks with sensible domain coverage. Reasoning traces are paper-worthy as illustrative Appendix content.

**Decision:** retain as single-seed Appendix artifact (reasoning trace + curriculum evolution); skip multi-seed. Rationale: action space (create/retire/none × pool selection) is constrained enough that a well-designed fixed sequence could plausibly match the suite evolution; multi-seed confirms replicability of reasoning but doesn't demonstrate LLM > fixed_sequence on outcome metrics. Proper paper claim would require a 3-mode comparison (LLM dynamic vs randomized_pool vs fixed_sequence at matched seeds) — out of scope this deadline.

**Runs:** 0 additional. Seed 101 run stays in `_llm_apr23_v1/llm/dynamic_evaluator_40r_s101/`.

## Tier 3 (deepening — after Tier 1 complete) — 24 LLM runs + dev

| Experiment | Runs | Model | Purpose |
|---|---|---|---|
| CS3 media shadow (after ~50 LOC) × 6 seeds | 6 | Sonnet | §5.4 |
| CS2 transparency mandate (after ~60 LOC) × 6 seeds | 6 | Sonnet | §5.3 |
| E8 eval_as_company × 6 seeds | 6 | Sonnet | App H CS4 |
| E9 Opus baseline paired (robustness) × 6 seeds | 6 | **Opus 4.6** | Robustness appendix — paired t-test vs E1 `baseline` at matched seeds 42-47 |

**Runs:** 24. Sonnet: 18, Opus: 6.

### Tier 3 gating

Ordered by paper-claim value when deadline known. Typical order:
1. CS3 media shadow (§5.4 enablement)
2. CS2 transparency mandate (§5.3 enablement)
3. E8 eval_as_company (App H retune validation)
4. E9 Opus paired robustness (robustness appendix)

## Post-deadline (tracked in `MEMORY.md` future-work)

- CS5 benchmark sponsorship (brainstorm)
- CS6 audit & verification (brainstorm)
- Organizational consumer audit (gated on `consumer_llm_organizations=True` + media-effects fix)
- Per-benchmark gap decomposition investigation (`future_work_per_benchmark_gap_decomposition.md`)
- Distribution-advantage mechanism (`future_work_distribution_advantage_limitation.md`)
- Multi-vendor robustness (GPT-4/5, Gemini, Llama) beyond Claude family
- Provider profile redesign (`future_work_provider_profile_redesign.md`)
- Identity mutation / D1 drift metric
- Positive-side media channel
- Cost dynamics

## Grand totals

| Layer | Sonnet runs | Opus runs | Cost estimate | Wall-clock |
|---|---|---|---|---|
| Tier 1 | 43 | 0 | $320-650 | ~14-18h |
| Tier 2 | 14 | 0 | $100-200 | ~5h |
| Tier 3 | 18 | 6 | $300-660 | ~12h + 2-3 days dev |
| **Total** | **75** | **6** | **~$720-1,510** | **~32h + dev** |

E4 dynamic_evaluator run at seed=101 already complete (single-seed Appendix artifact; not counted in totals). 3-4 parallel streams → ~10-15h wall-clock total for all LLM runs.

## Seed discipline

- **Seeds 42-47:** all Tier 1 and Tier 3 runs (N=6; enables paired tests across conditions + model families)
- **Seeds 42-43:** Tier 2 ablations (N=2 directional)
- **Seeds 1, 2, 101:** earlier post-49d evidence runs (101 is the retained dynamic-evaluator single-seed artifact); NOT used for Tier 1+ to avoid selection contamination
- Seeds were selected deterministically before running — resistant to cherry-picking accusations.

## Decision gates

| Gate | Decision |
|---|---|
| After E1 | Does privacy-ladder monotonic compression replicate? If no, investigate; if yes, launch Tier 2. |
| After E2-smoke | Does EV1 shock propagate through actor reasoning? If no, defer E2a/E2b until plumbing fix; if yes, scale to 6 seeds. |
| After dynamic_evaluator seed=101 | Is evaluator agency paper-worthy? If yes, add to Tier 2 (+3 seeds); if no, defer post-deadline. |
| After Tier 1 complete | Deadline-aware Tier 3 ordering. If deadline tight, drop CS2 or E9 Opus. |

## Blocking dependencies

### Resolved
1. **Session 48-49 commits** — still pending as of session 51; required before Batches 2+ launch.
2. **`recent_exogenous_events` plumbing** — ✓ landed; `_ev1_smoke` validates the mechanism at s42.

### Open
1. **Commit session-48 through session-51 work** (sim + paper) — blocks Batch 2 onward.
2. **CS2 lever implementation (~60 LOC)** — blocks Batch 5 only; optional for this cycle.

## Storage policy

- Heuristic runs: keep `rounds.jsonl` + `config.json` + `metadata.json` + `summary.json` per seed; aggregate CSVs at `output/heuristic_analysis/`.
- LLM runs: retain full per-seed directories including `providers/`, `funders/`, `regulators/`, `consumers/` memories for reasoning-trace analysis; small N makes this affordable.
- Delete plots/game_log.md on replication runs once aggregation CSV rows are written.

## What "done" looks like for the paper

For the NeurIPS paper (target 10pp):
- CS1 privacy ladder: heuristic ✓, LLM pending → §5.2 + App H
- CS4 eval-as-company: retune heuristic pending, LLM Tier 3 → App H demoted
- CS2/CS3 post-implementation → §5.3 + §5.4 (Tier 3 — risk if deadline tight)
- §5 figures refresh after LLM Tier 1 completes
- Appendix F stubs resolved or pruned
- Appendix A TODOs resolved (benchmark-pool 22 rows, switching description, evaluator modes subsection)
- Main-body trim 14.5pp → 10pp (Related Work + Simulation)
- Appendix I prompts doc landed (session 49e)
- Robustness appendix via E9 Opus paired test

## Claim → evidence map

| Paper claim | Evidence |
|---|---|
| Privacy ladder compresses benchmark gaming | E1 (+ heuristic N=30) |
| Safety archetype persistence is share-pressure-dependent | E1 `baseline` post-49d vs seed=1/2 reference |
| VC herding emerges from identity language, not just visibility | Session-49c (vcfix) + E1 cross-seed |
| Regulatory targeting works mechanically but doesn't persistently suppress dominance | E1 `baseline` (Orion rebuild) + E3 `no_regulator` |
| eval_as_company retune favors safety-investing providers | E8 + heuristic N=30 |
| Capability-vector asymmetry is load-bearing for market structure | E3 `initial_uniform_capability` |
| OpenCore-as-safety-leader requires open-source archetype | E3 `no_opensource` |
| Exogenous shocks propagate through actor reasoning | E2a/E2b |
| Results replicate across Claude model families | E9 Opus paired |

## What this plan does NOT establish

- Multi-vendor robustness beyond Claude family (future work)
- Long-horizon (>40 round) dynamics — out of scope
- Market share realism for platform-distributed providers (`future_work_distribution_advantage_limitation.md`)
- External validity beyond "archetype practitioners recognize their role" (interview study separate track)

## References

- `docs/case_studies/README.md` — canonical case-study bank
- `docs/stakeholders.md` — architecture reference (Session Changelog tracks breaking changes)
- `docs/funder_calibration.md` — session-49 funder recalibration provenance
- `docs/llm_actor_prompt_audit_playbook.md` — seven-pass prompt audit procedure
- `docs/exogenous_event_validation.md` — EV1/EV2 design
- `SESSION_HANDOFF.md` — current session state
- `archive/EXPERIMENT_PLAN_phase-structure.md` — retired phase-based plan for reference
- `future_work_per_benchmark_gap_decomposition.md`, `future_work_distribution_advantage_limitation.md` — methodological concerns flagged but deferred
