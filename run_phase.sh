#!/usr/bin/env bash
# run_phase.sh — Run all experiments for a given phase from EXPERIMENT_PLAN.md.
#
# Usage:
#   ./run_phase.sh --phase <phase> [options]
#
# Phases:
#   5      Heuristic baseline (free, no LLM calls, 27 conditions x 30 seeds)
#   2p0    P0 replications: 3 full-ecosystem conditions x 30 seeds
#   2p1    P1 replications: 9 high-signal ablation conditions x 30 seeds
#   2p2    P2 replications: 15 remaining ablation conditions x 30 seeds
#   3      Sensitivity sweeps: 7 parameters x ~5 levels x 3 seeds
#   4      Cross-model comparison: full_ecosystem_balanced x 5 models x 5 seeds
#
# Options:
#   --phase <phase>        Phase to run (required)
#   --model <preset>       Model preset (required for LLM phases)
#   --port N               vLLM port (default: 8000)
#   --n-seeds N            Override default seed count
#   --dry-run              Show commands without executing
#   --help, -h             Show this help
#
# Examples:
#   ./run_phase.sh --phase 5                                  # heuristic baseline (free)
#   ./run_phase.sh --phase 2p0 --model qwen                   # P0 replications
#   ./run_phase.sh --phase 3   --model qwen                   # sensitivity sweeps
#   ./run_phase.sh --phase 4                                  # cross-model comparison
#   ./run_phase.sh --phase 5   --dry-run                      # preview commands
#   ./run_phase.sh --phase 2p0 --model qwen --n-seeds 5       # override seed count
#
# Implementation notes:
#   - This script calls scripts/run_diagnostics.py with --condition <name> and
#     --output-dir pointing to output/validation/. run_diagnostics.py must be
#     updated to accept these flags (currently it uses exp IDs from index.json
#     and writes to output/experiments/). Until updated, use --dry-run to
#     inspect intended commands.
#   - build_registry.py must be implemented before the registry step at the
#     end of each phase will work (see EXPERIMENT_PLAN.md Runs Registry section).
#   - This script does NOT start a vLLM server. For Qwen runs, start the server
#     first via run_qwen_all_phases.sh or manually (see EXPERIMENT_PLAN.md).
#   - GPU device IDs for vLLM: confirm available devices on your machine.
#     The default (0,1,2,3) in run_qwen_all_phases.sh may not match your setup.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ── Usage ──────────────────────────────────────────────────────────────────
usage() {
    head -34 "$0" | tail -33
}

# ── Defaults ───────────────────────────────────────────────────────────────
PHASE=""
MODEL_PRESET=""
VLLM_PORT=8000
SEED_OVERRIDE=""
DRY_RUN=false

# ── Parse arguments ────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --phase)   PHASE="$2";         shift 2 ;;
        --model)   MODEL_PRESET="$2";  shift 2 ;;
        --port)    VLLM_PORT="$2";     shift 2 ;;
        --n-seeds) SEED_OVERRIDE="$2"; shift 2 ;;
        --dry-run) DRY_RUN=true;       shift ;;
        --help|-h) usage; exit 0 ;;
        *)
            echo "ERROR: Unknown option: $1"
            usage; exit 1 ;;
    esac
done

if [[ -z "$PHASE" ]]; then
    echo "ERROR: --phase is required."
    usage; exit 1
fi

PYTHON=$(command -v python3 || command -v python)

MODEL_FLAGS=""
if [[ -n "$MODEL_PRESET" ]]; then
    MODEL_FLAGS="--model $MODEL_PRESET --port $VLLM_PORT"
fi

# ── Condition lists ────────────────────────────────────────────────────────

# P0: 3 full-ecosystem conditions (all presets)
FULL_ECOSYSTEM_CONDITIONS=(
    full_ecosystem_balanced
    full_ecosystem_us
    full_ecosystem_eu
)

