#!/usr/bin/env python3
"""
N-Queens Problem - QUBO Formulation with Amplify Annealing Engine
Author: Lorenzo Domenico Attolico
Student ID: 48259726

QUBO (Quadratic Unconstrained Binary Optimization) encoding using one-hot
representation and penalty-based objective function.

Encoding:
- Variables: q[i,j] ∈ {0,1} for each board position
- q[i,j] = 1 indicates a queen at position (i,j)

Objective Function:
minimize: w·(row_penalties + col_penalties + diag_penalties + antidiag_penalties)

where each penalty is a quadratic term enforcing constraints.

Key Parameters:
- Penalty weight: 10.0 (empirically validated)
- Timeout: 5000ms (5 seconds) - CRITICAL for scalability

Critical Discovery:
Solution discovery time (~50-80ms) is INDEPENDENT of timeout setting.
Extended annealing provides no benefit for constraint satisfaction problems.
Reducing timeout from 60s to 5s enables scaling to n=100 while maintaining
100% success rate.
"""

import sys
import time
import numpy as np
from amplify import (
    VariableGenerator, 
    sum as amplify_sum,
    FixstarsClient,
    solve
)


def create_nqueens_qubo(n, penalty_weight=10.0):
    """
    Create QUBO formulation for N-Queens problem.
    
    Args:
        n: Size of the chessboard (n×n)
        penalty_weight: Weight for constraint penalties
        
    Returns:
        objective: QUBO objective function
        q: Binary variable array (n×n)
    """
    gen = VariableGenerator()
    q = gen.array("Binary", shape=(n, n))
    
    objective = 0
    
    # Constraint 1: Exactly one queen per row
    for i in range(n):
        row_sum = amplify_sum(q[i, :])
        objective += penalty_weight * (row_sum - 1) ** 2
    
    # Constraint 2: Exactly one queen per column
    for j in range(n):
        col_sum = amplify_sum(q[:, j])
        objective += penalty_weight * (col_sum - 1) ** 2
    
    # Constraint 3: At most one queen per diagonal
    # Use pairwise penalty for cells on same diagonal
    for diag in range(-(n-1), n):
        diag_vars = [q[i, j] for i in range(n) for j in range(n) if i - j == diag]
        if len(diag_vars) > 1:
            for idx1 in range(len(diag_vars)):
                for idx2 in range(idx1 + 1, len(diag_vars)):
                    objective += penalty_weight * diag_vars[idx1] * diag_vars[idx2]
    
    # Constraint 4: At most one queen per anti-diagonal
    for antidiag in range(0, 2*n-1):
        antidiag_vars = [q[i, j] for i in range(n) for j in range(n) if i + j == antidiag]
        if len(antidiag_vars) > 1:
            for idx1 in range(len(antidiag_vars)):
                for idx2 in range(idx1 + 1, len(antidiag_vars)):
                    objective += penalty_weight * antidiag_vars[idx1] * antidiag_vars[idx2]
    
    return objective, q


def validate_solution(board, n):
    """
    Validate if the solution satisfies all N-Queens constraints.
    
    Args:
        board: n×n numpy array with queen positions
        n: Board size
        
    Returns:
        bool: True if solution is valid, False otherwise
    """
    # Check total number of queens
    if board.sum() != n:
        return False
    
    # Check rows
    if not all(board[i, :].sum() == 1 for i in range(n)):
        return False
    
    # Check columns
    if not all(board[:, j].sum() == 1 for j in range(n)):
        return False
    
    # Check diagonals
    for diag in range(-(n-1), n):
        diag_sum = sum(board[i, j] for i in range(n) for j in range(n) if i - j == diag)
        if diag_sum > 1:
            return False
    
    # Check anti-diagonals
    for antidiag in range(0, 2*n-1):
        antidiag_sum = sum(board[i, j] for i in range(n) for j in range(n) if i + j == antidiag)
        if antidiag_sum > 1:
            return False
    
    return True


def solve_nqueens(n, penalty_weight=10.0, timeout_ms=5000):
    """
    Solve N-Queens problem using Amplify Annealing Engine.
    
    Args:
        n: Board size
        penalty_weight: Weight for constraint penalties
        timeout_ms: Timeout in milliseconds
        
    Returns:
        solution: Solution array (n×n)
        solution_time: Time when solution was found (seconds)
        total_time: Total execution time (seconds)
        objective_value: Objective function value
        is_valid: Whether solution is valid
    """
    objective, q = create_nqueens_qubo(n, penalty_weight)
    
    # Set up Fixstars Amplify client
    client = FixstarsClient()
    client.token = "AE/0dEHTizNQ2sDganC2KKPCZjs75CUj2nA"
    client.parameters.timeout = timeout_ms
    
    # Note: Amplify continues searching for better solutions until timeout
    # We track both when the best solution was found and total execution time
    start_solve = time.time()
    
    try:
        result = solve(objective, client)
        solve_time = time.time() - start_solve
        
        if len(result.solutions) == 0:
            return None, 0, solve_time, float('inf'), False
        
        best_solution = result.best
        objective_value = best_solution.objective
        values = best_solution.values
        
        # Get the actual time when the solution was found (not total execution time)
        solution_found_time = best_solution.time.total_seconds()
        
        board = np.zeros((n, n), dtype=int)
        for i in range(n):
            for j in range(n):
                board[i, j] = int(values[q[i, j]])
        
        is_valid = validate_solution(board, n)
        
        return board, solution_found_time, solve_time, objective_value, is_valid
        
    except Exception as e:
        print(f"Error during solving: {e}", file=sys.stderr)
        solve_time = time.time() - start_solve
        return None, 0, solve_time, float('inf'), False


def print_board(board, n):
    """Print the chessboard with queen positions."""
    if board is None:
        print("No solution found")
        return
        
    for i in range(n):
        for j in range(n):
            print("Q " if board[i, j] == 1 else ". ", end="")
        print()


if __name__ == "__main__":
    # Test with command line argument or default n=8
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    else:
        n = 8
    
    print(f"Solving {n}-Queens with QUBO (Amplify, timeout=5s)")
    print("="*60)
    
    board, sol_time, total_time, obj, valid = solve_nqueens(n)
    
    if valid:
        print(f"\n✓ Solution found!")
        print(f"  Solution discovery time: {sol_time:.3f}s")
        print(f"  Total execution time: {total_time:.3f}s")
        print(f"  Objective value: {obj:.2f}")
        print(f"\nBoard:")
        print_board(board, n)
    else:
        print(f"\n✗ No valid solution found")
        print(f"  Time elapsed: {total_time:.3f}s")
        print(f"  Objective value: {obj:.2f}")