"""Path-dependence illustration: Orion market-share trajectory across seeds,
overlaid with critical + major incident markers.

Shows that the same provider archetype under the same calibration lands at
final shares ranging from ~0.1 to ~0.8, governed by incident timing+severity.

Reads from the canonical staging layout:
  hf_data_staging/<bucket>/llm/<model>/<cond>/seed_*/rounds.jsonl

Restricted to the 5 core privacy conditions (public_only / baseline /
private_dominant / private_only / iid_holdout); sequence-robustness
sub-conditions like s5_aligned_* / s8_agentic_* are excluded from the
"same calibration" figure framing.

Usage:
  python -m scripts.plots.paper.incident_path_dependence
"""
from __future__ import annotations
import argparse, glob, json, os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from .. import paths as _paths

PROVIDER = "Orion Labs"
SEV_MARK = {"major": ("^", "#E76F51", 50), "critical": ("X", "#D62828", 90)}

CORE_PRIVACY_CONDS = {
    "public_only", "baseline", "private_dominant", "private_only", "iid_holdout",
}

# Short labels used in run-name strings for legend / titles.
_MODEL_SHORT = {
    "claude-sonnet-4-6":     "sonnet",
    "claude-opus-4-6":       "opus",
    "gpt-5.5-2026-04-23":    "gpt55",
}


def load_trajectory(jsonl_path: str):
    rounds = [json.loads(l) for l in open(jsonl_path) if l.strip()]
    xs, ys = [], []
    incidents = []  # list of (round, severity)
    for r in rounds:
        xs.append(r["round"])
        ys.append(r["consumer_data"]["market_shares"].get(PROVIDER, 0.0))
        for inc in r.get("incidents", []):
            if inc.get("provider") == PROVIDER and inc.get("severity") in SEV_MARK:
                incidents.append((r["round"], inc["severity"]))
    return xs, ys, incidents, len(rounds)


