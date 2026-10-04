# Evaluator Information Design: The Privacy Ladder

## 1. Policy anchor

Three real-world patterns for how evaluators reveal benchmark information:

- **Fully public** — MMLU, HumanEval, GPQA publish items, labels, and scoring logic. Providers can train on anything resembling the distribution.
- **Partially private (SEAL-style)** — Scale's SEAL benchmarks keep items private but leak through metadata and item-family patterns. Contamination estimates: 8–16 percentage-point inflation (Singh 2024, Dominguez-Olmedo 2024).
- **Adversarial private (FrontierMath-T4)** — Epoch's Tier-4 holdout never touches public infrastructure. Within-family Pearson to public items ≈ 0.85 (Epoch Hub).

No single law mandates any of these; they emerge as evaluator design choices. The policy question is: what information structure should evaluators adopt, given that provider behavior responds to each differently?

## 2. Simulation mechanism

Three orthogonal information-design channels, implemented in `src/actors/evaluator.py` and `src/visibility.py`:

1. **Weight distance (`cosine`)** — holdout weights differ from public weights. Closer cosine = more exploitable via score-targeting. A composite proxy for contamination, train-on-test-task, and adversarial construction.
2. **Reporting lag (`K`)** — holdout score published every K rounds, else frozen; stale signal delays feedback. Default K=3, calibrated to real-world benchmark release cadence.
3. **Noise scaling (`h`)** — holdout score computed on `samples × h` items; σ/√(samples·h) noise floor.

Four benchmark types:

| Type | `h` | `cosine` | Real-world analog |
|---|---|---|---|
| `public` | 0 | — | MMLU, HumanEval, GPQA |
| `partial` | 0.3 | 0.95 | SEAL with leakage |
| `private` | 1.0 | 0.85 | FrontierMath-T4 |
| `iid_holdout` | 1.0 | 1.00 | Ablation only — isolates noise+lag from weight distance |

Five ablation conditions assign types uniformly across the 13-benchmark roster:

| Condition | Assignment | Role |
|---|---|---|
| `public_only` | all public | pre-private-era baseline |
| `baseline` | 8 public / 3 partial / 2 private | matches 2024–2025 reality |
| `private_dominant` | all partial | SEAL-dominant future |
| `private_only` | all private | FrontierMath-dominant future |
| `iid_holdout` | all iid_holdout | channels 2+3 without channel 1 |

Belief primitive: `σ_prior = 0.05`. Providers know benchmark framing but not exact dimension weights; initial belief = `normalize(clip_nonneg(public_weights + Normal(0, σ_prior)))`.

## 3. Findings

Adversarial privacy (high `h`, low `cosine`) reduces the |score–satisfaction gap| monotonically across the ladder. The `iid_holdout` ablation pushes the gap more negative than `public_only`, revealing that channels 2+3 alone produce **cleaner measurement that undershoots gaming-inflated public scores** — the weight-distance channel (cosine) is what creates the selection bias in the first place. The mechanism is legible at the per-benchmark level: 8 of 10 benchmarks show the expected direction.

## 4. Open questions

- **σ_prior calibration** — current 0.05 is preliminary; longer sweeps needed to verify convergence on private benchmarks.
- **Asynchronous release** — current implementation locks synchronized K=3; gap-level jitter and Bernoulli release variants are sensitivity ablations not yet run.
- **Premium access** — `premium_pre_access` axis (orthogonal to privacy) reserved for evaluator-capture and benchmark-sponsorship extensions.

## 5. References

- Singh, Nan, Wang (2025). "The Leaderboard Illusion." arXiv:2504.20879.
- Dominguez-Olmedo et al. (2024). Contamination magnitude in LLM benchmarks.
- Xu et al. (2024); Deng et al. (2024). Train-on-test and adversarial construction.
- Epoch AI Benchmarking Hub — within-family cosine empirics.
- Manheim & Garrabrant (2018). Categorizing Variants of Goodhart's Law.
- Lu et al. (2024); Datta Kaggle dataset — benchmark metadata analysis.
