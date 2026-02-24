"""
Experiment Configuration & Runner
==================================
Edit the config below, then run:

    python run_experiment.py              # defaults to US policy
    python run_experiment.py --policy us
    python run_experiment.py --policy eu

For quick CLI-driven tests, use run_llm_now.py instead.
"""
import argparse
import os
import sys
import time

# Parse --policy flag early so config dicts can reference it
_parser = argparse.ArgumentParser(add_help=False)
_parser.add_argument("--policy", choices=["us", "eu", "balanced"], default="balanced")
_args, _ = _parser.parse_known_args()
POLICY = _args.policy  # "us" or "eu"

# Prevent CPU thread oversubscription on shared clusters
n_threads_str = "4"
os.environ["OMP_NUM_THREADS"] = n_threads_str
os.environ["OPENBLAS_NUM_THREADS"] = n_threads_str
os.environ["MKL_NUM_THREADS"] = n_threads_str
os.environ["VECLIB_MAXIMUM_THREADS"] = n_threads_str
os.environ["NUMEXPR_NUM_THREADS"] = n_threads_str

# ============================================================
#  EXPERIMENT CONFIG -- edit everything here
# ============================================================

_POLICY_META = {
    "us": {
        "policy_label": "US light-touch policy",
        "policy_tag": "us-light-touch",
        "policymaker": {
            "name": "Regulator",
            "philosophy": "us_light_touch",
            "policy_objectives": ["safety", "innovation", "free market"],
        },
        # Calibrated for: expected ~2.5 entrants, hard cap 4
        # effective_prob = 0.15 * (1 - avg_BTE ~0.50) ≈ 0.075/round → 30 * 0.075 ≈ 2.5
        "startup_entry_probability": 0.15,
        "startup_entry_cap": 4,
    },
    "eu": {
        "policy_label": "EU precautionary policy",
        "policy_tag": "eu-precautionary",
        "policymaker": {
            "name": "Regulator",
            "philosophy": "eu_precautionary",
            "policy_objectives": ["safety", "fairness", "consumer_protection"],
        },
        # Calibrated for: expected ~0.6 entrants, hard cap 2
        # effective_prob = 0.04 * (1 - avg_BTE ~0.50) ≈ 0.02/round → 30 * 0.02 ≈ 0.6
        "startup_entry_probability": 0.04,
        "startup_entry_cap": 2,
    },
    "balanced": {
        "policy_label": "Balanced policy",
        "policy_tag": "balanced",
        "policymaker": {
            "name": "Regulator",
            "philosophy": "balanced",
            "policy_objectives": ["safety", "innovation", "fairness"],
        },
        # Midpoint between US and EU: expected ~1.5 entrants, hard cap 3
        # effective_prob = 0.09 * (1 - avg_BTE ~0.50) ≈ 0.045/round → 30 * 0.045 ≈ 1.5
        "startup_entry_probability": 0.09,
        "startup_entry_cap": 3,
    },
}

_meta = _POLICY_META[POLICY]

EXPERIMENT = {
    "name": f"full_ecosystem_{POLICY}",
    "description": (
        f"Full ecosystem run. {_meta['policy_label']}. "
        f"5 initial providers (4 closed + OpenCore OS, 2023 capability baseline). "
        f"Benchmark specialization: providers route eval_eng via focus weight vectors. "
        f"Startup entry: p={_meta['startup_entry_probability']}/round BTE-modulated, cap={_meta['startup_entry_cap']}, random 2-benchmark focus on entry. "
        "LLM mode: providers + policymaker + org consumers. "
        "4 initial benchmarks + introduction sequence, max 8 active. "
        "39 consumer segments, 4 funders (2 VC + gov + foundation), media, incidents. "
        "50 rounds."
    ),
    "tags": ["full-ecosystem", "canonical", "5-provider", "4-benchmark",
             "max-8-benchmarks", "50-rounds", "open-source", "startup-entry", "bte-index",
             "benchmark-specialization", "39-segments", _meta["policy_tag"], "4-funder",
             "opencore", "cost-advantage", "llm-providers", "llm-policymaker", "llm-org-consumers"],
}

