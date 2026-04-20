"""
Prototype three headline result figure options for the NeurIPS paper.

Option A: "Anatomy of Emergent Misalignment" — 3-panel narrative strip
  Panel A: Gap decomposition waterfall (aggregate across heuristic seeds)
  Panel B: Horizontal lollipop of ablation effects
  Panel C: LLM vs Heuristic leader portfolio scatter

Option B: "The Structural Invariant" — gap trajectory ribbon plot
  Heuristic ribbons (mean +/- p10/p90) for key conditions with LLM lines overlaid

Option C: "Dual Dashboard" — 2x2 structure vs. behavior
  Top-left: Volcano (compact)
  Top-right: Aggregate gap waterfall by condition
  Bottom-left: Pathway scatter (compact)
  Bottom-right: Incident response dot chart

Usage:
  python scripts/prototype_headline_figures.py
"""
import os
import sys
import csv
import warnings

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

# -- Project paths --
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))

HEURISTIC_SUMMARY = os.path.join(PROJECT_ROOT, "output", "heuristic_analysis", "heuristic_summary.csv")
LLM_SUMMARY = os.path.join(PROJECT_ROOT, "output", "llm_analysis", "llm_summary.csv")
LLM_OUTCOMES = os.path.join(PROJECT_ROOT, "output", "llm_analysis", "llm_outcome_typology.csv")
HEURISTIC_OUTCOMES = os.path.join(PROJECT_ROOT, "output", "heuristic_analysis", "outcome_typology.csv")
HEURISTIC_TRAJECTORIES = os.path.join(PROJECT_ROOT, "output", "heuristic_analysis", "trajectory_data")
LLM_TRAJECTORIES = os.path.join(PROJECT_ROOT, "output", "llm_analysis", "llm_trajectory_data")
LLM_INCIDENTS = os.path.join(PROJECT_ROOT, "output", "llm_analysis", "llm_incident_response.csv")
OUT_DIR = os.path.join(PROJECT_ROOT, "output", "headline_prototypes")
os.makedirs(OUT_DIR, exist_ok=True)

# -- Style --
try:
    from tueplots import bundles as _tueplots_bundles
    _NEURIPS_RC = _tueplots_bundles.neurips2024()
    _NEURIPS_RC.pop("figure.figsize", None)
    if os.environ.get("MPLLATEX", "1") != "0":
        _NEURIPS_RC["text.usetex"] = True
    matplotlib.rcParams.update(_NEURIPS_RC)
except ImportError:
    warnings.warn("tueplots not installed, using defaults")

INV_COLORS = {"rd": "#2E86AB", "safety": "#C73E1D", "product": "#A23B72"}


# =============================================================================
# Data loading helpers
# =============================================================================

def _read_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _f(val, default=0.0):
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def _tex(s):
    if not matplotlib.rcParams.get("text.usetex", False):
        return s
    for ch, esc in (("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"), ("_", r"\_")):
        s = s.replace(ch, esc)
    return s


def load_heuristic_balanced():
    rows = _read_csv(HEURISTIC_SUMMARY)
    return [r for r in rows if r["policy"] == "balanced"]


def load_llm_balanced():
    rows = _read_csv(LLM_SUMMARY)
    return [r for r in rows if r["policy"] == "balanced" and r["seed"] == "221"]


def load_trajectory(base_dir, filename):
    path = os.path.join(base_dir, filename)
    if not os.path.exists(path):
        return None
    return _read_csv(path)


NICE_NAMES = {
    "full_ecosystem": "Full ecosystem",
    "no_media": "No media",
    "no_funders": "No funders",
    "no_regulator": "No regulator",
    "no_opensource": "No open-source",
    "no_incidents": "No incidents",
    "no_product_channels": "No product ch.",
    "bm_orientation_max": "BM orient. max",
    "bm_orientation_adjustable": "BM orient. adj.",
    "dynamic_evaluator": "Dynamic eval.",
    "eval_as_company": "Eval-as-company",
    "aligned_benchmarks": "Aligned BMs",
    "fixed_market_size": "Fixed market",
    "homogeneous_consumers": "Homog. consumers",
    "initial_leader": "Initial leader",
    "initial_duopoly": "Initial duopoly",
    "initial_uniform": "Initial uniform",
    "static_enterprise_size": "Static enterprise size",
}


