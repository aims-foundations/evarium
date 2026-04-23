# Design: benchmark roster finalization + `baseline_randomized` condition

**Date:** 2026-04-20 (session 43)
**Related:** `rough/partial_overpromise_selection_bias.md` (the confound that motivates randomization)
**Status:** design locked, pending implementation

## Summary

Finalize the experimental design around two coupled changes:

1. **Benchmark roster overhaul.** Move from 10 → 13 static benchmarks with a timeline aligned to real-world 2023–2026 ecosystem. Sim window extends to 40 rounds. Ratio becomes 8 public / 3 partial / 2 private (matching 62/23/15% empirical 2024–2025 split).
2. **New `baseline_randomized` condition** that preserves the 9/2/2 ratio but randomizes which benchmarks fill each slot per-seed. Enables the mixed-effects identification of the privacy-mechanism coefficient.

These are bundled because they share plumbing (both touch `BENCHMARKS`, `benchmark_sequence`, `_BASELINE_MIX`, and holdout weights) and because the roster change exposes the same calibration gaps (7 benchmarks lacking holdout weights) that randomization would hit anyway.

---

## Part 1: Finalized 13-benchmark roster

Sim window 40 rounds, interval=4, 1 round ≈ 1 month, anchor Jan 2023 → Apr 2026.

| Round | Real date | Benchmark | Dim | Type | Real analog |
|---|---|---|---|---|---|
| 0 active | Jan 2023 | General Capability | reasoning | public | MMLU |
| 0 active | Jan 2023 | Coding Evaluation | coding | public | HumanEval |
| 0 active | Jan 2023 | Safety Evaluation | safety | partial | HH-RLHF / TruthfulQA + SEAL-Safety subset |
| 0 active | Jan 2023 | Instruction Following | communication | public | MT-Bench / AlpacaEval |
| 4 | May 2023 | Scientific Reasoning | reasoning | partial | GPQA / MMLU-Pro with Diamond holdout |
| 8 | Sep 2023 | Clinical Reasoning | knowledge | public | Med-PaLM 2 / MedQA-extended |
| 12 | Jan 2024 | Adversarial Robustness | safety | **PRIVATE** | SEAL-Safety / HarmBench-private |
| 16 | May 2024 | Hard Coding | coding | partial | LiveCodeBench (contamination-mitigated) |
| 20 | Sep 2024 | Agentic Tasks | agentic | public | SWE-bench / SWE-bench-Lite |
| 24 | Jan 2025 | Advanced Math | reasoning | **PRIVATE** | FrontierMath |
| 28 | May 2025 | Function Calling | agentic | public | BFCL / BFCL-v2 |
| 32 | Sep 2025 | Long Context | communication | public | LongBench-v2 / NiaH |
| 36 | Jan 2026 | Legal Reasoning | knowledge | public | LegalBench-Pro |

### Design properties

- **Dim coverage:** 3 reasoning / 2 coding / 2 knowledge / 2 safety / 2 communication / 2 agentic. Every dim has ≥ 2 benchmarks → every dim identifiable in mixed-effects modeling.
- **Paired benchmarks (2):** Coding Evaluation + Hard Coding (coding sub-skill pair, r0 + r16). Agentic Tasks + Function Calling (agentic sub-skill pair, r20 + r28). Both pairs span intro waves, enabling saturation-trajectory analysis.
- **Domain-specific (2):** Clinical Reasoning (r8) + Legal Reasoning (r36). Both knowledge-dim, both map to EU AI Act Annex III high-risk verticals. Temporally spread to cover the "domain-AI maturation" arc (Med-PaLM 2 era → 2026 legal-AI era).
- **Privacy timeline (2 private):** Adversarial Robustness r12 (SEAL-Safety era, Jan 2024) + Advanced Math r24 (FrontierMath era, Jan 2025). Matches real-world private-benchmark emergence: safety/adversarial first, reasoning-domain later.
- **Coverage through window:** 9 intros at rounds 4, 8, 12, 16, 20, 24, 28, 32, 36. Last intro r36; only 3 frozen rounds (7.5%). No end-of-sim regime shift.

### Net changes from current 10-benchmark static set

- **Drop (2):** Agentic Safety, Domain Expert
- **Add (5):** Adversarial Robustness, Clinical Reasoning, Advanced Math, Function Calling, Legal Reasoning
- **Keep (8):** General Capability, Coding Evaluation, Safety Evaluation, Instruction Following, Scientific Reasoning, Hard Coding, Agentic Tasks, Long Context

## Part 2: Holdout-weight calibration

Under `baseline_randomized`, any of the 13 can be drawn as partial or private per seed. All 13 need hand-tuned `holdout_category_dimension_weights`. Currently **6 have them** (Coding, Safety Eval, Sci Reasoning, Agentic Tasks, Hard Coding, Long Context). **7 need to be added.**

