#!/usr/bin/env bash
# reproduce_deepseek.sh — Reproduce all 15 experiments using DeepSeek-R1 via vLLM.
#
# Usage:
#   ./reproduce_deepseek.sh                        # start vLLM + run all 15 experiments
#   ./reproduce_deepseek.sh --jobs 4               # run 4 experiments at a time
#   ./reproduce_deepseek.sh --experiments 1 2 3    # run only exp_001, exp_002, exp_003
#   ./reproduce_deepseek.sh --dry-run              # show what would run without executing
#   ./reproduce_deepseek.sh --skip-server          # skip vLLM launch (server already running)
#
# Prerequisites:
#   - Python 3.12+ with dependencies: pip install -r requirements.txt
#   - vLLM installed: pip install vllm
#   - GPUs 0-5 available (6x GPU for tensor parallelism)
#
# Output:
#   - New experiment directories in output/experiments/
#   - Logs in output/reproduce_logs/
#   - vLLM server log in output/reproduce_logs/vllm_server.log
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ── vLLM / DeepSeek-R1 Configuration ─────────────────────────────────────
VLLM_MODEL="deepseek-ai/DeepSeek-R1"
VLLM_PORT=8000
VLLM_GPUS="0,1,2,3"
VLLM_TP=4                        # tensor-parallel-size (must match GPU count)
VLLM_MAX_MODEL_LEN=16384         # reduce from 64K default to save GPU memory
VLLM_GPU_MEMORY_UTILIZATION=0.95 # fraction of GPU memory to use

# ── All 15 experiments ──────────────────────────────────────────────────────
ALL_EXPERIMENTS=(
    exp_001_full_ecosystem_us
    exp_002_full_ecosystem_eu
    exp_003_full_ecosystem_us
    exp_004_ablation_no_media_balanced
    exp_005_ablation_no_incidents_balanced
    exp_006_ablation_no_startups_balanced
    exp_007_ablation_no_opencore_balanced
    exp_008_ablation_single_benchmark_balanced
    exp_009_ablation_no_funders_balanced
    exp_010_ablation_no_benchmark_evolution_balanced
    exp_011_full_ecosystem_balanced
    exp_012_ablation_eval_as_company_balanced
    exp_013_full_ecosystem_balanced
    exp_014_full_ecosystem_us
    exp_015_full_ecosystem_eu
)

# ── Defaults ────────────────────────────────────────────────────────────────
MAX_JOBS=2
DRY_RUN=false
SKIP_SERVER=false
SELECTED_NUMS=()

# ── Parse arguments ─────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --jobs)
            MAX_JOBS="$2"; shift 2 ;;
        --experiments)
            shift
            while [[ $# -gt 0 && ! "$1" =~ ^-- ]]; do
                SELECTED_NUMS+=("$1"); shift
            done
            ;;
        --dry-run)
            DRY_RUN=true; shift ;;
        --skip-server)
            SKIP_SERVER=true; shift ;;
        --help|-h)
            head -16 "$0" | tail -15; exit 0 ;;
        *)
            echo "Unknown option: $1"; exit 1 ;;
    esac
done