# =============================================================================
# OPTION A: 3-panel narrative strip
# =============================================================================

def option_a():
    print("Generating Option A: 3-panel narrative strip...")

    heur = load_heuristic_balanced()
    llm = load_llm_balanced()

    # -- Data for Panel A: Aggregate gap waterfall --
    baseline = [r for r in heur if r["condition"] == "full_ecosystem"][0]
    # Components for the baseline condition (averaged across 30 seeds)
    components = {
        "Score noise": _f(baseline["score_noise"]),
        "Dim. mismatch": _f(baseline["dim_mismatch"]),
        "Externalities": _f(baseline["penalty_load"]),
    }
    total_gap = _f(baseline["total_gap"])
    component_ses = {
        "Score noise": _f(baseline["score_noise_se"]),
        "Dim. mismatch": _f(baseline["dim_mismatch_se"]),
        "Externalities": _f(baseline["penalty_load_se"]),
    }

    # -- Data for Panel B: Lollipop ablation effects --
    baseline_gap = _f(baseline["total_gap"])
    ablation_data = []
    from scipy import stats
    for r in heur:
        cond = r["condition"]
        if cond == "full_ecosystem":
            continue
        delta = _f(r["total_gap"]) - baseline_gap
        # approximate p from CI width: se = (ci_hi - ci_lo) / (2*1.96)
        se_abl = _f(r["total_gap_se"])
        se_base = _f(baseline["total_gap_se"])
        se_diff = np.sqrt(se_abl**2 + se_base**2)
        if se_diff > 0:
            z = abs(delta) / se_diff
            p = 2 * (1 - stats.norm.cdf(z))
        else:
            p = 1.0
        ablation_data.append({
            "condition": cond,
            "delta": delta,
            "p": p,
            "sig": p < 0.05,
        })
    ablation_data.sort(key=lambda x: x["delta"])

    # -- Data for Panel C: Pathway scatter --
    llm_outcomes = _read_csv(LLM_OUTCOMES)
    llm_outcomes = [r for r in llm_outcomes if r["policy"] == "balanced" and r["seed"] == "221"]
    llm_by_cond = {r["condition"]: r for r in llm_outcomes}

    heur_outcomes = _read_csv(HEURISTIC_OUTCOMES)
    from collections import defaultdict
    heur_by_cond = defaultdict(list)
    for r in heur_outcomes:
        if r["policy"] == "balanced":
            heur_by_cond[r["condition"]].append(r)

    # -- Build figure --
    fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.4),
                             gridspec_kw={"width_ratios": [1.0, 1.5, 1.3]})

    # === Panel A: Waterfall ===
    ax = axes[0]
    labels = list(components.keys())
    vals = [components[k] for k in labels]
    ses = [component_ses[k] for k in labels]
    colors = ["#7EB5D6", "#D35F5F", "#9B8EC1"]

    bars = ax.bar(range(len(labels)), vals, color=colors, width=0.6,
                  edgecolor="white", linewidth=0.5)
    ax.errorbar(range(len(labels)), vals, yerr=[1.96*s for s in ses],
                fmt="none", ecolor="black", capsize=3, linewidth=0.8)

    # Total gap marker
    ax.axhline(total_gap, color="black", linewidth=0.8, linestyle="--", alpha=0.6)
    ax.text(len(labels)-0.5, total_gap + 0.0005,
            f"Total: {total_gap:.4f}", fontsize=6, ha="right", va="bottom")

    ax.axhline(0, color="grey", linewidth=0.5, alpha=0.5)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels([_tex(l) for l in labels], fontsize=6, rotation=25, ha="right")
    ax.set_ylabel("Gap component", fontsize=7)
    ax.set_title("A. Where the gap comes from", fontsize=8, fontweight="bold", loc="left")
    ax.tick_params(axis="y", labelsize=6)

    # === Panel B: Horizontal lollipop ===
    ax = axes[1]
    y_positions = range(len(ablation_data))
    for i, d in enumerate(ablation_data):
        color = "#D35F5F" if d["sig"] and d["delta"] > 0 else \
                "#5B8DB8" if d["sig"] and d["delta"] < 0 else "#AAAAAA"
        ax.plot([0, d["delta"]], [i, i], color=color, linewidth=1.0, alpha=0.7)
        ax.plot(d["delta"], i, "o", color=color, markersize=4, zorder=5)

    ax.axvline(0, color="grey", linewidth=0.5, alpha=0.5)
    ax.set_yticks(y_positions)
    ax.set_yticklabels([_tex(NICE_NAMES.get(d["condition"], d["condition"]))
                        for d in ablation_data], fontsize=5.5)
    ax.set_xlabel(r"$\Delta$ gap vs baseline", fontsize=7)
    ax.set_title("B. What moves the gap", fontsize=8, fontweight="bold", loc="left")
    ax.tick_params(axis="x", labelsize=6)

    # Add significance annotation for aligned_benchmarks
    for i, d in enumerate(ablation_data):
        if d["condition"] == "aligned_benchmarks":
            ax.annotate(f"$p<10^{{-10}}$", xy=(d["delta"], i),
                        xytext=(d["delta"]-0.005, i+1.2),
                        fontsize=5, ha="center",
                        arrowprops=dict(arrowstyle="-", lw=0.5, color="grey"))

    # === Panel C: Pathway scatter ===
    ax = axes[2]
    conditions = sorted(set(llm_by_cond.keys()) & set(heur_by_cond.keys()))

    for c in conditions:
        l = llm_by_cond[c]
        l_rd = _f(l["leader_rd"])
        l_sa = _f(l["leader_safety"])

        h_rds = [_f(r["leader_rd"]) for r in heur_by_cond[c]]
        h_sas = [_f(r["leader_safety"]) for r in heur_by_cond[c]]
        h_rd = sum(h_rds) / len(h_rds)
        h_sa = sum(h_sas) / len(h_sas)

        ax.plot([h_rd, l_rd], [h_sa, l_sa], color="grey", linewidth=0.4, alpha=0.5, zorder=1)
        ax.plot(h_rd, h_sa, "o", color="#457B9D", markersize=4, markerfacecolor="none",
                markeredgewidth=0.8, zorder=3)
        ax.plot(l_rd, l_sa, "o", color="#C73E1D", markersize=4, zorder=3)

    # Simplex boundary
    ax.fill([0, 1, 0, 0], [0, 0, 1, 0], color="#f0f0f0", alpha=0.3, zorder=0)
    ax.plot([0, 1], [1, 0], color="grey", linewidth=0.5, alpha=0.3, zorder=0)

    ax.set_xlim(-0.02, 0.75)
    ax.set_ylim(-0.02, 0.58)
    ax.set_xlabel("Leader R\\&D alloc." if matplotlib.rcParams.get("text.usetex") else "Leader R&D alloc.", fontsize=7)
    ax.set_ylabel("Leader safety alloc.", fontsize=7)
    ax.set_title("C. How reasoning responds", fontsize=8, fontweight="bold", loc="left")
    ax.tick_params(axis="both", labelsize=6)

    h_handle = mlines.Line2D([], [], color="#457B9D", marker="o", markersize=4,
                              markerfacecolor="none", markeredgewidth=0.8, linestyle="None",
                              label="Heuristic")
    l_handle = mlines.Line2D([], [], color="#C73E1D", marker="o", markersize=4,
                              linestyle="None", label="LLM")
    ax.legend(handles=[h_handle, l_handle], fontsize=5.5, loc="upper right",
              frameon=True, framealpha=0.9)

    fig.tight_layout(w_pad=1.5)
    out = os.path.join(OUT_DIR, "option_a_narrative_strip.pdf")
    fig.savefig(out, bbox_inches="tight", dpi=200)
    print(f"  Saved: {out}")
    # Also save PNG for quick viewing
    fig.savefig(out.replace(".pdf", ".png"), bbox_inches="tight", dpi=200)
    plt.close(fig)


