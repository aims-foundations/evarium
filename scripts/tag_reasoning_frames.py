"""Keyword+regex tagging of provider reasoning frames for Appendix G.

For each (condition, seed) run under sandbox/experiments/_core_privacy/llm
where ALL models in MODEL_ORDER (sonnet, opus, gpt55) have full 40-round
traces, load each of the 6 providers' memory.json files and tag the
'reasoning' field of every type='planning' entry with one or more frame
labels.

Frames:
    portfolio   allocation / R&D / safety / product / budget reasoning
    competitor  references to rivals by name, leaderboard position, or "catch up"
    incident    incidents, accidents, harms, red-teaming, mitigation
    privacy     holdout / benchmark-type / reporting-lag reasoning
                (the key frame for K.3 — does the model reason about the mechanism?)
    market      market-share / customer / enterprise / switching / churn
    regulatory  regulator / mandate / audit / sanction / advisory
    media       media / press / narrative / buzz / sentiment
    financial   funder / capital / revenue / deploy / round-raise

Each entry can match multiple frames (a single reasoning paragraph often
covers portfolio + competitor + market simultaneously). Per-frame count is
incremented at most once per entry.

Outputs:
    model_robustness_frames_detail.csv  per-entry long form: model, provider,
                                         condition, seed, round, frame_list,
                                         reasoning_excerpt (first 200 chars)
    model_robustness_frames.csv          aggregated for plotting:
                                         model, provider, frame, count
    model_robustness_frames_audit.md     markdown sample of ~3 tagged excerpts
                                         per frame per model, for hand-audit

CLI:
    python -m scripts.tag_reasoning_frames
    python -m scripts.tag_reasoning_frames --out-dir output/paper/
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
from collections import defaultdict

import pandas as pd

from scripts.plots import paths as _paths
from scripts.plots.paper.model_robustness import discover_paired_runs, MODEL_ORDER

PROVIDERS = ["Apex AI", "Orion Labs", "Genesis Systems",
             "Mirage AI", "OpenCore", "Spark AI"]

# Frame patterns. All case-insensitive; each pattern is tried against the
# reasoning text once per entry.
FRAME_PATTERNS = {
    "portfolio":  r"\b(allocat\w*|r&d|\brd\b|r ?and ?d|safety (budget|investment|allocation|lever|focus)|product (budget|investment|allocation|lever)|portfolio|\bbudget\w*)\b",
    "competitor": r"\b(orion|apex|genesis|mirage|opencore|spark|competitor|rival|leader|second[- ]place|catch[- ]?up|gap to|trail|overtak\w+|outpac\w+)\b",
    "incident":   r"\b(incident|accident|\bharm\w*|crisis|mishap|catastroph\w+|red[- ]?team\w*|mitigation)\b",
    "privacy":    r"\b(holdout|private[- ]bench\w*|partial[- ]bench\w*|public[- ]bench\w*|benchmark[- ]type|reporting[- ]lag|K[- ]round|evaluation[- ]lag|holdout[- ]weighted|three[- ]round lag|weight asymmetry|published score|lag.{0,10}round)\b",
    "market":     r"\b(market[- ]?share|adoption|customer|user[- ]?base|enterprise|segment\w*|switching|churn|market cap|retention)\b",
    "regulatory": r"\b(regulator\w*|regulation\w*|audit|investigation|mandate|advisory|compliance|sanction|intervention|regulatory body)\b",
    "media":      r"\b(media|press|headline|narrative|coverage|buzz|sentiment|tech[- ]?press)\b",
    "financial":  r"\b(funder\w*|funding|capital|revenue|deploy\w*|round[- ]raise|\bvc\b|venture|grant|foundation funding|runway)\b",
}
FRAME_COMPILED = {name: re.compile(p, re.IGNORECASE) for name, p in FRAME_PATTERNS.items()}


def tag_reasoning(text: str) -> list[str]:
    """Return sorted list of frame labels that match `text`."""
    if not text:
        return []
    hits = [name for name, pat in FRAME_COMPILED.items() if pat.search(text)]
    return sorted(hits)


def iter_planning_entries(memory_path: str):
    """Yield (round, reasoning_text) for type=='planning' entries with non-empty reasoning."""
    if not os.path.exists(memory_path):
        return
    try:
        with open(memory_path, encoding="utf-8") as f:
            entries = json.load(f)
    except Exception as e:
        print(f"  ERROR loading {memory_path}: {e}", file=sys.stderr)
        return
    if not isinstance(entries, list):
        return
    for e in entries:
        if not isinstance(e, dict) or e.get("type") != "planning":
            continue
        reasoning = e.get("reasoning")
        if not isinstance(reasoning, str) or not reasoning.strip():
            continue
        yield int(e.get("round", -1)), reasoning.strip()


def _paired_conditions(batch: str) -> list[tuple[str, int]]:
    """Return (condition, seed) pairs that have ALL MODEL_ORDER models full runs."""
    by_key = defaultdict(set)
    for cond, seed, model, *_ in discover_paired_runs(batch):
        by_key[(cond, seed)].add(model)
    required = set(MODEL_ORDER)
    return sorted([k for k, ms in by_key.items() if required.issubset(ms)])


def build_frames_detail(batch: str) -> pd.DataFrame:
    """One row per (model, provider, condition, seed, round) — matched triples only."""
    pairs = _paired_conditions(batch)
    if not pairs:
        print(f"No (cond, seed) pairs with all {len(MODEL_ORDER)} models full runs; "
              f"nothing to tag.")
        return pd.DataFrame()
    print(f"Tagging {len(pairs)} matched {len(MODEL_ORDER)}-way pairs: {pairs}")

    # Second-pass discovery so we can resolve seed_dir by (cond, seed, model).
    dirs = {(cond, seed, model): seed_dir
            for cond, seed, model, seed_dir, _ in discover_paired_runs(batch)}

    rows = []
    for cond, seed in pairs:
        for model in MODEL_ORDER:
            seed_dir = dirs.get((cond, seed, model))
            if seed_dir is None:
                continue
            for prov in PROVIDERS:
                mem = os.path.join(seed_dir, "providers", prov, "memory.json")
                for round_n, text in iter_planning_entries(mem):
                    frames = tag_reasoning(text)
                    rows.append({
                        "model": model, "provider": prov,
                        "condition": cond, "seed": seed, "round": round_n,
                        "frames": ",".join(frames) if frames else "untagged",
                        "n_frames": len(frames),
                        "reasoning_excerpt": text[:200].replace("\n", " "),
                        "reasoning_len": len(text),
                    })
    return pd.DataFrame(rows)


def aggregate_for_plot(detail: pd.DataFrame) -> pd.DataFrame:
    """Long form: model, provider, frame, count — one row per frame per entry."""
    rows = []
    for _, r in detail.iterrows():
        if r["frames"] == "untagged":
            rows.append({"model": r["model"], "provider": r["provider"],
                         "frame": "untagged", "count": 1})
            continue
        for fr in r["frames"].split(","):
            rows.append({"model": r["model"], "provider": r["provider"],
                         "frame": fr, "count": 1})
    agg = pd.DataFrame(rows).groupby(["model", "provider", "frame"])["count"].sum().reset_index()
    return agg


def write_audit_sample(detail: pd.DataFrame, out_path: str, n_per: int = 3, seed: int = 0):
    """Markdown file with n_per tagged excerpts per (frame, model), for hand-audit."""
    random.seed(seed)
    frames_ordered = list(FRAME_PATTERNS.keys()) + ["untagged"]
    lines = ["# Reasoning-frame tagging — audit sample",
             "",
             "Sampled excerpts per (frame, model). Use this to sanity-check that "
             "the keyword patterns are catching the right reasoning patterns and "
             "not overmatching.", ""]
    for fr in frames_ordered:
        lines.append(f"## Frame: `{fr}`")
        for model in MODEL_ORDER:
            matches = detail[(detail.frames.str.contains(fr, regex=False)) &
                             (detail.model == model)]
            if fr == "untagged":
                matches = detail[(detail.frames == "untagged") & (detail.model == model)]
            lines.append(f"### {model.capitalize()}  (matches: {len(matches)})")
            if matches.empty:
                lines.append("_none_\n")
                continue
            sample = matches.sample(min(n_per, len(matches)), random_state=seed)
            for _, r in sample.iterrows():
                lines.append(f"- **{r['provider']} / {r['condition']} s{r['seed']} r{r['round']}**: "
                             f"frames=`{r['frames']}`")
                lines.append(f"  > {r['reasoning_excerpt']}")
                lines.append("")
        lines.append("")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Saved {out_path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--batch", default="_core_privacy")
    ap.add_argument("--out-dir", default=None,
                    help="Default: output/paper/ via scripts.plots.paths.paper_dir()")
    ap.add_argument("--audit-n", type=int, default=3,
                    help="Excerpts per (frame, model) in the audit markdown (default 3)")
    args = ap.parse_args()

    out_dir = args.out_dir or _paths.paper_dir()
    os.makedirs(out_dir, exist_ok=True)

    detail = build_frames_detail(args.batch)
    if detail.empty:
        sys.exit(1)

    detail_path = os.path.join(out_dir, "model_robustness_frames_detail.csv")
    detail.to_csv(detail_path, index=False)
    print(f"Saved {detail_path}  ({len(detail)} entries tagged)")

    agg = aggregate_for_plot(detail)
    agg_path = os.path.join(out_dir, "model_robustness_frames.csv")
    agg.to_csv(agg_path, index=False)
    print(f"Saved {agg_path}")

    print("\nSummary by (model, frame):")
    pivot = agg.pivot_table(index="frame", columns="model", values="count",
                            aggfunc="sum", fill_value=0)
    print(pivot.to_string())

    write_audit_sample(detail, os.path.join(out_dir, "model_robustness_frames_audit.md"),
                       n_per=args.audit_n)


if __name__ == "__main__":
    main()
