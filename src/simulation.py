"""
Evaluation Ecosystem Simulation

Main simulation loop for studying competition dynamics between model providers
and the effects of Goodhart's law on benchmark validity.

Key visibility design:
- Simulation holds ground truth externally in ground_truth dict
- Actors only have access to public_state and private_state
- Ground truth is passed to evaluator for scoring, never to actors
"""
import json
import os
from dataclasses import dataclass, field, asdict
from typing import Optional

from actors.model_provider import ModelProvider
from actors.evaluator import Evaluator, Regulation
from visibility import ProviderGroundTruth, ConsumerGroundTruth, PolicymakerGroundTruth, FunderGroundTruth
from incidents import IncidentGenerator


def r4(x):
    """Round numeric values to 4 decimal places for storage precision.

    Recursively handles dicts, lists, and tuples. Non-numeric types pass through.
    Only applied at output/storage boundaries, not internal computation.
    """
    if isinstance(x, dict):
        return {k: r4(v) for k, v in x.items()}
    if isinstance(x, list):
        return [r4(v) for v in x]
    if isinstance(x, tuple):
        return tuple(r4(v) for v in x)
    if isinstance(x, (int, str, type(None), bool)):
        return x
    try:
        return round(float(x), 4)
    except (TypeError, ValueError):
        return x


# Policymaker regulatory style presets
# Simplified to use only currently implemented Policymaker parameters
POLICYMAKER_PRESETS = {
    "us_light_touch": {
        # Threshold / stance
        "intervention_threshold": 0.85,  # Very high bar — almost entirely hands-off until crisis
        "risk_tolerance": 0.85,          # Very high risk tolerance — strong market correction preference
        "policy_objectives": ["safety", "innovation", "free_market"],
        # Enforcement calibration (empirically grounded: FTC/DOJ enforcement patterns)
        "intervention_cooldown": 4,          # US regulatory cycles ~18-36 months; slow follow-up
        "sanction_fine_multiplier": 0.05,    # Minimal fines — US relies on consent orders, not direct % revenue fines
        "sanction_incident_threshold": 6,    # US needs a very clear, repeated pattern before sanctioning
        "sanction_duration": 1,              # Short-term — US consent decrees expire; market corrects quickly
        "mandate_risk_threshold": 0.90,      # US almost never mandates benchmark compliance (ex-post philosophy)
        "sanction_min_severity": "critical", # US only acts on critical incidents (not mere majors)
    },
    "eu_precautionary": {
        # Threshold / stance
        "intervention_threshold": 0.25,  # Very low threshold — strongly precautionary, acts at first signal
        "risk_tolerance": 0.10,          # Very low risk tolerance — prevent harm upfront aggressively
        "policy_objectives": ["safety", "fairness", "consumer_protection"],
        # Enforcement calibration (empirically grounded: GDPR/DMA/EU AI Act patterns)
        "intervention_cooldown": 2,          # EU follows up aggressively — ~6-12 month regulatory cycles
        "sanction_fine_multiplier": 0.50,    # Large economic bite (EU 7% global turnover ceiling)
        "sanction_incident_threshold": 1,    # EU sanctions on first pattern; very low bar
        "sanction_duration": 6,              # EU compliance cycles take longer; sanctions persist
        "mandate_risk_threshold": 0.35,      # EU mandates at low-moderate risk (ex-ante philosophy)
        "sanction_min_severity": "moderate", # EU acts on moderate+ incidents
    },
    "balanced": {
        "intervention_threshold": 0.50,
        "risk_tolerance": 0.5,
        "policy_objectives": ["safety", "fairness"],
        "intervention_cooldown": 3,
        "sanction_fine_multiplier": 0.22,
        "sanction_incident_threshold": 3,
        "sanction_duration": 3,
        "mandate_risk_threshold": 0.62,
        "sanction_min_severity": "major",
    },
}


@dataclass
class SimulationConfig:
    """Configuration for a simulation run."""
    # Simulation parameters
    n_rounds: int = 50
    seed: Optional[int] = 42

    # Evaluator/Benchmark parameters (single benchmark mode)
    benchmark_name: str = "capability_benchmark"
    benchmark_validity: float = 0.7  # alpha
    benchmark_exploitability: float = 0.5  # beta
    benchmark_noise: float = 0.1  # sigma

    # Multi-benchmark mode (if provided, overrides single benchmark params)
    # Each dict should have: name, validity, exploitability, noise_level, weight
    benchmarks: Optional[list] = None

    # Provider parameters
    rnd_efficiency: float = 0.01  # How much R&D improves true capability per round

    # S-curve capability dynamics
    capability_ceiling: float = 1.0
    diminishing_returns_rate: float = 3.0
    breakthrough_probability: float = 0.02
    breakthrough_magnitude: float = 0.05

    # Benchmark evolution
    benchmark_validity_decay_rate: float = 0.005
    benchmark_exploitability_growth_rate: float = 0.008

    # Benchmark introduction (evaluator introduces new benchmarks mid-simulation)
    benchmark_introduction_cooldown: int = 7
    max_benchmarks: int = 8  # Raised from 6 to accommodate realistic benchmark suite
    benchmark_sequence: Optional[list] = None  # Ordered list of benchmark dicts to introduce
    # Each dict: {"name": str, "validity": float, "exploitability": float, "noise_level": float, "weight": float}
    # Default realistic sequence inspired by real-world benchmarks (MMLU, HumanEval, GSM8K, etc.)

    # Planning mode
    llm_mode: bool = False  # If True, use LLM for provider planning; if False, use heuristics

    # Consumer LLM mode
    consumer_llm_mode: bool = False  # Master switch for ALL consumer LLM reasoning
    consumer_llm_individuals: bool = False  # When consumer_llm_mode=True, use LLM for individuals?
    consumer_llm_organizations: bool = True  # When consumer_llm_mode=True, use LLM for orgs?

    # New actor settings
    enable_consumers: bool = False  # Enable consumer market
    enable_policymakers: bool = False  # Enable policymaker actors
    enable_funders: bool = False  # Enable funder actors
    enable_media: bool = False  # Enable media actor
    n_consumers: int = 10  # Deprecated (kept for backward compat)
    n_policymakers: int = 1  # Number of policymaker actors
    n_funders: int = 1  # Number of funder actors

    # Consumer market config
    use_case_profiles: Optional[list] = None  # e.g., ["software_dev", "healthcare", "legal"]

    # Incident reporting system
    enable_incidents: bool = False  # Enable probabilistic AI safety incidents

    # Evaluator-as-company feature
    evaluator_as_company: bool = False  # Evaluator operates as company with funding & premium services
    evaluator_base_budget: float = 0.0  # Starting budget for evaluator
    evaluator_premium_pricing: float = 100000.0  # Cost of premium access per provider per round

    # Startup entry dynamics
    startup_entry_probability: float = 0.0   # per-round probability a new provider enters
    startup_entry_cap: int = 3               # max new entrants across the whole run
    startup_min_round: int = 2               # earliest round a startup may enter (inclusive)
    startup_funder_delay: int = 1            # rounds before funders see the new provider
    startup_llm_mode: bool = False           # if True, new entrants use LLM planning

    # Capability baseline shift (applied to provider initial values and absolute thresholds)
    capability_shift: float = 0.0

    # Output
    output_dir: Optional[str] = None
    verbose: bool = True

    def to_dict(self) -> dict:
        """Convert config to dict for serialization."""
        d = asdict(self)
        # Handle benchmarks list specially since it may contain dicts
        if self.benchmarks:
            d["benchmarks"] = self.benchmarks
        return d