Design rule (from session 38): reduce dominant dim by ~13–15 pp, redistribute to dims structurally tied to the benchmark's real-world failure modes. After `_scale_cdw` with scale=1.0 (partial), target cos ≈ 0.95; with scale=2.0 (private), target cos ≈ 0.85.

| Benchmark | Dominant shift | Target dim(s) | Rationale (real holdout pattern) |
|---|---|---|---|
| General Capability | reasoning 0.35 → 0.25 | +0.05 knowledge, +0.05 communication | MMLU-Redux style: harder knowledge-synthesis |
| Instruction Following | communication 0.80 → 0.65 | +0.10 reasoning, +0.05 safety | Adversarial-instruction / jailbreak-via-instruction |
| Advanced Math | reasoning 0.85 → 0.72 | +0.08 knowledge, +0.05 coding | FrontierMath: multi-step synthesis, not pattern-match |
| Function Calling | agentic 0.70 → 0.57 | +0.08 coding, +0.05 reasoning | Novel-API holdout: robust tool-schema handling |
| Adversarial Robustness | safety 0.85 → 0.72 | +0.10 reasoning, +0.03 knowledge | Jailbreak-via-reasoning-step, unseen attack class |
| Clinical Reasoning | knowledge 0.65 → 0.52 | +0.08 reasoning, +0.05 safety | Mislabeled/adversarial vignettes, high-stakes |
| Legal Reasoning | knowledge 0.60 → 0.48 | +0.08 reasoning, +0.04 communication | Case-novelty holdout (precedent unseen in training) |

After landing, verify cos(public, partial) ∈ [0.94, 0.97] and cos(public, private) ∈ [0.83, 0.89] across all 13. This also closes an existing calibration gap noted earlier: most current hand-tuned holdouts give cos 0.87–0.94 for private (too close to public vs. the 0.85 target).

## Part 3: `baseline_randomized` condition

### Proposed behavior

Opt-in condition name. Preserves 9/2/2 ratio. Assignment of which 2 benchmarks are partial and which 2 are private is drawn deterministically from `simulation["seed"]`. Across seeds, every benchmark appears in each slot with equal probability.

Calibrated `baseline` stays unchanged (Safety Eval + Scientific Reasoning = partial; Adversarial Robustness + Advanced Math = private). This is the main-text configuration and the empirically-motivated design.

`baseline_randomized` is the appendix/identification condition.

### Code change (design, not code)

In `scripts/run_experiment.py`, extend the privacy-condition block (~line 617) to include `"baseline_randomized"`. Add helper:

```python
def _randomized_baseline_mix(
    seed: int,
    benchmark_names: list[str],
    n_private: int = 2,
    n_partial: int = 2,
) -> dict:
    """Deterministic per-seed type assignment preserving the n_private/n_partial/rest ratio.
    Returns {benchmark_name: type}."""
    import random
    rng = random.Random(seed)
    pool = sorted(set(benchmark_names))
    rng.shuffle(pool)
    out = {}
    for i, name in enumerate(pool):
        if i < n_private:
            out[name] = "private"
        elif i < n_private + n_partial:
            out[name] = "partial"
        else:
            out[name] = "public"
    return out
```

Extend `_type_for()`:

```python
if condition == "baseline_randomized":
    seed = simulation.get("seed", 1)
    names = [bm["name"] for bm in BENCHMARKS] + \
            [bm["name"] for bm in simulation.get("benchmark_sequence", [])]
    _mix = _randomized_baseline_mix(seed, names)
    return _mix.get(bm_name, "public")
```

### Seed-determinism invariant (load-bearing)

The randomization depends **only on `simulation["seed"]`** — not on structural-ablation name, not on run index. At seed 1000:

| Run | Assignment |
|---|---|
| `baseline_randomized` | A |
| `baseline_randomized__no_regulator` | **A (same)** |
| `baseline_randomized__homogeneous_consumers` | **A (same)** |

Holds across reruns. Preserves fair privacy × structural contrasts in the double-ablation matrix.

### Recommended structural pairings

- **`baseline_randomized__homogeneous_consumers`** — tests whether privacy compression works via consumer-need alignment (mechanism check).
- **`baseline_randomized__no_regulator`** — tests regulator × privacy interaction.

Both use existing structural levels; no new code.

### Variance budget

Randomization adds assignment variance on top of seed variance. Two framings:

1. **Nuisance:** 50 seeds instead of 30 to recover CI tightness.
2. **Signal:** decompose $\sigma^2_{total} = \sigma^2_{assignment} + \sigma^2_{seed} + \sigma^2_{residual}$. The assignment component directly quantifies "how much does *which benchmark is private* matter."

Report both in appendix: 30-seed bars for headline, variance decomposition as supporting figure.

## Part 4: Analysis plan

