"""Per-benchmark widening under holdout designs, paired by seed (paper Appendix F, Table tab:holdout-widening).

For each benchmark and seed, g is the provider-mean gap (score minus matched satisfaction,
as in Figure 4). A seed "widens" under a condition when |g_condition| > |g_public_only| for
that seed. Reports the fraction of seeds that widen under private_only and under the
iid_holdout null, for LLM (Sonnet 4.6) and heuristic modes, plus the sign of the change in
mean g and in mean |g|.

Data: hf_data_staging/core_privacy (the Figure 4 runs).

Usage: python -m scripts.plots.paper.holdout_widening_table
Output: output/paper/holdout_widening_table.csv
"""
from __future__ import annotations

import os

import pandas as pd

from scripts.plots import paths as _paths
from scripts.plots.per_benchmark import BM_ORDER, EXCLUDE_BM
from scripts.plots.per_benchmark_core_privacy import build_long_df
from scripts.plots.paper.privacy_gap_main import build_long_df_heuristic

CONDS = ["public_only", "private_only", "iid_holdout"]


def per_seed_gap(df: pd.DataFrame) -> pd.DataFrame:
    g = df[df.condition.isin(CONDS)].groupby(["condition", "seed", "benchmark"])["clean_gap"].mean()
    return g.unstack("condition").dropna(subset=["public_only"])


def summarize(wide: pd.DataFrame, mode: str) -> pd.DataFrame:
    rows = []
    for bm in BM_ORDER:
        if bm not in wide.index.get_level_values("benchmark"):
            continue
        w = wide.xs(bm, level="benchmark")
        row = {"mode": mode, "benchmark": bm, "in_figure4": bm not in EXCLUDE_BM,
               "g_public_mean": w["public_only"].mean()}
        for cond in ["private_only", "iid_holdout"]:
            paired = w[["public_only", cond]].dropna()
            row[f"n_{cond}"] = len(paired)
            row[f"frac_widen_{cond}"] = float((paired[cond].abs() > paired["public_only"].abs()).mean())
            row[f"g_{cond}_mean"] = paired[cond].mean()
        row["abs_mean_widens_private"] = abs(row["g_private_only_mean"]) > abs(row["g_public_mean"])
        rows.append(row)
    return pd.DataFrame(rows)


def roster_sequences() -> pd.DataFrame:
    """Same widening fraction across benchmark-roster sequences (heuristic, output of
    scripts/plots/paper/sequence_robustness.py): does the widening set follow roster composition?"""
    d = pd.read_csv(os.path.join(_paths.paper_dir(), "sequence_robustness_per_bm_long.csv"))
    wide = d[d.rung.isin(["public_only", "private_only"])].pivot_table(
        index=["sequence", "seed", "benchmark"], columns="rung", values="mean_gap").dropna()
    frac = (wide["private_only"].abs() > wide["public_only"].abs()).groupby(["sequence", "benchmark"]).mean()
    n = wide.groupby(["sequence", "benchmark"]).size()
    return pd.DataFrame({"frac_widen_private_only": frac, "n_seeds": n}).reset_index()


def main():
    seq = roster_sequences()
    seq_path = os.path.join(_paths.paper_dir(), "holdout_widening_by_roster.csv")
    seq.to_csv(seq_path, index=False)
    focus = ["Clinical Reasoning", "Legal Reasoning", "Instruction Following", "Adversarial Robustness", "Long Context"]
    print(seq[seq.benchmark.isin(focus)].pivot(index="sequence", columns="benchmark",
                                               values="frac_widen_private_only").round(2).to_string())
    print("seeds per sequence:", seq.groupby("sequence").n_seeds.max().to_dict())
    print(f"Wrote {seq_path}")

    llm = build_long_df("_core_privacy", "sonnet")
    heur = build_long_df_heuristic(restrict_conds=CONDS)
    out = pd.concat([summarize(per_seed_gap(llm), "llm_sonnet"),
                     summarize(per_seed_gap(heur), "heuristic")], ignore_index=True)
    path = os.path.join(_paths.paper_dir(), "holdout_widening_table.csv")
    out.to_csv(path, index=False)
    cols = ["mode", "benchmark", "n_private_only", "frac_widen_private_only", "n_iid_holdout",
            "frac_widen_iid_holdout", "g_public_mean", "g_private_only_mean", "abs_mean_widens_private"]
    with pd.option_context("display.width", 200, "display.max_rows", 40):
        print(out[cols].round(3).to_string(index=False))
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
