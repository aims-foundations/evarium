"""
Experiment Comparison Tool
==========================
Usage:
    python compare_experiments.py <exp_a> <exp_b>

Arguments accept any unambiguous prefix of the experiment folder name, e.g.:
    python compare_experiments.py exp_039 exp_040

Output:
    compare_output.md  -- markdown file with side-by-side tables and plots
"""

import base64
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent
EXP_DIRS = [ROOT / "experiments", ROOT / "experiments" / "heuristic"]
COMPARISONS_DIR = ROOT / "comparisons"

PLOT_ORDER = [
    "summary_dashboard",
    "provider_dashboard",
    "consumer_dashboard",
    "policymaker_dashboard",
    "incident_dashboard",
    "investment_comparison",
    "funder_dashboard",
    "evaluator_dashboard",
    "media_dashboard",
    "validity_over_time",
    "incident_analysis_dashboard",
]


# ---------------------------------------------------------------------------
# Experiment discovery
# ---------------------------------------------------------------------------

def find_experiment(query):
    candidates = []
    for base in EXP_DIRS:
        if not base.exists():
            continue
        for d in sorted(base.iterdir()):
            if d.is_dir() and d.name.startswith(query):
                candidates.append(d)
    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        sys.exit(f"ERROR: No experiment found matching '{query}'")
    exact = [c for c in candidates if c.name == query]
    if len(exact) == 1:
        return exact[0]
    sys.exit(f"ERROR: Ambiguous prefix '{query}' matches: {[c.name for c in candidates]}")


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_json(path):
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


def parse_rounds(exp_dir):
    path = exp_dir / "rounds.jsonl"
    if not path.exists():
        return []
    rounds = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                rounds.append(json.loads(line))
    return rounds


def extract_rounds_data(rounds):
    incidents = []
    interventions = []
    active_sanctions = []

    for r in rounds:
        rn = r.get("round", "?")
        for inc in r.get("incidents", []):
            incidents.append({"round": rn, **inc})
        pm = r.get("policymaker_data", {})
        for iv in pm.get("interventions", []):
            interventions.append({"round": rn, **iv})
        sanctions = pm.get("active_sanctions", {})
        if sanctions:
            active_sanctions.append({"round": rn, "sanctions": sanctions})

    return {
        "incidents": incidents,
        "interventions": interventions,
        "active_sanctions": active_sanctions,
        "n_rounds": len(rounds),
    }


# ---------------------------------------------------------------------------
# Markdown helpers
# ---------------------------------------------------------------------------

def f2(v):
    return f"{v:.3f}" if v is not None else "n/a"

def f1(v):
    return f"{v:.1f}" if v is not None else "n/a"

def pct(v):
    return f"{v:.1%}" if v is not None else "n/a"

def md_table(headers, rows):
    """Return a markdown table string. headers = list of str, rows = list of lists."""
    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        lines.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(lines)


def intervention_log(interventions):
    if not interventions:
        return "none"
    parts = []
    for iv in interventions:
        t = iv.get("type", "?")
        rn = iv.get("round", "?")
        target = iv.get("target", "")
        fine = iv.get("details", {}).get("fine_amount")
        if fine is not None:
            parts.append(f"R{rn}: {t} -> {target} (fine={fine:.1%})")
        elif target:
            parts.append(f"R{rn}: {t} -> {target}")
        else:
            parts.append(f"R{rn}: {t}")
    return "  \n".join(parts)  # markdown line breaks


def by_key(items, key):
    out = {}
    for i in items:
        v = i.get(key, "?")
        out[v] = out.get(v, 0) + 1
    return out


def img_data_uri(path):
    """Encode image as base64 data URI so it works in any markdown viewer."""
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{data}"


# ---------------------------------------------------------------------------
# Main comparison builder
# ---------------------------------------------------------------------------

