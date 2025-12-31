#!/bin/bash
# Test script for N-Queens Local Search
# Author: Lorenzo Domenico Attolico
# Student ID: 48259726

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
cd "$PROJECT_ROOT"

echo "N-Queens Local Search Testing"
echo "Author: Lorenzo Domenico Attolico (48259726)"
echo ""

n_values=(8 10 15 20 25 30 40 50 60 70 80 90 100)

mkdir -p results

output_file="results/local_search_results.json"
echo "[" > "$output_file"

first_result=true

echo "Running Local Search experiments..."
echo ""

for n in "${n_values[@]}"; do
    echo "Testing n=$n (10 trials)"
    
    result=$(python3 -c "
import sys
import json
sys.path.insert(0, 'models')
from nqueens_local_search import run_multiple_trials

results = run_multiple_trials(
    n=$n, 
    num_trials=10, 
    max_iterations=10000, 
    max_restarts=100
)

output = {
    'n': $n,
    'avg_time': results['avg_time'],
    'avg_iterations': results['avg_iterations'],
    'avg_restarts': results['avg_restarts'],
    'success_rate': results['success_rate'],
    'num_trials': 10
}

print(json.dumps(output))
")
    
    avg_time=$(echo "$result" | python3 -c "import sys, json; print(f\"{json.load(sys.stdin)['avg_time']:.6f}\")")
    success=$(echo "$result" | python3 -c "import sys, json; print(f\"{json.load(sys.stdin)['success_rate']:.0f}\")")
    
    if [ "$first_result" = true ]; then
        first_result=false
    else
        echo "," >> "$output_file"
    fi
    
    echo "$result" | python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin), indent=2))" >> "$output_file"
    
    echo "  Success rate: ${success}%, Time: ${avg_time}s"
done

echo "" >> "$output_file"
echo "]" >> "$output_file"

echo ""
echo "Done. Results saved to: $output_file"
