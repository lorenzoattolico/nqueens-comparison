#!/usr/bin/env python3
"""
N-Queens Problem - Local Search with Min-Conflicts Heuristic
Author: Lorenzo Domenico Attolico
Student ID: 48259726

Min-Conflicts heuristic (Minton et al., 1992) with permutation representation.

Representation:
- board[i] = column position of queen in row i
- Permutation implicitly satisfies row and column constraints
- Only diagonal conflicts need to be minimized

Algorithm:
1. Initialize: random permutation (one queen per row, all different columns)
2. While conflicts exist and within iteration limit:
   - Select random queen with conflicts
   - Move to column position that minimizes total conflicts
3. Restart from new random configuration if iteration limit reached
"""

import sys
import time
import random
import numpy as np


def count_conflicts(board, n):
    """
    Count total number of diagonal conflicts (attacking queen pairs).
    
    Row and column conflicts are implicitly zero due to permutation.
    
    Args:
        board: Array where board[i] = column of queen in row i
        n: Board size
        
    Returns:
        int: Total number of diagonal conflicts
    """
    conflicts = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            # Check diagonal conflict: |row_diff| = |col_diff|
            if abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    
    return conflicts


def count_conflicts_for_queen(board, row, n):
    """
    Count conflicts for a specific queen.
    
    Args:
        board: Current board configuration
        row: Row of the queen to check
        n: Board size
        
    Returns:
        int: Number of conflicts for this queen
    """
    conflicts = 0
    col = board[row]
    
    for other_row in range(n):
        if other_row == row:
            continue
        
        other_col = board[other_row]
        
        # Check diagonal conflict
        if abs(col - other_col) == abs(row - other_row):
            conflicts += 1
    
    return conflicts


def get_best_column(board, row, n):
    """
    Find column position that minimizes conflicts for given row.
    
    Args:
        board: Current board configuration
        row: Row to optimize
        n: Board size
        
    Returns:
        int: Best column position (random choice among ties)
    """
    min_conflicts = float('inf')
    best_columns = []
    
    current_col = board[row]
    
    # Try all possible column positions
    for col in range(n):
        # Temporarily move queen to this column
        board[row] = col
        
        # Count resulting conflicts
        conflicts = count_conflicts_for_queen(board, row, n)
        
        if conflicts < min_conflicts:
            min_conflicts = conflicts
            best_columns = [col]
        elif conflicts == min_conflicts:
            best_columns.append(col)
    
    # Restore original position
    board[row] = current_col
    
    # Return random best column (tie-breaking)
    return random.choice(best_columns)


def solve_min_conflicts(n, max_iterations=10000, max_restarts=100):
    """
    Solve N-Queens using Min-Conflicts heuristic.
    
    Args:
        n: Board size
        max_iterations: Maximum iterations per restart
        max_restarts: Maximum number of restarts
        
    Returns:
        tuple: (board, iterations, restarts, success)
            - board: Solution array or None if failed
            - iterations: Total iterations used
            - restarts: Number of restarts used
            - success: Boolean indicating if solution found
    """
    
    for restart in range(max_restarts):
        # Random initialization: permutation ensures row/column constraints
        board = np.random.permutation(n)
        
        for iteration in range(max_iterations):
            # Check if solution found
            conflicts = count_conflicts(board, n)
            
            if conflicts == 0:
                return board.copy(), iteration + 1, restart + 1, True
            
            # Find all queens with conflicts
            conflicted_queens = []
            for row in range(n):
                if count_conflicts_for_queen(board, row, n) > 0:
                    conflicted_queens.append(row)
            
            if not conflicted_queens:
                # Should not happen if conflicts > 0, but safeguard
                continue
            
            # Select random conflicted queen
            row = random.choice(conflicted_queens)
            
            # Move to column that minimizes conflicts
            best_col = get_best_column(board, row, n)
            board[row] = best_col
    
    # Failed after all restarts
    return None, max_iterations * max_restarts, max_restarts, False


def run_multiple_trials(n, num_trials=10, max_iterations=10000, max_restarts=100):
    """
    Run multiple independent trials and collect statistics.
    
    Args:
        n: Board size
        num_trials: Number of independent trials
        max_iterations: Maximum iterations per restart
        max_restarts: Maximum restarts per trial
        
    Returns:
        dict: Statistics including times, iterations, restarts, success rate
    """
    
    results = {
        'times': [],
        'iterations': [],
        'restarts': [],
        'successes': 0
    }
    
    for trial in range(num_trials):
        start_time = time.time()
        
        board, iters, restarts, success = solve_min_conflicts(
            n, max_iterations, max_restarts
        )
        
        elapsed = time.time() - start_time
        
        if success:
            results['times'].append(elapsed)
            results['iterations'].append(iters)
            results['restarts'].append(restarts)
            results['successes'] += 1
    
    # Compute averages
    if results['successes'] > 0:
        results['avg_time'] = np.mean(results['times'])
        results['avg_iterations'] = np.mean(results['iterations'])
        results['avg_restarts'] = np.mean(results['restarts'])
        results['success_rate'] = (results['successes'] / num_trials) * 100
    else:
        results['avg_time'] = 0
        results['avg_iterations'] = 0
        results['avg_restarts'] = 0
        results['success_rate'] = 0
    
    return results


def print_board(board, n):
    """Print board in readable format with Q for queens, . for empty."""
    if board is None:
        print("No solution found")
        return
    
    for row in range(n):
        for col in range(n):
            if board[row] == col:
                print("Q", end=" ")
            else:
                print(".", end=" ")
        print()


if __name__ == "__main__":
    # Test with command line argument or default n=8
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    else:
        n = 8
    
    print(f"Solving {n}-Queens with Min-Conflicts (10 trials)")
    print("="*60)
    
    results = run_multiple_trials(n, num_trials=10)
    
    if results['successes'] > 0:
        print(f"\n✓ Success rate: {results['success_rate']:.0f}%")
        print(f"  Average time: {results['avg_time']:.6f}s")
        print(f"  Average iterations: {results['avg_iterations']:.0f}")
        print(f"  Average restarts: {results['avg_restarts']:.1f}")
        
        # Show one example solution
        print(f"\nExample solution:")
        board, _, _, _ = solve_min_conflicts(n)
        if board is not None:
            print_board(board, n)
    else:
        print(f"\n✗ No solutions found in {results['successes']} trials")
