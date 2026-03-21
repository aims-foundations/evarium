# Session Handoff — 2026-03-20

## Completed
- Went through all 11 open threads in `docs/stakeholders.md`; resolved 10 of 11 (thread 9 is a unified post-implementation calibration list)
- Consumer satisfaction formula: removed `safety_bonus`; defined `expected_quality` explicitly; incident penalty quadratic in market share `(1 + market_share²)`; media penalty scaled by `leaderboard_trust`
- Incident system: removed gaming gap factor; remaining 4 factors sufficient
- OS mechanics: `deployment_breadth` = OS market share directly; safety erosion formula linear and bounded; `broadcast_rate` (0.30) and `erosion_sensitivity` (0.50) hardcoded as constants
- Provider profiles: `specialization[dim]` initial values set for all providers (0.05–0.55 range)
- `benchmark_weight_confidence` dropped entirely; `learning_rate = 0.15` provides sufficient damping
- `product` lever: accumulates `product_stock` → `cost_advantage` → `cost_bonus`; switching cost / enterprise adoption extensions deferred
- Funder model redesigned: `funding_multiplier` replaced by additive budget model (`base_revenue_income + funder_allocations`); new `corporate` funder type added; per-funder vs per-provider cooldowns by type; scoring formulas differentiated by type; funders are amplifying not corrective (empirically grounded)
- `public_comms` mechanic: replaces `press_releases`; covers `rd`, `safety`, `product` post types; sampled proportionally from lever allocations with silence weight; at most 1 per provider per round; funders read directly
- Legacy attribute audit: `believed_provider_gaming`, `consumer_satisfaction` direct access, `exploitability`, `benchmark_params.validity` all flagged for removal at implementation time
- `docs/stakeholders.md` fully updated and internally consistent

## In Progress
- Nothing partially done

## Next Steps
1. **Implementation**: begin with file-by-file changes per implementation plan Section 14 order
2. **Thread 9 (post-implementation calibration)**: safety floor (est. 0.35), `revenue_per_share`, `funder_pool` sizes, media/regulator thresholds, `running_experienced_quality` init — all require early simulation runs
3. **Implementation fixes**: remove `believed_provider_gaming`, `consumer_satisfaction` direct access, `exploitability`, `benchmark_params.validity` from source files
4. **Rename**: `press_releases` → `public_comms` throughout all source files
