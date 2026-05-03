"""Sequence-robustness forest: privacy ladder × 5 sequences × 30 seeds.

Tests whether the monotone privacy effect is robust to the r0 anchor counterfactual.
Each of S0-S4 pins a different (active-13, intro-schedule); privacy mix held constant.
S0 = baseline reference. See run_experiment.py:_SEQUENCE_OVERRIDES for the configs.

Reads heuristic runs from sandbox/experiments/_seq_robustness/heuristic/<cond>/seeds/seed_*/
where <cond> = s{0-4}_<rung>. Aggregates per-seed mean Δgap (score - matched
satisfaction), then plots a 5x5 grouped forest.

Output: output/paper/sequence_robustness.{png,pdf}
        output/paper/sequence_robustness_long.csv  (raw per-seed table)

Usage:
    python -m scripts.plots.paper.sequence_robustness \\
        [--batch _seq_robustness] [--exclude-bm "Agentic Tasks,Function Calling"]
"""
from __future__ import annotations

import argparse
import glob
import json
import os
from collections import defaultdict

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .. import paths as _paths
from ..per_benchmark import per_benchmark_from_rows, EXCLUDE_BM as _DEFAULT_EXCLUDE_BM

SEQS = ["s0", "s1_safety", "s2_coding", "s3_knowledge", "s4_comm",
        "s5_aligned", "s6_vertical", "s7_multilingual", "s8_agentic"]
SEQ_LABELS = {
    "s0":               "S0\nbaseline",
    "s1_safety":        "S1\nsafety-shaped\n(AdvRob@r0)",
    "s2_coding":        "S2\ncoding-shaped\n(HardCoding@r0)",
    "s3_knowledge":     "S3\nknowledge-shaped\n(HardKnow@r0)",
    "s4_comm":          "S4\ncomm-shaped\n(CreativeWri@r0)",
    "s5_aligned":       "S5\nalignment-led\n(AgenticSafety@r0)",
    "s6_vertical":      "S6\nvertical-AI\n(DomainExp@r0)",
    "s7_multilingual":  "S7\nmultilingual\n(Multilingual@r0)",
    "s8_agentic":       "S8\nagentic-revolution\n(FuncCall@r0)",
}
RUNGS = ["public_only", "baseline", "private_dominant", "private_only", "iid_holdout"]
RUNG_LABELS = {
    "public_only":      "public_only",
    "baseline":         "baseline (8/3/2)",
    "private_dominant": "private_dominant",
    "private_only":     "private_only",
    "iid_holdout":      "iid_holdout",
}

# Palette F (matches per_benchmark_core_privacy convention).
RUNG_COLORS = {
    "public_only":      "#2c7fb8",  # blue
    "baseline":         "#fec44f",  # yellow-orange
    "private_dominant": "#fd8d3c",  # orange
    "private_only":     "#b10026",  # dark red
    "iid_holdout":      "#7f7f7f",  # gray
}

plt.rcParams.update({
    "figure.dpi": 110, "savefig.dpi": 150,
    "font.size": 10, "axes.titlesize": 12, "axes.labelsize": 10,
    "xtick.labelsize": 9, "ytick.labelsize": 10, "legend.fontsize": 9,
    "axes.spines.top": False, "axes.spines.right": False,
    "font.family": "DejaVu Sans",
})


def _seed_per_bm_gaps(seed_dir: str) -> list[dict] | None:
    """Return per-benchmark mean Δgap (across providers + rounds) for one seed run.
    Returns list of {benchmark, mean_gap} dicts, or None if data missing.
    Caller filters benchmarks (e.g. exclude Agentic Tasks) downstream."""
    jsonl = os.path.join(seed_dir, "rounds.jsonl")
    if not os.path.isfile(jsonl):
        return None
    with open(jsonl) as f:
        rounds = [json.loads(l) for l in f if l.strip()]
    if not rounds:
        return None
    bm_gaps: dict[str, list[float]] = defaultdict(list)
    for k in range(len(rounds)):
        df = per_benchmark_from_rows([rounds[k]])
        if df.empty:
            continue
        for _, r in df.iterrows():
            bm_gaps[r["benchmark"]].append(float(r["clean_gap"]))
    return [{"benchmark": b, "mean_gap": float(np.mean(gs))} for b, gs in bm_gaps.items() if gs]