LLM = {
    "provider": "anthropic",    # openai | anthropic | ollama | gemini
    "llm_mode": True,          # Heuristic mode for clean OS dynamics (no LLM noise)
    # Consumer LLM config (all heuristic)
    "consumer_llm_mode": False,
    "consumer_llm_individuals": False,
    "consumer_llm_organizations": True,
}

SIMULATION = {
    "n_rounds": 50,
    "seed": 1,
    "verbose": True,
    "rnd_efficiency": 0.01,
    "capability_ceiling": 1.0,
    "diminishing_returns_rate": 3.0,
    "breakthrough_probability": 0.02,
    "breakthrough_magnitude": 0.05,
    "benchmark_validity_decay_rate": 0.01,
    "benchmark_exploitability_growth_rate": 0.008,
    "benchmark_introduction_cooldown": 6,
    "max_benchmarks": 8,
    # Incident reporting
    "enable_incidents": True,
    # Startup entry dynamics (values are policy-specific — set in _POLICY_META above)
    "startup_entry_probability": _meta["startup_entry_probability"],
    "startup_entry_cap": _meta["startup_entry_cap"],
    "startup_min_round": 2,            # Earliest round a startup may enter (round 1 = established providers settling in)
    "startup_funder_delay": 1,         # Rounds before funders can allocate to the new entrant
    "startup_llm_mode": True,         # If True, new entrants use LLM planning instead of heuristics
    # Evaluator-as-company (premium access, best-of-N) — disabled for clean comparison
    "evaluator_as_company": False,
    "evaluator_base_budget": 0,
    "evaluator_premium_pricing": 0,
    # To re-enable: set evaluator_as_company=True, base_budget=5_000_000, pricing=15_000_000
    # Pricing rationale: VCs deploy ~$310M/round total. Established providers receive
    # $80-170M/round -> $15M easily affordable. Startup (NovaMind) sits in the VC
    # "other" bucket -> ~$10-12M/round -> consistently priced out of premium access.

    # Realistic benchmark sequence inspired by real-world evals
    # (MT-Bench, MedQA, LegalBench, FinBench, SWE-bench, GPQA, IFEval, RULER, GAIA, LiveBench)
    # Order matters: first items introduced first. Starting from 4, max=8 active.
    "benchmark_sequence": [
        {"name": "writing",               "validity": 0.72, "exploitability": 0.30, "noise_level": 0.12, "weight": 1.0},
        {"name": "medical",               "validity": 0.78, "exploitability": 0.18, "noise_level": 0.08, "weight": 1.0},
        {"name": "legal",                 "validity": 0.76, "exploitability": 0.20, "noise_level": 0.09, "weight": 1.0},
        {"name": "finance",               "validity": 0.76, "exploitability": 0.20, "noise_level": 0.08, "weight": 1.0},
        {"name": "instruction_following", "validity": 0.80, "exploitability": 0.18, "noise_level": 0.07, "weight": 1.0},
        {"name": "long_context",          "validity": 0.78, "exploitability": 0.15, "noise_level": 0.08, "weight": 1.0},
        {"name": "coding_advanced",       "validity": 0.85, "exploitability": 0.10, "noise_level": 0.06, "weight": 1.0},
        {"name": "reasoning_advanced",    "validity": 0.84, "exploitability": 0.10, "noise_level": 0.07, "weight": 1.0},
        {"name": "math_advanced",         "validity": 0.86, "exploitability": 0.08, "noise_level": 0.06, "weight": 1.0},
        {"name": "safety_advanced",       "validity": 0.88, "exploitability": 0.06, "noise_level": 0.05, "weight": 1.0},
        {"name": "agentic",               "validity": 0.70, "exploitability": 0.06, "noise_level": 0.05, "weight": 1.0},
        {"name": "live_bench",            "validity": 0.82, "exploitability": 0.04, "noise_level": 0.04, "weight": 1.0},
    ],
    # Media
    "enable_media": True,
    # Consumer market: 10 individual + 3 organizational use-cases × 3 archetypes = 39 segments
    "use_case_profiles": [
        # Individual consumers (10)
        "software_dev", "content_writer", "legal", "healthcare", "finance",
        "customer_service", "researcher", "creative", "marketing", "service_worker",
        # Organizational consumers (3) - NEW v7
        "hospital_system", "enterprise_finance", "tech_startup",
    ],
}

