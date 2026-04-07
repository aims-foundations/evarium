# PIMMUR Principles Reference

**Source:** Zhou et al. (2026), "The PIMMUR Principles: Ensuring Validity in Collective Behavior of LLM Societies," arXiv:2509.18052v2

Key finding: 90.7% of LLM multi-agent simulation studies violate at least one principle. Reported "emergent" behaviors often vanish or reverse when principles are enforced, suggesting many findings are methodological artifacts rather than genuine social dynamics.

---

## Profile

Agents should possess diverse socio-demographic backgrounds, cognitive styles, and value systems to ensure systemic heterogeneity, avoiding the artifacts of a monolithic model distribution.

**For this project:** All LLM agents call the same backbone model. Diversity is achieved via persona text (strategy_profile, innate_traits), not architectural differences. Risk: all providers drift toward the same reasoning patterns regardless of stated identity. Mitigation: heuristic mode uses parametric differentiation; LLM mode should be cross-validated against multiple model backends.

## Interaction

Agents should exert agency through direct or indirect communication, responding to the specific actions of others rather than reacting to researcher-provided statistical aggregates.

**For this project:** Providers respond to competitor scores (aggregates), not competitor strategies (actions). The shared environment provides genuine indirect interaction (Goodhart pressure, market share shifts), but strategic reciprocity (gaming arms races, signaling) is structurally absent because the action layer is private.

## Memory

Agents should maintain and update persistent internal states across time, allowing information to be internalized, retained, and re-expressed rather than rephrased statelessly.

**For this project:** Numerical beliefs evolve persistently (learning rates, incident pressure decay). Strategy memos from prior rounds are fed back into planning prompts (reasoning_memory_depth=2). Portfolio allocations carry forward. Main gap: consumer agents have no historical context in LLM mode.

## Minimal-Control

Agents should be provided only the essential environmental context and action space, minimizing demand characteristics. Observed collective behaviors must emerge from agent interactions rather than from researcher-imposed behavioral cues.

**For this project:** The most consequential principle. Session 16 ablation demonstrated that changing the orientation prompt from "benchmark performance vs user feedback" to "external evaluation results vs internal product analytics" eliminated a uniform ratchet artifact and produced genuine provider differentiation. Small framing choices in prompts can dominate simulation dynamics. All prompts must be audited for loaded language, implicit coaching, or framing that pre-determines outcomes.

## Unawareness

Agents should remain unaware of the experimental hypothesis, design, and evaluation criteria. This reduces experimental biases, where models adjust their behavior to align with perceived social expectations or experimental goals.

**For this project:** Frontier LLMs trained on AI evaluation literature will recognize the experimental structure from prompt labels alone, independent of provider names. Provider anonymization (Orion Labs, Apex AI) mitigates company-association bias but does not address structure recognition. The strongest mitigation is domain reframing or using models less exposed to the AI evaluation discourse.

## Realism

Simulations should use empirical data from real-world human societies as references rather than simplified theoretical models, ensuring that AI's emergent behaviors can be meaningfully validated in real-world human dynamics.

**For this project:** External validation pipeline exists (external-validation/) targeting empirical shape-matching against HELM, PapersWithCode, and market data. Consumer segments grounded in sector-level AI usage surveys. Regulatory presets calibrated against EU AI Act and US enforcement patterns. Incident path-dependence validated against 12+ cross-sector case studies (session 15). Ongoing gap: behavioral model coefficients (satisfaction formula, incident rates) are analytically constructed, not empirically derived.
