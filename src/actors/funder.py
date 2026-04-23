"""
Funder Actor for Evaluation Ecosystem Simulation

Represents capital allocators (VCs, Corporates, Government/AISI, Foundations) who
influence provider development through funding decisions.

Key dynamics:
- Funders observe leaderboard, media sentiment, incidents, and market shares
- They infer provider quality from public signals (cannot see strategies directly)
- Funding affects providers via additive budget model (base_revenue + funder allocations)
- Different funder types have different scoring formulas and allocation patterns

Funder Types and Scoring Formulas (per stakeholders.md spec):
- VC: market_share_growth * media_sentiment * (1 - incident_risk) — concentrated bets, no OS
- Corporate: market_share * media_sentiment * (1 - incident_risk) — multi-relationship, 2-4 strategic partners
- Government/AISI: (1 - incident_rate) * market_share_growth — proportional spread, safety-first
- Foundation: (1 - incident_rate) * market_share_growth — proportional with underdog bonus

Visibility:
- PUBLIC: name, active investments (provider names only)
- PRIVATE: funder_type, beliefs, allocation history, mission
- INVISIBLE: true_roi, actual funding effectiveness
"""
import json
import os
from dataclasses import dataclass, field
from typing import Optional

from visibility import PublicState, FunderPrivateState, FunderGroundTruth


