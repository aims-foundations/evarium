"""Prototype: (market structure, leader allocation, incident-burden) grid.

Two grids stacked vertically (structure on top, allocation below) with column
headers repeated above each. Column-order follows a thematic grouping
(baseline -> initial conditions -> market shape -> feedback/signals ->
evaluation & oversight). Per-row pie charts on the right of the structure
grid show incident burden attribution across providers, averaged across
conditions for that (mode, seed). Burden uses
`consumer_data.penalty_breakdown.{provider}.incident_penalty` summed across
rounds as a proxy (severity-weighted, decayed). See memory note
`future_work_incident_logging` for the upstream data gap.

Sizes scale off column/row counts; no hardcoded per-figure dimensions.
"""

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.plotting import PROVIDER_COLOR_MAP  # noqa: E402

HEURISTIC_ROOT = ROOT / "sandbox" / "experiments" / "heuristic"
LLM_ROOT       = ROOT / "sandbox" / "experiments" / "llm"

HEUR_RENAME = {
    "static_enterprise_size_balanced": "static_consumer_market_balanced",
}
SKIP_CONDITIONS = {"phase4_smoke_dyn"}
N_HEURISTIC_SEEDS = 5

# Thematic column ordering. Conditions present but not listed here get appended
# at the end; anything listed but missing from disk is silently dropped.
CONDITION_ORDER = [
    "full_ecosystem_balanced",
    "initial_uniform_balanced",
    "initial_leader_balanced",
    "initial_duopoly_balanced",
    "fixed_market_size_balanced",
    "static_enterprise_size_balanced",
    "homogeneous_consumers_balanced",
    "no_opensource_balanced",
    "no_media_balanced",
    "no_funders_balanced",
    "no_incidents_balanced",
    "no_product_channels_balanced",
    "aligned_benchmarks_balanced",
    "bm_orientation_adjustable_balanced",
    "bm_orientation_max_balanced",
    "dynamic_evaluator_balanced",
    "eval_as_company_balanced",
    "no_regulator_balanced",
]

PORTFOLIO_COLORS = {
    "rd":      "#555555",
    "safety":  "#D55E00",
    "product": "#BBBBBB",
}

MIN_SLIVER = 0.01
CELL_BORDER_WIDTH = 0.9


def load_all_rounds(path: Path):
    if not path.exists():
        return None
    rounds = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                rounds.append(json.loads(line))
    return rounds or None


def end_state(rounds):
    return rounds[-1] if rounds else None


def discover_conditions():
    available_llm = {p.name for p in LLM_ROOT.iterdir() if p.is_dir()
                     and p.name.endswith("_balanced") and p.name not in SKIP_CONDITIONS}
    ordered = [c for c in CONDITION_ORDER if c in available_llm]
    remainder = sorted(available_llm - set(CONDITION_ORDER))
    if remainder:
        print(f"note: appending unordered conditions: {remainder}")
    ordered.extend(remainder)

    conds = []
    for name in ordered:
        heur_name = HEUR_RENAME.get(name, name)
        if not (HEURISTIC_ROOT / heur_name / "seeds").exists():
            print(f"warning: heuristic dir missing for {name!r}; dropping")
            continue
        conds.append((name, heur_name))
    return conds


def discover_seeds(conds):
    heur_intersect = None
    llm_union = set()
    for _, heur_name in conds:
        heur_seeds = {p.name for p in (HEURISTIC_ROOT / heur_name / "seeds").iterdir() if p.is_dir()}
        heur_intersect = heur_seeds if heur_intersect is None else heur_intersect & heur_seeds
    for name, _ in conds:
        llm_dir = LLM_ROOT / name / "seeds"
        if llm_dir.exists():
            for p in llm_dir.iterdir():
                if p.is_dir():
                    llm_union.add(p.name)
    heur_sel = sorted(heur_intersect or set())[:N_HEURISTIC_SEEDS]
    llm_sel  = sorted(llm_union)
    return heur_sel, llm_sel


def build_rows(heur_seeds, llm_seeds):
    rows = [("heuristic", s) for s in heur_seeds]
    rows.append(("gap", None))
    rows.extend(("llm", s) for s in llm_seeds)
    return rows


def collect_runs(conds, rows):
    """Load all rounds per (cond, mode, seed). Returns {(cond, mode, seed): [rounds] | None}."""
    runs = {}
    for name, heur_name in conds:
        for mode, seed in rows:
            if mode == "gap":
                continue
            root = HEURISTIC_ROOT / heur_name if mode == "heuristic" else LLM_ROOT / name
            path = root / "seeds" / seed / "rounds.jsonl"
            runs[(name, mode, seed)] = load_all_rounds(path)
    return runs


