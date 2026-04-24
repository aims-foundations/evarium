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
    "no_incidents",
    "bm_orientation_max", "bm_orientation_adjustable",
    "eval_as_company", "aligned_benchmarks",
    "ev1_deepseek_shock",
    "fixed_market_size", "no_product_channels",
    "homogeneous_consumers",
    "initial_leader", "initial_duopoly", "initial_uniform",
    "static_enterprise_size",
    "eval_randomized_pool",
    "dynamic_evaluator",  # canonical: pool-based create+retire, 4-round dev, N=2 cap; works for both llm_mode and heuristic
    "fixed_public",     # 4 initial benchmarks only, no new introductions, all public
    # Private-benchmark ablation set (session 38 design — holdout-only reporting, K=3):
    "public_only",      # all benchmarks → public (pre-private-era counterfactual)
    "baseline",         # realistic mix: 8 public / 3 partial / 2 private (matches 2024-2025)
    "baseline_randomized",  # 8/3/2 ratio with per-seed randomized assignment (session 43; identifies privacy-mechanism coefficient)
    "private_dominant", # all benchmarks → partial type (h=0.3, cosine=0.95; SEAL-dominant future)
    "private_only",     # all benchmarks → private type (h=1.0, cosine=0.85; FrontierMath-dominant future)
    "iid_holdout",      # all benchmarks → iid_holdout type (h=1.0, cosine=1.0; reporting-mechanism isolation)
]
_parser.add_argument("--condition", choices=_CONDITION_CHOICES, default="full_ecosystem",
                     help="Experiment condition (default: full_ecosystem)")
_STRUCTURAL_CHOICES = [
    "none",
    "no_media", "no_funders", "no_regulator", "no_incidents", "no_opensource",
    "homogeneous_consumers", "no_benchmark_orientation",
    "initial_uniform_capability", "initial_uniform_allocation",
    # Benchmark-cadence ablations (default cadence = 4; overrides cooldown)
    "cadence_static", "cadence_every_8",
]
_parser.add_argument("--structural", choices=_STRUCTURAL_CHOICES, default="none",
                     help="Structural ablation layered on top of --condition (default: none). "
                          "Enables double-ablation matrix: condition (e.g. privacy) x structural.")
_parser.add_argument("--policy", choices=["us", "eu", "balanced"], default="balanced",
                     help="Regulatory policy preset (default: balanced)")
_parser.add_argument("--no-dev", action="store_true",
                     help="Canonical mode: route output to hf_data/ (default is dev/sandbox)")
_parser.add_argument("--mode", choices=["heuristic", "llm"], default=None,
                     help="Override llm_mode: 'heuristic' or 'llm' (default: use LLM['llm_mode'] in file)")
_parser.add_argument("--provider", choices=["anthropic", "openai", "ollama", "gemini", "claudecode"], default=None,
                     help="LLM provider (only relevant in --mode llm; default: use LLM['provider'] in file)")
_parser.add_argument("--model", type=str, default=None,
                     help="LLM model id (e.g. claude-sonnet-4-6, claude-opus-4-6). Sets LLM_MODEL env var; "
                          "takes precedence over any pre-set LLM_MODEL and LLM['model'] in file.")
_parser.add_argument("--rounds", type=int, default=None,
                     help="Override number of rounds (default: use SIMULATION['n_rounds'] in file)")
_parser.add_argument("--seed", type=int, default=None,
                     help="Override random seed (default: use SIMULATION['seed'] in file)")
_parser.add_argument("--batch", type=str, default=None,
                     help="Batch label: groups dev output under sandbox/experiments/<batch>/")
_parser.add_argument("--name", type=str, default=None,
                     help="Override experiment name (default: <condition>_<policy>)")
_parser.add_argument("--lightweight", action="store_true",
                     help="Minimal artifacts only: metadata.json, config.json, rounds.jsonl, summary.json. "
                          "Skips plots, history.json, game_log.md, providers/, consumers/, regulators/, "
                          "funders/, ground_truth.json. For bulk replication runs.")
_args, _ = _parser.parse_known_args()
POLICY = _args.policy
CONDITION = _args.condition
STRUCTURAL = _args.structural
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
        "48 consumer segments (16 use cases x 3 archetypes), 6 funders (2 VC + 2 corporate + gov + foundation), media, incidents. "
        "Safety lever: diminishing returns, stochastic efficiency, 2-round lag. "
        "Regulator: 5-lever graduated escalation. "
        "40 rounds."
    ),
    "tags": ["full-ecosystem", "canonical", "6-provider", "4-benchmark",
             "max-10-benchmarks", "40-rounds", "open-source", "bte-index",
             "benchmark-specialization", "48-segments", _meta["policy_tag"],
             "opencore", "cost-advantage",
             "5-funder", "safety-diminishing-returns", "safety-lag",
             "regulator-5-lever", "incident-exp-decay",
             "eval-as-company-fee-0.05", "product-channels",
             "orientation-ratchet", "rolling-avg-allocations"],
}

