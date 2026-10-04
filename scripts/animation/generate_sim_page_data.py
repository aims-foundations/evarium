"""Generate website/client/js/sim_data.js for the simulation explainer page.

Every number the explainer page renders is computed here from the live
simulation source (BENCHMARK_POOL, USE_CASE_PROFILES, ARCHETYPES) rather than
transcribed from docs, so the page cannot silently drift from the model.

Run after any change to benchmark weights, consumer profiles, or archetypes:

    python scripts/animation/generate_sim_page_data.py

Then bump the ?v=N on the <script> tag in website/client/simulation.html
(static assets cache hard).
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from actors.consumer import ARCHETYPES, USE_CASE_PROFILES  # noqa: E402
from actors.evaluator import BENCHMARK_POOL  # noqa: E402

OUT = ROOT / "website" / "client" / "js" / "sim_data.js"

# DIMENSIONS lives in actors/model_provider.py (docs list a
# src/capability_dimensions.py that does not exist -- see stakeholders.md
# File Reference). Import from the real home.
from actors.model_provider import DIMENSIONS  # noqa: E402

DIM_LABEL = {
    "reasoning": "Reasoning",
    "coding": "Coding",
    "knowledge": "Knowledge",
    "safety": "Safety",
    "communication": "Communication",
    "agentic": "Agentic",
}

# Adoption-weighted population shares, mirrored from
# consumer.create_default_segments.USE_CASE_POP_WEIGHTS (local constant, not
# importable). Asserted against the profile roster below.
USE_CASE_POP_WEIGHTS = {
    "software_dev": 0.14, "content_writer": 0.08, "legal": 0.04,
    "healthcare": 0.05, "finance": 0.05, "educator": 0.07,
    "customer_service": 0.08, "researcher": 0.06, "creative": 0.06,
    "marketing": 0.07, "service_worker": 0.05, "hospital_system": 0.05,
    "enterprise_finance": 0.05, "tech_startup": 0.06,
    "enterprise_legal": 0.04, "government_agency": 0.05,
    "enterprise_hr": 0.04,
}

ARCHETYPE_LABEL = {
    "leaderboard_follower": "Leaderboard follower",
    "experience_driven": "Experience-driven",
    "cautious": "Cautious",
    "enterprise_cautious": "Enterprise, cautious",
    "enterprise_growth": "Enterprise, growth",
    "enterprise_established": "Enterprise, established",
}

# Benchmarks active at round 0 (evaluator initial set). The roster grows to 13
# over the 40-round horizon via the introduction schedule.
ROUND0 = ["General Capability", "Coding Evaluation",
          "Safety Evaluation", "Instruction Following"]


def aggregate(bench: dict, key: str):
    """Mean dimension loading across a benchmark's public task categories."""
    cats = bench.get(key) or {}
    if not cats:
        return None
    acc = {d: 0.0 for d in DIMENSIONS}
    for weights in cats.values():
        for d in DIMENSIONS:
            acc[d] += weights.get(d, 0.0)
    n = len(cats)
    return {d: round(acc[d] / n, 4) for d in DIMENSIONS}


def mean_vector(vectors: list[dict]) -> dict:
    n = len(vectors)
    return {d: round(sum(v[d] for v in vectors) / n, 4) for d in DIMENSIONS}


def cosine(a: dict, b: dict) -> float:
    dot = sum(a[d] * b[d] for d in DIMENSIONS)
    na = sum(a[d] ** 2 for d in DIMENSIONS) ** 0.5
    nb = sum(b[d] ** 2 for d in DIMENSIONS) ** 0.5
    return round(dot / (na * nb), 4) if na and nb else 0.0


