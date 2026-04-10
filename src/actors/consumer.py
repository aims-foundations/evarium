"""
Consumer Market for Evaluation Ecosystem Simulation

Models the consumer market as segments rather than individuals.
Each segment = archetype × use_case (e.g., "software_dev_leaderboard_follower").

Key dynamics:
- Segments observe leaderboard rankings weighted by their use-case benchmark preferences
- Switching is tracked as proportions within each segment, not headcounts
- Satisfaction = dot(capability_vector, need_weights) - incident_penalty*(1+ms²) + cost_bonus
  (purely experience-based; media influence routes through exploration, not satisfaction)
- Gaming creates a perception gap: high benchmark score but low true satisfaction
- The gap drives probabilistic switching within each segment

Visibility:
- PUBLIC: market_shares (aggregate), switching_rate
- PRIVATE: per-segment beliefs, satisfaction, provider distribution
- INVISIBLE: capability_vector, need_weights (held by simulation)
"""
import json
import math
import os
from dataclasses import dataclass, field
from typing import Optional

import numpy as np


# ============================================================
#  Use-Case Profiles
# ============================================================

USE_CASE_PROFILES = {
    # Individual consumer profiles
    # need_weights: {reasoning, coding, knowledge, safety, communication, agentic}
    # Sourced from stakeholders.md — these are the hidden utility functions that determine
    # what each segment actually values regardless of how they select providers.
    # --- Individual consumer profiles ---
    # need_weights empirically grounded in sector-level AI usage surveys:
    #   Stack Overflow Developer Survey 2024/2025, McKinsey State of AI 2025,
    #   Stanford AI Index 2025, Thomson Reuters Legal AI 2025, AMA Physician
    #   AI Sentiment 2024, Gallup Teachers & AI 2024-25, Adobe Creators 2025,
    #   NBER Bick/Blandin/Deming 2024 occupation-level adoption data.
    # See docs/references.md for full citation list.
    "software_dev": {
        "label": "Software Developer",
        "benchmark_prefs": {"coding": 0.90, "reasoning": 0.08, "writing": 0.02},
        "consumer_type": "individual",
        "need_weights": {"reasoning": 0.22, "coding": 0.55, "knowledge": 0.03,
                         "safety": 0.02, "communication": 0.03, "agentic": 0.15},
    },
    "content_writer": {
        "label": "Content Writer",
        "benchmark_prefs": {"writing": 0.90, "reasoning": 0.08, "coding": 0.02},
        "consumer_type": "individual",
        "need_weights": {"reasoning": 0.10, "coding": 0.02, "knowledge": 0.20,
                         "safety": 0.03, "communication": 0.63, "agentic": 0.02},
    },
    "legal": {
        "label": "Legal Professional",
        "benchmark_prefs": {"reasoning": 0.75, "writing": 0.20, "safety": 0.05},
        "consumer_type": "individual",
        "need_weights": {"reasoning": 0.30, "coding": 0.01, "knowledge": 0.35,
                         "safety": 0.22, "communication": 0.10, "agentic": 0.02},
    },
    "healthcare": {
        "label": "Healthcare Worker",
        "benchmark_prefs": {"safety": 0.75, "reasoning": 0.20, "writing": 0.05},
        "consumer_type": "individual",
        "need_weights": {"reasoning": 0.12, "coding": 0.02, "knowledge": 0.28,
                         "safety": 0.48, "communication": 0.08, "agentic": 0.02},
    },
    "finance": {
        "label": "Finance Analyst",
        "benchmark_prefs": {"reasoning": 0.70, "safety": 0.25, "coding": 0.05},
        "consumer_type": "individual",
        "need_weights": {"reasoning": 0.35, "coding": 0.08, "knowledge": 0.22,
                         "safety": 0.25, "communication": 0.05, "agentic": 0.05},
    },
    "educator": {
        "label": "Educator",
        "benchmark_prefs": {"writing": 0.50, "reasoning": 0.40, "safety": 0.10},
        "consumer_type": "individual",
        "need_weights": {"reasoning": 0.15, "coding": 0.02, "knowledge": 0.28,
                         "safety": 0.08, "communication": 0.45, "agentic": 0.02},
    },
    "customer_service": {
        "label": "Customer Service",
        "benchmark_prefs": {"writing": 0.85, "reasoning": 0.12, "safety": 0.03},
        "consumer_type": "individual",
        "need_weights": {"reasoning": 0.05, "coding": 0.01, "knowledge": 0.12,
                         "safety": 0.15, "communication": 0.50, "agentic": 0.17},
    },
    "researcher": {
        "label": "Researcher",
        "benchmark_prefs": {"reasoning": 0.50, "coding": 0.45, "writing": 0.05},
        "consumer_type": "individual",
        "need_weights": {"reasoning": 0.30, "coding": 0.22, "knowledge": 0.28,
                         "safety": 0.03, "communication": 0.07, "agentic": 0.10},
    },
    "creative": {
        "label": "Creative Professional",
        "benchmark_prefs": {"writing": 0.85, "reasoning": 0.10, "coding": 0.05},
        "consumer_type": "individual",
        "need_weights": {"reasoning": 0.12, "coding": 0.02, "knowledge": 0.10,
                         "safety": 0.03, "communication": 0.65, "agentic": 0.08},
    },
    "marketing": {
        "label": "Marketing Professional",
        "benchmark_prefs": {"writing": 0.75, "reasoning": 0.20, "coding": 0.05},
        "consumer_type": "individual",
        "need_weights": {"reasoning": 0.12, "coding": 0.02, "knowledge": 0.18,
                         "safety": 0.03, "communication": 0.55, "agentic": 0.10},
    },
    "service_worker": {
        "label": "Service Worker",
        "benchmark_prefs": {"writing": 0.65, "reasoning": 0.25, "safety": 0.10},
        "consumer_type": "individual",
        "need_weights": {"reasoning": 0.08, "coding": 0.01, "knowledge": 0.15,
                         "safety": 0.18, "communication": 0.55, "agentic": 0.03},
    },

    # --- Organizational consumer profiles ---
    "hospital_system": {
        "label": "Hospital System",
        "benchmark_prefs": {"safety": 0.65, "reasoning": 0.25, "writing": 0.10},
        "consumer_type": "organization",
        "compliance_requirements": ["HIPAA", "patient_safety"],
        "integration_friction": 0.0,
        "decision_delay": 6,
        "need_weights": {"reasoning": 0.12, "coding": 0.02, "knowledge": 0.25,
                         "safety": 0.48, "communication": 0.10, "agentic": 0.03},
    },
    "enterprise_finance": {
        "label": "Financial Institution",
        "benchmark_prefs": {"reasoning": 0.60, "safety": 0.30, "coding": 0.10},
        "consumer_type": "organization",
        "compliance_requirements": ["SOX", "financial_reporting"],
        "integration_friction": 0.0,
        "decision_delay": 4,
        "need_weights": {"reasoning": 0.32, "coding": 0.08, "knowledge": 0.18,
                         "safety": 0.30, "communication": 0.05, "agentic": 0.07},
    },
    "tech_startup": {
        "label": "Tech Startup",
        "benchmark_prefs": {"coding": 0.70, "reasoning": 0.25, "writing": 0.05},
        "consumer_type": "organization",
        "compliance_requirements": [],
        "integration_friction": 0.0,
        "decision_delay": 2,
        "need_weights": {"reasoning": 0.18, "coding": 0.38, "knowledge": 0.05,
                         "safety": 0.04, "communication": 0.05, "agentic": 0.30},
    },
    "enterprise_legal": {
        "label": "Legal Organization",
        "benchmark_prefs": {"reasoning": 0.65, "writing": 0.25, "safety": 0.10},
        "consumer_type": "organization",
        "compliance_requirements": ["client_confidentiality", "data_protection"],
        "integration_friction": 0.0,
        "decision_delay": 5,
        "need_weights": {"reasoning": 0.28, "coding": 0.02, "knowledge": 0.35,
                         "safety": 0.22, "communication": 0.11, "agentic": 0.02},
    },
    "government_agency": {
        "label": "Government Agency",
        "benchmark_prefs": {"safety": 0.50, "reasoning": 0.30, "writing": 0.20},
        "consumer_type": "organization",
        "compliance_requirements": ["security_clearance", "data_sovereignty"],
        "integration_friction": 0.0,
        "decision_delay": 8,
        "need_weights": {"reasoning": 0.12, "coding": 0.02, "knowledge": 0.22,
                         "safety": 0.48, "communication": 0.12, "agentic": 0.04},
    },
}