def main(batch: str, out_dir: str, model_filter: str = "claude-sonnet-4-6",
         min_rounds: int = 40, conds: set[str] | None = None):
    """Walk hf_data_staging/<bucket>/llm/<model>/<cond>/seed_*/rounds.jsonl.

    `batch` accepts either the staging name (`core_privacy`) or the legacy
    sandbox form with leading underscore (`_core_privacy`); the underscore
    is stripped.
    """
    bucket = batch.lstrip("_")
    root = Path(_paths.PROJECT_ROOT) / "hf_data_staging" / bucket / "llm"
    if not root.is_dir():
        raise FileNotFoundError(f"Canonical staging dir not found: {root}")

    accepted_conds = conds if conds is not None else CORE_PRIVACY_CONDS
    runs = []
    for model_dir in sorted(root.iterdir()):
        if not model_dir.is_dir():
            continue
        if model_filter and model_dir.name != model_filter:
            continue
        model_short = _MODEL_SHORT.get(model_dir.name, model_dir.name)
        for cond_dir in sorted(model_dir.iterdir()):
            if not cond_dir.is_dir():
                continue
            cond = cond_dir.name
            if cond not in accepted_conds:
                continue
            for seed_dir in sorted(cond_dir.glob("seed_*")):
                if not seed_dir.is_dir():
                    continue
                try:
                    seed = int(seed_dir.name.split("_", 1)[1])
                except ValueError:
                    continue
                jsonl = seed_dir / "rounds.jsonl"
                if not jsonl.exists():
                    continue
                xs, ys, inc, n = load_trajectory(str(jsonl))
                if n < min_rounds:
                    continue
                runs.append({"cond": cond, "seed": seed, "xs": xs, "ys": ys,
                             "inc": inc, "model": model_short,
                             "name": f"{cond}_s{seed}_{model_short}",
                             "final": ys[-1]})
    if not runs:
        raise FileNotFoundError(
            f"No {min_rounds}-round runs found under {root} "
            f"(model={model_filter}, conds={sorted(accepted_conds)})")
    print(f"Loaded {len(runs)} runs across {len({r['cond'] for r in runs})} conditions: "
          f"{sorted({(r['cond'], r['seed']) for r in runs}, key=lambda x: (x[0], x[1]))[:6]}...")

    # Identify exemplars: worst-final-share (early wipeout) and best-final-share (recovery + dominance)
    runs_sorted = sorted(runs, key=lambda r: r["final"])
    wipeout = runs_sorted[0]
    dominator = runs_sorted[-1]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    # All trajectories thin + light
    for r in runs:
        is_exemplar = r["name"] in (wipeout["name"], dominator["name"])
        if is_exemplar:
            continue
        ax.plot(r["xs"], r["ys"], color="#808080", lw=0.9, alpha=0.45, zorder=2)
        # critical incidents only on background lines
        for rnd, sev in r["inc"]:
            if sev == "critical":
                mk, c, sz = SEV_MARK[sev]
                y = r["ys"][rnd] if rnd < len(r["ys"]) else 0
                ax.scatter(rnd, y, marker=mk, s=sz * 0.6, color=c,
                           edgecolors="black", linewidths=0.3, alpha=0.5, zorder=3)

    # Exemplars — bold lines + full incident markers
    for r, color, label in [(wipeout, "#D62828", f"{wipeout['cond']} s{wipeout['seed']} (final={wipeout['final']:.2f})"),
                            (dominator, "#2c7fb8", f"{dominator['cond']} s{dominator['seed']} (final={dominator['final']:.2f})")]:
        ax.plot(r["xs"], r["ys"], color=color, lw=2.2, alpha=0.95, zorder=5, label=label)
        for rnd, sev in r["inc"]:
            mk, c, sz = SEV_MARK[sev]
            y = r["ys"][rnd] if rnd < len(r["ys"]) else 0
            ax.scatter(rnd, y, marker=mk, s=sz * 1.3, color=c,
                       edgecolors="black", linewidths=0.7, zorder=6)

    ax.set_xlabel("Round", fontsize=10)
    ax.set_ylabel(f"Market share — {PROVIDER}", fontsize=10)
    ax.set_ylim(0, 1.0)
    ax.set_xlim(0, max(r["xs"][-1] for r in runs))
    ax.grid(True, alpha=0.25, linewidth=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Legend: exemplars + marker types
    marker_handles = [
        Line2D([0], [0], marker="X", color="w", markerfacecolor="#D62828",
               markeredgecolor="black", markersize=10, linestyle="None",
               label="critical incident"),
        Line2D([0], [0], marker="^", color="w", markerfacecolor="#E76F51",
               markeredgecolor="black", markersize=8, linestyle="None",
               label="major incident"),
        Line2D([0], [0], color="#808080", lw=1, alpha=0.6, label="other seeds"),
    ]
    line_handles, line_labels = ax.get_legend_handles_labels()
    ax.legend(handles=line_handles + marker_handles,
              loc="lower right", fontsize=8, frameon=True, framealpha=0.9)

    model_short = _MODEL_SHORT.get(model_filter, model_filter or "all")
    ax.set_title(
        f"Path dependence: {PROVIDER} market share by seed × incident timing\n"
        f"N={len(runs)} {model_short} runs in hf_data_staging/{batch.lstrip('_')}; exemplars bolded",
        loc="left", fontsize=11)

    os.makedirs(out_dir, exist_ok=True)
    pdf = os.path.join(out_dir, "incident_path_dependence.pdf")
    png = os.path.join(out_dir, "incident_path_dependence.png")
    fig.tight_layout()
    fig.savefig(pdf, dpi=300, bbox_inches="tight")
    fig.savefig(png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {pdf}")
    print(f"Saved {png}")


def cli():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", default="core_privacy",
                    help="HF staging bucket name (e.g. core_privacy). Leading "
                         "underscore is stripped if present.")
    ap.add_argument("--model", default="sonnet",
                    choices=["sonnet", "opus", "gpt55", "all"],
                    help="Which LLM model dir to walk (default: sonnet).")
    ap.add_argument("--all-conds", action="store_true",
                    help="Include all conditions in the bucket (e.g. s5_*/s8_* "
                         "sequence-robustness sub-conditions). Default: 5 core "
                         "privacy conditions only.")
    ap.add_argument("--out-dir", default=None)
    args = ap.parse_args()
    out_dir = args.out_dir or _paths.paper_dir()

    short_to_canonical = {
        "sonnet": "claude-sonnet-4-6",
        "opus":   "claude-opus-4-6",
        "gpt55":  "gpt-5.5-2026-04-23",
    }
    model_filter = None if args.model == "all" else short_to_canonical[args.model]
    conds = None if args.all_conds else CORE_PRIVACY_CONDS
    main(args.batch, out_dir, model_filter=model_filter, conds=conds)


if __name__ == "__main__":
    cli()
