# Dynamic Consumer Market

> Design doc for two coupled mechanisms that make consumer market composition evolve over the simulation window. Last updated: 2026-04-09.
>
> **Status (2026-04-12):** Mechanism A (enterprise share growth) shipped in session 23 and is the default since session 27 (`dynamic_consumer_market: bool = True`). Mechanism B (technology-triggered need evolution) was scoped here but **not built** — sections 3 and the related sub-toggles (`enterprise_share_growth`, `need_evolution`) below are design record only. Ablation: `--condition static_enterprise_size` flips Mechanism A off.

---

## 1. Motivation

The current consumer market is static: segment fractions and need weights are set at init and never change. In reality, 2023-2025 saw two major shifts:

1. **Enterprise adoption surge.** Enterprise share of AI spending grew from ~25% (Q1 2023) to ~55% (mid-2025), driven by IT budget reallocations, compliance frameworks, and remote-work tooling consolidation (McKinsey State of AI 2025; Bain Enterprise AI 2025).
2. **Capability-triggered demand creation.** GPT-4-level coding unlocked coding demand in non-developer segments. Tool-use capabilities (mid-2024) created agentic demand that did not exist in early 2023. Capabilities create their own markets.

Both effects change what consumers want over time, which changes the demand signal providers face, which changes investment incentives. Without them, the simulation misses a key feedback loop: provider R&D -> capability thresholds -> demand shifts -> more R&D.

---

## 2. Mechanism A: Exogenous Enterprise Share Growth

### What changes

Each round, the share of total market allocated to organizational segments grows along a logistic curve, while individual segments shrink proportionally. `market_fraction` for all 48 segments is recomputed. Total still sums to 1.0.

### Logistic schedule

Enterprise share at round `t`:

```
enterprise_share(t) = start + (end - start) / (1 + exp(-k * (t - midpoint)))
```

where:
- `start = enterprise_share_start` (default 0.25)
- `end = enterprise_share_end` (default 0.55)
- `midpoint = enterprise_growth_midpoint` (default 18, i.e., round 18 ~ mid-2024)
- `k = 0.25` (steepness; derived from fitting the empirical anchors below)

Empirical calibration targets:

| Round | Calendar     | Target enterprise share |
|-------|-------------|------------------------|
| 0     | Q1 2023     | ~25%                   |
| 12    | Q1 2024     | ~35%                   |
| 24    | Q1 2025     | ~50%                   |
| 30    | Mid-2025    | ~55%                   |

### Rebalancing rule

Let `E(t)` = `enterprise_share(t)`. Let `I(t) = 1 - E(t)`.

For each organizational segment `s`:
```
s.market_fraction = s.base_fraction * (E(t) / E(0))
```

For each individual segment `s`:
```
s.market_fraction = s.base_fraction * (I(t) / I(0))
```

where `base_fraction` is the segment's fraction at init (round 0). This preserves relative proportions within each class (e.g., tech_startup stays 24% of enterprise, not 24% of total) while shifting the class-level split.

After rebalancing, renormalize all fractions to sum to exactly 1.0 (guards against float drift).

### Which segments are "enterprise"

A segment is enterprise if `USE_CASE_PROFILES[use_case]["consumer_type"] == "organization"`. Currently: `hospital_system`, `enterprise_finance`, `tech_startup`, `enterprise_legal`, `government_agency` (5 use cases x 3 archetypes = 15 segments).

---

## 3. Mechanism B: Technology-Triggered Need Evolution

### What changes

Segment `need_weights` evolve endogenously. When frontier capability in a dimension crosses a threshold, specified segments start upweighting that dimension. This models capability-driven demand creation.

### Frontier tracking

Each round, compute:
```
frontier[dim] = mean of top-3 providers' capability_vector[dim]
```

This is `mean_top_k_capability` with `k=3`, already available in the simulation's ground truth.

### Activation rules

Each rule specifies: dimension, threshold, and which segments are affected.

