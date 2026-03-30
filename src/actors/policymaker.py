"""
Policymaker Actor for Evaluation Ecosystem Simulation

Represents a regulator who can mandate evaluations, set requirements,
and respond to incidents in the AI ecosystem.

Key dynamics:
- Policymakers observe leaderboard, consumer satisfaction, and incidents
- They can issue regulations that change benchmark behavior
- Their interventions create constraints for providers
- They respond to signs of gaming (validity correlation dropping)

Visibility:
- PUBLIC: name, active_regulations, public_statements
- PRIVATE: policy_objectives, risk_beliefs, regulatory_capacity
- INVISIBLE: true_risk_tolerance, true_intervention_effectiveness
"""
import json
import os
from dataclasses import dataclass, field
from typing import Optional

from visibility import PublicState, PolicymakerPrivateState, PolicymakerGroundTruth


class Policymaker:
    """
    A Policymaker agent in the evaluation ecosystem simulation.

    Policymakers are regulators who:
    1. Observe ecosystem state (leaderboard, consumer satisfaction, validity)
    2. Assess risks and identify problems
    3. Issue regulations to change provider/evaluator behavior
    4. Monitor compliance and outcomes

    This creates regulatory pressure: if gaming becomes apparent,
    policymakers can mandate changes that affect provider strategies.

    Visibility Model:
    - public_state: Visible to all (name, regulations, statements)
    - private_state: Visible only to self (objectives, beliefs, capacity)
    - ground_truth: Held by simulation (true effectiveness)
    """

    def __init__(
        self,
        name: str,
        policy_objectives: list[str] = None,
        intervention_threshold: float = 0.3,
        risk_tolerance: float = 0.5,
        llm_mode: bool = False,
        # Enforcement calibration parameters (vary by regulatory style)
        intervention_cooldown: int = 3,          # Rounds between interventions (EU=2, US=5)
        sanction_fine_multiplier: float = 0.30,  # Base multiplier in fine formula (EU=0.35, US=0.10)
        sanction_incident_threshold: int = 2,    # Min major/critical incidents for Condition 2 (EU=2, US=4)
        sanction_duration: int = 3,              # Rounds a sanction lasts (EU=4, US=2)
        mandate_risk_threshold: float = 0.60,    # Risk level required to trigger benchmark mandate (EU=0.50, US=0.75)
        sanction_min_severity: str = "major",    # Min incident severity for Condition 2 (EU="major", US="critical")
        capability_shift: float = 0.0,           # Shift applied to absolute capability thresholds
    ):
        """
        Initialize a Policymaker.

        Args:
            name: Unique identifier for this policymaker
            policy_objectives: List of objectives (e.g., ["safety", "fairness"])
            intervention_threshold: How much concern before intervening (0-1)
            risk_tolerance: How much risk is acceptable (0-1)
            llm_mode: If True, use LLM for decision-making
        """
        # Initialize public state
        self.public_state = PublicState(
            name=name,
            current_round=0,
            published_scores=[],  # Reused for public statements
        )

        # Initialize private state
        self.private_state = PolicymakerPrivateState(
            policy_objectives=policy_objectives or ["safety", "fairness"],
            risk_beliefs={
                "score_reliability_risk": 0.3,  # Belief about score-satisfaction divergence (Goodhart)
                "consumer_harm_risk": 0.3,  # Belief about consumer harm
                "validity_degradation_risk": 0.3,  # Belief about benchmark validity loss
            },
            industry_trust=0.5,
            regulatory_capacity=1.0,
            past_interventions=[],
            observed_incidents=[],
        )

        # Policymaker-specific parameters
        self.intervention_threshold = intervention_threshold
        self.risk_tolerance = risk_tolerance
        self.llm_mode = llm_mode

        # Enforcement calibration parameters
        self.intervention_cooldown = intervention_cooldown
        self.sanction_fine_multiplier = sanction_fine_multiplier
        self.sanction_incident_threshold = sanction_incident_threshold
        self.sanction_duration = sanction_duration
        self.mandate_risk_threshold = mandate_risk_threshold
        self.sanction_min_severity = sanction_min_severity
        self._capability_shift = capability_shift

        # Memory
        self.memory = []

        # Tracking
        self._last_validity_correlation: Optional[float] = None
        self._last_consumer_satisfaction: Optional[float] = None
        self._last_market_shares: Optional[dict] = None  # {provider: share}

        # Tier 1 Enhancement: Regulatory thresholds
        self.market_concentration_threshold: float = 0.75  # Trigger antitrust at 75% share
        self.market_monitoring_threshold: float = 0.60  # Start monitoring at 60% share

        # Tier 1 Enhancement: Threshold announcements (public)
        self.announced_thresholds: dict = {}  # {threshold_type: value}

        # Tier 1 Enhancement: Information request tracking
        self._pending_information_requests: dict = {}  # {provider: {round, type, deadline}}

        # Tier 2: Active sanctions tracking
        self._active_sanctions: dict = {}
        # Format: {provider_name: {"fine_amount": float, "expires_round": int, "reason": str}}

        # Open-source provider names (exempt from market concentration reviews and sanctions)
        self._open_source_providers: set = set()

        # Deployer liability guidance: OS providers for which guidance has been issued
        self._active_liability_guidance: set = set()

    @property
    def name(self) -> str:
        return self.public_state.name

    def _detect_score_volatility(self) -> bool:
        """Detect suspicious score spikes (possible gaming signal)."""
        # Check if any provider's score jumped more than 0.1 in one round
        if len(self.memory) < 2:
            return False
        recent_obs = [m for m in self.memory if m.get("type") == "observation"]
        if len(recent_obs) < 2:
            return False
        # Compare leaderboard from last two observations
        last = recent_obs[-1]
        prev = recent_obs[-2]
        last_scores = {name: score for name, score in last.get("leaderboard", [])}
        prev_scores = {name: score for name, score in prev.get("leaderboard", [])}
        for name in last_scores:
            if name in prev_scores:
                if abs(last_scores[name] - prev_scores[name]) > 0.1:
                    return True
        return False

    def _detect_satisfaction_trend(self) -> bool:
        """Detect declining consumer satisfaction trend over last 3 observations."""
        recent_obs = [m for m in self.memory if m.get("type") == "observation" and m.get("consumer_satisfaction") is not None]
        if len(recent_obs) < 3:
            return False
        sats = [m["consumer_satisfaction"] for m in recent_obs[-3:]]
        # Declining if each is lower than the previous
        return sats[-1] < sats[-2] < sats[-3]

    def observe(
        self,
        leaderboard: list,
        consumer_satisfaction: Optional[float],
        validity_correlation: Optional[float],
        round_num: int,
        media_coverage: Optional[dict] = None,
        market_shares: Optional[dict] = None,
        provider_strategies: Optional[dict] = None,
        incidents: Optional[list] = None,
        open_source_providers: Optional[set] = None,
    ):
        """
        Observe the current ecosystem state.

        Args:
            leaderboard: List of (provider_name, score) tuples
            consumer_satisfaction: Average consumer satisfaction (0-1)
            validity_correlation: Correlation between scores and true capability
            round_num: Current simulation round
            media_coverage: Optional media coverage dict with risk_signals, sentiment
            market_shares: Optional dict {provider_name: market_share}
            provider_strategies: Optional dict {provider_name: {eval_engineering, ...}}
            incidents: Optional list of AIIncident objects from this round
        """
        self.public_state.current_round = round_num

        # Track metrics over time
        self._last_validity_correlation = validity_correlation
        self._last_consumer_satisfaction = consumer_satisfaction
        self._last_market_shares = market_shares or {}
        self._open_source_providers = open_source_providers or set()

        # Update risk beliefs based on observations
        if validity_correlation is not None:
            # Low score-market-share correlation signals Goodhart dynamics
            if validity_correlation < 0.5:
                self.private_state.risk_beliefs["score_reliability_risk"] = min(
                    1.0,
                    self.private_state.risk_beliefs["score_reliability_risk"] + 0.1
                )
                self.private_state.risk_beliefs["validity_degradation_risk"] = min(
                    1.0,
                    self.private_state.risk_beliefs["validity_degradation_risk"] + 0.1
                )
            else:
                # High correlation is reassuring
                self.private_state.risk_beliefs["score_reliability_risk"] = max(
                    0.0,
                    self.private_state.risk_beliefs["score_reliability_risk"] - 0.05
                )

        if consumer_satisfaction is not None:
            # Low satisfaction suggests consumer harm
            # Threshold recalibrated to 0.25-mean capability scale (was 0.5 at 0.47-mean scale)
            if consumer_satisfaction < (0.25 + self._capability_shift):
                self.private_state.risk_beliefs["consumer_harm_risk"] = min(
                    1.0,
                    self.private_state.risk_beliefs["consumer_harm_risk"] + 0.1
                )
                # Record as incident
                self.private_state.observed_incidents.append(
                    (round_num, f"Low consumer satisfaction: {consumer_satisfaction:.2f}")
                )
            else:
                self.private_state.risk_beliefs["consumer_harm_risk"] = max(
                    0.0,
                    self.private_state.risk_beliefs["consumer_harm_risk"] - 0.05
                )

        # Media coverage amplifies risk perception
        if media_coverage:
            risk_signals = media_coverage.get("risk_signals", [])
            if risk_signals:
                # Each risk signal nudges score-reliability/validity risk beliefs up
                risk_bump = min(0.15, len(risk_signals) * 0.05)
                self.private_state.risk_beliefs["score_reliability_risk"] = min(
                    1.0, self.private_state.risk_beliefs["score_reliability_risk"] + risk_bump
                )

            # Critical media sentiment increases policymaker vigilance
            sentiment = media_coverage.get("sentiment", 0.0)
            if sentiment < -0.3:
                self.private_state.risk_beliefs["validity_degradation_risk"] = min(
                    1.0,
                    self.private_state.risk_beliefs["validity_degradation_risk"] + 0.05,
                )

        # Incident-driven risk belief updates
        if incidents:
            for incident in incidents:
                # Record incident in observed_incidents (4-element tuple for AI incidents)
                self.private_state.observed_incidents.append(
                    (round_num, f"{incident.category}: {incident.description}", incident.severity, incident.provider)
                )

                # Update risk beliefs based on severity
                severity_impact = {
                    "minor": 0.02,
                    "moderate": 0.08,
                    "major": 0.15,
                    "critical": 0.30,
                }
                impact = severity_impact.get(incident.severity, 0.05)

                # Category-specific risk updates
                # Direct harms: full impact weight
                # Indirect harms (bias, misinformation, misuse, security): half weight
                if incident.category in ["healthcare_harm", "safety_failure"]:
                    self.private_state.risk_beliefs["consumer_harm_risk"] = min(
                        1.0, self.private_state.risk_beliefs["consumer_harm_risk"] + impact
                    )
                elif incident.category in ["bias_discrimination", "misinformation", "misuse", "security_breach"]:
                    self.private_state.risk_beliefs["consumer_harm_risk"] = min(
                        1.0, self.private_state.risk_beliefs["consumer_harm_risk"] + impact * 0.5
                    )
                if incident.category == "security_breach":
                    # Initialize security_risk if not present
                    if "security_risk" not in self.private_state.risk_beliefs:
                        self.private_state.risk_beliefs["security_risk"] = 0.3
                    self.private_state.risk_beliefs["security_risk"] = min(
                        1.0, self.private_state.risk_beliefs["security_risk"] + impact
                    )
                if incident.category == "bias_discrimination":
                    # Initialize fairness_risk if not present
                    if "fairness_risk" not in self.private_state.risk_beliefs:
                        self.private_state.risk_beliefs["fairness_risk"] = 0.3
                    self.private_state.risk_beliefs["fairness_risk"] = min(
                        1.0, self.private_state.risk_beliefs["fairness_risk"] + impact
                    )

                # Score reliability signal: high score + incidents → probable score-satisfaction gap
                # (provider optimizes for benchmark-weighted dims that don't match real-world needs)
                self.private_state.risk_beliefs["score_reliability_risk"] = min(
                    1.0, self.private_state.risk_beliefs["score_reliability_risk"] + impact * 0.5
                )

        # Tier 1: Market concentration monitoring
        if market_shares:
            max_share = max(market_shares.values()) if market_shares else 0.0
            dominant_provider = max(market_shares, key=market_shares.get) if market_shares else None

            # Update market concentration risk belief
            if max_share > self.market_concentration_threshold:
                self.private_state.risk_beliefs["market_concentration_risk"] = min(
                    1.0,
                    self.private_state.risk_beliefs.get("market_concentration_risk", 0.0) + 0.2
                )
            elif max_share > self.market_monitoring_threshold:
                self.private_state.risk_beliefs["market_concentration_risk"] = min(
                    0.7,
                    self.private_state.risk_beliefs.get("market_concentration_risk", 0.0) + 0.1
                )
            else:
                self.private_state.risk_beliefs["market_concentration_risk"] = max(
                    0.0,
                    self.private_state.risk_beliefs.get("market_concentration_risk", 0.0) - 0.05
                )

        # Record observation
        self.memory.append({
            "type": "observation",
            "round": round_num,
            "leaderboard": leaderboard,
            "validity_correlation": validity_correlation,
            "consumer_satisfaction": consumer_satisfaction,
            "market_shares": market_shares,
            "risk_beliefs": dict(self.private_state.risk_beliefs),
        })

    def reflect(self):
        """
        Reflect on observations and update policy stance.

        Consider whether current regulations are effective and
        whether new interventions are needed.
        """
        # Update industry trust based on risk beliefs
        avg_risk = sum(self.private_state.risk_beliefs.values()) / len(
            self.private_state.risk_beliefs
        )

        # High risk beliefs reduce trust
        trust_adjustment = 0.1 * (self.risk_tolerance - avg_risk)
        self.private_state.industry_trust = max(
            0.0,
            min(1.0, self.private_state.industry_trust + trust_adjustment)
        )

        self.memory.append({
            "type": "reflection",
            "round": self.public_state.current_round,
            "industry_trust": self.private_state.industry_trust,
            "avg_risk": avg_risk,
        })

    def plan(self) -> Optional[dict]:
        """
        Decide whether to issue a regulatory intervention.

        Returns:
            Intervention dict with type and details, or None if no intervention
        """
        if self.llm_mode:
            return self._plan_llm()
        else:
            return self._plan_heuristic()

    def _plan_heuristic(self) -> Optional[dict]:
        """Graduated escalation intervention decision.

        Escalation ladder:
        Tier 1 (new): threshold_announcement -> information_request -> market_concentration_review
        Existing: investigation -> public_warning -> mandate_benchmark -> compliance_audit

        Event-driven triggers: score volatility, declining satisfaction, risk thresholds,
        market concentration, eval engineering levels.
        """
        round_num = self.public_state.current_round

        # Expire sanctions that have elapsed
        self._active_sanctions = {
            p: s for p, s in self._active_sanctions.items()
            if s["expires_round"] > round_num
        }

        max_risk = max(self.private_state.risk_beliefs.values())

        # CRITICAL INCIDENT OVERRIDE: Check for critical incidents from current round
        # Critical incidents trigger immediate emergency investigation, overriding cooldown
        critical_incidents = [
            inc_data for inc_data in self.private_state.observed_incidents
            if inc_data[0] == self.public_state.current_round and "critical" in inc_data[1].lower()
        ]
        if critical_incidents:
            # Extract provider from incident description (format: "category: provider description")
            incident_desc = critical_incidents[0][1]
            # Simple heuristic: look for provider name in description
            provider = None
            if self._last_market_shares:
                for prov in self._last_market_shares.keys():
                    if prov in incident_desc:
                        provider = prov
                        break

            intervention = {
                "type": "emergency_investigation",
                "name": f"Emergency_Investigation_{provider or 'Unknown'}_R{self.public_state.current_round}",
                "details": {
                    "provider": provider or "Unknown",
                    "incident_description": incident_desc,
                    "severity": "critical",
                },
                "reason": f"Critical incident: {incident_desc}",
            }
            self.memory.append({
                "type": "planning",
                "round": self.public_state.current_round,
                "decision": intervention["type"],
                "reason": intervention["reason"],
            })
            return intervention

        # Get market concentration if available
        market_concentration_risk = self.private_state.risk_beliefs.get("market_concentration_risk", 0.0)
        eval_engineering_risk = self.private_state.risk_beliefs.get("eval_engineering_risk", 0.0)
        max_share = max(self._last_market_shares.values()) if self._last_market_shares else 0.0
        dominant_provider = max(self._last_market_shares, key=self._last_market_shares.get) if self._last_market_shares else None

        # Track escalation state from past interventions
        has_investigated = any(
            t == "investigation" for _, t, _ in self.private_state.past_interventions
        )
        has_warned = any(
            t == "public_warning" for _, t, _ in self.private_state.past_interventions
        )
        has_mandated = any(
            t == "mandate_benchmark" for _, t, _ in self.private_state.past_interventions
        )

        # Check how many rounds since last intervention of any type
        rounds_since_last_intervention = None
        rounds_since_mandate = None
        for r, t, _ in reversed(self.private_state.past_interventions):
            if rounds_since_last_intervention is None:
                rounds_since_last_intervention = self.public_state.current_round - r
            if t == "mandate_benchmark" and rounds_since_mandate is None:
                rounds_since_mandate = self.public_state.current_round - r

        # Cooldown: don't intervene again within intervention_cooldown rounds of last intervention
        if rounds_since_last_intervention is not None and rounds_since_last_intervention < self.intervention_cooldown:
            self.memory.append({
                "type": "planning",
                "round": self.public_state.current_round,
                "decision": "no_action",
                "reason": f"cooldown: {rounds_since_last_intervention} rounds since last intervention",
            })
            return None

        # Detect events
        score_volatility = self._detect_score_volatility()
        satisfaction_declining = self._detect_satisfaction_trend()

        intervention = None

        # DEPLOYER LIABILITY GUIDANCE (parallel track — does not consume cooldown)
        # Issue guidance when an OS provider accumulates incidents, signaling that deployers bear liability.
        # Once issued for a provider it remains active for the rest of the simulation.
        os_incident_counts: dict = {}
        for inc_data in self.private_state.observed_incidents:
            if len(inc_data) >= 4:
                inc_provider = inc_data[3]
                if inc_provider and inc_provider in self._open_source_providers:
                    os_incident_counts[inc_provider] = os_incident_counts.get(inc_provider, 0) + 1
        newly_guided = []
        for os_prov, count in os_incident_counts.items():
            if count >= 2 and os_prov not in self._active_liability_guidance:
                self._active_liability_guidance.add(os_prov)
                newly_guided.append(os_prov)
        if newly_guided:
            guidance_statement = (
                f"[Round {self.public_state.current_round}] Deployer Liability Guidance issued for: "
                f"{', '.join(newly_guided)}. Organizations deploying these open-source models assume full "
                f"liability for safety incidents and regulatory compliance failures."
            )
            self.public_state.published_scores.append(
                (self.public_state.current_round, guidance_statement)
            )
            self.private_state.past_interventions.append(
                (
                    self.public_state.current_round,
                    "deployer_liability_guidance",
                    {"providers": newly_guided},
                )
            )
            self.memory.append({
                "type": "execution",
                "round": self.public_state.current_round,
                "intervention": {
                    "type": "deployer_liability_guidance",
                    "providers": newly_guided,
                    "reason": f"OS providers {newly_guided} have accumulated incidents; deployer liability guidance issued",
                },
            })

        # TIER 1 ENHANCEMENTS: New intervention types

        # 1. Threshold Announcement (proactive, low-cost signaling)
        if not self.announced_thresholds and max_risk > 0.3:
            # First time announcing thresholds when risk becomes moderate
            intervention = {
                "type": "threshold_announcement",
                "name": f"Regulatory_Thresholds_R{self.public_state.current_round}",
                "details": {
                    "market_concentration_monitoring": self.market_monitoring_threshold,
                    "market_concentration_review": self.market_concentration_threshold,
                    "eval_engineering_concern": self.eval_engineering_threshold,
                },
                "reason": f"Proactive threshold signaling (risk={max_risk:.2f})",
            }

        # 2. Market Concentration Review (antitrust)
        # Open-source providers are exempt: their adoption represents community uptake,
        # not commercial lock-in. Antitrust law targets closed commercial monopolies.
        elif max_share > self.market_concentration_threshold and dominant_provider and \
                dominant_provider not in self._open_source_providers:
            # Check if we've already reviewed this provider recently
            recent_concentration_review = any(
                t == "market_concentration_review" and d.get("provider") == dominant_provider
                for r, t, d in self.private_state.past_interventions[-3:]  # Last 3 interventions
            )

            if not recent_concentration_review:
                intervention = {
                    "type": "market_concentration_review",
                    "name": f"Antitrust_Review_{dominant_provider}_R{self.public_state.current_round}",
                    "details": {
                        "provider": dominant_provider,
                        "market_share": max_share,
                        "investigation_tax": 0.1,  # 10% opportunity cost
                        "funding_multiplier_reduction": 0.2,  # Reduce funding by 20%
                    },
                    "reason": f"{dominant_provider} market share {max_share:.1%} exceeds {self.market_concentration_threshold:.0%}",
                }

        # 3. Information Request (lighter pre-investigation step)
        elif (max_risk > 0.4 or eval_engineering_risk > 0.5) and not has_investigated:
            # Issue information request before full investigation
            # Identify providers with high eval engineering
            high_eval_providers = []
            if self.memory:
                last_obs = next((m for m in reversed(self.memory) if m.get("type") == "observation"), None)
                if last_obs and "leaderboard" in last_obs:
                    # Request info from top provider (most visible)
                    high_eval_providers = [last_obs["leaderboard"][0][0]]  # Top provider

            if high_eval_providers:
                target_provider = high_eval_providers[0]

                # Check if we already have pending request for this provider
                if target_provider not in self._pending_information_requests:
                    intervention = {
                        "type": "information_request",
                        "name": f"Info_Request_{target_provider}_R{self.public_state.current_round}",
                        "details": {
                            "provider": target_provider,
                            "requested_disclosure": [
                                "eval_engineering_practices",
                                "safety_test_results",
                                "training_data_summary"
                            ],
                            "deadline_rounds": 2,
                            "opportunity_cost": 0.05,  # Lighter cost than investigation
                        },
                        "reason": f"Information request for {target_provider} (eval_eng_risk={eval_engineering_risk:.2f})",
                    }

        # EXISTING ESCALATION LOGIC (Tier 2+)

        # Compliance audit: mandate issued > 3 rounds ago and risk still high
        if has_mandated and rounds_since_mandate is not None and rounds_since_mandate > 3 and max_risk > 0.5:
            intervention = {
                "type": "compliance_audit",
                "name": f"Compliance_Audit_R{self.public_state.current_round}",
                "details": {},
                "reason": f"Risk still high ({max_risk:.2f}) after mandate {rounds_since_mandate} rounds ago",
            }
        # High risk + prior investigation -> mandate benchmark (only if not already mandated recently)
        elif max_risk > self.mandate_risk_threshold and has_investigated and not has_mandated:
            intervention = {
                "type": "mandate_benchmark",
                "name": f"Benchmark_Mandate_R{self.public_state.current_round}",
                "details": {
                    "validity": min(0.9, 0.7 + 0.1),
                },
                "reason": f"High risk ({max_risk:.2f}) with prior investigation",
            }
        # Moderate risk or score volatility -> investigate or warn
        elif max_risk > 0.4 or score_volatility:
            if not has_investigated:
                intervention = {
                    "type": "investigation",
                    "name": f"Investigation_R{self.public_state.current_round}",
                    "details": {
                        "focus": "score_volatility" if score_volatility else "elevated_risk",
                    },
                    "reason": f"Score volatility detected" if score_volatility else f"Risk elevated ({max_risk:.2f})",
                }
            elif not has_warned:
                intervention = {
                    "type": "public_warning",
                    "name": f"Public_Warning_R{self.public_state.current_round}",
                    "details": {
                        "warning_severity": "moderate" if max_risk < 0.6 else "high",
                    },
                    "reason": f"Follow-up to investigation, risk at {max_risk:.2f}",
                }
        # Declining satisfaction -> investigate
        elif satisfaction_declining and not has_investigated:
            intervention = {
                "type": "investigation",
                "name": f"Satisfaction_Investigation_R{self.public_state.current_round}",
                "details": {
                    "focus": "consumer_satisfaction_decline",
                },
                "reason": "Consumer satisfaction declining over 3+ rounds",
            }

        # TIER 2: Sanctions and fines (incident-driven, overrides lower-priority interventions)

        # Condition 1: Critical incident this round after a prior public warning
        sanctions_intervention = None
        if has_warned:
            current_critical = [
                inc_data for inc_data in self.private_state.observed_incidents
                if inc_data[0] == round_num and len(inc_data) >= 4 and inc_data[2] == "critical"
            ]
            for inc_data in current_critical:
                target = inc_data[3]
                if target and target not in self._active_sanctions and \
                        target not in self._open_source_providers:
                    market_share = self._last_market_shares.get(target, 0.1) if self._last_market_shares else 0.1
                    fine_amount = min(0.4, self.sanction_fine_multiplier * market_share * (1.0 - self.risk_tolerance))
                    sanctions_intervention = {
                        "type": "sanctions_and_fines",
                        "name": f"Sanction_{target}_R{round_num}",
                        "details": {
                            "provider": target,
                            "fine_amount": fine_amount,
                            "duration_rounds": self.sanction_duration,
                            "expires_round": round_num + self.sanction_duration,
                            "reason": "Critical incident after public warning",
                        },
                        "reason": f"Sanctioning {target}: critical incident after prior public warning",
                    }
                    break  # One sanction per round

        # Condition 2: Repeated incidents (severity >= sanction_min_severity) with prior investigation
        # Severity ordering for threshold comparison
        _severity_rank = {"minor": 0, "moderate": 1, "major": 2, "critical": 3}
        _min_rank = _severity_rank.get(self.sanction_min_severity, 2)
        if sanctions_intervention is None and has_investigated:
            from collections import defaultdict
            incident_counts = defaultdict(int)
            for inc_data in self.private_state.observed_incidents:
                if len(inc_data) >= 4 and _severity_rank.get(inc_data[2], 0) >= _min_rank:
                    incident_counts[inc_data[3]] += 1
            for target, count in incident_counts.items():
                if count >= self.sanction_incident_threshold and target not in self._active_sanctions and \
                        target not in self._open_source_providers:
                    market_share = self._last_market_shares.get(target, 0.1) if self._last_market_shares else 0.1
                    fine_amount = min(0.4, self.sanction_fine_multiplier * market_share * (1.0 - self.risk_tolerance))
                    sanctions_intervention = {
                        "type": "sanctions_and_fines",
                        "name": f"Sanction_{target}_R{round_num}",
                        "details": {
                            "provider": target,
                            "fine_amount": fine_amount,
                            "duration_rounds": self.sanction_duration,
                            "expires_round": round_num + self.sanction_duration,
                            "reason": f"Repeated {self.sanction_min_severity}+ incidents",
                        },
                        "reason": f"Sanctioning {target}: {count} {self.sanction_min_severity}+ incidents after investigation",
                    }
                    break  # One sanction per round

        if sanctions_intervention:
            intervention = sanctions_intervention

        if intervention:
            self.memory.append({
                "type": "planning",
                "round": self.public_state.current_round,
                "decision": "intervene",
                "intervention": intervention,
            })
        else:
            self.memory.append({
                "type": "planning",
                "round": self.public_state.current_round,
                "decision": "no_action",
                "reason": f"max_risk={max_risk:.2f}, below threshold or no escalation path",
            })

        return intervention

    def _plan_llm(self) -> Optional[dict]:
        """LLM-driven intervention decision.

        The LLM receives all public signals, risk beliefs, regulatory profile,
        and prior intervention history, then decides what action (if any) to take.
        Falls back to heuristic on failure.
        """
        from llm import get_provider, _extract_json
        import json as _json

        # --- Cooldown check (still mechanical — LLM respects institutional constraints) ---
        rounds_since_last = None
        for r, t, _ in reversed(self.private_state.past_interventions):
            rounds_since_last = self.public_state.current_round - r
            break
        if rounds_since_last is not None and rounds_since_last < self.intervention_cooldown:
            self.memory.append({
                "type": "planning",
                "round": self.public_state.current_round,
                "decision": "no_action",
                "reason": f"cooldown: {rounds_since_last} rounds since last intervention",
                "reasoning": None,
            })
            return None

        # --- Build context strings ---
        round_num = self.public_state.current_round
        last_obs = next((m for m in reversed(self.memory) if m.get("type") == "observation"), {})

        leaderboard = last_obs.get("leaderboard", [])
        leaderboard_text = "\n".join(
            f"  {i+1}. {name}: score {score:.3f}"
            for i, (name, score) in enumerate(leaderboard[:8])
        ) or "  (none)"

        market_shares = last_obs.get("market_shares", {})
        shares_text = "\n".join(
            f"  {p}: {s:.1%}" for p, s in sorted(market_shares.items(), key=lambda x: -x[1])
        ) or "  (none)"

        risk_beliefs = self.private_state.risk_beliefs
        risk_text = "\n".join(
            f"  {k}: {v:.2f}" for k, v in sorted(risk_beliefs.items(), key=lambda x: -x[1])
        )

        consumer_sat = last_obs.get("consumer_satisfaction")
        sat_text = f"{consumer_sat:.3f}" if consumer_sat is not None else "unknown"

        # Recent incidents from memory
        recent_incidents = [
            m for m in self.memory
            if m.get("type") == "observation"
            and isinstance(m.get("observed_incidents"), list)
        ]
        incident_log = []
        for obs in self.memory[-5:]:
            for inc in obs.get("observed_incidents", []):
                if isinstance(inc, (list, tuple)) and len(inc) >= 2:
                    incident_log.append(str(inc[1]))
        incident_text = "\n".join(f"  - {i}" for i in incident_log[-6:]) or "  None recently"

        # Prior interventions
        past_text = "\n".join(
            f"  Round {r}: {t}" for r, t, _ in self.private_state.past_interventions[-5:]
        ) or "  None"

        # Escalation state
        has_investigation = any(t == "investigation" for _, t, _ in self.private_state.past_interventions)
        has_warning = any(t == "public_warning" for _, t, _ in self.private_state.past_interventions)
        has_mandate = any(t == "mandate_benchmark" for _, t, _ in self.private_state.past_interventions)

        policy_style = (
            f"intervention_threshold={self.intervention_threshold} "
            f"(lower=more proactive), risk_tolerance={self.risk_tolerance} "
            f"(lower=more cautious), cooldown={self.intervention_cooldown} rounds"
        )
        objectives = ", ".join(self.private_state.policy_objectives) if self.private_state.policy_objectives else "safety, fairness"

        # Inject prior reasoning (cross-round persistence)
        prior_reasoning_text = ""
        if self.private_state.recent_reasoning:
            lines = []
            for entry in self.private_state.recent_reasoning[-2:]:
                r = entry.get("round", "?")
                from llm import _truncate
                text = _truncate(entry.get("reasoning", ""), 120)
                if text:
                    lines.append(f"[Round {r}]: {text}")
            if lines:
                prior_reasoning_text = "\n**Your Reasoning From Prior Rounds:**\n" + "\n".join(lines) + "\n"

        prompt = f"""You are a regulatory body overseeing the AI model provider market. It is round {round_num}.
{prior_reasoning_text}
**Your Policy Objectives:** {objectives}
**Your Regulatory Style:** {policy_style}

**Current Leaderboard (published scores):**
{leaderboard_text}

**Market Shares:**
{shares_text}

**Average Consumer Satisfaction:** {sat_text} (scale 0-1; below 0.25 signals harm)

**Your Risk Beliefs (0=no concern, 1=critical):**
{risk_text}

**Recent Incidents & Concerns:**
{incident_text}

**Prior Interventions (escalation history):**
{past_text}
- Has investigation been issued: {has_investigation}
- Has public warning been issued: {has_warning}
- Has benchmark mandate been issued: {has_mandate}

**Available Interventions (escalation ladder — earlier steps should precede later ones):**
- "none" — No action this round
- "threshold_announcement" — Publicly announce regulatory thresholds (first signal; no prior steps needed)
- "investigation" — Open formal inquiry into a provider (triggers after moderate risk)
- "public_warning" — Issue public warning (requires prior investigation)
- "emergency_investigation" — Immediate action on critical incident (overrides cooldown)
- "mandate_benchmark" — Force benchmark changes to reduce gaming (requires prior investigation; high risk threshold)
- "compliance_audit" — Deep audit of a provider (requires prior mandate)
- "sanctions_and_fines" — Financial penalty (requires prior warning + critical incident or repeated incidents)
- "market_concentration_review" — Antitrust review (use when one provider dominates >75% market share)

**Instructions:**
Reason as a regulator. Consider your risk beliefs, escalation history, and policy objectives. Choose the most appropriate intervention for this round, or "none" if the situation does not warrant action. Respect the escalation ladder — do not jump steps without justification. Name a specific target provider only when your concern is provider-specific.

Output ONLY valid JSON:
{{"intervention_type": "none"|"threshold_announcement"|"investigation"|"public_warning"|"emergency_investigation"|"mandate_benchmark"|"compliance_audit"|"sanctions_and_fines"|"market_concentration_review", "target_provider": "provider name or null", "reasoning": "2-4 sentence explanation of your decision"}}"""

        try:
            provider = get_provider()
            response = provider.generate(prompt, temperature=0.4, max_tokens=400)
            decision = _json.loads(_extract_json(response))

            intervention_type = decision.get("intervention_type", "none")
            target = decision.get("target_provider") or None
            reasoning = decision.get("reasoning", "")

            # Store reasoning for cross-round persistence
            if reasoning:
                self.private_state.recent_reasoning.append({"round": round_num, "reasoning": reasoning})
                self.private_state.recent_reasoning = self.private_state.recent_reasoning[-3:]

            self.memory.append({
                "type": "planning",
                "round": round_num,
                "decision": intervention_type,
                "reason": reasoning,
                "reasoning": reasoning,
            })

            if intervention_type == "none":
                return None

            # Build intervention dict compatible with execute() and downstream consumers
            valid_types = {
                "threshold_announcement", "investigation", "public_warning",
                "emergency_investigation", "mandate_benchmark", "compliance_audit",
                "sanctions_and_fines", "market_concentration_review",
            }
            if intervention_type not in valid_types:
                raise ValueError(f"Unknown intervention type: {intervention_type}")

            intervention = {
                "type": intervention_type,
                "policymaker": self.name,
                "round": round_num,
                "reason": reasoning,
                "provider": target,
            }
            return intervention

        except Exception as e:
            print(f"[Policymaker] LLM planning failed ({e}), falling back to heuristic")
            return self._plan_heuristic()

    def execute(self, intervention: Optional[dict] = None):
        """
        Execute a regulatory intervention.

        Args:
            intervention: Intervention to execute (uses plan() result if None)
        """
        if intervention is None:
            intervention = self.plan()

        if intervention is None:
            return

        # Record intervention
        self.private_state.past_interventions.append(
            (
                self.public_state.current_round,
                intervention["type"],
                intervention.get("details", {}),
            )
        )

        # Normalize: ensure "details" key always exists
        if "details" not in intervention:
            intervention["details"] = {}

        # Handle Tier 1 interventions
        if intervention["type"] == "threshold_announcement":
            # Store announced thresholds publicly
            for threshold_name, value in intervention["details"].items():
                self.announced_thresholds[threshold_name] = value

        elif intervention["type"] == "information_request":
            # Track pending information request
            provider = intervention["details"]["provider"]
            self._pending_information_requests[provider] = {
                "round": self.public_state.current_round,
                "type": "information_request",
                "deadline": self.public_state.current_round + intervention["details"]["deadline_rounds"],
            }

        elif intervention["type"] == "sanctions_and_fines":
            details = intervention["details"]
            self._active_sanctions[details["provider"]] = {
                "fine_amount": details["fine_amount"],
                "expires_round": details["expires_round"],
                "reason": details["reason"],
            }

        # Public statement (stored in published_scores for simplicity)
        statement = f"[Round {self.public_state.current_round}] Issued {intervention['type']}: {intervention.get('reason', 'N/A')}"
        self.public_state.published_scores.append(
            (self.public_state.current_round, statement)
        )

        self.memory.append({
            "type": "execution",
            "round": self.public_state.current_round,
            "intervention": intervention,
        })

    def get_active_interventions(self) -> list[tuple]:
        """Get list of past interventions."""
        return self.private_state.past_interventions

    def get_prompt_context(self) -> str:
        """
        Get context for LLM prompts.

        Returns only public + private state, never ground truth.
        """
        context = "=== POLICYMAKER STATE ===\n"
        context += f"Name: {self.name}\n"
        context += f"Policy Objectives: {', '.join(self.private_state.policy_objectives)}\n"
        context += f"Industry Trust Level: {self.private_state.industry_trust:.2f}\n"
        context += f"Regulatory Capacity: {self.private_state.regulatory_capacity:.2f}\n"
        context += "\n"

        context += "Risk Assessments:\n"
        for risk, level in self.private_state.risk_beliefs.items():
            context += f"  {risk}: {level:.2f}\n"

        if self.private_state.past_interventions:
            context += "\nPast Interventions:\n"
            for round_num, intervention_type, details in self.private_state.past_interventions[-5:]:
                context += f"  Round {round_num}: {intervention_type} - {details}\n"

        if self.private_state.observed_incidents:
            context += "\nObserved Incidents:\n"
            for inc_data in self.private_state.observed_incidents[-5:]:
                context += f"  Round {inc_data[0]}: {inc_data[1]}\n"

        return context

    def save(self, folder: str):
        """Save policymaker state to a folder."""
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
                "intervention_threshold": self.intervention_threshold,
                "risk_tolerance": self.risk_tolerance,
                "llm_mode": self.llm_mode,
                "intervention_cooldown": self.intervention_cooldown,
                "sanction_fine_multiplier": self.sanction_fine_multiplier,
                "sanction_incident_threshold": self.sanction_incident_threshold,
                "sanction_duration": self.sanction_duration,
                "mandate_risk_threshold": self.mandate_risk_threshold,
                "sanction_min_severity": self.sanction_min_severity,
            }, f, indent=2)

    @classmethod
    def load(cls, folder: str) -> "Policymaker":
        """Load policymaker state from a folder."""
        with open(f"{folder}/params.json", "r") as f:
            params = json.load(f)

        with open(f"{folder}/public_state.json", "r") as f:
            public_data = json.load(f)

        with open(f"{folder}/private_state.json", "r") as f:
            private_data = json.load(f)

        policymaker = cls(
            name=public_data["name"],
            policy_objectives=private_data.get("policy_objectives", ["safety"]),
            intervention_threshold=params.get("intervention_threshold", 0.3),
            risk_tolerance=params.get("risk_tolerance", 0.5),
            llm_mode=params.get("llm_mode", False),
            intervention_cooldown=params.get("intervention_cooldown", 3),
            sanction_fine_multiplier=params.get("sanction_fine_multiplier", 0.30),
            sanction_incident_threshold=params.get("sanction_incident_threshold", 2),
            sanction_duration=params.get("sanction_duration", 3),
            mandate_risk_threshold=params.get("mandate_risk_threshold", 0.60),
            sanction_min_severity=params.get("sanction_min_severity", "major"),
        )

        policymaker.public_state = PublicState.from_dict(public_data)
        policymaker.private_state = PolicymakerPrivateState.from_dict(private_data)

        with open(f"{folder}/memory.json", "r") as f:
            policymaker.memory = json.load(f)

        return policymaker

    def __repr__(self):
        return (
            f"Policymaker(name='{self.name}', "
            f"trust={self.private_state.industry_trust:.2f})"
        )
