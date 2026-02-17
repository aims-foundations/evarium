# TODO: Future Enhancements

My additions:
1. double check benchmark saturation process. it seems like it takes a long time for benchmarks to be introduced.
2. Ran into this error while running on cluster: 
- Media dashboard saved
/lfs/skampere1/0/yashdave/evaluation-ecosystem-simulation/plotting.py:1842: UserWarning: set_ticklabels() should only be used with a fixed number of ticks, i.e. after set_ticks() or using a FixedLocator.
  ax6.set_xticklabels(provider_names, rotation=45, ha='right')
- Incident dashboard saved
this was with older version of code, verify if it is fixed after changes below.


This document tracks planned improvements and features to be implemented later.

---

## Plotting Enhancements for New Features

### Priority: High - Evaluator-as-Company Visualizations

**1. New Dashboard: `plot_evaluator_business_dashboard()`**
- **Purpose:** Visualize evaluator-as-company business metrics
- **Panels (3x2 layout):**
  1. **Budget Over Time**
     - Line plot: Total budget, base funding, service revenue
     - Track financial sustainability
     - Show benchmark creation costs as vertical markers (-$50K)

  2. **Premium Provider Timeline**
     - Timeline scatter: Which providers have premium access each round
     - Color by provider, marker size by funding level
     - Shows who's paying for advantage

  3. **Trial Counts by Provider**
     - Stacked bar chart per round showing n_trials per provider
     - Premium providers (2-5 trials) vs non-premium (1 trial)
     - Reveals best-of-N advantage distribution

  4. **Revenue Breakdown**
     - Stacked area chart: Base funding vs service revenue over time
     - Shows dependency on provider payments vs funder support
     - Pie chart inset showing funder type contributions (VC/Gov/Foundation)

  5. **Premium Access vs Performance**
     - Scatter: Premium access status vs score improvement
     - X-axis: Rounds with premium access
     - Y-axis: Score delta (current - previous)
     - Tests hypothesis: premium access → score inflation

  6. **Trial Result Distributions**
     - Box plots showing score distributions from N trials
     - Compare published score (max) vs trial mean/median
     - Reveals magnitude of best-of-N advantage

- **Data Requirements:**
  - `evaluator_business_metrics` from round_data
  - `evaluator_funding_data` from round_data
  - Provider `evaluator_premium_access` from private_state
  - `trial_results` from evaluator private_state

- **Implementation Notes:**
  - Only render if `evaluator_as_company=True` in config
  - Extract from `history[i]["evaluator_business_metrics"]`
  - Handle missing data gracefully (pre-feature experiments)
  - Add to `create_all_dashboards()` as conditional dashboard

---

### Priority: Medium - Incident Dashboard Enhancements

**2. Enhance Existing `plot_incident_dashboard()`**

**Current Panels (already implemented):**
- Incident Timeline by Provider
- Severity Distribution
- Category Breakdown
- Provider Safety vs Incident Rate
- Incidents per Round
- Provider Incident Comparison

**Proposed Additions (new panels or separate dashboard):**

1. **Safety Investment vs Incident Rate Correlation**
   - Scatter plot: X=average safety_alignment, Y=total incidents
   - Should show negative correlation (more safety → fewer incidents)
   - Color by provider, size by market share
   - Validates incident probability model

2. **Gaming Gap vs Incidents**
   - Scatter: X=gaming_gap (score - capability), Y=incident count
   - Tests hypothesis: gaming causes real-world failures
   - Include regression line to show trend

3. **Incident Impact Timeline**
   - Multi-line plot showing incident effects:
     - Consumer satisfaction drops (red)
     - Policymaker risk beliefs (orange)
     - Funder gaming beliefs (yellow)
     - Media sentiment (blue)
   - Vertical markers for incidents with severity color-coding
   - Shows ecosystem propagation visually

