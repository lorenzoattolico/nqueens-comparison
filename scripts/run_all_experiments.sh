#!/bin/bash
# Run all N-Queens experiments
# Lorenzo Domenico Attolico - 48259726

set -e

cd "$(dirname "$0")/.."

echo "Running all N-Queens experiments..."
echo "Student: Lorenzo Domenico Attolico (48259726)"
echo ""

# Quick checks
echo "Checking requirements..."
command -v minizinc >/dev/null 2>&1 || { echo "Error: MiniZinc not found"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "Error: Python3 not found"; exit 1; }
echo "OK"
echo ""

mkdir -p results figures

# Run experiments
echo "1. Boolean model (MiniZinc + COIN-BC)..."
if [ -f "scripts/test_boolean.sh" ]; then
    chmod +x scripts/test_boolean.sh
    scripts/test_boolean.sh
else
    echo "Warning: test_boolean.sh not found, skipping"
fi

echo ""
echo "2. Integer model (MiniZinc + Gecode)..."
if [ -f "scripts/test_integer.sh" ]; then
    chmod +x scripts/test_integer.sh
    scripts/test_integer.sh
else
    echo "Warning: test_integer.sh not found, skipping"
fi

echo ""
echo "3. QUBO model (Amplify)..."
if [ -f "scripts/test_qubo.sh" ]; then
    chmod +x scripts/test_qubo.sh
    scripts/test_qubo.sh
else
    echo "Warning: test_qubo.sh not found, skipping"
fi

echo ""
echo "4. Local search..."
if [ -f "scripts/test_local_search.sh" ]; then
    chmod +x scripts/test_local_search.sh
    scripts/test_local_search.sh
else
    echo "Warning: test_local_search.sh not found, skipping"
fi

# Analysis
echo ""
echo "Generating figures and statistics..."
if python3 -c "import pandas, matplotlib" 2>/dev/null; then
    if [ -f "scripts/analyze_results.py" ]; then
        cd results
        python3 ../scripts/analyze_results.py
        cd ..
        echo "Done"
    else
        echo "analyze_results.py not found, skipping"
    fi
else
    echo "pandas or matplotlib not installed, skipping analysis"
fi

echo ""
echo "All experiments complete!"
echo "Results in: results/"
echo "Figures in: figures/"