"""Structural-prediction scatter (Option B for SK reviewer feedback).

For each (benchmark, provider) pair under a given condition pair (public_only vs private_only):
  observed Δgap = mean(private_only gap) − mean(public_only gap)        [from sim]
  predicted Δgap = capability_vector · (holdout_weights − public_weights)  [from gap formula]

By the gap mechanism: gap = capability·benchmark_weights − capability·need_weights, so the
difference (private − public) is exactly capability·(holdout − public). Points landing on
y=x are direct mathematical proof that the structural mechanism is operating.

Three figures:
  structural_prediction_scatter_heuristic.{png,pdf}  — sandbox/experiments/_seq_robustness (S0-S8)
  structural_prediction_scatter_llm.{png,pdf}        — hf_data_staging/core_privacy/llm/sonnet
  structural_prediction_scatter_combined.{png,pdf}   — overlay heuristic-S0 + LLM-Sonnet-S0

Usage:
    python -m scripts.plots.paper.structural_prediction_scatter
"""
from __future__ import annotations

import argparse
import glob
import json
import os
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .. import paths as _paths
from ..per_benchmark import per_benchmark_from_rows

DIMS = ["reasoning", "coding", "knowledge", "safety", "communication", "agentic"]

PROVIDER_MARKERS = {
    "Orion Labs":      "o",
    "Apex AI":         "s",
    "Genesis Systems": "D",
    "Mirage AI":       "^",
    "OpenCore":        "v",
    "Spark AI":        "P",
}

BM_PALETTE = plt.get_cmap("tab20").colors


def _vec(d):
    return np.array([d.get(k, 0.0) for k in DIMS], dtype=float)


def _load_run(seed_dir: Path):
    """Load a single run: returns (rounds, config) or (None, None) if missing."""
    j = seed_dir / "rounds.jsonl"
    c = seed_dir / "config.json"
    if not j.exists() or not c.exists():
        return None, None
    with open(j) as f:
        rounds = [json.loads(l) for l in f if l.strip()]
    with open(c) as f:
        config = json.load(f)
    return rounds, config


def _benchmark_weights_from_config(config):
    """Return {bm_name: (public_weights_dict, holdout_weights_dict_or_None)}."""
    weights = {}
    for bm in (config.get("benchmarks") or []) + (config.get("benchmark_sequence") or []):
        name = bm["name"]
        pub = bm.get("category_dimension_weights", {}).get("overall")
        hold = bm.get("holdout_category_dimension_weights", {}).get("overall") if bm.get("holdout_category_dimension_weights") else None
        if pub:
            weights[name] = (pub, hold)
    return weights


def _per_bm_gaps_per_seed(seed_dir: Path):
    """Return DataFrame with columns (benchmark, provider, mean_gap) for one run.
    Mean across all rounds (not last-round-only)."""
    rounds, _config = _load_run(seed_dir)
    if rounds is None:
        return None
    accum = defaultdict(list)
    for k in range(len(rounds)):
        df = per_benchmark_from_rows([rounds[k]])
        if df.empty:
            continue
        for _, r in df.iterrows():
            accum[(r["benchmark"], r["provider"])].append(float(r["clean_gap"]))
    if not accum:
        return None
    rows = [{"benchmark": b, "provider": p, "mean_gap": float(np.mean(gs))}
            for (b, p), gs in accum.items()]
    return pd.DataFrame(rows)


def _per_provider_capability(seed_dir: Path):
    """Return {provider: mean_capability_vector_dict} averaged across all rounds."""
    rounds, _ = _load_run(seed_dir)
    if rounds is None:
        return None
    accum = defaultdict(lambda: np.zeros(len(DIMS)))
    counts = defaultdict(int)
    for r in rounds:
        for p, cap in r.get("capability_vectors", {}).items():
            accum[p] += _vec(cap)
            counts[p] += 1
    return {p: dict(zip(DIMS, accum[p] / counts[p])) for p in accum if counts[p] > 0}


