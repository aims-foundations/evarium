# Paper verification checklist & NeurIPS response draft

Last updated: 2026-04-24 (session 51).

Two parts:
- **Part A** — general paper verification checks (formatting, consistency, citation, compilation).
- **Part B** — NeurIPS paper checklist (`overleaf/checklist.tex`) with skeleton draft answers for each of the 16 items. Fill these in before submission; NeurIPS desk-rejects papers without a completed checklist.

---

## Part A — General paper checks

### Correctness / consistency
1. **Numerical consistency across main body.** Seed counts, N values, percentages, HHI, quoted deltas must agree where repeated. Already found: §5 intro `N=5 per condition` vs Fig 4 caption `N=4` vs §5.2 body `N=4–5`. Resolve to one phrasing.
2. **Caption ↔ body agreement.** Every claim in a figure/table caption ("9 of 11 benchmarks agree", "$\sim$26% reduction in HHI") must match a body claim exactly or be clearly derivable.
3. **Ground-truth values across appendices.** `base incident rate = 20%/provider/round`, `K=3`, `cos=0.85 / 0.95`, `benchmark_orientation=0.80`, `48 consumer segments`, seeds `42–46`, `benchmark_introduction_cooldown=4`. Quote once authoritatively, reference elsewhere.
4. **Appendix letters match inclusion order.** Appendices were renamed; verify rendered order matches cross-references (`\ref{app:architecture}` really points to `Appendix A`, etc.).
5. **Orphan section files.** `sections/5diagnostic.tex` and `sections/6scope.tex` exist but aren't in `main.tex`. Contain undefined refs (`sec:diag-results`, `sec:appendix-diagnostics`) and duplicate `sec:limitations` label. Safe while orphaned; re-including without fixing will break.

### Compilation (need fresh Overleaf log; the local copy is stale)
6. **Overfull/underfull hbox warnings** — refresh after recent table + paragraph edits.
7. **Undefined references** — grep log for `LaTeX Warning: Reference.*undefined`.
8. **Labels defined but never referenced** — harmless but can be pruned.
9. **Duplicate labels** — LaTeX emits a warning; confirm the `sec:limitations` duplicate (live in 5exp.tex, orphan in 6scope.tex) isn't silently resolving wrong.

### Style / formatting
10. **Title case consistency.** Mix of title case (*"Simulator as Hypothesis Generator"*) and sentence case (*"A catalog of simulation case studies"*). Pick one.
11. **Abbreviation discipline.** First use expanded, later abbreviated. Audit: HHI, CI, R&D, AIID, PIMMUR, V&V, RLHF, CoT, CRN.
12. **Floats placement.** `[!htb]` used mostly; check no figure floats far from its reference.
13. **Equation numbering.** Number only equations you reference; unnumber the rest.

### Bibliography
14. **DOI/URL present** — NeurIPS accepts both; audit for missing.
15. **Preprint vs published** — some entries likely `arxiv:xxxx` when a peer-reviewed version exists.
16. **Unused bib entries** — ~47 in `references.bib`; prune for cleanliness.

### Anonymization (submission version)
17. **Author names, institution, funding sources** stripped.
18. **Acknowledgments** (`\ack{}`) hidden in anonymous submission via `preprint` vs `final` flag in NeurIPS style.
19. **Self-cites** anonymized.
20. **Supplementary code URL** anonymized (anonymous GitHub / anonymous drive).

---

## Part B — NeurIPS checklist: skeleton responses

Copy these into `checklist.tex`, replacing each `\answerTODO{}` and `\justificationTODO{}`. All draft text below is a starting point — **edit to match actual submission state before locking**.

---

**1. Claims.** Do the main claims made in the abstract and introduction accurately reflect the paper's contributions and scope?

- Answer: `\answerYes{}`
- Justification: The abstract and §1 state the paper's contributions (ecosystem-level multi-agent simulation; privacy-ladder case study showing per-benchmark gap redistribution; catalog of additional case studies) and explicitly scope claims as hypothesis-generating and directional rather than predictive. Limitations are discussed in §5.4 and Appendix J.

**2. Limitations.** Does the paper discuss the limitations of the work?

- Answer: `\answerYes{}`
- Justification: §5.4 discusses two classes of limitation (per-actor action-space simplifications; absence of out-of-sample prediction), with extended treatment in Appendix J.

**3. Theory assumptions and proofs.** For each theoretical result, full assumptions and a complete proof?

- Answer: `\answerNA{}`
- Justification: The paper presents an empirical simulation study and does not contain formal theorems or proofs. §4.1 states a generative measurement model (Eq. 1) with assumptions stated inline, but makes no theoretical claim about it.

**4. Experimental result reproducibility.** Does the paper fully disclose information needed to reproduce the main experimental results?

- Answer: `\answerYes{}`
- Justification: The simulation protocol (Appendix A), full actor prompts (Appendix D), hyperparameters with empirical grounding (Appendix K), and the privacy-ladder batch specification (§5.2 and Appendix G) are documented. LLM models (Claude Sonnet 4.6 and Opus 4.7), seed set (42–46), and round count (40 rounds per run) are stated.

**5. Open access to data and code.** Does the paper provide open access to code and data with reproduction instructions?

- Answer: `\answerYes{}` **[CONFIRM BEFORE LOCKING — depends on actual release plan]**
- Justification: Simulation code and privacy-ladder run artifacts are released at `[ANONYMIZED URL TBD]` with a README, per-experiment runbook, and `rounds.jsonl` / `memory.json` / `summary.json` per run. **Alt (if no release): `\answerNo{}` with justification "Code and run artifacts will be released upon publication; available to reviewers via the conference's confidential-review channel on request."**

**6. Experimental setting/details.** Does the paper specify all training/test details?

