# CS5: Benchmark Sponsorship

**Status:** Brainstorm. Locked through mechanic + prompt in session 33; spec not persisted; deferred post-deadline. This doc re-establishes the frame for future pickup.

## 1. Policy anchor

Benchmark sponsorship is the arrangement where a model provider pays (in capital, compute, or problem contributions) for preferential access to a benchmark that the evaluator then publishes publicly. The real-world template is **FrontierMath / OpenAI**:

- Epoch AI's FrontierMath (launched Nov 2024) — tiered math problems (T1–T4), T4 items are especially difficult and kept strictly private.
- OpenAI was revealed (Jan 2025) to have had item-level access to FrontierMath under an undisclosed sponsorship arrangement, used for o3 pre-release training.
- Post-disclosure controversy reshaped community expectations about sponsor disclosure and pre-access.

Adjacent patterns:

- **ARC Prize** (Chollet, 2024 on) — sponsor-funded prize pool ($1M+) for ARC-AGI; scoring harness public; private test set.
- **MLPerf** (MLCommons) — vendor-sponsored benchmark consortium; participants partially steer benchmark design.
- **Scale AI / SEAL** — not strictly sponsored, but evaluator-capture revenue creates adjacent capture vectors (see CS4).

**The policy question** is: should benchmark sponsorship be (a) disclosed, (b) prohibited, (c) structured with sponsor rotation, or (d) left to market norms? The FrontierMath episode suggests that absence of any of these produces structural unfairness that emerges only after disclosure.

## 2. Sim mechanism (designed but not implemented)

### 2.1 Primitives to add

- **Per-benchmark `sponsor` attribute** on `BenchmarkGroundTruth`: `Optional[str]` — provider name, or None. Optionally a list for multi-sponsor benchmarks.
- **Per-benchmark `sponsor_disclosed` flag**: does the public ecosystem know who sponsors this benchmark? Controls reputational downside on disclosure events.
- **Sponsor pre-access**: reuse the `premium_pre_access` axis reserved in session 38. Sponsor gets N rounds of public-weight observations at t=0 for the sponsored benchmark. Simulates FrontierMath-style item access.
- **Sponsor submission advantage**: reuse `premium_submissions_per_round` (best-of-M). Matches evaluator-capture framing.
- **Sponsor fee** → evaluator budget: ties into evaluator-capture funding mix. Higher sponsor fees shift evaluator dependency toward paying providers.

### 2.2 Exposure event (optional, richer variant)

Model post-hoc disclosure as a stochastic event:

```
P_expose(t) = base_rate + investigative_pressure × (n_sponsored_benchmarks / n_total)
```

When exposed, the sponsored benchmark's `sponsor_disclosed` flips to True. Effects:

- Media narrative turns negative toward sponsor (existing `media.py` path).
- Funder allocation to sponsor takes a reputation hit.
- Consumer `leaderboard_trust` to that benchmark's scores decays.
- Regulator `audit` lever (sense 1) probability rises.

Anchor for calibration: the Leaderboard Illusion / Meta 27-variants episode, the FrontierMath/OpenAI episode.

### 2.3 Ablation conditions

| Condition | Disclosure rule | Sponsor pre-access | Expected effect |
|---|---|---|---|
| `no_sponsorship` | — | 0 rounds | Reference |
| `sponsorship_disclosed` | Mandatory at launch | 3 rounds | Tests price-of-transparency on sponsor advantage |
| `sponsorship_undisclosed` | Hidden unless exposed | 3 rounds | Primary contrast — captures FrontierMath-style arrangement |
| `sponsorship_rotation` | Sponsor identity rotates every K rounds | 3 rounds (to current sponsor only) | Tests capture-mitigation via structural rotation |

### 2.4 LOC estimate

~70 LOC:

- `src/visibility.py` — `sponsor`, `sponsor_disclosed` fields on `BenchmarkGroundTruth`.
- `src/actors/evaluator.py` — sponsor pre-access gating in `init_benchmark`; sponsor-specific `n_trials`.
- `src/actors/model_provider.py` — sponsor pre-access materialized as lower `σ_prior` for the sponsored benchmark.
- `src/actors/media.py` — exposure event + narrative generation.
- `src/simulation.py` — exposure probability schedule; sponsor fee flow to evaluator budget.
- `scripts/run_experiment.py` — 4 conditions above.

## 3. Status & sequencing

- Session 33: mechanic + LLM prompt locked. Spec was drafted in `rough/benchmark_sponsorship_design.md` but the file is no longer present; content not recovered.
- Session 38 reserved the `premium_pre_access` and `premium_submissions_per_round` primitives specifically for this use case.
- Session 47 ran an agent deep-dive ("20 axes, 6 bundles") that expanded the design space. Results in-conversation, not persisted.

**Blockers for implementation:**

- Exposure-probability calibration: base rate + investigative-pressure model is unanchored.
- Interaction with CS4 evaluator-capture: sponsor fees and premium-subscription fees stack. Need clear separation of which lever is being tested.
- Disclosure-rule ablations require at least 4 conditions × 30 heuristic seeds = 120 runs; not yet budgeted.

## 4. Paper claim (hypothetical — not for current paper)

Undisclosed benchmark sponsorship creates a **late-breaking market reshuffle**: the sponsor accumulates dominance via pre-access and best-of-N selection advantage; when disclosure occurs (stochastically), the accumulated gains reverse through funder reallocation and consumer trust loss. Disclosed sponsorship produces a smaller steady-state advantage; rotation produces no persistent advantage. The cumulative welfare ordering depends on exposure probability and market memory length.

## 5. Open questions

- **Sponsor selection** — is sponsorship exogenous (simulation assigns), or does a provider elect to sponsor (strategic choice)?
- **Multi-sponsor benchmarks** — ARC Prize has multiple sponsors; how does multi-sponsor affect capture? (First-pass: treat as diluted sponsorship.)
- **Sponsor visibility gradient** — beyond binary disclosed/undisclosed, there's "technical community knows, general public doesn't" — worth modeling?
- **Interaction with CS1 privacy ladder** — sponsorship is most consequential on private benchmarks (where pre-access is most valuable). Run sponsorship ablations within each privacy condition or only on baseline privacy?
- **Scope** — is this a stand-alone case study, or a sub-ablation inside CS4 (evaluator-capture)? Argues for standalone because the mechanism (per-benchmark sponsorship, not per-provider subscription) is structurally different.

## 6. References

- Epoch AI — FrontierMath launch + OpenAI disclosure
- Chollet — ARC-AGI; ARC Prize 2024–2025
- MLCommons — MLPerf governance
- Singh et al. (2025). "The Leaderboard Illusion." (Adjacent selection-bias mechanism)
- Bolton, Freixas, Shapiro (2012). The Credit Ratings Game. (Issuer-pays analog)
- Hardy et al. (2024). Benchmarks as Shared Information Goods.
- Lundh et al. (2017). Cochrane MR000033 — industry sponsorship and research outcome.

## 7. Internal pointers

- `src/visibility.py` — `BenchmarkGroundTruth` (sponsor fields to add)
- `src/actors/evaluator.py` — `premium_pre_access` hook (unused, reserved for this)
- `case_studies/evaluator_capture.md` (CS4) — overlapping but distinct business-model case
- `case_studies/privacy_ladder.md` (CS1) — sponsorship interacts with privacy; most relevant on private benchmarks
- `case_studies/audit_verification.md` (CS6) — sponsorship exposure is one specific case of the capture-exposure event
- Session memory: `session33_design_threads.md`, `session38_privacy_mechanism_redesign.md` (§ premium-access axis)
