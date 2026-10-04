# Design

Evaluarium is a static-first explorer over simulation runs from the
AI Evaluation Ecosystem project.

## Architecture (T1 &mdash; current)

Three top-level destinations share a nav. Only the right-hand branch
touches run data; the two framing pages are self-contained.

```
   ┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐
   │  index.html       │  │ simulation.html   │  │  explorer.html    │
   │  Ecosystem:       │  │ Simulation:       │  │  Explorer:        │
   │  actor map +      │  │ how-it-works      │  │  condition card   │
   │  literature strip │  │ explainer         │  │  grid + filters   │
   └─────────┬─────────┘  └─────────┬─────────┘  └─────────┬─────────┘
             │                      │                      │
             ▼                      ▼                      │ ?run=...
   ┌───────────────────┐  ┌───────────────────┐            │ ?conditions=...
   │ ecosystem_data_v2 │  │ sim_data.js       │            ▼
   │ figure geometry,  │  │ GENERATED from    │  ┌───────────────────────┐
   │ papers, events,   │  │ the live sim      │  │ viewer.html           │
   │ quotes            │  │ source            │  │ compare.html          │
   └───────────────────┘  └───────────────────┘  └───────────┬───────────┘
        no run data            no run data                   │
                                                             │ loadRun(path)
                                                             │ loadRunsManifest()
                                                             ▼
                                        ┌────────────────────────────────┐
                                        │  js/loader.js                  │
                                        │  the only data-access layer    │
                                        │  Evaluarium.config lives here  │
                                        └───────────────┬────────────────┘
                                                        │ fetch
                                                        ▼
                                        ┌────────────────────────────────┐
                                        │ data/<bucket>/<mode>/<model?>/ │
                                        │      <condition>/seed_<N>/     │
                                        │      frames.json               │
                                        │ runs.json  ← manifest          │
                                        └────────────────────────────────┘
```

`viewer.html` and `compare.html` also load a vendored `js/vendor/d3.v7.min.js`.
Nothing else on the site uses a library. All URLs are relative &mdash; works
under any mount point (`/`, `/evaluarium/`, etc.) without rebuilds.

The split matters when changing things: `index.html` and `simulation.html`
cannot break by a data re-generation, and `explorer`/`viewer`/`compare` cannot
break by a figure edit. The only shared surface is the nav.

## Future tiers

- **T2 &mdash; in-browser heuristic runs (Pyodide).** Users specify params
  in a form; sim runs client-side via Pyodide; output is fed into
  `viewer.html` without persistence. `loadRun()` gains a memory branch
  that returns an in-memory blob instead of fetching from `data/` &mdash;
  call sites don't change.
- **T3 &mdash; BYOK LLM runs.** Users provide their own provider key; a
  small backend (under `website/server/`) proxies LLM calls and streams
  results back. Architecture catches up to `benchmark-caliper`'s
  Render+Vercel-proxy pattern at that point.

## Data contract

`runs.json` is an array of 366 run records. `path` is the directory under
`data/` holding that run's `frames.json`, and is the join key between the two:

```
path          "core_privacy/llm/claude-sonnet-4-6/baseline/seed_42"
bucket        one of core_privacy, core_evaluator_capture,
              structural_ablations, exogenous_validation
mode          "llm" | "heuristic"
model         model id, or null for heuristic runs
condition     condition id, e.g. "baseline", "private_only"
seed          "seed_42"
n_rounds      40 for every bundled run
providers     provider names, in chart order
final_shares  / final_scores   per-provider, at the last round
peak_gap      largest score-satisfaction gap reached
leader_traj   leader share per round, for the card sparkline
```

`frames.json`, generated upstream by
`scripts/animation/generate_explorer.py`:

```
providers, colors      per-provider names and chart colors
n                      round count; equals frames.length
dot_cats               consumer-dot use-case category, 200 dots
dot_enterprise         consumer-dot enterprise flag, 200 dots
frames[]               one entry per round:
  round                round index
  shares, scores, sat  per-provider market share, published score, satisfaction
  avg_sat              market-wide mean satisfaction
  portfolio            per-provider {rd, safety, product} split
  events, incidents    round events and incident records
  active_incidents     incidents still in effect
  media, headlines     media state and generated headlines
  log                  natural-language round summary
  dot_provs            which provider each of the 200 consumer dots holds
  traces               LLM reasoning traces, when captured
  cum_funding          cumulative funding per provider
```

Some per-round maps are empty in many runs (`traces`, `incidents`,
`cum_funding`); consumers of the contract must treat them as optional rather
than assume presence. Two invariants the pages rely on: `n === frames.length`,
and every run in a bundle shares one round count. A single 80-round run among
40-round runs previously hung the compare page's aggregate view.

For T2, where Pyodide-generated runs must satisfy this same contract, this
section should move into a `client/SCHEMA.md` with types rather than shapes.
