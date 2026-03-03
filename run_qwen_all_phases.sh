#!/usr/bin/env bash
# run_qwen_all_phases.sh — Start vLLM with Qwen and run all LLM phases in priority order.
# Intended to run inside tmux.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

VLLM_MODEL="Qwen/Qwen3-235B-A22B"
VLLM_PORT=8000
VLLM_GPUS="0,1,3,4"
VLLM_TP=4
VLLM_MAX_MODEL_LEN=16384
VLLM_GPU_MEM_UTIL=0.95

LOG_DIR="output/reproduce_logs"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
VLLM_LOG="$LOG_DIR/${TIMESTAMP}_vllm_qwen_server.log"

PYTHON=$(command -v python3 || command -v python)

# ── Start vLLM server ──────────────────────────────────────────────────────
echo "========================================"
echo "  Starting vLLM for Qwen3-235B-A22B"
echo "  GPUs: $VLLM_GPUS (TP=$VLLM_TP)"
echo "  Port: $VLLM_PORT"
echo "  Log:  $VLLM_LOG"
echo "========================================"
echo ""

CUDA_VISIBLE_DEVICES=$VLLM_GPUS $PYTHON -m vllm.entrypoints.openai.api_server \
    --model "$VLLM_MODEL" \
    --tensor-parallel-size "$VLLM_TP" \
    --max-model-len "$VLLM_MAX_MODEL_LEN" \
    --gpu-memory-utilization "$VLLM_GPU_MEM_UTIL" \
    --trust-remote-code \
    --port "$VLLM_PORT" \
    --disable-log-requests \
    > "$VLLM_LOG" 2>&1 &
VLLM_PID=$!

cleanup() {
    echo ""
    echo "Shutting down vLLM server (PID $VLLM_PID)..."
    kill "$VLLM_PID" 2>/dev/null || true
    wait "$VLLM_PID" 2>/dev/null || true
    echo "Done."
}
trap cleanup EXIT

echo "Waiting for vLLM to be ready (PID $VLLM_PID)..."
MAX_WAIT=600
WAITED=0
while [[ $WAITED -lt $MAX_WAIT ]]; do
    if ! kill -0 "$VLLM_PID" 2>/dev/null; then
        echo "ERROR: vLLM exited. Check $VLLM_LOG"
        tail -30 "$VLLM_LOG"
        exit 1
    fi
    if curl -s "http://localhost:$VLLM_PORT/health" > /dev/null 2>&1; then
        echo "vLLM ready! (${WAITED}s)"
        break
    fi
    sleep 5
    WAITED=$((WAITED + 5))
    [[ $((WAITED % 30)) -eq 0 ]] && echo "  Still loading... (${WAITED}s)"
done
if [[ $WAITED -ge $MAX_WAIT ]]; then
    echo "ERROR: vLLM timeout. Check $VLLM_LOG"
    exit 1
fi
echo ""

# ── Run LLM phases in priority order ──────────────────────────────────────
echo "========================================"
echo "  Running LLM Phases with Qwen"
echo "========================================"
echo ""

run_phase() {
    local phase="$1"
    local label="$2"
    echo ""
    echo "================================================================"
    echo "  Starting: $label"
    echo "  $(date)"
    echo "================================================================"
    echo ""
    ./run_phase.sh --phase "$phase" --model qwen
    echo ""
    echo "$label COMPLETE at $(date)"
    echo ""
}

# Priority order from EXPERIMENT_PLAN.md:
# 1. Phase 2 P0 — most important for paper (3 conditions x 10 seeds)
# 2. Phase 3   — sensitivity sweeps (addresses reviewer concerns)
# 3. Phase 2 P1 — key ablation replications
# 4. Phase 2 P2 — remaining ablation replications

run_phase 2p0 "Phase 2 P0: Full Ecosystem Replications (30 runs)"
run_phase 3   "Phase 3: Sensitivity Sweeps (90 runs)"
run_phase 2p1 "Phase 2 P1: Key Ablation Replications (30 runs)"
run_phase 2p2 "Phase 2 P2: Remaining Ablation Replications (50 runs)"

echo ""
echo "========================================"
echo "  ALL LLM PHASES COMPLETE"
echo "  $(date)"
echo "========================================"
