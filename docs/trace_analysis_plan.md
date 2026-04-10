# Trace Analysis: Execution Plan

What to do with LLM reasoning traces, in what order, with what evidence standards. Methodology is in `aggregation_pipeline.md`; this doc is the execution plan for the paper.

---

## Evidence Structure for the Paper

The results section presents three layers of evidence. Each layer has its own data source and evidentiary standard.

| Layer | Data source | N | Standard | Supports |
|-------|-------------|---|----------|----------|
| Structural findings | Heuristic runs | 30 seeds/condition | Pattern pass rates, CIs, statistical tests | "Score inflation emerges reliably", "markets concentrate", "incidents drive safety investment" |
| Behavioral findings | LLM traces | 3-10 seeds/condition | Case studies, outcome enumeration | "LLM agents reason about competitors", "path dependence produces diverse outcomes" |
| Testbed demonstration | Custom condition runs | 10+ seeds | Ablation comparison | "The simulation can test policy questions" |

Every claim in the paper should be tagged to one of these layers. Do not make statistical claims from LLM N=3. Do not make behavioral claims from heuristic runs (no traces). Do not mix evidence types without being explicit.

---

## 1. Incident-Response Validation

**Purpose:** Face validation. Do actors respond to shocks in directionally plausible ways?

**Evidence standard:** Directional only. We validate that providers increase safety after incidents, regulators escalate, funders pull back from affected providers. We do not validate magnitudes — the empirical calibration data (Boeing, Samsung, Cruise) comes from different sectors with different market structures, and magnitude comparisons would be apples-to-oranges.

**What to extract per incident:**

For each major/critical incident across all LLM runs:

| Field | Source |
|-------|--------|
| Provider, round, incident type | `media_data.risk_signals` + `consumer_data.penalty_breakdown` |
| Safety allocation change (pp) | `effective_strategies[p].safety` at round N vs N-1 |
| Market share loss (pp) | `consumer_data.market_shares[p]` at N vs N-1 |
| Recovery time (rounds) | Rounds until share returns to 50% of pre-incident level |
| Provider reasoning excerpt | `actor_traces[provider]` at round N+1 (first round they can react) |
| Regulator action | `regulator_data.interventions` at round N |
| Funder allocation change | `funder_data.provider_funding_totals[p]` at N+1 vs N-1 |

**Output:** A standardized response profile table across all incidents. No subjective plausibility rating — present the patterns and let readers judge. Group by incident severity to show dose-response: do major incidents produce larger responses than moderate ones?

**What to watch for honestly:** Cases where actors *don't* respond plausibly. If a provider ignores a major breach, that's a simulation failure worth reporting. Honest presentation of failures builds more credibility than a 100% plausibility pass rate.

**Runs needed:** All LLM runs with incidents enabled. Extraction only — no new runs or code.

---

## 2. LLM-Adds-What

**Purpose:** Justify the LLM agent design. What does LLM reasoning produce that heuristic rules cannot?

**Evidence standard:** High bar. Each example must be: (a) contextual to the specific state the agent is in, (b) impossible to produce with any reasonable fixed rule, and (c) faithful to how a real actor would reason. We want 2-3 strong examples, not 10 weak ones.

**Two levels of evidence:**

**Quantitative (outcome comparison):**
- Compare outcome type distributions between LLM and heuristic runs (same conditions, CRN-paired seeds)
- If LLM mode produces more diverse outcomes (e.g., 3 outcome types vs 1), that's evidence the LLM adds strategic richness
- If both produce the same distribution, the LLM adds interpretability (reasoning traces) but not behavioral diversity — still a contribution, just a different one
- Requires re-running heuristic baseline with current code

**Qualitative (trace case studies):**
- Find specific decisions where the LLM trace shows reasoning that couldn't be a heuristic rule
- Strongest type: **emergent strategy shifts** where the agent contradicts its initialization (e.g., OpenCore investing in safety despite "no guardrails" identity, because user demand data shifted)
- For each example, verify empirically what the heuristic actually did on the same seed — don't speculate about "what a heuristic would do"
- Present as a small table: round, provider, what happened, reasoning excerpt, what heuristic actually did on same seed

