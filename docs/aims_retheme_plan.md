# Retheming evaluarium to the AIMS live theme

Plan only. Written 2026-09-03. Nothing in `website/client` has been changed.
Source of truth for the target values is [aims_theme_audit.md](aims_theme_audit.md).

**Decision:** match the live `aimslab.stanford.edu` (`rd-*`) theme. Not
benchmark-caliper.

**Scope:** the five pages in `website/client` (`index`, `simulation`,
`explorer`, `compare`, `viewer`) plus the `palette` block in
`js/ecosystem_data_v2.js`.

This touches far more than 2-3 files, so per the project working style this
plan wants sign-off before any of it is written. The four open questions at
the bottom are the parts I should not decide alone.

---

## What we are moving from and to

| | now | target |
|---|---|---|
| Ground | `#f0e6d3` tan | `#f3efec` warm off-white |
| Ink | `#2a1a0e` brown-black | `#000` |
| Accent | `#3d5a8a` slate blue | `#8c1515` cardinal |
| Sans | `"Inter"` (declared, never loaded) | Google Sans Flex, weight 300 |
| Mono | `ui-monospace` stack | Roboto Mono |
| Serif | Playfair Display (viewer only) | Times New Roman, for citation titles |
| Display type | 14 to 20px, weight 600-700 | fluid to `6.75rem`, weight 300, tracking `-.045em` |
| Container | 880 / 1060px | 1334px, prose constrained to ~58ch |

The character of the change: our site is small, warm and bold; AIMS is large,
cool-neutral and light. The weight inversion (700 down to 300) and the tracking
(0 to negative) do more of the work than the hex values do.

---

## Phase A - foundation  [DONE 2026-09-03]

Landed as written, with two corrections to the estimates below.

**The palette was not six values, it was 104.** A census across the five pages
found 104 distinct hex values in ~600 occurrences. About 40 of those are the
structural palette (grounds, surfaces, borders, inks, accent) and those moved:
487 hex replacements plus 27 `rgba()` literals the hex sweep could not see.
The rest are actor colours, edge-family colours and the explorer/compare
categorical series, all deliberately left for Phase C.

Inside `<style>` blocks the replacement is `var(--token)`; outside them it is a
literal hex, because `fill="var(--x)"` is not valid as an SVG presentation
attribute and would have silently rendered black.

**The figure did not move, and that is deliberate.** Its SVG group still
declares `"Inter, system-ui, sans-serif"` at `index.html:940`, so it does not
pick up Google Sans Flex and its 24 solved label positions stay valid. The
figure will change face in Phase C, together with its colours and a re-solve.

Also fixed along the way: five `:focus-visible` rules would have gone cardinal
via the accent mapping. AIMS keeps digital blue for focus even where it drops
digital blue for links, so those were restored by hand.

Two judgment calls made while looking at the result:

- `section h2` was 15px bold uppercase. The headings are written in sentence
  case in the markup and only uppercased by CSS, so dropping `text-transform`
  restored AIMS's casing for free. They now take the `.rd-h3` scale.
- `simulation.html`'s lede is held at `clamp(1rem, 1.15vw, 1.125rem)` rather
  than the full AIMS lead size. AIMS ledes run two or three lines; ours runs
  eleven, and at `1.25rem` it swallowed the page.

Verified: all five pages render, the figure draws, charts draw, the viewer
newspaper survives, no old structural colour remains, and line endings are
unchanged (all LF, matching HEAD).

### As planned

One new file, `client/css/aims.css`, linked from all five pages. No build step,
so it is a plain stylesheet holding tokens, base type and the resets that are
currently duplicated inline five times. Page-specific rules stay inline.

1. **Fonts.** Google Sans Flex (variable) + Roboto Mono. Times New Roman is a
   system face, free. See open question 4 on CDN vs self-hosting.
   This also fixes the standing bug that Inter is declared but never loaded on
   four of the five pages. *Corrected in Phase C:* measurement showed Inter is
   installed locally on this machine, so those pages rendered in real Inter
   here and in `system-ui` for anyone without it. The defect was per-reader
   inconsistency, not a universal fallback.
2. **Token block** in `:root`, lifted from the audit: the full Stanford palette,
   the `--rd-*` layer, `--rd-grotesk` / `--rd-serif` / `--rd-mono`,
   `--ease-out`.
3. **Base type**: `line-height: 1.375`, `color: #000`, ground `--rd-warm`,
   focus ring `2px solid var(--digital-blue)` at `2px` offset, selection
   `#8c15152e`. All four are AIMS values.