def collect_long_df(batch: str, exclude_bm: list[str]) -> pd.DataFrame:
    """Long-form: one row per (sequence, rung, seed, benchmark) with mean_gap.
    Aggregating-across-benchmarks is the caller's responsibility (groupby + mean)."""
    root = os.path.join(_paths.PROJECT_ROOT, "sandbox", "experiments", batch, "heuristic")
    rows = []
    for seq in SEQS:
        for rung in RUNGS:
            cond = f"{seq}_{rung}"
            cond_dir = os.path.join(root, cond, "seeds")
            if not os.path.isdir(cond_dir):
                print(f"  [missing] {cond}")
                continue
            n = 0
            for seed_dir in sorted(glob.glob(os.path.join(cond_dir, "seed_*"))):
                seed = int(os.path.basename(seed_dir).split("_")[1])
                bm_rows = _seed_per_bm_gaps(seed_dir)
                if bm_rows is None:
                    continue
                for bm_row in bm_rows:
                    if exclude_bm and bm_row["benchmark"] in exclude_bm:
                        continue
                    rows.append({"sequence": seq, "rung": rung, "seed": seed,
                                 "benchmark": bm_row["benchmark"], "mean_gap": bm_row["mean_gap"]})
                n += 1
            print(f"  {cond}: {n} seeds")
    return pd.DataFrame(rows)


def collapse_to_seed_mean(df: pd.DataFrame) -> pd.DataFrame:
    """Collapse per-benchmark long-form to one row per (sequence, rung, seed) by averaging
    benchmarks. Used by the headline forest plot."""
    return df.groupby(["sequence", "rung", "seed"], as_index=False)["mean_gap"].mean()


def plot_forest(df: pd.DataFrame, out_path: str):
    """Grouped forest: x = N sequences, color = 5 rungs, dot = mean across seeds, bar = 95% CI."""
    fig_w = max(11.5, 1.8 * len(SEQS) + 3)  # scale width with sequence count
    fig, ax = plt.subplots(figsize=(fig_w, 5.0))

    n_seq = len(SEQS)
    n_rung = len(RUNGS)
    group_width = 0.85
    bar_width = group_width / n_rung
    x_centers = np.arange(n_seq)

    for j, rung in enumerate(RUNGS):
        # offset each rung within its sequence cluster
        offset = (j - (n_rung - 1) / 2) * bar_width
        means, ci_lo, ci_hi, xs = [], [], [], []
        for i, seq in enumerate(SEQS):
            sub = df[(df.sequence == seq) & (df.rung == rung)]["mean_gap"].values
            if len(sub) == 0:
                continue
            m = float(np.mean(sub))
            sem = float(np.std(sub, ddof=1) / np.sqrt(len(sub))) if len(sub) > 1 else 0.0
            means.append(m)
            ci_lo.append(m - 1.96 * sem)
            ci_hi.append(m + 1.96 * sem)
            xs.append(x_centers[i] + offset)
        if not means:
            continue
        means = np.array(means); ci_lo = np.array(ci_lo); ci_hi = np.array(ci_hi); xs = np.array(xs)
        ax.errorbar(xs, means, yerr=[means - ci_lo, ci_hi - means],
                    fmt="o", color=RUNG_COLORS[rung], markersize=6,
                    capsize=2.5, elinewidth=1.2, label=RUNG_LABELS[rung])

    ax.axhline(0, color="black", lw=0.6, alpha=0.4)
    ax.set_xticks(x_centers)
    ax.set_xticklabels([SEQ_LABELS[s] for s in SEQS])
    ax.set_ylabel(r"Mean $\Delta$gap (score $-$ matched satisfaction)")
    ax.set_title(
        "Privacy-ladder effect across r0-anchor counterfactuals (heuristic, 30 seeds)\n"
        "Each cluster = one sequence (S0-S4). Within-cluster ordering tests privacy monotonicity; "
        "cross-cluster consistency tests anchor robustness.",
        loc="left", fontsize=10.5,
    )
    ax.legend(title="privacy rung", loc="upper left", bbox_to_anchor=(1.005, 1.0),
              frameon=True, framealpha=0.95)
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        out = out_path + "." + ext
        fig.savefig(out, bbox_inches="tight")
        print(f"  wrote {out}")
    plt.close(fig)


