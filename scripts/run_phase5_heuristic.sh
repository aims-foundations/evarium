#!/usr/bin/env bash
# run_phase5_heuristic.sh — Run Phase 5 heuristic baseline for all 27 conditions.
# Sequential execution (index.json has no locking).
# ~6 min per condition x 27 = ~2.7 hours total.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

N_SEEDS="${1:-30}"
PYTHON=$(command -v python3 || command -v python)

# All 27 conditions: 11 existing + 16 generated
CONDITIONS=(
    # Full ecosystem (3)
    "exp_011:full_ecosystem_balanced"
    "exp_001:full_ecosystem_us"
    "exp_002:full_ecosystem_eu"
    # Balanced ablations (8)
    "exp_004:no_media_balanced"
    "exp_005:no_incidents_balanced"
    "exp_006:no_startups_balanced"
    "exp_007:no_opencore_balanced"
    "exp_008:single_benchmark_balanced"
    "exp_009:no_funders_balanced"
    "exp_010:no_bench_evolution_balanced"
    "exp_012:eval_as_company_balanced"
    # US ablations (8)
    "gen_ablation_no_media_us:no_media_us"
    "gen_ablation_no_incidents_us:no_incidents_us"
    "gen_ablation_no_startups_us:no_startups_us"
    "gen_ablation_no_opencore_us:no_opencore_us"
    "gen_ablation_single_benchmark_us:single_benchmark_us"
    "gen_ablation_no_funders_us:no_funders_us"
    "gen_ablation_no_bench_evolution_us:no_bench_evolution_us"
    "gen_ablation_eval_as_company_us:eval_as_company_us"
    # EU ablations (8)
    "gen_ablation_no_media_eu:no_media_eu"
    "gen_ablation_no_incidents_eu:no_incidents_eu"
    "gen_ablation_no_startups_eu:no_startups_eu"
    "gen_ablation_no_opencore_eu:no_opencore_eu"
    "gen_ablation_single_benchmark_eu:single_benchmark_eu"
    "gen_ablation_no_funders_eu:no_funders_eu"
    "gen_ablation_no_bench_evolution_eu:no_bench_evolution_eu"
    "gen_ablation_eval_as_company_eu:eval_as_company_eu"
)

total=${#CONDITIONS[@]}
passed=0
failed=0
start_time=$(date +%s)

echo "========================================"
echo "  Phase 5: Heuristic Baseline"
echo "  Conditions: $total"
echo "  Seeds per condition: $N_SEEDS"
echo "  Total runs: $((total * N_SEEDS))"
echo "  Started: $(date)"
echo "========================================"
echo ""

for i in "${!CONDITIONS[@]}"; do
    IFS=: read -r exp_id label <<< "${CONDITIONS[$i]}"
    idx=$((i + 1))

    echo "[$idx/$total] $label ($exp_id) — $N_SEEDS seeds"
    cond_start=$(date +%s)

    if $PYTHON scripts/run_diagnostics.py replicate "$exp_id" --n-seeds "$N_SEEDS" --heuristic > /dev/null 2>&1; then
        cond_end=$(date +%s)
        dur=$((cond_end - cond_start))
        echo "  PASS (${dur}s)"
        passed=$((passed + 1))
    else
        cond_end=$(date +%s)
        dur=$((cond_end - cond_start))
        echo "  FAIL (${dur}s) — check output for errors"
        failed=$((failed + 1))
    fi
done

end_time=$(date +%s)
total_dur=$((end_time - start_time))
echo ""
echo "========================================"
echo "  Phase 5 COMPLETE"
echo "  Passed: $passed / $total"
if [ $failed -gt 0 ]; then
    echo "  Failed: $failed"
fi
echo "  Duration: $((total_dur / 60))m $((total_dur % 60))s"
echo "  Finished: $(date)"
echo "========================================"
