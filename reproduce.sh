#!/usr/bin/env bash
# reproduce.sh — Reproduce all 15 experiments using any supported model.
#
# Usage:
#   ./reproduce.sh --model <preset> [options]
#
# Model presets:
#   Local (vLLM):
#     qwen             Qwen/Qwen3-235B-A22B (4 GPUs, TP=4)
#     deepseek         deepseek-ai/DeepSeek-R1 (6 GPUs, TP=6)
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
#   --experiments N N N    Run only specific experiments (by number)
#   --gpus 0,1,2,3        Override GPU selection (vLLM models only)
#   --port N               Override vLLM port (default: 8000)
#   --skip-server          Skip vLLM server launch (assumes already running)
#   --dry-run              Show what would run without executing
#   --help, -h             Show this help
#
# Examples:
#   ./reproduce.sh --model qwen                            # Qwen via vLLM
#   ./reproduce.sh --model deepseek --gpus 0,1,2,3,4,5    # DeepSeek with specific GPUs
#   ./reproduce.sh --model claude-sonnet --jobs 4          # Claude, 4 concurrent
#   ./reproduce.sh --model gpt-5 --experiments 1 2 3      # GPT-5, only 3 experiments
#   ./reproduce.sh --model gemini-flash --dry-run          # Dry run with Gemini Flash
#
# Prerequisites:
#   - Python 3.12+ with dependencies: pip install -r requirements.txt
#   - For local models: vLLM installed (pip install vllm), GPUs available
#   - For commercial models: API key set in environment or .env file
#
# Output:
#   - New experiment directories in output/experiments/
#   - Logs in output/reproduce_logs/
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ── Usage ──────────────────────────────────────────────────────────────────
usage() {
    head -42 "$0" | tail -41
}

# ── Model preset loader ───────────────────────────────────────────────────
# Each preset sets:
#   PRESET_DISPLAY_NAME   — human-readable name for banners/logs
#   PRESET_LLM_PROVIDER   — openai | anthropic | gemini
#   PRESET_LLM_MODEL      — model ID string
#   PRESET_NEEDS_VLLM     — true for local models, false for commercial
#   PRESET_DEFAULT_GPUS   — CUDA_VISIBLE_DEVICES value (vLLM only)
#   PRESET_TP_SIZE        — tensor parallel size (vLLM only)
#   PRESET_MAX_MODEL_LEN  — max context length (vLLM only)
#   PRESET_GPU_MEM_UTIL   — GPU memory utilization fraction (vLLM only)
#   PRESET_API_KEY_VAR    — env var name to check for API key (commercial only)

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
            echo ""
            echo "Available presets:"
            echo "  Local (vLLM):    qwen, deepseek"
            echo "  Commercial API:  claude-sonnet, claude-sonnet-4, gpt-5, gemini-flash, gemini-pro"
            exit 1
            ;;
    esac
}

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
MODEL_PRESET=""
MAX_JOBS=2
DRY_RUN=false
SKIP_SERVER=false
SELECTED_NUMS=()
GPU_OVERRIDE=""
VLLM_PORT=8000

