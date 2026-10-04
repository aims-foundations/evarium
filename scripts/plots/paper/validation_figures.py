"""
plot_validation_figures.py
Exploratory analysis of hf_data/runs.jsonl — LLM models only (no heuristic).
Saves all plots to evaluation_ecosystem_overleaf/figures/validation/.
"""

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from .. import paths as _paths

# ── Paths ─────────────────────────────────────────────────────────────────────

ROOT = Path(_paths.PROJECT_ROOT)
runs_path = ROOT / "hf_data" / "runs.jsonl"
FIG_DIR = ROOT.parent / "evaluation_ecosystem_overleaf" / "figures" / "validation"
FIG_DIR.mkdir(parents=True, exist_ok=True)

def savefig(name):
    path = FIG_DIR / f"{name}.pdf"
    plt.savefig(path, bbox_inches="tight")
    print(f"  saved {path.relative_to(ROOT.parent)}")

# ── Load ──────────────────────────────────────────────────────────────────────

rows = [json.loads(l) for l in runs_path.read_text(encoding="utf-8").splitlines() if l.strip()]
df = pd.DataFrame(rows)
df = df[df["model"] != "heuristic"]  # LLM runs only

PRESETS = ["balanced", "us", "eu"]

def split_condition(c):
    for p in PRESETS:
        if c.endswith("_" + p):
            return c[:-(len(p) + 1)], p
    return c, "balanced"

df[["condition_base", "preset"]] = pd.DataFrame(
    df["condition"].apply(split_condition).tolist(), index=df.index
)

CONDITION_LABELS = {
    "full_ecosystem":              "Full Ecosystem",
    "ablation_no_media":           "No Media",
    "ablation_no_incidents":       "No Incidents",
    "ablation_no_startups":        "No Startups",
    "ablation_no_opencore":        "No OpenCore",
    "ablation_single_benchmark":   "Single Benchmark",
    "ablation_no_funders":         "No Funders",
    "ablation_no_bench_evolution": "No Bench Evolution",
    "ablation_eval_as_company":    "Eval As Company",
}
COND_ORDER = list(CONDITION_LABELS.keys())
df["condition_label"] = df["condition_base"].map(CONDITION_LABELS).fillna(df["condition_base"])

METRICS = ["gaming_gap_final", "hhi_final", "mean_capability_final",
           "mean_safety_final", "benchmark_validity_final"]
METRIC_LABELS = {
    "gaming_gap_final":         "Gaming Gap",
    "hhi_final":                "HHI",
    "mean_capability_final":    "Capability",
    "mean_safety_final":        "Safety Inv.",
    "benchmark_validity_final": "BM Validity",
}

PATTERNS = [
    "pattern_score_inflation", "pattern_benchmark_turnover",
    "pattern_regulatory_escalation", "pattern_commoditization_shock",
    "pattern_safety_incident_response", "pattern_gaming_persistence",
    "pattern_funding_follows_scores",
]
PATTERN_LABELS = [
    "Score Infl.", "Bench Turn.", "Reg. Escal.", "Commoditiz.",
    "Safety Resp.", "Gaming Pers.", "Funding->Scores",
]

MODEL_COLORS = {
    "llama-70b":         "#6ACC65",
    "qwen-235b":         "#D65F5F",
    "claude-3.5-sonnet": "#B47CC7",
}
PRESET_COLORS = {"balanced": "#4878CF", "us": "#6ACC65", "eu": "#D65F5F"}

print(df.groupby(["phase", "model"]).size().to_string())


# ── 1. Cross-model metric distributions (full_ecosystem_balanced) ─────────────

fe = df[(df["condition"] == "full_ecosystem_balanced") & (df["model"] != "claude-3.5-sonnet")].copy()

fig, axes = plt.subplots(1, len(METRICS), figsize=(16, 4))
for ax, metric in zip(axes, METRICS):
    for model, grp in fe.groupby("model"):
        vals = grp[metric].dropna()
        color = MODEL_COLORS.get(model, "gray")
        if len(vals) == 1:
            ax.axvline(vals.iloc[0], label=model, color=color, linewidth=2, linestyle="--")
        elif len(vals) > 1:
            ax.hist(vals, bins=10, alpha=0.55, label=model, color=color, edgecolor="white", density=True)
    ax.set_title(METRIC_LABELS[metric], fontsize=10)
    ax.tick_params(labelsize=8)