def plot_per_benchmark_heatmap(df: pd.DataFrame, out_path: str):
    """Grid heatmap: one panel per sequence, rows=benchmarks, cols=privacy rungs.
    Cell color = mean Δgap (across providers + seeds + rounds). Shared color scale.
    Cells where the benchmark is not in the sequence's active-13 are hatched gray.
    Layout: single row up to 5 sequences; 3-col wrap for >5."""
    # Aggregate to (sequence, rung, benchmark) -> mean gap
    agg = df.groupby(["sequence", "rung", "benchmark"], as_index=False)["mean_gap"].mean()
    # Stable benchmark ordering: by mean gap in S0 baseline (descending).
    bm_order = (
        df[df.sequence == "s0"]
        .groupby("benchmark")["mean_gap"].mean()
        .sort_values(ascending=False).index.tolist()
    )
    for b in df.benchmark.unique():
        if b not in bm_order:
            bm_order.append(b)

    vmin, vmax = float(agg.mean_gap.min()), float(agg.mean_gap.max())

    # Layout: up to 5 sequences in a single row; otherwise wrap into 3-col grid.
    n_seq = len(SEQS)
    if n_seq <= 5:
        n_rows, n_cols = 1, n_seq
    else:
        n_cols = 3
        n_rows = (n_seq + n_cols - 1) // n_cols

    panel_w = 2.4
    panel_h = 0.42 * len(bm_order)
    fig_w = panel_w * n_cols + 4.5
    fig_h = panel_h * n_rows + 2.0
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(fig_w, fig_h), sharey=False)
    if n_rows == 1:
        axes = np.array([axes]).reshape(1, -1) if n_cols == 1 else np.atleast_1d(axes).reshape(1, -1)
    fig.subplots_adjust(left=0.18, right=0.90, top=0.92, bottom=0.08, wspace=0.10, hspace=0.45)

    cmap = plt.get_cmap("RdYlBu_r")

    for i, seq in enumerate(SEQS):
        row, col = divmod(i, n_cols)
        ax = axes[row, col]
        sub = agg[agg.sequence == seq]
        # Build matrix benchmarks x rungs
        mat = np.full((len(bm_order), len(RUNGS)), np.nan)
        for r_i, bm in enumerate(bm_order):
            for c_i, rung in enumerate(RUNGS):
                cell = sub[(sub.benchmark == bm) & (sub.rung == rung)]
                if not cell.empty:
                    mat[r_i, c_i] = float(cell.mean_gap.iloc[0])

        # Hatched gray for missing cells; main cells colored
        masked = np.ma.masked_invalid(mat)
        ax.imshow(np.zeros_like(mat), cmap="gray", vmin=0, vmax=1, aspect="auto", alpha=0.0)
        # Hatched-gray underlay only for missing
        for r_i in range(mat.shape[0]):
            for c_i in range(mat.shape[1]):
                if np.isnan(mat[r_i, c_i]):
                    ax.add_patch(plt.Rectangle((c_i - 0.5, r_i - 0.5), 1, 1,
                                                facecolor="#e8e8e8", hatch="///",
                                                edgecolor="#b8b8b8", linewidth=0.4, zorder=0.5))
        im = ax.imshow(masked, cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto",
                       interpolation="nearest", zorder=1.0)

        # Cell text annotations (gap value)
        for r_i in range(mat.shape[0]):
            for c_i in range(mat.shape[1]):
                v = mat[r_i, c_i]
                if not np.isnan(v):
                    txt_color = "white" if (v - vmin) / (vmax - vmin + 1e-9) > 0.6 or (v - vmin) / (vmax - vmin + 1e-9) < 0.15 else "black"
                    ax.text(c_i, r_i, f"{v:.3f}", ha="center", va="center",
                            color=txt_color, fontsize=7)

        ax.set_xticks(range(len(RUNGS)))
        ax.set_xticklabels([r.replace("_", "\n") for r in RUNGS], rotation=0, fontsize=8.5)
        ax.set_yticks(range(len(bm_order)))
        ax.set_ylim(len(bm_order) - 0.5, -0.5)  # match imshow row order
        # Show y-tick labels on first column of each row
        if col == 0:
            ax.set_yticklabels(bm_order, fontsize=9)
        else:
            ax.set_yticklabels([])
            ax.tick_params(axis="y", length=0)
        # Two-line title: short ID on top, anchor description below
        seq_short = seq.upper()
        seq_desc = SEQ_LABELS[seq].split("\n", 1)[1].replace("\n", " ") if "\n" in SEQ_LABELS[seq] else ""
        ax.set_title(f"{seq_short}\n{seq_desc}", fontsize=9.5, pad=8)
        # Subtle gridlines
        ax.set_xticks(np.arange(-0.5, len(RUNGS), 1), minor=True)
        ax.set_yticks(np.arange(-0.5, len(bm_order), 1), minor=True)
        ax.grid(which="minor", color="white", linewidth=0.5, alpha=0.5)
        ax.tick_params(which="minor", length=0)

    # Hide unused axes if grid has empty cells
    for j in range(len(SEQS), n_rows * n_cols):
        row, col = divmod(j, n_cols)
        axes[row, col].set_visible(False)

    fig.suptitle(
        "Per-benchmark mean Δgap across r0-anchor counterfactuals × privacy ladder (heuristic, 30 seeds)\n"
        "Hatched cells: benchmark not in sequence's active-13. Color: red = high gap, blue = low.",
        y=0.995, fontsize=11,
    )
    cbar = fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.65, fraction=0.018, pad=0.015)
    cbar.set_label("Mean Δgap (score $-$ matched satisfaction)", fontsize=9)
    cbar.ax.tick_params(labelsize=8)
    for ext in ("png", "pdf"):
        out = out_path + "." + ext
        # Note: deliberately NOT using bbox_inches='tight' — it can override
        # subplots_adjust margins and clip y-axis tick labels on the leftmost panel.
        fig.savefig(out, dpi=160)
        print(f"  wrote {out}")
    plt.close(fig)


