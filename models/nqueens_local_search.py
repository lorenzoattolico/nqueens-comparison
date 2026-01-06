#!/usr/bin/env python3
"""
N-Queens Problem - Local Search with Min-Conflicts Heuristic (Optimized)
Author: Lorenzo Domenico Attolico
Student ID: 48259726

Min-Conflicts heuristic (Minton et al., 1992) with optimized implementation.

Representation:
- board[i] = column position of queen in row i
- Permutation implicitly satisfies row and column constraints
- Only diagonal conflicts need to be minimized

Optimization (as per Minton et al. 1992):
- Frequency arrays for O(1) conflict evaluation
- diag_conflicts[d]: number of queens on diagonal d (where d = row - col + n - 1)
- antidiag_conflicts[a]: number of queens on anti-diagonal a (where a = row + col)

Algorithm:
1. Initialize: random permutation with frequency arrays
2. While conflicts exist and within iteration limit:
   - Select queen with MOST conflicts (as per Lecture 7)
   - Swap with position that minimizes total conflicts
3. Restart from new random configuration if iteration limit reached

Complexity: O(n) per iteration
"""

import sys
import time
import random
import numpy as np


class MinConflictsBoard:
    """
    Optimized board representation with frequency arrays for O(1) conflict checking.
    """
    
    def __init__(self, n):
        """Initialize with random permutation and frequency arrays."""
        self.n = n
        self.board = np.random.permutation(n).tolist()
        
        # Frequency arrays for O(1) conflict lookup
        self.diag_conflicts = [0] * (2 * n - 1)
        self.antidiag_conflicts = [0] * (2 * n - 1)
        
        # Initialize frequency arrays
        for row in range(n):
            col = self.board[row]
            self.diag_conflicts[row - col + n - 1] += 1
            self.antidiag_conflicts[row + col] += 1
    
    def conflicts_at(self, row, col):
        """Count conflicts for a queen at position (row, col). O(1)"""
        diag_idx = row - col + self.n - 1
        antidiag_idx = row + col
        return max(0, self.diag_conflicts[diag_idx] + 
                   self.antidiag_conflicts[antidiag_idx] - 2)
    
    def total_conflicts(self):
        """Calculate total number of attacking pairs. O(n)"""
        total = 0
        for count in self.diag_conflicts:
            if count > 1:
                total += count * (count - 1) // 2
        for count in self.antidiag_conflicts:
            if count > 1:
                total += count * (count - 1) // 2
        return total
    
    def swap_queens(self, row1, row2):
        """Swap queens in two rows, updating frequency arrays. O(1)"""
        if row1 == row2:
            return
        
        col1 = self.board[row1]
        col2 = self.board[row2]
        
        # Remove both queens
        self.diag_conflicts[row1 - col1 + self.n - 1] -= 1
        self.antidiag_conflicts[row1 + col1] -= 1
        self.diag_conflicts[row2 - col2 + self.n - 1] -= 1
        self.antidiag_conflicts[row2 + col2] -= 1
        
        # Swap
        self.board[row1], self.board[row2] = self.board[row2], self.board[row1]
        
        # Add back in new positions
        self.diag_conflicts[row1 - col2 + self.n - 1] += 1
        self.antidiag_conflicts[row1 + col2] += 1
        self.diag_conflicts[row2 - col1 + self.n - 1] += 1
        self.antidiag_conflicts[row2 + col1] += 1


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


def get_best_swap(board_state, row):
    """
    Find best row to swap with to minimize conflicts.
    Uses swap strategy to maintain permutation property.
    
    Args:
        board_state: MinConflictsBoard object
        row: Row to find best swap for
        
    Returns:
        int: Best row to swap with (random choice among ties)
    """
    min_conflicts = float('inf')
    best_swaps = []
    
    current_col = board_state.board[row]
    
    # Try swapping with each other row
    for other_row in range(board_state.n):
        other_col = board_state.board[other_row]
        
        # Temporarily swap
        board_state.swap_queens(row, other_row)
        
        # Count conflicts for both affected queens
        conflicts = (board_state.conflicts_at(row, other_col) + 
                    board_state.conflicts_at(other_row, current_col))
        
        if conflicts < min_conflicts:
            min_conflicts = conflicts
            best_swaps = [other_row]
        elif conflicts == min_conflicts:
            best_swaps.append(other_row)
        
        # Swap back
        board_state.swap_queens(row, other_row)
    
    return random.choice(best_swaps)


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
        # Initialize board with frequency arrays
        board_state = MinConflictsBoard(n)
        
        for iteration in range(max_iterations):
            # Check if solution found
            if board_state.total_conflicts() == 0:
                return np.array(board_state.board), iteration + 1, restart + 1, True
            
            # Find queen(s) with MOST conflicts (as per Lecture 7)
            max_conf = 0
            most_conflicted_queens = []
            
            for row in range(n):
                conf = board_state.conflicts_at(row, board_state.board[row])
                if conf > max_conf:
                    max_conf = conf
                    most_conflicted_queens = [row]
                elif conf == max_conf and conf > 0:
                    most_conflicted_queens.append(row)
            
            if not most_conflicted_queens:
                # Should not happen if conflicts > 0, but safeguard
                continue
            
            # Select the most conflicting queen (random among ties)
            row = random.choice(most_conflicted_queens)
            
            # Find best row to swap with
            best_swap_row = get_best_swap(board_state, row)
            
            # Perform the swap
            board_state.swap_queens(row, best_swap_row)
    
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