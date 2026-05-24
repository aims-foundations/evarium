# Evaluarium — website

Interactive explorer for AI Evaluation Ecosystem simulation runs.
Once deployed, will live at `https://aimslab.stanford.edu/evaluarium/`.

## Pages

| File | What it does |
|---|---|
| `client/index.html` | Condition card grid (bucket / mode / model / search filters; compare mode) |
| `client/viewer.html` | Full single-run playback &mdash; fetched via `?run=<path>` |
| `client/compare.html` | Multi-run comparison (condition &times; seed &times; p10/p90) |

## Running locally

```bash
cd website/client
python -m http.server 8080
# open http://localhost:8080
```

Pure static &mdash; any HTTP server works.

## URL formats

```
index.html?bucket=core_privacy&mode=llm&model=claude-sonnet-4-6&q=baseline
viewer.html?run=core_privacy/llm/claude-sonnet-4-6/baseline/seed_42
compare.html?conditions=baseline|public_only&seeds=seed_42&model=claude-sonnet-4-6
compare.html?conditions=baseline&seeds=seed_42|seed_43&model=claude-sonnet-4-6&agg=1
```

## Data

`client/data/` (~65 MB, 367 frame files) and `client/runs.json` (~500 KB)
are bundled in this repo. Provenance lives in `client/data/VERSION`.
Regenerated upstream via `scripts/animation/generate_explorer.py`.

## Layout

```
website/
├── README.md        ← this file
├── DESIGN.md        ← architecture and tier roadmap
├── DEPLOYMENT.md    ← hosting notes
└── client/          ← pure-static HTML/JS/CSS + bundled run data
    ├── index.html
    ├── viewer.html
    ├── compare.html
    ├── runs.json
    ├── LICENSE
    ├── js/
    │   └── loader.js
    └── data/
        ├── VERSION
        └── <bucket>/<mode>/<model?>/<condition>/seed_<N>/frames.json
```

## License

MIT &mdash; see [`client/LICENSE`](client/LICENSE).
