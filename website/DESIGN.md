# Design

Evaluarium is a static-first explorer over simulation runs from the
AI Evaluation Ecosystem project.

## Architecture (T1 &mdash; current)

```
                ┌──────────────────────────┐
                │  index.html              │
                │  ─ card grid + filters   │
                │  ─ entry point           │
                └────────────┬─────────────┘
                             │ ?run=...   ?conditions=...
                             ▼
         ┌────────────────────────────────────────┐
         │  viewer.html         compare.html      │
         │  ─ single-run        ─ multi-run       │
         │    animation          comparison       │
         └────────────────────┬───────────────────┘
                              │ Evaluarium.loadRun(path)
                              │ Evaluarium.loadRunsManifest()
                              ▼
         ┌────────────────────────────────────────┐
         │  js/loader.js                          │
         │  ─ one place to change how runs load   │
         │  ─ basePath / dataPath constants here  │
         └────────────────────┬───────────────────┘
                              │ fetch
                              ▼
         ┌────────────────────────────────────────┐
         │  data/<bucket>/<mode>/<model?>/        │
         │       <condition>/seed_<N>/frames.json │
         │  runs.json   ← top-level manifest      │
         └────────────────────────────────────────┘
```

All pages share `js/loader.js`. All URLs are relative &mdash; works under
any mount point (`/`, `/evaluarium/`, etc.) without rebuilds.

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

`runs.json` is an array of run records:
`{ bucket, mode, model, condition, seed, path, ... }`. `path` is the
directory under `data/` where the corresponding `frames.json` lives.

`frames.json` is generated upstream by
`scripts/animation/generate_explorer.py`. Its full schema is not yet
documented here &mdash; for T2 (Pyodide-generated runs that need to satisfy
the same contract) this should grow into a `client/SCHEMA.md`.
