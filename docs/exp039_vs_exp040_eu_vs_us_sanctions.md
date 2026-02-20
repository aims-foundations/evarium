# exp039 vs exp040: EU Precautionary vs US Light-Touch (Sanctions Era)

**Date:** 2026-02-18
**Experiments:** exp039 (`eu_precautionary_sanctions_v1`) vs exp040 (`us_lighttouch_sanctions_v1`)
**Feature under test:** `sanctions_and_fines` Tier 2 policymaker action (first runs with this feature)

---

## 1. Setup

| | exp039 | exp040 |
|---|---|---|
| Experiment | `eu_precautionary_sanctions_v1` | `us_lighttouch_sanctions_v1` |
| Shared conditions | 5 providers, 30 rounds, LLM mode (Anthropic), 4 initial benchmarks + 12-item sequence, 39 consumer segments, 3 funders, incidents enabled, no eval-as-company |

---

## 2. Regulatory Parameters

| Parameter | EU (039) | US (040) |
|---|---|---|
| intervention_threshold | 0.35 | 0.75 |
| risk_tolerance | 0.2 | 0.7 |
| Fine formula factor (1 − risk_tol) | 0.8 | 0.3 |

---

## 3. Interventions (Round-by-Round)

| Round | EU (039) | US (040) |
|---|---|---|
| R1 | investigation | investigation |
| R4 | public_warning | public_warning |
| R7 | threshold_announcement | threshold_announcement |
| R10 | emergency_investigation → Anthropic | emergency_investigation → Anthropic |
| R23 | **sanctions_and_fines → Anthropic** (fine=1.9%) | — |
| R25 | — | **sanctions_and_fines → OpenAI** (fine=1.3%) |
| R26 | **sanctions_and_fines → Google** (fine=1.9%) | — |
| R28 | — | **mandate_benchmark** (validity→0.80, exploitability→0.30) |
| R29 | **sanctions_and_fines → Google** (fine=1.5%, new cycle) | — |
| **Total** | **7** | **6** |

Both runs followed the same escalation path through R10 — the divergence began at R23/R25. EU issued 3 sanctions and no mandate. US issued 1 sanction and then escalated to a benchmark mandate at R28.

The sanctions fine sizes were modest: EU fines peaked at ~1.9% R&D efficiency reduction. This is because the targeted providers (Anthropic, Google) had small market shares at the time — the formula's `market_share` factor kept penalties low even with the EU's aggressive `(1−risk_tol)=0.8` multiplier.

---

## 4. Incidents

| Severity | EU (039) | US (040) |
|---|---|---|
| critical | 1 | 1 |
| major | 3 | 2 |
| moderate | 4 | 3 |
| minor | 8 | 6 |
| **Total** | **16** | **12** |

| By provider | EU (039) | US (040) |
|---|---|---|
| Anthropic | **8** | 4 |
| Google | 4 | 2 |
| StartupDotAI | 2 | 2 |
| OpenAI | 1 | 2 |
| MetaAI | 1 | 2 |

Critical incident: EU — **Anthropic R23** (DOJ civil rights suit). US — **OpenAI R25** (same incident type). These directly triggered the respective sanctions.

---

## 5. Key Event Narrative

**EU run:** The EU regulator fired quickly — investigation at R1, warning at R4. Anthropic became a repeated incident target (8 incidents) and drew an emergency investigation at R10. By R23, a critical incident triggered the first sanction (Anthropic, fine=1.9%). Google then accumulated major incidents and was sanctioned at R26 and again at R29. The EU never escalated to a benchmark mandate — the sanctions pathway absorbed regulatory energy.

**US run:** Identical early escalation through R10. With its high risk tolerance (0.7), the US regulator sat quiet from R10–R24. OpenAI's critical incident at R25 finally triggered a sanction (1.3% fine). Three rounds later, the US issued a benchmark mandate (R28), forcing validity=0.80 and exploitability=0.30. The mandate came very late (2 rounds before end) and had little time to affect outcomes.

---

## 6. Final Market Shares

| Provider | EU (039) | US (040) |
|---|---|---|
| OpenAI | **48.1%** | 7.9% |
| MetaAI | 37.9% | 13.2% |
| Anthropic | 4.5% | **50.7%** |
| Google | 6.3% | 25.6% |
| StartupDotAI | 3.1% | 2.6% |

Market outcomes flipped completely. In EU, OpenAI+MetaAI captured 86% (high two-firm concentration). In US, Anthropic+Google took 77%. The market leader in each run was the provider that avoided being sanctioned or heavily incident-targeted and received the resulting funding flow advantage.

---

## 7. True Capabilities (Final)

