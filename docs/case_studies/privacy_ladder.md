# CS1: Evaluator Information Design — The Privacy Ladder

**Status:** Live. Primary mechanism of the current paper's main result (§5.2).

## 1. Policy anchor

Three real-world patterns for how evaluators reveal benchmark information:

- **Fully public** — MMLU, HumanEval, GPQA publish items, labels, and scoring logic. Providers can train on anything resembling the distribution.
- **Partially private (SEAL-style)** — Scale's SEAL benchmarks keep items private but leak through metadata and item-family patterns. Contamination estimates: 8–16 percentage-point inflation (Singh 2024, Dominguez-Olmedo 2024).
- **Adversarial private (FrontierMath-T4)** — Epoch's Tier-4 holdout never touches public infrastructure. Within-family Pearson to public items ≈ 0.85 (Epoch Hub).

No single law mandates any of these; they emerge as evaluator design choices. The **policy question** is: what information structure do we want evaluators to adopt, given that provider behavior responds to each differently?

## 2. Sim mechanism (live)

Three orthogonal information-design channels, implemented in `src/actors/evaluator.py` and `src/visibility.py`:

1. **Weight distance (`cosine`)** — holdout weights differ from public weights. Closer cosine = more exploitable via score-targeting. Composite proxy for contamination + train-on-test-task + adversarial construction.
2. **Reporting lag (`K=3`)** — holdout score published every K rounds, else frozen; stale signal delays feedback. Empirically calibrated to real-world benchmark release cadence (session 37).
3. **Noise scaling (`h`)** — holdout score computed on `samples × h` items; σ/√(samples·h) noise floor.

Four benchmark types:

| Type | `h` | `cosine` | Real-world analog |
|---|---|---|---|
| `public` | 0 | — | MMLU, HumanEval, GPQA |
| `partial` | 0.3 | 0.95 | SEAL with leakage |
| `private` | 1.0 | 0.85 | FrontierMath-T4 |
| `iid_holdout` | 1.0 | 1.00 | Ablation-only — isolates noise+lag from weight distance |

Five ablation conditions assign types uniformly across the 13-benchmark session-43 roster:

| Condition | Assignment | Role |
|---|---|---|
| `public_only` | all public | pre-private-era baseline |
| `baseline` | 8 public / 3 partial / 2 private | matches 2024–2025 reality |
| `private_dominant` | all partial | SEAL-dominant future |
| `private_only` | all private | FrontierMath-dominant future |
| `iid_holdout` | all iid_holdout | channels 2+3 without channel 1 |

Belief primitive: `σ_prior = 0.05`. Providers know benchmark framing but not exact dimension weights; initial belief = `normalize(clip_nonneg(public_weights + Normal(0, σ_prior)))`.

## 3. Status

- Mechanism landed session 38 (2026-04-18).
- Session-43 roster overhaul (13 benchmarks, 8/3/2 ratio) changed `baseline` composition; full re-baseline required.
- LLM runs at seeds {1000, 221, 427, 125, 127}, claude-sonnet-4-6; heuristic N=30 per condition.
- Re-baseline on new roster is part of the §5 redesign workstream (Phase 2).

## 4. Paper claim (§5.2)

Adversarial privacy (high `h`, low `cosine`) reduces the |score–satisfaction gap| monotonically across the ladder. The `iid_holdout` ablation pushes the gap more negative than `public_only`, which reveals that channels 2+3 alone produce **cleaner measurement that undershoots gaming-inflated public scores** — the weight-distance channel (cosine) is what creates the selection bias in the first place. The mechanism is legible at the per-benchmark level: 8 of 10 benchmarks show the expected direction in post-session-43 runs.

## 5. Open questions

- **σ_prior calibration** — current 0.05 is preliminary; longer sweeps needed to verify convergence on private benchmarks.
- **Asynchronous release** — F1 locks synchronized K=3; Fix-C gap-level jitter and F3 Bernoulli release deferred as sensitivity ablations.
- **Premium access** — `premium_pre_access` axis (orthogonal to privacy) reserved for CS4 / CS5 ablations.

## 6. References

- Singh, Nan, Wang (2025). "The Leaderboard Illusion." arXiv:2504.20879
- Dominguez-Olmedo et al. (2024). Contamination magnitude in LLM benchmarks.
- Xu et al. (2024); Deng et al. (2024). Train-on-test and adversarial construction.
- Epoch AI Benchmarking Hub — within-family cosine empirics.
- Manheim & Garrabrant (2018). Categorizing Variants of Goodhart's Law.
- Lu et al. (2024); Datta Kaggle dataset — benchmark metadata analysis.

## 7. Internal pointers

- `src/visibility.py` — `BenchmarkGroundTruth.benchmark_type` field
- `src/actors/evaluator.py` — `_score_provider_on_benchmark` (holdout-only scoring + h-noise + K-lag)
- `src/actors/model_provider.py` — `init_benchmark` with noisy-public-weights prior
- `src/simulation.py` — `sigma_prior` config
- `scripts/run_experiment.py` — 5 condition presets via `_scale_cdw` helper
- `scripts/plots/paper/plot_ablation_main.py` — §5.2 main figure
- `scripts/plots/paper/privacy_ladder_scatter.py` — per-benchmark + per-condition scatter
- Session memory: `session38_privacy_mechanism_redesign.md`, `session37_k_calibration.md`, `session43_roster_randomization.md`
- Canonical architecture: `docs/stakeholders.md` "Private benchmark blending formula"
