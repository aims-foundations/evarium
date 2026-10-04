# Animated Demo

A self-contained HTML animation that plays back a completed simulation run
round-by-round. Every visual element is driven by `rounds.jsonl` data;
no server is required — the output is a single file you open in a browser.

---

## Quick start

```
cd evaluation-ecosystem-simulation
python scripts/animation/generate_demo.py <run_dir>
```

`<run_dir>` is any directory that contains `rounds.jsonl`. Typical paths:

```
sandbox/experiments/_preserved/llm/full_ecosystem_balanced/seeds/seed_221
hf_data_staging/core_privacy/llm/claude-sonnet-4-6/baseline/seed_42
```

Output defaults to `output/demo/demo.html`. Override with `--output`:

```
python scripts/animation/generate_demo.py <run_dir> --output output/demo/my_run.html
```

Open the resulting file in Chrome or Firefox. An internet connection is needed
on first load for Google Fonts (Inter, Playfair Display) and D3.js v7 from CDN;
everything else is embedded.

---

## What data it uses

| File | Required | Used for |
|---|---|---|
| `rounds.jsonl` | Yes | All simulation state |
| `game_log.md` | No | Market brief in newspaper (falls back gracefully if absent) |

The script reads all rounds from `rounds.jsonl`, sorts by round number, and
embeds the full dataset as a JSON blob inside the HTML file. File size is
typically 400–500 KB.

---

## Visual inventory

### Provider orbs (left panel)
- **Size** — proportional to market share (animates each round)
- **Inner donut** — portfolio allocation: R&D (blue) / Safety (sage) / Product (amber)
- **Score** — composite benchmark score, center of orb
- **Market share %** — below score
- **Rank badge** — `#1 ▲2` in top-left corner of each orb cell; gold for leader,
  green/red delta arrows relative to previous round
- **Incident ring** — amber ring expands outward once on incident onset, then fades

### Consumer dots (behind orbs)
200 dots representing consumer market segments. Each dot is:
- Assigned a use-case category at generation time via stratified sampling of
  round-0 segment fractions (fixed across all rounds)
- Colored by category: Tech / Professional / Health & Gov / Consumer / Research
- Positioned near whichever provider currently holds majority share of its
  segment (smooth D3 transitions each round)

### Market share chart (right panel, top)
- Stacked area chart across all 40 rounds
- Moving "now" vertical line
- Small colored triangles at incident onset rounds (moderate+ severity, onset only)

### Score-satisfaction gap chart (right panel, bottom)
- One line per provider: `benchmark_score − consumer_satisfaction`
- Zero line dashed; positive = overvalued on benchmarks vs real satisfaction

### The Eval Times (newspaper, bottom of left panel)
- **Masthead** — edition line (`Vol. I · Round N`) + live funds-raised ticker
  per provider in provider colors
- **Headlines** — up to 4 per round; first headline larger (13 px Playfair),
  remaining three at 10 px, each separated by a thin rule; provider names are
  colored in their legend color
- **No major headlines** — shown when the LLM produced no headlines that round
  (common in early and late rounds of short runs)

### Event chips (bottom strip)
- Regulator intervention chips (blue) — clickable; opens trace panel with
  regulator's full reasoning for that specific intervention
- Incident onset chips (amber) — `Incident: <Provider>` at the round it fires

### Trace panel (slides up from orb area)
- Click any provider orb to see their LLM reasoning for the current round
- Click a regulator chip to see regulator reasoning for that intervention
- Read more / Read less toggle
- Pauses playback on open; resumes on close
- Updates content if you scrub to a new round while the panel is open

---

## Playback controls

| Control | Behaviour |
|---|---|
| ⟲ | Restart from round 0 and play |
| ◀ | Step back one round |
| ▶ / ⏸ | Play / pause |
| ▶\| | Step forward one round |
| 0.5× / 1× / 2× / 4× | Speed — 1× = 1.2 s per round |
| Scrubber | Jump to any round |

---

## Architecture

```
scripts/animation/generate_demo.py
    Python extraction layer + HTML template (single file)
         |
         v
    output/demo/demo.html
         |--- embedded JSON (all frame data)
         |--- D3.js v7 (CDN)
         |--- Vanilla JS animation loop
         |--- Playfair Display + Inter (Google Fonts CDN)
```

### Python pipeline

1. `load_rounds(path)` — parse `rounds.jsonl`, sort by round number
2. `parse_game_log(path)` — extract per-round market summary from `game_log.md`
3. `aggregate_segments(rd)` — collapse 51 consumer segments to 16 use-cases
4. `build_dot_definitions(first_segs, n_dots=200)` — stratified sample of 200
   consumer dots with fixed use-case and uniform draw value (seed 42)
5. `extract_frame(rd, game_log, dot_defs, provider_idx)` — extract per-round
   display fields from one round dict
