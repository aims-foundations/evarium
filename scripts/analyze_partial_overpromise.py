"""Diagnostic: why does `partial` overpromise more than `public` in heuristic mode?

For a set of runs, compute per (benchmark, provider, seed) at the final round:
    s_pub  = dot(cap, public_weights)    [expected score if benchmark were public]
    s_hold = dot(cap, holdout_weights)   [expected score if scored on holdout]
    score  = actual published score
    match  = matched-sat vs public weights (consumer-needs-aligned)
Then check:
    Does score ≈ s_pub (public) or s_hold (partial/private)?
    Is matched using public or holdout?
    Which term (s_pub vs s_hold vs ratchet vs noise vs matched) drives the partial>public gap?
"""
from __future__ import annotations
import json, os, glob, sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "actors"))
from consumer import USE_CASE_PROFILES  # type: ignore

DIMS = ["reasoning", "coding", "knowledge", "safety", "communication", "agentic"]


def _vec(d): return np.array([d.get(k, 0.0) for k in DIMS], dtype=float)
def _norm(x):
    s = x.sum()
    return x / s if s > 0 else x


def _agg_cdw(cat_dim_weights):
    """Avg per-category loadings into a flat dim vector (same rule as evaluator.py)."""
    if not cat_dim_weights:
        return None
    if isinstance(next(iter(cat_dim_weights.values())), dict):
        agg = {}
        for cat in cat_dim_weights.values():
            for d, w in cat.items():
                agg[d] = agg.get(d, 0.0) + w
        n = len(cat_dim_weights)
        return {d: w / n for d, w in agg.items()}
    return dict(cat_dim_weights)


def load_config_weights(config_path):
    """Return {bm_name: {type, public_w, holdout_w}}."""
    with open(config_path) as f:
        cfg = json.load(f)
    bms = list(cfg.get("benchmarks", [])) + list(cfg.get("benchmark_sequence", []))
    out = {}
    for b in bms:
        name = b.get("name")
        if not name:
            continue
        pub_agg = _agg_cdw(b.get("category_dimension_weights"))
        hold_agg = _agg_cdw(b.get("holdout_category_dimension_weights"))
        out[name] = {
            "type": b.get("benchmark_type", "public"),
            "public_w": _norm(_vec(pub_agg)) if pub_agg else None,
            "holdout_w": _norm(_vec(hold_agg)) if hold_agg else None,
        }
    return out


def analyze_run(rounds_path, config_path):
    """Per benchmark × provider row: type, score, s_pub, s_hold, matched."""
    wmap = load_config_weights(config_path)
    with open(rounds_path) as f:
        rows = [json.loads(l) for l in f]
    last = rows[-1]
    providers = list(last["scores"].keys())
    caps = {p: _vec(last["capability_vectors"][p]) for p in providers}

    cdw_logged = {b: _norm(_vec(last["benchmark_dimension_weights"][b]))
                  for b in last["per_benchmark_scores"].keys()}

    seg = last["consumer_data"]["segment_data"]
    nw_mat = np.zeros((len(seg), len(DIMS)))
    sizes = np.zeros(len(seg))
    for i, n in enumerate(seg):
        uc = seg[n].get("use_case")
        nw = USE_CASE_PROFILES.get(uc, {}).get("need_weights")
        nw_mat[i] = _norm(_vec(nw)) if nw else np.ones(len(DIMS)) / len(DIMS)
        sizes[i] = float(seg[n].get("market_fraction", 0.0))

    rows_out = []
    for bm, cdw_b in cdw_logged.items():
        meta = wmap.get(bm, {})
        pub_w = meta.get("public_w")
        hold_w = meta.get("holdout_w")
        btype = meta.get("type", "public")
        # matched_sat uses cdw_logged (public per evaluator.py)
        alignment = nw_mat @ cdw_b
        weights = alignment * sizes
        denom = weights.sum()
        if denom <= 0 or pub_w is None:
            continue
        for p, cap in caps.items():
            score = float(last["per_benchmark_scores"][bm].get(p, 0.0))
            base = nw_mat @ cap
            matched = float(np.sum(base * weights) / denom)
            s_pub = float(np.dot(cap, pub_w))
            s_hold = float(np.dot(cap, hold_w)) if hold_w is not None else np.nan
            rows_out.append({
                "benchmark": bm, "provider": p, "type": btype,
                "score": score, "s_pub": s_pub, "s_hold": s_hold,
                "matched": matched,
                "cdw_matches_public": float(np.allclose(cdw_b, pub_w, atol=1e-6)),
            })
    return pd.DataFrame(rows_out)


def walk_runs(batches, modes=("heuristic",)):
    """Walk sandbox/experiments/<batch>/<mode>/<cond>/seeds/seed_*/ for listed batches."""
    root = os.path.join(os.path.dirname(__file__), "..", "sandbox", "experiments")
    paths = []
    for batch in batches:
        for mode in modes:
            paths.extend(glob.glob(os.path.join(root, batch, mode, "*", "seeds", "seed_*")))
    return sorted(paths)


