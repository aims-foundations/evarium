# Validation Brainstorm

> Exhaustive sketch of approaches to validating the evaluation-ecosystem simulation. Organized by axis; each entry flags data/infra requirements and what the approach can actually buy.

---

## Axes

Standard ABM validation literature crosses three axes:
- **Internal ↔ External** — consistency inside the model vs. match to reality
- **Objective ↔ Subjective** — quantitative metric vs. expert judgment
- **Structural ↔ Output** — mechanisms right vs. behavior right

Cross-cutting: **retrospective** (match past) vs. **prospective** (predict future).

---

## I. Internal validation

### I.A Objective

1. **Parameter sensitivity** — Sobol / one-at-a-time sweeps over `learning_rate`, `benchmark_orientation`, `rnd_efficiency`, `holdout_fraction`, incident penalties, etc. Ranks which parameters move which outputs. Cheap with heuristic mode; we have N=30 infrastructure already. What it buys: identifies fragile/dominant parameters; rules out "result is a knife-edge artifact." Doesn't validate correctness.

2. **Structural ablations** (partly done) — already running with 22-benchmark ablation grid. Extensible: ablate media, funders, regulator, incidents entirely, one at a time. Differentiates which mechanisms are *load-bearing* for each phenomenon.

3. **Seed variance decomposition** — partition output variance into seed / parameter / condition components (Gelman-style). Tells you when N=30 is enough and when LLM N=3 is woefully underpowered.

4. **Monotonicity / sign tests** — "more R&D → higher scores", "higher `holdout_fraction` → lower gap", "more safety budget → fewer incidents (in expectation)". If any fail, the mechanism is mis-specified. Cheap; worth a nightly regression suite.

5. **Boundary/edge cases** — 100% safety, 0% R&D, single provider, 1 benchmark, `holdout=1.0`. Check degenerate cases produce sensible limits.

6. **Conservation invariants** — market shares sum to 1, portfolio sums to 1, no negative capability, published_scores monotone non-decreasing. Already partly enforced; worth a standing assertion sweep.

7. **Convergence / stability** — does p10–p90 band stabilize by N=30? Is the system chaotic (Lyapunov-like sensitivity to ε parameter perturbation)? If yes, single-run case studies can't carry epistemic weight without aggregate backing.

8. **Parameter recovery** (identification) — simulate with known params, try to re-infer them from outputs via SMM/ABC. If you can't recover `benchmark_orientation` from observables, you can't calibrate it from data either. Underused; would be a real contribution.

9. **Regression tests** — `smoke_test.py` exists. Extend to golden-trajectory tests for key conditions so refactors don't silently shift dynamics.

### I.B Subjective

10. **PIMMUR trace audit** — already doing. Extensible to full-corpus coding (instead of flagged-term grep): have an LLM judge rate provider reasoning on {internal consistency, awareness of uncertainty, mechanism-appropriate response}.

11. **Manual trace inspection** — read random N traces, mark any that would fail a domain-expert sniff test. The vignettes file already has 3; scale to ~30.

12. **Counter-narrative reading** — pick traces where simulation says X happened; check if the reasoning *supports* X vs just being followed by X.

---

## II. External validation

### II.A Objective — quantitative data matches

13. **Benchmark score trajectories vs HELM / Papers-with-Code** — you already have `external-validation/data/`. Compare simulated score curves 2023→2025 against HELM longitudinal data for MMLU, HumanEval, GPQA, SWE-bench. Can match per-provider slopes *and* saturation timing. Strongest single external anchor available.

14. **Market share dynamics vs SimilarWeb / State of AI Report / a16z Top 50 GenAI** — compare simulated 6-provider HHI and share-over-time against real adoption. Caveat: "market share" is poorly operationalized in real AI (API revenue? MAU? developer surveys?) — pick one and match it.

15. **Incident rates vs AI Incident Database (AIID) / OECD AI Incidents Monitor** — both public. Compare severity distribution and frequency over 2023–2025. ~800+ AIID entries in that window; enough for distributional match.

16. **Funding allocation vs Crunchbase / Pitchbook / State of AI** — match VC vs corporate vs government share; match concentration (top-3 share of AI funding). State of AI has this compiled.

17. **Regulatory timing vs actual regs** — EU AI Act (passed 2024-05), EO 14110 (2023-10, revoked 2025-01), SB 1047 (vetoed 2024-09). Does the sim's regulator escalate at comparable times under US-lite vs EU presets?

18. **Media sentiment vs GDELT / MIT Media Cloud** — both scrapable. Match attention spikes around real events (GPT-4 release, Bing Sydney, DeepSeek-R1).

19. **Published safety budgets / RSP disclosures** — Anthropic's RSP, OpenAI's preparedness framework, DeepMind's safety framework publish qualitative allocations. Check simulated allocations aren't wildly off (Apex AI highest safety share — matches).

20. **Score-satisfaction divergence vs Chatbot Arena vs MMLU** — *this is the real-world version of your gap*. Chatbot Arena Elo vs benchmark scores is a documented divergence (Zheng et al. 2023, various follow-ups). Directly maps onto `score_reliability`. Strong theoretical-empirical bridge for the credence-good framing.

21. **Market concentration vs real HHI** — Epoch AI tracks frontier-model concentration. Compare.

22. **Benchmark introduction cadence vs Papers-with-Code** — real benchmark releases 2023–2025 are timestamped; compare cadence against dynamic evaluator's schedule.

23. **Benchmark saturation dynamics vs HELM** — HELM tracks when benchmarks saturate (MMLU saturation timeline is documented). Compare retirement timing.

### II.B Objective — stylized facts (Windrum et al.)

