#!/usr/bin/env bash
# run_phase.sh — Run all experiments for a given phase from EXPERIMENT_PLAN.md.
#
# Usage:
#   ./run_phase.sh --phase <phase> [options]
#
# Phases:
#   5      Heuristic baseline (free, no LLM calls, 11 conditions x 10 seeds)
#   2p0    P0 replications: 3 full-ecosystem conditions x 10 seeds
#   2p1    P1 replications: 3 key ablations x 10 seeds
#   2p2    P2 replications: 5 remaining ablations x 10 seeds
#   3      Sensitivity sweeps: 6 parameters x 5 levels x 3 seeds
#   4      Cross-model comparison: exp_013 with multiple models x 5 seeds
#
# Options:
#   --phase <phase>        Phase to run (required)
#   --model <preset>       Model preset (passed to run_diagnostics.py)
#   --port N               vLLM port (default: 8000)
#   --n-seeds N            Override default seed count
#   --dry-run              Show commands without executing
#   --help, -h             Show this help
#
# Examples:
#   ./run_phase.sh --phase 5                                  # heuristic baseline (free)
#   ./run_phase.sh --phase 2p0 --model claude-sonnet          # P0 replications
#   ./run_phase.sh --phase 3 --model gemini-flash             # sensitivity sweeps
#   ./run_phase.sh --phase 4                                  # cross-model comparison
#   ./run_phase.sh --phase 5 --dry-run                        # show what would run
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ── Usage ──────────────────────────────────────────────────────────────────
usage() {
    head -30 "$0" | tail -29
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
        --phase)
            PHASE="$2"; shift 2 ;;
        --model)
            MODEL_PRESET="$2"; shift 2 ;;
        --port)
            VLLM_PORT="$2"; shift 2 ;;
        --n-seeds)
            SEED_OVERRIDE="$2"; shift 2 ;;
        --dry-run)
            DRY_RUN=true; shift ;;
        --help|-h)
            usage; exit 0 ;;
        *)
            echo "ERROR: Unknown option: $1"
            echo ""
            usage
            exit 1
            ;;
    esac
done

if [[ -z "$PHASE" ]]; then
    echo "ERROR: --phase is required."
    echo ""
    usage
    exit 1
fi

# Check Python
if ! command -v python3 &>/dev/null && ! command -v python &>/dev/null; then
    echo "ERROR: python3 not found."
    exit 1
fi
PYTHON=$(command -v python3 || command -v python)

# ── Build model flags ──────────────────────────────────────────────────────
MODEL_FLAGS=""
if [[ -n "$MODEL_PRESET" ]]; then
    MODEL_FLAGS="--model $MODEL_PRESET --port $VLLM_PORT"
fi

# ── Phase definitions ──────────────────────────────────────────────────────
# Each phase function populates the COMMANDS array with run_diagnostics.py commands.
declare -a COMMANDS=()

phase_5() {
    # Heuristic baseline: all 11 unique conditions, 10 seeds each
    local n_seeds="${SEED_OVERRIDE:-10}"

    local experiments=(
        exp_011  # Full Ecosystem, Balanced (baseline)
        exp_001  # Full Ecosystem, US light-touch
        exp_002  # Full Ecosystem, EU precautionary
        exp_004  # No Media
        exp_005  # No Incidents
        exp_006  # No Startups
        exp_007  # No OpenCore
        exp_008  # Single Benchmark
        exp_009  # No Funders
        exp_010  # No Benchmark Evolution
        exp_012  # Eval As Company
    )

    echo "Phase 5: Heuristic Baseline"
    echo "  Conditions: ${#experiments[@]}"
    echo "  Seeds per condition: $n_seeds"
    echo "  Total runs: $(( ${#experiments[@]} * n_seeds ))"
    echo "  Cost: FREE (no LLM calls)"
    echo ""

    for exp in "${experiments[@]}"; do
        COMMANDS+=("$PYTHON scripts/run_diagnostics.py replicate $exp --n-seeds $n_seeds --heuristic")
    done
}

