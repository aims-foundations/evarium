"""Within-benchmark rescoring: scoring-layer versus capability share of the holdout gap shift
(paper Appendix F, Robustness check 3).

For each benchmark b and matched seed s, with C_priv / C_pub the end-of-run capability
matrices of the private_only / public_only heuristic runs and w_pub / w_hold the same
benchmark's public and holdout weight vectors (logged in each run's config.json):

  scoring-layer effect  S = score(C_priv, w_hold) - score(C_priv, w_pub)
  capability effect     K = score(C_priv, w_pub)  - score(C_pub,  w_pub)

score(C, w) = mean over providers of dot(cap_p, w): the simulation's linear projection,
without observation noise and without the running-max publication rule. Matched
satisfaction does not depend on the scoring weights, so S passes into delta g one-for-one
and delta_g_noiseless = S + (K - delta_matched_sat).

Also evaluates the identity delta g = c . (w_hold - w_pub) on round-0 capability (mean of
the configured provider vectors) and compares its sign with the logged delta g.

Data: hf_data_staging/core_privacy/heuristic/{public_only,private_only}/seed_*

Usage: python -m scripts.plots.paper.holdout_rescoring
Output: output/paper/holdout_rescoring_per_benchmark.csv, output/paper/holdout_rescoring_paired.csv
"""
from __future__ import annotations

import glob
import json
import os
import sys

import numpy as np
import pandas as pd

from scripts.plots import paths as _paths

sys.path.insert(0, os.path.join(_paths.PROJECT_ROOT, "src", "actors"))
from consumer import USE_CASE_PROFILES  # type: ignore  # noqa: E402

DIMS = ["reasoning", "coding", "knowledge", "safety", "communication", "agentic"]
DATA_ROOT = os.path.join(_paths.PROJECT_ROOT, "hf_data_staging", "core_privacy", "heuristic")
OUTLIERS = ["Agentic Tasks", "Function Calling"]
MIN_ROUNDS = 40


def _vec(d):
    return np.array([d.get(k, 0.0) for k in DIMS], dtype=float)


def _normalize(x):
    s = x.sum()
    return x / s if s > 0 else x


def agg_cdw(cdw):
    """Average the per-category dimension weights (evaluator._score_provider_on_benchmark)."""
    agg = {}
    for cat_w in cdw.values():
        for d, w in cat_w.items():
            agg[d] = agg.get(d, 0.0) + w
    n = len(cdw)
    return _vec({d: w / n for d, w in agg.items()})


def load_weights():
    """Public and holdout weight vectors per benchmark; asserts they are identical across seeds."""
    w_pub, w_hold = {}, {}
    for cond in ["private_only", "public_only"]:
        for rd in sorted(glob.glob(os.path.join(DATA_ROOT, cond, "seed_*"))):
            with open(os.path.join(rd, "config.json")) as f:
                cfg = json.load(f)
            for b in (cfg["benchmarks"] or []) + (cfg["benchmark_sequence"] or []):
                name = b["name"]
                pub = agg_cdw(b["category_dimension_weights"])
                if name in w_pub:
                    assert np.allclose(w_pub[name], pub, atol=1e-12), f"public weights differ: {name} {rd}"
                else:
                    w_pub[name] = pub
                if cond == "private_only":
                    hw = b.get("holdout_category_dimension_weights")
                    assert hw is not None, f"missing holdout weights: {name} {rd}"
                    hold = agg_cdw(hw)
                    if name in w_hold:
                        assert np.allclose(w_hold[name], hold, atol=1e-12), f"holdout weights differ: {name} {rd}"
                    else:
                        w_hold[name] = hold
    return w_pub, w_hold


def load_final_states(cond):
    """{seed: final-round record} for runs with at least MIN_ROUNDS rounds."""
    out = {}
    for rd in sorted(glob.glob(os.path.join(DATA_ROOT, cond, "seed_*"))):
        path = os.path.join(rd, "rounds.jsonl")
        if not os.path.exists(path):
            continue
        with open(path) as f:
            rows = [json.loads(line) for line in f]
        if len(rows) < MIN_ROUNDS:
            continue
        out[int(os.path.basename(rd).replace("seed_", ""))] = rows[-1]
    return out


def matched_sat(last, w_pub_norm):
    """Per-benchmark matched satisfaction (per_benchmark.py convention), mean over providers."""
    providers = list(last["scores"].keys())
    cap = {p: _vec(last["capability_vectors"][p]) for p in providers}
    segdata = last["consumer_data"]["segment_data"]
    names = list(segdata.keys())
    nw_mat = np.zeros((len(names), len(DIMS)))
    sizes = np.zeros(len(names))
    for i, n in enumerate(names):
        sd = segdata[n]
        nw = USE_CASE_PROFILES.get(sd.get("use_case"), {}).get("need_weights")
        nw_mat[i] = _normalize(_vec(nw)) if nw else np.ones(len(DIMS)) / len(DIMS)
        sizes[i] = float(sd.get("market_fraction", 0.0))
    out = {}
    for bm, cdw_b in w_pub_norm.items():
        weights = (nw_mat @ cdw_b) * sizes
        denom = weights.sum()
        out[bm] = float(np.mean([np.sum((nw_mat @ cap[p]) * weights) / denom for p in providers]))
    return out