# =============================================================================
# OPTION B: Gap trajectory ribbon plot
# =============================================================================

def option_b():
    print("Generating Option B: trajectory ribbon plot...")

    KEY_CONDITIONS = [
        ("full_ecosystem", "#2A9D8F", "Full ecosystem"),
        ("aligned_benchmarks", "#E63946", "Aligned benchmarks"),
        ("no_regulator", "#457B9D", "No regulator"),
        ("no_incidents", "#6A4C93", "No incidents"),
        ("homogeneous_consumers", "#E9C46A", "Homog. consumers"),
    ]

    fig, ax = plt.subplots(figsize=(5.5, 3.0))

    for cond, color, label in KEY_CONDITIONS:
        # Heuristic ribbon
        traj_file = f"{cond}_balanced.csv"
        traj = load_trajectory(HEURISTIC_TRAJECTORIES, traj_file)
        if not traj:
            print(f"  Skipping {cond}: no heuristic trajectory")
            continue

        rounds_h = [_f(r["round"]) for r in traj]
        gap_mean = [_f(r["gap_mean"]) for r in traj]
        gap_p10 = [_f(r["gap_p10"]) for r in traj]
        gap_p90 = [_f(r["gap_p90"]) for r in traj]

        ax.fill_between(rounds_h, gap_p10, gap_p90, color=color, alpha=0.12)
        ax.plot(rounds_h, gap_mean, color=color, linewidth=1.2, label=_tex(label))

        # LLM overlay (single seed)
        llm_file = f"{cond}_balanced_seed221.csv"
        llm_traj = load_trajectory(LLM_TRAJECTORIES, llm_file)
        if llm_traj:
            rounds_l = [_f(r["round"]) for r in llm_traj]
            gap_l = [_f(r["gap"]) for r in llm_traj]
            ax.plot(rounds_l, gap_l, color=color, linewidth=0.7, linestyle="--", alpha=0.7)

    ax.axhline(0, color="grey", linewidth=0.5, alpha=0.5)
    ax.set_xlabel("Round", fontsize=8)
    ax.set_ylabel("Score $-$ satisfaction gap", fontsize=8)
    ax.set_title("Gap trajectories: heuristic ribbons (p10--p90) with LLM overlays (dashed)",
                 fontsize=7, loc="left")
    ax.tick_params(axis="both", labelsize=7)
    ax.legend(fontsize=6, loc="upper right", frameon=True, framealpha=0.9, ncol=2)

    # Annotation: the aligned_benchmarks band is in a completely different range
    # Add a text callout
    ax.annotate("Aligned BMs:\nonly condition\nwith positive gap",
                xy=(20, 0.015), fontsize=5.5,
                color="#E63946", fontstyle="italic",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#E63946",
                          alpha=0.8, linewidth=0.5))

    fig.tight_layout()
    out = os.path.join(OUT_DIR, "option_b_trajectory_ribbon.pdf")
    fig.savefig(out, bbox_inches="tight", dpi=200)
    fig.savefig(out.replace(".pdf", ".png"), bbox_inches="tight", dpi=200)
    print(f"  Saved: {out}")
    plt.close(fig)