# Field-specific benchmark keyword priorities for organizations
# Organizations upweight benchmarks containing these keywords beyond their base preferences
ORG_FIELD_PRIORITIES = {
    "hospital_system": ["medical", "healthcare", "health", "safety", "clinical", "diagnosis"],
    "enterprise_finance": ["finance", "financial", "accounting", "quant", "economic", "reasoning"],
    "tech_startup": ["coding", "code", "software", "engineering", "swe"],
    "enterprise_legal": ["legal", "law", "reasoning", "logic", "argument"],
    "government_agency": ["safety", "security", "compliance", "policy"],
}


# ============================================================
#  Archetype Definitions
# ============================================================

ARCHETYPES = {
    # Individual archetypes
    "leaderboard_follower": {
        "leaderboard_trust": 0.85,
        "switching_cost": 0.05,
        "switching_threshold": 0.10,
        "cost_sensitivity": 0.15,  # Follows scores, not price
    },
    "experience_driven": {
        "leaderboard_trust": 0.35,
        "switching_cost": 0.08,
        "switching_threshold": 0.06,
        "cost_sensitivity": 0.30,  # Will switch for better value
    },
    "cautious": {
        "leaderboard_trust": 0.50,
        "switching_cost": 0.20,
        "switching_threshold": 0.18,
        "cost_sensitivity": 0.20,  # Weighs cost but risk-averse about quality
    },

    # Organizational archetypes
    "enterprise_cautious": {
        "leaderboard_trust": 0.25,  # Very experience-driven
        "switching_cost": 0.35,
        "switching_threshold": 0.20,  # Above individual range (0.06-0.15)
        "cost_sensitivity": 0.10,  # Enterprises care less about per-token cost
    },
    "enterprise_growth": {
        "leaderboard_trust": 0.45,
        "switching_cost": 0.25,
        "switching_threshold": 0.15,  # Growth-oriented but still stickier than individuals
        "cost_sensitivity": 0.15,  # Some cost awareness
    },
    "enterprise_established": {
        "leaderboard_trust": 0.35,
        "switching_cost": 0.40,
        "switching_threshold": 0.18,  # Moderate inertia
        "cost_sensitivity": 0.08,  # Inertia dominates
    },
}


# ============================================================
#  MarketSegment
# ============================================================

@dataclass
class MarketSegment:
    """A segment of the consumer market defined by archetype × use_case."""

    name: str                          # e.g., "software_dev_leaderboard_follower"
    archetype: str                     # "leaderboard_follower" | "experience_driven" | "cautious"
    use_case: str                      # "software_dev" | "healthcare" | etc.
    market_fraction: float             # proportion of total market (sums to 1.0)

    # Resolved benchmark weights {benchmark_name: weight}  — for leaderboard observation
    benchmark_weights: dict = field(default_factory=dict)

    # True utility weights over capability dimensions {dim: weight} — ground truth need function
    # Used in satisfaction formula: satisfaction = dot(capability_vector, need_weights) + ...
    need_weights: dict = field(default_factory=dict)

    # Archetype parameters
    leaderboard_trust: float = 0.7
    switching_cost: float = 0.1
    switching_threshold: float = 0.15

    # Cost sensitivity: how much cost_advantage factors into satisfaction
    cost_sensitivity: float = 0.0  # 0=no price sensitivity, 0.3=max individual sensitivity

    # NEW: LLM reasoning toggle
    llm_mode: bool = False  # Use LLM for decision-making (default False for individuals)

    # NEW: Organizational parameters
    consumer_type: str = "individual"  # "individual" | "organization"
    decision_delay: int = 1  # Rounds between decisions (higher for orgs)
    integration_friction: float = 0.0  # Extra switching cost for orgs
    compliance_requirements: list = field(default_factory=list)  # e.g., ["HIPAA", "GDPR"]
    compliance_weight: float = 1.0  # Multiplier for safety satisfaction (higher for orgs)

    # Decision tracking
    rounds_since_decision: int = 0  # Track decision delay (legacy, unused in heuristic)
    last_llm_decision: Optional[dict] = None  # Store LLM reasoning trace
    prior_decisions: list = field(default_factory=list)  # Cross-round memory for LLM mode

    # Dynamic state
    provider_shares: dict = field(default_factory=dict)    # {provider: proportion}
    believed_quality: dict = field(default_factory=dict)   # {provider: expected_quality}
    running_perceived_quality: dict = field(default_factory=dict)  # {provider: EMA on satisfaction}
    satisfaction: dict = field(default_factory=dict)        # {provider: satisfaction_level}
    tenure: dict = field(default_factory=dict)              # {provider: rounds_subscribed}

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "archetype": self.archetype,
            "use_case": self.use_case,
            "market_fraction": self.market_fraction,
            "benchmark_weights": self.benchmark_weights,
            "leaderboard_trust": self.leaderboard_trust,
            "switching_cost": self.switching_cost,
            "switching_threshold": self.switching_threshold,
            "cost_sensitivity": self.cost_sensitivity,
            "llm_mode": self.llm_mode,
            "consumer_type": self.consumer_type,
            "decision_delay": self.decision_delay,
            "integration_friction": self.integration_friction,
            "compliance_requirements": self.compliance_requirements,
            "compliance_weight": self.compliance_weight,
            "rounds_since_decision": self.rounds_since_decision,
            "last_llm_decision": self.last_llm_decision,
            "prior_decisions": self.prior_decisions,
            "provider_shares": self.provider_shares,
            "believed_quality": self.believed_quality,
            "running_perceived_quality": self.running_perceived_quality,
            "satisfaction": self.satisfaction,
            "tenure": self.tenure,
        }


# ============================================================
#  ConsumerMarket
# ============================================================

