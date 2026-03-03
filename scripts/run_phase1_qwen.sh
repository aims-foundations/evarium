#!/usr/bin/env bash
# run_phase1_qwen.sh — Start vLLM with Qwen3-235B, then run all 27 Phase 1 core experiments.
# Intended to run inside tmux so it survives session disconnects.
#
# Usage:
#   ./scripts/run_phase1_qwen.sh
#
# This script:
#   1. Starts vLLM server on all 8 GPUs (TP=8)
#   2. Waits for Phase 5 heuristic to finish (if running) to avoid index.json conflicts
#   3. Runs all 27 conditions sequentially
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

# Use ecosystem conda env and LFS HuggingFace cache
eval "$(conda shell.bash hook 2>/dev/null)"
conda activate ecosystem 2>/dev/null || true
export HF_HOME="/lfs/skampere1/0/sttruong/.cache/huggingface"

PYTHON=$(command -v python3 || command -v python)
VLLM_PORT=8000
VLLM_MODEL="Qwen/Qwen3-235B-A22B"
VLLM_GPUS="0,1,2,3,4,5,6,7"
VLLM_TP=8

LOG_DIR="output/reproduce_logs"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
VLLM_LOG="$LOG_DIR/${TIMESTAMP}_vllm_qwen_phase1.log"
RUN_LOG="$LOG_DIR/${TIMESTAMP}_phase1_qwen.log"

# ── Start vLLM server ────────────────────────────────────────────────────
echo "========================================"
echo "  Starting vLLM: $VLLM_MODEL"
echo "  GPUs: $VLLM_GPUS (TP=$VLLM_TP)"
echo "  Port: $VLLM_PORT"
echo "  Log:  $VLLM_LOG"
echo "========================================"
echo ""

CUDA_VISIBLE_DEVICES=$VLLM_GPUS $PYTHON -m vllm.entrypoints.openai.api_server \
    --model "$VLLM_MODEL" \
    --tensor-parallel-size "$VLLM_TP" \
    --max-model-len 16384 \
    --gpu-memory-utilization 0.95 \
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
while [ $WAITED -lt $MAX_WAIT ]; do
    if ! kill -0 "$VLLM_PID" 2>/dev/null; then
        echo "ERROR: vLLM exited unexpectedly. Check: $VLLM_LOG"
        tail -30 "$VLLM_LOG"
        exit 1
    fi
    if curl -s "http://localhost:$VLLM_PORT/health" > /dev/null 2>&1; then
        echo "vLLM ready! (${WAITED}s)"
        break
    fi
    sleep 5; WAITED=$((WAITED + 5))
    if [ $((WAITED % 30)) -eq 0 ]; then
        echo "  Still loading... (${WAITED}s)"
    fi
done
if [ $WAITED -ge $MAX_WAIT ]; then
    echo "ERROR: vLLM timeout after ${MAX_WAIT}s. Check: $VLLM_LOG"
    exit 1
fi
echo ""

# ── Set LLM environment ──────────────────────────────────────────────────
export LLM_PROVIDER=openai
export LLM_MODEL="$VLLM_MODEL"
export OPENAI_API_KEY=dummy
export OPENAI_BASE_URL="http://localhost:$VLLM_PORT/v1"

echo "LLM environment set:"
echo "  LLM_PROVIDER=$LLM_PROVIDER"
echo "  LLM_MODEL=$LLM_MODEL"
echo "  OPENAI_BASE_URL=$OPENAI_BASE_URL"
echo ""

# ── Wait for Phase 5 heuristic to finish (if running) ────────────────────
# Phase 5 and Phase 1 both write to index.json without locking.
# Wait for any run_phase5_heuristic.sh process to finish.
echo "Checking for running Phase 5 heuristic..."
while pgrep -f "run_phase5_heuristic" > /dev/null 2>&1; do
    echo "  Phase 5 still running. Waiting 60s..."
    sleep 60
done
echo "  No Phase 5 process detected. Proceeding."
echo ""

# ── All 27 conditions ─────────────────────────────────────────────────────
CONDITIONS=(
    # Full ecosystem (3) — highest priority
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
echo "  Phase 1: Qwen Core Runs (LLM mode)"
echo "  Conditions: $total"
echo "  Rounds per condition: 30"
echo "  Started: $(date)"
echo "========================================"
echo ""

{
for i in "${!CONDITIONS[@]}"; do
    IFS=: read -r exp_id label <<< "${CONDITIONS[$i]}"
    idx=$((i + 1))

    echo ""
    echo "================================================================"
    echo "  [$idx/$total] $label ($exp_id)"
    echo "  $(date)"
    echo "================================================================"

    cond_start=$(date +%s)

    if $PYTHON scripts/rerun_experiment.py "$exp_id"; then
        cond_end=$(date +%s)
        dur=$((cond_end - cond_start))
        echo ""
        echo "  [$idx/$total] $label — PASS (${dur}s)"
        passed=$((passed + 1))
    else
        cond_end=$(date +%s)
        dur=$((cond_end - cond_start))
        echo ""
        echo "  [$idx/$total] $label — FAIL (${dur}s)"
        failed=$((failed + 1))
    fi
done

end_time=$(date +%s)
total_dur=$((end_time - start_time))

echo ""
echo "========================================"
echo "  Phase 1 COMPLETE"
echo "  Passed: $passed / $total"
if [ $failed -gt 0 ]; then
    echo "  Failed: $failed"
fi
echo "  Duration: $((total_dur / 3600))h $(((total_dur % 3600) / 60))m"
echo "  Finished: $(date)"
echo "========================================"
} 2>&1 | tee "$RUN_LOG"
