#!/bin/bash
# Test script for N-Queens Integer Model
# Author: Lorenzo Domenico Attolico
# Student ID: 48259726

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
cd "$PROJECT_ROOT"

echo "N-Queens Integer Model Testing"
echo "Author: Lorenzo Domenico Attolico (48259726)"
echo ""

n_values=(8 10 15 20 25 30 40 50 60 70 80 90 100)

mkdir -p results solutions

output_json="results/integer_results.json"
output_csv="results/integer_results.csv"

echo "[" > "$output_json"
echo "n,time_ms,status,solver" > "$output_csv"

TIMEOUT=120000
first_result=true

echo "Running Integer Model experiments..."
echo ""

for n in "${n_values[@]}"; do
    echo "Testing n=$n"
    
    echo "n = $n;" > temp_n${n}.dzn
    
    start_time=$(python3 -c 'import time; print(int(time.time() * 1000))')
    
    minizinc models/nqueens_integer.mzn temp_n${n}.dzn \
        --solver gecode \
        --time-limit $TIMEOUT \
        > temp_output_${n}.txt 2>&1
    
    end_time=$(python3 -c 'import time; print(int(time.time() * 1000))')
    elapsed_ms=$((end_time - start_time))
    
    if grep -q "q = " temp_output_${n}.txt; then
        status="SOLVED"
    else
        status="ERROR"
    fi
    
    if [ "$first_result" = true ]; then
        first_result=false
    else
        echo "," >> "$output_json"
    fi
    
    cat >> "$output_json" << EOF
  {
    "n": $n,
    "time": $(python3 -c "print($elapsed_ms / 1000)"),
    "time_ms": $elapsed_ms,
    "status": "$status",
    "solver": "gecode"
  }
EOF
    
    echo "$n,$elapsed_ms,$status,gecode" >> "$output_csv"
    
    elapsed_sec=$(python3 -c "print(f'{$elapsed_ms/1000:.3f}')")
    echo "  Status: $status, Time: ${elapsed_sec}s"
    
    if [ "$status" = "SOLVED" ] && [ $n -le 15 ]; then
        cp temp_output_${n}.txt solutions/solution_integer_n${n}.txt
    fi
done

echo "" >> "$output_json"
echo "]" >> "$output_json"

rm -f temp_n*.dzn temp_output_*.txt

echo ""
echo "Done. Results saved to:"
echo "  - $output_json"
echo "  - $output_csv"