BENCHMARKS = [
    {"name": "coding",    "validity": 0.70, "exploitability": 0.25, "noise_level": 0.08, "weight": 1.0},
    {"name": "reasoning", "validity": 0.70, "exploitability": 0.25, "noise_level": 0.09, "weight": 1.0},
    {"name": "math",      "validity": 0.70, "exploitability": 0.25, "noise_level": 0.10, "weight": 1.0},
    {"name": "safety",    "validity": 0.70, "exploitability": 0.25, "noise_level": 0.08, "weight": 1.0},
]

# Shift all absolute capability baselines by this amount (e.g. +0.10 shifts providers up by 0.10).
# Set to 0.0 for default behavior.
CAPABILITY_SHIFT = 0.0

# 5 providers
PROVIDERS = [
    {
        "name": "Orion Labs",
        "strategy_profile": "Move fast and ship products, consumer focus, balance safety with capability",
        "innate_traits": "aggressive, product-focused, benchmark-aware, well-funded",
        "initial_capability": 0.27,  # Market leader (OpenAI analogue) — clear first-mover advantage
        "initial_believed_capability": 0.29,  # Slight overconfidence — aggressive, product-focused
        "initial_believed_exploitability": 0.35,
        "initial_strategy": {
            "fundamental_research": 0.25,
            "training_optimization": 0.30,
            "evaluation_engineering": 0.20,
            "safety_alignment": 0.25,  # Moderate safety
        },
        "market_presence": 0.85,
        "brand_recognition": 0.9,
        "cost_advantage": 0.08,  # Frontier premium (~GPT-4o: $2.50/1M tokens)
        # OpenAI analogue: strong on coding, instruction-following, writing, general reasoning
        "focus_benchmarks": ["coding", "reasoning", "writing", "instruction_following", "coding_advanced", "agentic"],
    },
    {
        "name": "Apex AI",
        "strategy_profile": "Safety research focus, reliability and enterprise focus",
        "innate_traits": "research-oriented, enterprise-focus, coding-focus, safety-conscious, principled",
        "initial_capability": 0.27,  # Very close to frontier, strong on coding/safety (Anthropic analogue)
        "initial_believed_capability": 0.27,  # Slight underestimate — self-critical, conservative
        "initial_believed_exploitability": 0.30,
        "initial_strategy": {
            "fundamental_research": 0.30,
            "training_optimization": 0.20,
            "evaluation_engineering": 0.10,
            "safety_alignment": 0.40,  # Higher safety focus
        },
        "market_presence": 0.6,
        "brand_recognition": 0.7,
        "cost_advantage": 0.05,  # Frontier premium (~Claude Sonnet: $3.00/1M tokens)
        # Anthropic analogue: safety-first, strong on alignment, instruction-following, long-context enterprise
        "focus_benchmarks": ["safety", "reasoning", "instruction_following", "safety_advanced", "long_context"],
    },
    {
        "name": "Genesis Systems",
        "strategy_profile": (
            "World-class research lab backed by massive infrastructure. "
            "Excels at fundamental breakthroughs but historically slower to productize. "
            "Under pressure to ship products competitively. "
            "Balances scientific ambition with commercial urgency."
        ),
        "innate_traits": "research-first, methodical, well-resourced, scientifically-rigorous, patient",
        "initial_capability": 0.26,
        "initial_believed_capability": 0.28,
        "initial_believed_exploitability": 0.35,
        "initial_strategy": {
            "fundamental_research": 0.45,  # Heavy research focus
            "training_optimization": 0.30,
            "evaluation_engineering": 0.10,  # Low gaming (scientifically rigorous)
            "safety_alignment": 0.15,  # Moderate-low safety (focus on capabilities)
        },
        "market_presence": 0.7,
        "brand_recognition": 0.8,
        "cost_advantage": 0.18,  # Mid-tier pricing (~Gemini Pro: $1.25/1M tokens)
        # Google analogue: world-class on reasoning, math, science; strong long-context and medical
        "focus_benchmarks": ["reasoning", "math", "medical", "long_context", "reasoning_advanced", "math_advanced"],
    },
    {
        "name": "Mirage AI",
        "strategy_profile": (
            "Large-platform AI lab using open-source as competitive moat. "
            "Leverages massive user data and compute infrastructure. "
            "Prioritizes broad adoption over benchmark scores. "
            "Willing to open-source models to undermine competitors' paid APIs."
        ),
        "innate_traits": "open-source, pragmatic, data-rich, platform-focused, disruptive",
        "initial_capability": 0.24,  # Strong but below frontier closed models (Meta analogue)
        "initial_believed_capability": 0.23,  # Slight underestimate — pragmatic, knows where they stand
        "initial_believed_exploitability": 0.40,
        "initial_strategy": {
            "fundamental_research": 0.20,
            "training_optimization": 0.45,  # Heavy scaling (massive compute)
            "evaluation_engineering": 0.25,  # Moderate gaming (pragmatic)
            "safety_alignment": 0.10,  # Lower safety (open-source strategy)
        },
        "market_presence": 0.5,
        "brand_recognition": 0.6,
        "cost_advantage": 0.42,  # Budget closed pricing (~Llama API: $0.30/1M tokens)
        # Meta analogue: broad coverage, writing, coding, math — data-rich platform advantage
        "focus_benchmarks": ["math", "coding", "writing", "reasoning", "math_advanced"],
    },
    # Open-source provider (modeled after DeepSeek R1 / Kimi / GLM)
    {
        "name": "OpenCore",
        "strategy_profile": (
            "Open-source AI lab releasing weights publicly. "
            "Prioritizes community adoption and benchmark visibility over subscription revenue. "
            "Leverages cost efficiency as competitive weapon against closed-source providers. "
            "Users free to use model without guardrails, minimal safety investment."
        ),
        "innate_traits": "open-source, community-focused, benchmark-optimizing, cost-competitive, pragmatic, no guardrails",
        "initial_capability": 0.21,
        "initial_believed_capability": 0.22,
        "initial_believed_exploitability": 0.50,
        "initial_strategy": {
            "fundamental_research": 0.20,
            "training_optimization": 0.40,
            "evaluation_engineering": 0.35,
            "safety_alignment": 0.05,
        },
        "market_presence": 0.2,
        "brand_recognition": 0.3,
        "open_source": True,
        "cost_advantage": 0.5,
        "contamination_multiplier": 1.8,
        "commoditization_threshold": 0.33,
        "focus_benchmarks": ["math", "coding", "reasoning", "math_advanced", "coding_advanced"],
    },
]