axes[0].set_ylabel("Density")
handles, labels = axes[-1].get_legend_handles_labels()
seen = {}
[seen.update({l: h}) for h, l in zip(handles, labels)]
fig.legend(seen.values(), seen.keys(), loc="upper right", fontsize=9, ncol=2)
fig.suptitle("full_ecosystem_balanced \u2014 metric distributions by model", fontsize=12)
plt.tight_layout()
savefig("01_cross_model_distributions")



# ── 2. Cross-model summary table ──────────────────────────────────────────────

rows_out = []
for model in sorted(fe["model"].unique()):
    grp = fe[fe["model"] == model]
    row = {"model": model, "N": len(grp)}
    for m in METRICS:
        vals = grp[m].dropna()
        mu, sd = vals.mean(), vals.std()
        row[METRIC_LABELS[m]] = f"{mu:.3f}" + (f" \u00b1{sd:.3f}" if len(vals) > 1 else "")
    rows_out.append(row)

print("\nCross-model summary (full_ecosystem_balanced):")
print(pd.DataFrame(rows_out).set_index("model").to_string())


# ── 3. Pattern pass rates by model (full_ecosystem_balanced) ──────────────────

models_order = ["llama-70b", "qwen-235b", "claude-3.5-sonnet"]
models_present = [m for m in models_order if m in fe["model"].values]

rate_data = {}
for model in models_present:
    grp = fe[fe["model"] == model]
    rate_data[model] = [grp[p].mean() if p in grp.columns else np.nan for p in PATTERNS]

x = np.arange(len(PATTERNS))
width = 0.8 / len(models_present)

fig, ax = plt.subplots(figsize=(13, 4))
for i, model in enumerate(models_present):
    offset = (i - len(models_present) / 2 + 0.5) * width
    ax.bar(x + offset, rate_data[model], width, label=model,
           color=MODEL_COLORS.get(model, "gray"), alpha=0.8)

ax.set_xticks(x)
ax.set_xticklabels(PATTERN_LABELS, rotation=20, ha="right", fontsize=9)
ax.set_ylabel("Pass rate")
ax.set_ylim(0, 1.05)
ax.axhline(1.0, color="black", linewidth=0.5, linestyle=":")
ax.legend(fontsize=9)
ax.set_title("Pattern pass rates \u2014 full_ecosystem_balanced", fontsize=12)
plt.tight_layout()
savefig("02_pattern_pass_rates")



# ── 4. Ablation heatmap (llama-70b, balanced) ────────────────────────────────

llm_bal = df[(df["phase"] == "llm_core") & (df["model"] == "llama-70b") & (df["preset"] == "balanced")]

abl_means = (
    llm_bal.groupby("condition_base")[METRICS].mean()
    .reindex(COND_ORDER)
)
abl_means.index = [CONDITION_LABELS.get(c, c) for c in abl_means.index]
normed = (abl_means - abl_means.min()) / (abl_means.max() - abl_means.min() + 1e-9)

fig, ax = plt.subplots(figsize=(10, 5))
im = ax.imshow(normed.values, cmap="RdYlGn_r", aspect="auto", vmin=0, vmax=1)
ax.set_xticks(range(len(METRICS)))
ax.set_xticklabels([METRIC_LABELS[m] for m in METRICS], fontsize=10)
ax.set_yticks(range(len(abl_means)))
ax.set_yticklabels(abl_means.index, fontsize=10)
for i in range(len(abl_means)):
    for j in range(len(METRICS)):
        v = abl_means.values[i, j]
        if not np.isnan(v):
            ax.text(j, i, f"{v:.3f}", ha="center", va="center", fontsize=8)
ax.set_title("Ablation metrics \u2014 llama-70b, balanced preset", fontsize=12)
plt.colorbar(im, ax=ax, fraction=0.02, pad=0.02, label="Normalized value")
plt.tight_layout()
savefig("03_ablation_heatmap_llama_balanced")


print("\nAblation deltas vs Full Ecosystem (llama-70b, balanced):")
baseline = abl_means.loc["Full Ecosystem"]
deltas = abl_means.drop("Full Ecosystem") - baseline
deltas.columns = [METRIC_LABELS[m] for m in METRICS]
print(deltas.to_string(float_format=lambda x: f"{x:+.3f}"))