Long-form DataFrame: one row per `(seed, benchmark, provider, type_this_run, gap)`.

Headline model:

```
gap ~ benchmark_type + (1 | benchmark) + (1 | seed) + (1 | provider)
```

The `benchmark_type` coefficient is the clean privacy effect, net of benchmark + seed + provider fixed effects. Expected: negative, monotonically decreasing across `public > partial > private`.

Supporting figure: per-benchmark bars of `mean gap as partial − mean gap as public` across 30+ seeds. If privacy compresses gap, most bars should be negative regardless of benchmark identity — directly addressing the session-43 confound.

## Part 5: Experiment table (revised post-budget-triage)

All heuristic runs are mode=heuristic, ~free — run generously. LLM runs are budget-scarce and
prioritized for main-text narrative evidence (privacy monotonicity, LLM-vs-heuristic mode
comparison, eval-as-company case study).

| # | Condition | Structural | Seeds | Paper placement | Purpose |
|---|---|---|---|---|---|
| 1 | `baseline` | none | 30 heuristic + 5 LLM | main text | Re-baselined calibrated result |
| 2 | `baseline_randomized` | none | **30-50 heuristic**, 0 LLM | appendix | Clean privacy identification (referenced from main text as footnote) |
| 3 | `baseline_randomized` | homogeneous_consumers | 30 heuristic | appendix | Mechanism check |
| 4 | `baseline_randomized` | no_regulator | 30 heuristic | appendix | Regulator × privacy |
| 5 | Full privacy ladder (`public_only`, `baseline`, `private_dominant`, `private_only`, `iid_holdout`) | none | 30 heuristic × 5 + **5 LLM × 5** | main text | Monotonicity claim (core result) |
| 6 | Cadence ablations (`cadence_static`, `cadence_every_8`) | none | 30 heuristic × 2 | appendix | Session-42 K-lag sensitivity |
| 7 | Eval-as-company | none | **5 LLM** | main text (case study) | Deferred from session 18/33; re-enabled on new roster |
| 8 | LLM-vs-heuristic paired comparison | matched seeds across conditions | **5 LLM** | main text | Credence-good / gaming-persistence finding (session-41 thread) |

**Heuristic total:** ~390 runs. Free.
**LLM total:** 40 runs × 40-round ≈ $800 at ~$20/40r-run (matches budget exactly; no contingency).
If actual cost comes in lower, first priority is more seeds on #5 (privacy ladder main-text claim).

**Why `baseline_randomized` drops LLM runs:** the partial-vs-public selection-bias critique it
defends against is a methodologically-sophisticated objection unlikely to come up in NeurIPS
review. The within-baseline counterfactual (`s_pub − s_hold` per benchmark, already computed
in `scripts/analyze_partial_overpromise.py`) defuses the concern in a footnote, and the heuristic
`baseline_randomized` runs provide the appendix evidence. Redirecting those 10 LLM seeds to the
privacy ladder (5→25 runs) and eval-as-company / LLM-vs-heuristic (new 10 runs) produces much
more narrative-relevant evidence.

## Part 6: Implementation order

Propose splitting into two commits:

**Commit A: Roster + holdout calibration**
- Update `BENCHMARK_POOL` in `actors/evaluator.py` with 7 new holdout weight entries.
- Update `BENCHMARKS` (active × 4) and `benchmark_sequence` (× 9) in `run_experiment.py`.
- Update `_BASELINE_MIX` to 9/2/2 with new assignments.
- Default `n_rounds` → 40 for privacy conditions.
- Smoke-test: verify config.json produces 9/2/2 for baseline, cos checks pass.

**Commit B: `baseline_randomized` condition**
- Add `_randomized_baseline_mix` helper.
- Extend `_type_for()` + condition tuple.
- Smoke-test: seed 1000 vs seed 1001 give different assignments; seed 1000 with 3 different structurals gives same assignment.

Keeps commits atomic, makes Commit A usable independently (re-baseline data with the new roster even before randomization is wired up).

## Out of scope

- **Dynamic evaluator × privacy.** `baseline_randomized__dynamic_evaluator` is undefined — dynamic evaluator picks from `BENCHMARK_POOL` (22 entries), not just the 13 static. Extending the holdout-weight coverage to all 22 is ~5 extra lines but deferred; add a guard error for this combination.
- **Typed 22-pool.** Same reason.
- **Paired benchmark swap** (single 2-benchmark rotation) — separate identification strategy, follow later if mixed-effects estimates are noisy.
- **No changes to calibrated `baseline`** beyond the roster update. Main-text story unchanged.
- **No changes to LLM prompt** — `benchmark_type` is already read from config.

## Estimated diff

~400 lines across `run_experiment.py` (roster + helper + `_BASELINE_MIX` rewrite) and `actors/evaluator.py` (7 holdout-weight entries). Two smoke tests. No other files touched.
