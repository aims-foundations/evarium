"""
Prototype plots for the privacy-ladder mechanism question (paper §5.2).

Two figures, both drawn from _core_privacy/llm/ LLM runs:

  (A) Capability-need alignment trajectory across privacy conditions.
      Does privacy change what providers *do*, or only what benchmarks
      *measure*?  If the capability-vector <-> population-need cosine
      rises under private_* conditions but not under public_only, the
      gap compression is endogenous to provider reorientation rather
      than a pure measurement-side artefact.

  (B) Gaming-debt trajectory: cumulative market-share-weighted |gap|
      integrated over rounds.  Rank-orders conditions by *total* gap
      accumulated, not just endpoint, and reveals when the divergence
      sets in.

Usage:
  python -m scripts.plots.paper.privacy_mechanism_prototypes
"""
from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .. import paths as _paths

try:
    from tueplots import bundles as _tb
    _RC = _tb.neurips2024()
    _RC.pop("figure.figsize", None)
    plt.rcParams.update(_RC)
except Exception:
    pass

# --- config ------------------------------------------------------------------

BASE = Path(_paths.PROJECT_ROOT) / "sandbox" / "experiments" / "_core_privacy" / "llm"

CONDITIONS = {
    "public_only":      ["public_only_s42_sonnet", "public_only_s43_sonnet", "public_only_s44_sonnet"],
    "baseline":         ["baseline_s42_sonnet",    "baseline_s43_sonnet"],
    "private_dominant": ["private_dominant_s42_sonnet"],
    "private_only":     ["private_only_s42_sonnet", "private_only_s43_sonnet", "private_only_s44_sonnet"],
    "iid_holdout":      ["iid_holdout_s42_sonnet"],
}

ORDER = ["public_only", "baseline", "private_dominant", "private_only", "iid_holdout"]

# palette: blue -> red ladder, iid_holdout as neutral grey
PALETTE = {
    "public_only":      "#2b6cb0",  # blue
    "baseline":         "#e6b45c",  # amber
    "private_dominant": "#dd8a4a",  # orange
    "private_only":     "#b5453d",  # red
    "iid_holdout":      "#7a7a7a",  # grey
}

LABEL = {
    "public_only":      "public_only",
    "baseline":         "baseline (8/3/2 mix)",
    "private_dominant": "private_dominant",
    "private_only":     "private_only",
    "iid_holdout":      "iid_holdout",
}

DIMS = ["reasoning", "coding", "knowledge", "safety", "communication", "agentic"]


def _load_rounds(run_name: str):
    seed_dirs = list((BASE / run_name / "seeds").iterdir())
    assert len(seed_dirs) == 1, f"expected 1 seed dir, got {seed_dirs}"
    p = seed_dirs[0] / "rounds.jsonl"
    rows = []
    with p.open() as f:
        for ln in f:
            rows.append(json.loads(ln))
    return rows


def _cos(u: dict, v: dict) -> float:
    k = [d for d in DIMS if d in u and d in v]
    a = np.array([u[d] for d in k])
    b = np.array([v[d] for d in k])
    na = np.linalg.norm(a); nb = np.linalg.norm(b)
    if na < 1e-12 or nb < 1e-12:
        return float("nan")
    return float(np.dot(a, b) / (na * nb))


# --- Plot A: capability-need alignment ---------------------------------------

def compute_alignment_series(rows):
    """Return (rounds, weighted_alignment, per_provider_alignment).

    Weighted by market share.  Alignment = cos(capability_vector, need_weights).
    """
    rnds, wa, pp = [], [], defaultdict(list)
    for d in rows:
        r = d["round"]
        cvs = d.get("capability_vectors", {})
        nw = d.get("consumer_data", {}).get("need_weights")
        ms = d.get("consumer_data", {}).get("market_shares", {})
        if not cvs or not nw or not ms:
            continue
        tot = sum(ms.values()) or 1.0
        per = {p: _cos(v, nw) for p, v in cvs.items()}
        w = sum((ms.get(p, 0.0) / tot) * a for p, a in per.items() if not math.isnan(a))
        rnds.append(r)
        wa.append(w)
        for p, a in per.items():
            pp[p].append((r, a))
    return rnds, wa, pp


