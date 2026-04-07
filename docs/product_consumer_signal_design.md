# Provider Model: R&D and Product — Design Document

**Status:** In progress (session 16, 2026-04-06)
**Context:** Redesign of how consumer signal feeds into provider decision-making, motivated by benchmark orientation ratchet problem and PIMMUR compliance.

---

## What the LLM decides each round

**Portfolio allocation:** `{rd, safety, product}` summing to 1.0, adjusted via ordinal signals (plus/minus 0.05 or 0.10 per round).

**Focus levels:** Per-benchmark priority scalars, adjusted via ordinal signals. This is the provider's proactive strategic choice — "I'm pursuing Coding Evaluation and Safety Evaluation." Drives which dimensions get R&D investment.

**Benchmark orientation** (when mode = "adjustable"): A scalar `bo` in [0.05, 0.95] controlling the blend between benchmark-driven and consumer-signal-driven R&D targeting. Adjusted via ordinal signal.

---

## What the LLM sees in its prompt

- Benchmark scores + per-round deltas (detailed, per-benchmark)
- Competitor scores (aggregate per competitor)
- Own portfolio history
- Own focus_levels + inferred benchmark dimension weights
- Market share (scalar)
- Recent incidents and regulatory actions
- Strategy memos from prior rounds (reasoning memory)
- **Consumer signal** — currently shown as "Your users seem to value: reasoning (28%), coding (22%)..." with confidence qualifier based on market share

### Open question: what should replace the consumer signal in the prompt?

| Option | What LLM sees | Anchoring risk | Strategic reasoning quality |
|--------|--------------|----------------|---------------------------|
| A. Full consumer signal (status quo) | 6-dim need vector with percentages | High — LLM follows the signal | High — LLM can reason about user needs vs. benchmark alignment |
| B. Consumer signal gated by product investment, two tiers | Nothing (below threshold) or noisy 6-dim vector (above) | High for tier 2 providers, none for tier 1 | Split — tier 1 reasons from business metrics, tier 2 anchors on signal |
| C. No consumer signal in prompt, mechanical only | Market share + churn only | None | Low — LLM can't reason about user needs; product analytics operates purely mechanically in compute_capability_gains() |

**Unresolved:** All three options have significant drawbacks. A causes anchoring and convergence. B causes anchoring for the providers that matter most (the ones with analytics). C removes a strategically interesting dimension of reasoning entirely.

---

## How R&D targeting works mechanically (compute_capability_gains)

```
focus_weights[b]      = normalize(focus_level[b])
benchmark_driven[dim] = sum( focus_weights[b] * inferred_benchmark_weights[b][dim] )
target[dim]           = bo * benchmark_driven[dim] + (1 - bo) * consumer_signal[dim]
gain[dim]             = rd_fraction * rd_budget * target[dim]
```

Safety has a separate path: dedicated budget fraction, diminishing returns, 2-round lag, stochastic efficiency.

**Agreed change:** Consumer signal quality in this formula should scale with product investment. Higher product budget -> lower noise on the signal -> more accurate R&D targeting. This operates regardless of what the LLM sees in its prompt.

```
effective_signal = quality(product_budget) * true_signal + (1 - quality) * uniform
```

Where `quality` scales continuously with product budget. Open-source providers have a structural quality ceiling.

---

## What product allocation currently does

**Nothing.** It's logged but has zero mechanical effect. No impact on consumer satisfaction, cost_advantage, signal quality, or anything else.

**Agreed change:** Product investment determines the quality of the consumer signal used in compute_capability_gains(). This is the primary mechanical role of product allocation.

### Open question: should product budget be current-round or rolling average?

| Option | Rationale | Implication |
|--------|-----------|-------------|
| Current-round | Simpler, no state to track | Provider can spike product for one round then cut — gets analytics benefit immediately |
| Rolling average (3 rounds) | Analytics infrastructure requires sustained investment | Provider must commit resources over time; brief spikes don't help |

**Decided: 3-round rolling average applied uniformly to ALL portfolio allocations (rd, safety, product).**

Rationale: the same "organizational change takes time" argument applies to R&D (hiring researchers), safety (building red-team capability), and product (analytics infrastructure). Using one uniform mechanism avoids reviewer criticism of ad-hoc per-lever smoothing.

The rolling average replaces the 2-round safety delivery lag, which was a separate mechanism modeling the same concept (execution delay). Safety retains diminishing returns and stochastic efficiency (growth physics, not timing). R&D retains diminishing returns and S-curve ceilings.

Implementation: `model_provider.py` tracks `_portfolio_history` (last 3 rounds), computes `_effective_portfolio` as the mean, and uses it in `compute_capability_gains()`. Both target and effective portfolios are logged to `rounds.jsonl`.

---

## What drives provider revenue and budget

```
base_revenue = market_share * revenue_per_share * total_market_size * (1 - cost_advantage)
total_budget = base_revenue + funder_allocation (scaled)
rd_budget    = total_budget (after regulatory sanctions)
```

Product allocation is a fraction of this budget. The absolute dollar amount spent on product determines signal quality.

---

## How benchmarks create provider value (mechanical channels)

| Channel | Mechanism | Provider can observe? |
|---------|-----------|----------------------|
| Consumer believed_quality | Benchmark scores -> leaderboard_trust-weighted belief -> switching decisions | No — provider sees market share change, not attribution |
| New user acquisition | New users allocate proportional to believed_quality (benchmark-derived) | No — invisible |
| Funder beliefs | Funders update believed_provider_quality from leaderboard scores | Indirectly — provider sees funding change |
| R&D targeting | Per-benchmark scores -> inferred_benchmark_weights -> focus_level -> capability gains | Yes — provider sees its own scores and can infer what benchmarks test |

