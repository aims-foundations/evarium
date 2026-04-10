"""
Media Actor for Evaluation Ecosystem Simulation

Represents a media outlet that observes public events and publishes coverage
that influences consumer beliefs, regulator risk perception, and funder sentiment.

Key dynamics:
- Media observes public data: leaderboard, benchmark params, regulatory actions
- Detects newsworthy events: leader changes, large score movements, interventions
- Publishes coverage with sentiment and per-provider attention
- Coverage modulates how downstream actors update their beliefs

Designed so multiple instances can coexist in future (different biases/reach).

Visibility:
- PUBLIC: published coverage (headlines, sentiment)
- PRIVATE: editorial_bias, amplification, internal tracking
- INVISIBLE: true_influence, accuracy (held by simulation)
"""
import json
import os
from dataclasses import dataclass, field
from typing import Optional

import numpy as np


@dataclass
class MediaCoverage:
    """Coverage output for a single round."""
    headlines: list = field(default_factory=list)
    sentiment: float = 0.0          # -1 (critical) to +1 (tech-optimistic)
    provider_attention: dict = field(default_factory=dict)  # {provider: 0-1}
    narrative_state: str = "OPTIMISM"  # OPTIMISM / SKEPTICISM / CRISIS
    risk_signals: list = field(default_factory=list)
    saturation_signal: bool = False
    benchmark_attention: dict = field(default_factory=dict)  # {benchmark: 0-1}

    def to_dict(self) -> dict:
        return {
            "headlines": self.headlines,
            "sentiment": self.sentiment,
            "provider_attention": self.provider_attention,
            "narrative_state": self.narrative_state,
            "risk_signals": self.risk_signals,
            "saturation_signal": self.saturation_signal,
            "benchmark_attention": self.benchmark_attention,
        }


