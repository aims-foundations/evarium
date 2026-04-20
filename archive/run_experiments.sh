#!/usr/bin/env bash
# run_experiments.sh — Run experiment conditions with a local vLLM server.
#
# Edit the arrays at the top to control what runs. Comment out conditions,
# presets, or seeds you don't need.
#
# Usage:
#   tmux new-session -s experiments
#   ./run_experiments.sh
#   # Ctrl+B D to detach; tmux attach -t experiments to reattach
#
#   # Heuristic only (no vLLM):
#   MODE=heuristic ./run_experiments.sh
#
#   # Dry run:
#   DRY_RUN=1 ./run_experiments.sh
#
#   # Skip existing (resume after failure):
#   SKIP_EXISTING=1 ./run_experiments.sh
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

# ── What to run ───────────────────────────────────────────────────────────
# Comment out what you don't need.

CONDITIONS=(
    full_ecosystem
    # --- Structural ablations ---
    no_media
    no_funders
    no_regulator
    no_opensource
    no_incidents
    # --- Mechanism ablations ---
    bm_orientation_max
    bm_orientation_adjustable
    dynamic_evaluator
    eval_as_company
    aligned_benchmarks
    # --- Internal validity ---
    homogeneous_consumers
)

PRESETS=(balanced us eu)

# Phase 1: single seed. Phase 2: $(seq 1 30). Phase 5: $(seq 1 30)
SEEDS=(1)

# "llm" or "heuristic"
MODE="${MODE:-llm}"

ROUNDS=30

# ── vLLM configuration (only used when MODE=llm) ─────────────────────────
# CONFIRM these match your available GPUs before running (nvidia-smi).
VLLM_MODEL="Qwen/Qwen3-235B-A22B"
VLLM_GPUS="0,1,3,4"
VLLM_TP=4
VLLM_PORT=8000
VLLM_MAX_MODEL_LEN=16384
VLLM_GPU_MEM_UTIL=0.95

# LLM provider flag for run_experiment.py.
# "openai" for vLLM (OpenAI-compatible API), "anthropic"/"gemini" for cloud.
PROVIDER="openai"

# ── Flags ─────────────────────────────────────────────────────────────────
DRY_RUN="${DRY_RUN:-0}"
SKIP_EXISTING="${SKIP_EXISTING:-0}"

PYTHON=$(command -v python3 || command -v python)
LOG_DIR="output/experiment_logs"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# ── vLLM server ───────────────────────────────────────────────────────────
VLLM_PID=""

start_vllm() {
    local log="$LOG_DIR/${TIMESTAMP}_vllm.log"
    echo "Starting vLLM: $VLLM_MODEL (GPUs: $VLLM_GPUS, TP=$VLLM_TP, port $VLLM_PORT)"
    echo "  Log: $log"

    CUDA_VISIBLE_DEVICES=$VLLM_GPUS $PYTHON -m vllm.entrypoints.openai.api_server \
        --model "$VLLM_MODEL" \
        --tensor-parallel-size "$VLLM_TP" \
        --max-model-len "$VLLM_MAX_MODEL_LEN" \
        --gpu-memory-utilization "$VLLM_GPU_MEM_UTIL" \
        --trust-remote-code \
        --port "$VLLM_PORT" \
        --disable-log-requests \
        > "$log" 2>&1 &
    VLLM_PID=$!

    echo "Waiting for vLLM (PID $VLLM_PID)..."
    local waited=0
    while [[ $waited -lt 600 ]]; do
        if ! kill -0 "$VLLM_PID" 2>/dev/null; then
            echo "ERROR: vLLM exited. Check: $log"
            tail -20 "$log"; exit 1
        fi
        if curl -s "http://localhost:$VLLM_PORT/health" > /dev/null 2>&1; then
            echo "vLLM ready (${waited}s)"
            return
        fi
        sleep 5; waited=$((waited + 5))
        [[ $((waited % 30)) -eq 0 ]] && echo "  Loading... (${waited}s)"
    done
    echo "ERROR: vLLM timeout. Check: $log"; exit 1
}

stop_vllm() {
    if [[ -n "$VLLM_PID" ]]; then
        echo "Shutting down vLLM (PID $VLLM_PID)..."
        kill "$VLLM_PID" 2>/dev/null || true
        wait "$VLLM_PID" 2>/dev/null || true
    fi
}