def main():
    # Focus: heuristic, session-38+ batches with benchmark_type and multiple privacy conditions
    batches = ["heuristic_apr19_postF1", "session38_heuristic", "session41_rebaseline"]
    dirs = walk_runs(batches, modes=("heuristic",))
    # Limit to a reasonable sample — 200 runs gives us plenty
    import random
    random.seed(0)
    random.shuffle(dirs)
    dirs = dirs[:200]

    all_rows = []
    for d in dirs:
        r = os.path.join(d, "rounds.jsonl")
        c = os.path.join(d, "config.json")
        if not (os.path.exists(r) and os.path.exists(c)):
            continue
        try:
            df = analyze_run(r, c)
        except Exception as e:
            print(f"SKIP {d}: {e}")
            continue
        parts = d.replace("\\", "/").split("/")
        df["condition"] = parts[-3]
        df["seed"] = parts[-1]
        all_rows.append(df)

    df = pd.concat(all_rows, ignore_index=True)
    # Exclude Agentic Tasks calibration outlier
    df = df[df.benchmark != "Agentic Tasks"]
    print(f"Sampled {len(dirs)} runs -> {len(df)} rows")
    print()

    # 1. Is matched using public weights?
    print(f"cdw_logged matches public_w in config: {df['cdw_matches_public'].mean()*100:.1f}%")
    print()

    # 2a. Within the *baseline* condition only — clean within-run comparison.
    #     baseline has ~18 public + ~3 partial + ~1 private, same providers same capability.
    bl = df[df["condition"].isin(["baseline"])]
    print(f"Within baseline only (n_rows={len(bl)}):")
    agg_bl = bl.groupby("type").agg(
        n=("score", "count"),
        score=("score", "mean"),
        s_pub=("s_pub", "mean"),
        s_hold=("s_hold", "mean"),
        matched=("matched", "mean"),
    ).round(4)
    agg_bl["gap"] = (agg_bl["score"] - agg_bl["matched"]).round(4)
    agg_bl["score_minus_s_pub"] = (agg_bl["score"] - agg_bl["s_pub"]).round(4)
    agg_bl["score_minus_s_hold"] = (agg_bl["score"] - agg_bl["s_hold"]).round(4)
    with pd.option_context("display.max_columns", None, "display.width", 200):
        print(agg_bl)
    print()

    # 2b. Per-benchmark within baseline — how much does each partial/private benchmark's
    #     holdout_weights reduce its score vs public counterfactual?
    print("Within baseline, per-benchmark:")
    bl_bm = bl.groupby(["benchmark", "type"]).agg(
        n=("score", "count"),
        score=("score", "mean"),
        s_pub=("s_pub", "mean"),
        s_hold=("s_hold", "mean"),
        matched=("matched", "mean"),
    ).round(4)
    bl_bm["gap"] = (bl_bm["score"] - bl_bm["matched"]).round(4)
    bl_bm["hold_vs_pub"] = (bl_bm["s_hold"] - bl_bm["s_pub"]).round(4)
    with pd.option_context("display.max_columns", None, "display.width", 200):
        print(bl_bm)
    print()

    # 2c. Per type (all conditions pooled — caveat: confounded)
    print("Per type (all conditions pooled — CONFOUNDED by condition):")
    agg = df.groupby("type").agg(
        n=("score", "count"),
        score=("score", "mean"),
        s_pub=("s_pub", "mean"),
        s_hold=("s_hold", "mean"),
        matched=("matched", "mean"),
    ).round(4)
    agg["score_minus_pub"] = (agg["score"] - agg["s_pub"]).round(4)
    agg["score_minus_hold"] = (agg["score"] - agg["s_hold"]).round(4)
    agg["score_minus_matched"] = (agg["score"] - agg["matched"]).round(4)
    agg["hold_minus_pub"] = (agg["s_hold"] - agg["s_pub"]).round(4)
    with pd.option_context("display.max_columns", None, "display.width", 200):
        print(agg)
    print()

    # 3. Which dimensions does partial holdout shift weight toward vs public?
    # For the partial type, compare holdout_w to public_w dimension-by-dimension
    print("Partial: holdout_weights - public_weights (avg per dim, across benchmarks)")
    partial = df[df.type == "partial"].drop_duplicates(subset=["benchmark"])
    if len(partial):
        # Re-load weights from config to get dim-level view
        diffs = []
        seen = set()
        for _, row in partial.iterrows():
            if row.benchmark in seen:
                continue
            seen.add(row.benchmark)
        # Take any run with that benchmark in partial type
        d = dirs[0]
        c = os.path.join(d, "config.json")
        wmap = load_config_weights(c)
        for bm in sorted(seen):
            if bm not in wmap:
                continue
            pub = wmap[bm]["public_w"]
            hold = wmap[bm]["holdout_w"]
            if pub is None or hold is None:
                continue
            diff = hold - pub
            print(f"  {bm:30s}  diff=[", end="")
            for i, d_name in enumerate(DIMS):
                print(f"{d_name[:4]}:{diff[i]:+.3f} ", end="")
            print("]")
    print()

    # 4. Capability per dim, then check which dims the partial's shift rewards
    print("Mean capability per dim (across all runs):")
    cap_means = []
    for d in dirs[:50]:
        r = os.path.join(d, "rounds.jsonl")
        if not os.path.exists(r): continue
        with open(r) as f:
            last = json.loads(list(f)[-1])
        for p, v in last.get("capability_vectors", {}).items():
            cap_means.append(_vec(v))
    if cap_means:
        cap_mean = np.mean(cap_means, axis=0)
        for i, d_name in enumerate(DIMS):
            print(f"  {d_name:15s} {cap_mean[i]:.3f}")


if __name__ == "__main__":
    main()
