#!/usr/bin/env python3
"""
N-Queens Problem - Results Analysis and Visualization
Author: Lorenzo Domenico Attolico
Student ID: 48259726

Generates figures from experimental results.
"""

import json
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 7)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['lines.markersize'] = 8


def load_data():
    """Load all experimental results."""
    print("Loading data...")
    
    # Boolean
    boolean_data = []
    try:
        with open('boolean_results.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                boolean_data.append({
                    'n': int(row['n']),
                    'time': float(row['time_ms']) / 1000.0,
                    'status': row['status']
                })
        print(f"  Boolean: {len(boolean_data)} instances")
    except FileNotFoundError:
        print("  Error: boolean_results.csv not found")
        sys.exit(1)
    
    # Integer
    try:
        with open('integer_results.json', 'r') as f:
            integer_data = json.load(f)
        print(f"  Integer: {len(integer_data)} instances")
    except FileNotFoundError:
        print("  Error: integer_results.json not found")
        sys.exit(1)
    
    # QUBO
    try:
        with open('qubo_results.json', 'r') as f:
            qubo_data = json.load(f)
        print(f"  QUBO: {len(qubo_data)} instances")
    except FileNotFoundError:
        print("  Warning: qubo_results.json not found, skipping")
        qubo_data = []
    
    # Local Search
    try:
        with open('local_search_results.json', 'r') as f:
            local_search_data = json.load(f)
        print(f"  Local Search: {len(local_search_data)} instances")
    except FileNotFoundError:
        print("  Error: local_search_results.json not found")
        sys.exit(1)
    
    # QUBO timeout (optional)
    qubo_timeout_data = None
    try:
        with open('qubo_timeout_analysis.json', 'r') as f:
            qubo_timeout_data = json.load(f)
        print(f"  QUBO Timeout Analysis: {len(qubo_timeout_data)} datapoints")
    except FileNotFoundError:
        pass
    
    return boolean_data, integer_data, qubo_data, local_search_data, qubo_timeout_data


def create_unified_table(boolean_data, integer_data, qubo_data, local_search_data):
    """Create unified comparison table."""
    print("Creating unified table...")
    
    n_values = sorted(set([d['n'] for d in boolean_data]))
    
    table_data = []
    for n in n_values:
        row = {'n': n}
        
        b = next((d for d in boolean_data if d['n'] == n), None)
        row['boolean_time'] = b['time'] if b else None
        row['boolean_status'] = b['status'] if b else None
        
        i = next((d for d in integer_data if d['n'] == n), None)
        row['integer_time'] = i['time'] if i else None
        row['integer_status'] = i['status'] if i else None
        
        q = next((d for d in qubo_data if d['n'] == n), None)
        row['qubo_solution_time'] = q['solution_time'] if q else None
        row['qubo_total_time'] = q['total_time'] if q else None
        row['qubo_status'] = 'SOLVED' if q and q['solved'] else 'FAILED' if q else None
        
        ls = next((d for d in local_search_data if d['n'] == n), None)
        row['ls_time'] = ls['avg_time'] if ls else None
        row['ls_success'] = ls['success_rate'] if ls else None
        row['ls_iterations'] = ls['avg_iterations'] if ls else None
        
        table_data.append(row)
    
    df = pd.DataFrame(table_data)
    df.to_csv('unified_results.csv', index=False)
    print(f"  Saved: unified_results.csv ({len(df)} instances)")
    
    return df