# ── 5. Ablation heatmap (qwen-235b, balanced) ────────────────────────────────

qwen_bal = df[(df["phase"] == "llm_core") & (df["model"] == "qwen-235b") & (df["preset"] == "balanced")]

abl_means_qwen = (
    qwen_bal.groupby("condition_base")[METRICS].mean()
    .reindex(COND_ORDER)
)
abl_means_qwen.index = [CONDITION_LABELS.get(c, c) for c in abl_means_qwen.index]
normed_qwen = (abl_means_qwen - abl_means_qwen.min()) / (abl_means_qwen.max() - abl_means_qwen.min() + 1e-9)

fig, ax = plt.subplots(figsize=(10, 5))
im = ax.imshow(normed_qwen.values, cmap="RdYlGn_r", aspect="auto", vmin=0, vmax=1)
ax.set_xticks(range(len(METRICS)))
ax.set_xticklabels([METRIC_LABELS[m] for m in METRICS], fontsize=10)
ax.set_yticks(range(len(abl_means_qwen)))
ax.set_yticklabels(abl_means_qwen.index, fontsize=10)
for i in range(len(abl_means_qwen)):
    for j in range(len(METRICS)):
        v = abl_means_qwen.values[i, j]
        if not np.isnan(v):
            ax.text(j, i, f"{v:.3f}", ha="center", va="center", fontsize=8)
ax.set_title("Ablation metrics \u2014 qwen-235b, balanced preset", fontsize=12)
plt.colorbar(im, ax=ax, fraction=0.02, pad=0.02, label="Normalized value")
plt.tight_layout()
savefig("04_ablation_heatmap_qwen_balanced")


print("\nAblation deltas vs Full Ecosystem (qwen-235b, balanced):")
baseline_qwen = abl_means_qwen.loc["Full Ecosystem"]
deltas_qwen = abl_means_qwen.drop("Full Ecosystem") - baseline_qwen
deltas_qwen.columns = [METRIC_LABELS[m] for m in METRICS]
print(deltas_qwen.to_string(float_format=lambda x: f"{x:+.3f}"))


# ── 6. Preset comparison — grouped bars per metric (was 5) ──────────────────

llm_all = df[df["phase"] == "llm_core"]

for metric in METRICS:
    preset_means = (
        llm_all.groupby(["condition_base", "preset"])[metric].mean()
        .unstack("preset").reindex(COND_ORDER)
    )
    preset_stds = (
        llm_all.groupby(["condition_base", "preset"])[metric].std()
        .unstack("preset").reindex(COND_ORDER)
    )
    labels = [CONDITION_LABELS.get(c, c) for c in preset_means.index]
    x = np.arange(len(labels))
    width = 0.25

    fig, ax = plt.subplots(figsize=(13, 4))
    for i, preset in enumerate(PRESETS):
        if preset not in preset_means.columns:
            continue
        offset = (i - 1) * width
        ax.bar(x + offset, preset_means[preset], width, yerr=preset_stds[preset],
               label=preset.upper(), color=PRESET_COLORS[preset], alpha=0.85,
               capsize=3, error_kw={"linewidth": 1})
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=9)
    ax.set_ylabel(METRIC_LABELS[metric])
    ax.legend(title="Preset")
    ax.set_title(f"{METRIC_LABELS[metric]} by condition and preset \u2014 llm_core", fontsize=11)
    plt.tight_layout()
    savefig(f"05_preset_bars_{metric}")
    


# ── 7. All metrics x preset — line overlay ───────────────────────────────────

fig, axes = plt.subplots(1, len(METRICS), figsize=(18, 4))
for ax, metric in zip(axes, METRICS):
    for preset in PRESETS:
        grp = llm_all[llm_all["preset"] == preset]
        means = grp.groupby("condition_base")[metric].mean().reindex(COND_ORDER)
        ax.plot(range(len(COND_ORDER)), means.values, marker="o", markersize=4,
                label=preset.upper(), color=PRESET_COLORS[preset], linewidth=1.5)
    ax.set_title(METRIC_LABELS[metric], fontsize=9)
    ax.set_xticks(range(len(COND_ORDER)))
    ax.set_xticklabels([CONDITION_LABELS.get(c, c) for c in COND_ORDER],
                       rotation=45, ha="right", fontsize=7)
    ax.tick_params(axis="y", labelsize=8)