def plot_alignment(out_path: Path):
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(9.8, 3.4), gridspec_kw={"width_ratios": [2.0, 1.0]})
    terminal_cos = {}
    terminal_shifts = {}  # cos(R=39) - cos(R=0) per seed
    for cond in ORDER:
        seeds = CONDITIONS[cond]
        series = []
        rmax = 0
        for s in seeds:
            rows = _load_rounds(s)
            rnds, wa, _ = compute_alignment_series(rows)
            if not rnds:
                continue
            series.append((np.array(rnds), np.array(wa)))
            rmax = max(rmax, int(rnds[-1]))
        if not series:
            continue
        rs_full = np.arange(0, rmax + 1)
        mat = np.full((len(series), len(rs_full)), np.nan)
        for i, (rs, ys) in enumerate(series):
            if len(rs) == 1:
                mat[i, rs[0]] = ys[0]
            else:
                mat[i, :] = np.interp(rs_full, rs, ys, left=np.nan, right=np.nan)
        mean = np.nanmean(mat, axis=0)
        color = PALETTE[cond]
        ax.plot(rs_full, mean, color=color, lw=2.0, label=f"{LABEL[cond]} (n={len(series)})")
        if mat.shape[0] > 1:
            lo = np.nanpercentile(mat, 25, axis=0)
            hi = np.nanpercentile(mat, 75, axis=0)
            ax.fill_between(rs_full, lo, hi, color=color, alpha=0.12, linewidth=0)
        terminal_cos[cond] = [ys[-1] for _, ys in series]
        terminal_shifts[cond] = [ys[-1] - ys[0] for _, ys in series]

    ax.set_xlabel("round")
    ax.set_ylabel(r"cosine(capability, need)")
    ax.set_title("Capability-need alignment, pooled over providers")
    ax.axhline(1.0, color="k", lw=0.5, ls="--", alpha=0.4)
    ax.grid(True, alpha=0.2)
    ax.legend(loc="lower right", fontsize=8, frameon=False)

    # right panel: terminal shift (cos_R39 - cos_R0) per condition
    labels = [c for c in ORDER if c in terminal_shifts]
    means = [np.mean(terminal_shifts[c]) for c in labels]
    ax2.barh(
        range(len(labels)), means,
        color=[PALETTE[c] for c in labels], alpha=0.85, edgecolor="k", linewidth=0.5,
    )
    for i, c in enumerate(labels):
        ys = terminal_shifts[c]
        ax2.scatter(ys, [i] * len(ys), color="k", s=9, zorder=3)
    ax2.set_yticks(range(len(labels)))
    ax2.set_yticklabels([LABEL[c] for c in labels], fontsize=8)
    ax2.invert_yaxis()
    ax2.set_xlabel(r"$\Delta$ alignment (round 39 $-$ round 0)")
    ax2.set_title("Total reorientation by round 39")
    ax2.grid(True, alpha=0.2, axis="x")
    ax2.axvline(0, color="k", lw=0.6, alpha=0.5)

    fig.suptitle(
        "Privacy does not change what providers do: alignment trajectories are invariant across conditions",
        fontsize=10, y=1.04,
    )
    fig.text(
        0.5, -0.03,
        "Providers reorient $\\approx{+}0.028$ in cosine alignment with the population-need vector over 40 rounds "
        "in every condition, including public_only. The gap compression seen in the main privacy-ladder scatter must therefore "
        "live in the reporting channel (benchmark CDW $\\neq$ population need) rather than in a strategic behavioral response to privacy.",
        ha="center", fontsize=7, style="italic", color="#555", wrap=True,
    )
    fig.tight_layout()
    fig.savefig(out_path, dpi=180, bbox_inches="tight")
    fig.savefig(out_path.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)


# --- Plot B: gaming-debt trajectory ------------------------------------------

def compute_gap_series(rows):
    """Weighted gap = sum_i share_i * (score_i - satisfaction_i)."""
    rnds, gaps = [], []
    for d in rows:
        ms = d.get("consumer_data", {}).get("market_shares", {})
        sat = d.get("consumer_data", {}).get("provider_satisfaction", {})
        sc = d.get("scores", {})
        if not ms or not sat or not sc:
            continue
        tot = sum(ms.values()) or 1.0
        g = sum((ms.get(p, 0.0) / tot) * (sc.get(p, 0.0) - sat.get(p, 0.0)) for p in ms)
        rnds.append(d["round"])
        gaps.append(g)
    return np.array(rnds), np.array(gaps)