4. **Ground and ink swap** across all five pages. Mechanical: our warm palette
   is six hex values used consistently, so this is a find-and-replace against
   a mapping table, not a judgment call per site.
5. **Type scale**: `.rd-display`, `.rd-page-title`, `.rd-h2`, `.rd-h3`,
   `.rd-lead`, `.eyebrow`, `.rd-mono` exactly as measured.

Verifiable at the end of Phase A: every page reads as AIMS at a glance, with
components still in our old shapes.

## Phase B - components  [DONE 2026-09-03]

Approach taken, which differs from what the table below implies: existing
selectors were **restyled in place** rather than reclassed in the markup. The
pages' JS queries several of these class names, so swapping `.card` for
`.rd-card` in the HTML would have been the riskier route for no visual gain.
`css/aims.css` gained the AIMS component vocabulary anyway, both as the shared
home for the site header and as the reference the page rules were written
against.

Two rules did most of the work, and are worth keeping in mind for Phase C:

- **Corners are pill or square.** AIMS has no mid-radius anywhere, so every
  4px/6px/8px radius became either `30px` or `0`.
- **Small text is mono, uppercase, tracked .08em.** That is how AIMS carries
  hierarchy at small sizes instead of bolding, and it replaced essentially
  every `font-weight: 700` label on the site.

**Header.** Now one shared `.site-hdr` in `aims.css` instead of five inline
copies, with a lockup of "Stanford AIMS" linking to the lab, a rule, our
wordmark, and pill nav. Compare and viewer keep their own headers, since they
carry run context rather than site nav, but match the same spec. As decided,
the AIMS nav is *not* mirrored: caliper mirrored it and its copy has since gone
stale.

**Notable substitutions.** The literature strip became an AIMS paper listing
(serif titles, mono uppercase author/date meta, pill state chips, solid rather
than dashed rules); explorer condition titles went serif; readout tiles and the
viewer's round counter became AIMS stat blocks, mono numeral in cardinal at
weight 300; explorer cards took the AIMS hover, a 3px lift and cardinal-tinted
border rather than a drop shadow, gated behind `prefers-reduced-motion`.

Four things caught by looking at the result rather than by reasoning:

- Explorer's model badges wrapped to three lines and stretched every card
  header, because mono plus pill padding is much wider than the sans it
  replaced. Fixed with `white-space: nowrap` and top-aligning the header row.
- The section rail overflowed for the same reason. It still scrolls; the
  scrollbar is now hidden, as AIMS does with its own overflowing strips.
- Every literature title was underlined, which AIMS does not do. Titles are
  undecorated at rest now, with the underline on hover.
- The viewer's round readout put "Round" in big cardinal and the number in
  small grey, i.e. the label styled as the value. Inverted.

Verified across all five pages at 1327px. Line endings unchanged.

### As planned

Port the AIMS component vocabulary onto what we already have. Mostly a
one-to-one swap:

| ours | AIMS |
|---|---|
| filter chips, buttons | `.rd-btn` black pill, mono uppercase, cardinal on hover |
| chip row | `.rd-chip` |
| paper / event rows | `.rd-paper-card` |
| section headers | `.eyebrow` + `.rd-h2` |
| list rows | `.rd-row` |
| stat readouts | `.rd-stat` |

`.rd-paper-card` is the notable one: serif title, authors at `.82rem` opacity
.7, and a mono uppercase meta footer above a hairline rule. That is close to
what our event rows already do, so the port is mostly renaming.

Two AIMS behaviours to decide on rather than copy blindly:

- **Links.** AIMS `.rd-prose a` inherits color with a cardinal-at-35%
  underline, going full cardinal on hover. That **departs from Stanford's own
  rule** that links are digital blue. Caliper follows Stanford; the live site
  does not. Since the instruction is to follow aimslab, I would follow aimslab
  and note the divergence here rather than silently split the difference.
- **Motion.** `.reveal` fade-and-rise with 80ms stagger is a real part of the
  AIMS identity, all correctly gated behind `prefers-reduced-motion`. Cheap to
  add, and without it the pages will read as flatter than their neighbours.

## Phase C - the main figure  [DONE 2026-09-03]

**The expensive half turned out to be cheap, and the estimate below was wrong
about why.** I assumed changing the figure's face would invalidate the solved
label positions. It does not, because the label boxes are sized from *string
length* (`maxLen * fs * 0.52 + 8`), not from measured glyph widths. Box
geometry is therefore font-independent, and the R5/R6 collision rules operate
on that geometry. Nothing needed re-solving.