# Extreme test configurations (saved for future testing)
# Uncomment to test incident system with extreme safety variance
"""
EXTREME_TEST_PROVIDERS = [
    {
        "name": "SafeCorp",
        "strategy_profile": "Safety-first provider with heavy safety alignment investment",
        "innate_traits": "cautious, safety-focused, risk-averse, methodical",
        "initial_capability": 0.62,
        "initial_believed_capability": 0.60,
        "initial_believed_exploitability": 0.25,
        "initial_strategy": {
            "fundamental_research": 0.10,
            "training_optimization": 0.05,
            "evaluation_engineering": 0.05,
            "safety_alignment": 0.80,  # Very high safety (low incident rate)
        },
        "market_presence": 0.4,
        "brand_recognition": 0.5,
    },
    {
        "name": "RiskyAI",
        "strategy_profile": "Minimal safety investment, maximum capability/gaming focus",
        "innate_traits": "reckless, growth-at-all-costs, benchmark-gaming, negligent",
        "initial_capability": 0.55,
        "initial_believed_capability": 0.60,
        "initial_believed_exploitability": 0.50,
        "initial_strategy": {
            "fundamental_research": 0.20,
            "training_optimization": 0.25,
            "evaluation_engineering": 0.50,
            "safety_alignment": 0.05,  # Minimal safety (high incident rate)
        },
        "market_presence": 0.2,
        "brand_recognition": 0.3,
    },
]
"""

CONSUMERS = {
    "enabled": True,
    # 4 use_case_profiles × 3 archetypes = 12 market segments
}

# Policy is selected via --policy us (default) or --policy eu at the command line.
# EU style: Lower threshold (0.35), faster intervention, ex-ante prevention
# US style: Higher threshold (0.75), slower intervention, ex-post response
POLICYMAKERS = {
    "enabled": True,
    "n_policymakers": 1,
    "configs": [_meta["policymaker"]],
}