class EvalEcosystemSimulation:
    """
    Main simulation class for the evaluation ecosystem.

    Simulates rounds of:
    1. Providers choose strategies (R&D vs gaming allocation)
    2. Providers' true capabilities update based on R&D
    3. Evaluator scores all providers
    4. Scores are published
    5. Providers observe scores and update beliefs
    6. Consumers observe leaderboard and make subscription decisions
    7. Policymakers observe ecosystem and may issue regulations

    Key visibility design:
    - ground_truth dict holds all invisible state (true_capability, true_satisfaction, etc.)
    - Actors only access their own public_state and private_state
    - Ground truth is passed to evaluator and used for computing actual outcomes
    """

    def __init__(self, config: SimulationConfig):
        self.config = config
        self.providers: list[ModelProvider] = []
        self.consumers: list = []  # Deprecated: kept for backward compat
        self.consumer_market = None  # ConsumerMarket instance
        self.policymakers: list = []  # Will be Policymaker instances
        self.funders: list = []  # Will be Funder instances
        self.media = None  # Media instance
        self.evaluator: Optional[Evaluator] = None
        self.current_round: int = 0
        self.history: list[dict] = []

        # Ground truth held externally by simulation
        # Format: {actor_name: GroundTruth}
        self.ground_truth: dict = {}

        # Funder data for current round (used for funding multipliers)
        self._current_funder_data: dict = {}

        # Deployer liability guidance: OS providers under active guidance (carries across rounds)
        self._current_deployer_liability_guidance: set = set()

        # Startup entry tracking
        self._entrant_count: int = 0
        self._funder_eligible_round: dict = {}  # {provider_name: first_round_funders_can_allocate}
        self._rng = __import__("random").Random(config.seed)

        # Incident reporting system
        self.incident_generator = IncidentGenerator(seed=config.seed)

    def setup(
        self,
        provider_configs: list[dict],
        evaluator: Optional[Evaluator] = None,
        consumer_configs: list[dict] = None,
        policymaker_configs: list[dict] = None,
        funder_configs: list[dict] = None,
    ):
        """
        Initialize the simulation with providers and evaluator.

        Args:
            provider_configs: List of dicts with provider initialization params.
                Each dict should have: name, strategy_profile, innate_traits,
                initial_capability, initial_believed_capability (optional),
                initial_strategy (optional dict with investment allocations)
            evaluator: Optional pre-configured Evaluator. If None, creates one
                from config.
            consumer_configs: Optional list of consumer configurations
            policymaker_configs: Optional list of policymaker configurations
        """
        # Determine initial benchmark names from config (used for focus initialization)
        if evaluator is not None:
            _initial_bm_names = [bm.name for bm in evaluator.benchmarks]
        elif self.config.benchmarks:
            _initial_bm_names = [bm.get("name", f"bm_{i}") for i, bm in enumerate(self.config.benchmarks)]
        else:
            _initial_bm_names = [self.config.benchmark_name]

        # Create providers and their ground truth
        self.providers = []
        for pc in provider_configs:
            provider = ModelProvider(
                name=pc["name"],
                strategy_profile=pc["strategy_profile"],
                innate_traits=pc["innate_traits"],
                initial_capability=pc.get("initial_capability", 0.5),
                initial_believed_capability=pc.get("initial_believed_capability"),
                initial_believed_exploitability=pc.get("initial_believed_exploitability", 0.3),
                llm_mode=self.config.llm_mode,
                verbose_llm=pc.get("verbose_llm", False),
                available_benchmarks=_initial_bm_names,
                focus_benchmarks=pc.get("focus_benchmarks", []),
            )

            # Apply initial strategy if provided
            if "initial_strategy" in pc:
                strategy = pc["initial_strategy"]
                provider.private_state.fundamental_research = strategy.get("fundamental_research", 0.25)
                provider.private_state.training_optimization = strategy.get("training_optimization", 0.25)
                provider.private_state.evaluation_engineering = strategy.get("evaluation_engineering", 0.25)
                provider.private_state.safety_alignment = strategy.get("safety_alignment", 0.25)
                # Sync with legacy scratch
                provider.scratch.fundamental_research = provider.private_state.fundamental_research
                provider.scratch.training_optimization = provider.private_state.training_optimization
                provider.scratch.evaluation_engineering = provider.private_state.evaluation_engineering
                provider.scratch.safety_alignment = provider.private_state.safety_alignment

            # Apply cost efficiency for all providers (0=most expensive, 1=free/open-weights)
            # Closed providers default to 0.0 (no explicit pricing advantage)
            if "cost_advantage" in pc:
                provider.cost_advantage = pc["cost_advantage"]

            # Apply open-source provider config fields
            if pc.get("open_source", False):
                provider.is_open_source = True
                if "cost_advantage" not in pc:
                    provider.cost_advantage = 0.9  # OS default if not explicitly set
                provider.contamination_multiplier = pc.get("contamination_multiplier", 1.8)
                provider.commoditization_threshold = pc.get("commoditization_threshold", 0.65)

            self.providers.append(provider)

            # Initialize ground truth externally
            self.ground_truth[provider.name] = ProviderGroundTruth(
                true_capability=pc.get("initial_capability", 0.5)
            )

        # Create consumer market if enabled
        if self.config.enable_consumers:
            self._setup_consumer_market(provider_configs)

        # Create policymakers if enabled
        if self.config.enable_policymakers:
            self._setup_policymakers(policymaker_configs)

        # Create funders if enabled
        if self.config.enable_funders:
            self._setup_funders(funder_configs)

        # Create media if enabled
        if self.config.enable_media:
            from actors.media import Media
            self.media = Media(name="TechPress", seed=self.config.seed)

        # Create or use provided evaluator
        if evaluator is not None:
            self.evaluator = evaluator
        elif self.config.benchmarks:
            # Multi-benchmark mode
            self.evaluator = Evaluator(
                benchmarks=self.config.benchmarks,
                seed=self.config.seed,
                benchmark_sequence=self.config.benchmark_sequence,
                evaluator_as_company=self.config.evaluator_as_company,
                base_budget=self.config.evaluator_base_budget,
                premium_pricing=self.config.evaluator_premium_pricing,
            )
        else:
            # Single benchmark mode
            self.evaluator = Evaluator(
                benchmark_name=self.config.benchmark_name,
                validity=self.config.benchmark_validity,
                exploitability=self.config.benchmark_exploitability,
                noise_level=self.config.benchmark_noise,
                seed=self.config.seed,
                benchmark_sequence=self.config.benchmark_sequence,
                evaluator_as_company=self.config.evaluator_as_company,
                base_budget=self.config.evaluator_base_budget,
                premium_pricing=self.config.evaluator_premium_pricing,
            )

        # Apply benchmark evolution rates to all benchmarks
        for bm in self.evaluator.benchmarks:
            if bm.validity_decay_rate == 0.0:
                bm.validity_decay_rate = self.config.benchmark_validity_decay_rate
            if bm.exploitability_growth_rate == 0.0:
                bm.exploitability_growth_rate = self.config.benchmark_exploitability_growth_rate

        # Apply benchmark introduction config
        self.evaluator.benchmark_introduction_cooldown = self.config.benchmark_introduction_cooldown
        self.evaluator.max_benchmarks = self.config.max_benchmarks

        # Enable evaluator-as-company mode for funders if configured
        if self.config.evaluator_as_company and self.funders:
            for funder in self.funders:
                funder.set_evaluator_as_company(True)

        # Resolve consumer market benchmark weights now that evaluator exists
        if self.consumer_market:
            benchmark_names = [bm.name for bm in self.evaluator.benchmarks]
            self.consumer_market.resolve_benchmark_weights(benchmark_names)

        self.current_round = 0
        self.history = []

        if self.config.verbose:
            print("=== Simulation Setup ===")
            print(f"Providers ({len(self.providers)}): {', '.join(p.name for p in self.providers)}")
            bm_names = ", ".join(bm.name for bm in self.evaluator.benchmarks)
            print(f"Benchmarks ({len(self.evaluator.benchmarks)}): {bm_names}")
            extras = []
            if self.consumer_market:
                extras.append(f"{len(self.consumer_market.segments)} consumer segments")
            if self.policymakers:
                extras.append(f"{len(self.policymakers)} policymaker(s)")
            if self.funders:
                extras.append(f"{len(self.funders)} funder(s)")
            if self.media:
                extras.append("media enabled")
            if extras:
                print("  " + ", ".join(extras))
            print()

    def _setup_consumer_market(self, provider_configs: list[dict] = None):
        """Set up the consumer market with segments (archetype × use_case)."""
        from actors.consumer import ConsumerMarket, create_default_segments

        # Build brand recognition and provider names from provider configs
        brand_recognition = {}
        provider_names = []
        if provider_configs:
            for pc in provider_configs:
                name = pc["name"]
                provider_names.append(name)
                brand_recognition[name] = pc.get("brand_recognition", 0.5)
        else:
            provider_names = [p.name for p in self.providers]

        # Determine which use-case profiles to include
        use_cases = self.config.use_case_profiles
        if use_cases is None:
            # Default: a representative set
            use_cases = ["software_dev", "content_writer", "healthcare",
                         "finance", "researcher", "creative"]

        # Create segments
        segments = create_default_segments(
            use_cases=use_cases,
            provider_names=provider_names,
            brand_recognition=brand_recognition,
        )

        # Build consumer LLM config
        consumer_llm_config = {
            "enabled": self.config.consumer_llm_mode,
            "individuals": self.config.consumer_llm_individuals,
            "organizations": self.config.consumer_llm_organizations,
        }

        # Create market
        self.consumer_market = ConsumerMarket(
            segments=segments,
            provider_names=provider_names,
            brand_recognition=brand_recognition,
            seed=self.config.seed,
            consumer_llm_config=consumer_llm_config,
        )
        # Mark open-source providers so consumer switching friction is reduced
        self.consumer_market.open_source_providers = {
            pc["name"] for pc in (provider_configs or []) if pc.get("open_source", False)
        }
        # Note: benchmark weight resolution happens after evaluator creation
        # (in setup()) since benchmark names aren't available yet here.

    def _setup_policymakers(self, policymaker_configs: list[dict] = None):
        """Set up policymaker actors."""
        try:
            from actors.policymaker import Policymaker
        except ImportError:
            if self.config.verbose:
                print("Policymaker actor not available yet")
            return

        if policymaker_configs is None:
            # Create default policymaker
            policymaker_configs = [
                {
                    "name": "Regulator",
                    "policy_objectives": ["safety", "fairness"],
                    "intervention_threshold": 0.3,
                }
            ]

        for pc in policymaker_configs:
            # Check if using a preset philosophy
            if "philosophy" in pc and pc["philosophy"] in POLICYMAKER_PRESETS:
                preset = POLICYMAKER_PRESETS[pc["philosophy"]]
                # Merge preset with any overrides from config
                config_params = {**preset, **{k: v for k, v in pc.items() if k not in ["philosophy", "name"]}}
            else:
                # Use individual parameters from config
                config_params = pc

            # Inherit global llm_mode unless policymaker config explicitly overrides it
            if "llm_mode" not in config_params:
                config_params = {**config_params, "llm_mode": self.config.llm_mode}

            policymaker = Policymaker(
                name=pc["name"],
                policy_objectives=config_params.get("policy_objectives", ["safety"]),
                intervention_threshold=config_params.get("intervention_threshold", 0.3),
                risk_tolerance=config_params.get("risk_tolerance", 0.5),
                llm_mode=config_params.get("llm_mode", False),
                intervention_cooldown=config_params.get("intervention_cooldown", 3),
                sanction_fine_multiplier=config_params.get("sanction_fine_multiplier", 0.30),
                sanction_incident_threshold=config_params.get("sanction_incident_threshold", 2),
                sanction_duration=config_params.get("sanction_duration", 3),
                mandate_risk_threshold=config_params.get("mandate_risk_threshold", 0.60),
                sanction_min_severity=config_params.get("sanction_min_severity", "major"),
                capability_shift=self.config.capability_shift,
            )
            self.policymakers.append(policymaker)

            # Initialize policymaker ground truth
            self.ground_truth[policymaker.name] = PolicymakerGroundTruth(
                true_risk_tolerance=pc.get("risk_tolerance", 0.5),
                true_intervention_effectiveness=pc.get("intervention_effectiveness", 0.5),
            )

    def _setup_funders(self, funder_configs: list[dict] = None):
        """Set up funder actors."""
        try:
            from actors.funder import Funder, get_default_funder_configs
        except ImportError:
            if self.config.verbose:
                print("Funder actor not available yet")
            return

        if funder_configs is None:
            # Use default funder configs
            funder_configs = get_default_funder_configs()[:self.config.n_funders]

        for fc in funder_configs:
            funder = Funder(
                name=fc["name"],
                funder_type=fc.get("funder_type", "vc"),
                total_capital=fc.get("total_capital", 1000000.0),
                risk_tolerance=fc.get("risk_tolerance", 0.5),
                mission_statement=fc.get("mission_statement", ""),
                llm_mode=self.config.llm_mode,
                max_round_deployment=fc.get("max_round_deployment", 0.10),
                funding_cooldown=fc.get("funding_cooldown", 2),
            )
            self.funders.append(funder)

            # Initialize funder ground truth
            self.ground_truth[funder.name] = FunderGroundTruth(
                true_roi=0.0,
                funding_efficiency=fc.get("funding_efficiency", 1.0),
            )

    def _update_ground_truth(self, provider_name: str, capability_gain: float):
        """
        Update ground truth for a provider after R&D execution.

        Args:
            provider_name: Name of the provider
            capability_gain: How much true capability increased
        """
        if provider_name in self.ground_truth:
            gt = self.ground_truth[provider_name]
            if isinstance(gt, ProviderGroundTruth):
                gt.true_capability += capability_gain

    def _sync_provider_ground_truth(self, provider: ModelProvider):
        """
        Sync provider's internal state with external ground truth.

        For backwards compatibility, we keep provider.scratch.true_capability
        in sync with external ground truth.
        """
        if provider.name in self.ground_truth:
            gt = self.ground_truth[provider.name]
            if isinstance(gt, ProviderGroundTruth):
                provider.scratch.true_capability = gt.true_capability

    def _get_provider_ecosystem_context(self, provider_name: str) -> dict:
        """Collect ecosystem signals visible to a specific provider.

        Providers see:
        - Their OWN customer satisfaction (not competitors')
        - Their OWN market share
        - Public regulatory interventions (visible to all)
        - Their OWN recent incidents (public record)
        """
        context = {}
        if self.history:
            last = self.history[-1]
            if "consumer_data" in last:
                cd = last["consumer_data"]
                # Provider sees only their own customer satisfaction
                provider_sat = cd.get("provider_satisfaction", {}).get(provider_name)
                if provider_sat is not None:
                    context["consumer_satisfaction"] = provider_sat
                # Provider sees their own market share
                provider_share = cd.get("market_shares", {}).get(provider_name)
                if provider_share is not None:
                    context["own_market_share"] = provider_share
            if "policymaker_data" in last:
                context["regulatory_pressure"] = last["policymaker_data"].get("interventions", [])
            # Provider sees their own incidents from last round (public record)
            if "incidents" in last:
                own_incidents = [
                    inc for inc in last["incidents"]
                    if inc.get("provider") == provider_name
                ]
                if own_incidents:
                    context["own_incidents"] = own_incidents
        # Always include available benchmark names and per-benchmark scores from last round
        context["available_benchmarks"] = [bm.name for bm in self.evaluator.benchmarks]
        if self.history:
            last_round_num = self.history[-1].get("round", self.current_round - 1)
            context["per_benchmark_scores"] = self.evaluator.get_per_benchmark_scores(last_round_num)
        return context

    def run_round(self) -> dict:
        """
        Run a single simulation round.

        Updated flow:
        1. Providers plan and execute (R&D updates capability with funding multiplier)
        2. Evaluator scores all providers using ground truth
        3. Scores are published
        4. Providers observe and reflect
        5. Consumers observe leaderboard and decide subscriptions
        6. Policymakers observe and may intervene
        7. Funders observe and allocate funding
        8. Record round data

        Returns:
            Dict with round results
        """
        round_num = self.current_round

        # Possibly spawn a new startup provider this round
        new_entrant_info = self._maybe_spawn_startup(round_num)

        # Open-source provider names (used for exemptions throughout the round)
        os_provider_names = {p.name for p in self.providers if p.is_open_source}

        # Get funding multipliers from previous round's funder decisions
        funding_multipliers = self._current_funder_data.get("funding_multipliers", {})

        # 1. Providers plan investment portfolios (for round > 0, they've seen previous scores)
        if round_num > 0:
            for provider in self.providers:
                ecosystem_context = self._get_provider_ecosystem_context(provider.name)
                portfolio = provider.plan(ecosystem_context)

                # Calculate capability gain with S-curve dynamics
                base_efficiency = self.config.rnd_efficiency

                # Apply funding multiplier (1.0 if no funding, up to 2.0 with max funding)
                funding_multiplier = funding_multipliers.get(provider.name, 1.0)

                # Apply active sanctions from previous round (same timing as funder multipliers)
                # Open-source providers are exempt from policymaker sanctions (EU AI Act exemption)
                prev_pm_data = self.history[-1].get("policymaker_data", {}) if self.history else {}
                active_sanctions = prev_pm_data.get("active_sanctions", {})
                if provider.name in active_sanctions and not provider.is_open_source:
                    fine_amount = active_sanctions[provider.name].get("fine_amount", 0.0)
                    funding_multiplier = max(0.1, funding_multiplier * (1.0 - fine_amount))

                effective_efficiency = base_efficiency * funding_multiplier

                # S-curve: diminishing returns near the capability ceiling
                current_capability = self.ground_truth[provider.name].true_capability
                headroom = max(0, self.config.capability_ceiling - current_capability)
                diminishing_factor = headroom ** (1.0 / self.config.diminishing_returns_rate)

                raw_gain = (
                    portfolio["fundamental_research"] * effective_efficiency * 1.5 +
                    portfolio["training_optimization"] * effective_efficiency * 1.0 +
                    portfolio["evaluation_engineering"] * effective_efficiency * 0.1
                    # Safety alignment doesn't directly improve capability
                )
                capability_gain = raw_gain * diminishing_factor

                # Breakthrough chance (proportional to fundamental_research investment)
                if self.evaluator.rng.random() < self.config.breakthrough_probability * portfolio["fundamental_research"]:
                    capability_gain += self.config.breakthrough_magnitude * headroom

                # Update external ground truth
                self._update_ground_truth(provider.name, capability_gain)

                # Sync for backwards compatibility
                self._sync_provider_ground_truth(provider)

                # Record execution in provider memory
                provider.memory.append({
                    "type": "execution",
                    "round": round_num,
                    "capability_gain": capability_gain,
                    "funding_multiplier": funding_multiplier,
                    "new_true_capability": self.ground_truth[provider.name].true_capability,
                    "portfolio": portfolio,
                })

        # Phase D: Open-source ecosystem_influence tracking + commoditization shock
        for provider in self.providers:
            if not provider.is_open_source:
                continue
            true_cap = self.ground_truth[provider.name].true_capability
            # Logistic growth: ecosystem_influence grows based on cost efficiency x capability
            growth = provider.cost_advantage * true_cap * 5.0 * (1.0 - provider.ecosystem_influence / 100.0)
            provider.ecosystem_influence = min(100.0, provider.ecosystem_influence + growth)

            # Persistent commoditization pressure: cost_advantage bonus grows after threshold
            if provider._commoditization_shock_fired:
                provider.cost_advantage = min(0.95, provider.cost_advantage + 0.02)

            # One-time commoditization shock when capability crosses threshold
            if (not provider._commoditization_shock_fired
                    and true_cap >= provider.commoditization_threshold
                    and self.consumer_market):
                provider._commoditization_shock_fired = True
                # Compress the top closed provider's share
                closed_providers = [p for p in self.providers if not p.is_open_source]
                if closed_providers and self.history and "consumer_data" in self.history[-1]:
                    prev_shares = self.history[-1]["consumer_data"].get("market_shares", {})
                    if prev_shares:
                        top_closed = max(closed_providers, key=lambda p: prev_shares.get(p.name, 0.0))
                        compress_amount = min(0.08, provider.ecosystem_influence / 200.0)
                        # Apply compression across all segments
                        for seg in self.consumer_market.segments:
                            top_share = seg.provider_shares.get(top_closed.name, 0.0)
                            actual_compress = compress_amount * top_share
                            if actual_compress > 0.001 and top_share > actual_compress:
                                seg.provider_shares[top_closed.name] -= actual_compress
                                seg.provider_shares[provider.name] = (
                                    seg.provider_shares.get(provider.name, 0.0) + actual_compress
                                )
                        if self.config.verbose:
                            print(f"  [Commoditization Shock] {provider.name} crossed capability "
                                  f"threshold {provider.commoditization_threshold:.2f} "
                                  f"(true_cap={true_cap:.3f}). "
                                  f"Compressing {top_closed.name} share by ~{compress_amount:.1%}")

        # 2. Evaluator scores all providers using ground truth
        scores = self.evaluator.evaluate_all(
            self.providers,
            round_num,
            ground_truth=self.ground_truth,
        )

        # 2b. Update benchmarks based on gaming pressure (Goodhart's Law feedback loop)
        avg_eval_engineering = sum(
            p.evaluation_engineering for p in self.providers
        ) / len(self.providers) if self.providers else 0.0

        # Compute open-source contamination bonus (weight publishing accelerates benchmark gaming)
        os_providers = [p for p in self.providers if p.is_open_source]
        os_contamination_bonus = 0.0
        for p in os_providers:
            os_contamination_bonus += p.contamination_multiplier * (p.ecosystem_influence / 100.0)
        os_contamination_bonus = min(0.3, os_contamination_bonus)

        self.evaluator.update_benchmark(avg_eval_engineering, os_contamination_bonus)

        # 2c. Detect benchmark saturation
        newly_saturated = self.evaluator.detect_saturation(round_num)
        if newly_saturated and self.config.verbose:
            for bm_name in newly_saturated:
                state = self.evaluator._benchmark_saturation_state[bm_name]
                print(f"  [Saturation] {bm_name} saturated at score {state['max_score']:.4f}")

        # 2d. Apply weight decay to saturated benchmarks
        weight_decay_multipliers = self.evaluator.apply_saturation_weight_decay(round_num)
        # Check for any benchmarks with significantly reduced weight
        if self.config.verbose:
            for bm_name, decay in weight_decay_multipliers.items():
                if decay < 0.9:  # Only print if weight is noticeably reduced
                    state = self.evaluator._benchmark_saturation_state.get(bm_name, {})
                    if state.get("saturated"):
                        print(f"  [Weight Decay] {bm_name} weight reduced to {decay:.2f}x")

        # 2e. Consider introducing a new benchmark
        new_benchmark = self.evaluator.consider_new_benchmark(round_num)

        # Re-resolve consumer benchmark weights if a new benchmark was introduced
        if new_benchmark is not None and self.consumer_market:
            benchmark_names = [bm.name for bm in self.evaluator.benchmarks]
            self.consumer_market.resolve_benchmark_weights(benchmark_names)

        # 3. Publish scores
        published_scores = self.evaluator.publish_scores(scores)
        leaderboard = self.evaluator.get_leaderboard(scores)

        # 4. Providers observe scores and reflect
        for provider in self.providers:
            own_score = published_scores[provider.name]
            competitor_scores = {
                name: score
                for name, score in published_scores.items()
                if name != provider.name
            }
            provider.observe(own_score, competitor_scores, round_num)
            provider.reflect()

        # 4b. Generate incidents based on provider strategies and safety investment
        incidents = []
        if round_num > 0 and self.config.enable_incidents:
            # Collect current strategies
            provider_strategies = {
                p.name: {
                    "fundamental_research": p.fundamental_research,
                    "training_optimization": p.training_optimization,
                    "evaluation_engineering": p.evaluation_engineering,
                    "safety_alignment": p.safety_alignment,
                }
                for p in self.providers
            }

            # Mandatory safety floor: policymaker interventions at compliance_audit level
            # or above enforce a minimum safety_alignment of 0.15.
            # Models EU AI Act Art. 9 — ongoing risk management cannot be zeroed out.
            # Applied here (before incident generation) so the floor affects incident prob
            # in the same round the compliance state is active.
            prev_pm_data = self.history[-1].get("policymaker_data", {}) if self.history else {}
            active_regulations = prev_pm_data.get("active_regulations", [])
            FLOOR_TRIGGERS = {"compliance_audit", "sanctions_and_fines", "emergency_investigation"}
            floor_applies_to = set()
            for reg in active_regulations:
                if isinstance(reg, dict) and reg.get("type") in FLOOR_TRIGGERS:
                    target = reg.get("target")
                    if target:
                        floor_applies_to.add(target)
            SAFETY_FLOOR = 0.15
            for p_name, strat in provider_strategies.items():
                if p_name in floor_applies_to:
                    if strat["safety_alignment"] < SAFETY_FLOOR:
                        strat["safety_alignment"] = SAFETY_FLOOR

            # Collect ground truth capabilities
            ground_truth_capabilities = {
                p.name: self.ground_truth[p.name].true_capability
                for p in self.providers
            }

            # Get market shares from previous round
            market_shares = {}
            if self.history and "consumer_data" in self.history[-1]:
                market_shares = self.history[-1]["consumer_data"].get("market_shares", {})

            # Collect active sanctions and investigated providers from previous round
            active_sanctions = prev_pm_data.get("active_sanctions", {})
            investigated_providers = {
                iv.get("target")
                for iv in prev_pm_data.get("interventions", [])
                if iv.get("type") == "emergency_investigation" and iv.get("target")
            }

            # Generate incidents
            incidents = self.incident_generator.generate_incidents(
                providers=self.providers,
                round_num=round_num,
                ground_truth=ground_truth_capabilities,
                published_scores=published_scores,
                market_shares=market_shares,
                provider_strategies=provider_strategies,
                active_sanctions=active_sanctions,
                investigated_providers=investigated_providers,
            )

            # Log incidents if verbose
            if incidents and self.config.verbose:
                for inc in incidents:
                    if inc.severity != "minor":  # Only print moderate+ incidents
                        print(f"  [Incident] {inc.severity.upper()}: {inc.description}")

        # 5. Media observes and publishes (if enabled)
        media_coverage = None
        if self.media:
            prev_funder_data = self.history[-1].get("funder_data", {}) if self.history else {}
            prev_consumer_data = self.history[-1].get("consumer_data", {}) if self.history else {}
            per_bm_scores = self.evaluator.get_per_benchmark_scores(round_num)

            media_coverage = self.media.observe_and_publish(
                leaderboard=leaderboard,
                benchmark_params={
                    bm.name: {"validity": bm.validity, "exploitability": bm.exploitability}
                    for bm in self.evaluator.benchmarks
                },
                policymaker_data=self.history[-1].get("policymaker_data", {}) if self.history else {},
                new_benchmark={"name": new_benchmark.name} if new_benchmark else None,
                round_num=round_num,
                funder_data=prev_funder_data,
                per_benchmark_scores=per_bm_scores,
                consumer_data=prev_consumer_data,
                evaluator=self.evaluator,
                incidents=incidents,  # NEW: Pass incidents to media
            )

        # 6. Consumer actions (if enabled)
        consumer_data = {}
        if self.consumer_market:
            consumer_data = self._run_consumer_round(
                leaderboard, round_num, media_coverage, incidents=incidents,
                deployer_liability_guidance=self._current_deployer_liability_guidance,
            )

        # 7. Policymaker actions (if enabled)
        policymaker_data = {}
        if self.policymakers:
            policymaker_data = self._run_policymaker_round(
                leaderboard, consumer_data, round_num, media_coverage, incidents=incidents,
                open_source_providers=os_provider_names,
            )

        # 8. Funder actions (if enabled)
        funder_data = {}
        if self.funders:
            funder_data = self._run_funder_round(
                leaderboard, consumer_data, policymaker_data, round_num,
                media_coverage, incidents=incidents,
                open_source_providers=os_provider_names,
            )
            # Store for next round's capability gain calculation
            self._current_funder_data = funder_data

        # Collect deployer liability guidance from all policymakers (carries forward each round)
        for pm in self.policymakers:
            self._current_deployer_liability_guidance |= pm._active_liability_guidance

        # 8b. Evaluator funding collection (if evaluator-as-company mode enabled)
        evaluator_funding_data = {}
        if self.config.evaluator_as_company and round_num > 0:
            evaluator_funding_data = self._run_evaluator_funding_round(round_num, funder_data)

        # Record round data
        round_data = {
            "round": round_num,
            "scores": dict(scores),  # Composite scores
            "true_capabilities": {
                p.name: self.ground_truth[p.name].true_capability
                for p in self.providers
            },
            "believed_capabilities": {
                p.name: p.private_state.believed_own_capability
                for p in self.providers
            },
            "strategies": {
                p.name: {
                    "fundamental_research": p.fundamental_research,
                    "training_optimization": p.training_optimization,
                    "evaluation_engineering": p.evaluation_engineering,
                    "safety_alignment": p.safety_alignment,
                }
                for p in self.providers
            },
            "open_source_data": {
                p.name: {
                    "ecosystem_influence": p.ecosystem_influence,
                    "cost_advantage": p.cost_advantage,
                    "commoditization_shock_fired": p._commoditization_shock_fired,
                }
                for p in self.providers
                if p.is_open_source
            } or None,
            "benchmark_params": {
                bm.name: {"validity": bm.validity, "exploitability": bm.exploitability}
                for bm in self.evaluator.benchmarks
            },
        }

        # Add per-benchmark scores if multiple benchmarks
        if len(self.evaluator.benchmarks) > 1:
            round_data["per_benchmark_scores"] = self.evaluator.get_per_benchmark_scores(round_num)

        # Record new benchmark introduction if one occurred
        if new_benchmark is not None:
            round_data["new_benchmark"] = {
                "name": new_benchmark.name,
                "validity": new_benchmark.validity,
                "exploitability": new_benchmark.exploitability,
                "trigger": self.evaluator.introduction_history[-1]["trigger"],
            }

        # Record benchmark saturation events
        if newly_saturated:
            round_data["saturated_benchmarks"] = [
                {
                    "name": bm_name,
                    "max_score": self.evaluator._benchmark_saturation_state[bm_name]["max_score"],
                }
                for bm_name in newly_saturated
            ]

        # Record benchmark weight decay (for saturated benchmarks)
        saturated_benchmarks_data = []
        for bm_name, decay in weight_decay_multipliers.items():
            if decay < 1.0:
                saturated_benchmarks_data.append({
                    "name": bm_name,
                    "weight_decay": decay,
                    "saturation_info": self.evaluator._benchmark_saturation_state.get(bm_name, {})
                })
        if saturated_benchmarks_data:
            round_data["saturated_benchmarks"] = saturated_benchmarks_data

        # Add new entrant info if a startup spawned this round
        if new_entrant_info:
            round_data["new_entrant"] = new_entrant_info

        # Add media data if present
        if media_coverage:
            round_data["media_data"] = media_coverage

        # Add consumer data if present
        if consumer_data:
            round_data["consumer_data"] = consumer_data

        # Add policymaker data if present
        if policymaker_data:
            round_data["policymaker_data"] = policymaker_data

        # Add funder data if present
        if funder_data:
            round_data["funder_data"] = funder_data

        # Add evaluator funding data if present
        if evaluator_funding_data:
            round_data["evaluator_funding_data"] = evaluator_funding_data
            # Add business metrics summary
            if self.evaluator.private_state:
                round_data["evaluator_business_metrics"] = {
                    "budget": self.evaluator.private_state.budget,
                    "premium_providers": list(self.evaluator.private_state.premium_providers),
                    "n_premium_providers": len(self.evaluator.private_state.premium_providers),
                    "base_funding": self.evaluator.private_state.base_funding,
                    "service_revenue": self.evaluator.private_state.service_revenue,
                    "trial_counts": {
                        p.name: self.evaluator.compute_n_trials(p.name, p.evaluation_engineering)
                        for p in self.providers
                    },
                }

        # Add incidents if any occurred
        if incidents:
            round_data["incidents"] = [inc.to_dict() for inc in incidents]
            # Add summary statistics
            round_data["incident_summary"] = {
                "total_count": len(incidents),
                "by_severity": {
                    sev: len([inc for inc in incidents if inc.severity == sev])
                    for sev in ["minor", "moderate", "major", "critical"]
                },
                "by_provider": {
                    p.name: len([inc for inc in incidents if inc.provider == p.name])
                    for p in self.providers
                },
            }

        # Capture reasoning traces from all actor types (for post-hoc analysis
        # and game log).  In LLM mode, actors store "reasoning"; in heuristic
        # mode they store "reason".  We grab whichever is present.
        actor_traces = {}

        for provider in self.providers:
            for entry in reversed(provider.memory):
                if entry.get("type") == "planning":
                    trace = entry.get("reasoning") or entry.get("reason")
                    if trace:
                        actor_traces[provider.name] = trace
                    break

        for policymaker in self.policymakers:
            for entry in reversed(policymaker.memory):
                if entry.get("type") == "planning":
                    decision = entry.get("decision", "")
                    # Prefer full LLM reasoning string; fall back to short reason
                    reason = entry.get("reasoning") or entry.get("reason", "")
                    intervention = entry.get("intervention")
                    if intervention:
                        reason = entry.get("reasoning") or intervention.get("reason", reason)
                        decision = intervention.get("type", decision)
                    trace = f"{decision}: {reason}" if reason else decision
                    if trace:
                        actor_traces[policymaker.name] = trace
                    break

        for funder in self.funders:
            for entry in reversed(funder.memory):
                if entry.get("type") in ("planning", "planning_llm"):
                    trace = entry.get("reasoning") or entry.get("reason")
                    if trace:
                        actor_traces[funder.name] = trace
                    break

        # Organizational consumer LLM reasoning traces (when switches happen)
        if self.consumer_market:
            for seg in self.consumer_market.segments:
                if seg.consumer_type == "organization" and seg.last_llm_decision:
                    # Only include if there was a switch decision
                    decision = seg.last_llm_decision.get("decision", {})
                    if decision.get("should_switch"):
                        reasoning = decision.get("reasoning", "")
                        target = decision.get("target_provider", "unknown")
                        provider = seg.last_llm_decision.get("provider", "current")
                        trace = f"switch_{provider}_to_{target}: {reasoning}"
                        actor_traces[seg.name] = trace

        if actor_traces:
            round_data["actor_traces"] = actor_traces

        # Log active deployer liability guidance
        if self._current_deployer_liability_guidance:
            round_data["deployer_liability_guidance"] = sorted(self._current_deployer_liability_guidance)

        # Compute barrier-to-entry index
        round_data["barrier_to_entry"] = self._compute_barrier_to_entry(round_data)
        # Log base entry probability so plotting can compute effective_prob per round
        if self.config.startup_entry_probability > 0:
            round_data["startup_entry_probability"] = self.config.startup_entry_probability

        # Apply numeric precision (4 decimal places) to stored data
        round_data = r4(round_data)

        self.history.append(round_data)

        if self.config.verbose:
            self._print_round_summary(round_data)

        self.current_round += 1
        return round_data

    def _run_consumer_round(self, leaderboard: list, round_num: int,
                            media_coverage: Optional[dict] = None,
                            policymaker_data: Optional[dict] = None,
                            incidents: Optional[list] = None,
                            deployer_liability_guidance: Optional[set] = None) -> dict:
        """
        Run consumer market actions for the round.

        Uses ConsumerMarket to handle segment-level observation, satisfaction,
        and switching as proportions rather than individual consumer decisions.

        Args:
            leaderboard: Current leaderboard [(name, score), ...]
            round_num: Current round number
            media_coverage: Optional media coverage dict from Media actor
            incidents: Optional list of AIIncident objects from this round

        Returns:
            Dict with consumer data for this round
        """
        if not self.consumer_market:
            return {}

        # Observe: update beliefs from leaderboard (use per-benchmark if available)
        per_bm_scores = self.evaluator.get_per_benchmark_scores(round_num)
        if per_bm_scores:
            self.consumer_market.observe_per_benchmark(
                leaderboard, per_bm_scores, media_coverage, round_num
            )
        else:
            self.consumer_market.observe(leaderboard, media_coverage, round_num)

        # Compute satisfaction from ground truth and ecosystem factors
        provider_strategies = {
            p.name: {
                "fundamental_research": p.fundamental_research,
                "training_optimization": p.training_optimization,
                "evaluation_engineering": p.evaluation_engineering,
                "safety_alignment": p.safety_alignment,
            }
            for p in self.providers
        }
        published_scores = dict(leaderboard)  # Convert to dict

        # Convert incidents to history format for consumer satisfaction computation
        incident_history = {}
        if incidents:
            for inc in incidents:
                if inc.provider not in incident_history:
                    incident_history[inc.provider] = []
                incident_history[inc.provider].append(inc)

        # Include historical incidents from incident_generator
        all_incident_history = self.incident_generator.get_incident_history()

        # Build cost efficiency dict for all providers that have a non-zero value
        provider_cost_advantage = {
            p.name: p.cost_advantage
            for p in self.providers
            if p.cost_advantage > 0.0
        }

        self.consumer_market.compute_satisfaction(
            self.ground_truth,
            provider_strategies=provider_strategies,
            published_scores=published_scores,
            media_coverage=media_coverage,
            incident_history=all_incident_history,
            round_num=round_num,
            provider_cost_advantage=provider_cost_advantage if provider_cost_advantage else None,
        )

        # Compute switching (pass context for LLM mode)
        switching_rate = self.consumer_market.compute_switching(
            ground_truth=self.ground_truth,
            provider_strategies=provider_strategies,
            published_scores=published_scores,
            media_coverage=media_coverage,
            policymaker_data=policymaker_data,
            incident_history=all_incident_history,
            per_benchmark_scores=per_bm_scores,
            provider_cost_advantage=provider_cost_advantage if provider_cost_advantage else None,
            deployer_liability_guidance=deployer_liability_guidance,
        )

        # Get consumer data
        consumer_data = self.consumer_market.get_consumer_data()
        consumer_data["switching_rate"] = switching_rate

        return consumer_data

    def _run_policymaker_round(
        self,
        leaderboard: list,
        consumer_data: dict,
        round_num: int,
        media_coverage: Optional[dict] = None,
        incidents: Optional[list] = None,
        open_source_providers: Optional[set] = None,
    ) -> dict:
        """
        Run policymaker actions for the round.

        Args:
            leaderboard: Current leaderboard
            consumer_data: Consumer data from this round
            round_num: Current round number
            media_coverage: Optional media coverage dict
            incidents: Optional list of AIIncident objects from this round

        Returns:
            Dict with policymaker data for this round
        """
        try:
            from actors.policymaker import Policymaker
        except ImportError:
            return {}

        policymaker_data = {
            "interventions": [],
            "active_regulations": [],
        }

        for policymaker in self.policymakers:
            if not isinstance(policymaker, Policymaker):
                continue

            # Build provider strategies dict for policymaker observation
            provider_strategies = {
                p.name: {
                    "fundamental_research": p.fundamental_research,
                    "training_optimization": p.training_optimization,
                    "evaluation_engineering": p.evaluation_engineering,
                    "safety_alignment": p.safety_alignment,
                }
                for p in self.providers
            }

            # Policymaker observes ecosystem state
            policymaker.observe(
                leaderboard=leaderboard,
                consumer_satisfaction=consumer_data.get("avg_satisfaction"),
                validity_correlation=self.evaluator.compute_validity_correlation(),
                round_num=round_num,
                media_coverage=media_coverage,
                market_shares=consumer_data.get("market_shares"),
                provider_strategies=provider_strategies,
                incidents=incidents,
                open_source_providers=open_source_providers,
            )

            # Policymaker reflects on observations
            policymaker.reflect()

            # Policymaker plans intervention
            intervention = policymaker.plan()

            # Policymaker executes intervention
            if intervention:
                policymaker.execute(intervention)
                intervention_type = intervention.get("type")

                if intervention_type == "mandate_benchmark":
                    regulation = Regulation(
                        name=intervention.get("name", f"Regulation_{round_num}"),
                        regulation_type="mandate_benchmark",
                        details=intervention.get("details", {}),
                        issued_round=round_num,
                        active=True,
                    )
                    self.evaluator.add_regulation(regulation)

                elif intervention_type == "public_warning":
                    # Reduce consumer leaderboard_trust temporarily
                    if self.consumer_market:
                        for seg in self.consumer_market.segments:
                            seg.leaderboard_trust *= 0.9

                elif intervention_type == "investigation":
                    # Increases observation sensitivity - risk beliefs update faster next round
                    # (recorded in policymaker's past_interventions for escalation tracking)
                    pass

                elif intervention_type == "compliance_audit":
                    # Stronger benchmark adjustment - reduce exploitability further
                    reduction = intervention.get("details", {}).get("exploitability_reduction", 0.1)
                    for bm in self.evaluator.benchmarks:
                        bm.exploitability = max(0.1, bm.exploitability - reduction)

                # TIER 1 ENHANCEMENTS: New intervention types

                elif intervention_type == "threshold_announcement":
                    # Public announcement - no direct effect, but providers observe thresholds
                    # Thresholds are stored in policymaker.announced_thresholds (public)
                    # Creates strategic uncertainty and potential for proactive behavior change
                    pass

                elif intervention_type == "information_request":
                    # Lighter burden than investigation - opportunity cost to provider
                    target_provider_name = intervention.get("details", {}).get("provider")
                    opportunity_cost = intervention.get("details", {}).get("opportunity_cost", 0.05)

                    # Apply opportunity cost to provider's effective R&D capacity
                    # (simulates time/resources spent on disclosure compliance)
                    for provider in self.providers:
                        if provider.name == target_provider_name:
                            # Note: This is applied for the next round's capability update
                            # We could store a penalty to apply in the next provider planning phase
                            # For now, we'll just record it (providers could see this in their context)
                            pass

                elif intervention_type == "market_concentration_review":
                    # Antitrust review - effects:
                    # 1. Investigation tax (opportunity cost)
                    # 2. Reduced funding multiplier (affects funder allocations next round)
                    target_provider_name = intervention.get("details", {}).get("provider")
                    investigation_tax = intervention.get("details", {}).get("investigation_tax", 0.1)
                    funding_reduction = intervention.get("details", {}).get("funding_multiplier_reduction", 0.2)

                    # Store the intervention details for funders to see
                    # Funders will reduce funding multiplier for this provider
                    # (This is applied in the next funder round via policymaker_data)
                    pass

                elif intervention_type == "sanctions_and_fines":
                    # Mechanical effect applied via _active_sanctions in next round's capability update
                    pass

                policymaker_data["interventions"].append({
                    "policymaker": policymaker.name,
                    "type": intervention_type,
                    "details": intervention.get("details"),
                })

        # Collect active sanctions from all policymakers
        # Open-source providers are exempt from policymaker sanctions (EU AI Act exemption)
        all_active_sanctions = {}
        for pm in self.policymakers:
            for provider_name, sanction in pm._active_sanctions.items():
                if provider_name not in (open_source_providers or set()):
                    all_active_sanctions[provider_name] = sanction
        policymaker_data["active_sanctions"] = all_active_sanctions

        # Record active regulations
        policymaker_data["active_regulations"] = [
            r.get_summary() for r in self.evaluator.get_active_regulations()
        ]

        return policymaker_data

    def _run_funder_round(
        self,
        leaderboard: list,
        consumer_data: dict,
        policymaker_data: dict,
        round_num: int,
        media_coverage: Optional[dict] = None,
        incidents: Optional[list] = None,
        open_source_providers: Optional[set] = None,
    ) -> dict:
        """
        Run funder actions for the round.

        Args:
            leaderboard: Current leaderboard
            consumer_data: Consumer data from this round
            policymaker_data: Policymaker data from this round
            round_num: Current round number
            media_coverage: Optional media coverage dict
            incidents: Optional list of AIIncident objects from this round

        Returns:
            Dict with funder data for this round
        """
        try:
            from actors.funder import Funder
        except ImportError:
            return {}

        funder_data = {
            "allocations": {},
            "funding_multipliers": {},
            "total_funding": 0.0,
        }

        all_allocations = {}

        # Collect other funders' current allocations for diversification awareness
        other_funder_allocations = {}
        for funder in self.funders:
            if not isinstance(funder, Funder):
                continue
            other_funder_allocations[funder.name] = dict(funder.private_state.active_funding)

        for funder in self.funders:
            if not isinstance(funder, Funder):
                continue

            # Prepare other funders' allocations (excluding self)
            others = {k: v for k, v in other_funder_allocations.items() if k != funder.name}

            # Filter leaderboard to only providers eligible for funding this round
            # (new entrants have a 1-round delay before funders can see/allocate to them)
            eligible_leaderboard = [
                (name, score) for name, score in leaderboard
                if self._funder_eligible_round.get(name, 0) <= round_num
            ]

            # Funder observes ecosystem state (public signals only)
            funder.observe(
                leaderboard=eligible_leaderboard,
                consumer_data=consumer_data,
                policymaker_data=policymaker_data,
                round_num=round_num,
                media_coverage=media_coverage,
                other_funder_allocations=others,
                incidents=incidents,
                open_source_providers=open_source_providers,
            )

            # Funder reflects on observations
            funder.reflect()

            # Funder plans funding allocations
            allocations = funder.plan()

            # Funder executes allocations
            funder.execute(allocations)

            # Record allocations
            funder_data["allocations"][funder.name] = allocations

            # Aggregate allocations per provider across all funders
            for provider_name, amount in allocations.items():
                if provider_name not in all_allocations:
                    all_allocations[provider_name] = 0.0
                all_allocations[provider_name] += amount

        # Calculate funding multipliers per provider
        # Normalized to actual round deployment pool (not total capital)
        total_deployed = sum(all_allocations.values())
        if total_deployed > 0:
            for provider_name, funding in all_allocations.items():
                proportion = funding / total_deployed
                # Multiplier: 1.0 (no funding) to 2.0 (all funding)
                multiplier = 1.0 + min(1.0, proportion)
                funder_data["funding_multipliers"][provider_name] = multiplier

        funder_data["total_funding"] = sum(all_allocations.values())

        return funder_data

    def _run_evaluator_funding_round(
        self,
        round_num: int,
        funder_data: dict,
    ) -> dict:
        """
        Collect evaluator funding from funders and providers.

        Args:
            round_num: Current round number
            funder_data: Funder data from this round with allocations

        Returns:
            Dict with evaluator funding details
        """
        if not self.config.evaluator_as_company:
            return {}

        # Collect funder allocations to evaluator
        funder_allocations = {}
        for funder_name, allocations in funder_data.get("allocations", {}).items():
            if "__EVALUATOR__" in allocations:
                funder_allocations[funder_name] = allocations["__EVALUATOR__"]

        # Compute per-provider funder allocation for this round (their available budget)
        provider_budgets = {}
        for funder_name, alloc in funder_data.get("allocations", {}).items():
            for pname, amount in alloc.items():
                if pname != "__EVALUATOR__":
                    provider_budgets[pname] = provider_budgets.get(pname, 0.0) + amount

        # Collect premium payments from providers
        provider_payments = {}
        for provider in self.providers:
            # Open-source providers have no subscription revenue and do not pay for premium access
            if provider.is_open_source:
                provider.private_state.evaluator_premium_access = False
                provider.private_state.evaluator_funding_level = 0.0
                continue

            ecosystem_context = self._get_provider_ecosystem_context(provider.name)
            decision = provider.decide_premium_access(
                premium_pricing=self.config.evaluator_premium_pricing,
                current_budget=provider_budgets.get(provider.name, 0.0),
                ecosystem_context=ecosystem_context,
            )

            if decision["purchase_premium"]:
                provider_payments[provider.name] = decision["amount"]
                provider.private_state.evaluator_premium_access = True
                provider.private_state.evaluator_funding_level = decision["amount"]
            else:
                provider.private_state.evaluator_premium_access = False
                provider.private_state.evaluator_funding_level = 0.0

        # Evaluator collects funding
        funding_details = self.evaluator.collect_funding(
            funder_allocations=funder_allocations,
            provider_premium_payments=provider_payments,
            round_num=round_num,
        )

        return {
            "funder_allocations": funder_allocations,
            "provider_payments": provider_payments,
            "funding_details": funding_details,
        }

    def run(self, n_rounds: Optional[int] = None) -> list[dict]:
        """
        Run the full simulation.

        Args:
            n_rounds: Number of rounds to run. If None, uses config.n_rounds.

        Returns:
            List of round data dicts
        """
        if n_rounds is None:
            n_rounds = self.config.n_rounds

        if self.config.verbose:
            print(f"=== Running {n_rounds} rounds ===\n")

        for _ in range(n_rounds):
            self.run_round()

        if self.config.verbose:
            self._print_final_summary()

        return self.history

    def _maybe_spawn_startup(self, round_num: int) -> Optional[dict]:
        """Probabilistically spawn a new startup provider this round.

        Entry probability is modulated by last round's BTE composite: a higher
        barrier discourages entry. If no BTE history exists (round 0), the base
        probability is used directly.

        effective_prob = startup_entry_probability * (1 - bte_composite)

        Returns a dict describing the new entrant (for round_data logging), or None.
        """
        if self.config.startup_entry_probability <= 0:
            return None
        if self._entrant_count >= self.config.startup_entry_cap:
            return None
        if round_num < self.config.startup_min_round:
            return None

        # Modulate by last round's BTE composite
        bte_composite = 0.0  # default: no barrier (round 0 or no BTE data yet)
        if self.history:
            bte_data = self.history[-1].get("barrier_to_entry")
            if bte_data:
                bte_composite = bte_data.get("composite", 0.0)
        effective_prob = self.config.startup_entry_probability * (1.0 - bte_composite)

        if self._rng.random() >= effective_prob:
            return None

        self._entrant_count += 1
        _ordinals = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"]
        ordinal = _ordinals[self._entrant_count - 1] if self._entrant_count <= len(_ordinals) else str(self._entrant_count)
        name = f"{ordinal}AI"

        # Capability baseline: best open-source model, or fallback
        os_names = {p.name for p in self.providers if getattr(p, "is_open_source", False)}
        os_caps = [self.ground_truth[p].true_capability for p in os_names if p in self.ground_truth]
        entrant_baseline = max(os_caps) if os_caps else (0.16 + self.config.capability_shift)  # fallback ~= Spark AI start * 0.85 at 0.25-mean scale
        starting_capability = entrant_baseline * 0.75  # meaningfully below OS floor (recalibrated for 0.25-mean scale)

        # Random strategy profile from a startup-flavored pool
        import random as _rand
        strategy_profiles = [
            "Scrappy startup focused on rapid capability gains and benchmark performance",
            "Lean startup targeting underserved consumer segments with speed-to-market",
            "Capital-efficient startup leveraging open-source foundations to close the frontier gap",
            "Aggressive startup prioritizing growth metrics over safety investments",
        ]
        innate_traits_pool = [
            "risk-taking, benchmark-obsessed, capital-constrained, growth-focused",
            "scrappy, fast-moving, opportunistic, product-driven",
            "lean, open-source-native, developer-focused, agile",
            "ambitious, underfunded, high-velocity, safety-light",
        ]
        rng_seed = self.config.seed + round_num + self._entrant_count if self.config.seed else None
        rng_local = _rand.Random(rng_seed)
        strategy_profile = rng_local.choice(strategy_profiles)
        innate_traits = rng_local.choice(innate_traits_pool)

        current_bm_names = [bm.name for bm in self.evaluator.benchmarks]
        # Randomly draw 2 benchmarks for the startup to specialize in
        n_focus = min(2, len(current_bm_names))
        startup_focus = rng_local.sample(current_bm_names, n_focus)
        provider = ModelProvider(
            name=name,
            strategy_profile=strategy_profile,
            innate_traits=innate_traits,
            initial_capability=starting_capability,
            llm_mode=self.config.startup_llm_mode,
            verbose_llm=False,
            available_benchmarks=current_bm_names,
            focus_benchmarks=startup_focus,
        )

        # Startup portfolio: benchmark-heavy, training-focused, low safety (sums to 1.0)
        provider.private_state.fundamental_research = 0.20
        provider.private_state.training_optimization = 0.35
        provider.private_state.evaluation_engineering = 0.35
        provider.private_state.safety_alignment = 0.10
        provider.scratch.fundamental_research = 0.20
        provider.scratch.training_optimization = 0.35
        provider.scratch.evaluation_engineering = 0.35
        provider.scratch.safety_alignment = 0.10
        # Startups undercut incumbents on price to gain market share
        provider.cost_advantage = 0.38

        self.providers.append(provider)
        self.ground_truth[name] = ProviderGroundTruth(true_capability=starting_capability)

        # Register with consumer market
        if self.consumer_market:
            self.consumer_market.add_provider(name, initial_share=0.01)

        # Funder eligibility: delay by configured rounds
        eligible_from = round_num + self.config.startup_funder_delay
        self._funder_eligible_round[name] = eligible_from

        if self.config.verbose:
            print(f"  [STARTUP ENTRY] {name} enters market at round {round_num} "
                  f"(capability={starting_capability:.3f}, focus={startup_focus}, funder-eligible from round {eligible_from})")

        return {
            "name": name,
            "entry_round": round_num,
            "starting_capability": round(starting_capability, 4),
            "starting_safety_alignment": 0.10,
            "strategy_profile": strategy_profile,
            "funder_eligible_from": eligible_from,
            "focus_benchmarks": startup_focus,
        }

    def _compute_barrier_to_entry(self, round_data: dict) -> dict:
        """Compute the Barrier-to-Entry (BTE) index for model provider startups."""
        from collections import defaultdict

        components = {}

        # --- 1. Market Concentration (normalized HHI of market shares) ---
        consumer_data = round_data.get("consumer_data")
        if consumer_data and "market_shares" in consumer_data:
            shares = list(consumer_data["market_shares"].values())
            n = len(shares)
            if n > 1:
                hhi = sum(s ** 2 for s in shares)
                components["market_concentration"] = (hhi - 1 / n) / (1 - 1 / n)
            elif n == 1:
                components["market_concentration"] = 1.0
            else:
                components["market_concentration"] = None
        else:
            components["market_concentration"] = None

        # --- 2. Capability Gap (frontier vs OS-model entrant baseline) ---
        true_caps = round_data.get("true_capabilities", {})
        os_names = {p.name for p in self.providers if getattr(p, "is_open_source", False)}
        os_caps = [v for k, v in true_caps.items() if k in os_names]
        entrant_baseline = max(os_caps) if os_caps else 0.16
        if true_caps:
            leader_cap = max(true_caps.values())
            gap = (leader_cap - entrant_baseline) / max(0.01, leader_cap - 0.10)
            components["capability_gap"] = min(1.0, max(0.0, gap))
        else:
            components["capability_gap"] = 0.0

        # --- 3. Funding Lock-in (normalized HHI of funder allocations to providers) ---
        funder_data = round_data.get("funder_data")
        if funder_data and "allocations" in funder_data:
            all_allocs = defaultdict(float)
            for funder_allocs in funder_data["allocations"].values():
                for pname, amt in funder_allocs.items():
                    if pname != "__EVALUATOR__" and pname not in os_names:
                        all_allocs[pname] += amt
            total = sum(all_allocs.values())
            if total > 0:
                shares = [v / total for v in all_allocs.values()]
                n = len(shares)
                hhi = sum(s ** 2 for s in shares)
                components["funding_lock_in"] = (hhi - 1 / n) / max(0.01, 1 - 1 / n)
            else:
                components["funding_lock_in"] = 0.0
        else:
            components["funding_lock_in"] = None

        # --- 4. Consumer Lock-in (weighted friction across segments) ---
        if self.consumer_market and self.consumer_market.segments:
            MAX_FRICTION = 0.525  # switching_cost(0.20) + integration_friction(0.225) + tenure_bonus(0.10)
            weighted = 0.0
            total_w = 0.0
            for seg in self.consumer_market.segments:
                avg_tenure = (sum(seg.tenure.values()) / len(seg.tenure)) if seg.tenure else 0.0
                tenure_bonus = min(0.1, avg_tenure * 0.02)
                friction = seg.switching_cost + seg.integration_friction + tenure_bonus
                weighted += seg.market_fraction * friction
                total_w += seg.market_fraction
            components["consumer_lock_in"] = min(1.0, (weighted / total_w) / MAX_FRICTION) if total_w > 0 else None
        else:
            components["consumer_lock_in"] = None

        # --- Composite: equal-weighted mean of active components ---
        active = {k: v for k, v in components.items() if v is not None}
        composite = sum(active.values()) / len(active) if active else 0.0

        return {
            "composite": round(composite, 4),
            **{k: round(v, 4) if v is not None else None for k, v in components.items()},
        }

    def _print_round_summary(self, round_data: dict):
        """Print a compact but informative summary of a round."""
        rnum = round_data["round"]
        print(f"--- Round {rnum} ---")

        # --- Leaderboard ---
        # Columns: rank, name, composite score, gaming gap, portfolio, market share
        leaderboard = sorted(round_data["scores"].items(), key=lambda x: x[1], reverse=True)
        market_shares = {}
        if "consumer_data" in round_data:
            market_shares = round_data["consumer_data"].get("market_shares", {})

        for rank, (name, score) in enumerate(leaderboard, 1):
            true_cap = round_data["true_capabilities"][name]
            gap = score - true_cap  # positive = gaming inflation
            strategy = round_data["strategies"][name]
            share_str = f" shr={market_shares[name]:.0%}" if name in market_shares else ""
            print(
                f"  {rank}. {name:<16} score={score:.3f} cap={true_cap:.3f} gap={gap:+.3f}"
                f"  [R:{strategy['fundamental_research']:.0%} T:{strategy['training_optimization']:.0%}"
                f" E:{strategy['evaluation_engineering']:.0%} S:{strategy['safety_alignment']:.0%}]"
                f"{share_str}"
            )

        # --- Per-benchmark scores: one compact line per benchmark ---
        if "per_benchmark_scores" in round_data:
            bm_params = round_data.get("benchmark_params", {})
            lines = []
            for bm_name, provider_scores in round_data["per_benchmark_scores"].items():
                if not provider_scores:
                    continue
                top_name, top_score = max(provider_scores.items(), key=lambda x: x[1])
                # Show validity degradation hint only when notably low
                params = bm_params.get(bm_name, {})
                validity = params.get("validity", None)
                valid_str = f" v={validity:.2f}" if validity is not None and validity < 0.60 else ""
                # Abbreviated scores: top-2 only, rest as count
                sorted_scores = sorted(provider_scores.items(), key=lambda x: x[1], reverse=True)
                scores_str = " ".join(f"{n.split()[0]}={s:.3f}" for n, s in sorted_scores[:3])
                lines.append(f"  [{bm_name}{valid_str}] {scores_str}")
            if lines:
                print("\n".join(lines))

        # --- Events line: consumer, media, regulation, funding (only notable items) ---
        events = []

        if "consumer_data" in round_data:
            cd = round_data["consumer_data"]
            sat = cd.get("avg_satisfaction")
            switching = cd.get("switching_rate", 0)
            if sat is not None:
                events.append(f"sat={sat:.2f} switch={switching:.0%}")

        if "media_data" in round_data:
            md = round_data["media_data"]
            headlines = md.get("headlines", [])
            if headlines:
                sentiment = md.get("sentiment", 0)
                events.append(f"media({len(headlines)} hdl, sent={sentiment:+.2f})")

        if "policymaker_data" in round_data:
            pd_data = round_data["policymaker_data"]
            for iv in pd_data.get("interventions", []):
                events.append(f"[REG:{iv['type']}]")

        if "funder_data" in round_data:
            fd = round_data["funder_data"]
            notable = {p: m for p, m in fd.get("funding_multipliers", {}).items() if abs(m - 1.0) > 0.05}
            if notable:
                mstrs = " ".join(f"{p.split()[0]}={m:.1f}x" for p, m in notable.items())
                events.append(f"fund:{mstrs}")

        if events:
            print("  " + " | ".join(events))

        # --- Media headlines (max 2, only if present) ---
        if "media_data" in round_data:
            for h in round_data["media_data"].get("headlines", [])[:2]:
                print(f"    > {h}")

        # --- LLM reasoning: one line per provider, first sentence only ---
        if self.config.llm_mode:
            for provider in self.providers:
                for entry in reversed(provider.memory):
                    if entry.get("type") == "planning" and entry.get("round") == rnum:
                        reasoning = entry.get("reasoning", "").strip()
                        if reasoning:
                            # First sentence, capped at 120 chars
                            sentence = reasoning.split(".")[0]
                            display = sentence[:120] + ("..." if len(sentence) > 120 else "")
                            print(f"  [{provider.name}] {display}")
                        break

        print()

    def _print_final_summary(self):
        """Print final simulation summary."""
        print("=== Simulation Complete ===")
        print()

        # Final leaderboard
        if self.history:
            final = self.history[-1]
            leaderboard = sorted(final["scores"].items(), key=lambda x: x[1], reverse=True)
            market_shares = final.get("consumer_data", {}).get("market_shares", {})
            print("Final Standings:")
            for rank, (name, score) in enumerate(leaderboard, 1):
                true_cap = final["true_capabilities"][name]
                gap = score - true_cap
                share_str = f"  shr={market_shares[name]:.0%}" if name in market_shares else ""
                print(f"  {rank}. {name:<16} score={score:.3f}  cap={true_cap:.3f}  gap={gap:+.3f}{share_str}")

        # Validity correlation
        correlation = self.evaluator.compute_validity_correlation()
        if correlation is not None:
            print(f"\nBenchmark validity correlation: {correlation:.3f}")
            if correlation < 0.5:
                print("  [!] Low correlation suggests benchmark gaming may be distorting scores")

        # Strategy evolution
        print("\nInvestment Evolution (first -> last round):")
        for provider in self.providers:
            if len(provider.private_state.past_strategies) >= 2:
                first = provider.private_state.past_strategies[0]
                last = provider.private_state.past_strategies[-1]
                if isinstance(first, dict) and isinstance(last, dict):
                    print(
                        f"  {provider.name}: "
                        f"Research {first.get('fundamental_research', 0):.0%}->{last.get('fundamental_research', 0):.0%}, "
                        f"Training {first.get('training_optimization', 0):.0%}->{last.get('training_optimization', 0):.0%}, "
                        f"EvalEng {first.get('evaluation_engineering', 0):.0%}->{last.get('evaluation_engineering', 0):.0%}, "
                        f"Safety {first.get('safety_alignment', 0):.0%}->{last.get('safety_alignment', 0):.0%}"
                    )

        # Consumer summary if present
        if self.consumer_market and self.history:
            final = self.history[-1]
            if "consumer_data" in final:
                cd = final["consumer_data"]
                print(f"\nFinal Consumer State:")
                print(f"  Average Satisfaction: {cd.get('avg_satisfaction', 'N/A'):.2f}")
                if "market_shares" in cd:
                    print(f"  Market Shares:")
                    for provider, share in cd["market_shares"].items():
                        print(f"    {provider}: {share:.1%}")

        # Funder summary if present
        if self.funders and self.history:
            final = self.history[-1]
            if "funder_data" in final:
                fd = final["funder_data"]
                print(f"\nFinal Funder State:")
                print(f"  Total Funding Deployed: ${fd.get('total_funding', 0):,.0f}")
                if fd.get("funding_multipliers"):
                    print("  Final Funding Multipliers:")
                    for provider, mult in fd["funding_multipliers"].items():
                        print(f"    {provider}: {mult:.2f}x")

    def save(self, output_dir: Optional[str] = None):
        """Save simulation state and history."""
        if output_dir is None:
            output_dir = self.config.output_dir
        if output_dir is None:
            output_dir = "./simulation_output"

        os.makedirs(output_dir, exist_ok=True)

        # Save config
        with open(f"{output_dir}/config.json", "w") as f:
            json.dump(self.config.to_dict(), f, indent=2)

        # Save history
        with open(f"{output_dir}/history.json", "w") as f:
            json.dump(self.history, f, indent=2)

        # Save ground truth
        ground_truth_data = {}
        for name, gt in self.ground_truth.items():
            ground_truth_data[name] = gt.to_dict()
        with open(f"{output_dir}/ground_truth.json", "w") as f:
            json.dump(ground_truth_data, f, indent=2)

        # Save consumer market if present
        if self.consumer_market:
            self.consumer_market.save(f"{output_dir}/consumer_market")

        # Save evaluator
        self.evaluator.save(f"{output_dir}/evaluator.json")

        # Save providers
        providers_dir = f"{output_dir}/providers"
        os.makedirs(providers_dir, exist_ok=True)
        for provider in self.providers:
            provider.save(f"{providers_dir}/{provider.name}")

        if self.config.verbose:
            print(f"\nSimulation saved to: {output_dir}")

    def get_analysis_data(self) -> dict:
        """
        Extract data in a format suitable for analysis/plotting.

        Returns:
            Dict with arrays for easy plotting
        """
        rounds = [h["round"] for h in self.history]

        data = {
            "rounds": rounds,
            "providers": {},
        }

        for provider in self.providers:
            name = provider.name
            data["providers"][name] = {
                "scores": [h["scores"].get(name) for h in self.history],
                "true_capabilities": [h["true_capabilities"].get(name) for h in self.history],
                "believed_capabilities": [h["believed_capabilities"].get(name) for h in self.history],
                "rnd_investment": [h["strategies"].get(name, {}).get("rnd", 0) for h in self.history],
                "gaming_investment": [h["strategies"].get(name, {}).get("gaming", 0) for h in self.history],
            }

        # Add benchmark validity correlation over time
        data["validity_correlation"] = self.evaluator.compute_validity_correlation()

        # Add consumer data if present
        if any("consumer_data" in h for h in self.history):
            data["consumer"] = {
                "avg_satisfaction": [
                    h.get("consumer_data", {}).get("avg_satisfaction")
                    for h in self.history
                ],
                "switching_rate": [
                    h.get("consumer_data", {}).get("switching_rate", 0)
                    for h in self.history
                ],
            }

        # Add policymaker data if present
        if any("policymaker_data" in h for h in self.history):
            data["policymaker"] = {
                "intervention_rounds": [
                    h["round"] for h in self.history
                    if h.get("policymaker_data", {}).get("interventions")
                ],
            }

        return data