class ConsumerMarket:
    """
    Manages the entire consumer market as segments.

    Each segment is defined by archetype × use_case, has a fraction of the
    total market, and tracks provider distribution as proportions.

    Replaces individual Consumer objects with aggregate market dynamics.
    """

    def __init__(
        self,
        segments: list[MarketSegment],
        provider_names: list[str],
        brand_recognition: Optional[dict] = None,
        seed: Optional[int] = None,
        consumer_llm_config: Optional[dict] = None,
    ):
        self.segments = segments
        self.provider_names = provider_names
        self.brand_recognition = brand_recognition or {}
        self.rng = np.random.default_rng(seed)
        self.current_round = 0
        self.memory = []
        self._last_segment_switching = {}  # Track per-segment switching rates
        self.open_source_providers: set = set()  # Providers with zero switching friction

        # Apply LLM configuration to segments
        if consumer_llm_config:
            self._apply_llm_config(consumer_llm_config)

        # Initialize provider shares if not already set
        for seg in self.segments:
            if not seg.provider_shares:
                seg.provider_shares = self._initial_shares(provider_names)
            if not seg.tenure:
                seg.tenure = {p: 0 for p in provider_names}

    def _apply_llm_config(self, config: dict):
        """Apply consumer LLM settings from config.

        Args:
            config: Dict with keys:
                - enabled: bool - Master switch for consumer LLM
                - individuals: bool - Use LLM for individual consumers
                - organizations: bool - Use LLM for organizational consumers
        """
        enabled = config.get("enabled", False)
        llm_individuals = config.get("individuals", False)
        llm_organizations = config.get("organizations", True)

        for seg in self.segments:
            if not enabled:
                seg.llm_mode = False
            elif seg.consumer_type == "organization":
                seg.llm_mode = llm_organizations
            else:  # individual
                seg.llm_mode = llm_individuals

    def _initial_shares(self, provider_names: list[str]) -> dict:
        """Distribute initial market shares weighted by brand recognition."""
        weights = []
        for name in provider_names:
            br = self.brand_recognition.get(name, 0.5)
            weights.append(br)
        total = sum(weights)
        if total == 0:
            return {name: 1.0 / len(provider_names) for name in provider_names}
        return {name: w / total for name, w in zip(provider_names, weights)}

    def add_provider(self, name: str, initial_share: float = 0.01):
        """Register a new provider mid-simulation with a small initial market share.

        Dilutes existing shares proportionally to make room for the entrant.
        """
        self.provider_names.append(name)
        self.brand_recognition[name] = 0.1  # low brand recognition for new entrant
        for seg in self.segments:
            # Shrink existing shares to make room
            existing_total = sum(seg.provider_shares.values())
            actual_share = min(initial_share, existing_total * 0.02)  # cap at 2% of existing
            scale = 1.0 - actual_share
            seg.provider_shares = {k: v * scale for k, v in seg.provider_shares.items()}
            seg.provider_shares[name] = actual_share
            seg.tenure[name] = 0

    def resolve_benchmark_weights(self, benchmark_tags: dict[str, str]):
        """Map use-case preference categories to benchmarks via tags.

        Matches category keywords against each benchmark's tags string
        (falls back to benchmark name if tags are empty).
        Unmatched benchmarks get a small default weight (0.1).

        For organizational consumers, applies additional upweighting (1.5x) to
        benchmarks matching their field-specific priorities.

        Args:
            benchmark_tags: {benchmark_name: tags_string}
        """
        for seg in self.segments:
            profile = USE_CASE_PROFILES.get(seg.use_case, {})
            prefs = profile.get("benchmark_prefs", {})
            weights = {}
            for bm_name, tags in benchmark_tags.items():
                match_text = (tags if tags else bm_name).lower()
                matched = False
                for category, pref_weight in prefs.items():
                    if category.lower() in match_text:
                        weights[bm_name] = max(weights.get(bm_name, 0), pref_weight)
                        matched = True
                if not matched:
                    weights[bm_name] = 0.1  # small default weight

            # Organizational field-specific upweighting
            if seg.consumer_type == "organization":
                field_keywords = ORG_FIELD_PRIORITIES.get(seg.use_case, [])
                for bm_name, tags in benchmark_tags.items():
                    match_text = (tags if tags else bm_name).lower()
                    for keyword in field_keywords:
                        if keyword.lower() in match_text:
                            weights[bm_name] = weights.get(bm_name, 0.1) * 1.5
                            break  # Only apply once per benchmark

            # Normalize
            total = sum(weights.values())
            if total > 0:
                weights = {k: v / total for k, v in weights.items()}
            seg.benchmark_weights = weights

    def observe(self, leaderboard: list, media_coverage: Optional[dict],
                round_num: int):
        """Update all segments' beliefs from leaderboard.

        Args:
            leaderboard: [(provider_name, score), ...] sorted descending
            media_coverage: Optional media coverage dict (for Phase 5)
            round_num: Current round number
        """
        self.current_round = round_num

        for seg in self.segments:
            learning_rate = 0.3

            # Media modulation (Phase 5 hook — no-op if media_coverage is None)
            if media_coverage:
                sentiment = media_coverage.get("sentiment", 0.0)
                # Positive sentiment → faster adoption of leaderboard signals
                learning_rate = 0.3 * (1 + 0.3 * sentiment)
                learning_rate = max(0.1, min(0.5, learning_rate))

                # Risk signals erode leaderboard trust, scaled by current trust.
                # High-trust segments erode more per signal (they had more to lose);
                # low-trust segments already discount benchmarks, so signals matter less.
                # Replaces the old leaderboard_follower-only gate.
                if media_coverage.get("risk_signals"):
                    incident_signals = [
                        sig for sig in media_coverage["risk_signals"]
                        if sig.startswith("incident_")
                    ]
                    other_signals = [
                        sig for sig in media_coverage["risk_signals"]
                        if not sig.startswith("incident_")
                    ]
                    if incident_signals:
                        seg.leaderboard_trust *= 0.95 ** (len(incident_signals) * seg.leaderboard_trust)
                    if other_signals:
                        seg.leaderboard_trust *= 0.98 ** (len(other_signals) * seg.leaderboard_trust)

            for provider_name, composite_score in leaderboard:
                # Blend: expected_quality = trust * leaderboard + (1-trust) * experience
                rpq = seg.running_perceived_quality.get(provider_name, composite_score)
                expected_quality = (
                    seg.leaderboard_trust * composite_score
                    + (1 - seg.leaderboard_trust) * rpq
                )

                if provider_name not in seg.believed_quality:
                    seg.believed_quality[provider_name] = expected_quality
                else:
                    old = seg.believed_quality[provider_name]
                    seg.believed_quality[provider_name] = (
                        (1 - learning_rate) * old + learning_rate * expected_quality
                    )

    def observe_per_benchmark(self, leaderboard: list,
                              per_benchmark_scores: dict,
                              media_coverage: Optional[dict],
                              round_num: int):
        """Update beliefs using per-benchmark scores weighted by use case.

        When per-benchmark scores are available, each segment weights them
        according to their benchmark_weights for a use-case-specific perception.

        Args:
            leaderboard: [(provider_name, score)] for provider name ordering
            per_benchmark_scores: {benchmark_name: {provider_name: score}}
            media_coverage: Optional media coverage dict
            round_num: Current round number
        """
        self.current_round = round_num

        for seg in self.segments:
            learning_rate = 0.3

            if media_coverage:
                sentiment = media_coverage.get("sentiment", 0.0)
                learning_rate = 0.3 * (1 + 0.3 * sentiment)
                learning_rate = max(0.1, min(0.5, learning_rate))

                # Risk signals erode leaderboard trust, scaled by current trust.
                if media_coverage.get("risk_signals"):
                    incident_signals = [
                        sig for sig in media_coverage["risk_signals"]
                        if sig.startswith("incident_")
                    ]
                    other_signals = [
                        sig for sig in media_coverage["risk_signals"]
                        if not sig.startswith("incident_")
                    ]
                    if incident_signals:
                        seg.leaderboard_trust *= 0.95 ** (len(incident_signals) * seg.leaderboard_trust)
                    if other_signals:
                        seg.leaderboard_trust *= 0.98 ** (len(other_signals) * seg.leaderboard_trust)

            for provider_name, _ in leaderboard:
                # Compute leaderboard signal: dot(published_scores, effective_relevance)
                weighted_score = 0.0
                total_weight = 0.0
                for bm_name, bm_weight in seg.benchmark_weights.items():
                    bm_scores = per_benchmark_scores.get(bm_name, {})
                    if provider_name in bm_scores:
                        weighted_score += bm_weight * bm_scores[provider_name]
                        total_weight += bm_weight
                if total_weight > 0:
                    leaderboard_signal = weighted_score / total_weight
                else:
                    leaderboard_signal = next(
                        (s for n, s in leaderboard if n == provider_name), 0.5
                    )

                # Blend: expected_quality = trust * leaderboard + (1-trust) * experience
                rpq = seg.running_perceived_quality.get(provider_name, leaderboard_signal)
                expected_quality = (
                    seg.leaderboard_trust * leaderboard_signal
                    + (1 - seg.leaderboard_trust) * rpq
                )

                # EMA smoothing on the blended expected_quality
                if provider_name not in seg.believed_quality:
                    seg.believed_quality[provider_name] = expected_quality
                else:
                    old = seg.believed_quality[provider_name]
                    seg.believed_quality[provider_name] = (
                        (1 - learning_rate) * old + learning_rate * expected_quality
                    )

    def compute_satisfaction(
        self,
        ground_truth: dict,
        provider_strategies: Optional[dict] = None,
        published_scores: Optional[dict] = None,
        media_coverage: Optional[dict] = None,
        incident_history: Optional[dict] = None,
        round_num: Optional[int] = None,
        provider_cost_advantage: Optional[dict] = None,
    ):
        """Compute per-segment per-provider satisfaction from ground truth.

        Satisfaction is now primarily based on believed_quality (use-case weighted
        perceived performance), adjusted for:
        1. Gaming detection penalty (score inflation above true capability)
        2. Safety alignment match (provider safety investment × segment safety preference)
        3. Media sentiment influence (negative coverage reduces satisfaction)
        4. Incident history penalty (recent safety incidents reduce trust and satisfaction)

        This creates natural differentiation across use cases: software developers
        experience satisfaction based on coding performance, healthcare workers based
        on safety/reasoning performance, etc.

        Args:
            ground_truth: {provider_name: ProviderGroundTruth}
            provider_strategies: {provider_name: {rd, safety, product, safety_capability}}
            published_scores: {provider_name: composite_score}
            media_coverage: Media coverage dict with sentiment and provider_attention
        """
        _DIMS = ["reasoning", "coding", "knowledge", "safety", "communication", "agentic"]
        _UNIFORM = {d: 1.0 / len(_DIMS) for d in _DIMS}

        for seg in self.segments:
            need_wts = seg.need_weights if seg.need_weights else _UNIFORM

            for provider_name in self.provider_names:
                if provider_name not in ground_truth:
                    continue

                gt = ground_truth[provider_name]
                cap_vec = gt.capability_vector

                # Base satisfaction: dot(capability_vector, need_weights)
                # This is what the segment actually experiences — true quality for their use case.
                # Gaming emerges naturally: providers over-invested in benchmark-weighted dims
                # score higher but satisfy less if those dims don't match segment needs.
                base_satisfaction = sum(
                    cap_vec.get(d, 0.0) * need_wts.get(d, 0.0) for d in _DIMS
                )

                # Media influence on consumers is routed through exploration
                # behavior (see _compute_switching_heuristic), not satisfaction.
                # Satisfaction is purely experience-based (Hardy et al. 2024).

                # Factor 1: Incident History Penalty
                # Exponential decay: recent incidents dominate, old ones fade naturally.
                # severity-weighted × decay^age × (1 + market_share²) — larger providers
                # face greater reputational exposure per incident (grounded in scale-
                # contingent regulatory obligations: EO 14110, SB 1047).
                incident_penalty = 0.0
                market_share = gt.market_share
                if incident_history and provider_name in incident_history and round_num is not None:
                    provider_incidents = incident_history[provider_name]
                    severity_weights = {"minor": 0.01, "moderate": 0.05, "major": 0.10, "critical": 0.20}
                    incident_decay_rate = 0.70  # ~2.3-round half-life
                    raw_penalty = 0.0
                    for inc in provider_incidents:
                        age = round_num - inc.round_num
                        if age < 0 or age > 10:
                            continue
                        weight = severity_weights.get(inc.severity, 0.05)
                        weight *= incident_decay_rate ** age
                        # 2x if incident category matches segment sector
                        if seg.use_case in inc.affected_sectors or seg.consumer_type in inc.affected_sectors:
                            weight *= 2.0
                        raw_penalty += weight
                    incident_penalty = raw_penalty * (1.0 + market_share ** 2)

                # Factor 2: Cost Efficiency Bonus
                # cost_sensitivity × cost_advantage × 0.15
                cost_bonus = 0.0
                if provider_cost_advantage and provider_name in provider_cost_advantage:
                    cost_eff = provider_cost_advantage[provider_name]
                    cost_bonus = seg.cost_sensitivity * cost_eff * 0.15

                # Compute final satisfaction (purely experience-based)
                satisfaction = (
                    base_satisfaction
                    - incident_penalty
                    + cost_bonus
                )

                # Clamp to [0, 1]
                sat_clamped = max(0.0, min(1.0, satisfaction))
                seg.satisfaction[provider_name] = sat_clamped

                # Update running_perceived_quality via EMA on realized satisfaction
                rpq_alpha = 0.3  # EMA learning rate
                old_rpq = seg.running_perceived_quality.get(provider_name, sat_clamped)
                seg.running_perceived_quality[provider_name] = (
                    (1 - rpq_alpha) * old_rpq + rpq_alpha * sat_clamped
                )

                # Store penalty breakdown for logging (segment-level, last round)
                if not hasattr(seg, '_penalty_breakdown'):
                    seg._penalty_breakdown = {}
                seg._penalty_breakdown[provider_name] = {
                    "base_satisfaction": base_satisfaction,
                    "incident_penalty": incident_penalty,
                    "cost_bonus": cost_bonus,
                }

    def compute_switching(self, provider_strategies: Optional[dict] = None,
                         published_scores: Optional[dict] = None,
                         media_coverage: Optional[dict] = None,
                         regulator_data: Optional[dict] = None,
                         incident_history: Optional[dict] = None,
                         per_benchmark_scores: Optional[dict] = None,
                         provider_cost_advantage: Optional[dict] = None,
                         deployer_liability_guidance: Optional[set] = None,
                         market_growth_rate: float = 0.0,
                         provider_product_budgets: Optional[dict] = None,
                         enable_product_retention: bool = True):
        """Compute switching proportions within each segment.

        Two triggers (same logic as original Consumer, but applied proportionally):
        1. Dissatisfaction: believed quality > actual satisfaction by > threshold
        2. Opportunity: a better alternative exceeds switching cost + tenure bonus

        Args:
            provider_strategies: {provider_name: {rd, safety, product}} - portfolio fractions only
            published_scores: {provider_name: score} - for LLM context
            media_coverage: Media coverage dict - for LLM context
            regulator_data: Regulator data dict - for LLM context

        Returns:
            Total switching rate (fraction of total market that switched)
        """
        total_switching = 0.0

        # Track per-segment switching for analysis
        segment_switching_rates = {}

        for seg in self.segments:
            # Decay switch cooldown each round (replaces decision_delay)
            if not hasattr(seg, '_switch_cooldown'):
                seg._switch_cooldown = 0.0
            seg._switch_cooldown *= 0.5  # ~2-round half-life

            # Branch on reasoning mode
            if seg.llm_mode:
                seg_switching = self._compute_switching_llm(
                    seg, provider_strategies, published_scores,
                    media_coverage, regulator_data, incident_history, per_benchmark_scores,
                    provider_cost_advantage, deployer_liability_guidance
                )
            else:
                seg_switching = self._compute_switching_heuristic(
                    seg, market_growth_rate, media_coverage,
                    provider_product_budgets=provider_product_budgets,
                    enable_product_retention=enable_product_retention)

            total_switching += seg_switching * seg.market_fraction
            segment_switching_rates[seg.name] = seg_switching

        # Store for later retrieval
        self._last_segment_switching = segment_switching_rates

        return total_switching

    def _compute_switching_heuristic(self, seg: MarketSegment,
                                     market_growth_rate: float = 0.0,
                                     media_coverage: Optional[dict] = None,
                                     provider_product_budgets: Optional[dict] = None,
                                     enable_product_retention: bool = True) -> float:
        """Compute heuristic-based switching for a segment.

        Returns:
            Switching rate for this segment
        """
        seg_switching = 0.0

        for provider in list(seg.provider_shares.keys()):
                share = seg.provider_shares.get(provider, 0.0)
                if share < 0.001:  # skip negligible shares
                    continue

                # Product investment retention bonus: higher product budget -> stickier users
                retention_bonus = 0.0
                if enable_product_retention and provider_product_budgets and provider in provider_product_budgets:
                    pb = provider_product_budgets[provider]
                    retention_bonus = _product_retention_bonus(
                        pb["product_budget"], pb.get("is_open_source", False))

                # Switching cost dampens the fraction that follows through (0 = frictionless, 1 = locked in)
                cost_damper = 1.0 - min(0.9, seg.switching_cost * (1.0 + retention_bonus))

                should_switch_prob = 0.0
                best_alternative = None
                best_alt_score = -1.0

                # Post-switch cooldown raises threshold temporarily
                cooldown = getattr(seg, '_switch_cooldown', 0.0)

                # --- Trigger 1: Dissatisfaction ---
                believed = seg.believed_quality.get(provider, 0.5)
                actual_sat = seg.satisfaction.get(provider, 0.5)
                gap = believed - actual_sat

                threshold = seg.switching_threshold + cooldown
                if gap > 0:
                    # Sigmoid-based probability: smooth transition
                    should_switch_prob = max(
                        should_switch_prob,
                        _switching_probability(gap, threshold),
                    )

                # --- Trigger 2: Better alternative ---
                current_blended = self._blended_score(seg, provider)
                opportunity_threshold = seg.switching_threshold * 0.5 + cooldown

                for alt_provider in self.provider_names:
                    if alt_provider == provider:
                        continue
                    alt_blended = self._blended_score(seg, alt_provider)
                    improvement = alt_blended - current_blended
                    if improvement > 0:
                        opp_prob = _switching_probability(
                            improvement, opportunity_threshold
                        )
                        if opp_prob > should_switch_prob:
                            should_switch_prob = opp_prob
                        if alt_blended > best_alt_score:
                            best_alt_score = alt_blended
                            best_alternative = alt_provider

                # Apply switching: cost_damper reduces fraction that follows through
                if should_switch_prob > 0.01 and best_alternative:
                    switching_fraction = should_switch_prob * share * cost_damper
                    switching_fraction = min(switching_fraction, share)  # can't exceed current share

                    seg.provider_shares[provider] -= switching_fraction
                    seg.provider_shares[best_alternative] = (
                        seg.provider_shares.get(best_alternative, 0.0) + switching_fraction
                    )
                    seg_switching += switching_fraction

                    # Spike cooldown after a switch
                    seg._switch_cooldown = 0.20

        # Exploration churn: per-provider, media-driven.
        # Base rate models free-tier trials, word-of-mouth, new product launches.
        # Negative media coverage about a specific provider drives its users to
        # explore alternatives at a higher rate, scaled by leaderboard_trust
        # (high-trust segments respond more to media signals; experience-driven
        # segments mostly ignore headlines). Hardy et al. (2024): benchmarks and
        # media drive attention/exploration, not direct quality perception.
        base_rate = 0.05
        exploration_pool = 0.0
        for provider in list(seg.provider_shares.keys()):
            share = seg.provider_shares.get(provider, 0.0)
            if share < 0.001:
                continue
            provider_rate = base_rate
            if media_coverage:
                p_attention = media_coverage.get("provider_attention", {}).get(provider, 0.0)
                sentiment = media_coverage.get("sentiment", 0.0)
                if sentiment < 0:
                    provider_rate += p_attention * abs(sentiment) * seg.leaderboard_trust
            churn = share * provider_rate
            seg.provider_shares[provider] -= churn
            exploration_pool += churn

        # Redistribution: blend satisfaction (experience-based) and believed_quality
        # (public-signal-based). When media drives extra exploration, those explorers
        # choose based on public signals (believed_quality + media buzz) rather than
        # satisfaction they haven't experienced. This preserves credence good dynamics:
        # consumers can't evaluate safety themselves, so media-driven explorers follow
        # public signals including safety coverage.
        if exploration_pool > 0:
            base_pool = sum(
                max(0.0, seg.provider_shares.get(p, 0.0)) * base_rate
                for p in self.provider_names
            )
            media_fraction = max(0.0, 1.0 - base_pool / exploration_pool) if exploration_pool > 0.001 else 0.0

            sat_scores = {p: max(0.01, seg.satisfaction.get(p, 0.3)) for p in self.provider_names}
            bq_scores = {p: max(0.01, seg.believed_quality.get(p, 0.3)) for p in self.provider_names}

            # Positive media pulls explorers toward buzzy providers
            if media_coverage and media_coverage.get("sentiment", 0.0) > 0:
                sentiment = media_coverage["sentiment"]
                for p in self.provider_names:
                    p_attn = media_coverage.get("provider_attention", {}).get(p, 0.0)
                    media_pull = 1.0 + sentiment * p_attn * seg.leaderboard_trust
                    bq_scores[p] *= media_pull

            sat_total = sum(sat_scores.values())
            bq_total = sum(bq_scores.values())
            for provider in self.provider_names:
                sat_share = sat_scores[provider] / sat_total
                bq_share = bq_scores[provider] / bq_total
                blended = (1.0 - media_fraction) * sat_share + media_fraction * bq_share
                seg.provider_shares[provider] = (
                    seg.provider_shares.get(provider, 0.0) + exploration_pool * blended
                )
            seg_switching += exploration_pool

        # New-user entry: in a growing market, new adopters choose independently
        # based on believed_quality rather than inheriting incumbent shares.
        # New users are additive — existing shares are diluted by renormalization.
        if market_growth_rate > 0:
            new_user_weight = market_growth_rate  # fraction of existing market that enters
            quality_scores = {p: max(0.01, seg.believed_quality.get(p, 0.3))
                              for p in self.provider_names}
            quality_total = sum(quality_scores.values())
            for provider in self.provider_names:
                seg.provider_shares[provider] = (
                    seg.provider_shares.get(provider, 0.0)
                    + new_user_weight * quality_scores[provider] / quality_total
                )

        # Update tenure for remaining subscribers
        for provider in self.provider_names:
            if seg.provider_shares.get(provider, 0) > 0.01:
                seg.tenure[provider] = seg.tenure.get(provider, 0) + 1

        # Normalize shares to prevent drift
        total_share = sum(seg.provider_shares.values())
        if total_share > 0:
            seg.provider_shares = {
                k: v / total_share for k, v in seg.provider_shares.items()
            }

        return seg_switching

    def _compute_switching_llm(self, seg: MarketSegment,
                               provider_strategies: Optional[dict],
                               published_scores: Optional[dict],
                               media_coverage: Optional[dict],
                               regulator_data: Optional[dict],
                               incident_history: Optional[dict] = None,
                               per_benchmark_scores: Optional[dict] = None,
                               provider_cost_advantage: Optional[dict] = None,
                               deployer_liability_guidance: Optional[set] = None) -> float:
        """LLM-based switching: single call per segment, vendor review brief format."""
        from llm import get_provider as get_llm_provider

        seg_switching = 0.0
        cooldown = getattr(seg, '_switch_cooldown', 0.0)

        # Skip LLM call if recent switch cooldown is active
        if cooldown > 0.15:
            return 0.0

        # Find primary vendor (largest share)
        current_provider = max(seg.provider_shares, key=seg.provider_shares.get)
        current_share = seg.provider_shares.get(current_provider, 0.0)
        if current_share < 0.05:
            return 0.0

        # Build the vendor review brief
        if seg.consumer_type == "organization":
            prompt = self._build_vendor_review_brief(
                seg, current_provider, published_scores, media_coverage,
                regulator_data, incident_history, per_benchmark_scores,
                provider_cost_advantage, deployer_liability_guidance)
        else:
            prompt = self._build_individual_prompt_v2(
                seg, current_provider, published_scores, media_coverage,
                per_benchmark_scores, provider_cost_advantage)

        # Single LLM call
        fail_safe = {"action": "renew", "target_provider": None,
                     "share_to_move": 0.0, "reasoning": "LLM parse failure - defaulting to renew"}
        try:
            llm = get_llm_provider()
            decision = llm.generate_json(prompt, retries=2, fail_safe=fail_safe)
        except Exception as e:
            print(f"[ConsumerMarket] LLM failed for {seg.name}: {e}")
            decision = fail_safe

        action = decision.get("action", "renew")
        target = decision.get("target_provider")
        share_to_move = float(decision.get("share_to_move", 0.0))
        reasoning = decision.get("reasoning", "")

        # Validate target
        if action in ("switch", "pilot") and (not target or target not in self.provider_names or target == current_provider):
            action = "renew"

        # Apply decision
        if action == "pilot":
            share_to_move = max(0.10, min(0.25, share_to_move))
            actual_move = share_to_move * current_share
            seg.provider_shares[current_provider] -= actual_move
            seg.provider_shares[target] = seg.provider_shares.get(target, 0.0) + actual_move
            seg_switching = actual_move
            seg._switch_cooldown = 0.15
        elif action == "switch":
            share_to_move = max(0.30, min(1.0, share_to_move))
            actual_move = share_to_move * current_share
            seg.provider_shares[current_provider] -= actual_move
            seg.provider_shares[target] = seg.provider_shares.get(target, 0.0) + actual_move
            seg_switching = actual_move
            seg._switch_cooldown = 0.25

        # Store decision in cross-round memory
        seg.last_llm_decision = {
            "round": self.current_round,
            "action": action,
            "current_provider": current_provider,
            "target_provider": target,
            "share_to_move": share_to_move if action != "renew" else 0.0,
            "reasoning": reasoning,
        }
        seg.prior_decisions.append({
            "round": self.current_round,
            "action": action,
            "target_provider": target,
            "reasoning": reasoning[:150],
        })
        seg.prior_decisions = seg.prior_decisions[-4:]

        # Update tenure
        for provider in self.provider_names:
            if seg.provider_shares.get(provider, 0) > 0.01:
                seg.tenure[provider] = seg.tenure.get(provider, 0) + 1

        # Normalize shares
        total_share = sum(seg.provider_shares.values())
        if total_share > 0:
            seg.provider_shares = {k: v / total_share for k, v in seg.provider_shares.items()}

        return seg_switching

    # ------------------------------------------------------------------
    #  Translation helpers (simulation state -> natural language)
    # ------------------------------------------------------------------

    @staticmethod
    def _satisfaction_label(sat: float) -> str:
        if sat > 0.75: return "Excellent"
        if sat > 0.55: return "Good"
        if sat > 0.40: return "Mixed"
        return "Poor"

    @staticmethod
    def _cost_tier(cost_advantage: float) -> str:
        if cost_advantage > 0.65: return "Budget-friendly"
        if cost_advantage > 0.25: return "Mid-range pricing"
        return "Premium pricing"

    @staticmethod
    def _benchmark_rank_label(rank: int, total: int) -> str:
        if rank == 1: return f"Leader (1st of {total})"
        if rank <= total // 2: return f"Above average ({rank}/{total})"
        return f"Below average ({rank}/{total})"

    # ------------------------------------------------------------------
    #  Vendor review brief (organizational LLM prompt)
    # ------------------------------------------------------------------

    def _build_vendor_review_brief(self, seg: MarketSegment, current_provider: str,
                                    published_scores: Optional[dict],
                                    media_coverage: Optional[dict],
                                    regulator_data: Optional[dict],
                                    incident_history: Optional[dict],
                                    per_benchmark_scores: Optional[dict],
                                    provider_cost_advantage: Optional[dict],
                                    deployer_liability_guidance: Optional[set]) -> str:
        """Build PIMMUR-compliant vendor review brief for organizational consumers."""
        use_case_label = USE_CASE_PROFILES.get(seg.use_case, {}).get("label", seg.use_case)
        compliance_text = ", ".join(seg.compliance_requirements) if seg.compliance_requirements else "None specific"
        cost_adv = provider_cost_advantage or {}
        liability = deployer_liability_guidance or set()

        # Prior decisions (cross-round memory)
        prior_text = ""
        if seg.prior_decisions:
            prior_lines = []
            for pd in seg.prior_decisions[-2:]:
                action_desc = {"renew": "Renewed contract", "switch": "Switched vendor",
                               "pilot": "Launched pilot"}.get(pd["action"], pd["action"])
                target_note = f" with {pd['target_provider']}" if pd.get("target_provider") else ""
                prior_lines.append(f"[Month {pd['round']}]: {action_desc}{target_note}. {pd['reasoning']}")
            prior_text = "Prior Reviews:\n" + "\n".join(prior_lines) + "\n"

        # Current vendor summary
        cur_sat = self._satisfaction_label(seg.satisfaction.get(current_provider, 0.5))
        cur_cost = self._cost_tier(cost_adv.get(current_provider, 0.0))
        cur_tenure = seg.tenure.get(current_provider, 0)

        # Incident record for current vendor
        incident_text = "No reported incidents."
        if incident_history:
            cur_incs = incident_history.get(current_provider, [])
            if cur_incs:
                recent = cur_incs[-5:]
                inc_lines = [f"- [{inc.severity.upper()}] Month {inc.round_num}: {inc.description}"
                             for inc in recent]
                incident_text = "\n".join(inc_lines)

        # Benchmark comparison table
        bm_table = ""
        if per_benchmark_scores:
            bm_names = list(per_benchmark_scores.keys())[:5]
            providers_with_scores = self.provider_names
            n_provs = len(providers_with_scores)

            header = "| Vendor |"
            sep = "|--------|"
            for bm in bm_names:
                short_bm = bm[:20]
                header += f" {short_bm} |"
                sep += "------|"

            rows = []
            for prov in providers_with_scores:
                marker = " (current)" if prov == current_provider else ""
                row = f"| {prov}{marker} |"
                for bm in bm_names:
                    scores = per_benchmark_scores.get(bm, {})
                    score = scores.get(prov)
                    if score is not None:
                        ranked = sorted(scores.values(), reverse=True)
                        rank = ranked.index(score) + 1
                        row += f" {self._benchmark_rank_label(rank, n_provs)} |"
                    else:
                        row += " N/A |"
                rows.append(row)

            bm_table = f"{header}\n{sep}\n" + "\n".join(rows)

        # Alternative vendors
        alt_lines = []
        for prov in self.provider_names:
            if prov == current_provider:
                continue
            alt_sat = self._satisfaction_label(seg.satisfaction.get(prov, 0.3))
            alt_cost = self._cost_tier(cost_adv.get(prov, 0.0))
            inc_count = len(incident_history.get(prov, [])) if incident_history else 0
            inc_note = f"{inc_count} incidents on record" if inc_count > 0 else "Clean safety record"
            liability_note = " [Note: Open-source model - your organization bears deployment liability]" if prov in liability else ""
            alt_lines.append(f"- {prov}: Performance {alt_sat}, {alt_cost}, {inc_note}{liability_note}")
        alternatives_text = "\n".join(alt_lines) if alt_lines else "(none)"

        # Media intelligence
        media_text = ""
        if media_coverage:
            headlines = media_coverage.get("headlines", [])[:4]
            if headlines:
                media_text = "Market Intelligence:\n" + "\n".join(f"- {h}" for h in headlines)
            risk_signals = media_coverage.get("risk_signals", [])
            if risk_signals:
                media_text += "\nRisk signals: " + ", ".join(risk_signals[:3])

        # Regulatory context
        reg_text = ""
        if regulator_data:
            interventions = regulator_data.get("interventions", [])
            if interventions:
                types = set(iv.get("type", "oversight") for iv in interventions)
                reg_text = f"Regulatory environment: {len(interventions)} active intervention(s) ({', '.join(types)})"

        # Liability warning for current vendor
        liability_text = ""
        if current_provider in liability:
            liability_text = (f"Deployer Liability Notice: Regulators have issued guidance that "
                              f"organizations deploying {current_provider} (open-source) bear "
                              f"liability for safety incidents with no recourse against the model provider.")

        # Cost sensitivity framing
        cost_sens = seg.cost_sensitivity
        if cost_sens >= 0.20:
            budget_note = "Budget pressure is a primary constraint for this organization."
        elif cost_sens >= 0.10:
            budget_note = "Cost matters but capability and safety take precedence."
        else:
            budget_note = ""

        prompt = f"""Quarterly AI Vendor Review - {use_case_label}

{prior_text}Current Vendor: {current_provider}
- Relationship tenure: {cur_tenure} months
- Overall experience: {cur_sat}
- Pricing: {cur_cost}

Safety and Incident Record:
{incident_text}

Published Benchmark Performance:
{bm_table if bm_table else "(Benchmark data not available)"}

Alternative Vendors:
{alternatives_text}

Compliance Requirements: {compliance_text}
{budget_note}
{media_text}
{reg_text}
{liability_text}

Your organization ({use_case_label}) is conducting its quarterly AI vendor review. Based on the information above, what is the committee's recommendation?

Respond with ONLY valid JSON:
{{"action": "renew" | "switch" | "pilot", "target_provider": "vendor name or null", "share_to_move": 0.0 to 1.0, "reasoning": "committee rationale (1-2 sentences)"}}

Guidelines:
- "renew": Continue with current vendor for all deployments
- "pilot": Trial an alternative for a portion of deployments (share_to_move typically 0.10-0.25)
- "switch": Full migration to a new vendor (share_to_move typically 0.50-1.0)
- Consider piloting when an alternative looks promising but migration risk is significant"""

        return prompt

    # ------------------------------------------------------------------
    #  Individual consumer LLM prompt (simplified, PIMMUR-compliant)
    # ------------------------------------------------------------------

    def _build_individual_prompt_v2(self, seg: MarketSegment, current_provider: str,
                                    published_scores: Optional[dict],
                                    media_coverage: Optional[dict],
                                    per_benchmark_scores: Optional[dict],
                                    provider_cost_advantage: Optional[dict]) -> str:
        """Build PIMMUR-compliant prompt for individual consumer decisions."""
        use_case_label = USE_CASE_PROFILES.get(seg.use_case, {}).get("label", seg.use_case)
        cost_adv = provider_cost_advantage or {}

        cur_sat = self._satisfaction_label(seg.satisfaction.get(current_provider, 0.5))
        cur_cost = self._cost_tier(cost_adv.get(current_provider, 0.0))

        # Top 3 alternatives by believed quality
        alts = []
        for prov in self.provider_names:
            if prov == current_provider:
                continue
            alts.append((prov, seg.believed_quality.get(prov, 0.3)))
        alts.sort(key=lambda x: -x[1])

        alt_lines = []
        for prov, _ in alts[:3]:
            alt_sat = self._satisfaction_label(seg.satisfaction.get(prov, 0.3))
            alt_cost = self._cost_tier(cost_adv.get(prov, 0.0))
            alt_lines.append(f"- {prov}: {alt_sat} experience, {alt_cost}")
        alternatives_text = "\n".join(alt_lines)

        media_text = ""
        if media_coverage:
            headlines = media_coverage.get("headlines", [])[:3]
            if headlines:
                media_text = "Recent news:\n" + "\n".join(f"- {h}" for h in headlines)

        prompt = f"""You are a {use_case_label} deciding whether to switch AI providers.

Current provider: {current_provider}
- Your experience: {cur_sat}
- Pricing: {cur_cost}
- Using for: {seg.tenure.get(current_provider, 0)} months

Top alternatives:
{alternatives_text}
{media_text}

Should you switch? Respond with ONLY valid JSON:
{{"action": "renew" | "switch", "target_provider": "name or null", "share_to_move": 1.0, "reasoning": "brief explanation"}}"""

        return prompt

    def _blended_score(self, seg: MarketSegment, provider: str) -> float:
        """Compute blended perceived quality for a provider within a segment."""
        trust = seg.leaderboard_trust
        believed = seg.believed_quality.get(provider, 0.5)
        actual_sat = seg.satisfaction.get(provider, 0.5)
        # Blend leaderboard-derived belief with actual experience
        return trust * believed + (1 - trust) * actual_sat

    # ------------------------------------------------------------------
    #  Dynamic consumer market: enterprise share rebalancing
    # ------------------------------------------------------------------

    def rebalance_market_fractions(
        self,
        round_num: int,
        start: float = 0.25,
        end: float = 0.55,
        midpoint: int = 18,
    ):
        """Rebalance market_fraction so enterprise share follows a logistic curve.

        Enterprise segments grow from `start` to `end` over the simulation.
        Individual segments shrink proportionally. Within each class, relative
        proportions are preserved.
        """
        # Store base fractions on first call
        if not hasattr(self, "_base_fractions"):
            self._base_fractions = {seg.name: seg.market_fraction for seg in self.segments}
            self._base_enterprise_total = sum(
                f for seg, f in zip(self.segments, [self._base_fractions[s.name] for s in self.segments])
                if seg.consumer_type == "organization"
            )
            self._base_individual_total = 1.0 - self._base_enterprise_total

        # Logistic curve: target enterprise share at this round
        k = 0.25  # steepness
        target_enterprise = start + (end - start) / (1.0 + math.exp(-k * (round_num - midpoint)))

        target_individual = 1.0 - target_enterprise

        # Scale each segment's fraction proportionally within its class
        for seg in self.segments:
            base = self._base_fractions[seg.name]
            if seg.consumer_type == "organization":
                if self._base_enterprise_total > 0:
                    seg.market_fraction = base * (target_enterprise / self._base_enterprise_total)
            else:
                if self._base_individual_total > 0:
                    seg.market_fraction = base * (target_individual / self._base_individual_total)

    def get_enterprise_share(self) -> float:
        """Return current fraction of market held by enterprise segments."""
        return sum(seg.market_fraction for seg in self.segments if seg.consumer_type == "organization")

    def get_consumer_data(self) -> dict:
        """Return consumer_data dict compatible with downstream systems.

        Returns dict with:
            market_shares: {provider: proportion} aggregated across segments
            provider_satisfaction: {provider: avg_satisfaction} weighted by share
            avg_satisfaction: float — market-wide weighted average
            switching_rate: float — stored from last compute_switching()
            segment_data: {segment_name: {provider_shares, satisfaction}}
        """
        # Aggregate market shares across segments
        market_shares = {p: 0.0 for p in self.provider_names}
        for seg in self.segments:
            for provider, share in seg.provider_shares.items():
                market_shares[provider] = (
                    market_shares.get(provider, 0.0) + share * seg.market_fraction
                )

        # Per-provider satisfaction (weighted by market share across segments)
        provider_satisfaction = {}
        for provider in self.provider_names:
            weighted_sat = 0.0
            total_weight = 0.0
            for seg in self.segments:
                seg_share = seg.provider_shares.get(provider, 0.0)
                weight = seg_share * seg.market_fraction
                if weight > 0:
                    sat = seg.satisfaction.get(provider, 0.5)
                    weighted_sat += sat * weight
                    total_weight += weight
            if total_weight > 0:
                provider_satisfaction[provider] = weighted_sat / total_weight
            else:
                provider_satisfaction[provider] = 0.0

        # Market-wide average satisfaction
        avg_satisfaction = 0.0
        total_share = sum(market_shares.values())
        if total_share > 0:
            for provider, share in market_shares.items():
                avg_satisfaction += (
                    provider_satisfaction.get(provider, 0.0) * share
                )
            avg_satisfaction /= total_share

        # Segment data for detailed analysis
        segment_data = {}
        for seg in self.segments:
            segment_data[seg.name] = {
                "archetype": seg.archetype,
                "use_case": seg.use_case,
                "market_fraction": seg.market_fraction,
                "provider_shares": dict(seg.provider_shares),
                "satisfaction": dict(seg.satisfaction),
                "switching_rate": self._last_segment_switching.get(seg.name, 0.0),
            }

        # Collect org LLM reasoning traces
        org_llm_decisions = {}
        for seg in self.segments:
            if seg.consumer_type == "organization" and hasattr(seg, "last_llm_decision") and seg.last_llm_decision:
                d = seg.last_llm_decision
                org_llm_decisions[seg.name] = {
                    "round": d.get("round"),
                    "action": d.get("action", "renew"),
                    "current_provider": d.get("current_provider"),
                    "target_provider": d.get("target_provider"),
                    "share_to_move": d.get("share_to_move", 0.0),
                    "reasoning": d.get("reasoning", ""),
                    "use_case": seg.use_case,
                    "archetype": seg.archetype,
                }

        # Aggregate penalty breakdown per provider (market-share-weighted across segments)
        penalty_breakdown = {}
        for provider in self.provider_names:
            agg = {"base_satisfaction": 0.0, "incident_penalty": 0.0,
                   "cost_bonus": 0.0}
            total_weight = 0.0
            for seg in self.segments:
                pb = getattr(seg, '_penalty_breakdown', {}).get(provider)
                if pb is None:
                    continue
                weight = seg.provider_shares.get(provider, 0.0) * seg.market_fraction
                if weight > 0:
                    for k in agg:
                        agg[k] += pb[k] * weight
                    total_weight += weight
            if total_weight > 0:
                penalty_breakdown[provider] = {k: v / total_weight for k, v in agg.items()}
            else:
                penalty_breakdown[provider] = agg

        # Population-weighted need_weights (fixed per run, but useful for analysis)
        agg_need = {}
        _DIMS = ["reasoning", "coding", "knowledge", "safety", "communication", "agentic"]
        for d in _DIMS:
            agg_need[d] = sum(
                seg.market_fraction * (seg.need_weights.get(d, 0.0) if seg.need_weights else 1.0 / len(_DIMS))
                for seg in self.segments
            )

        return {
            "market_shares": market_shares,
            "provider_satisfaction": provider_satisfaction,
            "avg_satisfaction": avg_satisfaction,
            "switching_rate": 0.0,  # set by caller after compute_switching()
            "segment_data": segment_data,
            "org_llm_decisions": org_llm_decisions,
            "penalty_breakdown": penalty_breakdown,
            "need_weights": agg_need,
        }

    def save(self, folder: str):
        """Save consumer market state to folder."""
        os.makedirs(folder, exist_ok=True)
        data = {
            "provider_names": self.provider_names,
            "brand_recognition": self.brand_recognition,
            "current_round": self.current_round,
            "segments": [seg.to_dict() for seg in self.segments],
        }
        with open(os.path.join(folder, "consumer_market.json"), "w") as f:
            json.dump(data, f, indent=2)

    def __repr__(self):
        return (
            f"ConsumerMarket(segments={len(self.segments)}, "
            f"providers={self.provider_names})"
        )


