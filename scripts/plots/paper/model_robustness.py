"""Cross-model robustness plots for the _core_privacy Tier 1 batch.

Appendix G support (model robustness, not a case study). Compares the privacy
ladder under three frontier LLM planners: Claude Sonnet 4.6, Claude Opus 4.6,
and OpenAI GPT-5.5. Produces:

    model_robustness_ladder.{png,pdf}        N-panel forest: privacy-condition
                                              ladder side-by-side, one panel per
                                              model. Headline robustness plot.
    model_robustness_forest.{png,pdf}         Paired per-benchmark dots at seed
                                              42: all conditions with a matched
                                              3-way pair. One panel per
                                              condition, marker by model.
    model_robustness_endpoints.csv            One row per (condition, seed,
                                              model) with score, HHI,
                                              mean_safety, total gap, mean
                                              satisfaction. Feeds Table G.1.
    model_robustness_frames.{png,pdf}         Reasoning-frame distribution
                                              (produced by Pass 2; this script
                                              skips gracefully if the input CSV
                                              is missing).

Data comes strictly from sandbox/experiments/_core_privacy/llm/. Model is
inferred from the directory-name suffix (`_sonnet`, `_opus`, `_gpt55`).

CLI:
    python -m scripts.plots.paper.model_robustness
    python -m scripts.plots.paper.model_robustness --frames-csv path/to/frames.csv
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .. import paths as _paths
from ..per_benchmark import per_benchmark_from_jsonl, BM_ORDER, EXCLUDE_BM, PRIV_ORDER

# Reuse the palette-F condition colors so the appendix reads against the main paper.
PRIV_COLORS = {
    "public_only":      "#2c7fb8",
    "baseline":         "#fec44f",
    "private_dominant": "#fd8d3c",
    "private_only":     "#b10026",
    "iid_holdout":      "#7f7f7f",
}

# Cross-model constants. MODEL_ORDER drives panel order, dodge order, and
# legend order everywhere.
MODEL_ORDER = ["sonnet", "opus", "gpt55"]
MODEL_MARKERS = {"sonnet": "o", "opus": "D", "gpt55": "s"}
MODEL_COLORS = {
    "sonnet": "#1f77b4",  # blue
    "opus":   "#d62728",  # red
    "gpt55":  "#2ca02c",  # green
}
MODEL_LABELS = {
    "sonnet": "Claude Sonnet 4.6",
    "opus":   "Claude Opus 4.6",
    "gpt55":  "GPT-5.5",
}
MODEL_SHORT_LABELS = {"sonnet": "Sonnet 4.6", "opus": "Opus 4.6", "gpt55": "GPT-5.5"}

plt.rcParams.update({
    "figure.dpi": 110, "savefig.dpi": 150,
    "font.size": 10, "axes.titlesize": 11, "axes.labelsize": 10,
    "xtick.labelsize": 9, "ytick.labelsize": 9, "legend.fontsize": 9,
    "axes.spines.top": False, "axes.spines.right": False,
    "font.family": "DejaVu Sans",
})

BM_KEEP = [b for b in BM_ORDER if b not in EXCLUDE_BM]

_NAME_RE = re.compile(
    r"^(?P<cond>.+?)_s(?P<seed>\d+)_(?P<model>" + "|".join(MODEL_ORDER) + r")$"
)

# Maps the resolved LLM_MODEL env value (recorded as the canonical-layout dir
# name) back to the short slug used internally throughout the appendix.
CANONICAL_MODEL_DIRS = {
    "claude-sonnet-4-6":   "sonnet",
    "claude-opus-4-6":     "opus",
    "gpt-5.5-2026-04-23":  "gpt55",
}


def discover_paired_runs(batch: str = "_core_privacy", min_rounds: int = 40):
    """Yield (condition, seed, model, seed_dir, jsonl_path) for all full runs.

    Reads two layouts and dedupes by (condition, seed, model):

      Legacy dev/sandbox:
        sandbox/experiments/<batch>/llm/<cond>_s<seed>_<model>/seeds/seed_<N>/

      Canonical hf_data_staging (bucket = batch with leading "_" stripped):
        hf_data_staging/<bucket>/llm/<model_long>/<cond>/seed_<N>/

    On collision, the legacy/sandbox entry wins (preserves the existing
    appendix data while the staging side is being populated by new runs).
    `seed_dir` is always the directory containing rounds.jsonl + providers/ +
    summary.json + metadata.json, regardless of layout.
    """
    seen = set()  # (cond, seed, model) tuples already yielded

    # Pass 1: legacy dev/sandbox layout
    sandbox_root = os.path.join(_paths.PROJECT_ROOT, "sandbox", "experiments", batch, "llm")
    if os.path.isdir(sandbox_root):
        for d in sorted(glob.glob(os.path.join(sandbox_root, "*"))):
            name = os.path.basename(d)
            m = _NAME_RE.match(name)
            if not m:
                continue
            cond, seed, model = m.group("cond"), int(m.group("seed")), m.group("model")
            seed_dir = os.path.join(d, "seeds", f"seed_{seed}")
            jsonl = os.path.join(seed_dir, "rounds.jsonl")
            if not os.path.exists(jsonl):
                continue
            with open(jsonl) as f:
                n = sum(1 for _ in f)
            if n < min_rounds:
                print(f"SKIP (partial {n}/{min_rounds}): sandbox {name}")
                continue
            key = (cond, seed, model)
            if key in seen:
                continue
            seen.add(key)
            yield cond, seed, model, seed_dir, jsonl

    # Pass 2: canonical hf_data_staging layout
    bucket = batch.lstrip("_")
    canonical_root = os.path.join(_paths.PROJECT_ROOT, "hf_data_staging", bucket, "llm")
    if os.path.isdir(canonical_root):
        for model_dir in sorted(glob.glob(os.path.join(canonical_root, "*"))):
            model_long = os.path.basename(model_dir)
            model = CANONICAL_MODEL_DIRS.get(model_long)
            if model is None or model not in MODEL_ORDER:
                continue
            for cond_dir in sorted(glob.glob(os.path.join(model_dir, "*"))):
                cond = os.path.basename(cond_dir)
                for seed_dir in sorted(glob.glob(os.path.join(cond_dir, "seed_*"))):
                    m_seed = re.match(r"seed_(\d+)$", os.path.basename(seed_dir))
                    if not m_seed:
                        continue
                    seed = int(m_seed.group(1))
                    jsonl = os.path.join(seed_dir, "rounds.jsonl")
                    if not os.path.exists(jsonl):
                        continue
                    with open(jsonl) as f:
                        n = sum(1 for _ in f)
                    if n < min_rounds:
                        print(f"SKIP (partial {n}/{min_rounds}): canonical "
                              f"{model_long}/{cond}/seed_{seed}")
                        continue
                    key = (cond, seed, model)
                    if key in seen:
                        continue
                    seen.add(key)
                    yield cond, seed, model, seed_dir, jsonl


# ─────────────────────── Endpoint table ───────────────────────

def build_endpoint_df(batch: str = "_core_privacy") -> pd.DataFrame:
    """One row per (condition, seed, model): score/gap/HHI/safety/satisfaction.

    All metrics are mean over the final 5 rounds, market-share-weighted across
    providers where applicable (matches convention in F_llm_results).
    """
    rows = []
    for cond, seed, model, run_dir, jsonl in discover_paired_runs(batch):
        with open(jsonl) as f:
            rs = [json.loads(ln) for ln in f if ln.strip()]
        if not rs:
            continue

        providers = list(rs[-1].get("scores", {}).keys())

        # Market share Herfindahl (final 5 mean)
        hhis = []
        for r in rs[-5:]:
            shares = list(r.get("consumer_data", {}).get("market_shares", {}).values())
            if shares:
                hhis.append(sum(s * s for s in shares))
        hhi = float(np.mean(hhis)) if hhis else float("nan")

        # Share-weighted mean score, mean gap, mean satisfaction (final 5)
        per_round = []
        for r in rs[-5:]:
            ms = r.get("consumer_data", {}).get("market_shares", {})
            if not ms:
                continue
            num_s, num_g, num_sat, denom = 0.0, 0.0, 0.0, 0.0
            for p, share in ms.items():
                try:
                    s = r["scores"][p]
                    sat = r["consumer_data"]["provider_satisfaction"][p]
                except (KeyError, TypeError):
                    continue
                num_s += share * s
                num_sat += share * sat
                num_g += share * (s - sat)
                denom += share
            if denom > 0:
                per_round.append((num_s / denom, num_sat / denom, num_g / denom))
        if per_round:
            arr = np.array(per_round)
            score_w, sat_w, gap_w = (float(x) for x in arr.mean(axis=0))
        else:
            score_w = sat_w = gap_w = float("nan")

        # Unweighted provider-mean safety allocation across providers (final 5)
        safe_vals = []
        for r in rs[-5:]:
            for p in providers:
                port = r.get("strategies", {}).get(p, {})
                if "safety" in port:
                    safe_vals.append(float(port["safety"]))
        mean_safety = float(np.mean(safe_vals)) if safe_vals else float("nan")

        # Incidents per round (total in run / n_rounds)
        incidents = 0
        for r in rs:
            ie = r.get("incident_events") or r.get("incidents") or []
            if isinstance(ie, list):
                incidents += len(ie)
        ipr = incidents / len(rs) if rs else float("nan")

        rows.append({
            "condition": cond, "seed": seed, "model": model,
            "n_rounds": len(rs),
            "score": score_w, "satisfaction": sat_w, "gap": gap_w,
            "HHI": hhi, "mean_safety": mean_safety, "incidents_per_round": ipr,
        })
    return pd.DataFrame(rows).sort_values(["condition", "seed", "model"]).reset_index(drop=True)


# ─────────────────────── Ladder figure (N-panel forest) ───────────────────────

def _per_benchmark_long(batch: str) -> pd.DataFrame:
    rows = []
    for cond, seed, model, run_dir, jsonl in discover_paired_runs(batch):
        try:
            df = per_benchmark_from_jsonl(jsonl)
        except Exception as e:
            print(f"ERROR {jsonl}: {e}")
            continue
        for _, r in df.iterrows():
            rows.append({
                "condition": cond, "seed": seed, "model": model,
                "benchmark": r["benchmark"], "provider": r["provider"],
                "clean_gap": r["clean_gap"], "score": r["score"],
                "clean_matched": r["clean_matched"],
            })
    return pd.DataFrame(rows)


def _agg_per_condition(df_long: pd.DataFrame) -> pd.DataFrame:
    g = df_long.groupby(["condition", "seed", "benchmark"])["clean_gap"].mean().reset_index()
    agg = g.groupby(["benchmark", "condition"])["clean_gap"].agg(
        mean="mean", sd="std", n="count"
    ).reset_index()
    agg["ci"] = np.where(agg["n"] > 1, 1.96 * agg["sd"] / np.sqrt(agg["n"]), 0.0)
    return agg


def plot_ladder_panels(df_long: pd.DataFrame, out_base: str):
    """N panels (one per model), shared y-axis benchmark ordering so the reader
    can eyeball whether the privacy-condition ordering replicates."""
    df_long = df_long[~df_long["benchmark"].isin(EXCLUDE_BM)]
    if df_long.empty:
        print("SKIP ladder — no usable rows")
        return

    models_present = [m for m in MODEL_ORDER if m in df_long.model.unique()]
    if not models_present:
        print("SKIP ladder — no rows for any known model")
        return

    # Shared benchmark ordering: Sonnet public_only mean, descending (fall back
    # to the first model present if Sonnet is absent).
    order_model = "sonnet" if "sonnet" in models_present else models_present[0]
    order_sub = df_long[df_long.model == order_model]
    agg_o = _agg_per_condition(order_sub) if not order_sub.empty else None
    if agg_o is not None and not agg_o.empty:
        order_src = agg_o[agg_o.condition == "public_only"].set_index("benchmark")["mean"]
        bm_sorted = (order_src.reindex([b for b in BM_KEEP if b in order_src.index])
                              .dropna().sort_values(ascending=False).index.tolist())
    else:
        bm_sorted = [b for b in BM_KEEP if b in df_long.benchmark.values]

    n = len(models_present)
    fig, axes = plt.subplots(1, n, figsize=(6.0 * n + 1.5, 6.8), sharey=True,
                             gridspec_kw={"wspace": 0.06})
    if n == 1:
        axes = [axes]
    y_pos = np.arange(len(bm_sorted))
    dodge = np.linspace(-0.28, 0.28, len(PRIV_ORDER))

    def _draw(ax, sub, title):
        agg = _agg_per_condition(sub)
        for i, cond in enumerate(PRIV_ORDER):
            xs, ys, cis = [], [], []
            for bm in bm_sorted:
                row = agg[(agg.benchmark == bm) & (agg.condition == cond)]
                if len(row):
                    xs.append(float(row["mean"].iloc[0]))
                    cis.append(float(row["ci"].iloc[0]))
                    ys.append(y_pos[bm_sorted.index(bm)] + dodge[i])
                else:
                    xs.append(np.nan); cis.append(0); ys.append(np.nan)
            ax.errorbar(xs, ys, xerr=cis, fmt="o", markersize=5,
                        color=PRIV_COLORS[cond], label=cond,
                        capsize=2, lw=1.0, elinewidth=0.9,
                        markeredgecolor="black", markeredgewidth=0.3)
        ax.axvline(0, color="black", lw=1, alpha=0.6)
        seed_counts = sub.groupby("condition")["seed"].nunique().to_dict()
        sstr = ", ".join(f"{c}:{seed_counts.get(c, 0)}" for c in PRIV_ORDER)
        ax.set_title(f"{title}\nseeds: {sstr}", loc="left", fontsize=10.5)
        ax.set_xlabel("Per-benchmark clean gap")

    for ax, model in zip(axes, models_present):
        _draw(ax, df_long[df_long.model == model], MODEL_LABELS[model])

    axes[0].set_yticks(y_pos); axes[0].set_yticklabels(bm_sorted)
    axes[0].invert_yaxis()

    # One shared legend; gather handles from any panel that drew them.
    handles, labels = [], []
    for ax in axes:
        h, l = ax.get_legend_handles_labels()
        if h:
            handles, labels = h, l
            break
    seen = set(); uniq = []
    for h, l in zip(handles, labels):
        if l not in seen:
            seen.add(l); uniq.append((h, l))
    if uniq:
        fig.legend([h for h, _ in uniq], [l for _, l in uniq],
                   title="privacy condition", loc="lower center",
                   ncol=len(uniq), bbox_to_anchor=(0.5, -0.02), frameon=True)

    fig.suptitle(
        f"Privacy-ladder robustness: per-benchmark clean gap by model "
        f"({n}-way comparison)\n"
        "Same mechanism, different planners — error bars = 95% CI where n≥2",
        fontsize=12, y=1.0)
    fig.tight_layout(rect=(0, 0.04, 1, 0.97))
    for ext in ("png", "pdf"):
        path = f"{out_base}.{ext}"
        fig.savefig(path, bbox_inches="tight")
        print(f"Saved {path}")
    plt.close(fig)


# ─────────────────────── Paired-s42 forest ───────────────────────

def plot_paired_s42_forest(df_long: pd.DataFrame, out_base: str, seed: int = 42):
    """One panel per privacy condition. Within each panel, per-benchmark dots
    with a marker per model overlaid. Only conditions with ALL models present
    at the given seed are drawn."""
    sub = df_long[(df_long.seed == seed) & (~df_long.benchmark.isin(EXCLUDE_BM))]
    if sub.empty:
        print(f"SKIP paired forest — no seed-{seed} rows")
        return

    models_required = set(MODEL_ORDER)
    paired_conds = [c for c in PRIV_ORDER
                    if models_required.issubset(set(sub[sub.condition == c].model.unique()))]
    if not paired_conds:
        print(f"SKIP paired forest — no conditions have all {len(MODEL_ORDER)} "
              f"models at seed {seed}")
        return

    # Shared benchmark ordering from Sonnet (or first present) public_only at this seed.
    order_model = "sonnet" if "sonnet" in sub.model.unique() else MODEL_ORDER[0]
    order_src_cond = "public_only" if "public_only" in paired_conds else paired_conds[0]
    order_src = (sub[(sub.model == order_model) & (sub.condition == order_src_cond)]
                 .groupby("benchmark")["clean_gap"].mean())
    bm_sorted = (order_src.reindex([b for b in BM_KEEP if b in order_src.index])
                          .dropna().sort_values(ascending=False).index.tolist())

    n_panels = len(paired_conds)
    fig, axes = plt.subplots(1, n_panels, figsize=(3.4 * n_panels + 1.8, 6.0),
                             sharey=True, gridspec_kw={"wspace": 0.08})
    if n_panels == 1:
        axes = [axes]
    y_pos = np.arange(len(bm_sorted))
    # Dodge spread: -0.24..0.24 for 3 models gives [-0.24, 0, 0.24].
    model_dodge = dict(zip(MODEL_ORDER, np.linspace(-0.24, 0.24, len(MODEL_ORDER))))

    for ax, cond in zip(axes, paired_conds):
        for model in MODEL_ORDER:
            vals = (sub[(sub.condition == cond) & (sub.model == model)]
                    .groupby("benchmark")["clean_gap"].mean())
            xs, ys = [], []
            for i, bm in enumerate(bm_sorted):
                if bm in vals.index:
                    xs.append(float(vals[bm]))
                    ys.append(i + model_dodge[model])
            ax.scatter(xs, ys, marker=MODEL_MARKERS[model], s=36,
                       color=MODEL_COLORS[model], edgecolor="black", linewidth=0.4,
                       label=MODEL_LABELS[model], zorder=3)
        ax.axvline(0, color="black", lw=1, alpha=0.6)
        ax.set_title(cond, loc="left", color=PRIV_COLORS.get(cond, "#000"),
                     fontsize=10.5, fontweight="bold")
        ax.set_xlabel("clean gap")

    axes[0].set_yticks(y_pos); axes[0].set_yticklabels(bm_sorted)
    axes[0].invert_yaxis()

    handles, labels = axes[-1].get_legend_handles_labels()
    seen = set(); uniq = []
    for h, l in zip(handles, labels):
        if l not in seen:
            seen.add(l); uniq.append((h, l))
    fig.legend([h for h, _ in uniq], [l for _, l in uniq], loc="lower center",
               ncol=len(uniq), bbox_to_anchor=(0.5, -0.02), frameon=True)

    fig.suptitle(
        f"Paired per-benchmark clean gap at seed {seed} — "
        f"{len(MODEL_ORDER)}-way model comparison\n"
        f"{len(paired_conds)} of {len(PRIV_ORDER)} privacy conditions with full matched triple",
        fontsize=12, y=1.0)
    fig.tight_layout(rect=(0, 0.04, 1, 0.96))
    for ext in ("png", "pdf"):
        path = f"{out_base}.{ext}"
        fig.savefig(path, bbox_inches="tight")
        print(f"Saved {path}")
    plt.close(fig)


# ─────────────────────── Frames figure (Pass 2 hookup) ───────────────────────

def plot_frames_from_csv(frames_csv: str, out_base: str):
    """Stacked-bar distribution of reasoning frames per (model, provider).

    Expects columns: model, provider, frame, count (long form). One bar per
    model per provider (N_models × N_providers bars total). If counts sum to 0
    for a cell, the stack is annotated 'no traces'."""
    if not os.path.exists(frames_csv):
        print(f"SKIP frames figure — {frames_csv} missing (Pass 2 not run yet)")
        return
    df = pd.read_csv(frames_csv)
    if df.empty:
        print(f"SKIP frames figure — {frames_csv} is empty")
        return

    preferred = ["portfolio", "market", "competitor", "incident", "privacy",
                 "regulatory", "media", "financial", "untagged"]
    present = set(df.frame.unique().tolist())
    frames = [f for f in preferred if f in present] + sorted(present - set(preferred))
    providers = sorted(df.provider.unique().tolist())
    models = [m for m in MODEL_ORDER if m in df.model.unique()]
    if not models:
        print("SKIP frames figure — no known model in CSV")
        return

    frame_colors = {
        "portfolio":  "#edc948", "market":     "#76b7b2",
        "competitor": "#4e79a7", "incident":   "#e15759",
        "privacy":    "#b07aa1", "regulatory": "#ff9da7",
        "media":      "#59a14f", "financial":  "#f28e2b",
        "untagged":   "#bab0ac",
    }

    n_bars_per_panel = len(models)
    fig, axes = plt.subplots(1, len(providers),
                             figsize=(0.7 * n_bars_per_panel * len(providers) + 2, 4.6),
                             sharey=True, gridspec_kw={"wspace": 0.08})
    if len(providers) == 1:
        axes = [axes]

    for ax, prov in zip(axes, providers):
        bottoms = {m: 0.0 for m in models}
        totals = {m: float(df[(df.model == m) & (df.provider == prov)]["count"].sum())
                  for m in models}
        for fr in frames:
            vals = []
            for m in models:
                c = df[(df.model == m) & (df.provider == prov) & (df.frame == fr)]["count"]
                v = float(c.iloc[0]) if len(c) else 0.0
                share = v / totals[m] if totals[m] > 0 else 0.0
                vals.append(share)
            xs = np.arange(len(models))
            ax.bar(xs, vals, bottom=[bottoms[m] for m in models], width=0.7,
                   color=frame_colors.get(fr, "#cccccc"), label=fr,
                   edgecolor="white", linewidth=0.4)
            for i, m in enumerate(models):
                bottoms[m] += vals[i]
        ax.set_xticks(np.arange(len(models)))
        ax.set_xticklabels([MODEL_SHORT_LABELS[m] for m in models],
                           rotation=0, fontsize=8)
        ax.set_title(prov, fontsize=9, loc="left")
        ax.set_ylim(0, 1.05)
        for i, m in enumerate(models):
            if totals[m] == 0:
                ax.text(i, 0.5, "no\ntraces", ha="center", va="center",
                        fontsize=7.5, color="#888", style="italic")

    axes[0].set_ylabel("share of tagged reasoning frames")

    handles = [plt.Rectangle((0, 0), 1, 1, facecolor=frame_colors.get(fr, "#cccccc"),
                             edgecolor="white") for fr in frames]
    fig.legend(handles, frames, loc="lower center", ncol=min(len(frames), 5),
               bbox_to_anchor=(0.5, -0.06), frameon=True, fontsize=8.5)

    detail_path = frames_csv.replace("_frames.csv", "_frames_detail.csv")
    sub = "Keyword+regex tagging over providers/<name>/memory.json planning entries"
    if os.path.exists(detail_path):
        try:
            det = pd.read_csv(detail_path)
            pairs = (det.groupby(["condition", "seed"]).size().reset_index()
                     .apply(lambda r: f"{r['condition']}@s{r['seed']}", axis=1).tolist())
            conds = sorted({p.split("@")[0] for p in pairs})
            seeds = sorted({p.split("@s")[1] for p in pairs})
            sub = (f"Tagged planning entries across {len(pairs)} matched "
                   f"{n_bars_per_panel}-way pairs: {len(conds)} privacy conditions "
                   f"× seeds {{{', '.join(seeds)}}}")
        except Exception:
            pass
    fig.suptitle(
        f"Reasoning-frame distribution by model and provider ({n_bars_per_panel}-way)\n{sub}",
        fontsize=11, y=1.0)
    fig.tight_layout(rect=(0, 0.06, 1, 0.94))
    for ext in ("png", "pdf"):
        path = f"{out_base}.{ext}"
        fig.savefig(path, bbox_inches="tight")
        print(f"Saved {path}")
    plt.close(fig)


# ─────────────────────────── CLI ───────────────────────────

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--batch", default="_core_privacy")
    ap.add_argument("--out-dir", default=None,
                    help="Default: output/paper/ via _paths.paper_dir()")
    ap.add_argument("--frames-csv", default=None,
                    help="Path to Pass-2 reasoning-frames CSV (model,provider,frame,count). "
                         "If absent, the frames figure is skipped.")
    ap.add_argument("--paired-seed", type=int, default=42,
                    help="Seed for the paired per-benchmark forest (default 42)")
    args = ap.parse_args()

    out_dir = args.out_dir or _paths.paper_dir()
    os.makedirs(out_dir, exist_ok=True)

    endpoints = build_endpoint_df(args.batch)
    if endpoints.empty:
        print(f"No runs found under sandbox/experiments/{args.batch}/llm/")
        sys.exit(1)
    endpoints_path = os.path.join(out_dir, "model_robustness_endpoints.csv")
    endpoints.to_csv(endpoints_path, index=False, float_format="%.4f")
    print(f"Saved {endpoints_path}")
    print(endpoints.to_string(index=False, float_format="%.3f"))

    df_long = _per_benchmark_long(args.batch)
    if df_long.empty:
        print("No per-benchmark rows built — skipping figures.")
        return

    print(f"Loaded {len(df_long)} per-benchmark rows: "
          f"models={sorted(df_long.model.unique().tolist())}, "
          f"seeds={sorted(df_long.seed.unique().tolist())}, "
          f"conditions={sorted(df_long.condition.unique().tolist())}")

    plot_ladder_panels(df_long, os.path.join(out_dir, "model_robustness_ladder"))
    plot_paired_s42_forest(df_long, os.path.join(out_dir, "model_robustness_forest"),
                           seed=args.paired_seed)

    frames_csv = args.frames_csv or os.path.join(out_dir, "model_robustness_frames.csv")
    plot_frames_from_csv(frames_csv, os.path.join(out_dir, "model_robustness_frames"))


if __name__ == "__main__":
    main()