4. **Sector-Specific Incidents**
   - Heatmap: Rows=providers, Columns=sectors (healthcare, finance, etc.)
   - Cell color intensity = incident count in that sector
   - Reveals which providers cause harm in which domains

5. **Incident-Driven Interventions**
   - Timeline showing incidents (bottom) and policymaker interventions (top)
   - Connect critical incidents to emergency investigations with arrows
   - Shows regulatory response effectiveness

6. **Cumulative Incident Cost**
   - Line chart tracking cumulative "cost" of incidents
   - Weight by severity (minor=1, moderate=5, major=20, critical=100)
   - Compare across providers
   - Shows long-term safety track record

---

### Priority: Medium - Cross-Feature Interactions

**3. Enhanced Provider Dashboard**

Add panels showing evaluator-as-company impact:
- **Panel: "Evaluation Advantage"**
  - Line plot: Providers with premium access highlighted
  - Show correlation between premium access and score jumps
  - Visual indicator when provider purchases access

- **Panel: "Investment vs Trials"**
  - Scatter: X=eval_engineering investment, Y=n_trials granted
  - Formula verification: n_trials = 1 + min(funding_bonus, eval_eng_bonus)
  - Shows who benefits from high eval engineering + premium access

**4. Enhanced Summary Dashboard**

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

**5. New Dashboard: `plot_ecosystem_dynamics_dashboard()`**

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

## Data Extraction Helpers Needed

**New functions to add to plotting.py:**

```python
def extract_evaluator_business_metrics(history: list) -> dict:
    """Extract evaluator-as-company metrics from history."""
    # Returns: {rounds, budget, base_funding, service_revenue, premium_providers}
    pass

def extract_trial_counts(history: list) -> dict:
    """Extract n_trials per provider per round."""
    # Returns: {round: {provider: n_trials}}
    pass

def extract_incident_impacts(history: list) -> dict:
    """Extract incident cascade effects on other actors."""
    # Returns: {rounds, satisfaction_changes, risk_belief_changes, etc}
    pass

def compute_incident_severity_score(severity: str) -> int:
    """Convert severity to numeric score for aggregation."""
    # minor=1, moderate=5, major=20, critical=100
    pass
```

---

## Configuration & Integration

**Update `create_all_dashboards()`:**

```python
def create_all_dashboards(history, output_dir, show=False, metadata=None):
    # ... existing dashboards ...

    # Conditional: Evaluator Business Dashboard
    if metadata and metadata.get("evaluator_as_company"):
        fig = plot_evaluator_business_dashboard(history, show=False)
        if fig:
            path = f"{output_dir}/evaluator_business_dashboard.png"
            fig.savefig(path, dpi=150, bbox_inches='tight')
            plt.close(fig)
            saved['evaluator_business_dashboard'] = path
            print(f"  - Evaluator business dashboard saved")

    # Conditional: Enhanced incident analytics (if incidents enabled)
    if metadata and metadata.get("enable_incidents"):
        # Additional incident visualizations
        pass
```

**Metadata propagation:**
- Pass `SimulationConfig` fields to `create_all_dashboards()` via `metadata` dict
- Check `evaluator_as_company` and `enable_incidents` flags
- Only render relevant dashboards

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

## Priority Summary

**Implement Next:**
1. ✅ **Evaluator Business Dashboard** - Most visible new feature
2. 🔵 **Enhanced Incident Dashboard** - Add correlation/impact panels
3. 🟡 **Summary Dashboard Updates** - Quick metrics tiles
4. 🟢 **Data Extraction Helpers** - Foundation for other plots

**Later:**
- Advanced analytics dashboards
- Interactive visualizations
- Animated timelines
- Comparative experiments

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

4. **Config building (lines 96-180):**
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

### Priority: Medium - Improve `rerun_experiment.py`

**Current functionality:**
- Loads config from past experiment
- Re-runs simulation with same parameters
- Creates new experiment entry with "rerun_" prefix

**Issues & improvements:**