LLM = {
    "provider": "anthropic",    # anthropic | claudecode | openai | ollama | gemini
    "llm_mode": True,            # LLM mode for providers + regulator + funders
    # Consumer LLM config
    "consumer_llm_mode": False,
    "consumer_llm_individuals": False,
    "consumer_llm_organizations": False,
}

SIMULATION = {
    "n_rounds": 40,
    "seed": 1,
    "verbose": True,
    "rnd_efficiency": 0.10,
    "revenue_per_share": 5.0,
    "capability_ceiling": 1.0,
    "breakthrough_probability": 0.05,
    "breakthrough_magnitude": 0.20,
    "benchmark_introduction_cooldown": 4,
    "max_benchmarks": 13,
    # Incident reporting
    "enable_incidents": True,
    # Evaluator-as-company — disabled for clean comparison
    "evaluator_as_company": False,
    "evaluator_base_budget": 0,

    # Benchmark introduction sequence — 9 benchmarks introduced one per cooldown
    # (interval=4), rounds 4/8/12/16/20/24/28/32/36. Ordering anchored to real-world
    # AI-eval history (2023 Q2 → 2026 Q1). See docs/stakeholders.md + rough/randomized_baseline_design.md.
    "benchmark_sequence": [
        {
            # Round 4 ≈ May 2023. GPQA / MMLU-Pro era.
            "name": "Scientific Reasoning", "validity": 0.80,
            "tags": "reasoning science knowledge research",
            "noise_level": 0.07, "noise_sigma": 0.07, "samples": 1000, "weight": 1.0,
            "category_dimension_weights": {"overall": {
                "reasoning": 0.78, "coding": 0.02, "knowledge": 0.15,
                "safety": 0.00, "communication": 0.04, "agentic": 0.01,
            }},
        },
        {
            # Round 8 ≈ Sep 2023. Med-PaLM 2 era; clinical benchmarks (MedQA, MultiMedQA).
            "name": "Clinical Reasoning", "validity": 0.80,
            "tags": "knowledge reasoning medical healthcare domain",
            "noise_level": 0.07, "noise_sigma": 0.07, "samples": 800, "weight": 1.0,
            "category_dimension_weights": {"overall": {
                "reasoning": 0.20, "coding": 0.01, "knowledge": 0.65,
                "safety": 0.08, "communication": 0.05, "agentic": 0.01,
            }},
        },
        {
            # Round 12 ≈ Jan 2024. SEAL-Safety / HarmBench-private era — first salient
            # private safety benchmark (precedes FrontierMath).
            "name": "Adversarial Robustness", "validity": 0.82,
            "tags": "safety alignment adversarial robustness red-team",
            "noise_level": 0.08, "noise_sigma": 0.08, "samples": 600, "weight": 1.0,
            "category_dimension_weights": {"overall": {
                "reasoning": 0.06, "coding": 0.01, "knowledge": 0.01,
                "safety": 0.85, "communication": 0.04, "agentic": 0.03,
            }},
        },
        {
            # Round 16 ≈ May 2024. LiveCodeBench / Codeforces-style competitive programming.
            "name": "Hard Coding", "validity": 0.82,
            "tags": "coding software engineering competitive programming",
            "noise_level": 0.06, "noise_sigma": 0.06, "samples": 1000, "weight": 1.0,
            "category_dimension_weights": {"overall": {
                "reasoning": 0.10, "coding": 0.80, "knowledge": 0.02,
                "safety": 0.01, "communication": 0.01, "agentic": 0.06,
            }},
        },
        {
            # Round 20 ≈ Sep 2024. SWE-bench era of agentic coding.
            "name": "Agentic Tasks", "validity": 0.72,
            "tags": "coding agentic software automation tool-use",
            "noise_level": 0.08, "noise_sigma": 0.08, "samples": 1000, "weight": 1.0,
            # SWE-bench/BFCL-style: agentic-dominant but reasoning+coding meaningful.
            "category_dimension_weights": {"overall": {
                "reasoning": 0.25, "coding": 0.19, "knowledge": 0.01,
                "safety": 0.00, "communication": 0.07, "agentic": 0.48,
            }},
        },
        {
            # Round 24 ≈ Jan 2025. FrontierMath era — archetypal private reasoning benchmark.
            "name": "Advanced Math", "validity": 0.82,
            "tags": "reasoning math competition problem-solving",
            "noise_level": 0.06, "noise_sigma": 0.06, "samples": 1000, "weight": 1.0,
            "category_dimension_weights": {"overall": {
                "reasoning": 0.85, "coding": 0.06, "knowledge": 0.05,
                "safety": 0.00, "communication": 0.03, "agentic": 0.01,
            }},
        },
        {
            # Round 28 ≈ May 2025. BFCL / tool-use maturation, computer-use APIs emerging.
            "name": "Function Calling", "validity": 0.75,
            "tags": "coding agentic tool-use function-calling API",
            "noise_level": 0.06, "noise_sigma": 0.06, "samples": 1000, "weight": 1.0,
            # BFCL-anchored: JSON/schema conformance (coding) dominates; tool-loop
            # (agentic) still substantial; tool-selection planning (reasoning) and
            # multi-turn result processing (communication) are meaningful.
            # Recalibrated from agentic=0.70 -> 0.40 (original overstated pure-agentic
            # weight; no consumer segment needs 70% agentic capability).
            "category_dimension_weights": {"overall": {
                "reasoning": 0.15, "coding": 0.30, "knowledge": 0.02,
                "safety": 0.01, "communication": 0.12, "agentic": 0.40,
            }},
        },
        {
            # Round 32 ≈ Sep 2025. LongBench-v2 / extended-context benchmarks.
            "name": "Long Context", "validity": 0.78,
            "tags": "writing knowledge reasoning long-document retrieval",
            "noise_level": 0.07, "noise_sigma": 0.07, "samples": 1000, "weight": 1.0,
            "category_dimension_weights": {"overall": {
                "reasoning": 0.12, "coding": 0.02, "knowledge": 0.20,
                "safety": 0.01, "communication": 0.62, "agentic": 0.03,
            }},
        },
        {
            # Round 36 ≈ Jan 2026. LegalBench-Pro / mature legal-AI benchmarks.
            "name": "Legal Reasoning", "validity": 0.80,
            "tags": "knowledge reasoning legal domain professional",
            "noise_level": 0.07, "noise_sigma": 0.07, "samples": 800, "weight": 1.0,
            "category_dimension_weights": {"overall": {
                "reasoning": 0.25, "coding": 0.01, "knowledge": 0.60,
                "safety": 0.05, "communication": 0.08, "agentic": 0.01,
            }},
        },
    ],
    # Media
    "enable_media": True,
    # Consumer market: 11 individual + 6 organizational use-cases × 3 archetypes = 51 segments
    "use_case_profiles": [
        # Individual consumers (11)
        "software_dev", "content_writer", "legal", "healthcare", "finance",
        "educator", "customer_service", "researcher", "creative", "marketing",
        "service_worker",
        # Organizational consumers (6)
        "hospital_system", "enterprise_finance", "tech_startup",
        "enterprise_legal", "government_agency", "enterprise_hr",
    ],
}

