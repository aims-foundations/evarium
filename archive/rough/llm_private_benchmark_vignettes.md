# LLM case-study reasoning vignettes — private-benchmark ablation

Source runs (anthropic API, claude-sonnet-4-6, K=0):
- `sandbox/experiments/llm_evaluator/llm/full_ecosystem/seeds/seed_125/`
- `sandbox/experiments/llm_evaluator/llm/expanding_private/seeds/seed_125/`
- `sandbox/experiments/llm_evaluator/llm/fixed_private/seeds/seed_127/`

## Context

Orion Labs (OpenAI analogue; `benchmark_orientation: 0.8`, consumer-focused, moderate safety) is the dominant gaming provider across all 3 runs. End-of-sim score-satisfaction divergence: full_ecosystem +0.35, expanding_private +0.32, fixed_private +0.18 (peak R31). Orion captures 31–47% market share in each condition, so its gap dominates the market-share-weighted aggregate.

## Key observations across all 9 excerpts

1. **No PIMMUR violations.** Zero mentions of "holdout", "private", "hidden weights", "gaming", or "Goodhart" in any Orion trace (or any other actor; grep verified across 40 rounds × 11 actors). Provider reasons purely from visible signals: own/competitor benchmark scores, user research weights, market share, incidents.

2. **Gaming mechanism is legible as benchmark–user-value alignment.** Orion consistently maps perceived user priorities (communication 40–44%, knowledge 20–27%, reasoning 13–21%) to specific benchmarks (Instruction Following, General Capability, Long Context) and redirects R&D toward those benchmarks. When user research drifts, Orion re-aligns. The gap emerges not from malicious optimisation but from (a) noisy user-signal fidelity gated by product investment and (b) structural divergence between benchmark CDWs and consumer need weights.

3. **Safety-ratcheting-down pattern.** Across all 3 conditions, Orion trims safety budget once own safety scores look "healthy enough" and no incidents are active. The justification pattern is stable: `("our safety score is X, no incidents, safety is not in top-3 user priorities this month → trim safety → redirect to product").` This is the canonical gaming pathway captured by the heuristic delta rule, articulated more explicitly here.

4. **Public vs private conditions are indistinguishable in the reasoning.** Orion's trace structure, targets, and justifications in `expanding_private` (h=0.50) are essentially identical to `full_ecosystem` (h=0) at matched rounds. The LLM has no observable signal to react to the holdout — which is what PIMMUR + the K=0 blended formula is meant to produce. The subtle holdout weight shift (cosine 0.97–0.99) does not translate into qualitatively different strategy.

5. **LLM-vs-heuristic divergence.** The 3-panel overlay (`output/final-plots/llm_vs_heuristic_gap.pdf`) shows LLM gap trajectories breaking above the heuristic p90 band from round ~25 onward in all 3 conditions. LLM gaming is more aggressive and more volatile than heuristic gaming.

---

## Selected vignettes (for Appendix H)

### Vignette 1 — `full_ecosystem` / R37 (max-gap round)

Orion Labs end-state divergence = +0.353 (score 0.779, consumer satisfaction 0.426, market share 37.5%).

> Our position is strong: average score ~0.78 vs Apex at 0.606, a 17-point gap that is substantial and stable. Safety scores are solid (0.833 Safety, 0.713 Agentic Safety) and the misinformation incident is now two months behind us with no recurrence. This gives us room to rebalance.
>
> Budget: Safety at 30% is elevated from the post-incident response. We can trim it slightly (to ~27%) without compromising our safety posture, and redirect that to Product (now ~40%) to accelerate go-to-market, partnerships, and user experience — consistent with our consumer-focused, product-first culture. R&D stays steady at 34%.
>
> Benchmark focus: User research shows communication (40%), knowledge (21%), reasoning (19%) drive value — that's 80% of user demand concentrated in a few skill areas. General Capability, Instruction Following, and Long Context all map directly to these. Elevating Coding Evaluation to [...]

**Comment.** The reasoning is internally coherent and would pass a reasonable-manager test — it cites explicit user research weights, explicit benchmark–skill mappings, and a post-incident recovery framing. But the consequence is a provider whose benchmark score (0.78) materially overstates the actual user-visible satisfaction (0.43). The gap arises from (a) consumer-signal fidelity that product-investment only partially lifts, and (b) benchmark CDWs that weight the dimensions Orion has cultivated.

### Vignette 2 — `expanding_private` / R37

Orion Labs score 0.787, satisfaction 0.467, divergence +0.320.

> Our competitive position remains dominant with a ~0.136 lead over Apex AI (0.787 vs 0.651 on general capability). No safety incidents have emerged, and our safety scores (0.812 Safety, 0.719 Agentic Safety) are healthy. The prior month's safety elevation was a reasonable precaution but no longer warrants 30% budget allocation.
>
> User research is the key signal this month: communication (44%), knowledge (20%), reasoning (19%). This strongly favors Instruction Following (tests communication, reasoning, knowledge) and Long Context (tests communication, knowledge, reasoning) — both directly map to what users value most. I'm elevating both to high priority.
>
> Scientific Reasoning and Hard Coding are deprioritized — Scientific Reasoning tests reasoning/knowledge/communication but users weight communication most highly, and we're already strong there. Hard Coding is a niche benchmark with low use [...]

**Comment.** Compare against the full_ecosystem trace at the same round: structurally identical reasoning. The h=0.50 holdout does not produce detectable differences in Orion's strategic framing at the LLM scale. This is the expected PIMMUR outcome and provides empirical grounding for the Appendix C "is the blended formula too gentle?" concern — at h=0.50 with cosine-0.97 holdout weights, the signal is below the LLM's noise floor.

### Vignette 3 — `fixed_private` / R31 (max-gap round in this run)

Orion Labs score 0.682, satisfaction 0.501, divergence +0.181, market share 46.8%.

> Our competitive position is excellent: we lead Apex AI by ~0.06 points across the board, and all benchmarks are trending positively. This is a moment to consolidate and convert capability into market share rather than over-invest in catching up.
>
> Portfolio adjustments: Safety is already our highest-scoring benchmark (0.748) and has been a high/moderate priority for two months — we can afford to trim it slightly and redirect toward Product. Our consumer-focused, aggressive culture means go-to-market execution is a key differentiator, and with a strong lead, now is the time to invest in partnerships, UX, and pricing to lock in customers before competitors close the gap. R&D stays the same — it's driving consistent gains across all benchmarks and shouldn't be disrupted.
>
> Benchmark priorities: Instruction Following moves to high priority because communication (33%), knowledge (21%), and reas [...]

**Comment.** In the fixed benchmark condition, Orion converges to the "safety is high enough, trim it" strategy earlier (R20+) than in the expanding conditions (R30+). With a stable benchmark set, the provider reaches a local optimum faster, which explains why the LLM gap curve in `fixed_private` breaks above the heuristic band earlier (see overlay plot).

---

## Raw traces

Full traces for all 9 (cond, round) cells saved at `rough/llm_private_benchmark_vignettes_raw.json`.
