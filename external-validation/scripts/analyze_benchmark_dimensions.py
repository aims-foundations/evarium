"""
analyze_benchmark_dimensions.py

Roster and dimension representativeness audit.
Audits the simulation's 6-dimension capability ontology and 13-benchmark roster
against the real benchmark landscape (ai-discourse benchmark census, 10,713
benchmarks 2018-2026), to test whether the roster is hand-picked and whether
the 6-dim ontology is representative.

Two frames:
  A. POPULATION  -- census `domain` composition (all 10,713 arXiv benchmarks),
     mapped to the sim's 6 dims via a published crosswalk; unmodeled domains
     (multimodal, long-context, efficiency) bucketed explicitly. Plus year trend.
  B. SALIENCE    -- the 60 most lab-reported benchmarks (registry test_top60):
     multimodal share (objective cut) + which sim-roster analogs are/aren't
     actually top-reported.

The sim's 6 dims are TEXT-ONLY (reasoning, coding, knowledge, safety,
communication, agentic) -- there is no multimodal axis. The headline finding is
the size of that gap, robust across both frames.

Caveats: census `domain` is multi-label (counts are tag-instances, ~1.95/bench);
census screen/tag human audit pending (~16% stage-2 flip rate is the only
reliability stat); population != salience (hence frame B); the crosswalk has
judgment calls (multilingual->communication, rag-retrieval->knowledge) that are
flagged -- the multimodal finding does not depend on them.

Reads the private frozen census from the ai-discourse repo; writes a processed
snapshot + crosswalk into data/processed/ so downstream runs are self-contained.
"""

import csv
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
EXTVAL = os.path.dirname(HERE)  # external-validation/
PROC = os.path.join(EXTVAL, "data", "processed")

# Private source (ai-discourse repo). Processed snapshot below makes reruns
# self-contained if this path is unavailable.
CENSUS_FROZEN = r"C:\Users\yashd\Desktop\ai-discourse\research\lab-reporting\data\linking\frozen_20260623\census.csv"
TOP60 = r"C:\Users\yashd\Desktop\ai-discourse\research\lab-reporting\data\linking\test_top60.csv"

# --- Crosswalk: census 20 `domain` values -> sim 6 dims (+ explicit UNMODELED) ---
# UNMODELED buckets are named so the gap is visible, not hidden. Judgment calls
# are flagged in comments; the multimodal gap is robust to them.
CROSSWALK = {
    "reasoning": "reasoning",
    "math": "reasoning",
    "coding": "coding",
    "knowledge-qa": "knowledge",
    "domain-science": "knowledge",
    "domain-med": "knowledge",
    "domain-finance": "knowledge",
    "domain-law": "knowledge",
    "rag-retrieval": "knowledge",          # judgment: retrieval-QA -> knowledge
    "safety-alignment": "safety",
    "agents-tool-use": "agentic",
    "instruction-following": "communication",
    "multilingual": "communication",       # judgment: language coverage -> communication
    "vision-multimodal": "UNMODELED:multimodal",
    "video": "UNMODELED:multimodal",
    "audio": "UNMODELED:multimodal",
    "image-video-generation": "UNMODELED:multimodal",
    "long-context": "UNMODELED:other",     # sim awkwardly folds long-context into communication
    "efficiency": "UNMODELED:other",
    "other": "UNMODELED:other",
}

SIM_DIMS = ["reasoning", "coding", "knowledge", "safety", "communication", "agentic"]

