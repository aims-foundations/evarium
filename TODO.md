# TODO

## Experiment Script (Planned)

Important plots (one plot = one experiment):
1. Market share across runs (Full EU, US + Media, Incident, Startup, OpenSource)
3. Score vs capability (with r value)
4. combine incident timeline per provider (top left, incident_analysis_dashboard) with benchmark validity and intervention and incidents (policymaker_dashboard)

Tables (one column = one experiment):
1. Safety investment (Market leader, average)
2. Final consumer satisfaction
3. Total number of incidents (broken down by severity)

### Primary Runs

These are the two canonical full-feature runs to establish baseline results.
Both use LLM mode, 30 rounds, 5 providers + OpenCore, full ecosystem.

| ID | Policy | Command |
|----|--------|---------|
| exp_001 | US light-touch | `python run_experiment.py --policy us` |
| exp_002 | EU precautionary | `python run_experiment.py --policy eu` |

Key things to observe:
- Does EU precautionary policy reduce incident rate and severity vs US?
- Does US light-touch lead to faster capability gains but higher gaming gaps?
- Do startup entrants behave differently under each regime (BTE, funding, survival)?
- How does OpenCore's commoditization shock play out under each regime?
- Do benchmark focus specializations hold up over 30 rounds, or do competitive
  pressures homogenize providers?

---

### Ablations (demonstrating complex systems value)

Each ablation isolates one feedback loop or emergent mechanism to show what the
simulation captures that simpler models miss. Run heuristic mode (fast) unless
noted. All vs the US full-feature baseline.

#### 1. No media (`enable_media=False`)
- **Tests:** Whether media coverage meaningfully amplifies incidents into
  consumer switching and funder reallocation, or if it's cosmetic.
- **Hypothesis:** Without media, incidents cause weaker consumer response and
  slower regulatory escalation — safety underinvestment goes less punished.

#### 2. No incidents (`enable_incidents=False`)
- **Tests:** Whether the incident system creates meaningful safety investment
  pressure, or providers would converge to similar safety allocations anyway.
- **Hypothesis:** Without incidents, safety_alignment collapses for all
  providers — no endogenous force counters the competitive pressure to defund it.

#### 3. No startups (`startup_entry_probability=0`)
- **Tests:** Whether dynamic entry disciplines incumbents, or whether the
  established 5 providers settle into stable oligopoly regardless.
- **Hypothesis:** Without entry threat, incumbents sustain higher gaming gaps
  and less capability investment; market concentration increases monotonically.

#### 4. No benchmark specialization (uniform benchmark_focus)
- **Tests:** The new benchmark_focus feature — does it produce meaningfully
  differentiated leaderboard profiles, or is it noise?
- **Hypothesis:** Without specialization, all providers converge to similar
  per-benchmark profiles; safety benchmark is inflated even for non-safety labs.
  With specialization, Apex AI clearly leads safety; OpenCore leads math.

#### 5. No funders (`enable_funders=False`)
- **Tests:** Whether funder allocation creates meaningful feedback between
  market performance and capability investment, or if providers self-fund evenly.
- **Hypothesis:** Without funders, capability gaps narrow (no Matthew effect);
  startup survival rate drops (no VC runway extension).

#### 6. No open-source provider (remove OpenCore)
- **Tests:** Whether OS disruption dynamics (commoditization shock, cost
  pressure, contamination multiplier) materially reshape the ecosystem, or
  whether the closed-source race dynamics dominate regardless.
- **Hypothesis:** Without OpenCore, consumer cost sensitivity matters less,
  gaming gap is lower (no contamination pressure), market concentration is higher.

#### 7. Single benchmark (remove multi-benchmark setup)
- **Tests:** Whether multiple benchmarks with different validity/exploitability
  produce richer dynamics than a single aggregate score.
- **Hypothesis:** Single-benchmark runs show faster Goodhart degradation and
  less provider differentiation; no benchmark churn or saturation dynamics.

#### 9. Evaluator as company (`evaluator_as_company=True`)
- **Tests:** Whether commercializing the evaluator (premium access, best-of-N
  submissions, early benchmark access) creates conflicts of interest that worsen
  ecosystem outcomes — a structural critique of for-profit evaluation bodies.
- **Hypothesis:** Premium providers gain systematic scoring advantages decoupled
  from true capability; well-funded incumbents widen their lead; gaming gaps
  grow faster; smaller providers and startups are structurally disadvantaged.
  Safety-focused providers (Apex AI) may opt out of premium access on principle,
  worsening their competitive position despite genuine capability.

#### 10. No benchmark evolution (fix validity/exploitability, no new benchmarks)
- **Tests:** The benchmark lifecycle — does validity decay + new benchmark
  introduction actually reset gaming incentives, or do providers adapt instantly?
- **Hypothesis:** Without evolution, gaming gaps widen monotonically; with
  evolution, new benchmarks create periodic resets in the leaderboard order.

1. make vcs want to diversify more. not solely based on leaderboard
2. double check that VCs cant fund opensource, opensource cant invest in safety


## Policymaker → Incident Probability (Medium Complexity)

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
5. Tier 2 and Tier 3 implementation of policymakers
6. Rethink market share approach to fines. Maybe do research about what happens in practice — are fine rates in the US actually higher?
7. Change provider names to avoid bias

## Open-Source Provider Modeling

Core mechanics implemented. Remaining work:

- **Funder `open_source_sponsor` archetype** — funders currently treat OS providers normally. A new funder type should fund based on ecosystem_influence (adoption) rather than market-share ROI. Low priority since current funder behavior is acceptable for most experiments.
- **Market share vs. ecosystem influence for funder traction** — currently funders use market share for all providers. For OS providers, ecosystem_influence (logged per round in `open_source_data`) should replace market share as the traction signal in funder allocations.

## Barriers to Entry / Startup Entry

Core mechanic implemented. Remaining follow-on work:

- **Endogenous entry triggers:** Currently exogenous (fixed probability per round). Could make entry probability market-driven — e.g. spike when top provider's market share exceeds 0.5 or when a funder has excess undeployed capital.
- **Brand barrier for consumers:** Consumers with high trust sensitivity currently don't distinguish new entrants from incumbents. Could add a `new_entrant_trust_penalty` that decays over N rounds post-entry.
- **Gov funder exclusion:** Government funders currently can allocate to new entrants after the delay. Could add a flag to restrict gov/foundation funders from funding startups in early rounds.

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
