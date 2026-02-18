# TODO: Future Enhancements

This document tracks planned improvements and features to be implemented later.

My additions:
1. double check that each actor in the ecosystem takes into account ecosystem public signals when making decisions. doesn't get pigeionholed into just their initial character profile.
2. VCs can also choose to invest in other. not bound to invest only in tech firms. no need to model this too deeply.
3. maybe make spacing of benchmarks depend on total number of rounds. rough guidelines: 50 rounds, 8 benchmarks
4. slow down saturation maybe. discuss ways to make benchmark introduction more realistic, without overloading the system.
5. lower initial_capability starting level for all model providers


---

## Known Edge Cases to Revisit

### Benchmark saturation — same-round simultaneous saturation

When two benchmarks saturate on the same round, the second one's replacement is delayed by `_saturation_cooldown + _saturation_min_gap = 2 + 1 = 3` rounds (after lowering min_gap to 1). This is just outside the 0-2 round target window.

**Root cause:** `consider_new_benchmark()` picks the first saturated benchmark via `break`, introduces it, updates `last_introduction_round`, and the second must wait for the `_saturation_min_gap` to pass.

**Potential fix:** Allow introducing two benchmarks in a single round when multiple saturate simultaneously. Would require returning a list instead of a single Benchmark, and updating the caller in `simulation.py`.

**Priority:** Low — simultaneous same-round saturation is an unlikely edge case. Revisit if it appears in experiment logs.

---

## Plotting Enhancements

### Priority: Medium - Cross-Feature Interactions

**1. Enhanced Provider Dashboard**

Add panels showing evaluator-as-company impact:
- **Panel: "Evaluation Advantage"**
  - Line plot: Providers with premium access highlighted
  - Show correlation between premium access and score jumps
  - Visual indicator when provider purchases access

- **Panel: "Investment vs Trials"**
  - Scatter: X=eval_engineering investment, Y=n_trials granted
  - Formula verification: n_trials = 1 + min(funding_bonus, eval_eng_bonus)
  - Shows who benefits from high eval engineering + premium access

**2. Enhanced Summary Dashboard**

Add metrics tiles:
- **Incident Summary Tile:**
  - Total incidents by severity
  - Most incident-prone provider
  - Critical incident count

- **Evaluator Business Tile (if enabled):**
  - Final budget
  - Number of premium providers
  - Average trial count
  - Revenue mix (funder vs provider %)

---

### Priority: Low - Advanced Analytics

**3. New Dashboard: `plot_ecosystem_dynamics_dashboard()`**

Comprehensive cross-actor interactions:
1. **Incident → Media → Consumer Flow**
   - Sankey diagram showing incident flow through ecosystem
   - Width = impact magnitude

2. **Evaluator Financial Sustainability**
   - Projection: Budget runway at current burn rate
   - Break-even analysis: base funding vs expenses

3. **Gaming Detection Performance**
   - ROC curve: How well actors detect gaming
   - Compare policymaker, funder, consumer detection accuracy

4. **Market Concentration & Incidents**
   - Time series: Market share concentration vs incident rate
   - Test if dominant providers have more incidents (scale effects)

---

## Testing Plan

**Unit Tests (future):**
1. Test each new plot function with synthetic data
2. Verify conditional rendering based on config flags
3. Test graceful handling of missing data (backward compatibility)
4. Validate color palettes for accessibility

**Integration Tests:**
1. Run experiment with both features enabled
2. Verify all dashboards render correctly
3. Check output file structure
4. Validate data extraction from `history` dict

**Visual Regression:**
1. Generate baseline plots
2. Compare after changes (pixel diff or hash)
3. Ensure consistent styling

---

## Documentation Updates Needed

**When implementing plots, update:**
1. `stakeholders.md` - Add plotting section for each feature
2. Function docstrings - Include example images or links
3. README plotting section - List all available dashboards
4. Experiment logs - Auto-include plot paths in summary

