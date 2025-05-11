#!/usr/bin/env python3
"""
Main script for analyzing cyclomatic complexity of C functions.
"""
import os
import argparse
from data_extraction import extract_function_definitions
from complexity_analyzer import analyze_cyclomatic_complexity
from visualization import (
    plot_complexity_histogram, 
    plot_complexity_boxplot, 
    plot_cumulative_distribution
)
from analysis import (
    print_complexity_summary, 
    complexity_distribution_analysis,
    find_high_complexity_functions, 
    print_high_complexity_examples
)
from export import export_to_csv

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Analyze cyclomatic complexity of C functions.')
    parser.add_argument('--folder', type=str, default='data/train_real_simple_io/',
                        help='Folder containing .jsonl.zst files')
    parser.add_argument('--threshold', type=int, default=10,
                        help='Threshold for high complexity functions')
    parser.add_argument('--examples', type=int, default=5,
                        help='Number of high complexity function examples to show')
    parser.add_argument('--output', type=str, default='complexity_results.csv',
                        help='Output CSV file name')
    parser.add_argument('--visualize', action='store_true',
                        help='Generate visualizations')
    return parser.parse_args()

def main():
    """Main function for the script."""
    args = parse_arguments()
    
    # Find all .jsonl.zst files in the specified folder
    filepaths = [os.path.join(args.folder, f) for f in os.listdir(args.folder) 
                 if f.endswith('.jsonl.zst')]
    
    if not filepaths:
        print(f"Error: No .jsonl.zst files found in the folder {args.folder}")
        return
    
    # Extract function definitions from all files
    all_function_defs = []
    for filepath in filepaths:
        if os.path.exists(filepath):
            function_defs = extract_function_definitions(filepath)
            all_function_defs.extend(function_defs)
        else:
            print(f"Error: File not found at {filepath}")
    
    if not all_function_defs:
        print("No function definitions found in the files.")
        return
    
    print(f"Total number of function definitions found: {len(all_function_defs)}")
    print("Analyzing cyclomatic complexity...")
    
    # Analyze cyclomatic complexity
    complexities, functions_with_complexity = analyze_cyclomatic_complexity(all_function_defs)
    
    if not complexities:
        print("No valid functions found for complexity analysis.")
        return
    
    # Print complexity summary
    print_complexity_summary(complexities)
    
    # Analyze distribution by complexity category
    complexity_distribution_analysis(complexities)
    
    # Find functions with high complexity
    high_complexity_funcs = find_high_complexity_functions(
        functions_with_complexity, 
        threshold=args.threshold
    )
    print(f"\nFound {len(high_complexity_funcs)} functions with complexity >= {args.threshold}")
    
    # Print examples of high complexity functions
    print_high_complexity_examples(high_complexity_funcs, n=args.examples)
    
    # Export results to CSV
    export_to_csv(functions_with_complexity, args.output)
    print(f"\nResults exported to {args.output}")
    
    # Create visualizations if requested
    if args.visualize:
        plot_complexity_histogram(complexities)
        plot_complexity_boxplot(complexities)
        plot_cumulative_distribution(complexities)

if __name__ == "__main__":
    main()