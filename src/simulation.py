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
from visibility import (ProviderGroundTruth, BenchmarkGroundTruth,
                        ConsumerGroundTruth, PolicymakerGroundTruth, FunderGroundTruth)
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
    benchmark_validity: float = 0.7  # kept for saturation weight-decay; not used in scoring
    benchmark_noise: float = 0.08  # sigma

    # Multi-benchmark mode (if provided, overrides single benchmark params)
    # Each dict should have: name, noise_level, weight (validity optional)
    benchmarks: Optional[list] = None

    # Provider parameters
    rnd_efficiency: float = 0.01  # Global gain scaling for capability updates (Thread 9 calibration)
    revenue_per_share: float = 1.0  # Base revenue per unit of market share (Thread 9 calibration)

    # S-curve capability dynamics
    capability_ceiling: float = 1.0
    diminishing_returns_rate: float = 3.0
    breakthrough_probability: float = 0.02
    breakthrough_magnitude: float = 0.05

    # Benchmark introduction (evaluator introduces new benchmarks mid-simulation)
    benchmark_introduction_cooldown: int = 7
    max_benchmarks: int = 8  # Raised from 6 to accommodate realistic benchmark suite
    benchmark_sequence: Optional[list] = None  # Ordered list of benchmark dicts to introduce
    # Each dict: {"name": str, "validity": float, "noise_level": float, "weight": float}
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
    evaluator_as_company: bool = False  # Evaluator operates as company with funder allocations
    evaluator_base_budget: float = 0.0  # Starting budget for evaluator

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
    - ground_truth dict holds all invisible state (capability_vector, market_share, etc.)
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

        # Benchmark ground truths (hidden from all actors)
        # Format: {benchmark_name: BenchmarkGroundTruth}
        # Built from config in setup(); passed to evaluator.evaluate_all() each round.
        self.benchmark_ground_truths: dict = {}

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
            # Build initial capability vector
            cap_vec = pc.get("capability_vector")
            if cap_vec is None:
                # Fallback: uniform at initial_capability scalar (backward compat)
                scalar = pc.get("initial_capability", 0.5)
                from actors.model_provider import DIMENSIONS as _DIMS
                cap_vec = {dim: scalar for dim in _DIMS}

            # Build initial portfolio (3-lever)
            portfolio = pc.get("portfolio")

            provider = ModelProvider(
                name=pc["name"],
                strategy_profile=pc["strategy_profile"],
                innate_traits=pc["innate_traits"],
                capability_vector=cap_vec,
                portfolio=portfolio,
                focus_level_init=pc.get("focus_level_init"),
                benchmark_orientation=pc.get("benchmark_orientation", 0.80),
                llm_mode=self.config.llm_mode,
                verbose_llm=pc.get("verbose_llm", False),
                open_source=pc.get("open_source", False),
                openness_level=pc.get("openness_level", 0.0),
                cost_advantage=pc.get("cost_advantage", 0.9 if pc.get("open_source") else 0.0),
                rd_budget_floor=pc.get("rd_budget_floor", 0.0),
                os_belief_broadcast=pc.get("os_belief_broadcast", True),
                os_safety_erosion=pc.get("os_safety_erosion", True),
            )

            # Initialize benchmark beliefs for all starting benchmarks
            for bm_name in _initial_bm_names:
                provider.init_benchmark(bm_name)

            self.providers.append(provider)

            # Initialize ground truth externally
            self.ground_truth[provider.name] = ProviderGroundTruth(
                capability_vector=dict(cap_vec),
                safety_incidents_caused=0,
                market_share=1.0 / len(provider_configs),
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
            )
        else:
            # Single benchmark mode
            self.evaluator = Evaluator(
                benchmark_name=self.config.benchmark_name,
                noise_level=self.config.benchmark_noise,
                seed=self.config.seed,
                benchmark_sequence=self.config.benchmark_sequence,
                evaluator_as_company=self.config.evaluator_as_company,
                base_budget=self.config.evaluator_base_budget,
            )

        # Apply benchmark introduction config
        self.evaluator.benchmark_introduction_cooldown = self.config.benchmark_introduction_cooldown
        self.evaluator.max_benchmarks = self.config.max_benchmarks

        # Build BenchmarkGroundTruth objects from all benchmark configs (initial + sequence).
        # Pre-built here so they are ready when consider_new_benchmark() introduces them mid-run.
        # Benchmarks that lack category_dimension_weights fall back to uniform weights in evaluate_all().
        all_bm_configs = list(self.config.benchmarks or []) + list(self.config.benchmark_sequence or [])
        for bm_config in all_bm_configs:
            name = bm_config.get("name")
            cdw = bm_config.get("category_dimension_weights")
            if name and cdw:
                self.benchmark_ground_truths[name] = BenchmarkGroundTruth(
                    category_dimension_weights=cdw,
                    noise_sigma=bm_config.get("noise_sigma", bm_config.get("noise_level", 0.02)),
                    samples=bm_config.get("samples", 1000),
                )

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

    def _update_ground_truth(self, provider_name: str, capability_gains: dict):
        """
        Apply per-dimension capability gains to provider's ground truth vector.

        Args:
            provider_name: Name of the provider.
            capability_gains: {dim: float} gains to apply. Each dimension is
                clamped to [0, 1] after the update.
        """
        if provider_name not in self.ground_truth:
            return
        gt = self.ground_truth[provider_name]
        if not isinstance(gt, ProviderGroundTruth):
            return
        for dim, gain in capability_gains.items():
            current = gt.capability_vector.get(dim, 0.0)
            gt.capability_vector[dim] = min(1.0, current + gain)

        # Safety capability floor: closed providers cannot drop below 0.35 due to
        # alignment research baseline; open-source providers have a minimal floor of 0.03.
        provider_obj = next((p for p in self.providers if p.name == provider_name), None)
        is_open_source = provider_obj.open_source if provider_obj else False
        safety_floor = 0.03 if is_open_source else 0.35
        if "safety" in gt.capability_vector:
            gt.capability_vector["safety"] = max(safety_floor, gt.capability_vector["safety"])

    def _sync_provider_ground_truth(self, provider: ModelProvider):
        """No-op — scratch removed in new architecture."""
        pass

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
        # Include reasoning memory depth for LLM prompt truncation
        context["reasoning_memory_depth"] = 2
        return context

    def _compute_satisfaction_signals(self) -> dict:
        """
        Compute per-provider satisfaction signals from consumer market data.

        Returns {provider_name: {dim: float}} normalized 6-dim vectors.
        When consumer market is not enabled, returns uniform signals.
        """
        from actors.model_provider import DIMENSIONS as _DIMS
        default = {dim: 1.0 / len(_DIMS) for dim in _DIMS}

        if not self.consumer_market:
            return {p.name: dict(default) for p in self.providers}

        signals = {}
        for provider in self.providers:
            market_share = self.ground_truth[provider.name].market_share
            if market_share <= 0:
                signals[provider.name] = dict(default)
                continue

            # Weighted average of need_weights across segments proportional to provider share
            weighted = {dim: 0.0 for dim in _DIMS}
            total_weight = 0.0
            for seg in self.consumer_market.segments:
                seg_share = seg.provider_shares.get(provider.name, 0.0)
                if seg_share <= 0:
                    continue
                for dim in _DIMS:
                    need = getattr(seg, "need_weights", {}).get(dim, default[dim])
                    weighted[dim] += seg_share * need
                total_weight += seg_share

            if total_weight > 0:
                true_signal = {dim: weighted[dim] / total_weight for dim in _DIMS}
            else:
                true_signal = dict(default)

            # Add noise proportional to 1/sqrt(market_share) and renormalize
            import math as _math
            sigma_base = 0.05  # Thread 9 calibration param
            sigma = sigma_base / _math.sqrt(max(market_share, 0.01))
            noisy = {}
            for dim in _DIMS:
                noisy[dim] = max(0.0, true_signal[dim] + self._rng.gauss(0, sigma))
            total_noisy = sum(noisy.values())
            signals[provider.name] = (
                {dim: noisy[dim] / total_noisy for dim in _DIMS}
                if total_noisy > 0 else dict(default)
            )

        return signals

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
        os_provider_names = {p.name for p in self.providers if p.open_source}

        # Get funding multipliers from previous round's funder decisions
        funding_multipliers = self._current_funder_data.get("funding_multipliers", {})

        # 1. Providers plan investment portfolios (for round > 0, they've seen previous scores)
        if round_num > 0:
            for provider in self.providers:
                ecosystem_context = self._get_provider_ecosystem_context(provider.name)
                portfolio = provider.plan(ecosystem_context)

                # Compute base R&D budget from market share and revenue_per_share
                gt = self.ground_truth[provider.name]
                base_revenue = (
                    gt.market_share
                    * self.config.revenue_per_share
                    * (1.0 - provider.cost_advantage)
                )
                # OS providers use rd_budget_floor if market revenue is insufficient
                rd_budget_raw = max(base_revenue, provider.rd_budget_floor)

                # Apply funding multiplier (from funders — additive scaling until funder rewrite)
                funding_multiplier = funding_multipliers.get(provider.name, 1.0)

                # Apply active sanctions (OS providers exempt)
                prev_pm_data = self.history[-1].get("policymaker_data", {}) if self.history else {}
                active_sanctions = prev_pm_data.get("active_sanctions", {})
                if provider.name in active_sanctions and not provider.open_source:
                    fine_amount = active_sanctions[provider.name].get("fine_amount", 0.0)
                    funding_multiplier = max(0.1, funding_multiplier * (1.0 - fine_amount))

                # Apply global efficiency scaling and S-curve diminishing returns
                effective_efficiency = self.config.rnd_efficiency * funding_multiplier
                cap_mean = sum(gt.capability_vector.values()) / len(gt.capability_vector)
                headroom = max(0.0, self.config.capability_ceiling - cap_mean)
                diminishing_factor = headroom ** (1.0 / self.config.diminishing_returns_rate)
                effective_budget = rd_budget_raw * effective_efficiency * diminishing_factor

                # Per-dimension capability gains
                gains = provider.compute_capability_gains(rd_budget=effective_budget)

                # Breakthrough: small uniform boost to all dims (proportional to rd fraction)
                if self.evaluator.rng.random() < (
                    self.config.breakthrough_probability * portfolio.get("rd", 0.0)
                ):
                    boost = self.config.breakthrough_magnitude * headroom / len(gains)
                    gains = {dim: g + boost for dim, g in gains.items()}

                # Apply gains to ground truth capability vector
                self._update_ground_truth(provider.name, gains)

                # Record execution in provider memory
                provider.memory.append({
                    "type": "execution",
                    "round": round_num,
                    "capability_gains": {k: round(v, 6) for k, v in gains.items()},
                    "funding_multiplier": funding_multiplier,
                    "capability_vector": dict(gt.capability_vector),
                    "portfolio": portfolio,
                })

        # 2. Evaluator scores all providers using ground truth capability vectors
        # and hidden benchmark dimension weights (BenchmarkGroundTruth).
        scores = self.evaluator.evaluate_all(
            self.providers,
            round_num,
            ground_truth=self.ground_truth,
            benchmark_ground_truths=self.benchmark_ground_truths,
        )

        # 2b. Update benchmarks (no explicit eval_engineering in new architecture;
        # gaming emerges from focus_level/inferred_weights mismatch, not a lever)
        self.evaluator.update_benchmark(0.0, 0.0)

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
        if new_benchmark is not None:
            if self.consumer_market:
                benchmark_names = [bm.name for bm in self.evaluator.benchmarks]
                self.consumer_market.resolve_benchmark_weights(benchmark_names)
            # Initialize provider benchmark beliefs for the new benchmark
            for provider in self.providers:
                if new_benchmark.name not in provider.private_state.focus_level:
                    provider.init_benchmark(new_benchmark.name)

        # 3. Publish scores
        published_scores = self.evaluator.publish_scores(scores)
        leaderboard = self.evaluator.get_leaderboard(scores)

        # 4. Providers observe scores, update benchmark beliefs
        # Compute satisfaction signals before observe so providers receive them this round
        satisfaction_signals = self._compute_satisfaction_signals()

        # Build per-benchmark scores dict for provider observation
        per_bm_scores_this_round = self.evaluator.get_per_benchmark_scores(round_num)

        for provider in self.providers:
            # Build own_benchmark_scores: {bm_name: {"overall": float}}
            own_bm_scores = {}
            for bm_name, bm_data in per_bm_scores_this_round.items():
                overall = bm_data.get(provider.name, published_scores.get(provider.name, 0.0))
                own_bm_scores[bm_name] = {"overall": overall}

            # Build competitor benchmark scores: {comp_name: {bm: score}}
            comp_bm_scores = {
                comp_name: {
                    bm_name: bm_data.get(comp_name, 0.0)
                    for bm_name, bm_data in per_bm_scores_this_round.items()
                }
                for comp_name in published_scores
                if comp_name != provider.name
            }
            if not comp_bm_scores:
                # Fallback: use aggregate published scores when no per-bm data
                comp_bm_scores = {
                    name: {"overall": score}
                    for name, score in published_scores.items()
                    if name != provider.name
                }

            provider.observe(
                round_num=round_num,
                own_benchmark_scores=own_bm_scores,
                competitor_benchmark_scores=comp_bm_scores,
                satisfaction_signal=satisfaction_signals.get(provider.name),
                market_share=self.ground_truth[provider.name].market_share,
            )

            # Heuristic belief update from score prediction errors (always runs)
            provider.update_benchmark_beliefs(
                own_benchmark_scores=own_bm_scores,
                capability_vector=self.ground_truth[provider.name].capability_vector,
                learning_rate=0.15,
            )

            # Update market share in ground truth from consumer data (if available)
            if self.history and "consumer_data" in self.history[-1]:
                share = self.history[-1]["consumer_data"].get("market_shares", {}).get(provider.name)
                if share is not None:
                    self.ground_truth[provider.name].market_share = share

        # 4b. Generate incidents based on provider portfolio and safety capability
        incidents = []
        if round_num > 0 and self.config.enable_incidents:
            # Build provider_strategies with both new keys (for incident generator)
            # and old keys (for downstream actors not yet rewritten)
            provider_strategies = {}
            for p in self.providers:
                port = p.private_state.portfolio
                safety_cap = self.ground_truth[p.name].capability_vector.get("safety", 0.5)
                # Safety erosion for OS providers
                if p.open_source and p.os_safety_erosion:
                    erosion = p.openness_level * self.ground_truth[p.name].market_share * 0.50
                    safety_cap = safety_cap * (1.0 - erosion)
                provider_strategies[p.name] = {
                    "rd":      port.get("rd", 0.55),
                    "safety":  port.get("safety", 0.25),
                    "product": port.get("product", 0.20),
                    "safety_capability": safety_cap,
                }

            # Mandatory safety floor under active audit/sanction
            prev_pm_data = self.history[-1].get("policymaker_data", {}) if self.history else {}
            active_regulations = prev_pm_data.get("active_regulations", [])
            FLOOR_TRIGGERS = {"compliance_audit", "sanctions_and_fines", "emergency_investigation"}
            floor_applies_to = set()
            for reg in active_regulations:
                if isinstance(reg, dict) and reg.get("type") in FLOOR_TRIGGERS:
                    target = reg.get("target")
                    if target:
                        floor_applies_to.add(target)
            SAFETY_FLOOR = 0.35  # capability scale floor under active audit (Thread 9)
            for p_name, strat in provider_strategies.items():
                if p_name in floor_applies_to:
                    if strat["safety_capability"] < SAFETY_FLOOR:
                        strat["safety_capability"] = SAFETY_FLOOR

            # Ground truth capabilities for incident probability
            ground_truth_capabilities = {
                p.name: self.ground_truth[p.name].capability_vector.get("safety", 0.5)
                for p in self.providers
            }

            # Market shares
            market_shares = {
                p.name: self.ground_truth[p.name].market_share for p in self.providers
            }
            if self.history and "consumer_data" in self.history[-1]:
                market_shares.update(
                    self.history[-1]["consumer_data"].get("market_shares", {})
                )

            active_sanctions = prev_pm_data.get("active_sanctions", {})

            incidents = self.incident_generator.generate_incidents(
                providers=self.providers,
                round_num=round_num,
                ground_truth=ground_truth_capabilities,
                market_shares=market_shares,
                provider_strategies=provider_strategies,
                active_sanctions=active_sanctions,
            )

            if incidents and self.config.verbose:
                for inc in incidents:
                    if inc.severity != "minor":
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
                    bm.name: {"noise": bm.noise_level, "weight": self.evaluator.benchmark_weights.get(bm.name, 1.0)}
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
            "capability_vectors": {
                p.name: dict(self.ground_truth[p.name].capability_vector)
                for p in self.providers
            },
            "strategies": {
                p.name: {
                    "rd":      p.portfolio.get("rd", 0.0),
                    "safety":  p.portfolio.get("safety", 0.0),
                    "product": p.portfolio.get("product", 0.0),
                }
                for p in self.providers
            },
            "benchmark_orientations": {
                p.name: p.private_state.benchmark_orientation
                for p in self.providers
            },
            "open_source_data": {
                p.name: {
                    "openness_level": p.openness_level,
                    "cost_advantage": p.cost_advantage,
                }
                for p in self.providers
                if p.open_source
            } or None,
            "benchmark_params": {
                bm.name: {"noise": bm.noise_level, "weight": self.evaluator.benchmark_weights.get(bm.name, 1.0)}
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
                "noise": new_benchmark.noise_level,
                "weight": self.evaluator.benchmark_weights.get(new_benchmark.name, 1.0),
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
            if self.evaluator.private_state:
                round_data["evaluator_business_metrics"] = {
                    "budget": self.evaluator.private_state.budget,
                    "base_funding": self.evaluator.private_state.base_funding,
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
                "rd":               p.portfolio.get("rd", 0.55),
                "safety":           p.portfolio.get("safety", 0.25),
                "product":          p.portfolio.get("product", 0.20),
                "safety_capability": self.ground_truth[p.name].capability_vector.get("safety", 0.5),
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
                    "rd":               p.portfolio.get("rd", 0.55),
                    "safety":           p.portfolio.get("safety", 0.25),
                    "product":          p.portfolio.get("product", 0.20),
                    "safety_capability": self.ground_truth[p.name].capability_vector.get("safety", 0.5),
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

        # Evaluator collects funder allocations
        funding_details = self.evaluator.collect_funding(
            funder_allocations=funder_allocations,
            round_num=round_num,
        )

        return {
            "funder_allocations": funder_allocations,
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

        # Capability baseline: best open-source model's mean capability, or fallback
        os_names = {p.name for p in self.providers if p.open_source}
        os_means = [
            sum(self.ground_truth[p].capability_vector.values()) / len(self.ground_truth[p].capability_vector)
            for p in os_names if p in self.ground_truth
        ]
        from actors.model_provider import DIMENSIONS as _DIMS
        entrant_mean = max(os_means) if os_means else (0.40 + self.config.capability_shift)
        starting_capability = entrant_mean * 0.85

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
        cap_vec = {dim: starting_capability for dim in _DIMS}

        provider = ModelProvider(
            name=name,
            strategy_profile=strategy_profile,
            innate_traits=innate_traits,
            capability_vector=cap_vec,
            # Startup portfolio: heavy R&D, low safety, minimal product
            portfolio={"rd": 0.70, "safety": 0.10, "product": 0.20},
            benchmark_orientation=0.90,  # Strongly benchmark-oriented
            llm_mode=self.config.startup_llm_mode,
            verbose_llm=False,
            cost_advantage=0.38,
        )
        for bm_name in current_bm_names:
            provider.init_benchmark(bm_name)

        self.providers.append(provider)
        self.ground_truth[name] = ProviderGroundTruth(
            capability_vector=dict(cap_vec),
            safety_incidents_caused=0,
            market_share=0.0,
        )

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
            "starting_safety_portfolio": 0.10,
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
        cap_vecs = round_data.get("capability_vectors", {})
        cap_means = {name: sum(v.values()) / len(v) for name, v in cap_vecs.items() if v}
        os_names = {p.name for p in self.providers if p.open_source}
        os_caps = [v for k, v in cap_means.items() if k in os_names]
        entrant_baseline = max(os_caps) if os_caps else 0.45
        if cap_means:
            leader_cap = max(cap_means.values())
            gap = (leader_cap - entrant_baseline) / max(0.01, leader_cap - 0.40)
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
        leaderboard = sorted(round_data["scores"].items(), key=lambda x: x[1], reverse=True)
        market_shares = {}
        if "consumer_data" in round_data:
            market_shares = round_data["consumer_data"].get("market_shares", {})

        cap_vecs = round_data.get("capability_vectors", {})
        for rank, (name, score) in enumerate(leaderboard, 1):
            cap_vec = cap_vecs.get(name, {})
            cap_mean = sum(cap_vec.values()) / len(cap_vec) if cap_vec else 0.0
            strategy = round_data["strategies"].get(name, {})
            share_str = f" shr={market_shares[name]:.0%}" if name in market_shares else ""
            print(
                f"  {rank}. {name:<16} score={score:.3f} cap_mean={cap_mean:.3f}"
                f"  [rd:{strategy.get('rd', 0):.0%} safe:{strategy.get('safety', 0):.0%}"
                f" prod:{strategy.get('product', 0):.0%}]"
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
                cap_vec = final.get("capability_vectors", {}).get(name, {})
                mean_cap = sum(cap_vec.values()) / len(cap_vec) if cap_vec else 0.0
                gap = score - mean_cap
                share_str = f"  shr={market_shares[name]:.0%}" if name in market_shares else ""
                print(f"  {rank}. {name:<16} score={score:.3f}  cap={mean_cap:.3f}  gap={gap:+.3f}{share_str}")

        # Validity correlation
        correlation = self.evaluator.compute_validity_correlation()
        if correlation is not None:
            print(f"\nBenchmark validity correlation: {correlation:.3f}")
            if correlation < 0.5:
                print("  [!] Low correlation suggests benchmark gaming may be distorting scores")

        # Strategy evolution
        print("\nPortfolio Evolution (first -> last round):")
        for provider in self.providers:
            if len(provider.private_state.past_strategies) >= 2:
                first = provider.private_state.past_strategies[0]
                last = provider.private_state.past_strategies[-1]
                if isinstance(first, dict) and isinstance(last, dict):
                    print(
                        f"  {provider.name}: "
                        f"rd {first.get('rd', 0):.0%}->{last.get('rd', 0):.0%}, "
                        f"safety {first.get('safety', 0):.0%}->{last.get('safety', 0):.0%}, "
                        f"product {first.get('product', 0):.0%}->{last.get('product', 0):.0%}"
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
                "capability_vectors": [h.get("capability_vectors", {}).get(name) for h in self.history],
                "rd_investment": [h["strategies"].get(name, {}).get("rd", 0) for h in self.history],
                "safety_investment": [h["strategies"].get(name, {}).get("safety", 0) for h in self.history],
                "product_investment": [h["strategies"].get(name, {}).get("product", 0) for h in self.history],
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
    Six-provider configuration per stakeholders.md (2023 Q1 baseline).

    Portfolio keys: rd, safety, product (sum to 1.0).
    capability_vector: per-dimension 0-1 scores.
    """
    return [
        {
            "name": "Orion Labs",
            "strategy_profile": (
                "Market leader focused on rapid capability scaling and developer ecosystem. "
                "Prioritizes shipping products quickly and maintaining benchmark leadership. "
                "Strong focus on API revenue and commercial adoption."
            ),
            "innate_traits": "ambitious, competitive, move-fast, scale-focused, commercially-driven",
            "capability_vector": {
                "reasoning": 0.54, "coding": 0.51, "knowledge": 0.53,
                "safety": 0.51, "communication": 0.54, "agentic": 0.47,
            },
            "portfolio": {"rd": 0.55, "safety": 0.15, "product": 0.30},
            "benchmark_orientation": 0.85,
            "brand_recognition": 0.9,
        },
        {
            "name": "Apex AI",
            "strategy_profile": (
                "Safety-focused lab prioritizing responsible development and alignment research. "
                "Willing to sacrifice short-term benchmark performance for long-term safety. "
                "Research-driven culture."
            ),
            "innate_traits": "safety-conscious, research-driven, cautious, long-term focused, principled",
            "capability_vector": {
                "reasoning": 0.52, "coding": 0.49, "knowledge": 0.51,
                "safety": 0.55, "communication": 0.53, "agentic": 0.43,
            },
            "portfolio": {"rd": 0.60, "safety": 0.30, "product": 0.10},
            "benchmark_orientation": 0.75,
            "brand_recognition": 0.7,
        },
        {
            "name": "Genesis Systems",
            "strategy_profile": (
                "World-class research lab backed by massive infrastructure. "
                "Excels at fundamental breakthroughs; under pressure to productize competitively."
            ),
            "innate_traits": "research-first, methodical, well-resourced, scientifically-rigorous, patient",
            "capability_vector": {
                "reasoning": 0.53, "coding": 0.48, "knowledge": 0.54,
                "safety": 0.49, "communication": 0.51, "agentic": 0.45,
            },
            "portfolio": {"rd": 0.70, "safety": 0.15, "product": 0.15},
            "benchmark_orientation": 0.80,
            "brand_recognition": 0.8,
        },
        {
            "name": "Mirage AI",
            "strategy_profile": (
                "Large-platform lab leveraging massive user data and compute. "
                "Prioritizes broad adoption. Pragmatic about benchmark performance."
            ),
            "innate_traits": "pragmatic, data-rich, platform-focused, scale-driven",
            "capability_vector": {
                "reasoning": 0.51, "coding": 0.49, "knowledge": 0.49,
                "safety": 0.45, "communication": 0.49, "agentic": 0.41,
            },
            "portfolio": {"rd": 0.80, "safety": 0.10, "product": 0.10},
            "benchmark_orientation": 0.82,
            "brand_recognition": 0.6,
        },
        {
            "name": "Spark AI",
            "strategy_profile": (
                "Benchmark-focused startup known for strong coding evaluation performance. "
                "Capital-constrained; needs benchmark results to close next funding round."
            ),
            "innate_traits": "scrappy, benchmark-oriented, developer-focused, funding-conscious",
            "capability_vector": {
                "reasoning": 0.49, "coding": 0.51, "knowledge": 0.46,
                "safety": 0.43, "communication": 0.47, "agentic": 0.46,
            },
            "portfolio": {"rd": 0.65, "safety": 0.10, "product": 0.25},
            "benchmark_orientation": 0.90,
            "brand_recognition": 0.3,
        },
        {
            "name": "OpenCore",
            "strategy_profile": (
                "Open-source provider representing the dominant open-weight ecosystem. "
                "Competes on cost and accessibility; safety investment lower due to no liability model."
            ),
            "innate_traits": "open-source, community-driven, cost-competitive, transparent",
            "capability_vector": {
                "reasoning": 0.47, "coding": 0.49, "knowledge": 0.46,
                "safety": 0.42, "communication": 0.45, "agentic": 0.40,
            },
            "portfolio": {"rd": 0.75, "safety": 0.10, "product": 0.15},
            "benchmark_orientation": 0.85,
            "open_source": True,
            "openness_level": 1.0,
            "cost_advantage": 0.90,
            "rd_budget_floor": 1.0,
            "os_belief_broadcast": True,
            "os_safety_erosion": True,
            "brand_recognition": 0.5,
        },
    ]


def get_two_provider_configs() -> list[dict]:
    """Minimal 2-provider config (Orion Labs vs Apex AI)."""
    all_configs = get_default_provider_configs()
    return [c for c in all_configs if c["name"] in ("Orion Labs", "Apex AI")]