What did need checking was whether the text still *fits* the unchanged boxes.
Measured in-browser across all 36 canonical label lines and all 53 extraEdge
labels:

- Google Sans Flex is **2.5% wider** than the old face on average.
- **Zero labels overflow.** Tightest slack falls from 6.85px to 4.87px (on
  "benchmarks"), so roughly 2.4px per side of remaining clearance.

The audit was re-run and reports no violations, though that is confirmation
rather than evidence: no coordinate moved.

**Italics are real, not synthesized.** Google Fonts serves no `ital` faces for
Google Sans Flex, so `font-style: italic` would have been faux-slanted by the
browser. The `slnt` axis *is* exposed and returns proper `oblique 10deg` faces,
so the font request on all five pages now asks for
`slnt,wght@-10,300..700;0,300..700`. This matters most in the figure, where the
role lines and every provenance label are italic.

**Colours.** All from the Stanford palette, in a deliberate two-register
scheme: each edge family takes the bright hue, the actor most associated with
it takes the dark variant. Evaluators cardinal, Consumers palo alto, Media
lagunita, Regulator plum, Model Providers digital-blue-dark, Funders a darkened
poppy. Grey stations moved to Stanford's own neutrals.

**Two derived values, both flagged in the data file.** Poppy is Stanford's only
orange and could not be used at full strength twice:

- `funders: #8f5100` - at full strength poppy fails WCAG AA both as a header
  fill behind `#f3efec` text and as body text on white. Actor colours are used
  three ways (header fill, box stroke, body text), so each must be dark enough
  for both. Darkening to meet the 4.5 threshold follows Stanford's web
  guidance rather than departing from it.
- `capital: #bf6a00` - full-strength poppy has far higher chroma than digital
  blue and digital green, so the capital arcs read as the loudest thing on the
  map and implied a salience the model does not claim. The three families are
  peer channels and needed comparable weight. This one is a judgement call and
  the easiest thing here to overrule.

Open, not acted on: the actor boxes keep `rx: 8` rounded corners while every
other surface on the site went square. Changing figure geometry is past what a
retheme should decide unilaterally, so it is left as a question.

### As estimated

Two halves with very different costs.

**Colors: cheap.** `ecosystem_data_v2.js:106` has a `palette` block that
overrides figure colors at render time, so the whole diagram recolors from one
object. And the AIMS accent hues land on our six actors almost too neatly:

| actor | now | AIMS |
|---|---|---|
| Evaluators | `#8a2f2b` | `--cardinal` `#8c1515` |
| Consumers | `#3f6b45` | `--palo-alto` `#175e54` |
| Media | `#2f6b7e` | `--lagunita` `#007c92` |
| Regulator | `#5c3a78` | `--plum` `#620059` |
| Funders | `#9a5b1f` | `--poppy` `#e98300` |
| Model Providers | `#35507e` | `--digital-blue` `#006cb8` or `--sky` |

Every actor color becomes a Stanford palette color, and the hue relationships
we already rely on survive. Poppy may read too bright against the others at
figure scale and want darkening; that is a look-at-it call.

Grey stations stay grey. Their whole job is "no modeled channel touches me,"
so they must not take a palette color.

**Type: expensive.** The SVG sets `"Inter, system-ui, sans-serif"` at
`index.html:940`, and its 13 font sizes were hand-tuned to 8-12.5px across
three passes last session. Label box widths are computed from those sizes
(`w = len * 8 * 0.52 + 7`), and the R5/R6 collision rules were verified against
them. Changing the face changes the metrics, which invalidates every solved
label position and means re-running the harness (`solve_prov.py`,
`audit_edges.py`, `fix_spot.py` in the session scratchpad).

Also: Google Sans Flex at weight 300 will be too thin at 8px. The figure will
need 400 or 500 even though the page display type is 300.

I would treat Phase C as its own sitting, after A and B are settled and the
type decisions have stopped moving.

## Phase D - page-specific  [DONE 2026-09-03]

**The retheme had introduced three responsive regressions, all the same
cause.** Mono caps with `.08em` tracking are much wider than the sans they
replaced, and three headers were non-wrapping flex rows. Measured against the
pre-retheme files rather than assumed:

| page | before | after retheme | now |
|---|---|---|---|
| compare @430 / @360 | 4px / 74px | 89px / 159px | 0 / 0 |
| viewer @720 / @430 | 29px / 319px | 223px / 513px | 0 / 0 |
| index @360 / @340 | 0 / 0 | 12px / 32px | 0 / 0 |

