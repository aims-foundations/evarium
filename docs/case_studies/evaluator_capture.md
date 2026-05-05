# Evaluator Capture

## 1. Policy anchor

Two real-world forces jointly enable evaluator-as-company dynamics.

### 1.1 The Leaderboard Illusion (Singh et al. 2025, NeurIPS D&B)

- **Multiple private submissions** — Meta tested 27 private Llama-4 variants pre-release; best-of-27 publication yields ~100-point Elo boost.
- **Data access inequality** — Google 19.2%, OpenAI 20.4%, 83 open-weight models combined 29.7% of Chatbot Arena evaluation data; more access correlates with 112% relative performance gains.
- **Premium private testing** — undisclosed pre-release evaluation creates a "distorted playing field."

### 1.2 LMArena business model

LMSYS Org (2023) → LMArena company (2025) → $150M Series A at $1.7B valuation (Jan 2026). Freemium model:

- **Free tier** — public arena, community evaluation, drives traffic and legitimacy.
- **Premium tier** (OpenAI, Google DeepMind, Anthropic, Meta) — public benchmarking, competitive positioning, confidential pre-release testing, custom evaluation infrastructure.

Revenue streams: VC ($250M total from a16z, Lightspeed, Felicis, UC Investments), infrastructure sponsors (Voltage Park, NVIDIA, Google Cloud, AMD, HuggingFace), provider service fees, API credits.

**Conflict of interest:** evaluator revenue depends on serving paying providers, who then get selection-biased score inflation through multiple submissions and early access.

## 2. Simulation mechanism

### 2.1 Configuration

```python
class SimulationConfig:
    evaluator_as_company: bool = False       # default OFF
    evaluator_base_budget: float = 0.0
    evaluator_premium_pricing: float = 10000.0   # per provider per round
```

### 2.2 Best-of-N trials (Leaderboard Illusion analog)

```python
def compute_n_trials(provider_name, eval_engineering) -> int:
    if not evaluator_as_company: return 1
    funding_bonus = 1 if provider in premium_providers else 0      # binary
    eval_eng_bonus = int(eval_engineering * 5)                      # 0.2→1, 0.4→2, 0.8→4
    return min(5, 1 + min(funding_bonus, eval_eng_bonus))           # need BOTH premium AND expertise
```

Score publication: `score = max(trial_scores)`. Empirical calibration target: ~10–20 point inflation per extra trial.

### 2.3 Early access (3-round head start)

Premium subscribers see new benchmarks 3 rounds before public launch. Implemented via `_get_effective_benchmark()` — 1.5× exploitability multiplier for providers in the early-access window after public introduction. Anchor: ~5–10 point advantage on new benchmarks.

### 2.4 Budget gating

`collect_funding()` aggregates base-funding (from funders) + service-revenue (from premium payments). `consider_new_benchmark()` requires `budget >= 50000` to introduce a new benchmark. Low budget → stale evaluation suite.

### 2.5 Mechanism focus

The current implementation models evaluator capture through a single axis: premium access (provider pays evaluator → gets extra trials + early access → score inflation → gaming gap → incidents). The fee-as-R&D-drain framing is **weak empirically**: LMArena and SEAL fees are rounding error relative to frontier R&D budgets (<0.1%).

Three real-world meaningful tensions are not currently modeled and are candidates for future extensions:

1. **Reputation risk if gaming is outed** — Leaderboard Illusion / Meta 27-variants scandal. An exposure event would create a negative media narrative, funder allocation drop, and consumer trust decay.
2. **Attention rivalry** — evaluator sampling asymmetry (Google 34% vs Reka 3.3% of daily Chatbot Arena battles). Providers compete for sampling allocation, not for a fixed fee.
3. **Collective action trust destruction** — as gaming normalizes, evaluator signal value drops ecosystem-wide. A commons-type externality distinct from individual capture.

A richer second-generation implementation would drop fee-drain entirely and instead add a stochastic exposure event plus an evaluator total-sampling-capacity constraint.

## 3. Evaluator landscape survey

