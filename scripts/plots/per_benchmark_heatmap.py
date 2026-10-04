"""Per-benchmark × per-provider gap decomposition heatmap.

For each run, produces a 3-panel figure:
  1. Clean gap: score − base_sat_matched (pure capability × weight mismatch)
  2. Full gap:  score − full_sat_matched (experienced gap incl. cost + incidents)
  3. Drag:      base_sat − full_sat        (cost + incident effects)

Complementary to `scripts.plots.per_benchmark` (which aggregates across providers).

Usage:
  python -m scripts.plots.per_benchmark_heatmap --llm-batch llm_apr19_diag --llm-seed 2026
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from . import paths as _paths
sys.path.insert(0, os.path.join(_paths.PROJECT_ROOT, "src", "actors"))
from consumer import USE_CASE_PROFILES  # type: ignore  # noqa: E402

DIMS = ["reasoning", "coding", "knowledge", "safety", "communication", "agentic"]


def _vec(d):
    return np.array([d.get(k, 0.0) for k in DIMS], dtype=float)


def _normalize(x):
    s = x.sum()
    return x / s if s > 0 else x


def _load_run(run_dir):
    with open(os.path.join(run_dir, "rounds.jsonl")) as f:
        return [json.loads(l) for l in f]


def compute_heatmaps(rows, return_details=False):
    last = rows[-1]
    providers = list(last["scores"].keys())
    benchmarks = list(last["per_benchmark_scores"].keys())

    cdw = {b: _normalize(_vec(last["benchmark_dimension_weights"][b])) for b in benchmarks}
    cap = {p: _vec(last["capability_vectors"][p]) for p in providers}

    score_mat = np.zeros((len(benchmarks), len(providers)))
    for i, b in enumerate(benchmarks):
        for j, p in enumerate(providers):
            score_mat[i, j] = last["per_benchmark_scores"][b].get(p, 0.0)

    segs = []
    for seg_name, sd in last["consumer_data"]["segment_data"].items():
        uc = sd.get("use_case")
        if uc in USE_CASE_PROFILES:
            nw = _normalize(_vec(USE_CASE_PROFILES[uc]["need_weights"]))
        else:
            nw = np.ones(len(DIMS)) / len(DIMS)
        segs.append({
            "name": seg_name,
            "use_case": uc,
            "need_weights": nw,
            "size": float(sd.get("market_fraction", 0.0)),
            "sat": sd.get("satisfaction", {}),
        })

    clean_matched = np.zeros((len(benchmarks), len(providers)))
    full_matched = np.zeros((len(benchmarks), len(providers)))
    for i, b in enumerate(benchmarks):
        cdw_b = cdw[b]
        for j, p in enumerate(providers):
            cap_p = cap[p]
            num_clean = num_full = denom = 0.0
            for seg in segs:
                align = float(np.dot(cdw_b, seg["need_weights"]))
                w = align * seg["size"]
                if w <= 0:
                    continue
                base_util = float(np.dot(cap_p, seg["need_weights"]))
                full_sat = float(seg["sat"].get(p, base_util))
                num_clean += base_util * w
                num_full += full_sat * w
                denom += w
            if denom > 0:
                clean_matched[i, j] = num_clean / denom
                full_matched[i, j] = num_full / denom

    clean_gap = score_mat - clean_matched
    full_gap = score_mat - full_matched
    drag = clean_matched - full_matched

    if return_details:
        return {
            "providers": providers, "benchmarks": benchmarks,
            "score": score_mat, "clean_matched": clean_matched,
            "full_matched": full_matched, "clean_gap": clean_gap,
            "full_gap": full_gap, "drag": drag,
        }
    return clean_gap, full_gap, drag, providers, benchmarks


def plot_run(run_dir, out_path, title_suffix=""):
    rows = _load_run(run_dir)
    d = compute_heatmaps(rows, return_details=True)
    providers, benchmarks = d["providers"], d["benchmarks"]
    clean_gap, full_gap, drag = d["clean_gap"], d["full_gap"], d["drag"]

    vmax = max(np.abs(clean_gap).max(), np.abs(full_gap).max())
    fig, axes = plt.subplots(1, 3, figsize=(17, 5.5))
    titles = [
        "Clean gap: score − base_sat_matched\n(capability × weight mismatch)",
        "Full gap: score − full_sat_matched\n(experienced gap incl. cost + incidents)",
        "Drag: base_sat − full_sat\n(cost + incident effects)",
    ]
    mats = [clean_gap, full_gap, drag]
    vlims = [vmax, vmax, max(np.abs(drag).max(), 0.01)]

    for ax, mat, title, vl in zip(axes, mats, titles, vlims):
        im = ax.imshow(mat, cmap="RdBu_r", vmin=-vl, vmax=vl, aspect="auto")
        ax.set_xticks(range(len(providers)))
        ax.set_xticklabels(providers, rotation=25, ha="right")
        ax.set_yticks(range(len(benchmarks)))
        ax.set_yticklabels(benchmarks)
        ax.set_title(title)
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                v = mat[i, j]
                color = "black" if abs(v) < vl * 0.6 else "white"
                ax.text(j, i, f"{v:+.2f}", ha="center", va="center", fontsize=8, color=color)
        plt.colorbar(im, ax=ax, fraction=0.045)

    fig.suptitle(f"Per-benchmark × per-provider gap decomposition — {title_suffix}",
                 fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(out_path, dpi=140)
    plt.close(fig)
    print(f"Saved {out_path}")

    print(f"\n  Mean per-benchmark clean gap (across providers):")
    for i, b in enumerate(benchmarks):
        print(f"    {b:25s} {clean_gap[i, :].mean():+.3f}")


DEFAULT_RUNS = [
    ("baseline", "baseline/none (dynamic pool)"),
    ("private_only", "private_only/none"),
    ("baseline__initial_uniform_allocation", "baseline/initial_uniform_allocation"),
    ("baseline__no_regulator", "baseline/no_regulator"),
    ("baseline__no_incidents", "baseline/no_incidents"),
    ("fixed_public", "fixed_public/none (static pool)"),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--llm-batch", default="llm_apr19_diag",
                    help="sandbox/experiments/<batch>/llm/ root")
    ap.add_argument("--llm-seed", type=int, default=2026)
    ap.add_argument("--out-subject", default="per_benchmark_gap")
    args = ap.parse_args()

    out_dir = _paths.analysis_dir(args.out_subject)
    for dir_name, label in DEFAULT_RUNS:
        run_dir = _paths.sandbox_run_dir(
            args.llm_batch, "llm", dir_name, "seeds", f"seed_{args.llm_seed}"
        )
        jsonl = os.path.join(run_dir, "rounds.jsonl")
        if not os.path.exists(jsonl):
            continue
        # Skip incomplete fixed_public
        with open(jsonl) as f:
            n = sum(1 for _ in f)
        if dir_name == "fixed_public" and n < 30:
            continue
        out_path = os.path.join(out_dir, f"perbm_heatmap_{dir_name}.png")
        print(f"\n=== {label} ===")
        plot_run(run_dir, out_path, title_suffix=label)


if __name__ == "__main__":
    main()