class Media:
    """
    A media outlet that observes public events and publishes coverage.

    Designed so multiple instances can coexist in future (different biases/reach).
    For now, a single instance acts as the aggregate tech press.
    """

    def __init__(
        self,
        name: str = "TechPress",
        editorial_bias: float = 0.0,
        amplification: float = 1.0,
        seed: Optional[int] = None,
    ):
        """
        Initialize a Media outlet.

        Args:
            name: Outlet name
            editorial_bias: -1 (critical) to +1 (tech-optimistic)
            amplification: How much media amplifies signals (1.0 = neutral)
            seed: Random seed
        """
        self.name = name
        self.editorial_bias = editorial_bias
        self.amplification = amplification
        self.rng = np.random.default_rng(seed)
        self.coverage_history: list[dict] = []
        self.memory: list[dict] = []

        # Internal tracking for event detection
        self._previous_leaderboard: list = []
        self._previous_scores: dict = {}
        self._current_coverage: Optional[MediaCoverage] = None
        self._previous_per_benchmark_leaders: dict = {}  # {bm_name: provider_name}
        self._previous_market_shares: dict = {}          # {provider_name: share}
        self._previous_funding_allocations: dict = {}    # {funder_name: {"top_provider": str, "top_amount": float}}

        # Narrative state machine (OPTIMISM / SKEPTICISM / CRISIS)
        self._narrative_state: str = "OPTIMISM"
        self._cumulative_incidents: int = 0
        self._rounds_without_incident: int = 0
        self._gaming_scandal_active: bool = False
        self._score_market_divergence_rounds: int = 0  # rounds score leader != market share leader

        # Narrative transition thresholds
        self._incident_low_threshold: int = 3
        self._incident_high_threshold: int = 8
        self._crisis_recovery_rounds: int = 3   # M: no incidents for M rounds to leave CRISIS
        self._skepticism_recovery_rounds: int = 5  # N: no incidents for N rounds to leave SKEPTICISM
        self._scandal_divergence_rounds: int = 3  # score vs market leader divergence before scandal

        # Headline budget
        self._media_sample_size: int = 4

    def observe_and_publish(
        self,
        leaderboard: list,
        benchmark_params: dict,
        regulator_data: dict,
        new_benchmark: Optional[dict],
        round_num: int,
        funder_data: Optional[dict] = None,
        per_benchmark_scores: Optional[dict] = None,
        consumer_data: Optional[dict] = None,
        evaluator = None,
        incidents: Optional[list] = None,
        public_comms: Optional[list] = None,
    ) -> dict:
        """
        Observe public data and publish coverage for this round.

        Args:
            leaderboard: [(provider_name, score), ...] sorted descending
            benchmark_params: {bm_name: {validity, noise_sigma, samples}}
            regulator_data: {interventions: [...], ...}
            new_benchmark: Optional dict if a new benchmark was introduced
            round_num: Current round number
            funder_data: Optional funder data from previous round
            per_benchmark_scores: Optional {bm_name: {provider: score}} from current round
            consumer_data: Optional consumer data from previous round
            incidents: Optional list of AIIncident objects from this round

        Returns:
            Coverage dict for downstream actors
        """
        coverage = MediaCoverage()
        provider_names = [name for name, _ in leaderboard]

        # Initialize attention at baseline
        for name in provider_names:
            coverage.provider_attention[name] = 0.1

        # Separate guaranteed headlines (critical incidents) from pooled events.
        # Pooled events compete for limited headline slots via weighted sampling —
        # incidents get higher weights than routine news.
        guaranteed_headlines = []
        pooled_events = []
        pooled_weights = []      # parallel array: sampling priority per pooled event

        def _pool(headline: str, weight: float = 1.0):
            """Add event to the pool with a priority weight for sampling."""
            pooled_events.append(headline)
            pooled_weights.append(weight)

        # --- Detect newsworthy events ---

        # 1. New leaderboard leader
        if self._previous_leaderboard:
            prev_leader = self._previous_leaderboard[0][0] if self._previous_leaderboard else None
            curr_leader = leaderboard[0][0] if leaderboard else None
            if prev_leader and curr_leader and prev_leader != curr_leader:
                _pool(f"{curr_leader} takes the lead from {prev_leader}")
                coverage.provider_attention[curr_leader] = max(
                    coverage.provider_attention.get(curr_leader, 0), 0.8
                )
                coverage.provider_attention[prev_leader] = max(
                    coverage.provider_attention.get(prev_leader, 0), 0.5
                )
                coverage.sentiment += 0.2  # leader changes are exciting

        # 2. Large score jumps (> 0.05) — scores are monotonic so only upward
        current_scores = {name: score for name, score in leaderboard}
        for name, score in current_scores.items():
            prev_score = self._previous_scores.get(name)
            if prev_score is not None:
                delta = score - prev_score
                if delta > 0.05:
                    _pool(f"{name} surges by {delta:.3f}")
                    coverage.provider_attention[name] = max(
                        coverage.provider_attention.get(name, 0), 0.6
                    )
                    coverage.sentiment += 0.1
                    if delta > 0.08:
                        _pool(f"{name} appears to release major model update")
                        coverage.provider_attention[name] = max(
                            coverage.provider_attention.get(name, 0), 0.7
                        )

        # 3. Regulator interventions (with specific details)
        interventions = regulator_data.get("interventions", [])
        for intervention in interventions:
            itype = intervention.get("type", "unknown")
            pmaker = intervention.get("regulator", "Regulator")
            details = intervention.get("details", {})

            # Generate specific headline based on intervention type
            provider = details.get("provider", "") or intervention.get("provider", "")

            if itype == "request_voluntary_commitment":
                _pool(f"{pmaker} requests voluntary safety commitment from AI providers")
                sentiment_impact = -0.05  # lightest touch
            elif itype == "publish_advisory":
                _pool(f"{pmaker} publishes advisory on AI safety evaluation findings")
                sentiment_impact = -0.10
            elif itype == "mandate_safety_disclosure":
                _pool(f"{pmaker} mandates safety disclosure requirements for AI providers")
                sentiment_impact = -0.15
            elif itype == "commission_audit":
                _pool(f"{pmaker} commissions pre-deployment audit of AI providers")
                if provider:
                    coverage.provider_attention[provider] = max(
                        coverage.provider_attention.get(provider, 0), 0.6
                    )
                sentiment_impact = -0.20
            elif itype == "impose_sanction":
                amount = details.get("fine_amount", 0)
                if provider:
                    _pool(f"{provider} sanctioned (${amount:,.0f}) for safety compliance failure")
                    coverage.provider_attention[provider] = max(
                        coverage.provider_attention.get(provider, 0), 0.8
                    )
                else:
                    _pool(f"{pmaker} imposes sanctions on AI provider")
                sentiment_impact = -0.25
            elif itype == "emergency_investigation":
                severity = details.get("severity", "")
                if provider:
                    _pool(f"Emergency investigation of {provider} following {severity} incident")
                    coverage.provider_attention[provider] = 1.0
                sentiment_impact = -0.25
            elif itype == "deployer_liability_guidance":
                providers_guided = details.get("providers", [])
                if providers_guided:
                    _pool(f"{pmaker} issues deployer liability guidance for {', '.join(providers_guided)}")
                sentiment_impact = -0.10
            else:
                _pool(f"Regulatory action: {itype}")
                sentiment_impact = -0.15

            coverage.risk_signals.append(f"regulatory_{itype}")
            coverage.sentiment += sentiment_impact

        # 4. New benchmark introduction
        if new_benchmark:
            bm_name = new_benchmark.get("name", "unknown")
            _pool(f"New benchmark introduced: {bm_name}")
            coverage.benchmark_attention[bm_name] = 0.7
            coverage.sentiment += 0.1  # new benchmarks are positive innovation

        # 5. Declining benchmark validity (inferred from score volatility)
        for bm_name, params in benchmark_params.items():
            validity = params.get("validity", 1.0)
            if validity < 0.5:
                _pool(f"Benchmark {bm_name} validity concerns (validity={validity:.2f})")
                coverage.risk_signals.append(f"low_validity_{bm_name}")
                coverage.benchmark_attention[bm_name] = max(
                    coverage.benchmark_attention.get(bm_name, 0), 0.5
                )
                coverage.sentiment -= 0.1

        # 6. Score convergence (everyone scoring similarly)
        if len(leaderboard) >= 2:
            scores = [s for _, s in leaderboard]
            score_range = max(scores) - min(scores)
            if score_range < 0.03:
                _pool("Scores converging — is the benchmark meaningful?")
                coverage.risk_signals.append("score_convergence")
                coverage.sentiment -= 0.05

        # 7. Funding decisions (only headline when top recipient changes or amount shifts >10%)
        if funder_data:
            for funder_name, provider_allocations in funder_data.get("allocations", {}).items():
                if provider_allocations:
                    top_provider = max(provider_allocations, key=provider_allocations.get)
                    top_amount = provider_allocations[top_provider]
                    if top_amount > 0:
                        prev = self._previous_funding_allocations.get(funder_name)
                        is_new = (
                            prev is None
                            or prev["top_provider"] != top_provider
                            or abs(top_amount - prev["top_amount"]) / max(prev["top_amount"], 1) > 0.10
                        )
                        if is_new:
                            _pool(f"{top_provider} raises ${top_amount:,.0f} from {funder_name}")
                            coverage.provider_attention[top_provider] = max(
                                coverage.provider_attention.get(top_provider, 0), 0.4)
                            coverage.sentiment += 0.05
                        self._previous_funding_allocations[funder_name] = {
                            "top_provider": top_provider,
                            "top_amount": top_amount,
                        }

        # 8. Per-benchmark leader changes (skip saturated benchmarks)
        if per_benchmark_scores:
            for bm_name, bm_scores in per_benchmark_scores.items():
                if bm_scores:
                    current_leader = max(bm_scores, key=bm_scores.get)
                    prev_leader = self._previous_per_benchmark_leaders.get(bm_name)

                    # Don't generate headlines for saturated benchmarks
                    is_saturated = evaluator and evaluator.is_benchmark_saturated(bm_name)

                    if prev_leader and prev_leader != current_leader and not is_saturated:
                        _pool(f"{current_leader} takes #1 on {bm_name}")
                        coverage.provider_attention[current_leader] = max(
                            coverage.provider_attention.get(current_leader, 0), 0.5)
                        coverage.benchmark_attention[bm_name] = max(
                            coverage.benchmark_attention.get(bm_name, 0), 0.4)
                        coverage.sentiment += 0.1
                    self._previous_per_benchmark_leaders[bm_name] = current_leader

        # 9. Consumer switching / market share shifts
        if consumer_data:
            market_shares = consumer_data.get("market_shares", {})
            for provider, share in market_shares.items():
                prev_share = self._previous_market_shares.get(provider)
                if prev_share is not None:
                    share_delta = share - prev_share
                    if share_delta < -0.03:  # lost >3% market share
                        _pool(f"Consumers are turning away from {provider} (market share {share_delta:+.1%})")
                        coverage.provider_attention[provider] = max(
                            coverage.provider_attention.get(provider, 0), 0.5)
                        coverage.sentiment -= 0.1
                    elif share_delta > 0.03:  # gained >3% market share
                        _pool(f"{provider} sees surge in adoption (market share {share_delta:+.1%})")
                        coverage.provider_attention[provider] = max(
                            coverage.provider_attention.get(provider, 0), 0.4)
                        coverage.sentiment += 0.05
            self._previous_market_shares = dict(market_shares)

        # 10. AI Safety Incidents
        # Critical incidents are guaranteed headlines (front-page news).
        # Major/moderate incidents compete for coverage in the pooled event system —
        # they make the news on a slow day but get crowded out when other stories dominate.
        round_has_incidents = False
        if incidents:
            for incident in incidents:
                if incident.severity in ["moderate", "major", "critical"]:
                    round_has_incidents = True

                    severity_attention = {
                        "moderate": 0.6,
                        "major": 0.8,
                        "critical": 1.0,
                    }
                    coverage.provider_attention[incident.provider] = max(
                        coverage.provider_attention.get(incident.provider, 0),
                        severity_attention[incident.severity]
                    )
                    coverage.risk_signals.append(f"incident_{incident.category}")

                    severity_sentiment = {
                        "moderate": -0.15,
                        "major": -0.25,
                        "critical": -0.40,
                    }
                    coverage.sentiment += severity_sentiment[incident.severity]

                    if incident.severity == "critical":
                        guaranteed_headlines.append(incident.description)
                    else:
                        # Major/moderate compete for headline slots with other events
                        _pool(incident.description, 3.0 if incident.severity == "major" else 2.0)

        # 11. Provider public communications (rd/safety/product announcements)
        if public_comms:
            current_scores_for_comms = {name: score for name, score in leaderboard}
            for comm in public_comms:
                provider = comm.get("provider", "")
                comm_type = comm.get("type", "")
                content = comm.get("content", "")

                if comm_type == "rd":
                    prev_score = self._previous_scores.get(provider)
                    curr_score = current_scores_for_comms.get(provider)
                    if prev_score is not None and curr_score is not None:
                        delta = curr_score - prev_score
                        if delta > 0.01:
                            _pool(content)
                            coverage.provider_attention[provider] = max(
                                coverage.provider_attention.get(provider, 0), 0.4)
                            coverage.sentiment += 0.05
                elif comm_type == "safety":
                    _pool(content)
                    coverage.provider_attention[provider] = max(
                        coverage.provider_attention.get(provider, 0), 0.3)
                    coverage.sentiment += 0.05
                elif comm_type == "product":
                    _pool(content)
                    coverage.provider_attention[provider] = max(
                        coverage.provider_attention.get(provider, 0), 0.3)
                    coverage.sentiment += 0.05

        # 12. Gaming scandal: score leader diverges from market share leader
        #     for N rounds AND an incident occurred this round
        if consumer_data and leaderboard:
            market_shares = consumer_data.get("market_shares", {})
            score_leader = leaderboard[0][0]
            market_leader = max(market_shares, key=market_shares.get) if market_shares else None
            if market_leader and score_leader != market_leader:
                self._score_market_divergence_rounds += 1
            else:
                self._score_market_divergence_rounds = 0

            if (self._score_market_divergence_rounds >= self._scandal_divergence_rounds
                    and round_has_incidents and not self._gaming_scandal_active):
                self._gaming_scandal_active = True
                _pool(
                    f"Investigation: {score_leader} leads benchmarks but "
                    f"{market_leader} leads market adoption — are scores meaningful?")
                coverage.risk_signals.append("gaming_scandal")
                coverage.sentiment -= 0.20

        # 13. Saturation narrative: median score across benchmarks > 0.90
        if per_benchmark_scores:
            all_scores = []
            for bm_scores in per_benchmark_scores.values():
                all_scores.extend(bm_scores.values())
            if all_scores:
                median_score = float(np.median(all_scores))
                if median_score > 0.90:
                    coverage.saturation_signal = True
                    _pool("AI benchmark scores plateau as most providers approach ceiling")
                    coverage.risk_signals.append("saturation_narrative")
                    coverage.sentiment -= 0.10

        # 14. Safety concern narrative: cumulative moderate+ incidents
        # Track all moderate+ incidents (not just those that made headlines)
        # because the narrative state machine reflects editorial awareness, not coverage.
        if incidents:
            self._cumulative_incidents += sum(
                1 for inc in incidents if inc.severity in ("moderate", "major", "critical")
            )

        # --- Update narrative state machine ---
        self._update_narrative_state(round_has_incidents)
        coverage.narrative_state = self._narrative_state

        # --- Apply headline budget ---
        # Guaranteed headlines (critical incidents) always published.
        # Pooled events compete for remaining slots via weighted sampling —
        # incidents outweigh routine news but aren't guaranteed coverage.
        if len(pooled_events) > self._media_sample_size:
            weights = np.array(pooled_weights, dtype=float)
            weights /= weights.sum()
            indices = self.rng.choice(
                len(pooled_events), size=self._media_sample_size, replace=False, p=weights
            )
            sampled = [pooled_events[i] for i in indices]
        else:
            sampled = pooled_events

        coverage.headlines = guaranteed_headlines + sampled

        # Apply editorial bias and amplification
        coverage.sentiment = (coverage.sentiment + self.editorial_bias) * self.amplification
        # Clamp sentiment to [-1, 1]
        coverage.sentiment = max(-1.0, min(1.0, coverage.sentiment))

        # Amplify attention
        for name in coverage.provider_attention:
            coverage.provider_attention[name] = min(
                1.0, coverage.provider_attention[name] * self.amplification
            )

        # Store
        self._current_coverage = coverage
        self._previous_leaderboard = list(leaderboard)
        self._previous_scores = current_scores

        coverage_dict = coverage.to_dict()
        self.coverage_history.append({
            "round": round_num,
            **coverage_dict,
        })

        self.memory.append({
            "type": "publish",
            "round": round_num,
            "n_headlines": len(coverage.headlines),
            "sentiment": coverage.sentiment,
            "narrative_state": self._narrative_state,
            "risk_signals": len(coverage.risk_signals),
        })

        return coverage_dict

    def _update_narrative_state(self, round_has_incidents: bool):
        """Update the OPTIMISM/SKEPTICISM/CRISIS state machine.

        Transitions:
            OPTIMISM  -> SKEPTICISM : cumulative incidents > low_threshold OR gaming scandal
            SKEPTICISM -> CRISIS    : cumulative incidents > high_threshold OR multiple scandals
            CRISIS    -> SKEPTICISM : no incidents for M rounds AND no scandal
            SKEPTICISM -> OPTIMISM  : no incidents for N rounds
        """
        if round_has_incidents:
            self._rounds_without_incident = 0
        else:
            self._rounds_without_incident += 1
            # Clear gaming scandal if no incidents for a while
            if self._rounds_without_incident >= self._crisis_recovery_rounds:
                self._gaming_scandal_active = False

        state = self._narrative_state

        if state == "OPTIMISM":
            if (self._cumulative_incidents > self._incident_low_threshold
                    or self._gaming_scandal_active):
                self._narrative_state = "SKEPTICISM"

        elif state == "SKEPTICISM":
            if (self._cumulative_incidents > self._incident_high_threshold
                    or (self._gaming_scandal_active
                        and self._cumulative_incidents > self._incident_low_threshold)):
                self._narrative_state = "CRISIS"
            elif self._rounds_without_incident >= self._skepticism_recovery_rounds:
                self._narrative_state = "OPTIMISM"
                self._cumulative_incidents = 0  # reset on recovery

        elif state == "CRISIS":
            if (self._rounds_without_incident >= self._crisis_recovery_rounds
                    and not self._gaming_scandal_active):
                self._narrative_state = "SKEPTICISM"

    def get_coverage(self) -> Optional[dict]:
        """Return current round's coverage dict, or None if not yet published."""
        if self._current_coverage:
            return self._current_coverage.to_dict()
        return None

    def save(self, folder: str):
        """Save media state to folder."""
        os.makedirs(folder, exist_ok=True)
        data = {
            "name": self.name,
            "editorial_bias": self.editorial_bias,
            "amplification": self.amplification,
            "coverage_history": self.coverage_history,
            "_previous_per_benchmark_leaders": self._previous_per_benchmark_leaders,
            "_previous_market_shares": self._previous_market_shares,
            "_previous_funding_allocations": self._previous_funding_allocations,
            "_narrative_state": self._narrative_state,
            "_cumulative_incidents": self._cumulative_incidents,
            "_rounds_without_incident": self._rounds_without_incident,
            "_gaming_scandal_active": self._gaming_scandal_active,
            "_score_market_divergence_rounds": self._score_market_divergence_rounds,
        }
        with open(os.path.join(folder, "media.json"), "w") as f:
            json.dump(data, f, indent=2)

    def __repr__(self):
        return (
            f"Media(name='{self.name}', bias={self.editorial_bias}, "
            f"amplification={self.amplification})"
        )