# --- Sim 13-benchmark roster (run_experiment.py:225-379), full 6-dim vectors ---
# (name, real-world analog, {dim: weight}). primary dim = argmax.
ROSTER = [
    ("General Capability", "MMLU",            {"reasoning":.35,"coding":.08,"knowledge":.30,"safety":.05,"communication":.20,"agentic":.02}),
    ("Coding Evaluation",  "HumanEval",        {"reasoning":.10,"coding":.78,"knowledge":.03,"safety":.01,"communication":.02,"agentic":.06}),
    ("Safety Evaluation",  "TruthfulQA/BBQ",   {"reasoning":.03,"coding":.01,"knowledge":.05,"safety":.80,"communication":.10,"agentic":.01}),
    ("Instruction Following","MT-Bench/IFEval",{"reasoning":.08,"coding":.02,"knowledge":.05,"safety":.04,"communication":.80,"agentic":.01}),
    ("Scientific Reasoning","GPQA/MMLU-Pro",   {"reasoning":.78,"coding":.02,"knowledge":.15,"safety":.00,"communication":.04,"agentic":.01}),
    ("Clinical Reasoning", "MedQA",            {"reasoning":.20,"coding":.01,"knowledge":.65,"safety":.08,"communication":.05,"agentic":.01}),
    ("Adversarial Robustness","SEAL/HarmBench",{"reasoning":.06,"coding":.01,"knowledge":.01,"safety":.85,"communication":.04,"agentic":.03}),
    ("Hard Coding",        "LiveCodeBench",    {"reasoning":.10,"coding":.80,"knowledge":.02,"safety":.01,"communication":.01,"agentic":.06}),
    ("Agentic Tasks",      "SWE-bench",        {"reasoning":.25,"coding":.19,"knowledge":.01,"safety":.00,"communication":.07,"agentic":.48}),
    ("Advanced Math",      "FrontierMath",     {"reasoning":.85,"coding":.06,"knowledge":.05,"safety":.00,"communication":.03,"agentic":.01}),
    ("Function Calling",   "BFCL",             {"reasoning":.15,"coding":.30,"knowledge":.02,"safety":.01,"communication":.12,"agentic":.40}),
    ("Long Context",       "LongBench-v2",     {"reasoning":.12,"coding":.02,"knowledge":.20,"safety":.01,"communication":.62,"agentic":.03}),
    ("Legal Reasoning",    "LegalBench",       {"reasoning":.25,"coding":.01,"knowledge":.60,"safety":.05,"communication":.08,"agentic":.01}),
]

# --- Frame B: objective multimodal subset of the top-60 (vision/video/doc/OCR) ---
TOP60_MULTIMODAL = {
    "MMMU","MMMU-Pro","MathVista","DocVQA","ChartQA","AI2D","OCRBench",
    "VideoMME (w sub.)","VideoMMMU","MMStar","RealWorldQA","ScreenSpot Pro",
    "LVBench","MVBench","MMLongBench-Doc","MathVision","RefCOCO(avg)","BLINK",
    "ERQA","HallusionBench","TextVQA",
}
# sim-roster analogs and whether each is present in the top-60 (by mention rank).
ROSTER_TOP60_HIT = {
    "MMLU":"#1","HumanEval":"#9","TruthfulQA/BBQ":"ABSENT (safety under-reported)",
    "MT-Bench/IFEval":"IFEval #22 (MT-Bench absent)","GPQA/MMLU-Pro":"#3 / #4",
    "MedQA":"ABSENT","SEAL/HarmBench":"ABSENT (safety under-reported)",
    "LiveCodeBench":"#6","SWE-bench":"SWE-bench Verified #5",
    "FrontierMath":"ABSENT (private under-reported); MATH #2 / AIME present",
    "BFCL":"BFCL-v3 #53","LongBench-v2":"#45","LegalBench":"ABSENT",
}