Taxonomy of real-world AI evaluators, with capture-risk classification that grounds simulation parameter choices:

| Archetype | Examples | Funding model | Capture risk |
|---|---|---|---|
| **Benchmark/leaderboard** | LMArena, HELM, Hugging Face | VC + provider fees + compute donations | High |
| **Red-team / adversarial** | Gray Swan, Haize, Trail of Bits | VC + lab consulting | Medium |
| **Compliance / audit** | Credo AI, Holistic AI, Big Four | Fee-for-service (auditee pays) | Very High |
| **Government / nonprofit** | UK AISI, METR, Apollo | Government / grants | Low |
| **Internal lab teams** | OpenAI Preparedness, Anthropic RSP | Parent company budget | Structural (self-eval) |

Key case studies (brief):

- **Gray Swan AI** (~$5.7M) — CMU-origin adversarial red-team; lab customers + UK AISI. Value-prop resists capture (evaluator finding nothing has no value), but scaling creates revenue dependency.
- **Haize Labs** ($12.5M seed) — pure-play adversarial; capture risk depends on revenue diversification.
- **Acquisition wave 2024–25** — Robust Intelligence (→Cisco, $400M), CalypsoAI (→F5, $180M), Protect AI (→Palo Alto, $500–700M), Lakera (→Check Point, $190M). Consolidation mirrors cloud security 2018–22; acquirer enterprise relationships create new capture vectors.
- **Scale AI / SEAL** ($29B, $1.8B revenue) — Meta's $14.3B investment creates direct lab-evaluator financial entanglement.
- **Stanford HELM** — academic independence + compute donations. Moderate capture risk via academic-to-industry talent pipeline.
- **Credo AI / Big Four** — classic "auditee pays" model. Very high capture risk, structurally similar to pre-SOX financial auditing.
- **UK AISI** (~£100M/year, 100+ researchers) — government-funded; voluntary lab cooperation; political capture risk (US AISI gutted under Trump, Jan 2025).
- **METR** (Beth Barnes) — explicitly refuses lab payments; grant-funded. Strongest independence model; depends on continued grant funding and voluntary lab cooperation.
- **Apollo Research** — grant-funded deception/scheming specialist. Same access-dependency as METR.
- **Internal teams** (OpenAI Preparedness, Anthropic FRT, DeepMind FSF, Meta Purple Llama) — structurally captured by design; serve internal risk management, not independent oversight.

## 4. Cross-sector capture dynamics

Five structural enablers of evaluator capture, cross-sector:

1. **"Evaluated entity pays" funding model** — every sector where the evaluated entity pays the evaluator develops capture over time. No sector has successfully reformed this (SOX did not change it for financial auditing; Dodd-Frank did not change it for credit ratings).
2. **Revolving door** — AI talent pipeline is especially severe (3–10× salary multiplier from labs to academia). Creates anticipatory bias plus knowledge transfer for future gaming.
3. **Information asymmetry / access dependency** — the **most severe** vector in AI and **unique** among analogous sectors. Financial auditors have legal access rights; AI evaluators do not. Labs have effective veto over evaluation scope.
4. **Evaluator concentration** — paradoxical: high concentration creates too-big-to-sanction; low concentration enables audit shopping (Bolton, Freixas, Shapiro 2012).
5. **Transparency of results** — partial at best in AI; evaluation methodology and failed tests often under NDA.

Historical precedents:

- **Arthur Andersen / Enron** — Andersen earned $25M audit + $27M consulting from Enron. SOX created PCAOB and prohibited most non-audit services, but kept the "auditee pays" core. Academic evidence: audit quality improved then plateaued.
- **Credit rating agencies / 2008** — structured-finance ratings = ~50% of Moody's revenue by mid-2000s. "Let's hope we are all wealthy and retired by the time this house of cards falters" (S&P analyst, FCIC). Dodd-Frank created SEC Office of Credit Ratings; issuer-pays model untouched.
- **Cybersecurity compliance** — SOC 2 / PCI-DSS compliance did not prevent Target (2013), Home Depot (2014), Heartland (2008) breaches. Voluntary, unregulated, structurally prone to capture.

