#!/usr/bin/env bash
# reproduce.sh — Reproduce all 15 experiments from the paper.
#
# Usage:
#   ./reproduce.sh                        # run all 15 experiments (2 concurrent)
#   ./reproduce.sh --jobs 4               # run 4 experiments at a time
#   ./reproduce.sh --experiments 1 2 3    # run only exp_001, exp_002, exp_003
#   ./reproduce.sh --dry-run              # show what would run without executing
#
# Prerequisites:
#   - Python 3.12+ with dependencies: pip install -r requirements.txt
#   - .env file with API keys (ANTHROPIC_API_KEY at minimum)
#
# Output:
#   - New experiment directories in output/experiments/
#   - Logs in output/reproduce_logs/
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

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
        --help|-h)
            head -14 "$0" | tail -13; exit 0 ;;
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
echo "  Reproduce: ${#EXPERIMENTS[@]} experiments"
echo "  Max concurrent jobs: $MAX_JOBS"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &>/dev/null && ! command -v python &>/dev/null; then
    echo "ERROR: python3 not found. Install Python 3.12+."
    exit 1
fi
PYTHON=$(command -v python3 || command -v python)

# Check .env
if [[ ! -f .env ]]; then
    echo "WARNING: .env file not found. LLM experiments need API keys."
    echo "  Create .env with: ANTHROPIC_API_KEY=sk-..."
    echo ""
fi

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
    for exp in "${EXPERIMENTS[@]}"; do
        rounds=$(${PYTHON} -c "import json; print(json.load(open('output/experiments/$exp/config.json'))['n_rounds'])")
        echo "  $PYTHON scripts/rerun_experiment.py $exp    ($rounds rounds)"
    done
    echo ""
    echo "Total: ${#EXPERIMENTS[@]} experiments"
    exit 0
fi

# ── Run experiments ─────────────────────────────────────────────────────────
LOG_DIR="output/reproduce_logs"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Arrays to track results
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

    log_file="$LOG_DIR/${TIMESTAMP}_${exp}.log"
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
echo "  REPRODUCTION SUMMARY"
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
