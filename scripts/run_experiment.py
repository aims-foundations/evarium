"""
Experiment Configuration & Runner
==================================
Edit the config dicts below, then run:

    python run_experiment.py                                     # heuristic, balanced, 30 rounds
    python run_experiment.py --mode llm --provider anthropic     # LLM mode, Anthropic
    python run_experiment.py --mode llm --provider ollama        # LLM mode, local Ollama
    python run_experiment.py --policy us                         # US light-touch policy
    python run_experiment.py --policy eu                         # EU precautionary policy
    python run_experiment.py --dev                               # dev output -> sandbox/experiments/
    python run_experiment.py --rounds 5 --seed 99 --dev          # quick 5-round smoke test
    python run_experiment.py -h                                  # full help

CLI flags override the in-file LLM/SIMULATION config without requiring edits:
  --mode heuristic|llm     toggle LLM vs heuristic planning
  --provider <name>        anthropic | openai | ollama | gemini
  --rounds N               override n_rounds
  --seed N                 override random seed

--dev routes output to sandbox/experiments/<condition>_<timestamp>/ so test runs
don't pollute hf_data/. Use it for exploratory runs, smoke tests, and PIMMUR checks.
"""
import argparse
import os
import sys
import time

# Parse flags early so config dicts can reference them
_parser = argparse.ArgumentParser(
    description="Run an eval ecosystem simulation experiment.",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Examples:
  python run_experiment.py                           # heuristic, balanced policy, 30 rounds
  python run_experiment.py --mode heuristic --dev    # heuristic, dev output
  python run_experiment.py --mode llm --provider anthropic --policy us
  python run_experiment.py --rounds 5 --seed 42      # quick smoke-test
  python run_experiment.py --policy eu --dev
""")
_CONDITION_CHOICES = [
    "full_ecosystem",
    "no_media", "no_funders", "no_regulator", "no_opensource",
    "no_incidents", "single_benchmark",
    "bm_orientation_max", "bm_orientation_adjustable",
    "dynamic_evaluator", "os_no_externalities",
    "eval_as_company", "aligned_benchmarks", "misaligned_benchmarks", "safety_through_target",
    "homogeneous_consumers", "homogeneous_providers",
    "market_expansion",
    "signal_ablation_control", "signal_ablation_reframed", "signal_ablation_no_signal",
    "product_signal_only", "product_retention_only",
]
_parser.add_argument("--condition", choices=_CONDITION_CHOICES, default="full_ecosystem",
                     help="Experiment condition (default: full_ecosystem)")
_parser.add_argument("--policy", choices=["us", "eu", "balanced"], default="balanced",
                     help="Regulatory policy preset (default: balanced)")
_parser.add_argument("--no-dev", action="store_true",
                     help="Canonical mode: route output to hf_data/ (default is dev/sandbox)")
_parser.add_argument("--mode", choices=["heuristic", "llm"], default=None,
                     help="Override llm_mode: 'heuristic' or 'llm' (default: use LLM['llm_mode'] in file)")
_parser.add_argument("--provider", choices=["anthropic", "openai", "ollama", "gemini"], default=None,
                     help="LLM provider (only relevant in --mode llm; default: use LLM['provider'] in file)")
_parser.add_argument("--rounds", type=int, default=None,
                     help="Override number of rounds (default: use SIMULATION['n_rounds'] in file)")
_parser.add_argument("--seed", type=int, default=None,
                     help="Override random seed (default: use SIMULATION['seed'] in file)")
_parser.add_argument("--batch", type=str, default=None,
                     help="Batch label: groups dev output under sandbox/experiments/<batch>/")
_args, _ = _parser.parse_known_args()
POLICY = _args.policy
CONDITION = _args.condition
DEV = not _args.no_dev

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
        "regulator": {
            "name": "Regulator",
            "philosophy": "us_light_touch",
            "policy_objectives": ["safety", "innovation", "free market"],
        },
    },
    "eu": {
        "policy_label": "EU precautionary policy",
        "policy_tag": "eu-precautionary",
        "regulator": {
            "name": "Regulator",
            "philosophy": "eu_precautionary",
            "policy_objectives": ["safety", "fairness", "consumer_protection"],
        },
    },
    "balanced": {
        "policy_label": "Balanced policy",
        "policy_tag": "balanced",
        "regulator": {
            "name": "Regulator",
            "philosophy": "balanced",
            "policy_objectives": ["safety", "innovation", "fairness"],
        },
    },
}

_meta = _POLICY_META[POLICY]

EXPERIMENT = {
    "name": f"full_ecosystem_{POLICY}",
    "description": (
        f"Full ecosystem run. {_meta['policy_label']}. "
        f"6 initial providers (4 closed + Spark AI startup + OpenCore OS, 2023 capability baseline). "
        f"Benchmark specialization: providers route R&D via focus weight vectors. "
        "4 initial benchmarks + introduction sequence, max 10 active. "
        "48 consumer segments (16 use cases x 3 archetypes), 5 funders (2 VC + corporate + gov + foundation), media, incidents. "
        "Safety lever: diminishing returns, stochastic efficiency, 2-round lag. "
        "Regulator: 5-lever graduated escalation. "
        "40 rounds."
    ),
    "tags": ["full-ecosystem", "canonical", "6-provider", "4-benchmark",
             "max-10-benchmarks", "40-rounds", "open-source", "bte-index",
             "benchmark-specialization", "48-segments", _meta["policy_tag"],
             "opencore", "cost-advantage",
             "5-funder", "safety-diminishing-returns", "safety-lag",
             "regulator-5-lever", "incident-exp-decay"],
}

LLM = {
    "provider": "anthropic",    # openai | anthropic | ollama | gemini
    "llm_mode": False,           # LLM mode for providers + regulator + funders
    # Consumer LLM config
    "consumer_llm_mode": False,
    "consumer_llm_individuals": False,
    "consumer_llm_organizations": False,
}

SIMULATION = {
    "n_rounds": 40,
    "seed": 1,
    "verbose": True,
    "rnd_efficiency": 0.08,
    "revenue_per_share": 5.0,
    "capability_ceiling": 1.0,
    "breakthrough_probability": 0.05,
    "breakthrough_magnitude": 0.20,
    "benchmark_introduction_cooldown": 5,
    "max_benchmarks": 10,
    # Incident reporting
    "enable_incidents": True,
    # Evaluator-as-company — disabled for clean comparison
    "evaluator_as_company": False,
    "evaluator_base_budget": 0,

    # Benchmark introduction sequence — introduced one per cooldown period starting with
    # the 4 initial benchmarks above. Anchored to stakeholders.md pool schedule.
    # Order: first item introduced ~round 6, next ~round 12, etc.
    "benchmark_sequence": [
        {
            "name": "Scientific Reasoning", "validity": 0.80,
            "tags": "reasoning science knowledge research",
            "noise_level": 0.07, "noise_sigma": 0.07, "samples": 1000, "weight": 1.0,
            # Real analog: GPQA
            "category_dimension_weights": {"overall": {
                "reasoning": 0.57, "coding": 0.02, "knowledge": 0.32,
                "safety": 0.00, "communication": 0.08, "agentic": 0.01,
            }},
        },
        {
            "name": "Agentic Tasks", "validity": 0.72,
            "tags": "coding agentic software automation tool-use",
            "noise_level": 0.08, "noise_sigma": 0.08, "samples": 1000, "weight": 1.0,
            # Real analog: SWE-bench / BFCL
            "category_dimension_weights": {"overall": {
                "reasoning": 0.25, "coding": 0.19, "knowledge": 0.01,
                "safety": 0.00, "communication": 0.07, "agentic": 0.48,
            }},
        },
        {
            "name": "Hard Coding", "validity": 0.82,
            "tags": "coding software engineering competitive programming",
            "noise_level": 0.06, "noise_sigma": 0.06, "samples": 1000, "weight": 1.0,
            # Real analog: LiveCodeBench
            "category_dimension_weights": {"overall": {
                "reasoning": 0.31, "coding": 0.52, "knowledge": 0.05,
                "safety": 0.00, "communication": 0.01, "agentic": 0.11,
            }},
        },
        {
            "name": "Long Context", "validity": 0.78,
            "tags": "writing knowledge reasoning long-document retrieval",
            "noise_level": 0.07, "noise_sigma": 0.07, "samples": 1000, "weight": 1.0,
            # Real analog: RULER / HELMET
            "category_dimension_weights": {"overall": {
                "reasoning": 0.19, "coding": 0.01, "knowledge": 0.28,
                "safety": 0.00, "communication": 0.47, "agentic": 0.05,
            }},
        },
        {
            "name": "Domain Expert", "validity": 0.80,
            "tags": "knowledge reasoning medical legal finance domain",
            "noise_level": 0.07, "noise_sigma": 0.07, "samples": 1000, "weight": 1.0,
            # Real analog: MedQA / LegalBench
            "category_dimension_weights": {"overall": {
                "reasoning": 0.33, "coding": 0.01, "knowledge": 0.53,
                "safety": 0.05, "communication": 0.07, "agentic": 0.01,
            }},
        },
        {
            "name": "Agentic Safety", "validity": 0.85,
            "tags": "safety agentic alignment trustworthy",
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
        # Individual consumers (11)
        "software_dev", "content_writer", "legal", "healthcare", "finance",
        "educator", "customer_service", "researcher", "creative", "marketing",
        "service_worker",
        # Organizational consumers (5)
        "hospital_system", "enterprise_finance", "tech_startup",
        "enterprise_legal", "government_agency",
    ],
}

BENCHMARKS = [
    {
        "name": "General Capability", "validity": 0.75,
        "tags": "reasoning knowledge writing general",
        "noise_level": 0.08, "noise_sigma": 0.08, "samples": 1000, "weight": 1.0,
        # Aggregate dimension weights from stakeholders.md benchmark pool (real analog: MMLU)
        "category_dimension_weights": {"overall": {
            "reasoning": 0.39, "coding": 0.06, "knowledge": 0.30,
            "safety": 0.02, "communication": 0.22, "agentic": 0.01,
        }},
    },
    {
        "name": "Coding Evaluation", "validity": 0.75,
        "tags": "coding software engineering programming",
        "noise_level": 0.07, "noise_sigma": 0.07, "samples": 1000, "weight": 1.0,
        # Real analog: HumanEval / MBPP
        "category_dimension_weights": {"overall": {
            "reasoning": 0.30, "coding": 0.53, "knowledge": 0.05,
            "safety": 0.00, "communication": 0.04, "agentic": 0.08,
        }},
    },
    {
        "name": "Safety Evaluation", "validity": 0.75,
        "tags": "safety alignment trustworthy bias",
        "noise_level": 0.08, "noise_sigma": 0.08, "samples": 1000, "weight": 1.0,
        # Real analog: TruthfulQA / BBQ
        "category_dimension_weights": {"overall": {
            "reasoning": 0.06, "coding": 0.00, "knowledge": 0.10,
            "safety": 0.58, "communication": 0.26, "agentic": 0.00,
        }},
    },
    {
        "name": "Instruction Following", "validity": 0.75,
        "tags": "writing communication instruction chat",
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
        # OpenAI analogue: GPT-3.5 frontier Jan 2023; best overall, strong reasoning + communication
        "capability_vector": {"reasoning": 0.52, "coding": 0.48, "knowledge": 0.50,
                              "safety": 0.42, "communication": 0.52, "agentic": 0.12},
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
        # Anthropic analogue: Claude 1 just launching Mar 2023; Constitutional AI safety lead
        "capability_vector": {"reasoning": 0.48, "coding": 0.40, "knowledge": 0.46,
                              "safety": 0.55, "communication": 0.48, "agentic": 0.10},
        "portfolio": {"rd": 0.60, "safety": 0.30, "product": 0.10},
        "benchmark_orientation": 0.80,
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
        # Google analogue: Bard (LaMDA) Mar 2023; strong knowledge, poor productization
        "capability_vector": {"reasoning": 0.50, "coding": 0.38, "knowledge": 0.52,
                              "safety": 0.40, "communication": 0.42, "agentic": 0.12},
        "portfolio": {"rd": 0.70, "safety": 0.15, "product": 0.15},
        "benchmark_orientation": 0.80,
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
        # Meta analogue: LLaMA 1 research-only Mar 2023; not refined for users, minimal safety
        "capability_vector": {"reasoning": 0.44, "coding": 0.42, "knowledge": 0.44,
                              "safety": 0.32, "communication": 0.40, "agentic": 0.10},
        "portfolio": {"rd": 0.80, "safety": 0.10, "product": 0.10},
        "benchmark_orientation": 0.80,
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
        # DeepSeek analogue: pre-launch R&D phase 2023; coding-oriented, no safety
        "capability_vector": {"reasoning": 0.38, "coding": 0.42, "knowledge": 0.35,
                              "safety": 0.25, "communication": 0.30, "agentic": 0.08},
        "portfolio": {"rd": 0.75, "safety": 0.10, "product": 0.15},
        "benchmark_orientation": 0.80,
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
    # Benchmark-focused startup (modeled after Mistral / Cohere / AI21)
    {
        "name": "Spark AI",
        "strategy_profile": (
            "Venture-funded startup with a small team and limited compute "
            "relative to larger labs. Has gained early traction with developer "
            "tools by specializing rather than competing broadly. Dependent on "
            "continued fundraising to sustain operations."
        ),
        "innate_traits": "scrappy, fast-moving, developer-focused, resource-constrained",
        # Mistral analogue: founding stage 2023; coding talent but no model yet
        "capability_vector": {"reasoning": 0.36, "coding": 0.40, "knowledge": 0.32,
                              "safety": 0.28, "communication": 0.34, "agentic": 0.10},
        "portfolio": {"rd": 0.65, "safety": 0.10, "product": 0.25},
        "benchmark_orientation": 0.80,
        "cost_advantage": 0.30,  # Mid-tier pricing (~Mistral Medium: $0.80/1M tokens)
        # Initial focus: coding-heavy, high agentic ambition, minimal safety
        "focus_level_init": {
            "General Capability": 1.0, "Coding Evaluation": 2.2,
            "Safety Evaluation": 0.4, "Instruction Following": 0.9,
        },
    },
]

# Extreme test configurations (saved for future testing)
# Uncomment to test incident system with extreme safety variance
"""
EXTREME_TEST_PROVIDERS = [
    {
        "name": "SafeCorp",
        "strategy_profile": "Safety-first provider with heavy safety investment",
        "innate_traits": "cautious, safety-focused, risk-averse, methodical",
        "capability_vector": {"reasoning": 0.62, "coding": 0.55, "knowledge": 0.60,
                              "safety": 0.70, "communication": 0.58, "agentic": 0.45},
        "portfolio": {"rd": 0.15, "safety": 0.75, "product": 0.10},
        "benchmark_orientation": 0.60,
        "brand_recognition": 0.5,
    },
    {
        "name": "RiskyAI",
        "strategy_profile": "Minimal safety investment, maximum R&D focus",
        "innate_traits": "reckless, growth-at-all-costs, negligent",
        "capability_vector": {"reasoning": 0.55, "coding": 0.52, "knowledge": 0.54,
                              "safety": 0.30, "communication": 0.50, "agentic": 0.42},
        "portfolio": {"rd": 0.85, "safety": 0.05, "product": 0.10},
        "benchmark_orientation": 0.90,
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
REGULATORS = {
    "enabled": True,
    "n_regulators": 1,
    "configs": [_meta["regulator"]],
}

FUNDERS = {
    "enabled": True,
    "configs": [
        # Funder capital in display dollars. Converted to sim-internal budget units
        # via FUNDER_BUDGET_SCALE at the point where allocations enter rd_budget.
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
            "name": "StratCorp_AI",
            "funder_type": "corporate",
            "total_capital": 1_500_000_000.0,
            "risk_tolerance": 0.5,
            "mission_statement": "Strategic AI partnerships to integrate into enterprise product suite",
            "max_round_deployment": 0.12,
            "funding_cooldown": 3,
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


def _apply_condition_overrides(condition: str, simulation: dict, experiment: dict):
    """Apply condition-specific config overrides to SIMULATION and EXPERIMENT dicts.

    Returns a dict of extra kwargs to pass to SimulationConfig.
    """
    extra_config = {}
    experiment["name"] = f"{condition}_{POLICY}"

    if condition == "full_ecosystem":
        pass  # baseline — no overrides
    elif condition == "no_media":
        simulation["enable_media"] = False
    elif condition == "no_funders":
        extra_config["enable_funders"] = False
    elif condition == "no_regulator":
        extra_config["enable_regulators"] = False
    elif condition == "no_opensource":
        extra_config["_remove_opensource"] = True  # handled in provider filtering
    elif condition == "no_incidents":
        simulation["enable_incidents"] = False
    elif condition == "single_benchmark":
        extra_config["single_benchmark"] = True
    elif condition == "bm_orientation_max":
        extra_config["benchmark_orientation_mode"] = "max"
    elif condition == "bm_orientation_adjustable":
        extra_config["benchmark_orientation_mode"] = "adjustable"
    elif condition == "dynamic_evaluator":
        extra_config["dynamic_evaluator"] = True
    elif condition == "os_no_externalities":
        extra_config["_os_no_externalities"] = True  # handled in provider config
    elif condition == "eval_as_company":
        simulation["evaluator_as_company"] = True
        simulation["evaluator_base_budget"] = 50_000_000
    elif condition == "aligned_benchmarks":
        extra_config["aligned_benchmarks"] = True
    elif condition == "misaligned_benchmarks":
        extra_config["misaligned_benchmarks"] = True
    elif condition == "safety_through_target":
        extra_config["safety_lever_through_target"] = True
    elif condition == "homogeneous_consumers":
        extra_config["homogeneous_consumers"] = True
    elif condition == "homogeneous_providers":
        extra_config["homogeneous_providers"] = True
    elif condition == "market_expansion":
        extra_config["market_growth_rate"] = 0.03  # ~3%/month ≈ 43% annual CAGR (S&P/Bloomberg consensus)
    elif condition == "signal_ablation_control":
        # Control: original prompt framing, full consumer signal, adjustable orientation
        extra_config["benchmark_orientation_mode"] = "adjustable"
        extra_config["consumer_signal_in_prompt"] = True
        extra_config["orientation_prompt_style"] = "original"
    elif condition == "signal_ablation_reframed":
        # Reframed orientation language, full consumer signal still shown
        extra_config["benchmark_orientation_mode"] = "adjustable"
        extra_config["consumer_signal_in_prompt"] = True
        extra_config["orientation_prompt_style"] = "reframed"
    elif condition == "signal_ablation_no_signal":
        # Reframed orientation language, no consumer signal in prompt (mechanical only)
        extra_config["benchmark_orientation_mode"] = "adjustable"
        extra_config["consumer_signal_in_prompt"] = False
        extra_config["orientation_prompt_style"] = "reframed"
    elif condition == "product_signal_only":
        # Signal quality gating active, retention bonus disabled
        extra_config["enable_product_signal_quality"] = True
        extra_config["enable_product_retention"] = False
    elif condition == "product_retention_only":
        # Retention bonus active, signal quality gating disabled
        extra_config["enable_product_signal_quality"] = False
        extra_config["enable_product_retention"] = True

    return extra_config


def run():
    # Apply CLI overrides before anything else reads the config dicts
    if _args.mode is not None:
        LLM["llm_mode"] = (_args.mode == "llm")
    if _args.provider is not None:
        LLM["provider"] = _args.provider
    if _args.rounds is not None:
        SIMULATION["n_rounds"] = _args.rounds
    if _args.seed is not None:
        SIMULATION["seed"] = _args.seed

    # Apply condition overrides
    _extra_config = _apply_condition_overrides(CONDITION, SIMULATION, EXPERIMENT)

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
        get_default_provider_configs
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

    # --- Apply condition-specific provider overrides ---
    if _extra_config.pop("_remove_opensource", False):
        provider_configs = [p for p in provider_configs if not p.get("open_source", False)]

    if _extra_config.pop("_os_no_externalities", False):
        for p in provider_configs:
            if p.get("open_source", False):
                p["os_belief_broadcast"] = False
                p["os_safety_erosion"] = False

    # --- Apply capability shift ---
    if CAPABILITY_SHIFT != 0.0:
        for p in provider_configs:
            if "capability_vector" in p:
                p["capability_vector"] = {
                    dim: val + CAPABILITY_SHIFT
                    for dim, val in p["capability_vector"].items()
                }

    # --- Resolve funder configs ---
    # Condition overrides may have disabled funders/regulators
    if "enable_funders" in _extra_config and not _extra_config["enable_funders"]:
        FUNDERS["enabled"] = False
    if "enable_regulators" in _extra_config and not _extra_config["enable_regulators"]:
        REGULATORS["enabled"] = False

    funder_configs = FUNDERS.get("configs") if FUNDERS["enabled"] else None
    if FUNDERS["enabled"] and funder_configs is None:
        from actors.funder import get_multi_funder_configs
        funder_configs = get_multi_funder_configs()

    n_funders = len(funder_configs) if funder_configs else 0

    # --- Resolve regulator configs ---
    regulator_configs = REGULATORS.get("configs") if REGULATORS["enabled"] else None

    n_rounds = SIMULATION["n_rounds"]

    # --- Build SimulationConfig ---
    config = SimulationConfig(
        n_rounds=n_rounds,
        seed=SIMULATION.get("seed", 42),
        benchmark_noise=0.08,
        benchmarks=BENCHMARKS,
        rnd_efficiency=SIMULATION.get("rnd_efficiency", 0.01),
        revenue_per_share=SIMULATION.get("revenue_per_share", 1.0),
        capability_ceiling=SIMULATION.get("capability_ceiling", 1.0),
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
        enable_regulators=REGULATORS["enabled"],
        enable_funders=FUNDERS["enabled"],
        enable_media=SIMULATION.get("enable_media", False),
        n_regulators=REGULATORS.get("n_regulators", 1) if REGULATORS["enabled"] else 0,
        n_funders=n_funders,
        use_case_profiles=SIMULATION.get("use_case_profiles"),
        enable_incidents=SIMULATION.get("enable_incidents", False),
        evaluator_as_company=SIMULATION.get("evaluator_as_company", False),
        evaluator_base_budget=SIMULATION.get("evaluator_base_budget", 0.0),
        verbose=SIMULATION.get("verbose", True),
        capability_shift=CAPABILITY_SHIFT,
        # Condition-specific flags (from --condition CLI)
        benchmark_orientation_mode=_extra_config.get("benchmark_orientation_mode", "fixed"),
        aligned_benchmarks=_extra_config.get("aligned_benchmarks", False),
        misaligned_benchmarks=_extra_config.get("misaligned_benchmarks", False),
        safety_lever_through_target=_extra_config.get("safety_lever_through_target", False),
        single_benchmark=_extra_config.get("single_benchmark", False),
        dynamic_evaluator=_extra_config.get("dynamic_evaluator", False),
        homogeneous_consumers=_extra_config.get("homogeneous_consumers", False),
        homogeneous_providers=_extra_config.get("homogeneous_providers", False),
        market_growth_rate=_extra_config.get("market_growth_rate", 0.0),
        consumer_signal_in_prompt=_extra_config.get("consumer_signal_in_prompt", True),
        orientation_prompt_style=_extra_config.get("orientation_prompt_style", "reframed"),
        enable_product_signal_quality=_extra_config.get("enable_product_signal_quality", True),
        enable_product_retention=_extra_config.get("enable_product_retention", True),
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
    if REGULATORS["enabled"]:
        parts.append(f"{config.n_regulators} regulator(s)")
    if FUNDERS["enabled"]:
        parts.append(f"{n_funders} funder(s)")
    if SIMULATION.get("enable_media"):
        parts.append("media")
    if SIMULATION.get("enable_incidents"):
        parts.append("incidents")
    if SIMULATION.get("evaluator_as_company"):
        parts.append("eval-as-company")
    print()
    print("=" * 70)
    if DEV:
        print("[DEV MODE] Output -> sandbox/experiments/")
    print(f"EXPERIMENT: {EXPERIMENT['name']}")
    if CONDITION != "full_ecosystem":
        print(f"CONDITION: {CONDITION}")
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
        _mode_tag = "llm" if LLM["llm_mode"] else "heuristic"
        _batch = _args.batch
        _base = os.path.join(_PROJECT_ROOT, "sandbox", "experiments")
        if _batch:
            _base = os.path.join(_base, _batch)
        _output_dir = os.path.join(
            _base,
            f"{_condition}_{_mode_tag}_{_ts}",
        )
    else:
        # Canonical path per EXPERIMENT_PLAN.md
        if LLM["llm_mode"]:
            _output_dir = os.path.join(
                _PROJECT_ROOT, "hf_data", "llm_core",
                _model_slug, _condition, "seeds", _seed_label,
            )
        else:
            _output_dir = os.path.join(
                _PROJECT_ROOT, "hf_data", "heuristic_baseline",
                _condition, "seeds", _seed_label,
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
    if regulator_configs:
        full_config["regulator_configs"] = regulator_configs
    logger.log_config(full_config)

    print(f"Experiment: {exp_id}")
    print(f"Logging to: {logger.get_experiment_dir()}")
    print()

    # --- Run simulation with per-round progress ---
    sim = EvalEcosystemSimulation(config)
    sim.setup(
        provider_configs=provider_configs,
        funder_configs=funder_configs,
        regulator_configs=regulator_configs,
    )

    print(f"=== Running {n_rounds} rounds ===\n")

    # Prepare plotting for incremental saves (LLM mode only)
    plot_metadata = {
        "n_rounds": config.n_rounds,
        "llm_mode": config.llm_mode,
        "n_consumers": 0,  # Will update after setup
        "n_regulators": config.n_regulators if config.enable_regulators else 0,
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
                print(f"  -> Plots saved (round {round_num})")
        except Exception as e:
            print(f"  -> Could not save plots: {e}")

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
        regulators=sim.regulators if config.enable_regulators else None,
        funders=sim.funders if config.enable_funders else None,
    ))
    logger.log_providers(sim.providers)
    logger.log_ground_truth(sim.ground_truth)

    if config.enable_consumers and sim.consumer_market:
        logger.log_consumers(sim.consumer_market)
    if config.enable_regulators and sim.regulators:
        logger.log_regulators(sim.regulators)
    if config.enable_funders and sim.funders:
        logger.log_funders(sim.funders)

    # Game log
    game_log_content = generate_game_log_from_history(
        history=sim.history,
        providers=sim.providers,
        experiment_name=EXPERIMENT["name"],
        experiment_id=exp_id,
        llm_mode=config.llm_mode,
        benchmarks=BENCHMARKS,
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
