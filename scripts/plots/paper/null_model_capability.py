"""Null-model capability prediction: how much of the observed dgap variance is predictable
from initial conditions alone, without running the simulation?

Motivation
----------
The structural-prediction scatter (structural_prediction_scatter_combined.png) shows
observed dgap = capability · (holdout − public) with r > 0.99 — but this is the gap-formula
identity. It validates implementation, not that the *simulation* is doing meaningful predictive
work. That capability vector is the sim's 40-round output. Could you have predicted it from
initial conditions alone?

This script fits a null capability model:

    cap_end[provider, dim] ≈ f(initial_cap[provider, dim], initial_portfolio[provider])

trained on a subset of seeds via 5-fold CV. It then propagates null-predicted cap to a
null dgap = null_cap · (holdout − public) and compares variance explained vs the
sim's (tautological) dgap = sim_cap · (holdout − public).

If null r²(observed dgap) ≈ 1, sim is window-dressing for closed-form algebra.
If null r²(observed dgap) ≪ 1, sim is doing real predictive work; the residual is the
sim-specific contribution.

Reads from sandbox/experiments/_seq_robustness/heuristic/<seq>_<rung>/seeds/seed_*/.

Output:
    output/paper/null_model_capability_scatter.{png,pdf}      — left panel: null preds; right: sim preds
    output/paper/null_model_capability_metrics.csv            — per-fold metrics + summary
    output/paper/null_model_capability_long.csv               — per-cell predictions + observed
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
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold

from .. import paths as _paths

DIMS = ["reasoning", "coding", "knowledge", "safety", "communication", "agentic"]

# Map each dim to the portfolio lever that primarily drives its growth in the sim.
# (Per docs/stakeholders.md investment model: rd directs all dims; safety dim has its own
# lever; product affects two channels but doesn't grow capability directly.)
_DIM_TO_LEVER = {
    "reasoning":     "rd",
    "coding":        "rd",
    "knowledge":     "rd",
    "communication": "rd",
    "agentic":       "rd",
    "safety":        "safety",
}


def _vec(d):
    return np.array([d.get(k, 0.0) for k in DIMS], dtype=float)


def _seed_payload(seed_dir: Path, last_n_rounds: int = 5):
    """For one run: return per-(provider, dim) initial_cap, end_cap, plus initial portfolio
    per provider, plus benchmark public/holdout weights."""
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

    # Initial capability per provider (round 0)
    init_cap = {p: _vec(cv) for p, cv in rounds[0].get("capability_vectors", {}).items()}
    # End capability (mean over last N rounds for stability)
    last = rounds[-min(last_n_rounds, len(rounds)):]
    end_accum = defaultdict(lambda: np.zeros(len(DIMS)))
    end_n = defaultdict(int)
    for r in last:
        for p, cv in r.get("capability_vectors", {}).items():
            end_accum[p] += _vec(cv)
            end_n[p] += 1
    end_cap = {p: end_accum[p] / end_n[p] for p in end_accum if end_n[p] > 0}

    # Initial portfolio per provider (from config; constant across rungs/sequences).
    # Config key is `provider_configs` (not `providers`).
    init_portfolio = {}
    for prov_cfg in config.get("provider_configs", []):
        name = prov_cfg.get("name")
        port = prov_cfg.get("portfolio") or {}
        init_portfolio[name] = {
            "rd":      float(port.get("rd", 0.0)),
            "safety":  float(port.get("safety", 0.0)),
            "product": float(port.get("product", 0.0)),
        }

    # Benchmark public/holdout weights
    bm_weights = {}
    for bm in (config.get("benchmarks") or []) + (config.get("benchmark_sequence") or []):
        name = bm["name"]
        pub = bm.get("category_dimension_weights", {}).get("overall")
        hold_obj = bm.get("holdout_category_dimension_weights")
        hold = hold_obj.get("overall") if isinstance(hold_obj, dict) else None
        if pub:
            bm_weights[name] = (_vec(pub), _vec(hold) if hold else None)

    return {
        "init_cap": init_cap,
        "end_cap": end_cap,
        "init_portfolio": init_portfolio,
        "bm_weights": bm_weights,
    }


_RUNG_NAMES = ("public_only", "private_dominant", "private_only", "iid_holdout", "baseline")


def _parse_cond_name(cond_name: str):
    """Parse <seq_id>_<rung> or bare <rung>. Returns (seq_id, rung) or (None, None)
    if not parseable. Bare-rung names default to seq_id='s0' (S0-baseline composition,
    which is what existing pre-session-62 LLM runs use)."""
    for r_name in _RUNG_NAMES:
        if cond_name == r_name:
            return "s0", r_name
        suffix = "_" + r_name
        if cond_name.endswith(suffix):
            return cond_name[:-len(suffix)], r_name
    return None, None


def collect_runs(batch: str = "_seq_robustness"):
    """Walk all heuristic runs and build a flat per-(seq, rung, seed) record.
    Path: sandbox/experiments/<batch>/heuristic/<seq>_<rung>/seeds/seed_*/."""
    root = os.path.join(_paths.PROJECT_ROOT, "sandbox", "experiments", batch, "heuristic")
    rows = []
    for cond_dir in sorted(glob.glob(os.path.join(root, "*"))):
        seq_id, rung = _parse_cond_name(os.path.basename(cond_dir))
        if rung is None:
            continue
        for seed_dir in sorted(glob.glob(os.path.join(cond_dir, "seeds", "seed_*"))):
            seed = int(os.path.basename(seed_dir).split("_", 1)[1])
            payload = _seed_payload(Path(seed_dir))
            if payload is None:
                continue
            rows.append({"sequence": seq_id, "rung": rung, "seed": seed,
                         "seed_dir": str(seed_dir), **payload})
    return rows


def collect_runs_llm(bucket: str = "core_privacy", model: str = "claude-sonnet-4-6",
                     min_rounds: int = 40):
    """Walk LLM runs at canonical staging:
    hf_data_staging/<bucket>/llm/<model>/<cond>/seed_*/.
    Skips partial runs (rounds < min_rounds)."""
    root = os.path.join(_paths.PROJECT_ROOT, "hf_data_staging", bucket, "llm", model)
    if not os.path.isdir(root):
        print(f"WARN: {root} does not exist")
        return []
    rows = []
    for cond_dir in sorted(glob.glob(os.path.join(root, "*"))):
        seq_id, rung = _parse_cond_name(os.path.basename(cond_dir))
        if rung is None:
            continue
        for seed_dir in sorted(glob.glob(os.path.join(cond_dir, "seed_*"))):
            seed = int(os.path.basename(seed_dir).split("_", 1)[1])
            jsonl = os.path.join(seed_dir, "rounds.jsonl")
            if not os.path.exists(jsonl):
                continue
            with open(jsonl) as f:
                n_rounds = sum(1 for _ in f)
            if n_rounds < min_rounds:
                print(f"  SKIP partial ({n_rounds}/{min_rounds}): {os.path.basename(cond_dir)}/seed_{seed}")
                continue
            payload = _seed_payload(Path(seed_dir))
            if payload is None:
                continue
            rows.append({"sequence": seq_id, "rung": rung, "seed": seed,
                         "seed_dir": str(seed_dir), **payload})
    return rows


def compute_obs_dgap_inline(runs):
    """Compute observed Δgap per (seq, seed, bm) by aggregating per_benchmark_from_rows
    across providers and rounds per run, then taking priv − pub. Reads rounds.jsonl from
    each run's seed_dir. Returns dict[(seq, seed, bm)] -> obs_dgap.

    Mirrors how sequence_robustness.py builds its CSV but inline so we don't depend on
    a pre-built CSV (which is heuristic-only)."""
    from scripts.plots.per_benchmark import per_benchmark_from_rows

    # Group runs by (seq, seed); we need both pub_only and priv_only present.
    by_seq_seed = defaultdict(dict)
    for run in runs:
        by_seq_seed[(run["sequence"], run["seed"])][run["rung"]] = run

    # Per-(seq, seed, rung) compute mean per-bm gap across rounds × providers
    def _per_bm_mean_gap(seed_dir: str):
        with open(os.path.join(seed_dir, "rounds.jsonl")) as f:
            rounds = [json.loads(l) for l in f if l.strip()]
        accum = defaultdict(list)
        for r in rounds:
            df = per_benchmark_from_rows([r])
            if df.empty:
                continue
            for _, row in df.iterrows():
                accum[row["benchmark"]].append(float(row["clean_gap"]))
        return {b: float(np.mean(gs)) for b, gs in accum.items() if gs}

    out = {}
    for (seq, seed), rung_map in by_seq_seed.items():
        if "public_only" not in rung_map or "private_only" not in rung_map:
            continue
        pub_gaps = _per_bm_mean_gap(rung_map["public_only"]["seed_dir"])
        priv_gaps = _per_bm_mean_gap(rung_map["private_only"]["seed_dir"])
        for bm in pub_gaps:
            if bm in priv_gaps:
                out[(seq, seed, bm)] = priv_gaps[bm] - pub_gaps[bm]
    return out


def build_training_table(runs):
    """Flatten runs into a per-(provider, dim) row table for fitting the null model.
    Features: provider one-hot + initial_cap[dim] + portfolio[dim_lever]
    Target: end_cap[dim]"""
    cells = []
    for run in runs:
        for prov, init_cv in run["init_cap"].items():
            end_cv = run["end_cap"].get(prov)
            port = run["init_portfolio"].get(prov)
            if end_cv is None or port is None:
                continue
            for di, dim in enumerate(DIMS):
                lever = _DIM_TO_LEVER[dim]
                cells.append({
                    "sequence": run["sequence"], "rung": run["rung"], "seed": run["seed"],
                    "provider": prov, "dim": dim,
                    "init_cap": float(init_cv[di]),
                    "lever_weight": float(port[lever]),
                    "end_cap": float(end_cv[di]),
                })
    return pd.DataFrame(cells)


def fit_null_per_provider_dim(df_train):
    """Fit a tiny linear model (Ridge) per (provider, dim). Features: [init_cap, lever_weight].
    Returns dict[(provider, dim)] -> sklearn Ridge model."""
    models = {}
    for (prov, dim), sub in df_train.groupby(["provider", "dim"]):
        if len(sub) < 2:
            continue
        X = sub[["init_cap", "lever_weight"]].values
        y = sub["end_cap"].values
        m = Ridge(alpha=1.0)
        m.fit(X, y)
        models[(prov, dim)] = m
    return models


def predict_null_cap(models, init_cap, init_portfolio):
    """Predict null end_cap dict[provider] -> ndarray[6]."""
    out = {}
    for prov, init_cv in init_cap.items():
        port = init_portfolio.get(prov)
        if port is None:
            continue
        cap = np.zeros(len(DIMS))
        for di, dim in enumerate(DIMS):
            lever = _DIM_TO_LEVER[dim]
            m = models.get((prov, dim))
            if m is None:
                cap[di] = float(init_cv[di])  # fallback
            else:
                cap[di] = float(m.predict(np.array([[init_cv[di], port[lever]]]))[0])
        out[prov] = np.clip(cap, 0.0, 1.0)
    return out


def compute_dgap_predictions(test_runs, null_cap_lookup, obs_dgap_lookup):
    """For each (seq, seed, bm) in test, compute observed dgap (from CSV), null dgap, sim dgap.
    Aggregates predictions across providers via mean (matches CSV's provider-averaging)."""
    # Group by (seq, seed) so we can pair pub_only and priv_only runs
    by_seq_seed = defaultdict(dict)  # (seq, seed) -> {rung: run_idx_in_test_runs}
    for i, run in enumerate(test_runs):
        by_seq_seed[(run["sequence"], run["seed"])][run["rung"]] = i

    rows = []
    for (seq, seed), rung_map in by_seq_seed.items():
        if "public_only" not in rung_map or "private_only" not in rung_map:
            continue
        pub_run = test_runs[rung_map["public_only"]]
        priv_run = test_runs[rung_map["private_only"]]
        for bm_name, (pub_w, hold_w) in priv_run["bm_weights"].items():
            if hold_w is None:
                continue
            delta_w = hold_w - pub_w
            obs_dgap = obs_dgap_lookup.get((seq, seed, bm_name))
            if obs_dgap is None:
                continue
            # Average end_cap and null_cap across providers (matches CSV's
            # per_benchmark_from_rows aggregation which sums across providers).
            sim_caps = []
            null_caps = []
            for prov, end_cap_priv_vec in priv_run["end_cap"].items():
                end_cap_pub_vec = pub_run["end_cap"].get(prov)
                if end_cap_pub_vec is None:
                    continue
                sim_caps.append((end_cap_priv_vec + end_cap_pub_vec) / 2.0)
                ncap = null_cap_lookup.get((seq, seed, prov))
                if ncap is not None:
                    null_caps.append(ncap)
            if not sim_caps or not null_caps:
                continue
            sim_cap_mean = np.mean(np.array(sim_caps), axis=0)
            null_cap_mean = np.mean(np.array(null_caps), axis=0)
            sim_dgap = float(sim_cap_mean @ delta_w)
            null_dgap = float(null_cap_mean @ delta_w)
            rows.append({
                "sequence": seq, "seed": seed, "benchmark": bm_name,
                "obs_dgap": obs_dgap,
                "sim_dgap": sim_dgap,
                "null_dgap": null_dgap,
            })
    return pd.DataFrame(rows)


def load_obs_dgap_from_csv(csv_path: str) -> dict:
    """Load per-(seq, seed, bm) observed dgap = mean_gap[private_only] − mean_gap[public_only]
    from sequence_robustness_per_bm_long.csv (which uses the correct segment-weighted gap
    via per_benchmark_from_rows)."""
    if not os.path.isfile(csv_path):
        print(f"WARN: {csv_path} not found — observed dgap will be missing for some cells.")
        return {}
    df = pd.read_csv(csv_path)
    # Pivot to get pub_only and priv_only mean_gap per (seq, seed, bm)
    sub = df[df.rung.isin(["public_only", "private_only"])]
    piv = sub.pivot_table(index=["sequence", "seed", "benchmark"], columns="rung",
                          values="mean_gap", aggfunc="mean")
    if "public_only" not in piv.columns or "private_only" not in piv.columns:
        return {}
    out = {}
    for (seq, seed, bm), row in piv.iterrows():
        if pd.notna(row["public_only"]) and pd.notna(row["private_only"]):
            out[(seq, int(seed), bm)] = float(row["private_only"] - row["public_only"])
    return out


def cv_evaluate(runs, obs_dgap_lookup, n_splits: int = 5, random_state: int = 42):
    """5-fold CV by seed: fit null on training seeds, predict cap for test seeds, compute
    dgap predictions, return aggregated long DataFrame across all folds."""
    all_seeds = sorted(set(r["seed"] for r in runs))
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    long_rows = []
    fold_metrics = []
    for fold_i, (train_idx, test_idx) in enumerate(kf.split(all_seeds)):
        train_seeds = {all_seeds[i] for i in train_idx}
        test_seeds = {all_seeds[i] for i in test_idx}
        train_runs = [r for r in runs if r["seed"] in train_seeds]
        test_runs = [r for r in runs if r["seed"] in test_seeds]

        train_table = build_training_table(train_runs)
        models = fit_null_per_provider_dim(train_table)

        # Predict null cap for each test (seq, seed)
        null_cap_lookup = {}
        for run in test_runs:
            null_caps = predict_null_cap(models, run["init_cap"], run["init_portfolio"])
            for prov, cap in null_caps.items():
                null_cap_lookup[(run["sequence"], run["seed"], prov)] = cap

        df = compute_dgap_predictions(test_runs, null_cap_lookup, obs_dgap_lookup)
        df["fold"] = fold_i
        long_rows.append(df)

        if not df.empty:
            r_null = float(np.corrcoef(df.obs_dgap, df.null_dgap)[0, 1]) if len(df) >= 2 else float("nan")
            r_sim  = float(np.corrcoef(df.obs_dgap, df.sim_dgap)[0, 1])  if len(df) >= 2 else float("nan")
            mae_null = float(np.mean(np.abs(df.obs_dgap - df.null_dgap)))
            mae_sim  = float(np.mean(np.abs(df.obs_dgap - df.sim_dgap)))
            fold_metrics.append({
                "fold": fold_i, "n_test_seeds": len(test_seeds), "n_cells": len(df),
                "r_null": r_null, "r_sim": r_sim,
                "r2_null": r_null ** 2 if r_null == r_null else float("nan"),
                "r2_sim":  r_sim ** 2 if r_sim == r_sim else float("nan"),
                "mae_null": mae_null, "mae_sim": mae_sim,
            })
            print(f"fold {fold_i}: n={len(df)} cells | r_null={r_null:.3f} (r²={r_null**2:.3f}) "
                  f"| r_sim={r_sim:.3f} (r²={r_sim**2:.3f}) | mae_null={mae_null:.4f} mae_sim={mae_sim:.4f}")

    return (pd.concat(long_rows, ignore_index=True) if long_rows else pd.DataFrame(),
            pd.DataFrame(fold_metrics))


def plot_two_panel(long_df, out_path):
    """Two scatter panels: null prediction (left) | sim prediction (right). Both with y=x."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6.0), sharex=True, sharey=True)

    if long_df.empty:
        for ax in axes:
            ax.text(0.5, 0.5, "no data", ha="center", va="center", transform=ax.transAxes)
    else:
        lo = min(long_df.obs_dgap.min(), long_df.null_dgap.min(), long_df.sim_dgap.min()) - 0.005
        hi = max(long_df.obs_dgap.max(), long_df.null_dgap.max(), long_df.sim_dgap.max()) + 0.005

        # Left: null
        ax = axes[0]
        ax.scatter(long_df.obs_dgap, long_df.null_dgap, s=12, c="#888", alpha=0.35,
                   edgecolors="none", rasterized=True)
        ax.plot([lo, hi], [lo, hi], ls="--", color="black", lw=0.8, alpha=0.6,
                label="y = x")
        r_null = float(np.corrcoef(long_df.obs_dgap, long_df.null_dgap)[0, 1])
        rmse_null = float(np.sqrt(((long_df.obs_dgap - long_df.null_dgap) ** 2).mean()))
        ax.set_title(f"NULL model: cap predicted from initial conditions only\n"
                     f"r = {r_null:.3f}  |  r² = {r_null**2:.3f}  |  RMSE from y=x: {rmse_null:.4f}",
                     fontsize=10.5)
        ax.set_xlabel(r"Observed $\Delta$gap (private_only $-$ public_only)")
        ax.set_ylabel(r"Predicted $\Delta$gap")
        ax.set_xlim(lo, hi); ax.set_ylim(lo, hi); ax.set_aspect("equal", adjustable="box")
        ax.axhline(0, color="gray", lw=0.4, alpha=0.4)
        ax.axvline(0, color="gray", lw=0.4, alpha=0.4)
        ax.legend(loc="upper left", fontsize=9)

        # Right: sim
        ax = axes[1]
        ax.scatter(long_df.obs_dgap, long_df.sim_dgap, s=12, c="#1f77b4", alpha=0.45,
                   edgecolors="none", rasterized=True)
        ax.plot([lo, hi], [lo, hi], ls="--", color="black", lw=0.8, alpha=0.6,
                label="y = x")
        r_sim = float(np.corrcoef(long_df.obs_dgap, long_df.sim_dgap)[0, 1])
        rmse_sim = float(np.sqrt(((long_df.obs_dgap - long_df.sim_dgap) ** 2).mean()))
        ax.set_title(f"SIM model: cap from running the simulation (40 rounds)\n"
                     f"r = {r_sim:.3f}  |  r² = {r_sim**2:.3f}  |  RMSE from y=x: {rmse_sim:.4f}",
                     fontsize=10.5)
        ax.set_xlabel(r"Observed $\Delta$gap (private_only $-$ public_only)")
        ax.legend(loc="upper left", fontsize=9)

    fig.suptitle("Null-vs-sim capability prediction: how much variance is sim-specific vs initial-conditions?",
                 y=1.005, fontsize=12)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        out = out_path + "." + ext
        fig.savefig(out, dpi=160, bbox_inches="tight")
        print(f"  wrote {out}")
    plt.close(fig)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=("heuristic", "llm"), default="heuristic",
                   help="Which run set to analyze. heuristic = sandbox/experiments/<batch>/heuristic; "
                        "llm = hf_data_staging/<bucket>/llm/<model>.")
    p.add_argument("--batch", default="_seq_robustness", help="Sandbox batch (heuristic mode only)")
    p.add_argument("--bucket", default="core_privacy", help="HF staging bucket (llm mode only)")
    p.add_argument("--llm-model", default="claude-sonnet-4-6", help="Canonical model name (llm mode only)")
    p.add_argument("--folds", type=int, default=5)
    p.add_argument("--obs-from-csv", action="store_true",
                   help="Load observed dgap from sequence_robustness_per_bm_long.csv (faster, "
                        "heuristic-mode only). Default: compute inline via per_benchmark_from_rows.")
    p.add_argument("--out-suffix", default=None,
                   help="Suffix appended to output filenames (default: derived from mode).")
    args = p.parse_args()

    if args.mode == "heuristic":
        print(f"Loading heuristic runs from sandbox/experiments/{args.batch}/heuristic/ ...")
        runs = collect_runs(args.batch)
        default_suffix = ""
    else:
        print(f"Loading LLM runs from hf_data_staging/{args.bucket}/llm/{args.llm_model}/ ...")
        runs = collect_runs_llm(args.bucket, args.llm_model)
        default_suffix = f"_llm_{args.llm_model.replace('-', '')}"

    print(f"  {len(runs)} runs loaded across "
          f"{len(set((r['sequence'], r['rung']) for r in runs))} (seq, rung) cells")
    if not runs:
        print("No runs found. Exiting.")
        return

    if args.mode == "heuristic" and args.obs_from_csv:
        print("Loading observed dgap from sequence_robustness_per_bm_long.csv ...")
        obs_csv = os.path.join(_paths.paper_dir(), "sequence_robustness_per_bm_long.csv")
        obs_dgap_lookup = load_obs_dgap_from_csv(obs_csv)
    else:
        print("Computing observed dgap inline from rounds.jsonl ...")
        obs_dgap_lookup = compute_obs_dgap_inline(runs)
    print(f"  {len(obs_dgap_lookup)} observed (seq, seed, bm) dgap cells loaded")
    if not obs_dgap_lookup:
        print("No observed dgap cells (need both pub_only and priv_only runs per seq/seed). Exiting.")
        return

    print(f"\nFitting null + {args.folds}-fold CV ...")
    long_df, fold_df = cv_evaluate(runs, obs_dgap_lookup, n_splits=args.folds)

    out_dir = _paths.paper_dir()
    suffix = args.out_suffix if args.out_suffix is not None else default_suffix
    long_csv = os.path.join(out_dir, f"null_model_capability_long{suffix}.csv")
    metrics_csv = os.path.join(out_dir, f"null_model_capability_metrics{suffix}.csv")
    long_df.to_csv(long_csv, index=False)
    fold_df.to_csv(metrics_csv, index=False)
    print(f"\nWrote {long_csv}  ({len(long_df)} cells)")
    print(f"Wrote {metrics_csv}")

    if not long_df.empty:
        r_null_all = float(np.corrcoef(long_df.obs_dgap, long_df.null_dgap)[0, 1])
        r_sim_all  = float(np.corrcoef(long_df.obs_dgap, long_df.sim_dgap)[0, 1])
        print(f"\nPooled across folds: r_null = {r_null_all:.3f} (r2 = {r_null_all**2:.3f}), "
              f"r_sim = {r_sim_all:.3f} (r2 = {r_sim_all**2:.3f})")
        print(f"Sim-specific contribution to r2: {r_sim_all**2 - r_null_all**2:+.3f}")

    plot_two_panel(long_df, os.path.join(out_dir, f"null_model_capability_scatter{suffix}"))


if __name__ == "__main__":
    main()
