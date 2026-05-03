"""Build hf_data_staging/ top-level metadata: runs.jsonl, README.md, DATASHEET.md, manifest.json.

Run after scripts/reorganize_for_hf.py --apply has populated hf_data_staging/.
Idempotent: overwrites the four files; everything else under hf_data_staging/ is untouched.

Outputs:
  runs.jsonl       one line per run with provenance + headline metrics
  README.md        layout map + paper-section mapping + citation
  DATASHEET.md     datasheet-for-datasets format (Gebru et al. 2018)
  manifest.json    machine-readable summary (paper SHA, model IDs, run counts, license)
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STAGING = PROJECT_ROOT / "hf_data_staging"

DATASET_NAME = "AI Evaluation Ecosystem Simulation Dataset"
HF_REPO_ID = "anon-author-B41C/evaluation-ecosystem-data"
LICENSE = "CC-BY-4.0"

PROVIDER_BY_MODEL = {
    "claude-sonnet-4-6":   "Anthropic",
    "claude-opus-4-6":     "Anthropic",
    "gpt-5.5-2026-04-23":  "OpenAI",
}

PAPER_SECTION_MAP = {
    "core_privacy":             "§5.2 — Privacy ladder main figure (Sonnet); Appendix G (Opus robustness)",
    "core_evaluator_capture":   "§5.3 + Appendix H — Evaluator capture case study",
    "exogenous_validation":     "§5 Validation — EV1 DeepSeek capability shock",
    "structural_ablations":     "§5 Validation — Structural ablation sweep (Tier 2)",
}


def load_jsonl(path: Path):
    if not path.is_file():
        return
    with path.open() as f:
        for line in f:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def headline_metrics(seed_dir: Path) -> dict:
    """Compute final-round HHI, mean gap, safety share, satisfaction, fallbacks."""
    rounds_path = seed_dir / "rounds.jsonl"
    if not rounds_path.is_file():
        return {}
    last = None
    fallbacks = 0
    n_rounds = 0
    for r in load_jsonl(rounds_path):
        n_rounds += 1
        last = r
        llm = r.get("llm_calls")
        if isinstance(llm, dict):
            fallbacks += int(llm.get("fallbacks", 0))
    if last is None:
        return {"n_rounds": 0}

    cd = last.get("consumer_data", {}) or {}
    ms = cd.get("market_shares", {}) or {}
    sat = cd.get("provider_satisfaction", {}) or {}
    scores = last.get("scores", {}) or {}
    cv = last.get("capability_vectors", {}) or {}

    def _hhi(vals): return round(sum(v * v for v in vals), 4) if vals else None
    def _mean(d): return round(sum(d.values()) / len(d), 4) if d else None

    if scores and sat:
        gap_unweighted = sum(scores[k] - sat.get(k, scores[k]) for k in scores) / len(scores)
        gap_share = sum(ms.get(k, 0) * (scores[k] - sat.get(k, scores[k])) for k in scores)
    else:
        gap_unweighted = gap_share = None

    safety_share = sum(ms.get(p, 0) * cv.get(p, {}).get("safety", 0) for p in ms) if ms and cv else None

    return {
        "n_rounds": n_rounds,
        "hhi_final": _hhi(list(ms.values())),
        "mean_satisfaction_final": _mean(sat),
        "mean_score_final": _mean(scores),
        "mean_gap_unweighted_final": round(gap_unweighted, 4) if gap_unweighted is not None else None,
        "mean_gap_shareweighted_final": round(gap_share, 4) if gap_share is not None else None,
        "safety_share_final": round(safety_share, 4) if safety_share is not None else None,
        "llm_fallbacks": fallbacks,
    }


def discover_runs() -> list[dict]:
    """Scan hf_data_staging/ for every seed_<N>/ dir and assemble run records."""
    runs = []
    for seed_dir in STAGING.rglob("seed_*"):
        if not seed_dir.is_dir():
            continue
        # We expect seed_dir to contain config.json + rounds.jsonl at minimum
        if not (seed_dir / "config.json").is_file():
            continue
        rel = seed_dir.relative_to(STAGING)
        parts = rel.parts
        bucket = parts[0]
        # Path shapes:
        #   <bucket>/llm/<model>/<condition>/seed_<N>/
        #   <bucket>/heuristic/<condition>/seed_<N>/
        #   case_studies/<study>/llm/<model>/<condition>/seed_<N>/
        if bucket == "case_studies" and len(parts) == 6:
            tier = bucket
            study = parts[1]
            model = parts[3]
            condition = parts[4]
            seed = int(parts[5].split("_", 1)[1])
            path = str(rel).replace("\\", "/")
            mode = "llm"
            display_bucket = f"{bucket}/{study}"
        elif len(parts) == 5 and parts[1] == "llm":
            tier = bucket
            model = parts[2]
            condition = parts[3]
            seed = int(parts[4].split("_", 1)[1])
            path = str(rel).replace("\\", "/")
            mode = "llm"
            display_bucket = bucket
        elif len(parts) == 4 and parts[1] == "heuristic":
            tier = bucket
            model = "heuristic"
            condition = parts[2]
            seed = int(parts[3].split("_", 1)[1])
            path = str(rel).replace("\\", "/")
            mode = "heuristic"
            display_bucket = bucket
        else:
            print(f"  [skip] unexpected layout: {rel}", file=sys.stderr)
            continue

        try:
            with (seed_dir / "config.json").open() as f:
                cfg = json.load(f)
        except Exception as e:
            print(f"  [skip] config read failed: {rel}: {e}", file=sys.stderr)
            continue
        meta = {}
        meta_path = seed_dir / "metadata.json"
        if meta_path.is_file():
            try:
                with meta_path.open() as f:
                    meta = json.load(f)
            except Exception:
                pass

        record = {
            "tier": tier,
            "bucket": display_bucket,
            "mode": mode,
            "model": model,
            "condition": condition,
            "seed": seed,
            "path": path,
            "evaluation_lag": cfg.get("evaluation_lag"),
            "git_commit": meta.get("git_commit"),
            "created_at": meta.get("created_at"),
        }
        record.update(headline_metrics(seed_dir))
        runs.append(record)
    runs.sort(key=lambda r: (r["tier"], r["model"], r["condition"], r["seed"]))
    return runs


def write_runs_jsonl(runs: list[dict]) -> Path:
    path = STAGING / "runs.jsonl"
    with path.open("w") as f:
        for r in runs:
            f.write(json.dumps(r) + "\n")
    return path


def write_manifest(runs: list[dict]) -> Path:
    by_tier: dict[str, dict] = defaultdict(lambda: {"runs": 0, "models": set(), "conditions": set()})
    by_tier_mode: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for r in runs:
        t = r["tier"]
        by_tier[t]["runs"] += 1
        by_tier[t]["models"].add(r["model"])
        by_tier[t]["conditions"].add(r["condition"])
        by_tier_mode[t][r["mode"]] += 1

    git_commits = sorted({r["git_commit"] for r in runs if r.get("git_commit")})
    llm_models = sorted({r["model"] for r in runs if r["mode"] == "llm"})

    manifest = {
        "name": DATASET_NAME,
        "huggingface_repo": HF_REPO_ID,
        "license": LICENSE,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "n_runs_total": len(runs),
        "n_runs_by_tier": {t: by_tier[t]["runs"] for t in sorted(by_tier)},
        "n_runs_by_tier_mode": {
            t: dict(sorted(by_tier_mode[t].items())) for t in sorted(by_tier_mode)
        },
        "modes_present": sorted({r["mode"] for r in runs}),
        "llm_models_present": llm_models,
        "conditions_by_tier": {
            t: sorted(by_tier[t]["conditions"]) for t in sorted(by_tier)
        },
        "evaluation_lag_canonical": 3,
        "git_commits_present": git_commits,
        "paper_section_map": PAPER_SECTION_MAP,
    }
    path = STAGING / "manifest.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    return path


def write_readme(runs: list[dict]) -> Path:
    by_tier: dict[str, list[dict]] = defaultdict(list)
    for r in runs:
        by_tier[r["tier"]].append(r)

    llm_models = sorted({r["model"] for r in runs if r["mode"] == "llm"})
    n_llm = sum(1 for r in runs if r["mode"] == "llm")
    n_heuristic = sum(1 for r in runs if r["mode"] == "heuristic")
    has_heuristic = n_heuristic > 0

    intro_modes = []
    if n_llm:
        intro_modes.append(f"{n_llm} LLM-mode runs (agent policies: " + ", ".join(llm_models) + ")")
    if n_heuristic:
        intro_modes.append(f"{n_heuristic} heuristic-mode runs (rule-based agent policies, used as a deterministic baseline)")

    lines = [
        f"# {DATASET_NAME}",
        "",
        f"Hugging Face dataset repository: [{HF_REPO_ID}](https://huggingface.co/datasets/{HF_REPO_ID}).",
        "",
        "Simulation outputs supporting the AI Evaluation Ecosystem paper. Each run is a stochastic",
        "simulation of an AI evaluation ecosystem (providers, evaluators, consumers, regulators,",
        "funders, media) over 40 monthly rounds. This release contains "
        + " and ".join(intro_modes) + ".",
        "",
        "## Layout",
        "",
        "```",
        "hf_data/",
        "├── README.md            this file",
        "├── DATASHEET.md         datasheet for datasets",
        "├── manifest.json        machine-readable summary",
        "├── runs.jsonl           per-run registry with headline metrics",
        "│",
    ]
    buckets_sorted = sorted(by_tier)
    for bi, t in enumerate(buckets_sorted):
        is_last_bucket = (bi == len(buckets_sorted) - 1)
        bucket_prefix = "└──" if is_last_bucket else "├──"
        sub_spacer = "    " if is_last_bucket else "│   "
        lines.append(f"{bucket_prefix} {t}/")
        modes = sorted({r["mode"] for r in by_tier[t]})
        for mi, m in enumerate(modes):
            is_last_mode = (mi == len(modes) - 1)
            mode_prefix = "└──" if is_last_mode else "├──"
            if m == "llm":
                models_in_tier = sorted({r["model"] for r in by_tier[t] if r["mode"] == "llm"})
                lines.append(f"{sub_spacer}{mode_prefix} llm/<model>/<condition>/seed_<N>/   (models: {', '.join(models_in_tier)})")
            elif m == "heuristic":
                lines.append(f"{sub_spacer}{mode_prefix} heuristic/<condition>/seed_<N>/")
    lines += [
        "```",
        "",
        "## Paper-section mapping",
        "",
        "| Bucket | Paper reference | Runs |",
        "|---|---|---|",
    ]
    for t in sorted(by_tier):
        section = PAPER_SECTION_MAP.get(t, "—")
        lines.append(f"| `{t}/` | {section} | {len(by_tier[t])} |")
    lines += [
        "",
        "## Per-run artifact set",
        "",
        "**LLM-mode runs** (`<bucket>/llm/<model>/<condition>/seed_<N>/`):",
        "",
        "- `config.json` — full `SimulationConfig`, sufficient to reproduce the run",
        "- `metadata.json` — seed, timestamp, git commit SHA, `llm_model`, `llm_provider`",
        "- `rounds.jsonl` — round-level data, one JSON line per round (40 lines)",
        "- `summary.json` — cached final-round metrics",
        "- `game_log.md` — natural-language run reconstruction for qualitative inspection",
        "- `ground_truth.json` — benchmark dimension weights (held by the simulation, not visible to actors)",
        "- `dashboard.png` — single-page run summary plot",
        "",
    ]
    if has_heuristic:
        lines += [
            "**Heuristic-mode runs** (`<bucket>/heuristic/<condition>/seed_<N>/`):",
            "",
            "- `config.json` — full `SimulationConfig`",
            "- `metadata.json` — seed, timestamp, git commit SHA",
            "- `rounds.jsonl` — round-level data, one JSON line per round (40 lines)",
            "",
            "Heuristic runs ship with a minimal artifact set: they are fully reproducible from",
            "`config.json` + the pinned source commit, so per-actor reasoning traces, dashboards,",
            "and natural-language game logs are not retained.",
            "",
        ]
    lines += [
        "The `runs.jsonl` registry at the top level lets you scan headline metrics without descending",
        "into individual run directories.",
        "",
        "## Conditions present",
        "",
    ]
    for t in sorted(by_tier):
        conds = sorted({r["condition"] for r in by_tier[t]})
        seeds_per_cond_mode = defaultdict(lambda: defaultdict(set))
        for r in by_tier[t]:
            seeds_per_cond_mode[r["condition"]][r["mode"]].add(r["seed"])
        lines.append(f"### `{t}/`")
        lines.append("")
        lines.append("| Condition | Mode | Seeds |")
        lines.append("|---|---|---|")
        for c in conds:
            for m in sorted(seeds_per_cond_mode[c]):
                seeds = sorted(seeds_per_cond_mode[c][m])
                if len(seeds) == 1:
                    seed_str = f"1 (`{seeds[0]}`)"
                else:
                    seed_str = f"{len(seeds)} (`{seeds[0]}`–`{seeds[-1]}`)"
                lines.append(f"| `{c}` | {m} | {seed_str} |")
        lines.append("")
    lines += [
        "## Reproducibility",
        "",
        f"All runs target `evaluation_lag = 3` (the canonical setting). The `metadata.json` of each run",
        "records the exact `git_commit` of the simulation code that produced it. Source code lives at",
        "the project's GitHub repository; pin to the commit recorded in metadata to reproduce a run",
        "byte-for-byte.",
        "",
        f"## License",
        "",
        f"This dataset is released under {LICENSE}.",
        "",
        "## Citation",
        "",
        "Please cite the accompanying paper (citation TBD).",
        "",
    ]
    path = STAGING / "README.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_datasheet(runs: list[dict]) -> Path:
    n = len(runs)
    n_llm = sum(1 for r in runs if r["mode"] == "llm")
    n_heuristic = sum(1 for r in runs if r["mode"] == "heuristic")
    llm_models = sorted({r["model"] for r in runs if r["mode"] == "llm"})
    providers = sorted({PROVIDER_BY_MODEL.get(m, "unknown") for m in llm_models})
    models_str = ", ".join(llm_models) if llm_models else "—"
    providers_str = " and ".join(providers) if len(providers) <= 2 else ", ".join(providers)
    tiers = sorted({r["tier"] for r in runs})

    mode_breakdown_parts = []
    if n_llm:
        mode_breakdown_parts.append(f"{n_llm} LLM-mode")
    if n_heuristic:
        mode_breakdown_parts.append(f"{n_heuristic} heuristic-mode")
    mode_breakdown = ", ".join(mode_breakdown_parts) if mode_breakdown_parts else f"{n}"

    text = f"""# Datasheet — {DATASET_NAME}

