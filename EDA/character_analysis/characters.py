import zstandard as zstd
import json
import matplotlib.pyplot as plt
import numpy as np
import os

def extract_function_definitions(filepath):
    """Reads a .jsonl.zst file and extracts C function definitions."""
    function_definitions = []
    with open(filepath, 'rb') as f:
        dctx = zstd.ZstdDecompressor()
        stream_reader = dctx.stream_reader(f)
        text_stream = stream_reader.read().decode('utf-8')
        lines = text_stream.strip().split('\n')
        for line in lines:
            try:
                obj = json.loads(line)
                if "text" in obj and "func_def" in obj["text"]:
                    func_def = obj["text"]["func_def"]
                    function_definitions.append(func_def)
            except json.JSONDecodeError:
                continue
            except Exception as e:
                print(f"Error processing line: {e}")
    return function_definitions

def analyze_character_count(function_definitions):
    """Analyzes the number of characters in each function definition."""
    character_counts = [len(func) for func in function_definitions]
    return character_counts

def plot_character_count_histogram(character_counts, title="Distribution of Characters per Function"):
    """Plots a histogram of the number of characters."""
    plt.figure(figsize=(10, 6))
    plt.hist(character_counts, bins=50, edgecolor='black', alpha=0.7)
    plt.title(title)
    plt.xlabel("Number of Characters")
    plt.ylabel("Frequency")
    plt.grid(axis='y', alpha=0.5)
    plt.show()

def plot_character_count_boxplot(character_counts, title="Box Plot of Characters per Function"):
    """Plots a box plot of the number of characters."""
    plt.figure(figsize=(8, 6))
    plt.boxplot(character_counts, vert=False)
    plt.title(title)
    plt.xlabel("Number of Characters")
    plt.show()

def plot_cumulative_distribution(character_counts, title="Cumulative Distribution of Characters"):
    """Plots the cumulative distribution of the number of characters."""
    sorted_counts = np.sort(character_counts)
    cumulative_probability = np.arange(1, len(sorted_counts) + 1) / len(sorted_counts)
    plt.figure(figsize=(10, 6))
    plt.plot(sorted_counts, cumulative_probability, marker='.', linestyle='-')
    plt.title(title)
    plt.xlabel("Number of Characters")
    plt.ylabel("Cumulative Probability")
    plt.grid(True)
    plt.show()

def analyze_non_whitespace_character_count(function_definitions):
    """Analyzes the number of non-whitespace characters in each function definition."""
    non_ws_counts = [len(''.join(func.split())) for func in function_definitions]
    return non_ws_counts

def plot_comparison(character_counts, non_ws_counts, title="Comparison of Character Counts"):
    """Plots a scatter plot comparing total characters vs non-whitespace characters."""
    plt.figure(figsize=(10, 6))
    plt.scatter(character_counts, non_ws_counts, alpha=0.5)
    plt.title(title)
    plt.xlabel("Total Character Count")
    plt.ylabel("Non-whitespace Character Count")
    # Add a diagonal line representing equality
    max_val = max(max(character_counts), max(non_ws_counts))
    plt.plot([0, max_val], [0, max_val], 'r--', label='Equality Line')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    folder_path = 'data/train_real_simple_io/'
    filepaths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.jsonl.zst')]
    
    if not filepaths:
        print(f"Error: No .jsonl.zst files found in the folder {folder_path}")
    else:
        all_function_defs = []
        for filepath in filepaths:
            if os.path.exists(filepath):
                function_defs = extract_function_definitions(filepath)
                all_function_defs.extend(function_defs)
            else:
                print(f"Error: File not found at {filepath}")
        
        if all_function_defs:
            character_counts = analyze_character_count(all_function_defs)
            non_ws_counts = analyze_non_whitespace_character_count(all_function_defs)
            
            print(f"Total number of function definitions found: {len(all_function_defs)}")
            print(f"Summary of character counts:")
            print(f"  Mean: {np.mean(character_counts):.2f}")
            print(f"  Median: {np.median(character_counts):.2f}")
            print(f"  Standard Deviation: {np.std(character_counts):.2f}")
            print(f"  Minimum: {np.min(character_counts)}")
            print(f"  Maximum: {np.max(character_counts)}")
            print(f"  Percentiles (25th, 50th, 75th): {np.percentile(character_counts, [25, 50, 75])}")
            
            print(f"\nSummary of non-whitespace character counts:")
            print(f"  Mean: {np.mean(non_ws_counts):.2f}")
            print(f"  Median: {np.median(non_ws_counts):.2f}")
            print(f"  Standard Deviation: {np.std(non_ws_counts):.2f}")
            print(f"  Minimum: {np.min(non_ws_counts)}")
            print(f"  Maximum: {np.max(non_ws_counts)}")
            print(f"  Percentiles (25th, 50th, 75th): {np.percentile(non_ws_counts, [25, 50, 75])}")
            
            plot_character_count_histogram(character_counts)
            plot_character_count_boxplot(character_counts)
            plot_cumulative_distribution(character_counts)
            plot_comparison(character_counts, non_ws_counts)
        else:
            print("No function definitions found in the files.")