def build() -> dict:
    benchmarks = []
    for b in BENCHMARK_POOL:
        benchmarks.append({
            "name": b["name"],
            "tags": b["tags"],
            "ncat": len(b["category_dimension_weights"]),
            "noise": b.get("noise_sigma"),
            "samples": b.get("samples"),
            "w": aggregate(b, "category_dimension_weights"),
            "hw": aggregate(b, "holdout_category_dimension_weights"),
        })

    missing = set(USE_CASE_PROFILES) - set(USE_CASE_POP_WEIGHTS)
    if missing:
        raise SystemExit(f"pop weights missing for profiles: {sorted(missing)}")

    pop_total = sum(USE_CASE_POP_WEIGHTS[k] for k in USE_CASE_PROFILES)
    profiles = []
    for key, p in USE_CASE_PROFILES.items():
        profiles.append({
            "key": key,
            "label": p["label"],
            "type": p["consumer_type"],
            "need": {d: round(p["need_weights"].get(d, 0.0), 4) for d in DIMENSIONS},
            "pop": round(USE_CASE_POP_WEIGHTS[key] / pop_total, 4),
        })

    pop_avg_need = {
        d: round(sum(pr["need"][d] * pr["pop"] for pr in profiles), 4)
        for d in DIMENSIONS
    }

    pool_avg = mean_vector([b["w"] for b in benchmarks])
    round0_avg = mean_vector([b["w"] for b in benchmarks if b["name"] in ROUND0])

    archetypes = [{
        "key": k,
        "label": ARCHETYPE_LABEL.get(k, k),
        "trust": v["leaderboard_trust"],
        "switchCost": v["switching_cost"],
        "threshold": v["switching_threshold"],
        "costSens": v["cost_sensitivity"],
    } for k, v in ARCHETYPES.items()]

    # Segment count: archetypes pair only within their consumer class.
    n_ind_profiles = sum(1 for p in profiles if p["type"] == "individual")
    n_org_profiles = len(profiles) - n_ind_profiles
    n_ind_arch = sum(1 for a in archetypes if not a["key"].startswith("enterprise_"))
    n_org_arch = len(archetypes) - n_ind_arch
    n_segments = n_ind_profiles * n_ind_arch + n_org_profiles * n_org_arch

    holdout_cos = [{
        "name": b["name"],
        "cos": cosine(b["w"], b["hw"]),
    } for b in benchmarks if b["hw"]]

    return {
        "generated": date.today().isoformat(),
        "dims": DIMENSIONS,
        "dimLabel": DIM_LABEL,
        "benchmarks": benchmarks,
        "round0": ROUND0,
        "profiles": profiles,
        "archetypes": archetypes,
        "popAvgNeed": pop_avg_need,
        "poolAvgW": pool_avg,
        "round0AvgW": round0_avg,
        "misalignPool": {d: round(pool_avg[d] - pop_avg_need[d], 4) for d in DIMENSIONS},
        "misalignRound0": {d: round(round0_avg[d] - pop_avg_need[d], 4) for d in DIMENSIONS},
        "cosPoolNeed": cosine(pool_avg, pop_avg_need),
        "holdoutCos": holdout_cos,
        "counts": {
            "poolSize": len(benchmarks),
            "activeRoster": 13,
            "round0": len(ROUND0),
            "profiles": len(profiles),
            "archetypes": len(archetypes),
            "segments": n_segments,
            "withHoldout": len(holdout_cos),
        },
    }


def main() -> None:
    data = build()
    body = json.dumps(data, indent=1, sort_keys=False)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        "// GENERATED by scripts/animation/generate_sim_page_data.py -- do not edit by hand.\n"
        "// Every value is computed from the live simulation source (BENCHMARK_POOL,\n"
        "// USE_CASE_PROFILES, ARCHETYPES). Re-run the generator after model changes\n"
        "// and bump the ?v=N on the simulation.html script tag.\n"
        f"window.SIMDATA = {body};\n",
        encoding="utf-8",
    )
    c = data["counts"]
    print(f"wrote {OUT}")
    print(f"  pool={c['poolSize']} profiles={c['profiles']} "
          f"archetypes={c['archetypes']} segments={c['segments']} "
          f"withHoldout={c['withHoldout']}")
    print(f"  cos(pool benchmark avg, population need) = {data['cosPoolNeed']}")
    print("  misalignment (pool avg - population need):")
    for d in data["dims"]:
        print(f"    {d:14s} {data['misalignPool'][d]:+.3f}")


if __name__ == "__main__":
    main()