# ── Resolve experiment list ─────────────────────────────────────────────────
EXPERIMENTS=()
if [[ ${#SELECTED_NUMS[@]} -gt 0 ]]; then
    for num in "${SELECTED_NUMS[@]}"; do
        padded=$(printf "%03d" "$num")
        found=false
        for exp in "${ALL_EXPERIMENTS[@]}"; do
            if [[ "$exp" == exp_${padded}_* ]]; then
                EXPERIMENTS+=("$exp")
                found=true
                break
            fi
        done
        if [[ "$found" == false ]]; then
            echo "ERROR: No experiment matching exp_${padded}_*"
            exit 1
        fi
    done
else
    EXPERIMENTS=("${ALL_EXPERIMENTS[@]}")
fi

# ── Preflight checks ───────────────────────────────────────────────────────
echo "========================================"
echo "  DeepSeek-R1 Reproduction Run"
echo "  Model: $VLLM_MODEL"
echo "  GPUs:  $VLLM_GPUS (TP=$VLLM_TP)"
echo "  Experiments: ${#EXPERIMENTS[@]}"
echo "  Max concurrent jobs: $MAX_JOBS"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &>/dev/null && ! command -v python &>/dev/null; then
    echo "ERROR: python3 not found. Install Python 3.12+."
    exit 1
fi
PYTHON=$(command -v python3 || command -v python)

# Check configs exist
missing=0
for exp in "${EXPERIMENTS[@]}"; do
    config="output/experiments/$exp/config.json"
    if [[ ! -f "$config" ]]; then
        echo "ERROR: Missing config: $config"
        missing=$((missing + 1))
    fi
done
if [[ $missing -gt 0 ]]; then
    echo "ERROR: $missing config(s) missing. Cannot reproduce."
    exit 1
fi

# ── Dry run ─────────────────────────────────────────────────────────────────
if [[ "$DRY_RUN" == true ]]; then
    echo "Dry run - would execute:"
    echo ""
    echo "  vLLM server: CUDA_VISIBLE_DEVICES=$VLLM_GPUS python -m vllm.entrypoints.openai.api_server \\"
    echo "    --model $VLLM_MODEL --tensor-parallel-size $VLLM_TP --port $VLLM_PORT"
    echo ""
    for exp in "${EXPERIMENTS[@]}"; do
        rounds=$(${PYTHON} -c "import json; print(json.load(open('output/experiments/$exp/config.json'))['n_rounds'])")
        echo "  $PYTHON scripts/rerun_experiment.py $exp    ($rounds rounds)"
    done
    echo ""
    echo "Total: ${#EXPERIMENTS[@]} experiments"
    exit 0
fi

# ── Start vLLM server ──────────────────────────────────────────────────────
LOG_DIR="output/reproduce_logs"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
VLLM_LOG="$LOG_DIR/${TIMESTAMP}_vllm_server.log"
VLLM_PID=""

cleanup() {
    if [[ -n "$VLLM_PID" ]] && kill -0 "$VLLM_PID" 2>/dev/null; then
        echo ""
        echo "Shutting down vLLM server (PID $VLLM_PID)..."
        kill "$VLLM_PID" 2>/dev/null || true
        wait "$VLLM_PID" 2>/dev/null || true
        echo "vLLM server stopped."
    fi
}
trap cleanup EXIT

if [[ "$SKIP_SERVER" == false ]]; then
    echo "Starting vLLM server..."
    echo "  Model: $VLLM_MODEL"
    echo "  GPUs:  $VLLM_GPUS (TP=$VLLM_TP)"
    echo "  Port:  $VLLM_PORT"
    echo "  Max context: $VLLM_MAX_MODEL_LEN"
    echo "  Log:   $VLLM_LOG"
    echo ""

    CUDA_VISIBLE_DEVICES=$VLLM_GPUS $PYTHON -m vllm.entrypoints.openai.api_server \
        --model "$VLLM_MODEL" \
        --tensor-parallel-size "$VLLM_TP" \
        --max-model-len "$VLLM_MAX_MODEL_LEN" \
        --gpu-memory-utilization "$VLLM_GPU_MEMORY_UTILIZATION" \
        --trust-remote-code \
        --port "$VLLM_PORT" \
        --disable-log-requests \
        > "$VLLM_LOG" 2>&1 &
    VLLM_PID=$!

    echo "vLLM server starting (PID $VLLM_PID)..."
    echo "Waiting for server to be ready (this may take several minutes for DeepSeek-R1)..."

    # Wait for vLLM to be ready (check /health endpoint)
    MAX_WAIT=600  # 10 minutes max
    WAITED=0
    while [[ $WAITED -lt $MAX_WAIT ]]; do
        if ! kill -0 "$VLLM_PID" 2>/dev/null; then
            echo ""
            echo "ERROR: vLLM server exited unexpectedly. Check log: $VLLM_LOG"
            tail -30 "$VLLM_LOG"
            exit 1
        fi

        if curl -s "http://localhost:$VLLM_PORT/health" > /dev/null 2>&1; then
            echo ""
            echo "vLLM server is ready! (took ${WAITED}s)"
            break
        fi

        sleep 5
        WAITED=$((WAITED + 5))
        # Print progress every 30 seconds
        if [[ $((WAITED % 30)) -eq 0 ]]; then
            echo "  Still waiting... (${WAITED}s elapsed)"
        fi
    done

    if [[ $WAITED -ge $MAX_WAIT ]]; then
        echo ""
        echo "ERROR: vLLM server did not become ready within ${MAX_WAIT}s."
        echo "Check log: $VLLM_LOG"
        tail -30 "$VLLM_LOG"
        exit 1
    fi
else
    echo "Skipping vLLM server launch (--skip-server). Assuming server at port $VLLM_PORT."
    # Verify server is reachable
    if ! curl -s "http://localhost:$VLLM_PORT/health" > /dev/null 2>&1; then
        echo "WARNING: vLLM server not responding at http://localhost:$VLLM_PORT/health"
        echo "Make sure the server is running before experiments start."
    else
        echo "vLLM server is reachable at port $VLLM_PORT."
    fi
    echo ""
fi

# ── Set environment for OpenAI-compatible vLLM endpoint ─────────────────────
export LLM_PROVIDER="openai"
export LLM_MODEL="$VLLM_MODEL"
export OPENAI_API_KEY="dummy"  # vLLM doesn't require a real key
export OPENAI_BASE_URL="http://localhost:$VLLM_PORT/v1"

echo "LLM environment:"
echo "  LLM_PROVIDER=$LLM_PROVIDER"
echo "  LLM_MODEL=$LLM_MODEL"
echo "  OPENAI_BASE_URL=$OPENAI_BASE_URL"
echo ""

# ── Run experiments ─────────────────────────────────────────────────────────
declare -a PIDS=()
declare -a EXP_NAMES=()
declare -a LOG_FILES=()
declare -a START_TIMES=()

running_jobs() {
    local count=0
    for pid in "${PIDS[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then
            count=$((count + 1))
        fi
    done
    echo "$count"
}

echo "Starting reproduction run at $(date)"
echo "Logs: $LOG_DIR/"
echo ""

for exp in "${EXPERIMENTS[@]}"; do
    # Wait if at max concurrent jobs
    while [[ $(running_jobs) -ge $MAX_JOBS ]]; do
        sleep 1
    done

    log_file="$LOG_DIR/${TIMESTAMP}_deepseek_${exp}.log"
    echo "[LAUNCH] $exp -> $log_file"

    $PYTHON scripts/rerun_experiment.py "$exp" > "$log_file" 2>&1 &
    pid=$!

    PIDS+=("$pid")
    EXP_NAMES+=("$exp")
    LOG_FILES+=("$log_file")
    START_TIMES+=("$(date +%s)")

    # Stagger launches to avoid ExperimentLogger index.json race condition
    sleep 3
done

echo ""
echo "All experiments launched. Waiting for completion..."
echo ""

# ── Wait and collect results ────────────────────────────────────────────────
declare -a STATUSES=()
declare -a DURATIONS=()

for i in "${!PIDS[@]}"; do
    pid="${PIDS[$i]}"
    exp="${EXP_NAMES[$i]}"
    start="${START_TIMES[$i]}"

    if wait "$pid"; then
        status="PASS"
    else
        status="FAIL"
    fi

    end=$(date +%s)
    duration=$((end - start))

    STATUSES+=("$status")
    DURATIONS+=("$duration")

    # Format duration
    if [[ $duration -lt 60 ]]; then
        dur_str="${duration}s"
    elif [[ $duration -lt 3600 ]]; then
        dur_str="$((duration / 60))m $((duration % 60))s"
    else
        dur_str="$((duration / 3600))h $(( (duration % 3600) / 60 ))m"
    fi

    echo "[$status] $exp  ($dur_str)"
done

# ── Summary ─────────────────────────────────────────────────────────────────
echo ""
echo "========================================"
echo "  DEEPSEEK-R1 REPRODUCTION SUMMARY"
echo "========================================"
echo ""

pass_count=0
fail_count=0

printf "%-50s  %-6s  %s\n" "EXPERIMENT" "STATUS" "DURATION"
printf "%-50s  %-6s  %s\n" "----------" "------" "--------"

for i in "${!EXP_NAMES[@]}"; do
    dur="${DURATIONS[$i]}"
    if [[ $dur -lt 60 ]]; then
        dur_str="${dur}s"
    elif [[ $dur -lt 3600 ]]; then
        dur_str="$((dur / 60))m $((dur % 60))s"
    else
        dur_str="$((dur / 3600))h $(( (dur % 3600) / 60 ))m"
    fi

    printf "%-50s  %-6s  %s\n" "${EXP_NAMES[$i]}" "${STATUSES[$i]}" "$dur_str"

    if [[ "${STATUSES[$i]}" == "PASS" ]]; then
        pass_count=$((pass_count + 1))
    else
        fail_count=$((fail_count + 1))
    fi
done

echo ""
echo "Passed: $pass_count / ${#EXP_NAMES[@]}"
if [[ $fail_count -gt 0 ]]; then
    echo "Failed: $fail_count (check logs in $LOG_DIR/)"
fi
echo "Logs:   $LOG_DIR/"
echo ""

if [[ $fail_count -gt 0 ]]; then
    exit 1
fi