# P1: 3 high-signal ablations x 3 presets = 9 conditions
P1_CONDITIONS=(
    ablation_no_opencore_balanced
    ablation_no_opencore_us
    ablation_no_opencore_eu
    ablation_no_startups_balanced
    ablation_no_startups_us
    ablation_no_startups_eu
    ablation_single_benchmark_balanced
    ablation_single_benchmark_us
    ablation_single_benchmark_eu
)

# P2: 5 remaining ablations x 3 presets = 15 conditions
P2_CONDITIONS=(
    ablation_no_media_balanced
    ablation_no_media_us
    ablation_no_media_eu
    ablation_no_incidents_balanced
    ablation_no_incidents_us
    ablation_no_incidents_eu
    ablation_no_funders_balanced
    ablation_no_funders_us
    ablation_no_funders_eu
    ablation_no_bench_evolution_balanced
    ablation_no_bench_evolution_us
    ablation_no_bench_evolution_eu
    ablation_eval_as_company_balanced
    ablation_eval_as_company_us
    ablation_eval_as_company_eu
)

# All 27 conditions
ALL_27_CONDITIONS=(
    "${FULL_ECOSYSTEM_CONDITIONS[@]}"
    "${P1_CONDITIONS[@]}"
    "${P2_CONDITIONS[@]}"
)

# ── Phase functions ────────────────────────────────────────────────────────
declare -a COMMANDS=()