def logged_score(last, bm):
    return float(np.mean(list(last["per_benchmark_scores"][bm].values())))


def main():
    w_pub, w_hold = load_weights()
    bms = sorted(w_pub)
    assert all(bm in w_hold for bm in bms)
    w_pub_norm = {bm: _normalize(w_pub[bm]) for bm in bms}

    pub_runs = load_final_states("public_only")
    prv_runs = load_final_states("private_only")
    seeds = sorted(set(pub_runs) & set(prv_runs))
    print(f"benchmarks: {len(bms)}; matched seeds: N={len(seeds)} ({min(seeds)}..{max(seeds)})")

    with open(os.path.join(DATA_ROOT, "private_only", f"seed_{seeds[0]}", "config.json")) as f:
        cfg = json.load(f)
    c_init = np.array([_vec(p["capability_vector"]) for p in cfg["provider_configs"]]).mean(axis=0)

    rows = []
    for s in seeds:
        lp, lv = pub_runs[s], prv_runs[s]
        provs = sorted(lp["capability_vectors"].keys())
        assert provs == sorted(lv["capability_vectors"].keys())
        C_pub = np.array([_vec(lp["capability_vectors"][p]) for p in provs])
        C_prv = np.array([_vec(lv["capability_vectors"][p]) for p in provs])
        ms_pub, ms_prv = matched_sat(lp, w_pub_norm), matched_sat(lv, w_pub_norm)
        for bm in bms:
            sc_prv_hold = float((C_prv @ w_hold[bm]).mean())
            sc_prv_pub = float((C_prv @ w_pub[bm]).mean())
            sc_pub_pub = float((C_pub @ w_pub[bm]).mean())
            S = sc_prv_hold - sc_prv_pub
            K = sc_prv_pub - sc_pub_pub
            d_ms = ms_prv[bm] - ms_pub[bm]
            rows.append({
                "seed": s, "benchmark": bm,
                "scoring_layer": S, "capability": K,
                "delta_matched_sat": d_ms,
                "delta_g_noiseless": S + K - d_ms,
                "remainder_delta_g": K - d_ms,
                "delta_g_logged": (logged_score(lv, bm) - ms_prv[bm]) - (logged_score(lp, bm) - ms_pub[bm]),
            })
    df = pd.DataFrame(rows)
    out_dir = _paths.paper_dir()
    df.to_csv(os.path.join(out_dir, "holdout_rescoring_paired.csv"), index=False)

    def ci(x):
        return 1.96 * x.std(ddof=1) / np.sqrt(len(x))

    agg = df.groupby("benchmark").agg(
        n=("seed", "count"),
        S_mean=("scoring_layer", "mean"), S_ci=("scoring_layer", ci),
        K_mean=("capability", "mean"), K_ci=("capability", ci),
        dg_noiseless=("delta_g_noiseless", "mean"),
        dg_logged=("delta_g_logged", "mean"),
        rem_mean=("remainder_delta_g", "mean"),
    ).reset_index()
    agg["identity_round0"] = [float(c_init @ (w_hold[b] - w_pub[b])) for b in agg["benchmark"]]
    agg = agg.sort_values("dg_noiseless").reset_index(drop=True)
    agg.to_csv(os.path.join(out_dir, "holdout_rescoring_per_benchmark.csv"), index=False)

    with pd.option_context("display.float_format", "{:+.4f}".format, "display.width", 200):
        print(agg.to_string(index=False))

    sgn = lambda x: np.sign(np.round(x, 10))  # noqa: E731
    print(f"\nsign(S) == sign(delta g logged): {int((sgn(agg.S_mean) == sgn(agg.dg_logged)).sum())}/{len(agg)}")
    print(f"S significant at 95%: {int((agg.S_mean.abs() > agg.S_ci).sum())}/{len(agg)}")
    print(f"K indistinguishable from zero: {int((agg.K_mean.abs() <= agg.K_ci).sum())}/{len(agg)}")
    miss = agg[sgn(agg.identity_round0) != sgn(agg.dg_logged)].benchmark.tolist()
    print(f"sign(identity at round 0) == sign(delta g logged): {len(agg) - len(miss)}/{len(agg)}; misses: {miss}")
    print(f"max |delta g noiseless - logged| per benchmark: {(agg.dg_noiseless - agg.dg_logged).abs().max():.4f}")
    for label, sub in [("all 13", agg), ("11 without outliers", agg[~agg.benchmark.isin(OUTLIERS)])]:
        S, R = sub.S_mean.abs().sum(), sub.rem_mean.abs().sum()
        print(f"scoring-layer share of delta g, sum|S|/(sum|S|+sum|rem|), {label}: {S / (S + R):.3f}")


if __name__ == "__main__":
    main()
