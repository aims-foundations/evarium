"""
Plotting utilities for Evaluation Ecosystem Simulation

Three dashboards organized by question:
  A. Gap Anatomy — "Did gaming happen? What kind?"
  B. Market & Strategy — "Who won and why?"
  C. Costs & Interventions — "What were the costs?"
"""
import os
import warnings
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib as mpl
import numpy as np
from typing import Optional


def _mean_cap(h: dict, name: str) -> float:
    """Return composite capability scalar for a provider from a round dict."""
    vec = h.get("capability_vectors", {}).get(name)
    if not vec:
        return float('nan')
    return sum(vec.values()) / len(vec)

# Apply tueplots NeurIPS bundle for publication-quality styling.
# Falls back gracefully if tueplots is not installed or LaTeX is unavailable.
try:
    from tueplots import bundles as _tueplots_bundles
    _NEURIPS_RC = _tueplots_bundles.neurips2024()
    # Dashboards need more space than a single paper column — drop figsize override.
    _NEURIPS_RC.pop("figure.figsize", None)
    # Enable LaTeX rendering for publication-quality fonts.
    # Set MPLLATEX=0 in the environment to disable if LaTeX is not available.
    if os.environ.get("MPLLATEX", "1") != "0":
        _NEURIPS_RC["text.usetex"] = True
    mpl.rcParams.update(_NEURIPS_RC)
except ImportError:
    warnings.warn(
        "tueplots not installed — using default matplotlib style. "
        "Run: pip install tueplots",
        stacklevel=1,
    )


# =============================================================================
# Color Palettes and Styling
# =============================================================================

# Fixed colors for all known named providers — stable across runs.
PROVIDER_COLOR_MAP = {
    # Core 6-provider set
    "Orion Labs":      "#E63946",   # red
    "Apex AI":         "#457B9D",   # steel blue
    "Genesis Systems": "#2A9D8F",   # teal
    "Mirage AI":       "#E9C46A",   # gold
    "OpenCore":        "#6A4C93",   # purple (open-source)
    "Spark AI":        "#F4A261",   # orange (benchmark-focused)
}

# Overflow palette for dynamic startup entrants (OneAI, TwoAI, ...)
_STARTUP_OVERFLOW = ["#F4A261", "#264653", "#A8DADC", "#FB5607", "#FF006E",
                     "#3A86FF", "#06D6A0", "#9C6644", "#FFB703"]


def get_provider_colors(providers: list) -> dict:
    """Return a {provider_name: hex_color} dict.

    Known providers get their fixed color from PROVIDER_COLOR_MAP.
    Unknown providers (startups) are assigned overflow colors in order of
    first appearance.
    """
    result = {}
    overflow_index = 0
    for p in providers:
        if p in PROVIDER_COLOR_MAP:
            result[p] = PROVIDER_COLOR_MAP[p]
        else:
            result[p] = _STARTUP_OVERFLOW[overflow_index % len(_STARTUP_OVERFLOW)]
            overflow_index += 1
    return result


def _dashboard_figsize(rows: int, cols: int, base_w: float = 2.25, base_h: float = 1.7) -> tuple:
    """Return a sensible figure size scaled to the number of dashboard panels."""
    return (base_w * cols, base_h * rows)


def get_investment_colors() -> dict:
    """Colors for the 3-lever investment portfolio."""
    return {
        "rd":      "#2E86AB",  # Blue
        "safety":  "#C73E1D",  # Red
        "product": "#A23B72",  # Magenta
    }


def _tex_escape(s: str) -> str:
    """Escape LaTeX special characters in a string for safe rendering with usetex=True."""
    if not mpl.rcParams.get("text.usetex", False):
        return s
    for ch, esc in (("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"), ("_", r"\_")):
        s = s.replace(ch, esc)
    return s


def _tex_autopct(pct: float) -> str:
    """autopct function that is safe with text.usetex=True."""
    if mpl.rcParams.get("text.usetex", False):
        return r"{:.0f}\%".format(pct)
    return "{:.0f}%".format(pct)


def style_axis(ax, title: str, xlabel: str, ylabel: str, legend: bool = True):
    """Apply consistent styling to an axis.

    Font sizes are inherited from tueplots rcParams -- no overrides needed.
    """
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if legend:
        ax.legend(loc='best')


# =============================================================================
# Data Extraction Helpers
# =============================================================================

_DIMS = ["reasoning", "coding", "knowledge", "safety", "communication", "agentic"]


def get_providers(history: list) -> list:
    """Extract all provider names from history, ordered by first appearance."""
    if not history:
        return []
    seen = {}
    for h in history:
        for name in h.get("scores", {}):
            if name not in seen:
                seen[name] = h["round"]
    return sorted(seen, key=lambda n: seen[n])


def get_strategy_key(history: list) -> str:
    """Determine which strategy format is used."""
    if not history:
        return "new"
    first_strategy = list(history[0]["strategies"].values())[0]
    if "rd" in first_strategy:
        return "new"
    return "old"


def extract_investment(history: list, provider: str, investment_type: str) -> list:
    """Extract investment values for a provider over time."""
    return [h["strategies"].get(provider, {}).get(investment_type, 0) for h in history]


def compute_rolling_correlation(history: list, window_size: int = 5) -> tuple:
    """Compute rolling correlation between scores and true capabilities."""
    if len(history) < window_size:
        return [], []

    providers = get_providers(history)
    correlations = []
    rounds_used = []

    for i in range(window_size, len(history) + 1):
        window = history[i - window_size:i]
        all_scores = []
        all_caps = []
        for h in window:
            for provider in providers:
                if provider in h["scores"] and provider in h.get("capability_vectors", {}):
                    all_scores.append(h["scores"][provider])
                    all_caps.append(_mean_cap(h, provider))

        if len(all_scores) >= 2:
            corr = np.corrcoef(all_scores, all_caps)[0, 1]
            if not np.isnan(corr):
                correlations.append(corr)
                rounds_used.append(history[i - 1]["round"])

    return rounds_used, correlations


