#!/usr/bin/env bash
# run_qwen_all_phases.sh — Start vLLM with Qwen and run all phases in priority order.
# Intended to run inside tmux on a machine with local GPUs.
#
# Execution order (from EXPERIMENT_PLAN.md):
#   1. Phase 5  — Heuristic baseline (free, fast, validates infrastructure)
#   2. Phase 2p0 — Full-ecosystem x 3 presets (most important for paper, 90 runs)
#   3. Phase 4  — Cross-model comparison (DeepSeek first, then cloud; 25 runs)
#   4. Phase 2p1 — High-signal ablations x 3 presets (90 runs)
#   5. Phase 3  — Sensitivity sweeps (105 runs)
#   6. Phase 2p2 — Remaining ablation replications (450 runs)
#
# Note: Phase 4 requires separate model servers/API keys per model and is NOT
# run automatically here (it uses multiple different models). After Phase 2p0
# completes, run Phase 4 manually per model. Phase 3 can use gemini-flash for
# budget runs; update MODEL_PRESET_PHASE3 below if desired.
#
# GPU configuration:
#   VLLM_GPUS defaults to "0,1,3,4" with TP=4 (as used in prior runs).
#   CONFIRM available device IDs on your machine before running —
#   use `nvidia-smi` to list devices and update VLLM_GPUS and VLLM_TP accordingly.
#
# Usage:
#   tmux new-session -s qwen
#   ./run_qwen_all_phases.sh
#   # Ctrl+B D to detach; tmux attach -t qwen to reattach
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

# ── Configuration ──────────────────────────────────────────────────────────
VLLM_MODEL="Qwen/Qwen3-235B-A22B"
VLLM_PORT=8000

# CONFIRM these match your available GPUs before running (use nvidia-smi).
VLLM_GPUS="0,1,3,4"
VLLM_TP=4

VLLM_MAX_MODEL_LEN=16384
VLLM_GPU_MEM_UTIL=0.95

# Model preset for Phase 3 sensitivity sweeps.
# Use "gemini-flash" for budget runs (~$0), "qwen" to use the local server.
MODEL_PRESET_PHASE3="qwen"

LOG_DIR="output/reproduce_logs"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
VLLM_LOG="$LOG_DIR/${TIMESTAMP}_vllm_qwen_server.log"

PYTHON=$(command -v python3 || command -v python)

# ── Start vLLM server ──────────────────────────────────────────────────────
echo "========================================"
echo "  Starting vLLM: Qwen3-235B-A22B"
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
MAX_WAIT=600; WAITED=0
while [[ $WAITED -lt $MAX_WAIT ]]; do
    if ! kill -0 "$VLLM_PID" 2>/dev/null; then
        echo "ERROR: vLLM exited unexpectedly. Check: $VLLM_LOG"
        tail -30 "$VLLM_LOG"; exit 1
    fi
    if curl -s "http://localhost:$VLLM_PORT/health" > /dev/null 2>&1; then
        echo "vLLM ready! (${WAITED}s)"; break
    fi
    sleep 5; WAITED=$((WAITED + 5))
    [[ $((WAITED % 30)) -eq 0 ]] && echo "  Still loading... (${WAITED}s)"
done
[[ $WAITED -ge $MAX_WAIT ]] && { echo "ERROR: vLLM timeout. Check: $VLLM_LOG"; exit 1; }
echo ""

# ── Helper ────────────────────────────────────────────────────────────────
run_phase() {
    local phase="$1"
    local label="$2"
    local extra_args="${3:-}"
    echo ""
    echo "================================================================"
    echo "  Starting: $label"
    echo "  $(date)"
    echo "================================================================"
    echo ""
    ./run_phase.sh --phase "$phase" --model qwen --port "$VLLM_PORT" $extra_args
    echo ""
    echo "$label COMPLETE at $(date)"
    echo ""
}

# ── Run phases in priority order ───────────────────────────────────────────
echo "========================================"
echo "  Running All Phases with Qwen3-235B"
echo "  Total LLM runs: ~645 (2p0: 90, 2p1: 270, 2p2: 450, 3: 105 at 3 seeds)"
echo "  Plus Phase 5 (heuristic, free): 810 runs"
echo "========================================"
echo ""

# Phase 5: Heuristic baseline — free, fast, validates infrastructure.
# No vLLM needed; run first to confirm the pipeline works end-to-end.
echo "================================================================"
echo "  Starting: Phase 5 — Heuristic Baseline (810 runs, free)"
echo "  $(date)"
echo "================================================================"
echo ""
./run_phase.sh --phase 5
echo ""
echo "Phase 5 COMPLETE at $(date)"
echo ""

# Phase 2 P0: Full ecosystem x 3 presets, 30 seeds each (90 runs).
# Most important for the paper — establish primary CIs first.
run_phase 2p0 "Phase 2 P0: Full Ecosystem Replications (90 runs)"

# Phase 2 P1: High-signal ablations x 3 presets, 30 seeds each (270 runs).
run_phase 2p1 "Phase 2 P1: High-Signal Ablation Replications (270 runs)"

# Phase 3: Sensitivity sweeps, 7 parameters x ~5 levels x 3 seeds (~105 runs).
# Uses MODEL_PRESET_PHASE3 (default: qwen; set to gemini-flash for budget runs).
if [[ "$MODEL_PRESET_PHASE3" == "qwen" ]]; then
    run_phase 3 "Phase 3: Sensitivity Sweeps (~105 runs)"
else
    echo ""
    echo "================================================================"
    echo "  Starting: Phase 3 — Sensitivity Sweeps (~105 runs)"
    echo "  Model: $MODEL_PRESET_PHASE3 (cloud — vLLM server not used)"
    echo "  $(date)"
    echo "================================================================"
    echo ""
    ./run_phase.sh --phase 3 --model "$MODEL_PRESET_PHASE3"
    echo ""
    echo "Phase 3 COMPLETE at $(date)"
    echo ""
fi

# Phase 2 P2: Remaining ablations x 3 presets, 30 seeds each (450 runs).
run_phase 2p2 "Phase 2 P2: Remaining Ablation Replications (450 runs)"

echo ""
echo "========================================"
echo "  ALL PHASES COMPLETE"
echo "  $(date)"
echo "========================================"
echo ""
echo "Phase 4 (cross-model comparison) must be run separately per model."
echo "Use: ./run_phase.sh --phase 4 --model <preset>"
echo "Priority order: deepseek, gemini-flash, gpt-5, gemini-pro, claude-sonnet-4"
echo ""
echo "Runs registry: output/runs.jsonl (rebuilt after each phase by run_phase.sh)"
