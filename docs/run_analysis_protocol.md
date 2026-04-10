# Single Run Analysis Protocol

When asked to analyze a run, follow this protocol in order. Use `python` (not `python3`) on Windows.

## 1. Locate and inventory the run directory

```
ls '<run_dir>/'
```

Expected files: `config.json`, `metadata.json`, `summary.json`, `rounds.jsonl`, `game_log.md`, `history.json`, `ground_truth.json`, plus directories `plots/`, `providers/`, `consumers/`, `funders/`, `regulators/`.

## 2. Read metadata and summary first

Read these three files directly (they are small):
- `metadata.json` — seed, llm_mode, created_at, git_commit, description
- `summary.json` — final scores, final capability vectors, final strategies, leaderboard, consumer/regulator/funder summaries, validity_correlation
- `config.json` — n_rounds, provider_configs, funder_configs, regulator_configs, feature flags

Count completed rounds:
```
wc -l '<run_dir>/rounds.jsonl'
```

## 3. Extract trajectories from rounds.jsonl

### rounds.jsonl schema

Each line is a JSON object with these top-level keys:

| Key | Type | Description |
|-----|------|-------------|
| `round` | int | Round number (0-indexed) |
| `scores` | dict[provider -> float] | Composite benchmark scores |
| `capability_vectors` | dict[provider -> dict[dim -> float]] | True capability per dimension |
| `strategies` | dict[provider -> dict] | Target/requested portfolio (rd, safety, product) |
| `effective_strategies` | dict[provider -> dict] | **Actual** portfolio after smoothing (USE THIS) |
| `benchmark_orientations` | dict[provider -> float] | Benchmark orientation level (0-1) |
| `product_data` | dict[provider -> dict] | Product investment effects |
| `open_source_data` | dict[provider -> dict] | Open-source specific data |
| `benchmark_params` | dict[benchmark -> dict] | Active benchmark parameters |
| `benchmark_dimension_weights` | dict[benchmark -> dict] | What each benchmark measures |
| `total_market_size` | float | Total market size |
| `focus_levels` | dict[provider -> dict] | Per-benchmark R&D focus levels |
| `inferred_benchmark_weights` | dict[provider -> dict] | Provider's inferred benchmark weights |
| `consumer_signals` | dict[provider -> dict] | Consumer feedback signals |
| `capability_gains` | list or dict | Capability changes this round |
| `per_benchmark_scores` | dict[benchmark -> dict[provider -> float]] | Scores broken down by benchmark |
| `media_data` | dict | See below |
| `consumer_data` | dict | See below |
| `regulator_data` | dict | See below |
| `funder_data` | dict | See below |
| `actor_traces` | dict[actor_name -> str] | LLM reasoning traces for each actor |
| `barrier_to_entry` | dict | Barrier components (composite, market_concentration, capability_gap, funding_lock_in, consumer_lock_in) |

**Nested structure for consumer_data:**
- `market_shares` — dict[provider -> float]
- `provider_satisfaction` — dict[provider -> float]
- `avg_satisfaction` — float
- `switching_rate` — float
- `segment_data` — detailed segment info
- `penalty_breakdown` — dict[provider -> dict] with `base_satisfaction`, `incident_penalty`, `cost_bonus`

**Nested structure for media_data:**
- `headlines` — list of strings
- `sentiment` — float (-1 to 1)
- `provider_attention` — dict
- `narrative_state` — dict
- `risk_signals` — list of strings (e.g. `"incident_security_breach"`, `"regulatory_publish_advisory"`)

**Nested structure for funder_data:**
- `allocations` — per-funder allocation details
- `funder_types` — list of funder type strings
- `provider_funding_totals` — dict[provider -> float] (cumulative funding in dollars)
- `total_funding` — float

**Nested structure for regulator_data:**
- `interventions` — list of dicts with `type`/`action`, `target`/`provider`
- `active_regulations` — list
- `active_sanctions` — list

### Standard extraction script

Run this single Python script to extract all key trajectories at once. Pipe output and read it.