---

## Performance Considerations

**For large experiments (100+ rounds, 10+ providers):**
- Consider subsampling for scatter plots (every Nth point)
- Use aggregation for heatmaps (binning)
- Lazy rendering: Only create plots on demand
- Parallel dashboard generation (multiprocessing)

**Memory optimization:**
- Close figures after saving (`plt.close(fig)`)
- Don't hold all trial results in memory (stream from disk)
- Use sparse storage for incident data (only non-zero entries)

---

## Nice-to-Have Features

**Interactive Plots (Plotly/Bokeh):**
- Hover tooltips showing incident descriptions
- Zoomable timelines
- Linked brushing (select incident → highlight affected actors)
- Export to HTML for web viewing

**Animated Visualizations:**
- GIF/video showing ecosystem evolution over time
- Watch incidents propagate through actors
- Observe provider strategies adapting

**Comparative Dashboards:**
- Side-by-side: US vs EU regulatory style
- With/without evaluator-as-company
- Incident-enabled vs baseline

---

## Notes

- All visualizations should follow existing style (colors, fonts, layout)
- Use `get_provider_colors()` for consistent color schemes
- Add `if not data: return None` checks for robustness
- Include clear axis labels and legends
- Save at 150 DPI for publication quality
- Test with both heuristic and LLM mode experiments

---

## Infrastructure & Tooling Improvements

### Priority: High - Fix `run_llm_now.py`

**Status:** Likely broken, hasn't been used in a while

**Issues to investigate:**
1. **New config parameters not passed:**
   - `enable_incidents` flag
   - `evaluator_as_company` flag
   - `evaluator_base_budget`, `evaluator_premium_pricing`
   - `enable_media` flag
   - `use_case_profiles` parameter
   - `consumer_llm_mode` and related flags

2. **CLI argument coverage:**
   - Current args: `n_rounds`, `provider`, `verbose_llm`, `enable_ecosystem`, `save_traces`, `log_experiment`, `experiment_name`, `n_providers`, `n_benchmarks`, `enable_funders`
   - Missing: incidents, evaluator-as-company, media, policymaker config, consumer LLM mode

3. **Outdated assumptions:**
   - Hard-coded consumer count (6) - should use use_case_profiles
   - No support for realistic benchmark suites
   - No support for policymaker presets (US/EU styles)
   - Missing benchmark_sequence parameter

4. **Config building:**
   - `SimulationConfig()` call doesn't include new parameters
   - Consumer/policymaker/funder setup may be outdated
   - Need to sync with `run_experiment.py` structure

**Proposed fixes:**

```python
# Add new CLI arguments:
parser.add_argument("--incidents", action="store_true",
                   help="Enable incident reporting")
parser.add_argument("--eval-company", action="store_true",
                   help="Enable evaluator-as-company mode")
parser.add_argument("--eval-budget", type=float, default=100000.0,
                   help="Evaluator starting budget")
parser.add_argument("--media", action="store_true",
                   help="Enable media actor")
parser.add_argument("--policy-style", choices=["us_light_touch", "eu_precautionary", "balanced"],
                   help="Policymaker regulatory style")
parser.add_argument("--consumer-llm", action="store_true",
                   help="Enable LLM reasoning for organizational consumers")
```

```python
# Update SimulationConfig creation:
config = SimulationConfig(
    # ... existing params ...
    enable_incidents=args.incidents,
    evaluator_as_company=args.eval_company,
    evaluator_base_budget=args.eval_budget,
    evaluator_premium_pricing=10000.0,
    enable_media=args.media or enable_ecosystem,
    consumer_llm_mode=args.consumer_llm,
    consumer_llm_individuals=False,
    consumer_llm_organizations=args.consumer_llm,
    # ... etc
)
```

