#!/usr/bin/env bash
# reproduce.sh — Reproduce all 27 Phase 1 core experiments using any supported model.
#
# Reads config.json from output/core/<condition>/ and reruns each experiment.
# Requires Phase 1 core runs to have been completed first (configs must exist).
#
# Usage:
#   ./reproduce.sh --model <preset> [options]
#
# Model presets:
#   Local (vLLM):
#     qwen             Qwen/Qwen3-235B-A22B
#     deepseek         deepseek-ai/DeepSeek-R1
#
#   Commercial APIs:
#     claude-sonnet    Claude 3.5 Sonnet (needs ANTHROPIC_API_KEY)
#     claude-sonnet-4  Claude Sonnet 4 (needs ANTHROPIC_API_KEY)
#     gpt-5            GPT-5 (needs OPENAI_API_KEY)
#     gemini-flash     Gemini 2.5 Flash (needs GEMINI_API_KEY)
#     gemini-pro       Gemini 2.5 Pro (needs GEMINI_API_KEY)
#
# Options:
#   --model <preset>       Model to use (required)
#   --jobs N               Max concurrent experiments (default: 2)
#   --conditions A B ...   Run only specific conditions (by name)
#   --gpus 0,1,2,3         GPU selection for vLLM models
#                          NOTE: confirm available device IDs before running —
#                          the default (0,1,2,3) may not match your machine.
#   --port N               vLLM port (default: 8000)
#   --skip-server          Skip vLLM server launch (assumes already running)
#   --dry-run              Show what would run without executing
#   --help, -h             Show this help
#
# Examples:
#   ./reproduce.sh --model qwen                                    # all 27 conditions
#   ./reproduce.sh --model qwen --conditions full_ecosystem_balanced ablation_no_media_balanced
#   ./reproduce.sh --model deepseek --gpus 0,1,2,3,4,5
#   ./reproduce.sh --model gemini-flash --jobs 4
#   ./reproduce.sh --model qwen --dry-run
#
# Prerequisites:
#   - Python 3.12+ with dependencies: pip install -r requirements.txt
#   - For local models: vLLM installed, GPUs available
#   - For commercial models: API key in environment or .env file
#   - output/core/<condition>/config.json must exist for each condition
#     (run Phase 1 first; reorganize output into core/ structure)
#
# Implementation note:
#   This script calls scripts/rerun_experiment.py with --config-path to read
#   configs directly from output/core/<condition>/config.json without going
#   through index.json. The --config-path flag must be implemented in
#   rerun_experiment.py if not already present.
#
# Output:
#   - New experiment directories in output/core/
#   - Logs in output/reproduce_logs/
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ── Usage ──────────────────────────────────────────────────────────────────
usage() {
    head -52 "$0" | tail -51
}

