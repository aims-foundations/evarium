# TODO

## Policymaker → Incident Probability (Medium Complexity)

These extend how policymaker actions reduce incident probability. The easy items
(safety floor, sanction reduction, investigation score discount, history escalation)
are already implemented (2026-02-19).

- **Pre-deployment gate (ex-ante requirement):** EU policymaker sets a flag requiring
  providers to pass a minimum true_capability/safety_alignment threshold before new
  capability gains are published to the market. Failed checks delay market impact by
  1 round and trigger a forced safety bump. Requires a new policymaker action type and
  a gate in the benchmark scoring / market update loop. Most structurally accurate model
  of EU AI Act conformity assessment (Art. 43). High realism.

- **Compliance burden R&D tax:** While under active regulation (compliance_audit or
  higher), provider faces a small `rnd_efficiency` reduction (e.g. 0.05–0.15x) modelling
  legal/documentation overhead. Separate from sanction fine. EU preset applies it at
  compliance_audit+; US never. Strong empirical basis: GDPR compliance costs 1–3%
  revenue (IAPP/EY 2017); EU AI Act conformity assessment €30K–€400K per system.

## Simulation Behavior

1. Verify each actor uses ecosystem public signals when making decisions, not just their initial character profile.
2. VCs should be able to invest in non-AI companies (no need to model deeply — just allow the option).
3. Benchmark spacing should scale with total rounds (rough target: ~8 benchmarks over 50 rounds).
4. Slow down benchmark saturation; make introduction timing more realistic without overloading the system.
5. Scope to introduce a new provider during the round. Can be useful to model the barriers to entry in the market, and the probability of a new startup entering the provider space.
6. Tier 2 and Tier 3 implementation of policymakers
7. rethink market share approach to fines. maybe do research about what happens in practice. are rates in US actually higher?
8. change names to avoid bias

## Open-Source Provider Modeling (PARTIALLY IMPLEMENTED 2026-02-21)

Core mechanics implemented. Remaining work:

- **Funder `open_source_sponsor` archetype** — funders currently treat OS providers normally. A new funder type should fund based on ecosystem_influence (adoption) rather than market-share ROI. Low priority since current funder behavior is acceptable for most experiments.
- **Market share vs. ecosystem influence for funder traction** — currently funders use market share for all providers. For OS providers, ecosystem_influence (logged per round in `open_source_data`) should replace market share as the traction signal in funder allocations.

## Barriers to Entry and Mid-Simulation Provider Entry

New providers entering mid-simulation is structurally important for modeling market competition and contestability. Design considerations:

- **Entry trigger conditions.** A new provider should enter when: (a) market is profitable enough (top providers generating high revenue), (b) a funder has excess capital and no good investment target, or (c) a random "startup formation" probability fires each round. Could be exogenous (scheduled) or endogenous (market-driven).
- **Initial conditions.** Entrant starts with low capability (0.30–0.40), low market presence, high evaluation_engineering weight (startups game benchmarks to signal quality cheaply), and limited funding. Mirrors real patterns: new labs often benchmark-optimize aggressively before establishing research depth.
- **Barriers to entry parameters.** Should be configurable: compute cost floor (min capital required to enter), regulatory barrier (EU gate means new entrants must pass pre-deployment check before round 1 of participation), and brand barrier (consumers with high trust sensitivity won't switch to unknown providers for N rounds).
- **Funder interaction.** Entry events should consume funder capital. TechVentures-type VCs are most likely to fund entrants. Gov funders should not fund new entrants by default.
- **Simulation mechanic.** `EvalEcosystemSimulation.run_round()` checks entry conditions each round; if triggered, instantiates a new `ModelProvider` and appends to `sim.providers`. History logging needs to handle variable-length provider arrays gracefully (already partially true since providers are keyed by name).
- **Item 5 in Simulation Behavior above** overlaps with this — consolidate once implementation starts.

## Research-Backed Sources for Simulation Components

Collect empirical and theoretical grounding for each major simulation mechanism. Goal: each key parameter or behavioral assumption should be citable.

- **Benchmark gaming / Goodhart's Law:** Goodhart (1975); Anthropic evals literature; Raji et al. "AI and the Everything in the Whole Wide World Benchmark" (NeurIPS 2021); Kiela et al. "Dynabench" (2021); Bowman et al. "Measuring Progress on Scalable Oversight" (2022).
- **Benchmark validity decay:** Document saturation rates empirically — how fast do SOTA models reach ceiling on major benchmarks (MMLU, HumanEval, GSM8K). Papers: Guo et al. on benchmark contamination; "Are We Done with MMLU?" (2024).
- **Safety underinvestment / race dynamics:** Dafoe "AI Governance" (2018); Chan et al. "Harms from Increasingly Agentic AI" (2023); Krakovna et al. on specification gaming; NIST AI RMF for empirical safety investment framing.
- **Funder behavior / VC dynamics:** Funding data from PitchBook/CB Insights AI investment reports; Cihon et al. "Corporate Governance of AI" for non-commercial funder types.
- **Regulatory interventions:** EU AI Act (2024) for precautionary/threshold parameters; NIST AI RMF for US light-touch framing; IAPP/EY GDPR compliance cost study (2017) for compliance burden parameter ($1–3% revenue).
- **Incident rates and severity:** AI Incident Database (AIID) for base rates; Weidinger et al. "Sociotechnical Safety Evaluation" (2023); Anthropic/DeepMind safety papers for severity classification schema.
- **Market share and consumer switching:** Standard discrete-choice / logit switching models; empirical AI adoption surveys (Stanford AI Index annual reports) for segment-level sensitivity parameters.
- **Evaluator independence and conflict of interest:** Raji et al. "Closing the AI Accountability Gap" (2020); Coston et al. on third-party auditing; UK DSIT evaluator landscape reports.

*Action: For each item above, find the canonical citation, extract the specific number or qualitative finding that maps to a simulation parameter, and annotate the relevant code with a comment referencing it.*

## Known Edge Cases

- **Same-round simultaneous saturation:** When two benchmarks saturate on the same round, the second replacement is delayed by the min-gap cooldown. Fix: allow introducing two benchmarks in one round (return a list instead of a single Benchmark). Low priority.

## Plotting

- Enhanced provider dashboard: "Evaluation Advantage" panel (premium access vs score jumps) and "Investment vs Trials" scatter.
- Enhanced summary dashboard: incident summary tile (by severity, most incident-prone provider) and evaluator business tile (budget, premium providers, revenue mix).
- New dashboard: `plot_ecosystem_dynamics_dashboard()` — incident→media→consumer flow, evaluator financial sustainability, gaming detection ROC, market concentration vs incident rate.
- Nice-to-have: interactive plots (Plotly/Bokeh), animated visualizations, comparative side-by-side dashboards.

## Infrastructure

- **`run_llm_now.py` is likely broken** — new config parameters (`enable_incidents`, `evaluator_as_company`, `enable_media`, `consumer_llm_mode`, policymaker presets, `use_case_profiles`) are not wired up. Needs sync with `run_experiment.py` structure.
- **`compare_experiments.py`** — tool to load two experiments, diff their configs, compute per-metric divergence timelines, and identify the first round of significant divergence. Would replace the current manual summary.json comparison workflow.