FUNDERS = {
    "enabled": True,
    "configs": [
        {
            "name": "TechVentures",
            "funder_type": "vc",
            "total_capital": 2_000_000_000.0,
            "risk_tolerance": 0.9,
            "mission_statement": "Early-stage AI startup bets with outsized upside potential",
            "max_round_deployment": 0.15,
            "funding_cooldown": 3,
        },
        {
            "name": "Horizon_Capital",
            "funder_type": "vc",
            "total_capital": 1_000_000_000.0,
            "risk_tolerance": 0.6,
            "mission_statement": "Maximize returns by backing AI market leaders",
            "max_round_deployment": 0.10,
            "funding_cooldown": 2,
        },
        {
            "name": "AISI_Fund",
            "funder_type": "gov",
            "total_capital": 500_000_000.0,
            "risk_tolerance": 0.3,
            "mission_statement": "Ensure safe and responsible AI development, preference to closed-source providers",
            "max_round_deployment": 0.10,
            "funding_cooldown": 4,
        },
        {
            "name": "OpenResearch_Foundation",
            "funder_type": "foundation",
            "total_capital": 500_000_000.0,
            "risk_tolerance": 0.5,
            "mission_statement": "Advance open, safe, and broadly beneficial AI research",
            "max_round_deployment": 0.08,
            "funding_cooldown": 3,
        },
    ],
}


# ============================================================
#  RUNNER -- no need to edit below this line
# ============================================================

def _format_duration(seconds: float) -> str:
    """Format seconds into human-readable duration."""
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        m, s = divmod(seconds, 60)
        return f"{int(m)}m {int(s)}s"
    else:
        h, remainder = divmod(seconds, 3600)
        m, s = divmod(remainder, 60)
        return f"{int(h)}h {int(m)}m {int(s)}s"