# ============================================================
#  Helper Functions
# ============================================================

def _switching_probability(gap: float, threshold: float,
                           steepness: float = 10.0) -> float:
    """Sigmoid-based switching probability.

    Args:
        gap: The dissatisfaction or improvement gap
        threshold: The switching threshold
        steepness: How sharp the sigmoid transition is (default 10)

    Returns:
        Probability of switching (0-1)
    """
    x = steepness * (gap - threshold)
    # Clamp to avoid overflow
    x = max(-20.0, min(20.0, x))
    return 1.0 / (1.0 + math.exp(-x))


# Product investment -> switching cost retention bonus
_PRODUCT_RETENTION_K = 2.0       # Saturating exponential steepness
_PRODUCT_RETENTION_MAX = 0.50    # Maximum 50% increase in switching cost
_OS_RETENTION_CAP = 0.15         # Open-source cap (users can self-host competitors)

def _product_retention_bonus(product_budget: float, is_open_source: bool = False) -> float:
    """Compute switching cost retention bonus from product investment.

    Saturating exponential: bonus = max_bonus * (1 - exp(-k * budget))
    Open-source providers capped at os_cap.

    At budget=0: bonus = 0 (no product = no lock-in).
    At budget=0.5: ~32% switching cost increase.
    At budget >> 1: approaches max_bonus (50%).
    """
    raw = _PRODUCT_RETENTION_MAX * (1.0 - math.exp(-_PRODUCT_RETENTION_K * product_budget))
    if is_open_source:
        return min(raw, _OS_RETENTION_CAP)
    return raw


