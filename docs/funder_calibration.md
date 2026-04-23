# Funder Calibration

## Purpose

Records calibrations of funder parameters against empirical data on the AI model-provider ecosystem. Current values, landed values, source anchors, and reasoning (especially the aggregation factor and availability curve) live here so future recalibrations can rebuild on traceable ground.

## Source data

- `docs/ai_corporate_funder_research.md` — timeline of corporate funding events in the frontier AI ecosystem, 2020 through April 2026. Compiled from press reports, SEC filings, and CMA/FTC inquiry documents.

## Timescale convention

1 simulation round = 1 calendar month. All cadence values below translate directly.

## Aggregation factor

The sim uses a small roster of representative funders to stand in for a much larger real population. Aggregation ratios shape both cadence and capital sizes:

| Type | Real active entities | Sim roster | Aggregation |
|---|---|---|---|
| VC | ~15–20 (a16z, Sequoia, Thrive, Tiger, Khosla, Founders Fund, General Catalyst, Lightspeed, Iconiq, Coatue, etc.) | 2 (TechVentures, Horizon_Capital) | ~2:1 on lead-VC firings |
| Corporate | ~8 (MS, Amazon, Google, Nvidia, Oracle, Salesforce, Cisco, AMD/IBM/Samsung/sovereigns) | 2 (StratCorp_AI, IndustryPartners_AI) | 4:1 |
| Gov | ~5 (UK AISI, US AISI, NIST, EU AI Office, sovereign quasi-gov) | 1 (AISI_Fund) | 5:1 |
| Foundation | ~3 active at scale (Open Philanthropy primarily) | 1 (OpenResearch_Foundation) | 3:1 |

Per-provider event rates observed in the research anchor cadences:

- **Anthropic** receives a corporate event every ~4 months (8 events across 31 months, 2023–2026).
- **OpenAI** receives a corporate event every ~3–4 months.
- Frontier labs receive VC-led round events every ~8 months.
- Gov direct funding to specific labs is rare — every ~24 months per provider.
- Foundation funding events per provider: ~18 months.

Dividing per-provider event rate by sim-rep count gives per-sim-rep cadence, which drives `funding_cooldown` calibration below.

## Parameters

### 1. `funding_cooldown` (per-funder decision cadence)

After a funder makes an allocation decision, it reuses the prior allocation for `funding_cooldown` rounds before re-deriving from the scoring formula. Short-circuit logic in `Funder.plan()` at `src/actors/funder.py`.

| Funder | Type | Previous | Landed | Anchor |
|---|---|---|---|---|
| TechVentures | vc | 3 | **4** | ~8mo VC-event rate ÷ 2 sim reps ≈ 4 |
| Horizon_Capital | vc | 2 | **4** | Same anchor |
| StratCorp_AI | corporate | 3 | **7** | ~4mo corporate-event rate ÷ 2 sim reps ≈ 7–8 |
| IndustryPartners_AI (new) | corporate | — | **7** | Same anchor |
| AISI_Fund | gov | 4 | **10** | Annual appropriation cycles; per-provider events rarer than annual but sim cooldown shouldn't exceed decision-window plausibility |
| OpenResearch_Foundation | foundation | 3 | **6** | Board-review cycle; ~18mo per-provider events ÷ 3:1 aggregation ≈ 6 |

Gov and foundation anchors are looser than VC/corporate — per-provider event data for direct gov/foundation funding is thin. Educated estimates, flagged as less-hard calibration.

### 2. Per-provider rotation rule (corporate type only) — DELETED

Original logic: after allocating to provider P, skip P for the next 3 rounds (previously at `funder.py:_plan_corporate`).

**Deleted.** No empirical support. The research documents zero strategic exits by corporate funders across the 5-year window (2020–April 2026); no pattern resembling rotation. Within aggregated funders, composition turns over but aggregate stake does not drop to zero on any provider that has been committed to.

Replacement behavior: corporate funders re-evaluate their top 2–4 partners each decision round using the scoring formula, with no artificial exclusion.

### 3. Representative corporate funder count

Previous: 1 (StratCorp_AI). Landed: 2 (added IndustryPartners_AI).

**Rationale:** The aggregation factor in the cooldown table assumes 2 representative corporates. A single corporate funder would aggregate ~8 real corporates at 8:1, collapsing all corporate-to-provider cadence into one firing and losing the ability to observe multi-corporate dynamics (one funder ratcheting up while another holds steady). 2 is the minimum roster for the aggregation math to work cleanly.

