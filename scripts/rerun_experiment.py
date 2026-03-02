"""
Rerun a past experiment from its saved config.json.

Usage:
    python rerun_experiment.py exp_016_5p_3b_full_ecosystem_ollama
    python rerun_experiment.py exp_016             # partial match
    python rerun_experiment.py exp_016 --seed 99  # different seed
    python rerun_experiment.py exp_016 --modify enable_incidents=True
    python rerun_experiment.py exp_016 --modify n_rounds=50 --modify seed=7
    python rerun_experiment.py --list              # list all experiments
"""
import os
import sys
import json
import time


def find_experiment(experiments_dir, query):
    """Find an experiment by exact or partial ID match."""
    index_path = os.path.join(experiments_dir, "index.json")
    if not os.path.exists(index_path):
        print("No experiments/index.json found.")
        sys.exit(1)

    with open(index_path) as f:
        index = json.load(f)

    matches = [
        e for e in index["experiments"]
        if e["id"] == query or e["id"].startswith(query)
    ]

    if len(matches) == 0:
        print(f"No experiment matching '{query}'.")
        print("Use --list to see all experiments.")
        sys.exit(1)
    elif len(matches) > 1:
        print(f"Multiple experiments match '{query}':")
        for m in matches:
            print(f"  {m['id']}")
        print("Be more specific.")
        sys.exit(1)

    return matches[0]


def list_experiments(experiments_dir):
    """Print all experiments."""
    index_path = os.path.join(experiments_dir, "index.json")
    if not os.path.exists(index_path):
        print("No experiments/index.json found.")
        return

    with open(index_path) as f:
        index = json.load(f)

    if not index["experiments"]:
        print("No experiments logged yet.")
        return

    print(f"\n{'='*70}")
    print(f"  Experiments ({len(index['experiments'])} total)")
    print(f"{'='*70}")
    for exp in index["experiments"]:
        llm = "[LLM]" if exp.get("llm_mode") else "[Heuristic]"
        tags = f" [{', '.join(exp.get('tags', []))}]" if exp.get("tags") else ""
        print(f"  {exp['id']}  {llm}{tags}")
    print(f"{'='*70}\n")


def _format_duration(seconds):
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        m, s = divmod(seconds, 60)
        return f"{int(m)}m {int(s)}s"
    else:
        h, remainder = divmod(seconds, 3600)
        m, s = divmod(remainder, 60)
        return f"{int(h)}h {int(m)}m {int(s)}s"


def _parse_modify_value(raw: str):
    """Parse a string value from --modify into a Python type."""
    if raw.lower() == "true":
        return True
    if raw.lower() == "false":
        return False
    if raw.lower() == "none":
        return None
    try:
        return int(raw)
    except ValueError:
        pass
    try:
        return float(raw)
    except ValueError:
        pass
    return raw  # Keep as string


def build_sim_config(config: dict, SimulationConfig) -> "SimulationConfig":
    """
    Build SimulationConfig dynamically from a saved config dict.

    Uses dataclass introspection so it automatically handles new fields
    added to SimulationConfig without needing manual updates here.

    - Ignores unknown keys in config (warns about them)
    - Uses dataclass defaults for fields missing from saved config (warns about them)
    """
    from dataclasses import fields as dc_fields

    valid_fields = {f.name: f for f in dc_fields(SimulationConfig)}

    # Find unknown keys (in saved config but not in SimulationConfig)
    non_config_keys = {"provider_configs", "funder_configs"}
    unknown_keys = [k for k in config if k not in valid_fields and k not in non_config_keys]
    if unknown_keys:
        print(f"  [Config] Ignoring unknown saved keys: {unknown_keys}")

    # Find missing keys (in SimulationConfig but not in saved config)
    missing_keys = [name for name in valid_fields if name not in config]
    if missing_keys:
        print(f"  [Config] Using current defaults for: {missing_keys}")

    # Build kwargs with only known valid fields
    kwargs = {k: v for k, v in config.items() if k in valid_fields}
    return SimulationConfig(**kwargs)


