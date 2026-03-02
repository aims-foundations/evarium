"""
Model Provider Actor for Evaluation Ecosystem Simulation

Represents an organization developing AI models in a competitive market.
Providers have imperfect knowledge of their own capabilities and must
infer them from noisy benchmark scores.

Key visibility design:
- PublicState: Visible to all actors (name, current_round, published_scores)
- PrivateState: Visible only to self (beliefs, strategies, history)
- GroundTruth: Held externally by simulation (true_capability)
"""
import json
import os
from dataclasses import dataclass, field, asdict
from typing import Optional

from visibility import PublicState, ProviderPrivateState, ProviderGroundTruth


@dataclass
class ModelProviderScratch:
    """
    Short-term memory / working state for a Model Provider.
    Analogous to Scratch in the original generative agents framework.

    NOTE: This class is maintained for backwards compatibility.
    New code should use the public/private state split via the
    ModelProvider.public_state and ModelProvider.private_state attributes.
    """
    # === IDENTITY ===
    name: str = ""
    strategy_profile: str = ""
    innate_traits: str = ""

    # === HIDDEN STATE (ground truth, not directly observable by provider) ===
    # NOTE: In the new architecture, true_capability should be stored
    # externally in the simulation's ground_truth dict. This field is
    # kept for backwards compatibility but will be synced with external state.
    true_capability: float = 0.5

    # === OBSERVABLE STATE ===
    last_score: Optional[float] = None
    current_round: int = 0

    # === BELIEF STATE (uncertain estimates, updated over time) ===
    believed_own_capability: float = 0.5
    believed_benchmark_exploitability: float = 0.3
    capability_belief_confidence: float = 0.5
    believed_competitor_capabilities: dict = field(default_factory=dict)

    # === INVESTMENT PORTFOLIO (decisions made each round) ===
    # These four investments must sum to effort_budget
    fundamental_research: float = 0.25  # Novel architectures, pre-training improvements
    training_optimization: float = 0.25  # Scaling, data quality, fine-tuning
    evaluation_engineering: float = 0.25  # Benchmark-specific optimization
    safety_alignment: float = 0.25  # RLHF, red-teaming, reliability
    effort_budget: float = 1.0

    # === HISTORY ===
    past_scores: list = field(default_factory=list)
    past_strategies: list = field(default_factory=list)
    observed_competitor_scores: dict = field(default_factory=dict)

    # === REFLECTION STATE ===
    importance_trigger_curr: float = 0.0
    importance_trigger_max: float = 100.0
    recent_insights: list = field(default_factory=list)

    def get_identity_summary(self) -> str:
        """Returns a string summary of the provider's identity for use in prompts."""
        summary = f"Name: {self.name}\n"
        summary += f"Strategy Profile: {self.strategy_profile}\n"
        summary += f"Core Traits: {self.innate_traits}\n"
        summary += f"Current Round: {self.current_round}\n"
        summary += f"Last Score: {self.last_score if self.last_score else 'None yet'}\n"
        summary += f"Believed Own Capability: {self.believed_own_capability:.2f}\n"
        summary += f"Believed Benchmark Exploitability: {self.believed_benchmark_exploitability:.2f}\n"
        return summary

    def get_strategy_summary(self) -> str:
        """Returns a summary of current investment portfolio."""
        return (f"Research: {self.fundamental_research:.0%}, "
                f"Training: {self.training_optimization:.0%}, "
                f"Eval Eng: {self.evaluation_engineering:.0%}, "
                f"Safety: {self.safety_alignment:.0%}")

    def get_history_summary(self, n_recent: int = 5) -> str:
        """Returns a summary of recent scores and strategies."""
        summary = "Recent History:\n"
        recent_scores = self.past_scores[-n_recent:] if self.past_scores else []
        recent_strategies = self.past_strategies[-n_recent:] if self.past_strategies else []

        for (r1, score), strategy in zip(recent_scores, recent_strategies):
            if isinstance(strategy, dict):
                summary += (f"  Round {r1}: Score={score:.2f}, "
                           f"Research={strategy.get('fundamental_research', 0):.0%}, "
                           f"Training={strategy.get('training_optimization', 0):.0%}, "
                           f"EvalEng={strategy.get('evaluation_engineering', 0):.0%}, "
                           f"Safety={strategy.get('safety_alignment', 0):.0%}\n")
            else:
                # Legacy format
                summary += f"  Round {r1}: Score={score:.2f}\n"

        if not recent_scores:
            summary += "  No history yet.\n"
        return summary

    def save(self, filepath: str):
        """Save scratch state to JSON file."""
        data = {
            "name": self.name,
            "strategy_profile": self.strategy_profile,
            "innate_traits": self.innate_traits,
            "true_capability": self.true_capability,
            "last_score": self.last_score,
            "current_round": self.current_round,
            "believed_own_capability": self.believed_own_capability,
            "believed_benchmark_exploitability": self.believed_benchmark_exploitability,
            "capability_belief_confidence": self.capability_belief_confidence,
            "believed_competitor_capabilities": self.believed_competitor_capabilities,
            "fundamental_research": self.fundamental_research,
            "training_optimization": self.training_optimization,
            "evaluation_engineering": self.evaluation_engineering,
            "safety_alignment": self.safety_alignment,
            "effort_budget": self.effort_budget,
            "past_scores": self.past_scores,
            "past_strategies": self.past_strategies,
            "observed_competitor_scores": self.observed_competitor_scores,
            "importance_trigger_curr": self.importance_trigger_curr,
            "importance_trigger_max": self.importance_trigger_max,
            "recent_insights": self.recent_insights,
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load(cls, filepath: str) -> "ModelProviderScratch":
        """Load scratch state from JSON file."""
        with open(filepath, "r") as f:
            data = json.load(f)
        return cls(**data)


class ModelProvider:
    """
    A Model Provider agent in the evaluation ecosystem simulation.

    Providers develop AI models and compete on benchmarks. They must decide
    how to allocate effort between genuine R&D (which improves true capability)
    and benchmark gaming (which improves scores without improving capability).

    Visibility Model:
    - public_state: Visible to all actors (name, round, published scores)
    - private_state: Visible only to self (beliefs, strategies, history)
    - ground_truth: Held externally by simulation (true_capability)

    The actor has NO direct access to ground_truth. The simulation manages
    ground truth externally and passes it to the evaluator for scoring.

    Modes:
    - llm_mode=False: Uses simple heuristics for planning/reflection (fast, no API calls)
    - llm_mode=True: Uses LLM for planning/reflection (slower, requires API key)
    """

    def __init__(
        self,
        name: str,
        strategy_profile: str,
        innate_traits: str,
        initial_capability: float = 0.5,
        initial_believed_capability: Optional[float] = None,
        initial_believed_exploitability: float = 0.3,
        llm_mode: bool = False,
        verbose_llm: bool = False,
        available_benchmarks: Optional[list] = None,
        focus_benchmarks: Optional[list] = None,
    ):
        """
        Initialize a Model Provider.

        Args:
            name: Unique identifier for this provider
            strategy_profile: Natural language description of strategic tendencies
            innate_traits: Core personality traits
            initial_capability: Starting true capability (will be stored in ground_truth)
            initial_believed_capability: Starting belief about own capability
                                        (defaults to initial_capability if None)
            initial_believed_exploitability: Starting belief about benchmark gaming
            llm_mode: If True, use LLM for planning/reflection; else use heuristics
            verbose_llm: If True, print LLM prompts and responses (for debugging)
        """
        # Initialize public state
        self.public_state = PublicState(
            name=name,
            current_round=0,
            published_scores=[],
        )

        # Initialize private state
        self.private_state = ProviderPrivateState(
            strategy_profile=strategy_profile,
            innate_traits=innate_traits,
            believed_own_capability=(
                initial_believed_capability
                if initial_believed_capability is not None
                else initial_capability
            ),
            believed_benchmark_exploitability=initial_believed_exploitability,
        )

        # Ground truth is now external, but we keep a reference for backwards compatibility
        # The simulation should manage this externally
        self._initial_capability = initial_capability

        # Initialize per-benchmark eval_eng routing weights
        # focus_benchmarks: priority-ordered list of benchmark names to specialize in
        # available_benchmarks: all benchmarks in the simulation at initialization
        self.private_state.benchmark_focus = self._compute_initial_focus(
            focus_benchmarks or [], available_benchmarks or []
        )

        # Legacy scratch for backwards compatibility
        # This syncs with public/private state
        self.scratch = ModelProviderScratch(
            name=name,
            strategy_profile=strategy_profile,
            innate_traits=innate_traits,
            true_capability=initial_capability,
            believed_own_capability=(
                initial_believed_capability
                if initial_believed_capability is not None
                else initial_capability
            ),
            believed_benchmark_exploitability=initial_believed_exploitability,
        )

        # Open-source provider flag (set after init via provider config)
        self.is_open_source: bool = False
        # Cost efficiency (0=closed-source default, 0.9=highly cost-competitive like DeepSeek)
        self.cost_advantage: float = 0.0
        # Contamination multiplier (extra gaming pressure on benchmarks when OS provider active)
        self.contamination_multiplier: float = 1.0
        # Threshold: true_capability level triggering one-time commoditization shock
        self.commoditization_threshold: float = 0.65
        # Ecosystem influence: cumulative adoption signal (0-100, logistic growth)
        self.ecosystem_influence: float = 0.0
        # Whether the commoditization shock has already fired for this provider
        self._commoditization_shock_fired: bool = False

        # Mode settings
        self.llm_mode = llm_mode
        self.verbose_llm = verbose_llm
        # When True, raises RuntimeError instead of silently falling back to heuristic
        self.llm_strict_mode = False
        self._llm_fallback_count = 0  # Consecutive fallback counter

        # Persistent incident safety pressure: accumulates on incidents, decays each round.
        # Survives across rounds so a major incident keeps safety investment elevated for
        # several rounds despite competitive pressure.
        self._incident_safety_pressure = 0.0

        # Memory structures
        self.memory = []

    @property
    def name(self) -> str:
        return self.public_state.name

    @property
    def true_capability(self) -> float:
        """For backwards compatibility. Ground truth should be managed externally."""
        return self.scratch.true_capability

    @true_capability.setter
    def true_capability(self, value: float):
        """Allow setting true_capability for backwards compatibility."""
        self.scratch.true_capability = value

    @property
    def fundamental_research(self) -> float:
        return self.private_state.fundamental_research

    @property
    def training_optimization(self) -> float:
        return self.private_state.training_optimization

    @property
    def evaluation_engineering(self) -> float:
        return self.private_state.evaluation_engineering

    @property
    def safety_alignment(self) -> float:
        return self.private_state.safety_alignment

    @property
    def benchmark_focus(self) -> dict:
        """Per-benchmark eval_eng weight vector (sums to 1.0)."""
        return self.private_state.benchmark_focus

    # Backwards compatibility properties
    @property
    def rnd_investment(self) -> float:
        """Backwards compatibility: R&D = fundamental_research + training_optimization"""
        return self.private_state.fundamental_research + self.private_state.training_optimization

    @property
    def gaming_investment(self) -> float:
        """Backwards compatibility: Gaming approximated by evaluation_engineering"""
        return self.private_state.evaluation_engineering

    @staticmethod
    def _compute_initial_focus(focus_benchmarks: list, available_benchmarks: list) -> dict:
        """
        Compute initial benchmark_focus weight vector from a priority-ordered focus list.

        Weight scheme:
        - 1 focus bm:  {focus[0]: 0.70, others: 0.30/(n-1)}
        - 2 focus bms: {focus[0]: 0.50, focus[1]: 0.30, others: 0.20/(n-2)}
        - 3+ focus bms:{focus[0]: 0.40, focus[1]: 0.30, focus[2]: 0.20, others: 0.10/(n-3)}
        - No focus / empty: uniform 1/n on all benchmarks
        """
        if not available_benchmarks:
            # No benchmarks known yet; return empty (will be populated on first update)
            return {}

        n = len(available_benchmarks)
        focus = [b for b in focus_benchmarks if b in available_benchmarks]

        if not focus:
            w = 1.0 / n
            return {bm: w for bm in available_benchmarks}

        weights = {}
        # Priority weight tables for focused benchmarks; remainder split among unfocused.
        # For 4+ focus benchmarks a geometric decay tail is used so all focus bms get
        # meaningfully elevated weight vs unfocused benchmarks.
        if len(focus) == 1:
            top_weights = [0.70]
            remainder = 0.30
        elif len(focus) == 2:
            top_weights = [0.50, 0.30]
            remainder = 0.20
        elif len(focus) == 3:
            top_weights = [0.40, 0.28, 0.20]
            remainder = 0.12
        elif len(focus) == 4:
            top_weights = [0.35, 0.25, 0.18, 0.12]
            remainder = 0.10
        elif len(focus) == 5:
            top_weights = [0.30, 0.22, 0.16, 0.12, 0.08]
            remainder = 0.12
        else:
            # 6+ focus benchmarks: assign top 6 with geometric tail, rest uniform remainder
            top_weights = [0.25, 0.18, 0.14, 0.10, 0.08, 0.06]
            remainder = 0.19
            focus = focus[:6]

        for bm in available_benchmarks:
            if bm in focus:
                idx = focus.index(bm)
                weights[bm] = top_weights[idx]
            else:
                n_others = n - len(focus)
                weights[bm] = remainder / n_others if n_others > 0 else 0.0

        # Normalize to sum to 1.0
        total = sum(weights.values())
        if total > 0:
            weights = {k: v / total for k, v in weights.items()}
        return weights

    def _update_benchmark_focus(self, ecosystem_context: Optional[dict] = None):
        """
        Update benchmark_focus weights each round.

        Steps:
        1. Expand focus dict to include any new benchmarks (with trait-affinity weights).
        2. Apply competitive pull: increase weight on benchmarks where we lag the leader.
        3. Add stochastic perturbation to prevent determinism.
        4. Clip to [0.05, 0.80] and re-normalize.
        """
        import numpy as _np

        ctx = ecosystem_context or {}
        available = ctx.get("available_benchmarks", [])
        per_bm_scores = ctx.get("per_benchmark_scores", {})

        focus = self.private_state.benchmark_focus

        # If no benchmarks known yet, skip
        if not available:
            return

        # 1. Expand to include new benchmarks
        traits_text = (
            self.private_state.innate_traits + " " +
            self.private_state.strategy_profile
        ).lower()
        affinity_keywords = {
            "coding":               ["coding", "software", "engineering", "developer", "api"],
            "coding_advanced":      ["coding", "software", "engineering", "developer", "api"],
            "reasoning":            ["reasoning", "logic", "research", "general", "analytical"],
            "reasoning_advanced":   ["reasoning", "logic", "research", "general", "analytical"],
            "math":                 ["math", "reasoning", "science", "research", "technical"],
            "math_advanced":        ["math", "reasoning", "science", "research", "technical"],
            "safety":               ["safety", "alignment", "risk", "guardrails", "responsible", "harmless"],
            "safety_advanced":      ["safety", "alignment", "risk", "guardrails", "responsible", "harmless"],
            "writing":              ["writing", "content", "creative", "marketing", "communication", "consumer"],
            "instruction_following":["instruction", "reliable", "precise", "enterprise", "product"],
            "long_context":         ["enterprise", "document", "legal", "finance", "long", "context"],
            "medical":              ["medical", "healthcare", "clinical", "health", "hospital"],
            "legal":                ["legal", "law", "compliance", "regulatory", "policy"],
            "finance":              ["finance", "financial", "economic", "investment", "enterprise"],
            "agentic":              ["agentic", "agent", "product", "api", "developer", "software"],
            "live_bench":           ["research", "general", "analytical", "rigorous", "science"],
        }

        rng = self._get_rng()
        new_bms = [bm for bm in available if bm not in focus]
        for bm in new_bms:
            # Compute affinity: look up exact benchmark name, then fall back to substring match
            affinity = 0.2
            keywords = affinity_keywords.get(bm)
            if keywords is None:
                # Substring fallback for unknown benchmark names
                for grp_name, grp_kws in affinity_keywords.items():
                    if grp_name in bm or any(kw in bm for kw in grp_kws):
                        keywords = grp_kws
                        break
            if keywords and any(kw in traits_text for kw in keywords):
                affinity = 0.6
            weight = float(_np.clip(affinity + rng.normal(0, 0.15), 0.05, 0.80))
            focus[bm] = weight

        # Remove benchmarks no longer in available set
        for bm in list(focus.keys()):
            if bm not in available:
                del focus[bm]

        if not focus:
            return

        n = len(focus)

        # 2. Competitive pull: shift weight toward benchmarks where we lag the leader
        own_name = self.public_state.name
        for bm in list(focus.keys()):
            bm_scores = per_bm_scores.get(bm, {})
            if not bm_scores:
                continue
            own_score = bm_scores.get(own_name, 0.0)
            leader_score = max(bm_scores.values())
            gap = leader_score - own_score
            if gap > 0.05:
                shift = min(0.08, gap * 0.3)
                focus[bm] = focus[bm] + shift

        # 3. Stochastic perturbation
        for bm in focus:
            focus[bm] += float(rng.normal(0, 0.03))

        # 4. Clip and normalize
        for bm in focus:
            focus[bm] = float(_np.clip(focus[bm], 0.05, 0.80))

        total = sum(focus.values())
        if total > 0:
            for bm in focus:
                focus[bm] /= total

        self.private_state.benchmark_focus = focus

    def _get_rng(self):
        """Get or create a numpy RNG for this provider (seeded by name for reproducibility)."""
        if not hasattr(self, "_rng"):
            import numpy as _np
            seed = sum(ord(c) for c in self.name) % (2**31)
            self._rng = _np.random.default_rng(seed)
        return self._rng

    def get_prompt_context(self) -> str:
        """
        Get the context available for LLM prompts.

        This method returns ONLY public and private state - never ground truth.
        This ensures LLM prompts cannot leak invisible information.
        """
        context = "=== PUBLIC INFORMATION ===\n"
        context += self.public_state.get_summary()
        context += "\n=== YOUR PRIVATE STATE ===\n"
        context += self.private_state.get_summary()
        context += self.private_state.get_history_summary()
        return context

    def observe(self, own_score: float, competitor_scores: dict, round_num: int):
        """
        Observe the results of an evaluation round.

        Args:
            own_score: This provider's benchmark score
            competitor_scores: Dict of {provider_name: score} for competitors
            round_num: Current simulation round
        """
        # Update public state
        self.public_state.current_round = round_num
        self.public_state.published_scores.append((round_num, own_score))

        # Update private state with competitor observations
        for comp_name, comp_score in competitor_scores.items():
            if comp_name not in self.private_state.observed_competitor_scores:
                self.private_state.observed_competitor_scores[comp_name] = []
            self.private_state.observed_competitor_scores[comp_name].append(
                (round_num, comp_score)
            )

        # Sync with legacy scratch
        self.scratch.last_score = own_score
        self.scratch.current_round = round_num
        self.scratch.past_scores.append((round_num, own_score))
        self.scratch.observed_competitor_scores = self.private_state.observed_competitor_scores

        # Add to memory
        self.memory.append({
            "type": "observation",
            "round": round_num,
            "own_score": own_score,
            "competitor_scores": competitor_scores,
        })

    def reflect(self):
        """
        Update beliefs based on observations.

        In LLM mode, uses LLM to reason about what scores imply about capability
        and benchmark properties. In heuristic mode, uses simple weighted averaging.
        """
        if self.llm_mode:
            self._reflect_llm()
        else:
            self._reflect_heuristic()

        # Update competitor capability beliefs based on their scores (always heuristic)
        for comp_name, score_history in self.private_state.observed_competitor_scores.items():
            if score_history:
                recent_scores = [s for _, s in score_history[-3:]]
                avg_score = sum(recent_scores) / len(recent_scores)
                self.private_state.believed_competitor_capabilities[comp_name] = avg_score

        # Sync with legacy scratch
        self.scratch.believed_own_capability = self.private_state.believed_own_capability
        self.scratch.believed_benchmark_exploitability = self.private_state.believed_benchmark_exploitability
        self.scratch.believed_competitor_capabilities = self.private_state.believed_competitor_capabilities

        # Record reflection in memory
        self.memory.append({
            "type": "reflection",
            "round": self.public_state.current_round,
            "updated_believed_capability": self.private_state.believed_own_capability,
            "updated_believed_exploitability": self.private_state.believed_benchmark_exploitability,
            "updated_competitor_beliefs": dict(self.private_state.believed_competitor_capabilities),
            "llm_mode": self.llm_mode,
        })

    def _reflect_heuristic(self):
        """Heuristic belief update (fast, no API calls)."""
        if self.public_state.published_scores:
            last_score = self.public_state.published_scores[-1][1]
            # Weighted average of prior belief and new observation
            learning_rate = 0.3
            self.private_state.believed_own_capability = (
                (1 - learning_rate) * self.private_state.believed_own_capability +
                learning_rate * last_score
            )

    def _reflect_llm(self):
        """LLM-driven belief update."""
        from llm import llm_reflect

        # Build recent history for the prompt
        recent_history = self._get_recent_history()

        # No history yet (round 0) — nothing meaningful to reflect on; use heuristic
        if not recent_history:
            self._reflect_heuristic()
            return

        # Call LLM
        new_capability, new_exploitability, reasoning = llm_reflect(
            name=self.name,
            strategy_profile=self.private_state.strategy_profile,
            current_believed_capability=self.private_state.believed_own_capability,
            current_believed_exploitability=self.private_state.believed_benchmark_exploitability,
            recent_history=recent_history,
            verbose=self.verbose_llm,
        )

        # Update beliefs
        self.private_state.believed_own_capability = new_capability
        self.private_state.believed_benchmark_exploitability = new_exploitability

        # Store reasoning
        self.private_state.recent_insights.append({
            "round": self.public_state.current_round,
            "type": "reflection",
            "reasoning": reasoning,
        })
        self.scratch.recent_insights = self.private_state.recent_insights

    def plan(self, ecosystem_context: Optional[dict] = None) -> dict:
        """
        Decide investment portfolio allocation for the next round.

        Args:
            ecosystem_context: Optional dict with public ecosystem signals
                (consumer_satisfaction, regulatory_pressure)

        Returns:
            Dict with keys: fundamental_research, training_optimization,
                           evaluation_engineering, safety_alignment
        """
        if self.llm_mode:
            portfolio, reasoning = self._plan_llm(ecosystem_context)
        else:
            portfolio = self._plan_heuristic(ecosystem_context)
            reasoning = None

        # Update private state
        self.private_state.fundamental_research = portfolio["fundamental_research"]
        self.private_state.training_optimization = portfolio["training_optimization"]
        self.private_state.evaluation_engineering = portfolio["evaluation_engineering"]
        self.private_state.safety_alignment = portfolio["safety_alignment"]

        # Update per-benchmark focus weights (heuristic, always)
        self._update_benchmark_focus(ecosystem_context)

        # Store strategy as dict in past_strategies
        strategy_record = {
            "round": self.public_state.current_round,
            "fundamental_research": portfolio["fundamental_research"],
            "training_optimization": portfolio["training_optimization"],
            "evaluation_engineering": portfolio["evaluation_engineering"],
            "safety_alignment": portfolio["safety_alignment"],
        }
        self.private_state.past_strategies.append(strategy_record)

        # Sync with legacy scratch
        self.scratch.fundamental_research = portfolio["fundamental_research"]
        self.scratch.training_optimization = portfolio["training_optimization"]
        self.scratch.evaluation_engineering = portfolio["evaluation_engineering"]
        self.scratch.safety_alignment = portfolio["safety_alignment"]
        self.scratch.past_strategies = self.private_state.past_strategies

        # Record in memory
        memory_entry = {
            "type": "planning",
            "round": self.public_state.current_round,
            "portfolio": portfolio,
            "llm_mode": self.llm_mode,
        }
        if reasoning:
            memory_entry["reasoning"] = reasoning
        self.memory.append(memory_entry)

        return portfolio

    def _plan_heuristic(self, ecosystem_context: Optional[dict] = None) -> dict:
        """
        Heuristic investment portfolio planning (fast, no API calls).

        Portfolio allocation logic:
        - Base allocation: previous round's allocation (preserves provider identity/personality)
        - Competitive pressure adjusts evaluation_engineering vs fundamental_research
        - Safety incidents push resources toward safety_alignment
        - Personality traits influence the balance
        - Loose bounds prevent any category collapsing to zero or dominating entirely
        """
        my_believed = self.private_state.believed_own_capability
        competitor_beliefs = self.private_state.believed_competitor_capabilities
        budget = self.private_state.effort_budget
        ctx = ecosystem_context or {}

        # Start from previous allocation so provider identity persists across rounds.
        # Round 0 config-set values (e.g. Orion Labs 15/50/30/5, Apex AI 35/20/5/40)
        # carry forward rather than being reset to 25/25/25/25 each round.
        fundamental = self.private_state.fundamental_research
        training = self.private_state.training_optimization
        eval_eng = self.private_state.evaluation_engineering
        safety = self.private_state.safety_alignment

        # Competitive pressure: if behind, shift from research to eval engineering
        if competitor_beliefs:
            max_competitor = max(competitor_beliefs.values())
            gap = max_competitor - my_believed  # Positive if behind

            # Shift up to 15% between fundamental research and eval engineering
            shift = gap * 0.3  # Scale factor
            shift = max(-0.15, min(0.15, shift))

            fundamental -= shift
            eval_eng += shift

        # Incident pressure: own safety incidents force a safety investment bump.
        # Severity multipliers doubled vs original so incidents compete with competitive pressure.
        # Pressure is persistent and decays 40% per round so impact lasts ~3-4 rounds.
        own_incidents = ctx.get("own_incidents", [])
        if own_incidents:
            severity_shifts = {"minor": 0.03, "moderate": 0.10, "major": 0.20, "critical": 0.30}
            new_pressure = sum(
                severity_shifts.get(inc.get("severity", "minor"), 0.0)
                for inc in own_incidents
            )
            new_pressure = min(new_pressure, 0.30)  # Cap per-round accumulation
            self._incident_safety_pressure = min(
                0.40,  # Overall cap
                self._incident_safety_pressure + new_pressure,
            )

        # Apply persistent incident pressure (shift from eval_eng to safety),
        # then decay it so the effect fades over several rounds.
        if self._incident_safety_pressure > 0.005:
            eval_eng -= self._incident_safety_pressure
            safety += self._incident_safety_pressure
            self._incident_safety_pressure *= 0.60  # ~50% gone after 1 round, ~88% after 4

        # Apply personality modifiers
        profile_lower = self.private_state.strategy_profile.lower()

        if "aggressive" in profile_lower or "competitive" in profile_lower:
            # Aggressive: more eval engineering, less safety
            eval_eng += 0.05
            safety -= 0.05

        if "quality" in profile_lower or "long-term" in profile_lower:
            # Quality-focused: more fundamental research, less eval engineering
            fundamental += 0.05
            eval_eng -= 0.05

        if "risk-averse" in self.private_state.innate_traits.lower():
            # Risk-averse: more safety
            safety += 0.05
            eval_eng -= 0.05

        # Open-source provider: community benchmark optimization bias + lower safety floor
        if self.is_open_source:
            eval_eng += 0.05  # Community benchmark optimization bias
            # Lower safety floor applies at clamping stage below

        # Loose bounds: prevent any category from collapsing to zero or dominating entirely.
        # These are intentionally wide — providers can still specialize, but can't drop
        # safety to 0% or go 80%+ eval_eng.
        # Open-source providers have a lower safety floor (0.03 vs 0.05 for closed).
        safety_floor = 0.03 if self.is_open_source else 0.05
        fundamental = max(0.05, min(0.65, fundamental))
        training    = max(0.05, min(0.70, training))
        eval_eng    = max(0.02, min(0.55, eval_eng))
        safety      = max(safety_floor, min(0.55, safety))

        # Normalize to ensure they sum to budget
        total = fundamental + training + eval_eng + safety
        fundamental = (fundamental / total) * budget
        training    = (training    / total) * budget
        eval_eng    = (eval_eng    / total) * budget
        safety      = (safety      / total) * budget

        return {
            "fundamental_research": fundamental,
            "training_optimization": training,
            "evaluation_engineering": eval_eng,
            "safety_alignment": safety,
        }

    def _plan_llm(self, ecosystem_context: Optional[dict] = None) -> tuple[dict, str]:
        """LLM-driven investment portfolio planning."""
        from llm import llm_plan_portfolio

        # Get recent competitor scores
        competitor_scores = {}
        for comp_name, score_history in self.private_state.observed_competitor_scores.items():
            if score_history:
                competitor_scores[comp_name] = score_history[-1][1]

        # Build recent history
        recent_history = self._get_recent_history()

        # Get last score
        last_score = None
        if self.public_state.published_scores:
            last_score = self.public_state.published_scores[-1][1]

        # Extract ecosystem context
        ctx = ecosystem_context or {}

        # Call LLM
        portfolio, reasoning = llm_plan_portfolio(
            name=self.name,
            strategy_profile=self.private_state.strategy_profile,
            innate_traits=self.private_state.innate_traits,
            believed_capability=self.private_state.believed_own_capability,
            believed_exploitability=self.private_state.believed_benchmark_exploitability,
            last_score=last_score,
            competitor_scores=competitor_scores,
            recent_history=recent_history,
            consumer_satisfaction=ctx.get("consumer_satisfaction"),
            regulatory_pressure=ctx.get("regulatory_pressure"),
            per_benchmark_scores=ctx.get("per_benchmark_scores"),
            benchmark_focus=self.private_state.benchmark_focus or None,
            verbose=self.verbose_llm,
        )

        # Detect silent fallback: fail_safe thinking field contains "fallback"
        is_fallback = "fallback" in str(reasoning).lower() or "fallback" in str(
            portfolio.get("thinking", "")
        ).lower()
        if is_fallback:
            self._llm_fallback_count += 1
            print(f"[LLM STRICT] {self.name} round {self.public_state.current_round}: "
                  f"LLM returned fail_safe (fallback #{self._llm_fallback_count}). "
                  f"Reasoning: {reasoning!r}")
            if self.llm_strict_mode:
                raise RuntimeError(
                    f"LLM fallback detected for {self.name} (round "
                    f"{self.public_state.current_round}). API call failed or returned "
                    f"unparseable response. Set llm_strict_mode=False to allow fallback, "
                    f"or fix the API connectivity issue."
                )
        else:
            self._llm_fallback_count = 0  # Reset on successful LLM call

        # Store reasoning
        self.private_state.recent_insights.append({
            "round": self.public_state.current_round,
            "type": "planning",
            "reasoning": reasoning,
        })
        self.scratch.recent_insights = self.private_state.recent_insights

        return portfolio, reasoning

    def _get_recent_history(self, n: int = 10) -> list:
        """Get recent history as list of dicts with round, score, and portfolio."""
        history = []
        scores = self.public_state.published_scores[-n:]
        strategies = self.private_state.past_strategies[-n:]

        for (round_num, score), strategy in zip(scores, strategies):
            if isinstance(strategy, dict):
                entry = {
                    "round": round_num,
                    "score": score,
                    "fundamental_research": strategy.get("fundamental_research", 0),
                    "training_optimization": strategy.get("training_optimization", 0),
                    "evaluation_engineering": strategy.get("evaluation_engineering", 0),
                    "safety_alignment": strategy.get("safety_alignment", 0),
                }
            else:
                # Legacy format - approximate
                entry = {"round": round_num, "score": score}
            history.append(entry)

        return history

    def execute(self, efficiency: float = 0.01):
        """
        Apply the chosen investment portfolio - update true capability.

        NOTE: In the new architecture, capability updates should be handled
        by the simulation using external ground truth. This method is kept
        for backwards compatibility.

        Capability gain formula:
        - Fundamental research: High variance, high ceiling (1.5x efficiency)
        - Training optimization: Moderate, reliable gains (1.0x efficiency)
        - Evaluation engineering: Minimal capability gain (0.1x efficiency)
        - Safety alignment: No direct capability gain, but affects reliability

        Args:
            efficiency: Base efficiency for capability improvement
        """
        # Different investment types contribute differently to capability
        capability_gain = (
            self.private_state.fundamental_research * efficiency * 1.5 +
            self.private_state.training_optimization * efficiency * 1.0 +
            self.private_state.evaluation_engineering * efficiency * 0.1
            # Safety alignment doesn't directly improve capability
        )
        self.scratch.true_capability += capability_gain

        self.memory.append({
            "type": "execution",
            "round": self.public_state.current_round,
            "capability_gain": capability_gain,
            "new_true_capability": self.scratch.true_capability,
            "portfolio": {
                "fundamental_research": self.private_state.fundamental_research,
                "training_optimization": self.private_state.training_optimization,
                "evaluation_engineering": self.private_state.evaluation_engineering,
                "safety_alignment": self.private_state.safety_alignment,
            },
        })

    def decide_premium_access(
        self,
        premium_pricing: float,
        current_budget: float,
        ecosystem_context: Optional[dict] = None
    ) -> dict:
        """
        Decide whether to purchase premium evaluator access.

        Premium access provides:
        - Best-of-N submission (multiple trials, publish best score)
        - Early access to new benchmarks (3 rounds before public introduction)

        Decision factors:
        - Can afford: current budget >= premium pricing
        - Behind competitors: own market share < 30%
        - High eval engineering investment: evaluation_engineering > 0.3
        - Strategic value: gaming-oriented providers benefit most

        Args:
            premium_pricing: Cost of premium access
            current_budget: Available budget
            ecosystem_context: Optional dict with own_market_share, competitor_scores, etc.

        Returns:
            Dict with purchase_premium (bool), amount (float), reasoning (str)
        """
        ctx = ecosystem_context or {}

        own_share = ctx.get("own_market_share", 0.5)
        behind = own_share < 0.3
        high_eval_eng = self.private_state.evaluation_engineering > 0.3
        can_afford = current_budget >= premium_pricing

        # Decision logic: purchase if can afford AND (behind OR high eval eng)
        should_purchase = can_afford and (behind or high_eval_eng)

        reasoning = []
        if should_purchase:
            reasoning.append(f"Purchasing premium access (${premium_pricing:,.0f})")
            if behind:
                reasoning.append(f"Market position: {own_share:.1%} (behind competitors)")
            if high_eval_eng:
                reasoning.append(f"High eval engineering investment: {self.private_state.evaluation_engineering:.1%}")
        else:
            if not can_afford:
                reasoning.append(f"Cannot afford premium access (budget: ${current_budget:,.0f})")
            else:
                reasoning.append(f"Premium access not strategic (share: {own_share:.1%}, eval_eng: {self.private_state.evaluation_engineering:.1%})")

        return {
            "purchase_premium": should_purchase,
            "amount": premium_pricing if should_purchase else 0.0,
            "reasoning": " | ".join(reasoning),
        }

    def step(self, own_score: float, competitor_scores: dict, round_num: int,
             efficiency: float = 0.01) -> dict:
        """
        Complete one simulation step: observe, reflect, plan, execute.

        Args:
            own_score: This provider's benchmark score from the previous round
            competitor_scores: Dict of competitor scores
            round_num: Current round number
            efficiency: Base efficiency for capability improvement

        Returns:
            Dict with investment portfolio for this round
        """
        self.observe(own_score, competitor_scores, round_num)
        self.reflect()
        portfolio = self.plan()
        self.execute(efficiency)
        return portfolio

    def save(self, folder: str):
        """Save provider state to a folder."""
        os.makedirs(folder, exist_ok=True)

        # Save legacy scratch
        self.scratch.save(f"{folder}/scratch.json")

        # Save new visibility state
        with open(f"{folder}/public_state.json", "w") as f:
            json.dump(self.public_state.to_dict(), f, indent=2)

        with open(f"{folder}/private_state.json", "w") as f:
            json.dump(self.private_state.to_dict(), f, indent=2)

        # Save memory
        with open(f"{folder}/memory.json", "w") as f:
            json.dump(self.memory, f, indent=2)

    @classmethod
    def load(cls, folder: str) -> "ModelProvider":
        """Load provider state from a folder."""
        scratch = ModelProviderScratch.load(f"{folder}/scratch.json")
        provider = cls(
            name=scratch.name,
            strategy_profile=scratch.strategy_profile,
            innate_traits=scratch.innate_traits,
        )
        provider.scratch = scratch

        # Load new visibility state if available
        public_path = f"{folder}/public_state.json"
        private_path = f"{folder}/private_state.json"

        if os.path.exists(public_path):
            with open(public_path, "r") as f:
                provider.public_state = PublicState.from_dict(json.load(f))

        if os.path.exists(private_path):
            with open(private_path, "r") as f:
                provider.private_state = ProviderPrivateState.from_dict(json.load(f))

        # Load memory
        with open(f"{folder}/memory.json", "r") as f:
            provider.memory = json.load(f)

        return provider

    def __repr__(self):
        return (f"ModelProvider(name='{self.name}', "
                f"true_cap={self.true_capability:.2f}, "
                f"believed_cap={self.private_state.believed_own_capability:.2f}, "
                f"portfolio=[R:{self.fundamental_research:.0%}, T:{self.training_optimization:.0%}, "
                f"E:{self.evaluation_engineering:.0%}, S:{self.safety_alignment:.0%}])")
