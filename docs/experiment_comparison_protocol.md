# Experiment Comparison Protocol

Instructions for efficiently comparing two simulation experiments. Written for Claude Code — less for human reading, more for AI efficiency.

---

## Step 0: Identify the Two Experiments

User will specify two experiment IDs (e.g., `exp_032_...`, `heur_009_...`). Experiments live in:

```
experiments/           # LLM-mode experiments (exp_XXX_name/)
experiments/heuristic/ # Heuristic-mode experiments (heur_XXX_name/)
```

If you're unsure which folder, use `Glob` on `experiments/**/summary.json` to find all.

---

## Step 1: Read summary.json First (Not game_log.md)

**The fastest and most complete data source is `summary.json`**, not `game_log.md`. Game logs are large (300-500KB) and slow to process. `summary.json` contains pre-aggregated final and mean values for everything you need.

Read both summaries in parallel:

```
Read: experiments/exp_A.../summary.json
Read: experiments/exp_B.../summary.json
```

`summary.json` contains:
- `n_rounds`
- `final_scores` — benchmark scores per provider (R29)
- `final_true_capabilities` — ground truth capabilities (R29)
- `final_strategies` — investment allocations (R29)
- `provider_summaries` — per-provider means over all rounds (capability growth, mean safety, mean eval_eng, etc.)
- `consumer_summary` — final satisfaction, market shares, switching rate, n_segments
- `policymaker_summary` — total interventions, intervention types, active regulations
- `funder_summary` — funding multipliers, funder types
- `validity_correlation` — overall benchmark quality
- `benchmark_params` — final benchmark validity/exploitability/noise

Also read both policymaker params in parallel (tiny files, no LLM cost):

```
Read: experiments/exp_A.../policymakers/Regulator/params.json
Read: experiments/exp_B.../policymakers/Regulator/params.json
```

---

## Step 2: Targeted rounds.jsonl Extraction (Use a Script, Not Read)

For time-series data (how metrics evolved over rounds), **do not read `rounds.jsonl` directly** — it can be 2-5MB. Instead, run a Python script via Bash:

```python
# Save to a temp file, e.g. C:\Users\yashd\AppData\Local\Temp\compare_exps.py
import json

def analyze(label, path):
    rounds = []
    with open(f"{path}\\rounds.jsonl") as f:
        for line in f:
            line = line.strip()
            if line:
                rounds.append(json.loads(line))

    print(f"\n=== {label} ===")
    print(f"Rounds: {len(rounds)}")

    # Incidents
    incidents = [{'round': r['round'], **inc} for r in rounds for inc in r.get('incidents', [])]
    by_sev = {}
    by_prov = {}
    for inc in incidents:
        by_sev[inc.get('severity', '?')] = by_sev.get(inc.get('severity', '?'), 0) + 1
        by_prov[inc.get('provider', '?')] = by_prov.get(inc.get('provider', '?'), 0) + 1
    print(f"Incidents: {len(incidents)} total | by severity: {by_sev} | by provider: {by_prov}")
    print(f"Incident rounds: {sorted(set(i['round'] for i in incidents))}")

    # Interventions
    interventions = [{'round': r['round'], **iv}
                     for r in rounds
                     for iv in r.get('policymaker_data', {}).get('interventions', [])]
    by_type = {}
    for iv in interventions:
        by_type[iv.get('type', '?')] = by_type.get(iv.get('type', '?'), 0) + 1
    targets = [iv.get('target', '') for iv in interventions if iv.get('target')]
    print(f"Interventions: {len(interventions)} | by type: {by_type} | targets: {targets}")
    print(f"Intervention rounds: {[iv['round'] for iv in interventions]}")

    # Strategy allocation over time (sampled)
    print("Strategy evolution (every 5 rounds):")
    for r in rounds[::5]:
        allocs = r.get('strategy_allocations', {})
        if allocs:
            n = len(allocs)
            avg_r = sum(v.get('fundamental_research', 0) for v in allocs.values()) / n
            avg_e = sum(v.get('evaluation_engineering', 0) for v in allocs.values()) / n
            avg_s = sum(v.get('safety_alignment', 0) for v in allocs.values()) / n
            print(f"  R{r['round']}: research={avg_r:.2f}, eval_eng={avg_e:.2f}, safety={avg_s:.2f}")

    # Consumer satisfaction over time (sampled)
    print("Consumer satisfaction (every 5 rounds):")
    for r in rounds[::5] + [rounds[-1]]:
        cd = r.get('consumer_data', {})
        sat = cd.get('avg_satisfaction', None)
        sw = cd.get('switching_rate', None)
        sat_s = f"{sat:.3f}" if isinstance(sat, float) else str(sat)
        sw_s = f"{sw:.3f}" if isinstance(sw, float) else str(sw)
        print(f"  R{r['round']}: sat={sat_s}, switching={sw_s}")

    # Policymaker risk beliefs over time (sampled)
    print("Max risk belief (every 5 rounds):")
    for r in rounds[::5]:
        pm = r.get('policymaker_data', {})
        risk = pm.get('risk_beliefs', {})
        if risk:
            max_risk = max(risk.values())
            print(f"  R{r['round']}: max_risk={max_risk:.3f} ({max(risk, key=risk.get)})")

    # Market shares final
    cd_last = rounds[-1].get('consumer_data', {})
    shares = cd_last.get('market_shares', {})
    print("Market shares (final):")
    for prov, share in sorted(shares.items(), key=lambda x: -x[1]):
        print(f"  {prov}: {share:.1%}")

    # Industry trust from policymaker data
    industry_trusts = [(r['round'], r.get('policymaker_data', {}).get('industry_trust', None))
                       for r in rounds if r.get('policymaker_data', {}).get('industry_trust') is not None]
    if industry_trusts:
        print(f"Industry trust: R0={industry_trusts[0][1]:.3f}, final={industry_trusts[-1][1]:.3f}")


base = r"C:\Users\yashd\Desktop\evaluation-ecosystem-simulation\experiments"
analyze("EXP_A (label)", f"{base}\\exp_A_name")
analyze("EXP_B (label)", f"{base}\\exp_B_name")
```