- Answer: `\answerYes{}`
- Justification: §5 and Appendices A/G/K specify the simulation protocol (6 providers, 48 consumer segments, 40-round horizon), seed set (42–46 matched for paired comparisons), LLM parameters (temperature 0; JSON-validation retry protocol in Appendix G), and privacy-condition definitions (§5.2).

**7. Experiment statistical significance.** Error bars reported suitably and correctly defined?

- Answer: `\answerYes{}`
- Justification: Figures 4, per-benchmark decompositions (App G), and Sonnet-vs-Opus comparisons (App H) report 95% confidence intervals computed as 1.96·σ/√n from seed-level means, with n labeled explicitly. Heuristic conditions use N=30 seeds; LLM conditions use N=4–5 seeds. Method stated in App G.

**8. Experiments compute resources.** Sufficient information to reproduce the compute?

- Answer: `\answerYes{}` **[CONFIRM: verify total-project-compute statement]**
- Justification: Per-run compute is documented in App H.6 (~65 min Sonnet / ~77 min Opus wall-clock for a 40-round run; ~$10–$30 per run at current Anthropic API rates). Total reported compute across the privacy-ladder batch and robustness runs: **[APPROX TBD, likely ~60–80 matched LLM runs]**. Preliminary calibration runs not included in the reported batch consumed an additional **[APPROX]** hours.

**9. Code of ethics.** Does the research conform to the NeurIPS Code of Ethics?

- Answer: `\answerYes{}`
- Justification: The research conforms to the NeurIPS Code of Ethics. No human subjects were harmed; practitioner interview participants (§5.3) provided informed consent **[CONFIRM: per institutional protocol]**.

**10. Broader impacts.** Does the paper discuss positive and negative societal impacts?

- Answer: `\answerYes{}` **[NEEDS A DEDICATED BLOCK — current draft scattered across §5.5 and §6]**
- Justification: §6 discusses broader impacts. Positive: the simulation framework clarifies which evaluator design choices (benchmark composition, privacy, business model) shape developer incentives, enabling policy stress-testing before deployment. Negative: results are directional and may be misread as prescriptive; simulated interventions are not validated against real-world magnitudes; practitioner interviews informed actor design but may bias the design space toward interviewed stakeholders.

**11. Safeguards.** Describe safeguards for high-risk data/model release?

- Answer: `\answerNA{}`
- Justification: The paper does not release new pre-trained models, scraped datasets, or generative systems with high misuse risk. Released artifacts are simulation code and structured run logs.

**12. Licenses for existing assets.** Creators credited, licenses respected?

- Answer: `\answerYes{}`
- Justification: LLM actor calls use the Claude API under Anthropic Terms of Service (Claude Sonnet 4.6, Opus 4.7). Referenced benchmarks (MMLU, HumanEval, SWE-bench, FrontierMath, and others in §4 / Appendix A) are cited to their source publications. No datasets are repackaged or redistributed.

**13. New assets.** New assets well documented?

- Answer: `\answerYes{}` **[CONFIRM: README + documentation actually exists in released repo]**
- Justification: The simulation codebase is released with a README, `CLAUDE.md` (architecture reference), and per-experiment runbook. Per-run artifacts (`rounds.jsonl`, `memory.json`, `summary.json`) are included for the reported privacy-ladder batch.

**14. Crowdsourcing and research with human subjects.** Full instructions to participants and compensation details?

- Answer: `\answerYes{}` **[IF interviews were formally conducted — CONFIRM and fill details]**
- Justification: §5.3 cites practitioner interviews that informed actor design. Interviews were semi-structured, opt-in, with **[N]** participants recruited through **[channel]**. **[Compensation details: either "No compensation" or "$X per hour"]**. Consent was obtained per institutional protocol; transcripts are not released to preserve participant anonymity.
- **Alt if no formal interview protocol: `\answerNA{}` with "Actor design was informed by informal conversations with practitioners, not formal crowdsourcing or human-subjects research."**

**15. IRB.** IRB approvals / equivalent?

- Answer: `\answerYes{}` **[IF interviews are in scope — CONFIRM with institution's IRB status]**
- Justification: The interview protocol referenced in §5.3 was reviewed by **[institution]** IRB (**[exempt/approved]** determination, protocol **[ID-OR-EXEMPT-CATEGORY]**). No sensitive or identifying data was collected.
- **Alt if no interviews or no IRB: `\answerNA{}` with justification matching item 14.**

**16. Declaration of LLM usage.** LLMs used in a core / non-standard way?

- Answer: `\answerYes{}`
- Justification: LLMs are a core method component: providers, regulator, funders, and media triggers are driven by Claude Sonnet 4.6 reasoning over observed public state (Opus 4.7 used for robustness in Appendix H). LLM outputs are non-deterministic even at temperature 0 due to server-side sampling; a fully rule-based heuristic mode serves as a cross-mode validation layer to isolate LLM-specific findings (Appendix G). Full actor prompts in Appendix D.

---

## Priority resolution order (before submission lock)

1. **Item 14 + 15** — confirm interview status. If §5.3 claims interview-informed actor design, the IRB/consent story has to exist. If interviews were informal (no protocol), soften §5.3's claim to "informed by practitioner conversations" and answer NA.
2. **Item 5** — decide release plan (public repo vs. reviewer-access). Commit anon URL before submission.
3. **Item 10** — draft a dedicated broader-impacts paragraph in §6 (current content is scattered).
4. **Item 8** — total-project compute: estimate Sonnet+Opus run count × per-run cost, add calibration overhead.
5. **Item 16** — already Yes; just draft the full paragraph per skeleton above.
6. **Part A #1–#5** — numerical + reference consistency pass once Overleaf re-compiles.