SEQ_COLORS = {
    "s0":               "#777777",   # gray (baseline reference)
    "s1_safety":        "#1f77b4",   # blue
    "s2_coding":        "#2ca02c",   # green
    "s3_knowledge":     "#9467bd",   # purple
    "s4_comm":          "#17becf",   # teal
    "s5_aligned":       "#d62728",   # red (2-swap)
    "s6_vertical":      "#bcbd22",   # olive (2-swap)
    "s7_multilingual":  "#e377c2",   # pink (2-swap)
    "s8_agentic":       "#ff7f0e",   # orange (2-swap)
}


def plot_private_vs_public_scatter(df: pd.DataFrame, out_path: str):
    """Scatter: x = mean gap in private_only, y = mean gap in public_only, per (sequence, benchmark).
    Two panels: left colored by benchmark, right colored by sequence. Diagonal = no privacy effect;
    above = privacy compresses gap, below = privacy increases gap."""
    # Build per-(seq, bm) means in each rung
    agg = (df.groupby(["sequence", "rung", "benchmark"], as_index=False)["mean_gap"].mean())
    pub = agg[agg.rung == "public_only"].set_index(["sequence", "benchmark"])["mean_gap"]
    pri = agg[agg.rung == "private_only"].set_index(["sequence", "benchmark"])["mean_gap"]
    # Inner join (only points present in both rungs for a given seq, bm)
    common = pub.index.intersection(pri.index)
    rows = []
    for (seq, bm) in common:
        rows.append({"sequence": seq, "benchmark": bm,
                     "public_only": float(pub.loc[(seq, bm)]),
                     "private_only": float(pri.loc[(seq, bm)])})
    sdf = pd.DataFrame(rows)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6.0))

    # Shared axis bounds
    lo = min(sdf.public_only.min(), sdf.private_only.min()) - 0.005
    hi = max(sdf.public_only.max(), sdf.private_only.max()) + 0.005
    bounds = (lo, hi)

    # Stable benchmark ordering (by overall public_only mean)
    bm_order = sdf.groupby("benchmark")["public_only"].mean().sort_values(ascending=False).index.tolist()
    bm_palette = plt.get_cmap("tab20").colors
    bm_color = {b: bm_palette[i % 20] for i, b in enumerate(bm_order)}

    # --- Panel A: color by benchmark ---
    axA = axes[0]
    for bm in bm_order:
        sub = sdf[sdf.benchmark == bm]
        axA.scatter(sub.private_only, sub.public_only, s=55,
                    c=[bm_color[bm]], edgecolors="black", linewidths=0.6,
                    alpha=0.85, label=bm)
    axA.plot(bounds, bounds, ls="--", color="black", lw=0.7, alpha=0.5, label="y = x (no privacy effect)")
    axA.axhline(0, color="gray", lw=0.4, alpha=0.4)
    axA.axvline(0, color="gray", lw=0.4, alpha=0.4)
    axA.set_xlim(*bounds); axA.set_ylim(*bounds)
    axA.set_aspect("equal", adjustable="box")
    axA.set_xlabel("Mean gap when this benchmark is private_only")
    axA.set_ylabel("Mean gap when this benchmark is public_only")
    axA.set_title("Color = benchmark", fontsize=10.5, pad=6)
    axA.legend(loc="center left", bbox_to_anchor=(1.005, 0.5), fontsize=7,
               frameon=True, framealpha=0.95, ncol=1, handletextpad=0.4, labelspacing=0.3,
               title="benchmark")
    axA.text(0.97, 0.97, "above diagonal:\nprivacy compresses gap",
             transform=axA.transAxes, ha="right", va="top", fontsize=8,
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.85))
    axA.text(0.97, 0.03, "below diagonal:\nprivacy increases gap",
             transform=axA.transAxes, ha="right", va="bottom", fontsize=8,
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.85))

    # --- Panel B: color by sequence ---
    axB = axes[1]
    seq_order = ["s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8"]
    for seq in seq_order:
        sub = sdf[sdf.sequence == seq]
        axB.scatter(sub.private_only, sub.public_only, s=55,
                    c=[SEQ_COLORS[seq]], edgecolors="black", linewidths=0.6,
                    alpha=0.85, label=SEQ_LABELS[seq].replace("\n", " "))
    axB.plot(bounds, bounds, ls="--", color="black", lw=0.7, alpha=0.5)
    axB.axhline(0, color="gray", lw=0.4, alpha=0.4)
    axB.axvline(0, color="gray", lw=0.4, alpha=0.4)
    axB.set_xlim(*bounds); axB.set_ylim(*bounds)
    axB.set_aspect("equal", adjustable="box")
    axB.set_xlabel("Mean gap when this benchmark is private_only")
    axB.set_ylabel("Mean gap when this benchmark is public_only")
    axB.set_title("Color = sequence (regime)", fontsize=10.5, pad=6)
    axB.legend(loc="center left", bbox_to_anchor=(1.005, 0.5), fontsize=7,
               frameon=True, framealpha=0.95, handletextpad=0.4, labelspacing=0.3,
               title="sequence")

    fig.suptitle(
        "Per-benchmark privacy compression: public_only vs private_only mean gap (heuristic, 30-seed mean)\n"
        "Each point = one (sequence, benchmark) cell. Above diagonal = privacy compresses gap; below = privacy increases gap.",
        y=0.995, fontsize=11,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    for ext in ("png", "pdf"):
        out = out_path + "." + ext
        fig.savefig(out, dpi=160, bbox_inches="tight")
        print(f"  wrote {out}")
    plt.close(fig)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--batch", default="_seq_robustness")
    p.add_argument("--exclude-bm", default=",".join(_DEFAULT_EXCLUDE_BM),
                   help="Comma-separated benchmark names to exclude. Pass '' to include all.")
    p.add_argument("--scatter-include-all", action="store_true",
                   help="For the scatter plot, include benchmarks normally in EXCLUDE_BM "
                        "(Agentic Tasks, Function Calling). Useful when those benchmarks are "
                        "structurally important (e.g. FuncCall@r0 in S8).")
    args = p.parse_args()

    exclude_bm = [b.strip() for b in args.exclude_bm.split(",") if b.strip()]
    print(f"Collecting from batch={args.batch}, excluding benchmarks: {exclude_bm or '(none)'}")
    df = collect_long_df(args.batch, exclude_bm)
    if df.empty:
        print("No data found. Exiting.")
        return

    out_dir = _paths.paper_dir()

    # Per-benchmark long-form CSV (one row per (seq, rung, seed, benchmark))
    csv_path = os.path.join(out_dir, "sequence_robustness_per_bm_long.csv")
    df.to_csv(csv_path, index=False)
    print(f"Wrote per-benchmark long-form CSV: {csv_path}")
    print(f"  {len(df)} rows; {df.sequence.nunique()} sequences x {df.rung.nunique()} rungs x ~{df.seed.nunique()} seeds x {df.benchmark.nunique()} benchmarks")

    # Headline forest (collapsed to seed-level mean across benchmarks)
    seed_df = collapse_to_seed_mean(df)
    seed_csv = os.path.join(out_dir, "sequence_robustness_long.csv")
    seed_df.to_csv(seed_csv, index=False)
    print(f"Wrote seed-level CSV: {seed_csv}")

    plot_forest(seed_df, os.path.join(out_dir, "sequence_robustness"))
    plot_per_benchmark_heatmap(df, os.path.join(out_dir, "sequence_robustness_per_benchmark"))

    # Scatter: load full per-bm data WITHOUT exclusions for this view (so FuncCall@r0 in S8
    # and similar structural anchors are visible).
    if args.scatter_include_all or exclude_bm != _DEFAULT_EXCLUDE_BM:
        scatter_df = df  # already configured
    else:
        scatter_df = collect_long_df(args.batch, [])  # re-load with no excludes
    plot_private_vs_public_scatter(scatter_df, os.path.join(out_dir, "sequence_robustness_scatter"))


if __name__ == "__main__":
    main()
