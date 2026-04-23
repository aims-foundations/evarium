# LLM Actor Prompt Audit Playbook

**Purpose.** Reusable procedure for auditing and improving an LLM actor's planning prompt to increase realism and strategic viability while preserving PIMMUR invariants. Built from the session-48 work on model providers; generalizes to regulator, funder, evaluator, and (when enabled) LLM consumer prompts.

**When to use.** Triggered by one or more of:
- Reasoning traces feel strategically dead or self-reflexive
- Reasoning references are disproportionate to real-world salience
- Actor is blind to signals a real counterpart would obviously have
- Actor's reasoning contradicts its own observations
- Context-window rebalance is being considered

**Prerequisites before starting.** Load:
- `docs/stakeholders.md` (visibility system, actor roster)
- A run with full per-actor memory (`memory.json`, `private_state.json`, `public_state.json` in provider dirs or equivalent for the actor)
- Access to the LLM prompt builder for that actor in `src/llm.py`
- The round loop location in `src/simulation.py` where `ecosystem_context` is assembled for that actor

---

## The Seven-Pass Audit

Each pass is independent; do all seven before proposing fixes. Findings from one pass often reframe findings from another.

### Pass 1 — Sample reasoning traces

Pull **random** (seed=42) traces across rounds and actor instances. Not carefully-chosen — random is harder to dismiss.

```python
import json, random
from pathlib import Path
random.seed(42)
RUN = Path("sandbox/experiments/<run>/llm/<cond>/seeds/seed_<N>")
actors = [...]  # actor names or ids (e.g. provider names)
for a in actors:
    mem = json.load(open(RUN / f"<actor_type>/{a}/memory.json", encoding="utf-8"))
    plans = [x for x in mem if x.get("type") == "planning"]
    sample = random.choice(plans[1:])  # skip R0 — always special
    print(f"=== {a} R{sample['round']} ===")
    print("REAS:", sample.get("reasoning", "")[:1200])
```

Read 6-10 samples. Note:
- What categories of information are actually referenced?
- What's conspicuously absent?
- Does reasoning feel purposive, or reactive-to-prompt?
- Is the reasoning repeatable text (tics) or novel each round?

### Pass 2 — PIMMUR scorecard

For this actor, rate each dimension ✓ / ⚠️ / ❌:

| Dimension | Question to ask |
|---|---|
| **Purposive** | Is there a coherent goal the actor pursues across rounds? Does the prompt support or override it? |
| **Independent** | Does the prompt let the actor reason freely, or does it prescribe structure (e.g. `(a)/(b)/(c)` scaffolds)? |
| **Memoryful** | Does prior-round state carry forward in a usable way? Is memory surfaced proportional to its relevance? |
| **Mutable** | Can the actor update its mind from evidence? Are update signals strong enough? Is identity/frame locked such that the actor can't evolve? |
| **Unidirectional causality** | Does the prompt leak researcher-only knowledge (aggregated interpretations, ground-truth facts, "this is noisy")? |
| **Rational** | Does the actor reason from its own utility given observations, or from externally-imposed heuristics? |

Any ⚠️ or ❌ is a finding.

### Pass 3 — Coaching risk audit (line-by-line imperatives)

Walk every imperative sentence in the system prompt and per-round prompt. For each, classify:

| Category | Example | Action |
|---|---|---|
| Role/persona (OK) | "You are the strategy team at an AI model company" | Keep |
| Information (OK) | "Your current budget: R&D 50%, Safety 20%, Product 30%" | Keep |
| Output structure (OK) | "Output valid JSON with keys X, Y, Z" | Keep |
| Reasoning scaffold (borderline) | "Focus on: (a) what changed, (b) what it implies, (c) why the move" | Flag — often coaching disguised as structure |
| Epistemic assertion (coaching) | "User-research signals are noisy" | **Remove** |
| Decision rule (coaching) | "Prefer multi-month patterns over one-round swings" | **Remove** |
| Identity meta-instruction (coaching) | "Treat identity as context, not as primary argument" | **Remove** |