| Provider | EU (039) | US (040) |
|---|---|---|
| OpenAI | **0.787** | 0.746 |
| Anthropic | 0.735 | **0.767** |
| Google | 0.704 | 0.718 |
| MetaAI | 0.692 | 0.676 |
| StartupDotAI | 0.639 | 0.633 |
| **Avg growth** | **+0.257** | **+0.254** |

Aggregate capability growth was nearly identical. The leader swapped: EU's OpenAI (+0.297) vs US's Anthropic (+0.267). Funding multipliers explain this — OpenAI received 1.46x in EU, Anthropic received 1.45x in US.

---

## 8. Safety Alignment (Mean over 30 Rounds)

| Provider | EU (039) | US (040) |
|---|---|---|
| OpenAI | 0.195 | 0.203 |
| Anthropic | 0.199 | **0.214** |
| Google | 0.202 | 0.173 |
| MetaAI | 0.149 | 0.161 |
| StartupDotAI | 0.161 | 0.166 |
| **Avg** | **0.181** | **0.183** |

US providers averaged slightly higher safety investment. The EU's aggressive early interventions pushed providers toward fundamental research (EU avg research: 0.46) but not specifically toward safety.

---

## 9. Benchmark Quality (Final)

| Metric | EU (039) | US (040) |
|---|---|---|
| Benchmark validity | 0.677 | **0.799** |
| Benchmark exploitability | 0.257 | 0.300 |
| Validity correlation | **0.922** | 0.910 |

The US benchmark mandate (R28) artificially elevated validity to 0.80. EU benchmarks degraded more through natural Goodhart decay (0.677) — but EU's validity correlation was higher (0.922 vs 0.910), meaning scores tracked true capability more accurately despite the lower nominal validity. This reflects EU providers' earlier pivot away from eval engineering (EU final avg eval_eng=0.024 vs US=0.036).

---

## 10. Consumer Satisfaction

| Metric | EU (039) | US (040) |
|---|---|---|
| Mean satisfaction (30 rounds) | 0.676 | **0.686** |
| Final satisfaction (R29) | **0.786** | 0.745 |
| Avg switching rate | 0.083 | 0.085 |

US had higher mean satisfaction across the run; EU had higher final-round satisfaction (still climbing at R29; US peaked ~R20 then dipped after OpenAI sanctions disrupted the R25–R28 period).

---

## 11. Hypothesis Verification

| Hypothesis | Result | Numbers |
|---|---|---|
| H1: EU reduces incident count | **WRONG** | EU: 16 incidents, US: 12 |
| H2: US achieves higher final capabilities | **WRONG** | Avg growth nearly equal (0.257 EU vs 0.254 US) |
| H3: US leads to more market concentration | **WRONG** | EU 2-firm concentration higher (86% vs 77%) |
| H4: EU forces more safety investment | **WRONG** | US avg safety slightly higher (0.183 vs 0.181) |
| H5: EU maintains higher consumer satisfaction | **PARTIAL** | EU higher final (0.786 vs 0.745), US higher mean (0.686 vs 0.676) |

---

## 12. Summary

All five standard EU-vs-US hypotheses came back wrong or partial — the dominant driver of outcomes in both runs was **which provider got sanctioned**, not the regulatory style itself. In EU, Anthropic accumulated 8 incidents and drew 2 sanctions; losing funding flow, it collapsed to 4.5% market share while OpenAI (largely untouched) surged to 48%. In US, OpenAI was sanctioned and then the late benchmark mandate disrupted the landscape, benefiting Anthropic (which ended at 51%).

The sanctions themselves were economically mild (1.3–1.9% R&D efficiency reduction) because the sanctioned providers had modest market shares at the time of enforcement — the fine formula's market-share component needs large incumbents to produce a meaningful bite. The most striking structural divergence: EU issued 3 sanctions with no mandate; US issued 1 sanction then escalated to a mandate — the EU's lower risk tolerance recycled regulatory energy into repeated incident-driven fines rather than structural benchmark reform.

---

## 13. Open Questions for Follow-Up

- **Sanction size sensitivity:** What happens when the critical incident hits a dominant provider (e.g., OpenAI at 48% share)? Fine would be ~11% efficiency reduction rather than ~2%.
- **Stacking effects:** Can a provider be double-sanctioned (funder reduction + sanction) in the same round? Check interaction with market_concentration_review.
- **Earlier mandate path:** Does EU ever reach `mandate_benchmark`? Requires `has_mandated=False`, `has_investigated=True`, `max_risk > 0.6` — the sanctions branch currently absorbs rounds that might have escalated there.
- **Seed sensitivity:** Both runs used seed=42. A different seed changes which provider gets the critical incident, which likely flips the entire market outcome.