1. **Missing config parameters:**
   - Lines 112-134: `SimulationConfig()` construction
   - Missing: `enable_incidents`, `evaluator_as_company`, `evaluator_base_budget`, `evaluator_premium_pricing`, `enable_media`, `consumer_llm_mode`, `use_case_profiles`
   - Missing: `benchmark_introduction_cooldown`, `max_benchmarks`, `benchmark_sequence`
   - Missing: S-curve parameters if not in old configs

2. **Easier ways to handle config evolution:**

   **Option A: Dynamic config loading (recommended)**
   ```python
   def build_config_from_dict(config_dict):
       """Build SimulationConfig from dict, handling missing keys gracefully."""
       from dataclasses import fields
       from simulation import SimulationConfig

       # Get all valid SimulationConfig field names
       valid_fields = {f.name for f in fields(SimulationConfig)}

       # Filter config_dict to only valid fields (ignore provider_configs, etc.)
       filtered = {k: v for k, v in config_dict.items() if k in valid_fields}

       # Build config (uses dataclass defaults for missing fields)
       return SimulationConfig(**filtered)
   ```
   - **Pros:** Automatic forward compatibility, no manual field listing
   - **Cons:** May use unexpected defaults for new fields

   **Option B: Explicit field mapping with version tracking**
   ```python
   CONFIG_VERSION = 3  # Increment when breaking changes occur

   def migrate_config(config_dict):
       """Migrate old configs to current version."""
       version = config_dict.get("_config_version", 1)

       if version == 1:
           # Add v2 fields with defaults
           config_dict.setdefault("enable_incidents", False)
           config_dict.setdefault("evaluator_as_company", False)
           version = 2

       if version == 2:
           # Add v3 fields
           config_dict.setdefault("consumer_llm_mode", False)
           version = 3

       config_dict["_config_version"] = version
       return config_dict
   ```
   - **Pros:** Explicit, controlled upgrades; clear migration path
   - **Cons:** Requires maintenance for each version

   **Option C: Hybrid approach (best of both)**
   - Use Option A (dynamic) as base
   - Add warning system for deprecated/unknown fields
   - Log which defaults were used for transparency

3. **CLI improvements:**
   ```bash
   # Current:
   python rerun_experiment.py exp_016

   # Proposed additions:
   python rerun_experiment.py exp_016 --modify "enable_incidents=True"
   python rerun_experiment.py exp_016 --modify "n_rounds=50"  # Extend run
   python rerun_experiment.py exp_016 --seed 123  # Change seed for variation
   python rerun_experiment.py exp_016 --diff exp_020  # Show config differences
   python rerun_experiment.py exp_016 --fork  # Create variant, don't tag as rerun
   ```

4. **Validation & safety:**
   - Warn if rerunning with different code version (git commit hash)
   - Check if dependent features are enabled (e.g., eval-company needs funders)
   - Validate that all required configs are present

**Implementation priority:**
1. ✅ **Immediate:** Add missing config fields to lines 112-134 (manual patch)
2. 🔵 **Next sprint:** Implement Option C (dynamic + warnings)
3. 🟡 **Later:** Add CLI modification flags
4. 🟢 **Nice-to-have:** Config diffing and validation

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

**Workflow:**
```bash
# Run baseline
python run_experiment.py  # Saves to exp_030

# Modify config for treatment
# Edit run_experiment.py: SIMULATION["enable_incidents"] = True
python run_experiment.py  # Saves to exp_031

# Manual comparison
# Read exp_030/summary.json and exp_031/summary.json
# Look at plots side-by-side
# Try to identify divergence points
```

**Limitations:**
- Manual, time-consuming comparison
- Hard to pinpoint exact divergence moments
- Difficult to attribute causality (multiple things change each round)
- No statistical framework for significance

---

