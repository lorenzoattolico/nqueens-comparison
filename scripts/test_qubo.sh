#!/bin/bash
# Test script for N-Queens QUBO Model
# Author: Lorenzo Domenico Attolico
# Student ID: 48259726

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
cd "$PROJECT_ROOT"

echo "N-Queens QUBO Model Testing"
echo "Author: Lorenzo Domenico Attolico (48259726)"
echo ""

# Using 5s timeout (solutions found in ~50-80ms, rest is API overhead)
n_values=(8 10 15 20 25 30 40 50 60 70 80 90 100)

mkdir -p results

output_file="results/qubo_results.json"
echo "[" > "$output_file"

first_result=true

echo "Running QUBO Model experiments..."
echo ""

for n in "${n_values[@]}"; do
    echo "Testing n=$n"
    
    result=$(python3 -c "
import sys
import json

sys.path.insert(0, 'models')

try:
    from nqueens_qubo_amplify import solve_nqueens
    
    board, sol_time, total_time, obj, valid = solve_nqueens(
        n=$n, 
        penalty_weight=10.0, 
        timeout_ms=5000
    )
    
    result = {
        'n': $n,
        'solution_time': sol_time,
        'total_time': total_time,
        'objective': obj,
        'valid': valid,
        'solved': (board is not None and valid),
        'variables': $n * $n,
        'timeout_ms': 5000
    }
    
    print(json.dumps(result))
    
except Exception as e:
    result = {
        'n': $n,
        'solution_time': 0,
        'total_time': 0,
        'objective': float('inf'),
        'valid': False,
        'solved': False,
        'variables': $n * $n,
        'timeout_ms': 5000,
        'error': str(e)
    }
    print(json.dumps(result))
    sys.exit(1)
" 2>&1)
    
    if echo "$result" | python3 -c "import sys, json; json.load(sys.stdin)" > /dev/null 2>&1; then
        solved=$(echo "$result" | python3 -c "import sys, json; print(json.load(sys.stdin).get('solved', False))")
        sol_time=$(echo "$result" | python3 -c "import sys, json; d=json.load(sys.stdin); print(f\"{d.get('solution_time', 0):.3f}\")")
        total_time=$(echo "$result" | python3 -c "import sys, json; d=json.load(sys.stdin); print(f\"{d.get('total_time', 0):.3f}\")")
        
        if [ "$first_result" = true ]; then
            first_result=false
        else
            echo "," >> "$output_file"
        fi
        
        echo "$result" | python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin), indent=2))" >> "$output_file"
        
        if [ "$solved" = "True" ]; then
            echo "  Status: SOLVED, Solution time: ${sol_time}s, Total time: ${total_time}s"
        else
            echo "  Status: FAILED"
        fi
    else
        echo "  Status: ERROR"
        
        if [ "$first_result" = true ]; then
            first_result=false
        else
            echo "," >> "$output_file"
        fi
        
        error_json=$(python3 -c "import json; print(json.dumps({
            'n': $n,
            'solution_time': 0,
            'total_time': 0,
            'objective': float('inf'),
            'valid': False,
            'solved': False,
            'variables': $n * $n,
            'timeout_ms': 5000,
            'error': 'Execution failed'
        }, indent=2))")
        
        echo "$error_json" >> "$output_file"
    fi
    
    sleep 2
done

echo "" >> "$output_file"
echo "]" >> "$output_file"

echo ""
echo "Done. Results saved to: $output_file"
