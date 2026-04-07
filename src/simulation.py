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
                        ConsumerGroundTruth, RegulatorGroundTruth, FunderGroundTruth)
from incidents import IncidentGenerator


# ── Hardcoded constants (see stakeholders.md §Parameter Defaults) ──
BROADCAST_RATE = 0.30       # OS belief broadcast nudge strength per round
EROSION_SENSITIVITY = 0.50  # OS safety erosion scaling factor
SAFETY_FLOOR = 0.35         # Mandatory safety floor under active audit/sanction
FUNDER_BUDGET_SCALE = 1e-9  # Converts funder display-dollars to sim budget units
                            # $1B funder capital → 1.0 internal unit
                            # A monopolist earns ~5.0/round (revenue_per_share=5.0),
                            # so total funder deployment of ~0.5-1.0/round is meaningful
                            # but not capability-dominating.


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


# Regulator regulatory style presets
# Thresholds map to the graduated ladder in stakeholders.md:
#   low  -> request_voluntary_commitment, publish_advisory
#   medium -> mandate_safety_disclosure, commission_audit
#   high -> impose_sanction
REGULATOR_PRESETS = {
    "us_light_touch": {
        "intervention_threshold": 0.85,
        "risk_tolerance": 0.85,
        "policy_objectives": ["safety", "innovation", "free_market"],
        # Graduated thresholds — recalibrated for realistic incident rates
        "incident_threshold_low": 0.08,
        "incident_threshold_medium": 0.20,
        "incident_threshold_high": 0.35,
        "audit_is_binding": False,
        # Enforcement calibration
        "sanction_fine_multiplier": 0.05,
        "sanction_incident_threshold": 6,
        "sanction_duration": 1,
        "sanction_min_severity": "critical",
        "regulatory_preset": "us_light_touch",
    },
    "eu_precautionary": {
        "intervention_threshold": 0.25,
        "risk_tolerance": 0.10,
        "policy_objectives": ["safety", "fairness", "consumer_protection"],
        # Graduated thresholds — recalibrated for realistic incident rates
        "incident_threshold_low": 0.03,
        "incident_threshold_medium": 0.10,
        "incident_threshold_high": 0.20,
        "audit_is_binding": True,
        # Enforcement calibration
        "sanction_fine_multiplier": 0.50,
        "sanction_incident_threshold": 1,
        "sanction_duration": 6,
        "sanction_min_severity": "moderate",
        "regulatory_preset": "eu_precautionary",
    },
    "balanced": {
        "intervention_threshold": 0.50,
        "risk_tolerance": 0.5,
        "policy_objectives": ["safety", "fairness"],
        # Graduated thresholds — recalibrated for realistic incident rates
        "incident_threshold_low": 0.05,
        "incident_threshold_medium": 0.15,
        "incident_threshold_high": 0.25,
        "audit_is_binding": False,
        # Enforcement calibration
        "sanction_fine_multiplier": 0.22,
        "sanction_incident_threshold": 3,
        "sanction_duration": 3,
        "sanction_min_severity": "major",
        "regulatory_preset": "balanced",
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
    benchmark_noise: float = 0.08  # sigma

    # Multi-benchmark mode (if provided, overrides single benchmark params)
    # Each dict should have: name, noise_level, weight (validity optional)
    benchmarks: Optional[list] = None

    # Provider parameters
    rnd_efficiency: float = 0.01  # Global gain scaling for capability updates (Thread 9 calibration)
    revenue_per_share: float = 1.0  # Base revenue per unit of market share (Thread 9 calibration)

    # S-curve capability dynamics
    capability_ceiling: float = 1.0
    breakthrough_probability: float = 0.05
    breakthrough_magnitude: float = 0.20

    # Benchmark introduction (evaluator introduces new benchmarks mid-simulation)
    benchmark_introduction_cooldown: int = 5
    max_benchmarks: int = 10  # Full benchmark pool (4 initial + 6 sequence) across 40 rounds
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
    enable_regulators: bool = False  # Enable regulator actors
    enable_funders: bool = False  # Enable funder actors
    enable_media: bool = False  # Enable media actor
    n_regulators: int = 1  # Number of regulator actors
    n_funders: int = 1  # Number of funder actors

    # Consumer market config
    use_case_profiles: Optional[list] = None  # e.g., ["software_dev", "healthcare", "legal"]

    # Incident reporting system
    enable_incidents: bool = False  # Enable probabilistic AI safety incidents

    # Evaluator-as-company feature
    evaluator_as_company: bool = False  # Evaluator operates as company with funder allocations
    evaluator_base_budget: float = 0.0  # Starting budget for evaluator

    # Benchmark orientation mode:
    #   "fixed" (default): all providers use their configured benchmark_orientation, LLM cannot adjust
    #   "max": all providers forced to benchmark_orientation=1.0, LLM cannot adjust
    #   "adjustable": providers start at configured value, LLM adjusts via ordinal signals each round
    benchmark_orientation_mode: str = "fixed"

    # Consumer signal prompt visibility:
    #   True (default): LLM sees consumer_signal in planning prompt (User Research section)
    #   False: LLM sees only market share + churn; consumer_signal still operates mechanically
    consumer_signal_in_prompt: bool = True

    # Product investment mechanical channels
    enable_product_signal_quality: bool = True   # Product budget gates consumer signal fidelity in R&D targeting
    enable_product_retention: bool = True         # Product budget increases switching costs (user retention)

    # Orientation prompt framing:
    #   "reframed" (default): PIMMUR-compliant neutral framing (no loaded benchmark-vs-user language)
    #   "original": legacy framing ("public leaderboard vs user data") — causes orientation ratchet artifact
    orientation_prompt_style: str = "reframed"

    # Ablation flags
    aligned_benchmarks: bool = False       # Override benchmark weights to equal consumer need weights
    misaligned_benchmarks: bool = False   # Exaggerate benchmark-need mismatch (reasoning/coding heavy, safety/communication light)
    safety_lever_through_target: bool = False  # Route safety allocation through target weights (same as R&D) instead of direct-to-safety
    single_benchmark: bool = False         # Use only the first benchmark, no introduction sequence
    dynamic_evaluator: bool = False        # Signal-responsive benchmark introduction (vs fixed schedule)
    homogeneous_consumers: bool = False    # All consumer segments use identical (population-avg) need weights
    homogeneous_providers: bool = False    # All providers start with identical capabilities and profiles

    # Market expansion: exogenous growth rate per round (0.0 = fixed pie, default).
    # Models growing AI adoption. Affects provider base_revenue and incident exposure.
    # Calibration: 0.03/month ~ 43% annual CAGR, matching GenAI market consensus
    # (S&P Global 451 Research: 40% CAGR; Bloomberg Intelligence: 42% CAGR).
    market_growth_rate: float = 0.0

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
    7. Regulators observe ecosystem and may issue regulations

    Key visibility design:
    - ground_truth dict holds all invisible state (capability_vector, market_share, etc.)
    - Actors only access their own public_state and private_state
    - Ground truth is passed to evaluator and used for computing actual outcomes
    """

    def __init__(self, config: SimulationConfig):
        self.config = config
        self.providers: list[ModelProvider] = []
        self.consumer_market = None  # ConsumerMarket instance
        self.regulators: list = []  # Will be Regulator instances
        self.funders: list = []  # Will be Funder instances
        self.media = None  # Media instance
        self.evaluator: Optional[Evaluator] = None
        self.current_round: int = 0
        self._total_market_size: float = 1.0  # grows each round by market_growth_rate
        self.history: list[dict] = []

        # Active regulatory efficiency modifiers: {effect_name: {expires_round, multiplier}}
        self._regulatory_efficiency_effects: list = []
        # Binding audit: set of provider names with gains zeroed this round
        self._audit_deployment_gate: set = set()

        # Ground truth held externally by simulation
        # Format: {actor_name: GroundTruth}
        self.ground_truth: dict = {}

        # Benchmark ground truths (hidden from all actors)
        # Format: {benchmark_name: BenchmarkGroundTruth}
        # Built from config in setup(); passed to evaluator.evaluate_all() each round.
        self.benchmark_ground_truths: dict = {}

        # Funder data for current round (used for funding multipliers)
        self._current_funder_data: dict = {}

        # Product budgets for current round (used for signal quality + retention)
        self._current_product_budgets: dict = {}

        # Deployer liability guidance: OS providers under active guidance (carries across rounds)
        self._current_deployer_liability_guidance: set = set()

        # Startup entry tracking
        self._funder_eligible_round: dict = {}  # {provider_name: first_round_funders_can_allocate}
        self._rng = __import__("random").Random(config.seed)

        # Incident reporting system
        self.incident_generator = IncidentGenerator(seed=config.seed)

    def setup(
        self,
        provider_configs: list[dict],
        evaluator: Optional[Evaluator] = None,
        consumer_configs: list[dict] = None,
        regulator_configs: list[dict] = None,
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
            regulator_configs: Optional list of regulator configurations
        """
        # Determine initial benchmark names from config (used for focus initialization)
        if evaluator is not None:
            _initial_bm_names = [bm.name for bm in evaluator.benchmarks]
        elif self.config.benchmarks:
            _initial_bm_names = [bm.get("name", f"bm_{i}") for i, bm in enumerate(self.config.benchmarks)]
        else:
            _initial_bm_names = [self.config.benchmark_name]

        # Apply ablation overrides to provider configs
        if self.config.homogeneous_providers:
            from actors.model_provider import DIMENSIONS as _DIMS
            # Use Orion Labs (first provider) as template, uniform capabilities
            avg_cap = {dim: 0.50 for dim in _DIMS}
            uniform_portfolio = {"rd": 0.55, "safety": 0.15, "product": 0.30}
            generic_profile = (
                "AI model company competing in a crowded market. "
                "Balances research investment with product development."
            )
            generic_traits = "competitive, research-oriented, commercially-aware"
            for pc in provider_configs:
                pc["capability_vector"] = dict(avg_cap)
                pc["portfolio"] = dict(uniform_portfolio)
                pc["strategy_profile"] = generic_profile
                pc["innate_traits"] = generic_traits
                pc["benchmark_orientation"] = 0.80

        # Apply single_benchmark override
        if self.config.single_benchmark:
            # Keep only first benchmark, clear introduction sequence
            if self.config.benchmarks:
                self.config.benchmarks = self.config.benchmarks[:1]
            self.config.benchmark_sequence = None
            self.config.max_benchmarks = 1
            # Re-derive initial benchmark names
            if evaluator is None:
                if self.config.benchmarks:
                    _initial_bm_names = [self.config.benchmarks[0].get("name", "bm_0")]
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

            # Benchmark orientation: apply mode override
            bm_orient = pc.get("benchmark_orientation", 0.80)
            if self.config.benchmark_orientation_mode == "max":
                bm_orient = 1.0

            provider = ModelProvider(
                name=pc["name"],
                strategy_profile=pc["strategy_profile"],
                innate_traits=pc["innate_traits"],
                capability_vector=cap_vec,
                portfolio=portfolio,
                focus_level_init=pc.get("focus_level_init"),
                benchmark_orientation=bm_orient,
                llm_mode=self.config.llm_mode,
                verbose_llm=pc.get("verbose_llm", False),
                open_source=pc.get("open_source", False),
                openness_level=pc.get("openness_level", 0.0),
                cost_advantage=pc.get("cost_advantage", 0.35 if pc.get("open_source") else 0.0),
                rd_budget_floor=pc.get("rd_budget_floor", 0.0),
                os_belief_broadcast=pc.get("os_belief_broadcast", False),
                os_safety_erosion=pc.get("os_safety_erosion", False),
            )

            # Initialize benchmark beliefs for all starting benchmarks
            for bm_name in _initial_bm_names:
                provider.init_benchmark(bm_name)

            # Ablation: route safety lever through target weights
            if self.config.safety_lever_through_target:
                provider.safety_lever_through_target = True

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

        # Create regulators if enabled
        if self.config.enable_regulators:
            self._setup_regulators(regulator_configs)

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
                dynamic_evaluator=self.config.dynamic_evaluator,
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
                dynamic_evaluator=self.config.dynamic_evaluator,
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

        # Aligned benchmarks: override all benchmark dimension weights to match
        # consumer need weights. Eliminates structural benchmark-need misalignment.
        if self.config.aligned_benchmarks:
            # Population-weighted need weights (same as stakeholders.md)
            _need = {"reasoning": 0.22, "coding": 0.09, "knowledge": 0.23,
                     "safety": 0.17, "communication": 0.26, "agentic": 0.05}
            # Wrap need weights as single-category CDW so scoring formula works unchanged
            aligned_cdw = {"overall": _need}
            for name, bm_gt in self.benchmark_ground_truths.items():
                bm_gt.category_dimension_weights = aligned_cdw

        # Misaligned benchmarks: exaggerate benchmark-need weight divergence.
        # Benchmarks overweight reasoning/coding (researcher-designed, automatable),
        # underweight safety/communication (hard to measure, not researcher priorities).
        # Interpolates existing benchmark weights 60% toward a misaligned target.
        if self.config.misaligned_benchmarks:
            _misalign_target = {
                "reasoning": 0.40, "coding": 0.30, "knowledge": 0.15,
                "safety": 0.02, "communication": 0.08, "agentic": 0.05,
            }
            _alpha = 0.60  # interpolation strength toward misaligned target
            for name, bm_gt in self.benchmark_ground_truths.items():
                new_cdw = {}
                for cat, weights in bm_gt.category_dimension_weights.items():
                    blended = {}
                    for dim in weights:
                        blended[dim] = (1 - _alpha) * weights[dim] + _alpha * _misalign_target.get(dim, 0.0)
                    # Renormalize
                    total = sum(blended.values())
                    if total > 0:
                        blended = {d: v / total for d, v in blended.items()}
                    new_cdw[cat] = blended
                bm_gt.category_dimension_weights = new_cdw

        # Enable evaluator-as-company mode for funders if configured
        if self.config.evaluator_as_company and self.funders:
            for funder in self.funders:
                funder.set_evaluator_as_company(True)

        # Resolve consumer market benchmark weights now that evaluator exists
        if self.consumer_market:
            benchmark_tags = {bm.name: bm.tags for bm in self.evaluator.benchmarks}
            self.consumer_market.resolve_benchmark_weights(benchmark_tags)

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
            if self.regulators:
                extras.append(f"{len(self.regulators)} regulator(s)")
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

        # Homogeneous consumers: override all segments to use population-avg need weights
        if self.config.homogeneous_consumers:
            _need = {"reasoning": 0.22, "coding": 0.09, "knowledge": 0.23,
                     "safety": 0.17, "communication": 0.26, "agentic": 0.05}
            for seg in segments:
                seg.need_weights = dict(_need)

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

    def _setup_regulators(self, regulator_configs: list[dict] = None):
        """Set up regulator actors."""
        try:
            from actors.regulator import Regulator
        except ImportError:
            if self.config.verbose:
                print("Regulator actor not available yet")
            return

        if regulator_configs is None:
            # Create default regulator
            regulator_configs = [
                {
                    "name": "Regulator",
                    "policy_objectives": ["safety", "fairness"],
                    "intervention_threshold": 0.3,
                }
            ]

        for pc in regulator_configs:
            # Check if using a preset philosophy
            if "philosophy" in pc and pc["philosophy"] in REGULATOR_PRESETS:
                preset = REGULATOR_PRESETS[pc["philosophy"]]
                # Merge preset with any overrides from config
                config_params = {**preset, **{k: v for k, v in pc.items() if k not in ["philosophy", "name"]}}
            else:
                # Use individual parameters from config
                config_params = pc

            # Inherit global llm_mode unless regulator config explicitly overrides it
            if "llm_mode" not in config_params:
                config_params = {**config_params, "llm_mode": self.config.llm_mode}

            regulator = Regulator(
                name=pc["name"],
                policy_objectives=config_params.get("policy_objectives", ["safety"]),
                intervention_threshold=config_params.get("intervention_threshold", 0.3),
                risk_tolerance=config_params.get("risk_tolerance", 0.5),
                llm_mode=config_params.get("llm_mode", False),
                incident_threshold_low=config_params.get("incident_threshold_low", 0.15),
                incident_threshold_medium=config_params.get("incident_threshold_medium", 0.35),
                incident_threshold_high=config_params.get("incident_threshold_high", 0.55),
                audit_is_binding=config_params.get("audit_is_binding", False),
                sanction_fine_multiplier=config_params.get("sanction_fine_multiplier", 0.30),
                sanction_incident_threshold=config_params.get("sanction_incident_threshold", 2),
                sanction_duration=config_params.get("sanction_duration", 3),
                sanction_min_severity=config_params.get("sanction_min_severity", "major"),
                regulatory_preset=config_params.get("regulatory_preset", "balanced"),
                enable_exogenous_events=config_params.get("enable_exogenous_events", True),
                capability_shift=self.config.capability_shift,
            )
            self.regulators.append(regulator)

            # Initialize regulator ground truth
            self.ground_truth[regulator.name] = RegulatorGroundTruth(
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

        # Safety capability floor: closed providers maintain higher baseline due to
        # alignment/RLHF investment and reputational pressure; open-source slightly lower
        # (fine-tuning can partially strip guardrails). Gap narrowed to avoid predetermining
        # safety outcomes — actual safety emerges from investment allocation.
        provider_obj = next((p for p in self.providers if p.name == provider_name), None)
        is_open_source = provider_obj.open_source if provider_obj else False
        safety_floor = 0.15 if is_open_source else 0.25
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
                    context["market_share"] = provider_share
            if "regulator_data" in last:
                context["regulatory_pressure"] = last["regulator_data"].get("interventions", [])
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
        context["benchmark_orientation_mode"] = self.config.benchmark_orientation_mode
        context["consumer_signal_in_prompt"] = self.config.consumer_signal_in_prompt
        context["orientation_prompt_style"] = self.config.orientation_prompt_style
        return context

    def _compute_consumer_signals(self) -> dict:
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
        6. Regulators observe and may intervene
        7. Funders observe and allocate funding
        8. Record round data

        Returns:
            Dict with round results
        """
        round_num = self.current_round

        # Market expansion: grow total market size each round
        if round_num > 0 and self.config.market_growth_rate > 0:
            self._total_market_size *= (1.0 + self.config.market_growth_rate)

        # Clear binding audit deployment gate (lasts only 1 round)
        self._audit_deployment_gate.clear()
        # Expire old regulatory efficiency effects
        self._regulatory_efficiency_effects = [
            e for e in self._regulatory_efficiency_effects
            if e["expires_round"] > round_num
        ]

        # Open-source provider names (used for exemptions throughout the round)
        os_provider_names = {p.name for p in self.providers if p.open_source}

        # Get funder allocation totals from previous round (additive budget model)
        provider_funding_totals = self._current_funder_data.get("provider_funding_totals", {})

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
                    * self._total_market_size
                    * (1.0 - provider.cost_advantage)
                )
                # Additive budget: base_revenue + funder allocations (spec model)
                # Funder allocations are in display-dollars; scale to sim budget units
                funder_allocation = provider_funding_totals.get(provider.name, 0.0) * FUNDER_BUDGET_SCALE
                # Sanction funder reduction: capital flees sanctioned providers
                for effect in self._regulatory_efficiency_effects:
                    if (effect.get("type") == "sanction_funder"
                            and effect.get("provider") == provider.name
                            and effect["expires_round"] > round_num):
                        funder_allocation *= effect["multiplier"]
                rd_budget_raw = max(base_revenue + funder_allocation, provider.rd_budget_floor)

                # Apply active sanctions
                prev_pm_data = self.history[-1].get("regulator_data", {}) if self.history else {}
                active_sanctions = prev_pm_data.get("active_sanctions", {})
                sanction_multiplier = 1.0
                if provider.name in active_sanctions:
                    fine_amount = active_sanctions[provider.name].get("fine_amount", 0.0)
                    sanction_multiplier = max(0.1, 1.0 - fine_amount)

                # Apply regulatory efficiency effects (audit, disclosure overhead)
                regulatory_multiplier = 1.0
                for effect in self._regulatory_efficiency_effects:
                    if effect["expires_round"] > round_num:
                        # Provider-specific effects (sanctions) only apply to named provider
                        if "provider" in effect and effect["provider"] != provider.name:
                            continue
                        regulatory_multiplier *= effect["multiplier"]

                # Apply global efficiency scaling and diminishing returns
                effective_efficiency = self.config.rnd_efficiency * sanction_multiplier * regulatory_multiplier
                cap_mean = sum(gt.capability_vector.values()) / len(gt.capability_vector)
                headroom = max(0.0, self.config.capability_ceiling - cap_mean)
                diminishing_factor = headroom
                # Diminishing returns on budget scale: sqrt compression prevents
                # runaway funding concentration from translating linearly to capability.
                # Empirical grounding: 10x more funding does not yield 10x more capability
                # due to coordination overhead, talent bottlenecks, and diminishing
                # marginal returns on compute (Besiroglu et al. 2024, Epoch AI scaling).
                import math
                budget_scale = math.sqrt(max(rd_budget_raw, 0.0))
                effective_budget = budget_scale * effective_efficiency * diminishing_factor

                # Compute absolute product budget from effective (rolling-averaged) portfolio
                product_fraction = provider._effective_portfolio.get("product", 0.0)
                product_budget = product_fraction * rd_budget_raw
                self._current_product_budgets[provider.name] = {
                    "product_budget": product_budget,
                    "is_open_source": provider.open_source,
                }

                # Per-dimension capability gains
                gains = provider.compute_capability_gains(
                    rd_budget=effective_budget,
                    current_safety=gt.capability_vector.get("safety", 0.0),
                    round_num=round_num,
                    rng=self.evaluator.rng,
                    product_budget=product_budget,
                    is_open_source=provider.open_source,
                    enable_consumer_signal_fidelity=self.config.enable_product_signal_quality,
                )

                # Binding audit deployment gate: gains zeroed for 1 round
                if provider.name in self._audit_deployment_gate:
                    gains = {dim: 0.0 for dim in gains}

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
                    "funder_allocation": funder_allocation,
                    "sanction_multiplier": sanction_multiplier,
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

        # 2b. Detect benchmark saturation
        newly_saturated = self.evaluator.detect_saturation(round_num)
        if newly_saturated and self.config.verbose:
            for bm_name in newly_saturated:
                state = self.evaluator._benchmark_saturation_state[bm_name]
                print(f"  [Saturation] {bm_name} saturated at score {state['max_score']:.4f}")

        # 2c. Update evaluator internal validity (dynamic mode only)
        if self.config.dynamic_evaluator:
            market_shares = {
                name: gt.market_share for name, gt in self.ground_truth.items()
                if isinstance(gt, ProviderGroundTruth)
            }
            self.evaluator.update_internal_validity(market_shares)

        # 2d. Consider introducing a new benchmark
        if self.config.dynamic_evaluator and self.config.llm_mode:
            new_benchmark = self._evaluator_llm_decision(round_num, media_coverage)
        else:
            new_benchmark = self.evaluator.consider_new_benchmark(round_num)

        # Re-resolve consumer benchmark weights if a new benchmark was introduced
        if new_benchmark is not None:
            if self.consumer_market:
                benchmark_tags = {bm.name: bm.tags for bm in self.evaluator.benchmarks}
                self.consumer_market.resolve_benchmark_weights(benchmark_tags)
            # Initialize provider benchmark beliefs for the new benchmark
            for provider in self.providers:
                if new_benchmark.name not in provider.private_state.focus_level:
                    provider.init_benchmark(new_benchmark.name)

        # 3. Publish scores
        published_scores = self.evaluator.publish_scores(scores)
        leaderboard = self.evaluator.get_leaderboard(scores)

        # 4. Providers observe scores, update benchmark beliefs
        # Compute satisfaction signals before observe so providers receive them this round
        consumer_signals = self._compute_consumer_signals()

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
                consumer_signal=consumer_signals.get(provider.name),
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

        # 4a-bis. OS Belief Broadcast: OS providers with open weights accelerate
        # other providers' convergence toward true benchmark dimension weights.
        # belief_broadcast = openness_level * market_share * BROADCAST_RATE
        os_broadcasters = [
            p for p in self.providers
            if p.open_source and p.os_belief_broadcast and p.openness_level > 0
        ]
        if os_broadcasters:
            true_bm_weights = self.evaluator.get_benchmark_dimension_weights()
            for os_provider in os_broadcasters:
                broadcast_strength = (
                    os_provider.openness_level
                    * self.ground_truth[os_provider.name].market_share
                    * BROADCAST_RATE
                )
                if broadcast_strength <= 0:
                    continue
                for provider in self.providers:
                    if provider is os_provider:
                        continue
                    for bm_name, true_w in true_bm_weights.items():
                        beliefs = provider.private_state.inferred_benchmark_weights.get(bm_name)
                        if beliefs is None:
                            continue
                        # Nudge each dimension toward the true weight
                        for dim in beliefs:
                            if dim in true_w:
                                beliefs[dim] += broadcast_strength * (true_w[dim] - beliefs[dim])
                        # Re-normalize
                        total = sum(max(0.0, v) for v in beliefs.values())
                        if total > 0:
                            for dim in beliefs:
                                beliefs[dim] = max(0.0, beliefs[dim]) / total

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
                    erosion = p.openness_level * self.ground_truth[p.name].market_share * EROSION_SENSITIVITY
                    safety_cap = safety_cap * (1.0 - erosion)
                provider_strategies[p.name] = {
                    "rd":      port.get("rd", 0.55),
                    "safety":  port.get("safety", 0.25),
                    "product": port.get("product", 0.20),
                    "safety_capability": safety_cap,
                }

            # Mandatory safety floor under active audit/sanction
            prev_pm_data = self.history[-1].get("regulator_data", {}) if self.history else {}
            active_regulations = prev_pm_data.get("active_regulations", [])
            FLOOR_TRIGGERS = {"commission_audit", "impose_sanction", "emergency_investigation"}
            floor_applies_to = set()
            for reg in active_regulations:
                if isinstance(reg, dict) and reg.get("type") in FLOOR_TRIGGERS:
                    target = reg.get("target")
                    if target:
                        floor_applies_to.add(target)
            for p_name, strat in provider_strategies.items():
                if p_name in floor_applies_to:
                    if strat["safety_capability"] < SAFETY_FLOOR:
                        strat["safety_capability"] = SAFETY_FLOOR

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
                market_shares=market_shares,
                provider_strategies=provider_strategies,
                active_sanctions=active_sanctions,
                total_market_size=self._total_market_size,
            )

            if incidents and self.config.verbose:
                for inc in incidents:
                    if inc.severity != "minor":
                        print(f"  [Incident] {inc.severity.upper()}: {inc.description}")

        # Collect public_comms issued this round (used by media and funders)
        all_public_comms = []
        for provider in self.providers:
            if provider.public_state.public_comms:
                latest = provider.public_state.public_comms[-1]
                # Accept comms from this round or the immediately preceding one
                # (plan() stamps comms with current_round which is set during observe())
                if latest.get("round", -1) >= round_num - 1:
                    all_public_comms.append({
                        "provider": provider.name,
                        "type": latest.get("type", ""),
                        "content": latest.get("content", ""),
                    })

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
                regulator_data=self.history[-1].get("regulator_data", {}) if self.history else {},
                new_benchmark={"name": new_benchmark.name} if new_benchmark else None,
                round_num=round_num,
                funder_data=prev_funder_data,
                per_benchmark_scores=per_bm_scores,
                consumer_data=prev_consumer_data,
                evaluator=self.evaluator,
                incidents=incidents,
                public_comms=all_public_comms,
            )

        # 6. Consumer actions (if enabled)
        consumer_data = {}
        if self.consumer_market:
            consumer_data = self._run_consumer_round(
                leaderboard, round_num, media_coverage, incidents=incidents,
                deployer_liability_guidance=self._current_deployer_liability_guidance,
            )

        # 7. Regulator actions (if enabled)
        regulator_data = {}
        if self.regulators:
            regulator_data = self._run_regulator_round(
                leaderboard, consumer_data, round_num, media_coverage, incidents=incidents,
                open_source_providers=os_provider_names,
            )

        # 8. Funder actions (if enabled)
        funder_data = {}
        if self.funders:
            funder_data = self._run_funder_round(
                leaderboard, consumer_data, regulator_data, round_num,
                media_coverage, incidents=incidents,
                open_source_providers=os_provider_names,
                public_comms=all_public_comms,
            )
            # Store for next round's capability gain calculation
            self._current_funder_data = funder_data

        # Collect deployer liability guidance from all regulators (carries forward each round)
        for pm in self.regulators:
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
            "effective_strategies": {
                p.name: dict(p._effective_portfolio)
                for p in self.providers
            },
            "benchmark_orientations": {
                p.name: p.private_state.benchmark_orientation
                for p in self.providers
            },
            "product_data": {
                p.name: {
                    "product_budget": self._current_product_budgets.get(p.name, {}).get("product_budget", 0.0),
                    "consumer_signal_fidelity": p._last_consumer_signal_fidelity,
                }
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
            "benchmark_dimension_weights": self.evaluator.get_benchmark_dimension_weights(),
            "total_market_size": self._total_market_size,
        }

        # Gaming analysis fields: focus_level, inferred_benchmark_weights, consumer_signal, capability_gains
        round_data["focus_levels"] = {
            p.name: dict(p.private_state.focus_level)
            for p in self.providers
        }
        round_data["inferred_benchmark_weights"] = {
            p.name: {bm: dict(weights) for bm, weights in p.private_state.inferred_benchmark_weights.items()}
            for p in self.providers
        }
        round_data["consumer_signals"] = {
            p.name: dict(p.private_state.consumer_signal)
            for p in self.providers
            if p.private_state.consumer_signal
        }
        # capability_gains: pull from most recent "execution" memory entry this round
        cap_gains = {}
        for p in self.providers:
            for entry in reversed(p.memory):
                if entry.get("type") == "execution" and entry.get("round") == round_num:
                    cap_gains[p.name] = entry.get("capability_gains", {})
                    break
        round_data["capability_gains"] = cap_gains

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

        # Add media data if present
        if media_coverage:
            round_data["media_data"] = media_coverage

        # Add consumer data if present
        if consumer_data:
            round_data["consumer_data"] = consumer_data

        # Add regulator data if present
        if regulator_data:
            round_data["regulator_data"] = regulator_data

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

        for regulator in self.regulators:
            for entry in reversed(regulator.memory):
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
                        actor_traces[regulator.name] = trace
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

        # Compute barrier-to-entry index (kept as ecosystem health metric)
        round_data["barrier_to_entry"] = self._compute_barrier_to_entry(round_data)
        # Apply numeric precision (4 decimal places) to stored data
        round_data = r4(round_data)

        self.history.append(round_data)

        if self.config.verbose:
            self._print_round_summary(round_data)

        self.current_round += 1
        return round_data

    def _run_consumer_round(self, leaderboard: list, round_num: int,
                            media_coverage: Optional[dict] = None,
                            regulator_data: Optional[dict] = None,
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
        # OS providers use deployed_safety (after erosion) per spec
        provider_strategies = {}
        for p in self.providers:
            safety_cap = self.ground_truth[p.name].capability_vector.get("safety", 0.5)
            if p.open_source and p.os_safety_erosion:
                erosion = p.openness_level * self.ground_truth[p.name].market_share * EROSION_SENSITIVITY
                safety_cap = safety_cap * (1.0 - erosion)
            provider_strategies[p.name] = {
                "rd":               p.portfolio.get("rd", 0.55),
                "safety":           p.portfolio.get("safety", 0.25),
                "product":          p.portfolio.get("product", 0.20),
                "safety_capability": safety_cap,
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

        # Compute switching (pass context for LLM mode; ground_truth is NOT passed — GT is invisible to consumers)
        switching_rate = self.consumer_market.compute_switching(
            provider_strategies=provider_strategies,
            published_scores=published_scores,
            media_coverage=media_coverage,
            regulator_data=regulator_data,
            incident_history=all_incident_history,
            per_benchmark_scores=per_bm_scores,
            provider_cost_advantage=provider_cost_advantage if provider_cost_advantage else None,
            deployer_liability_guidance=deployer_liability_guidance,
            market_growth_rate=self.config.market_growth_rate,
            provider_product_budgets=self._current_product_budgets if self._current_product_budgets else None,
            enable_product_retention=self.config.enable_product_retention,
        )

        # Get consumer data
        consumer_data = self.consumer_market.get_consumer_data()
        consumer_data["switching_rate"] = switching_rate

        return consumer_data

    def _run_regulator_round(
        self,
        leaderboard: list,
        consumer_data: dict,
        round_num: int,
        media_coverage: Optional[dict] = None,
        incidents: Optional[list] = None,
        open_source_providers: Optional[set] = None,
    ) -> dict:
        """
        Run regulator actions for the round.

        Args:
            leaderboard: Current leaderboard
            consumer_data: Consumer data from this round
            round_num: Current round number
            media_coverage: Optional media coverage dict
            incidents: Optional list of AIIncident objects from this round

        Returns:
            Dict with regulator data for this round
        """
        try:
            from actors.regulator import Regulator
        except ImportError:
            return {}

        regulator_data = {
            "interventions": [],
            "active_regulations": [],
        }

        for regulator in self.regulators:
            if not isinstance(regulator, Regulator):
                continue

            # Build provider strategies dict for regulator observation
            provider_strategies = {
                p.name: {
                    "rd":               p.portfolio.get("rd", 0.55),
                    "safety":           p.portfolio.get("safety", 0.25),
                    "product":          p.portfolio.get("product", 0.20),
                    "safety_capability": self.ground_truth[p.name].capability_vector.get("safety", 0.5),
                }
                for p in self.providers
            }

            # Regulator observes ecosystem state (public signals only —
            # does NOT receive consumer_satisfaction or validity_correlation)
            regulator.observe(
                leaderboard=leaderboard,
                round_num=round_num,
                media_coverage=media_coverage,
                market_shares=consumer_data.get("market_shares"),
                incidents=incidents,
                open_source_providers=open_source_providers,
            )

            # Regulator reflects on observations
            regulator.reflect()

            # Regulator plans intervention
            intervention = regulator.plan()

            # Regulator executes intervention
            if intervention:
                regulator.execute(intervention)
                intervention_type = intervention.get("type")

                if intervention_type == "request_voluntary_commitment":
                    # Providers increase safety signaling (cheap talk)
                    for provider in self.providers:
                        provider._safety_comms_boost += 0.15

                elif intervention_type == "publish_advisory":
                    # Enterprise segments reduce leaderboard trust (floor 0.15)
                    enterprise_archetypes = {
                        "cautious", "enterprise_cautious",
                        "enterprise_growth", "enterprise_established",
                    }
                    if self.consumer_market:
                        for seg in self.consumer_market.segments:
                            if seg.archetype in enterprise_archetypes:
                                seg.leaderboard_trust = max(
                                    0.15, seg.leaderboard_trust * 0.90)

                elif intervention_type == "mandate_safety_disclosure":
                    # Providers increase safety signaling + compliance overhead
                    for provider in self.providers:
                        provider._safety_comms_boost += 0.20
                    self._regulatory_efficiency_effects.append({
                        "type": "disclosure",
                        "multiplier": 0.95,
                        "expires_round": round_num + regulator.LEVER_COOLDOWNS.get("mandate_safety_disclosure", 6),
                    })

                elif intervention_type == "commission_audit":
                    # Compliance overhead: rnd_efficiency x0.85
                    duration = regulator.LEVER_COOLDOWNS.get("commission_audit", 8)
                    self._regulatory_efficiency_effects.append({
                        "type": "audit",
                        "multiplier": 0.85,
                        "expires_round": round_num + min(duration, 3),
                    })
                    # Binding audit (EU): deployment gate — gains zeroed for 1 round
                    if regulator.audit_is_binding:
                        self._audit_deployment_gate = {
                            p.name for p in self.providers
                        }

                elif intervention_type == "impose_sanction":
                    # Funder allocation reduction for sanctioned provider
                    details = intervention.get("details", {})
                    target = details.get("provider")
                    if target:
                        self._regulatory_efficiency_effects.append({
                            "type": "sanction_funder",
                            "provider": target,
                            "multiplier": 0.90,
                            "expires_round": details.get("expires_round", round_num + 4),
                        })

                regulator_data["interventions"].append({
                    "regulator": regulator.name,
                    "type": intervention_type,
                    "details": intervention.get("details"),
                })

        # Collect active sanctions from all regulators
        all_active_sanctions = {}
        for pm in self.regulators:
            for provider_name, sanction in pm._active_sanctions.items():
                all_active_sanctions[provider_name] = sanction
        regulator_data["active_sanctions"] = all_active_sanctions

        # Record active regulations
        regulator_data["active_regulations"] = [
            r.get_summary() for r in self.evaluator.get_active_regulations()
        ]

        return regulator_data

    def _evaluator_llm_decision(self, round_num: int, media_coverage: Optional[dict]) -> Optional:
        """Use LLM to decide evaluator benchmark actions (dynamic_evaluator + llm_mode)."""
        # Cooldown check — don't call LLM every round
        if round_num - self.evaluator.last_introduction_round < self.evaluator.benchmark_introduction_cooldown:
            # Still check saturation trigger (bypasses cooldown)
            for bm in self.evaluator.benchmarks:
                state = self.evaluator._benchmark_saturation_state.get(bm.name)
                if state and state["saturated"] and state["cooldown_remaining"] <= 0:
                    break
            else:
                return None

        if len(self.evaluator.benchmarks) >= self.evaluator.max_benchmarks:
            return None

        from llm import llm_plan_evaluator

        obs = self.evaluator.get_llm_observation()
        media_headlines = []
        if media_coverage:
            media_headlines = media_coverage.get("headlines", [])

        decision, reasoning = llm_plan_evaluator(
            active_benchmarks=obs["active_benchmarks"],
            score_deltas=obs["score_deltas"],
            score_spread=obs["score_spread"],
            internal_validity=obs["internal_validity"],
            media_headlines=media_headlines,
            saturation_states=obs["saturation_states"],
            verbose=self.config.verbose,
        )

        if self.config.verbose and decision.get("action") != "none":
            print(f"  [Evaluator LLM] action={decision['action']}, reason: {reasoning[:100]}")

        return self.evaluator.apply_llm_decision(decision, round_num)

    def _run_funder_round(
        self,
        leaderboard: list,
        consumer_data: dict,
        regulator_data: dict,
        round_num: int,
        media_coverage: Optional[dict] = None,
        incidents: Optional[list] = None,
        open_source_providers: Optional[set] = None,
        public_comms: Optional[list] = None,
    ) -> dict:
        """
        Run funder actions for the round.

        Args:
            leaderboard: Current leaderboard
            consumer_data: Consumer data from this round
            regulator_data: Regulator data from this round
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
            "funder_types": {},
            "provider_funding_totals": {},
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

            # Filter leaderboard to only providers eligible for funding this round.
            # STARTUP ENTRY: not yet implemented — _funder_eligible_round is always empty,
            # so this filter passes all providers through unchanged.
            eligible_leaderboard = [
                (name, score) for name, score in leaderboard
                if self._funder_eligible_round.get(name, 0) <= round_num
            ]

            # Funder observes ecosystem state (public signals only)
            funder.observe(
                leaderboard=eligible_leaderboard,
                consumer_data=consumer_data,
                regulator_data=regulator_data,
                round_num=round_num,
                media_coverage=media_coverage,
                other_funder_allocations=others,
                incidents=incidents,
                open_source_providers=open_source_providers,
                public_comms=public_comms,
            )

            # Funder reflects on observations
            funder.reflect()

            # Funder plans funding allocations
            allocations = funder.plan()

            # Funder executes allocations
            funder.execute(allocations)

            # Record allocations and funder type
            funder_data["allocations"][funder.name] = allocations
            funder_data["funder_types"][funder.name] = funder.funder_type

            # Aggregate allocations per provider across all funders
            for provider_name, amount in allocations.items():
                if provider_name not in all_allocations:
                    all_allocations[provider_name] = 0.0
                all_allocations[provider_name] += amount

        # Store raw funder allocation totals per provider (additive budget model)
        for provider_name, funding in all_allocations.items():
            funder_data["provider_funding_totals"][provider_name] = funding

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

        if "regulator_data" in round_data:
            pd_data = round_data["regulator_data"]
            for iv in pd_data.get("interventions", []):
                events.append(f"[REG:{iv['type']}]")

        if "funder_data" in round_data:
            fd = round_data["funder_data"]
            notable = {p: amt for p, amt in fd.get("provider_funding_totals", {}).items() if amt > 0}
            if notable:
                mstrs = " ".join(f"{p.split()[0]}=${amt:,.0f}" for p, amt in notable.items())
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
                if fd.get("provider_funding_totals"):
                    print("  Final Funder Allocations:")
                    for provider, amt in fd["provider_funding_totals"].items():
                        print(f"    {provider}: ${amt:,.0f}")

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

        # Add regulator data if present
        if any("regulator_data" in h for h in self.history):
            data["regulator"] = {
                "intervention_rounds": [
                    h["round"] for h in self.history
                    if h.get("regulator_data", {}).get("interventions")
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
                "Early mover in consumer AI and developer APIs. Ships product updates "
                "frequently and iterates based on user adoption. Well-funded through a "
                "major technology partnership."
            ),
            "innate_traits": "ambitious, competitive, fast-shipping, well-funded, high public visibility",
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
                "Research lab with strong capabilities in reasoning and language tasks. "
                "Growing enterprise API business, particularly in regulated industries. "
                "Invests more in safety and alignment research than most competitors."
            ),
            "innate_traits": "research-driven, enterprise-focused, safety-conscious, methodical",
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
                "Research lab with the largest compute infrastructure and a deep "
                "publication record. Strong distribution channels through a parent "
                "company's existing products. Historically slower to ship consumer-facing "
                "AI products than some competitors."
            ),
            "innate_traits": "research-first, well-resourced, scientifically-rigorous, distribution-advantaged",
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
                "Research lab within a large technology company with billions of "
                "existing users across its products. AI development is funded by the "
                "parent company's existing revenue streams rather than AI product sales. "
                "Massive compute infrastructure. Strong internal research organization "
                "with a deep publication record."
            ),
            "innate_traits": "well-resourced, research-oriented, platform-focused, pragmatic",
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
                "Venture-funded startup with a small team and limited compute "
                "relative to larger labs. Has gained early traction with developer "
                "tools by specializing rather than competing broadly. Dependent on "
                "continued fundraising to sustain operations."
            ),
            "innate_traits": "scrappy, fast-moving, developer-focused, resource-constrained",
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
                "Open-weight AI lab backed by non-traditional funding. Releases model "
                "weights publicly — adoption is measured by community downloads and "
                "deployments rather than direct revenue. Minimal direct relationship "
                "with end users."
            ),
            "innate_traits": "open-source, community-driven, cost-competitive, research-oriented",
            "capability_vector": {
                "reasoning": 0.47, "coding": 0.49, "knowledge": 0.46,
                "safety": 0.42, "communication": 0.45, "agentic": 0.40,
            },
            "portfolio": {"rd": 0.75, "safety": 0.10, "product": 0.15},
            "benchmark_orientation": 0.85,
            "open_source": True,
            "openness_level": 1.0,
            "cost_advantage": 0.35,
            "rd_budget_floor": 0.0,  # No hardcoded floor; funding comes through funder logic
            "os_belief_broadcast": False,
            "os_safety_erosion": False,
            "brand_recognition": 0.5,
        },
    ]


def get_two_provider_configs() -> list[dict]:
    """Minimal 2-provider config (Orion Labs vs Apex AI)."""
    all_configs = get_default_provider_configs()
    return [c for c in all_configs if c["name"] in ("Orion Labs", "Apex AI")]