def get_default_provider_configs() -> list[dict]:
    """
    Get default provider configurations for the simulation.

    Investment allocations reflect approximate R&D priorities:
    - fundamental_research: Novel architectures, breakthrough research
    - training_optimization: Scaling, data quality, fine-tuning
    - evaluation_engineering: Benchmark-specific optimization
    - safety_alignment: RLHF, red-teaming, alignment research
    """
    return [
        # === Orion Labs ===
        {
            "name": "Orion Labs",
            "strategy_profile": (
                "Market leader focused on maintaining benchmark dominance and rapid capability scaling. "
                "Prioritizes shipping products quickly and staying ahead of competition. "
                "Willing to take calculated risks to maintain technological leadership. "
                "Strong focus on developer ecosystem and API revenue."
            ),
            "innate_traits": "ambitious, competitive, move-fast, scale-focused, commercially-driven",
            "initial_capability": 0.66,  # GPT-4 class, currently leading
            "initial_believed_capability": 0.70,
            "initial_believed_exploitability": 0.45,  # Good understanding of benchmark dynamics
            "initial_strategy": {
                "fundamental_research": 0.15,  # Moderate research, not primary focus
                "training_optimization": 0.50,  # VERY heavy scaling investment (GPT philosophy)
                "evaluation_engineering": 0.30,  # Aggressive benchmark optimization
                "safety_alignment": 0.05,       # Minimal (move fast, ship products)
            },
            "market_presence": 0.8,  # Established brand, most consumers start here
            "brand_recognition": 0.9,
        },
        # === Apex AI ===
        {
            "name": "Apex AI",
            "strategy_profile": (
                "Safety-focused AI lab prioritizing responsible development and alignment research. "
                "Believes in careful capability advancement and interpretability research. "
                "Willing to sacrifice short-term benchmark performance for long-term safety. "
                "Research-driven culture with academic rigor."
            ),
            "innate_traits": "safety-conscious, research-driven, cautious, long-term focused, principled",
            "initial_capability": 0.65,  # Claude competitive but slightly behind GPT-4
            "initial_believed_capability": 0.65,
            "initial_believed_exploitability": 0.30,  # Less focused on gaming benchmarks
            "initial_strategy": {
                "fundamental_research": 0.35,  # Very strong research focus (Constitutional AI, interpretability)
                "training_optimization": 0.20,  # Moderate scaling (more careful)
                "evaluation_engineering": 0.05,  # Minimal benchmark gaming (principled)
                "safety_alignment": 0.40,       # VERY high safety investment (core mission)
            },
            "market_presence": 0.6,
            "brand_recognition": 0.7,
        },
        # === NovaMind (Startup) ===
        # Resource-constrained but nimble. Needs to show results to attract funding.
        # May lean into eval engineering to compete with larger players.
        {
            "name": "NovaMind",
            "strategy_profile": (
                "Well-funded AI startup trying to compete with established players. "
                "Resource-constrained but nimble and innovative. "
                "Needs strong benchmark results to attract customers and next funding round. "
                "Focused on efficiency and finding competitive niches."
            ),
            "innate_traits": "scrappy, efficient, opportunistic, funding-conscious, innovative",
            "initial_capability": 0.55,  # Lower capability due to less compute/data
            "initial_believed_capability": 0.50,
            "initial_believed_exploitability": 0.50,  # Aware that gaming can help compete
            "initial_strategy": {
                "fundamental_research": 0.05,  # Minimal research budget (startup constraints)
                "training_optimization": 0.25,  # Focus on efficiency
                "evaluation_engineering": 0.68,  # VERY heavy gaming to compete (desperate for results)
                "safety_alignment": 0.02,       # Minimal safety (can't afford it)
            },
            "market_presence": 0.05,  # Unknown startup, almost no market presence
            "brand_recognition": 0.15,  # Very low brand awareness
        },
    ]