**Testing plan:**
1. Run basic test: `python run_llm_now.py -r 3 -p ollama`
2. Test with incidents: `python run_llm_now.py -r 5 --incidents --media`
3. Test eval-company: `python run_llm_now.py -r 5 --eval-company --funders`
4. Test full ecosystem: `python run_llm_now.py -r 10 -e --incidents --media --policy-style eu_precautionary`
5. Compare output to `run_experiment.py` to ensure parity

**Stretch goals:**
- Add `--preset` flag for common configurations (baseline, full-ecosystem, incidents-test)
- Add `--compare-to <exp_id>` to run side-by-side with past experiment
- Add `--dry-run` to show config without running

---

### Priority: Medium - Causal Mechanism Analysis Framework

**Goal:** Run two experiments with one controlled difference, then systematically analyze when/how/why they diverged.

**Use cases:**
- **Parameter sensitivity:** Does increasing safety investment reduce incidents?
- **Policy comparison:** US light-touch vs EU precautionary - where do outcomes differ?
- **Feature impact:** With vs without evaluator-as-company - how does it change provider behavior?
- **Counterfactual analysis:** What if OpenAI invested 40% in safety instead of 25%?

---

#### **Approach 1: Sequential Comparison (Current Method)**

Manual baseline: run two experiments, compare `summary.json` and plots side-by-side.

**Limitations:**
- Manual, time-consuming comparison
- Hard to pinpoint exact divergence moments
- No statistical framework for significance

---

#### **Approach 2: Automated Divergence Analysis** (Recommended)

**New tool: `compare_experiments.py`**

```python
"""
Compare two experiments and identify when/where they diverge.

Usage:
    python compare_experiments.py exp_030 exp_031
    python compare_experiments.py exp_030 exp_031 --diff-only
    python compare_experiments.py exp_030 exp_031 --metric incidents
"""

def compare_experiments(exp_a_id, exp_b_id):
    history_a = load_history(exp_a_id)
    history_b = load_history(exp_b_id)

    config_diff = compare_configs(exp_a, exp_b)

    for metric in TRACKED_METRICS:
        divergence_timeline = compute_divergence_timeline(history_a, history_b, metric)
        first_div_round = find_first_divergence(divergence_timeline, threshold=0.10)
        # ... record results

    attribution = attribute_divergence(history_a, history_b, config_diff)
    return {"config_diff": config_diff, "divergence_analysis": ..., "attribution": attribution}
```

**Implementation phases:**
1. Basic script: load two experiments, show config diff, plot side-by-side (~200 lines)
2. Divergence detection: compute difference timelines, find first divergence round (~150 lines)
3. Causal attribution: rule-based heuristics with confidence scoring (~200 lines)
4. Ensemble analysis: multiple seeds, statistical significance testing (~150 lines)
5. Live comparison: real-time divergence tracking, early stopping (~100 lines)

**Total estimate:** ~800 lines for full framework

---

#### **Approach 3: Differential Experiment Runner**

```python
def run_differential_experiment(base_config, param_to_vary, values):
    """Run multiple experiments varying a single parameter."""
    results = {}
    for value in values:
        config = base_config.copy()
        config[param_to_vary] = value
        sim = run_experiment(config)
        results[value] = sim.history
    comparison_report = compare_all_results(results, param_to_vary)
    plot_parameter_sweep(results, param_to_vary)
    return comparison_report
```

Usage example:
```python
run_differential_experiment(
    base_config=baseline,
    param_to_vary="benchmark_validity",
    values=[0.5, 0.6, 0.7, 0.8, 0.9]
)
```

---

**Testing scenarios:**

1. **Incident impact:** `enable_incidents=False` vs `True`
2. **Evaluator-as-company:** `evaluator_as_company=False` vs `True`
3. **Policy styles:** `us_light_touch` vs `eu_precautionary`
4. **Safety investment:** OpenAI `safety_alignment=0.25` vs `0.50`

---

**Last Updated:** 2026-02-17