class Funder:
    """
    A Funder agent in the evaluation ecosystem simulation.

    Funders are capital allocators who:
    1. Observe ecosystem state (leaderboard, consumer satisfaction, regulatory interventions)
    2. Infer provider quality from public signals
    3. Allocate funding to providers based on their type and strategy
    4. Funding affects provider capability gains via efficiency multiplier

    This creates capital-side pressure: good performance and low gaming attracts funding,
    which creates advantages in capability development.

    Visibility Model:
    - public_state: Visible to all (name, funded providers)
    - private_state: Visible only to self (type, beliefs, allocations)
    - ground_truth: Held by simulation (true ROI, effectiveness)
    """

    def __init__(
        self,
        name: str,
        funder_type: str = "vc",
        total_capital: float = 1000000.0,
        risk_tolerance: float = 0.5,
        mission_statement: str = "",
        llm_mode: bool = False,
        max_round_deployment: float = 0.10,
        funding_cooldown: int = 2,
        capital_growth_rate: float = 0.07,
        sim_total_rounds: int = 40,
    ):
        """
        Initialize a Funder.

        Args:
            name: Unique identifier for this funder
            funder_type: Type of funder ("vc", "corporate", "gov", "foundation")
            total_capital: Sim-wide capital integral (deployable across full sim window)
            risk_tolerance: How much risk is acceptable (0-1)
            mission_statement: Mission-driven objective (for foundation type)
            llm_mode: If True, use LLM for decision-making
            max_round_deployment: Fraction of active-this-round capital deployable per decision (default 10%)
            funding_cooldown: Rounds between new allocation decisions (default 2)
            capital_growth_rate: Geometric monthly growth of available capital (default 0.07 = 7%/mo).
                See docs/funder_calibration.md for empirical anchor.
            sim_total_rounds: Sim length for availability-curve normalization (default 40).
        """
        # Initialize public state
        self.public_state = PublicState(
            name=name,
            current_round=0,
            published_scores=[],  # Reused to track public funding announcements
        )

        # Initialize private state
        self.private_state = FunderPrivateState(
            funder_type=funder_type,
            mission_statement=mission_statement,
            total_capital=total_capital,
            deployed_capital=0.0,
            believed_provider_quality={},
            active_funding={},
            funding_history=[],
        )

        # Funder-specific parameters
        self.risk_tolerance = risk_tolerance
        self.llm_mode = llm_mode
        self.max_round_deployment = max_round_deployment
        self.funding_cooldown = funding_cooldown
        self.capital_growth_rate = capital_growth_rate
        self.sim_total_rounds = sim_total_rounds

        # Memory
        self.memory = []

        # Tracking for inference
        self._last_leaderboard: list = []
        self._last_consumer_data: dict = {}
        self._last_regulator_data: dict = {}
        self._previous_scores: dict = {}  # For computing score growth

        # Momentum tracking
        self._score_history: list[dict] = []  # [{provider: score}, ...] last N rounds
        self._previous_market_shares: dict = {}  # {provider: share} from prior round
        self._current_market_momentum: dict = {}

        # Media (updated each round from media_coverage)
        self._media_sentiment: float = 0.0
        self._media_coverage: Optional[dict] = None

        # Public comms from providers (updated each round)
        self._public_comms: list = []

        # Incident tracking (recent incidents per provider)
        self._recent_incident_counts: dict = {}

        # Regulator intervention tracking: [(round, type, target), ...] last 3 rounds
        self._recent_interventions: list = []

        # Open-source provider names (VCs do not fund these)
        self._open_source_providers: set = set()

        # Cooldown tracking
        self._last_funding_round: int = -2  # Ensures funding happens on round 0

    @property
    def name(self) -> str:
        return self.public_state.name

    @property
    def funder_type(self) -> str:
        return self.private_state.funder_type

    def observe(
        self,
        leaderboard: list,
        consumer_data: dict,
        regulator_data: dict,
        round_num: int,
        media_coverage: Optional[dict] = None,
        other_funder_allocations: Optional[dict] = None,
        incidents: Optional[list] = None,
        open_source_providers: Optional[set] = None,
        public_comms: Optional[list] = None,
    ):
        """
        Observe the current ecosystem state.

        Funders can only see public signals:
        - Leaderboard scores (performance)
        - Consumer satisfaction (true quality proxy)
        - Regulatory interventions (compliance/safety risk)
        - Media coverage (sentiment, risk signals)
        - Other funders' allocations (for portfolio diversification)
        - Public incidents (safety failures, security breaches)

        Args:
            leaderboard: List of (provider_name, score) tuples
            consumer_data: Dict with avg_satisfaction, provider_satisfaction, etc.
            regulator_data: Dict with interventions, active_regulations
            round_num: Current simulation round
            media_coverage: Optional media coverage dict
            other_funder_allocations: Dict of {funder_name: {provider: amount}}
            incidents: Optional list of AIIncident objects from this round
        """
        self.public_state.current_round = round_num

        # Store for inference
        self._last_leaderboard = leaderboard
        self._last_consumer_data = consumer_data
        self._last_regulator_data = regulator_data
        self._other_funder_allocations = other_funder_allocations or {}
        self._open_source_providers = open_source_providers or set()

        # Media: store full coverage dict for LLM mode; extract sentiment for heuristic
        self._media_coverage = media_coverage
        self._media_sentiment = 0.0  # raw sentiment [-1, +1]
        if media_coverage:
            self._media_sentiment = media_coverage.get("sentiment", 0.0)

        # Public comms from providers
        self._public_comms = public_comms or []

        # Update beliefs about provider quality from benchmark scores at face value
        # Per observation model: funders see scores directly, not validity-adjusted
        for provider_name, score in leaderboard:
            if provider_name not in self.private_state.believed_provider_quality:
                self.private_state.believed_provider_quality[provider_name] = score
            else:
                learning_rate = 0.3
                old_belief = self.private_state.believed_provider_quality[provider_name]
                self.private_state.believed_provider_quality[provider_name] = (
                    (1 - learning_rate) * old_belief + learning_rate * score
                )

        # Pruning window scales with funding_cooldown so longer-cadence funders
        # retain history spanning the gap between their decisions. Minimum 3
        # rounds so short-cadence funders keep their existing behavior.
        history_window = max(3, self.funding_cooldown)

        # Track regulator intervention history for prompt context.
        # Simulation aggregation stores the target under "provider"; older paths
        # may use "target_provider" (LLM output) or nested details — fall through all.
        current_interventions = regulator_data.get("interventions", []) if regulator_data else []
        for iv in current_interventions:
            itype = iv.get("type", "unknown")
            target = (
                iv.get("provider")
                or iv.get("target_provider")
                or (iv.get("details") or {}).get("target_provider")
            )
            self._recent_interventions.append((round_num, itype, target))
        self._recent_interventions = [
            (r, t, tgt) for (r, t, tgt) in self._recent_interventions
            if r >= round_num - history_window
        ]

        # Track incident history per provider
        if incidents:
            for incident in incidents:
                provider = incident.provider
                if provider not in self._recent_incident_counts:
                    self._recent_incident_counts[provider] = []
                self._recent_incident_counts[provider].append((round_num, incident.severity))

            # Prune old incidents
            for provider in list(self._recent_incident_counts.keys()):
                self._recent_incident_counts[provider] = [
                    (r, s) for r, s in self._recent_incident_counts[provider]
                    if r >= round_num - history_window
                ]
                if not self._recent_incident_counts[provider]:
                    del self._recent_incident_counts[provider]

        # Store previous scores for growth calculation
        self._previous_scores = {name: score for name, score in leaderboard}

        # Track score history for momentum (keep last 4 snapshots to compute 3-round deltas)
        current_scores = {name: score for name, score in leaderboard}
        self._score_history.append(current_scores)
        if len(self._score_history) > 4:
            self._score_history = self._score_history[-4:]

        # Track market share momentum
        market_shares = consumer_data.get("market_shares", {})
        self._current_market_momentum = {}
        for provider_name in [name for name, _ in leaderboard]:
            curr_share = market_shares.get(provider_name, 0)
            prev_share = self._previous_market_shares.get(provider_name, curr_share)
            self._current_market_momentum[provider_name] = curr_share - prev_share
        self._previous_market_shares = dict(market_shares)

        # Record observation
        self.memory.append({
            "type": "observation",
            "round": round_num,
            "leaderboard": leaderboard,
            "interventions": len(regulator_data.get("interventions", [])),
        })

    def reflect(self):
        """
        Reflect on observations and update beliefs about providers.

        Consider:
        - Provider performance trends
        - Score and market share momentum
        """
        self.memory.append({
            "type": "reflection",
            "round": self.public_state.current_round,
            "beliefs": dict(self.private_state.believed_provider_quality),
        })

    def plan(self) -> dict:
        """
        Decide funding allocations for the next round.

        Respects funding_cooldown: if fewer than `funding_cooldown` rounds
        have passed since last allocation, returns previous allocations.

        Returns:
            Dict mapping provider names to funding amounts
        """
        current_round = self.public_state.current_round
        if current_round - self._last_funding_round < self.funding_cooldown:
            # Reuse previous allocations (no new decision)
            return dict(self.private_state.active_funding)

        self._last_funding_round = current_round

        if self.llm_mode:
            return self._plan_llm()
        else:
            return self._plan_heuristic()

    def set_evaluator_as_company(self, enabled: bool):
        """Enable or disable evaluator-as-company allocation split."""
        self._evaluator_as_company = enabled

    def _availability(self, round_num: int) -> float:
        """
        Fraction of total_capital active for deployment at this round.

        Geometric growth normalized so availabilities sum to 1.0 over sim_total_rounds,
        modeling the empirical ecosystem capital ramp (~7%/mo compound, ~2.3x YoY).
        See docs/funder_calibration.md for data anchors.

        availability(r) = (1 + g)^r / Sum_{i=0}^{N-1} (1+g)^i
        """
        g = self.capital_growth_rate
        N = self.sim_total_rounds
        if N <= 0:
            return 1.0
        if g == 0:
            return 1.0 / N
        normalization = ((1 + g) ** N - 1) / g
        return ((1 + g) ** round_num) / normalization

    def _plan_heuristic(self) -> dict:
        """
        Heuristic funding decision based on funder type.

        Returns:
            Dict mapping provider names to funding amounts
            If evaluator_as_company is enabled, may include "__EVALUATOR__" key
        """
        if not self._last_leaderboard:
            return {}

        providers = [name for name, _ in self._last_leaderboard]
        allocations = {}

        availability = self._availability(self.public_state.current_round)
        available_capital = (
            self.private_state.total_capital
            * availability
            * self.max_round_deployment
        )

        # Split capital: providers + evaluator (if company mode enabled)
        evaluator_allocation = 0.0
        provider_capital = available_capital

        if hasattr(self, '_evaluator_as_company') and self._evaluator_as_company:
            # Type-specific splits
            if self.funder_type == "vc":
                evaluator_share = 0.05  # VCs invest minimally in infrastructure
            elif self.funder_type == "corporate":
                evaluator_share = 0.10  # Corporates invest modestly in eval infra
            elif self.funder_type == "gov":
                evaluator_share = 0.30  # Governments fund public goods
            elif self.funder_type == "foundation":
                evaluator_share = 0.20  # Foundations support ecosystem infrastructure
            else:
                evaluator_share = 0.10

            evaluator_allocation = available_capital * evaluator_share
            provider_capital = available_capital * (1 - evaluator_share)

        if self.funder_type == "vc":
            allocations = self._plan_vc(providers, provider_capital)
        elif self.funder_type == "corporate":
            allocations = self._plan_corporate(providers, provider_capital)
        elif self.funder_type == "gov":
            allocations = self._plan_gov(providers, provider_capital)
        elif self.funder_type == "foundation":
            allocations = self._plan_foundation(providers, provider_capital)
        else:
            # Default: spread evenly
            per_provider = provider_capital / len(providers)
            allocations = {p: per_provider for p in providers}

        # Add evaluator allocation if company mode enabled
        if evaluator_allocation > 0:
            allocations["__EVALUATOR__"] = evaluator_allocation

        # Build a short reasoning summary
        top_provider = max((k for k in allocations if k != "__EVALUATOR__"),
                          key=lambda k: allocations[k], default="none")
        top_amount = allocations.get(top_provider, 0) if top_provider != "none" else 0
        reason = (
            f"{self.funder_type} strategy: top allocation "
            f"${top_amount:,.0f} to {top_provider}"
        )
        if evaluator_allocation > 0:
            reason += f", ${evaluator_allocation:,.0f} to evaluator"

        self.memory.append({
            "type": "planning",
            "round": self.public_state.current_round,
            "funder_type": self.funder_type,
            "allocations": allocations,
            "reason": reason,
        })

        return allocations

    def _get_score_momentum(self, provider: str) -> float:
        """Average score delta over last 3 rounds for a provider."""
        if len(self._score_history) < 2:
            return 0.0
        deltas = []
        for i in range(1, len(self._score_history)):
            prev = self._score_history[i - 1].get(provider)
            curr = self._score_history[i].get(provider)
            if prev is not None and curr is not None:
                deltas.append(curr - prev)
        return sum(deltas) / len(deltas) if deltas else 0.0

    def _compute_portfolio_concentration(self, provider: str) -> float:
        """
        Compute how concentrated other funders are on this provider.

        Returns:
            Value 0-1 where 1 = highly concentrated (all funders funding it)
        """
        if not self._other_funder_allocations:
            return 0.0  # No concentration data available

        total_funders = len(self._other_funder_allocations)
        if total_funders == 0:
            return 0.0

        # Count how many other funders are funding this provider
        funders_funding_provider = 0
        for funder_name, allocations in self._other_funder_allocations.items():
            if provider in allocations and allocations[provider] > 0:
                funders_funding_provider += 1

        # Concentration = fraction of other funders funding this provider
        return funders_funding_provider / total_funders

    def _get_incident_risk(self, provider: str) -> float:
        """Compute incident risk score [0,1] from recent incidents.

        Severity-weighted sum of incidents in last 3 rounds, capped at 1.0.
        """
        if provider not in self._recent_incident_counts:
            return 0.0
        severity_weights = {"minor": 0.05, "moderate": 0.15, "major": 0.30, "critical": 0.50}
        total = sum(severity_weights.get(s, 0.10) for _, s in self._recent_incident_counts[provider])
        return min(1.0, total)

    def _get_media_sentiment_factor(self) -> float:
        """Convert raw media sentiment [-1,+1] to a multiplicative factor [0.5, 1.5].

        Neutral sentiment (0) maps to 1.0. Negative sentiment reduces score,
        positive sentiment boosts it. Used by VC and corporate scoring.
        """
        return 1.0 + self._media_sentiment * 0.5

    def _score_providers_vc(self, providers: list) -> dict:
        """VC scoring: growth * media * (1 - incident_risk) * (1 - market_share).

        VCs chase momentum and upside potential. The (1 - market_share) term
        models diminishing VC interest in mature positions — smaller providers
        have more upside, and VCs naturally exit as companies mature.
        """
        media_factor = self._get_media_sentiment_factor()
        scores = {}
        for provider in providers:
            market_growth = max(0.0, self._current_market_momentum.get(provider, 0))
            incident_risk = self._get_incident_risk(provider)
            market_share = self._previous_market_shares.get(provider, 0.1)
            upside = 1.0 - market_share
            concentration = self._compute_portfolio_concentration(provider)
            diversification = 1.0 + 0.3 * (1.0 - concentration)
            scores[provider] = max(0, market_growth * media_factor * (1 - incident_risk) * upside * diversification)
        return scores

    def _score_providers_corporate(self, providers: list) -> dict:
        """Corporate scoring: market_share * media_sentiment * (1 - incident_risk).

        Corporates anchor to current market position rather than growth.
        """
        market_shares = self._last_consumer_data.get("market_shares", {})
        media_factor = self._get_media_sentiment_factor()
        scores = {}
        for provider in providers:
            share = max(0.01, market_shares.get(provider, 0))
            incident_risk = self._get_incident_risk(provider)
            scores[provider] = max(0, share * media_factor * (1 - incident_risk))
        return scores

    def _score_providers_gov(self, providers: list) -> dict:
        """Gov scoring: (1 - incident_rate) * market_share_growth.

        Government funders prioritize safety track record and growth.
        """
        scores = {}
        for provider in providers:
            incident_risk = self._get_incident_risk(provider)
            market_growth = max(0.01, self._current_market_momentum.get(provider, 0) + 0.1)
            scores[provider] = max(0, (1 - incident_risk) * market_growth)
        return scores

    def _score_providers_foundation(self, providers: list) -> dict:
        """Foundation scoring: (1 - incident_rate) * market_share_growth.

        Same base formula as gov, but allocation logic differs (underdog bonus).
        """
        return self._score_providers_gov(providers)

    def _plan_vc(self, providers: list, capital: float) -> dict:
        """
        VC strategy: Concentrated bets on top 1-2 high-growth providers.

        Spec formula: market_share_growth * media_sentiment * (1 - incident_risk).
        Open-source providers excluded (no equity model).
        Funds at most 2 providers. Second pick must score at least 40% of the top.
        """
        providers = [p for p in providers if p not in self._open_source_providers]
        if not providers:
            return {}

        scores = self._score_providers_vc(providers)
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        top_score = ranked[0][1] if ranked else 0
        if top_score <= 0:
            return {}

        allocations = {}
        if len(ranked) >= 2 and ranked[1][1] >= top_score * 0.40:
            # Two-bet split: 70/30
            allocations[ranked[0][0]] = capital * 0.70
            allocations[ranked[1][0]] = capital * 0.30
        else:
            # Single concentrated bet
            allocations[ranked[0][0]] = capital

        return allocations

    def _plan_gov(self, providers: list, capital: float) -> dict:
        """
        Government/AISI strategy: Safety & stability, proportional spread.

        Spec formula: (1 - incident_rate) * market_share_growth.
        Penalizes providers with active regulatory interventions.
        Allocation: proportional to normalized scores; providers scoring
        below 10% of the top are excluded.
        """
        scores = self._score_providers_gov(providers)

        # Penalize providers with active regulatory interventions
        interventions = self._last_regulator_data.get("interventions", [])
        if interventions:
            for provider in providers:
                scores[provider] = max(0, scores.get(provider, 0) * 0.8)

        # Exclude providers scoring below 10% of the top score
        top_score = max(scores.values()) if scores else 0
        threshold = top_score * 0.10
        scores = {p: s for p, s in scores.items() if s >= threshold}

        # Normalize and allocate proportionally
        total_score = sum(scores.values())
        if total_score > 0:
            allocations = {p: (scores[p] / total_score) * capital for p in scores}
        else:
            allocations = {}

        return allocations

    def _plan_foundation(self, providers: list, capital: float) -> dict:
        """
        Foundation strategy: Ecosystem health, underdog support.

        Spec formula: (1 - incident_rate) * market_share_growth (same base as gov).
        Adds underdog bonus for lower-quality providers.
        Allocation: top 3 by adjusted score, proportional among those.
        """
        scores = self._score_providers_foundation(providers)

        # Underdog bonus: lower quality providers get a boost
        for provider in providers:
            quality = self.private_state.believed_provider_quality.get(provider, 0.5)
            scores[provider] = scores.get(provider, 0) + (1 - quality) * 0.15

        # Pick top 3 by adjusted score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
        selected_scores = {p: s for p, s in ranked if s > 0}

        # Normalize and allocate proportionally among selected
        total_score = sum(selected_scores.values())
        if total_score > 0:
            allocations = {p: (s / total_score) * capital for p, s in selected_scores.items()}
        else:
            allocations = {}

        return allocations

    def _plan_corporate(self, providers: list, capital: float) -> dict:
        """
        Corporate strategy: Strategic multi-relationship, anchored to market position.

        Spec formula: market_share * media_sentiment * (1 - incident_risk).
        Can fund OS providers. Picks top 2-4 strategic partners each decision round.
        """
        scores = self._score_providers_corporate(providers)

        # Pick top 2-4 by score (strategic partnerships, not spray)
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        max_partners = min(4, len(ranked))
        selected = {p: s for p, s in ranked[:max_partners] if s > 0}

        # Normalize and allocate proportionally among selected
        total_score = sum(selected.values())
        if total_score > 0:
            allocations = {p: (s / total_score) * capital for p, s in selected.items()}
        else:
            allocations = {}

        return allocations

    def _plan_llm(self) -> dict:
        """LLM-driven funding decision."""
        try:
            from llm import llm_plan_funding
            round_num = self.public_state.current_round
            availability = self._availability(round_num)
            capped_capital = (
                self.private_state.total_capital
                * availability
                * self.max_round_deployment
            )

            # Compute score deltas from history — last-round and 2-round
            score_deltas = {}
            score_deltas_2round = {}
            if len(self._score_history) >= 2:
                prev = self._score_history[-2]
                curr = self._score_history[-1]
                for p in curr:
                    if p in prev:
                        score_deltas[p] = curr[p] - prev[p]
            if len(self._score_history) >= 3:
                earlier = self._score_history[-3]
                curr = self._score_history[-1]
                for p in curr:
                    if p in earlier:
                        score_deltas_2round[p] = curr[p] - earlier[p]

            # Extract media headlines only (no sentiment label — coaching removed)
            media_headlines = None
            if self._media_coverage:
                media_headlines = self._media_coverage.get("headlines")

            # Peer funder allocations — {provider: [(funder_name, amount), ...]}
            # sorted by amount desc, excluding self, excluding zero allocations.
            peer_funder_allocations: dict = {}
            for other_name, other_allocs in self._other_funder_allocations.items():
                if other_name == self.name:
                    continue
                for provider, amount in other_allocs.items():
                    if provider == "__EVALUATOR__" or amount <= 0:
                        continue
                    peer_funder_allocations.setdefault(provider, []).append(
                        (other_name, amount)
                    )
            for provider in peer_funder_allocations:
                peer_funder_allocations[provider].sort(
                    key=lambda t: t[1], reverse=True
                )
            peer_funder_allocations = peer_funder_allocations or None

            # Regulator context
            regulator_interventions = (
                self._recent_interventions if self._recent_interventions else None
            )
            active_regulations = self._last_regulator_data.get("active_regulations") or None

            # Own cumulative allocations by provider, with last-round info
            cumulative_allocations: dict = {}
            for hist_round, hist_allocs in self.private_state.funding_history:
                for provider, amount in hist_allocs.items():
                    if provider == "__EVALUATOR__":
                        continue
                    if provider not in cumulative_allocations:
                        cumulative_allocations[provider] = {
                            "total": 0.0, "last_amount": 0.0, "last_round": None
                        }
                    cumulative_allocations[provider]["total"] += amount
                    if amount > 0:
                        cumulative_allocations[provider]["last_amount"] = amount
                        cumulative_allocations[provider]["last_round"] = hist_round
            cumulative_allocations = cumulative_allocations or None

            allocations, reasoning = llm_plan_funding(
                name=self.name,
                funder_type=self.funder_type,
                total_capital=capped_capital,
                leaderboard=self._last_leaderboard,
                market_shares=self._last_consumer_data.get("market_shares", {}),
                recent_insights=self.private_state.recent_reasoning[-2:],
                incidents=self._recent_incident_counts if self._recent_incident_counts else None,
                media_headlines=media_headlines,
                score_deltas=score_deltas if score_deltas else None,
                score_deltas_2round=score_deltas_2round if score_deltas_2round else None,
                public_comms=self._public_comms if self._public_comms else None,
                peer_funder_allocations=peer_funder_allocations,
                regulator_interventions=regulator_interventions,
                active_regulations=active_regulations,
                cumulative_allocations=cumulative_allocations,
                mission_statement=self.private_state.mission_statement,
                verbose=False,
            )

            # Store reasoning for cross-round persistence
            if reasoning:
                self.private_state.recent_reasoning.append({"round": round_num, "reasoning": reasoning})
                self.private_state.recent_reasoning = self.private_state.recent_reasoning[-3:]

            # VCs cannot fund open-source providers (no equity model) — enforce same rule as heuristic
            if self.funder_type == "vc" and self._open_source_providers:
                allocations = {p: v for p, v in allocations.items() if p not in self._open_source_providers}

            self.memory.append({
                "type": "planning_llm",
                "round": round_num,
                "reasoning": reasoning,
                "allocations": allocations,
            })

            return allocations
        except Exception as e:
            # Fallback to heuristic
            print(f"LLM planning failed: {e}, falling back to heuristic")
            return self._plan_heuristic()

    def execute(self, allocations: Optional[dict] = None):
        """
        Execute funding allocations.

        Args:
            allocations: Funding allocations (uses plan() result if None)
        """
        if allocations is None:
            allocations = self.plan()

        # Update active funding
        self.private_state.active_funding = allocations

        # Track deployed capital
        self.private_state.deployed_capital = sum(allocations.values())

        # Record in history
        self.private_state.funding_history.append(
            (self.public_state.current_round, dict(allocations))
        )

        # Public announcement (store in published_scores for simplicity)
        funded_providers = list(allocations.keys())
        if funded_providers:
            announcement = f"Round {self.public_state.current_round}: Funded {', '.join(funded_providers)}"
            self.public_state.published_scores.append(
                (self.public_state.current_round, announcement)
            )

        self.memory.append({
            "type": "execution",
            "round": self.public_state.current_round,
            "allocations": allocations,
            "total_deployed": self.private_state.deployed_capital,
        })

    def get_funding_multiplier(self, provider_name: str) -> float:
        """
        Get the funding multiplier for a provider.

        Multiplier ranges from 1.0 (no funding) to 2.0 (max funding).
        Based on the proportion of total capital allocated to the provider.

        Args:
            provider_name: Name of the provider

        Returns:
            Funding multiplier (1.0 - 2.0)
        """
        if not self.private_state.active_funding:
            return 1.0

        funding = self.private_state.active_funding.get(provider_name, 0)
        if funding <= 0:
            return 1.0

        # Multiplier based on funding proportion
        # Max funding (100% of capital) = 2.0x multiplier
        # No funding = 1.0x multiplier
        proportion = funding / self.private_state.total_capital
        multiplier = 1.0 + proportion

        # Cap at 2.0
        return min(2.0, multiplier)

    def get_prompt_context(self) -> str:
        """
        Get context for LLM prompts.

        Returns only public + private state, never ground truth.
        """
        context = "=== FUNDER STATE ===\n"
        context += f"Name: {self.name}\n"
        context += f"Type: {self.funder_type}\n"
        context += f"Mission: {self.private_state.mission_statement or 'N/A'}\n"
        context += f"Total Capital: ${self.private_state.total_capital:,.0f}\n"
        context += f"Deployed: ${self.private_state.deployed_capital:,.0f}\n"
        context += "\n"

        if self.private_state.believed_provider_quality:
            context += "Provider Assessments (benchmark scores at face value):\n"
            for name, quality in sorted(
                self.private_state.believed_provider_quality.items(),
                key=lambda x: x[1],
                reverse=True
            ):
                context += f"  {name}: score={quality:.2f}\n"

        if self.private_state.active_funding:
            context += "\nCurrent Funding:\n"
            for name, amount in self.private_state.active_funding.items():
                context += f"  {name}: ${amount:,.0f}\n"

        return context

    def save(self, folder: str):
        """Save funder state to a folder."""
        os.makedirs(folder, exist_ok=True)

        with open(f"{folder}/public_state.json", "w") as f:
            json.dump(self.public_state.to_dict(), f, indent=2)

        with open(f"{folder}/private_state.json", "w") as f:
            json.dump(self.private_state.to_dict(), f, indent=2)

        with open(f"{folder}/memory.json", "w") as f:
            json.dump(self.memory, f, indent=2)

        # Save parameters
        with open(f"{folder}/params.json", "w") as f:
            json.dump({
                "risk_tolerance": self.risk_tolerance,
                "llm_mode": self.llm_mode,
                "max_round_deployment": self.max_round_deployment,
                "funding_cooldown": self.funding_cooldown,
                "capital_growth_rate": self.capital_growth_rate,
                "sim_total_rounds": self.sim_total_rounds,
            }, f, indent=2)

    @classmethod
    def load(cls, folder: str) -> "Funder":
        """Load funder state from a folder."""
        with open(f"{folder}/params.json", "r") as f:
            params = json.load(f)

        with open(f"{folder}/public_state.json", "r") as f:
            public_data = json.load(f)

        with open(f"{folder}/private_state.json", "r") as f:
            private_data = json.load(f)

        funder = cls(
            name=public_data["name"],
            funder_type=private_data.get("funder_type", "vc"),
            total_capital=private_data.get("total_capital", 1000000.0),
            mission_statement=private_data.get("mission_statement", ""),
            risk_tolerance=params.get("risk_tolerance", 0.5),
            llm_mode=params.get("llm_mode", False),
            max_round_deployment=params.get("max_round_deployment", 0.10),
            funding_cooldown=params.get("funding_cooldown", 2),
            capital_growth_rate=params.get("capital_growth_rate", 0.07),
            sim_total_rounds=params.get("sim_total_rounds", 40),
        )

        funder.public_state = PublicState.from_dict(public_data)
        funder.private_state = FunderPrivateState.from_dict(private_data)

        with open(f"{folder}/memory.json", "r") as f:
            funder.memory = json.load(f)

        return funder

    def __repr__(self):
        return (
            f"Funder(name='{self.name}', "
            f"type='{self.funder_type}', "
            f"deployed=${self.private_state.deployed_capital:,.0f})"
        )