Capture-resistance mechanisms (AI applicability):

| Mechanism | Source | AI applicability |
|---|---|---|
| Independent oversight board (PCAOB) | Financial auditing | High — "AI PCAOB" frequently proposed |
| Mandatory evaluator rotation | Financial auditing (EU) | Moderate |
| Legal access rights for evaluators | Financial auditing (securities law) | **Critical need — requires legislation** |
| Public disclosure of evaluation results | SEC filings | High |
| Separation of evaluation and consulting | SOX §201 | High |
| Assignment system (break shopping) | Proposed but rejected for CRAs | Novel |
| Accreditation of evaluators | CREST (cybersecurity) | High |
| Third-party-funded evaluation | METR model | Ideal but economically challenging at scale |

## 5. Hypothesis

Evaluator-as-company dynamics produce capture that degrades signal quality without requiring individual malfeasance. The dominant channel is not fee-induced R&D drain (fees are <0.1% of R&D budgets) but reputation risk under exposure events, attention rivalry for sampling allocation, and collective trust erosion as gaming normalizes. The existing sampling-asymmetry empirics (Chatbot Arena Fig 5: Google 34% / Reka 3.3%) are replicable in the simulation via a total-capacity constraint.

## 6. Open questions

- **Exposure-event calibration** — `base_rate` and `investigative_pressure` coefficient against what empirical anchor? The Leaderboard Illusion paper's publication date and Meta's public response timing are one data point.
- **Post-exposure magnitudes** — funder allocation drop, consumer trust decay, regulator attention spike. Cross-check against Meta's public-communications response and LMArena's policy updates post-publication.
- **Interaction with benchmark sponsorship** — both involve evaluator-provider fee flows. Separation: evaluator capture is per-provider subscription (any benchmark); benchmark sponsorship is per-benchmark sponsorship. Need to confirm these don't stack incorrectly.
- **Funder-to-evaluator allocation** — funders currently don't split capital between providers and evaluator. Would make evaluator funding mix endogenous.
- **Evaluator type differentiation** — current simulation treats all evaluators as a single archetype. Adding government, nonprofit, and industry-captive archetypes with different capture profiles would map to the landscape survey above.
- **Evaluator budget affecting benchmark validity decay** — low budget produces slower refresh, faster contamination, faster validity erosion. Not currently modeled.

## 7. References

### Primary

- Singh, Nan, Wang (2025). "The Leaderboard Illusion." arXiv:2504.20879. NeurIPS D&B Track.
- Contrary Research — LMArena business breakdown.
- TechCrunch — LMArena $1.7B Series A (Jan 2026).

### Landscape survey anchors

- Gray Swan AI; Haize Labs; Robust Intelligence / Cisco acquisition; CalypsoAI / F5; Protect AI / Palo Alto; Lakera / Check Point.
- Scale AI / SEAL; Meta's $14.3B Scale investment (2025).
- Stanford HELM / CRFM; UK AI Safety Institute; METR; Apollo Research.
- OpenAI Preparedness Framework v2; Anthropic Responsible Scaling Policy v3; Google DeepMind Frontier Safety Framework v3; Meta Purple Llama.

### Cross-sector capture

- Bolton, Freixas, Shapiro (2012). The Credit Ratings Game. J. Finance.
- Lundh et al. (2017). Cochrane MR000033 (industry sponsorship and research outcome).
- FCIC Report (2011) — Moody's/S&P structured-finance dynamics.
- SOX §201, PCAOB establishment.
- Dodd-Frank SEC Office of Credit Ratings.
- Cuéllar (2024). Common Law and Emerging Technology. Stanford L Rev.

### Academic frames

- Akerlof (1970). Market for Lemons.
- Arrow (1963). Uncertainty and the Welfare Economics of Medical Care. (Professional norms and trust.)
- Longpre et al. (2024). A Safe Harbor for Independent AI Evaluation. ICML.
- Casper et al. (2024). Black-Box Access is Insufficient for Rigorous AI Audits.