Anything in the bottom three rows is coaching and should be pulled unless there's a strong defense.

### Pass 4 — Prompt composition measurement

**Rationale.** LLMs allocate attention roughly proportional to content volume. If one section is 44% of the prompt, reasoning will be 44% about that section regardless of whether the real-world exec would weight it that way.

**Measurement.** Reconstruct the prompt from logged state + the real builder, split by `##` headers, count chars per section.

```python
from pathlib import Path
import json
# Import the actual prompt builder from src/llm.py for this actor
from llm import _build_<actor>_planning_prompt

RUN = Path("sandbox/experiments/<run>/llm/<cond>/seeds/seed_<N>")
rounds = [json.loads(l) for l in open(RUN / "rounds.jsonl", encoding="utf-8")]
# ... reconstruct ctx for a chosen round and actor
prompt = _build_<actor>_planning_prompt(**ctx)

sections = {}
current = "PREAMBLE"
for line in prompt.split("\n"):
    if line.startswith("## ") and not line.startswith("### "):
        current = line[3:].strip()
    sections[current] = sections.get(current, "") + line + "\n"
total = len(prompt)
for sec, content in sections.items():
    print(f"{sec:45s} {len(content):5d} chars ({len(content)/total*100:5.1f}%)")
```

Measure at 3+ rounds (early, mid, late) and flag:
- Any section > 40% — over-indexed
- Any semantically-important category < 10% — under-represented
- Any section that grows unbounded with actor-scale (e.g. benchmarks as pool grows) — structural bloat candidate

### Pass 5 — Information completeness

Ask: *what does the real-world counterpart of this actor see on a normal morning?* Then compare to what the prompt provides.

Reference the **visibility system in `stakeholders.md`** — some signals are deliberately private. Candidates for inclusion must be:
- Public-state visible per the visibility contract, OR
- Derivable from public state (e.g. own funding from allocations)

Rank candidates by **marginal benefit per token**:

- **Tier 1** (add): high-signal, small cost (e.g. own financial state, competitor public announcements, recent benchmark-type metadata)
- **Tier 2** (consider): medium-signal, medium cost (e.g. cumulative trajectory summaries, competitor market share breakdown)
- **Tier 3** (skip): low-signal OR PIMMUR-risky (e.g. narrative-state labels that are researcher aggregations, competitor private state)

### Pass 6 — False-precision scan

Walk every numeric field in the prompt and ask: *is this precision real or fabricated?*

- Survey-derived percentages — usually fabricated (drop to ordered list)
- Researcher-interpolated summaries ("~$X run-rate") — fabricated, drop
- Confidence qualifiers derived from thresholds ("substantial/moderate/limited usage data") — redundant if raw number is also shown; drop the qualifier
- Public leaderboard metrics (scores, deltas, market share) — real, keep
- Own portfolio percentages — real (actor chose them), keep

### Pass 7 — Redundancy + bloat

Grep reasoning traces for common restating patterns:
- Leaderboard restating ("Orion at X.XX vs our Y.YY")
- User-research % restating
- Portfolio restating ("budget stays at A/B/C")
- Identity restating ("our [profile phrase]")

Each restating pattern that shows up frequently indicates the prompt provides the info AND the LLM is re-stating it for no content gain. The fix is usually a terse `"Do NOT restate X, Y, Z"` instruction in the reasoning-field spec (efficiency instruction, not reasoning coaching).

Also: look for static sections that could be compressed when unchanged (e.g. belief maps, persona, team composition).

---

## Fix Taxonomy

Mapping findings to fix categories:

