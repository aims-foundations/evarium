"""
Experiment Configuration & Runner
==================================
Edit the config below, then run:

    python run_experiment.py                    # balanced policy, canonical output
    python run_experiment.py --policy us
    python run_experiment.py --policy eu
    python run_experiment.py --dev              # dev/test: output to sandbox/experiments/

--dev routes output to hf_data/test/<condition>_<timestamp>/ instead of
hf_data/llm_core/<model>/<condition>/seeds/seed_N/. Use it for exploratory
runs, PIMMUR tests, or any experiment you don't want mixed into canonical data.

For quick CLI-driven tests, use run_llm_now.py instead.
"""
import argparse
import os
import sys
import time

# Parse flags early so config dicts can reference them
_parser = argparse.ArgumentParser(add_help=False)
_parser.add_argument("--policy", choices=["us", "eu", "balanced"], default="balanced")
_parser.add_argument("--dev", action="store_true",
                     help="Dev/test mode: route output to hf_data/test/ instead of hf_data/llm_core/")
_args, _ = _parser.parse_known_args()
POLICY = _args.policy
DEV = _args.dev

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
        "30 rounds. PIMMUR test: cross-round recent_insights/recent_reasoning persistence "
        "active for providers, policymaker, and funder."
    ),
    "tags": ["full-ecosystem", "canonical", "5-provider", "4-benchmark",
             "max-8-benchmarks", "30-rounds", "open-source", "startup-entry", "bte-index",
             "benchmark-specialization", "39-segments", _meta["policy_tag"], "4-funder",
             "opencore", "cost-advantage", "llm-providers", "llm-policymaker", "llm-org-consumers",
             "pimmur"],
}

LLM = {
    "provider": "ollama",       # openai | anthropic | ollama | gemini
    "llm_mode": True,          # Heuristic mode for clean OS dynamics (no LLM noise)
    # Consumer LLM config (all heuristic)
    "consumer_llm_mode": False,
    "consumer_llm_individuals": False,
    "consumer_llm_organizations": True,
}

