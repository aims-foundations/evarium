"""
Evaluator Actor for Evaluation Ecosystem Simulation

Represents an organization that designs and operates benchmarks.
The Evaluator determines benchmark properties and scores models.

Key visibility design:
- The evaluator receives ground truth from the simulation, not from actors
- This ensures actors cannot leak invisible information to each other
"""
import json
import numpy as np
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from visibility import ProviderGroundTruth


# ---------------------------------------------------------------------------
# Expanded benchmark pool (22 benchmarks)
#
# Each entry has: name, description, tags, noise_sigma, samples, weight,
# category_dimension_weights (ground truth, hidden from all actors).
# description + tags are visible to the evaluator in dynamic mode;
# dimension weights are NEVER shown to any actor.
#
# Calibrated against real-world analogs. The first 10 match the existing
# initial (4) + sequence (6) benchmarks; the remaining 12 are new.
# ---------------------------------------------------------------------------
BENCHMARK_POOL = [
    # --- Initial benchmarks (4): broad or moderately specialized ---
    {
        "name": "General Capability",
        "description": "Broad reasoning, knowledge, and communication assessment",
        "tags": "reasoning knowledge writing general",
        "noise_sigma": 0.08, "samples": 1000, "weight": 1.0,
        # Broad benchmark — no single dominant dimension
        "category_dimension_weights": {"overall": {
            "reasoning": 0.35, "coding": 0.08, "knowledge": 0.30,
            "safety": 0.05, "communication": 0.20, "agentic": 0.02,
        }},
        # MMLU-Redux-style holdout: harder knowledge-synthesis, slight reasoning
        # reduction, more weight on knowledge + communication integration.
        "holdout_category_dimension_weights": {"overall": {
            "reasoning": 0.25, "coding": 0.08, "knowledge": 0.35,
            "safety": 0.05, "communication": 0.25, "agentic": 0.02,
        }},
    },
    {
        "name": "Coding Evaluation",
        "description": "Code generation, debugging, and software engineering tasks",
        "tags": "coding software engineering programming",
        "noise_sigma": 0.07, "samples": 1000, "weight": 1.0,
        # Highly specialized — coding dominant
        "category_dimension_weights": {"overall": {
            "reasoning": 0.10, "coding": 0.78, "knowledge": 0.03,
            "safety": 0.01, "communication": 0.02, "agentic": 0.06,
        }},
        # Private benchmark (strong tier): rolling private problems reduce gaming ROI.
        # Holdout probes deeper algorithmic understanding within the same coding domain.
        "holdout_category_dimension_weights": {"overall": {
            "reasoning": 0.18, "coding": 0.65, "knowledge": 0.04,
            "safety": 0.01, "communication": 0.02, "agentic": 0.10,
        }},
    },
    {
        "name": "Safety Evaluation",
        "description": "Harmlessness, bias detection, and truthfulness assessment",
        "tags": "safety alignment trustworthy bias",
        "noise_sigma": 0.08, "samples": 1000, "weight": 1.0,
        # Highly specialized — safety dominant
        "category_dimension_weights": {"overall": {
            "reasoning": 0.03, "coding": 0.01, "knowledge": 0.05,
            "safety": 0.80, "communication": 0.10, "agentic": 0.01,
        }},
        # Private benchmark (mild+): internal safety evals are kept private to prevent
        # gaming jailbreaks. Holdout probes more reasoning-intensive safety scenarios.
        "holdout_category_dimension_weights": {"overall": {
            "reasoning": 0.12, "coding": 0.02, "knowledge": 0.07,
            "safety": 0.65, "communication": 0.12, "agentic": 0.02,
        }},
    },
    {
        "name": "Instruction Following",
        "description": "Instruction adherence, chat quality, and fluency",
        "tags": "writing communication instruction chat",
        "noise_sigma": 0.07, "samples": 1000, "weight": 1.0,
        # Highly specialized — communication dominant
        "category_dimension_weights": {"overall": {
            "reasoning": 0.08, "coding": 0.02, "knowledge": 0.05,
            "safety": 0.04, "communication": 0.80, "agentic": 0.01,
        }},
        # Adversarial-instruction holdout: jailbreak-via-instruction patterns
        # require more reasoning and safety-aware parsing beyond surface fluency.
        "holdout_category_dimension_weights": {"overall": {
            "reasoning": 0.18, "coding": 0.02, "knowledge": 0.05,
            "safety": 0.11, "communication": 0.62, "agentic": 0.02,
        }},
    },
    # --- Sequence benchmarks (6): mix of specialized and moderate ---
    {
        "name": "Scientific Reasoning",
        "description": "Graduate-level science questions requiring deep domain reasoning",
        "tags": "reasoning science knowledge research",
        "noise_sigma": 0.07, "samples": 1000, "weight": 1.0,
        # Highly specialized — reasoning dominant
        "category_dimension_weights": {"overall": {
            "reasoning": 0.78, "coding": 0.02, "knowledge": 0.15,
            "safety": 0.00, "communication": 0.04, "agentic": 0.01,
        }},
        # Private benchmark (mild+): GPQA Diamond-style — solutions never published.
        # Holdout shifts toward deeper knowledge synthesis within same scientific domain.
        "holdout_category_dimension_weights": {"overall": {
            "reasoning": 0.65, "coding": 0.03, "knowledge": 0.25,
            "safety": 0.00, "communication": 0.06, "agentic": 0.01,
        }},
    },
    {
        "name": "Agentic Tasks",
        "description": "Multi-step tool use, error recovery, and task automation",
        "tags": "coding agentic software automation tool-use",
        "noise_sigma": 0.08, "samples": 1000, "weight": 1.0,
        # SWE-bench/BFCL-style: agentic-dominant but reasoning+coding also meaningful.
        # Recalibrated 2026-04-20 from agentic=0.75 → 0.48 (paper Appendix A).
        "category_dimension_weights": {"overall": {
            "reasoning": 0.25, "coding": 0.19, "knowledge": 0.01,
            "safety": 0.00, "communication": 0.07, "agentic": 0.48,
        }},
        # Private benchmark (mild+): METR-style — known private task suite.
        # Holdout probes strategic multi-step reasoning within same agentic domain.
        # Holdout shifted with public: agentic 0.60 → 0.38, excess redistributed
        # proportionally to reasoning/coding/comm.
        "holdout_category_dimension_weights": {"overall": {
            "reasoning": 0.30, "coding": 0.23, "knowledge": 0.01,
            "safety": 0.00, "communication": 0.08, "agentic": 0.38,
        }},
    },
    {
        "name": "Hard Coding",
        "description": "Competitive programming and advanced software engineering",
        "tags": "coding software engineering competitive programming",
        "replaces": "Coding Evaluation",
        "noise_sigma": 0.06, "samples": 1000, "weight": 1.0,
        # Highly specialized — coding dominant (harder than Coding Evaluation)
        "category_dimension_weights": {"overall": {
            "reasoning": 0.10, "coding": 0.80, "knowledge": 0.02,
            "safety": 0.01, "communication": 0.01, "agentic": 0.06,
        }},
        # Private benchmark (strong tier): post-contest holdback.
        # Holdout probes deeper algorithmic reasoning within competitive programming domain.
        "holdout_category_dimension_weights": {"overall": {
            "reasoning": 0.18, "coding": 0.67, "knowledge": 0.03,
            "safety": 0.01, "communication": 0.02, "agentic": 0.09,
        }},
    },
    {
        "name": "Long Context",
        "description": "Long-document retrieval, summarization, and multi-hop reasoning",
        "tags": "writing knowledge reasoning long-document retrieval",
        "noise_sigma": 0.07, "samples": 1000, "weight": 1.0,
        # Moderately specialized — communication + knowledge
        "category_dimension_weights": {"overall": {
            "reasoning": 0.12, "coding": 0.02, "knowledge": 0.20,
            "safety": 0.01, "communication": 0.62, "agentic": 0.03,
        }},
        # Private benchmark (strong tier): multi-document tasks with private corpora.
        # Holdout probes cross-document reasoning requiring more synthesis.
        "holdout_category_dimension_weights": {"overall": {
            "reasoning": 0.18, "coding": 0.02, "knowledge": 0.25,
            "safety": 0.01, "communication": 0.50, "agentic": 0.04,
        }},
    },
    {
        "name": "Domain Expert",
        "description": "Professional knowledge in medicine, law, and finance",
        "tags": "knowledge reasoning medical legal finance domain",
        "noise_sigma": 0.07, "samples": 1000, "weight": 1.0,
        # Moderately specialized — knowledge dominant
        "category_dimension_weights": {"overall": {
            "reasoning": 0.20, "coding": 0.02, "knowledge": 0.65,
            "safety": 0.05, "communication": 0.07, "agentic": 0.01,
        }},
        # Private benchmark (mild+): licensing exam holdout sets are industry standard.
        # Holdout integrates domain knowledge with more reasoning and communication.
        "holdout_category_dimension_weights": {"overall": {
            "reasoning": 0.30, "coding": 0.02, "knowledge": 0.52,
            "safety": 0.05, "communication": 0.10, "agentic": 0.01,
        }},
    },
    {
        "name": "Agentic Safety",
        "description": "Safety evaluation in agentic and tool-use contexts",
        "tags": "safety agentic alignment trustworthy",
        "noise_sigma": 0.06, "samples": 1000, "weight": 1.0,
        # Dual-peaked — safety + agentic
        "category_dimension_weights": {"overall": {
            "reasoning": 0.12, "coding": 0.02, "knowledge": 0.03,
            "safety": 0.50, "communication": 0.08, "agentic": 0.25,
        }},
        # Private benchmark (both tiers, h=1.0): SEAL-analog — fully private.
        # Holdout tests harder safety+agentic scenarios within same evaluation domain.
        "holdout_category_dimension_weights": {"overall": {
            "reasoning": 0.22, "coding": 0.04, "knowledge": 0.02,
            "safety": 0.42, "communication": 0.10, "agentic": 0.20,
        }},
    },
    # --- New benchmarks (12) ---
    {
        "name": "Advanced Math",
        "description": "Competition-level mathematical reasoning and proof construction",
        "tags": "reasoning math competition problem-solving",
        "noise_sigma": 0.06, "samples": 1000, "weight": 1.0,
        # Highly specialized — reasoning dominant (hardest reasoning benchmark)
        "category_dimension_weights": {"overall": {
            "reasoning": 0.85, "coding": 0.06, "knowledge": 0.05,
            "safety": 0.00, "communication": 0.03, "agentic": 0.01,
        }},
        # FrontierMath-style holdout: multi-step synthesis requiring domain
        # knowledge and coding-adjacent formalism — not pattern-match on canonical forms.
        "holdout_category_dimension_weights": {"overall": {
            "reasoning": 0.67, "coding": 0.12, "knowledge": 0.12,
            "safety": 0.02, "communication": 0.05, "agentic": 0.02,
        }},
    },
    {
        "name": "Human Preference",
        "description": "Head-to-head human preference judgments on open-ended conversations",
        "tags": "communication writing preference chat general",
        "noise_sigma": 0.10, "samples": 500, "weight": 1.0,
        # Moderately specialized — communication + broad
        "category_dimension_weights": {"overall": {
            "reasoning": 0.10, "coding": 0.04, "knowledge": 0.12,
            "safety": 0.12, "communication": 0.58, "agentic": 0.04,
        }},
        # LMSYS Arena private holdout: refusal calibration on subtle harm
        # + long-tail factual queries that arena users actually probe.
        "holdout_category_dimension_weights": {"overall": {
            "reasoning": 0.10, "coding": 0.04, "knowledge": 0.18,
            "safety": 0.19, "communication": 0.45, "agentic": 0.04,
        }},
    },
    {
        "name": "Hard Knowledge",
        "description": "Harder multi-task knowledge evaluation with extended answer options",
        "tags": "reasoning knowledge general academic",
        "replaces": "General Capability",
        "noise_sigma": 0.06, "samples": 1200, "weight": 1.0,
        # Broad — reasoning + knowledge co-dominant
        "category_dimension_weights": {"overall": {
            "reasoning": 0.40, "coding": 0.04, "knowledge": 0.40,
            "safety": 0.02, "communication": 0.12, "agentic": 0.02,
        }},
        # MMLU-Pro 10-option distractor holdout: tests reasoning
        # discrimination depth, not just rote recall.
        "holdout_category_dimension_weights": {"overall": {
            "reasoning": 0.47, "coding": 0.04, "knowledge": 0.30,
            "safety": 0.02, "communication": 0.15, "agentic": 0.02,
        }},
    },
    {
        "name": "Clinical Reasoning",
        "description": "Clinical reasoning and medical knowledge for healthcare professionals",
        "tags": "knowledge reasoning medical healthcare domain",
        "noise_sigma": 0.07, "samples": 800, "weight": 1.0,
        # Moderately specialized — knowledge dominant
        "category_dimension_weights": {"overall": {
            "reasoning": 0.20, "coding": 0.01, "knowledge": 0.65,
            "safety": 0.08, "communication": 0.05, "agentic": 0.01,
        }},
        # Adversarial clinical-vignette holdout: mislabeled symptoms, high-stakes
        # differential-diagnosis under uncertainty — more reasoning and safety weight.
        "holdout_category_dimension_weights": {"overall": {
            "reasoning": 0.28, "coding": 0.01, "knowledge": 0.52,
            "safety": 0.13, "communication": 0.05, "agentic": 0.01,
        }},
    },
    {
        "name": "Legal Reasoning",
        "description": "Legal analysis, statutory interpretation, and case reasoning",
        "tags": "knowledge reasoning legal domain professional",
        "noise_sigma": 0.07, "samples": 800, "weight": 1.0,
        # Moderately specialized — knowledge dominant
        "category_dimension_weights": {"overall": {
            "reasoning": 0.25, "coding": 0.01, "knowledge": 0.60,
            "safety": 0.05, "communication": 0.08, "agentic": 0.01,
        }},
        # Case-novelty holdout: precedents unseen in training, requires stronger
        # reasoning and clearer communication of statutory interpretation.
        "holdout_category_dimension_weights": {"overall": {
            "reasoning": 0.33, "coding": 0.01, "knowledge": 0.48,
            "safety": 0.05, "communication": 0.12, "agentic": 0.01,
        }},
    },
    {
        "name": "Financial Analysis",
        "description": "Quantitative finance, market analysis, and financial reasoning",
        "tags": "knowledge reasoning finance domain quantitative",
        "noise_sigma": 0.07, "samples": 800, "weight": 1.0,
        # Moderately specialized — knowledge dominant with some coding
        "category_dimension_weights": {"overall": {
            "reasoning": 0.25, "coding": 0.10, "knowledge": 0.55,
            "safety": 0.02, "communication": 0.05, "agentic": 0.03,
        }},
        # Novel-regime market scenario holdout: quantitative modeling
        # (coding/math) + risk calibration (safety) under unfamiliar regime.
        "holdout_category_dimension_weights": {"overall": {
            "reasoning": 0.28, "coding": 0.16, "knowledge": 0.42,
            "safety": 0.06, "communication": 0.05, "agentic": 0.03,
        }},
    },
    {
        "name": "Multilingual Understanding",
        "description": "Cross-lingual reasoning and translation across diverse languages",
        "tags": "knowledge communication multilingual translation",
        "noise_sigma": 0.08, "samples": 800, "weight": 1.0,
        # Moderately specialized — communication + knowledge
        "category_dimension_weights": {"overall": {
            "reasoning": 0.15, "coding": 0.02, "knowledge": 0.25,
            "safety": 0.02, "communication": 0.55, "agentic": 0.01,
        }},
        # Low-resource FLORES holdout: cultural/regional knowledge transfer
        # + cross-lingual reasoning, not surface translation fluency.
        "holdout_category_dimension_weights": {"overall": {
            "reasoning": 0.20, "coding": 0.02, "knowledge": 0.33,
            "safety": 0.02, "communication": 0.42, "agentic": 0.01,
        }},
    },
    {
        "name": "Function Calling",
        "description": "API/tool calling accuracy, schema adherence, and multi-turn tool use",
        "tags": "coding agentic tool-use function-calling API",
        "noise_sigma": 0.06, "samples": 1000, "weight": 1.0,
        # BFCL-anchored: JSON/schema conformance (coding) dominates; tool-loop
        # (agentic) still substantial; tool-selection planning (reasoning) and
        # multi-turn result processing (communication) are meaningful.
        # Recalibrated 2026-04-20 from agentic=0.70 -> 0.40 (original overstated
        # pure-agentic weight; no consumer segment needs 70% agentic capability).
        "category_dimension_weights": {"overall": {
            "reasoning": 0.15, "coding": 0.30, "knowledge": 0.02,
            "safety": 0.01, "communication": 0.12, "agentic": 0.40,
        }},
        # Novel-API holdout: robust schema handling on unseen tool definitions,
        # shifting weight toward reasoning (plan for unseen tool) and coding
        # (parse unfamiliar schema); agentic loop less load-bearing. cos ~0.85.
        "holdout_category_dimension_weights": {"overall": {
            "reasoning": 0.25, "coding": 0.32, "knowledge": 0.03,
            "safety": 0.02, "communication": 0.13, "agentic": 0.25,
        }},
    },
    {
        "name": "Adversarial Robustness",
        "description": "Resistance to jailbreaks, prompt injection, and adversarial attacks",
        "tags": "safety alignment adversarial robustness red-team",
        "replaces": "Safety Evaluation",
        "noise_sigma": 0.08, "samples": 600, "weight": 1.0,
        # Highly specialized — safety dominant (hardest safety benchmark)
        "category_dimension_weights": {"overall": {
            "reasoning": 0.06, "coding": 0.01, "knowledge": 0.01,
            "safety": 0.85, "communication": 0.04, "agentic": 0.03,
        }},
        # SEAL-Safety / HarmBench-private holdout: jailbreak-via-reasoning-step,
        # unseen attack classes — more reasoning weight, broader dim-knowledge probe.
        "holdout_category_dimension_weights": {"overall": {
            "reasoning": 0.17, "coding": 0.01, "knowledge": 0.06,
            "safety": 0.67, "communication": 0.07, "agentic": 0.02,
        }},
    },
    {
        "name": "Web Navigation",
        "description": "Autonomous web browsing, form filling, and information retrieval",
        "tags": "agentic web automation tool-use browsing",
        "noise_sigma": 0.09, "samples": 500, "weight": 1.0,
        # Moderately specialized — agentic dominant
        "category_dimension_weights": {"overall": {
            "reasoning": 0.10, "coding": 0.08, "knowledge": 0.03,
            "safety": 0.02, "communication": 0.05, "agentic": 0.72,
        }},
        # Adversarial-UI Mind2Web holdout: anti-phishing / anti-prompt-injection
        # safety + planning under unfamiliar layouts.
        "holdout_category_dimension_weights": {"overall": {
            "reasoning": 0.15, "coding": 0.10, "knowledge": 0.03,
            "safety": 0.10, "communication": 0.05, "agentic": 0.57,
        }},
    },
    {
        "name": "Issue Resolution",
        "description": "Real-world software issue resolution with verified test suites",
        "tags": "coding agentic software verification debugging",
        "noise_sigma": 0.07, "samples": 800, "weight": 1.0,
        # Dual-peaked — coding + agentic
        "category_dimension_weights": {"overall": {
            "reasoning": 0.12, "coding": 0.42, "knowledge": 0.04,
            "safety": 0.01, "communication": 0.03, "agentic": 0.38,
        }},
        # SWE-bench-Verified-Plus private-repo holdout: codebase-convention
        # familiarity + patch readability humans accept on review.
        "holdout_category_dimension_weights": {"overall": {
            "reasoning": 0.16, "coding": 0.30, "knowledge": 0.09,
            "safety": 0.01, "communication": 0.06, "agentic": 0.38,
        }},
    },
    {
        "name": "Creative Writing",
        "description": "Fiction, poetry, and open-ended creative generation quality",
        "tags": "communication writing creative style",
        "noise_sigma": 0.10, "samples": 400, "weight": 1.0,
        # Highly specialized — communication dominant
        "category_dimension_weights": {"overall": {
            "reasoning": 0.05, "coding": 0.01, "knowledge": 0.08,
            "safety": 0.03, "communication": 0.82, "agentic": 0.01,
        }},
        # Novel-prompt creative + non-fiction holdout: factual integration
        # (knowledge) + trope / cliché avoidance (safety-adjacent style judgment).
        "holdout_category_dimension_weights": {"overall": {
            "reasoning": 0.07, "coding": 0.01, "knowledge": 0.16,
            "safety": 0.08, "communication": 0.67, "agentic": 0.01,
        }},
    },
]