def collect_predictions(run_dirs_pub: list, run_dirs_priv: list):
    """For each (benchmark, provider) pair appearing in BOTH the public_only and private_only
    runs, compute observed and predicted Δgap.

    run_dirs_pub: list of seed dirs for public_only runs
    run_dirs_priv: list of seed dirs for private_only runs

    Returns DataFrame with columns: benchmark, provider, observed, predicted, n_pub_seeds, n_priv_seeds.
    """
    # --- Aggregate per-seed gaps ---
    pub_gaps: dict[tuple, list[float]] = defaultdict(list)
    priv_gaps: dict[tuple, list[float]] = defaultdict(list)
    for d in run_dirs_pub:
        df = _per_bm_gaps_per_seed(Path(d))
        if df is None:
            continue
        for _, r in df.iterrows():
            pub_gaps[(r.benchmark, r.provider)].append(r.mean_gap)
    for d in run_dirs_priv:
        df = _per_bm_gaps_per_seed(Path(d))
        if df is None:
            continue
        for _, r in df.iterrows():
            priv_gaps[(r.benchmark, r.provider)].append(r.mean_gap)

    # --- Aggregate per-seed capability vectors (use private_only runs as the "what providers
    # built" reference, since predicted Δgap = cap_under_priv · (holdout - public)) ---
    cap_accum: dict[str, list[np.ndarray]] = defaultdict(list)
    for d in run_dirs_priv:
        cv = _per_provider_capability(Path(d))
        if cv is None:
            continue
        for p, vec in cv.items():
            cap_accum[p].append(_vec(vec))
    mean_cap = {p: np.mean(np.array(vs), axis=0) for p, vs in cap_accum.items() if vs}

    # --- Get benchmark public/holdout weights from one private_only config ---
    sample_cfg = None
    for d in run_dirs_priv:
        _, cfg = _load_run(Path(d))
        if cfg is not None:
            sample_cfg = cfg
            break
    if sample_cfg is None:
        return pd.DataFrame()
    bw = _benchmark_weights_from_config(sample_cfg)

    # --- Build the final DataFrame ---
    rows = []
    common_keys = set(pub_gaps.keys()) & set(priv_gaps.keys())
    for (bm, prov) in sorted(common_keys):
        if bm not in bw or prov not in mean_cap:
            continue
        pub_w_dict, hold_w_dict = bw[bm]
        if hold_w_dict is None:
            # Public benchmark in this run; holdout = public (no priv shift)
            continue
        delta = _vec(hold_w_dict) - _vec(pub_w_dict)
        predicted = float(mean_cap[prov] @ delta)
        observed = float(np.mean(priv_gaps[(bm, prov)]) - np.mean(pub_gaps[(bm, prov)]))
        rows.append({
            "benchmark": bm, "provider": prov,
            "observed": observed, "predicted": predicted,
            "n_pub_seeds": len(pub_gaps[(bm, prov)]),
            "n_priv_seeds": len(priv_gaps[(bm, prov)]),
        })
    return pd.DataFrame(rows)


def collect_heuristic(seq_filter: list[str] | None = None):
    """Walk sandbox/experiments/_seq_robustness/heuristic/<seq>_<rung>/seeds/seed_*/.
    seq_filter: list of sequence IDs to include (e.g. ['s0']). None = all S0-S8."""
    root = os.path.join(_paths.PROJECT_ROOT, "sandbox", "experiments", "_seq_robustness", "heuristic")
    if seq_filter is None:
        seq_filter = [f"s{i}" for i in range(9)]
    pub_dirs, priv_dirs = [], []
    for seq in seq_filter:
        for d in sorted(glob.glob(os.path.join(root, f"{seq}_public_only", "seeds", "seed_*"))):
            pub_dirs.append(d)
        for d in sorted(glob.glob(os.path.join(root, f"{seq}_private_only", "seeds", "seed_*"))):
            priv_dirs.append(d)
    print(f"  heuristic ({len(seq_filter)} seqs): {len(pub_dirs)} pub_only seeds, {len(priv_dirs)} priv_only seeds")
    return collect_predictions(pub_dirs, priv_dirs)


def collect_llm(model: str = "claude-sonnet-4-6"):
    """Walk hf_data_staging/core_privacy/llm/<model>/<cond>/seed_*/."""
    root = os.path.join(_paths.PROJECT_ROOT, "hf_data_staging", "core_privacy", "llm", model)
    pub_dirs = sorted(glob.glob(os.path.join(root, "public_only", "seed_*")))
    priv_dirs = sorted(glob.glob(os.path.join(root, "private_only", "seed_*")))
    print(f"  llm ({model}): {len(pub_dirs)} pub_only seeds, {len(priv_dirs)} priv_only seeds")
    return collect_predictions(pub_dirs, priv_dirs)


