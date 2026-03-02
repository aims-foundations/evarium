# mainfig_option1.tex — Figure Specification & TikZ Notes

## Purpose
Hexagonal ecosystem wheel showing 6 actors around a "Public Signals" center, with
spoke arrows (observe/contribute), 4 outer feedback loop arcs, annotation boxes,
concentric info-tier shading, and a legend. Intended as the paper's main figure.

---

## Final Design Decisions

### Actor arrangement — clockwise from top
Conceptual narrative order (not strict simulation round order):

| Position | Angle | Actor | Sublabel |
|----------|-------|-------|----------|
| Top | 90° | Model Providers | 6 providers |
| Top-right | 30° | Evaluator | 8 benchmark domains |
| Right | -30° | Consumer Market | 39 segments |
| Bottom | -90° | Media | 1 outlet (TechPress) |
| Bottom-left | -150° / 210° | Policymakers | 3 regulatory presets |
| Top-left | 150° | Funders | 3 types: VC, gov, foundation |

Rationale: Providers act → Evaluator scores → Consumers interact and experience incidents
→ Media reports on incidents (moderate+) → Policymakers observe and intervene
→ Funders allocate capital → back to Providers.

Actor radius: 4.5cm from center. Sublabels in \tiny unbolded text on the line below the actor name, same color as border but lighter.

---