#### **Approach 2: Automated Divergence Analysis** ⭐ **RECOMMENDED**

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
    """Load two experiments and generate comprehensive comparison."""

    # Load histories
    history_a = load_history(exp_a_id)
    history_b = load_history(exp_b_id)

    # 1. CONFIG DIFF
    config_diff = compare_configs(exp_a, exp_b)
    # Shows exactly what changed between experiments

    # 2. TRAJECTORY COMPARISON
    divergence_analysis = {
        "first_divergence_round": None,
        "divergence_metrics": {},
        "attribution": {}
    }

    for metric in TRACKED_METRICS:
        # Compute divergence: |metric_a - metric_b| over time
        divergence_timeline = compute_divergence_timeline(
            history_a, history_b, metric
        )

        # Find first significant divergence (>10% difference)
        first_div_round = find_first_divergence(divergence_timeline, threshold=0.10)

        if first_div_round:
            divergence_analysis["divergence_metrics"][metric] = {
                "first_divergence_round": first_div_round,
                "peak_divergence": max(divergence_timeline),
                "final_divergence": divergence_timeline[-1],
                "trend": compute_trend(divergence_timeline),  # "increasing", "stable", "decreasing"
            }

    # 3. CAUSAL ATTRIBUTION (heuristic)
    # Try to attribute divergence to specific mechanisms
    attribution = attribute_divergence(history_a, history_b, config_diff)

    return {
        "config_diff": config_diff,
        "divergence_analysis": divergence_analysis,
        "attribution": attribution,
    }

def attribute_divergence(history_a, history_b, config_diff):
    """Heuristic causal attribution."""

    attribution = {}

    # Example: If incidents enabled and consumer satisfaction diverges
    if config_diff.get("enable_incidents") == (False, True):
        # Check if incidents occurred in exp_b
        incident_count_b = count_incidents(history_b)
        if incident_count_b > 0:
            # Check if satisfaction dropped after incidents
            satisfaction_drops = find_satisfaction_drops_after_incidents(history_b)
            if satisfaction_drops:
                attribution["consumer_satisfaction"] = {
                    "likely_cause": "incident_reporting_enabled",
                    "evidence": f"{incident_count_b} incidents caused satisfaction drops",
                    "confidence": "high" if len(satisfaction_drops) > 3 else "medium"
                }

    # Example: If evaluator-as-company enabled and score inflation diverges
    if config_diff.get("evaluator_as_company") == (False, True):
        # Check for premium access purchases
        premium_providers = get_premium_providers(history_b)
        if premium_providers:
            # Check if their scores increased more than non-premium
            score_advantage = compute_premium_score_advantage(history_b)
            if score_advantage > 0.05:
                attribution["score_inflation"] = {
                    "likely_cause": "best_of_N_submission",
                    "evidence": f"Premium providers had {score_advantage:.2%} score advantage",
                    "confidence": "high"
                }

    return attribution
```

**Output:**
```
================================================================================
EXPERIMENT COMPARISON
================================================================================

Baseline:     exp_030_baseline_no_incidents
Treatment:    exp_031_baseline_with_incidents

CONFIG DIFFERENCES:
  enable_incidents:    False → True

TRAJECTORY COMPARISON:
  First divergence detected at round 7

  Diverging metrics:
    consumer_satisfaction:
      - First divergence: Round 7 (-8.2% difference)
      - Peak divergence:   Round 15 (-15.3% difference)
      - Final divergence:  Round 25 (-12.1% difference)
      - Trend: Increasing divergence, stabilizes after round 20

    market_shares['OpenAI']:
      - First divergence: Round 9 (-3.1% difference)
      - Peak divergence:   Round 18 (-11.4% difference)
      - Final divergence:  Round 25 (-9.2% difference)
      - Trend: Increasing divergence

    policymaker_interventions:
      - First divergence: Round 11 (2 additional interventions in treatment)
      - Cumulative difference: +5 interventions by end