axes[0].legend(title="Preset", fontsize=8)
fig.suptitle("All metrics by condition \u2014 llm_core, presets overlaid", fontsize=11)
plt.tight_layout()
savefig("06_preset_lines_all_metrics")



# ── 8. All models x balanced conditions — bar grid ───────────────────────────

all_models = ["llama-70b", "qwen-235b", "claude-3.5-sonnet"]
all_conds_balanced = [c + "_balanced" for c in COND_ORDER]

model_condition_means = {
    (model, cond): grp[METRICS].mean()
    for (model, cond), grp in df.groupby(["model", "condition"])
}

fig, axes = plt.subplots(len(METRICS), 1, figsize=(14, 14))
x = np.arange(len(all_conds_balanced))
width = 0.8 / len(all_models)

for ax, metric in zip(axes, METRICS):
    for i, model in enumerate(all_models):
        vals = [
            model_condition_means.get((model, c), pd.Series({metric: np.nan}))[metric]
            for c in all_conds_balanced
        ]
        offset = (i - len(all_models) / 2 + 0.5) * width
        ax.bar(x + offset, vals, width, label=model,
               color=MODEL_COLORS.get(model, "gray"), alpha=0.8)
    ax.set_ylabel(METRIC_LABELS[metric], fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels(
        [CONDITION_LABELS.get(c.replace("_balanced", ""), c) for c in all_conds_balanced],
        rotation=30, ha="right", fontsize=8,
    )
    ax.legend(fontsize=7, ncol=4)

fig.suptitle("All models \u00d7 balanced conditions \u2014 primary metrics", fontsize=12)
plt.tight_layout()
savefig("07_all_models_all_conditions")



# ── 9. Pattern heatmaps ───────────────────────────────────────────────────────

def pattern_heatmap(subset_df, title, figname):
    mat = np.full((len(COND_ORDER), len(PATTERNS)), np.nan)
    counts = np.zeros((len(COND_ORDER), len(PATTERNS)), dtype=int)
    for i, cbase in enumerate(COND_ORDER):
        grp = subset_df[subset_df["condition_base"] == cbase]
        for j, pat in enumerate(PATTERNS):
            if len(grp) > 0 and pat in grp.columns:
                mat[i, j] = grp[pat].mean()
                counts[i, j] = len(grp)

    fig, ax = plt.subplots(figsize=(12, 5))
    im = ax.imshow(mat, cmap="RdYlGn", aspect="auto", vmin=0, vmax=1)
    ax.set_xticks(range(len(PATTERNS)))
    ax.set_xticklabels(PATTERN_LABELS, rotation=25, ha="right", fontsize=9)
    ax.set_yticks(range(len(COND_ORDER)))
    ax.set_yticklabels([CONDITION_LABELS.get(c, c) for c in COND_ORDER], fontsize=9)
    for i in range(len(COND_ORDER)):
        for j in range(len(PATTERNS)):
            if not np.isnan(mat[i, j]):
                k = round(mat[i, j] * counts[i, j])
                ax.text(j, i, f"{k}/{counts[i,j]}", ha="center", va="center", fontsize=8)
    plt.colorbar(im, ax=ax, fraction=0.015, pad=0.02, label="Pass rate")
    ax.set_title(title, fontsize=11)
    plt.tight_layout()
    savefig(figname)
    


pattern_heatmap(
    df[(df["phase"] == "llm_core") & (df["model"] == "llama-70b")],
    "Pattern pass rates \u2014 llama-70b (all presets pooled)",
    "08_pattern_heatmap_llama",
)
pattern_heatmap(
    df[(df["phase"] == "llm_core") & (df["model"] == "qwen-235b")],
    "Pattern pass rates \u2014 qwen-235b (all presets pooled)",
    "09_pattern_heatmap_qwen",
)


# ── 10. llm_core metric distributions by model (all conditions pooled) ────────

all_plot_metrics = METRICS + ["role_adherence_violations"]
all_plot_labels = [METRIC_LABELS.get(m, m) for m in METRICS] + ["Role Adherence Violations"]

fig, axes = plt.subplots(2, 3, figsize=(14, 8))
for ax, metric, label in zip(axes.flatten(), all_plot_metrics, all_plot_labels):
    for model in [m for m in all_models if m != "claude-3.5-sonnet"]:
        vals = llm_all[llm_all["model"] == model][metric].dropna()
        if len(vals) == 0:
            continue
        color = MODEL_COLORS.get(model, "gray")
        if len(vals) == 1:
            ax.axvline(vals.iloc[0], label=model, color=color, linewidth=2, linestyle="--")
        else:
            ax.hist(vals, bins=15, alpha=0.55, label=model, color=color, edgecolor="white", density=True)
    ax.set_title(label)
    ax.set_ylabel("Density", fontsize=8)
    ax.legend(fontsize=7)
    ax.tick_params(labelsize=8)

fig.suptitle("llm_core metric distributions by model (all conditions pooled)", fontsize=12)
plt.tight_layout()
savefig("10_distributions_by_model")



# ── 11. llama-70b replications — full_ecosystem_balanced (N=30) ───────────────

llama_fe = df[
    (df["phase"] == "llm_core") &
    (df["model"] == "llama-70b") &
    (df["condition"] == "full_ecosystem_balanced")
]
print(f"\nllama-70b full_ecosystem_balanced: N={len(llama_fe)} seeds")

fig, axes = plt.subplots(1, len(METRICS), figsize=(16, 3))
for ax, metric in zip(axes, METRICS):
    vals = llama_fe[metric].dropna()
    ax.hist(vals, bins=12, color=MODEL_COLORS["llama-70b"], edgecolor="white", alpha=0.85, density=True)
    ax.axvline(vals.mean(), color="black", linestyle="--", linewidth=1.5,
               label=f"mean={vals.mean():.3f}")
    ax.set_title(METRIC_LABELS[metric], fontsize=9)
    ax.legend(fontsize=7)
    ax.tick_params(labelsize=8)

fig.suptitle("llama-70b replications \u2014 full_ecosystem_balanced (N=30)", fontsize=11)
plt.tight_layout()
savefig("11_llama_replications")


print("\nPattern pass rates (llama-70b, full_ecosystem_balanced):")
for p, pl in zip(PATTERNS, PATTERN_LABELS):
    rate = llama_fe[p].mean()
    k = round(rate * len(llama_fe))
    print(f"  {pl:25s}: {k}/{len(llama_fe)} ({rate:.0%})")


# ── Shared helpers for sections 12-14 ─────────────────────────────────────────

import math

def _t_crit(n):
    if n < 2:
        return 0.0
    try:
        from scipy.stats import t
        return float(t.ppf(0.975, df=n - 1))
    except ImportError:
        return 2.0

def ci_halfwidth(vals):
    vals = [v for v in vals if v == v]  # drop NaN
    n = len(vals)
    if n < 2:
        return 0.0
    return _t_crit(n) * (float(np.std(vals, ddof=1)) / math.sqrt(n))

# Load full df including heuristic for cross-phase comparisons
rows_all = [json.loads(l) for l in runs_path.read_text(encoding="utf-8").splitlines() if l.strip()]
df_all = pd.DataFrame(rows_all)
df_all[["condition_base", "preset"]] = pd.DataFrame(
    df_all["condition"].apply(split_condition).tolist(), index=df_all.index
)
df_all["condition_label"] = df_all["condition_base"].map(CONDITION_LABELS).fillna(df_all["condition_base"])

ALL_MODEL_COLORS = {**MODEL_COLORS, "heuristic": "#999999"}
ALL_MODEL_MARKERS = {"llama-70b": "o", "qwen-235b": "s", "heuristic": "^",
                     "claude-3.5-sonnet": "D"}


# ── 12. Gaming gap vs HHI scatter ─────────────────────────────────────────────

# One point per (model × condition_base), balanced preset, mean ± CI error bars
# Include heuristic baseline for reference
sources_12 = [
    (df_all[df_all["phase"] == "llm_core"],          ["llama-70b", "qwen-235b"]),
    (df_all[df_all["phase"] == "heuristic_baseline"], ["heuristic"]),
]

fig, ax = plt.subplots(figsize=(9, 6))

for src_df, models in sources_12:
    bal = src_df[src_df["preset"] == "balanced"]
    for model in models:
        mdf = bal[bal["model"] == model]
        for cond_base in COND_ORDER:
            grp = mdf[mdf["condition_base"] == cond_base]
            if len(grp) == 0:
                continue
            xvals = grp["hhi_final"].dropna().tolist()
            yvals = grp["gaming_gap_final"].dropna().tolist()
            if not xvals or not yvals:
                continue
            xm, ym = np.mean(xvals), np.mean(yvals)
            xe, ye = ci_halfwidth(xvals), ci_halfwidth(yvals)
            color  = ALL_MODEL_COLORS.get(model, "gray")
            marker = ALL_MODEL_MARKERS.get(model, "o")
            ax.errorbar(xm, ym, xerr=xe if xe > 0 else None,
                        yerr=ye if ye > 0 else None,
                        fmt=marker, color=color, markersize=7,
                        capsize=3, linewidth=1.2, alpha=0.85)
            # Label Full Ecosystem and notable outliers
            label_text = CONDITION_LABELS.get(cond_base, cond_base)
            if cond_base in ("full_ecosystem", "ablation_no_funders",
                             "ablation_single_benchmark", "ablation_no_opencore",
                             "ablation_eval_as_company"):
                ax.annotate(label_text, (xm, ym),
                            textcoords="offset points", xytext=(5, 4),
                            fontsize=7, color=color, alpha=0.9)

# Legend for models
for model, color in [("llama-70b", ALL_MODEL_COLORS["llama-70b"]),
                     ("qwen-235b", ALL_MODEL_COLORS["qwen-235b"]),
                     ("heuristic", ALL_MODEL_COLORS["heuristic"])]:
    ax.plot([], [], marker=ALL_MODEL_MARKERS[model], color=color,
            linestyle="none", label=model, markersize=7)

ax.set_xlabel("HHI (market concentration)", fontsize=10)
ax.set_ylabel("Gaming gap (score \u2212 true capability)", fontsize=10)
ax.set_title("Gaming gap vs market concentration \u2014 balanced preset, all conditions",
             fontsize=11)
ax.legend(fontsize=9)
ax.tick_params(labelsize=9)
plt.tight_layout()
savefig("12_gaming_gap_vs_hhi")


# ── 13. Variance decomposition ────────────────────────────────────────────────

# For each metric: decompose total variance into fraction explained by
# model, condition_base, and preset, with residual.
# Method: SS_factor = sum_g( n_g * (mean_g - grand_mean)^2 ) / SS_total

llm_df = df_all[df_all["phase"] == "llm_core"].copy()

fig, ax = plt.subplots(figsize=(9, 4))

factors      = ["model", "condition_base", "preset"]
factor_labels = ["Model", "Condition", "Preset"]
factor_colors = ["#4878CF", "#D65F5F", "#6ACC65"]
bar_bottom   = np.zeros(len(METRICS))

fracs_all = {f: [] for f in factors}
fracs_all["residual"] = []

for metric in METRICS:
    col = llm_df[metric].dropna()
    if len(col) < 2:
        for f in factors:
            fracs_all[f].append(0.0)
        fracs_all["residual"].append(1.0)
        continue
    grand_mean = col.mean()
    ss_total   = ((col - grand_mean) ** 2).sum()
    if ss_total == 0:
        for f in factors:
            fracs_all[f].append(0.0)
        fracs_all["residual"].append(1.0)
        continue
    ss_factors = {}
    for factor in factors:
        groups = llm_df.loc[col.index].groupby(factor)[metric]
        ss = sum(
            len(g) * (g.mean() - grand_mean) ** 2
            for _, g in groups if len(g) > 0
        )
        ss_factors[factor] = min(ss / ss_total, 1.0)
    total_explained = min(sum(ss_factors.values()), 1.0)
    residual = max(1.0 - total_explained, 0.0)
    for f in factors:
        fracs_all[f].append(ss_factors[f])
    fracs_all["residual"].append(residual)

x = np.arange(len(METRICS))
bottoms = np.zeros(len(METRICS))
for factor, label, color in zip(factors, factor_labels, factor_colors):
    vals = np.array(fracs_all[factor])
    ax.bar(x, vals, bottom=bottoms, label=label, color=color, alpha=0.85)
    bottoms += vals
ax.bar(x, np.array(fracs_all["residual"]), bottom=bottoms,
       label="Residual (seed noise)", color="#CCCCCC", alpha=0.85)

ax.set_xticks(x)
ax.set_xticklabels([METRIC_LABELS[m] for m in METRICS], fontsize=10)
ax.set_ylabel("Fraction of total variance", fontsize=10)
ax.set_ylim(0, 1.05)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
ax.set_title("Variance decomposition by factor \u2014 llm_core runs", fontsize=11)
ax.legend(fontsize=9, loc="upper right")
ax.tick_params(labelsize=9)
plt.tight_layout()
savefig("13_variance_decomposition")


# ── 14. Forest plot — ablation effect sizes on gaming gap ─────────────────────
#
# SE of delta uses actual within-condition SD where N > 1, otherwise falls
# back to a pooled SD estimated from full_ecosystem (which has N=30 for all
# three model sources).  Pooled assumption: within-condition variance is
# roughly equal across ablation conditions.
#
# SE(delta) = pooled_SD * sqrt(1/n_abl + 1/n_base)   [equal-variance two-sample]
# For N=1 ablation: SE(delta) = pooled_SD * sqrt(1 + 1/n_base)

ABLATIONS = [c for c in COND_ORDER if c != "full_ecosystem"]

forest_models = [
    ("llm_core",           "llama-70b",  ALL_MODEL_COLORS["llama-70b"],  "o"),
    ("llm_core",           "qwen-235b",  ALL_MODEL_COLORS["qwen-235b"],  "s"),
    ("heuristic_baseline", "heuristic",  ALL_MODEL_COLORS["heuristic"],  "^"),
]

fig, ax = plt.subplots(figsize=(9, 6))
y_positions = np.arange(len(ABLATIONS))
offsets = [-0.22, 0.0, 0.22]

for (phase, model, color, marker), offset in zip(forest_models, offsets):
    mdf = df_all[(df_all["phase"] == phase) & (df_all["model"] == model)]

    baseline_vals = mdf[mdf["condition"] == "full_ecosystem_balanced"]["gaming_gap_final"].dropna()
    if len(baseline_vals) == 0:
        continue
    baseline_mean = baseline_vals.mean()
    n_base        = len(baseline_vals)

    # Pooled SD: estimated from full_ecosystem_balanced (largest N available)
    pooled_sd = float(baseline_vals.std(ddof=1)) if n_base >= 2 else None

    for i, cond_base in enumerate(ABLATIONS):
        grp = mdf[(mdf["condition_base"] == cond_base) &
                  (mdf["preset"] == "balanced")]["gaming_gap_final"].dropna()
        if len(grp) == 0:
            continue

        n_abl = len(grp)
        delta = float(grp.mean()) - baseline_mean

        # SE of delta
        if n_abl >= 2:
            # Use actual within-condition variance for ablation, pooled for baseline
            se_abl  = float(grp.std(ddof=1)) / math.sqrt(n_abl)
            se_base = (pooled_sd / math.sqrt(n_base)) if pooled_sd else 0.0
            se_delta = math.sqrt(se_abl**2 + se_base**2)
        elif pooled_sd is not None:
            # N=1: use pooled SD for both terms
            se_delta = pooled_sd * math.sqrt(1.0/n_abl + 1.0/n_base)
        else:
            se_delta = 0.0

        tc = _t_crit(max(n_abl, n_base))
        hw = tc * se_delta

        y = y_positions[i] + offset
        ax.errorbar(delta, y,
                    xerr=hw if hw > 0 else None,
                    fmt=marker, color=color, markersize=7,
                    capsize=3, linewidth=1.2, alpha=0.9,
                    label=model if i == 0 else None)

ax.axvline(0, color="black", linewidth=0.9, linestyle="--", alpha=0.6)
ax.set_yticks(y_positions)
ax.set_yticklabels([CONDITION_LABELS[c] for c in ABLATIONS], fontsize=10)
ax.set_xlabel("$\Delta$ Gaming gap vs full ecosystem baseline (95% CI)", fontsize=10)
ax.set_title("Forest plot \u2014 ablation effect on gaming gap, balanced preset\n"
             "(CI from seed variance; N=1 conditions use pooled SD from full ecosystem)",
             fontsize=10)
ax.legend(fontsize=9)
ax.tick_params(labelsize=9)
ax.invert_yaxis()
plt.tight_layout()
savefig("14_forest_plot_gaming_gap")
