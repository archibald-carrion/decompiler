"""
Module for creating visualizations of complexity data.
"""
import matplotlib.pyplot as plt
import numpy as np

def plot_complexity_histogram(complexities, title="Distribution of Cyclomatic Complexity"):
    """
    Plots a histogram of the cyclomatic complexity.
    
    Args:
        complexities: List of complexity values
        title: Title for the plot
    """
    plt.figure(figsize=(10, 6))
    
    # Use dynamic bin size based on the range of complexities
    max_complexity = max(complexities)
    if max_complexity > 50:
        bin_edges = list(range(1, 21)) + list(range(25, 51, 5)) + list(range(60, max_complexity + 11, 10))
    else:
        bin_edges = range(1, max_complexity + 2)
    
    plt.hist(complexities, bins=bin_edges, edgecolor='black', alpha=0.7)
    plt.title(title)
    plt.xlabel("Cyclomatic Complexity")
    plt.ylabel("Frequency")
    plt.grid(axis='y', alpha=0.5)
    
    # Set reasonable x-ticks based on the range
    if max_complexity > 50:
        plt.xticks([1] + list(range(5, max_complexity + 1, 5)))
    else:
        plt.xticks(range(1, max_complexity + 1, 2))
        
    plt.savefig("complexity_histogram.png")
    plt.show()

def plot_complexity_boxplot(complexities, title="Box Plot of Cyclomatic Complexity"):
    """
    Plots a box plot of the cyclomatic complexity.
    
    Args:
        complexities: List of complexity values
        title: Title for the plot
    """
    plt.figure(figsize=(8, 6))
    plt.boxplot(complexities, vert=False)
    plt.title(title)
    plt.xlabel("Cyclomatic Complexity")
    plt.grid(axis='x', alpha=0.5)
    plt.savefig("complexity_boxplot.png")
    plt.show()

def plot_cumulative_distribution(complexities, title="Cumulative Distribution of Cyclomatic Complexity"):
    """
    Plots the cumulative distribution of the cyclomatic complexity.
    
    Args:
        complexities: List of complexity values
        title: Title for the plot
    """
    sorted_counts = np.sort(complexities)
    cumulative_probability = np.arange(1, len(sorted_counts) + 1) / len(sorted_counts)
    
    plt.figure(figsize=(10, 6))
    plt.plot(sorted_counts, cumulative_probability, marker='.', linestyle='-')
    plt.title(title)
    plt.xlabel("Cyclomatic Complexity")
    plt.ylabel("Cumulative Probability")
    plt.grid(True)
    plt.savefig("complexity_cumulative_distribution.png")
    plt.show()