CAUSAL ATTRIBUTION:
  consumer_satisfaction divergence:
    Likely cause: incident_reporting_enabled
    Evidence:     12 moderate/major incidents caused satisfaction drops
    Confidence:   HIGH

  market_shares divergence:
    Likely cause: incident_impact_on_consumer_choice
    Evidence:     Providers with incidents lost market share
    Confidence:   MEDIUM (could also be indirect via media coverage)

VISUALIZATION:
  Plots saved to: experiments/comparison_exp030_vs_exp031/
    - divergence_timeline.png (all metrics over time)
    - satisfaction_comparison.png
    - market_share_comparison.png
    - incident_impact_analysis.png

================================================================================
```

**Implementation components:**

1. **Metric tracking:**
   ```python
   TRACKED_METRICS = [
       "scores",  # Per-provider benchmark scores
       "true_capabilities",  # Ground truth capability
       "consumer_satisfaction",  # Average satisfaction
       "market_shares",  # Per-provider market share
       "policymaker_interventions",  # Count of interventions
       "funder_allocations",  # Funding distribution
       "media_sentiment",  # Media coverage sentiment
       "incidents",  # Incident counts and severity
       "evaluator_budget",  # Evaluator financial state (if applicable)
       # ... add more as needed
   ]
   ```

2. **Divergence detection:**
   ```python
   def find_first_divergence(timeline, threshold=0.10):
       """Find first round where difference exceeds threshold."""
       for round_num, diff in enumerate(timeline):
           if abs(diff) > threshold:
               return round_num
       return None
   ```

3. **Visualization:**
   ```python
   def plot_divergence_analysis(history_a, history_b, metric, save_path):
       """Create divergence visualization with annotations."""
       fig, axes = plt.subplots(2, 1, figsize=(14, 8))

       # Top panel: Both trajectories
       ax1 = axes[0]
       plot_metric_trajectory(ax1, history_a, metric, label="Baseline", color="blue")
       plot_metric_trajectory(ax1, history_b, metric, label="Treatment", color="orange")
       annotate_first_divergence(ax1, first_div_round)

       # Bottom panel: Difference over time
       ax2 = axes[1]
       diff_timeline = compute_difference_timeline(history_a, history_b, metric)
       ax2.plot(diff_timeline, color="red", linewidth=2)
       ax2.axhline(y=0, color='black', linestyle='--', alpha=0.3)
       ax2.fill_between(range(len(diff_timeline)), 0, diff_timeline, alpha=0.3)
   ```

---

#### **Approach 3: Ensemble Analysis (Multiple Seeds)**

For more robust causal claims:

```python
def run_ensemble_comparison(
    baseline_config,
    treatment_config,
    n_seeds=10,
    parallel=True
):
    """Run multiple experiments with different seeds for statistical power."""

    baseline_results = []
    treatment_results = []

    for seed in range(n_seeds):
        baseline_config["seed"] = seed
        treatment_config["seed"] = seed

        baseline_sim = run_experiment(baseline_config)
        treatment_sim = run_experiment(treatment_config)

        baseline_results.append(extract_metrics(baseline_sim.history))
        treatment_results.append(extract_metrics(treatment_sim.history))

    # Statistical analysis
    comparison = {
        "mean_difference": {},
        "std_difference": {},
        "p_values": {},  # T-test for significance
    }

    for metric in TRACKED_METRICS:
        baseline_values = [r[metric] for r in baseline_results]
        treatment_values = [r[metric] for r in treatment_results]

        comparison["mean_difference"][metric] = np.mean(treatment_values) - np.mean(baseline_values)
        comparison["std_difference"][metric] = np.std(treatment_values - baseline_values)
        comparison["p_values"][metric] = scipy.stats.ttest_ind(baseline_values, treatment_values).pvalue

    return comparison