This datasheet follows the format of Gebru et al. (2018), *Datasheets for Datasets*.

## Motivation

**For what purpose was the dataset created?** To enable reproducibility, secondary analysis,
and qualitative inspection of the simulation experiments reported in the AI Evaluation
Ecosystem paper. The simulation models a multi-agent AI evaluation ecosystem and produces
round-level traces of agent decisions, market dynamics, and benchmark scores under a range
of structural and policy conditions.

**Who created the dataset?** The paper authors.

**Funding:** [TBD before submission].

## Composition

**What do the instances represent?** Each instance is one *seed* of a simulation *condition*:
40 monthly rounds of a stylised AI evaluation ecosystem. There are {n} runs total
({mode_breakdown}), organised under {len(tiers)} top-level buckets. LLM-mode runs use a
frontier LLM as the agent policy for providers, evaluators, regulators, and funders.
Heuristic-mode runs replace the LLM policy with deterministic rule-based agents and serve
as a stochastic-baseline reference.

**LLM models used:** {models_str} ({providers_str}).

**How many instances?** {n} runs ({mode_breakdown}).

**What data does each instance contain?** Round-level scores, capability vectors,
market shares, satisfaction signals, regulator interventions, funder allocations, media
coverage, incidents, and (for LLM-mode runs) agent reasoning traces. Every run ships
`config.json`, `metadata.json`, and `rounds.jsonl`. LLM-mode runs additionally ship
`summary.json`, `game_log.md`, `ground_truth.json`, and a `dashboard.png` plot.