def _setup_axes(ax, df, mode_label: str):
    """Common setup: y=x diagonal, axis bounds, grid."""
    if df.empty:
        ax.text(0.5, 0.5, f"No data ({mode_label})", ha="center", va="center", transform=ax.transAxes)
        return
    lo = min(df.observed.min(), df.predicted.min()) - 0.005
    hi = max(df.observed.max(), df.predicted.max()) + 0.005
    ax.plot([lo, hi], [lo, hi], color="black", lw=0.8, ls="--", alpha=0.6, zorder=0,
            label="y = x (structural prediction)")
    ax.axhline(0, color="gray", lw=0.4, alpha=0.4)
    ax.axvline(0, color="gray", lw=0.4, alpha=0.4)
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel(r"Observed $\Delta$gap (private_only $-$ public_only)")
    ax.set_ylabel(r"Predicted $\Delta$gap = capability $\cdot$ (holdout $-$ public)")
    # Pearson r and slope-1 RMSE
    if len(df) >= 2:
        r = float(np.corrcoef(df.observed, df.predicted)[0, 1])
        rmse_diag = float(np.sqrt(((df.observed - df.predicted) ** 2).mean()))
        ax.text(0.03, 0.97, f"r = {r:.3f}\nRMSE from y=x: {rmse_diag:.4f}\nN = {len(df)} (bm × prov)",
                transform=ax.transAxes, ha="left", va="top", fontsize=8.5,
                bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="gray", alpha=0.95))


def _plot_points(ax, df, color_by="benchmark"):
    """Scatter df points, color by benchmark or by mode."""
    bm_order = sorted(df.benchmark.unique())
    bm_color = {b: BM_PALETTE[i % 20] for i, b in enumerate(bm_order)}
    if color_by == "benchmark":
        for bm in bm_order:
            sub = df[df.benchmark == bm]
            for _, r in sub.iterrows():
                ax.scatter(r.observed, r.predicted, s=55, c=[bm_color[bm]],
                           marker=PROVIDER_MARKERS.get(r.provider, "o"),
                           edgecolors="black", linewidths=0.5, alpha=0.85, zorder=2)
        # Two-row legend: benchmarks (color), providers (marker shape)
        bm_handles = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=bm_color[b],
                                  markeredgecolor="black", markersize=7, label=b) for b in bm_order]
        prov_handles = [plt.Line2D([0], [0], marker=m, color="w", markerfacecolor="gray",
                                    markeredgecolor="black", markersize=7, label=p)
                        for p, m in PROVIDER_MARKERS.items() if p in df.provider.unique()]
        leg1 = ax.legend(handles=bm_handles, loc="lower right", fontsize=7, frameon=True,
                          framealpha=0.95, title="benchmark", title_fontsize=8, handletextpad=0.4)
        ax.add_artist(leg1)
        ax.legend(handles=prov_handles, loc="upper right", bbox_to_anchor=(1.0, 0.55),
                  fontsize=7, frameon=True, framealpha=0.95, title="provider",
                  title_fontsize=8, handletextpad=0.4)


def plot_single_mode(df: pd.DataFrame, mode_label: str, out_path: str):
    fig, ax = plt.subplots(figsize=(8.5, 8.0))
    _setup_axes(ax, df, mode_label)
    if not df.empty:
        _plot_points(ax, df, color_by="benchmark")
    ax.set_title(f"Structural-prediction scatter ({mode_label})\n"
                 r"Each point = one (benchmark, provider). Distance from y=x reveals where K-lag and noise matter.",
                 fontsize=10.5)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        out = out_path + "." + ext
        fig.savefig(out, dpi=160, bbox_inches="tight")
        print(f"  wrote {out}")
    plt.close(fig)