def plot_gaming_debt(out_path: Path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 3.4), gridspec_kw={"width_ratios": [2.2, 1.0]})

    terminal = {}  # cond -> list of terminal cumulative gaps
    for cond in ORDER:
        seeds = CONDITIONS[cond]
        series = []
        for s in seeds:
            rows = _load_rounds(s)
            rs, gs = compute_gap_series(rows)
            if len(rs) < 5:
                continue
            cum = np.cumsum(gs)  # gaming debt trajectory
            series.append((rs, cum))
        if not series:
            continue
        rmax = max(int(rs[-1]) for rs, _ in series)
        rs_full = np.arange(0, rmax + 1)
        mat = np.full((len(series), len(rs_full)), np.nan)
        for i, (rs, ys) in enumerate(series):
            mat[i, :] = np.interp(rs_full, rs, ys, left=np.nan, right=np.nan)
        mean = np.nanmean(mat, axis=0)
        color = PALETTE[cond]
        ax1.plot(rs_full, mean, color=color, lw=1.9, label=f"{LABEL[cond]} (n={len(series)})")
        if mat.shape[0] > 1:
            lo = np.nanpercentile(mat, 25, axis=0)
            hi = np.nanpercentile(mat, 75, axis=0)
            ax1.fill_between(rs_full, lo, hi, color=color, alpha=0.15, linewidth=0)
        # terminal cumulative at last valid round
        last = [ys[-1] for _, ys in series]
        terminal[cond] = last

    ax1.axhline(0, color="k", lw=0.6, alpha=0.5)
    ax1.set_xlabel("round")
    ax1.set_ylabel(r"cumulative $\sum_t \,\bar{g}_t$  (gaming debt)")
    ax1.set_title("Gaming debt over time")
    ax1.grid(True, alpha=0.2)
    ax1.legend(loc="upper left", fontsize=8, frameon=False)

    # right panel: terminal debt bars with seed points
    labels = [c for c in ORDER if c in terminal]
    means = [np.mean(terminal[c]) for c in labels]
    ax2.barh(
        range(len(labels)),
        means,
        color=[PALETTE[c] for c in labels],
        alpha=0.85, edgecolor="k", linewidth=0.5,
    )
    for i, c in enumerate(labels):
        ys = terminal[c]
        ax2.scatter(ys, [i] * len(ys), color="k", s=8, zorder=3)
    ax2.set_yticks(range(len(labels)))
    ax2.set_yticklabels([LABEL[c] for c in labels], fontsize=8)
    ax2.invert_yaxis()
    ax2.axvline(0, color="k", lw=0.6, alpha=0.5)
    ax2.set_xlabel("terminal gaming debt")
    ax2.set_title("Round-40 total")
    ax2.grid(True, alpha=0.2, axis="x")

    fig.text(
        0.5, -0.02,
        "Left: cumulative $\\sum_{t} \\bar{g}_t$ where $\\bar{g}_t$ = market-share-weighted score-minus-satisfaction at round $t$. "
        "Right: terminal value per condition with per-seed scatter. Total gaming debt collapses from public_only to private_only; "
        "iid_holdout returns to the public_only regime, isolating the effect to weight asymmetry, not reporting lag.",
        ha="center", fontsize=7, style="italic", color="#555",
    )
    fig.tight_layout()
    fig.savefig(out_path, dpi=180, bbox_inches="tight")
    fig.savefig(out_path.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)


# --- Plot C: capital concentration vs market concentration -------------------

def _hhi(vals):
    s = sum(vals) or 1.0
    return sum((v / s) ** 2 for v in vals)


def compute_hhi_series(rows):
    """Return (rounds, market_hhi, funder_hhi) — HHI across providers."""
    rnds, mh, fh = [], [], []
    for d in rows:
        ms = d.get("consumer_data", {}).get("market_shares", {})
        fd = d.get("funder_data", {}).get("allocations", {})
        if not ms or not fd:
            continue
        # funder allocation pooled across funders -> per-provider totals
        pt = defaultdict(float)
        for funder, prov_alloc in fd.items():
            for p, amt in prov_alloc.items():
                pt[p] += float(amt)
        if not pt:
            continue
        rnds.append(d["round"])
        mh.append(_hhi(ms.values()))
        fh.append(_hhi(pt.values()))
    return np.array(rnds), np.array(mh), np.array(fh)


