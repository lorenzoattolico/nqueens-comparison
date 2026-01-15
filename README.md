# N-Queens Problem: Comparative Study

**Author:** Lorenzo Domenico Attolico  
**Student ID:** 48259726  
**Course:** Special Lecture in Computer Science III  
**Institution:** Graduate School of Information Science and Technology, The University of Tokyo  
**Instructor:** Prof. Philippe Codognet  
**Date:** January 2026

---

## Overview

Comparative implementation and analysis of four algorithmic approaches to solving the N-Queens problem, completed as final project for the Combinatorial Optimization and Game AI course.

**Methods Implemented:**

1. **Boolean Model** - Mixed Integer Programming (MiniZinc + COIN-BC)
2. **Integer Model** - Constraint Programming with global constraints (MiniZinc + Gecode)
3. **QUBO Model** - Quantum-inspired annealing (Fixstars Amplify SDK)
4. **Local Search** - Min-Conflicts heuristic with random restart (Python)

**Experimental Range:** n = 8 to n = 100 (up to 10,000 binary variables)

**Success Rate:** 100% across all methods and instances

---

## Key Results

### Performance at n=100

| Method | Time (s) | Growth (8→100) |
|--------|----------|----------------|
| **Local Search** | 0.00393 | 1.29× |
| **QUBO (discovery)** | 0.145 | 1.65× |
| **Integer** | 0.263 | 2.04× |
| **Boolean** | 2.473 | 9.48× |
| **QUBO (total)** | 5.852 | 1.07× |

*Growth factor represents scaling from n=8 to n=100 (12.5× board size increase)*

### Main Findings

- **Integer Model**: 2.04× growth validates power of global constraints and specialized propagation
- **QUBO Model**: Competitive algorithmic performance (0.145s discovery, 1.65× growth), total time dominated by cloud API (~5.9s)
- **Local Search**: Fastest absolute times with optimized implementation (1.29× growth)
- **Boolean Model**: 9.48× growth despite 156× variable increase demonstrates MIP solver capability

---

## Complete Results

| n | Boolean | Integer | QUBO (sol) | QUBO (tot) | Local Search | LS Iters |
|---|---------|---------|------------|------------|--------------|----------|
| 8 | 0.261 | 0.129 | 0.088 | 5.457 | 0.00304 | 10.1 |
| 10 | 0.152 | 0.111 | 0.068 | 5.839 | 0.00132 | 16.1 |
| 15 | 0.162 | 0.112 | 0.059 | 5.316 | 0.00116 | 12.6 |
| 20 | 0.191 | 0.117 | 0.054 | 5.268 | 0.00161 | 16.7 |
| 25 | 0.183 | 0.120 | 0.063 | 5.408 | 0.00226 | 14.6 |
| 30 | 0.209 | 0.121 | 0.069 | 5.424 | 0.00248 | 20.2 |
| 40 | 0.256 | 0.134 | 0.070 | 5.507 | 0.00205 | 18.3 |
| 50 | 0.512 | 0.150 | 0.083 | 5.693 | 0.00230 | 21.6 |
| 60 | 0.937 | 0.161 | 0.100 | 5.564 | 0.00357 | 25.9 |
| 70 | 0.936 | 0.178 | 0.139 | 5.547 | 0.00231 | 27.7 |
| 80 | 1.205 | 0.203 | 0.101 | 5.788 | 0.00377 | 29.5 |
| 90 | 1.485 | 0.223 | 0.119 | 5.917 | 0.00600 | 32.0 |
| 100 | 2.473 | 0.263 | 0.145 | 5.852 | 0.00393 | 33.7 |

*All times in seconds. QUBO shows solution discovery time and total execution time. Local Search averaged over 10 trials.*

---

## Repository Structure
```
nqueens-comparison/
│
├── README.md                      # This file
├── report.pdf                     # Detailed analysis
│
├── models/                        # Source implementations
│   ├── nqueens_boolean.mzn
│   ├── nqueens_integer.mzn
│   ├── nqueens_qubo_amplify.py
│   └── nqueens_local_search.py
│
├── results/                       # Experimental data
│   ├── boolean_results.csv
│   ├── integer_results.csv
│   ├── qubo_results.json
│   ├── local_search_results.json
│   └── unified_results.csv
│
├── figures/                       # Visualizations
│   ├── fig_performance_comparison.png
│   └── fig_scalability_analysis.png
│
└── scripts/                       # Experiment automation
    ├── analyze_results.py
    └── run_experiments.sh
```

---

## Prerequisites

- **MiniZinc 2.6+** (includes COIN-BC and Gecode solvers)
- **Python 3.8+** with numpy, pandas, matplotlib
- **Fixstars Amplify SDK** (for QUBO experiments, requires free API token)

### Installation
```bash
# MiniZinc
brew install minizinc              # macOS
sudo snap install minizinc         # Linux
# or download from https://www.minizinc.org/

# Python dependencies
pip install numpy pandas matplotlib

# Amplify SDK (for QUBO)
pip install amplify
# Get token: https://amplify.fixstars.com/
```

---

## Running Experiments
```bash
# Clone repository
git clone https://github.com/lorenzoattolico/nqueens-comparison.git
cd nqueens-comparison

# Configure Amplify token (for QUBO)
export AMPLIFY_TOKEN="your_token_here"

# Run individual methods
cd models

# Boolean
minizinc --solver cbc nqueens_boolean.mzn -D "n=20"

# Integer
minizinc --solver gecode nqueens_integer.mzn -D "n=20"

# QUBO
python3 nqueens_qubo_amplify.py --n 20

# Local Search
python3 nqueens_local_search.py --n 20 --trials 10
```

---

## Method Summary

### 1. Boolean Model (MiniZinc + COIN-BC)

**Formulation:** n² binary variables with explicit row, column, and diagonal constraints

**Performance:** 2.473s @ n=100, 9.48× growth (156× variable increase)

**Solver:** COIN-BC branch-and-cut algorithm

---

### 2. Integer Model (MiniZinc + Gecode)

**Formulation:** n integer variables with three `alldifferent` global constraints

**Performance:** 0.263s @ n=100, 2.04× growth

**Solver:** Gecode with Régin's matching-based propagation for `alldifferent`

---

### 3. QUBO Model (Fixstars Amplify SDK)

**Formulation:** n² binary variables with penalty-based energy minimization (w = 10.0)

**Performance:** 
- Solution discovery: 0.145s @ n=100, 1.65× growth
- Total execution: 5.852s @ n=100 (includes API overhead)

**Solver:** Fixstars Amplify Annealing Engine (quantum-inspired)

---

### 4. Local Search (Min-Conflicts)

**Formulation:** Permutation representation with frequency array optimization

**Performance:** 0.00393s @ n=100, 1.29× growth

**Algorithm:** Min-conflicts heuristic with random restart (10,000 iterations max, 100 restarts)

---

## Experimental Setup

- **Hardware:** MacBook Pro M3, 16GB RAM
- **MiniZinc:** 2.8+
- **Python:** 3.8+
- **OS:** macOS

All experiments conducted with 120-second timeouts for MiniZinc solvers and 5-second timeout for QUBO. Local search results averaged over 10 independent trials.

---

## License

This project was completed as coursework for the University of Tokyo. Code is provided for educational and research purposes.