"""
analyze_registry.py

Reads hf_data/runs.jsonl and writes docs/results_analysis.md.

Usage:
    python scripts/analyze_registry.py [--runs PATH] [--out PATH]
"""

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path
from datetime import datetime


# ---------------------------------------------------------------------------
# Stats helpers
# ---------------------------------------------------------------------------

def _mean(vals):
    vals = [v for v in vals if v is not None]
    return sum(vals) / len(vals) if vals else None


def _std(vals):
    vals = [v for v in vals if v is not None]
    n = len(vals)
    if n < 2:
        return None
    m = sum(vals) / n
    return math.sqrt(sum((x - m) ** 2 for x in vals) / (n - 1))


def _ci95(vals):
    """95% CI half-width using t-distribution (df=n-1), approximated for large n."""
    vals = [v for v in vals if v is not None]
    n = len(vals)
    if n < 2:
        return None
    s = _std(vals)
    # t critical values (two-tailed 95%)
    T = {2: 12.706, 3: 4.303, 4: 3.182, 5: 2.776, 6: 2.571, 7: 2.447,
         8: 2.365, 9: 2.306, 10: 2.228, 15: 2.131, 20: 2.086, 25: 2.060,
         30: 2.042, 40: 2.021, 60: 2.000}
    t = T.get(n, T.get(30, 2.042) if n >= 30 else 2.228)
    return t * s / math.sqrt(n)


def fmt(v, decimals=3):
    if v is None:
        return "—"
    return f"{v:.{decimals}f}"


def fmt_ci(mean, ci, decimals=3):
    if mean is None:
        return "—"
    if ci is None:
        return fmt(mean, decimals)
    return f"{mean:.{decimals}f} ±{ci:.{decimals}f}"


def pass_rate(vals):
    """Return (rate, wilson_lower, wilson_upper) for boolean list."""
    vals = [v for v in vals if v is not None]
    n = len(vals)
    if n == 0:
        return None, None, None
    k = sum(1 for v in vals if v)
    p = k / n
    # Wilson 95% CI
    z = 1.96
    denom = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / denom
    margin = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denom
    return p, max(0, centre - margin), min(1, centre + margin)


def fmt_pass(vals, n_label=True):
    p, lo, hi = pass_rate(vals)
    if p is None:
        return "—"
    vals_clean = [v for v in vals if v is not None]
    k = sum(1 for v in vals_clean if v)
    n = len(vals_clean)
    s = f"{k}/{n}"
    return s


# ---------------------------------------------------------------------------
# Condition name prettifier
# ---------------------------------------------------------------------------

CONDITION_LABELS = {
    "full_ecosystem": "Full Ecosystem",
    "ablation_no_media": "No Media",
    "ablation_no_incidents": "No Incidents",
    "ablation_no_startups": "No Startups",
    "ablation_no_opencore": "No OpenCore",
    "ablation_single_benchmark": "Single Benchmark",
    "ablation_no_funders": "No Funders",
    "ablation_no_bench_evolution": "No Bench Evolution",
    "ablation_eval_as_company": "Eval As Company",
}

PRESET_LABELS = {
    "balanced": "Balanced",
    "us": "US",
    "eu": "EU",
}

CONDITION_ORDER = [
    "full_ecosystem",
    "ablation_no_media",
    "ablation_no_incidents",
    "ablation_no_startups",
    "ablation_no_opencore",
    "ablation_single_benchmark",
    "ablation_no_funders",
    "ablation_no_bench_evolution",
    "ablation_eval_as_company",
]

PRESET_ORDER = ["balanced", "us", "eu"]

PATTERN_LABELS = {
    "pattern_score_inflation": "Score Inflation",
    "pattern_benchmark_turnover": "Bench Turnover",
    "pattern_regulatory_escalation": "Reg. Escalation",
    "pattern_commoditization_shock": "Commoditization",
    "pattern_safety_incident_response": "Safety Response",
    "pattern_gaming_persistence": "Gaming Persist.",
    "pattern_funding_follows_scores": "Funding→Scores",
}

METRIC_LABELS = {
    "gaming_gap_final": "Gaming Gap",
    "hhi_final": "HHI",
    "mean_capability_final": "Capability",
    "mean_eval_eng_final": "Eval Eng.",
    "benchmark_validity_final": "BM Validity",
}


def parse_condition_preset(condition_str):
    """Split 'full_ecosystem_balanced' → ('full_ecosystem', 'balanced')"""
    for preset in PRESET_ORDER:
        if condition_str.endswith("_" + preset):
            base = condition_str[: -(len(preset) + 1)]
            return base, preset
    return condition_str, "balanced"