def plot_combined(heur_df: pd.DataFrame, llm_df: pd.DataFrame, out_path: str):
    fig, ax = plt.subplots(figsize=(8.5, 8.0))
    # Combined axis bounds
    all_df = pd.concat([heur_df, llm_df], ignore_index=True)
    if all_df.empty:
        ax.text(0.5, 0.5, "No data", ha="center", va="center", transform=ax.transAxes)
    else:
        lo = min(all_df.observed.min(), all_df.predicted.min()) - 0.005
        hi = max(all_df.observed.max(), all_df.predicted.max()) + 0.005
        ax.plot([lo, hi], [lo, hi], color="black", lw=0.8, ls="--", alpha=0.6, zorder=0,
                label="y = x (structural prediction)")
        ax.axhline(0, color="gray", lw=0.4, alpha=0.4)
        ax.axvline(0, color="gray", lw=0.4, alpha=0.4)
        ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
        ax.set_aspect("equal", adjustable="box")
        # Plot heuristic in blue circles, LLM in red diamonds
        ax.scatter(heur_df.observed, heur_df.predicted, s=40, c="#2c7fb8",
                   marker="o", edgecolors="black", linewidths=0.4, alpha=0.55,
                   label=f"heuristic (n={len(heur_df)})", zorder=1)
        ax.scatter(llm_df.observed, llm_df.predicted, s=70, c="#b10026",
                   marker="D", edgecolors="black", linewidths=0.6, alpha=0.85,
                   label=f"LLM Sonnet 4.6 (n={len(llm_df)})", zorder=2)
        # Stats
        for label, df, anchor in [("heuristic", heur_df, (0.03, 0.97)),
                                   ("LLM", llm_df, (0.03, 0.85))]:
            if len(df) >= 2:
                r = float(np.corrcoef(df.observed, df.predicted)[0, 1])
                rmse = float(np.sqrt(((df.observed - df.predicted) ** 2).mean()))
                ax.text(anchor[0], anchor[1], f"{label}: r={r:.3f}, RMSE={rmse:.4f}",
                        transform=ax.transAxes, ha="left", va="top", fontsize=9,
                        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.95))
        ax.set_xlabel(r"Observed $\Delta$gap (private_only $-$ public_only)")
        ax.set_ylabel(r"Predicted $\Delta$gap = capability $\cdot$ (holdout $-$ public)")
        ax.legend(loc="lower right", fontsize=9, frameon=True, framealpha=0.95)

    ax.set_title("Structural prediction vs observation: heuristic + LLM (S0 baseline composition only)\n"
                 r"y=x = structural mechanism's prediction; both modes should track if mechanism dominates.",
                 fontsize=10.5)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        out = out_path + "." + ext
        fig.savefig(out, dpi=160, bbox_inches="tight")
        print(f"  wrote {out}")
    plt.close(fig)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--llm-model", default="claude-sonnet-4-6")
    args = p.parse_args()

    out_dir = _paths.paper_dir()

    print("Loading heuristic (S0-S8, sandbox)...")
    heur_full = collect_heuristic(seq_filter=None)  # all 9 sequences
    print(f"  -> {len(heur_full)} (bm, provider, sequence) pairs")

    print("Loading heuristic S0-only (for combined apples-to-apples)...")
    heur_s0 = collect_heuristic(seq_filter=["s0"])
    print(f"  -> {len(heur_s0)} (bm, provider) pairs")

    print(f"Loading LLM ({args.llm_model}, S0 baseline)...")
    llm_df = collect_llm(model=args.llm_model)
    print(f"  -> {len(llm_df)} (bm, provider) pairs")

    # Save raw CSVs
    heur_full.to_csv(os.path.join(out_dir, "structural_prediction_heuristic_long.csv"), index=False)
    llm_df.to_csv(os.path.join(out_dir, "structural_prediction_llm_long.csv"), index=False)

    # Three figures
    plot_single_mode(heur_full, f"heuristic, S0-S8, N={len(heur_full)}",
                     os.path.join(out_dir, "structural_prediction_scatter_heuristic"))
    plot_single_mode(llm_df, f"LLM Sonnet 4.6, S0 baseline, N={len(llm_df)}",
                     os.path.join(out_dir, "structural_prediction_scatter_llm"))
    plot_combined(heur_s0, llm_df,
                  os.path.join(out_dir, "structural_prediction_scatter_combined"))


if __name__ == "__main__":
    main()