| Dimension | Threshold | Affected segments (use_case) | Rationale |
|-----------|-----------|-------------------------------|-----------|
| `agentic` | 0.45 | tech_startup, software_dev, customer_service, researcher | Tool-use capabilities unlock agentic workflows |
| `coding` | 0.50 | researcher, marketing, finance | Adjacent segments discover coding utility (data analysis, automation) |
| `safety` | 0.50 | hospital_system, enterprise_finance, enterprise_legal, government_agency | Regulatory compliance drives safety demand as capabilities mature |

Stored as `need_evolution_thresholds` in config:
```python
{
    "agentic": {"threshold": 0.45, "segments": ["tech_startup", "software_dev", "customer_service", "researcher"]},
    "coding":  {"threshold": 0.50, "segments": ["researcher", "marketing", "finance"]},
    "safety":  {"threshold": 0.50, "segments": ["hospital_system", "enterprise_finance", "enterprise_legal", "government_agency"]},
}
```

### Update rule

For each activated (dimension, segment) pair where `frontier[dim] > threshold`:

```
raw_shift = growth_rate * (frontier[dim] - threshold)
shift = min(raw_shift, max_shift)
```

Then for the segment's `need_weights`:
```
need_weights[dim] += shift
for other_dim in DIMENSIONS if other_dim != dim:
    need_weights[other_dim] -= shift * (need_weights[other_dim] / (1 - need_weights[dim] + shift))
```

Finally renormalize `need_weights` to sum to 1.0.

Parameters:
- `need_evolution_growth_rate`: 0.15 (controls magnitude; unitless multiplier)
- `need_evolution_max_shift`: 0.01 (max per-dimension per-round change)

The cap at 0.01/round means a dimension can grow by at most 0.30 over 30 rounds, which is large enough to matter but bounded enough to prevent instability.

### Proportional shrinkage

When dimension `d` grows by `shift`, all other dimensions shrink proportionally to their current weight. This preserves the relative ranking among non-activated dimensions. Edge case: if a dimension is already at 0.0, it cannot shrink further; the deficit is distributed among remaining nonzero dimensions.

---

## 4. Implementation Plan

### Files to touch

| File | Changes |
|------|---------|
| `src/simulation.py` | Add config params to `SimulationConfig`; call `update_market_composition()` at start of each round |
| `src/actors/consumer.py` | Add `update_market_composition()` method to `ConsumerMarket`; store `base_fractions` at init |
| `scripts/run_experiment.py` | Wire new config params through `extra_config` |

### Config parameters on `SimulationConfig`

Actually shipped (Mechanism A only):
```python
dynamic_consumer_market: bool = True   # default since session 27
enterprise_share_start: float = 0.25
enterprise_share_end: float = 0.55
enterprise_growth_midpoint: int = 18
```

Originally scoped but not built (Mechanism B sub-toggles + thresholds):
```python
# enterprise_share_growth: bool = True   # never added — Mechanism A is the only mechanism
# need_evolution: bool = True            # never added — Mechanism B not implemented
# need_evolution_thresholds: Optional[dict] = None
# need_evolution_growth_rate: float = 0.15
# need_evolution_max_shift: float = 0.01
```

`dynamic_consumer_market` is the gate for Mechanism A: True (default) enables enterprise share growth via the logistic curve; False (set by `static_enterprise_size` ablation) freezes shares at init.

### Method signatures on `ConsumerMarket`

```python
def update_market_composition(
    self,
    round_num: int,
    frontier_capabilities: dict[str, float],   # {dim: mean_top_k}
    config: "SimulationConfig",
) -> dict:
    """Recompute market_fractions (Mechanism A) and need_weights (Mechanism B).

    Returns dict of changes for logging:
        {"enterprise_share": float, "need_shifts": {segment: {dim: delta}}}
    """
```

Called from `simulation.py` at the top of each round, after market expansion but before `compute_satisfaction` and `compute_switching`.

### Init-time changes

`ConsumerMarket.__init__` stores `self._base_fractions = {seg.name: seg.market_fraction for seg in self.segments}` and `self._base_need_weights = {seg.name: dict(seg.need_weights) for seg in self.segments}` for use in rebalancing and diagnostics.

