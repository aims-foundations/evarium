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
        dynamic_evaluator: bool = False,
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
        self.benchmark_introduction_cooldown: int = 7
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

        # Benchmark saturation tracking (delta-based per spec)
        self._saturation_window: int = 3  # Consecutive rounds of near-zero deltas
        self._saturation_delta_threshold: float = 0.005  # Max delta to count as "near zero"
        self._saturation_cooldown: int = 2  # Rounds to wait before starting weight decay
        self._benchmark_saturation_state: dict[str, dict] = {
            bm.name: {
                "saturated": False,
                "saturation_round": None,
                "cooldown_remaining": 0,
                "max_score": 0.0,
                "max_score_history": [],  # Recent max scores for delta computation
                "perfect_score_hit": False,  # True if any provider hit exactly 1.000
            } for bm in self.benchmarks
        }
        self.saturation_history: list[dict] = []  # [{round, benchmark_name, max_score}]

        # Dynamic evaluator mode (signal-based introduction vs fixed schedule)
        self.dynamic_evaluator = dynamic_evaluator
        self._internal_validity: Optional[float] = None  # Pearson-r(score_rank, market_share_rank)
        self._validity_threshold: float = 0.5  # Below this triggers fresh benchmark introduction

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

            score ~ Normal(dot(capability_vector, dim_weights), (noise_sigma / sqrt(samples))^2)

        Gaming emerges naturally: providers whose capability_vector aligns with
        the benchmark's dimension weights score higher than providers with equal
        general capability but different specialization.

        Args:
            capability_vector: Dict {dim: float} from ProviderGroundTruth
            bm_gt: BenchmarkGroundTruth object from sim (or None for fallback)
            benchmark: Benchmark object (for noise fallback)

        Returns:
            Score in [0, 1]
        """
        if bm_gt is not None:
            cdw = bm_gt.category_dimension_weights
            noise_sigma = bm_gt.noise_sigma
            samples = bm_gt.samples
            # Aggregate {category: {dim: weight}} to flat {dim: weight} by averaging categories.
            # This implements: raw_score = dot(capability_vector, benchmark_true_weights)
            # where benchmark_true_weights is the mean of per-category dimension loadings.
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
            # Fallback: uniform weights, default noise
            weights = {d: 1.0 / len(self._DIMS) for d in self._DIMS}
            noise_sigma = benchmark.noise_level
            samples = 100

        mean_score = sum(
            capability_vector.get(d, 0.0) * weights.get(d, 0.0)
            for d in self._DIMS
        )
        noise_std = noise_sigma / np.sqrt(max(samples, 1))
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

                # Best-of-N trials for premium providers (eval_as_company)
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
        active_benchmarks = [
            {"name": bm.name, "tags": bm.tags, "weight": self.benchmark_weights.get(bm.name, 1.0)}
            for bm in self.benchmarks
        ]

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

        return {
            "active_benchmarks": active_benchmarks,
            "score_deltas": score_deltas,
            "score_spread": score_spread,
            "internal_validity": self._internal_validity,
            "saturation_states": saturation_states,
        }

    def _evaluate_introduction_trigger(self, round_num: int) -> Optional[str]:
        """Decide whether to introduce a new benchmark this round.

        Returns a trigger string if yes, None if no.

        Fixed mode (dynamic_evaluator=False):
            - Saturation trigger (bypasses cooldown with min gap of 1 round)
            - Periodic introduction every cooldown rounds

        Dynamic mode (dynamic_evaluator=True):
            - Saturation trigger (same as fixed)
            - Low internal validity (score-rank vs market-share-rank decoupled)
            - Fallback: periodic at 2x cooldown (ensures benchmarks are introduced
              even when signals are weak)
        """
        # --- Saturation trigger: checked BEFORE main cooldown in both modes ---
        saturation_trigger = None
        for bm in self.benchmarks:
            state = self._benchmark_saturation_state.get(bm.name)
            if state and state["saturated"] and state["cooldown_remaining"] <= 0:
                saturation_trigger = f"saturation:{bm.name}={state['max_score']:.4f}"
                break

        _saturation_min_gap = 1
        if saturation_trigger and round_num - self.last_introduction_round >= _saturation_min_gap:
            return saturation_trigger

        # --- Mode-specific triggers (subject to standard cooldown) ---
        if round_num - self.last_introduction_round < self.benchmark_introduction_cooldown:
            return None

        if not self.dynamic_evaluator:
            # Fixed schedule: periodic introduction
            if round_num > 0 and round_num % self.benchmark_introduction_cooldown == 0:
                return f"periodic_introduction:round_{round_num}"
            return None

        # Dynamic mode: signal-based triggers
        # Trigger 1: Low internal validity — scores decoupled from market reality
        if (self._internal_validity is not None
                and self._internal_validity < self._validity_threshold):
            return f"low_validity:{self._internal_validity:.3f}"

        # Trigger 2: Fallback periodic at 2x cooldown (ensure progress)
        fallback_cooldown = self.benchmark_introduction_cooldown * 2
        if round_num > 0 and round_num % fallback_cooldown == 0:
            return f"dynamic_fallback:round_{round_num}"

        return None

    def apply_llm_decision(self, decision: dict, round_num: int) -> Optional["Benchmark"]:
        """Apply an LLM evaluator decision to introduce a benchmark.

        Called by the simulation when dynamic_evaluator=True and llm_mode=True.
        Bypasses heuristic triggers — the LLM has already decided.

        Args:
            decision: {"action": "introduce_successor"|"introduce_fresh"|"none",
                       "target_benchmark": str}
            round_num: Current round

        Returns:
            New Benchmark if introduced, None otherwise
        """
        action = decision.get("action", "none")
        if action == "none":
            return None

        if len(self.benchmarks) >= self.max_benchmarks:
            return None

        if action == "introduce_successor":
            target = decision.get("target_benchmark", "")
            trigger = f"llm_successor:{target}"
        elif action == "introduce_fresh":
            trigger = "llm_fresh"
        else:
            return None

        return self._create_and_register_benchmark(round_num, trigger)

    def consider_new_benchmark(self, round_num: int) -> Optional[Benchmark]:
        """
        Consider introducing a new benchmark.

        Two modes controlled by `dynamic_evaluator`:
        - False (fixed schedule): periodic introduction every cooldown rounds,
          plus saturation-triggered replacement. Pulls from sequence in order.
        - True (signal-based): introduces when saturation, low validity, or
          coverage gap is detected. Sequence is a pool, not a fixed order.

        Returns:
            New Benchmark if introduced, None otherwise
        """
        # Check hard constraints (always apply)
        if len(self.benchmarks) >= self.max_benchmarks:
            return None

        # Check budget (if company mode)
        benchmark_cost = 50000.0
        if self.evaluator_as_company:
            if self.private_state.budget < benchmark_cost:
                return None

        trigger = self._evaluate_introduction_trigger(round_num)
        if trigger is None:
            return None

        return self._create_and_register_benchmark(round_num, trigger)

    def _create_and_register_benchmark(self, round_num: int, trigger: str) -> Optional[Benchmark]:
        """Create a new benchmark from sequence or auto-generate, and register it.

        Shared by consider_new_benchmark (heuristic) and apply_llm_decision (LLM).
        """
        benchmark_cost = 50000.0
        if self.evaluator_as_company:
            if self.private_state.budget < benchmark_cost:
                return None

        # Create new benchmark - use sequence if available, otherwise auto-generate
        if self.benchmark_sequence and self._sequence_index < len(self.benchmark_sequence):
            bm_config = self.benchmark_sequence[self._sequence_index]
            new_name = bm_config.get("name", f"benchmark_r{round_num}")
            new_bm = Benchmark(
                name=new_name,
                tags=bm_config.get("tags", ""),
                noise_level=bm_config.get("noise_level", 0.08),
            )
            if "weight" in bm_config:
                new_weight = bm_config["weight"]
            else:
                new_weight = sum(self.benchmark_weights.values()) / len(self.benchmark_weights)
            self._sequence_index += 1
        else:
            new_name = f"benchmark_r{round_num}"
            new_bm = Benchmark(
                name=new_name,
                noise_level=0.08,
            )
            new_weight = sum(self.benchmark_weights.values()) / len(self.benchmark_weights)

        # Register in evaluator state
        self.benchmarks.append(new_bm)
        self.benchmark_weights[new_name] = new_weight
        self.benchmark_score_history[new_name] = []
        self._best_published_scores[new_name] = {}

        self._benchmark_saturation_state[new_name] = {
            "saturated": False,
            "saturation_round": None,
            "cooldown_remaining": 0,
            "max_score": 0.0,
            "max_score_history": [],
            "perfect_score_hit": False,
        }

        # If triggered by saturation, reset the triggering benchmark's cooldown
        if trigger.startswith("saturation:"):
            trigger_bm_name = trigger.split(":")[1].split("=")[0]
            if trigger_bm_name in self._benchmark_saturation_state:
                self._benchmark_saturation_state[trigger_bm_name]["cooldown_remaining"] = (
                    self.benchmark_introduction_cooldown
                )

        self.last_introduction_round = round_num
        self.introduction_history.append({
            "round": round_num,
            "benchmark_name": new_name,
            "trigger": trigger,
        })

        if self.evaluator_as_company:
            self.private_state.budget -= benchmark_cost

        return new_bm

    def detect_saturation(self, round_num: int) -> list[str]:
        """
        Detect benchmarks that have been saturated (score deltas near zero).

        A benchmark is considered saturated when the max-score delta is below
        `saturation_delta_threshold` for `saturation_window` consecutive rounds.
        Perfect scores (>= 1.0) also trigger immediate saturation.

        Args:
            round_num: Current round number

        Returns:
            List of newly saturated benchmark names
        """
        newly_saturated = []

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

                    # Track max score history for delta computation
                    state["max_score_history"].append(max_score)

                    # Check for perfect score (1.000) — immediate saturation
                    if max_score >= 1.0:
                        state["perfect_score_hit"] = True
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
        evaluator.benchmark_introduction_cooldown = data.get("benchmark_introduction_cooldown", 8)
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

        return evaluator

    def __repr__(self):
        bm_names = ", ".join(bm.name for bm in self.benchmarks)
        return f"Evaluator(benchmarks=[{bm_names}])"
