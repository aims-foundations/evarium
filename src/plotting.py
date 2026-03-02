"""
Plotting utilities for Evaluation Ecosystem Simulation

Provides dashboards for each actor type and a summary dashboard.
Scalable to N providers/actors.
"""
import os
import warnings
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib as mpl
import numpy as np
from typing import Optional

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
    # Core 5-provider set
    "Orion Labs":      "#E63946",   # red
    "Apex AI":         "#457B9D",   # steel blue
    "Genesis Systems": "#2A9D8F",   # teal
    "Mirage AI":       "#E9C46A",   # gold
    "OpenCore":        "#6A4C93",   # purple (open-source)
}

# Overflow palette for dynamic startup entrants (OneAI, TwoAI, …)
# Reuses legacy colors + additional distinct picks (avoids purple overlap with OpenCore)
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
    """Colors for the 4-way investment portfolio."""
    return {
        "fundamental_research": "#2E86AB",    # Blue
        "training_optimization": "#A23B72",   # Magenta
        "evaluation_engineering": "#F18F01",  # Orange
        "safety_alignment": "#C73E1D",        # Red
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

    Font sizes are inherited from tueplots rcParams — no overrides needed.
    """
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if legend:
        ax.legend(loc='best')


# =============================================================================
# Data Extraction Helpers
# =============================================================================

def get_providers(history: list) -> list:
    """Extract all provider names from history, ordered by first appearance.

    Handles mid-run entrants (startups) that are absent from early rounds.
    """
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
    if "fundamental_research" in first_strategy:
        return "new"
    return "old"


def extract_investment(history: list, provider: str, investment_type: str) -> list:
    """Extract investment values for a provider over time.

    Returns 0 for rounds where the provider did not yet exist.
    """
    return [h["strategies"].get(provider, {}).get(investment_type, 0) for h in history]


def compute_rolling_correlation(history: list, window_size: int = 5) -> tuple:
    """Compute rolling correlation between scores and true capabilities.

    Returns (rounds, correlations) where rounds are actual round numbers
    (from history[i]["round"]), not array indices.
    """
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
                if provider in h["scores"] and provider in h["true_capabilities"]:
                    all_scores.append(h["scores"][provider])
                    all_caps.append(h["true_capabilities"][provider])

        if len(all_scores) >= 2:
            corr = np.corrcoef(all_scores, all_caps)[0, 1]
            if not np.isnan(corr):
                correlations.append(corr)
                # Use actual round number from history, not array index
                rounds_used.append(history[i - 1]["round"])

    return rounds_used, correlations


def compute_per_benchmark_rolling_correlation(history: list, window_size: int = 5) -> dict:
    """Compute rolling correlation per benchmark.

    Returns {benchmark_name: (rounds, correlations)} where each benchmark
    gets its own validity correlation over time.
    """
    if len(history) < window_size:
        return {}

    # Check if we have per-benchmark data
    if not history or "per_benchmark_scores" not in history[0]:
        return {}

    providers = get_providers(history)

    # Get all benchmark names across all rounds
    all_benchmarks = set()
    for h in history:
        if "per_benchmark_scores" in h:
            all_benchmarks.update(h["per_benchmark_scores"].keys())

    benchmark_correlations = {}

    for benchmark in all_benchmarks:
        correlations = []
        rounds_used = []

        for i in range(window_size, len(history) + 1):
            window = history[i - window_size:i]
            benchmark_scores = []
            benchmark_caps = []

            for h in window:
                per_bm = h.get("per_benchmark_scores", {})
                if benchmark in per_bm:
                    for provider in providers:
                        if provider in per_bm[benchmark] and provider in h["true_capabilities"]:
                            benchmark_scores.append(per_bm[benchmark][provider])
                            benchmark_caps.append(h["true_capabilities"][provider])

            if len(benchmark_scores) >= 2:
                corr = np.corrcoef(benchmark_scores, benchmark_caps)[0, 1]
                if not np.isnan(corr):
                    correlations.append(corr)
                    rounds_used.append(history[i - 1]["round"])

        if correlations:
            benchmark_correlations[benchmark] = (rounds_used, correlations)

    return benchmark_correlations


def categorize_headline(headline: str) -> str:
    """Classify a media headline into one of 7 categories via substring matching."""
    hl = headline.lower()
    if "takes the lead" in hl or "takes #1" in hl:
        return "leader_change"
    if "surges by" in hl:
        return "score_surge"
    if any(kw in hl for kw in ("investigation", "warning", "mandate", "audit")):
        return "regulatory"
    if "raises $" in hl:
        return "funding"
    if "surge in adoption" in hl or "turning away" in hl:
        return "consumer"
    if "benchmark" in hl or "validity" in hl:
        return "benchmark"
    return "other"


# =============================================================================
# Provider Dashboard
# =============================================================================

def plot_provider_dashboard(
    history: list,
    save_path: Optional[str] = None,
    show: bool = True,
    figsize: tuple = (6.75, 5.06),
    os_provider_names: set = None,
) -> Optional[plt.Figure]:
    """
    Create a comprehensive dashboard for Model Providers.

    Panels:
    1. Benchmark Scores over time
    2. True vs Believed Capability
    3. Investment Portfolio (stacked area)
    4. Gaming vs Safety Investment
    5. Score - True Capability Gap
    6. OS vs Closed Frontier Gap (or Capability Growth bar if no OS providers)

    Args:
        history: List of round data dicts
        save_path: Path to save figure
        show: Whether to display
        figsize: Figure size
        os_provider_names: Set of open-source provider names (auto-detected if None)

    Returns:
        matplotlib Figure or None
    """
    if not history:
        print("No history to plot")
        return None

    providers = get_providers(history)
    n_providers = len(providers)
    provider_colors = get_provider_colors(providers)
    inv_colors = get_investment_colors()

    rounds = [h["round"] for h in history]

    # Auto-detect OS/startup providers from new_entrant rounds
    entrant_names = {h["new_entrant"]["name"] for h in history if "new_entrant" in h}
    os_provider_names = (os_provider_names or set()) | entrant_names

    # Build entry event dict: {round: entrant_name}
    entry_rounds = {h["round"]: h["new_entrant"]["name"] for h in history if "new_entrant" in h}

    def _add_entry_lines(ax):
        for r in entry_rounds:
            ax.axvline(x=r, color='gray', linestyle=':', alpha=0.4, linewidth=1)

    def _provider_line_style(provider):
        """Return kwargs for line style based on OS vs closed."""
        if provider in os_provider_names:
            return dict(linestyle='--', marker='o', markerfacecolor='none')
        return dict(linestyle='-', marker='o')

    def _provider_label(provider):
        if provider in os_provider_names:
            return f"{provider} [OS]"
        return provider

    from matplotlib.gridspec import GridSpecFromSubplotSpec

    fig, axes = plt.subplots(2, 3, figsize=figsize)
    fig.suptitle("Provider Dashboard", fontweight='bold')

    investment_types = ["fundamental_research", "training_optimization",
                        "evaluation_engineering", "safety_alignment"]

    # --- Panel 1: Scores over time ---
    ax1 = axes[0, 0]
    for provider in providers:
        scores = [h["scores"].get(provider) for h in history]
        ax1.plot(rounds, scores, label=_provider_label(provider),
                 color=provider_colors[provider], markersize=3, linewidth=1.5, alpha=0.8,
                 **_provider_line_style(provider))
    _add_entry_lines(ax1)
    ax1.set_ylim(0, 1)
    style_axis(ax1, "Benchmark Scores Over Time", "Round", "Score", legend=False)

    # --- Panel 2: True vs Believed Capability ---
    ax2 = axes[0, 1]
    for provider in providers:
        true_caps = [h["true_capabilities"].get(provider) for h in history]
        believed_caps = [h["believed_capabilities"].get(provider) for h in history]
        ls = '--' if provider in os_provider_names else '-'
        ax2.plot(rounds, true_caps, ls, color=provider_colors[provider], linewidth=2)
        ax2.plot(rounds, believed_caps, ':', color=provider_colors[provider],
                 linewidth=1.5, alpha=0.6)
    _add_entry_lines(ax2)
    style_handles = [
        mlines.Line2D([], [], color='gray', linestyle='-', linewidth=2, label='True'),
        mlines.Line2D([], [], color='gray', linestyle=':', linewidth=1.5,
                      alpha=0.6, label='Believed'),
    ]
    ax2.legend(handles=style_handles, loc='best', fontsize=7)
    style_axis(ax2, "True vs Believed Capability", "Round", "Capability", legend=False)

    # --- Panel 3: Investment Portfolio (mini-grid inside top-right cell) ---
    ax3 = axes[0, 2]
    ax3.axis('off')

    # Determine mini-grid layout: prefer 2 columns, as few rows as needed
    if n_providers <= 2:
        grid_rows, grid_cols = 1, 2
    elif n_providers <= 4:
        grid_rows, grid_cols = 2, 2
    elif n_providers <= 6:
        grid_rows, grid_cols = 3, 2
    else:
        grid_rows, grid_cols = 4, 2

    # Add a title row (index 0) and legend row (last) via height_ratios so the
    # mini-subplots don't fill the entire cell — no floating text/legend overlaps.
    title_ratio = 0.15
    legend_ratio = 0.18
    gs = GridSpecFromSubplotSpec(
        grid_rows + 2, grid_cols,
        subplot_spec=ax3.get_subplotspec(),
        hspace=0.12, wspace=0.12,
        height_ratios=[title_ratio] + [1.0] * grid_rows + [legend_ratio],
    )

    # Title row — single invisible axis spanning all columns
    ax_title = fig.add_subplot(gs[0, :])
    ax_title.axis('off')
    ax_title.text(0.5, 0.5, "Investment Portfolio",
                  ha='center', va='center', fontsize=9, fontweight='bold',
                  transform=ax_title.transAxes)

    for idx, provider in enumerate(providers):
        if idx >= grid_rows * grid_cols:
            break
        row = idx // grid_cols
        col = idx % grid_cols
        sub_ax = fig.add_subplot(gs[row + 1, col])  # +1 to skip title row

        bottom_arr = np.zeros(len(rounds))
        for inv_type in investment_types:
            values = np.array(extract_investment(history, provider, inv_type))
            sub_ax.fill_between(rounds, bottom_arr, bottom_arr + values,
                               alpha=0.7, color=inv_colors[inv_type])
            bottom_arr += values

        sub_ax.set_ylim(0, 1.05)
        sub_ax.set_title(provider, fontsize=7, fontweight='bold', pad=2)
        sub_ax.tick_params(labelsize=5)
        sub_ax.grid(False)
        if row < grid_rows - 1:
            sub_ax.set_xticklabels([])
        if col > 0:
            sub_ax.set_yticklabels([])

    # Legend row — single invisible axis spanning all columns, below the plots
    ax_legend = fig.add_subplot(gs[grid_rows + 1, :])
    ax_legend.axis('off')
    legend_elements = [
        mpatches.Patch(facecolor=inv_colors[t], alpha=0.7,
                       label=t.replace("_", " ").title()[:14])
        for t in investment_types
    ]
    ax_legend.legend(handles=legend_elements, loc='center',
                     ncol=2, fontsize=6, frameon=True)

    # --- Panel 4: Gaming vs Safety Investment ---
    ax4 = axes[1, 0]
    for provider in providers:
        eval_eng = extract_investment(history, provider, "evaluation_engineering")
        safety_al = extract_investment(history, provider, "safety_alignment")
        style = _provider_line_style(provider)
        ax4.plot(rounds, eval_eng, label=_provider_label(provider),
                 color=provider_colors[provider], markersize=3, linewidth=2, **style)
        ax4.plot(rounds, safety_al,
                 color=provider_colors[provider], markersize=2, linewidth=1.2,
                 linestyle=':', alpha=0.7)
    _add_entry_lines(ax4)
    ax4.axhline(y=0.25, color='gray', linestyle=':', alpha=0.5)
    ax4.set_ylim(0, 1)
    style_handles_p4 = [
        mlines.Line2D([], [], color='gray', linestyle='-', label='Eval Eng'),
        mlines.Line2D([], [], color='gray', linestyle=':', label='Safety'),
        mlines.Line2D([], [], color='gray', linestyle=':', alpha=0.5, label='Balanced'),
    ]
    ax4.legend(handles=style_handles_p4, fontsize=7, loc='best')
    style_axis(ax4, "Gaming vs Safety Investment", "Round", "Investment", legend=False)

    # --- Panel 5: Score - Capability Gap ---
    ax5 = axes[1, 1]
    for provider in providers:
        scores = np.array([h["scores"].get(provider) for h in history], dtype=float)
        true_caps = np.array([h["true_capabilities"].get(provider) for h in history], dtype=float)
        gap = scores - true_caps
        ax5.plot(rounds, gap, label=_provider_label(provider),
                 color=provider_colors[provider], markersize=3, linewidth=2,
                 **_provider_line_style(provider))
    _add_entry_lines(ax5)
    ax5.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.5)
    ax5.fill_between(rounds, 0, 0.1, alpha=0.1, color='orange', label='Inflated')
    ax5.fill_between(rounds, -0.1, 0, alpha=0.1, color='blue', label='Deflated')
    shade_handles = [
        mpatches.Patch(facecolor='orange', alpha=0.1, label='Inflated'),
        mpatches.Patch(facecolor='blue', alpha=0.1, label='Deflated'),
    ]
    ax5.legend(handles=shade_handles, fontsize=7, loc='best')
    style_axis(ax5, "Score - True Capability Gap", "Round", "Gap (Score - True)", legend=False)

    # --- Panel 6: OS vs Closed Frontier Gap (or Capability Growth bar if no OS) ---
    ax6 = axes[1, 2]
    if os_provider_names:
        gap_vals = []
        gap_rounds = []
        for h in history:
            tc = h["true_capabilities"]
            closed_caps = [tc[p] for p in providers if p not in os_provider_names and p in tc]
            os_caps = [tc[p] for p in providers if p in os_provider_names and p in tc]
            if closed_caps and os_caps:
                gap_vals.append(max(closed_caps) - max(os_caps))
                gap_rounds.append(h["round"])
        if gap_vals:
            gap_arr = np.array(gap_vals)
            ax6.plot(gap_rounds, gap_vals, 'o-', color='#457B9D', linewidth=2)
            ax6.fill_between(gap_rounds, 0, gap_vals,
                             where=gap_arr >= 0, alpha=0.2, color='blue',
                             interpolate=True, label='Closed ahead')
            ax6.fill_between(gap_rounds, 0, gap_vals,
                             where=gap_arr < 0, alpha=0.2, color='green',
                             interpolate=True, label='OS ahead')
            ax6.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.5)
            _add_entry_lines(ax6)
            style_axis(ax6, "OS vs Closed Frontier Gap", "Round", "Closed Leader - OS Leader")
        else:
            ax6.text(0.5, 0.5, "No OS capability data", ha='center', va='center',
                     transform=ax6.transAxes, fontsize=10, alpha=0.5)
            style_axis(ax6, "OS vs Closed Frontier Gap", "Round", "Gap", legend=False)
    else:
        initial_caps = [
            next(h["true_capabilities"][p] for h in history if p in h["true_capabilities"])
            for p in providers
        ]
        final_caps = [
            next(h["true_capabilities"][p] for h in reversed(history) if p in h["true_capabilities"])
            for p in providers
        ]
        growth = [f - i for i, f in zip(initial_caps, final_caps)]
        x = np.arange(len(providers))
        bars = ax6.bar(x, growth, color=[provider_colors[p] for p in providers], alpha=0.8)
        ax6.set_xticks(x)
        ax6.set_xticklabels(providers, rotation=45, ha='right', fontsize=8)
        ax6.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        style_axis(ax6, "Capability Growth (Final - Initial)", "", "Growth", legend=False)
        for bar, val in zip(bars, growth):
            ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                    f'{val:.3f}', ha='center', va='bottom', fontsize=8)


    # Shared provider legend at the bottom
    provider_handles = [
        mlines.Line2D([], [], color=provider_colors[p], linewidth=2,
                      label=_provider_label(p), **_provider_line_style(p))
        for p in providers
    ]
    fig.legend(handles=provider_handles, loc='lower center',
               ncol=min(len(providers), 5), fontsize=7, frameon=True,
               bbox_to_anchor=(0.5, -0.16))
    fig.subplots_adjust(bottom=0.12)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Provider dashboard saved to: {save_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig


# =============================================================================
# Consumer Dashboard (split into Satisfaction + Switching/Market figures)
# =============================================================================

def _consumer_common(history):
    """Extract common data for consumer plots."""
    consumer_rounds = [h for h in history if "consumer_data" in h]
    if not consumer_rounds:
        return None
    providers = get_providers(history)
    provider_colors = get_provider_colors(providers)
    rounds = [h["round"] for h in consumer_rounds]
    # Map each provider to the round it first appears in scores
    provider_first_round = {}
    for h in consumer_rounds:
        for p in h.get("scores", {}):
            if p not in provider_first_round:
                provider_first_round[p] = h["round"]

    # Use cases
    use_cases_set = set()
    for h in consumer_rounds:
        for seg_info in h["consumer_data"].get("segment_data", {}).values():
            uc = seg_info.get("use_case")
            if uc:
                use_cases_set.add(uc)
    use_cases = sorted(use_cases_set)
    use_case_colors = list(get_provider_colors(use_cases).values())

    # Archetypes
    archetypes_set = set()
    for h in consumer_rounds:
        for seg_info in h["consumer_data"].get("segment_data", {}).values():
            arch = seg_info.get("archetype")
            if arch:
                archetypes_set.add(arch)
    archetypes = sorted(archetypes_set)
    archetype_colors = list(get_provider_colors(archetypes).values())

    return dict(
        consumer_rounds=consumer_rounds, providers=providers,
        provider_colors=provider_colors, rounds=rounds,
        provider_first_round=provider_first_round, use_cases=use_cases,
        use_case_colors=use_case_colors, archetypes=archetypes,
        archetype_colors=archetype_colors,
    )


def plot_consumer_satisfaction(
    history: list,
    save_path: Optional[str] = None,
    show: bool = True,
    figsize: tuple = (6.75, 2.5),
) -> Optional[plt.Figure]:
    """Consumer satisfaction dashboard (1x3): by Use Case, per Provider, Gap."""
    ctx = _consumer_common(history)
    if ctx is None:
        print("No consumer data to plot")
        return None

    consumer_rounds = ctx["consumer_rounds"]
    providers, provider_colors = ctx["providers"], ctx["provider_colors"]
    rounds = ctx["rounds"]
    provider_first_round = ctx["provider_first_round"]
    use_cases, use_case_colors = ctx["use_cases"], ctx["use_case_colors"]
    first_round_min = min(rounds) if rounds else 0

    fig, axes = plt.subplots(1, 3, figsize=figsize)
    fig.suptitle("Consumer Satisfaction", fontweight='bold')

    # --- Panel 1: Satisfaction by Use Case ---
    ax1 = axes[0]
    for i, use_case in enumerate(use_cases):
        use_case_satisfaction = []
        for h in consumer_rounds:
            segment_data = h["consumer_data"].get("segment_data", {})
            total_sat, count = 0.0, 0
            for seg_info in segment_data.values():
                if seg_info.get("use_case") == use_case:
                    seg_sats = seg_info.get("satisfaction", {}).values()
                    if seg_sats:
                        total_sat += sum(seg_sats) / len(seg_sats)
                        count += 1
            use_case_satisfaction.append(total_sat / count if count > 0 else 0)
        ax1.plot(rounds, use_case_satisfaction, 'o-',
                 label=use_case.replace("_", " ").title(),
                 color=use_case_colors[i], markersize=2, linewidth=1.2)
    ax1.set_ylim(0, 1)
    style_axis(ax1, "Satisfaction by Use Case", "Round", "Satisfaction", legend=False)

    # --- Panel 2: Satisfaction by Provider ---
    ax2 = axes[1]
    avg_satisfaction = [h["consumer_data"].get("avg_satisfaction", 0)
                        for h in consumer_rounds]
    for provider in providers:
        prov_sats = [h["consumer_data"].get("provider_satisfaction", {}).get(provider, float('nan'))
                     for h in consumer_rounds]
        ax2.plot(rounds, prov_sats, 'o-', color=provider_colors[provider],
                 markersize=2, linewidth=1.5)
        # Star marker at provider's first round
        fr = provider_first_round.get(provider)
        if fr is not None and fr > first_round_min:
            idx = rounds.index(fr) if fr in rounds else None
            if idx is not None and not np.isnan(prov_sats[idx]):
                ax2.plot(fr, prov_sats[idx], '*', color=provider_colors[provider],
                         markersize=10, zorder=5)
    ax2.plot(rounds, avg_satisfaction, 'k--', linewidth=1.5, alpha=0.5, label='Market Avg')
    ax2.set_ylim(0, 1)
    ax2.legend(fontsize=6, loc='best')
    style_axis(ax2, "Satisfaction by Provider", "Round", "Satisfaction", legend=False)

    # --- Panel 3: Satisfaction Gap ---
    ax3 = axes[2]
    for provider in providers:
        pcr = [h for h in consumer_rounds if provider in h["scores"]]
        p_rounds = [h["round"] for h in pcr]
        scores = [h["scores"][provider] for h in pcr]
        prov_sats = [h["consumer_data"].get("provider_satisfaction", {}).get(provider, float('nan'))
                     for h in pcr]
        gap = [s - sat for s, sat in zip(scores, prov_sats)]
        ax3.plot(p_rounds, gap, 'o-', color=provider_colors[provider],
                 markersize=2, linewidth=1.5)
        # Star marker at provider's first round
        fr = provider_first_round.get(provider)
        if fr is not None and fr > first_round_min and fr in p_rounds:
            idx = p_rounds.index(fr)
            if not np.isnan(gap[idx]):
                ax3.plot(fr, gap[idx], '*', color=provider_colors[provider],
                         markersize=10, zorder=5)
    style_axis(ax3, "Satisfaction Gap by Provider", "Round", "Score - Satisfaction", legend=False)

    # Bottom legends: row 1 = providers, row 2 = use cases
    provider_handles = [
        mlines.Line2D([], [], color=provider_colors[p], linewidth=2, label=p)
        for p in providers
    ]
    use_case_handles = [
        mlines.Line2D([], [], color=use_case_colors[i], linewidth=2,
                      label=uc.replace("_", " ").title())
        for i, uc in enumerate(use_cases)
    ]
    leg1 = fig.legend(handles=provider_handles, loc='lower center',
                      ncol=len(providers), fontsize=6, frameon=False,
                      bbox_to_anchor=(0.5, -0.16), title="Providers",
                      title_fontproperties={'size': 7, 'weight': 'bold'})
    fig.add_artist(leg1)
    import math
    fig.legend(handles=use_case_handles, loc='lower center',
               ncol=math.ceil(len(use_cases) / 2), fontsize=6, frameon=False,
               bbox_to_anchor=(0.5, -0.32), title="Use Cases",
               title_fontproperties={'size': 7, 'weight': 'bold'})

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Consumer satisfaction saved to: {save_path}")
    if show:
        plt.show()
    else:
        plt.close(fig)
    return fig


def plot_consumer_switching(
    history: list,
    save_path: Optional[str] = None,
    show: bool = True,
    figsize: tuple = (6.75, 2.5),
) -> Optional[plt.Figure]:
    """Consumer switching + market dashboard (1x3): by Use Case, by Archetype, Market Share."""
    ctx = _consumer_common(history)
    if ctx is None:
        print("No consumer data to plot")
        return None

    consumer_rounds = ctx["consumer_rounds"]
    providers, provider_colors = ctx["providers"], ctx["provider_colors"]
    rounds = ctx["rounds"]
    provider_first_round = ctx["provider_first_round"]
    use_cases, use_case_colors = ctx["use_cases"], ctx["use_case_colors"]
    archetypes, archetype_colors = ctx["archetypes"], ctx["archetype_colors"]
    first_round_min = min(rounds) if rounds else 0

    fig, axes = plt.subplots(1, 3, figsize=figsize)
    fig.suptitle("Consumer Switching and Market Share", fontweight='bold')

    # --- Panel 1: Switching Rate by Use Case ---
    ax1 = axes[0]
    use_case_switching = {uc: [] for uc in use_cases}
    for h in consumer_rounds:
        segment_data = h["consumer_data"].get("segment_data", {})
        uc_totals = {uc: 0.0 for uc in use_cases}
        for seg_info in segment_data.values():
            uc = seg_info.get("use_case")
            if uc in use_cases:
                uc_totals[uc] += seg_info.get("switching_rate", 0.0) * seg_info.get("market_fraction", 0.0)
        for uc in use_cases:
            use_case_switching[uc].append(uc_totals[uc])

    bottom = np.zeros(len(rounds))
    for i, uc in enumerate(use_cases):
        values = np.array(use_case_switching[uc])
        ax1.bar(rounds, values, bottom=bottom,
                label=uc.replace("_", " ").title(),
                color=use_case_colors[i], alpha=0.8, width=0.8)
        bottom += values
    style_axis(ax1, "Switching Rate by Use Case", "Round", "Switching Rate", legend=False)

    # --- Panel 2: Switching Rate by Archetype ---
    ax2 = axes[1]
    archetype_switching = {arch: [] for arch in archetypes}
    for h in consumer_rounds:
        segment_data = h["consumer_data"].get("segment_data", {})
        arch_totals = {arch: 0.0 for arch in archetypes}
        for seg_info in segment_data.values():
            arch = seg_info.get("archetype")
            if arch in archetypes:
                arch_totals[arch] += seg_info.get("switching_rate", 0.0) * seg_info.get("market_fraction", 0.0)
        for arch in archetypes:
            archetype_switching[arch].append(arch_totals[arch])

    bottom = np.zeros(len(rounds))
    for i, arch in enumerate(archetypes):
        values = np.array(archetype_switching[arch])
        ax2.bar(rounds, values, bottom=bottom,
                label=arch.replace("_", " ").title(),
                color=archetype_colors[i], alpha=0.8, width=0.8)
        bottom += values
    style_axis(ax2, "Switching Rate by Archetype", "Round", "Switching Rate", legend=False)

    # --- Panel 3: Market Share Over Time ---
    ax3 = axes[2]
    market_share = {p: [] for p in providers}
    for h in consumer_rounds:
        shares = h["consumer_data"].get("market_shares", {})
        for p in providers:
            market_share[p].append(shares.get(p, 0))
    bottom = np.zeros(len(rounds))
    for provider in providers:
        values = np.array(market_share[provider])
        ax3.fill_between(rounds, bottom, bottom + values,
                         alpha=0.7, color=provider_colors[provider])
        # Star marker at provider's first round (on the stacked area)
        fr = provider_first_round.get(provider)
        if fr is not None and fr > first_round_min and fr in rounds:
            idx = rounds.index(fr)
            y_mid = bottom[idx] - values[idx] / 2  # middle of this provider's band
            ax3.plot(fr, bottom[idx] - values[idx] / 2, '*',
                     color=provider_colors[provider], markersize=10,
                     zorder=5, markeredgecolor='white', markeredgewidth=0.5)
        bottom += values
    ax3.set_ylim(0, 1.05)
    style_axis(ax3, "Market Share", "Round", "Share", legend=False)

    # Bottom legends: row 1 = providers, row 2 = use cases, row 3 = archetypes
    provider_handles = [
        mlines.Line2D([], [], color=provider_colors[p], linewidth=2, label=p)
        for p in providers
    ]
    use_case_handles = [
        mpatches.Patch(facecolor=use_case_colors[i], alpha=0.8,
                       label=uc.replace("_", " ").title())
        for i, uc in enumerate(use_cases)
    ]
    archetype_handles = [
        mpatches.Patch(facecolor=archetype_colors[i], alpha=0.8,
                       label=arch.replace("_", " ").title())
        for i, arch in enumerate(archetypes)
    ]
    leg1 = fig.legend(handles=provider_handles, loc='lower center',
                      ncol=len(providers), fontsize=6, frameon=False,
                      bbox_to_anchor=(0.5, -0.16), title="Providers",
                      title_fontproperties={'size': 7, 'weight': 'bold'})
    fig.add_artist(leg1)
    import math
    leg2 = fig.legend(handles=use_case_handles, loc='lower center',
                      ncol=math.ceil(len(use_cases) / 2), fontsize=6, frameon=False,
                      bbox_to_anchor=(0.5, -0.32), title="Use Cases",
                      title_fontproperties={'size': 7, 'weight': 'bold'})
    fig.add_artist(leg2)
    fig.legend(handles=archetype_handles, loc='lower center',
               ncol=len(archetypes), fontsize=6, frameon=False,
               bbox_to_anchor=(0.5, -0.48), title="Archetypes",
               title_fontproperties={'size': 7, 'weight': 'bold'})

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Consumer switching saved to: {save_path}")
    if show:
        plt.show()
    else:
        plt.close(fig)
    return fig


def plot_consumer_dashboard(
    history: list,
    save_path: Optional[str] = None,
    show: bool = True,
    **kwargs,
) -> Optional[plt.Figure]:
    """Consumer dashboard — generates two separate figures (satisfaction + switching).

    When save_path is provided, saves *_satisfaction.png and *_switching.png
    alongside the original path.
    """
    import os
    base, ext = (os.path.splitext(save_path) if save_path else (None, ".png"))

    sat_path = f"{base}_satisfaction{ext}" if save_path else None
    swi_path = f"{base}_switching{ext}" if save_path else None

    fig1 = plot_consumer_satisfaction(history, save_path=sat_path, show=show)
    fig2 = plot_consumer_switching(history, save_path=swi_path, show=show)
    return fig1


# =============================================================================
# Policymaker Dashboard
# =============================================================================

def plot_policymaker_dashboard(
    history: list,
    save_path: Optional[str] = None,
    show: bool = True,
    figsize: tuple = (6.75, 3.86),
) -> Optional[plt.Figure]:
    """
    Create a dashboard for Policymaker actors.

    Panels:
    1. Validity Correlation with Intervention & Incident Markers
    2. Intervention Timeline
    3. Active Regulations Count
    4. Intervention Types Distribution

    Args:
        history: List of round data dicts
        save_path: Path to save figure
        show: Whether to display
        figsize: Figure size

    Returns:
        matplotlib Figure or None
    """
    policymaker_rounds = [h for h in history if "policymaker_data" in h]
    if not policymaker_rounds:
        print("No policymaker data to plot")
        return None

    rounds = [h["round"] for h in history]

    # Extract intervention data
    intervention_rounds = []
    intervention_types = []
    for h in history:
        if "policymaker_data" in h:
            interventions = h["policymaker_data"].get("interventions", [])
            if interventions:
                intervention_rounds.append(h["round"])
                for interv in interventions:
                    if "type" in interv:
                        intervention_types.append(interv["type"])

    # Extract incident data
    incident_rounds = []
    incident_severities = []
    for h in history:
        if "incidents" in h and h["incidents"]:
            for inc in h["incidents"]:
                incident_rounds.append(h["round"])
                incident_severities.append(inc["severity"])

    fig, axes = plt.subplots(2, 2, figsize=figsize)
    fig.suptitle("Policymaker Dashboard", fontweight='bold')

    # --- Panel 1: Validity Correlation with Interventions & Incidents ---
    ax1 = axes[0, 0]
    validity_rounds, validity_values = compute_rolling_correlation(history)

    if validity_values:
        ax1.plot(validity_rounds, validity_values, '-', color='#457B9D',
                 linewidth=1.5, label='Validity')

    # Mark interventions
    for ir in intervention_rounds:
        ax1.axvline(x=ir, color='#E63946', linestyle='--', alpha=0.5, linewidth=0.8)
    if intervention_rounds:
        ax1.axvline(x=intervention_rounds[0], color='#E63946', linestyle='--',
                   alpha=0.5, linewidth=0.8, label='Intervention')

    # Mark incidents with different colors by severity
    severity_colors = {"minor": "#90EE90", "moderate": "#FFD700", "major": "#FF8C00", "critical": "#DC143C"}
    incident_legend_added = {}
    for ir, sev in zip(incident_rounds, incident_severities):
        color = severity_colors.get(sev, "#666666")
        label = f'Incident ({sev})' if sev not in incident_legend_added else None
        if label:
            incident_legend_added[sev] = True
        ax1.axvline(x=ir, color=color, linestyle=':', alpha=0.4, linewidth=1, label=label)

    ax1.set_ylim(-0.2, 1.0)
    style_axis(ax1, r"Benchmark Validity \& Events", "Round", "Correlation")

    # --- Panel 2: Intervention Timeline ---
    ax2 = axes[0, 1]
    intervention_indicator = [1 if r in intervention_rounds else 0 for r in rounds]
    colors = ['#E63946' if v else '#CCCCCC' for v in intervention_indicator]
    ax2.bar(rounds, [1]*len(rounds), color=colors, alpha=0.7)
    ax2.set_ylim(0, 1.5)
    ax2.set_yticks([])
    style_axis(ax2, "Intervention Timeline", "Round", "", legend=False)

    # Add count annotation
    total_interventions = sum(intervention_indicator)
    ax2.text(0.95, 0.95, f"Total: {total_interventions}", transform=ax2.transAxes,
             ha='right', va='top', fontsize=8, fontweight='bold')

    # --- Panel 3: Active Regulations Count ---
    ax3 = axes[1, 0]
    active_counts = []
    for h in history:
        if "policymaker_data" in h:
            active = h["policymaker_data"].get("active_regulations", [])
            active_counts.append(len(active))
        else:
            active_counts.append(0)

    ax3.fill_between(rounds, 0, active_counts, alpha=0.3, color='#6A4C93')
    ax3.plot(rounds, active_counts, '-', color='#6A4C93', linewidth=1.5)
    style_axis(ax3, "Active Regulations Over Time", "Round", "Count", legend=False)

    # --- Panel 4: Intervention Types Distribution ---
    ax4 = axes[1, 1]
    if intervention_types:
        unique_types = list(set(intervention_types))
        type_counts = [intervention_types.count(t) for t in unique_types]
        colors = plt.cm.Set2(np.linspace(0, 1, len(unique_types)))
        ax4.pie(type_counts, labels=[_tex_escape(t) for t in unique_types],
                autopct=_tex_autopct, colors=colors, textprops={'fontsize': 6})
        ax4.set_title("Intervention Types", fontweight='bold')
    else:
        ax4.text(0.5, 0.5, "No interventions", ha='center', va='center', fontsize=8)
        ax4.set_title("Intervention Types", fontweight='bold')
        ax4.axis('off')


    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Policymaker dashboard saved to: {save_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig


# =============================================================================
# Evaluator Dashboard
# =============================================================================

def plot_evaluator_dashboard(
    history: list,
    save_path: Optional[str] = None,
    show: bool = True,
    figsize: tuple = (6.75, 2.5),
) -> Optional[plt.Figure]:
    """
    Create a dashboard for the Evaluator (benchmark analysis).

    Panels (1x3):
    1. Benchmark Score by Provider Over Time
    2. True Capability by Provider Over Time
    3. Validity Correlation Over Time
    """
    if not history:
        print("No history to plot")
        return None

    providers = get_providers(history)
    provider_colors = get_provider_colors(providers)
    rounds = [h["round"] for h in history]
    first_round_min = min(rounds) if rounds else 0

    # Detect each provider's first round
    provider_first_round = {}
    for h in history:
        for p in h.get("scores", {}):
            if p not in provider_first_round:
                provider_first_round[p] = h["round"]

    fig, axes = plt.subplots(1, 3, figsize=figsize)
    fig.suptitle("Evaluator Dashboard", fontweight='bold')

    # --- Panel 1: Benchmark Score by Provider ---
    ax1 = axes[0]
    for provider in providers:
        scores = [h["scores"].get(provider, float('nan')) for h in history]
        ax1.plot(rounds, scores, 'o-', color=provider_colors[provider],
                 markersize=2, linewidth=1.5)
        fr = provider_first_round.get(provider)
        if fr is not None and fr > first_round_min and fr in rounds:
            idx = rounds.index(fr)
            if not np.isnan(scores[idx]):
                ax1.plot(fr, scores[idx], '*', color=provider_colors[provider],
                         markersize=10, zorder=5)
    ax1.set_ylim(0, 1)
    style_axis(ax1, "Benchmark Score by Provider", "Round", "Score", legend=False)

    # --- Panel 2: True Capability by Provider ---
    ax2 = axes[1]
    for provider in providers:
        caps = [h["true_capabilities"].get(provider, float('nan')) for h in history]
        ax2.plot(rounds, caps, 'o-', color=provider_colors[provider],
                 markersize=2, linewidth=1.5)
        fr = provider_first_round.get(provider)
        if fr is not None and fr > first_round_min and fr in rounds:
            idx = rounds.index(fr)
            if not np.isnan(caps[idx]):
                ax2.plot(fr, caps[idx], '*', color=provider_colors[provider],
                         markersize=10, zorder=5)
    ax2.set_ylim(0, 1)
    style_axis(ax2, "True Capability by Provider", "Round", "Capability", legend=False)

    # --- Panel 3: Validity Correlation Over Time ---
    ax3 = axes[2]
    validity_rounds, validity_values = compute_rolling_correlation(history)
    if validity_values:
        ax3.plot(validity_rounds, validity_values, 'o-', color='#2A9D8F',
                 markersize=3, linewidth=2)
    ax3.set_ylim(-0.2, 1.0)
    style_axis(ax3, "Benchmark Validity", "Round", "Correlation", legend=False)

    # Shared bottom legend for providers
    provider_handles = [
        mlines.Line2D([], [], color=provider_colors[p], linewidth=2, label=p)
        for p in providers
    ]
    fig.legend(handles=provider_handles, loc='lower center',
               ncol=len(providers), fontsize=6, frameon=False,
               bbox_to_anchor=(0.5, -0.16), title="Providers",
               title_fontproperties={'size': 7, 'weight': 'bold'})

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Evaluator dashboard saved to: {save_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig


# =============================================================================
# Summary Dashboard
# =============================================================================

def plot_summary_dashboard(
    history: list,
    save_path: Optional[str] = None,
    show: bool = True,
    figsize: tuple = (6.75, 4.50),
    metadata: Optional[dict] = None,
) -> Optional[plt.Figure]:
    """
    Create a comprehensive summary dashboard showing all ecosystem dynamics.

    Layout (3x3):
    Row 1: Scores | True vs Believed | Investment Portfolio
    Row 2: Eval Engineering | Validity | Score-Capability Gap
    Row 3: Consumer Satisfaction | Market Share | Interventions

    Args:
        history: List of round data dicts
        save_path: Path to save figure
        show: Whether to display
        figsize: Figure size
        metadata: Optional dict with experiment metadata (n_rounds, llm_mode,
                  n_consumers, n_policymakers, etc.)

    Returns:
        matplotlib Figure or None
    """
    if not history:
        print("No history to plot")
        return None

    providers = get_providers(history)
    provider_colors = get_provider_colors(providers)
    inv_colors = get_investment_colors()

    rounds = [h["round"] for h in history]
    has_consumers = any("consumer_data" in h for h in history)
    has_policymakers = any("policymaker_data" in h for h in history)

    fig, axes = plt.subplots(3, 3, figsize=figsize)
    has_funders = any("funder_data" in h for h in history)

    fig.suptitle("Evaluation Ecosystem Summary Dashboard", fontweight='bold')

    # Detect provider first rounds for NaN/star markers
    provider_first_round = {}
    for h in history:
        for p in h.get("scores", {}):
            if p not in provider_first_round:
                provider_first_round[p] = h["round"]
    first_round_min = min(rounds) if rounds else 0

    # =========== ROW 1 ===========

    # --- Panel 1,1: Scores Over Time ---
    ax = axes[0, 0]
    for provider in providers:
        fr = provider_first_round.get(provider, first_round_min)
        scores = [h["scores"].get(provider, float('nan')) if h["round"] >= fr else float('nan')
                  for h in history]
        ax.plot(rounds, scores, '-', color=provider_colors[provider],
                linewidth=1.5, alpha=0.8)
    ax.set_ylim(0, 1)
    style_axis(ax, "Benchmark Scores", "Round", "Score", legend=False)

    # --- Panel 1,2: True vs Believed Capability ---
    ax = axes[0, 1]
    for provider in providers:
        fr = provider_first_round.get(provider, first_round_min)
        true_caps = [h["true_capabilities"].get(provider, float('nan')) if h["round"] >= fr
                     else float('nan') for h in history]
        believed_caps = [h["believed_capabilities"].get(provider, float('nan')) if h["round"] >= fr
                         else float('nan') for h in history]
        ax.plot(rounds, true_caps, '-', color=provider_colors[provider], linewidth=1.5)
        ax.plot(rounds, believed_caps, '--', color=provider_colors[provider],
                linewidth=1, alpha=0.5)
    # Line-style legend only
    style_handles = [
        mlines.Line2D([], [], color='gray', linestyle='-', linewidth=1.5, label='True'),
        mlines.Line2D([], [], color='gray', linestyle='--', linewidth=1, alpha=0.5, label='Believed'),
    ]
    ax.legend(handles=style_handles, loc='best', fontsize=5)
    style_axis(ax, "True vs Believed Capability", "Round", "Capability", legend=False)

    # --- Panel 1,3: Investment Portfolio (first provider) ---
    ax = axes[0, 2]
    investment_types = ["fundamental_research", "training_optimization",
                        "evaluation_engineering", "safety_alignment"]
    if providers:
        provider = providers[0]
        bottom = np.zeros(len(rounds))
        for inv_type in investment_types:
            values = np.array(extract_investment(history, provider, inv_type))
            ax.fill_between(rounds, bottom, bottom + values, alpha=0.7,
                           label=inv_type.replace("_", " ").title()[:12],
                           color=inv_colors[inv_type])
            bottom += values
    ax.set_ylim(0, 1.05)
    ax.set_title(f"Investment ({providers[0] if providers else 'N/A'})",
                 fontweight='bold')
    ax.set_xlabel("Round")
    ax.legend(loc='upper right', fontsize=4)

    # =========== ROW 2 ===========

    # --- Panel 2,1: Evaluation Engineering ---
    ax = axes[1, 0]
    for provider in providers:
        fr = provider_first_round.get(provider, first_round_min)
        eval_eng = extract_investment(history, provider, "evaluation_engineering")
        plot_vals = [v if rounds[i] >= fr else float('nan') for i, v in enumerate(eval_eng)]
        ax.plot(rounds, plot_vals, '-', color=provider_colors[provider], linewidth=1.5)
    ax.set_ylim(0, 1)
    style_axis(ax, "Evaluation Engineering", "Round", "Investment", legend=False)

    # --- Panel 2,2: Validity Correlation ---
    ax = axes[1, 1]

    per_benchmark = compute_per_benchmark_rolling_correlation(history)

    if per_benchmark:
        benchmark_names = sorted(per_benchmark.keys())
        bm_colors = list(get_provider_colors(benchmark_names).values())

        for i, benchmark in enumerate(benchmark_names):
            bm_rounds, bm_corrs = per_benchmark[benchmark]
            ax.plot(bm_rounds, bm_corrs, '-', color=bm_colors[i],
                    linewidth=1.2)

        validity_rounds, validity_values = compute_rolling_correlation(history)
        if validity_values:
            ax.plot(validity_rounds, validity_values, '--', color='black',
                   linewidth=1.5, alpha=0.5)
    else:
        validity_rounds, validity_values = compute_rolling_correlation(history)
        if validity_values:
            ax.plot(validity_rounds, validity_values, '-', color='#2A9D8F',
                    linewidth=2)

    ax.set_ylim(-0.2, 1.0)
    style_axis(ax, "Benchmark Validity", "Round", "Correlation", legend=False)

    # --- Panel 2,3: Score - Capability Gap ---
    ax = axes[1, 2]
    for provider in providers:
        fr = provider_first_round.get(provider, first_round_min)
        scores = np.array([h["scores"].get(provider, float('nan')) if h["round"] >= fr
                           else float('nan') for h in history], dtype=float)
        true_caps = np.array([h["true_capabilities"].get(provider, float('nan')) if h["round"] >= fr
                              else float('nan') for h in history], dtype=float)
        gap = scores - true_caps
        ax.plot(rounds, gap, '-', color=provider_colors[provider], linewidth=1.5)
    style_axis(ax, "Score - Capability Gap", "Round", "Gap", legend=False)

    # =========== ROW 3 ===========

    # --- Panel 3,1: Consumer Satisfaction ---
    ax = axes[2, 0]
    if has_consumers:
        consumer_rounds = [h["round"] for h in history if "consumer_data" in h]
        avg_satisfaction = [h["consumer_data"].get("avg_satisfaction", 0)
                          for h in history if "consumer_data" in h]
        if consumer_rounds:
            ax.plot(consumer_rounds, avg_satisfaction, '-', color='#2A9D8F',
                    linewidth=2)
    ax.set_ylim(0, 1)
    style_axis(ax, "Consumer Satisfaction", "Round", "Satisfaction", legend=False)
    if not has_consumers:
        ax.text(0.5, 0.5, "No consumer data", ha='center', va='center',
                transform=ax.transAxes, alpha=0.5)

    # --- Panel 3,2: Market Share ---
    ax = axes[2, 1]
    if has_consumers:
        consumer_rounds_data = [h for h in history if "consumer_data" in h]
        if consumer_rounds_data:
            market_share = {p: [] for p in providers}
            plot_rounds = [h["round"] for h in consumer_rounds_data]
            for h in consumer_rounds_data:
                shares = h["consumer_data"].get("market_shares", {})
                for p in providers:
                    market_share[p].append(shares.get(p, 0))

            bottom = np.zeros(len(plot_rounds))
            for provider in providers:
                values = np.array(market_share[provider])
                ax.fill_between(plot_rounds, bottom, bottom + values, alpha=0.7,
                               color=provider_colors[provider])
                bottom += values
            ax.set_ylim(0, 1.05)
    style_axis(ax, "Market Share", "Round", "Share", legend=False)
    if not has_consumers:
        ax.text(0.5, 0.5, "No consumer data", ha='center', va='center',
                transform=ax.transAxes, alpha=0.5)

    # --- Panel 3,3: Policymaker Interventions ---
    ax = axes[2, 2]
    if has_policymakers:
        intervention_rounds = []
        for h in history:
            if "policymaker_data" in h and h["policymaker_data"].get("interventions"):
                intervention_rounds.append(h["round"])

        intervention_indicator = [1 if r in intervention_rounds else 0 for r in rounds]
        colors_bar = ['#E63946' if v else '#EEEEEE' for v in intervention_indicator]
        ax.bar(rounds, [1]*len(rounds), color=colors_bar, alpha=0.7)
        ax.set_ylim(0, 1.5)
        ax.set_yticks([])
        ax.text(0.95, 0.95, f"Total: {len(intervention_rounds)}", transform=ax.transAxes,
                ha='right', va='top', fontweight='bold')
    style_axis(ax, "Regulatory Interventions", "Round", "", legend=False)
    if not has_policymakers:
        ax.text(0.5, 0.5, "No policymaker data", ha='center', va='center',
                transform=ax.transAxes, alpha=0.5)

    # Shared bottom legend for providers
    provider_handles = [
        mlines.Line2D([], [], color=provider_colors[p], linewidth=2, label=p)
        for p in providers
    ]
    fig.legend(handles=provider_handles, loc='lower center',
               ncol=len(providers), fontsize=5, frameon=False,
               bbox_to_anchor=(0.5, -0.06), title="Providers",
               title_fontproperties={'size': 6, 'weight': 'bold'})


    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Summary dashboard saved to: {save_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig


# =============================================================================
# Individual Plot Functions (for backwards compatibility and flexibility)
# =============================================================================

def plot_scores_over_time(
    history: list,
    save_path: Optional[str] = None,
    show: bool = True,
) -> Optional[plt.Figure]:
    """Plot benchmark scores over time."""
    if not history:
        return None

    providers = get_providers(history)
    provider_colors = get_provider_colors(providers)
    rounds = [h["round"] for h in history]

    fig, ax = plt.subplots(figsize=(3.25, 1.95))

    for provider in providers:
        scores = [h["scores"].get(provider) for h in history]
        ax.plot(rounds, scores, 'o-', label=provider, color=provider_colors[provider],
                markersize=4, linewidth=2)

    ax.set_ylim(0, 1)
    style_axis(ax, "Benchmark Scores Over Time", "Round", "Score")


    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig


def plot_validity_over_time(
    history: list,
    window_size: int = 5,
    save_path: Optional[str] = None,
    show: bool = True,
) -> Optional[plt.Figure]:
    """Plot rolling validity correlation, broken down by benchmark if available."""
    if len(history) < window_size:
        print(f"Need at least {window_size} rounds")
        return None

    # Try per-benchmark correlations first
    per_benchmark = compute_per_benchmark_rolling_correlation(history, window_size)

    fig, ax = plt.subplots(figsize=(3.25, 1.63))

    if per_benchmark:
        # Plot per-benchmark correlations
        benchmark_names = sorted(per_benchmark.keys())
        colors = list(get_provider_colors(benchmark_names).values())

        for i, benchmark in enumerate(benchmark_names):
            rounds, correlations = per_benchmark[benchmark]
            ax.plot(rounds, correlations, '-', label=_tex_escape(benchmark),
                   color=colors[i], linewidth=1.5)

        # Also plot overall correlation as a thicker dashed line
        validity_rounds, validity_values = compute_rolling_correlation(history, window_size)
        if validity_values:
            ax.plot(validity_rounds, validity_values, '--', color='black',
                   linewidth=2, alpha=0.6, label='Overall')

        title = f"Benchmark Validity by Benchmark (window={window_size})"
    else:
        # Fallback to overall correlation
        validity_rounds, validity_values = compute_rolling_correlation(history, window_size)
        if not validity_values:
            return None

        ax.plot(validity_rounds, validity_values, '-', color='#2A9D8F',
                linewidth=1.5, label='Overall')
        title = f"Benchmark Validity Over Time (window={window_size})"

    ax.set_ylim(-0.2, 1.0)

    style_axis(ax, title, "Round", r"Correlation ($\rho$, Score vs True Capability)")


    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig


def plot_investment_comparison(
    history: list,
    save_path: Optional[str] = None,
    show: bool = True,
) -> Optional[plt.Figure]:
    """Plot investment portfolio comparison across all providers."""
    if not history:
        return None

    providers = get_providers(history)
    provider_colors = get_provider_colors(providers)
    inv_colors = get_investment_colors()
    investment_types = list(inv_colors.keys())
    rounds = [h["round"] for h in history]
    first_round_min = min(rounds) if rounds else 0

    # Detect each provider's first round
    provider_first_round = {}
    for h in history:
        for p in h.get("scores", {}):
            if p not in provider_first_round:
                provider_first_round[p] = h["round"]

    fig, axes = plt.subplots(2, 2, figsize=(6.75, 4.82))
    fig.suptitle("Investment Comparison Across Providers", fontweight='bold')

    for idx, inv_type in enumerate(investment_types):
        ax = axes[idx // 2, idx % 2]
        for provider in providers:
            values = extract_investment(history, provider, inv_type)
            # Use NaN for rounds before provider exists
            fr = provider_first_round.get(provider, first_round_min)
            plot_vals = [v if rounds[i] >= fr else float('nan')
                         for i, v in enumerate(values)]
            ax.plot(rounds, plot_vals, '-', color=provider_colors[provider],
                    markersize=2, linewidth=1.5)
            # Star marker at entry
            if fr > first_round_min and fr in rounds:
                entry_idx = rounds.index(fr)
                if not np.isnan(plot_vals[entry_idx]):
                    ax.plot(fr, plot_vals[entry_idx], '*',
                            color=provider_colors[provider],
                            markersize=10, zorder=5)
        ax.set_ylim(0, 1)
        style_axis(ax, inv_type.replace("_", " ").title(), "Round", "Investment", legend=False)

    # Shared bottom legend
    provider_handles = [
        mlines.Line2D([], [], color=provider_colors[p], linewidth=2, label=p)
        for p in providers
    ]
    fig.legend(handles=provider_handles, loc='lower center',
               ncol=len(providers), fontsize=6, frameon=False,
               bbox_to_anchor=(0.5, -0.06), title="Providers",
               title_fontproperties={'size': 7, 'weight': 'bold'})

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig


# =============================================================================
# Funder Dashboard
# =============================================================================

def plot_funder_dashboard(
    history: list,
    save_path: Optional[str] = None,
    show: bool = True,
    figsize: tuple = (6.75, 3.38),
) -> Optional[plt.Figure]:
    """
    Create a dashboard for Funder actors.

    Panels:
    1. Funding Allocations Over Time (stacked area)
    2. Provider Funding Multipliers Over Time
    3. Total Funding Deployed
    4. Funder ROI Tracking (inferred from provider performance)

    Args:
        history: List of round data dicts
        save_path: Path to save figure
        show: Whether to display
        figsize: Figure size

    Returns:
        matplotlib Figure or None
    """
    funder_rounds = [h for h in history if "funder_data" in h]
    if not funder_rounds:
        print("No funder data to plot")
        return None

    providers = get_providers(history)
    provider_colors = get_provider_colors(providers)

    rounds = [h["round"] for h in funder_rounds]

    fig, axes = plt.subplots(2, 3, figsize=figsize)
    fig.suptitle("Funder Dashboard", fontweight='bold')

    # --- Panel 1: Funding Allocations Over Time (stacked area) ---
    ax1 = axes[0, 0]

    # Aggregate funding per provider across all funders
    funding_per_provider = {p: [] for p in providers}
    for h in funder_rounds:
        fd = h["funder_data"]
        allocations = fd.get("allocations", {})
        # Sum across all funders
        provider_totals = {p: 0 for p in providers}
        for funder_allocs in allocations.values():
            if isinstance(funder_allocs, dict):
                for provider, amount in funder_allocs.items():
                    if provider in provider_totals:
                        provider_totals[provider] += amount
        for p in providers:
            funding_per_provider[p].append(provider_totals.get(p, 0))

    # Stacked area chart
    bottom = np.zeros(len(rounds))
    for provider in providers:
        values = np.array(funding_per_provider[provider])
        # Convert to thousands for readability
        values_k = values / 1000
        ax1.fill_between(rounds, bottom, bottom + values_k, alpha=0.7,
                        color=provider_colors[provider])
        bottom += values_k

    style_axis(ax1, "Funding Allocations Over Time", "Round", r"Funding (\$K)", legend=False)

    # --- Panel 2: Provider Funding Multipliers Over Time ---
    ax2 = axes[0, 1]

    for provider in providers:
        multipliers = []
        for h in funder_rounds:
            fd = h["funder_data"]
            mult = fd.get("funding_multipliers", {}).get(provider, 1.0)
            multipliers.append(mult)
        ax2.plot(rounds, multipliers, '-', color=provider_colors[provider],
                 linewidth=1.5)

    ax2.set_ylim(0.9, 2.1)
    style_axis(ax2, "Funding Multipliers Over Time", "Round", "Multiplier", legend=False)

    # --- Panel 3: Total Funding Deployed ---
    ax3 = axes[1, 0]

    total_funding = [h["funder_data"].get("total_funding", 0) / 1000 for h in funder_rounds]
    ax3.fill_between(rounds, 0, total_funding, alpha=0.3, color='#2A9D8F')
    ax3.plot(rounds, total_funding, '-', color='#2A9D8F', linewidth=1.5)
    style_axis(ax3, "Total Funding Deployed", "Round", r"Total Funding (\$K)", legend=False)

    # --- Panel 4: Provider Performance vs Funding (scatter) ---
    ax4 = axes[1, 1]

    # For each provider, plot funding received vs capability growth
    for provider in providers:
        # Get average funding multiplier
        avg_multiplier = np.mean([
            h["funder_data"].get("funding_multipliers", {}).get(provider, 1.0)
            for h in funder_rounds
        ])

        # Get capability growth
        if len(history) >= 2:
            initial_cap = history[0]["true_capabilities"].get(provider, 0.5)
            final_cap = history[-1]["true_capabilities"].get(provider, 0.5)
            cap_growth = final_cap - initial_cap
        else:
            cap_growth = 0

        ax4.scatter(avg_multiplier, cap_growth, s=60, color=provider_colors[provider],
                   alpha=0.8, zorder=3)

    style_axis(ax4, "Funding Impact on Capability Growth", "Avg Funding Multiplier", "Capability Growth", legend=False)

    # --- Panel 5: Per-Funder Top Allocation ---
    ax5 = axes[0, 2]
    funder_names = set()
    for h in funder_rounds:
        funder_names.update(h["funder_data"].get("allocations", {}).keys())
    funder_names = sorted(funder_names)

    funder_line_colors = list(get_provider_colors(funder_names).values())
    for i, funder in enumerate(funder_names):
        top_allocs = []
        for h in funder_rounds:
            allocs = h["funder_data"].get("allocations", {}).get(funder, {})
            if isinstance(allocs, dict) and allocs:
                top_allocs.append(max(allocs.values()) / 1_000_000)
            else:
                top_allocs.append(0)
        ax5.plot(rounds, top_allocs, '-', label=_tex_escape(funder), color=funder_line_colors[i],
                 linewidth=1.5)
    ax5.legend(loc='best', fontsize=5)
    style_axis(ax5, "Per-Funder Top Allocation", "Round", r"Top Allocation (\$M)", legend=False)

    # --- Panel 6: Score Momentum (3-Round Avg Delta) ---
    ax6 = axes[1, 2]
    for provider in providers:
        provider_hist = [(h["round"], h["scores"][provider]) for h in history if provider in h["scores"]]
        if len(provider_hist) < 2:
            continue
        p_rounds_momentum = [r for r, _ in provider_hist]
        scores = [s for _, s in provider_hist]
        # Compute rolling 3-round average of score deltas
        deltas = [scores[i] - scores[i - 1] for i in range(1, len(scores))]
        window = 3
        if len(deltas) >= window:
            momentum = []
            momentum_rounds = []
            for i in range(window - 1, len(deltas)):
                avg_delta = np.mean(deltas[i - window + 1:i + 1])
                momentum.append(avg_delta)
                # Round index corresponds to the end of the window
                momentum_rounds.append(p_rounds_momentum[i + 1])
            ax6.plot(momentum_rounds, momentum, '-',
                     color=provider_colors[provider], linewidth=1.5)
    style_axis(ax6, "Score Momentum (3-Round Avg Delta)", "Round", "Avg Delta", legend=False)

    # Shared provider legend at the bottom
    provider_handles = [
        mlines.Line2D([], [], color=provider_colors[p], linewidth=2, label=p)
        for p in providers
    ]
    fig.legend(handles=provider_handles, loc='lower center',
               ncol=len(providers), fontsize=6, frameon=False,
               bbox_to_anchor=(0.5, -0.08), title="Providers",
               title_fontproperties={'size': 7, 'weight': 'bold'})

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Funder dashboard saved to: {save_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig


# =============================================================================
# Media Dashboard
# =============================================================================

def plot_media_dashboard(
    history: list,
    save_path: Optional[str] = None,
    show: bool = True,
    figsize: tuple = (6.75, 4.82),
) -> Optional[plt.Figure]:
    """
    Create a dashboard for Media coverage.

    Panels:
    1. Media Sentiment Over Time (line + fill)
    2. Headlines by Category (stacked bar)
    3. Provider Attention Heatmap
    4. Risk Signals Per Round

    Args:
        history: List of round data dicts
        save_path: Path to save figure
        show: Whether to display
        figsize: Figure size

    Returns:
        matplotlib Figure or None
    """
    media_rounds = [h for h in history if "media_data" in h]
    if not media_rounds:
        print("No media data to plot")
        return None

    providers = get_providers(history)
    rounds = [h["round"] for h in media_rounds]

    fig, axes = plt.subplots(2, 2, figsize=figsize, layout="constrained")
    fig.suptitle("Media Dashboard", fontweight='bold')

    # --- Panel 1: Media Sentiment Over Time ---
    ax1 = axes[0, 0]
    sentiments = [h["media_data"].get("sentiment", 0) for h in media_rounds]
    ax1.plot(rounds, sentiments, '-', color='#457B9D', linewidth=1.5)
    sentiments_arr = np.array(sentiments)
    rounds_arr = np.array(rounds)
    ax1.fill_between(rounds_arr, 0, sentiments_arr,
                     where=sentiments_arr >= 0, alpha=0.2, color='green',
                     interpolate=True)
    ax1.fill_between(rounds_arr, 0, sentiments_arr,
                     where=sentiments_arr < 0, alpha=0.2, color='red',
                     interpolate=True)
    ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.5, alpha=0.3)
    style_axis(ax1, "Media Sentiment Over Time", "Round", "Sentiment", legend=False)

    # --- Panel 2: Headlines by Category (stacked bar) ---
    ax2 = axes[0, 1]
    categories = ["leader_change", "score_surge", "regulatory", "funding",
                  "consumer", "benchmark", "other"]
    cat_colors = {
        "leader_change": "#E63946", "score_surge": "#457B9D",
        "regulatory": "#6A4C93", "funding": "#2A9D8F",
        "consumer": "#F4A261", "benchmark": "#E9C46A", "other": "#CCCCCC",
    }
    # Count categories per round
    cat_counts = {cat: [] for cat in categories}
    for h in media_rounds:
        headlines = h["media_data"].get("headlines", [])
        round_cats = {cat: 0 for cat in categories}
        for headline in headlines:
            cat = categorize_headline(headline)
            round_cats[cat] += 1
        for cat in categories:
            cat_counts[cat].append(round_cats[cat])

    bottom = np.zeros(len(rounds))
    for cat in categories:
        values = np.array(cat_counts[cat])
        ax2.bar(rounds, values, bottom=bottom, label=_tex_escape(cat.replace("_", " ").title()),
                color=cat_colors[cat], alpha=0.8, width=0.8)
        bottom += values
    ax2.legend(loc='upper right', fontsize=5)
    style_axis(ax2, "Headlines by Category", "Round", "Count", legend=False)

    # --- Panel 3: Provider Attention Heatmap ---
    ax3 = axes[1, 0]
    attention_matrix = []
    for p in providers:
        row = []
        for h in media_rounds:
            attn = h["media_data"].get("provider_attention", {})
            row.append(attn.get(p, 0))
        attention_matrix.append(row)
    attention_matrix = np.array(attention_matrix)

    if attention_matrix.size > 0:
        im = ax3.imshow(attention_matrix, aspect='auto', cmap='YlOrRd',
                        vmin=0, vmax=1)
        ax3.set_yticks(range(len(providers)))
        ax3.set_yticklabels(providers, fontsize=6)
        ax3.set_xlabel("Round Index")
        fig.colorbar(im, ax=ax3, fraction=0.046, pad=0.04)
    ax3.set_title("Provider Attention Heatmap", fontweight='bold')

    # --- Panel 4: Risk Signals Per Round ---
    ax4 = axes[1, 1]
    risk_counts = [len(h["media_data"].get("risk_signals", [])) for h in media_rounds]
    bar_colors = ['#E63946' if c > 0 else '#CCCCCC' for c in risk_counts]
    ax4.bar(rounds, risk_counts, color=bar_colors, alpha=0.8)
    total_risks = sum(risk_counts)
    ax4.text(0.95, 0.95, f"Total: {total_risks}", transform=ax4.transAxes,
             ha='right', va='top', fontsize=8, fontweight='bold')
    style_axis(ax4, "Risk Signals Per Round", "Round", "Count", legend=False)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Media dashboard saved to: {save_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig


# =============================================================================
# Incident Dashboard
# =============================================================================

def plot_incident_dashboard(
    history: list,
    save_path: Optional[str] = None,
    show: bool = True,
    figsize: tuple = (6.75, 4.22),
) -> Optional[plt.Figure]:
    """
    Create a comprehensive dashboard for AI safety incidents.

    Panels:
    1. Incident Timeline by Provider
    2. Incident Severity Distribution
    3. Incident Category Breakdown
    4. Provider Safety vs Incident Rate
    5. Incidents per Round
    6. Provider Incident Comparison

    Args:
        history: List of round data dicts
        save_path: Path to save figure
        show: Whether to display
        figsize: Figure size

    Returns:
        matplotlib Figure or None
    """
    # Extract incidents from history
    all_incidents = []
    for h in history:
        if "incidents" in h and h["incidents"]:
            for inc in h["incidents"]:
                inc_data = inc.copy()
                inc_data["round"] = h["round"]
                all_incidents.append(inc_data)

    if not all_incidents:
        print("No incidents to plot")
        return None

    providers = get_providers(history)
    rounds = [h["round"] for h in history]

    fig, axes = plt.subplots(3, 2, figsize=figsize)
    fig.suptitle("AI Safety Incident Dashboard", fontweight='bold')

    provider_colors = get_provider_colors(providers)

    # --- Panel 1: Incident Timeline by Provider ---
    ax1 = axes[0, 0]
    for inc in all_incidents:
        severity_markers = {"minor": "o", "moderate": "s", "major": "^", "critical": "X"}
        severity_sizes = {"minor": 20, "moderate": 40, "major": 60, "critical": 90}
        marker = severity_markers.get(inc["severity"], "o")
        size = severity_sizes.get(inc["severity"], 30)
        color = provider_colors.get(inc["provider"], "#666666")
        ax1.scatter(inc["round"], providers.index(inc["provider"]),
                   marker=marker, s=size, color=color, alpha=0.7, edgecolors='black', linewidth=0.5)

    ax1.set_yticks(range(len(providers)))
    ax1.set_yticklabels(providers, fontsize=5)
    ax1.set_xlim(min(rounds)-1, max(rounds)+1)

    legend_elements = [
        mlines.Line2D([0], [0], marker='o', color='w', markerfacecolor='gray',
                     markersize=4, label='Minor', markeredgecolor='black'),
        mlines.Line2D([0], [0], marker='s', color='w', markerfacecolor='gray',
                     markersize=5, label='Moderate', markeredgecolor='black'),
        mlines.Line2D([0], [0], marker='^', color='w', markerfacecolor='gray',
                     markersize=6, label='Major', markeredgecolor='black'),
        mlines.Line2D([0], [0], marker='X', color='w', markerfacecolor='gray',
                     markersize=7, label='Critical', markeredgecolor='black'),
    ]
    ax1.legend(handles=legend_elements, loc='upper right', fontsize=5, ncol=2)
    style_axis(ax1, "Incident Timeline by Provider", "Round", "", legend=False)

    # --- Panel 2: Severity Distribution ---
    ax2 = axes[0, 1]
    severities = [inc["severity"] for inc in all_incidents]
    severity_counts = {
        "minor": severities.count("minor"),
        "moderate": severities.count("moderate"),
        "major": severities.count("major"),
        "critical": severities.count("critical"),
    }

    severity_colors = {"minor": "#90EE90", "moderate": "#FFD700", "major": "#FF8C00", "critical": "#DC143C"}
    labels = [f"{k.capitalize()} ({v})" for k, v in severity_counts.items() if v > 0]
    values = [v for v in severity_counts.values() if v > 0]
    pie_colors = [severity_colors[k] for k, v in severity_counts.items() if v > 0]

    if values:
        ax2.pie(values, labels=[_tex_escape(l) for l in labels],
                autopct=_tex_autopct, colors=pie_colors,
                textprops={'fontsize': 6}, startangle=90)
    ax2.set_title("Severity Distribution", fontweight='bold')

    # --- Panel 3: Category Breakdown ---
    ax3 = axes[1, 0]
    categories = [inc["category"] for inc in all_incidents]
    unique_categories = list(set(categories))
    category_counts = [categories.count(c) for c in unique_categories]

    category_colors_map = {
        "healthcare_harm": "#E63946", "security_breach": "#F77F00",
        "bias_discrimination": "#FCBF49", "safety_failure": "#EAE2B7",
        "misinformation": "#457B9D", "misuse": "#A8DADC",
    }

    bar_colors = [category_colors_map.get(c, "#666666") for c in unique_categories]
    ax3.barh([_tex_escape(c.replace("_", " ")) for c in unique_categories], category_counts,
             color=bar_colors, alpha=0.8)

    for i, count in enumerate(category_counts):
        ax3.text(count + 0.1, i, str(count), va='center', fontsize=6, fontweight='bold')

    style_axis(ax3, "Incidents by Category", "Count", "", legend=False)

    # --- Panel 4: Safety Investment vs Incidents ---
    ax4 = axes[1, 1]

    provider_incidents = {p: 0 for p in providers}
    for inc in all_incidents:
        provider_incidents[inc["provider"]] += 1

    provider_safety = {}
    for p in providers:
        safety_values = [h["strategies"][p]["safety_alignment"]
                        for h in history if p in h["strategies"]]
        provider_safety[p] = np.mean(safety_values) if safety_values else 0

    x_vals = [provider_safety[p] for p in providers]
    y_vals = [provider_incidents[p] for p in providers]
    scatter_colors = [provider_colors[p] for p in providers]

    ax4.scatter(x_vals, y_vals, s=60, c=scatter_colors, alpha=0.7, edgecolors='black', linewidth=0.5)

    if len(x_vals) > 1:
        z = np.polyfit(x_vals, y_vals, 1)
        p_fit = np.poly1d(z)
        x_trend = np.linspace(min(x_vals), max(x_vals), 100)
        ax4.plot(x_trend, p_fit(x_trend), "--", color='gray', alpha=0.5, linewidth=1.5)

    style_axis(ax4, "Safety Investment vs Incidents",
               "Avg Safety Alignment", "Total Incidents", legend=False)

    # --- Panel 5: Incidents per Round ---
    ax5 = axes[2, 0]
    incidents_per_round = {r: 0 for r in rounds}
    for inc in all_incidents:
        incidents_per_round[inc["round"]] += 1

    incident_counts = [incidents_per_round[r] for r in rounds]
    ax5.bar(rounds, incident_counts, color='#E63946', alpha=0.7)
    style_axis(ax5, "Incidents per Round", "Round", "Count", legend=False)

    # --- Panel 6: Total Incidents by Provider ---
    ax6 = axes[2, 1]
    provider_names_list = list(provider_incidents.keys())
    incident_counts_by_provider = list(provider_incidents.values())
    bar_colors_p = [provider_colors[p] for p in provider_names_list]

    bars = ax6.bar(range(len(provider_names_list)), incident_counts_by_provider,
                   color=bar_colors_p, alpha=0.8)
    ax6.set_xticks(range(len(provider_names_list)))
    ax6.set_xticklabels(provider_names_list, rotation=45, ha='right', fontsize=5)

    for bar, count in zip(bars, incident_counts_by_provider):
        if count > 0:
            ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(count), ha='center', va='bottom', fontsize=6, fontweight='bold')

    style_axis(ax6, "Total Incidents by Provider", "", "Count", legend=False)


    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Incident dashboard saved to: {save_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig


# =============================================================================
# Data Extraction Helpers
# =============================================================================

def compute_incident_severity_score(severity: str) -> int:
    """Convert incident severity to numeric cost score for aggregation."""
    return {"minor": 1, "moderate": 5, "major": 20, "critical": 100}.get(severity, 1)


def extract_incident_impacts(history: list) -> dict:
    """Extract incident cascade effects across actors per round."""
    rounds = [h["round"] for h in history]
    satisfaction = []
    media_sentiment = []
    intervention_counts = []
    incident_rounds = set()

    for h in history:
        cd = h.get("consumer_data", {})
        satisfaction.append(cd.get("avg_satisfaction", None))

        md = h.get("media_data", {})
        media_sentiment.append(md.get("sentiment", None))

        pd = h.get("policymaker_data", {})
        intervention_counts.append(len(pd.get("interventions", [])))

        if h.get("incidents"):
            incident_rounds.add(h["round"])

    return {
        "rounds": rounds,
        "satisfaction": satisfaction,
        "media_sentiment": media_sentiment,
        "intervention_counts": intervention_counts,
        "incident_rounds": sorted(incident_rounds),
    }


def extract_evaluator_business_metrics(history: list) -> dict:
    """Extract evaluator-as-company financial metrics from history."""
    biz_rounds = [h for h in history if "evaluator_business_metrics" in h]
    return {
        "rounds": [h["round"] for h in biz_rounds],
        "budget": [h["evaluator_business_metrics"]["budget"] for h in biz_rounds],
        "base_funding": [h["evaluator_business_metrics"].get("base_funding", 0) for h in biz_rounds],
        "service_revenue": [h["evaluator_business_metrics"].get("service_revenue", 0) for h in biz_rounds],
        "premium_providers": [h["evaluator_business_metrics"].get("premium_providers", []) for h in biz_rounds],
        "trial_counts": [h["evaluator_business_metrics"].get("trial_counts", {}) for h in biz_rounds],
    }


def extract_trial_counts(history: list) -> dict:
    """Extract n_trials per provider per round."""
    biz_rounds = [h for h in history if "evaluator_business_metrics" in h]
    result = {}
    for h in biz_rounds:
        result[h["round"]] = h["evaluator_business_metrics"].get("trial_counts", {})
    return result


# =============================================================================
# Enhanced Incident Analysis Dashboard
# =============================================================================

def plot_incident_analysis_dashboard(
    history: list,
    save_path: Optional[str] = None,
    show: bool = True,
    figsize: tuple = (6.75, 5.5),
) -> Optional[plt.Figure]:
    """
    Advanced incident analysis dashboard with causal and impact panels.

    Panels (3x2):
    1. Safety Investment vs Incident Rate (correlation)
    2. Gaming Gap vs Incidents
    3. Incident Impact Timeline (cascade: satisfaction, sentiment)
    4. Sector-Specific Incidents Heatmap
    5. Incident-Driven Interventions Timeline
    6. Cumulative Incident Cost by Provider
    """
    all_incidents = []
    for h in history:
        if "incidents" in h and h["incidents"]:
            for inc in h["incidents"]:
                ic = inc.copy()
                ic["round"] = h["round"]
                all_incidents.append(ic)

    if not all_incidents:
        return None

    providers = get_providers(history)
    provider_colors = get_provider_colors(providers)
    rounds = [h["round"] for h in history]

    fig, axes = plt.subplots(3, 2, figsize=figsize)
    fig.suptitle("AI Safety Incident Analysis Dashboard", fontweight='bold')

    # --- Panel 1: Safety Investment vs Incident Rate ---
    ax1 = axes[0, 0]
    for p in providers:
        safety_vals = [
            h["strategies"][p].get("safety_alignment", 0)
            for h in history if p in h.get("strategies", {})
        ]
        avg_safety = np.mean(safety_vals) if safety_vals else 0
        p_incidents = [inc for inc in all_incidents if inc["provider"] == p]
        ax1.scatter(avg_safety, len(p_incidents),
                    color=provider_colors[p], s=60, zorder=3)

    # Trend line
    xs, ys = [], []
    for p in providers:
        safety_vals = [h["strategies"][p].get("safety_alignment", 0)
                       for h in history if p in h.get("strategies", {})]
        xs.append(np.mean(safety_vals) if safety_vals else 0)
        ys.append(len([inc for inc in all_incidents if inc["provider"] == p]))
    if len(xs) > 1:
        z = np.polyfit(xs, ys, 1)
        pf = np.poly1d(z)
        x_line = np.linspace(min(xs), max(xs), 50)
        ax1.plot(x_line, pf(x_line), '--', color='gray', alpha=0.5)
    style_axis(ax1, "Safety Investment vs Incidents",
               "Avg Safety Alignment", "Total Incidents", legend=False)

    # --- Panel 2: Gaming Gap vs Incidents ---
    ax2 = axes[0, 1]
    for p in providers:
        p_incidents = [inc for inc in all_incidents if inc["provider"] == p]
        if p_incidents:
            avg_gap = np.mean([inc.get("gaming_gap_at_time", 0) for inc in p_incidents])
        else:
            avg_gap = np.mean([
                max(0, h["scores"].get(p, 0) - h["true_capabilities"].get(p, 0))
                for h in history if "scores" in h and "true_capabilities" in h
            ])
        ax2.scatter(avg_gap, len(p_incidents),
                    color=provider_colors[p], s=60, zorder=3)
    style_axis(ax2, "Gaming Gap vs Incidents",
               "Avg Score - Capability", "Total Incidents", legend=False)

    # --- Panel 3: Incident Impact Timeline ---
    ax3 = axes[1, 0]
    impacts = extract_incident_impacts(history)
    r = impacts["rounds"]

    sat = [s if s is not None else float('nan') for s in impacts["satisfaction"]]
    sent = [s if s is not None else float('nan') for s in impacts["media_sentiment"]]

    ax3_twin = ax3.twinx()
    if any(s == s for s in sat):
        ax3.plot(r, sat, color='#457B9D', linewidth=1.5, label='Avg Satisfaction')
    if any(s == s for s in sent):
        ax3_twin.plot(r, sent, color='#E9C46A', linewidth=1.5, linestyle='--', label='Media Sentiment')
        ax3_twin.set_ylabel("Media Sentiment")

    for ir in impacts["incident_rounds"]:
        ax3.axvline(x=ir, color='red', alpha=0.2, linewidth=1)

    ax3.set_xlabel("Round")
    ax3.set_ylabel("Avg Satisfaction")
    ax3.set_title("Incident Impact Timeline", fontweight='bold')

    lines1, labels1 = ax3.get_legend_handles_labels()
    lines2, labels2 = ax3_twin.get_legend_handles_labels()
    ax3.legend(lines1 + lines2, labels1 + labels2, fontsize=5, loc='lower left')

    # --- Panel 4: Sector-Specific Incidents Heatmap ---
    ax4 = axes[1, 1]
    all_sectors = sorted(set(
        s for inc in all_incidents for s in inc.get("affected_sectors", [])
    ))
    if all_sectors:
        heatmap = np.zeros((len(providers), len(all_sectors)))
        for inc in all_incidents:
            if inc["provider"] in providers:
                pi = providers.index(inc["provider"])
                for s in inc.get("affected_sectors", []):
                    if s in all_sectors:
                        si = all_sectors.index(s)
                        heatmap[pi, si] += 1
        im = ax4.imshow(heatmap, aspect='auto', cmap='Reds', interpolation='nearest')
        ax4.set_xticks(range(len(all_sectors)))
        ax4.set_xticklabels(
            [_tex_escape(s.replace('_', ' ')) for s in all_sectors],
            fontsize=5, rotation=45, ha='right'
        )
        ax4.set_yticks(range(len(providers)))
        ax4.set_yticklabels(providers, fontsize=5)
        plt.colorbar(im, ax=ax4, label='Incident Count', shrink=0.8)
    style_axis(ax4, "Sector-Specific Incidents", "", "", legend=False)

    # --- Panel 5: Incident-Driven Interventions Timeline ---
    ax5 = axes[2, 0]
    severity_colors_map = {"minor": "#90EE90", "moderate": "#FFD700",
                           "major": "#FF8C00", "critical": "#DC143C"}

    for inc in all_incidents:
        sc = severity_colors_map.get(inc["severity"], "gray")
        ax5.scatter(inc["round"], -0.2, color=sc, s=40, marker='v',
                    zorder=3, alpha=0.8)

    for h in history:
        pd_data = h.get("policymaker_data", {})
        for iv in pd_data.get("interventions", []):
            ax5.scatter(h["round"], 0.2, color='#9C6644', s=40, marker='^',
                        zorder=3, alpha=0.8)

    ax5.set_yticks([-0.2, 0.2])
    ax5.set_yticklabels(['Incidents', 'Interventions'], fontsize=6)
    ax5.set_xlim(min(rounds) - 0.5, max(rounds) + 0.5)

    legend_elements = [mpatches.Patch(color=c, label=s.capitalize())
                       for s, c in severity_colors_map.items()]
    ax5.legend(handles=legend_elements, fontsize=5, loc='upper right', ncol=2)
    style_axis(ax5, "Incidents vs Interventions", "Round", "", legend=False)

    # --- Panel 6: Cumulative Incident Cost by Provider ---
    ax6 = axes[2, 1]
    for p in providers:
        cumulative = 0
        cum_costs = []
        for r_val in rounds:
            round_inc = [inc for inc in all_incidents if inc["provider"] == p and inc["round"] == r_val]
            cumulative += sum(compute_incident_severity_score(inc["severity"]) for inc in round_inc)
            cum_costs.append(cumulative)
        ax6.plot(rounds, cum_costs, color=provider_colors[p], linewidth=1.5)
    style_axis(ax6, "Cumulative Incident Cost", "Round", "Weighted Cost", legend=False)

    # Shared bottom legend for providers
    provider_handles = [
        mlines.Line2D([], [], color=provider_colors[p], linewidth=2,
                      marker='o', markersize=4, label=p)
        for p in providers
    ]
    fig.legend(handles=provider_handles, loc='lower center',
               ncol=len(providers), fontsize=6, frameon=False,
               bbox_to_anchor=(0.5, -0.06), title="Providers",
               title_fontproperties={'size': 7, 'weight': 'bold'})


    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Incident analysis dashboard saved to: {save_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig


# =============================================================================
# Evaluator Business Dashboard (evaluator-as-company mode)
# =============================================================================

def plot_evaluator_business_dashboard(
    history: list,
    save_path: Optional[str] = None,
    show: bool = True,
    figsize: tuple = (6.75, 4.73),
) -> Optional[plt.Figure]:
    """
    Dashboard for evaluator-as-company business metrics.
    Only renders when evaluator_as_company=True data is present.

    Panels (3x2):
    1. Budget Over Time
    2. Premium Provider Timeline
    3. Trial Counts by Provider (average across rounds)
    4. Revenue Breakdown (base funding vs service revenue)
    5. Premium Access vs Score Improvement
    6. Average Trial Count per Provider
    """
    biz_rounds = [h for h in history if "evaluator_business_metrics" in h]
    if not biz_rounds:
        return None

    providers = get_providers(history)
    provider_colors = get_provider_colors(providers)
    rounds = [h["round"] for h in biz_rounds]

    fig, axes = plt.subplots(3, 2, figsize=figsize)
    fig.suptitle("Evaluator Business Dashboard", fontweight='bold')

    # --- Panel 1: Budget Over Time ---
    ax1 = axes[0, 0]
    budgets = [h["evaluator_business_metrics"]["budget"] for h in biz_rounds]
    ax1.plot(rounds, [b / 1000 for b in budgets], color='#2A9D8F', linewidth=1.5)
    ax1.fill_between(rounds, 0, [b / 1000 for b in budgets], alpha=0.15, color='#2A9D8F')
    style_axis(ax1, "Evaluator Budget Over Time", "Round", r"Budget (\$K)", legend=False)

    # --- Panel 2: Premium Provider Timeline ---
    ax2 = axes[0, 1]
    provider_y = {p: i for i, p in enumerate(providers)}
    for h in biz_rounds:
        r = h["round"]
        premium = h["evaluator_business_metrics"].get("premium_providers", [])
        for p in premium:
            if p in provider_y:
                ax2.scatter(r, provider_y[p], color=provider_colors.get(p, 'gray'),
                           s=40, marker='s', zorder=3)
    ax2.set_yticks(range(len(providers)))
    ax2.set_yticklabels(providers, fontsize=6)
    ax2.set_xlim(min(rounds) - 0.5, max(rounds) + 0.5)
    style_axis(ax2, "Premium Provider Access Timeline", "Round", "", legend=False)

    # --- Panel 3: Revenue Breakdown (stacked area) ---
    ax3 = axes[1, 0]
    base_fundings = [h["evaluator_business_metrics"].get("base_funding", 0) / 1000 for h in biz_rounds]
    svc_revenues = [h["evaluator_business_metrics"].get("service_revenue", 0) / 1000 for h in biz_rounds]
    ax3.fill_between(rounds, 0, base_fundings, alpha=0.5, color='#457B9D', label='Base Funding')
    ax3.fill_between(rounds, base_fundings,
                     [b + s for b, s in zip(base_fundings, svc_revenues)],
                     alpha=0.5, color='#E9C46A', label='Service Revenue')
    style_axis(ax3, "Revenue Breakdown per Round", "Round", r"Revenue (\$K)")

    # --- Panel 4: Trial Counts by Provider (average over all rounds) ---
    ax4 = axes[1, 1]
    trial_sums = {p: [] for p in providers}
    for h in biz_rounds:
        counts = h["evaluator_business_metrics"].get("trial_counts", {})
        for p in providers:
            trial_sums[p].append(counts.get(p, 1))
    avg_trials = {p: np.mean(trial_sums[p]) for p in providers}
    x = np.arange(len(providers))
    bars = ax4.bar(x, [avg_trials[p] for p in providers],
                   color=[provider_colors[p] for p in providers], alpha=0.8)
    ax4.set_xticks(x)
    ax4.set_xticklabels([_tex_escape(p) for p in providers], rotation=45, ha='right', fontsize=6)
    style_axis(ax4, "Average Trial Count per Provider", "", "Avg Trials", legend=False)

    # --- Panel 5: Premium Access vs Score Improvement ---
    ax5 = axes[2, 0]
    premium_counts = {p: 0 for p in providers}
    score_deltas = {p: [] for p in history[0]["scores"].keys() if p in providers}
    for i, h in enumerate(biz_rounds):
        premium = h["evaluator_business_metrics"].get("premium_providers", [])
        for p in premium:
            if p in premium_counts:
                premium_counts[p] += 1
        if i > 0:
            prev_h = biz_rounds[i - 1]
            for p in providers:
                if p in h["scores"] and p in prev_h["scores"]:
                    score_deltas[p].append(h["scores"][p] - prev_h["scores"][p])
    for p in providers:
        avg_delta = np.mean(score_deltas[p]) if score_deltas[p] else 0
        ax5.scatter(premium_counts[p], avg_delta,
                    color=provider_colors[p], s=60, zorder=3)
    style_axis(ax5, "Premium Access vs Avg Score Improvement",
               "Rounds with Premium Access", "Avg Score Delta", legend=False)

    # Shared provider legend
    provider_handles = [
        mlines.Line2D([], [], color=provider_colors[p], linewidth=2,
                      marker='o', markersize=4, label=p)
        for p in providers
    ]
    fig.legend(handles=provider_handles, loc='lower center',
               ncol=len(providers), fontsize=6, frameon=False,
               bbox_to_anchor=(0.5, -0.06), title="Providers",
               title_fontproperties={'size': 7, 'weight': 'bold'})

    # --- Panel 6: Trial Count Heatmap (provider x round) ---
    ax6 = axes[2, 1]
    n_rounds = len(biz_rounds)
    heatmap_data = np.ones((len(providers), n_rounds))
    for j, h in enumerate(biz_rounds):
        counts = h["evaluator_business_metrics"].get("trial_counts", {})
        for i, p in enumerate(providers):
            heatmap_data[i, j] = counts.get(p, 1)
    im = ax6.imshow(heatmap_data, aspect='auto', cmap='YlOrRd',
                    vmin=1, vmax=5, interpolation='nearest')
    ax6.set_yticks(range(len(providers)))
    ax6.set_yticklabels(providers, fontsize=6)
    ax6.set_xlabel("Round Index")
    plt.colorbar(im, ax=ax6, label='N Trials')
    style_axis(ax6, "Trial Count Heatmap", "Round Index", "", legend=False)


    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Evaluator business dashboard saved to: {save_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig


# =============================================================================
# Barrier-to-Entry Dashboard
# =============================================================================

def plot_barrier_to_entry_dashboard(
    history: list,
    save_path: Optional[str] = None,
    show: bool = True,
    figsize: tuple = (6.75, 4.22),
) -> Optional[plt.Figure]:
    """
    Dashboard for barrier-to-entry (BTE) dynamics.

    Panels:
    1. Composite BTE over time (with zone shading and entry annotations)
    2. BTE component breakdown (concentration, capability_gap, funding_lock_in, consumer_lock_in)
    3. Entry event scatter (BTE composite vs capability_gap at entry round)
    4. Market concentration vs provider count (dual axis)

    Returns:
        matplotlib Figure or None if no BTE data present.
    """
    bte_rounds = [h for h in history if "barrier_to_entry" in h]
    if not bte_rounds:
        return None

    rounds_bte = [h["round"] for h in bte_rounds]
    composite = [h["barrier_to_entry"]["composite"] for h in bte_rounds]

    # Entry events in history
    entry_rounds = {h["round"]: h["new_entrant"]["name"] for h in history if "new_entrant" in h}

    def _add_bte_entry_lines(ax):
        for r in entry_rounds:
            ax.axvline(x=r, color='gray', linestyle=':', alpha=0.4, linewidth=1)

    fig, axes = plt.subplots(2, 2, figsize=figsize)
    fig.suptitle("Barrier-to-Entry Dashboard", fontweight='bold')

    # --- Panel 1: Composite BTE over time + effective entry probability ---
    ax1 = axes[0, 0]
    ax1.plot(rounds_bte, composite, '-', color='#457B9D', linewidth=1.5,
             label='BTE Composite')
    ax1.fill_between(rounds_bte, 0, composite, alpha=0.15, color='#457B9D')
    ax1.set_ylim(0, 1)
    ax1.set_ylabel("BTE Composite", color='#457B9D')
    ax1.tick_params(axis='y', colors='#457B9D')

    # Overlay effective entry probability on right axis
    base_prob = next(
        (h["startup_entry_probability"] for h in history
         if h.get("startup_entry_probability") is not None),
        None
    )
    if base_prob is not None and base_prob > 0:
        eff_probs = []
        eff_rounds = []
        prev_bte = 0.0
        for h in history:
            if "barrier_to_entry" not in h:
                continue
            eff_probs.append(base_prob * (1.0 - prev_bte))
            eff_rounds.append(h["round"])
            prev_bte = h["barrier_to_entry"].get("composite", prev_bte)
        if eff_rounds:
            ax1_r = ax1.twinx()
            ax1_r.plot(eff_rounds, eff_probs, '--', color='#E63946', linewidth=1.5,
                       alpha=0.8, label='Effective Entry Prob')
            ax1_r.set_ylim(0, base_prob * 1.5)
            ax1_r.set_ylabel("Effective Entry Prob", color='#E63946')
            ax1_r.tick_params(axis='y', colors='#E63946', labelsize=6)
            # Combined legend
            lines1, labels1 = ax1.get_legend_handles_labels()
            lines2, labels2 = ax1_r.get_legend_handles_labels()
            ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=5, loc='upper left')

    ax1.set_title(r"Composite BTE \& Entry Probability", fontweight='bold')
    ax1.set_xlabel("Round")

    # --- Panel 2: BTE component breakdown ---
    ax2 = axes[0, 1]
    component_colors = {
        "market_concentration": "blue",
        "capability_gap": "orange",
        "funding_lock_in": "purple",
        "consumer_lock_in": "green",
    }
    for comp, color in component_colors.items():
        comp_rounds = []
        comp_vals = []
        for h in bte_rounds:
            val = h["barrier_to_entry"].get(comp)
            if val is not None:
                comp_rounds.append(h["round"])
                comp_vals.append(val)
        if comp_rounds:
            ax2.plot(comp_rounds, comp_vals, '-', color=color, linewidth=1.5,
                     label=_tex_escape(comp.replace("_", " ").title()))
    style_axis(ax2, "BTE Components Over Time", "Round", "Value")

    # --- Panel 3: Entry event scatter ---
    ax3 = axes[1, 0]
    has_scatter = False
    for h in history:
        if "new_entrant" not in h:
            continue
        r = h["round"]
        bte_at_entry = next((bh["barrier_to_entry"] for bh in bte_rounds if bh["round"] == r), None)
        if bte_at_entry is None:
            continue
        bte_comp = bte_at_entry.get("composite", None)
        cap_gap = bte_at_entry.get("capability_gap", None)
        if bte_comp is None or cap_gap is None:
            continue
        name = h["new_entrant"]["name"]
        ax3.scatter(bte_comp, cap_gap, s=40, zorder=3)
        ax3.annotate(_tex_escape(name), (bte_comp, cap_gap), fontsize=6,
                     xytext=(4, 3), textcoords='offset points')
        has_scatter = True
    if not has_scatter:
        ax3.text(0.5, 0.5, "No startup entries this run",
                 transform=ax3.transAxes, ha='center', va='center', fontsize=8, alpha=0.6)
    ax3.set_xlim(0, 1)
    style_axis(ax3, "Entry Events: BTE vs Capability Gap",
               "BTE Composite at Entry", "Capability Gap at Entry", legend=False)

    # --- Panel 4: Market concentration vs provider count (dual axis) ---
    ax4 = axes[1, 1]
    concentration = []
    conc_rounds = []
    for h in bte_rounds:
        val = h["barrier_to_entry"].get("market_concentration")
        if val is not None:
            conc_rounds.append(h["round"])
            concentration.append(val)

    if conc_rounds:
        ax4.plot(conc_rounds, concentration, '-', color='blue', linewidth=1.5,
                 label='Market Concentration')
        ax4.set_ylabel("Market Concentration", color='blue')
        ax4.tick_params(axis='y', colors='blue')
        ax4.set_ylim(0, 1)

    # Provider count per round
    ax4_twin = ax4.twinx()
    prov_counts = [len(h["true_capabilities"]) for h in history]
    all_rounds = [h["round"] for h in history]
    ax4_twin.plot(all_rounds, prov_counts, '--', color='gray', linewidth=1.5,
                  label='Provider Count')
    ax4_twin.set_ylabel("Provider Count", color='gray')
    ax4_twin.tick_params(axis='y', colors='gray')

    ax4.set_xlabel("Round")
    ax4.set_title("Market Concentration vs Provider Count", fontweight='bold')
    lines1, labels1 = ax4.get_legend_handles_labels()
    lines2, labels2 = ax4_twin.get_legend_handles_labels()
    ax4.legend(lines1 + lines2, labels1 + labels2, fontsize=5, loc='best')


    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"BTE dashboard saved to: {save_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig


# =============================================================================
# Startup Cohort Dashboard
# =============================================================================

def plot_startup_cohort_dashboard(
    history: list,
    os_provider_names: set = None,
    save_path: Optional[str] = None,
    show: bool = True,
    figsize: tuple = (6.75, 4.22),
) -> Optional[plt.Figure]:
    """
    Dashboard showing per-startup cohort trajectories.

    One row of 4 sub-panels per startup (capped at 6):
    - Col 0: True capability trajectory (with OS leader for context)
    - Col 1: Market share over time
    - Col 2: Safety alignment investment
    - Col 3: Score vs true capability gap

    Returns:
        matplotlib Figure or None if no startup entries in history.
    """
    from matplotlib.gridspec import GridSpec

    entrant_rounds = {h["new_entrant"]["name"]: h["round"] for h in history if "new_entrant" in h}
    if not entrant_rounds:
        return None

    providers = get_providers(history)
    provider_colors = get_provider_colors(providers)

    # Auto-detect OS provider names
    entrant_names = set(entrant_rounds.keys())
    os_provider_names = (os_provider_names or set()) | entrant_names

    startups = sorted(entrant_rounds.keys(), key=lambda n: entrant_rounds[n])
    startups = startups[:6]  # cap at 6
    n_startups = len(startups)

    fig = plt.figure(figsize=figsize)
    fig.suptitle("Startup Cohort Dashboard", fontweight='bold')
    gs = GridSpec(n_startups, 4, figure=fig, hspace=0.5, wspace=0.35)

    all_rounds = [h["round"] for h in history]
    has_consumer = any("consumer_data" in h for h in history)

    for row_idx, startup in enumerate(startups):
        entry_round = entrant_rounds[startup]
        # Filter history from entry_round onward
        startup_history = [h for h in history if h["round"] >= entry_round
                           and startup in h.get("true_capabilities", {})]

        if not startup_history:
            continue

        s_rounds = [h["round"] for h in startup_history]
        color = provider_colors.get(startup, '#666666')

        # --- Col 0: True capability trajectory ---
        ax0 = fig.add_subplot(gs[row_idx, 0])
        ax0.set_title(_tex_escape(f"{startup} (entry r{entry_round})"), fontsize=7, fontweight='bold')
        s_caps = [h["true_capabilities"][startup] for h in startup_history]
        ax0.plot(s_rounds, s_caps, '-', color=color, linewidth=1.5, label=_tex_escape(startup))

        # OS leader context line (excluding this startup)
        os_leaders = []
        for h in startup_history:
            tc = h["true_capabilities"]
            os_caps = [tc[p] for p in providers if p in os_provider_names
                       and p != startup and p in tc]
            os_leaders.append(max(os_caps) if os_caps else None)
        os_rounds_filt = [r for r, v in zip(s_rounds, os_leaders) if v is not None]
        os_vals_filt = [v for v in os_leaders if v is not None]
        if os_rounds_filt:
            ax0.plot(os_rounds_filt, os_vals_filt, '--', color='gray',
                     linewidth=1, alpha=0.5, label='OS Leader')
        ax0.set_ylim(0, 1)
        ax0.tick_params(labelsize=6)
        ax0.grid(False)
        ax0.set_xlabel("Round", fontsize=7)
        ax0.set_ylabel("True Cap", fontsize=7)
        ax0.legend(fontsize=5, loc='best')

        # --- Col 1: Market share ---
        ax1 = fig.add_subplot(gs[row_idx, 1])
        if has_consumer:
            ms_rounds = []
            ms_vals = []
            for h in startup_history:
                if "consumer_data" in h:
                    shares = h["consumer_data"].get("market_shares", {})
                    ms_rounds.append(h["round"])
                    ms_vals.append(shares.get(startup, 0))
            if ms_rounds:
                ax1.plot(ms_rounds, ms_vals, '-', color=color, linewidth=1.5)
                ax1.set_ylim(0, max(ms_vals) * 1.2 + 0.01)
            else:
                ax1.text(0.5, 0.5, "No data", transform=ax1.transAxes,
                         ha='center', va='center', fontsize=7, alpha=0.5)
        else:
            ax1.text(0.5, 0.5, "Consumers disabled", transform=ax1.transAxes,
                     ha='center', va='center', fontsize=7, alpha=0.5)
        ax1.tick_params(labelsize=6)
        ax1.grid(False)
        ax1.set_xlabel("Round", fontsize=7)
        ax1.set_ylabel("Market Share", fontsize=7)

        # --- Col 2: Safety alignment investment ---
        ax2 = fig.add_subplot(gs[row_idx, 2])
        safety_vals = [h["strategies"].get(startup, {}).get("safety_alignment", 0)
                       for h in startup_history]
        ax2.plot(s_rounds, safety_vals, '-', color=color, linewidth=1.5)
        ax2.set_ylim(0, 1)
        ax2.tick_params(labelsize=6)
        ax2.grid(False)
        ax2.set_xlabel("Round", fontsize=7)
        ax2.set_ylabel("Safety Invest.", fontsize=7)

        # --- Col 3: Score vs true capability gap ---
        ax3 = fig.add_subplot(gs[row_idx, 3])
        gap_vals = []
        for h in startup_history:
            score = h["scores"].get(startup, 0)
            true_cap = h["true_capabilities"].get(startup, 0)
            gap_vals.append(score - true_cap)
        ax3.plot(s_rounds, gap_vals, '-', color=color, linewidth=1.5)
        ax3.tick_params(labelsize=6)
        ax3.grid(False)
        ax3.set_xlabel("Round", fontsize=7)
        ax3.set_ylabel("Score - Cap Gap", fontsize=7)

    fig.subplots_adjust(top=0.93, hspace=0.55, wspace=0.35)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Startup cohort dashboard saved to: {save_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig


# =============================================================================
# Convenience Function: Create All Dashboards
# =============================================================================

def create_all_dashboards(
    history: list,
    output_dir: str = "./plots",
    show: bool = False,
    metadata: Optional[dict] = None,
) -> dict:
    """
    Create and save all dashboards.

    Args:
        history: List of round data dicts
        output_dir: Directory to save plots
        show: Whether to display plots
        metadata: Optional experiment metadata dict with keys like:
                  n_rounds, llm_mode, n_consumers, n_policymakers

    Returns:
        Dict of {dashboard_name: figure_path}
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    saved = {}

    print("Creating dashboards...")

    # Provider Dashboard
    fig = plot_provider_dashboard(history, show=False)
    if fig:
        path = f"{output_dir}/provider_dashboard.png"
        fig.savefig(path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        saved['provider_dashboard'] = path
        print(f"  - Provider dashboard saved")

    # Consumer Satisfaction
    fig = plot_consumer_satisfaction(history, show=False)
    if fig:
        path = f"{output_dir}/consumer_satisfaction_dashboard.png"
        fig.savefig(path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        saved['consumer_satisfaction'] = path
        print(f"  - Consumer satisfaction dashboard saved")

    # Consumer Switching + Market Share
    fig = plot_consumer_switching(history, show=False)
    if fig:
        path = f"{output_dir}/consumer_switching_dashboard.png"
        fig.savefig(path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        saved['consumer_switching'] = path
        print(f"  - Consumer switching dashboard saved")

    # Policymaker Dashboard
    fig = plot_policymaker_dashboard(history, show=False)
    if fig:
        path = f"{output_dir}/policymaker_dashboard.png"
        fig.savefig(path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        saved['policymaker_dashboard'] = path
        print(f"  - Policymaker dashboard saved")

    # Funder Dashboard
    fig = plot_funder_dashboard(history, show=False)
    if fig:
        path = f"{output_dir}/funder_dashboard.png"
        fig.savefig(path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        saved['funder_dashboard'] = path
        print(f"  - Funder dashboard saved")

    # Media Dashboard
    fig = plot_media_dashboard(history, show=False)
    if fig:
        path = f"{output_dir}/media_dashboard.png"
        fig.savefig(path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        saved['media_dashboard'] = path
        print(f"  - Media dashboard saved")

    # Incident Dashboard
    fig = plot_incident_dashboard(history, show=False)
    if fig:
        path = f"{output_dir}/incident_dashboard.png"
        fig.savefig(path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        saved['incident_dashboard'] = path
        print(f"  - Incident dashboard saved")

    # Evaluator Dashboard
    fig = plot_evaluator_dashboard(history, show=False)
    if fig:
        path = f"{output_dir}/evaluator_dashboard.png"
        fig.savefig(path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        saved['evaluator_dashboard'] = path
        print(f"  - Evaluator dashboard saved")

    # Summary Dashboard (with metadata)
    fig = plot_summary_dashboard(history, show=False, metadata=metadata)
    if fig:
        path = f"{output_dir}/summary_dashboard.png"
        fig.savefig(path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        saved['summary_dashboard'] = path
        print(f"  - Summary dashboard saved")

    # Investment Comparison
    fig = plot_investment_comparison(history, show=False)
    if fig:
        path = f"{output_dir}/investment_comparison.png"
        fig.savefig(path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        saved['investment_comparison'] = path
        print(f"  - Investment comparison saved")

    # Validity Over Time
    if len(history) >= 5:
        fig = plot_validity_over_time(history, show=False)
        if fig:
            path = f"{output_dir}/validity_over_time.png"
            fig.savefig(path, dpi=300, bbox_inches='tight')
            plt.close(fig)
            saved['validity_over_time'] = path
            print(f"  - Validity over time saved")

    # Incident Analysis Dashboard (only if incidents present)
    fig = plot_incident_analysis_dashboard(history, show=False)
    if fig:
        path = f"{output_dir}/incident_analysis_dashboard.png"
        fig.savefig(path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        saved['incident_analysis_dashboard'] = path
        print(f"  - Incident analysis dashboard saved")

    # Evaluator Business Dashboard (only if evaluator-as-company data exists)
    fig = plot_evaluator_business_dashboard(history, show=False)
    if fig:
        path = f"{output_dir}/evaluator_business_dashboard.png"
        fig.savefig(path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        saved['evaluator_business_dashboard'] = path
        print(f"  - Evaluator business dashboard saved")

    # Barrier-to-Entry Dashboard (only if BTE data exists)
    if any("barrier_to_entry" in h for h in history):
        path = os.path.join(output_dir, "barrier_to_entry_dashboard.png")
        fig = plot_barrier_to_entry_dashboard(history, save_path=path, show=False)
        if fig:
            saved["barrier_to_entry_dashboard"] = path
            print(f"  - BTE dashboard saved")

    # Startup Cohort Dashboard (only if startup entries exist)
    if any("new_entrant" in h for h in history):
        path = os.path.join(output_dir, "startup_cohort_dashboard.png")
        fig = plot_startup_cohort_dashboard(history, save_path=path, show=False)
        if fig:
            saved["startup_cohort_dashboard"] = path
            print(f"  - Startup cohort dashboard saved")

    print(f"\nAll dashboards saved to: {output_dir}")
    return saved


# =============================================================================
# Legacy Compatibility (maps old function names to new ones)
# =============================================================================

def plot_simulation_results(history, save_path=None, show=True):
    """Legacy function - redirects to plot_provider_dashboard."""
    return plot_provider_dashboard(history, save_path, show)


def plot_strategy_evolution(history, save_path=None, show=True):
    """Legacy function - redirects to plot_investment_comparison."""
    return plot_investment_comparison(history, save_path, show)


def plot_belief_accuracy(history, save_path=None, show=True):
    """Plot belief accuracy (kept for compatibility)."""
    if not history:
        return None

    providers = get_providers(history)
    provider_colors = get_provider_colors(providers)
    rounds = [h["round"] for h in history]

    fig, ax = plt.subplots(figsize=(3.25, 1.63))

    for provider in providers:
        true_caps = np.array([h["true_capabilities"].get(provider) for h in history], dtype=float)
        believed_caps = np.array([h["believed_capabilities"].get(provider) for h in history], dtype=float)
        belief_error = believed_caps - true_caps
        ax.plot(rounds, belief_error, 'o-', label=provider, color=provider_colors[provider],
                markersize=4, linewidth=2)

    ax.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.5)
    ax.fill_between(rounds, -0.05, 0.05, alpha=0.1, color='green', label='Accurate zone')

    style_axis(ax, "Belief Accuracy (Believed - True Capability)", "Round", "Error")


    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig


# plot_consumer_satisfaction is now a first-class function (defined above)
# -- legacy alias removed to avoid shadowing --


def plot_policymaker_interventions(history, save_path=None, show=True):
    """Legacy function - redirects to plot_policymaker_dashboard."""
    return plot_policymaker_dashboard(history, save_path, show)


def plot_ecosystem_dashboard(history, save_path=None, show=True):
    """Legacy function - redirects to plot_summary_dashboard."""
    return plot_summary_dashboard(history, save_path, show)


def create_all_plots(history, output_dir="./plots", show=True):
    """Legacy function - redirects to create_all_dashboards."""
    return create_all_dashboards(history, output_dir, show)


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    # Test with a quick simulation
    from simulation import EvalEcosystemSimulation, SimulationConfig, get_default_provider_configs

    print("Running simulation...")
    config = SimulationConfig(n_rounds=20, seed=42, verbose=True)
    sim = EvalEcosystemSimulation(config)
    sim.setup(get_default_provider_configs())
    sim.run()

    print("\nCreating dashboards...")
    create_all_dashboards(sim.history, output_dir="./test_plots", show=False)
