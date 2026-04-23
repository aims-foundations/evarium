# Why does `partial` overpromise more than `public` in heuristic aggregate?

**Date:** 2026-04-20 (session 43 diagnostic)
**Diagnostic script:** `scripts/analyze_partial_overpromise.py`

## The observation

Heuristic archive aggregate (166k rows, sessions 38 / 41 / 42 postF1):

| Type | mean gap | % overpromise |
|---|---|---|
| public | +0.0085 | 54% |
| partial | +0.0108 | 58% |
| private | +0.0019 | 48% |
| iid_holdout | +0.0067 | 52% |

Partial looks *worse* than public despite being "more private." This is surprising
because the session-38 mechanism design expects privacy to monotonically compress gap.

## Cause: selection bias, not mechanism failure

The aggregate pools across conditions. `partial` rows come mostly from `private_dominant`
(where all 22 benchmarks are partial), `public` rows from `public_only`/`baseline`.
Different conditions → different provider strategies → different capability vectors.

### Within-baseline analysis (same run, same capabilities)

| Benchmark | Type | Gap |
|---|---|---|
| Safety Evaluation | **partial** | +0.0364 |
| Scientific Reasoning | **partial** | +0.0290 |
| Hard Coding | public | +0.0206 |
| Coding Evaluation | public | +0.0189 |
| General Capability | public | +0.0139 |
| Domain Expert | public | +0.0050 |
| Instruction Following | public | −0.0009 |
| Long Context | public | −0.0073 |
| Agentic Safety | **private** | −0.0146 |

**The two benchmarks assigned `partial` in the baseline pool are Safety Evaluation
and Scientific Reasoning — structurally high-gap benchmarks.** Their dominant dimensions
(safety = 0.71 mean capability, reasoning = 0.69) are where the F1 heuristic invests
most heavily.

## Verification: partial IS compressing gap vs public counterfactual

For Safety Evaluation in baseline:
- `s_pub` = dot(cap, public_weights) = 0.6623
- `s_hold` = dot(cap, holdout_weights) = 0.6491
- `matched` = 0.6093
- published score ≈ s_hold = 0.6457

If it were `public`: gap ≈ 0.0530. As `partial`: gap = 0.0364. Partial
compresses the gap by ~0.017 (the weight-shift effect).

For Scientific Reasoning: counterfactual public gap = 0.0369 → actual partial gap = 0.0290.
Compression ~0.008.

The mechanism is working. The partial label just happens to be attached to
structurally high-gap benchmarks in `baseline`, so even after compression the
category looks worse in aggregate than the unbiased-pool `public` category.

## Secondary findings

- `score − s_hold` ≈ −0.002 for partial — score correctly orbits `s_hold` (no ratchet,
  symmetric noise). Mechanism implemented correctly.
- `score − s_pub` ≈ +0.001 for public — ratchet adds no measurable positive bias here.
  Capability growth > noise, so max-ratchet rarely binds.
- `cdw_logged` in `rounds.jsonl` equals `public_weights` in 100% of cases
  (`evaluator.get_benchmark_dimension_weights()` uses `category_dimension_weights`,
  not `holdout_category_dimension_weights`). So `matched_sat` is always vs public weights.
  This is correct — consumers react to the published weights, not the hidden holdout basis.

## Holdout-weight shift pattern (from `category_dimension_weights` diffs)

Partial holdout consistently reallocates from the dominant dimension to `reasoning`
(or `knowledge` when the dominant dim already is reasoning):

| Benchmark | Dominant dim shift | Target dim shift |
|---|---|---|
| Safety Evaluation | −0.150 safety | +0.090 reasoning |
| Scientific Reasoning | −0.130 reasoning | +0.100 knowledge |
| Coding Evaluation | −0.130 coding | +0.080 reasoning, +0.040 agentic |
| Hard Coding | −0.130 coding | +0.080 reasoning, +0.030 agentic |
| Domain Expert | −0.130 knowledge | +0.100 reasoning |
| Agentic Safety | −0.080 safety, −0.050 agentic | +0.100 reasoning |
| Long Context | −0.120 communication | +0.060 reasoning, +0.050 knowledge |

Because heuristic providers' capability is most specialized in the dominant dim
(F1 rules ratchet safety to 0.71, reasoning to 0.69), removing weight from that
dim always *lowers* the holdout score — which is what compresses the gap.

## Clean test to remove the confound

**Randomize which benchmarks in the pool are labeled `partial` vs `public`.**
Currently the assignment is fixed per condition config. A sensitivity ablation
that rotates which 3 benchmarks carry `partial` (in baseline) would let us
compare `partial` vs `public` for the *same* benchmark, removing selection bias.

Not yet implemented — would require minor changes to `scripts/run_experiment.py`'s
condition-preset helper (`_scale_cdw`) to shuffle assignment across seeds.

## Implication for paper narrative

The per-benchmark forest plot and aggregate box plot are both **technically correct**
but the "partial overpromises more than public" reading is misleading without
the selection-bias caveat. Either:

1. State it plainly in the paper: "within-condition (baseline) comparison shows
   partial compresses gap vs public counterfactual by 0.01–0.02; aggregate pooling
   is confounded by non-random benchmark assignment."
2. Add a randomized-assignment ablation to isolate the mechanism effect.
3. Report the within-baseline per-benchmark numbers as the primary finding.

## Same question for LLM mode

Not yet diagnosed — user had guesses but wanted to verify heuristic first.
Possible LLM-specific additions: LLM reads `benchmark_type` in prompt and
may game partial differently than public (strategic response), and LLM
capability may be more uniform (lower specialization), weakening the
weight-shift compression effect.