### Center node
- Style: ellipse, fill=tierPub (#DBEAFE), border=Ccore (#1E293B)
- Label: **Public Signals** (bold), then tiny text:
  leaderboard · market shares / incidents · interventions / media coverage

---

### Concentric background rings
- Inner ring radius 3.6cm: fill tierPub (#DBEAFE) at 42% opacity — labeled "Public" (rotated 90°, left side)
- Outer ring radius 5.5cm: fill tierPriv (#F0FDF4) at 35% opacity — labeled "Private" (rotated 90°, left side)
- Dashed circle borders at both radii

---

### Spoke arrows — center ↔ actor

Only show non-obvious, mechanistically important signals. Two arrows per actor max.

**Solid arrow: center → actor (what actor observes)**

| Actor | Label |
|-------|-------|
| Model Providers | competitor scores, sanctions |
| Evaluator | *(remove — Evaluator produces the leaderboard, doesn't consume it)* |
| Consumer Market | scores, incidents, sentiment |
| Media | *(remove — its triggers are already listed in center node)* |
| Policymakers | inflation, incidents |
| Funders | scores, media risk signals |

**Dashed arrow: actor → center (what actor contributes)**

| Actor | Label |
|-------|-------|
| Model Providers | *(remove — Evaluator publishes their scores, not them directly)* |
| Evaluator | leaderboard |
| Consumer Market | market shares |
| Media | coverage, sentiment |
| Policymakers | warnings, sanctions |
| Funders | *(remove — funding_multiplier is a direct private effect on providers, never enters public signals)* |

---

### Outer feedback loop arcs (between actor nodes, not through center)

4 loops, color-coded. Each arc stays outside the public ring.

| Loop | Color | Arcs | Label style |
|------|-------|------|-------------|
| A Benchmark–Training | #E11D48 (red) | Provider → Evaluator (solid, bend left ~42°) | forward arc only |
| A return | #E11D48 dashed | Evaluator → Provider (dashed, bend left ~32°) | Goodhart decay |
| B Media Influence | #2563EB (blue) | Media → Consumer Market (solid) | direct sentiment effect |
| C Regulatory | #059669 (green) | Consumer → Policymakers (solid) + Policymakers → Providers (solid, wide outer arc) | two-arc chain |
| D Capital | #D97706 (orange) | Funders → Providers (solid) | funding multiplier |

Drop the "Loop return path" legend entry — the dashed red arc is just labeled "Goodhart decay" directly.

---

### Annotation boxes (one per loop, outside the wheel)

| Loop | Position | Content |
|------|----------|---------|
| A | top-center, anchor=south, ~(1.6, 6.6) | Benchmark–Training / eval_eng → score via β / Goodhart: α↓, β↑ each round / Benchmark retires at ŝ≥0.90 |
| B | bottom, anchor=north, ~(0, -6.2) | Media Influence / sentiment modulates consumer belief update rate / risk signals raise policymaker gaming_risk / believed_gaming raised for funders |
| C | bottom-left, anchor=north east, ~(-0.5, -6.8) | Regulatory / EU: threshold 0.35, fine ×0.35 / US: threshold 0.75, fine ×0.10 / invest. → warn → mandate → audit → sanctions |
| D | top-left, anchor=south east, ~(-1.0, 7.0) OR right side below legend | Capital / VC/Gov/Foundation signals: / scores, market traction, media risk / OS providers: VC-exempt |

**Important**: the legend panel sits at shift=(6.7, 6.5) and spans to x≈10.85. The Capital box must not overlap it — place below legend or on left side.

---

### Legend (top-right corner, shift=(6.7, 6.5))
Panel: white fill, Ccore!22 border, rounded corners.
Contents (top to bottom):
- "Legend" title
- Info tiers: Public swatch (tierPub) + Private swatch (tierPriv)
- Spoke arrows: solid = actor observes / dashed = actor contributes
- Feedback loops: colored lines for A (red), B (blue), C (green), D (orange)
- Remove "Loop return path" entry — redundant

---

## Color Definitions

```latex
\definecolor{Cprov}{HTML}{1D4ED8}   % Model Providers
\definecolor{Ceval}{HTML}{047857}   % Evaluator
\definecolor{Cfund}{HTML}{D97706}   % Funders
\definecolor{Cpol} {HTML}{7C3AED}   % Policymakers
\definecolor{Ccons}{HTML}{B91C1C}   % Consumer Market
\definecolor{Cmed} {HTML}{4F46E5}   % Media
\definecolor{Ccore}{HTML}{1E293B}   % center / neutral
\definecolor{loopA}{HTML}{E11D48}
\definecolor{loopB}{HTML}{2563EB}
\definecolor{loopC}{HTML}{059669}
\definecolor{loopD}{HTML}{D97706}
\definecolor{tierPub} {HTML}{DBEAFE}
\definecolor{tierPriv}{HTML}{F0FDF4}
```

---

## TikZ Node Styles

```latex
actor/.style={
    rectangle, rounded corners=5pt,
    minimum width=2.6cm, minimum height=1.0cm,
    text width=2.4cm, align=center,
    font=\sffamily\small\bfseries,
    draw=#1, fill=white, line width=1.2pt, text=#1
}
centernode/.style={
    ellipse, minimum width=3.5cm, minimum height=2.0cm,
    align=center, font=\sffamily\small,
    draw=Ccore, fill=tierPub, line width=1.5pt, text=Ccore
}
oblbl/.style={   % observe label
    font=\sffamily\tiny, text=#1,
    fill=white, fill opacity=0.93, text opacity=1,
    inner sep=1.2pt, align=center
}
contlbl/.style={ % contribute label (italic)
    font=\sffamily\tiny\itshape, text=#1,
    fill=white, fill opacity=0.93, text opacity=1,
    inner sep=1.2pt, align=center
}
loopfwd/.style={->, line width=1.6pt, color=#1, shorten >=5pt, shorten <=5pt}
loopret/.style={->, line width=1.1pt, color=#1, dashed, shorten >=5pt, shorten <=5pt}
annbox/.style={
    rectangle, rounded corners=4pt,
    draw=#1!60, fill=#1!8, line width=0.9pt,
    font=\sffamily\tiny, inner sep=4pt, align=left,
    text width=2.8cm
}
```

---

## TikZ Pitfalls Encountered

1. **Inline arc labels at fixed coordinates**: placing `\node` at hardcoded `(x,y)` to label an arc does not guarantee the node sits on the arc. If the arc bends, the label floats far away or gets cut at the figure border. **Fix**: remove inline arc labels entirely; use annotation boxes outside the wheel instead.

2. **Annotation box hidden by legend**: the legend panel uses `\fill[white]` which paints over anything drawn before it (or under it if drawn after). The Capital box at `(6.6, 1.2)` was inside the legend's x-range (6.55–10.85) and got covered. **Fix**: always check annotation box coordinates against the legend panel's bounding box; place boxes outside that rectangle.

3. **`text=#1` in parameterized styles**: `actor/.style={..., text=#1}` works but the color applies to all text in the node including sublabels. To make sublabels lighter, wrap them in `{\color{#1!60}\tiny ...}` inside the node text.

4. **Multi-line node labels with `\\`**: requires `align=center` (or `align=left`) in the node style. Without it, `\\` is silently ignored and text runs together.

5. **`to[bend left=N]` for dashed return arcs**: the `bend left` value needs to be slightly smaller than the forward arc's bend to visually separate the two arcs. Use ~42° forward and ~32° return for the Benchmark–Training loop.

6. **`on background layer` scope**: all outer loop arcs should be inside `\begin{scope}[on background layer]` so they render behind actor boxes. Otherwise arcs overdraw node borders.

7. **`\begin{scope}[on background layer]`** must be paired with the `backgrounds` tikz library: `\usetikzlibrary{arrows.meta, backgrounds, calc, shapes.geometric}`.

8. **Standalone border**: `\documentclass[border=10pt]{standalone}` clips to the bounding box of all content + 10pt padding. Any node placed far from the wheel will expand the page. Keep annotation boxes within ~7–8cm of center to avoid an excessively wide figure.

9. **Actor node anchors for spoke arrows**: use named anchors like `.south`, `.north east` rather than center-to-center lines to avoid arrows terminating in the middle of node boxes.

10. **`loopD` and `Cfund` share the same hex color (#D97706)**: this is intentional (Funders = orange = Capital loop color). But define them separately in case one changes.

---

## Libraries Required

```latex
\usetikzlibrary{arrows.meta, backgrounds, calc, shapes.geometric}
```
- `arrows.meta`: for `>=Stealth` arrowheads
- `backgrounds`: for `on background layer` scope
- `calc`: for `$(A)!t!(B)$` midpoint interpolation in spoke label positioning
- `shapes.geometric`: for ellipse centernode style

---

## Compilation

```bash
cd overleaf/figures
pdflatex -interaction=nonstopmode mainfig_option1.tex
# Preview:
python -c "import fitz; doc=fitz.open('mainfig_option1.pdf'); pix=doc[0].get_pixmap(matrix=fitz.Matrix(2.5,2.5)); pix.save('mainfig_option1_preview.png')"
```
PyMuPDF (`pip install pymupdf`) required for preview. ImageMagick and pdftoppm not available in this environment.