6. Sequential loop in `generate()`:
   - Incident onset detection (`penalty > 0.025` and rising from previous round)
   - Cumulative funding accumulation per provider
7. `generate()` — assembles payload JSON, injects into `HTML_TEMPLATE`,
   writes output file

### JS runtime (inside the HTML)

The embedded JSON payload shape:
```json
{
  "providers": ["Orion Labs", "Apex AI", ...],
  "colors":    ["#3d5a8a", "#3d7a5a", ...],
  "dot_cats":       [...],   // 200 strings, fixed
  "dot_enterprise": [...],   // 200 booleans, fixed
  "n": 40,
  "frames": [
    {
      "round":    0,
      "shares":   {"Orion Labs": 0.288, ...},
      "scores":   {"Orion Labs": 0.476, ...},
      "sat":      {"Orion Labs": 0.466, ...},
      "portfolio":{"Orion Labs": {"rd":0.55,"safety":0.15,"product":0.30}, ...},
      "events":   [{"kind":"reg","text":"...","trace":"...","round":0}, ...],
      "media":    "OPTIMISM",
      "headlines":["...", "..."],
      "log":      "Avg sat 0.411 — ...",
      "traces":   {"Orion Labs": "We're starting from a position of...", ...},
      "dot_provs":  [3, 0, 1, ...],   // 200 ints, provider index per dot
      "incidents":  {"OpenCore": 0.0113},
      "active_incidents": {},
      "cum_funding":{"Orion Labs": 50000000, ...}
    }, ...
  ]
}
```

Key JS functions:
- `render(r)` — main per-round update; calls all sub-updaters
- `updateOrbs(frame, r)` — D3 arc tween for donut, rank badge, incident ring
- `updateDots(frame)` — D3 transition dots to new provider positions
- `buildShareChart(el, incidentData)` — constructs stacked area + incident markers (called once)
- `buildGapChart(el)` — constructs gap lines (called once)
- `updateNewspaper(frame, r)` — ticker, headline colorization, layout
- `colorizeProviders(text)` — regex replacement of provider names with colored spans
- `showTrace(prov, pIdx)` / `showRegTrace(text, round)` — open trace panel
- `toggleTrace(prov, pIdx)` — click handler for orbs

---

## Customization

### Provider colors
Edit `PROVIDER_COLORS` at the top of `generate_demo.py`. Falls back to
`FALLBACK_COLORS` for any provider not in the dict.

### Number of consumer dots
Change `N_DOTS = 200` near the top of the script. Higher values give a denser
field; 100–300 is the practical range.

### Headline count
Change `[:4]` in `extract_frame` (the `headlines` field) to show more or fewer.
Also adjust `.np-hl-sub { -webkit-line-clamp: N }` in the CSS if sub-headlines
need more lines.

### Animation speeds
Edit the `<option value="...">` entries in the speed select HTML and the
default `let delay = 1200` in JS.

### Segment categories
`SEGMENT_CATEGORIES` in Python maps use-case string → one of five category keys.
`CATEGORY_META` in JS maps category key → `{color, label}`. Add or rename
categories in both places consistently.

### Incident threshold
The `> 0.025` threshold in `generate()` controls which penalty magnitudes count
as "moderate+". Lower it to catch minor incidents; raise it to show only severe ones.

---

## Extending the demo

**Add a new chart panel (right side):**
1. Add a `.csec` div in HTML with a `.cwrap` inside
2. Write a `buildXChart(el)` function that returns `{x, nl}` or similar
3. Call it in the `window.addEventListener("load")` block
4. Update `render(r)` to call a `moveNow` equivalent on the new chart

**Add a new event type:**
1. In `extract_frame`, append `{"kind": "mytype", "text": "..."}` to `frame["events"]`
2. Add `.chip.mytype { ... }` CSS
3. Optionally add a click handler in `pushEvents`

**Add hover tooltips on dots:**
In the dot setup block, add `.on("mouseover", ...)` / `.on("mouseout", ...)` on
the `dots` selection. The dot index `i` maps to `DOT_CATS[i]` for the category.

---

## Known limitations

- **LLM error strings in headlines** — the filter strips lines starting with `ERROR`
  or shorter than 15 chars, but other malformed LLM output may slip through.
- **Fonts require internet** — Playfair Display and Inter load from Google Fonts.
  Offline use falls back to Georgia / system-ui respectively.
- **CSS `transform-box: fill-box`** — needed for the incident ring pulse animation;
  works in Chrome, Firefox, Safari. Not supported in older Edge.
- **`-webkit-line-clamp`** — headline truncation. Works in all modern browsers;
  not part of the formal CSS spec but universally supported.
- **Large runs** — runs longer than 60 rounds or with many providers will increase
  file size and may make the scrubber harder to use precisely.
- **Heuristic runs** — `actor_traces` is empty in heuristic mode, so the trace
  panel shows "No reasoning recorded" for all orb clicks. The rest of the demo
  works fine.
