# Round Ordering: Proposal and Analysis

## Current Execution Order

Within each round of `run_round()` (simulation.py:811-1489), actors execute in a fixed sequence:

```
1. Providers plan & execute capability gains    (line 861)
2. Evaluator scores all providers               (line 989)
3. Scores published, leaderboard created        (line 1050)
4. Providers observe scores & update beliefs     (line 1054)
5. Incidents generated                          (line 1141)
6. Media observes & publishes                   (line 1214)
7. Consumers observe & switch                   (line 1238)
8. Regulators observe & intervene               (line 1246)
9. Funders observe & allocate                   (line 1254)
10. Round data recorded                         (line 1275)
```

Within each phase, actors iterate in list order (e.g., providers iterate in config order: Orion, Apex, Genesis, Mirage, OpenCore, Spark).

## What Could Be Shuffled?

### Between-phase ordering (the 10 steps above)

**Not worth shuffling.** These phases have genuine causal dependencies:
- Providers must invest before evaluator can score
- Scores must exist before anyone can observe them
- Consumers need media coverage to inform switching
- Funders need regulator actions to inform allocations

Shuffling phases would break the information flow or create impossible observations (e.g., consumers reacting to scores that haven't been computed yet). The current ordering represents a natural causal chain.

### Within-phase ordering (which provider goes first, which funder goes first)

**This is the real question.** Two phases have potential ordering effects:

#### A. Provider planning (phase 1)
Providers plan independently — they don't observe each other's current-round plans. Each provider's `plan()` call uses previous-round public state. Ground truth capability updates happen as each provider executes, but the evaluator doesn't score until all providers are done.

**Ordering effect: NONE.** Provider plans are independent; all use the same stale (previous-round) state. No provider sees another's current-round decision before making its own.

#### B. Funder allocation (phase 9)
Funders observe `other_funders_allocations` — meaning later funders see what earlier funders allocated this round. This creates a genuine first-mover asymmetry:
- The first funder (TechVentures) decides with no knowledge of other allocations
- The last funder (OpenResearch_Foundation) sees all prior allocations

**Ordering effect: MODERATE.** In LLM mode, later funders can react to earlier funders' moves (e.g., "TechVentures already gave Orion $50M, so I'll diversify elsewhere"). This is arguably realistic (funding rounds have temporal sequencing), but the fixed ordering means the same funder always moves first.

#### C. Regulator actions (phase 8)
Only one regulator in the current config, so ordering is irrelevant. If multiple regulators were added (e.g., US + EU), their ordering would matter.

## Expected Impact of Shuffling

### If we shuffle funder order each round:

**Expected changes:**
- More uniform funding distribution across providers (no funder consistently gets first-mover advantage)
- Slightly higher variance in per-round allocations
- Reduced risk of funder herding (where later funders pile onto early leader's pick)

**Magnitude estimate:** Small. Funders already have different types (VC, corporate, gov, foundation) with distinct scoring functions. The within-round information advantage is one signal among many (scores, market share, media sentiment, incidents). Shuffling would reduce a second-order effect.

### If we shuffle provider order (within phase 1):

**Expected changes:** None. Providers plan independently using previous-round state. Shuffling is a no-op for the current architecture.

### If we shuffle the observer phase (phase 4):

**Expected changes:** Minimal. Providers observe independently. OS belief broadcast (line 1109-1139) does iterate over providers, but the broadcast target's beliefs are nudged regardless of iteration order because each broadcast is independent.

## Recommendation

**Not worth implementing now.** The reasoning:

1. **The main ordering bias is in funder allocation**, which is a second-order effect on a second-order actor. Funder allocations affect provider R&D budgets, which affect capability gains, which affect scores — three steps removed from the primary dynamics we're studying (gaming, market concentration, evaluation quality).

2. **Fixed funder ordering is arguably realistic.** In real markets, funding rounds are sequential — some investors move first (lead investors), others follow. The current ordering simulates this naturally.

3. **Implementation cost is low but validation cost is high.** Adding `random.shuffle(self.funders)` is trivial, but proving it matters requires re-running the full heuristic baseline (27 conditions x 30 seeds) to compare. That's a significant compute commitment for a small expected effect.

4. **The paper doesn't claim ordering-independence.** We'd need to either claim it doesn't matter (requiring ablation evidence) or acknowledge it as a limitation (one sentence in the paper). The latter is cheaper.

### If we do implement it later

The implementation is minimal:
- Add `shuffle_actor_order: bool = False` to SimulationConfig
- In `_run_funder_round()`, shuffle `self.funders` list before iteration
- Run 5-seed paired comparison (CRN) to measure effect size on HHI, funding concentration, and capability variance
- If effect size < 2% on primary metrics, document as negligible and default to True for robustness

**Estimated effort:** 30 minutes implementation + 2 hours compute for CRN comparison.