def create_performance_plot(df):
    """Create performance comparison plot."""
    print("Generating performance comparison...")
    
    os.makedirs('../figures', exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    n_vals = df['n'].values
    
    ax.plot(n_vals, df['boolean_time'], 'o-', label='Boolean Model (COIN-BC)', 
            linewidth=2, markersize=8, color='#1f77b4')
    ax.plot(n_vals, df['integer_time'], 's-', label='Integer Model (Gecode)', 
            linewidth=2, markersize=8, color='#ff7f0e')
    
    qubo_df = df[df['qubo_solution_time'].notna()]
    if not qubo_df.empty:
        ax.plot(qubo_df['n'], qubo_df['qubo_solution_time'], '^-', 
                label='QUBO Model (Amplify)', 
                linewidth=2, markersize=8, color='#2ca02c')
    
    ax.plot(n_vals, df['ls_time'], 'd-', label='Local Search (Min-Conflicts)', 
            linewidth=2, markersize=8, color='#d62728')
    
    ax.set_xlabel('Problem Size (n)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Time (seconds)', fontsize=13, fontweight='bold')
    ax.set_title('N-Queens: Performance Comparison', fontsize=15, fontweight='bold', pad=20)
    ax.legend(loc='upper left', fontsize=11)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig('../figures/fig_performance_comparison.png', dpi=300, bbox_inches='tight')
    plt.savefig('../figures/fig_performance_comparison.pdf', bbox_inches='tight')
    plt.close()
    
    print("  Saved: fig_performance_comparison.png, .pdf")


def create_scalability_plot(df):
    """Create scalability analysis plot."""
    print("Generating scalability analysis...")
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    n_vals = df['n'].values
    
    # Normalize to n=8
    n8_row = df[df['n'] == 8].iloc[0]
    
    bool_norm = df['boolean_time'] / n8_row['boolean_time']
    int_norm = df['integer_time'] / n8_row['integer_time']
    
    ax.plot(n_vals, bool_norm, 'o-', label='Boolean Model', linewidth=2, markersize=8)
    ax.plot(n_vals, int_norm, 's-', label='Integer Model', linewidth=2, markersize=8)

    qubo_df = df[df['qubo_solution_time'].notna()]
    if not qubo_df.empty and 8 in qubo_df['n'].values:
        qubo8 = qubo_df[qubo_df['n'] == 8].iloc[0]['qubo_solution_time']
        qubo_norm = qubo_df['qubo_solution_time'] / qubo8
        ax.plot(qubo_df['n'], qubo_norm, '^-', label='QUBO Model', linewidth=2, markersize=8)

    ls_norm = df['ls_time'] / n8_row['ls_time']
    ax.plot(n_vals, ls_norm, 'd-', label='Local Search', linewidth=2, markersize=8)
    
    ax.set_xlabel('Problem Size (n)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Normalized Time (relative to n=8)', fontsize=13, fontweight='bold')
    ax.set_title('N-Queens: Scalability Analysis', fontsize=15, fontweight='bold', pad=20)
    ax.legend(loc='upper left', fontsize=11)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig('../figures/fig_scalability_analysis.png', dpi=300, bbox_inches='tight')
    plt.savefig('../figures/fig_scalability_analysis.pdf', bbox_inches='tight')
    plt.close()
    
    print("  Saved: fig_scalability_analysis.png, .pdf")


def create_local_search_details_plot(df):
    """Create local search iteration analysis plot."""
    print("Generating local search details...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    n_vals = df['n'].values
    
    # Time plot
    ax1.plot(n_vals, df['ls_time'], 'o-', linewidth=2, markersize=8, color='#d62728')
    ax1.set_xlabel('Problem Size (n)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Average Time (seconds)', fontsize=12, fontweight='bold')
    ax1.set_title('Execution Time', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')
    
    # Iterations plot
    ax2.plot(n_vals, df['ls_iterations'], 's-', linewidth=2, markersize=8, color='#9467bd')
    ax2.set_xlabel('Problem Size (n)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Average Iterations', fontsize=12, fontweight='bold')
    ax2.set_title('Iteration Count', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.suptitle('Local Search (Min-Conflicts): Performance Details', 
                 fontsize=15, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('../figures/fig_local_search_details.png', dpi=300, bbox_inches='tight')
    plt.savefig('../figures/fig_local_search_details.pdf', bbox_inches='tight')
    plt.close()
    
    print("  Saved: fig_local_search_details.png, .pdf")


def create_qubo_timeout_plot(qubo_timeout_data):
    """Create QUBO timeout sensitivity plot."""
    if qubo_timeout_data is None:
        return
    
    print("Generating QUBO timeout analysis...")
    
    df_timeout = pd.DataFrame(qubo_timeout_data)
    df_timeout = df_timeout[df_timeout['solved'] == True]
    
    if df_timeout.empty:
        print("  Warning: No successful QUBO timeout data")
        return
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    timeouts = sorted(df_timeout['timeout_ms'].unique())
    colors = plt.cm.viridis(np.linspace(0, 0.8, len(timeouts)))
    
    # Solution time
    for i, timeout_ms in enumerate(timeouts):
        subset = df_timeout[df_timeout['timeout_ms'] == timeout_ms]
        ax1.plot(subset['n'], subset['solution_time'], 'o-', 
                label=f'{timeout_ms/1000:.0f}s timeout',
                linewidth=2, markersize=8, color=colors[i])
    
    ax1.set_xlabel('Problem Size (n)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Solution Discovery Time (seconds)', fontsize=12, fontweight='bold')
    ax1.set_title('Solution Time vs Timeout', fontsize=13, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Total time
    for i, timeout_ms in enumerate(timeouts):
        subset = df_timeout[df_timeout['timeout_ms'] == timeout_ms]
        ax2.plot(subset['n'], subset['total_time'], 's-', 
                label=f'{timeout_ms/1000:.0f}s timeout',
                linewidth=2, markersize=8, color=colors[i])
    
    ax2.set_xlabel('Problem Size (n)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Total Time (seconds)', fontsize=12, fontweight='bold')
    ax2.set_title('Total Time vs Timeout', fontsize=13, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    plt.suptitle('QUBO Timeout Sensitivity Analysis', 
                 fontsize=15, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('../figures/fig_qubo_timeout_analysis.png', dpi=300, bbox_inches='tight')
    plt.savefig('../figures/fig_qubo_timeout_analysis.pdf', bbox_inches='tight')
    plt.close()
    
    print("  Saved: fig_qubo_timeout_analysis.png, .pdf")


def main():
    """Main analysis pipeline."""
    print("\nN-Queens Analysis")
    print("Author: Lorenzo Domenico Attolico (48259726)\n")
    
    boolean_data, integer_data, qubo_data, local_search_data, qubo_timeout_data = load_data()
    
    df = create_unified_table(boolean_data, integer_data, qubo_data, local_search_data)
    
    create_performance_plot(df)
    create_scalability_plot(df)
    create_local_search_details_plot(df)
    create_qubo_timeout_plot(qubo_timeout_data)
    
    print("\nDone. Figures saved to ../figures/")


if __name__ == "__main__":
    main()
