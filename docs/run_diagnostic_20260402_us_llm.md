# Run Diagnostic: full_ecosystem_us_llm_20260402_102131

> 24 rounds (of 40 configured), US light-touch preset, LLM mode (Anthropic), seed 3, 6 providers.

---

## 1. What Went Well

### Market responds to incidents realistically
Round-4 Orion critical security breach (10M user conversations) triggers 60.4% -> 13.8% market share collapse in one round. Apex AI absorbs most of it. 51.7% switching rate is high but defensible for a critical incident on the dominant provider.

### Capability growth rates are reasonable
Over 24 rounds (~2 years), Apex AI goes from ~0.47 mean to ~0.65 mean. No unrealistic capability explosions. The frontier spreads out -- OpenCore leads coding (0.62) and agentic (0.25), Apex leads safety (1.0), knowledge (0.72), communication (0.83). Differentiation emerges naturally from portfolio choices.

### Benchmark introduction works
Scientific Reasoning (r6), Agentic Tasks (r12), Hard Coding (r18) arrive on schedule. Each causes a visible composite score dip -- exactly the real-world pattern when new benchmarks reshuffle rankings.

### Portfolio allocations are LLM-diverse and responsive
Providers don't converge to the same portfolio. Apex shifts safety down (0.30->0.08) while consolidating dominance, then back up (0.22) after its healthcare incident at r12. Orion spikes safety to 0.30 post-incident. OpenCore maintains highest R&D throughout.

### Funder behavior tracks market signals
Orion funding collapses from 115M to 5M after the critical incident, then slowly recovers. Genesis funding decays to 0 by r22 as it becomes the weakest provider. Apex gets ~335M throughout its dominance period.