phase_2p0() {
    # P0: 3 full-ecosystem conditions (50 rounds), 10 seeds each
    local n_seeds="${SEED_OVERRIDE:-10}"

    if [[ -z "$MODEL_PRESET" ]]; then
        echo "ERROR: Phase 2p0 requires --model (LLM replications)."
        exit 1
    fi

    local experiments=(
        exp_013  # Full Ecosystem, Balanced, 50 rounds
        exp_014  # Full Ecosystem, US light-touch, 50 rounds
        exp_015  # Full Ecosystem, EU precautionary, 50 rounds
    )

    echo "Phase 2 P0: Full Ecosystem Replications"
    echo "  Model: $MODEL_PRESET"
    echo "  Conditions: ${#experiments[@]} (50 rounds each)"
    echo "  Seeds per condition: $n_seeds"
    echo "  Total runs: $(( ${#experiments[@]} * n_seeds ))"
    echo ""

    for exp in "${experiments[@]}"; do
        COMMANDS+=("$PYTHON scripts/run_diagnostics.py $MODEL_FLAGS replicate $exp --n-seeds $n_seeds")
    done
}

phase_2p1() {
    # P1: 3 key ablations (30 rounds), 10 seeds each
    local n_seeds="${SEED_OVERRIDE:-10}"

    if [[ -z "$MODEL_PRESET" ]]; then
        echo "ERROR: Phase 2p1 requires --model (LLM replications)."
        exit 1
    fi

    local experiments=(
        exp_006  # No Startups
        exp_007  # No OpenCore
        exp_008  # Single Benchmark
    )

    echo "Phase 2 P1: Key Ablation Replications"
    echo "  Model: $MODEL_PRESET"
    echo "  Conditions: ${#experiments[@]} (30 rounds each)"
    echo "  Seeds per condition: $n_seeds"
    echo "  Total runs: $(( ${#experiments[@]} * n_seeds ))"
    echo ""

    for exp in "${experiments[@]}"; do
        COMMANDS+=("$PYTHON scripts/run_diagnostics.py $MODEL_FLAGS replicate $exp --n-seeds $n_seeds")
    done
}

phase_2p2() {
    # P2: 5 remaining ablations (30 rounds), 10 seeds each
    local n_seeds="${SEED_OVERRIDE:-10}"

    if [[ -z "$MODEL_PRESET" ]]; then
        echo "ERROR: Phase 2p2 requires --model (LLM replications)."
        exit 1
    fi

    local experiments=(
        exp_004  # No Media
        exp_005  # No Incidents
        exp_009  # No Funders
        exp_010  # No Benchmark Evolution
        exp_012  # Eval As Company
    )

    echo "Phase 2 P2: Remaining Ablation Replications"
    echo "  Model: $MODEL_PRESET"
    echo "  Conditions: ${#experiments[@]} (30 rounds each)"
    echo "  Seeds per condition: $n_seeds"
    echo "  Total runs: $(( ${#experiments[@]} * n_seeds ))"
    echo ""

    for exp in "${experiments[@]}"; do
        COMMANDS+=("$PYTHON scripts/run_diagnostics.py $MODEL_FLAGS replicate $exp --n-seeds $n_seeds")
    done
}

phase_3() {
    # Sensitivity sweeps: 6 parameters x 5 levels x 3 seeds = 90 runs
    local n_seeds="${SEED_OVERRIDE:-3}"
    local base_exp="exp_011"

    if [[ -z "$MODEL_PRESET" ]]; then
        echo "ERROR: Phase 3 requires --model (LLM sensitivity sweeps)."
        echo "  Tip: use --model gemini-flash for budget sweeps."
        exit 1
    fi

    # Parameter sweeps from EXPERIMENT_PLAN.md
    declare -A PARAMS
    PARAMS[rnd_efficiency]="0.005,0.008,0.01,0.012,0.015"
    PARAMS[benchmark_validity_decay_rate]="0.01,0.015,0.02,0.03,0.04"
    PARAMS[benchmark_exploitability_growth_rate]="0.005,0.01,0.015,0.02,0.03"
    PARAMS[startup_entry_probability]="0,0.05,0.09,0.15,0.25"
    PARAMS[capability_ceiling]="0.7,0.85,1.0,1.2"
    PARAMS[diminishing_returns_rate]="1.5,2.0,3.0,4.0,5.0"

    local n_params=${#PARAMS[@]}
    echo "Phase 3: Sensitivity Analysis"
    echo "  Model: $MODEL_PRESET"
    echo "  Base experiment: $base_exp"
    echo "  Parameters: $n_params"
    echo "  Seeds per point: $n_seeds"
    echo ""

    for param in "${!PARAMS[@]}"; do
        local values="${PARAMS[$param]}"
        COMMANDS+=("$PYTHON scripts/run_diagnostics.py $MODEL_FLAGS sensitivity $base_exp --param $param --values $values --n-seeds $n_seeds")
    done
}

phase_4() {
    # Cross-model comparison: full ecosystem balanced (50 rounds) with multiple models
    local n_seeds="${SEED_OVERRIDE:-5}"
    local base_exp="exp_013"

    # Models to compare (from EXPERIMENT_PLAN.md)
    local models=(
        claude-sonnet-4
        gpt-5
        gemini-flash
        gemini-pro
    )

    echo "Phase 4: Cross-Model Robustness"
    echo "  Base experiment: $base_exp (50 rounds)"
    echo "  Models: ${models[*]}"
    echo "  Seeds per model: $n_seeds"
    echo "  Total runs: $(( ${#models[@]} * n_seeds ))"
    echo ""

    for model in "${models[@]}"; do
        COMMANDS+=("$PYTHON scripts/run_diagnostics.py --model $model --port $VLLM_PORT replicate $base_exp --n-seeds $n_seeds")
    done
}

# ── Dispatch phase ─────────────────────────────────────────────────────────
echo "========================================"
echo "  Experiment Phase Runner"
echo "  Phase: $PHASE"
echo "========================================"
echo ""

case "$PHASE" in
    5)       phase_5 ;;
    2p0)     phase_2p0 ;;
    2p1)     phase_2p1 ;;
    2p2)     phase_2p2 ;;
    3)       phase_3 ;;
    4)       phase_4 ;;
    *)
        echo "ERROR: Unknown phase: $PHASE"
        echo "Available phases: 5, 2p0, 2p1, 2p2, 3, 4"
        exit 1
        ;;