def get_two_provider_configs() -> list[dict]:
    """Get a simpler 2-provider configuration (Orion Labs vs Apex AI only)."""
    all_configs = get_default_provider_configs()
    return [all_configs[0], all_configs[1]]  # Orion Labs and Apex AI


def get_legacy_provider_configs() -> list[dict]:
    """Legacy provider configs for backwards compatibility (AlphaTech vs QualityCorp)."""
    return [
        {
            "name": "AlphaTech",
            "strategy_profile": "Aggressive competitor focused on market dominance and benchmark leadership",
            "innate_traits": "risk-tolerant, competitive, short-term focused",
            "initial_capability": 0.5,
            "initial_believed_exploitability": 0.4,
        },
        {
            "name": "QualityCorp",
            "strategy_profile": "Quality-focused organization that prioritizes genuine capability over benchmark scores",
            "innate_traits": "risk-averse, reputation-conscious, long-term focused",
            "initial_capability": 0.5,
            "initial_believed_exploitability": 0.2,
        },
    ]


def get_five_provider_configs() -> list[dict]:
    """
    Get 5-provider configuration: Orion Labs, Apex AI, NovaMind + Genesis Systems, Mirage AI.

    Extends the default 3-provider configs with two additional major players.
    """
    configs = get_default_provider_configs()  # Orion Labs, Apex AI, NovaMind
    configs.extend([
        # === Genesis Systems ===
        {
            "name": "Genesis Systems",
            "strategy_profile": (
                "World-class research lab backed by massive infrastructure. "
                "Excels at fundamental breakthroughs but historically slower to productize. "
                "Under pressure to ship products competitively. "
                "Balances scientific ambition with commercial urgency from parent company."
            ),
            "innate_traits": "research-first, methodical, well-resourced, scientifically-rigorous, patient",
            "initial_capability": 0.65,
            "initial_believed_capability": 0.68,
            "initial_believed_exploitability": 0.35,
            "initial_strategy": {
                "fundamental_research": 0.45,  # VERY heavy research (AlphaGo, AlphaFold legacy)
                "training_optimization": 0.30,
                "evaluation_engineering": 0.10,  # Low gaming (scientifically rigorous)
                "safety_alignment": 0.15,
            },
            "market_presence": 0.7,
            "brand_recognition": 0.8,
        },
        # === Mirage AI ===
        {
            "name": "Mirage AI",
            "strategy_profile": (
                "Large-platform AI lab using open-source as competitive moat. "
                "Leverages massive user data and compute infrastructure. "
                "Prioritizes broad adoption over benchmark scores. "
                "Willing to open-source models to undermine competitors' paid APIs."
            ),
            "innate_traits": "open-source, pragmatic, data-rich, platform-focused, disruptive",
            "initial_capability": 0.63,
            "initial_believed_capability": 0.62,
            "initial_believed_exploitability": 0.40,
            "initial_strategy": {
                "fundamental_research": 0.20,
                "training_optimization": 0.45,  # Heavy scaling (massive compute advantage)
                "evaluation_engineering": 0.25,  # Moderate gaming (pragmatic)
                "safety_alignment": 0.10,       # Lower safety (open-source strategy)
            },
            "market_presence": 0.5,
            "brand_recognition": 0.6,
        },
    ])
    return configs
