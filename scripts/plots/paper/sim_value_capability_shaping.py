"""Sim-adds-value figure: capability evolution differs across sequences in ways that
predict the resulting gap regime.

Two-panel composition:
  Left  — heatmap of end-state mean capability per (sequence, dim).
          Differences across rows = the sim's emergent shaping output.
  Right — scatter of per-sequence "structural misalignment" vs observed aggregate gap.
          Misalignment = mean_capability · (mean_active_benchmark_weights - mean_consumer_need).
          If sim shaping correlates with gap, the sim is doing meaningful predictive work
          beyond the algebraic identity tested in structural_prediction_scatter.

Reads from sandbox/experiments/_seq_robustness/heuristic/<seq>_baseline/seeds/seed_*/.
Output: output/paper/sim_value_capability_shaping.{png,pdf}
        output/paper/sim_value_capability_shaping_long.csv

Usage:
    python -m scripts.plots.paper.sim_value_capability_shaping
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .. import paths as _paths

# USE_CASE_PROFILES lives in src/actors/consumer.py and provides per-use-case need vectors
# we need for per-segment consumer-need aggregation.
sys.path.insert(0, os.path.join(_paths.PROJECT_ROOT, "src"))
from actors.consumer import USE_CASE_PROFILES

DIMS = ["reasoning", "coding", "knowledge", "safety", "communication", "agentic"]
DIM_LABELS = ["reason", "code", "know", "safety", "comm", "agentic"]

SEQS = ["s0", "s1_safety", "s2_coding", "s3_knowledge", "s4_comm",
        "s5_aligned", "s6_vertical", "s7_multilingual", "s8_agentic"]
SEQ_TITLES = {
    "s0":               "S0 baseline",
    "s1_safety":        "S1 safety-shaped",
    "s2_coding":        "S2 coding-shaped",
    "s3_knowledge":     "S3 knowledge-shaped",
    "s4_comm":          "S4 comm-shaped",
    "s5_aligned":       "S5 alignment-led",
    "s6_vertical":      "S6 vertical-AI",
    "s7_multilingual":  "S7 multilingual",
    "s8_agentic":       "S8 agentic-revolution",
}


def _vec(d):
    return np.array([d.get(k, 0.0) for k in DIMS], dtype=float)


def _normalize(v):
    s = float(v.sum())
    return v / s if s > 0 else v


def _seed_payload(seed_dir: Path, last_n_rounds: int = 5):
    """Return {provider: end_capability_vector_avg, ...} averaged over the last N rounds,
    plus active benchmark mean public weights, plus consumer need (pop-avg) — all derived
    from the run's rounds.jsonl + config.json. Returns None if missing."""
    j = seed_dir / "rounds.jsonl"
    c = seed_dir / "config.json"
    if not j.exists() or not c.exists():
        return None
    with open(j) as f:
        rounds = [json.loads(l) for l in f if l.strip()]
    if not rounds:
        return None
    with open(c) as f:
        config = json.load(f)
    last = rounds[-min(last_n_rounds, len(rounds)):]

    # End-state mean capability per provider (averaged over last N rounds)
    cap_accum = defaultdict(lambda: np.zeros(len(DIMS)))
    cap_n = defaultdict(int)
    for r in last:
        for p, cv in r.get("capability_vectors", {}).items():
            cap_accum[p] += _vec(cv)
            cap_n[p] += 1
    end_cap = {p: cap_accum[p] / cap_n[p] for p in cap_accum if cap_n[p] > 0}

    # Active benchmark aggregate public weights (mean across all active bms in this run)
    bm_weights = []
    for bm in (config.get("benchmarks") or []) + (config.get("benchmark_sequence") or []):
        cdw = bm.get("category_dimension_weights", {}).get("overall")
        if cdw:
            bm_weights.append(_vec(cdw))
    bm_mean = np.mean(np.array(bm_weights), axis=0) if bm_weights else np.zeros(len(DIMS))
    bm_mean = _normalize(bm_mean)

    # Population-average consumer need (segment-size-weighted via USE_CASE_PROFILES lookup)
    last_round = rounds[-1]
    seg = last_round.get("consumer_data", {}).get("segment_data", {})
    need_accum = np.zeros(len(DIMS))
    size_accum = 0.0
    for n, sd in seg.items():
        uc = sd.get("use_case")
        nw = USE_CASE_PROFILES.get(uc, {}).get("need_weights") if uc else None
        sz = float(sd.get("market_fraction", 0.0))
        if nw and sz > 0:
            need_accum += _vec(nw) * sz
            size_accum += sz
    need_mean = _normalize(need_accum / size_accum) if size_accum > 0 else None

    return {
        "end_cap": end_cap,
        "bm_mean": bm_mean,
        "need_mean": need_mean,
    }