# ── Run one experiment ────────────────────────────────────────────────────
run_one() {
    local condition="$1" preset="$2" seed="$3"
    local label="${condition}/${preset}/seed_${seed}"

    # Skip existing
    if [[ "$SKIP_EXISTING" == "1" ]]; then
        # Check hf_data for existing rounds.jsonl
        local model_slug="qwen-235b"
        [[ "$PROVIDER" == "anthropic" ]] && model_slug="claude-sonnet-4-6"
        [[ "$PROVIDER" == "gemini" ]] && model_slug="gemini-flash"
        local base_dir
        if [[ "$MODE" == "heuristic" ]]; then
            base_dir="hf_data/heuristic_baseline/${condition}_${preset}/seeds/seed_${seed}"
        else
            base_dir="hf_data/llm_core/${model_slug}/${condition}_${preset}/seeds/seed_${seed}"
        fi
        if [[ -f "$base_dir/rounds.jsonl" ]]; then
            echo "  SKIP $label (exists)"
            return 0
        fi
    fi

    local cmd=(
        "$PYTHON" scripts/run_experiment.py
        --condition "$condition"
        --policy "$preset"
        --mode "$MODE"
        --seed "$seed"
        --rounds "$ROUNDS"
    )
    [[ "$MODE" == "llm" ]] && cmd+=(--provider "$PROVIDER")

    if [[ "$DRY_RUN" == "1" ]]; then
        echo "  $label"
        echo "    ${cmd[*]}"
        return 0
    fi

    local run_log="$LOG_DIR/${TIMESTAMP}_${condition}_${preset}_seed${seed}.log"
    echo -n "  $label ... "

    if "${cmd[@]}" > "$run_log" 2>&1; then
        echo "OK ($(date +%H:%M:%S))"
        return 0
    else
        echo "FAIL (see $run_log)"
        tail -5 "$run_log" | sed 's/^/    /'
        return 1
    fi
}

# ── Main ──────────────────────────────────────────────────────────────────
n_jobs=$(( ${#CONDITIONS[@]} * ${#PRESETS[@]} * ${#SEEDS[@]} ))

echo "========================================"
echo "  Experiments: $n_jobs jobs"
echo "  Conditions: ${#CONDITIONS[@]} | Presets: ${#PRESETS[@]} | Seeds: ${#SEEDS[@]}"
echo "  Mode: $MODE | Rounds: $ROUNDS"
[[ "$MODE" == "llm" ]] && echo "  Provider: $PROVIDER | Model: $VLLM_MODEL"
[[ "$DRY_RUN" == "1" ]] && echo "  [DRY RUN]"
[[ "$SKIP_EXISTING" == "1" ]] && echo "  [SKIP EXISTING]"
echo "========================================"
echo ""

# Set env vars for vLLM-backed runs
if [[ "$MODE" == "llm" && "$PROVIDER" == "openai" ]]; then
    export LLM_PROVIDER=openai
    export LLM_MODEL="$VLLM_MODEL"
    export OPENAI_API_KEY=dummy
    export OPENAI_BASE_URL="http://localhost:$VLLM_PORT/v1"

    if [[ "$DRY_RUN" != "1" ]]; then
        # Check if vLLM is already running
        if curl -s "http://localhost:$VLLM_PORT/health" > /dev/null 2>&1; then
            echo "vLLM already running on port $VLLM_PORT"
        else
            start_vllm
            trap stop_vllm EXIT
        fi
    fi
fi

completed=0
failed=0
skipped=0
start_time=$(date +%s)

for condition in "${CONDITIONS[@]}"; do
    for preset in "${PRESETS[@]}"; do
        for seed in "${SEEDS[@]}"; do
            if run_one "$condition" "$preset" "$seed"; then
                completed=$((completed + 1))
            else
                failed=$((failed + 1))
            fi
        done
    done
done

end_time=$(date +%s)
elapsed=$(( (end_time - start_time) / 60 ))

echo ""
echo "========================================"
echo "  FINISHED in ${elapsed}m"
echo "  Completed: $completed | Failed: $failed"
echo "  Logs: $LOG_DIR/"
echo "========================================"