**Is there any sensitive content?** No. All actors are synthetic; no real-world personal
data is present.

**Are relationships between instances explicit?** Yes — runs are organised by
`tier/model/condition/seed`. Multiple seeds of the same (model, condition) are direct
replicates; same (condition, seed) across models supports cross-model robustness analysis.

**Are there errors or noise?** Stochastic noise is intrinsic to the simulation
(seeded). All released runs use the canonical `evaluation_lag = 3`. Runs with other
lag settings are excluded from this release.

**Self-contained?** Yes. Configs are sufficient to reproduce given a pinned source
commit; reproduction requires API access to the relevant LLM provider(s).

## Collection process

**How was data acquired?** By executing `scripts/run_experiment.py` against the
simulation source code at the recorded git commit. LLM agent calls were issued to the
provider recorded in each run's `metadata.json` (`llm_provider` field).

**Sampling?** No — runs are exhaustive over the configured (condition, seed) grid.

**Time period:** April 2026 (run timestamps in `metadata.created_at`).

## Preprocessing

The released artifacts are slimmed from the raw run output. Per-run files dropped before
release: `history.json` (redundant with `rounds.jsonl`), `plots/` (presentation slides;
regenerable from `rounds.jsonl` + project plotting scripts), `dashboard.pdf` (the PNG
version is retained), and per-actor dumps (`providers/`, `consumers/`, `funders/`,
`regulators/`).