def build_markdown(exp_dir_a, exp_dir_b):
    label_a = exp_dir_a.name
    label_b = exp_dir_b.name

    sum_a = load_json(exp_dir_a / "summary.json")
    sum_b = load_json(exp_dir_b / "summary.json")
    pm_a = load_json(exp_dir_a / "policymakers" / "Regulator" / "params.json")
    pm_b = load_json(exp_dir_b / "policymakers" / "Regulator" / "params.json")
    rd_a = extract_rounds_data(parse_rounds(exp_dir_a))
    rd_b = extract_rounds_data(parse_rounds(exp_dir_b))

    lines = []
    lines.append(f"# Experiment Comparison\n")
    lines.append(f"| | A | B |")
    lines.append(f"| --- | --- | --- |")
    lines.append(f"| Experiment | {label_a} | {label_b} |")
    lines.append(f"| Rounds | {rd_a['n_rounds']} | {rd_b['n_rounds']} |")
    lines.append("")

    # -- Regulatory config ---------------------------------------------------
    lines.append("## Regulatory Configuration\n")

    def pmv(params, key, fmt=f2):
        v = params.get(key)
        return fmt(v) if v is not None else "n/a"

    lines.append(md_table(
        ["Parameter", "A", "B"],
        [
            ["intervention_threshold",      pmv(pm_a, "intervention_threshold"),       pmv(pm_b, "intervention_threshold")],
            ["risk_tolerance",              pmv(pm_a, "risk_tolerance"),               pmv(pm_b, "risk_tolerance")],
            ["intervention_cooldown",       pmv(pm_a, "intervention_cooldown", f1),    pmv(pm_b, "intervention_cooldown", f1)],
            ["sanction_fine_multiplier",    pmv(pm_a, "sanction_fine_multiplier"),     pmv(pm_b, "sanction_fine_multiplier")],
            ["sanction_incident_threshold", pmv(pm_a, "sanction_incident_threshold", f1), pmv(pm_b, "sanction_incident_threshold", f1)],
            ["sanction_duration",           pmv(pm_a, "sanction_duration", f1),        pmv(pm_b, "sanction_duration", f1)],
            ["mandate_risk_threshold",      pmv(pm_a, "mandate_risk_threshold"),       pmv(pm_b, "mandate_risk_threshold")],
            ["sanction_min_severity",       pm_a.get("sanction_min_severity", "n/a"), pm_b.get("sanction_min_severity", "n/a")],
        ]
    ))
    lines.append("")

    # -- Interventions -------------------------------------------------------
    lines.append("## Interventions\n")
    ivs_a = rd_a["interventions"]
    ivs_b = rd_b["interventions"]
    by_type_a = by_key(ivs_a, "type")
    by_type_b = by_key(ivs_b, "type")
    all_types = sorted(set(list(by_type_a) + list(by_type_b)))

    iv_rows = [["**total**", f"**{len(ivs_a)}**", f"**{len(ivs_b)}**"]]
    for t in all_types:
        iv_rows.append([t, by_type_a.get(t, 0), by_type_b.get(t, 0)])
    lines.append(md_table(["Type", "A", "B"], iv_rows))
    lines.append("")
    lines.append("**A timeline:** " + intervention_log(ivs_a))
    lines.append("")
    lines.append("**B timeline:** " + intervention_log(ivs_b))
    lines.append("")

    # -- Active sanctions log ------------------------------------------------
    san_a = rd_a["active_sanctions"]
    san_b = rd_b["active_sanctions"]
    if san_a or san_b:
        lines.append("## Active Sanctions Log\n")
        san_rows = []
        for s in san_a:
            for provider, info in s["sanctions"].items():
                san_rows.append([
                    "A", f"R{s['round']}", provider,
                    f"{info.get('fine_amount', 0):.1%}",
                    f"R{info.get('expires_round', '?')}",
                    info.get("reason", "")[:60],
                ])
        for s in san_b:
            for provider, info in s["sanctions"].items():
                san_rows.append([
                    "B", f"R{s['round']}", provider,
                    f"{info.get('fine_amount', 0):.1%}",
                    f"R{info.get('expires_round', '?')}",
                    info.get("reason", "")[:60],
                ])
        lines.append(md_table(["Exp", "Round", "Provider", "Fine", "Expires", "Reason"], san_rows))
        lines.append("")

    # -- Incidents -----------------------------------------------------------
    lines.append("## Incidents\n")
    inc_a = rd_a["incidents"]
    inc_b = rd_b["incidents"]
    by_sev_a = by_key(inc_a, "severity")
    by_sev_b = by_key(inc_b, "severity")
    by_prov_a = by_key(inc_a, "provider")
    by_prov_b = by_key(inc_b, "provider")
    all_sevs = [s for s in ["critical", "major", "moderate", "minor"]
                if by_sev_a.get(s) or by_sev_b.get(s)]
    all_provs = sorted(set(list(by_prov_a) + list(by_prov_b)))

    inc_rows = [["**total**", f"**{len(inc_a)}**", f"**{len(inc_b)}**"]]
    for s in all_sevs:
        inc_rows.append([s, by_sev_a.get(s, 0), by_sev_b.get(s, 0)])
    lines.append(md_table(["", "A", "B"], inc_rows))
    lines.append("")
    lines.append(md_table(
        ["Provider", "A incidents", "B incidents"],
        [[p, by_prov_a.get(p, 0), by_prov_b.get(p, 0)] for p in all_provs]
    ))
    lines.append("")

    # -- Market shares -------------------------------------------------------
    lines.append("## Final Market Shares\n")
    cs_a = sum_a.get("consumer_summary", {})
    cs_b = sum_b.get("consumer_summary", {})
    shares_a = cs_a.get("final_market_shares", {})
    shares_b = cs_b.get("final_market_shares", {})
    all_provs_mkt = sorted(set(list(shares_a) + list(shares_b)))
    lines.append(md_table(
        ["Provider", "A", "B"],
        [[p, pct(shares_a.get(p)), pct(shares_b.get(p))] for p in all_provs_mkt]
    ))
    lines.append("")

    # -- True capabilities ---------------------------------------------------
    lines.append("## Final True Capabilities\n")
    caps_a = sum_a.get("final_true_capabilities", {})
    caps_b = sum_b.get("final_true_capabilities", {})
    all_provs_cap = sorted(set(list(caps_a) + list(caps_b)))
    cap_rows = [[p, f2(caps_a.get(p)), f2(caps_b.get(p))] for p in all_provs_cap]
    avg_a = sum(caps_a.values()) / len(caps_a) if caps_a else None
    avg_b = sum(caps_b.values()) / len(caps_b) if caps_b else None
    cap_rows.append(["**avg**", f"**{f2(avg_a)}**", f"**{f2(avg_b)}**"])
    lines.append(md_table(["Provider", "A", "B"], cap_rows))
    lines.append("")

    # -- Provider strategy means ---------------------------------------------
    lines.append("## Provider Strategy (Round Means)\n")
    prov_sums_a = sum_a.get("provider_summaries", {})
    prov_sums_b = sum_b.get("provider_summaries", {})
    strat_rows = []
    for p in all_provs_cap:
        da = prov_sums_a.get(p, {})
        db = prov_sums_b.get(p, {})
        strat_rows.append([p,
            f2(da.get("mean_safety_alignment")),
            f2(db.get("mean_safety_alignment")),
            f2(da.get("mean_eval_engineering")),
            f2(db.get("mean_eval_engineering")),
        ])
    lines.append(md_table(
        ["Provider", "A safety", "B safety", "A eval_eng", "B eval_eng"],
        strat_rows
    ))
    lines.append("")

    # -- Consumer outcomes ---------------------------------------------------
    lines.append("## Consumer Outcomes\n")
    lines.append(md_table(
        ["Metric", "A", "B"],
        [
            ["mean satisfaction", f2(cs_a.get("mean_satisfaction")),  f2(cs_b.get("mean_satisfaction"))],
            ["final satisfaction", f2(cs_a.get("final_satisfaction")), f2(cs_b.get("final_satisfaction"))],
            ["avg switching rate", f2(cs_a.get("avg_switching_rate")), f2(cs_b.get("avg_switching_rate"))],
        ]
    ))
    lines.append("")

    # -- Benchmark quality ---------------------------------------------------
    lines.append("## Benchmark Quality (Final)\n")
    bq_a = sum_a.get("benchmark_params", {})
    bq_b = sum_b.get("benchmark_params", {})
    lines.append(md_table(
        ["Metric", "A", "B"],
        [
            ["validity",             f2(bq_a.get("validity")),      f2(bq_b.get("validity"))],
            ["exploitability",       f2(bq_a.get("exploitability")), f2(bq_b.get("exploitability"))],
            ["validity_correlation", f2(sum_a.get("validity_correlation")), f2(sum_b.get("validity_correlation"))],
        ]
    ))
    lines.append("")

    # -- Plots side by side --------------------------------------------------
    lines.append("## Plots\n")
    plots_a = exp_dir_a / "plots"
    plots_b = exp_dir_b / "plots"

    seen = set()
    plot_names = []
    for name in PLOT_ORDER:
        plot_names.append(name)
        seen.add(name)
    for p in sorted(plots_a.glob("*.png")):
        if p.stem not in seen:
            plot_names.append(p.stem)
            seen.add(p.stem)

    for name in plot_names:
        pa = plots_a / f"{name}.png"
        pb = plots_b / f"{name}.png"
        if not pa.exists() and not pb.exists():
            continue
        title = name.replace("_", " ").title()
        lines.append(f"### {title}\n")
        img_a = f'<img src="{img_data_uri(pa)}" width="100%">' if pa.exists() else "<i>no plot</i>"
        img_b = f'<img src="{img_data_uri(pb)}" width="100%">' if pb.exists() else "<i>no plot</i>"
        lines.append("<table><tr>")
        lines.append(f"<td width='50%'><b>A</b><br>{img_a}</td>")
        lines.append(f"<td width='50%'><b>B</b><br>{img_b}</td>")
        lines.append("</tr></table>\n")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 3:
        print("Usage: python compare_experiments.py <exp_a> <exp_b>")
        print("  e.g. python compare_experiments.py exp_039 exp_040")
        sys.exit(1)

    exp_dir_a = find_experiment(sys.argv[1])
    exp_dir_b = find_experiment(sys.argv[2])

    print(f"A: {exp_dir_a.name}")
    print(f"B: {exp_dir_b.name}")

    md = build_markdown(exp_dir_a, exp_dir_b)

    COMPARISONS_DIR.mkdir(exist_ok=True)

    # Extract short IDs (e.g. "exp_039" and "exp_040") for the filename
    def short_id(d):
        parts = d.name.split("_")
        # Keep prefix + number, e.g. "exp_039" or "heur_009"
        if len(parts) >= 2:
            return f"{parts[0]}_{parts[1]}"
        return d.name

    id_a = short_id(exp_dir_a)
    id_b = short_id(exp_dir_b)
    filename = f"{id_a}_vs_{id_b}.md"
    out = COMPARISONS_DIR / filename

    with open(out, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
