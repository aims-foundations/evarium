"""
Model Provider Actor for Evaluation Ecosystem Simulation

Represents an organization developing AI models in a competitive market.

Gaming is not an explicit investment lever. Goodhart dynamics emerge when
benchmark dimension weights diverge from consumer need weights and providers
discover — through score signals — that specializing toward benchmark-measured
dimensions raises scores faster than it raises satisfaction.

Visibility model:
- PublicState: benchmark scores, market share, public_comms (visible to all)
- PrivateState: portfolio, focus_level, inferred_benchmark_weights,
                benchmark_orientation, consumer_signal (self only)
- GroundTruth: capability_vector, market_share, incidents (simulation only)

Modes:
- llm_mode=False: Heuristic planning and belief updates (fast, no API calls)
- llm_mode=True: LLM planning with ordinal output signals
"""
import json
import os
from dataclasses import dataclass, field
from typing import Optional

from visibility import PublicState, ProviderPrivateState, ProviderGroundTruth

# Ordered list of capability dimensions (must match capability_dimensions.py)
DIMENSIONS = ["reasoning", "coding", "knowledge", "safety", "communication", "agentic"]

# Ordinal step sizes applied to portfolio fractions, focus_level, and benchmark_orientation.
# 5-level scale: much_more / more / same / less / much_less
# Clipped and renormalized after application.
ORDINAL_DELTA = 0.05         # "more" / "less"
ORDINAL_DELTA_LARGE = 0.10   # "much_more" / "much_less"

def _ordinal_to_delta(signal: str) -> float:
    """Map a 5-level ordinal signal to a numeric delta."""
    return {
        "much_more": ORDINAL_DELTA_LARGE,
        "more": ORDINAL_DELTA,
        "same": 0.0,
        "less": -ORDINAL_DELTA,
        "much_less": -ORDINAL_DELTA_LARGE,
    }.get(signal, 0.0)

# Bounds for benchmark_orientation
BENCHMARK_ORIENTATION_MIN = 0.05
BENCHMARK_ORIENTATION_MAX = 0.95

# Signal quality: product investment -> R&D targeting accuracy
_CONSUMER_SIGNAL_FIDELITY_K = 3.0        # Sigmoid steepness
_CONSUMER_SIGNAL_FIDELITY_MID = 0.5      # Budget midpoint for 50% quality
_OS_QUALITY_CEILING = 0.40     # Open-source structural ceiling

def _consumer_signal_fidelity(product_budget: float, is_open_source: bool = False) -> float:
    """Continuous signal quality from product budget.

    Sigmoid: quality = 1 / (1 + exp(-k * (budget - mid)))
    Open-source providers capped at os_ceiling.

    At budget=0: ~18% quality (some signal from market share data alone).
    At budget=mid: 50% quality.
    At budget >> mid: approaches 1.0.
    """
    import math
    raw = 1.0 / (1.0 + math.exp(-_CONSUMER_SIGNAL_FIDELITY_K * (product_budget - _CONSUMER_SIGNAL_FIDELITY_MID)))
    if is_open_source:
        return min(raw, _OS_QUALITY_CEILING)
    return raw