def structure_segments(shares: dict):
    total = sum(max(v, 0) for v in shares.values())
    if total <= 0:
        return []
    filt = [(n, v / total) for n, v in shares.items() if v / total >= MIN_SLIVER]
    filt.sort(key=lambda kv: kv[1], reverse=True)
    renorm = sum(s for _, s in filt)
    return [(n, s / renorm) for n, s in filt]


def allocation_segments(port: dict):
    return [("rd", port["rd"]), ("safety", port["safety"]), ("product", port["product"])]


def incident_burden_shares(rounds):
    """Sum incident_penalty per provider across rounds; return normalized shares dict."""
    totals = {}
    for r in rounds:
        pb = r.get("consumer_data", {}).get("penalty_breakdown", {})
        for prov, d in pb.items():
            totals[prov] = totals.get(prov, 0.0) + max(d.get("incident_penalty", 0.0), 0.0)
    s = sum(totals.values())
    if s <= 0:
        return {}
    return {p: v / s for p, v in totals.items()}


def draw_bar(ax, segments, colors):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    x = 0.0
    for name, frac in segments:
        if frac <= 0:
            continue
        ax.add_patch(Rectangle((x, 0), frac, 1, facecolor=colors.get(name, "#888"),
                               edgecolor="white", linewidth=0.3))
        x += frac
    ax.add_patch(Rectangle((0, 0), 1, 1, fill=False, edgecolor="#222",
                           linewidth=CELL_BORDER_WIDTH))


def draw_missing(ax):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.add_patch(Rectangle((0, 0), 1, 1, facecolor="white",
                           edgecolor="#bbb", linewidth=CELL_BORDER_WIDTH, hatch="///"))


def draw_pie(ax, shares: dict):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    if not shares:
        ax.text(0.5, 0.5, "—", ha="center", va="center", color="#888",
                fontsize=8, transform=ax.transAxes)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        return
    # Stable provider order for pie slices.
    order = [p for p in PROVIDER_COLOR_MAP if p in shares and shares[p] > 0]
    sizes  = [shares[p] for p in order]
    colors = [PROVIDER_COLOR_MAP[p] for p in order]
    ax.pie(sizes, colors=colors, startangle=90,
           wedgeprops={"edgecolor": "white", "linewidth": 0.5})
    ax.set_aspect("equal")


def render_grid(ax_target, conds, rows, runs, which, fig):
    bbox = ax_target.get_position()
    ax_target.axis("off")
    n_cols = len(conds)

    row_heights = [0.3 if mode == "gap" else 1.0 for mode, _ in rows]
    total_h = sum(row_heights)
    y_fracs = [h / total_h for h in row_heights]

    cell_w = bbox.width / n_cols * 0.94
    col_gap = (bbox.width - cell_w * n_cols) / (n_cols - 1) if n_cols > 1 else 0

    y_cursor = bbox.y0 + bbox.height
    for r_idx, (mode, seed) in enumerate(rows):
        row_h_total = y_fracs[r_idx] * bbox.height
        y_cursor -= row_h_total
        if mode == "gap":
            divider_y = y_cursor + row_h_total / 2
            fig.add_artist(plt.Line2D(
                [bbox.x0, bbox.x0 + bbox.width], [divider_y, divider_y],
                color="#555", linewidth=1.0, transform=fig.transFigure,
            ))
            continue
        cell_h = row_h_total * 0.84
        pad = (row_h_total - cell_h) / 2
        for c_idx, (cond_name, _) in enumerate(conds):
            cx = bbox.x0 + c_idx * (cell_w + col_gap)
            ax = fig.add_axes([cx, y_cursor + pad, cell_w, cell_h])
            end = end_state(runs[(cond_name, mode, seed)])
            if end is None:
                draw_missing(ax)
                continue
            if which == "struct":
                segs = structure_segments(end["consumer_data"]["market_shares"])
                draw_bar(ax, segs, PROVIDER_COLOR_MAP)
            else:
                shares = end["consumer_data"]["market_shares"]
                leader = max(shares, key=shares.get)
                segs = allocation_segments(end["strategies"][leader])
                draw_bar(ax, segs, PORTFOLIO_COLORS)