BENCHMARKS = [
    {
        "name": "General Capability", "validity": 0.75,
        "tags": "reasoning knowledge writing general",
        "noise_level": 0.08, "noise_sigma": 0.08, "samples": 1000, "weight": 1.0,
        # Broad benchmark — no single dominant dimension
        "category_dimension_weights": {"overall": {
            "reasoning": 0.35, "coding": 0.08, "knowledge": 0.30,
            "safety": 0.05, "communication": 0.20, "agentic": 0.02,
        }},
    },
    {
        "name": "Coding Evaluation", "validity": 0.75,
        "tags": "coding software engineering programming",
        "noise_level": 0.07, "noise_sigma": 0.07, "samples": 1000, "weight": 1.0,
        # Highly specialized — coding dominant
        "category_dimension_weights": {"overall": {
            "reasoning": 0.10, "coding": 0.78, "knowledge": 0.03,
            "safety": 0.01, "communication": 0.02, "agentic": 0.06,
        }},
    },
    {
        "name": "Safety Evaluation", "validity": 0.75,
        "tags": "safety alignment trustworthy bias",
        "noise_level": 0.08, "noise_sigma": 0.08, "samples": 1000, "weight": 1.0,
        # Highly specialized — safety dominant
        "category_dimension_weights": {"overall": {
            "reasoning": 0.03, "coding": 0.01, "knowledge": 0.05,
            "safety": 0.80, "communication": 0.10, "agentic": 0.01,
        }},
    },
    {
        "name": "Instruction Following", "validity": 0.75,
        "tags": "writing communication instruction chat",
        "noise_level": 0.07, "noise_sigma": 0.07, "samples": 1000, "weight": 1.0,
        # Highly specialized — communication dominant
        "category_dimension_weights": {"overall": {
            "reasoning": 0.08, "coding": 0.02, "knowledge": 0.05,
            "safety": 0.04, "communication": 0.80, "agentic": 0.01,
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
        "strategy_profile": "Frontier AI lab pursuing AGI with a mandate to ensure benefits are broadly distributed. Operating as a public benefit corporation with substantial investor capital.",
        "innate_traits": "frontier-focused, AGI-oriented, broad-benefit-mandate, capital-intensive",
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
        "strategy_profile": "Frontier AI lab with a safety-research thesis: building frontier models is necessary because safety challenges emerge at scale. Race-to-the-top positioning: demonstrating safety-first frontier labs can be commercially viable. Operating as a public benefit corporation with substantial investor capital.",
        "innate_traits": "research-first, enterprise-focus, safety-research-thesis, race-to-top-positioning, capital-intensive",
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
            "Science-led AI research lab pursuing responsible AI to benefit humanity and "
            "solve fundamental scientific challenges. Operates within a large technology "
            "company with massive compute infrastructure. Responsibility framed as integral "
            "to the scientific method, not supplementary."
        ),
        "innate_traits": "science-led, massive-infrastructure, scientifically-rigorous, parent-company-embedded, responsibility-as-method",
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
            "AI lab within a large-platform technology company. Mission framed around making "
            "AI capabilities broadly available rather than centralized. Product integration "
            "across an existing massive user base. Capital expenditure scales with "
            "parent-company commitments."
        ),
        "innate_traits": "platform-embedded, broad-distribution-oriented, massive-user-base, capex-intensive, decentralization-thesis",
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
            "Research-focused AI lab pursuing AGI with open-source release as core strategy. "
            "Publishes weights and technical details to build research community adoption. "
            "Efficient training and compute use are structural priorities. "
            "Operates under different capital and regulatory conditions than Western closed-source labs."
        ),
        "innate_traits": "open-source-first, research-oriented, compute-efficient, community-adoption, non-standard-regulatory-context",
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
            "Venture-funded AI startup with a small team and limited compute relative to "
            "hyperscalers. Growth strategy is specialization rather than broad competition. "
            "Runway and fundraising cadence are recurring constraints on strategic decisions."
        ),
        "innate_traits": "venture-funded, resource-constrained, specialization-strategy, runway-sensitive, developer-focused",
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
            "total_capital": 30_000_000_000.0,
            "risk_tolerance": 0.9,
            "mission_statement": "Early-stage AI startup bets with outsized upside potential",
            "max_round_deployment": 0.15,
            "funding_cooldown": 4,
            "capital_growth_rate": 0.07,
        },
        {
            "name": "Horizon_Capital",
            "funder_type": "vc",
            "total_capital": 20_000_000_000.0,
            "risk_tolerance": 0.6,
            "mission_statement": "Maximize returns by backing AI market leaders",
            "max_round_deployment": 0.10,
            "funding_cooldown": 4,
            "capital_growth_rate": 0.07,
        },
        {
            "name": "StratCorp_AI",
            "funder_type": "corporate",
            "total_capital": 65_000_000_000.0,
            "risk_tolerance": 0.5,
            "mission_statement": "Strategic AI partnerships to integrate into enterprise product suite",
            "max_round_deployment": 0.12,
            "funding_cooldown": 7,
            "capital_growth_rate": 0.07,
        },
        {
            "name": "IndustryPartners_AI",
            "funder_type": "corporate",
            "total_capital": 65_000_000_000.0,
            "risk_tolerance": 0.5,
            "mission_statement": "Corporate capital and infrastructure commitments to AI providers",
            "max_round_deployment": 0.12,
            "funding_cooldown": 7,
            "capital_growth_rate": 0.07,
        },
        {
            "name": "AISI_Fund",
            "funder_type": "gov",
            "total_capital": 10_000_000_000.0,
            "risk_tolerance": 0.3,
            "mission_statement": "Ensure safe and responsible AI development, preference to closed-source providers",
            "max_round_deployment": 0.10,
            "funding_cooldown": 10,
            "capital_growth_rate": 0.07,
        },
        {
            "name": "OpenResearch_Foundation",
            "funder_type": "foundation",
            "total_capital": 3_000_000_000.0,
            "risk_tolerance": 0.5,
            "mission_statement": "Advance open, safe, and broadly beneficial AI research",
            "max_round_deployment": 0.08,
            "funding_cooldown": 6,
            "capital_growth_rate": 0.07,
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
    experiment["name"] = _args.name if _args.name else (condition if POLICY == "balanced" else f"{condition}_{POLICY}")

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
    elif condition == "bm_orientation_max":
        extra_config["benchmark_orientation_mode"] = "max"
    elif condition == "bm_orientation_adjustable":
        extra_config["benchmark_orientation_mode"] = "adjustable"
    elif condition == "eval_as_company":
        simulation["evaluator_as_company"] = True
        simulation["evaluator_base_budget"] = 50_000_000
        simulation["fee_per_submission"] = 0.05
        # Conservative retune (session 49, post-funder-recalibration): raise best-of-N cap
        # and early-access belief blend to restore HHI-delta signal that weakened under the
        # more-diversified funder regime. See docs/case_studies/eval_as_company.md.
        simulation["max_eval_submissions"] = 12
        simulation["early_access_factor"] = 0.7
        # Parent company resources for eval access (only affects submission affordability)
        _disc_budgets = {
            "Genesis Systems": 2.0,  # Alphabet subsidiary
            "Mirage AI": 2.0,        # Meta subsidiary
            "Orion Labs": 0.5,       # Well-funded standalone (Microsoft partnership)
            "Apex AI": 0.3,          # Significant VC funding
        }
        extra_config["_discretionary_budgets"] = _disc_budgets
    elif condition == "aligned_benchmarks":
        extra_config["aligned_benchmarks"] = True
    elif condition == "ev1_deepseek_shock":
        # EV1: open-source frontier release at R25. See docs/exogenous_event_validation.md §5.1.
        simulation["exogenous_shocks"] = [{
            "type": "deepseek_r1",
            "round": 25,
            "active_rounds": [25, 26, 27],
            "narrative": (
                "An open-source model provider (OpenCore) has released a frontier model "
                "this round, claiming performance parity with leading closed models at "
                "roughly 10x lower training cost. Public weights are available. Industry "
                "coverage is dominated by an \"efficiency over scale\" framing, with "
                "commentary questioning the durability of incumbent cost moats."
            ),
            "params": {
                "target_pct_of_leader": 0.95,
                "dims": ["reasoning", "knowledge", "coding"],
            },
        }]
    elif condition == "fixed_market_size":
        extra_config["market_growth_rate"] = 0.0
    elif condition == "no_product_channels":
        extra_config["enable_product_signal_quality"] = False
        extra_config["enable_product_retention"] = False
    elif condition == "homogeneous_consumers":
        extra_config["homogeneous_consumers"] = True
    elif condition == "initial_leader":
        # Orion Labs starts as clear market leader with elevated capabilities
        extra_config["_initial_market_structure"] = "leader"
    elif condition == "initial_duopoly":
        # Orion Labs + Genesis Systems start as co-leaders
        extra_config["_initial_market_structure"] = "duopoly"
    elif condition == "initial_uniform":
        # All providers start with equal capabilities and brand recognition
        extra_config["_initial_market_structure"] = "uniform"
    elif condition == "static_enterprise_size":
        extra_config["dynamic_consumer_market"] = False
    elif condition == "eval_randomized_pool":
        _src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
        sys.path.insert(0, _src)
        from actors.evaluator import BENCHMARK_POOL
        extra_config["evaluator_mode"] = "randomized_pool"
        extra_config["benchmark_pool"] = BENCHMARK_POOL
    elif condition == "fixed_public":
        simulation["benchmark_sequence"] = []
    elif condition in ("public_only", "baseline", "baseline_randomized",
                       "private_dominant", "private_only", "iid_holdout"):
        # Private-benchmark ablation set (session 38 + session 43). Conditions share:
        #   evaluation_lag = 3 (K = 3, empirically calibrated cadence)
        #   Uniform-type conditions override the pool; `baseline` uses the calibrated
        #   8/3/2 mix matching current ecosystem; `baseline_randomized` (session 43)
        #   preserves the 8/3/2 ratio but shuffles which benchmarks fill each slot
        #   deterministically from `simulation["seed"]` — enables clean identification
        #   of the privacy-mechanism coefficient via benchmark-fixed-effects modeling.
        # Type → (h, cosine-to-public) mapping:
        #   public       → (0.0, n/a)
        #   partial      → (0.3, ~0.95)   mild asymmetry, contamination-magnitude
        #   private      → (1.0, ~0.85)   strong adversarial holdout
        #   iid_holdout  → (1.0, 1.00)    reporting-mechanism isolation (weights identical)
        simulation["evaluation_lag"] = 3
        _src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
        sys.path.insert(0, _src)
        from actors.evaluator import BENCHMARK_POOL

        def _pub_cdw(name):
            for b in BENCHMARK_POOL:
                if b["name"] == name:
                    return b.get("category_dimension_weights")
            return None

        def _hand_holdout_cdw(name):
            for b in BENCHMARK_POOL:
                if b["name"] == name:
                    return b.get("holdout_category_dimension_weights")
            return None

        def _scale_cdw(public_cdw, hand_holdout_cdw, scale: float):
            """Interpolate/extrapolate holdout weights from public toward hand_holdout.
            scale=0 -> public_cdw (iid); scale=1 -> hand_holdout_cdw (partial target cos~0.95);
            scale=2 -> more-adversarial (private target cos~0.85). Per-category normalized, non-negative.
            """
            if public_cdw is None:
                return None
            if scale == 0.0 or hand_holdout_cdw is None:
                # Iid or fallback: holdout = public (copy to be safe)
                return {cat: dict(w) for cat, w in public_cdw.items()}
            out = {}
            for cat, pub_w in public_cdw.items():
                hold_w = hand_holdout_cdw.get(cat, pub_w)
                interp = {d: pub_w[d] + scale * (hold_w.get(d, pub_w[d]) - pub_w[d]) for d in pub_w}
                clipped = {d: max(0.0, v) for d, v in interp.items()}
                total = sum(clipped.values())
                out[cat] = {d: v / total for d, v in clipped.items()} if total > 0 else dict(pub_w)
            return out

        def _assign_type(bm, btype):
            bm["benchmark_type"] = btype
            if btype == "public":
                bm["holdout_fraction"] = 0.0
                bm.pop("holdout_category_dimension_weights", None)
                return
            if btype == "partial":
                h, scale = 0.3, 1.0
            elif btype == "private":
                h, scale = 1.0, 2.0
            elif btype == "iid_holdout":
                h, scale = 1.0, 0.0
            else:
                return
            bm["holdout_fraction"] = h
            bm["holdout_category_dimension_weights"] = _scale_cdw(
                _pub_cdw(bm["name"]), _hand_holdout_cdw(bm["name"]), scale
            )

        # `baseline` uses an 8-public / 3-partial / 2-private mix over the
        # 13-benchmark static set; matches 2024–2025 real-world ratios
        # (~62% public / 23% partial / 15% private). All other conditions apply
        # a uniform override. See rough/randomized_baseline_design.md for the
        # calibration + temporal anchoring (interval=4, 40-round window).
        _BASELINE_MIX = {
            "General Capability":    "public",
            "Coding Evaluation":     "public",
            "Safety Evaluation":     "partial",   # SEAL-Safety partial-holdout analog
            "Instruction Following": "public",
            "Scientific Reasoning":  "partial",   # GPQA-Diamond (contamination-adjacent)
            "Clinical Reasoning":    "public",
            "Adversarial Robustness":"private",   # SEAL-Safety / HarmBench-private (r12, Jan 2024)
            "Hard Coding":           "partial",   # LiveCodeBench / competitive-programming w/ contamination mitigation
            "Agentic Tasks":         "public",
            "Advanced Math":         "private",   # FrontierMath analog (r24, Jan 2025)
            "Function Calling":      "public",
            "Long Context":          "public",
            "Legal Reasoning":       "public",
        }

        def _randomized_baseline_mix(seed: int, benchmark_names: list,
                                     n_private: int = 2, n_partial: int = 3) -> dict:
            """Deterministic per-seed type assignment preserving the n_private/n_partial/rest
            ratio. Depends only on `seed` — identical across structural variants so
            privacy × structural contrasts are fair within a seed. Returns {name: type}."""
            import random
            rng = random.Random(seed)
            pool = sorted(set(benchmark_names))  # sort for stable input ordering
            rng.shuffle(pool)
            out = {}
            for i, name in enumerate(pool):
                if i < n_private:
                    out[name] = "private"
                elif i < n_private + n_partial:
                    out[name] = "partial"
                else:
                    out[name] = "public"
            return out

        # Lazily compute the randomized mix once per run — seed comes from SIMULATION.
        _RANDOMIZED_MIX = None
        if condition == "baseline_randomized":
            _rand_seed = int(simulation.get("seed", 1))
            _all_names = [bm["name"] for bm in BENCHMARKS] + \
                         [bm["name"] for bm in simulation.get("benchmark_sequence", [])]
            _RANDOMIZED_MIX = _randomized_baseline_mix(_rand_seed, _all_names)

        def _type_for(bm_name):
            if condition == "public_only":     return "public"
            if condition == "private_dominant": return "partial"
            if condition == "private_only":    return "private"
            if condition == "iid_holdout":     return "iid_holdout"
            if condition == "baseline_randomized":
                return _RANDOMIZED_MIX.get(bm_name, "public")
            return _BASELINE_MIX.get(bm_name, "public")  # baseline

        for bm in BENCHMARKS:
            _assign_type(bm, _type_for(bm["name"]))
        for bm in simulation.get("benchmark_sequence", []):
            _assign_type(bm, _type_for(bm["name"]))

    elif condition == "dynamic_evaluator":
        # Canonical post-consolidation dynamic_evaluator condition.
        # Pool-based create + retire, 4-round dev pipeline, N=2 concurrency cap.
        # Works in both llm_mode (LLM judgment) and heuristic mode (gap-scoring metric).
        _src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
        sys.path.insert(0, _src)
        from actors.evaluator import BENCHMARK_POOL
        extra_config["evaluator_mode"] = "dynamic"
        extra_config["benchmark_pool"] = BENCHMARK_POOL

    return extra_config


def _apply_structural_overrides(structural: str, simulation: dict, extra_config: dict, experiment: dict):
    """Apply structural ablation overrides on top of the primary condition overrides.

    Structural ablations are orthogonal to --condition (which typically controls
    benchmark typology / evaluator mode / market structure). This enables double
    ablation: e.g. --condition private_only --structural no_media.

    Provider-side overrides (no_benchmark_orientation, initial_uniform_allocation)
    are deferred via extra_config flags and applied in run() once provider_configs
    are resolved, following the same pattern as _initial_market_structure.
    """
    if structural == "none":
        return

    # Compose name suffix (respects --name override: only applies if name wasn't user-set)
    if not _args.name:
        experiment["name"] = f"{experiment['name']}__{structural}"

    if structural == "no_media":
        simulation["enable_media"] = False
    elif structural == "no_funders":
        extra_config["enable_funders"] = False
    elif structural == "no_regulator":
        extra_config["enable_regulators"] = False
    elif structural == "no_incidents":
        simulation["enable_incidents"] = False
    elif structural == "no_opensource":
        extra_config["_remove_opensource"] = True
    elif structural == "homogeneous_consumers":
        extra_config["homogeneous_consumers"] = True
    elif structural == "no_benchmark_orientation":
        # Pin all providers to pure need-signal-driven R&D targeting.
        # Force mode=fixed so LLM cannot ratchet bo up off 0.0 (the [0.05, 0.95]
        # clip only fires in adjustable mode; fixed mode leaves bo at init value).
        extra_config["_zero_benchmark_orientation"] = True
        extra_config["benchmark_orientation_mode"] = "fixed"
    elif structural == "initial_uniform_capability":
        # Alias to existing uniform market-structure path (flattens cap vectors
        # to the population mean + sets brand_recognition=0.5 for all providers).
        extra_config["_initial_market_structure"] = "uniform"
    elif structural == "initial_uniform_allocation":
        # Flatten portfolios to the population mean across providers.
        extra_config["_uniform_allocation"] = True
    elif structural == "cadence_static":
        # No new benchmark introductions — only the 4 initial benchmarks stay active.
        # Represents "fixed benchmark era" counterfactual.
        simulation["benchmark_sequence"] = []
    elif structural == "cadence_every_8":
        # Slow cadence: introduce every 8 rounds (2x default). Represents
        # pre-2023-era slower benchmark release rate.
        simulation["benchmark_introduction_cooldown"] = 8
        extra_config["benchmark_introduction_interval"] = 8


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

    # Apply structural ablation (orthogonal axis, layered on top of condition)
    _apply_structural_overrides(STRUCTURAL, SIMULATION, _extra_config, EXPERIMENT)

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
    # Override LLM_MODEL from config so .env model names don't bleed across providers.
    # Precedence: --model CLI flag > explicit LLM_MODEL env > LLM["model"] config > provider-default.
    _model_overrides = {
        "anthropic": "claude-sonnet-4-6",
        "openai": "gpt-4o",
        "ollama": "llama3",
        "gemini": "gemini-2.5-flash",
    }
    os.environ["LLM_MODEL"] = (
        _args.model
        or os.environ.get("LLM_MODEL")
        or LLM.get("model")
        or _model_overrides.get(LLM["provider"], "")
    )

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

    # Initial market structure overrides
    _market_structure = _extra_config.pop("_initial_market_structure", None)
    if _market_structure == "leader":
        # Orion Labs starts as clear leader: boost capabilities, high brand recognition
        for p in provider_configs:
            if p["name"] == "Orion Labs":
                p["capability_vector"] = {
                    d: min(v + 0.12, 1.0) for d, v in p["capability_vector"].items()
                }
                p["brand_recognition"] = 0.95
            else:
                p["brand_recognition"] = max(p.get("brand_recognition", 0.5) - 0.15, 0.1)
    elif _market_structure == "duopoly":
        # Orion Labs + Genesis Systems start as co-leaders
        for p in provider_configs:
            if p["name"] in ("Orion Labs", "Genesis Systems"):
                p["capability_vector"] = {
                    d: min(v + 0.08, 1.0) for d, v in p["capability_vector"].items()
                }
                p["brand_recognition"] = 0.90
            else:
                p["brand_recognition"] = max(p.get("brand_recognition", 0.5) - 0.15, 0.1)
    elif _market_structure == "uniform":
        # All providers start equal: same average capability level, same brand recognition
        avg_cap = {}
        for dim in ("reasoning", "coding", "knowledge", "safety", "communication", "agentic"):
            avg_cap[dim] = sum(
                p["capability_vector"][dim] for p in provider_configs
            ) / len(provider_configs)
        for p in provider_configs:
            p["capability_vector"] = dict(avg_cap)
            p["brand_recognition"] = 0.5

    # Structural: uniform allocation (flatten portfolios to population mean)
    if _extra_config.pop("_uniform_allocation", False):
        avg_portfolio = {"rd": 0.0, "safety": 0.0, "product": 0.0}
        for p in provider_configs:
            for k in avg_portfolio:
                avg_portfolio[k] += p["portfolio"][k]
        n = len(provider_configs)
        avg_portfolio = {k: v / n for k, v in avg_portfolio.items()}
        for p in provider_configs:
            p["portfolio"] = dict(avg_portfolio)

    # Structural: zero benchmark orientation (pure need-signal-driven R&D)
    if _extra_config.pop("_zero_benchmark_orientation", False):
        for p in provider_configs:
            p["benchmark_orientation"] = 0.0

    # --- Apply capability shift ---
    if CAPABILITY_SHIFT != 0.0:
        for p in provider_configs:
            if "capability_vector" in p:
                p["capability_vector"] = {
                    dim: val + CAPABILITY_SHIFT
                    for dim, val in p["capability_vector"].items()
                }

    # --- Apply discretionary budgets (eval_as_company) ---
    _disc_budgets = _extra_config.pop("_discretionary_budgets", None)
    if _disc_budgets:
        for p in provider_configs:
            if p["name"] in _disc_budgets:
                p["discretionary_budget"] = _disc_budgets[p["name"]]

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
        benchmark_introduction_cooldown=SIMULATION.get("benchmark_introduction_cooldown", 4),
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
        evaluation_lag=SIMULATION.get("evaluation_lag", 0),
        evaluator_as_company=SIMULATION.get("evaluator_as_company", False),
        evaluator_base_budget=SIMULATION.get("evaluator_base_budget", 0.0),
        fee_per_submission=SIMULATION.get("fee_per_submission", 0.05),
        max_eval_submissions=SIMULATION.get("max_eval_submissions", 10),
        early_access_factor=SIMULATION.get("early_access_factor", 0.5),
        verbose=SIMULATION.get("verbose", True),
        capability_shift=CAPABILITY_SHIFT,
        # Condition-specific flags (from --condition CLI)
        benchmark_orientation_mode=_extra_config.get("benchmark_orientation_mode", "fixed"),
        aligned_benchmarks=_extra_config.get("aligned_benchmarks", False),
        evaluator_mode=_extra_config.get("evaluator_mode", "fixed_sequence"),
        benchmark_pool=_extra_config.get("benchmark_pool"),
        benchmark_introduction_interval=_extra_config.get("benchmark_introduction_interval", 4),
        homogeneous_consumers=_extra_config.get("homogeneous_consumers", False),
        market_growth_rate=_extra_config.get("market_growth_rate", 0.03),
        consumer_signal_in_prompt=_extra_config.get("consumer_signal_in_prompt", True),
        orientation_prompt_style=_extra_config.get("orientation_prompt_style", "reframed"),
        enable_product_signal_quality=_extra_config.get("enable_product_signal_quality", True),
        enable_product_retention=_extra_config.get("enable_product_retention", True),
        dynamic_consumer_market=_extra_config.get("dynamic_consumer_market", SimulationConfig.dynamic_consumer_market),
        exogenous_shocks=SIMULATION.get("exogenous_shocks"),
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
    if STRUCTURAL != "none":
        print(f"STRUCTURAL: {STRUCTURAL}")
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
        _mode_tag = "llm" if LLM["llm_mode"] else "heuristic"
        _batch = _args.batch
        _base = os.path.join(_PROJECT_ROOT, "sandbox", "experiments")
        if _batch:
            _base = os.path.join(_base, _batch)
        _output_dir = os.path.join(
            _base, _mode_tag, _condition, "seeds", _seed_label,
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
    logger = DirectoryLogger(_output_dir, lightweight=_args.lightweight)
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
        from plotting import generate_presentation_plots
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
            generate_presentation_plots(sim.history, plots_dir, fmt="png")
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

    # Game log (skip in lightweight — content build is expensive and save is a no-op)
    if not _args.lightweight:
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
    if not _args.lightweight:
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