Fixes: `flex-wrap` plus narrow-width rules on compare's and viewer's headers,
and on index the citation meta line, where a long author list
("GUHA, ZHANG, TSANG, MANNING, NYARKO & HO (2026)") in mono caps could not
wrap or shrink. All five pages are now at zero horizontal overflow from 1440px
down to 340px, which is better than the state before the retheme on three of
them. Viewer remains a desktop layout, as it was.

Mobile header rules moved into `aims.css` with `.site-hdr` rather than being
repeated per page, with a second breakpoint at 460px where the three-part
lockup drops its rule and the wordmark takes its own row.

**Viewer frame** reskinned as decided, pastiche kept: mono uppercase panel
labels, outlined pill event chips, AIMS stat treatment on the round counter,
and the onboarding overlay on white cards with a black pill button. Playfair
and the newspaper masthead are untouched.

**Prose pass** on explorer and compare was deliberately light. Most strings
were already fine, so only four changed: a placeholder that disagreed with its
own aria-label, "Loading data" where the sibling page says runs, and two
compare warnings that were semicolon splices leaving the reader to work out
what was meant. Rewriting strings that read well would have been churn.

**Content-column alignment (added on YD request, 2026-09-03).** The prose
looked short of the layout, but measuring rendered characters per line showed
the opposite of the intuition: body copy was already running **96 characters
per line on index and 92 on simulation**, against a comfortable maximum of
about 80. The text was not narrow, the container was wide, so widening prose
to the old 1012px column would have meant roughly 138 characters per line.

Fixed by bringing the container in rather than pushing the text out. Both pages
now use `main { max-width: 752px }`, which is 704px of content, exactly the
68ch prose measure, so prose, entry cards, literature rows, tables and inline
figures all end on the same line. The ecosystem figure is unaffected: it
already breaks out of `main` via `left: 50%` and keeps its full 1280px. On
index the entry grid's `minmax` dropped 240px to 200px, since three 240px
tracks no longer fit and auto-fit would have wrapped the third card.

Cost, accepted by YD: simulation's inline diagrams lose about 15% of their
width. Checked afterwards that they still render and that nothing overflows.

Verified: all five pages valid UTF-8 (an apparent mojibake was my terminal, not
the files), line endings unchanged, and zero horizontal overflow on index and
simulation from 1600px down to 340px.

### As planned

- `explorer` and `compare` UI chrome, which has never had a prose or style
  pass either way.
- `viewer.html` is the odd one out: it is a newspaper pastiche, with Playfair
  Display, a masthead, and an "edition" line. See open question 3.
- The `?v=N` cache-buster on `ecosystem_data_v2.js` gets bumped once at the end,
  not per phase.

---

## Open questions

**1. Type density.** AIMS body copy is ~17.8px at weight 300 with generous
band padding; ours is 13.5-14px and dense. Our pages carry tables, event rows
and a run explorer, and at the AIMS scale they get a lot longer. AIMS itself
runs small text in its component layer (`.rd-paper-card-meta` is `.65rem`,
`.rd-research-map-description` is `.8rem`), so there is precedent inside the
theme for both. My recommendation: take the AIMS scale for heroes, headings
and prose, and keep a denser scale for tables and UI chrome, exactly as AIMS
does. Worth confirming, because it is the difference between a site that
matches AIMS and a site that reads as AIMS.

**2. Header and nav.** Recreate the AIMS header with its full nav, as caliper
does, or run a minimal brand bar with a single link back to AIMS plus our own
page nav? Caliper chose the first and its nav is now visibly stale
(Competition / Workshop, which the live site no longer shows). I would take
the second: nothing to go stale, and it is honest about being a sub-app.

**3. `viewer.html`.** The newspaper conceit is a deliberate visual register,
not site chrome that drifted. I would keep the pastiche and reskin only its
frame, so it still reads as a newspaper but sits in an AIMS page. The
alternative is converting it fully and losing the device. Your call.

**4. Font delivery.** Google Fonts CDN is one link tag. Self-hosting woff2
matches what both AIMS and caliper actually do, survives a CDN block, and
removes a third-party request, at the cost of binary files in the repo. AIMS
self-hosts; I lean the same way, but the CDN gets us moving faster and can be
swapped later without touching anything but the token file.

**5. Figure family colors.** The three edge families (scores / events /
capital, currently `#2f6b9e` / `#3f7a47` / `#b05f14`) have no clean Stanford
mapping that does not collide with the actor hues above. Options are to run
them as neutrals, to run them at reduced saturation, or to accept the
collision, which already exists today. Lowest priority; belongs to Phase C.