Naming is deliberately generic — no pre-assignment of provider partnerships or hyperscaler-identity. Partnerships emerge from scoring + allocation decisions.

### 4. Funder capital sizes (empirical-first splits)

`total_capital` is now interpreted as the funder's intended sum of capital deployment across the full 40-round sim window. Values anchor to the research's aggregate disclosed capital into frontier labs (~$198B over 40 months, 2023–2026).

Splits by sim-funder share of that aggregate:

| Funder | Type | Previous | Landed | Share of $198B |
|---|---|---|---|---|
| TechVentures | vc | $2.0B | **$30B** | 15% |
| Horizon_Capital | vc | $1.0B | **$20B** | 10% |
| StratCorp_AI | corporate | $1.5B | **$65B** | 33% |
| IndustryPartners_AI | corporate | — | **$65B** | 33% |
| AISI_Fund | gov | $500M | **$10B** | 5% |
| OpenResearch_Foundation | foundation | $500M | **$3B** | 2% |
| **Total** | | $5.5B | **$193B** | 98% of $198B aggregate |

Corporate dominates (66% of deployment) matching the real 2024–2026 distribution. VC a distant second. Gov/foundation small. This contradicts the previous `stakeholders.md` assumption of a "relatively inelastic" pool — see §5 and §6 for the availability mechanism that makes the scale change work without breaking capability-growth calibration.

### 5. Availability curve

`total_capital` is released across the sim via a geometric availability function:

```
availability(r) = (1 + g)^r / Σ_{i=0}^{N-1} (1+g)^i
```

Where `g = capital_growth_rate = 0.07` (7%/month compounded) and `N = sim_total_rounds` (= `SimulationConfig.n_rounds`).

Per-decision deployment: `max_round_deployment × availability(r) × total_capital`.

**Empirical anchor for g = 0.07:**

| Year | Aggregate corporate equity into frontier labs | YoY |
|---|---|---|
| 2023 | ~$14B | — |
| 2024 | ~$32B | 2.3× |
| 2025 | ~$80–100B | 2.5–3.1× |
| 2026 (Jan–Apr annualized) | ~$185B–$550B | ~2.3× |

YoY growth ~2.3–2.5× corresponds to monthly compound ~7%. Over 40 rounds, availability ramps from 0.5% at round 0 to 7% at round 39 — a ~14× range. This gives early-vs-late variance in capital inflow that mirrors the real ecosystem's maturation.

**Shared across funder types** (not per-type). Per-type rates are defensible (corporate ~7%, VC ~5%, gov ~2%, foundation ~1%) but add three parameters. The shared 7% is a reasonable first pass; per-type differentiation flagged as future refinement if the paper wants heterogeneous funder growth.

**Round-0 behavior.** Availability at round 0 is 0.5% of total — very small. Early sim deploys much less capital than late sim. Real history has MSFT-OpenAI $10B in Jan 2023 as a discrete event on month 1, which the geometric curve understates. Accepted for parsimony: the purpose is to model the *shape* of growth, not match any single real event exactly.

### 6. Downstream: provider R&D budgets

Funder allocations enter provider budgets via:

```
rd_budget_raw = base_revenue + funder_contribution × FUNDER_BUDGET_SCALE
capability_gain ∝ sqrt(rd_budget_raw) × rnd_efficiency
```

`FUNDER_BUDGET_SCALE = 1e-9` (`src/simulation.py:33`) converts display-dollars to sim budget units.

**Scale jump does not require rescaling `FUNDER_BUDGET_SCALE`.**

Reasoning: under cooldown-reuse semantics, `active_funding` at round r = most recent decision's allocation. The decision's allocation is `max_round_deployment × availability(r_decision) × total_capital`. At sim midpoint (round 20), availability ≈ 1/N (mean), so mean allocation ≈ `max_round_deployment × total_capital / N`. For StratCorp with total_capital=$65B, N=40, max_deploy=0.12, this gives ~$195M — nearly identical to the prior regime's per-decision $180M.

So mean rd_budget contribution is preserved; early-vs-late variance opens up:

| Round | avail(r) | Funder contribution (relative to previous regime) | sqrt(rd_budget) (relative) |
|---|---|---|---|
| 0 | 0.50% | ~0.20× | ~0.45× |
| 20 | 1.94% | ~0.78× | ~0.88× |
| 39 | 7.01% | ~2.80× | ~1.67× |

