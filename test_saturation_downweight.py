"""
Test saturation downweighting instead of retirement
"""
import os
os.environ["LLM_PROVIDER"] = "ollama"

from simulation import EvalEcosystemSimulation, SimulationConfig

# Quick 15-round test with saturation
config = SimulationConfig(
    n_rounds=15,
    seed=42,
    benchmark_validity=0.7,
    benchmark_exploitability=0.5,
    benchmark_noise=0.1,
    benchmarks=[
        {"name": "coding", "validity": 0.55, "exploitability": 0.35, "noise_level": 0.08, "weight": 0.5},
        {"name": "qa", "validity": 0.7, "exploitability": 0.45, "noise_level": 0.1, "weight": 0.5},
    ],
    rnd_efficiency=0.01,
    llm_mode=False,  # Heuristic for speed
    enable_consumers=True,
    enable_policymakers=False,
    enable_funders=False,
    enable_media=True,
    use_case_profiles=["software_dev", "content_writer"],  # Just 6 segments
    verbose=True,
)

sim = EvalEcosystemSimulation(config)
from simulation import get_default_provider_configs
sim.setup(provider_configs=get_default_provider_configs())

print("\n=== Testing Saturation Downweighting ===\n")

for round_num in range(15):
    print(f"\n--- Round {round_num} ---")
    round_data = sim.run_round()

    # Check for saturation and weight decay
    for bm_name in ["coding", "qa"]:
        state = sim.evaluator._benchmark_saturation_state.get(bm_name, {})
        decay = sim.evaluator._benchmark_weight_decay.get(bm_name, 1.0)

        if state.get("saturated"):
            print(f"  {bm_name}: SATURATED (round {state['saturation_round']}), "
                  f"weight decay = {decay:.2f}x, "
                  f"max_score = {state['max_score']:.4f}")
        elif decay < 1.0:
            print(f"  {bm_name}: weight decay = {decay:.2f}x")

print("\n=== Test Complete ===")
print(f"Active benchmarks: {[bm.name for bm in sim.evaluator.benchmarks]}")
print(f"Total benchmarks: {len(sim.evaluator.benchmarks)} (should still be 2, not retired)")
