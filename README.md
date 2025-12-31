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

| Method | Time (s) | Growth (8→100) | Variables | Scaling |
|--------|----------|----------------|-----------|---------|
| **Local Search** | 0.131 | 50.4× | 100 | Super-linear |
| **QUBO (discovery)** | 0.145 | 1.94× | 10,000 | Near-constant ⭐ |
| **Integer** | 0.254 | 2.15× | 100 | Near-constant ⭐ |
| **Boolean** | 2.383 | 9.57× | 10,000 | Sub-quadratic |
| **QUBO (total)** | 5.596 | 1.04× | 10,000 | API overhead |

### Main Findings

- **Integer Model**: Exceptional near-constant scaling (2.15×) validates power of global constraints
- **QUBO Model**: Rapid discovery (0.145s) with near-constant algorithmic growth (1.94×), but total time dominated by cloud API (~5.5s)
- **Local Search**: Fastest for small instances (n ≤ 40), but super-linear scaling (50.4×)
- **Boolean Model**: Sub-quadratic scaling (9.57×) demonstrates modern MIP solver capability

---

## Complete Results

| n | Boolean | Integer | QUBO (discovery) | QUBO (total) | Local Search | LS Iters |
|---|---------|---------|-----------------|--------------|--------------|----------|
| 8 | 0.249 | 0.118 | 0.075 | 5.394 | 0.003 | 5.4 |
| 10 | 0.149 | 0.112 | 0.059 | 5.345 | 0.001 | 6.5 |
| 15 | 0.164 | 0.114 | 0.059 | 5.345 | 0.001 | 7.3 |
| 20 | 0.188 | 0.118 | 0.055 | 5.360 | 0.003 | 10.2 |
| 25 | 0.179 | 0.120 | 0.063 | 5.325 | 0.004 | 12.5 |
| 30 | 0.202 | 0.125 | 0.063 | 5.309 | 0.007 | 14.7 |
| 40 | 0.246 | 0.222 | 0.070 | 5.338 | 0.014 | 19.6 |
| 50 | 0.489 | 0.176 | 0.083 | 5.450 | 0.022 | 21.5 |
| 60 | 0.885 | 0.230 | 0.100 | 5.625 | 0.033 | 26.3 |
| 70 | 0.899 | 0.200 | 0.124 | 5.876 | 0.052 | 32.4 |
| 80 | 1.164 | 0.199 | 0.101 | 5.730 | 0.071 | 36.6 |
| 90 | 1.419 | 0.215 | 0.119 | 5.671 | 0.096 | 40.9 |
| 100 | 2.383 | 0.254 | 0.145 | 5.596 | 0.131 | 45.7 |

*All times in seconds. QUBO shows both discovery time (internal) and total time (wall-clock). Local Search averaged over 10 trials.*

---

## Repository Structure

```
nqueens-comparative-study/
│
├── README.md                      # This file
│
├── config/                        # Solver configurations
│   └── gecode.msc
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
│   ├── integer_results.json
│   ├── qubo_results.json
│   ├── qubo_timeout_analysis.json
│   ├── local_search_results.json
│   └── unified_results.csv
│
├── figures/                       # Visualizations
│   ├── fig_performance_comparison.png/pdf
│   ├── fig_scalability_analysis.png/pdf
│   ├── fig_local_search_details.png/pdf
│   └── fig_qubo_timeout_analysis.png/pdf
│
├── scripts/                       # Experiment automation
│   ├── analyze_results.py
│   ├── run_all_experiments.sh
│   ├── test_*.sh
│   └── test_qubo_timeout_analysis.sh
│
└── solutions/                     # Example outputs
    ├── solution_boolean_n*.txt
    └── solution_integer_n*.txt
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
git clone https://github.com/yourusername/nqueens-comparative-study.git
cd nqueens-comparative-study

# Configure Amplify token (for QUBO)
export AMPLIFY_TOKEN="your_token_here"

# Run experiments
cd scripts
chmod +x *.sh
./run_all_experiments.sh

# Generate figures
cd ../results
python3 ../scripts/analyze_results.py
```

### Individual Methods

```bash
# Boolean
minizinc --solver cbc models/nqueens_boolean.mzn -D "n=20"

# Integer
minizinc --solver gecode models/nqueens_integer.mzn -D "n=20"

# QUBO
python3 models/nqueens_qubo_amplify.py --n 20

# Local Search
python3 models/nqueens_local_search.py --n 20 --trials 10
```

---

## Method Summary

### 1. Boolean Model (MiniZinc + COIN-BC)

**Formulation:**
- n² binary variables `board[i,j]`
- Constraints: one queen per row/column, at most one per diagonal

**Performance:** 2.383s @ n=100, 9.57× growth

**Best for:** Educational purposes, intuitive encoding

---

### 2. Integer Model (MiniZinc + Gecode)

**Formulation:**
- n integer variables `q[i]` = column of queen in row i
- Three `alldifferent` constraints (columns, diagonals, anti-diagonals)

**Performance:** 0.254s @ n=100, 2.15× growth (near-constant!)

**Why fast:** Gecode's `alldifferent` uses Régin's matching-based propagation

**Best for:** Large instances, production use

---

### 3. QUBO Model (Fixstars Amplify SDK)

**Formulation:**
- n² binary variables with penalty-based energy minimization
- Penalty weight w = 10.0, timeout 5000ms

**Performance:** 
- Discovery: 0.145s @ n=100, 1.94× growth
- Total: 5.596s @ n=100 (API overhead)

**Key insight:** Solutions found in first annealing cycle (~50-145ms), independent of timeout

**Best for:** Quantum computing research, QUBO studies

---

### 4. Local Search (Min-Conflicts)

**Formulation:**
- Permutation representation (implicit row/column satisfaction)
- Min-conflicts heuristic with random restart

**Performance:** 0.131s @ n=100, 50.4× growth (super-linear)

**Interesting:** Iterations grow sub-linearly (8.5×) but total time super-linearly due to O(n) per-iteration cost

**Best for:** Fast approximate solutions, small instances

---

## Practical Recommendations

| Use Case | Best Method | Why |
|----------|-------------|-----|
| **Large instances (n>50)** | Integer | Near-constant scaling |
| **Completeness required** | Integer | Systematic search |
| **Quick solutions (n≤40)** | Local Search | Fastest absolute time |
| **QUBO research** | QUBO | Relevant formulation |
| **Learning/teaching** | Boolean | Intuitive encoding |

---

## Experimental Setup

- **Hardware:** MacBook Pro M3, 16GB RAM
- **MiniZinc:** 2.9.4
- **Python:** 3.14.2
- **OS:** macOS

All results are reproducible (MiniZinc deterministic, QUBO/LS stochastic within expected variance).

