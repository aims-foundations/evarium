"""
Visibility System for Evaluation Ecosystem Simulation

Implements three-tier visibility model:
- PUBLIC: Visible to all actors and logger
- PRIVATE: Visible only to self and logger
- INVISIBLE (GroundTruth): Only visible to simulation/logger, never to actors

Key Design Principle: Invisible state doesn't live inside the actor.
The simulation holds ground truth externally, making it structurally
impossible for LLM prompts to access it.

Audit (2026-03-31):
- FIXED: safety_capability (GT field) was leaking into consumer LLM prompts via
  provider_strategies dict. Now consumer.py uses only portfolio "safety" fraction.
- FIXED: ground_truth dict was passed through compute_switching / _compute_switching_llm /
  _build_decision_context in consumer.py but never used. Removed from all signatures.
- FIXED: provider_strategies was passed to regulator.observe() but never read. Removed.
- ADDED: MediaGroundTruth dataclass (was missing; media.py docstring declared GT fields
  true_influence and accuracy but no dataclass existed).
- VERIFIED: No other GT fields leak into actor observations or LLM prompts.
- NOTE: MarketSegment.need_weights is GT-equivalent (defines hidden utility function)
  but is only used in compute_satisfaction (simulation-internal). Not surfaced to actors.
- NOTE: ProviderGroundTruth.market_share redundancy with PublicState.market_share is
  intentional — GT is authoritative, public is the announced value.
"""
import json
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AIIncident:
    """
    A single AI safety incident.

    Represents real-world AI failures (healthcare harm, security breaches,
    bias incidents, safety failures) that cascade through the ecosystem.
    """
    provider: str
    round_num: int
    category: str  # "healthcare_harm", "security_breach", "bias_discrimination", "safety_failure", "misinformation", "misuse"
    severity: str  # "minor", "moderate", "major", "critical"
    description: str  # Generated headline
    affected_sectors: list  # ["hospital_system", "enterprise_finance", etc.]

    # Computed at generation time
    safety_investment_at_time: float = 0.0
    market_share_at_time: float = 0.0

    def to_dict(self) -> dict:
        """Convert to dict for serialization."""
        return {
            "provider": self.provider,
            "round_num": self.round_num,
            "category": self.category,
            "severity": self.severity,
            "description": self.description,
            "affected_sectors": self.affected_sectors,
            "safety_investment_at_time": self.safety_investment_at_time,
            "market_share_at_time": self.market_share_at_time,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AIIncident":
        """Create from dict (forward/backward compatible)."""
        known = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in data.items() if k in known})