def get_default_funder_configs() -> list[dict]:
    """
    Get default funder configuration (1 VC funder).

    Returns:
        List with single VC funder config
    """
    return [
        {
            "name": "TechVentures",
            "funder_type": "vc",
            "total_capital": 1000000.0,
            "risk_tolerance": 0.7,
            "mission_statement": "Maximize returns by backing AI market leaders",
        },
    ]


def get_multi_funder_configs() -> list[dict]:
    """
    Get multi-funder configuration with all four types.

    Returns:
        List with VC, Corporate, Government, and Foundation funder configs
    """
    return [
        {
            "name": "TechVentures",
            "funder_type": "vc",
            "total_capital": 1000000.0,
            "risk_tolerance": 0.7,
            "mission_statement": "Maximize returns by backing AI market leaders",
        },
        {
            "name": "CloudPartners",
            "funder_type": "corporate",
            "total_capital": 800000.0,
            "risk_tolerance": 0.5,
            "mission_statement": "Strategic partnerships anchored to market position",
        },
        {
            "name": "AISI_Fund",
            "funder_type": "gov",
            "total_capital": 500000.0,
            "risk_tolerance": 0.3,
            "mission_statement": "Ensure safe and responsible AI development",
        },
        {
            "name": "OpenResearch",
            "funder_type": "foundation",
            "total_capital": 300000.0,
            "risk_tolerance": 0.5,
            "mission_statement": "Support authentic capability advancement for societal benefit",
        },
    ]