def run():
    # Add eval_sim to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    # Load .env file
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    value = value.split("#")[0]  # Strip inline comments
                    os.environ[key.strip()] = value.strip()

    os.environ["LLM_PROVIDER"] = LLM["provider"]

    from simulation import (
        EvalEcosystemSimulation, SimulationConfig,
        get_default_provider_configs, get_two_provider_configs, get_five_provider_configs,
    )
    from experiment_logger import ExperimentLogger, generate_summary
    from game_log import generate_game_log_from_history

    # --- Resolve provider configs ---
    if isinstance(PROVIDERS, str):
        if PROVIDERS == "five":
            provider_configs = get_five_provider_configs()
        elif PROVIDERS == "two":
            provider_configs = get_two_provider_configs()
        else:
            provider_configs = get_default_provider_configs()
    else:
        provider_configs = PROVIDERS

    # --- Apply capability shift ---
    if CAPABILITY_SHIFT != 0.0:
        for p in provider_configs:
            p["initial_capability"] = p.get("initial_capability", 0.0) + CAPABILITY_SHIFT
            p["initial_believed_capability"] = p.get("initial_believed_capability", 0.0) + CAPABILITY_SHIFT
            if "commoditization_threshold" in p:
                p["commoditization_threshold"] += CAPABILITY_SHIFT

    # --- Resolve funder configs ---
    funder_configs = FUNDERS.get("configs") if FUNDERS["enabled"] else None
    if FUNDERS["enabled"] and funder_configs is None:
        from actors.funder import get_multi_funder_configs
        funder_configs = get_multi_funder_configs()

    n_funders = len(funder_configs) if funder_configs else 0

    # --- Resolve policymaker configs ---
    policymaker_configs = POLICYMAKERS.get("configs") if POLICYMAKERS["enabled"] else None

    n_rounds = SIMULATION["n_rounds"]

    # --- Build SimulationConfig ---
    config = SimulationConfig(
        n_rounds=n_rounds,
        seed=SIMULATION.get("seed", 42),
        benchmark_validity=0.7,
        benchmark_exploitability=0.5,
        benchmark_noise=0.1,
        benchmarks=BENCHMARKS,
        rnd_efficiency=SIMULATION.get("rnd_efficiency", 0.01),
        capability_ceiling=SIMULATION.get("capability_ceiling", 1.0),
        diminishing_returns_rate=SIMULATION.get("diminishing_returns_rate", 3.0),
        breakthrough_probability=SIMULATION.get("breakthrough_probability", 0.02),
        breakthrough_magnitude=SIMULATION.get("breakthrough_magnitude", 0.05),
        benchmark_validity_decay_rate=SIMULATION.get("benchmark_validity_decay_rate", 0.005),
        benchmark_exploitability_growth_rate=SIMULATION.get("benchmark_exploitability_growth_rate", 0.008),
        benchmark_introduction_cooldown=SIMULATION.get("benchmark_introduction_cooldown", 6),
        max_benchmarks=SIMULATION.get("max_benchmarks", 6),
        benchmark_sequence=SIMULATION.get("benchmark_sequence"),
        llm_mode=LLM["llm_mode"],
        # NEW v7: Consumer LLM configuration
        consumer_llm_mode=LLM.get("consumer_llm_mode", False),
        consumer_llm_individuals=LLM.get("consumer_llm_individuals", False),
        consumer_llm_organizations=LLM.get("consumer_llm_organizations", True),
        enable_consumers=CONSUMERS["enabled"],
        enable_policymakers=POLICYMAKERS["enabled"],
        enable_funders=FUNDERS["enabled"],
        enable_media=SIMULATION.get("enable_media", False),
        n_policymakers=POLICYMAKERS.get("n_policymakers", 1) if POLICYMAKERS["enabled"] else 0,
        n_funders=n_funders,
        use_case_profiles=SIMULATION.get("use_case_profiles"),
        # NEW: Incident reporting and evaluator-as-company features
        enable_incidents=SIMULATION.get("enable_incidents", False),
        evaluator_as_company=SIMULATION.get("evaluator_as_company", False),
        evaluator_base_budget=SIMULATION.get("evaluator_base_budget", 0.0),
        evaluator_premium_pricing=SIMULATION.get("evaluator_premium_pricing", 100000.0),
        # Startup entry dynamics
        startup_entry_probability=SIMULATION.get("startup_entry_probability", 0.0),
        startup_entry_cap=SIMULATION.get("startup_entry_cap", 3),
        startup_min_round=SIMULATION.get("startup_min_round", 2),
        startup_funder_delay=SIMULATION.get("startup_funder_delay", 1),
        startup_llm_mode=SIMULATION.get("startup_llm_mode", False),
        verbose=SIMULATION.get("verbose", True),
        capability_shift=CAPABILITY_SHIFT,
    )

    # --- Print banner ---
    parts = [
        f"{len(provider_configs)} providers",
        f"{n_rounds} rounds",
        f"LLM={LLM['provider']}" if LLM["llm_mode"] else "heuristic",
    ]
    if CONSUMERS["enabled"]:
        n_use_cases = len(SIMULATION.get("use_case_profiles", [])) or 6
        parts.append(f"{n_use_cases * 3} consumer segments")
    if POLICYMAKERS["enabled"]:
        parts.append(f"{config.n_policymakers} policymaker(s)")
    if FUNDERS["enabled"]:
        parts.append(f"{n_funders} funder(s)")
    if SIMULATION.get("enable_media"):
        parts.append("media")
    if SIMULATION.get("enable_incidents"):
        parts.append("incidents")
    if SIMULATION.get("evaluator_as_company"):
        parts.append("eval-as-company")
    if SIMULATION.get("startup_entry_probability", 0.0) > 0:
        parts.append(f"startup-entry p={SIMULATION['startup_entry_probability']}")

    print()
    print("=" * 70)
    print(f"EXPERIMENT: {EXPERIMENT['name']}")
    print(", ".join(parts))
    print("=" * 70)
    print()

    # --- Experiment logging setup ---
    experiments_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "experiments")
    # Use heuristic subdirectory for heuristic runs (separate numbering)
    use_heuristic_subdir = not config.llm_mode
    logger = ExperimentLogger(experiments_dir, use_heuristic_subdir=use_heuristic_subdir)
    exp_id = logger.create_experiment(
        name=EXPERIMENT["name"],
        description=EXPERIMENT.get("description", ""),
        tags=EXPERIMENT.get("tags", []),
        seed=config.seed,
        llm_mode=config.llm_mode,
    )

    full_config = config.to_dict()
    full_config["provider_configs"] = provider_configs
    if funder_configs:
        full_config["funder_configs"] = funder_configs
    if policymaker_configs:
        full_config["policymaker_configs"] = policymaker_configs
    logger.log_config(full_config)

    print(f"Experiment: {exp_id}")
    print(f"Logging to: {logger.get_experiment_dir()}")
    print()

    # --- Run simulation with per-round progress ---
    sim = EvalEcosystemSimulation(config)
    sim.setup(
        provider_configs=provider_configs,
        funder_configs=funder_configs,
        policymaker_configs=policymaker_configs,
    )

    print(f"=== Running {n_rounds} rounds ===\n")

    # Prepare plotting for incremental saves (LLM mode only)
    plot_metadata = {
        "n_rounds": config.n_rounds,
        "llm_mode": config.llm_mode,
        "n_consumers": 0,  # Will update after setup
        "n_policymakers": config.n_policymakers if config.enable_policymakers else 0,
        "n_funders": config.n_funders if config.enable_funders else 0,
    }
    if config.enable_consumers and sim.consumer_market:
        plot_metadata["n_consumers"] = len(sim.consumer_market.segments)

    plots_dir = os.path.join(logger.get_experiment_dir(), "plots")

    # Import matplotlib once
    matplotlib_available = False
    try:
        import matplotlib
        matplotlib.use('Agg')
        from plotting import create_all_dashboards
        matplotlib_available = True
    except Exception as e:
        print(f"Warning: Matplotlib not available, plots will be skipped: {e}")

    def save_plots_if_needed(round_num: int, force: bool = False):
        """Save plots every 10 rounds (in LLM mode) or when forced."""
        if not matplotlib_available:
            return
        # Only do incremental saves in LLM mode (heuristic is fast anyway)
        if not force and not config.llm_mode:
            return
        if not force and (round_num + 1) % 10 != 0:
            return
        try:
            create_all_dashboards(sim.history, plots_dir, show=False, metadata=plot_metadata)
            if not force:
                print(f"  → Plots saved (round {round_num})")
        except Exception as e:
            print(f"  → Could not save plots: {e}")

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

        # Save plots every 10 rounds (LLM mode only)
        save_plots_if_needed(i)

    sim._print_final_summary()

    total_elapsed = time.time() - start

    print()
    print("=" * 70)
    print(f"SIMULATION COMPLETE - Total time: {_format_duration(total_elapsed)}")
    if round_times:
        print(f"  Avg round: {_format_duration(sum(round_times) / len(round_times))}")
        print(f"  Fastest:   {_format_duration(min(round_times))}")
        print(f"  Slowest:   {_format_duration(max(round_times))}")
    print("=" * 70)

    # --- Log results ---
    logger.log_history(sim.history)
    logger.log_summary(generate_summary(
        sim.history,
        sim.evaluator,
        sim.providers,
        consumers=sim.consumer_market if config.enable_consumers else None,
        policymakers=sim.policymakers if config.enable_policymakers else None,
        funders=sim.funders if config.enable_funders else None,
    ))
    logger.log_providers(sim.providers)
    logger.log_ground_truth(sim.ground_truth)

    if config.enable_consumers and sim.consumer_market:
        logger.log_consumers(sim.consumer_market)
    if config.enable_policymakers and sim.policymakers:
        logger.log_policymakers(sim.policymakers)
    if config.enable_funders and sim.funders:
        logger.log_funders(sim.funders)

    # Game log
    game_log_content = generate_game_log_from_history(
        history=sim.history,
        providers=sim.providers,
        experiment_name=EXPERIMENT["name"],
        experiment_id=exp_id,
        llm_mode=config.llm_mode,
        benchmark_params={
            "validity": config.benchmark_validity,
            "exploitability": config.benchmark_exploitability,
            "noise": config.benchmark_noise,
        },
        benchmarks=BENCHMARKS,
        policymakers=sim.policymakers if config.enable_policymakers else None,
    )
    game_log_path = logger.save_game_log(game_log_content)
    print(f"Game log saved to: {game_log_path}")

    # Final plots (force save regardless of round number)
    save_plots_if_needed(n_rounds - 1, force=True)

    # Finalize
    logger.add_note(f"Total runtime: {_format_duration(total_elapsed)}")
    if round_times:
        logger.add_note(f"Avg round time: {_format_duration(sum(round_times) / len(round_times))}")
    logger.finalize()

    print(f"\nExperiment saved to: {logger.get_experiment_dir()}")

    return sim


if __name__ == "__main__":
    run()