def render_pies(ax_target, conds, rows, runs, fig, pie_bbox):
    """Render one pie per data row, aligned vertically with ax_target's rows.

    pie_bbox is the figure-coord rectangle where pies live (right of ax_target).
    """
    bbox = ax_target.get_position()
    row_heights = [0.3 if mode == "gap" else 1.0 for mode, _ in rows]
    total_h = sum(row_heights)
    y_fracs = [h / total_h for h in row_heights]

    y_cursor = bbox.y0 + bbox.height
    for r_idx, (mode, seed) in enumerate(rows):
        row_h_total = y_fracs[r_idx] * bbox.height
        y_cursor -= row_h_total
        if mode == "gap":
            continue
        # Aggregate across conditions for this row.
        per_prov = {}
        n_runs = 0
        for cond_name, _ in conds:
            rounds = runs[(cond_name, mode, seed)]
            if rounds is None:
                continue
            s = incident_burden_shares(rounds)
            if not s:
                continue
            n_runs += 1
            for p, v in s.items():
                per_prov[p] = per_prov.get(p, 0.0) + v
        if n_runs > 0:
            per_prov = {p: v / n_runs for p, v in per_prov.items()}
        side = min(row_h_total * 0.80, pie_bbox[2])
        cy = y_cursor + row_h_total / 2 - side / 2
        cx = pie_bbox[0] + (pie_bbox[2] - side) / 2
        ax = fig.add_axes([cx, cy, side, side])
        draw_pie(ax, per_prov)


def add_titles_headers(fig, ax_struct, ax_alloc, conds, col_label_fs,
                       title_gap=0.065, header_gap=0.006):
    for ax, title in [(ax_struct, "market structure (end-state)"),
                      (ax_alloc,  "leader portfolio (rd / safety / product)")]:
        b = ax.get_position()
        fig.text(b.x0 + b.width / 2, b.y0 + b.height + title_gap, title,
                 ha="center", fontsize=13, fontweight="bold")
        col_w = b.width / len(conds)
        for c_idx, (cond_name, _) in enumerate(conds):
            label = cond_name.replace("_balanced", "").replace("_", "\n")
            fig.text(b.x0 + c_idx * col_w + col_w / 2, b.y0 + b.height + header_gap,
                     label, ha="center", va="bottom",
                     fontsize=col_label_fs, fontweight="bold", color="#222",
                     linespacing=0.9)


def add_block_labels(fig, ax_struct, rows):
    b = ax_struct.get_position()
    row_heights = [0.3 if mode == "gap" else 1.0 for mode, _ in rows]
    total_h = sum(row_heights)

    blocks = {}
    cur = None; block_top = block_bot = None
    y_cursor = b.y0 + b.height
    for r_idx, (mode, _) in enumerate(rows):
        top = y_cursor
        y_cursor -= (row_heights[r_idx] / total_h) * b.height
        bot = y_cursor
        if mode == "gap":
            if cur is not None:
                blocks[cur] = (block_bot, block_top); cur = None
            continue
        if cur != mode:
            if cur is not None:
                blocks[cur] = (block_bot, block_top)
            cur = mode; block_top = top
        block_bot = bot
    if cur is not None:
        blocks[cur] = (block_bot, block_top)

    pretty = {"heuristic": "heuristic", "llm": "LLM"}
    for mode, (y_bot, y_top) in blocks.items():
        fig.text(b.x0 - 0.012, (y_bot + y_top) / 2, pretty[mode],
                 ha="right", va="center", fontsize=12, fontweight="bold",
                 color="#222", rotation=90)


def add_pie_label(fig, ax_struct, pie_bbox):
    b = ax_struct.get_position()
    fig.text(pie_bbox[0] + pie_bbox[2] / 2, b.y0 + b.height + 0.006,
             "incident\nburden\nby provider", ha="center", va="bottom",
             fontsize=8, fontweight="bold", color="#222", linespacing=0.95)


def add_legend(fig, legend_box):
    """Draw provider (left half) and portfolio (right half) legends in one strip."""
    lx, ly, lw, lh = legend_box

    def draw_block(x0, width, items, n_cols, title,
                   swatch_w=0.016, swatch_h=0.22,
                   fontsize=11, title_fs=11):
        ax = fig.add_axes([x0, ly, width, lh])
        ax.axis("off")
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.text(0.0, 0.92, title, fontweight="bold", fontsize=title_fs,
                va="top", transform=ax.transAxes)
        n_rows = (len(items) + n_cols - 1) // n_cols
        col_w = 1.0 / n_cols
        row_y_positions = [0.58 - r * 0.36 for r in range(n_rows)]
        for idx, (name, color) in enumerate(items):
            row = idx // n_cols
            col = idx % n_cols
            x = col * col_w
            y = row_y_positions[row]
            ax.add_patch(Rectangle((x, y - swatch_h / 2), swatch_w, swatch_h,
                                   facecolor=color, edgecolor="none",
                                   transform=ax.transAxes))
            ax.text(x + swatch_w + 0.010, y, name, fontsize=fontsize,
                    va="center", transform=ax.transAxes)

    half = lw / 2
    draw_block(lx,           half - 0.01, list(PROVIDER_COLOR_MAP.items()),
               n_cols=3, title="providers")
    draw_block(lx + half + 0.01, half - 0.01, list(PORTFOLIO_COLORS.items()),
               n_cols=3, title="portfolio")