def create_default_segments(
    use_cases: list[str],
    provider_names: list[str],
    brand_recognition: Optional[dict] = None,
    archetype_weights: Optional[dict] = None,
    organizational_archetype_weights: Optional[dict] = None,
) -> list[MarketSegment]:
    """Create market segments from use cases and archetypes.

    Args:
        use_cases: List of use case profile keys (e.g., ["software_dev", "healthcare"])
        provider_names: List of provider names
        brand_recognition: Optional {provider: recognition_factor}
        archetype_weights: Optional custom archetype distribution for individuals.
            Default: {"leaderboard_follower": 0.4, "experience_driven": 0.35, "cautious": 0.25}
        organizational_archetype_weights: Optional archetype distribution for organizations.
            Default: {"enterprise_cautious": 0.5, "enterprise_growth": 0.3, "enterprise_established": 0.2}

    Returns:
        List of MarketSegment objects with equal market fractions per use case
    """
    if archetype_weights is None:
        archetype_weights = {
            "leaderboard_follower": 0.40,
            "experience_driven": 0.35,
            "cautious": 0.25,
        }

    if organizational_archetype_weights is None:
        organizational_archetype_weights = {
            "enterprise_cautious": 0.50,
            "enterprise_growth": 0.30,
            "enterprise_established": 0.20,
        }

    # Adoption-weighted population shares per use-case.
    # Grounded in NBER Bick/Blandin/Deming 2024, Stanford AI Index 2025,
    # McKinsey State of AI 2025. See docs/references.md.
    USE_CASE_POP_WEIGHTS = {
        "software_dev": 0.14, "content_writer": 0.08, "legal": 0.04,
        "healthcare": 0.05, "finance": 0.05, "educator": 0.07,
        "customer_service": 0.08, "researcher": 0.06, "creative": 0.06,
        "marketing": 0.07, "service_worker": 0.05, "hospital_system": 0.05,
        "enterprise_finance": 0.05, "tech_startup": 0.06,
        "enterprise_legal": 0.04, "government_agency": 0.05,
    }

    segments = []

    # Compute population fractions: use pop weights for known use-cases,
    # equal share for any custom/unknown ones, then normalize.
    raw_fractions = {}
    for uc in use_cases:
        raw_fractions[uc] = USE_CASE_POP_WEIGHTS.get(uc, 1.0 / len(use_cases))
    frac_total = sum(raw_fractions.values())
    use_case_fractions = {uc: w / frac_total for uc, w in raw_fractions.items()}

    for use_case in use_cases:
        profile = USE_CASE_PROFILES.get(use_case)
        if profile is None:
            continue

        use_case_fraction = use_case_fractions[use_case]
        consumer_type = profile.get("consumer_type", "individual")

        # Select appropriate archetype weights based on consumer type
        if consumer_type == "organization":
            archetypes_to_use = organizational_archetype_weights
        else:
            archetypes_to_use = archetype_weights

        for archetype, arch_weight in archetypes_to_use.items():
            arch_params = ARCHETYPES.get(archetype, ARCHETYPES["cautious"])
            seg_fraction = use_case_fraction * arch_weight

            # Initial provider shares from brand recognition
            shares = {}
            if brand_recognition:
                weights = [brand_recognition.get(p, 0.5) for p in provider_names]
                total = sum(weights)
                shares = {p: w / total for p, w in zip(provider_names, weights)}
            else:
                shares = {p: 1.0 / len(provider_names) for p in provider_names}

            # Get organizational parameters from profile
            decision_delay = profile.get("decision_delay", 1)
            integration_friction = profile.get("integration_friction", 0.0)
            compliance_requirements = profile.get("compliance_requirements", [])
            compliance_weight = 1.5 if consumer_type == "organization" else 1.0

            seg = MarketSegment(
                name=f"{use_case}_{archetype}",
                archetype=archetype,
                use_case=use_case,
                market_fraction=seg_fraction,
                leaderboard_trust=arch_params["leaderboard_trust"],
                switching_cost=arch_params["switching_cost"],
                switching_threshold=arch_params["switching_threshold"],
                cost_sensitivity=arch_params.get("cost_sensitivity", 0.0),
                llm_mode=False,  # Will be set by ConsumerMarket based on config
                consumer_type=consumer_type,
                decision_delay=decision_delay,
                integration_friction=integration_friction,
                compliance_requirements=compliance_requirements,
                compliance_weight=compliance_weight,
                rounds_since_decision=0,
                last_llm_decision=None,
                provider_shares=shares,
                believed_quality={},
                satisfaction={},
                tenure={p: 0 for p in provider_names},
                need_weights=profile.get("need_weights", {}),
            )
            segments.append(seg)

    return segments
