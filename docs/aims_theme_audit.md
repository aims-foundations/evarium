# AIMS / Stanford theme audit

Gathered 2026-09-03 for retheming the evaluarium site to sit under
`aimslab.stanford.edu`. **Information only.** No styling decisions are made
here, and nothing in `website/client` has been changed.

Sources are the live stylesheets, not the guideline prose: values below were
read out of `aimslab.stanford.edu`'s own CSS bundles and out of
`benchmark-caliper`'s, then cross-checked against computed styles in the
browser. Where the Stanford identity site is quoted, it is the identity site.

---

> **Resolved 2026-09-03 (YD): follow the live aimslab site (`rd-*`), not
> benchmark-caliper.** The section below is kept because it records what the
> two options were and why the choice was not obvious. Everything downstream
> targets Theme A. Theme B is now reference only, useful mainly as the worked
> example of packaging a self-contained static app at this mount point.
>
> Licensing checked and clear: Google Sans Flex was released under the SIL
> Open Font License in November 2025 and is on Google Fonts, so AIMS's display
> face is ours to use.

## The finding that decides everything else

**AIMS is running two different design systems right now, and the sibling app
we were told to mirror uses the older one.**

| | Live `aimslab.stanford.edu` pages | `aimslab.stanford.edu/benchmark-caliper/` |
|---|---|---|
| CSS namespace | `.rd-*` (`rd-root`, `rd-h2`, `rd-paper-card`, ...) | plain element + `.site-*` selectors |
| Display face | **Google Sans Flex**, weight 300 | **Source Serif 4**, weight 400 |
| Body face | Google Sans Flex 300 | Source Sans 3 400 |
| Page ground | warm off-white `#f3efec` | white `#ffffff` |
| Serif used for | paper/citation titles only (Times New Roman) | all headings |
| Header | fixed, transparent then `--rd-warm` on scroll, pill nav | sticky, white 95% + blur, underline nav |
| Buttons | black pill, uppercase Roboto Mono, cardinal on hover | cardinal rectangle, 6px radius, sans 600 |
| Nav contents | Research / Data & Software / Education / Community / Blog | Research / Competition / Workshop / Education (stale) |

Both are AIMS, both are inside Stanford's identity, and they do not look like
each other. The `type-*` / `panel` / `section-band` token set still shipped in
the main site's global stylesheet is the one caliper was built against; the
site itself has since moved to `rd-*` and left those tokens unreferenced on
the pages checked.

So "match aimslab" is ambiguous, and it is the one thing to settle before any
CSS gets written. The two readings:

- **Match the live site (`rd-*`).** The visitor arriving from AIMS nav sees no
  seam. Cost: a full rebuild of our type system around a grotesk at weight
  300, and we inherit a look that is itself new and may keep moving.
- **Match caliper.** The precedent for an embedded static app at this exact
  mount point, self-contained, self-hosted fonts, no build step, and closest
  to the Stanford identity guidance as written (Source Serif + Source Sans are
  the *official* pairing; Google Sans Flex is not a Stanford typeface at all).
  Cost: our page looks a half-generation behind the site linking to it.

Worth noting caliper's nav is stale, which suggests it was themed once and has
not tracked the parent since. Whatever we pick, it will drift the same way
unless someone owns re-syncing it.

---

## Stanford identity guidance (identity.stanford.edu)

The general layer. Thin on specifics; it defers to sub-pages and to Decanter,
Stanford's CSS framework.

**Typefaces** (`/design-elements/typography/`)

- Primary: **Source Sans 3** (body) + **Source Serif 4** (complementary).
  Both Google Fonts.
- Accent: Roboto, Roboto Condensed, **Roboto Mono**, Roboto Slab.
- Leading: start 2 to 4 points above the point size.
- Tracking: optical kerning, adjust by eye.

**Web interactive colors** (`/design-elements/color/web/`) - digital only, and
each has a defined job:

| Token | Primary | Light | Dark | Sanctioned use |
|---|---|---|---|---|
| Digital red | `#b1040e` | `#e50808` | `#820000` | buttons, rollovers, alerts. Not a Cardinal substitute; never on the wordmark |
| Digital blue | `#006cb8` | `#6fc3ff` | `#00548f` | **links only.** dark = hover/focus, light = links on dark |
| Digital green | `#008566` | `#1aecba` | `#006f54` | form validation. dark = hover/focus |

**Accessibility** is stated as a requirement, not a nicety: WCAG AA, minimum
3.0 contrast for headings and bold text, 4.5 for paragraph text. The web-design
page adds "don't treat accessibility as an add-on" and a rough-and-ready "50%
contrast between elements."

Also referenced: [Decanter](https://decanter.stanford.edu/) (Stanford's own
CSS/JS framework), [minweb.stanford.edu](http://minweb.stanford.edu/) minimum
standards, and the UIT online accessibility policy.

---

## AIMS palette (identical in both AIMS themes)

Straight from `:root` in the AIMS global bundle. This is Stanford's palette
verbatim, so it is the least contested part of the whole exercise.

```
--white        #fff        --cardinal      #8c1515
--fog-light    #f4f4f4     --digital-red   #b1040e
--fog          #dad7cb     --digital-blue  #006cb8
--black        #2e2d29     --digital-green #008566
--cool-grey    #53565a     --stone         #7f7776

--palo-alto    #175e54   light #2d716f   dark #014240
--lagunita     #007c92   light #009ab4   dark #006b81
--sky          #4298b5   light #67afd2
--poppy        #e98300
--plum         #620059

--black-90 #43423e   --black-80 #585754   --black-60 #767674
--black-30 #c0c0bf   --black-20 #d5d5d4   --black-10 #eaeaea

--ink var(--black)   --muted var(--cool-grey)   --line var(--black-20)
--text-secondary #585754   --text-tertiary #767674
--text-on-dark #ffffffb3   --text-on-dark-muted #ffffffa6
```

Body text is `--black` `#2e2d29` on `--white`. Focus ring everywhere is
`2px solid var(--digital-blue)` at `2px` offset. Selection is `#8c15152e`
(cardinal at 18%).

---

## Theme A: the live site (`rd-*`)

Scoped under `.rd-root`, which wraps the whole document including the 404 page.

**Fonts**

```
--rd-grotesk  "Google Sans Flex", "Helvetica Neue", Arial, sans-serif
--rd-serif    "Times New Roman", Times, serif
--rd-mono     "Roboto Mono", ui-monospace, monospace
```

Google Sans Flex is self-hosted as a variable font (`font-weight: 1 1000`,
ten `@font-face` slices, `font-display: swap`). It is **not** on Stanford's
approved typeface list. Base `line-height: 1.375`, `color: #000` (pure black,
not `--black`), ground `--rd-warm`.

**Its own palette layer**

```
--rd-warm      #f3efec     page ground
--rd-warm-2    #f6f2ee     hover ground, dropdown ground
--rd-beige     #f0e7de
--rd-sage      #eaf1ed     --rd-sage-dark #d8e4dd
--rd-cardinal  #8c1515     --rd-darkred #401415     --rd-dark #0d0f0f
--rd-accent    #e98300     (poppy, used for hover arrows)
--rd-hai-blue  #005fa3     --rd-hai-fig #72307c     --rd-hai-cyan #9cf2f2
```

The `--rd-hai-*` trio is Stanford HAI's palette, which is a useful signal
about where this design came from and where it is heading.

**Type scale** (all fluid, all weight 300, all tight tracking)

| Class | Size | Weight | Line height | Tracking |
|---|---|---|---|---|
| `.rd-display` | `clamp(2.5rem, 7vw, 6.75rem)` | 300 | .98 | -.045em |
| `.rd-page-title` | `clamp(2.35rem, 5.6vw, 4.5rem)` | 300 | 1 | -.035em |
| `.rd-h2` | `clamp(1.9rem, 3.8vw, 3.125rem)` | 300 | 1.04 | -.02em |
| `.rd-section-heading` | `clamp(2.4rem, 5vw, 4rem)` | 500 | - | -.025em |
| `.rd-h3` | `clamp(1.35rem, 2.2vw, 1.875rem)` | 300 | 1.15 | -.01em |
| `.rd-lead` | `clamp(1.15rem, 1.8vw, 1.5rem)` | 300 | 1.35 | - |
| `.rd-serif-title` | `1.5rem` Times | 400 | 1.17 | 0 |
| `.rd-mono` | `.75rem` Roboto Mono | 400 | - | .1em, uppercase |

The signature move is very large text at weight 300 with negative tracking.
Our current site does the opposite (small text, 400 to 700, normal tracking),
so this is the largest single delta.

**Layout**

- `.rd-container` `max-width: 1334px`, `padding-inline: clamp(20px, 3.5vw, 50px)`
- `.rd-band` `padding-block: clamp(56px, 8vw, 112px)` - the vertical rhythm
- Bands by ground: warm / white / sage / beige / cardinal / darkred / dark

**Components**

- `.rd-btn` black pill, `border-radius: 30px`, Roboto Mono `.75rem` uppercase
  `letter-spacing: .08em`, `padding: .55rem 1.35rem`, hovers to cardinal.
  Ghost variants use `currentColor` borders.
- `.rd-chip` same pill at `.66rem` on `--rd-warm`.
- `.rd-paper-card` white-at-68% on a hairline `#00000026` border, **serif
  title** `clamp(1.15rem, 1.55vw, 1.35rem)`, authors at `.82rem/1.45` opacity
  .7, and a mono uppercase meta footer at `.65rem` letter-spacing `.08em`
  above a `1px` top border. Hover lifts `translateY(-3px) scale(1.006)` with
  `box-shadow: 0 10px 24px #40141524` and a cardinal-tinted border.
  **This is the closest existing AIMS component to our paper/event rows.**
- `.rd-stat` mono value in cardinal at `clamp(1.9rem, 3.2vw, 2.6rem)` weight
  300, label `.9rem` weight 300 opacity .75.
- `.rd-prose a` inherits color, underlined in `#8c151559` (cardinal at 35%),
  `text-underline-offset: 3px`, going full cardinal on hover. Note this
  **departs from Stanford's digital-blue-for-links rule.**
- `.rd-row` list rows, `1px` bottom border, hover to `--rd-warm-2`.
- Nav pills go cardinal-filled with white text on hover.
- Corners: pill (`30px` / `9999px`) or square. No mid-radius anywhere.

**Motion** is a real part of the identity: `.reveal` fade-and-rise on scroll
with 80ms stagger, hero scan beam, and animated matrix/confusion-matrix cells
with breathe, drift and bloom phases. All of it is properly gated behind
`@media (prefers-reduced-motion: reduce)`.

**Backgrounds** are a set of measurement-flavored grid textures, and this is
what gives AIMS pages their signature: `bg-grid-dots` (24px radial dots),
`bg-dot-grid-fine` (12px), `bg-ruled-lines` (32px), `bg-axis-grid` (48px),
`bg-graph-paper` (80px + 16px), `bg-calibration-crosshairs`,
`bg-isometric-grid`. The homepage and Research hero use a scattered
grey/pink cell matrix over `--rd-warm`.

---

## Theme B: benchmark-caliper (the embedded-app precedent)

One stylesheet, 27KB, self-contained, no framework, fonts self-hosted as
woff2+woff under `/benchmark-caliper/assets/`. Structurally this is what we
already have, so a port here is a token swap rather than a rebuild.

```
--font-sans   "Source Sans 3", -apple-system, BlinkMacSystemFont, "Segoe UI",
              Roboto, Helvetica, Arial, sans-serif
--font-serif  "Source Serif 4", Georgia, "Iowan Old Style", Palatino,
              "Times New Roman", serif
--font-mono   "Roboto Mono", ui-monospace, SFMono-Regular, Menlo, Consolas,
              monospace
--radius-sm .375rem   --radius-md .5rem   --radius-lg .75rem
--site-header-h 4.25rem
--ease-out cubic-bezier(.16, 1, .3, 1)
```

Weights actually shipped: Source Sans 400/500/600/700, Source Serif 400 only,
Roboto Mono 400/500/700.

- Root `line-height: 1.55`, `--ink` on white.
- `h1` serif `clamp(2rem, 4vw, 2.6rem)` weight 400, `line-height 1.12`,
  tracking `-.015em`. `h2` serif `1.4rem` weight 400, `1.25`, `-.01em`.
- `.eyebrow` mono `.72rem` weight 500, `letter-spacing: .18em`, uppercase, in
  **cardinal** (the live site puts eyebrows in cool-grey instead).
- `.tagline` `1rem` in `--muted`. `.help` `.9rem` in `--muted`.
- `button` cardinal fill, `--radius-md`, weight 600, `.95rem`,
  `padding: .55rem 1.1rem`, hovering to `--digital-red`. `button.link` is
  digital-blue underlined, hovering to lagunita, with a `.danger` variant in
  digital-red hovering to cardinal.
- `code` mono `.88em` on `--fog-light` inside a `--black-10` border at
  `--radius-sm`.
- `.site-header` sticky, `#fffffff2` + `blur(4px)`, `1px --line` bottom,
  shell `max-width: 80rem`, padding `1rem` to `2rem` by breakpoint, nav links
  `.875rem` weight 500 in `--muted` going `--ink` when active, with a `2px`
  cardinal underline.
- Content column `max-width: 680px`; hero bleeds full width behind it.
- Errors: `border-left: 3px solid --digital-red` on `#fdf3f3`.

Caliper keeps Stanford's link rule (digital blue) where the live site does not.

---

## Where our site stands today

For sizing the work. Current values in `website/client`:

| | evaluarium now | AIMS live (`rd-*`) | caliper |
|---|---|---|---|
| Ground | `#f0e6d3` tan | `#f3efec` warm off-white | `#ffffff` |
| Ink | `#2a1a0e` warm brown-black | `#000` | `#2e2d29` |
| Secondary ink | `#5a4030`, `#3d2a1a`, `#7a6045` | opacity on black | `#53565a`, `#767674` |
| Accent | `#3d5a8a` slate blue | `#8c1515` cardinal | `#8c1515` cardinal |
| Sans | `"Inter", system-ui` | Google Sans Flex | Source Sans 3 |
| Serif | Playfair Display + Georgia (viewer only) | Times (paper titles) | Source Serif 4 |
| Body size | 13.5 to 14px | ~17.8px, weight 300 | ~16px |
| Content width | 880px (simulation), 1060px (index) | 1334px | 680px |

Two things to flag before any retheme starts:

1. **Inter is declared but never loaded** on `index`, `simulation`, `explorer`
   and `compare`. Only `viewer.html` pulls it from Google Fonts.
   *Corrected 2026-09-03:* measuring in the browser showed Inter **is**
   installed locally on this machine, so those pages have been rendering in
   real Inter here, and in `system-ui` (Segoe UI, SF) for anyone without it.
   The defect is not that nobody saw Inter, it is that the pages set type
   differently depending on the reader's installed fonts. A font decision
   should pin a loaded webfont rather than inherit this.
2. **Our warm ground is close to, but not, the AIMS warm ground.** `#f0e6d3`
   against `#f3efec` is a shift from tan toward near-white grey. It is a small
   hex delta and a large perceptual one, and it is the change that would make
   the site read as AIMS rather than as ours.

The main diagram is the hard part: font sizes there were hand-tuned to
8 to 12.5px across three passes last session, label boxes are solved against
those exact sizes (`w = len * 8 * 0.52 + 7`), and the R5/R6 collision rules
were verified at those sizes. Any change to the figure's type will invalidate
the solved label positions and require re-running the harness.

---

## Not yet checked

- Whether AIMS has an internal brand kit, Figma file or component library
  beyond what is compiled into the shipped CSS.
- Whether Decanter is expected for Stanford sub-sites, or is optional.
- Whether the `rd-*` theme is finished or mid-rollout, and who owns it.
- Mobile rendering of either theme. Everything above was read at 1456px.
- Whether AIMS wants our page to carry the AIMS header at all, or to sit bare
  inside their chrome. Caliper carries its own recreated header, which is why
  its nav has gone stale.