# ── Model preset loader ───────────────────────────────────────────────────
load_preset() {
    case "$1" in
        qwen)
            PRESET_DISPLAY_NAME="Qwen3-235B-A22B (vLLM)"
            PRESET_LLM_PROVIDER="openai"
            PRESET_LLM_MODEL="Qwen/Qwen3-235B-A22B"
            PRESET_NEEDS_VLLM=true
            PRESET_DEFAULT_GPUS="0,1,2,3"
            PRESET_TP_SIZE=4
            PRESET_MAX_MODEL_LEN=16384
            PRESET_GPU_MEM_UTIL="0.95"
            PRESET_API_KEY_VAR=""
            ;;
        deepseek)
            PRESET_DISPLAY_NAME="DeepSeek-R1 (vLLM)"
            PRESET_LLM_PROVIDER="openai"
            PRESET_LLM_MODEL="deepseek-ai/DeepSeek-R1"
            PRESET_NEEDS_VLLM=true
            PRESET_DEFAULT_GPUS="0,1,2,3,4,5,6,7"
            PRESET_TP_SIZE=8
            PRESET_MAX_MODEL_LEN=16384
            PRESET_GPU_MEM_UTIL="0.95"
            PRESET_API_KEY_VAR=""
            ;;
        claude-sonnet)
            PRESET_DISPLAY_NAME="Claude 3.5 Sonnet"
            PRESET_LLM_PROVIDER="anthropic"
            PRESET_LLM_MODEL="claude-3-5-sonnet-20241022"
            PRESET_NEEDS_VLLM=false
            PRESET_DEFAULT_GPUS=""
            PRESET_TP_SIZE=0
            PRESET_MAX_MODEL_LEN=0
            PRESET_GPU_MEM_UTIL=""
            PRESET_API_KEY_VAR="ANTHROPIC_API_KEY"
            ;;
        claude-sonnet-4)
            PRESET_DISPLAY_NAME="Claude Sonnet 4"
            PRESET_LLM_PROVIDER="anthropic"
            PRESET_LLM_MODEL="claude-sonnet-4-20250514"
            PRESET_NEEDS_VLLM=false
            PRESET_DEFAULT_GPUS=""
            PRESET_TP_SIZE=0
            PRESET_MAX_MODEL_LEN=0
            PRESET_GPU_MEM_UTIL=""
            PRESET_API_KEY_VAR="ANTHROPIC_API_KEY"
            ;;
        gpt-5)
            PRESET_DISPLAY_NAME="GPT-5"
            PRESET_LLM_PROVIDER="openai"
            PRESET_LLM_MODEL="gpt-5"
            PRESET_NEEDS_VLLM=false
            PRESET_DEFAULT_GPUS=""
            PRESET_TP_SIZE=0
            PRESET_MAX_MODEL_LEN=0
            PRESET_GPU_MEM_UTIL=""
            PRESET_API_KEY_VAR="OPENAI_API_KEY"
            ;;
        gemini-flash)
            PRESET_DISPLAY_NAME="Gemini 2.5 Flash"
            PRESET_LLM_PROVIDER="gemini"
            PRESET_LLM_MODEL="gemini-2.5-flash"
            PRESET_NEEDS_VLLM=false
            PRESET_DEFAULT_GPUS=""
            PRESET_TP_SIZE=0
            PRESET_MAX_MODEL_LEN=0
            PRESET_GPU_MEM_UTIL=""
            PRESET_API_KEY_VAR="GEMINI_API_KEY"
            ;;
        gemini-pro)
            PRESET_DISPLAY_NAME="Gemini 2.5 Pro"
            PRESET_LLM_PROVIDER="gemini"
            PRESET_LLM_MODEL="gemini-2.5-pro"
            PRESET_NEEDS_VLLM=false
            PRESET_DEFAULT_GPUS=""
            PRESET_TP_SIZE=0
            PRESET_MAX_MODEL_LEN=0
            PRESET_GPU_MEM_UTIL=""
            PRESET_API_KEY_VAR="GEMINI_API_KEY"
            ;;
        *)
            echo "ERROR: Unknown model preset: $1"
            echo "Available presets: qwen, deepseek, claude-sonnet, claude-sonnet-4, gpt-5, gemini-flash, gemini-pro"
            exit 1
            ;;
    esac
}

# ── All 27 Phase 1 core conditions ─────────────────────────────────────────
ALL_CONDITIONS=(
    # Full ecosystem x 3 presets
    full_ecosystem_balanced
    full_ecosystem_us
    full_ecosystem_eu
    # No Media x 3 presets
    ablation_no_media_balanced
    ablation_no_media_us
    ablation_no_media_eu
    # No Incidents x 3 presets
    ablation_no_incidents_balanced
    ablation_no_incidents_us
    ablation_no_incidents_eu
    # No Startups x 3 presets
    ablation_no_startups_balanced
    ablation_no_startups_us
    ablation_no_startups_eu
    # No OpenCore x 3 presets
    ablation_no_opencore_balanced
    ablation_no_opencore_us
    ablation_no_opencore_eu
    # Single Benchmark x 3 presets
    ablation_single_benchmark_balanced
    ablation_single_benchmark_us
    ablation_single_benchmark_eu
    # No Funders x 3 presets
    ablation_no_funders_balanced
    ablation_no_funders_us
    ablation_no_funders_eu
    # No Benchmark Evolution x 3 presets
    ablation_no_bench_evolution_balanced
    ablation_no_bench_evolution_us
    ablation_no_bench_evolution_eu
    # Eval As Company x 3 presets
    ablation_eval_as_company_balanced
    ablation_eval_as_company_us
    ablation_eval_as_company_eu
)