@dataclass
class PublicState:
    """
    State visible to all actors.

    This information can be freely shared in prompts and accessed by any actor.
    """
    name: str = ""
    current_round: int = 0

    # Per-benchmark score histories: {benchmark_name: [(round, overall_score), ...]}
    benchmark_scores: dict = field(default_factory=dict)

    # Current market share (updated each round by simulation)
    market_share: float = 0.0

    # Recent public communications: [{"round": int, "type": str, "content": str}, ...]
    public_comms: list = field(default_factory=list)

    # Legacy: flat score list for backward compatibility
    published_scores: list = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dict for serialization."""
        return {
            "name": self.name,
            "current_round": self.current_round,
            "benchmark_scores": self.benchmark_scores,
            "market_share": self.market_share,
            "public_comms": self.public_comms,
            "published_scores": self.published_scores,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PublicState":
        """Create from dict (forward/backward compatible)."""
        known = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in data.items() if k in known})

    def get_summary(self) -> str:
        """Get human-readable summary for prompts."""
        summary = f"Name: {self.name}\n"
        summary += f"Current Round: {self.current_round}\n"
        summary += f"Market Share: {self.market_share:.1%}\n"
        if self.benchmark_scores:
            summary += "Recent Benchmark Scores:\n"
            for bm_name, history in self.benchmark_scores.items():
                if history:
                    last_round, last_score = history[-1]
                    delta_str = ""
                    if len(history) >= 2:
                        delta = last_score - history[-2][1]
                        delta_str = f" ({delta:+.3f})"
                    summary += f"  {bm_name}: {last_score:.3f}{delta_str}\n"
        else:
            summary += "No benchmark scores yet.\n"
        return summary


@dataclass
class ProviderPrivateState:
    """
    Private state for Model Provider actors.

    Only accessible to the owning actor and the logger.
    Competitors cannot see this state.
    """
    # Identity
    strategy_profile: str = ""
    innate_traits: str = ""

    # Investment portfolio: rd + safety + product = 1.0
    portfolio: dict = field(default_factory=lambda: {"rd": 0.55, "safety": 0.25, "product": 0.20})

    # Per-benchmark focus scalar (running value; ordinal LLM-updated each round).
    # {benchmark_name: float}  — not normalized; relative values drive capability targeting.
    # Initialized at mean of existing benchmarks when a new benchmark is introduced.
    focus_level: dict = field(default_factory=dict)

    # Per-benchmark inferred dimension weights (heuristic-updated from score prediction errors).
    # {benchmark_name: {dim: float, ...}}  — each inner dict is normalized.
    # Initialized to uniform across 6 dimensions when benchmark is first seen.
    inferred_benchmark_weights: dict = field(default_factory=dict)

    # How much R&D targets benchmark-weighted dimensions vs consumer satisfaction signal.
    # [0.05, 0.95]; ordinal LLM-updated. Higher = more benchmark-oriented.
    benchmark_orientation: float = 0.80

    # Market-share-weighted consumer need signal (6-dim, normalized).
    # Updated each round by simulation; not passed to LLM prompts directly.
    consumer_signal: dict = field(default_factory=dict)

    # Competitor capability beliefs (inferred from observed scores)
    believed_competitor_capabilities: dict = field(default_factory=dict)

    # History tracking
    past_strategies: list = field(default_factory=list)  # [{round, rd, safety, product}, ...]
    observed_competitor_scores: dict = field(default_factory=dict)  # {name: [(round, score), ...]}

    # Cross-round reasoning memory (PIMMUR)
    # [{round: int, type: str, reasoning: str}, ...]
    recent_insights: list = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dict for serialization."""
        return {
            "strategy_profile": self.strategy_profile,
            "innate_traits": self.innate_traits,
            "portfolio": self.portfolio,
            "focus_level": self.focus_level,
            "inferred_benchmark_weights": self.inferred_benchmark_weights,
            "benchmark_orientation": self.benchmark_orientation,
            "consumer_signal": self.consumer_signal,
            "believed_competitor_capabilities": self.believed_competitor_capabilities,
            "past_strategies": self.past_strategies,
            "observed_competitor_scores": self.observed_competitor_scores,
            "recent_insights": self.recent_insights,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ProviderPrivateState":
        """Create from dict (forward/backward compatible)."""
        known = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in data.items() if k in known})

    def get_summary(self) -> str:
        """Get human-readable summary for prompts."""
        summary = f"Strategy Profile: {self.strategy_profile}\n"
        summary += f"Core Traits: {self.innate_traits}\n"
        p = self.portfolio
        summary += (f"Current Portfolio: R&D={p.get('rd', 0):.0%}, "
                    f"Safety={p.get('safety', 0):.0%}, "
                    f"Product={p.get('product', 0):.0%}\n")
        summary += f"Benchmark Orientation: {self.benchmark_orientation:.2f}\n"

        if self.focus_level:
            summary += "Benchmark Focus Levels:\n"
            for bm, lvl in self.focus_level.items():
                summary += f"  {bm}: {lvl:.3f}\n"

        if self.consumer_signal:
            summary += "Consumer Satisfaction Signal:\n"
            for dim, val in self.consumer_signal.items():
                summary += f"  {dim}: {val:.3f}\n"

        if self.believed_competitor_capabilities:
            summary += "Competitor Capability Beliefs:\n"
            for name, cap in self.believed_competitor_capabilities.items():
                summary += f"  {name}: {cap:.3f}\n"

        return summary

    def get_history_summary(self, n_recent: int = 5) -> str:
        """Get recent strategy history for prompts."""
        summary = "Recent Investment History:\n"
        if self.past_strategies:
            recent = self.past_strategies[-n_recent:]
            summary += "| Round | R&D | Safety | Product |\n"
            summary += "|-------|-----|--------|----------|\n"
            for entry in recent:
                if isinstance(entry, dict):
                    summary += (f"| {entry.get('round', '?')} "
                                f"| {entry.get('rd', 0):.0%} "
                                f"| {entry.get('safety', 0):.0%} "
                                f"| {entry.get('product', 0):.0%} |\n")
        else:
            summary += "  No history yet.\n"
        return summary


@dataclass
class ProviderGroundTruth:
    """
    Ground truth for Model Provider actors.

    INVISIBLE - Only accessible to simulation and logger.
    This data is NEVER passed to actors or included in LLM prompts.
    """
    # Per-dimension capability scores, 0–1
    capability_vector: dict = field(default_factory=lambda: {
        "reasoning": 0.5, "coding": 0.5, "knowledge": 0.5,
        "safety": 0.5, "communication": 0.5, "agentic": 0.5,
    })
    safety_incidents_caused: int = 0
    market_share: float = 0.0

    def to_dict(self) -> dict:
        """Convert to dict for serialization."""
        return {
            "capability_vector": self.capability_vector,
            "safety_incidents_caused": self.safety_incidents_caused,
            "market_share": self.market_share,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ProviderGroundTruth":
        """Create from dict (forward/backward compatible)."""
        known = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in data.items() if k in known})


