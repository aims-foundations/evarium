"""3x3 single-run dashboard composer.

Stitches the 9 panels + a metadata header strip into one figure, saved
alongside every LLM run.

Layout:
  P1 market share           P2 incidents+interventions   P3 per-benchmark scores
  P4 portfolio allocations  P5 score vs sat + reliab.    P6 per-benchmark dumbbell
  P7 funder allocation      P8 regulator heatmap         P9 media attention share

Usage:
  python scripts/dashboard/dashboard.py \\
    --run-dir sandbox/experiments/_core_privacy/llm/baseline_s42_sonnet/seeds/seed_42
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(Path(__file__).parent))

from plots.paper.single_run_loop import (  # noqa: E402
    _panel_market_share, _panel_incidents,
    _panel_allocations, _panel_dumbbell,
)
from plots.portfolio import extract_portfolio_data  # noqa: E402
from plotting import get_provider_colors  # noqa: E402

from panel3_benchmark_scores import draw_panel as panel3_draw, load_privacy_map, _BM_SHORT  # noqa: E402
from panel5_score_sat_reliability import draw_panel as panel5_draw  # noqa: E402
from panel7_funder_allocation import draw_panel as panel7_draw  # noqa: E402
from panel8_regulator_heatmap import draw_panel as panel8_draw  # noqa: E402
from panel9_media_attention import draw_panel as panel9_draw  # noqa: E402


PRIV_SUFFIX = {"public": "pub", "private": "priv", "partial": "part"}


def _panel_dumbbell_with_privacy(ax, rounds, privacy_map):
    """Wrap the existing dumbbell panel and append (priv)/(pub)/(part) to ylabels."""
    _panel_dumbbell(ax, rounds)
    new_labels = []
    for tick in ax.get_yticklabels():
        bm = tick.get_text()
        suf = PRIV_SUFFIX.get(privacy_map.get(bm, "public"), "pub")
        new_labels.append(f"{bm} ({suf})")
    ax.set_yticklabels(new_labels, fontsize=10)


def _header_strip(fig, run_dir: Path, cfg: dict, privacy_map: dict):
    parent = run_dir.parent
    if parent.name == "seeds":
        parent = parent.parent
    cond_label = parent.name
    seed = cfg.get("seed", "?")

    haystack = " ".join(p.lower() for p in run_dir.parts)
    if "gpt-5.5" in haystack or "_gpt55" in haystack:
        model = "gpt-5.5"
    elif "claude-sonnet" in haystack or "_sonnet" in haystack:
        model = "sonnet"
    elif "claude-opus" in haystack or "_opus" in haystack:
        model = "opus"
    elif "qwen" in haystack:
        model = "qwen"
    elif "llama" in haystack:
        model = "llama"
    elif "deepseek" in haystack:
        model = "deepseek"
    else:
        model = "?"

    eval_mode = cfg.get("evaluator_mode", "?")
    eval_lag = cfg.get("evaluation_lag", "?")
    n_rounds = cfg.get("n_rounds", "?")
    llm_mode = cfg.get("llm_mode", False)

    line1 = (f"Run: {cond_label}    seed {seed}    model: {model}    "
             f"evaluator: {eval_mode}, lag={eval_lag}    "
             f"{n_rounds} rounds    llm\\_mode={llm_mode}")
    fig.text(0.5, 0.985, line1, ha="center", va="top",
             fontsize=13, fontweight="bold", color="#222")

    by_status = {"public": [], "private": [], "partial": []}
    for bm, status in privacy_map.items():
        by_status.setdefault(status, []).append(_BM_SHORT.get(bm, bm[:8]))
    pub_n = len(by_status["public"]); pri_n = len(by_status["private"]); par_n = len(by_status["partial"])
    bm_summary = (f"Benchmarks: public ({pub_n}): {', '.join(by_status['public']) or '-'}    |    "
                  f"private ({pri_n}): {', '.join(by_status['private']) or '-'}    |    "
                  f"partial ({par_n}): {', '.join(by_status['partial']) or '-'}")
    fig.text(0.5, 0.962, bm_summary, ha="center", va="top",
             fontsize=9.5, color="#555")


def render(run_dir: Path, out_path: Path, save_pdf: bool = False):
    rounds = [json.loads(l) for l in (run_dir / "rounds.jsonl").read_text().splitlines() if l.strip()]
    cfg = json.loads((run_dir / "config.json").read_text()) if (run_dir / "config.json").is_file() else {}
    privacy_map = load_privacy_map(cfg)

    providers, T, portfolios, final_shares = extract_portfolio_data(rounds)
    providers = sorted(providers, key=lambda p: -final_shares.get(p, 0.0))
    p_colors = get_provider_colors(providers)

    fig = plt.figure(figsize=(24.0, 16.0), constrained_layout=False)
    gs = fig.add_gridspec(3, 3, top=0.905, bottom=0.045, left=0.040, right=0.992,
                          hspace=0.22, wspace=0.18)

    ax_p1 = fig.add_subplot(gs[0, 0]); _panel_market_share(ax_p1, rounds, providers, p_colors)
    ax_p2 = fig.add_subplot(gs[0, 1]); _panel_incidents(ax_p2, rounds, providers)
    ax_p3 = fig.add_subplot(gs[0, 2]); panel3_draw(ax_p3, rounds, privacy_map)

    ax_p4 = fig.add_subplot(gs[1, 0]); _panel_allocations(ax_p4, rounds, providers, portfolios, p_colors)
    ax_p4.set_title("(d) Portfolio allocations", fontsize=13, loc="left", fontweight="bold")
    ax_p5 = fig.add_subplot(gs[1, 1]); panel5_draw(ax_p5, rounds)
    ax_p6 = fig.add_subplot(gs[1, 2]); _panel_dumbbell_with_privacy(ax_p6, rounds, privacy_map)
    ax_p6.set_title("(f) Per-benchmark gap", fontsize=13, loc="left", fontweight="bold")

    ax_p7 = fig.add_subplot(gs[2, 0]); panel7_draw(ax_p7, rounds)
    ax_p8 = fig.add_subplot(gs[2, 1]); panel8_draw(ax_p8, rounds, providers)
    ax_p9 = fig.add_subplot(gs[2, 2]); panel9_draw(ax_p9, rounds)

    _header_strip(fig, run_dir, cfg, privacy_map)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=130)
    print(f"Saved: {out_path}")
    if save_pdf:
        fig.savefig(out_path.with_suffix(".pdf"))
        print(f"Saved: {out_path.with_suffix('.pdf')}")
    plt.close(fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--run-dir", type=Path, required=True)
    ap.add_argument("--out", type=Path,
                    default=Path("output/dashboard/dashboard.png"))
    ap.add_argument("--pdf", action="store_true",
                    help="Also save a PDF copy alongside the PNG.")
    args = ap.parse_args()
    render(args.run_dir, args.out, save_pdf=args.pdf)