```

**Use case:** "Does enabling incidents significantly reduce consumer satisfaction?"
- Run 10 baseline experiments (incidents=False)
- Run 10 treatment experiments (incidents=True)
- Compute mean consumer satisfaction in final round
- T-test: Is the difference statistically significant (p < 0.05)?

---

#### **Approach 4: Live Divergence Tracking (Advanced)**

Track divergence in real-time during simulation:

```python
class LiveComparator:
    """Compare experiment to baseline in real-time."""

    def __init__(self, baseline_history):
        self.baseline = baseline_history
        self.current_round = 0

    def on_round_complete(self, round_data):
        """Called after each round completes."""
        baseline_round = self.baseline[self.current_round]

        # Compare key metrics
        divergence = {}
        for metric in TRACKED_METRICS:
            diff = compute_difference(round_data[metric], baseline_round[metric])
            divergence[metric] = diff

        # Alert if significant divergence detected
        if max(divergence.values()) > 0.15:
            print(f"⚠️  DIVERGENCE ALERT at round {self.current_round}")
            print(f"   Largest difference: {max(divergence, key=divergence.get)}")

        self.current_round += 1
```

**Use case:** Stop early if experiment is replicating baseline (save compute time).

---

#### **Implementation Priority:**

1. ✅ **Phase 1:** Basic `compare_experiments.py` script
   - Load two experiments
   - Show config diff
   - Plot side-by-side trajectories
   - ~200 lines of code

2. 🔵 **Phase 2:** Divergence detection
   - Compute difference timelines
   - Find first divergence round
   - Annotate plots with divergence points
   - ~150 lines

3. 🟡 **Phase 3:** Causal attribution (heuristic)
   - Rule-based attribution for known mechanisms
   - Confidence scoring
   - ~200 lines

4. 🟢 **Phase 4:** Ensemble analysis (multiple seeds)
   - Parallel experiment running
   - Statistical significance testing
   - ~150 lines

5. 🟢 **Phase 5:** Live comparison (advanced)
   - Real-time divergence tracking
   - Early stopping criteria
   - ~100 lines

**Total estimate:** ~800 lines for full framework

---

**Testing scenarios:**

1. **Incident impact:**
   - Baseline: `enable_incidents=False`
   - Treatment: `enable_incidents=True`
   - **Expected:** Consumer satisfaction drops when incidents occur; providers with low safety see more incidents

2. **Evaluator-as-company:**
   - Baseline: `evaluator_as_company=False`
   - Treatment: `evaluator_as_company=True`
   - **Expected:** Premium providers get higher scores; evaluator budget grows; gaming advantage visible

3. **Policy styles:**
   - Baseline: `policymaker_philosophy="us_light_touch"`
   - Treatment: `policymaker_philosophy="eu_precautionary"`
   - **Expected:** EU has fewer incidents but slower capability growth; US has more incidents but faster innovation

4. **Safety investment:**
   - Baseline: OpenAI `safety_alignment=0.25`
   - Treatment: OpenAI `safety_alignment=0.50`
   - **Expected:** Fewer incidents for OpenAI; possible market share changes; different policymaker attention

---

**Alternative: Differential experiment runner**

Instead of running sequentially, run both in one script:

```python
def run_differential_experiment(base_config, param_to_vary, values):
    """Run multiple experiments varying a single parameter."""
    results = {}

    for value in values:
        config = base_config.copy()
        config[param_to_vary] = value

        sim = run_experiment(config)
        results[value] = sim.history

    # Auto-generate comparison
    comparison_report = compare_all_results(results, param_to_vary)
    plot_parameter_sweep(results, param_to_vary)

    return comparison_report
```

Usage:
```python
run_differential_experiment(
    base_config=baseline,
    param_to_vary="benchmark_validity",
    values=[0.5, 0.6, 0.7, 0.8, 0.9]
)
# Outputs: How does benchmark validity affect gaming behavior?
```

---

**Last Updated:** 2026-02-16
**Status:** Planning phase - no plots implemented yet for evaluator-as-company
**Incident Dashboard:** ✅ Already implemented (excellent baseline)
