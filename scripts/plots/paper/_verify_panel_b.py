"""Print the panel-b data so we can sanity-check what's being plotted."""
import os, sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))
import glob
import numpy as np
import pandas as pd

from scripts.plots import paths as _paths
from scripts.plots.per_benchmark_core_privacy import build_long_df
from scripts.plots.paper.privacy_gap_main import (
    build_long_df_heuristic, benchmark_primary_dims,
    population_capability_surplus, _build_panel_b_points,
    discover_heuristic_runs, EXCLUDE_BM,
)

print("=" * 70)
print("LLM Sonnet 4.6 (hf_data_staging/core_privacy/llm/claude-sonnet-4-6)")
print("=" * 70)
df_llm = build_long_df("_core_privacy", "sonnet")
df_llm = df_llm[~df_llm.benchmark.isin(EXCLUDE_BM)]
n_seeds_llm = df_llm[df_llm.condition == "public_only"]["seed"].nunique()
print(f"  public_only seeds: {n_seeds_llm}")

print("\n" + "=" * 70)
print("Heuristic (hf_data_staging/core_privacy/heuristic)")
print("=" * 70)
df_heur = build_long_df_heuristic()
df_heur = df_heur[~df_heur.benchmark.isin(EXCLUDE_BM)]
n_seeds_heur = df_heur[df_heur.condition == "public_only"]["seed"].nunique()
print(f"  public_only seeds: {n_seeds_heur}")

# Sample LLM jsonl for primary-dim inference
sample = sorted(glob.glob(os.path.join(
    _paths.PROJECT_ROOT, "hf_data_staging", "core_privacy",
    "llm", "claude-sonnet-4-6", "public_only", "seed_*", "rounds.jsonl")))
primary = benchmark_primary_dims(sample[0])

llm_pub_jsonls = sample
heur_pub_jsonls = [j for cond, _s, j in discover_heuristic_runs() if cond == "public_only"]

llm_pts  = _build_panel_b_points(df_llm,  llm_pub_jsonls,  primary)
heur_pts = _build_panel_b_points(df_heur, heur_pub_jsonls, primary)

print("\n" + "=" * 70)
print("LLM panel-b points (each row: surplus_x, dgap_y)")
print("=" * 70)
print(llm_pts.sort_values("surplus").to_string(index=False))
print("\n" + "=" * 70)
print("HEURISTIC panel-b points")
print("=" * 70)
print(heur_pts.sort_values("surplus").to_string(index=False))

print("\n" + "=" * 70)
print("Correlations / regressions")
print("=" * 70)
for label, df in [("LLM", llm_pts), ("HEUR", heur_pts)]:
    r = float(np.corrcoef(df.surplus, df.dgap)[0, 1])
    slope, intercept = np.polyfit(df.surplus, df.dgap, 1)
    print(f"  {label}: r = {r:+.4f}, slope = {slope:+.4f}, intercept = {intercept:+.5f}, "
          f"surplus_range = [{df.surplus.min():+.4f}, {df.surplus.max():+.4f}]")

# Compare LLM-mode capability surplus per dimension to heuristic-mode capability surplus
print("\n" + "=" * 70)
print("Pop capability per dimension (averaged across providers + rounds + seeds)")
print("=" * 70)
from scripts.plots.per_benchmark import DIMS
import json
from collections import defaultdict
def pop_vec(jsonls):
    per_run = []
    for j in jsonls:
        rounds = [json.loads(l) for l in open(j) if l.strip()]
        if not rounds: continue
        accum = defaultdict(lambda: np.zeros(len(DIMS)))
        cnt = defaultdict(int)
        for r in rounds:
            for p, cap in r.get("capability_vectors", {}).items():
                v = np.array([cap.get(k, 0.0) for k in DIMS])
                accum[p] += v; cnt[p] += 1
        per_run.append({p: accum[p] / cnt[p] for p, c in cnt.items() if c})
    if not per_run: return None
    provs = set().union(*(d.keys() for d in per_run))
    prov_mean = {p: np.mean([d[p] for d in per_run if p in d], axis=0) for p in provs}
    return np.mean(list(prov_mean.values()), axis=0)

llm_pop = pop_vec(llm_pub_jsonls)
heur_pop = pop_vec(heur_pub_jsonls)
print(f"  {'dim':<14} {'LLM':>10} {'HEUR':>10}")
for i, d in enumerate(DIMS):
    print(f"  {d:<14} {llm_pop[i]:>10.4f} {heur_pop[i]:>10.4f}")
print(f"  {'mean':<14} {llm_pop.mean():>10.4f} {heur_pop.mean():>10.4f}")
print()
print(f"  {'surplus':<14} {'LLM':>10} {'HEUR':>10}")
for i, d in enumerate(DIMS):
    print(f"  {d:<14} {llm_pop[i] - llm_pop.mean():>+10.4f} "
          f"{heur_pop[i] - heur_pop.mean():>+10.4f}")