def categorize_headline(headline: str) -> str:
    """Classify a media headline into one of 7 categories via substring matching."""
    hl = headline.lower()
    if "takes the lead" in hl or "takes #1" in hl:
        return "leader_change"
    if "surges by" in hl:
        return "score_surge"
    if any(kw in hl for kw in ("investigation", "advisory", "commitment", "disclosure", "audit", "sanction")):
        return "regulatory"
    if "raises $" in hl:
        return "funding"
    if "surge in adoption" in hl or "turning away" in hl:
        return "consumer"
    if "benchmark" in hl or "validity" in hl:
        return "benchmark"
    return "other"


# =============================================================================
# Vector math helpers
# =============================================================================

def _to_vec(d: dict) -> np.ndarray:
    """Convert a {dim: value} dict to a numpy array in canonical DIMS order."""
    return np.array([d.get(dim, 0.0) for dim in _DIMS])


def _cos_sim(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity, returns 0 if either vector is zero."""
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na < 1e-12 or nb < 1e-12:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def _get_need_weights(history: list) -> np.ndarray:
    """Extract population-weighted need_weights from history.

    Falls back to stakeholders.md defaults if not logged.
    """
    for h in history:
        cd = h.get("consumer_data", {})
        nw = cd.get("need_weights")
        if nw:
            return _to_vec(nw)
    # Fallback: population-weighted average from stakeholders.md
    return np.array([0.22, 0.09, 0.23, 0.17, 0.26, 0.05])


def _get_bm_agg_weights(h: dict) -> np.ndarray:
    """Compute aggregate benchmark dimension weights for a round.

    Equal-weighted average across active benchmarks.
    """
    bdw = h.get("benchmark_dimension_weights", {})
    if not bdw:
        return np.ones(len(_DIMS)) / len(_DIMS)
    vecs = [_to_vec(w) for w in bdw.values()]
    return np.mean(vecs, axis=0)


def _gap_decomposition(h: dict, provider: str, need: np.ndarray) -> dict:
    """Decompose the score-satisfaction gap for one provider in one round.

    Returns dict with keys: score_noise, dim_mismatch, penalty_load, total_gap.
    """
    score = h.get("scores", {}).get(provider, 0.0)
    cap_dict = h.get("capability_vectors", {}).get(provider, {})
    cap = _to_vec(cap_dict)
    bm_agg = _get_bm_agg_weights(h)

    dot_cap_bm = float(np.dot(cap, bm_agg))
    dot_cap_need = float(np.dot(cap, need))

    cd = h.get("consumer_data", {})
    satisfaction = cd.get("provider_satisfaction", {}).get(provider, dot_cap_need)

    score_noise = score - dot_cap_bm
    dim_mismatch = dot_cap_bm - dot_cap_need
    penalty_load = dot_cap_need - satisfaction
    total_gap = score - satisfaction

    return {
        "score_noise": score_noise,
        "dim_mismatch": dim_mismatch,
        "penalty_load": penalty_load,
        "total_gap": total_gap,
    }


# =============================================================================
# Dashboard A: Gap Anatomy
# =============================================================================

def _cap_share(h: dict, provider: str) -> np.ndarray:
    """Get normalized capability share vector for a provider in a round."""
    cap_dict = h.get("capability_vectors", {}).get(provider, {})
    cap = _to_vec(cap_dict)
    total = cap.sum()
    return cap / total if total > 0 else cap


def plot_gap_anatomy(history: list, save_path: Optional[str] = None,
                     show: bool = True) -> Optional[plt.Figure]:
    """Dashboard A: Decompose the score-satisfaction gap.

    6 panels (3x2) — focused on dynamic evolution:
      A1: Cosine alignment to needs over time (line per provider)
      A2: L2 deviation from needs over time (line per provider)
      A3: Gap decomposition over time (total gap line per provider)
      A4: Rolling growth direction (cos of recent growth vs needs)
      A5: Score reliability over time
      A6: Gap waterfall (final round, decomposed)
    """
    if not history:
        return None

    providers = get_providers(history)
    colors = get_provider_colors(providers)
    need = _get_need_weights(history)
    rounds = [h["round"] for h in history]

    fig, axes = plt.subplots(3, 2, figsize=_dashboard_figsize(3, 2, 3.2, 2.4))

    # --- A1: Cosine alignment over time ---
    ax = axes[0, 0]
    for p in providers:
        cos_need = []
        cos_bm = []
        for h in history:
            cs = _cap_share(h, p)
            cos_need.append(_cos_sim(cs, need))
            bm_agg = _get_bm_agg_weights(h)
            cos_bm.append(_cos_sim(cs, bm_agg))
        ax.plot(rounds, cos_need, color=colors[p], lw=1.2,
                label=_tex_escape(p.split()[0]))
        ax.plot(rounds, cos_bm, color=colors[p], lw=0.8, ls='--', alpha=0.5)
    # Legend entries for line styles (A1-specific)
    ax.plot([], [], color='grey', ls='-', lw=1.2, label="vs needs")
    ax.plot([], [], color='grey', ls='--', lw=0.8, alpha=0.5, label="vs benchmarks")
    style_axis(ax, "Capability-Need Alignment", "Round", "Cosine similarity", legend=False)
    # A1 gets its own small legend for line styles only
    ax.legend(handles=[
        plt.Line2D([], [], color='grey', ls='-', lw=1.2, label="vs needs"),
        plt.Line2D([], [], color='grey', ls='--', lw=0.8, alpha=0.5, label="vs benchmarks"),
    ], loc='lower left', fontsize='x-small')

    # --- A2: L2 deviation from needs over time ---
    ax = axes[0, 1]
    for p in providers:
        l2_vals = []
        for h in history:
            cs = _cap_share(h, p)
            l2_vals.append(float(np.linalg.norm(cs - need)))
        ax.plot(rounds, l2_vals, color=colors[p], lw=1.2,
                label=_tex_escape(p.split()[0]))
    ax.axhline(0, color='grey', lw=0.5, ls='--')
    style_axis(ax, "Profile Deviation from Needs (L2)", "Round", "L2 distance", legend=False)

    # --- A3: Gap decomposition over time ---
    ax = axes[1, 0]
    for p in providers:
        gaps = []
        for h in history:
            g = _gap_decomposition(h, p, need)
            gaps.append(g["total_gap"])
        ax.plot(rounds, gaps, color=colors[p], label=_tex_escape(p.split()[0]), lw=1.2)
    ax.axhline(0, color='grey', lw=0.5, ls='--')
    style_axis(ax, "Score $-$ Satisfaction Gap", "Round", "Score $-$ Satisfaction", legend=False)

    # --- A4: Rolling growth direction (cos of recent growth vs needs) ---
    ax = axes[1, 1]
    growth_window = min(5, max(2, len(history) // 5))
    for p in providers:
        rolling_cos = []
        rolling_rounds = []
        for i in range(growth_window, len(history)):
            cap_prev = _to_vec(history[i - growth_window].get("capability_vectors", {}).get(p, {}))
            cap_curr = _to_vec(history[i].get("capability_vectors", {}).get(p, {}))
            growth = cap_curr - cap_prev
            if np.linalg.norm(growth) > 1e-8:
                rolling_cos.append(_cos_sim(growth, need))
            else:
                rolling_cos.append(float('nan'))
            rolling_rounds.append(history[i]["round"])
        if rolling_rounds:
            ax.plot(rolling_rounds, rolling_cos, color=colors[p], lw=1.2,
                    label=_tex_escape(p.split()[0]))
    style_axis(ax, f"Rolling Growth Direction ({growth_window}r window)",
               "Round", "cos(growth, needs)", legend=False)

    # Shared provider legend between rows 2 and 3
    handles = [plt.Line2D([], [], color=colors[p], lw=1.2, label=_tex_escape(p.split()[0]))
               for p in providers]
    fig.legend(handles=handles, loc='lower center', ncol=min(len(providers), 6),
               bbox_to_anchor=(0.5, 0.32), fontsize='small', frameon=False)

    # --- A5: Score Reliability ---
    ax = axes[2, 0]
    if len(history) >= 3:
        window = min(5, len(history))
        rel_rounds = []
        rel_vals = []
        for i in range(window, len(history) + 1):
            w = history[i - window:i]
            scores_list, sats_list = [], []
            for h in w:
                cd = h.get("consumer_data", {})
                ps = cd.get("provider_satisfaction", {})
                for p in providers:
                    if p in h.get("scores", {}) and p in ps:
                        scores_list.append(h["scores"][p])
                        sats_list.append(ps[p])
            if len(scores_list) >= 2:
                from scipy.stats import rankdata
                sr = rankdata(scores_list)
                satr = rankdata(sats_list)
                corr = np.corrcoef(sr, satr)[0, 1]
                if not np.isnan(corr):
                    rel_rounds.append(history[i - 1]["round"])
                    rel_vals.append(corr)
        if rel_rounds:
            ax.plot(rel_rounds, rel_vals, color="#333333", lw=1.5)
            ax.fill_between(rel_rounds, rel_vals, alpha=0.15, color="#333333")
            ax.set_ylim(-0.1, 1.1)
    style_axis(ax, "Score Reliability (rank corr)", "Round",
               "Pearson r(score rank, sat rank)", legend=False)

    # --- A6: Gap Waterfall (final round) ---
    ax = axes[2, 1]
    final = history[-1]
    gap_components = {p: _gap_decomposition(final, p, need) for p in providers}

    x = np.arange(len(providers))
    bar_w = 0.22
    noise_vals = [gap_components[p]["score_noise"] for p in providers]
    mismatch_vals = [gap_components[p]["dim_mismatch"] for p in providers]
    penalty_vals = [gap_components[p]["penalty_load"] for p in providers]

    ax.bar(x - bar_w, noise_vals, bar_w, label="Inflation", color="#4ECDC4")
    ax.bar(x, mismatch_vals, bar_w, label="Misalignment", color="#FF6B6B")
    ax.bar(x + bar_w, penalty_vals, bar_w, label="Externalities", color="#45B7D1")
    totals = [gap_components[p]["total_gap"] for p in providers]
    ax.scatter(x, totals, color="black", zorder=5, s=20, marker="D", label="Total gap")
    ax.set_xticks(x)
    ax.set_xticklabels([_tex_escape(p.split()[0]) for p in providers], rotation=30, ha='right')
    ax.axhline(0, color='grey', lw=0.5, ls='--')
    style_axis(ax, "Gap Waterfall (Final Round)", "", "Score $-$ Satisfaction")

    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
    if show:
        plt.show()
    return fig


def plot_initial_conditions(history: list, save_path: Optional[str] = None,
                            show: bool = True) -> Optional[plt.Figure]:
    """Static context plot: benchmark weights vs consumer need weights.

    Run once per experimental setup, not per run. Shows the structural
    misalignment between what benchmarks measure and what consumers need.

    4 panels (2x2):
      Top-left: Dimensional profile (benchmark agg vs needs per dimension)
      Top-right: Per-benchmark structural alignment (cos(bm, need) bars)
      Bottom-left: Provider-Benchmark cosine similarity heatmap
      Bottom-right: Provider-Need cosine similarity heatmap
    """
    if not history:
        return None

    providers = get_providers(history)
    need = _get_need_weights(history)
    h0 = history[0]

    fig, axes = plt.subplots(2, 2, figsize=(8, 6), layout='constrained')

    # Top-left: Dimensional profile
    ax = axes[0, 0]
    bm_agg = _get_bm_agg_weights(h0)
    dim_labels = [_tex_escape(d[:5]) for d in _DIMS]
    x = np.arange(len(_DIMS))
    bar_w = 0.35
    ax.bar(x - bar_w / 2, bm_agg, bar_w, label="Benchmark avg", color="#555555", alpha=0.8)
    ax.bar(x + bar_w / 2, need, bar_w, label="Consumer needs", color="#2A9D8F", alpha=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(dim_labels)
    style_axis(ax, "Benchmark vs Consumer Weights", "", "Weight")

    # Top-right: Per-benchmark alignment
    ax = axes[0, 1]
    bdw = h0.get("benchmark_dimension_weights", {})
    if bdw:
        bm_names = list(bdw.keys())
        cos_vals = [_cos_sim(_to_vec(bdw[b]), need) for b in bm_names]
        y = np.arange(len(bm_names))
        bar_colors_bm = plt.cm.RdYlGn(np.array(cos_vals))
        ax.barh(y, cos_vals, color=bar_colors_bm, height=0.6)
        ax.set_yticks(y)
        ax.set_yticklabels([_tex_escape(b[:18]) for b in bm_names])
        ax.set_xlim(0, 1)
    style_axis(ax, "Benchmark-Need Alignment", "cos(bm, need)", "", legend=False)

    # Bottom-left: Provider-Benchmark cosine similarity heatmap
    ax = axes[1, 0]
    if bdw:
        bm_names = list(bdw.keys())
        cap_vecs = {p: _to_vec(h0.get("capability_vectors", {}).get(p, {})) for p in providers}
        bm_vecs = {b: _to_vec(bdw[b]) for b in bm_names}
        matrix_bm = np.array([
            [_cos_sim(cap_vecs[p], bm_vecs[b]) for b in bm_names]
            for p in providers
        ])
        im = ax.imshow(matrix_bm, cmap="RdYlGn", aspect="auto", vmin=0.7, vmax=1.0)
        ax.set_xticks(range(len(bm_names)))
        ax.set_xticklabels([_tex_escape(b[:12]) for b in bm_names], rotation=30, ha='right')
        ax.set_yticks(range(len(providers)))
        ax.set_yticklabels([_tex_escape(p.split()[0]) for p in providers])
        # Annotate cells
        for i in range(len(providers)):
            for j in range(len(bm_names)):
                ax.text(j, i, f"{matrix_bm[i, j]:.2f}", ha='center', va='center', fontsize=7)
        fig.colorbar(im, ax=ax, shrink=0.8)
    style_axis(ax, "Provider-Benchmark Alignment", "", "", legend=False)

    # Bottom-right: Provider-Need cosine similarity heatmap
    ax = axes[1, 1]
    cap_vecs = {p: _to_vec(h0.get("capability_vectors", {}).get(p, {})) for p in providers}
    cos_need_vals = [_cos_sim(cap_vecs[p], need) for p in providers]
    # Single-column heatmap
    matrix_need = np.array(cos_need_vals).reshape(-1, 1)
    im = ax.imshow(matrix_need, cmap="RdYlGn", aspect=0.3, vmin=0.7, vmax=1.0)
    ax.set_xticks([0])
    ax.set_xticklabels(["Consumer needs"])
    ax.set_yticks(range(len(providers)))
    ax.set_yticklabels([_tex_escape(p.split()[0]) for p in providers])
    for i in range(len(providers)):
        ax.text(0, i, f"{cos_need_vals[i]:.3f}", ha='center', va='center', fontsize=8)
    fig.colorbar(im, ax=ax, shrink=0.8)
    style_axis(ax, "Provider-Need Alignment", "", "", legend=False)

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
    if show:
        plt.show()
    return fig


# =============================================================================
# Dashboard B: Market & Strategy
# =============================================================================

def plot_market_strategy(history: list, save_path: Optional[str] = None,
                         show: bool = True) -> Optional[plt.Figure]:
    """Dashboard B: Market dynamics and provider strategy.

    6 panels (3x2):
      B1: Market Share (stacked area)
      B2: Investment Portfolio (small multiples)
      B3: Funder Allocations
      B4: Benchmark Orientation
      B5: Consumer Switching Rate
      B6: Per-Benchmark Scores (small multiples)
    """
    if not history:
        return None

    providers = get_providers(history)
    colors = get_provider_colors(providers)
    inv_colors = get_investment_colors()
    rounds = [h["round"] for h in history]

    fig, axes = plt.subplots(3, 2, figsize=_dashboard_figsize(3, 2, 3.2, 2.4))

    # --- B1: Market Share (stacked area) ---
    ax = axes[0, 0]
    share_data = {p: [] for p in providers}
    for h in history:
        cd = h.get("consumer_data", {})
        ms = cd.get("market_shares", {})
        for p in providers:
            share_data[p].append(ms.get(p, 0.0))
    bottom = np.zeros(len(rounds))
    for p in providers:
        vals = np.array(share_data[p])
        ax.fill_between(rounds, bottom, bottom + vals, label=_tex_escape(p.split()[0]),
                        color=colors[p], alpha=0.8)
        bottom += vals
    style_axis(ax, "Market Share", "Round", "Share")

    # --- B2: Investment Portfolio (small multiples) ---
    ax = axes[0, 1]
    # Show as lines (one per lever per provider) since small multiples don't fit one axis
    for p in providers:
        rd = extract_investment(history, p, "rd")
        safety = extract_investment(history, p, "safety")
        ax.plot(rounds, rd, color=colors[p], lw=1.0, ls='-')
        ax.plot(rounds, safety, color=colors[p], lw=1.0, ls='--', alpha=0.7)
    # Manual legend entries
    ax.plot([], [], color='grey', ls='-', label="R\\&D" if mpl.rcParams.get("text.usetex") else "R&D")
    ax.plot([], [], color='grey', ls='--', label="Safety")
    style_axis(ax, "Investment (solid=R\\&D, dash=Safety)" if mpl.rcParams.get("text.usetex")
               else "Investment (solid=R&D, dash=Safety)", "Round", "Allocation")

    # --- B3: Funder Allocations ---
    ax = axes[1, 0]
    funder_rounds = [h for h in history if "funder_data" in h]
    if funder_rounds:
        funder_names = set()
        for h in funder_rounds:
            funder_names.update(h["funder_data"].get("allocations", {}).keys())
        funder_names = sorted(funder_names)
        funder_palette = plt.cm.Set2(np.linspace(0, 1, max(len(funder_names), 1)))

        fr_rounds = [h["round"] for h in funder_rounds]
        # Total funding per funder over time
        for i, fn in enumerate(funder_names):
            totals = []
            for h in funder_rounds:
                alloc = h["funder_data"].get("allocations", {}).get(fn, {})
                totals.append(sum(alloc.values()) if isinstance(alloc, dict) else 0)
            ax.plot(fr_rounds, totals, label=_tex_escape(fn[:15]), color=funder_palette[i], lw=1.0)
    style_axis(ax, "Funder Allocations", "Round", _tex_escape("Total ($)"))

    # --- B4: Benchmark Orientation ---
    ax = axes[1, 1]
    for p in providers:
        bo = [h.get("benchmark_orientations", {}).get(p, float('nan')) for h in history]
        ax.plot(rounds, bo, color=colors[p], label=_tex_escape(p.split()[0]), lw=1.2)
    ax.set_ylim(-0.05, 1.05)
    style_axis(ax, "Benchmark Orientation", "Round", "Orientation (0=need, 1=benchmark)")

    # --- B5: Consumer Switching Rate ---
    ax = axes[2, 0]
    sr = [h.get("consumer_data", {}).get("switching_rate", 0.0) for h in history]
    ax.plot(rounds, sr, color="#333333", lw=1.5)
    ax.fill_between(rounds, sr, alpha=0.15, color="#333333")
    style_axis(ax, "Consumer Switching Rate", "Round", "Rate", legend=False)

    # --- B6: Per-Benchmark Scores ---
    ax = axes[2, 1]
    # Collect all benchmarks
    all_bm = set()
    for h in history:
        all_bm.update(h.get("per_benchmark_scores", {}).keys())
    all_bm = sorted(all_bm)

    if all_bm and len(providers) > 0:
        # Plot mean score across providers per benchmark
        bm_palette = plt.cm.tab10(np.linspace(0, 1, max(len(all_bm), 1)))
        for i, bm in enumerate(all_bm):
            means = []
            bm_rounds = []
            for h in history:
                bm_scores = h.get("per_benchmark_scores", {}).get(bm, {})
                if bm_scores:
                    means.append(np.max(list(bm_scores.values())))
                    bm_rounds.append(h["round"])
            if bm_rounds:
                ax.plot(bm_rounds, means, color=bm_palette[i],
                        label=_tex_escape(bm[:12]), lw=1.0, alpha=0.8)
    style_axis(ax, "Benchmark Scores (max)", "Round", "Score")

    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
    if show:
        plt.show()
    return fig


# =============================================================================
# Dashboard C: Costs & Interventions
# =============================================================================

def plot_costs_interventions(history: list, save_path: Optional[str] = None,
                             show: bool = True) -> Optional[plt.Figure]:
    """Dashboard C: Costs of gaming and ecosystem interventions.

    6 panels (3x2):
      C1: Incident Timeline
      C2: Safety Investment vs Incident Rate
      C3: Penalty Load Over Time
      C4: Media Sentiment + Provider Attention
      C5: Intervention Timeline
      C6: Cumulative Incidents by Provider
    """
    if not history:
        return None

    providers = get_providers(history)
    colors = get_provider_colors(providers)
    need = _get_need_weights(history)
    rounds = [h["round"] for h in history]

    fig, axes = plt.subplots(3, 2, figsize=_dashboard_figsize(3, 2, 3.2, 2.4),
                             layout='constrained')

    severity_colors = {
        "minor": "#A8DADC",
        "moderate": "#F4A261",
        "major": "#E76F51",
        "critical": "#E63946",
    }

    # --- C1: Incident Timeline ---
    ax = axes[0, 0]
    for h in history:
        incidents = h.get("incidents", [])
        for inc in incidents:
            sev = inc.get("severity", "minor")
            prov = inc.get("provider", "")
            ax.scatter(h["round"], providers.index(prov) if prov in providers else 0,
                       color=severity_colors.get(sev, "#999"),
                       s={"minor": 15, "moderate": 30, "major": 60, "critical": 100}.get(sev, 20),
                       alpha=0.8, zorder=3)
    ax.set_yticks(range(len(providers)))
    ax.set_yticklabels([_tex_escape(p.split()[0]) for p in providers])
    # Legend for severity
    for sev, col in severity_colors.items():
        ax.scatter([], [], color=col, s=30, label=sev)
    style_axis(ax, "Incident Timeline", "Round", "")

    # --- C2: Safety Investment vs Incident Rate ---
    ax = axes[0, 1]
    for p in providers:
        safety_vals = []
        inc_rates = []
        for h in history:
            s = h.get("strategies", {}).get(p, {}).get("safety", 0)
            safety_vals.append(s)
            incs = h.get("incidents", [])
            inc_rates.append(sum(1 for i in incs if i.get("provider") == p))
        # Plot as connected scatter (safety vs cumulative incident rate)
        cum_inc = np.cumsum(inc_rates)
        ax.plot(safety_vals, cum_inc, color=colors[p], marker='o', ms=2.5, lw=0.8,
                label=_tex_escape(p.split()[0]), alpha=0.8)
        # Arrow showing direction
        if len(safety_vals) > 1:
            ax.annotate("", xy=(safety_vals[-1], cum_inc[-1]),
                        xytext=(safety_vals[-2], cum_inc[-2]),
                        arrowprops=dict(arrowstyle="->", color=colors[p], lw=1.0))
    style_axis(ax, "Safety Invest. vs Incidents", "Safety allocation", "Cumulative incidents")

    # --- C3: Penalty Load Over Time ---
    ax = axes[2, 0]  # Moved to bottom-left
    for p in providers:
        penalty_vals = []
        for h in history:
            cap = _to_vec(h.get("capability_vectors", {}).get(p, {}))
            dot_cn = float(np.dot(cap, need))
            cd = h.get("consumer_data", {})
            sat = cd.get("provider_satisfaction", {}).get(p, dot_cn)
            penalty_vals.append(dot_cn - sat)
        ax.plot(rounds, penalty_vals, color=colors[p],
                label=_tex_escape(p.split()[0]), lw=1.2)
    ax.axhline(0, color='grey', lw=0.5, ls='--')
    style_axis(ax, "Penalty Load (dot(cap,need) - sat)", "Round", "Penalty")

    # --- C4: Media Sentiment + Provider Attention ---
    ax = axes[1, 0]
    media_rounds = [h for h in history if "media_data" in h]
    if media_rounds and providers:
        mr = [h["round"] for h in media_rounds]
        # Heatmap of provider attention
        attn_matrix = np.zeros((len(providers), len(media_rounds)))
        for j, h in enumerate(media_rounds):
            pa = h["media_data"].get("provider_attention", {})
            sent = h["media_data"].get("sentiment", 0.0)
            for i, p in enumerate(providers):
                # Combine attention and sentiment sign
                attn_matrix[i, j] = pa.get(p, 0.0) * (1 if sent >= 0 else -1)
        im = ax.imshow(attn_matrix, aspect='auto', cmap='RdYlGn',
                       vmin=-1, vmax=1, interpolation='nearest')
        ax.set_yticks(range(len(providers)))
        ax.set_yticklabels([_tex_escape(p.split()[0]) for p in providers])
        # Show round numbers on x axis
        tick_step = max(1, len(mr) // 6)
        ax.set_xticks(range(0, len(mr), tick_step))
        ax.set_xticklabels([str(mr[i]) for i in range(0, len(mr), tick_step)])
    style_axis(ax, "Media: Attention x Sentiment", "Round", "", legend=False)

    # --- C5: Intervention Timeline ---
    ax = axes[1, 1]
    # Parse regulator interventions
    intervention_events = []
    for h in history:
        rd = h.get("regulator_data", h.get("policymaker_data", {}))
        if not rd:
            continue
        interventions = rd.get("interventions", [])
        for intv in interventions:
            if isinstance(intv, dict):
                intervention_events.append({
                    "round": h["round"],
                    "type": intv.get("type", intv.get("action", "unknown")),
                    "target": intv.get("provider", intv.get("target", "")),
                })
            elif isinstance(intv, str):
                intervention_events.append({
                    "round": h["round"],
                    "type": intv,
                    "target": "",
                })
    if intervention_events:
        intv_types = sorted(set(e["type"] for e in intervention_events))
        type_palette = plt.cm.Set1(np.linspace(0, 1, max(len(intv_types), 1)))
        type_color = {t: type_palette[i] for i, t in enumerate(intv_types)}
        for e in intervention_events:
            target_idx = providers.index(e["target"]) if e["target"] in providers else -0.5
            ax.scatter(e["round"], target_idx, color=type_color[e["type"]],
                       s=40, zorder=3, alpha=0.8)
        ax.set_yticks(range(len(providers)))
        ax.set_yticklabels([_tex_escape(p.split()[0]) for p in providers])
        for t, c in type_color.items():
            ax.scatter([], [], color=c, s=30, label=_tex_escape(t[:15]))
    style_axis(ax, "Interventions", "Round", "")

    # --- C6: Cumulative Incidents by Provider ---
    ax = axes[2, 1]
    cum_incidents = {p: [] for p in providers}
    running = {p: 0 for p in providers}
    for h in history:
        for inc in h.get("incidents", []):
            prov = inc.get("provider", "")
            if prov in running:
                running[prov] += 1
        for p in providers:
            cum_incidents[p].append(running[p])
    for p in providers:
        ax.plot(rounds, cum_incidents[p], color=colors[p],
                label=_tex_escape(p.split()[0]), lw=1.2)
    style_axis(ax, "Cumulative Incidents", "Round", "Count")

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
    if show:
        plt.show()
    return fig


# =============================================================================
# Orchestration
# =============================================================================

def create_all_dashboards(
    history: list,
    output_dir: str = "./plots",
    show: bool = False,
    metadata: Optional[dict] = None,
) -> dict:
    """Create and save all dashboards.

    Returns:
        Dict of {dashboard_name: figure_path}
    """
    os.makedirs(output_dir, exist_ok=True)
    saved = {}

    print("Creating dashboards...")

    # Initial conditions (static context)
    fig = plot_initial_conditions(history, show=False)
    if fig:
        path = f"{output_dir}/initial_conditions.png"
        fig.savefig(path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        saved['initial_conditions'] = path
        print("  - Initial conditions saved")

    # Dashboard A: Gap Anatomy
    fig = plot_gap_anatomy(history, show=False)
    if fig:
        path = f"{output_dir}/gap_anatomy.png"
        fig.savefig(path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        saved['gap_anatomy'] = path
        print("  - Gap Anatomy dashboard saved")

    # Dashboard B: Market & Strategy
    fig = plot_market_strategy(history, show=False)
    if fig:
        path = f"{output_dir}/market_strategy.png"
        fig.savefig(path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        saved['market_strategy'] = path
        print("  - Market & Strategy dashboard saved")

    # Dashboard C: Costs & Interventions
    fig = plot_costs_interventions(history, show=False)
    if fig:
        path = f"{output_dir}/costs_interventions.png"
        fig.savefig(path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        saved['costs_interventions'] = path
        print("  - Costs & Interventions dashboard saved")

    print(f"\nAll dashboards saved to: {output_dir}")
    return saved


# =============================================================================
# Presentation Plots (slide-optimized, 16:9 beamer)
# =============================================================================

def _pres_figsize(n_cols: int) -> tuple:
    """Figure size for a 1×N row on a 16:9 beamer slide."""
    w = 3.6 * n_cols
    h = 2.8
    return (w, h)


def _pres_provider_legend(fig, providers, colors, ncol=None):
    """Add a shared provider legend at the bottom of a presentation figure."""
    if ncol is None:
        ncol = min(len(providers), 6)
    handles = [mlines.Line2D([], [], color=colors[p], lw=1.8,
                              label=_tex_escape(p))
               for p in providers]
    fig.legend(handles=handles, loc='lower center', ncol=ncol,
               bbox_to_anchor=(0.5, -0.02), fontsize='small', frameon=False)


def pres_slide1_gap_anatomy(history: list, save_path: str,
                            show: bool = False) -> Optional[plt.Figure]:
    """Presentation slide 1: Gap Anatomy (1×3).

    Panel 1: Capability-Need Alignment (cosine over rounds)
    Panel 2: Score-Satisfaction Gap + Score Reliability overlay
    Panel 3: Gap Waterfall (final round, decomposed)
    """
    if not history:
        return None

    providers = get_providers(history)
    colors = get_provider_colors(providers)
    need = _get_need_weights(history)
    rounds = [h["round"] for h in history]

    fig, axes = plt.subplots(1, 3, figsize=_pres_figsize(3))

    # --- Panel 1: Capability-Need Alignment ---
    ax = axes[0]
    for p in providers:
        cos_need = []
        cos_bm = []
        for h in history:
            cs = _cap_share(h, p)
            cos_need.append(_cos_sim(cs, need))
            bm_agg = _get_bm_agg_weights(h)
            cos_bm.append(_cos_sim(cs, bm_agg))
        ax.plot(rounds, cos_need, color=colors[p], lw=1.4)
        ax.plot(rounds, cos_bm, color=colors[p], lw=0.8, ls='--', alpha=0.45)
    ax.plot([], [], color='grey', ls='-', lw=1.4, label="vs needs")
    ax.plot([], [], color='grey', ls='--', lw=0.8, alpha=0.45, label="vs benchmarks")
    ax.legend(loc='lower left', fontsize=6)
    style_axis(ax, "Capability-Need Alignment", "Round", "Cosine similarity", legend=False)

    # --- Panel 2: Score-Satisfaction Gap + Score Reliability ---
    ax = axes[1]
    for p in providers:
        gaps = [_gap_decomposition(h, p, need)["total_gap"] for h in history]
        ax.plot(rounds, gaps, color=colors[p], lw=1.4)
    ax.axhline(0, color='grey', lw=0.5, ls='--')
    style_axis(ax, "Score $-$ Satisfaction Gap", "Round", "Score $-$ Satisfaction", legend=False)

    # Overlay score reliability on secondary y-axis
    if len(history) >= 3:
        ax2 = ax.twinx()
        window = min(5, len(history))
        rel_rounds, rel_vals = [], []
        for i in range(window, len(history) + 1):
            w = history[i - window:i]
            scores_list, sats_list = [], []
            for h in w:
                cd = h.get("consumer_data", {})
                ps = cd.get("provider_satisfaction", {})
                for p in providers:
                    if p in h.get("scores", {}) and p in ps:
                        scores_list.append(h["scores"][p])
                        sats_list.append(ps[p])
            if len(scores_list) >= 2:
                from scipy.stats import rankdata
                sr = rankdata(scores_list)
                satr = rankdata(sats_list)
                corr = np.corrcoef(sr, satr)[0, 1]
                if not np.isnan(corr):
                    rel_rounds.append(history[i - 1]["round"])
                    rel_vals.append(corr)
        if rel_rounds:
            ax2.plot(rel_rounds, rel_vals, color='#333333', lw=1.5, ls=':', alpha=0.7)
            ax2.fill_between(rel_rounds, rel_vals, alpha=0.08, color='#333333')
            ax2.set_ylim(-0.1, 1.1)
            ax2.set_ylabel("Score reliability", fontsize=7)
            ax2.tick_params(labelsize=6)
            # Add to panel legend
            ax.plot([], [], color='#333333', ls=':', lw=1.5, alpha=0.7, label="Reliability")
            ax.legend(loc='upper right', fontsize=6)

    # --- Panel 3: Gap Waterfall (mean over last 5 rounds) ---
    ax = axes[2]
    tail = history[-min(10, len(history)):]

    # Collect per-provider decomposition across tail rounds
    noise_vals, mismatch_vals, penalty_vals = [], [], []
    total_means, total_ses = [], []
    for p in providers:
        p_noise, p_mismatch, p_penalty, p_total = [], [], [], []
        for h in tail:
            g = _gap_decomposition(h, p, need)
            p_noise.append(g["score_noise"])
            p_mismatch.append(g["dim_mismatch"])
            p_penalty.append(g["penalty_load"])
            p_total.append(g["total_gap"])
        noise_vals.append(np.mean(p_noise))
        mismatch_vals.append(np.mean(p_mismatch))
        penalty_vals.append(np.mean(p_penalty))
        total_means.append(np.mean(p_total))
        total_ses.append(np.std(p_total, ddof=1) / np.sqrt(len(p_total))
                         if len(p_total) > 1 else 0.0)

    x = np.arange(len(providers))
    bar_w = 0.22
    ax.bar(x - bar_w, noise_vals, bar_w, label="Inflation", color="#4ECDC4")
    ax.bar(x, mismatch_vals, bar_w, label="Misalignment", color="#FF6B6B")
    ax.bar(x + bar_w, penalty_vals, bar_w, label="Externalities", color="#45B7D1")
    ax.errorbar(x, total_means, yerr=total_ses, fmt='D', color="black",
                markersize=4, capsize=2, capthick=0.8, lw=0.8, zorder=5, label="Total gap")
    ax.set_xticks(x)
    ax.set_xticklabels([_tex_escape(p.split()[0]) for p in providers], rotation=30, ha='right')
    ax.axhline(0, color='grey', lw=0.5, ls='--')
    n_tail = len(tail)
    style_axis(ax, f"Gap Waterfall (last {n_tail}r mean)", "", "Score $-$ Satisfaction")

    _pres_provider_legend(fig, providers, colors)
    fig.tight_layout(rect=[0, 0.06, 1, 1.0])

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
    if show:
        plt.show()
    return fig


def pres_slide2_market_safety(history: list, save_path: str,
                              show: bool = False) -> Optional[plt.Figure]:
    """Presentation slide 2: Market & Safety (1×3).

    Panel 1: Market Share (stacked area)
    Panel 2: Incident Timeline + Interventions
    Panel 3: Score-Satisfaction Gap (repeated for comparison)
    """
    if not history:
        return None

    providers = get_providers(history)
    colors = get_provider_colors(providers)
    need = _get_need_weights(history)
    rounds = [h["round"] for h in history]

    fig, axes = plt.subplots(1, 3, figsize=_pres_figsize(3))

    # --- Panel 1: Market Share (stacked area) ---
    ax = axes[0]
    share_data = {p: [] for p in providers}
    for h in history:
        cd = h.get("consumer_data", {})
        ms = cd.get("market_shares", {})
        for p in providers:
            share_data[p].append(ms.get(p, 0.0))
    bottom = np.zeros(len(rounds))
    for p in providers:
        vals = np.array(share_data[p])
        ax.fill_between(rounds, bottom, bottom + vals,
                        color=colors[p], alpha=0.8)
        bottom += vals
    style_axis(ax, "Market Share", "Round", "Share", legend=False)

    # --- Panel 2: Score-Satisfaction Gap + Score Reliability (same as slide 1) ---
    ax = axes[1]
    for p in providers:
        gaps = [_gap_decomposition(h, p, need)["total_gap"] for h in history]
        ax.plot(rounds, gaps, color=colors[p], lw=1.4)
    ax.axhline(0, color='grey', lw=0.5, ls='--')
    style_axis(ax, "Score $-$ Satisfaction Gap", "Round", "Score $-$ Satisfaction", legend=False)

    # Overlay score reliability on secondary y-axis
    if len(history) >= 3:
        ax2 = ax.twinx()
        window = min(5, len(history))
        rel_rounds, rel_vals = [], []
        for i in range(window, len(history) + 1):
            w = history[i - window:i]
            scores_list, sats_list = [], []
            for h in w:
                cd = h.get("consumer_data", {})
                ps = cd.get("provider_satisfaction", {})
                for p in providers:
                    if p in h.get("scores", {}) and p in ps:
                        scores_list.append(h["scores"][p])
                        sats_list.append(ps[p])
            if len(scores_list) >= 2:
                from scipy.stats import rankdata
                sr = rankdata(scores_list)
                satr = rankdata(sats_list)
                corr = np.corrcoef(sr, satr)[0, 1]
                if not np.isnan(corr):
                    rel_rounds.append(history[i - 1]["round"])
                    rel_vals.append(corr)
        if rel_rounds:
            ax2.plot(rel_rounds, rel_vals, color='#333333', lw=1.5, ls=':', alpha=0.7)
            ax2.fill_between(rel_rounds, rel_vals, alpha=0.08, color='#333333')
            ax2.set_ylim(-0.1, 1.1)
            ax2.set_ylabel("Score reliability", fontsize=7)
            ax2.tick_params(labelsize=6)
            ax.plot([], [], color='#333333', ls=':', lw=1.5, alpha=0.7, label="Reliability")
            ax.legend(loc='upper right', fontsize=6)

    # --- Panel 3: Incident Timeline + Interventions ---
    ax = axes[2]
    severity_markers = {"minor": "o", "moderate": "s", "major": "^", "critical": "X"}
    severity_sizes = {"minor": 25, "moderate": 50, "major": 80, "critical": 120}

    for h in history:
        for inc in h.get("incidents", []):
            prov = inc.get("provider", "")
            if prov not in providers:
                continue
            sev = inc.get("severity", "minor")
            ax.scatter(
                h["round"], providers.index(prov),
                marker=severity_markers.get(sev, "o"),
                s=severity_sizes.get(sev, 25),
                color=colors[prov], alpha=0.8,
                edgecolors='black', linewidth=0.5, zorder=3,
            )

    # Overlay interventions as vertical lines / markers
    for h in history:
        rd = h.get("regulator_data", h.get("policymaker_data", {}))
        if not rd:
            continue
        for intv in rd.get("interventions", []):
            if isinstance(intv, dict):
                target = intv.get("provider", intv.get("target", ""))
                itype = intv.get("type", intv.get("action", ""))
                if target in providers:
                    ax.axvline(h["round"], color='#E63946', lw=0.6, ls='--', alpha=0.35)
                    ax.scatter(h["round"], providers.index(target),
                               marker='|', s=100, color='#E63946',
                               lw=1.5, zorder=4, alpha=0.8)
                else:
                    # Ecosystem-wide intervention (no specific target)
                    ax.axvline(h["round"], color='#E63946', lw=0.8, ls='--', alpha=0.4, zorder=2)

    ax.set_yticks(range(len(providers)))
    ax.set_yticklabels([_tex_escape(p.split()[0]) for p in providers], fontsize=7)

    # Severity legend
    sev_handles = [
        mlines.Line2D([0], [0], marker=m, color='w', markerfacecolor='gray',
                      markeredgecolor='black', markersize=sz**0.5,
                      label=sev.capitalize())
        for sev, m in severity_markers.items()
        for sz in [severity_sizes[sev]]
    ]
    intv_handle = mlines.Line2D([0], [0], marker='|', color='#E63946',
                                markersize=8, lw=0, label="Intervention")
    ax.legend(handles=sev_handles + [intv_handle], loc='upper right',
              fontsize=5, ncol=2, handletextpad=0.3)
    style_axis(ax, "Incidents \\& Interventions" if mpl.rcParams.get("text.usetex")
               else "Incidents & Interventions", "Round", "", legend=False)

    _pres_provider_legend(fig, providers, colors)
    fig.tight_layout(rect=[0, 0.06, 1, 1.0])

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
    if show:
        plt.show()
    return fig


def generate_presentation_plots(
    history: list,
    output_dir: str,
    fmt: str = "pdf",
) -> dict:
    """Generate all presentation-optimized plots.

    Args:
        history: List of round dicts from rounds.jsonl.
        output_dir: Directory to save figures.
        fmt: Output format ('pdf' for vector, 'png' for raster).

    Returns:
        Dict of {name: file_path}.
    """
    os.makedirs(output_dir, exist_ok=True)
    saved = {}

    print("Generating presentation plots...")

    path = os.path.join(output_dir, f"pres_slide1_gap_anatomy.{fmt}")
    fig = pres_slide1_gap_anatomy(history, save_path=path, show=False)
    if fig:
        plt.close(fig)
        saved['slide1_gap_anatomy'] = path
        print(f"  - Slide 1: Gap Anatomy saved")

    path = os.path.join(output_dir, f"pres_slide2_market_safety.{fmt}")
    fig = pres_slide2_market_safety(history, save_path=path, show=False)
    if fig:
        plt.close(fig)
        saved['slide2_market_safety'] = path
        print(f"  - Slide 2: Market & Safety saved")

    print(f"Presentation plots saved to: {output_dir}")
    return saved