def collect_per_sequence(batch: str = "_seq_robustness"):
    """For each sequence, aggregate end-state cap, active-bm-mean, need-mean across seeds + providers.
    Returns DataFrame with one row per sequence: cap_dim columns + bm_dim + need_dim + summary scalars."""
    root = os.path.join(_paths.PROJECT_ROOT, "sandbox", "experiments", batch, "heuristic")
    rows = []
    for seq in SEQS:
        seed_dirs = sorted(glob.glob(os.path.join(root, f"{seq}_baseline", "seeds", "seed_*")))
        if not seed_dirs:
            print(f"  [missing] {seq}_baseline")
            continue
        # Accumulate across seeds
        all_cap = defaultdict(list)  # provider -> list of cap-vectors (one per seed)
        bms = []
        needs = []
        for sd in seed_dirs:
            payload = _seed_payload(Path(sd))
            if payload is None:
                continue
            for p, cv in payload["end_cap"].items():
                all_cap[p].append(cv)
            bms.append(payload["bm_mean"])
            if payload["need_mean"] is not None:
                needs.append(payload["need_mean"])
        if not all_cap or not bms:
            continue
        # Mean across providers (then across seeds via per-provider list)
        provider_means = np.array([np.mean(np.array(vs), axis=0) for vs in all_cap.values()])
        cap_mean = provider_means.mean(axis=0)
        bm_mean = np.mean(np.array(bms), axis=0)
        need_mean = np.mean(np.array(needs), axis=0) if needs else None

        row = {"sequence": seq}
        for i, d in enumerate(DIMS):
            row[f"cap_{d}"] = float(cap_mean[i])
            row[f"bm_{d}"] = float(bm_mean[i])
            if need_mean is not None:
                row[f"need_{d}"] = float(need_mean[i])
        # Summary scalars: structural misalignment + alignment metrics
        if need_mean is not None:
            misalign = bm_mean - need_mean
            row["structural_misalign_proj"] = float(cap_mean @ misalign)  # the gap formula's mean
            row["bm_need_cosine"] = float(bm_mean @ need_mean / (np.linalg.norm(bm_mean) * np.linalg.norm(need_mean)))
            row["cap_need_cosine"] = float(cap_mean @ need_mean / (np.linalg.norm(cap_mean) * np.linalg.norm(need_mean)))
        rows.append(row)
        print(f"  {seq}: {len(seed_dirs)} seeds, {len(all_cap)} providers")
    return pd.DataFrame(rows)


