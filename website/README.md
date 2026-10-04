# Evaluarium — website

Interactive explorer for AI Evaluation Ecosystem simulation runs.
Once deployed, will live at `https://aimslab.stanford.edu/evaluarium/`.

## Naming

Three names are in play and they are deliberately not unified:

| Where | Name |
|---|---|
| Git repo and push target | `github.com/aims-foundations/evarium` |
| Deploy path and Render service | `/evaluarium/`, `evaluarium.onrender.com` |
| JS namespace in `client/js/loader.js` | `Evaluarium` |
| **Anything a visitor sees** | **none of them** |

The site never displays a product name. Every page title and header reads
"The AI Evaluation Ecosystem", so none of this is visitor-facing.

Leave all three as they are. The repo rename is owned elsewhere, and the
deploy paths are established, so do not unify the spelling in `render.yaml`,
`loader.js`, the Vercel route, or these docs.

## Pages

Three top-level destinations, reachable from the shared nav on every page:
**Ecosystem** (framing) &rarr; **Simulation** (how it works) &rarr; **Explorer** (results).

| File | What it does |
|---|---|
| `client/index.html` | **Ecosystem.** Landing page: framing + three entry cards + the merged Fig-1 map (6 modeled actors + grey unmodeled stations; click-to-pin detail panes; spotlight system with a literature strip) |
| `client/simulation.html` | **Simulation.** Explainer: the score-vs-satisfaction mechanism, capability space, round protocol, information partition, belief update, holdout case study, scope limits. Six built-in diagrams, no external deps |
| `client/explorer.html` | **Explorer.** Condition card grid (bucket / mode / model / search filters; compare mode) |
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
explorer.html?bucket=core_privacy&mode=llm&model=claude-sonnet-4-6&q=baseline
viewer.html?run=core_privacy/llm/claude-sonnet-4-6/baseline/seed_42
compare.html?conditions=baseline|public_only&seeds=seed_42&model=claude-sonnet-4-6
compare.html?conditions=baseline&seeds=seed_42|seed_43&model=claude-sonnet-4-6&agg=1
```

## Data

`client/data/` (66 MB, 366 frame files across four buckets) and
`client/runs.json` (472 KB, 366 entries) are bundled in this repo. Provenance
lives in `client/data/VERSION`. Regenerated upstream via
`scripts/animation/generate_explorer.py`.

Every run is 40 rounds. A single 80-round `core_privacy/heuristic/baseline`
run was removed from the bundle on 2026-08-17: it broke the compare page's
aggregate view, which indexed every seed to the first series' length. The
guard is now `Math.min` over the series, but the invariant is still worth
keeping, so add runs of one length at a time.

`runs.json` and `client/data/` must agree exactly in both directions. To check:

```bash
python - <<'EOF'
import json, glob
declared = {r["path"] for r in json.load(open("client/runs.json"))}
on_disk  = {p.replace("\\","/").replace("client/data/","").replace("/frames.json","")
            for p in glob.glob("client/data/**/frames.json", recursive=True)}
print("declared but missing:", sorted(declared - on_disk) or "none")
print("on disk but undeclared:", sorted(on_disk - declared) or "none")
EOF
```

## Layout

```
website/
├── README.md        ← this file
├── DESIGN.md        ← architecture and tier roadmap
├── DEPLOYMENT.md    ← hosting notes
└── client/          ← pure-static HTML/JS/CSS + bundled run data
    ├── index.html        ← Ecosystem: landing page + actor map + literature/events strip
    ├── simulation.html   ← Simulation: how-it-works explainer
    ├── explorer.html     ← Explorer: run card grid
    ├── viewer.html       ← single-run playback (?run=<path>)
    ├── compare.html      ← multi-run comparison
    ├── runs.json         ← manifest; must match client/data/ exactly
    ├── favicon.svg
    ├── LICENSE
    ├── js/
    │   ├── loader.js              ← the ONLY data-access layer: Evaluarium.loadRun /
    │   │                            .loadRunsManifest. Swapping the data source (CDN, HF)
    │   │                            is a change to Evaluarium.config here and nowhere else
    │   ├── ecosystem_data_v2.js   ← context-page data; `fig` block = verbatim paper Fig-1 port
    │   │                            (bump the `?v=N` on its <script> tag when data changes)
    │   ├── sim_data.js            ← GENERATED, do not hand-edit. Benchmark weights, consumer
    │   │                            need profiles, and archetypes computed from the live sim
    │   │                            source by scripts/animation/generate_sim_page_data.py;
    │   │                            re-run it after model changes and bump the `?v=N`
    │   └── vendor/
    │       └── d3.v7.min.js       ← vendored, not a CDN: compare.html and viewer.html only
    └── data/
        ├── VERSION
        └── <bucket>/<mode>/<model?>/<condition>/seed_<N>/frames.json
            buckets: core_privacy, core_evaluator_capture,
                     structural_ablations, exogenous_validation
```

## Conventions worth knowing before editing

- **Self-contained by design.** No CDN, no build step, no framework. d3 is
  vendored. The one exception is the Google Fonts link in `viewer.html`, which
  the other four pages do not load, so they fall back to system fonts.
- **Figure geometry is data, not code.** In `ecosystem_data_v2.js`, `EDGES`
  carries baked `lx`/`ly` label centres and `extraEdges` carry `lt`/`ldx`/`ldy`.
  Four rules hold and are worth re-checking after any move: a label sits on the
  line it names, no label covers an arrowhead (the head is an 8-unit triangle,
  not a point), no label collides with another or with a box, and each label
  moves as little as possible.
- **Provenance edges are spotlight-only.** They render under the boxes with
  their label boxes topmost, and appear only while their row is selected.
- **`?v=N` is the cache key.** `index.html` versions `ecosystem_data_v2.js`;
  bump it on every data change or returning visitors keep the old figure.
  `index.html` itself is unversioned, so its own edits need a hard reload.

## License

MIT &mdash; see [`client/LICENSE`](client/LICENSE).
