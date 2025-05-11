"""
Module for analyzing the complexity data.
"""
import numpy as np

def print_complexity_summary(complexities):
    """
    Prints summary statistics of the complexity values.
    
    Args:
        complexities: List of complexity values
    """
    print(f"\nSummary of cyclomatic complexity:")
    print(f"  Mean: {np.mean(complexities):.2f}")
    print(f"  Median: {np.median(complexities):.2f}")
    print(f"  Standard Deviation: {np.std(complexities):.2f}")
    print(f"  Minimum: {np.min(complexities)}")
    print(f"  Maximum: {np.max(complexities)}")
    print(f"  Percentiles (25th, 50th, 75th): {np.percentile(complexities, [25, 50, 75])}")

def complexity_distribution_analysis(complexities):
    """
    Analyzes the distribution of complexity values.
    
    Args:
        complexities: List of complexity values
    """
    print("\nComplexity distribution analysis:")
    
    categories = {
        "Low (1-10)": 0,
        "Moderate (11-20)": 0,
        "High (21-50)": 0,
        "Very High (>50)": 0
    }
    
    for c in complexities:
        if c <= 10:
            categories["Low (1-10)"] += 1
        elif c <= 20:
            categories["Moderate (11-20)"] += 1
        elif c <= 50:
            categories["High (21-50)"] += 1
        else:
            categories["Very High (>50)"] += 1
    
    total = len(complexities)
    for category, count in categories.items():
        percentage = (count / total) * 100
        print(f"  {category}: {count} functions ({percentage:.2f}%)")

def find_high_complexity_functions(functions_with_complexity, threshold=10):
    """
    Finds functions with high cyclomatic complexity.
    
    Args:
        functions_with_complexity: List of (function, complexity) tuples
        threshold: Minimum complexity to be considered "high"
        
    Returns:
        list: Sorted list of (function, complexity) tuples above threshold
    """
    high_complexity = [(func, complexity) for func, complexity in functions_with_complexity 
                      if complexity >= threshold]
    # Sort by complexity in descending order
    high_complexity.sort(key=lambda x: x[1], reverse=True)
    return high_complexity

def print_high_complexity_examples(high_complexity_funcs, n=5):
    """
    Prints examples of high complexity functions.
    
    Args:
        high_complexity_funcs: List of (function, complexity) tuples
        n: Number of examples to print
    """
    print(f"\nTop {min(n, len(high_complexity_funcs))} highest complexity functions:")
    
    for i, (func, complexity) in enumerate(high_complexity_funcs[:n]):
        # Get the first line of the function (usually contains the name)
        first_line = func.strip().split('\n')[0]
        print(f"{i+1}. Complexity: {complexity}, Function: {first_line[:80]}...")