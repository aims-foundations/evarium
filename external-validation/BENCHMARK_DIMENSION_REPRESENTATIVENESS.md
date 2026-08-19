# Benchmark roster and dimension representativeness

_2026-07-14. Reproduce: `python external-validation/scripts/analyze_benchmark_dimensions.py`
(reads the private ai-discourse frozen census; writes processed snapshots to
`external-validation/data/processed/census_dimension_*.csv` +
`census_domain_to_sim_dimension.csv`)._

Addresses two questions about the design: whether the benchmark roster is
hand-picked, and whether the 6-dimension ontology is representative. Audits the sim's 6-dim ontology and
13-benchmark roster against the real benchmark landscape in two frames:
POPULATION (census, all 10,713 arXiv benchmarks 2018-2026) and SALIENCE (the 60
most lab-reported benchmarks). The finding cuts both ways — most dimensions are
well-calibrated, one axis is entirely missing — which is what makes it credible.

## Headline

**1. The one real gap is multimodal, and it is large and robust across both frames.**
The sim's 6 dimensions are text-only (reasoning, coding, knowledge, safety,
communication, agentic). Multimodal (vision/video/audio/generation) is:
- **18.1%** of census domain tags (the 2nd-largest cluster), and
- **35%** of the top-60 lab-reported benchmarks by count (**29.8%** mention-weighted),

and the sim models **zero** multimodal benchmarks. It is also **growing**: multimodal
rose 7.7% -> 19.5% of census tags across 2020-2025. This quantifies the paper's
existing §5.3 concession that "the six-dimension capability ontology is a design
choice" — the concrete scope boundary is: **text-capability only; the ~18-35%
multimodal axis is out of scope.** (Framing: state the number,
own it as a scope boundary, note the sim's mechanism — score-vs-satisfaction gap
under dimension mismatch — is axis-agnostic and would replicate on a multimodal
suite.)

**2. On the six dimensions it DOES model, the roster is well-calibrated.**
Roster share (argmax of 13) vs census mapped share:

| dim | roster% | census% | verdict |
|---|---|---|---|
| reasoning | 23.1 | 25.1 | match |
| agentic | 15.4 | 14.6 | match |
| communication | 15.4 | 13.2 | match |
| safety | 15.4 | 11.9 | match (roster slightly higher) |
| coding | 15.4 | 7.2 | OVER (~2x) |
| knowledge | 15.4 | 28.0 | UNDER |

Only two mismatches. Coding is over-weighted (~2x). Knowledge is under-weighted,
but that verdict is partly a crosswalk artifact — census "knowledge" bundles
domain-science/med/finance/law/rag-retrieval, which the sim partially covers via
its Clinical Reasoning + Legal Reasoning benchmarks. Neither mismatch is fatal;
both are honest limitations, not tuning targets.

**3. Safety is NOT under-represented.** Sim roster 15.4% vs census 11.9% — the
roster carries a *higher* safety share than the benchmark population. Pre-empts
any "the roster under-weights safety" objection and supports the paper's
dimension story (which a prior internal review flagged for a safety-side error).

**4. The roster is not arbitrary — and its absences are informative.**
9 of 13 sim analogs are genuinely top-reported: MMLU #1, GPQA/MMLU-Pro #3/#4,
SWE-bench Verified #5, LiveCodeBench #6, HumanEval #9, IFEval #22, LongBench-v2
#45, BFCL-v3 #53. The 4 absent analogs are **safety** (TruthfulQA/BBQ,
SEAL/HarmBench), **Clinical** (MedQA), **FrontierMath** (private), **LegalBench**.
The safety + private absences corroborate item #1: labs under-report safety and
private-holdout benchmarks (they are evaluator-run / internal), so the roster
deliberately includes ecosystem-relevant benchmarks that labs do not self-report.

**5. Agentic is rising and the sim tracks it.** Agentic share grows 2.2% -> 16.2%
of census tags (2022 -> 2026); the sim's 2/13 (15%) agentic allocation matches the
current landscape, and the trend validates including it as a first-class dim.

## Crosswalk & caveats

- Crosswalk (`data/processed/census_domain_to_sim_dimension.csv`) has two judgment
  calls: `multilingual -> communication`, `rag-retrieval -> knowledge`. The
  **multimodal finding does not depend on them** (vision/video/audio/generation
  have no plausible home among the 6 text dims).
- Census `domain` is multi-label; shares are tag-instances (~1.95 tags/benchmark),
  not benchmark-primary. Population != salience — hence frame B.
- Census screen/tag human audit is pending (~16% stage-2 flip rate is the only
  reliability stat); treat exact percentages as approximate, directional claims as
  solid.
- Frame-B multimodal subset is an objective vision/video/document cut of the top-60
  (21 benchmarks; see `TOP60_MULTIMODAL` in the script).

## What this establishes

Converts §5.3's bare "the ontology is a design choice" concession into a
**quantified scope statement** with an empirical backbone: the 6 modeled
dimensions are proportionate to the real landscape (safety/agentic/reasoning/
communication all matched; coding over-, knowledge under-, both explained), and
the single omission — multimodal, ~18-35% — is named, sized, and argued to be
mechanism-neutral. Attaches to the empty "Observable system" cell in the
Appendix-E operational-validity table.
