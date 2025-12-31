#!/bin/bash
# QUBO Timeout Sensitivity Analysis (Optional)
# Author: Lorenzo Domenico Attolico
# Student ID: 48259726

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
cd "$PROJECT_ROOT"

echo "QUBO Timeout Sensitivity Analysis"
echo "Author: Lorenzo Domenico Attolico (48259726)"
echo ""

# Test different timeout settings to verify solution discovery time
n_values=(8 15 20 25 30)
timeouts=(5000 10000 30000)

mkdir -p results

output_file="results/qubo_timeout_analysis.json"
echo "[" > "$output_file"

first_result=true

echo "Running timeout sensitivity experiments..."
echo ""

for timeout_ms in "${timeouts[@]}"; do
    timeout_sec=$((timeout_ms / 1000))
    echo "Testing with timeout=${timeout_sec}s"
    
    for n in "${n_values[@]}"; do
        echo "  n=$n"
        
        result=$(python3 -c "
import sys
import json

sys.path.insert(0, 'models')

try:
    from nqueens_qubo_amplify import solve_nqueens
    
    board, sol_time, total_time, obj, valid = solve_nqueens(
        n=$n, 
        penalty_weight=10.0, 
        timeout_ms=$timeout_ms
    )
    
    result = {
        'n': $n,
        'timeout_ms': $timeout_ms,
        'solution_time': sol_time,
        'total_time': total_time,
        'objective': obj,
        'valid': valid,
        'solved': (board is not None and valid)
    }
    
    print(json.dumps(result))
    
except Exception as e:
    result = {
        'n': $n,
        'timeout_ms': $timeout_ms,
        'solution_time': 0,
        'total_time': 0,
        'objective': float('inf'),
        'valid': False,
        'solved': False,
        'error': str(e)
    }
    print(json.dumps(result))
    sys.exit(1)
" 2>&1)
        
        if echo "$result" | python3 -c "import sys, json; json.load(sys.stdin)" > /dev/null 2>&1; then
            solved=$(echo "$result" | python3 -c "import sys, json; print(json.load(sys.stdin).get('solved', False))")
            sol_time=$(echo "$result" | python3 -c "import sys, json; d=json.load(sys.stdin); print(f\"{d.get('solution_time', 0):.3f}\")")
            
            if [ "$first_result" = true ]; then
                first_result=false
            else
                echo "," >> "$output_file"
            fi
            
            echo "$result" | python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin), indent=2))" >> "$output_file"
            
            if [ "$solved" = "True" ]; then
                echo "    Status: SOLVED, Time: ${sol_time}s"
            else
                echo "    Status: FAILED"
            fi
        else
            echo "    Status: ERROR"
        fi
        
        sleep 1
    done
    
    echo ""
done

echo "" >> "$output_file"
echo "]" >> "$output_file"

echo ""
echo "Done. Results saved to: $output_file"