# ── Defaults ────────────────────────────────────────────────────────────────
MODEL_PRESET=""
MAX_JOBS=2
DRY_RUN=false
SKIP_SERVER=false
SELECTED_CONDITIONS=()
GPU_OVERRIDE=""
VLLM_PORT=8000

# ── Parse arguments ─────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --model)
            MODEL_PRESET="$2"; shift 2 ;;
        --jobs)
            MAX_JOBS="$2"; shift 2 ;;
        --conditions)
            shift
            while [[ $# -gt 0 && ! "$1" =~ ^-- ]]; do
                SELECTED_CONDITIONS+=("$1"); shift
            done
            ;;
        --gpus)
            GPU_OVERRIDE="$2"; shift 2 ;;
        --port)
            VLLM_PORT="$2"; shift 2 ;;
        --dry-run)
            DRY_RUN=true; shift ;;
        --skip-server)
            SKIP_SERVER=true; shift ;;
        --help|-h)
            usage; exit 0 ;;
        *)
            echo "ERROR: Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if [[ -z "$MODEL_PRESET" ]]; then
    echo "ERROR: --model is required."
    usage
    exit 1
fi

load_preset "$MODEL_PRESET"

if [[ -n "$GPU_OVERRIDE" ]]; then
    if [[ "$PRESET_NEEDS_VLLM" == false ]]; then
        echo "WARNING: --gpus is ignored for commercial API model '$MODEL_PRESET'."
    else
        PRESET_DEFAULT_GPUS="$GPU_OVERRIDE"
        PRESET_TP_SIZE=$(echo "$GPU_OVERRIDE" | tr ',' '\n' | wc -l)
        echo "GPU override: $PRESET_DEFAULT_GPUS (TP=$PRESET_TP_SIZE)"
    fi
fi

# ── Load .env ────────────────────────────────────────────────────────────
if [[ -f .env ]]; then
    set -a; source .env; set +a
fi

if [[ "$PRESET_NEEDS_VLLM" == false && -n "$PRESET_API_KEY_VAR" ]]; then
    if [[ -z "${!PRESET_API_KEY_VAR:-}" ]]; then
        echo "ERROR: $PRESET_API_KEY_VAR is not set."
        exit 1
    fi
fi