phase_5() {
    local n_seeds="${SEED_OVERRIDE:-30}"
    local total=$(( ${#ALL_27_CONDITIONS[@]} * n_seeds ))

    echo "Phase 5: Heuristic Baseline"
    echo "  Conditions: ${#ALL_27_CONDITIONS[@]} (all 27)"
    echo "  Seeds per condition: $n_seeds"
    echo "  Total runs: $total"
    echo "  Cost: FREE (no LLM calls)"
    echo "  Output: output/validation/heuristic_baseline/<condition>/seeds/"
    echo ""

    for cond in "${ALL_27_CONDITIONS[@]}"; do
        COMMANDS+=("$PYTHON scripts/run_diagnostics.py replicate --condition $cond --n-seeds $n_seeds --heuristic --output-dir output/validation/heuristic_baseline/$cond")
    done
}

phase_2p0() {
    local n_seeds="${SEED_OVERRIDE:-30}"

    if [[ -z "$MODEL_PRESET" ]]; then
        echo "ERROR: Phase 2p0 requires --model."
        exit 1
    fi

    local total=$(( ${#FULL_ECOSYSTEM_CONDITIONS[@]} * n_seeds ))

    echo "Phase 2 P0: Full Ecosystem Replications"
    echo "  Model: $MODEL_PRESET"
    echo "  Conditions: ${#FULL_ECOSYSTEM_CONDITIONS[@]} (full ecosystem x 3 presets)"
    echo "  Seeds per condition: $n_seeds"
    echo "  Total runs: $total"
    echo "  Output: output/validation/replications_llm/$MODEL_PRESET/<condition>/seeds/"
    echo ""

    for cond in "${FULL_ECOSYSTEM_CONDITIONS[@]}"; do
        COMMANDS+=("$PYTHON scripts/run_diagnostics.py $MODEL_FLAGS replicate --condition $cond --n-seeds $n_seeds --output-dir output/validation/replications_llm/$MODEL_PRESET/$cond")
    done
}

phase_2p1() {
    local n_seeds="${SEED_OVERRIDE:-30}"

    if [[ -z "$MODEL_PRESET" ]]; then
        echo "ERROR: Phase 2p1 requires --model."
        exit 1
    fi

    local total=$(( ${#P1_CONDITIONS[@]} * n_seeds ))

    echo "Phase 2 P1: High-Signal Ablation Replications"
    echo "  Model: $MODEL_PRESET"
    echo "  Conditions: ${#P1_CONDITIONS[@]} (No OpenCore, No Startups, Single Benchmark x 3 presets)"
    echo "  Seeds per condition: $n_seeds"
    echo "  Total runs: $total"
    echo "  Output: output/validation/replications_llm/$MODEL_PRESET/<condition>/seeds/"
    echo ""

    for cond in "${P1_CONDITIONS[@]}"; do
        COMMANDS+=("$PYTHON scripts/run_diagnostics.py $MODEL_FLAGS replicate --condition $cond --n-seeds $n_seeds --output-dir output/validation/replications_llm/$MODEL_PRESET/$cond")
    done
}

phase_2p2() {
    local n_seeds="${SEED_OVERRIDE:-30}"

    if [[ -z "$MODEL_PRESET" ]]; then
        echo "ERROR: Phase 2p2 requires --model."
        exit 1
    fi

    local total=$(( ${#P2_CONDITIONS[@]} * n_seeds ))

    echo "Phase 2 P2: Remaining Ablation Replications"
    echo "  Model: $MODEL_PRESET"
    echo "  Conditions: ${#P2_CONDITIONS[@]} (5 ablations x 3 presets)"
    echo "  Seeds per condition: $n_seeds"
    echo "  Total runs: $total"
    echo "  Output: output/validation/replications_llm/$MODEL_PRESET/<condition>/seeds/"
    echo ""

    for cond in "${P2_CONDITIONS[@]}"; do
        COMMANDS+=("$PYTHON scripts/run_diagnostics.py $MODEL_FLAGS replicate --condition $cond --n-seeds $n_seeds --output-dir output/validation/replications_llm/$MODEL_PRESET/$cond")
    done
}

phase_3() {
    local n_seeds="${SEED_OVERRIDE:-3}"
    local base_cond="full_ecosystem_balanced"

    if [[ -z "$MODEL_PRESET" ]]; then
        echo "ERROR: Phase 3 requires --model (tip: use --model gemini-flash for budget sweeps)."
        exit 1
    fi

    # 7 parameters from EXPERIMENT_PLAN.md Phase 3.
    # Param names must match SimulationConfig field names exactly.
    # Note: initial_capability_mean is set via provider configs, not SimulationConfig
    # directly — run_diagnostics.py sensitivity may need special handling for it.
    declare -A PARAMS
    PARAMS[rnd_efficiency]="0.005,0.008,0.01,0.012,0.015"
    PARAMS[benchmark_validity_decay_rate]="0.01,0.015,0.02,0.03,0.04"
    PARAMS[benchmark_exploitability_growth_rate]="0.005,0.01,0.015,0.02,0.03"
    PARAMS[startup_entry_probability]="0,0.05,0.09,0.15,0.25"
    PARAMS[capability_ceiling]="0.7,0.85,1.0,1.2"
    PARAMS[initial_capability_mean]="0.15,0.20,0.25,0.30,0.35"
    PARAMS[capability_shift]="-0.10,0.0,0.10,0.20,0.30"

    echo "Phase 3: Sensitivity Analysis"
    echo "  Model: $MODEL_PRESET"
    echo "  Base condition: $base_cond"
    echo "  Parameters: ${#PARAMS[@]}"
    echo "  Seeds per point: $n_seeds"
    echo "  Output: output/validation/sensitivity/<param>/"
    echo ""

    for param in "${!PARAMS[@]}"; do
        COMMANDS+=("$PYTHON scripts/run_diagnostics.py $MODEL_FLAGS sensitivity --condition $base_cond --param $param --values ${PARAMS[$param]} --n-seeds $n_seeds --output-dir output/validation/sensitivity/$param")
    done
}

phase_4() {
    local n_seeds="${SEED_OVERRIDE:-5}"
    local base_cond="full_ecosystem_balanced"

    # Cross-model comparison: Qwen is the primary model (Phase 1/2).
    # These are the additional models to compare against, in priority order.
    local models=(
        deepseek
        gemini-flash
        gpt-5
        gemini-pro
        claude-sonnet-4
    )

    local total=$(( ${#models[@]} * n_seeds ))

    echo "Phase 4: Cross-Model Robustness"
    echo "  Base condition: $base_cond (30 rounds)"
    echo "  Models: ${models[*]}"
    echo "  Seeds per model: $n_seeds"
    echo "  Total runs: $total"
    echo "  Output: output/validation/cross_model/$base_cond/<model>/seeds/"
    echo ""

    for model in "${models[@]}"; do
        COMMANDS+=("$PYTHON scripts/run_diagnostics.py --model $model --port $VLLM_PORT replicate --condition $base_cond --n-seeds $n_seeds --output-dir output/validation/cross_model/$base_cond/$model")
    done
}

# ── Dispatch ───────────────────────────────────────────────────────────────
echo "========================================"
echo "  Experiment Phase Runner  |  Phase: $PHASE"
echo "========================================"
echo ""

case "$PHASE" in
    5)    phase_5 ;;
    2p0)  phase_2p0 ;;
    2p1)  phase_2p1 ;;
    2p2)  phase_2p2 ;;
    3)    phase_3 ;;
    4)    phase_4 ;;
    *)
        echo "ERROR: Unknown phase: $PHASE"
        echo "Available: 5, 2p0, 2p1, 2p2, 3, 4"
        exit 1 ;;
esac

# ── Dry run ────────────────────────────────────────────────────────────────
if [[ "$DRY_RUN" == true ]]; then
    echo "Dry run - ${#COMMANDS[@]} commands would execute:"
    echo ""
    for i in "${!COMMANDS[@]}"; do
        echo "  [$((i+1))/${#COMMANDS[@]}] ${COMMANDS[$i]}"
    done
    echo ""
    exit 0
fi

# ── Execute ────────────────────────────────────────────────────────────────
LOG_DIR="output/reproduce_logs"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

total=${#COMMANDS[@]}
passed=0; failed=0
start_time=$(date +%s)

echo "Executing $total commands..."
echo "Logs: $LOG_DIR/"
echo ""

for i in "${!COMMANDS[@]}"; do
    cmd="${COMMANDS[$i]}"
    idx=$((i+1))
    label=$(echo "$cmd" | sed 's|.*/run_diagnostics.py ||; s/ /_/g; s/--//g' | cut -c1-60)
    log_file="$LOG_DIR/${TIMESTAMP}_phase${PHASE}_${label}.log"

    echo "[$idx/$total] $cmd"
    echo "  Log: $log_file"

    if $cmd > "$log_file" 2>&1; then
        echo "  -> PASS"; passed=$((passed+1))
    else
        echo "  -> FAIL (check log)"; failed=$((failed+1))
    fi
    echo ""
done

# ── Build runs registry ─────────────────────────────────────────────────────
echo "Building runs registry..."
if [[ -f scripts/build_registry.py ]]; then
    $PYTHON scripts/build_registry.py
    echo "Registry updated: output/runs.jsonl"
else
    echo "WARNING: scripts/build_registry.py not found — registry not updated."
    echo "  Implement build_registry.py (see EXPERIMENT_PLAN.md Runs Registry section)."
fi
echo ""

# ── Summary ────────────────────────────────────────────────────────────────
end_time=$(date +%s)
dur=$(( end_time - start_time ))
[[ $dur -lt 60 ]] && dur_str="${dur}s" || { [[ $dur -lt 3600 ]] && dur_str="$((dur/60))m $((dur%60))s" || dur_str="$((dur/3600))h $(((dur%3600)/60))m"; }

echo "========================================"
echo "  PHASE $PHASE COMPLETE"
echo "========================================"
echo "  Passed:   $passed / $total"
[[ $failed -gt 0 ]] && echo "  Failed:   $failed (check logs in $LOG_DIR/)"
echo "  Duration: $dur_str"
echo "  Logs:     $LOG_DIR/"
echo ""

case "$PHASE" in
    5|2p0|2p1|2p2)
        echo "Next: review aggregate.json files in output/validation/"
        echo "  python scripts/run_diagnostics.py analyze <batch_name>"
        ;;
    3)
        echo "Next: review sensitivity results in output/validation/sensitivity/"
        echo "  python scripts/run_diagnostics.py analyze sensitivity_<param>"
        ;;
    4)
        echo "Next: compare cross-model results in output/validation/cross_model/"
        ;;
esac
echo ""

[[ $failed -gt 0 ]] && exit 1 || exit 0