# ── Parse arguments ─────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --model)
            MODEL_PRESET="$2"; shift 2 ;;
        --jobs)
            MAX_JOBS="$2"; shift 2 ;;
        --experiments)
            shift
            while [[ $# -gt 0 && ! "$1" =~ ^-- ]]; do
                SELECTED_NUMS+=("$1"); shift
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
            echo ""
            usage
            exit 1
            ;;
    esac
done

# ── Validate --model ──────────────────────────────────────────────────────
if [[ -z "$MODEL_PRESET" ]]; then
    echo "ERROR: --model is required."
    echo ""
    usage
    exit 1
fi

load_preset "$MODEL_PRESET"

# ── Apply GPU override (vLLM only) ──────────────────────────────────────
if [[ -n "$GPU_OVERRIDE" ]]; then
    if [[ "$PRESET_NEEDS_VLLM" == false ]]; then
        echo "WARNING: --gpus is ignored for commercial API model '$MODEL_PRESET'."
    else
        PRESET_DEFAULT_GPUS="$GPU_OVERRIDE"
        PRESET_TP_SIZE=$(echo "$GPU_OVERRIDE" | tr ',' '\n' | wc -l)
        echo "GPU override: $PRESET_DEFAULT_GPUS (TP=$PRESET_TP_SIZE)"
    fi
fi

# ── Load .env for API keys ──────────────────────────────────────────────
if [[ -f .env ]]; then
    set -a
    source .env
    set +a
fi

# ── Validate API key for commercial models ───────────────────────────────
if [[ "$PRESET_NEEDS_VLLM" == false && -n "$PRESET_API_KEY_VAR" ]]; then
    if [[ -z "${!PRESET_API_KEY_VAR:-}" ]]; then
        echo "ERROR: $PRESET_API_KEY_VAR is not set."
        echo "  For model '$MODEL_PRESET', set $PRESET_API_KEY_VAR in your environment or .env file."
        exit 1
    fi
fi

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
echo "  Reproduction Run"
echo "  Model: $PRESET_DISPLAY_NAME"
if [[ "$PRESET_NEEDS_VLLM" == true ]]; then
    echo "  GPUs:  $PRESET_DEFAULT_GPUS (TP=$PRESET_TP_SIZE)"
    echo "  Port:  $VLLM_PORT"
fi
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
    echo "  Model:    $PRESET_DISPLAY_NAME"
    echo "  Provider: $PRESET_LLM_PROVIDER"
    echo "  Model ID: $PRESET_LLM_MODEL"
    if [[ "$PRESET_NEEDS_VLLM" == true ]]; then
        echo ""
        echo "  vLLM server: CUDA_VISIBLE_DEVICES=$PRESET_DEFAULT_GPUS python -m vllm.entrypoints.openai.api_server \\"
        echo "    --model $PRESET_LLM_MODEL --tensor-parallel-size $PRESET_TP_SIZE --port $VLLM_PORT"
    fi
    echo ""
    for exp in "${EXPERIMENTS[@]}"; do
        rounds=$(${PYTHON} -c "import json; print(json.load(open('output/experiments/$exp/config.json'))['n_rounds'])")
        echo "  $PYTHON scripts/rerun_experiment.py $exp    ($rounds rounds)"
    done
    echo ""
    echo "Total: ${#EXPERIMENTS[@]} experiments"
    exit 0
fi

# ── Log directory setup ─────────────────────────────────────────────────────
LOG_DIR="output/reproduce_logs"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# ── vLLM server (local models only) ─────────────────────────────────────────
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

if [[ "$PRESET_NEEDS_VLLM" == true ]]; then
    if [[ "$SKIP_SERVER" == false ]]; then
        VLLM_LOG="$LOG_DIR/${TIMESTAMP}_vllm_server.log"

        echo "Starting vLLM server..."
        echo "  Model: $PRESET_LLM_MODEL"
        echo "  GPUs:  $PRESET_DEFAULT_GPUS (TP=$PRESET_TP_SIZE)"
        echo "  Port:  $VLLM_PORT"
        echo "  Max context: $PRESET_MAX_MODEL_LEN"
        echo "  Log:   $VLLM_LOG"
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

        echo "vLLM server starting (PID $VLLM_PID)..."
        echo "Waiting for server to be ready..."

        MAX_WAIT=600  # 10 minutes
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
        if ! curl -s "http://localhost:$VLLM_PORT/health" > /dev/null 2>&1; then
            echo "WARNING: vLLM server not responding at http://localhost:$VLLM_PORT/health"
            echo "Make sure the server is running before experiments start."
        else
            echo "vLLM server is reachable at port $VLLM_PORT."
        fi
        echo ""
    fi
fi

# ── Set LLM environment variables ───────────────────────────────────────────
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
echo "  LLM_PROVIDER=$LLM_PROVIDER"
echo "  LLM_MODEL=$LLM_MODEL"
if [[ "$PRESET_NEEDS_VLLM" == true ]]; then
    echo "  OPENAI_BASE_URL=$OPENAI_BASE_URL"
fi
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

    log_file="$LOG_DIR/${TIMESTAMP}_${MODEL_PRESET}_${exp}.log"
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
echo "  ${PRESET_DISPLAY_NAME} REPRODUCTION SUMMARY"
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