# ── Resolve condition list ───────────────────────────────────────────────────
CONDITIONS=()
if [[ ${#SELECTED_CONDITIONS[@]} -gt 0 ]]; then
    CONDITIONS=("${SELECTED_CONDITIONS[@]}")
else
    CONDITIONS=("${ALL_CONDITIONS[@]}")
fi

PYTHON=$(command -v python3 || command -v python)

# ── Preflight ───────────────────────────────────────────────────────────────
echo "========================================"
echo "  Phase 1 Core Reproduction"
echo "  Model: $PRESET_DISPLAY_NAME"
if [[ "$PRESET_NEEDS_VLLM" == true ]]; then
    echo "  GPUs:  $PRESET_DEFAULT_GPUS (TP=$PRESET_TP_SIZE)"
    echo "  NOTE:  Confirm GPU device IDs match your machine before running"
    echo "  Port:  $VLLM_PORT"
fi
echo "  Conditions: ${#CONDITIONS[@]}"
echo "  Max concurrent jobs: $MAX_JOBS"
echo "========================================"
echo ""

missing=0
for cond in "${CONDITIONS[@]}"; do
    config="output/core/$cond/config.json"
    if [[ ! -f "$config" ]]; then
        echo "WARNING: Missing config: $config"
        missing=$((missing + 1))
    fi
done
if [[ $missing -gt 0 ]]; then
    echo ""
    echo "ERROR: $missing config(s) missing in output/core/."
    echo "Phase 1 core runs must be completed and reorganized into output/core/"
    echo "before reproduce.sh can rerun them."
    exit 1
fi

# ── Dry run ─────────────────────────────────────────────────────────────────
if [[ "$DRY_RUN" == true ]]; then
    echo "Dry run - would execute:"
    echo "  Model: $PRESET_DISPLAY_NAME"
    if [[ "$PRESET_NEEDS_VLLM" == true ]]; then
        echo ""
        echo "  vLLM: CUDA_VISIBLE_DEVICES=$PRESET_DEFAULT_GPUS python -m vllm.entrypoints.openai.api_server \\"
        echo "    --model $PRESET_LLM_MODEL --tensor-parallel-size $PRESET_TP_SIZE --port $VLLM_PORT"
    fi
    echo ""
    for cond in "${CONDITIONS[@]}"; do
        echo "  $PYTHON scripts/rerun_experiment.py --config-path output/core/$cond/config.json"
    done
    echo ""
    echo "Total: ${#CONDITIONS[@]} conditions"
    exit 0
fi

# ── Log directory ────────────────────────────────────────────────────────────
LOG_DIR="output/reproduce_logs"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# ── vLLM server ──────────────────────────────────────────────────────────────
VLLM_PID=""

cleanup() {
    if [[ -n "$VLLM_PID" ]] && kill -0 "$VLLM_PID" 2>/dev/null; then
        echo "Shutting down vLLM server (PID $VLLM_PID)..."
        kill "$VLLM_PID" 2>/dev/null || true
        wait "$VLLM_PID" 2>/dev/null || true
        echo "vLLM server stopped."
    fi
}
trap cleanup EXIT

if [[ "$PRESET_NEEDS_VLLM" == true && "$SKIP_SERVER" == false ]]; then
    VLLM_LOG="$LOG_DIR/${TIMESTAMP}_vllm_server.log"
    echo "Starting vLLM server..."
    echo "  Model: $PRESET_LLM_MODEL"
    echo "  GPUs:  $PRESET_DEFAULT_GPUS (TP=$PRESET_TP_SIZE)"
    echo "  Port:  $VLLM_PORT  |  Log: $VLLM_LOG"
    echo ""

    CUDA_VISIBLE_DEVICES=$PRESET_DEFAULT_GPUS $PYTHON -m vllm.entrypoints.openai.api_server \
        --model "$PRESET_LLM_MODEL" \
        --tensor-parallel-size "$PRESET_TP_SIZE" \
        --max-model-len "$PRESET_MAX_MODEL_LEN" \
        --gpu-memory-utilization "$PRESET_GPU_MEM_UTIL" \
        --trust-remote-code \
        --port "$VLLM_PORT" \
        --disable-log-requests \
        > "$VLLM_LOG" 2>&1 &
    VLLM_PID=$!

    echo "Waiting for vLLM server (PID $VLLM_PID)..."
    MAX_WAIT=600; WAITED=0
    while [[ $WAITED -lt $MAX_WAIT ]]; do
        if ! kill -0 "$VLLM_PID" 2>/dev/null; then
            echo "ERROR: vLLM exited. Check: $VLLM_LOG"
            tail -30 "$VLLM_LOG"; exit 1
        fi
        if curl -s "http://localhost:$VLLM_PORT/health" > /dev/null 2>&1; then
            echo "vLLM ready (${WAITED}s)"; break
        fi
        sleep 5; WAITED=$((WAITED + 5))
        [[ $((WAITED % 30)) -eq 0 ]] && echo "  Still waiting... (${WAITED}s)"
    done
    [[ $WAITED -ge $MAX_WAIT ]] && { echo "ERROR: vLLM timeout. Check: $VLLM_LOG"; exit 1; }
    echo ""
elif [[ "$PRESET_NEEDS_VLLM" == true && "$SKIP_SERVER" == true ]]; then
    echo "Skipping vLLM server launch. Assuming server at port $VLLM_PORT."
    curl -s "http://localhost:$VLLM_PORT/health" > /dev/null 2>&1 \
        && echo "vLLM server reachable." \
        || echo "WARNING: vLLM not responding at port $VLLM_PORT."
    echo ""
fi

# ── Set LLM environment ──────────────────────────────────────────────────────
if [[ "$PRESET_NEEDS_VLLM" == true ]]; then
    export LLM_PROVIDER="openai"
    export LLM_MODEL="$PRESET_LLM_MODEL"
    export OPENAI_API_KEY="dummy"
    export OPENAI_BASE_URL="http://localhost:$VLLM_PORT/v1"
else
    export LLM_PROVIDER="$PRESET_LLM_PROVIDER"
    export LLM_MODEL="$PRESET_LLM_MODEL"
    unset OPENAI_BASE_URL 2>/dev/null || true
fi

echo "LLM environment:"
echo "  LLM_PROVIDER=$LLM_PROVIDER  LLM_MODEL=$LLM_MODEL"
[[ "$PRESET_NEEDS_VLLM" == true ]] && echo "  OPENAI_BASE_URL=$OPENAI_BASE_URL"
echo ""

# ── Run conditions ──────────────────────────────────────────────────────────
declare -a PIDS=()
declare -a COND_NAMES=()
declare -a LOG_FILES=()
declare -a START_TIMES=()

running_jobs() {
    local count=0
    for pid in "${PIDS[@]}"; do
        kill -0 "$pid" 2>/dev/null && count=$((count + 1))
    done
    echo "$count"
}

echo "Starting at $(date)"
echo ""

for cond in "${CONDITIONS[@]}"; do
    while [[ $(running_jobs) -ge $MAX_JOBS ]]; do sleep 1; done

    log_file="$LOG_DIR/${TIMESTAMP}_${MODEL_PRESET}_${cond}.log"
    echo "[LAUNCH] $cond -> $log_file"

    # NOTE: rerun_experiment.py must support --config-path for this to work.
    # Without --config-path, it falls back to index.json lookup which will not
    # find output/core/ entries.
    $PYTHON scripts/rerun_experiment.py \
        --config-path "output/core/$cond/config.json" \
        > "$log_file" 2>&1 &

    PIDS+=("$!")
    COND_NAMES+=("$cond")
    LOG_FILES+=("$log_file")
    START_TIMES+=("$(date +%s)")
    sleep 3
done

echo ""
echo "All conditions launched. Waiting for completion..."
echo ""

declare -a STATUSES=()
declare -a DURATIONS=()

for i in "${!PIDS[@]}"; do
    wait "${PIDS[$i]}" && STATUSES+=("PASS") || STATUSES+=("FAIL")
    end=$(date +%s)
    dur=$((end - START_TIMES[$i]))
    DURATIONS+=("$dur")
    [[ $dur -lt 60 ]] && ds="${dur}s" || { [[ $dur -lt 3600 ]] && ds="$((dur/60))m $((dur%60))s" || ds="$((dur/3600))h $(((dur%3600)/60))m"; }
    echo "[${STATUSES[$i]}] ${COND_NAMES[$i]}  ($ds)"
done

echo ""
echo "========================================"
echo "  $PRESET_DISPLAY_NAME REPRODUCTION SUMMARY"
echo "========================================"
pass_count=0; fail_count=0
printf "%-45s  %-6s  %s\n" "CONDITION" "STATUS" "DURATION"
printf "%-45s  %-6s  %s\n" "---------" "------" "--------"
for i in "${!COND_NAMES[@]}"; do
    dur=${DURATIONS[$i]}
    [[ $dur -lt 60 ]] && ds="${dur}s" || { [[ $dur -lt 3600 ]] && ds="$((dur/60))m $((dur%60))s" || ds="$((dur/3600))h $(((dur%3600)/60))m"; }
    printf "%-45s  %-6s  %s\n" "${COND_NAMES[$i]}" "${STATUSES[$i]}" "$ds"
    [[ "${STATUSES[$i]}" == "PASS" ]] && pass_count=$((pass_count+1)) || fail_count=$((fail_count+1))
done
echo ""
echo "Passed: $pass_count / ${#COND_NAMES[@]}"
[[ $fail_count -gt 0 ]] && echo "Failed: $fail_count (check logs in $LOG_DIR/)"
echo "Logs: $LOG_DIR/"
[[ $fail_count -gt 0 ]] && exit 1 || exit 0