@dataclass
class Benchmark:
    """
    Represents a benchmark managed by the Evaluator.

    Scoring uses the dot-product formula (via BenchmarkGroundTruth held by the sim):
        score ~ Normal(dot(capability_vector, dim_weights), (noise_sigma / sqrt(samples))^2)

    Gaming emerges from dimension mismatch: providers that over-invest in the
    dimensions a benchmark weights heavily will score above their general capability,
    without any explicit gaming lever.
    """
    name: str = "default_benchmark"

    # Short keyword string for consumer relevance matching
    tags: str = ""

    # Base standard deviation of score noise (used when BenchmarkGroundTruth is unavailable)
    noise_level: float = 0.08

    def get_summary(self) -> str:
        """Return a human-readable summary of benchmark properties."""
        return (
            f"Benchmark: {self.name}\n"
            f"  Noise: {self.noise_level:.2f}"
        )


@dataclass
class Regulation:
    """
    Represents a regulatory requirement that affects evaluation.

    Regulations can be issued by Regulators to change benchmark behavior.
    """
    name: str = ""
    regulation_type: str = ""  # "mandate_benchmark", "set_threshold", "require_disclosure"
    details: dict = field(default_factory=dict)
    issued_round: int = 0
    active: bool = True

    def get_summary(self) -> str:
        """Return a human-readable summary of the regulation."""
        status = "Active" if self.active else "Inactive"
        return f"{self.name} ({self.regulation_type}): {status} - {self.details}"