def column_label_fontsize(n_cols):
    if n_cols <= 4:  return 10
    if n_cols <= 9:  return 9
    if n_cols <= 14: return 7
    return 6


def figure_size(n_cols, n_data_rows):
    fig_w = 0.58 * n_cols + 2.5
    fig_h = 0.42 * n_data_rows * 2 + 3.5
    return fig_w, fig_h


def main():
    conds = discover_conditions()
    heur_seeds, llm_seeds = discover_seeds(conds)
    rows = build_rows(heur_seeds, llm_seeds)
    runs = collect_runs(conds, rows)

    n_cols = len(conds)
    n_data_rows = sum(1 for m, _ in rows if m != "gap")
    print(f"conditions ({n_cols}): {[c[0].replace('_balanced','') for c in conds]}")
    print(f"heuristic seeds ({len(heur_seeds)}): {heur_seeds}")
    print(f"llm seeds ({len(llm_seeds)}): {llm_seeds}")

    fig_w, fig_h = figure_size(n_cols, n_data_rows)
    fig = plt.figure(figsize=(fig_w, fig_h))

    # ---- Layout in figure coords, computed top-down. ----
    top_margin       = 0.02
    title_h          = 0.03
    header_h         = 0.08   # column labels
    header_title_gap = 0.01
    inter_section    = 0.03   # gap between bottom of top grid and top of bottom title
    legend_h         = 0.06
    bottom_margin    = 0.02

    left_margin      = 0.05
    right_margin     = 0.02
    pie_gutter_w     = 0.09
    pie_gap          = 0.01

    grid_left  = left_margin
    grid_right = 1 - right_margin - pie_gutter_w - pie_gap
    grid_w     = grid_right - grid_left
    pie_bbox_x = grid_right + pie_gap
    pie_bbox_w = pie_gutter_w

    # Vertical budget: two grids of equal height, each with title + headers above.
    total_non_grid = (top_margin + 2 * (title_h + header_title_gap + header_h)
                      + inter_section + legend_h + bottom_margin)
    grid_h = (1 - total_non_grid) / 2

    # Top grid (structure).
    struct_top_edge = 1 - top_margin - title_h - header_title_gap - header_h
    struct_y        = struct_top_edge - grid_h
    # Bottom grid (allocation).
    alloc_top_edge  = struct_y - inter_section - title_h - header_title_gap - header_h
    alloc_y         = alloc_top_edge - grid_h

    ax_struct = fig.add_axes([grid_left, struct_y, grid_w, grid_h])
    ax_alloc  = fig.add_axes([grid_left, alloc_y,  grid_w, grid_h])

    pie_bbox = (pie_bbox_x, struct_y, pie_bbox_w, grid_h)
    legend_box = (grid_left, bottom_margin, 1 - grid_left - right_margin, legend_h)

    render_grid(ax_struct, conds, rows, runs, which="struct", fig=fig)
    render_grid(ax_alloc,  conds, rows, runs, which="alloc",  fig=fig)
    render_pies(ax_struct, conds, rows, runs, fig, pie_bbox)

    col_label_fs = column_label_fontsize(n_cols)
    add_titles_headers(fig, ax_struct, ax_alloc, conds, col_label_fs,
                       title_gap=header_h + header_title_gap,
                       header_gap=0.006)
    add_block_labels(fig, ax_struct, rows)
    add_block_labels(fig, ax_alloc, rows)
    add_pie_label(fig, ax_struct, pie_bbox)
    add_legend(fig, legend_box)

    out = ROOT / "output" / "prototype"
    out.mkdir(parents=True, exist_ok=True)
    out_path = out / "full_grid.png"
    fig.savefig(out_path, dpi=180)
    print(f"wrote {out_path}")

    missing = [(c, m, s) for (c, m, s), v in runs.items() if v is None]
    print(f"missing cells: {len(missing)}")


if __name__ == "__main__":
    main()