@dataclass
class BenchmarkGroundTruth:
    """
    Ground truth for a Benchmark.

    INVISIBLE - Only accessible to simulation and logger.
    Defines how the evaluator converts capability vectors into scores.
    Providers never see the true dimension weights — they infer them
    from score prediction errors via inferred_benchmark_weights.
    """
    # Hidden per-category dimension loadings:
    # {category_name: {dim: weight, ...}}  — each inner dict normalized
    category_dimension_weights: dict = field(default_factory=dict)
    noise_sigma: float = 0.02
    samples: int = 1000

    def to_dict(self) -> dict:
        """Convert to dict for serialization."""
        return {
            "category_dimension_weights": self.category_dimension_weights,
            "noise_sigma": self.noise_sigma,
            "samples": self.samples,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "BenchmarkGroundTruth":
        """Create from dict."""
        known = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in data.items() if k in known})


# ──────────────────────────────────────────────────────────────────────────────
# Consumer, Regulator, Funder, Evaluator state classes
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class ConsumerPrivateState:
    """
    Private state for Consumer actors.

    Only accessible to the owning consumer and the logger.
    """
    use_cases: list = field(default_factory=list)
    budget: float = 100.0
    current_subscription: Optional[str] = None
    believed_model_quality: dict = field(default_factory=dict)
    satisfaction_history: list = field(default_factory=list)
    subscription_history: list = field(default_factory=list)
    switching_cost: float = 0.1
    leaderboard_trust: float = 0.7
    rounds_with_provider: int = 0

    def to_dict(self) -> dict:
        return {
            "use_cases": self.use_cases,
            "budget": self.budget,
            "current_subscription": self.current_subscription,
            "believed_model_quality": self.believed_model_quality,
            "satisfaction_history": self.satisfaction_history,
            "subscription_history": self.subscription_history,
            "switching_cost": self.switching_cost,
            "leaderboard_trust": self.leaderboard_trust,
            "rounds_with_provider": self.rounds_with_provider,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ConsumerPrivateState":
        known = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in data.items() if k in known})

    def get_summary(self) -> str:
        summary = f"Use Cases: {', '.join(self.use_cases) if self.use_cases else 'General'}\n"
        summary += f"Budget: ${self.budget:.0f}/month\n"
        summary += f"Current Subscription: {self.current_subscription or 'None'}\n"
        summary += f"Leaderboard Trust: {self.leaderboard_trust:.2f}\n"
        summary += f"Switching Cost: {self.switching_cost:.2f}\n"
        summary += f"Rounds with Current Provider: {self.rounds_with_provider}\n"
        if self.believed_model_quality:
            summary += "Model Quality Beliefs:\n"
            for name, quality in self.believed_model_quality.items():
                summary += f"  {name}: {quality:.2f}\n"
        if self.satisfaction_history:
            recent = self.satisfaction_history[-3:]
            summary += "Recent Experience:\n"
            for round_num, provider, satisfaction in recent:
                summary += f"  Round {round_num} ({provider}): {satisfaction:.2f} satisfaction\n"
        return summary


@dataclass
class RegulatorPrivateState:
    """
    Private state for Regulator actors.

    Only accessible to the owning actor and the logger.
    """
    policy_objectives: list = field(default_factory=list)
    risk_beliefs: dict = field(default_factory=dict)
    industry_trust: float = 0.5
    regulatory_capacity: float = 1.0
    past_interventions: list = field(default_factory=list)
    observed_incidents: list = field(default_factory=list)
    recent_reasoning: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "policy_objectives": self.policy_objectives,
            "risk_beliefs": self.risk_beliefs,
            "industry_trust": self.industry_trust,
            "regulatory_capacity": self.regulatory_capacity,
            "past_interventions": self.past_interventions,
            "observed_incidents": self.observed_incidents,
            "recent_reasoning": self.recent_reasoning,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "RegulatorPrivateState":
        known = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in data.items() if k in known})

    def get_summary(self) -> str:
        summary = f"Policy Objectives: {', '.join(self.policy_objectives) if self.policy_objectives else 'General oversight'}\n"
        summary += f"Industry Trust Level: {self.industry_trust:.2f}\n"
        summary += f"Regulatory Capacity: {self.regulatory_capacity:.2f}\n"
        if self.risk_beliefs:
            summary += "Risk Assessments:\n"
            for risk, belief in self.risk_beliefs.items():
                summary += f"  {risk}: {belief:.2f}\n"
        if self.past_interventions:
            recent = self.past_interventions[-3:]
            summary += "Recent Interventions:\n"
            for round_num, intervention_type, details in recent:
                summary += f"  Round {round_num}: {intervention_type} - {details}\n"
        return summary