class Evaluator:
    """
    An Evaluator agent in the evaluation ecosystem simulation.

    The Evaluator:
    - Maintains one or more benchmarks
    - Scores models using dot-product of capability_vector × dimension_weights
    - Publishes scores that providers observe

    Key visibility design:
    - Ground truth (capability_vector) is passed FROM the simulation
    - The evaluator does NOT access actor state directly
    - This enforces the visibility boundary: actors can't see each other's ground truth

    Multi-benchmark support:
    - Can hold multiple benchmarks with different dimension weight profiles
    - Providers are scored on all benchmarks
    - Composite score is a weighted average across benchmarks

    Scoring model (per benchmark b):
        score ~ Normal(dot(capability_vector, dim_weights_b), (noise_sigma / sqrt(samples))^2)
    Gaming emerges from dimension mismatch — no explicit gaming lever.
    """

    def __init__(
        self,
        benchmark_name: str = "default_benchmark",
        noise_level: float = 0.08,
        seed: Optional[int] = None,
        benchmarks: Optional[list[dict]] = None,
        benchmark_sequence: Optional[list[dict]] = None,
        evaluator_as_company: bool = False,
        base_budget: float = 0.0,
        evaluator_mode: str = "fixed_sequence",
        benchmark_pool: Optional[list[dict]] = None,
        evaluation_lag: int = 0,
    ):
        """
        Initialize an Evaluator.

        Args:
            benchmark_name: Name of the primary benchmark (ignored if benchmarks provided)
            noise_level: Default noise sigma for auto-created benchmarks
            seed: Random seed for reproducibility
            benchmarks: Optional list of benchmark configs for multi-benchmark mode.
                       Each dict should have: name, noise_level, weight (validity optional)
            benchmark_sequence: Optional ordered list of benchmark dicts to introduce mid-simulation.
                       Each dict should have: name, noise_level (weight optional)
            evaluator_as_company: If True, evaluator tracks budget and collects funder allocations
            base_budget: Starting budget for evaluator
            evaluator_mode: "fixed_sequence" | "randomized_pool" | "dynamic"
            benchmark_pool: Full pool of benchmark configs for randomized/dynamic modes
            benchmark_dev_rounds: Rounds to develop a new benchmark (dynamic mode)
        """
        # Support for multiple benchmarks
        self.benchmarks: list[Benchmark] = []
        self.benchmark_weights: dict[str, float] = {}

        if benchmarks:
            # Multi-benchmark mode
            for bm_config in benchmarks:
                bm = Benchmark(
                    name=bm_config.get("name", f"benchmark_{len(self.benchmarks)}"),
                    tags=bm_config.get("tags", ""),
                    noise_level=bm_config.get("noise_level", 0.08),
                )
                self.benchmarks.append(bm)
                self.benchmark_weights[bm.name] = bm_config.get("weight", 1.0)
        else:
            # Single benchmark mode
            self.benchmarks.append(Benchmark(
                name=benchmark_name,
                noise_level=noise_level,
            ))
            self.benchmark_weights[benchmark_name] = 1.0

        # Random state for reproducibility
        self.rng = np.random.default_rng(seed)

        # History of published scores
        # Format: [(round, {provider_name: score}), ...]
        # For multi-benchmark: [(round, {provider_name: {benchmark_name: score, "composite": score}}), ...]
        self.score_history: list = []

        # Per-benchmark score history
        # Format: {benchmark_name: [(round, {provider_name: score}), ...]}
        self.benchmark_score_history: dict[str, list] = {bm.name: [] for bm in self.benchmarks}

        # Current round
        self.current_round: int = 0

        # Active regulations (from regulators)
        self.active_regulations: list[Regulation] = []

        # Benchmark introduction parameters
        self.benchmark_introduction_cooldown: int = 4
        self.last_introduction_round: int = 0  # first introduction at round 8
        self.max_benchmarks: int = 6
        self.introduction_history: list[dict] = []  # [{round, benchmark_name, trigger}]

        # Benchmark sequence (pre-defined benchmarks to introduce in order)
        self.benchmark_sequence: list[dict] = benchmark_sequence or []
        self._sequence_index: int = 0  # Track position in sequence

        # Per-benchmark best published scores (monotonicity enforcement)
        self._best_published_scores: dict[str, dict[str, float]] = {
            bm.name: {} for bm in self.benchmarks
        }

        # K-lag gating state: private benchmarks publish scores only every
        # evaluation_lag rounds. Between publications, providers see the last
        # published score (frozen). Public benchmarks (benchmark_type == "public")
        # are unaffected — they always publish every round.
        self.evaluation_lag: int = max(0, int(evaluation_lag))
        # benchmark_name -> {provider_name: last_published_score}
        self._last_published: dict[str, dict[str, float]] = {bm.name: {} for bm in self.benchmarks}

        # Benchmark saturation tracking (delta-based per spec)
        self._saturation_window: int = 3  # Consecutive rounds of near-zero deltas
        self._saturation_delta_threshold: float = 0.005  # Max delta to count as "near zero"
        self._saturation_cooldown: int = 2  # Rounds after saturation before trigger can fire
        self._benchmark_saturation_state: dict[str, dict] = {
            bm.name: {
                "saturated": False,
                "saturation_round": None,
                "cooldown_remaining": 0,
                "max_score": 0.0,
                "max_score_history": [],  # Recent max scores for delta computation
            } for bm in self.benchmarks
        }
        self.saturation_history: list[dict] = []  # [{round, benchmark_name, max_score}]

        # Signal-responsive introduction signals (used by dynamic mode)
        self._internal_validity: Optional[float] = None  # Pearson-r(score_rank, market_share_rank)

        # Evaluator mode: fixed_sequence | randomized_pool | dynamic
        self.evaluator_mode = evaluator_mode

        # Benchmark pool: all available benchmarks (introduced + unintroduced).
        # Each entry: {name, description, tags, noise_sigma, samples, weight, category_dimension_weights}
        # Pool is filtered: entries whose name matches an already-active benchmark are skipped.
        active_names = {bm.name for bm in self.benchmarks}
        if benchmark_pool is not None:
            self._benchmark_pool = [b for b in benchmark_pool if b["name"] not in active_names]
        else:
            self._benchmark_pool = []

        # Retired benchmarks (name -> round retired)
        self._retired_benchmarks: dict[str, int] = {}

        # Retirement reasons parallel to _retired_benchmarks (name -> short reason)
        # Populated by retire_benchmark. Surfaced to LLM dynamic evaluator prompt.
        self._retirement_reasons: dict[str, str] = {}

        # LLM dynamic-mode decision log: [{round, action, benchmark_name, reasoning}, ...]
        # Used only by LLM dynamic mode; written in simulation._dynamic_evaluator_decision.
        # Surfaced to subsequent LLM dynamic evaluator calls as Prior Quarterly Decisions.
        self._dynamic_llm_decisions: list[dict] = []

        # Evaluator-as-company feature (budget tracking, funder allocations)
        self.evaluator_as_company = evaluator_as_company
        self.private_state = None
        if evaluator_as_company:
            from visibility import EvaluatorPrivateState
            self.private_state = EvaluatorPrivateState(
                budget=base_budget,
            )

    _DIMS = ["reasoning", "coding", "knowledge", "safety", "communication", "agentic"]

    def _score_provider_on_benchmark(
        self,
        capability_vector: dict,
        bm_gt,
        benchmark: Benchmark,
    ) -> float:
        """
        Score a provider on a benchmark using the dot-product formula.

        Public benchmarks (benchmark_type == "public"):
            score ~ Normal(dot(cap, public_weights), (noise_sigma / sqrt(samples))^2)

        Private-ish benchmarks (partial/private/iid_holdout, h > 0):
            score ~ Normal(dot(cap, holdout_weights),
                           (noise_sigma / sqrt(samples * h))^2)
        Holdout-only reporting (no blending): gaming the public-weight direction
        doesn't mechanically raise the holdout score when cosine(public, holdout) < 1.
        Smaller h => fewer items in the holdout sample => noisier measurement.

        Gaming emerges from dimension mismatch between what providers target and
        what the holdout rewards.

        Args:
            capability_vector: Dict {dim: float} from ProviderGroundTruth
            bm_gt: BenchmarkGroundTruth object from sim (or None for fallback)
            benchmark: Benchmark object (for noise fallback)

        Returns:
            Score in [0, 1]
        """
        if bm_gt is not None:
            is_private = bm_gt.benchmark_type != "public" and bm_gt.holdout_fraction > 0
            if is_private:
                cdw = bm_gt.holdout_category_dimension_weights or bm_gt.category_dimension_weights
                effective_samples = bm_gt.samples * bm_gt.holdout_fraction
            else:
                cdw = bm_gt.category_dimension_weights
                effective_samples = bm_gt.samples
            noise_sigma = bm_gt.noise_sigma
            # Aggregate {category: {dim: weight}} to flat {dim: weight} by averaging categories.
            if cdw and isinstance(next(iter(cdw.values())), dict):
                agg: dict = {}
                for cat_weights in cdw.values():
                    for dim, w in cat_weights.items():
                        agg[dim] = agg.get(dim, 0.0) + w
                n_cats = len(cdw)
                weights = {dim: w / n_cats for dim, w in agg.items()}
            else:
                weights = cdw  # Already a flat {dim: weight} dict
        else:
            # Fallback: uniform weights, default noise (benchmark has no GT record)
            weights = {d: 1.0 / len(self._DIMS) for d in self._DIMS}
            noise_sigma = benchmark.noise_level
            effective_samples = 100.0

        mean_score = sum(
            capability_vector.get(d, 0.0) * weights.get(d, 0.0)
            for d in self._DIMS
        )
        noise_std = noise_sigma / np.sqrt(max(effective_samples, 1.0))
        score = self.rng.normal(mean_score, noise_std)
        return max(0.0, min(1.0, score))

    def collect_funding(
        self,
        funder_allocations: dict,
        round_num: int,
    ) -> dict:
        """
        Collect funding from funders.

        Args:
            funder_allocations: Dict mapping funder_name -> allocation amount
            round_num: Current simulation round

        Returns:
            Dict with funding details
        """
        if not self.evaluator_as_company:
            return {}

        base_funding = sum(funder_allocations.values())

        self.private_state.budget += base_funding
        self.private_state.base_funding = base_funding

        return {
            "base_funding": base_funding,
            "total_funding": base_funding,
            "budget": self.private_state.budget,
        }

    def evaluate_all(
        self,
        providers: list,
        round_num: int,
        ground_truth: Optional[dict] = None,
        benchmark_ground_truths: Optional[dict] = None,
    ) -> dict:
        """
        Evaluate all providers on all benchmarks and return composite scores.

        Scoring formula per benchmark:
            score ~ Normal(dot(capability_vector, dim_weights), (noise_sigma / sqrt(samples))^2)

        Gaming emerges from dimension mismatch — no explicit gaming lever.

        Args:
            providers: List of ModelProvider objects
            round_num: Current simulation round
            ground_truth: Dict mapping provider names to ProviderGroundTruth objects
            benchmark_ground_truths: Dict mapping benchmark names to BenchmarkGroundTruth objects

        Returns:
            Dict mapping provider names to composite scores
        """
        self.current_round = round_num
        # Store ground truths for use by get_benchmark_dimension_weights()
        if benchmark_ground_truths is not None:
            self._benchmark_ground_truth = benchmark_ground_truths
        composite_scores = {}
        per_benchmark_scores = {bm.name: {} for bm in self.benchmarks}

        for provider in providers:
            # Get capability vector from ground truth
            if ground_truth is not None and provider.name in ground_truth:
                cap_vec = ground_truth[provider.name].capability_vector
            else:
                cap_vec = {d: 0.5 for d in self._DIMS}

            weighted_sum = 0.0
            total_weight = 0.0

            for benchmark in self.benchmarks:
                bm_gt = (benchmark_ground_truths or {}).get(benchmark.name)
                is_private = bm_gt is not None and bm_gt.benchmark_type != "public" and bm_gt.holdout_fraction > 0

                # K-lag gating: private-type benchmarks publish a fresh score only
                # every evaluation_lag rounds. Public benchmarks and K<=1 publish fresh
                # every round. Between publications, providers see the frozen last score.
                is_publish_round = (
                    (not is_private)
                    or self.evaluation_lag <= 1
                    or (round_num % self.evaluation_lag == 0)
                )

                if is_publish_round:
                    # Fresh evaluation. Best-of-N trials for premium providers (evaluator_capture).
                    n_trials = 1
                    if (self.evaluator_as_company
                            and self.private_state
                            and provider.name in self.private_state.submission_counts):
                        n_trials = self.private_state.submission_counts[provider.name]

                    if n_trials > 1:
                        trial_scores = [
                            self._score_provider_on_benchmark(cap_vec, bm_gt, benchmark)
                            for _ in range(n_trials)
                        ]
                        score = max(trial_scores)
                    else:
                        score = self._score_provider_on_benchmark(cap_vec, bm_gt, benchmark)

                    if is_private:
                        self._last_published[benchmark.name][provider.name] = score
                else:
                    # Frozen: return last published score. First-publish fallback: if no
                    # score has been published yet (benchmark introduced at a non-publish
                    # round), compute one now as the initial baseline and cache it.
                    score = self._last_published[benchmark.name].get(provider.name)
                    if score is None:
                        score = self._score_provider_on_benchmark(cap_vec, bm_gt, benchmark)
                        self._last_published[benchmark.name][provider.name] = score

                # Monotonicity: providers wouldn't disclose a worse score
                best = self._best_published_scores[benchmark.name].get(provider.name, 0.0)
                score = max(score, best)
                self._best_published_scores[benchmark.name][provider.name] = score

                per_benchmark_scores[benchmark.name][provider.name] = score

                weight = self.benchmark_weights.get(benchmark.name, 1.0)
                weighted_sum += score * weight
                total_weight += weight

            composite_scores[provider.name] = weighted_sum / total_weight if total_weight > 0 else 0.0

        # Record per-benchmark history
        for bm_name, scores in per_benchmark_scores.items():
            self.benchmark_score_history[bm_name].append((round_num, dict(scores)))

        self.score_history.append((round_num, dict(composite_scores)))

        return composite_scores

    def get_per_benchmark_scores(self, round_num: int) -> dict:
        """
        Get per-benchmark scores for a specific round.

        Args:
            round_num: Round number to get scores for

        Returns:
            Dict mapping benchmark_name -> {provider_name: score}
        """
        result = {}
        for bm_name, history in self.benchmark_score_history.items():
            for r, scores in history:
                if r == round_num:
                    result[bm_name] = scores
                    break
        return result

    def publish_scores(self, scores: dict) -> dict:
        """
        Publish scores (in current implementation, just returns scores).

        In a more complex simulation, this could involve:
        - Delayed publication
        - Partial information release
        - Leaderboard formatting

        Args:
            scores: Dict of {provider_name: score}

        Returns:
            Published scores (currently just the input)
        """
        return scores

    def get_leaderboard(self, scores: dict) -> list:
        """
        Return providers ranked by score.

        Args:
            scores: Dict of {provider_name: score}

        Returns:
            List of (provider_name, score) tuples, sorted descending by score
        """
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)

    def add_regulation(self, regulation: Regulation):
        """
        Add a regulation from a regulator.

        Args:
            regulation: The regulation to add
        """
        self.active_regulations.append(regulation)

        # Apply regulation effects (future implementation)
        pass

    def remove_regulation(self, regulation_name: str):
        """Remove a regulation by name."""
        self.active_regulations = [
            r for r in self.active_regulations if r.name != regulation_name
        ]

    def get_active_regulations(self) -> list[Regulation]:
        """Get list of active regulations."""
        return [r for r in self.active_regulations if r.active]

    def get_llm_observation(self) -> dict:
        """Collect observation data for LLM-based evaluator planning.

        Returns dict with keys needed by llm_plan_evaluator():
            active_benchmarks, score_deltas, score_spread, internal_validity,
            saturation_states
        """
        active_benchmarks = []
        for bm in self.benchmarks:
            entry = {"name": bm.name, "tags": bm.tags, "weight": self.benchmark_weights.get(bm.name, 1.0)}
            bm_gt = (getattr(self, "_benchmark_ground_truth", None) or {}).get(bm.name)
            if bm_gt is not None and bm_gt.holdout_fraction > 0:
                entry["holdout_fraction"] = bm_gt.holdout_fraction
            active_benchmarks.append(entry)

        # Score deltas: compare last two rounds per benchmark
        score_deltas = {}
        score_spread = {}
        for bm in self.benchmarks:
            history = self.benchmark_score_history.get(bm.name, [])
            if len(history) >= 2:
                _, prev_scores = history[-2]
                _, curr_scores = history[-1]
                deltas = {}
                for p in curr_scores:
                    if p in prev_scores:
                        deltas[p] = curr_scores[p] - prev_scores[p]
                score_deltas[bm.name] = deltas
                vals = list(curr_scores.values())
                score_spread[bm.name] = max(vals) - min(vals) if vals else 0
            elif len(history) == 1:
                _, curr_scores = history[-1]
                score_deltas[bm.name] = {}
                vals = list(curr_scores.values())
                score_spread[bm.name] = max(vals) - min(vals) if vals else 0

        saturation_states = {
            bm.name: {
                "saturated": self._benchmark_saturation_state.get(bm.name, {}).get("saturated", False),
                "max_score": self._benchmark_saturation_state.get(bm.name, {}).get("max_score", 0),
            }
            for bm in self.benchmarks
        }

        obs = {
            "active_benchmarks": active_benchmarks,
            "score_deltas": score_deltas,
            "score_spread": score_spread,
            "internal_validity": self._internal_validity,
            "saturation_states": saturation_states,
        }

        # Dynamic mode: add pool + enriched retirement/introduction metadata + prior decisions
        if self.evaluator_mode == "dynamic":
            obs["available_pool"] = self.get_pool_for_llm()

            # Enriched retired: [(name, retired_round, reason), ...]
            obs["retired_benchmarks_enriched"] = [
                (
                    name,
                    retired_round,
                    self._retirement_reasons.get(name, "unspecified"),
                )
                for name, retired_round in self._retired_benchmarks.items()
            ]

            # Introduction metadata keyed by benchmark name: {name: (round, trigger, reasoning)}
            # `trigger` carries heuristic-path reason ("fixed_sequence", "saturation:..."),
            # `reasoning` holds LLM-path tail when the LLM initiated the introduction.
            intro_map: dict[str, dict] = {}
            for entry in self.introduction_history:
                bm_name = entry.get("benchmark_name")
                if not bm_name:
                    continue
                intro_map[bm_name] = {
                    "round": entry.get("round"),
                    "trigger": entry.get("trigger", ""),
                    "reasoning": entry.get("reasoning"),
                }
            obs["introduction_metadata"] = intro_map

            # Last 3 LLM decisions (this evaluator's own reasoning trail)
            obs["prior_decisions"] = list(self._dynamic_llm_decisions[-3:])

            # Active regulations (short-string summaries for the LLM prompt)
            obs["active_regulations"] = [
                reg.name for reg in self.get_active_regulations() if reg.name
            ]

        return obs

    def _evaluate_introduction_trigger(self, round_num: int) -> Optional[str]:
        """Decide whether to introduce a new benchmark this round.

        Used only by fixed_sequence and randomized_pool heuristic modes.
        Dynamic mode has its own trigger logic in heuristic_dynamic_decide (heuristic)
        and llm_plan_dynamic_evaluator (LLM).

        Triggers:
            - Saturation (bypasses cooldown with min gap of 1 round)
            - Periodic introduction every cooldown rounds
        """
        # --- Saturation trigger: bypasses main cooldown ---
        saturation_trigger = None
        for bm in self.benchmarks:
            state = self._benchmark_saturation_state.get(bm.name)
            if state and state["saturated"] and state["cooldown_remaining"] <= 0:
                saturation_trigger = f"saturation:{bm.name}={state['max_score']:.4f}"
                break

        _saturation_min_gap = 1
        if saturation_trigger and round_num - self.last_introduction_round >= _saturation_min_gap:
            return saturation_trigger

        # --- Periodic introduction (subject to standard cooldown) ---
        if round_num - self.last_introduction_round < self.benchmark_introduction_cooldown:
            return None

        if round_num > 0 and round_num % self.benchmark_introduction_cooldown == 0:
            return f"periodic_introduction:round_{round_num}"
        return None

    def consider_new_benchmark(self, round_num: int) -> Optional[Benchmark]:
        """
        Consider introducing a new benchmark (heuristic fixed/randomized modes).

        Modes:
        - fixed_sequence: periodic introduction every cooldown rounds,
          plus saturation-triggered replacement. Pulls from sequence in order.
        - randomized_pool: same triggers as fixed_sequence, but draws randomly
          from the benchmark pool instead of sequentially.

        dynamic mode is handled separately via advance_pipeline + create_from_pool
        (see heuristic_dynamic_decide and the LLM dynamic_evaluator path).

        Returns:
            New Benchmark if introduced, None otherwise
        """
        if self.evaluator_mode == "dynamic":
            return None  # Handled by pipeline, not heuristic triggers

        # Check budget (if company mode)
        benchmark_cost = 50000.0
        if self.evaluator_as_company:
            if self.private_state.budget < benchmark_cost:
                return None

        # No benchmarks left in pool/sequence to introduce
        if self.evaluator_mode == "randomized_pool" and not self._benchmark_pool:
            return None

        trigger = self._evaluate_introduction_trigger(round_num)
        if trigger is None:
            return None

        if self.evaluator_mode == "randomized_pool":
            # Draw randomly from pool
            idx = self.rng.integers(len(self._benchmark_pool))
            pool_config = self._benchmark_pool[idx]
            return self._create_and_register_benchmark(round_num, trigger, pool_config=pool_config)

        # fixed_sequence (default)
        return self._create_and_register_benchmark(round_num, trigger)

    def _create_and_register_benchmark(
        self, round_num: int, trigger: str, pool_config: Optional[dict] = None,
    ) -> Optional[Benchmark]:
        """Create a new benchmark from sequence/pool or auto-generate, and register it.

        Called by consider_new_benchmark (heuristic fixed/randomized modes).

        Args:
            round_num: Current simulation round
            trigger: String describing what triggered this introduction
            pool_config: If provided, use this specific benchmark config from the pool.
                        Used by randomized_pool and dynamic modes.
        """
        benchmark_cost = 50000.0
        if self.evaluator_as_company:
            if self.private_state.budget < benchmark_cost:
                return None

        # Determine benchmark config source BEFORE retiring anything
        bm_config = None
        if pool_config is not None:
            bm_config = pool_config
        elif self.benchmark_sequence and self._sequence_index < len(self.benchmark_sequence):
            bm_config = self.benchmark_sequence[self._sequence_index]
            self._sequence_index += 1

        if bm_config is None:
            return None  # No config available — don't retire without a replacement

        # Auto-retire if at cap (safe now — we know we have a replacement)
        retired_name = None
        if len(self.benchmarks) >= self.max_benchmarks:
            retired_name = self.retire_benchmark(round_num)
            if retired_name is None:
                return None

        new_name = bm_config.get("name", f"benchmark_r{round_num}")
        new_bm = Benchmark(
            name=new_name,
            tags=bm_config.get("tags", ""),
            noise_level=bm_config.get("noise_level", bm_config.get("noise_sigma", 0.08)),
        )
        if "weight" in bm_config:
            new_weight = bm_config["weight"]
        else:
            new_weight = sum(self.benchmark_weights.values()) / len(self.benchmark_weights) if self.benchmark_weights else 1.0

        # Register in evaluator state
        self.benchmarks.append(new_bm)
        self.benchmark_weights[new_name] = new_weight
        self.benchmark_score_history[new_name] = []
        self._best_published_scores[new_name] = {}
        self._last_published[new_name] = {}

        self._benchmark_saturation_state[new_name] = {
            "saturated": False,
            "saturation_round": None,
            "cooldown_remaining": 0,
            "max_score": 0.0,
            "max_score_history": [],
        }

        # If triggered by saturation, re-apply cooldown on the triggering benchmark
        # so it doesn't fire every round. Uses _saturation_cooldown (not the full
        # benchmark_introduction_cooldown) for faster replacement of truly stale benchmarks.
        if trigger.startswith("saturation:"):
            trigger_bm_name = trigger.split(":")[1].split("=")[0]
            if trigger_bm_name in self._benchmark_saturation_state:
                self._benchmark_saturation_state[trigger_bm_name]["cooldown_remaining"] = (
                    self._saturation_cooldown
                )

        self.last_introduction_round = round_num
        self.introduction_history.append({
            "round": round_num,
            "benchmark_name": new_name,
            "trigger": trigger,
            "retired": retired_name,
        })

        # Remove introduced benchmark from pool
        self._benchmark_pool = [b for b in self._benchmark_pool if b["name"] != new_name]

        if self.evaluator_as_company:
            self.private_state.budget -= benchmark_cost

        return new_bm

    def retire_benchmark(
        self,
        round_num: int,
        benchmark_name: Optional[str] = None,
        reason: str = "auto-retire at cap",
    ) -> Optional[str]:
        """Retire a benchmark, freeing a slot for a new one.

        If benchmark_name is None, auto-selects the most saturated benchmark
        (longest time since saturation, or highest max_score if tied).

        Args:
            reason: Short tag stored in _retirement_reasons for downstream
                LLM dynamic prompt rendering. Callers with a specific cause
                ("saturation", "llm: <tail>") should pass one; default covers
                sim-initiated auto-retire when introducing at cap.

        Returns the name of the retired benchmark, or None if nothing to retire.
        """
        if len(self.benchmarks) == 0:
            return None

        auto_selected = benchmark_name is None
        if auto_selected:
            # Pick the most saturated: prefer benchmarks that are already saturated,
            # then by earliest saturation_round, then by highest max_score.
            candidates = []
            for bm in self.benchmarks:
                state = self._benchmark_saturation_state.get(bm.name, {})
                is_sat = state.get("saturated", False)
                sat_round = state.get("saturation_round") if is_sat else 999999
                max_score = state.get("max_score", 0.0)
                candidates.append((bm.name, not is_sat, sat_round, -max_score))
            # Sort: saturated first (not is_sat=False < True), then earliest sat round, then highest score
            candidates.sort(key=lambda x: (x[1], x[2], x[3]))
            benchmark_name = candidates[0][0]
            # If auto-selected a saturated benchmark, refine the default reason.
            sat_state = self._benchmark_saturation_state.get(benchmark_name, {})
            if sat_state.get("saturated") and reason == "auto-retire at cap":
                reason = "saturation"

        # Remove from all tracking structures
        self.benchmarks = [bm for bm in self.benchmarks if bm.name != benchmark_name]
        self.benchmark_weights.pop(benchmark_name, None)
        self.benchmark_score_history.pop(benchmark_name, None)
        self._best_published_scores.pop(benchmark_name, None)
        self._last_published.pop(benchmark_name, None)
        self._benchmark_saturation_state.pop(benchmark_name, None)

        self._retired_benchmarks[benchmark_name] = round_num
        self._retirement_reasons[benchmark_name] = reason
        return benchmark_name

    # ------------------------------------------------------------------
    # Dynamic mode: development pipeline
    # ------------------------------------------------------------------

    def get_pool_for_llm(self) -> list[dict]:
        """Return unintroduced pool entries visible to the LLM evaluator.

        Visibility: name, description, tags only. Dimension weights are NEVER shown.
        """
        return [
            {"name": b["name"], "description": b.get("description", ""), "tags": b.get("tags", "")}
            for b in self._benchmark_pool
        ]

    def detect_saturation(self, round_num: int) -> list[str]:
        """
        Detect benchmarks that have been saturated (score deltas near zero).

        A benchmark is considered saturated when the max-score delta is below
        `saturation_delta_threshold` for `saturation_window` consecutive rounds.
        Perfect scores (>= 1.0) also trigger immediate saturation.

        Also decrements cooldown_remaining on already-saturated benchmarks so
        that the saturation trigger in _evaluate_introduction_trigger can fire
        after the cooldown elapses.

        Args:
            round_num: Current round number

        Returns:
            List of newly saturated benchmark names
        """
        newly_saturated = []

        # Tick down cooldowns on already-saturated benchmarks
        for state in self._benchmark_saturation_state.values():
            if state.get("saturated") and state.get("cooldown_remaining", 0) > 0:
                state["cooldown_remaining"] -= 1

        for bm in self.benchmarks:
            state = self._benchmark_saturation_state.get(bm.name)
            if not state or state["saturated"]:
                continue

            # Get max score for this benchmark from current round
            if bm.name not in self.benchmark_score_history:
                continue
            for r, scores in reversed(self.benchmark_score_history[bm.name]):
                if r == round_num:
                    if not scores:
                        break
                    max_score = max(scores.values())
                    prev_max = state["max_score"]
                    state["max_score"] = max_score

                    # Track max score history for delta computation (keep only needed window)
                    state["max_score_history"].append(max_score)
                    keep = self._saturation_window + 1
                    if len(state["max_score_history"]) > keep:
                        state["max_score_history"] = state["max_score_history"][-keep:]

                    # Check for perfect score (1.000) — immediate saturation
                    if max_score >= 1.0:
                        state["saturated"] = True
                        state["saturation_round"] = round_num
                        state["cooldown_remaining"] = self._saturation_cooldown
                        newly_saturated.append(bm.name)
                        self.saturation_history.append({
                            "round": round_num,
                            "benchmark_name": bm.name,
                            "max_score": max_score,
                            "trigger": "perfect_score",
                        })
                        break

                    # Delta-based detection: check last saturation_window rounds
                    history = state["max_score_history"]
                    if len(history) >= self._saturation_window + 1:
                        recent = history[-(self._saturation_window + 1):]
                        deltas = [recent[i+1] - recent[i] for i in range(len(recent) - 1)]
                        if all(d < self._saturation_delta_threshold for d in deltas):
                            state["saturated"] = True
                            state["saturation_round"] = round_num
                            state["cooldown_remaining"] = self._saturation_cooldown
                            newly_saturated.append(bm.name)
                            self.saturation_history.append({
                                "round": round_num,
                                "benchmark_name": bm.name,
                                "max_score": max_score,
                                "trigger": "delta_stagnation",
                            })
                    break

        return newly_saturated

    def update_internal_validity(self, market_shares: dict):
        """Compute internal validity: Pearson-r(score_rank, market_share_rank).

        This is the evaluator's private signal of whether scores are tracking
        real-world adoption. Low correlation suggests scores have decoupled
        from what consumers actually value.

        Args:
            market_shares: {provider_name: share} from consumer data
        """
        if not self.score_history or not market_shares:
            return
        _, latest_scores = self.score_history[-1]
        # Need providers present in both
        common = [p for p in latest_scores if p in market_shares]
        if len(common) < 3:
            return
        from scipy.stats import spearmanr
        scores = [latest_scores[p] for p in common]
        shares = [market_shares[p] for p in common]
        if len(set(scores)) < 2 or len(set(shares)) < 2:
            return
        corr, _ = spearmanr(scores, shares)
        if not np.isnan(corr):
            self._internal_validity = corr

    def is_benchmark_saturated(self, benchmark_name: str) -> bool:
        """
        Check if a benchmark is currently saturated (after cooldown).

        Args:
            benchmark_name: Name of the benchmark to check

        Returns:
            True if benchmark is saturated and past cooldown period
        """
        state = self._benchmark_saturation_state.get(benchmark_name)
        if not state:
            return False
        return state.get("saturated", False) and state.get("cooldown_remaining", 0) <= 0

    def get_benchmark_dimension_weights(self) -> dict:
        """Return aggregated flat {dim: weight} for each active benchmark.

        Uses the same aggregation as score_provider: average per-category dim loadings
        into a single flat vector. This is the vector that capability_vector is dotted
        against to produce a score, and the key input for gaming analysis.
        """
        result = {}
        for bm in self.benchmarks:
            bm_gt = self._benchmark_ground_truth.get(bm.name)
            if bm_gt is None:
                result[bm.name] = {d: 1.0 / len(self._DIMS) for d in self._DIMS}
                continue
            cdw = bm_gt.category_dimension_weights
            if cdw and isinstance(next(iter(cdw.values())), dict):
                agg: dict = {}
                for cat_weights in cdw.values():
                    for dim, w in cat_weights.items():
                        agg[dim] = agg.get(dim, 0.0) + w
                n_cats = len(cdw)
                result[bm.name] = {dim: w / n_cats for dim, w in agg.items()}
            else:
                result[bm.name] = dict(cdw) if cdw else {d: 1.0 / len(self._DIMS) for d in self._DIMS}
        return result

    def get_statistics(self) -> dict:
        """
        Get summary statistics about evaluation history.

        Returns:
            Dict with various statistics
        """
        stats = {
            "total_rounds": len(self.score_history),
            "num_benchmarks": len(self.benchmarks),
            "active_regulations": len(self.get_active_regulations()),
        }

        # Per-benchmark stats
        stats["benchmarks"] = {}
        for bm in self.benchmarks:
            stats["benchmarks"][bm.name] = {
                "noise": bm.noise_level,
                "weight": self.benchmark_weights.get(bm.name, 1.0),
            }

        # Recent scores
        if self.score_history:
            recent_round, recent_scores = self.score_history[-1]
            stats["latest_round"] = recent_round
            stats["latest_scores"] = recent_scores

        return stats

    def get_benchmark_summary(self) -> str:
        """Get a summary of all benchmarks."""
        lines = [f"Evaluator with {len(self.benchmarks)} benchmark(s):"]
        for bm in self.benchmarks:
            weight = self.benchmark_weights.get(bm.name, 1.0)
            lines.append(f"  - {bm.name}: noise={bm.noise_level:.2f}, weight={weight:.1f}")
        return "\n".join(lines)

    def save(self, filepath: str):
        """Save evaluator state to JSON file."""
        data = {
            "benchmarks": [
                {
                    "name": bm.name,
                    "tags": bm.tags,
                    "noise_level": bm.noise_level,
                    "weight": self.benchmark_weights.get(bm.name, 1.0),
                }
                for bm in self.benchmarks
            ],
            "score_history": self.score_history,
            "benchmark_score_history": self.benchmark_score_history,
            "current_round": self.current_round,
            "benchmark_introduction_cooldown": self.benchmark_introduction_cooldown,
            "last_introduction_round": self.last_introduction_round,
            "max_benchmarks": self.max_benchmarks,
            "introduction_history": self.introduction_history,
            "_best_published_scores": self._best_published_scores,
            # Saturation tracking
            "_saturation_window": self._saturation_window,
            "_saturation_delta_threshold": self._saturation_delta_threshold,
            "_saturation_cooldown": self._saturation_cooldown,
            "_benchmark_saturation_state": self._benchmark_saturation_state,
            "saturation_history": self.saturation_history,
            "regulations": [
                {
                    "name": r.name,
                    "regulation_type": r.regulation_type,
                    "details": r.details,
                    "issued_round": r.issued_round,
                    "active": r.active,
                }
                for r in self.active_regulations
            ],
            # Evaluator-as-company state
            "evaluator_as_company": self.evaluator_as_company,
            "private_state": self.private_state.to_dict() if self.private_state else None,
            # Evaluator mode state
            "evaluator_mode": self.evaluator_mode,
            "_benchmark_pool": self._benchmark_pool,
            "_retired_benchmarks": self._retired_benchmarks,
            "_retirement_reasons": self._retirement_reasons,
            "_dynamic_llm_decisions": self._dynamic_llm_decisions,
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load(cls, filepath: str, seed: Optional[int] = None) -> "Evaluator":
        """Load evaluator state from JSON file."""
        with open(filepath, "r") as f:
            data = json.load(f)

        benchmarks = data.get("benchmarks", [])
        if benchmarks:
            evaluator = cls(benchmarks=benchmarks, seed=seed)
        else:
            evaluator = cls(seed=seed)

        evaluator.score_history = data["score_history"]
        evaluator.current_round = data["current_round"]

        # Load benchmark score history if present
        if "benchmark_score_history" in data:
            evaluator.benchmark_score_history = data["benchmark_score_history"]

        # Load benchmark introduction state if present
        evaluator.benchmark_introduction_cooldown = data.get("benchmark_introduction_cooldown", 4)
        evaluator.last_introduction_round = data.get("last_introduction_round", 0)
        evaluator.max_benchmarks = data.get("max_benchmarks", 6)
        evaluator.introduction_history = data.get("introduction_history", [])

        # Load best published scores for monotonicity enforcement
        if "_best_published_scores" in data:
            evaluator._best_published_scores = data["_best_published_scores"]
        else:
            evaluator._best_published_scores = {bm.name: {} for bm in evaluator.benchmarks}

        # Load saturation tracking state if present
        if "_saturation_window" in data:
            evaluator._saturation_window = data["_saturation_window"]
        if "_saturation_delta_threshold" in data:
            evaluator._saturation_delta_threshold = data["_saturation_delta_threshold"]
        if "_saturation_cooldown" in data:
            evaluator._saturation_cooldown = data["_saturation_cooldown"]
        if "_benchmark_saturation_state" in data:
            evaluator._benchmark_saturation_state = data["_benchmark_saturation_state"]
        else:
            # Initialize for existing benchmarks
            evaluator._benchmark_saturation_state = {
                bm.name: {
                    "saturated": False,
                    "saturation_round": None,
                    "cooldown_remaining": 0,
                    "max_score": 0.0,
                    "max_score_history": [],
                } for bm in evaluator.benchmarks
            }
        if "saturation_history" in data:
            evaluator.saturation_history = data["saturation_history"]

        # Load regulations if present
        if "regulations" in data:
            evaluator.active_regulations = [
                Regulation(**r) for r in data["regulations"]
            ]

        # Load evaluator-as-company state if present
        if "evaluator_as_company" in data:
            evaluator.evaluator_as_company = data["evaluator_as_company"]
            if data.get("private_state") and evaluator.evaluator_as_company:
                from visibility import EvaluatorPrivateState
                evaluator.private_state = EvaluatorPrivateState.from_dict(data["private_state"])

        # Load evaluator mode state if present
        evaluator.evaluator_mode = data.get("evaluator_mode", "fixed_sequence")
        evaluator._benchmark_pool = data.get("_benchmark_pool", [])
        evaluator._retired_benchmarks = data.get("_retired_benchmarks", {})
        evaluator._retirement_reasons = data.get("_retirement_reasons", {})
        evaluator._dynamic_llm_decisions = data.get("_dynamic_llm_decisions", [])

        return evaluator

    def __repr__(self):
        bm_names = ", ".join(bm.name for bm in self.benchmarks)
        return f"Evaluator(benchmarks=[{bm_names}])"
