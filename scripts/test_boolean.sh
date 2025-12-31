#!/bin/bash
# Test script for N-Queens Boolean Model
# Author: Lorenzo Domenico Attolico
# Student ID: 48259726

set -e

export AMPLIFY_TOKEN="AE/0dEHTizNQ2sDganC2KKPCZjs75CUj2nA"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
cd "$PROJECT_ROOT"

echo "N-Queens Boolean Model Testing"
echo "Author: Lorenzo Domenico Attolico (48259726)"
echo ""

n_values=(8 10 15 20 25 30 40 50 60 70 80 90 100)

mkdir -p results solutions

output_file="results/boolean_results.csv"
echo "n,time_ms,status,solver" > "$output_file"

SOLVER="org.minizinc.mip.coin-bc"
TIMEOUT=120000

echo "Running Boolean Model experiments..."
echo ""

for n in "${n_values[@]}"; do
    echo "Testing n=$n"
    
    echo "n = $n;" > temp_n${n}.dzn
    
    start_time=$(python3 -c 'import time; print(int(time.time() * 1000))')
    
    minizinc models/nqueens_boolean.mzn temp_n${n}.dzn \
        --solver "$SOLVER" \
        --time-limit $TIMEOUT \
        > temp_output_${n}.txt 2>&1
    
    end_time=$(python3 -c 'import time; print(int(time.time() * 1000))')
    elapsed_ms=$((end_time - start_time))
    
    if grep -q "Q" temp_output_${n}.txt; then
        status="SOLVED"
    else
        status="ERROR"
    fi
    
    echo "$n,$elapsed_ms,$status,$SOLVER" >> "$output_file"
    
    elapsed_sec=$(python3 -c "print(f'{$elapsed_ms/1000:.3f}')")
    echo "  Status: $status, Time: ${elapsed_sec}s"
    
    if [ "$status" = "SOLVED" ] && [ $n -le 15 ]; then
        cp temp_output_${n}.txt solutions/solution_boolean_n${n}.txt
    fi
done

rm -f temp_n*.dzn temp_output_*.txt

echo ""
echo "Done. Results saved to: $output_file"