def run_from_config(config, source_exp_id):
    """Run a simulation from a saved config dict."""
    _PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(_PROJECT_ROOT, "src"))

    # Load .env file
    env_path = os.path.join(_PROJECT_ROOT, ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()

    # Set LLM provider if in LLM mode
    if config.get("llm_mode"):
        provider = os.environ.get("LLM_PROVIDER", "ollama")
        os.environ["LLM_PROVIDER"] = provider

    from simulation import EvalEcosystemSimulation, SimulationConfig
    from experiment_logger import ExperimentLogger, generate_summary
    from game_log import generate_game_log_from_history

    # Extract provider and funder configs (not part of SimulationConfig)
    provider_configs = config.pop("provider_configs", None)
    funder_configs = config.pop("funder_configs", None)

    if provider_configs is None:
        print("ERROR: config.json missing 'provider_configs'. Cannot rerun.")
        sys.exit(1)

    # Build SimulationConfig dynamically from saved params
    print("Building SimulationConfig from saved config:")
    sim_config = build_sim_config(config, SimulationConfig)

    n_rounds = sim_config.n_rounds
    n_funders = len(funder_configs) if funder_configs else 0

    # Print banner
    parts = [
        f"{len(provider_configs)} providers",
        f"{n_rounds} rounds",
        f"LLM" if sim_config.llm_mode else "heuristic",
    ]
    if sim_config.enable_consumers:
        parts.append(f"{sim_config.n_consumers} consumers")
    if sim_config.enable_policymakers:
        parts.append(f"{sim_config.n_policymakers} policymaker(s)")
    if sim_config.enable_funders:
        parts.append(f"{n_funders} funder(s)")

    print()
    print("=" * 70)
    print(f"RERUN of: {source_exp_id}")
    print(", ".join(parts))
    print("=" * 70)
    print()

    # Experiment logging
    experiments_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "experiments")
    logger = ExperimentLogger(experiments_dir)
    exp_id = logger.create_experiment(
        name=f"rerun_{source_exp_id}",
        description=f"Rerun of {source_exp_id}",
        tags=["rerun", source_exp_id],
        seed=sim_config.seed,
        llm_mode=sim_config.llm_mode,
    )

    # Log the full config (re-add provider/funder configs)
    full_config = sim_config.to_dict()
    full_config["provider_configs"] = provider_configs
    if funder_configs:
        full_config["funder_configs"] = funder_configs
    logger.log_config(full_config)

    print(f"Experiment: {exp_id}")
    print(f"Logging to: {logger.get_experiment_dir()}")
    print()

    # Run simulation
    sim = EvalEcosystemSimulation(sim_config)
    sim.setup(provider_configs=provider_configs, funder_configs=funder_configs)

    print(f"=== Running {n_rounds} rounds ===\n")

    start = time.time()
    round_times = []

    for i in range(n_rounds):
        round_start = time.time()

        elapsed = round_start - start
        if round_times:
            avg_round_time = sum(round_times) / len(round_times)
            remaining_rounds = n_rounds - i
            eta = avg_round_time * remaining_rounds
            print(f"[Round {i}/{n_rounds}] "
                  f"Elapsed: {_format_duration(elapsed)} | "
                  f"ETA: {_format_duration(eta)} | "
                  f"Avg/round: {_format_duration(avg_round_time)}")
        elif i == 0:
            print(f"[Round {i}/{n_rounds}] Starting...")

        round_data = sim.run_round()
        logger.log_round(round_data)

        round_elapsed = time.time() - round_start
        round_times.append(round_elapsed)

    sim._print_final_summary()

    total_elapsed = time.time() - start

    print()
    print("=" * 70)
    print(f"RERUN COMPLETE - Total time: {_format_duration(total_elapsed)}")
    if round_times:
        print(f"  Avg round: {_format_duration(sum(round_times) / len(round_times))}")
        print(f"  Fastest:   {_format_duration(min(round_times))}")
        print(f"  Slowest:   {_format_duration(max(round_times))}")
    print("=" * 70)

    # Log results
    logger.log_history(sim.history)
    logger.log_summary(generate_summary(
        sim.history,
        sim.evaluator,
        sim.providers,
        consumers=sim.consumers if sim_config.enable_consumers else None,
        policymakers=sim.policymakers if sim_config.enable_policymakers else None,
        funders=sim.funders if sim_config.enable_funders else None,
    ))
    logger.log_providers(sim.providers)
    logger.log_ground_truth(sim.ground_truth)

    if sim_config.enable_consumers and sim.consumers:
        logger.log_consumers(sim.consumers)
    if sim_config.enable_policymakers and sim.policymakers:
        logger.log_policymakers(sim.policymakers)
    if sim_config.enable_funders and sim.funders:
        logger.log_funders(sim.funders)

    # Game log
    benchmarks = full_config.get("benchmarks", [])
    game_log_content = generate_game_log_from_history(
        history=sim.history,
        providers=sim.providers,
        experiment_name=f"rerun_{source_exp_id}",
        experiment_id=exp_id,
        llm_mode=sim_config.llm_mode,
        benchmark_params={
            "validity": sim_config.benchmark_validity,
            "exploitability": sim_config.benchmark_exploitability,
            "noise": sim_config.benchmark_noise,
        },
        benchmarks=benchmarks,
        consumers=sim.consumers if sim_config.enable_consumers else None,
        policymakers=sim.policymakers if sim_config.enable_policymakers else None,
    )
    game_log_path = logger.save_game_log(game_log_content)
    print(f"Game log saved to: {game_log_path}")

    # Plots
    try:
        import matplotlib
        matplotlib.use('Agg')
        from plotting import create_all_dashboards

        plot_metadata = {
            "n_rounds": sim_config.n_rounds,
            "llm_mode": sim_config.llm_mode,
            "n_consumers": sim_config.n_consumers if sim_config.enable_consumers else 0,
            "n_policymakers": sim_config.n_policymakers if sim_config.enable_policymakers else 0,
            "n_funders": sim_config.n_funders if sim_config.enable_funders else 0,
        }
        plots_dir = os.path.join(logger.get_experiment_dir(), "plots")
        create_all_dashboards(sim.history, plots_dir, show=False, metadata=plot_metadata)
    except Exception as e:
        print(f"Could not create plots: {e}")

    # Finalize
    logger.add_note(f"Rerun of: {source_exp_id}")
    logger.add_note(f"Total runtime: {_format_duration(total_elapsed)}")
    if round_times:
        logger.add_note(f"Avg round time: {_format_duration(sum(round_times) / len(round_times))}")
    logger.finalize()

    print(f"\nExperiment saved to: {logger.get_experiment_dir()}")
    return sim, exp_id


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    if sys.argv[1] == "--list":
        experiments_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "experiments")
        list_experiments(experiments_dir)
        sys.exit(0)

    # Parse positional arg (experiment query) and optional flags
    query = sys.argv[1]
    args = sys.argv[2:]

    # Parse --modify key=value pairs and --seed override
    overrides = {}
    i = 0
    while i < len(args):
        if args[i] == "--modify" and i + 1 < len(args):
            pair = args[i + 1]
            if "=" not in pair:
                print(f"ERROR: --modify requires key=value format, got: {pair}")
                sys.exit(1)
            k, v = pair.split("=", 1)
            overrides[k.strip()] = _parse_modify_value(v.strip())
            i += 2
        elif args[i] == "--seed" and i + 1 < len(args):
            overrides["seed"] = int(args[i + 1])
            i += 2
        else:
            print(f"Unknown argument: {args[i]}")
            sys.exit(1)

    experiments_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "experiments")

    # Find the experiment
    exp_entry = find_experiment(experiments_dir, query)
    exp_id = exp_entry["id"]

    # Load its config
    config_path = os.path.join(experiments_dir, exp_id, "config.json")
    if not os.path.exists(config_path):
        print(f"ERROR: {config_path} not found. Cannot rerun without saved config.")
        sys.exit(1)

    with open(config_path) as f:
        config = json.load(f)

    # Apply overrides
    if overrides:
        print(f"Applying overrides: {overrides}")
        config.update(overrides)

    print(f"Loaded config from: {exp_id}")
    run_from_config(config, exp_id)