**Key observation:** The upward pressure on benchmark orientation is real but invisible to the provider. Benchmarks drive acquisition and funding, but the provider can only observe the downstream effects (market share change, funding change) without attribution.

---

## Benchmark orientation: the ratchet problem

**Empirical finding:** In LLM adjustable mode, ALL providers drive orientation from 0.80 to 0.05 (floor) by round 15-22. Monotonic, uniform across providers with different profiles.

**Diagnosed causes:**
1. Prompt framing ("public leaderboard vs. user data") is loaded — triggers demand characteristics (PIMMUR Minimal-Control violation)
2. LLM backbone recognizes benchmark-gaming experimental structure (PIMMUR Unawareness violation)
3. No visible upward pressure — provider can't see that benchmarks drive acquisition/funding
4. Consumer signal always available and always directional — gives the LLM a reason to lower orientation every round

**Agreed fix:** Rewrite the system prompt to remove loaded "benchmarks vs. user feedback" framing. Present orientation as an internal resource allocation question.

### Open question: does orientation remain LLM-adjustable, get removed, or become derived?

Current leaning: keep adjustable, with the expectation that fixing the prompt and information environment may resolve the ratchet. If it doesn't, that's a finding about LLM backbone bias worth documenting.

---

## Open-source structural differences (agreed)

- Signal quality ceiling regardless of product investment (no deployment telemetry)
- Open-source providers invest more in R&D, less in product (users build their own products)
- Consistent with existing OS mechanics (no VC funding, lower safety floor, contamination multiplier)

---

## Strategic targeting vs. reactive signal

An important design distinction surfaced during discussion:

**Focus_levels = proactive strategy.** The provider decides which benchmarks/capabilities to pursue based on its own strategic vision, competitive analysis, and identity. Example: Anthropic deciding to pursue enterprise coding.

**Consumer_signal = reactive validation.** Did the bet pay off? Are the users the provider is attracting actually happy with what was built? Example: privacy-preserving transcript analysis confirming coding users are retained but want better agentic capabilities.

**Product investment = ability to get that validation.** Without product analytics, providers make strategic bets blind — they set focus_levels but never learn whether their R&D direction matches user needs. With product analytics, they get course-correction data.

The consumer signal should NOT steer strategy. It should check whether strategy is working. This distinction is why showing the full signal in the prompt is problematic — the LLM treats it as strategic direction rather than validation feedback.

---

## Real-world information access by provider type

| Company type | What they know about usage | Sim analogue |
|---|---|---|
| Frontier labs (Anthropic, OpenAI) | Detailed task category distribution from transcript analysis | High-fidelity provider-specific consumer_signal |
| Cloud API providers (Google, AWS) | API call patterns, token volumes, less semantic understanding | Moderate signal — ranked dimensions, no precise weights |
| Open-source (Meta, Mistral) | Download counts, community benchmarks, HuggingFace trending | Near-blind — market-level signals only |
| Smaller/newer labs | Enterprise customer conversations + basic telemetry | Noisy, biased toward loudest customers |

This maps to a structural visibility difference rather than a uniform signal, and justifies the open-source ceiling.

---

## What's settled (implemented session 16)

- **Prompt reframe:** "external evaluation results vs internal product analytics" replaces "benchmark performance vs user feedback". New default. Ablation confirmed: eliminates orientation ratchet, produces provider differentiation.
- **Consumer signal in prompt:** shown to all providers uniformly with reframed framing. No gating by product investment in the prompt — gating is mechanical only.
- **3-round rolling average** applied uniformly to all portfolio allocations (rd, safety, product). Replaces the 2-round safety delivery lag.
- **Benchmark_orientation** stays LLM-adjustable. Its effective importance scales with product investment (see signal fidelity channel).
- **Product investment: two mechanical channels:**
  - **Consumer signal fidelity** (`model_provider.py`): `quality = sigmoid(product_budget)`, open-source capped at 0.40. Affects R&D targeting accuracy in `compute_capability_gains()`. Higher product investment -> capabilities grow in dimensions users actually need. Config flag: `enable_product_signal_quality`.
  - **Switching cost retention** (`consumer.py`): `bonus = 0.50 * (1 - exp(-2 * product_budget))`, open-source capped at 0.15. Multiplies effective switching cost. Higher product investment -> stickier users. Heuristic mode only. Config flag: `enable_product_retention`.
- **Ablation conditions:** `product_signal_only`, `product_retention_only` isolate each channel.

**Open:**
- Calibration sensitivity analysis (signal fidelity midpoint, retention bonus strength)
- Full PIMMUR prompt audit (flagged in TODO.md) — all LLM prompts should be checked for loaded language following the orientation reframe finding

---

## PIMMUR compliance notes

Relevant principles from Zhou et al. (2026), arXiv:2509.18052:

- **Minimal-Control:** Orientation prompt reframe (session 16) eliminated a uniform ratchet artifact. Empirically demonstrated that small framing changes dominate LLM simulation dynamics. All prompts require audit.
- **Unawareness:** LLM backbone recognizes benchmark-gaming structure from prompt labels. Consumer signal framing should not reinforce this recognition.
- **Profile:** Product-investment-gated signal creates endogenous differentiation rather than cosmetic persona differences.
- **Realism:** Information asymmetry between frontier labs and smaller providers is empirically grounded. Open-source visibility gap is structurally justified.

Full PIMMUR principles reference: `docs/pimmur_principles.md`
Full PIMMUR audit (pre-reframe): `rough/pimmur_audit.md`