# ---------------------------------------------------------------------------
# Load and group
# ---------------------------------------------------------------------------

def load_runs(path: Path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def group_by(rows, *keys):
    result = defaultdict(list)
    for r in rows:
        key = tuple(r.get(k) for k in keys)
        result[key].append(r)
    return result


# ---------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------

def section_overview(rows):
    phases = defaultdict(list)
    for r in rows:
        phases[r["phase"]].append(r)

    lines = ["## Overview\n"]
    lines.append(f"Registry generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    lines.append(f"Total runs: **{len(rows)}**\n")
    lines.append("")
    lines.append("| Phase | Model | Runs |")
    lines.append("|-------|-------|------|")
    phase_order = ["heuristic_baseline", "llm_core", "claude_archive"]
    model_counts = defaultdict(lambda: defaultdict(int))
    for r in rows:
        model_counts[r["phase"]][r["model"]] += 1
    for phase in phase_order:
        if phase not in model_counts:
            continue
        for model, count in sorted(model_counts[phase].items()):
            lines.append(f"| {phase} | {model} | {count} |")
    lines.append("")
    return "\n".join(lines)


def section_pattern_validation(rows, phase, model_filter=None):
    """Pattern pass/fail table: rows=conditions, cols=presets."""
    filtered = [r for r in rows if r["phase"] == phase]
    if model_filter:
        filtered = [r for r in filtered if r["model"] == model_filter]

    # Group by condition_base x preset
    groups = defaultdict(list)
    for r in filtered:
        base, preset = parse_condition_preset(r["condition"])
        groups[(base, preset)].append(r)

    patterns = list(PATTERN_LABELS.keys())
    pattern_short = list(PATTERN_LABELS.values())

    lines = []
    header = "| Condition | Preset | N | " + " | ".join(pattern_short) + " |"
    sep = "|-----------|--------|---|" + "|".join(["---"] * len(patterns)) + "|"
    lines.append(header)
    lines.append(sep)

    for cbase in CONDITION_ORDER:
        label = CONDITION_LABELS.get(cbase, cbase)
        for preset in PRESET_ORDER:
            key = (cbase, preset)
            grp = groups.get(key, [])
            if not grp:
                continue
            n = len(grp)
            cells = []
            for pat in patterns:
                vals = [r.get(pat) for r in grp]
                cells.append(fmt_pass(vals))
            lines.append(f"| {label} | {PRESET_LABELS.get(preset, preset)} | {n} | " +
                         " | ".join(cells) + " |")

    return "\n".join(lines)


def section_metrics_table(rows, phase, model_filter=None, show_ci=True):
    """Primary metrics table: rows=conditions×presets."""
    filtered = [r for r in rows if r["phase"] == phase]
    if model_filter:
        filtered = [r for r in filtered if r["model"] == model_filter]

    groups = defaultdict(list)
    for r in filtered:
        base, preset = parse_condition_preset(r["condition"])
        groups[(base, preset)].append(r)

    metrics = list(METRIC_LABELS.keys())
    metric_labels = list(METRIC_LABELS.values())

    lines = []
    header = "| Condition | Preset | N | " + " | ".join(metric_labels) + " |"
    sep = "|-----------|--------|---|" + "|".join(["---"] * len(metrics)) + "|"
    lines.append(header)
    lines.append(sep)

    for cbase in CONDITION_ORDER:
        label = CONDITION_LABELS.get(cbase, cbase)
        for preset in PRESET_ORDER:
            key = (cbase, preset)
            grp = groups.get(key, [])
            if not grp:
                continue
            n = len(grp)
            cells = []
            for m in metrics:
                vals = [r.get(m) for r in grp]
                mu = _mean(vals)
                ci = _ci95(vals) if show_ci and n >= 2 else None
                cells.append(fmt_ci(mu, ci))
            lines.append(f"| {label} | {PRESET_LABELS.get(preset, preset)} | {n} | " +
                         " | ".join(cells) + " |")

    return "\n".join(lines)


def section_ablation_deltas(rows, phase, model_filter=None, preset="balanced"):
    """Delta table vs full_ecosystem baseline for a given preset."""
    filtered = [r for r in rows if r["phase"] == phase]
    if model_filter:
        filtered = [r for r in filtered if r["model"] == model_filter]

    groups = defaultdict(list)
    for r in filtered:
        base, p = parse_condition_preset(r["condition"])
        if p == preset:
            groups[base].append(r)

    baseline = groups.get("full_ecosystem", [])
    if not baseline:
        return f"*No full_ecosystem_{preset} baseline found.*"

    metrics = list(METRIC_LABELS.keys())
    metric_labels = list(METRIC_LABELS.values())
    baseline_means = {m: _mean([r.get(m) for r in baseline]) for m in metrics}

    lines = []
    header = "| Condition | N | " + " | ".join(f"Δ {l}" for l in metric_labels) + " |"
    sep = "|-----------|---|" + "|".join(["---"] * len(metrics)) + "|"
    lines.append(header)
    lines.append(sep)

    for cbase in CONDITION_ORDER:
        if cbase == "full_ecosystem":
            continue
        label = CONDITION_LABELS.get(cbase, cbase)
        grp = groups.get(cbase, [])
        if not grp:
            continue
        n = len(grp)
        cells = []
        for m in metrics:
            mu = _mean([r.get(m) for r in grp])
            base_mu = baseline_means[m]
            if mu is None or base_mu is None:
                cells.append("—")
            else:
                delta = mu - base_mu
                cells.append(f"{delta:+.3f}")
        lines.append(f"| {label} | {n} | " + " | ".join(cells) + " |")

    return "\n".join(lines)


def section_cross_model(rows, condition="full_ecosystem_balanced"):
    """Compare metrics across models for a single condition."""
    filtered = [r for r in rows if r["condition"] == condition]

    groups = defaultdict(list)
    for r in filtered:
        key = (r["phase"], r["model"])
        groups[key].append(r)

    if not groups:
        return f"*No runs found for condition `{condition}`.*"

    metrics = list(METRIC_LABELS.keys())
    metric_labels = list(METRIC_LABELS.values())
    patterns = list(PATTERN_LABELS.keys())
    pattern_short = list(PATTERN_LABELS.values())

    lines = []
    header = "| Phase | Model | N | " + " | ".join(metric_labels) + " | " + " | ".join(pattern_short) + " |"
    sep = "|-------|-------|---|" + "|".join(["---"] * len(metrics)) + "|" + "|".join(["---"] * len(patterns)) + "|"
    lines.append(header)
    lines.append(sep)

    phase_order = ["heuristic_baseline", "llm_core", "claude_archive"]
    for phase in phase_order:
        for (p, model), grp in sorted(groups.items(), key=lambda x: x[0][1]):
            if p != phase:
                continue
            n = len(grp)
            metric_cells = []
            for m in metrics:
                vals = [r.get(m) for r in grp]
                mu = _mean(vals)
                ci = _ci95(vals) if n >= 2 else None
                metric_cells.append(fmt_ci(mu, ci))
            pat_cells = [fmt_pass([r.get(pat) for r in grp]) for pat in patterns]
            lines.append(f"| {phase} | {model} | {n} | " +
                         " | ".join(metric_cells) + " | " +
                         " | ".join(pat_cells) + " |")

    return "\n".join(lines)


def section_regulatory_preset_comparison(rows, phase, model_filter=None):
    """For each condition_base, compare balanced vs US vs EU."""
    filtered = [r for r in rows if r["phase"] == phase]
    if model_filter:
        filtered = [r for r in filtered if r["model"] == model_filter]

    groups = defaultdict(list)
    for r in filtered:
        base, preset = parse_condition_preset(r["condition"])
        groups[(base, preset)].append(r)

    metrics = ["gaming_gap_final", "hhi_final", "mean_capability_final"]
    metric_labels = ["Gaming Gap", "HHI", "Capability"]

    lines = []
    header = "| Condition | Balanced | US | EU |"
    sep = "|-----------|----------|----|-----|"
    # One sub-table per metric
    for metric, mlabel in zip(metrics, metric_labels):
        lines.append(f"### {mlabel}\n")
        lines.append(header)
        lines.append(sep)
        for cbase in CONDITION_ORDER:
            label = CONDITION_LABELS.get(cbase, cbase)
            row_cells = []
            for preset in PRESET_ORDER:
                grp = groups.get((cbase, preset), [])
                mu = _mean([r.get(metric) for r in grp])
                ci = _ci95([r.get(metric) for r in grp]) if len(grp) >= 2 else None
                row_cells.append(fmt_ci(mu, ci))
            lines.append(f"| {label} | " + " | ".join(row_cells) + " |")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", default=None)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    runs_path = Path(args.runs) if args.runs else project_root / "hf_data" / "runs.jsonl"
    out_path = Path(args.out) if args.out else project_root / "docs" / "results_analysis.md"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    rows = load_runs(runs_path)

    md = []
    md.append("# Simulation Results Analysis\n")
    md.append(f"> Auto-generated by `scripts/analyze_registry.py` on "
              f"{datetime.now().strftime('%Y-%m-%d %H:%M')}  \n"
              f"> Source: `{runs_path.name}`\n")
    md.append("")

    # --- Overview ---
    md.append(section_overview(rows))

    # --- Heuristic Baseline ---
    md.append("---\n")
    md.append("## Phase 5: Heuristic Baseline (30 seeds × 27 conditions)\n")

    md.append("### Primary Metrics (mean ±95% CI)\n")
    md.append(section_metrics_table(rows, "heuristic_baseline"))
    md.append("")

    md.append("### Pattern Validation Pass Rates (k/N)\n")
    md.append(section_pattern_validation(rows, "heuristic_baseline"))
    md.append("")

    md.append("### Ablation Deltas vs Full Ecosystem — Balanced Preset\n")
    md.append("*Delta = ablation mean − full_ecosystem_balanced mean.*\n")
    md.append(section_ablation_deltas(rows, "heuristic_baseline", preset="balanced"))
    md.append("")

    md.append("### Ablation Deltas vs Full Ecosystem — US Preset\n")
    md.append(section_ablation_deltas(rows, "heuristic_baseline", preset="us"))
    md.append("")

    md.append("### Ablation Deltas vs Full Ecosystem — EU Preset\n")
    md.append(section_ablation_deltas(rows, "heuristic_baseline", preset="eu"))
    md.append("")

    md.append("### Regulatory Preset Comparison\n")
    md.append(section_regulatory_preset_comparison(rows, "heuristic_baseline"))
    md.append("")

    # --- LLM Core ---
    md.append("---\n")
    md.append("## LLM Core Runs\n")

    for model in ["qwen-235b", "llama-70b"]:
        model_rows = [r for r in rows if r["phase"] == "llm_core" and r["model"] == model]
        if not model_rows:
            continue
        n_total = len(model_rows)
        n_conds = len(set(r["condition"] for r in model_rows))
        md.append(f"### Model: `{model}` ({n_total} runs across {n_conds} conditions)\n")

        md.append("#### Primary Metrics\n")
        md.append(section_metrics_table(rows, "llm_core", model_filter=model))
        md.append("")

        md.append("#### Pattern Validation\n")
        md.append(section_pattern_validation(rows, "llm_core", model_filter=model))
        md.append("")

        # Only show ablation deltas if we have a full_ecosystem_balanced baseline
        baseline = [r for r in model_rows if r["condition"] == "full_ecosystem_balanced"]
        if baseline:
            md.append("#### Ablation Deltas vs Full Ecosystem — Balanced\n")
            md.append(section_ablation_deltas(rows, "llm_core", model_filter=model, preset="balanced"))
            md.append("")

    # --- Claude Archive ---
    md.append("---\n")
    md.append("## Claude Archive (exp_001–015, Claude 3.5 Sonnet)\n")

    md.append("### Primary Metrics\n")
    md.append(section_metrics_table(rows, "claude_archive", show_ci=False))
    md.append("")

    md.append("### Pattern Validation\n")
    md.append(section_pattern_validation(rows, "claude_archive"))
    md.append("")

    # --- Cross-model comparison ---
    md.append("---\n")
    md.append("## Cross-Model Comparison\n")

    md.append("### `full_ecosystem_balanced` — All Models\n")
    md.append(section_cross_model(rows, "full_ecosystem_balanced"))
    md.append("")

    md.append("### `full_ecosystem_us` — All Models\n")
    md.append(section_cross_model(rows, "full_ecosystem_us"))
    md.append("")

    # --- Metric definitions ---
    md.append("---\n")
    md.append("## Metric Definitions\n")
    md.append("""
| Metric | Definition |
|--------|------------|
| Gaming Gap | mean(published_score − true_capability) at round 30 |
| HHI | Herfindahl-Hirschman Index: sum(market_share²) at round 30 |
| Capability | Mean true capability across providers at round 30 |
| Eval Eng. | Mean evaluation_engineering strategy allocation at round 30 |
| BM Validity | Mean benchmark validity parameter at round 30 |
| Score Inflation | mean_inflation > 0.10 sustained from round 15 onward |
| Bench Turnover | At least one benchmark retired + one introduced |
| Reg. Escalation | At least one intervention beyond threshold_announcement/investigation |
| Commoditization | OpenCore commoditization shock fired |
| Safety Response | Funder allocation shifted after a major/critical incident |
| Gaming Persist. | Mean eval_eng above initial level through round 20+ |
| Funding→Scores | r(funding, score) > r(funding, true_capability) |
""")

    out_path.write_text("\n".join(md), encoding="utf-8")
    print(f"Written to {out_path}")


if __name__ == "__main__":
    main()