```python
import json

with open('rounds.jsonl') as f:
    rounds = [json.loads(line) for line in f]

providers = list(rounds[0]['scores'].keys())
header = 'Round,' + ','.join(providers)

# --- Scores ---
print('=== SCORES ===')
print(header)
for r in rounds:
    vals = ','.join(f"{r['scores'][p]:.3f}" for p in providers)
    print(f"{r['round']},{vals}")

# --- Market Shares ---
print('\n=== MARKET SHARES ===')
print(header)
for r in rounds:
    shares = r['consumer_data']['market_shares']
    vals = ','.join(f"{shares.get(p, 0):.3f}" for p in providers)
    print(f"{r['round']},{vals}")

# --- Effective Strategies ---
print('\n=== EFFECTIVE STRATEGIES (rd/safety/product) ===')
print(header)
for r in rounds:
    strats = r['effective_strategies']
    vals = []
    for p in providers:
        s = strats.get(p, {})
        vals.append(f"{s.get('rd',0):.2f}/{s.get('safety',0):.2f}/{s.get('product',0):.2f}")
    print(f"{r['round']},{','.join(vals)}")

# --- Funding Totals ---
print('\n=== CUMULATIVE FUNDING (millions) ===')
print(header)
for r in rounds:
    fd = r['funder_data']['provider_funding_totals']
    vals = ','.join(f"{fd.get(p, 0)/1e6:.0f}" for p in providers)
    print(f"{r['round']},{vals}")

# --- Satisfaction and Switching ---
print('\n=== SATISFACTION & SWITCHING ===')
print('Round,avg_satisfaction,switching_rate')
for r in rounds:
    cd = r['consumer_data']
    print(f"{r['round']},{cd['avg_satisfaction']:.3f},{cd['switching_rate']:.3f}")

# --- Media Sentiment ---
print('\n=== MEDIA SENTIMENT ===')
print('Round,sentiment')
for r in rounds:
    print(f"{r['round']},{r['media_data']['sentiment']:.3f}")

# --- Benchmark Count / Introductions ---
print('\n=== BENCHMARK INTRODUCTIONS ===')
prev_n = 0
for r in rounds:
    n = len(r['benchmark_params'])
    if n != prev_n:
        benchmarks = list(r['benchmark_params'].keys())
        print(f"Round {r['round']}: {n} benchmarks - {benchmarks}")
        prev_n = n

# --- Benchmark Orientation ---
print('\n=== BENCHMARK ORIENTATION ===')
print(header)
for r in rounds:
    bo = r['benchmark_orientations']
    vals = ','.join(f"{bo.get(p, 0):.2f}" for p in providers)
    print(f"{r['round']},{vals}")

# --- Regulatory Interventions ---
print('\n=== REGULATORY INTERVENTIONS ===')
for r in rounds:
    for i in r['regulator_data'].get('interventions', []):
        itype = i.get('type', i.get('action', 'unknown'))
        target = i.get('target', i.get('provider', 'all'))
        print(f"Round {r['round']}: {itype} -> {target}")

# --- Incidents and Risk Signals ---
print('\n=== INCIDENTS & RISK SIGNALS ===')
for r in rounds:
    risk = r['media_data'].get('risk_signals', [])
    if isinstance(risk, list):
        incidents = [x for x in risk if isinstance(x, str) and 'incident' in x]
    elif isinstance(risk, dict):
        incidents = [k for k, v in risk.items() if v and 'incident' in k]
    else:
        incidents = []
    if incidents:
        # Also grab incident penalty from consumer data
        penalties = r['consumer_data'].get('penalty_breakdown', {})
        penalty_str = ', '.join(
            f"{p}: -{v.get('incident_penalty', 0):.3f}"
            for p, v in penalties.items()
            if v.get('incident_penalty', 0) > 0
        )
        print(f"Round {r['round']}: {', '.join(incidents)}" + (f" | penalties: {penalty_str}" if penalty_str else ""))

# --- Barrier to Entry ---
print('\n=== BARRIER TO ENTRY ===')
print('Round,composite,mkt_conc,cap_gap,fund_lock,consumer_lock')
for r in rounds:
    b = r['barrier_to_entry']
    print(f"{r['round']},{b['composite']:.3f},{b['market_concentration']:.3f},{b['capability_gap']:.3f},{b['funding_lock_in']:.3f},{b['consumer_lock_in']:.3f}")

# --- Capability Growth Summary ---
print('\n=== CAPABILITY GROWTH (initial -> final) ===')
dims = ['reasoning', 'coding', 'knowledge', 'safety', 'communication', 'agentic']
for p in providers:
    init = rounds[0]['capability_vectors'][p]
    final = rounds[-1]['capability_vectors'][p]
    print(f'{p}:')
    for d in dims:
        delta = final[d] - init[d]
        print(f'  {d:15s}: {init[d]:.3f} -> {final[d]:.3f} ({delta:+.3f})')
```

## 4. Read game_log.md selectively

The game log is large (typically 2000+ lines). Do NOT read the whole file. Instead:

- **Early rounds** (offset 0, limit 100): Initial strategies, first consumer reactions
- **Incident rounds**: Use the risk_signals output from step 3 to identify rounds with incidents, then read those sections. Each round is separated by `---` and starts with `## Round N`.
- **Late game** (offset from end, limit 80): Final strategic postures, endgame dynamics

To find a specific round in the game log:
```
grep -n '^## Round' '<run_dir>/game_log.md'
```

## 5. Analysis framework

Structure your analysis around these dimensions:

1. **Market structure**: Winner-take-most vs competitive? Final concentration. Share trajectory shape (monotonic vs disrupted).

2. **Strategic differentiation**: Do providers make character-consistent decisions? Do strategies diverge over time? Key portfolio shifts and their triggers.

3. **Incident-response cycles**: How do incidents affect share, satisfaction, funding? How fast is recovery? Does the leader recover too easily?

4. **Regulatory escalation**: Does the regulator progress through the ladder coherently? Are sanctions targeted or broad?

5. **Funder behavior**: Do funder types behave differently? (VC chases winners, gov funds challengers, foundation balances). Does funding track or predict performance?

6. **Consumer dynamics**: Satisfaction trend, switching rate evolution, lock-in growth.

7. **Capability dynamics**: Diminishing returns? Ceiling effects? Which dimensions grow fastest? Does funding correlate with capability growth?

8. **Benchmark/gaming dynamics**: Does orientation change? Is validity correlation maintained? Any score inflation visible?

9. **Validity correlation**: 1.0 = perfect ranking fidelity. Below 0.9 = gaming distortion.

10. **Concerns/issues**: Anything that looks unrealistic, too stable, or broken.
