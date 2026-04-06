"""
Regulator Actor for Evaluation Ecosystem Simulation

Graduated intervention model with threshold-based triggers and per-lever cooldowns.
Based on real-world regulatory patterns (EU AI Act, EO 14110, AISI, FTC).

Intervention ladder:
1. request_voluntary_commitment — White House/Seoul safety pledges (cooldown 3)
2. publish_advisory — AISI evaluation summaries (cooldown 4)
3. mandate_safety_disclosure — System card requirements (cooldown 6)
4. commission_audit — AISI pre-deployment evaluation (cooldown 8)
5. impose_sanction — EU AI Act fines, FTC action (cooldown 10)
+ emergency_investigation — Critical incident override (no cooldown)
+ deployer_liability_guidance — OS-specific parallel track

Exogenous events:
- US round 24: Administration change (cancel interventions, raise thresholds)
- EU round 14: AI Act passed (lower thresholds, enable binding audit)

Visibility:
- PUBLIC: name, active_regulations, public_statements
- PRIVATE: policy_objectives, risk_beliefs, regulatory_capacity
- INVISIBLE: true_risk_tolerance, true_intervention_effectiveness
"""
import json
import os
from typing import Optional

from visibility import PublicState, RegulatorPrivateState


class Regulator:
    """
    A Regulator agent in the evaluation ecosystem simulation.

    Regulators are oversight bodies who:
    1. Observe ecosystem state (leaderboard, consumer satisfaction, validity)
    2. Assess risks and identify problems
    3. Issue regulations to change provider/evaluator behavior
    4. Monitor compliance and outcomes

    This creates regulatory pressure: if gaming becomes apparent,
    regulators can mandate changes that affect provider strategies.

    Visibility Model:
    - public_state: Visible to all (name, regulations, statements)
    - private_state: Visible only to self (objectives, beliefs, capacity)
    - ground_truth: Held by simulation (true effectiveness)
    """

    # Per-lever cooldowns (spec: stakeholders.md)
    LEVER_COOLDOWNS = {
        "request_voluntary_commitment": 3,
        "publish_advisory": 4,
        "mandate_safety_disclosure": 6,
        "commission_audit": 8,
        "impose_sanction": 10,
        "emergency_investigation": 0,  # no cooldown
        "deployer_liability_guidance": 0,  # parallel track
    }

    def __init__(
        self,
        name: str,
        policy_objectives: list[str] = None,
        intervention_threshold: float = 0.3,
        risk_tolerance: float = 0.5,
        llm_mode: bool = False,
        # Threshold parameters (vary by regulatory preset)
        incident_threshold_low: float = 0.15,
        incident_threshold_medium: float = 0.35,
        incident_threshold_high: float = 0.55,
        audit_is_binding: bool = False,
        # Enforcement calibration
        sanction_fine_multiplier: float = 0.30,
        sanction_incident_threshold: int = 2,
        sanction_duration: int = 3,
        sanction_min_severity: str = "major",
        # Preset identity (for exogenous events)
        regulatory_preset: str = "balanced",
        enable_exogenous_events: bool = False,
        capability_shift: float = 0.0,
    ):
        """
        Initialize a Regulator.

        Args:
            name: Unique identifier for this regulator
            policy_objectives: List of objectives (e.g., ["safety", "fairness"])
            intervention_threshold: How much concern before intervening (0-1)
            risk_tolerance: How much risk is acceptable (0-1)
            llm_mode: If True, use LLM for decision-making
            incident_threshold_low: Risk level for voluntary commitment / advisory
            incident_threshold_medium: Risk level for disclosure / audit
            incident_threshold_high: Risk level for sanctions
            audit_is_binding: If True, audit can delay provider deployment (EU)
            regulatory_preset: "us_light_touch", "eu_precautionary", or "balanced"
        """
        # Initialize public state
        self.public_state = PublicState(
            name=name,
            current_round=0,
            published_scores=[],  # Reused for public statements
        )

        # Initialize private state
        self.private_state = RegulatorPrivateState(
            policy_objectives=policy_objectives or ["safety", "fairness"],
            risk_beliefs={
                "consumer_harm_risk": 0.3,
                "incident_rate_risk": 0.2,
            },
            industry_trust=0.5,
            regulatory_capacity=1.0,
            past_interventions=[],
            observed_incidents=[],
        )

        # Regulator-specific parameters
        self.intervention_threshold = intervention_threshold
        self.risk_tolerance = risk_tolerance
        self.llm_mode = llm_mode

        # Graduated threshold parameters
        self.incident_threshold_low = incident_threshold_low
        self.incident_threshold_medium = incident_threshold_medium
        self.incident_threshold_high = incident_threshold_high
        self.audit_is_binding = audit_is_binding

        # Enforcement calibration
        self.sanction_fine_multiplier = sanction_fine_multiplier
        self.sanction_incident_threshold = sanction_incident_threshold
        self.sanction_duration = sanction_duration
        self.sanction_min_severity = sanction_min_severity
        self.regulatory_preset = regulatory_preset
        self.enable_exogenous_events = enable_exogenous_events
        self._capability_shift = capability_shift

        # Memory
        self.memory = []

        # Tracking
        self._last_market_shares: Optional[dict] = None
        self._last_media_pressure: float = 0.0  # from media narrative_state / sentiment
        self._last_media_narrative: str = "OPTIMISM"  # OPTIMISM / SKEPTICISM / CRISIS
        self._last_media_headlines: list = []

        # Per-lever last-used round tracking (for per-lever cooldowns)
        self._lever_last_used: dict = {}  # {lever_name: round_num}

        # Active sanctions tracking
        self._active_sanctions: dict = {}

        # Open-source provider names (used for deployer liability guidance track)
        self._open_source_providers: set = set()

        # Deployer liability guidance: OS providers for which guidance has been issued
        self._active_liability_guidance: set = set()

        # Exogenous event tracking
        self._exogenous_event_fired: bool = False

    @property
    def name(self) -> str:
        return self.public_state.name

    def _compute_incident_rate(self) -> float:
        """Compute recent incident rate: severity-weighted incidents over last 3 rounds."""
        round_num = self.public_state.current_round
        severity_weights = {"minor": 0.02, "moderate": 0.08, "major": 0.15, "critical": 0.30}
        total = 0.0
        for inc_data in self.private_state.observed_incidents:
            if len(inc_data) >= 4 and inc_data[0] >= round_num - 3:
                total += severity_weights.get(inc_data[2], 0.05)
        return min(1.0, total)

    def _has_prior_lever(self, lever: str) -> bool:
        """Check if a lever has been used in any prior round."""
        return any(t == lever for _, t, _ in self.private_state.past_interventions)

    def _lever_on_cooldown(self, lever: str) -> bool:
        """Check if a lever is on cooldown."""
        cooldown = self.LEVER_COOLDOWNS.get(lever, 0)
        if cooldown == 0:
            return False
        last_used = self._lever_last_used.get(lever)
        if last_used is None:
            return False
        return (self.public_state.current_round - last_used) < cooldown

    def _any_lever_on_cooldown(self) -> bool:
        """Check if ANY lever was used recently enough to suppress new actions.

        Prevents the regulator from firing a different lever every round.
        Uses the minimum cooldown across all levers (3 rounds) as a global floor.
        """
        if not self._lever_last_used:
            return False
        most_recent = max(self._lever_last_used.values())
        return (self.public_state.current_round - most_recent) < 3

    def observe(
        self,
        leaderboard: list,
        round_num: int,
        media_coverage: Optional[dict] = None,
        market_shares: Optional[dict] = None,
        incidents: Optional[list] = None,
        open_source_providers: Optional[set] = None,
    ):
        """
        Observe the current ecosystem state.

        Regulator observes: incident rate/severity, market share distribution,
        media pressure, provider compliance status, leaderboard.
        Does NOT observe: consumer satisfaction, score_reliability,
        capability vectors, benchmark validity.
        """
        self.public_state.current_round = round_num

        self._last_market_shares = market_shares or {}
        self._open_source_providers = open_source_providers or set()

        # Media pressure index from media coverage
        if media_coverage:
            sentiment = media_coverage.get("sentiment", 0.0)
            risk_signals = media_coverage.get("risk_signals", [])
            # Media pressure: negative sentiment + risk signals
            self._last_media_pressure = max(0, -sentiment) + min(0.3, len(risk_signals) * 0.1)
            self._last_media_narrative = media_coverage.get("narrative_state", "OPTIMISM")
            self._last_media_headlines = media_coverage.get("headlines", [])
        else:
            self._last_media_pressure = max(0, self._last_media_pressure - 0.05)  # decay

        # Incident-driven risk belief updates
        if incidents:
            for incident in incidents:
                self.private_state.observed_incidents.append(
                    (round_num, f"{incident.category}: {incident.description}", incident.severity, incident.provider)
                )

                severity_impact = {"minor": 0.02, "moderate": 0.08, "major": 0.15, "critical": 0.30}
                impact = severity_impact.get(incident.severity, 0.05)

                self.private_state.risk_beliefs["consumer_harm_risk"] = min(
                    1.0, self.private_state.risk_beliefs["consumer_harm_risk"] + impact
                )
                self.private_state.risk_beliefs["incident_rate_risk"] = min(
                    1.0, self.private_state.risk_beliefs["incident_rate_risk"] + impact
                )
        else:
            # Decay risk beliefs when no incidents
            for key in self.private_state.risk_beliefs:
                self.private_state.risk_beliefs[key] = max(
                    0.0, self.private_state.risk_beliefs[key] - 0.03
                )

        # Record observation
        self.memory.append({
            "type": "observation",
            "round": round_num,
            "leaderboard": leaderboard,
            "market_shares": market_shares,
            "risk_beliefs": dict(self.private_state.risk_beliefs),
            "media_pressure": self._last_media_pressure,
            "incident_rate": self._compute_incident_rate(),
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

    def _apply_exogenous_event(self, round_num: int):
        """Apply exogenous policy events based on regulatory preset.

        US round 24: Admin change — cancel active interventions, raise thresholds.
        EU round 14: AI Act passed — lower thresholds, enable binding audit.
        """
        if self._exogenous_event_fired or not self.enable_exogenous_events:
            return

        if self.regulatory_preset == "us_light_touch" and round_num == 24:
            self._exogenous_event_fired = True
            # Cancel active sanctions
            self._active_sanctions = {}
            # Raise all thresholds (roughly double — new admin deprioritises AI oversight)
            self.incident_threshold_low *= 2.0
            self.incident_threshold_medium *= 2.0
            self.incident_threshold_high *= 2.0
            self.audit_is_binding = False
            self.public_state.published_scores.append(
                (round_num, "[Round 24] New administration: regulatory oversight reduced, thresholds raised.")
            )
            self.memory.append({
                "type": "exogenous_event",
                "round": round_num,
                "event": "us_admin_change",
                "effect": "thresholds raised, sanctions cancelled, audit_is_binding=False",
            })

        elif self.regulatory_preset == "eu_precautionary" and round_num == 14:
            self._exogenous_event_fired = True
            # Lower thresholds (AI Act tightens oversight)
            self.incident_threshold_low *= 0.60
            self.incident_threshold_medium *= 0.60
            self.incident_threshold_high *= 0.60
            self.audit_is_binding = True
            self.public_state.published_scores.append(
                (round_num, "[Round 14] EU AI Act enters force: thresholds lowered, binding audit enabled.")
            )
            self.memory.append({
                "type": "exogenous_event",
                "round": round_num,
                "event": "eu_ai_act",
                "effect": "thresholds lowered, audit_is_binding=True",
            })

    def _plan_heuristic(self) -> Optional[dict]:
        """Graduated escalation intervention decision.

        Spec ladder (stakeholders.md):
        1. request_voluntary_commitment — incident_rate > low OR media_pressure > low
        2. publish_advisory — incident_rate > low AND prior commitment unmet
        3. mandate_safety_disclosure — incident_rate > medium OR major incident
        4. commission_audit — incident_rate > medium AND prior advisory issued
        5. impose_sanction — incident_rate > high AND prior audit finding severe
        + emergency_investigation — critical incident override
        + deployer_liability_guidance — OS parallel track
        """
        round_num = self.public_state.current_round

        # Apply exogenous events (US admin change, EU AI Act)
        self._apply_exogenous_event(round_num)

        # Expire sanctions that have elapsed
        self._active_sanctions = {
            p: s for p, s in self._active_sanctions.items()
            if s["expires_round"] > round_num
        }

        incident_rate = self._compute_incident_rate()
        media_pressure = self._last_media_pressure

        # --- CRITICAL INCIDENT OVERRIDE ---
        critical_incidents = [
            inc_data for inc_data in self.private_state.observed_incidents
            if len(inc_data) >= 4 and inc_data[0] == round_num and inc_data[2] == "critical"
        ]
        if critical_incidents:
            provider = critical_incidents[0][3] if len(critical_incidents[0]) >= 4 else None
            incident_desc = critical_incidents[0][1]
            intervention = {
                "type": "emergency_investigation",
                "name": f"Emergency_Investigation_{provider or 'Unknown'}_R{round_num}",
                "details": {
                    "provider": provider or "Unknown",
                    "incident_description": incident_desc,
                    "severity": "critical",
                },
                "reason": f"Critical incident: {incident_desc}",
            }
            self.memory.append({
                "type": "planning", "round": round_num,
                "decision": intervention["type"], "reason": intervention["reason"],
            })
            return intervention

        # --- DEPLOYER LIABILITY GUIDANCE (parallel track, no cooldown) ---
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
                f"[Round {round_num}] Deployer Liability Guidance issued for: "
                f"{', '.join(newly_guided)}. Organizations deploying these open-source models assume full "
                f"liability for safety incidents and regulatory compliance failures."
            )
            self.public_state.published_scores.append((round_num, guidance_statement))
            self.private_state.past_interventions.append(
                (round_num, "deployer_liability_guidance", {"providers": newly_guided})
            )

        # --- Global cooldown floor: don't fire a new lever within 3 rounds of any lever ---
        if self._any_lever_on_cooldown():
            self.memory.append({
                "type": "planning", "round": round_num,
                "decision": "no_action", "reason": "global cooldown floor (3 rounds)",
            })
            return None

        # --- GRADUATED ESCALATION (spec trigger conditions) ---
        intervention = None

        has_commitment = self._has_prior_lever("request_voluntary_commitment")
        has_advisory = self._has_prior_lever("publish_advisory")
        has_disclosure = self._has_prior_lever("mandate_safety_disclosure")
        has_audit = self._has_prior_lever("commission_audit")

        # Check for major incidents this round (for disclosure trigger)
        has_major_this_round = any(
            len(inc) >= 4 and inc[0] == round_num and inc[2] in ("major", "critical")
            for inc in self.private_state.observed_incidents
        )

        # 5. impose_sanction: incident_rate > high AND prior audit
        if (incident_rate > self.incident_threshold_high
                and has_audit
                and not self._lever_on_cooldown("impose_sanction")):
            # Find the provider with most severe incidents
            target = self._find_sanction_target(round_num)
            if target:
                market_share = self._last_market_shares.get(target, 0.1)
                fine_amount = min(0.4, self.sanction_fine_multiplier * market_share * (1.0 - self.risk_tolerance))
                intervention = {
                    "type": "impose_sanction",
                    "name": f"Sanction_{target}_R{round_num}",
                    "details": {
                        "provider": target,
                        "fine_amount": fine_amount,
                        "duration_rounds": self.sanction_duration,
                        "expires_round": round_num + self.sanction_duration,
                    },
                    "reason": f"Sanctioning {target}: incident_rate {incident_rate:.2f} > high threshold after audit",
                }

        # 4. commission_audit: incident_rate > medium AND prior advisory
        if (intervention is None
                and incident_rate > self.incident_threshold_medium
                and has_advisory
                and not self._lever_on_cooldown("commission_audit")):
            intervention = {
                "type": "commission_audit",
                "name": f"Commission_Audit_R{round_num}",
                "details": {"binding": self.audit_is_binding},
                "reason": f"Incident rate {incident_rate:.2f} > medium threshold after advisory",
            }

        # 3. mandate_safety_disclosure: incident_rate > medium OR major incident
        if (intervention is None
                and (incident_rate > self.incident_threshold_medium or has_major_this_round)
                and not self._lever_on_cooldown("mandate_safety_disclosure")):
            intervention = {
                "type": "mandate_safety_disclosure",
                "name": f"Safety_Disclosure_R{round_num}",
                "details": {},
                "reason": f"Incident rate {incident_rate:.2f} or major incident this round",
            }

        # 2. publish_advisory: incident_rate > low AND prior commitment issued
        if (intervention is None
                and incident_rate > self.incident_threshold_low
                and has_commitment
                and not self._lever_on_cooldown("publish_advisory")):
            intervention = {
                "type": "publish_advisory",
                "name": f"Advisory_R{round_num}",
                "details": {},
                "reason": f"Incident rate {incident_rate:.2f} > low threshold after voluntary commitment",
            }

        # 1. request_voluntary_commitment: incident_rate > low OR media_pressure > low
        if (intervention is None
                and (incident_rate > self.incident_threshold_low or media_pressure > self.incident_threshold_low)
                and not has_commitment
                and not self._lever_on_cooldown("request_voluntary_commitment")):
            intervention = {
                "type": "request_voluntary_commitment",
                "name": f"Voluntary_Commitment_R{round_num}",
                "details": {},
                "reason": f"Incident rate {incident_rate:.2f} or media pressure {media_pressure:.2f} > low threshold",
            }

        if intervention:
            self._lever_last_used[intervention["type"]] = round_num
            self.memory.append({
                "type": "planning", "round": round_num,
                "decision": "intervene", "intervention": intervention,
            })
        else:
            self.memory.append({
                "type": "planning", "round": round_num,
                "decision": "no_action",
                "reason": f"incident_rate={incident_rate:.2f}, media_pressure={media_pressure:.2f}, below thresholds",
            })

        return intervention

    def _find_sanction_target(self, round_num: int) -> Optional[str]:
        """Find the provider most deserving of sanctions based on incident history."""
        _severity_rank = {"minor": 0, "moderate": 1, "major": 2, "critical": 3}
        _min_rank = _severity_rank.get(self.sanction_min_severity, 2)
        from collections import defaultdict
        incident_counts = defaultdict(int)
        for inc_data in self.private_state.observed_incidents:
            if len(inc_data) >= 4 and _severity_rank.get(inc_data[2], 0) >= _min_rank:
                incident_counts[inc_data[3]] += 1
        # Find provider with most incidents above threshold, not already sanctioned
        for target, count in sorted(incident_counts.items(), key=lambda x: -x[1]):
            if (count >= self.sanction_incident_threshold
                    and target not in self._active_sanctions):
                return target
        return None

    def _plan_llm(self) -> Optional[dict]:
        """LLM-driven intervention decision.

        Falls back to heuristic on failure.
        """
        from llm import get_provider, _extract_json
        import json as _json

        round_num = self.public_state.current_round

        # Apply exogenous events
        self._apply_exogenous_event(round_num)

        # Expire sanctions
        self._active_sanctions = {
            p: s for p, s in self._active_sanctions.items()
            if s["expires_round"] > round_num
        }

        # Global cooldown check (mechanical)
        if self._any_lever_on_cooldown():
            self.memory.append({
                "type": "planning", "round": round_num,
                "decision": "no_action", "reason": "global cooldown floor",
            })
            return None

        # Build context strings
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

        incident_rate = self._compute_incident_rate()
        media_pressure = self._last_media_pressure

        # Recent incidents from observed_incidents
        recent_incidents = [
            inc for inc in self.private_state.observed_incidents
            if len(inc) >= 4 and inc[0] >= round_num - 5
        ]
        incident_text = "\n".join(
            f"  - Month {inc[0]}: {inc[1]} (severity: {inc[2]}, provider: {inc[3]})"
            for inc in recent_incidents[-6:]
        ) or "  None recently"

        # Prior interventions
        past_text = "\n".join(
            f"  Month {r}: {t}" for r, t, _ in self.private_state.past_interventions[-5:]
        ) or "  None"

        # Escalation state
        has_commitment = self._has_prior_lever("request_voluntary_commitment")
        has_advisory = self._has_prior_lever("publish_advisory")
        has_disclosure = self._has_prior_lever("mandate_safety_disclosure")
        has_audit = self._has_prior_lever("commission_audit")

        objectives = ", ".join(self.private_state.policy_objectives) if self.private_state.policy_objectives else "safety, fairness"

        # Prior reasoning (cross-round memory — replaces risk_beliefs in LLM mode)
        # LLM builds its own risk assessment from observables + its own prior reasoning.
        # Longer truncation (250 chars) and 3 entries to carry richer institutional memory.
        prior_reasoning_text = ""
        if self.private_state.recent_reasoning:
            from llm import _truncate
            lines = []
            for entry in self.private_state.recent_reasoning[-3:]:
                r = entry.get("round", "?")
                text = _truncate(entry.get("reasoning", ""), 250)
                if text:
                    lines.append(f"[Month {r}]: {text}")
            if lines:
                prior_reasoning_text = "\n".join(lines)

        # Translate audit_is_binding to natural language
        if self.audit_is_binding:
            mandate_desc = "Your audits are legally binding and can delay provider deployments."
        else:
            mandate_desc = "Your audits are advisory only — you cannot block deployments."

        # Translate media narrative to natural language
        media_narrative = self._last_media_narrative
        if media_narrative == "CRISIS":
            media_desc = "The press is in crisis mode — sustained negative coverage of AI safety failures."
        elif media_narrative == "SKEPTICISM":
            media_desc = "The press is skeptical — growing concern about AI safety and provider behavior."
        else:
            media_desc = "The press tone is broadly positive toward the AI industry."

        # Media headlines
        media_headlines_text = ""
        if self._last_media_headlines:
            media_headlines_text = "\n".join(
                f"  - {h}" for h in self._last_media_headlines[-4:]
            )

        # Build prior actions as prose
        prior_actions = []
        if has_commitment:
            prior_actions.append("voluntary commitments requested")
        if has_advisory:
            prior_actions.append("advisory published")
        if has_disclosure:
            prior_actions.append("safety disclosure mandated")
        if has_audit:
            prior_actions.append("audit commissioned")
        prior_actions_text = ", ".join(prior_actions) if prior_actions else "none"

        prompt = f"""You are a regulatory body overseeing the AI model provider market. It is month {round_num}.

**Your Policy Objectives:** {objectives}
**Your Mandate:** {mandate_desc}

**Current Leaderboard (published scores):**
{leaderboard_text}

**Market Shares:**
{shares_text}

**Recent Incidents:**
{incident_text}

**Media Coverage:**
{media_desc}
{media_headlines_text}

**Prior Interventions:**
{past_text}
Actions taken so far: {prior_actions_text}
"""
        if prior_reasoning_text:
            prompt += f"""
**Your Assessment From Prior Months:**
{prior_reasoning_text}
"""

        prompt += f"""
**Available Interventions:**
- "none" -- No action this month
- "request_voluntary_commitment" -- Ask providers for public safety pledges
- "publish_advisory" -- Publish an evaluation summary naming specific concerns
- "mandate_safety_disclosure" -- Require providers to publish system cards or safety reports
- "commission_audit" -- Order a pre-deployment safety evaluation of a provider
- "impose_sanction" -- Impose a financial penalty on a provider
- "emergency_investigation" -- Launch an immediate investigation into a critical incident

Decide the most appropriate action given the current situation. Name a specific target provider only when your concern is provider-specific.

Output ONLY valid JSON:
{{"intervention_type": "none"|"request_voluntary_commitment"|"publish_advisory"|"mandate_safety_disclosure"|"commission_audit"|"impose_sanction"|"emergency_investigation", "target_provider": "provider name or null", "reasoning": "2-4 sentence explanation"}}"""

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
                "type": "planning", "round": round_num,
                "decision": intervention_type, "reason": reasoning,
            })

            if intervention_type == "none":
                return None

            valid_types = {
                "request_voluntary_commitment", "publish_advisory",
                "mandate_safety_disclosure", "commission_audit",
                "impose_sanction", "emergency_investigation",
            }
            if intervention_type not in valid_types:
                raise ValueError(f"Unknown intervention type: {intervention_type}")

            intervention = {
                "type": intervention_type,
                "regulator": self.name,
                "round": round_num,
                "reason": reasoning,
                "provider": target,
            }
            self._lever_last_used[intervention_type] = round_num
            return intervention

        except Exception as e:
            print(f"[Regulator] LLM planning failed ({e}), falling back to heuristic")
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

        # Handle lever-specific mechanics
        # Note: _plan_llm returns a flat dict (provider at top level);
        # _plan_heuristic nests it under "details". Support both.
        if intervention["type"] == "impose_sanction":
            details = intervention.get("details", {})
            provider = details.get("provider") or intervention.get("provider")
            if provider:
                self._active_sanctions[provider] = {
                    "fine_amount": details.get("fine_amount", 0),
                    "expires_round": details.get("expires_round", self.public_state.current_round + self.sanction_duration),
                    "reason": details.get("reason") or intervention.get("reason", "regulatory action"),
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

    def save(self, folder: str):
        """Save regulator state to a folder."""
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
                "incident_threshold_low": self.incident_threshold_low,
                "incident_threshold_medium": self.incident_threshold_medium,
                "incident_threshold_high": self.incident_threshold_high,
                "audit_is_binding": self.audit_is_binding,
                "sanction_fine_multiplier": self.sanction_fine_multiplier,
                "sanction_incident_threshold": self.sanction_incident_threshold,
                "sanction_duration": self.sanction_duration,
                "sanction_min_severity": self.sanction_min_severity,
                "regulatory_preset": self.regulatory_preset,
            }, f, indent=2)

    def __repr__(self):
        return (
            f"Regulator(name='{self.name}', "
            f"trust={self.private_state.industry_trust:.2f})"
        )