### Media narrative transitions
OPTIMISM -> SKEPTICISM at r16 (Genesis's second security breach), back to OPTIMISM at r21. Plausible timescales.

### Consumer satisfaction trends upward
Aggregate satisfaction 0.43 -> 0.69 over 24 rounds. The market is getting better at serving consumers.

---

## 2. What Could Be Better -- Simpler In-Simulation Fixes

### FIXED: Benchmark orientation collapsed to floor for 5/6 providers
All providers except OpenCore decayed to 0.05 (the hard floor) by round 11-12 and stayed there. The LLM outputs "less" for benchmark_orientation nearly every round; the -0.075 delta compounds to floor in ~10 rounds.

**Root cause:** `run_experiment.py` defaulted to `benchmark_orientation_mode="adjustable"` even though `SimulationConfig` defaults to `"fixed"`. The LLM rationally discovers that optimizing for user feedback beats optimizing for benchmarks, and abandons benchmarks entirely.

**Fix applied:** Changed `run_experiment.py` default to `"fixed"`. Providers now hold their configured benchmark_orientation (default 0.80) throughout the run. The `"adjustable"` setting remains available as a `--condition bm_orientation_adjustable` ablation for future study.

**Open question (flagged for discussion):** Should adjustable mode exist at all? If so, what prevents universal decay? Options: slower delta (0.04 instead of 0.075), asymmetric deltas (harder to reduce), per-provider floors (0.15-0.40 instead of 0.05), or removing adjustability entirely.

### Orion satisfaction cliff-edge at round 10
Satisfaction suppressed at 0.17-0.19 for rounds 5-9, then jumps to 0.54 at round 10. The incident penalty uses a hard 5-round window (in `consumer.py` line 646: `inc.round_num >= round_num - 5`). No decay within the window -- an incident 4 rounds ago hits as hard as this round's. When the window expires, penalty drops from full to zero instantly.

**Fix:** Replace the hard window with exponential decay, e.g. `penalty *= decay_factor ** (round_num - inc.round_num)` with decay ~0.5-0.6 per round. This gives a natural 2-3 round half-life without cliff edges.

### No startups entered (despite p=0.15/round)
Over 24 rounds with p=0.15, expected entries ~3.6. Zero entries suggests the BTE modulation is too aggressive. Composite BTE is 0.40-0.53, which likely suppresses effective entry probability below meaningful levels.

**Fix:** Check the BTE-to-entry-probability formula. Possibly needs a floor on effective probability or a softer modulation curve.

### Incident frequency is very low
Only 6 incidents across 144 provider-rounds (4.2% effective rate vs 10% base). Long stretches of zero incidents (rounds 5-11, rounds 17-23) make the regulator and media largely idle.

**Root cause (worked example for Apex AI at safety=0.78, market_share=0.67):**
```
prob = 0.10 * (1 - 0.78*0.8) * (0.5 + 0.67*1.5) * (0.8 + 0.78*0.4)
     = 0.10 * 0.376 * 1.505 * 1.112
     = 6.3%
```
The safety_multiplier (0.376) is the dominant suppressor. High-safety providers become nearly incident-immune.

**Fix options:** (a) Raise base rate to 12-15%. (b) Soften the safety discount (use 0.6 instead of 0.8 in the multiplier). (c) Add a minimum effective probability floor (e.g. 4% regardless of safety investment).

### Regulator acts on clockwork cadence
Actions every 3 rounds (voluntary commitment -> disclosure -> advisory -> audit -> advisory -> audit -> audit -> silence). No sanctions ever. Looks like a timer rather than a strategic actor. Likely connected to low incident frequency -- with near-zero incident rate for most rounds, the regulator has little to respond to.

---

## 3. What Could Require Larger Design Changes

### Score-satisfaction gap (Goodhart dynamics) never emerged
With orientation at floor, R&D was routed 95% by consumer_signal -- providers directly optimized consumer utility. No wedge for Goodhart dynamics. This is the central phenomenon the sim is built to study.

**Interaction with orientation fix:** Fixing orientation to 0.80 should restore the benchmark-driven R&D pathway. Providers will route 80% of R&D via inferred_benchmark_weights and only 20% via consumer_signal. If benchmark weights diverge from consumer need weights (which they do -- see benchmark pool), the gap should emerge. This needs to be verified in the next run.

### Single-incident dominance / excessive path dependence
The entire 24-round trajectory is determined by one stochastic event (round-4 critical Orion breach). Without it, Orion likely dominates throughout. The market switching model allows 51.7% reallocation in one round, and the winner-take-most dynamic locks in the new leader.

**Possible changes:** (a) Cap per-round switching at 20-25%. (b) Exponential incident penalty decay (see above). (c) Increase exploration churn above 3%. These compound -- any two together may be sufficient.

### Apex AI safety caps at 1.0 by round 17
Unrealistic -- no real provider achieves perfect safety. The direct safety lever (`safety_fraction * effective_budget`) adds unconditionally and exclusively to the safety dimension. When safety_frac = 0.22 and effective_budget = 0.11, that's 0.024/round straight to safety. Combined with the RD pathway contributing ~0.01/round via consumer_signal, the 0.45 gap closes in ~17 rounds.

**Three compounding factors:**
1. Highest starting safety (0.55) -- less distance to ceiling
2. Consistently high safety_fraction (never below 0.079, averages ~0.20)
3. Massive funding (330M from funders) -- even after sqrt compression, effective_budget is ~0.11

**Possible changes:** (a) Soft cap / asymptotic approach: `gain *= (1 - current_value)^k` for k>3 (current diminishing_returns_rate=3.0 may not be enough on single dimensions). (b) Add a realistic ceiling below 1.0 (e.g. 0.90). (c) Make the direct safety lever subject to the same diminishing returns as the RD pathway.

### OpenCore is inert
Steady 12% market share, no qualitative role. Belief broadcast is on but irrelevant (orientation at floor). Safety erosion is on but incidents are rare. Cost_bonus contribution is small (max ~0.04 for high-cost-sensitivity segments).

**Possible changes:** (a) Increase cost_bonus multiplier. (b) Implement the step-change jump mechanism described in stakeholders.md. (c) With orientation fixed at 0.80, belief broadcast may actually matter -- needs post-fix verification.

### Genesis and Spark are dead weight by mid-run
Genesis decays from 12% to 3%, loses all funding. Spark goes from 9% to 2%. No catch-up mechanism exists -- the funding->capability->market share loop is negative for laggards.

**Possible changes:** (a) Scale breakthrough probability inversely with market share. (b) Niche-specialization pathway. (c) Contrarian/underdog funder allocation mode.

---

## Key Data Tables

### Market Shares (selected rounds)

| Round | Apex AI | Genesis | Mirage | OpenCore | Orion | Spark |
|-------|---------|---------|--------|----------|-------|-------|
| 0 | 14.8% | 11.9% | 11.0% | 9.3% | 43.9% | 9.1% |
| 3 | 14.7% | 7.5% | 6.6% | 5.6% | 60.5% | 5.1% |
| 4 | 50.6% | 9.3% | 12.5% | 9.6% | 13.8% | 4.3% |
| 10 | 67.2% | 7.3% | 5.5% | 11.7% | 5.1% | 3.2% |
| 20 | 66.8% | 3.2% | 3.8% | 12.3% | 11.5% | 2.4% |
| 23 | 67.4% | 3.1% | 3.4% | 14.0% | 10.0% | 2.1% |

### Benchmark Orientation (all providers collapsed to 0.05 floor by round 12, except OpenCore)

### Incidents

| Round | Provider | Severity | Category |
|-------|----------|----------|----------|
| 1 | Orion Labs | minor | safety_failure |
| 4 | Orion Labs | critical | security_breach |
| 4 | Spark AI | moderate | security_breach |
| 12 | Apex AI | minor | healthcare_harm |
| 14 | Genesis | moderate | security_breach |
| 16 | Genesis | moderate | security_breach |

### Apex AI Safety Trajectory
Round 0: 0.550, Round 5: 0.654, Round 10: 0.782, Round 15: 0.960, Round 17: 1.000 (capped)

---

## Incident System Deep Dive

### Probability Formula
```
prob = (base_rate + history_addend) * safety_mult * exposure_mult * capability_mult * sanction_mult
```
- base_rate = 0.10
- history_addend = min(prior_major_critical * 0.04, 0.20)
- safety_mult = 1.0 - (safety_investment * 0.8)  -- portfolio allocation, NOT capability
- exposure_mult = (0.5 + market_share * 1.5) * sqrt(total_market_size)
- capability_mult = 0.8 + (safety_capability * 0.4)  -- higher safety = riskier deployment contexts
- sanction_mult = 0.75 if sanctioned, else 1.0
- Cap: 0.40

### Penalty Windows by Actor
| Actor | Window | Decay | Notes |
|-------|--------|-------|-------|
| Consumer satisfaction | 5 rounds | None (cliff-edge) | Full penalty within window, zero outside |
| Regulator incident_rate | 3 rounds | None | Severity-weighted sum |
| Regulator risk_beliefs | Permanent | 5%/round when no incidents | Ratchets up |
| Funder incident tracking | 3 rounds | None | Pruned each round |
| Media cumulative_incidents | Permanent | Resets on narrative recovery | Drives state machine |
| IncidentGenerator history | Permanent | Never pruned | Feeds history_addend |

### Key Issue: Safety Multiplier Uses Portfolio Allocation, Not Capability
The safety_multiplier term uses the portfolio `safety` fraction (investment decision), not `capability_vector["safety"]` (actual safety level). This means a provider investing 30% in safety gets multiplier 0.76, while one investing 8% gets 0.936. But the 30%-investor may have much higher actual safety capability. This creates a disconnect where the *decision to invest* matters more for incident probability than the *outcome of past investment*.

The capability_multiplier term does use actual safety capability, but counterintuitively makes higher-safety providers *more* incident-prone (0.8 + safety*0.4), modeling "deployed in riskier contexts." These two forces partially cancel out, leaving the net safety->incident relationship weaker than intended.