# =============================================================================
# OPTION C: 2x2 dual dashboard
# =============================================================================

def option_c():
    print("Generating Option C: 2x2 dual dashboard...")

    heur = load_heuristic_balanced()
    llm = load_llm_balanced()
    baseline = [r for r in heur if r["condition"] == "full_ecosystem"][0]
    baseline_gap = _f(baseline["total_gap"])

    # Load pathway scatter data
    llm_outcomes = _read_csv(LLM_OUTCOMES)
    llm_outcomes = [r for r in llm_outcomes if r["policy"] == "balanced" and r["seed"] == "221"]
    llm_by_cond = {r["condition"]: r for r in llm_outcomes}

    from collections import defaultdict
    heur_outcomes = _read_csv(HEURISTIC_OUTCOMES)
    heur_by_cond = defaultdict(list)
    for r in heur_outcomes:
        if r["policy"] == "balanced":
            heur_by_cond[r["condition"]].append(r)

    fig, axes = plt.subplots(2, 2, figsize=(5.5, 4.5))

    # === Top-left: Compact volcano ===
    ax = axes[0, 0]
    from scipy import stats

    for r in heur:
        cond = r["condition"]
        if cond == "full_ecosystem":
            continue
        delta = _f(r["total_gap"]) - baseline_gap
        se_abl = _f(r["total_gap_se"])
        se_base = _f(baseline["total_gap_se"])
        se_diff = np.sqrt(se_abl**2 + se_base**2)
        if se_diff > 0:
            z = abs(delta) / se_diff
            p = max(2 * (1 - stats.norm.cdf(z)), 1e-11)
        else:
            p = 1.0
        neg_log_p = -np.log10(p)
        sig = p < 0.05

        color = "#D35F5F" if sig and delta > 0 else \
                "#5B8DB8" if sig and delta < 0 else "#AAAAAA"
        ax.plot(delta, neg_log_p, "o", color=color, markersize=4, zorder=3)

        if sig:
            label = NICE_NAMES.get(cond, cond)
            offset = (5, 5) if delta > 0 else (-5, 5)
            ax.annotate(_tex(label), xy=(delta, neg_log_p), xytext=offset,
                        textcoords="offset points", fontsize=4.5, color=color,
                        ha="left" if delta > 0 else "right")

    ax.axhline(-np.log10(0.05), color="grey", linewidth=0.5, linestyle="--", alpha=0.5)
    ax.axvline(0, color="grey", linewidth=0.5, alpha=0.5)
    ax.set_xlabel(r"$\Delta$ gap vs baseline", fontsize=6)
    ax.set_ylabel(r"$-\log_{10}(p)$", fontsize=6)
    ax.set_title("A. Structure: ablation effects", fontsize=7, fontweight="bold", loc="left")
    ax.tick_params(axis="both", labelsize=5)

    # === Top-right: Stacked gap waterfall by condition ===
    ax = axes[0, 1]

    # Sort by total_gap for visual clarity
    conditions_sorted = sorted(heur, key=lambda r: _f(r["total_gap"]))
    cond_labels = [NICE_NAMES.get(r["condition"], r["condition"]) for r in conditions_sorted]
    noise_vals = [_f(r["score_noise"]) for r in conditions_sorted]
    mismatch_vals = [_f(r["dim_mismatch"]) for r in conditions_sorted]
    extern_vals = [_f(r["penalty_load"]) for r in conditions_sorted]

    x = np.arange(len(cond_labels))

    # Stacked horizontal bars
    ax.barh(x, noise_vals, height=0.6, color="#7EB5D6", label="Score noise", zorder=2)
    ax.barh(x, mismatch_vals, height=0.6, left=noise_vals, color="#D35F5F",
            label="Dim. mismatch", zorder=2)
    lefts = [n + m for n, m in zip(noise_vals, mismatch_vals)]
    ax.barh(x, extern_vals, height=0.6, left=lefts, color="#9B8EC1",
            label="Externalities", zorder=2)

    # Total gap markers
    total_gaps = [_f(r["total_gap"]) for r in conditions_sorted]
    ax.plot(total_gaps, x, "k|", markersize=6, zorder=5, alpha=0.7)

    ax.axvline(0, color="grey", linewidth=0.5, alpha=0.5)
    ax.set_yticks(x)
    ax.set_yticklabels([_tex(l) for l in cond_labels], fontsize=4.5)
    ax.set_xlabel("Gap decomposition", fontsize=6)
    ax.set_title("B. Structure: gap anatomy", fontsize=7, fontweight="bold", loc="left")
    ax.tick_params(axis="x", labelsize=5)
    ax.legend(fontsize=4.5, loc="lower right", frameon=True, framealpha=0.9)

    # === Bottom-left: Compact pathway scatter ===
    ax = axes[1, 0]
    conditions = sorted(set(llm_by_cond.keys()) & set(heur_by_cond.keys()))

    for c in conditions:
        l = llm_by_cond[c]
        l_rd = _f(l["leader_rd"])
        l_sa = _f(l["leader_safety"])

        h_rds = [_f(r["leader_rd"]) for r in heur_by_cond[c]]
        h_sas = [_f(r["leader_safety"]) for r in heur_by_cond[c]]
        h_rd = sum(h_rds) / len(h_rds)
        h_sa = sum(h_sas) / len(h_sas)

        ax.plot([h_rd, l_rd], [h_sa, l_sa], color="grey", linewidth=0.4, alpha=0.5, zorder=1)
        ax.plot(h_rd, h_sa, "o", color="#457B9D", markersize=3.5, markerfacecolor="none",
                markeredgewidth=0.7, zorder=3)
        ax.plot(l_rd, l_sa, "o", color="#C73E1D", markersize=3.5, zorder=3)

    ax.fill([0, 1, 0, 0], [0, 0, 1, 0], color="#f0f0f0", alpha=0.3, zorder=0)
    ax.plot([0, 1], [1, 0], color="grey", linewidth=0.5, alpha=0.3, zorder=0)
    ax.set_xlim(-0.02, 0.75)
    ax.set_ylim(-0.02, 0.58)
    ax.set_xlabel("Leader R\\&D alloc." if matplotlib.rcParams.get("text.usetex") else "Leader R&D alloc.", fontsize=6)
    ax.set_ylabel("Leader safety alloc.", fontsize=6)
    ax.set_title("C. Behavior: portfolio shift", fontsize=7, fontweight="bold", loc="left")
    ax.tick_params(axis="both", labelsize=5)

    h_handle = mlines.Line2D([], [], color="#457B9D", marker="o", markersize=3.5,
                              markerfacecolor="none", markeredgewidth=0.7, linestyle="None",
                              label="Heuristic")
    l_handle = mlines.Line2D([], [], color="#C73E1D", marker="o", markersize=3.5,
                              linestyle="None", label="LLM")
    ax.legend(handles=[h_handle, l_handle], fontsize=5, loc="upper right",
              frameon=True, framealpha=0.9)

    # === Bottom-right: Incident response dot chart ===
    ax = axes[1, 1]

    # Load incident response data
    if os.path.exists(LLM_INCIDENTS):
        inc_rows = _read_csv(LLM_INCIDENTS)
        # Aggregate by condition
        from collections import Counter
        cond_hits = Counter()
        cond_total = Counter()
        for r in inc_rows:
            cond = r.get("condition", "")
            if not cond or r.get("policy", "") != "balanced":
                continue
            cond_total[cond] += 1
            if r.get("safety_increased", "").lower() in ("true", "1", "yes"):
                cond_hits[cond] += 1

        inc_conditions = sorted(cond_total.keys())
        y_pos = range(len(inc_conditions))
        rates = []
        ci_los = []
        ci_his = []
        for c in inc_conditions:
            n = cond_total[c]
            k = cond_hits[c]
            rate = k / n if n > 0 else 0
            rates.append(rate)
            # Wilson interval
            z = 1.96
            denom = 1 + z**2 / n
            center = (rate + z**2 / (2*n)) / denom
            margin = z * np.sqrt((rate*(1-rate)/n + z**2/(4*n**2))) / denom
            ci_los.append(max(0, center - margin))
            ci_his.append(min(1, center + margin))

        for i, c in enumerate(inc_conditions):
            color = "#D35F5F" if rates[i] < 0.5 else "#2A9D8F"
            ax.plot(rates[i], i, "o", color=color, markersize=4, zorder=5)
            ax.plot([ci_los[i], ci_his[i]], [i, i], color=color, linewidth=1.0, alpha=0.5)

        ax.axvline(0.5, color="grey", linewidth=0.5, linestyle="--", alpha=0.5)
        ax.axvline(0.79, color="#2A9D8F", linewidth=0.5, linestyle=":", alpha=0.5,
                   label=f"Mean: 79\\%" if matplotlib.rcParams.get("text.usetex") else "Mean: 79%")
        ax.set_yticks(y_pos)
        ax.set_yticklabels([_tex(NICE_NAMES.get(c, c)) for c in inc_conditions], fontsize=4.5)
        ax.set_xlabel("Safety response rate", fontsize=6)
        ax.set_xlim(-0.05, 1.05)
        ax.legend(fontsize=5, loc="lower left", frameon=True, framealpha=0.9)
    else:
        ax.text(0.5, 0.5, "Incident data\nnot found", transform=ax.transAxes,
                ha="center", va="center", fontsize=8, color="grey")

    ax.set_title("D. Behavior: incident response", fontsize=7, fontweight="bold", loc="left")
    ax.tick_params(axis="both", labelsize=5)

    fig.tight_layout(h_pad=1.5, w_pad=1.2)
    out = os.path.join(OUT_DIR, "option_c_dual_dashboard.pdf")
    fig.savefig(out, bbox_inches="tight", dpi=200)
    fig.savefig(out.replace(".pdf", ".png"), bbox_inches="tight", dpi=200)
    print(f"  Saved: {out}")
    plt.close(fig)


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    option_a()
    option_b()
    option_c()
    print(f"\nAll prototypes saved to: {OUT_DIR}")
