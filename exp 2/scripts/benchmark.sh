#!/usr/bin/env bash
# ==============================================================================
# Experiment 2: Memory Performance Benchmark Automation Suite
# Target Environments: Virtual Machine (Native) vs Docker Container
# Workload: Sysbench Memory Benchmark (Write Operations)
# ==============================================================================

set -euo pipefail

# ------------------------------------------------------------------------------
# Configuration Variables
# ------------------------------------------------------------------------------
RUNS=${RUNS:-10}
BLOCK_SIZE=${BLOCK_SIZE:-"1M"}
TOTAL_SIZE=${TOTAL_SIZE:-"10G"}
THREADS=${THREADS:-4}
OPER=${OPER:-"write"}
SCOPE=${SCOPE:-"global"}
IMAGE_NAME=${IMAGE_NAME:-"vm-container-benchmark"}

# Directory resolution relative to script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXP_DIR="$(dirname "$SCRIPT_DIR")"
RAW_DIR="$EXP_DIR/results/raw/memory"
VM_RAW_DIR="$RAW_DIR/vm"
CONTAINER_RAW_DIR="$RAW_DIR/container"

mkdir -p "$VM_RAW_DIR" "$CONTAINER_RAW_DIR"

echo "=================================================================="
echo " Starting Experiment 2: Memory Benchmark Automation"
echo " Repetitions:         $RUNS iterations per environment"
echo " Block Size:          $BLOCK_SIZE"
echo " Total Transfer:      $TOTAL_SIZE"
echo " Threads:             $THREADS"
echo " Operation:           $OPER ($SCOPE)"
echo " Image Name:          $IMAGE_NAME"
echo "=================================================================="

# ------------------------------------------------------------------------------
# 1. Native Virtual Machine Benchmark Iterations
# ------------------------------------------------------------------------------
echo ""
echo ">>> [Phase 1/2] Running VM Memory Benchmarks ($RUNS runs)..."
for i in $(seq 1 "$RUNS"); do
    OUT_FILE="$VM_RAW_DIR/run_$i.txt"
    echo -n "    - Executing VM Run #$i/$RUNS ... "
    sysbench memory \
        --memory-block-size="$BLOCK_SIZE" \
        --memory-total-size="$TOTAL_SIZE" \
        --threads="$THREADS" \
        --memory-oper="$OPER" \
        --memory-scope="$SCOPE" \
        run > "$OUT_FILE"
    echo "Done -> $OUT_FILE"
done

# ------------------------------------------------------------------------------
# 2. Docker Container Benchmark Iterations
# ------------------------------------------------------------------------------
echo ""
echo ">>> [Phase 2/2] Running Docker Container Memory Benchmarks ($RUNS runs)..."
# Check if container image exists
if ! docker image inspect "$IMAGE_NAME" >/dev/null 2>&1; then
    echo "[-] Error: Docker image '$IMAGE_NAME' not found."
    echo "    Please build it first: docker build -t $IMAGE_NAME -f '$EXP_DIR/docker/Dockerfile' '$EXP_DIR'"
    exit 1
fi

for i in $(seq 1 "$RUNS"); do
    OUT_FILE="$CONTAINER_RAW_DIR/run_$i.txt"
    echo -n "    - Executing Container Run #$i/$RUNS ... "
    docker run --rm "$IMAGE_NAME" \
        sysbench memory \
        --memory-block-size="$BLOCK_SIZE" \
        --memory-total-size="$TOTAL_SIZE" \
        --threads="$THREADS" \
        --memory-oper="$OPER" \
        --memory-scope="$SCOPE" \
        run > "$OUT_FILE"
    echo "Done -> $OUT_FILE"
done

echo ""
echo "=================================================================="
echo " Benchmark Execution Complete!"
echo " Raw results stored at:"
echo "   VM:        $VM_RAW_DIR"
echo "   Container: $CONTAINER_RAW_DIR"
echo " Next step: Run 'python3 scripts/parse_sysbench.py' to analyze results."
echo "=================================================================="