| Finding | Fix type | Session-48 example |
|---|---|---|
| Output channel generated but not logged | Add logging | Fix 4: log `strategy_memo` in `memory.json` |
| Persona re-injected every round as live argument | Move persona to system-prompt role layer; strip from per-round user prompt | Fix 1B |
| Reasoning scaffold prescribes inference direction | Remove scaffold; keep efficiency instructions only | Fix 2 partial rollback (kept "do NOT restate", removed `(a)/(b)/(c)`) |
| Memory reframing is neutral | Rename section to match actual content semantics | Fix 3a: "Notes From Prior Months" → "What You Committed To In Recent Months" |
| Researcher asserts "X is noisy" / prescribes decision rule | Remove the assertion entirely | Fix 3b rollback: removed noise-skepticism lines |
| False-precision percentages | Drop to ordered list | Consumer-signal %s removed |
| Redundant confidence qualifier derived from visible number | Drop the qualifier, keep the number | "Based on moderate usage data" → raw market-share % |
| Missing competitor actions | Pipe existing `public_comms` into prompt (doesn't require new state) | Competitor Activity section |
| Missing competitor per-metric movement | Pipe per-round state history, build filtered matrix | X6-rank matrix (top-5 focused / rest non-focused, 3+3 by delta) |
| Missing industry/press signal | Pipe `media.headlines` raw, no narrative-state label | Industry News section |
| Missing financial state | Pipe funding allocations + funder-type participation | Expanded Current State |
| Static dimensional metadata bloat | Compress to changed-only per round | "What Your Team Thinks" now only shows new benchmarks OR top-dim-weight Δ >0.05 |

---

## Core Principles Discovered

### 1. Salience-to-tokens correlation is real

LLMs weight attention roughly proportional to prompt content volume. Don't assume a long benchmark section will be appropriately de-weighted just because the instructions say so. **Rebalance by addition, not subtraction** — adding signals is reversible, filtering is lossy.

### 2. Information vs. coaching

Adding data is PIMMUR-safe. Adding rules, interpretations, or framings that the agent could derive itself is coaching. When in doubt:
- Could a real actor in this role derive this from the raw data? → it's a rule; don't inject
- Is this just exposing something the public-state system already tracks? → it's information; inject

### 3. Labels that organize known facts are borderline

"In benchmarks you're prioritizing:" / "Movement elsewhere:" split the matrix into sections that the agent could derive from its own `focus_level` column. Organizational framing, not coaching — acceptable. But don't layer semantic interpretation on top ("critical areas", "surprise movements").

### 4. Rank-based > threshold-based for focus splits

Threshold filters (e.g. `focus_level >= 1.2`) degrade asymmetrically — an agent with many moderate+ priorities gets a thin "elsewhere" section; an agent with few gets a thin "focus" section. Rank-based (top-K by focus_level) handles both regimes cleanly.

### 5. Don't fabricate numbers

If your simulation doesn't natively expose revenue, don't compute `~$X/mo` from market share × static factor in the prompt. Either expose it as a first-class signal in the sim or leave it out.

### 6. Stateless API calls

Every planning call is a fresh, stateless LLM invocation. There is no conversation memory. System prompt fires every round regardless of where you put identity. The choice between system-prompt vs user-prompt placement is about **framing** (role vs. live evidence), not about frequency.

---

## Session-48 Worked Example: Model Provider

### Before

| Section | % of prompt (mid-round) |
|---|---|
| Evaluation Results + Beliefs | **~44%** (combined) |
| What You Committed To (memos) | ~35% |
| User Research | 5-6% |
| Competitor Results | **~6%** (scalar scores only) |
| Current State | 3% (percentages only, no financial) |

Reasoning traces: obsessive about own benchmarks, disproportionate weight on noisy user-research %s, blind to competitor actions and industry context.

### After

| Section | % of prompt (at 13 benchmarks, projected) |
|---|---|
| Competitor Activity (comms + X6 matrix) | ~34% |
| Evaluation Results (+ type column + (new) tag) | ~23% |
| Industry News (raw headlines, last 2 months) | ~14% |
| Memos | ~15% |
| Current State (market share + funding) | ~6% |
| Beliefs (compressed to changed-only) | ~4% |
| User Research (ordered list, no %s) | ~2% |

Reasoning traces (smoke test): reference competitor market-share surges, specific per-benchmark gaps, partnership announcements, and funding state — all signals the old prompt made invisible.

### Specific changes (see `src/llm.py`, `src/actors/model_provider.py`, `src/simulation.py`)

- **Fix 4** — `strategy_memo` now logged to `memory.json`
- **Fix 1B** — identity (name, strategy_profile, innate_traits) moved from per-round user prompt into system prompt role layer
- **Fix 2 (partial)** — reasoning spec includes "do NOT restate" but no `(a)/(b)/(c)` scaffold
- **Fix 3a** — "Notes From Prior Months" → "What You Committed To In Recent Months" (factual rename, no epistemic nudge)
- **Rolled back** — "identity as context, not primary argument", noise-skepticism assertions, "before overturning a commitment" nudges
- **Added** — Competitor Activity section (announcements + X6 rank-based delta matrix), Industry News section, financial block in Current State, benchmark type + (new) tag, belief compression, user-research %s + confidence qualifier removed

---

## Adapting to Other Actors

Same seven-pass audit per actor. Differences are in **which signals are candidates for Tier 1** (Pass 5) and **what counts as PIMMUR-clean organization vs. coaching** (Pass 3).

### Regulator

**Existing prompt surface (approx).** Narrative state, recent incidents, intervention cooldowns, incident escalation patterns.

**Things to check specifically.**
- Is the narrative state (`OPTIMISM/SKEPTICISM/CRISIS`) surfaced as a categorical label or derivable from raw headlines? The label is researcher aggregation; prefer raw.
- Does the regulator see the full ladder-progression history (how many times each lever has been used, cooldown status), or just last-N actions?
- Does the regulator see its own prior-round reasoning? Memory continuity matters for consistent escalation.
- Is there any coaching about "when to escalate" vs. pure information?
- Is `score_reliability` / Pearson r leaking into the regulator prompt? It's a **researcher-only diagnostic per stakeholders.md** — do not leak.

**Tier 1 additions to consider.**
- Own intervention history summarized by lever (count, most-recent-round, cooldown remaining)
- Media narrative **as headlines**, not as state label
- Per-provider incident trajectory (not just last round)

### Funder

**Existing prompt surface (approx).** Leaderboard, market shares, recent allocation history, `public_comms` from providers, media sentiment/headlines, incidents.

**Things to check specifically.**
- Media sentiment is already wired in — is it surfaced as a number, a qualitative tone label, or raw headlines? Prefer raw over interpretation.
- Funder type (VC / corporate / gov / foundation) determines reasoning — is the persona in the system prompt (role layer) or injected every round?
- Does the funder see its own cumulative allocation per provider across rounds, or only recent?
- Does the funder see competitor funders' allocations? (Public? Private?)
- Ordering of leaderboard / incident list / allocation history — does it bias attention?

**Tier 1 additions to consider.**
- Own cumulative allocation per provider (trajectory)
- Peer funders' public allocations (if modeled as public)
- Provider revenue / market-share trajectories (not just current snapshot)

### Evaluator (dynamic mode only)

**Existing prompt surface (approx).** Benchmark pool, saturation signals, provider scores, recent introductions / retirements.

**Things to check specifically.**
- Are saturation signals surfaced as `bool` labels (researcher aggregation) or as raw dispersion/reliability metrics?
- Is the benchmark pool fully listed every round, or compressed to changed-only?
- Does the evaluator see provider investment reasoning? It shouldn't (visibility).
- Is there coaching about when to introduce / retire ("introduce new when saturated")?

**Tier 1 additions to consider.**
- Own intervention history (which benchmark introduced when, which retired, why)
- Cross-benchmark score dispersion trajectories
- Public provider announcements relevant to benchmark domain

### Organizational Consumer (when enabled)

**Currently off by default.** If enabled:

**Things to check specifically.**
- Consumer satisfaction is **ground truth** per visibility system — do not leak it to the consumer agent itself. Consumer should reason from experience/trust/media, not from own-satisfaction scores.
- Segment archetype (enterprise / individual / by sector) — persona in system prompt or injected?
- Is the consumer seeing all providers uniformly, or proportional to their current usage / awareness?
- Media effects are **under-modeled** (`media_audit_flag.md`) — consumer's exposure to press/narrative needs auditing alongside prompt audit.

**Tier 1 additions to consider.**
- Experience-based signals (own satisfaction with current provider, via public proxies only — not ground truth)
- Peer-segment signals (what are similar-archetype consumers doing?)
- Press exposure subset relevant to the segment's sector

---

## Measurement Toolkit (copy-paste snippets)

### Profile-phrase frequency grep

```python
import json, re
from pathlib import Path
RUN = Path("sandbox/experiments/<run>/llm/<cond>/seeds/seed_<N>")
patterns = {
    "<actor_id>": r"<keyword>|<keyword>",
    # ... one pattern per actor, capturing persona tics
}
for actor_id, pat in patterns.items():
    mem = json.load(open(RUN / f"<actor_type>/{actor_id}/memory.json", encoding="utf-8"))
    plans = [x for x in mem if x.get("type") == "planning"]
    hits_per_round = [len(re.findall(pat, x.get("reasoning", ""), re.I)) for x in plans]
    rounds_w_hit = sum(1 for h in hits_per_round if h > 0)
    print(f"{actor_id}: total_hits={sum(hits_per_round)}, rounds_w_hit={rounds_w_hit}/{len(plans)}")
```

### Restating scans

```python
import re
checks = {
    "leaderboard_restate": r"<pattern that captures X at Y.YY vs our Y.YY>",
    "pct_restate":         r"\b\w+\s*\(\d+%\)",
    "portfolio_restate":   r"(?:R&D|Safety|Product).*\d+%",
}
for actor in actors:
    reasoning_texts = [p.get("reasoning", "") for p in plans]
    for name, pat in checks.items():
        hits = sum(len(re.findall(pat, t, re.I)) for t in reasoning_texts)
        print(f"  {actor} {name}: {hits}")
```

### Section composition

See Pass 4 above.

### Reconstructing ctx from rounds.jsonl

When per-actor memory isn't saved (lightweight logs), the per-actor ctx can be partially reconstructed from `rounds.jsonl`. Stable fields (scores, market shares, funding allocations, incidents, media data) are always there. Missing per-actor fields (`recent_insights`, `inferred_*`) may need stub defaults for measurement purposes. See session-48 replay script in `interview_traces_sonnet46` analysis for a worked example.

### Reuse existing runs before launching fresh ones

Before burning tokens on a new smoke run, check whether existing artifacts suffice:

- **`sandbox/experiments/interview_traces_sonnet46/`** — 40-round LLM run, all 13 benchmarks active by late rounds, full per-actor memory including regulator/funder/evaluator traces. Rich source for sampling reasoning traces (Pass 1) and composition measurement (Pass 4) without any new tokens.
- **`sandbox/experiments/smoke_session48*/`** — 5-round and 10-round anthropic smoke runs with full state. Good for validating the shape of new prompt components against modern config.
- **Heuristic runs** — for any audit that's structural-only (composition, coaching-risk, bloat) and doesn't need LLM reasoning traces, a heuristic-mode run gets to 13 benchmarks in ~15 rounds at zero token cost.

Only launch a fresh LLM smoke after the audit is complete and fixes are staged — use the smoke as a verification step, not an exploration step. Two types of smoke:
1. **Pre-fix replay** (zero tokens) — reconstruct the existing prompt from past run state via the real builder; measure sections, grep traces. Validates the *status quo* before any edit.
2. **Post-fix LLM run** (tokens) — launch 1-seed × 5-rounds with the edit bundle in place; verify no fallbacks + reasoning uses new signals.

---

## Scope discipline

One actor per session. Do not bundle. Pattern:

1. Complete seven-pass audit → produces a findings list
2. Propose fixes in priority order, with before/after diffs
3. Critical self-inspection pass ("what did I miss / over-index on?")
4. User approves bundle
5. Smoke test: 1 seed × 5 rounds × anthropic
6. Verify: no fallbacks, new signals visible in reasoning, composition targets hit
7. Lock, commit, move to next actor

Session-48 showed this cycle running ~2-3 hours per actor when well-scoped. Scope creep (e.g. bundling model provider + regulator) explodes wall time and muddies smoke-test attribution.