**Runs needed:** CRN-paired LLM and heuristic runs on current code, same conditions, same seeds. The heuristic baseline re-run is a prerequisite.

---

## 3. Testbed Case Study

**Purpose:** Demonstrate the simulation as a tool for exploring specific questions. One fully-executed example.

**Primary candidate: Evaluator responsiveness**

*Question:* Does a dynamic evaluator (that responds to benchmark saturation by introducing harder benchmarks) produce better outcomes than a passive evaluator (fixed-schedule introduction)?

*Why this is the strongest case study:*
- The paper is about the evaluation ecosystem — the evaluator should be central to at least one result
- `dynamic_evaluator` config flag already exists — no new code needed
- Score reliability is the natural primary metric and directly measures evaluation quality
- It tests whether evaluation governance matters, which is the paper's central thesis
- Real-world parallel: the shift from static benchmarks (MMLU) to adaptive evaluation (Chatbot Arena, SWE-bench evolution)

*Configuration:*
- Condition 1: `full_ecosystem` (passive evaluator, fixed 5-round introduction schedule)
- Condition 2: `full_ecosystem` with `dynamic_evaluator=True` (evaluator detects saturation and responds)
- CRN-paired seeds, 10+ seeds per condition

*Metrics:*
- Score reliability trajectory (does the dynamic evaluator maintain higher reliability?)
- Dimensional mismatch (does responsive introduction reduce the gap between what benchmarks measure and what consumers need?)
- Provider strategy adaptation (do providers game less when benchmarks evolve responsively?)
- Benchmark introduction timing (when does the dynamic evaluator act vs the fixed schedule?)

*Visualization:* Spaghetti trajectory plots (LLM) or quantile bands (heuristic) for score reliability, with benchmark introduction events overlaid as vertical markers.

### Other Case Study Candidates (deferred)

Listed for future work. Not specified in detail because we should commit to one and execute it well.

- **Benchmark proliferation** — 1 vs 4 vs 10 benchmarks. Tests whether more benchmarks improve signal or add noise. Already partially configurable (`single_benchmark` condition, `max_benchmarks` param).
- **Progressive compliance** — regulator scales fines by provider size. Tests whether the consolidation paradox can be broken. Requires regulator code changes with careful formula design.
- **Evaluator business model** — eval_as_company vs free evaluation. Tests pay-to-play distortion. Already implemented, but the mechanism (score variance reduction from multiple submissions) may be too weak to detect.
- **Open-source entrant** — mid-sim provider entry. Strongest policy question but requires significant architecture work (mid-run provider initialization). Future work.

---

## Execution Order

1. **Re-run heuristic baseline** (current code, 30 seeds, key conditions). Prerequisite for structural claims and LLM-adds-what comparison.
2. **Incident-response validation** from existing LLM runs. Extraction only.
3. **LLM-adds-what** once heuristic baseline is ready for paired comparison.
4. **Evaluator case study** runs (10+ seeds per condition, LLM mode).
5. **Paper writing** — results section structured around the three evidence layers.

---

## Failure Modes

What to do if things don't work:

- **Incident validation shows implausible responses:** Report honestly. Document which response patterns fail and why. This is diagnostic information about the simulation's limitations, not a reason to hide results.
- **LLM-adds-what shows no meaningful difference:** Report that the LLM adds interpretability but not behavioral richness. Reframe the contribution as "reasoning traces enable a new kind of analysis" rather than "LLM agents are better."
- **Evaluator case study shows no effect:** Report null result. "Dynamic evaluation does not measurably improve outcomes in this simulation" is itself a finding — it suggests that evaluation responsiveness is less important than other ecosystem dynamics (incidents, market structure).
- **All seeds converge to the same outcome (no divergence to analyze):** Skip divergence analysis. Report convergence as a finding about structural determinism. Focus on which conditions produce convergence vs diversity.
