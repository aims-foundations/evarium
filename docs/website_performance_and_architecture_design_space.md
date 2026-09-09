# Website performance and architecture: design space

Written 2026-09-06 as an investigation. Four changes were implemented the same
day; see [What was implemented](#what-was-implemented). Git history has **not**
been touched. Every number below was measured, not estimated; the method is
stated alongside each one so it can be re-run.

Source of truth for the architecture is [../website/DESIGN.md](../website/DESIGN.md)
and [../website/DEPLOYMENT.md](../website/DEPLOYMENT.md). This document does not
restate them; it records what measurement added.

**Trigger:** YD reported two symptoms. Reopening the local preview sometimes
takes very long while an incognito tab loads instantly, and the explorer tab
feels much slower than the framing pages. The question asked was how much of
that is the preview versus real structural problems.

---

## Summary of the answer

The two symptoms have different causes and neither is what it looks like.

- The reopen-versus-incognito gap is **unresolved**. The local preview is
  measurably worse-configured than production (no gzip, HTTP/1.0, no
  `Cache-Control`), but the measured magnitudes cannot produce a "very long"
  load, so that is a preview-quality finding and not an explanation of the
  symptom. A DevTools check is the first action, not the last.
- The explorer page itself is cheap. What is expensive is everything reachable
  from it, and the worst path is `compare.html` variance mode.
- The largest single structural problem is `traces`: **58.3% of the corpus by
  raw bytes**, in a field with one reader. It is unevenly distributed, so it is
  worth less than a naive read suggests (see the correction in that section).
- A separate, unrelated problem surfaced during the investigation: the git
  history carries ~590 MB of long-untracked experiment output. A measured trial
  rewrite reduces the repo by 90% with zero working-file changes.

---

## What is preview-only

Measured by serving `website/client` with `python -m http.server` and comparing
response headers against the live GitHub Pages copy.

Local:

```
HTTP/1.0 200 OK
Content-Length: 482729          (runs.json)
Last-Modified: ...
```

Live GH Pages:

```
HTTP/1.1 200 OK
Content-Encoding: gzip
Cache-Control: max-age=600
Content-Length: 55290
```

Three differences, all making the preview worse than production:

1. **No compression.** `runs.json` is 482 KB locally against 55 KB live. A
   `frames.json` is 446 KB locally against 120 KB live. A 4x to 9x penalty only
   the preview pays.
2. **HTTP/1.0, so no keep-alive.** Python's `SimpleHTTPRequestHandler` defaults
   to `protocol_version = "HTTP/1.0"` and closes the socket after every
   response. Every asset, including every 304, costs a fresh TCP connection.
3. **No `Cache-Control`, only `Last-Modified`.** Chrome falls back to heuristic
   freshness and fires a conditional request per cached resource on reopen. The
   server was confirmed to answer those with `304`. Each 304 costs a new
   connection because of point 2.

That combination makes a warm reload slower than a cold one, which matches the
reported symptom: incognito has an empty cache and simply fetches, while the
normal profile spends the load revalidating over non-reusable connections.

Byte size is not the local bottleneck. Every asset returned in 6 to 30 ms over
loopback, largest included. "Forever" is not transfer time.

### The incognito asymmetry specifically: still unresolved

Not resolved. Both are profile-level, neither is provable from the filesystem,
and the site itself is ruled out as a cause (zero `serviceWorker`, zero
`caches.` across all five pages and all four JS files).

- **Extensions.** Chrome disables extensions in incognito by default. Every page
  makes exactly one third-party request, a render-blocking Google Fonts
  stylesheet. If a content blocker stalls rather than fails it, first paint waits.
- **A stale service worker on that localhost port**, registered by some earlier
  project on the same origin. Incognito does not run persisted workers.

**Update after browser testing (2026-09-06).** The extension hypothesis is now
the leading one, though still not confirmed as the cause. Loading the site in
YD's normal Chrome profile against the local server produced, on every page:

- console errors from `chrome-extension://jjfblogammkiefalfpafidabbnamoknm`
  injecting into the page;
- exactly one third-party network request, to
  `https://dealfinder.retailmenot.com/experience/app`, made by an extension and
  not by the site.

So an extension is doing network work on every page load, on localhost.
Extensions are disabled in incognito by default, which is precisely the reported
asymmetry. This is circumstantial: it shows an extension is active and talking to
the network, not that it stalls the load.

Resolve with sixty seconds in DevTools: reload the slow page in the normal
profile, look at what dominates the waterfall, and check
`chrome://serviceworker-internals` for that port. Note that no change to this
site can fix an extension, which is worth knowing before spending effort on the
symptom.

---

## Structural findings

These survive deployment.

### 1. `traces` is 58.3% of the corpus and has one reader

`traces` is referenced exactly once in the whole client, at `viewer.html:370`,
to show one provider's reasoning text at the current round. `compare.html` and
`explorer.html` never touch it.

**Correction (2026-09-06, after review).** An earlier version of this document
said "79% of every run file". That figure is from the single largest file in the
corpus and is not typical. Measured across all 366 files:

```
files with any traces:       117
files with none:             249   (all heuristic runs)
median file size:           70.8 KB
max file size:             437.3 KB
traces share of raw corpus:  58.3%   (37.7 of 64.7 MB)
```

So the field is large in aggregate but concentrated in the 117 LLM runs. The
worst single file breakdown, which is what the original 79% described:

| field | bytes across 40 frames | share of that file |
|---|---|---|
| `traces` | 354,029 | 79.0% |
| `dot_provs` | 24,000 | 5.4% |
| `portfolio` | 15,830 | 3.5% |
| everything else | ~52,600 | 12.1% |

Corpus effect of removing it, measured across all 366 runs:

```
gzipped:   15.0 MB  ->   4.3 MB
on disk:   64.7 MB  ->  26.9 MB
```

The on-disk figure was previously stated as "roughly 20 MB", which was
overstated by about a third.

### 2. `compare.html` variance mode fetches whole conditions

`compare.html:583` fires one request per seed inside a single `Promise.all`.
Worst groups, on the wire after gzip:

```
  n    now(gz)   no-traces(gz)   group
 10      1.12M          0.16M    iid_holdout / claude-sonnet-4-6
 10      1.11M          0.17M    baseline / claude-sonnet-4-6
 50      0.52M          0.51M    public_only / heuristic
```

**Correction (2026-09-06, after review).** The second column was previously
labelled `used(gz)`, which was wrong. It is "everything except traces", not what
compare actually reads. Compare reads only `shares`, `scores` and `sat` per
frame (`compare.html:192`, `:197`, `:602`). Gzipped, that is roughly 0.02 to
0.03 MB for the LLM groups and 0.12 to 0.14 MB for the 50-seed heuristic groups.

Two consequences the original text got wrong:

- The LLM variance views download about 1.1 MB to use roughly 30 KB, so the
  waste is worse than stated.
- **The traces split does almost nothing for the heuristic groups** (0.52 MB to
  0.51 MB, about 2%), because heuristic runs carry no traces at all. Those are
  exactly the three worst groups by request count. The claim elsewhere in this
  document that the traces split "fixes the compare path" is false for them.

The aggregate curves being drawn do not need per-seed frames. Note that compare
also picks three actual seeds by final leader share and draws their full
trajectories (`compare.html:589-617`), so any precomputed summary must still
identify those seeds and fetch three frames files. Option C is therefore not
free (see the design space section).

### 3. Render-blocking assets

- ~~The 280 KB vendored d3 loads synchronously in `<head>` on `compare.html:8`
  (above the stylesheet) and `viewer.html:14`.~~ **FIXED 2026-09-06.**
- ~~The Google Fonts stylesheet is render-blocking on all five pages and is the
  site's only external dependency, and its main archival liability.~~ **FIXED
  2026-09-06**, self-hosted.
- **Still open:** on explorer and viewer the data fetch is the critical path but
  starts only after all scripts parse.

### 4. Generator and cache-versioning nits

- ~~`runs.json` is written with `indent=2` at
  `scripts/animation/generate_explorer.py:291` while `frames.json` is minified at
  line 281. 482 KB against 294 KB minified, for no reason.~~ **FIXED
  2026-09-06** at the generator and by re-dumping the existing file.
- `generate_explorer.py:147` (`write_viewer_shell`) emits a second viewer with a
  hardcoded `fetch('data/' + _run + '/frames.json')` at line 210, bypassing
  `loader.js` and defeating the single-data-access-layer design.
- The manual `?v=N` convention has already drifted: `index.html` carries `?v=52`
  while the 2026-09-02 handoff records `?v=48`.

### 5. What is not a problem

Explorer rendering. It builds 19 condition cards and 366 seed chips from one
fetch. That is negligible work. The perceived slowness is a blank loading state
waiting on a second round trip, plus the fact that everything clicked from it
lands on viewer or compare.

---

## Design space

### Data architecture

| Option | What it is | Corpus (gz) | Cost | Verdict |
|---|---|---|---|---|
| A. Status quo | one `frames.json` per run | 15.0 MB | none | baseline |
| B. Split by access pattern | frames minus traces, plus sibling `traces.json` | 4.3 MB hot | small generator change | **take** |
| C. Precomputed aggregates | build-time per-condition summary for compare | +tiny | medium | **take** |
| D. Columnar / binary | typed arrays for numeric fields | ~3 MB | high | reject |
| E. Parquet + DuckDB-WASM | one file, SQL in browser | ~2 MB | high | reject |

B costs a few lines in `build_payload` and one lazy fetch in the viewer. It
breaks the one-file-per-run contract that `DESIGN.md` documents and that T2's
Pyodide branch must satisfy, so `loader.js` grows a `loadTraces(runPath)`
alongside `loadRun`. That is the right place for it and the indirection already
exists for exactly this reason.

C is the one usually skipped. It converts compare's 50-request fan-out into one
request, algorithmically rather than by transport tuning, so it survives any
hosting change. Its risk is derived data going stale, mitigated by a checksum in
the aggregate file.

D trades the format's best property, that anyone can open a run file and read
it, for a gain gzip has already largely taken. E is a real architecture for this
data and would be right at 10x the corpus size, but it puts a heavy wasm
dependency inside an artifact that needs to work in 2031.

Also considered and rejected: HTTP range requests over one concatenated file
with an offset index. Minimal request count on any static host, but fragile
against range-mishandling proxies and unreadable by hand. Not worth it at 15 MB.

### Asset delivery

Standard and low risk:

- Self-host the font families. Removes the only third-party dependency, the only
  render-blocking external request, and the main archival liability.
  **Done, see below.** Two things this document did not anticipate:
  - **Licensing is not uniform.** `ofl/robotomono`, `ofl/playfairdisplay`,
    `ofl/sourceserif4` and `ofl/sourcesans3` all exist in the `google/fonts`
    repo. **`ofl/googlesansflex` returns 404.** Google Sans has historically
    been Google's proprietary brand typeface, so redistributing that woff2 in a
    public repo is not self-evidently fine.
  - **AIMS already settled it.** `aimslab.stanford.edu` self-hosts every face
    from its own `/_next/static/media/`, including Google Sans Flex, and makes
    zero requests to `fonts.googleapis.com` or `fonts.gstatic.com`. Its
    variables are the same ones this site uses
    (`--font-rd-sans: "Google Sans Flex"`,
    `--font-roboto-mono: "Roboto Mono", "Roboto Mono Fallback"`,
    `--rd-serif: "Times New Roman", Times, serif`). Since evaluarium is proxied
    under that domain, matching the institution is the defensible position, and
    it removes an inconsistency where evaluarium hit Google's CDN for faces AIMS
    serves itself.
- `defer` on d3 in `compare.html` and `viewer.html`.
- Start the data fetch in the head rather than after all scripts parse.
- Replace the manual `?v=N` with a generator-computed content hash. Cannot drift
  and enables immutable caching on Render.

### Client runtime

- Compare's `Promise.all` becomes moot under option C. Without C it needs a
  concurrency cap; 50 parallel fetches is worse than batches of 6 on a real
  connection.
- The viewer's per-frame re-render is a smoothness question, not a load
  question. Not profiled. Should not be touched without evidence.
- Server-rendering the explorer card grid at generation time would remove the
  loading state, at the cost of making explorer regeneration-dependent, which
  `DESIGN.md` deliberately avoided. Probably not worth it.

### Verification

No tests exist. Two cheap checks would have caught bugs that already happened:

- **Manifest-versus-disk consistency**: every `runs.json` path resolves to a
  file and every file appears in the manifest. Catches the seed_42 class of
  drift.
- **Contract invariants**: `n === frames.length`, and one round count per
  bundle. `DESIGN.md` records that a single 80-round run among 40-round runs
  once hung the compare page.

Optionally a byte-budget assertion, so a corpus re-cut that doubles the payload
fails loudly instead of quietly making the site slow again.

### Explicitly ruled out

- Any JS bundler, framework, or client build step. Breaks clone-and-serve, adds
  a toolchain a collaborator would need, and the pages are hand-authored for
  good reasons.
- Service workers or offline caching. Adds a persistent hard-to-debug layer to a
  site whose main complaint may already involve one.
- A CDN in front of the data. Render and Pages are both already CDN-fronted.

### What is already right and should not be churned

The `loader.js` indirection, the vendored d3, relative URLs throughout, the
framing-pages versus data-pages split, minified frames, the documented data
contract, `data/VERSION` provenance, `croissant.json`, and the incremental
generator.

---

## Hosting: Render Static

Capabilities differ materially across the three targets:

| | Compression | Cache-Control | Custom headers |
|---|---|---|---|
| local `python -m http.server` | none | none | no |
| GitHub Pages (preview) | gzip, automatic | fixed `max-age=600` | no |
| Render Static (planned) | gzip/brotli | you set it | yes, in `render.yaml` |

**Engineering effort is essentially zero.** `render.yaml` exists and is correct
(`rootDir: website/client`, `staticPublishPath: .`, no build step). The client
is committed and self-sufficient as of `3c4acfe`. All URLs are relative, so no
base-path variable. `origin/main` is current.

The work is organizational, not technical:

| Step | Who | Time |
|---|---|---|
| Create the Static Site from the blueprint | someone with Render access to `aims-foundations` | 10 min |
| Verify `evaluarium.onrender.com` serves | YD | 10 min |
| AIMS adds the Vercel route `/evaluarium/*` | AIMS infra | out of our hands |

**Verdict: worth doing, but it is a distribution decision, not a performance
fix, and it should not go first.** It buys the citable institutional URL, kills
the multiple-copies sync hazard, and lifts the `max-age=600` ceiling. It fixes
none of the structural findings above: `traces` is still 79% and compare still
fans out on Render. Doing the data work first means deploying the good version
once rather than deploying and re-deploying.

Add a `headers:` block to `render.yaml` at the same time: long `Cache-Control`
on `data/*`, short on `*.html`. That is the one capability GH Pages cannot give.

Gate to check first: a Render deploy behind `aimslab.stanford.edu` is public,
indexed, and institutionally attributed. If the paper is in any anonymous phase,
this is a blocker rather than a detail.

---

## Corpus: keep it in git

Two things get conflated and separating them settles the question:

- **Canonical data of record.** The `rounds.jsonl` runs on HF at
  `aims-foundations/ecosystem`. The paper's claims rest on these.
- **Display corpus.** `frames.json`, a lossy derived projection built by
  `generate_explorer.py`. A build output.

For the display corpus the artifact-site convention is to commit it but treat it
as a release artifact rather than a working file: regenerate rarely and
deliberately, tie each regeneration to a paper version, record provenance in the
corpus itself. **This project already does that.** `data/VERSION` records the
generation date, sim commit, pipeline and counts; `croissant.json` is present;
only 2 of 86 commits have ever touched `website/client/data`.

The alternative, generating `data/` at deploy time and gitignoring it, is
cleaner in the abstract and worse here. It breaks clone-and-serve, which
`DEPLOYMENT.md` treats as a design goal; it makes the site un-archivable, since
a Zenodo or Software Heritage snapshot would capture an empty shell; and it adds
a Python toolchain dependency to a deploy that currently has none.

**Decision: leave the corpus in git.** At 66 MB and two commits it costs nothing
real, and the traces split reduces it to roughly 20 MB, making the question less
pressing rather than more.

Tripwires for revisiting, so this stays a decision rather than drift:

- More than about three further full re-cuts. Each adds roughly its compressed
  size permanently.
- Growth past roughly 150 MB, where Render and contributor clone times start to
  hurt.

---

## Git history: the actual repo-size problem

The corpus was initially suspected and is not the cause. Blob volume across all
history, measured with `git rev-list --objects --all` piped through
`git cat-file --batch-check`:

```
   589.9 MB  output/experiments        (untracked now, still in history)
    75.1 MB  experiments/...           (untracked now, still in history)
    67.2 MB  website/client            <- the corpus, ~7%
    20.7 MB  output/explore-benchmark-plots
    18.1 MB  output/final-plots
    12.0 MB  output/comparisons
```

The weight is dead history: none of these paths are in the working tree.

**Correction (2026-09-06, after review).** An earlier version said `output/` and
`experiments/` are "already gitignored". Only `output/` is. `.gitignore` lists
`output/`, `/hf_data` and `/hf_data_staging`; `experiments/` and `comparisons/`
are simply absent from the working tree, not ignored. A future `git add -A`
after a local run would re-track them, so a cleanup is not self-maintaining
unless `.gitignore` is extended at the same time.

The table above also omits top-level `comparisons/` (roughly 40 MB of
`exp_NNN_vs_exp_NNN.md` files), which the trial rewrite does remove. That is why
the table does not visibly reconcile 524 MiB to 54 MiB on its own.

### Measured trial rewrite

Run on a mirror clone in the session scratchpad. The real repo was not touched.
Command: `git filter-repo --invert-paths --path output/ --path experiments/ --path comparisons/`

```
BEFORE   524.2 MiB pack   14,446 objects   86 commits
AFTER     54.3 MiB pack    2,027 objects   77 commits
```

**90% reduction.** The safety check that matters:

```
rewritten HEAD tree: 0ef3c3de7957ffec870ef71cb95967cdfb856834
original  HEAD tree: 0ef3c3de7957ffec870ef71cb95967cdfb856834
IDENTICAL -- no working file changed
```

All 635 tracked files survive byte-identical. The 9 commits that disappeared
only ever touched removed paths ("saving exp", "ran exp27", "cleared outdated
experiments", "deleting old heuristic runs"). No source history is lost.

### Blast radius, as of 2026-09-06

| | |
|---|---|
| Forks | 0 |
| Stars / watchers | 0 |
| Remote branches | 1 (`main`) |
| Tags | 0 |
| References to the repo in the Overleaf tree | none |
| Unpushed local commits | 0 |

About as clean as a public-repo rewrite gets. The window only closes: once the
Render service exists and the AIMS handoff happens, more people hold clones.

### Casualties: a full SHA-citation inventory

**Correction (2026-09-06, after review).** An earlier version said there was one
casualty, `data/VERSION`. That was wrong and it understated the risk
substantially. Verified inventory:

| Citation site | Count | SHAs | Survives rewrite |
|---|---|---|---|
| `data/VERSION` | 1 | `fb893fbf` | no |
| `hf_data_staging/**/metadata.json` | **369** | `c0886be` (338), `ac0893b` (31) | no |
| `hf_data_staging/manifest.json` `git_commits_present` | 1 | both of the above | no |

All three SHAs were confirmed to be real commits in this repository. The
`metadata.json` files are the per-run provenance records of the **public HF
dataset** `aims-foundations/ecosystem`, and `hf_data_staging/README.md:113`
instructs readers to pin to the commit recorded in metadata in order to
reproduce a run. A history rewrite silently breaks that instruction for every
published run.

This does not make the rewrite impossible, but it makes it a coordinated
data-and-code operation rather than a repo-hygiene task. Any rewrite plan must:

- ship the commit map that `git filter-repo` writes, so old SHAs remain
  resolvable;
- either push an HF revision updating the 369 `metadata.json` files, or add a
  README note mapping old SHAs to new;
- grep `SESSION_HANDOFF.md`, `docs/`, and the memory files for short SHAs before
  pushing.

Independently of the rewrite, a git SHA is a fragile provenance anchor precisely
because rewrites happen. The durable anchor is the HF dataset revision, which is
the actual data of record. `VERSION` should cite both.

### Plan, when it goes ahead

1. Commit or stash the current website changes (tree currently has 6 modified
   pages plus untracked `js/boundary.js`).
2. Mirror-backup the current state so the old history is recoverable.
3. Run the rewrite on the real repo, same three paths.
4. Verify the HEAD tree hash still matches and `git status` is clean.
5. Update `data/VERSION` with the new anchor plus the HF revision, commit.
6. `git push --force-with-lease origin main`.
7. Tell anyone with a clone to re-clone.

Steps 1 to 5 are local and reversible. Step 6 is the irreversible one.

Sequencing note: if the traces split happens later, the re-cut orphans the
current 67 MB corpus in history and a second rewrite would reclaim roughly
15 MB more. Both orderings are defensible. Doing it now takes the 90% win
immediately at the cost of a possible cheap second pass; holding until after the
corpus re-cut disrupts clones only once.

---

## What was implemented

Done 2026-09-06, after the tree was committed at `483461a` so a restore point
existed. All four are the no-regeneration items; nothing here runs
`generate_explorer.py` or touches git history.

### 1. `defer` on d3

`compare.html:8`, `viewer.html:14`. 280 KB no longer blocks parsing.

Safe because both pages put their real code in `<script type="module">`, which
is deferred by default and shares the deferred queue with `defer` classics in
document order. d3 sits earlier in the document, so it still executes first.
Verified in Chrome rather than trusting the spec reading: compare rendered and
normalized its own query params, viewer set its title from fetched run data
(`baseline seed 46 · Run Viewer`), zero site console errors on either.

### 2. `runs.json` minified

Fixed at source (`generate_explorer.py:291`, `indent=2` to
`separators=(",", ":")`) and the existing file re-dumped with a content
assertion:

```
content identical after re-dump: True   (366 entries)
raw  482,729 -> 293,917 bytes  (-39%)
gzip  52,502 ->  48,413 bytes   (-8%)
```

Mostly a local-preview gain, since gzip already erased most of the indent cost.

### 3. Self-hosted fonts

`client/css/fonts.css` (generated, 18 faces) plus 8 woff2 in `client/fonts/`,
**269 KB**. Regenerator at `scripts/fetch_fonts.py`. The four Google `<link>`
tags (two preconnects plus a stylesheet, plus viewer's larger variant) were
removed from all five pages and replaced with one same-origin stylesheet, so
per-page request count is unchanged.

Decisions worth not re-deriving:

- **latin + latin-ext only.** Google serves 13 subsets for these families
  (cherokee, syriac, tifinagh, nushu, math, and so on). Latin-ext is the floor
  because the literature strip carries author names with diacritics.
- **Google Sans Flex deduped.** Its `slnt` axis means the normal and oblique
  faces are byte-identical files. Both `@font-face` blocks point at one file;
  keeping both would have wasted 118,248 bytes.
- **Separate stylesheet, not `aims.css`.** 150 lines of generated content does
  not belong in the hand-maintained theme file, and regenerating fonts should
  never touch it.
- **No fallback metric-override faces.** AIMS defines them only for Source Sans
  3 and Source Serif 4, which this site does not use. Inventing
  `ascent-override` / `size-adjust` numbers for these three families would be
  guesswork. This is a real remaining gap: the site takes a reflow when
  webfonts land that AIMS does not.
- `aims.css` bumped to `?v=3` so nobody gets the old file against new markup.

Verified in Chrome on `viewer.html` and `index.html`:

```
googleFontRequests: 0
fontsFetched:       google-sans-flex-normal-latin.woff2, roboto-mono-normal-latin.woff2
googleSansApplied:  true     robotoMonoApplied: true
bodyComputed:       "Google Sans Flex", "Helvetica Neue", Arial, sans-serif
domContentLoaded:   191ms    loadComplete: 465ms    figureNodes: 671
```

Only the subsets actually needed are downloaded; latin-ext and the Playfair
weights load lazily when text requires them.

### 4. `website/serve.py`

Preview server with HTTP/1.1 keep-alive, gzip, and a `Cache-Control` policy
matching what `render.yaml` should carry. Lives in `website/`, not
`website/client/`, because `client/` is the deploy root and has to stay purely
static. Also registers `font/woff2` in `mimetypes`, which Python does not know
and which otherwise ships fonts as `application/octet-stream`.

Measured against live GitHub Pages:

| | serve.py | live Pages |
|---|---|---|
| `index.html` | 26,305 gz | 25,709 gz |
| `runs.json` | 48,413 gz | 55,290 gz (smaller now, from the minify) |
| `frames.json` | 119,177 gz | 122,591 gz |

```
python website/serve.py
```

### Not done

The `traces` split and the compare fan-out both need `generate_explorer.py` to
run, which is still gated on the three hazards in the review section. The git
history rewrite is untouched and deferred.

---

## Recommended sequence

1. Split `traces` out in the generator, lazy-fetch in the viewer via a new
   `loader.js` method. 15.0 MB to 4.3 MB gzipped. Note it helps the LLM compare
   groups only; the three worst groups by request count are heuristic and carry
   no traces.
2. Precompute per-condition aggregates for compare's variance mode. Removes the
   50-request fan-out as a category. See the review section below for a cheaper
   alternative (`gap_traj` on the existing manifest) that may supersede this.
3. ~~Self-host fonts and `defer` d3.~~ **DONE 2026-09-06.** Note the framing was
   wrong: it does not make the reopen symptom moot. Browser testing points at an
   extension, which no site change can fix.
4. ~~Minify `runs.json` and bring the local preview to parity.~~ **DONE
   2026-09-06** (`website/serve.py`).
5. Stand up Render, set explicit cache headers in `render.yaml`, retire the
   Pages preview.
6. Add the two consistency checks to the generator. **Promote this above items 1
   and 2:** it is the guard that has to exist before any regeneration, and both
   remaining items require one.

Items 1, 2 and 6 all live in `generate_explorer.py`, so they are one coordinated
change to one file plus a schema-doc update. That is also the moment to do the
`client/SCHEMA.md` move that `DESIGN.md` already asks for.

Per the project working style, item 1 alone touches the generator, `loader.js`,
`viewer.html` and `DESIGN.md`, so it wants sign-off before any of it is written.

---

## Open questions for YD

1. **Does anyone besides YD hold a working clone of `aims-foundations/evarium`?**
   The only input that cannot be determined from here. 0 forks covers GitHub
   forks, not `git clone` by org collaborators. Gates the force-push.
2. **Rewrite now, or after the corpus re-cut?** See the sequencing note above.
3. **Is the paper in an anonymous phase?** Gates the Render deploy, not the
   local work.
4. **DevTools check on the slow reopen**, to close out the extensions versus
   service-worker question before any work is done on its account.

---

## External review, 2026-09-06

This document was reviewed by a second agent (Fable 5.1) with access to the
repository. Its factual findings were independently re-verified before being
accepted. The corrections marked "after review" above are the result.

**Verified and accepted** (all re-measured directly):

- `traces` is 58.3% of the corpus, not 79% of every file; 249 of 366 files have
  none.
- Post-split corpus is 26.9 MB on disk, not "roughly 20 MB".
- Compare reads only `shares`, `scores`, `sat`; the `used(gz)` column measured
  the wrong thing, and the traces split does not help the heuristic compare
  groups.
- 369 `metadata.json` files plus `manifest.json` cite git SHAs that the rewrite
  invalidates; this is the public HF dataset's reproducibility anchor.
- `experiments/` and `comparisons/` are not gitignored, only `output/` is.

**Raised, not yet verified, and worth checking before any regeneration:**

- `generate_explorer.py:293` calls `write_viewer_shell()` unconditionally, so
  running the generator with `-o website/client` would **overwrite the
  hand-authored `viewer.html`**. Described in this document as "a second
  viewer"; the reviewer characterises it as a clobber.
- `discover_runs()` finds 369 runs against a 366-run manifest; the three extra
  are the deliberately deleted seed_42 set, which a regeneration would re-add.
  The proposed manifest-versus-disk check cannot catch this, because both sides
  regenerate consistently. The missing check is manifest-versus-exclusion-list.
- The mtime skip at `generate_explorer.py:265-274` means a partial regeneration
  would leave a mixed corpus silently violating the new contract. Needs
  `--force`.
- `git filter-repo` deletes the `origin` remote and refuses to run on a
  non-fresh clone without `--force`, so plan step 6 as written would fail.
- GitHub retains old objects and old SHAs stay fetchable until server-side GC,
  so the size drop is not immediate and "the history is gone" is not true for
  months.

**Design-space options this document missed**, offered by the reviewer and not
yet evaluated:

1. **Add `gap_traj` to `runs.json`.** The manifest already carries `leader_traj`,
   which is compare's first metric. Adding the second gives compare's variance
   bands everything with zero extra requests, no new file, no checksum and no
   staleness path. Strictly cheaper than option C, and it may remove the need
   for it.
2. **Host the display corpus on Hugging Face** and fetch cross-origin.
   `loader.js` already anticipates this. Removes the corpus from all three git
   histories at once and makes the HF revision the provenance anchor. Costs CORS,
   rate limits, and archival self-containment.
3. **`git clone --depth 1`** as the zero-risk alternative to a history rewrite.
   Roughly a 70 MB clone today, no irreversible action.
4. **`python -m http.server --protocol HTTP/1.1`** (available since 3.11) fixes
   the keep-alive half of the preview problem with a flag and no code.
5. Emit `runs.js` the way `sim_data.js` is emitted, removing the explorer's
   second round trip without server-rendering markup.
6. Prefetch on explorer card hover.

**Open disagreement, for YD to settle.** The reviewer argues the recommended
sequence is inverted for a single maintainer mid-review: it would put the
DevTools check, committing `boundary.js`, `defer` d3 and the `runs.json`
re-dump first (all zero-risk), then the generator guards, then the traces split,
and would **defer the history rewrite past the paper decision** or fold it into
the frozen-release-repo plan. Given the HF SHA finding, deferring the rewrite
looks right to me and reverses the recommendation made earlier in this document.
That reversal has not been applied to the sequence above; it needs YD's call.

One further item the reviewer raised that this document should have caught:
`js/boundary.js` is untracked while all six modified pages now reference it, so
committing the HTML without the JS reproduces exactly the failure class
`DEPLOYMENT.md:29-37` describes.

---

## Status as of 2026-09-06

Investigation, then four changes implemented. **No commits and no push**; the
working tree carries the changes and the restore point is `483461a`. Git history
is untouched: the trial rewrite ran only on a scratchpad mirror clone.

Working tree at end of session:

```
 M scripts/animation/generate_explorer.py   runs.json minified at source
 M website/client/compare.html              defer d3, fonts swap
 M website/client/viewer.html               defer d3, fonts swap
 M website/client/index.html                fonts swap
 M website/client/explorer.html             fonts swap
 M website/client/simulation.html           fonts swap
 M website/client/css/aims.css              header comment, load order
 M website/client/runs.json                 re-dump, content identical
?? website/client/css/fonts.css             new, generated
?? website/client/fonts/                    new, 8 woff2, 269 KB
?? website/serve.py                         new
?? scripts/fetch_fonts.py                   new
?? docs/website_performance_and_architecture_design_space.md
```

Two environment changes: `git-filter-repo` installed via pip for the trial
rewrite, and 269 KB of woff2 added to the repo.

Consequence not yet handled: the GH Pages copy at
`yashdave003/evaluation-ecosystem-explorer` was already about 248 diff lines
behind `website/client` before this session and is now further behind, and it
does not have `client/fonts/` at all. If it is re-synced, the font directory
must go with it or every page there falls back to Helvetica.
