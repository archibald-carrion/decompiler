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

def analyze_lines_of_code(function_definitions):
    """Analyzes the number of lines of code in each function definition."""
    line_counts = [len(func.strip().split('\n')) for func in function_definitions]
    return line_counts

def plot_line_count_histogram(line_counts, title="Distribution of Lines of Code per Function"):
    """Plots a histogram of the number of lines of code."""
    plt.figure(figsize=(10, 6))
    plt.hist(line_counts, bins=50, edgecolor='black', alpha=0.7)
    plt.title(title)
    plt.xlabel("Number of Lines of Code")
    plt.ylabel("Frequency")
    plt.grid(axis='y', alpha=0.5)
    plt.show()

def plot_line_count_boxplot(line_counts, title="Box Plot of Lines of Code per Function"):
    """Plots a box plot of the number of lines of code."""
    plt.figure(figsize=(8, 6))
    plt.boxplot(line_counts, vert=False)
    plt.title(title)
    plt.xlabel("Number of Lines of Code")
    plt.show()

def plot_cumulative_distribution(line_counts, title="Cumulative Distribution of Lines of Code"):
    """Plots the cumulative distribution of the number of lines of code."""
    sorted_counts = np.sort(line_counts)
    cumulative_probability = np.arange(1, len(sorted_counts) + 1) / len(sorted_counts)
    plt.figure(figsize=(10, 6))
    plt.plot(sorted_counts, cumulative_probability, marker='.', linestyle='-')
    plt.title(title)
    plt.xlabel("Number of Lines of Code")
    plt.ylabel("Cumulative Probability")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    filepath = 'data/train_synth_compilable/data_0_time1677787985_default.jsonl.zst'
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}")
    else:
        function_defs = extract_function_definitions(filepath)
        if function_defs:
            line_counts = analyze_lines_of_code(function_defs)

            print(f"Total number of function definitions found: {len(function_defs)}")
            print(f"Summary of line counts:")
            print(f"  Mean: {np.mean(line_counts):.2f}")
            print(f"  Median: {np.median(line_counts):.2f}")
            print(f"  Standard Deviation: {np.std(line_counts):.2f}")
            print(f"  Minimum: {np.min(line_counts)}")
            print(f"  Maximum: {np.max(line_counts)}")
            print(f"  Percentiles (25th, 50th, 75th): {np.percentile(line_counts, [25, 50, 75])}")

            plot_line_count_histogram(line_counts)
            plot_line_count_boxplot(line_counts)
            plot_cumulative_distribution(line_counts)
        else:
            print("No function definitions found in the file.")