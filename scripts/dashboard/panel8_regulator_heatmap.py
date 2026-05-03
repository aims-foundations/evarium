"""Prototype: Panel 8 -- regulator action heatmap.

Provider x intervention-type matrix; cell = count of interventions of that type
targeted at that provider over the run. Interventions with target=None go to a
'system-wide' row at the bottom.

Usage:
  python scripts/dashboard/panel8_regulator_heatmap.py \\
    --run-dir sandbox/experiments/_core_privacy/llm/baseline_s42_sonnet/seeds/seed_42
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ESCALATION_ORDER = [
    "request_voluntary_commitment", "publish_advisory",
    "mandate_safety_disclosure", "commission_audit",
    "impose_sanction", "emergency_investigation",
]
SHORT_LABELS = {
    "request_voluntary_commitment": "Voluntary",
    "publish_advisory": "Advisory",
    "mandate_safety_disclosure": "Disclosure",
    "commission_audit": "Audit",
    "impose_sanction": "Sanction",
    "emergency_investigation": "Emergency",
}


def draw_panel(ax, rounds, providers):
    counts = defaultdict(lambda: defaultdict(int))  # row -> col -> count
    for h in rounds:
        for iv in (h.get("regulator_data", {}) or {}).get("interventions", []) or []:
            if not isinstance(iv, dict):
                continue
            t = iv.get("type") or iv.get("action", "?")
            tgt = iv.get("provider") or iv.get("target") or "system-wide"
            counts[tgt][t] += 1

    rows = list(providers) + ["system-wide"]
    cols = ESCALATION_ORDER
    M = np.array([[counts[r][c] for c in cols] for r in rows], dtype=float)

    vmax = max(1.0, float(M.max()))
    im = ax.imshow(M, cmap="OrRd", vmin=0, vmax=vmax, aspect="auto")

    for i, r in enumerate(rows):
        for j, c in enumerate(cols):
            v = int(M[i, j])
            color = "white" if v > 0.55 * vmax else "#222"
            ax.text(j, i, str(v) if v > 0 else "",
                    ha="center", va="center", fontsize=10, color=color)

    if 0 < len(providers) < len(rows):
        ax.axhline(len(providers) - 0.5, color="black", linewidth=1.2)

    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels([SHORT_LABELS[c] for c in cols], fontsize=8.5, rotation=30, ha="right")
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r if r != "system-wide" else "(system-wide)" for r in rows],
                       fontsize=9.5)
    ax.tick_params(axis="both", length=0)
    ax.set_title("(h) Regulator action distribution",
                 fontsize=13, loc="left", fontweight="bold")

    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)

    total = int(M.sum())
    ax.text(0.99, 1.04, f"total interventions: {total}",
            transform=ax.transAxes, ha="right", va="bottom",
            fontsize=8.5, color="#444")


def render(run_dir: Path, out_path: Path):
    rounds = [json.loads(l) for l in (run_dir / "rounds.jsonl").read_text().splitlines() if l.strip()]
    providers = sorted(rounds[-1]["scores"].keys())
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    draw_panel(ax, rounds, providers)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    fig.savefig(out_path.with_suffix(".pdf"), bbox_inches="tight")
    print(f"Saved: {out_path}")
    plt.close(fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--run-dir", type=Path, required=True)
    ap.add_argument("--out", type=Path,
                    default=Path("output/dashboard/panel8_regulator_heatmap.png"))
    args = ap.parse_args()
    render(args.run_dir, args.out)