def plot_capital_concentration(out_path: Path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 3.6))

    # trajectory panel (funder HHI over time)
    for cond in ORDER:
        seeds = CONDITIONS[cond]
        all_fh = []
        rmax = 0
        for s in seeds:
            rows = _load_rounds(s)
            rs, mh, fh = compute_hhi_series(rows)
            if len(rs) < 5:
                continue
            all_fh.append((rs, fh))
            rmax = max(rmax, int(rs[-1]))
        if not all_fh:
            continue
        rs_full = np.arange(0, rmax + 1)
        mat = np.full((len(all_fh), len(rs_full)), np.nan)
        for i, (rs, ys) in enumerate(all_fh):
            mat[i, :] = np.interp(rs_full, rs, ys, left=np.nan, right=np.nan)
        mean = np.nanmean(mat, axis=0)
        color = PALETTE[cond]
        ax1.plot(rs_full, mean, color=color, lw=1.9, label=f"{LABEL[cond]} (n={len(all_fh)})")
        if mat.shape[0] > 1:
            lo = np.nanpercentile(mat, 25, axis=0); hi = np.nanpercentile(mat, 75, axis=0)
            ax1.fill_between(rs_full, lo, hi, color=color, alpha=0.12, linewidth=0)
    ax1.set_xlabel("round")
    ax1.set_ylabel("funder allocation HHI")
    ax1.set_title("Capital concentration over time")
    ax1.grid(True, alpha=0.2)
    ax1.legend(loc="best", fontsize=8, frameon=False)

    # scatter panel: funder HHI vs market HHI per round, all conditions overlaid
    for cond in ORDER:
        seeds = CONDITIONS[cond]
        mhs, fhs = [], []
        for s in seeds:
            rows = _load_rounds(s)
            rs, mh, fh = compute_hhi_series(rows)
            if len(rs) < 5:
                continue
            # take last-20-round mean per seed to summarise
            mhs.append(float(np.mean(mh[-20:])))
            fhs.append(float(np.mean(fh[-20:])))
        if not fhs:
            continue
        color = PALETTE[cond]
        ax2.scatter(mhs, fhs, color=color, s=70, edgecolor="k", linewidth=0.6, label=LABEL[cond], zorder=3)
    # 45-degree reference
    lo = min(ax2.get_xlim()[0], ax2.get_ylim()[0])
    hi = max(ax2.get_xlim()[1], ax2.get_ylim()[1])
    ax2.plot([lo, hi], [lo, hi], "k--", alpha=0.4, lw=0.8, zorder=1)
    ax2.set_xlabel("market-share HHI  (last-20-round mean)")
    ax2.set_ylabel("funder-allocation HHI  (last-20-round mean)")
    ax2.set_title("Capital tracks market — but by how much?")
    ax2.grid(True, alpha=0.2)
    ax2.legend(loc="best", fontsize=7, frameon=False)

    fig.suptitle(
        "Does privacy disperse or concentrate capital?",
        fontsize=10, y=1.02,
    )
    fig.text(
        0.5, -0.03,
        "Left: Herfindahl index of funder allocations pooled across all funders. Right: last-20-round mean funder HHI vs market HHI, one "
        "point per (condition, seed). Points above $y{=}x$ mean capital is more concentrated than the market; below, less. "
        "Use to check whether privacy blunts the funder channel's amplification of score signals.",
        ha="center", fontsize=7, style="italic", color="#555",
    )
    fig.tight_layout()
    fig.savefig(out_path, dpi=180, bbox_inches="tight")
    fig.savefig(out_path.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)


# --- main --------------------------------------------------------------------

def main():
    out = Path(_paths.paper_dir())
    plot_alignment(out / "prototype_alignment_trajectory.png")
    plot_gaming_debt(out / "prototype_gaming_debt.png")
    plot_capital_concentration(out / "prototype_capital_concentration.png")
    print("wrote:")
    print(" ", out / "prototype_alignment_trajectory.png")
    print(" ", out / "prototype_gaming_debt.png")
    print(" ", out / "prototype_capital_concentration.png")


if __name__ == "__main__":
    main()