@dataclass
class FunderPrivateState:
    """
    Private state for Funder actors.

    Only accessible to the owning funder and the logger.
    """
    funder_type: str = "vc"  # "vc", "corporate", "gov", "foundation"
    mission_statement: str = ""
    total_capital: float = 1000000.0
    deployed_capital: float = 0.0
    believed_provider_quality: dict = field(default_factory=dict)
    active_funding: dict = field(default_factory=dict)
    funding_history: list = field(default_factory=list)
    recent_reasoning: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "funder_type": self.funder_type,
            "mission_statement": self.mission_statement,
            "total_capital": self.total_capital,
            "deployed_capital": self.deployed_capital,
            "believed_provider_quality": self.believed_provider_quality,
            "active_funding": self.active_funding,
            "funding_history": self.funding_history,
            "recent_reasoning": self.recent_reasoning,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "FunderPrivateState":
        known = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in data.items() if k in known})

    def get_summary(self) -> str:
        summary = f"Funder Type: {self.funder_type}\n"
        summary += f"Mission: {self.mission_statement or 'N/A'}\n"
        summary += f"Total Capital: ${self.total_capital:,.0f}\n"
        summary += f"Deployed Capital: ${self.deployed_capital:,.0f}\n"
        summary += f"Available: ${self.total_capital - self.deployed_capital:,.0f}\n"
        if self.believed_provider_quality:
            summary += "\nProvider Quality Beliefs:\n"
            for name, quality in sorted(
                self.believed_provider_quality.items(), key=lambda x: x[1], reverse=True
            ):
                summary += f"  {name}: {quality:.2f}\n"
        if self.active_funding:
            summary += "\nActive Funding:\n"
            for name, amount in self.active_funding.items():
                summary += f"  {name}: ${amount:,.0f}\n"
        return summary


@dataclass
class EvaluatorPrivateState:
    """
    Private state for Evaluator actors.
    """
    budget: float = 0.0
    base_funding: float = 0.0
    recent_reasoning: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "budget": self.budget,
            "base_funding": self.base_funding,
            "recent_reasoning": self.recent_reasoning,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "EvaluatorPrivateState":
        known = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in data.items() if k in known})


# ──────────────────────────────────────────────────────────────────────────────
# Ground truth classes for other actors
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class ConsumerGroundTruth:
    """Ground truth for Consumer actors. INVISIBLE."""
    true_satisfaction: float = 0.5
    true_quality_sensitivity: float = 0.5

    def to_dict(self) -> dict:
        return {
            "true_satisfaction": self.true_satisfaction,
            "true_quality_sensitivity": self.true_quality_sensitivity,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ConsumerGroundTruth":
        return cls(**data)


@dataclass
class RegulatorGroundTruth:
    """Ground truth for Regulator actors. INVISIBLE."""
    true_risk_tolerance: float = 0.5
    true_intervention_effectiveness: float = 0.5

    def to_dict(self) -> dict:
        return {
            "true_risk_tolerance": self.true_risk_tolerance,
            "true_intervention_effectiveness": self.true_intervention_effectiveness,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "RegulatorGroundTruth":
        return cls(**data)


@dataclass
class FunderGroundTruth:
    """Ground truth for Funder actors. INVISIBLE."""
    true_roi: float = 0.0
    funding_efficiency: float = 1.0

    def to_dict(self) -> dict:
        return {"true_roi": self.true_roi, "funding_efficiency": self.funding_efficiency}

    @classmethod
    def from_dict(cls, data: dict) -> "FunderGroundTruth":
        return cls(**data)


@dataclass
class MediaGroundTruth:
    """Ground truth for Media actor. INVISIBLE.

    true_influence and accuracy are internal simulation levers — never surfaced to actors.
    """
    true_influence: float = 0.5   # Actual reach/impact of media coverage
    accuracy: float = 0.8         # How accurately media reports true safety/capability state

    def to_dict(self) -> dict:
        return {"true_influence": self.true_influence, "accuracy": self.accuracy}

    @classmethod
    def from_dict(cls, data: dict) -> "MediaGroundTruth":
        return cls(**data)


# Type aliases
PrivateState = (ProviderPrivateState | ConsumerPrivateState | RegulatorPrivateState
                | FunderPrivateState | EvaluatorPrivateState)
GroundTruth = (ProviderGroundTruth | BenchmarkGroundTruth | ConsumerGroundTruth
               | RegulatorGroundTruth | FunderGroundTruth | MediaGroundTruth)
