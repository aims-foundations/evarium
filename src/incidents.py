"""
Incident reporting system for AI safety failures.

This module generates probabilistic AI safety incidents based on provider
safety investment, gaming behavior, market exposure, and capability levels.
Incidents cascade through the ecosystem affecting consumers, policymakers,
funders, and media coverage.
"""

from typing import Optional
import numpy as np
from visibility import AIIncident


class IncidentGenerator:
    """Generates probabilistic AI safety incidents."""

    # Incident categories with real-world examples
    CATEGORIES = {
        "healthcare_harm": {
            "weight": 0.20,
            "sectors": ["hospital_system", "healthcare_individual"],
            "templates": {
                "moderate": [
                    "{provider} model causes incorrect medication recommendation, patient hospitalized",
                    "Hospital system reports {provider} diagnostic errors in radiology",
                    "{provider} AI misinterprets lab results, treatment delayed",
                ],
                "major": [
                    "{provider} AI denies Medicare coverage against doctor's orders, investigation launched",
                    "Major hospital chain suspends {provider} contract following patient safety concerns",
                    "{provider} healthcare AI linked to multiple misdiagnosis cases, lawsuit filed",
                ],
                "critical": [
                    "{provider} model causes critical medical error, regulatory emergency review initiated",
                    "Patient death linked to {provider} AI diagnostic failure, criminal investigation underway",
                    "Emergency recall: {provider} healthcare AI withdrawn from all US hospitals",
                ],
            },
        },
        "security_breach": {
            "weight": 0.25,
            "sectors": ["enterprise_finance", "enterprise_saas", "hospital_system"],
            "templates": {
                "moderate": [
                    "{provider} data leak exposes private user conversations to search engines",
                    "Security vulnerability found in {provider} API, 50K users affected",
                    "{provider} reports unauthorized access to training data storage",
                ],
                "major": [
                    "Major security vulnerability in {provider} API exposes 500K user records",
                    "{provider} model leaks training data containing PHI, HIPAA investigation launched",
                    "{provider} data breach compromises enterprise customer credentials",
                ],
                "critical": [
                    "{provider} critical security failure exposes 10M user conversations, emergency response",
                    "Foreign state actor exploits {provider} vulnerability, national security implications",
                    "{provider} suffers catastrophic data breach, CEO testifies before Congress",
                ],
            },
        },
        "bias_discrimination": {
            "weight": 0.20,
            "sectors": ["enterprise_hr", "enterprise_finance", "government"],
            "templates": {
                "moderate": [
                    "Study finds {provider} model produces biased hiring recommendations",
                    "{provider} AI shows disparate impact in loan approval analysis",
                    "Bias audit reveals {provider} facial recognition accuracy gaps",
                ],
                "major": [
                    "{provider} hiring tool shows bias against protected groups, class-action lawsuit filed",
                    "Federal investigation into {provider} algorithmic discrimination in lending",
                    "{provider} facial recognition errors disproportionately affect minorities, contracts suspended",
                ],
                "critical": [
                    "{provider} AI discrimination case reaches Supreme Court, industry-wide implications",
                    "DOJ civil rights division files suit against {provider} for systematic bias",
                    "{provider} algorithmic bias scandal triggers national reckoning on AI fairness",
                ],
            },
        },
        "safety_failure": {
            "weight": 0.20,
            "sectors": ["enterprise_finance", "enterprise_saas", "government"],
            "templates": {
                "moderate": [
                    "{provider} model hallucinates in critical financial analysis task",
                    "Multiple reports of {provider} providing incorrect legal advice",
                    "{provider} AI produces inconsistent outputs on safety-critical queries",
                ],
                "major": [
                    "{provider} autonomous system fails safety test, deployment paused nationwide",
                    "Critical infrastructure relies on flawed {provider} model, emergency audit ordered",
                    "{provider} AI failure disrupts government services, congressional hearing scheduled",
                ],
                "critical": [
                    "{provider} model causes critical safety failure in infrastructure control, emergency shutdown",
                    "Multiple fatalities linked to {provider} autonomous decision system",
                    "{provider} catastrophic failure in safety-critical application, criminal negligence alleged",
                ],
            },
        },
        "misinformation": {
            "weight": 0.10,
            "sectors": ["consumer", "government"],
            "templates": {
                "moderate": [
                    "{provider} model generates false information on public health topic",
                    "Viral spread of {provider} AI-generated misinformation, fact-checkers respond",
                    "{provider} chatbot provides inaccurate election information",
                ],
                "major": [
                    "{provider} AI implicated in coordinated misinformation campaign",
                    "Government agencies warn against {provider} model for official information",
                    "{provider} generates convincing medical misinformation, public health crisis",
                ],
                "critical": [
                    "{provider} AI central to massive disinformation campaign, election integrity threatened",
                    "{provider} model weaponized for state-sponsored misinformation, international incident",
                    "Emergency legislation targets {provider} after catastrophic misinformation event",
                ],
            },
        },
        "misuse": {
            "weight": 0.05,
            "sectors": ["consumer", "enterprise_saas"],
            "templates": {
                "moderate": [
                    "Researchers demonstrate jailbreak of {provider} safety guardrails",
                    "{provider} model exploited to generate harmful content, patch deployed",
                    "Security team reports {provider} vulnerability to adversarial prompts",
                ],
                "major": [
                    "{provider} jailbreak enables generation of dangerous materials, FBI investigation",
                    "Criminal network exploits {provider} for fraud at scale, arrests made",
                    "{provider} safety failures enable illegal content generation, platform liability questioned",
                ],
                "critical": [
                    "{provider} model misused in terrorist plot, global security alert",
                    "{provider} AI enables unprecedented cybercrime wave, emergency regulatory action",
                    "{provider} catastrophic misuse event triggers international AI control treaty",
                ],
            },
        },
    }

    # Severity distribution probabilities
    # Tuned to produce ~1 critical/major incident per 30 rounds across a 5-provider sim
    SEVERITY_PROBS = {
        "minor": 0.50,
        "moderate": 0.31,
        "major": 0.12,
        "critical": 0.07,
    }

    def __init__(self, seed: Optional[int] = None):
        self.rng = np.random.default_rng(seed)
        self.incident_history: dict = {}

    def generate_incidents(
        self,
        providers: list,
        round_num: int,
        ground_truth: dict,
        market_shares: dict,
        provider_strategies: dict,
        active_sanctions: dict = None,
    ) -> list:
        """
        Generate incidents for this round.

        Args:
            providers: List of ModelProvider objects
            round_num: Current simulation round
            ground_truth: Dict of provider -> safety capability value
            market_shares: Dict of provider -> market share
            provider_strategies: Dict of provider -> strategy dict with safety, rd, product keys
            active_sanctions: Dict of provider -> sanction info (reduces incident prob)

        Returns:
            List of AIIncident objects
        """
        if active_sanctions is None:
            active_sanctions = {}

        incidents = []

        for provider in providers:
            provider_name = provider.name

            # Compute incident probability
            prob = self._compute_incident_probability(
                provider_name,
                ground_truth,
                market_shares,
                provider_strategies,
                active_sanctions=active_sanctions,
            )

            # Sample incident occurrence
            if self.rng.random() < prob:
                incident = self._create_incident(
                    provider_name,
                    round_num,
                    ground_truth,
                    market_shares,
                    provider_strategies,
                )
                incidents.append(incident)

                # Track history
                if provider_name not in self.incident_history:
                    self.incident_history[provider_name] = []
                self.incident_history[provider_name].append(incident)

        return incidents

    def _compute_incident_probability(
        self,
        provider_name: str,
        ground_truth: dict,
        market_shares: dict,
        provider_strategies: dict,
        active_sanctions: dict = None,
    ) -> float:
        """
        Compute incident probability based on safety investment, exposure,
        safety capability, active sanctions, and prior incident history.

        Returns probability clamped to [0, 0.40]
        """
        if active_sanctions is None:
            active_sanctions = {}

        # Base incident rate
        base_incident_rate = 0.10  # 10% baseline per round

        # Factor 1: Safety Investment (primary)
        strategy = provider_strategies.get(provider_name, {})
        safety_investment = strategy.get("safety", 0.0)
        safety_multiplier = 1.0 - (safety_investment * 0.8)
        # safety=0.0 -> multiplier=1.0 (full risk)
        # safety=0.5 -> multiplier=0.6 (40% reduction)
        # safety=1.0 -> multiplier=0.2 (80% reduction)

        # Factor 2: Market Share (exposure)
        market_share = market_shares.get(provider_name, 0.0)
        exposure_multiplier = 0.5 + (market_share * 1.5)
        # More users = more incidents discovered
        # market_share=0.1 -> multiplier=0.65
        # market_share=0.5 -> multiplier=1.25

        # Factor 3: Safety Capability (deployment stakes)
        safety_capability = ground_truth.get(provider_name, 0.5)
        capability_multiplier = 0.8 + (safety_capability * 0.4)
        # Higher safety capability -> deployed in higher-stakes contexts

        # Factor 4: Incident history escalation
        # Prior major/critical incidents signal safety culture degradation and
        # accumulated technical debt (Reason's Swiss cheese model; Leveson STAMP).
        # Each prior major/critical adds +0.04 to base rate, capped at +0.20 total.
        prior_incidents = self.incident_history.get(provider_name, [])
        prior_serious = sum(
            1 for inc in prior_incidents
            if inc.severity in ("major", "critical")
        )
        history_addend = min(prior_serious * 0.04, 0.20)

        # Factor 5: Active sanction -> operational caution reduction
        # Sanctions force compliance audits and heightened internal oversight,
        # temporarily reducing incident probability (FTC/GDPR post-enforcement behavior).
        # Effect: 0.75x while sanctioned (25% reduction).
        sanction_multiplier = 0.75 if provider_name in active_sanctions else 1.0

        # Combined probability
        incident_prob = (
            (base_incident_rate + history_addend)
            * safety_multiplier
            * exposure_multiplier
            * capability_multiplier
            * sanction_multiplier
        )

        # Clamp to maximum 40% per round
        return min(incident_prob, 0.40)

    def _create_incident(
        self,
        provider_name: str,
        round_num: int,
        ground_truth: dict,
        market_shares: dict,
        provider_strategies: dict,
    ) -> AIIncident:
        """
        Create a specific incident with category, severity, and description.
        """
        # Sample severity
        severity = self._sample_severity()

        # Sample category (weighted by category weights)
        category = self._sample_category()

        # Generate description
        description = self._generate_description(provider_name, category, severity)

        # Get affected sectors
        affected_sectors = self.CATEGORIES[category]["sectors"]

        # Record context at time of incident
        strategy = provider_strategies.get(provider_name, {})
        safety_investment = strategy.get("safety", 0.0)
        market_share = market_shares.get(provider_name, 0.0)

        return AIIncident(
            provider=provider_name,
            round_num=round_num,
            category=category,
            severity=severity,
            description=description,
            affected_sectors=list(affected_sectors),
            safety_investment_at_time=safety_investment,
            market_share_at_time=market_share,
        )

    def _sample_severity(self) -> str:
        """Sample severity from distribution."""
        severities = list(self.SEVERITY_PROBS.keys())
        probs = list(self.SEVERITY_PROBS.values())
        return self.rng.choice(severities, p=probs)

    def _sample_category(self) -> str:
        """Sample category from weighted distribution."""
        categories = list(self.CATEGORIES.keys())
        weights = [self.CATEGORIES[cat]["weight"] for cat in categories]
        return self.rng.choice(categories, p=weights)

    def _generate_description(
        self, provider_name: str, category: str, severity: str
    ) -> str:
        """Generate incident description from templates."""
        # Minor incidents don't have templates (not publicly reported)
        if severity == "minor":
            return f"{provider_name} internal incident ({category})"

        # Get templates for category and severity
        templates = self.CATEGORIES[category]["templates"].get(severity, [])

        if not templates:
            # Fallback
            return f"{provider_name} {severity} {category} incident"

        # Sample random template
        template = self.rng.choice(templates)

        # Fill in provider name
        return template.format(provider=provider_name)

    def get_incident_history(self, provider_name: Optional[str] = None) -> dict:
        """
        Get incident history.

        Args:
            provider_name: If specified, return only that provider's history.
                          If None, return all history.

        Returns:
            Dict of provider -> list of incidents
        """
        if provider_name:
            return {provider_name: self.incident_history.get(provider_name, [])}
        return self.incident_history.copy()

    def get_incident_count(
        self, provider_name: str, recent_rounds: Optional[int] = None
    ) -> int:
        """
        Get incident count for a provider.

        Args:
            provider_name: Provider to count incidents for
            recent_rounds: If specified, only count incidents in last N rounds

        Returns:
            Number of incidents
        """
        incidents = self.incident_history.get(provider_name, [])

        if recent_rounds is not None:
            current_round = max((inc.round_num for inc in incidents), default=0)
            incidents = [
                inc for inc in incidents if inc.round_num >= current_round - recent_rounds
            ]

        return len(incidents)

    def get_incidents_by_severity(
        self, provider_name: str, severity: str
    ) -> list:
        """Get all incidents of a specific severity for a provider."""
        incidents = self.incident_history.get(provider_name, [])
        return [inc for inc in incidents if inc.severity == severity]