esac

# ── Dry run ────────────────────────────────────────────────────────────────
if [[ "$DRY_RUN" == true ]]; then
    echo "Dry run - would execute ${#COMMANDS[@]} batch commands:"
    echo ""
    for i in "${!COMMANDS[@]}"; do
        echo "  [$((i + 1))/${#COMMANDS[@]}] ${COMMANDS[$i]}"
    done
    echo ""
    exit 0
fi

# ── Execute ────────────────────────────────────────────────────────────────
LOG_DIR="output/reproduce_logs"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

total=${#COMMANDS[@]}
passed=0
failed=0
start_time=$(date +%s)

echo "Executing ${total} batch commands..."
echo "Logs: $LOG_DIR/"
echo ""

for i in "${!COMMANDS[@]}"; do
    cmd="${COMMANDS[$i]}"
    idx=$((i + 1))

    # Extract a short label from the command for the log filename
    label=$(echo "$cmd" | sed 's|.*/run_diagnostics.py ||; s/ /_/g; s/--//g' | cut -c1-60)
    log_file="$LOG_DIR/${TIMESTAMP}_phase${PHASE}_${label}.log"

    echo "[$idx/$total] $cmd"
    echo "  Log: $log_file"

    if $cmd > "$log_file" 2>&1; then
        echo "  -> PASS"
        passed=$((passed + 1))
    else
        echo "  -> FAIL (check log)"
        failed=$((failed + 1))
    fi
    echo ""
done

# ── Summary ────────────────────────────────────────────────────────────────
end_time=$(date +%s)
duration=$((end_time - start_time))

if [[ $duration -lt 60 ]]; then
    dur_str="${duration}s"
elif [[ $duration -lt 3600 ]]; then
    dur_str="$((duration / 60))m $((duration % 60))s"
else
    dur_str="$((duration / 3600))h $(( (duration % 3600) / 60 ))m"
fi

echo "========================================"
echo "  PHASE $PHASE COMPLETE"
echo "========================================"
echo ""
echo "  Passed: $passed / $total"
if [[ $failed -gt 0 ]]; then
    echo "  Failed: $failed (check logs in $LOG_DIR/)"
fi
echo "  Duration: $dur_str"
echo "  Logs: $LOG_DIR/"
echo ""

# Suggest analysis commands
case "$PHASE" in
    5|2p0|2p1|2p2)
        echo "Next step: analyze the batches with:"
        echo "  python scripts/run_diagnostics.py list-batches"
        echo "  python scripts/run_diagnostics.py analyze <batch_name>"
        ;;
    3)
        echo "Next step: analyze the sensitivity sweeps with:"
        echo "  python scripts/run_diagnostics.py list-batches"
        echo "  python scripts/run_diagnostics.py analyze sensitivity_<param>_exp_011_full_ecosystem_balanced"
        ;;
    4)
        echo "Next step: compare cross-model results with:"
        echo "  python scripts/run_diagnostics.py list-batches"
        ;;
esac
echo ""

if [[ $failed -gt 0 ]]; then
    exit 1
fi