### Logging

The return dict from `update_market_composition` is merged into the round's `jsonl` record under key `"market_dynamics"`. This enables post-hoc analysis of when shifts occurred and their magnitude.

---

## 5. Interaction Effects

The two mechanisms are designed to interact:

- **Compound demand for agentic safety.** Mechanism A grows enterprise share (segments with high safety needs). Mechanism B can further increase safety weights in those same segments when safety capabilities mature. The compound effect: enterprise segments that already value safety at 0.30-0.48 see both their market weight and their safety need weight increase simultaneously.

- **Demand signal amplification.** When enterprise share grows (A), the aggregate demand vector across all segments tilts toward enterprise preferences (safety, reasoning, knowledge). If provider investment responds and pushes safety capability past 0.50 (triggering B), safety needs grow further. This creates a positive feedback loop that the simulation can capture.

- **Coding demand diversification.** Mechanism B's coding activation spreads coding demand beyond software_dev and tech_startup into researcher, marketing, and finance. Combined with Mechanism A's enterprise growth, this can create a broader base of coding demand that rewards general-purpose coding investment over narrow benchmark optimization.

- **Goodhart dynamics shift.** As need weights evolve, the gap between benchmark dimension weights and consumer need weights changes. A benchmark that was well-aligned in round 0 may become misaligned by round 20 if consumer needs have shifted. This creates dynamic Goodhart pressure that evolves over the simulation.

---

## 6. Calibration Notes

After first runs with the dynamic market enabled:

1. **Enterprise share curve fit.** Verify the logistic with `k=0.25`, `midpoint=18` actually hits the four calibration targets. Adjust `k` if the curve is too steep or too shallow. Plot `enterprise_share(t)` against targets.

2. **Need evolution timing.** Check when agentic threshold (0.45) and coding threshold (0.50) are first crossed. If they are crossed too early (before round 6) or too late (after round 24), the feature has no meaningful effect. Adjust thresholds based on observed capability trajectories from existing runs.

3. **Max shift sensitivity.** Run with `max_shift` at 0.005, 0.01, and 0.02 to check stability. At 0.02, a dimension can shift by 0.60 over 30 rounds, which may be excessive.

4. **Aggregate need vector.** Plot the market-weighted average need vector across all segments over time. It should show: (a) rising safety and reasoning weights from enterprise growth, (b) a visible bump in agentic needs around the threshold crossing, (c) smooth transitions without discontinuities.

5. **Score-satisfaction gap.** Compare gap trajectories with and without dynamic market. The dynamic market should increase the gap in mid-simulation (as demand shifts away from what benchmarks measure) and potentially decrease it late if providers adapt.

---

## 7. Ablation Design

As shipped (Mechanism A only), the ablation is a single binary toggle:

| Condition | `dynamic_consumer_market` | Purpose |
|-----------|--------------------------|---------|
| (default — any condition) | True  | Enterprise share grows ~25% → ~55% via logistic |
| `static_enterprise_size`  | False | Enterprise share frozen at init values (baseline check) |

Wire-in (already present in `run_experiment.py`):
```python
elif condition == "static_enterprise_size":
    extra_config["dynamic_consumer_market"] = False
```

Mechanism B's planned sub-ablations (`enterprise_only`, `needs_only`, `dynamic_full`) are not wired since Mechanism B was never built. If Mechanism B is implemented later, restore the original 4-row table.

Run each condition with the same seed set (30 seeds minimum) under the `balanced` regulatory preset. Compare:

- Market-weighted aggregate need vector trajectory
- Enterprise share trajectory (should be flat for `static_enterprise_size`)
- Per-dimension need weight evolution for key segments (software_dev, tech_startup, enterprise_finance)
- Score-satisfaction gap (mean across providers)
- Provider investment allocation shifts (do providers respond to changing demand?)
- Incident count (enterprise segments have higher safety needs; does dynamic market change incident impact?)