24. **Qualitative regularities** — does the sim reproduce these without being tuned to?
    - Fast-follower catch-up (Anthropic catching OpenAI)
    - Open-weight model disruption (Llama / DeepSeek shock)
    - Safety-capability substitution under funding pressure
    - Benchmark saturation → new benchmark cycle
    - Goodhart divergence accelerating under high leaderboard trust
    - Incident → media spike → regulator escalation chain
    
    Each is a binary pass/fail. 6/6 is strong; 3/6 is diagnostic.

### II.C Subjective

25. **Expert elicitation** — structured interviews with AI lab researchers / AI policy analysts / METR-adjacent folks. Show traces + aggregate plots, ask plausibility on a rubric. Costly but high-signal. Stanford access makes this genuinely feasible.

26. **Turing-style trace comparison** — mix simulated provider reasoning with real blog posts / RSP excerpts / leaked strategy docs (Anthropic's are partly public). Can experts tell them apart better than chance? Powerful but setup-heavy.

27. **Case-study plausibility scoring** — take 3–5 real events (DeepSeek shock, GPT-4o release, Claude 3 Opus release) and ask experts: does the closest-matching simulated trajectory read as a plausible rendering?

---

## III. Structural / theoretical validation

28. **Credence-good theory match (Dulleck & Kerschbamer 2006)** — already cited. Their model predicts specific quality-distortion dynamics under unobservable quality; check sim reproduces them (overprovision of observable attributes, verified).

29. **Goodhart specializations (Manheim & Garrabrant 2018)** — they taxonomize 4 Goodhart modes. Check which emerge; good framing for discussion.

30. **Rational inattention / signal theory (Sims 2003; Hardy et al. 2024)** — Hardy already cited. Check consumer exploration behavior matches predicted form.

31. **Game-theoretic equilibrium checks** — in degenerate configs (2 providers, 1 benchmark, no incidents), does provider behavior converge to Cournot-like or Bertrand-like predicted equilibria? If yes, you have analytic backing on a simple slice.

32. **Out-of-equilibrium behavior** — ABMs *should* differ from GT equilibria off-equilibrium. Document where and why.

---

## IV. LLM-specific robustness

33. **Cross-LLM-provider structural convergence** — partly done (claudecode vs anthropic |Δgap| ≤ 0.012). Extend to Gemini, GPT-4.x. Convergence = behavior is driven by sim structure not LLM idiosyncrasy.

34. **Model-generation sensitivity** — Claude 3.5 vs 4 vs 4.6 vs 4.7. If newer models dramatically change results, your findings age with the model.

35. **Prompt ablations** — drop memory, shuffle field order, paraphrase key sentences. How much do results depend on prompt surface?

36. **Temperature sweep** — at T=0 vs T=1, do aggregate results hold? Checks whether results depend on a single mode or are distribution-level.

---

## V. Meta-frameworks

37. **Sargent's framework** — already referenced in `rough/validation_plan.md`. Face validity + historical data + Turing test + predictive. Use as a checklist, not a method.

38. **Axtell docking** — independent reimplementation in a different language/framework. Prohibitively expensive for a solo project; skip unless a collaborator volunteers.

39. **Park et al. generative agents** — they validate via believability ratings on isolated behaviors. Adaptable: rate specific provider decisions on a Likert scale.

40. **History-friendly calibration (Malerba et al.)** — tune structural params to one historical period, validate on a later one. 2023 → 2024–2025 is the obvious split.

---

## VI. Natural experiments / case-based

41. **Retrodiction of specific events** — initialize sim to Q1 2023, ask: does DeepSeek shock emerge? Does an Anthropic-like safety lead persist? Does GPT-4o-like product gap emerge?

42. **Out-of-sample counterfactuals** — calibrate on 2023 only, predict 2024 H1 with no recalibration, compare. Most demanding external test.

43. **Policy counterfactuals** — run EU-style vs US-style vs no-reg. Do differential outcomes match real EU vs US divergence (where observable)?

---

## VII. What we probably can't validate

- **Specific private reasoning** — can validate aggregates of lab behavior but not "is Orion's reasoning at R17 the actual reasoning of any real lab." Honest to surface.
- **Individual funder decisions** — VC term sheets mostly private.
- **Counterfactual policy effectiveness** — no ground truth for "what would have happened under SB 1047."
- **Long-horizon predictions** — sim is 2.5 years; beyond that compounding uncertainty dominates.

---

## Critical framing for the paper

Two honest claims are defensible now:
- **Structural**: the sim reproduces documented stylized facts (score-satisfaction divergence, Goodhart dynamics, safety-capability tradeoffs) under mechanisms grounded in cited theory.
- **Exploratory**: conditional on the mechanisms, it lets you ask counterfactual questions that can't be asked empirically.

Two stronger claims would need real work:
- **Predictive**: requires II.A (13, 14, 20, 23) + VI.42 (out-of-sample).
- **Causal**: requires I.8 (identification) — otherwise you can't attribute outcomes to specific mechanisms.

---

## Recommended prioritization (cheapest signal-per-hour first)

1. Monotonicity + edge-case regression suite (I.4, I.5) — 1 day, catches silent breakage
2. HELM trajectory overlay (II.A.13) — data already local, strongest single external anchor
3. Chatbot Arena ↔ MMLU gap comparison (II.A.20) — direct support for credence-good framing
4. Stylized facts checklist (II.B.24) — table in paper
5. Cross-LLM convergence extension to Gemini/GPT (IV.33) — you have the infra
6. Expert elicitation on existing traces (II.C.25) — slow calendar, high paper value
7. Parameter recovery / identification (I.8) — ambitious, would be a methodological contribution
