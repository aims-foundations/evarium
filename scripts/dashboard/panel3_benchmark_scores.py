"""Prototype: Panel 3 -- per-benchmark max-score trajectories.

One line per benchmark = max score across providers per round. Lines start when
the benchmark is introduced. Benchmark labels include privacy suffix
(pub) / (priv) / (part).

Usage:
  python scripts/dashboard/panel3_benchmark_scores.py \\
    --run-dir sandbox/experiments/_core_privacy/llm/baseline_s42_sonnet/seeds/seed_42
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


_BM_SHORT = {
    "General Capability": "GenCap",
    "Coding Evaluation": "CodingE",
    "Hard Coding": "HardCode",
    "Safety Evaluation": "Safety",
    "Adversarial Robustness": "AdvRob",
    "Instruction Following": "InstFol",
    "Long Context": "LongCtx",
    "Scientific Reasoning": "SciReas",
    "Clinical Reasoning": "ClinReas",
    "Legal Reasoning": "LegReas",
    "Advanced Math": "AdvMath",
    "Function Calling": "FuncCall",
    "Agentic Tasks": "Agentic",
}

PRIVACY_ABBR = {"public": "pub", "private": "priv", "partial": "part"}


def load_privacy_map(cfg: dict) -> dict:
    bms = cfg.get("benchmark_sequence", []) + cfg.get("benchmarks", [])
    return {b["name"]: b.get("benchmark_type", "public") for b in bms if "name" in b}


def draw_panel(ax, rounds, privacy_map: dict):
    bm_data = {}
    for h in rounds:
        rnd = h["round"]
        for bm_name, provider_scores in (h.get("per_benchmark_scores") or {}).items():
            if bm_name not in bm_data:
                bm_data[bm_name] = {"rounds": [], "max": []}
            if provider_scores:
                bm_data[bm_name]["rounds"].append(rnd)
                bm_data[bm_name]["max"].append(max(provider_scores.values()))

    if not bm_data:
        ax.text(0.5, 0.5, "no per-benchmark data", ha="center", va="center",
                transform=ax.transAxes, color="#888")
        return

    bm_names = sorted(bm_data.keys(), key=lambda b: bm_data[b]["rounds"][0])
    cmap = plt.cm.get_cmap("tab20", max(len(bm_names), 4))
    bm_colors = {name: cmap(i) for i, name in enumerate(bm_names)}

    for bm_name in bm_names:
        d = bm_data[bm_name]
        short = _BM_SHORT.get(bm_name, bm_name[:8])
        priv = PRIVACY_ABBR.get(privacy_map.get(bm_name, "public"), "pub")
        label = f"{short} ({priv})"
        ax.plot(d["rounds"], d["max"], color=bm_colors[bm_name], linewidth=1.4,
                label=label, zorder=3)

    ax.set_title("(c) Per-benchmark max scores",
                 fontsize=13, loc="left", fontweight="bold")
    ax.set_xlabel("Round", fontsize=12)
    ax.set_ylabel("Max score across providers", fontsize=12)
    ax.set_ylim(0, 1)
    ax.tick_params(labelsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, alpha=0.25, linewidth=0.4)
    ax.legend(fontsize=5.5, loc="lower right", ncol=3,
              frameon=True, framealpha=0.92,
              handlelength=1.4, columnspacing=0.8,
              labelspacing=0.25, borderpad=0.3)


def render(run_dir: Path, out_path: Path):
    rounds = [json.loads(l) for l in (run_dir / "rounds.jsonl").read_text().splitlines() if l.strip()]
    cfg = json.loads((run_dir / "config.json").read_text()) if (run_dir / "config.json").is_file() else {}
    privacy_map = load_privacy_map(cfg)
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    draw_panel(ax, rounds, privacy_map)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    fig.savefig(out_path.with_suffix(".pdf"), bbox_inches="tight")
    print(f"Saved: {out_path}")
    plt.close(fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--run-dir", type=Path, required=True)
    ap.add_argument("--out", type=Path,
                    default=Path("output/dashboard/panel3_benchmark_scores.png"))
    args = ap.parse_args()
    render(args.run_dir, args.out)