## Uses

**Intended uses:** Reproducing paper results, computing additional metrics from the
round-level traces, qualitative inspection of LLM reasoning traces in `game_log.md` or
the `actor_traces` field of `rounds.jsonl`.

**Tasks the dataset should NOT be used for:** Training generative models on the LLM
reasoning traces (these are model outputs, not curated supervision data). Inferring
general AI-policy claims directly without consulting the paper's caveats.

## Distribution

**License:** {LICENSE}.

**Distribution:** Hugging Face Datasets at `{HF_REPO_ID}`.

## Maintenance

**Maintainer:** Paper authors (contact via repository).

**Versioning:** Future revisions will land as additional commits on the same dataset
repo; pin to a specific revision for reproducibility.
"""
    path = STAGING / "DATASHEET.md"
    path.write_text(text, encoding="utf-8")
    return path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.parse_args()

    if not STAGING.is_dir():
        print(f"ERROR: {STAGING} does not exist. Run scripts/reorganize_for_hf.py --apply first.",
              file=sys.stderr)
        return 1

    print(f"Scanning {STAGING.relative_to(PROJECT_ROOT)} ...")
    runs = discover_runs()
    print(f"  found {len(runs)} runs")

    runs_path = write_runs_jsonl(runs)
    print(f"  wrote {runs_path.relative_to(PROJECT_ROOT)} ({len(runs)} lines)")

    manifest_path = write_manifest(runs)
    print(f"  wrote {manifest_path.relative_to(PROJECT_ROOT)}")

    readme_path = write_readme(runs)
    print(f"  wrote {readme_path.relative_to(PROJECT_ROOT)}")

    datasheet_path = write_datasheet(runs)
    print(f"  wrote {datasheet_path.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
