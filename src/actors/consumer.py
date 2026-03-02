"""
Consumer Market for Evaluation Ecosystem Simulation

Models the consumer market as segments rather than individuals.
Each segment = archetype × use_case (e.g., "software_dev_leaderboard_follower").

Key dynamics:
- Segments observe leaderboard rankings weighted by their use-case benchmark preferences
- Switching is tracked as proportions within each segment, not headcounts
- Satisfaction depends on true_capability (ground truth), not benchmark scores
- Gaming creates a perception gap: high weighted score but low true satisfaction
- The gap drives probabilistic switching within each segment

Visibility:
- PUBLIC: market_shares (aggregate), switching_rate
- PRIVATE: per-segment beliefs, satisfaction, provider distribution
- INVISIBLE: true_capability (held by simulation)
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
    "software_dev": {
        "label": "Software Developer",
        "benchmark_prefs": {"coding": 0.90, "reasoning": 0.08, "writing": 0.02},
        "consumer_type": "individual",
    },
    "content_writer": {
        "label": "Content Writer",
        "benchmark_prefs": {"writing": 0.90, "reasoning": 0.08, "coding": 0.02},
        "consumer_type": "individual",
    },
    "legal": {
        "label": "Legal Professional",
        "benchmark_prefs": {"reasoning": 0.75, "writing": 0.20, "safety": 0.05},
        "consumer_type": "individual",
    },
    "healthcare": {
        "label": "Healthcare Worker",
        "benchmark_prefs": {"safety": 0.75, "reasoning": 0.20, "writing": 0.05},
        "consumer_type": "individual",
    },
    "finance": {
        "label": "Finance Analyst",
        "benchmark_prefs": {"reasoning": 0.70, "safety": 0.25, "coding": 0.05},
        "consumer_type": "individual",
    },
    "educator": {
        "label": "Educator",
        "benchmark_prefs": {"writing": 0.50, "reasoning": 0.40, "safety": 0.10},
        "consumer_type": "individual",
    },
    "customer_service": {
        "label": "Customer Service",
        "benchmark_prefs": {"writing": 0.85, "reasoning": 0.12, "safety": 0.03},
        "consumer_type": "individual",
    },
    "researcher": {
        "label": "Researcher",
        "benchmark_prefs": {"reasoning": 0.50, "coding": 0.45, "writing": 0.05},
        "consumer_type": "individual",
    },
    "creative": {
        "label": "Creative Professional",
        "benchmark_prefs": {"writing": 0.85, "reasoning": 0.10, "coding": 0.05},
        "consumer_type": "individual",
    },
    "marketing": {
        "label": "Marketing Professional",
        "benchmark_prefs": {"writing": 0.75, "reasoning": 0.20, "coding": 0.05},
        "consumer_type": "individual",
    },
    "service_worker": {
        "label": "Service Worker",
        "benchmark_prefs": {"writing": 0.65, "reasoning": 0.25, "safety": 0.10},
        "consumer_type": "individual",
    },

    # Organizational consumer profiles
    "hospital_system": {
        "label": "Hospital System",
        "benchmark_prefs": {"safety": 0.65, "reasoning": 0.25, "writing": 0.10},
        "consumer_type": "organization",
        "compliance_requirements": ["HIPAA", "patient_safety"],
        "integration_friction": 0.175,
        "decision_delay": 6,
    },
    "enterprise_finance": {
        "label": "Financial Institution",
        "benchmark_prefs": {"reasoning": 0.60, "safety": 0.30, "coding": 0.10},
        "consumer_type": "organization",
        "compliance_requirements": ["SOX", "financial_reporting"],
        "integration_friction": 0.20,
        "decision_delay": 4,
    },
    "tech_startup": {
        "label": "Tech Startup",
        "benchmark_prefs": {"coding": 0.70, "reasoning": 0.25, "writing": 0.05},
        "consumer_type": "organization",
        "compliance_requirements": [],
        "integration_friction": 0.075,
        "decision_delay": 2,
    },
    "enterprise_legal": {
        "label": "Legal Organization",
        "benchmark_prefs": {"reasoning": 0.65, "writing": 0.25, "safety": 0.10},
        "consumer_type": "organization",
        "compliance_requirements": ["client_confidentiality", "data_protection"],
        "integration_friction": 0.15,
        "decision_delay": 5,
    },
    "government_agency": {
        "label": "Government Agency",
        "benchmark_prefs": {"safety": 0.50, "reasoning": 0.30, "writing": 0.20},
        "consumer_type": "organization",
        "compliance_requirements": ["security_clearance", "data_sovereignty"],
        "integration_friction": 0.225,
        "decision_delay": 8,
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
        "switching_threshold": 0.15,
        "cost_sensitivity": 0.15,  # Follows scores, not price
    },
    "experience_driven": {
        "leaderboard_trust": 0.35,
        "switching_cost": 0.08,
        "switching_threshold": 0.08,
        "cost_sensitivity": 0.30,  # Will switch for better value
    },
    "cautious": {
        "leaderboard_trust": 0.50,
        "switching_cost": 0.20,
        "switching_threshold": 0.25,
        "cost_sensitivity": 0.20,  # Weighs cost but risk-averse about quality
    },

    # Organizational archetypes
    "enterprise_cautious": {
        "leaderboard_trust": 0.25,  # Very experience-driven
        "switching_cost": 0.35,
        "switching_threshold": 0.50,
        "cost_sensitivity": 0.10,  # Enterprises care less about per-token cost
    },
    "enterprise_growth": {
        "leaderboard_trust": 0.45,
        "switching_cost": 0.25,
        "switching_threshold": 0.30,
        "cost_sensitivity": 0.15,  # Some cost awareness
    },
    "enterprise_established": {
        "leaderboard_trust": 0.35,
        "switching_cost": 0.40,
        "switching_threshold": 0.40,
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

    # Resolved benchmark weights {benchmark_name: weight}
    benchmark_weights: dict = field(default_factory=dict)

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
    rounds_since_decision: int = 0  # Track decision delay
    last_llm_decision: Optional[dict] = None  # Store LLM reasoning trace

    # Dynamic state
    provider_shares: dict = field(default_factory=dict)    # {provider: proportion}
    believed_quality: dict = field(default_factory=dict)   # {provider: quality_estimate}
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
            "provider_shares": self.provider_shares,
            "believed_quality": self.believed_quality,
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

    def resolve_benchmark_weights(self, benchmark_names: list[str]):
        """Map use-case preference categories to actual benchmark names.

        Uses substring matching: "coding_bench" matches category "coding".
        Unmatched benchmarks get a small default weight (0.1).

        For organizational consumers, applies additional upweighting (1.5x) to
        benchmarks matching their field-specific priorities.
        """
        for seg in self.segments:
            profile = USE_CASE_PROFILES.get(seg.use_case, {})
            prefs = profile.get("benchmark_prefs", {})
            weights = {}
            for bm_name in benchmark_names:
                matched = False
                for category, pref_weight in prefs.items():
                    if category.lower() in bm_name.lower():
                        weights[bm_name] = pref_weight
                        matched = True
                        break
                if not matched:
                    weights[bm_name] = 0.1  # small default weight

            # Organizational field-specific upweighting
            if seg.consumer_type == "organization":
                field_keywords = ORG_FIELD_PRIORITIES.get(seg.use_case, [])
                for bm_name in benchmark_names:
                    # Check if benchmark name contains any field-priority keyword
                    for keyword in field_keywords:
                        if keyword.lower() in bm_name.lower():
                            # Apply 1.5x multiplier to emphasize field relevance
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

                # Risk signals reduce leaderboard trust for followers
                if (media_coverage.get("risk_signals") and
                        seg.archetype == "leaderboard_follower"):
                    # Check for incident signals specifically
                    incident_signals = [
                        sig for sig in media_coverage.get("risk_signals", [])
                        if sig.startswith("incident_")
                    ]
                    if incident_signals:
                        # Reduce trust by 5% per incident signal
                        seg.leaderboard_trust *= (0.95 ** len(incident_signals))
                    # Other risk signals also reduce trust but less severely
                    other_risk_signals = [
                        sig for sig in media_coverage.get("risk_signals", [])
                        if not sig.startswith("incident_")
                    ]
                    if other_risk_signals:
                        seg.leaderboard_trust *= (0.98 ** len(other_risk_signals))

            for provider_name, composite_score in leaderboard:
                # Compute use-case-weighted perceived score from per-benchmark
                # scores if available. Falls back to composite score.
                perceived_score = composite_score

                if provider_name not in seg.believed_quality:
                    seg.believed_quality[provider_name] = perceived_score
                else:
                    old = seg.believed_quality[provider_name]
                    seg.believed_quality[provider_name] = (
                        (1 - learning_rate) * old + learning_rate * perceived_score
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

                # Risk signals reduce leaderboard trust for followers
                if (media_coverage.get("risk_signals") and
                        seg.archetype == "leaderboard_follower"):
                    # Check for incident signals specifically
                    incident_signals = [
                        sig for sig in media_coverage.get("risk_signals", [])
                        if sig.startswith("incident_")
                    ]
                    if incident_signals:
                        # Reduce trust by 5% per incident signal
                        seg.leaderboard_trust *= (0.95 ** len(incident_signals))
                    # Other risk signals also reduce trust but less severely
                    other_risk_signals = [
                        sig for sig in media_coverage.get("risk_signals", [])
                        if not sig.startswith("incident_")
                    ]
                    if other_risk_signals:
                        seg.leaderboard_trust *= (0.98 ** len(other_risk_signals))

            for provider_name, _ in leaderboard:
                # Compute weighted score based on segment's benchmark preferences
                weighted_score = 0.0
                total_weight = 0.0
                for bm_name, bm_weight in seg.benchmark_weights.items():
                    bm_scores = per_benchmark_scores.get(bm_name, {})
                    if provider_name in bm_scores:
                        weighted_score += bm_weight * bm_scores[provider_name]
                        total_weight += bm_weight
                if total_weight > 0:
                    perceived_score = weighted_score / total_weight
                else:
                    # Fallback to composite
                    perceived_score = next(
                        (s for n, s in leaderboard if n == provider_name), 0.5
                    )

                if provider_name not in seg.believed_quality:
                    seg.believed_quality[provider_name] = perceived_score
                else:
                    old = seg.believed_quality[provider_name]
                    seg.believed_quality[provider_name] = (
                        (1 - learning_rate) * old + learning_rate * perceived_score
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
            provider_strategies: {provider_name: {fundamental_research, ...}}
            published_scores: {provider_name: composite_score}
            media_coverage: Media coverage dict with sentiment and provider_attention
        """
        for seg in self.segments:
            for provider_name in self.provider_names:
                if provider_name not in ground_truth:
                    continue

                gt = ground_truth[provider_name]
                true_capability = gt.true_capability

                # Base satisfaction: use-case weighted perceived quality
                # This is what the segment actually experiences in their domain
                base_satisfaction = seg.believed_quality.get(provider_name, true_capability)

                # If no believed_quality yet (early rounds), use true_capability
                if provider_name not in seg.believed_quality:
                    base_satisfaction = true_capability

                # Factor 1: Gaming Detection Penalty
                # If score >> true_capability, consumer experiences disappointment
                # (high scores attracted them, but actual performance disappoints)
                gaming_penalty = 0.0
                if published_scores and provider_name in published_scores:
                    score = published_scores[provider_name]
                    gap = max(0, score - true_capability)
                    gaming_penalty = 0.20 * gap  # 20% penalty per unit of inflation

                # Factor 2: Safety Alignment Match
                # Segments with high safety preferences value safety investment
                # Organizational consumers weight compliance/safety more heavily
                safety_bonus = 0.0
                if provider_strategies and provider_name in provider_strategies:
                    strategy = provider_strategies[provider_name]
                    safety_investment = strategy.get("safety_alignment", 0.0)
                    # Get segment's safety preference weight
                    safety_pref = 0.0
                    for cat, weight in USE_CASE_PROFILES.get(seg.use_case, {}).get("benchmark_prefs", {}).items():
                        if "safety" in cat.lower():
                            safety_pref = weight
                            break
                    # Bonus scales with both provider investment and segment preference
                    # Apply compliance_weight multiplier for organizations
                    safety_bonus = 0.12 * safety_investment * safety_pref * seg.compliance_weight

                # Factor 3: Media Sentiment Influence
                # Negative media coverage reduces satisfaction beyond objective metrics
                media_penalty = 0.0
                if media_coverage:
                    sentiment = media_coverage.get("sentiment", 0.0)
                    provider_attention = media_coverage.get("provider_attention", {}).get(provider_name, 0.0)
                    # Only negative sentiment creates penalty
                    if sentiment < 0:
                        media_penalty = 0.10 * abs(sentiment) * provider_attention

                # Factor 4: Incident History Penalty
                # Recent safety incidents reduce trust and satisfaction
                incident_penalty = 0.0
                if incident_history and provider_name in incident_history and round_num is not None:
                    provider_incidents = incident_history[provider_name]
                    # Focus on recent incidents (last 5 rounds)
                    recent_incidents = [
                        inc for inc in provider_incidents
                        if inc.round_num >= round_num - 5
                    ]
                    # Weight by severity
                    severity_weights = {"minor": 0.02, "moderate": 0.08, "major": 0.15, "critical": 0.30}
                    for inc in recent_incidents:
                        weight = severity_weights.get(inc.severity, 0.05)
                        # Extra penalty if incident affects this segment's sector
                        if seg.use_case in inc.affected_sectors or seg.consumer_type in inc.affected_sectors:
                            weight *= 2.0  # Double penalty for sector-specific incidents
                        incident_penalty += weight

                # Factor 5: Cost Efficiency Bonus
                # Open-source providers offer lower cost; price-sensitive segments benefit
                cost_bonus = 0.0
                if provider_cost_advantage and provider_name in provider_cost_advantage:
                    cost_eff = provider_cost_advantage[provider_name]
                    cost_bonus = seg.cost_sensitivity * cost_eff * 0.15

                # Compute final satisfaction
                satisfaction = (
                    base_satisfaction
                    - gaming_penalty
                    + safety_bonus
                    - media_penalty
                    - incident_penalty
                    + cost_bonus
                )

                # Clamp to [0, 1]
                seg.satisfaction[provider_name] = max(0.0, min(1.0, satisfaction))

    def compute_switching(self, ground_truth: Optional[dict] = None,
                         provider_strategies: Optional[dict] = None,
                         published_scores: Optional[dict] = None,
                         media_coverage: Optional[dict] = None,
                         policymaker_data: Optional[dict] = None,
                         incident_history: Optional[dict] = None,
                         per_benchmark_scores: Optional[dict] = None,
                         provider_cost_advantage: Optional[dict] = None,
                         deployer_liability_guidance: Optional[set] = None):
        """Compute switching proportions within each segment.

        Two triggers (same logic as original Consumer, but applied proportionally):
        1. Dissatisfaction: believed quality > actual satisfaction by > threshold
        2. Opportunity: a better alternative exceeds switching cost + tenure bonus

        Args:
            ground_truth: {provider_name: ProviderGroundTruth} - for LLM context
            provider_strategies: {provider_name: strategy_dict} - for LLM context
            published_scores: {provider_name: score} - for LLM context
            media_coverage: Media coverage dict - for LLM context
            policymaker_data: Policymaker data dict - for LLM context

        Returns:
            Total switching rate (fraction of total market that switched)
        """
        total_switching = 0.0

        # Track per-segment switching for analysis
        segment_switching_rates = {}

        for seg in self.segments:
            # Organizations decide less frequently
            if seg.consumer_type == "organization":
                seg.rounds_since_decision += 1
                if seg.rounds_since_decision < seg.decision_delay:
                    segment_switching_rates[seg.name] = 0.0
                    continue  # Skip this round, not time to decide yet
                seg.rounds_since_decision = 0  # Reset counter

            # Branch on reasoning mode
            if seg.llm_mode:
                seg_switching = self._compute_switching_llm(
                    seg, ground_truth, provider_strategies, published_scores,
                    media_coverage, policymaker_data, incident_history, per_benchmark_scores,
                    provider_cost_advantage, deployer_liability_guidance
                )
            else:
                seg_switching = self._compute_switching_heuristic(seg)

            total_switching += seg_switching * seg.market_fraction
            segment_switching_rates[seg.name] = seg_switching

        # Store for later retrieval
        self._last_segment_switching = segment_switching_rates

        return total_switching

    def _compute_switching_heuristic(self, seg: MarketSegment) -> float:
        """Compute heuristic-based switching for a segment.

        Returns:
            Switching rate for this segment
        """
        seg_switching = 0.0

        for provider in list(seg.provider_shares.keys()):
                share = seg.provider_shares.get(provider, 0.0)
                if share < 0.001:  # skip negligible shares
                    continue

                # Apply integration friction for organizations
                effective_switching_cost = seg.switching_cost + seg.integration_friction

                tenure_bonus = min(0.1, seg.tenure.get(provider, 0) * 0.02)
                should_switch_prob = 0.0
                best_alternative = None
                best_alt_score = -1.0

                # --- Trigger 1: Dissatisfaction ---
                believed = seg.believed_quality.get(provider, 0.5)
                actual_sat = seg.satisfaction.get(provider, 0.5)
                gap = believed - actual_sat

                threshold = seg.switching_threshold + tenure_bonus + effective_switching_cost
                if gap > 0:
                    # Sigmoid-based probability: smooth transition
                    should_switch_prob = max(
                        should_switch_prob,
                        _switching_probability(gap, threshold),
                    )

                # --- Trigger 2: Better alternative ---
                current_blended = self._blended_score(seg, provider)
                opportunity_threshold = effective_switching_cost + tenure_bonus

                for alt_provider in self.provider_names:
                    if alt_provider == provider:
                        continue
                    alt_blended = self._blended_score(seg, alt_provider)
                    improvement = alt_blended - current_blended
                    if improvement > 0:
                        # Open-source providers are free to try — halve the switching threshold
                        alt_threshold = opportunity_threshold
                        if alt_provider in self.open_source_providers:
                            alt_threshold = opportunity_threshold * 0.5
                        opp_prob = _switching_probability(
                            improvement, alt_threshold
                        )
                        if opp_prob > should_switch_prob:
                            should_switch_prob = opp_prob
                        if alt_blended > best_alt_score:
                            best_alt_score = alt_blended
                            best_alternative = alt_provider

                # Apply switching
                if should_switch_prob > 0.01 and best_alternative:
                    switching_fraction = should_switch_prob * share
                    switching_fraction = min(switching_fraction, share)  # can't exceed current share

                    seg.provider_shares[provider] -= switching_fraction
                    seg.provider_shares[best_alternative] = (
                        seg.provider_shares.get(best_alternative, 0.0) + switching_fraction
                    )
                    seg_switching += switching_fraction

                    # Reset tenure for switchers
                    seg.tenure[provider] = max(0, seg.tenure.get(provider, 0) - 1)

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

    def _compute_switching_llm(self, seg: MarketSegment, ground_truth: Optional[dict],
                               provider_strategies: Optional[dict],
                               published_scores: Optional[dict],
                               media_coverage: Optional[dict],
                               policymaker_data: Optional[dict],
                               incident_history: Optional[dict] = None,
                               per_benchmark_scores: Optional[dict] = None,
                               provider_cost_advantage: Optional[dict] = None,
                               deployer_liability_guidance: Optional[set] = None) -> float:
        """Compute LLM-based switching decisions for a segment.

        Args:
            seg: Market segment
            ground_truth: Ground truth data
            provider_strategies: Provider strategies
            published_scores: Published scores
            media_coverage: Media coverage
            policymaker_data: Policymaker data

        Returns:
            Switching rate for this segment
        """
        from llm import call_llm
        import json as json_module

        seg_switching = 0.0

        for provider in list(seg.provider_shares.keys()):
            share = seg.provider_shares.get(provider, 0.0)
            if share < 0.001:  # skip negligible shares
                continue

            # Build decision context
            context = self._build_decision_context(
                seg, provider, ground_truth, provider_strategies,
                published_scores, media_coverage, policymaker_data,
                incident_history, per_benchmark_scores, provider_cost_advantage,
                deployer_liability_guidance
            )

            # Build prompt based on consumer type
            if seg.consumer_type == "organization":
                prompt = self._build_organizational_prompt(seg, provider, context)
            else:
                prompt = self._build_individual_prompt(seg, provider, context)

            # Call LLM
            try:
                response = call_llm(prompt, temperature=0.7, max_tokens=500)

                # Parse JSON response
                decision = json_module.loads(response)
                should_switch = decision.get("should_switch", False)
                target_provider = decision.get("target_provider")
                confidence = decision.get("confidence", 0.5)
                reasoning = decision.get("reasoning", "")

                # Store decision trace
                seg.last_llm_decision = {
                    "provider": provider,
                    "decision": decision,
                    "round": self.current_round,
                }

                # Apply switching based on LLM decision
                if should_switch and target_provider and target_provider in self.provider_names:
                    switching_fraction = confidence * share
                    switching_fraction = min(switching_fraction, share)

                    seg.provider_shares[provider] -= switching_fraction
                    seg.provider_shares[target_provider] = (
                        seg.provider_shares.get(target_provider, 0.0) + switching_fraction
                    )
                    seg_switching += switching_fraction

                    # Reset tenure for switchers
                    seg.tenure[provider] = max(0, seg.tenure.get(provider, 0) - 1)

            except Exception as e:
                # Fallback to heuristic if LLM fails
                print(f"[ConsumerMarket] LLM decision failed for {seg.name}/{provider}: {e}")
                # Use heuristic logic as fallback
                pass

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

    def _build_decision_context(self, seg: MarketSegment, provider: str,
                                ground_truth: Optional[dict],
                                provider_strategies: Optional[dict],
                                published_scores: Optional[dict],
                                media_coverage: Optional[dict],
                                policymaker_data: Optional[dict],
                                incident_history: Optional[dict] = None,
                                per_benchmark_scores: Optional[dict] = None,
                                provider_cost_advantage: Optional[dict] = None,
                                deployer_liability_guidance: Optional[set] = None) -> dict:
        """Build context dictionary for LLM decision-making."""
        context = {
            "satisfaction": seg.satisfaction.get(provider, 0.5),
            "believed_quality": seg.believed_quality.get(provider, 0.5),
            "tenure": seg.tenure.get(provider, 0),
            "alternatives": [],
            "cost_advantage": provider_cost_advantage or {},
            "deployer_liability_guidance": deployer_liability_guidance or set(),
        }

        # Provider safety alignment (from strategies)
        if provider_strategies:
            context["provider_safety"] = {
                p: strat.get("safety_alignment", 0.0)
                for p, strat in provider_strategies.items()
            }

        # Per-benchmark scores for this provider and alternatives
        if per_benchmark_scores:
            context["per_benchmark_scores"] = per_benchmark_scores

        # Build alternatives list (include safety, benchmark scores, and cost_advantage)
        cost_adv = provider_cost_advantage or {}
        for alt_provider in self.provider_names:
            if alt_provider == provider:
                continue
            alt_data = {
                "name": alt_provider,
                "believed_quality": seg.believed_quality.get(alt_provider, 0.5),
                "satisfaction": seg.satisfaction.get(alt_provider, 0.0),
                "score": published_scores.get(alt_provider, 0.5) if published_scores else 0.5,
                "safety": provider_strategies.get(alt_provider, {}).get("safety_alignment", 0.0)
                          if provider_strategies else 0.0,
                "cost_advantage": cost_adv.get(alt_provider, 0.0),
            }
            context["alternatives"].append(alt_data)
        # Also store current provider's cost_advantage in context
        context["current_cost_advantage"] = cost_adv.get(provider, 0.0)

        # Sort alternatives by believed quality
        context["alternatives"].sort(key=lambda x: x["believed_quality"], reverse=True)

        # Add media context
        if media_coverage:
            context["media_sentiment"] = media_coverage.get("sentiment", 0.0)
            context["media_headlines"] = media_coverage.get("headlines", [])
            context["provider_attention"] = media_coverage.get("provider_attention", {}).get(provider, 0.0)
            context["risk_signals"] = media_coverage.get("risk_signals", [])

        # Add regulatory context
        if policymaker_data:
            context["regulatory_pressure"] = len(policymaker_data.get("interventions", []))
            context["regulatory_interventions"] = [
                iv.get("type", "unknown") for iv in policymaker_data.get("interventions", [])
            ]

        # Add incident history for current provider and alternatives
        if incident_history:
            # Recent incidents (last 10 rounds) for current provider
            provider_incs = incident_history.get(provider, [])
            context["provider_incidents"] = [
                {
                    "severity": inc.severity,
                    "category": inc.category,
                    "description": inc.description,
                    "round": inc.round_num,
                }
                for inc in provider_incs[-5:]  # Last 5 incidents
            ]
            # Incident counts per provider (summary for alternatives)
            context["incident_counts"] = {
                p: len(incs) for p, incs in incident_history.items()
            }
            # Severity breakdown for current provider
            sev_counts = {"minor": 0, "moderate": 0, "major": 0, "critical": 0}
            for inc in provider_incs:
                sev_counts[inc.severity] = sev_counts.get(inc.severity, 0) + 1
            context["provider_incident_severity"] = sev_counts

        return context

    def _build_individual_prompt(self, seg: MarketSegment, provider: str, context: dict) -> str:
        """Build LLM prompt for individual consumer decision."""
        use_case_label = USE_CASE_PROFILES.get(seg.use_case, {}).get("label", seg.use_case)

        current_cost = context.get("current_cost_advantage", 0.0)
        cost_adv = context.get("cost_advantage", {})
        include_cost = seg.cost_sensitivity >= 0.10  # Only surface cost for price-sensitive individuals

        alternatives_text = "\n".join([
            f"  - {alt['name']}: quality {alt['believed_quality']:.2f}, score {alt['score']:.2f}"
            + (f", cost_advantage {alt.get('cost_advantage', 0.0):.2f}" if include_cost else "")
            for alt in context["alternatives"][:3]
        ])

        media_text = ""
        if "media_headlines" in context and context["media_headlines"]:
            headlines = context["media_headlines"][:3]
            media_text = f"\n**Recent News:**\n" + "\n".join([f"  - {h}" for h in headlines])

        cost_text = ""
        if include_cost:
            cost_text = f"\n- Price sensitivity: {seg.cost_sensitivity:.2f} (higher = more budget-conscious)\n- Current provider cost_advantage: {current_cost:.2f} (0=expensive, 1=cheapest)"

        prompt = f"""You are a {use_case_label} who uses AI models for your work.

**Current Situation:**
- Provider: {provider}
- Your satisfaction: {context['satisfaction']:.2f}/1.0
- Your believed quality: {context['believed_quality']:.2f}/1.0
- Tenure: {context['tenure']} rounds

**Alternatives:**
{alternatives_text}

**Your Decision Style:**
- Leaderboard trust: {seg.leaderboard_trust:.0%}
- Switching cost: {seg.switching_cost}{cost_text}
{media_text}

Should you switch providers? Consider:
1. Is your current satisfaction meeting your needs?
2. Are there significantly better alternatives?
3. Is the improvement worth the switching cost?{"" if not include_cost else chr(10) + "4. Does a cheaper alternative offer sufficient quality for your budget?"}

Output ONLY valid JSON with this structure:
{{"should_switch": true/false, "target_provider": "name" or null, "confidence": 0.0-1.0, "reasoning": "brief explanation"}}"""

        return prompt

    def _build_organizational_prompt(self, seg: MarketSegment, provider: str, context: dict) -> str:
        """Build LLM prompt for organizational consumer decision."""
        use_case_label = USE_CASE_PROFILES.get(seg.use_case, {}).get("label", seg.use_case)

        compliance_text = ", ".join(seg.compliance_requirements) if seg.compliance_requirements else "None"

        # Current provider safety vs alternatives
        provider_safety = context.get("provider_safety", {})
        current_safety = provider_safety.get(provider, 0.0)
        current_cost = context.get("current_cost_advantage", 0.0)
        alt_safety_lines = []
        for alt in context["alternatives"][:4]:
            alt_name = alt["name"]
            alt_saf = provider_safety.get(alt_name, alt.get("safety", 0.0))
            alt_cost = alt.get("cost_advantage", 0.0)
            inc_count = context.get("incident_counts", {}).get(alt_name, 0)
            liability_flag = " [DEPLOYER LIABILITY ACTIVE]" if alt.get("deployer_liability") else ""
            alt_safety_lines.append(
                f"  - {alt_name}: quality {alt['believed_quality']:.2f}, "
                f"score {alt['score']:.2f}, safety {alt_saf:.2f}, "
                f"cost_advantage {alt_cost:.2f}, incidents {inc_count}{liability_flag}"
            )
        alternatives_text = "\n".join(alt_safety_lines) if alt_safety_lines else "  (none)"

        # Per-benchmark scores for org-relevant benchmarks
        per_bm = context.get("per_benchmark_scores", {})
        benchmark_lines = []
        if per_bm:
            for bm_name, scores in per_bm.items():
                cur_score = scores.get(provider, None)
                if cur_score is not None:
                    top_alt = max(
                        ((p, s) for p, s in scores.items() if p != provider),
                        key=lambda x: x[1], default=(None, None)
                    )
                    leader_note = f" (leader: {top_alt[0]} {top_alt[1]:.2f})" if top_alt[0] else ""
                    benchmark_lines.append(f"  - {bm_name}: {cur_score:.3f}{leader_note}")
        benchmark_text = "\n".join(benchmark_lines) if benchmark_lines else "  (not available)"

        # Incident history for current provider
        incident_lines = []
        provider_incidents = context.get("provider_incidents", [])
        if provider_incidents:
            sev_counts = context.get("provider_incident_severity", {})
            incident_lines.append(
                f"  Current vendor safety record: "
                f"minor={sev_counts.get('minor',0)}, "
                f"moderate={sev_counts.get('moderate',0)}, "
                f"major={sev_counts.get('major',0)}, "
                f"critical={sev_counts.get('critical',0)}"
            )
            for inc in provider_incidents[-3:]:  # Last 3 incidents
                incident_lines.append(
                    f"  - [{inc['severity'].upper()}] Round {inc['round']}: {inc['description']}"
                )
        else:
            incident_lines.append(f"  {provider}: no reported incidents")
        incident_text = "\n".join(incident_lines)

        # Media intelligence
        media_text = ""
        if "media_headlines" in context and context["media_headlines"]:
            headlines = context["media_headlines"][:3]
            media_text = "\n**Market Intelligence (Media):**\n" + "\n".join([f"  - {h}" for h in headlines])
            if "media_sentiment" in context:
                sentiment_label = "positive" if context["media_sentiment"] > 0.1 else \
                                  "negative" if context["media_sentiment"] < -0.1 else "neutral"
                media_text += f"\n  Sector sentiment: {context['media_sentiment']:.2f} ({sentiment_label})"
            risk_signals = context.get("risk_signals", [])
            if risk_signals:
                media_text += f"\n  Risk signals: {', '.join(risk_signals[:5])}"

        # Regulatory context
        regulatory_text = ""
        if "regulatory_pressure" in context and context["regulatory_pressure"] > 0:
            interventions = context.get("regulatory_interventions", [])
            regulatory_text = (
                f"\n**Regulatory Environment:**\n"
                f"  Active interventions: {context['regulatory_pressure']}\n"
                f"  Types: {', '.join(set(interventions)) if interventions else 'general oversight'}"
            )

        # Deployer liability warning for open-source providers
        liability_guidance = context.get("deployer_liability_guidance", set())
        liability_text = ""
        if provider in liability_guidance:
            liability_text = (
                f"\n**REGULATORY ALERT: Deployer Liability Guidance Active**\n"
                f"  Regulators have issued guidance stating that organizations deploying {provider} "
                f"(open-source) assume FULL liability for safety incidents, compliance failures, and "
                f"regulatory breaches — with no recourse against the model provider.\n"
                f"  Your legal and compliance teams must factor this into vendor risk assessment."
            )
        # Flag alternatives that are under liability guidance
        for alt in context.get("alternatives", []):
            if alt["name"] in liability_guidance:
                alt["deployer_liability"] = True

        # Cost sensitivity label for the prompt
        cost_sens = seg.cost_sensitivity
        if cost_sens >= 0.20:
            cost_label = "HIGH — budget pressure is a primary constraint; cost savings can justify capability tradeoffs"
        elif cost_sens >= 0.10:
            cost_label = "MODERATE — cost matters but capability and safety take precedence"
        else:
            cost_label = "LOW — performance and reliability dominate; pricing is secondary"

        prompt = f"""You are the decision-making committee for a {use_case_label} organization evaluating AI vendor relationships.

**Current Vendor: {provider}**
- Organizational satisfaction: {context['satisfaction']:.2f}/1.0
- Believed quality: {context['believed_quality']:.2f}/1.0
- Safety investment: {current_safety:.2f}/1.0
- Cost advantage: {current_cost:.2f}/1.0 (0=most expensive, 1=cheapest)
- Contract tenure: {context['tenure']} quarters

**Alternative Vendors (quality / score / safety / cost_advantage / incidents):**
{alternatives_text}

**Benchmark Performance (current vendor vs. market leader):**
{benchmark_text}

**Safety & Incident Record:**
{incident_text}

**Organizational Constraints:**
- Compliance requirements: {compliance_text}
- Integration friction: {seg.integration_friction:.0%} (migration cost)
- Decision cadence: Review every {seg.decision_delay} quarters
- Stakeholder risk tolerance: {seg.switching_threshold}
- Cost sensitivity: {cost_label}
{media_text}
{regulatory_text}
{liability_text}

**Decision Framework:**
1. Safety & Compliance: Does the vendor's incident record and safety investment meet our risk standards?
2. Performance: Are benchmark scores and satisfaction sufficient for our use case?
3. Cost vs Capability Tradeoff: Given our cost sensitivity ({cost_sens:.2f}), weigh whether a cheaper alternative's cost_advantage justifies any capability gap, or whether a more expensive provider's quality premium is worth it.
4. Deployer Liability: If active liability guidance applies to the current or alternative vendor, factor in the legal and compliance risk your organization bears.
5. Migration Cost: Do the benefits (capability or cost) justify switching given integration friction?
6. Strategic Alignment: Long-term vendor stability, regulatory standing, and mission fit?

Reason through this decision as an organizational committee. For a {use_case_label} with {cost_label.split('—')[0].strip()} cost sensitivity, explicitly weigh the cost-capability tradeoff and any liability exposure before deciding.

Output ONLY valid JSON with this structure:
{{"should_switch": true/false, "target_provider": "name" or null, "confidence": 0.0-1.0, "reasoning": "committee decision rationale covering safety, performance, cost tradeoff, and compliance"}}"""

        return prompt

    def _blended_score(self, seg: MarketSegment, provider: str) -> float:
        """Compute blended perceived quality for a provider within a segment."""
        trust = seg.leaderboard_trust
        believed = seg.believed_quality.get(provider, 0.5)
        actual_sat = seg.satisfaction.get(provider, 0.5)
        # Blend leaderboard-derived belief with actual experience
        return trust * believed + (1 - trust) * actual_sat

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
                decision = seg.last_llm_decision
                org_llm_decisions[seg.name] = {
                    "provider": decision.get("provider"),
                    "round": decision.get("round"),
                    "should_switch": decision.get("decision", {}).get("should_switch"),
                    "target_provider": decision.get("decision", {}).get("target_provider"),
                    "confidence": decision.get("decision", {}).get("confidence"),
                    "reasoning": decision.get("decision", {}).get("reasoning", ""),
                    "use_case": seg.use_case,
                    "archetype": seg.archetype,
                }

        return {
            "market_shares": market_shares,
            "provider_satisfaction": provider_satisfaction,
            "avg_satisfaction": avg_satisfaction,
            "switching_rate": 0.0,  # set by caller after compute_switching()
            "segment_data": segment_data,
            "org_llm_decisions": org_llm_decisions,
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

    segments = []
    n_use_cases = len(use_cases)

    for use_case in use_cases:
        profile = USE_CASE_PROFILES.get(use_case)
        if profile is None:
            continue

        use_case_fraction = 1.0 / n_use_cases
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
            )
            segments.append(seg)

    return segments