Capability gains vary ~3.7× from early to late sim. Mean preserved, variance reflecting ecosystem growth.

**Non-uniform across funder types.** Mean preservation is exact only for StratCorp/IndustryPartners (total_capital ≈ 43× previous). VC/gov/foundation got smaller multiples (TechVentures 15×, Horizon 20×, AISI 20×, OpenResearch 6×), so their mid-sim contribution is **below** the previous regime (0.37×, 0.50×, 0.50×, 0.15× respectively). Providers previously funded primarily by VC/gov/foundation will see reduced capability-growth contribution from those channels, partially compensated by sqrt damping and late-sim amplification. This matches the empirical reality where corporate capital dwarfs all other types by 2025.

### 7. Things that are NOT changing

- **`rnd_efficiency`** — mean rd_budget preserved at midpoint, efficiency untouched.
- **`rd_budget_floor` (OS providers)** — in sim units, independent of FUNDER_BUDGET_SCALE. Untouched.
- **`revenue_per_share`, `cost_advantage`** — revenue-side mechanics. Untouched.
- **`max_round_deployment`** — kept at prior values per funder; it now gates fraction of active-this-round, not fraction of total pool.
- **`FUNDER_BUDGET_SCALE`** — kept at 1e-9. See §6.

## Deferred mechanics

### Asymmetric floor ratchet (not implemented)

Proposed primitive: once allocation to provider P has been held above a threshold for N consecutive rounds, a fraction of peak allocation becomes a floor the formula cannot drop below.

**Deferred.** Individual-corporate divestments are near-zero in the data, but within-aggregate composition turns over (Oracle exits Cohere; CoreWeave enters OpenAI). A floor on aggregate allocation is a population-level claim that individual-corporate data doesn't cleanly support. Calibration parameters (N, floor fraction, release conditions) lack clean empirical anchors at the aggregation level.

### Reciprocal compute flow (not implemented)

Proposed primitive: corporate funder allocations create reciprocal compute-spend obligations from the funded provider back to the funder, mirroring the 3–20× compute-to-equity multipliers documented in the research (e.g., Microsoft-OpenAI equity ~$14B vs committed Azure spend ~$250B).

**Deferred.** Collapsing Microsoft + Nvidia + Oracle into one sim-corporate aggregates real corporates whose compute relationships differ fundamentally (cloud vs chip supply vs infrastructure). The "compute share" primitive is per-real-corporate; assigning it to a representative is an arbitrary modeling choice without clean calibration.

Revisit if/when the paper wants compute-concentration dynamics as a mechanical primitive rather than an LLM-prompt-side inference.

## Open threads for future calibration

- **Per-type growth rates** — current regime is shared `g=0.07`. Real corporate grew faster than VC/gov/foundation. Per-type rates would add three parameters but capture differential maturation.
- **Round-0 under-shoot** — geometric curve starts very low. Piecewise matching to actual annual aggregates would fit better but adds complexity.
- **Sovereign-corporate tier** (MGX, QIA, PSP, HOOPP) — absent from the sim's type system. By 2026 these appear in ≥3 frontier cap tables each.
- **Reverse acqui-hire as provider exit** (Inflection → Microsoft, Adept → Amazon, Character.AI → Google, Scale → Meta). Sim has no provider exit mechanism; this is a documented real-world exit class.
- **Announcement vs deployment gap** — 20–50% headline-to-confirmed discount per research. Sim treats allocations as immediately effective.
- **China–US segmentation** — no cross-border strategic capital into Chinese labs since 2023. Sim is not geographically split.
- **Circular chip deals** (Nvidia–OpenAI LOI, AMD–OpenAI reversed warrants, xAI SPV). Emergent structural class not modeled.

## Revision history

- **2026-04-22** — Initial doc. Cooldown recalibration + corporate per-provider rotation rule deletion + second corporate funder added. LLM funder allocation renormalization bug fix (`src/llm.py`: scale-down only, never scale up). Availability-curve mechanism added (geometric `g=0.07`, shared across types); `total_capital` re-anchored to empirical $198B ecosystem integral with empirical-first splits. `FUNDER_BUDGET_SCALE` left at 1e-9 (mean-preserving by construction). Source: `ai_corporate_funder_research.md`.