def load_census():
    with open(CENSUS_FROZEN, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def frame_a(rows):
    """Population: census domain -> sim dim composition (overall + by year)."""
    overall = Counter()
    by_year = defaultdict(Counter)
    unknown_domains = Counter()
    for r in rows:
        y = (r.get("date", "") or "")[:4]
        for d in (r.get("domain", "") or "").split("|"):
            d = d.strip()
            if not d:
                continue
            mapped = CROSSWALK.get(d)
            if mapped is None:
                unknown_domains[d] += 1
                mapped = "UNMODELED:other"
            overall[mapped] += 1
            by_year[y][mapped] += 1
    return overall, by_year, unknown_domains


def roster_distribution():
    """Sim roster dimension mass: argmax-count and summed-weight."""
    argmax = Counter()
    weight = Counter()
    for name, analog, vec in ROSTER:
        primary = max(vec, key=vec.get)
        argmax[primary] += 1
        for dim, w in vec.items():
            weight[dim] += w
    total_w = sum(weight.values())
    return argmax, weight, total_w


def pct(x, tot):
    return (100.0 * x / tot) if tot else 0.0


def main():
    os.makedirs(PROC, exist_ok=True)
    rows = load_census()
    overall, by_year, unknown = frame_a(rows)
    total_tags = sum(overall.values())

    # mapped-only (6 sim dims) renormalization
    mapped_total = sum(v for k, v in overall.items() if not k.startswith("UNMODELED"))
    argmax, rweight, rtotal = roster_distribution()

    print("=" * 70)
    print("FRAME A -- POPULATION (census 10,713 benchmarks, domain tag-instances)")
    print("=" * 70)
    print("Total domain-tag instances: %d (multi-label, ~%.2f tags/benchmark)"
          % (total_tags, total_tags / len(rows)))
    print("\nComposition (all buckets, %% of tags):")
    order = SIM_DIMS + ["UNMODELED:multimodal", "UNMODELED:other"]
    for k in order:
        print("  %-24s %5d  (%4.1f%%)" % (k, overall[k], pct(overall[k], total_tags)))
    print("\n  --> UNMODELED total: %d (%.1f%%); of which multimodal %d (%.1f%%)"
          % (overall["UNMODELED:multimodal"] + overall["UNMODELED:other"],
             pct(overall["UNMODELED:multimodal"] + overall["UNMODELED:other"], total_tags),
             overall["UNMODELED:multimodal"], pct(overall["UNMODELED:multimodal"], total_tags)))

    print("\nSIM ROSTER vs CENSUS (6 dims only, renormalized):")
    print("  %-14s %8s %8s %10s" % ("dim", "roster%", "census%", "verdict"))
    for d in SIM_DIMS:
        rp = pct(argmax[d], 13)                  # roster argmax share
        rw = pct(rweight[d], rtotal)             # roster weight share
        cp = pct(overall[d], mapped_total)       # census mapped share
        # verdict on argmax-share vs census
        diff = rp - cp
        verdict = "match" if abs(diff) < 5 else ("OVER" if diff > 0 else "UNDER")
        print("  %-14s %6.1f%% %6.1f%%   %s (wt %4.1f%%)" % (d, rp, cp, verdict, rw))

    print("\nYEAR TREND -- multimodal (UNMODELED) share of tags by census year:")
    for y in sorted(k for k in by_year if k and k >= "2020"):
        yt = sum(by_year[y].values())
        mm = by_year[y]["UNMODELED:multimodal"]
        ag = by_year[y]["agentic"]
        print("  %s  multimodal %4.1f%%   agentic %4.1f%%   (n_tags=%d)"
              % (y, pct(mm, yt), pct(ag, yt), yt))

    # Frame B
    with open(TOP60, encoding="utf-8-sig") as f:
        t60 = list(csv.DictReader(f))
    mm_rows = [r for r in t60 if r["canonical"] in TOP60_MULTIMODAL]
    mm_ment = sum(int(r["total_mentions"]) for r in mm_rows)
    tot_ment = sum(int(r["total_mentions"]) for r in t60)
    print("\n" + "=" * 70)
    print("FRAME B -- SALIENCE (top-60 lab-reported benchmarks)")
    print("=" * 70)
    print("Multimodal share of top-60: %d/60 (%.1f%%) by count; %.1f%% by mentions"
          % (len(mm_rows), pct(len(mm_rows), 60), pct(mm_ment, tot_ment)))
    print("  --> the sim roster models ZERO multimodal benchmarks.")
    print("\nSim-roster analogs in the top-60 (roster is NOT arbitrary where it covers):")
    for analog, hit in ROSTER_TOP60_HIT.items():
        print("  %-18s -> %s" % (analog, hit))

    # --- write processed snapshots (self-contained downstream) ---
    with open(os.path.join(PROC, "census_domain_to_sim_dimension.csv"), "w",
              encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["census_domain", "sim_dimension"])
        for k, v in CROSSWALK.items():
            w.writerow([k, v])
    with open(os.path.join(PROC, "census_dimension_composition.csv"), "w",
              encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["bucket", "tag_instances", "pct_of_all_tags"])
        for k in order:
            w.writerow([k, overall[k], "%.2f" % pct(overall[k], total_tags)])
    with open(os.path.join(PROC, "census_dimension_by_year.csv"), "w",
              encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year"] + order + ["n_tags"])
        for y in sorted(k for k in by_year if k):
            yt = sum(by_year[y].values())
            w.writerow([y] + [by_year[y][k] for k in order] + [yt])
    print("\nWrote 3 processed CSVs to %s" % PROC)
    if unknown:
        print("WARNING unmapped census domains (fell to UNMODELED:other):", dict(unknown))


if __name__ == "__main__":
    main()