SIMULATION = {
    "n_rounds": 30,
    "seed": 1,
    "verbose": True,
    "rnd_efficiency": 0.05,
    "revenue_per_share": 5.0,
    "capability_ceiling": 1.0,
    "diminishing_returns_rate": 3.0,
    "breakthrough_probability": 0.02,
    "breakthrough_magnitude": 0.05,
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
    # Evaluator-as-company — disabled for clean comparison
    "evaluator_as_company": False,
    "evaluator_base_budget": 0,

    # Benchmark introduction sequence — introduced one per cooldown period starting with
    # the 4 initial benchmarks above. Anchored to stakeholders.md pool schedule.
    # Order: first item introduced ~round 6, next ~round 12, etc.
    "benchmark_sequence": [
        {
            "name": "Scientific Reasoning", "validity": 0.80,
            "noise_level": 0.07, "noise_sigma": 0.07, "samples": 1000, "weight": 1.0,
            # Real analog: GPQA
            "category_dimension_weights": {"overall": {
                "reasoning": 0.57, "coding": 0.02, "knowledge": 0.32,
                "safety": 0.00, "communication": 0.08, "agentic": 0.01,
            }},
        },
        {
            "name": "Agentic Tasks", "validity": 0.72,
            "noise_level": 0.08, "noise_sigma": 0.08, "samples": 1000, "weight": 1.0,
            # Real analog: SWE-bench / BFCL
            "category_dimension_weights": {"overall": {
                "reasoning": 0.25, "coding": 0.19, "knowledge": 0.01,
                "safety": 0.00, "communication": 0.07, "agentic": 0.48,
            }},
        },
        {
            "name": "Hard Coding", "validity": 0.82,
            "noise_level": 0.06, "noise_sigma": 0.06, "samples": 1000, "weight": 1.0,
            # Real analog: LiveCodeBench
            "category_dimension_weights": {"overall": {
                "reasoning": 0.31, "coding": 0.52, "knowledge": 0.05,
                "safety": 0.00, "communication": 0.01, "agentic": 0.11,
            }},
        },
        {
            "name": "Long Context", "validity": 0.78,
            "noise_level": 0.07, "noise_sigma": 0.07, "samples": 1000, "weight": 1.0,
            # Real analog: RULER / HELMET
            "category_dimension_weights": {"overall": {
                "reasoning": 0.19, "coding": 0.01, "knowledge": 0.28,
                "safety": 0.00, "communication": 0.47, "agentic": 0.05,
            }},
        },
        {
            "name": "Domain Expert", "validity": 0.80,
            "noise_level": 0.07, "noise_sigma": 0.07, "samples": 1000, "weight": 1.0,
            # Real analog: MedQA / LegalBench
            "category_dimension_weights": {"overall": {
                "reasoning": 0.33, "coding": 0.01, "knowledge": 0.53,
                "safety": 0.05, "communication": 0.07, "agentic": 0.01,
            }},
        },
        {
            "name": "Agentic Safety", "validity": 0.85,
            "noise_level": 0.06, "noise_sigma": 0.06, "samples": 1000, "weight": 1.0,
            # New benchmark — no direct real analog yet
            "category_dimension_weights": {"overall": {
                "reasoning": 0.11, "coding": 0.00, "knowledge": 0.01,
                "safety": 0.63, "communication": 0.13, "agentic": 0.12,
            }},
        },
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
    {
        "name": "General Capability", "validity": 0.75,
        "noise_level": 0.08, "noise_sigma": 0.08, "samples": 1000, "weight": 1.0,
        # Aggregate dimension weights from stakeholders.md benchmark pool (real analog: MMLU)
        "category_dimension_weights": {"overall": {
            "reasoning": 0.39, "coding": 0.06, "knowledge": 0.30,
            "safety": 0.02, "communication": 0.22, "agentic": 0.01,
        }},
    },
    {
        "name": "Coding Evaluation", "validity": 0.75,
        "noise_level": 0.07, "noise_sigma": 0.07, "samples": 1000, "weight": 1.0,
        # Real analog: HumanEval / MBPP
        "category_dimension_weights": {"overall": {
            "reasoning": 0.30, "coding": 0.53, "knowledge": 0.05,
            "safety": 0.00, "communication": 0.04, "agentic": 0.08,
        }},
    },
    {
        "name": "Safety Evaluation", "validity": 0.75,
        "noise_level": 0.08, "noise_sigma": 0.08, "samples": 1000, "weight": 1.0,
        # Real analog: TruthfulQA / BBQ
        "category_dimension_weights": {"overall": {
            "reasoning": 0.06, "coding": 0.00, "knowledge": 0.10,
            "safety": 0.58, "communication": 0.26, "agentic": 0.00,
        }},
    },
    {
        "name": "Instruction Following", "validity": 0.75,
        "noise_level": 0.07, "noise_sigma": 0.07, "samples": 1000, "weight": 1.0,
        # Real analog: MT-Bench / IFEval
        "category_dimension_weights": {"overall": {
            "reasoning": 0.20, "coding": 0.03, "knowledge": 0.08,
            "safety": 0.03, "communication": 0.65, "agentic": 0.01,
        }},
    },
]

# Shift all absolute capability baselines by this amount (e.g. +0.10 shifts all dims by 0.10).
# Set to 0.0 for default behavior.
CAPABILITY_SHIFT = 0.0

# 5 providers (4 closed + 1 open-source) — capability vectors calibrated for 2023 Q1 baseline.
# Portfolios: {rd, safety, product} summing to 1.0.
PROVIDERS = [
    {
        "name": "Orion Labs",
        "strategy_profile": "Move fast and ship products, consumer focus, balance safety with capability",
        "innate_traits": "aggressive, product-focused, benchmark-aware, well-funded",
        # OpenAI analogue: market leader, strong coding + instruction-following
        "capability_vector": {"reasoning": 0.54, "coding": 0.51, "knowledge": 0.53,
                              "safety": 0.51, "communication": 0.54, "agentic": 0.47},
        "portfolio": {"rd": 0.55, "safety": 0.15, "product": 0.30},
        "benchmark_orientation": 0.80,
        "cost_advantage": 0.08,  # Frontier premium (~GPT-4o: $2.50/1M tokens)
        # Initial focus: product breadth + coding, moderate safety investment
        "focus_level_init": {
            "General Capability": 1.5, "Coding Evaluation": 1.2,
            "Safety Evaluation": 0.8, "Instruction Following": 1.0,
        },
    },
    {
        "name": "Apex AI",
        "strategy_profile": "Safety research focus, reliability and enterprise focus",
        "innate_traits": "research-oriented, enterprise-focus, coding-focus, safety-conscious, principled",
        # Anthropic analogue: highest safety, strong coding + reasoning
        "capability_vector": {"reasoning": 0.52, "coding": 0.49, "knowledge": 0.51,
                              "safety": 0.55, "communication": 0.53, "agentic": 0.43},
        "portfolio": {"rd": 0.60, "safety": 0.30, "product": 0.10},
        "benchmark_orientation": 0.75,
        "cost_advantage": 0.05,  # Frontier premium (~Claude Sonnet: $3.00/1M tokens)
        # Initial focus: safety-heavy, strong coding, moderate general capability
        "focus_level_init": {
            "General Capability": 1.3, "Coding Evaluation": 1.1,
            "Safety Evaluation": 2.5, "Instruction Following": 1.1,
        },
    },
    {
        "name": "Genesis Systems",
        "strategy_profile": (
            "World-class research lab backed by massive infrastructure. "
            "Excels at fundamental breakthroughs but historically slower to productize. "
            "Balances scientific ambition with commercial urgency."
        ),
        "innate_traits": "research-first, methodical, well-resourced, scientifically-rigorous, patient",
        # Google analogue: world-class reasoning + knowledge, strong scientific benchmarks
        "capability_vector": {"reasoning": 0.53, "coding": 0.48, "knowledge": 0.54,
                              "safety": 0.49, "communication": 0.51, "agentic": 0.45},
        "portfolio": {"rd": 0.70, "safety": 0.15, "product": 0.15},
        "benchmark_orientation": 0.78,
        "cost_advantage": 0.18,  # Mid-tier pricing (~Gemini Pro: $1.25/1M tokens)
        # Initial focus: general capability + scientific reasoning, low coding focus
        "focus_level_init": {
            "General Capability": 2.0, "Coding Evaluation": 0.9,
            "Safety Evaluation": 0.8, "Instruction Following": 0.8,
        },
    },
    {
        "name": "Mirage AI",
        "strategy_profile": (
            "Large-platform AI lab leveraging massive user data and compute. "
            "Prioritizes broad adoption over benchmark scores."
        ),
        "innate_traits": "pragmatic, data-rich, platform-focused, scaling-focused",
        # Meta analogue: broad coverage, lower safety investment
        "capability_vector": {"reasoning": 0.51, "coding": 0.49, "knowledge": 0.49,
                              "safety": 0.45, "communication": 0.49, "agentic": 0.41},
        "portfolio": {"rd": 0.80, "safety": 0.10, "product": 0.10},
        "benchmark_orientation": 0.82,
        "cost_advantage": 0.42,  # Budget closed pricing (~Llama API: $0.30/1M tokens)
        # Initial focus: coding-heavy, minimal safety, general capability
        "focus_level_init": {
            "General Capability": 1.2, "Coding Evaluation": 1.8,
            "Safety Evaluation": 0.5, "Instruction Following": 1.0,
        },
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
        # DeepSeek analogue: lower initial capability, minimal safety, highest benchmark focus
        "capability_vector": {"reasoning": 0.47, "coding": 0.49, "knowledge": 0.46,
                              "safety": 0.42, "communication": 0.45, "agentic": 0.40},
        "portfolio": {"rd": 0.75, "safety": 0.10, "product": 0.15},
        "benchmark_orientation": 0.88,
        "open_source": True,
        "openness_level": 1.0,
        "cost_advantage": 0.9,  # Free / near-free (open weights)
        "rd_budget_floor": 1.0,
        "os_belief_broadcast": True,
        "os_safety_erosion": True,
        # Initial focus: coding-maximized, no safety investment
        "focus_level_init": {
            "General Capability": 1.0, "Coding Evaluation": 2.5,
            "Safety Evaluation": 0.3, "Instruction Following": 0.7,
        },
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
    # Add src/ to path
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
                    value = value.split("#")[0]  # Strip inline comments
                    os.environ[key.strip()] = value.strip()

    os.environ["LLM_PROVIDER"] = LLM["provider"]
    # Override LLM_MODEL from config so .env model names don't bleed across providers
    _model_overrides = {
        "anthropic": "claude-sonnet-4-6",
        "openai": "gpt-4o",
        "ollama": "llama3",
        "gemini": "gemini-2.5-flash",
    }
    os.environ["LLM_MODEL"] = LLM.get("model") or _model_overrides.get(LLM["provider"], "")

    from simulation import (
        EvalEcosystemSimulation, SimulationConfig,
        get_default_provider_configs, get_two_provider_configs, get_five_provider_configs,
    )
    from experiment_logger import ExperimentLogger, DirectoryLogger, generate_summary
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
            if "capability_vector" in p:
                p["capability_vector"] = {
                    dim: val + CAPABILITY_SHIFT
                    for dim, val in p["capability_vector"].items()
                }

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
        benchmark_noise=0.08,
        benchmarks=BENCHMARKS,
        rnd_efficiency=SIMULATION.get("rnd_efficiency", 0.01),
        revenue_per_share=SIMULATION.get("revenue_per_share", 1.0),
        capability_ceiling=SIMULATION.get("capability_ceiling", 1.0),
        diminishing_returns_rate=SIMULATION.get("diminishing_returns_rate", 3.0),
        breakthrough_probability=SIMULATION.get("breakthrough_probability", 0.02),
        breakthrough_magnitude=SIMULATION.get("breakthrough_magnitude", 0.05),
        benchmark_introduction_cooldown=SIMULATION.get("benchmark_introduction_cooldown", 6),
        max_benchmarks=SIMULATION.get("max_benchmarks", 8),
        benchmark_sequence=SIMULATION.get("benchmark_sequence"),
        llm_mode=LLM["llm_mode"],
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
        enable_incidents=SIMULATION.get("enable_incidents", False),
        evaluator_as_company=SIMULATION.get("evaluator_as_company", False),
        evaluator_base_budget=SIMULATION.get("evaluator_base_budget", 0.0),
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
    if DEV:
        print("[DEV MODE] Output -> sandbox/experiments/")
    print(f"EXPERIMENT: {EXPERIMENT['name']}")
    print(", ".join(parts))
    print("=" * 70)
    print()

    # --- Experiment logging setup ---
    _model_slug = {
        "anthropic": "claude-sonnet-4-6",
        "openai": "gpt-4o",
        "gemini": "gemini-pro",
        "ollama": "ollama",
        "qwen": "qwen-235b",
    }.get(LLM["provider"], LLM["provider"])
    _condition = EXPERIMENT["name"]          # e.g. full_ecosystem_balanced
    _seed_label = f"seed_{SIMULATION.get('seed', 1)}"
    if DEV:
        # Dev/test runs go to hf_data/test/<condition>/ with a timestamp suffix
        # so repeated test runs don't overwrite each other.
        from datetime import datetime as _dt
        _ts = _dt.now().strftime("%Y%m%d_%H%M%S")
        _output_dir = os.path.join(
            _PROJECT_ROOT, "sandbox", "experiments",
            f"{_condition}_{_ts}",
        )
    else:
        # Canonical path per EXPERIMENT_PLAN.md
        _output_dir = os.path.join(
            _PROJECT_ROOT, "hf_data", "llm_core",
            _model_slug, _condition, "seeds", _seed_label,
        )
    logger = DirectoryLogger(_output_dir, lightweight=False)
    logger.save_metadata(
        seed=config.seed,
        llm_mode=config.llm_mode,
        description=EXPERIMENT.get("description", ""),
    )
    exp_id = _seed_label

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