class ModelProvider:
    """
    A Model Provider agent in the evaluation ecosystem simulation.

    Providers develop AI models and compete on benchmarks. They allocate a
    training budget across three levers (rd, safety, product) and choose,
    per capability dimension, how narrowly or broadly to target training.

    Gaming emerges from focus_level and inferred_benchmark_weights — when
    providers learn that certain benchmark-weighted dimensions yield faster
    score gains, they concentrate R&D there. The score-satisfaction gap
    is discovered by the simulation, not imposed.
    """

    def __init__(
        self,
        name: str,
        strategy_profile: str,
        innate_traits: str,
        capability_vector: Optional[dict] = None,
        portfolio: Optional[dict] = None,
        focus_level_init: Optional[dict] = None,
        benchmark_orientation: float = 0.80,
        llm_mode: bool = False,
        verbose_llm: bool = False,
        # Open-source provider config
        open_source: bool = False,
        openness_level: float = 0.0,
        cost_advantage: float = 0.0,
        rd_budget_floor: float = 0.0,
        os_belief_broadcast: bool = True,
        os_safety_erosion: bool = True,
        # Evaluator-as-company: parent company resources for eval access
        discretionary_budget: float = 0.0,
    ):
        """
        Initialize a Model Provider.

        Args:
            name: Unique identifier for this provider.
            strategy_profile: Natural language description of strategic tendencies.
            innate_traits: Core personality traits.
            capability_vector: Initial per-dimension capability scores {dim: float}.
                Defaults to provider preset values; simulation overrides at setup.
            portfolio: Initial {rd, safety, product} fractions summing to 1.0.
            focus_level_init: Initial per-benchmark focus scalars {benchmark: float}.
                Populated at simulation setup when benchmarks are known.
            benchmark_orientation: Initial blend weight [0.05, 0.95].
            llm_mode: If True, use LLM for planning each round.
            verbose_llm: If True, print LLM prompts/responses for debugging.
            open_source: Whether this is an open-source provider.
            openness_level: 0=closed, 0.5=open-weight, 1.0=fully-open.
            cost_advantage: Relative pricing competitiveness (0=expensive, 1=free).
            rd_budget_floor: Exogenous minimum R&D budget (for OS providers).
            os_belief_broadcast: Whether OS weights accelerate competitors' belief convergence.
            os_safety_erosion: Whether deployed safety is discounted below nominal.
        """
        # Public state
        self.public_state = PublicState(
            name=name,
            current_round=0,
            benchmark_scores={},
            market_share=0.0,
            public_comms=[],
        )

        # Private state
        default_portfolio = portfolio or {"rd": 0.55, "safety": 0.25, "product": 0.20}
        self.private_state = ProviderPrivateState(
            strategy_profile=strategy_profile,
            innate_traits=innate_traits,
            portfolio=dict(default_portfolio),
            focus_level=dict(focus_level_init) if focus_level_init else {},
            inferred_benchmark_weights={},
            benchmark_orientation=float(benchmark_orientation),
            consumer_signal={},
        )

        # Initial capability vector stored for simulation to read at setup.
        # After setup the simulation manages ground truth externally.
        self._initial_capability_vector = capability_vector or {
            dim: 0.5 for dim in DIMENSIONS
        }

        # Open-source provider fields
        self.open_source: bool = open_source
        self.openness_level: float = openness_level
        self.cost_advantage: float = cost_advantage
        self.rd_budget_floor: float = rd_budget_floor
        self.os_belief_broadcast: bool = os_belief_broadcast
        self.os_safety_erosion: bool = os_safety_erosion
        self.discretionary_budget: float = discretionary_budget

        # Mode settings
        self.llm_mode = llm_mode
        self.verbose_llm = verbose_llm
        self.llm_strict_mode = False
        self._llm_fallback_count = 0

        # Incident safety pressure: accumulates on incidents, decays each round.
        self._incident_safety_pressure: float = 0.0

        # Portfolio history for rolling average (organizational inertia).
        # Stores last N portfolio dicts; effective_portfolio averages them.
        # Seeded with initial portfolio so round 0 is included in the window.
        self._portfolio_history: list = [dict(self.private_state.portfolio)]
        self._effective_portfolio: dict = dict(self.private_state.portfolio)
        self._last_consumer_signal_fidelity: float = 0.0

        # Regulatory pressure: boost to safety public_comms weight (from voluntary
        # commitment / disclosure mandates). Decays each round.
        self._safety_comms_boost: float = 0.0

        # Ablation: route safety lever through target weights instead of direct-to-safety
        self.safety_lever_through_target: bool = False

        # Evaluator-as-company: number of model submissions last decided
        self._last_n_submissions: int = 1

        # Per-round memory list (within-session only — not persisted in ProviderPrivateState)
        self.memory: list = []

    # ──────────────────────────────────────────────────────────────────────
    # Properties
    # ──────────────────────────────────────────────────────────────────────

    @property
    def name(self) -> str:
        return self.public_state.name

    @property
    def portfolio(self) -> dict:
        return self.private_state.portfolio

    @property
    def rd_investment(self) -> float:
        return self.private_state.portfolio.get("rd", 0.0)

    @property
    def safety_investment(self) -> float:
        return self.private_state.portfolio.get("safety", 0.0)

    @property
    def product_investment(self) -> float:
        return self.private_state.portfolio.get("product", 0.0)

    # ──────────────────────────────────────────────────────────────────────
    # Benchmark belief initialization (called by simulation when new
    # benchmarks are introduced)
    # ──────────────────────────────────────────────────────────────────────

    def init_benchmark(self, benchmark_name: str):
        """
        Initialize beliefs and focus for a newly introduced benchmark.

        - inferred_benchmark_weights[b]: uniform across 6 dimensions
        - focus_level[b]: mean of existing focus_level values (or 1.0 if first)
        """
        # Uniform initial belief
        uniform = {dim: 1.0 / len(DIMENSIONS) for dim in DIMENSIONS}
        self.private_state.inferred_benchmark_weights[benchmark_name] = uniform

        # Focus: preserve focus_level_init value if already set; otherwise initialize
        # at mean of existing benchmarks (used for newly-introduced benchmarks mid-sim).
        if benchmark_name not in self.private_state.focus_level:
            existing = list(self.private_state.focus_level.values())
            init_focus = sum(existing) / len(existing) if existing else 1.0
            self.private_state.focus_level[benchmark_name] = init_focus

    # ──────────────────────────────────────────────────────────────────────
    # Observe
    # ──────────────────────────────────────────────────────────────────────

    def observe(
        self,
        round_num: int,
        own_benchmark_scores: dict,
        competitor_benchmark_scores: dict,
        consumer_signal: Optional[dict] = None,
        market_share: Optional[float] = None,
    ):
        """
        Observe results of an evaluation round.

        Args:
            round_num: Current simulation round.
            own_benchmark_scores: {benchmark_name: {"overall": float, "per_category": {cat: float}}}
            competitor_benchmark_scores: {provider_name: {benchmark_name: float}}
                (overall scores only — per-category not needed for competitor tracking)
            consumer_signal: 6-dim normalized need vector from simulation, or None.
            market_share: Own current market share, or None.
        """
        self.public_state.current_round = round_num

        # Update per-benchmark score histories
        for bm_name, scores in own_benchmark_scores.items():
            overall = scores.get("overall", scores) if isinstance(scores, dict) else scores
            if bm_name not in self.public_state.benchmark_scores:
                self.public_state.benchmark_scores[bm_name] = []
            self.public_state.benchmark_scores[bm_name].append((round_num, overall))

        # Update competitor score observations
        for comp_name, bm_scores in competitor_benchmark_scores.items():
            if comp_name not in self.private_state.observed_competitor_scores:
                self.private_state.observed_competitor_scores[comp_name] = []
            # Aggregate to a single representative score for competitor belief tracking
            if isinstance(bm_scores, dict):
                vals = [v for v in bm_scores.values() if isinstance(v, (int, float))]
                agg = sum(vals) / len(vals) if vals else 0.0
            else:
                agg = float(bm_scores)
            self.private_state.observed_competitor_scores[comp_name].append((round_num, agg))

        # Update competitor capability beliefs
        for comp_name, score_history in self.private_state.observed_competitor_scores.items():
            if score_history:
                recent = [s for _, s in score_history[-3:]]
                self.private_state.believed_competitor_capabilities[comp_name] = (
                    sum(recent) / len(recent)
                )

        # Store satisfaction signal if provided
        if consumer_signal:
            self.private_state.consumer_signal = dict(consumer_signal)

        # Update public market share
        if market_share is not None:
            self.public_state.market_share = market_share

        self.memory.append({
            "type": "observation",
            "round": round_num,
            "own_scores": {k: (v.get("overall") if isinstance(v, dict) else v)
                           for k, v in own_benchmark_scores.items()},
            "market_share": market_share,
        })

    # ──────────────────────────────────────────────────────────────────────
    # Belief update (always heuristic — beliefs are epistemic, not LLM output)
    # ──────────────────────────────────────────────────────────────────────

    def update_benchmark_beliefs(
        self,
        own_benchmark_scores: dict,
        capability_vector: dict,
        learning_rate: float = 0.15,
    ):
        """
        Update inferred_benchmark_weights from score prediction errors.

        For each active benchmark b:
            predicted_score = dot(capability_vector, inferred_benchmark_weights[b])
            error = observed_score[b] - predicted_score
            for dim: inferred_benchmark_weights[b][dim] += lr * error * capability_vector[dim]
            normalize and clip non-negative

        Args:
            own_benchmark_scores: {benchmark_name: {"overall": float, ...}}
            capability_vector: Provider's current true capability vector (ground truth,
                passed in by simulation — never stored on provider).
            learning_rate: Step size for weight update.
        """
        for bm_name, scores in own_benchmark_scores.items():
            observed = scores.get("overall", scores) if isinstance(scores, dict) else float(scores)

            if bm_name not in self.private_state.inferred_benchmark_weights:
                self.init_benchmark(bm_name)

            weights = self.private_state.inferred_benchmark_weights[bm_name]

            # Predicted score under current belief
            predicted = sum(
                capability_vector.get(dim, 0.0) * weights.get(dim, 0.0)
                for dim in DIMENSIONS
            )
            error = observed - predicted

            # Delta rule update
            for dim in DIMENSIONS:
                weights[dim] = weights.get(dim, 0.0) + learning_rate * error * capability_vector.get(dim, 0.0)

            # Clip non-negative and normalize
            total = sum(max(0.0, w) for w in weights.values())
            if total > 0:
                self.private_state.inferred_benchmark_weights[bm_name] = {
                    dim: max(0.0, weights[dim]) / total for dim in DIMENSIONS
                }

    # ──────────────────────────────────────────────────────────────────────
    # Plan
    # ──────────────────────────────────────────────────────────────────────

    def plan(self, ecosystem_context: Optional[dict] = None) -> dict:
        """
        Decide investment portfolio allocation for the next round.

        Returns: portfolio dict {rd, safety, product} summing to 1.0.
        Also updates focus_level and benchmark_orientation via ordinal signals.
        """
        ctx = ecosystem_context or {}

        strategy_memo = None
        if self.llm_mode:
            portfolio, focus_deltas, orientation_delta, reasoning, strategy_memo = self._plan_llm(ctx)
            self._apply_ordinal_deltas(focus_deltas, orientation_delta)
        else:
            portfolio = self._plan_heuristic(ctx)
            reasoning = None

        # Apply and store portfolio
        self.private_state.portfolio = portfolio

        # Track portfolio history for rolling average (organizational inertia)
        self._portfolio_history.append(dict(portfolio))
        rolling_window = 3
        if len(self._portfolio_history) > rolling_window:
            self._portfolio_history = self._portfolio_history[-rolling_window:]

        # Compute effective portfolio (rolling average over last N rounds)
        # This represents organizational execution speed: decisions take time to fully implement.
        eff = {}
        for key in ("rd", "safety", "product"):
            eff[key] = sum(p.get(key, 0.0) for p in self._portfolio_history) / len(self._portfolio_history)
        # Renormalize to sum to 1.0 (in case of floating point drift)
        eff_total = sum(eff.values())
        if eff_total > 0:
            self._effective_portfolio = {k: v / eff_total for k, v in eff.items()}
        else:
            self._effective_portfolio = dict(portfolio)

        # Issue public_comms (heuristic sampling from portfolio weights)
        public_comm = self._sample_public_comms()
        if public_comm:
            self.public_state.public_comms.append({
                "round": self.public_state.current_round,
                "type": public_comm["type"],
                "content": public_comm["content"],
            })
            # Keep only last 5 comms
            self.public_state.public_comms = self.public_state.public_comms[-5:]

        # Record in past_strategies
        strategy_record = {
            "round": self.public_state.current_round,
            "rd": portfolio["rd"],
            "safety": portfolio["safety"],
            "product": portfolio["product"],
        }
        self.private_state.past_strategies.append(strategy_record)

        # Append reasoning to recent_insights if LLM mode
        if reasoning:
            self.private_state.recent_insights.append({
                "round": self.public_state.current_round,
                "type": "planning",
                "strategy_memo": strategy_memo or "",
                "reasoning": reasoning,  # store full reasoning
            })

        self.memory.append({
            "type": "planning",
            "round": self.public_state.current_round,
            "portfolio": portfolio,
            "llm_mode": self.llm_mode,
            "reasoning": reasoning,
        })

        return portfolio

    def _plan_heuristic(self, ctx: dict) -> dict:
        """
        Heuristic portfolio planning.

        Base allocation preserved from last round (provider identity persists).
        Adjustments:
        - Incident pressure shifts budget from rd toward safety.
        - Profile modifiers nudge allocation based on strategy_profile.
        - Bounds prevent any lever collapsing or dominating.
        """
        p = dict(self.private_state.portfolio)
        rd = p.get("rd", 0.55)
        safety = p.get("safety", 0.25)
        product = p.get("product", 0.20)

        # Incident pressure: accumulates from own_incidents, decays 60%/round
        own_incidents = ctx.get("own_incidents", [])
        if own_incidents:
            severity_shifts = {"minor": 0.01, "moderate": 0.04, "major": 0.08, "critical": 0.12}
            new_pressure = sum(
                severity_shifts.get(inc.get("severity", "minor"), 0.0)
                for inc in own_incidents
            )
            new_pressure = min(new_pressure, 0.20)
            self._incident_safety_pressure = min(
                0.25, self._incident_safety_pressure + new_pressure
            )

        if self._incident_safety_pressure > 0.005:
            rd -= self._incident_safety_pressure
            safety += self._incident_safety_pressure
            self._incident_safety_pressure *= 0.40

        # Profile modifiers
        profile_lower = self.private_state.strategy_profile.lower()
        traits_lower = self.private_state.innate_traits.lower()

        if "aggressive" in profile_lower or "competitive" in profile_lower:
            rd += 0.05
            safety -= 0.05

        if "quality" in profile_lower or "long-term" in profile_lower:
            rd += 0.03
            product -= 0.03

        if "safety" in profile_lower or "responsible" in profile_lower:
            safety += 0.05
            rd -= 0.05

        if "risk-averse" in traits_lower:
            safety += 0.03
            rd -= 0.03

        if "product" in profile_lower or "market" in profile_lower:
            product += 0.03
            rd -= 0.03

        # OS providers: slightly lower safety floor (fine-tuning can strip guardrails)
        safety_floor = 0.10 if self.open_source else 0.15

        # Bounds
        rd      = max(0.10, min(0.75, rd))
        safety  = max(safety_floor, min(0.55, safety))
        product = max(0.05, min(0.50, product))

        # Normalize to sum to 1.0
        total = rd + safety + product
        return {
            "rd":      rd / total,
            "safety":  safety / total,
            "product": product / total,
        }

    def _decide_n_submissions_heuristic(self, base_revenue: float, fee: float, max_n: int) -> int:
        """Decide how many model variants to submit to evaluator (heuristic mode).

        Affordability is based on base_revenue + discretionary_budget (parent
        company resources). Fee is still deducted from R&D budget in sim loop.
        Spends up to 15% of total affordability on extra submissions.
        """
        affordability = base_revenue + self.discretionary_budget
        max_spend = affordability * 0.15
        return min(max_n, max(1, 1 + int(max_spend / fee))) if fee > 0 else 1

    def _plan_llm(self, ctx: dict) -> tuple:
        """
        LLM-driven portfolio planning.

        Returns: (portfolio dict, focus_deltas dict, orientation_delta float,
                  reasoning str, strategy_memo str)
        """
        from llm import llm_plan_provider

        round_num = self.public_state.current_round
        memory_depth = ctx.get("reasoning_memory_depth", 2)
        # Pass strategy memos (or truncated reasoning) from recent rounds
        recent_insights = []
        for e in self.private_state.recent_insights[-memory_depth:]:
            recent_insights.append({
                "round": e["round"],
                "strategy_memo": e.get("strategy_memo", ""),
                "reasoning": e.get("reasoning", ""),
            })

        # Build per-benchmark score deltas for prompt
        score_deltas = {}
        for bm, history in self.public_state.benchmark_scores.items():
            if len(history) >= 2:
                score_deltas[bm] = history[-1][1] - history[-2][1]
            elif len(history) == 1:
                score_deltas[bm] = 0.0

        # Get current market share for confidence qualifier on satisfaction signal
        market_share = ctx.get("market_share", 0.0)
        orientation_adjustable = ctx.get("benchmark_orientation_mode") == "adjustable"
        consumer_signal_in_prompt = ctx.get("consumer_signal_in_prompt", True)
        orientation_prompt_style = ctx.get("orientation_prompt_style", "original")

        # Build market share history from memory for trend/churn display
        market_share_history = [
            e.get("market_share") for e in self.memory
            if e.get("type") == "observation" and e.get("market_share") is not None
        ]
        if market_share is not None:
            market_share_history.append(market_share)

        result = llm_plan_provider(
            name=self.name,
            strategy_profile=self.private_state.strategy_profile,
            innate_traits=self.private_state.innate_traits,
            round_num=round_num,
            portfolio=self.private_state.portfolio,
            focus_level=self.private_state.focus_level,
            inferred_benchmark_weights=self.private_state.inferred_benchmark_weights,
            benchmark_scores=self.public_state.benchmark_scores,
            score_deltas=score_deltas,
            competitor_scores={
                comp: hist[-1][1] if hist else 0.0
                for comp, hist in self.private_state.observed_competitor_scores.items()
            },
            consumer_signal=self.private_state.consumer_signal,
            benchmark_orientation=self.private_state.benchmark_orientation,
            market_share=market_share,
            orientation_adjustable=orientation_adjustable,
            recent_insights=recent_insights,
            own_incidents=ctx.get("own_incidents", []),
            regulatory_actions=ctx.get("regulatory_actions", []),
            verbose=self.verbose_llm,
            consumer_signal_in_prompt=consumer_signal_in_prompt,
            orientation_prompt_style=orientation_prompt_style,
            market_share_history=market_share_history,
        )

        # Detect fallback
        reasoning = result.get("reasoning", "")
        strategy_memo = result.get("strategy_memo", "")
        is_fallback = "fallback" in reasoning.lower()
        if is_fallback:
            self._llm_fallback_count += 1
            if self.llm_strict_mode:
                raise RuntimeError(
                    f"LLM fallback for {self.name} round {round_num} "
                    f"(#{self._llm_fallback_count})"
                )
        else:
            self._llm_fallback_count = 0

        # Parse ordinal portfolio signals -> absolute fractions
        portfolio = self._apply_portfolio_ordinals(result.get("portfolio", {}))
        focus_deltas = result.get("benchmark_focus", {})

        # Orientation only adjustable when config says so
        orientation_delta = 0.0
        if orientation_adjustable:
            orientation_signal = result.get("benchmark_orientation", "same")
            orientation_delta = _ordinal_to_delta(orientation_signal)

        # Evaluator submissions (eval_as_company): integer 1-N from LLM
        n_subs = result.get("n_submissions")
        if n_subs is not None:
            try:
                n_subs = max(1, min(int(n_subs), 10))
            except (ValueError, TypeError):
                n_subs = self._last_n_submissions
            self._last_n_submissions = n_subs

        return portfolio, focus_deltas, orientation_delta, reasoning, strategy_memo

    def _apply_portfolio_ordinals(self, signals: dict) -> dict:
        """
        Apply 5-level ordinal signals to current portfolio fractions.

        much_more/more/same/less/much_less mapped to +LARGE/+DELTA/0/-DELTA/-LARGE.
        Result is clipped per lever and renormalized.
        """
        p = dict(self.private_state.portfolio)
        for lever in ("rd", "safety", "product"):
            sig = signals.get(lever, "same")
            p[lever] = p.get(lever, 0.33) + _ordinal_to_delta(sig)

        # Clip
        safety_floor = 0.10 if self.open_source else 0.15
        p["rd"]      = max(0.10, min(0.75, p.get("rd", 0.55)))
        p["safety"]  = max(safety_floor, min(0.55, p.get("safety", 0.25)))
        p["product"] = max(0.05, min(0.50, p.get("product", 0.20)))

        total = sum(p.values())
        return {k: v / total for k, v in p.items()}

    def _apply_ordinal_deltas(self, focus_deltas: dict, orientation_delta: float):
        """
        Apply ordinal {more/less/same} signals to focus_level and benchmark_orientation.
        """
        # focus_level: additive delta, clip to [0.1, 5.0]
        for bm, signal in focus_deltas.items():
            if bm in self.private_state.focus_level:
                delta = _ordinal_to_delta(signal)
                self.private_state.focus_level[bm] = max(
                    0.1, min(5.0, self.private_state.focus_level[bm] + delta)
                )

        # benchmark_orientation: additive delta, clip to [0.05, 0.95]
        self.private_state.benchmark_orientation = max(
            BENCHMARK_ORIENTATION_MIN,
            min(BENCHMARK_ORIENTATION_MAX,
                self.private_state.benchmark_orientation + orientation_delta)
        )

    # ──────────────────────────────────────────────────────────────────────
    # Execute (capability update — called by simulation with ground truth)
    # ──────────────────────────────────────────────────────────────────────

    def compute_capability_gains(self, rd_budget: float,
                                 current_safety: float = 0.0,
                                 round_num: int = 0,
                                 rng=None,
                                 product_budget: float = 0.0,
                                 is_open_source: bool = False,
                                 enable_consumer_signal_fidelity: bool = True) -> dict:
        """
        Compute per-dimension capability gains for this round.

        Called by the simulation, which then applies the gains to the
        capability_vector it holds externally.

        Formula (per stakeholders.md):
            focus_weights[b]      = normalize(focus_level[b] for b in active_benchmarks)
            benchmark_driven[dim] = sum(focus_weights[b] * inferred_benchmark_weights[b][dim])
            quality               = _consumer_signal_fidelity(product_budget, is_open_source)
            effective_signal[dim] = quality * true_signal[dim] + (1-quality) * uniform[dim]
            target[dim]           = bo * benchmark_driven[dim] + (1-bo) * effective_signal[dim]
            gain[dim]             = rd * target[dim]

        Safety lever mechanics:
            - Diminishing returns: gain scales by (1 - current_safety)
            - Stochastic efficiency: uniform(0.3, 0.9), mean 0.6
            - Execution inertia via rolling-averaged portfolio (not per-gain lag)

        Args:
            rd_budget: Total R&D budget this round (base_revenue + funder_allocations).
            current_safety: Provider's current safety capability (for diminishing returns).
            round_num: Current round number.
            rng: NumPy RNG for stochastic safety efficiency.
            product_budget: Absolute product budget (for signal quality gating).
            is_open_source: Whether this provider is open-source (quality ceiling).
            enable_consumer_signal_fidelity: If False, skip quality gating (use raw signal).

        Returns:
            {dim: gain} dict (not yet applied — simulation applies it).
        """
        import numpy as _np

        # Use effective (rolling-averaged) portfolio for execution.
        # private_state.portfolio holds the TARGET; _effective_portfolio is the
        # organizationally-smoothed allocation that actually drives spending.
        p = self._effective_portfolio
        rd_fraction = p.get("rd", 0.55)
        safety_fraction = p.get("safety", 0.25)

        # focus_weights: normalize focus_level scalars across active benchmarks
        fl = self.private_state.focus_level
        fl_total = sum(fl.values()) if fl else 0.0

        if fl_total > 0:
            focus_weights = {bm: v / fl_total for bm, v in fl.items()}
        else:
            # No active benchmarks yet: uniform across known benchmarks or skip
            n = len(self.private_state.inferred_benchmark_weights)
            if n > 0:
                focus_weights = {
                    bm: 1.0 / n
                    for bm in self.private_state.inferred_benchmark_weights
                }
            else:
                # No benchmarks at all: uniform gain across dims
                uniform_gain = rd_fraction * rd_budget / len(DIMENSIONS)
                gains = {dim: uniform_gain for dim in DIMENSIONS}
                # Safety lever still goes through diminishing returns + stochastic efficiency
                gains["safety"] = gains.get("safety", 0.0) + self._compute_safety_gain(
                    safety_fraction * rd_budget, current_safety, rng)
                return gains

        # benchmark_driven[dim]
        benchmark_driven = {dim: 0.0 for dim in DIMENSIONS}
        for bm, fw in focus_weights.items():
            bm_weights = self.private_state.inferred_benchmark_weights.get(bm, {})
            for dim in DIMENSIONS:
                benchmark_driven[dim] += fw * bm_weights.get(dim, 1.0 / len(DIMENSIONS))

        # consumer signal with product-investment quality gating
        uniform_signal = {dim: 1.0 / len(DIMENSIONS) for dim in DIMENSIONS}
        sig = self.private_state.consumer_signal
        if sig:
            total_sig = sum(sig.values())
            true_signal = {dim: sig.get(dim, 0.0) / total_sig for dim in DIMENSIONS} if total_sig > 0 else dict(uniform_signal)
        else:
            true_signal = dict(uniform_signal)

        # Quality-gate: product investment determines how accurately
        # the R&D pipeline responds to consumer needs.
        if enable_consumer_signal_fidelity:
            quality = _consumer_signal_fidelity(product_budget, is_open_source)
        else:
            quality = 1.0  # ablation: raw signal, no gating
        self._last_consumer_signal_fidelity = quality

        sat_signal = {
            dim: quality * true_signal[dim] + (1.0 - quality) * uniform_signal[dim]
            for dim in DIMENSIONS
        }

        bo = self.private_state.benchmark_orientation
        gains = {}
        for dim in DIMENSIONS:
            target = bo * benchmark_driven.get(dim, 0.0) + (1.0 - bo) * sat_signal.get(dim, 0.0)
            gains[dim] = rd_fraction * rd_budget * target

        if self.safety_lever_through_target:
            # Ablation: safety allocation spreads across dimensions via target weights
            # (same as R&D pathway — no concentrated single-dimension stream)
            for dim in DIMENSIONS:
                target = bo * benchmark_driven.get(dim, 0.0) + (1.0 - bo) * sat_signal.get(dim, 0.0)
                gains[dim] += safety_fraction * rd_budget * target
        else:
            # Default: safety lever with diminishing returns + stochastic efficiency.
            # Execution delay is handled by the rolling average on portfolio allocations
            # (simulation.py), so no delivery lag here.
            gains["safety"] = gains.get("safety", 0.0) + self._compute_safety_gain(
                safety_fraction * rd_budget, current_safety, rng)

        return gains

    def _compute_safety_gain(self, raw_safety_budget: float,
                             current_safety: float,
                             rng=None) -> float:
        """Compute safety gain with diminishing returns + stochastic efficiency."""
        import numpy as _np
        if rng is None:
            rng = _np.random.default_rng()
        # Diminishing returns — harder to improve at higher levels
        diminishing = max(0.0, 1.0 - current_safety)
        # Stochastic efficiency — safety R&D is generally less efficient
        # than expected, with occasional good rounds. Mean 0.6.
        noise = rng.uniform(0.3, 0.9)
        return raw_safety_budget * diminishing * noise

    # ──────────────────────────────────────────────────────────────────────
    # Public communications
    # ──────────────────────────────────────────────────────────────────────

    def _sample_public_comms(self) -> Optional[dict]:
        """
        Sample a public communication type based on portfolio weights.

        Type weights:
            rd:      rd_fraction
            safety:  safety_fraction if safety_fraction > 0.20, else 0
            product: product_fraction if product_fraction > 0.15, else 0
            none:    0.30 (silence — always competes)

        In LLM mode, generates a one-liner via lightweight LLM call.
        In heuristic mode, uses templates.
        """
        import random

        p = self.private_state.portfolio
        safety_weight = p.get("safety", 0.0) if p.get("safety", 0.0) > 0.20 else 0.0
        safety_weight += self._safety_comms_boost
        raw = {
            "rd":      p.get("rd", 0.0),
            "safety":  safety_weight,
            "product": p.get("product", 0.0) if p.get("product", 0.0) > 0.15 else 0.0,
            "none":    0.30,
        }
        # Decay boost each round
        self._safety_comms_boost *= 0.70
        total = sum(raw.values())
        if total <= 0:
            return None

        weights = {k: v / total for k, v in raw.items()}
        post_type = random.choices(list(weights.keys()), weights=list(weights.values()), k=1)[0]

        if post_type == "none":
            return None

        templates = {
            "rd":      f"{self.name} publishes new research on capabilities",
            "safety":  f"{self.name} releases safety evaluation results",
            "product": f"{self.name} announces new enterprise deployment",
        }

        if self.llm_mode:
            try:
                from llm import llm_generate_public_comm
                content = llm_generate_public_comm(
                    provider_name=self.name,
                    comm_type=post_type,
                    strategy_profile=self.private_state.strategy_profile,
                    portfolio=p,
                )
                if content:
                    return {"type": post_type, "content": content}
            except Exception:
                pass  # fall through to template

        return {"type": post_type, "content": templates[post_type]}

    # ──────────────────────────────────────────────────────────────────────
    # Persistence
    # ──────────────────────────────────────────────────────────────────────

    def save(self, folder: str):
        """Save provider state to a folder."""
        os.makedirs(folder, exist_ok=True)

        with open(f"{folder}/public_state.json", "w") as f:
            json.dump(self.public_state.to_dict(), f, indent=2)

        with open(f"{folder}/private_state.json", "w") as f:
            json.dump(self.private_state.to_dict(), f, indent=2)

        with open(f"{folder}/memory.json", "w") as f:
            json.dump(self.memory, f, indent=2)

    @classmethod
    def load(cls, folder: str) -> "ModelProvider":
        """Load provider state from a folder."""
        with open(f"{folder}/public_state.json") as f:
            public = PublicState.from_dict(json.load(f))
        with open(f"{folder}/private_state.json") as f:
            private = ProviderPrivateState.from_dict(json.load(f))

        provider = cls(
            name=public.name,
            strategy_profile=private.strategy_profile,
            innate_traits=private.innate_traits,
            portfolio=private.portfolio,
            benchmark_orientation=private.benchmark_orientation,
        )
        provider.public_state = public
        provider.private_state = private

        mem_path = f"{folder}/memory.json"
        if os.path.exists(mem_path):
            with open(mem_path) as f:
                provider.memory = json.load(f)

        return provider

    def __repr__(self):
        p = self.private_state.portfolio
        return (f"ModelProvider(name='{self.name}', "
                f"market_share={self.public_state.market_share:.1%}, "
                f"portfolio=[R:{p.get('rd', 0):.0%}, "
                f"S:{p.get('safety', 0):.0%}, "
                f"P:{p.get('product', 0):.0%}])")