# ============================================================
#  Deprecated: Individual Consumer (kept for loading old experiments)
# ============================================================

class Consumer:
    """DEPRECATED: Individual consumer model. Kept for loading old experiments.

    New code should use ConsumerMarket + MarketSegment instead.
    """

    def __init__(self, name, use_cases=None, budget=100.0,
                 quality_sensitivity=0.5, switching_threshold=0.3,
                 leaderboard_trust=0.7, switching_cost=0.1, llm_mode=False):
        from visibility import PublicState, ConsumerPrivateState
        self.public_state = PublicState(name=name, current_round=0, published_scores=[])
        self.private_state = ConsumerPrivateState(
            use_cases=use_cases or ["general"],
            budget=budget,
            current_subscription=None,
            believed_model_quality={},
            satisfaction_history=[],
            subscription_history=[],
            leaderboard_trust=leaderboard_trust,
            switching_cost=switching_cost,
        )
        self.quality_sensitivity = quality_sensitivity
        self.switching_threshold = switching_threshold
        self.llm_mode = llm_mode
        self.memory = []
        self._last_leaderboard = []
        self._brand_recognition = {}

    @property
    def name(self):
        return self.public_state.name

    def observe(self, leaderboard, round_num):
        self.public_state.current_round = round_num
        self._last_leaderboard = leaderboard
        for provider_name, score in leaderboard:
            if provider_name not in self.private_state.believed_model_quality:
                self.private_state.believed_model_quality[provider_name] = score
            else:
                lr = 0.3
                old = self.private_state.believed_model_quality[provider_name]
                self.private_state.believed_model_quality[provider_name] = (1 - lr) * old + lr * score
        self.memory.append({"type": "observation", "round": round_num, "leaderboard": leaderboard})

    def reflect(self):
        if not self.private_state.satisfaction_history:
            return
        recent = self.private_state.satisfaction_history[-3:]
        current_sub = self.private_state.current_subscription
        if not current_sub:
            return
        recent_with_current = [sat for _, provider, sat in recent if provider == current_sub]
        if recent_with_current:
            avg_sat = sum(recent_with_current) / len(recent_with_current)
            expected = self.private_state.believed_model_quality.get(current_sub, 0.5)
            self.private_state.believed_model_quality[current_sub] = 0.6 * expected + 0.4 * avg_sat

    def plan(self):
        return self._plan_heuristic()

    def _plan_heuristic(self):
        current_sub = self.private_state.current_subscription
        should_switch = False
        switch_reason = ""
        if current_sub and self._last_leaderboard:
            tenure_bonus = min(0.1, self.private_state.rounds_with_provider * 0.02)
            if self.private_state.satisfaction_history:
                recent = [sat for _, provider, sat in self.private_state.satisfaction_history[-3:]
                          if provider == current_sub]
                if recent:
                    avg_sat = sum(recent) / len(recent)
                    lb_exp = next((s for n, s in self._last_leaderboard if n == current_sub), None)
                    if lb_exp is None:
                        lb_exp = self.private_state.believed_model_quality.get(current_sub, 0.5)
                    gap = lb_exp - avg_sat
                    threshold = self.switching_threshold + tenure_bonus + self.private_state.switching_cost
                    if gap > threshold:
                        should_switch = True
                        switch_reason = f"dissatisfied: gap={gap:.3f} > threshold={threshold:.3f}"
            if not should_switch:
                current_lb = next((s for n, s in self._last_leaderboard if n == current_sub), None)
                if current_lb is not None:
                    trust = self.private_state.leaderboard_trust
                    br = self._brand_recognition.get(current_sub, 0.5)
                    cur_believed = self.private_state.believed_model_quality.get(current_sub, current_lb * br)
                    cur_blended = trust * current_lb + (1 - trust) * cur_believed
                    opp_threshold = self.private_state.switching_cost + tenure_bonus
                    for name, score in self._last_leaderboard:
                        if name == current_sub:
                            continue
                        alt_br = self._brand_recognition.get(name, 0.5)
                        alt_believed = self.private_state.believed_model_quality.get(name, score * alt_br)
                        alt_blended = trust * score + (1 - trust) * alt_believed
                        if alt_blended - cur_blended > opp_threshold:
                            should_switch = True
                            switch_reason = f"better option: {name}"
                            break
        if should_switch or current_sub is None:
            if not self._last_leaderboard:
                return None
            best_score = -1
            best = None
            for pn, lbs in self._last_leaderboard:
                trust = self.private_state.leaderboard_trust
                br = self._brand_recognition.get(pn, 0.5)
                believed = self.private_state.believed_model_quality.get(pn, lbs * br)
                blended = trust * lbs + (1 - trust) * believed
                if blended > best_score:
                    best_score = blended
                    best = pn
            self.memory.append({"type": "planning", "round": self.public_state.current_round,
                                "decision": "switch" if current_sub else "subscribe",
                                "provider": best, "from": current_sub, "reason": switch_reason or "initial"})
            return best
        self.memory.append({"type": "planning", "round": self.public_state.current_round,
                            "decision": "stay", "provider": current_sub, "reason": "satisfied"})
        return current_sub

    def execute(self, new_subscription=None):
        if new_subscription is None:
            new_subscription = self.plan()
        old_sub = self.private_state.current_subscription
        if old_sub != new_subscription:
            self.memory.append({"type": "subscription_change", "round": self.public_state.current_round,
                                "from": old_sub, "to": new_subscription})
        self.private_state.current_subscription = new_subscription
        if new_subscription:
            self.private_state.subscription_history.append((self.public_state.current_round, new_subscription))

    def receive_satisfaction(self, satisfaction):
        current_sub = self.private_state.current_subscription
        if current_sub:
            self.private_state.satisfaction_history.append(
                (self.public_state.current_round, current_sub, satisfaction))

    def save(self, folder):
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, "public_state.json"), "w") as f:
            json.dump(self.public_state.to_dict(), f, indent=2)
        with open(os.path.join(folder, "private_state.json"), "w") as f:
            json.dump(self.private_state.to_dict(), f, indent=2)
        with open(os.path.join(folder, "memory.json"), "w") as f:
            json.dump(self.memory, f, indent=2)

    def __repr__(self):
        return f"Consumer(name='{self.name}', subscription='{self.private_state.current_subscription}')"