def plot_two_panel(df: pd.DataFrame, gap_df: pd.DataFrame, out_path: str):
    """Left: heatmap of cap_dim per sequence. Right: scatter of structural misalignment vs gap."""
    if df.empty:
        print("no data")
        return

    fig = plt.figure(figsize=(15, 6.5))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.3, 1.0], wspace=0.32)

    # --- Left panel: capability heatmap ---
    axL = fig.add_subplot(gs[0, 0])
    cap_mat = df[[f"cap_{d}" for d in DIMS]].values  # n_seq x 6
    seq_labels = [SEQ_TITLES[s] for s in df.sequence]

    # Compute per-dim deviation from sequence-mean to highlight DIFFERENCES (sim's shaping)
    cap_centered = cap_mat - cap_mat.mean(axis=0, keepdims=True)

    vmax = float(np.abs(cap_centered).max())
    im = axL.imshow(cap_centered, cmap="RdBu_r", vmin=-vmax, vmax=vmax, aspect="auto")
    axL.set_xticks(range(len(DIMS))); axL.set_xticklabels(DIM_LABELS, fontsize=10)
    axL.set_yticks(range(len(seq_labels))); axL.set_yticklabels(seq_labels, fontsize=9.5)
    for r_i in range(cap_centered.shape[0]):
        for c_i in range(cap_centered.shape[1]):
            v = cap_centered[r_i, c_i]
            axL.text(c_i, r_i, f"{v:+.3f}", ha="center", va="center",
                     color="white" if abs(v) > 0.6 * vmax else "black", fontsize=8.5)
    axL.set_title("End-state mean capability, deviation from cross-sequence mean\n"
                  "(red = sequence built more capability in this dim; blue = less)",
                  fontsize=10.5, pad=8)
    cbar = fig.colorbar(im, ax=axL, fraction=0.04, pad=0.02)
    cbar.set_label("capability deviation from row-mean", fontsize=9)
    cbar.ax.tick_params(labelsize=8)

    # --- Right panel: structural misalignment vs aggregate gap ---
    axR = fig.add_subplot(gs[0, 1])
    # Merge with gap_df to get aggregate baseline gap per sequence
    g = gap_df.groupby("sequence")["mean_gap"].mean().rename("agg_gap").reset_index()
    plot_df = df.merge(g, on="sequence")
    if "structural_misalign_proj" not in plot_df.columns:
        axR.text(0.5, 0.5, "need vectors unavailable", ha="center", va="center", transform=axR.transAxes)
    else:
        seq_colors = {"s0": "#777777", "s1": "#1f77b4", "s2": "#2ca02c", "s3": "#9467bd",
                      "s4": "#17becf", "s5": "#d62728", "s6": "#bcbd22", "s7": "#e377c2", "s8": "#ff7f0e"}
        for _, r in plot_df.iterrows():
            axR.scatter(r.structural_misalign_proj, r.agg_gap, s=130,
                        c=[seq_colors[r.sequence]], edgecolors="black", linewidths=0.8,
                        label=SEQ_TITLES[r.sequence], zorder=2)
            axR.annotate(r.sequence.upper(), (r.structural_misalign_proj, r.agg_gap),
                         xytext=(8, 4), textcoords="offset points", fontsize=9, fontweight="bold")
        # Fit + plot
        x = plot_df.structural_misalign_proj.values
        y = plot_df.agg_gap.values
        if len(x) >= 2:
            slope, intercept = np.polyfit(x, y, 1)
            r = float(np.corrcoef(x, y)[0, 1])
            xr = np.array([x.min() - 0.001, x.max() + 0.001])
            axR.plot(xr, slope * xr + intercept, ls="--", color="black", lw=0.8, alpha=0.6,
                     label=f"OLS fit: y = {slope:.2f}x + {intercept:.4f}\nr = {r:.3f}", zorder=1)
        axR.axhline(0, color="gray", lw=0.4, alpha=0.4)
        axR.axvline(0, color="gray", lw=0.4, alpha=0.4)
        axR.set_xlabel(r"Per-sequence structural misalignment proj." "\n"
                       r"$=$ mean_cap $\cdot$ (mean_active_bm_weights $-$ mean_consumer_need)")
        axR.set_ylabel("Per-sequence observed aggregate gap (baseline rung)")
        axR.set_title("Sim-emergent capability shape predicts the gap regime\n"
                      "(if r is high, the chain composition→shaping→gap is doing real work)",
                      fontsize=10.5, pad=8)
        axR.legend(loc="upper left", fontsize=7.5, frameon=True, framealpha=0.95,
                   handletextpad=0.4, labelspacing=0.3)

    fig.suptitle("Does the sim add value? Capability shaping is sequence-specific (left), "
                 "and shape-vs-need misalignment predicts the gap regime (right).",
                 y=1.005, fontsize=12)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        out = out_path + "." + ext
        fig.savefig(out, dpi=160, bbox_inches="tight")
        print(f"  wrote {out}")
    plt.close(fig)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--batch", default="_seq_robustness")
    args = p.parse_args()

    print("Collecting per-sequence capability + benchmark + need vectors (heuristic baseline runs)...")
    df = collect_per_sequence(args.batch)
    if df.empty:
        print("No data, exiting.")
        return

    out_dir = _paths.paper_dir()
    csv_path = os.path.join(out_dir, "sim_value_capability_shaping_long.csv")
    df.to_csv(csv_path, index=False)
    print(f"Wrote {csv_path}")

    # Pull per-sequence aggregate gap from existing CSV
    gap_csv = os.path.join(out_dir, "sequence_robustness_long.csv")
    if not os.path.isfile(gap_csv):
        print(f"WARN: {gap_csv} not found; right panel will be empty. Re-run sequence_robustness.py first.")
        gap_df = pd.DataFrame()
    else:
        gap_full = pd.read_csv(gap_csv)
        gap_df = gap_full[gap_full.rung == "baseline"]

    plot_two_panel(df, gap_df, os.path.join(out_dir, "sim_value_capability_shaping"))


if __name__ == "__main__":
    main()
