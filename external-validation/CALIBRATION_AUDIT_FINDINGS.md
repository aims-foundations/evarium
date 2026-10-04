# Calibration audit: sim parameters vs empirical measurement

_2026-07-14. Reproduce: `python external-validation/scripts/calibration_audit_table.py`
(reads private ai-discourse census+registry + in-repo Epoch; writes
`external-validation/data/processed/calibration_audit_table.csv`)._

Extends Appendix C's parameter-grounding longtable with corpus/Epoch-measured rows.
The K=3 row is the accepted precedent; these add temporal/structural rows in the
same genre. **Audit only — mismatches are limitations text, never retuning.**
Round = MONTH (canonical mapping; the external-validation README quarterly line is
stale drift).

| # | parameter | sim value | empirical | verdict |
|---|---|---|---|---|
| A | round / run window | 40 mo, Jan 2023–Apr 2026 | registry window 2023-02..2026-06 | **match** |
| B | benchmark intro cadence | 1 / 4 mo (3/yr) | flagship arrival ~1–1.8 / mo | **sim 2–7x slower** |
| C | active roster size | 13 | 10.6 benchmarks/doc | **match** (same order) |
| D | model release tempo | continuous monthly | frontier 0.7–3.5 mo median gap | **round=month OK** |
| E | reporting lag K | 3 mo | 3.0 mo (Epoch, App C) | **anchored** |
| F | saturation → retirement | prompt retire at cap | reported 23–38 mo after saturation | **sim retires too fast** |

## Four rows validate the sim; two surface honest simplifications

**Validated (defensive ammunition):**
- **[A] round=month & the 40-month window** land exactly on the observed
  lab-reporting window (registry `group_min_date` spans 2023-02 to 2026-06).
- **[D] release tempo:** distinct frontier-model releases (Epoch ECI, 2023+,
  same-day variants deduped) arrive every **0.7–3.5 months** (OpenAI 1.0,
  Google DeepMind 0.7, Anthropic 2.4, DeepSeek 2.1, Meta 3.5). The sim's monthly
  capability tick is a well-calibrated granularity for this cadence.
- **[C] roster size 13** vs mean **10.6** benchmarks reported per model card —
  same order; a provider faces ~13 salient benchmarks and reports ~10–11.
- **[E] K=3** is the already-anchored exemplar (Epoch 24-bench × 8-lab, 3.0 mo).

**Two honest mismatches (flag as limitations, with known direction):**

- **[B] The 4-month introduction cooldown is slower than reality AND slower than
  the paper's own prose.** 43 new top-60 benchmarks first entered lab reporting
  across 2024–2025 = **~1.8/month** (an *upper bound* — registry first-mention
  can post-date true debut). The code introduces 1 per 4 months (0.25/mo); App B
  prose says "one category-defining benchmark every 1–2 months" (0.5–1/mo). So
  the prose is closer to reality than the code, and the direction is unambiguous:
  **the sim under-introduces benchmarks (2–7x).** Resolves the internal
  inconsistency: either reconcile the App B prose to the implemented 4-month
  cadence and label it a deliberate tractability simplification (fewer benchmarks
  = cleaner attribution), or note the code is conservative. (Retuning the cooldown
  would require a full re-run, out of scope here.) Context: the census firehose is **148
  benchmarks/yr at ≥100 citations** — the sim's 13-benchmark roster is an explicit
  curated flagship subset, not an attempt to model the full academic stream.

- **[F] Real benchmarks are reported long after they saturate; the sim retires
  promptly.** MMLU's top score plateaus ~2023 (HELM-tracked max 0.881) yet is
  still reported in 2026 (**~38-month** lag); GSM8K plateaus ~mid-2024, still
  reported 2026 (**~23-month** lag). The sim retires a saturated benchmark once at
  the roster cap. This *understates* the persistence of saturated public
  benchmarks as a continued gaming surface — arguably a point in the paper's favor
  (saturated-but-still-reported benchmarks are exactly where score-vs-value gaps
  fester), so worth flagging as a limitation that cuts toward the thesis, not
  against it. (Plateau dates carry HELM data-source noise; the large lag is robust.)

## Caveats

- Row B first-mention is an upper bound on true debut; a true-debut version needs
  the census↔registry join (blocked). The direction (sim under-introduces) holds
  regardless.
- Row F plateau detection is running-max within 0.02 of the series max; HELM caps
  MMLU ~0.88 (real frontier ~0.90+), so plateau dates are approximate; the
  saturation→still-reported lag (the point) is robust.
- Registry is human-audited (0 major errors); Epoch is public CC-BY. Directional
  claims solid; exact figures approximate.

## What this establishes

A single table showing the sim's temporal/structural backbone is empirically
grounded (round=month, run window, release tempo, roster size, K all check out),
with two simplifications named, signed, and sourced rather than hidden — the exact
posture Appendix C already takes for K=3, now extended. Fills more of the empty
"Observable system" cell in the Appendix-E operational-validity table.
