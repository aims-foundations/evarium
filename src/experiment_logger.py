"""
Experiment Logger for Evaluation Ecosystem Simulation

Provides systematic logging of experiments with hybrid naming scheme:
    exp_<number>_<short_description>

Each experiment gets its own folder with:
    - config.json: Full configuration (reproducible)
    - history.json: Round-by-round data
    - summary.json: Final metrics
    - metadata.json: Description, tags, timestamp, etc.
    - plots/: Generated visualizations
    - providers/: Provider state snapshots
"""
import json
import os
import re
import subprocess
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional


@dataclass
class ExperimentMetadata:
    """Metadata for an experiment."""
    experiment_id: str
    name: str
    description: str = ""
    tags: list = field(default_factory=list)
    created_at: str = ""
    git_commit: str = ""
    seed: Optional[int] = None
    llm_mode: bool = False
    notes: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.git_commit:
            self.git_commit = self._get_git_commit()

    @staticmethod
    def _get_git_commit() -> str:
        """Try to get current git commit hash."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return ""


class ExperimentLogger:
    """
    Manages experiment logging with hybrid naming scheme.

    Usage:
        logger = ExperimentLogger("./experiments")
        exp_id = logger.create_experiment("baseline_heuristic",
                                          description="Initial baseline run",
                                          tags=["baseline", "heuristic"])

        # After running simulation:
        logger.log_config(config_dict)
        logger.log_history(history_list)
        logger.log_summary(summary_dict)
        logger.save_plots(fig, "overview.png")
        logger.finalize()
    """

    def __init__(self, base_dir: str = "./experiments", use_heuristic_subdir: bool = False):
        """
        Initialize ExperimentLogger.

        Args:
            base_dir: Base experiments directory
            use_heuristic_subdir: If True, uses experiments/_heuristic/ with separate numbering
        """
        self.base_experiments_dir = base_dir
        self.use_heuristic_subdir = use_heuristic_subdir

        # Set paths based on whether using heuristic subdir
        if use_heuristic_subdir:
            self.base_dir = os.path.join(base_dir, "_heuristic")
            self.index_file = os.path.join(self.base_dir, "heuristic_index.json")
            self.exp_prefix = "heur"
        else:
            self.base_dir = base_dir
            self.index_file = os.path.join(base_dir, "index.json")
            self.exp_prefix = "exp"

        self.current_experiment: Optional[str] = None
        self.current_metadata: Optional[ExperimentMetadata] = None

        # Ensure base directory exists
        os.makedirs(self.base_dir, exist_ok=True)

        # Load or create index
        self.index = self._load_index()

    def _load_index(self) -> dict:
        """Load experiment index or create empty one."""
        if os.path.exists(self.index_file):
            with open(self.index_file, "r") as f:
                return json.load(f)
        return {"experiments": [], "next_id": 1}

    def _save_index(self):
        """Save experiment index."""
        with open(self.index_file, "w") as f:
            json.dump(self.index, f, indent=2)

    def _sanitize_name(self, name: str) -> str:
        """Sanitize name for use in directory/file names."""
        # Replace spaces with underscores, remove special chars
        name = re.sub(r'[^\w\-]', '_', name.lower())
        # Remove consecutive underscores
        name = re.sub(r'_+', '_', name)
        # Trim length
        return name[:50].strip('_')

    def _get_next_id(self) -> int:
        """Get next experiment ID."""
        next_id = self.index["next_id"]
        self.index["next_id"] = next_id + 1
        return next_id

    def create_experiment(
        self,
        name: str,
        description: str = "",
        tags: list = None,
        seed: Optional[int] = None,
        llm_mode: bool = False,
    ) -> str:
        """
        Create a new experiment.

        Args:
            name: Short descriptive name (e.g., "baseline_heuristic")
            description: Longer description of the experiment
            tags: List of tags for filtering
            seed: Random seed used
            llm_mode: Whether LLM is used for planning

        Returns:
            Experiment ID (e.g., "exp_001_baseline_heuristic")
        """
        exp_num = self._get_next_id()
        sanitized_name = self._sanitize_name(name)
        experiment_id = f"{self.exp_prefix}_{exp_num:03d}_{sanitized_name}"

        # Create experiment directory
        exp_dir = os.path.join(self.base_dir, experiment_id)
        os.makedirs(exp_dir, exist_ok=True)
        os.makedirs(os.path.join(exp_dir, "plots"), exist_ok=True)
        os.makedirs(os.path.join(exp_dir, "providers"), exist_ok=True)

        # Create metadata
        self.current_metadata = ExperimentMetadata(
            experiment_id=experiment_id,
            name=name,
            description=description,
            tags=tags or [],
            seed=seed,
            llm_mode=llm_mode,
        )
        self.current_experiment = experiment_id

        # Save metadata
        self._save_metadata()

        # Add to index
        self.index["experiments"].append({
            "id": experiment_id,
            "name": name,
            "created_at": self.current_metadata.created_at,
            "tags": tags or [],
            "llm_mode": llm_mode,
        })
        self._save_index()

        print(f"Created experiment: {experiment_id}")
        return experiment_id

    def get_experiment_dir(self) -> str:
        """Get current experiment directory."""
        if not self.current_experiment:
            raise ValueError("No experiment created. Call create_experiment() first.")
        return os.path.join(self.base_dir, self.current_experiment)

    def _save_metadata(self):
        """Save current experiment metadata."""
        exp_dir = self.get_experiment_dir()
        with open(os.path.join(exp_dir, "metadata.json"), "w") as f:
            json.dump(asdict(self.current_metadata), f, indent=2)

    def log_config(self, config: dict):
        """Log experiment configuration."""
        exp_dir = self.get_experiment_dir()
        with open(os.path.join(exp_dir, "config.json"), "w") as f:
            json.dump(config, f, indent=2)

    def log_history(self, history: list):
        """Log simulation history (round-by-round data)."""
        exp_dir = self.get_experiment_dir()
        with open(os.path.join(exp_dir, "history.json"), "w") as f:
            json.dump(history, f, indent=2)

    def log_round(self, round_data: dict):
        """Append a single round's data to rounds.jsonl (incremental logging).

        This writes each round immediately so data is preserved even if the
        experiment crashes mid-run.
        """
        exp_dir = self.get_experiment_dir()
        with open(os.path.join(exp_dir, "rounds.jsonl"), "a") as f:
            f.write(json.dumps(round_data) + "\n")

    def log_summary(self, summary: dict):
        """Log experiment summary/final metrics."""
        exp_dir = self.get_experiment_dir()
        with open(os.path.join(exp_dir, "summary.json"), "w") as f:
            json.dump(summary, f, indent=2)

    def log_providers(self, providers: list):
        """Log provider final states."""
        exp_dir = self.get_experiment_dir()
        providers_dir = os.path.join(exp_dir, "providers")
        for provider in providers:
            provider.save(os.path.join(providers_dir, provider.name))

    def log_consumers(self, consumers):
        """Log consumer final states.

        Accepts either a list of Consumer objects (legacy) or a ConsumerMarket.
        """
        exp_dir = self.get_experiment_dir()
        consumers_dir = os.path.join(exp_dir, "consumers")
        os.makedirs(consumers_dir, exist_ok=True)

        # Handle ConsumerMarket (new format)
        from actors.consumer import ConsumerMarket
        if isinstance(consumers, ConsumerMarket):
            consumers.save(consumers_dir)
            return

        # Legacy: list of Consumer objects
        if isinstance(consumers, list):
            for consumer in consumers:
                consumer.save(os.path.join(consumers_dir, consumer.name))

    def log_policymakers(self, policymakers: list):
        """Log policymaker final states."""
        exp_dir = self.get_experiment_dir()
        policymakers_dir = os.path.join(exp_dir, "policymakers")
        os.makedirs(policymakers_dir, exist_ok=True)
        for policymaker in policymakers:
            policymaker.save(os.path.join(policymakers_dir, policymaker.name))

    def log_funders(self, funders: list):
        """Log funder final states."""
        exp_dir = self.get_experiment_dir()
        funders_dir = os.path.join(exp_dir, "funders")
        os.makedirs(funders_dir, exist_ok=True)
        for funder in funders:
            funder.save(os.path.join(funders_dir, funder.name))

    def log_ground_truth(self, ground_truth: dict):
        """Log ground truth data."""
        exp_dir = self.get_experiment_dir()
        ground_truth_data = {}
        for name, gt in ground_truth.items():
            ground_truth_data[name] = gt.to_dict()
        with open(os.path.join(exp_dir, "ground_truth.json"), "w") as f:
            json.dump(ground_truth_data, f, indent=2)

    def save_plot(self, fig, filename: str):
        """Save a matplotlib figure to the plots directory."""
        exp_dir = self.get_experiment_dir()
        plot_path = os.path.join(exp_dir, "plots", filename)
        fig.savefig(plot_path, dpi=150, bbox_inches="tight")
        return plot_path

    def save_game_log(self, content: str, filename: str = "game_log.md"):
        """
        Save game log markdown to experiment directory.

        Args:
            content: Markdown content to save
            filename: Output filename (default: game_log.md)

        Returns:
            Path to saved file
        """
        exp_dir = self.get_experiment_dir()
        log_path = os.path.join(exp_dir, filename)
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(content)
        return log_path

    def add_note(self, note: str):
        """Add a note to the experiment."""
        if self.current_metadata:
            if self.current_metadata.notes:
                self.current_metadata.notes += f"\n{note}"
            else:
                self.current_metadata.notes = note
            self._save_metadata()

    def finalize(self):
        """Finalize the experiment (update metadata with completion time)."""
        if self.current_metadata:
            self.add_note(f"Completed at: {datetime.now().isoformat()}")
            print(f"Experiment finalized: {self.current_experiment}")
            print(f"  Location: {self.get_experiment_dir()}")

    # --- Query/List Methods ---

    def list_experiments(self, tag: Optional[str] = None, llm_mode: Optional[bool] = None) -> list:
        """
        List experiments, optionally filtered by tag or llm_mode.

        Args:
            tag: Filter by tag
            llm_mode: Filter by LLM mode (True/False)

        Returns:
            List of experiment entries from index
        """
        experiments = self.index["experiments"]

        if tag:
            experiments = [e for e in experiments if tag in e.get("tags", [])]

        if llm_mode is not None:
            experiments = [e for e in experiments if e.get("llm_mode") == llm_mode]

        return experiments

    def load_experiment(self, experiment_id: str) -> dict:
        """
        Load all data from an experiment.

        Returns:
            Dict with keys: metadata, config, history, summary
        """
        exp_dir = os.path.join(self.base_dir, experiment_id)

        if not os.path.exists(exp_dir):
            raise ValueError(f"Experiment not found: {experiment_id}")

        data = {}

        for filename in ["metadata.json", "config.json", "history.json", "summary.json"]:
            filepath = os.path.join(exp_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, "r") as f:
                    key = filename.replace(".json", "")
                    data[key] = json.load(f)

        return data

    def get_latest_experiment(self) -> Optional[str]:
        """Get the ID of the most recent experiment."""
        if self.index["experiments"]:
            return self.index["experiments"][-1]["id"]
        return None

    def print_summary(self):
        """Print a summary of all experiments."""
        experiments = self.index["experiments"]

        if not experiments:
            print("No experiments logged yet.")
            return

        print(f"\n{'='*60}")
        print(f"Experiment Log ({len(experiments)} experiments)")
        print(f"{'='*60}")

        for exp in experiments:
            llm_str = "[LLM]" if exp.get("llm_mode") else "[Heuristic]"
            tags_str = f" [{', '.join(exp.get('tags', []))}]" if exp.get('tags') else ""
            print(f"  {exp['id']}: {exp['name']} {llm_str}{tags_str}")

        print(f"{'='*60}\n")


def generate_summary(
    history: list,
    evaluator,
    providers: list,
    consumers: list = None,
    policymakers: list = None,
    funders: list = None,
) -> dict:
    """
    Generate a summary dict from simulation results.

    Args:
        history: List of round data dicts
        evaluator: Evaluator instance
        providers: List of ModelProvider instances
        consumers: Optional list of Consumer instances
        policymakers: Optional list of Policymaker instances

    Returns:
        Summary dict with key metrics
    """
    if not history:
        return {}

    final = history[-1]

    # Compute Pearson-r(score_rank, market_share_rank) as validity proxy
    # Only possible when consumer market data is available in the final round
    validity_correlation = None
    final_market_shares = final.get("consumer_data", {}).get("market_shares", {}) if "consumer_data" in final else {}
    if final_market_shares and final.get("scores"):
        providers_in_both = [p for p in final["scores"] if p in final_market_shares]
        if len(providers_in_both) >= 2:
            scores_list = [final["scores"][p] for p in providers_in_both]
            shares_list = [final_market_shares[p] for p in providers_in_both]
            n = len(providers_in_both)
            score_ranks = sorted(range(n), key=lambda i: scores_list[i])
            share_ranks = sorted(range(n), key=lambda i: shares_list[i])
            sr = [score_ranks.index(i) for i in range(n)]
            mr = [share_ranks.index(i) for i in range(n)]
            sr_mean = sum(sr) / n
            mr_mean = sum(mr) / n
            num = sum((sr[i] - sr_mean) * (mr[i] - mr_mean) for i in range(n))
            denom = (sum((sr[i] - sr_mean) ** 2 for i in range(n)) *
                     sum((mr[i] - mr_mean) ** 2 for i in range(n))) ** 0.5
            validity_correlation = num / denom if denom > 0 else None

    # Per-benchmark params from evaluator state (noise_sigma, weight, n_active)
    benchmark_params = {
        bm.name: {"noise": bm.noise_level, "weight": evaluator.benchmark_weights.get(bm.name, 1.0)}
        for bm in evaluator.benchmarks
    }

    # Final capability vectors (6-dim per provider)
    final_cap_vecs = final.get("capability_vectors", {})

    summary = {
        "n_rounds": len(history),
        "final_scores": final["scores"],
        "final_capability_vectors": final_cap_vecs,
        "final_strategies": final["strategies"],
        "leaderboard": sorted(final["scores"].items(), key=lambda x: x[1], reverse=True),
        "validity_correlation": validity_correlation,
        "n_active_benchmarks": len(evaluator.benchmarks),
        "benchmark_params": benchmark_params,
        "provider_summaries": {},
    }

    # Per-provider summaries
    for provider in providers:
        name = provider.name
        # Only include rounds where this provider exists (startups enter mid-run)
        provider_history = [h for h in history if name in h.get("scores", {})]
        if not provider_history:
            continue
        scores = [h["scores"][name] for h in provider_history]

        # Capability vectors (6-dim dicts); compute mean for scalar summary
        def _cap_mean(cv):
            return sum(cv.values()) / len(cv) if cv else 0.0

        cap_vecs = [h.get("capability_vectors", {}).get(name, {}) for h in provider_history]
        initial_cap_vec = cap_vecs[0] if cap_vecs else {}
        final_cap_vec = final_cap_vecs.get(name, {})

        strategies = [h["strategies"][name] for h in provider_history]
        mean_score = sum(scores) / len(scores)

        summary["provider_summaries"][name] = {
            "initial_capability_vector": initial_cap_vec,
            "final_capability_vector": final_cap_vec,
            "initial_capability_mean": _cap_mean(initial_cap_vec),
            "final_capability_mean": _cap_mean(final_cap_vec),
            "capability_growth": _cap_mean(final_cap_vec) - _cap_mean(initial_cap_vec),
            "mean_score": mean_score,
            "score_std": (sum((s - mean_score) ** 2 for s in scores) / len(scores)) ** 0.5,
            "mean_rd": sum(s.get("rd", 0) for s in strategies) / len(strategies),
            "mean_safety": sum(s.get("safety", 0) for s in strategies) / len(strategies),
            "mean_product": sum(s.get("product", 0) for s in strategies) / len(strategies),
        }

    # Consumer summary
    if any("consumer_data" in h for h in history):
        consumer_rounds = [h for h in history if "consumer_data" in h]
        if consumer_rounds:
            avg_satisfactions = [
                h["consumer_data"].get("avg_satisfaction")
                for h in consumer_rounds
                if h["consumer_data"].get("avg_satisfaction") is not None
            ]
            avg_switching = sum(
                h["consumer_data"].get("switching_rate", 0) for h in consumer_rounds
            ) / len(consumer_rounds)

            final_cd = consumer_rounds[-1]["consumer_data"]
            consumer_summary = {
                "mean_satisfaction": sum(avg_satisfactions) / len(avg_satisfactions) if avg_satisfactions else None,
                "final_satisfaction": final_cd.get("avg_satisfaction"),
                "avg_switching_rate": avg_switching,
            }

            # Add market shares if available
            if "market_shares" in final_cd:
                consumer_summary["final_market_shares"] = final_cd["market_shares"]

            # Add segment count if available
            if "segment_data" in final_cd:
                consumer_summary["n_segments"] = len(final_cd["segment_data"])

            summary["consumer_summary"] = consumer_summary

    # Policymaker summary
    if policymakers and any("policymaker_data" in h for h in history):
        policymaker_rounds = [h for h in history if "policymaker_data" in h]
        if policymaker_rounds:
            interventions = []
            for h in policymaker_rounds:
                interventions.extend(h["policymaker_data"].get("interventions", []))

            summary["policymaker_summary"] = {
                "n_policymakers": len(policymakers),
                "total_interventions": len(interventions),
                "intervention_types": list(set(i["type"] for i in interventions if "type" in i)),
                "active_regulations": policymaker_rounds[-1]["policymaker_data"].get("active_regulations", []),
            }

    # Funder summary
    if funders and any("funder_data" in h for h in history):
        funder_rounds = [h for h in history if "funder_data" in h]
        if funder_rounds:
            final_funder_data = funder_rounds[-1]["funder_data"]

            # Calculate total funding over simulation
            total_funding = sum(
                h["funder_data"].get("total_funding", 0)
                for h in funder_rounds
            )

            # Get final funding multipliers
            final_multipliers = final_funder_data.get("funding_multipliers", {})

            summary["funder_summary"] = {
                "n_funders": len(funders),
                "total_funding_deployed": total_funding,
                "final_funding_multipliers": final_multipliers,
                "funder_types": [f.funder_type for f in funders] if hasattr(funders[0], 'funder_type') else [],
            }

    return summary


class DirectoryLogger:
    """
    Lightweight logger that writes to a specified directory path.

    Unlike ExperimentLogger, this does NOT:
    - Maintain index.json or sequential numbering
    - Generate experiment IDs

    Used for the deterministic-path output structure:
      output/validation/<phase>/<condition>/seeds/seed_N/
      output/core/<condition>/
    """

    def __init__(self, output_dir: str, lightweight: bool = False):
        """
        Args:
            output_dir: Absolute path to write artifacts into.
            lightweight: If True, skip heavy artifacts (history.json,
                game_log.md, plots/, providers/, funders/, policymakers/,
                consumers/, ground_truth.json).
        """
        self.output_dir = output_dir
        self.lightweight = lightweight
        os.makedirs(output_dir, exist_ok=True)

    def get_experiment_dir(self) -> str:
        return self.output_dir

    def save_metadata(self, seed=None, llm_mode=False, description=""):
        """Save metadata.json."""
        metadata = ExperimentMetadata(
            experiment_id=os.path.basename(self.output_dir),
            name=os.path.basename(self.output_dir),
            description=description,
            seed=seed,
            llm_mode=llm_mode,
        )
        with open(os.path.join(self.output_dir, "metadata.json"), "w") as f:
            json.dump(asdict(metadata), f, indent=2)

    def log_config(self, config: dict):
        with open(os.path.join(self.output_dir, "config.json"), "w") as f:
            json.dump(config, f, indent=2)

    def log_round(self, round_data: dict):
        with open(os.path.join(self.output_dir, "rounds.jsonl"), "a") as f:
            f.write(json.dumps(round_data) + "\n")

    def log_summary(self, summary: dict):
        with open(os.path.join(self.output_dir, "summary.json"), "w") as f:
            json.dump(summary, f, indent=2)

    def log_history(self, history: list):
        if self.lightweight:
            return
        with open(os.path.join(self.output_dir, "history.json"), "w") as f:
            json.dump(history, f, indent=2)

    def log_providers(self, providers: list):
        if self.lightweight:
            return
        providers_dir = os.path.join(self.output_dir, "providers")
        os.makedirs(providers_dir, exist_ok=True)
        for provider in providers:
            provider.save(os.path.join(providers_dir, provider.name))

    def log_consumers(self, consumers):
        if self.lightweight:
            return
        consumers_dir = os.path.join(self.output_dir, "consumers")
        os.makedirs(consumers_dir, exist_ok=True)
        from actors.consumer import ConsumerMarket
        if isinstance(consumers, ConsumerMarket):
            consumers.save(consumers_dir)
        elif isinstance(consumers, list):
            for c in consumers:
                c.save(os.path.join(consumers_dir, c.name))

    def log_policymakers(self, policymakers: list):
        if self.lightweight:
            return
        d = os.path.join(self.output_dir, "policymakers")
        os.makedirs(d, exist_ok=True)
        for p in policymakers:
            p.save(os.path.join(d, p.name))

    def log_funders(self, funders: list):
        if self.lightweight:
            return
        d = os.path.join(self.output_dir, "funders")
        os.makedirs(d, exist_ok=True)
        for f_ in funders:
            f_.save(os.path.join(d, f_.name))

    def log_ground_truth(self, ground_truth: dict):
        if self.lightweight:
            return
        gt_data = {name: gt.to_dict() for name, gt in ground_truth.items()}
        with open(os.path.join(self.output_dir, "ground_truth.json"), "w") as f:
            json.dump(gt_data, f, indent=2)

    def save_plot(self, fig, filename: str):
        if self.lightweight:
            return None
        plots_dir = os.path.join(self.output_dir, "plots")
        os.makedirs(plots_dir, exist_ok=True)
        path = os.path.join(plots_dir, filename)
        fig.savefig(path, dpi=150, bbox_inches="tight")
        return path

    def save_game_log(self, content: str, filename: str = "game_log.md"):
        if self.lightweight:
            return None
        path = os.path.join(self.output_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def add_note(self, note: str):
        pass

    def finalize(self):
        pass


if __name__ == "__main__":
    # Demo
    logger = ExperimentLogger("./experiments")
    logger.print_summary()