Run with:
```
python "C:\Users\yashd\AppData\Local\Temp\compare_exps.py"
```

Note: on Windows, use `python`, not `python3`. Quote the path.

---

## Step 3: Read game_log.md Only for Specific Events

`game_log.md` is useful for narrative context around a specific round — e.g., what the media said during a critical incident, what the leaderboard looked like at the moment of a mandate. Use it surgically:

```
Read: experiments/exp_A.../game_log.md  (offset=N, limit=60)
```

Estimate line offset: each round is roughly 30-60 lines. Round N starts around line N*45.

Do NOT read the full game_log.md unless explicitly asked.

---

## Step 4: Check policymaker/memory.json Only for Intervention Rationale

`memory.json` is large (~1800 lines for 30 rounds). Read only if the user wants detailed intervention reasoning (why each no_action was taken, what risk beliefs were). The rounds.jsonl script above captures the essential intervention data more efficiently.

If needed, read just the tail of memory.json to see final state:
```
Read: experiments/exp_A.../policymakers/Regulator/memory.json  (offset=1750, limit=50)
```

---

## Step 5: Use Parallel Agents for Independent Lookups

If collecting data from two experiments at the same time, launch two parallel `Explore` or `Bash` agents, one per experiment. Do not wait for one to finish before starting the other.

For a full comparison (both exps, all data), this order minimizes elapsed time:
1. **Parallel**: Read both `summary.json` files + both `params.json` files (4 reads in one message)
2. **Sequential**: Write and run the Python comparison script (needs both paths known first)
3. **Only if needed**: Targeted game_log.md reads for specific events

---

## Step 6: Key Metrics to Extract and Compare

For every comparison, always surface these metrics:

**Regulatory config:**
- intervention_threshold, risk_tolerance (from params.json)
- total_interventions, intervention_types (from summary.json policymaker_summary)

**Market outcomes:**
- final_market_shares per provider
- Which provider dominated; who declined vs recovered

**Provider performance:**
- final_true_capabilities per provider
- mean_safety_alignment per provider (from provider_summaries)
- mean_evaluation_engineering per provider

**Consumer:**
- final_satisfaction, mean_satisfaction
- avg_switching_rate

**Safety/risk events:**
- Total incidents, by severity, by provider
- Rounds with incidents (from script)
- Targets of emergency investigations (from script)

**Benchmark mandate:**
- Round it occurred, what triggered it
- Market share shift in the round after (look at game_log for that round if needed)

**Industry trust trajectory:**
- Start and end values (from script policymaker_data)

---

## Step 7: Hypothesis Verification Template

After collecting data, check these testable hypotheses (from US_vs_EU_Comparison_Guide.md):

1. **Incident count**: Does the precautionary style reduce incident count?
2. **Innovation/capability**: Does the light-touch style achieve higher final capabilities?
3. **Market concentration**: Which style leads to more concentration?
4. **Safety investment**: Does the precautionary style force more safety_alignment?
5. **Consumer satisfaction**: Does the precautionary style maintain higher satisfaction?

Mark each as CORRECT / WRONG / PARTIAL with the specific numbers.

---

## Common Pitfalls

- **game_log.md is too large to read wholesale.** Always use offset+limit or the script.
- **rounds.jsonl field names**: actual field names are `strategy_allocations` (not `strategies`), `consumer_data` (not `consumers`), `policymaker_data` (not `policymaker`). Verify against a single parsed line if unsure.
- **Heuristic vs LLM experiments**: heuristic experiments are in `experiments/heuristic/`, LLM-mode in `experiments/`. Check both locations.
- **JSON trailing commas**: if editing any index.json files, validate JSON after editing.
- **Path quoting on Windows**: always quote paths passed to python. Use `python "C:\path\to\script.py"`, not unquoted paths.
- **market_shares in rounds.jsonl**: lives at `consumer_data.market_shares`, not top-level.
- **policymaker_data.interventions**: list of dicts with keys `type`, `target`, `details`. `target` may be absent if the intervention is ecosystem-wide.

---

## Output Template

When writing up a comparison for the docs, follow the structure used in `US_vs_EU_Comparison_Guide.md` under "Empirical Results":

1. Setup (experiment IDs, scenario, shared conditions)
2. Regulatory Parameters table
3. Interventions table (round-by-round, side-by-side)
4. Incidents table (by severity)
5. Key event narrative (e.g., the benchmark mandate, any emergency investigations)
6. Market shares table (final)
7. Safety alignment table
8. Consumer satisfaction
9. True capabilities
10. Hypothesis verification table
11. Summary paragraph (3-5 sentences: what differed, what was counterintuitive, main takeaway)
