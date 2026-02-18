# exp030 Post-Run Analysis

**Experiment:** exp_030_baseline_with_incidents_v1
**Intended mode:** LLM (Anthropic, llm_mode=True, consumer_llm_organizations=True)
**Actual mode:** Heuristic fallback on every round (see Issue 1 below)
**Rounds:** 10

---

## What Went Wrong

### Issue 1: LLM mode never ran — silent fallback to heuristic on every round

`llm_mode=True` was set, but every Anthropic API call returned a 404 "model not found" error (first for `phi3` left in `LLM_MODEL` env var from Ollama, then for `claude-3-5-haiku-20241022` which the API key couldn't access). The `_plan_llm()` method catches exceptions and silently falls back to `_plan_heuristic()` with only a printed line, not an interruption. Tokens were still consumed by the failed API calls.

Confirmation: provider allocation trajectories show pure mechanical heuristic drift, e.g. Anthropic the company:
```
R0: 30/20/10/40
R1: 26/20/14/40  <- competitive gap grinding fundamental down, eval_eng up
...
R9:  5/20/36/40
```
No LLM reasoning would produce that steady linear drift. Final summary also shows "Strategy shifts: 0".

No "Organizational Consumer Reasoning (LLM)" sections appear anywhere in the game log, confirming org consumers also ran heuristic throughout.

**To fix:** Resolve API key model access (billing tier), and add a hard-stop option when fallback occurs so the run can be interrupted rather than wasting API credits silently.

### Issue 2: Benchmark churn too aggressive for 10-round runs

8 benchmarks were introduced across 9 rounds:
- R2: writing (saturation: reasoning=0.9197)
- R3: medical (saturation: reasoning=0.9197)
- R4: legal (saturation: reasoning=1.0)
- R5: finance (saturation: coding=0.9661)
- R6: instruction_following (saturation: coding=1.0)
- R7: long_context (saturation: coding=1.0)
- R8: coding_advanced (saturation: coding=1.0)
- R9: reasoning_advanced (saturation: coding=1.0)

Root cause: initial validity=0.70 + exploitability=0.25 + providers at 25-55% eval_eng = saturation threshold (0.90) hit within 2 rounds. The `coding` benchmark triggered introductions in R5, R6, R7, R8, R9 because the saturation state wasn't clearing after firing. Benchmarks had no time to create meaningful differentiation before being replaced.

**To fix for 10-round runs:** Raise `benchmark_introduction_cooldown` to 8-10 and lower `max_benchmarks` to 6. Current settings are calibrated for 50-round runs.

### Issue 3: Funder allocations locked rigid

TechVentures ($171M) and Horizon_Capital ($57M) concentrated on OpenAI through R3, then rigidly on MetaAI for R4-9 with zero variation. Once MetaAI took the #1 spot it never lost it, so the VC 60/30/10 split never reassigned. The leader received 3x more funding than #2 for 7 straight rounds with no corrective mechanism. AISI also locked similarly.

### Issue 4: Incident safety pressure overwhelmed by competitive pressure

One visible incident: Google bias/discrimination in R4 (major severity). Google's safety did tick up R4→R5 (5%→10%), confirming the incident pressure code fired. But competitive pressure immediately resumed pushing safety back down (R6: 5% again). The competitive gap pressure is an order of magnitude stronger than the incident safety nudge in heuristic mode.

---

## What Worked Correctly

- **Benchmark introduction sequence** fired in the correct order (writing first, then domain-specific, then advanced)
- **Goodhart's Law detected correctly:** MetaAI finished #1 on scores (0.907) but OpenAI had highest true capability (0.754) the entire run
- **StartupDotAI gaming visible:** score 0.889 vs true_cap 0.598 — largest score inflation gap (0.291) of any provider; 55% eval_eng throughout
- **Regulatory escalation correct:** investigation (R1) → mandate_benchmark (R4) → public_warning (R7)
- **Market dynamics coherent:** MetaAI gaining share via gaming, Anthropic stuck at ~5% despite highest safety investment
- **Incident system fired:** Google bias incident generated correct media headline and risk signal

---

## Final Standings

| Rank | Provider | Final Score | True Cap | Avg EvalEng | Notes |
|------|----------|-------------|----------|-------------|-------|
| 1 | MetaAI | 0.907 | 0.677 | 46% | Goodhart winner — highest score, not highest capability |
| 2 | OpenAI | 0.888 | 0.754 | 22% | Highest true capability, lost on gaming |
| 3 | Google | 0.869 | 0.698 | 35% | Had 1 major incident (bias), safety dropped anyway |
| 4 | Anthropic | 0.860 | 0.682 | 24% | Highest safety (40%), lowest cap growth (+0.032) |
| 5 | StartupDotAI | 0.828 | 0.607 | 53% | Most extreme gaming, peaked at #1 in R6 |

---

## Config Changes Needed Before Next LLM Run

1. Verify `ANTHROPIC_API_KEY` has billing enabled and model access at console.anthropic.com
2. Set `LLM_MODEL` in `.env` to a confirmed accessible model (e.g. `claude-3-haiku-20240307`)
3. For 10-round runs: set `benchmark_introduction_cooldown=8`, `max_benchmarks=6`
4. Add explicit fallback logging / abort option to prevent silent heuristic substitution consuming API credits
